# Cubic-Symmetry Monopole Reduction for the Strong-Field Exterior

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_cubic_monopole_reduction.py`  
**Status:** Exact `O_h` symmetry theorem for the finite-rank source class plus bounded asymptotic monopole reduction

## Purpose

The previous strong-field work established:

- exact source closure for rank-one, diagonal finite-support, and finite-rank
  support operators
- a bounded 4D residual result showing that the direct common-source metric
  candidate is not yet vacuum-closed, while its isotropic monopole projection
  is nearly vacuum

That left one sharp question:

> why is the isotropic projection the right thing to do at all?

This note answers the best version of that question currently available on the
Codex branch:

> for the exact cubic-symmetric finite-rank source class, the exterior field is
> exactly `O_h`-invariant and its first anisotropic exterior correction is the
> unique cubic `l=4` mode, so the isotropic reduction is asymptotically
> justified rather than ad hoc.

This does **not** yet close full nonlinear GR. It removes a major ambiguity in
the asymptotic strong-field exterior.

## Exact theorem: cubic symmetry is inherited by the renormalized source and field

Take the finite-rank source class

`H_W = H_0 - P W P^T`

with:

- `H_0 = -Delta_lat`
- support `S = {0, ±e_x, ±e_y, ±e_z}`
- support operator `W` invariant under the full cubic group `O_h`
- bare source vector `m` invariant under the same group

Then:

1. `W` commutes with the induced support permutation representation of `O_h`
2. `m` is fixed by that representation
3. the exact renormalized source

   `q_eff = (I - W G_S)^-1 m`

   is also `O_h`-invariant
4. the exact exterior field

   `phi = G_0 P q_eff`

   is `O_h`-invariant on the lattice

The script verifies all four facts exactly:

- `48/48` cubic symmetries preserve `W`
- `q_eff` is symmetric at machine precision
- sampled exterior field values satisfy `phi(gx) = phi(x)` at machine precision

So asymptotic isotropy is not being inserted by hand for this source class.
It is already encoded in the exact exterior field through cubic symmetry.

## Bounded asymptotic theorem: first anisotropic term is the cubic `l=4` mode

For an `O_h`-invariant exterior harmonic field, the continuum angular
decomposition is not arbitrary:

- dipole (`l=1`) is forbidden
- quadrupole (`l=2`) is forbidden
- octupole (`l=3`) is forbidden
- the first non-monopole `O_h`-invariant harmonic is the unique cubic `l=4`
  mode

The corresponding angular basis is

`Y_4^{cubic} ~ n_x^4 + n_y^4 + n_z^4 - 3/5`

or equivalently, in homogeneous form,

`H_4(x,y,z) = x^4 + y^4 + z^4 - 3 r^4 / 5`.

So the exterior field should have the asymptotic structure

`phi(r, n) = a/r + b/r^3 + c * Y_4^{cubic}(n) / r^5 + ...`

where the anisotropic correction is suppressed by `r^-4` relative to the
monopole term.

## What the script finds

Using the exact `O_h`-symmetric finite-rank source class:

1. the angular residual on spheres of radius `r = 3,4,5,6` is captured by the
   unique cubic harmonic with correlations

   - `0.963`
   - `0.975`
   - `0.993`
   - `0.950`

2. the relative anisotropy `std(phi) / mean(phi)` on those spheres decays with
   log-log slope

   `-3.382`

   which is consistent with the expected quartic suppression of the first
   anisotropic correction

3. by radius `r = 6`, the relative exterior anisotropy is already only

   `0.163%`

This is exactly the kind of result the strong-field branch needed:

- not a blanket claim that the field is perfectly isotropic everywhere
- but a controlled asymptotic statement that the exterior is monopole-dominated
  and that the first anisotropic correction is the expected cubic harmonic

## What this buys us

This note does not close gravity, but it changes the closure problem:

Before:

- the isotropic projection looked like a plausible but ad hoc move

After:

- for the exact cubic-symmetric finite-rank source class, the isotropic
  reduction is now asymptotically justified
- the remaining gravity gap is no longer “why isotropy at all?”
- it is now:

> why the physical strong-field source lands in, or flows to, the cubic
> symmetric source class strongly enough that the asymptotic isotropic-vacuum
> sector controls the exterior geometry relevant for the metric closure

That is a much narrower target.

## What this does not close

This note still does **not** close:

1. the actual physical many-body source law
2. the near-source matching problem
3. the full nonlinear 4D field equation
4. no-horizon / no-echo claims

## Updated gravity interpretation

Current honest state on `codex/review-active` is now:

- exact:
  - rank-one strong-field resolvent closure
  - finite-support diagonal-source closure
  - finite-rank support-operator closure
  - `O_h` symmetry inheritance for the cubic source class
- bounded:
  - common-source `g_tt` / `g_ij` candidate
  - asymptotic monopole reduction with leading cubic `l=4` correction
- still open:
  - theorem-grade strong-field metric / full nonlinear GR closure

That is real progress. The exterior geometry problem is now asymptotically much
less ambiguous than it was before this note.
