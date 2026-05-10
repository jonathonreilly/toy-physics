# Ordered-Lattice Quasi-Persistent Relaunch 2D Note

**Date:** 2026-04-04
**Last sync:** 2026-05-10 — narrowed to a purely numerical replay statement, in line with the
audit ask for the audited_conditional ledger entry. The runner now pins each
reported metric with explicit tolerance assertions.
**Status:** bounded numerical replay — six-row metric table on the fixed
ordered-lattice harness. This is **not** a persistent-mass theorem and
is not promoted to a family-generic claim.

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

## Safe read (narrowed 2026-05-10)

The bounded conclusion is purely numerical:

- on the fixed ordered-lattice harness above, the runner reproduces the
  six-row table (capture 0.344, carry 0.911, valley-linear width ratio
  exactly 1.000, spent-delay width ratio in [0.990, 0.996]) deterministically
- the runner now asserts each reported metric within tight numerical
  tolerances, so any drift from this table forces the note to be re-synced
- this is **not** a persistent-mass theorem
- this is **not** a "family-generic" result; the harness only tests the
  one fixed 2D ordered-lattice family at `(h=0.5, W=12, L=20)` and the
  one fixed Gaussian/top-k packet recipe
- no acceptance threshold, packet-class, reidentification rule, or
  invariance guarantee is asserted; what survives is a frozen replay of
  six numbers, not a theorem about packets

The most honest phrasing is:

- the runner produces the same six metric rows on every replay
- nothing more should be read into them than that

This is a diagnostic numerical replay, not a persistent-particle result
and not a family-genericity claim.

## Relation to the 3D control

This note is the second-family companion to
`ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md` and
`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md` (sibling artifacts;
cross-reference only — not one-hop deps of this note).

The cross-references are sibling artifacts only; they are **not** load-bearing
inputs to the table above and they are **not** used to upgrade the 2D
numerical replay into a persistent-mass or family-generic claim.

## Best next move

The next physics step would be a true persistent or quasi-persistent
inertial-response experiment, if one can be built without leaving the
retained ordered-lattice family too much. This note does not perform
that step and does not claim progress toward it; it only pins the six
numerical rows above.
