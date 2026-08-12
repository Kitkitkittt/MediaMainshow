from __future__ import annotations

import re
import unicodedata
from datetime import timedelta
from typing import Any
from urllib.parse import parse_qs, urlparse

WHITESPACE = re.compile(r"\s+")
EPISODE_PATTERNS = (
    re.compile(r"\b(?:tap|episode)\s*0*(\d{1,3})(?=\D|$)", re.IGNORECASE),
    re.compile(r"\bep\.?\s*0*(\d{1,3})(?=\D|$)", re.IGNORECASE),
)
FINAL_PATTERN = re.compile(r"\b(?:tap cuoi|chung ket|dem chung ket|finale?|final)\b")


def normalize_text(value: str, *, strip_diacritics: bool = True) -> str:
    normalized = unicodedata.normalize("NFKD", value).lower()
    if strip_diacritics:
        normalized = "".join(char for char in normalized if not unicodedata.combining(char))
        normalized = normalized.replace("đ", "d")
    normalized = re.sub(r"[^\w\s]", " ", normalized, flags=re.UNICODE)
    return WHITESPACE.sub(" ", normalized).strip()


def parse_episode_number(title: str) -> int | None:
    normalized = normalize_text(title)
    for pattern in EPISODE_PATTERNS:
        if match := pattern.search(normalized):
            return int(match.group(1))
    return None


def has_final_label(title: str) -> bool:
    return bool(FINAL_PATTERN.search(normalize_text(title)))


def parse_bare_episode_number(title: str, aliases: list[str] | tuple[str, ...]) -> int | None:
    """Parse titles such as 'Mái Ấm Gia Đình Việt 172:' only when explicitly enabled."""
    normalized = normalize_text(title)
    for alias in sorted((normalize_text(value) for value in aliases), key=len, reverse=True):
        match = re.search(rf"\b{re.escape(alias)}\s+(\d{{1,3}})(?=\D|$)", normalized)
        if match:
            return int(match.group(1))
    return None


def parse_video_id(item: dict[str, Any]) -> str | None:
    for key in ("videoId", "id", "video_id"):
        value = item.get(key)
        if isinstance(value, str) and value:
            return value
    url = str(item.get("url") or item.get("videoUrl") or "")
    if not url:
        return None
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path.strip("/") or None
    return parse_qs(parsed.query).get("v", [None])[0]


def parse_playlist_id(url: str) -> str | None:
    if not url:
        return None
    return parse_qs(urlparse(url).query).get("list", [None])[0]


def parse_duration_seconds(value: Any) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, int | float):
        return int(value)
    text = str(value).strip()
    if text.isdigit():
        return int(text)
    if text.startswith("PT"):
        match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", text)
        if match:
            hours, minutes, seconds = (int(part or 0) for part in match.groups())
            return int(timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds())
    parts = text.split(":")
    if all(part.isdigit() for part in parts) and 2 <= len(parts) <= 3:
        values = [int(part) for part in parts]
        if len(values) == 2:
            values.insert(0, 0)
        return values[0] * 3600 + values[1] * 60 + values[2]
    return None


def exact_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    cleaned = str(value).replace(",", "").replace(" ", "")
    return int(cleaned) if cleaned.isdigit() else None
