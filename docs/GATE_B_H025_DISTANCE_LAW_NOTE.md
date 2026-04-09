# Gate B h=0.25 Grown-Geometry Distance-Law Note

**Date:** 2026-04-05  
**Status:** bounded h=0.25 distance-law transfer replay on the retained grown-geometry family

## Artifact chain

- [`scripts/gate_b_h025_distance_law.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_h025_distance_law.py)
- [`logs/2026-04-05-gate-b-h025-distance-law.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-h025-distance-law.txt)

## Question

Does a compact retained grown-geometry family still carry a positive declining
far-field tail when the spacing is refined to `h = 0.25`?

This note is intentionally narrow:

- exact grid versus grown geometry
- same moderate-drift row if possible
- distance tail only

## Frozen result

The frozen log compares a compact h=0.25 replay:

- exact grid
- grown geometry with `drift = 0.2`, `restore = 0.7`

The h=0.25 replay is bounded to a small seed set and a compact physical
window so the comparison stays reviewable. The window is intentionally
smaller than the earlier `h=0.5` companion because the `h=0.25` family is
more expensive to propagate, but still wide enough to admit a tail fit.

Frozen readout:

- exact grid: `10/10` TOWARD, tail `b^(-0.42)`, `R^2=0.855`, peak `z=2`
- grown `drift = 0.2`: `10/10` TOWARD, tail `b^(-0.54)`, `R^2=0.948`, peak `z=3`

## Safe read

The honest bounded statement is now:

- the h=0.25 grown row keeps a positive declining tail on the compact
  retained family
- the grown row is slightly steeper than the exact-grid row on this replay
- this is a refinement companion, not a full generated-geometry closure

## Relation to Gate B

Read this with:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
- [`docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md)

The purpose of this companion is simple:

- check whether the grown-geometry distance-law story survives at the finer
  `h = 0.25` scale
- keep the claim bounded to the same moderate-drift family if it does
