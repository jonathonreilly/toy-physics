# Exact Reduced Outer-Shell Stress Law on the Static Isotropic Bridge

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_reduced_outer_shell_stress_law.py`  
**Status:** Exact reduced shell-stress law on the bridge surface plus bounded closure consequence

## Purpose

The gravity line had already solved the reduced sewing law:

- exact radial DtN shell kernel
- exact reduced anisotropic DtN mode
- exact charge-fixed amplitude for that mode
- exact rank-one reduced junction operator

That still left the legitimate complaint that none of this yet looked like a
stress law in the 4D static isotropic system. This note gives the first exact
lift of the reduced junction law into that bridge.

## Outer-shell reduced data

Work on the outer half of the sewing band:

`4 < r <= 5`

This is the side of the shell where the DtN exterior trace already lives.

For the seven star-support point-Green columns, the script finds:

- the same outer-shell radial source profile per unit charge:
  `k(r)`
- the same outer-shell exterior potential profile per unit charge:
  `u(r)`

Both are exact consequences of the current reduced junction program.

## Exact reduced shell-stress law on the bridge surface

On the static isotropic conformal bridge, use

- `psi_Q(r) = 1 + Q u(r)`
- `alpha_Q(r) = (1 - Q u(r)) / (1 + Q u(r))`

and interpret the outer-shell source through the standard conformal constraint
pair:

- `-Delta psi = 2 pi psi^5 rho`
- `-Delta(alpha psi) = -2 pi alpha psi^5 (rho + 2S)`

This yields the reduced one-parameter outer-shell stress family:

- `rho_Q(r) = Q k(r) / (2 pi (1 + Q u(r))^5)`
- `S_Q(r) = 0.5 rho_Q(r) (1/alpha_Q(r) - 1)`

So on the reduced outer-shell surface, the shell-stress law is now explicit and
charge-fixed.

## Exact agreement with current source families

The script checks:

1. the exact local `O_h` source family
2. the broader exact finite-rank source family

and finds machine-precision agreement with this same one-parameter reduced
outer-shell stress law.

So the current exact source families are not using family-specific stress
profiles on the bridge surface. They realize the same charge-parameterized
reduced shell-stress family already latent in the star-support DtN problem.

## Interpretation

This is not full nonlinear GR. It is the sharpest shell-stress statement so
far:

> on the outer half of the sewing band, the reduced shell-stress lift of the
> exact junction operator is solved on the static isotropic bridge surface

That removes another real ambiguity from the gravity program.

## What this closes

This closes another real gap:

> the reduced shell-stress law is no longer merely heuristic on the outer DtN
> trace side of the sewing band; it is an exact one-parameter family under the
> static isotropic conformal bridge

## What this still does not close

This note still does **not** close:

1. the full local shell-stress tensor across the whole sewing band
2. the derivation of the static isotropic bridge itself from the lattice
3. the full nonlinear 4D spacetime theorem

## Updated gravity target

After this note, the remaining blocker tightens again:

- the reduced shell-stress lift is solved on the outer DtN side of the sewing
  band
- the remaining problem is the full local lift across the whole shell and the
  derivation of the static isotropic bridge from the lattice closure itself
