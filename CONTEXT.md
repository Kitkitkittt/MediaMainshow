# Domain context

The authoritative research object is a **canonical episode registry**, not a search result or a
season total. One logical episode is identified by `show_id + season_id + episode_no`; one YouTube
upload is identified by `video_id`. When several uploads map to one logical episode, only the
reviewed canonical upload enters the normal metric.

An **episode candidate** is a machine-observed YouTube video awaiting deterministic classification.
A **canonical episode** is an accepted full main-show upload from a verified official source. A
**view snapshot** is an append-only observation of the exact integer view count at an ISO timestamp.
A **season summary** is derived only from canonical episodes and carries `PASS`, `WARNING`, or
`FAIL` QC status.

The primary metric is **aggregate views across canonical full episodes**. It is neither unique
viewers nor total audience.

