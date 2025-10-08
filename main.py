from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from inertia import InertiaDep
from services.software import SoftwareService


# TODO: Re-enable GraphQL when we migrate to SQLModel/plain SQL
# from typing import Any
# from fastapi import Request, Response, WebSocket
# from strawberry.asgi import GraphQL
# from api.schema import schema
#
# class MyGraphQL(GraphQL):
#     async def get_context(
#         self,
#         request: Request | WebSocket,
#         response: Response | None = None,
#     ) -> Any:
#         return {"request": request, "response": response}
#
# graphql_app = MyGraphQL(schema, graphql_ide="apollo-sandbox")


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# app.add_route("/graphql", graphql_app)

software_service = SoftwareService()


@app.get("/")
async def home(inertia: InertiaDep):
    return inertia.render("Home", {})


@app.get("/{software}")
async def software_page(software: str, inertia: InertiaDep):
    # Split software name and version (e.g., "python@3.11")
    parts = software.split("@")
    query = parts[0]
    at_version_str = parts[1] if len(parts) > 1 else None

    # Find software using our service
    softwares = await software_service.find_softwares(query)

    # Handle no results
    if not softwares:
        return RedirectResponse(url="/404", status_code=302)

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
        },
    )

