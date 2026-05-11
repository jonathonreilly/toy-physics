# Universal GR Isotropic Glue Operator on `PL S^3 x R`

**Status:** bounded structural-assembly note. The note assembles already-derived
local Hessian, slice-generator `Lambda_R`, canonical block projectors, and
Schur-irreducibility ingredients into a single covariant quadratic operator
`K_GR^iso(D) = M_D ⊗ Lambda_R` on the invariant background `D = diag(a,b,b,b)`.
It is **not** an axiom-first uniqueness theorem; the "no remaining covariant
quadratic freedom" statement is the bookkeeping consequence of the imported
ingredients above, not a derivation closing them.
**Date:** 2026-04-14 (audit-narrowing refresh: 2026-05-10)  
**Branch:** `codex/review-active`  
**Role:** direct universal route / structural-assembly step
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane. The
`bounded_theorem` label is a source-side claim-boundary declaration,
not an audit verdict; the prior `bounded_structural_assembly` label
was non-canonical (the audit-pipeline `compute_effective_status.py`
recognizes `positive_theorem`, `bounded_theorem`, `no_go`,
`open_gate`, `decoration`, `meta`), and the 2026-05-10 audit verdict's
repair-target option (b) "narrow the claim to an explicitly
hypothetical definition over named assumed inputs" is implemented
by retyping to `bounded_theorem` with the four imports formalized
as bounded admissions in §"Bounded admissions" below.

## Bounded admissions

The load-bearing claim is **conditional on the four bounded admissions**
below. None of (BA-1)–(BA-4) is derived in this note; each is admitted
as a named bounded sister-authority input. The chain closes class-A
algebraically from (BA-1)–(BA-4) plus elementary tensor-product
algebra; the chain does **not** derive the admissions themselves.

(BA-1) **Local universal Hessian.** The exact local universal Hessian

```text
M_D = a^{-2} P_lapse + (ab)^{-1} P_shift + b^{-2} P_trace + b^{-2} P_shear
```

on the invariant background `D = diag(a, b, b, b)` is admitted. Taken
from the support-tier discrete-Einstein/Regge lift chain.

(BA-2) **Route-2 slice generator.** The exact slice generator
`Lambda_R` (symmetric and positive on the invariant block) is admitted.
Taken from the Route-2 slice-generator construction.

(BA-3) **Canonical `3+1` block projectors.** The lapse / shift / trace /
shear block projectors `(P_lapse, P_shift, P_trace, P_shear)` are
admitted as canonical and exact. Taken from the canonical `3+1`
block-localization chain.

(BA-4) **Invariant-background Schur irreducibility.** The
Schur-irreducibility statement on the shift and shear sectors over the
invariant background is admitted. Taken from the invariant-background
Schur localization.

## Audit boundary

This note assembles imported objects into one composite operator on the
invariant background `D = diag(a,b,b,b)`. The "uniqueness" language used
historically below has been narrowed: the operator `K_GR^iso(D)` is the
**unique covariant quadratic combination of the four imported ingredients
listed below**, not a uniqueness theorem over all possible covariant quadratic
operators on `PL S^3 x R`. Eliminating other covariant quadratic terms requires
(BA-4) Schur-irreducibility and (BA-3) block-localization to be
independently accepted.

This note does **not** re-derive (BA-1)–(BA-4). It only states that,
conditional on them, the tensor-product combination
`K_GR^iso(D) = M_D ⊗ Lambda_R` is the unique covariant quadratic
combination that uses each imported ingredient exactly once and
respects the imported block decomposition.

## Verdict (scope-bounded)

The direct universal branch assembles, at this bounded scope, into the
**single covariant quadratic combination** of the four imported ingredients:

`K_GR^iso(D) = M_D ⊗ Lambda_R`

with

`M_D = a^-2 P_lapse + (ab)^-1 P_shift + b^-2 P_trace + b^-2 P_shear`.

