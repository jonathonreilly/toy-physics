# Gate B No-Restore Far-Field Note

**Date:** 2026-04-05  
**Status:** bounded no-restore far-field companion replay

## Artifact chain

- [`scripts/gate_b_no_restore_farfield.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_no_restore_farfield.py)
- [`logs/2026-04-05-gate-b-no-restore-farfield.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-no-restore-farfield.txt)

## Question

If we keep the same grown-geometry family but set `restore = 0`, how much of
the far-field gravity package survives?

This note is intentionally narrow:

- same layered generated-geometry family
- same far-field `z >= 3` readout
- restore removed
- drift varied across a small bounded row set

## Frozen result

The frozen log compares the no-restore rows at:

- `drift = 0.0`
- `drift = 0.1`
- `drift = 0.2`
- `drift = 0.3`
- `drift = 0.5`

The row format is:

- `TOWARD` fraction over the tested far-field mass positions
- `F~M` from the same retained three-strength probe

## Safe read

The honest bounded statement is:

- this harness tells us how much far-field gravity survives when the restoring
  force is removed from the grown-geometry rule
- the result should be read as a survival boundary, not as a full generated-
  geometry replacement for the retained `restore > 0` family

## Relation to Gate B

Read this with:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
- [`docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)
- [`docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md)

The use case is simple:

- if the no-restore rows keep a strong far-field TOWARD rate and `F~M`
  fidelity, that is evidence that connectivity structure carries much of the
  physics even without the restoring pull
- if they collapse, that tells us the restoring force is doing real work and is
  not just cosmetic

Either result is useful. The point is to freeze the boundary cleanly.
