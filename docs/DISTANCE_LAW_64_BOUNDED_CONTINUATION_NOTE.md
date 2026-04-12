# 64³ Path-Sum Distance Law: Bounded Continuation Note

**Date:** 2026-04-11
**Status:** bounded continuation — not standalone closure
**Runner:** `scripts/distance_law_3d_64_closure.py`

## What was tested

Five 3D cubic lattice sizes (31³ through 64³) using the Poisson-field
path-sum propagator with valley-linear action S = L(1-f) and h²/T
normalization. A point source at the lattice center; ray deflection
measured across impact parameters b = 2..14.

## Results

| N   | alpha (b>=3) | error  |
|-----|-------------|--------|
| 31  | -1.086      | 0.010  |
| 40  | -1.069      | 0.010  |
| 48  | -1.057      | 0.012  |
| 56  | -1.040      | 0.013  |
| 64  | -1.023      | 0.012  |

Extrapolation to N → ∞: alpha_inf = -0.976 ± 0.019 (deflection),
equivalent to a force exponent of -1.976 ± 0.019, which is 1.2σ from
Newtonian -2.0.

Mass linearity (delta/M spread) confirmed at 0.1% on the same lattice.

Clear monotonic convergence: the finite-size steepening at 31³ (alpha
~ -1.09) systematically relaxes toward -1.0 as N increases.

## What this is

A single-family continuation of the 3D path-sum distance story on the
ordered cubic lattice. The convergence toward 1/r² is real and
monotonic.

## What this is not

- Not a standalone distance-law closure (single architecture family)
- Not architecture-independent (only ordered cubic lattice tested)
- Not both-masses closure
- Not a full Newton closure
- Does not include the staggered, Wilson, or irregular graph families

## Promotion status

Bounded continuation note only. Can be retained as supporting evidence
for the ordered-lattice distance-law convergence story. Does not by
itself close any promotion gate on the review inbox.

## Required for promotion

- Architecture portability (same measurement on staggered and/or
  Wilson lattices)
- Or explicit restriction of claim to ordered-cubic family level
