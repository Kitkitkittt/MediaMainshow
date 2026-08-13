# Multi-platform source feasibility for derivative entertainment content

Status date: **2026-08-13**  
Research boundary: first-party documentation and official API specifications only. No credentials were used and no external state was changed.

## Decision

Keep the existing canonical-episode registry as the authority for full episodes. Add a separate **derivative-content registry** whose records may link to an episode, season, show, person, performance, or event, but never silently become canonical episodes. Platform metrics remain separate observations because a YouTube view, TikTok view, Instagram play/view, X impression, and Threads view are not equivalent measures.

Only YouTube is `SUPPORTED_NOW` for broad automated public discovery in the current project. X, Threads, and several owner-authorized account feeds are `CONNECTOR_READY`: their official APIs are technically usable, but production use first requires an app, token/approval, paid credits, or account-owner consent. Sources without a documented, policy-compliant public interface remain `BLOCKED` or manual corroboration only.

## Capability matrix

Status meanings:

- `SUPPORTED_NOW`: official broad public discovery and public metrics are available through an ordinary developer API, and the project already has a suitable ingestion pattern.
- `CONNECTOR_READY`: an official API exists, but a credential, billing, app review, permission, or account-owner authorization gate must pass before data collection.
- `BLOCKED`: no suitable documented official API exists for this use case, or current eligibility/geographic rules exclude it.

