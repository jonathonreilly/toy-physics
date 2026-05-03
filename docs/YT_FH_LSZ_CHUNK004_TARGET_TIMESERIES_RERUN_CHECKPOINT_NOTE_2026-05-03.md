# PR #230 FH/LSZ Chunk004 Target-Timeseries Rerun Checkpoint

**Status:** bounded-support / FH-LSZ chunk004 target-timeseries replacement checkpoint  
**Runners:** `scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py`, `scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py`, `scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py`  
**Certificates:** `outputs/yt_fh_lsz_chunk004_target_timeseries_generic_checkpoint_2026-05-02.json`, `outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json`, `outputs/yt_fh_lsz_target_timeseries_replacement_queue_2026-05-02.json`

## Result

`L12_T24_chunk004` completed as a target-timeseries replacement that was
already running when the selected-mass normal-cache optimization landed.  It
uses the original full FH/LSZ measurement shape rather than the optimized
selected-mass-only harness, but the output is production-phase,
seed-controlled under `numba_gauge_seed_v1`, and carries per-configuration
target time series for both same-source `dE/ds` and scalar `C_ss(q)` rows.

```text
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 4
# SUMMARY: PASS=14 FAIL=0
```

After refreshing the queue, target-series coverage was complete for
chunks001, 002, 003, 004, 011, and 012.  The remaining replacement queue was
therefore:

```text
replacement_queue = [5, 6, 7, 8, 9, 10]
next_replacement_chunk = 5
```

The optimized follow-on replacement policy is fixed-seed, chunk-isolated, and
does not use `--resume`, because old ready chunk artifacts can predate target
serialization.

## Claim Boundary

This is production-processing support only. It does not certify target ESS,
response stability, combined L12/L16/L24 production, scalar-pole derivative or
model-class control, FV/IR control, or canonical-Higgs identity. It does not
set `kappa_s = 1` and authorizes no retained or `proposed_retained` wording.

## Verification

```text
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 4
# SUMMARY: PASS=14 FAIL=0
python3 scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py
# SUMMARY: PASS=10 FAIL=0
python3 scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py
# SUMMARY: PASS=9 FAIL=0
python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=109 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=135 FAIL=0
```
