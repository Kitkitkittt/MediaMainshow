from pathlib import Path

import pytest

from mainshow.config import find_season, load_project_config, season_sources


def test_find_season_and_legacy_source_normalization() -> None:
    root = Path(__file__).resolve().parents[1]
    config = load_project_config(root)
    show_id, show, season = find_season(config, "ATSH_2024")
    assert show_id == "ATSH"
    assert show["name"] == 'Anh Trai "Say Hi"'
    source = season_sources(season)[0]
    assert source["source_type"] == "official_full_playlist"
    assert source["authority_status"] == "verified"
    assert source["url"].startswith("https://www.youtube.com/playlist?")


def test_unknown_season_fails_closed() -> None:
    root = Path(__file__).resolve().parents[1]
    with pytest.raises(KeyError, match="Unknown season_id"):
        find_season(load_project_config(root), "NOT_A_SEASON")
