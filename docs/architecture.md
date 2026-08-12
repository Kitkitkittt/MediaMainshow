# Phase 1 implementation architecture

## Decision

Build the canonical registry before aggregation and put the paid-source seam behind one small
interface. The pipeline is restartable: a cached raw actor response can be normalized, classified,
QC'd, and aggregated without another paid run.

```text
Tier 1 YAML -> Apify adapter -> immutable raw envelope -> normalizer -> classifier
                                                            |             |
                                                            v             v
                                                     episode registry -> QC
                                                            |
                                                            v
                                                append-only view snapshot
                                                            |
                                                            v
                                                     season summary
```

## Module interfaces

- `ApifyYouTubeClient.run(actor, input) -> RawRun`: submits and polls an actor, fetches its default
  dataset, and returns run metadata plus items. Credentials remain inside the adapter.
- `normalize_actor_item(item, provenance) -> VideoCandidate`: translates actor-specific fields into
  the stable candidate schema.
- `classify(candidate, show, rules) -> Classification`: applies hard exclusions before positive
  evidence. It returns a score, decision, reasons, and parsed episode number.
- `build_pilot(raw_run, configuration) -> OutputBundle`: creates registries, snapshots, summaries,
  manual review, and QC from cached evidence.

Tests cross the same interfaces. No classifier test needs Apify, and no cached-data rebuild spends
credits.

## Storage and audit invariants

1. Save the raw run envelope before normalization.
2. Never store an access token in a URL, output file, or log record.
3. Enforce unique `video_id` and flag duplicate logical episodes.
4. Append snapshots by `(video_id, snapshot_at)`; never overwrite historical observations.
5. Suppress completed-season totals when QC is `FAIL`.
6. Preserve actor name, run ID, dataset ID, retrieval timestamp, source URL, and classifier reasons.

## Phase boundary

This slice may spend credits on one bounded `ATSH` run only. The remaining Tier 1 shows stay
configuration-only until ATSH source authority, episode continuity, exclusions, and duplicates are
reviewed.

