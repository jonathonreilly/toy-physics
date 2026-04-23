# PMNS Selector Sector-Odd Reduction

**Date:** 2026-04-15
**Status:** exact reduction theorem for the parity class of any future PMNS
selector on the reduced one-sided surface
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_sector_odd_bridge_reduction.py`

## Question

After the current support-side and scalar-observable banks both fail to realize
the one-sided PMNS selector, what exact form can the missing selector now be
reduced to?

## Bottom line

On the reduced one-sided PMNS surface, any branch-distinguishing scalar can be
replaced by its sector-odd part under the exact sector-exchange involution

`sigma : (Y_nu, Y_e) -> (Y_e, Y_nu)`.

So the missing selector can be reduced to a nonzero **sector-odd mixed bridge
functional**.

The current exact banks do not contain such an object:

- the retained support-side bank supplies only sector-even reduced data
- the retained additive scalar observable bank supplies only sector-even
  block-local data

## Atlas and axiom inputs

This theorem reuses:

- `PMNS sector-exchange nonforcing`
- `PMNS scalar bridge nonrealization`

## Why this is stronger than the current obstruction notes

The current obstruction notes say:

- the support-side bank cannot force the bit
- the current scalar observable bank cannot realize the bridge either

This theorem goes one step further. It identifies the minimal parity class that
any successful future selector must inhabit:

- it must be sector-odd under `sigma`
- and it must be genuinely mixed / inter-sector

## Theorem-level statement

**Theorem (Reduction of the missing PMNS selector to a sector-odd mixed
bridge).**
Assume the exact PMNS sector-exchange nonforcing theorem and the exact PMNS
scalar bridge nonrealization theorem. Then on the reduced non-universal
one-sided PMNS surface:

1. any branch-distinguishing scalar functional is equivalent, for selector
   purposes, to its nonzero sector-odd part under the exact involution
   `sigma`
2. the retained support-side bank contributes only sector-even reduced data
3. the retained additive scalar observable bank contributes only sector-even
   block-local data

Therefore the minimal missing selector object can be taken to be a nonzero
sector-odd mixed bridge functional.

## What this closes

This closes the last vague wording around “some new bridge.”

It is now exact that the remaining selector science is not just “a bridge” in
the abstract. It must be a bridge with a very specific parity signature.

## What this does not close

This note does **not** construct that bridge.

It does not prove:

- that a sector-odd mixed bridge exists
- that universality is true
- that universality failure is true
- any coefficient derivation on a surviving extension class

It is a reduction theorem only.

## Command

```bash
python3 scripts/frontier_pmns_sector_odd_bridge_reduction.py
```
