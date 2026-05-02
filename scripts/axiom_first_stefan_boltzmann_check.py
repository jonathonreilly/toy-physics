"""Axiom-first Stefan-Boltzmann check.

Verifies the Stefan-Boltzmann law on the framework's retained EW +
Lorentz + Block 01 KMS surface:

  u(T) = (pi^2 / 15) (k_B T)^4 / (hbar c)^3

(in natural units hbar = c = k_B = 1: u(T) = (pi^2 / 15) T^4).

Tests:
  T1: Planck distribution from KMS - n(omega, T) = 1/(exp(beta omega) - 1)
      via direct evaluation of the Gibbs trace on a single harmonic oscillator.
  T2: spectral energy density Planck spectrum integral - numerically
      integrate to recover (pi^2/15) T^4.
  T3: T^4 scaling - u(T)/T^4 is constant across a sweep of T values.
  T4: zeta(4) = pi^4 / 90 numerical check via the Bose-Einstein integral.
  T5: Wien displacement law - omega_max / T = 2.821 (Wien constant).
  T6: Stefan-Boltzmann constant in SI = 5.67 x 10^-8 W m^-2 K^-4.
"""
from __future__ import annotations

import math

import numpy as np


def planck_occupation(omega: float, T: float) -> float:
    """Planck distribution n(omega, T) = 1 / (exp(omega/T) - 1) (natural units)."""
    if T <= 0:
        return 0.0
    x = omega / T
    if x < 1e-15:
        return float("inf")
    return 1.0 / (math.exp(x) - 1.0)


def planck_occupation_from_gibbs(omega: float, T: float, n_max: int = 1000) -> float:
    """<a^dagger a>_beta = sum_n n e^{-beta n omega} / sum_n e^{-beta n omega}.

    This is Block 01 KMS applied to a single harmonic oscillator,
    using the Gibbs sum directly (not the closed-form Planck formula).
    """
    if T <= 0:
        return 0.0
    beta = 1.0 / T
    # Compute the partition function and <a^dagger a>
    Z = 0.0
    avg_n = 0.0
    for n in range(n_max):
        weight = math.exp(-beta * n * omega)
        Z += weight
        avg_n += n * weight
        if weight < 1e-300:
            break
    return avg_n / Z


def planck_energy_density(T: float, omega_max_factor: float = 30.0, n_pts: int = 1000) -> float:
    """Numerically integrate the Planck energy spectrum:

      u(T) = (1 / pi^2) integral_0^infty omega^3 / (exp(omega/T) - 1) domega

    in natural units (hbar = c = k_B = 1).

    omega_max = omega_max_factor * T (factor 30 captures > 99.99999% of integral).
    """
    omega_max = omega_max_factor * T
    omegas = np.linspace(omega_max / n_pts, omega_max, n_pts)
    integrand = omegas ** 3 / (np.exp(omegas / T) - 1.0)
    integral = np.trapezoid(integrand, omegas)
    return float(integral / math.pi ** 2)


def stefan_boltzmann_constant_SI() -> float:
    """sigma_SB = (pi^2 / 60) k_B^4 / (hbar^3 c^2) in SI units."""
    k_B = 1.380649e-23  # J/K
    hbar = 1.054571817e-34  # J s
    c = 2.99792458e8  # m/s
    return (math.pi ** 2 / 60) * (k_B ** 4) / (hbar ** 3 * c ** 2)


