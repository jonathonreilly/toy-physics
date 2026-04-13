# Exact Reduced Whole-Shell Stress Law on the Static Isotropic Bridge

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_reduced_whole_shell_stress_law.py`  
**Status:** Exact reduced whole-shell stress law on the bridge surface plus bounded closure consequence

## Purpose

The previous shell-stress step solved only the outer half of the sewing band:

- `4 < r <= 5`

That was the correct DtN side of the shell, but it still left the legitimate
complaint that the reduced shell-stress lift had not yet been checked on the
inner half of the exact sewing band:

- `3 < r <= 4`

This note closes that reduced whole-shell gap on the current bridge surface.

## Exact whole-shell reduced profiles

Work on the full sewing band:

- `3 < r <= 5`

For the seven star-support point-Green columns, the script finds:

- the same whole-shell radial source profile per unit charge:
  `k(r)`
- the same whole-shell exterior-projector potential profile per unit charge:
  `u(r)`

The inner/outer split is itself exact:

- on the inner half `3 < r <= 4`, one has `u(r) = 0`
- on the outer half `4 < r <= 5`, one recovers the same DtN-side profile from
  the previous outer-shell note

So the exact sewing band now carries one reduced source/potential profile pair,
not two unrelated halves.

## Exact reduced whole-shell stress law on the bridge surface

On the static isotropic conformal bridge, use

- `psi_Q(r) = 1 + Q u(r)`
- `alpha_Q(r) = (1 - Q u(r)) / (1 + Q u(r))`

and interpret the reduced shell source through the same conformal constraint
pair:

- `-Delta psi = 2 pi psi^5 rho`
- `-Delta(alpha psi) = -2 pi alpha psi^5 (rho + 2S)`

This yields the reduced one-parameter whole-shell stress family:

- `rho_Q(r) = Q k(r) / (2 pi (1 + Q u(r))^5)`
- `S_Q(r) = 0.5 rho_Q(r) (1/alpha_Q(r) - 1)`

So on the reduced whole-shell surface, the shell-stress law is now explicit and
charge-fixed across the entire exact sewing band.

## Exact agreement with current source families

The script checks:

1. the exact local `O_h` source family
2. the broader exact finite-rank source family

and finds machine-precision agreement with the same one-parameter reduced
whole-shell stress law.

So the current exact source families are not using family-specific reduced
shell stresses on either half of the band. They realize one universal
charge-parameterized whole-shell stress family already latent in the star-
support DtN problem.

## Interpretation

This is not full nonlinear GR. It is the sharpest reduced shell-stress
statement so far:

> on the full sewing band `3 < r <= 5`, the reduced shell-stress lift of the
> exact junction operator is solved on the static isotropic bridge surface

That removes another real ambiguity from the gravity program.

## What this closes

This closes another real gap:

> the reduced shell-stress law is no longer merely heuristic across the sewing
> band; it is an exact one-parameter family on the full reduced shell surface

## What this still does not close

This note still does **not** close:

1. the full local/angular shell-stress tensor across the sewing band
2. the derivation of the static isotropic bridge itself from the lattice
3. the full nonlinear 4D spacetime theorem

## Updated gravity target

After this note, the remaining blocker tightens again:

- the reduced whole-shell stress lift is solved on the current bridge surface
- the remaining problem is the local/angular lift and the derivation of the
  static isotropic bridge from the lattice closure itself
