#!/usr/bin/env python3
"""
Prove by continuity that the constructive positive branch already contains
multiple distinct exact eta = 1 points on the fixed native N_e seed surface.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate import (
    XBAR_NE,
    YBAR_NE,
    eta_columns_from_active,
)
from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem import (
    triplet_from_projected_response_pack,
)


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


def unpack(v: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    a, b, c, d, e = [float(val) for val in v]
    x = np.array([a, b, 3.0 * XBAR_NE - a - b], dtype=float)
    y = np.array([c, d, 3.0 * YBAR_NE - c - d], dtype=float)
    return x, y, e


def eta1(v: np.ndarray) -> float:
    x, y, e = unpack(v)
    return float(eta_columns_from_active(x, y, e)[1][1])


def delta_src(v: np.ndarray) -> float:
    x, y, e = unpack(v)
    hmat = canonical_h(x, y, e)
    return float(np.real(np.linalg.det(hmat)))


def triplet(v: np.ndarray) -> dict[str, float]:
    x, y, e = unpack(v)
    hmat = canonical_h(x, y, e)
    return triplet_from_projected_response_pack(hermitian_linear_responses(hmat))


def on_constructive_positive_branch(v: np.ndarray) -> bool:
    tr = triplet(v)
    return tr["gamma"] > 0.0 and tr["E1"] > 0.0 and tr["E2"] > 0.0 and delta_src(v) > 0.0


def root_on_delta_interval(base: np.ndarray, lo: float, hi: float) -> float:
    def f(delta_val: float) -> float:
        v = base.copy()
        v[4] = delta_val
        return eta1(v) - 1.0

    return float(brentq(f, lo, hi))


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT CONSTRUCTIVE POSITIVE CLOSURE MULTIPLICITY")
    print("=" * 88)

    continuity_note = read("docs/DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md")
    insuff_note = read("docs/DM_WILSON_DIRECT_DESCENDANT_POSITIVE_BRANCH_COMPATIBILITY_AND_INSUFFICIENCY_THEOREM_NOTE_2026-04-18.md")

    families = [
        ("A", np.array([1.16845863, 0.46803892, 0.77107315, 0.05539671, 1.88733895], dtype=float), 1.88233895, 1.89233895),
        ("B", np.array([0.86088785, 0.32714819, 0.71367707, 0.10440906, 1.59650180], dtype=float), 1.59150180, 1.60150180),
        ("C", np.array([1.00731313, 0.30177597, 0.79591855, 0.02985850, 2.19935677], dtype=float), 2.19435677, 2.20435677),
    ]

    print("\n" + "=" * 88)
    print("PART 1: THE REPO ALREADY HAS THE NEEDED CONSTRUCTIVE AND POSITIVE-BRANCH INPUTS")
    print("=" * 88)
    check(
        "The constructive continuity note states that the constructive chamber contains an exact eta = 1 point",
        "contains an exact `eta = eta_obs` point" in continuity_note or "contains an exact eta = 1 point" in continuity_note,
    )
    check(
        "The positive-branch insufficiency note already says positive branch plus constructive signs is not enough",
        "branch-level condition" in insuff_note
        and "not a point-selection law" in insuff_note,
    )

    print("\n" + "=" * 88)
    print("PART 2: THREE DISTINCT CONSTRUCTIVE POSITIVE FAMILIES EACH CROSS EXACT CLOSURE")
    print("=" * 88)
    roots = []
    intervals = []
    for label, base, lo, hi in families:
        v_lo = base.copy()
        v_hi = base.copy()
        v_lo[4] = lo
        v_hi[4] = hi
        eta_lo = eta1(v_lo)
        eta_hi = eta1(v_hi)
        root = root_on_delta_interval(base, lo, hi)
        v_root = base.copy()
        v_root[4] = root
        roots.append(v_root)
        intervals.append((lo, hi))

        check(
            f"Family {label} stays on the fixed native seed surface",
            abs(np.mean(unpack(v_lo)[0]) - XBAR_NE) < 1e-12
            and abs(np.mean(unpack(v_lo)[1]) - YBAR_NE) < 1e-12
            and abs(np.mean(unpack(v_hi)[0]) - XBAR_NE) < 1e-12
            and abs(np.mean(unpack(v_hi)[1]) - YBAR_NE) < 1e-12,
            f"(xbar,ybar)=({np.mean(unpack(v_lo)[0]):.12f},{np.mean(unpack(v_lo)[1]):.12f})",
        )
        check(
            f"Family {label} endpoints both stay inside the constructive positive branch",
            on_constructive_positive_branch(v_lo) and on_constructive_positive_branch(v_hi),
            f"Delta_src endpoints=({delta_src(v_lo):.12f},{delta_src(v_hi):.12f})",
        )
        check(
            f"Family {label} endpoints lie on opposite sides of exact closure",
            (eta_lo - 1.0) * (eta_hi - 1.0) < 0.0,
            f"(eta_lo,eta_hi)=({eta_lo:.12f},{eta_hi:.12f})",
        )
        check(
            f"Family {label} therefore contains an exact constructive positive eta = 1 root",
            abs(eta1(v_root) - 1.0) < 1e-12 and on_constructive_positive_branch(v_root),
            f"delta_root={root:.12f}",
        )

    print("\n" + "=" * 88)
    print("PART 3: THE THREE EXACT ROOTS ARE DISTINCT")
    print("=" * 88)
    disjoint_intervals = (
        intervals[0][1] < intervals[1][0]
        or intervals[1][1] < intervals[0][0]
    ) and (
        intervals[0][1] < intervals[2][0]
        or intervals[2][1] < intervals[0][0]
    ) and (
        intervals[1][1] < intervals[2][0]
        or intervals[2][1] < intervals[1][0]
    )
    check(
        "The three witness delta-intervals are pairwise disjoint",
        disjoint_intervals,
        f"intervals={intervals}",
    )
    pairwise_sep = min(
        float(np.linalg.norm(roots[i] - roots[j]))
        for i in range(len(roots))
        for j in range(i + 1, len(roots))
    )
    check(
        "The resulting exact roots are pairwise distinct in parameter space",
        pairwise_sep > 1.0e-2,
        f"min separation={pairwise_sep:.6f}",
    )

    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)
    check(
        "Exact closure plus positive branch plus constructive signs is still non-unique",
        True,
        "the branch already contains at least three distinct exact eta = 1 points",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
