from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .apify import ApifyYouTubeClient, load_apify_token, save_raw_run
from .config import find_season, load_project_config, season_sources
from .pipeline import build_pilot
from .population import build_all, pending_sources
from .registry import write_config_registries

APIDOJO_ACTOR = "apidojo/youtube-scraper-api"
DEFAULT_ACTOR = "streamers/youtube-scraper"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _source_input(actor: str, url: str, max_results: int) -> dict[str, object]:
    if actor == APIDOJO_ACTOR:
        return {
            "startUrls": [url],
            "maxItems": max_results,
            "includeShorts": False,
            "includeLiveStreams": False,
        }
    return {
        "startUrls": [{"url": url}],
        "maxResults": max_results,
        "maxResultsShorts": 0,
        "maxResultStreams": 0,
    }


def _canonical_source(season: dict[str, object]) -> dict[str, object]:
    sources = season_sources(season)
    explicit = [source for source in sources if source.get("canonical_enumeration") is True]
    candidates = explicit or [
        source
        for source in sources
        if source.get("authority_status") == "verified"
        and source.get("source_type") in {"official_full_playlist", "official_show_playlist"}
    ]
    if not candidates:
        raise RuntimeError(f"No verified canonical source configured for {season['season_id']}")
    return candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build auditable YouTube main-show datasets")
    subparsers = parser.add_subparsers(dest="command", required=True)
    registry_parser = subparsers.add_parser("registry", help="Build configuration registries")
    registry_parser.add_argument("--output", type=Path, default=Path("outputs"))
    build_parser = subparsers.add_parser(
        "build", help="Rebuild pilot outputs from a cached raw run"
    )
    build_parser.add_argument("raw", type=Path)
    build_parser.add_argument("--show", default="ATSH")
    build_parser.add_argument("--season")
    build_parser.add_argument("--output", type=Path, default=Path("outputs"))
    pilot_parser = subparsers.add_parser("pilot", help="Run one bounded paid actor pilot")
    pilot_parser.add_argument("--show", default="ATSH")
    pilot_parser.add_argument("--search-limit", type=int, default=20, choices=range(1, 51))
    pilot_parser.add_argument("--actor", default=DEFAULT_ACTOR)
    pilot_parser.add_argument(
        "--source-url", help="Known official video, playlist, channel, or search-results URL"
    )
    resume_parser = subparsers.add_parser(
        "resume", help="Resume a completed Apify run without starting a new paid run"
    )
    resume_parser.add_argument("run_id")
    resume_parser.add_argument("--show", default="ATSH")
    resume_parser.add_argument("--actor", default=DEFAULT_ACTOR)
    subparsers.add_parser("build-all", help="Rebuild every configured season from cached runs")
    pending_parser = subparsers.add_parser(
        "pending", help="List configured canonical sources without successful raw receipts"
    )
    pending_parser.add_argument("--tier", type=int)
    extract_parser = subparsers.add_parser(
        "extract-season", help="Run the configured canonical source for one season"
    )
    extract_parser.add_argument("season_id")
    extract_parser.add_argument("--max-results", type=int)
    extract_parser.add_argument("--max-charge-usd", type=float, default=1.0)
    populate_parser = subparsers.add_parser(
        "extract-pending", help="Extract pending configured sources within one cumulative cap"
    )
    populate_parser.add_argument("--tier", type=int)
    populate_parser.add_argument("--budget-cap-usd", type=float, required=True)
    populate_parser.add_argument("--limit-seasons", type=int)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    root = project_root()
    config = load_project_config(root)
    if args.command == "registry":
        write_config_registries(config, root / args.output)
        return
    if args.command == "build":
        write_config_registries(config, root / args.output)
        result = build_pilot(
            root / args.raw,
            root / args.output,
            config,
            args.show,
            season_id=args.season,
        )
        logging.info("Built pilot outputs %s", result)
        return
    if args.command == "resume":
        with ApifyYouTubeClient(load_apify_token()) as client:
            run = client.fetch(args.actor, args.run_id)
        raw_path = save_raw_run(run, root / "data" / "raw")
        write_config_registries(config, root / "outputs")
        result = build_pilot(raw_path, root / "outputs", config, args.show)
        logging.info("Resumed pilot raw=%s outputs=%s", raw_path, result)
        return
    if args.command == "build-all":
        result = build_all(root / "data" / "raw", root / "outputs", config)
        logging.info("Built consolidated outputs %s", result)
        return
    if args.command == "pending":
        for show_id, season, source in pending_sources(
            root / "data" / "raw", config, tier=args.tier
        ):
            print(f"{show_id}\t{season['season_id']}\t{source['url']}")
        return
    if args.command == "extract-season":
        show_id, _, season = find_season(config, args.season_id)
        source = _canonical_source(season)
        actor = str(source.get("actor", DEFAULT_ACTOR))
        max_results = int(args.max_results or source.get("max_results", 50))
        with ApifyYouTubeClient(load_apify_token()) as client:
            run = client.run(
                actor,
                _source_input(actor, str(source["url"]), max_results),
                max_total_charge_usd=args.max_charge_usd,
            )
        raw_path = save_raw_run(run, root / "data" / "raw")
        result = build_all(root / "data" / "raw", root / "outputs", config)
        logging.info(
            "Extracted show=%s season=%s raw=%s result=%s",
            show_id,
            args.season_id,
            raw_path,
            result,
        )
        return
    if args.command == "extract-pending":
        sources = pending_sources(root / "data" / "raw", config, tier=args.tier)
        if args.limit_seasons:
            sources = sources[: args.limit_seasons]
        spent = 0.0
        with ApifyYouTubeClient(load_apify_token()) as client:
            for show_id, season, source in sources:
                remaining = args.budget_cap_usd - spent
                if remaining <= 0:
                    logging.warning("Budget cap reached before season=%s", season["season_id"])
                    break
                actor = str(source.get("actor", DEFAULT_ACTOR))
                max_results = int(source.get("max_results", 50))
                run = client.run(
                    actor,
                    _source_input(actor, str(source["url"]), max_results),
                    max_total_charge_usd=min(remaining, 1.0),
                )
                save_raw_run(run, root / "data" / "raw")
                cost = float(run.run_metadata.get("usageTotalUsd", 0) or 0)
                spent += cost
                logging.info(
                    "Extracted show=%s season=%s items=%d cost_usd=%.4f cumulative_usd=%.4f",
                    show_id,
                    season["season_id"],
                    len(run.items),
                    cost,
                    spent,
                )
        result = build_all(root / "data" / "raw", root / "outputs", config)
        logging.info("Extraction wave complete spent_usd=%.4f result=%s", spent, result)
        return
    show = config.shows[args.show]
    if args.actor == APIDOJO_ACTOR:
        run_input = {
            "maxItems": args.search_limit,
            "includeShorts": False,
            "includeLiveStreams": False,
        }
        if args.source_url:
            run_input["startUrls"] = [args.source_url]
        else:
            run_input["keywords"] = [f"{show['name']} tập full"]
    else:
        run_input = {
            "maxResults": args.search_limit,
            "maxResultsShorts": 0,
            "maxResultStreams": 0,
        }
        if args.source_url:
            run_input["startUrls"] = [{"url": args.source_url}]
        else:
            run_input["searchQueries"] = [f"{show['name']} tập full"]
    with ApifyYouTubeClient(load_apify_token()) as client:
        run = client.run(args.actor, run_input)
    raw_path = save_raw_run(run, root / "data" / "raw")
    write_config_registries(config, root / "outputs")
    result = build_pilot(raw_path, root / "outputs", config, args.show)
    logging.info("Pilot raw=%s outputs=%s", raw_path, result)


if __name__ == "__main__":
    main()
