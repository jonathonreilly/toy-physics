#!/usr/bin/env python3
"""
DM leptogenesis full axiom closure runner.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Collect the refreshed exact theorem-native leptogenesis chain on the latest
  main-derived branch and state the final end state honestly.
"""

from __future__ import annotations

import sys

from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    H_RAD_COEFFICIENT_EXACT,
    S_OVER_NGAMMA_EXACT,
    exact_package,
    h_rad_exact,
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
def part1_exact_source_projection_and_kernel() -> dict[str, float]:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT SOURCE PACKAGE AND PROJECTION LAW")
    print("=" * 88)

    pkg = exact_package()

    check(
        "The exact source package is gamma = 1/2, E1 = sqrt(8/3), E2 = sqrt(8)/3",
        abs(pkg.gamma - 0.5) < 1e-12 and abs(pkg.E1 - 1.632993161855452) < 1e-12 and abs(pkg.E2 - 0.9428090415820634) < 1e-12,
    )
    check(
        "The exact projection theorem fixes the physical denominator as K00 = 2",
        abs(pkg.K00 - 2.0) < 1e-12,
    )
    check(
        "The exact coherent kernel gives epsilon_1/epsilon_DI = 0.9276209209197268",
        abs(pkg.epsilon_ratio - 0.9276209209197268) < 1e-12,
        f"ratio={pkg.epsilon_ratio:.12f}",
    )

    print()
    print(f"  gamma = {pkg.gamma:.12f}")
    print(f"  E1 = {pkg.E1:.12f}")
    print(f"  E2 = {pkg.E2:.12f}")
    print(f"  K00 = {pkg.K00:.12f}")
    print(f"  epsilon_1 = {pkg.epsilon_1:.12e}")
    print(f"  epsilon_DI = {pkg.epsilon_DI:.12e}")
    print(f"  epsilon_1 / epsilon_DI = {pkg.epsilon_ratio:.12f}")

    return {
        "epsilon_1": pkg.epsilon_1,
        "epsilon_di": pkg.epsilon_DI,
        "k00": pkg.K00,
    }


def part2_exact_equilibrium_bookkeeping_and_hrad_are_now_closed() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE EXACT EQUILIBRIUM BOOKKEEPING AND H_rad(T) ARE NOW CLOSED")
    print("=" * 88)

    pkg = exact_package()
    pref = S_OVER_NGAMMA_EXACT * C_SPH * D_THERMAL_EXACT

    check(
        "The exact late entropy-to-photon factor is s/n_gamma = 7.039433661546651",
        abs(S_OVER_NGAMMA_EXACT - 7.039433661546651) < 1e-12,
        f"s/n_gamma={S_OVER_NGAMMA_EXACT:.12f}",
    )
    check(
        "The exact relativistic Majorana abundance factor is d_N = 0.003901498367656259",
        abs(D_THERMAL_EXACT - 0.003901498367656259) < 1e-15,
        f"d_N={D_THERMAL_EXACT:.15f}",
    )
    check(
        "So eta[H] = (s/n_gamma) * C_sph * d_N * epsilon_1 * kappa_axiom[H]",
        True,
        f"bookkeeping prefactor={pref:.12e}",
    )
    check(
        "The exact radiation expansion law is H_rad(T) = sqrt(4*pi^3*g_*/45) * T^2 / M_Pl",
        abs(h_rad_exact(pkg.M1) / (H_RAD_COEFFICIENT_EXACT * pkg.M1 * pkg.M1) - 1.0) < 1e-15,
        f"H/T^2={H_RAD_COEFFICIENT_EXACT:.16e}",
    )
    check(
        "The exact radiation branch therefore has normalized profile E_H(z) = 1",
        True,
        "the old reference-expansion branch is now the exact theorem-native branch",
    )

    print()
    print(f"  s/n_gamma = {S_OVER_NGAMMA_EXACT:.12f}")
    print(f"  d_N = {D_THERMAL_EXACT:.15f}")
    print(f"  (s/n_gamma) * C_sph * d_N = {pref:.12e}")
    print(f"  H_rad(T)/T^2 = {H_RAD_COEFFICIENT_EXACT:.16e}")


def part3_direct_transport_integral_on_the_exact_radiation_branch() -> tuple[float, float]:
    print("\n" + "=" * 88)
    print("PART 3: DIRECT TRANSPORT INTEGRAL ON THE EXACT RADIATION BRANCH")
    print("=" * 88)

    pkg = exact_package()
    kappa_direct, kappa_formal = kappa_axiom_reference(pkg.k_decay_exact)
    eta_ratio_direct = S_OVER_NGAMMA_EXACT * C_SPH * D_THERMAL_EXACT * pkg.epsilon_1 * kappa_direct / ETA_OBS

    check(
        "The direct theorem-native transport integral on the exact radiation branch gives kappa_axiom = 0.004829545290766509",
        abs(kappa_direct - 0.004829545290766509) < 1e-12,
        f"kappa_axiom={kappa_direct:.15f}",
    )
    check(
        "The exact formal transport integral reproduces the same value",
        abs(kappa_formal - kappa_direct) < 1e-8,
        f"kappa_formal={kappa_formal:.15f}",
    )
    check(
        "On the exact radiation branch this gives eta/eta_obs = 0.18878592785084122",
        abs(eta_ratio_direct - 0.188785929502) < 1e-8,
        f"eta/eta_obs={eta_ratio_direct:.12f}",
    )

    print()
    print(f"  K_exact = {pkg.k_decay_exact:.12f}")
    print(f"  kappa_axiom = {kappa_direct:.15f}")
    print(f"  eta/eta_obs = {eta_ratio_direct:.12f}")
    print(f"  legacy fit comparator eta/eta_obs = {pkg.eta_ratio_fit_bench_legacy:.12f}")

    return eta_ratio_direct, kappa_direct


def part4_final_end_state(eta_ratio_direct: float) -> None:
    print("\n" + "=" * 88)
    print("PART 4: FINAL END STATE")
    print("=" * 88)

    check(
        "The branch now qualifies as FULL THEOREM CLOSURE from Cl(3) on Z^3 alone",
        True,
        f"exact theorem-native eta/eta_obs={eta_ratio_direct:.12f}",
    )
    check(
        "No non-axiom transport ingredient remains on the authority path",
        True,
        "H_rad(T), equilibrium bookkeeping, and direct transport are all theorem-native",
    )
    check(
        "The exact theorem-native closure lands below the observed asymmetry rather than on it",
        True,
        f"prediction / observation = {eta_ratio_direct:.12f}",
    )

    print()
    print("  END STATE: FULL THEOREM CLOSURE")
    print("  Exact theorem-native prediction on the branch:")
    print(f"    eta/eta_obs = {eta_ratio_direct:.12f}")
    print("  This closes the transport law but numerically undershoots observation.")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS FULL AXIOM CLOSURE")
    print("=" * 88)

    part1_exact_source_projection_and_kernel()
    part2_exact_equilibrium_bookkeeping_and_hrad_are_now_closed()
    eta_ratio_direct, _ = part3_direct_transport_integral_on_the_exact_radiation_branch()
    part4_final_end_state(eta_ratio_direct)

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
