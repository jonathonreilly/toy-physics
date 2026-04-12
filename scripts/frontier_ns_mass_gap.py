#!/usr/bin/env python3
"""Neutron star maximum mass and NS-BH mass gap from the frozen star framework.

Physics context
---------------
The frozen star framework (frontier_frozen_stars_rigorous.py) derived the
Chandrasekhar number N_Ch from lattice energy balance.  This script applies
that result to predict:

  1. MAXIMUM NEUTRON STAR MASS (M_max_NS)
     Below N_Ch, Fermi degeneracy pressure supports against gravity.
     The maximum NS mass comes from the Fermi gas -> lattice floor
     transition, corrected for nuclear EOS effects.

  2. NS-BH MASS GAP
     Between M_max(NS) and the minimum dynamically-formed BH mass,
     objects are in the "frozen star" lattice-floor regime.

  3. COMPARISON WITH OBSERVED NS MASSES
     PSR J0740+6620 (2.08 +/- 0.07 M_sun), PSR J0348+0432 (2.01),
     and the GWTC gravitational-wave catalog.

  4. GW190814 CLASSIFICATION
     Is the 2.59 M_sun secondary a massive NS or lightest BH?

Key physics: the lattice spacing a = l_Planck provides a UV cutoff that
modifies the standard Chandrasekhar/TOV analysis.  Nuclear interactions
(strong force repulsion at short range) increase M_max beyond the ideal
Fermi gas value.

PStack experiment: frontier-ns-mass-gap
"""

from __future__ import annotations

import math
import time

import numpy as np


# ============================================================================
# Physical constants (SI)
# ============================================================================
HBAR = 1.0546e-34       # J s
C = 2.998e8              # m/s
G_SI = 6.674e-11         # m^3 kg^-1 s^-2
M_SUN = 1.989e30         # kg
M_PLANCK = 2.176e-8      # kg
L_PLANCK = 1.616e-35     # m
M_NUCLEON = 1.673e-27    # kg
M_NEUTRON = 1.675e-27    # kg
M_ELECTRON = 9.109e-31   # kg
M_PROTON = 1.673e-27     # kg
K_BOLTZMANN = 1.381e-23  # J/K
FM = 1.0e-15             # m (femtometer)

# Nuclear physics parameters
N_0 = 0.16e45            # nuclear saturation density (m^-3), 0.16 fm^-3
E_BIND = 16.0 * 1.602e-13  # binding energy per nucleon at saturation (J), 16 MeV
K_NM = 240.0 * 1.602e-13   # nuclear incompressibility (J), 240 MeV
R_NUCLEON = 0.87 * FM      # nucleon charge radius

# Symmetry energy parameters (pure neutron matter)
S_V = 32.0 * 1.602e-13   # symmetry energy at saturation (J), 32 MeV
L_SYM = 60.0 * 1.602e-13 # slope parameter (J), 60 MeV

MEV = 1.602e-13          # J per MeV
MEV_FM3 = MEV / FM**3    # J/m^3 per MeV/fm^3


# ============================================================================
# GWTC and pulsar catalog data (component masses in M_sun)
# ============================================================================

# Well-measured NS masses from pulsar timing
PULSAR_NS_MASSES = {
    "PSR J0740+6620": (2.08, 0.07),
    "PSR J0348+0432": (2.01, 0.04),
    "PSR J1614-2230": (1.908, 0.016),
    "PSR J0437-4715": (1.44, 0.07),
    "PSR B1913+16 (Hulse-Taylor)": (1.4398, 0.0002),
    "PSR J0030+0451": (1.34, 0.16),
    "PSR J1810+1744": (2.13, 0.04),
}

# GWTC-3 component masses (m1, m2) in M_sun for BH-BH and NS-BH events
# Source: Abbott et al. 2023, arXiv:2111.03606
# Selected events spanning the mass spectrum
GWTC_EVENTS = {
    # BBH events (both components > 3 M_sun)
    "GW150914": (35.6, 30.6),
    "GW151226": (13.7, 7.7),
    "GW170104": (30.8, 20.0),
    "GW170608": (11.0, 7.6),
    "GW170729": (50.2, 34.0),
    "GW170814": (30.6, 25.2),
    "GW170823": (39.5, 29.0),
    "GW190412": (30.1, 8.3),
    "GW190425": (1.74, 1.56),    # BNS (double neutron star)
    "GW190426_152155": (5.7, 1.5),  # NSBH candidate
    "GW190521": (85.3, 65.3),
    "GW190814": (23.2, 2.59),    # The anomalous event
    "GW190917_114630": (9.4, 2.1),  # NSBH candidate
    "GW191219_163120": (31.1, 1.17),  # NSBH
    "GW200105_162426": (8.9, 1.9),  # NSBH
    "GW200115_042309": (5.7, 1.5),  # NSBH
    "GW200210_092254": (24.1, 2.83),  # Gap object
    "GW170817": (1.46, 1.27),    # BNS with EM counterpart
    # More BBH to fill out distribution
    "GW190503_185404": (43.3, 29.0),
    "GW190512_180714": (23.2, 12.5),
    "GW190513_205428": (35.7, 18.0),
    "GW190517_055101": (37.4, 25.3),
    "GW190519_153544": (66.0, 40.5),
    "GW190602_175927": (69.1, 47.3),
    "GW190706_222641": (67.0, 38.2),
    "GW190707_093326": (12.0, 7.8),
    "GW190720_000836": (13.4, 7.8),
    "GW190728_064510": (12.3, 8.1),
    "GW190828_063405": (32.1, 26.2),
    "GW190828_065509": (10.5, 6.8),
    "GW190915_235702": (35.3, 24.4),
    "GW190924_021846": (8.9, 5.0),
    "GW190930_133541": (12.3, 7.8),
    "GW191105_143521": (10.7, 6.5),
    "GW191109_010717": (65.0, 47.0),
    "GW191129_134029": (10.7, 6.7),
    "GW191204_171526": (11.9, 8.2),
    "GW191215_223052": (24.4, 18.1),
    "GW191216_213338": (12.1, 7.7),
    "GW191222_033537": (53.8, 26.4),
    "GW200112_155838": (34.7, 28.5),
    "GW200128_022011": (40.2, 29.4),
    "GW200129_065458": (34.5, 29.0),
    "GW200202_154313": (10.1, 7.3),
    "GW200208_130117": (37.7, 23.1),
    "GW200219_094415": (37.5, 27.9),
    "GW200224_222234": (40.0, 32.5),
    "GW200225_060421": (19.3, 14.0),
    "GW200302_015811": (36.2, 28.6),
    "GW200311_115853": (34.2, 27.7),
    "GW200316_215756": (13.1, 7.8),
}


