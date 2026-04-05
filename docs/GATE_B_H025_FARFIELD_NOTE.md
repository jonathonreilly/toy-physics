# Gate B h=0.25 Far-Field Note

**Date:** 2026-04-05  
**Status:** bounded h=0.25 far-field replay on the retained generated-geometry family

## Artifact chain

- [`scripts/gate_b_h025_farfield.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_h025_farfield.py)
- [`logs/2026-04-05-gate-b-h025-farfield.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-h025-farfield.txt)

## Question

Does the retained grown-geometry far-field package survive at finer spacing
`h = 0.25`?

This note is intentionally narrow:

- exact grid control
- one retained moderate-drift grown row
- far-field `z >= 3` readout

## Safe read

This is a bounded scaling check, not a full Gate B closure.

The frozen result is:

- exact grid: `12/12` TOWARD, `F~M = 1.00`
- grown `drift = 0.2`: `12/12` TOWARD, `F~M = 1.00`

So the retained grown-geometry far-field package survives the `h = 0.25`
refinement on this bounded family.

The result to reject if it fails is:

- the grown package only worked at `h = 0.5`

## Relation to Gate B

Read this together with:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
- [`docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)
- [`docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md)

If the h=0.25 row stays clean, it strengthens the generated-geometry story by
showing the far-field package survives refinement in a smaller bounded family.
