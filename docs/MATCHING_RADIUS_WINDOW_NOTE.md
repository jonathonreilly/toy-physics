# Finite Matching-Radius Window for Strong-Field Exterior Coarse-Graining

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_matching_radius_window.py`  
**Status:** Bounded positive result; not a matching theorem

## Purpose

The previous coarse-grained exterior-law result showed that once the exact
lattice exterior field is projected onto the unique radial harmonic law
`phi_eff = a/r`, the resulting exterior metric is already vacuum-close.

That still left one question:

> is there an actual finite matching window where this coarse-grained
> replacement becomes justified, or is the good behavior only a diffuse
> large-radius asymptotic effect?

This note answers that in the strongest bounded form currently available.

## Test

For each exact source family:

1. take the exact lattice field
2. fit the radial harmonic projection `a/r` outside a trial matching radius
   `R_match`
3. compare the direct same-source 4D residual to the coarse-grained projected
   4D residual at that same radius

The test is applied to:

1. the exact local `O_h` source family
2. the broader exact finite-rank source family

## What the script finds

### Exact local `O_h` family

First matching window satisfying:

- coarse residual `< 1e-5`
- improvement factor `> 100`

appears at:

`R_match = 4.0`

with:

- direct residual: `8.59e-3`
- coarse residual: `9.04e-6`
- improvement: `~9.50e2`

### Exact finite-rank family

First matching window satisfying:

- coarse residual `< 2e-5`
- improvement factor `> 100`

appears at:

`R_match = 4.5`

with:

- direct residual: `2.79e-2`
- coarse residual: `1.19e-5`
- improvement: `~2.35e3`

## Interpretation

This is stronger than a mere asymptotic statement.

Across two different exact source families, a finite matching window emerges in
the same narrow radial band:

`R_match ~ 4.0 - 4.5`

So the gravity problem is now even more sharply localized:

- the coarse-grained exterior law is already working
- and it starts working at a finite, source-family-stable matching radius

That means the remaining gravity target is no longer “guess the right
macroscopic law.” It is:

> derive why the exact lattice field crosses over to that radial harmonic
> exterior representation in this finite matching band

## What this closes

This closes another ambiguity:

> the coarse-grained exterior law is not only asymptotically good; it becomes
> effective in a finite and fairly stable matching window across different
> exact source families

## What this does not close

This note still does **not** close:

1. the theorem-grade matching rule itself
2. the near-source strong-field metric
3. full nonlinear GR

## Practical next step

The next Codex gravity move should therefore be:

1. derive the coarse-graining / matching mechanism that explains the emergence
   of the `R_match ~ 4 - 4.5` window
2. relate that window to the exact lattice source data rather than fitting it
   numerically