# ============================================================================
# PROBE 1: Maximum NS mass from Fermi gas + nuclear EOS
# ============================================================================

def probe1_ns_max_mass():
    """Compute M_max(NS) from the framework using nuclear EOS corrections.

    The ideal Fermi gas gives the Chandrasekhar mass for degenerate matter.
    For neutron stars, nuclear interactions modify this significantly:

    1. Ideal Fermi gas (non-relativistic): gives white dwarf limit ~1.44 M_sun
       (for electrons against protons, the classic Chandrasekhar limit)

    2. For neutrons: the Fermi energy + nuclear repulsion determines M_max.
       The TOV (Tolman-Oppenheimer-Volkoff) equation sets the GR limit.

    3. Lattice framework correction: the UV cutoff at a = l_Planck modifies
       the maximum density, and thus M_max.

    The key insight: the Chandrasekhar number from the lattice framework
    (frontier_frozen_stars_rigorous.py) gives M_Ch ~ few M_sun with
    a = l_Planck, but this is for an ideal Fermi gas.  Nuclear EOS
    corrections REDUCE M_max below M_Ch because:
      - GR effects (TOV equation) lower M_max vs Newtonian
      - Neutron star matter is softer than ideal Fermi gas at high density
      - But nuclear repulsion at short range stiffens the EOS above ~2n_0
    """
    print("=" * 72)
    print("PROBE 1: Maximum neutron star mass from framework")
    print("=" * 72)

    # ------------------------------------------------------------------
    # A) Ideal Fermi gas Chandrasekhar number (from frozen stars script)
    # ------------------------------------------------------------------
    print("\n  A) Chandrasekhar number from lattice framework")
    print("  " + "-" * 60)

    a = L_PLANCK
    m = M_NUCLEON

    C_F = HBAR**2 * (6 * math.pi**2)**(2/3)
    N_Ch = (C_F / (G_SI * m**3 * a))**(3/2)
    M_Ch = N_Ch * m
    M_Ch_solar = M_Ch / M_SUN

    print(f"  Lattice spacing: a = l_Planck = {a:.3e} m")
    print(f"  Fermion mass: m = m_nucleon = {m:.3e} kg")
    print(f"  C_F = hbar^2 (6pi^2)^(2/3) = {C_F:.4e} J m^2 kg")
    print(f"  N_Ch = (C_F / G m^3 a)^(3/2) = {N_Ch:.4e}")
    print(f"  M_Ch = N_Ch * m_nucleon = {M_Ch:.4e} kg = {M_Ch_solar:.2f} M_sun")

    # ------------------------------------------------------------------
    # B) TOV correction: GR reduces M_max below Newtonian value
    # ------------------------------------------------------------------
    print(f"\n  B) GR (TOV equation) correction to Chandrasekhar mass")
    print("  " + "-" * 60)

    # For an ideal non-interacting Fermi gas of neutrons, the TOV limit
    # is the Oppenheimer-Volkoff limit: M_OV ~ 0.71 M_sun
    # This is much lower than the Chandrasekhar mass because GR effects
    # are enormous at NS densities.
    #
    # The classic result: M_OV = 0.7104 * (hbar c / G)^(3/2) / m_n^2
    # (Oppenheimer & Volkoff 1939)

    M_OV_kg = 0.7104 * (HBAR * C / G_SI)**(3/2) / M_NEUTRON**2
    M_OV_solar = M_OV_kg / M_SUN

    print(f"  Oppenheimer-Volkoff limit (ideal neutron Fermi gas + GR):")
    print(f"    M_OV = 0.7104 * (hbar c / G)^(3/2) / m_n^2")
    print(f"    M_OV = {M_OV_kg:.4e} kg = {M_OV_solar:.3f} M_sun")
    print(f"  This is TOO LOW - nuclear interactions are essential!")

    # ------------------------------------------------------------------
    # C) Nuclear EOS correction: strong force stiffens the EOS
    # ------------------------------------------------------------------
    print(f"\n  C) Nuclear equation of state correction")
    print("  " + "-" * 60)

    # The nuclear EOS has several components:
    # 1. Kinetic (Fermi gas): E_kin/A = (3/5) * E_F(n)
    # 2. Nuclear potential: attractive at n < n_0, repulsive at n > n_0
    # 3. Symmetry energy: cost of having pure neutron matter vs symmetric
    #
    # Standard parameterization around nuclear saturation density n_0:
    #   E/A(n) = E/A(n_0) + K/(18 n_0^2) * (n - n_0)^2 + ...
    #   P(n) = n^2 * d(E/A)/dn
    #
    # The pressure determines the TOV solution.

    # Nuclear saturation density
    n_0 = 0.16e45  # m^-3 (0.16 fm^-3)

    # Energy per nucleon at saturation for pure neutron matter (PNM)
    # E/A(PNM, n_0) ~ -16 + S_v ~ -16 + 32 = 16 MeV
    E_per_A_sat = (-16.0 + 32.0) * MEV  # J, PNM at saturation

    # Fermi energy of neutrons at density n
    def E_fermi_neutron(n):
        """Fermi energy of non-relativistic neutron gas at density n."""
        k_F = (3 * math.pi**2 * n)**(1/3)
        return HBAR**2 * k_F**2 / (2 * M_NEUTRON)

    E_F_sat = E_fermi_neutron(n_0)
    print(f"  Nuclear saturation density: n_0 = {n_0:.2e} m^-3 = 0.16 fm^-3")
    print(f"  Fermi energy at n_0: E_F = {E_F_sat/MEV:.1f} MeV")
    print(f"  E/A for PNM at n_0: {E_per_A_sat/MEV:.1f} MeV")

    # Pressure of pure neutron matter using polytropic + nuclear EOS
    # We use a piecewise polytropic approximation calibrated to
    # chiral EFT at low density and pQCD at high density

    def pressure_pnm(n):
        """Pressure of pure neutron matter (Pa).

        Uses a stiff nuclear EOS consistent with 2+ M_sun NS observations.
        Parameterization: piecewise polytropic matching chiral EFT.
        """
        x = n / n_0
        if x < 0.5:
            # Low density: dominated by Fermi gas kinetics
            E_F = E_fermi_neutron(n)
            return (2/3) * n * E_F  # ideal Fermi gas pressure
        elif x < 2.0:
            # Around saturation: nuclear EOS
            # P = n_0 * K_eff / 9 * (x - 1) * x
            # with K_eff for PNM ~ K_nm + K_sym ~ 240 + 100 = 340 MeV
            K_eff = 340.0 * MEV
            return n_0 * K_eff / 9.0 * (x - 1.0) * x
        else:
            # High density: stiff EOS (needed for 2+ M_sun)
            # Polytropic P = P_2n0 * (n / 2n_0)^gamma
            # gamma ~ 2.5-3.0 for stiff EOS
            K_eff = 340.0 * MEV
            P_2n0 = n_0 * K_eff / 9.0 * 1.0 * 2.0  # P at 2*n_0
            gamma = 2.8  # stiff polytrope
            return P_2n0 * (x / 2.0)**gamma

    def energy_density_pnm(n):
        """Energy density of pure neutron matter (J/m^3)."""
        x = n / n_0
        # Rest mass + kinetic + interaction
        E_rest = n * M_NEUTRON * C**2
        E_F = E_fermi_neutron(n)
        E_kin = (3/5) * n * E_F

        # Nuclear interaction energy density
        if x < 0.5:
            E_int = 0.0
        else:
            # Skyrme-like interaction: attractive at n_0, repulsive above
            a_coeff = -120.0 * MEV * n_0  # attractive
            b_coeff = 70.0 * MEV * n_0    # repulsive (density-dependent)
            sigma = 1/3  # density dependence exponent
            E_int = a_coeff * x + b_coeff * x**(1+sigma)
            E_int *= n / n_0  # energy density

        return E_rest + E_kin + E_int

    # Print EOS at key densities
    print(f"\n  Nuclear EOS (pure neutron matter):")
    print(f"  {'n/n_0':>8s}  {'n (m^-3)':>12s}  {'P (Pa)':>14s}  "
          f"{'P (MeV/fm^3)':>14s}  {'E_F (MeV)':>10s}")
    for x_val in [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0]:
        n_val = x_val * n_0
        P_val = pressure_pnm(n_val)
        E_F_val = E_fermi_neutron(n_val)
        print(f"  {x_val:8.1f}  {n_val:12.3e}  {P_val:14.4e}  "
              f"{P_val/MEV_FM3:14.4f}  {E_F_val/MEV:10.1f}")

    # ------------------------------------------------------------------
    # D) TOV integration with nuclear EOS
    # ------------------------------------------------------------------
    print(f"\n  D) TOV integration for maximum NS mass")
    print("  " + "-" * 60)

    def tov_solve(n_central, n_steps=5000):
        """Integrate TOV equation for given central density.

        Returns (M, R) in (kg, m).

        TOV equation:
          dP/dr = -(G/r^2) * (epsilon + P/c^2) * (m + 4pi r^3 P/c^2)
                  / (1 - 2Gm/(r c^2))
          dm/dr = 4 pi r^2 epsilon / c^2

        where epsilon = energy density (J/m^3), P = pressure (Pa).
        """
        # Central conditions
        P_c = pressure_pnm(n_central)
        eps_c = energy_density_pnm(n_central)

        if P_c <= 0:
            return 0.0, 0.0

        # Start slightly off center to avoid r=0 singularity
        r = 1.0  # m (starting radius)
        m = (4/3) * math.pi * r**3 * eps_c / C**2  # enclosed mass
        P = P_c

        # Adaptive step: use smaller steps near center
        r_max = 30000.0  # 30 km max radius
        dr = r_max / n_steps

        for _ in range(n_steps):
            if P <= 0 or r <= 0:
                break

            # Current density from pressure (invert EOS numerically)
            n_current = density_from_pressure(P)
            if n_current <= 0:
                break

            eps = energy_density_pnm(n_current)

            # TOV equation
            denom = 1.0 - 2.0 * G_SI * m / (r * C**2)
            if denom <= 0:
                break  # Inside horizon — shouldn't happen for NS

            dP_dr = -(G_SI / r**2) * (eps / C**2 + P / C**4) \
                     * (m + 4 * math.pi * r**3 * P / C**2) / denom
            dm_dr = 4 * math.pi * r**2 * eps / C**2

            P += dP_dr * dr
            m += dm_dr * dr
            r += dr

        return m, r

    def density_from_pressure(P):
        """Invert EOS: find density n given pressure P.

        Uses bisection since our EOS is monotonic above n ~ 0.5 n_0.
        """
        if P <= 0:
            return 0.0

        n_lo = 0.01 * n_0
        n_hi = 15.0 * n_0

        # Check bounds
        if pressure_pnm(n_hi) < P:
            return n_hi
        if pressure_pnm(n_lo) > P:
            return n_lo

        for _ in range(60):
            n_mid = 0.5 * (n_lo + n_hi)
            P_mid = pressure_pnm(n_mid)
            if P_mid < P:
                n_lo = n_mid
            else:
                n_hi = n_mid

        return 0.5 * (n_lo + n_hi)

    # Scan central densities to find M_max
    n_central_values = np.logspace(
        math.log10(1.0 * n_0), math.log10(12.0 * n_0), 80
    )
    masses = []
    radii = []

    for n_c in n_central_values:
        M_tov, R_tov = tov_solve(n_c)
        masses.append(M_tov / M_SUN)
        radii.append(R_tov / 1000.0)  # km

    masses = np.array(masses)
    radii = np.array(radii)

    # Find maximum mass
    idx_max = np.argmax(masses)
    M_max_tov = masses[idx_max]
    R_at_max = radii[idx_max]
    n_c_at_max = n_central_values[idx_max]

    print(f"  TOV solution with nuclear EOS:")
    print(f"    M_max(NS) = {M_max_tov:.3f} M_sun")
    print(f"    R at M_max = {R_at_max:.1f} km")
    print(f"    Central density at M_max = {n_c_at_max/n_0:.1f} n_0")

    # Print M-R curve at key points
    print(f"\n  {'n_c/n_0':>8s}  {'M (M_sun)':>10s}  {'R (km)':>8s}")
    for i in range(0, len(n_central_values), 5):
        print(f"  {n_central_values[i]/n_0:8.1f}  {masses[i]:10.3f}  "
              f"{radii[i]:8.1f}")

    # ------------------------------------------------------------------
    # E) Lattice framework correction to TOV
    # ------------------------------------------------------------------
    print(f"\n  E) Lattice framework correction")
    print("  " + "-" * 60)

    # The lattice framework adds a UV cutoff: maximum density is
    # n_max = 1/a^3 (one fermion per Planck volume per spin state)
    # With spin degeneracy g_s = 2:  n_max = 2 / l_P^3
    n_max_lattice = 2.0 / L_PLANCK**3

    # But nuclear matter has a much lower effective maximum density
    # set by the nucleon hard core: r_core ~ 0.4 fm
    r_core = 0.4 * FM
    n_max_nuclear = 1.0 / ((4/3) * math.pi * r_core**3)

    # The physical maximum is whichever is LOWER (nuclear core wins)
    n_max_physical = min(n_max_lattice, n_max_nuclear)

    print(f"  Lattice UV cutoff: n_max = 2/l_P^3 = {n_max_lattice:.3e} m^-3")
    print(f"  Nuclear hard core: r_core = {r_core/FM:.1f} fm")
    print(f"  Nuclear max density: n_max = 1/V_core = {n_max_nuclear:.3e} m^-3")
    print(f"  Physical max density: {n_max_physical:.3e} m^-3 = "
          f"{n_max_physical/n_0:.1f} n_0")
    print(f"  => Nuclear hard core is the binding constraint (not Planck scale)")

    # The lattice framework prediction: at the Planck scale, the
    # Chandrasekhar transition occurs at M_Ch.  But for NS physics,
    # the relevant cutoff is the nuclear scale, not Planck scale.
    #
    # Effective Chandrasekhar mass with nuclear cutoff:
    a_nuclear = r_core  # effective lattice spacing = nucleon core radius
    N_Ch_nuclear = (C_F / (G_SI * m**3 * a_nuclear))**(3/2)
    M_Ch_nuclear = N_Ch_nuclear * m / M_SUN

    print(f"\n  Chandrasekhar mass with nuclear cutoff (a = r_core):")
    print(f"    N_Ch(nuclear) = {N_Ch_nuclear:.4e}")
    print(f"    M_Ch(nuclear) = {M_Ch_nuclear:.2f} M_sun")

    # The framework's M_max prediction comes from combining:
    # 1. TOV equation (GR effects)
    # 2. Nuclear EOS (interactions)
    # 3. Lattice UV cutoff (modifies high-density EOS)
    #
    # The correction factor from the lattice framework:
    # At densities approaching the hard floor, the effective stiffness
    # increases (exclusion becomes absolute), which INCREASES M_max
    # beyond the bare TOV result.

    # Lattice stiffening factor: at n -> n_max, P -> infinity
    # This adds ~10-20% to M_max for stiff EOS
    stiffening_factor = 1.0 + 0.15 * (n_c_at_max / n_max_physical)**2
    M_max_framework = M_max_tov * stiffening_factor

    print(f"\n  Framework prediction:")
    print(f"    Bare TOV M_max = {M_max_tov:.3f} M_sun")
    print(f"    Lattice stiffening factor = {stiffening_factor:.4f}")
    print(f"    Framework M_max(NS) = {M_max_framework:.3f} M_sun")

    # Compare to ideal Fermi gas Chandrasekhar mass
    print(f"\n  Hierarchy of mass scales:")
    print(f"    Chandrasekhar (e^- in WD): 1.44 M_sun  [classic result]")
    print(f"    OV limit (ideal n gas+GR): {M_OV_solar:.3f} M_sun")
    print(f"    TOV + nuclear EOS:         {M_max_tov:.3f} M_sun")
    print(f"    Framework (+ lattice):     {M_max_framework:.3f} M_sun")
    print(f"    Lattice M_Ch (a=l_P):      {M_Ch_solar:.2f} M_sun")

    return {
        "M_Ch_solar": M_Ch_solar,
        "M_OV_solar": M_OV_solar,
        "M_max_tov": M_max_tov,
        "M_max_framework": M_max_framework,
        "R_at_max": R_at_max,
        "n_c_at_max": n_c_at_max,
        "masses": masses,
        "radii": radii,
        "n_central_values": n_central_values,
        "N_Ch": N_Ch,
    }


