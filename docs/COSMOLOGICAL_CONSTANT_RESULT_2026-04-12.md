# Cosmological Constant — Spectral-Gap Companion

**Date:** 2026-04-12  
**Status:** bounded/conditional cosmology companion. Canonical positive
`Lambda` surface on `main`.

**Current publication disposition:** bounded/conditional cosmology companion
only. Not on the retained flagship claim surface.

## Safe Theorem Surface

On the retained `S^3` topology surface, the lowest scalar Laplacian eigenvalue
is

`lambda_1(S^3_R) = 3 / R^2`.

If the cosmological radius is identified with a Hubble-scale radius
`R = c / H_0`, the framework gives the bounded/conditional companion value

`Lambda_pred = 3 H_0^2 / c^2 = 1.59 x 10^-52 m^-2`.

Against the current observational comparator

`Lambda_obs = 1.11 x 10^-52 m^-2`,

the ratio is `Lambda_pred / Lambda_obs ~ 1.44`, i.e. an `O(1)` match rather
than the usual UV-vacuum `10^122` catastrophe.

## What Is Exact vs Conditional

### Exact on the retained internal surface

1. The coefficient `3` is the exact `d = 3` first-eigenvalue coefficient on
   `S^3`.
2. The spectral-gap identification is IR/geometric:
   `Lambda = lambda_1(S^3_R) = 3 / R^2`.
3. The same spectral-gap mechanism is the one used by the bounded dark-energy
   EOS companion:
   [DARK_ENERGY_EOS_NOTE.md](./DARK_ENERGY_EOS_NOTE.md).

### Still conditional

1. The cosmological radius identification is not yet derived on the same
   theorem surface. The current companion uses the observed Hubble scale:
   `R = c / H_0`, or equivalently a nearby formation-scale version.
2. The remaining `O(1)` factor is the same matter-fraction issue that appears
   in the bounded `Omega_Lambda` chain:
   [OMEGA_LAMBDA_DERIVATION_NOTE.md](./OMEGA_LAMBDA_DERIVATION_NOTE.md).
3. This is not yet a full FRW / expansion-history derivation.

## What This Is Not

This is **not** the claim that finite lattice vacuum-energy sums automatically
solve the cosmological-constant problem.

That broader vacuum-energy audit is recorded separately in
[COSMOLOGICAL_CONSTANT_VACUUM_ENERGY_AUDIT_NOTE.md](./COSMOLOGICAL_CONSTANT_VACUUM_ENERGY_AUDIT_NOTE.md)
with
[frontier_cosmological_constant.py](../scripts/frontier_cosmological_constant.py).

That audit is useful because it rules out the wrong mechanism. The controlling
positive companion surface is the `S^3` spectral-gap route.

## Interpretation

The framework changes the object being identified as `Lambda`:

| Standard UV picture | Current companion route |
|---|---|
| vacuum-energy sum | spectral gap of the retained spatial graph/topology |
| UV-cutoff dominated | IR/geometric scale dominated |
| misses by `10^122` | lands at an `O(1)` ratio |

The clean current claim is therefore:

> on the retained `S^3` surface, the framework supplies a bounded/conditional
> IR-geometric cosmological-constant companion with exact coefficient `3`
> and Hubble-scale value `3 H_0^2 / c^2`.

## Relationship To Other Cosmology Companions

- [DARK_ENERGY_EOS_NOTE.md](./DARK_ENERGY_EOS_NOTE.md):
  fixed spectral gap implies `w = -1` exactly on the same conditional route
- [OMEGA_LAMBDA_DERIVATION_NOTE.md](./OMEGA_LAMBDA_DERIVATION_NOTE.md):
  matter fraction and flatness convert the same mechanism into the bounded
  `Omega_Lambda` chain
- [GRAVITON_MASS_DERIVED_NOTE.md](./GRAVITON_MASS_DERIVED_NOTE.md):
  the graviton-mass companion reuses the same `1/R^2` spectral/topological
  structure

## Falsifiability

The clean failure modes are:

- if dark energy is not a cosmological constant (`w != -1`) on the final
  cosmology surface, the fixed spectral-gap identification fails
- if the relevant cosmological radius is shown not to be Hubble/formation
  scale on the same route, this companion must be revised

## Canonical Validation

- [frontier_cosmological_constant_spectral_gap.py](../scripts/frontier_cosmological_constant_spectral_gap.py)
- [frontier_dark_energy_eos.py](../scripts/frontier_dark_energy_eos.py)
- [frontier_omega_lambda_derivation.py](../scripts/frontier_omega_lambda_derivation.py)
