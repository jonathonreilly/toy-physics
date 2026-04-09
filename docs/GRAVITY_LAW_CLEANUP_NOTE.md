# Gravity Law Cleanup Note

Date: 2026-04-02

This note records the controlled replacements for the earlier gravity-law
claims that were not review-safe.

## Why these reruns were needed

Two older scripts were useful as exploratory scans but not clean enough for
strong claims:

- `scripts/gravity_distance_v2.py`
  - changed `y_range` with impact parameter `b`
  - so geometry and beam/support width changed at the same time as `b`
- `scripts/gravity_mass_scaling.py`
  - varied mass count by taking prefixes of a drifting candidate set
  - so count and source geometry moved together

The replacements below remove those confounds.

## Controlled replacement 1: fixed-geometry distance sweep

Script:
- [gravity_distance_fixed_geometry.py](/Users/jonreilly/Projects/Physics/scripts/gravity_distance_fixed_geometry.py)

Protocol:
- one fixed graph per seed
- fixed `N`, `nodes_per_layer`, `y_range`, and `connect_radius`
- fixed barrier/slit geometry
- fixed mass count
- only the mass-anchor position moves with `b`

Best current controlled run:
- `N=30`
- `nodes_per_layer=90`
- `y_range=28`
- `connect_radius=4.0`
- `mass_count=4`
- `24 seeds`
- `b = 6, 10, 14, 18, 22, 26`

Result:
- mean shift rises to a peak at `b = 14`
- then falls on the tail:
  - `b=18`: `+1.7462 ± 0.3223`
  - `b=22`: `+1.4409 ± 0.3437`
  - `b=26`: `+0.9821 ± 0.3035`
- tail fit on the fixed geometry:
  - `delta ~= C * b^-1.545`
  - `R^2 = 0.943`

Safe conclusion:
- there is a real **peaked distance response with a falling far tail**
- the old clean `1/b²` claim does not survive as a locked statement
- the current fixed-geometry tail is nontrivial and review-worthy, but not yet
  stable enough across configurations/seed counts to promote as the final law

## Controlled replacement 2: fixed-anchor mass sweep

Script:
- [gravity_mass_scaling_fixed_anchor.py](/Users/jonreilly/Projects/Physics/scripts/gravity_mass_scaling_fixed_anchor.py)

Protocol:
- one fixed graph per seed
- one fixed anchor `y = center + b_anchor`
- on the gravity layer, define a **frozen ordering** of candidate mass nodes by
  distance to that anchor
- varying `M` takes prefixes of that same ordered set

Current clean run:
- `N=30`
- `nodes_per_layer=30`
- `y_range=12`
- `connect_radius=3.0`
- `anchor_b = 6.0`
- `24 seeds`
- `M = 1, 2, 3, 5, 8, 12`
- fit window declared in advance on `M in {2,3,5,8,12}`

Result:
- `M=2`: `+0.4230 ± 0.2356`
- `M=3`: `+0.6219 ± 0.2421`
- `M=5`: `+0.9156 ± 0.3004`
- `M=8`: `+1.3296 ± 0.3396`
- `M=12`: `+1.3510 ± 0.3513`
- fixed-anchor window fit:
  - `delta ~= 0.2872 * M^0.678`
  - `R^2 = 0.954`

Safe conclusion:
- the controlled mass window is **positive and sublinear**
- the older strong `F ∝ M` framing is not retained by the fixed-anchor rerun
- there is a real mass response, but it is currently better described as a
  sublinear window than a clean Newtonian law

## Current gravity-law status

What is retained:
- a statistically real gravity-like deflection signal exists
- controlled reruns show:
  - a peaked distance response with a falling tail
  - a positive sublinear mass window

What is not retained:
- exact `1/b²` as a locked distance law
- exact `F ∝ M` as a locked mass law

Current safe wording:
- **gravity signal is real**
- **exact force-law scaling is still unresolved**

## Best next step

Follow-up completed:

- [gravity_distance_channel_observables.py](/Users/jonreilly/Projects/Physics/scripts/gravity_distance_channel_observables.py)
  was run on the same fixed-geometry `b` sweep used above
- channel-space observables do retain structure, but they do **not** reveal a
  dramatically cleaner law than centroid:
  - `corr(centroid, b) = +0.165`
  - `corr(bundle_bias, b) = +0.289`
  - `corr(cancellation, b) = -0.685`
  - `corr(eff_ch, b) = -0.407`

Safe conclusion from the follow-up:
- channel observables are useful diagnostics, but on the current generated-DAG
  gravity lane they do not yet rescue a clean promoted force law

If we keep pushing on the gravity-law side, the next discriminator is:

1. measure channel/bundle observables on the same fixed-geometry `b` sweeps,
   on **other** candidate gravity architectures, not just the current DAG lane
2. see whether a law-like trend survives more cleanly in channel space there
   than in centroid space

That is now a better next move than continuing to promote centroid-only
distance/mass exponents as final.
