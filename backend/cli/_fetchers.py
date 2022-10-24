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

    async with httpx.AsyncClient() as client:
        has_previous_page = True
        before = None

        # TODO: optimize this in future

        while has_previous_page:
            response = await client.post(
                "https://api.github.com/graphql",
                headers={"Authorization": f"bearer {github_token}"},
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
