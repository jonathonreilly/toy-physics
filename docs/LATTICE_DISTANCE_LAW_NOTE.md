# Lattice Distance-Law Note

**Date:** 2026-04-03  
**Status:** proposed_retained ordered-lattice distance-law branch

This note freezes the ordered-lattice distance-law result that reopens the
gravity-distance question outside the current random-connected symmetry
architecture.

Artifacts:

- [`scripts/lattice_no_barrier_distance.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_no_barrier_distance.py)
- [`logs/2026-04-03-lattice-no-barrier-distance.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-no-barrier-distance.txt)
- companion sign-changing barrier probe:
  [`scripts/lattice_mirror_distance.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_mirror_distance.py)

## Question

The earlier closure on the mirror / random-connected symmetry family said that
the current connected DAG architecture does not retain a clean `1/b` law
because transverse spreading destroys beam confinement.

The ordered-lattice question is narrower:

- if transport is regular enough to keep the beam confined, does a clean
  distance-dependent gravity magnitude appear?

## Setup

- ordered 2D lattice with forward edges and `|Δy| <= 1`
- `N = 40`
- half-width `= 20`
- source at `y = 0`
- **no barrier**
- one mass node row at `y = b` on the gravity layer
- `k = 5.0`
- detector readout: centroid shift `delta`

## Retained result

The ordered lattice gives a clean distance-dependent magnitude law on the
far-field window `b >= 7`:

```text
|delta| ~= 23.5071 * b^(-1.052)
R^2 = 0.9850
```

Saved rows:

| b | `delta` | `|delta|` |
|---|---:|---:|
| 3 | `-3.5350` | `3.5350` |
| 5 | `-3.3798` | `3.3798` |
| 7 | `-2.8797` | `2.8797` |
| 10 | `-2.1879` | `2.1879` |
| 13 | `-1.6612` | `1.6612` |
| 16 | `-1.2787` | `1.2787` |
| 19 | `-1.0045` | `1.0045` |

And the phase-only control remains clean:

- `k = 0` gives `+0.000000e+00`

## Interpretation

This is the first retained branch in the repo that supports a clean
distance-dependent gravity magnitude law.

Important scope limits:

- the signed centroid shift is **negative** on this no-barrier harness, so the
  retained law is currently about `|delta|`, not a clean attractive signed
  deflection law
- the barrier lattice and no-barrier lattice are different measurement
  geometries; the no-barrier harness gives the cleanest law, while the barrier
  harness shows sign-changing distance dependence
- this result does **not** rescue the old distance-law claim on the flagship
  mirror / random-connected symmetry family

## Project-level read

The safest synthesis update is:

- **random-connected symmetry family:** distance law remains a structural
  negative
- **ordered-lattice family:** distance-law branch is now retained and
  review-safe on the no-barrier harness

So the project now has:

- a flagship symmetry-protected coexistence program
- and a separate ordered-lattice branch that reopens the distance-law bridge

## Next step

The highest-value next move on this branch is:

- test whether an ordered lattice can inherit enough of the mirror / symmetry
  program to unify:
  - Born
  - strong slit separation / decoherence
  - gravity
  - distance law

That is the natural “lattice-mirror hybrid” frontier.
