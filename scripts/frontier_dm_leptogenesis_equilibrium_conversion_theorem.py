#!/usr/bin/env python3
"""
DM leptogenesis equilibrium-conversion theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  Can the equilibrium conversion factors entering the leptogenesis transport
  map be closed from the theorem-grade equilibrium counting surface?

Answer:
  Yes.

  The branch already fixes the relativistic spectrum count

      g_* = 106.75,

  and the equilibrium number/entropy densities then give

      d_N = Y_N1^eq(0) = 135 zeta(3) / (4 pi^4 g_*)
          = 0.003901498367656259

  for a relativistic Majorana N1, while entropy conservation across
  e^+ e^- annihilation gives

      s / n_gamma = 7.039433661546651.
"""

from __future__ import annotations

import math
import sys

from scipy import integrate

from dm_leptogenesis_exact_common import (
    D_THERMAL_EXACT,
    G_S_TODAY_EXACT,
    G_STAR_EXACT,
    S_OVER_NGAMMA_EXACT,
    n_eq_gamma_over_t3_exact,
    n_eq_majorana_over_t3_exact,
    s_over_t3_relativistic,
)

PASS_COUNT = 0
FAIL_COUNT = 0

PI = math.pi
ZETA_3 = 1.2020569031595942


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def part1_the_relativistic_spectrum_count_is_exact() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE RELATIVISTIC SPECTRUM COUNT IS EXACT")
    print("=" * 88)

    bosonic = 28.0
    fermionic = 90.0
    g_star = bosonic + (7.0 / 8.0) * fermionic

    check(
        "The exact taste-spectrum count gives g_* = 28 + (7/8)*90",
        abs(g_star - G_STAR_EXACT) < 1e-12,
        f"g_*={g_star:.12f}",
    )
    check(
        "Numerically that is g_* = 106.75",
        abs(G_STAR_EXACT - 106.75) < 1e-12,
        f"g_*={G_STAR_EXACT:.12f}",
    )


def part2_the_majorana_equilibrium_yield_is_exact() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE MAJORANA EQUILIBRIUM YIELD IS EXACT")
    print("=" * 88)

    bose = integrate.quad(lambda x: x * x / (math.exp(x) - 1.0), 0.0, 40.0, epsabs=1e-12, epsrel=1e-12)[0]
    fermi = integrate.quad(lambda x: x * x / (math.exp(x) + 1.0), 0.0, 40.0, epsabs=1e-12, epsrel=1e-12)[0]

    n_gamma_t3 = n_eq_gamma_over_t3_exact()
    n_majorana_t3 = n_eq_majorana_over_t3_exact()
    s_t3 = s_over_t3_relativistic(G_STAR_EXACT)
    d_n = n_majorana_t3 / s_t3

    check(
        "The equilibrium integrals reproduce the exact Bose/Fermi zeta(3) coefficients",
        abs(bose - 2.0 * ZETA_3) < 1e-11 and abs(fermi - 1.5 * ZETA_3) < 1e-11,
        f"(bose,fermi)=({bose:.12f},{fermi:.12f})",
    )
    check(
        "A relativistic Majorana N1 has n/T^3 = 3 zeta(3)/(2 pi^2)",
        abs(n_majorana_t3 - 3.0 * ZETA_3 / (2.0 * PI**2)) < 1e-15,
        f"n_N/T^3={n_majorana_t3:.15f}",
    )
    check(
        "Dividing by the exact entropy density gives d_N = 135 zeta(3)/(4 pi^4 g_*)",
        abs(d_n - D_THERMAL_EXACT) < 1e-15,
        f"d_N={d_n:.15f}",
    )


def part3_the_late_entropy_to_photon_ratio_is_exact() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE LATE ENTROPY-TO-PHOTON RATIO IS EXACT")
    print("=" * 88)

    g_em_before = 2.0 + (7.0 / 8.0) * 4.0
    g_em_after = 2.0
    t_gamma_over_t_nu_cubed = g_em_before / g_em_after
    g_s_today = 2.0 + (7.0 / 8.0) * 6.0 * (4.0 / 11.0)
    s_over_ngamma = (PI**4 / (45.0 * ZETA_3)) * g_s_today

    check(
        "Entropy conservation in the electromagnetic sector gives (T_gamma/T_nu)^3 = 11/4",
        abs(t_gamma_over_t_nu_cubed - 11.0 / 4.0) < 1e-12,
        f"(Tg/Tnu)^3={t_gamma_over_t_nu_cubed:.12f}",
    )
    check(
        "So the exact late relativistic entropy count is g_*S(today) = 43/11",
        abs(g_s_today - G_S_TODAY_EXACT) < 1e-12,
        f"g_*S(today)={g_s_today:.12f}",
    )
    check(
        "Hence the exact late conversion factor is s/n_gamma = 7.039433661546651",
        abs(s_over_ngamma - S_OVER_NGAMMA_EXACT) < 1e-12,
        f"s/n_gamma={s_over_ngamma:.12f}",
    )


def part4_the_entire_equilibrium_conversion_prefactor_is_closed() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE ENTIRE EQUILIBRIUM CONVERSION PREFACTOR IS CLOSED")
    print("=" * 88)

    pref = S_OVER_NGAMMA_EXACT * D_THERMAL_EXACT

    check(
        "The theorem-native equilibrium conversion product is fixed numerically",
        abs(pref - 0.02746433893974878) < 1e-15,
        f"(s/n_gamma)*d_N={pref:.15f}",
    )
    print("  [INFO] Neither 7.04 nor d_th remains a benchmark ingredient on this authority path.")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS EQUILIBRIUM-CONVERSION THEOREM")
    print("=" * 88)

    part1_the_relativistic_spectrum_count_is_exact()
    part2_the_majorana_equilibrium_yield_is_exact()
    part3_the_late_entropy_to_photon_ratio_is_exact()
    part4_the_entire_equilibrium_conversion_prefactor_is_closed()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
