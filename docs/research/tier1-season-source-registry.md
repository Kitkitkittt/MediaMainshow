# Tier 1 season source registry

Research cutoff: **2026-08-12 (Asia/Saigon)**  
Scope: `ATSH`, `EXSH`, `THSH`, `ATVNCG`, and `CDDG`  
Source rule: official YouTube channel/playlist/video pages and first-party broadcaster/producer pages only.

## Decision summary

The verified Tier 1 universe contains **eight seasons/editions**:

| season_id | show | broadcast year | status at cutoff | source-bound main episode count | canonical YouTube source |
|---|---|---:|---|---:|---|
| `ATSH_2024` | Anh Trai "Say Hi" | 2024 | completed | 14 | official show-hub playlist; numbered full-episode block |
| `ATSH_2025` | Anh Trai "Say Hi" season 2 | 2025 | completed | 14 | official show-hub playlist; numbered full-episode block |
| `EXSH_2025` | Em Xinh "Say Hi" | 2025 | completed | 14 | official show-hub playlist; numbered full-episode block |
| `THSH_2026` | Tinh Hà "Say Hi" | 2026 | airing | 14 planned; episode 6 observed | **no official full-main-show playlist located** |
| `ATVNCG_2024` | Anh Trai Vượt Ngàn Chông Gai | 2024 | completed | 15 | official full-main-show playlist |
| `ATVNCG_2026` | Anh Trai Vượt Ngàn Chông Gai | 2026 | airing | 15 planned; episode 6 observed | two official playlists mirror the same full episodes |
| `CDDG_2023` | Chị Đẹp Đạp Gió Rẽ Sóng | 2023 | completed | 15 | official full-main-show playlist |
| `CDDG_2024` | Chị Đẹp Đạp Gió | 2024 | completed | 15 | official full-main-show playlist |

No official first-party announcement or numbered full episode was found for an additional `ATSH`, `EXSH`, `CDDG`, or `ATVNCG` season through the cutoff. This is an **evidence-gap statement**, not proof that a future season will not be commissioned.

## Canonical channel registry

