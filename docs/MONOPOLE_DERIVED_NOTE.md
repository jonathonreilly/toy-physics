# Magnetic Monopole Mass: First-Principles Derivation

**Date:** 2026-04-12
**Script:** `scripts/frontier_monopole_derived.py`
**Status:** Derived -- `M_mono ~ 0.80 M_Planck` on the current Planck-scale package pin

**Current publication disposition:** bounded companion only. Not on the
retained flagship claim surface.

## Summary

The monopole mass `M_mono ~ 0.80 M_Planck` is derived from the compact-lattice
self-energy chain on the current Planck-scale package pin, with every
assumption explicit. The Dirac quantization
condition is automatic (not postulated), and the overclosure calculation
shows the framework requires inflation for cosmological consistency.

## Derivation Chain

### Step 1: Compactness

On Z^3, gauge fields live as group elements U = exp(i*theta) on edges,
with theta in [0, 2*pi). This compactness is forced by the lattice
structure. The magnetic charge through any cube is provably an integer
(verified numerically on 100 random L=8 configurations).

### Step 2: Dirac Quantization

The minimum magnetic charge is m = 1 in lattice units. The physical
charge is g = 2*pi/e, giving e*g = 2*pi -- the Dirac condition. This
is not a new postulate; it follows from the periodicity of theta.

### Step 3: Monopole Mass

The monopole self-energy is computed analytically from the lattice
Coulomb Green's function:

    M_mono = c * beta * M_Planck

where:
- c = G_lat(0) = 0.2527 (lattice Green's function at origin, cubic Z^3)
- beta = 1/(4*pi*alpha_EM(M_Pl)) with alpha_EM(M_Pl) ~ 1/40
- M_Planck = 1.221 x 10^19 GeV

Result: `M_mono = 0.80 M_Planck = 9.8 x 10^18 GeV`.

Sensitivity: for `alpha^{-1}(M_Pl)` in `[30, 60]`, `M_mono` ranges over
`[0.60, 1.21] M_Planck`. The order of magnitude remains Planckian.

### Step 4: Numerical Cross-Check

Direct Wilson action measurement on L = 6, 8, 10, 12 lattices with
explicit monopole-antimonopole configurations. Finite-volume effects
are significant but the trend is consistent with the analytic result.

### Step 5: Overclosure

Kibble mechanism at the graph-growth epoch gives n_mono/n_gamma ~ 4.
Without inflation: Omega_mono ~ 6 x 10^27 (catastrophic overclosure).
With inflation (N_e > 21 e-folds): monopoles diluted to zero.
Post-inflation thermal production impossible since T_RH << M_mono.
All experimental bounds (Parker, MACRO, IceCube, MoEDAL) trivially satisfied.

## Assumptions (Explicit)

1. **Planck-scale package pin:** on the accepted physical-lattice reading,
   `a^(-1) = M_Pl` is carried as an explicit package pin rather than as a
   derived theorem
2. **Wilson action** -- simplest compact U(1) action on cubic lattice
3. **alpha_EM(M_Pl) ~ 1/40** -- from SM RG running (external input,
   not derived within the framework)
4. **Standard FRW cosmology** -- for abundance calculation
5. **Kibble mechanism** -- applies at graph-growth epoch

## What Is Not Derived

- The exact value of alpha_EM(M_Pl) (requires full SM RG, external input)
- Whether inflation actually occurred (required by the framework, not derived)
- Short-range monopole-monopole interactions (lattice artifacts dominate)

## Relation to Previous Script

Older scripts advertised a larger order-one Planck-mass coefficient. The current
derivation uses the cubic-lattice Green's-function coefficient
`G_lat(0) ~ 0.2527` together with `alpha_EM(M_Pl)^(-1) ~ 40`, giving
`M_mono ~ 0.80 M_Planck`. The older larger headline came from mixing in a
4D DeGrand-Toussaint-style coefficient instead of the 3D spatial BKM value.
The public package now tracks the runner-consistent 3D result.
