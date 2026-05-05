# PR230 Neutral Off-Diagonal Generator Derivation Attempt

**Status:** exact negative boundary / neutral off-diagonal generator not
derivable from current PR230 surface
**Runner:** `scripts/frontier_yt_neutral_offdiagonal_generator_derivation_attempt.py`
**Certificate:** `outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json`

## Purpose

This block tests the clean neutral-sector version of the remaining bridge:
can the current Cl(3)/Z3 source surface derive the off-diagonal
source/orthogonal neutral generator needed by Burnside, primitive-cone, or
Perron-Frobenius rank-one closure?

The attempt uses outside-math tools only as certificate engines:
Burnside/double-commutant, primitive positive matrices, Schur commutants, GNS
flat extension, and Schur/tensor row contracts.  None of those names is used
as a proof selector.

## Result

The attempt does not close.  Current PR230 rows are source-only or
absence-guarded:

- `C_ss` and `dE_top/ds` define the source coordinate but are block diagonal in
  a source/orthogonal neutral completion.
- `O_H/C_sH/C_HH` source-Higgs pole rows are absent.
- Same-source W/Z response rows and matched top/W covariance are absent.
- Schur `A/B/C` kernel rows are absent.
- The primitive-cone and Burnside gates already show the current neutral
  generator algebra is not irreducible.
- The invariant-ring and GNS attempts leave the two-singlet or missing-row
  obstruction intact.

The runner records a positive acceptance-shape witness: a nonnegative
two-state transfer matrix with source/orthogonal off-diagonal entries can be
strongly connected and primitive.  That witness is not PR230 evidence because
the off-diagonal generator is not derived or measured on the current surface.

## Positive Contract

To make the route positive, a future certificate must supply:

- same-surface origin from the PR230 Cl(3)/Z3 action/source functional or a
  production same-ensemble non-source response row;
- nonzero source/orthogonal neutral entry with normalization and sign;
- full matrix algebra/scalar commutant or positive primitive transfer power;
- isolated lowest neutral pole and source/canonical-Higgs overlap authority;
- a firewall rejecting `H_unit`, Ward authority, observed selectors,
  `alpha_LM`/plaquette/`u0`, reduced pilots, and unit `kappa_s/c2/Z_match`
  shortcuts.

## Claim Boundary

No retained or `proposed_retained` PR230 closure is claimed.  This block does
not write a neutral off-diagonal generator certificate and does not treat the
synthetic primitive witness, source-only rows, Burnside theorem names, GNS
rank labels, Schur method names, or PSLQ/value recognition as physical
top-Yukawa evidence.

## Verification

```bash
python3 scripts/frontier_yt_neutral_offdiagonal_generator_derivation_attempt.py
```
