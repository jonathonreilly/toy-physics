# Geometry Superposition on a DAG Ensemble

**Date:** 2026-04-11  
**Script:** `frontier_geometry_superposition.py`  
**Status:** exploratory path-sum result, not a staggered retained result

## Question

If amplitudes are coherently summed across different DAG geometries, does the
detector distribution differ from the incoherent classical mixture?

## Important Scope

This script is **not** a staggered-fermion geometry-superposition harness.
It is a DAG-ensemble path-sum probe built on the older `toy_event_physics`
stack.

So this result should not be described as a new retained staggered result.

## Rerun Result

Current rerun output on `2026-04-18`:

- raw coherent-vs-incoherent contrast: `3.93%`
- normalized phase-only contrast: `3.93%`
- centroid shift: `0.0574`
- width change: `0.0211`
- pairwise detector-phase differences up to about `0.323 rad` (`18.5°`)

Current mainline fix:

- the added-edge DAG variant no longer uses the broken early-exit loop from the
  review finding
- the added-edge geometry now samples valid forward skip edges explicitly, so
  the `added-10%` row is a real perturbed geometry rather than a sometimes-empty
  pseudo-variant

## Safe Read

This is a real **bounded path-sum geometry-superposition signal**:

- different DAG geometries induce measurably different detector phases
- coherent geometry summation is distinguishable from the incoherent mixture
- the phase differences are modest but clearly nonzero
- the added-edge perturbation family is now constructed honestly on current
  `main`

## What This Is NOT

- not a retained staggered-fermion result
- not the claimed `TV=0.37`, `TVq=0.079`, `dphi=1.87` headline
- not yet a BMV-style gravity-entanglement closure

## Correct Role In The Repo

Treat this as:

- a real historical/path-sum exploratory lead
- useful motivation for building a proper staggered geometry-superposition
  harness
- not part of the current staggered headline package
