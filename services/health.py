import asyncio
import json
import logging
import os
import platform
import shutil
import time
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from importlib.metadata import version as package_version
from pathlib import Path, PurePosixPath
from typing import Any

import aiosqlite

logger = logging.getLogger(__name__)

DATABASE_PATH = Path("db.sqlite")
FRONTEND_MANIFEST_PATH = Path("static/build/.vite/manifest.json")
FRONTEND_ENTRYPOINT = "frontend/app.tsx"
DISK_WARNING_PERCENTAGE = 85
DISK_FAILURE_PERCENTAGE = 95
PROCESS_STARTED_AT = time.monotonic()
FASTAPI_VERSION = package_version("fastapi")

CheckResult = dict[str, Any]
Check = Callable[[], Awaitable[CheckResult]]


@dataclass(frozen=True)
class CheckDefinition:
    name: str
    label: str
    run: Check


@dataclass(frozen=True)
class FrontendAssetStats:
    manifest_entries: int
    referenced_assets: int
    missing_assets: int
    total_asset_bytes: int
    javascript_assets: int
    stylesheet_assets: int
    entrypoint_present: bool


def _database_uri() -> str:
    # Read-only mode prevents a missing database from being silently created.
    return f"{DATABASE_PATH.resolve().as_uri()}?mode=ro"


async def _fetch_database_scalar(database: aiosqlite.Connection, query: str) -> Any:
    async with database.execute(query) as cursor:
        row = await cursor.fetchone()
    if row is None:
        raise RuntimeError("Database query returned no result")
    return row[0]


async def check_application_boot() -> CheckResult:
    return {
        "name": "ApplicationBoot",
        "label": "Application",
        "status": "ok",
        "shortSummary": "FastAPI is serving requests",
        "notificationMessage": "The FastAPI application did not boot",
        "meta": {
            "framework": "FastAPI",
            "fastapiVersion": FASTAPI_VERSION,
            "pythonVersion": platform.python_version(),
            "pythonImplementation": platform.python_implementation(),
            "processUptimeSeconds": round(time.monotonic() - PROCESS_STARTED_AT),
            "processId": os.getpid(),
            "operatingSystem": platform.system(),
            "machineArchitecture": platform.machine(),
            "cpuCount": os.cpu_count(),
            "eventLoop": type(asyncio.get_running_loop()).__name__,
        },
    }


async def check_database_connection() -> CheckResult:
    started_at = time.perf_counter()
    async with aiosqlite.connect(_database_uri(), uri=True) as database:
        software_count = int(
            await _fetch_database_scalar(database, "SELECT COUNT(*) FROM Software")
        )
        software_with_latest_version_count = int(
            await _fetch_database_scalar(
                database,
                """
                SELECT COUNT(*)
                FROM Software AS software
                JOIN Version AS version ON version.id = software.latest_version_id
                """,
            )
        )
        version_count = int(
            await _fetch_database_scalar(database, "SELECT COUNT(*) FROM Version")
        )
        alias_count = int(
            await _fetch_database_scalar(database, "SELECT COUNT(*) FROM Alias")
        )
        link_count = int(
            await _fetch_database_scalar(database, "SELECT COUNT(*) FROM Link")
        )
        integrity_result = str(
            await _fetch_database_scalar(database, "PRAGMA quick_check(1)")
        )
        page_count = int(await _fetch_database_scalar(database, "PRAGMA page_count"))
        page_size = int(await _fetch_database_scalar(database, "PRAGMA page_size"))

    check_duration_ms = round((time.perf_counter() - started_at) * 1000)
    status = "ok" if integrity_result == "ok" else "failed"
    return {
        "name": "DatabaseConnection",
        "label": "Database",
        "status": status,
        "shortSummary": f"{check_duration_ms}ms · {software_count} software",
        "notificationMessage": (
            "SQLite is reachable and passed its integrity check"
            if status == "ok"
            else "SQLite failed its integrity check"
        ),
        "meta": {
            "checkDurationMs": check_duration_ms,
            "integrityCheck": integrity_result,
            "databaseSizeBytes": page_count * page_size,
            "pageCount": page_count,
            "pageSizeBytes": page_size,
            "softwareCount": software_count,
            "softwareWithLatestVersionCount": software_with_latest_version_count,
            "versionCount": version_count,
            "aliasCount": alias_count,
            "linkCount": link_count,
        },
    }


def _inspect_frontend_manifest(manifest_path: Path) -> FrontendAssetStats:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or not manifest:
        raise ValueError("Frontend asset manifest is empty")

    asset_paths: set[PurePosixPath] = set()
    for entry in manifest.values():
        if not isinstance(entry, dict) or not isinstance(entry.get("file"), str):
            raise ValueError("Frontend asset manifest contains an invalid entry")

        referenced_paths = [entry["file"]]
        for field_name in ("css", "assets"):
            field_value = entry.get(field_name, [])
            if not isinstance(field_value, list) or not all(
                isinstance(value, str) for value in field_value
            ):
                raise ValueError(
                    f"Frontend asset manifest contains an invalid {field_name} field"
                )
            referenced_paths.extend(field_value)

        for referenced_path in referenced_paths:
            asset_path = PurePosixPath(referenced_path)
            if asset_path.is_absolute() or ".." in asset_path.parts:
                raise ValueError("Frontend asset manifest contains an unsafe path")
            asset_paths.add(asset_path)

    build_path = manifest_path.parent.parent
    existing_paths = [
        build_path.joinpath(*asset_path.parts)
        for asset_path in asset_paths
        if build_path.joinpath(*asset_path.parts).is_file()
    ]
    return FrontendAssetStats(
        manifest_entries=len(manifest),
        referenced_assets=len(asset_paths),
        missing_assets=len(asset_paths) - len(existing_paths),
        total_asset_bytes=sum(path.stat().st_size for path in existing_paths),
        javascript_assets=sum(
            asset_path.suffix in {".js", ".mjs"} for asset_path in asset_paths
        ),
        stylesheet_assets=sum(
            asset_path.suffix == ".css" for asset_path in asset_paths
        ),
        entrypoint_present=FRONTEND_ENTRYPOINT in manifest,
    )


