from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

from .adapters import normalize_actor_item
from .classifier import classify_video
from .config import ProjectConfig, derivative_sources, find_source_season
from .models import Provenance

TYPE_TO_ROLE = {
    "short_form": "SHORT",
    "preview": "TEASER_PREVIEW",
    "promo": "TEASER_PREVIEW",
    "highlight": "HIGHLIGHT",
    "recap": "RECAP",
    "reaction_commentary": "REACTION_COMMENTARY",
    "uncut_extended": "UNCUT_EXTENDED",
    "backstage": "BEHIND_THE_SCENES",
    "production_diary": "BEHIND_THE_SCENES",
    "dance_practice": "DANCE_PRACTICE",
    "interview_press": "INTERVIEW_PRESS",
    "cast_content": "CAST_CONTENT",
    "compilation": "COMPILATION",
    "music_asset": "MUSIC_ASSET",
    "ost_theme": "MUSIC_ASSET",
    "clip_or_segment": "CLIP_OR_SEGMENT",
    "special_extra": "SPECIAL_EXTRA",
    "livestream": "LIVESTREAM",
    "performance": "PERFORMANCE",
    "interview": "INTERVIEW",
    "annual_segment": "ANNUAL_SEGMENT",
}

PROFILE_HOSTS = {
    "facebook.com": "facebook",
    "www.facebook.com": "facebook",
    "fb.com": "facebook",
    "www.fb.com": "facebook",
    "instagram.com": "instagram",
    "www.instagram.com": "instagram",
    "tiktok.com": "tiktok",
    "www.tiktok.com": "tiktok",
    "threads.com": "threads",
    "www.threads.com": "threads",
    "threads.net": "threads",
    "www.threads.net": "threads",
    "x.com": "x",
    "www.x.com": "x",
    "twitter.com": "x",
    "www.twitter.com": "x",
}

NON_PROFILE_ROOTS = {
    "hashtag",
    "p",
    "reel",
    "reels",
    "stories",
    "watch",
    "groups",
    "share",
    "sharer",
    "photo",
    "photos",
    "video",
    "videos",
    "intent",
    "search",
}

DERIVATIVE_COLUMNS = [
    "platform",
    "native_content_id",
    "content_url",
    "show_id",
    "season_id",
    "title",
    "platform_format",
    "content_role",
    "authority_class",
    "relationship_target_type",
    "relationship_evidence",
    "classification_state",
    "review_status",
    "published_at",
    "duration_seconds",
    "view_count",
    "like_count",
    "comment_count",
    "availability_status",
    "actor_run_id",
    "source_url",
]


@dataclass(frozen=True)
class NormalizedSocialItem:
    platform: str
    native_content_id: str
    content_url: str
    published_at: str | None
    text: str | None
    account_native_id: str | None
    account_handle: str | None
    platform_format: str
    metrics: dict[str, int]


def normalize_social_item(platform: str, item: dict[str, Any]) -> NormalizedSocialItem:
    """Normalize a connector item without pretending unsupported fields are zero."""
    native_id = str(item.get("native_content_id") or item.get("id") or "").strip()
    content_url = str(item.get("content_url") or item.get("url") or item.get("permalink") or "")
    if not native_id or not content_url:
        raise ValueError("A social item requires native content ID and URL")
    metrics: dict[str, int] = {}
    for name, value in (item.get("metrics") or {}).items():
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"Metric {name} must be an exact integer or null")
        metrics[str(name)] = value
    return NormalizedSocialItem(
        platform=platform,
        native_content_id=native_id,
        content_url=content_url,
        published_at=item.get("published_at") or item.get("timestamp"),
        text=item.get("text") or item.get("caption") or item.get("title"),
        account_native_id=item.get("account_native_id") or item.get("author_id"),
        account_handle=item.get("account_handle") or item.get("username"),
        platform_format=str(item.get("platform_format") or item.get("media_type") or "UNKNOWN"),
        metrics=metrics,
    )


