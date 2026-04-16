# Baryogenesis `K_EWPT` Single-Order-Parameter Note

**Date:** 2026-04-16
**Status:** exact current-surface transition-stage reduction with bounded target geometry on `main`
**Script:** `scripts/frontier_baryogenesis_kewpt_single_order_parameter.py`

## Safe statement

On the current `main` package surface, the transition-history stage of the
remaining baryogenesis bridge

`K_NP = K_EWPT * K_tr * K_sph`

does not live on a hidden multi-field scalar surface.

It reduces exactly to one real functional

`K_EWPT = F_EWPT[χ(τ)]`

of one unique retained scalar thermal history lane `χ(τ)` on the APBC/Higgs
surface.

This note does **not** compute `F_EWPT`. It closes the weaker but important
review question:

> does the current same-surface `K_EWPT` problem live on one scalar history
> lane or on some hidden higher-multiplicity scalar family?

Answer:

- one scalar history lane
- not a hidden extra same-surface scalar family

## What is already fixed upstream

The current package already fixes:

1. one additive CPT-even scalar generator through the exact observable
   principle
2. one bosonic-bilinear thermal scalar response kernel on the APBC surface
3. one unique minimal resolved thermal orbit at `L_t = 4`
4. one same-surface Higgs doublet from the `G_5` condensate
5. one radial Higgs mode plus three Goldstones on the Higgs/CW surface
6. no currently derived extra same-surface scalar family that rescues the old
   2HDM-like baryogenesis route

Those ingredients are enough to reduce the transition-stage configuration
space to one retained scalar history lane.

## Exact single-lane reduction

The thermal-order-parameter uniqueness result already gives the static
normalization surface:

- `A_2 = 1/8`
- `A_4 = 1/7`
- `A_inf = 1/(4 sqrt(3))`

Normalizing to the `L_t = 2` anchor gives one retained scalar lane:

- `χ_2 = A_2 / A_2 = 1`
- `χ_4 = A_4 / A_2 = 8/7`
- `χ_inf = A_inf / A_2 = 2/sqrt(3)`

So the static same-surface freedom is only an `O(10%)` normalization band.

That means the genuinely open content of the transition stage is not extra
field content. It is the nonequilibrium history functional

`F_EWPT[χ(τ)]`

on this one retained scalar lane.

Hence

`K_EWPT = F_EWPT[χ(τ)]`.

## Why this is not a hidden extra scalar family

The present authority surface still derives exactly:

- one Higgs doublet from the `G_5` condensate
- one radial Higgs mode plus three Goldstones
- no extra taste-scalar doublet on the authority path

The old current-surface no-go already says the old 2HDM-like route is not live
on `main`, and the thermal-order-parameter uniqueness note already says the
APBC selector stack gives a unique thermal order-parameter surface rather than
a hidden extra scalar family.

Together these results remove the remaining same-surface multi-order-parameter
escape hatch for `K_EWPT`.

## Bounded target geometry

Using the retained promoted weak-flavor source and observed asymmetry
normalization,

- `η_obs = 6.12e-10`
- `J = 3.330901e-5`
- `K_NP,target = η_obs / J = 1.837341e-5`

the transition stage inherits the following exact benchmark geometry:

### If transport and sphaleron stages were ideal

`K_EWPT = K_NP,target = 1.837341e-5`

### Equal three-stage split

`K_EWPT = (K_NP,target)^(1/3) = 2.638740e-2`

### If `K_tr = K_sph = 0.1`

`K_EWPT = K_NP,target / (0.1 * 0.1) = 1.837341e-3`

These are not derived values of `K_EWPT`. They are the correct same-surface
target geometry once the stage decomposition is fixed.

## What this closes

This note closes the question:

> “What configuration space does the transition-history factor `K_EWPT`
> actually live on, on current `main`?”

Answer:

- one unique scalar thermal order-parameter history lane `χ(τ)`
- one real functional `F_EWPT[χ(τ)]`
- not a hidden extra same-surface scalar-family parameter space

## What remains open

This note does **not** derive:

- the real-time or Euclidean finite-`T` history `χ(τ)`
- the functional `F_EWPT`
- `K_tr`
- `K_sph`
- the final first-principles `η`

So baryogenesis remains open.

But the transition stage is now reduced as tightly as the current package
supports.

## Relation to the existing baryogenesis notes

- [BARYOGENESIS_THERMAL_ORDER_PARAMETER_UNIQUENESS_NOTE.md](./BARYOGENESIS_THERMAL_ORDER_PARAMETER_UNIQUENESS_NOTE.md)
  fixed the unique APBC thermal order-parameter surface
- [BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md](./BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md)
  removed the old same-surface extra-doublet rescue path
- [BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md](./BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md)
  fixed the exact stage product

This note is the next reduction:

- the transition-history stage itself now lives on one scalar history lane

## Validation

- [frontier_baryogenesis_kewpt_single_order_parameter.py](./../scripts/frontier_baryogenesis_kewpt_single_order_parameter.py)
- [BARYOGENESIS_THERMAL_ORDER_PARAMETER_UNIQUENESS_NOTE.md](./BARYOGENESIS_THERMAL_ORDER_PARAMETER_UNIQUENESS_NOTE.md)
- [BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md](./BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md)
- [BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md](./BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md)

Current runner state:

- `frontier_baryogenesis_kewpt_single_order_parameter.py`: expected `PASS>0`,
  `FAIL=0`
