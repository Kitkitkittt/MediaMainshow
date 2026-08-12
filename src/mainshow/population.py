from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any

from .config import ProjectConfig, find_source_season, iter_seasons, season_sources
from .pipeline import build_pilot
from .registry import write_config_registries


def _input_urls(payload: dict[str, Any]) -> tuple[str, ...]:
    actor_input = payload.get("actor_input", {})
    values = actor_input.get("startUrls", [])
    urls = tuple(
        str(value.get("url") if isinstance(value, dict) else value) for value in values if value
    )
    binding = actor_input.get("sourceBindingUrl")
    return (*urls, str(binding)) if binding else urls


def load_raw_receipts(raw_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    receipts: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(raw_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        receipts.append((path, payload))
    return receipts


def raw_manifest_rows(raw_dir: Path, config: ProjectConfig) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, payload in load_raw_receipts(raw_dir):
        urls = _input_urls(payload)
        matches = [find_source_season(config, url) for url in urls]
        match = next((value for value in matches if value), None)
        metadata = payload.get("run_metadata", {})
        rows.append(
            {
                "raw_cache_path": path.as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "actor_name": payload.get("actor_name", ""),
                "actor_build_id": payload.get("actor_build_id", ""),
                "actor_run_id": payload.get("actor_run_id", ""),
                "actor_dataset_id": payload.get("dataset_id", ""),
                "retrieved_at": payload.get("retrieved_at", ""),
                "source_urls": "|".join(urls),
                "show_id": match[0] if match else "",
                "season_id": match[2]["season_id"] if match else "",
                "status": metadata.get("status", ""),
                "usage_total_usd": metadata.get("usageTotalUsd", ""),
                "item_count": len(payload.get("items", [])),
            }
        )
    return rows


def _canonical_source(season: dict[str, Any]) -> dict[str, Any] | None:
    sources = season_sources(season)
    explicit = [source for source in sources if source.get("canonical_enumeration") is True]
    if explicit:
        return explicit[0]
    verified = [
        source
        for source in sources
        if source.get("authority_status") == "verified"
        and source.get("source_type") in {"official_full_playlist", "official_show_playlist"}
    ]
    return verified[0] if verified else None


def pending_sources(
    raw_dir: Path, config: ProjectConfig, *, tier: int | None = None
) -> list[tuple[str, dict[str, Any], dict[str, Any]]]:
    observed = {
        url
        for _, payload in load_raw_receipts(raw_dir)
        for url in _input_urls(payload)
        if payload.get("run_metadata", {}).get("status") == "SUCCEEDED"
        and any("id" in item or "videoId" in item for item in payload.get("items", []))
    }
    pending = []
    for show_id, show, season in iter_seasons(config):
        if tier is not None and int(show.get("tier", 0)) != tier:
            continue
        source = _canonical_source(season)
        if (
            source
            and source.get("extraction_status") != "actor_no_videos"
            and source.get("url") not in observed
        ):
            pending.append((show_id, season, source))
    return pending


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames or []), list(reader)


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _consolidate_csv(
    season_dirs: list[Path], filename: str, output_path: Path, dedupe: tuple[str, ...]
) -> None:
    fields: list[str] = []
    rows: list[dict[str, str]] = []
    for directory in season_dirs:
        current_fields, current_rows = _read_csv(directory / filename)
        for field in current_fields:
            if field not in fields:
                fields.append(field)
        rows.extend(current_rows)
    index: dict[tuple[str, ...], dict[str, str]] = {}
    for row in rows:
        index[tuple(row.get(field, "") for field in dedupe)] = row
    _write_csv(output_path, fields, list(index.values()))


def _merge_season_receipts(receipts: list[tuple[Path, dict[str, Any]]], output_path: Path) -> Path:
    """Create one deterministic latest-value view without mutating immutable raw receipts."""
    latest = dict(receipts[-1][1])
    items: dict[str, dict[str, Any]] = {}
    for _, payload in receipts:
        for position, item in enumerate(payload.get("items", [])):
            key = str(
                item.get("id")
                or item.get("videoId")
                or item.get("url")
                or f"{payload.get('actor_run_id', '')}:{position}"
            )
            items[key] = item
    latest["items"] = list(items.values())
    latest["merged_actor_run_ids"] = [payload.get("actor_run_id", "") for _, payload in receipts]
    output_path.write_text(json.dumps(latest, ensure_ascii=False), encoding="utf-8")
    return output_path


def build_all(raw_dir: Path, output_dir: Path, config: ProjectConfig) -> dict[str, int]:
    receipts = load_raw_receipts(raw_dir)
    by_url: defaultdict[str, list[tuple[Path, dict[str, Any]]]] = defaultdict(list)
    for path, payload in receipts:
        for url in _input_urls(payload):
            by_url[url].append((path, payload))

    with tempfile.TemporaryDirectory(prefix="mainshow-build-") as temporary:
        staging = Path(temporary)
        season_dirs: list[Path] = []
        status_rows: list[dict[str, Any]] = []
        for show_id, show, season in iter_seasons(config):
            source = _canonical_source(season)
            source_url = str(source.get("url", "")) if source else ""
            season_receipts = sorted(
                by_url.get(source_url, []), key=lambda value: value[1].get("retrieved_at", "")
            )
            season_dir = staging / season["season_id"]
            result: dict[str, int] | None = None
            if season_receipts:
                raw_path = _merge_season_receipts(
                    season_receipts, staging / f"{season['season_id']}-merged.json"
                )
                result = build_pilot(
                    raw_path,
                    season_dir,
                    config,
                    show_id,
                    season_id=season["season_id"],
                )
            qc_status = "NOT_EXTRACTED"
            if season_receipts:
                _, summaries = _read_csv(season_dir / "season_summary.csv")
                qc_status = summaries[0]["qc_status"] if summaries else "FAIL"
                season_dirs.append(season_dir)
            status_rows.append(
                {
                    "tier": show.get("tier", ""),
                    "show_id": show_id,
                    "season_id": season["season_id"],
                    "season_status": season.get("status", "unknown"),
                    "source_status": season.get(
                        "source_status", "configured" if source else "missing"
                    ),
                    "canonical_source_url": source_url,
                    "raw_receipt_count": len(season_receipts),
                    "candidate_count": result["candidates"] if result else 0,
                    "canonical_episode_count": result["canonical"] if result else 0,
                    "manual_review_count": result["review"] if result else 0,
                    "qc_status": qc_status,
                }
            )

        output_dir.mkdir(parents=True, exist_ok=True)
        write_config_registries(config, output_dir)
        _consolidate_csv(
            season_dirs,
            "episode_registry.csv",
            output_dir / "episode_registry.csv",
            ("season_id", "video_id"),
        )
        _consolidate_csv(
            season_dirs,
            "view_snapshot.csv",
            output_dir / "view_snapshot.csv",
            ("video_id", "snapshot_at"),
        )
        _consolidate_csv(
            season_dirs,
            "season_summary.csv",
            output_dir / "season_summary.csv",
            ("season_id",),
        )
        _consolidate_csv(
            season_dirs,
            "manual_review.csv",
            output_dir / "manual_review.csv",
            ("season", "video_id", "reason_for_review"),
        )
        _write_csv(
            output_dir / "population_status.csv",
            list(status_rows[0]) if status_rows else [],
            status_rows,
        )
        manifest = raw_manifest_rows(raw_dir, config)
        _write_csv(
            output_dir / "raw_manifest.csv",
            list(manifest[0]) if manifest else [],
            manifest,
        )
        report = ["# Consolidated QC report", ""]
        for directory in season_dirs:
            report.append((directory / "qc_report.md").read_text(encoding="utf-8").strip())
            report.extend(("", "---", ""))
        (output_dir / "qc_report.md").write_text(
            "\n".join(report).rstrip() + "\n", encoding="utf-8"
        )

    return {
        "configured_seasons": len(status_rows),
        "extracted_seasons": len(season_dirs),
        "raw_receipts": len(receipts),
    }


def reset_output_directory(output_dir: Path) -> None:
    """Delete only generated output files, never raw evidence or configuration."""
    if output_dir.exists():
        for path in output_dir.iterdir():
            if path.is_file() and path.name != ".gitkeep":
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
