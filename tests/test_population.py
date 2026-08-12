import csv
from pathlib import Path

from mainshow.config import load_project_config
from mainshow.population import build_all, raw_manifest_rows


def test_cached_build_consolidates_pilot_without_paid_calls(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    config = load_project_config(root)
    result = build_all(root / "data" / "raw", tmp_path, config)
    assert result == {"configured_seasons": 7, "extracted_seasons": 1, "raw_receipts": 3}
    with (tmp_path / "season_summary.csv").open(encoding="utf-8-sig") as stream:
        summaries = list(csv.DictReader(stream))
    assert summaries[0]["season_id"] == "ATSH_2024"
    assert summaries[0]["total_views"] == "195316422"
    with (tmp_path / "view_snapshot.csv").open(encoding="utf-8-sig") as stream:
        assert len(list(csv.DictReader(stream))) == 14


def test_raw_manifest_binds_only_verified_configured_source() -> None:
    root = Path(__file__).resolve().parents[1]
    rows = raw_manifest_rows(root / "data" / "raw", load_project_config(root))
    assert len(rows) == 3
    official = [row for row in rows if row["season_id"] == "ATSH_2024"]
    assert len(official) == 1
    assert official[0]["sha256"]
    assert official[0]["usage_total_usd"] == 0.116
