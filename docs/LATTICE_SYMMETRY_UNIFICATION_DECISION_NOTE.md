# Lattice Symmetry Unification Decision Note

**Date:** 2026-04-03  
**Status:** negative on the dense ordered-lattice symmetry window

This note records the canonical decision test for whether the ordered lattice +
explicit symmetry line can move from a same-family two-harness bridge to a true
one-family retained architecture.

Artifacts:

- [`scripts/lattice_symmetry_unification_decision.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_symmetry_unification_decision.py)
- [`logs/2026-04-03-lattice-symmetry-unification-decision.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-symmetry-unification-decision.txt)

## Scope

This decision does **not** replace the current retained family split:

- exact mirror remains the flagship coexistence lane
- `Z2 x Z2` remains the best decoherence / range-extension lane
- ordered lattice remains the strongest distance-law branch

The only question here is whether the dense ordered-lattice symmetry extension
can merge those advantages on one review-safe retained setup.

## Setup

- ordered 2D lattice with explicit `Z2` symmetry and standard linear transport
- dense sweep `max_dy = 3, 4, 5, 6`
- canonical two-slit family: upper rows `[3, 4, 5]`, mirrored lower rows
- canonical mass convention: one mass node on the gravity layer at
  `top_slit + 1`
- detector observable: final-layer centroid shift
- companion Born audit: same-family 3-slit Sorkin card, **not** the exact same
  2-slit aperture card used for MI / `d_TV` / gravity

A compact tradeoff map then varied:

- slit geometry: `narrow_center`, `wide_center`, `wide_outer`
- mass offset relative to the top slit: `-1, 0, +1`

## Canonical Sweep

| `max_dy` | `MI` | `d_TV` | `pur_cl` | `1-pur_cl` | gravity | sign | Born `|I3|/P` | `k=0` |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 3 | `0.339` | `0.590` | `0.954` | `0.046` | `-7.9536` | away | `4.88e-16` | `0.00e+00` |
| 4 | `0.517` | `0.735` | `0.876` | `0.124` | `-7.4171` | away | `6.54e-16` | `0.00e+00` |
| 5 | `0.653` | `0.835` | `0.915` | `0.085` | `-6.5389` | away | `4.24e-16` | `0.00e+00` |
| 6 | `0.380` | `0.574` | `0.959` | `0.041` | `-5.4673` | away | `7.61e-16` | `0.00e+00` |

So the canonical family is Born-clean, keeps nontrivial MI and decoherence, and
keeps the `k=0` control exactly zero, but it never produces attraction on the
same 2-slit card.

## Distance-Law Read

Barrier harness, canonical slit family:

- all four `max_dy` cases stay **negative at every tested `b`**
- the barrier-harness magnitude can decay on the tail, but there is **no
  attraction-preserving region** to promote

No-barrier companion harness:

- `max_dy = 3`: tail fit `alpha = -0.98`, `R^2 = 0.93`
- `max_dy = 4`: tail fit `alpha = -1.68`, `R^2 = 0.92`
- `max_dy = 5`: tail fit `alpha = -3.37`, `R^2 = 0.75`
- `max_dy = 6`: tail fit `alpha = -1.55`, `R^2 = 0.89`

So the dense symmetry extension can still show decaying `|delta|` on a
no-barrier companion harness, but that does not rescue the same-slit barrier
sign failure.

## Tradeoff Map Read

Across the full `4 x 3 x 3 = 36` tradeoff rows:

- Born companion audit is clean on `36/36`
- nontrivial MI plus nontrivial decoherence survives on `36/36`
- positive gravity appears on `0/36`
- retained one-family rows: `0/36`

The slit-geometry retuning does not fix the sign:

- `narrow_center`, `wide_center`, and `wide_outer` all stay gravity-negative
- offsets `-1, 0, +1` all stay gravity-negative

The beam-depletion diagnostic points in the same direction. On the canonical
`max_dy = 5` card, the upper mass-side single-slit throughput falls to
`0.0406 x` its flat baseline, while the opposite slit still carries `0.7441 x`
its baseline. That is a same-slit depletion / opposite-shift read, not a clean
centroid-toward-mass read.

## Blocker

The blocker is **not** Born failure and it is **not** lack of path
multiplicity:

- Born stays machine-clean everywhere tested
- MI and decoherence stay real everywhere tested

Simple aperture retuning is also disfavored, because the sign stays negative
across all tested slit geometries and nearby mass offsets.

The narrow read is:

- the dominant failure mode is the unresolved same-slit beam-depletion sign
  problem on the symmetric two-slit barrier
- on this dense ordered-lattice symmetry window, that behaves like a real
  one-family incompatibility rather than a missing Born or decoherence pocket

## Conclusion

**Negative:** two-slit decoherence and same-slit attractive gravity remain
incompatible on the ordered lattice family in the tested dense symmetry window.

The ordered lattice therefore remains a same-family two-harness bridge only:
use it for the retained distance-law branch and bounded coexistence reads, but
do not promote this lattice-symmetry line to `docs/UNIFIED_PROGRAM_NOTE.md`.