This is a bookkeeping assembly, not a uniqueness theorem over arbitrary
covariant quadratic operators on `PL S^3 x R`. Any stricter uniqueness claim
would require a retained-grade derivation of the four imported ingredients
and an independent argument excluding covariant quadratic terms outside the
imported block decomposition.

## Exact inputs

Already exact on the branch:

- scalar observable generator
- exact `3+1` lift `PL S^3 x R`
- exact unique symmetric quotient kernel
- exact canonical lapse / shift / trace / shear block localization
- exact invariant-background Schur localization
- exact isotropic supermetric normal form
- exact slice generator `Lambda_R`

The only question was whether these are merely compatible objects or whether
they already force one exact glued operator.

## Bounded structural-assembly statement

Conditional on the four admitted authority inputs above (each of which lives
on its own support-tier authority — none re-derived here):

1. the local universal Hessian `M_D = a^-2 P_lapse + (ab)^-1 P_shift +
   b^-2 P_trace + b^-2 P_shear` on the invariant background is taken as given;

2. the Route-2 slice generator `Lambda_R` is taken as symmetric and positive on
   the invariant block;

3. the canonical block projectors are taken as canonical and exact;

4. the shift and shear sectors are taken as irreducible scalar Schur blocks
   over the invariant background;

the **unique covariant quadratic combination of these imported ingredients**
that uses each ingredient exactly once and respects the imported block
decomposition is

`K_GR^iso(D) = M_D ⊗ Lambda_R`.

This is a bounded structural-assembly statement, not a uniqueness theorem
over arbitrary covariant quadratic operators on `PL S^3 x R`. The
"no remaining covariant quadratic freedom" phrase historically used here
refers only to freedom *within the four imported ingredients*; freedom
outside the imported block decomposition is not addressed.

## Why this is the right Einstein/Regge operator on the current route

This operator has the right exact features simultaneously:

- local metric-channel weights from the universal Hessian
- exact slice dynamics from the Schur boundary action
- canonical Hamiltonian / momentum / spatial block split
- exact restriction to the scalar bridge surface (legacy alias: `A1`)

On the scalar bridge core, the operator reduces to the exact restricted discrete
Einstein/Regge lift after the background-rescaling already encoded by
`M_D`.

On the shift and shear sectors, Schur irreducibility leaves no additional
covariant block freedom.

So on the invariant background, this is the unique covariant quadratic
combination of the four imported ingredients within the imported block
decomposition. No claim is made here about uniqueness outside that
decomposition.

## What is now assembled (at this bounded scope)

The direct universal branch assembles at this bounded scope into:

- a single composite isotropic quadratic `3+1` operator
  `K_GR^iso(D) = M_D ⊗ Lambda_R` on `PL S^3 x R`, conditional on the four
  imported ingredients above remaining valid.

That is stronger than:

- mere localization
- mere supermetric normal form
- mere separate slice dynamics

only in the bookkeeping sense that it groups the four imported ingredients
into one composite expression. It is not stronger as a derivation, because
the four ingredients themselves are imported, not re-derived here.

## What remains open

If the standard is stricter than the current direct-universal branch,
the remaining issue is no longer this operator.

The only remaining escalation would be:

- nonlinear completion beyond the exact quadratic invariant surface
- widening beyond the invariant `diag(a,b,b,b)` background family

Those are genuine next ladders, but they are beyond the direct-universal
quadratic gluing problem itself.

## Honest status

At this bounded scope, the direct universal route assembles:

- a scalar observable level (imported)
- a `3+1` lift level (imported)
- a quotient-kernel level (imported)
- a canonical block-localization level (imported)
- an invariant-background Schur-localization level (imported)
- a local isotropic supermetric-normal-form level (imported)
- a structural-assembly composite isotropic quadratic operator on the
  invariant background `D = diag(a,b,b,b)`, conditional on the imports above.

This is a structural-assembly checkpoint, not a closure theorem on its own.
Any stronger claim on this row requires retained-grade authorities for the
imported ingredients and a separate uniqueness argument outside the imported
block decomposition.
