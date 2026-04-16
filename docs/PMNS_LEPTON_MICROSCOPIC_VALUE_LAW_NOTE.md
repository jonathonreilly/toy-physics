# PMNS Lepton Microscopic Value Law

**Date:** 2026-04-15  
**Status:** exact microscopic value-law theorem for the effective lepton
operator pair  
**Script:** `scripts/frontier_pmns_lepton_microscopic_value_law.py`

## Question

Once the PMNS lane has already identified

- the lepton supports `E_nu`, `E_e`
- the canonical lepton Schur complement
- and the exact charge-localized split `L_nu ⊕ L_e`,

what is the exact microscopic value law for `L_nu` and `L_e`?

## Bottom line

They are the charge-sector Schur complements of the microscopic operator.

Write the full charge-preserving finite `Cl(3)` on `Z^3` Gaussian as

`D = D_0 ⊕ D_- ⊕ D_+`

under the exact charge split

- charge `0`
- charge `-1`
- charge `+1`.

Then the already-fixed lepton supports satisfy

- `E_nu ⊂ E_0`
- `E_e  ⊂ E_-`.

So the exact microscopic value law is:

- `L_nu = Schur_{E_nu}(D_0)`
- `L_e  = Schur_{E_e}(D_-)`

More explicitly, if

```text
D_0 =
[ A_nu  B_nu ]
[ C_nu  F_0  ]
```

on `E_nu ⊕ E_0^rest`, and

```text
D_- =
[ A_e  B_e ]
[ C_e  F_- ]
```

on `E_e ⊕ E_-^rest`, then

- `L_nu = A_nu - B_nu F_0^(-1) C_nu`
- `L_e  = A_e  - B_e  F_-^(-1) C_e`.

So the effective PMNS lepton operators are not extra flavor-side constructs.
They are exact microscopic Schur values in the neutral and charge-`-1`
sectors.

## Why this is sharper than the earlier lepton-Schur note

The previous theorem showed that the canonical lepton Schur complement on
`E_nu ⊕ E_e` splits as `L_nu ⊕ L_e`.

This theorem goes one level deeper:

- the full microscopic operator already splits by charge
- so `L_nu` and `L_e` are not just subblocks of a larger lepton Schur object
- they are each direct charge-sector Schur complements of the microscopic
  operator

That is the exact microscopic value law.

## Exact reduction

### 1. Charge preservation block-diagonalizes the microscopic operator

On the gauge-preserving microscopic class,

`[D,Q] = 0`.

Therefore the full finite Gaussian splits exactly into charge sectors
`D_0 ⊕ D_- ⊕ D_+`.

### 2. The lepton supports sit in definite charge sectors

By one-generation matter closure:

- neutrinos lie on charge `0`
- charged leptons lie on charge `-1`

and by retained three-generation structure each becomes a triplet support.

So:

- `E_nu ⊂ E_0`
- `E_e  ⊂ E_-`.

### 3. `L_nu` and `L_e` are direct sector Schur complements

Because the microscopic operator is already charge block diagonal, the positive
charge sector `D_+` does not enter the effective lepton value law at all.

The neutral and charge-`-1` sectors close independently, and the exact value
laws are:

- `L_nu = Schur_{E_nu}(D_0)`
- `L_e  = Schur_{E_e}(D_-)`.

### 4. Source responses factorize sector-by-sector

For sources supported on `E_nu` and `E_e`, the exact scalar source response
splits additively into:

- a neutral-sector response through `L_nu`
- a charge-`-1`-sector response through `L_e`

So the PMNS microscopic value law is already charge-localized before any PMNS
parametrization is introduced.

## Theorem-level statement

**Theorem (Microscopic value law for the effective PMNS lepton operators).**
Assume:

1. one-generation matter closure
2. retained three-generation matter structure
3. the exact observable principle from `Cl(3)` on `Z^3`
4. the exact lepton charge Schur-localization theorem
5. the charge-preserving full microscopic finite Gaussian class

Then:

1. the microscopic operator splits exactly by charge as `D_0 ⊕ D_- ⊕ D_+`
2. the lepton supports satisfy `E_nu ⊂ E_0`, `E_e ⊂ E_-`
3. the effective PMNS lepton operators are exactly
   - `L_nu = Schur_{E_nu}(D_0)`
   - `L_e  = Schur_{E_e}(D_-)`
4. source-supported responses on `E_nu` and `E_e` factor exactly through those
   two charge-sector Schur complements

Therefore the microscopic PMNS block-value law is already exact:
`L_nu` and `L_e` are the neutral- and charge-`-1`-sector Schur values of the
full `Cl(3)` on `Z^3` operator.

## What this closes

This closes the remaining ambiguity about what the PMNS effective block values
*are* microscopically.

The remaining open problem is no longer to identify a PMNS-side bridge object.
It is only:

- derive or evaluate the actual microscopic sector operators `D_0` and `D_-`
  from `Cl(3)` on `Z^3`, and then take their exact Schur complements.

## What this does not close

This note does **not** yet evaluate the actual entries of `D_0` or `D_-` from
the full microscopic `Cl(3)` on `Z^3` construction.

So it does not yet give numerical or closed symbolic entries for `L_nu` and
`L_e`.

It gives their exact microscopic value law.

## Command

```bash
python3 scripts/frontier_pmns_lepton_microscopic_value_law.py
```
