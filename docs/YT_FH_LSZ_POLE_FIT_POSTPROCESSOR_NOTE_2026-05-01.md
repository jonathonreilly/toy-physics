# PR #230 FH/LSZ Scalar-Pole Fit Postprocessor Scaffold

**Status:** bounded-support / FH-LSZ scalar-pole fit postprocessor scaffold
**Runner:** `scripts/frontier_yt_fh_lsz_pole_fit_postprocessor.py`
**Certificate:** `outputs/yt_fh_lsz_pole_fit_postprocessor_2026-05-01.json`

## Purpose

The FH/LSZ production route needs a concrete postprocess step after chunk
combination.  This runner defines that step without treating absent or partial
data as evidence.

## Readiness Gate

The postprocessor requires:

- combined same-source production output;
- zero momentum plus at least three positive `p_hat^2` shells;
- finite `Gamma_ss(q)` rows for the same source used in `dE_top/ds`;
- an isolated negative-`p_hat^2` pole from the fit;
- finite `dGamma_ss/dp^2` at that pole.

The current input is absent/nonready, so the runner writes an open bounded
support certificate only.

## Claim Boundary

```text
proposal_allowed: false
```

This does not set `kappa_s = 1` and does not use `H_unit`, Ward authority,
observed target values, alpha/plaquette inputs, or reduced pilots.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_pole_fit_postprocessor.py
python3 scripts/frontier_yt_fh_lsz_pole_fit_postprocessor.py
# SUMMARY: PASS=5 FAIL=0
```
