from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ProjectConfig:
    shows: dict[str, dict[str, Any]]
    channels: dict[str, dict[str, Any]]
    exclusions: tuple[str, ...]
    classifier: dict[str, Any]
    decisions: dict[str, dict[str, Any]]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream) or {}


def load_project_config(root: Path) -> ProjectConfig:
    config_dir = root / "config"
    shows = load_yaml(config_dir / "shows.yaml").get("shows", {})
    channels = load_yaml(config_dir / "channels.yaml").get("channels", {})
    exclusions = load_yaml(config_dir / "exclusion_terms.yaml").get("hard_exclusions", [])
    classifier = load_yaml(config_dir / "classifier_rules.yaml")
    decisions = load_yaml(config_dir / "decisions.yaml").get("decisions", {})
    return ProjectConfig(shows, channels, tuple(exclusions), classifier, decisions)


def iter_seasons(config: ProjectConfig):
    for show_id, show in config.shows.items():
        for season in show.get("seasons", []):
            yield show_id, show, season


def find_season(config: ProjectConfig, season_id: str):
    for show_id, show, season in iter_seasons(config):
        if season["season_id"] == season_id:
            return show_id, show, season
    raise KeyError(f"Unknown season_id={season_id}")


def season_sources(season: dict[str, Any]) -> list[dict[str, Any]]:
    sources = [dict(source) for source in season.get("sources", [])]
    legacy_url = season.get("official_playlist_url")
    if legacy_url and all(source.get("url") != legacy_url for source in sources):
        sources.insert(
            0,
            {
                "source_type": "official_full_playlist",
                "url": legacy_url,
                "playlist_id": season.get("official_playlist_id", ""),
                "authority_status": "verified",
                "actor": "streamers/youtube-scraper",
                "max_results": max(int(season.get("expected_episode_count") or 20) + 16, 30),
            },
        )
    return sources


def find_source_season(config: ProjectConfig, url: str):
    for show_id, show, season in iter_seasons(config):
        for source in season_sources(season):
            if source.get("url") == url:
                return show_id, show, season, source
    return None
