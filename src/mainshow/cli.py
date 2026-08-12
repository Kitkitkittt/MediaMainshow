from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .apify import ApifyYouTubeClient, load_apify_token, save_raw_run
from .config import load_project_config
from .pipeline import build_pilot
from .registry import write_config_registries

APIDOJO_ACTOR = "apidojo/youtube-scraper-api"
DEFAULT_ACTOR = "streamers/youtube-scraper"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


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
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    root = project_root()
    config = load_project_config(root)
    if args.command == "registry":
        write_config_registries(config, root / args.output)
        return
    if args.command == "build":
        write_config_registries(config, root / args.output)
        result = build_pilot(root / args.raw, root / args.output, config, args.show)
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
