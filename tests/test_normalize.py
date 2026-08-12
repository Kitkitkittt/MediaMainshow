from mainshow.normalize import (
    exact_int,
    normalize_text,
    parse_bare_episode_number,
    parse_duration_seconds,
    parse_episode_number,
    parse_playlist_id,
)


def test_normalize_vietnamese_and_episode_patterns() -> None:
    assert normalize_text("TẬP 01 – Chung kết") == "tap 01 chung ket"
    assert parse_episode_number("Anh Trai Say Hi | Tập 3") == 3
    assert parse_episode_number("Rap Việt - EP.01") == 1
    assert parse_episode_number("Sao Nhập Ngũ 2023 TẬP 7I Chậm mà chắc") == 7
    assert (
        parse_bare_episode_number(
            "Mái Ấm Gia Đình Việt 172: Lâm Bảo Ngọc", ["Mái Ấm Gia Đình Việt"]
        )
        == 172
    )


def test_parse_exact_machine_values() -> None:
    assert exact_int("17,492,843") == 17_492_843
    assert exact_int("17M") is None
    assert parse_duration_seconds("2:03:04") == 7_384
    assert parse_duration_seconds("PT1H5M2S") == 3_902
    assert parse_playlist_id("https://www.youtube.com/playlist?list=PL123") == "PL123"
