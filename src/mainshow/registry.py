from __future__ import annotations

import csv
from pathlib import Path

from .config import ProjectConfig
from .normalize import normalize_text


def write_config_registries(config: ProjectConfig, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    show_fields = (
        "show_id",
        "show_name",
        "show_name_normalized",
        "aliases",
        "producer",
        "broadcaster",
        "primary_youtube_channel_ids",
        "comparison_group",
        "format_type",
        "notes",
    )
    with (output_dir / "show_registry.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=show_fields)
        writer.writeheader()
        for show_id, show in config.shows.items():
            writer.writerow(
                {
                    "show_id": show_id,
                    "show_name": show["name"],
                    "show_name_normalized": normalize_text(show["name"]),
                    "aliases": "|".join(show["aliases"]),
                    "producer": "",
                    "broadcaster": "",
                    "primary_youtube_channel_ids": "",
                    "comparison_group": show["comparison_group"],
                    "format_type": show["format_type"],
                    "notes": "Official source pending verification",
                }
            )
    season_fields = (
        "show_id",
        "season_id",
        "season_name",
        "season_year",
        "season_number",
        "season_status",
        "expected_episode_count",
        "official_playlist_id",
        "official_playlist_url",
        "season_start_date",
        "season_end_date",
        "format_type",
        "review_status",
    )
    with (output_dir / "season_registry.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=season_fields)
        writer.writeheader()
        for show_id, show in config.shows.items():
            for number, season in enumerate(show["seasons"], start=1):
                writer.writerow(
                    {
                        "show_id": show_id,
                        "season_id": season["season_id"],
                        "season_name": season["season_name"],
                        "season_year": season["year"],
                        "season_number": number,
                        "season_status": season["status"],
                        "expected_episode_count": season.get("expected_episode_count") or "",
                        "official_playlist_id": season.get("official_playlist_id", ""),
                        "official_playlist_url": season.get("official_playlist_url", ""),
                        "season_start_date": "",
                        "season_end_date": "",
                        "format_type": show["format_type"],
                        "review_status": season["review_status"],
                    }
                )
