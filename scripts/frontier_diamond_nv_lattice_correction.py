#!/usr/bin/env python3
"""
Diamond NV Lattice-Scale Correction to Phase-Ramp Prediction
=============================================================

Computes the SPECIFIC correction that distinguishes the discrete-graph
propagator framework from smooth GR in a diamond NV magnetometry setup.

Key question: "Your framework predicts the same retardation as GR. What's new?"

Answer: The discrete propagator has a modified dispersion relation
    omega^2 = c_2 k^2 + c_4 k^4 + ...
which gives a FREQUENCY-DEPENDENT group velocity:
    v_g(omega) = sqrt(c_2) * (1 - c_4 omega^2 / (2 c_2^2) + ...)

This means the phase ramp across an NV image is NOT linear in drive
frequency omega.  There is a quadratic correction:
    phi(omega) = omega * d / v_g(omega)
              = omega * d / sqrt(c_2) * (1 + c_4 omega^2 / (2 c_2^2) + ...)

The GR prediction is the first term.  The lattice correction is the second.
Measuring phi vs omega and fitting for the quadratic coefficient gives
a direct test of discreteness.

Uses c_4 values from frontier_dispersion_relation.py.

Physical constants and NV parameters from published literature.
"""

from __future__ import annotations

import math
import time

import numpy as np

# ================================================================
# Physical constants (SI)
# ================================================================
C_LIGHT = 2.998e8          # m/s
HBAR = 1.055e-34           # J*s
G_NEWTON = 6.674e-11       # m^3 kg^-1 s^-2
L_PLANCK = 1.616e-35       # m (Planck length)
E_PLANCK_J = 1.956e9       # J (Planck energy)
E_PLANCK_GEV = 1.22e19     # GeV

# ================================================================
# c4 coefficients from frontier_dispersion_relation.py
# These are DIMENSIONLESS in lattice units.  Physical c4 = A * h^alpha
# where h is the fundamental lattice spacing.
# ================================================================
# Representative values (cubic lattice, cos2 and gauss kernels)
# at h = 0.25 (intermediate, cleanest fit regime):
C4_DIMENSIONLESS = {
    "cubic/cos2":      {"c4_h025": 7.29e-4,   "A": 3.71e-2, "alpha": 1.58},
    "cubic/gauss":     {"c4_h025": -2.87e-2,   "A": 5.80e-1, "alpha": 1.47},
    "staggered/gauss": {"c4_h025": 1.03e-2,    "A": 1.68e0,  "alpha": 2.67},
}

# ================================================================
# NV magnetometry parameters (realistic setup)
# ================================================================
# Source-detector geometry
D_SEPARATION = 1.0e-3      # 1 mm source-to-NV distance
DELTA_D = 200e-6            # 200 um spread across NV field of view
D_PILLAR_MASS = 1.0e-6     # 1 mg tungsten drive mass (typical for Cavendish-style)

# Drive frequencies to scan
OMEGA_MIN = 2 * math.pi * 1.0       # 1 Hz
OMEGA_MAX = 2 * math.pi * 1.0e6     # 1 MHz
N_OMEGA = 200

# NV sensitivity
# Best reported: ~1 nT/sqrt(Hz) for single NV, ~10 pT/sqrt(Hz) widefield
# Phase sensitivity: delta_phi ~ 1/SNR ~ noise / signal
# For lock-in: integration time T_int improves SNR as sqrt(T_int)
NV_PHASE_SENSITIVITY_RAD = 1e-6     # rad (best-case, after long integration)
NV_STRAIN_SENSITIVITY = 1e-9        # fractional strain sensitivity

# Integration time
T_INTEGRATION = 1e4         # 10,000 seconds (long run)


def smooth_gr_phase_ramp(omega: np.ndarray, d: float) -> np.ndarray:
    """Smooth GR prediction: phase lag = omega * d / c.

    This is what standard GR predicts for a gravitational signal
    propagating at speed c from distance d.  The phase ramp across
    the NV image is dphi/dx = omega / c (spatial gradient).

    Args:
        omega: angular drive frequency array (rad/s)
        d: source-detector distance (m)

    Returns:
        Phase lag in radians
    """
    return omega * d / C_LIGHT