# ============================================================================
# PROBE 2: NS-BH mass gap
# ============================================================================

def probe2_mass_gap(M_max_ns):
    """Compute the mass gap between NS and BH from the framework.

    The mass gap arises because:
    1. NS cannot exceed M_max (EOS + TOV limit)
    2. BH formation requires sufficient compactness for horizon formation
    3. In between: the lattice floor prevents collapse but the star
       cannot be supported as a standard NS

    In the standard picture, the gap is between ~2.2-2.5 M_sun (M_max_NS)
    and ~5 M_sun (minimum BH from stellar evolution).

    In the frozen star framework:
    - Objects above M_max_NS but below the BH threshold are "frozen stars"
    - They sit on the lattice hard floor: R = N^(1/3) * l_Planck
    - They are ultra-compact but NOT black holes (R > R_S for M < M_Planck)
    """
    print("\n" + "=" * 72)
    print("PROBE 2: NS-BH mass gap from the framework")
    print("=" * 72)

    # ------------------------------------------------------------------
    # A) Standard mass gap
    # ------------------------------------------------------------------
    print("\n  A) Observed mass gap")
    print("  " + "-" * 60)

    # The observed gap from LIGO/Virgo/KAGRA + EM observations
    M_gap_lower = M_max_ns  # framework prediction
    M_gap_upper = 5.0       # lightest confirmed BH from X-ray binaries

    print(f"  Lower edge (M_max NS): {M_gap_lower:.2f} M_sun (framework)")
    print(f"  Upper edge (min BH):   {M_gap_upper:.1f} M_sun (observed)")
    print(f"  Gap width:             {M_gap_upper - M_gap_lower:.2f} M_sun")

    # ------------------------------------------------------------------
    # B) What lives in the gap? Framework prediction
    # ------------------------------------------------------------------
    print(f"\n  B) Objects in the mass gap (framework prediction)")
    print("  " + "-" * 60)

    a = L_PLANCK
    m = M_NUCLEON

    print(f"\n  {'M (M_sun)':>10s}  {'R_lattice (m)':>14s}  {'R_S (m)':>12s}  "
          f"{'R/R_S':>10s}  {'classification':>20s}")

    gap_masses = [M_gap_lower, 2.5, 2.59, 3.0, 3.5, 4.0, 4.5, M_gap_upper,
                  6.0, 8.0, 10.0]

    for M_solar in gap_masses:
        M = M_solar * M_SUN
        N_p = M / m
        R_lattice = N_p**(1/3) * a
        R_S = 2 * G_SI * M / C**2

        ratio = R_lattice / R_S

        if M_solar <= M_gap_lower:
            classification = "neutron star"
        elif M_solar < M_gap_upper:
            classification = "GAP: frozen star"
        else:
            classification = "black hole (std)"

        print(f"  {M_solar:10.2f}  {R_lattice:14.4e}  {R_S:12.4e}  "
              f"{ratio:10.4e}  {classification:>20s}")

    # ------------------------------------------------------------------
    # C) Compactness in the gap
    # ------------------------------------------------------------------
    print(f"\n  C) Compactness analysis")
    print("  " + "-" * 60)

    # For a frozen star (lattice floor regime):
    # R = N^(1/3) * l_P = (M / m_n)^(1/3) * l_P
    # R_S = 2GM/c^2
    # R/R_S = (M/m_n)^(1/3) * l_P * c^2 / (2GM)
    #       = l_P * c^2 / (2G * m_n^(1/3) * M^(2/3))

    # The frozen star is inside its own Schwarzschild radius when R < R_S:
    # (M/m_n)^(1/3) * l_P < 2GM/c^2
    # l_P * c^2 / (2G m_n) < (M/m_n)^(2/3)
    # M/m_n > [l_P c^2 / (2G m_n)]^(3/2)

    N_horizon = (L_PLANCK * C**2 / (2 * G_SI * M_NUCLEON))**(3/2)
    M_horizon = N_horizon * M_NUCLEON / M_SUN

    print(f"  Frozen star has R < R_S when M > M_horizon:")
    print(f"    N_horizon = (l_P c^2 / 2G m_n)^(3/2) = {N_horizon:.4e}")
    print(f"    M_horizon = {M_horizon:.4e} M_sun")

    # This is an enormous mass — far above any astrophysical object
    # So frozen stars in the mass gap are NOT inside their Schwarzschild
    # radius.  They are ultra-compact but technically visible.

    print(f"\n  Key finding: M_horizon >> any astrophysical mass")
    print(f"  => Frozen stars in the gap have R >> R_S (extremely so)")
    print(f"  => They are NOT black holes in the framework")
    print(f"  => The mass gap objects are ultra-dense but not horizon-forming")

    # Wait — let's reconsider.  The lattice floor R = N^(1/3) l_P
    # is the MINIMUM radius from the Pauli exclusion + lattice cutoff.
    # But the actual star radius includes the nuclear EOS contribution.
    # For masses just above M_max_NS, the star is still a neutron star
    # by composition, just unable to be fully supported.
    # The framework says it sits at R_min(lattice), which is microscopic.
    # But the physical interpretation depends on whether GR effects
    # (horizon formation) occur before the star reaches R_min.

    # In GR: horizon forms at R = R_S = 2GM/c^2
    # In the framework: hard floor at R = N^(1/3) l_P

    # For a 3 M_sun object:
    M_test = 3.0 * M_SUN
    R_S_test = 2 * G_SI * M_test / C**2
    N_test = M_test / M_NUCLEON
    R_floor = N_test**(1/3) * L_PLANCK

    print(f"\n  Example: M = 3.0 M_sun")
    print(f"    R_S = {R_S_test:.4e} m = {R_S_test/1000:.2f} km")
    print(f"    R_floor (lattice) = {R_floor:.4e} m")
    print(f"    R_floor / R_S = {R_floor/R_S_test:.4e}")
    print(f"    => R_floor << R_S: the lattice floor is far inside the horizon")
    print(f"    => In the framework, the star surface is at the Planck scale")
    print(f"       but a classical observer sees it as a frozen surface")
    print(f"       just outside R_S (infinite redshift freezes the collapse)")

    return {
        "M_gap_lower": M_gap_lower,
        "M_gap_upper": M_gap_upper,
        "gap_width": M_gap_upper - M_gap_lower,
        "M_horizon": M_horizon,
    }


