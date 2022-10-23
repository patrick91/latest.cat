from typing import AsyncGenerator

import httpx

from ._config import github_token
from ._software import Software

FETCH_TAGS_QUERY = """
query FetchTags($owner: String!, $name: String!) {
    repository(owner: $owner, name: $name) {
        refs(refPrefix: "refs/tags/", last: 100) {
            nodes {
                name
            }
        }
    }
}
"""


async def fetch_tags_from_github(repository: str) -> AsyncGenerator[str, None]:
    owner, name = repository.split("/")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.github.com/graphql",
            headers={"Authorization": f"bearer {github_token}"},
            json={
                "query": FETCH_TAGS_QUERY,
                "variables": {
                    "owner": owner,
                    "name": name,
                },
            },
        )

        response.raise_for_status()

    tags = response.json()["data"]["repository"]["refs"]["nodes"]

    for tag in tags:
        yield tag["name"]


async def fetch_versions(
    software: Software,
) -> list[tuple[int | None, ...]]:
    # we only support github for now
    assert software.repository

    tags: list[tuple[int | None, ...]] = []

    async for tag in fetch_tags_from_github(software.repository):
        pattern = software._namings.get(software.version_naming)

        assert pattern

        if match := pattern.match(tag):
            major = match.group("major")
            minor = match.group("minor")
            patch = match.group("patch")

            tags.append((int(major), int(minor), int(patch) if patch else None))

    return tags
