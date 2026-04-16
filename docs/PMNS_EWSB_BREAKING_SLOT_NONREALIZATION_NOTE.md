# PMNS EWSB Breaking-Slot Nonrealization

**Date:** 2026-04-15  
**Status:** exact current-bank boundary theorem on the generic active-branch
Hermitian breaking slots  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_ewsb_breaking_slot_nonrealization.py`

## Question

Once the active one-sided PMNS Hermitian law is decomposed into the exact
EWSB-aligned residual-`Z_2` core plus the three explicit breaking slots

`(d_2-d_3, r_12-r_31, phi)`,

does the current retained bank already derive that three-slot vector?

Or is it only an exact coordinate reduction, with the breaking-slot law still
open?

## Bottom line

It is only a reduction.

The current retained bank:

- exactly isolates the generic active Hermitian branch as
  `aligned core + three breaking slots`
- but does not yet derive the breaking-slot vector itself

More precisely, on the same exact canonical active two-Higgs support class,
there exist full-rank active points satisfying all current support and
Hermitian inverse-problem conditions with different breaking-slot vectors.

So the present bank already gives the right coordinates for the remaining
Hermitian problem, but not yet the law that fixes those coordinates.

## Atlas and axiom inputs

This theorem reuses:

- `Neutrino Dirac two-Higgs canonical reduction`
- `Neutrino Dirac two-Higgs observable inverse problem`
- `PMNS EWSB residual-Z2 Hermitian core`
- `PMNS EWSB alignment nonforcing`
- `PMNS intrinsic completion boundary`

## Why this is exact

The current bank already proves:

1. the active one-sided PMNS branch is the exact canonical two-Higgs branch
2. the active Hermitian inverse problem on that branch is exact and
   seven-dimensional
3. under the explicit EWSB alignment bridge, the active Hermitian law
   collapses to the four-real residual-`Z_2` core
4. the difference between the generic active Hermitian grammar and that core is
   exactly the three-slot vector `(d_2-d_3, r_12-r_31, phi)`
5. the current bank does not force the active branch onto the aligned core

So to test whether the current bank already derives the breaking-slot law, it
is enough to ask whether distinct full-rank active points on the same exact
canonical branch can carry different breaking-slot vectors while still
satisfying all current-bank conditions.

They can.

## Exact nonrealization statement

Take the canonical active branch

`Y = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i phi}) C`.

Its active Hermitian coordinates are

`(d_1, d_2, d_3, r_12, r_23, r_31, phi)`.

The aligned residual-`Z_2` core is the codimension-three locus

`d_2=d_3`, `r_12=r_31`, `phi=0`.

The complementary breaking-slot vector is therefore

`beta = (d_2-d_3, r_12-r_31, phi)`.

On the same exact support class `A + B C`, there exist:

- aligned full-rank points with `beta = (0,0,0)`
- generic full-rank points with `beta != (0,0,0)`
- distinct generic full-rank points with different nonzero `beta`

all while staying on the same exact canonical active branch and satisfying the
current Hermitian inverse-problem conditions.

So the current bank does not yet derive a breaking-slot law.

## Theorem-level statement

**Theorem (Current-bank nonrealization of the active EWSB breaking-slot law).**
Assume the exact canonical active two-Higgs branch theorem, the exact
active-branch Hermitian inverse-problem theorem, the exact residual-`Z_2`
Hermitian-core theorem, and the exact EWSB alignment nonforcing theorem. Then:

1. the generic active Hermitian law splits exactly into
   `aligned residual-Z_2 core + beta`, where
   `beta = (d_2-d_3, r_12-r_31, phi)`
2. there exist distinct full-rank points on the same exact canonical active
   branch with different values of `beta`
3. therefore the current retained bank does not yet derive the breaking-slot
   vector `beta`

So the breaking-slot decomposition is exact, but the breaking-slot law remains
open.

## What this closes

This closes the ambiguity about the status of the three explicit active
breaking slots.

It is now exact that:

- the three-slot vector is real, not bookkeeping
- it is the correct generic complement to the aligned residual-`Z_2` core
- but it is not yet an axiom-side output of the current retained bank

So the next honest derivation target is:

- derive an exact alignment bridge theorem
- or derive the generic three-slot breaking law directly

## What this does not close

This note does **not** derive:

- the alignment bridge theorem
- the four aligned-core parameters
- the three breaking-slot values
- the residual selected-branch coefficient sheet

It is a boundary theorem only.

## Command

```bash
python3 scripts/frontier_pmns_ewsb_breaking_slot_nonrealization.py
```
