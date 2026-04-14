# Universal GR Polarization-Frame Bundle Attempt on `PL S^3 x R`

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / attempt note  
**Purpose:** test whether the current axiom-first universal stack can derive a
canonical covariant `3+1` polarization-frame / projector bundle before
curvature localization

## Verdict

The current universal stack does **not** derive a canonical polarization-frame
bundle from the scalar observable principle, the exact `3+1` lift, and the
unique symmetric quotient kernel alone.

What it does give is:

- an exact scalar observable generator;
- an exact `3+1` kinematic background `PL S^3 x R`;
- an exact tensor-valued variational candidate;
- an exact unique symmetric `3+1` quotient kernel on the finite prototype.

What it does **not** give is a canonical section or projector bundle that
splits the symmetric kernel into lapse, shift, and spatial trace/shear
channels before localization.

## Attempted derivation

The natural attempt is:

1. start from the exact `3+1` background scaffold `PL S^3 x R`;
2. use the unique symmetric quotient kernel to define the tensor channels;
3. declare the channel split to be the polarization bundle;
4. promote the induced localization to a curvature operator `Pi_curv`.

The attempt fails at step 2 -> 3.

The quotient kernel is unique, but the channel split is not canonical on the
current stack. Two valid `3+1` polarization frames related by a spatial
rotation yield different localized channel coefficients for the same kernel.
That is not a numerical artifact. It is the exact obstruction.

The audit runner records the frame dependence explicitly:

- the quotient kernel stays fixed;
- the localized channel coefficients change with polarization frame choice;
- the resulting channel mismatch is `frame_delta = 6.767e-02`.

So the current universal route determines an associated family of candidate
localizations, not a canonical polarization section or projector bundle.

## Exact obstruction

The present stack does not supply a covariant polarization frame bundle with
a distinguished connection or horizontal distribution.

Equivalently, it does not supply a canonical `Pi_curv` on the quotient kernel
alone.

The obstruction is now sharp:

- the scalar generator is exact;
- the `3+1` lift is exact;
- the symmetric quotient kernel is exact;
- the localization map is not canonical without an extra bundle primitive.

## Minimal extra primitive

The smallest missing object is now:

> a covariant `3+1` polarization-frame bundle, or equivalent projector
> bundle, equipped with a distinguished connection that canonically splits
> lapse, shift, and spatial trace/shear before curvature localization.

That is the extra primitive required to turn the exact quotient kernel into a
canonical Einstein/Regge dynamics law.

## Honest status

The current direct universal route is:

- exact at the scalar observable level
- exact at the `3+1` kinematic lift level
- exact at the symmetric `3+1` quotient-kernel level
- blocked at the covariant polarization-frame / curvature-localization level

This is the sharpest exact statement currently available on the universal
route.
