# Magnetic Monopole Mass: First-Principles Derivation

**Date:** 2026-04-12 (RECONCILED 2026-05-01)
**Script:** `scripts/frontier_monopole_derived.py`
**Status:** Derived -- `M_mono ~ 1.43 M_Planck` on the current Planck-scale package pin

**Current publication disposition:** bounded companion only. Not on the
retained flagship claim surface.

## Summary

The monopole mass `M_mono ~ 1.43 M_Planck = 1.75e19 GeV` is derived from the
compact-lattice self-energy chain on the current Planck-scale package pin,
with every assumption explicit. The Dirac quantization condition is automatic
(not postulated), and the overclosure calculation shows the framework requires
inflation for cosmological consistency.

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

- `c = G_lat(0) = 0.2527` (lattice Green's function at origin, cubic Z^3)
- `beta = 1/(4*pi*alpha_EM(M_Pl))` with `alpha_EM^{-1}(M_Pl) ~ 72.1` from
  one-loop SM RG running (`b_EM = 41/10`, `alpha_inv(M_Z) = 127.9`)
- `M_Planck = 1.221 x 10^19 GeV`

Result: `M_mono = 0.2527 * 5.738 * M_Pl = 1.43 M_Planck = 1.75e19 GeV`.

Sensitivity: for `alpha^{-1}(M_Pl)` in `[30, 60]`, `M_mono` ranges over
`[0.60, 1.21] M_Planck`; for `alpha^{-1}(M_Pl) ~ 72` (one-loop SM RG),
the result is `1.43 M_Planck`. The order of magnitude `M ~ M_Planck`
is robust across the full plausible range.

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

## Reconciliation Note (2026-05-01)

An earlier version of this note advertised `M_mono ~ 0.80 M_Planck` based on
the placeholder estimate `alpha_EM^{-1}(M_Pl) ~ 40`. The live runner now
performs one-loop SM RG running from `alpha_EM(M_Z)` and obtains
`alpha_EM^{-1}(M_Pl) ~ 72.1`, which gives `M_mono = 1.43 M_Planck` instead.

Both values are Planckian; the order-of-magnitude prediction
`M_mono ~ M_Planck` is the robust headline. The exact prefactor depends on
which `alpha_EM(M_Pl)` extrapolation is used. The runner's current value
(`1.43`) is the headline of this reconciled note.

## Assumptions (Explicit)

1. **Planck-scale package pin:** on the accepted physical-lattice reading,
   `a^(-1) = M_Pl` is carried as an explicit package pin rather than as a
   derived theorem
2. **Wilson action** -- simplest compact U(1) action on cubic lattice
3. **alpha_EM(M_Pl) from one-loop SM RG running** (external input).
   Two-loop and threshold matching corrections not implemented; the prefactor
   on `M_mono` therefore inherits the uncertainty in this extrapolation.
4. **Standard FRW cosmology** -- for abundance calculation
5. **Kibble mechanism** -- applies at graph-growth epoch

## What Is Not Derived

- The exact value of `alpha_EM(M_Pl)` (one-loop only; full two-loop SM RG
  with threshold matching not implemented)
- Whether inflation actually occurred (required by the framework, not derived)
- Short-range monopole-monopole interactions (lattice artifacts dominate)

## Relation to Earlier Versions

Earlier scripts and notes carried a different prefactor depending on the
`alpha_EM(M_Pl)` extrapolation:

- mixing in a 4D DeGrand-Toussaint-style coefficient instead of the 3D BKM
  value gave a much larger headline
- using the placeholder `alpha^{-1} ~ 40` gave `M_mono ~ 0.80 M_Planck`
- using the live one-loop SM RG running (`alpha^{-1} ~ 72`) gives
  `M_mono ~ 1.43 M_Planck`

The package now tracks the runner-consistent value `1.43 M_Planck` and
labels it as bounded support, not a flagship retained claim.
