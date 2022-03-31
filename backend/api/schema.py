from __future__ import annotations

import strawberry
from config import database
from utils import Version


async def find_version(
    slug: str, version: str | None = None
) -> FindVersionResult | None:
    software_query = """
        SELECT slug, name FROM Software
        WHERE slug LIKE :q
            OR :q2 IN (
                select value
                from json_each(aliases)
            )
    """
    slug, software_name = await database.fetch_one(
        software_query, {"q": slug, "q2": slug}
    )

    """if slug is None:
        loop = asyncio.get_event_loop()
        loop.create_task(Notion.increment_counter(slug_q))
        return await four_oh_four(request)
    """

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

    if version:
        if not (filter_version := Version.from_string(version)):
            return None

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

    query = query.format(where)

    result = await database.fetch_one(query, values)

    if result is None:
        return None

    version = Version(*result)

    return FindVersionResult(
        latest_version=str(version), software=Software(name=software_name, slug=slug)
    )


@strawberry.type
class Software:
    name: str
    slug: str


@strawberry.type
class FindVersionResult:
    latest_version: str
    software: Software


@strawberry.type
class Query:
    find_version: FindVersionResult | None = strawberry.field(resolver=find_version)


schema = strawberry.Schema(query=Query)