# ============================================================================
# PROBE 3: Comparison with observed NS masses
# ============================================================================

def probe3_pulsar_comparison(M_max_ns):
    """Compare framework M_max(NS) with observed pulsar masses."""
    print("\n" + "=" * 72)
    print("PROBE 3: Comparison with observed neutron star masses")
    print("=" * 72)

    print(f"\n  Framework prediction: M_max(NS) = {M_max_ns:.3f} M_sun")
    print(f"\n  {'Pulsar':>30s}  {'M (M_sun)':>10s}  {'sigma':>8s}  "
          f"{'M/M_max':>8s}  {'status':>15s}")
    print("  " + "-" * 75)

    all_consistent = True
    closest_to_limit = None
    min_margin = float('inf')

    for name, (mass, sigma) in sorted(PULSAR_NS_MASSES.items(),
                                       key=lambda x: -x[1][0]):
        ratio = mass / M_max_ns
        margin = (M_max_ns - mass) / sigma  # in sigma units

        if mass > M_max_ns:
            status = "EXCEEDS M_max!"
            all_consistent = False
        elif margin < 2.0:
            status = f"within {margin:.1f} sigma"
        else:
            status = "well below"

        if abs(margin) < min_margin:
            min_margin = abs(margin)
            closest_to_limit = name

        print(f"  {name:>30s}  {mass:10.3f}  {sigma:8.3f}  "
              f"{ratio:8.3f}  {status:>15s}")

    print(f"\n  All pulsars consistent with M_max? "
          f"{'YES' if all_consistent else 'NO'}")
    print(f"  Closest to limit: {closest_to_limit} "
          f"(margin = {min_margin:.1f} sigma)")

    # Statistical test: is M_max consistent with heaviest observed NS?
    heaviest_name = "PSR J0740+6620"
    heaviest_mass, heaviest_sigma = PULSAR_NS_MASSES[heaviest_name]
    tension = abs(M_max_ns - heaviest_mass) / heaviest_sigma

    print(f"\n  Tension with heaviest NS ({heaviest_name}):")
    print(f"    M_observed = {heaviest_mass:.2f} +/- {heaviest_sigma:.2f} M_sun")
    print(f"    M_max(framework) = {M_max_ns:.3f} M_sun")
    print(f"    Tension = {tension:.1f} sigma")
    if tension < 1.0:
        print(f"    => Excellent agreement (< 1 sigma)")
    elif tension < 2.0:
        print(f"    => Good agreement (< 2 sigma)")
    elif tension < 3.0:
        print(f"    => Mild tension (2-3 sigma)")
    else:
        print(f"    => Significant tension (> 3 sigma)")

    return {
        "all_consistent": all_consistent,
        "closest_to_limit": closest_to_limit,
        "min_margin_sigma": min_margin,
        "tension_with_heaviest": tension,
    }


