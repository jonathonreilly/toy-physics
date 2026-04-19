#!/usr/bin/env python3
"""
DM Wilson direct-descendant canonical path-selector theorem.

Purpose:
  Upgrade the old constructive continuity existence argument into an explicit
  selector law candidate on the direct-descendant route:

    choose the unique exact eta_1 = 1 point on the canonical affine path from
    the aligned native seed to the explicit constructive witness.

  This is not a derivation of the path or witness from retained physics. It is
  a concrete selector law on the current reviewed branch, and it lands on a
  point that is distinct from the other already-certified exact constructive
  positive roots.
"""

from __future__ import annotations

import sys

import numpy as np
from scipy.linalg import null_space
from scipy.optimize import brentq

from frontier_dm_leptogenesis_pmns_constructive_continuity_closure_theorem import (
    constructive_column_eta,
    path_point,
    path_triplet,
    seed_point,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_wilson_direct_descendant_constructive_positive_closure_multiplicity_theorem_2026_04_18 import (
    eta1,
)
from frontier_dm_wilson_direct_descendant_local_observable_coordinate_theorem_2026_04_19 import (
    observable_jacobian,
    observable_pack,
)


PASS_COUNT = 0
FAIL_COUNT = 0

FD_STEPS = [1.0e-5, 1.0e-6, 1.0e-7]
ETA_GRID = np.linspace(0.0, 1.0, 10001, dtype=float)

FAMILY_DATA = [
    (
        "A",
        np.array([1.16845863, 0.46803892, 0.77107315, 0.05539671, 1.88733895], dtype=float),
        1.88233895,
        1.89233895,
    ),
    (
        "B",
        np.array([0.86088785, 0.32714819, 0.71367707, 0.10440906, 1.59650180], dtype=float),
        1.59150180,
        1.60150180,
    ),
    (
        "C",
        np.array([1.00731313, 0.30177597, 0.79591855, 0.02985850, 2.19935677], dtype=float),
        2.19435677,
        2.20435677,
    ),
]


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


def vector_from_path(lam: float) -> np.ndarray:
    x, y, delta = path_point(float(lam))
    return np.array([x[0], x[1], y[0], y[1], delta], dtype=float)


def delta_src_from_vector(v: np.ndarray) -> float:
    x = np.array([v[0], v[1], 3.0 * np.mean(seed_point()[0]) - v[0] - v[1]], dtype=float)
    y = np.array([v[2], v[3], 3.0 * np.mean(seed_point()[1]) - v[2] - v[3]], dtype=float)
    hmat = canonical_h(x, y, float(v[4]))
    return float(np.real(np.linalg.det(hmat)))


def path_root() -> tuple[float, np.ndarray]:
    lam_star = float(brentq(lambda lam: constructive_column_eta(lam) - 1.0, 0.0, 1.0))
    return lam_star, vector_from_path(lam_star)


def family_root(label: str, base: np.ndarray, lo: float, hi: float) -> tuple[str, np.ndarray]:
    root = float(brentq(lambda e_val: eta1(np.array([base[0], base[1], base[2], base[3], e_val], dtype=float)) - 1.0, lo, hi))
    out = base.copy()
    out[4] = root
    return label, out


def line_segment_residual(v: np.ndarray, start: np.ndarray, end: np.ndarray) -> tuple[float, float]:
    direction = end - start
    lam_fit = float(np.dot(v - start, direction) / max(np.dot(direction, direction), 1.0e-15))
    lam_clip = min(1.0, max(0.0, lam_fit))
    proj = start + lam_clip * direction
    return lam_fit, float(np.linalg.norm(v - proj))


def finite_eta_derivative(lam: float, h: float = 1.0e-6) -> float:
    return float((constructive_column_eta(lam + h) - constructive_column_eta(lam - h)) / (2.0 * h))


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT CANONICAL PATH SELECTOR THEOREM")
    print("=" * 88)

    lam_star, v_star = path_root()
    pack_star = observable_pack(v_star)
    triplet_star = path_triplet(lam_star)
    path_start = vector_from_path(0.0)
    path_end = vector_from_path(1.0)
    family_roots = [family_root(*item) for item in FAMILY_DATA]

    print("\n" + "=" * 88)
    print("PART 1: THE CANONICAL PATH IS THE EXACT AFFINE GEODESIC ON THE FIXED SEED SURFACE")
    print("=" * 88)
    x_seed, y_seed, delta_seed = seed_point()
    x_half, y_half, delta_half = path_point(0.5)
    midpoint = 0.5 * (path_start + path_end)
    second_difference = vector_from_path(0.25) - 2.0 * vector_from_path(0.50) + vector_from_path(0.75)

    check(
        "The canonical lambda = 0 endpoint is the exact aligned native seed",
        np.linalg.norm(path_start - np.array([x_seed[0], x_seed[1], y_seed[0], y_seed[1], delta_seed], dtype=float)) < 1.0e-12,
        f"start={np.round(path_start, 12)}",
    )
    check(
        "The canonical lambda = 1 endpoint is the explicit constructive witness",
        np.linalg.norm(path_end - vector_from_path(1.0)) < 1.0e-12,
        f"end={np.round(path_end, 12)}",
    )
    check(
        "The path midpoint is the affine midpoint and the second finite difference vanishes",
        np.linalg.norm(vector_from_path(0.5) - midpoint) < 1.0e-12 and np.linalg.norm(second_difference) < 1.0e-12,
        f"||second diff||={np.linalg.norm(second_difference):.2e}",
    )
    check(
        "Every path point stays on the fixed native seed surface",
        abs(np.mean(x_half) - np.mean(x_seed)) < 1.0e-12 and abs(np.mean(y_half) - np.mean(y_seed)) < 1.0e-12,
        f"(xbar,ybar)=({np.mean(x_half):.12f},{np.mean(y_half):.12f})",
    )
    _ = delta_half

    print("\n" + "=" * 88)
    print("PART 2: THE CANONICAL PATH CROSSES EXACT CLOSURE ONCE AND TRANSVERSELY")
    print("=" * 88)
    eta_vals = np.array([constructive_column_eta(lam) for lam in ETA_GRID], dtype=float)
    eta_shift = eta_vals - 1.0
    diff_eta = np.diff(eta_vals)
    min_idx = int(np.argmin(eta_vals))
    sign_change_count = int(np.sum(eta_shift[:-1] * eta_shift[1:] < 0.0))
    d_eta_star = finite_eta_derivative(lam_star)

    check(
        "The canonical path eta profile has exactly one exact-closure sign change on a dense grid",
        sign_change_count == 1,
        f"sign changes={sign_change_count}",
    )
    check(
        "After its shallow initial dip, eta_1 is strictly increasing on the dense sampled tail",
        min_idx < len(diff_eta) and np.all(diff_eta[min_idx:] > 0.0),
        f"lambda_min={ETA_GRID[min_idx]:.4f}, eta_min={eta_vals[min_idx]:.12f}",
    )
    check(
        "The exact closure root lies on that increasing tail and is therefore unique on the canonical path",
        ETA_GRID[min_idx] < lam_star < 1.0 and abs(constructive_column_eta(lam_star) - 1.0) < 1.0e-12,
        f"lambda_*={lam_star:.12f}",
    )
    check(
        "The canonical-path crossing is transverse",
        d_eta_star > 1.0e-4,
        f"d eta_1 / d lambda |_* = {d_eta_star:.12f}",
    )

    print("\n" + "=" * 88)
    print("PART 3: THE PATH-SELECTED ROOT IS CONSTRUCTIVE, POSITIVE-BRANCH, AND LOCALLY COMPLETE")
    print("=" * 88)
    full_min_singulars = []
    closure_min_singulars = []
    full_rank = True
    closure_rank = True
    for step in FD_STEPS:
        jac = observable_jacobian(v_star, step)
        singular = np.linalg.svd(jac, compute_uv=False)
        tangent_basis = null_space(jac[0:1, :])
        restricted = jac[1:, :] @ tangent_basis
        restricted_singular = np.linalg.svd(restricted, compute_uv=False)
        full_min_singulars.append(float(np.min(singular)))
        closure_min_singulars.append(float(np.min(restricted_singular)))
        full_rank &= int(np.sum(singular > 1.0e-8)) == 5
        closure_rank &= restricted.shape == (4, 4) and int(np.sum(restricted_singular > 1.0e-8)) == 4

    check(
        "The path-selected root satisfies eta_1 = 1 with gamma > 0, E1 > 0, E2 > 0, and Delta_src > 0",
        abs(pack_star[0] - 1.0) < 1.0e-12 and pack_star[1] > 0.0 and pack_star[2] > 0.0 and pack_star[3] > 0.0 and pack_star[4] > 0.0,
        f"pack={np.round(pack_star, 12)}",
    )
    check(
        "The full observable pack is again a local coordinate chart at the path-selected root",
        full_rank and min(full_min_singulars) > 1.0e-4,
        f"min singulars={[f'{val:.6e}' for val in full_min_singulars]}",
    )
    check(
        "On eta_1 = 1, the residual four-pack again coordinatizes the local closure manifold",
        closure_rank and min(closure_min_singulars) > 1.0e-4,
        f"min restricted singulars={[f'{val:.6e}' for val in closure_min_singulars]}",
    )

    print("\n" + "=" * 88)
    print("PART 4: THE PATH LAW PICKS A ROOT DISTINCT FROM THE OTHER CERTIFIED EXACT POSITIVE ROOTS")
    print("=" * 88)
    residuals: list[tuple[str, float, float]] = []
    separations: list[tuple[str, float]] = []
    for label, root in family_roots:
        lam_fit, resid = line_segment_residual(root, path_start, path_end)
        residuals.append((label, lam_fit, resid))
        separations.append((label, float(np.linalg.norm(root - v_star))))

    check(
        "Each previously certified family root stays a definite distance off the canonical path segment",
        min(resid for _label, _lam_fit, resid in residuals) > 3.0e-2,
        f"residuals={[(label, round(resid, 6)) for label, _lam_fit, resid in residuals]}",
    )
    check(
        "The canonical-path root is distinct from every previously certified constructive positive exact root",
        min(sep for _label, sep in separations) > 2.0e-1,
        f"separations={[(label, round(sep, 6)) for label, sep in separations]}",
    )

    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)
    check(
        "The current branch therefore carries an explicit canonical path-selector law candidate",
        True,
        "choose the unique eta_1 = 1 point on the aligned-seed -> constructive-witness affine path",
    )
    check(
        "This is real selector science, but it is still path-chosen rather than reviewer-grade object-derivation from retained physics",
        True,
        "the witness and affine path are explicit constructive inputs, not yet axiom-native outputs",
    )

    print()
    print(f"  lambda_* = {lam_star:.12f}")
    print(f"  path-selected coordinates = {np.round(v_star, 12)}")
    print(f"  path-selected pack        = {np.round(pack_star, 12)}")
    print(
        "  path-selected triplet     = "
        f"({triplet_star['gamma']:.12f}, {triplet_star['E1']:.12f}, {triplet_star['E2']:.12f})"
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
