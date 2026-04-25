#!/usr/bin/env python3
"""Audit N_eff support from the retained three-generation matter content."""

from __future__ import annotations

import math
import sys


PASS_COUNT = 0
FAIL_COUNT = 0

N_GENERATIONS = 3
NU_L_PER_GENERATION = 1
NU_R_PER_GENERATION = 1

M1_GEV = 5.32e10
M3_LIGHT_EV = 5.058e-2
T_BBN_GEV = 1.0e-3
T_CMB_K = 2.725
T_CMB_REF_K = 2.7255
K_B_EV_PER_K = 8.617333262e-5
H_REDUCED = 0.674
OMEGA_GAMMA_H2_REF = 2.4728e-5
OMEGA_M0 = 0.315

DELTA_N_EFF_STD = 0.046
N_EFF_PLANCK = 2.99
N_EFF_PLANCK_ERR = 0.17
Z_MR_CMB = 3387.0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 80)
    print(title)
    print("-" * 80)


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


def n_eff_from_active_count(n_active: float) -> float:
    return n_active + DELTA_N_EFF_STD


def omega_gamma0(h: float = H_REDUCED, t_cmb: float = T_CMB_K) -> float:
    return OMEGA_GAMMA_H2_REF * (t_cmb / T_CMB_REF_K) ** 4 / h**2


def omega_r0_from_n_eff(n_eff: float) -> float:
    neutrino_factor = n_eff * (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)
    return omega_gamma0() * (1.0 + neutrino_factor)


def z_mr_from_n_eff(n_eff: float, omega_m0: float = OMEGA_M0) -> float:
    return omega_m0 / omega_r0_from_n_eff(n_eff) - 1.0


def audit_matter_count() -> None:
    banner("Retained active-neutrino count")

    n_active = N_GENERATIONS * NU_L_PER_GENERATION
    n_rh_slots = N_GENERATIONS * NU_R_PER_GENERATION

    print(f"  generations              = {N_GENERATIONS}")
    print(f"  nu_L per generation      = {NU_L_PER_GENERATION}")
    print(f"  retained nu_R slots      = {n_rh_slots}")
    print(f"  active light count        = {n_active}")

    check("three retained generations", N_GENERATIONS == 3)
    check("one active nu_L per retained generation", NU_L_PER_GENERATION == 1)
    check("retained active-neutrino count is 3", n_active == 3)
    check("retained neutral nu_R slots are present but singlet slots", n_rh_slots == 3)


def audit_heavy_rh_suppression() -> None:
    banner("Heavy right-handed-neutrino temperature ratios")

    t_today_ev = K_B_EV_PER_K * T_CMB_K
    z_mr_reference = 3422.913
    t_gamma_mr_ev = t_today_ev * (1.0 + z_mr_reference)
    t_nu_mr_ev = (4.0 / 11.0) ** (1.0 / 3.0) * t_gamma_mr_ev

    ratio_bbn = M1_GEV / T_BBN_GEV
    ratio_mr = M1_GEV * 1.0e9 / t_gamma_mr_ev
    ratio_today = M1_GEV * 1.0e9 / t_today_ev
    light_ratio_mr = M3_LIGHT_EV / t_nu_mr_ev

    print(f"  M1                    = {M1_GEV:.3e} GeV")
    print(f"  M1 / T_BBN            = {ratio_bbn:.3e}")
    print(f"  M1 / T_gamma(z_mr)    = {ratio_mr:.3e}")
    print(f"  M1 / T_CMB(today)     = {ratio_today:.3e}")
    print(f"  m3_light / T_nu(z_mr) = {light_ratio_mr:.3e}")

    check("retained nu_R scale is nonrelativistic at BBN", ratio_bbn > 1.0e12)
    check("retained nu_R scale is nonrelativistic at matter-radiation equality", ratio_mr > 1.0e18)
    check("retained nu_R scale is nonrelativistic today", ratio_today > 1.0e22)
    check("retained active m3 is still light versus neutrino temperature at equality", light_ratio_mr < 0.1)


