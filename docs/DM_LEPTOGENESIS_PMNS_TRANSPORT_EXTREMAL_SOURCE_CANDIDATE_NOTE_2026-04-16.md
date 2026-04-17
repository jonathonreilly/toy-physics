# DM Leptogenesis PMNS Transport-Extremal Source Candidate

**Date:** 2026-04-16  
**Status:** exact positive selector candidate beyond the sole-axiom boundary  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate.py`

## Question

If the sole axiom

`Cl(3)` on `Z^3`

does not by itself fix the off-seed `5`-real source on the PMNS-assisted
charged-lepton-active `N_e` route, what is the strongest positive derived law
candidate for full-stack closure?

## Bottom line

Use the exact flavored transport functional itself as the selector on the fixed
native seed surface.

That is:

1. keep the already-derived seed pair `(xbar, ybar)` fixed
2. vary only the off-seed `5`-real source
   `(xi_1, xi_2, eta_1, eta_2, delta)`
3. choose the source that extremizes the exact flavored transport lift

`max_i eta_i / eta_obs`.

This is not a sole-axiom theorem. It is a constructive **derived dynamical
selector candidate** on top of the already-closed exact DM transport law.

## Exact construction

### 1. Fixed native seed surface

On the canonical `N_e` seed pair:

- `xbar = 0.5633333333333334`
- `ybar = 0.30666666666666664`

the aligned seed point gives only

`eta / eta_obs = 0.7190825360613422`.

So the exact seed law alone is not enough.

### 2. Transport-extremal source candidate

Using a positive seed-preserving parameterization of the active class, the
exact flavored transport functional produces a concrete extremal source:

- `x_opt = (0.0876587, 1.49144738, 0.11089392)`
- `y_opt = (0.29016988, 0.18598487, 0.44384525)`
- `delta_opt = -2.2327839107695158`

with

`eta / eta_obs = 1.0522203130495849`

on its best selected column.

So the off-seed source class contains points that already overshoot the
required value.

### 3. Exact closure by continuity

Because:

- the aligned seed point gives `0.7190825360613422 < 1`
- the extremal candidate gives `1.0522203130495849 > 1`

and the exact transport value is continuous on the interpolating fixed-seed
family, there exists an exact closure point on the same source class with

`eta / eta_obs = 1`.

The runner exhibits one such point:

- `lambda_* = 0.9141068558905899`
- `x_close = (0.128516, 1.411729, 0.149755)`
- `y_close = (0.291587, 0.196351, 0.432063)`
- `delta_* = -2.0410030805566177`

and

`eta / eta_obs = 1`

on its best selected flavor column.

## Consequence

This does **not** prove that the sole axiom already fixed the off-seed source.

It proves something sharper and more useful for the DM branch:

- the remaining obstruction is no longer **existence**
- full-stack closure is already **constructive**
- what is still missing is only the final selector law for the off-seed source

So the live scientific question is now:

> Is exact transport extremality on the fixed native seed surface the correct
> derived dynamical law inside the framework?

If yes, the off-seed source closes and the PMNS-assisted DM route closes with
it.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate.py
```
