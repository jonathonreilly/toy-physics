# Gate B Non-Label Connectivity V1 h=0.25 Note

**Date:** 2026-04-05  
**Status:** bounded h=0.25 refinement check for the geometry-sector stencil on
the no-restore grown family

## Artifact chain

- [`scripts/gate_b_nonlabel_connectivity_v1_h025.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_nonlabel_connectivity_v1_h025.py)
- [`logs/2026-04-05-gate-b-nonlabel-connectivity-v1-h025.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-nonlabel-connectivity-v1-h025.txt)

## Question

Does the geometry-only sector stencil that survived on the retained no-restore
grown family still preserve the far-field sign / `F~M` package after one
bounded refinement step to `h = 0.25`?

This note is intentionally narrow:

- exact grid control
- no-restore grown family with geometry-sector stencil connectivity

Only the far-field `TOWARD` fraction and `F~M` scaling are frozen here.

## Frozen result

The frozen log compares a compact `h = 0.25` replay:

- exact grid
- no-restore grown geometry with geometry-sector stencil connectivity

Frozen readout:

- exact grid: `5/5` TOWARD, `F~M = 1.00`
- geometry-sector stencil: `10/10` TOWARD, `F~M = 1.00`

## Safe read

The bounded statement should be read only from the frozen log.

This note is intentionally narrow:

- the geometry-sector stencil stays at `TOWARD` with `F~M = 1.00`
- that makes it a one-step refinement-stable positive for the far-field
  package on this compact retained family
- this is still not a full Gate B closure or a universal theorem

## Relation to Gate B

Read this together with:

- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)

The purpose of this refinement companion is simple:

- check whether the geometry-sector stencil survives one finer spacing
- keep the claim bounded to the same retained moderate-drift family if it does