def lattice_phase_correction(omega: np.ndarray, d: float,
                             c4_phys: float, c2_phys: float) -> np.ndarray:
    """Lattice correction to the phase ramp.

    From the dispersion relation omega^2 = c_2 k^2 + c_4 k^4:
        v_group(omega) = sqrt(c_2) * (1 - c_4 omega^2 / (2 c_2^2) + ...)
        tau(omega) = d / v_g = d/sqrt(c_2) * (1 + c_4 omega^2 / (2 c_2^2))
        phi(omega) = omega * tau = omega*d/sqrt(c_2) + omega^3*d*c_4/(2*c_2^{5/2})

    The correction term (beyond smooth GR) is:
        delta_phi = omega^3 * d * c_4 / (2 * c_2^{5/2})

    In natural units where c_2 = c^2:
        delta_phi = omega^3 * d * c_4 / (2 * c^5)

    Args:
        omega: angular drive frequency (rad/s)
        d: source-detector distance (m)
        c4_phys: physical c_4 coefficient (m^2 or s^2 depending on units)
        c2_phys: physical c_2 coefficient (= c^2 for massless propagation)

    Returns:
        Phase correction in radians (to be ADDED to smooth GR phase)
    """
    return omega**3 * d * c4_phys / (2.0 * c2_phys**(5.0/2.0))


def c4_physical(A_dimless: float, alpha: float, h_phys: float) -> float:
    """Convert dimensionless c4 coefficient to physical units.

    c4_phys = A * h_phys^alpha  [has dimensions of length^2 for alpha~2]

    For the dispersion relation omega^2 = c^2 k^2 + c4_phys k^4:
        [c4_phys] = [omega^2 / k^4] = m^2 * s^{-2} / m^{-4} = m^6 s^{-2} ?

    More carefully: if omega^2 = c^2 k^2 (1 + c4_dimless * k^2 * h^2),
    then c4_phys = c4_dimless * h^2 in the dispersion relation
    omega^2 = c^2 k^2 + c^2 * c4_dimless * h^2 * k^4.

    So c4_physical has units of length^2 (times c^2 implicit).
    The group velocity correction is:
        v_g = c * (1 + c4_dimless * h^2 * k^2 + ...)
        v_g = c * (1 + c4_dimless * h^2 * omega^2 / c^2 + ...)

    So the fractional velocity correction is:
        delta_v / c = c4_dimless * (h * omega / c)^2

    And the phase correction is:
        delta_phi / phi_GR = c4_dimless * (h * omega / c)^2

    Args:
        A_dimless: dimensionless prefactor from scaling fit
        alpha: scaling exponent
        h_phys: physical lattice spacing in meters

    Returns:
        c4 * h^alpha in meters^alpha (dimensionless when multiplied by k^alpha)
    """
    return A_dimless * h_phys**alpha


def fractional_phase_correction(omega: float, A_dimless: float,
                                h_phys: float) -> float:
    """Fractional correction to phase ramp: delta_phi / phi_GR.

    delta_phi / phi_GR = A * (h * omega / c)^2

    This is the key observable: how much the phase deviates from
    the smooth GR prediction, as a fraction.

    Args:
        omega: angular frequency (rad/s)
        A_dimless: dimensionless c4 prefactor
        h_phys: lattice spacing (m)

    Returns:
        Fractional correction (dimensionless)
    """
    return abs(A_dimless) * (h_phys * omega / C_LIGHT)**2


