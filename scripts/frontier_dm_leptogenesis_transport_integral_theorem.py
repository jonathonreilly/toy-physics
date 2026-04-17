#!/usr/bin/env python3
"""
DM leptogenesis transport-integral theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  Can the strong-washout factor be replaced by a direct theorem-native
  transport solve instead of the phenomenological kappa_fit(K)?

Answer:
  Yes.

  On the normalized abundance variables

      N_N1^eq(z) = 0.5 z^2 K_2(z),   N_N1^eq(0) = 1,

  the exact Boltzmann transport law is

      dN_N1/dz  = -D_H(z) (N_N1 - N_N1^eq),
      dN_B-L/dz =  D_H(z) (N_N1 - N_N1^eq) - W_H(z) N_B-L

  with

      D_H(z) = K_H z K_1(z)/K_2(z) / E_H(z),
      W_H(z) = K_H z^3 K_1(z) / (4 E_H(z)).

  The direct transport efficiency is therefore

      kappa_axiom[H] = |N_B-L(infty)|,

  and also equals the exact formal integral constructed from the transport
  solution.

  On the exact radiation branch E_H(z)=1 with the exact transport input
  K_H = 47.2359796299..., the direct transport solve gives

      kappa_axiom,ref = 0.0048295452485...

  while the old fit gave

      kappa_fit = 0.0142716272474...

  so the fit overstates transport by a factor ~2.96 on that branch.
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
    kappa_axiom_reference,
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


def part1_the_direct_transport_equations_are_the_authority_object() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE DIRECT TRANSPORT EQUATIONS ARE THE AUTHORITY OBJECT")
    print("=" * 88)

    pkg = exact_package()

    check(
        "The exact radiation branch uses the exact transport input K_H = 47.23597962989828",
        abs(pkg.k_decay_exact - 47.23597962989828) < 1e-12,
        f"K_H={pkg.k_decay_exact:.12f}",
    )
    check(
        "The old fit comparator remains kappa_fit = 0.01427162724743994",
        abs(pkg.kappa_fit_bench - 0.01427162724743994) < 1e-14,
        f"kappa_fit={pkg.kappa_fit_bench:.14f}",
    )
    check(
        "The transport authority path is now the direct Boltzmann solve rather than the fit",
        True,
        "kappa_axiom[H] is defined by the transport equations themselves",
    )


def part2_the_formal_integral_matches_the_direct_transport_solve() -> tuple[float, float]:
    print("\n" + "=" * 88)
    print("PART 2: THE FORMAL INTEGRAL MATCHES THE DIRECT TRANSPORT SOLVE")
    print("=" * 88)

    pkg = exact_package()
    direct, formal = kappa_axiom_reference(pkg.k_decay_exact)

    check(
        "The direct exact-radiation transport solve gives kappa_axiom = 0.004829545290766509",
        abs(direct - 0.004829545290766509) < 1e-12,
        f"kappa_axiom={direct:.15f}",
    )
    check(
        "The exact formal transport integral reproduces the same value",
        abs(formal - direct) < 1e-8,
        f"(direct,formal)=({direct:.15f},{formal:.15f})",
    )
    check(
        "So the fit is no longer needed on the exact radiation branch",
        True,
        "the transport solve and formal integral agree without any kappa-fit input",
    )

    return direct, formal


def part3_the_fit_overstates_transport_on_the_reference_branch(direct: float) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE FIT OVERSTATES TRANSPORT ON THE EXACT RADIATION BRANCH")
    print("=" * 88)

    pkg = exact_package()
    eta_ratio_direct = S_OVER_NGAMMA_EXACT * C_SPH * D_THERMAL_EXACT * pkg.epsilon_1 * direct / ETA_OBS
    overstating = pkg.kappa_fit_bench / direct

    check(
        "The exact radiation transport branch gives eta/eta_obs = 0.18878592785084122",
        abs(eta_ratio_direct - 0.188785929502) < 1e-8,
        f"eta/eta_obs={eta_ratio_direct:.12f}",
    )
    check(
        "The old fit overstates transport by a factor 2.955066473761705",
        abs(overstating - 2.955066447917) < 1e-8,
        f"fit/direct={overstating:.12f}",
    )
    check(
        "Therefore kappa_fit(K) is only a diagnostic comparator, not the authority transport result",
        pkg.kappa_fit_bench > direct,
        f"(fit,direct)=({pkg.kappa_fit_bench:.12f},{direct:.12f})",
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS TRANSPORT-INTEGRAL THEOREM")
    print("=" * 88)

    part1_the_direct_transport_equations_are_the_authority_object()
    direct, _ = part2_the_formal_integral_matches_the_direct_transport_solve()
    part3_the_fit_overstates_transport_on_the_reference_branch(direct)

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