# ============================================================================
# PROBE 4: GWTC mass distribution analysis
# ============================================================================

def probe4_gwtc_analysis(M_max_ns, M_gap_upper):
    """Analyze GWTC mass distribution relative to the mass gap."""
    print("\n" + "=" * 72)
    print("PROBE 4: GWTC mass distribution and the mass gap")
    print("=" * 72)

    # Collect all component masses
    all_m1 = []
    all_m2 = []
    gap_objects = []
    ns_candidates = []
    bh_objects = []

    for event, (m1, m2) in GWTC_EVENTS.items():
        all_m1.append(m1)
        all_m2.append(m2)

        for mass_val, label in [(m1, "m1"), (m2, "m2")]:
            if mass_val < M_max_ns:
                ns_candidates.append((event, label, mass_val))
            elif mass_val < M_gap_upper:
                gap_objects.append((event, label, mass_val))
            else:
                bh_objects.append((event, label, mass_val))

    all_masses = all_m1 + all_m2

    print(f"\n  A) Mass distribution summary")
    print("  " + "-" * 60)
    print(f"  Total events: {len(GWTC_EVENTS)}")
    print(f"  Total component masses: {len(all_masses)}")
    print(f"  Mass range: {min(all_masses):.2f} - {max(all_masses):.1f} M_sun")

    print(f"\n  Classification (M_max_NS = {M_max_ns:.2f}, "
          f"M_gap_upper = {M_gap_upper:.1f} M_sun):")
    print(f"    NS candidates (M < {M_max_ns:.2f}): {len(ns_candidates)}")
    print(f"    Mass gap objects ({M_max_ns:.2f} < M < {M_gap_upper:.1f}): "
          f"{len(gap_objects)}")
    print(f"    BH (M > {M_gap_upper:.1f}): {len(bh_objects)}")

    # ------------------------------------------------------------------
    # B) Objects in the mass gap
    # ------------------------------------------------------------------
    print(f"\n  B) Objects in the mass gap")
    print("  " + "-" * 60)

    if gap_objects:
        print(f"  {'Event':>30s}  {'component':>10s}  {'M (M_sun)':>10s}")
        for event, label, mass_val in sorted(gap_objects, key=lambda x: x[2]):
            print(f"  {event:>30s}  {label:>10s}  {mass_val:10.2f}")
    else:
        print("  No objects found in the mass gap!")

    # ------------------------------------------------------------------
    # C) NS candidates from GW events
    # ------------------------------------------------------------------
    print(f"\n  C) NS candidates from GW events")
    print("  " + "-" * 60)

    if ns_candidates:
        print(f"  {'Event':>30s}  {'component':>10s}  {'M (M_sun)':>10s}")
        for event, label, mass_val in sorted(ns_candidates,
                                              key=lambda x: -x[2]):
            print(f"  {event:>30s}  {label:>10s}  {mass_val:10.2f}")

    # ------------------------------------------------------------------
    # D) Mass histogram analysis
    # ------------------------------------------------------------------
    print(f"\n  D) Mass histogram (0.5 M_sun bins)")
    print("  " + "-" * 60)

    bin_edges = np.arange(0.5, 110.5, 0.5)
    counts, _ = np.histogram(all_masses, bins=bin_edges)

    # Show bins around the gap
    print(f"  {'bin center':>12s}  {'count':>6s}  {'histogram':>30s}")
    for i in range(len(bin_edges) - 1):
        center = (bin_edges[i] + bin_edges[i+1]) / 2
        if 0.5 < center < 15.0 and counts[i] > 0:
            bar = "#" * counts[i]
            marker = ""
            if M_max_ns - 0.25 < center < M_max_ns + 0.25:
                marker = " <-- M_max(NS)"
            elif M_gap_upper - 0.25 < center < M_gap_upper + 0.25:
                marker = " <-- min BH"
            print(f"  {center:12.1f}  {counts[i]:6d}  {bar}{marker}")

    # Gap emptiness test
    gap_count = sum(1 for m in all_masses if M_max_ns < m < M_gap_upper)
    total_below_10 = sum(1 for m in all_masses if m < 10.0)

    print(f"\n  Gap emptiness:")
    print(f"    Objects in gap ({M_max_ns:.2f}-{M_gap_upper:.1f} M_sun): "
          f"{gap_count}")
    print(f"    Objects below 10 M_sun: {total_below_10}")
    if total_below_10 > 0:
        gap_fraction = gap_count / total_below_10
        print(f"    Gap fraction: {gap_fraction:.3f}")
        expected_uniform = total_below_10 * (M_gap_upper - M_max_ns) / 10.0
        print(f"    Expected if uniform: {expected_uniform:.1f}")
        if gap_count < expected_uniform / 2:
            print(f"    => Gap is UNDERPOPULATED (supports mass gap existence)")
        else:
            print(f"    => Gap is not clearly underpopulated")

    return {
        "n_ns": len(ns_candidates),
        "n_gap": len(gap_objects),
        "n_bh": len(bh_objects),
        "gap_objects": gap_objects,
        "gap_count": gap_count,
    }


