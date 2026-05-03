# PR #230 FH/LSZ Target-Timeseries Replacement Queue

**Status:** bounded-support / replacement scheduling checkpoint
**Runner:** `scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py`
**Certificate:** `outputs/yt_fh_lsz_target_timeseries_replacement_queue_2026-05-02.json`

## Purpose

The autocorrelation/ESS gate now has a ready set large enough for target
statistics. The current target-series complete ready chunks are chunks001
through 012. The earlier replacement queue, chunks004-010, has been consumed
with fixed seeds and chunk-isolated artifact paths.

This runner derives the replacement queue from the current autocorrelation
certificate. It prevents the campaign from mistaking more new chunks for a
complete repair of the existing ready-set target ESS gap.

## Result

```text
python3 scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py
# SUMMARY: PASS=9 FAIL=0
```

The current replacement queue is empty for the ready set:

```text
complete_target_timeseries_indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
replacement_queue = []
```

Chunk013 and later can add new target-timeseries support, but they are no
longer a repair for a missing ready-set target-series queue. Target ESS still
needs its own predeclared blocking/bootstrap or integrated-autocorrelation
certificate.

## Claim Boundary

This is scheduling support only. It does not certify target ESS, response
stability, full L12/L16/L24 production, scalar-pole derivative/model-class/FV/IR
control, or canonical-Higgs identity. It authorizes no retained or
`proposed_retained` wording.

## Next Action

Rerun the autocorrelation/ESS gate with a target-observable blocking/bootstrap
certificate before treating the ready set as production evidence. Continue new
target-series chunks toward the full L12 set only as production support.
