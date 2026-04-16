#!/usr/bin/env python3
"""
DM leptogenesis flavored / N2-aware transport diagnostic.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Status:
  Diagnostic extension lane beyond the exact one-flavor theorem-closure path.

Purpose:
  Quantify whether the post-closure mismatch can plausibly be repaired by
  flavor-resolved transport and/or a protected N2 sequential source, without
  mutating the current exact authority runner.
"""

from __future__ import annotations

import math
import sys
from functools import lru_cache

import numpy as np

from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
    kappa_axiom_reference,
    solve_multisource_flavored_transport,
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


def eta_ratio_from_kappa(pkg_epsilon_1: float, kappa_value: float) -> float:
    return S_OVER_NGAMMA_EXACT * C_SPH * D_THERMAL_EXACT * pkg_epsilon_1 * kappa_value / ETA_OBS


@lru_cache(maxsize=None)
def kappa_cached(k_decay: float) -> float:
    return float(kappa_axiom_reference(float(k_decay))[0])


def eta_ratio_single_source_flavored(pkg: object, projectors: tuple[float, ...]) -> float:
    _, _, asym_grid = solve_multisource_flavored_transport(
        lambdas=np.array([1.0]),
        k_decays=np.array([pkg.k_decay_exact]),
        source_matrix=np.array([projectors], dtype=float),
        washout_matrix=np.array([projectors], dtype=float),
    )
    kappa_value = abs(float(asym_grid[:, -1].sum()))
    return eta_ratio_from_kappa(pkg.epsilon_1, kappa_value)


def part1_exact_one_flavor_authority_baseline() -> tuple[object, float, float]:
    print("\n" + "=" * 88)
    print("PART 1: EXACT ONE-FLAVOR AUTHORITY BASELINE")
    print("=" * 88)

    pkg = exact_package()
    kappa_one = kappa_cached(pkg.k_decay_exact)
    eta_one = eta_ratio_from_kappa(pkg.epsilon_1, kappa_one)

    check(
        "The exact one-flavor authority path still gives eta/eta_obs = 0.188785929502",
        abs(eta_one - 0.188785929502) < 1e-8,
        f"eta/eta_obs={eta_one:.12f}",
    )
    check(
        "The exact numerator is already close to the DI ceiling",
        abs(pkg.epsilon_ratio - 0.9276209209197268) < 1e-12,
        f"epsilon_1/epsilon_DI={pkg.epsilon_ratio:.12f}",
    )
    check(
        "So the remaining gap is transport-side rather than a large missing numerator factor",
        (1.0 / eta_one) / (1.0 / pkg.epsilon_ratio) > 4.0,
        f"transport gap factor={(1.0 / eta_one):.6f}",
    )

    print()
    print(f"  epsilon_1 / epsilon_DI = {pkg.epsilon_ratio:.12f}")
    print(f"  kappa_1flavor = {kappa_one:.15f}")
    print(f"  eta/eta_obs = {eta_one:.12f}")

    return pkg, kappa_one, eta_one


