# PR #230 FH/LSZ Chunks013-016 Target-ESS Wave Checkpoint

**Status:** bounded-support / FH-LSZ target-observable ESS support
**Runners:** `scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py`, `scripts/frontier_yt_fh_lsz_target_observable_ess_certificate.py`, `scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py`
**Certificates:** `outputs/yt_fh_lsz_chunk013_target_timeseries_generic_checkpoint_2026-05-02.json` through `outputs/yt_fh_lsz_chunk016_target_timeseries_generic_checkpoint_2026-05-02.json`, `outputs/yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json`, `outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json`

## Result

The target-observable ESS certificate showed that chunks001-012 were below the
target-observable ESS threshold.  The campaign launched chunks013-016 with the
optimized selected-mass FH/LSZ and normal-cache harness, using fixed seeds,
chunk-isolated output directories, no `--resume`, and concurrency capped at
four workers.

The four chunks completed and passed the reusable target-timeseries
checkpoint:

```text
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 13
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 14
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 15
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 16
# each: SUMMARY: PASS=14 FAIL=0
```

The ready set is now chunks001-016:

```text
python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=9 FAIL=0
# present_chunks=16 ready_chunks=16 missing_chunks=47

python3 scripts/frontier_yt_fh_lsz_ready_chunk_set_checkpoint_certificate.py
# SUMMARY: PASS=8 FAIL=0
# available_saved_configurations=256 target_saved_configurations=1000

python3 scripts/frontier_yt_fh_lsz_target_observable_ess_certificate.py
# SUMMARY: PASS=8 FAIL=0
# limiting_target_ess=210.7849819291294
```

Response stability remains open:

```text
python3 scripts/frontier_yt_fh_lsz_ready_chunk_response_stability.py
# SUMMARY: PASS=6 FAIL=0
# n_chunks=16 relative_stdev=0.8943920916391181
# spread_ratio=5.476535332624479 relative_fit_error=8.121324509664896
```

## Claim Boundary

This wave is production-processing support only.  It does not certify a
combined L12 ensemble, L16/L24 scaling, scalar-pole derivative/model-class,
FV/IR/zero-mode control, or canonical-Higgs identity.  It does not derive or
set `kappa_s` and authorizes no retained or `proposed_retained` wording.

## Next Action

Do not treat target ESS as closure.  Continue the response-stability and
scalar-pole postprocess gates while prioritizing a canonical-Higgs identity
route: same-surface `O_H/C_sH/C_HH`, real W/Z response rows with
sector-overlap identity, or a retained rank-one neutral-scalar theorem.
