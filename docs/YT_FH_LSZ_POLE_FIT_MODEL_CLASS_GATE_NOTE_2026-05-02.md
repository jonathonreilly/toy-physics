# PR #230 FH/LSZ Pole-Fit Model-Class Gate

**Status:** open / FH-LSZ pole-fit model-class gate blocks finite-shell fit as evidence
**Runner:** `scripts/frontier_yt_fh_lsz_pole_fit_model_class_gate.py`
**Certificate:** `outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json`

## Purpose

The finite-shell identifiability no-go shows that a finite set of Euclidean
`Gamma_ss(p^2)` shell rows does not determine the pole derivative.  This gate
makes that boundary executable.

## Acceptance Rule

A future FH/LSZ pole-fit result is not load-bearing retained evidence unless it
has:

- combined production same-source FH/LSZ output;
- postprocessor readiness;
- a model-class, analytic-continuation, pole-saturation, continuum, or
  microscopic scalar-denominator certificate that excludes shell-vanishing
  derivative deformations.

The current surface has no production fit and no model-class certificate, so
the gate blocks retained/proposed-retained wording.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_pole_fit_model_class_gate.py
python3 scripts/frontier_yt_fh_lsz_pole_fit_model_class_gate.py
# SUMMARY: PASS=6 FAIL=0
```
