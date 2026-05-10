# Universal GR Positive-Background Local Closure on `PL S^3 x R`

**Status:** bounded local linear-algebra closure, conditional on the imported
isotropic-glue authority and the SPD-background `B_D`/`Lambda_R` bridge being
independently retained. Within those imports, this note proves a class-A
algebraic closure: `K_GR(D) = H_D ⊗ Lambda_R` is symmetric negative-definite,
hence invertible with a unique stationary boundary field and an exact quadratic
completion identity. It is **not** a route-level closure of full universal GR.
**Date:** 2026-04-14 (sign character corrected 2026-05-01; audit-narrowing
refresh 2026-05-10)
**Branch:** `codex/review-active`
**Role:** direct universal route / bounded local algebraic closure
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only.
**Runner:** scripts/universal_gr_positive_background_local_closure.py

## Audit boundary

The runner numerically validates the algebraic sign, invertibility, stationary
equation, and completion identity for sampled dense finite-dimensional
instances. Those sampled checks support the class-A algebraic content of this
note. They do **not** independently retain the upstream isotropic-glue
authority or the SPD-background `B_D`/`Lambda_R` bridge.

**Admitted authority inputs (cited but not derived in this note):**

- the exact isotropic glue assembly
  [`UNIVERSAL_GR_ISOTROPIC_GLUE_OPERATOR_NOTE.md`](UNIVERSAL_GR_ISOTROPIC_GLUE_OPERATOR_NOTE.md)
  — which itself is bounded structural assembly conditional on its own
  imports, not retained-grade. So the universal SPD-background `B_D` family
  used in this note is also conditional on those upstream imports.
- the slice generator `Lambda_R` symmetric-positivity, taken from the Route-2
  slice-generator construction (not re-derived here).

If the upstream isotropic-glue / `Lambda_R` chain is later promoted to
retained-grade, the bounded algebraic closure recorded here propagates
forward without further repair on this row.

## Verdict (scope-bounded)

Conditional on the imports above, the direct-universal route admits an exact
**definite-background local algebraic closure** on `PL S^3 x R`: for every
real positive-symmetric background `D` and source `J`, there is a unique
exact stationary boundary field `F_*(D, J) = K_GR(D)^{-1} J` and an exact
quadratic completion identity around it.

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

At this bounded scope, the direct-universal route assembles:

- a scalar observable level (imported)
- a `3+1` lift level (imported)
- a tensor variational level (imported)
- a canonical block / constraint level (imported)
- an isotropic glue level (imported, bounded structural assembly)
- an invariant-family nonlinear level (imported)
- a positive-background extension level (imported)
- a **definite-background** local algebraic closure level (this note,
  bounded; class-A algebra conditional on the imports above).

This is the furthest disciplined definite-background local algebraic claim
the current branch supports given the imported chain. It is **not** a route-
level closure of full universal GR — the residual gap to a Lorentzian /
unrestricted-GR action remains global and interpretive, and the upstream
authorities themselves are not yet retained-grade.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [universal_gr_isotropic_glue_operator_note](UNIVERSAL_GR_ISOTROPIC_GLUE_OPERATOR_NOTE.md)
