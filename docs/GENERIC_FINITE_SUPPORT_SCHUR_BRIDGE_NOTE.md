# Generic Finite-Support Schur Bridge Closure on the Current Static Conformal Surface

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_generic_finite_support_schur_bridge.py`  
**Status:** Exact support-class widening theorem on the current bridge surface;
not full nonlinear GR

## Purpose

The current strong-field bridge package is already exact on the local `O_h`
star-supported benchmark class and on the broader star-supported finite-rank
class.

The remaining honest objection is now narrower:

> perhaps the bridge package is still tied to star-supported geometry, even if
> it is exact on the current benchmark families

This note removes that specific limitation on the current bridge surface by
showing that the same microscopic variational bridge action and static
conformal lift are support-agnostic across generic finite support sets.

## Exact finite-support theorem

Let `S` be any finite support inside the current Dirichlet box and let `W` be
any positive-semidefinite support operator on `S`. Define

- `H_W = H_0 - P W P^T`
- `G_0 = H_0^-1`
- `G_S = P^T G_0 P`

Then the exact Woodbury / Dyson identity gives

- `G_W P = G_0 P (I - W G_S)^-1`

and therefore, for any bare support weights `m`,

- `phi = G_W P m = G_0 P q_eff`
- `q_eff = (I - W G_S)^-1 m`

so the exact exterior field is always one source-renormalized harmonic object
outside `S`.

The important point for the bridge is that this statement does **not** use the
star geometry. It only uses finite support and the exact lattice resolvent.

## Exact support-class bridge closure

For the exterior projector field `phi_ext`, define the native same-charge
bridge

- `psi = 1 + phi_ext`
- `chi = 1 - phi_ext = alpha psi`

and the local source/stress fields

- `sigma_R = H_0 phi_ext`
- `rho = sigma_R / (2 pi psi^5)`
- `S = 0.5 rho (1/alpha - 1)`

Then the static conformal constraint pair remains exact:

- `H_0 psi = 2 pi psi^5 rho`
- `H_0 chi = -2 pi alpha psi^5 (rho + 2S)`

and the same microscopic Schur-complement boundary action remains stationary
at the shell trace.

That means the bridge-side closure package is support-agnostic on finite
support, not just on the current star-supported benchmark classes.

## What the script checks

The runner samples several genuinely non-star finite-support source operators
and verifies:

1. the support is non-star and finite
2. the exterior field still localizes its shell source to the same sewing band
   `3 < r <= 5`
3. the local static conformal constraints remain exact to machine precision
4. the same microscopic Schur boundary action remains stationary at the exact
   shell trace

This is a support-class widening test, not a retread of the star benchmark.

## What this closes

This closes the remaining support-class objection within the current bridge
surface:

> the exact bridge-side closure package is not confined to star-supported
> finite-rank sources; it extends to generic finite-support source operators on
> the same finite Dirichlet box

That is the strongest support-class generalization currently defensible on the
branch.

## What this does not close

This note still does **not** close:

1. closure beyond the current static conformal bridge
2. noncompact or long-range support classes
3. fully general nonlinear GR

## Practical conclusion

The remaining gravity problem is now even sharper:

- the exact bridge package is no longer star-specific
- the live gap is the extension beyond the current static conformal bridge,
  and then any truly broader noncompact support class
