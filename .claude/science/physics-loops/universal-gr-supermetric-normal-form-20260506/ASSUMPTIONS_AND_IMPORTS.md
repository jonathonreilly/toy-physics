# Assumptions And Imports

## In-Scope Inputs

- Route scalar generator:
  `W[J] = log|det(D+J)| - log|det D|`.
- Universal Hessian definition:
  `B_D(h,k) := D^2 W[0](h,k)` on symmetric `3+1` metric-source
  perturbations.
- Positive invariant background:
  `D = diag(a,b,b,b)`, `a,b > 0`.
- Canonical symmetric lapse / shift / trace / shear basis.

## Imports Retired By This Block

- The Hessian/supermetric identification is no longer an asserted
  substitution. It is derived from Jacobi's formula and
  `partial_t A^-1 = -A^-1 k A^-1`.
- The block weights are no longer asserted. They are evaluated from the
  derived trace contraction and checked symbolically.

## Remaining Out-Of-Scope Imports

- The scalar-observable selection premises behind the log-det generator are
  upstream to this note.
- The `PL S^3 x R` route remains a kinematic background context, not a full
  GR dynamics theorem.
- The Einstein/Regge gluing law remains open and is not claimed here.
