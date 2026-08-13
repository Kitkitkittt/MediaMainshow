from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import httpx

LOGGER = logging.getLogger(__name__)
API_BASE = "https://api.apify.com/v2"
VIETNAM_TIME = timezone(timedelta(hours=7), name="Asia/Ho_Chi_Minh")


@dataclass(frozen=True)
class RawRun:
    actor_name: str
    run_id: str
    dataset_id: str
    build_id: str | None
    retrieved_at: str
    actor_input: dict[str, Any]
    items: list[dict[str, Any]]
    run_metadata: dict[str, Any]


def load_apify_token() -> str:
    # `apify_api` is the existing user-provided legacy variable name.
    token = os.getenv("APIFY_TOKEN") or os.getenv("apify_api")  # noqa: SIM112
    if not token:
        raise RuntimeError("Set APIFY_TOKEN or apify_api before starting a paid actor run")
    return token


class ApifyYouTubeClient:
    def __init__(self, token: str, *, timeout_seconds: float = 30.0) -> None:
        self._client = httpx.Client(
            base_url=API_BASE,
            headers={"Authorization": f"Bearer {token}"},
            timeout=timeout_seconds,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> ApifyYouTubeClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def run(
        self,
        actor_name: str,
        actor_input: dict[str, Any],
        *,
        wait_timeout_seconds: int = 600,
        poll_seconds: float = 3.0,
        max_total_charge_usd: float = 1.0,
    ) -> RawRun:
        actor_id = actor_name.replace("/", "~")
        response = self._client.post(
            f"/acts/{actor_id}/runs",
            params={"maxTotalChargeUsd": max_total_charge_usd},
            json=actor_input,
        )
        response.raise_for_status()
        run = response.json()["data"]
        run_id = run["id"]
        LOGGER.info("Started Apify actor=%s run_id=%s", actor_name, run_id)
        deadline = time.monotonic() + wait_timeout_seconds
        while run["status"] not in {"SUCCEEDED", "FAILED", "TIMED-OUT", "ABORTED"}:
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Apify run {run_id} exceeded local wait timeout")
            time.sleep(poll_seconds)
            status_response = self._client.get(f"/actor-runs/{run_id}")
            status_response.raise_for_status()
            run = status_response.json()["data"]
        if run["status"] != "SUCCEEDED":
            raise RuntimeError(f"Apify run {run_id} ended with status={run['status']}")
        return self._collect(actor_name, actor_input, run)

    def fetch(self, actor_name: str, run_id: str, *, allow_partial: bool = False) -> RawRun:
        """Resume a completed run, or retain an explicitly allowed partial result."""
        status_response = self._client.get(f"/actor-runs/{run_id}")
        status_response.raise_for_status()
        run = status_response.json()["data"]
        if run["status"] != "SUCCEEDED" and not (allow_partial and run["status"] == "ABORTED"):
            raise RuntimeError(f"Apify run {run_id} has status={run['status']}, not SUCCEEDED")
        return self._collect(actor_name, {}, run)

    def _collect(self, actor_name: str, actor_input: dict[str, Any], run: dict[str, Any]) -> RawRun:
        run_id = run["id"]
        dataset_id = run["defaultDatasetId"]
        dataset_response = self._client.get(
            f"/datasets/{dataset_id}/items", params={"clean": "true", "format": "json"}
        )
        dataset_response.raise_for_status()
        items = dataset_response.json()
        retrieved_at = datetime.now(VIETNAM_TIME).isoformat()
        LOGGER.info(
            "Fetched Apify run_id=%s dataset_id=%s items=%d", run_id, dataset_id, len(items)
        )
        return RawRun(
            actor_name,
            run_id,
            dataset_id,
            run.get("buildId") or run.get("buildNumber"),
            retrieved_at,
            actor_input,
            items,
            {
                key: run.get(key)
                for key in (
                    "status",
                    "startedAt",
                    "finishedAt",
                    "usageTotalUsd",
                    "chargedEventCounts",
                )
                if run.get(key) is not None
            },
        )


def save_raw_run(run: RawRun, directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = run.retrieved_at.replace(":", "-")
    path = directory / f"{timestamp}_{run.run_id}.json"
    payload = {
        "actor_name": run.actor_name,
        "actor_run_id": run.run_id,
        "dataset_id": run.dataset_id,
        "actor_build_id": run.build_id,
        "retrieved_at": run.retrieved_at,
        "actor_input": run.actor_input,
        "run_metadata": run.run_metadata,
        "items": run.items,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
