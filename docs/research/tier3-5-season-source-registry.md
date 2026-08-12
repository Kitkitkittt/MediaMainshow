# Tier 3-5 season source registry

**Evidence cutoff:** 2026-08-12  
**Scope:** the 19 programs named in the Tier 3-5 seed handoff.  
**Authority rule:** only first-party broadcaster, producer, program-site, and official YouTube channel/video/playlist surfaces are admitted. Search results were used only to locate those first-party surfaces. No Apify actor or credential was used.

## Registry semantics

- `completed`, `airing`, and `upcoming` describe the state at the cutoff, not the present-day state when this file is later read.
- `expected_main_count` is populated only when a first-party catalog, finale, or complete numbered run binds the count. A YouTube playlist's raw item count is not automatically an episode count.
- `clean` means the official playlist reconciles to full numbered main shows. `mixed` means the playlist is official but also contains trailers, recaps, highlights, uncut cuts, shorts, or unrelated contamination and therefore requires title/video-level filtering.
- `format_type` is a show-level population policy: `episodic_reality`, `closed_season`, `rolling_weekly`, or `annual_special`. None of the verified rows required `limited_special`.
- A missing playlist is a source gap, not permission to substitute a fan playlist. Mirrored official uploads map to one logical episode.

## Official YouTube authorities

