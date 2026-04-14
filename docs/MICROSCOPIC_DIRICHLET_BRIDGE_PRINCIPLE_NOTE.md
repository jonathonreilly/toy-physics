# Microscopic Dirichlet Principle for the Bridge

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_microscopic_dirichlet_bridge_principle.py`  
**Status:** Exact global-minimizer theorem on the current star-supported strong-field class

## Purpose

The bridge-side strong-field chain already has:

- an exact shell source
- an exact Schur-complement boundary action
- an exact same-charge bridge
- an exact local static-constraint lift

What still remained open was the conceptual question:

> Is the current bridge only a convenient harmonic packaging, or is it the
> unique minimum of the microscopic boundary energy itself?

This note answers that on the current star-supported finite-rank class.

## Exact Dirichlet principle

Let `Gamma_R` be the shell trace at `R = 4`, and let

- `Lambda_R = H_tt - H_tb H_bb^{-1} H_bt`

be the exact Schur-complement Dirichlet-to-Neumann matrix of the exterior
microscopic lattice Laplacian.

For any trace field `f` on `Gamma_R` with microscopic flux source `j`, the
exact sourced boundary action is

- `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`.

If `f_*` denotes the exact shell trace of the exterior projector field
`phi_ext`, then `j = Lambda_R f_*` on the current source classes. Completing
the square gives the exact identity

- `I_R(f ; j) = I_R(f_* ; j) + 1/2 (f - f_*)^T Lambda_R (f - f_*)`.

Because `Lambda_R` is symmetric positive definite on the current bridge
surface, the quadratic remainder is nonnegative and vanishes only when
`f = f_*`. Therefore:

- `f_*` is the unique global minimizer of the exact microscopic boundary
  energy.

Since the harmonic bulk extension is unique for each trace, the exact bridge is
therefore the unique minimum-energy discrete Dirichlet extension of the shell
data on the current star-supported class.

## Why this is stronger than the static conformal ansatz

The static conformal bridge says:

- if the exterior is static isotropic vacuum, then `psi = 1 + phi_ext` and
  `chi = 1 - phi_ext`

The Dirichlet principle says something stronger:

- the same bridge is not merely compatible with the exact exterior shell law;
  it is the unique global minimizer of the exact microscopic boundary energy.

So the bridge is now forced by a variational/geometric principle on the
current source class, not just by the static isotropic vacuum target.

## Exact bridge statement

On the current star-supported finite-rank class:

- the exact shell trace `f_*` equals the unique minimizer of `I_R`
- the corresponding harmonic extension is the exact native same-charge bridge
  `psi = 1 + phi_ext`, `chi = 1 - phi_ext = alpha psi`
- any trace deformation `f_* + delta` increases the boundary action by
  `1/2 delta^T Lambda_R delta`

That is the discrete Dirichlet principle for the bridge.

## What the script checks

The companion script verifies, on exact local `O_h` and broader finite-rank
source classes:

1. the minimizer reconstructed from `Lambda_R^{-1} j` matches the exact shell
   trace to machine precision
2. the quadratic completion identity holds to machine precision
3. sampled random perturbations always raise the exact microscopic boundary
   action
4. the same result holds for both the exact local `O_h` family and the broader
   finite-rank family on the current bridge surface

## What this closes

This closes the remaining “ansatz vs principle” ambiguity on the current bridge
surface:

> the native same-charge bridge is the unique minimum-energy discrete Dirichlet
> extension of the exact shell data on the current star-supported strong-field
> class.

That is a genuine microscopic variational/geometric principle, stronger than
the static conformal ansatz alone.

## What this still does not close

This note still does **not** close:

1. a full pointwise Einstein/Regge theorem beyond the current bridge surface
2. broader support classes beyond the current star-supported finite-rank
   sector
3. fully general nonlinear GR

## Updated gravity target

After this note, the remaining gravity gap is narrower again:

- the bridge is no longer an ansatz on the current class
- the live blocker is now the extension beyond the current bridge surface and
  support class, not the local variational justification of the bridge itself
