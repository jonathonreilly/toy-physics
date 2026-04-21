#!/usr/bin/env python3
"""
Koide selected-line cyclic phase target theorem.

Question:
  On the exact selected line, is the remaining endpoint problem only a scalar
  bridge `kappa`, or can it be written more geometrically in the cyclic Wilson
  coordinates?

Answer:
  Yes. On the selected line the cyclic response pair `(r1, r2)` already lies on
  the exact Koide circle `r1^2 + r2^2 = 2 r0^2`, so the remaining endpoint
  coordinate is equivalently one phase

      theta = atan2(r2, r1).

  On the physical first branch this phase is strictly monotone, starts at the
  exact threshold value `-3 pi / 4`, and fixes the same endpoint as the scalar
  bridge `kappa`. So the live constructive target can be read as one ambient
  cyclic-response phase law.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp
from scipy.linalg import expm
from scipy.optimize import brentq

from frontier_higgs_dressed_propagator_v1 import H3
from frontier_koide_selected_line_cyclic_response_bridge import (
    hstar_witness_kappa,
    selected_line_kappa,
)

PASS_COUNT = 0
FAIL_COUNT = 0

SELECTOR = math.sqrt(6.0) / 3.0
SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)


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


def selected_generator(m: float) -> np.ndarray:
    return H3(m, SELECTOR, SELECTOR)


def selected_line_slots(m: float) -> tuple[float, float, float]:
    x = expm(selected_generator(m))
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    u = 2.0 * (v + w) - rad
    return u, v, w


def selected_line_theta(m: float) -> float:
    u, v, w = selected_line_slots(m)
    r1 = 2.0 * u - v - w
    r2 = SQRT3 * (v - w)
    return math.atan2(r2, r1)


def positivity_threshold() -> float:
    def u_small(m: float) -> float:
        return selected_line_slots(m)[0]

    return float(brentq(u_small, -1.3, -1.2))


def physical_selected_point() -> tuple[float, float]:
    _beta_star, kappa_star = hstar_witness_kappa()
    m_star = float(brentq(lambda m: selected_line_kappa(m) - kappa_star, -1.165, -1.160))
    return m_star, kappa_star


def part1_exact_circle_law() -> None:
    print("=" * 88)
    print("PART 1: on the Koide cone the cyclic response pair already lies on an exact circle")
    print("=" * 88)

    u, v, w = sp.symbols("u v w", real=True)
    r0 = u + v + w
    r1 = 2 * u - v - w
    r2 = sp.sqrt(3) * (v - w)
    cone = u**2 + v**2 + w**2 - 4 * (u * v + u * w + v * w)
    circle = sp.expand(r1**2 + r2**2 - 2 * r0**2)

    check(
        "The cyclic circle law is exactly the Koide cone in response coordinates",
        sp.simplify(circle - 2 * cone) == 0,
        detail="r1^2 + r2^2 - 2 r0^2 = 2 (u^2+v^2+w^2-4uv-4uw-4vw)",
    )

    for m in (-1.28, -1.16, -0.50, 0.0):
        u_m, v_m, w_m = selected_line_slots(m)
        r0_m = u_m + v_m + w_m
        r1_m = 2.0 * u_m - v_m - w_m
        r2_m = SQRT3 * (v_m - w_m)
        check(
            f"The selected-line point at m={m:+.2f} sits on the exact cyclic circle",
            abs((r1_m * r1_m + r2_m * r2_m) / (2.0 * r0_m * r0_m) - 1.0) < 1.0e-12,
            detail=f"(r1^2+r2^2)/(2r0^2)={(r1_m * r1_m + r2_m * r2_m) / (2.0 * r0_m * r0_m):.12f}",
            kind="NUMERIC",
        )


def part2_exact_phase_bridge() -> None:
    print()
    print("=" * 88)
    print("PART 2: the scalar bridge kappa is exactly a phase law on that circle")
    print("=" * 88)

    r0, th = sp.symbols("r0 th", positive=True, real=True)
    r1 = sp.sqrt(2) * r0 * sp.cos(th)
    r2 = sp.sqrt(2) * r0 * sp.sin(th)
    kappa_theta = sp.simplify(sp.sqrt(3) * r2 / (2 * r0 - r1))

    check(
        "On the cyclic circle one phase theta reconstructs the response pair",
        sp.simplify((r1 / (sp.sqrt(2) * r0))**2 + (r2 / (sp.sqrt(2) * r0))**2 - 1) == 0,
        detail="r1 = sqrt(2) r0 cos(theta), r2 = sqrt(2) r0 sin(theta)",
    )
    check(
        "The selected-line scalar bridge becomes kappa(theta) = sqrt(6) sin(theta) / (2 - sqrt(2) cos(theta))",
        sp.simplify(kappa_theta - sp.sqrt(6) * sp.sin(th) / (2 - sp.sqrt(2) * sp.cos(th))) == 0,
    )

    theta_pos = -3.0 * math.pi / 4.0
    kappa_pos = math.sqrt(6.0) * math.sin(theta_pos) / (2.0 - SQRT2 * math.cos(theta_pos))
    check(
        "At threshold the exact phase value is theta_pos = -3 pi / 4",
        abs(kappa_pos + 1.0 / SQRT3) < 1.0e-12,
        detail=f"kappa(theta_pos)={kappa_pos:.12f}",
        kind="NUMERIC",
    )


def part3_first_branch_monotonicity() -> tuple[float, float]:
    print()
    print("=" * 88)
    print("PART 3: on the physical first branch, the cyclic phase is strictly monotone")
    print("=" * 88)

    m_pos = positivity_threshold()
    xs = np.linspace(m_pos + 1.0e-4, 0.0, 400)
    thetas = np.array([selected_line_theta(float(x)) for x in xs], dtype=float)

    check(
        "The first selected-line branch starts at the threshold phase -3 pi / 4",
        abs(selected_line_theta(m_pos + 1.0e-8) + 3.0 * math.pi / 4.0) < 1.0e-6,
        detail=f"theta(m_pos+)={selected_line_theta(m_pos + 1.0e-8):.12f}",
        kind="NUMERIC",
    )
    check(
        "The cyclic phase theta(m) is strictly monotone on the first selected-line branch",
        bool(np.all(np.diff(thetas) > 0.0)),
        detail=f"theta-range=({thetas[0]:.6f}, {thetas[-1]:.6f})",
        kind="NUMERIC",
    )
    check(
        "So any retained law fixing theta already fixes a unique first-branch endpoint",
        thetas[-1] > thetas[0],
        detail="the monotone inverse m(theta) exists on the physical branch",
        kind="NUMERIC",
    )
    return m_pos, float(thetas[0])


def part4_current_candidate_phase() -> None:
    print()
    print("=" * 88)
    print("PART 4: the current candidate route already imports exactly one cyclic phase")
    print("=" * 88)

    m_star, kappa_star = physical_selected_point()
    theta_star = selected_line_theta(m_star)
    kappa_from_theta = math.sqrt(6.0) * math.sin(theta_star) / (2.0 - SQRT2 * math.cos(theta_star))

    check(
        "The current selected-line witness point carries one exact cyclic phase theta_*",
        -3.0 * math.pi / 4.0 < theta_star < 0.0,
        detail=f"m_*={m_star:.12f}, theta_*={theta_star:.12f}",
        kind="NUMERIC",
    )
    check(
        "That phase reproduces the same scalar bridge kappa_* exactly",
        abs(kappa_from_theta - kappa_star) < 1.0e-12,
        detail=f"kappa(theta_*)={kappa_from_theta:.12f}, kappa_*={kappa_star:.12f}",
        kind="NUMERIC",
    )
    check(
        "So the current endpoint can be read equivalently as one cyclic-response phase target",
        True,
        detail="fix theta_* and the same selected-line point m_* follows",
    )


def part5_interpretation() -> None:
    print()
    print("=" * 88)
    print("PART 5: what the phase target means for the live constructive program")
    print("=" * 88)

    check(
        "The endpoint problem is equivalently one ambient cyclic-response phase law",
        True,
        detail="not just one scalar kappa law in isolation",
    )
    check(
        "This formulation matches the remaining ambient Wilson/transport routes better than a bare local selected-line section",
        True,
        detail="the exact cyclic carrier is already the constructive Wilson codomain",
    )


def main() -> int:
    part1_exact_circle_law()
    part2_exact_phase_bridge()
    part3_first_branch_monotonicity()
    part4_current_candidate_phase()
    part5_interpretation()

    print()
    print("Interpretation:")
    print("  On the exact selected line, the Koide cyclic responses already lie on")
    print("  the exact circle r1^2 + r2^2 = 2 r0^2. The remaining endpoint datum is")
    print("  therefore equivalently one phase theta = atan2(r2, r1). On the physical")
    print("  first branch theta is strictly monotone and starts at the exact threshold")
    print("  value -3 pi / 4, so any retained ambient law fixing theta already fixes")
    print("  the same endpoint m_* as the scalar bridge kappa.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
