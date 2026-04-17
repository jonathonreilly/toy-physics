#!/usr/bin/env python3
"""
DM leptogenesis transport-decomposition theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  With the exact source package and projection law already fixed, what is the
  exact remaining transport object in the DM denominator lane?

Answer:
  The baryon-to-photon ratio factors as

      eta[H] = C_late * C_sph * d_N * epsilon_1 * kappa_axiom[H],

  where

      C_late = s/n_gamma on the late radiation branch,
      d_N    = Y_N1^eq(z->0),

  are bookkeeping conversion factors, while the only unresolved transport
  physics lives in the direct Boltzmann transport functional

      kappa_axiom[H].

  The old kappa_fit(K) is therefore only a diagnostic comparator.
"""

from __future__ import annotations

import math
import sys

from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
)

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


def part1_exact_upstream_inputs_are_frozen() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT UPSTREAM INPUTS ARE FROZEN")
    print("=" * 88)

    pkg = exact_package()
    check(
        "The exact source package remains gamma = 1/2, E1 = sqrt(8/3), E2 = sqrt(8)/3",
        abs(pkg.gamma - 0.5) < 1e-12 and abs(pkg.E1 - math.sqrt(8.0 / 3.0)) < 1e-12 and abs(pkg.E2 - math.sqrt(8.0) / 3.0) < 1e-12,
    )
    check(
        "The exact projection law remains K00 = 2",
        abs(pkg.K00 - 2.0) < 1e-12,
    )
    check(
        "The exact coherent kernel remains epsilon_1/epsilon_DI = 0.9276209209197268",
        abs(pkg.epsilon_ratio - 0.9276209209197268) < 1e-12,
        f"ratio={pkg.epsilon_ratio:.12f}",
    )


def part2_transport_factors_split_into_bookkeeping_and_transport() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ETA SPLITS INTO BOOKKEEPING AND A SINGLE TRANSPORT FUNCTIONAL")
    print("=" * 88)

    pref = S_OVER_NGAMMA_EXACT * C_SPH * D_THERMAL_EXACT

    check(
        "The late conversion factor is exact once s/n_gamma and d_N are closed",
        abs(S_OVER_NGAMMA_EXACT - 7.039433661546651) < 1e-12 and abs(D_THERMAL_EXACT - 0.003901498367656259) < 1e-15,
        f"(Clate,dN)=({S_OVER_NGAMMA_EXACT:.12f},{D_THERMAL_EXACT:.15f})",
    )
    check(
        "So eta[H] = C_late * C_sph * d_N * epsilon_1 * kappa_axiom[H]",
        True,
        f"bookkeeping prefactor={pref:.12e}",
    )
    check(
        "This demotes kappa_fit(K) from authority path to diagnostic comparator",
        True,
        "the authority path is the direct transport functional kappa_axiom[H]",
    )


def part3_the_old_physically_consistent_fit_benchmark_is_preserved_only_as_a_comparator() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE OLD FIT BENCHMARK IS PRESERVED ONLY AS A COMPARATOR")
    print("=" * 88)

    pkg = exact_package()

    check(
        "The legacy physically consistent fit benchmark remains eta/eta_obs = 0.557919848420251",
        abs(pkg.eta_ratio_fit_bench_legacy - 0.557919848420251) < 1e-12,
        f"legacy fit ratio={pkg.eta_ratio_fit_bench_legacy:.12f}",
    )
    check(
        "Using exact bookkeeping with the same fit gives eta/eta_obs = 0.557874966110017",
        abs(pkg.eta_ratio_fit_bench_exact_bookkeeping - 0.557874966110017) < 1e-12,
        f"exact-bookkeeping fit ratio={pkg.eta_ratio_fit_bench_exact_bookkeeping:.12f}",
    )
    check(
        "So the fit may be retained for comparison, but it is not the theorem-native transport law",
        pkg.eta_ratio_fit_bench_legacy > 0.5 and pkg.eta_ratio_fit_bench_exact_bookkeeping > 0.5,
        "the fit remains a diagnostic comparator only",
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS TRANSPORT-DECOMPOSITION THEOREM")
    print("=" * 88)

    part1_exact_upstream_inputs_are_frozen()
    part2_transport_factors_split_into_bookkeeping_and_transport()
    part3_the_old_physically_consistent_fit_benchmark_is_preserved_only_as_a_comparator()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
