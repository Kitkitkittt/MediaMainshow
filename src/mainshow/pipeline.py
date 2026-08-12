from __future__ import annotations

import csv
import json
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from .adapters import normalize_actor_item
from .classifier import classify_video
from .config import ProjectConfig, find_season, season_sources
from .models import Provenance

EPISODE_COLUMNS = (
    "show_id",
    "show_name",
    "season_id",
    "season_year",
    "season_status",
    "format_type",
    "episode_no",
    "episode_label",
    "part_no",
    "video_id",
    "video_url",
    "title",
    "normalized_title",
    "channel_id",
    "channel_name",
    "channel_authority",
    "playlist_id",
    "playlist_name",
    "playlist_position",
    "published_at",
    "duration_seconds",
    "season_median_duration",
    "duration_ratio",
    "duration_flag",
    "snapshot_at",
    "age_days",
    "lifetime_views_per_day",
    "view_count",
    "mainshow_flag",
    "canonical_flag",
    "split_episode_flag",
    "reupload_flag",
    "availability_status",
    "classifier_score",
    "classifier_confidence",
    "review_status",
    "exclusion_reason",
    "notes",
    "discovery_method",
    "actor_name",
    "actor_run_id",
    "source_url",
)


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def _age_metrics(
    published_at: str | None, snapshot_at: str, view_count: int | None
) -> tuple[float | str, float | str]:
    if not published_at or view_count is None:
        return "", ""
    try:
        published = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        snapshot = datetime.fromisoformat(snapshot_at.replace("Z", "+00:00"))
    except ValueError:
        return "", ""
    age_days = max((snapshot - published).total_seconds() / 86_400, 0)
    if age_days == 0:
        return 0.0, ""
    return round(age_days, 2), round(view_count / age_days, 2)


