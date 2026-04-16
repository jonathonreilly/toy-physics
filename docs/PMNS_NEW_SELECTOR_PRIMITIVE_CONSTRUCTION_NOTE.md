# PMNS New Selector Primitive Construction

**Date:** 2026-04-15  
**Status:** exact minimal-extension theorem for the restricted Higgs-offset
selector on the canonical `(0,1)` pair  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_new_selector_primitive_construction.py`

## Question

Starting from the restricted Higgs-offset selector on the canonical `(0,1)`
pair, can the current retained bank derive a genuinely new exact selector law?

If not, what is the smallest exact selector primitive that must be admitted
to make a positive selector law mathematically possible?

## Bottom line

The current retained bank does **not** derive a positive selector law.

What it does derive, exactly, is the sharp minimal extension class needed to
realize one:

- the canonical selector reduces to one binary monomial-edge bit on `(0,1)`
- the reduced selector class is one-dimensional on the branch-class quotient
- the reduced microscopic datum is one real amplitude `a_sel`
- the smallest honest positive primitive is a non-additive sector-sensitive
  mixed bridge on the non-universal locus

So the exact new object is not a new continuous family of selectors. It is a
single primitive with one real amplitude slot and one binary edge selector on
the canonical pair.

## Exact construction

On the compatible weak-axis seed patch, the canonical active coefficients are

`Y_+ = x_+ I + y_+ C`,
`Y_- = y_+ I + x_+ C`.

At the monomial boundary `A = B`, these limit exactly to the two one-Higgs
monomial edges:

`Y_+ -> sqrt(A) I`,
`Y_- -> sqrt(A) C`.

Therefore the remaining selector on the canonical `(0,1)` pair is exactly the
edge selector between these two endpoints.

On the reduced branch-class quotient `X_red = {U_1, U_2, N_nu, N_e}`, the
unique admissible reduced selector class is

`S_cls = chi_N_nu - chi_N_e`.

Hence any future microscopic realization, once admitted, has the reduced form

`B_red = a_sel S_cls`

for one real amplitude

`a_sel in R`.

This is the minimal exact selector primitive.

## Theorem-level statement

**Theorem (Minimal selector primitive on the canonical PMNS seed pair).**
Assume the exact restricted Higgs-offset selector reduction theorem, the exact
selector class-space uniqueness theorem, the exact selector unique-amplitude
slot theorem, and the exact current-stack zero law. Then:

1. the remaining selector on the canonical `(0,1)` pair is exactly the binary
   edge bit between `sqrt(A) I` and `sqrt(A) C`
2. on the reduced quotient, the selector class is unique up to scale and is
   given by `S_cls = chi_N_nu - chi_N_e`
3. any positive selector realization must therefore be a non-additive
   sector-sensitive mixed bridge with one real amplitude slot
4. the current retained bank does not determine `a_sel`

So the smallest exact extension theorem is not a new bank-internal selector
law. It is the explicit minimal primitive that such a law would have to
occupy.

## Positive vs obstruction

Positive statement, conditional on admitting the minimal extension:

- the canonical selector is a one-bit edge choice on `(0,1)`
- the reduced microscopic datum is one real amplitude `a_sel`
- the primitive is `B_red = a_sel (chi_N_nu - chi_N_e)`
- the monomial-edge representatives are `sqrt(A) I` and `sqrt(A) C`

Obstruction statement for the current retained bank:

- no current-bank theorem fixes `a_sel`
- no current-bank theorem chooses the edge bit
- no current-bank theorem derives the primitive from the retained support-plus-
  scalar bank

## What this closes

This closes the selector-shape ambiguity at the strongest exact level the
current bank supports.

It is now exact that the remaining selector problem is:

- discrete on the canonical pair
- one-dimensional on the reduced quotient
- realized, if at all, by one real amplitude on one sector-sensitive bridge

## What this does not close

This note does **not** prove:

- that the current retained bank realizes the primitive
- that `a_sel` is nonzero
- that the branch Hermitian-data law is derived from the axiom bank
- that the generic breaking-triplet law is derived from the axiom bank

So this is a minimal-extension theorem, not a full closure theorem.

## Command

```bash
python3 scripts/frontier_pmns_new_selector_primitive_construction.py
```
