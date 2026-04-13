# Universal Radial Shell Profile for the Strong-Field Matching Law

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_universal_shell_profile.py`  
**Status:** Exact universality result for the current exact source families

## Purpose

The gravity program had already established:

- the sewing shell exists exactly on the lattice
- it carries the correct total charge exactly
- its radial part already captures the exterior field well

That still left one obvious concern:

> perhaps each exact source family carries a different shell profile, so the
> matching law is still family-dependent

This note removes that ambiguity for the current exact source families on the
Codex branch.

## Result

Take the exact shell source `sigma_R` at the physically relevant cutoff
radius `R = 4`, and form its shell-radial average `sigma_rad`.

Normalize by the total charge:

`k_shell(r) = sigma_rad(r) / Q`

The script compares this normalized radial shell profile for:

1. the exact local `O_h` source family
2. the exact finite-rank source family

and finds:

> the normalized shell profile is identical to machine precision across the
> two exact source families

The shared shell radii are:

- `sqrt(10)`
- `sqrt(11)`
- `sqrt(12)`
- `sqrt(13)`
- `sqrt(14)`
- `4`
- `sqrt(17)`
- `sqrt(18)`
- `sqrt(19)`
- `sqrt(20)`
- `sqrt(21)`
- `5`

and the normalized shell weights agree exactly on every one of them.

## Interpretation

This means the exact shell source is not merely “radial enough.”

It actually reduces to

`sigma_rad = Q * k_shell`

with one universal shell kernel `k_shell` across the two exact source families
already on the branch.

So the remaining gravity problem is no longer:

- find a shell profile for each source family

It is now:

- interpret this one universal shell kernel as the effective matching / shell
  stress law of the nonlinear 4D closure
- understand the zero-monopole anisotropic correction as a controlled
  subleading shell stress

## What this closes

This closes another real ambiguity:

> for the current exact source families on `codex/review-active`, the radial
> sewing-shell profile is universal rather than family-dependent

That is a meaningful narrowing of the strong-field gravity problem.

## What this does not close

This note still does **not** close:

1. the continuum / effective-stress interpretation of the universal shell
   kernel
2. the final nonlinear 4D spacetime theorem
3. the control of the anisotropic shell correction at theorem grade

## Updated gravity target

After this note, the cleanest gravity target is sharper again:

- derive the universal shell kernel from the microscopic lattice dynamics
- interpret it as the effective shell stress / matching law
- then control the zero-monopole anisotropic correction well enough to close
  the nonlinear 4D exterior-plus-shell spacetime theorem
