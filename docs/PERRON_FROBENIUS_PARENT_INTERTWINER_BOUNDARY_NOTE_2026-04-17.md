# Perron-Frobenius Parent / Intertwiner Boundary

**Date:** 2026-04-17  
**Status:** exact science-only boundary theorem for the operator-first global PF program  
**Script:** `scripts/frontier_perron_frobenius_parent_intertwiner_boundary_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

At the `30k`-foot theory level, is step 1 of the global PF-selector program
already closed?

Here step 1 means:

- the sole axiom canonically defines the relevant positive parent dynamics, and
- the live sector transfer laws arise from that parent object by canonical
  intertwiner / projection operations.

## Answer

Partially, but not globally.

The current stack already closes the Wilson-side half of step 1:

- on the retained Wilson gauge surface there is one exact positive parent
  transfer object;
- the plaquette source-sector transfer law is already a canonical descendant of
  that parent object;
- the strong-CP `theta` law is already a canonical Fourier descendant of that
  same parent object.

But the current stack does **not** yet close step 1 globally across the live
retained sectors, because:

1. the strongest canonical sole-axiom `hw=1` PMNS pack remains trivial;
2. there is still no Wilson-to-PMNS intertwiner / projection theorem;
3. the plaquette framework-point operator-side data are still not explicitly
   evaluated at `beta = 6`, so even the Wilson-descendant lane is not yet fully
   closed at framework point.

So yes: **more work on step 1 is still required.**

The right next theory target is therefore not another sample-side PF note. It
is a **parent / intertwiner theorem**.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md):

- the retained Wilson surface already has one exact parent partition object;
- plaquette and `theta` are already exact canonical descendants of that parent;
- PMNS is explicitly **not** yet shown to be a canonical projection of that
  same parent object.

From
[PERRON_FROBENIUS_GLOBAL_SELECTOR_CURRENT_STACK_CLOSURE_NOTE_2026-04-17.md](./PERRON_FROBENIUS_GLOBAL_SELECTOR_CURRENT_STACK_CLOSURE_NOTE_2026-04-17.md):

- the remaining honest positive global route is operator-plus-projection;
- the PMNS-side blocker is absence of a nontrivial descendant / projection law;
- the plaquette-side blocker is absence of determined framework-point beta-side
  operator data.

From
[PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](./PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md):

- the strongest canonical sole-axiom `hw=1` PMNS source/transfer construction
  still stays trivial.

## Definition: parent / intertwiner theorem

For the global PF program, a true parent / intertwiner theorem would require:

1. one canonically axiom-derived positive parent operator family
   `T_parent`;
2. for each live retained sector `S`, one canonical map `I_S` or `P_S` such
   that the sector law is a descendant of `T_parent`;
3. compatibility strong enough that sector PF states are descendants of one
   common parent PF state.

In operator language the missing load-bearing form is an intertwiner /
projection relation of the schematic type

`P_S T_parent = T_S P_S`

or equivalently

`I_S^* T_parent I_S = T_S`

on the relevant retained sector.

## Theorem 1: current-stack status of step 1

On the current exact stack, step 1 is closed only on the Wilson gauge surface.

More precisely:

1. the Wilson one-clock transfer object is already an exact positive parent
   object on the retained gauge surface;
2. plaquette and `theta` are already exact canonical descendants of that parent
   object;
3. but the current stack still does **not** supply a PMNS intertwiner /
   projection theorem, and therefore does **not** yet promote the Wilson parent
   object into one common global sole-axiom parent dynamics across the live
   sectors.

Therefore the current exact bank supports a **partial step-1 theorem** but not
the full global step-1 closure needed for a positive global PF-selector proof.

## Corollary 1: the right next move is operator-first and projection-first

The next honest theorem target is:

1. strengthen the Wilson parent object into the explicit canonical parent
   dynamics statement actually needed by the global PF program;
2. prove exact descendant / intertwiner laws for the live sectors;
3. only then ask PF to select one common global state.

This is why the right next move is a parent / intertwiner theorem rather than a
further sample-side reconstruction theorem.

## Corollary 2: more work on step 1 is still required

The clean `30k`-foot answer is therefore:

- **step 1 on the Wilson gauge surface:** yes;
- **step 1 globally across plaquette, strong-CP, and PMNS:** no.

So the global PF program still needs more step-1 work.

## What this closes

- one exact answer to the theory-ordering question "do we still need more work
  on step 1?"
- one exact clarification that the current Wilson parent/compression theorem is
  the right starting point but not yet the full global parent theorem
- one exact statement that the next honest target is a parent / intertwiner
  theorem

## What this does not close

- a positive global PF-selector theorem
- explicit `beta = 6` plaquette operator-side closure
- a Wilson-to-PMNS intertwiner / projection theorem
- cross-sector PF-state compatibility

## Why this matters

This note fixes the theory order.

The branch should no longer talk as if "step 1 is done and PF just needs more
computation." That is too optimistic.

The stronger and more correct statement is:

- step 1 is already real on the Wilson surface,
- step 1 is still incomplete globally,
- and the next honest science target is to strengthen the parent object into a
  true parent / intertwiner theorem.

## Atlas inputs used

- [GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_GLOBAL_SELECTOR_CURRENT_STACK_CLOSURE_NOTE_2026-04-17.md](./PERRON_FROBENIUS_GLOBAL_SELECTOR_CURRENT_STACK_CLOSURE_NOTE_2026-04-17.md)
- [PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](./PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_parent_intertwiner_boundary_2026_04_17.py
```
