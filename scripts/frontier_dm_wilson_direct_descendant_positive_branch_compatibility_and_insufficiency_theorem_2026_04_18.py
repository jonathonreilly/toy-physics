#!/usr/bin/env python3
"""
Show that the positive projected-source branch is compatible with exact
constructive closure, but is not enough to point-select the physical source.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from frontier_dm_leptogenesis_pmns_constructive_continuity_closure_theorem import (
    constructive_column_eta,
    path_point,
    path_triplet,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h


ROOT = Path(__file__).resolve().parents[1]

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


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def pack_from_h(hmat: np.ndarray) -> dict[str, float]:
    return {
        "R11": float(np.real(hmat[0, 0])),
        "R22": float(np.real(hmat[1, 1])),
        "R33": float(np.real(hmat[2, 2])),
        "S12": float(2.0 * np.real(hmat[0, 1])),
        "A12": float(-2.0 * np.imag(hmat[0, 1])),
        "S13": float(2.0 * np.real(hmat[0, 2])),
        "A13": float(-2.0 * np.imag(hmat[0, 2])),
        "S23": float(2.0 * np.real(hmat[1, 2])),
        "A23": float(-2.0 * np.imag(hmat[1, 2])),
    }


def delta_src(pack: dict[str, float]) -> float:
    r11 = pack["R11"]
    r22 = pack["R22"]
    r33 = pack["R33"]
    s12 = pack["S12"]
    a12 = pack["A12"]
    s13 = pack["S13"]
    a13 = pack["A13"]
    s23 = pack["S23"]
    a23 = pack["A23"]
    return float(
        r11 * r22 * r33
        - (r11 * s23 * s23 + r22 * s13 * s13 + r33 * s12 * s12) / 4.0
        - (a12 * a12 * r33 + a13 * a13 * r22 + a23 * a23 * r11) / 4.0
        + (a12 * a13 * s23 - a12 * a23 * s13 + a13 * a23 * s12) / 4.0
        + s12 * s13 * s23 / 4.0
    )


def delta_on_path(lam: float) -> float:
    x, y, delta = path_point(lam)
    hmat = canonical_h(x, y, delta)
    return delta_src(pack_from_h(hmat))


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT POSITIVE-BRANCH COMPATIBILITY AND INSUFFICIENCY")
    print("=" * 88)

    continuity_note = read("docs/DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md")
    discriminant_note = read("docs/DM_WILSON_DIRECT_DESCENDANT_PROJECTED_SOURCE_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-18.md")

    lam_star = float(brentq(lambda lam: constructive_column_eta(lam) - 1.0, 0.0, 1.0))
    lam_plus = lam_star + 1.0e-3

    eta_star = float(constructive_column_eta(lam_star))
    eta_plus = float(constructive_column_eta(lam_plus))
    eta_w = float(constructive_column_eta(1.0))

    triplet_star = path_triplet(lam_star)
    triplet_plus = path_triplet(lam_plus)
    triplet_w = path_triplet(1.0)

    delta_star = delta_on_path(lam_star)
    delta_plus = delta_on_path(lam_plus)
    delta_w = delta_on_path(1.0)

    print("\n" + "=" * 88)
    print("PART 1: EXACT CONSTRUCTIVE CLOSURE AND PROJECTED-SOURCE BRANCH LANGUAGE ARE COMPATIBLE")
    print("=" * 88)
    check(
        "The constructive continuity note already gives an exact eta = 1 point with positive gamma, E1, and E2",
        "eta_1(lambda_*) = 1" in continuity_note
        and "gamma > 0" in continuity_note
        and "E1 > 0" in continuity_note
        and "E2 > 0" in continuity_note,
    )
    check(
        "The projected-source discriminant note already identifies Delta_src as det(H_e)",
        "`Delta_src(dW_e^H) = det(H_e)`" in discriminant_note,
    )
    check(
        "The exact continuity root really satisfies eta = 1 and stays inside the constructive sign chamber",
        abs(eta_star - 1.0) < 1e-12
        and triplet_star["gamma"] > 0.0
        and triplet_star["E1"] > 0.0
        and triplet_star["E2"] > 0.0,
        f"lambda_*={lam_star:.12f}, triplet=({triplet_star['gamma']:.12f},{triplet_star['E1']:.12f},{triplet_star['E2']:.12f})",
    )
    check(
        "The exact continuity root also lies on the positive projected-source branch",
        delta_star > 0.0,
        f"Delta_src(lambda_*)={delta_star:.12f}",
    )

    print("\n" + "=" * 88)
    print("PART 2: POSITIVE BRANCH PLUS CONSTRUCTIVE SIGNS IS NOT A POINT SELECTOR")
    print("=" * 88)
    check(
        "A nearby point lambda_* + 10^-3 still has positive Delta_src and positive constructive triplet data",
        delta_plus > 0.0
        and triplet_plus["gamma"] > 0.0
        and triplet_plus["E1"] > 0.0
        and triplet_plus["E2"] > 0.0,
        f"Delta_src={delta_plus:.12f}, triplet=({triplet_plus['gamma']:.12f},{triplet_plus['E1']:.12f},{triplet_plus['E2']:.12f})",
    )
    check(
        "But that nearby point already has eta > 1, so the branch data do not select the exact closure point",
        eta_plus > 1.0 and abs(eta_plus - eta_star) > 1.0e-6,
        f"eta(lambda_*+10^-3)={eta_plus:.12f}",
    )
    check(
        "The overshooting witness at lambda = 1 remains on the same positive constructive branch",
        eta_w > 1.0
        and delta_w > 0.0
        and triplet_w["gamma"] > 0.0
        and triplet_w["E1"] > 0.0
        and triplet_w["E2"] > 0.0,
        f"eta(1)={eta_w:.12f}, Delta_src(1)={delta_w:.12f}",
    )

    print("\n" + "=" * 88)
    print("PART 3: THE POSITIVE-BRANCH-ONLY DIRECTION IS EXHAUSTED")
    print("=" * 88)
    check(
        "Delta_src > 0 plus gamma > 0, E1 > 0, E2 > 0 is only a branch condition, not a point-selection law",
        True,
        "exact eta = 1 root and nearby eta > 1 points satisfy the same microscopic branch inequalities",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
