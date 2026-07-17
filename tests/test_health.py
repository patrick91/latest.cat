import time
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

import main
from services.health import HEALTH_CHECKS, CheckDefinition, run_health_checks

HEALTH_CHECK_SECRET = "test-health-check-secret"
HEALTH_CHECK_URL = "/oh-dear-health-check-results"


@pytest.fixture
async def client():
    transport = ASGITransport(app=main.app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"oh-dear-health-check-secret": "wrong-secret"},
    ],
)
async def test_health_endpoint_rejects_unauthorized_requests_without_running_checks(
    client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
    headers: dict[str, str],
):
    check_runner = AsyncMock(
        return_value=[{"name": "SensitiveCheckResult", "status": "ok"}]
    )
    monkeypatch.setenv("OH_DEAR_HEALTH_CHECK_SECRET", HEALTH_CHECK_SECRET)
    monkeypatch.setattr(main, "run_health_checks", check_runner)

    response = await client.get(HEALTH_CHECK_URL, headers=headers)

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}
    assert "checkResults" not in response.text
    check_runner.assert_not_awaited()


async def test_health_endpoint_returns_fresh_results_for_the_correct_secret(
    client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
):
    check_results = [
        {
            "name": "ApplicationBoot",
            "label": "Application",
            "status": "ok",
            "shortSummary": "FastAPI is serving requests",
            "notificationMessage": "The FastAPI application did not boot",
            "meta": {"framework": "FastAPI"},
        }
    ]
    check_runner = AsyncMock(return_value=check_results)
    monkeypatch.setenv("OH_DEAR_HEALTH_CHECK_SECRET", HEALTH_CHECK_SECRET)
    monkeypatch.setattr(main, "run_health_checks", check_runner)
    timestamps = iter([1_716_383_400, 1_716_383_401])
    monkeypatch.setattr(main, "time", lambda: next(timestamps))

    first_response = await client.get(
        HEALTH_CHECK_URL,
        headers={"oh-dear-health-check-secret": HEALTH_CHECK_SECRET},
    )
    second_response = await client.get(
        HEALTH_CHECK_URL,
        headers={"oh-dear-health-check-secret": HEALTH_CHECK_SECRET},
    )

    assert first_response.status_code == 200
    assert first_response.json() == {
        "finishedAt": 1_716_383_400,
        "checkResults": check_results,
    }
    assert second_response.status_code == 200
    assert second_response.json() == {
        "finishedAt": 1_716_383_401,
        "checkResults": check_results,
    }
    assert check_runner.await_count == 2


async def test_health_endpoint_runs_the_real_application_checks(
    client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv("OH_DEAR_HEALTH_CHECK_SECRET", HEALTH_CHECK_SECRET)

    before_request = int(time.time())
    response = await client.get(
        HEALTH_CHECK_URL,
        headers={"oh-dear-health-check-secret": HEALTH_CHECK_SECRET},
    )
    after_request = int(time.time())

    assert response.status_code == 200
    assert before_request <= response.json()["finishedAt"] <= after_request

    check_results = response.json()["checkResults"]
    assert [result["name"] for result in check_results] == [
        check.name for check in HEALTH_CHECKS
    ]
    assert all(
        result["status"] in {"ok", "warning", "failed", "crashed", "skipped"}
        for result in check_results
    )
    assert all(len(result["meta"]) <= 20 for result in check_results)
    assert all(
        isinstance(value, str | int | float | bool) or value is None
        for result in check_results
        for value in result["meta"].values()
    )
    assert (
        next(
            result for result in check_results if result["name"] == "DatabaseConnection"
        )["status"]
        == "ok"
    )


async def test_one_crashed_check_does_not_prevent_other_results():
    async def healthy_check():
        return {"name": "HealthyCheck", "status": "ok"}

    async def crashing_check():
        raise RuntimeError("boom")

    results = await run_health_checks(
        [
            CheckDefinition("CrashingCheck", "Crashing check", crashing_check),
            CheckDefinition("HealthyCheck", "Healthy check", healthy_check),
        ]
    )

    assert results == [
        {
            "name": "CrashingCheck",
            "label": "Crashing check",
            "status": "crashed",
            "shortSummary": "Check crashed",
            "notificationMessage": "The Crashing check health check crashed",
            "meta": {"exceptionType": "RuntimeError"},
        },
        {"name": "HealthyCheck", "status": "ok"},
    ]