| Authority | Channel ID | Programs / role |
|---|---:|---|
| [2 Ngày 1 Đêm Vietnam](https://www.youtube.com/channel/UChGncdgzOKmp5XQTnQa2h4w) | `UChGncdgzOKmp5XQTnQa2h4w` | 2 Ngày 1 Đêm primary archive |
| [Chạy Đi Chờ Chi](https://www.youtube.com/channel/UCSpmT3hpL4J_4ievnGzkmsQ) | `UCSpmT3hpL4J_4ievnGzkmsQ` | Running Man Vietnam Mùa 1 archive |
| [Running Man Vietnam - Chạy Ngay Đi](https://www.youtube.com/channel/UCjTlq6Z0HG8C7BVI8x5BOnA) | `UCjTlq6Z0HG8C7BVI8x5BOnA` | Running Man 2026 primary program channel |
| [FOREST STUDIO](https://www.youtube.com/channel/UCTOWyiIkPEqyh_2O-ArJR5w) | `UCTOWyiIkPEqyh_2O-ArJR5w` | Running Man Mùa 3; Xuân Hạ Thu Đông Rồi Lại Xuân |
| [YEAH1 SHOW](https://www.youtube.com/channel/UCh_zF2FsiCflCPgYDudtcqg) | `UCh_zF2FsiCflCPgYDudtcqg` | Gia Đình Haha full shows |
| [YeaH1 Giải Trí](https://www.youtube.com/channel/UCecta98cdYVFV6L_lfH__IA) | `UCecta98cdYVFV6L_lfH__IA` | Gia Đình Haha trailers/promos |
| [Sao Nhập Ngũ](https://www.youtube.com/channel/UCzZ94GZFgqqx6Pzbnj3UMjA) | `UCzZ94GZFgqqx6Pzbnj3UMjA` | Sao Nhập Ngũ; Bậc Thầy Săn Thưởng |
| [Chiến Sĩ Quả Cảm](https://www.youtube.com/channel/UC7TbGjadpjgOfnUoA-iW6Dg) | `UC7TbGjadpjgOfnUoA-iW6Dg` | Chiến Sĩ Quả Cảm |
| [Đấu Trường Gia Tốc](https://www.youtube.com/channel/UC5bxATIALkxlwWQzACzdjHw) | `UC5bxATIALkxlwWQzACzdjHw` | Đấu Trường Gia Tốc; legacy Chơi Là Chạy / Hành Trình Rực Rỡ archive |
| [Đông Tây Promotion Official](https://www.youtube.com/channel/UCFMEYTv6N64hIL9FlQ_hxBw) | `UCFMEYTv6N64hIL9FlQ_hxBw` | Tổ Đội 1 Không 2; La Cà Hát Ca; Anh Trai & Cái Đuôi Nhỏ; official umbrella playlists |
| [Halotimes TV](https://www.youtube.com/channel/UCgL3LEm7JuJNXKWDQTmbuYA) | `UCgL3LEm7JuJNXKWDQTmbuYA` | Về Quê Làm Giàu |
| [TV HUB](https://www.youtube.com/channel/UC1VAL4j9yiPQVKMtIS1yUOA) | `UC1VAL4j9yiPQVKMtIS1yUOA` | Bố Ơi! Mình Đi Đâu Thế? Mùa 5 |
| [HTV Entertainment](https://www.youtube.com/channel/UCbq8aOyj9ZtIqcD-0MwG1fQ) | `UCbq8aOyj9ZtIqcD-0MwG1fQ` | Broadcaster mirrors for multiple HTV7 shows |
| [Mẹ Vắng Nhà - Ba Là Siêu Nhân](https://www.youtube.com/channel/UCT4q1IIX1rWoN95I-_89aVw) | `UCT4q1IIX1rWoN95I-_89aVw` | Mẹ Vắng Nhà, Ba Là Siêu Nhân |
| [Bee Comm Network](https://www.youtube.com/channel/UClOMHp76zB3wHcKGYxTRWFA) | `UClOMHp76zB3wHcKGYxTRWFA` | Current Mái Ấm Gia Đình Việt producer archive |
| [Vie Channel](https://www.youtube.com/channel/UCkna2OcuN1E6u5I8GVtdkOw) | `UCkna2OcuN1E6u5I8GVtdkOw` | Sóng main-program archive |
| [Vie Channel MUSIC](https://www.youtube.com/channel/UC2fu6CiFfNYz5UFORvFyc0w) | `UC2fu6CiFfNYz5UFORvFyc0w` | Sóng music/performance mirror |

Channel identity is evidence of authority, not an instruction to ingest every upload on the channel.

## 1. 2 Ngày 1 Đêm

`format_type: episodic_reality`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---|---|---:|---|---|
| Mùa 1 | 2022-2023 | completed | 31 | [`PLY-AuYi7sTugPLS6_J0oa1wFmWkCExstr`](https://www.youtube.com/playlist?list=PLY-AuYi7sTugPLS6_J0oa1wFmWkCExstr) | Official playlist is a clean numbered run 1-31. |
| Mùa 2 | 2023-2024 | completed | 19 | [`PLY-AuYi7sTugYnwSrAy9DQtC-sAoitZDJ`](https://www.youtube.com/playlist?list=PLY-AuYi7sTugYnwSrAy9DQtC-sAoitZDJ) | Main numbering continues globally at 32-50; the official playlist has 25 items because six are non-main extras. |
| Mùa 3 / Lễ Hội 2024 | 2024-2025 | completed | 30 | [`PLY-AuYi7sTuiekcFnXNeSR2-r_zPbuiLz`](https://www.youtube.com/playlist?list=PLY-AuYi7sTuiekcFnXNeSR2-r_zPbuiLz) | Official main run is global episodes 51-80. |
| Mùa 4 | 2025-2026 | completed | 17 | [`PLY-AuYi7sTujnjUSFEFLK6a5FX_CQ7_14`](https://www.youtube.com/playlist?list=PLY-AuYi7sTujnjUSFEFLK6a5FX_CQ7_14) | Main run is global episodes 81-97. The playlist has 18 items because one unrelated *Say Hi Rực Rỡ* upload is contamination. The [official episode 94 page](https://www.youtube.com/watch?v=eJ5bGiSt-M0) binds the program channel and season context. |

Population rule: retain the season key and the global displayed episode number; do not renumber Mùa 2-4 from 1. A second official Mùa 4 mirror exists on Dong Tay Promotion (`PLy_TpcUT2LZtXvH1z8NTxInXdl09ODACC`), but the program-channel playlists above are the preferred canonical discovery surfaces.

## 2. Running Man Vietnam / Chạy Đi Chờ Chi / Chạy Ngay Đi

`format_type: episodic_reality`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---|---|---:|---|---|
| Mùa 1 — Chạy Đi Chờ Chi | 2019 | completed | 15 | [`PLyb1d5OP9TmFphpG73S6sUrQm5uXV7IrJ`](https://www.youtube.com/playlist?list=PLyb1d5OP9TmFphpG73S6sUrQm5uXV7IrJ) | Official channel playlist contains 15 full episodes; the [official episode 2 page](https://www.youtube.com/watch?v=9fDw0IpvulQ) exposes that exact playlist and channel identity. |
| Mùa 2 — Chơi Là Chạy | 2021 | completed | 15 | [`PLG7CUxrpEOnfzfuMy-SQsENMcthLsO_v-`](https://www.youtube.com/playlist?list=PLG7CUxrpEOnfzfuMy-SQsENMcthLsO_v-) | The [official episode 15 finale](https://www.youtube.com/watch?v=xW0DtfvHkzw) closes the numbered run. The hosting channel was later renamed Đấu Trường Gia Tốc; retain the immutable channel ID. |
| Mùa 3 — Chạy Ngay Đi | 2025-2026 | completed | 16 | [`PLxNMBnO9F8FOdZR7YLDrrT0bk3WaYyApf`](https://www.youtube.com/playlist?list=PLxNMBnO9F8FOdZR7YLDrrT0bk3WaYyApf) | [Official episode 16](https://www.youtube.com/watch?v=5_ktCUWKhm0) is the final numbered episode. Playlist has 18 items because two long retrospective programs are extras. |
| 2026 — Chạy Ngay Đi | 2026 | airing | unknown; episodes 1-3 published by cutoff | **Gap — no season-level full-main playlist exposed yet** | The new program-channel [episode 3](https://www.youtube.com/watch?v=Yj8BPShct2Y) premiered 2026-08-07 and links the new official channel ID `UCjTlq6Z0HG8C7BVI8x5BOnA`; episode 1 and 2 are also linked from the same first-party page. Do not merge this reset-to-1 run into Mùa 3. |

## 3. Gia Đình Haha

`format_type: episodic_reality`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---|---|---:|---|---|
| Mùa 1 | 2025-2026 | completed | 20 | [`PLt3LgMEKzFxz_bKONMLhVVhqGkvgmz0rY`](https://www.youtube.com/playlist?list=PLt3LgMEKzFxz_bKONMLhVVhqGkvgmz0rY) | The [official episode 15 page](https://www.youtube.com/watch?v=pB-AoylTecw) calls itself the final journey and directly exposes the exact show playlist. Episodes 16-20 are the contiguous special return to Bản Liền; VTV identifies [episode 20 as the closing program](https://vtv.vn/buc-thu-tinh-gui-lai-cua-gia-dinh-haha-100260214225739076.htm). |
| Mùa 2 — Quán Nhà Haha | 2026 | upcoming | unknown | **Gap — not published** | VTV's first-party announcements describe [the new Mùa 2 format](https://vtv.vn/gia-dinh-haha-mua-2-co-dien-mao-moi-100260512144825086.htm) and [an October 2026 planned opening](https://vtv.vn/quan-nha-haha-doi-hinh-cu-ap-luc-moi-100260528214309592.htm). |

Important correction: `PLt3LgMEKzFxzJoCs9IE7LuiFrcB1P7V44` is a Tân Binh Toàn Năng derivative playlist linked under “other shows”; it is **not** Gia Đình Haha.

## 4. Sao Nhập Ngũ

`format_type: episodic_reality`

The [official Sao Nhập Ngũ playlists surface](https://www.youtube.com/channel/UCzZ94GZFgqqx6Pzbnj3UMjA/playlists) establishes the following editions. Legacy playlist item counts are not used as episode counts because those archives split episodes into parts and mix related material.

| Edition | Year | Status | expected_main_count | Exact official playlist | Scope note |
|---|---:|---|---:|---|---|
| Mùa 1 — Vượt Qua Giới Hạn | 2017 | completed | unknown | [`PLC_d5n_vB0CptpsuXpJwuxHpwWxlv1Tme`](https://www.youtube.com/playlist?list=PLC_d5n_vB0CptpsuXpJwuxHpwWxlv1Tme) | Official legacy playlist; multipart/mixed. |
| Mùa 2 — Thử Thách Bản Lĩnh | 2017 | completed | unknown | [`PLC_d5n_vB0CrwHkJz3hUNhzdEMhzHiIvg`](https://www.youtube.com/playlist?list=PLC_d5n_vB0CrwHkJz3hUNhzdEMhzHiIvg) | Official legacy playlist; multipart/mixed. |
| Mùa 3 — Kỷ Luật Thép | 2017 | completed | unknown | [`PLC_d5n_vB0Cp3lgS7G06G9w1mChbxZUf_`](https://www.youtube.com/playlist?list=PLC_d5n_vB0Cp3lgS7G06G9w1mChbxZUf_) | Official legacy playlist; multipart/mixed. |
| Mùa 4 — Bông Hồng Thép | 2017 | completed | unknown | [`PLC_d5n_vB0CqCdnDzNstfo0Gsjgkoou5x`](https://www.youtube.com/playlist?list=PLC_d5n_vB0CqCdnDzNstfo0Gsjgkoou5x) | Official legacy playlist; multipart/mixed. |
| Mùa 5 — Không Gục Ngã | 2018 | completed | unknown | [`PLC_d5n_vB0CoGXjo5DpopjFxHny_Ep9hH`](https://www.youtube.com/playlist?list=PLC_d5n_vB0CoGXjo5DpopjFxHny_Ep9hH) | Official legacy playlist; multipart/mixed. |
| Mùa 6 — Biệt Đội Chống Độc | 2018 | completed | unknown | [`PLC_d5n_vB0CphKjGtYpd6u7LJvJ9l3WCd`](https://www.youtube.com/playlist?list=PLC_d5n_vB0CphKjGtYpd6u7LJvJ9l3WCd) | Official legacy playlist; multipart/mixed. |
| Mùa 7 — Lá Chắn Thép | 2018 | completed | unknown | [`PLC_d5n_vB0Co88uDvJGUYQ9npjPoaySdB`](https://www.youtube.com/playlist?list=PLC_d5n_vB0Co88uDvJGUYQ9npjPoaySdB) | Official legacy playlist; multipart/mixed. |
| Mùa 8 — Đối Mặt Với Biển | 2019 | completed | unknown | [`PLC_d5n_vB0CqDKc1F_pBYsL8ma1oaAP4n`](https://www.youtube.com/playlist?list=PLC_d5n_vB0CqDKc1F_pBYsL8ma1oaAP4n) | Official legacy playlist; multipart/mixed. |
| Nữ Chiến Binh | 2020 | completed | unknown | [`PLC_d5n_vB0CpiGXxipKjNENU8hkenUgOO`](https://www.youtube.com/playlist?list=PLC_d5n_vB0CpiGXxipKjNENU8hkenUgOO) | Official but not proven main-only. |
| Bước Chân Thần Tốc | 2022 | completed | unknown | [`PLC_d5n_vB0CqKPJB_nKNGC5usu-epusl-`](https://www.youtube.com/playlist?list=PLC_d5n_vB0CqKPJB_nKNGC5usu-epusl-) | Official season playlist. |
| Những Chiến Binh Của Biển | 2023 | completed | unknown | [`PLC_d5n_vB0CriKOGYS3OtwqdTUYU8Ex1-`](https://www.youtube.com/playlist?list=PLC_d5n_vB0CriKOGYS3OtwqdTUYU8Ex1-) | Official season playlist. |
| Không Khoan Nhượng | 2024 | completed | unknown | [`PLC_d5n_vB0Cr41NjQr7k08taDRxmj_jUG`](https://www.youtube.com/playlist?list=PLC_d5n_vB0Cr41NjQr7k08taDRxmj_jUG) | Male 2024 edition. |
| Gót Hồng Trên Lửa Đạn | 2024 | completed | unknown | [`PLC_d5n_vB0CoI8qgSX7mPMpAC_nlcbf57`](https://www.youtube.com/playlist?list=PLC_d5n_vB0CoI8qgSX7mPMpAC_nlcbf57) | Separate female 2024 edition; do not merge with *Không Khoan Nhượng*. |
| Khi Tổ Quốc Gọi Tên | 2025 | completed | 16 | [`PLC_d5n_vB0Cq3f_8Fj98GNIcl7l7tnjAp`](https://www.youtube.com/playlist?list=PLC_d5n_vB0Cq3f_8Fj98GNIcl7l7tnjAp) | Official 16-video numbered season; [official episode 2](https://www.youtube.com/watch?v=uTGqZJb8FYg) binds the edition. |
| 2026 edition | 2026 | airing | unknown | [`PLZuraW9kAXuE`](https://www.youtube.com/playlist?list=PLZuraW9kAXuE) | Official current playlist, but its 40 items are mixed/current and cannot be treated as 40 main episodes. |

**Source gaps:** no separate 2021 full season surface was verified; exact logical episode counts for 2017-2024 remain unresolved; the 2026 final count is not yet source-bound.

## 5. Chiến Sĩ Quả Cảm

`format_type: closed_season`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---:|---|---:|---|---|
| Mùa 1 | 2025 | completed | 15 | [`PLCgARQSDdGSz-rFWvFVciI3bvFFHhaD82`](https://www.youtube.com/playlist?list=PLCgARQSDdGSz-rFWvFVciI3bvFFHhaD82) | Clean official 1-15 playlist. The [official episode 15 finale](https://www.youtube.com/watch?v=erm2i198E44) describes the close of the first season. |

No first-party Mùa 2 announcement or numbered Mùa 2 episode was verified. Later official highlight compilations using `#CSQC` are not evidence of a new season.

## 6. Đấu Trường Gia Tốc

`format_type: closed_season`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---:|---|---:|---|---|
| Mùa 1 | 2025 | completed | 12 | [`PLy_TpcUT2LZtKjiN00baVxhHVN1HthDiQ`](https://www.youtube.com/playlist?list=PLy_TpcUT2LZtKjiN00baVxhHVN1HthDiQ) | Official playlist has 13 items: episodes 1-12 plus one unrelated *Say Hi Rực Rỡ* item. HTV's [first-party launch page](https://htv.vn/dau-truong-gia-toc-20g30-ngay-17-8-2025-tren-htv7-222250815124838904.htm) binds the show and broadcast. |

No first-party Mùa 2 was verified.

## 7. Tổ Đội 1 Không 2

`format_type: closed_season`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---:|---|---:|---|---|
| Mùa 1 | 2025 | completed | 12 | [`PLy_TpcUT2LZuLuV_ZdXi-Q84PGwjQ2GR3`](https://www.youtube.com/playlist?list=PLy_TpcUT2LZuLuV_ZdXi-Q84PGwjQ2GR3) | Official playlist has 14 items: episodes 1-12, a recap, and unrelated contamination. [Official episode 1](https://www.youtube.com/watch?v=_7DygDmrWbU) binds the publisher; the [HTV program hub](https://www.htv.com.vn/to-doi-1-khong-2) reaches episode 12 and calls this the first season. |

No first-party Mùa 2 was verified.

## 8. Bậc Thầy Săn Thưởng

`format_type: closed_season`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---|---|---:|---|---|
| Mùa 1 | 2024-2025 | completed | 21 | [`PLC_d5n_vB0CrecgNHLjt6kxEMlZDeBqp5`](https://www.youtube.com/playlist?list=PLC_d5n_vB0CrecgNHLjt6kxEMlZDeBqp5) | Official Viettel Media playlist is mixed (53 items), not main-only. The [HTV program hub](https://www.htv.com.vn/bac-thay-san-thuong) and [official video ledger](https://htv.vn/bac-thay-san-thuong/video.htm) establish the numbered run through episode 21. |

No first-party second season was verified.

## 9. Hành Trình Rực Rỡ

`format_type: closed_season`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---:|---|---:|---|---|
| Mùa 1 | 2023 | completed | 20 | [`PLy_TpcUT2LZtT4YxNqO277e2zk-7oUS_6`](https://www.youtube.com/playlist?list=PLy_TpcUT2LZtT4YxNqO277e2zk-7oUS_6) | Official playlist is mixed (32 items) but contains the 20 numbered main shows. VTV retains the [official episode 20 page](https://vtv.vn/video/hanh-trinh-ruc-ro-tap-20-644205.htm); an official archive upload such as [episode 19](https://www.youtube.com/watch?v=AkTrDpr8c8o) binds the legacy channel ID. |

No first-party second season was verified.

## 10. Về Quê Làm Giàu

`format_type: closed_season`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---:|---|---:|---|---|
| Mùa 1 | 2025 | completed | 15-numbered range | [`PLaHmC9pxzevpEDOuWCKZPWyWhLNCgZFLy`](https://www.youtube.com/playlist?list=PLaHmC9pxzevpEDOuWCKZPWyWhLNCgZFLy) | Official Halotimes playlist is heavily mixed (hundreds of shorts/highlights/trailers). Full main titles reach episode 15; the [official episode 12 trailer](https://www.youtube.com/watch?v=_fGoYb7rXcg) binds the channel. Episode 4 is hidden/unavailable in the visible playlist, so the range is source-bound but population is not complete. |

**Source gap:** no clean 15-item full-main playlist and no first-party second season were verified. Fail closed on episode 4 until an official surviving upload is found.

## 11. Bố Ơi! Mình Đi Đâu Thế?

`format_type: episodic_reality`

VTV confirms [four historical seasons and the 2025 return](https://vtv.vn/truyen-hinh/anh-tai-neko-le-trung-ruoi-duy-hung-gay-sot-khi-cung-con-tham-gia-bo-oi-minh-di-dau-the-2025051714342767.htm).

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / gap |
|---|---|---|---:|---|---|
| Mùa 1 | 2014-2015 | completed | unknown | **Gap** | Season identity is first-party; no complete official episode ledger/playlist was verified. |
| Mùa 2 | 2015-2016 | completed | unknown | **Gap** | First-party season identity verified; count and clean playlist unresolved. |
| Mùa 3 | 2016 | completed | 32 | **Gap** | VTV explicitly identifies [episode 32 as the final](https://vtv.vn/truyen-hinh/bo-oi-minh-di-dau-the-3-cac-be-dam-minh-trong-nhung-cau-chuyen-co-tich-cua-bo-20161210150802641.htm). |
| Mùa 4 | 2017-2018 | completed | unknown | **Gap** | VTV retains the [finale page](https://vtv.vn/truyen-hinh/bo-oi-minh-di-dau-the-tap-cuoi-khoanh-khac-chia-xa-dam-nuoc-mat-20180811141612342.htm), but the exact logical count was not stated cleanly enough to bind. |
| Mùa 5 | 2025 | completed | 15 | [`PLLg_kRqp4Dpq0Gd1snNkyj5FF7hFIpGku`](https://www.youtube.com/playlist?list=PLLg_kRqp4Dpq0Gd1snNkyj5FF7hFIpGku) | Official TV HUB sequence reaches [episode 15, the farewell/finale](https://www.youtube.com/watch?v=Uhe7UTfPxm8). The official episode-10 teaser also labels it [Mùa 5](https://www.youtube.com/watch?v=MRQGj91tucg). Treat the playlist as official discovery and filter teasers/clips. |

## 12. Biệt Đội Siêu Sao

`format_type: closed_season`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---|---|---:|---|---|
| Mùa 1 | 2024-2025 | completed | 13 | [`PLJSRfYQoW3dn5wLuH9xgrMbaazxZdZBZ_`](https://www.youtube.com/playlist?list=PLJSRfYQoW3dn5wLuH9xgrMbaazxZdZBZ_) | The [official HTV episode 13](https://www.youtube.com/watch?v=zNY5kLHWze8) directly exposes this 44-item official playlist. It is mixed; use only full episodes 1-13. The [HTV program hub](https://www.htv.com.vn/biet-doi-sieu-sao) independently reaches episode 13. |

No first-party second season was verified.

## 13. La Cà Hát Ca

`format_type: closed_season`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---:|---|---:|---|---|
| Mùa 1 | 2023 | completed | 13 | [`PLJSRfYQoW3dmvVTD69QV9X8wpEgxGFfca`](https://www.youtube.com/playlist?list=PLJSRfYQoW3dmvVTD69QV9X8wpEgxGFfca) | HTV's [official episode 13](https://www.youtube.com/watch?v=CdY7trxkhjY) closes the numbered run and its first-party “Full Playlist” shortlink resolves to this ID. A former Dong Tay Promotion finale upload is now private, so HTV is the surviving canonical source. |

No first-party second season was verified.

## 14. Mẹ Vắng Nhà, Ba Là Siêu Nhân

`format_type: episodic_reality`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / gap |
|---|---:|---|---:|---|---|
| Mùa 1 | 2022 | completed | unknown | **Gap — no clean full-main playlist verified** | Official channel archive establishes the edition; logical count remains unresolved. |
| Mùa 2 | 2023 | completed | unknown | **Gap — no clean full-main playlist verified** | Official channel archive establishes the edition; logical count remains unresolved. |
| Mùa 3 | 2024 | completed | unknown | **Gap — no clean full-main playlist verified** | Official channel archive and HTV mirrors establish the edition. |
| Mùa 4 | 2025 | completed | unknown | **Gap — no clean full-main playlist verified** | The [HTV Mùa 4 hub](https://www.htv.com.vn/me-vang-nha-ba-la-sieu-nhan) and first-party program archive establish the edition. |
| Mùa 5 / 2026 | 2026 | completed | 18 | **Gap — channel has many family/segment playlists, no clean 18-item main-only playlist verified** | The [official trailer](https://www.youtube.com/watch?v=NxQuB7BvDRQ) announces the 2026 run. The official sequence begins at [episode 1](https://www.youtube.com/watch?v=bjKBuI8JXRk) and ends with [episode 18, the families welcoming the mothers home](https://www.youtube.com/watch?v=R1RSoQSHwoY), published five days before the cutoff. |

Population rule: prefer the numbered full/uncut program that combines the participating families; family-only cuts, “ngày thứ N” compilations, shorts, and “không lên sóng” playlists are derivatives.

## 15. Mái Ấm Gia Đình Việt

`format_type: rolling_weekly`

| Run | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---|---|---:|---|---|
| Continuous run | 2022-present | airing | open-ended; episodes 1-197 published by cutoff | [`PLDNVHSVr-vVkKKgcJr--k4Dtplx8TwHmW`](https://www.youtube.com/playlist?list=PLDNVHSVr-vVkKKgcJr--k4Dtplx8TwHmW) — current Bee Comm full-show playlist; [`PLJSRfYQoW3dlOYbVEqJVpg_8NGG8Xpd4L`](https://www.youtube.com/playlist?list=PLJSRfYQoW3dlOYbVEqJVpg_8NGG8Xpd4L) — older HTV playlist | The official program site lists the continuous weekly ledger through [episode 197](https://maiamgiadinhviet.vn/) and states the HTV7/Bee Comm weekly schedule. The older HTV playlist stops at 119 items; use it only as legacy discovery. Bee Comm's [official episode 184 page](https://www.youtube.com/watch?v=8bXTcPkA-5o) directly links the current full-show playlist and resolves channel ID `UClOMHp76zB3wHcKGYxTRWFA`. |

Do not create artificial seasons or reset numbering by calendar year. Missing dates/pauses do not close the run.

## 16. Anh Trai & Cái Đuôi Nhỏ

`format_type: closed_season`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---:|---|---:|---|---|
| Mùa 1 | 2026 | completed | 12 | [`PLy_TpcUT2LZvcJAmF_eYxx195KpRGmzrB`](https://www.youtube.com/playlist?list=PLy_TpcUT2LZvcJAmF_eYxx195KpRGmzrB) | The official playlist contains numbered full episodes 1-12. [Official episode 12](https://www.youtube.com/watch?v=FuAYbk9j0h0) is the graduation/farewell program; [episode 1](https://www.youtube.com/watch?v=KRef2BML-wc) binds the sequence and publisher. |

No first-party second season was verified by the cutoff.

## 17. Xuân Hạ Thu Đông, Rồi Lại Xuân

`format_type: episodic_reality`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---|---|---:|---|---|
| Mùa 1 | 2021 | completed | 11 | [`PLxNMBnO9F8FNxpfidsVyxNffOg_VhLOOa`](https://www.youtube.com/playlist?list=PLxNMBnO9F8FNxpfidsVyxNffOg_VhLOOa) | Clean official 11-video full-episode playlist; [official episode 1](https://www.youtube.com/watch?v=3Ap8mrCUyOA) binds the channel. |
| Mùa 2 | 2022 | completed | unknown | [`PLxNMBnO9F8FNbuRLhE0V1dYdSqFfA129g`](https://www.youtube.com/playlist?list=PLxNMBnO9F8FNbuRLhE0V1dYdSqFfA129g); alternate full-show surface [`PLxNMBnO9F8FOmUuA6DZDZZTeGbOKnR5i7`](https://www.youtube.com/playlist?list=PLxNMBnO9F8FOmUuA6DZDZZTeGbOKnR5i7) | The 14-item playlist includes opening/related material, so 14 is not admitted as a main count without item classification. |
| Mùa 3 — Street's Harmony | 2024-2025 | completed | 18 | [`PLxNMBnO9F8FMtG4_3bKxsshIs4cpaii3F`](https://www.youtube.com/playlist?list=PLxNMBnO9F8FMtG4_3bKxsshIs4cpaii3F) | Official “FULL các tập” playlist contains 18 full episodes; HTV reported the [Mùa 3 close](https://www.youtube.com/watch?v=jb9CtuR_gu4). |

## 18. Điều Ước Của Mẹ

`format_type: episodic_reality`

| Edition | Year | Status | expected_main_count | Exact official playlist | Evidence / scope |
|---|---|---|---:|---|---|
| Mùa 1 | 2025-2026 | completed | 22 | **Gap — no official YouTube channel ID or clean playlist verified** | The [official program ledger](https://dieuuoccuame.vn/video/tap-phat-song/) runs from episode 1 to episode 22, titled as a look back over the journey. |
| Mùa 2 — Hành Trình Tỏa Sắc Cùng Điều Ước Của Mẹ | 2026 | airing | 21 planned main broadcasts | **Gap — no official YouTube channel ID or clean playlist verified** | The [official site](https://dieuuoccuame.vn/) explicitly says Mùa 2 has 21 broadcasts, two stories each, weekly on HTV9. It continues the public main numbering at episode 23; site news had reached [episode 32](https://dieuuoccuame.vn/tap-32-dam-nuoc-mat-bat-luc-canh-cu-ong-80-tuoi-vat-kiet-suc-tan-va-co-be-9-tuoi-chap-nhan-nghi-hoc-de-me-duoc-song/) by 2026-07-27. |

The site also exposes a separately numbered four-part *Hành Trình Tỏa Sắc* companion sequence. Do not silently count those four cards as main episodes or assume Mùa 2 episode 1-4; retain them as companion assets until first-party video-level reconciliation proves otherwise. If the stated 21-program plan is delivered with continuous global numbering, the expected endpoint would be 43, but `43` is an inference and must not be stored as a delivered count yet.

## 19. Sóng

`format_type: annual_special`

Each year is one Tết annual edition, not a multi-episode season. Official playlists commonly split a single broadcast into performances and segments, so raw playlist item counts are not episode counts.

| Edition | Year | Status | expected_main_count | Exact official playlist(s) | Evidence / gap |
|---|---:|---|---:|---|---|
| Sóng 18 | 2018 | completed | 1 annual edition | [`PLxKLMN7WdG5BOtJOsSKTjxXWD_LVCYPYd`](https://www.youtube.com/playlist?list=PLxKLMN7WdG5BOtJOsSKTjxXWD_LVCYPYd) | Official “trọn bộ” playlist; [official full program](https://www.youtube.com/watch?v=N35K-SRhZQ4). |
| Sóng 19 | 2019 | completed | 1 annual edition | **Gap — exact official annual playlist not verified** | Edition is present in the official Vie archive, but no clean annual playlist ID was source-bound. |
| Sóng 20 | 2020 | completed | 1 annual edition | [`PLxKLMN7WdG5DWTxwel5hsaLSOlpzgayQ5`](https://www.youtube.com/playlist?list=PLxKLMN7WdG5DWTxwel5hsaLSOlpzgayQ5) | Official Sóng VieON / night-music playlist; segment-level filtering required. |
| Sóng 21 | 2021 | completed | 1 annual edition | **Gap — exact official annual playlist not verified** | Official edition identity verified; playlist gap retained. |
| Sóng 22 | 2022 | completed | 1 annual edition | **Gap — exact official annual playlist not verified** | Official edition identity verified; playlist gap retained. |
| Sóng 23 | 2023 | completed | 1 annual edition | [`PLxKLMN7WdG5Ddu4T4qbzgUbixCkeS_A5y`](https://www.youtube.com/playlist?list=PLxKLMN7WdG5Ddu4T4qbzgUbixCkeS_A5y) | Official main-channel edition playlist. |
| Sóng 24 | 2024 | completed | 1 annual edition | [`PLxKLMN7WdG5DgQQKKUMdu2_ZOgfoSMPT7`](https://www.youtube.com/playlist?list=PLxKLMN7WdG5DgQQKKUMdu2_ZOgfoSMPT7) | Official main-channel edition playlist. |
| Sóng 25 | 2025 | completed | 1 annual edition | [`PLxKLMN7WdG5BIwNQgqYSWciQhg-Jtj8yQ`](https://www.youtube.com/playlist?list=PLxKLMN7WdG5BIwNQgqYSWciQhg-Jtj8yQ) live stages; [`PLxKLMN7WdG5BbaNOm4v30QD5EQld9-roU`](https://www.youtube.com/playlist?list=PLxKLMN7WdG5BbaNOm4v30QD5EQld9-roU) concert | Both are official but neither was proven to be a clean single full-broadcast playlist. Music-channel mirrors are `PL0br2ZOewY7hV1CW_ljh5TEYHj9YTd31V` and `PL0br2ZOewY7jUXOknYlsJQiaI2qntp83I`. |
| Sóng 26 | 2026 | completed | 1 annual edition | [`PLxKLMN7WdG5CjEObleDT2wm09IizUC5I6`](https://www.youtube.com/playlist?list=PLxKLMN7WdG5CjEObleDT2wm09IizUC5I6); music mirror [`PL0br2ZOewY7g2D1TrNu3wnCJIaYGizuZp`](https://www.youtube.com/playlist?list=PL0br2ZOewY7g2D1TrNu3wnCJIaYGizuZp) | Official 2026 main-show and music mirror surfaces; deduplicate logical segments. |

## Population readiness and fail-closed gaps

| Program | Ready unit | Required fail-closed action |
|---|---|---|
| 2 Ngày 1 Đêm | Four editions, 97 global episodes | Filter known extras/contamination and preserve global numbering. |
| Running Man Vietnam | Mùa 1-3 complete; 2026 run airing | Keep 2026 reset separate; wait for a season playlist/final count. |
| Gia Đình Haha | Mùa 1 complete; Mùa 2 upcoming | Include 16-20 as the source-bound special continuation; do not ingest the unrelated Tân Binh playlist. |
| Sao Nhập Ngũ | Edition universe source-bound | Legacy logical counts and 2026 final count remain unresolved; classify multipart/mixed playlists before population. |
| Chiến Sĩ Quả Cảm | Mùa 1 complete | Do not infer Mùa 2 from later highlight uploads. |
| Đấu Trường Gia Tốc | Mùa 1 complete | Exclude one unrelated playlist item. |
| Tổ Đội 1 Không 2 | Mùa 1 complete | Exclude recap and unrelated item. |
| Bậc Thầy Săn Thưởng | Mùa 1 count source-bound | Filter 53-item mixed playlist to 21 logical main episodes. |
| Hành Trình Rực Rỡ | Mùa 1 complete | Filter uncut/extras and retain 20 logical episodes. |
| Về Quê Làm Giàu | 1-15 range source-bound | Episode 4 is unavailable; do not declare complete population. |
| Bố Ơi! Mình Đi Đâu Thế? | Five seasons identified | Mùa 1, 2, and 4 counts/playlists remain gaps. |
| Biệt Đội Siêu Sao | Mùa 1 complete | Filter 44-item official playlist to episodes 1-13. |
| La Cà Hát Ca | Mùa 1 complete | Use surviving HTV mirror; former DTP finale is private. |
| Mẹ Vắng Nhà, Ba Là Siêu Nhân | Five seasons identified; Mùa 5 count bound | Reconstruct Mùa 1-4 counts; classify family-only and off-air derivatives. |
| Mái Ấm Gia Đình Việt | Continuous run through 197 | Treat as rolling weekly; merge legacy/current publisher provenance without resetting episode numbers. |
| Anh Trai & Cái Đuôi Nhỏ | Mùa 1 complete | Populate 12 numbered full episodes only. |
| Xuân Hạ Thu Đông Rồi Lại Xuân | Three seasons identified | Mùa 2 logical main count requires classification. |
| Điều Ước Của Mẹ | Mùa 1 complete; Mùa 2 airing | Do not mix global main numbering with the four-part companion series; YouTube authority remains unresolved. |
| Sóng | Annual editions 18-26 | Treat each year as one annual special and segment playlists beneath it; gaps remain for 19, 21, and 22. |

## Canonical ingestion tests

1. **Authority:** the uploader channel ID or first-party site must match this registry.
2. **Edition binding:** title, description, playlist, or broadcaster ledger must bind the item to the exact season/edition.
3. **Main-show class:** accept a complete numbered episode or source-bound annual full show; reject trailers, previews, shorts, highlights, reactions, recaps, uncut alternates, family-only cuts, concerts, performances, and behind-the-scenes items unless explicitly modeled as non-main assets.
4. **Logical identity:** deduplicate official mirrors by program + season/edition + logical episode number; retain alternate video IDs as provenance.
5. **Count discipline:** never equate playlist item count with main episode count until every item is classified.
6. **Completeness:** unresolved or unavailable members remain explicit gaps. No season is marked fully populated merely because the highest observed episode matches an expected endpoint.
