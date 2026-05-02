# PR #230 FH/LSZ Chunk002 Production Checkpoint

**Status:** bounded-support / FH-LSZ chunk002 production checkpoint seed-invalid diagnostic
**Runner:** `scripts/frontier_yt_fh_lsz_chunk002_checkpoint_certificate.py`
**Certificate:** `outputs/yt_fh_lsz_chunk002_checkpoint_certificate_2026-05-02.json`

## Claim

Historical `L12_T24` chunk002 completed with production-phase metadata,
same-source `dE/ds`, and four-mode/x16 same-source scalar `C_ss(q)` rows.

The chunk combiner now sees two chunks present and one ready chunk after the
seed-independence gate: replacement chunk001 is ready, while historical
chunk002 lacks the `numba_gauge_seed_v1` marker and remains seed-invalid.  The
checkpoint runner now handles both states: the current historical diagnostic
and a future replacement chunk002 once it records valid seed-control metadata.

## Boundary

This is seed-invalid bounded production support only.  It does not supply an
independent L12 chunk, a combined L12 summary, L16/L24 scaling, isolated
scalar-pole derivative, model-class certificate, FV/IR/zero-mode control, or
retained-proposal gate.

## Verification

```bash
python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk002_checkpoint_certificate.py
# SUMMARY: PASS=11 FAIL=0
```
