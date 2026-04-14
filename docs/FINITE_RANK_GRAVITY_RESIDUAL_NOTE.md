# Finite-Rank Strong-Field Source Closure and `3+1` Einstein-Residual Test

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_finite_rank_gravity_residual.py`  
**Status:** Exact finite-rank source theorem plus bounded `3+1` residual separation; not full nonlinear GR

## Purpose

The previous Codex strong-field footholds already established:

- exact rank-one resolvent closure
- exact finite-support diagonal-source closure
- a bounded common-source static-isotropic candidate

The obvious remaining objection was:

> the actual strong-field matter source is not rank-one and need not be diagonal
> on its support

This note pushes the source model one step further and then uses that stronger
source object to test the `3+1` metric candidate directly.

## Exact theorem: finite-rank support operator

Let:

- `H_0 = -Delta_lat`
- `S` be a finite support of lattice sites
- `P` inject the support basis into the full lattice basis
- `W` be a positive-semidefinite matrix on `S`
- `H_W = H_0 - P W P^T`
- `G_0 = H_0^-1`
- `G_S = P^T G_0 P`

Then the exact Woodbury / Dyson identity gives:

`G_W P = G_0 P (I - W G_S)^-1`

So for any bare source weights `m` supported on `S`,

`phi = G_W P m = G_0 P q_eff`

with

`q_eff = (I - W G_S)^-1 m`.

This is a genuine exact upgrade over the earlier diagonal attractive class:

- the support can be multi-site
- the support operator can contain off-diagonal correlations / mixing
- the exterior field still factors through one support-renormalized source
  vector `q_eff`

## Exact consequence: exterior harmonicity still holds

Because

`H_0 phi = P q_eff`,

the exact field obeys

`(-Delta_lat) phi = 0`

at every site outside the support.

So the exterior strong-field data are still one exact harmonic object, now for
a broader finite-rank source class.

## Bounded `3+1` test: direct candidate vs monopole projection

Using that exact harmonic field, define the same common-source metric candidate:

- `psi = 1 + phi`
- `alpha = (1 - phi) / (1 + phi)`

and therefore

- `g_tt = -alpha^2`
- `g_ij = psi^4 delta_ij`

This is the natural “same object drives both sectors” candidate.

The new script tests two things:

1. **Direct common-source candidate**
   - use the exact finite-rank `phi(x)` directly
   - compute a numerical `3+1` Einstein tensor residual at exterior probe points

2. **Monopole-projected isotropic candidate**
   - shell-average the same exact `phi(x)`
   - fit the exterior harmonic data by
     `phi_shell(r) = a/r + b/r^3`
   - keep only the derived monopole coefficient `a`
   - rebuild the isotropic candidate from `phi_mono(r) = a/r`
   - compute the same `3+1` Einstein residual

## What the script finds

### Exact checks

1. finite-rank column identity
2. compressed-source field formula
3. exterior harmonicity outside support

All three pass at machine precision.

### Bounded checks

4. the exact exterior field is monopole-dominated after shell averaging
   - fitted `a = 0.3465`
   - fitted `b = 0.6312`
   - relative RMS shell-fit error `~ 5.2%`
5. the **direct** common-source `3+1` candidate has a nonzero vacuum Einstein
   residual outside the source
   - max sampled `|G_{mu nu}| ~ 9.85e-2`
6. the **monopole-projected** isotropic candidate from the same exact field
   sharply reduces that residual
   - max sampled `|G_{mu nu}| ~ 1.52e-4`
   - improvement factor `~ 6.5e2`

## Interpretation

This is the clearest Codex-side gravity statement so far:

- the exact source-model foothold is now broader than a point source or a
  diagonal support potential
- the exact exterior field still comes from one source-renormalized harmonic
  object
- feeding that object directly into the conformastatic metric ansatz is **not**
  yet a vacuum Einstein solution
- but the monopole / isotropic projection of the same exact field is already
  extremely close to vacuum at the sampled `3+1` residual level

So the remaining gravity gap is no longer vague. It is:

> derive why the exact finite-rank harmonic exterior data reduce to the
> isotropic-vacuum surface used by the strong-field metric candidate.

That is a much sharper target than “derive all of GR.”

## What this closes

This closes a real sub-gap:

> the exact strong-field source-model foothold is no longer limited to a
> point source or to a diagonal support operator

The exact source theorem now covers a broader finite-rank positive-semidefinite
support class.

## What this does not close

This note still does **not** close:

1. the actual physical many-body matter source law
2. the theorem-grade reduction to the isotropic-vacuum sector
3. full nonlinear GR
4. downstream no-horizon / no-echo claims

## Practical next step

The next gravity target is now precise:

1. derive why the physical strong-field source produces monopole-dominated
   exterior data strongly enough to justify the isotropic-vacuum reduction
2. or derive the correct broader nonlinear exterior field equations directly
   from the same exact closure object

Until one of those happens, full nonlinear GR remains open.
