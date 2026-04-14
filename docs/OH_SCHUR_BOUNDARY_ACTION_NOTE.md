# Exact Schur-Complement Boundary Action for the `O_h` Strong-Field Shell Law

**Date:** 2026-04-13  
**Script:** `scripts/frontier_oh_schur_boundary_action.py`  
**Status:** Exact microscopic shell-boundary action on current strong-field source classes

## Purpose

The gravity line already had:

- an exact sewing shell
- an exact DtN shell kernel
- an exact reduced shell action on the orbit quotient
- an exact local static-constraint lift on the current bridge surface

What still remained open was whether that shell action really came from the
microscopic lattice dynamics, or was only a reduced packaging of the solved
boundary map.

This note closes that specific microscopic gap on the current source classes.

## Exact Schur boundary action

Fix the exterior domain `Omega_R` with inner trace `Gamma_R` at `R = 4`.

Split the lattice negative Laplacian into trace and harmonic-bulk blocks.
Eliminating the harmonic bulk by exact Schur complement gives the boundary
operator

- `Lambda_R = H_tt - H_tb H_bb^{-1} H_bt`.

This is the exact lattice Dirichlet-to-Neumann matrix on `Gamma_R`.

For a trace field `f` with harmonic extension `u_f` on `Omega_R`, the exterior
Dirichlet energy is therefore the exact quadratic boundary functional

- `E_R(f) = 1/2 f^T Lambda_R f`.

Its gradient is the exact trace flux:

- `grad E_R(f) = Lambda_R f = (H_0 u_f)|_(Gamma_R)`.

So the shell-boundary action is no longer inserted by hand. It is the exact
Schur-complement energy of the microscopic lattice Laplacian.

## Exact sourced stationarity on current source classes

For the exact local `O_h` and broader finite-rank source classes, let `f` be
the exact shell trace of the exterior projector field `phi_ext`.

Using the microscopic trace flux of that same field as the source term

- `j = (H_0 phi_ext)|_(Gamma_R)`,

the sourced boundary action

- `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`

has Euler-Lagrange equation

- `Lambda_R f - j = 0`.

The script finds that:

- the exact harmonic extension reconstructed from `f` matches `phi_ext` to
  machine precision
- the Schur boundary gradient matches the microscopic trace flux to machine
  precision
- the exact local `O_h` and broader finite-rank shell traces are stationary
  points of the same microscopic sourced boundary action

So the current strong-field shell law is no longer only a reduced junction map.
It is the stationary point of an exact microscopic lattice boundary energy.

## Interpretation

This is the cleanest discrete Regge-style statement currently available on the
branch:

- finitely many shell trace variables on the sewing boundary
- one exact microscopic quadratic boundary energy from the lattice Laplacian
- sourced stationarity reproducing the shell trace law

Combined with the already-derived local static-constraint lift, this is a real
restricted strong-field closure theorem on the current bridge surface.

## What this closes

This closes the microscopic shell-action gap:

> on the current strong-field source classes, the shell boundary law is derived
> from the Schur-complement boundary energy of the lattice dynamics itself

That is stronger than the earlier reduced quadratic shell action, because the
action is no longer inserted on the reduced surface.

## What this still does not close

This note still does **not** close:

1. a fully general Einstein/Regge theorem beyond the current static conformal
   bridge
2. fully general non-`O_h` strong-field closure
3. fully general nonlinear GR

## Updated gravity target

After this note, the remaining gravity problem is narrower again:

- the microscopic shell-boundary action is no longer open on the current
  source classes
- the live blocker is the final extension from this exact boundary-action-plus-
  bridge closure to a broader pointwise Einstein/Regge theorem beyond the
  current bridge surface
