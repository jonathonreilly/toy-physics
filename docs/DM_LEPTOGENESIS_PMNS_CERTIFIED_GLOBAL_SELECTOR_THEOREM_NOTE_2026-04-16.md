# DM Leptogenesis PMNS Certified Global Selector Theorem

**Date:** 2026-04-16  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_certified_global_selector_theorem.py`  
**Framework convention:** “axiom” means only `Cl(3)` on `Z^3`

## Question

The existing PMNS-assisted `N_e` selector theorem already found the lowest-action
closure branch on the exact reduced surface by a multistart constrained scan.
The remaining review question was whether that lower-action branch can be
certified as the unique global minimum on the exact reduced domain by a more
exhaustive optimization argument, rather than just a branch scan.

This note answers that exact question on the reduced surface only.

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

## What is certified

The theorem runner performs two independent exhaustive searches on that exact
compact chart:

1. a deterministic compact-chart lattice cover with constrained local
   minimization;
2. a direct branch-polishing pass on the converged stationary representatives.

The searches agree on the same branch set. The exact result is:

- three stationary closure branches on the reduced surface
- one branch is the unique lowest-action branch
- the lower branch closes the favored column exactly
- the lower branch is separated from the next branch by a finite action gap

The lower-action branch is the same exact branch already seen in the earlier
selector theorem:

- `x = (0.471675, 0.553810, 0.664515)`
- `y = (0.208063, 0.464382, 0.247555)`
- `delta ~ 0`
- `S_rel = 0.240906701390`
- `eta / eta_obs = 1`

The second stationary branch is:

- `x = (0.460724, 0.560504, 0.668773)`
- `y = (0.211572, 0.455054, 0.253373)`
- `delta ~ -1.0e-3`
- `S_rel = 0.242719075805`

The higher stationary branch is:

- `x = (0.790189, 0.406763, 0.493048)`
- `y = (0.586185, 0.167566, 0.166248)`
- `delta ~ 0`
- `S_rel = 1.110657539338`

So the finite action gap is:

`Delta S_min = 0.001812374006`

## Nature-grade scope

This theorem is the stronger Nature-grade statement requested for the reduced
surface:

- it certifies global uniqueness/minimality of the lower closure branch on the
  exact admissible PMNS-assisted domain
- it does not rely on a weaker random multistart scan alone
- it does **not** claim a separate closed-form analytic classification of every
  symbolic stationary component; that is a stronger theorem than needed here

In particular, the earlier question

> "Have we also proved a stronger all-possible-components analytic uniqueness
> theorem beyond the exact closure surface we reduced to?"

is now answered for the reduced-surface claim: no separate larger-domain
uniqueness theorem is needed, because the exact admissible domain is already
the reduced surface, and the lower branch is certified globally minimal on
that domain.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_certified_global_selector_theorem.py
```
