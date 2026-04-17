# Ordered-Lattice Quasi-Persistent Relaunch 2D Note

**Date:** 2026-04-04  
**Status:** bounded cross-family sanity check for the relaunch-packet idea

## Artifact chain

- Script: [`scripts/ordered_lattice_quasi_persistent_relaunch_2d.py`](/Users/jonreilly/Projects/Physics/scripts/ordered_lattice_quasi_persistent_relaunch_2d.py)
- Log: [`logs/2026-04-04-ordered-lattice-quasi-persistent-relaunch-2d.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-ordered-lattice-quasi-persistent-relaunch-2d.txt)

This is the cheapest cross-family check I could build for the relaunch-packet
idea. It mirrors the retained 3D quasi-persistent relaunch control, but on the
retained 2D ordered-lattice family.

## What it tested

The harness launches a compact Gaussian packet on the source layer, propagates
it with and without a weak external field, and compares:

- detector-layer centroid shift
- packet carry-over overlap after re-identification
- width ratio of the relaunch surrogate

The question is not whether the packet moves. The question is whether it stays
recognizable enough that a relaunch surrogate is still meaningful on a second
retained family.

## Frozen replay

On the retained `h = 0.5`, `W = 12`, `L = 20` 2D ordered-lattice family:

### Valley-linear

- capture fraction: `0.344`
- carry overlap: `0.911`
- field-induced shift:
  - `+0.000394` at `2e-5`
  - `+0.000985` at `5e-5`
  - `+0.001968` at `1e-4`
- relaunch shift:
  - `+0.000205` at `2e-5`
  - `+0.000512` at `5e-5`
  - `+0.001024` at `1e-4`
- width ratio: `1.000`

### Spent-delay

- capture fraction: `0.344`
- carry overlap: `0.911`
- field-induced shift:
  - `+0.111785` at `2e-5`
  - `+0.174422` at `5e-5`
  - `+0.242946` at `1e-4`
- relaunch shift:
  - `+0.073447` at `2e-5`
  - `+0.115193` at `5e-5`
  - `+0.161549` at `1e-4`
- width ratio: `0.996` to `0.990`

## Safe read

The bounded cross-family conclusion is:

- the packet surrogate is **family-generic enough to relaunch** on the 2D
  retained ordered-lattice family
- it is still **not** a persistent-mass theorem
- the 2D replay is a weaker surrogate than the 3D control, but it does not
  collapse or look obviously fragile

The most honest phrasing is:

- the relaunch-packet idea is family-generic at the surrogate level
- the inertial-response claim remains open

This is a diagnostic control, not a persistent-particle result.

## Relation to the 3D control

This note is the second-family companion to
[`ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md)
and
[`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md).

Together they say:

- 3D ordered lattice: packet surrogate survives and relaunches cleanly
- 2D ordered lattice: packet surrogate also survives and relaunches cleanly
- persistent inertial mass: still not produced or measured

## Best next move

The next physics step should still be a true persistent or quasi-persistent
inertial-response experiment, if one can be built without leaving the retained
ordered-lattice family too much.
