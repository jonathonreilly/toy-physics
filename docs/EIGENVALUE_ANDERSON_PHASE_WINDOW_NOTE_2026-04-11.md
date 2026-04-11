# Eigenvalue-Spacing and Anderson Phase Window Note

**Date:** 2026-04-11  
**Status:** retained candidate on frontier; not yet promoted  
**Script:** `frontier_eigenvalue_phase_window.py`

## Scope

This note is intentionally narrower than the combined phase-map runner. It
answers two questions only:

1. Is the eigenvalue-spacing negative result stable?
2. What is the strongest defensible perturbative window where gravity is
   distinguishable from matched disorder?

## 1. Eigenvalue-Spacing Result

Surface:

- `10 x 10` periodic staggered lattice
- `G in {0, 1, 5, 10, 20, 50, 100}`
- diagnostic: mean spacing ratio `<r>`

Result:

- `G=0`: `<r> = 0.2882`
- peak value: `0.4326` at `G=5`
- all tested `G` remain below the Poisson-GOE midpoint `0.458`

Clean statement:

> No Poisson-to-Wigner-Dyson transition is detected on this audited surface.

This is the stable negative result. It supports the repo-wide spectral thesis:
the self-consistent staggered Hamiltonian does not show a chaos transition on
this size and parameter range.

## 2. Anderson-Gravity Phase Window

Surface:

- periodic staggered lattices with `L = 6, 8, 10, 12`
- `G in {0.5, 1, 2, 5, 10, 20, 50}`
- random disorder controls with 5 seeds
- main discriminator: boundary-law coefficient separation `sigma_alpha`

### Strongest single point

The strongest single separation from matched disorder is:

- `L=8`, `G=5`
- `sigma_alpha = 13.2`

This is the peak point, but it is not the best cross-size claim because
`L=8` is unusually sensitive.

### Strongest defensible cross-size window

If the claim must survive both `L=10` and `L=12`, the defensible perturbative
window is:

- `G in [2, 5]`
- `L=10`: `sigma_alpha = 3.1` at `G=2`, `3.7` at `G=5`
- `L=12`: `sigma_alpha = 3.5` at `G=2`, `5.1` at `G=5`

This is the cleanest window that is simultaneously:

- perturbative
- above the `3σ` threshold on both stable sizes
- not dependent on the anomalously sensitive `L=8` surface

### Size caveat

- `L=8` is the most sensitive surface and gives the largest sigma values
- `L=6` is inconsistent and only becomes significant at `G=10`
- `G=50` is not a robust discriminator on any tested size

So the strongest defensible statement is:

> Gravity is distinguishable from matched disorder in a finite perturbative
> window, with the best cross-size support at `G = 2-5` on `L = 10, 12`.

That is stronger than the earlier single-control `2.7σ` claim, but weaker
than a universal `L >= 10` statement.

## Sign Diagnostic Caveat

The sign-count auxiliary is not the main discriminator here.

- gravitational runs are always positive on the audited surface
- random controls can also produce positive sign counts on some sizes

The real signal is the boundary-law coefficient separation, not the sign row.

## Use

Use this note when the claim is:

- self-gravity is measurably distinguishable from matched disorder
- the distinction lives in a finite perturbative window
- eigenvalue spacing stays Poisson-like and does not cross into a chaos
  transition on the audited surface

Do **not** use it to claim:

- universal `L >= 10` dominance
- a chaos transition
- disorder-free proof of gravity in every regime
