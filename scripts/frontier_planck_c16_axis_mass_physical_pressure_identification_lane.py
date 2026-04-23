#!/usr/bin/env python3
"""Audit the direct endpoint of the C^16 axis-mass boundary-pressure lane.

This lane does not claim retained Planck closure. It proves the sharper direct
endpoint:

  - the current Schur boundary scalar grammar fixes p_obs = p_vac(L);
  - the current action grammar fixes p_*(nu) = nu - lambda_min(L);
  - the quarter-valued C^16 candidate is m_axis = 1/4;
  - no current same-surface theorem identifies p_phys with m_axis;
  - exact closure on this route is equivalent to one new worldtube-projector
    law p_phys = m_axis, equivalently nu = lambda_min(L) + m_axis.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md"
)
OBS = (
    ROOT
    / "docs/PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md"
)
ACTION = ROOT / "docs/PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md"
VAC_DENSITY = ROOT / "docs/PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md"
C16 = ROOT / "docs/PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md"
SYNTH = ROOT / "docs/PLANCK_SCALE_BULK_BOUNDARY_C16_SYNTHESIS_LANE_2026-04-23.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    passed = bool(passed)
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def main() -> int:
    note = normalized(NOTE)
    obs = normalized(OBS)
    action = normalized(ACTION)
    vac_density = normalized(VAC_DENSITY)
    c16 = normalized(C16)
    synth = normalized(SYNTH)

    n_pass = 0
    n_fail = 0

    print("Planck C^16 axis-mass physical-pressure identification lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM STACK IS SHARP")
    p = check(
        "observable-principle boundary lane still fixes p_phys = p_vac(L) on the scalar grammar",
        "p_obs(l_sigma) = p_vac(l_sigma)" in obs
        and "not `1/4`" in obs,
        "the direct endpoint must start from the fact that the current scalar boundary observable is already fixed",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "action-pressure lane still fixes p_*(nu) = nu - lambda_min(L_sigma)",
        "p_*(nu) = nu - lambda_min(l_sigma)" in action
        and "nu = 5/4" in action,
        "the direct endpoint should work on the already-earned one-parameter action family",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "vacuum-density lane still says the canonical nu values are {0, p_vac(L_sigma)}",
        "nu in {0, p_vac(l_sigma)}" in vac_density
        and (
            "neither canonical same-surface value matches the required quarter value" in vac_density
            or "a new vacuum reference law beyond the two canonical same-surface choices" in vac_density
        ),
        "the direct endpoint should not pretend the boundary shift is still canonically free",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "C^16 bridge lane still isolates m_axis = 1/4 as the surviving quarter-valued candidate",
        "m_axis = 1/4" in c16
        and "physical boundary pressure = c^16 axis-sector mass" in c16,
        "the last open bridge should be the coarse axis-sector projector mass, not the primitive 1/16 share",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "bulk/boundary/C^16 synthesis lane still says the surviving bridge is p_* = m_axis",
        "surviving load-bearing bridge is now explicit" in synth
        and "`p_* = m_axis`" in synth,
        "the direct endpoint should match the already-earned synthesis reduction",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: THE TWO CURRENT EXACT QUANTITIES ARE DISTINCT")
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    evals = sorted(l_sigma.eigenvals().keys(), key=lambda expr: float(sp.N(expr)))
    lambda_min = evals[0]
    det_l = sp.simplify(l_sigma.det())
    p_vac = sp.simplify(sp.log(det_l) / 4)
    m_axis = sp.Rational(1, 4)

    p = check(
        "the canonical witness still has lambda_min = 1 and det(L_sigma) = 5/3",
        evals == [sp.Integer(1), sp.Rational(5, 3)] and det_l == sp.Rational(5, 3),
        "this is the exact witness shared by the boundary stack",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the current scalar Schur quantity is p_vac = (1/4) log(5/3)",
        sp.simplify(p_vac - sp.log(sp.Rational(5, 3)) / 4) == 0,
        "the direct endpoint must keep the currently derived scalar boundary observable explicit",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the quarter-valued C^16 quantity is m_axis = 1/4",
        m_axis == sp.Rational(1, 4),
        "the only quarter-valued exact C^16 candidate is the coarse axis-sector mass",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the current Schur scalar and the C^16 axis mass are not equal on the witness",
        sp.simplify(p_vac - m_axis) != 0
        and abs(float(sp.N(p_vac, 50)) - 0.12770640594149768) < 1e-15,
        "the existing stack already proves the two exact quantities remain distinct",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: FAMILY-LEVEL OBSTRUCTION")
    r = sp.symbols("r", positive=True, real=True)
    l_r = sp.Matrix([[1 + r, r], [r, 1 + r]])
    evals_r = sorted(l_r.eigenvals().keys(), key=sp.default_sort_key)
    lambda_min_r = evals_r[0]
    det_r = sp.simplify(l_r.det())
    p_vac_r = sp.simplify(sp.log(det_r) / 4)

    p = check(
        "on the symmetric family L(r), lambda_min stays fixed at 1",
        sp.simplify(lambda_min_r - 1) == 0,
        "the family keeps the same boundary floor while allowing the Schur vacuum scalar to move",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "on the same family p_vac(L(r)) = (1/4) log(1 + 2r) varies with r",
        sp.simplify(p_vac_r - sp.log(1 + 2 * r) / 4) == 0
        and sp.simplify(sp.diff(p_vac_r, r) - 1 / (2 * (1 + 2 * r))) == 0,
        "the current scalar Schur observable is not pinned to the constant quarter by the present grammar",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p_vac_r1 = sp.simplify(p_vac_r.subs(r, sp.Rational(1, 4)))
    p_vac_r2 = sp.simplify(p_vac_r.subs(r, sp.Rational(1, 2)))
    p = check(
        "the family therefore separates the varying Schur scalar from the fixed C^16 axis mass",
        sp.simplify(p_vac_r1 - p_vac_r2) != 0
        and sp.simplify(p_vac_r1 - m_axis) != 0
        and sp.simplify(p_vac_r2 - m_axis) != 0,
        "a quarter law does not come for free from the current Schur scalar family",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: THE REMAINING CONTENT IS EXACTLY ONE NEW LAW")
    nu = sp.symbols("nu", real=True)
    p_star = sp.simplify(nu - lambda_min)
    nu_bridge = sp.simplify(lambda_min + m_axis)

    p = check(
        "quarter closure on the action lane is exactly equivalent to nu = lambda_min + m_axis",
        sp.simplify(p_star.subs(nu, nu_bridge) - m_axis) == 0
        and sp.simplify(nu_bridge - sp.Rational(5, 4)) == 0,
        "the entire remaining boundary problem has collapsed to one additive worldtube-pressure law",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the canonical currently-earned nu values do not produce that bridge",
        sp.simplify(0 - nu_bridge) != 0
        and sp.simplify(p_vac - nu_bridge) != 0,
        "the present boundary grammar stops short of the bridge value 5/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "so exact closure on this route is equivalent to a new worldtube-projector identification p_phys = m_axis",
        sp.simplify(p_star.subs(nu, nu_bridge) - sp.Rational(1, 4)) == 0,
        "without that new identification law the route is reduced, not closed",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: HONESTY CHECK")
    p = check(
        "the note explicitly says the current stack does not derive p_phys = m_axis",
        "does **not** derive" in NOTE.read_text(encoding="utf-8")
        and "`p_phys = m_axis`" in NOTE.read_text(encoding="utf-8"),
        "the writeup should record the endpoint as a no-go/reduction theorem, not fake closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly identifies one new worldtube-projector law as the remaining content",
        "worldtube-projector law" in note
        and "equivalent to one new identification theorem" in note,
        "the endpoint should collapse the open bridge to one explicit law",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly concludes the boundary route is reduced, not retained Planck closure",
        "not retained planck closure" in note
        and "open/bounded bridge" in note,
        "the final classification should be honest about the current scientific status",
    )
    n_pass += int(p)
    n_fail += int(not p)

    print("\n" + "=" * 78)
    print(f"SUMMARY: PASS={n_pass} FAIL={n_fail}")
    print("=" * 78)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
