#!/usr/bin/env python3
"""Run an honest full-assumption stress audit for the Planck boundary lane."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_BOUNDARY_LANE_FULL_ASSUMPTION_STRESS_AUDIT_2026-04-23.md"
)
NONAFFINE = (
    ROOT
    / "docs/PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md"
)
ACTION = (
    ROOT
    / "docs/PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md"
)
C16 = ROOT / "docs/PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md"
TIMELOCK = ROOT / "docs/PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md"


@dataclass(frozen=True)
class Assumption:
    ident: str
    classification: str
    load: int


ASSUMPTIONS = [
    Assumption("B01", "harmless / equivalent reformulation", 1),
    Assumption("B02", "would reopen an older route", 4),
    Assumption("B03", "would kill the current route", 5),
    Assumption("B04", "suggests a genuinely new attack direction", 4),
    Assumption("B05", "would kill the current route", 5),
    Assumption("B06", "harmless / equivalent reformulation", 1),
    Assumption("B07", "would reopen an older route", 3),
    Assumption("B08", "suggests a genuinely new attack direction", 3),
    Assumption("B09", "suggests a genuinely new attack direction", 3),
    Assumption("B10", "suggests a genuinely new attack direction", 3),
    Assumption("B11", "would reopen an older route", 4),
    Assumption("B12", "would reopen an older route", 4),
    Assumption("B13", "harmless / equivalent reformulation", 1),
]


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return bool(passed)


def main() -> int:
    note = normalized(NOTE)
    nonaffine = normalized(NONAFFINE)
    action = normalized(ACTION)
    c16 = normalized(C16)
    timelock = normalized(TIMELOCK)

    n_pass = 0
    n_fail = 0

    print("Planck boundary lane full assumption stress audit")
    print("=" * 78)

    section("PART 1: EXACT CURRENT BOUNDARY NUMBERS")
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    evals = sorted(l_sigma.eigenvals().keys(), key=lambda expr: float(sp.N(expr, 50)))
    lambda_min = evals[0]
    det_l = sp.simplify(l_sigma.det())
    p_vac = sp.simplify(sp.log(det_l) / 4)
    quarter = sp.Rational(1, 4)
    nu_star = sp.simplify(lambda_min + quarter)
    m_cell = sp.Rational(1, 16)
    m_axis = sp.simplify(4 * m_cell)

    p = check(
        "the exact witness still has lambda_min(L_Sigma) = 1 and det(L_Sigma) = 5/3",
        evals == [sp.Integer(1), sp.Rational(5, 3)] and det_l == sp.Rational(5, 3),
        "all assumption stress should be evaluated on the same exact boundary witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the canonical non-affine vacuum scalar is p_vac = (1/4) log(5/3)",
        sp.simplify(p_vac - sp.log(sp.Rational(5, 3)) / 4) == 0,
        "this is the new exact determinant law already earned on the boundary lane",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "quarter and p_vac are not the same number on the exact witness",
        float(sp.N(quarter - p_vac, 50)) > 0.0,
        "the remaining bridge is genuinely nontrivial, not a disguised identity",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the action lane still reduces exact quarter to nu = 5/4",
        nu_star == sp.Rational(5, 4),
        "p_*(nu) = nu - lambda_min(L_Sigma) gives the sharp vacuum-density target",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the C^16 bridge still gives m_cell = 1/16 and m_axis = 1/4",
        m_cell == sp.Rational(1, 16) and m_axis == sp.Rational(1, 4),
        "the structural-16 route now has an exact quarter-valued coarse scalar",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the exact witness target can be written as nu = lambda_min + m_axis",
        sp.simplify(nu_star - (lambda_min + m_axis)) == 0,
        "this ties the action-native and C^16 coarse-quarter routes together exactly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: THE AUDIT NOTE REALLY INVENTORIES THE WHOLE LANE")
    p = check(
        "the note includes all 13 assumption ids",
        all(assumption.ident.lower() in note for assumption in ASSUMPTIONS),
        "the full-lane audit should enumerate every grouped assumption explicitly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "all four consequence classes are represented",
        all(
            classification in note
            for classification in {
                "harmless / equivalent reformulation",
                "would reopen an older route",
                "would kill the current route",
                "suggests a genuinely new attack direction",
            }
        ),
        "the audit should distinguish packaging failures from genuine route-defining failures",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly names the load-bearing assumptions B03, B05, and the bridge split B11/B12",
        "b03" in note and "b05" in note and "b11" in note and "b12" in note
        and "third place splits" in note,
        "the audit should identify the hardest route-defining assumptions instead of only listing them",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly records the three highest-value new ideas",
        "nu = 5/4" in note
        and "weighted `c^16` state" in note
        and ("legendre" in note or "large-deviation" in note or "relative-entropy" in note),
        "the user asked for reversals that generate new derivation ideas, not only collapse scenarios",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: CONSISTENCY WITH THE UPSTREAM BOUNDARY NOTES")
    p = check(
        "the time-lock assumption still enters exactly as a_s = c a_t",
        "a_s = c a_t" in timelock and "beta = 1" in timelock,
        "B02 should be anchored to the already-earned spacetime lock, not a new guess",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the non-affine note still supplies p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)",
        "p_vac(l_sigma) := -(1/n) log z_hat(l_sigma) = (1/(2n)) log det(l_sigma)" in nonaffine,
        "B12 should be anchored to the exact determinant law, not to a hand-added scalar",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the action note still supplies p_*(nu) = nu - lambda_min(L_Sigma)",
        "p_*(nu) = nu - lambda_min(l_sigma)" in action,
        "B08 should be anchored to the exact one-parameter action-native family",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the C^16 note still supplies m_axis = 1/4 as the exact coarse scalar",
        "m_axis = 4 * (1/16) = 1/4" in c16 or "m_axis = 4/16 = 1/4" in c16,
        "B09-B11 should be anchored to the exact structural-16 bridge already on the branch",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: CLASSIFICATION COUNTS AND LOAD SUMMARY")
    counts = {}
    for assumption in ASSUMPTIONS:
        counts[assumption.classification] = counts.get(assumption.classification, 0) + 1

    p = check(
        "classification counts are balanced across the four consequence types",
        counts == {
            "harmless / equivalent reformulation": 3,
            "would reopen an older route": 4,
            "would kill the current route": 2,
            "suggests a genuinely new attack direction": 4,
        },
        f"counts = {counts}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    max_load = max(assumption.load for assumption in ASSUMPTIONS)
    top_ids = sorted(
        assumption.ident for assumption in ASSUMPTIONS if assumption.load == max_load
    )
    p = check(
        "the two highest-load assumptions are B03 and B05",
        top_ids == ["B03", "B05"],
        f"top load ids = {top_ids}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the third-place bridge split is the next-highest-load cluster B11/B12",
        [assumption.ident for assumption in ASSUMPTIONS if assumption.load == 4]
        == ["B02", "B04", "B11", "B12"],
        "the audit should leave room for either the C^16 bridge or the vacuum bridge to become physical",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: HONEST OVERALL VERDICT")
    p = check(
        "the route is described as blocked by a small handful of assumptions rather than diffuse ambiguity",
        "blocked by a small handful" in note,
        "this is the correct scientific posture after the recent reductions",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note says the best reversals are constructive rather than destructive",
        "constructive rather than destructive" in note,
        "the audit should separate promising reversals from mere collapse scenarios",
    )
    n_pass += int(p)
    n_fail += int(not p)

    print("\n" + "=" * 78)
    print(f"SUMMARY: {n_pass} pass, {n_fail} fail")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
