# Tensor Transfer Localizes to Intra-Orbit Shell Structure

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_intraorbit_source_law.py`  
**Status:** exact localization of the remaining microscopic gravity datum

## Purpose

The selector-transfer obstruction already proved that the current retained
shell toolbox does **not** determine the remaining tensor coefficient
`tau_tensor` exactly.

This note asks the next sharper question:

> if the current shell toolbox is insufficient, what microscopic shell datum is
> actually still missing?

Using the retained shell/projector/DtN stack from the derivation atlas, the
answer is now much more specific.

## Retained shell tools already in play

The current branch already has:

- exact projector-shell source law
- exact reduced shell law
- exact DtN anisotropic orbit mode

Those are exactly the gravity shell tools already treated as reusable
infrastructure in the main-branch derivation atlas.

## Orbit-summed shell data are still identical

On the exact local `O_h` and finite-rank families, the normalized shell source
on the sewing band `3 < r <= 5` has the same orbit means on every active orbit:

- max orbit-mean difference: `6.939e-18`

So even the full shell source, once reduced to orbit-summed data, is still the
same on the two audited families.

This is stronger than the earlier obstruction from shell means alone.

## The distinguishing datum is intra-orbit shell fine structure

The exact local `O_h` shell source is orbit-constant on each shell orbit:

- max orbit standard deviation: `2.349e-17`
- weighted RMS orbit standard deviation: `1.252e-17`

The finite-rank shell source is not orbit-constant:

- max orbit standard deviation: `1.727253e-04`
- weighted RMS orbit standard deviation: `6.342145e-05`

So the two families differ only after passing beyond orbit sums into
microscopic intra-orbit structure.

## Why this matters for the tensor gap

The selector-transfer coefficients still differ:

- `tau_tensor(O_h) = 4.388505e-02`
- `tau_tensor(finite-rank) = 4.073405e-02`
- relative difference: `7.180115e-02`

But that mismatch appears **after** all orbit-summed shell data have already
collapsed to the same object.

Therefore the clean conclusion is:

> the remaining tensor-transfer law cannot factor only through orbit-summed
> shell-source data. The missing microscopic input is intra-orbit shell
> structure on the sewing band.

## What this changes

Before this note, the remaining gravity target could still be phrased vaguely
as:

- derive additional microscopic source/lift data beyond the reduced shell
  surface

After this note, the open target is sharper:

- derive how intra-orbit shell-source structure transfers into the tensor
  boundary drive

That is a materially narrower theorem target.

## Current best gravity read

The strongest honest statement now is:

> the retained shell toolbox fixes the orbit-summed shell source completely on
> the audited restricted class, but full tensor completion still depends on
> intra-orbit shell fine structure. Full nonlinear GR therefore remains open on
> a microscopic intra-orbit shell-to-tensor lift law, not on any unresolved
> orbit-summed shell observable.

This does **not** close full nonlinear GR. It does localize the remaining gap
to a very specific microscopic datum.
