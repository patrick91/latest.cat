from asyncio import run

from config import database


async def setup_db():
    await database.connect()
    await database.execute(
        query="""
          CREATE TABLE "Software" (
            "id" UUID NOT NULL PRIMARY KEY,
            "name" TEXT NOT NULL,
            "slug" TEXT NOT NULL,
            "aliases" JSON,
            "links" JSON
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


run(setup_db())
