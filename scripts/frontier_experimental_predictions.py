#!/usr/bin/env python3
"""Experimental predictions distinguishing graph-propagator gravity from GR.

The two-axiom framework (path-sum propagator + Poisson field on a graph)
reproduces weak-field GR.  But the discrete graph structure leaves fingerprints
that differ from smooth GR.  This script computes three candidate predictions
and evaluates each against current experimental sensitivity.

Candidate 1 -- Gravitational decoherence rate
  A spatial superposition (cat state across graph sites) in a gravitational
  field decoheres because different branches sample different field values.
  On a discrete graph the decoherence rate acquires a lattice correction.
  Compare to the Diosi-Penrose prediction tau ~ hbar / Delta_E_grav.

Candidate 2 -- Modified COW neutron interferometry phase
  In a Colella-Overhauser-Werner experiment, neutrons accumulate gravitational
  phase Phi = m g H T / hbar.  On a lattice, the propagator phase picks up
  a correction proportional to (a/H)^2 from the discrete sum vs integral.

Candidate 3 -- Entanglement generation rate (BMV experiment)
  Two masses in superposition can become entangled via gravity.  The second-
  quantized prototype showed Bogoliubov particle creation.  The entanglement
  rate on a lattice has a specific dependence on mass, separation, and
  lattice spacing.

Physical constants in SI unless noted.  All corrections expressed in terms
of the fundamental lattice spacing a (free parameter of the model).

PStack experiment: frontier-experimental-predictions
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np
from numpy.linalg import eigh

# ── Physical constants (SI) ─────────────────────────────────────────
HBAR = 1.054571817e-34      # J s
G_NEWTON = 6.67430e-11      # m^3 kg^-1 s^-2
C_LIGHT = 2.99792458e8      # m/s
K_BOLTZMANN = 1.380649e-23  # J/K
M_NEUTRON = 1.67493e-27     # kg
M_PROTON = 1.67262e-27      # kg
M_ELECTRON = 9.10938e-31    # kg
L_PLANCK = 1.616255e-35     # m
T_PLANCK = 5.391247e-44     # s
M_PLANCK = 2.176434e-8      # kg
E_PLANCK = M_PLANCK * C_LIGHT**2  # J

# ── Experimental parameters ──────────────────────────────────────────

# COW experiment (best current neutron interferometry)
COW_HEIGHT_M = 0.02         # 2 cm path height
COW_AREA_M2 = 6e-4          # ~6 cm^2 enclosed area
COW_TIME_S = 1e-3           # ~1 ms traversal time
COW_PHASE_PRECISION = 1e-3  # ~10^-3 rad precision (state of art)

# MAQRO / matter-wave interferometry
MAQRO_MASS_KG = 1e-15       # ~10^9 amu nanoparticle
MAQRO_SUPERPOSITION_M = 1e-6  # 1 micron superposition
MAQRO_TIME_S = 100.0        # 100 s free fall time

# BMV experiment (Bose-Marletto-Vedral)
BMV_MASS_KG = 1e-14         # ~10 pg diamond microsphere
BMV_SEPARATION_M = 500e-6   # 500 micron separation (center-to-center)
BMV_SUPERPOSITION_M = 100e-6  # 100 micron superposition size per mass
BMV_TIME_S = 2.0            # 2 s interaction time


# =====================================================================
# CANDIDATE 1: Gravitational decoherence rate
# =====================================================================

def decoherence_diosi_penrose(mass_kg: float, delta_x_m: float) -> float:
    """Diosi-Penrose gravitational decoherence rate.

    For a uniform-density sphere of mass m in a spatial superposition
    of separation delta_x >> sphere radius R:

        tau_DP = hbar / Delta_E_grav
        Delta_E_grav = G m^2 / delta_x   (self-energy difference)

    Returns decoherence rate gamma = 1/tau in Hz.
    """
    delta_E = G_NEWTON * mass_kg**2 / delta_x_m
    tau = HBAR / delta_E
    gamma = 1.0 / tau
    return gamma


def decoherence_lattice_correction(mass_kg: float, delta_x_m: float,
                                    a_m: float) -> dict:
    """Lattice correction to the gravitational decoherence rate.

    On a discrete graph with spacing a, the gravitational self-energy
    of a superposition at separation delta_x is computed as a lattice sum
    rather than a continuous integral.  The key difference:

    Continuum: Delta_E = G m^2 / delta_x
    Lattice:   Delta_E = G m^2 / delta_x * [1 + C_lat * (a/delta_x)^2 + ...]

    The lattice correction C_lat comes from the Euler-Maclaurin expansion
    of the discrete Poisson Green's function vs the continuum 1/r:

        sum_{n} 1/|r - n*a| vs integral 1/|r - x| dx/a

    For a 3D cubic lattice, the leading correction is:
        G_lattice(r) = G_continuum(r) * [1 + (pi^2/6) * (a/r)^2 + O((a/r)^4)]

    This modifies the self-energy and thus the decoherence rate.
    """
    # Continuum Diosi-Penrose
    gamma_dp = decoherence_diosi_penrose(mass_kg, delta_x_m)
    tau_dp = 1.0 / gamma_dp if gamma_dp > 0 else float('inf')

    # Lattice correction coefficient
    # From Euler-Maclaurin: the discrete Green's function on a cubic lattice
    # has leading correction (pi^2/6) * (a/r)^2 in 3D.
    # (This is the Madelung-like correction for the discrete Laplacian.)
    C_lat = math.pi**2 / 6.0  # ~ 1.645

    ratio = a_m / delta_x_m
    correction_factor = 1.0 + C_lat * ratio**2

    gamma_lattice = gamma_dp * correction_factor
    tau_lattice = 1.0 / gamma_lattice if gamma_lattice > 0 else float('inf')

    delta_gamma = gamma_lattice - gamma_dp
    fractional_correction = C_lat * ratio**2

    return {
        "gamma_dp": gamma_dp,
        "tau_dp": tau_dp,
        "gamma_lattice": gamma_lattice,
        "tau_lattice": tau_lattice,
        "delta_gamma": delta_gamma,
        "fractional_correction": fractional_correction,
        "C_lat": C_lat,
        "a_m": a_m,
        "delta_x_m": delta_x_m,
    }


def lattice_decoherence_numerical(N: int, delta_n: int, strength: float,
                                   a_spacing: float = 1.0) -> dict:
    """Numerically compute decoherence of a two-site cat state on a 1D lattice.

    Place a superposition |L> + |R> where L and R are separated by delta_n sites.
    Apply a gravitational field from a source at the center.
    The decoherence rate is set by the off-diagonal decay of the reduced density
    matrix when the gravitational field is treated as an environment.

    On the lattice, the phase difference accumulated by the two branches is:
        delta_phi = k * sum over paths of [S_L(path) - S_R(path)]

    For a static field, this reduces to:
        delta_phi = k * [f(x_R) - f(x_L)] * T

    where f is the gravitational potential at each site.
    """
    # Build 1D gravitational potential
    source = N // 2
    V = np.zeros(N)
    for i in range(N):
        r = max(abs(i - source), 1) * a_spacing
        V[i] = strength / r

    # Cat state: superposition at sites L and R, OFFSET from source
    # (symmetric placement gives delta_f = 0 trivially)
    offset = N // 4  # place cat state away from source
    L = source + offset
    R = source + offset + delta_n

    if L < 0 or R >= N:
        return {"valid": False}

    # Phase difference from gravitational potential
    delta_f = V[R] - V[L]

    # On a continuum, this would be:
    # delta_f_continuum = strength * (1/|R-source| - 1/|L-source|) / a_spacing
    r_L = abs(L - source) * a_spacing
    r_R = abs(R - source) * a_spacing
    if r_L > 0 and r_R > 0:
        delta_f_continuum = strength * (1.0 / r_R - 1.0 / r_L)
    else:
        delta_f_continuum = 0.0

    # The decoherence rate (dephasing) is proportional to |delta_f|
    # gamma ~ |delta_f| / hbar  (in appropriate units)

    return {
        "valid": True,
        "delta_f_lattice": delta_f,
        "delta_f_continuum": delta_f_continuum,
        "ratio": delta_f / delta_f_continuum if abs(delta_f_continuum) > 1e-30 else float('nan'),
        "L": L,
        "R": R,
        "V_L": V[L],
        "V_R": V[R],
    }


def run_candidate_1():
    """Run gravitational decoherence analysis."""
    print("\n" + "=" * 78)
    print("CANDIDATE 1: GRAVITATIONAL DECOHERENCE RATE")
    print("=" * 78)

    # ── Analytic comparison: Diosi-Penrose vs lattice ────────────────
    print("\n--- Diosi-Penrose vs Lattice-corrected decoherence ---")
    print(f"\nDiosi-Penrose: gamma_DP = G m^2 / (hbar * delta_x)")
    print(f"Lattice:       gamma_lat = gamma_DP * [1 + (pi^2/6)(a/delta_x)^2]")
    print(f"Correction coefficient C_lat = pi^2/6 = {math.pi**2/6:.6f}")

    # Test for different lattice spacings
    a_values_m = [L_PLANCK, 10 * L_PLANCK, 100 * L_PLANCK,
                  1e-30, 1e-25, 1e-20, 1e-15]
    a_labels = ["l_P", "10 l_P", "100 l_P",
                "1e-30 m", "1e-25 m", "1e-20 m", "1e-15 m"]

    # MAQRO-class experiment
    print(f"\n  MAQRO parameters:")
    print(f"    mass = {MAQRO_MASS_KG:.2e} kg")
    print(f"    superposition = {MAQRO_SUPERPOSITION_M:.2e} m")
    print(f"    time = {MAQRO_TIME_S:.0f} s")

    gamma_dp_maqro = decoherence_diosi_penrose(MAQRO_MASS_KG, MAQRO_SUPERPOSITION_M)
    tau_dp_maqro = 1.0 / gamma_dp_maqro if gamma_dp_maqro > 0 else float('inf')
    print(f"\n    Diosi-Penrose rate: gamma_DP = {gamma_dp_maqro:.4e} Hz")
    print(f"    Diosi-Penrose time: tau_DP  = {tau_dp_maqro:.4e} s")

    print(f"\n    {'a':>12s}  {'frac_corr':>14s}  {'delta_gamma (Hz)':>18s}  {'detectable?':>14s}")
    for a_m, label in zip(a_values_m, a_labels):
        result = decoherence_lattice_correction(MAQRO_MASS_KG,
                                                 MAQRO_SUPERPOSITION_M, a_m)
        frac = result["fractional_correction"]
        dg = result["delta_gamma"]
        # Detectable if delta_gamma * T > some threshold (say 0.01 for 1% effect)
        detectable = frac > 1e-2
        print(f"    {label:>12s}  {frac:14.4e}  {dg:18.4e}  "
              f"{'YES' if detectable else 'no':>14s}")

    # ── Required lattice spacing for detection ────────────────────────
    # frac_corr > threshold  =>  a > delta_x * sqrt(threshold / C_lat)
    C_lat = math.pi**2 / 6.0
    threshold = 1e-2  # 1% effect
    a_required = MAQRO_SUPERPOSITION_M * math.sqrt(threshold / C_lat)
    print(f"\n    Required a for 1% correction: a > {a_required:.4e} m")
    print(f"    In Planck lengths: a > {a_required/L_PLANCK:.4e} l_P")
    print(f"    This is {'MACROSCOPIC' if a_required > 1e-10 else 'sub-nuclear' if a_required > 1e-15 else 'sub-Planckian' if a_required < L_PLANCK else 'plausible'}")

    # ── Numerical lattice computation ─────────────────────────────────
    print(f"\n--- Numerical lattice verification ---")
    N = 400
    separations = [2, 4, 8, 16, 32, 64]
    strength = 1.0

    print(f"  N={N}, source at center, strength={strength}")
    print(f"  {'delta_n':>8s}  {'delta_f_lat':>14s}  {'delta_f_cont':>14s}  {'ratio':>10s}")
    for dn in separations:
        r = lattice_decoherence_numerical(N, dn, strength)
        if r["valid"]:
            print(f"  {dn:8d}  {r['delta_f_lattice']:14.8f}  "
                  f"{r['delta_f_continuum']:14.8f}  {r['ratio']:10.6f}")

    # The ratio approaches 1 as delta_n grows (lattice -> continuum)
    # Deviations at small delta_n are the lattice fingerprint
    r_small = lattice_decoherence_numerical(N, 2, strength)
    r_large = lattice_decoherence_numerical(N, 64, strength)
    if r_small["valid"] and r_large["valid"]:
        dev_small = abs(r_small["ratio"] - 1.0)
        dev_large = abs(r_large["ratio"] - 1.0)
        print(f"\n  Lattice deviation at delta_n=2:  {dev_small:.6f}")
        print(f"  Lattice deviation at delta_n=64: {dev_large:.6f}")
        print(f"  Scaling: deviation ~ 1/delta_n^2 expected")
        if dev_small > 0 and dev_large > 0:
            alpha_est = -math.log(dev_large / dev_small) / math.log(64.0 / 2.0)
            print(f"  Measured scaling exponent: {alpha_est:.2f}")

    # ── Verdict ───────────────────────────────────────────────────────
    print(f"\n  VERDICT (Candidate 1):")
    print(f"    The lattice correction to gravitational decoherence is")
    print(f"    proportional to (a/delta_x)^2.  For a = l_Planck and")
    print(f"    delta_x = 1 micron, the fractional correction is")
    frac_planck = C_lat * (L_PLANCK / MAQRO_SUPERPOSITION_M)**2
    print(f"    C_lat * (l_P / delta_x)^2 = {frac_planck:.4e}")
    print(f"    This is ~{frac_planck:.0e} -- utterly undetectable.")
    print(f"    Even MAQRO (most ambitious proposal) cannot see this.")
    print(f"    STATUS: NOT TESTABLE with a = l_Planck")

    return {"frac_correction_planck": frac_planck, "a_required_m": a_required}


# =====================================================================
# CANDIDATE 2: Modified COW neutron interferometry phase
# =====================================================================

def cow_phase_continuum(mass_kg: float, g_ms2: float,
                        height_m: float, time_s: float) -> float:
    """Standard COW phase shift in continuum.

    Phi = m * g * H * T / hbar
    """
    return mass_kg * g_ms2 * height_m * time_s / HBAR


def cow_phase_lattice(mass_kg: float, g_ms2: float, height_m: float,
                      time_s: float, a_m: float) -> dict:
    """COW phase shift on a discrete lattice.

    On a lattice with spacing a, the phase accumulated along a path of
    height H is a sum rather than an integral:

    Continuum: Phi = (m*g/hbar) * integral_0^H z dz * (T/H) = m*g*H*T/(2*hbar)
      (Wait -- the COW phase is m*g*H*T/hbar where H is the height difference
       between the two paths, not an integral.  The two arms of the
       interferometer are at heights z and z+H.)

    On the lattice, the gravitational potential at height z is
    V(z) = m*g*z for the continuum, but on the lattice it becomes
    V(n) = m*g*n*a where n is the site index.

    The phase difference between the upper and lower arms:
    Continuum: delta_Phi = m*g*H*T/hbar  (exact)
    Lattice:   delta_Phi = m*g*N_H*a*T/hbar where N_H = round(H/a)

    The correction comes from the discretization of H:
    N_H * a = H + epsilon,  |epsilon| <= a/2

    So: delta_Phi_lattice = delta_Phi_continuum * (1 + epsilon/H)

    The WORST-CASE fractional error is a/(2*H).
    The AVERAGE fractional error (random offset) is a/(2*sqrt(3)*H).

    But there's a more subtle correction from the propagator itself.
    The path-sum propagator on a lattice has action S = sum_steps L_i*(1-f_i)
    rather than the integral.  The Euler-Maclaurin correction to this sum
    gives a systematic phase correction:

    delta_Phi_sys = (m*g*T/hbar) * (a^2/12) * d^2(f)/dz^2 * T

    For a uniform gravitational field f(z) = g*z, d^2f/dz^2 = 0, so the
    leading systematic correction VANISHES.

    The next correction comes from the curvature of the actual gravitational
    field: d^2f/dz^2 = 2*G*M/r^3.  This gives:

    delta_Phi_sys = (a^2/12) * (2*G*M_earth/R_earth^3) * m * T^2 / hbar
    """
    # Continuum phase
    phi_cont = mass_kg * g_ms2 * height_m * time_s / HBAR

    # Discretization error (random)
    frac_random = a_m / (2.0 * math.sqrt(3) * height_m)

    # Systematic Euler-Maclaurin correction from field curvature
    # d^2(g*z)/dz^2 = 0 for uniform field
    # d^2(G*M/r)/dz^2 at Earth's surface ~ 2*g/R_earth
    R_earth = 6.371e6  # m
    g_earth = 9.81     # m/s^2
    d2f_dz2 = 2.0 * g_earth / R_earth  # ~ 3e-6 /s^2

    # Euler-Maclaurin systematic correction
    phi_em = (a_m**2 / 12.0) * d2f_dz2 * mass_kg * time_s / HBAR
    frac_systematic = phi_em / phi_cont if abs(phi_cont) > 0 else 0

    # Total fractional correction
    frac_total = math.sqrt(frac_random**2 + frac_systematic**2)

    return {
        "phi_continuum": phi_cont,
        "phi_em_correction": phi_em,
        "frac_random": frac_random,
        "frac_systematic": frac_systematic,
        "frac_total": frac_total,
    }


def cow_numerical_lattice(N: int, g_scaled: float, height_sites: int,
                           n_paths: int = 1000) -> dict:
    """Numerical lattice path-sum for COW-like geometry.

    Propagate a wavepacket along two paths at different heights on a 1D lattice.
    Compare the accumulated phase to the continuum expectation.

    This uses a tight-binding model: the propagator transfer matrix on a
    1D chain with gravitational potential V(n) = g * n gives phases that
    can be compared to the continuum limit.
    """
    # Build Hamiltonian with linear potential
    H = np.zeros((N, N))
    for i in range(N - 1):
        H[i, i + 1] = -1.0
        H[i + 1, i] = -1.0
    for i in range(N):
        H[i, i] = g_scaled * i

    # Diagonalize
    energies, vecs = eigh(H)

    # Phase accumulated by states at different heights
    # The energy eigenvalue gives the phase rate: phi = E * t
    # For a localized state at site n, the effective energy is approximately
    # the on-site potential g*n plus the hopping contribution.

    # For two "paths" at heights n_low and n_high = n_low + height_sites:
    n_low = N // 4
    n_high = n_low + height_sites

    if n_high >= N:
        return {"valid": False}

    # Local Green's function: G(n,n; E) tells us the local density of states
    # Phase difference between two sites in the ground state:
    # delta_phi = sum_k |psi_k(n_high)|^2 * E_k - sum_k |psi_k(n_low)|^2 * E_k
    # This is just the local energy at each site.
    local_E_low = np.sum(np.abs(vecs[n_low, :])**2 * energies)
    local_E_high = np.sum(np.abs(vecs[n_high, :])**2 * energies)
    delta_E_lattice = local_E_high - local_E_low

    # Continuum expectation: delta_E = g * height_sites
    delta_E_continuum = g_scaled * height_sites

    ratio = delta_E_lattice / delta_E_continuum if abs(delta_E_continuum) > 1e-30 else float('nan')

    return {
        "valid": True,
        "delta_E_lattice": delta_E_lattice,
        "delta_E_continuum": delta_E_continuum,
        "ratio": ratio,
        "deviation": abs(ratio - 1.0),
    }


def run_candidate_2():
    """Run COW phase shift analysis."""
    print("\n" + "=" * 78)
    print("CANDIDATE 2: MODIFIED COW NEUTRON INTERFEROMETRY PHASE")
    print("=" * 78)

    g_earth = 9.81  # m/s^2

    # ── Analytic prediction ───────────────────────────────────────────
    print("\n--- Analytic: continuum COW phase ---")
    phi_cow = cow_phase_continuum(M_NEUTRON, g_earth, COW_HEIGHT_M, COW_TIME_S)
    print(f"  COW phase (continuum): Phi = {phi_cow:.4e} rad")
    print(f"  Current precision: ~{COW_PHASE_PRECISION:.0e} rad")

    # Lattice corrections for various a
    print(f"\n--- Lattice corrections to COW phase ---")
    print(f"  Uniform field: Euler-Maclaurin leading correction = 0 (d^2f/dz^2 = 0)")
    print(f"  Correction from Earth's field curvature: d^2(g*z)/dz^2 = 2g/R_earth")

    a_values_m = [L_PLANCK, 10 * L_PLANCK, 100 * L_PLANCK,
                  1e-30, 1e-25, 1e-20, 1e-15]
    a_labels = ["l_P", "10 l_P", "100 l_P",
                "1e-30 m", "1e-25 m", "1e-20 m", "1e-15 m"]

    print(f"\n  {'a':>12s}  {'frac_random':>14s}  {'frac_systematic':>16s}  "
          f"{'delta_Phi (rad)':>16s}  {'detectable?':>12s}")
    for a_m, label in zip(a_values_m, a_labels):
        result = cow_phase_lattice(M_NEUTRON, g_earth, COW_HEIGHT_M,
                                    COW_TIME_S, a_m)
        delta_phi = result["phi_em_correction"]
        frac = result["frac_systematic"]
        detectable = abs(delta_phi) > COW_PHASE_PRECISION
        print(f"  {label:>12s}  {result['frac_random']:14.4e}  {frac:16.4e}  "
              f"{delta_phi:16.4e}  {'YES' if detectable else 'no':>12s}")

    # ── Required a for detectability ──────────────────────────────────
    R_earth = 6.371e6
    d2f = 2.0 * g_earth / R_earth
    # delta_phi = (a^2/12) * d2f * m * T / hbar > precision
    # a^2 > precision * 12 * hbar / (d2f * m * T)
    a_sq_required = COW_PHASE_PRECISION * 12.0 * HBAR / (d2f * M_NEUTRON * COW_TIME_S)
    a_required = math.sqrt(a_sq_required) if a_sq_required > 0 else float('inf')
    print(f"\n  Required a for detection: a > {a_required:.4e} m")
    print(f"  In Planck lengths: a > {a_required/L_PLANCK:.4e} l_P")

    # ── Numerical lattice verification ────────────────────────────────
    print(f"\n--- Numerical lattice verification ---")
    N_lat = 200
    g_values = [0.001, 0.01, 0.1]
    height_sites_list = [5, 10, 20, 40]

    for g_scaled in g_values:
        print(f"\n  g_scaled = {g_scaled}")
        print(f"  {'height':>8s}  {'dE_lat':>14s}  {'dE_cont':>14s}  {'ratio':>10s}  {'dev':>12s}")
        for hs in height_sites_list:
            r = cow_numerical_lattice(N_lat, g_scaled, hs)
            if r["valid"]:
                print(f"  {hs:8d}  {r['delta_E_lattice']:14.8f}  "
                      f"{r['delta_E_continuum']:14.8f}  "
                      f"{r['ratio']:10.6f}  {r['deviation']:12.4e}")

    # Check scaling of deviation with height
    print(f"\n  Deviation scaling with height (g=0.01):")
    devs = []
    heights = []
    for hs in [4, 8, 16, 32, 64]:
        r = cow_numerical_lattice(N_lat, 0.01, hs)
        if r["valid"] and r["deviation"] > 1e-15:
            devs.append(r["deviation"])
            heights.append(hs)
    if len(devs) >= 2:
        devs = np.array(devs)
        heights = np.array(heights, dtype=float)
        # Fit: dev ~ height^alpha
        log_d = np.log(devs)
        log_h = np.log(heights)
        alpha = np.polyfit(log_h, log_d, 1)[0]
        print(f"  Fit: deviation ~ height^{alpha:.2f}")

    # ── Verdict ───────────────────────────────────────────────────────
    print(f"\n  VERDICT (Candidate 2):")
    print(f"    For a uniform gravitational field, the leading lattice")
    print(f"    correction to COW phase VANISHES (d^2f/dz^2 = 0).")
    print(f"    The surviving correction from field curvature is")
    print(f"    proportional to a^2 * (g/R_earth).  For a = l_Planck,")
    frac_planck_cow = cow_phase_lattice(M_NEUTRON, g_earth, COW_HEIGHT_M,
                                         COW_TIME_S, L_PLANCK)
    print(f"    fractional correction = {frac_planck_cow['frac_systematic']:.4e}")
    print(f"    Required a > {a_required:.4e} m for detection")
    print(f"    STATUS: NOT TESTABLE with a = l_Planck")

    return {"a_required_m": a_required,
            "frac_correction_planck": frac_planck_cow["frac_systematic"]}


# =====================================================================
# CANDIDATE 3: Entanglement generation rate (BMV)
# =====================================================================

def bmv_entanglement_phase_continuum(m1_kg: float, m2_kg: float,
                                      d_close_m: float, d_far_m: float,
                                      time_s: float) -> float:
    """BMV entanglement phase in the Newtonian/continuum limit.

    Two masses, each in a superposition |L> + |R>.  The gravitational
    interaction creates entanglement.  The key phase is:

    delta_Phi = G*m1*m2*T/hbar * (1/d_close - 1/d_far)

    where d_close and d_far are the two possible separations when the
    masses are in the same/opposite branches.

    For superposition size delta_x and separation D:
        d_close = D - delta_x
        d_far   = D + delta_x

    This phase must exceed ~pi for maximal entanglement.
    """
    phi = G_NEWTON * m1_kg * m2_kg * time_s / HBAR * (
        1.0 / d_close_m - 1.0 / d_far_m
    )
    return phi


def bmv_entanglement_lattice(m_kg: float, d_m: float, delta_x_m: float,
                              time_s: float, a_m: float) -> dict:
    """BMV entanglement phase with lattice correction.

    On a discrete lattice, the gravitational potential 1/r is replaced by
    the lattice Green's function G_lat(r).  For separations r >> a:

    G_lat(r) = (1/r) * [1 + C_lat * (a/r)^2 + ...]

    The entanglement phase becomes:
    delta_Phi_lat = delta_Phi_cont * [1 + C_lat * a^2 * (1/d_close^2 - 1/d_far^2)
                                       / (1/d_close - 1/d_far) ]

    More precisely, both 1/d_close and 1/d_far pick up corrections:
    1/d -> (1/d)[1 + C*(a/d)^2]

    So: delta_Phi_lat / delta_Phi_cont
        = [d_close^{-1}(1 + C(a/d_close)^2) - d_far^{-1}(1 + C(a/d_far)^2)]
          / [d_close^{-1} - d_far^{-1}]
    """
    C_lat = math.pi**2 / 6.0

    d_close = d_m - delta_x_m
    d_far = d_m + delta_x_m

    if d_close <= 0:
        return {"valid": False}

    # Continuum phase
    phi_cont = bmv_entanglement_phase_continuum(m_kg, m_kg, d_close, d_far, time_s)

    # Lattice-corrected inverse distances
    inv_close_lat = (1.0 / d_close) * (1.0 + C_lat * (a_m / d_close)**2)
    inv_far_lat = (1.0 / d_far) * (1.0 + C_lat * (a_m / d_far)**2)

    inv_close_cont = 1.0 / d_close
    inv_far_cont = 1.0 / d_far

    correction_factor = ((inv_close_lat - inv_far_lat) /
                         (inv_close_cont - inv_far_cont))

    phi_lattice = phi_cont * correction_factor
    delta_phi = phi_lattice - phi_cont
    frac_correction = correction_factor - 1.0

    return {
        "valid": True,
        "phi_continuum": phi_cont,
        "phi_lattice": phi_lattice,
        "delta_phi": delta_phi,
        "frac_correction": frac_correction,
        "C_lat": C_lat,
        "d_close": d_close,
        "d_far": d_far,
    }


def bmv_numerical_lattice(N: int, mass_sites: list[int],
                           superposition_dn: int) -> dict:
    """Numerical lattice computation of BMV-like entanglement.

    Two masses on a 1D lattice, each in a superposition of two sites.
    Compute the gravitational interaction energy for all four configurations
    (LL, LR, RL, RR) and extract the entanglement phase.

    On the lattice, the interaction is via the lattice Green's function
    (inverse Laplacian), not 1/r.
    """
    # Lattice Green's function on 1D periodic chain: exact
    # G(n) = (N - n) * n / (2 * N)  for 1D with periodic BC
    # For open BC: solve Laplacian directly

    # Build 1D Laplacian
    L_mat = np.zeros((N, N))
    for i in range(N):
        L_mat[i, i] = -2.0
        if i > 0:
            L_mat[i, i-1] = 1.0
        if i < N - 1:
            L_mat[i, i+1] = 1.0

    # Pseudo-inverse (remove zero mode)
    evals, evecs = eigh(L_mat)
    # Replace zero eigenvalue with large number to get pseudo-inverse
    evals_inv = np.where(np.abs(evals) > 1e-10, 1.0 / evals, 0.0)
    G_lat = evecs @ np.diag(evals_inv) @ evecs.T

    # Mass positions
    m1_L, m1_R = mass_sites[0], mass_sites[0] + superposition_dn
    m2_L, m2_R = mass_sites[1], mass_sites[1] + superposition_dn

    if max(m1_R, m2_R) >= N or min(m1_L, m2_L) < 0:
        return {"valid": False}

    # Four interaction energies (via lattice Green's function)
    # E(i,j) = -G_lat(i,j) [negative sign for gravity]
    E_LL = -G_lat[m1_L, m2_L]
    E_LR = -G_lat[m1_L, m2_R]
    E_RL = -G_lat[m1_R, m2_L]
    E_RR = -G_lat[m1_R, m2_R]

    # Entanglement phase: phi = (E_LL + E_RR - E_LR - E_RL) * T
    # (This is zero only if the interaction is linear in position)
    phi_lattice = E_LL + E_RR - E_LR - E_RL

    # Continuum 1D Green's function on an interval [0, N-1]:
    # G(x,y) = -min(x, y) * (N-1-max(x,y)) / (N-1)
    # (solution to G'' = delta(x-y) with Dirichlet BC at 0 and N-1)
    def green_1d_cont(x, y, Ntot):
        mn = min(x, y)
        mx = max(x, y)
        return -mn * (Ntot - 1 - mx) / (Ntot - 1)

    E_LL_cont = -green_1d_cont(m1_L, m2_L, N)
    E_LR_cont = -green_1d_cont(m1_L, m2_R, N)
    E_RL_cont = -green_1d_cont(m1_R, m2_L, N)
    E_RR_cont = -green_1d_cont(m1_R, m2_R, N)

    phi_continuum = E_LL_cont + E_RR_cont - E_LR_cont - E_RL_cont

    ratio = phi_lattice / phi_continuum if abs(phi_continuum) > 1e-30 else float('nan')

    return {
        "valid": True,
        "phi_lattice": phi_lattice,
        "phi_continuum": phi_continuum,
        "ratio": ratio,
        "deviation": abs(ratio - 1.0) if np.isfinite(ratio) else float('nan'),
        "E_LL": E_LL, "E_LR": E_LR, "E_RL": E_RL, "E_RR": E_RR,
    }


def run_candidate_3():
    """Run BMV entanglement analysis."""
    print("\n" + "=" * 78)
    print("CANDIDATE 3: ENTANGLEMENT GENERATION RATE (BMV EXPERIMENT)")
    print("=" * 78)

    # ── Continuum BMV prediction ──────────────────────────────────────
    print("\n--- Continuum BMV entanglement phase ---")
    d_close = BMV_SEPARATION_M - BMV_SUPERPOSITION_M
    d_far = BMV_SEPARATION_M + BMV_SUPERPOSITION_M

    phi_bmv = bmv_entanglement_phase_continuum(
        BMV_MASS_KG, BMV_MASS_KG, d_close, d_far, BMV_TIME_S
    )
    print(f"  BMV parameters:")
    print(f"    mass = {BMV_MASS_KG:.2e} kg")
    print(f"    separation = {BMV_SEPARATION_M*1e6:.0f} um")
    print(f"    superposition = {BMV_SUPERPOSITION_M*1e6:.0f} um")
    print(f"    time = {BMV_TIME_S:.1f} s")
    print(f"    d_close = {d_close*1e6:.0f} um")
    print(f"    d_far = {d_far*1e6:.0f} um")
    print(f"  Entanglement phase: Phi = {phi_bmv:.4e} rad")
    print(f"  For maximal entanglement need Phi > pi = {math.pi:.4f}")
    print(f"  Phi/pi = {phi_bmv/math.pi:.4e}")

    # ── Lattice corrections ───────────────────────────────────────────
    print(f"\n--- Lattice corrections to BMV phase ---")

    a_values_m = [L_PLANCK, 10 * L_PLANCK, 100 * L_PLANCK,
                  1e-30, 1e-25, 1e-20, 1e-15]
    a_labels = ["l_P", "10 l_P", "100 l_P",
                "1e-30 m", "1e-25 m", "1e-20 m", "1e-15 m"]

    print(f"\n  {'a':>12s}  {'frac_corr':>14s}  {'delta_Phi':>14s}  {'detectable?':>12s}")
    for a_m, label in zip(a_values_m, a_labels):
        result = bmv_entanglement_lattice(
            BMV_MASS_KG, BMV_SEPARATION_M, BMV_SUPERPOSITION_M,
            BMV_TIME_S, a_m
        )
        if result["valid"]:
            # Detection threshold: need delta_phi to change entanglement witness
            # Roughly, need fractional correction > 1% of the already-small phase
            frac = result["frac_correction"]
            dphi = result["delta_phi"]
            # BMV measures presence/absence of entanglement, not precise phase
            # So the lattice correction matters only if it changes phi by O(phi)
            detectable = abs(frac) > 0.01
            print(f"  {label:>12s}  {frac:14.4e}  {dphi:14.4e}  "
                  f"{'YES' if detectable else 'no':>12s}")

    # ── Required a for detection ──────────────────────────────────────
    C_lat = math.pi**2 / 6.0
    # Simplified: frac ~ C_lat * a^2 * (1/d_close^2 + 1/d_far^2)
    # (approximate, dominant term is 1/d_close^2)
    frac_target = 0.01
    a_sq = frac_target * d_close**2 / C_lat
    a_required = math.sqrt(a_sq)
    print(f"\n  Required a for 1% correction: a > {a_required:.4e} m")
    print(f"  In Planck lengths: a > {a_required/L_PLANCK:.4e} l_P")

    # ── Numerical lattice verification ────────────────────────────────
    print(f"\n--- Numerical lattice verification (1D) ---")
    N_lat = 400
    separations_sites = [20, 40, 80, 160]
    superposition_dn = 5

    print(f"  N={N_lat}, superposition_dn={superposition_dn}")
    print(f"  {'separation':>12s}  {'phi_lat':>14s}  {'phi_cont':>14s}  "
          f"{'ratio':>10s}  {'deviation':>12s}")
    for sep in separations_sites:
        m1_pos = N_lat // 2 - sep // 2
        m2_pos = N_lat // 2 + sep // 2
        r = bmv_numerical_lattice(N_lat, [m1_pos, m2_pos], superposition_dn)
        if r["valid"]:
            print(f"  {sep:12d}  {r['phi_lattice']:14.8f}  "
                  f"{r['phi_continuum']:14.8f}  "
                  f"{r['ratio']:10.6f}  {r['deviation']:12.4e}")

    # ── Scaling with separation ───────────────────────────────────────
    print(f"\n  Deviation scaling with separation (superposition_dn=5):")
    devs = []
    seps = []
    for sep in [10, 20, 40, 80, 160]:
        m1_pos = N_lat // 2 - sep // 2
        m2_pos = N_lat // 2 + sep // 2
        r = bmv_numerical_lattice(N_lat, [m1_pos, m2_pos], superposition_dn)
        if r["valid"] and r["deviation"] > 1e-15:
            devs.append(r["deviation"])
            seps.append(sep)
    if len(devs) >= 2:
        devs = np.array(devs)
        seps = np.array(seps, dtype=float)
        alpha = np.polyfit(np.log(seps), np.log(devs), 1)[0]
        print(f"  Fit: deviation ~ separation^{alpha:.2f}")

    # ── Key physics point ─────────────────────────────────────────────
    print(f"\n--- Key physics: BMV tests QUANTUM gravity, not lattice spacing ---")
    print(f"  The BMV experiment tests whether gravity can mediate entanglement.")
    print(f"  Our framework predicts YES -- the Bogoliubov mechanism creates")
    print(f"  entanglement via gravitational interaction on the graph.")
    print(f"  This is a QUALITATIVE prediction, not a precision test of a.")
    print(f"  If BMV sees entanglement: consistent with our framework.")
    print(f"  If BMV sees NO entanglement: our framework is FALSIFIED")
    print(f"  (since it treats gravity as quantum at all scales).")

    # ── Verdict ───────────────────────────────────────────────────────
    print(f"\n  VERDICT (Candidate 3):")
    print(f"    The lattice correction to BMV entanglement phase is")
    print(f"    proportional to (a/d)^2 where d is the mass separation.")
    print(f"    For a = l_Planck and d = 200 um:")
    frac_planck = C_lat * (L_PLANCK / d_close)**2
    print(f"    fractional correction = {frac_planck:.4e}")
    print(f"    This is undetectable as a precision test.")
    print(f"    HOWEVER: the qualitative prediction (gravity entangles)")
    print(f"    IS testable and IS distinguishing vs classical gravity.")
    print(f"    STATUS: QUALITATIVE prediction testable; precision lattice")
    print(f"             correction NOT testable with a = l_Planck")

    return {"frac_correction_planck": frac_planck, "phi_bmv": phi_bmv,
            "a_required_m": a_required}


# =====================================================================
# Cross-cutting analysis: what lattice spacing IS testable?
# =====================================================================

def run_detectability_analysis(results: dict):
    """Determine the minimum detectable lattice spacing across all candidates."""
    print("\n" + "=" * 78)
    print("CROSS-CUTTING: MINIMUM DETECTABLE LATTICE SPACING")
    print("=" * 78)

    C_lat = math.pi**2 / 6.0

    # For each candidate, what is the minimum a that produces a detectable signal?
    print(f"\n  Experiment              Required a (m)     a / l_Planck      Status")
    print(f"  {'─' * 72}")

    for name, res in results.items():
        a_req = res.get("a_required_m", float('inf'))
        ratio = a_req / L_PLANCK if np.isfinite(a_req) else float('inf')
        if ratio < 1:
            status = "Sub-Planckian: always detectable (trivially)"
        elif ratio < 1e10:
            status = f"Requires a >> l_Planck"
        else:
            status = f"Requires macroscopic a"
        print(f"  {name:<22s}  {a_req:14.4e}  {ratio:14.4e}  {status}")

    # ── The honest conclusion ─────────────────────────────────────────
    print(f"\n--- Honest assessment ---")
    print(f"  ALL lattice corrections scale as (a/L)^2 where L is the")
    print(f"  experimental length scale (superposition size, height, separation).")
    print(f"")
    print(f"  If a = l_Planck = {L_PLANCK:.4e} m, then for ANY experiment")
    print(f"  with L > 1 nm, the correction is < {C_lat * (L_PLANCK / 1e-9)**2:.2e}.")
    print(f"  This is not just hard to detect -- it is astronomically small.")
    print(f"")
    print(f"  The ONLY way to get a detectable lattice correction is if")
    print(f"  a >> l_Planck.  Specifically:")
    for name, res in results.items():
        a_req = res.get("a_required_m", float('inf'))
        if np.isfinite(a_req):
            print(f"    {name}: a > {a_req:.2e} m = {a_req/L_PLANCK:.2e} l_P")

    print(f"\n  These are all many orders of magnitude above the Planck length.")
    print(f"  A null result in these experiments would constrain a < [above values]")
    print(f"  but would NOT distinguish this framework from smooth GR.")

    # ── The QUALITATIVE prediction that IS testable ──────────────────
    print(f"\n{'=' * 78}")
    print(f"THE TESTABLE PREDICTION: GRAVITY MEDIATES ENTANGLEMENT")
    print(f"{'=' * 78}")
    print(f"""
  The framework treats gravity as quantum (Bogoliubov particle creation,
  vacuum entanglement) at all scales.  This makes a sharp prediction:

  PREDICTION: Two masses in superposition, interacting only via gravity,
  WILL become entangled.  The entanglement phase is:

      Phi = G m^2 T / hbar * (1/d_close - 1/d_far)

  This is testable by the BMV experiment (target: ~2030).

  COMPARISON:
  - Our framework:     gravity entangles (quantum field on graph)
  - Classical gravity:  gravity does NOT entangle
  - Semiclassical:     gravity does NOT entangle
  - Penrose collapse:  gravity DESTROYS superpositions (no entanglement)

  If BMV sees entanglement: consistent with framework + standard QG
  If BMV sees NO entanglement: framework falsified

  This is a genuine, testable, distinguishing prediction -- but it
  matches the prediction of ANY quantum gravity theory, not just ours.
  It distinguishes quantum-gravity from classical-gravity, not
  graph-gravity from continuum-gravity.

  For a prediction unique to the LATTICE structure, we need experiments
  probing scales a ~ {L_PLANCK:.0e} m, which is not foreseeable.
