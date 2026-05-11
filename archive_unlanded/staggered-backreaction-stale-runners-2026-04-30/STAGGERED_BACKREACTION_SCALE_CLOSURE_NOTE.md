# Staggered Backreaction Scale-Closure Note

**Date:** 2026-04-10  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/staggered-backreaction-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/staggered-backreaction-stale-runners-2026-04-30/` (the directory name encodes the failure reason: stale staggered-backreaction runners)
- **Audit verdict_rationale (verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json) under claim_id `staggered_backreaction_scale_closure_note`):**

> Issue: The frozen scale-closure table is stale relative to scripts/frontier_staggered_backreaction_scale_closure.py. Current output gives best map invheat_b3p00, gain 0.621, raw cycle gap 4.314e-01, calibrated cycle gap 2.053e-01, improvement 4.69x, best holdout gap 7.249e+00, and source-response R^2 mean 0.9945; the note claims invheat_b1p00, gain 5.374, calibrated cycle gap 5.869e-02, improvement 15.16x, holdout 1.678e+00, and R^2 mean 0.9998. Why this blocks: the candidate retained-grade scale-closure claim is exactly about the best calibrated map and size of the force-scale closure, and the current runner shows a much weaker closure with a different map and severe holdout divergence. Repair target: update the note from the current runner or restore the historical artifact, then add assertions for best map identity, fitted gain, raw/calibrated cycle gaps, improvement factor, holdout gap, self-gap, R^2, two-body residual, TOWARD count, and norm drift. Claim boundary until fixed: it is safe to claim that the current runner finds a 4.69x calibrated cycle-gap reduction with checks still passing, but no universal scale closure because the best holdout gap is 7.249e+00; it is not safe to retain the frozen 15.16x invheat_b1p00 closure claim.

- **Do NOT cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a 'closed no-go'.

## Question

Can a single linear normalization of the source-generated `Phi` materially
close the force-scale gap to the external-kernel control on the cycle-bearing
bipartite graph families, while preserving the retained staggered checks?

## Harness

- Script: [`frontier_staggered_backreaction_scale_closure.py`](../scripts/frontier_staggered_backreaction_scale_closure.py)
- Families:
  - bipartite random geometric, `n=36`
  - bipartite growing, `n=48`
  - layered bipartite DAG-compatible, `n=36` holdout
- Mappings searched:
  - `gaussian`
  - `lap1_b0p25`
  - `lap2_b0p25`
  - `lap1_b0p50`
  - `lap2_b1p00`
  - `invheat_b0p25`
  - `invheat_b0p50`
  - `invheat_b1p00`
  - `invheat_b1p50`
  - `invheat_b2p00`
  - `invheat_b3p00`
- Observable:
  - force `F = < -dPhi/dd >`
- Fit:
  - one global scalar gain per mapping, fitted on the cycle-bearing families only

## Exact Results

### Best Calibration

The best cycle-bearing closure came from `invheat_b1p00`:

- fitted gain: `5.374`
- raw cycle-bearing mean gap: `8.899e-01`
- calibrated cycle-bearing mean gap: `5.869e-02`
- improvement factor: `15.16x`

Family-level retained checks stayed intact under the calibrated map:

- source-response linearity mean `R² = 0.9998`
- two-body residual max `3.011e-16`
- minimum TOWARD count `3/3`
- norm drift max `7.772e-16`

### Raw vs Calibrated Summary

| Mapping | Gain | Raw cycle gap | Cal cycle gap | Raw holdout gap | Cal holdout gap |
|---|---:|---:|---:|---:|---:|
| `invheat_b1p00` | `5.374` | `8.108e-01` | `5.869e-02` | `5.257e-01` | `1.678e+00` |
| `lap2_b1p00` | `4.128` | `7.550e-01` | `5.906e-02` | `3.584e-01` | `1.788e+00` |
| `invheat_b1p50` | `3.737` | `7.329e-01` | `9.727e-02` | `1.605e-02` | `3.127e+00` |
| `invheat_b2p00` | `2.508` | `6.099e-01` | `9.759e-02` | `1.391e+00` | `5.256e+00` |
| `gaussian` | `9.476` | `8.899e-01` | `1.358e-01` | `8.759e-01` | `1.809e-01` |

## Readout

- The blocker is **not** a small normalization typo on the cycle-bearing
  families.
- A single gain does materially reduce the cycle-bearing force gap, from
  `8.899e-01` to `5.869e-02`.
- That is a real reduction, but the best cycle-bearing calibration does not
  transfer cleanly to the layered DAG holdout.
- The holdout divergence is the important residual: the normalization is not
  yet universal across cycle-bearing and DAG-compatible families.

## Interpretation

- The staggered transport law remains healthy:
  - TOWARD sign preserved
  - linearity preserved
  - two-body additivity preserved
  - norm stability preserved
- The force-scale mismatch has a significant normalization component.
- But the cycle-bearing families and the DAG-compatible holdout are not yet
  governed by one universal source-to-field scale.

## Next Step

- Try a genuinely endogenous update rule or a family-aware normalization that
  closes the cycle-bearing gap without degrading the DAG holdout.
- Keep the retained battery fixed while testing whether the source sector
  itself needs a graph-class-dependent normalization.
