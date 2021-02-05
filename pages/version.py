import butter
from butter.render import render
from components.layout import root
from components.logo import logo
from components.title import title
from data.config import database
from starlette.responses import HTMLResponse, PlainTextResponse


async def fetch_latest(request):
    slug = request.path_params["slug"]
    version = request.path_params.get("version")

    query = """
        SELECT Version FROM Version
        INNER JOIN Software on Software.id = Version.Software
        WHERE Software.slug = :slug
    """

    values = {"slug": slug}
    if version:
        query += "AND Version.version like :version"
        values["version"] = f"{version}%"

    result = await database.fetch_one(query, values)

    if "curl/" in request.headers.get("user-agent"):
        return PlainTextResponse(result[0])

    content = root(f"latest.cat - latest version for {slug}") > [
        logo(),
        title()
        > [
            f"latest version for {slug} is ",
            butter.span(style="border-bottom: 4px solid currentColor;") > result[0],
        ],
    ]

    return HTMLResponse(render(content))
