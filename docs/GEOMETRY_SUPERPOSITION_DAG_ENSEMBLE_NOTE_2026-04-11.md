# Geometry Superposition on a DAG Ensemble

**Date:** 2026-04-11  
**Script:** `frontier_geometry_superposition.py`  
**Status:** bounded exploratory path-sum result on a DAG ensemble; not on the staggered release surface
**Claim type:** bounded_theorem

**Audit-conditional perimeter (2026-05-01):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
bounded_theorem`. The audit chain-closure explanation is exact: "The
live runner reproduces the bounded DAG path-sum signal and the
corrected added-edge construction. The runner output is not formatted
as classified PASS lines, so the audit lane cannot treat the
computation as a closed classified check surface." This rigorization
edit only sharpens the boundary of the conditional perimeter; nothing
here promotes audit status. The supported content of this note is
the bounded path-sum signal itself: 3.93% raw / phase-only contrast,
0.0574 centroid shift, 0.0211 width change, pairwise phase
differences up to 0.323 rad — all reproduced live by the registered
runner. The conditional gap is purely a runner-output formatting
issue (no classified PASS lines), not a numerical or scientific
discrepancy. A future runner-source rigorization adding explicit
PASS/FAIL assertions on the four numerical rows would close the
conditional perimeter; that change requires a runner SHA refresh and
is deferred.

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
