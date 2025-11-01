from datetime import datetime

from pydantic import BaseModel


class Link(BaseModel):
    id: int
    name: str
    url: str
    software_id: int


class Version(BaseModel):
    id: int
    major: int
    minor: int | None
    patch: int | None
    build: str | None
    software_id: int
    pushed_at: datetime

    @property
    def as_string(self) -> str:
        """Format version as string (e.g., '3.12.1')"""
        parts = [str(self.major)]
        if self.minor is not None:
            parts.append(str(self.minor))
        if self.patch is not None:
            parts.append(str(self.patch))
        version = ".".join(parts)
        if self.build:
            version += f"+{self.build}"
        return version


class Software(BaseModel):
    id: int
    name: str
    slug: str
    latest_version_id: int | None = None
    latest_version: Version | None = None
    links: list[Link] = []
