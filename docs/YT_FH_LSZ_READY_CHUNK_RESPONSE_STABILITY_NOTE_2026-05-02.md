# PR #230 FH/LSZ Ready Chunk Response-Stability Diagnostic

**Status:** bounded-support / FH-LSZ ready chunk response-stability diagnostic
**Runner:** `scripts/frontier_yt_fh_lsz_ready_chunk_response_stability.py`
**Certificate:** `outputs/yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json`

## Result

The current seed-controlled ready set has twenty-six L12 chunks
`[1, 2, 3, ..., 24, 25, 26]`.  Their same-source top response slopes are finite,
but the fitted response surface remains unstable.  The newest v2 chunks have:

```text
chunk025: dE/ds = 1.421535070856338
chunk026: dE/ds = 1.4202420204986004
```

The partial set fails the diagnostic stability rule:

```text
n_chunks = 26
relative_stdev = 0.8963361077055534
spread_ratio = 5.920283844112204
relative_fit_error = 8.001618437516202
stability_rule = n >= 8, relative_stdev < 0.25, spread_ratio < 2
stability_passed = false
```

The fitted slope uncertainties are also too large for production-grade
response use at this stage.  This is expected for `26/63` L12 chunks and is a
reason to keep collecting chunks, not a physics closure.

The 2026-05-03 response-window forensics runner separates this from the target
time-series stability.  The fitted-slope central values have
`relative_stdev=0.8963361077055534`, while the tau=1 target diagnostic across
the same chunks has `relative_stdev=0.006279954340116946` and
`spread_ratio=1.0229374224682368`.  That is useful debugging support, but it
does not authorize switching the production response readout without a
predeclared response-window acceptance gate.

The response-window acceptance gate now records the next acceptance boundary.
Chunk-level tau-window central values are stable across tau windows 0-9, but
the gate remains open because per-configuration multi-tau covariance and
multiple source radii are absent.

## Claim Boundary

This diagnostic does not authorize retained or proposed-retained wording.  It
does not treat `dE/ds` as physical `dE/dh`, does not set `kappa_s = 1`, and
does not use observed target values, `H_unit`, Ward authority, `alpha_LM`,
plaquette, or `u0` as proof inputs.

Even a stable production slope would still need the scalar LSZ pole derivative,
model-class or pole-saturation control, FV/IR/zero-mode control, and
canonical-Higgs source-pole identity before physical `y_t` closure.

## Verification

```bash
python3 scripts/frontier_yt_fh_lsz_ready_chunk_response_stability.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_fh_lsz_response_window_forensics.py
# SUMMARY: PASS=10 FAIL=0

python3 scripts/frontier_yt_fh_lsz_response_window_acceptance_gate.py
# SUMMARY: PASS=12 FAIL=0
```
