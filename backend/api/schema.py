from collections import defaultdict

import strawberry
from datetime import datetime
from prisma.types import VersionWhereInput
from strawberry.types.info import Info

from .context import Context
from .types import FindVersionResult, Software, SoftwareWithMajorVersions


# TODO: this is bad, but I want to implement this quickly :)
@strawberry.type
class Release:
    version: str
    software_name: str
    software_slug: str
    pushed_at: datetime


@strawberry.type
class Query:
    @strawberry.field
    async def find_softwares(
        self, info: Info[Context, None], query: str
    ) -> list[Software]:
        softwares = await info.context["db"].software.find_many(
            where={
                "OR": [
                    {"name": {"contains": query}},
                    {"slug": {"contains": query}},
                    {"aliases": {"some": {"name": {"contains": query}}}},
                ]
            },
            include={"latest_version": True, "links": True},
        )
        aliases = await info.context["db"].alias.find_many(
            where={"name": {"contains": query}},
            include={"software": {"include": {"latest_version": True, "links": True}}},
        )

        all_softwares = {
            software.id: software
            for software in softwares
            + [alias.software for alias in aliases if alias.software]
        }

        all_softwares = sorted(
            all_softwares.values(),
            key=lambda s: s.name,
        )

        return [Software.from_db(software) for software in all_softwares]

    @strawberry.field
    async def find_version(
        self, info: Info[Context, None], slug: str, version: str | None = None
    ) -> FindVersionResult | None:
        software = await info.context["db"].software.find_unique(
            where={"slug": slug},
            include={"links": True, "latest_version": True},
        )

        if not software:
            alias = await info.context["db"].alias.find_first(
                where={"name": slug},
                include={"software": {"include": {"links": True}}},
            )

            if not alias:
                return None

            software = alias.software

            assert software

        where: VersionWhereInput = {"software_id": software.id}

        if version:
            major, *rest = version.split(".")

            where["major"] = int(major)

            if rest:
                where["minor"] = int(rest[0])

        latest_version = await info.context["db"].version.find_first(
            where=where,
            order=[{"major": "desc"}, {"minor": "desc"}, {"patch": "desc"}],
        )

        # TODO: handle this case better
        if not latest_version:
            return None

        latest_version_str = (
            f"{latest_version.major}.{latest_version.minor}.{latest_version.patch}"
        )

        return FindVersionResult(
            latest_version=latest_version_str,
            software=Software.from_db(software, latest_version),
        )

    @strawberry.field
    async def all_software(
        self, info: Info[Context, None]
    ) -> list[SoftwareWithMajorVersions]:
        database = info.context["db"]

        versions = await database.version.group_by(
            by=["software_id", "major"],
        )

        # TODO: this api doesn't make a lot of sense, might be better to return
        # all the versions for a software? 🤔

        ids = filter(None, [version.get("software_id") for version in versions])

        softwares = await database.software.find_many(
            where={"id": {"in": list(ids)}},
            include={"links": True, "latest_version": True},
        )

        major_versions_by_software = defaultdict[int, list[str]](list)

        for version in versions:
            software_id = version.get("software_id")

            if software_id is None:
                continue

            if software_id not in major_versions_by_software:
                major_versions_by_software[software_id] = []

            major_versions_by_software[software_id].append(str(version.get("major")))

        return [
            SoftwareWithMajorVersions(
                software=Software.from_db(software),
                major_versions=major_versions_by_software[software.id],
            )
            for software in softwares
        ]

    @strawberry.field
    async def latest_releases(self, info: Info[Context, None]) -> list[Release]:
        database = info.context["db"]

        data = await database.query_raw(
            """
            WITH RankedVersions AS (
                SELECT
                    v."id",
                    v."major",
                    v."minor",
                    v."patch",
                    v."build",
                    v."software_id",
                    v."pushed_at",
                    ROW_NUMBER() OVER (PARTITION BY v."software_id" ORDER BY v."pushed_at" DESC) as rn
                FROM "Version" v
            )
            SELECT
                rv."id",
                rv."major",
                rv."minor",
                rv."patch",
                rv."build",
                rv."software_id",
                s."name" AS software_name,
                s."slug" AS software_slug,
                rv."pushed_at"
            FROM RankedVersions rv
            JOIN "Software" s ON rv."software_id" = s."id"
            WHERE rv.rn = 1
            ORDER BY rv."pushed_at" DESC
            LIMIT 10;
            """
        )

        print(data)

        return [
            Release(
                version=f"{version['major']}.{version['minor']}.{version['patch']}",
                software_name=version["software_name"],
                software_slug=version["software_slug"],
                pushed_at=datetime.fromisoformat(version["pushed_at"]),
            )
            for version in data
        ]


schema = strawberry.Schema(query=Query)
