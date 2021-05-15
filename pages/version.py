from starlette.responses import HTMLResponse, PlainTextResponse

import asyncio
import butter
from butter.render import render
from components.layout import root
from components.logo import logo
from components.title import title
from data.config import database
from data.utils import Version

from .four_oh_four import four_oh_four
from data.notion import Notion


async def fetch_latest(request):
    slug_q = request.path_params["slug"]
    version_q = request.path_params.get("version")

    query = """
        SELECT slug FROM Software
        WHERE slug LIKE :q
            OR :q2 IN (
                select value
                from json_each(aliases)
            )
    """
    slug = await database.fetch_val(query, {"q": slug_q, "q2": slug_q})
    if slug is None:
        loop = asyncio.get_event_loop()
        loop.create_task(Notion.increment_counter(slug_q))
        return await four_oh_four(request)

    query = """
        SELECT major, minor, revision, build FROM Version
        INNER JOIN Software on Software.id = Version.Software
        WHERE Software.slug = :slug {}
        ORDER BY
            Version.major DESC,
            Version.minor DESC,
            Version.revision DESC,
            Version.build DESC
    """

    where = ""
    values = {"slug": slug}

    if version_q:
        filter_version = Version.from_string(version_q)
        if filter_version:
            if filter_version.major is not None:
                where += " AND Version.major = :major"
                values["major"] = filter_version.major
            if filter_version.minor is not None:
                where += " AND Version.minor = :minor"
                values["minor"] = filter_version.minor
            if filter_version.revision is not None:
                where += " AND Version.revision = :revision"
                values["revision"] = filter_version.revision
            if filter_version.build is not None:
                where += " AND Version.build like :build"
                values["build"] = f"{filter_version.build}%"
        else:
            return await four_oh_four(request)

    query = query.format(where)

    result = await database.fetch_one(query, values)

    if result is None:
        return await four_oh_four(request)

    version = Version(*result)

    if "curl/" in request.headers.get("user-agent"):
        return PlainTextResponse(str(version))

    version_q = f"{version_q} " if version_q else ""
    content = root(f"latest.cat - latest version for {slug}") > [
        logo(),
        title()
        > [
            f"latest version for {slug} {version_q}is ",
            butter.span(style="border-bottom: 4px solid currentColor;") > str(version),
        ],
    ]

    return HTMLResponse(render(content))
