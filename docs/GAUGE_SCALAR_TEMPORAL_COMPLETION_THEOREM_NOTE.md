# Gauge-Scalar Temporal Completion Theorem

**Date:** 2026-04-16
**Status:** exact theorem on the accepted Wilson nearest-neighbor gauge-source class
**Script:** `scripts/frontier_gauge_scalar_temporal_completion_theorem.py`

## Question

On the accepted `3 spatial + 1 derived time` Wilson surface, is the factor

`A_inf / A_2 = 2 / sqrt(3)`

just a property of one chosen scalar kernel, or is it the universal temporal
completion law for the entire accepted class of local bosonic scalar gauge
sources?

## Answer

It is universal on the accepted source class.

More precisely:

> every accepted local bosonic scalar gauge source on the Wilson
> nearest-neighbor plaquette surface inherits the same normalized temporal
> completion law on the exact minimal `3 spatial + 1 derived-time` block.

The important point is that the accepted source class is already fixed by the
Wilson grammar. It is not an arbitrary family of scalar kernels.

## Theorem 1: the accepted Wilson source grammar is one-dimensional

The Wilson gauge action uses one common coefficient on the six nearest-neighbor
plaquette orientations

`(x,y), (x,z), (x,t), (y,z), (y,t), (z,t)`.

So an accepted local bosonic scalar gauge source is determined by one overall
plaquette weight `w`.

There is no independent site-term scalar source on the accepted gauge side, and
there is no allowed anisotropic splitting of the six plaquette orientations on
the accepted Wilson surface.

That makes the accepted gauge-source class one-dimensional.

## Theorem 2: the accepted Wilson source induces equal directional weights on all four coordinates

Each coordinate direction appears in exactly three of the six plaquette
orientations.

So if every plaquette orientation carries the same source weight `w`, the
induced directional coefficients are

`a_x = a_y = a_z = a_t = 3w`.

This is exact combinatorics on the `3 spatial + 1 derived-time` hypercubic
surface.

## Theorem 3: exact reduction on the minimal APBC spatial cube

Let the local scalar gauge-source kernel be written in directional form as

`K_O(p) = a_x sin^2 p_x + a_y sin^2 p_y + a_z sin^2 p_z + a_t sin^2 omega`.

On the accepted APBC minimal spatial cube `L_s = 2`, each spatial direction
contributes the unit gap

`sin^2(pi/2) = 1`.

Using the exact Wilson-induced coefficients from Theorem 2 gives

`K_O(omega) = 3w + 3w + 3w + 3w sin^2 omega`

so every accepted source reduces exactly to

`K_O(omega) = 3w (3 + sin^2 omega)`.

That is the load-bearing result:

> the accepted Wilson local bosonic scalar gauge-source class has one exact
> temporal kernel shape on the minimal `3+1` block, differing only by overall
> normalization.

## Corollary: universal temporal completion law

Define the intensive source-response coefficient

`A_O(L_t) = (1 / (2 L_t)) sum_omega 1 / K_O(omega)`.

Since

`K_O(omega) = 3w (3 + sin^2 omega)`,

the normalization `3w` cancels in the endpoint ratio, leaving the universal
law

`A_O(inf) / A_O(2) = 2 / sqrt(3)`.

So the exact temporal completion law is universal on the full accepted local
bosonic scalar gauge-source class.

For a local dimension-4 gauge scalar density, the corresponding bridge factor
is therefore

`Gamma_sc = (2 / sqrt(3))^(1/4)`.

## Why this matters for the plaquette bridge

This closes one specific objection to the plaquette bridge:

> the scalar completion factor is not tied only to one chosen scalar toy kernel.

The plaquette source is now covered by a stronger exact theorem:

1. it is an accepted local bosonic scalar gauge source on the Wilson surface;
2. the accepted source class has one universal temporal completion law;
3. that law is exactly `A_inf / A_2 = 2 / sqrt(3)`.

So the plaquette inherits the scalar temporal bridge because the whole accepted
Wilson local gauge-source class does.

## What this does not yet close

This theorem does **not** by itself finish the full analytic plaquette closure.

What still remains is the observable-level reduction step:

> why the full interacting gauge-vacuum plaquette expectation is exactly the
> local one-plaquette response evaluated at the completed effective coupling.

So this theorem upgrades the bridge-support stack materially, but it does not
by itself justify repo-wide migration from the canonical same-surface plaquette
value to the analytic candidate.

## Command

```bash
python3 scripts/frontier_gauge_scalar_temporal_completion_theorem.py
```

Expected summary:

- `PASS=8 FAIL=0`
