# PR #230 FH/LSZ Paired Variance Calibration Gate

**Status:** open / paired x8/x16 variance calibration awaiting production outputs  
**Runner:** `scripts/frontier_yt_fh_lsz_paired_variance_calibration_gate.py`  
**Certificate:** `outputs/yt_fh_lsz_paired_variance_calibration_gate_2026-05-04.json`

## Purpose

The pole-fit mode budget found an eight-mode/eight-noise L12 launch shape that
can fit the foreground chunk budget, but lowering the scalar-LSZ stochastic
noise count from x16 to x8 is not evidence until the same source coordinate is
calibrated.

This gate consumes the paired x8/x16 variance-calibration manifest and checks
the future outputs under one contract:

- both outputs must be production phase;
- run controls must match except for scalar noise count and artifact
  directory;
- both outputs must contain exactly the eight pole-fit scalar-LSZ modes;
- each mode must have at least 16 configurations and noise-subsample
  diagnostics;
- `C_ss(q)` and `Gamma_ss(q)` must be stable between x8 and x16 under the
  recorded z-score and relative-delta thresholds.

## Current Result

The paired calibration outputs are absent, so x8 remains unaccepted.  The
useful progress is contract-level: a future calibration wave will either pass
or fail this gate directly instead of landing as an orphan output that the old
variance gate cannot consume.

Verification:

```bash
python3 scripts/frontier_yt_fh_lsz_paired_variance_calibration_gate.py
# SUMMARY: PASS=8 FAIL=0
```

## Claim Boundary

This is launch support only.  It does not derive scalar LSZ normalization,
does not provide physical `y_t`, does not set `kappa_s`, `c2`, `Z_match`, or
`cos(theta)` to one, and does not use `H_unit`, `yt_ward_identity`, observed
targets, `alpha_LM`, plaquette, or `u0`.
