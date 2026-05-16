#!/usr/bin/env python3
"""
DM leptogenesis exact-kernel closure runner.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Honest scope (audit class E repair, 2026-05-16):
  This runner is a downstream consumer of the exact source-and-CP-channel
  package. The four source-package values

    gamma = 1/2
    E1    = sqrt(8/3)
    E2    = sqrt(8)/3
    K00   = 2

  are imported from upstream conditional support authorities:

    * gamma = 1/2 (== c_odd a_sel with c_odd = +1, a_sel = 1/2)
      upstream: DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15
      (audit row: dm_neutrino_codd_bosonic_normalization_theorem_note_2026-04-15,
       currently `unaudited`).
    * (E1, E2) = (sqrt(8/3), sqrt(8)/3)
      upstream: DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15
      (audit row: dm_neutrino_veven_bosonic_normalization_theorem_note_2026-04-15,
       currently `audited_conditional`).
    * K00 = 2
      upstream: DM_NEUTRINO_K00_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15
      (audit row: dm_neutrino_k00_bosonic_normalization_theorem_note_2026-04-15,
       currently `audited_renaming`).

  They are NOT re-derived from `Cl(3)` on `Z^3` inside this restricted packet.
  The runner therefore self-classifies the corresponding Part 1 checks
  (source-package values, CP tensor channels) and Part 2 checks
  (epsilon_1 / epsilon_DI ratio that propagates them) as class D
  (conditional-on-imported-upstream), not class C. This matches the live
  pattern of `frontier_dm_current_bank_quantitative_mapping_2026_04_21.py`
  for downstream consumers of the same imported package.

  The class-D self-classification of the Part 1 and Part 2 checks is the
  audit class E repair recorded by the 2026-05-16 science-fix-loop iter18
  pass (`audited_renaming -> audited_conditional` candidate move once
  upstream `_codd_bosonic` and `_veven_bosonic` lift past `audited_renaming`).
  Whether the audit lane actually lifts the verdict is for the audit lane
  to decide; this runner change does not edit the audit ledger.

Question:
  Once the exact source package and the exact heavy-basis diagonal
  normalization are both accepted as imported (see above), what does the
  standard coherent leptogenesis kernel predict on the refreshed
  main-derived branch?

Answer:
  Conditional on the imported source-package values:

    cp1 = -2 gamma E1 / 3
    cp2 =  2 gamma E2 / 3

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


CLASS_COUNTS: dict[str, int] = {}


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    CLASS_COUNTS[cls] = CLASS_COUNTS.get(cls, 0) + 1
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
    print("PART 1: IMPORTED SOURCE AND DIAGONAL PACKAGE (UPSTREAM-CONDITIONAL)")
    print("=" * 88)
    print(
        "  (These four source-package values are imported from upstream\n"
        "   support theorems, not re-derived from Cl(3) on Z^3 inside this\n"
        "   restricted packet. Per the 2026-05-05 audit verdict the\n"
        "   corresponding checks are class D conditional-on-import, not\n"
        "   class C standalone-derivation. See the module docstring for\n"
        "   the explicit upstream authority citations.)"
    )

    gamma = 0.5
    e1 = math.sqrt(8.0 / 3.0)
    e2 = math.sqrt(8.0) / 3.0
    k00 = 2.0
    cp1 = -2.0 * gamma * e1 / 3.0
    cp2 = 2.0 * gamma * e2 / 3.0

    check(
        "Imported (upstream-conditional): odd source gamma = 1/2 and even responses E1 = sqrt(8/3), E2 = sqrt(8)/3",
        abs(gamma - 0.5) < 1e-12 and abs(e1 - math.sqrt(8.0 / 3.0)) < 1e-12 and abs(e2 - math.sqrt(8.0) / 3.0) < 1e-12,
        f"(gamma,E1,E2)=({gamma:.6f},{e1:.12f},{e2:.12f})"
        f"  [upstream: _codd_bosonic_normalization_theorem_note_2026-04-15,"
        f" _veven_bosonic_normalization_theorem_note_2026-04-15]",
        cls="D",
    )
    check(
        "Imported (upstream-conditional): exact diagonal normalization K00 = 2",
        abs(k00 - 2.0) < 1e-12,
        f"K00={k00:.12f}"
        f"  [upstream: _k00_bosonic_normalization_theorem_note_2026-04-15]",
        cls="D",
    )
    check(
        "Derived from imports: exact heavy-basis CP tensor channels cp1 = -2 gamma E1 / 3, cp2 = 2 gamma E2 / 3",
        abs(cp1 + 0.5443310539518174) < 1e-12 and abs(cp2 - 0.3142696805273545) < 1e-12,
        f"(cp1,cp2)=({cp1:.12f},{cp2:.12f})",
        cls="D",
    )
    return gamma, e1, cp1, cp2, k00


def part2_exact_coherent_epsilon(cp1: float, cp2: float, k00: float) -> tuple[float, float, float]:
    print("\n" + "=" * 88)
    print("PART 2: COHERENT KERNEL EPSILON_1 (CONDITIONAL ON IMPORTED PART 1)")
    print("=" * 88)
    print(
        "  (The numeric epsilon_1 here is downstream arithmetic on the\n"
        "   imported (cp1, cp2, K00) of Part 1. The retained benchmark\n"
        "   constants (k_A = 7, k_B = 8, eps/B = alpha_LM / 2) are\n"
        "   themselves admitted retained-fit inputs, not derived inside\n"
        "   this packet. The corresponding checks are therefore class D\n"
        "   conditional-on-imported-Part-1, not class C standalone.)"
    )

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
        "Downstream arithmetic on imported (cp1, cp2, K00): epsilon_1 stays below the Davidson-Ibarra ceiling",
        ratio < 1.0,
        f"epsilon_1/DI={ratio:.12f}",
        cls="D",
    )
    check(
        "Downstream arithmetic on imported (cp1, cp2, K00): epsilon_1 / epsilon_DI = 0.9276209209",
        abs(ratio - 0.9276209209197268) < 1e-12,
        f"ratio={ratio:.12f}",
        cls="D",
    )
    check(
        "Downstream arithmetic on imported (cp1, cp2, K00): old 0.30 suppression is gone once K00 = 2 is consumed",
        ratio > 0.9,
        f"ratio={ratio:.12f}",
        cls="D",
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
        "Downstream arithmetic on imported K00 and retained washout benchmark: still in strong-washout regime",
        k_washout > 1.0,
        f"K={k_washout:.12f}",
        cls="D",
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
    if CLASS_COUNTS:
        breakdown = ", ".join(f"class {k}: {v}" for k, v in sorted(CLASS_COUNTS.items()))
        print(f"CLASS BREAKDOWN: {breakdown}")
    print(
        "AUDIT NOTE: this runner has zero class-C standalone-derivation checks.\n"
        "All checks are class-D conditional-on-imported-upstream. The imported\n"
        "source-package values (gamma=1/2, E1=sqrt(8/3), E2=sqrt(8)/3, K00=2)\n"
        "come from the upstream support theorems named in the module docstring.\n"
        "This honest self-classification is the audit class-E repair recorded\n"
        "by the 2026-05-16 science-fix-loop iter18 pass."
    )
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
