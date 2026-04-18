# Eigenvalue Statistics and Anderson Phase Note

**Date:** 2026-04-11  
**Status:** bounded companion on the current `main` surface; not promoted to flagship core
**Script:** `frontier_eigenvalue_stats_and_anderson_phase.py`

## Scope

This script contains two separate probes:

1. eigenvalue-spacing statistics under self-gravity
2. an Anderson-vs-gravity phase map on the boundary-law coefficient

The two should not be collapsed into one headline claim.

## Part 1: Eigenvalue Statistics

Surface:

- `10 x 10` periodic staggered lattice
- `G in {0, 1, 5, 10, 20, 50, 100}`
- diagnostic: mean spacing ratio `<r>`

Result:

- `G=0`: `<r> = 0.2882`
- peak value: `0.4326` at `G=5`
- all tested `G` remain below the Poisson-GOE midpoint `0.458`

So the clean statement is:

> No Poisson-to-Wigner-Dyson transition is detected on this audited surface.

This is a useful negative result and is consistent with the repo-wide
"spectral, not chaotic/dynamical" interpretation.

## Part 2: Anderson-Gravity Phase Map

Surface:

- periodic staggered lattices with `L = 6, 8, 10, 12`
- `G in {0.5, 1, 2, 5, 10, 20, 50}`
- random disorder controls with 5 seeds
- comparison metric:
  - boundary-law coefficient difference `sigma_alpha`
  - auxiliary sign-count diagnostic

### Strongest positive window

The strongest separation from disorder is:

- `L=8`, `G=5`
- `sigma_alpha = 13.2`

Other strong rows:

- `L=8`, `G=2`: `12.2`
- `L=8`, `G=10`: `9.2`
- `L=12`, `G=5`: `5.1`
- `L=12`, `G=10`: `4.3`
- `L=12`, `G=20`: `3.6`
- `L=10`, `G=2`: `3.1`
- `L=10`, `G=5`: `3.7`

### Honest interpretation

The separation from disorder is real, but it is not uniform in size:

- `L=8` is the strongest and somewhat unusually sensitive surface
- `L=10` and `L=12` support a more modest but still real window at
  roughly `G in [2, 20]`
- `L=6` is inconsistent and only becomes significant at `G=10`
- `G=50` is no longer a strong discriminator on any size

So the clean statement is:

> Gravity is most cleanly distinguishable from matched Anderson disorder in a
> finite perturbative window, strongest on `L=8` and still present on
> `L=10,12` for `G ~ 2-20`.

That is stronger and more accurate than the older single-control `2.7σ`
statement, but weaker than a universal `L>=10` claim.

## Sign Diagnostic Caveat

The sign-count auxiliary is not the main result here.

- gravitational runs always return `+20`
- random controls can also return positive sign counts on some sizes

So the real discriminator in this script is the boundary-law coefficient
separation, not the sign row by itself.

## Use

Use this note when the claim is:

- self-gravity is measurably distinguishable from matched disorder
- the distinction lives in a finite `G`-window, not uniformly everywhere
- self-gravity does not drive a chaos transition on this audited surface

Do **not** use it to claim:

- universal `L>=10` dominance
- a chaos transition
- a disorder-free proof of "gravity is real" in every regime
