# Cosmology Scale Identification and Reduction

**Date:** 2026-04-15
**Status:** bounded/conditional cosmology-lane synthesis on `main`
**Primary runner:** [`scripts/frontier_cosmology_scale_identification.py`](../scripts/frontier_cosmology_scale_identification.py) (PASS=7/0)

## Verdict

The cosmology lane is tighter than the older companion notes made it look.

On the current post-closure gravity/QG stack:

1. the cosmological-constant companion and the `w = -1` companion now sit on
   the same fixed-gap vacuum surface;
2. the natural scale is the de Sitter curvature radius
   `R_Lambda = sqrt(3/Lambda) = c/H_inf`, not the present-day Hubble radius
   `c/H_0`;
3. therefore the remaining remaining blocker for promoting the cosmology package is
   not a second independent `Lambda` or `w` theorem, but the matter-content
   bridge behind present-day `Omega_Lambda`.

So the active cosmology lane is now:

> fixed-gap vacuum scale closed up to cosmological scale identification;
> present-day vacuum fraction reduced to matter-content closure.

## Exact Content

### 1. Fixed-gap vacuum scale

The retained topology route already gives

`lambda_1(S^3_R) = 3/R^2`.

The direct-universal gravity/QG route already closes one canonical textbook
continuum gravitational weak/stationary action family on the chosen smooth
realization of `PL S^3 x R`. On the de Sitter vacuum sector of that same
surface, the curvature radius `R_Lambda` and asymptotic de Sitter Hubble scale
`H_inf` satisfy

`H_inf = c / R_Lambda`,

so the vacuum relation is exactly

`Lambda = 3 / R_Lambda^2 = 3 H_inf^2 / c^2`.

This is the right same-surface scale identification for the cosmological
constant companion.

### 2. `w = -1` is the same mechanism

Once the fixed spectral-gap radius is constant,

`rho_Lambda = Lambda c^2 / (8 pi G)`

is constant as well. Therefore

`d ln rho_Lambda / d ln a = 0`,

and the dark-energy equation of state is

`w = -1`

exactly.

So `w = -1` is no longer a separate cosmology blocker. It is the EOS face of
the same fixed-gap vacuum-scale theorem.

### 3. Present-day `Omega_Lambda` reduces to matter content

Using the present critical density

`rho_crit = 3 H_0^2 / (8 pi G)`,

the vacuum fraction is exactly

`Omega_Lambda = rho_Lambda / rho_crit = Lambda c^2 / (3 H_0^2)`.

Substituting the fixed-gap/de-Sitter relation gives

`Omega_Lambda = H_inf^2 / H_0^2 = (R_H(now) / R_Lambda)^2`,

with `R_H(now) = c/H_0`.

So the `O(1)` difference between `R_Lambda` and `c/H_0` is not a second
cosmological-constant discrepancy. It is just the present-day matter fraction.

Under flatness,

`Omega_Lambda = 1 - Omega_m - Omega_r`.

Therefore the remaining promotion blocker for the cosmology package is the
matter-content bridge, i.e. closure of the `Omega_m` side of the story. On the
current package surface that is exactly the still-open DM relic mapping lane.

## What This Changes

Before this note, the cosmology companion portfolio looked like three loosely
related bounded items:

- `Lambda`
- `w = -1`
- `Omega_Lambda`

After this note, the clean interpretation is:

- `Lambda`: fixed-gap vacuum scale
- `w = -1`: same fixed-gap scale viewed as EOS
- `Omega_Lambda`: present-vs-asymptotic vacuum fraction, hence a matter-bridge
  question

That is a better active lane because it removes fake multiplicity in the
blockers.

## Honest Remaining Gap

What is **not** yet closed on the same surface:

1. a first-principles derivation of the cosmological scale matching that picks
   out the vacuum/de-Sitter scale without using observed `H_0`, and
2. the matter-content bridge that fixes `Omega_m` internally enough to promote
   `Omega_Lambda`.

In practical package terms, the second item is the main remaining gate,
because the current bounded DM/baryon chain already lands close to the needed
matter fraction.

## Canonical Validation

- [frontier_cosmology_scale_identification.py](../scripts/frontier_cosmology_scale_identification.py)
- [frontier_cosmological_constant_spectral_gap.py](../scripts/frontier_cosmological_constant_spectral_gap.py)
- [frontier_dark_energy_eos.py](../scripts/frontier_dark_energy_eos.py)
- [frontier_omega_lambda_derivation.py](../scripts/frontier_omega_lambda_derivation.py)
