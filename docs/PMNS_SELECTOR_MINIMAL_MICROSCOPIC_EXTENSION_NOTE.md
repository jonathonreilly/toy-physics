# PMNS Selector Minimal Microscopic Extension

**Date:** 2026-04-15
**Status:** exact extension-class theorem for any positive PMNS selector
realization
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_selector_minimal_microscopic_extension.py`

## Question

Given the current exact bank, what is the smallest honest microscopic extension
class that could realize the PMNS selector positively?

## Bottom line

The minimal surviving positive class is now fully specified.

Any future positive PMNS selector realization must be:

- genuinely new relative to the current retained support-plus-scalar bank
- sector-sensitive and inter-sector
- supported only on the non-universal locus
- non-additive over the lepton direct sum
- and reduced on the branch-class quotient to one real amplitude

`B_red = a_sel (chi_N_nu - chi_N_e)`.

So the smallest honest positive object is a **non-additive sector-sensitive
mixed bridge with one real amplitude slot**.

## Atlas and package inputs

This theorem reuses:

- `PMNS scalar bridge nonrealization`
- `PMNS selector non-universal support reduction`
- `PMNS selector class-space uniqueness`
- `PMNS selector unique amplitude slot`
- `PMNS selector current-stack zero law`

And, as structural naming only:

- `Action geometry bridge`

That last import is not a theorem import. It is only the safe naming precedent
that “mixed bridge” is the right label when a direct-sum baseline is ruled out
but the positive bridge object is not yet explicitly derived.

## Why this is stronger than the current-zero-law note

The current-zero-law note says the retained bank sets `a_sel,current = 0`.

This note goes one step further. It identifies the smallest positive extension
class that survives all current exact obstructions.

So the remaining microscopic science is no longer vague. It is not “some new
bridge” in the abstract. It is one very specific kind of new bridge.

## Theorem-level statement

**Theorem (Minimal surviving microscopic extension class for a positive PMNS
selector realization).** Assume the exact PMNS scalar-bridge nonrealization
theorem, the exact PMNS selector non-universal support reduction theorem, the
exact PMNS selector class-space uniqueness theorem, the exact PMNS selector
unique-amplitude-slot theorem, and the exact PMNS selector current-stack zero
law. Then any future positive PMNS selector realization must:

1. lie outside the current support-plus-scalar retained bank
2. be sector-sensitive and inter-sector
3. be nonzero only on the non-universal locus
4. be non-additive over the lepton direct sum
5. reduce on the branch-class quotient to
   `B_red = a_sel (chi_N_nu - chi_N_e)` for one real amplitude `a_sel`

Therefore the minimal surviving positive extension class is a non-additive
sector-sensitive mixed bridge with one real amplitude slot.

## What this closes

This closes the last extension-class ambiguity around the PMNS selector.

It is now exact that the remaining microscopic bridge problem is not:

- another support-bank refinement
- another additive scalar observable
- another reduced selector family
- another multi-slot reduced amplitude law

The remaining positive problem is one specific extension class.

## What this does not close

This note does **not** derive:

- the microscopic bridge functional itself
- the sign or magnitude of `a_sel`
- the branch-conditioned coefficients on the selected branch

It is an extension-class theorem only.

## Command

```bash
python3 scripts/frontier_pmns_selector_minimal_microscopic_extension.py
```
