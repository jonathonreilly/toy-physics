# Orbit-Resolved Whole-Shell Stress Law on the Static Isotropic Bridge

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_orbit_mean_shell_stress_law.py`  
**Status:** Exact orbit-mean whole-shell law plus bounded within-orbit consequence

## Purpose

The reduced whole-shell note solved the shell-stress lift only after averaging
over each radius shell.

That still left one legitimate concern:

> perhaps the unresolved gravity content is really a large uncontrolled angular
> sector inside the sewing band, even if the shell means are solved

This note checks the next sharper surface: cubic orbit means across the full
sewing band `3 < r <= 5`.

## Exact orbit-mean universality

Partition the sewing band by cubic orbit type

- `(2,2,2)`, `(3,1,0)`, ..., `(5,0,0)`

and compute for each orbit:

- the orbit-mean exterior-projector potential per unit charge
- the orbit-mean shell-source profile per unit charge

The script finds machine-precision agreement between:

1. the exact local `O_h` source family
2. the broader exact finite-rank source family

So the whole-shell law is not merely shell-radial. It is already universal at
orbit resolution.

## Exact pointwise orbit law for the local `O_h` family

For the exact local `O_h` family, the orbit spreads vanish to machine
precision. So on that exact source class the orbit-mean law is already the
pointwise whole-shell law.

That is stronger than the previous reduced-shell statement.

## Bounded within-orbit correction for the finite-rank family

For the broader exact finite-rank source family, the remaining within-orbit
variation is small rather than arbitrary:

- `u` spread stays below about `1.4%`
- `k` spread stays below about `1.7%`
- the induced bridge-side `rho` spread stays below about `1.4%`
- the induced bridge-side `S` spread stays below about `2.7%`

So the residual angular freedom is no longer a large shell tensor ambiguity.
It is a bounded within-orbit correction on top of an exact orbit-mean law.

## Bounded bridge consequence

Using the universal orbit-mean profiles from the exact local `O_h` family and
inserting the finite-rank total charge `Q`, the static isotropic bridge already
predicts the finite-rank orbit-mean stress law with tiny absolute error:

- orbit-mean `rho` error below `2e-7`
- orbit-mean `S` error below `3e-8`

So even on the broader non-`O_h` exact source family, the bridge-side whole-
shell stress law is already very close to being fixed at orbit resolution.

## What this closes

This closes another real ambiguity:

> the remaining gravity gap is no longer a generic local/angular shell freedom
> across the sewing band; at orbit resolution the whole-shell law is exact, and
> the broader finite-rank family deviates only by a small within-orbit
> correction

## What this still does not close

This note still does **not** close:

1. the derivation of the static isotropic bridge itself from the lattice
2. the full pointwise local/angular shell-stress law for the broader exact
   finite-rank family
3. the full nonlinear 4D spacetime theorem

## Updated gravity target

After this note, the remaining blocker tightens again:

- the reduced whole-shell stress lift is solved exactly
- the orbit-mean whole-shell law is solved exactly
- the only remaining angular freedom on the broader exact source family is a
  small within-orbit correction
- the main unsolved step is now the derivation of the static isotropic bridge
  itself, followed by the final pointwise 4D lift
