# Tier 2 season source registry

**Evidence cutoff:** 2026-08-12  
**Scope:** Rap Việt; The Masked Singer Vietnam / Ca Sĩ Mặt Nạ; Tân Binh Toàn Năng; Bài Hát Của Chúng Ta / Our Song Vietnam; Vietnam Idol; Nữ Hoàng Vũ Đạo Đường Phố.  
**Authority rule:** only first-party broadcaster/producer pages and official YouTube channel, playlist, or video pages are accepted below.

## Decision summary

The source-bound universe contains **17 completed broadcast seasons**: Rap Việt (4), The Masked Singer Vietnam (2), Tân Binh Toàn Năng (1), Our Song Vietnam (1), Vietnam Idol (8), and Nữ Hoàng Vũ Đạo Đường Phố (1). Tân Binh Toàn Năng also has a separate, completed **14-episode feeder phase** called *Giai Đoạn Sống Còn / Project 100%*. It must be retained for discovery, but must not be counted as a second season.

No first-party source reviewed by the cutoff established a newer season for any of the six formats. All rows are therefore `completed`; nothing in this registry supports an `announced`, `airing`, or `upcoming` row.

“Main episode” means a complete numbered broadcast episode or a named final that forms part of the competition sequence. It does **not** mean an individual performance, audio/lyric video, music compilation, reveal cut, highlight, recap, uncut/behind-the-scenes item, concert, press event, or isolated audition clip. A full episode may contain auditions; an isolated audition clip is still excluded.

## Official YouTube authorities

