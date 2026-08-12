# Apify actor selection for the Phase-1 YouTube main-show dataset

**Research date:** 2026-08-12  
**Scope:** Read-only review of current official Apify Store pages, actor schemas, actor-maintainer documentation hosted by Apify, and Apify API documentation. No Actor was run, no credits were spent, and no credential was read or exposed.

## Decision

**Live override:** use `streamers/youtube-scraper` for this repository's current automated runs. The account-level pilot returned complete machine-readable records from Streamers, while API Dojo returned demo placeholders only.

The following paragraph records the documentation-only decision made before live validation:

Use **`apidojo/youtube-scraper-api`** (including the `-api` suffix) for the first bounded ATSH pilot. It is the strongest current candidate for a unified discovery and metadata workflow because it accepts video, channel, playlist, search, and handle inputs and explicitly documents `views` as an integer, `duration` as integer seconds, and `publishDate` as ISO-8601. Those types align directly with the canonical episode and snapshot contracts. Its current event-based pricing is also substantially below the mature Streamers actor for ordinary discovery volumes. [Actor documentation](https://apify.com/apidojo/youtube-scraper-api) [input schema](https://apify.com/apidojo/youtube-scraper-api/input-schema) [pricing](https://apify.com/apidojo/youtube-scraper-api/pricing)

This is a **pilot recommendation, not production approval**. The actor is community-maintained, and its prose promises playlist metadata and video order without documenting the concrete playlist-position field name in its example or field guarantee table. The ATSH pilot must therefore preserve the raw payload and fail closed if required fields or source provenance cannot be mapped unambiguously.

Keep **`streamers/youtube-scraper`** as the fallback for the pilot. It is maintained by Apify and has far stronger adoption and review evidence, and its formal output schema names useful provenance fields (`fromYTUrl`, `order`). However, its core fields are all optional in the schema, its duration is a formatted string, and its playlist/search results can expose relative rather than exact publication dates. Use a direct-video second pass and validate returned values before admitting a record to the canonical registry. [Actor documentation](https://apify.com/streamers/youtube-scraper) [input schema](https://apify.com/streamers/youtube-scraper/input-schema) [output schema](https://apify.com/streamers/youtube-scraper/output-schema) [pricing](https://apify.com/streamers/youtube-scraper/pricing)

Do not make **`apidojo/youtube-playlist-scraper`** the sole extractor. It is an inexpensive playlist enumerator, but the documented guarantee table does not guarantee publish date, playlist position, playlist ID, or unavailable-video status even though the README describes those capabilities. It is acceptable as an optional discovery/enumeration fallback only, followed by canonical video-detail extraction and schema validation. [Actor documentation](https://apify.com/apidojo/youtube-playlist-scraper) [input schema](https://apify.com/apidojo/youtube-playlist-scraper/input-schema) [pricing](https://apify.com/apidojo/youtube-playlist-scraper/pricing)

## Current comparison

| Actor | Maintenance evidence | Current pricing model | Relevant inputs | Relevant documented output | Phase-1 assessment |
| --- | --- | --- | --- | --- | --- |
| `apidojo/youtube-scraper-api` | Community-maintained; recently modified; smaller installed base | Pay per event: channel/search query **$0.015** including 30 videos; playlist query **$0.05** including 100; single-video query **$0.005**; each additional item **$0.0005**; Shorts/live query **$0.02** including 40 | `startUrls` for video/channel/playlist/search URLs; `youtubeHandles`; `keywords`; `includeShorts`; `includeLiveStreams`; `getTrending`; locale/filter controls; `maxItems` | Always documented: `id`, `url`, `title`, `channel.id`, `channel.name`, integer `views`, integer-second `duration`, ISO-8601 `publishDate`; playlist support promises order but does not name its JSON key | **Primary gated pilot.** Best match to exact-value and typed-field requirements; verify playlist provenance/order and unavailable-video behavior in raw output |
| `streamers/youtube-scraper` | Maintained by Apify; 4.9 rating and roughly 103K users shown at review time | Tiered pay per event: **$4.00/1,000 videos** on Free through **$2.40/1,000** on Business; channel date-range and AI options cost extra | `searchQueries`; `startUrls` for video/channel/playlist/search/hashtag; separate limits for regular videos, Shorts, and streams; search/date/length filters | `id`, numeric `viewCount`, `date`, formatted `duration`, `type`, channel fields, `fromYTUrl`, `order`; all relevant fields are optional in the formal schema | **Fallback / cross-check.** Strongest operational maturity and named source-order fields, but exact-date/type completeness must be proven per mode |
| `apidojo/youtube-playlist-scraper` | Community-maintained; specialized and smaller installed base | Pay per event: playlist query **$0.025** including 100 videos; keyword search **$0.005** including 100; additional item **$0.0005** | `startUrls`, `keywords`, `gl`, `hl`, `sort`, `maxItems`, `customMapFunction` | Guaranteed table includes video `id`, title, URL, numeric `views`, numeric-second `duration`, channel ID/name, thumbnails and `isLive`; README additionally claims playlist identifiers/order, publish date and unavailable flags without concrete guaranteed keys | **Discovery fallback only.** Cheap enumeration, but insufficient alone for the audit contract |

Pricing is time-sensitive. The Pricing tabs and current public Actor metadata were treated as authoritative where README marketing copy differed. In particular, the playlist actor README still shows a **$0.05** playlist-query figure while its current Pricing configuration shows **$0.025**; re-check pricing immediately before any paid run. The Streamers README has likewise advertised an older flat **$5/1,000** figure while its current Pricing tab is tiered.

## Field-contract assessment

### Playlist, channel, and video discovery

- `apidojo/youtube-scraper-api` provides the broadest single-actor input surface: direct video, channel, playlist and search URLs, handles, and keywords. It is therefore the simplest Phase-1 adapter and can support the preferred hierarchy of official playlist, official channel, then search fallback. [Input schema](https://apify.com/apidojo/youtube-scraper-api/input-schema)
- `streamers/youtube-scraper` also accepts video, channel, playlist, hashtag and search-result URLs, plus search terms. `maxResults`, `maxResultsShorts`, and `maxResultStreams` can keep regular-video discovery separate from excluded formats. [Input schema](https://apify.com/streamers/youtube-scraper/input-schema)
- `apidojo/youtube-playlist-scraper` accepts known playlist URLs and keywords that find playlists; it does not replace the general channel/video discovery actor. [Input schema](https://apify.com/apidojo/youtube-playlist-scraper/input-schema)

### Exact views, duration, and publication date

- `apidojo/youtube-scraper-api` has the strongest stated contract: integer `views`, integer seconds in `duration`, and ISO-8601 `publishDate` are documented as always present for its video records. [Output documentation](https://apify.com/apidojo/youtube-scraper-api#output)
- `streamers/youtube-scraper` defines numeric `viewCount`, a string `date`, and a string `duration` such as `00:03:27`, but all are optional. Discovery-mode examples can use relative dates. Treat playlist/search output as candidates and confirm canonical records with direct-video inputs when the publication value is not absolute. [Output schema](https://apify.com/streamers/youtube-scraper/output-schema)
- `apidojo/youtube-playlist-scraper` guarantees numeric `views` and numeric seconds in `duration`, but its formal guarantee table omits publication date. Its README's broader claims are not sufficient evidence for a required schema field until observed in the pilot. [Output documentation](https://apify.com/apidojo/youtube-playlist-scraper#output-format)

No Actor's marketing claim makes a value intrinsically trustworthy. The pipeline must require integer, non-negative views; parse and range-check duration; require an absolute publication timestamp for canonical episodes; and retain the unmodified raw item behind every normalized value.

### Playlist position and availability

This is the largest unresolved schema risk:

- `streamers/youtube-scraper` formally defines optional `order` and `fromYTUrl`, giving a concrete source-order and source-page mapping.
- Both API Dojo actors describe playlist order/position in prose but omit the concrete key from their minimal output and guaranteed-field tables.
- The specialized playlist actor describes unavailable/deleted handling, but availability/status is not in its guaranteed-field table.

Consequently, the pilot must not invent a playlist position or convert an omitted view count to zero. Missing, private, members-only, deleted, or region-blocked items must remain `view_count = null` with an availability/research flag. If the primary actor does not expose auditable playlist membership and position, use the Streamers actor as a bounded cross-check or preserve the playlist enumeration separately from the video-detail pass.

## Run and dataset identifiers

Every paid or free pilot extraction must retain both identifiers returned by Apify:

- Actor run ID: REST field `id` (Python client v3 attribute `run.id`).
- Default dataset ID: REST field `defaultDatasetId` (Python client v3 attribute `run.default_dataset_id`).

The Apify Run response includes the run ID and `defaultDatasetId`; dataset items are then fetched from `/v2/datasets/{DATASET_ID}/items`. Apify also supports a run-level `maxTotalChargeUsd` cap, which should be set even for a bounded pilot. [Run Actor API](https://docs.apify.com/api/v2/act-runs-post) [Apify API workflow](https://docs.apify.com/api/v2) [dataset retrieval](https://docs.apify.com/api/v2/dataset-items-get)

Persist at minimum:

```text
actor_name
actor_run_id
actor_dataset_id
actor_build_or_version
source_url
retrieved_at
raw_cache_path
```

`actor_dataset_id` should be added to the raw-run manifest even if the current CSV deliverables only require `actor_run_id`. A dataset ID alone is not a stable substitute for the cached raw response, so save the response before normalization.

## ATSH pilot gate

Use one known official ATSH playlist or, if none has yet passed authority review, one bounded official-channel/search input. Do not batch all Tier-1 shows in the first run.

1. Invoke `apidojo/youtube-scraper-api` with Shorts and live-stream expansion disabled, the smallest useful `maxItems`, and an explicit `maxTotalChargeUsd` safety cap.
2. Save the run object and complete raw dataset before transformation. Never log the API token.
3. Assert observed keys and types for video ID, source URL, channel ID, integer views, integer-second duration, absolute publish date, playlist/source provenance, order, and availability.
4. Classify and review ATSH candidates, then directly re-fetch only the accepted canonical video URLs if discovery records lack exact absolute metadata.
5. Compare the canonical set with the official playlist count/sequence. Any unexplained gap, duplicate logical episode, missing exact view, missing absolute publish date, or uncertain official source is `FAIL`, not a publishable season total.
6. If the primary actor fails the required-field or provenance assertions, run the same small input through `streamers/youtube-scraper` as the fallback. Do not expand to the other Tier-1 shows until one adapter produces a reproducible, cached and QC-complete ATSH registry.

## Caveats

- Actor schemas, prices, and behavior can change independently of this repository. Pin and record the Actor build/version returned by the run; revalidate the schema before each expansion wave.
- `apidojo/youtube-scraper-api` is community-maintained. Its lower cost and stronger written field contract do not outweigh a failed live schema test.
- `streamers/youtube-scraper` is maintained by Apify and much more widely used, but maintenance/adoption does not guarantee that optional fields are populated for Vietnamese playlist or channel results.
- Public, private, deleted, members-only, age-restricted, or geo-blocked videos can behave differently. Omission is not proof that an episode never existed.
- `view_count` is a current video-view counter, not a unique-audience measure. The dataset should describe cumulative YouTube main-show video views only.
## Live pilot evidence

These receipts were produced after the documentation review and supersede the pre-run preference for this account:

- `apidojo/youtube-scraper-api` run `nwyoqUcy8ejtMNKDP`, dataset `AgIFuyYunacWJ2DS9`, cost `$0.005`: ten records containing only `{"demo": true}`. This adapter is blocked for automated extraction on the current account/plan.
- `streamers/youtube-scraper` search run `qksDGsRv8IoDwbJjA`, dataset `Ta8xM3DVYEqihCMEE`, cost `$0.076`: 20 real records. It exposed exact video fields and a Vie Channel description link resolving to the official ATSH 2024 full-show playlist.
- `streamers/youtube-scraper` playlist run `6aaRakgaGJxf19zR1`, dataset `hlNp8mYjcKeR3aqOZ`, cost `$0.116`: 30 real playlist records, including 14 contiguous numbered main episodes and 16 deterministic exclusions.

Total observed Phase-1 actor usage was `$0.197`. The versioned raw envelopes preserve build IDs, inputs, run/dataset IDs, timestamps, charged-event counts, and unmodified items. ATSH 2024 has no unresolved `FAIL`; Episode 4 retains a duration `WARNING` because its runtime is 0.5751 of the season median.
