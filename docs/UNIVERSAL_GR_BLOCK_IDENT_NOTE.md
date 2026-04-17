# Universal GR Blockwise Einstein/Regge Identification Note

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / blockwise identification note  
**Ownership:** universal blockwise Einstein/Regge identification only

## Verdict

This note records the anisotropic finite-prototype audit only.

On the bookkeeping prototype `diag(2,3,5,7)`, the canonical universal block
projectors are exact, but the unique universal Hessian does **not** identify
the Einstein/Regge law blockwise in the strong sense because it carries a
rank-1 `trace ↔ shear` mixer.

That is **not** the current live direct-universal blocker on the invariant
`PL S^3 x R` background. The exact invariant-background result is now in
[UNIVERSAL_GR_ISOTROPIC_SCHUR_LOCALIZATION_NOTE.md](/Users/jonreilly/Projects/Physics/docs/UNIVERSAL_GR_ISOTROPIC_SCHUR_LOCALIZATION_NOTE.md),
where the `trace ↔ shear` mixer vanishes identically on `diag(a,b,b,b)`.

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

The honest current reading is:

- this note proves a real anisotropic prototype obstruction;
- the direct universal branch has since improved on the invariant
  `PL S^3 x R` background;
- the live remaining gap is now operator identification / normalization on
  the already-localized isotropic background, not trace-shear leakage.
