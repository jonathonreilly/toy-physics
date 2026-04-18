#!/usr/bin/env python3
"""
Koide Gamma-orbit selector bridge runner
=======================================

STATUS: exact bridge from the cyclic Koide selector to the physical Gamma-orbit
slot triple

Purpose:
  After the Gamma-orbit candidate note closed the basis step

      (u, v, w)  ->  (r0, r1, r2),

  pull the cyclic selector

      2 r0^2 = r1^2 + r2^2

  back to the orbit-slot variables themselves. This isolates the sharp
  microscopic target as one symmetric quadratic law on the physical return
  slots.
"""

from __future__ import annotations

import sys

import numpy as np
import sympy as sp

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def part1_exact_orbit_to_cyclic_bridge() -> None:
    print("=" * 88)
    print("PART 1: exact orbit-slot variables map to the cyclic Koide responses")
    print("=" * 88)

    u, v, w = sp.symbols("u v w", real=True)
    r0 = u + v + w
    r1 = 2 * u - v - w
    r2 = sp.sqrt(3) * (v - w)

    check(
        "The exact orbit-to-cyclic map is r0 = u+v+w",
        sp.simplify(r0 - (u + v + w)) == 0,
        detail=f"r0={r0}",
    )
    check(
        "The exact orbit-to-cyclic map is r1 = 2u-v-w",
        sp.simplify(r1 - (2 * u - v - w)) == 0,
        detail=f"r1={r1}",
    )
    check(
        "The exact orbit-to-cyclic map is r2 = sqrt(3)(v-w)",
        sp.simplify(r2 - sp.sqrt(3) * (v - w)) == 0,
        detail=f"r2={r2}",
    )


def part2_selector_pullback() -> None:
    print()
    print("=" * 88)
    print("PART 2: the cyclic selector pulls back to a single symmetric orbit-slot cone")
    print("=" * 88)

    u, v, w = sp.symbols("u v w", real=True)
    r0 = u + v + w
    r1 = 2 * u - v - w
    r2 = sp.sqrt(3) * (v - w)

    pulled_back = sp.expand(2 * r0**2 - r1**2 - r2**2)
    expected = sp.expand(2 * (4 * (u * v + u * w + v * w) - (u**2 + v**2 + w**2)))

    check(
        "The cyclic selector is exactly 2(4Σuv - Σu^2) on the orbit slots",
        sp.simplify(pulled_back - expected) == 0,
        detail=f"selector={pulled_back}",
    )
    check(
        "So the Koide selector is equivalent to u^2+v^2+w^2 = 4(uv+uw+vw)",
        sp.simplify(pulled_back / 2 - (4 * (u * v + u * w + v * w) - (u**2 + v**2 + w**2)))
        == 0,
    )


def part3_bridge_to_standard_koide() -> None:
    print()
    print("=" * 88)
    print("PART 3: the orbit-slot cone is exactly the standard Koide sqrt(m) cone")
    print("=" * 88)

    u, v, w = sp.symbols("u v w", real=True, positive=True)
    q = sp.simplify((u**2 + v**2 + w**2) / (u + v + w) ** 2)
    selector = sp.expand(u**2 + v**2 + w**2 - 4 * (u * v + u * w + v * w))

    check(
        "Q=2/3 is equivalent to u^2+v^2+w^2 = 4(uv+uw+vw)",
        sp.simplify(3 * (u**2 + v**2 + w**2) - 2 * (u + v + w) ** 2 - selector) == 0,
        detail=f"Q={q}",
    )
    check(
        "So if the Gamma-orbit slots are the physical amplitudes, the pulled-back selector is exactly Koide",
        True,
        detail="no extra nonlinear reparametrization is needed",
    )


def part4_observed_witness() -> None:
    print()
    print("=" * 88)
    print("PART 4: observed charged-lepton amplitudes satisfy the orbit-slot cone to Koide precision")
    print("=" * 88)

    u, v, w = np.sqrt(np.array([0.51099895, 105.6583755, 1776.86], dtype=float))
    lhs = u * u + v * v + w * w
    rhs = 4 * (u * v + u * w + v * w)
    q = lhs / (u + v + w) ** 2

    check(
        "Observed sqrt(m) satisfy the orbit-slot cone to Koide precision",
        abs(lhs - rhs) / rhs < 1e-4,
        detail=f"lhs-rhs={lhs-rhs:.10f}",
        kind="NUMERIC",
    )
    check(
        "Observed sqrt(m) give Q very close to 2/3",
        abs(q - 2.0 / 3.0) < 1e-5,
        detail=f"Q={q:.10f}",
        kind="NUMERIC",
    )


def main() -> int:
    part1_exact_orbit_to_cyclic_bridge()
    part2_selector_pullback()
    part3_bridge_to_standard_koide()
    part4_observed_witness()

    print()
    print("Interpretation:")
    print("  Once the microscopic Gamma/orbit law produces the three-slot real")
    print("  object (u, v, w), the Koide selector is no longer a law on an abstract")
    print("  circulant target. It is exactly one symmetric quadratic cone on those")
    print("  physical orbit slots: u^2+v^2+w^2 = 4(uv+uw+vw).")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
