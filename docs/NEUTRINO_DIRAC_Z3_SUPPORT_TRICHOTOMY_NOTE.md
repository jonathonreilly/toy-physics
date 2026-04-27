# Neutrino Dirac `Z_3` Support Trichotomy

**Date:** 2026-04-15
**Status:** exact support theorem on the proposed_retained Dirac-neutrino lane,
conditioned on a single Higgs doublet with definite `Z_3` charge
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_dirac_z3_support_trichotomy.py`

## Question

After reducing the retained neutrino-mass problem to the Dirac Yukawa lane,
what does the exact retained `Z_3` generation structure actually force for the
support of the neutrino Dirac matrix `Y_nu`?

Is the remaining object a generic complex `3 x 3` matrix, or does the retained
generation structure constrain it further?

## Bottom line

It is constrained further.

If the retained theory uses a **single Higgs doublet** carrying a definite
generation-`Z_3` charge `q_H in Z_3`, then the neutrino Dirac Yukawa support is
forced into exactly one of three permutation patterns:

- `q_H = 0`: diagonal support
- `q_H = +1`: forward cyclic support
- `q_H = -1`: backward cyclic support

Equivalently: fixing one discrete Higgs-`Z_3` offset collapses the support of
`Y_nu` from a generic `3 x 3` grid to exactly three allowed entries.

So the retained Dirac-neutrino lane is now sharper than a general `Mat_3(C)`
search. The remaining unknown is:

1. which Higgs `Z_3` charge is realized, and
2. the three coefficients on the selected support pattern.

## Atlas and axiom inputs

This theorem reuses the retained/current atlas stack:

- `One-generation matter closure`
- `Three-generation matter structure`
- `Neutrino mass reduction to Dirac lane`

and adds one explicit conditional input:

- a single admitted Higgs doublet with definite generation `Z_3` charge `q_H`

That last input is the honest bridge condition. The theorem does **not** derive
`q_H`.

## Retained generation charges

On the retained three-generation surface, the exact `Z_3` generation charges on
the neutrino lane are:

- left-handed triplet: `q_L = (0, +1, -1)`
- right-handed triplet: `q_R = (0, -1, +1)`

The right-handed charges are the conjugates of the left-handed charges.

## Dirac invariance condition

The Higgs-assisted neutrino Yukawa term is

`epsilon_ab L_L^a H^b nu_R`.

In the retained `Z_3` eigenbasis, a Yukawa entry `Y_ij` is allowed only if

`q_L(i) + q_H + q_R(j) = 0 mod 3`.

Because `q_L` and `q_R` are conjugate triplets, for any fixed `q_H` this
equation has:

- exactly one solution in each row
- exactly one solution in each column

So the support is always a permutation pattern.

## The three exact patterns

### 1. `q_H = 0`

The invariance condition gives:

- `(1,1)`
- `(2,2)`
- `(3,3)`

So `Y_nu` is diagonal in the retained `Z_3` eigenbasis.

### 2. `q_H = +1`

The invariance condition gives:

- `(1,2)`
- `(2,3)`
- `(3,1)`

So `Y_nu` has the forward cyclic support pattern.

### 3. `q_H = -1`

The invariance condition gives:

- `(1,3)`
- `(2,1)`
- `(3,2)`

So `Y_nu` has the backward cyclic support pattern.

These three support patterns are pairwise disjoint, and their union is the full
`3 x 3` support grid.

## Coefficient count

Once `q_H` is fixed, the neutrino Dirac lane is not a 9-entry support problem.
It is a 3-entry support problem:

`Y_nu = sum_k y_k E_k(q_H)`

on the corresponding permutation pattern.

A generic choice of those three coefficients gives rank `3`, so nothing in this
support theorem forces the neutrinos to remain massless.

## The theorem-level statement

**Theorem (Neutrino Dirac `Z_3` support trichotomy).**
Assume the retained three-generation matter structure, the retained reduction of
neutrino mass to the Dirac lane, and a single Higgs doublet with definite
generation `Z_3` charge `q_H in Z_3`. Then the allowed support of the
three-generation neutrino Dirac Yukawa matrix `Y_nu` is exactly one of three
permutation patterns:

- diagonal if `q_H = 0`
- forward cyclic if `q_H = +1`
- backward cyclic if `q_H = -1`

In particular, fixing `q_H` reduces the Dirac support search from nine entries
to three coefficient slots.

## What this closes

This closes the next honest structural question on the retained Dirac lane:

- the remaining problem is **not** a generic `3 x 3` support search
- the unresolved discrete support choice is just the Higgs `Z_3` offset
- after that, only three coefficients remain

This also links the neutrino Dirac lane to the same Higgs-`Z_3` blocker family
that already appears on the CKM / flavor side.

## What this does not close

This note does **not** derive:

- the Higgs `Z_3` charge `q_H`
- the three coefficients on the selected support
- the absolute neutrino masses
- PMNS mixing angles

It is an exact support theorem only.

## Safe wording

**Can claim**

- with a single Higgs doublet of definite `Z_3` charge, the retained neutrino
  Dirac support has only three exact patterns
- fixing `q_H` reduces the Dirac support problem from 9 entries to 3
- the remaining unresolved Dirac problem is `q_H` plus three coefficients

**Cannot claim**

- the Higgs `Z_3` charge is already derived
- the full Dirac neutrino matrix is numerically closed
- the full neutrino spectrum is solved

## Command

```bash
python3 scripts/frontier_neutrino_dirac_z3_support_trichotomy.py
```
