# Exact Sewing-Shell Source Law for the Strong-Field Exterior

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_sewing_shell_source.py`  
**Status:** Exact shell-source decomposition plus bounded sewing-band identification

## Purpose

The latest gravity work had already shown:

- the exact shell averages of the current star-supported source classes are
  fixed by total charge
- the macroscopic exterior beyond the sewing band is already vacuum-close
- the remaining blocker is the law of the sewing shell itself

This note replaces the previous bounded smooth-blend picture with an exact
lattice-native shell-source decomposition.

## Exact projector-shell identity

Fix a radius `R` that encloses the microscopic source support, and let

`Pi_R^ext phi`

denote the exact field with everything inside `r <= R` projected away.

Define the shell source

`sigma_R = H_0 (Pi_R^ext phi)`

where `H_0` is the Dirichlet lattice negative Laplacian already used
throughout the gravity program.

Then, by exact Green inversion on the same lattice box,

`Pi_R^ext phi = G_0 sigma_R`

with `G_0 = H_0^{-1}`.

So the full field admits the exact decomposition

`phi = Pi_R^in phi + G_0 sigma_R`

where:

- `Pi_R^in phi` is the exact microscopic interior field
- `sigma_R` is an exact effective source supported only on the sewing shell

This is not an ansatz and not a fitted blend. It is an exact lattice identity.

## Why the shell source is localized

If the physical source support lies strictly inside `B_R`, then the projected
exterior field is harmonic away from the discrete boundary where the projector
jumps from `0` to `1`.

Therefore `sigma_R` vanishes everywhere except on the one-lattice-thick shell
band straddling that boundary.

So the sewing shell is not merely a bounded convenience. For the projector
surface, it is an exact support law.

## Exact charge inheritance

The shell source carries the same total enclosed charge as the original field:

`sum sigma_R = sum H_0 phi = Q`

This means the exact shell source preserves the same monopole charge that was
already shown to fix the shell-averaged exterior law.

So the monopole exterior is not being re-fit at the sewing stage. It is
transmitted exactly through the shell source.

## Numerical extraction at the physically relevant sewing radius

Taking `R = 4`, which sits inside the previously identified bounded sewing
window `3 < r < 5`, the script finds:

### Exact local `O_h` family

- exact exterior reconstruction error: `4.86e-17`
- exact full decomposition error: `4.86e-17`
- `Q_total = 2.52683051`
- `Q_shell = 2.52683051`
- shell support band: `[3.162278, 5.000000]`

### Exact finite-rank family

- exact exterior reconstruction error: `1.67e-16`
- exact full decomposition error: `1.67e-16`
- `Q_total = 9.53220124`
- `Q_shell = 9.53220124`
- shell support band: `[3.162278, 5.000000]`

So for both exact source families already on the branch:

1. the exterior field is generated exactly by a shell source
2. the shell source carries the correct total charge exactly
3. the shell source is confined to the same finite band previously identified
   only by bounded sewing tests

## What this closes

This closes a real ambiguity in the gravity program:

> the sewing shell is no longer just a bounded smooth interpolation region; it
> can be represented exactly as a microscopic lattice shell source supported
> in the finite band `3 < r <= 5`

That is a real advance over the previous bounded blend construction.

## What this still does not close

This note still does **not** close:

1. the full nonlinear 4D spacetime theorem
2. the continuum / effective-stress interpretation of `sigma_R`
3. the final derivation of the nonlinear exterior field equation from the same
   shell-source law

## Updated gravity target

After this note, the remaining gravity gap is sharper again:

- the sewing shell itself is now represented exactly on the lattice
- the remaining problem is to interpret that exact shell source as the correct
  coarse-grained stress / matching law for the 4D spacetime closure

That is a much narrower target than “find the sewing shell.”
