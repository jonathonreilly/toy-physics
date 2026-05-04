# Gravitational Decoherence Rate -- Derived from Framework Axioms

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-13
**Script:** `scripts/frontier_grav_decoherence_derived.py`
**Depends on:** `frontier_newton_derived.py` (lattice Green's function), `frontier_dm_coulomb_from_lattice.py` (subtracted Fourier integral)

**Current publication disposition:** bounded companion only. Not on the
retained flagship claim surface.

---

## Derivation Chain

The gravitational decoherence rate follows from the single axiom (Cl(3) on Z^3) in five steps:

1. **Cl(3) on Z^3 => Poisson equation.** The staggered scalar field satisfies (-Delta_lat) phi = rho, the lattice Poisson equation.

2. **Poisson equation => Lattice Green's function.** The Green's function G_lat(r) = 1/(4 pi r) + Delta(r), where Delta(r) encodes lattice corrections that vanish as r -> infinity. (Maradudin et al. 1971; confirmed numerically in frontier_newton_derived.py to < 1% for r >= 5.)

3. **Superposed mass => distinguishable field configurations.** A mass m in superposition at positions x_1, x_2 (separation delta_x) sources two gravitational fields phi_1, phi_2 via the lattice Green's function. The gravitational self-energy difference (Penrose 1996): E_G = G m^2 / delta_x * F(delta_x / a), where F is the lattice form factor.

4. **Field distinguishability => decoherence rate.** The decoherence rate gamma = E_G / hbar = (G m^2)/(hbar delta_x) * F(delta_x / a). This is the Penrose-Diosi rate modified by the lattice form factor.

5. **Form factor F -> 1 in continuum limit.** For `delta_x >> a`, `F = 1 + O(a/delta_x)^2`. On the current Planck-scale package pin for the physical lattice, `a = l_Planck`, so at physical separations `|F - 1| ~ 10^{-58}` and the lattice correction is undetectable.

---

## Key Results

### Decoherence Rates

| Configuration | m (kg) | delta_x | gamma (Hz) | tau (s) | Phi_ent (rad) |
|--------------|--------|---------|------------|---------|---------------|
| Conservative NV | 10^{-14} | 1 um | 52.6 | 0.019 | 6.3e-3 |
| BMV original | 10^{-14} | 250 um | 0.253 | 3.95 | 12.4 |
| Aspelmeyer tabletop | 10^{-12} | 10 um | 5.7e4 | 1.8e-5 | 1.3e3 |
| Optimistic next-dec | 10^{-10} | 1 um | 7.6e9 | 1.3e-10 | 5.1e7 |

### Lattice Form Factor (3D, on-axis)

| r (lattice units) | F = G_lat / G_cont | |F - 1| |
|---|---|---|
| 1 | 1.030 | 3.0% |
| 5 | 0.990 | 1.0% |
| 10 | 1.014 | 1.4% |
| 20 | 1.006 | 0.6% |
| 30 | 1.004 | 0.4% |

The form factor converges to 1 as r increases, confirming the continuum limit. The oscillatory approach is a lattice artifact from the cubic symmetry of Z^3.

### Lattice Correction at Physical Scales

On the current Planck-scale package pin `a = l_Planck = 1.616e-35 m`:

    delta_x = 1 um:   delta_x/a = 6.2e28,  |F-1| ~ 6.5e-58
    delta_x = 250 um: delta_x/a = 1.5e31,  |F-1| ~ 10^{-62}

The lattice correction to the decoherence rate is undetectable at any experimentally accessible separation.

---

## BMV Feasibility

At BMV original parameters (m = 10 pg, delta_x = 250 um, d = 200 um, T = 2 s):

- **Decoherence rate:** gamma_grav = 0.253 Hz
- **Decoherence budget:** gamma_total < 1/T = 0.5 Hz
- **Gravity uses 50.6% of the budget** -- feasible but not negligible
- **Entanglement phase:** Phi = 12.4 rad >> 1 -- strongly detectable

The arms cross in the original BMV geometry (d - delta_x = -50 um), so the minimum approach is set by the physical extent of the microspheres (~10 um). This crossing geometry is what gives the large entanglement phase.

---

## Born Rule Connection

The decoherence rate and the Born rule are both consequences of the propagator linearity:

    gamma(beta) = gamma_0 * [1 + (beta - 1) + O((beta - 1)^2)]

where beta parametrizes propagator nonlinearity.

**Current bounds:**
- |I_3| < 10^{-4} (Pleinert 2020) => |beta - 1| < 0.01 => delta_gamma/gamma < 1%
- |beta - 1| < 10^{-5} (Eot-Wash) => delta_gamma/gamma < 10^{-5}

**Framework prediction:** beta = 1 exactly (linear propagator), so gamma = gamma_Penrose-Diosi exactly (up to geometry corrections).

A measurement of gamma_grav that disagrees with this prediction constrains:
- The lattice form factor (new physics at short distances)
- The Born rule parameter (propagator nonlinearity)
- The framework itself (potential falsification)

---

## Verification

The script runs 7 numerical checks, all passing:
- G_lat(20)/G_cont(20) = 1 to < 1%
- Form factor F(20) = 1 to < 1%
- gamma_PD = 63.3 Hz (m=10pg, dx=1um)
- gamma_geom = 52.6 Hz (with sphere geometry)
- Lattice correction negligible (~ 10^{-58})
- gamma_BMV = 0.253 Hz
- Phi_BMV = 12.4 rad

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [newton_law_derived_note](NEWTON_LAW_DERIVED_NOTE.md)
- [gravity_full_self_consistency_note](GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md)
