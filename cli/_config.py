import os
from pathlib import Path

from dotenv import load_dotenv

HERE = Path(__file__).parent

load_dotenv(HERE.parent / ".env")

# TODO: use pydantic for this

github_token = os.getenv("GITHUB_TOKEN")

notion_token = os.getenv("NOTION_TOKEN")
notion_db = os.getenv("NOTION_DB")
