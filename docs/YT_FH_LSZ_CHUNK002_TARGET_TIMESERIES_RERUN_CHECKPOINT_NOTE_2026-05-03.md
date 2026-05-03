# PR #230 FH/LSZ Chunk002 Target-Timeseries Rerun Checkpoint

**Status:** bounded-support / FH-LSZ chunk002 target-timeseries replacement checkpoint  
**Runners:** `scripts/frontier_yt_fh_lsz_chunk002_checkpoint_certificate.py`, `scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py`, `scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py`, `scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py`  
**Certificates:** `outputs/yt_fh_lsz_chunk002_checkpoint_certificate_2026-05-02.json`, `outputs/yt_fh_lsz_chunk002_target_timeseries_generic_checkpoint_2026-05-02.json`, `outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json`, `outputs/yt_fh_lsz_target_timeseries_replacement_queue_2026-05-02.json`

## Result

`L12_T24_chunk002` was rerun without `--resume`, replacing the old
production-format artifact that lacked target time series.  The new output is
production-phase, seed-controlled under `numba_gauge_seed_v1`, and carries
per-configuration target time series for both same-source `dE/ds` and scalar
`C_ss(q)` rows.

```text
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 2
# SUMMARY: PASS=14 FAIL=0
```

The ready L12 set remains `12/63` chunks with `192/1000` saved configurations.
Target-series coverage is now complete for chunks001, 002, 011, and 012, but
still missing for chunks003-010. The refreshed replacement queue is therefore:

```text
replacement_queue = [3, 4, 5, 6, 7, 8, 9, 10]
next_replacement_chunk = 3
```

## Claim Boundary

This is production-processing support only. It does not certify target ESS,
response stability, combined L12/L16/L24 production, scalar-pole derivative or
model-class control, FV/IR control, or canonical-Higgs identity. It does not
set `kappa_s = 1` and authorizes no retained or `proposed_retained` wording.

## Verification

```text
python3 -m py_compile scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py scripts/frontier_yt_fh_lsz_chunk002_checkpoint_certificate.py scripts/frontier_yt_retained_closure_route_certificate.py scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_fh_lsz_chunk002_checkpoint_certificate.py
# SUMMARY: PASS=11 FAIL=0
python3 scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py
# SUMMARY: PASS=10 FAIL=0
python3 scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py
# SUMMARY: PASS=8 FAIL=0
python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=108 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=134 FAIL=0
```

