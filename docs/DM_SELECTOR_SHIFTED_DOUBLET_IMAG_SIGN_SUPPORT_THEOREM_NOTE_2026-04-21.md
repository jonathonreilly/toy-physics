# DM Selector Shifted-Doublet-Imaginary-Sign Support Theorem

**Date:** 2026-04-21  
**Status:** selector-side support theorem on the open DM gate  
**Primary runner:** `scripts/frontier_dm_selector_shifted_doublet_imag_sign_support_2026_04_21.py`

## Statement

The selector-side bridge is now sharper than a generic recovered projection
problem.

The exact `Z_3` doublet-block theorem already gives the identity

```text
Im(K_Z3[1,2]) = sqrt(3) delta - 4 sqrt(2) / 3.
```

So the canonical sign boundary on the active target is

```text
delta = 4 sqrt(2) / (3 sqrt(3)),
```

equivalently

```text
Im(K_Z3[1,2]) = 0.
```

On the current selector packet:

- the exact observable-relative-action source lies on the **positive** side of
  this boundary,
- the preferred recovered lift `0` is the **unique** recovered lift on that
  same positive side,
- every competing recovered lift lies on the negative side,
- and the same preferred lift is already the unique recovered threshold
  selector chosen by `tau_b,min`.

So the remaining selector burden narrows again. On the current packet, the
live positive target is no longer a generic recovered-bank bridge. The
constructive triplet chamber

- `gamma > 0`,
- `E1 > 0`,
- `E2 > 0`,

is already shared across the whole recovered packet, and the same is true of
the oriented-phase sign `sin(delta) > 0`.

The first right-sensitive datum that actually breaks that recovered
degeneracy is:

- derive the positive activation law for the shifted imaginary doublet mixing
  `Im(K_Z3[1,2])`, or
- replace the whole packet by a finer microscopic law.

## Prior branch state

Three earlier results are used here:

1. `docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md`
   gives the exact doublet-block readout

   ```text
   delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3).
   ```

2. `docs/DM_SELECTOR_RELATIVE_ACTION_RECOVERED_BRANCH_SEPARATION_SUPPORT_THEOREM_NOTE_2026-04-21.md`
   shows the exact observable-relative-action selector does not itself land on
   the recovered selector branch.
3. `docs/DM_SELECTOR_RELATIVE_ACTION_RECOVERED_PROJECTION_SUPPORT_THEOREM_NOTE_2026-04-21.md`
   shows that the internal selector already has one canonical recovered image:
   the preferred recovered lift `0`, also selected by `tau_b,min`.

That still left the remaining bridge framed as a generic projection-principle
problem.

## New support theorem

### 1. The internal selector already chooses one side of a canonical doublet-block sign boundary

For the exact observable-relative-action source, the active target
`(delta_rel, q_+,rel)` satisfies

```text
delta_rel > 4 sqrt(2) / (3 sqrt(3)),
```

hence

```text
Im(K_Z3[1,2])_rel > 0.
```

So the internal selector does not merely point toward the preferred recovered
lift metrically. It already chooses one exact side of the canonical
doublet-block sign boundary.

### 2. On the recovered bank, only the preferred lift lies on that same side

Evaluating the exact recovered bank shows:

- lift `0`: `Im(K_Z3[1,2]) > 0`
- lifts `1,2,3,4`: `Im(K_Z3[1,2]) < 0`

So the preferred recovered lift is the unique recovered point on the same
positive side as the internal selector.

### 3. The constructive triplet chamber still does not distinguish the recovered packet

Across the recovered bank, the exact projected-source triplet is already
shared:

```text
gamma = 1/2,
E1    = sqrt(8/3),
E2    = sqrt(8)/3.
```

So every recovered lift already lies in the same constructive sign chamber

```text
gamma > 0,
E1 > 0,
E2 > 0.
```

And every recovered lift also satisfies

```text
sin(delta) > 0.
```

Therefore neither the sharp source tuple nor the constructive triplet chamber
breaks the recovered selector degeneracy.

### 4. This same lift is already the recovered threshold selector

The exact threshold selector candidate `tau_b,min` already chooses the same
preferred recovered lift uniquely.

Therefore the branch now has a stronger agreement packet than before:

- the exact internal selector,
- the sharp source tuple and constructive triplet chamber,
- the canonical recovered projection,
- the recovered threshold selector,
- and the recovered doublet-block sign side

all point to the same recovered lift `0`.

## Consequence

This does **not** close the microscopic selector law.

It does sharpen the remaining positive target again.

Before this theorem, the live selector statement was:

- justify the projection from the exact internal selector to the preferred
  recovered lift, or replace both selector objects by a finer microscopic law.

After this theorem, the sharper packet-level statement is:

- derive the positive activation law for the shifted imaginary doublet mixing
  `Im(K_Z3[1,2])`, which already selects the same preferred recovered lift on
  the current packet and is the first right-sensitive refinement beyond the
  shared constructive triplet chamber, or
- replace the packet by a finer microscopic law.

So the remaining microscopic bridge is now more concrete:

```text
activate the positive side of the canonical doublet-block odd direction.
```

## Boundary

This is a support theorem, not closure.

It does **not** prove that positivity of `Im(K_Z3[1,2])` is already a
retained-derived law on the full native branch, and it does **not** yet
replace the need for a genuine right-sensitive microscopic selector theorem.

It proves only that on the current selector packet the live burden has
collapsed from a generic branch-bridge problem to one explicit odd
doublet-block activation side.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_selector_shifted_doublet_imag_sign_support_2026_04_21.py
```

Expected:

```text
SUMMARY: PASS=17 FAIL=0
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16](DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)
- [dm_selector_relative_action_recovered_branch_separation_support_theorem_note_2026-04-21](DM_SELECTOR_RELATIVE_ACTION_RECOVERED_BRANCH_SEPARATION_SUPPORT_THEOREM_NOTE_2026-04-21.md)
- [dm_selector_relative_action_recovered_projection_support_theorem_note_2026-04-21](DM_SELECTOR_RELATIVE_ACTION_RECOVERED_PROJECTION_SUPPORT_THEOREM_NOTE_2026-04-21.md)
- [scalar_selector_remaining_open_imports_2026-04-20](SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md)
