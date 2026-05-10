# Gate B Non-Label Connectivity V1 Distance-Law Note

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** bounded numerical distance-law companion comparing exact grid
with the no-restore geometry-sector stencil at `h = 0.5`, four seeds,
`z = {3, 4, 5}`. Frozen on disk.
**Status authority:** independent audit lane only.
**Script:** [`scripts/gate_b_nonlabel_connectivity_v1_distance.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_nonlabel_connectivity_v1_distance.py) (PASS=1, C-class)

## Audit boundary (2026-05-10)

The independent audit verdict on this row is `audited_conditional`. The
runner is non-print-only — it constructs the geometries, propagates
amplitudes, and fits the post-peak distance-law tail directly — and the
bounded numerical comparison itself is supported by that runner output.

The conditional grade comes from non-retained one-hop dependencies:

- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
  (`audit_status: audited_conditional`) — base geometry-sector candidate
  this row companions. Conditional.
- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
  (`audit_status: audited_conditional`) — far-field Gate B reference;
  conditional.

This note's load-bearing claim is therefore narrowed to the bounded
numerical distance-law tail comparison on the declared scope. The broader
"non-label distance-law transfers" reading is recorded only as a
cross-reference, conditional on the upstream rows.

## Artifact chain

- [`scripts/gate_b_nonlabel_connectivity_v1_distance.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_nonlabel_connectivity_v1_distance.py)
- [`logs/2026-04-05-gate-b-nonlabel-connectivity-v1-distance.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-nonlabel-connectivity-v1-distance.txt)

## Question

On the retained `h = 0.5` no-restore grown family, does the geometry-sector
stencil keep a positive declining far-field distance-law fit?

This note is intentionally narrow:

- exact grid control
- no-restore grown geometry with geometry-sector stencil connectivity
- distance-law tail only

## Frozen result

The frozen log compares:

- exact grid
- no-restore grown geometry with geometry-sector stencil connectivity

Frozen readout:

- exact grid: `12/12` TOWARD, tail `b^(-0.56)`, `R^2 = 0.720`, peak `z = 3`
- geometry-sector stencil: `12/12` TOWARD, tail `b^(-0.53)`, `R^2 = 0.992`, peak `z = 3`

## Safe read

This companion is intentionally bounded.

The safe statement after the frozen replay is:

- the geometry-sector stencil keeps the far-field distance-law fit positive on
  the retained no-restore family
- the fit remains declining on the tested far-field window
- the geometry-sector row is the cleaner fit on this replay, with a much
  higher `R^2` than the exact-grid control
- this is a companion read, not a universal non-label connectivity theorem

## Relation to Gate B (cross-references)

Read this together with:

- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
  (`audit_status: audited_conditional`) — base geometry-sector candidate; one-hop dep.
- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
  (`audit_status: audited_conditional`) — far-field Gate B reference; one-hop dep.

The bounded numerical observation: on the tested no-restore family, the
geometry-sector stencil keeps a positive declining post-peak distance-law
tail (`b^(-0.53)`, `R^2 = 0.992`) on the `z = 3..5` window relative to the
exact-grid control (`b^(-0.56)`, `R^2 = 0.720`). That is a bounded numerical
companion read on the declared scope, not a "non-label distance-law
transfers" closure. Promotion past `audited_conditional` waits on the
upstream `gate_b_nonlabel_connectivity_v1_note` and `gate_b_farfield_note`
rows.
