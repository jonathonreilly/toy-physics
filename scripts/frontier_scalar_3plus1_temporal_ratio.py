#!/usr/bin/env python3
"""
Exact scalar 3+1 temporal ratio on the minimal APBC block.

The exact theorem is the endpoint pair

    A_2   = 1 / 8
    A_inf = 1 / (4 sqrt(3))

and the exact ratio

    A_inf / A_2 = 2 / sqrt(3).

The fourth-root factor for a dimension-4 scalar density is reported as a
support corollary rather than promoted here as a standalone observable-level
insertion theorem.
"""

from __future__ import annotations

import math

import numpy as np


def apbc_frequencies(lt: int) -> np.ndarray:
    n = np.arange(lt, dtype=float)
    return 2.0 * math.pi * (n + 0.5) / lt


def scalar_bridge_coefficient(lt: int) -> float:
    omega = apbc_frequencies(lt)
    return float(np.mean(1.0 / (3.0 + np.sin(omega) ** 2)) / 2.0)


def a2_exact() -> float:
    return 1.0 / 8.0


def ainf_exact() -> float:
    return 1.0 / (4.0 * math.sqrt(3.0))


def completion_ratio() -> float:
    return ainf_exact() / a2_exact()


def dim4_scalar_density_factor() -> float:
    return completion_ratio() ** 0.25


def fmt(x: float) -> str:
    return f"{x:.15f}"


def check_close(name: str, value: float, target: float, tol: float) -> tuple[bool, str]:
    delta = abs(value - target)
    ok = delta <= tol
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={fmt(value)} target={fmt(target)} delta={delta:.3e} tol={tol:.1e}"


def main() -> int:
    a2_direct = scalar_bridge_coefficient(2)
    a8_direct = scalar_bridge_coefficient(8)
    a4096_direct = scalar_bridge_coefficient(4096)
    a2 = a2_exact()
    ainf = ainf_exact()
    ratio = completion_ratio()
    factor = dim4_scalar_density_factor()

    print("=" * 78)
    print("SCALAR 3+1 TEMPORAL RATIO")
    print("=" * 78)
    print()
    print("Exact theorem surface")
    print("  K_sc(omega) = 3 + sin^2(omega)")
    print("  A(L_t)      = (1 / (2 L_t)) sum_omega 1 / (3 + sin^2 omega)")
    print()
    print(f"  A_2 direct                 = {fmt(a2_direct)}")
    print(f"  A_2 exact                  = {fmt(a2)}")
    print(f"  A_8 direct                 = {fmt(a8_direct)}")
    print(f"  A_4096 direct              = {fmt(a4096_direct)}")
    print(f"  A_inf exact                = {fmt(ainf)}")
    print(f"  A_inf / A_2                = {fmt(ratio)}")
    print()
    print("Support corollary")
    print(f"  Gamma_sc,cand = ratio^(1/4)= {fmt(factor)}")
    print()

    exact_checks: list[tuple[bool, str]] = []
    exact_checks.append(check_close("A_2 direct", a2_direct, a2, 1.0e-15))
    exact_checks.append(
        (
            a8_direct > a2 and a8_direct < ainf,
            "PASS: A_8 lies strictly between the UV endpoint and the temporal average"
            if (a8_direct > a2 and a8_direct < ainf)
            else "FAIL: A_8 lies strictly between the UV endpoint and the temporal average",
        )
    )
    exact_checks.append(check_close("A_4096 approaches A_inf", a4096_direct, ainf, 1.0e-12))
    exact_checks.append(check_close("A_inf / A_2", ratio, 2.0 / math.sqrt(3.0), 1.0e-15))

    support_checks: list[tuple[bool, str]] = []
    support_checks.append(
        check_close(
            "dimension-4 scalar-density factor candidate",
            factor,
            (2.0 / math.sqrt(3.0)) ** 0.25,
            1.0e-15,
        )
    )

    exact_pass = 0
    support_pass = 0

    print("Checks")
    for ok, msg in exact_checks:
        print(" ", msg)
        exact_pass += int(ok)
    for ok, msg in support_checks:
        print(" ", msg)
        support_pass += int(ok)

    fail = (len(exact_checks) - exact_pass) + (len(support_checks) - support_pass)
    print()
    print(f"SUMMARY: EXACT PASS={exact_pass} SUPPORT={support_pass} FAIL={fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
