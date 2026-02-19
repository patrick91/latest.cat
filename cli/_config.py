import os
from pathlib import Path

from dotenv import load_dotenv

HERE = Path(__file__).parent

load_dotenv(HERE.parent / ".env")

# TODO: use pydantic for this

def _get_github_token() -> str | None:
    if token := os.getenv("GITHUB_TOKEN"):
        return token
    try:
        import subprocess

        result = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    return None


github_token = _get_github_token()

notion_token = os.getenv("NOTION_TOKEN")
notion_db = os.getenv("NOTION_DB")
