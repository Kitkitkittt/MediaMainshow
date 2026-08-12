import csv
from pathlib import Path

from mainshow.config import load_project_config
from mainshow.population import build_all, raw_manifest_rows


def test_cached_build_consolidates_pilot_without_paid_calls(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    config = load_project_config(root)
    result = build_all(root / "data" / "raw", tmp_path, config)
    configured_seasons = sum(len(show.get("seasons", [])) for show in config.shows.values())
    assert result["configured_seasons"] == configured_seasons
    assert result["raw_receipts"] == len(list((root / "data" / "raw").glob("*.json")))
    with (tmp_path / "season_summary.csv").open(encoding="utf-8-sig") as stream:
        summaries = list(csv.DictReader(stream))
    assert result["extracted_seasons"] == len(summaries)
    pilot = next(row for row in summaries if row["season_id"] == "ATSH_2024")
    assert pilot["total_views"] == "195316422"
    with (tmp_path / "view_snapshot.csv").open(encoding="utf-8-sig") as stream:
        snapshots = [row for row in csv.DictReader(stream) if row["season_id"] == "ATSH_2024"]
    assert len(snapshots) == 14


def test_raw_manifest_binds_only_verified_configured_source() -> None:
    root = Path(__file__).resolve().parents[1]
    rows = raw_manifest_rows(root / "data" / "raw", load_project_config(root))
    assert len(rows) == len(list((root / "data" / "raw").glob("*.json")))
    official = [row for row in rows if row["season_id"] == "ATSH_2024"]
    assert len(official) == 1
    assert official[0]["sha256"]
    assert official[0]["usage_total_usd"] == 0.116
