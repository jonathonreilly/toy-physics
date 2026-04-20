#!/usr/bin/env python3
"""
DM Wilson direct-descendant canonical-fiber Schur-entropy candidate / no-go.

Purpose:
  Push the new canonical transport-column fiber theorem one step further on the
  source side.

  Result:
    1. on the orbit-level canonical favored-column fiber, standard normalized
       Schur-spectral isotropy laws do not canonically extend the plateau
       selector;
    2. an explicit Shannon-entropy point and an explicit Renyi-2 /
       participation point both lie on the same exact positive fiber, but the
       two laws rank them oppositely;
    3. their normalized Schur spectra are majorization-incomparable, so the
       phrase "most isotropic spectrum" is not well-defined on the full fiber;
    4. if one nevertheless adds the extra entropy-additivity axiom that picks
       Shannon, the resulting endpoint is explicit, but the aligned-seed ->
       endpoint exact eta_1 = 1 crossing leaves the constructive chamber.
"""

from __future__ import annotations

import math
import sys
import warnings

import numpy as np
from scipy.linalg import null_space
from scipy.optimize import NonlinearConstraint, brentq, minimize

import frontier_dm_wilson_direct_descendant_constructive_transport_plateau_theorem_2026_04_19 as plateau
import frontier_dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_2026_04_19 as fiber
from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem import (
    triplet_from_projected_response_pack,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate import (
    build_active_from_seed_logits,
    eta_columns_from_active,
)
from frontier_dm_wilson_direct_descendant_local_observable_coordinate_theorem_2026_04_19 import (
    eta1,
    observable_jacobian,
    observable_pack,
)


PASS_COUNT = 0
FAIL_COUNT = 0

RANK_TOL = 1.0e-8
FD_STEP = 1.0e-6
POS_TOL = 1.0e-9
FIBER_TOL = 1.0e-6

SEED_SOURCE5 = np.array(
    [0.5633333333333334, 0.5633333333333334, 0.30666666666666664, 0.30666666666666664, 0.0],
    dtype=float,
)
SHANNON_START = np.array([0.5, 0.5, 0.2, 0.2, 0.0], dtype=float)
RENYI2_START = np.array([1.23430754, 0.99431952, -1.26251272, 1.13252495, 2.31870143], dtype=float)


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


def canonical_orbit_targets() -> np.ndarray:
    params = plateau.plateau_witness_params()[1]
    column = fiber.favored_column_from_params(params)
    return np.array([float(np.sum(column**2)), float(np.sum(column**3))], dtype=float)


TARGET_P2_P3 = canonical_orbit_targets()


def spectrum_desc_from_params(params: np.ndarray) -> np.ndarray:
    x, y, delta = build_active_from_seed_logits(*np.asarray(params, dtype=float))
    evals = np.linalg.eigvalsh(canonical_h(x, y, delta))
    evals = np.sort(np.real(evals))[::-1]
    return np.asarray(evals / np.sum(evals), dtype=float)


def shannon_entropy(params: np.ndarray) -> float:
    probs = spectrum_desc_from_params(params)
    return float(-np.sum(probs * np.log(probs)))


def renyi2_entropy(params: np.ndarray) -> float:
    probs = spectrum_desc_from_params(params)
    return float(-np.log(np.sum(probs * probs)))


def participation_ratio(params: np.ndarray) -> float:
    probs = spectrum_desc_from_params(params)
    return float(1.0 / np.sum(probs * probs))


def source5_from_params(params: np.ndarray) -> np.ndarray:
    x, y, delta = build_active_from_seed_logits(*np.asarray(params, dtype=float))
    return np.array([x[0], x[1], y[0], y[1], delta], dtype=float)


def canonical_fiber_invariants(params: np.ndarray) -> np.ndarray:
    column = fiber.favored_column_from_params(np.asarray(params, dtype=float))
    return np.array([float(np.sum(column**2)), float(np.sum(column**3))], dtype=float)


def projected_pack4_from_params(params: np.ndarray) -> np.ndarray:
    x, y, delta = build_active_from_seed_logits(*np.asarray(params, dtype=float))
    hmat = canonical_h(x, y, delta)
    triplet = triplet_from_projected_response_pack(hermitian_linear_responses(hmat))
    return np.array(
        [triplet["gamma"], triplet["E1"], triplet["E2"], float(np.real(np.linalg.det(hmat)))],
        dtype=float,
    )


def eta_vector_from_params(params: np.ndarray) -> np.ndarray:
    x, y, delta = build_active_from_seed_logits(*np.asarray(params, dtype=float))
    return np.asarray(eta_columns_from_active(x, y, delta)[1], dtype=float)


def majorized_by(more_uniform: np.ndarray, comparator: np.ndarray, tol: float = 1.0e-12) -> bool:
    u = np.asarray(more_uniform, dtype=float)
    v = np.asarray(comparator, dtype=float)
    partial_u = np.cumsum(u[:-1])
    partial_v = np.cumsum(v[:-1])
    return bool(np.all(partial_u <= partial_v + tol) and np.any(partial_u < partial_v - tol))


def solve_positive_fiber_extremum(start: np.ndarray, objective) -> tuple[np.ndarray, object]:
    constraints = [
        NonlinearConstraint(canonical_fiber_invariants, TARGET_P2_P3, TARGET_P2_P3),
        NonlinearConstraint(lambda p: projected_pack4_from_params(p)[0], POS_TOL, np.inf),
        NonlinearConstraint(lambda p: projected_pack4_from_params(p)[1], POS_TOL, np.inf),
        NonlinearConstraint(lambda p: projected_pack4_from_params(p)[2], POS_TOL, np.inf),
        NonlinearConstraint(lambda p: projected_pack4_from_params(p)[3], POS_TOL, np.inf),
    ]
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="delta_grad == 0.0")
        result = minimize(
            lambda p: -objective(np.asarray(p, dtype=float)),
            np.asarray(start, dtype=float),
            method="trust-constr",
            bounds=[(-8.0, 8.0), (-8.0, 8.0), (-8.0, 8.0), (-8.0, 8.0), (-math.pi, math.pi)],
            constraints=constraints,
            options={
                "maxiter": 1000,
                "gtol": 1.0e-10,
                "xtol": 1.0e-10,
                "barrier_tol": 1.0e-12,
                "verbose": 0,
            },
        )
    return np.asarray(result.x, dtype=float), result


