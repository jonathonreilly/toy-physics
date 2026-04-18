# Ollivier Curvature Proxy Note

**Date:** 2026-04-11  
**Lane:** staggered bounded side probe  
**Status:** bounded companion structured-curvature proxy with explicit caveats

## Bottom line

On the audited `10x10` periodic staggered torus, the **potential-weighted**
Ollivier curvature observable shows a strong edgewise relation

- `Delta_kappa ~ G * T`

after the validated wraparound-weight bug is fixed in the lane-local runners.

What survives:

- the signal survives both the screened run (`mu^2 = 0.22`) and the
  low-screening rerun (`mu^2 = 0.001`)
- the signal is **not** reproduced by random-`Phi` controls matched in mean/std
- the signal is **not** reproduced by shuffled self-consistent `Phi`
- the relation is stable across `G = 1, 5, 10, 20, 50`

What does **not** survive:

- the density-weighted and combined curvature definitions do **not** show a
  comparably strong relation
- the result does **not** justify a direct “Einstein equation derived” claim
- dynamic backreaction is only **partially** isolated, because both a fixed
  `Phi` sourced by the initial packet and a smooth shell-averaged `Phi`
  reproduce a large fraction of the same signal
- in the low-screening run, the shell-averaged control is nearly identical to
  the self-consistent result, so the strongest honest read is
  **structured-curvature proxy**, not Einstein-equation closure

## Audited runners

- [`scripts/frontier_ollivier_einstein.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_ollivier_einstein.py)
- [`scripts/frontier_ollivier_control.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_ollivier_control.py)

Both runners were updated to use the correct minimum-image torus distance for
periodic wraparound hopping weights before rerun.

## Rerun summary

### Screened run (`mu^2 = 0.22`)

Using the corrected periodic metric, the three curvature definitions give:

- `density`: mean `R^2(Delta_kappa, G*T) = 0.1481`
- `potential`: mean `R^2(Delta_kappa, G*T) = 0.9728`
- `combined`: mean `R^2(Delta_kappa, G*T) = 0.1742`

So the lane only works on the **potential-weighted** metric construction.

### Screened controls (`mu^2 = 0.22`)

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
- therefore the clean screened statement is:

> the potential-weighted Ollivier observable is a **bounded linearized
> curvature-density proxy** on this surface, with dynamic self-consistency
> helping at weak/moderate coupling but not uniquely determining the strong
> coupling result

### Low-screening rerun (`mu^2 = 0.001`)

The dedicated low-screening runner gives:

- `self_consistent`: mean `R^2(Delta_kappa, G*T) = 0.9990`
- `random_matched`: mean `R^2 = 0.0014`
- random-control separation: `698.8x`

So the proxy clearly survives the move to a long screening length.

### Low-screening structured controls (`mu^2 = 0.001`)

Running the full control battery at the same `mu^2` gives mean
`R^2(Delta_kappa, G*T)`:

- `self_consistent`: `0.9990`
- `static_initial`: `0.4656`
- `shell_averaged`: `0.9935`
- `random_matched`: `0.0014`
- `shuffled`: `0.0020`

Interpretation:

- unscreening does **not** kill the proxy
- random/shuffled controls still collapse decisively
- but a smooth shell-averaged field almost perfectly reproduces the signal
- therefore the low-screening rerun strengthens the claim that this is a real
  **structured curvature proxy**, while weakening any claim that the exact
  self-consistent update is uniquely responsible for it

## Why this is bounded, not headline

This lane still has several important caveats:

- it still lives on a periodic staggered torus
- it uses an **effective metric definition** `d_eff = 1 + Phi_avg + offset`,
  not a standard graph-geometric Einstein derivation
- the successful signal is method-specific
- the low-screening rerun shows that **smooth structured controls** already
  explain almost all of the effect on this surface
- there is still no open-boundary / Wilson cross-check for this observable

## Honest retained claim

The retainable claim is:

> On the audited screened periodic staggered torus, a **potential-weighted
> Ollivier curvature proxy** tracks `G*T` strongly. The same proxy survives in
> the low-screening regime and decisively beats random/shuffled controls, but
> it remains a **bounded structured-curvature proxy** rather than an
> Einstein-equation derivation because the signal is method-specific and a
> shell-averaged structured potential reproduces almost all of it.

## What needs further work

Before any stronger claim, this lane needs:

1. an open-boundary or Wilson-style comparison surface
2. a nontrivial structured control that is smoother than random but less tied
   to the final self-consistent profile than shell averaging
3. a justification for why the potential-weighted Ollivier metric should be the
   physically preferred curvature observable here
