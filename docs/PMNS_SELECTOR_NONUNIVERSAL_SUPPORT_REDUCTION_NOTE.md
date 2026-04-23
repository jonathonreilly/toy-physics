# PMNS Selector Non-Universal Support Reduction

**Date:** 2026-04-15
**Status:** exact reduction theorem on the support locus of any future PMNS
sector selector
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_selector_nonuniversal_support_reduction.py`

## Question

After reducing the missing PMNS selector to a nonzero sector-odd mixed bridge
functional, can its support be sharpened any further on the current exact bank?

## Bottom line

Yes.

On the reduced lepton branch-class surface, the shared-Higgs universal classes

- `U_1 = (single-offset, single-offset)`
- `U_2 = (two-offset, two-offset)`

are fixed by the exact sector exchange

`sigma : (Y_nu, Y_e) -> (Y_e, Y_nu)`.

Any sector-odd selector `F_-` obeys

`F_-(sigma x) = -F_-(x)`.

So on the `sigma`-fixed universal locus,

`F_-(x) = 0`.

Therefore the minimal missing selector object is not merely sector-odd and
mixed. It is supported only on the **non-universal** locus. Equivalently: it
must detect universality failure and orient it.

## Atlas and package inputs

This theorem reuses:

- `Lepton shared-Higgs universality collapse`
- `Lepton shared-Higgs universality underdetermination`
- `PMNS selector sector-odd reduction`

And, as structural framing only:

- `Universal A1 invariant section`

The GR import is not a dynamics import. It is a safe structural reuse: once an
exact invariant/fixed locus is isolated, any missing selector must live in the
moving complement rather than on the fixed locus itself.

## Why this is stronger than the sector-odd reduction note

The sector-odd reduction note identified the parity class of any successful
future selector.

This note goes one step further. It identifies the support locus on which that
future selector can even be nonzero:

- not on the universal classes
- only on the non-universal locus

So the remaining bridge must do two jobs at once:

- detect universality failure
- and distinguish its orientation

## Theorem-level statement

**Theorem (Any future PMNS sector selector is supported on the non-universal
locus).** Assume the exact shared-Higgs universality collapse theorem, the
exact shared-Higgs universality underdetermination theorem, and the exact PMNS
selector sector-odd reduction theorem. Then on the reduced lepton branch-class
surface:

1. the universal one-offset and universal two-offset classes are fixed points
   of the exact sector-exchange involution `sigma`
2. any branch-distinguishing selector can be reduced to a sector-odd part
   `F_-` with `F_-(sigma x) = -F_-(x)`
3. therefore `F_-` vanishes identically on the `sigma`-fixed universal locus

Therefore any future PMNS selector is supported only on the non-universal
locus. Equivalently, the minimal missing object is a sector-odd mixed bridge
that detects universality failure.

## What this closes

This closes one more selector-side loophole.

It is now exact that the remaining PMNS selector science is not:

- a selector that turns on already on universal one-offset classes
- a selector that turns on already on universal two-offset classes
- a parity-only refinement with no universality content

The future bridge must be nonzero only where the two sectors no longer share
the same offset-set class.

## What this does not close

This note does **not** prove:

- that such a non-universal sector-odd bridge exists
- that universality is true
- that universality failure is true
- any coefficient derivation on a surviving non-universal branch

It is a reduction theorem only.

## Command

```bash
python3 scripts/frontier_pmns_selector_nonuniversal_support_reduction.py
```
