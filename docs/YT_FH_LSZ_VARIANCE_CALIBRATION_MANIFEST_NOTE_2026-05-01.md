# PR #230 FH/LSZ Variance Calibration Manifest

**Status:** bounded-support / FH-LSZ variance calibration manifest  
**Runner:** `scripts/frontier_yt_fh_lsz_variance_calibration_manifest.py`  
**Certificate:** `outputs/yt_fh_lsz_variance_calibration_manifest_2026-05-01.json`

## Question

What exact production-facing calibration would test whether eight scalar-LSZ
noise vectors are adequate for the pole-fit mode set?

## Result

The manifest emits a paired L12 calibration:

```text
x8:  eight modes, eight noises
x16: eight modes, sixteen noises
```

The pair matches volume, selected mass, source shifts, scalar-LSZ modes, seed,
thermalization, measurements, and separation.  The only allowed differences
are scalar-LSZ noise count, output path, and production artifact directory.

This gives the next executable calibration surface for the variance gate.  It
does not run the calibration and does not provide production evidence.

## Claim Boundary

```text
proposal_allowed: false
```

The manifest is launch planning only.  It does not pass the eight-mode variance
gate, does not derive `kappa_s`, and does not supply scalar pole data.

## Exact Next Action

If pursuing the x8 foreground route, run both calibration commands to
completion, then compare same-mode `C_ss(q)`, `Gamma_ss(q)`, and pole-derivative
stability using the `noise_subsample_stability` fields.  Otherwise keep the
x16 noise plan and schedule outside the 12-hour foreground window.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_variance_calibration_manifest.py
python3 scripts/frontier_yt_fh_lsz_variance_calibration_manifest.py
# SUMMARY: PASS=9 FAIL=0
```
