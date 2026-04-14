# Tensor Transfer Localizes to Non-Scalar Support Irreps

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_support_irrep_lift.py`  
**Status:** exact localization of the remaining microscopic source datum

## Purpose

The previous note localized the remaining tensor-transfer gap to microscopic
intra-orbit shell structure on the sewing band.

This note sharpens that again by moving back to the exact microscopic source
itself.

Using the retained star-supported source class and the exact lattice Green
solve, the question is:

> what microscopic source data generate the intra-orbit shell structure that is
> still missing from the current gravity closure?

## Exact support decomposition

On the seven-site star support, the exact source decomposes into the canonical
`O_h` support irreps:

- `A1(center)`
- `A1(shell-average)`
- `E1`, `E2`
- `T1x`, `T1y`, `T1z`

This is the natural microscopic basis already implicit in the retained
star-supported source class.

## Exact shell lift of each support irrep

The exact projector-shell source law and exact lattice Green solve show:

- the two `A1` support basis vectors lift to orbit-constant shell-source
  patterns
- the non-scalar `E ⊕ T1` basis vectors lift with:
  - zero orbit means
  - nonzero intra-orbit shell structure

Numerically:

- `A1(center)` max orbit std: `2.538e-17`
- `A1(shell)` max orbit std: `5.471e-17`
- `E1` max orbit std: `7.274e-03`
- `E2` max orbit std: `5.939e-03`
- `T1x`, `T1y`, `T1z` max orbit std: `2.737e-02`

So the shell-source split is exact:

- orbit-summed shell data come from `A1`
- intra-orbit shell structure comes from `E ⊕ T1`

## Exact finite-rank reconstruction

The finite-rank source decomposes in that support-irrep basis as:

- `A1(center) = 1.891827e+00`
- `A1(shell) = 3.119170e+00`
- `E1 = 1.190758e-01`
- `E2 = 2.055241e-01`
- `T1x = 3.811993e-02`
- `T1y = 3.034763e-02`
- `T1z = 2.265056e-02`

And the resulting shell source satisfies:

- exact full reconstruction error from the irrep lift: `2.776e-16`
- `A1` sector alone reproduces the finite-rank orbit means with error:
  `1.110e-16`
- non-`A1` sector alone reproduces the entire finite-rank intra-orbit shell
  fine structure with error:
  `2.877e-16`

So this is not just a useful interpretation. It is an exact decomposition on
the current audited class.

## What this changes

Before this note, the remaining gravity gap could be stated as:

- derive an intra-orbit shell-to-tensor lift law

After this note, the target is sharper and more canonical:

- derive the lift from the non-scalar microscopic source irreps
  `E ⊕ T1`
  into the tensor boundary channels

That is a better theorem target because it is phrased directly in the exact
source basis, not only in shell phenomenology.

## Current best gravity read

The strongest honest statement now is:

> the retained shell toolbox already determines the orbit-summed shell data,
> and the remaining missing microscopic datum is exactly the non-scalar
> `E ⊕ T1` support-irrep content of the seven-site source. Full nonlinear GR is
> therefore open on a theorem that lifts those non-scalar source irreps into
> the tensor boundary drive.

This still does **not** close full nonlinear GR. It does turn the remaining
gap into a much more canonical representation-theoretic target.
