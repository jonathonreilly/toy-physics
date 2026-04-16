# PMNS Full Lepton Pair Reduction

**Date:** 2026-04-15  
**Status:** exact reduction theorem for the remaining full neutrino target on
the one-sided minimal PMNS classes  
**Script:** `scripts/frontier_pmns_full_lepton_pair_reduction.py`

## Question

After the unified bridge carrier and its full-closure consequences are in hand,
what is the clean single target that still has to be derived from `Cl(3)` on
`Z^3`?

Do we really still need to think in terms of the piecewise bookkeeping objects

- `U_full^nu = (A,B,u,v,delta,rho,gamma,a_sel,s)`
- `U_full^e  = (A,B,u,v,delta,rho,gamma,a_sel,s,m_1,m_2,m_3)`

or is there a sharper non-piecewise target?

## Bottom line

Yes. There is a sharper target.

On the one-sided minimal PMNS classes, full neutrino closure is exactly
equivalent to deriving:

1. the full lepton Hermitian pair `(H_nu, H_e)`
2. one active two-Higgs sheet bit `s in Z_2`

Everything else becomes readable from that pair:

- the active branch is readable from which sector is non-monomial
- the active `2 + 2 + 3` bridge coordinates are readable from the active
  Hermitian matrix
- on the charged-lepton-side branch, the passive neutrino monomial mass triple
  is readable directly from the passive diagonal Hermitian matrix

So the remaining full-closing target from `Cl(3)` on `Z^3` is not best thought
of as the piecewise bookkeeping objects `U_full^nu` and `U_full^e`. It is the
single pair-level target

`((H_nu, H_e), s)`.

## Exact reduction

### 1. Branch selection is readable from the pair

On the one-sided minimal PMNS classes:

- one sector is canonical two-Higgs and therefore non-monomial
- the other sector is monomial and therefore diagonal at the Hermitian level

Therefore the branch is readable directly from the pair `(H_nu, H_e)`:

- if `H_nu` is non-diagonal and `H_e` is diagonal, the branch is `N_nu`
- if `H_e` is non-diagonal and `H_nu` is diagonal, the branch is `N_e`

So for full closure, one does not need a separate branch target once the full
pair law is the target.

### 2. The active bridge data are readable from the active Hermitian matrix

The active Hermitian law already splits exactly as

`H = H_core + B(delta,rho,gamma)`.

Hence from the active member of the pair one reads the exact bridge package

`(A,B,u,v,delta,rho,gamma)`.

So the `2 + 2 + 3` active bridge is not an additional full-closing target once
the pair law is derived. It is part of what is already encoded in the pair.

### 3. The passive monomial triple is readable from the passive Hermitian matrix

On the charged-lepton-side branch, the passive neutrino sector is monomial.

Therefore

`H_nu = diag(m_1^2, m_2^2, m_3^2)`

on the canonical passive branch, and the mass triple is read directly as

`(m_1, m_2, m_3) = sqrt(diag(H_nu))`.

So the passive triple is not a separate target once the full pair law is
derived. It is already contained in the passive Hermitian member of the pair.

### 4. Full coefficient closure adds only one sheet bit

The selected active Hermitian data determine the canonical two-Higgs
coefficients only up to one residual `Z_2` sheet.

So full coefficient closure requires one additional non-Hermitian datum:

`s in Z_2`.

That is the only extra datum beyond the pair itself.

## Theorem-level statement

**Theorem (Full neutrino closure reduces to the lepton Hermitian pair plus one
sheet bit on the one-sided minimal PMNS classes).** Assume the exact
one-sided minimal PMNS branch structure, the exact intrinsic completion
boundary, the exact unified bridge carrier theorem, the exact unified
bridge full-closure consequence theorem, and the exact branch-conditioned
quadratic-sheet closure theorem. Then:

1. the active branch is readable directly from the derived pair `(H_nu, H_e)`
2. the active bridge coordinates `(A,B,u,v,delta,rho,gamma)` are readable
   directly from the active Hermitian member of the pair
3. on the charged-lepton-side branch, the passive neutrino monomial mass
   triple `(m_1,m_2,m_3)` is readable directly from the passive diagonal
   Hermitian member of the pair
4. full coefficient closure then requires exactly one additional active
   two-Higgs sheet bit `s in Z_2`

Therefore full neutrino closure on the one-sided minimal PMNS classes is
equivalent to deriving

`((H_nu, H_e), s)`,

not to separately deriving the piecewise bookkeeping objects
`U_full^nu` and `U_full^e`.

## What this closes

This closes the bookkeeping ambiguity about the remaining target.

It is now exact that the clean full-closing target from `Cl(3)` on `Z^3` is:

- one full lepton-pair Hermitian law
- plus one residual sheet datum

It is **not** best thought of anymore as:

- one branch amplitude target
- one active bridge target
- one passive mass target
- one extra seed-edge target

Those are all readable from the full pair once the pair itself is derived.

## What this does not close

This note does **not** derive:

- the pair `(H_nu, H_e)` from `Cl(3)` on `Z^3`
- the residual sheet bit `s`

So it does not complete neutrino closure by itself. It sharpens the remaining
target to its cleanest exact form.

## Command

```bash
python3 scripts/frontier_pmns_full_lepton_pair_reduction.py
```
