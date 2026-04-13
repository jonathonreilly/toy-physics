# Localized Sewing Band for the Strong-Field Exterior

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_localized_sewing_band.py`  
**Status:** Bounded sewing result; not full nonlinear GR

## Purpose

The previous gravity work had established:

- the exact shell-level coarse-graining of the current star-supported source
  classes is fixed by total charge
- the resulting radial harmonic exterior law is already vacuum-close
- the remaining blocker is the sewing step from the microscopic interior field
  to that macroscopic exterior metric

This note gives the first honest bounded sewing result on the Codex branch.

## Sewing construction

Use:

1. the exact microscopic field inside a finite radius `r <= R_in`
2. the charge-fixed radial harmonic exterior metric outside `r >= R_out`
3. a smooth blend of the metric variables

   - `psi`
   - `alpha psi`

   across the finite band `R_in < r < R_out`

The blend is not claimed as a derived law. It is a bounded test of whether the
remaining nonvacuum content can be confined to a finite matching shell rather
than leaking into the macroscopic exterior.

## Shared finite sewing band

The strongest shared band found so far across both exact source families is:

`R_in = 3.0`, `R_out = 5.0`

This is wider than the earlier `R_match ~ 4.0 - 4.5` vacuum window because the
band now includes the transition shell itself rather than only the exterior
region beyond it.

## What the script finds

### Exact local `O_h` family

- transition-band residual: `3.69e-2`
- exterior residual beyond `r > 5`: `1.12e-6`

### Exact finite-rank family

- transition-band residual: `1.03e-1`
- exterior residual beyond `r > 5`: `3.19e-6`

So in both exact source families:

- the nonvacuum part is strongly localized to the finite sewing shell
- the exterior beyond that shell is already vacuum-close

## Interpretation

This does not derive the final nonlinear field equation. It does remove another
major ambiguity:

> the remaining strong-field mismatch does not need to be spread throughout the
> macroscopic exterior

At the current Codex state, it can be confined to a finite matching shell.

That sharply narrows what is still missing:

1. derive the physical law of the sewing shell / coarse-grained source band
2. show that this band emerges from the microscopic lattice dynamics rather
   than from a chosen smooth blend
3. then promote the resulting exterior-plus-band construction to a theorem-
   grade nonlinear spacetime closure

## What this closes

This closes the following bounded question:

> after the exact shell projector is imposed, can the remaining nonvacuum
> content be localized to a finite matching shell while keeping the exterior
> vacuum-close?

The answer is yes, for the current exact source families.

## What this does not close

This note still does **not** close:

1. the full nonlinear GR theorem
2. the derivation of the sewing-band law from the exact microscopic dynamics
3. no-horizon / no-echo consequences

## Updated gravity target

The remaining gravity problem is now even sharper:

- the exterior law is not the blocker
- shell-level coarse-graining is not the blocker
- the live blocker is the derivation of the finite sewing-band dynamics that
  replaces the current bounded blending rule

That is the right next target if gravity is to be pushed to full closure.
