# Gate B V6 Near-Field Comparator Note

**Date:** 2026-04-05  
**Status:** bounded exact-vs-grown control for the retained mixed near-field row

## Artifact chain

- [`scripts/gate_b_v6_nearfield_comparator.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_v6_nearfield_comparator.py)
- [`logs/2026-04-05-gate-b-v6-nearfield-comparator.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-v6-nearfield-comparator.txt)

## Question

Is the mixed signal in the frozen v6 replay evidence that the retained
structured-growth rule fails relative to the ordered-lattice control, or is it
the same near-field optics problem that already appears on the exact grid?

This comparator stays narrow:

- retain the frozen v6 setup exactly:
  - `h = 0.5`
  - `layers = 13`
  - `half-width = 5`
  - `y_mass = 1.0, 1.5, 2.0`
  - strengths `0.75, 1.0, 1.25`
- hold the generated row fixed at the retained mixed row
  `drift = 0.3`, `restore = 0.5`
- compare it directly against the ordered-lattice control on the same grid

## Frozen Result

Overall:

- exact grid: `6/9` `TOWARD`, mean detector-centroid shift `+0.000007`
- retained grown row: `33/36` `TOWARD`, mean detector-centroid shift
  `+0.000021`

By near-field bucket:

| `y_mass` | exact control | grown row |
| --- | --- | --- |
| `1.0` | `0/3` `TOWARD`, mean `-0.000019` | `9/12` `TOWARD`, mean `+0.000006` |
| `1.5` | `3/3` `TOWARD`, mean `+0.000011` | `12/12` `TOWARD`, mean `+0.000023` |
| `2.0` | `3/3` `TOWARD`, mean `+0.000030` | `12/12` `TOWARD`, mean `+0.000035` |

Closest-bucket detail (`y = 1.0`):

- exact grid is `AWAY` on all three tested strengths:
  `-0.000014, -0.000019, -0.000023`
- grown seed `5`: `3/3` `TOWARD`
- grown seed `18`: `3/3` `TOWARD` with near-zero positive deltas
- grown seed `31`: `3/3` `TOWARD`
- grown seed `44`: `0/3` `TOWARD`

So the full v6 miss set is now localized very tightly:

- only the closest near-field bucket is mixed
- within that bucket, only one of the four retained seeds flips all three
  strengths

## Safe Read

The clean bounded statement is:

- the v6 mixed result is **not** a case where the grown rule collapses while
  the exact grid stays clean
- the ordered-lattice control is already worse on the closest bucket
- the retained grown row is actually better than the exact grid there, even
  though it is still not universal across all seeds

That sharpens the Gate B read:

- far-field closure remains the main retained positive
- the mixed near-field region is now localized to the closest bucket
- the near-field issue is best read as a bounded beam-optics / detector-geometry
  effect, not as evidence that structured growth fails relative to the exact
  lattice

## Guardrail

This note does **not** close full Gate B.
It does **not** prove that every generated row will beat the exact control at
close range.
It only freezes the missing exact-vs-grown control for the retained mixed v6
row.
