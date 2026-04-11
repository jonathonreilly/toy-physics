# Wilson Mu^2 Distance Sweep Note

**Date:** 2026-04-11  
**Status:** bounded-retained calibration note on frontier; not a promoted Newton-law claim  
**Script:** `frontier_wilson_mu2_distance_sweep.py`

## Question

Is the steep open-lattice Wilson distance exponent primarily a screening-mass
artifact?

This sweep keeps the open Wilson law surface fixed and varies only the
screening mass:

- `side = 11, 13, 15`
- `G = 5`
- `d = 3, 4, 5, 6`
- packet width fixed at the base open-lattice setting
- `mu^2 = 0.22, 0.05, 0.01, 0.005, 0.001`

Observable:

- early-time mutual acceleration from `SHARED - SELF_ONLY`
- fit `|a_mut| ~ d^alpha` on clean attractive rows only

## Result

The exponent shifts strongly as `mu^2` is reduced:

- `mu^2 = 0.22` -> `alpha = -3.315` (`R^2 = 0.9960`)
- `mu^2 = 0.05` -> `alpha = -2.392` (`R^2 = 0.9978`)
- `mu^2 = 0.01` -> `alpha = -1.992` (`R^2 = 0.9984`)
- `mu^2 = 0.005` -> `alpha = -1.927` (`R^2 = 0.9985`)
- `mu^2 = 0.001` -> `alpha = -1.871` (`R^2 = 0.9986`)

All sampled configurations remained attractive and clean (`12/12` per `mu^2`).

## Interpretation

The steep `d^-3.4` falloff seen at `mu^2 = 0.22` is not stable under
screening removal. As the screening mass is reduced, the distance exponent
softens toward the Newtonian `-2` value.

Current best statement:

> On the open Wilson lattice, the distance exponent is strongly controlled by
> the screening mass. The steep `mu^2 = 0.22` law is primarily a screened
> Yukawa artifact of the chosen operating point, and the open-surface law
> moves toward `1/r^2` as `mu^2 -> 0`.

This does **not** establish an exact Newton-law derivation yet, because the
smallest `mu^2` values still sit slightly above `-2` in the tested window.
It does, however, rule out the earlier interpretation that the steep exponent
was a fixed discrete universality class independent of screening.

## Relation to the Earlier Open Wilson Note

The original open Wilson note remains valid as a description of the
`mu^2 = 0.22` surface. This addendum narrows its interpretation:

- the mutual-attraction channel is real on the open surface
- the exponent at the default screened operating point is steep
- but that steepness is largely screening-controlled

So the Wilson lane is now best read as a screened open-lattice mutual-channel
result with a clear path toward Newtonian scaling in the weak-screening
limit, not as a fixed non-Newtonian law.