| Platform / access path | Status | Public discovery scope | Useful content and metric fields | Access, quota, and fail-closed caveats |
|---|---|---|---|---|
| **YouTube Data API / Shorts** | `SUPPORTED_NOW` | `search.list` can search public videos by query, channel, publication window, region, duration and order; verified channel uploads/playlists should still be preferred to broad keywords. | Video ID; title/description/tags; channel ID/title; publish time; duration; thumbnails; `viewCount`, `likeCount`, `commentCount`. | API key is sufficient for public data; OAuth is for private/owner operations. Current defaults are 100 `search.list` calls/day in its search bucket and 10,000 units/day for other endpoints; `videos.list` costs 1. Channel-scoped video search can return at most 500 videos unless an owner/developer filter applies. The public API has no reliable `isShort` field: `videoDuration=short` only means under four minutes. Owner-authorized Analytics has `creatorContentType=SHORTS`, but it cannot classify arbitrary public channels. Since 2025-03-31, Shorts `viewCount` counts starts/replays without a minimum watch time. ([search](https://developers.google.com/youtube/v3/docs/search/list), [video resource](https://developers.google.com/youtube/v3/docs/videos), [quota](https://developers.google.com/youtube/v3/determine_quota_cost), [Shorts counting change](https://developers.google.com/youtube/v3/revision_history), [Analytics dimensions](https://developers.google.com/youtube/analytics/dimensions)) |
| **X API v2** | `CONNECTOR_READY` | Seven-day recent search, full-archive search back to 2006, filtered stream, account timelines, and lookup support keywords, hashtags, `from:` accounts, language, media and other query operators. | Post ID/text/time/language; author; entities, references and conversation; attachments; public post metrics (`retweet_count`, `reply_count`, `like_count`, `quote_count`, `impression_count`, `bookmark_count`); video/GIF type, duration and public `view_count`. | Requires an X developer app, Bearer Token, prepaid credits, and an explicit spending limit. Pricing is pay-per-use and endpoint prices are shown in the Developer Console. Current documented request ceilings include recent search 450/app/15 min with 100 results/request, full archive 1/sec and 300/app/15 min with 500 results/request, and account timelines 10,000/app/15 min. Pay-per-use plans have a 2 million Post-read monthly cap. Store both Post impressions and media video views: they are different metrics, and the video view count is aggregated across posts containing that video. ([search](https://docs.x.com/x-api/posts/search/introduction), [query guide](https://docs.x.com/x-api/posts/search/integrate/overview), [rate limits](https://docs.x.com/x-api/fundamentals/rate-limits), [metrics](https://docs.x.com/x-api/fundamentals/metrics), [pricing](https://docs.x.com/x-api/getting-started/pricing), [usage cap](https://docs.x.com/x-api/fundamentals/post-cap)) |
| **Threads API public discovery** | `CONNECTOR_READY` | `keyword_search` finds public Threads posts by keyword or topic tag, `TOP` or `RECENT`, and time range; `profile_lookup` and `profile_posts` support exact public-profile discovery. | Post ID; media/product type; URL/permalink; username; text; timestamp; thumbnail/children; quote/repost relationships; alt text; topic/location and verification fields. | Requires a Meta app, Threads OAuth user token, and the relevant `threads_keyword_search` and/or `threads_profile_discovery` scopes. The official search request allows up to 50 records/page. The official public-search response does not expose post insights; the insights endpoint documents views, likes, replies, reposts, quotes and shares for authorized account use. Treat numerical quota as `UNKNOWN_UNTIL_QUALIFIED` unless the active app dashboard/response headers state it. ([official Threads workspace](https://www.postman.com/meta/threads/overview), [keyword search](https://www.postman.com/meta/threads/request/34203612-b3b2c12a-7ce6-4d86-a3c6-6d31e3b66ea1), [public profile posts](https://www.postman.com/meta/threads/documentation/dht3nzz/threads-api?entity=request-34203612-b819fb2c-8315-461f-8f30-365f7a32d1b1), [post insights](https://www.postman.com/meta/threads/request/34203612-385abc7d-b3cc-4e5d-9937-ebbe7174e041)) |
| **Instagram API: professional-account media and insights** | `CONNECTOR_READY` | Can retrieve media owned by an authorizing professional account. Business Discovery returns basic metadata/media for other professional accounts; hashtag search returns `top_media` and public `recent_media`. It cannot access consumer/personal accounts and is not general keyword search. | Media ID, caption, media/product type, URL/permalink, thumbnail, timestamp, children, public like/comment/view fields where supported; owner-authorized insights can include views/plays, reach, likes, comments, shares, saves, total interactions, watch time and replay-related Reel metrics. | Requires a Meta app, querying professional account and user/page token; Advanced Access is required when serving accounts not owned/managed by the app operator. Hashtag Search also requires Instagram Public Content Access and is capped at 30 distinct hashtags per rolling seven days; `recent_media` covers only the prior 24 hours, top/recent return at most 50/page, ordering is not guaranteed, promoted posts are excluded, and username cannot be requested there. Insights are only for owned media, some account metrics require 100+ followers, and user metrics are retained up to 90 days. Empty insight data means unavailable, not zero. Quotas use Meta usage headers/business-use-case controls; qualify observed headers before scheduling. ([official Instagram collection](https://www.postman.com/meta/instagram/documentation/6yqw8pt/instagram-api), [Business Discovery](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/business_discovery/), [hashtag search](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-hashtag-search/), [recent media](https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-hashtag/recent-media), [official insight requirements and fields](https://www.postman.com/meta/instagram/documentation/6yqw8pt/instagram-api?entity=request-23987686-26e7999c-fc7e-44c8-8f71-ab2de8d35c32), [platform rate limits](https://developers.facebook.com/docs/graph-api/overview/rate-limiting/)) |
| **Facebook Pages / Reels owned by an authorizing Page** | `CONNECTOR_READY` | The Pages API can operate on Pages a user manages; use an explicit registry of verified official Page IDs, not consumer search results. | Page identity/tasks and Page-owned post/video/Reel identifiers and metadata; available engagement/insight fields depend on permissions and endpoint version. | Requires a Meta app, user token, Page access token and appropriate Page permissions. This path proves control of an official Page but does not grant broad arbitrary-page discovery. Capture Graph API version and `x-app-usage` / `x-business-use-case-usage` headers on every receipt because limits are app/use-case dependent. ([official Facebook collection](https://www.postman.com/meta/facebook/documentation/r56bjfd/facebook-api), [Page token flow](https://www.postman.com/meta/facebook/documentation/r56bjfd/facebook-api?entity=request-23987686-4437f4e3-569e-4982-95ba-69a9c2452500), [official Reels example and usage headers](https://www.postman.com/meta/facebook/documentation/r56bjfd/facebook-api?entity=request-23987686-0b79260c-96bd-49de-875b-6076213785fc)) |
| **Facebook arbitrary public Pages** | `BLOCKED` pending approval; public video coverage remains incomplete | Page search/feed access outside Pages managed by an app user requires Page Public Metadata Access and/or approved Page Public Content Access (PPCA). PPCA covers public business metadata, Page posts/comments and engagement, but there is no approved project credential in evidence. | Page posts can expose creation time/message/attachments/permalink, shares, comments and reactions after approval; exact fields must be contract-tested against the approved app and current Graph version. | App Review and business verification are hard gates; Meta may require an additional contract. Before approval, access is limited to Pages connected to app-role users. A Page feed returns roughly 600 ranked published posts/year with at most 100/request, and restricted/shared/expired posts can be absent. Critically, Meta documents Page video listing as admin-only and the Page `videos` edge as no longer readable, so PPCA does not establish comprehensive public-video discovery. Until qualification passes, record `ACCESS_NOT_APPROVED`, not zero results. ([Page search](https://developers.facebook.com/docs/pages-api/search-pages/), [PPCA](https://developers.facebook.com/docs/features-reference/page-public-content-access/), [Page feed](https://developers.facebook.com/docs/graph-api/reference/page/feed/), [Page posts](https://developers.facebook.com/docs/graph-api/reference/page-post/), [Page videos](https://developers.facebook.com/docs/graph-api/reference/page/videos/)) |
| **TikTok Display API** | `CONNECTOR_READY` for official partners | Lists recent public videos of a TikTok user who explicitly authorizes the app; known IDs can be queried for that user. It is not cross-account keyword discovery. | ID; title/description; creation time; duration/dimensions; share/embed/cover URLs; view, like, comment and share counts. | Requires developer app approval, Login Kit, `video.list`, and creator consent. `video.list` returns at most 20/page; the documented default is 600 requests/minute per endpoint; cover URLs expire. Best fit is opt-in feeds from verified show/broadcaster/talent accounts. ([overview](https://developers.tiktok.com/doc/display-api-overview), [authorization](https://developers.tiktok.com/doc/display-api-get-started), [video list](https://developers.tiktok.com/doc/tiktok-api-v2-video-list/), [video fields](https://developers.tiktok.com/doc/tiktok-api-v2-video-object), [limits](https://developers.tiktok.com/doc/tiktok-api-v2-rate-limit/)) |
| **TikTok Research API** | `BLOCKED` for the current ordinary/commercial project unless eligibility is independently proved | Powerful public-video query by description keyword, username, region, hashtag, music, effect, duration, date or ID, with Boolean conditions and fuzzy string matching. | ID/creator/description/time/region/duration; hashtags, music, effects, mentions, playlist, labels/tags, voice-to-text; views, likes, comments, shares and favorites. | TikTok limits access to qualifying non-commercial researchers and eligible institutions/regions; a developer account alone is insufficient, and creators, advertisers and commercial users are explicitly ineligible. Approved use is limited to 30-day query windows, 100 records/page, 1,000 requests and 100,000 records/day; tokens expire after two hours. New videos may lag 48 hours and statistics up to 10 days. Vietnam is a queryable content region, but that does not make a Vietnam-based commercial applicant eligible. ([eligibility](https://developers.tiktok.com/products/research-api/), [query](https://developers.tiktok.com/doc/research-api-specs-query-videos), [codebook](https://developers.tiktok.com/doc/research-api-codebook), [limits and lag](https://developers.tiktok.com/doc/research-api-faq)) |
| **TikTok Commercial Content API** | `BLOCKED` for Vietnam coverage | Search disclosed commercial content/ads after application approval. | Advertiser/creator/brand/label, dates, video link/status/cover, plus ad reach/targeting fields where applicable. | TikTok states that the current dataset is EU-only; it does not solve Vietnamese entertainment coverage. ([official product page](https://developers.tiktok.com/products/commercial-content-api)) |
| **Zalo / Zalo Video** | `BLOCKED`; manual first-party evidence only | The public developer catalog covers Zalo Official Account operations, messages/content management, Login/Social, SDKs and widgets. No documented public cross-account Zalo Video/post search or public engagement-metrics API was found in that catalog. | No suitable documented public discovery/metrics contract. | Do not reverse-engineer consumer endpoints. Accept only manually supplied official URLs/screenshots/exports or a future documented partner feed, each with provenance and observation time. ([Zalo developer catalog](https://developers.zalo.me/docs/), [Zalo developer products](https://developers.zalo.me/)) |
| **VieON** | `BLOCKED` as metrics connector; manual first-party catalog corroboration | Official title pages expose show/episode and related-video catalog information such as trailers, previews, interviews, MV/OST and scene clips. | Page-visible titles, episode/season context, duration/year/rating/resolution and derivative labels. | No public developer API, authentication contract, supported quota or stable metric definition was found. Use official pages to corroborate taxonomy/identity, not as a scalable engagement feed; never treat a page-visible count as a validated metric without a published definition. ([example official title page](https://vieon.vn/cuoc-chien-ha-luu--eps-tap-5.html)) |
| **FPT Play** | `BLOCKED`; manual first-party evidence only | No suitable public developer/search API was found on the official service surface reviewed. | No documented public content/metrics schema. | Request a formal partner feed/API or retain manual official URLs as evidence. Do not reverse-engineer the consumer service. ([official service](https://fptplay.vn/)) |

## Derivative-content scope

Use a controlled `content_role` vocabulary so expanding coverage does not contaminate the canonical episode metric:

| Group | `content_role` values | Typical signals, never sufficient alone |
|---|---|---|
| Editorial extracts | `CLIP`, `HIGHLIGHT`, `SCENE`, `BEST_MOMENT`, `PERFORMANCE_EXCERPT` | “clip”, “highlight”, “trich doan”, “man trinh dien”, short duration, explicit episode reference |
| Promotion and navigation | `TEASER`, `TRAILER`, `PREVIEW`, `PROMO`, `COUNTDOWN`, `NEXT_EPISODE` | “teaser”, “trailer”, “preview”, “don xem”, scheduled date |
| Retrospective/editorial | `RECAP`, `REACTION`, `COMMENTARY`, `ANALYSIS`, `COMPILATION`, `TOP_MOMENTS` | “recap”, “reaction”, “tong hop”, “top”, multiple episode references |
| Production access | `BEHIND_THE_SCENES`, `BACKSTAGE`, `MAKING_OF`, `INTERVIEW`, `PRESS_EVENT`, `CAST_CONTENT` | “hau truong”, “behind the scenes”, cast/crew names |
| Music | `OST`, `MUSIC_VIDEO`, `LYRIC_VIDEO`, `THEME_SONG`, `LIVE_PERFORMANCE`, `DANCE_PRACTICE` | track/music IDs, song title, performer, show branding |
| Platform-native reuse | `SHORT`, `REEL`, `STORY`, `THREAD`, `POST`, `LIVESTREAM_EXCERPT` | platform format plus content evidence; format is not the editorial role |
| Transformative/community | `REMIX`, `DUET`, `STITCH`, `MEME`, `FAN_EDIT`, `FAN_CAM`, `PARODY`, `COVER` | explicit native relationship when exposed, creator authority, transformation markers |
| Re-publication and risk | `LICENSED_REUPLOAD`, `UNAUTHORIZED_COPY`, `PIRATED_FULL_EPISODE`, `UNKNOWN_REUPLOAD` | exact/near duplicate, official rights statement, source provenance; never infer licensing from popularity |

Keep `platform_format` separate from `content_role`: an Instagram Reel can be a trailer, backstage clip, fan edit, or unauthorized full-episode copy. A content item may have one primary role and multiple secondary tags, but uncertain classifications must remain `UNKNOWN` and enter review.

## Updateable fail-closed pipeline

### 1. Configuration, not hard-coded searches

Maintain one versioned source record per official or watched account:

```yaml
source_id: datvietvac_youtube
platform: youtube
account_native_id: "..."
account_url: "..."
authority: SHOW_OWNER
authority_evidence_url: "..."
shows: [show_id]
discovery_modes: [uploads_playlist, channel_search]
enabled: true
credential_profile: youtube_public_v1
last_authority_reviewed_at: 2026-08-13
```

Maintain search packs separately by show/season with official titles, aliases, diacritic-free forms, cast/judge names, episode tokens, hashtags, song/performance names, and derivative terms. Each term records language, validity dates and why it exists. This makes future updates a data change rather than an adapter rewrite.

### 2. A common adapter contract

Every platform adapter must implement four independently testable capabilities:

1. `qualify()` — prove authentication mode, permissions, API/schema version, account authority, quota headers and a non-demo live response.
2. `discover(cursor, window)` — emit immutable raw candidates and pagination/checkpoint state.
3. `hydrate(native_ids)` — retrieve current metadata and public metrics in batches where supported.
4. `snapshot(native_ids, observed_at)` — append exact integer observations with the platform metric name and definition version.

The adapter declares capabilities (`keyword_search`, `account_feed`, `historical_search`, `public_metrics`, `owner_insights`, `webhooks`) and limitations. Unsupported capabilities return a typed status, never an empty successful dataset.

### 3. Immutable evidence before normalization

For every request retain a content-addressed receipt containing platform, endpoint/API version, request parameters with secrets removed, account/app mode, HTTP status, response headers relevant to quota/version, retrieval time, cursor/window, raw body hash and raw object count. Store raw response bytes before normalization. Resume completed pages/runs instead of paying for or re-requesting them.

### 4. Candidate identity and relationships

Use `(platform, native_content_id)` as immutable observed identity. Keep URLs as mutable attributes. Record:

- `authority_class`: `SHOW_OWNER`, `LICENSED_BROADCASTER`, `TALENT_OFFICIAL`, `SPONSOR_OFFICIAL`, `PRESS_OFFICIAL`, `FAN`, `UNVERIFIED`;
- `relationship_target_type`: `SHOW`, `SEASON`, `EPISODE`, `PERSON`, `SONG`, `EVENT`, or `UNKNOWN`;
- `relationship_evidence`: `EXPLICIT_NATIVE_LINK`, `EXPLICIT_TEXT_LINK`, `OFFICIAL_PLAYLIST_COLLECTION`, `MANUAL_CONFIRMED`, `INFERRED`, or `UNKNOWN`;
- `classification_state`: `ACCEPTED`, `REJECTED`, `NEEDS_REVIEW`, or `UNCLASSIFIED`.

Only `ACCEPTED` candidates from a reviewed authority source may enter published derivative summaries. Inferred episode links can support discovery but not episode-level aggregation.

### 5. Preserve metric semantics

Store metric observations long-form:

```text
platform, native_content_id, metric_name, metric_value_exact,
observed_at, metric_definition_version, visibility, receipt_id
```

Never sum unlike metrics into “total views.” Present per-platform totals and, if useful, a clearly labelled cross-platform **activity index** whose formula is versioned and does not claim audience reach. Snapshot deletions/private transitions as state changes; do not erase prior observations.

### 6. Explicit run and coverage statuses

At source, show and platform levels use:

- `PASS`: qualified adapter, authoritative sources covered, pagination/window complete, raw receipts present, schema and dedupe checks pass;
- `WARNING`: usable but delayed metrics, an API-documented coverage limitation, or a bounded manual-review queue;
- `FAIL`: transport/schema/authority/dedupe/completeness failure;
- `ACCESS_NOT_APPROVED`: app review, owner consent, billing or research eligibility absent;
- `NO_SUPPORTED_API`: official documentation offers no compliant connector;
- `NOT_RUN`: configured but not attempted;
- `STALE`: last successful observation exceeds the source-specific freshness SLA.

An empty result is `PASS` only when the adapter is qualified, the search window and pagination are complete, and a control query proves the endpoint was returning real data.

### 7. Bounded rollout

1. Extend YouTube first: add the derivative taxonomy and search packs while preserving the canonical-episode boundary.
2. Pilot X with a hard prepaid/spending cap against two shows and two official accounts; validate Post impressions versus media video views.
3. Pilot Threads keyword/profile discovery with one token and record observed permission/rate headers; do not publish insights for posts the token cannot legitimately access.
4. Offer TikTok Display, Instagram, and Facebook connectors only to verified official account owners who authorize access.
5. Keep TikTok Research, arbitrary Facebook Pages, Zalo Video, VieON metrics and FPT Play automated discovery disabled until their documented gate changes or formal access is granted.

## Maintenance checklist

Review quarterly and whenever a platform changelog or API version changes:

1. Re-open every primary source link and record `docs_reviewed_at`, API version, deprecations and changed metric definitions.
2. Re-run `qualify()` with a tiny capped control set; compare observed keys/types against the stored schema fixture.
3. Confirm permissions, billing cap, rate-limit headers, token lifetime and regional/eligibility terms.
4. Re-prove official account ownership/authority; quarantine renamed, transferred or compromised accounts.
5. Diff derivative search packs and taxonomy; add new labels without rewriting historical classifications.
6. Run deterministic duplicate/near-duplicate and episode-link review before aggregation.
7. Publish coverage by platform/status, including `ACCESS_NOT_APPROVED` and `NO_SUPPORTED_API`; never hide unavailable platforms inside a zero.

## Recommended near-term backlog

| Priority | Deliverable | Exit gate |
|---|---|---|
| P0 | Derivative registry schema, controlled taxonomy, raw-receipt format and long-form metric snapshots | Unit/schema tests prove derivative records cannot enter canonical episode totals |
| P0 | YouTube derivative search packs for all shows, seeded from verified channel IDs/playlists | Bounded pilot has complete pagination receipts, deterministic classifications and reviewed false positives |
| P1 | X read-only connector | App/token and prepaid hard cap approved; live schema, rate headers, dedupe and cost receipt pass |
| P1 | Threads read-only connector | Required scopes approved; keyword and exact-profile control queries pass; unavailable insights remain null with reason |
| P2 | Owner-opt-in TikTok Display + Instagram/Facebook professional connectors | Each account authorizes; authority and token lifecycle are proved; app-review scope is documented |
| Hold | TikTok Research, arbitrary Facebook Pages, Zalo Video, VieON/FPT Play metrics | Enable only after eligibility/approval or a documented first-party partner contract exists |
