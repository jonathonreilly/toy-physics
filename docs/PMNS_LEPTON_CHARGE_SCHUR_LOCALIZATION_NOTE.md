# PMNS Lepton Charge Schur Localization

**Date:** 2026-04-15  
**Status:** exact structural theorem on the effective lepton operator pair  
**Script:** `scripts/frontier_pmns_lepton_charge_schur_localization.py`

## Question

After fixing the lepton supports

- `E_nu = span{nu_0,nu_1,nu_2}`
- `E_e  = span{e_0,e_1,e_2}`,

do the effective lepton operators still have to be invented as extra PMNS-side
objects?

Or are they already forced as canonical charge blocks of the full
`Cl(3)` on `Z^3` finite Gaussian once the lepton Schur complement is taken?

## Bottom line

They are already forced structurally.

On the gauge-preserving full finite Gaussian, let `D` be written on the split

`E_nu ⊕ E_e ⊕ E_rest`.

First take the canonical Schur complement onto the lepton support

`E_lep = E_nu ⊕ E_e`.

Then charge preservation forces the resulting effective lepton operator to
commute with the restricted lepton charge operator

`Q_lep = 0 * P_nu - 1 * P_e`.

Because `0` and `-1` are distinct eigenvalues, the lepton Schur complement
must split exactly as

`L_lep = L_nu ⊕ L_e`

with

- `L_nu = P_nu L_lep P_nu`
- `L_e  = P_e  L_lep P_e`.

So the effective neutrino and charged-lepton operators are not extra support
choices. They are the canonical charge blocks of the lepton Schur complement.

## Exact reduction

### 1. The lepton support pair is already fixed

The retained matter/generation stack already fixes:

- lepton species labels `nu`, `e`
- one physical generation triplet for each species

so the support pair `E_nu ⊕ E_e` is already canonical.

### 2. The lepton Schur complement is the canonical effective lepton operator

By the exact Schur/source-law reduction, once the lepton support is fixed the
effective retained operator is the Schur complement of the full finite Gaussian
onto that support.

So the canonical lepton effective operator is already

`L_lep`.

### 3. Charge preservation forces the `nu/e` block split

On the gauge-preserving operator class, the microscopic operator commutes with
the exact charge operator. Schur complementation preserves that commutation on
invariant supports.

Therefore

`[L_lep, Q_lep] = 0`.

Since `Q_lep` has eigenvalue `0` on `E_nu` and `-1` on `E_e`, any commuting
operator must be block diagonal in that decomposition. Hence:

`L_lep = L_nu ⊕ L_e`.

### 4. Source laws factor through `L_nu` and `L_e` separately

Because the lepton Schur complement is charge block diagonal, source-supported
responses factor exactly:

- sources on `E_nu` factor through `L_nu`
- sources on `E_e` factor through `L_e`
- simultaneous sources add

So the PMNS lane’s effective operator pair is exactly the pair
`(L_nu,L_e)`.

### 5. Intrinsic Hermitian and positive representatives follow canonically

Once `L_nu` and `L_e` are identified, their intrinsic Hermitian data are

- `H_nu = L_nu L_nu^dag`
- `H_e  = L_e  L_e^dag`

and the intrinsic positive representatives are

- `Y_nu,+ = H_nu^(1/2)`
- `Y_e,+  = H_e^(1/2)`.

So the remaining ambiguity is no longer structural. It is only the microscopic
law for the values of `L_nu` and `L_e`.

## Theorem-level statement

**Theorem (Lepton charge Schur localization).** Assume:

1. one-generation matter closure
2. retained three-generation matter structure
3. the exact observable principle from `Cl(3)` on `Z^3`
4. the exact PMNS Schur/source-law reduction
5. the exact lepton support identification reduction
6. the gauge-preserving full finite Gaussian class

Then:

1. the canonical effective lepton operator is the Schur complement `L_lep` on
   the already-fixed support `E_nu ⊕ E_e`
2. `L_lep` commutes with the restricted lepton charge operator
   `Q_lep = 0 * P_nu - 1 * P_e`
3. therefore `L_lep` splits exactly as
   `L_lep = L_nu ⊕ L_e`
4. source-supported responses on `E_nu` and `E_e` factor exactly through
   `L_nu` and `L_e`
5. their intrinsic Hermitian and positive representatives then follow
   canonically

Therefore the effective PMNS lepton operators are already identified
structurally as the canonical charge Schur blocks `(L_nu,L_e)`. The remaining
independent gap is only the microscopic law for their values.

## What this closes

This closes the structural “what are the effective lepton blocks?” question.

The remaining target is no longer:

- identify supports
- identify blocks
- identify a probe direction

It is just:

- derive the values of `L_nu` and `L_e` from `Cl(3)` on `Z^3`

because everything else is now canonical downstream structure.

## What this does not close

This note does **not** derive the actual microscopic values of `L_nu` or `L_e`
from `Cl(3)` on `Z^3`.

It identifies them exactly and canonically.

## Command

```bash
python3 scripts/frontier_pmns_lepton_charge_schur_localization.py
```
