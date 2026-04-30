# Universal GR Casimir Block Localization on `PL S^3 x R`

**Status:** support - exact Casimir block-localization step
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / canonical block-localization theorem step

## Verdict

The direct universal route already has a canonical lapse/shift/trace/shear
block split.

The old universal blocker was too strong because it asked for a full canonical
complement frame. That is more than GR needs at this stage.

What is actually needed is a canonical block localization into:

- lapse
- shift
- spatial trace
- traceless spatial shear

and the current universal stack already supplies exactly that.

## Exact ingredients

The universal stack already had:

- exact scalar observable generator `W[J]`
- exact `PL S^3 x R` lift
- exact unique symmetric `3+1` quotient kernel
- exact invariant projector `Pi_A1`

with

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

So lapse and spatial trace were already canonically fixed.

## Casimir theorem on the complement

On the 8D complement of `Pi_A1`, the universal `SO(3)` generators define the
Casimir operator

`C = G_x^2 + G_y^2 + G_z^2`.

Its exact spectrum on the current canonical universal representation is:

- `-2` with multiplicity `3`
- `-6` with multiplicity `5`

These are exactly the `j=1` and `j=2` irreps:

- `j=1`: shift vector block
- `j=2`: traceless spatial shear block

So the spectral projectors of `C` canonically split the complement into:

- shift (`dim 3`)
- traceless shear (`dim 5`)

## Canonical block projectors

The full universal block projectors are therefore:

- `P_lapse`
- `P_shift`
- `P_trace`
- `P_shear`

with ranks:

- `1`
- `3`
- `1`
- `5`

They are:

- exact
- orthogonal
- complete
- commuting with the universal `SO(3)` generators

So the universal route now has an exact canonical block-localization operator
into the physically relevant GR channel blocks.

## What this changes

This sharply upgrades the direct universal route.

Before:

> the route was blocked by the absence of a canonical complement-frame bundle.

Now:

> the route already has a canonical block localization into lapse / shift /
> trace / shear, and the real remaining question is whether that canonical
> block-localized Hessian is already enough to identify the Einstein/Regge law.

So the missing object is smaller than previously stated.

## Remaining open issue

The current theorem does **not** yet prove full GR.

What remains open is whether the canonical block-localized universal Hessian:

- already matches Einstein/Regge dynamics blockwise, or
- still needs an extra theorem inside the shift/shear blocks

for example:

- channel normalization
- sign convention
- constraint interpretation
- blockwise curvature identification

But the direct universal route is now materially stronger:

- canonical block localization is no longer missing.

## Bottom line

The direct universal route has cleared a real obstacle.

It now has a canonical, exact block-localization operator:

`lapse ⊕ shift ⊕ trace ⊕ traceless-shear`.

That means the flagship GR route should now focus on:

> identifying the canonical block-localized universal Hessian with the
> Einstein/Regge law, rather than searching for a full complement frame.
