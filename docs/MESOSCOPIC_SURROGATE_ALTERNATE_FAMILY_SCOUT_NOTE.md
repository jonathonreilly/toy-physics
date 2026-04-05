# Mesoscopic Surrogate Alternate-Family Scout Note

**Date:** 2026-04-04  
**Status:** cheap scouting memo; recommends the next localized attempt only on
the retained 3D `h=0.25` family

## Question

Which already-bounded non-Gate-B family is the cheapest plausible next target
for a more localized source object, if we want to beat the retained 3D
`h=0.5` mesoscopic-surrogate family?

## Frozen evidence

The current mesoscopic-surrogate lane already freezes three useful facts:

- the retained 3D `h=0.5` localization frontier does **not** reward sharp
  localization
  - the only numerical winners are degenerate point-like cases
  - once the family is meaningfully localized, `topN` remains the least-bad
    mesoscopic control
- the retained 2D support-threshold scan also does **not** show a sharp
  collapse
  - every scanned `topN` from `1` to `81` stayed stable
  - shrinking support is not the lever there
- the retained 3D `h=0.25` family is already the strongest bounded ordered
  family for the asymptotic bridge
  - same-family closure exists
  - the near-Newtonian finite-size bridge is much cleaner than the coarse
    `h=0.5` family

## Scout result

The cheapest already-bounded family that still plausibly has room for a more
localized source object to matter is:

- the retained 3D ordered-lattice family at `h = 0.25`

Why this family:

- it is already bounded on `main`
- it has the best retained continuum-like resolution among the mesoscopic
  ordered-lattice families
- the `h = 0.5` frontier is already closed as a degenerate-point-source lane
- the 2D lane is already closed as a no-threshold lane

## Recommendation

If we do another localization attempt, it should be:

- on the retained 3D `h = 0.25` family
- with non-degenerate localized shapes only
- with an explicit minimum support or capture floor so point-like winners are
  excluded by construction

Good candidate families:

- annular windows
- tapered ellipsoids
- compact Gaussians with enforced capture floor

## Safe read

The honest recommendation is:

- do **not** keep sweeping the 3D `h=0.5` frontier
- do **not** keep hunting a 2D threshold
- if a more localized source object is still worth trying, the retained 3D
  `h=0.25` family is the cheapest plausible target

If that family still cannot beat the broad mesoscopic control, the localization
lane should be frozen as a bounded negative result.