| Program / role | Official channel | Channel ID | Population use |
|---|---|---:|---|
| Rap Việt and The Masked Singer Vietnam, full shows | [Vie Channel](https://www.youtube.com/channel/UCkna2OcuN1E6u5I8GVtdkOw) | `UCkna2OcuN1E6u5I8GVtdkOw` | Include complete numbered shows and named finals only. |
| Rap Việt and The Masked Singer Vietnam, music | [Vie Channel MUSIC](https://www.youtube.com/channel/UC2fu6CiFfNYz5UFORvFyc0w) | `UC2fu6CiFfNYz5UFORvFyc0w` | Exclusion authority: performances, audio/lyric videos, and compilations are not main episodes. |
| Our Song Vietnam | [Dong Tay Promotion Official](https://www.youtube.com/channel/UCFMEYTv6N64hIL9FlQ_hxBw) | `UCFMEYTv6N64hIL9FlQ_hxBw` | Primary full-show publisher. |
| Tân Binh Toàn Năng feeder phase | [YEAH1 SHOW](https://www.youtube.com/channel/UCh_zF2FsiCflCPgYDudtcqg) | `UCh_zF2FsiCflCPgYDudtcqg` | `Project 100%` / survival-phase full episodes. |
| Tân Binh Toàn Năng main phase | [YeaH1 ONE](https://www.youtube.com/channel/UC_np0YZuvNMIJceE6jHeggQ) | `UC_np0YZuvNMIJceE6jHeggQ` | Main broadcast full episodes. |
| Vietnam Idol | [Vietnam Idol](https://www.youtube.com/channel/UCs0N0TBi2j156kZ4AOnnB2g) | `UCs0N0TBi2j156kZ4AOnnB2g` | Verified current official archive, principally 2023. Do not infer historical completeness. |
| Nữ Hoàng Vũ Đạo Đường Phố, producer | [Madison Media Group](https://www.youtube.com/channel/UCHNYJheRUSucT2rERYMn45A) | `UCHNYJheRUSucT2rERYMn45A` | Official original/full-episode publisher. |
| Nữ Hoàng Vũ Đạo Đường Phố, broadcaster | [HTV Entertainment](https://www.youtube.com/channel/UCbq8aOyj9ZtIqcD-0MwG1fQ) | `UCbq8aOyj9ZtIqcD-0MwG1fQ` | Official broadcast/catch-up publisher; contains duplicates and related clips. |

Channel ownership is source-bound by the linked official channel/video surfaces. A channel ID identifies an authority, not an instruction to ingest every video on that channel.

## 1. Rap Việt

First-party VieON exposes four seasons and no fifth season at the cutoff. All four are completed.

| Season | Year / completion | Status | Source-bound main count | Official full-main-show playlist | Evidence and classification |
|---|---|---|---:|---|---|
| Mùa 1 | 2020 | completed | 16 | **Gap — no clean official playlist ID verified** | [VieON season page](https://vieon.vn/rap-viet.html) reports `16/16` and exposes numbered episodes 1–16. Treat those 16 as the main sequence. Do not substitute performance compilations from Vie Channel MUSIC. |
| Mùa 2 | 2021–2022 | completed | 16 | **Gap — no clean official playlist ID verified** | [VieON season page](https://vieon.vn/rap-viet-mua-2.html) reports `16/16`; its catalog resolves episodes 1–14 followed by two final programs. Vie Channel also publishes the [official Tập 16 full show](https://www.youtube.com/watch?v=aZvGIa09Cd8). |
| Mùa 3 | 2023 | completed | 16 | [`PLxKLMN7WdG5DYy2yJiXnhMVnvNN1e31l7`](https://www.youtube.com/playlist?list=PLxKLMN7WdG5DYy2yJiXnhMVnvNN1e31l7) | [VieON season page](https://vieon.vn/rap-viet-mua-3.html) reports `16/16`; the official sequence ends at Vie Channel’s [Tập 16 full show](https://www.youtube.com/watch?v=QUsUGayd6IE). The linked playlist is the official season playlist titled for Rap Việt Mùa 3 (2023). |
| Mùa 4 | 2024 | completed | **16 VieON catalog entries; numbering requires QC** | **Gap — no clean official playlist ID verified** | [VieON season page](https://vieon.vn/rap-viet-mua-4.html) reports `16/16` and lists episodes 1–15 plus a named final/award program. Vie Channel’s final upload is titled [Tập 15: Đêm Chung Kết và Trao Giải](https://www.youtube.com/watch?v=cWcPlbQ6G9U). Therefore preserve the platform count of 16 entries, but do not assign a synthetic `episode_number=16` until video-ID/duration comparison proves the named final is distinct from the numbered Tập 15 entry. |

### Rap Việt population guardrails

- Mùa 3 is the only season for which this research verified an exact, official, season-level full-show playlist.
- For Mùa 1, Mùa 2, and Mùa 4, discovery must start from the official VieON catalog and exact full-show video titles on Vie Channel. Search-generated or fan playlists are not acceptable replacements.
- Individual rap performances, team compilations, casting/audition snippets, trailers, recaps, livestream preshows, and Vie Channel MUSIC uploads are derivative assets, not main episodes.
- Mùa 4 has a real catalog-versus-YouTube numbering conflict. The source registry should retain that conflict rather than silently choosing a count.

## 2. The Masked Singer Vietnam / Ca Sĩ Mặt Nạ

First-party VieON exposes two seasons and no third season at the cutoff.

| Season | Year | Status | Source-bound main count | Official full-main-show playlist | Evidence and classification |
|---|---:|---|---:|---|---|
| Mùa 1 | 2022 | completed | **16 numbered competition episodes, plus a separate award/reveal program** | **Gap — no clean official playlist ID verified** | [VieON season page](https://vieon.vn/ca-si-mat-na.html) has a `17/17` headline while its detailed catalog intermixes numbered episodes 1–16 with five “Tập đặc biệt” items, concert parts, and an award program. A first-party Vie-network video links the official [Tập 15](https://www.youtube.com/watch?v=Bgwawpq62Fg), [Tập 16](https://www.youtube.com/watch?v=pTVkxR_67-A), and [Đêm Công Bố & Trao Giải](https://www.youtube.com/watch?v=tKHS96W8lAQ). Canonicalize the 16 numbered episodes as the main sequence and store the award/reveal program as a special, not episode 17. |
| Mùa 2 | 2023 | completed | 16 numbered competition episodes; award/reveal separate | [`PLxKLMN7WdG5ANJruYBhSGi5UBRUIhQTbi`](https://www.youtube.com/playlist?list=PLxKLMN7WdG5ANJruYBhSGi5UBRUIhQTbi) | [VieON season page](https://vieon.vn/ca-si-mat-na-mua-2.html) reports `16/16` and exposes numbered episodes 1–16. Its additional “Lộ diện,” recap, and award-program entries are not numbered main episodes. The linked official playlist is titled for The Masked Singer Vietnam / Ca Sĩ Mặt Nạ Mùa 2 (2023). |

### The Masked Singer population guardrails

- The official Mùa 1 platform header and item list are not semantically clean. Use title class plus logical episode number, not raw page-card count.
- Concerts, “Tập đặc biệt,” individual reveal cuts, recaps, award/reveal programs, and Vie Channel MUSIC audio or lyric uploads are related programs, not main episodes. For example, Vie Channel MUSIC explicitly labels [this Mùa 2 item as an Audio Lyric release](https://www.youtube.com/watch?v=_21XPgbDPjo), even though its description references Tập 16.
- Only the Mùa 2 clean season playlist is verified. Mùa 1 must be reconstructed from official full-show links and deduplicated against specials.

## 3. Tân Binh Toàn Năng

The first-party program structure is **one 2025 season with two distribution phases**. The survival/feeder phase is not a second season.

| Registry unit | Year / completion | Status | Source-bound main count | Official playlist | Evidence and classification |
|---|---|---|---:|---|---|
| Feeder: *Giai Đoạn Sống Còn / Project 100%* | 2025 | completed | 14 | [`PLG0XT99Vqlcvdcn3cPc7XIIzBz2k9o0RX`](https://www.youtube.com/playlist?list=PLG0XT99Vqlcvdcn3cPc7XIIzBz2k9o0RX) | YEAH1 SHOW’s [Tập 14 full episode](https://www.youtube.com/watch?v=YbKOET_UdQg) closes the numbered feeder sequence and its first-party description distinguishes the survival route from the later main broadcast route. Retain `phase=feeder`; do not increment season count. |
| Main broadcast: *Tân Binh Toàn Năng 2025* | 2025–2026 | completed | 15 | [`PLkdwPUk2nejAsI3DcmBXdLg1dv1M0XhrL`](https://www.youtube.com/playlist?list=PLkdwPUk2nejAsI3DcmBXdLg1dv1M0XhrL) | YeaH1 ONE publishes the [Tập 15 finale](https://www.youtube.com/watch?v=KQQPuP-2Tgs). VTV’s first-party report says [Tập 15 was the final and describes the journey across 15 episodes](https://vtv.vn/nhom-nhac-tu-tan-binh-toan-nang-ra-mat-voi-7-thanh-vien-100260117202850691.htm); VTV separately confirms [the finale moved to 17 January 2026](https://vtv.vn/tan-binh-toan-nang-thay-doi-lich-phat-song-tap-cuoi-100251231214844649.htm). |

### Tân Binh Toàn Năng population guardrails

- Store one season and two phases. The producer’s SEO tags or text fragments such as `mua3` are not season authority.
- The feeder and main phases have different official channels and different episode-number ranges; preserve their phase identity rather than merging two “Tập 1” records.
- The official description also links a playlist labelled **Series Phái Sinh TÂN BINH TOÀN NĂNG** (`PLt3LgMEKzFxzJoCs9IE7LuiFrcB1P7V44`). Its own label makes it derivative; exclude it from full-main-show population.
- Performances, trainee diaries, practice clips, elimination snippets, and other spin-offs remain non-main even when linked from an official episode description.

## 4. Bài Hát Của Chúng Ta / Our Song Vietnam

| Season | Year | Status | Source-bound main count | Official full-main-show playlist | Evidence and classification |
|---|---:|---|---:|---|---|
| Mùa 1 | 2024 | completed | 14 | [`PLy_TpcUT2LZs0BkTqKYtAn61FZgtT3XwP`](https://www.youtube.com/playlist?list=PLy_TpcUT2LZs0BkTqKYtAn61FZgtT3XwP) | [VieON season page](https://vieon.vn/bai-hat-cua-chung-ta.html) says one season and `14/14`; VTV says [the program concluded after 14 episodes](https://vtv.vn/bai-hat-cua-chung-ta.html). Dong Tay Promotion’s official [Tập 14 finale](https://www.youtube.com/watch?v=nv-EC2OPtYw) directly links the complete season playlist. |

An early DatVietVAC announcement described [a planned 13-episode format](https://datvietvac.vn/news/our-song-viet-nam-chuong-trinh-am-nhac-thoi-thuong). That plan was superseded by the delivered 14-episode first-party catalog and finale. The production record should therefore use 14 and retain the 13 only as a planning-history note, not a competing expected count.

The separate VieON performance collection (78 music tracks at the cutoff), “Uncut” items, rehearsals, and individual song videos are not main episodes.

## 5. Vietnam Idol

VTV’s season numbering establishes eight completed seasons. The historical archive is materially less complete than the other Tier 2 programs: exact main-episode totals and clean official YouTube playlists for Mùa 1–7 were not established by the permitted sources. Those gaps are explicit and must not be filled from Wikipedia, fan channels, or inferred numbering.

| Season | Branded year / completion | Status | Source-bound main count | Official full-main-show playlist | First-party season evidence / gap |
|---|---|---|---:|---|---|
| Mùa 1 | 2007 | completed | **Unknown** | **Gap** | Historical first season in VTV’s eight-season sequence. No first-party complete episode ledger or clean official YouTube playlist was verified. |
| Mùa 2 | 2008 | completed | **Unknown** | **Gap** | VTV retains a first-party [Vietnam Idol 2008 topic archive](https://vtv.vn/vietnam-idol-2008.html). No complete main-episode ledger or playlist was verified. |
| Mùa 3 | 2010 | completed | **Unknown** | **Gap** | Historical third season in the broadcaster’s sequence. Available VTV articles describe stages and galas, but no complete source-bound main count or official full-show playlist was verified. |
| Mùa 4 | 2012 (finale 2013) | completed | **Unknown** | **Gap** | VTV explicitly calls [Vietnam Idol 2012 the fourth season](https://vtv.vn/van-hoa-giai-tri/vietnam-idol-2012-tap-1-vui-nhung-chua-nong-nhu-mong-doi-65388.htm). The complete episode count and official full-show playlist remain unresolved. |
| Mùa 5 | 2013 (finale 2014) | completed | **Unknown** | **Gap** | VTV’s finale report identifies it as [the fifth season](https://vtv.vn/truyen-hinh/chung-ket-vietnam-idol-2013-nhat-thuy-tro-thanh-than-tuong-am-nhac-viet-nam--139284.htm). The complete episode count and official full-show playlist remain unresolved. |
| Mùa 6 | 2015 | completed | **Unknown** | **Gap** | VTV identifies [Vietnam Idol 2015 as season six](https://vtv.vn/truyen-hinh/vietnam-idol-2015-chao-san-an-tuong-20150406065821298.htm). The complete episode count and official full-show playlist remain unresolved. |
| Mùa 7 | 2016 | completed | **Unknown** | **Gap** | VTV’s launch identifies [Vietnam Idol 2016 as season seven](https://vtv.vn/goc-khan-gia/vietnam-idol-2016-chinh-thuc-khoi-dong-20160301232835106.htm). The complete episode count and official full-show playlist remain unresolved. |
| Mùa 8 | 2023 | completed | **16 numbered full-show uploads** | **Gap — official channel verified, no clean main-only playlist ID verified** | VTV calls the 2023 return [season eight after a seven-year break](https://vtv.vn/truyen-hinh/ha-an-huy-doi-thu-nang-ky-hang-muc-guong-mat-tre-an-tuong-vtv-awards-2023-20231218125017739.htm). The official channel publishes the numbered sequence, including [Tập 1](https://www.youtube.com/watch?v=pBi3ilxAtVU), [Tập 8](https://www.youtube.com/watch?v=JOfxP-h3qV0), and the Tập 16 finale on the same official channel. VTV’s wording calls these “16 liveshow”; use the verified numbered full-show sequence while retaining that terminology caveat. |

### Vietnam Idol population guardrails

- The official present-day channel ID does not prove that it owns or completely archives Mùa 1–7. Historical broadcaster/rights topology must be verified before attaching old uploads to the same authority.
- Do not fabricate episode counts from the highest surviving clip number. Older official pages often expose individual auditions, gala performances, result segments, or contestant packages rather than complete episodes.
- For Mùa 8, include titles that clearly identify a complete numbered episode. Exclude single audition clips, individual performances, judges’ reactions, highlights, and result snippets even when their thumbnails use the season branding.
- The branded years are intentional: Mùa 4 is commonly labelled 2012 though its final fell in 2013; Mùa 5 is labelled 2013 though its final fell in 2014.

## 6. Nữ Hoàng Vũ Đạo Đường Phố

| Season | Year | Status | Source-bound main count | Official playlist | Evidence and classification |
|---|---:|---|---:|---|---|
| Mùa 1 | 2024 | completed | 15 | [`PLJSRfYQoW3dlrKn-U263kJN6t8JogGz0r`](https://www.youtube.com/playlist?list=PLJSRfYQoW3dlrKn-U263kJN6t8JogGz0r) — **official but mixed, not a clean 15-item main-only playlist** | HTV’s [show hub](https://www.htv.com.vn/nu-hoang-vu-dao-duong-pho) and [video hub](https://www.htv.com.vn/video-nu-hoang-vu-dao-duong-pho) establish the numbered run through Tập 15. The first-party launch identifies [Madison Media Group, Studio Gl1de, and Needlab G&C and the 27 July 2024 broadcast start](https://www.htv.com.vn/chuong-trinh-nu-hoang-vu-dao-duong-pho-street-woman-fighter-viet-nam-ra-mat). |

The official producer channel publishes full episodes including [Tập 1](https://www.youtube.com/watch?v=91tRLDt_dHs), [Tập 2](https://www.youtube.com/watch?v=47rrIVa174U), [Tập 3](https://www.youtube.com/watch?v=hUya6D_dBFY), [Tập 4](https://www.youtube.com/watch?v=aHO5QlfHRc8), [Tập 5](https://www.youtube.com/watch?v=Hl12NL_Gs6U), and [Tập 6](https://www.youtube.com/watch?v=KkMWNF3O1nc). HTV Entertainment also publishes official catch-up episodes such as [Tập 9](https://www.youtube.com/watch?v=8ClSKzIXYPo).

### Nữ Hoàng Vũ Đạo Đường Phố population guardrails

- The linked HTV playlist contains substantially more than 15 items and mixes full episodes with related assets. It is an official discovery surface, not a ready-to-ingest main-season manifest.
- Madison Media Group and HTV may carry duplicate official uploads of the same logical episode. Resolve by season + logical episode number and select one canonical publisher/video; do not count duplicate uploads as additional episodes.
- Exclude dance-performance extracts, battle-only cuts, teasers, interviews, crew profiles, highlights, reaction clips, and press-event videos.
- No first-party Mùa 2 announcement or episode was verified by the cutoff.

## Population-ready source matrix

| Program | Verified seasons | Clean official full-main playlist coverage | Required fail-closed action |
|---|---:|---|---|
| Rap Việt | 4 | Mùa 3 only | Reconstruct Mùa 1, 2, and 4 from official full-show pages; resolve Mùa 4’s 16-entry/“Tập 15 final” conflict before canonical numbering. |
| The Masked Singer Vietnam | 2 | Mùa 2 only | Reconstruct Mùa 1 and separate its 16 numbered episodes from specials, concerts, and the award/reveal program. |
| Tân Binh Toàn Năng | 1 season + 1 feeder phase | Both phases | Preserve phase identity and exclude the explicitly labelled spin-off playlist. |
| Our Song Vietnam | 1 | Complete | Use 14 delivered episodes; exclude the early 13-episode plan and the 78-track performance collection. |
| Vietnam Idol | 8 | None verified as clean main-only playlists | Treat Mùa 1–7 counts/playlists as unresolved; populate Mùa 8 only from complete numbered official uploads. |
| Nữ Hoàng Vũ Đạo Đường Phố | 1 | Official playlist exists but is mixed | Filter to 15 logical episodes and deduplicate Madison/HTV official mirrors. |

## Canonical ingestion tests

Before an item from these sources is accepted as a full main episode, all of the following should pass:

1. **Authority:** uploader channel ID or first-party page matches an authority in this registry.
2. **Season binding:** title, description, playlist, or broadcaster catalog binds the item to the exact season/phase.
3. **Full-show classification:** the item is a complete numbered episode or source-bound named final, not a performance, music/audio asset, highlight, recap, reveal, uncut item, concert, spin-off, or isolated audition.
4. **Logical numbering:** episode number is source-bound. Conflicted cases, especially Rap Việt Mùa 4, remain unresolved rather than receiving a guessed number.
5. **Deduplication:** mirrored official uploads map to one logical episode; aliases and alternate publisher video IDs are retained as provenance, not counted as extra episodes.
6. **Completeness:** a playlist is called “complete” only when its member inventory reconciles to the source-bound main count and all non-main items have been excluded.

## Explicit unresolved gaps

- Exact clean official full-main playlist IDs remain unverified for Rap Việt Mùa 1, Mùa 2, and Mùa 4; The Masked Singer Vietnam Mùa 1; all eight Vietnam Idol seasons; and Nữ Hoàng Vũ Đạo Đường Phố (whose available official playlist is mixed).
- Exact source-bound main-episode counts remain unverified for Vietnam Idol Mùa 1–7.
- Historical Vietnam Idol uploader/rights ownership for Mùa 1–7 remains unresolved; the current official channel must not be retroactively treated as complete authority without direct first-party evidence.
- Rap Việt Mùa 4 has a source conflict between VieON’s `16/16` catalog and Vie Channel’s final title using `Tập 15`; it requires video-level reconciliation.
- The Masked Singer Mùa 1 has a `17/17` platform header but only 16 numbered competition episodes plus separately classified specials/award programming. Raw card count is not a valid main-episode count.
- No later season for any program in scope was admitted because no first-party season announcement or episode surface was verified by the cutoff.