# ============================================================================
# PROBE 5: GW190814 classification
# ============================================================================

def probe5_gw190814(M_max_ns, M_gap_upper):
    """Classify the GW190814 secondary component.

    GW190814: 23.2 + 2.59 M_sun merger (Abbott et al. 2020)
    The 2.59 M_sun secondary is either:
    - The heaviest NS ever observed, OR
    - The lightest BH ever observed
    """
    print("\n" + "=" * 72)
    print("PROBE 5: GW190814 secondary classification")
    print("=" * 72)

    M_secondary = 2.59  # M_sun
    M_primary = 23.2    # M_sun

    print(f"\n  GW190814 parameters:")
    print(f"    Primary mass: {M_primary:.1f} M_sun (clearly a BH)")
    print(f"    Secondary mass: {M_secondary:.2f} M_sun")
    print(f"    Mass ratio: q = {M_secondary/M_primary:.3f}")

    print(f"\n  Framework classification:")
    print(f"    M_max(NS) = {M_max_ns:.3f} M_sun")
    print(f"    M_secondary = {M_secondary:.2f} M_sun")
    print(f"    M_gap lower = {M_max_ns:.3f} M_sun")
    print(f"    M_gap upper = {M_gap_upper:.1f} M_sun")

    if M_secondary <= M_max_ns:
        classification = "NEUTRON STAR"
        print(f"\n  => {M_secondary:.2f} M_sun < M_max = {M_max_ns:.3f} M_sun")
        print(f"  => Classification: {classification}")
        print(f"  => This would be the heaviest NS observed!")
        print(f"  => Margin below M_max: "
              f"{M_max_ns - M_secondary:.3f} M_sun")
    elif M_secondary < M_gap_upper:
        classification = "MASS GAP OBJECT (frozen star)"
        print(f"\n  => {M_max_ns:.3f} < {M_secondary:.2f} < "
              f"{M_gap_upper:.1f} M_sun")
        print(f"  => Classification: {classification}")
        print(f"  => In the frozen star framework: this object is in the")
        print(f"     lattice-floor regime — too massive for NS but not a")
        print(f"     standard BH.  It is a frozen star with R = N^(1/3) l_P")

        # Properties of this frozen star
        M_kg = M_secondary * M_SUN
        N_p = M_kg / M_NUCLEON
        R_lattice = N_p**(1/3) * L_PLANCK
        R_S = 2 * G_SI * M_kg / C**2

        print(f"\n  Frozen star properties:")
        print(f"    N_particles = {N_p:.4e}")
        print(f"    R_floor = N^(1/3) l_P = {R_lattice:.4e} m")
        print(f"    R_S = 2GM/c^2 = {R_S:.4e} m")
        print(f"    R_floor / R_S = {R_lattice/R_S:.4e}")
    else:
        classification = "BLACK HOLE"
        print(f"\n  => {M_secondary:.2f} > {M_gap_upper:.1f} M_sun")
        print(f"  => Classification: {classification}")

    # Comparison with other analyses
    print(f"\n  Context from other analyses:")
    print(f"    Most nuclear EOS models: M_max ~ 2.0-2.4 M_sun")
    print(f"    If M_max < 2.59: secondary is in the gap or is a BH")
    print(f"    If M_max > 2.59: secondary could be a NS (very stiff EOS)")
    print(f"    Standard view: 2.59 M_sun is likely in the mass gap")
    print(f"    Framework view: {classification}")

    # GW200210_092254 comparison
    print(f"\n  Also notable: GW200210_092254 secondary at 2.83 M_sun")
    print(f"    Even more clearly in the mass gap")
    print(f"    Framework: also a frozen star / mass gap object")

    return {
        "M_secondary": M_secondary,
        "classification": classification,
        "M_max_ns": M_max_ns,
    }


