# Vietnam Entertainment Main-Show YouTube Views

This repository builds an auditable registry of canonical full main-show episodes on official
YouTube channels. It records exact, timestamped video views; it does **not** estimate unique
viewers or cross-platform audience.

The current implementation is deliberately limited to the Phase 1 gate: configure all five Tier
1 shows, validate the method on one `ATSH` source, and expand only after the pilot passes QC.

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

See [the architecture](docs/architecture.md) and the current
[Apify actor selection](docs/research/apify-actor-selection.md).
