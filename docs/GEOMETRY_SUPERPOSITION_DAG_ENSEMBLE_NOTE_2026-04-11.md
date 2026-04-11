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

Current rerun output:

- raw coherent-vs-incoherent contrast: `4.37%`
- normalized phase-only contrast: `4.37%`
- centroid shift: `0.0557`
- width change: `0.0204`
- pairwise detector-phase differences up to about `0.257 rad` (`14.7°`)

## Safe Read

This is a real **bounded path-sum geometry-superposition signal**:

- different DAG geometries induce measurably different detector phases
- coherent geometry summation is distinguishable from the incoherent mixture
- the phase differences are modest but clearly nonzero

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