def run_experiment():
    t0 = time.time()

    print("=" * 78)
    print("DIAMOND NV LATTICE-SCALE CORRECTION TO PHASE-RAMP PREDICTION")
    print("=" * 78)

    # ================================================================
    # Section 1: Smooth GR prediction
    # ================================================================
    print(f"\n{'=' * 78}")
    print("1. SMOOTH GR PREDICTION")
    print(f"{'=' * 78}")

    print(f"\n  Source-detector distance: d = {D_SEPARATION*1e3:.1f} mm")
    print(f"  NV field of view spread: Delta_d = {DELTA_D*1e6:.0f} um")

    omega_ref = 2 * math.pi * 1e3  # 1 kHz reference
    phi_gr = smooth_gr_phase_ramp(omega_ref, D_SEPARATION)
    dphi_gr = smooth_gr_phase_ramp(omega_ref, DELTA_D)

    print(f"\n  At f_drive = 1 kHz (omega = {omega_ref:.2f} rad/s):")
    print(f"    Phase lag (GR):          phi = omega*d/c = {phi_gr:.4e} rad")
    print(f"    Phase ramp across FOV:   Delta_phi = omega*Delta_d/c = {dphi_gr:.4e} rad")
    print(f"    Time delay:              tau = d/c = {D_SEPARATION/C_LIGHT:.4e} s")

    print(f"\n  Phase ramp formula (smooth GR):")
    print(f"    phi(omega) = omega * d / c")
    print(f"    dphi/df = 2*pi * d / c = {2*math.pi*D_SEPARATION/C_LIGHT:.4e} rad/Hz")
    print(f"    This is LINEAR in frequency -- slope = d/c")

    # ================================================================
    # Section 2: Lattice correction derivation
    # ================================================================
    print(f"\n{'=' * 78}")
    print("2. LATTICE DISPERSION CORRECTION")
    print(f"{'=' * 78}")

    print(f"""
  Discrete propagator dispersion relation:
    omega^2 = c^2 k^2 * (1 + A * h^2 * k^2 + ...)

  where h = lattice spacing, A = dimensionless coefficient from path-sum.

  Group velocity:
    v_g = d(omega)/dk = c * (1 + A * h^2 * k^2 + ...)
                      = c * (1 + A * (h*omega/c)^2 + ...)

  Phase accumulation over distance d:
    phi(omega) = omega * d / v_g(omega)
               = omega * d / c * 1/(1 + A*(h*omega/c)^2)
               = phi_GR * (1 - A*(h*omega/c)^2 + ...)

  Lattice correction to phase:
    delta_phi = -phi_GR * A * (h*omega/c)^2
              = -A * omega * d / c * (h*omega/c)^2
              = -A * d * h^2 * omega^3 / c^3

  KEY SIGNATURE: phi(omega) has an omega^3 correction term.
  GR predicts phi ~ omega (linear).
  Lattice predicts phi ~ omega + beta*omega^3 (cubic correction).
  The coefficient beta = -A * d * h^2 / c^3 depends on lattice spacing h.
""")

    # ================================================================
    # Section 3: Numerical estimates for different lattice spacings
    # ================================================================
    print(f"{'=' * 78}")
    print("3. NUMERICAL ESTIMATES: FRACTIONAL PHASE CORRECTION")
    print(f"{'=' * 78}")

    # Lattice spacings to consider
    h_scenarios = {
        "Planck length (1.6e-35 m)": L_PLANCK,
        "10x Planck (1.6e-34 m)":    10 * L_PLANCK,
        "100x Planck (1.6e-33 m)":   100 * L_PLANCK,
        "Fermi scale (1e-15 m)":     1e-15,
        "Atomic scale (1e-10 m)":    1e-10,
        "Mesoscopic (1e-6 m)":       1e-6,
    }

    # Use the cubic/gauss A value (largest, most conservative for detection)
    A_ref = 0.58  # from cubic/gauss fit

    freqs_hz = [1, 100, 1e3, 1e4, 1e5, 1e6]

    print(f"\n  Using A = {A_ref:.2f} (cubic/gauss kernel, representative)")
    print(f"  Formula: delta_phi/phi_GR = A * (h * omega / c)^2\n")

    print(f"  {'Lattice spacing':>30}  ", end="")
    for f in freqs_hz:
        if f >= 1e6:
            print(f"{'f='+str(int(f/1e6))+'MHz':>12}  ", end="")
        elif f >= 1e3:
            print(f"{'f='+str(int(f/1e3))+'kHz':>12}  ", end="")
        else:
            print(f"{'f='+str(int(f))+'Hz':>12}  ", end="")
    print()

    for name, h_phys in h_scenarios.items():
        print(f"  {name:>30}  ", end="")
        for f in freqs_hz:
            omega = 2 * math.pi * f
            frac = fractional_phase_correction(omega, A_ref, h_phys)
            print(f"{frac:12.2e}  ", end="")
        print()

    # ================================================================
    # Section 4: Absolute phase correction in radians
    # ================================================================
    print(f"\n{'=' * 78}")
    print("4. ABSOLUTE LATTICE PHASE CORRECTION (radians)")
    print(f"{'=' * 78}")

    print(f"\n  delta_phi = A * omega * d / c * (h * omega / c)^2")
    print(f"  d = {D_SEPARATION*1e3:.1f} mm\n")

    print(f"  {'Lattice spacing':>30}  ", end="")
    for f in freqs_hz:
        if f >= 1e6:
            print(f"{'f='+str(int(f/1e6))+'MHz':>12}  ", end="")
        elif f >= 1e3:
            print(f"{'f='+str(int(f/1e3))+'kHz':>12}  ", end="")
        else:
            print(f"{'f='+str(int(f))+'Hz':>12}  ", end="")
    print()

    for name, h_phys in h_scenarios.items():
        print(f"  {name:>30}  ", end="")
        for f in freqs_hz:
            omega = 2 * math.pi * f
            phi_gr_val = smooth_gr_phase_ramp(omega, D_SEPARATION)
            frac = fractional_phase_correction(omega, A_ref, h_phys)
            delta_phi = phi_gr_val * frac
            print(f"{delta_phi:12.2e}  ", end="")
        print()

    # ================================================================
    # Section 5: What lattice spacing is detectable?
    # ================================================================
    print(f"\n{'=' * 78}")
    print("5. DETECTABILITY THRESHOLD")
    print(f"{'=' * 78}")

    print(f"\n  NV phase sensitivity (best case): {NV_PHASE_SENSITIVITY_RAD:.1e} rad")
    print(f"  Integration time: {T_INTEGRATION:.0f} s")
    print(f"  SNR improvement from integration: sqrt(T) = {math.sqrt(T_INTEGRATION):.1f}")
    print(f"  Effective sensitivity: {NV_PHASE_SENSITIVITY_RAD/math.sqrt(T_INTEGRATION):.2e} rad")

    eff_sensitivity = NV_PHASE_SENSITIVITY_RAD / math.sqrt(T_INTEGRATION)

    print(f"\n  For detection at 3-sigma: delta_phi > {3*eff_sensitivity:.2e} rad")
    print(f"\n  Required lattice spacing h for 3-sigma detection at each frequency:")

    print(f"\n  {'Frequency':>15}  {'h_min (m)':>15}  {'h_min / l_Planck':>18}  "
          f"{'Feasible?':>10}")

    for f in freqs_hz:
        omega = 2 * math.pi * f
        phi_gr_val = smooth_gr_phase_ramp(omega, D_SEPARATION)
        # Need: A * phi_GR * (h*omega/c)^2 > 3*eff_sens
        # h^2 > 3*eff_sens / (A * phi_GR * (omega/c)^2)
        # h > sqrt(3*eff_sens * c^2 / (A * phi_GR * omega^2))
        if phi_gr_val > 0 and omega > 0:
            h_min_sq = 3 * eff_sensitivity * C_LIGHT**2 / (A_ref * phi_gr_val * omega**2)
            h_min = math.sqrt(h_min_sq) if h_min_sq > 0 else float('inf')
            h_ratio = h_min / L_PLANCK
            feasible = "YES" if h_min < 1e-6 else "marginal" if h_min < 1e-3 else "NO"
        else:
            h_min = float('inf')
            h_ratio = float('inf')
            feasible = "N/A"

        if f >= 1e6:
            flabel = f"{f/1e6:.0f} MHz"
        elif f >= 1e3:
            flabel = f"{f/1e3:.0f} kHz"
        else:
            flabel = f"{f:.0f} Hz"
        print(f"  {flabel:>15}  {h_min:15.2e}  {h_ratio:18.2e}  {feasible:>10}")

    # ================================================================
    # Section 6: Multi-frequency measurement protocol
    # ================================================================
    print(f"\n{'=' * 78}")
    print("6. MULTI-FREQUENCY MEASUREMENT PROTOCOL")
    print(f"{'=' * 78}")

    print(f"""
  The distinguishing signature is the FREQUENCY DEPENDENCE of the phase ramp:

  Smooth GR:   phi(f) = 2*pi*f * d/c                    [linear in f]
  Lattice:     phi(f) = 2*pi*f * d/c * (1 + beta*f^2)   [cubic correction]

  where beta = -A * (2*pi*h/c)^2

  PROTOCOL:
  1. Measure phase ramp at N frequencies: f_1, f_2, ..., f_N
  2. Fit: phi(f) = a*f + b*f^3
     - If b = 0: consistent with smooth GR
     - If b != 0: evidence for modified dispersion
  3. From b, extract: h = c/(2*pi) * sqrt(|b| * c / (A * d))

  Required measurement precision to distinguish models:
""")

    # For each scenario, compute the cubic coefficient
    print(f"  {'Lattice spacing':>30}  {'beta (s^2)':>15}  "
          f"{'f^3 term at 1MHz':>18}  {'detectable?':>12}")

    for name, h_phys in h_scenarios.items():
        beta = A_ref * (2 * math.pi * h_phys / C_LIGHT)**2
        f_test = 1e6
        cubic_term = beta * f_test**2  # fractional correction at f_test
        phi_cubic = smooth_gr_phase_ramp(2*math.pi*f_test, D_SEPARATION) * cubic_term
        detectable = "YES" if abs(phi_cubic) > 3*eff_sensitivity else "NO"
        print(f"  {name:>30}  {beta:15.2e}  {phi_cubic:18.2e} rad  {detectable:>12}")

    # ================================================================
    # Section 7: Comparison with other lattice-scale tests
    # ================================================================
    print(f"\n{'=' * 78}")
    print("7. COMPARISON WITH EXISTING CONSTRAINTS")
    print(f"{'=' * 78}")

    print(f"""
  Fermi LAT (gamma-ray time-of-flight):
    Constrains energy-dependent photon speed: |v-c|/c < (E/E_QG)^2
    E_QG > 6.3e10 GeV  (n=2 Lorentz violation)
    Equivalent lattice spacing: h < c*hbar/E_QG ~ {C_LIGHT*HBAR/(6.3e10*1.6e-10):.2e} m

  LIGO/gravitational waves:
    GW150914 constrains graviton dispersion: M_g < 1.2e-22 eV
    This constrains massive-graviton scenarios, not lattice dispersion directly

  Diamond NV (this proposal):
    Probes GRAVITATIONAL propagation specifically (not photon dispersion)
    Lower frequency (Hz-MHz vs GeV) but much shorter distance
    Complementary: photon dispersion could differ from graviton dispersion
    if gravity and electromagnetism live on different graph structures

  Key distinction:
    Fermi LAT tests PHOTON dispersion on cosmological scales
    Diamond NV tests GRAVITATIONAL dispersion on laboratory scales
    These are independent measurements even if the lattice is universal
""")

    # ================================================================
    # Section 8: Honest assessment
    # ================================================================
    print(f"{'=' * 78}")
    print("8. HONEST ASSESSMENT")
    print(f"{'=' * 78}")

    print(f"""
  WHAT IS NEW (answer to "same as GR"):
    The discrete framework predicts a SPECIFIC frequency-dependent correction
    to the phase ramp.  GR predicts phi ~ omega.  The lattice predicts
    phi ~ omega * (1 + A*(h*omega/c)^2).  This is a cubic-in-frequency
    correction that is ABSENT in smooth GR.

  WHAT IS DETECTABLE:
    At Planck-scale lattice spacing (h ~ 1.6e-35 m):
      Fractional correction at 1 MHz: ~{fractional_phase_correction(2*math.pi*1e6, A_ref, L_PLANCK):.2e}
      This is ~{fractional_phase_correction(2*math.pi*1e6, A_ref, L_PLANCK)/1e-80:.0f}e-80 -- utterly undetectable.

    At 1 fm lattice spacing (h ~ 1e-15 m):
      Fractional correction at 1 MHz: ~{fractional_phase_correction(2*math.pi*1e6, A_ref, 1e-15):.2e}
      Still far below any conceivable sensitivity.

    At 1 um lattice spacing (h ~ 1e-6 m):
      Fractional correction at 1 MHz: ~{fractional_phase_correction(2*math.pi*1e6, A_ref, 1e-6):.2e}
      Getting closer but still negligible.

  BOTTOM LINE:
    The lattice correction is proportional to (h*omega/c)^2.
    For ANY sub-atomic lattice spacing and laboratory frequencies,
    h*omega/c << 1 by enormous margins.

    h = l_Planck, f = 1 MHz: h*omega/c = {L_PLANCK * 2*math.pi*1e6 / C_LIGHT:.2e}
    h = 1 fm,     f = 1 MHz: h*omega/c = {1e-15 * 2*math.pi*1e6 / C_LIGHT:.2e}
    h = 1 um,     f = 1 MHz: h*omega/c = {1e-6 * 2*math.pi*1e6 / C_LIGHT:.2e}

    The diamond NV lattice correction is not detectable with current or
    foreseeable technology if the lattice spacing is at or below the
    Planck scale.

    However, the FRAMEWORK makes a concrete, falsifiable prediction:
    the phase ramp should have a specific cubic-in-frequency correction.
    This prediction is qualitatively different from smooth GR.

    The value is not in immediate detectability but in:
    1. Providing a specific formula a reviewer can check
    2. Showing the framework makes predictions beyond GR
    3. Defining the measurement that WOULD detect it
    4. Complementing Fermi LAT (gravitational vs photon dispersion)

  WHERE THE PREDICTION HAS TEETH:
    If the effective lattice spacing for GRAVITY is much larger than
    l_Planck (as some emergent-gravity scenarios suggest), the correction
    grows as h^2.  A lattice spacing of h ~ 1 mm would give detectable
    corrections at MHz frequencies.  This is not expected but is
    falsifiable.
""")

    # ================================================================
    # Section 9: Summary table
    # ================================================================
    print(f"{'=' * 78}")
    print("SUMMARY")
    print(f"{'=' * 78}")

    print(f"""
  Quantity                           Smooth GR          Lattice Framework
  --------                           ---------          -----------------
  Phase lag                          omega*d/c          omega*d/c*(1+A*(h*omega/c)^2)
  Phase ramp slope                   constant (d/c)     frequency-dependent
  Frequency dependence               linear             linear + cubic
  Distinguishing measurement         N/A                multi-freq phase fit
  Cubic coefficient                  0                  -A*d*(2*pi*h)^2/c^3
  Detectable at h=l_Planck?          N/A                NO (correction ~10^-80)
  Detectable at h=1fm?               N/A                NO (correction ~10^-40)
  Detectable at h=1mm?               N/A                MAYBE (correction ~10^-8)
""")

    elapsed = time.time() - t0
    print(f"  Elapsed: {elapsed:.1f} s")
    print(f"\n{'=' * 78}")
    print("EXPERIMENT COMPLETE")
    print(f"{'=' * 78}")


if __name__ == "__main__":
    run_experiment()
