# PR #230 FH/LSZ Ready Chunk-Set Production Checkpoint

**Status:** bounded-support / FH-LSZ complete L12 ready chunk-set checkpoint
**Runner:** `scripts/frontier_yt_fh_lsz_ready_chunk_set_checkpoint_certificate.py`
**Certificate:** `outputs/yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json`

## Result

The ready-set checkpoint is dynamic: it derives `ready_chunk_indices` from the
combiner gate rather than hardcoding a fixed chunk range. It accepts both
partial and complete L12 support states without treating either as physical
`y_t` closure. After the chunks061-063 final wave, the seed-controlled
`L12_T24` FH/LSZ ready set contains chunks001-063:

```text
ready_chunk_indices = [1, 2, 3, ..., 24, 25, 26]
present_chunks = 63
ready_chunks = 63
expected_chunks = 63
available_saved_configurations = 1008
target_saved_configurations = 1000
```

Each ready chunk has production-phase run-control metadata, chunk-local output
directories, `numba_gauge_seed_v1` gauge seed-control metadata, same-source
top `dE/ds`, and same-source scalar `C_ss(q)` / `Gamma_ss(q)` rows for the
four-mode, sixteen-noise plan.

The combiner has also written the complete L12 support summary consumed by the
pole-fit postprocessor:

```text
outputs/yt_pr230_fh_lsz_production_L12_T24_chunked_combined_2026-05-01.json
```

The response-stability, target ESS, response-window, v2 target-stability,
pole-fit postprocessor, retained-route, and campaign certificates consume this
dynamic ready set.

## Claim Boundary

This is bounded production support only. It does not authorize retained or
proposed-retained wording. The current surface has a complete L12 support
summary, but still lacks L16/L24 scaling, an isolated scalar-pole inverse-
derivative fit, model-class or pole-saturation control, FV/IR/zero-mode
control, and the canonical-Higgs identity needed to turn the source pole into
physical `y_t`.

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
