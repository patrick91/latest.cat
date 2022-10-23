from collections import defaultdict

import strawberry
from prisma.types import VersionWhereInput
from strawberry.types.info import Info

from .context import Context
from .types import FindVersionResult, Software, SoftwareWithMajorVersions


@strawberry.type
class Query:
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


schema = strawberry.Schema(query=Query)
