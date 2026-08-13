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
    "annual_min_duration_seconds": 9000,
    "video_types": {
        "hard": {
            "preview": [r"\b(?:teaser|trailer|preview|xem truoc)\b"],
            "clip_or_segment": [r"^(?:game|hai tet)\b"],
            "compilation": [r"^(?!.*\btap \d).*(?:^top|\bnhung .* top) \d+\b"],
        },
        "soft": {"performance": [r"\bperformance\b"]},
    },
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


def test_source_bound_finale_maps_to_expected_episode() -> None:
    result = classify_video(
        candidate("Sao Nhập Ngũ 2025 TẬP CUỐI", duration=5_459),
        {"aliases": ["Sao Nhập Ngũ"], "format_type": "episodic_reality"},
        EXCLUSIONS,
        RULES,
        official_channel=True,
        season={"expected_episode_count": 16},
    )
    assert result.decision == "INCLUDE"
    assert result.episode_no == 16
    assert result.episode_label == "finale"


def test_bare_numbered_rolling_episode_is_included_only_when_configured() -> None:
    result = classify_video(
        candidate("Mái Ấm Gia Đình Việt 172: Lâm Bảo Ngọc", duration=5_574),
        {"aliases": ["Mái Ấm Gia Đình Việt"], "format_type": "rolling_weekly"},
        EXCLUSIONS,
        RULES,
        official_channel=True,
        official_full_playlist=True,
        season={"episode_number_mode": "bare_after_alias"},
    )
    assert result.decision == "INCLUDE"
    assert result.episode_no == 172


def test_explicit_segment_type_overrides_episode_reference() -> None:
    result = classify_video(
        candidate("GAME VÀO PHÒNG | Tinh Hà Say Hi Tập 5", duration=3_458),
        {"aliases": ["Tinh Hà Say Hi"], "format_type": "closed_season"},
        EXCLUSIONS,
        RULES,
        official_channel=True,
    )
    assert result.decision == "EXCLUDE"
    assert result.video_type == "clip_or_segment"


def test_annual_full_show_maps_to_one_without_accepting_segments() -> None:
    show = {"aliases": ["Sóng"], "format_type": "annual_special"}
    full_show = classify_video(
        candidate("Sóng 24 - Chương trình giải trí Đêm Giao Thừa 2024", duration=15_652),
        show,
        EXCLUSIONS,
        RULES,
        official_channel=True,
        season={"expected_episode_count": 1},
    )
    segment = classify_video(
        candidate("HÀI TẾT 2024: Dương Lâm | Sóng 24", duration=2_236),
        show,
        EXCLUSIONS,
        RULES,
        official_channel=True,
        season={"expected_episode_count": 1},
    )
    assert full_show.decision == "INCLUDE"
    assert full_show.episode_no == 1
    assert full_show.video_type == "annual_full_show"
    assert segment.decision == "EXCLUDE"


def test_episode_zero_is_a_special_extra() -> None:
    result = classify_video(
        candidate("Đấu Trường Gia Tốc Tập 0", duration=5_000),
        {"aliases": ["Đấu Trường Gia Tốc"], "format_type": "closed_season"},
        EXCLUSIONS,
        RULES,
        official_channel=True,
    )
    assert result.decision == "EXCLUDE"
    assert result.video_type == "special_extra"


def test_annual_segment_and_music_channel_mirror_are_excluded() -> None:
    show = {"aliases": ["Sóng"], "format_type": "annual_special"}
    segment = classify_video(
        candidate("#2 Sóng VieON - Đêm nhạc giải trí", duration=4_928),
        show,
        EXCLUSIONS,
        RULES,
        official_channel=True,
        season={"expected_episode_count": 1},
    )
    mirror = classify_video(
        candidate("Sóng 24 - Chương trình Đêm Giao Thừa", duration=15_652),
        show,
        EXCLUSIONS,
        RULES,
        excluded_channel=True,
        season={"expected_episode_count": 1},
    )
    assert segment.decision == "EXCLUDE"
    assert segment.video_type == "annual_segment"
    assert mirror.decision == "EXCLUDE"
    assert mirror.video_type == "non_main_channel"


def test_unknown_channel_search_hit_fails_closed_instead_of_review() -> None:
    result = classify_video(
        candidate("FAPtv Com Nguoi: Tap 232 - Giac Mo Rap Viet", duration=4_014),
        {"aliases": ["Rap Viet"], "format_type": "closed_season"},
        EXCLUSIONS,
        RULES,
    )
    assert result.decision == "EXCLUDE"
    assert "source_authority_unverified" in result.reasons


def test_top_n_inside_numbered_episode_is_not_a_compilation() -> None:
    result = classify_video(
        candidate("Rap Việt Mùa 3 - Tập 15: Chung kết 1 - Top 9 lột xác", duration=8_000),
        {"aliases": ["Rap Việt"], "format_type": "closed_season"},
        EXCLUSIONS,
        RULES,
        official_channel=True,
        official_full_playlist=True,
    )
    assert result.decision == "INCLUDE"
    assert result.video_type == "main_episode"
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


def test_unverified_source_fails_closed_even_with_strong_title_and_duration() -> None:
    result = classify_video(candidate("Anh Trai Say Hi | Tập 3"), SHOW, EXCLUSIONS, RULES)
    assert result.decision == "EXCLUDE"
    assert "source_authority_unverified" in result.reasons
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


def test_expanded_derivative_types_are_hard_exclusions() -> None:
    expanded = {
        **RULES,
        "video_types": {
            "hard": {
                **RULES["video_types"]["hard"],
                "highlight": [r"\bhighlight\b"],
                "uncut_extended": [r"\buncut\b"],
                "reaction_commentary": [r"\breaction\b"],
                "dance_practice": [r"\bdance practice\b"],
                "short_form": [r"\bshorts?\b"],
            },
            "soft": RULES["video_types"]["soft"],
        },
    }
    cases = {
        "Anh Trai Say Hi HIGHLIGHT Táº­p 6": "highlight",
        "Anh Trai Say Hi UNCUT vòng loại": "uncut_extended",
        "Anh Trai Say Hi REACTION": "reaction_commentary",
        "Anh Trai Say Hi DANCE PRACTICE": "dance_practice",
        "Anh Trai Say Hi #shorts": "short_form",
    }
    for title, expected in cases.items():
        result = classify_video(
            candidate(title, duration=600),
            SHOW,
            EXCLUSIONS,
            expanded,
            official_channel=True,
        )
        assert result.decision == "EXCLUDE"
        assert result.video_type == expected
