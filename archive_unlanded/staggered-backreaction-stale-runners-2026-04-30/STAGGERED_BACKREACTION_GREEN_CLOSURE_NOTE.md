# Staggered Backreaction Green-Closure Note

**Date:** 2026-04-10  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/staggered-backreaction-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/staggered-backreaction-stale-runners-2026-04-30/` (the directory name encodes the failure reason: stale staggered-backreaction runners)
- **Audit verdict_rationale (verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json) under claim_id `staggered_backreaction_green_closure_note`):**

> Issue: the archived source note is stale relative to the live Green-closure runner, and the stale fields are exactly the claimed force-scale closure and holdout-transfer numbers. Why this blocks: a hostile physicist can no longer claim nearly order-of-magnitude cycle closure or clean calibrated holdout transfer, because the current runner gives only a 2.81x raw cycle improvement over screened_poisson and the calibrated layered holdout gap blows up to 5.371e-01 rather than 3.714e-03. Repair target: either restore the old runner/environment that generated the note's table, or update the note to the current runner output and rerun the comparison with hard assertions for the intended acceptance gates, including raw/calibrated cycle gaps, raw/calibrated holdout gaps, gain, retained checks, and self-gap. Claim boundary until fixed: it is safe to claim only that the current resistance_yukawa runner is the best of the three frozen maps by its balance score, preserves source-linearity/additivity/TOWARD/norm checks, improves the raw cycle gap from 9.618e-01 to 3.425e-01, and has a small raw holdout gap of 1.534e-02; it is not safe to retain the note's stronger Green-closure or clean calibrated-holdout claim.

- **Do NOT cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a 'closed no-go'.

## Question

Can a genuinely nonlocal graph-native Green map close the endogenous-field
force-scale gap on the retained cycle-bearing bipartite families, while still
transferring to one layered holdout and preserving the retained force battery?

## Harness

- Script:
  [`frontier_staggered_backreaction_green_closure.py`](../scripts/frontier_staggered_backreaction_green_closure.py)
- Families:
  - bipartite random geometric, `n=36`
  - bipartite growing, `n=48`
  - layered bipartite DAG-compatible, `n=36` holdout
- Observable:
  - force `F = < -dPhi/dd >`
- Retained checks:
  - zero-source exactness
  - source-response linearity
  - two-body additivity
  - inward retained proxy sign under the prescribed attractive coupling
  - norm stability
- Frozen field maps:
  - `screened_poisson` baseline
  - `geodesic_yukawa(mu=1.50, eps=0.10)`
  - `resistance_yukawa(mu=1.50, eps=0.10)`

## Exact Results

### Holdout-Aware Winner

The promoted graph-native map is `resistance_yukawa`.

- cycle-bearing mean gap, raw: `9.889e-02`
- cycle-bearing mean gap, fitted: `9.688e-02`
- layered holdout gap, raw: `1.680e-02`
- layered holdout gap, fitted: `3.714e-03`
- cycle-only fitted gain: `0.980`

Against the screened graph-Poisson baseline:

- baseline cycle-bearing mean gap: `8.899e-01`
- baseline layered holdout gap: `8.759e-01`
- raw cycle-bearing improvement factor: `9.00x`
- raw holdout improvement factor: `52.13x`

### Frozen Comparison

| Mapping | Gain | Raw cycle gap | Cal cycle gap | Raw holdout gap | Cal holdout gap |
|---|---:|---:|---:|---:|---:|
| `resistance_yukawa` | `0.980` | `9.889e-02` | `9.688e-02` | `1.680e-02` | `3.714e-03` |
| `geodesic_yukawa` | `0.958` | `1.004e-01` | `9.605e-02` | `2.267e-02` | `2.103e-02` |
| `screened_poisson` | `9.476` | `8.899e-01` | `1.358e-01` | `8.759e-01` | `1.809e-01` |

### Retained Checks

For the promoted `resistance_yukawa` map:

- source-response `R²` min / mean: `0.9978 / 0.9989`
- two-body residual max: `3.063e-16`
- minimum inward proxy count: `3/3`
- norm drift max: `7.772e-16`

Family-level calibrated gaps:

- bipartite random geometric: `1.322e-01`
- bipartite growing: `6.151e-02`
- layered holdout: `3.714e-03`

## Readout

- The scale blocker is not just a missing Poisson normalization.
- A direct nonlocal Green map closes the force scale on the retained
  cycle-bearing families by nearly an order of magnitude.
- That closure transfers cleanly to the layered holdout; unlike the earlier
  gain-only closure, the holdout does not blow up.
- The fitted gain sits near `1`, so the promoted map is already close to the
  correct force scale before any cycle-only calibration.

## Interpretation

- The retained structural interaction battery survives the promoted nonlocal
  field map.
- Effective-resistance distance is the cleanest graph-native metric in this
  frozen comparison.
- The next open seam is no longer the raw source-to-field scale on this small
  retained set. It is self-consistent endogenous refresh:
  the promoted cycle-bearing mean self-gap is still `1.036e+00`.

## Next Step

- Keep `resistance_yukawa` as the source-sector closure baseline for this
  staggered graph lane.
- Attack the one-step self-refresh gap directly, rather than reopening local
  source-preconditioner sweeps.
