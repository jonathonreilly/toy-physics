# PMNS Selector Current-Stack Zero Law

**Date:** 2026-04-15
**Status:** support - structural or confirmatory support note
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_selector_current_stack_zero_law.py`

## Question

After the reduced PMNS selector bridge has been compressed to one real
amplitude slot

`a_sel`,

what is the actual activation law for that amplitude on the stack currently
retained today?

## Bottom line

On the current retained bank, the activation law is the zero law:

`a_sel,current = 0`.

This is an exact current-stack theorem, not a statement about every future
extension.

The reason is already present in the current exact chain:

1. the reduced selector class is unique and carries one real amplitude slot
2. the current support-side bank is sector-even and therefore projects to zero
   on that class
3. the current additive scalar observable bank is block-local and sector-even
   and also projects to zero
4. the current atlas contains no additional retained PMNS bridge object that
   shifts that zero

So on the stack actually retained today, the effective reduced selector
amplitude is exactly zero.

## Atlas and package inputs

This theorem reuses:

- `PMNS selector unique amplitude slot`
- `PMNS sector-exchange nonforcing`
- `PMNS scalar bridge nonrealization`
- `PMNS selector class-space uniqueness`

## Theorem-level statement

**Theorem (Current-stack zero law for the reduced PMNS selector amplitude).**
Assume the current retained atlas, the exact PMNS selector unique-amplitude-slot
theorem, the exact support-side nonforcing theorem, and the exact scalar-bridge
nonrealization theorem. Then the effective current-stack amplitude on the
unique reduced selector class

`S_cls = chi_N_nu - chi_N_e`

is exactly

`a_sel,current = 0`.

Equivalently: on the stack retained today, the reduced PMNS selector bridge is
not activated.

## What this closes

This closes the present-tense PMNS selector amplitude question on the current
bank.

It is now exact that the current bank has not merely “failed to derive the
bridge yet.” On the retained support-plus-scalar bank, the effective reduced
selector amplitude is zero.

## What this does not close

This note does **not** prove:

- that no future extension can realize `a_sel != 0`
- that universality failure is impossible
- that the full PMNS problem is solved negatively forever

It is a current-stack theorem only.

## Command

```bash
python3 scripts/frontier_pmns_selector_current_stack_zero_law.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [pmns_selector_unique_amplitude_slot_note](PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md)
- [pmns_sector_exchange_nonforcing_note](PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md)
- [pmns_scalar_bridge_nonrealization_note](PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md)
- [publication.ci3_z3.derivation_atlas](publication/ci3_z3/DERIVATION_ATLAS.md)