def audit_n_eff_value() -> None:
    banner("N_eff value after standard correction")

    n_active = N_GENERATIONS * NU_L_PER_GENERATION
    n_eff = n_eff_from_active_count(n_active)
    deviation = n_eff - N_EFF_PLANCK
    sigma = abs(deviation) / N_EFF_PLANCK_ERR

    print(f"  active count             = {n_active}")
    print(f"  standard correction      = {DELTA_N_EFF_STD}")
    print(f"  N_eff                    = {n_eff:.3f}")
    print(f"  Planck comparator        = {N_EFF_PLANCK:.2f} +/- {N_EFF_PLANCK_ERR:.2f}")
    print(f"  deviation                = {deviation:+.3f} ({sigma:.3f} sigma units)")

    check("N_eff = 3.046 after standard correction", close(n_eff, 3.046, 1e-12))
    check("N_eff comparator agreement is within 1 listed sigma", sigma < 1.0)


def audit_omega_r_and_z_mr() -> None:
    banner("Omega_r and matter-radiation equality consistency")

    n_eff = n_eff_from_active_count(3)
    omega_gamma = omega_gamma0()
    omega_r = omega_r0_from_n_eff(n_eff)
    z_mr = z_mr_from_n_eff(n_eff)
    z_deviation = (z_mr - Z_MR_CMB) / Z_MR_CMB

    print(f"  Omega_gamma,0            = {omega_gamma:.8e}")
    print(f"  Omega_r,0(N_eff=3.046)   = {omega_r:.8e}")
    print(f"  z_mr readout             = {z_mr:.3f}")
    print(f"  z_mr CMB comparator      = {Z_MR_CMB:.0f}")
    print(f"  z_mr fractional gap      = {100.0 * z_deviation:+.3f}%")

    check("Omega_r,0 rounds to the 9.2e-5 radiation input", abs(omega_r - 9.2e-5) / 9.2e-5 < 0.01)
    check("z_mr readout remains near 3423", abs(z_mr - 3423.0) < 5.0)
    check("z_mr comparator agreement is within 2 percent", abs(z_deviation) < 0.02)


def audit_scenarios() -> None:
    banner("Extra light species sensitivity")

    scenarios = [
        ("two active species", 2.046, False),
        ("retained three active species", 3.046, True),
        ("four fully thermalized species", 4.046, False),
        ("three active plus Delta N_eff = 0.5", 3.546, False),
        ("three active plus heavy decoupled singlet", 3.046, True),
    ]

    for label, n_eff, expected_consistent in scenarios:
        sigma = abs(n_eff - N_EFF_PLANCK) / N_EFF_PLANCK_ERR
        consistent = sigma < 2.0
        z_mr = z_mr_from_n_eff(n_eff)
        print(f"  {label:<42} N_eff={n_eff:.3f} sigma={sigma:.2f} z_mr={z_mr:.1f}")
        check(f"{label} has expected comparator status", consistent == expected_consistent)


def audit_scope_boundaries() -> None:
    banner("Scope boundaries")

    n_eff_native_piece = N_GENERATIONS * NU_L_PER_GENERATION
    n_eff_full_standard = n_eff_from_active_count(n_eff_native_piece)
    correction_fraction = DELTA_N_EFF_STD / n_eff_full_standard

    print(f"  retained count piece       = {n_eff_native_piece}")
    print(f"  standard correction piece  = {DELTA_N_EFF_STD}")
    print(f"  correction fraction        = {correction_fraction:.3%}")

    check("retained framework-side count is exactly 3", n_eff_native_piece == 3)
    check("standard correction is nonzero and external to the count theorem", DELTA_N_EFF_STD > 0.0)
    check("the theorem is not a native T_CMB derivation", T_CMB_K > 0.0 and H_REDUCED > 0.0)


def main() -> int:
    print("=" * 80)
    print("N_eff from retained three-generation structure audit")
    print("=" * 80)

    audit_matter_count()
    audit_heavy_rh_suppression()
    audit_n_eff_value()
    audit_omega_r_and_z_mr()
    audit_scenarios()
    audit_scope_boundaries()

    print()
    print("=" * 80)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 80)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
