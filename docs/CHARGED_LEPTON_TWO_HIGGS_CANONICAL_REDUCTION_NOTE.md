# Charged-Lepton Two-Higgs Canonical Reduction Theorem

**Date:** 2026-04-15
**Status:** exact reduction/counting theorem on the minimal surviving
charged-lepton-side extension class
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_charged_lepton_two_higgs_canonical_reduction.py`

## Question

If the charged-lepton sector, rather than the neutrino sector, is the first
lepton Yukawa lane to leave the single-Higgs monomial class, what is the exact
remaining freedom on that minimal charged-lepton extension?

## Bottom line

It is structurally the same size as the minimal neutrino-side extension.

Up to generation relabeling and charged-lepton field rephasings, every
distinct-offset charged-lepton two-Higgs texture reduces to one canonical
support class

`Y_e = A_e + B_e C`

with `C` the forward `3`-cycle and `A_e, B_e` diagonal.

After exact phase reduction, the generic canonical point has the form

`Y_e,can = diag(x^e_1,x^e_2,x^e_3) + diag(y^e_1,y^e_2,y^e_3 e^{i delta_e}) C`

with all moduli positive and one surviving phase `delta_e`.

So the minimal exact charged-lepton-side extension class also carries exactly
**seven real physical quantities**:

- six positive moduli
- one phase

## Atlas and axiom inputs

This theorem reuses:

- `Lepton single-Higgs PMNS triviality theorem`
- `Neutrino Dirac two-Higgs escape theorem`

The key exact reuse fact is already in the single-Higgs lepton theorem: the
charged-lepton support analysis depends only on one effective `Z_3` offset, not
on whether that offset arose directly from `H` or from a conjugated Higgs
insertion.

So the same two-offset support algebra applies on the charged-lepton lane.

## Why the offset-pair label is not a remaining physical ambiguity

There are three unordered distinct effective-offset pairs:

- `(0,1)`
- `(0,2)`
- `(1,2)`

Any such texture has the form

`Y_e = D_a P_a + D_b P_b`

with `P_a != P_b`.

Exactly as on the neutrino side, right-multiplying by `P_a^dag` makes one term
diagonal and leaves a relative permutation which is always a nontrivial
`3`-cycle. All such cycles are conjugate by generation relabeling.

Therefore all distinct charged-lepton offset pairs reduce to the same
canonical support class `A_e + B_e C`.

## Exact phase reduction

Write the canonical support class as

`Y_e = diag(a^e_1,a^e_2,a^e_3) + diag(b^e_1,b^e_2,b^e_3) C`.

This starts with `6` complex numbers, i.e. `12` real parameters.

Diagonal charged-lepton left/right rephasings then:

1. make all three `a^e_i` positive and real
2. make two of the three `b^e_i` positive and real
3. leave one common phase direction redundant

So exactly one invariant phase survives. A convenient generic normal form is

`Y_e,can = diag(x^e_1,x^e_2,x^e_3) + diag(y^e_1,y^e_2,y^e_3 e^{i delta_e}) C`

with all `x^e_i > 0`, all `y^e_i > 0`.

## Exact parameter count

The generic charged-lepton two-Higgs lane therefore carries:

- `12` starting real parameters
- minus `5` exact removable phase directions

leaving

`12 - 5 = 7`

physical real quantities.

## The theorem-level statement

**Theorem (Canonical reduction of the minimal two-Higgs charged-lepton lane).**
Assume the exact single-Higgs lepton-sector PMNS triviality theorem and a
charged-lepton Yukawa lane with two distinct effective `Z_3` offsets. Then:

1. every such charged-lepton texture is equivalent up to generation relabeling
   to the canonical support class `Y_e = A_e + B_e C`
2. after exact charged-lepton field rephasings, the generic point has normal
   form
   `diag(x^e_1,x^e_2,x^e_3) + diag(y^e_1,y^e_2,y^e_3 e^{i delta_e}) C`
3. the minimal charged-lepton-side extension class therefore carries exactly
   `7` real physical quantities

So if the charged-lepton sector is the first non-monomial lane, its exact
remaining gap is also a seven-quantity problem rather than a generic complex
`3 x 3` texture.

## What this closes

This closes the charged-lepton-side analogue of the neutrino two-Higgs
reduction.

It is now exact that:

- the charged-lepton minimal non-monomial lane is canonical up to relabeling
- its remaining unknown is not a generic matrix family
- its exact residual freedom is seven real quantities

## What this does not close

This note does **not** derive:

- the seven charged-lepton quantities
- a selector choosing the charged-lepton-side branch over the neutrino-side one
- a cross-sector relation tying the charged-lepton and neutrino canonical lanes

It is a reduction theorem only.

## Command

```bash
python3 scripts/frontier_charged_lepton_two_higgs_canonical_reduction.py
```
