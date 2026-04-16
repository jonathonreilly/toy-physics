# DM Leptogenesis PMNS Reduced-Surface Selector Support

**Date:** 2026-04-16
**Script:** `scripts/frontier_dm_leptogenesis_pmns_reduced_surface_selector_support.py`
**Framework convention:** “axiom” means only `Cl(3)` on `Z^3`

## Question

The existing PMNS-assisted `N_e` selector support had already found a
lowest-action closure branch on the exact reduced surface, but earlier support
machinery still depended on previously known branch seeds. The remaining review
question was whether the low-action branch can still be recovered by a stronger
anchor-free global search on the exact reduced domain.

This note answers that question on the reduced surface only, but it remains
strong optimization support rather than a live theorem-grade certification.

## What the reduced domain is

The reduction-exhaustion theorem already eliminated all admissible closure
components beyond the fixed native `N_e` seed surface. On that exact domain we
use the compact chart

`(u_1, u_2, v_1, v_2, delta) in [0,1]^4 x [-pi, pi]`

with

`x = 3 XBAR_NE * (u_1, (1-u_1)u_2, (1-u_1)(1-u_2))`

`y = 3 YBAR_NE * (v_1, (1-v_1)v_2, (1-v_1)(1-v_2))`

This chart is exact and surjective onto the fixed native `N_e` seed surface.
So a global optimization over this compact chart is already a global
optimization over the admissible PMNS-assisted closure domain.

## What is supported

The runner performs an anchor-free deterministic global optimization on that
exact compact chart, followed by local polishing.

1. a deterministic Sobol / SHGO global search on the full compact reduced
   chart with the exact closure constraint;
2. a direct local branch-polishing pass on the resulting stationary
   representatives.

The anchor-free search recovers a finite three-branch reduced-surface set with
a unique lowest-action branch. The support result is:

- three stationary closure branches on the reduced surface
- one branch is the unique lowest-action branch in the current reduced-surface search
- the lower branch closes the favored column exactly
- the lower branch is separated from the next branch by a finite action gap

The lower-action branch is:

- `x = (0.471678, 0.553804, 0.664518)`
- `y = (0.208061, 0.464382, 0.247557)`
- `delta ~ 0`
- `S_rel = 0.240906701926`
- `eta / eta_obs = 1`

The second stationary branch is:

- `x = (0.790189, 0.406763, 0.493048)`
- `y = (0.586185, 0.167566, 0.166248)`
- `delta ~ 0`
- `S_rel = 1.110657539337`

The higher stationary branch is:

- `x = (0.734928, 0.402194, 0.552878)`
- `y = (0.552002, 0.322360, 0.045638)`
- `delta ~ pi`
- `S_rel = 1.465909517428`

So the finite action gap is:

`Delta S_min = 0.869750837412`

## Scope

This file is kept as **support** rather than live theorem authority because
the current result is still a numerical global optimization support argument,
not a certified interval/global proof. So the safe live statement is:

- the reduced-surface search support consistently recovers a three-branch
  stationary set with an anchor-free global search
- the low branch remains separated by a finite action gap
- this materially strengthens the PMNS-assisted route
- it is not yet promoted here as a theorem-grade global selector certificate

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_reduced_surface_selector_support.py
```
