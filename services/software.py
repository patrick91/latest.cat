import aiosqlite
from models import Software, Version, Link
from sql_tstring import sql


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
