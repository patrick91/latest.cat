from datetime import datetime

import aiosqlite
from sql_tstring import sql

from models import Link, Software, Version


class Release:
    """Release information for latest releases query"""

    def __init__(
        self, version: str, software_name: str, software_slug: str, pushed_at: datetime
    ):
        self.version = version
        self.software_name = software_name
        self.software_slug = software_slug
        self.pushed_at = pushed_at


class SoftwareService:
    def __init__(self, db_path: str = "db.sqlite"):
        self.db_path = db_path

    async def find_softwares(self, query: str) -> list[Software]:
        """
        Find software by name, slug, or alias.
        Returns a list of matching software with their latest version and links.
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            # Search in software table (name or slug) and aliases
            search_query = f"%{query}%"
            sql_query, values = sql(
                t"""
                SELECT DISTINCT s.id, s.name, s.slug, s.latest_version_id
                FROM Software s
                LEFT JOIN Alias a ON a.software_id = s.id
                WHERE s.name LIKE {search_query}
                   OR s.slug LIKE {search_query}
                   OR a.name LIKE {search_query}
                ORDER BY s.name
                """
            )
            cursor = await db.execute(sql_query, values)

            rows = await cursor.fetchall()

            if not rows:
                return []

            softwares = []
            for row in rows:
                software_dict = dict(row)

                # Fetch latest version
                if software_dict["latest_version_id"]:
                    version_id = software_dict["latest_version_id"]
                    version_query, version_values = sql(
                        t"""
                        SELECT id, major, minor, patch, build, software_id, pushed_at
                        FROM Version
                        WHERE id = {version_id}
                        """
                    )
                    version_cursor = await db.execute(version_query, version_values)
                    version_row = await version_cursor.fetchone()
                    if version_row:
                        software_dict["latest_version"] = Version(**dict(version_row))

                # Fetch links
                software_id = software_dict["id"]
                links_query, links_values = sql(
                    t"""
                    SELECT id, name, url, software_id
                    FROM Link
                    WHERE software_id = {software_id}
                    """
                )
                links_cursor = await db.execute(links_query, links_values)
                links_rows = await links_cursor.fetchall()
                software_dict["links"] = [Link(**dict(row)) for row in links_rows]

                softwares.append(Software(**software_dict))

            return softwares

    async def find_software_by_slug(self, slug: str) -> Software | None:
        """
        Find a specific software by its slug.
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            sql_query, values = sql(
                t"""
                SELECT id, name, slug, latest_version_id
                FROM Software
                WHERE slug = {slug}
                """
            )
            cursor = await db.execute(sql_query, values)

            row = await cursor.fetchone()
            if not row:
                return None

            software_dict = dict(row)

            # Fetch latest version
            if software_dict["latest_version_id"]:
                version_id = software_dict["latest_version_id"]
                version_query, version_values = sql(
                    t"""
                    SELECT id, major, minor, patch, build, software_id, pushed_at
                    FROM Version
                    WHERE id = {version_id}
                    """
                )
                version_cursor = await db.execute(version_query, version_values)
                version_row = await version_cursor.fetchone()
                if version_row:
                    software_dict["latest_version"] = Version(**dict(version_row))

            # Fetch links
            software_id = software_dict["id"]
            links_query, links_values = sql(
                t"""
                SELECT id, name, url, software_id
                FROM Link
                WHERE software_id = {software_id}
                """
            )
            links_cursor = await db.execute(links_query, links_values)
            links_rows = await links_cursor.fetchall()
            software_dict["links"] = [Link(**dict(row)) for row in links_rows]

            return Software(**software_dict)

    async def find_version(
        self, slug: str, major: int, minor: int | None = None
    ) -> str | None:
        """
        Find the latest version for a software matching the major (and optionally minor) version.
        Returns the version string.
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            # First get the software
            sql_query, values = sql(
                t"""
                SELECT id FROM Software WHERE slug = {slug}
                """
            )
            cursor = await db.execute(sql_query, values)
            software_row = await cursor.fetchone()
            if not software_row:
                return None

            software_id = software_row["id"]

            # Build the version query
            if minor is not None:
                version_query, version_values = sql(
                    t"""
                    SELECT major, minor, patch, build
                    FROM Version
                    WHERE software_id = {software_id}
                      AND major = {major}
                      AND minor = {minor}
                    ORDER BY major DESC, minor DESC, patch DESC
                    LIMIT 1
                    """
                )
                version_cursor = await db.execute(version_query, version_values)
            else:
                version_query, version_values = sql(
                    t"""
                    SELECT major, minor, patch, build
                    FROM Version
                    WHERE software_id = {software_id}
                      AND major = {major}
                    ORDER BY major DESC, minor DESC, patch DESC
                    LIMIT 1
                    """
                )
                version_cursor = await db.execute(version_query, version_values)

            version_row = await version_cursor.fetchone()
            if not version_row:
                return None

            # Format version string
            parts = [str(version_row["major"])]
            if version_row["minor"] is not None:
                parts.append(str(version_row["minor"]))
            if version_row["patch"] is not None:
                parts.append(str(version_row["patch"]))
            version = ".".join(parts)
            if version_row["build"]:
                version += f"+{version_row['build']}"

            return version

    async def get_all_software(self) -> list[Software]:
        """
        Get all software with their latest versions and links.
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            sql_query, values = sql(
                t"""
                SELECT id, name, slug, latest_version_id
                FROM Software
                ORDER BY name
                """
            )
            cursor = await db.execute(sql_query, values)
            rows = await cursor.fetchall()

            if not rows:
                return []

            softwares = []
            for row in rows:
                software_dict = dict(row)

                # Fetch latest version
                if software_dict["latest_version_id"]:
                    version_id = software_dict["latest_version_id"]
                    version_query, version_values = sql(
                        t"""
                        SELECT id, major, minor, patch, build, software_id, pushed_at
                        FROM Version
                        WHERE id = {version_id}
                        """
                    )
                    version_cursor = await db.execute(version_query, version_values)
                    version_row = await version_cursor.fetchone()
                    if version_row:
                        software_dict["latest_version"] = Version(**dict(version_row))

                # Fetch links
                software_id = software_dict["id"]
                links_query, links_values = sql(
                    t"""
                    SELECT id, name, url, software_id
                    FROM Link
                    WHERE software_id = {software_id}
                    """
                )
                links_cursor = await db.execute(links_query, links_values)
                links_rows = await links_cursor.fetchall()
                software_dict["links"] = [Link(**dict(row)) for row in links_rows]

                softwares.append(Software(**software_dict))

            return softwares

    async def get_major_versions(self, software_id: int) -> list[int]:
        """
        Get all distinct major versions for a software.
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            sql_query, values = sql(
                t"""
                SELECT DISTINCT major
                FROM Version
                WHERE software_id = {software_id}
                ORDER BY major DESC
                """
            )
            cursor = await db.execute(sql_query, values)
            rows = await cursor.fetchall()

            return [row["major"] for row in rows]

    async def get_latest_releases(self, limit: int = 10) -> list[Release]:
        """
        Get the latest releases across all software.
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            sql_query, values = sql(
                t"""
                WITH RankedVersions AS (
                    SELECT
                        v.id,
                        v.major,
                        v.minor,
                        v.patch,
                        v.build,
                        v.software_id,
                        v.pushed_at,
                        ROW_NUMBER() OVER (PARTITION BY v.software_id ORDER BY v.pushed_at DESC) as rn
                    FROM Version v
                )
                SELECT
                    rv.id,
                    rv.major,
                    rv.minor,
                    rv.patch,
                    rv.build,
                    rv.software_id,
                    s.name AS software_name,
                    s.slug AS software_slug,
                    rv.pushed_at
                FROM RankedVersions rv
                JOIN Software s ON rv.software_id = s.id
                WHERE rv.rn = 1
                ORDER BY rv.pushed_at DESC
                LIMIT {limit}
                """
            )
            cursor = await db.execute(sql_query, values)
            rows = await cursor.fetchall()

            releases = []
            for row in rows:
                parts = [str(row["major"])]
                if row["minor"] is not None:
                    parts.append(str(row["minor"]))
                if row["patch"] is not None:
                    parts.append(str(row["patch"]))
                version = ".".join(parts)
                if row["build"]:
                    version += f"+{row['build']}"

                # Handle pushed_at - could be string or datetime
                pushed_at = row["pushed_at"]
                if isinstance(pushed_at, str):
                    pushed_at = datetime.fromisoformat(pushed_at)
                elif not isinstance(pushed_at, datetime):
                    pushed_at = datetime.now()

                releases.append(
                    Release(
                        version=version,
                        software_name=row["software_name"],
                        software_slug=row["software_slug"],
                        pushed_at=pushed_at,
                    )
                )

            return releases

    async def upsert_software(self, name: str, slug: str) -> int:
        """
        Create or update software, returns the software ID.
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            # Check if software exists
            sql_query, values = sql(
                t"""
                SELECT id FROM Software WHERE slug = {slug}
                """
            )
            cursor = await db.execute(sql_query, values)
            row = await cursor.fetchone()

            if row:
                return row["id"]

            # Insert new software
            sql_query, values = sql(
                t"""
                INSERT INTO Software (name, slug) VALUES ({name}, {slug})
                """
            )
            cursor = await db.execute(sql_query, values)
            await db.commit()

            return cursor.lastrowid

    async def delete_aliases(self, software_id: int) -> None:
        """Delete all aliases for a software."""
        async with aiosqlite.connect(self.db_path) as db:
            sql_query, values = sql(
                t"""
                DELETE FROM Alias WHERE software_id = {software_id}
                """
            )
            await db.execute(sql_query, values)
            await db.commit()

    async def create_alias(self, software_id: int, name: str) -> None:
        """Create an alias for a software."""
        async with aiosqlite.connect(self.db_path) as db:
            sql_query, values = sql(
                t"""
                INSERT INTO Alias (software_id, name) VALUES ({software_id}, {name})
                """
            )
            await db.execute(sql_query, values)
            await db.commit()

    async def delete_versions(self, software_id: int) -> None:
        """Delete all versions for a software."""
        async with aiosqlite.connect(self.db_path) as db:
            sql_query, values = sql(
                t"""
                DELETE FROM Version WHERE software_id = {software_id}
                """
            )
            await db.execute(sql_query, values)
            await db.commit()

    async def create_version(
        self,
        software_id: int,
        major: int,
        minor: int | None,
        patch: int | None,
        pushed_at: datetime,
        build: str | None = None,
    ) -> None:
        """Create a version for a software."""
        async with aiosqlite.connect(self.db_path) as db:
            sql_query, values = sql(
                t"""
                INSERT INTO Version (software_id, major, minor, patch, build, pushed_at)
                VALUES ({software_id}, {major}, {minor}, {patch}, {build}, {pushed_at})
                """
            )
            await db.execute(sql_query, values)
            await db.commit()

    async def update_latest_version(self, software_id: int) -> None:
        """Update the latest_version_id for a software."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            # Find the latest version
            sql_query, values = sql(
                t"""
                SELECT id FROM Version
                WHERE software_id = {software_id}
                ORDER BY major DESC, minor DESC, patch DESC
                LIMIT 1
                """
            )
            cursor = await db.execute(sql_query, values)
            row = await cursor.fetchone()

            if row:
                version_id = row["id"]
                sql_query, values = sql(
                    t"""
                    UPDATE Software
                    SET latest_version_id = {version_id}
                    WHERE id = {software_id}
                    """
                )
                await db.execute(sql_query, values)
                await db.commit()

    async def delete_links(self, software_id: int) -> None:
        """Delete all links for a software."""
        async with aiosqlite.connect(self.db_path) as db:
            sql_query, values = sql(
                t"""
                DELETE FROM Link WHERE software_id = {software_id}
                """
            )
            await db.execute(sql_query, values)
            await db.commit()

    async def create_link(self, software_id: int, name: str, url: str) -> None:
        """Create a link for a software."""
        async with aiosqlite.connect(self.db_path) as db:
            sql_query, values = sql(
                t"""
                INSERT INTO Link (software_id, name, url) VALUES ({software_id}, {name}, {url})
                """
            )
            await db.execute(sql_query, values)
            await db.commit()
