# Universal Weight Decomposition Under the Shared-Axis `SO(2)` Stabilizer

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** narrow the universal curvature side after the common residual gauge has collapsed to `SO(2)`

## Verdict

The universal complement is not an undifferentiated orbit once the shared axis
is fixed.

Under the residual shared-axis `SO(2)` stabilizer, the universal complement
decomposes into definite weight sectors:

- invariant pieces;
- exact weight-1 doublets;
- a separate weight-2 shear sector.

This matters because the support dark phase carries charge `1` under the same
`SO(2)` action.

So any canonical universal lift of the support dark phase must land in a
weight-1 universal sector, not in the weight-2 shear block.

## Exact decomposition

With the shared bright axis fixed, the universal complement contains:

1. the `yz` shift pair, which is an exact weight-1 doublet;
2. the `x`-offdiagonal shear pair, which is an exact weight-1 doublet;
3. a remaining shear block containing a weight-2 sector.

So the universal side already distinguishes which complement sectors transform
with the same `SO(2)` charge as the support dark phase.

## Consequence for the phase lift

The support side now provides an exact phase-sensitive object:

`vartheta_R = atan2(d_z, d_y)`.

The universal side now tells us:

> if `vartheta_R` is lifted canonically, it must map into a weight-1 universal
> doublet.

That is a stronger statement than the older generic bundle blocker.

## Sharpened frontier

The remaining universal ambiguity is no longer:

> which arbitrary complement section?

It is:

> which canonical weight-1 universal doublet, and by what exact map, carries
> the support dark phase?

So the direct phase-to-curvature problem is now a representation-matching
problem on the residual `SO(2)` stabilizer.

## Bottom line

The all-out push has narrowed the universal side again.

The support dark phase is charge `1`, and the universal complement contains
exact weight-1 sectors. So the remaining theorem target is:

> derive the canonical map from the support dark phase into the universal
> weight-1 curvature sector.
