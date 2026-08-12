from __future__ import annotations

from typing import Any

from .models import Provenance, VideoCandidate
from .normalize import (
    exact_int,
    normalize_text,
    parse_duration_seconds,
    parse_playlist_id,
    parse_video_id,
)


def _first(item: dict[str, Any], *keys: str) -> Any:
    return next((item[key] for key in keys if item.get(key) not in (None, "")), None)


def normalize_actor_item(item: dict[str, Any], provenance: Provenance) -> VideoCandidate:
    video_id = parse_video_id(item)
    if not video_id:
        raise ValueError("Actor item has no usable YouTube video ID")
    title = str(_first(item, "title", "name") or "")
    video_url = str(
        _first(item, "url", "videoUrl") or f"https://www.youtube.com/watch?v={video_id}"
    )
    duration = _first(item, "durationSeconds", "lengthSeconds", "duration", "durationText")
    source_page = str(_first(item, "fromYTUrl", "input") or "")
    return VideoCandidate(
        video_id=video_id,
        video_url=video_url,
        title=title,
        normalized_title=normalize_text(title),
        channel_id=_first(item, "channelId", "channel_id"),
        channel_name=_first(item, "channelName", "channelTitle", "channel"),
        playlist_id=_first(item, "playlistId", "playlist_id") or parse_playlist_id(source_page),
        playlist_name=_first(item, "playlistName", "playlistTitle"),
        playlist_position=exact_int(_first(item, "playlistPosition", "position", "index", "order")),
        published_at=_first(item, "date", "publishedAt", "uploadDate", "published_at"),
        duration_seconds=parse_duration_seconds(duration),
        view_count=exact_int(_first(item, "viewCount", "views", "view_count")),
        like_count=exact_int(_first(item, "likes", "likeCount", "like_count")),
        comment_count=exact_int(_first(item, "commentsCount", "commentCount", "comment_count")),
        availability_status=str(_first(item, "availability", "availabilityStatus") or "available"),
        source_url=video_url,
        provenance=provenance,
        raw=item,
    )
