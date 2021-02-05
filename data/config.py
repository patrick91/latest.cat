from pathlib import Path

from databases import Database

database_path = Path(".").parent / "db.sqlite"

database = Database(f"sqlite:///{database_path}")
