from databases import Database

from pathlib import Path

database_path = Path(".").parent / "db.sqlite"

database = Database(f"sqlite:///{database_path}")
