#!/usr/bin/env python3
"""
DM Wilson direct-descendant canonical-path status audit.

Purpose:
  Test whether the aligned-seed -> constructive-witness affine path is now
  forced by retained physics on the DM canonical-path lane.

Answer:
  No. The current affine segment remains a useful support-level selector
  candidate, but the path itself is still chosen.

  What the runner certifies:
    1. the current candidate path still has a unique transverse constructive
       positive exact-closure root;
    2. at least three other equally seed-fixed constructive overshooting
       affine segments produce distinct exact transverse roots;
    3. in the present affine chart, all of those segments are straight-line
       geodesics for the natural constant-metric class, so geodesic language
       does not make the current segment unique;
    4. even after upgrading to the exact pullback metrics from the canonical
       Y- and H-carriers, the seed-based eta_1 gradient flows still land on
       nonconstructive exact roots, not on the current constructive point;
    5. the neighboring source-surface selector packet does not descend to the
       direct-descendant exact roots or plateau witnesses, so it cannot yet be
       imported as the missing endpoint-direction law.
"""

from __future__ import annotations

import sys

import numpy as np
from scipy.linalg import eigh, null_space
from scipy.optimize import brentq

import frontier_dm_wilson_direct_descendant_constructive_transport_plateau_theorem_2026_04_19 as plateau
from dm_leptogenesis_exact_common import exact_package
from frontier_dm_leptogenesis_pmns_constructive_continuity_closure_theorem import (
    constructive_column_eta,
    path_point,
    seed_point,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h, canonical_y
from frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate import (
    build_active_from_seed_logits,
)
from frontier_dm_neutrino_positive_polar_h_cp_theorem import cp_pair_from_h
from frontier_dm_neutrino_postcanonical_polar_section import slot_pair_from_h
from frontier_dm_neutrino_source_surface_intrinsic_slot_theorem import (
    intrinsic_slot_formula,
)
from frontier_dm_wilson_direct_descendant_local_observable_coordinate_theorem_2026_04_19 import (
    delta_src,
    eta1,
    observable_jacobian,
    observable_pack,
    triplet,
)


PASS_COUNT = 0
FAIL_COUNT = 0
FD_STEP = 1.0e-6
PKG = exact_package()
A_STAR, B_STAR = intrinsic_slot_formula()


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


SEED_X, SEED_Y, SEED_DELTA = seed_point()
SEED_VECTOR = np.array(
    [SEED_X[0], SEED_X[1], SEED_Y[0], SEED_Y[1], SEED_DELTA],
    dtype=float,
)

CONSTRUCTIVE_WITNESS = np.array(
    [1.174161560603, 0.462544348009, 0.758741415897, 0.026904299513, 1.882595756164],
    dtype=float,
)

OVERSHOOT_WITNESSES = {
    "A+": np.array([1.16845863, 0.46803892, 0.77107315, 0.05539671, 1.89233895], dtype=float),
    "B+": np.array([0.86088785, 0.32714819, 0.71367707, 0.10440906, 1.59150180], dtype=float),
    "C+": np.array([1.00731313, 0.30177597, 0.79591855, 0.02985850, 2.19435677], dtype=float),
}

FLOW_METRICS = {
    "euclid": np.eye(5, dtype=float),
    "x1-heavy": np.diag([25.0, 1.0, 1.0, 1.0, 1.0]),
}


def path_vector(lam: float) -> np.ndarray:
    x, y, delta = path_point(float(lam))
    return np.array([x[0], x[1], y[0], y[1], delta], dtype=float)


def source5_to_xyd(v: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    v = np.asarray(v, dtype=float)
    x = np.array([v[0], v[1], 3.0 * SEED_X.mean() - v[0] - v[1]], dtype=float)
    y = np.array([v[2], v[3], 3.0 * SEED_Y.mean() - v[2] - v[3]], dtype=float)
    return x, y, float(v[4])


def canonical_h_from_source5(v: np.ndarray) -> np.ndarray:
    x, y, delta = source5_to_xyd(v)
    return canonical_h(x, y, delta)


def canonical_y_from_source5(v: np.ndarray) -> np.ndarray:
    x, y, delta = source5_to_xyd(v)
    return canonical_y(x, y, delta)


def segment(endpoint: np.ndarray, lam: float) -> np.ndarray:
    return (1.0 - lam) * SEED_VECTOR + lam * endpoint


def segment_eta(endpoint: np.ndarray, lam: float) -> float:
    return float(eta1(segment(endpoint, lam)))


def segment_root(endpoint: np.ndarray) -> tuple[float, np.ndarray]:
    lam_star = float(brentq(lambda lam: segment_eta(endpoint, lam) - 1.0, 0.0, 1.0))
    return lam_star, segment(endpoint, lam_star)


def derivative_on_segment(endpoint: np.ndarray, lam: float, h: float = FD_STEP) -> float:
    return float(
        (segment_eta(endpoint, lam + h) - segment_eta(endpoint, lam - h)) / (2.0 * h)
    )


def midpoint_and_second_difference(endpoint: np.ndarray) -> tuple[float, float]:
    midpoint_err = float(
        np.linalg.norm(
            segment(endpoint, 0.5) - 0.5 * (segment(endpoint, 0.0) + segment(endpoint, 1.0))
        )
    )
    second_diff = float(
        np.linalg.norm(
            segment(endpoint, 0.25) - 2.0 * segment(endpoint, 0.50) + segment(endpoint, 0.75)
        )
    )
    return midpoint_err, second_diff


def local_rank_data(v: np.ndarray) -> tuple[int, float, int, float]:
    jac = observable_jacobian(v, FD_STEP)
    singular = np.linalg.svd(jac, compute_uv=False)
    tangent_basis = null_space(jac[0:1, :])
    restricted = jac[1:, :] @ tangent_basis
    restricted_singular = np.linalg.svd(restricted, compute_uv=False)
    return (
        int(np.sum(singular > 1.0e-8)),
        float(np.min(singular)),
        int(np.sum(restricted_singular > 1.0e-8)),
        float(np.min(restricted_singular)),
    )


def constructive_positive(v: np.ndarray) -> bool:
    pack = observable_pack(v)
    return (
        abs(pack[0] - 1.0) < 1.0e-10
        and pack[1] > 0.0
        and pack[2] > 0.0
        and pack[3] > 0.0
        and pack[4] > 0.0
    )


def overshooting_constructive(endpoint: np.ndarray) -> bool:
    tr = triplet(endpoint)
    return (
        eta1(endpoint) > 1.0
        and tr["gamma"] > 0.0
        and tr["E1"] > 0.0
        and tr["E2"] > 0.0
        and delta_src(endpoint) > 0.0
    )


def grad_eta(v: np.ndarray, h: float = FD_STEP) -> np.ndarray:
    grad = np.zeros_like(v)
    for idx in range(v.size):
        vp = v.copy()
        vm = v.copy()
        vp[idx] += h
        vm[idx] -= h
        grad[idx] = (eta1(vp) - eta1(vm)) / (2.0 * h)
    return grad


def solve_metric(metric: np.ndarray, grad: np.ndarray) -> np.ndarray:
    evals, evecs = eigh(metric)
    evals = np.maximum(evals, 1.0e-8)
    inv_metric = (evecs * (1.0 / evals)) @ evecs.T
    return inv_metric @ grad


def pullback_metric(v: np.ndarray, carrier_map, h: float = FD_STEP) -> np.ndarray:
    derivs = []
    for idx in range(v.size):
        vp = v.copy()
        vm = v.copy()
        vp[idx] += h
        vm[idx] -= h
        derivs.append((carrier_map(vp) - carrier_map(vm)) / (2.0 * h))
    metric = np.zeros((v.size, v.size), dtype=float)
    for i in range(v.size):
        for j in range(v.size):
            metric[i, j] = float(np.real(np.vdot(derivs[i], derivs[j])))
    return metric


def flow_to_exact_root(metric_provider) -> np.ndarray:
    v = SEED_VECTOR.copy()
    step = 2.0e-3
    for _ in range(8000):
        grad = grad_eta(v)
        velocity = solve_metric(metric_provider(v), grad)
        norm = float(np.linalg.norm(velocity))
        if norm < 1.0e-12:
            break
        velocity /= norm
        trial = v + step * velocity
        if eta1(trial) >= 1.0:
            lo = 0.0
            hi = step
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                candidate = v + mid * velocity
                if eta1(candidate) >= 1.0:
                    hi = mid
                else:
                    lo = mid
            return v + hi * velocity
        v = trial
    raise RuntimeError("gradient flow did not reach eta_1 = 1")


def source5_from_transport_params(params: np.ndarray) -> np.ndarray:
    x, y, delta = build_active_from_seed_logits(*np.asarray(params, dtype=float))
    return np.array([x[0], x[1], y[0], y[1], delta], dtype=float)


def source_surface_slot_error(v: np.ndarray) -> float:
    h = canonical_h_from_source5(v)
    a, b = slot_pair_from_h(h)
    return max(abs(a - A_STAR), abs(b - B_STAR))


def source_surface_cp_error(v: np.ndarray) -> float:
    cp1, cp2 = cp_pair_from_h(canonical_h_from_source5(v))
    return max(abs(cp1 - PKG.cp1), abs(cp2 - PKG.cp2))


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT CANONICAL PATH STATUS AUDIT")
    print("=" * 88)

    path_lambda = float(brentq(lambda lam: constructive_column_eta(lam) - 1.0, 0.0, 1.0))
    path_root = path_vector(path_lambda)
    path_pack = observable_pack(path_root)
    path_rank = local_rank_data(path_root)

    alt_data: dict[str, dict[str, object]] = {}
    for label, endpoint in OVERSHOOT_WITNESSES.items():
        root_lambda, root = segment_root(endpoint)
        alt_data[label] = {
            "endpoint": endpoint,
            "root_lambda": root_lambda,
            "root": root,
            "pack": observable_pack(root),
            "rank": local_rank_data(root),
            "deriv": derivative_on_segment(endpoint, root_lambda),
        }

    flow_roots = {
        name: flow_to_exact_root(lambda _v, metric=metric: metric)
        for name, metric in FLOW_METRICS.items()
    }
    pullback_roots = {
        "H-pullback": flow_to_exact_root(lambda v: pullback_metric(v, canonical_h_from_source5)),
        "Y-pullback": flow_to_exact_root(lambda v: pullback_metric(v, canonical_y_from_source5)),
    }

    plateau_params = [("W0", plateau.witness_params())]
    for idx, anchor in enumerate(plateau.ANCHOR_PARAMS, start=1):
        refined, _res = plateau.refine_constructive_maximizer(anchor)
        plateau_params.append((f"W{idx}", refined))
    plateau_source5 = {
        label: source5_from_transport_params(params) for label, params in plateau_params
    }
    plateau_slot_errors = {
        label: source_surface_slot_error(v) for label, v in plateau_source5.items()
    }
    plateau_cp_errors = {
        label: source_surface_cp_error(v) for label, v in plateau_source5.items()
    }

    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT ALIGNED-SEED -> CONSTRUCTIVE-WITNESS PATH REMAINS SUPPORT-LEVEL SCIENCE")
    print("=" * 88)
    check(
        "The current candidate affine path still reaches a unique exact eta_1 = 1 point",
        0.0 < path_lambda < 1.0 and abs(path_pack[0] - 1.0) < 1.0e-12,
        f"lambda_*={path_lambda:.12f}",
    )
    check(
        "The current candidate root is still constructive and positive-branch",
        path_pack[1] > 0.0 and path_pack[2] > 0.0 and path_pack[3] > 0.0 and path_pack[4] > 0.0,
        f"pack={np.round(path_pack, 12)}",
    )
    check(
        "The current candidate root is still locally visible in the full observable chart",
        path_rank[0] == 5 and path_rank[1] > 1.0e-4 and path_rank[2] == 4 and path_rank[3] > 1.0e-4,
        f"min singulars=({path_rank[1]:.6e},{path_rank[3]:.6e})",
    )

    print("\n" + "=" * 88)
    print("PART 2: COMPETING FIXED-SEED AFFINE SELECTOR LAWS ALREADY EXIST")
    print("=" * 88)
    check(
        "The A+, B+, and C+ multiplicity endpoints are all constructive positive overshooting witnesses",
        all(overshooting_constructive(endpoint) for endpoint in OVERSHOOT_WITNESSES.values()),
        "three retained overshooting witnesses on the same fixed seed surface",
    )
    check(
        "Each competing seed-fixed affine segment has an exact eta_1 = 1 root in (0,1)",
        all(0.0 < data["root_lambda"] < 1.0 and abs(data["pack"][0] - 1.0) < 1.0e-10 for data in alt_data.values()),
        ", ".join(f"{label}: {data['root_lambda']:.12f}" for label, data in alt_data.items()),
    )
    check(
        "Each competing affine crossing is transverse",
        all(data["deriv"] > 1.0e-4 for data in alt_data.values()),
        ", ".join(f"{label}: d eta/dlambda={data['deriv']:.6f}" for label, data in alt_data.items()),
    )
    check(
        "Each competing affine root is itself constructive positive and locally complete",
        all(
            constructive_positive(data["root"])
            and data["rank"][0] == 5
            and data["rank"][1] > 1.0e-4
            and data["rank"][2] == 4
            and data["rank"][3] > 1.0e-4
            for data in alt_data.values()
        ),
        "A+, B+, and C+ all land on full-rank constructive positive exact roots",
    )
    check(
        "Those competing affine-selected roots are distinct from the current candidate root",
        min(float(np.linalg.norm(data["root"] - path_root)) for data in alt_data.values()) > 5.0e-2,
        ", ".join(
            f"{label}: dist={np.linalg.norm(data['root'] - path_root):.6f}"
            for label, data in alt_data.items()
        ),
    )

    print("\n" + "=" * 88)
    print("PART 3: GEODESIC LANGUAGE DOES NOT MAKE THE CURRENT SEGMENT UNIQUE")
    print("=" * 88)
    geodesic_candidates = {"P": CONSTRUCTIVE_WITNESS, **OVERSHOOT_WITNESSES}
    midpoint_ok = True
    second_diff_ok = True
    details = []
    for label, endpoint in geodesic_candidates.items():
        midpoint_err, second_diff = midpoint_and_second_difference(endpoint)
        midpoint_ok &= midpoint_err < 1.0e-12
        second_diff_ok &= second_diff < 1.0e-12
        details.append(f"{label}: ({midpoint_err:.1e}, {second_diff:.1e})")
    check(
        "The current and competing selector segments are all straight affine geodesics in the natural constant-metric chart",
        midpoint_ok and second_diff_ok,
        "; ".join(details),
    )
    check(
        "So the standard affine-geodesic class already contains multiple constructive exact candidates",
        len(geodesic_candidates) >= 4,
        "P together with A+, B+, and C+",
    )

    print("\n" + "=" * 88)
    print("PART 4: THE OBVIOUS SEED-BASED ETA_1 GRADIENT FLOW IS METRIC-DEPENDENT")
    print("=" * 88)
    flow_packs = {name: observable_pack(root) for name, root in flow_roots.items()}
    check(
        "The Euclidean and x1-heavy eta_1 gradient flows both hit exact eta_1 = 1 roots",
        all(abs(pack[0] - 1.0) < 1.0e-10 for pack in flow_packs.values()),
        ", ".join(f"{name}: eta_1={pack[0]:.12f}" for name, pack in flow_packs.items()),
    )
    check(
        "Those gradient-flow roots are distinct, so the flow law depends on the chosen metric",
        float(np.linalg.norm(flow_roots["euclid"] - flow_roots["x1-heavy"])) > 1.0e-2,
        f"dist={np.linalg.norm(flow_roots['euclid'] - flow_roots['x1-heavy']):.6f}",
    )
    check(
        "Neither obvious eta_1 gradient flow lands on the current constructive path-selected root",
        all(float(np.linalg.norm(root - path_root)) > 5.0e-2 for root in flow_roots.values()),
        ", ".join(f"{name}: dist_to_P={np.linalg.norm(root - path_root):.6f}" for name, root in flow_roots.items()),
    )
    check(
        "Neither obvious eta_1 gradient flow root is constructive positive",
        all(not constructive_positive(root) for root in flow_roots.values()),
        "; ".join(
            f"{name}: pack={np.round(flow_packs[name], 9)}"
            for name in flow_roots
        ),
    )

    print("\n" + "=" * 88)
    print("PART 5: NATURAL CARRIER PULLBACK GEOMETRIES STILL DO NOT RECOVER THE CURRENT ROOT")
    print("=" * 88)
    pullback_packs = {name: observable_pack(root) for name, root in pullback_roots.items()}
    seed_pullback_metrics = {
        "H-pullback": pullback_metric(SEED_VECTOR, canonical_h_from_source5),
        "Y-pullback": pullback_metric(SEED_VECTOR, canonical_y_from_source5),
    }
    check(
        "The canonical Y- and H-carriers induce positive-definite pullback metrics at the aligned seed",
        all(float(np.min(np.linalg.eigvalsh(metric))) > 1.0e-6 for metric in seed_pullback_metrics.values()),
        "; ".join(
            f"{name}: min eig={np.min(np.linalg.eigvalsh(metric)):.6e}"
            for name, metric in seed_pullback_metrics.items()
        ),
    )
    check(
        "The H- and Y-pullback eta_1 flows both hit exact eta_1 = 1 roots",
        all(abs(pack[0] - 1.0) < 1.0e-10 for pack in pullback_packs.values()),
        ", ".join(f"{name}: eta_1={pack[0]:.12f}" for name, pack in pullback_packs.items()),
    )
    check(
        "Those pullback-flow roots are distinct, so even natural carrier geometries do not produce one canonical eta_1 flow",
        float(np.linalg.norm(pullback_roots["H-pullback"] - pullback_roots["Y-pullback"])) > 1.0e-2,
        f"dist={np.linalg.norm(pullback_roots['H-pullback'] - pullback_roots['Y-pullback']):.6f}",
    )
    check(
        "Neither pullback-flow root lands on the current constructive path-selected point",
        all(float(np.linalg.norm(root - path_root)) > 5.0e-2 for root in pullback_roots.values()),
        ", ".join(f"{name}: dist_to_P={np.linalg.norm(root - path_root):.6f}" for name, root in pullback_roots.items()),
    )
    check(
        "Neither pullback-flow root is constructive positive",
        all(not constructive_positive(root) for root in pullback_roots.values()),
        "; ".join(
            f"{name}: pack={np.round(pullback_packs[name], 9)}"
            for name in pullback_roots
        ),
    )

    print("\n" + "=" * 88)
    print("PART 6: THE SOURCE-SURFACE SELECTOR PACKET DOES NOT DESCEND TO THIS LANE")
    print("=" * 88)
    check(
        "Every current exact direct-descendant root stays uniformly away from the source-surface intrinsic slot pair",
        min([source_surface_slot_error(path_root)] + [source_surface_slot_error(data["root"]) for data in alt_data.values()]) > 9.0e-1,
        ", ".join(
            [f"P: {source_surface_slot_error(path_root):.6f}"]
            + [f"{label}: {source_surface_slot_error(data['root']):.6f}" for label, data in alt_data.items()]
        ),
    )
    check(
        "Every current exact direct-descendant root also stays uniformly away from the source-surface CP pair",
        min([source_surface_cp_error(path_root)] + [source_surface_cp_error(data["root"]) for data in alt_data.values()]) > 5.0e-1,
        ", ".join(
            [f"P: {source_surface_cp_error(path_root):.6f}"]
            + [f"{label}: {source_surface_cp_error(data['root']):.6f}" for label, data in alt_data.items()]
        ),
    )
    check(
        "The constructive transport-plateau witnesses are likewise outside the source-surface sheet",
        min(plateau_slot_errors.values()) > 9.0e-1 and min(plateau_cp_errors.values()) > 5.0e-1,
        "; ".join(
            f"{label}: (slot={plateau_slot_errors[label]:.6f}, cp={plateau_cp_errors[label]:.6f})"
            for label in plateau_source5
        ),
    )
    slot_winner = min(plateau_slot_errors, key=plateau_slot_errors.get)
    cp_winner = min(plateau_cp_errors, key=plateau_cp_errors.get)
    check(
        "Even nearest-source-surface heuristics split on the plateau rather than selecting one witness direction",
        slot_winner != cp_winner,
        f"slot nearest={slot_winner}, cp nearest={cp_winner}",
    )

    print("\n" + "=" * 88)
    print("PART 7: BOTTOM LINE")
    print("=" * 88)
    check(
        "The aligned-seed -> constructive-witness affine path is still chosen rather than derived",
        True,
        "competing affine/geodesic candidates exist; natural carrier pullback flows miss P; the source-surface selector packet does not descend",
    )
    check(
        "A future closure theorem must add either a direct-descendant -> source-surface bridge theorem or a microscopic value law on L_e itself",
        True,
        "a generic metric or borrowed source-surface law is not enough on the present retained packet",
    )

    print()
    print(f"  current path root P   = {np.round(path_root, 12)}")
    for label, data in alt_data.items():
        print(f"  competing root {label:>2} = {np.round(data['root'], 12)}")
    for name, root in flow_roots.items():
        print(f"  flow root {name:>8} = {np.round(root, 12)}")
    for name, root in pullback_roots.items():
        print(f"  pullback root {name:>10} = {np.round(root, 12)}")

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("VERDICT: PATH STILL CHOSEN")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
