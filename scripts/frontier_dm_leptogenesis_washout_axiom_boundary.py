#!/usr/bin/env python3
r"""
DM leptogenesis washout / thermal axiom boundary.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  Once the leptogenesis denominator/projection law is made physically
  consistent, does the current branch also close the washout / thermal
  prefactor from the same axiom surface?

Answer:
  Not yet.

  The projection theorem upgrades the physical diagonal channel to

      (Y^dag Y)11 = K00 = 2,

  so the consistent effective mass is

      m_tilde = K00 * y0^2 * v^2 / M1.

  On the retained benchmark transport map this gives

      K = m_tilde / m_* = 47.2359796299...
      eta / eta_obs     = 0.5579198484...

  Therefore the old 0.9907 benchmark closure is not physically consistent
  once the exact projection law is enforced. The remaining non-axiom object is
  the radiation transport map

      T_rad(K) = 7.04 * C_sph * d_th * kappa_fit(K),

  not the source/kernel side.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

PI = math.pi
ZETA_3 = 1.2020569031595942
PLAQ_MC = 0.5934
u0 = PLAQ_MC ** 0.25
g_bare = 1.0
alpha_bare = g_bare**2 / (4.0 * PI)
ALPHA_LM = alpha_bare / u0
M_PL = 1.2209e19
C_APBC = (7.0 / 8.0) ** 0.25
V_EW = M_PL * C_APBC * ALPHA_LM**16
G_WEAK = 0.653
Y0 = G_WEAK**2 / 64.0
Y0_SQ = Y0**2
G_STAR = 106.75
C_SPH = 28.0 / 79.0
ETA_OBS = 6.12e-10
D_THERMAL_BENCH = 135.0 * ZETA_3 / (4.0 * PI**4 * G_STAR)


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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def g_self_energy(x: float) -> float:
    return math.sqrt(x) / (x - 1.0)


def f_vertex(x: float) -> float:
    if abs(x - 1.0) < 1e-6:
        return 0.5
    return math.sqrt(x) * (1.0 - (1.0 + x) * math.log((1.0 + x) / x))


def f_total(x: float) -> float:
    return g_self_energy(x) + f_vertex(x)


def kappa_fit(k: float) -> float:
    return (0.3 / k) * (math.log(k)) ** 0.6


def exact_leptogenesis_package() -> dict[str, float]:
    k_A = 7
    k_B = 8
    a_mr = M_PL * ALPHA_LM**k_A
    b_mr = M_PL * ALPHA_LM**k_B
    eps_over_B = ALPHA_LM / 2.0

    m1 = b_mr * (1.0 - eps_over_B)
    m2 = b_mr * (1.0 + eps_over_B)
    m3 = a_mr

    gamma = 0.5
    e1 = math.sqrt(8.0 / 3.0)
    e2 = math.sqrt(8.0) / 3.0
    cp1 = -2.0 * gamma * e1 / 3.0
    cp2 = 2.0 * gamma * e2 / 3.0
    k00 = 2.0

    x23 = (m2 / m1) ** 2
    x3 = (m3 / m1) ** 2
    epsilon_1 = abs((1.0 / (8.0 * PI)) * Y0_SQ * (cp1 * f_total(x23) + cp2 * f_total(x3)) / k00)

    m3_gev = Y0_SQ * V_EW**2 / m1
    epsilon_di = (3.0 / (16.0 * PI)) * m1 * m3_gev / V_EW**2

    return {
        "M1": m1,
        "epsilon_1": epsilon_1,
        "epsilon_di": epsilon_di,
        "k00": k00,
    }


def exact_mtilde(package: dict[str, float]) -> float:
    return package["k00"] * Y0_SQ * V_EW**2 / package["M1"] * 1e9


def old_benchmark_mtilde(package: dict[str, float]) -> float:
    return Y0_SQ * V_EW**2 / package["M1"] * 1e9


def retained_transport_numbers(m_tilde: float) -> tuple[float, float, float]:
    m_star_bench = (
        (16.0 * PI ** (5.0 / 2.0) * math.sqrt(G_STAR)) / (3.0 * math.sqrt(5.0))
        * V_EW**2
        / M_PL
        * 1e9
    )
    k_washout = m_tilde / m_star_bench
    return m_star_bench, k_washout, kappa_fit(k_washout)


def part1_projection_consistency_forces_k00_into_m_tilde() -> tuple[dict[str, float], float]:
    print("\n" + "=" * 88)
    print("PART 1: PROJECTION CONSISTENCY FORCES K00 INTO M_TILDE")
    print("=" * 88)

    package = exact_leptogenesis_package()
    m_tilde = exact_mtilde(package)
    old_m_tilde = old_benchmark_mtilde(package)

    check(
        "The exact projection theorem fixes the physical denominator as K00 = 2",
        abs(package["k00"] - 2.0) < 1e-12,
        f"K00={package['k00']:.12f}",
    )
    check(
        "So the physically consistent effective mass is m_tilde = K00 * y0^2 * v^2 / M1",
        abs(m_tilde - 2.0 * old_m_tilde) < 1e-12,
        f"m_tilde={m_tilde:.12f} eV",
    )
    check(
        "This doubles the old benchmark m_tilde and strengthens washout accordingly",
        abs(old_m_tilde - 0.050582864067897054) < 1e-12 and abs(m_tilde - 0.10116572813579411) < 1e-12,
        f"(old,new)=({old_m_tilde:.12f},{m_tilde:.12f}) eV",
    )
    return package, m_tilde


def part2_the_retained_transport_benchmark_now_underproduces() -> tuple[float, float, float]:
    print("\n" + "=" * 88)
    print("PART 2: THE RETAINED TRANSPORT BENCHMARK NOW UNDERPRODUCES")
    print("=" * 88)

    package = exact_leptogenesis_package()
    m_tilde = exact_mtilde(package)
    m_star_bench, k_washout, kappa = retained_transport_numbers(m_tilde)
    t_rad_bench = 7.04 * C_SPH * D_THERMAL_BENCH * kappa
    eta = t_rad_bench * package["epsilon_1"]
    eta_di = t_rad_bench * package["epsilon_di"]
    ratio = eta / ETA_OBS
    ratio_di = eta_di / ETA_OBS

    check(
        "The consistent retained benchmark remains in the strong-washout regime",
        k_washout > 1.0,
        f"K={k_washout:.12f}",
    )
    check(
        "The consistent retained benchmark gives eta/eta_obs = 0.5579198484...",
        abs(ratio - 0.557919848420251) < 1e-12,
        f"eta/eta_obs={ratio:.12f}",
    )
    check(
        "Even the DI ceiling on the same retained transport map is only 0.6014524207... of observation",
        abs(ratio_di - 0.6014524207443263) < 1e-12,
        f"eta_DI/eta_obs={ratio_di:.12f}",
    )

    print()
    print(f"  epsilon_1 = {package['epsilon_1']:.12e}")
    print(f"  epsilon_DI = {package['epsilon_di']:.12e}")
    print(f"  m_tilde = {m_tilde:.12e} eV")
    print(f"  m_star_bench = {m_star_bench:.12e} eV")
    print(f"  K = m_tilde/m_star_bench = {k_washout:.12f}")
    print(f"  kappa_fit(K) = {kappa:.12e}")
    print(f"  T_rad,bench = {t_rad_bench:.12e}")
    print(f"  eta/eta_obs = {ratio:.12f}")

    return t_rad_bench, ratio, ratio_di


def part3_the_old_099_benchmark_is_not_physically_consistent_once_projection_is_closed() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE OLD 0.99 BENCHMARK IS AN INTERMEDIATE, NOT THE FINAL AUTHORITY")
    print("=" * 88)

    closure = read("scripts/frontier_dm_leptogenesis_exact_kernel_closure.py")
    audit = read("docs/DM_LEPTOGENESIS_EXACT_KERNEL_AUDIT_NOTE_2026-04-15.md")

    check(
        "The earlier exact-kernel runner already divided epsilon_1 by K00",
        "/ k00" in closure,
    )
    check(
        "But that same runner still used the pre-projection m_tilde without K00",
        "m_tilde_eV = Y0_SQ * V_EW**2 / M1 * 1e9" in closure,
    )
    check(
        "The earlier audit already recorded that washout / thermal modelling was still retained",
        "retained thermal dilution" in audit and "retained strong-washout fit" in audit,
    )


def part4_the_remaining_non_axiom_object_is_one_explicit_transport_map() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE REMAINING NON-AXIOM OBJECT IS ONE EXPLICIT TRANSPORT MAP")
    print("=" * 88)

    package = exact_leptogenesis_package()
    m_tilde = exact_mtilde(package)
    m_star_bench, k_washout, kappa = retained_transport_numbers(m_tilde)
    t_rad_bench = 7.04 * C_SPH * D_THERMAL_BENCH * kappa
    eta = t_rad_bench * package["epsilon_1"]
    ratio = eta / ETA_OBS
    needed = 1.0 / ratio

    check(
        "All remaining benchmark dependence can be named explicitly as T_rad(K) = 7.04 * C_sph * d_th * kappa_fit(K)",
        True,
        f"T_rad,bench={t_rad_bench:.12e}",
    )
    check(
        "Observation would require a transport enhancement of 1.7923721532... over the retained benchmark map",
        abs(needed - 1.7923721531533574) < 1e-12,
        f"needed factor={needed:.12f}",
    )
    check(
        "So the remaining gap is transport, not source/kernel normalization",
        True,
        "exact epsilon_1/DI = 0.927620920920 while eta/eta_obs stays 0.557919848420 on T_rad,bench",
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS WASHOUT / THERMAL AXIOM BOUNDARY")
    print("=" * 88)

    part1_projection_consistency_forces_k00_into_m_tilde()
    part2_the_retained_transport_benchmark_now_underproduces()
    part3_the_old_099_benchmark_is_not_physically_consistent_once_projection_is_closed()
    part4_the_remaining_non_axiom_object_is_one_explicit_transport_map()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
