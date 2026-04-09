# Ordered-Lattice Quasi-Persistent Relaunch Note

**Date:** 2026-04-04  
**Status:** bounded support/compression control for a quasi-persistent packet surrogate

## Artifact chain

- Script: [`scripts/ordered_lattice_quasi_persistent_relaunch.py`](/Users/jonreilly/Projects/Physics/scripts/ordered_lattice_quasi_persistent_relaunch.py)
- Log: [`logs/2026-04-04-ordered-lattice-quasi-persistent-relaunch.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-ordered-lattice-quasi-persistent-relaunch.txt)

This probe asks a narrow question:

- can a localized packet on the retained 3D ordered-lattice family be
  compressed into a small-support surrogate and relaunched without the
  downstream free propagation changing too much?

The answer on the frozen `h = 0.5`, `W = 8`, `L = 12` family is:

- yes, in a bounded control sense
- no, in the sense of a persistent-mass theorem

## Frozen result

Two seed packets were tested:

- `point`
- `compact5`

For each seed, the free-stage packet was compressed to its top-5 support
bins and relaunched on the same ordered-lattice family.

### `point`

- free spread: `2.7599`
- 90% support: `20` z-bins
- top-5 capture fraction: `0.376`
- stage-1 carry overlap: `0.6131`
- field-induced centroid shift: `+0.000144`
- relaunch carry overlap: `0.9516`
- relaunch field shift: `+0.000024`

### `compact5`

- free spread: `2.2539`
- 90% support: `16` z-bins
- top-5 capture fraction: `0.462`
- stage-1 carry overlap: `0.6797`
- field-induced centroid shift: `+0.000083`
- relaunch carry overlap: `0.9839`
- relaunch field shift: `+0.000025`

## Safe read

This is the strongest honest read from the control:

- localized packets remain recognizable after one free propagation segment
- compressing the detector-layer packet to a small top-5 support state still
  preserves most of the downstream free-profile identity
- the quasi-persistent surrogate is therefore plausible as a bounded control
  object

But this does **not** yet produce:

- a self-maintaining persistent object
- an independently measurable inertial mass
- a closed inertial-response theorem

## Relation to the packet re-identification control

This relaunch note should be read together with
[`ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md):

- the re-identification control says the packet remains recognizable
- this relaunch control says the compressed packet surrogate can be launched
  again without collapsing the downstream profile

Together they narrow the blocker, but they do not close it.

The 2D cross-family sanity note is:

- [`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md)

## Best next move

If we want a real inertial-response probe, the next step is to see whether the
same surrogate can be given a reproducible response measure that survives
across at least one more propagation segment.

If that fails, the honest conclusion remains:

- useful quasi-persistent control
- no persistent-mass theorem yet
