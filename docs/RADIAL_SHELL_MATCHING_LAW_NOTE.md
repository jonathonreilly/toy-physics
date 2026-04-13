# Radial Shell Matching Law from the Exact Sewing-Shell Source

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_radial_shell_matching_law.py`  
**Status:** Exact shell-source decomposition plus bounded radial-shell reduction

## Purpose

The exact sewing-shell theorem showed that the exterior field can be written as

`phi_ext = G_0 sigma_R`

with `sigma_R` supported exactly in the finite shell band `3 < r <= 5`.

That still left one live ambiguity:

> does the shell source itself already collapse mostly onto a purely radial
> shell law, or is its anisotropic structure load-bearing for the exterior?

This note extracts the strongest bounded answer currently available.

## Exact decomposition of the shell source

On each discrete shell inside the sewing band, average `sigma_R` over all
lattice points with the same radius. This gives a unique shell-radial source

`sigma_rad`.

Then define the remainder

`delta sigma = sigma_R - sigma_rad`.

This decomposition is exact.

Because shell-averaging preserves the shell sum, it preserves the total charge:

`sum sigma_rad = sum sigma_R = Q`

and therefore

`sum delta sigma = 0`.

So the anisotropic remainder carries zero monopole charge exactly.

## Bounded exterior result

Solving the lattice Green problem for `sigma_rad` alone gives a radial-shell
matching field `phi_rad = G_0 sigma_rad`.

Comparing `phi_rad` to the exact exterior field beyond the sewing shell
(`r > 5`) gives:

### Exact local `O_h` family

- max relative exterior error: `0.1124`
- RMS relative exterior error: `0.0320`

### Exact finite-rank family

- max relative exterior error: `0.1184`
- RMS relative exterior error: `0.0321`

So across both exact source families:

- the shell-radial source carries the full total charge exactly
- the anisotropic shell remainder is exactly zero-monopole
- the radial shell law already captures the exterior field at the
  `10%`-level max error and `3%`-level RMS error

## Interpretation

This does **not** yet prove the final 4D closure. But it sharpens the gravity
problem substantially:

> the exact shell source is already mostly a radial shell law; the remaining
> anisotropic shell content is a zero-monopole correction

That means the remaining gravity problem is no longer “find some shell law.”
It is:

1. derive the radial shell profile from the microscopic dynamics
2. understand the zero-monopole anisotropic correction as a controlled
   subleading shell stress
3. then promote that shell law into the nonlinear spacetime closure

## What this closes

This closes another real ambiguity:

> the exact sewing shell does not look like an arbitrary angularly structured
> source; it already reduces strongly to a radial shell law across the exact
> source families on the branch

## What this still does not close

This note still does **not** close:

1. the full nonlinear 4D spacetime theorem
2. the exact continuum / stress-tensor interpretation of the shell law
3. the final Einstein/Regge closure from that shell law

## Updated gravity target

After this note, the cleanest remaining gravity target is:

- derive the radial shell profile and its effective stress meaning from the
  microscopic lattice dynamics
- then show the zero-monopole anisotropic shell correction is controlled well
  enough for the full nonlinear closure