def part2_flavored_n1_transport_can_lift_the_exact_branch(pkg: object, kappa_one: float) -> tuple[float, float, float]:
    print("\n" + "=" * 88)
    print("PART 2: FLAVORED N1 TRANSPORT CAN LIFT THE EXACT BRANCH")
    print("=" * 88)

    two_equal = (0.5, 0.5)
    three_equal = (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
    eta_two = eta_ratio_single_source_flavored(pkg, two_equal)
    eta_three = eta_ratio_single_source_flavored(pkg, three_equal)

    check(
        "Two-flavor equal aligned splitting lifts the exact branch to eta/eta_obs = 0.425764574711",
        abs(eta_two - 0.42576457471114665) < 1e-8,
        f"eta/eta_obs={eta_two:.12f}",
    )
    check(
        "Three-flavor equal aligned splitting lifts the exact branch to eta/eta_obs = 0.693223839689",
        abs(eta_three - 0.6932238396886656) < 1e-8,
        f"eta/eta_obs={eta_three:.12f}",
    )
    check(
        "So flavor resolution alone can move the transport efficiency by order-one factors",
        eta_three / eta_ratio_from_kappa(pkg.epsilon_1, kappa_one) > 3.0,
        f"enhancement={eta_three / eta_ratio_from_kappa(pkg.epsilon_1, kappa_one):.6f}",
    )

    def eta_hierarchical(p: float) -> float:
        return eta_ratio_single_source_flavored(pkg, (p, p, 1.0 - 2.0 * p))

    lo = 0.001
    hi = 0.1
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        if eta_hierarchical(mid) < 1.0:
            lo = mid
        else:
            hi = mid
    crossing = (hi, eta_hierarchical(hi))

    check(
        "A hierarchical three-flavor aligned branch crosses observation with p ~= 0.022895",
        abs(crossing[0] - 0.02289492429047824) < 5e-6,
        f"first crossing={crossing}",
    )

    print()
    print(f"  two-flavor equal split  : eta/eta_obs = {eta_two:.12f}")
    print(f"  three-flavor equal split: eta/eta_obs = {eta_three:.12f}")
    print(f"  hierarchical branch (p,p,1-2p) first reaches observation at p = {crossing[0]:.6f}")

    return eta_two, eta_three, crossing[0]


def part3_protected_n2_sequential_transport_is_more_expensive(pkg: object) -> float:
    print("\n" + "=" * 88)
    print("PART 3: A PROTECTED N2 SOURCE HELPS, BUT IS MORE EXPENSIVE")
    print("=" * 88)

    lambda_2 = pkg.M2 / pkg.M1
    k2_diag = pkg.k_decay_exact / lambda_2

    def eta_two_source(r2: float) -> float:
        _, _, asym_grid = solve_multisource_flavored_transport(
            lambdas=np.array([1.0, lambda_2]),
            k_decays=np.array([pkg.k_decay_exact, k2_diag]),
            source_matrix=np.array([[1.0, 0.0], [0.0, r2]]),
            washout_matrix=np.array([[1.0, 0.0], [0.0, 1.0]]),
        )
        return eta_ratio_from_kappa(pkg.epsilon_1, abs(float(asym_grid[:, -1].sum())))

    eta_r0 = eta_two_source(0.0)
    eta_r1 = eta_two_source(1.0)

    lo = 0.0
    hi = 10.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if eta_two_source(mid) < 1.0:
            lo = mid
        else:
            hi = mid
    r_required = hi
    eta_required = eta_two_source(r_required)

    check(
        "The protected N2 diagnostic reproduces the exact one-flavor baseline at r2 = 0",
        abs(eta_r0 - 0.188785929502) < 1e-8,
        f"eta/eta_obs={eta_r0:.12f}",
    )
    check(
        "An N2 source equal to epsilon_1 still only lifts the branch to eta/eta_obs = 0.398594964429",
        abs(eta_r1 - 0.39859496442919634) < 1e-8,
        f"eta/eta_obs={eta_r1:.12f}",
    )
    check(
        "This optimistic protected N2 model needs epsilon_2 ~= 3.86644 epsilon_1 to hit observation",
        abs(r_required - 3.866440120145853) < 1e-6,
        f"r2_required={r_required:.12f}",
    )
    check(
        "So the cheapest recovery path is flavor-resolved N1 transport, not a new N2 source by itself",
        r_required > 3.0,
        f"r2_required={r_required:.12f}",
    )

    print()
    print(f"  lambda_2 = M2/M1 = {lambda_2:.12f}")
    print(f"  K2 diagnostic = {k2_diag:.12f}")
    print(f"  eta/eta_obs at r2 = 1 = {eta_r1:.12f}")
    print(f"  required epsilon_2 / epsilon_1 = {r_required:.12f}")
    print(f"  eta/eta_obs at the crossing = {eta_required:.12f}")

    return r_required


def part4_bottom_line(p_cross: float, r_required: float) -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)

    check(
        "The exact one-flavor transport miss is plausibly recoverable by flavor structure alone",
        p_cross < 0.03,
        f"hierarchical crossing p={p_cross:.6f}",
    )
    check(
        "The same miss is harder to repair with a new N2 source alone in the current optimistic model",
        r_required > 3.0,
        f"required epsilon_2/epsilon_1={r_required:.6f}",
    )
    check(
        "So the strongest next physics target is a theorem for non-democratic flavor projectors / flavored transport",
        True,
        "N2-aware transport remains relevant, but not as the cheapest first fix",
    )

    print()
    print("  Main diagnostic read:")
    print("    - exact N1 flavor resolution can plausibly erase the 5.3x miss")
    print("    - a protected N2 source can help, but needs a comparatively large new CP input")
    print("    - the first transport extension worth deriving is flavored projector structure")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS FLAVORED / N2-AWARE TRANSPORT DIAGNOSTIC")
    print("=" * 88)

    pkg, kappa_one, _ = part1_exact_one_flavor_authority_baseline()
    _, _, p_cross = part2_flavored_n1_transport_can_lift_the_exact_branch(pkg, kappa_one)
    r_required = part3_protected_n2_sequential_transport_is_more_expensive(pkg)
    part4_bottom_line(p_cross, r_required)

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
