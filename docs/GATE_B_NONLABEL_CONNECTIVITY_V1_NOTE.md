# Gate B Non-Label Connectivity V1 Note

**Date:** 2026-04-05  
**Status:** bounded geometry-only forward-connectivity candidate on the no-restore grown family

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

## Relation to Gate B

Read this together with:

- [`docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md)
- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)

The safe combined picture is now:

- label-based no-restore connectivity carries the far-field package
- naive KNN+floor does not
- this geometry-only sector stencil restores the far-field package on the
  tested retained family

That is enough to make the candidate review-relevant, but not enough to close
full Gate B or to promote the rule beyond this bounded test.
