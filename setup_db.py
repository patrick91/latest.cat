import json
import uuid
from asyncio import run

from data.config import database


async def setup_db():
    await database.connect()
    await database.execute(
        query="""
          CREATE TABLE "Software" (
            "id" UUID NOT NULL PRIMARY KEY,
            "name" TEXT NOT NULL,
            "slug" TEXT NOT NULL,
            "aliases" JSON
          );
        """
    )
    await database.execute(
        query="""
          CREATE TABLE "Version" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "software" UUID NOT NULL REFERENCES "Software" ("id") ON DELETE CASCADE,
            "major" INTEGER NOT NULL,
            "minor" INTEGER,
            "revision" INTEGER,
            "build" TEXT
          );
        """
    )
    await database.execute(
        query='CREATE INDEX "idx_version__software" ON "Version" ("software")'
    )

    python_uuid = uuid.uuid4()

    query = """
        INSERT INTO Software(id, name, slug, aliases)
        VALUES (:id, :name, :slug, :aliases)
    """
    values = {
        "name": "Python",
        "slug": "python",
        "aliases": json.dumps(["py", "🐍"]),
        "id": str(python_uuid),
    }

    await database.execute(query=query, values=values)

    query = (
        "INSERT INTO Version(software, major, minor, revision)"
        + "VALUES (:software, :major, :minor, :revision)"
    )
    values = {"major": 3, "minor": 9, "revision": 1, "software": str(python_uuid)}

    await database.execute(query=query, values=values)


run(setup_db())
