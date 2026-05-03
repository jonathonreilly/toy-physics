# PR #230 FH/LSZ Chunk002 Production Checkpoint

**Status:** bounded-support / FH-LSZ chunk002 seed-controlled production checkpoint
**Runner:** `scripts/frontier_yt_fh_lsz_chunk002_checkpoint_certificate.py`
**Certificate:** `outputs/yt_fh_lsz_chunk002_checkpoint_certificate_2026-05-02.json`

## Claim

Replacement `L12_T24` chunk002 completed with production-phase metadata,
same-source `dE/ds`, four-mode/x16 same-source scalar `C_ss(q)` rows, and
`numba_gauge_seed_v1` seed-control metadata.  The 2026-05-03 rerun replaced
the older production-format artifact and now also serializes per-configuration
target time series for same-source `dE/ds` and scalar `C_ss(q)`.

The chunk combiner now sees twelve chunks present and twelve ready chunks
after the seed-independence gate: chunks001-012 are seed-controlled and ready,
but the L12 set is still only `12/63` complete. Target-series coverage is now
complete for chunks001, 002, 011, and 012; chunks003-010 remain in the
replacement queue.

## Boundary

This is bounded production support only.  It does not supply a combined L12
summary, L16/L24 scaling, isolated scalar-pole derivative, model-class
certificate, FV/IR/zero-mode control, or retained-proposal gate.

## Verification

```bash
python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk002_checkpoint_certificate.py
# SUMMARY: PASS=11 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 2
# SUMMARY: PASS=14 FAIL=0
```
