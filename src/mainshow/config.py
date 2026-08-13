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
    social: dict[str, Any]
    derivative_search: dict[str, Any]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream) or {}


def load_project_config(root: Path) -> ProjectConfig:
    config_dir = root / "config"
    shows = load_yaml(config_dir / "shows.yaml").get("shows", {})
    catalog_path = config_dir / "season_catalog_tier3_5.yaml"
    if catalog_path.exists():
        for show_id, seasons in load_yaml(catalog_path).get("seasons", {}).items():
            if show_id not in shows:
                raise KeyError(f"Season catalog references unknown show_id={show_id}")
            shows[show_id]["seasons"] = seasons
    channels = load_yaml(config_dir / "channels.yaml").get("channels", {})
    exclusions = load_yaml(config_dir / "exclusion_terms.yaml").get("hard_exclusions", [])
    classifier = load_yaml(config_dir / "classifier_rules.yaml")
    decisions = load_yaml(config_dir / "decisions.yaml").get("decisions", {})
    social = load_yaml(config_dir / "social_sources.yaml")
    derivative_search = load_yaml(config_dir / "derivative_search_packs.yaml")
    return ProjectConfig(
        shows,
        channels,
        tuple(exclusions),
        classifier,
        decisions,
        social,
        derivative_search,
    )


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
    for source in sources:
        source.setdefault("authority_status", "verified")
        source.setdefault("actor", "streamers/youtube-scraper")
        source.setdefault(
            "max_results", max(int(season.get("expected_episode_count") or 20) + 16, 30)
        )
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


def find_derivative_source(config: ProjectConfig, source_id: str) -> dict[str, Any]:
    for source in derivative_sources(config):
        if source.get("source_id") == source_id:
            return source
    raise KeyError(f"Unknown derivative source_id={source_id}")


def derivative_sources(config: ProjectConfig) -> list[dict[str, Any]]:
    """Return reviewed sources plus one bounded official-channel source per show/channel."""
    explicit = [dict(source) for source in config.social.get("derivative_sources", [])]
    explicit_show_ids = {str(source.get("show_id", "")) for source in explicit}
    generated: list[dict[str, Any]] = []
    for show_id, show in config.shows.items():
        if show_id in explicit_show_ids:
            continue
        channel_ids = [str(value) for value in show.get("primary_youtube_channel_ids", [])]
        if not channel_ids:
            for season in show.get("seasons", []):
                for source in season_sources(season):
                    channel_id = str(source.get("channel_id", ""))
                    if channel_id and channel_id not in channel_ids:
                        channel_ids.append(channel_id)
        for channel_id in channel_ids:
            generated.append(
                {
                    "source_id": f"youtube_{show_id.lower()}_{channel_id[:8]}_derivatives",
                    "show_id": show_id,
                    "source_url": f"https://www.youtube.com/channel/{channel_id}",
                    "queries": [str(show["name"])],
                    "channel_id": channel_id,
                    "actor": "streamers/youtube-scraper",
                    "max_results": 50,
                    "include_shorts": True,
                    "include_livestreams": True,
                    "generated_from": "verified_show_channel",
                }
            )
    return explicit + generated
