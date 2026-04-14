# Hierarchy Finite-`L_t` Interpolation Note

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_hierarchy_finite_lt_interpolation.py`

## Question

Can the exact APBC temporal normalization on the minimal hierarchy block be
written in closed form for **all** finite `L_t`, not just at `L_t = 2` and
`L_t -> infinity`?

## Exact result

Yes.

For the spatial-APBC minimal block, the exact small-m effective-potential
coefficient

`Delta f(L_t, m) = A(L_t, u_0) m^2 + O(m^4)`

has the exact finite-`L_t` closed form

`A(L_t, u_0) = [1 / (4 sqrt(3) u_0^2)] * (1 - q^Lt) / (1 + q^Lt)`

with

`q = 2 - sqrt(3)`.

So the temporal normalization is not an arbitrary interpolation. It is an
exact exponential approach from the UV endpoint `L_t = 2` to the `3+1`
temporal average `L_t -> infinity`.

## Endpoint recovery

The closed form reproduces both exact endpoints:

- `A_2 = 1 / (8 u_0^2)`
- `A_inf = 1 / (4 sqrt(3) u_0^2)`

since:

- at `L_t = 2`, `(1 - q^2)/(1 + q^2) = sqrt(3) / 2`
- as `L_t -> infinity`, `q^Lt -> 0`

## Why this matters

The dimension-4 hierarchy correction factor becomes an exact family:

`C(L_t) = (A_2 / A(L_t))^(1/4)`

with:

- `C(2) = 1`
- `C(4) = (7/8)^(1/4) ~= 0.967168210`
- `C(infinity) = (3/4)^(1/8) ~= 0.964678630`

The observed hierarchy prefactor is:

`C_obs = 246.22 / 253.4 ~= 0.971665351`

and it lies on the same exact interpolation curve, corresponding to

`L_t,eff ~= 3.177`

which is between the exact `L_t = 2` UV endpoint and the exact `L_t = 4`
correction.

## Honest interpretation

This still does **not** prove the hierarchy theorem.

What it does prove is much sharper:

1. the temporal normalization family is exact
2. the observed prefactor is not ad hoc; it sits on the same exact finite-`L_t`
   curve
3. the remaining theorem is now precisely:

> which exact member, or derived combination, of this closed finite-`L_t`
> family is the physical electroweak order-parameter normalization?

That is a much narrower problem than the old "what is the prefactor?" framing.

## What is still open

The last load-bearing step remains:

- derive why the physical EWSB observable picks the `L_t = 2` UV endpoint,
  or a derived finite-`L_t` normalization from this exact family
- then insert that exact normalization into the final `det -> v` map

So the hierarchy route is still not fully closed, but the remaining gap is now
an exact finite-`L_t` order-parameter selection theorem.
