# PMNS Sector-Exchange Nonforcing

**Date:** 2026-04-15
**Status:** support - structural or confirmatory support note
one-sided PMNS orientation bit by the present support-side bank
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_sector_exchange_nonforcing.py`

## Question

After reducing the non-universal one-sided PMNS surface to the unordered core

`{single-offset monomial lane, two-offset canonical lane}`,

can the current support-side bank force whether the active two-Higgs lane sits
on `Y_nu` or on `Y_e`?

## Bottom line

No.

On the reduced one-sided surface there is an exact sector-exchange involution

`sigma : (Y_nu, Y_e) -> (Y_e, Y_nu)`.

And the retained support-side descriptors on that surface are `sigma`-even:
they record only the unordered role pattern

`{monomial lane, active two-Higgs lane}`.

So the residual orientation bit

`tau in Z_2`

is not forceable by the current support-side bank.

## Atlas and axiom inputs

This theorem reuses:

- `PMNS minimal-branch nonselection`
- `Lepton shared-Higgs universality underdetermination`
- `PMNS sector-orientation orbit reduction`

## Why this is stronger than the orbit-reduction note

The orbit-reduction theorem showed that the remaining non-universal freedom is
only one sector-orientation bit.

This note goes one step further. It proves that the current support-side bank
cannot force even that last bit, because the reduced surface has an exact
sector-exchange involution and the retained descriptors are invariant under it.

## The theorem-level statement

**Theorem (Current-bank nonforcing of the one-sided PMNS
sector-orientation bit).**
Assume the exact PMNS minimal-branch nonselection theorem, the exact
shared-Higgs universality underdetermination theorem, and the exact
sector-orientation orbit-reduction theorem. Then:

1. the reduced non-universal one-sided PMNS surface admits an exact
   sector-exchange involution `sigma`
2. the retained support-side descriptors on that surface depend only on the
   unordered core `{single-offset monomial lane, two-offset canonical lane}`
3. the current atlas contains no retained sector-sensitive inter-sector bridge
   theorem

Therefore the current support-side bank cannot force the residual
sector-orientation bit `tau in Z_2`.

## What this closes

This closes the last support-side selector loophole.

It is now exact that the remaining non-universal selector science is not:

- another local support theorem
- another branch-classification theorem
- another atlas-bank selector audit

It must instead be:

- a genuinely sector-sensitive inter-sector bridge
- a universality theorem that kills the one-sided class
- or a stronger impossibility theorem

## What this does not close

This note does **not** prove:

- that shared-Higgs universality is true
- that universality failure is impossible
- that `Y_nu` is preferred
- that `Y_e` is preferred
- the actual coefficient derivation on any surviving class

It is a current-bank theorem only.

## Command

```bash
python3 scripts/frontier_pmns_sector_exchange_nonforcing.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- `publication/ci3_z3/DERIVATION_ATLAS.md` (publication aggregator;
  backticked to avoid length-2 cycle — citation graph direction is
  *atlas → this_note*)
- [pmns_minimal_branch_nonselection_note](PMNS_MINIMAL_BRANCH_NONSELECTION_NOTE.md)
- [lepton_shared_higgs_universality_underdetermination_note](LEPTON_SHARED_HIGGS_UNIVERSALITY_UNDERDETERMINATION_NOTE.md)
- [pmns_sector_orientation_orbit_note](PMNS_SECTOR_ORIENTATION_ORBIT_NOTE.md)
