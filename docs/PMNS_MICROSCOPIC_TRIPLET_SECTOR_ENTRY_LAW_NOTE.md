# PMNS Microscopic Triplet-Sector Entry Law

**Date:** 2026-04-15  
**Status:** exact physical-triplet sector-entry theorem  
**Script:** `scripts/frontier_pmns_microscopic_triplet_sector_entry_law.py`

## Question

After reducing the PMNS lane to the effective lepton operators and then to the
charge-sector microscopic value law, what are the **actual entries** of the
neutral and charge-`-1` sector operators on the retained physical lepton
surface?

## Bottom line

On the retained physical three-generation lepton surface, the PMNS-relevant
microscopic sector representatives are already `3 x 3` generation operators:

- `D_0^trip` on `E_nu = span{nu_0,nu_1,nu_2}`
- `D_-^trip` on `E_e  = span{e_0,e_1,e_2}`.

Their exact entry patterns are already fixed by the `Cl(3)` on `Z^3`
derivation stack:

### Single-Higgs fixed-offset lane

For one effective Higgs `Z_3` offset `q in {0,+1,-1}`,

`D_s^trip(q) = diag(a_1,a_2,a_3) P_q`

with `P_q` one of the three exact permutation supports. So the actual entries
are monomial:

- one nonzero entry in each row
- one nonzero entry in each column
- support fixed exactly by the retained `Z_3` charge pattern.

### Minimal two-Higgs lane

On the canonical two-Higgs class,

`D_s^trip = A_s + B_s C`

with

- `C` the forward `3`-cycle
- `A_s` diagonal
- `B_s` diagonal.

In canonical normal form,

```text
D_s^trip =
[ x_1              y_1              0 ]
[ 0                x_2              y_2 ]
[ y_3 e^{i delta}  0                x_3 ]
```

So the actual triplet-sector entries are already explicit up to the coefficient
values.

### Weak-axis seed patch

On the exact weak-axis seed patch, the active triplet entries reduce further to

- `x I + y C`, or
- the exchange sheet `y I + x C`.

So even there the matrix entries are explicit up to one residual global sheet
bit.

## Why this is sharper than the earlier microscopic value-law note

The earlier note showed only that

- `L_nu = Schur_{E_nu}(D_0)`
- `L_e  = Schur_{E_e}(D_-)`.

That still left the impression that the relevant microscopic sector operators
were abstract.

This note sharpens the statement on the retained **physical triplet surface**:

- the PMNS-relevant neutral and charge-`-1` operators are already triplet
  operators
- their support classes are already exact
- their actual entry patterns are already explicit

So the remaining gap is no longer “what shape are the sector matrices?” It is
only:

- the coefficient/value law
- and, on the weak-axis seed patch, one residual sheet bit.

## Exact reduction

### 1. The retained physical lepton surface is already `3 + 3`

By one-generation matter closure, retained three-generation matter structure,
and the PMNS support-identification reduction:

- `E_nu = span{nu_0,nu_1,nu_2}`
- `E_e  = span{e_0,e_1,e_2}`.

So the PMNS-relevant sector representatives are `3 x 3`.

### 2. Single-Higgs entries are exact monomial matrices

By the exact `Z_3` support trichotomy and the single-Higgs lepton no-mixing
results, any retained single-Higgs lepton-sector operator has the exact form

`diag(a_1,a_2,a_3) P_q`.

### 3. Minimal two-Higgs entries are exact `A + B C`

By the neutrino-side and charged-lepton-side canonical two-Higgs reductions,
every distinct-charge two-Higgs lane reduces to one canonical support class

`A_s + B_s C`.

So the actual entries are already the explicit `3 x 3` pattern above.

### 4. One-sided minimal PMNS classes give explicit sector pairs

Therefore the branch-conditioned physical triplet-sector pairs are:

- neutrino-side branch:
  `D_0^trip = A_nu + B_nu C`,
  `D_-^trip = diag(a_e1,a_e2,a_e3) P_q`
- charged-lepton-side branch:
  `D_0^trip = diag(a_nu1,a_nu2,a_nu3) P_q`,
  `D_-^trip = A_e + B_e C`.

### 5. The weak-axis seed patch closes the active entries further

On the exact seed patch, the active triplet entries reduce to

- `x I + y C`
- or `y I + x C`.

So the active entry law closes there up to one sheet exchange.

## Theorem-level statement

**Theorem (Microscopic triplet-sector entry law on the retained PMNS lane).**
Assume:

1. `Cl(3)` on `Z^3`
2. one-generation matter closure
3. retained three-generation matter structure
4. PMNS lepton support identification reduction
5. the exact single-Higgs and two-Higgs support/canonical-reduction theorems

Then on the retained physical lepton triplet surface:

1. the PMNS-relevant neutral and charge-`-1` sector representatives are
   `3 x 3` operators `D_0^trip` and `D_-^trip`
2. on a single-Higgs fixed-offset lane they are exactly monomial matrices
   `diag(a_1,a_2,a_3) P_q`
3. on a minimal two-Higgs lane they are exactly canonical matrices
   `A_s + B_s C`
4. on the weak-axis seed patch the active entries reduce to
   `x I + y C` up to one residual sheet exchange

Therefore the actual retained physical-triplet entries of the microscopic
neutral and charge-`-1` lepton-sector operators are already explicit.

## Boundary

This note does **not** claim:

- the coefficient values are derived
- the residual seed-patch sheet bit is fixed
- every off-triplet spectator entry of a larger ambient charge sector is known

It identifies the actual entries on the retained **physical triplet surface**.

## Command

```bash
python3 scripts/frontier_pmns_microscopic_triplet_sector_entry_law.py
```
