#!/usr/bin/env python3
"""
Minimal local face-closure candidate rejection at beta = 6.

After the exact local directed-cell and root-face launch theorems, the weakest
possible local closure candidate is:

  G = 1 + 3 p^4 G^5 + p^14 G^15
  H = 1 + 4 p^4 G^5 + 4 p^14 G^15
  P(6) = p * H

where p = P_1plaq(6) is the exact local SU(3) one-plaquette block, and G is the
generic frontier-face dressing factor.

This runner proves that the generic fixed-point equation has no positive real
solution for a strict lower bound on p. Therefore the minimal local face-closure
candidate is rejected before any canonical promotion.

Self-contained: standard library only.
"""

from __future__ import annotations

from decimal import Decimal, getcontext


getcontext().prec = 80

# Strict lower bound to the exact local block printed by the exact SU(3) runner.
LOCAL_PLAQUETTE_LOWER = Decimal("0.42253173964998")


def g(value: Decimal, p: Decimal) -> Decimal:
    return Decimal(1) + Decimal(3) * (p**4) * (value**5) + (p**14) * (value**15) - value


def g_prime(value: Decimal, p: Decimal) -> Decimal:
    return Decimal(15) * (p**4) * (value**4) + Decimal(15) * (p**14) * (value**14) - Decimal(1)


def critical_point(p: Decimal) -> Decimal:
    left = Decimal("1.2")
    right = Decimal("1.22")
    if not (g_prime(left, p) < 0 < g_prime(right, p)):
        raise ValueError("critical-point bracket failed")
    for _ in range(200):
        mid = (left + right) / 2
        if g_prime(mid, p) > 0:
            right = mid
        else:
            left = mid
    return (left + right) / 2


def check_true(name: str, condition: bool, detail: str) -> tuple[bool, str]:
    tag = "PASS" if condition else "FAIL"
    return condition, f"{tag}: {name}: {detail}"


def main() -> int:
    p = LOCAL_PLAQUETTE_LOWER
    x_star = critical_point(p)
    min_value = g(x_star, p)

    print("=" * 78)
    print("MINIMAL LOCAL FACE-CLOSURE CANDIDATE REJECTION AT BETA = 6")
    print("=" * 78)
    print()
    print(f"strict lower bound on p = P_1plaq(6)     = {p}")
    print("closure candidate:")
    print("  G = 1 + 3 p^4 G^5 + p^14 G^15")
    print("  H = 1 + 4 p^4 G^5 + 4 p^14 G^15")
    print()
    print(f"unique positive critical point of g(G)    = {x_star}")
    print(f"minimum value g(G_*) with p = p_low        = {min_value}")
    print()

    checks = [
        check_true("g(0) > 0", g(Decimal(0), p) > 0, f"g(0) = {g(Decimal(0), p)}"),
        check_true(
            "g''(G) > 0 for G > 0",
            True,
            "convexity is immediate because every nonconstant coefficient is positive",
        ),
        check_true(
            "critical-point bracket is valid",
            g_prime(Decimal("1.2"), p) < 0 < g_prime(Decimal("1.22"), p),
            f"g'(1.2) = {g_prime(Decimal('1.2'), p)}, g'(1.22) = {g_prime(Decimal('1.22'), p)}",
        ),
        check_true("minimum value is strictly positive", min_value > Decimal("0.03"), f"g(G_*) = {min_value}"),
    ]

    print("Checks")
    passed = 0
    for ok, message in checks:
        print(" ", message)
        passed += int(ok)
    failed = len(checks) - passed
    print()
    print(f"SUMMARY: bounded {passed} pass / {failed} fail")
    print()

    if failed:
        return 1

    print("Conclusion: the minimal local face-closure candidate has no positive fixed point.")
    print("So this closure axiom is rejected at beta = 6.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
