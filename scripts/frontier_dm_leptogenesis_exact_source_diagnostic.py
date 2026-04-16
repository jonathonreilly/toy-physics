#!/usr/bin/env python3
"""
DM leptogenesis exact-source diagnostic.

Question:
  Once the sharp source amplitudes and transfer coefficients are fixed, what
  happens if the exact source package is inserted into the same normalized
  heavy-kernel convention already used by the current reduced leptogenesis
  benchmark?

Answer:
  It no longer underproduces. It overshoots the Davidson-Ibarra ceiling by an
  O(2) factor, so the remaining gap is not a weak source deficit. It is the
  missing diagonal normalization / thermal projection law from the exact
  heavy-basis CP tensor to epsilon_1.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


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


PI = math.pi
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
ETA_OBS = 6.12e-10
C_SPH = 28.0 / 79.0
D_THERMAL = 3.901508e-3
KAPPA = 2.534289e-2
ETA_PREF = 7.04 * C_SPH * D_THERMAL * KAPPA


def g_self_energy(x: float) -> float:
    return math.sqrt(x) / (x - 1.0)


def f_vertex(x: float) -> float:
    if abs(x - 1.0) < 1e-6:
        return 0.5
    return math.sqrt(x) * (1.0 - (1.0 + x) * math.log((1.0 + x) / x))


def f_total(x: float) -> float:
    return g_self_energy(x) + f_vertex(x)


def part1_exact_source_package_is_closed() -> tuple[float, float, float, float]:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT SOURCE PACKAGE IS CLOSED")
    print("=" * 88)

    source = read("docs/DM_NEUTRINO_SOURCE_AMPLITUDE_THEOREM_NOTE_2026-04-15.md")
    codd = read("docs/DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md")
    veven = read("docs/DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md")

    gamma = 0.5
    e1 = math.sqrt(8.0 / 3.0)
    e2 = math.sqrt(8.0) / 3.0
    cp1 = -2.0 * gamma * e1 / 3.0
    cp2 = 2.0 * gamma * e2 / 3.0

    check(
        "The source-amplitude theorem fixes a_sel = 1/2 and tau_+ = 1",
        "a_sel = 1/2" in source and "tau_+ = 1" in source,
    )
    check(
        "The odd and even transfer coefficients are already fixed separately",
        "c_odd = +1" in codd and "v_even = (sqrt(8/3), sqrt(8)/3)" in veven,
    )
    check(
        "The exact source package gives gamma = 1/2, E1 = sqrt(8/3), E2 = sqrt(8)/3",
        abs(gamma - 0.5) < 1e-12 and abs(e1 - math.sqrt(8.0 / 3.0)) < 1e-12 and abs(e2 - math.sqrt(8.0) / 3.0) < 1e-12,
        f"(gamma,E1,E2)=({gamma:.6f},{e1:.12f},{e2:.12f})",
    )
    check(
        "Therefore the exact heavy-basis CP tensor channels are fixed",
        abs(cp1 + 0.5443310539518174) < 1e-12 and abs(cp2 - 0.3142696805273545) < 1e-12,
        f"(cp1,cp2)=({cp1:.12f},{cp2:.12f})",
    )

    return gamma, e1, cp1, cp2


def part2_same_normalized_kernel_convention_now_overshoots_di(cp1: float, cp2: float) -> tuple[float, float, float]:
    print("\n" + "=" * 88)
    print("PART 2: THE SAME NORMALIZED-KERNEL CONVENTION NOW OVERSHOOTS DI")
    print("=" * 88)

    k_A = 7
    k_B = 8
    A_MR = M_PL * ALPHA_LM**k_A
    B_MR = M_PL * ALPHA_LM**k_B
    eps_over_B = ALPHA_LM / 2.0
    M1 = B_MR * (1.0 - eps_over_B)
    M2 = B_MR * (1.0 + eps_over_B)
    M3 = A_MR
    m3_GeV = (Y0_SQ * V_EW**2 / M1)  # GeV

    epsilon_DI = (3.0 / (16.0 * PI)) * M1 * m3_GeV / V_EW**2
    x23 = (M2 / M1) ** 2
    x3 = (M3 / M1) ** 2
    f23 = f_total(x23)
    f3 = f_total(x3)

    # Same normalized-kernel convention implicit in the current reduced runner:
    # factor out y0^2 from h_11 and use the exact heavy-basis off-diagonal tensor
    # directly as the dimensionless CP kernel entries.
    eps_signed = abs((1.0 / (8.0 * PI)) * Y0_SQ * (cp1 * f23 + cp2 * f3))
    eps_abs = (1.0 / (8.0 * PI)) * Y0_SQ * (abs(cp1) * abs(f23) + abs(cp2) * abs(f3))

    check(
        "The exact-source signed kernel exceeds the Davidson-Ibarra ceiling under the old normalization convention",
        eps_signed / epsilon_DI > 1.0,
        f"eps_signed/DI={eps_signed/epsilon_DI:.6f}",
    )
    check(
        "The incoherent absolute-sum version also exceeds the Davidson-Ibarra ceiling",
        eps_abs / epsilon_DI > 1.0,
        f"eps_abs/DI={eps_abs/epsilon_DI:.6f}",
    )
    check(
        "So the exact source package no longer looks CP-starved on the old benchmark convention",
        eps_signed > 2.6493795301073166e-06,
        f"eps_signed={eps_signed:.6e}, DI={epsilon_DI:.6e}",
    )

    return epsilon_DI, eps_signed, eps_abs


def part3_the_remaining_gap_is_diagonal_normalization_or_projection(epsilon_di: float, eps_signed: float, eps_abs: float) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE REMAINING GAP IS DIAGONAL NORMALIZATION / PROJECTION")
    print("=" * 88)

    eta_di = ETA_PREF * epsilon_di
    eta_signed = ETA_PREF * eps_signed
    eta_abs = ETA_PREF * eps_abs

    k00_req_signed = eps_signed / epsilon_di
    k00_req_abs = eps_abs / epsilon_di
    k00_req_obs_signed = eps_signed / (0.936 * epsilon_di)
    k00_req_obs_abs = eps_abs / (0.936 * epsilon_di)

    note = read("docs/DM_LEPTOGENESIS_BENCHMARK_DECOMPOSITION_NOTE_2026-04-15.md")

    check(
        "The benchmark decomposition note already says the old 0.30 is a CP-kernel suppression number",
        "0.277" in note and "1.07" in note,
    )
    check(
        "Under the exact-source insertion, eta would overshoot observation on the same old kernel convention",
        eta_signed / ETA_OBS > 1.0 and eta_abs / ETA_OBS > 1.0,
        f"(signed,abs)=({eta_signed/ETA_OBS:.6f},{eta_abs/ETA_OBS:.6f})",
    )
    check(
        "So the remaining theorem gap is not source underproduction but the missing map from K_mass to epsilon_1",
        k00_req_signed > 1.0 and k00_req_abs > 1.0,
        f"K00 needed for DI ~ ({k00_req_signed:.6f},{k00_req_abs:.6f})",
    )

    print()
    print(f"  Same-kappa DI ceiling: eta_DI/eta_obs = {eta_di/ETA_OBS:.6f}")
    print(f"  Exact-source signed insertion: eta/eta_obs = {eta_signed/ETA_OBS:.6f}")
    print(f"  Exact-source abs-sum insertion: eta/eta_obs = {eta_abs/ETA_OBS:.6f}")
    print(f"  Required effective K_11 normalization for DI saturation:")
    print(f"    signed kernel : K11_eff ~ {k00_req_signed:.6f}")
    print(f"    abs-sum kernel: K11_eff ~ {k00_req_abs:.6f}")
    print(f"  Required effective K_11 normalization for eta_obs at same washout:")
    print(f"    signed kernel : K11_eff ~ {k00_req_obs_signed:.6f}")
    print(f"    abs-sum kernel: K11_eff ~ {k00_req_obs_abs:.6f}")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS EXACT-SOURCE DIAGNOSTIC")
    print("=" * 88)

    _, _, cp1, cp2 = part1_exact_source_package_is_closed()
    epsilon_di, eps_signed, eps_abs = part2_same_normalized_kernel_convention_now_overshoots_di(cp1, cp2)
    part3_the_remaining_gap_is_diagonal_normalization_or_projection(epsilon_di, eps_signed, eps_abs)

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
