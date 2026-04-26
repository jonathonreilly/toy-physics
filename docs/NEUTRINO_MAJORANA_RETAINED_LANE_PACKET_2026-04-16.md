# Neutrino Majorana Retained Lane Packet (2026-04-16)

## Scope

This packet covers the retained Majorana side of the neutrino lane on the
current `main` package.

## Exact Surviving Chain

- one-generation operator/slot/block reduction:
  [NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md](./NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md),
  [NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md](./NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md),
  [NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md](./NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md),
  [NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md](./NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md)
- current-stack zero law:
  [NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md](./NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md)
- three-generation current-stack zero matrix:
  [NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md](./NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md)
- lower-level charge-preserving response obstruction:
  [NEUTRINO_MAJORANA_LOWER_LEVEL_PAIRING_NOGO_NOTE.md](./NEUTRINO_MAJORANA_LOWER_LEVEL_PAIRING_NOGO_NOTE.md)
- sharpened `nu_R` character / charge-`2` support reductions:
  [NEUTRINO_MAJORANA_NUR_CHARACTER_BOUNDARY_NOTE.md](./NEUTRINO_MAJORANA_NUR_CHARACTER_BOUNDARY_NOTE.md),
  [NEUTRINO_MAJORANA_NUR_CHARGE2_PRIMITIVE_REDUCTION_NOTE.md](./NEUTRINO_MAJORANA_NUR_CHARGE2_PRIMITIVE_REDUCTION_NOTE.md)
- conditional Schur-boundary theorem for a future supplied Majorana/seesaw
  block:
  [NEUTRINO_MAJORANA_SEESAW_SCHUR_BOUNDARY_THEOREM_NOTE_2026-04-25.md](./NEUTRINO_MAJORANA_SEESAW_SCHUR_BOUNDARY_THEOREM_NOTE_2026-04-25.md)

## Current Exact Endpoint

On the retained current bank:

- the canonical one-generation Majorana block is `mu J_2`
- the current-stack activation law is `mu_current = 0`
- the three-generation retained current-stack matrix is exactly zero
- the lower-level charge-preserving response layer does not reopen the
  anomalous Nambu block
- if a future nonzero `D` and invertible `M_R` are supplied, the light
  Majorana boundary operator is exactly the Schur response

So the present retained Majorana endpoint is:

- structurally allowed slot
- zero current-stack activation
- zero lower-level charge-preserving reopening

## What Is Closed

- the current retained Majorana lane is closed negatively
- the remaining honest Majorana frontier is one real amplitude `mu`
- any future nonzero Majorana reopening would require a genuinely new
  off-diagonal charge-`2` primitive outside the current retained stack

## What Is Not Claimed

- no theorem of impossibility for every future extension
- no statement that Majorana reopening is impossible in principle
- no flagship neutrino promotion
- no derivation of `D`, `M_R`, `mu`, or the neutrino mass spectrum from the
  Schur-boundary theorem alone

## Representative Runners

- [frontier_neutrino_majorana_current_stack_zero_law.py](../scripts/frontier_neutrino_majorana_current_stack_zero_law.py)
- [frontier_neutrino_majorana_lower_level_pairing_nogo.py](../scripts/frontier_neutrino_majorana_lower_level_pairing_nogo.py)
- [frontier_neutrino_majorana_nur_character_boundary.py](../scripts/frontier_neutrino_majorana_nur_character_boundary.py)
- [frontier_neutrino_majorana_nur_charge2_primitive_reduction.py](../scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py)
- [frontier_neutrino_majorana_seesaw_schur_boundary.py](../scripts/frontier_neutrino_majorana_seesaw_schur_boundary.py)
