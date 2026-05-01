# Universal GR Positive-Background Local Closure on `PL S^3 x R`

**Status:** support - structural or confirmatory support note
**Date:** 2026-04-14 (sign character corrected 2026-05-01)
**Branch:** `codex/review-active`
**Role:** direct universal route / strongest local closure theorem
**Runner:** scripts/universal_gr_positive_background_local_closure.py

## Verdict

The direct-universal route closes as an exact **definite-background local
Einstein/Regge boundary-action family** on `PL S^3 x R` with a unique exact
stationary boundary field for every real positive-symmetric background `D`
and source `J`.

The earlier draft of this note labelled the resulting kinetic operator
`K_GR(D)` as symmetric positive-definite. That polarity claim was wrong:
for the bilinear form `B_D(h,k) = -Tr(D^-1 h D^-1 k)` displayed below,
`B_D(h,h) = -Tr(H̃²) ≤ 0` for every symmetric `h ≠ 0` (where
`H̃ = D^{-1/2} h D^{-1/2}`). So `H_D` is symmetric **negative-definite**
on the symmetric tangent space, not positive-definite. The substantive
content — existence and uniqueness of the stationary boundary field
`F_* = K_GR(D)^{-1} J` and the completion identity — survives unchanged;
only the extremum polarity changes.

This note now states the corrected version of the closure.

## Exact local family

The exact universal local bilinear form is

`B_D(h,k) = -Tr(D^-1 h D^-1 k)`.

For `D` symmetric positive-definite and `h` symmetric, define
`H̃ = D^{-1/2} h D^{-1/2}` (also symmetric). Then by cyclic permutation

`B_D(h,h) = -Tr(D^-1 h D^-1 h) = -Tr(H̃²) ≤ 0`,

with equality iff `h = 0`. So `B_D` is symmetric **negative-definite** on
the symmetric tangent space. This is the standard sign for the second
variation of `log det D` at a symmetric positive-definite `D` — `log det`
is concave on the positive cone, so its Hessian is negative-definite.

The exact slice generator `Lambda_R` is symmetric positive-definite on the
branch (independent calculation, unchanged by the present correction).

So the direct-universal local action family is

`I_GR(F ; D, J) = 1/2 <F, K_GR(D) F> - <J, F>`

with

`K_GR(D) = H_D ⊗ Lambda_R`,

where `H_D` is the operator induced by `B_D`. Because `H_D ≺ 0` and
`Lambda_R ≻ 0`, the tensor product satisfies

`K_GR(D) ≺ 0`     (symmetric **negative**-definite).

## Unique stationary boundary field

`K_GR(D)` is invertible (negative-definite, hence nonsingular). The
stationary point of `I_GR` is unique:

`F_* = K_GR(D)^{-1} J`.

This is a **maximum** of the concave action `I_GR`, equivalently the
**minimum** of the convex action `J_GR := -I_GR`. The completion
identity holds with a non-positive remainder:

`I_GR(F_* + Δ ; D, J) - I_GR(F_* ; D, J) = (1/2) <Δ, K_GR(D) Δ> ≤ 0`,

with equality iff `Δ = 0`. Equivalently, in the convex formulation

`J_GR(F_* + Δ) - J_GR(F_*) = -(1/2) <Δ, K_GR(D) Δ> ≥ 0`,

with equality iff `Δ = 0`. Either way the stationary boundary field is
unique and isolated.

## What this says, and what it does not

What this **does** say:

> for each real positive-symmetric background `D` and boundary source `J`,
> the direct-universal action admits a unique exact stationary boundary
> field `F_*(D, J) = K_GR(D)^{-1} J`, and the action is concave around
> that point with a quadratic completion identity.

What it does **not** say:

- The operator `K_GR(D)` is **not** positive-definite as the earlier draft
  claimed; it is negative-definite. The unique-stationary-solution content
  is the load-bearing claim, and that survives the sign correction. The
  earlier "positive local minimum" framing was incorrect.
- This local-closure result does not yet identify the concave family with
  a Lorentzian/unrestricted-GR action. The residual gap to full GR
  remains global and interpretive, not local and operator-level.

## Why this is still a real local closure

The earlier draft over-claimed by inserting a polarity adjective
("positive-definite") that the math did not support. The substantive
content is:

- a single closed-form bilinear form `B_D` for every symmetric
  positive-definite background `D`,
- a single closed-form action operator `K_GR(D) = H_D ⊗ Lambda_R`,
- a unique stationary boundary field for every source `J`, and
- an exact quadratic completion identity around that field.

Those four points are what the "local closure" deliverable was always
supposed to provide. They hold under the corrected sign analysis. The
runner cited above validates the negative-definite character of `H_D`
and the existence/uniqueness of `F_*` numerically over random
positive-definite backgrounds.

## Honest status

Current direct-universal route:

- exact scalar observable level
- exact `3+1` lift level
- exact tensor variational level
- exact canonical block / constraint level
- exact isotropic glue level
- exact invariant-family nonlinear level
- exact positive-background extension level
- exact **definite-background** (negative-definite `K_GR`) local closure level

This is the furthest disciplined gravity claim the current branch can
honestly support, with the operator polarity now stated correctly.
