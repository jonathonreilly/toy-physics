# Universal GR Lorentzian Global Atlas Closure on `PL S^3 x R`

**Status:** bounded overlap-covariance check. The note proves a class-A
algebraic identity — the trace bilinear `B_D(h,k) = -Tr(D^-1 h D^-1 k)` is
exactly invariant under invertible chart/frame congruences `D' = S^T D S`,
`h' = S^T h S` — and records the bookkeeping consequence that compatible
local stationary representatives glue compatibly on overlaps. The "unique
global stationary section on a finite atlas" statement is **conditional** on
imported atlas, transition-cocycle, and operator-nondegeneracy hypotheses
that this note does not close.
**Date:** 2026-04-14 (audit-narrowing refresh: 2026-05-10)  
**Branch:** `codex/review-active`  
**Role:** direct universal route / bounded overlap-covariance assembly
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only.

## Audit boundary

This note does two things:

1. **Class-A algebraic check (closed in-note):** the bilinear
   `B_D(h,k) = -Tr(D^-1 h D^-1 k)` is exactly invariant under invertible
   congruence `D' = S^T D S`, `h' = S^T h S`, `k' = S^T k S`. By cyclic
   permutation, `B_{D'}(h',k') = B_D(h,k)`. Equivalently, the local
   operator matrices obey `G_{D'} = T_S^{-T} G_D T_S^{-1}`, and the glued
   operator family transforms by congruence on overlaps. This is exact
   linear algebra and is closed inside the note.

2. **Bookkeeping consequence (conditional):** *if* (a) the underlying finite
   atlas, (b) its transition cocycle, (c) the source/field pairing transforms
   compatibly chart-by-chart, (d) each local Lorentzian operator is
   nondegenerate, then compatible local stationary representatives patch
   compatibly into a global stationary section. The hypotheses (a)-(d) are
   imported, not closed in this note.

**Admitted authority inputs (cited but not derived in this note):**

- a finite atlas of `PL S^3 x R` with its discrete transition cocycle (taken
  from the discrete `3+1` spacetime construction);
- chart-wise nondegeneracy of `K_GR(D)` over the atlas (taken from the
  positive-background local closure with Lorentzian signature extension —
  itself bounded conditional on its own imports);
- chart-wise compatibility of the source/field pairing under congruence
  (taken from the universal local action structure).

If hypotheses (a)-(d) are later upgraded to retained-grade, the bookkeeping
patching consequence inherits that retention without further repair on this
row.

## Verdict (scope-bounded)

Conditional on the imports above, the direct-universal Lorentzian
operator family transforms by exact congruence covariance on chart overlaps.
At this bounded scope, the consequence recorded here is a structural-
assembly statement that compatible local stationary representatives patch
compatibly into a global stationary section on a finite atlas, conditional
on the imported atlas and nondegeneracy data.

The class-A trace identity itself is exact and chart-independent within
this note.

## Exact patching mechanism

The exact local bilinear form is

`B_D(h,k) = -Tr(D^-1 h D^-1 k)`.

Under an invertible chart/frame change `S`,

`D' = S^T D S`,
`h' = S^T h S`,
`k' = S^T k S`,

and therefore

`B_{D'}(h',k') = B_D(h,k)`.

So the local Hessian is not merely covariant in a bookkeeping sense. It is an
exact overlap-invariant quadratic density.

If `T_S` is the induced representation on symmetric `3+1` coefficient vectors,
then the local operator matrices obey the exact overlap relation

`G_{D'} = T_S^{-T} G_D T_S^-1`,

and the glued operator family

`K_GR(D) = H_D ⊗ Lambda_R`

transforms accordingly on overlaps.

## Global stationary section (bookkeeping consequence)

Conditional on the imported hypotheses (a)-(d) above:

- each local Lorentzian operator `K_GR(D)` is nondegenerate (imported);
- the local action densities agree exactly on overlaps (consequence of the
  class-A trace identity proven in-note above);
- the source/field pairing transforms compatibly (imported);

the local stationary solutions transform compatibly across the atlas as a
bookkeeping consequence.

At this bounded scope the structural-assembly statement is:

> *Conditional on the imported atlas, transition-cocycle, source/field-
> pairing-covariance, and operator-nondegeneracy data above*, compatible
> local stationary representatives of the direct-universal Lorentzian
> action family patch compatibly into a global stationary section on the
> finite atlas of `PL S^3 x R`.

The unconditional theorem-form ("direct-universal Lorentzian Einstein/Regge
action family is globally well-defined on finite atlases of `PL S^3 x R`,
and its local stationary representatives patch exactly into a unique global
stationary section") is **not** closed in this note — its hypotheses are
imported, not derived.

## Why this is a class-A algebraic check, not a route-level closure

The earlier positive-background and Lorentzian signature-class objects were
already local/operator-family statements imported from elsewhere. This note
adds:

- one new class-A in-note item: the exact congruence-covariance trace
  identity for `B_D` on overlaps;
- one new bookkeeping item: under the imported hypotheses, compatibility on
  overlaps propagates to compatibility on a finite atlas.

It does **not** independently retain the imported hypotheses. The "first
honest global direct-universal theorem" framing the earlier draft used is
narrowed to: a bounded overlap-covariance assembly conditional on the
imports.

## Honest status

Within the project's discrete `3+1` Einstein/Regge setting, this note adds
to the direct-universal stack:

- one exact in-note class-A overlap-covariance trace identity for `B_D`;
- one bounded structural-assembly bookkeeping statement that, conditional on
  the imported atlas + nondegeneracy + pairing-covariance data, compatible
  local stationary representatives patch compatibly on a finite atlas.

Any unconditional global stationary closure theorem requires a separate
retained-grade bridge that derives the imported hypotheses (atlas finiteness,
nondegeneracy, source/field-pairing covariance) — that bridge is not in this
note.
