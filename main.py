import logging
import os
from typing import Any

from fastapi import FastAPI, Request, Response, WebSocket
from fastapi.responses import (
    FileResponse,
    PlainTextResponse,
    RedirectResponse,
    StreamingResponse,
)
from fastapi.staticfiles import StaticFiles
from strawberry.asgi import GraphQL

from api.schema import schema
from inertia.fastapi import InertiaDep
from services.og_image import OGImageGenerator
from services.og_meta import get_home_og_meta, get_software_og_meta
from services.software import SoftwareService

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


@app.get("/favicon.{ext}")
async def favicon(ext: str):
    file_path = f"frontend/public/favicon.{ext}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "Not found"}


app.add_route("/graphql", graphql_app)

software_service = SoftwareService()
og_image_generator = OGImageGenerator()


@app.get("/")
async def home(request: Request, inertia: InertiaDep):
    # Fetch latest releases for the marquee
    releases = await software_service.get_latest_releases(limit=10)

    # Determine base URL
    is_local = request.url.hostname == "localhost"
    base_url = "http://localhost:8000" if is_local else "https://latest.cat"

    return inertia.render(
        "Home",
        props={
            "latestReleases": [
                {
                    "name": f"{release.software_name} {release.version}",
                    "url": f"/{release.software_slug}",
                }
                for release in releases
            ]
        },
        view_data={"og_meta": get_home_og_meta(base_url)},
    )


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

    # Determine base URL
    is_local = request.url.hostname == "localhost"
    base_url = "http://localhost:8000" if is_local else "https://latest.cat"

    # Find software using our service
    softwares = await software_service.find_softwares(query)

    # Handle no results
    if not softwares:
        if is_curl_request(request):
            return PlainTextResponse("not found", status_code=404)
        # Render NotFound page instead of redirecting
        releases = await software_service.get_latest_releases(limit=10)
        return inertia.render(
            "NotFound",
            {
                "softwareName": query,
                "latestReleases": [
                    {
                        "name": f"{release.software_name} {release.version}",
                        "url": f"/{release.software_slug}",
                    }
                    for release in releases
                ],
            },
        )

    software_data = softwares[0]

    # Redirect to canonical slug if different
    if software_data.slug != query:
        redirect_url = f"/{software_data.slug}"
        if at_version_str:
            redirect_url += f"@{at_version_str}"
        return RedirectResponse(url=redirect_url, status_code=302)

    # Get version
    version = (
        software_data.latest_version.as_string
        if software_data.latest_version
        else "unknown"
    )

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
        props={
            "software": {
                "name": software_data.name,
                "slug": software_data.slug,
                "links": [
                    {"url": link.url, "name": link.name} for link in software_data.links
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
            ],
        },
        view_data={
            "og_meta": get_software_og_meta(
                base_url=base_url,
                path=request.url.path,
                software_name=software_data.name,
                software_slug=software_data.slug,
                version=version,
            )
        },
    )


@app.get("/og-image/{software}.png")
async def og_image_software(software: str):
    """Generate OG image for software page"""
    # Find software using our service
    softwares = await software_service.find_softwares(software)

    if not softwares:
        # Redirect to static home image for unknown software
        return RedirectResponse(url="/static/og-home.png")

    software_data = softwares[0]
    version = (
        software_data.latest_version.as_string
        if software_data.latest_version
        else "unknown"
    )

    image_bytes = og_image_generator.generate_software_image(
        software_name=software_data.name, version=version
    )

    return StreamingResponse(
        iter([image_bytes]),
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=3600"},
    )
