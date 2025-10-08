import strawberry
from datetime import datetime
from strawberry.types.info import Info

from services.software import SoftwareService
from .context import Context
from .types import FindVersionResult, Software, SoftwareWithMajorVersions


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
        service = SoftwareService()
        softwares = await service.find_softwares(query)
        return [Software.from_model(s) for s in softwares]

    @strawberry.field
    async def find_version(
        self, info: Info[Context, None], slug: str, version: str | None = None
    ) -> FindVersionResult | None:
        service = SoftwareService()
        software = await service.find_software_by_slug(slug)

        if not software:
            return None

        latest_version_str = None

        if version:
            major, *rest = version.split(".")
            minor = int(rest[0]) if rest else None

            latest_version_str = await service.find_version(
                slug, int(major), minor
            )
        else:
            if software.latest_version:
                latest_version_str = software.latest_version.as_string

        if not latest_version_str:
            return None

        return FindVersionResult(
            latest_version=latest_version_str,
            software=Software.from_model(software, software.latest_version),
        )

    @strawberry.field
    async def all_software(
        self, info: Info[Context, None]
    ) -> list[SoftwareWithMajorVersions]:
        service = SoftwareService()
        softwares = await service.get_all_software()

        result = []
        for software in softwares:
            major_versions = await service.get_major_versions(software.id)
            result.append(
                SoftwareWithMajorVersions(
                    software=Software.from_model(software),
                    major_versions=[str(v) for v in major_versions],
                )
            )

        return result

    @strawberry.field
    async def latest_releases(self, info: Info[Context, None]) -> list[Release]:
        service = SoftwareService()
        releases = await service.get_latest_releases(limit=10)

        return [
            Release(
                version=release.version,
                software_name=release.software_name,
                software_slug=release.software_slug,
                pushed_at=release.pushed_at,
            )
            for release in releases
        ]


schema = strawberry.Schema(query=Query)
