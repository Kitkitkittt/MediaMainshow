from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Provenance:
    actor_name: str
    actor_run_id: str
    dataset_id: str
    retrieved_at: str


@dataclass
class VideoCandidate:
    video_id: str
    video_url: str
    title: str
    normalized_title: str
    channel_id: str | None
    channel_name: str | None
    playlist_id: str | None
    playlist_name: str | None
    playlist_position: int | None
    published_at: str | None
    duration_seconds: int | None
    view_count: int | None
    like_count: int | None
    comment_count: int | None
    availability_status: str
    source_url: str
    provenance: Provenance
    raw: dict[str, Any] = field(repr=False)


@dataclass(frozen=True)
class Classification:
    decision: str
    score: int
    confidence: str
    episode_no: int | None
    episode_label: str | None
    video_type: str
    exclusion_reason: str | None
    reasons: tuple[str, ...]


def row_dict(value: Any) -> dict[str, Any]:
    return asdict(value)
