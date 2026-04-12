#!/usr/bin/env python3
"""Gravitational decoherence rate for the diamond NV center experiment.

===========================================================================
Computes the SPECIFIC decoherence rate the discrete-graph framework
predicts for the BMV-class diamond NV experiment. Gives the experimentalist
a concrete number to aim for.

Seven computations:
  1. Experimental parameters from the diamond NV experiment card
  2. Framework decoherence rate: gamma_grav = (Gm^2)/(hbar*d) * f(geometry)
  3. Geometry factor f from the lattice Poisson propagator
  4. Penrose-Diosi rate and the framework's modification
  5. Numerical evaluation for diamond NV parameters
  6. Lattice correction at Planck spacing
  7. Modified rate as a function of Born-rule parameter beta

PStack experiment: frontier-grav-decoherence-rate
===========================================================================
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.special import erf
from scipy.integrate import quad


# =====================================================================
# Physical constants (SI)
# =====================================================================
HBAR     = 1.054571817e-34      # J s
G_N      = 6.67430e-11          # m^3 kg^-1 s^-2
C        = 2.99792458e8         # m/s
K_B      = 1.380649e-23         # J/K
L_PL     = 1.616255e-35         # m  (Planck length)
M_PL     = 2.176434e-8          # kg (Planck mass)
EV_TO_J  = 1.602176634e-19      # J per eV


# =====================================================================
# Section 1: Diamond NV experiment parameters
# =====================================================================

# BMV-class experiment parameters (from experiment card + literature)
BMV_PARAMS = {
    "name": "BMV (Bose et al. 2017)",
    "m_kg": 1e-14,           # 10 pg diamond microsphere
    "d_m": 200e-6,           # 200 um center-to-center separation
    "delta_x_m": 1e-6,       # ~1 um superposition width (Stern-Gerlach split)
    "sigma_m": 0.5e-6,       # wavepacket width (ground state of trap)
    "T_interact_s": 2.0,     # interaction time
    "T_coherence_needed_s": 2.0,  # must maintain coherence for this long
}

# Also consider variations
EXPERIMENT_CONFIGS = [
    {
        "name": "BMV original (Bose 2017)",
        "m_kg": 1e-14,
        "d_m": 200e-6,
        "delta_x_m": 250e-6,     # large superposition in original proposal
        "sigma_m": 0.5e-6,
        "T_s": 2.0,
    },
    {
        "name": "Aspelmeyer (tabletop, near-term)",
        "m_kg": 1e-12,
        "d_m": 100e-6,
        "delta_x_m": 10e-6,
        "sigma_m": 1e-6,
        "T_s": 1.0,
    },
    {
        "name": "Conservative NV setup",
        "m_kg": 1e-14,
        "d_m": 200e-6,
        "delta_x_m": 1e-6,
        "sigma_m": 0.5e-6,
        "T_s": 2.0,
    },
    {
        "name": "Optimistic next-decade",
        "m_kg": 1e-10,
        "d_m": 50e-6,
        "delta_x_m": 1e-6,
        "sigma_m": 1e-6,
        "T_s": 10.0,
    },
]


def section_1_parameters():
    """Print experimental parameters."""
    print("=" * 78)
    print("1. DIAMOND NV EXPERIMENT PARAMETERS")
    print("=" * 78)
    print()

    p = BMV_PARAMS
    print(f"  Reference configuration: {p['name']}")
    print(f"  Mass per microsphere:       m = {p['m_kg']:.0e} kg")
    print(f"  Center-to-center distance:  d = {p['d_m']*1e6:.0f} um")
    print(f"  Superposition width:        dx = {p['delta_x_m']*1e6:.1f} um")
    print(f"  Wavepacket width:           sigma = {p['sigma_m']*1e6:.1f} um")
    print(f"  Interaction time:           T = {p['T_interact_s']:.1f} s")
    print(f"  Required coherence time:    T_coh > {p['T_coherence_needed_s']:.1f} s")
    print()

    # Derived quantities
    m = p["m_kg"]
    d = p["d_m"]
    dx = p["delta_x_m"]

    r_S = 2 * G_N * m / C**2
    print(f"  Derived quantities:")
    print(f"    Schwarzschild radius:     r_S = 2Gm/c^2 = {r_S:.4e} m")
    print(f"    r_S / d = {r_S/d:.4e}")
    print(f"    r_S / dx = {r_S/dx:.4e}")
    print(f"    Gm^2/(hbar*d) = {G_N*m**2/(HBAR*d):.4e} Hz")
    print(f"    Gm^2/(hbar*dx) = {G_N*m**2/(HBAR*dx):.4e} Hz")
    print()


# =====================================================================
# Section 2: Framework decoherence rate
# =====================================================================

def penrose_diosi_rate(m: float, delta_x: float) -> float:
    """Penrose-Diosi gravitational decoherence rate.

    gamma_PD = G * m^2 / (hbar * delta_x)

    This is the rate at which a mass m in a superposition of separation
    delta_x loses coherence due to the gravitational self-energy difference
    between the two branches.

    Args:
        m: mass in kg
        delta_x: superposition separation in meters

    Returns:
        Decoherence rate in Hz (1/s)
    """
    return G_N * m**2 / (HBAR * delta_x)


def geometry_factor_spheres(delta_x: float, R: float) -> float:
    """Geometry factor f for two uniform spheres displaced by delta_x.

    For two identical uniform spheres of radius R displaced by delta_x,
    the gravitational self-energy difference (Penrose's E_G) is:

    E_G = (6 G m^2) / (5 R) * [1 - (5/(16)) * (delta_x/R)^2 + ...]
        for delta_x << R

    E_G = G m^2 / delta_x * [1 - (3/5)(R/delta_x)^2 + ...]
        for delta_x >> R

    The geometry factor is the ratio to the point-particle result:
    f = E_G / (G m^2 / delta_x)

    For the BMV experiment: delta_x ~ 1 um, R ~ 10 um (for 10 pg diamond)
    so delta_x << R and we need the near-field formula.

    Args:
        delta_x: displacement of the superposition (m)
        R: sphere radius (m)

    Returns:
        Dimensionless geometry factor f
    """
    if delta_x < 1e-30:
        return 0.0

    ratio = delta_x / R

    if ratio < 0.5:
        # Small displacement limit (Penrose's overlap integral for spheres)
        # E_G = (G m^2 / R) * (6/5) * [1 - (5/16)(delta_x/R)^2
        #        - (5/48)(delta_x/R)^4 + ...]
        # f = E_G / (G m^2 / delta_x) = (6/5) * (delta_x/R) * [1 - ...]
        f = (6.0 / 5.0) * ratio * (1.0 - (5.0/16.0) * ratio**2)
    elif ratio > 5.0:
        # Large displacement limit
        # E_G ~ G m^2 / delta_x * [1 - (3/5)(R/delta_x)^2]
        f = 1.0 - (3.0/5.0) * (R / delta_x)**2
    else:
        # Intermediate: numerical integration of the overlap integral
        # E_G = G * integral d^3r d^3r' [rho_L(r) - rho_R(r)] [rho_L(r') - rho_R(r')] / |r-r'|
        # For uniform spheres, use the analytical result (Diosi 1987):
        f = _sphere_overlap_exact(delta_x, R)

    return f


def _sphere_overlap_exact(delta_x: float, R: float) -> float:
    """Exact geometry factor for two overlapping uniform spheres.

    Uses the analytical result for the gravitational self-energy of the
    difference density rho_L - rho_R for two uniform spheres of radius R
    separated by delta_x.

    The Newtonian self-energy integral:
    E_G = G * integral |rho_L(r) - rho_R(r)|^2 / |r - r'| d^3r d^3r'

    For uniform spheres, the density difference has support in the
    non-overlapping regions. The result (Diosi 1987, Penrose 2014):

    For delta_x < 2R (overlapping):
    E_G = (G m^2 / R) * h(delta_x / R)

    where h(u) = (6/5) u - (1/2) u^3 + (3/16) u^5 - (1/60) u^7
    (valid for u = delta_x/R < 2)

    f = E_G / (G m^2 / delta_x) = R * h(delta_x/R) / delta_x
    """
    u = delta_x / R
    if u >= 2.0:
        # Non-overlapping: E_G = G m^2 / delta_x * [1 - 3R^2/(5 delta_x^2)]
        return 1.0 - 3.0 * R**2 / (5.0 * delta_x**2)

    # Overlapping regime: polynomial formula
    h_u = (6.0/5.0) * u - 0.5 * u**3 + (3.0/16.0) * u**5 - (1.0/60.0) * u**7
    f = R * h_u / delta_x
    return f


def framework_decoherence_rate(m: float, delta_x: float, sigma: float,
                                R: float) -> dict:
    """Full framework gravitational decoherence rate.

    Combines:
    1. Penrose-Diosi base rate: gamma_PD = G m^2 / (hbar * delta_x)
    2. Geometry factor: f(delta_x, R) from sphere overlap
    3. Wavepacket smearing: when sigma > 0, the density is Gaussian,
       not a point. This modifies the overlap integral.
    4. Self-consistent correction: from iterating the Poisson equation
       (approach 3 of frontier_accessible_prediction.py)

    Args:
        m: mass in kg
        delta_x: superposition separation in meters
        sigma: wavepacket width in meters
        R: physical sphere radius in meters

    Returns:
        Dictionary with all rate components
    """
    # Base Penrose-Diosi rate (point particles)
    gamma_pd = penrose_diosi_rate(m, delta_x)

    # Geometry factor for finite-size spheres
    f_geom = geometry_factor_spheres(delta_x, R)

    # Wavepacket smearing factor
    # For Gaussian wavepackets of width sigma, the overlap integral
    # involves erf functions. The key modification: the density is
    # rho(x) ~ exp(-(x-x_0)^2 / (2 sigma^2)) instead of a delta function.
    #
    # The decoherence rate for Gaussian wavepackets:
    # gamma_gauss = (G m^2) / (hbar * sqrt(2*pi) * sigma)
    #     * [1 - exp(-delta_x^2 / (4 sigma^2))]
    #
    # For delta_x >> sigma: gamma_gauss -> gamma_PD * sigma/delta_x * correction
    # For delta_x << sigma: gamma_gauss -> G m^2 delta_x^2 / (hbar * (2pi)^{1/2} * 4 sigma^3)
    #
    # More precisely, from Diosi (1987) for Gaussian mass distributions:
    if sigma > 1e-30 and delta_x > 1e-30:
        # The self-energy difference for two Gaussians separated by delta_x:
        # E_G = G m^2 / (sqrt(pi) sigma) * [1 - exp(-delta_x^2/(4 sigma^2))]
        # gamma = E_G / hbar
        gamma_gauss = (G_N * m**2 / (math.sqrt(math.pi) * sigma * HBAR)) * (
            1.0 - math.exp(-delta_x**2 / (4.0 * sigma**2))
        )
        f_gauss = gamma_gauss / gamma_pd if gamma_pd > 0 else 0
    else:
        gamma_gauss = gamma_pd
        f_gauss = 1.0

    # Self-consistent correction (from frontier_accessible_prediction.py Approach 3)
    # gamma_SC = gamma * [1 + c_1 * r_S / sigma + ...]
    # where r_S = 2Gm/c^2, c_1 ~ O(1) (computed as ~0.5 from 1D model)
    r_S = 2.0 * G_N * m / C**2
    c_1 = 0.5  # from 1D self-consistent iteration
    sc_correction = c_1 * r_S / sigma if sigma > 0 else 0
    gamma_sc = gamma_gauss * (1.0 + sc_correction)

    # Combined rate with geometry factor
    # For physical spheres with Gaussian wavepackets:
    # Use the Gaussian rate (which already accounts for finite extent)
    # The sphere geometry factor applies when the wavepacket is localized
    # within the sphere (sigma << R).
    if sigma < R:
        gamma_physical = gamma_pd * f_geom * (1.0 + sc_correction)
    else:
        gamma_physical = gamma_gauss * (1.0 + sc_correction)

    return {
        "gamma_pd": gamma_pd,
        "gamma_gauss": gamma_gauss,
        "gamma_sc": gamma_sc,
        "gamma_physical": gamma_physical,
        "f_geom": f_geom,
        "f_gauss": f_gauss,
        "sc_correction": sc_correction,
        "r_S": r_S,
    }


def section_2_framework_rate():
    """Compute the framework decoherence rate."""
    print("=" * 78)
    print("2. FRAMEWORK DECOHERENCE RATE: gamma = (Gm^2)/(hbar*d) * f(geometry)")
    print("=" * 78)
    print()

    print("  The framework treats gravity as sourced by |psi|^2. For a mass in")
    print("  a superposition of two locations separated by delta_x, the two")
    print("  branches source different gravitational fields. The overlap between")
    print("  these fields decays exponentially, giving decoherence.")
    print()
    print("  Three levels of approximation:")
    print("    Level 0 (Penrose-Diosi):  gamma_PD = G m^2 / (hbar * delta_x)")
    print("    Level 1 (+ geometry):     gamma = gamma_PD * f(delta_x, R)")
    print("    Level 2 (+ wavepacket):   gamma = G m^2 / (sqrt(pi)*sigma*hbar)")
    print("                              * [1 - exp(-delta_x^2/(4*sigma^2))]")
    print("    Level 3 (+ self-consist): gamma *= [1 + c_1 * r_S/sigma + ...]")
    print()

    # Compute for BMV parameters
    p = BMV_PARAMS
    m = p["m_kg"]
    d = p["d_m"]
    dx = p["delta_x_m"]
    sigma = p["sigma_m"]

    # Diamond microsphere radius: rho_diamond = 3500 kg/m^3
    # m = (4/3) pi R^3 rho => R = (3m/(4 pi rho))^{1/3}
    rho_diamond = 3500.0  # kg/m^3
    R = (3.0 * m / (4.0 * math.pi * rho_diamond))**(1.0/3.0)

    print(f"  Diamond microsphere radius: R = {R*1e6:.2f} um")
    print(f"  (from m = {m:.0e} kg, rho = {rho_diamond:.0f} kg/m^3)")
    print()

    rates = framework_decoherence_rate(m, dx, sigma, R)

    print(f"  Penrose-Diosi rate (point particles):")
    print(f"    gamma_PD = G m^2 / (hbar * delta_x)")
    print(f"    = {G_N:.4e} * ({m:.0e})^2 / ({HBAR:.4e} * {dx:.0e})")
    print(f"    = {rates['gamma_pd']:.6e} Hz")
    print(f"    tau_PD = 1/gamma_PD = {1.0/rates['gamma_pd']:.6e} s")
    print()

    print(f"  Geometry factor (finite spheres):")
    print(f"    delta_x/R = {dx/R:.4f}")
    print(f"    f_geom = {rates['f_geom']:.6f}")
    print()

    print(f"  Gaussian wavepacket rate:")
    print(f"    gamma_gauss = G m^2 / (sqrt(pi)*sigma*hbar)")
    print(f"                  * [1 - exp(-delta_x^2/(4*sigma^2))]")
    print(f"    = {rates['gamma_gauss']:.6e} Hz")
    print(f"    tau_gauss = {1.0/rates['gamma_gauss']:.6e} s")
    print(f"    ratio to PD: {rates['f_gauss']:.6f}")
    print()

    print(f"  Self-consistent correction:")
    print(f"    r_S = {rates['r_S']:.4e} m")
    print(f"    r_S / sigma = {rates['r_S']/sigma:.4e}")
    print(f"    correction = c_1 * r_S / sigma = {rates['sc_correction']:.4e}")
    print(f"    gamma_SC = {rates['gamma_sc']:.6e} Hz")
    print()

    print(f"  Physical rate (best estimate):")
    print(f"    gamma_phys = {rates['gamma_physical']:.6e} Hz")
    print(f"    tau_phys = {1.0/rates['gamma_physical']:.6e} s")
    print()

    return rates, R


# =====================================================================
# Section 3: Geometry factor from lattice Poisson propagator
# =====================================================================

def section_3_geometry_factor():
    """Compute geometry factor f from the lattice Poisson propagator."""
    print("=" * 78)
    print("3. GEOMETRY FACTOR FROM THE LATTICE PROPAGATOR")
    print("=" * 78)
    print()

    print("  On a lattice, the gravitational potential is the Poisson solution.")
    print("  For two mass sources at positions x_L and x_R, the gravitational")
    print("  field overlap integral determines the decoherence rate.")
    print()
    print("  On a 1D lattice of N sites with spacing a:")
    print("    phi(i) = -G * sum_j rho(j) * K^{-1}(i,j)")
    print("  where K is the discrete Laplacian.")
    print()
    print("  The self-energy difference between the two branches is:")
    print("    E_G = integral d^3r [phi_L(r) - phi_R(r)]^2 / (8 pi G)")
    print("  This integral, on the lattice, gives the geometry factor f.")
    print()

    # 1D lattice computation
    N_values = [50, 100, 200, 500]
    delta_n_values = [2, 4, 8, 16, 32]

    print(f"  1D LATTICE COMPUTATION")
    print(f"  {'N':>6s}  {'delta_n':>8s}  {'f_lattice':>12s}  "
          f"{'f_continuum':>12s}  {'relative_diff':>14s}")
    print("  " + "-" * 60)

    for N in N_values:
        # Build 1D Poisson Green's function
        # K^{-1}(i,j) = -min(i,j) * (N - max(i,j)) / N  (Dirichlet BCs)
        G_poisson = np.zeros((N, N))
        for i in range(1, N - 1):
            for j in range(1, N - 1):
                G_poisson[i, j] = -min(i, j) * (N - max(i, j)) / float(N)

        for delta_n in delta_n_values:
            center = N // 2
            L = center - delta_n // 2
            R_pos = center + delta_n // 2

            if L < 1 or R_pos >= N - 1:
                continue

            # Field from source at L
            phi_L = G_poisson[:, L]
            # Field from source at R
            phi_R = G_poisson[:, R_pos]

            # Self-energy difference (discretized integral)
            delta_phi = phi_L - phi_R
            E_G_lattice = np.sum(delta_phi**2)

            # Continuum: for two point sources separated by delta_n on a 1D chain
            # E_G_cont = G m^2 / delta_n (up to factors)
            # On lattice: phi(i) ~ -|i-j| for 1D Poisson
            # E_G should scale as delta_n for small delta_n (overlapping regime)
            # and as 1/delta_n for large delta_n

            # Geometry factor: ratio to point-source result
            # For 1D: E_G_point = G m^2 * sum_i [1/|i-L| - 1/|i-R|]^2
            # Normalize by E_G for well-separated sources (delta_n = N//4)
            phi_ref = G_poisson[:, N // 4]
            E_G_ref = np.sum(phi_ref**2)

            f_lattice = E_G_lattice / (delta_n**2) if delta_n > 0 else 0

            # Continuum 1D prediction: f ~ delta_n / N (finite size)
            f_cont = delta_n / float(N)

            rel_diff = abs(f_lattice - f_cont) / f_cont if f_cont > 0 else 0

            print(f"  {N:6d}  {delta_n:8d}  {f_lattice:12.6f}  "
                  f"{f_cont:12.6f}  {rel_diff:14.6f}")

    print()

    # 3D analytical result for Gaussian wavepackets
    print("  3D ANALYTICAL RESULT (Gaussian wavepackets)")
    print()
    print("  For two Gaussian mass distributions of width sigma, separated by delta_x:")
    print("    E_G = G m^2 / (sqrt(pi) * sigma) * [1 - exp(-delta_x^2 / (4 sigma^2))]")
    print()
    print("  Limiting cases:")
    print("    delta_x >> sigma: E_G -> G m^2 / (sqrt(pi) * sigma)")
    print("                      (saturates at self-energy of single Gaussian)")
    print("    delta_x << sigma: E_G -> G m^2 * delta_x^2 / (4 sqrt(pi) * sigma^3)")
    print("                      (quadratic growth -- slow decoherence)")
    print()

    # Compute for a range of delta_x / sigma
    dx_over_sigma = np.array([0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0])
    print(f"  {'delta_x/sigma':>14s}  {'E_G / (Gm^2/sigma)':>20s}  {'f = E_G/(Gm^2/delta_x)':>22s}")
    print("  " + "-" * 60)

    for r in dx_over_sigma:
        E_G_norm = (1.0 / math.sqrt(math.pi)) * (1.0 - math.exp(-r**2 / 4.0))
        f = E_G_norm * (r)  # ratio to point-source result Gm^2/delta_x
        print(f"  {r:14.2f}  {E_G_norm:20.8f}  {f:22.8f}")

    print()
    return {}


# =====================================================================
# Section 4: Penrose-Diosi rate and framework modification
# =====================================================================

def section_4_penrose_diosi_comparison():
    """Compare Penrose-Diosi to framework prediction."""
    print("=" * 78)
    print("4. PENROSE-DIOSI RATE vs FRAMEWORK MODIFICATION")
    print("=" * 78)
    print()

    print("  PENROSE-DIOSI (1987/1996):")
    print("    gamma_PD = G (Delta m)^2 / (hbar * d)")
    print("    where Delta m = mass difference between branches (= m for cat state)")
    print("    and d = separation of the superposition")
    print()
    print("  FRAMEWORK MODIFICATION:")
    print("    The framework solves the Poisson equation self-consistently for")
    print("    the quantum density |psi|^2. This gives TWO modifications:")
    print()
    print("    (a) Gaussian smearing: replace 1/d with erf integral")
    print("        gamma = (Gm^2)/(sqrt(pi)*sigma*hbar) * [1 - exp(-d^2/(4 sigma^2))]")
    print()
    print("    (b) Self-consistent backreaction: iterate phi -> psi -> rho -> phi")
    print("        gamma -> gamma * [1 + c_1 * r_S/sigma]")
    print("        where r_S = 2Gm/c^2 is the Schwarzschild radius")
    print()
    print("    The LEADING term is (a). Modification (b) is r_S/sigma ~ 10^{-37}")
    print("    for m = 10^{-14} kg, sigma = 1 um.")
    print()

    # Compute for all experiment configurations
    print(f"  {'Configuration':<30s}  {'gamma_PD (Hz)':>14s}  {'gamma_FW (Hz)':>14s}  "
          f"{'tau_PD (s)':>12s}  {'tau_FW (s)':>12s}  {'ratio':>8s}")
    print("  " + "-" * 100)

    rho_diamond = 3500.0

    for cfg in EXPERIMENT_CONFIGS:
        m = cfg["m_kg"]
        dx = cfg["delta_x_m"]
        sigma = cfg["sigma_m"]
        R = (3.0 * m / (4.0 * math.pi * rho_diamond))**(1.0/3.0)

        rates = framework_decoherence_rate(m, dx, sigma, R)

        tau_pd = 1.0 / rates["gamma_pd"] if rates["gamma_pd"] > 0 else float('inf')
        tau_fw = 1.0 / rates["gamma_physical"] if rates["gamma_physical"] > 0 else float('inf')
        ratio = rates["gamma_physical"] / rates["gamma_pd"] if rates["gamma_pd"] > 0 else 0

        print(f"  {cfg['name']:<30s}  {rates['gamma_pd']:14.4e}  "
              f"{rates['gamma_physical']:14.4e}  {tau_pd:12.4e}  {tau_fw:12.4e}  {ratio:8.4f}")

    print()

    # Key comparison: required coherence time vs decoherence time
    print("  FEASIBILITY CHECK: Is the decoherence time > interaction time?")
    print()
    print(f"  {'Configuration':<30s}  {'tau_decoh (s)':>14s}  {'T_interact (s)':>14s}  "
          f"{'tau/T':>10s}  {'feasible?':>10s}")
    print("  " + "-" * 84)

    for cfg in EXPERIMENT_CONFIGS:
        m = cfg["m_kg"]
        dx = cfg["delta_x_m"]
        sigma = cfg["sigma_m"]
        T = cfg["T_s"]
        R = (3.0 * m / (4.0 * math.pi * rho_diamond))**(1.0/3.0)

        rates = framework_decoherence_rate(m, dx, sigma, R)
        tau = 1.0 / rates["gamma_physical"] if rates["gamma_physical"] > 0 else float('inf')
        ratio = tau / T
        feasible = "YES" if ratio > 1.0 else "MARGINAL" if ratio > 0.1 else "NO"

        print(f"  {cfg['name']:<30s}  {tau:14.4e}  {T:14.1f}  "
              f"{ratio:10.2e}  {feasible:>10s}")

    print()
    print("  NOTE: For the BMV experiment to work, other decoherence sources")
    print("  (thermal, electromagnetic, vibrational) must ALSO be suppressed")
    print("  below the gravitational signal. The gravitational decoherence rate")
    print("  is the SIGNAL, not the noise. The experiment measures WHETHER")
    print("  gravity creates entanglement (correlation between the two masses),")
    print("  not whether gravity causes decoherence (which it does, but that's")
    print("  a separate channel).")
    print()

    return {}


# =====================================================================
# Section 5: Numerical evaluation for diamond NV parameters
# =====================================================================

def section_5_numerical_evaluation():
    """Compute specific numbers for the diamond NV experiment."""
    print("=" * 78)
    print("5. SPECIFIC NUMBERS FOR THE DIAMOND NV EXPERIMENT")
    print("=" * 78)
    print()

    m = 1e-14       # 10 pg
    d = 200e-6       # 200 um
    dx = 1e-6        # 1 um superposition (conservative)
    sigma = 0.5e-6   # wavepacket width
    T = 2.0          # interaction time
    rho_diamond = 3500.0
    R = (3.0 * m / (4.0 * math.pi * rho_diamond))**(1.0/3.0)

    print(f"  Parameters:")
    print(f"    m = {m:.0e} kg ({m*1e15:.1f} fg = {m/(1.66054e-27):.2e} amu)")
    print(f"    d = {d*1e6:.0f} um (center-to-center)")
    print(f"    delta_x = {dx*1e6:.1f} um (superposition separation)")
    print(f"    sigma = {sigma*1e6:.1f} um (wavepacket width)")
    print(f"    R = {R*1e6:.2f} um (diamond sphere radius)")
    print(f"    T = {T:.1f} s (interaction time)")
    print()

    # === The key number: gravitational entanglement phase ===
    # For two masses each in superposition of delta_x at separation d:
    # The entanglement phase accumulates as:
    #   Phi_ent = G m^2 T / hbar * [1/(d-delta_x) - 1/d]
    # For delta_x << d:
    #   Phi_ent ~ G m^2 T delta_x / (hbar d^2)

    d_near = d - dx
    d_far = d + dx
    Phi_ent_exact = G_N * m**2 * T / HBAR * abs(1.0/d_near - 1.0/d_far)
    Phi_ent_approx = G_N * m**2 * T * 2 * dx / (HBAR * d**2)

    print(f"  === ENTANGLEMENT PHASE (the signal) ===")
    print(f"    Phi_ent = G m^2 T / hbar * |1/(d-dx) - 1/(d+dx)|")
    print(f"    = {Phi_ent_exact:.6e} rad (exact)")
    print(f"    ~ G m^2 T * 2*dx / (hbar * d^2) = {Phi_ent_approx:.6e} rad (approx)")
    print(f"    Detectable (Phi > 0.01 rad): {'YES' if Phi_ent_exact > 0.01 else 'NO'}")
    print()

    # === The decoherence rate ===
    rates = framework_decoherence_rate(m, dx, sigma, R)

    print(f"  === GRAVITATIONAL DECOHERENCE RATE ===")
    print()
    print(f"  Level 0: Penrose-Diosi (point particles)")
    print(f"    gamma_PD = G m^2 / (hbar * delta_x)")
    print(f"    = {rates['gamma_pd']:.6e} Hz")
    print(f"    tau_PD = {1.0/rates['gamma_pd']:.6e} s")
    print()

    print(f"  Level 1: Gaussian wavepackets")
    print(f"    gamma_gauss = (G m^2) / (sqrt(pi)*sigma*hbar) * [1 - exp(-dx^2/(4 sigma^2))]")
    exp_factor = 1.0 - math.exp(-dx**2 / (4.0 * sigma**2))
    print(f"    exp factor = 1 - exp(-{dx**2/(4*sigma**2):.4f}) = {exp_factor:.6f}")
    print(f"    gamma_gauss = {rates['gamma_gauss']:.6e} Hz")
    print(f"    tau_gauss = {1.0/rates['gamma_gauss']:.6e} s")
    print()

    print(f"  Level 2: + self-consistent correction")
    print(f"    correction = c_1 * r_S / sigma = 0.5 * {rates['r_S']:.4e} / {sigma:.0e}")
    print(f"    = {rates['sc_correction']:.4e}")
    print(f"    gamma_SC = {rates['gamma_sc']:.6e} Hz")
    print(f"    (correction is negligible: {rates['sc_correction']:.2e})")
    print()

    print(f"  Level 3: Physical rate (with geometry)")
    print(f"    gamma_phys = {rates['gamma_physical']:.6e} Hz")
    print(f"    tau_phys = {1.0/rates['gamma_physical']:.6e} s")
    print()

    # === Comparison to required coherence time ===
    print(f"  === COMPARISON TO EXPERIMENTAL REQUIREMENTS ===")
    print()
    tau = 1.0 / rates['gamma_physical']
    print(f"  Gravitational decoherence time: tau = {tau:.4e} s")
    print(f"  Required coherence time:        T   = {T:.1f} s")
    print(f"  Ratio tau/T = {tau/T:.4e}")
    print()

    if tau > T:
        print(f"  RESULT: The gravitational decoherence time ({tau:.2e} s) EXCEEDS")
        print(f"  the required interaction time ({T:.1f} s) by a factor of {tau/T:.2e}.")
        print(f"  The gravitational decoherence itself is NOT the bottleneck.")
    else:
        print(f"  RESULT: The gravitational decoherence time ({tau:.2e} s) is SHORTER")
        print(f"  than the required interaction time ({T:.1f} s).")
        print(f"  Gravitational decoherence will suppress the entanglement signal.")

    print()

    # === What the experimentalist should target ===
    print(f"  === TARGET FOR EXPERIMENTALISTS ===")
    print()
    print(f"  The framework predicts:")
    print(f"    gamma_grav = {rates['gamma_physical']:.4e} Hz")
    print(f"    = {rates['gamma_physical']*1e3:.4e} mHz")
    print()
    print(f"  This means the total decoherence rate from ALL sources must satisfy:")
    print(f"    gamma_total < 1/T = {1.0/T:.2f} Hz = {1.0/T*1e3:.0f} mHz")
    print()
    gamma_ratio = rates['gamma_physical'] / (1.0/T)
    if gamma_ratio > 1.0:
        print(f"  WARNING: The gravitational decoherence ALONE ({rates['gamma_physical']:.1f} Hz)")
        print(f"  EXCEEDS the coherence budget ({1.0/T:.2f} Hz) by a factor of {gamma_ratio:.0f}.")
        print(f"  With these parameters (dx = {dx*1e6:.0f} um), the superposition")
        print(f"  decoheres gravitationally before the entanglement can accumulate.")
        print(f"  This is WHY the original BMV proposal uses dx = 250 um >> sigma")
        print(f"  with d = 200 um: larger dx gives more entanglement phase per unit")
        print(f"  decoherence. The experiment needs the RATIO Phi_ent / gamma*T > 1.")
    else:
        print(f"  The gravitational decoherence is {gamma_ratio*100:.2e}% of the budget.")
    print()
    print(f"  The gravitational entanglement phase to measure:")
    print(f"    Phi_ent = {Phi_ent_exact:.4e} rad")
    print()

    # For the larger-displacement BMV proposal
    # Original BMV: two masses each in dx=250um superposition, d=200um apart
    # The arms overlap: d_near = d - dx = 200 - 250 = -50 um
    # This means the near arms CROSS, so we use d_near = |d - dx| as minimum
    # approach. In the original proposal the geometry is:
    #   mass1: at x=0 in superposition of -dx/2 and +dx/2
    #   mass2: at x=d in superposition of d-dx/2 and d+dx/2
    # Closest approach: |d - dx| = 200 - 250 = -50 -> use small cutoff
    # Actually in BMV the superposition is along the line joining the masses
    # d_near = d - dx_1/2 - dx_2/2 for same-side arms
    dx_large = 250e-6
    # For each mass in dx/2 superposition (Stern-Gerlach):
    d_near2 = d - dx_large  # closest approach of near arms
    d_far2 = d + dx_large    # farthest approach of far arms
    if d_near2 > 1e-9:
        Phi_large = G_N * m**2 * T / HBAR * abs(1.0/d_near2 - 1.0/d_far2)
    else:
        # Arms overlap: use d_near = min feasible = 10 um
        d_near2 = 10e-6
        Phi_large = G_N * m**2 * T / HBAR * abs(1.0/d_near2 - 1.0/d_far2)
    print(f"  With original BMV parameters (delta_x = 250 um):")
    print(f"    d_near = {d_near2*1e6:.0f} um, d_far = {d_far2*1e6:.0f} um")
    print(f"    Phi_ent = {Phi_large:.4e} rad")
    print(f"    {'DETECTABLE' if Phi_large > 0.01 else 'too small'}")
    print()

    return {
        "gamma_phys": rates['gamma_physical'],
        "tau_phys": tau,
        "Phi_ent": Phi_ent_exact,
        "Phi_ent_large_dx": Phi_large,
    }


# =====================================================================
# Section 6: Lattice correction at Planck spacing
# =====================================================================

def section_6_lattice_correction():
    """Compute the lattice correction to the decoherence rate."""
    print("=" * 78)
    print("6. LATTICE CORRECTION TO DECOHERENCE RATE")
    print("=" * 78)
    print()

    print("  On a discrete lattice of spacing l_P, the gravitational potential")
    print("  has corrections at short distances:")
    print("    phi(r) = -(Gm/r) * [1 + alpha_lat * (l_P/r)^2 + ...]")
    print()
    print("  The decoherence rate inherits this correction:")
    print("    gamma = gamma_continuum * [1 + alpha_lat * (l_P/delta_x)^2 + ...]")
    print()

    m = 1e-14
    dx = 1e-6
    sigma = 0.5e-6
    d = 200e-6
    rho_diamond = 3500.0
    R = (3.0 * m / (4.0 * math.pi * rho_diamond))**(1.0/3.0)

    rates = framework_decoherence_rate(m, dx, sigma, R)
    gamma_base = rates["gamma_physical"]

    # Lattice correction: alpha_lat * (l_P / delta_x)^2
    # alpha_lat ~ O(1) from the dispersion relation analysis
    alpha_lat = 1.0  # order-unity coefficient

    lattice_spacings = {
        "Planck (1.6e-35 m)": L_PL,
        "10 x Planck": 10 * L_PL,
        "100 x Planck": 100 * L_PL,
        "1 fm (1e-15 m)": 1e-15,
        "1 pm (1e-12 m)": 1e-12,
        "1 nm (1e-9 m)": 1e-9,
        "1 um (1e-6 m)": 1e-6,
    }

    print(f"  Base rate: gamma = {gamma_base:.4e} Hz")
    print(f"  Superposition separation: delta_x = {dx:.0e} m")
    print()

    print(f"  {'Lattice spacing':>25s}  {'(l/dx)^2':>14s}  {'delta_gamma (Hz)':>16s}  "
          f"{'delta_gamma/gamma':>18s}  {'measurable?':>12s}")
    print("  " + "-" * 90)

    for name, l in lattice_spacings.items():
        correction = alpha_lat * (l / dx)**2
        delta_gamma = gamma_base * correction
        frac = correction

        # Measurable if the fractional correction exceeds ~1e-3
        # (decoherence rates are hard to measure to better than 0.1%)
        measurable = "YES" if frac > 1e-3 else "NO"

        print(f"  {name:>25s}  {(l/dx)**2:14.4e}  {delta_gamma:16.4e}  "
              f"{frac:18.4e}  {measurable:>12s}")

    print()
    print("  VERDICT: For l_P = Planck length (1.6e-35 m):")
    print(f"    (l_P / delta_x)^2 = ({L_PL:.2e} / {dx:.0e})^2 = {(L_PL/dx)**2:.2e}")
    print(f"    This is a correction of ~ 10^{math.log10((L_PL/dx)**2):.0f}")
    print()
    print("  The lattice correction to the decoherence rate is UNDETECTABLE")
    print("  for any sub-atomic lattice spacing. The correction only becomes")
    print("  measurable when the lattice spacing approaches the superposition")
    print("  separation (l ~ delta_x).")
    print()

    # What IS the leading observable effect?
    print("  WHAT IS THE LEADING OBSERVABLE EFFECT?")
    print("  ======================================")
    print()
    print("  The framework's leading observable effect is NOT a lattice correction.")
    print("  It is the QUALITATIVE prediction that gravity mediates entanglement.")
    print()
    print("  Specifically:")
    print("  1. ENTANGLEMENT PHASE: Phi = G m^2 T / hbar * [1/(d-dx) - 1/(d+dx)]")
    print("     This is the BMV signal. It does NOT depend on the lattice spacing.")
    print("     It depends only on G, m, d, dx, and T -- all macroscopic.")
    print()
    print("  2. BORN RULE PRESERVATION: I_3 = 0 exactly during the experiment.")
    print("     The framework predicts I_3 = 0 as a structural theorem.")
    print("     This CAN be tested (Experiment 1 from the NV card).")
    print()
    print("  3. DECOHERENCE RATE: gamma_grav follows the Gaussian-smeared")
    print("     Penrose-Diosi formula. The framework gives the same rate as")
    print("     standard gravitational decoherence models to all accessible")
    print("     precision. The lattice correction is ~ (l_P/dx)^2 ~ 10^{-58}.")
    print()

    return {}


# =====================================================================
# Section 7: Modified rate as a function of Born-rule parameter beta
# =====================================================================

def section_7_born_rule_modification():
    """Compute the modified decoherence rate as a function of beta."""
    print("=" * 78)
    print("7. MODIFIED DECOHERENCE RATE AS A FUNCTION OF beta (BORN RULE)")
    print("=" * 78)
    print()

    print("  From frontier_accessible_prediction.py, the cross-constraint:")
    print("    |beta - 1| ~ sqrt(|I_3|)")
    print()
    print("  If gravity is slightly nonlinear (as some models allow), the")
    print("  propagator acquires a perturbation of strength epsilon:")
    print("    K_eff = K_linear + epsilon * K_nonlinear")
    print()
    print("  This modifies the decoherence rate:")
    print("    gamma(epsilon) = gamma_PD * [1 + a_1 * epsilon + a_2 * epsilon^2 + ...]")
    print()
    print("  From the cross-constraint: epsilon ~ |beta - 1| ~ sqrt(|I_3|)")
    print()
    print("  The coefficient a_1 arises from the nonlinear correction to the")
    print("  gravitational field overlap. For a quadratic perturbation:")
    print("    a_1 ~ O(1), from the ratio of nonlinear to linear field energy")
    print()

    m = 1e-14
    dx = 1e-6
    sigma = 0.5e-6
    rho_diamond = 3500.0
    R = (3.0 * m / (4.0 * math.pi * rho_diamond))**(1.0/3.0)

    rates_linear = framework_decoherence_rate(m, dx, sigma, R)
    gamma_0 = rates_linear["gamma_physical"]

    # Modified rate: gamma(beta) = gamma_0 * [1 + a_1 * (beta - 1) + a_2 * (beta-1)^2]
    # With a_1 ~ 1, a_2 ~ 1 (order-unity coefficients)
    a_1 = 1.0
    a_2 = 0.5

    print(f"  Base rate: gamma_0 = {gamma_0:.4e} Hz")
    print()

    beta_values = [
        0.9, 0.95, 0.99, 0.999, 0.9999,
        1.0,
        1.0001, 1.001, 1.01, 1.05, 1.1
    ]

    print(f"  Modified rate: gamma(beta) = gamma_0 * [1 + (beta-1) + 0.5*(beta-1)^2]")
    print()
    print(f"  {'beta':>8s}  {'|beta-1|':>10s}  {'implied |I_3|':>14s}  "
          f"{'gamma (Hz)':>14s}  {'delta_gamma/gamma':>18s}  {'tau (s)':>12s}")
    print("  " + "-" * 82)

    for beta in beta_values:
        eps = beta - 1.0
        I3_implied = eps**2
        correction = a_1 * eps + a_2 * eps**2
        gamma_mod = gamma_0 * (1.0 + correction)
        if gamma_mod <= 0:
            gamma_mod = 1e-100
        frac = correction
        tau = 1.0 / gamma_mod

        print(f"  {beta:8.4f}  {abs(eps):10.4e}  {I3_implied:14.4e}  "
              f"{gamma_mod:14.4e}  {frac:18.4e}  {tau:12.4e}")

    print()

    # Current experimental bounds on beta
    print("  CURRENT EXPERIMENTAL CONSTRAINTS:")
    print()
    print("  From Born rule measurements (I_3 bounds):")
    print("    |I_3| < 10^{-4} (Pleinert 2020)")
    print("    => |beta - 1| < sqrt(10^{-4}) = 0.01")
    print("    => gamma is within 1% of gamma_0")
    print()
    print("  From direct gravity measurements:")
    print("    Mass law: |beta - 1| < 10^{-5} (Eot-Wash)")
    print("    => |I_3| < 10^{-10} (cross-constraint)")
    print("    => gamma is within 10^{-5} of gamma_0")
    print()
    print("  CONCLUSION: Current bounds restrict the Born-rule modification")
    print("  to the decoherence rate to be < 10^{-5}. The framework predicts")
    print("  beta = 1 exactly (linear propagator), so gamma = gamma_0 exactly.")
    print("  Any measured deviation would falsify the framework.")
    print()

    # The key prediction for the diamond NV experiment
    print("  FOR THE DIAMOND NV EXPERIMENT:")
    print()
    print("  The framework predicts a SPECIFIC decoherence rate:")
    print(f"    gamma_grav = {gamma_0:.4e} Hz")
    print(f"    tau_grav = {1.0/gamma_0:.4e} s")
    print()
    print("  If the experiment measures a decoherence rate significantly")
    print("  different from this value (after accounting for all other")
    print("  decoherence sources), it constrains the Born rule parameter:")
    print(f"    delta_gamma / gamma = (beta - 1) + O((beta-1)^2)")
    print()
    print("  This connects the DECOHERENCE MEASUREMENT to the BORN RULE TEST")
    print("  (Experiment 1 from the NV card).")
    print()

    return {
        "gamma_0": gamma_0,
        "a_1": a_1,
        "a_2": a_2,
    }


# =====================================================================
# Summary
# =====================================================================

def print_summary(results: dict):
    """Print the executive summary for experimentalists."""
    print()
    print("=" * 78)
    print("EXECUTIVE SUMMARY: GRAVITATIONAL DECOHERENCE RATE FOR DIAMOND NV")
    print("=" * 78)
    print()

    gamma = results["gamma_phys"]
    tau = results["tau_phys"]
    Phi = results["Phi_ent"]

    print("  The framework predicts the following for the BMV diamond NV experiment:")
    print()
    print(f"  1. GRAVITATIONAL DECOHERENCE RATE:")
    print(f"     gamma_grav = {gamma:.4e} Hz")
    print(f"     tau_grav = {tau:.4e} s")
    print(f"     (Gaussian-smeared Penrose-Diosi, m=10 pg, dx=1 um, sigma=0.5 um)")
    print()
    print(f"  2. ENTANGLEMENT PHASE (the BMV signal):")
    print(f"     Phi_ent = {Phi:.4e} rad (dx = 1 um, d = 200 um, T = 2 s)")
    print(f"     Phi_ent = {results['Phi_ent_large_dx']:.4e} rad (dx = 250 um, original BMV)")
    print()
    print(f"  3. LATTICE CORRECTION:")
    print(f"     delta_gamma/gamma ~ (l_P/dx)^2 ~ {(L_PL/1e-6)**2:.0e}")
    print(f"     UNDETECTABLE. Not the point of the experiment.")
    print()
    print(f"  4. BORN RULE CONNECTION:")
    print(f"     If |beta - 1| = epsilon, then delta_gamma/gamma ~ epsilon")
    print(f"     Current bound: epsilon < 10^{{-5}} (from Eot-Wash)")
    print(f"     Framework predicts: epsilon = 0 exactly")
    print()
    print(f"  5. WHAT THE EXPERIMENTALIST SHOULD AIM FOR:")
    print(f"     - Total decoherence budget: gamma_total < 0.5 Hz (= 1/T)")
    print(f"     - For dx = 1 um: gamma_grav = {gamma:.1f} Hz >> 0.5 Hz (PROBLEM)")
    print(f"       The gravitational decoherence itself kills coherence.")
    print(f"     - For dx = 250 um (original BMV): gamma_grav = 0.25 Hz < 0.5 Hz (OK)")
    print(f"       And Phi_ent is large: the signal dominates.")
    print(f"     - The key ratio is Phi_ent * tau_grav: must exceed ~1.")
    print(f"     - For dx = 250 um: Phi_ent = {results['Phi_ent_large_dx']:.1e} rad")
    print(f"     - For dx = 1 um: Phi = {Phi:.1e} rad (very challenging)")
    print()
    print(f"  6. THE FRAMEWORK'S UNIQUE PREDICTION:")
    print(f"     Born rule (I_3 = 0) and gravitational entanglement are BOTH")
    print(f"     consequences of the same propagator linearity. Testing one")
    print(f"     constrains the other. Run Experiments 1 and 2 from the NV card")
    print(f"     and compare: if I_3 = 0 AND entanglement is detected, the")
    print(f"     framework passes. If either fails, the framework is falsified.")
    print()
    print("=" * 78)


# =====================================================================
# Main
# =====================================================================

def main():
    t_start = time.time()

    print("=" * 78)
    print("GRAVITATIONAL DECOHERENCE RATE FOR THE DIAMOND NV EXPERIMENT")
    print("From the discrete-graph spacetime framework")
    print("=" * 78)
    print()

    # Run all seven sections
    section_1_parameters()
    rates, R = section_2_framework_rate()
    section_3_geometry_factor()
    section_4_penrose_diosi_comparison()
    sec5 = section_5_numerical_evaluation()
    section_6_lattice_correction()
    sec7 = section_7_born_rule_modification()

    # Summary
    print_summary(sec5)

    elapsed = time.time() - t_start
    print(f"  Total runtime: {elapsed:.1f} s")
    print(f"\n{'=' * 78}")
    print("EXPERIMENT COMPLETE")
    print(f"{'=' * 78}")

    return {
        "sec5": sec5,
        "sec7": sec7,
    }


if __name__ == "__main__":
    results = main()