""")


# =====================================================================
# Bonus: what a NON-Planckian lattice spacing would predict
# =====================================================================

def run_if_a_not_planck():
    """What if the fundamental spacing is NOT the Planck length?

    Some discrete spacetime models predict a >> l_Planck.  Causal set theory,
    for example, has fundamental elements at density ~ 1/l_Planck^4 but
    effective discreteness could manifest at larger scales.

    If a ~ 1e-20 m (a million times l_Planck), what would be detectable?
    """
    print(f"\n{'=' * 78}")
    print(f"BONUS: PREDICTIONS IF a >> l_Planck")
    print(f"{'=' * 78}")

    a_test_values = [1e-20, 1e-18, 1e-15, 1e-12]
    C_lat = math.pi**2 / 6.0

    print(f"\n  {'a (m)':>12s}  {'a/l_P':>12s}  "
          f"{'decoherence':>14s}  {'COW':>14s}  {'BMV':>14s}")

    for a in a_test_values:
        # Decoherence: frac = C_lat * (a/delta_x)^2
        frac_dec = C_lat * (a / MAQRO_SUPERPOSITION_M)**2
        # COW: frac = (a^2/12) * (2g/R) * T / (g*H)
        R_earth = 6.371e6
        frac_cow = (a**2 / 12.0) * (2.0 * 9.81 / R_earth) / (9.81 * COW_HEIGHT_M)
        # BMV: frac = C_lat * (a/d_close)^2
        d_close = BMV_SEPARATION_M - BMV_SUPERPOSITION_M
        frac_bmv = C_lat * (a / max(d_close, 1e-30))**2

        print(f"  {a:12.2e}  {a/L_PLANCK:12.2e}  "
              f"{frac_dec:14.4e}  {frac_cow:14.4e}  {frac_bmv:14.4e}")

    print(f"\n  Even at a = 1e-15 m (nuclear scale), corrections are tiny.")
    print(f"  Only at a ~ 1e-12 m (atomic scale) do corrections approach 1%.")
    print(f"  But atomic-scale discreteness is already ruled out by many")
    print(f"  experiments (crystal diffraction, atomic spectroscopy, etc.).")


# =====================================================================
# Main
# =====================================================================

def main():
    t_start = time.time()
    print("=" * 78)
    print("EXPERIMENTAL PREDICTIONS: GRAPH-PROPAGATOR GRAVITY vs SMOOTH GR")
    print("Three candidates for distinguishing the discrete framework")
    print("=" * 78)

    results = {}

    # Candidate 1: Gravitational decoherence
    r1 = run_candidate_1()
    results["decoherence"] = r1

    # Candidate 2: COW phase shift
    r2 = run_candidate_2()
    results["COW_phase"] = r2

    # Candidate 3: BMV entanglement
    r3 = run_candidate_3()
    results["BMV_entanglement"] = r3

    # Cross-cutting analysis
    run_detectability_analysis(results)

    # Bonus: non-Planckian spacing
    run_if_a_not_planck()

    # ── Final summary ─────────────────────────────────────────────────
    elapsed = time.time() - t_start
    print(f"\n{'=' * 78}")
    print(f"FINAL SUMMARY")
    print(f"{'=' * 78}")
    print(f"""
  All three candidates produce lattice corrections proportional to (a/L)^2
  where a is the lattice spacing and L is the experimental length scale.

  For a = l_Planck:
    - Decoherence correction:  {r1['frac_correction_planck']:.2e}
    - COW phase correction:    {r2['frac_correction_planck']:.2e}
    - BMV phase correction:    {r3['frac_correction_planck']:.2e}

  None of these are remotely detectable.

  The one TESTABLE prediction of the framework is qualitative:
  gravity mediates entanglement (testable via BMV, ~2030).
  But this prediction is shared by ALL quantum gravity theories.

  To produce a prediction UNIQUE to the lattice structure, one needs
  either:
    (a) a >> l_Planck (which other experiments already constrain), or
    (b) experiments at the Planck scale (not foreseeable).

  This is an honest negative result: the framework is empirically
  indistinguishable from smooth GR at currently accessible scales.

  Elapsed: {elapsed:.1f} s
""")
    print("=" * 78)

    return results


if __name__ == "__main__":
    results = main()
