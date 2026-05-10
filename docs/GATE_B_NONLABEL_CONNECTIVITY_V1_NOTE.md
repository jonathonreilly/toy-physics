# Gate B Non-Label Connectivity V1 Note

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** bounded numerical comparison at `h = 0.5`, `W = 10`, `NL = 25`,
seeds `0..3`, `z = {3, 4, 5}`, `drift = 0.2` between exact grid, no-restore
KNN+floor connectivity, and no-restore geometry-sector forward connectivity.
Frozen on disk.
**Status authority:** independent audit lane only.
**Script:** [`scripts/gate_b_nonlabel_connectivity_v1.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_nonlabel_connectivity_v1.py) (PASS=1, C-class)

## Audit boundary (2026-05-10)

The independent audit verdict on this row is `audited_conditional`. The
runner is non-print-only — it constructs the tested geometries and
connectivities, propagates amplitudes, and computes the TOWARD fractions and
`F~M` readouts directly — and the bounded numerical comparison itself is
supported by that runner output.

The conditional grade comes from non-retained one-hop dependencies:

- [`docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md)
  (`audit_status: audited_conditional`) — bounded weak-connectivity replay,
  the no-restore KNN+floor negative this row's geometry-sector candidate
  is contrasted against. Conditional.
- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
  (`audit_status: audited_conditional`) — far-field Gate B reference whose
  primitive-to-physical-gravity bridge is itself flagged. Conditional.

This note's load-bearing claim is therefore narrowed to the bounded numerical
comparison on the declared scope. The broader "geometry-sector stencil
restores Gate B closure" reading is recorded only as a cross-reference,
conditional on the upstream rows.

## Artifact chain

- [`scripts/gate_b_nonlabel_connectivity_v1.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_nonlabel_connectivity_v1.py)
- [`logs/2026-04-05-gate-b-nonlabel-connectivity-v1.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-nonlabel-connectivity-v1.txt)

## Question

Can we replace the next-layer label stencil with a geometry-only forward rule
that uses actual node positions, not grid labels, and still preserve the
retained far-field grown-geometry package better than naive KNN+floor?

This note is intentionally narrow:

- exact grid control
- no-restore grown geometry with naive KNN+floor connectivity
- no-restore grown geometry with a geometry-sector stencil connectivity

Only the far-field `TOWARD` fraction and `F~M` scaling are measured here.

## Frozen result

The frozen log is:

- `h = 0.5`
- `W = 10`
- `NL = 25`
- `seeds = 4`
- `z = [3, 4, 5]`
- no-restore grown family with `drift = 0.2`

Frozen readout:

- exact grid: `3/3` TOWARD, `F~M = 1.00`
- no-restore KNN+floor: `0/12` TOWARD, `F~M = n/a`
- geometry-sector stencil: `12/12` TOWARD, `F~M = 1.00`

## Safe read

The bounded statement is:

- the geometry-sector stencil beats the naive KNN+floor control on the tested
  no-restore grown family
- unlike KNN+floor, the candidate keeps the far-field package alive on this
  retained row
- this is a bounded candidate, not a universal non-label connectivity theorem

## Relation to Gate B (cross-references)

Read this together with:

- [`docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md)
  (`audit_status: audited_conditional`) — bounded weak-connectivity replay; one-hop dep.
- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
  (`audit_status: audited_conditional`) — far-field Gate B reference; one-hop dep.

The bounded numerical picture this note frozen-replays:

- on the tested no-restore family, the label-based connectivity stencil
  matches the exact grid harness signature
- on the same family, naive KNN+floor does not match the harness signature
- the geometry-sector stencil candidate matches the harness signature on the
  declared rows

That is a bounded numerical comparison on the declared scope. The full
"Gate B closure" reading remains conditional on the upstream
`gate_b_farfield_note` row's primitive-to-physical-gravity bridge.
