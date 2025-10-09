from dataclasses import dataclass
from datetime import datetime
from typing import AsyncGenerator

import httpx
from dateutil.parser import parse

from ._config import github_token
from ._software import Software

FETCH_TAGS_QUERY = """
query FetchTags($owner: String!, $name: String!, $before: String) {
  repository(owner: $owner, name: $name) {
    refs(refPrefix: "refs/tags/", last: 100, before: $before) {
      pageInfo {
        hasPreviousPage
        startCursor
      }
      nodes {
        name
        id
        target {
          __typename
          ... on Commit {
            pushedDate
            committedDate
          }
          ... on Tag {
            target {
              __typename
              ... on Tag {
                target {
                  __typename
                  ... on Commit {
                    pushedDate
                    committedDate
                  }
                }
              }
              ... on Commit {
                pushedDate
                committedDate
              }
            }
          }
        }
      }
    }
  }
}
"""


@dataclass
class Tag:
    major: int
    minor: int
    patch: int | None
    pushed_date: datetime


async def fetch_tags_from_github(
    repository: str,
) -> AsyncGenerator[tuple[str, datetime], None]:
    owner, name = repository.split("/")

    if not github_token:
        raise ValueError(
            "GITHUB_TOKEN environment variable is not set. "
            "Please create a .env file with your GitHub personal access token:\n"
            "GITHUB_TOKEN=your_token_here\n\n"
            "Get a token at: https://github.com/settings/tokens"
        )

    async with httpx.AsyncClient() as client:
        has_previous_page = True
        before = None

        # TODO: optimize this in future

        while has_previous_page:
            try:
                response = await client.post(
                    "https://api.github.com/graphql",
                    headers={
                        "Authorization": f"bearer {github_token}",
                        "User-Agent": "latest.cat/1",
                    },
                    json={
                        "query": FETCH_TAGS_QUERY,
                        "variables": {
                            "owner": owner,
                            "name": name,
                            "before": before,
                        },
                    },
                )

                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    raise ValueError(
                        f"GitHub API authentication failed (401 Unauthorized) for repository {repository}.\n"
                        "Your GITHUB_TOKEN may be invalid or expired.\n"
                        "Please check your .env file and ensure you have a valid GitHub personal access token.\n"
                        "Get a new token at: https://github.com/settings/tokens"
                    ) from e
                elif e.response.status_code == 404:
                    raise ValueError(
                        f"Repository not found: {repository}\n"
                        "Please check the repository name in software.yml"
                    ) from e
                else:
                    raise ValueError(
                        f"GitHub API error for {repository}: {e.response.status_code} {e.response.reason_phrase}"
                    ) from e
            content = response.json()

            if errors := content.get("errors"):
                raise ValueError(errors)

            data = content["data"]
            tags = data["repository"]["refs"]["nodes"]
            has_previous_page = data["repository"]["refs"]["pageInfo"][
                "hasPreviousPage"
            ]
            before = data["repository"]["refs"]["pageInfo"]["startCursor"]

            for tag in tags:
                target = tag["target"]

                while target["__typename"] == "Tag":
                    target = target["target"]

                date = target["pushedDate"] or target["committedDate"]

                yield tag["name"], parse(date)


async def fetch_versions(
    software: Software,
) -> list[Tag]:
    # we only support github for now
    assert software.repository

    tags: list[Tag] = []

    async for version, pushed_at in fetch_tags_from_github(software.repository):
        pattern = software._namings.get(software.version_naming)

        assert pattern

        if match := pattern.match(version):
            major = match.group("major")
            minor = match.group("minor")
            patch = match.group("patch")

            tags.append(
                Tag(
                    major=int(major),
                    minor=int(minor),
                    patch=int(patch) if patch is not None else None,
                    pushed_date=pushed_at,
                )
            )

    return tags
