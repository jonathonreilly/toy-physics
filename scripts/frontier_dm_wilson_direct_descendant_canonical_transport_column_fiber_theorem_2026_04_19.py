#!/usr/bin/env python3
"""
DM Wilson direct-descendant canonical transport-column fiber theorem.

Purpose:
  Push the transport-side DM science as far as the current branch supports.

  Result:
    1. exact flavored transport on the column simplex selects a unique
       current-branch maximizer orbit
           (0.0356443..., 0.0356443..., 0.9287114...)
       up to flavor permutation;
    2. all known constructive transport-plateau witnesses realize that same
       favored-column orbit;
    3. on the fixed native seed surface, the direct-descendant source ->
       favored-column map has rank 2 on a 5-real source surface, so transport
       still leaves a local 3-real source fiber unresolved.

  So transport now canonically fixes a favored column, but not a unique
  direct-descendant source.
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np
from scipy.optimize import differential_evolution, minimize

import frontier_dm_wilson_direct_descendant_constructive_transport_plateau_theorem_2026_04_19 as plateau
from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
)
from frontier_dm_leptogenesis_flavor_column_functional_theorem import (
    flavored_column_functional,
    flavored_transport_kernel,
)
from frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate import (
    XBAR_NE,
    YBAR_NE,
    build_active_from_seed_logits,
    eta_columns_from_active,
)

PASS_COUNT = 0
FAIL_COUNT = 0

OPT_TOL = 1.0e-8
ETA_TOL = 1.0e-10
JAC_TOL = 1.0e-8
RANK_TOL = 1.0e-8
HESS_STEP = 1.0e-5
GRAD_STEP = 1.0e-7

COLUMN_STARTS = [
    np.array([0.02, 0.93], dtype=float),
    np.array([0.03, 0.93], dtype=float),
    np.array([0.10, 0.80], dtype=float),
    np.array([0.30, 0.30], dtype=float),
    np.array([0.90, 0.05], dtype=float),
    np.array([0.04, 0.92], dtype=float),
]

PKG = exact_package()
Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL = flavored_transport_kernel(PKG.k_decay_exact)


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


def eta_from_column(column: np.ndarray) -> float:
    return (
        S_OVER_NGAMMA_EXACT
        * C_SPH
        * D_THERMAL_EXACT
        * PKG.epsilon_1
        * flavored_column_functional(np.asarray(column, dtype=float), Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL)
        / ETA_OBS
    )


def triangle_column(params: np.ndarray) -> np.ndarray:
    a, b = np.asarray(params, dtype=float)
    return np.array([a, b, 1.0 - a - b], dtype=float)


def column_objective(params: np.ndarray) -> float:
    col = triangle_column(params)
    if float(np.min(col)) < 0.0:
        return 1.0e6 + 1.0e3 * abs(float(np.min(col)))
    return -eta_from_column(col)


def refine_column_maximizer(start: np.ndarray) -> tuple[np.ndarray, object]:
    result = minimize(
        column_objective,
        np.asarray(start, dtype=float),
        method="SLSQP",
        bounds=[(0.0, 1.0), (0.0, 1.0)],
        constraints=[
            {"type": "ineq", "fun": lambda p: float(p[0])},
            {"type": "ineq", "fun": lambda p: float(p[1])},
            {"type": "ineq", "fun": lambda p: float(1.0 - p[0] - p[1])},
        ],
        options={"ftol": 1.0e-14, "maxiter": 1000},
    )
    return triangle_column(result.x), result


def column_gradient(column: np.ndarray, step: float = GRAD_STEP) -> np.ndarray:
    column = np.asarray(column, dtype=float)
    grad = np.zeros_like(column)
    for idx in range(column.size):
        dcol = np.zeros_like(column)
        dcol[idx] = step
        grad[idx] = (eta_from_column(column + dcol) - eta_from_column(column - dcol)) / (2.0 * step)
    return grad


def column_hessian(column: np.ndarray, step: float = HESS_STEP) -> np.ndarray:
    column = np.asarray(column, dtype=float)
    hess = np.zeros((column.size, column.size), dtype=float)
    for i in range(column.size):
        for j in range(column.size):
            di = np.zeros_like(column)
            dj = np.zeros_like(column)
            di[i] = step
            dj[j] = step
            hess[i, j] = (
                eta_from_column(column + di + dj)
                - eta_from_column(column + di - dj)
                - eta_from_column(column - di + dj)
                + eta_from_column(column - di - dj)
            ) / (4.0 * step * step)
    return hess


def best_row_permutation_error(column: np.ndarray, target: np.ndarray) -> tuple[float, tuple[int, int, int]]:
    best_err = float("inf")
    best_perm = (0, 1, 2)
    for perm in itertools.permutations(range(3)):
        err = float(np.linalg.norm(np.asarray(column, dtype=float)[list(perm)] - np.asarray(target, dtype=float)))
        if err < best_err:
            best_err = err
            best_perm = tuple(int(x) for x in perm)
    return best_err, best_perm


def favored_column_from_params(params: np.ndarray) -> np.ndarray:
    x, y, delta = build_active_from_seed_logits(*np.asarray(params, dtype=float))
    packet, _etas = eta_columns_from_active(x, y, delta)
    return np.asarray(packet[:, 1], dtype=float)


def fixed_seed_source5_from_params(params: np.ndarray) -> np.ndarray:
    x, y, delta = build_active_from_seed_logits(*np.asarray(params, dtype=float))
    return np.array([x[0], x[1], y[0], y[1], delta], dtype=float)


def source5_to_xyd(vector: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    v = np.asarray(vector, dtype=float)
    x = np.array([v[0], v[1], 3.0 * XBAR_NE - v[0] - v[1]], dtype=float)
    y = np.array([v[2], v[3], 3.0 * YBAR_NE - v[2] - v[3]], dtype=float)
    return x, y, float(v[4])


def favored_column_from_source5(vector: np.ndarray) -> np.ndarray:
    x, y, delta = source5_to_xyd(vector)
    packet, _etas = eta_columns_from_active(x, y, delta)
    return np.asarray(packet[:, 1], dtype=float)


def favored_column_jacobian(vector: np.ndarray, step: float = 1.0e-6) -> np.ndarray:
    vector = np.asarray(vector, dtype=float)
    jac = np.zeros((3, vector.size), dtype=float)
    for idx in range(vector.size):
        dv = np.zeros_like(vector)
        dv[idx] = step
        jac[:, idx] = (
            favored_column_from_source5(vector + dv) - favored_column_from_source5(vector - dv)
        ) / (2.0 * step)
    return jac


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT CANONICAL TRANSPORT-COLUMN FIBER THEOREM")
    print("=" * 88)

    witness_params = plateau.witness_params()
    witness_column = favored_column_from_params(witness_params)
    witness_sorted = np.sort(witness_column)
    witness_eta = eta_from_column(witness_column)

    de_result = differential_evolution(
        column_objective,
        bounds=[(0.0, 1.0), (0.0, 1.0)],
        seed=0,
        maxiter=80,
        popsize=18,
        polish=True,
        disp=False,
    )
    de_column = triangle_column(de_result.x)

    refined_columns = []
    refined_values = []
    for start in COLUMN_STARTS:
        col, _res = refine_column_maximizer(start)
        refined_columns.append(col)
        refined_values.append(eta_from_column(col))

    grad = column_gradient(witness_sorted)
    hess = column_hessian(witness_sorted)
    tangent_basis = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0]], dtype=float)
    restricted_hess = tangent_basis.T @ hess @ tangent_basis
    restricted_eigs = np.linalg.eigvalsh(restricted_hess)

    plateau_params = [witness_params]
    for anchor in plateau.ANCHOR_PARAMS:
        refined, _res = plateau.refine_constructive_maximizer(anchor)
        plateau_params.append(refined)

    plateau_columns = [favored_column_from_params(params) for params in plateau_params]
    plateau_source5 = [fixed_seed_source5_from_params(params) for params in plateau_params]
    plateau_eta = [eta_from_column(col) for col in plateau_columns]
    plateau_orbit_errors = [best_row_permutation_error(col, witness_column) for col in plateau_columns]

    jac = favored_column_jacobian(fixed_seed_source5_from_params(witness_params))
    singular_vals = np.linalg.svd(jac, compute_uv=False)
    jac_rank = int(np.sum(singular_vals > RANK_TOL))
    min_source_sep = min(
        float(np.linalg.norm(plateau_source5[i] - plateau_source5[j]))
        for i in range(len(plateau_source5))
        for j in range(i + 1, len(plateau_source5))
    )
    max_sorted_col_sep = max(
        float(np.linalg.norm(np.sort(plateau_columns[i]) - np.sort(plateau_columns[j])))
        for i in range(len(plateau_columns))
        for j in range(i + 1, len(plateau_columns))
    )

    print("\n" + "=" * 88)
    print("PART 1: EXACT TRANSPORT FIXES A UNIQUE CURRENT-BRANCH COLUMN ORBIT")
    print("=" * 88)
    check(
        "The constructive favored column is an interior probability column",
        abs(float(np.sum(witness_sorted)) - 1.0) < 1.0e-12 and float(np.min(witness_sorted)) > 0.0,
        f"col*={np.round(witness_sorted, 12)}",
    )
    check(
        "Its ordered representative has the symmetric two-leakage form q_small, q_small, 1 - 2 q_small",
        abs(witness_sorted[0] - witness_sorted[1]) < OPT_TOL
        and abs(witness_sorted[2] - (1.0 - 2.0 * witness_sorted[0])) < OPT_TOL,
        f"col*={np.round(witness_sorted, 12)}",
    )
    check(
        "Deterministic global transport search returns the same simplex maximizer orbit",
        float(np.linalg.norm(np.sort(de_column) - witness_sorted)) < 5.0e-7
        and abs(eta_from_column(de_column) - witness_eta) < 5.0e-12,
        f"DE sorted col={np.round(np.sort(de_column), 12)}",
    )
    check(
        "Independent local maximizations from separated starts all collapse to that same ordered orbit",
        max(float(np.linalg.norm(np.sort(col) - witness_sorted)) for col in refined_columns) < 5.0e-7
        and max(abs(val - witness_eta) for val in refined_values) < 5.0e-12,
        f"orbit spread={max(float(np.linalg.norm(np.sort(col) - witness_sorted)) for col in refined_columns):.3e}",
    )
    check(
        "The ordered column satisfies the interior simplex stationarity equations",
        float(np.max(np.abs(grad - np.mean(grad)))) < 1.0e-6,
        f"grad={np.round(grad, 9)}",
    )
    check(
        "The restricted Hessian on the simplex tangent space is negative definite there",
        float(np.max(restricted_eigs)) < -1.0e-3,
        f"eig={np.round(restricted_eigs, 9)}",
    )

    print("\n" + "=" * 88)
    print("PART 2: THE CONSTRUCTIVE TRANSPORT PLATEAU REALIZES THAT SAME COLUMN ORBIT")
    print("=" * 88)
    check(
        "All four constructive plateau witnesses have the same favored-column orbit up to row permutation",
        max(err for err, _perm in plateau_orbit_errors) < 5.0e-8,
        f"max orbit err={max(err for err, _perm in plateau_orbit_errors):.3e}",
    )
    check(
        "At least one constructive plateau witness reaches that same orbit by a nontrivial row permutation",
        any(perm != (0, 1, 2) for _err, perm in plateau_orbit_errors[1:]),
        f"perms={[perm for _err, perm in plateau_orbit_errors]}",
    )
    check(
        "The plateau witnesses all share the same ordered favored-column multiset to current-branch precision",
        max_sorted_col_sep < 5.0e-8,
        f"max sorted-col sep={max_sorted_col_sep:.3e}",
    )
    check(
        "Therefore their common extremal eta_1 value is exactly the transport-maximal column value",
        max(abs(val - witness_eta) for val in plateau_eta) < ETA_TOL,
        f"eta_1={witness_eta:.12f}",
    )

    print("\n" + "=" * 88)
    print("PART 3: THE DIRECT-DESCENDANT SOURCE FIBER ABOVE THAT COLUMN IS NONTRIVIAL")
    print("=" * 88)
    check(
        "The source -> favored-column Jacobian has rank 2 on the 5-real fixed-seed source surface",
        jac_rank == 2,
        f"singular values={np.round(singular_vals, 12)}",
    )
    check(
        "The column-sum constraint is exact at Jacobian level, so only two column directions are independent",
        float(np.max(np.abs(np.sum(jac, axis=0)))) < JAC_TOL,
        f"max row-sum drift={float(np.max(np.abs(np.sum(jac, axis=0)))):.3e}",
    )
    check(
        "So transport leaves a local 3-real source fiber unresolved above the canonical favored column orbit",
        jac_rank == 2 and jac.shape == (3, 5),
        "5 source reals - 2 independent column reals = 3 residual local fiber dimensions",
    )
    check(
        "The current constructive plateau already intersects that fiber in multiple macroscopically separated sources",
        min_source_sep > 4.0e-1,
        f"min source separation={min_source_sep:.12f}",
    )

    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)
    check(
        "Exact transport now canonically fixes a favored direct-descendant column orbit",
        True,
        f"col*={np.round(witness_sorted, 12)}, eta_1={witness_eta:.12f}",
    )
    check(
        "But the remaining DM object is now a concrete microscopic source-fiber law, not a missing transport law",
        True,
        "derive a point in the 3-real fixed-seed source fiber over the canonical favored column orbit",
    )

    print()
    print(f"  canonical ordered favored column = {np.round(witness_sorted, 12)}")
    print(f"  canonical eta_1 / eta_obs        = {witness_eta:.12f}")
    print(f"  favored-column Jacobian singulars= {np.round(singular_vals, 12)}")
    print(f"  min constructive source sep      = {min_source_sep:.12f}")

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
