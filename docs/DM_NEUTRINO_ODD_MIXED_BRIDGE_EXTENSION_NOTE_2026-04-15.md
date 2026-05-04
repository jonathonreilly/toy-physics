# DM Neutrino Odd Mixed-Bridge Extension

**Date:** 2026-04-15  
**Status:** exact extension-class theorem for any positive DM odd-slot activator  
**Script:** `scripts/frontier_dm_neutrino_odd_mixed_bridge_extension.py`

## Question

After the odd-slot theorem and the current-stack zero law, what is the smallest
honest positive extension class that could activate the DM odd slot?

## Bottom line

A **residual-`Z_2`-odd non-additive mixed bridge with one real amplitude slot**.

More sharply, any future positive local activator must:

- lie outside the current retained even support/Hermitian/scalar bank
- live on the canonical non-universal two-Higgs locus
- be residual-`Z_2` odd
- be non-additive over the even/odd circulant decomposition
- reduce to one real amplitude on the unique odd class `i(S - S^2)`

So the remaining extension problem is no longer vague. It is one specific
bridge class.

## Why this is now exact

The branch already knows:

1. the unique odd local class: `c_odd i(S-S^2)`
2. the current-stack law: `c_odd,current = 0`
3. the unique minimal support lane: the canonical distinct-charge two-Higgs
   branch
4. the local sheet on that lane is already fixed on the DM circulant route

So all the easy freedom is gone. A positive activator has one honest shape
left.

## Theorem-level statement

**Theorem (Minimal surviving positive extension class for DM odd-slot
activation).** Assume the exact DM odd-slot theorem, the exact DM odd-slot
current-stack zero law, the exact DM two-Higgs minimality theorem, and the
exact DM two-Higgs continuity sheet theorem. Then any future positive local DM
activator must:

1. lie outside the current retained even support/Hermitian/scalar bank
2. be supported on the canonical non-universal two-Higgs locus
3. be residual-`Z_2` odd
4. be non-additive over the even/odd circulant decomposition
5. reduce on the local quotient to one real amplitude multiplying the unique
   odd class `i(S-S^2)`

Therefore the minimal surviving positive DM extension class is a
residual-`Z_2`-odd non-additive mixed bridge with one real amplitude slot.

## What this closes

This closes the last extension-class ambiguity around the DM odd-slot blocker.

The remaining bridge problem is not:

- another even support refinement
- another Hermitian/scalar post-processing trick
- another multi-parameter local coefficient family

It is one specific positive bridge class.

## What this does not close

This note does **not** derive the microscopic bridge functional itself.

It identifies the extension class only.

## Command

```bash
python3 scripts/frontier_dm_neutrino_odd_mixed_bridge_extension.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [dm_neutrino_odd_circulant_z2_slot_theorem_note_2026-04-15](DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15.md)
- [dm_neutrino_odd_circulant_current_stack_zero_law_note_2026-04-15](DM_NEUTRINO_ODD_CIRCULANT_CURRENT_STACK_ZERO_LAW_NOTE_2026-04-15.md)
- [dm_neutrino_two_higgs_minimality_theorem_note_2026-04-15](DM_NEUTRINO_TWO_HIGGS_MINIMALITY_THEOREM_NOTE_2026-04-15.md)
- [dm_neutrino_two_higgs_continuity_sheet_theorem_note_2026-04-15](DM_NEUTRINO_TWO_HIGGS_CONTINUITY_SHEET_THEOREM_NOTE_2026-04-15.md)