| owner/use | official channel | channel ID | canonical-use decision |
|---|---|---|---|
| Vie Channel / full `Say Hi` episodes | [Vie Channel](https://www.youtube.com/channel/UCkna2OcuN1E6u5I8GVtdkOw) | `UCkna2OcuN1E6u5I8GVtdkOw` | Accept numbered, long-form main-show uploads for `ATSH`, `EXSH`, and `THSH`. |
| Vie Channel - MUSIC / performance cuts | [Vie Channel - MUSIC](https://www.youtube.com/channel/UC2fu6CiFfNYz5UFORvFyc0w) | `UC2fu6CiFfNYz5UFORvFyc0w` | Official, but **not** canonical for the full-episode metric. |
| YEAH1 SHOW / full episodes | [YEAH1 SHOW](https://www.youtube.com/channel/UCh_zF2FsiCflCPgYDudtcqg) | `UCh_zF2FsiCflCPgYDudtcqg` | Accept numbered, long-form main-show uploads for `ATVNCG` and `CDDG`. |

Channel ownership is stated by the channels themselves: Vie Channel describes itself as the official home for `Tinh Hà`, `Anh Trai`, and `Em Xinh`; YEAH1 SHOW describes itself as YeaH1 Digital's official YouTube channel. The individual episode descriptions additionally identify Vie Channel/DatVietVAC or YeaH1 as the producing/rightsholding parties.

## Season evidence

### `ATSH` — Anh Trai "Say Hi"

#### `ATSH_2024`

- **Status:** completed.
- **Broadcast year:** 2024.
- **Expected main episodes:** 14. VieON labels the season `14/14 tập` and enumerates `Tập 1` through `Tập 14`; its separate finale award stream does not create episode 15. Source: [VieON — Anh Trai Say Hi 2024](https://vieon.vn/anh-trai-say-hi.html).
- **Official full-show source:** [YouTube playlist](https://www.youtube.com/playlist?list=PLxKLMN7WdG5AYDsDPTbq7zZTpOTGH7ay6), ID `PLxKLMN7WdG5AYDsDPTbq7zZTpOTGH7ay6`, on Vie Channel.
- **Playlist class:** official show hub. It begins with the 14 numbered long-form episodes but continues with BTS/short-form material. Ingestion must keep only `Tập 1`–`Tập 14` that pass the full-main-show classifier.
- **Completion evidence:** VieON's `14/14` catalogue and the official playlist's `Tập 14: Đêm Chung Kết - Công Bố & Trao Giải`.

#### `ATSH_2025`

- **Status:** completed.
- **Broadcast year:** 2025; VieON identifies it as season 2 and gives a 20 September 2025 launch.
- **Expected main episodes:** 14. VieON labels the season `14/14 tập`; `Tập 14` is presented in two programme parts (`Đêm Chung Kết` and `Công Bố và Trao Giải`) but remains one logical episode number. Source: [VieON — Anh Trai Say Hi 2025](https://vieon.vn/anh-trai-say-hi-2025.html).
- **Official full-show source:** [YouTube playlist](https://www.youtube.com/playlist?list=PLxKLMN7WdG5BScv1MASDarMh12mB8tIU2), ID `PLxKLMN7WdG5BScv1MASDarMh12mB8tIU2`, on Vie Channel.
- **Playlist class:** official show hub, not a performance-only list. Apply the numbered full-episode filter because the hub may also contain related material.

**ATSH performance exclusion:** [playlist `PL0br2ZOewY7jy7aP-8z_szE2rsy0pYiK4`](https://www.youtube.com/playlist?list=PL0br2ZOewY7jy7aP-8z_szE2rsy0pYiK4) is explicitly titled `Anh Trai "Say Hi" [PERFORMANCE]`; it belongs to Vie Channel - MUSIC and must not populate canonical episodes. Concert catalogues are also separate event objects, not additional seasons.

### `EXSH` — Em Xinh "Say Hi"

#### `EXSH_2025`

- **Status:** completed. DatVietVAC reports the live finale/awards on 23 August 2025 and describes all 14 instalments. Sources: [DatVietVAC launch](https://datvietvac.vn/news/em-xinh-say-hi-hien-tuong-am-nhac-moi-cua-mua-he-2025-chinh-thuc-ra-mat), [DatVietVAC finale](https://datvietvac.vn/news/pho-giam-doc-so-vhtt-thanh-thuy-xuc-dong-o-chung-ket-em-xinh-say-hi).
- **Broadcast year:** 2025.
- **Expected main episodes:** 14. VieON labels the season `14/14 tập`, with `Tập 14` split into finale and award-programme parts under one logical episode number. Source: [VieON — Em Xinh Say Hi](https://vieon.vn/em-xinh-say-hi.html).
- **Official full-show source:** [YouTube playlist](https://www.youtube.com/playlist?list=PLxKLMN7WdG5D1LrbMdeJMn_fL9FrQbJ6V), ID `PLxKLMN7WdG5D1LrbMdeJMn_fL9FrQbJ6V`, on Vie Channel.
- **Playlist class:** official show hub. The top numbered block contains `Tập 1`–`Tập 14`; subsequent highlights, BTS, uncut, and shorts are not canonical episodes.

**EXSH performance exclusion:** [playlist `PL0br2ZOewY7j1sDGZtYTE88r3SIZJGBCu`](https://www.youtube.com/playlist?list=PL0br2ZOewY7j1sDGZtYTE88r3SIZJGBCu) is explicitly titled `Em Xinh "Say Hi" [PERFORMANCE]` on Vie Channel - MUSIC. It is an official music/performance projection, not a full-main-show source. Concert footage likewise remains outside the season registry.

### `THSH` — Tinh Hà "Say Hi"

#### `THSH_2026`

- **Status:** airing at the cutoff, not announced-only. DatVietVAC states that the series began broadcasting at 20:00 Saturdays from 4 July 2026 on HTV2 - Vie Channel, ON - Vie Entertainment, YouTube Vie Channel, and VieON. Source: [DatVietVAC launch record](https://datvietvac.vn/en/news/24-artists-of-the-say-hi-galaxy-group-officially-debut-to-the-audience-1).
- **Broadcast year:** 2026.
- **Expected main episodes:** 14 planned. VieON labels the title `Tinh Hà Say Hi - 14 Tập`; because the season is still airing, use this as the planned order rather than a completed count. Source: [VieON — Tinh Hà Say Hi](https://vieon.vn/tinh-ha-say-hi.html).
- **Current observed main episode:** `Tập 6` was present on the official channel by the cutoff: [official episode 6](https://www.youtube.com/watch?v=0mQn-pPDLuM).
- **Official full-show playlist:** **not located.** The official channel's playlist shelf exposed Live Stage and Dance Practice lists but no numbered full-main-show playlist. Until one appears, discovery must be bounded to the official Vie Channel ID and require the exact title pattern `TINH HÀ SAY HI TẬP n` plus long-form/full-show checks.

**THSH performance exclusions:** [Live Stage playlist `PLJmLkEeTGhVc`](https://www.youtube.com/playlist?list=PLJmLkEeTGhVc) and [Dance Practice playlist `PLLroHtYhpFt8`](https://www.youtube.com/playlist?list=PLLroHtYhpFt8) are official but are not main episodes. Their existence does not close the missing-full-playlist gap.

### `ATVNCG` — Anh Trai Vượt Ngàn Chông Gai

#### `ATVNCG_2024`

- **Status:** completed.
- **Broadcast year:** 2024; the official episode descriptions state a 29 June 2024 launch.
- **Expected main episodes:** 15. The official final upload calls `Tập 15` the last episode and says the nearly four-month journey closes there. Source: [official episode 15](https://www.youtube.com/watch?v=8NbKhGsnJyI).
- **Official full-show source:** [YouTube playlist](https://www.youtube.com/playlist?list=PLt3LgMEKzFxy03fvdFk_rEtjfVJfD8pUq), ID `PLt3LgMEKzFxy03fvdFk_rEtjfVJfD8pUq`, on YEAH1 SHOW. The final episode's official description labels this link `Xem trọn playlist (2024)`.
- **Playlist class:** full numbered main show. Keep `Tập 1`–`Tập 15`; performance compilations and eight concert nights mentioned by YEAH1 SHOW are separate products, not seasons or logical episodes.

#### `ATVNCG_2026`

- **Status:** airing at the cutoff. The official playlist contained numbered full episodes through `Tập 6`.
- **Broadcast year:** 2026; first episode aired 27 June 2026.
- **Expected main episodes:** 15 planned. YeaH1's project release states `Số tập: 15 tập` and the weekly VTV3/YEAH1 SHOW schedule. Source: [YeaH1 project announcement](https://www.yeah1group.com/tap-doan-yeah1-chinh-thuc-cong-bo-khoi-dong-du-an-chien-luoc-anh-trai-vuot-ngan-chong-gai-2026).
- **Official full-show sources:**
  - preferred chronological playlist: [ID `PLdWk-MlnCC7M`](https://www.youtube.com/playlist?list=PLdWk-MlnCC7M), titled `CHƯƠNG TRÌNH ANH TRAI VƯỢT NGÀN CHÔNG GAI 2026`;
  - official mirror: [ID `PLWaGid9TiMXE`](https://www.youtube.com/playlist?list=PLWaGid9TiMXE), titled `ANH TRAI VƯỢT NGÀN CHÔNG GAI 2026 [K26]`.
- **Duplicate-source rule:** both playlists expose the same numbered episode video IDs in different ordering. Merge by `video_id`; do not interpret the mirror as another season.

**ATVNCG performance/concert exclusions:** [Performance playlist `PLVUnLNjswtwk`](https://www.youtube.com/playlist?list=PLVUnLNjswtwk), [Focus Cam playlist `PLbce4FUxuhqo`](https://www.youtube.com/playlist?list=PLbce4FUxuhqo), and all playlists labelled `CONCERT` are official ancillary catalogues, not full episodes or additional seasons.

### `CDDG` — Chị Đẹp Đạp Gió

#### `CDDG_2023`

- **Status:** completed.
- **Broadcast year:** 2023.
- **Expected main episodes:** 15. The official final upload is numbered `Tập 15`, describes itself as the finale/awards programme, and says it closes the first season. Source: [official episode 15](https://www.youtube.com/watch?v=Xh35QRR97Y4).
- **Official full-show source:** [YouTube playlist](https://www.youtube.com/playlist?list=PLt3LgMEKzFxxvhzWqiZPdQsr84wrtmK1A), ID `PLt3LgMEKzFxxvhzWqiZPdQsr84wrtmK1A`, titled `Show CHỊ ĐẸP ĐẠP GIÓ RẼ SÓNG 2023 | Bản Quyền thuộc sở hữu của YeaH1`.
- **Playlist class:** full numbered main show; keep `Tập 1`–`Tập 15` only.

#### `CDDG_2024`

- **Status:** completed.
- **Broadcast year:** 2024 (the weekly run began 26 October 2024 and concluded with numbered episode 15).
- **Expected main episodes:** 15. Source: [official episode 15](https://www.youtube.com/watch?v=GC0PYg7k9wk).
- **Official full-show source:** [YouTube playlist](https://www.youtube.com/playlist?list=PLt3LgMEKzFxz2EslvirjbydcPyz_MZErF), ID `PLt3LgMEKzFxz2EslvirjbydcPyz_MZErF`, titled `Show CHỊ ĐẸP ĐẠP GIÓ 2024 | Bản Quyền thuộc sở hữu của YeaH1`.
- **Playlist class:** full numbered main show; keep `Tập 1`–`Tập 15` only.

**CDDG performance/concert exclusions:** official playlists labelled `FOCUS CAM`, `BEST CUT`, `REACTION`, `Sân Khấu`/performance, and `Concert Chị Đẹp` are ancillary catalogues. For example, [Focus Cam `PLt3LgMEKzFxz_F4eporRq1umfddKC4xmm`](https://www.youtube.com/playlist?list=PLt3LgMEKzFxz_F4eporRq1umfddKC4xmm) and [Concert `PLt3LgMEKzFxx26rq30jWl3wYUtqk5G3AJ`](https://www.youtube.com/playlist?list=PLt3LgMEKzFxx26rq30jWl3wYUtqk5G3AJ) must not enter the canonical episode registry.

## Population rules derived from the evidence

1. Register all eight seasons above. Add `ATVNCG_2026`; correct `THSH_2026` to `airing`.
2. Use counts of 14 for all three completed Vie `Say Hi` seasons (`ATSH_2024`, `ATSH_2025`, `EXSH_2025`), 15 for completed `ATVNCG_2024`, `CDDG_2023`, and `CDDG_2024`, and planned counts of 14/15 for the two airing 2026 seasons.
3. A split finale/awards broadcast sharing one numbered episode remains one logical episode unless the product explicitly numbers the second part separately.
4. For `THSH_2026`, cache official-channel search/discovery receipts until Vie Channel publishes a dedicated full-main-show playlist. Do not substitute Live Stage or Dance Practice playlists.
5. Treat `ATVNCG_2026` playlist IDs as mirrors and deduplicate their identical uploads by `video_id`.
6. Never infer a new season from concerts, concert days, movies, focus cams, performances, dance practices, BTS, uncut, reactions, or best-cut packages.
7. Airing-season totals must be labelled `views_to_date` and refreshed against only the canonical numbered episode IDs.

## Evidence gaps and recheck triggers

- **`THSH_2026` full-main-show playlist:** absent from the official playlist shelf at cutoff. Recheck the official channel before each scheduled refresh.
- **Future seasons:** no first-party confirmation found for `ATSH_2026`, `EXSH_2026`, `CDDG_2025/2026`, or `ATVNCG_2025`. Keep them out of the population registry unless an official producer/broadcaster announcement or numbered full episode appears.
- **Airing-season final counts:** the 14 (`THSH`) and 15 (`ATVNCG`) figures are producer/broadcaster-planned orders, not proof that every episode has aired. Completion requires the numbered finale and a closed official catalogue.

