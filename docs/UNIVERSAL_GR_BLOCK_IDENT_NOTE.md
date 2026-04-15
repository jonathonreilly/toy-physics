# Universal GR Blockwise Einstein/Regge Identification Note

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / blockwise identification note  
**Ownership:** universal blockwise Einstein/Regge identification only

## Verdict

The canonical universal block projectors are exact, but the unique universal
Hessian does **not** already identify the Einstein/Regge law blockwise in the
strong sense.

What it does identify exactly is:

- lapse
- shift
- spatial trace

What remains blocked is the final `trace ↔ shear` localization inside the
traceless spatial sector.

So the strongest exact blockwise statement is:

> the universal Hessian is canonically block-localized on lapse and shift,
> but it still carries a rank-1 trace-shear mixer, so the blockwise
> Einstein/Regge identification is not complete yet.

## Exact block projectors

On the current canonical universal basis, the exact block projectors are:

- `P_lapse`
- `P_shift`
- `P_trace`
- `P_shear`

with ranks:

- `1`
- `3`
- `1`
- `5`

They are exact, orthogonal, and complete on the symmetric `3+1` sector.

The invariant `A1` core is still

`Pi_A1 = P_lapse + P_trace = diag(1,0,0,0,1,0,0,0,0,0)`.

## What the block test checks

The finite-prototype universal Hessian is the exact symmetric bilinear form
already used on the direct universal route.

The blockwise test checks whether that unique Hessian:

1. is block-diagonal under `P_lapse`, `P_shift`, `P_trace`, `P_shear`;
2. already fixes the Einstein/Regge law blockwise; or
3. leaves a residual block-level obstruction.

## Strongest exact identification

The Hessian is already exact on the following blocks:

- lapse block: exact and isolated
- shift block: exact and isolated
- trace block: exact and isolated as a core channel

So the universal Hessian already identifies the `lapse ⊕ shift` part blockwise.

That is the strongest exact identification available from the current atlas.

## Exact residual obstruction

The only remaining cross-block term on the finite prototype is the mixed
`trace ↔ shear` block.

That residual is:

- nonzero
- rank `1`
- exactly the obstruction to turning the canonical block split into a fully
  blockwise Einstein/Regge identification

Equivalently:

> the universal Hessian is blockwise exact except for a single trace-shear
> mixer.

This means the current atlas does not yet supply the final curvature
localization inside the traceless spatial sector.

## Honest status

The current direct universal route is:

- exact at the scalar observable level;
- exact at the `3+1` kinematic lift level;
- exact at the invariant `A1` core level;
- exact at the lapse/shift block level;
- blocked at the trace-shear block-localization level.

So the answer to the blockwise question is:

> no, the unique universal Hessian does not yet identify the Einstein/Regge
> law blockwise all the way through; the exact remaining block-level
> obstruction is a rank-1 trace-shear mixer.

