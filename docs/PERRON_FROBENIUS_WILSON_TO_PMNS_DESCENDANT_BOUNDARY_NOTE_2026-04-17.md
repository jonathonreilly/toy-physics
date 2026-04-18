# Perron-Frobenius Wilson-to-PMNS Descendant Boundary

**Date:** 2026-04-17  
**Status:** exact science-only boundary theorem for the step-2 PF bottleneck  
**Script:** `scripts/frontier_perron_frobenius_wilson_to_pmns_descendant_boundary_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

If step 2 is the actual bottleneck of the global PF program, what exactly is
the missing theorem?

## Answer

The missing theorem is **not** a generic PMNS support theorem and it is **not**
another internal PMNS transport theorem.

The missing theorem is specifically:

- a **Wilson-to-PMNS descendant / intertwiner theorem**.

The current stack already has:

1. one exact Wilson parent object with canonical plaquette and `theta`
   descendants;
2. exact support intertwiners on the PMNS carrier support;
3. exact PMNS-native graph-first and transport-first partial laws on the
   retained `hw=1` carrier;
4. exact closure of the retained PMNS lane if the nontrivial `hw=1`
   source/transfer pack is supplied.

But the current stack still does **not** prove that the PMNS transfer law is a
canonical descendant of the Wilson parent object.

So the missing step-2 theorem is now sharp.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md):

- the Wilson surface already has one exact parent object with canonical
  plaquette and `theta` descendants;
- PMNS is explicitly not yet shown to be a canonical descendant.

From
[SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md):

- there is an exact support intertwiner between the taste-cube operator algebra
  and the BZ-corner support.

From
[PMNS_GRAPH_FIRST_AXIS_ALIGNMENT_NOTE.md](./PMNS_GRAPH_FIRST_AXIS_ALIGNMENT_NOTE.md),
[PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md](./PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md),
and
[PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md](./PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md):

- there are exact native PMNS partial laws on the retained `hw=1` carrier.

From
[PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](./PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md):

- if the nontrivial `hw=1` source/transfer pack is supplied, the retained PMNS
  lane closes exactly.

From
[PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](./PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md):

- the strongest canonical sole-axiom `hw=1` pack still remains trivial.

## Theorem 1: exact current-stack bottleneck in step 2

On the current exact stack:

1. there are already exact Wilson-side descendants;
2. there are already exact PMNS-side support intertwiners and transport laws;
3. but there is still no theorem of the form

   `P_PMNS T_Wilson = T_PMNS P_PMNS`

   or equivalent descendant law identifying the PMNS transfer object as a
   canonical descendant of the Wilson parent object.

Therefore the missing step-2 theorem is not "find any PMNS structure." It is
specifically:

- find a Wilson-to-PMNS descendant / intertwiner theorem.

## Corollary 1: internal PMNS exactness is not enough

The branch already has real exact PMNS structure:

- support intertwiner,
- graph-first axis selector,
- active corner transport law,
- aligned transfer-operator dominant-mode law,
- retained PMNS closure if the nontrivial pack is supplied.

Those are scientifically useful, but none of them yet supply the missing
cross-sector descendant law.

So step 2 is bottlenecked by **cross-sector provenance**, not by lack of PMNS
internal structure.

## Corollary 2: the next honest theorem target is cross-sector, not intra-PMNS

The next theorem target is therefore:

- either prove a canonical Wilson-to-PMNS descendant / intertwiner law;
- or derive a nontrivial sole-axiom PMNS transfer construction strong enough to
  play that role.

Without one of those, the branch cannot honestly advance from step 2 to step
3.

## What this closes

- one exact identification of the step-2 bottleneck
- one exact distinction between internal PMNS support theorems and the missing
  cross-sector descendant theorem
- one exact target statement for the next science move

## What this does not close

- a Wilson-to-PMNS descendant theorem
- a positive global PF-selector theorem
- explicit plaquette operator-side closure
- common-state compatibility

## Why this matters

This note says where the real theorem pressure belongs.

The branch should no longer diffuse effort across every PMNS-side object as if
any additional PMNS exactness would help equally. The missing theorem is
cross-sector and specific.

## Atlas inputs used

- [GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md)
- [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
- [PMNS_GRAPH_FIRST_AXIS_ALIGNMENT_NOTE.md](./PMNS_GRAPH_FIRST_AXIS_ALIGNMENT_NOTE.md)
- [PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md](./PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md)
- [PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md](./PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md)
- [PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](./PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)
- [PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](./PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_wilson_to_pmns_descendant_boundary_2026_04_17.py
```
