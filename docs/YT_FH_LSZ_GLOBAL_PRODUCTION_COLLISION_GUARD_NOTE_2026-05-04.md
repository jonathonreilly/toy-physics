# PR #230 FH/LSZ Global Production Collision Guard

Date: 2026-05-04

Status: bounded-support / infrastructure and provenance guard only.  This note
does not authorize retained or proposed_retained y_t closure.

## Purpose

The FH/LSZ target-timeseries and pole-fit production lanes now have enough
long-running workers that launch provenance is a claim-surface issue.  A chunk
must not be counted as evidence merely because a foreground session started,
an empty output directory exists, or `launchctl submit` returned success.  It
must produce the expected artifact and pass the relevant chunk certificate.

This guard records the current global FH/LSZ production occupancy from the
process table, compares it with the configured global cap of six production
workers and a conservative local resource threshold of four active workers,
and records whether launching new workers is allowed.

## Current Checkpoint

Latest update: the polefit8x8 wave orchestrator was hardened to use the same
process-table shape as this guard.  A dry run showed 12 completed polefit8x8
chunks, zero active workers, and 51 missing chunks.  After the guard allowed
launch, chunks013-018 were started from the repository cwd with fixed seeds
2026051913-2026051918 and isolated output directories.

The refreshed guard now records six active polefit8x8 production workers,
which is exactly the global cap.  It therefore blocks any additional FH/LSZ
production launch until workers finish and their artifacts can be checked.
The active chunk013-018 workers are run control only: no root polefit8x8
outputs are counted as evidence until the chunk combiner and downstream
certificates pass.

The earlier attempted interactive chunk025/chunk026 runs in this worktree
wrote no output certificates; those failed sessions are not evidence.  After
rebasing onto the updated PR branch, completed chunk025/chunk026 artifacts are
present and are counted only through their own chunk certificates, not through
this guard.  Scheduler submission success by itself is never evidence.

A separate worktree has been running the FH/LSZ polefit8x8 wave.  The guard
blocks additional FH/LSZ production chunks whenever active global occupancy is
at the hard cap or already above the conservative local resource threshold.

## Certificate

Runner:

```bash
python3 scripts/frontier_yt_fh_lsz_global_production_collision_guard.py
```

Output:

```text
outputs/yt_fh_lsz_global_production_collision_guard_2026-05-04.json
```

The certificate is support only.  It preserves these boundaries:

- no empty directory or failed run is evidence;
- no detached launch counts without a passing output artifact/certificate;
- no source-only FH/LSZ result is a physical y_t readout until the
  canonical-Higgs/source-overlap or same-source W/Z response route closes;
- no H_unit, yt_ward_identity, observed top mass/y_t, alpha_LM, plaquette/u0,
  or assumed kappa_s = 1 input is used as proof authority.
