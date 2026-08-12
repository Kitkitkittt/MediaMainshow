from mainshow.classifier import classify_video
from mainshow.models import Provenance, VideoCandidate
from mainshow.normalize import normalize_text

SHOW = {"aliases": ["Anh Trai Say Hi", "ATSH"]}
RULES = {
    "scores": {
        "official_full_playlist": 6,
        "primary_official_channel": 4,
        "exact_show_alias": 4,
        "numbered_episode": 4,
        "plausible_duration": 2,
        "hard_exclusion": -15,
        "unofficial_channel": -8,
        "abnormal_duration": -5,
    },
    "threshold_high": 8,
    "threshold_low": 0,
    "broad_min_duration_seconds": 1500,
}
EXCLUSIONS = ("highlight", "official mv", "concert")


def candidate(title: str, duration: int = 7_200) -> VideoCandidate:
    return VideoCandidate(
        "abc12345678",
        "https://www.youtube.com/watch?v=abc12345678",
        title,
        normalize_text(title),
        "channel",
        "Vie Channel",
        None,
        None,
        None,
        None,
        duration,
        123,
        None,
        None,
        "available",
        "https://www.youtube.com/watch?v=abc12345678",
        Provenance("actor", "run", "dataset", "2026-08-12T12:00:00+07:00"),
        {},
    )


def test_numbered_main_episode_is_included() -> None:
    result = classify_video(
        candidate("Anh Trai Say Hi | Tập 3"),
        SHOW,
        EXCLUSIONS,
        RULES,
        official_channel=True,
    )
    assert result.decision == "INCLUDE"
    assert result.episode_no == 3


def test_hard_exclusions_win_over_positive_signals() -> None:
    assert (
        classify_video(
            candidate("Anh Trai Say Hi | Tập 3 Highlight"), SHOW, EXCLUSIONS, RULES
        ).decision
        == "EXCLUDE"
    )


def test_verified_numbered_episode_can_mention_concert_in_its_title() -> None:
    result = classify_video(
        candidate("ATVNCG Tập 1 | 33 Anh Tài bung miếng & concert cháy hết mình"),
        {"aliases": ["ATVNCG"]},
        EXCLUSIONS,
        RULES,
        official_full_playlist=True,
    )
    assert result.decision == "INCLUDE"
    assert result.episode_no == 1


def test_official_long_numbered_episode_can_mention_derivative_format() -> None:
    result = classify_video(
        candidate(
            "TINH HÀ SAY HI TẬP 2: tranh đấu với 6 set quay Performance Video",
            duration=15_128,
        ),
        {"aliases": ["Tinh Hà Say Hi"]},
        EXCLUSIONS,
        RULES,
        official_channel=True,
    )
    assert result.decision == "INCLUDE"
    assert result.episode_no == 2


def test_short_official_highlight_remains_excluded() -> None:
    result = classify_video(
        candidate("Tinh Hà Say Hi Tập 2 Highlight", duration=600),
        {"aliases": ["Tinh Hà Say Hi"]},
        EXCLUSIONS,
        RULES,
        official_channel=True,
    )
    assert result.decision == "EXCLUDE"
    assert (
        classify_video(candidate("Anh Trai Say Hi | Official MV"), SHOW, EXCLUSIONS, RULES).decision
        == "EXCLUDE"
    )
    assert (
        classify_video(
            candidate("ATVNCG Concert Full 240 phút"), {"aliases": ["ATVNCG"]}, EXCLUSIONS, RULES
        ).decision
        == "EXCLUDE"
    )


def test_numbered_cong_dien_can_pass_without_derivative_marker() -> None:
    show = {"aliases": ["ATVNCG"]}
    result = classify_video(
        candidate("ATVNCG | Công diễn 3 | Tập 8 Full"),
        show,
        EXCLUSIONS,
        RULES,
        official_channel=True,
    )
    assert result.decision == "INCLUDE"
    assert result.episode_no == 8


def test_unverified_source_is_review_even_with_strong_title_and_duration() -> None:
    result = classify_video(candidate("Anh Trai Say Hi | Tập 3"), SHOW, EXCLUSIONS, RULES)
    assert result.decision == "REVIEW"
    assert "source_authority_unverified" in result.reasons


def test_numbered_main_episode_can_mention_tiet_muc() -> None:
    result = classify_video(
        candidate("Anh Trai Say Hi Tập 13: 8 tiết mục solo chung kết"),
        SHOW,
        EXCLUSIONS,
        RULES,
        official_full_playlist=True,
    )
    assert result.decision == "INCLUDE"


def test_verified_playlist_does_not_override_wrong_show_or_missing_episode() -> None:
    wrong_show = classify_video(
        candidate("Say Hi Rực Rỡ - Tập 3"),
        SHOW,
        EXCLUSIONS,
        RULES,
        official_full_playlist=True,
    )
    promo = classify_video(
        candidate('MC Trấn Thành tung hint | Anh Trai "Say Hi"', duration=214),
        SHOW,
        EXCLUSIONS,
        RULES,
        official_full_playlist=True,
    )
    assert wrong_show.decision == "EXCLUDE"
    assert promo.decision == "EXCLUDE"
