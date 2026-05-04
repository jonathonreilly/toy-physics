# PR #230 FH/LSZ Finite-Source-Linearity Calibration Checkpoint

**Status:** bounded-support / finite-source-linearity calibration checkpoint
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

The production calibration output landed:

- output: `outputs/yt_pr230_fh_lsz_finite_source_linearity_L12_T24_calib001_2026-05-02.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_linearity/L12_T24_calib001/L12xT24/ensemble_measurement.json`
- seed: `2026052001`
- runtime: `2995.968582868576` seconds
- source shifts: `[-0.015, -0.01, -0.005, 0.0, 0.005, 0.01, 0.015]`
- source radii: `[0.005, 0.01, 0.015]`

The checkpoint now records three symmetric finite-radius slope rows and a
zero-source intercept fit:

```text
S(0.005) = 1.4328455864415446 +/- 48.74105900530836
S(0.010) = 1.4328644399029145 +/- 24.780904478045105
S(0.015) = 1.4329053270860945 +/- 16.972844049142754

intercept = 1.4328344029594695 +/- 35.72880463605988
curvature = 0.31414156585863684 +/- 191445.24456861272
max fractional deviation from intercept = 4.94991790248229e-05
```

Verification:

```text
python3 scripts/frontier_yt_fh_lsz_finite_source_linearity_calibration_checkpoint.py
# SUMMARY: PASS=13 FAIL=0
```

Dependent gates were rerun:

```text
python3 scripts/frontier_yt_fh_lsz_response_window_acceptance_gate.py
# SUMMARY: PASS=12 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=140 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=166 FAIL=0
```

The response-window acceptance gate remains open.  The calibration checkpoint
is bounded support only because the parent finite-source-linearity gate does
not yet accept the response readout, production response stability is still
open, and the scalar LSZ/canonical-Higgs identity gates remain unresolved.

## Claim Boundary

This is response-window support only.  Even a passing multi-radius calibration
would not identify the scalar source with the canonical Higgs radial operator,
would not supply scalar LSZ pole control, would not derive `kappa_s`, and would
not authorize retained or `proposed_retained` top-Yukawa closure.

The runner does not use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0`, and it does not set `kappa_s = 1`,
`cos(theta) = 1`, `c2 = 1`, or `Z_match = 1`.
