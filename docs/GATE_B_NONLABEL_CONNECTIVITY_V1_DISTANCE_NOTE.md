# Gate B Non-Label Connectivity V1 Distance-Law Note

**Date:** 2026-04-05  
**Status:** bounded distance-law companion for the geometry-sector stencil
candidate on the no-restore grown family

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

## Relation to Gate B

Read this together with:

- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)

This note should be promoted only if the geometry-sector candidate retains a
positive declining far-field tail on the no-restore family. Otherwise it is a
bounded negative for the distance-law extension of that candidate.
