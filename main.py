from typing import Any
import logging
from fastapi import FastAPI, Request, Response, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, PlainTextResponse
from strawberry.asgi import GraphQL

from inertia import InertiaDep
from services.software import SoftwareService
from api.schema import schema

# Reduce watchfiles logging noise
logging.getLogger("watchfiles.main").setLevel(logging.WARNING)


class MyGraphQL(GraphQL):
    async def get_context(
        self,
        request: Request | WebSocket,
        response: Response | None = None,
    ) -> Any:
        return {}


graphql_app = MyGraphQL(schema, graphql_ide="apollo-sandbox")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/fonts", StaticFiles(directory="frontend/public/fonts"), name="fonts")

# Serve favicon files
import os
from fastapi.responses import FileResponse

@app.get("/favicon.{ext}")
async def favicon(ext: str):
    file_path = f"frontend/public/favicon.{ext}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "Not found"}

app.add_route("/graphql", graphql_app)

software_service = SoftwareService()


@app.get("/")
async def home(inertia: InertiaDep):
    # Fetch latest releases for the marquee
    releases = await software_service.get_latest_releases(limit=10)

    return inertia.render("Home", {
        "latestReleases": [
            {
                "name": f"{release.software_name} {release.version}",
                "url": f"/{release.software_slug}",
            }
            for release in releases
        ]
    })


def is_curl_request(request: Request) -> bool:
    """Check if the request is from curl or similar CLI tool"""
    user_agent = request.headers.get("user-agent", "").lower()
    return any(client in user_agent for client in ["curl", "wget", "httpie", "fetch"])


@app.get("/{software}")
async def software_page(software: str, request: Request, inertia: InertiaDep):
    # Split software name and version (e.g., "python@3.11")
    parts = software.split("@")
    query = parts[0]
    at_version_str = parts[1] if len(parts) > 1 else None

    # Find software using our service
    softwares = await software_service.find_softwares(query)

    # Handle no results
    if not softwares:
        if is_curl_request(request):
            return PlainTextResponse("not found", status_code=404)
        # Render NotFound page instead of redirecting
        releases = await software_service.get_latest_releases(limit=10)
        return inertia.render("NotFound", {
            "softwareName": query,
            "latestReleases": [
                {
                    "name": f"{release.software_name} {release.version}",
                    "url": f"/{release.software_slug}",
                }
                for release in releases
            ]
        })

    software_data = softwares[0]

    # Redirect to canonical slug if different
    if software_data.slug != query:
        redirect_url = f"/{software_data.slug}"
        if at_version_str:
            redirect_url += f"@{at_version_str}"
        return RedirectResponse(url=redirect_url, status_code=302)

    # Get version
    version = software_data.latest_version.as_string if software_data.latest_version else "unknown"

    # Handle version filtering (e.g., python@3.11)
    if at_version_str:
        version_parts = at_version_str.split(".")
        major = int(version_parts[0])
        minor = int(version_parts[1]) if len(version_parts) > 1 else None

        filtered_version = await software_service.find_version(
            software_data.slug, major, minor
        )
        if filtered_version:
            version = filtered_version

    # Return plain text for curl/CLI requests
    if is_curl_request(request):
        return PlainTextResponse(version)

    # Fetch latest releases for the marquee
    releases = await software_service.get_latest_releases(limit=10)

    return inertia.render(
        "Software",
        {
            "software": {
                "name": software_data.name,
                "slug": software_data.slug,
                "links": [
                    {"url": link.url, "name": link.name}
                    for link in software_data.links
                ],
            },
            "version": version,
            "requestedVersion": at_version_str,
            "latestReleases": [
                {
                    "name": f"{release.software_name} {release.version}",
                    "url": f"/{release.software_slug}",
                }
                for release in releases
            ]
        },
    )

