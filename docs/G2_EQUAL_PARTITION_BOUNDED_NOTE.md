# G2 Equal-Partition Bound

**Date:** 2026-04-12
**Status:** Bounded coupling normalization; equal-partition principle remains open
**Script:** `scripts/frontier_g2_lattice_derivation.py`

## What is derived

The staggered hopping structure gives a clean lattice-side normalization:

- the per-direction kinetic weight is `1/2`
- the total Euclidean spacetime weight is `(d+1)/2`
- the ratio is `1/(d+1)` if the directions are equally partitioned

That is the honest output of the current script and its local check.

## What is not yet derived

The missing theorem is the equal-partition principle itself:

- why the gauge coupling should be identified with the per-direction fraction
- why the total unit coupling should be distributed democratically across all
  `d+1` directions
- why this should follow from the graph/staggered structure rather than being
  imposed as a geometric normalization rule

## Safe claim

The current lane supports:

- a derived lattice-side weight decomposition
- a conditional `g_2^2 = 1/(d+1)` statement

It does not yet support:

- an unconditional derivation of `g_2^2 = 1/(d+1)` from the staggered action
  alone

## Next theorem

Prove the equal-partition principle from the graph/staggered symmetry, or keep
the gauge-coupling lane explicitly bounded at the conditional normalization
statement.
