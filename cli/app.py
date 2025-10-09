import asyncio
import pathlib
from typing import Awaitable, Callable, ParamSpec, TypeVar

import typer
import yaml  # type: ignore
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from services.software import SoftwareService
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
    ) -> list[_fetchers.Tag] | None:
        padded_name = software.name.ljust(longest_name)

        task = progress.add_task(
            f"Fetching versions for [bold]{padded_name}[/]", total=None
        )

        try:
            versions = await _fetchers.fetch_versions(software)
            progress.remove_task(task)
            return versions
        except Exception as e:
            progress.remove_task(task)
            progress.console.print(f"[red]✗ Error fetching {padded_name}: {e}[/]")
            return None

    async def _save_versions(
        service: SoftwareService,
        software_id: int,
        versions: list[_fetchers.Tag],
    ):
        for version in versions:
            assert version.major is not None
            assert version.minor is not None

            await service.create_version(
                software_id=software_id,
                major=version.major,
                minor=version.minor,
                patch=version.patch,
                pushed_at=version.pushed_date,
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

        service = SoftwareService()

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
            # Skip if fetching failed
            if versions is None:
                continue

            # Upsert software
            software_id = await service.upsert_software(
                name=software["name"],
                slug=software["slug"],
            )

            # Update aliases
            await service.delete_aliases(software_id)
            for alias in software["aliases"]:
                await service.create_alias(software_id, alias)

            # Update versions
            await service.delete_versions(software_id)
            await _save_versions(service, software_id, versions)

            # Update latest version
            await service.update_latest_version(software_id)

            # Update links
            await service.delete_links(software_id)
            for link in software["links"]:
                await service.create_link(software_id, link["name"], link["url"])

    asyncio.run(_fetch())
