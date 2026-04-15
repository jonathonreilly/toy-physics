# Polarization Common Primitive Synthesis

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** cross-lane synthesis between the finite-rank widening lane and the direct universal GR lane  
**Purpose:** decide whether the finite-rank missing `Pi_3+1` support-side polarization frame and the universal missing covariant `3+1` polarization-frame/projector bundle are the same axiom-native primitive in two guises

## Verdict

They are **not the same exact object**, but they **are the same missing
primitive family**.

The finite-rank lane is blocked **before** scalar renormalization collapse:
it needs a support-side tensor polarization frame that can split the active
quotient into lapse, shift, and spatial trace/shear channels.

The direct universal lane is blocked **after** the exact `3+1` kinematic lift
and tensor Hessian candidate are already in hand: it needs a covariant
polarization-frame / projector bundle that can localize the unique symmetric
quotient kernel into the same lapse, shift, and spatial trace/shear channels.
The strongest exact universal-side output so far is an associated family of
such localizations over valid `3+1` polarization frames, not a canonical
section.

So the two blockers are different stage-specific realizations of the same
missing family:

> an exact `3+1` polarization bundle that canonically splits the tensor
> degrees of freedom into lapse, shift, and spatial trace/shear channels.

## Why they are not literally identical

### Finite-rank widening lane

The finite-rank blocker is support-side and pre-collapse:

- the support response collapses to rank one after renormalization
- the active quotient remains rank two
- the strongest exact support-side specialization already in hand is the
  Route 2 bilinear carrier
  `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`
- the missing object is still a support-side polarization frame with enough
  independent generators to lift the scalar active quotient canonically

This is the `Pi_3+1` side of the story.

### Direct universal lane

The universal blocker is quotient-side and post-candidate:

- the scalar observable generator is exact
- the `3+1` lift is exact
- the tensor Hessian candidate is exact
- the symmetric quotient kernel is unique
- what is missing is the covariant localization bundle that turns that kernel
  into Einstein/Regge curvature channels

This is the `Pi_curv` side of the story.

So the exact objects differ because the stage differs. The family is the same.

## The smallest common primitive

The smallest common primitive that would advance both lanes at once is:

> a covariant `3+1` polarization-frame bundle with a support-side restriction
> and a curvature-localization projection.

Concretely, that primitive must provide two functorial specializations:

- a support-side polarization lift `Pi_3+1` that splits the finite-rank active
  quotient into lapse, shift, and spatial trace/shear before scalar collapse
- a curvature-localization map `Pi_curv` that splits the unique symmetric
  Hessian kernel into the same channels on `PL S^3 x R`

If one wants a single name for the common primitive family, the right name is:

> the `3+1` polarization bundle / projector bundle.

## Relation to Route 2

The Route 2 bilinear carrier/action stack is the natural interface between the
two lanes because it already separates:

- the exact scalar background datum `delta_A1`
- the aligned bright channels `E_x` and `T1x`
- the exact `PL S^3 x R` semigroup factor `exp(-t Lambda_R)`
- the exact support-side bilinear carrier `K_R`

That stack does **not** yet close either lane by itself, but it gives the
common bundle a concrete place to act.

## Strongest exact common construction from Route 2

The strongest exact common object the current Route 2 interface actually
supports is the bridge triple

`B_R := (K_R, I_TB, Xi_TB)`.

This is exact on the current Route 2 stack because each component is exact:

- `K_R` is the exact support-side bilinear carrier
- `I_TB` is the exact tensorized action/coupling construction
- `Xi_TB` is the exact spacetime carrier on `PL S^3 x R`

`B_R` is the best common interface object because it already lives at the
support/curvature boundary and carries the aligned bright channels plus the
`PL S^3 x R` semigroup factor.

But `B_R` is still not the missing polarization bundle:

- it does not canonically split lapse, shift, and spatial trace/shear
- it does not supply a covariant connection
- it does not define `Pi_3+1` or `Pi_curv`

So the exact missing step is still a covariant `3+1` polarization-frame /
projector bundle with a distinguished connection.

## Implications

1. A successful derivation of the common polarization bundle would advance
   both lanes simultaneously.
2. The finite-rank lane would gain a canonical `Pi_3+1` lift.
3. The universal lane would gain a canonical `Pi_curv`.
4. If the bundle cannot be derived from the current atlas, then both lanes are
   missing the same kind of primitive, just at different stages.

## Bottom line

The missing primitive is **shared as a family**, not identical as a finished
object.

The exact common primitive to pursue is:

> a covariant `3+1` polarization-frame / projector bundle that canonically
> splits lapse, shift, and spatial trace/shear, with support-side and
> curvature-side specializations.