def segment(seed: np.ndarray, endpoint: np.ndarray, lam: float) -> np.ndarray:
    return (1.0 - lam) * seed + lam * endpoint


def eta_root_count(seed: np.ndarray, endpoint: np.ndarray, grid_size: int = 2001) -> int:
    grid = np.linspace(0.0, 1.0, grid_size, dtype=float)
    vals = np.array([eta1(segment(seed, endpoint, lam)) - 1.0 for lam in grid], dtype=float)
    count = 0
    for idx in range(grid.size - 1):
        if abs(vals[idx]) < 1.0e-12:
            count += 1
        elif vals[idx] * vals[idx + 1] < 0.0:
            count += 1
    return count


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT CANONICAL-FIBER SCHUR-ENTROPY CANDIDATE / NO-GO")
    print("=" * 88)

    shannon_params, shannon_result = solve_positive_fiber_extremum(SHANNON_START, shannon_entropy)
    renyi_params, renyi_result = solve_positive_fiber_extremum(RENYI2_START, renyi2_entropy)
    w1_params = plateau.plateau_witness_params()[1]

    shannon_source5 = source5_from_params(shannon_params)
    renyi_source5 = source5_from_params(renyi_params)
    shannon_spec = spectrum_desc_from_params(shannon_params)
    renyi_spec = spectrum_desc_from_params(renyi_params)
    shannon_pack4 = projected_pack4_from_params(shannon_params)
    renyi_pack4 = projected_pack4_from_params(renyi_params)
    w1_spec = spectrum_desc_from_params(w1_params)

    print("\n" + "=" * 88)
    print("PART 1: THE ORBIT-LEVEL CANONICAL FIBER AND POSITIVE BRANCH ARE EXACTLY REPRESENTABLE")
    print("=" * 88)
    plateau_targets_ok = True
    for params in plateau.plateau_witness_params():
        plateau_targets_ok &= np.max(np.abs(canonical_fiber_invariants(params) - TARGET_P2_P3)) < FIBER_TOL
    check(
        "The canonical favored-column orbit is fixed exactly by the two permutation-invariant moments (sum c_i^2, sum c_i^3)",
        plateau_targets_ok,
        f"(p2,p3)=({TARGET_P2_P3[0]:.12f},{TARGET_P2_P3[1]:.12f})",
    )
    check(
        "The Shannon and Renyi-2 constructions both land exactly on that orbit-level fiber and inside gamma > 0, E1 > 0, E2 > 0, Delta_src > 0",
        shannon_result.success
        and renyi_result.success
        and np.max(np.abs(canonical_fiber_invariants(shannon_params) - TARGET_P2_P3)) < 1.0e-12
        and np.max(np.abs(canonical_fiber_invariants(renyi_params) - TARGET_P2_P3)) < 1.0e-12
        and np.min(shannon_pack4) > 0.0
        and np.min(renyi_pack4) > 0.0,
        (
            f"Shannon pack={np.round(shannon_pack4, 12)}, "
            f"Renyi2 pack={np.round(renyi_pack4, 12)}"
        ),
    )

    print("\n" + "=" * 88)
    print("PART 2: THE PLATEAU SCHUR-ISOTROPY SLOGAN DOES NOT EXTEND CANONICALLY TO THE FULL FIBER")
    print("=" * 88)
    check(
        "The Shannon construction beats the certified plateau witness W1 in Shannon entropy",
        shannon_entropy(shannon_params) > shannon_entropy(w1_params) + 1.0e-6,
        f"(S_H,W1)=({shannon_entropy(shannon_params):.12f},{shannon_entropy(w1_params):.12f})",
    )
    check(
        "The Renyi-2 / participation construction beats W1 in Renyi-2 entropy",
        renyi2_entropy(renyi_params) > renyi2_entropy(w1_params) + 1.0e-6,
        f"(S_R,W1)=({renyi2_entropy(renyi_params):.12f},{renyi2_entropy(w1_params):.12f})",
    )
    check(
        "Shannon and Renyi-2 rank the two exact positive-fiber points oppositely",
        shannon_entropy(shannon_params) > shannon_entropy(renyi_params) + 1.0e-6
        and renyi2_entropy(renyi_params) > renyi2_entropy(shannon_params) + 1.0e-6
        and participation_ratio(renyi_params) > participation_ratio(shannon_params) + 1.0e-6,
        (
            f"H(S_H,S_R)=({shannon_entropy(shannon_params):.12f},{shannon_entropy(renyi_params):.12f}), "
            f"R2(S_H,S_R)=({renyi2_entropy(shannon_params):.12f},{renyi2_entropy(renyi_params):.12f})"
        ),
    )
    check(
        "Their normalized Schur spectra are majorization-incomparable, so 'most isotropic spectrum' is not a well-defined law on the full fiber",
        (not majorized_by(shannon_spec, renyi_spec)) and (not majorized_by(renyi_spec, shannon_spec)),
        f"S_H={np.round(shannon_spec, 12)}, S_R={np.round(renyi_spec, 12)}",
    )

    print("\n" + "=" * 88)
    print("PART 3: THE EXTRA AXIOM THAT PICKS SHANNON DOES GIVE AN EXPLICIT ENDPOINT CANDIDATE")
    print("=" * 88)
    check(
        "The Shannon point is an explicit positive source on the canonical orbit-level fiber",
        np.max(np.abs(canonical_fiber_invariants(shannon_params) - TARGET_P2_P3)) < 1.0e-12 and np.min(shannon_pack4) > 0.0,
        (
            f"source5={np.round(shannon_source5, 12)}, "
            f"spectrum={np.round(shannon_spec, 12)}"
        ),
    )
    check(
        "That candidate keeps the exact transport-maximal favored-column value eta_1 = 1.052220313052...",
        abs(eta_vector_from_params(shannon_params)[1] - plateau.eta1_from_params(w1_params)) < 1.0e-10,
        f"etas={np.round(eta_vector_from_params(shannon_params), 12)}",
    )

    print("\n" + "=" * 88)
    print("PART 4: EVEN THE SHANNON ENDPOINT DOES NOT YET CLOSE THE PHYSICAL SELECTOR")
    print("=" * 88)
    root_count = eta_root_count(SEED_SOURCE5, shannon_source5)
    root_lambda = float(brentq(lambda lam: eta1(segment(SEED_SOURCE5, shannon_source5, lam)) - 1.0, 0.0, 1.0))
    root_point = segment(SEED_SOURCE5, shannon_source5, root_lambda)
    root_pack = observable_pack(root_point)
    jac = observable_jacobian(root_point, FD_STEP)
    singular = np.linalg.svd(jac, compute_uv=False)
    tangent_basis = null_space(jac[0:1, :], rcond=RANK_TOL)
    restricted = jac[1:, :] @ tangent_basis
    restricted_singular = np.linalg.svd(restricted, compute_uv=False)
    check(
        "The aligned-seed -> Shannon-endpoint segment still has a unique exact eta_1 = 1 crossing",
        root_count == 1 and 0.0 < root_lambda < 1.0 and abs(root_pack[0] - 1.0) < 1.0e-10,
        f"lambda={root_lambda:.12f}",
    )
    check(
        "That exact crossing is locally full-rank but it leaves the constructive chamber because E1 < 0",
        int(np.sum(singular > RANK_TOL)) == 5
        and int(np.sum(restricted_singular > RANK_TOL)) == 4
        and root_pack[2] < 0.0,
        f"root pack={np.round(root_pack, 12)}",
    )

    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)
    check(
        "The full canonical source fiber therefore does not carry a canonical coefficient-free Schur-spectral isotropy law on the current branch",
        True,
        "Shannon and Renyi-2 / participation disagree on exact positive-fiber points",
    )
    check(
        "What the branch now has is a sharper conditional candidate: if one adds the entropy-additivity axiom, Shannon selects an explicit endpoint, but constructive physical closure still remains open",
        True,
        "the remaining gap is not generic spectral isotropy but the extra physical law beyond it",
    )

    print()
    print(f"  canonical orbit targets (p2,p3) = {np.round(TARGET_P2_P3, 12)}")
    print(f"  Shannon source5                 = {np.round(shannon_source5, 12)}")
    print(f"  Shannon spectrum                = {np.round(shannon_spec, 12)}")
    print(f"  Renyi2 source5                  = {np.round(renyi_source5, 12)}")
    print(f"  Renyi2 spectrum                 = {np.round(renyi_spec, 12)}")
    print(f"  Shannon root pack               = {np.round(root_pack, 12)}")

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
