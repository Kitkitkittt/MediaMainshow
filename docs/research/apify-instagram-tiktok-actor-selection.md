# Apify actor selection: Instagram and TikTok derivative discovery

Status date: **2026-08-13**  
Research boundary: Apify Store pages only; actors were not run and no account credentials were used.

## Decision

Use public Apify actors only as a separate, non-canonical discovery lane. A
keyword result is an observed candidate, never proof that an account is official
or that a post belongs to a show. Admit an item to a published derivative
summary only after the source account matches a reviewed authority record and
the run has a complete, schema-valid raw receipt.

## Recommended actors

| Platform and job | Actor ID | Minimal bounded input | Normalization fields to retain | Current stated price | Why selected |
|---|---|---|---|---|---|
| Instagram candidate-account and trend discovery | [`apify/instagram-search-scraper`](https://apify.com/apify/instagram-search-scraper) | One show/season keyword; one search type (`user`, `hashtag`, or `popular reels`); `resultsPerPage` no higher than the needed review batch (the Store documents a maximum of 250/keyword). | Search term/source; `id`; username; profile URL; name/bio; verified/business flags; follower/post counts. For reels: shortcode/URL, caption, hashtags, creator/coauthors, timestamp, duration, likes/comments/views/plays. | From **$1.50/1,000 results** in the current Store header; README lists Free $2.70/1,000, Starter $2.30/1,000 and Scale $1.90/1,000. | Apify-maintained, supports the three discovery modes needed to seed a reviewed authority queue. [Store contract](https://apify.com/apify/instagram-search-scraper) |
| Instagram verification of a candidate handle | [`apify/instagram-profile-scraper`](https://apify.com/apify/instagram-profile-scraper) | Explicit usernames, profile URLs, or profile IDs only; no keyword expansion. | Input URL; native profile ID; username/URL; name/bio/external links; verified/private/business flags; follower/following/post counts; latest-post/reel metadata if returned. | README: **$2.60/1,000 results** Free, **$2.30/1,000** Starter. The Store header is a lower “from” price, so quote the live pricing tab in each run receipt. | Apify-maintained, profile-first authority check rather than a broad content scrape. [Input and output](https://apify.com/apify/instagram-profile-scraper) |
| Instagram content from a verified handle | [`apify/instagram-reel-scraper`](https://apify.com/apify/instagram-reel-scraper) | A reviewed username/profile/ID or explicit Reel URLs; use a tight date boundary and exclude stale pinned posts if the actor input supports it. | Reel native ID/shortcode/URL; account ID/username; caption/hashtags/mentions; media type/duration/timestamp; likes/comments/views; music and any native collaboration fields. | README: **$2.60/1,000 results** Free, **$2.30/1,000** Starter; re-check the live pricing tab before scheduling. | Apify-maintained, and it directly accepts an already-reviewed profile or a specific Reel URL. [Input, output, and pricing](https://apify.com/apify/instagram-reel-scraper) |
| TikTok keyword, hashtag, or verified-profile content discovery | [`clockworks/tiktok-scraper`](https://apify.com/clockworks/tiktok-scraper) | Exactly one of `search`, `hashtags`, `profiles`, or video URLs per run; use small `resultsPerPage`; `profileScrapeSections: ["videos"]`; all `shouldDownload*` flags false; `scrapeRelatedVideos: false`. | Video ID and `webVideoUrl`; author ID/name/profile URL/verification; text/hashtags; `createTimeISO`; duration; music metadata; exact `playCount`, `diggCount`, `commentCount`, and `shareCount`. | From **$1.70/1,000 results** in the current Store header; PPE events and plan discounts require a live-price check. | The documented general-purpose actor covers discovery and exact verified-profile harvesting, and emits explicit error items. [Input, output, pricing, and errors](https://apify.com/clockworks/tiktok-scraper) |
| TikTok deep crawl of a reviewed official account | [`clockworks/tiktok-profile-scraper`](https://apify.com/clockworks/tiktok-profile-scraper) | `profiles: ["reviewed_handle"]`; explicit low `resultsPerPage`; all media-download flags false. | Profile ID/handle/bio/verification/privacy/follower and video counts; per-video ID, URL, caption, timestamp, music and exact plays/likes/comments/shares. | Store header: from **$1.00/1,000 results**; README says **$5/1,000**. This conflict is a hard pre-run pricing gate: record the live Pricing-tab quote or do not launch. | Dedicated account-first actor when the account has already passed authority review. [Input, output, and pricing](https://apify.com/clockworks/tiktok-profile-scraper) |

All quoted pricing is time-sensitive. Set both an Apify run `maxChargeUsd` and
a project-level cumulative cap; a price discrepancy is a failed preflight, not
a reason to estimate.

## Fail-closed run gates

1. **Authority first.** Discovery results become `NEEDS_REVIEW`. A deep profile
   or content run accepts only a configured, reviewed native handle/ID plus an
   evidence URL tying it to the show, broadcaster, or talent.
2. **One mode and bounded scope.** Keep search, hashtag, profile, and explicit
   URL runs separate. Supply the precise result/page limit, time window, and
   no media-download flags. Do not follow related-content graphs by default.
3. **Raw receipt before normalization.** Preserve actor ID/version, sanitized
   input, run/dataset ID, start/end times, status, charge, item count, raw
   dataset hash, and pagination/window. Store raw output outside the canonical
   episode lane.
4. **Schema and error gates.** Require platform-native item ID, canonical URL,
   source-account identity, timestamp, and integer metric fields when the actor
   claims them. TikTok records containing `errorCode` (such as `PROFILE_PRIVATE`,
   `NOT_FOUND`, or `INVALID_INPUT`) are receipt evidence, never empty successes.
   Missing/changed schemas, private items, incomplete pagination, or an
   unresolved actor error set status to `FAIL`, `WARNING`, or `NEEDS_REVIEW`.
5. **Metric semantics.** Snapshot Instagram `views`/`plays` and TikTok
   `playCount` separately with the field name and observation time. Never sum
   them with YouTube views or treat a null/missing value as zero.
6. **Canonical isolation.** Do not call the canonical episode extractor or
   write these records into the canonical registry. Use `(platform,
   native_content_id)` for deduplication in the derivative/social registry.

## Safe rollout order

1. Run a **single** small discovery control query per platform with a fresh
   live-price preflight and a hard per-run cap.
2. Manually validate returned handles against the existing authority evidence.
3. Deep-crawl only verified official handles with the profile/reel actors.
4. Compare the observed keys and error-item behaviour with this note before
   enabling a batch. Any material actor-schema, price, or authority change
   returns the source to `NOT_RUN`/`NEEDS_REVIEW`.

This accommodates broader derivative content without implying a first-party
platform API or platform-owner authorization; the existing official-API
feasibility matrix remains the governing policy for publication and metrics.
