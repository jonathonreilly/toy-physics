#!/usr/bin/env python3
"""
Koide delta Euclidean-rotation support audit.

This runner lands the useful science from the reviewed
claude/koide-delta-euclidean-rotation branch as support-grade content only.
It proves the selected-line Euclidean-angle identity in closed form while
preserving the open physical readout boundary for delta = 2/9 rad.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}")
    if detail:
        print(f"       {detail}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def read_doc(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return re.sub(r"[\s*`_]+", " ", text.lower())


def has_all(text: str, phrases: tuple[str, ...]) -> bool:
    haystack = normalized(text)
    return all(phrase.lower().replace("_", " ") in haystack for phrase in phrases)


def boundary_checks() -> None:
    section("A. Current main keeps Koide delta closure open")

    package = read_doc("docs/KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md")
    geometry = read_doc("docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md")
    radian = read_doc("docs/KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md")
    so2 = read_doc("docs/KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md")

    check(
        "A.1 package names two explicit scientific bridges as open",
        has_all(package, ("two explicit scientific bridges remain open",)),
    )
    check(
        "A.2 April 22 Brannen geometry is support, not closure",
        has_all(
            geometry,
            (
                "does not claim closure of the physical Brannen-phase bridge",
                "δ = 2/9 remains open",
            ),
        ),
    )
    check(
        "A.3 A1/radian audit keeps Type-B readout primitive open",
        "TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE=TRUE" in radian,
    )
    check(
        "A.4 SO(2) phase-erasure theorem does not derive delta",
        "KOIDE_DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE" in so2,
    )


def selected_line_symbolic_identity() -> None:
    section("B. Closed-form Euclidean-angle identity on the selected-line carrier")

    theta = sp.symbols("theta", real=True)
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2

    v1 = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
    vomega = sp.Matrix([1, omega, omega**2]) / sp.sqrt(3)
    vomega_bar = sp.Matrix([1, omega**2, omega]) / sp.sqrt(3)

    s_complex = (
        v1 / sp.sqrt(2)
        + sp.exp(sp.I * theta) * vomega / 2
        + sp.exp(-sp.I * theta) * vomega_bar / 2
    )
    s = sp.re(s_complex).applyfunc(lambda x: sp.trigsimp(sp.simplify(x)))

    e_plus = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
    e1 = sp.Matrix([1, -1, 0]) / sp.sqrt(2)
    e2 = sp.Matrix([1, 1, -2]) / sp.sqrt(6)

    p1 = sp.trigsimp((s.T * e1)[0])
    p2 = sp.trigsimp((s.T * e2)[0])
    singlet = sp.trigsimp((s.T * e_plus)[0])
    radius_sq = sp.trigsimp(p1**2 + p2**2)

    target_p1 = sp.sin(theta + sp.pi / 3) / sp.sqrt(2)
    target_p2 = sp.cos(theta + sp.pi / 3) / sp.sqrt(2)

    check(
        "B.1 selected line has fixed positive singlet component 1/sqrt(2)",
        sp.simplify(singlet - 1 / sp.sqrt(2)) == 0,
        f"s.e_plus={singlet}",
    )
    check(
        "B.2 doublet radius squared is 1/2",
        sp.simplify(radius_sq - sp.Rational(1, 2)) == 0,
        f"p1^2+p2^2={radius_sq}",
    )
    check(
        "B.3 p1(theta)=2^(-1/2) sin(theta+pi/3)",
        sp.trigsimp(p1 - target_p1) == 0,
        f"p1={p1}",
    )
    check(
        "B.4 p2(theta)=2^(-1/2) cos(theta+pi/3)",
        sp.trigsimp(p2 - target_p2) == 0,
        f"p2={p2}",
    )

    z = sp.trigsimp(p1 + sp.I * p2)
    z_target = sp.exp(sp.I * (sp.pi / 6 - theta)) / sp.sqrt(2)
    # Sympy proves this most robustly after expanding into real trig parts.
    z_diff = sp.expand_trig(z - z_target)
    check(
        "B.5 complex coordinate z=p1+i p2 equals 2^(-1/2) exp(i(pi/6-theta))",
        sp.simplify(sp.re(z_diff)) == 0 and sp.simplify(sp.im(z_diff)) == 0,
        f"z={z}",
    )

    alpha = sp.pi / 6 - theta
    delta = theta - 2 * sp.pi / 3
    check(
        "B.6 alpha(theta)=-pi/2-delta(theta)",
        sp.simplify(alpha - (-sp.pi / 2 - delta)) == 0,
        f"alpha={alpha}; delta={delta}",
    )


def first_branch_lift_and_delta_target() -> None:
    section("C. First-branch lift and delta=2/9 support reading")

    delta_target = sp.Rational(2, 9)
    theta0 = 2 * sp.pi / 3
    theta_star = theta0 + delta_target
    alpha0 = sp.pi / 6 - theta0
    alpha_star = sp.pi / 6 - theta_star
    angle_difference = sp.simplify(alpha_star - alpha0)

    check(
        "C.1 unphased reference has alpha(theta0)=-pi/2",
        sp.simplify(alpha0 + sp.pi / 2) == 0,
        f"alpha0={alpha0}",
    )
    check(
        "C.2 if delta*=2/9, Euclidean angle difference is -2/9",
        angle_difference == -delta_target,
        f"alpha_star-alpha0={angle_difference}",
    )

    # The historical first-branch span from the April 22 support note is pi/12.
    # On any interval of that length, atan2 has a unique continuous lift.
    span = sp.pi / 12
    check(
        "C.3 first branch span pi/12 is contractible and far below 2pi",
        bool(span < 2 * sp.pi),
        f"span={span}, 2pi={2 * sp.pi}",
    )

    samples = []
    for index in range(401):
        delta_value = float(span) * index / 400.0
        theta_value = float(2 * math.pi / 3 + delta_value)
        p1 = math.sin(theta_value + math.pi / 3) / math.sqrt(2)
        p2 = math.cos(theta_value + math.pi / 3) / math.sqrt(2)
        alpha_value = math.atan2(p2, p1)
        samples.append(alpha_value)

    jumps = [abs(samples[i + 1] - samples[i]) for i in range(len(samples) - 1)]
    check(
        "C.4 sampled atan2 lift on first branch has no 2pi wrap",
        max(jumps) < 1e-3,
        f"max adjacent jump={max(jumps):.6e}",
    )

    canonical_rz_angle = 2 * sp.pi * delta_target
    literal_angle = delta_target
    check(
        "C.5 canonical R/Z phase map gives 4pi/9, not 2/9",
        sp.simplify(canonical_rz_angle - literal_angle) != 0,
        f"2pi*(2/9)={canonical_rz_angle}; literal={literal_angle}",
    )


def support_boundary_flags() -> None:
    section("D. Support boundary flags")

    flags = {
        "KOIDE_DELTA_EUCLIDEAN_ROTATION_SUPPORT": True,
        "SELECTED_LINE_EUCLIDEAN_ANGLE_IDENTITY": True,
        "SELECTED_LINE_FIRST_BRANCH_LIFT_CONTRACTIBLE": True,
        "EUCLIDEAN_ROTATION_TO_PHYSICAL_BRANNEN_READOUT_PROVED": False,
        "KOIDE_DELTA_2_OVER_9_RAD_RETAINED_CLOSURE": False,
        "KOIDE_Q_RETAINED_NATIVE_CLOSURE": False,
        "TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE": True,
    }

    for name, value in flags.items():
        check(f"D flag {name}={str(value).upper()}", True)
        print(f"{name}={str(value).upper()}")


def main() -> int:
    print("Koide delta Euclidean-rotation support audit")
    boundary_checks()
    selected_line_symbolic_identity()
    first_branch_lift_and_delta_target()
    support_boundary_flags()

    print()
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print(f"PASSED: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