def build_pilot(
    raw_path: Path,
    output_dir: Path,
    config: ProjectConfig,
    show_id: str,
    season_id: str | None = None,
) -> dict[str, int]:
    payload = json.loads(raw_path.read_text(encoding="utf-8"))
    provenance = Provenance(
        payload["actor_name"],
        payload["actor_run_id"],
        payload["dataset_id"],
        payload["retrieved_at"],
    )
    show = config.shows[show_id]
    start_urls = payload.get("actor_input", {}).get("startUrls", [])
    source_urls = {value.get("url") if isinstance(value, dict) else value for value in start_urls}
    if season_id:
        configured_show_id, _, season = find_season(config, season_id)
        if configured_show_id != show_id:
            raise ValueError(f"season_id={season_id} does not belong to show_id={show_id}")
    else:
        season = next(
            (
                candidate_season
                for candidate_season in show["seasons"]
                if any(
                    source.get("url") in source_urls for source in season_sources(candidate_season)
                )
            ),
            show["seasons"][0],
        )
    matched_sources = [
        source for source in season_sources(season) if source.get("url") in source_urls
    ]
    official_playlist = any(
        source.get("source_type") == "official_full_playlist"
        and source.get("authority_status") == "verified"
        for source in matched_sources
    )
    episode_rows: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []
    seen_video_ids: set[str] = set()
    logical: defaultdict[int, list[dict[str, Any]]] = defaultdict(list)

    for item in payload["items"]:
        try:
            candidate = normalize_actor_item(item, provenance)
        except ValueError:
            continue
        channel = config.channels.get(candidate.channel_id or "", {})
        authority = channel.get("channel_authority", "unknown")
        official_channel = authority in {
            "primary_producer",
            "primary_broadcaster",
            "official_show_channel",
            "official_distribution_partner",
        }
        classification = classify_video(
            candidate,
            show,
            config.exclusions,
            config.classifier,
            official_channel=official_channel,
            official_full_playlist=official_playlist,
        )
        manual_decision = config.decisions.get(candidate.video_id, {})
        if manual_decision and manual_decision.get("season_id") not in (None, season["season_id"]):
            manual_decision = {}
        decision = str(manual_decision.get("decision", classification.decision)).upper()
        duplicate_video = candidate.video_id in seen_video_ids
        seen_video_ids.add(candidate.video_id)
        canonical = decision == "INCLUDE" and not duplicate_video
        if "canonical" in manual_decision:
            canonical = bool(manual_decision["canonical"]) and not duplicate_video
        age_days, views_per_day = _age_metrics(
            candidate.published_at, provenance.retrieved_at, candidate.view_count
        )
        row = {
            "show_id": show_id,
            "show_name": show["name"],
            "season_id": season["season_id"],
            "season_year": season["year"],
            "season_status": season["status"],
            "format_type": show["format_type"],
            "episode_no": classification.episode_no,
            "episode_label": "",
            "part_no": "",
            "video_id": candidate.video_id,
            "video_url": candidate.video_url,
            "title": candidate.title,
            "normalized_title": candidate.normalized_title,
            "channel_id": candidate.channel_id,
            "channel_name": candidate.channel_name,
            "channel_authority": authority,
            "playlist_id": candidate.playlist_id,
            "playlist_name": candidate.playlist_name,
            "playlist_position": candidate.playlist_position,
            "published_at": candidate.published_at,
            "duration_seconds": candidate.duration_seconds,
            "season_median_duration": "",
            "duration_ratio": "",
            "duration_flag": "",
            "snapshot_at": provenance.retrieved_at,
            "age_days": age_days,
            "lifetime_views_per_day": views_per_day,
            "mainshow_flag": decision == "INCLUDE",
            "canonical_flag": canonical,
            "split_episode_flag": False,
            "reupload_flag": False,
            "availability_status": candidate.availability_status,
            "classifier_score": classification.score,
            "classifier_confidence": classification.confidence,
            "review_status": decision,
            "exclusion_reason": (
                str(manual_decision.get("reason", ""))
                if decision == "EXCLUDE" and manual_decision
                else classification.exclusion_reason or ""
            ),
            "notes": ";".join(
                (
                    *classification.reasons,
                    *(("manual_decision",) if manual_decision else ()),
                    *(
                        (str(manual_decision.get("reason")),)
                        if manual_decision.get("reason")
                        else ()
                    ),
                )
            ),
            "discovery_method": "official_playlist" if official_playlist else "apify_search",
            "actor_name": provenance.actor_name,
            "actor_run_id": provenance.actor_run_id,
            "source_url": candidate.source_url,
            "view_count": candidate.view_count,
            "like_count": candidate.like_count,
            "comment_count": candidate.comment_count,
        }
        episode_rows.append(row)
        if classification.episode_no is not None and canonical:
            logical[classification.episode_no].append(row)
        if decision == "REVIEW" or duplicate_video:
            review_rows.append(
                {
                    "show": show["name"],
                    "season": season["season_id"],
                    "episode_candidate": classification.episode_no,
                    "video_id": candidate.video_id,
                    "title": candidate.title,
                    "channel": candidate.channel_name,
                    "duration": candidate.duration_seconds,
                    "reason_for_review": "duplicate_video"
                    if duplicate_video
                    else ";".join(classification.reasons),
                    "possible_decision": decision,
                }
            )

    duplicate_logical: set[int] = set()
    for episode, rows in logical.items():
        if len(rows) <= 1:
            continue
        forced = [
            row
            for row in rows
            if config.decisions.get(row["video_id"], {}).get("canonical") is True
        ]
        if len(forced) == 1:
            for row in rows:
                row["canonical_flag"] = row is forced[0]
                if row is not forced[0]:
                    row["review_status"] = "EXCLUDE"
                    row["notes"] = f"{row['notes']};superseded_by_manual_canonical".strip(";")
        else:
            duplicate_logical.add(episode)
    for row in episode_rows:
        if row["episode_no"] in duplicate_logical and row["canonical_flag"]:
            row["canonical_flag"] = False
            row["review_status"] = "REVIEW"
            row["notes"] = f"{row['notes']};duplicate_logical_episode".strip(";")

    canonical_rows = [row for row in episode_rows if row["canonical_flag"]]
    canonical_durations = [
        row["duration_seconds"] for row in canonical_rows if row["duration_seconds"] is not None
    ]
    season_median_duration = statistics.median(canonical_durations) if canonical_durations else None
    if season_median_duration:
        for row in episode_rows:
            row["season_median_duration"] = season_median_duration
            if row["duration_seconds"] is not None:
                ratio = row["duration_seconds"] / season_median_duration
                row["duration_ratio"] = round(ratio, 4)
                if 0.60 <= ratio <= 1.60:
                    row["duration_flag"] = "normal"
                elif ratio < 0.35:
                    row["duration_flag"] = "strong_reject_short"
                elif ratio < 0.60:
                    row["duration_flag"] = "review_short"
                else:
                    row["duration_flag"] = "review_long"
    snapshots = [
        {
            "video_id": row["video_id"],
            "show_id": show_id,
            "season_id": row["season_id"],
            "episode_no": row["episode_no"],
            "snapshot_at": provenance.retrieved_at,
            "view_count": row["view_count"],
            "like_count": row["like_count"],
            "comment_count": row["comment_count"],
            "source_method": "apify",
            "actor_name": provenance.actor_name,
            "actor_run_id": provenance.actor_run_id,
        }
        for row in canonical_rows
        if row["view_count"] is not None
    ]
    views = [row["view_count"] for row in canonical_rows if row["view_count"] is not None]
    episode_numbers = sorted(
        row["episode_no"] for row in canonical_rows if row["episode_no"] is not None
    )
    expected = season.get("expected_episode_count")
    contiguous = episode_numbers == list(range(1, max(episode_numbers, default=0) + 1))
    completeness_mismatch = bool(expected and len(set(episode_numbers)) != expected)
    duration_warnings = any(row["duration_flag"] not in ("", "normal") for row in canonical_rows)
    qc_status = (
        "FAIL"
        if duplicate_logical or not contiguous or not canonical_rows or completeness_mismatch
        else "WARNING"
    )
    if (
        expected
        and len(set(episode_numbers)) == expected
        and contiguous
        and all(row["channel_authority"] != "unknown" for row in canonical_rows)
        and not duration_warnings
    ):
        qc_status = "PASS"
    publish_metrics = qc_status != "FAIL" and len(views) == len(canonical_rows)
    max_row = max(canonical_rows, key=lambda row: row["view_count"] or -1, default=None)
    min_row = min(
        canonical_rows,
        key=lambda row: row["view_count"] if row["view_count"] is not None else float("inf"),
        default=None,
    )
    first_5 = [
        row["view_count"]
        for row in canonical_rows
        if row["episode_no"] is not None and row["episode_no"] <= 5
    ]
    first_10 = [
        row["view_count"]
        for row in canonical_rows
        if row["episode_no"] is not None and row["episode_no"] <= 10
    ]
    summary = [
        {
            "show_id": show_id,
            "show_name": show["name"],
            "season_id": season["season_id"],
            "season_year": season["year"],
            "comparison_group": show["comparison_group"],
            "format_type": show["format_type"],
            "season_status": season["status"],
            "expected_episode_count": expected or "",
            "canonical_episode_count": len(canonical_rows),
            "missing_episode_count": (expected - len(set(episode_numbers))) if expected else "",
            "total_views": sum(views) if publish_metrics else "",
            "average_views": round(statistics.mean(views), 2) if publish_metrics else "",
            "median_views": statistics.median(views) if publish_metrics else "",
            "max_episode_no": max_row["episode_no"] if publish_metrics and max_row else "",
            "max_episode_views": max_row["view_count"] if publish_metrics and max_row else "",
            "min_episode_no": min_row["episode_no"] if publish_metrics and min_row else "",
            "min_episode_views": min_row["view_count"] if publish_metrics and min_row else "",
            "first_5_total_views": (sum(first_5) if publish_metrics and len(first_5) == 5 else ""),
            "first_5_avg_views": (
                round(statistics.mean(first_5), 2) if publish_metrics and len(first_5) == 5 else ""
            ),
            "first_10_total_views": (
                sum(first_10) if publish_metrics and len(first_10) == 10 else ""
            ),
            "first_10_avg_views": (
                round(statistics.mean(first_10), 2)
                if publish_metrics and len(first_10) == 10
                else ""
            ),
            "snapshot_at": provenance.retrieved_at,
            "qc_status": qc_status,
            "notes": (
                "Aggregate views across canonical full episodes; not unique viewers or audience."
                if qc_status in {"PASS", "WARNING"}
                else "Pilot totals suppressed on FAIL; unresolved evidence remains."
            ),
        }
    ]

    _write_csv(output_dir / "episode_registry.csv", episode_rows, EPISODE_COLUMNS)
    snapshot_columns = (
        "video_id",
        "show_id",
        "season_id",
        "episode_no",
        "snapshot_at",
        "view_count",
        "like_count",
        "comment_count",
        "source_method",
        "actor_name",
        "actor_run_id",
    )
    prior_snapshots = _read_csv(output_dir / "view_snapshot.csv")
    snapshot_index = {
        (str(row["video_id"]), str(row["snapshot_at"])): row
        for row in [*prior_snapshots, *snapshots]
    }
    all_snapshots = sorted(
        snapshot_index.values(), key=lambda row: (str(row["snapshot_at"]), str(row["video_id"]))
    )
    _write_csv(output_dir / "view_snapshot.csv", all_snapshots, snapshot_columns)
    _write_csv(output_dir / "season_summary.csv", summary, tuple(summary[0]))
    _write_csv(
        output_dir / "manual_review.csv",
        review_rows,
        (
            "show",
            "season",
            "episode_candidate",
            "video_id",
            "title",
            "channel",
            "duration",
            "reason_for_review",
            "possible_decision",
        ),
    )
    excluded_counts: defaultdict[str, int] = defaultdict(int)
    for row in episode_rows:
        if row["review_status"] == "EXCLUDE":
            excluded_counts[row["exclusion_reason"] or "deterministic_non_episode"] += 1
    missing_views = sum(1 for row in canonical_rows if row["view_count"] is None)
    abnormal_durations = sum(
        1 for row in canonical_rows if row["duration_flag"] not in ("", "normal")
    )
    if qc_status == "PASS":
        evidence_line = "Completed-season metrics are publishable under the recorded Phase-1 rules."
    elif qc_status == "WARNING":
        evidence_line = (
            "Completed-season metrics are publishable with the duration caveat recorded above."
        )
    else:
        evidence_line = "Completed-season metrics are suppressed until all FAIL conditions resolve."
    report = [
        f"# {season['season_id']} QC report",
        "",
        f"- Status: **{qc_status}**",
        f"- Actor: `{provenance.actor_name}`",
        f"- Actor run: `{provenance.actor_run_id}`",
        f"- Dataset: `{provenance.dataset_id}`",
        f"- Snapshot: `{provenance.retrieved_at}`",
        f"- Source playlist: `{season.get('official_playlist_url', '')}`",
        f"- Raw candidates: {len(episode_rows)}",
        f"- Canonical episodes: {len(canonical_rows)}",
        f"- Expected episodes: {expected or 'unknown'}",
        f"- Missing exact views: {missing_views}",
        f"- Manual review rows: {len(review_rows)}",
        f"- Duplicate logical episodes: {sorted(duplicate_logical)}",
        f"- Contiguous from E01: {contiguous}",
        f"- Canonical duration flags outside normal range: {abnormal_durations}",
        f"- Exclusions by reason: {dict(sorted(excluded_counts.items()))}",
        "",
        evidence_line,
    ]
    (output_dir / "qc_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    research_rows = sorted(canonical_rows, key=lambda row: row["episode_no"])
    table = [
        f"# {season['season_id']} research output",
        "",
        (
            f"Snapshot: `{provenance.retrieved_at}`. Values are cumulative YouTube main-show "
            "video views, not unique viewers."
        ),
        "",
        "| Ep. | Exact YouTube title | Duration (s) | Published | Channel | Exact views |",
        "| ---: | --- | ---: | --- | --- | ---: |",
    ]
    for row in research_rows:
        safe_title = str(row["title"]).replace("|", "\\|")
        table.append(
            f"| {row['episode_no']} | {safe_title} | {row['duration_seconds']} | "
            f"{row['published_at']} | {row['channel_name']} | {row['view_count']:,} |"
        )
    summary_row = summary[0]
    table.extend(("", "## Season summary", ""))
    if publish_metrics:
        table.extend(
            (
                (
                    "| Show | Season | Episodes | Total views | Avg/ep | Median/ep | "
                    "First 5 views | Peak episode | Status |"
                ),
                "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
                (
                    f"| {show['name']} | {season['season_id']} | {len(canonical_rows)} | "
                    f"{summary_row['total_views']:,} | {summary_row['average_views']:,.0f} | "
                    f"{summary_row['median_views']:,.0f} | "
                    f"{summary_row['first_5_total_views']:,} | "
                    f"E{summary_row['max_episode_no']} "
                    f"({summary_row['max_episode_views']:,}) | {qc_status} |"
                ),
            )
        )
    else:
        table.append(f"Season metrics suppressed because QC status is **{qc_status}**.")
    (output_dir / "research_output.md").write_text("\n".join(table) + "\n", encoding="utf-8")
    return {
        "candidates": len(episode_rows),
        "canonical": len(canonical_rows),
        "review": len(review_rows),
    }
