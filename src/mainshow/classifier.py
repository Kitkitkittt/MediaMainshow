from __future__ import annotations

import re
from typing import Any

from .models import Classification, VideoCandidate
from .normalize import (
    has_final_label,
    normalize_text,
    parse_bare_episode_number,
    parse_episode_number,
)


def _video_type(title: str, rules: dict[str, Any]) -> tuple[str, str | None]:
    normalized = normalize_text(title)
    for video_type, patterns in rules.get("video_types", {}).get("hard", {}).items():
        if any(re.search(pattern, normalized) for pattern in patterns):
            return video_type, video_type
    for video_type, patterns in rules.get("video_types", {}).get("soft", {}).items():
        if any(re.search(pattern, normalized) for pattern in patterns):
            return video_type, video_type
    for video_type, patterns in rules.get("video_types", {}).get("observational", {}).items():
        if any(re.search(pattern, normalized) for pattern in patterns):
            return video_type, video_type
    return "unknown", None


def classify_video(
    candidate: VideoCandidate,
    show: dict[str, Any],
    exclusions: tuple[str, ...],
    rules: dict[str, Any],
    *,
    official_channel: bool = False,
    official_full_playlist: bool = False,
    excluded_channel: bool = False,
    season: dict[str, Any] | None = None,
) -> Classification:
    score_map = rules["scores"]
    normalized_exclusions = tuple(normalize_text(term) for term in exclusions)
    aliases = {normalize_text(alias) for alias in show["aliases"]}
    alias_match = next((alias for alias in aliases if alias in candidate.normalized_title), None)
    episode_no = parse_episode_number(candidate.title)
    episode_label: str | None = None
    video_type = "unknown"
    if episode_no is None and season and season.get("episode_number_mode") == "bare_after_alias":
        episode_no = parse_bare_episode_number(candidate.title, tuple(show["aliases"]))
    if episode_no is None and season and has_final_label(candidate.title):
        expected = season.get("expected_episode_count")
        if expected:
            episode_no = int(season.get("episode_number_start", 1)) + int(expected) - 1
            episode_label = "finale"
    if episode_no == 0:
        video_type = "special_extra"
    min_duration = int(rules["broad_min_duration_seconds"])
    duration_plausible = (
        candidate.duration_seconds is not None and candidate.duration_seconds >= min_duration
    )
    detected_video_type, typed_exclusion = _video_type(candidate.title, rules)
    if video_type != "special_extra":
        video_type = detected_video_type
    matched_exclusion = next(
        (
            term
            for term in normalized_exclusions
            if f" {term} " in f" {candidate.normalized_title} "
        ),
        None,
    )
    annual_full_show = bool(
        season
        and show.get("format_type") == "annual_special"
        and alias_match
        and candidate.duration_seconds is not None
        and candidate.duration_seconds >= int(rules.get("annual_min_duration_seconds", 9_000))
        and video_type == "unknown"
    )
    if annual_full_show:
        episode_no = 1
        episode_label = "annual full show"
        video_type = "annual_full_show"
    elif season and show.get("format_type") == "annual_special" and alias_match:
        video_type = "annual_segment"
        typed_exclusion = "annual_segment"
    if excluded_channel:
        video_type = "non_main_channel"
        typed_exclusion = "non_main_channel_authority"
    hard_typed_exclusion = video_type in {
        "special_extra",
        "annual_segment",
        "non_main_channel",
    } or (
        typed_exclusion is not None and video_type in rules.get("video_types", {}).get("hard", {})
    )
    verified_numbered_episode = (
        (official_channel or official_full_playlist)
        and alias_match
        and episode_no is not None
        and duration_plausible
        and not hard_typed_exclusion
    )
    if (hard_typed_exclusion or matched_exclusion) and not verified_numbered_episode:
        exclusion_reason = typed_exclusion or matched_exclusion
        return Classification(
            decision="EXCLUDE",
            score=int(score_map["hard_exclusion"]),
            confidence="HIGH",
            episode_no=episode_no,
            episode_label=episode_label,
            video_type=video_type,
            exclusion_reason=exclusion_reason,
            reasons=(f"video_type:{video_type}",),
        )

    if video_type == "unknown" and episode_no is not None:
        video_type = "main_episode"

    reasons: list[str] = []
    score = 0
    if alias_match:
        score += int(score_map["exact_show_alias"])
        reasons.append("show_alias")

    if episode_no is not None:
        score += int(score_map["numbered_episode"])
        reasons.append("numbered_episode")

    if official_channel:
        score += int(score_map["primary_official_channel"])
        reasons.append("official_channel")
    if official_full_playlist:
        score += int(score_map["official_full_playlist"])
        reasons.append("official_full_playlist")
    if candidate.duration_seconds is not None and candidate.duration_seconds >= min_duration:
        score += int(score_map["plausible_duration"])
        reasons.append("plausible_duration")

    source_verified = official_channel or official_full_playlist
    required_mainshow_evidence = source_verified and alias_match and episode_no is not None
    if score >= int(rules["threshold_high"]) and required_mainshow_evidence:
        decision, confidence = "INCLUDE", "HIGH"
    elif not alias_match:
        decision, confidence = "EXCLUDE", "HIGH"
        reasons.append("show_alias_missing")
    elif episode_no is None:
        decision, confidence = "EXCLUDE", "MEDIUM"
        reasons.append("episode_number_missing")
        if not duration_plausible:
            reasons.append("duration_too_short")
    elif not duration_plausible and not source_verified:
        decision, confidence = "EXCLUDE", "MEDIUM"
        reasons.extend(("source_authority_unverified", "duration_too_short"))
    elif not source_verified:
        # Search Actors can return videos from any channel, even when the query
        # starts from an official channel URL. Fail closed unless the item's
        # channel or containing playlist is independently verified.
        decision, confidence = "EXCLUDE", "HIGH"
        reasons.append("source_authority_unverified")
    elif score >= int(rules["threshold_high"]):
        decision, confidence = "REVIEW", "LOW"
        reasons.append("episode_identity_unresolved")
    elif score <= int(rules["threshold_low"]):
        decision, confidence = "EXCLUDE", "MEDIUM"
    else:
        decision, confidence = "REVIEW", "LOW"
    return Classification(
        decision=decision,
        score=score,
        confidence=confidence,
        episode_no=episode_no,
        episode_label=episode_label,
        video_type=video_type,
        exclusion_reason=None,
        reasons=tuple(reasons),
    )
