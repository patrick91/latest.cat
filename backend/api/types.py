from datetime import datetime
from typing import Protocol
import strawberry
from prisma import models
from typing_extensions import Self


class VersionProtocol(Protocol):
    major: int
    minor: int | None
    patch: int | None


def version_as_string(version: VersionProtocol) -> str:
    out = str(version.major)

    if version.minor is not None:
        out += f".{version.minor}"
        if version.patch is not None:
            out += f".{version.patch}"

    return out


@strawberry.type
class Link:
    url: str
    name: str

    @classmethod
    def from_db(cls, link: models.Link, version: models.Version | None):
        url = (
            (
                link.url.replace("{version}", version_as_string(version))
                .replace("{major}", str(version.major or ""))
                .replace("{minor}", str(version.minor or ""))
                .replace("{patch}", str(version.patch or ""))
            )
            if version
            else link.url
        )

        return cls(url=url, name=link.name)


@strawberry.type
class Version:
    major: int
    minor: int | None
    patch: int | None
    pushed_at: datetime

    @strawberry.field
    def as_string(self) -> str:
        return version_as_string(self)

    @classmethod
    def from_db(cls, version: models.Version):
        return cls(
            major=version.major,
            minor=version.minor,
            patch=version.patch,
            pushed_at=version.pushed_at,
        )


@strawberry.type
class Software:
    id: strawberry.ID
    name: str
    slug: str
    links: list[Link]
    latest_version: Version | None

    @classmethod
    def from_db(
        cls, software: models.Software, version: models.Version | None = None
    ) -> Self:
        latest_version = software.latest_version

        return cls(
            id=strawberry.ID(str(software.id)),
            name=software.name,
            slug=software.slug,
            links=(
                [Link.from_db(link, version) for link in software.links]
                if software.links
                else []
            ),
            latest_version=Version.from_db(latest_version) if latest_version else None,
        )


@strawberry.type
class SoftwareWithMajorVersions:
    software: Software
    major_versions: list[str]


@strawberry.type
class FindVersionResult:
    latest_version: str
    software: Software
