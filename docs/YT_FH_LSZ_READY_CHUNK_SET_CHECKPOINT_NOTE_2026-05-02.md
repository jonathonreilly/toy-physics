# PR #230 FH/LSZ Ready Chunk-Set Production Checkpoint

**Status:** bounded-support / FH-LSZ ready chunk-set production checkpoint
**Runner:** `scripts/frontier_yt_fh_lsz_ready_chunk_set_checkpoint_certificate.py`
**Certificate:** `outputs/yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json`

## Result

The ready-set checkpoint is now dynamic: it derives `ready_chunk_indices` from
the combiner gate rather than hardcoding a fixed chunk range.  It also accepts
non-contiguous ready sets, because chunk completion order need not be
sequential.  After chunk012 and the chunk001 target-series replacement, the
seed-controlled `L12_T24` FH/LSZ ready set contains chunks001-012:

```text
ready_chunk_indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
present_chunks = 12
ready_chunks = 12
expected_chunks = 63
available_saved_configurations = 192
target_saved_configurations = 1000
```

Each ready chunk has production-phase run-control metadata, chunk-local output
directories, `numba_gauge_seed_v1` gauge seed-control metadata, same-source
top `dE/ds`, and same-source scalar `C_ss(q)` / `Gamma_ss(q)` rows for the
four-mode, sixteen-noise plan.

When later chunks finish, rerunning this certificate will include every
combiner-ready seed-controlled chunk in `ready_chunk_indices`, and the
response-stability diagnostic will consume that dynamic set.

## Claim Boundary

This is bounded production support only.  It does not authorize retained or
proposed-retained wording.  The current surface still lacks a combined L12
ensemble, L16/L24 scaling, an isolated scalar-pole inverse-derivative fit,
model-class or pole-saturation control, FV/IR/zero-mode control, and the
canonical-Higgs identity needed to turn the source pole into physical `y_t`.

The checkpoint also keeps the claim firewall explicit: it does not set
`kappa_s = 1`, does not use `H_unit`, Ward authority, observed target values,
`alpha_LM`, plaquette, or `u0` as proof inputs, and does not treat source
response as a physical Higgs readout.

## Verification

```bash
python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_fh_lsz_ready_chunk_set_checkpoint_certificate.py
# SUMMARY: PASS=8 FAIL=0
```
