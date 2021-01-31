from __future__ import annotations

import yaml
import re
import uuid
import json
import logging

from github import Github
from typing import Iterator, Optional, List, Tuple
from dataclasses import dataclass
from databases import Database
from asyncio import run


logging.basicConfig(level=logging.INFO)

github = Github("TOKEN", per_page=100)

database_path = "../../../db.sqlite"
database = Database(f"sqlite:///{database_path}")


@dataclass
class Version:
    version: str
    pre: Optional[bool]


@dataclass
class Software:
    name: str
    aliases: List[str]
    slug: str
    source: str
    version_naming: str
    repository: Optional[str]

    _namings = {
        # https://github.com/rust-lang/rust/tags
        "basic": re.compile(r"^(\d+\.\d+(?:\.\d+)?)$"),
        # https://github.com/python/cpython/tags
        "python": re.compile(r"^v?(\d+\.\d+(?:\.\d+)?)$"),
        # "python_pre": re.compile(r"^v?(\d+\.\d+(?:\.\w+)?)$"),
        # https://github.com/php/php-src/tags
        "php": re.compile(r"^php-?(\d+\.\d+(?:\.\d+)?)$"),
        # "php_pre": re.compile(r"^php-?(\d+\.\d+(?:\.\w+)?)$"),
        # https://github.com/apple/swift/tags
        "swift": re.compile(r"^swift-(\d+\.\d+(?:\.\d+)?)-RELEASE$"),
        # https://github.com/golang/go/tags
        "go": re.compile(r"^go(\d+\.\d+(?:\.\d+)?)$"),
        # "go_pre": re.compile(r"^go(\d+\.\d+(?:\.\d+)?\w+)$"),
    }

    async def get_saved_versions(self) -> List[Version]:
        versions: List[Version] = []
        query = """
            select version, pre
            from Version
            where software = :software_id
        """

        results = await database.fetch_all(
            query=query, values={"software_id": await self.get_id()}
        )

        for result in results:
            versions.append(Version(version=result[0], pre=bool(result[1])))
        return versions

    def _fetch_github(self) -> Iterator[Version]:
        tags = github.get_repo(self.repository).get_tags()
        pattern = self._namings.get(self.version_naming)
        pre_pattern = self._namings.get(self.version_naming + "_pre")

        for tag in tags:
            match = pattern.findall(tag.name)
            if match:
                yield Version(match[0], False)
            elif pre_pattern:
                match = pre_pattern.findall(tag.name)
                if match:
                    yield Version(match[0], True)

    def fetch_versions(self) -> Iterator[Version]:
        fun = getattr(self, f"_fetch_{self.source}")
        return fun()

    async def get_id(self) -> str:
        query = """
            select id
            from Software
            where slug = :slug
        """
        return await database.fetch_val(query=query, values={"slug": self.slug})

    async def save(self) -> Tuple[str, str, str, str]:
        query = """
            select id
            from Software
            where slug = :slug
        """
        current_id = await self.get_id()
        if current_id:
            query = """
                update Software
                set name = :name, aliases = :aliases
                where id = :id
            """
            values = {
                "name": self.name,
                "aliases": json.dumps(self.aliases),
                "id": current_id,
            }
        else:
            software_id = uuid.uuid4()
            query = """
                insert into Software(id, name, slug, aliases)
                values (:id, :name, :slug, :aliases)
            """
            values = {
                "name": self.name,
                "slug": self.slug,
                "aliases": json.dumps(self.aliases),
                "id": str(software_id),
            }
        await database.execute(query=query, values=values)

        query = """
            select id, name, slug, aliases
            from Software
            where slug = :slug
        """
        return await database.fetch_one(query=query, values={"slug": self.slug})

    async def add_versions(self) -> int:
        software_id = await self.get_id()
        query = """
            select v.version
            from Version v
            join Software s on s.id = v.software
            where s.slug = :slug
        """
        saved_versions = await database.fetch_all(
            query=query, values={"slug": self.slug}
        )
        saved_versions = [v[0] for v in saved_versions]

        fetched_versions = self.fetch_versions()

        new_versions = [v for v in fetched_versions if v.version not in saved_versions]

        query = """
            insert into Version(software, version, pre)
            values(:software, :version, :pre)
        """
        values = [
            {"software": software_id, "version": v.version, "pre": v.pre}
            for v in new_versions
        ]
        await database.execute_many(query=query, values=values)

        return len(new_versions)


async def main():
    await database.connect()

    with open("software.yml", "r") as yml:
        software_list = yaml.safe_load(yml)

    for s in software_list:
        software = Software(**s)

        await software.save()
        added_versions = await software.add_versions()
        logging.info(f"{software.name} - Added {added_versions} versions")


if __name__ == "__main__":
    run(main())
