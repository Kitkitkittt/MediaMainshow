from __future__ import annotations

import csv
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

from .adapters import normalize_actor_item
from .config import ProjectConfig
from .models import Provenance
from .normalize import normalize_text, parse_episode_number

EPISODE_TOKEN = re.compile(r"\b(?:tap|episode|ep)\.?\s*0*\d{1,3}\b", re.IGNORECASE)
SEASON_SUFFIX = re.compile(r"\b(?:mua|season)\s*\d{1,2}\b|\b20\d{2}\b", re.IGNORECASE)


def cluster_prefix(title: str) -> str:
    normalized = normalize_text(title)
    match = EPISODE_TOKEN.search(normalized)
    if not match:
        return ""
    prefix = normalized[: match.start()].strip()
    prefix = SEASON_SUFFIX.sub(" ", prefix)
    return " ".join(prefix.split()).strip()


def _known_aliases(config: ProjectConfig) -> set[str]:
    return {
        normalize_text(alias)
        for show in config.shows.values()
        for alias in show.get("aliases", [])
        if len(normalize_text(alias)) >= 4
    }


def _write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def discover_unknown_shows(
    raw_dir: Path, output_dir: Path, config: ProjectConfig
) -> dict[str, int]:
    official_channels = {
        channel_id
        for channel_id, channel in config.channels.items()
        if channel.get("channel_authority")
        in {
            "primary_producer",
            "primary_broadcaster",
            "official_show_channel",
            "official_distribution_partner",
        }
    }
    known_aliases = _known_aliases(config)
    clusters: defaultdict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    scanned = 0
    for path in sorted(raw_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        provenance = Provenance(
            payload.get("actor_name", ""),
            payload.get("actor_run_id", ""),
            payload.get("dataset_id", ""),
            payload.get("retrieved_at", ""),
        )
        for item in payload.get("items", []):
            try:
                candidate = normalize_actor_item(item, provenance)
            except ValueError:
                continue
            scanned += 1
            if candidate.channel_id not in official_channels:
                continue
            episode_no = parse_episode_number(candidate.title)
            prefix = cluster_prefix(candidate.title)
            if (
                episode_no is None
                or not prefix
                or candidate.duration_seconds is None
                or candidate.duration_seconds < 1_500
            ):
                continue
            if any(alias == prefix or alias in prefix for alias in known_aliases):
                continue
            clusters[(candidate.channel_id, prefix)].append(
                {
                    "channel_id": candidate.channel_id,
                    "channel_name": candidate.channel_name,
                    "cluster_prefix": prefix,
                    "episode_no": episode_no,
                    "video_id": candidate.video_id,
                    "title": candidate.title,
                    "duration_seconds": candidate.duration_seconds,
                    "published_at": candidate.published_at,
                    "actor_run_id": provenance.actor_run_id,
                    "source_url": candidate.source_url,
                }
            )

    accepted: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    for (channel_id, prefix), rows in sorted(clusters.items()):
        episode_numbers = sorted({int(row["episode_no"]) for row in rows})
        continuity = len(episode_numbers) / (max(episode_numbers) - min(episode_numbers) + 1)
        median_duration = statistics.median(int(row["duration_seconds"]) for row in rows)
        accepted_cluster = (
            len(episode_numbers) >= 4 and continuity >= 0.60 and median_duration >= 1_500
        )
        for row in rows:
            evidence.append(
                {
                    **row,
                    "distinct_episode_count": len(episode_numbers),
                    "episode_continuity": round(continuity, 4),
                    "median_duration_seconds": median_duration,
                    "cluster_accepted": accepted_cluster,
                }
            )
        if accepted_cluster:
            accepted.append(
                {
                    "candidate_show_name": prefix,
                    "candidate_show_name_normalized": prefix,
                    "channel_id": channel_id,
                    "channel_name": rows[0]["channel_name"],
                    "distinct_episode_count": len(episode_numbers),
                    "min_episode_no": min(episode_numbers),
                    "max_episode_no": max(episode_numbers),
                    "episode_continuity": round(continuity, 4),
                    "median_duration_seconds": median_duration,
                    "discovered_by": "channel_scan",
                    "review_status": "REVIEW",
                }
            )

    _write_csv(
        output_dir / "candidate_show_registry.csv",
        (
            "candidate_show_name",
            "candidate_show_name_normalized",
            "channel_id",
            "channel_name",
            "distinct_episode_count",
            "min_episode_no",
            "max_episode_no",
            "episode_continuity",
            "median_duration_seconds",
            "discovered_by",
            "review_status",
        ),
        accepted,
    )
    _write_csv(
        output_dir / "candidate_cluster_evidence.csv",
        (
            "channel_id",
            "channel_name",
            "cluster_prefix",
            "episode_no",
            "video_id",
            "title",
            "duration_seconds",
            "published_at",
            "actor_run_id",
            "source_url",
            "distinct_episode_count",
            "episode_continuity",
            "median_duration_seconds",
            "cluster_accepted",
        ),
        evidence,
    )
    return {"scanned_videos": scanned, "clusters": len(clusters), "accepted": len(accepted)}
