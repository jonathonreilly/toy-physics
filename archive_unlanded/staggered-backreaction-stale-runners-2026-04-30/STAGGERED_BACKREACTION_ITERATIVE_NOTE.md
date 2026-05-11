# Staggered Backreaction Iterative Source-Mapping Note

**Date:** 2026-04-10  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/staggered-backreaction-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/staggered-backreaction-stale-runners-2026-04-30/` (the directory name encodes the failure reason: stale staggered-backreaction runners)
- **Audit verdict_rationale (verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json) under claim_id `staggered_backreaction_iterative_note`):**

> Issue: The exact numerical result in the note is stale relative to scripts/frontier_staggered_backreaction_iterative.py. Current output gives baseline cycle-bearing mean gap 9.618e-01, best mean gap 4.314e-01 at invheat_b3p00, improvement 2.23x, baseline self-gap mean 3.822e-01, and best-map self-gap mean 1.581e+01; the note instead freezes baseline 8.899e-01, best 6.099e-01 at invheat_b2p00, improvement 1.46x, and best-map self-gap 2.275e+00. Why this blocks: the retained negative readout depends on the exact source-map ranking and gap table, and those values now identify a different best map and much larger self-update failure. Repair target: update the note from the current runner or restore the intended artifact, then add assertions for baseline gap, best-map identity, best gap, improvement factor, R^2, two-body residual, TOWARD counts, norm drift, and self-gap. Claim boundary until fixed: it is safe to claim that the current runner still finds no clean cycle-bearing closure from linear source preconditioning, with all rows TOWARD and stable but best self-gap exploding to 1.581e+01; it is not safe to retain the frozen invheat_b2p00 table or the stated 1.46x no-go numerics.

- **Do NOT cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a 'closed no-go'.

## Objective

Attack the endogenous-field scaling blocker in the staggered graph lane by
keeping the transport law fixed and varying only the source-to-field map.

The target was the force-scale gap between the solved graph field and the
external-kernel control on the cycle-bearing bipartite families.

## Harness

- Script: [`frontier_staggered_backreaction_iterative.py`](../scripts/frontier_staggered_backreaction_iterative.py)
- Families:
  - bipartite random geometric, `n=36`
  - bipartite growing, `n=48`
  - layered bipartite DAG-compatible, `n=36`
- Observable:
  - force `F = < -dPhi/dd >`
- Retained checks:
  - zero-source reduction
  - source-response linearity
  - two-body additivity
  - force sign
  - norm stability
  - one-step endogenous self-update

## Mappings Tested

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

All maps were linear operators on the source density.

## Exact Results

### Cycle-Bearing Families

| Mapping | Random geometric gap | Growing gap | Mean gap |
|---|---:|---:|---:|
| `gaussian` | `8.767e-01` | `9.032e-01` | `8.899e-01` |
| `lap1_b0p25` | `8.646e-01` | `8.904e-01` | `8.775e-01` |
| `lap2_b0p25` | `8.504e-01` | `8.749e-01` | `8.627e-01` |
| `lap1_b0p50` | `8.526e-01` | `8.776e-01` | `8.651e-01` |
| `lap2_b1p00` | `7.483e-01` | `7.616e-01` | `7.549e-01` |
| `invheat_b0p25` | `8.634e-01` | `8.888e-01` | `8.761e-01` |
| `invheat_b0p50` | `8.473e-01` | `8.708e-01` | `8.591e-01` |
| `invheat_b1p00` | `8.031e-01` | `8.185e-01` | `8.108e-01` |
| `invheat_b1p50` | `7.341e-01` | `7.318e-01` | `7.329e-01` |
| `invheat_b2p00` | `6.279e-01` | `5.919e-01` | `6.099e-01` |
| `invheat_b3p00` | `1.848e-01` | `1.055e+00` | `6.169e-01` |

Best cycle-bearing mean gap:

- `6.099e-01` with `invheat_b2p00`
- improvement over baseline: `1.46x`

### Layered DAG-Compatible Family

The layered family moved much closer under strong inverse-heat sharpening:

- `invheat_b1p50`: gap `1.605e-02`
- `invheat_b2p00`: gap `1.391e+00`
- `invheat_b3p00`: gap `1.330e+01`

That is a real structural asymmetry, but it does not rescue the cycle-bearing
families.

## Retained Checks

- Zero-source reduction stayed exact on every family and every mapping.
- Source-response linearity stayed exact to machine precision on the retained
  linear maps.
- Two-body additivity stayed exact to machine precision on the retained linear
  maps.
- Force remained TOWARD on every family for every mapping.
- Norm drift stayed at machine precision.

## Readout

The blocker is not a small normalization typo.

The strongest linear source preconditioner reduced the cycle-bearing force gap
from `8.899e-01` to `6.099e-01`, which is an improvement but not a material
closure. The one-step endogenous self-gap also got worse at the best map:

- baseline self-gap mean: `6.762e-01`
- best-map self-gap mean: `2.275e+00`

So the graph-solved field still does not land on the external-kernel force
scale in a way that looks structurally close.

## Interpretation

- Linear source sharpening helps a little.
- It does not solve the scale gap on cycle-bearing bipartite families.
- The transport law stays healthy.
- The missing piece is still the endogenous-field closure itself, not the
  observables.

## Next Step

Try a different source sector or a genuinely iterative endogenous closure rule,
not more linear source preconditioning.
