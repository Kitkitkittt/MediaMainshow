import csv
import json
from pathlib import Path

from mainshow.config import load_project_config
from mainshow.pipeline import build_pilot


def test_duplicate_logical_episode_suppresses_total(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    raw = tmp_path / "raw.json"
    raw.write_text(
        json.dumps(
            {
                "actor_name": "fixture/actor",
                "actor_run_id": "run1",
                "dataset_id": "ds1",
                "retrieved_at": "2026-08-12T12:00:00+07:00",
                "items": [
                    {
                        "id": "aaaaaaaaaaa",
                        "title": "Anh Trai Say Hi Tập 1",
                        "duration": "1:00:00",
                        "viewCount": 100,
                    },
                    {
                        "id": "bbbbbbbbbbb",
                        "title": "Anh Trai Say Hi Tập 1",
                        "duration": "1:01:00",
                        "viewCount": 90,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "output"
    result = build_pilot(raw, output, load_project_config(root), "ATSH")
    assert result["canonical"] == 0
    with (output / "season_summary.csv").open(encoding="utf-8-sig") as stream:
        summary = next(csv.DictReader(stream))
    assert summary["qc_status"] == "FAIL"
    assert summary["total_views"] == ""


def test_view_snapshots_are_append_only_and_idempotent(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    raw = tmp_path / "raw.json"
    payload = {
        "actor_name": "fixture/actor",
        "actor_run_id": "run1",
        "dataset_id": "ds1",
        "retrieved_at": "2026-08-12T12:00:00+07:00",
        "actor_input": {
            "startUrls": [
                {
                    "url": (
                        "https://www.youtube.com/playlist?list=PLxKLMN7WdG5AYDsDPTbq7zZTpOTGH7ay6"
                    )
                }
            ]
        },
        "items": [
            {
                "id": "aaaaaaaaaaa",
                "title": "Anh Trai Say Hi Tập 1",
                "channelId": "UCkna2OcuN1E6u5I8GVtdkOw",
                "duration": "1:00:00",
                "date": "2024-06-15T13:00:00Z",
                "viewCount": 100,
            }
        ],
    }
    raw.write_text(json.dumps(payload), encoding="utf-8")
    output = tmp_path / "output"
    config = load_project_config(root)
    build_pilot(raw, output, config, "ATSH")
    build_pilot(raw, output, config, "ATSH")
    with (output / "view_snapshot.csv").open(encoding="utf-8-sig") as stream:
        assert len(list(csv.DictReader(stream))) == 1

    payload["actor_run_id"] = "run2"
    payload["retrieved_at"] = "2026-08-19T12:00:00+07:00"
    payload["items"][0]["viewCount"] = 120
    raw.write_text(json.dumps(payload), encoding="utf-8")
    build_pilot(raw, output, config, "ATSH")
    with (output / "view_snapshot.csv").open(encoding="utf-8-sig") as stream:
        snapshots = list(csv.DictReader(stream))
    assert [row["view_count"] for row in snapshots] == ["100", "120"]
