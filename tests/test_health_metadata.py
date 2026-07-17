import json
import sqlite3

import pytest

from services import health


async def test_application_check_reports_runtime_metadata():
    result = await health.check_application_boot()

    assert result["status"] == "ok"
    assert result["meta"]["framework"] == "FastAPI"
    assert result["meta"]["fastapiVersion"]
    assert result["meta"]["pythonVersion"]
    assert result["meta"]["processUptimeSeconds"] >= 0
    assert result["meta"]["eventLoop"]


async def test_database_check_reports_schema_counts_and_integrity(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
):
    database_path = tmp_path / "db.sqlite"
    with sqlite3.connect(database_path) as database:
        database.execute("CREATE TABLE Software (slug TEXT, latest_version_id INTEGER)")
        database.execute("CREATE TABLE Version (id INTEGER)")
        database.execute("CREATE TABLE Alias (id INTEGER)")
        database.execute("CREATE TABLE Link (id INTEGER)")
        database.execute("INSERT INTO Version VALUES (1)")
        database.execute("INSERT INTO Software VALUES ('python', 1)")
        database.execute("INSERT INTO Alias VALUES (1)")
        database.execute("INSERT INTO Link VALUES (1)")
    monkeypatch.setattr(health, "DATABASE_PATH", database_path)

    result = await health.check_database_connection()

    assert result["status"] == "ok"
    assert result["meta"]["integrityCheck"] == "ok"
    assert result["meta"]["softwareCount"] == 1
    assert result["meta"]["softwareWithLatestVersionCount"] == 1
    assert result["meta"]["versionCount"] == 1
    assert result["meta"]["aliasCount"] == 1
    assert result["meta"]["linkCount"] == 1
    assert result["meta"]["databaseSizeBytes"] > 0


async def test_frontend_check_reports_asset_details_and_missing_files(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
):
    manifest_path = tmp_path / "static/build/.vite/manifest.json"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text(
        json.dumps(
            {
                "frontend/app.tsx": {
                    "file": "assets/app.js",
                    "css": ["assets/app.css"],
                }
            }
        ),
        encoding="utf-8",
    )
    assets_path = manifest_path.parent.parent / "assets"
    assets_path.mkdir()
    (assets_path / "app.js").write_text("console.log('ok')", encoding="utf-8")
    monkeypatch.setattr(health, "FRONTEND_MANIFEST_PATH", manifest_path)

    result = await health.check_frontend_assets()

    assert result["status"] == "failed"
    assert result["meta"]["entrypointPresent"] is True
    assert result["meta"]["referencedAssetCount"] == 2
    assert result["meta"]["missingAssetCount"] == 1
    assert result["meta"]["javascriptAssetCount"] == 1
    assert result["meta"]["stylesheetAssetCount"] == 1
    assert result["meta"]["totalAssetBytes"] > 0
