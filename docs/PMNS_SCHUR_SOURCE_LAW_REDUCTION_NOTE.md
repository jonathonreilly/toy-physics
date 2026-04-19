# PMNS Schur Source-Law Reduction

**Date:** 2026-04-15  
**Status:** exact reduction theorem for the remaining PMNS derivation target
inside the full `Cl(3)` on `Z^3` Grassmann Gaussian  
**Script:** `scripts/frontier_pmns_schur_source_law_reduction.py`

## Question

After the projected source-law reduction, is the projected PMNS source law
itself still an extra object that must be invented beyond `Cl(3)` on `Z^3`?

## Bottom line

No.

Once the relevant effective lepton finite blocks are identified inside the full
finite Grassmann Gaussian, the projected source law is exact Schur pushforward.

So the remaining target is **not**:

- invent a new PMNS source grammar
- invent a new projected determinant law

It is:

1. derive the effective lepton finite blocks
2. derive one oriented active-block probe direction

inside the full `Cl(3)` on `Z^3` Grassmann system.

## Exact reduction

Let the full finite Gaussian operator split as

`D = [[A,B],[C,F]]`

with the retained lepton block `A` and complement `F`.

For a source `J = [[X,0],[0,0]]` supported only on the retained block, the
finite determinant identity gives

`det(D+J) = det(F) det(A + X - B F^(-1) C)`.

Therefore the retained-block source response is exactly

`log|det(D+J)| - log|det D|`
`= log|det(D_eff + X)| - log|det D_eff|`

with

`D_eff = A - B F^(-1) C`.

So once the effective lepton block is identified, its full projected source law
is exact Schur pushforward from the full `Cl(3)` on `Z^3` Gaussian.

## Consequence for PMNS closure

This means the remaining PMNS target is no longer the projected source law
itself.

That projected source law is automatic once:

- the effective lepton blocks are identified
- the active oriented probe direction is identified

The projected Hermitian linear responses then reconstruct `(H_nu,H_e)`, and one
oriented active non-Hermitian probe fixes the residual sheet bit.

## Theorem-level statement

**Theorem (PMNS Schur/source-law reduction).** Assume the exact observable
principle from `Cl(3)` on `Z^3`, the exact projected source-law reduction, and
the exact finite-dimensional Schur determinant identity. Then:

1. once the effective lepton finite blocks are identified inside the full
   Grassmann Gaussian, the projected lepton source law is exact Schur
   pushforward and is therefore derived rather than admitted
2. the projected Hermitian linear source law on those blocks reconstructs the
   full lepton Hermitian pair `(H_nu,H_e)`
3. one oriented active-block probe fixes the residual active two-Higgs sheet

Therefore the clean remaining target from `Cl(3)` on `Z^3` is not a new PMNS
source law but the derivation of:

- the effective lepton blocks
- one active probe direction

inside the full finite Grassmann Gaussian.

## What this closes

This closes the source-law-invention loophole.

The projected PMNS source law is no longer an extra formal object once the
relevant finite blocks are known.

## What this does not close

This note does **not** derive the effective lepton blocks themselves from
`Cl(3)` on `Z^3`, nor the active probe direction.

That is now the clean remaining target.

## Command

```bash
python3 scripts/frontier_pmns_schur_source_law_reduction.py
```
