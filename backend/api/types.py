import strawberry
from prisma import models
from typing_extensions import Self


def _get_version_string(version: models.Version) -> str:
    out = str(version.major)

    if version.minor is not None:
        out += f".{version.minor}"
        if version.patch is not None:
            out += f".{version.patch}"

    if version.build is not None:
        out += version.build

    return out


@strawberry.type
class Link:
    url: str
    name: str

    @classmethod
    def from_db(cls, link: models.Link, version: models.Version | None):
        url = (
            (
                link.url.replace("{version}", _get_version_string(version))
                .replace("{major}", str(version.major or ""))
                .replace("{minor}", str(version.minor or ""))
                .replace("{patch}", str(version.patch or ""))
            )
            if version
            else link.url
        )

        return cls(url=url, name=link.name)


@strawberry.type
class Software:
    id: strawberry.ID
    name: str
    slug: str
    links: list[Link]

    @classmethod
    def from_db(
        cls, software: models.Software, version: models.Version | None = None
    ) -> Self:
        return cls(
            id=strawberry.ID(str(software.id)),
            name=software.name,
            slug=software.slug,
            links=(
                [Link.from_db(link, version) for link in software.links]
                if software.links
                else []
            ),
        )


@strawberry.type
class SoftwareWithMajorVersions:
    software: Software
    major_versions: list[str]


@strawberry.type
class FindVersionResult:
    latest_version: str
    software: Software
