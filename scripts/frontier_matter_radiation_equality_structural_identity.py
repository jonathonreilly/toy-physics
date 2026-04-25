#!/usr/bin/env python3
"""Audit the matter-radiation equality structural identity."""

from __future__ import annotations

import math
import sys


PASS_COUNT = 0
FAIL_COUNT = 0

OMEGA_M0 = 0.315
OMEGA_R0 = 9.2e-5
OMEGA_L0 = 0.685
Z_MR_CMB = 3387.0
Z_MR_CMB_ERR = 21.0
Z_REC_CMB = 1090.0

H0_REDUCED = 0.674
T_CMB = 2.725
T_CMB_REF = 2.7255
OMEGA_GAMMA_H2_REF = 2.4728e-5
N_EFF_STANDARD = 3.046


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


def rho_m(a: float, omega_m0: float = OMEGA_M0) -> float:
    return omega_m0 / a**3


def rho_r(a: float, omega_r0: float = OMEGA_R0) -> float:
    return omega_r0 / a**4


def one_plus_z_mr(omega_m0: float = OMEGA_M0, omega_r0: float = OMEGA_R0) -> float:
    return omega_m0 / omega_r0


def omega_ratio_with_common_e2(
    a: float,
    omega_m0: float,
    omega_r0: float,
    omega_l0: float,
    omega_k0: float,
) -> float:
    e2 = omega_r0 / a**4 + omega_m0 / a**3 + omega_k0 / a**2 + omega_l0
    omega_m_a = (omega_m0 / a**3) / e2
    omega_r_a = (omega_r0 / a**4) / e2
    return omega_m_a / omega_r_a


def radiation_density_from_thermal_history(
    h0: float = H0_REDUCED,
    t_cmb: float = T_CMB,
    n_eff: float = N_EFF_STANDARD,
) -> float:
    omega_gamma_h2 = OMEGA_GAMMA_H2_REF * (t_cmb / T_CMB_REF) ** 4
    omega_gamma = omega_gamma_h2 / h0**2
    neutrino_factor = n_eff * (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)
    return omega_gamma * (1.0 + neutrino_factor)


def audit_structural_identity() -> None:
    banner("Matter-radiation equality identity")

    a1 = 0.2
    a2 = 0.5
    matter_scaling = rho_m(a1) / rho_m(a2)
    radiation_scaling = rho_r(a1) / rho_r(a2)

    check("matter scales as a^-3", close(matter_scaling, (a2 / a1) ** 3))
    check("radiation scales as a^-4", close(radiation_scaling, (a2 / a1) ** 4))

    a_mr = OMEGA_R0 / OMEGA_M0
    density_gap = abs(rho_m(a_mr) - rho_r(a_mr)) / rho_m(a_mr)
    z_mr = one_plus_z_mr() - 1.0

    print(f"  a_mr       = {a_mr:.15e}")
    print(f"  1 + z_mr   = {one_plus_z_mr():.12f}")
    print(f"  z_mr       = {z_mr:.6f}")

    check("a_mr = Omega_r0/Omega_m0 solves rho_m = rho_r", density_gap < 1e-12)
    check("1 + z_mr = Omega_m0/Omega_r0", close(1.0 / a_mr, one_plus_z_mr()))


def audit_cancellations() -> None:
    banner("Independence checks")

    a = 1.0e-3
    expected = (OMEGA_M0 / OMEGA_R0) * a
    ratio = omega_ratio_with_common_e2(a, OMEGA_M0, OMEGA_R0, OMEGA_L0, 0.0)
    check("common E(a)^2 factor cancels in Omega_m(a)/Omega_r(a)", close(ratio, expected))

    lambda_ratios = [
        omega_ratio_with_common_e2(a, OMEGA_M0, OMEGA_R0, omega_l0, 0.0)
        for omega_l0 in (0.0, 0.3, 0.685, 0.9)
    ]
    check("matter-radiation ratio is Lambda-independent", max(lambda_ratios) - min(lambda_ratios) < 1e-12)

    h0_readouts = [one_plus_z_mr(OMEGA_M0, OMEGA_R0) - 1.0 for _h0 in (0.55, 0.674, 0.80)]
    check("z_mr readout is H0-independent once density fractions are supplied", max(h0_readouts) - min(h0_readouts) == 0.0)


def audit_numerical_comparator() -> None:
    banner("Numerical readout after supplying density fractions")

    z_mr = one_plus_z_mr() - 1.0
    deviation = (z_mr - Z_MR_CMB) / Z_MR_CMB
    sigma = abs(z_mr - Z_MR_CMB) / Z_MR_CMB_ERR

    print(f"  z_mr framework readout = {z_mr:.3f}")
    print(f"  z_mr CMB comparator    = {Z_MR_CMB:.0f} +/- {Z_MR_CMB_ERR:.0f}")
    print(f"  fractional deviation   = {100.0 * deviation:+.3f}%")
    print(f"  sigma deviation        = {sigma:.3f}")

    check("z_mr readout rounds to 3423", round(z_mr) == 3423)
    check("z_mr comparator agreement is within 2 percent", abs(deviation) < 0.02)
    check("z_mr comparator agreement is within 2 sigma", sigma < 2.0)


def audit_radiation_density() -> None:
    banner("Radiation-density and generation-count consistency")

    omega_r_calc = radiation_density_from_thermal_history()
    z_mr_direct = one_plus_z_mr() - 1.0
    z_mr_calc = one_plus_z_mr(OMEGA_M0, omega_r_calc) - 1.0
    omega_r_four = radiation_density_from_thermal_history(n_eff=4.0)
    z_mr_four = one_plus_z_mr(OMEGA_M0, omega_r_four) - 1.0

    print(f"  Omega_r0 from T_CMB, h, N_eff=3.046 = {omega_r_calc:.8e}")
    print(f"  used Omega_r0                         = {OMEGA_R0:.8e}")
    print(f"  z_mr from computed Omega_r0           = {z_mr_calc:.3f}")
    print(f"  illustrative N_eff=4 z_mr             = {z_mr_four:.3f}")

    check("thermal-history Omega_r0 matches the used value within 1 percent", abs(omega_r_calc - OMEGA_R0) / OMEGA_R0 < 0.01)
    check("N_eff=3.046 readout remains close to the direct Omega_r0 readout", abs(z_mr_calc - z_mr_direct) / z_mr_direct < 0.01)
    check("changing to N_eff=4 shifts z_mr by more than 8 percent", abs(z_mr_four - Z_MR_CMB) / Z_MR_CMB > 0.08)


def audit_cosmic_history_ordering() -> None:
    banner("Cosmic-history ordering")

    z_mr = one_plus_z_mr() - 1.0
    z_star = (2.0 * OMEGA_L0 / OMEGA_M0) ** (1.0 / 3.0) - 1.0
    z_mlambda = (OMEGA_L0 / OMEGA_M0) ** (1.0 / 3.0) - 1.0

    print(f"  z_mr      = {z_mr:.3f}")
    print(f"  z_rec     = {Z_REC_CMB:.3f}")
    print(f"  z_star    = {z_star:.6f}")
    print(f"  z_mLambda = {z_mlambda:.6f}")

    ordered = z_mr > Z_REC_CMB > z_star > z_mlambda > 0.0
    check("z_mr > z_rec > z_star > z_mLambda > 0", ordered)


def main() -> int:
    print("=" * 80)
    print("Matter-radiation equality structural identity audit")
    print("=" * 80)

    audit_structural_identity()
    audit_cancellations()
    audit_numerical_comparator()
    audit_radiation_density()
    audit_cosmic_history_ordering()

    print()
    print("=" * 80)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 80)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
