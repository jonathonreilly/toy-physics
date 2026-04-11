# Ollivier Curvature Proxy Note

**Date:** 2026-04-11  
**Lane:** staggered bounded side probe  
**Status:** bounded-retained proxy result with explicit caveats

## Bottom line

On the screened `10x10` periodic staggered torus, the **potential-weighted**
Ollivier curvature observable shows a strong edgewise relation

- `Delta_kappa ~ G * T`

after the validated wraparound-weight bug is fixed in the lane-local runners.

What survives:

- the signal is **not** reproduced by random-`Phi` controls matched in mean/std
- the signal is **not** reproduced by shuffled self-consistent `Phi`
- the relation is stable across `G = 1, 5, 10, 20, 50`

What does **not** survive:

- the density-weighted and combined curvature definitions do **not** show a
  comparably strong relation
- the result does **not** justify a direct “Einstein equation derived” claim
- dynamic backreaction is only **partially** isolated, because a fixed
  `Phi` sourced by the initial packet reproduces an increasing fraction of the
  same signal and is essentially indistinguishable at `G = 50`

## Audited runners

- [`scripts/frontier_ollivier_einstein.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_ollivier_einstein.py)
- [`scripts/frontier_ollivier_control.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_ollivier_control.py)

Both runners were updated to use the correct minimum-image torus distance for
periodic wraparound hopping weights before rerun.

## Rerun summary

### Main runner

Using the corrected periodic metric, the three curvature definitions give:

- `density`: mean `R^2(Delta_kappa, G*T) = 0.1481`
- `potential`: mean `R^2(Delta_kappa, G*T) = 0.9728`
- `combined`: mean `R^2(Delta_kappa, G*T) = 0.1742`

So the lane only works on the **potential-weighted** metric construction.

### Controls

For the same corrected surface, the control runner gives mean
`R^2(Delta_kappa, G*T)` across `G = 1, 5, 10, 20, 50`:

- `self_consistent`: `0.9728`
- `static_initial`: `0.4656`
- `random_matched`: `0.0030`
- `shuffled`: `0.0033`

Interpretation:

- random/shuffled `Phi` controls collapse, so the signal is not a trivial
  “any matched variance potential works” artifact
- a **structured fixed** `Phi` sourced by the initial packet carries a real
  part of the same signal, and this share grows with `G`
- therefore the clean statement is:

> the potential-weighted Ollivier observable is a **bounded linearized
> curvature-density proxy** on this surface, with dynamic self-consistency
> helping at weak/moderate coupling but not uniquely determining the strong
> coupling result

## Why this is bounded, not headline

This lane still has several important caveats:

- it lives on a screened (`mu^2 = 0.22`) periodic torus
- it uses an **effective metric definition** `d_eff = 1 + Phi_avg + offset`,
  not a standard graph-geometric Einstein derivation
- the successful signal is method-specific
- the static-initial control shows that “structured positive potential” already
  explains a substantial part of the effect
- there is no open-boundary / unscreened / Wilson cross-check yet

## Honest retained claim

The retainable claim is:

> On the audited screened periodic staggered torus, a **potential-weighted
> Ollivier curvature proxy** tracks `G*T` strongly and decisively beats
> random/shuffled controls, but it remains a **bounded proxy result** rather
> than an Einstein-equation derivation because the signal is method-specific
> and a static initial-source potential reproduces an increasing fraction of it.

## What needs further work

Before any stronger claim, this lane needs:

1. an unscreened / low-`mu^2` rerun of the same proxy
2. an open-boundary or Wilson-style comparison surface
3. a control that preserves smooth radial structure but breaks the exact
   self-consistent update
4. a justification for why the potential-weighted Ollivier metric should be the
   physically preferred curvature observable here
