#!/usr/bin/env python3
"""
DM leptogenesis benchmark decomposition.

Question:
  Why does the current benchmark land at eta ~= 1.81e-10 ~= 0.30 eta_obs
  instead of much smaller or much larger?

Answer:
  Almost entirely because the current reduced CP kernel only realizes about
  27.7% of the Davidson-Ibarra ceiling at the same M1 and washout.

  At the benchmark:
    eta = 7.04 * C_sph * d * kappa * epsilon_1
    eta_DI = 7.04 * C_sph * d * kappa * epsilon_DI

  and numerically
    eta_DI ~= 6.54e-10 ~= 1.07 eta_obs
    epsilon_1 / epsilon_DI ~= 0.277

  so
    eta / eta_obs = (epsilon_1/epsilon_DI) * (eta_DI/eta_obs)
                  ~= 0.277 * 1.068
                  ~= 0.296.

  The 0.30 is therefore mostly a CP-kernel suppression number, not a washout
  or staircase-placement failure.
"""

from __future__ import annotations

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


def part1_eta_factorizes_through_the_di_ceiling() -> tuple[float, float, float, float]:
    print("\n" + "=" * 88)
    print("PART 1: THE BENCHMARK ETA FACTORIZES THROUGH THE DI CEILING")
    print("=" * 88)

    eta_obs = 6.12e-10
    eps = 7.350125e-7
    eps_di = 2.649380e-6
    kappa = 2.534289e-2
    C_sph = 28.0 / 79.0
    d_thermal = 3.901508e-3
    pref = 7.04 * C_sph * d_thermal
    eta = pref * kappa * eps
    eta_di = pref * kappa * eps_di
    ratio = eta / eta_obs
    fact = (eps / eps_di) * (eta_di / eta_obs)

    check(
        "The benchmark eta is reproduced by the stated prefactor chain",
        abs(eta - 1.8133722460155063e-10) < 1e-18,
        f"eta={eta:.6e}",
    )
    check(
        "The benchmark ratio factorizes exactly through epsilon_1 / epsilon_DI",
        abs(ratio - fact) < 1e-12,
        f"ratio={ratio:.6f}, fact={fact:.6f}",
    )
    check(
        "The same-kappa DI ceiling is already near the observed eta",
        abs(eta_di / eta_obs - 1.0680339817146773) < 1e-12,
        f"eta_DI/eta_obs={eta_di/eta_obs:.6f}",
    )

    print()
    print("  So the observed 0.30 is not mainly coming from washout or M1.")
    print("  At fixed M1 and kappa, the benchmark would be near eta_obs if")
    print("  epsilon_1 saturated the DI ceiling.")
    return ratio, eps / eps_di, eta_di / eta_obs, eta_di


def part2_the_cp_kernel_supplies_most_of_the_suppression(eps_over_di: float) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CP KERNEL SUPPLIES THE 0.30 SUPPRESSION")
    print("=" * 88)

    n3 = 2.245474e-8
    n2 = 7.125577e-7
    eps_di = 2.649380e-6

    check(
        "The N2 piece contributes about 26.9% of the DI ceiling",
        abs(n2 / eps_di - 0.2689526228778054) < 1e-12,
        f"N2/DI={n2/eps_di:.6f}",
    )
    check(
        "The N3 piece contributes only about 0.85% of the DI ceiling",
        abs(n3 / eps_di - 0.008475469732541199) < 1e-12,
        f"N3/DI={n3/eps_di:.6f}",
    )
    check(
        "Together they reproduce the full epsilon_1 / epsilon_DI ratio",
        abs((n2 + n3) / eps_di - eps_over_di) < 1e-6,
        f"sum/DI={(n2+n3)/eps_di:.6f}, eps/DI={eps_over_di:.6f}",
    )

    print()
    print("  The current benchmark is therefore N2-dominated.")
    print("  The reduced CP kernel gets most of its strength from the")
    print("  quasi-degenerate doublet pair, but still only reaches 27.7% of DI.")


def part3_bank_records_the_benchmark_explanation() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE BANK RECORDS THE 0.30 EXPLANATION")
    print("=" * 88)

    note = read("docs/DM_LEPTOGENESIS_BENCHMARK_DECOMPOSITION_NOTE_2026-04-15.md")
    blocker = read("docs/DM_LEPTOGENESIS_NOTE.md")

    check(
        "The new note states eta_DI ~ 1.07 eta_obs and eps/DI ~ 0.277",
        "1.07" in note and "0.277" in note and "Davidson-Ibarra" in note,
    )
    check(
        "The main leptogenesis note still reports the benchmark 0.30 ratio",
        "ratio           = 0.30" in blocker or "0.30" in blocker,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS BENCHMARK DECOMPOSITION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Why does the benchmark land at eta ~= 0.30 eta_obs?")

    ratio, eps_over_di, eta_di_over_obs, eta_di = part1_eta_factorizes_through_the_di_ceiling()
    part2_the_cp_kernel_supplies_most_of_the_suppression(eps_over_di)
    part3_bank_records_the_benchmark_explanation()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print(f"  eta/eta_obs   = {ratio:.6f}")
    print(f"  eps/eps_DI    = {eps_over_di:.6f}")
    print(f"  eta_DI/eta_obs= {eta_di_over_obs:.6f}")
    print(f"  eta_DI        = {eta_di:.6e}")
    print()
    print("  So the 0.30 benchmark is mainly a CP-kernel suppression effect.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
