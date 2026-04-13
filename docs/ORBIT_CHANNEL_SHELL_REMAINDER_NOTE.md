# Orbit-Channel Structure of the Sewing-Shell Anisotropic Remainder

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_orbit_channel_shell_remainder.py`  
**Status:** Exact orbit-channel reduction plus bounded exterior-control consequence

## Purpose

The gravity line had already shown:

- the sewing shell exists exactly
- its radial kernel is universal
- that kernel is the exact discrete DtN shell law

That still left one legitimate complaint:

> the remaining anisotropic shell correction might still be a large uncontrolled
> angular sector, even if the radial kernel is exact

This note removes most of that ambiguity for the current exact source families.

## Exact orbit-channel reduction

Fix the exact sewing-shell source `sigma_R` at cutoff `R = 4` and subtract its
shell-radial average:

`delta sigma = sigma_R - sigma_rad`

By construction, `delta sigma` has zero shell sum on every shell. The new point
is that for both exact source families already on `codex/review-active`:

- the orbit-sum support of `delta sigma` is confined to only four cubic orbit
  channels in the sewing band:
  - `(3,2,2)`
  - `(3,3,0)`
  - `(4,1,0)`
  - `(4,1,1)`
- those channels cancel shellwise:
  - `S_(3,2,2) + S_(4,1,0) = 0`
  - `S_(3,3,0) + S_(4,1,1) = 0`

So the anisotropic remainder is not a generic angular cloud on the shell. It is
already compressed into a tiny cubic orbit-channel sector.

## Exact universality up to one amplitude

Normalize the orbit sums by the anchor channel `S_(3,3,0)`.

The script finds that the normalized orbit-sum vector is identical to machine
precision across:

1. the exact local `O_h` source family
2. the broader exact finite-rank source family

So the anisotropic shell remainder now reduces to:

> one universal cubic orbit-channel pattern multiplied by one scalar amplitude

This is a real narrowing of the gravity problem.

## Bounded exterior consequence

Let `phi_aniso = G_0 delta sigma` and compare its shell-mean exterior response
to the shell-mean exterior response of the radial shell law `phi_rad`.

The script finds two bounded but strong consequences:

- after normalizing by the same orbit-channel anchor amplitude, the shell-mean
  exterior response of `phi_aniso` is identical to machine precision across the
  two exact source families
- the shell-mean anisotropic correction stays below `8.1%` of the radial-shell
  contribution outside the sewing band

So even before a final nonlinear closure theorem, the anisotropic shell sector
is no longer a free large-dimensional obstruction. It is one universal cubic
channel with a bounded shell-mean exterior effect.

## What this closes

This closes another real ambiguity:

> for the current exact source families, the sewing-shell anisotropy is not a
> generic uncontrolled angular remainder; it reduces to one universal cubic
> orbit-channel pattern times one scalar amplitude

## What this still does not close

This note still does **not** close:

1. the microscopic derivation of that one scalar anisotropic amplitude
2. the full effective shell-stress interpretation of the orbit-channel law
3. the final nonlinear 4D spacetime closure

## Updated gravity target

After this note, the remaining gravity target is sharper again:

- the radial DtN shell kernel is exact
- the anisotropic remainder is one universal cubic orbit-channel pattern
- the live blocker is now to derive the amplitude and stress meaning of that
  orbit-channel correction, then promote the resulting shell law into the
  nonlinear 4D closure
