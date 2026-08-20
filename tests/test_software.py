import sqlite3

from services.software import SoftwareService


async def test_find_softwares_prefers_exact_slug_over_partial_name(tmp_path):
    database_path = tmp_path / "db.sqlite"
    with sqlite3.connect(database_path) as database:
        database.executescript(
            """
            CREATE TABLE Software (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                latest_version_id INTEGER
            );
            CREATE TABLE Alias (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                software_id INTEGER NOT NULL
            );
            CREATE TABLE Version (
                id INTEGER PRIMARY KEY,
                major INTEGER NOT NULL,
                minor INTEGER,
                patch INTEGER,
                build TEXT,
                software_id INTEGER NOT NULL,
                pushed_at DATETIME NOT NULL
            );
            CREATE TABLE Link (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                software_id INTEGER NOT NULL
            );

            INSERT INTO Software (id, name, slug) VALUES
                (1, 'Go', 'go'),
                (2, 'Django', 'django');
            """
        )

    results = await SoftwareService(str(database_path)).find_softwares("go")

    assert [software.slug for software in results] == ["go", "django"]
