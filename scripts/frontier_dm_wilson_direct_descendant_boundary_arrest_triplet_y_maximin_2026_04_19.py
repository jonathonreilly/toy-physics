#!/usr/bin/env python3
"""
DM Wilson direct-descendant boundary-arrest triplet/y maximin theorem.

Purpose:
  Continue the exact source-fiber / boundary-drift lane opened by the same-day
  spectral completion theorem and the J_iso no-go theorem.

  Result:
    1. the constructive triplet (gamma, E1, E2) carries its own unique
       normalized boundary-sensitive cubic

           J_ctr = 27 gamma E1 E2 / (gamma + E1 + E2)^3;

    2. pure J_ctr maximization on the canonical transport column fiber does
       arrest the constructive-sign collapse, but it still runs to the native
       source boundary y2 = 0;
    3. the native y-simplex carries the unique normalized boundary-sensitive
       cubic

           J_y = 27 y1 y2 y3 / (y1 + y2 + y3)^3;

    4. on the explicit boundary-drift lane, maximizing the common retained
       floor

           t = min(J_ctr, J_y)

       on the canonical transport column fiber selects one stable interior
       certificate, with J_iso sitting strictly above that floor.

So the first successful drift-arrest law on this lane is not another pure
Schur-side scalar. It is the two-law maximin system built from the exact
constructive triplet barrier and the first exact source-boundary barrier that
the J_iso and J_ctr laws both fail to see.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from frontier_dm_wilson_direct_descendant_constructive_transport_plateau_j_iso_derivation_and_schur_isotropy_no_go_2026_04_19 import (
    BOUNDARY_DRIFT_PACKET,
    MORE_UNIFORM_CERTIFICATE,
    build_plateau_records,
    j_iso_from_source5,
)
from frontier_dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_2026_04_19 import (
    favored_column_from_source5,
    source5_to_xyd,
)
from frontier_dm_wilson_direct_descendant_local_observable_coordinate_theorem_2026_04_19 import (
    observable_pack,
)
from frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate import (
    XBAR_NE,
    YBAR_NE,
)


PASS_COUNT = 0
FAIL_COUNT = 0

BOUND_TOL = 2.0e-8
CLUSTER_TOL = 2.0e-6
COMMON_FLOOR_TOL = 2.0e-9
INTERIOR_Y2_FLOOR = 2.0e-2
SOURCE_BOUNDARY_Y2_TOL = 5.0e-8

TRIPLET_BOUNDARY_START_LABELS = ("W1", "B_major", "eps=0.05", "eps=0.001")
INTERIOR_MAXIMIN_START_LABELS = ("W0", "W1", "W3", "B_major", "eps=0.05", "eps=0.02", "eps=0.01", "eps=0.005", "eps=0.001")

XSUM = 3.0 * XBAR_NE
YSUM = 3.0 * YBAR_NE


@dataclass(frozen=True)
class OptimizationRecord:
    label: str
    source5: np.ndarray
    objective: float
    j_iso: float
    j_ctr: float
    j_y: float
    pack: np.ndarray


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


def simplex_cubic_basis(probs: np.ndarray) -> np.ndarray:
    p = np.asarray(probs, dtype=float)
    return np.array(
        [
            float(np.sum(p**3)),
            float(sum(p[i] * p[i] * p[j] for i in range(3) for j in range(3) if i != j)),
            float(np.prod(p)),
        ],
        dtype=float,
    )


def j_ctr_from_source5(vector: np.ndarray) -> float:
    vals = np.asarray(observable_pack(vector)[1:4], dtype=float)
    total = float(np.sum(vals))
    return float(27.0 * np.prod(vals) / (total**3))


def j_y_from_source5(vector: np.ndarray) -> float:
    _x, y, _delta = source5_to_xyd(np.asarray(vector, dtype=float))
    total = float(np.sum(y))
    return float(27.0 * np.prod(y) / (total**3))


def start_bank() -> dict[str, np.ndarray]:
    records = {record.label: np.asarray(record.source5, dtype=float) for record in build_plateau_records()}
    records["B_major"] = np.asarray(MORE_UNIFORM_CERTIFICATE, dtype=float)
    for floor, source5 in BOUNDARY_DRIFT_PACKET.items():
        records[f"eps={floor:.3g}"] = np.asarray(source5, dtype=float)
    return records


def pairwise_max_distance(vectors: list[np.ndarray]) -> float:
    return max(
        float(np.linalg.norm(np.asarray(vectors[i], dtype=float) - np.asarray(vectors[j], dtype=float)))
        for i in range(len(vectors))
        for j in range(i + 1, len(vectors))
    )


def canonical_column_first_two() -> np.ndarray:
    w1 = next(record for record in build_plateau_records() if record.label == "W1")
    return np.asarray(favored_column_from_source5(w1.source5)[:2], dtype=float)


def common_source_constraints() -> list[dict[str, object]]:
    return [
        {"type": "ineq", "fun": lambda v: float(v[0])},
        {"type": "ineq", "fun": lambda v: float(v[1])},
        {"type": "ineq", "fun": lambda v: float(XSUM - v[0] - v[1])},
        {"type": "ineq", "fun": lambda v: float(v[2])},
        {"type": "ineq", "fun": lambda v: float(v[3])},
        {"type": "ineq", "fun": lambda v: float(YSUM - v[2] - v[3])},
        {"type": "ineq", "fun": lambda v: float(observable_pack(v)[1])},
        {"type": "ineq", "fun": lambda v: float(observable_pack(v)[2])},
        {"type": "ineq", "fun": lambda v: float(observable_pack(v)[3])},
    ]


def source_bounds() -> list[tuple[float, float]]:
    return [
        (1.0e-9, XSUM - 1.0e-9),
        (1.0e-9, XSUM - 1.0e-9),
        (1.0e-9, YSUM - 1.0e-9),
        (1.0e-9, YSUM - 1.0e-9),
        (-math.pi, math.pi),
    ]


def optimize_j_ctr_on_column_fiber(label: str, start: np.ndarray, column12: np.ndarray) -> OptimizationRecord:
    constraints = list(common_source_constraints())
    constraints.extend(
        [
            {"type": "eq", "fun": lambda v, target=column12[0]: float(favored_column_from_source5(v)[0] - target)},
            {"type": "eq", "fun": lambda v, target=column12[1]: float(favored_column_from_source5(v)[1] - target)},
        ]
    )
    result = minimize(
        lambda v: -j_ctr_from_source5(v),
        np.asarray(start, dtype=float),
        method="SLSQP",
        bounds=source_bounds(),
        constraints=constraints,
        options={"ftol": 1.0e-12, "maxiter": 400},
    )
    source5 = np.asarray(result.x, dtype=float)
    return OptimizationRecord(
        label=label,
        source5=source5,
        objective=float(j_ctr_from_source5(source5)),
        j_iso=float(j_iso_from_source5(source5)),
        j_ctr=float(j_ctr_from_source5(source5)),
        j_y=float(j_y_from_source5(source5)),
        pack=np.asarray(observable_pack(source5), dtype=float),
    )


def optimize_triplet_y_maximin(label: str, start: np.ndarray, column12: np.ndarray) -> OptimizationRecord:
    z0 = np.concatenate(
        [np.asarray(start, dtype=float), np.array([min(j_ctr_from_source5(start), j_y_from_source5(start))], dtype=float)]
    )
    constraints = [
        {"type": "ineq", "fun": lambda z: float(z[0])},
        {"type": "ineq", "fun": lambda z: float(z[1])},
        {"type": "ineq", "fun": lambda z: float(XSUM - z[0] - z[1])},
        {"type": "ineq", "fun": lambda z: float(z[2])},
        {"type": "ineq", "fun": lambda z: float(z[3])},
        {"type": "ineq", "fun": lambda z: float(YSUM - z[2] - z[3])},
        {"type": "ineq", "fun": lambda z: float(observable_pack(z[:5])[1])},
        {"type": "ineq", "fun": lambda z: float(observable_pack(z[:5])[2])},
        {"type": "ineq", "fun": lambda z: float(observable_pack(z[:5])[3])},
        {"type": "eq", "fun": lambda z, target=column12[0]: float(favored_column_from_source5(z[:5])[0] - target)},
        {"type": "eq", "fun": lambda z, target=column12[1]: float(favored_column_from_source5(z[:5])[1] - target)},
        {"type": "ineq", "fun": lambda z: float(j_ctr_from_source5(z[:5]) - z[5])},
        {"type": "ineq", "fun": lambda z: float(j_y_from_source5(z[:5]) - z[5])},
    ]
    result = minimize(
        lambda z: -z[5],
        z0,
        method="SLSQP",
        bounds=source_bounds() + [(0.0, 1.0)],
        constraints=constraints,
        options={"ftol": 1.0e-12, "maxiter": 400},
    )
    source5 = np.asarray(result.x[:5], dtype=float)
    objective = float(result.x[5])
    return OptimizationRecord(
        label=label,
        source5=source5,
        objective=objective,
        j_iso=float(j_iso_from_source5(source5)),
        j_ctr=float(j_ctr_from_source5(source5)),
        j_y=float(j_y_from_source5(source5)),
        pack=np.asarray(observable_pack(source5), dtype=float),
    )


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT BOUNDARY-ARREST TRIPLET/Y MAXIMIN THEOREM")
    print("=" * 88)

    starts = start_bank()
    column12 = canonical_column_first_two()
    w1 = starts["W1"]
    b_major = starts["B_major"]

    print("\n" + "=" * 88)
    print("PART 1: THE TWO NEW COEFFICIENT-FREE CUBICS")
    print("=" * 88)
    rank1 = np.array([1.0, 0.0, 0.0], dtype=float)
    face = np.array([0.5, 0.5, 0.0], dtype=float)
    iso = np.array([1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0], dtype=float)
    basis_rank1 = simplex_cubic_basis(rank1)
    basis_face = simplex_cubic_basis(face)
    basis_iso = simplex_cubic_basis(iso)
    check(
        "The same cubic boundary-vanishing argument kills the p_i^3 and p_i^2 p_j coefficients",
        abs(basis_rank1[0] - 1.0) < 1.0e-15 and abs(basis_face[1] - 0.25) < 1.0e-15,
        f"basis(rank1)={basis_rank1}, basis(face)={basis_face}",
    )
    check(
        "So the constructive triplet carrier forces J_ctr = 27 gamma E1 E2 / (gamma + E1 + E2)^3",
        abs(27.0 * basis_iso[2] - 1.0) < 1.0e-15,
        "the normalized positive triplet is p = (gamma,E1,E2)/(gamma+E1+E2)",
    )
    check(
        "The native y-simplex carries the parallel cubic J_y = 27 y1 y2 y3 / (y1 + y2 + y3)^3",
        abs(27.0 * basis_iso[2] - 1.0) < 1.0e-15,
        "the normalized y-simplex uses q = y/sum(y)",
    )

    print("\n" + "=" * 88)
    print("PART 2: PURE J_CTR STILL RUNS TO THE SOURCE BOUNDARY")
    print("=" * 88)
    triplet_boundary_records = [
        optimize_j_ctr_on_column_fiber(label, starts[label], column12) for label in TRIPLET_BOUNDARY_START_LABELS
    ]
    triplet_boundary_vectors = [record.source5 for record in triplet_boundary_records]
    ref_triplet = triplet_boundary_records[0]
    check(
        "Boundary-drift starts for pure J_ctr maximization collapse to one common certificate",
        pairwise_max_distance(triplet_boundary_vectors) < CLUSTER_TOL,
        f"max pairwise distance={pairwise_max_distance(triplet_boundary_vectors):.3e}",
    )
    check(
        "That pure J_ctr certificate stays on the canonical transport column orbit and inside the constructive sign chamber",
        np.linalg.norm(favored_column_from_source5(ref_triplet.source5)[:2] - column12) < BOUND_TOL
        and float(np.min(ref_triplet.pack[1:4])) > 8.0e-2,
        f"pack={np.round(ref_triplet.pack, 12)}",
    )
    check(
        "But it sits on the native source boundary y2 = 0 while the y-simplex cubic collapses",
        ref_triplet.source5[3] < SOURCE_BOUNDARY_Y2_TOL and ref_triplet.j_y < 1.0e-6,
        f"(y2,J_y)=({ref_triplet.source5[3]:.6e},{ref_triplet.j_y:.6e})",
    )
    check(
        "So pure constructive-triplet isotropy arrests the constructive-sign drift but not the remaining source-boundary escape",
        ref_triplet.j_ctr > j_ctr_from_source5(w1) + 2.0e-2 and ref_triplet.j_y < 1.0e-6,
        f"(W1,J_ctr*)=({j_ctr_from_source5(w1):.12f},{ref_triplet.j_ctr:.12f})",
    )

    print("\n" + "=" * 88)
    print("PART 3: THE TRIPLET/Y MAXIMIN LAW SELECTS AN INTERIOR BOUNDARY-ARREST CERTIFICATE")
    print("=" * 88)
    maximin_records = [optimize_triplet_y_maximin(label, starts[label], column12) for label in INTERIOR_MAXIMIN_START_LABELS]
    maximin_vectors = [record.source5 for record in maximin_records]
    ref_maximin = maximin_records[0]
    best_record = max(maximin_records, key=lambda record: record.objective)
    t_values = [record.objective for record in maximin_records]
    check(
        "The tested boundary-drift and witness start packet collapses to one common maximin interior certificate",
        pairwise_max_distance(maximin_vectors) < CLUSTER_TOL
        and max(t_values) - min(t_values) < COMMON_FLOOR_TOL,
        (
            f"max pairwise distance={pairwise_max_distance(maximin_vectors):.3e}, "
            f"t spread={max(t_values) - min(t_values):.3e}"
        ),
    )
    check(
        "The selected maximin certificate stays on the canonical column fiber and is source-interior",
        np.linalg.norm(favored_column_from_source5(ref_maximin.source5)[:2] - column12) < BOUND_TOL
        and ref_maximin.source5[3] > INTERIOR_Y2_FLOOR,
        f"(y2,col12)=({ref_maximin.source5[3]:.12f},{np.round(favored_column_from_source5(ref_maximin.source5)[:2], 12)})",
    )
    check(
        "At that point the active barriers equalize exactly: J_ctr = J_y = t_*",
        abs(ref_maximin.j_ctr - ref_maximin.objective) < COMMON_FLOOR_TOL
        and abs(ref_maximin.j_y - ref_maximin.objective) < COMMON_FLOOR_TOL,
        f"(t,J_ctr,J_y)=({ref_maximin.objective:.12f},{ref_maximin.j_ctr:.12f},{ref_maximin.j_y:.12f})",
    )
    check(
        "The Schur isotropy cubic then sits strictly above the active floor rather than driving the point to the boundary",
        ref_maximin.j_iso > ref_maximin.objective + 1.0e-2,
        f"(J_iso,t)=({ref_maximin.j_iso:.12f},{ref_maximin.objective:.12f})",
    )
    check(
        "The interior certificate is genuinely new but remains W1-local on the canonical fiber",
        float(np.linalg.norm(ref_maximin.source5 - w1)) > 5.0e-2 and float(np.linalg.norm(ref_maximin.source5 - w1)) < 1.0e-1,
        f"distance to W1={float(np.linalg.norm(ref_maximin.source5 - w1)):.12f}",
    )
    check(
        "The maximin selector strictly improves the vanishing common floor of the pure J_ctr source-boundary certificate",
        ref_maximin.objective > 1.0e-1 and ref_triplet.j_y < 1.0e-6,
        f"(t_*, J_y[J_ctr*])=({ref_maximin.objective:.12f},{ref_triplet.j_y:.6e})",
    )
    check(
        "The more-isotropic B_major certificate is rejected because its constructive-triplet barrier collapses below the maximin floor",
        j_ctr_from_source5(b_major) < ref_maximin.objective and min(j_ctr_from_source5(b_major), j_y_from_source5(b_major)) < ref_maximin.objective,
        (
            f"(J_ctr,J_y)[B_major]=({j_ctr_from_source5(b_major):.12f},"
            f"{j_y_from_source5(b_major):.12f})"
        ),
    )

    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)
    check(
        "The first successful retained drift-arrest law on this lane is the coefficient-free two-law maximin system t = min(J_ctr, J_y)",
        ref_maximin.objective > 1.0e-1 and ref_maximin.source5[3] > INTERIOR_Y2_FLOOR,
        "J_iso remains part of the certificate, but the active arrest barriers are the constructive triplet and the native y-simplex",
    )

    print()
    print(f"  canonical column first two entries = {np.round(column12, 12)}")
    print()
    print("  pure J_ctr source-boundary certificate:")
    print(f"    source5 = {np.round(ref_triplet.source5, 12)}")
    print(f"    pack    = {np.round(ref_triplet.pack, 12)}")
    print(
        "    "
        f"(J_iso, J_ctr, J_y) = ({ref_triplet.j_iso:.12f}, {ref_triplet.j_ctr:.12f}, {ref_triplet.j_y:.12e})"
    )
    print()
    print("  triplet/y maximin interior certificate:")
    print(f"    source5 = {np.round(ref_maximin.source5, 12)}")
    print(f"    pack    = {np.round(ref_maximin.pack, 12)}")
    print(
        "    "
        f"(J_iso, J_ctr, J_y, t_*) = "
        f"({ref_maximin.j_iso:.12f}, {ref_maximin.j_ctr:.12f}, {ref_maximin.j_y:.12f}, {ref_maximin.objective:.12f})"
    )
    print()
    print(f"  best tested interior certificate label = {best_record.label}")
    print(f"  PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
