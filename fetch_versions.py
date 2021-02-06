from __future__ import annotations

import json
import logging
import re
import uuid
from asyncio import run
from dataclasses import dataclass
from typing import Iterator, List, Optional, Tuple

import yaml
from databases import Database
from github import Github
from data.utils import Version

logging.basicConfig(level=logging.INFO)

github = Github("38fc66afc7ce30d9fcd0559c9aaf9b5b924b2464", per_page=100)

database_path = "db.sqlite"
database = Database(f"sqlite:///{database_path}")


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
        "basic": re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?$"),
        # https://github.com/python/cpython/tags
        "python": re.compile(r"^v?(\d+)\.(\d+)(?:\.(\d+))?$"),
        # https://github.com/php/php-src/tags
        "php": re.compile(r"^php-?(\d+)\.(\d+)(?:\.(\d+))?$"),
        # https://github.com/apple/swift/tags
        "swift": re.compile(r"^swift-(\d+)\.(\d+)(?:\.(\d+))?-RELEASE$"),
        # https://github.com/golang/go/tags
        "go": re.compile(r"^go(\d+)\.(\d+)(?:\.(\d+))?$"),
    }

    def _fetch_github(self) -> Iterator[Version]:
        tags = github.get_repo(self.repository).get_tags()
        pattern = self._namings.get(self.version_naming)

        for tag in tags:
            match = pattern.findall(tag.name)
            if match:
                match = [int(x) if x else None for x in match[0]]
                yield Version(*match)

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
            select v.major, v.minor, v.revision, v.build
            from Version v
            join Software s on s.id = v.software
            where s.slug = :slug
        """
        result = await database.fetch_all(query=query, values={"slug": self.slug})
        saved_versions = [Version(*v) for v in result]

        fetched_versions = self.fetch_versions()

        new_versions = [v for v in fetched_versions if v not in saved_versions]

        query = """
            insert into Version(software, major, minor, revision, build)
            values(:software, :major, :minor, :revision, :build)
        """
        values = [
            {
                "software": software_id,
                "major": v.major,
                "minor": v.minor,
                "revision": v.revision,
                "build": v.build,
            }
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