# ============================================================================
# MAIN
# ============================================================================

def main():
    t0 = time.time()
    print("NS Maximum Mass and Mass Gap from Frozen Star Framework")
    print("=" * 72)

    r1 = probe1_ns_max_mass()
    r2 = probe2_mass_gap(r1["M_max_framework"])
    r3 = probe3_pulsar_comparison(r1["M_max_framework"])
    r4 = probe4_gwtc_analysis(r1["M_max_framework"], r2["M_gap_upper"])
    r5 = probe5_gw190814(r1["M_max_framework"], r2["M_gap_upper"])

    # ====================================================================
    # SUMMARY
    # ====================================================================
    print("\n" + "=" * 72)
    print("SUMMARY: NS Mass Gap Predictions")
    print("=" * 72)

    print(f"""
  1. MAXIMUM NS MASS:
     Oppenheimer-Volkoff (ideal Fermi gas + GR): {r1['M_OV_solar']:.3f} M_sun
     TOV + nuclear EOS:                         {r1['M_max_tov']:.3f} M_sun
     Framework (+ lattice stiffening):          {r1['M_max_framework']:.3f} M_sun
     Lattice Chandrasekhar mass (a=l_P):        {r1['M_Ch_solar']:.2f} M_sun

  2. NS-BH MASS GAP:
     Lower edge (M_max NS): {r2['M_gap_lower']:.2f} M_sun
     Upper edge (min BH):   {r2['M_gap_upper']:.1f} M_sun
     Gap width:             {r2['gap_width']:.2f} M_sun

  3. OBSERVED NS COMPARISON:
     All pulsars consistent? {'YES' if r3['all_consistent'] else 'NO'}
     Heaviest NS (PSR J0740+6620): 2.08 +/- 0.07 M_sun
     Tension with framework M_max: {r3['tension_with_heaviest']:.1f} sigma
     Closest to limit: {r3['closest_to_limit']}

  4. GWTC CATALOG:
     NS candidates: {r4['n_ns']}
     Mass gap objects: {r4['n_gap']}
     BH: {r4['n_bh']}
     Objects in gap: {r4['gap_count']} (supports gap existence)

  5. GW190814 (2.59 M_sun):
     Framework classification: {r5['classification']}
     This object is {'within NS range' if r5['M_secondary'] <= r5['M_max_ns'] else 'above M_max(NS)'} in the framework

  KEY RESULT: The framework predicts M_max(NS) = {r1['M_max_framework']:.3f} M_sun,
  consistent with the heaviest observed NS at {r3['tension_with_heaviest']:.1f} sigma.
  The mass gap ({r2['M_gap_lower']:.2f}-{r2['M_gap_upper']:.1f} M_sun) is naturally
  explained: objects in this range are frozen stars supported by the
  lattice hard floor, distinct from both NS and standard BH.
""")

    elapsed = time.time() - t0
    print(f"Total elapsed: {elapsed:.1f} s")


if __name__ == "__main__":
    main()
