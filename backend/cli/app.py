import asyncio
import pathlib
from typing import Awaitable, Callable, ParamSpec, TypeVar

import prisma
import typer
import yaml  # type: ignore
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from . import _fetchers
from ._software import Software

app = typer.Typer(pretty_exceptions_enable=False)


@app.command()
def hello():
    typer.echo("Hello World")


@app.command()
def fetch_versions():
    semaphore = asyncio.Semaphore(4)
    softwares = yaml.safe_load(pathlib.Path("software.yml").read_text())
    longest_name = max(len(s["name"]) for s in softwares)

    async def _fetch_versions(
        software: Software, progress: Progress
    ) -> list[tuple[int | None, ...]]:
        padded_name = software.name.ljust(longest_name)

        task = progress.add_task(
            f"Fetching versions for [bold]{padded_name}[/]", total=None
        )

        versions = await _fetchers.fetch_versions(software)

        progress.remove_task(task)

        return versions

    def _save_versions(
        db: prisma.Batch,
        software: prisma.models.Software,
        versions: list[tuple[int | None, ...]],
    ):
        for version_bits in versions:
            major, minor, patch = version_bits

            assert major is not None
            assert minor is not None

            db.version.create(
                {
                    "software_id": software.id,
                    "major": major,
                    "minor": minor,
                    "patch": patch,
                }
            )

    async def _fetch():
        P = ParamSpec("P")
        R = TypeVar("R")

        def _wrap(f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
            async def inner(*args: P.args, **kwargs: P.kwargs) -> R:
                async with semaphore:
                    return await f(*args, **kwargs)

            return inner

        _fetch = _wrap(_fetch_versions)

        async with prisma.Prisma() as db:
            with Progress(
                SpinnerColumn("clock"),
                TextColumn("{task.description}  "),
                BarColumn(),
                TextColumn("  "),
                TimeElapsedColumn(),
            ) as progress:
                tasks = [
                    _fetch(Software(**software), progress) for software in softwares
                ]

                results = await asyncio.gather(*tasks)

            for software, versions in zip(softwares, results):
                db_software = await db.software.upsert(
                    where={"slug": software["slug"]},
                    data={
                        "create": {
                            "name": software["name"],
                            "slug": software["slug"],
                        },
                        "update": {},
                    },
                )

                await db.alias.delete_many(where={"software_id": db_software.id})

                for alias in software["aliases"]:
                    await db.alias.create(
                        data={"software_id": db_software.id, "name": alias}
                    )

                await db.version.delete_many(
                    {
                        "software_id": db_software.id,
                    }
                )

                async with db.batch_() as batcher:
                    _save_versions(batcher, db_software, versions)

                latest_version = await db.version.find_first(
                    where={"software_id": db_software.id},
                    order=[{"major": "desc"}, {"minor": "desc"}, {"patch": "desc"}],
                )

                assert latest_version

                await db.software.update(
                    where={"id": db_software.id},
                    data={"latest_version": {"connect": {"id": latest_version.id}}},
                )

                await db.link.delete_many(
                    {
                        "software_id": db_software.id,
                    }
                )
                async with db.batch_() as batcher:
                    for link in software["links"]:
                        batcher.link.create(
                            {
                                "software_id": db_software.id,
                                "name": link["name"],
                                "url": link["url"],
                            }
                        )

    asyncio.run(_fetch())
