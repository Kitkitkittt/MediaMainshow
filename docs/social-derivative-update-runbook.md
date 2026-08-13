# Social and derivative update runbook

This runbook keeps derivative coverage easy to extend without contaminating the canonical
episode/view totals. Raw evidence is immutable; normalized registries can always be rebuilt.

## Current boundary

- `outputs/episode_registry.csv` remains the canonical YouTube candidate universe.
- `outputs/derivative_content_registry.csv` is a separate candidate registry. Only rows with
  `classification_state=ACCEPTED` have both a known derivative role and reviewed YouTube
  channel authority.
- `CANONICAL_OVERLAP` means a long numbered canonical episode also contains a derivative
  keyword. It stays canonical and is queued for review; no automatic removal occurs.
- `outputs/social_account_candidates.csv` contains profile links observed in official-source
  YouTube descriptions. `SOURCE_LINKED_CANDIDATE` is evidence of a link, not proof of ownership.
- Cross-platform metrics are never added together as "total views." Metric names and platform
  definitions remain separate.

## Routine cached rebuild

From the repository root:

```powershell
uv sync --extra dev
uv run mainshow build-all --output outputs
uv run python -m pytest -q
uv run ruff check src tests
git diff --check
```

The build regenerates `derivative_content_registry.csv`, `derivative_search_plan.csv`,
`social_account_candidates.csv`, `social_metric_snapshot.csv`, and
`social_platform_coverage.csv`. It does not call a paid actor or any social platform.

## Add or change a derivative type

1. Add title patterns to `config/classifier_rules.yaml`.
   - `hard`: always excluded from the canonical registry.
   - `soft`: descriptive label that a verified numbered episode may retain.
   - `observational`: expands derivative discovery but never overturns a previously accepted
     numbered canonical episode.
2. Map the type to one controlled role in `TYPE_TO_ROLE` in `src/mainshow/social.py`.
3. Add discovery terms to `config/derivative_search_packs.yaml`.
4. Add a positive test and one collision test using a long numbered main episode.
5. Rebuild and compare the canonical count to the last approved baseline. Any change requires
   explicit review and a documented reason.

Prefer a narrow expression over a broad word. For example, `dance practice` is safer than
`dance`, and `official mv` is safer than `music`.

## Verify a discovered social account

1. Open the candidate's evidence video URLs and confirm that the linking YouTube channel is a
   reviewed official show owner/broadcaster/producer.
2. Confirm the destination profile identifies the same owner or show. Capture a stable
   first-party authority URL; follower count or a blue check alone is insufficient.
3. Add the account to `verified_sources` in `config/social_sources.yaml` with:

```yaml
- source_id: viechannel_instagram
  show_id: ATSH
  platform: instagram
  account_native_id: "..."
  account_url: https://www.instagram.com/viechannelhtv2
  authority_class: SHOW_OWNER
  authority_evidence_url: "..."
  discovery_modes: [authorized_professional_account]
  enabled: true
  last_authority_reviewed_at: 2026-08-13
```

4. Rebuild. The candidate becomes `VERIFIED`; it still has no content/metric coverage until a
   qualified connector produces immutable receipts.

## Enable a platform connector

Use the feasibility gates in `docs/research/multi-platform-source-feasibility.md`.

1. Obtain the documented app/token/owner consent and set a hard billing cap where applicable.
2. Implement and test `qualify`, `discover`, `hydrate`, and `snapshot` independently.
3. Save redacted request metadata, relevant quota/version headers, raw response bytes, cursor,
   observed time, and a body hash before normalization.
4. Contract-test IDs, timestamps, nullable metrics, exact integer metrics, pagination, deletion/
   private state, and token expiry against a tiny live control set.
5. Change platform status only after live qualification passes: `PASS`, `WARNING`,
   `ACCESS_NOT_APPROVED`, `NO_SUPPORTED_API`, or `FAIL`.
6. Append snapshots; never rewrite prior observations or convert unavailable metrics to zero.

## Recommended refresh cadence

- Every 14 days: rebuild cached registries, refresh qualified platform feeds, review new accounts,
  and resolve `CANONICAL_OVERLAP`/high-evidence unknowns.
- Every quarter: re-open official API documentation, record the API version and review date,
  re-run a tiny qualification set, validate permissions/rate headers, and re-prove account
  authority.
- On every platform/API change: stop publication for that platform until schema fixtures and
  metric definitions pass again.

## Release checklist

1. Raw receipt exists and its manifest/hash is present.
2. Platform/native ID dedupe passes.
3. Account authority is reviewed.
4. Content role is accepted; unknowns remain review-only.
5. Relationship to show/season/episode is explicit or manually confirmed.
6. Metric names, exact values, observation time, and definition version are present.
7. Coverage report shows unavailable/gated platforms explicitly.
8. Canonical episode count and totals are unchanged unless a separate canonical-registry review
   approved the change.
