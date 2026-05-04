# PR #230 FH/LSZ Finite-Source-Linearity Calibration Checkpoint

**Status:** open / finite-source-linearity calibration awaiting output  
**Runner:** `scripts/frontier_yt_fh_lsz_finite_source_linearity_calibration_checkpoint.py`  
**Certificate:** `outputs/yt_fh_lsz_finite_source_linearity_calibration_checkpoint_2026-05-03.json`

## Purpose

The current FH/LSZ response-window gate blocks because the production chunks
use a single nonzero scalar source radius.  That is not enough to certify that
the finite symmetric source shift is the zero-source Feynman-Hellmann
derivative.

This checkpoint consumes a multi-radius calibration run when it exists:

```text
s in {-0.015, -0.010, -0.005, 0.0, 0.005, 0.010, 0.015}
```

For each nonzero radius it forms

```text
S(delta) = [E(+delta) - E(-delta)] / (2 delta)
```

and fits

```text
S(delta) = intercept + curvature * delta^2
```

to test whether the source-coordinate response has a controlled zero-source
intercept.

## Current Result

The production calibration job is still running, so the checkpoint currently
records the output as absent and keeps the response-window surface open:

```text
python3 scripts/frontier_yt_fh_lsz_finite_source_linearity_calibration_checkpoint.py
# SUMMARY: PASS=7 FAIL=0
```

When the calibration output lands, rerun this checkpoint, then rerun the
response-window acceptance, retained-route, and campaign-status certificates.

## Claim Boundary

This is response-window support only.  Even a passing multi-radius calibration
would not identify the scalar source with the canonical Higgs radial operator,
would not supply scalar LSZ pole control, would not derive `kappa_s`, and would
not authorize retained or `proposed_retained` top-Yukawa closure.

The runner does not use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0`, and it does not set `kappa_s = 1`,
`cos(theta) = 1`, `c2 = 1`, or `Z_match = 1`.
