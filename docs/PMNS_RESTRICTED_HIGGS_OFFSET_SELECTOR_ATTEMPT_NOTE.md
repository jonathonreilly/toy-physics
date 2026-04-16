# PMNS Restricted Higgs-Offset Selector Attempt

**Date:** 2026-04-15  
**Status:** exact boundary theorem on the canonical PMNS seed-pair selector  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_restricted_higgs_offset_selector_attempt.py`

## Question

On the canonical PMNS seed pair `(0,1)`, can the current exact bank derive a
positive law for the remaining restricted Higgs-offset selector?

If not, what is the strongest exact theorem that identifies the minimally
missing selector input?

## Bottom line

No positive selector law is derivable from the current exact bank.

The strongest exact statement is that the remaining seed-patch selector is a
single discrete Higgs-offset / monomial-edge bit on the canonical pair:

- `Y = sqrt(A) I` on the offset-`0` monomial edge
- `Y = sqrt(A) C` on the offset-`1` monomial edge

Equivalently, on the canonical pair `(0,1)` the remaining selector is exactly
the restricted single-Higgs Higgs-`Z_3` choice

`q_H in {0,+1}`.

The current exact bank reduces the problem to this bit, but does not fix it.
So the minimally missing selector input is not a continuous coefficient, not a
right-Gram scalar, and not an aligned-core parameter. It is one binary
monomial-edge selector on the canonical seed pair.

## Atlas and axiom inputs

This theorem reuses:

- `Neutrino Higgs Z3 underdetermination`
- `Neutrino Dirac Z3 support trichotomy`
- `PMNS EWSB weak-axis Z3 seed`
- `PMNS EWSB weak-axis seed coefficient closure`
- `PMNS EWSB weak-axis seed edge-selector reduction`
- `PMNS selector current-stack zero law`

These inputs already give the exact reduction chain:

1. the single-Higgs generation charge is not fixed globally
2. the compatible weak-axis seed patch collapses to two exchange sheets
3. the equal-split boundary of that patch is the pair of monomial edges
4. the current bank does not select between those two edges

## Why the selector is discrete

The current retained single-Higgs Dirac lane already reduces the generation
charge to the exact discrete set

`q_H in {0,+1,-1}`.

On the canonical compatible seed patch, the active coefficients close to the
two exchange sheets

`Y_+ = x_+ I + y_+ C`, `Y_- = y_+ I + x_+ C`.

At the monomial boundary `A = B`, one has `y_+ -> 0`, so these sheets limit
exactly to the two one-Higgs monomial edges:

- `Y_+ -> sqrt(A) I`
- `Y_- -> sqrt(A) C`

Therefore the remaining selector on the canonical pair is exactly the discrete
choice between those two edges.

## Theorem-level statement

**Theorem (Restricted Higgs-offset selector on the canonical PMNS seed pair).**
Assume the exact Higgs-`Z_3` underdetermination theorem, the exact Dirac
`Z_3` support trichotomy, the exact weak-axis seed coefficient-closure theorem,
and the exact weak-axis seed edge-selector reduction theorem. Then:

1. the canonical PMNS seed pair `(0,1)` reduces the remaining selector to a
   single discrete monomial-edge bit
2. on the monomial boundary `A = B`, that bit is exactly the choice between
   `sqrt(A) I` and `sqrt(A) C`
3. equivalently, the remaining selector is the restricted Higgs-offset choice
   `q_H in {0,+1}` on the canonical pair
4. the current exact bank does not determine that bit

So the current bank does **not** derive a positive selector law. It derives
the sharpest possible obstruction: the remaining selector is one binary
Higgs-offset bit and nothing smaller.

## What this closes

This closes the ambiguity about the shape of the remaining seed-patch
selector.

It is now exact that the remaining object is:

- discrete
- support-theoretic
- tied to the canonical one-Higgs edges
- equivalent to the restricted Higgs-offset selector on the `(0,1)` pair

## What this does not close

This note does **not** derive:

- which edge the current bank selects
- a positive law for the restricted Higgs-offset bit
- the microscopic bridge functional that would activate the bit
- the global branch Hermitian-data law

So this is a boundary theorem, not a full closure theorem.

## Command

```bash
python3 scripts/frontier_pmns_restricted_higgs_offset_selector_attempt.py
```
