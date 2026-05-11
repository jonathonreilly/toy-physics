# Universal GR Curvature Localization Blocker Note

**Status:** support - structural or confirmatory support note
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / blocker note  
**Purpose:** isolate the minimal missing primitive on the straight-to-full-GR
path after the exact scalar observable generator, exact `3+1` lift, exact
tensor-valued variational candidate, and unique symmetric quotient kernel are
already in hand

## Verdict

This note is now historical/superseded as the live direct-universal blocker.

The current axiom-first stack gives:

- an exact scalar observable generator from the observable principle
- an exact `3+1` kinematic lift on `PL S^3 x R`
- an exact tensor-valued variational candidate on that lifted background
- an exact unique symmetric `3+1` quotient kernel on the finite prototype

It does **not** yet give:

- the final operator-identification theorem that turns the already-localized
  isotropic universal Hessian into the Einstein/Regge tensor law on the full
  `3+1` metric space

So the remaining gap is no longer a scalar problem, no longer a
quotient-uniqueness problem, no longer a complement-frame problem on the
invariant background, and no longer an isotropic operator-identification
problem either.

The older frame-orbit blocker was too strong. The direct universal branch now
has:

- exact `Pi_A1` invariant section
- exact Casimir block localization into lapse / shift / trace / shear
- exact isotropic-background Schur localization on `diag(a,b,b,b)`

That isotropic operator-identification step has now been discharged by
[UNIVERSAL_GR_ISOTROPIC_GLUE_OPERATOR_NOTE.md](/Users/jonreilly/Projects/Physics/docs/UNIVERSAL_GR_ISOTROPIC_GLUE_OPERATOR_NOTE.md).

The live remaining object is now smaller still:

> a stronger interpretation theorem beyond the exact discrete global
> Lorentzian closure already supported on `PL S^3 x R`.

## What is exact already

### Scalar generator

The axiom-side observable principle gives the scalar generator

`W[J] = log|det(D+J)| - log|det D|`

This is exact, but scalar.

### `3+1` lift

Route 2 gives the exact kinematic background

`PL S^3 x R`.

That is exact on the current atlas, but kinematic only.

### Tensor variational candidate

The scalar generator can be lifted into a tensor-valued quadratic form by
taking its metric-source Hessian on the lifted background:

`S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)`.

This is the exact tensor-valued variational candidate, but it is still only a
variational object until a curvature-localization map is supplied.

### Quotient uniqueness

On the symmetric `3+1` perturbation quotient, the Hessian kernel is the
unique bilinear lift of the scalar generator at quadratic order. On the finite
prototype used by the current runner, that quotient kernel is nondegenerate.

That proves uniqueness of the tensor candidate on the quotient. It does not
identify the kernel with Einstein/Regge curvature dynamics.

### Exact invariant section

The strongest exact invariant selector latent in the universal route is the
rank-2 `A1` projector onto lapse and spatial trace:

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

This projector is frame-independent across the sampled valid `3+1`
polarization frames and is the exact minimal-covariance selector already
present in the current construction.

### Exact canonical block localization

The universal complement also localizes exactly by the `SO(3)` Casimir into:

- shift (`j=1`)
- traceless shear (`j=2`)

So the direct universal route already has the exact block projectors

- `P_lapse`
- `P_shift`
- `P_trace`
- `P_shear`

### Exact invariant-background Schur localization

On the correct `SO(3)`-invariant lifted background, the fixed background
subspace is exactly the 2D `A1` core, so the background has the form

`diag(a,b,b,b)`.

On that background the universal Hessian candidate Schur-localizes exactly:

- all cross-block leakages vanish;
- the shift block is scalar;
- the shear block is scalar;
- the old anisotropic `trace ↔ shear` mixer disappears identically.

## Why the current stack still stops short of full GR

The present data now determine much more than before:

1. a unique bilinear kernel on the symmetric quotient;
2. an exact canonical block split into lapse / shift / trace / shear;
3. an exact isotropic-background Schur form for the universal Hessian.

What they still do not yet prove is:

1. a stronger global unrestricted-GR solution-class / interpretation theorem
   beyond the exact positive-background local closure family.

## Minimal missing primitive

The smallest honest missing object is now:

> a stronger interpretation theorem that upgrades the exact discrete global
> Lorentzian closure into whatever still stricter notion of “full GR” one
> wants beyond the project’s `PL S^3 x R` Einstein/Regge setting.

Equivalently, the missing primitive is no longer a frame bundle, no longer an
isotropic block-operator identification law, no longer invariant-family
nonlinear completion, no longer widening beyond the invariant family, no
longer merely a local operator-family theorem, and no longer merely a global
finite-atlas closure theorem.

## Honest status

The current direct universal route is:

- exact at the scalar observable level
- exact at the `3+1` kinematic lift level
- exact at the symmetric `3+1` quotient-kernel level
- exact at the canonical block-localization level
- exact at the invariant-background Schur-localization level
- exact at the local isotropic supermetric-normal-form level
- exact at the isotropic quadratic Einstein/Regge glue-operator level
- exact at the invariant-family nonlinear completion level
- exact at the positive-background extension level
- exact at the positive-background local closure level
- exact at the Lorentzian signature-class local closure level
- exact at the Lorentzian finite-atlas global closure level
- exact at the discrete global closure level recorded in
  `UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md` (downstream consumer; backticked
  to avoid length-5 cycle — this blocker note is historical/superseded and references
  the closure as a status pointer "this has been discharged", not as a load-bearing
  input; citation graph direction is *downstream closure → this blocker note*)
- still open only beyond that, at a stricter interpretation theorem beyond the
  exact discrete global closure

That is the sharpest disciplined statement available on the current atlas.
