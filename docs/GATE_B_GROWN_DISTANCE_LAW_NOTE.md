# Gate B Grown-Geometry Distance-Law Note

**Date:** 2026-04-05  
**Status:** bounded distance-law transfer replay on the retained grown-geometry family

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

Across `8` seeds and `z = 2..9`, the fitted tails are:

- exact grid: `b^(-1.05)`, `R^2 = 0.919`
- grown geometry: `b^(-1.01)`, `R^2 = 0.914`

## Safe read

The honest bounded statement is:

- the distance-law tail transfers from the exact grid to the retained moderate-
  drift grown geometry on this tested family
- both rows are near-Newtonian on the far-field fit
- the grown row is at least as good as the exact-grid row on this bounded fit

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
- the far-field distance-law fit transfers

The remaining open boundary is no longer the retained moderate-drift far-field
row. It is the rest of the generated-geometry parameter space.
