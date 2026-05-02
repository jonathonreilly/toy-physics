# PR #230 Same-Source Pole-Data Sufficiency Gate

**Status:** open / same-source pole-data sufficiency gate not passed  
**Runner:** `scripts/frontier_yt_same_source_pole_data_sufficiency_gate.py`  
**Certificate:** `outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json`

## Result

This block records the positive-side FH/LSZ closure condition.

If the same scalar source supplies both the top response and scalar two-point
pole data, then the source-coordinate normalization cancels in

```text
y_proxy = (dE_top/ds) * sqrt(D'_ss(pole))
```

under `O_s -> c O_s` because `dE/ds -> c dE/ds` and
`D'_ss -> D'_ss / c^2`.  This is the honest route around `kappa_s = 1`: measure
the pole derivative for the same source.

## Current Gate

The gate is not passed on the current PR #230 surface:

- ready L12 chunks are only `6/63`;
- response stability is not production-grade;
- the postprocess gate has no accepted production pole derivative;
- finite-shell model-class / pole-saturation control is not passed;
- the measured source pole is not certified as the canonical Higgs radial mode.

## Verification

```bash
python3 scripts/frontier_yt_same_source_pole_data_sufficiency_gate.py
# SUMMARY: PASS=11 FAIL=0
```

## Claim Boundary

This is support, not retained or proposed-retained `y_t` closure.  It does not
license `kappa_s = 1`, reduced/partial chunks as production evidence, `H_unit`
readout, `yt_ward_identity` authority, observed top mass/yukawa proof
selection, or alpha/plaquette/u0 proof input.

