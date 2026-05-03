# PR #230 FH/LSZ Target-Timeseries Replacement Queue

**Status:** bounded-support / replacement scheduling checkpoint
**Runner:** `scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py`
**Certificate:** `outputs/yt_fh_lsz_target_timeseries_replacement_queue_2026-05-02.json`

## Purpose

The autocorrelation/ESS gate now has a ready set large enough for target
statistics, but only chunks001, 011, and 012 carry per-configuration
source-response and scalar-LSZ target time series. Chunks002-010 are ready
production chunks, but they predate target-timeseries serialization.

This runner derives the replacement queue from the current autocorrelation
certificate. It prevents the campaign from mistaking more new chunks for a
complete repair of the existing ready-set target ESS gap.

## Result

```text
python3 scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py
# SUMMARY: PASS=8 FAIL=0
```

The current replacement queue is chunks002-010. Chunk013 and later can add new
target-timeseries support, but `complete_for_all_ready_chunks` remains false
while chunks002-010 stay in the ready set without target-series replacement.

## Claim Boundary

This is scheduling support only. It does not certify target ESS, response
stability, full L12/L16/L24 production, scalar-pole derivative/model-class/FV/IR
control, or canonical-Higgs identity. It authorizes no retained or
`proposed_retained` wording.

## Next Action

Rerun chunk002 with target-timeseries serialization if completing the current
ready-set target ESS gate is prioritized; otherwise continue new target-series
chunks toward the full L12 set. Do not claim complete target ESS while the
replacement queue is nonempty.
