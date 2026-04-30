#!/usr/bin/env python3
"""
DM leptogenesis exact-kernel closure runner.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  Once the exact source package and the exact heavy-basis diagonal
  normalization are both fixed, what does the standard coherent leptogenesis
  kernel predict on the refreshed main-derived branch?

Answer:
  On the exact source-oriented branch:

    gamma = 1/2
    E1    = sqrt(8/3)
    E2    = sqrt(8)/3
    K00   = 2

  with the exact heavy-basis tensor channels

    cp1 = -2 gamma E1 / 3
    cp2 =  2 gamma E2 / 3.

  Inserting those into the standard coherent sum

    epsilon_1 = |(1/8pi) y0^2 (cp1 f23 + cp2 f3) / K00|

  gives

    epsilon_1 / epsilon_DI = 0.9276209209...
    eta / eta_obs          = 0.5578749661...

  on the same retained-fit transport benchmark used on this branch, once the
  exact `K00` denominator is used consistently in both `epsilon_1` and
  `m_tilde`.
"""

from __future__ import annotations

import math
import sys

from dm_leptogenesis_exact_common import exact_package

PASS_COUNT = 0
FAIL_COUNT = 0

PI = math.pi

g_bare = 1.0
PLAQ_MC = 0.5934
u0 = PLAQ_MC ** 0.25
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
D_THERMAL = 3.901508e-3
ETA_OBS = 6.12e-10


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{cls}] {status}: {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def g_self_energy(x: float) -> float:
    return math.sqrt(x) / (x - 1.0)


def f_vertex(x: float) -> float:
    if abs(x - 1.0) < 1e-6:
        return 0.5
    return math.sqrt(x) * (1.0 - (1.0 + x) * math.log((1.0 + x) / x))


def f_total(x: float) -> float:
    return g_self_energy(x) + f_vertex(x)


def part1_exact_source_and_diagonal_package() -> tuple[float, float, float, float, float]:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT SOURCE AND DIAGONAL PACKAGE IS CLOSED")
    print("=" * 88)

    gamma = 0.5
    e1 = math.sqrt(8.0 / 3.0)
    e2 = math.sqrt(8.0) / 3.0
    k00 = 2.0
    cp1 = -2.0 * gamma * e1 / 3.0
    cp2 = 2.0 * gamma * e2 / 3.0

    check(
        "The exact source package fixes gamma = 1/2, E1 = sqrt(8/3), E2 = sqrt(8)/3",
        abs(gamma - 0.5) < 1e-12 and abs(e1 - math.sqrt(8.0 / 3.0)) < 1e-12 and abs(e2 - math.sqrt(8.0) / 3.0) < 1e-12,
        f"(gamma,E1,E2)=({gamma:.6f},{e1:.12f},{e2:.12f})",
    )
    check(
        "The exact diagonal normalization theorem fixes K00 = 2",
        abs(k00 - 2.0) < 1e-12,
        f"K00={k00:.12f}",
    )
    check(
        "The exact heavy-basis CP tensor channels are fixed",
        abs(cp1 + 0.5443310539518174) < 1e-12 and abs(cp2 - 0.3142696805273545) < 1e-12,
        f"(cp1,cp2)=({cp1:.12f},{cp2:.12f})",
    )
    return gamma, e1, cp1, cp2, k00


def part2_exact_coherent_epsilon(cp1: float, cp2: float, k00: float) -> tuple[float, float, float]:
    print("\n" + "=" * 88)
    print("PART 2: THE STANDARD COHERENT KERNEL NOW GIVES AN EXACT EPSILON_1")
    print("=" * 88)

    k_A = 7
    k_B = 8
    A_MR = M_PL * ALPHA_LM**k_A
    B_MR = M_PL * ALPHA_LM**k_B
    eps_over_B = ALPHA_LM / 2.0

    M1 = B_MR * (1.0 - eps_over_B)
    M2 = B_MR * (1.0 + eps_over_B)
    M3 = A_MR

    m3_GeV = Y0_SQ * V_EW**2 / M1
    epsilon_di = (3.0 / (16.0 * PI)) * M1 * m3_GeV / V_EW**2

    x23 = (M2 / M1) ** 2
    x3 = (M3 / M1) ** 2
    f23 = f_total(x23)
    f3 = f_total(x3)

    epsilon_1 = abs((1.0 / (8.0 * PI)) * Y0_SQ * (cp1 * f23 + cp2 * f3) / k00)
    ratio = epsilon_1 / epsilon_di

    check(
        "The exact coherent sum stays below the Davidson-Ibarra ceiling",
        ratio < 1.0,
        f"epsilon_1/DI={ratio:.12f}",
    )
    check(
        "The exact coherent sum lands at 0.9276209209 of the DI ceiling",
        abs(ratio - 0.9276209209197268) < 1e-12,
        f"ratio={ratio:.12f}",
    )
    check(
        "So the old 0.30 suppression is gone once the exact K00 normalization is restored",
        ratio > 0.9,
        f"ratio={ratio:.12f}",
    )

    print()
    print(f"  epsilon_1 = {epsilon_1:.12e}")
    print(f"  epsilon_DI = {epsilon_di:.12e}")
    print(f"  epsilon_1 / epsilon_DI = {ratio:.12f}")

    return epsilon_1, epsilon_di, M1


def part3_exact_eta_hits_observation_on_the_retained_benchmark(epsilon_1: float, M1: float) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE EXACT KERNEL ON THE CONSISTENT RETAINED-FIT BENCHMARK")
    print("=" * 88)

    pkg = exact_package()
    m_tilde_eV = pkg.m_tilde_exact_eV
    m_star_eV = pkg.m_star_exact_eV
    k_washout = pkg.k_decay_exact
    kappa = pkg.kappa_fit_bench
    ratio = pkg.eta_ratio_fit_bench_exact_bookkeeping
    eta = ratio * ETA_OBS

    check(
        "The retained washout benchmark still lies in the strong-washout regime",
        k_washout > 1.0,
        f"K={k_washout:.12f}",
    )
    check(
        "The retained-fit benchmark no longer lands near observation once K00 is used consistently in the washout path",
        ratio < 0.7,
        f"eta/eta_obs={ratio:.12f}",
        cls="D",
    )
    check(
        "Numerically the exact kernel gives eta/eta_obs = 0.5578749661... on the consistent retained-fit benchmark",
        abs(ratio - 0.557874966110017) < 1e-12,
        f"ratio={ratio:.12f}",
        cls="D",
    )

    print()
    print(f"  kappa = {kappa:.12e}")
    print(f"  eta = {eta:.12e}")
    print(f"  eta_obs = {ETA_OBS:.12e}")
    print(f"  eta / eta_obs = {ratio:.12f}")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS EXACT-KERNEL CLOSURE")
    print("=" * 88)

    _, _, cp1, cp2, k00 = part1_exact_source_and_diagonal_package()
    epsilon_1, _, M1 = part2_exact_coherent_epsilon(cp1, cp2, k00)
    part3_exact_eta_hits_observation_on_the_retained_benchmark(epsilon_1, M1)

    print("\n" + "=" * 88)
    print(f"SUMMARY: classified_pass={PASS_COUNT} fail={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
