import json
from pathlib import Path

from mainshow.config import load_project_config
from mainshow.discovery import cluster_prefix, discover_unknown_shows


def test_cluster_prefix_normalizes_episode_variants() -> None:
    assert cluster_prefix("2 NGÀY 1 ĐÊM - TẬP 36: thử thách") == "2 ngay 1 dem"
    assert cluster_prefix("XYZ Season 2 | EP.04") == "xyz"


def test_unknown_cluster_requires_four_contiguous_official_long_episodes(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    items = [
        {
            "id": f"video00000{episode}",
            "title": f"Chương Trình Mới - Tập {episode}: thử thách",
            "channelId": "UCkna2OcuN1E6u5I8GVtdkOw",
            "channelName": "Vie Channel",
            "duration": "1:00:00",
        }
        for episode in range(1, 5)
    ]
    (raw_dir / "fixture.json").write_text(
        json.dumps(
            {
                "actor_name": "fixture/actor",
                "actor_run_id": "run",
                "dataset_id": "dataset",
                "retrieved_at": "2026-08-12T12:00:00+07:00",
                "items": items,
            }
        ),
        encoding="utf-8",
    )
    result = discover_unknown_shows(raw_dir, tmp_path / "output", load_project_config(root))
    assert result["accepted"] == 1
