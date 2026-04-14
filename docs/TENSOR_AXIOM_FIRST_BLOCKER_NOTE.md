# Axiom-First Blocker for the Final Gravity Shape Law

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Status:** exact blocker note

## What is already in

The current gravity frontier already has:

- exact reduced shell amplitude law
  - `A_aniso = c_aniso * Q`
- exact local bright-channel selection
  - only `E_x` and `T1x` survive
- bounded evidence that the remaining normalized coefficients are governed by
  one projective `A1` shape ratio
  - `r = s/e0`

So the symbolic foothold is real.

## Exact blocker

The current load-bearing tensor observable is still

- `eta_floor_tf`

and that quantity is presently obtained only through the numerical Einstein
residual pipeline in
[frontier_tensorial_einstein_regge_completion.py](/private/tmp/physics-review-active/scripts/frontier_tensorial_einstein_regge_completion.py):

- interpolate `phi_grid`
- build an ADM metric numerically
- compute Christoffels / Ricci / Einstein tensor by centered differences
- sample a small probe set
- take a `max(abs(...))` traceless-spatial residual

That means the current map

- `q -> phi -> eta_floor_tf -> beta -> gamma`

is not yet an exact algebraic or operator-theoretic map on the retained
framework surface.

## Consequence

So the remaining gravity law cannot honestly be promoted as axiom-derived from
the current implementation alone.

The exact next theorem target is therefore:

- replace `eta_floor_tf` with an exact tensor boundary observable on the same
  `A1 x {E_x, T1x}` block
- then derive the projective `A1` law
  - `r -> (gamma_E(r), gamma_T(r))`

Until that exact tensor observable exists, the current line can localize the
gap sharply and organize it mechanically, but it cannot close full nonlinear GR
as a theorem.
