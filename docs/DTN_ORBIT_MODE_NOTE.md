# Exact DtN Origin of the Universal Anisotropic Orbit Mode

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_dtn_orbit_mode.py`  
**Status:** Exact reduced-mode derivation plus bounded closure consequence

## Purpose

The previous shell-remainder note showed that the anisotropic sewing-shell
sector for the current exact source families collapses onto one universal cubic
orbit-channel pattern up to one scalar amplitude.

That still left one legitimate complaint:

> perhaps this is only a coincidence of the two exact source families already
> on the branch, rather than an operator-level feature of the lattice boundary
> problem itself

This note removes that ambiguity on the reduced orbit/shell-mean surface.

## Exact point-Green DtN mode

Take the seven point-Green columns on the star support and apply the same
construction as before:

1. exterior projector at cutoff `R = 4`
2. exact shell source `sigma_R`
3. shell-radial subtraction `delta sigma = sigma_R - sigma_rad`
4. orbit-sum reduction and shell-mean exterior response

The script finds:

- every star-support point-Green column induces the same normalized
  anisotropic orbit-sum vector
- every star-support point-Green column induces the same normalized shell-mean
  exterior response

So on this reduced surface, the anisotropic shell correction is already one
exact DtN mode of the star-support boundary problem.

## Exact agreement with the current exact source families

The script then compares that DtN point-Green mode to:

1. the exact local `O_h` source family
2. the broader exact finite-rank source family

and finds machine-precision agreement for both:

- the normalized orbit-sum vector
- the normalized shell-mean exterior response

So the current exact source families are not generating ad hoc family-specific
anisotropy. They are exciting the same reduced anisotropic DtN mode already
present in the lattice boundary problem.

## Interpretation

This is the cleanest strong-field gravity statement so far about the
anisotropic shell sector:

> on the reduced orbit/shell-mean surface, the sewing-shell anisotropy is one
> exact DtN mode multiplied by one scalar amplitude

That is a meaningful upgrade from “we have a bounded anisotropic remainder.”

## What this closes

This closes another real ambiguity:

> the universal anisotropic shell pattern is not just a coincidence of two
> solved source families; it is already present as an exact reduced DtN mode of
> the star-support lattice boundary problem

## What this still does not close

This note still does **not** close:

1. the microscopic derivation of the single amplitude multiplying that DtN mode
2. the full shell-stress / junction interpretation of that mode
3. the final nonlinear 4D spacetime theorem

## Updated gravity target

After this note, the gravity problem is sharper again:

- the radial shell kernel is exact and DtN-derived
- the anisotropic shell sector is one exact reduced DtN mode
- the remaining blocker is to derive the amplitude and shell-stress meaning of
  that mode, then promote the combined shell law into the nonlinear 4D closure
