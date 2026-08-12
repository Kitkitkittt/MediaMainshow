from __future__ import annotations

from typing import Any

from .models import Classification, VideoCandidate
from .normalize import normalize_text, parse_episode_number


def classify_video(
    candidate: VideoCandidate,
    show: dict[str, Any],
    exclusions: tuple[str, ...],
    rules: dict[str, Any],
    *,
    official_channel: bool = False,
    official_full_playlist: bool = False,
) -> Classification:
    score_map = rules["scores"]
    normalized_exclusions = tuple(normalize_text(term) for term in exclusions)
    aliases = {normalize_text(alias) for alias in show["aliases"]}
    alias_match = next((alias for alias in aliases if alias in candidate.normalized_title), None)
    episode_no = parse_episode_number(candidate.title)
    min_duration = int(rules["broad_min_duration_seconds"])
    duration_plausible = (
        candidate.duration_seconds is not None and candidate.duration_seconds >= min_duration
    )
    matched_exclusion = next(
        (
            term
            for term in normalized_exclusions
            if f" {term} " in f" {candidate.normalized_title} "
        ),
        None,
    )
    verified_numbered_episode = (
        (official_channel or official_full_playlist)
        and alias_match
        and episode_no is not None
        and duration_plausible
    )
    if matched_exclusion and not verified_numbered_episode:
        return Classification(
            "EXCLUDE",
            int(score_map["hard_exclusion"]),
            "HIGH",
            episode_no,
            matched_exclusion,
            (f"hard_exclusion:{matched_exclusion}",),
        )

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
    elif episode_no is None and not duration_plausible:
        decision, confidence = "EXCLUDE", "MEDIUM"
        reasons.extend(("episode_number_missing", "duration_too_short"))
    elif score >= int(rules["threshold_high"]):
        decision, confidence = "REVIEW", "LOW"
        reasons.append("source_authority_unverified")
    elif score <= int(rules["threshold_low"]):
        decision, confidence = "EXCLUDE", "MEDIUM"
    else:
        decision, confidence = "REVIEW", "LOW"
    return Classification(decision, score, confidence, episode_no, None, tuple(reasons))
