# Gate B Grown-Geometry Joint Package Note

**Date:** 2026-04-05  
**Status:** bounded Born / interference / decoherence transfer replay on grown geometry

## Artifact chain

- [`scripts/gate_b_grown_joint_package.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_joint_package.py)
- [`logs/2026-04-05-gate-b-grown-joint-package.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-joint-package.txt)

## Question

Do the non-gravity observables also transfer from the exact grid to the grown
geometry on the retained generated-geometry family?

This note freezes:

- Born
- `d_TV`
- `MI`
- CL-bath decoherence

on:

- exact grid
- grown geometry at `drift = 0.2`, `restore = 0.7`
- noisier grown geometry at `drift = 0.3`, `restore = 0.5` as a stress row

## Frozen result

The frozen log reports mean values across `4` seeds.

The retained moderate-drift grown row stays extremely close to the exact grid:

- exact grid: Born `2.12e-15`, `d_TV = 0.787`, `MI = 0.568`,
  decoherence `49.4%`
- grown `drift = 0.2`, `restore = 0.7`: Born `2.19e-15`,
  `d_TV = 0.811`, `MI = 0.569`, decoherence `49.4%`

The noisier `drift = 0.3` stress row remains useful as a boundary read:

- Born `2.45e-15`
- `d_TV = 0.790`
- `MI = 0.446`
- decoherence `47.2%`

## Safe read

The honest bounded statement is:

- on the retained moderate-drift generated-geometry row, the non-gravity joint
  observables transfer well from the exact grid
- the moderate-drift row matches the exact grid almost exactly on Born, `MI`,
  and decoherence, and stays close on `d_TV`
- the noisier grown row shows that the transfer is not trivial under arbitrary
  growth noise: Born remains clean, while `MI` weakens first

This is exactly the kind of boundary skeptical readers need:

- one retained moderate-drift positive row
- one noisier stress row that degrades without collapsing everything at once

## Relation to Gate B

Read this with:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
- [`docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)

Together they now support the stronger bounded package read on the retained
moderate-drift row:

- far-field gravity sign transfers
- far-field `F~M` transfers
- a positive declining distance-law fit transfers
- Born / `d_TV` / `MI` / decoherence transfer

The remaining open step is not whether one retained grown row can match the
fixed lattice package. It is how broadly that transfer survives across the full
generated-geometry family.
