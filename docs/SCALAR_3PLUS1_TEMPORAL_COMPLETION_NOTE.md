# Scalar `3+1` Temporal Completion Theorem

**Date:** 2026-04-15  
**Status:** THEOREM -- exact temporal-completion factor for local scalar densities on the minimal `3+1` block  
**Script:** `scripts/frontier_scalar_3plus1_temporal_completion.py`

## Question

Is the exact factor

`2 / sqrt(3)`

just a hierarchy-side curiosity, or is it the universal temporal-completion
factor for local scalar observables on the exact `3 spatial + 1 time` route?

## Answer

It is the exact `3+1` scalar temporal-completion factor.

The key point is kinematic, not hierarchy-specific.

On the exact minimal `3+1` block:

1. there are exactly `3` spatial directions;
2. the accepted spatial APBC minimal cube puts each spatial direction at unit
   gap;
3. there is exactly `1` derived time direction;
4. a local bosonic scalar source is a source-response coefficient of the exact
   fermionic Gaussian generator, so it inherits the same APBC temporal orbit;
5. a local scalar source couples only to the scalar bridge.

Therefore the exact scalar bridge kernel is

`K_sc(omega) = 3 + sin^2(omega)`.

The associated intensive local scalar coefficient is

`A(L_t) = (1 / (2 L_t)) sum_omega 1 / (3 + sin^2 omega)`.

Its exact endpoints are:

- `A_2 = 1 / 8`
- `A_inf = 1 / (4 sqrt(3))`

so the exact temporal-completion ratio is

`A_inf / A_2 = 2 / sqrt(3)`.

For a local **dimension-4** scalar density, the corresponding normalization
factor is the fourth root:

`Gamma_sc = (A_inf / A_2)^(1/4) = (2 / sqrt(3))^(1/4)`.

## Theorem 1: exact scalar bridge kernel on the minimal `3+1` block

The exact route has:

- `3` spatial directions from the project’s `Z^3` base;
- `1` derived time direction from the anomaly-forced single clock.

For the accepted minimal APBC spatial cube `L_s = 2`, each spatial direction
contributes the unit gap

`sin^2(pi/2) = 1`.

So the exact local scalar bridge on the minimal `3+1` block is

`K_sc(omega) = 1 + 1 + 1 + sin^2(omega) = 3 + sin^2(omega)`.

This is the unique local scalar bridge because the source is bosonic,
gauge-invariant, and rotation-scalar on the exact `3+1` route, while the
underlying exact source generator is still the APBC fermionic Gaussian
`W[J] = log|det(D+J)| - log|det D|`.

## Theorem 2: exact endpoint coefficients

The exact intensive local scalar coefficient is

`A(L_t) = (1 / (2 L_t)) sum_omega 1 / K_sc(omega)`
`= (1 / (2 L_t)) sum_omega 1 / (3 + sin^2 omega)`.

### UV endpoint `L_t = 2`

For APBC on `L_t = 2`, the temporal frequencies are `omega = ±pi/2`, so

`sin^2 omega = 1`

and therefore

`A_2 = (1 / 4) * (1/4 + 1/4) = 1 / 8`.

### Temporal average `L_t -> infinity`

As `L_t -> infinity`,

`A_inf = (1 / 2) * (1 / (2 pi)) integral_0^(2 pi) d omega / (3 + sin^2 omega)`.

Using the standard integral

`(1 / (2 pi)) integral_0^(2 pi) d omega / (a + b sin^2 omega)`
`= 1 / sqrt(a (a+b))`,

with `a = 3`, `b = 1`, one gets

`A_inf = (1 / 2) * 1 / sqrt(3 * 4) = 1 / (4 sqrt(3))`.

So:

`A_inf / A_2 = (1 / (4 sqrt(3))) / (1 / 8) = 2 / sqrt(3)`.

## Corollary: dimension-4 scalar completion factor

For a local scalar observable that is a **dimension-4** density, the
normalization acts on the density rather than directly on a scale.

Therefore the exact completion factor is the fourth root:

`Gamma_sc = (A_inf / A_2)^(1/4) = (2 / sqrt(3))^(1/4)`.

This is the correct insertion for local dimension-4 bosonic scalar densities on
the exact minimal `3+1` route.

## Why this matters for the plaquette

The plaquette observable

`P = <(1/3) Re Tr U_P>`

is:

1. local
2. bosonic
3. gauge-invariant
4. spatial-rotation scalar
5. a dimension-4 density with `4` links

So its temporal completion is governed by the exact scalar factor

`Gamma_sc = (2 / sqrt(3))^(1/4)`,

not because it is “the hierarchy factor,” but because it is the exact
`3+1` scalar temporal-completion factor.

## Commands run

```bash
python3 scripts/frontier_scalar_3plus1_temporal_completion.py
```

Output summary:

- exact checks: `5 pass / 0 fail`
- `A_2 = 1/8`
- `A_inf = 1/(4 sqrt(3))`
- `A_inf / A_2 = 2 / sqrt(3)`
- `Gamma_sc = (2 / sqrt(3))^(1/4)`