async def check_frontend_assets() -> CheckResult:
    started_at = time.perf_counter()
    try:
        stats = await asyncio.to_thread(
            _inspect_frontend_manifest, FRONTEND_MANIFEST_PATH
        )
    except FileNotFoundError:
        return {
            "name": "FrontendAssets",
            "label": "Frontend assets",
            "status": "failed",
            "shortSummary": "Manifest missing",
            "notificationMessage": "The frontend asset manifest is missing",
            "meta": {"manifestPresent": False},
        }
    except OSError, ValueError:
        return {
            "name": "FrontendAssets",
            "label": "Frontend assets",
            "status": "failed",
            "shortSummary": "Manifest invalid",
            "notificationMessage": "The frontend asset manifest is invalid",
            "meta": {"manifestPresent": True, "manifestValid": False},
        }

    status = (
        "ok" if stats.entrypoint_present and stats.missing_assets == 0 else "failed"
    )
    return {
        "name": "FrontendAssets",
        "label": "Frontend assets",
        "status": status,
        "shortSummary": (
            f"{stats.referenced_assets} assets available"
            if status == "ok"
            else f"{stats.missing_assets} assets missing"
        ),
        "notificationMessage": (
            "Every frontend asset referenced by the manifest exists"
            if status == "ok"
            else "The frontend entrypoint or one of its assets is missing"
        ),
        "meta": {
            "checkDurationMs": round((time.perf_counter() - started_at) * 1000),
            "manifestPresent": True,
            "manifestValid": True,
            "entrypointPresent": stats.entrypoint_present,
            "manifestEntries": stats.manifest_entries,
            "referencedAssetCount": stats.referenced_assets,
            "missingAssetCount": stats.missing_assets,
            "javascriptAssetCount": stats.javascript_assets,
            "stylesheetAssetCount": stats.stylesheet_assets,
            "otherAssetCount": (
                stats.referenced_assets
                - stats.javascript_assets
                - stats.stylesheet_assets
            ),
            "totalAssetBytes": stats.total_asset_bytes,
        },
    }


async def check_used_disk_space() -> CheckResult:
    started_at = time.perf_counter()
    usage = await asyncio.to_thread(shutil.disk_usage, DATABASE_PATH.resolve().parent)
    used_percentage = (usage.used / usage.total) * 100

    if used_percentage >= DISK_FAILURE_PERCENTAGE:
        status = "failed"
    elif used_percentage >= DISK_WARNING_PERCENTAGE:
        status = "warning"
    else:
        status = "ok"

    gibibyte = 1024**3
    return {
        "name": "UsedDiskSpace",
        "label": "Disk space",
        "status": status,
        "shortSummary": f"{used_percentage:.1f}% used",
        "notificationMessage": (
            f"Disk usage is {used_percentage:.1f}% "
            f"({usage.free // (1024 * 1024)} MiB free)"
        ),
        "meta": {
            "checkDurationMs": round((time.perf_counter() - started_at) * 1000),
            "usedSpacePercentage": round(used_percentage, 1),
            "totalBytes": usage.total,
            "usedBytes": usage.used,
            "freeBytes": usage.free,
            "totalGiB": round(usage.total / gibibyte, 2),
            "usedGiB": round(usage.used / gibibyte, 2),
            "freeGiB": round(usage.free / gibibyte, 2),
            "warningThresholdPercentage": DISK_WARNING_PERCENTAGE,
            "failureThresholdPercentage": DISK_FAILURE_PERCENTAGE,
        },
    }


HEALTH_CHECKS = (
    CheckDefinition("ApplicationBoot", "Application", check_application_boot),
    CheckDefinition("DatabaseConnection", "Database", check_database_connection),
    CheckDefinition("FrontendAssets", "Frontend assets", check_frontend_assets),
    CheckDefinition("UsedDiskSpace", "Disk space", check_used_disk_space),
)


async def run_health_checks(
    checks: Sequence[CheckDefinition] = HEALTH_CHECKS,
) -> list[CheckResult]:
    results = []

    for check in checks:
        try:
            results.append(await check.run())
        except Exception as exception:
            logger.exception("Application health check %s crashed", check.name)
            results.append(
                {
                    "name": check.name,
                    "label": check.label,
                    "status": "crashed",
                    "shortSummary": "Check crashed",
                    "notificationMessage": f"The {check.label} health check crashed",
                    "meta": {"exceptionType": type(exception).__name__},
                }
            )

    return results
