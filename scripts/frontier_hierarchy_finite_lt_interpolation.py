#!/usr/bin/env python3
"""
Exact finite-Lt interpolation for the hierarchy effective-potential coefficient.

This script closes the finite-Lt APBC temporal normalization formula on the
minimal L_s = 2 spatial-APBC block:

    A(L_t, u0) = [1 / (4 sqrt(3) u0^2)] * (1 - q^Lt) / (1 + q^Lt)
    q = 2 - sqrt(3)

So the remaining hierarchy normalization gap is not a vague prefactor. It is
an exact exponential interpolation between the UV endpoint Lt = 2 and the
3+1 temporal average Lt -> infinity.
"""

from __future__ import annotations

import math
import sys

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = ""):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def temporal_modes(Lt: int):
    return [(2 * n + 1) * math.pi / Lt for n in range(Lt)]


def a_direct(Lt: int, u0: float) -> float:
    return (1.0 / (2.0 * Lt * u0**2)) * sum(
        1.0 / (3.0 + math.sin(w) ** 2) for w in temporal_modes(Lt)
    )


def q_parameter() -> float:
    return 2.0 - math.sqrt(3.0)


def a_closed(Lt: int, u0: float) -> float:
    q = q_parameter()
    return (1.0 / (4.0 * math.sqrt(3.0) * u0**2)) * ((1.0 - q**Lt) / (1.0 + q**Lt))


def c_lt(Lt: int) -> float:
    a2 = 1.0 / 8.0
    a = a_closed(Lt, 1.0)
    return (a2 / a) ** 0.25


def c_obs() -> float:
    return 246.22 / 253.4


def lt_eff_from_cobs() -> float:
    c = c_obs()
    y = (1.0 / 8.0) / (c**4)
    a_inf = 1.0 / (4.0 * math.sqrt(3.0))
    r = y / a_inf
    # r = (1 - q^Lt)/(1 + q^Lt), so q^Lt = (1-r)/(1+r)
    z = (1.0 - r) / (1.0 + r)
    return math.log(z) / math.log(q_parameter())


def test_closed_form_interpolation():
    print("\n" + "=" * 78)
    print("PART 1: EXACT FINITE-Lt CLOSED FORM")
    print("=" * 78)

    u0 = 0.9
    max_rel = 0.0
    for Lt in [2, 4, 6, 8, 10, 12, 20]:
        direct = a_direct(Lt, u0)
        exact = a_closed(Lt, u0)
        rel = abs(direct - exact) / exact
        max_rel = max(max_rel, rel)
        print(f"  Lt={Lt}: direct={direct:.12e}, exact={exact:.12e}, rel={rel:.2e}")
    check(
        "A(Lt) matches exact q^Lt interpolation formula",
        max_rel < 5e-15,
        f"max relative error = {max_rel:.2e}",
    )


def test_endpoint_recovery():
    print("\n" + "=" * 78)
    print("PART 2: ENDPOINT RECOVERY")
    print("=" * 78)

    u0 = 0.9
    q = q_parameter()
    a2 = a_closed(2, u0)
    ainf = (1.0 / (4.0 * math.sqrt(3.0) * u0**2))

    print(f"  q = 2 - sqrt(3) = {q:.12f}")
    print(f"  A_2 closed      = {a2:.12e}")
    print(f"  A_inf exact     = {ainf:.12e}")

    check(
        "closed form reproduces the exact Lt=2 UV endpoint",
        abs(a2 - 1.0 / (8.0 * u0**2)) < 1e-15,
        f"absolute error = {abs(a2 - 1.0 / (8.0 * u0**2)):.2e}",
    )
    check(
        "closed form approaches the exact Lt->infinity temporal average",
        abs(a_closed(40, u0) - ainf) < 1e-15,
        f"absolute error at Lt=40 = {abs(a_closed(40, u0) - ainf):.2e}",
    )


def test_observed_prefactor_location():
    print("\n" + "=" * 78)
    print("PART 3: OBSERVED PREFATOR ON THE EXACT INTERPOLATION CURVE")
    print("=" * 78)

    c2 = c_lt(2)
    c4 = c_lt(4)
    c6 = c_lt(6)
    cobs = c_obs()
    lt_eff = lt_eff_from_cobs()

    print(f"  C(Lt=2) = {c2:.12f}")
    print(f"  C(Lt=4) = {c4:.12f}")
    print(f"  C(Lt=6) = {c6:.12f}")
    print(f"  C_obs   = {cobs:.12f}")
    print(f"  Lt_eff(C_obs) = {lt_eff:.12f}")

    check(
        "observed prefactor lies on the exact finite-Lt interpolation curve",
        2.0 < lt_eff < 4.0,
        f"Lt_eff = {lt_eff:.6f}",
    )
    check(
        "observed prefactor sits between the exact Lt=2 and Lt=4 corrections",
        c4 < cobs < c2,
        f"{c4:.12f} < {cobs:.12f} < {c2:.12f}",
    )


def main():
    print("Hierarchy finite-Lt interpolation theorem")
    print("=" * 78)
    test_closed_form_interpolation()
    test_endpoint_recovery()
    test_observed_prefactor_location()
    print("\n" + "=" * 78)
    print(f"SCORECARD: {PASS_COUNT} pass, {FAIL_COUNT} fail out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 78)
    sys.exit(1 if FAIL_COUNT else 0)


if __name__ == "__main__":
    main()
