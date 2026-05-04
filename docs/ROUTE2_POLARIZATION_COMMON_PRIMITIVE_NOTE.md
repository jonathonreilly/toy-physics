# Route 2 Polarization Common Primitive Candidate

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** exact Route 2 bridge object between the finite-rank widening lane and
the direct universal GR lane  
**Purpose:** extract the strongest exact common candidate construction from the
Route 2 bridge triple and state the compatibility conditions that any support-
side `Pi_3+1` and curvature-side `Pi_curv` specialization must satisfy

## Verdict

The strongest exact common object currently supported by Route 2 is the bridge
triple

`B_R := (K_R, I_TB, Xi_TB)`.

That triple is exact and already lives at the support/curvature boundary:

- `K_R` is the exact support-side bilinear carrier
- `I_TB` is the exact tensorized action/coupling construction
- `Xi_TB` is the exact spacetime carrier on `PL S^3 x R`

From that exact triple, the strongest exact common *candidate construction* is
now explicit:

> the Route 2 bridge bundle candidate is the exact bridge triple `B_R`
> together with the exact orbit of localized `3+1` channel coefficients over
> valid polarization frames.

Concretely, the candidate object is the pair

`P_R^cand := (B_R, O_R)`,

where:

- `B_R = (K_R, I_TB, Xi_TB)`
- `O_R` is the exact orbit of localized `3+1` channel coefficients over valid
  `3+1` polarization frames

This is the strongest exact common construction because it already packages:

- the support-side scalar datum `delta_A1`
- the aligned bright channels `E_x` and `T1x`
- the exact `PL S^3 x R` semigroup factor `exp(-t Lambda_R)`
- the exact tensor-valued variational candidate `S_GR^cand`

The finite-rank support-side enlargement behind this candidate is documented
separately in
[`FINITE_RANK_SUPPORT_GENERATOR_FAMILY_NOTE.md`](./FINITE_RANK_SUPPORT_GENERATOR_FAMILY_NOTE.md):
the exact support-irrep frame `A1(center) ⊕ A1(shell) ⊕ E ⊕ T1` and the
aligned bright channels `u_E`, `u_T` give the largest exact noncanonical
support-side enlargement currently built from the atlas objects.

It is not yet a finished polarization bundle, because `O_R` is an orbit, not a
canonical section.

## Exact bridge data

The Route 2 carrier is

`K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`,

with

- `u_E = <E_x, q>`
- `u_T = <T1x, q>`
- `delta_A1 = phi_support(center)/Q - phi_support(arm_mean)/Q`

The exact tensorized action is

`I_TB(f, a ; j) = I_R(f ; j) + 1/2 ||a - vec K_R(q)||^2`.

The exact spacetime carrier is

`Xi_TB(t ; q) = vec K_R(q) \otimes exp(-t Lambda_R) u_*`.

These three objects are the shared interface between the two GR lanes.

## Compatibility conditions

Any support-side `Pi_3+1` specialization must satisfy:

1. it factors through the exact Route 2 carrier `K_R`;
2. it preserves the exact scalar support datum `delta_A1`;
3. it preserves the aligned bright channels `u_E` and `u_T`;
4. it splits the active quotient into lapse, shift, and spatial trace/shear
   before scalar collapse;
5. on the canonical `A1` family, it reproduces the exact endpoint columns
   `[(1, 1/6), (1, 0)]` already carried by `K_R`;
6. it agrees with the scalar active-quotient law on the exact finite-rank
   class;
7. it commutes with the Route 2 tensorized action `I_TB` on the shared carrier
   module.

Any curvature-side `Pi_curv` specialization must satisfy:

1. it factors through the exact tensor-valued variational candidate
   `S_GR^cand`;
2. it preserves the unique symmetric `3+1` quotient kernel;
3. it chooses a section from the exact orbit of localized `3+1` channel
   coefficients over valid `3+1` frames;
4. it splits the kernel into lapse, shift, and spatial trace/shear before
   localization;
5. it is covariant under valid `3+1` frame changes, not frame-dependent;
6. it commutes with the Route 2 spacetime carrier `Xi_TB` under the exact
   semigroup `exp(-t Lambda_R)`;
7. it reproduces the same scalar-line restriction as the Hessian candidate.

These conditions are the exact shared compatibility requirements for the
support-side and curvature-side specializations.

## Smallest missing axiom-native structure

The candidate construction above still does not close either lane, because the
orbit `O_R` is not canonical.

The smallest missing axiom-native structure is therefore still:

> a covariant `3+1` polarization-frame / projector bundle with a distinguished
> connection that turns the exact orbit of localized channel coefficients into
> a canonical section.

Equivalently:

> the missing primitive is a distinguished connection `\nabla_R` on the
> common `3+1` polarization bundle candidate.

That single structure would make both specializations derivable:

- on the finite-rank side, it would promote the exact Route 2 carrier into a
  canonical `Pi_3+1` lift;
- on the universal side, it would promote the exact quotient-kernel orbit into
  a canonical `Pi_curv`.

## Bottom line

The exact strongest common candidate construction is:

`P_R^cand := (B_R, O_R)`, with `B_R = (K_R, I_TB, Xi_TB)`.

The exact compatibility conditions are the seven support-side conditions above
and the seven curvature-side conditions above.

The exact missing axiom-native structure is:

> a covariant `3+1` polarization-frame / projector bundle with a distinguished
> connection `\nabla_R`.
