# Scalar `3+1` Temporal Ratio Theorem

**Date:** 2026-04-16
**Status:** exact scalar-bridge theorem plus dimension-4 support corollary
**Script:** `scripts/frontier_scalar_3plus1_temporal_ratio.py`

## Question

What exact `3+1` scalar quantity is currently closed on the minimal APBC block,
and what part of the old plaquette-bridge story is still only support-level?

## Answer

The exact closed result is the scalar bridge endpoint ratio on the minimal
`3 spatial + 1 time` APBC block:

- `A_2 = 1 / 8`
- `A_inf = 1 / (4 sqrt(3))`
- `A_inf / A_2 = 2 / sqrt(3)`

That ratio is exact.

What is **not** promoted here as a standalone theorem is the final insertion of
the fourth-root factor into a specific physical observable such as the gauge
plaquette. The fourth root is recorded as the natural dimension-4 scalar-density
candidate on this bridge, but that observable-level insertion remains a support
step unless independently closed.

## Exact theorem

On the exact minimal `3+1` block:

1. there are exactly `3` spatial directions from the retained `Z^3` base
2. there is exactly `1` derived time direction from anomaly-forced time
3. on the accepted APBC spatial cube `L_s = 2`, each spatial direction
   contributes the unit gap `sin^2(pi/2) = 1`

So the exact local scalar bridge kernel is

`K_sc(omega) = 3 + sin^2(omega)`.

The associated intensive scalar coefficient is

`A(L_t) = (1 / (2 L_t)) sum_omega 1 / (3 + sin^2 omega)`.

Its exact endpoints are:

- `A_2 = 1 / 8`
- `A_inf = 1 / (4 sqrt(3))`

Therefore

`A_inf / A_2 = 2 / sqrt(3)`.

## Support corollary for dimension-4 scalar densities

If a local observable couples through this scalar bridge as a dimension-4
density normalization, then the natural scalar-density factor is

`Gamma_sc = (A_inf / A_2)^(1/4) = (2 / sqrt(3))^(1/4)`.

This corollary is useful and numerically sharp, but it does **not** by itself
prove that a particular observable must inherit this insertion as its physical
vacuum completion.

## Why this matters

This exact ratio is a reusable atlas tool for:

- hierarchy endpoint arguments
- local scalar-density normalization work
- analytic plaquette support attempts

It removes the need to quote the old `(2 / sqrt(3))^(1/4)` factor as a loose
hierarchy-side diagnostic. The exact ratio now lives on its own exact `3+1`
scalar bridge surface.

## Commands run

```bash
python3 scripts/frontier_scalar_3plus1_temporal_ratio.py
```

Expected summary:

- `EXACT PASS=4 FAIL=0`
- `SUPPORT=1`
