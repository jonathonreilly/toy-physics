#!/usr/bin/env python3
"""Exact rank-one reduced junction operator on the star-supported source class.

Exact content:
  1. The reduced junction data attached to each star-support point-Green column
     are identical.
  2. Therefore the reduced junction operator from star-support source weights
     to reduced shell/exterior data has rank one.
  3. The operator factors exactly as
         J_red = v_red * (1,1,...,1)
     i.e. total charge functional followed by one fixed reduced junction vector.

Bounded content:
  4. On the current reduced gravity surface, the nonlinear shell law is no
     longer an unknown operator family. It is one exact reduced operator that
     still needs to be lifted to the full 4D closure.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


star = SourceFileLoader(
    "star_shell_projector",
    "/private/tmp/physics-review-active/scripts/frontier_star_shell_projector.py",
).load_module()
same_source = SourceFileLoader(
    "same_source_metric",
    "/private/tmp/physics-review-active/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    "/private/tmp/physics-review-active/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()
sew = SourceFileLoader(
    "sewing_shell",
    "/private/tmp/physics-review-active/scripts/frontier_sewing_shell_source.py",
).load_module()
rad = SourceFileLoader(
    "radial_shell",
    "/private/tmp/physics-review-active/scripts/frontier_radial_shell_matching_law.py",
).load_module()


ACTIVE_ORBITS = [
    (3, 2, 2),
    (3, 3, 0),
    (4, 1, 0),
    (4, 1, 1),
]
ANCHOR_ORBIT = (3, 3, 0)


def orbit_key(i: int, j: int, k: int, size: int) -> tuple[int, int, int]:
    center = (size - 1) // 2
    return tuple(sorted([abs(i - center), abs(j - center), abs(k - center)], reverse=True))


def radial_profile(source_grid: np.ndarray) -> list[float]:
    sigma_rad = rad.radial_average_shell(source_grid)
    total_charge = float(np.sum(sigma_rad))
    size = source_grid.shape[0]
    center = (size - 1) / 2.0
    groups: dict[int, list[tuple[int, int, int]]] = {}
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if abs(sigma_rad[i, j, k]) <= 1e-12:
                    continue
                d2 = int((i - center) ** 2 + (j - center) ** 2 + (k - center) ** 2)
                groups.setdefault(d2, []).append((i, j, k))
    vals = []
    for d2 in sorted(groups):
        shell_sum = float(np.sum([sigma_rad[p] for p in groups[d2]]))
        vals.append(shell_sum / total_charge)
    return vals


def shell_mean_rows(field: np.ndarray, cutoff: float = 5.0) -> list[float]:
    size = field.shape[0]
    center = (size - 1) / 2.0
    groups: dict[int, list[tuple[int, int, int]]] = {}
    for i in range(size):
        for j in range(size):
            for k in range(size):
                d2 = int((i - center) ** 2 + (j - center) ** 2 + (k - center) ** 2)
                groups.setdefault(d2, []).append((i, j, k))
    vals = []
    for d2 in sorted(groups):
        radius = float(np.sqrt(d2))
        if radius <= cutoff + 1e-12:
            continue
        cell_vals = np.array([field[p] for p in groups[d2]], dtype=float)
        vals.append(float(np.mean(cell_vals)))
    return vals


def reduced_vector(phi_grid: np.ndarray, shell_radius: float = 4.0) -> tuple[float, np.ndarray]:
    sigma = sew.full_neg_laplacian(sew.exterior_projector(phi_grid, shell_radius))
    sigma_rad = rad.radial_average_shell(sigma)
    delta_sigma = sigma - sigma_rad
    phi_shell = rad.solve_from_source(sigma)
    phi_aniso = rad.solve_from_source(delta_sigma)

    total_charge = float(np.sum(sigma))
    size = sigma.shape[0]
    orbit_sums: dict[tuple[int, int, int], float] = {}
    for i in range(size):
        for j in range(size):
            for k in range(size):
                key = orbit_key(i, j, k, size)
                orbit_sums.setdefault(key, 0.0)
                orbit_sums[key] += float(delta_sigma[i, j, k])

    vec = np.array(
        radial_profile(sigma)
        + [orbit_sums[k] / total_charge for k in ACTIVE_ORBITS]
        + [v / total_charge for v in shell_mean_rows(phi_shell)]
        + [v / total_charge for v in shell_mean_rows(phi_aniso)],
        dtype=float,
    )
    return total_charge, vec


def max_column_diff(mat: np.ndarray) -> float:
    ref = mat[:, [0]]
    return float(np.max(np.abs(mat - ref)))


def main() -> None:
    print("Exact rank-one reduced junction operator")
    print("=" * 72)

    columns, _, _ = star.build_point_green_columns(15)
    q_list = []
    vecs = []
    for col in columns:
        q, vec = reduced_vector(col)
        q_list.append(q)
        vecs.append(vec)
    Q_cols = np.array(q_list, dtype=float)
    J = np.column_stack(vecs)
    ref_vec = J[:, 0]
    ones = np.ones((1, J.shape[1]), dtype=float)
    J_ref = ref_vec[:, None] @ ones

    point_diff = max_column_diff(J)
    rank = int(np.linalg.matrix_rank(J, tol=1e-12))
    factor_err = float(np.max(np.abs(J - J_ref)))
    charge_err = float(np.max(np.abs(Q_cols - 1.0)))

    family_q_oh, family_vec_oh = reduced_vector(same_source.build_best_phi_grid())
    family_q_fr, family_vec_fr = reduced_vector(coarse.build_finite_rank_phi_grid())
    family_err = max(
        float(np.max(np.abs(family_vec_oh - ref_vec))),
        float(np.max(np.abs(family_vec_fr - ref_vec))),
    )

    print(f"max point-column reduced-junction difference = {point_diff:.3e}")
    print(f"reduced operator rank = {rank}")
    print(f"rank-one factorization error = {factor_err:.3e}")
    print(f"unit-charge column error = {charge_err:.3e}")
    print(f"family reduced-vector difference = {family_err:.3e}")

    record(
        "all seven star-support point-Green columns induce the same reduced junction vector",
        point_diff < 1e-12,
        f"max point-column difference = {point_diff:.3e}",
    )
    record(
        "the star-support reduced junction operator has rank one",
        rank == 1,
        f"rank = {rank}",
    )
    record(
        "the reduced junction operator factors as fixed vector times total-charge functional",
        factor_err < 1e-12 and charge_err < 1e-12,
        f"factorization error = {factor_err:.3e}, max |Q-1| = {charge_err:.3e}",
    )
    record(
        "the exact local O_h and finite-rank source families lie on the same reduced junction operator image",
        family_err < 1e-12,
        f"max family reduced-vector difference = {family_err:.3e}",
    )
    record(
        "on the current reduced gravity surface the sewing law is one exact reduced junction operator, not a family of unknown closures",
        factor_err < 1e-12 and family_err < 1e-12,
        f"rank = {rank}, factorization error = {factor_err:.3e}",
        status="BOUNDED",
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
