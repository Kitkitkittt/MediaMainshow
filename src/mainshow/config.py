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


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream) or {}


def load_project_config(root: Path) -> ProjectConfig:
    config_dir = root / "config"
    shows = load_yaml(config_dir / "shows.yaml").get("shows", {})
    channels = load_yaml(config_dir / "channels.yaml").get("channels", {})
    exclusions = load_yaml(config_dir / "exclusion_terms.yaml").get("hard_exclusions", [])
    classifier = load_yaml(config_dir / "classifier_rules.yaml")
    return ProjectConfig(shows, channels, tuple(exclusions), classifier)
