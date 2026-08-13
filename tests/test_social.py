import csv
import json
from pathlib import Path

import pytest

from mainshow.config import load_project_config
from mainshow.social import (
    _social_profile,
    build_social_outputs,
    normalize_social_item,
)


def test_normalize_social_item_preserves_exact_metric_semantics() -> None:
    item = normalize_social_item(
        "x",
        {
            "id": "123",
            "url": "https://x.com/example/status/123",
            "metrics": {"impression_count": 42, "media_view_count": None},
        },
    )
    assert item.metrics == {"impression_count": 42}
    with pytest.raises(TypeError, match="exact integer"):
        normalize_social_item(
            "x",
            {"id": "123", "url": "https://x.com/example/status/123", "metrics": {"views": 1.2}},
        )


def test_social_profile_normalization_rejects_post_urls() -> None:
    assert _social_profile("https://www.instagram.com/viechannelhtv2/") == (
        "instagram",
        "viechannelhtv2",
        "https://www.instagram.com/viechannelhtv2",
    )
    assert _social_profile("https://www.instagram.com/reel/ABC") is None
    assert _social_profile("https://www.tiktok.com/@viechannel.show/video/1") == (
        "tiktok",
        "viechannel.show",
        "https://www.tiktok.com/@viechannel.show",
    )


def test_build_social_outputs_keeps_derivatives_outside_canonical_registry(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    raw_dir = tmp_path / "raw"
    output_dir = tmp_path / "out"
    raw_dir.mkdir()
    output_dir.mkdir()
    config = load_project_config(root)
    source_url = str(config.shows["ATSH"]["seasons"][0]["official_playlist_url"])
    (raw_dir / "receipt.json").write_text(
        json.dumps(
            {
                "actor_run_id": "run-1",
                "retrieved_at": "2026-08-13T00:00:00Z",
                "actor_input": {"sourceBindingUrl": source_url},
                "items": [
                    {
                        "id": "clip1",
                        "url": "https://www.youtube.com/watch?v=clip1",
                        "channelId": "channel",
                        "descriptionLinks": [
                            {"url": "https://www.instagram.com/viechannelhtv2/"}
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    registry = output_dir / "episode_registry.csv"
    fields = [
        "show_id",
        "season_id",
        "video_id",
        "video_url",
        "title",
        "normalized_title",
        "video_type",
        "channel_authority",
        "canonical_flag",
        "episode_no",
        "review_status",
        "snapshot_at",
        "view_count",
    ]
    with registry.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerow(
            {
                "show_id": "ATSH",
                "season_id": "ATSH_2024",
                "video_id": "clip1",
                "video_url": "https://www.youtube.com/watch?v=clip1",
                "title": "Highlight",
                "normalized_title": "highlight",
                "video_type": "highlight",
                "channel_authority": "primary_producer",
                "canonical_flag": "False",
                "review_status": "EXCLUDE",
                "snapshot_at": "2026-08-13T00:00:00Z",
                "view_count": "123",
            }
        )
        writer.writerow(
            {
                "show_id": "ATSH",
                "season_id": "ATSH_2024",
                "video_id": "ep1",
                "title": "Episode",
                "video_type": "main_episode",
                "canonical_flag": "True",
                "review_status": "INCLUDE",
            }
        )
    result = build_social_outputs(raw_dir, registry, output_dir, config)
    assert result["derivative_candidates"] == 1
    assert result["social_account_candidates"] == 1
    derivative = list(
        csv.DictReader((output_dir / "derivative_content_registry.csv").open(encoding="utf-8-sig"))
    )[0]
    assert derivative["content_role"] == "HIGHLIGHT"
    assert derivative["classification_state"] == "ACCEPTED"
    account = list(
        csv.DictReader((output_dir / "social_account_candidates.csv").open(encoding="utf-8-sig"))
    )[0]
    assert account["authority_status"] == "NEEDS_REVIEW"
    assert account["evidence_strength"] == "LOW"
    snapshot = list(
        csv.DictReader((output_dir / "social_metric_snapshot.csv").open(encoding="utf-8-sig"))
    )[0]
    assert snapshot["metric_name"] == "view_count"
    assert snapshot["metric_value_exact"] == "123"
    assert snapshot["observed_at"] == "2026-08-13T00:00:00Z"


def test_derivative_receipt_is_separate_from_canonical_population(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    config = load_project_config(root)
    config.social["derivative_sources"] = [
        {
            "source_id": "test_source",
            "show_id": "ATSH",
            "season_id": "ATSH_2024",
            "source_url": "https://www.youtube.com/@VieChannelHTV2",
            "channel_id": "UCkna2OcuN1E6u5I8GVtdkOw",
        }
    ]
    raw_dir = tmp_path / "raw"
    derivative_raw_dir = tmp_path / "derivative_raw"
    output_dir = tmp_path / "out"
    raw_dir.mkdir()
    derivative_raw_dir.mkdir()
    output_dir.mkdir()
    (output_dir / "episode_registry.csv").write_text(
        "video_id,canonical_flag\nmain,True\n", encoding="utf-8-sig"
    )
    (derivative_raw_dir / "receipt.json").write_text(
        json.dumps(
            {
                "actor_name": "actor",
                "actor_run_id": "run-derivative",
                "dataset_id": "dataset",
                "retrieved_at": "2026-08-13T00:00:00Z",
                "actor_input": {"derivativeSourceId": "test_source"},
                "items": [
                    {
                        "id": "short1",
                        "url": "https://www.youtube.com/watch?v=short1",
                        "title": "Anh Trai Say Hi #shorts",
                        "channelId": "UCkna2OcuN1E6u5I8GVtdkOw",
                        "duration": "00:30",
                        "viewCount": 42,
                        "type": "shorts",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    build_social_outputs(
        raw_dir,
        output_dir / "episode_registry.csv",
        output_dir,
        config,
        derivative_raw_dir=derivative_raw_dir,
    )
    rows = list(
        csv.DictReader((output_dir / "derivative_content_registry.csv").open(encoding="utf-8-sig"))
    )
    assert len(rows) == 1
    assert rows[0]["native_content_id"] == "short1"
    assert rows[0]["platform_format"] == "SHORT"
    assert rows[0]["classification_state"] == "ACCEPTED"
