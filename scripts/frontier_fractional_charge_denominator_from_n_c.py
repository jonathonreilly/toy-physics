#!/usr/bin/env python3
"""Exact audit for the fractional-charge-denominator-from-N_c theorem."""

from __future__ import annotations

from fractions import Fraction
from math import gcd
import sys


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 80)
    print(title)
    print("-" * 80)


def hypercharges(n_c: int) -> tuple[Fraction, Fraction]:
    """Return (Y_Q, Y_L) from trace zero plus Y_L = -1."""
    y_l = Fraction(-1, 1)
    y_q = -y_l / n_c
    return y_q, y_l


def left_charges(n_c: int) -> dict[str, Fraction]:
    """Return left-handed charges with Q = T3 + Y/2."""
    y_q, y_l = hypercharges(n_c)
    return {
        "u_L": Fraction(1, 2) + y_q / 2,
        "d_L": Fraction(-1, 2) + y_q / 2,
        "nu_L": Fraction(1, 2) + y_l / 2,
        "e_L": Fraction(-1, 2) + y_l / 2,
    }


def nonzero_charge_denominator(charges: dict[str, Fraction]) -> int:
    denoms = [charge.denominator for charge in charges.values() if charge != 0]
    return max(denoms) if denoms else 1


def expected_denominator(n_c: int) -> int:
    return n_c if n_c % 2 else 2 * n_c


def witten_ok(n_c: int) -> bool:
    # A retained-style generation has N_D = N_c + 1 weak doublets.
    return (n_c + 1) % 2 == 0


def audit_retained_n_c_3() -> None:
    banner("Retained N_c = 3 left-handed trace and charges")

    n_c = 3
    y_q, y_l = hypercharges(n_c)
    trace = 2 * n_c * y_q + 2 * y_l
    ratio = y_q / y_l
    charges = left_charges(n_c)

    print(f"  Y(Q_L) = {y_q}; Y(L_L) = {y_l}; trace = {trace}")
    print("  left-handed charges:")
    for field in ("u_L", "d_L", "nu_L", "e_L"):
        print(f"    Q({field}) = {charges[field]}")

    check("Y(Q_L) = 1/3", y_q == Fraction(1, 3), f"actual={y_q}")
    check("Y(L_L) = -1", y_l == Fraction(-1, 1), f"actual={y_l}")
    check("2 N_c Y(Q_L) + 2 Y(L_L) = 0", trace == 0, f"trace={trace}")
    check("Y(Q_L)/Y(L_L) = -1/3", ratio == Fraction(-1, 3), f"ratio={ratio}")
    check("Q(u_L) = 2/3", charges["u_L"] == Fraction(2, 3), f"actual={charges['u_L']}")
    check("Q(d_L) = -1/3", charges["d_L"] == Fraction(-1, 3), f"actual={charges['d_L']}")
    check("Q(nu_L) = 0", charges["nu_L"] == 0, f"actual={charges['nu_L']}")
    check("Q(e_L) = -1", charges["e_L"] == Fraction(-1, 1), f"actual={charges['e_L']}")


def audit_full_sm_charge_set() -> None:
    banner("Retained full one-generation charge set after RH uniqueness input")

    y_q, y_l = hypercharges(3)
    rh_hypercharges = {
        "u_R": Fraction(4, 3),
        "d_R": Fraction(-2, 3),
        "e_R": Fraction(-2, 1),
        "nu_R": Fraction(0, 1),
    }
    charges = left_charges(3)
    charges.update({field: y / 2 for field, y in rh_hypercharges.items()})

    expected = {
        "u_L": Fraction(2, 3),
        "d_L": Fraction(-1, 3),
        "nu_L": Fraction(0, 1),
        "e_L": Fraction(-1, 1),
        "u_R": Fraction(2, 3),
        "d_R": Fraction(-1, 3),
        "e_R": Fraction(-1, 1),
        "nu_R": Fraction(0, 1),
    }

    print(f"  input Y(Q_L)={y_q}, Y(L_L)={y_l}")
    for field in sorted(charges):
        print(f"    Q({field}) = {charges[field]}")

    for field, expected_charge in expected.items():
        check(
            f"Q({field}) = {expected_charge}",
            charges[field] == expected_charge,
            f"actual={charges[field]}",
        )

    denoms = {charge.denominator for charge in charges.values() if charge != 0}
    check("full nonzero denominator set is contained in {1, 3}", denoms <= {1, 3}, f"denoms={sorted(denoms)}")


def audit_n_c_denominator_scan() -> None:
    banner("N_c denominator parity scan")

    print("  N_c  parity  Y(Q_L)  Q(u_L)  Q(d_L)  denom  expected")
    for n_c in range(1, 11):
        y_q, _ = hypercharges(n_c)
        charges = left_charges(n_c)
        denom = nonzero_charge_denominator(charges)
        expected = expected_denominator(n_c)
        parity = "odd" if n_c % 2 else "even"
        print(
            f"  {n_c:>3}  {parity:>6}  {str(y_q):>6}  "
            f"{str(charges['u_L']):>6}  {str(charges['d_L']):>6}  "
            f"{denom:>5}  {expected:>8}"
        )
        check(
            f"N_c={n_c}: denominator rule",
            denom == expected,
            f"actual={denom}, expected={expected}",
        )


def audit_witten_scan() -> None:
    banner("Witten parity scan")

    print("  N_c  N_D=N_c+1  Witten_ok  expected_odd")
    for n_c in range(1, 11):
        ok = witten_ok(n_c)
        expected = n_c % 2 == 1
        print(f"  {n_c:>3}  {n_c + 1:>9}  {str(ok):>9}  {str(expected):>12}")
        check(
            f"N_c={n_c}: Witten consistency iff N_c is odd",
            ok == expected,
            f"N_D={n_c + 1}",
        )


def audit_gcd_structure() -> None:
    banner("GCD structure behind denominator reduction")

    odd_samples = [1, 3, 5]
    even_samples = [2, 4, 6]

    for n_c in odd_samples:
        g = gcd(n_c + 1, 2 * n_c)
        reduced = Fraction(n_c + 1, 2 * n_c)
        check(
            f"odd N_c={n_c}: gcd(N_c+1, 2 N_c)=2",
            g == 2,
            f"reduced Q(u_L)={reduced}",
        )

    for n_c in even_samples:
        g = gcd(n_c + 1, 2 * n_c)
        reduced = Fraction(n_c + 1, 2 * n_c)
        check(
            f"even N_c={n_c}: gcd(N_c+1, 2 N_c)=1",
            g == 1,
            f"reduced Q(u_L)={reduced}",
        )


def main() -> int:
    print("=" * 80)
    print("Fractional charge denominator from N_c theorem audit")
    print("=" * 80)

    audit_retained_n_c_3()
    audit_full_sm_charge_set()
    audit_n_c_denominator_scan()
    audit_witten_scan()
    audit_gcd_structure()

    print()
    print("=" * 80)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 80)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
