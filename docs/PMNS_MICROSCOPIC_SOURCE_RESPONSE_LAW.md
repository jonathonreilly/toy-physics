# PMNS Microscopic Source-Response Law

**Date:** 2026-04-16  
**Status:** exact microscopic source-response theorem on the fixed lepton supports  
**Script:** `scripts/frontier_pmns_microscopic_source_response_law.py`

## Question

Working only from `Cl(3)` on `Z^3`, what does the microscopic source-response
route on the fixed lepton supports `E_nu` and `E_e` actually determine?

## Bottom line

The microscopic source-response law is exact Schur pushforward to the Hermitian
lepton pair `(H_nu, H_e)`.

On the fixed supports, the 18 Hermitian linear responses reconstruct
`(H_nu, H_e)` exactly, and the Hermitian pair already reads the active
one-sided branch.

But the same source-response law is blind to the residual right-sheet / Y-level
data. Distinct canonical Yukawa sheets with the same `H` give identical
Hermitian source responses. So this route fixes a genuine subset of the
unresolved microscopic data, but not full microscopic closure.

## Exact reduction

Let the full microscopic operator be split into the retained lepton block and
the complement:

`D = [[A,B],[C,F]]`

For a source `J` supported only on the retained lepton block, the finite
determinant identity gives

`det(D+J) = det(F) det(A + J - B F^(-1) C)`.

Therefore the retained-block source response is exactly

`log|det(D+J)| - log|det D|`
`= log|det(D_eff + J)| - log|det D_eff|`

with

`D_eff = A - B F^(-1) C`.

After the fixed lepton supports are identified, the microscopic source-response
law is therefore exact Schur pushforward.

## What it fixes

On the fixed supports, the nine Hermitian source directions on `E_nu` and the
nine Hermitian source directions on `E_e` reconstruct the full Hermitian pair
exactly:

`(H_nu, H_e)`.

Once `(H_nu, H_e)` is known, the active one-sided branch is readable directly:
the non-diagonal Hermitian block is the active branch and the diagonal block is
the passive monomial branch.

So the source-response route genuinely closes the Hermitian-pair subset of the
microscopic problem.

## What it does not fix

The source-response law factors through `H = Y Y^dag`. That makes it blind to
the residual right-sheet / non-Hermitian `Y`-level data.

On a generic active branch there are two canonical sheets with the same `H`,
and they have identical Hermitian source responses on every Hermitian probe.
One oriented non-Hermitian probe distinguishes them, but that probe is not part
of the Hermitian source-response law itself.

So this route does **not** by itself determine:

- the residual sheet bit `s`
- the full microscopic Yukawa representative `Y`
- the remaining non-Hermitian value law

## Theorem-level statement

**Theorem (PMNS microscopic source-response law).** Assume the exact
observable principle from `Cl(3)` on `Z^3`, the exact finite-dimensional Schur
identity, and the fixed lepton supports `E_nu` and `E_e`. Then:

1. the microscopic source-response law on the fixed lepton supports is exact
   Schur pushforward to `(H_nu, H_e)`
2. the Hermitian pair reconstructs the active branch exactly
3. the same source-response law is blind to the residual right-sheet / `Y`
   data and therefore does not close the full microscopic `Y`-level problem

## Meaning for the lane

This is a positive-but-bounded microscopic result.

It closes the Hermitian-pair subset of the unresolved PMNS problem from the
source-response side, but it also proves that the source-response route alone
cannot finish the full positive neutrino closure.

## Verification

```bash
python3 scripts/frontier_pmns_microscopic_source_response_law.py
```
