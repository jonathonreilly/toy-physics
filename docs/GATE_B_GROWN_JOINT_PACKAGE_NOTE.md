# Gate B Grown-Geometry Joint Package Note

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** bounded Born / interference / decoherence numerical comparison
between exact grid and grown geometry on the declared `h = 0.5`,
`drift = 0.2`, `restore = 0.7` row, with `drift = 0.3`, `restore = 0.5` as
a stress row, on four seeds.
**Status authority:** independent audit lane only.
**Script:** [`scripts/gate_b_grown_joint_package.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_joint_package.py) (PASS=1, C-class)

## Audit boundary (2026-05-10)

The independent audit verdict on this row is `audited_conditional`. The
runner is non-print-only — it constructs the geometries, propagates
amplitudes, and computes Born / `d_TV` / MI / decoherence directly — and
the bounded numerical comparison itself is supported by that runner output.

The conditional grade comes from a non-retained one-hop dependency:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
  (`claim_type: bounded_theorem`, `audit_status: audited_conditional`) —
  cited for the far-field gravity sign / `F ~ M` package on the same
  generated-geometry family. Conditional, not retained.
- [`docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: retained_bounded`) —
  cited for the bounded distance-law fit on the same row. Retained-bounded,
  cross-confirmed.

The non-retained farfield dep keeps any "Gate B package" reading on this
row conditional. This note's load-bearing claim is therefore narrowed to
the bounded numerical Born / `d_TV` / MI / decoherence comparison on the
declared scope; the broader "package transfers as Gate B closure" reading
is recorded only as a conditional cross-reference until the farfield dep
is independently retained.

## Artifact chain

- [`scripts/gate_b_grown_joint_package.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_joint_package.py)
- [`logs/2026-04-05-gate-b-grown-joint-package.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-joint-package.txt)

## Question

Do the non-gravity observables also transfer from the exact grid to the grown
geometry on the retained generated-geometry family?

This note freezes:

- Born
- `d_TV`
- `MI`
- CL-bath decoherence

on:

- exact grid
- grown geometry at `drift = 0.2`, `restore = 0.7`
- noisier grown geometry at `drift = 0.3`, `restore = 0.5` as a stress row

## Frozen result

The frozen log reports mean values across `4` seeds.

The retained moderate-drift grown row stays extremely close to the exact grid:

- exact grid: Born `2.12e-15`, `d_TV = 0.787`, `MI = 0.568`,
  decoherence `49.4%`
- grown `drift = 0.2`, `restore = 0.7`: Born `2.19e-15`,
  `d_TV = 0.811`, `MI = 0.569`, decoherence `49.4%`

The noisier `drift = 0.3` stress row remains useful as a boundary read:

- Born `2.45e-15`
- `d_TV = 0.790`
- `MI = 0.446`
- decoherence `47.2%`

## Safe read

The honest bounded statement is:

- on the retained moderate-drift generated-geometry row, the non-gravity joint
  observables transfer well from the exact grid
- the moderate-drift row matches the exact grid almost exactly on Born, `MI`,
  and decoherence, and stays close on `d_TV`
- the noisier grown row shows that the transfer is not trivial under arbitrary
  growth noise: Born remains clean, while `MI` weakens first

This is exactly the kind of boundary skeptical readers need:

- one retained moderate-drift positive row
- one noisier stress row that degrades without collapsing everything at once

## Relation to Gate B (cross-references)

Read this with:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
  (`audit_status: audited_conditional`) — far-field gravity sign / `F ~ M`
  bounded harness positive on the same generated-geometry family;
  one-hop dep of this note.
- [`docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)
  (`effective_status: retained_bounded`) — bounded distance-law tail fit on
  the same row, cross-confirmed; one-hop dep of this note.

Together they support a *bounded numerical* package read on the moderate-drift
row:

- the far-field harness reports gravity sign / `F ~ M` (conditional on the
  upstream `gate_b_farfield_note` row)
- the distance-law fit on the bounded `z = 3..7` window is retained-bounded
- Born / `d_TV` / MI / decoherence stay close between exact grid and grown
  geometry on the four-seed comparison run by this runner

That is a bounded numerical observation on the declared scope, **not** a
"Gate B package transfer" closure. The remaining open step has two parts:
how broadly that comparison survives across the full generated-geometry
family, *and* the upstream primitive-to-physical-gravity bridge that the
farfield dep is itself flagged on. Both are recorded as deferred to the
upstream rows.
