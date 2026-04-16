# PMNS EWSB Weak-Axis Seed Edge-Selector Reduction

**Date:** 2026-04-15  
**Status:** exact reduction theorem on the remaining `Y`-level selector on the
compatible weak-axis seed patch  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_ewsb_weak_axis_seed_edge_selector_reduction.py`

## Question

The compatible weak-axis seed patch already closes the canonical active
coefficients up to one exact exchange sheet

- `Y_+ = x_+ I + y_+ C`
- `Y_- = y_+ I + x_+ C`.

What exactly is that remaining `Y`-level selector?

## Bottom line

It is exactly an edge selector between the two one-Higgs monomial limits of
the canonical pair, and therefore exactly a Higgs-offset edge selector on that
pair.

On the compatible seed patch, as `A -> B` one has `nu -> 0`, hence `y_+ -> 0`
and

- `Y_+ -> sqrt(A) I`
- `Y_- -> sqrt(A) C`.

So the two residual sheets are not mysterious. They are the two exact monomial
edges of the canonical `(0,1)` two-Higgs support pair:

- the offset-`0` monomial edge
- the offset-`1` monomial edge

Therefore the remaining seed-patch full-closure object is an edge selector:
which one-Higgs monomial boundary the compatible seed deforms to.

On the canonical active pair `(0,1)`, those two one-Higgs monomial edges are
exactly the single-Higgs offset-`0` and offset-`1` supports. So the remaining
seed-patch selector is not independent of the Higgs-`Z_3` problem. It is the
same unresolved Higgs-offset choice, restricted to the `(0,1)` pair.

## Atlas and axiom inputs

This theorem reuses:

- `Neutrino Higgs Z3 underdetermination`
- `PMNS EWSB weak-axis Z3 seed`
- `PMNS EWSB weak-axis seed coefficient closure`

The current-bank consequence is immediate:

- the seed-patch sheet selector is not a generic new continuous datum
- it is a discrete Higgs-offset / monomial-edge selector
- and the current bank still does not fix it

## Exact monomial-edge limits

For the canonical pair `(0,1)`, the active chart is

`Y = x I + y C`.

On the compatible seed patch:

- `x = x_+(A,B)`
- `y = y_+(A,B)`
- `x y = nu = (A-B)/3`.

So at the equal-split edge `A = B`:

- `nu = 0`
- `x_+ = sqrt(A)`
- `y_+ = 0`.

Therefore

- `Y_+ = sqrt(A) I`
- `Y_- = sqrt(A) C`.

These are precisely the two one-Higgs monomial endpoints already present in
the canonical support pair.

## Theorem-level statement

**Theorem (The remaining weak-axis seed sheet is exactly a monomial-edge
selector).** Assume the exact weak-axis seed coefficient-closure theorem on the
canonical active pair `(0,1)`. Then:

1. the two residual compatible-patch sheets are
   `Y_+ = x_+ I + y_+ C` and `Y_- = y_+ I + x_+ C`
2. as `A -> B`, these limit exactly to the two one-Higgs monomial edges
   `sqrt(A) I` and `sqrt(A) C`
3. therefore the remaining `Y`-level seed-patch selector is exactly a
   discrete monomial-edge selector between the two Higgs offsets in the
   canonical pair
4. this is exactly the restricted single-Higgs Higgs-`Z_3` selector
   `q_H in {0,+1}` on that pair

So the weak-axis seed patch reduces the remaining full-closure problem even
further: it is not “which coefficients?” but “which monomial edge is the
deformation anchored to?”, equivalently “which Higgs offset is the deformation
anchored to on the `(0,1)` pair?”

## What this closes

This closes the interpretation of the last seed-patch ambiguity.

It is now exact that the remaining selector on that patch is:

- discrete
- support-theoretic
- tied directly to the two one-Higgs endpoints of the active pair
- and identical to the unresolved restricted Higgs-offset selector on that pair

## What this does not close

This note does **not** derive:

- which monomial edge the current bank selects
- the Higgs-offset selector from the current stack
- the global branch Hermitian-data law beyond the seed patch

So the weak-axis seed patch is not globally fully closed yet. But the
remaining object is now identified exactly.

## Command

```bash
python3 scripts/frontier_pmns_ewsb_weak_axis_seed_edge_selector_reduction.py
```
