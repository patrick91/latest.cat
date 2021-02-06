run:
	poetry run uvicorn --reload main:app

fetch:
	poetry run python fetch_versions.py