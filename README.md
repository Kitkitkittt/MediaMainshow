# Vietnam Entertainment Main-Show YouTube Views

This repository builds an auditable registry of canonical full main-show episodes on official
YouTube channels. It records exact, timestamped video views; it does **not** estimate unique
viewers or cross-platform audience.

The current implementation covers the seeded 30-show universe across Tiers 1-5. Seasons without
a verified official YouTube source remain explicit source gaps rather than being filled from fan
uploads or inferred metadata.

## Quick start

```powershell
uv sync --extra dev
$env:APIFY_TOKEN = $env:apify_api  # only if your local token uses the legacy name
uv run mainshow pilot --show ATSH --search-limit 20
uv run mainshow pilot --show ATSH --actor streamers/youtube-scraper `
  --source-url "https://www.youtube.com/playlist?list=..." --search-limit 30
uv run pytest
```

The CLI also reads `APIFY_TOKEN` or `apify_api` directly. It never writes or logs the token.
Actor responses are cached under `data/raw/` before transformation. Generated research tables
are written to `outputs/`.

## Phase 1 gate

Do not publish a completed-season total unless its QC status is `PASS`. `WARNING` may be used for
clearly disclosed caveats; `FAIL` suppresses the total. Only canonical video IDs contribute to
normal aggregation, so syndicated copies and re-uploads are not silently double-counted.

## Video typing and review

The deterministic classifier records a `video_type` before deciding whether a candidate is a
canonical main episode. It distinguishes numbered episodes, source-bound finales, annual full
shows, Shorts, previews, highlights, recaps/reactions, uncut material, backstage/production
diaries, dance practice, press/interviews, cast challenges, compilations, music/performance
assets, livestreams, clips, special extras, annual fragments, and non-main-channel mirrors.
Season configuration can enable
bare episode numbers for rolling programs, while `config/decisions.yaml` records exceptional
episode assignments and exclusions with an auditable reason. Ambiguous evidence remains in
`manual_review.csv`; it is never silently promoted into aggregates.

See [the architecture](docs/architecture.md) and the current
[Apify actor selection](docs/research/apify-actor-selection.md).

`build-all` also produces a separate derivative registry, a complete versioned YouTube search
plan, source-linked social-account candidates, and an explicit platform-access coverage matrix.
These outputs never enter canonical episode totals. See the
[social/derivative update runbook](docs/social-derivative-update-runbook.md) and the
[official-platform feasibility research](docs/research/multi-platform-source-feasibility.md).
