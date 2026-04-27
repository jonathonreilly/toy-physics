# Gate B Grown-Geometry Distance-Law Note

**Date:** 2026-04-05  
**Status:** bounded distance-law transfer replay on the proposed_retained grown-geometry family

## Artifact chain

- [`scripts/gate_b_grown_distance_law.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_distance_law.py)
- [`logs/2026-04-05-gate-b-grown-distance-law.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-distance-law.txt)

## Question

Once far-field sign and `F~M` are frozen on grown geometry, does the
distance-law fit also transfer on the same retained `h = 0.5` generated family?

This note is intentionally narrow:

- exact grid versus grown geometry
- same retained growth rule
- same far-field family
- distance tail only

## Frozen result

The frozen log compares:

- exact grid
- grown geometry with `drift = 0.2`, `restore = 0.7`

Across `4` seeds and `z = 3..7`, the fitted tails are:

- exact grid: `20/20` TOWARD, `b^(-0.90)`, `R^2 = 0.855`
- grown geometry: `20/20` TOWARD, `b^(-0.83)`, `R^2 = 0.884`

Both rows peak at `z = 4` and then decline across the retained far-field
window.

## Safe read

The honest bounded statement is:

- the distance-law tail transfers from the exact grid to the retained moderate-
  drift grown geometry on this tested family
- both rows stay cleanly `TOWARD` across the tested `z = 3..7` window
- both rows show a positive declining far-field tail with similar fit quality
- this bounded replay is weaker than the earlier inline `-1.01` branch claim,
  so the safe read is **tail transfer and comparable decline**, not “exact
  Newtonian equality”

This is still a companion result:

- it does **not** by itself close all of Gate B
- it should be read together with the frozen far-field sign / `F~M` harness

## Relation to Gate B

Read this with:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
- [`docs/GATE_B_DYNAMICS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_DYNAMICS_NOTE.md)

Together they now support the stronger bounded read:

- far-field sign transfers
- far-field `F~M = 1.00` transfers
- the far-field distance-law fit stays positive and comparable on the retained
  moderate-drift row

The remaining open boundary is no longer the retained moderate-drift far-field
row. It is the rest of the generated-geometry parameter space.
