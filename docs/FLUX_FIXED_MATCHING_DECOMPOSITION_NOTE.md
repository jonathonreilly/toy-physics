# Flux-Fixed Matching Decomposition for the Strong-Field Exterior

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_flux_fixed_matching_theorem.py`  
**Status:** Exact decomposition theorem plus bounded shell-level matching result

## Purpose

The previous Codex gravity work had isolated the live blocker very sharply:

- the coarse-grained radial harmonic exterior law already works
- it becomes vacuum-close in a finite matching band around `R_match ~ 4.0-4.5`
- what remained missing was a theorem explaining why the exact microscopic
  lattice field should collapse onto that macroscopic exterior law

This note extracts the cleanest exact lattice statement now available.

## Exact decomposition

Let `phi` be an exact lattice field produced by a finite enclosed source on the
physical cubic lattice with Dirichlet boundary conditions on the finite box.

Define the enclosed discrete charge

`Q = sum_{cube(R)} (-Delta phi)`

for any cube radius `R` enclosing the source support.

Let `G_0` be the unit point-source lattice Green function on the same box.
Then the exact flux-fixed monopole representative is

`phi_mono = Q * G_0`.

The key exact identity is then:

`h = phi - phi_mono`

with:

1. `h` harmonic outside the joint source support
2. `h` carrying zero enclosed monopole charge on every enclosing cube

So the exterior field splits exactly into:

- a unique monopole piece fixed by conserved discrete charge
- a zero-monopole harmonic remainder

This is the lattice-native replacement for the earlier ad hoc `a/r` fit.

## What the script proves exactly

For both exact source families already constructed on `codex/review-active`:

1. the enclosed discrete charge is radius-independent for `R = 2,3,4,5`
2. the flux-fixed point-Green representative carries that same charge
3. the remainder `h = phi - Q G_0` carries zero enclosed charge

The tested families are:

1. the exact local `O_h` source family
2. the broader exact finite-rank source family

So this is not a single special-source artifact.

## What the script finds

### Exact local `O_h` source family

- enclosed charge:

  `Q = 2.52683051`

- the remainder charge is zero to machine precision
- the flux-fixed point-Green representative matches the lattice shell data
  exactly outside the source support:

  `max relative shell error ~ 1e-15` for `R_match >= 3`

So for the exact local cubic source family, the exterior shell data are already
pure monopole data once the charge is fixed.

### Exact finite-rank source family

- enclosed charge:

  `Q = 9.53220124`

- the remainder charge is again zero to machine precision
- the flux-fixed point-Green representative captures the exterior shell data at
  the percent level:

  - `max shell error = 1.19%` at `R_match = 3.0`
  - `max shell error = 0.65%` by `R_match = 4.5`

So for the broader exact finite-rank family, the monopole piece is already the
dominant shell-level exterior object very near the source.

## Interpretation

This closes an important part of the matching problem.

The exact microscopic lattice field is not transitioning to the macroscopic
exterior law in a vague or fitted way. It already admits the exact lattice
decomposition:

`exact field = charge-fixed monopole Green field + zero-monopole harmonic remainder`

Combined with the earlier cubic-multipole result:

- the remainder is not a hidden monopole
- for cubic-symmetric sources its leading surviving sector is the cubic `l=4`
  anisotropy

So the matching problem is now reduced to:

1. why that zero-monopole remainder is negligible after shell / angular
   coarse-graining in the macroscopic exterior
2. how the near-source region is sewn to the monopole-dominated exterior metric

That is much narrower than “derive all of GR.”

## What this closes

This closes the following real ambiguity:

> the macroscopic exterior law is not merely a fitted `a/r` ansatz; it is the
> lattice monopole Green representative fixed exactly by conserved discrete
> charge

That is an exact matching decomposition statement.

## What this does not close

This note still does **not** close:

1. the full nonlinear 4D spacetime theorem
2. the near-source sewing of the exact field to the vacuum metric
3. full Einstein-equation / Regge closure

## Practical next step

The next Codex gravity move should now be:

1. derive the shell / angular coarse-graining map that kills the zero-monopole
   remainder in the macroscopic exterior
2. use that to build the near-source-to-exterior sewing rule for the 4D metric
