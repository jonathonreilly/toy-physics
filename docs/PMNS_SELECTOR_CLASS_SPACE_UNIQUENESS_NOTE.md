# PMNS Selector Class-Space Uniqueness

**Date:** 2026-04-15
**Status:** support - structural or confirmatory support note
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_selector_class_space_uniqueness.py`

## Question

After the missing PMNS selector is reduced to a sector-odd mixed bridge
supported only on the non-universal locus, is there still any residual
class-level selector freedom left on the reduced branch-class surface?

## Bottom line

Only one real direction remains.

On the reduced branch-class surface

`X_red = {U_1, U_2, N_nu, N_e}`,

the exact current-bank constraints are:

- `U_1` and `U_2` are `sigma`-fixed universal classes
- `N_nu` and `N_e` form the exchanged non-universal orbit
- any future selector may be reduced to a sector-odd part
- that sector-odd part vanishes on the universal locus

So the admissible class-level selector space is

`span_R { chi_N_nu - chi_N_e }`.

Equivalently: up to overall normalization, the reduced class-level selector is
already unique. It is just the **signed non-universality indicator**.

## Atlas and package inputs

This theorem reuses:

- `PMNS selector sector-odd reduction`
- `PMNS selector non-universal support reduction`

And, as structural framing from another closed lane:

- `Majorana unique source slot`

That import is not a dynamics import. It is a safe structural reuse: once a
channel space is reduced to one support locus and one symmetry class, the
remaining admissible object can collapse to a one-dimensional slot.

## Why this is stronger than the non-universal support note

The non-universal-support note says where a future selector may be nonzero.

This note goes one step further. It says that on the reduced class quotient,
there is no further selector-shape freedom to search over. Any admissible
class-level selector is proportional to one canonical basis element.

So the remaining science is not:

- another class-level parity choice
- another class-level support family
- another independent class-level selector coordinate

It is the microscopic realization and activation law of a **unique** reduced
selector class.

## Theorem-level statement

**Theorem (Uniqueness of the reduced PMNS selector class).** Assume the exact
PMNS selector sector-odd reduction theorem and the exact PMNS selector
non-universal support reduction theorem. Then on the reduced branch-class
surface `X_red = {U_1, U_2, N_nu, N_e}`:

1. any admissible future selector `F` can be replaced by a sector-odd part
   `F_-`
2. `F_-` vanishes on the universal classes `U_1, U_2`
3. sector exchange gives `F_-(N_e) = -F_-(N_nu)`

Therefore the admissible real vector space of reduced class-level selectors is
one-dimensional, spanned by

`S_cls = chi_N_nu - chi_N_e`.

## What this closes

This closes the last class-level ambiguity in the current selector reduction.

It is now exact that the remaining selector gap is not a search over multiple
reduced class-level bridge shapes. On the reduced quotient, there is only one
candidate class left, up to scale.

## What this does not close

This note does **not** prove:

- that the unique reduced selector class is realized microscopically
- that its coefficient is nonzero
- that the bank already derives the underlying bridge functional
- that full PMNS closure is complete

It is a class-space uniqueness theorem only.

## Command

```bash
python3 scripts/frontier_pmns_selector_class_space_uniqueness.py
```