def _write_csv(path: Path, columns: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def _receipt_urls(payload: dict[str, Any]) -> tuple[str, ...]:
    actor_input = payload.get("actor_input", {})
    start_urls = tuple(
        str(value.get("url") if isinstance(value, dict) else value)
        for value in actor_input.get("startUrls", [])
        if value
    )
    binding = actor_input.get("sourceBindingUrl")
    return (*start_urls, str(binding)) if binding else start_urls


def _receipt_context(config: ProjectConfig, payload: dict[str, Any]) -> tuple[str, str]:
    for url in _receipt_urls(payload):
        match = find_source_season(config, url)
        if match:
            return match[0], str(match[2]["season_id"])
    return "", ""


def _social_profile(url: str) -> tuple[str, str, str] | None:
    try:
        parsed = urlsplit(unquote(url.strip()))
    except ValueError:
        return None
    platform = PROFILE_HOSTS.get(parsed.hostname.lower() if parsed.hostname else "")
    parts = [part for part in parsed.path.split("/") if part]
    if not platform or not parts:
        return None
    root = parts[0].lower()
    if root in NON_PROFILE_ROOTS:
        return None
    if platform in {"tiktok", "threads"} and not root.startswith("@"):
        return None
    handle = root.lstrip("@").strip()
    if not handle:
        return None
    host = {
        "facebook": "www.facebook.com",
        "instagram": "www.instagram.com",
        "tiktok": "www.tiktok.com",
        "threads": "www.threads.com",
        "x": "x.com",
    }[platform]
    prefix = "@" if platform in {"tiktok", "threads"} else ""
    normalized = f"https://{host}/{prefix}{handle}"
    return platform, handle, normalized


def _platform_format(row: dict[str, str]) -> str:
    title = row.get("normalized_title", "")
    url = row.get("video_url", "")
    if "/shorts/" in url or "#short" in title or " shorts" in f" {title}":
        return "SHORT"
    if row.get("video_type") == "livestream":
        return "LIVESTREAM"
    return "VIDEO"


def derivative_rows(episode_registry: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in _read_csv(episode_registry):
        canonical = row.get("canonical_flag", "").lower() == "true"
        if canonical and row.get("video_type") not in TYPE_TO_ROLE:
            continue
        video_type = row.get("video_type", "unknown")
        role = TYPE_TO_ROLE.get(video_type, "UNKNOWN")
        authority = row.get("channel_authority", "")
        reviewed_authority = bool(authority and authority != "unknown")
        if row.get("reupload_flag", "").lower() == "true" or video_type == "non_main_channel":
            role = "UNKNOWN_REUPLOAD"
        accepted = role not in {"UNKNOWN", "UNKNOWN_REUPLOAD"} and reviewed_authority
        state = "ACCEPTED" if accepted and not canonical else "NEEDS_REVIEW"
        rows.append(
            {
                "platform": "youtube",
                "native_content_id": row.get("video_id", ""),
                "content_url": row.get("video_url", ""),
                "show_id": row.get("show_id", ""),
                "season_id": row.get("season_id", ""),
                "title": row.get("title", ""),
                "platform_format": _platform_format(row),
                "content_role": role,
                "authority_class": authority.upper() if reviewed_authority else "UNVERIFIED",
                "relationship_target_type": "EPISODE" if row.get("episode_no") else "SEASON",
                "relationship_evidence": (
                    "OFFICIAL_PLAYLIST_COLLECTION" if reviewed_authority else "INFERRED"
                ),
                "classification_state": state,
                "review_status": "CANONICAL_OVERLAP" if canonical else state,
                "published_at": row.get("published_at", ""),
                "duration_seconds": row.get("duration_seconds", ""),
                "view_count": row.get("view_count", ""),
                "like_count": "",
                "comment_count": "",
                "availability_status": row.get("availability_status", ""),
                "actor_run_id": row.get("actor_run_id", ""),
                "source_url": row.get("source_url", ""),
            }
        )
    return rows


def derivative_receipt_rows(raw_dir: Path, config: ProjectConfig) -> list[dict[str, Any]]:
    """Normalize separately-bound derivative runs; never feed them to canonical QC."""
    rows: list[dict[str, Any]] = []
    source_by_id = {str(source.get("source_id")): source for source in derivative_sources(config)}
    for path in sorted(raw_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        source = source_by_id.get(str(payload.get("actor_input", {}).get("derivativeSourceId", "")))
        if not source:
            continue
        show = config.shows[str(source["show_id"])]
        season_id = str(source.get("season_id", ""))
        season = next(
            (item for item in show["seasons"] if item["season_id"] == season_id), None
        )
        provenance = Provenance(
            str(payload.get("actor_name", "")),
            str(payload.get("actor_run_id", "")),
            str(payload.get("dataset_id", "")),
            str(payload.get("retrieved_at", "")),
        )
        for item in payload.get("items", []):
            try:
                candidate = normalize_actor_item(item, provenance)
            except ValueError:
                continue
            authority = config.channels.get(candidate.channel_id or "", {}).get(
                "channel_authority", "unknown"
            )
            source_channel_match = candidate.channel_id == source.get("channel_id")
            classification = classify_video(
                candidate,
                show,
                config.exclusions,
                config.classifier,
                official_channel=source_channel_match,
                season=season,
            )
            role = TYPE_TO_ROLE.get(classification.video_type, "UNKNOWN")
            accepted = role != "UNKNOWN" and source_channel_match and authority != "unknown"
            rows.append(
                {
                    "platform": "youtube",
                    "native_content_id": candidate.video_id,
                    "content_url": candidate.video_url,
                    "show_id": source["show_id"],
                    "season_id": season_id,
                    "title": candidate.title,
                    "platform_format": (
                        "SHORT"
                        if str(item.get("type", "")).lower() == "shorts"
                        else "LIVESTREAM"
                        if str(item.get("type", "")).lower() == "stream"
                        else "VIDEO"
                    ),
                    "content_role": role,
                    "authority_class": (
                        authority.upper() if authority != "unknown" else "UNVERIFIED"
                    ),
                    "relationship_target_type": (
                        "EPISODE"
                        if classification.episode_no
                        else "SEASON"
                        if season_id
                        else "SHOW"
                    ),
                    "relationship_evidence": "EXPLICIT_TEXT_LINK",
                    "classification_state": "ACCEPTED" if accepted else "NEEDS_REVIEW",
                    "review_status": "ACCEPTED" if accepted else "NEEDS_REVIEW",
                    "published_at": candidate.published_at or "",
                    "duration_seconds": candidate.duration_seconds or "",
                    "view_count": candidate.view_count if candidate.view_count is not None else "",
                    "like_count": candidate.like_count if candidate.like_count is not None else "",
                    "comment_count": (
                        candidate.comment_count if candidate.comment_count is not None else ""
                    ),
                    "availability_status": candidate.availability_status,
                    "actor_run_id": provenance.actor_run_id,
                    "source_url": str(source["source_url"]),
                }
            )
    return rows


def pending_derivative_sources(raw_dir: Path, config: ProjectConfig) -> list[dict[str, Any]]:
    """Return sources with no retained live receipt, including accepted partial receipts."""
    recorded: set[str] = set()
    for path in raw_dir.glob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        source_id = str(payload.get("actor_input", {}).get("derivativeSourceId", ""))
        if source_id:
            recorded.add(source_id)
    return [
        source for source in derivative_sources(config) if str(source["source_id"]) not in recorded
    ]


def social_account_rows(raw_dir: Path, config: ProjectConfig) -> list[dict[str, Any]]:
    evidence: defaultdict[tuple[str, str, str], dict[str, Any]] = defaultdict(
        lambda: {
            "seasons": set(),
            "receipt_ids": set(),
            "video_ids": set(),
            "official_video_ids": set(),
            "source_channels": set(),
            "evidence_urls": set(),
            "first_observed_at": "",
            "last_observed_at": "",
        }
    )
    for path in sorted(raw_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        show_id, season_id = _receipt_context(config, payload)
        if not show_id:
            continue
        observed = str(payload.get("retrieved_at", ""))
        receipt_id = str(payload.get("actor_run_id") or path.stem)
        for item in payload.get("items", []):
            video_id = str(item.get("id") or item.get("videoId") or "")
            if not video_id:
                continue
            channel_id = str(item.get("channelId") or "")
            channel_authority = config.channels.get(channel_id, {}).get(
                "channel_authority", "unknown"
            )
            reviewed_channel = channel_authority not in {"unknown", "unofficial", ""}
            for link in item.get("descriptionLinks") or []:
                url = str(link.get("url", "") if isinstance(link, dict) else link)
                profile = _social_profile(url)
                if not profile:
                    continue
                platform, handle, profile_url = profile
                record = evidence[(show_id, platform, profile_url)]
                record["seasons"].add(season_id)
                record["receipt_ids"].add(receipt_id)
                record["video_ids"].add(video_id)
                if reviewed_channel:
                    record["official_video_ids"].add(video_id)
                record["source_channels"].add(channel_id)
                record["evidence_urls"].add(str(item.get("url") or ""))
                if not record["first_observed_at"] or observed < record["first_observed_at"]:
                    record["first_observed_at"] = observed
                if observed > record["last_observed_at"]:
                    record["last_observed_at"] = observed

    verified = {
        (str(source.get("show_id", "")), str(source.get("platform", "")), source.get("account_url"))
        for source in config.social.get("verified_sources", [])
    }
    rows: list[dict[str, Any]] = []
    for (show_id, platform, profile_url), record in sorted(evidence.items()):
        is_verified = (show_id, platform, profile_url) in verified
        rows.append(
            {
                "show_id": show_id,
                "season_ids": "|".join(sorted(record["seasons"])),
                "platform": platform,
                "account_handle": profile_url.rsplit("/", 1)[-1].lstrip("@"),
                "account_url": profile_url,
                "authority_class": "SHOW_OWNER" if is_verified else "SOURCE_LINKED_CANDIDATE",
                "authority_status": "VERIFIED" if is_verified else "NEEDS_REVIEW",
                "evidence_video_count": len(record["video_ids"]),
                "official_evidence_video_count": len(record["official_video_ids"]),
                "evidence_strength": (
                    "HIGH"
                    if len(record["official_video_ids"]) >= 3
                    else "MEDIUM"
                    if record["official_video_ids"]
                    else "LOW"
                ),
                "evidence_receipt_count": len(record["receipt_ids"]),
                "source_channel_ids": "|".join(sorted(record["source_channels"] - {""})),
                "first_observed_at": record["first_observed_at"],
                "last_observed_at": record["last_observed_at"],
                "evidence_video_urls": "|".join(sorted(record["evidence_urls"] - {""})[:10]),
            }
        )
    return rows


def query_plan_rows(config: ProjectConfig) -> list[dict[str, Any]]:
    defaults = config.derivative_search.get("defaults", {})
    rows: list[dict[str, Any]] = []
    for show_id, show in config.shows.items():
        for role, pack in config.derivative_search.get("roles", {}).items():
            terms = [str(term) for term in pack.get("terms", [])]
            query_terms = " OR ".join(f'"{term}"' if " " in term else term for term in terms)
            rows.append(
                {
                    "show_id": show_id,
                    "show_name": show["name"],
                    "content_role": role,
                    "query": f'"{show["name"]}" ({query_terms})',
                    "max_results": defaults.get("max_results_per_query", 30),
                    "include_shorts": defaults.get("include_shorts", True),
                    "include_livestreams": defaults.get("include_livestreams", True),
                    "run_status": "NOT_RUN",
                }
            )
    return rows


def build_social_outputs(
    raw_dir: Path,
    episode_registry: Path,
    output_dir: Path,
    config: ProjectConfig,
    *,
    derivative_raw_dir: Path | None = None,
) -> dict[str, int]:
    derivatives = derivative_rows(episode_registry)
    if derivative_raw_dir:
        index = {(row["platform"], row["native_content_id"]): row for row in derivatives}
        for row in derivative_receipt_rows(derivative_raw_dir, config):
            index[(row["platform"], row["native_content_id"])] = row
        derivatives = list(index.values())
    accounts = social_account_rows(raw_dir, config)
    query_plan = query_plan_rows(config)
    _write_csv(output_dir / "derivative_content_registry.csv", DERIVATIVE_COLUMNS, derivatives)
    registry_index = {
        row.get("video_id", ""): row.get("snapshot_at", "") for row in _read_csv(episode_registry)
    }
    snapshots: list[dict[str, Any]] = []
    for row in derivatives:
        for metric_name in ("view_count", "like_count", "comment_count"):
            value = row.get(metric_name)
            if value in (None, ""):
                continue
            snapshots.append(
                {
                    "platform": row["platform"],
                    "native_content_id": row["native_content_id"],
                    "metric_name": metric_name,
                    "metric_value_exact": int(value),
                    "observed_at": registry_index.get(row["native_content_id"], ""),
                    "metric_definition_version": "youtube_public_v1",
                    "visibility": "PUBLIC",
                    "receipt_id": row.get("actor_run_id", ""),
                }
            )
    snapshot_columns = list(snapshots[0]) if snapshots else [
        "platform",
        "native_content_id",
        "metric_name",
        "metric_value_exact",
        "observed_at",
        "metric_definition_version",
        "visibility",
        "receipt_id",
    ]
    _write_csv(output_dir / "social_metric_snapshot.csv", snapshot_columns, snapshots)
    account_columns = list(accounts[0]) if accounts else [
        "show_id",
        "season_ids",
        "platform",
        "account_handle",
        "account_url",
        "authority_class",
        "authority_status",
        "evidence_video_count",
        "official_evidence_video_count",
        "evidence_strength",
        "evidence_receipt_count",
        "source_channel_ids",
        "first_observed_at",
        "last_observed_at",
        "evidence_video_urls",
    ]
    _write_csv(output_dir / "social_account_candidates.csv", account_columns, accounts)
    _write_csv(
        output_dir / "derivative_search_plan.csv",
        list(query_plan[0]) if query_plan else [],
        query_plan,
    )
    coverage = []
    for platform, values in config.social.get("platforms", {}).items():
        candidate_count = sum(1 for row in accounts if row["platform"] in platform)
        availability = values.get("availability", "NOT_RUN")
        coverage.append(
            {
                "platform": platform,
                "availability": availability,
                "discovery_modes": "|".join(values.get("discovery_modes", [])),
                "public_metrics": "|".join(values.get("public_metrics", [])),
                "owner_metrics": "|".join(values.get("owner_metrics", [])),
                "credential_gate": values.get("credential_gate", ""),
                "freshness_sla_days": values.get("freshness_sla_days", ""),
                "source_linked_account_candidates": candidate_count,
                "run_status": "PASS" if platform == "youtube" else availability,
            }
        )
    _write_csv(
        output_dir / "social_platform_coverage.csv",
        list(coverage[0]) if coverage else [],
        coverage,
    )
    return {
        "derivative_candidates": len(derivatives),
        "social_account_candidates": len(accounts),
        "search_plan_rows": len(query_plan),
        "metric_snapshots": len(snapshots),
    }
