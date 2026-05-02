# Assumptions and Imports

## Inputs treated as retained (not under audit here)

1. **Wilson 3+1 source surface.** The accepted finite-volume Wilson
   action with three spatial directions and one derived-time direction
   in temporal gauge. (Cited authority within the source note's
   surrounding atlas chain.)
2. **`SU(3)` character expansion of the central class function**
   `w_beta(g) = exp[(beta/3) Re Tr g]`. Standard Lie-algebraic identity;
   no observation or fit involved.
3. **Bessel-determinant formula** for the one-link Wilson character
   coefficients `c_(p,q)(beta)`. Standard `SU(3)` matrix-element
   identity (Eskola, Polonyi, etc.); used here only as an exact algebraic
   input to compute `a_(p,q)(beta)`.

## Imports retired by this audit move

None. This route does not retire any external import; it only flips
the audit `claim_type` for an already-clean row.

## Imports newly exposed

None. The bounded-theorem reading does not expand the input set.
The residual environment data remain explicitly outside scope and are
tracked in companion notes.

## Forbidden imports / no-go routes

- Do not silently absorb the residual environment data into this row.
  The bounded-theorem statement is exactly the *factorization*; any
  attempt to claim P(6) closure here is a no-go on this row.
- Do not reuse PDG / lattice-QCD comparators here. The runner's
  `|local-only - 0.5934| = 0.141` check is a *support-class
  observation* about the residual being non-trivial, not a derivation
  input.
