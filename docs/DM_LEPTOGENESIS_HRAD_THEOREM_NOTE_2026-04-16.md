# DM Leptogenesis Exact `H_rad(T)` Theorem

**Date:** 2026-04-16  
**Script:** `scripts/frontier_dm_leptogenesis_hrad_theorem.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`.

## Result

The radiation-era expansion law is now closed on the refreshed DM branch.

The exact chain is:

1. the axiom geometry `Z^3` is intrinsically flat
2. the homogeneous/isotropic spatial slice therefore has exact `k = 0`
3. the already-retained Poisson / Newton chain gives the flat first
   Friedmann law
4. the exact radiation density gives

   `rho_rad(T) = (pi^2/30) g_* T^4`

5. therefore

   `H_rad(T) = sqrt(4*pi^3*g_*/45) * T^2 / M_Pl`

with exact normalized transport profile

`E_H(z) = z^2 H(M1/z)/H(M1) = 1`.

## Why `k = 0` is no longer bounded

The old bounded lane treated `k = 0` as an external flatness assumption.
That is no longer necessary on the DM transport lane itself.

On the cubic spatial tessellation of `Z^3`, each edge has four incident
square plaquettes with dihedral angle `pi/2`, so the Regge deficit is

`delta_e = 2*pi - 4*(pi/2) = 0`.

Hence the coarse-grained homogeneous/isotropic spatial curvature is exactly
zero on the axiom geometry.

## Exact transport consequences

This promotes three old benchmark objects to theorem-native objects:

- `H_rad(T)` itself
- `m_* = 8*pi*v^2*H_rad(T)/T^2`
- `K = m_tilde / m_*`

Numerically on the refreshed branch:

- `m_* = 0.0021417091151373236 eV`
- `K = 47.23597962989829`

These are not retained benchmark comparators anymore. They are the exact
radiation-branch transport inputs.

## Main consequence for the closure path

The current direct transport solver was already using the normalized branch
`E_H(z) = 1`. This note identifies that branch as the exact theorem-native
radiation branch rather than a diagnostic placeholder.

So the old final exact boundary on `H_rad(T)` is removed.