def main() -> None:
    print("=" * 72)
    print("AXIOM-FIRST STEFAN-BOLTZMANN CHECK")
    print("=" * 72)
    print()
    print("Setup:")
    print("  Block 01 KMS (Gibbs state on harmonic oscillator → Planck dist)")
    print("  retained framework EW + emergent Lorentz (3D photon dispersion)")
    print("  natural units hbar = c = k_B = 1")
    print()
    print("Stefan-Boltzmann: u(T) = (pi^2 / 15) T^4 in natural units")
    print()

    # ----- Test 1: Planck distribution via KMS Gibbs trace -----
    print("-" * 72)
    print("TEST 1: Planck distribution from KMS Gibbs trace")
    print("        n(omega, T) = 1 / (exp(omega/T) - 1)")
    print("-" * 72)
    print(f"  {'omega':>6}  {'T':>6}  {'<n> (Gibbs)':>14}  {'1/(e^x - 1)':>14}  {'|diff|':>10}")
    max_diff_t1 = 0.0
    for omega in [1.0, 2.0, 5.0]:
        for T in [0.5, 1.0, 2.0, 5.0]:
            n_gibbs = planck_occupation_from_gibbs(omega, T)
            n_formula = planck_occupation(omega, T)
            diff = abs(n_gibbs - n_formula)
            max_diff_t1 = max(max_diff_t1, diff)
            print(f"  {omega:>6.2f}  {T:>6.2f}  {n_gibbs:>14.8f}  {n_formula:>14.8f}  {diff:.2e}")
    print()
    print(f"  max |Gibbs - Planck formula| = {max_diff_t1:.3e}")
    t1_ok = max_diff_t1 < 1e-10
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: Stefan-Boltzmann from numerical spectrum integral -----
    print("-" * 72)
    print("TEST 2: u(T) = (pi^2/15) T^4 from Planck spectrum integral")
    print("-" * 72)
    sb_coef = math.pi ** 2 / 15
    print(f"  Stefan-Boltzmann coefficient (pi^2/15) = {sb_coef:.10f}")
    print()
    print(f"  {'T':>6}  {'u(T) numeric':>16}  {'(pi^2/15) T^4':>16}  {'ratio':>10}")
    max_resid_t2 = 0.0
    for T in [0.5, 1.0, 2.0, 5.0, 10.0]:
        u_num = planck_energy_density(T, omega_max_factor=50.0, n_pts=20000)
        u_form = sb_coef * T ** 4
        ratio = u_num / u_form
        resid = abs(u_num - u_form) / u_form
        max_resid_t2 = max(max_resid_t2, resid)
        print(f"  {T:>6.2f}  {u_num:>16.10e}  {u_form:>16.10e}  {ratio:>10.6f}")
    print()
    print(f"  max relative residual = {max_resid_t2:.3e}")
    t2_ok = max_resid_t2 < 1e-4  # numerical integration accuracy
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: T^4 scaling -----
    print("-" * 72)
    print("TEST 3: T^4 scaling — u(T) / T^4 is constant")
    print("-" * 72)
    print(f"  {'T':>6}  {'u(T) / T^4':>20}  {'(pi^2/15)':>14}  {'|diff|':>10}")
    coefs = []
    for T in np.linspace(0.5, 10.0, 7):
        u_num = planck_energy_density(T, omega_max_factor=50.0, n_pts=20000)
        coef = u_num / T ** 4
        diff = abs(coef - sb_coef)
        coefs.append(coef)
        print(f"  {T:>6.2f}  {coef:>20.10f}  {sb_coef:>14.10f}  {diff:.2e}")
    print()
    coef_std = np.std(coefs) / np.mean(coefs)
    print(f"  coefficient of variation in u/T^4 = {coef_std:.3e}")
    t3_ok = coef_std < 1e-4
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: zeta(4) = pi^4 / 90 via Bose-Einstein integral -----
    print("-" * 72)
    print("TEST 4: zeta(4) = pi^4 / 90 from Bose-Einstein integral")
    print("        integral_0^inf x^3 / (e^x - 1) dx = Gamma(4) zeta(4) = 6 * pi^4/90 = pi^4/15")
    print("-" * 72)
    xs = np.linspace(1e-6, 50.0, 100000)
    integrand = xs ** 3 / (np.exp(xs) - 1.0)
    bose_integral = np.trapezoid(integrand, xs)
    expected = math.pi ** 4 / 15.0
    diff_t4 = abs(bose_integral - expected) / expected
    print(f"  numeric integral = {bose_integral:.10f}")
    print(f"  pi^4 / 15        = {expected:.10f}")
    print(f"  relative diff    = {diff_t4:.3e}")
    t4_ok = diff_t4 < 1e-6
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: Wien displacement law -----
    print("-" * 72)
    print("TEST 5: Wien displacement law")
    print("        omega_max / T = x_max where x_max satisfies (3 - x) e^x = 3")
    print("        numerically x_max ≈ 2.82144")
    print("-" * 72)
    # Find max of x^3 / (e^x - 1) numerically
    from scipy.optimize import brentq
    # Derivative: d/dx [x^3/(e^x-1)] = 0 →  3 x^2 (e^x-1) - x^3 e^x = 0 → 3 (1 - e^-x) = x
    f = lambda x: 3 * (1 - math.exp(-x)) - x
    x_max = brentq(f, 2.0, 4.0)
    expected_wien = 2.821439372  # known value
    print(f"  numeric x_max from solver = {x_max:.6f}")
    print(f"  expected Wien constant     = {expected_wien:.6f}")
    diff_t5 = abs(x_max - expected_wien)
    print(f"  |diff| = {diff_t5:.3e}")
    t5_ok = diff_t5 < 1e-5
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: Stefan-Boltzmann constant in SI -----
    print("-" * 72)
    print("TEST 6: Stefan-Boltzmann constant sigma_SB in SI units")
    print("        sigma_SB = (pi^2/60) k_B^4 / (hbar^3 c^2)")
    print("-" * 72)
    sigma_computed = stefan_boltzmann_constant_SI()
    sigma_codata_2018 = 5.670374419e-8  # CODATA 2018 in W m^-2 K^-4
    diff_t6 = abs(sigma_computed - sigma_codata_2018) / sigma_codata_2018
    print(f"  computed sigma_SB       = {sigma_computed:.10e} W m^-2 K^-4")
    print(f"  CODATA 2018 sigma_SB    = {sigma_codata_2018:.10e} W m^-2 K^-4")
    print(f"  relative diff           = {diff_t6:.3e}")
    t6_ok = diff_t6 < 1e-7
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    # ----- Summary -----
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Test 1 (Planck dist from KMS Gibbs trace):    {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (u(T) = (pi^2/15) T^4 numerical):      {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (T^4 scaling u/T^4 = const):           {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (zeta(4) = pi^4/90):                   {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (Wien displacement law):               {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (sigma_SB in SI = CODATA 2018):        {'PASS' if t6_ok else 'FAIL'}")
    print()
    all_ok = t1_ok and t2_ok and t3_ok and t4_ok and t5_ok and t6_ok
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    print()
    print("Note: this runner verifies the Stefan-Boltzmann law via")
    print("(a) explicit Gibbs-trace evaluation of the Planck distribution")
    print("    (Test 1, the KMS step from Block 01),")
    print("(b) numerical integration of the Planck energy spectrum (Tests 2-3),")
    print("(c) the Bose-Einstein integral identity (Test 4),")
    print("(d) the Wien displacement law (Test 5), and")
    print("(e) the SI Stefan-Boltzmann constant matching CODATA 2018 (Test 6).")
    print("The proof in the companion theorem note composes Block 01 KMS")
    print("with retained framework EW + emergent Lorentz + 3D mode-counting.")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
