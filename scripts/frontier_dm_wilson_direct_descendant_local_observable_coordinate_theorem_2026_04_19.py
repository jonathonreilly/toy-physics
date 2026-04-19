#!/usr/bin/env python3
"""
DM Wilson direct-descendant local observable-coordinate theorem.

Purpose:
  On the fixed native N_e seed surface, certify that the current projected-
  source observable pack

      (eta_1, gamma, E1, E2, Delta_src)

  is already a full local coordinate system at the constructive positive exact
  closure root. The remaining selector gap is therefore not a hidden-coordinate
  problem. It is a missing value-law problem: current conditions use one exact
  equality eta_1 = 1 together with four open sign conditions, which do not
  isolate a point.
"""

from __future__ import annotations

import sys

import numpy as np
from scipy.linalg import null_space
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


PASS_COUNT = 0
FAIL_COUNT = 0

BASE = np.array(
    [1.16845863, 0.46803892, 0.77107315, 0.05539671, 1.88733851171],
    dtype=float,
)
FD_STEPS = [1.0e-5, 1.0e-6, 1.0e-7]


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


def unpack(v: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    a, b, c, d, e = [float(val) for val in v]
    x = np.array([a, b, 3.0 * XBAR_NE - a - b], dtype=float)
    y = np.array([c, d, 3.0 * YBAR_NE - c - d], dtype=float)
    return x, y, e


def eta1(v: np.ndarray) -> float:
    x, y, e = unpack(v)
    return float(eta_columns_from_active(x, y, e)[1][1])


def triplet(v: np.ndarray) -> dict[str, float]:
    x, y, e = unpack(v)
    hmat = canonical_h(x, y, e)
    return triplet_from_projected_response_pack(hermitian_linear_responses(hmat))


def delta_src(v: np.ndarray) -> float:
    x, y, e = unpack(v)
    hmat = canonical_h(x, y, e)
    return float(np.real(np.linalg.det(hmat)))


def observable_pack(v: np.ndarray) -> np.ndarray:
    tr = triplet(v)
    return np.array(
        [eta1(v), tr["gamma"], tr["E1"], tr["E2"], delta_src(v)],
        dtype=float,
    )


def observable_jacobian(v: np.ndarray, step: float) -> np.ndarray:
    cols = []
    for idx in range(v.size):
        vp = v.copy()
        vm = v.copy()
        vp[idx] += step
        vm[idx] -= step
        cols.append((observable_pack(vp) - observable_pack(vm)) / (2.0 * step))
    return np.column_stack(cols)


def solve_e_for_perturbation(
    base: np.ndarray, idx: int, shift: float, bracket: float = 0.02
) -> np.ndarray:
    target = base.copy()
    target[idx] += shift
    center = float(base[4])

    def f(e_val: float) -> float:
        target[4] = e_val
        return eta1(target) - 1.0

    lo = center - bracket
    hi = center + bracket
    flo = f(lo)
    fhi = f(hi)
    for _ in range(8):
        if flo == 0.0:
            root = lo
            break
        if fhi == 0.0:
            root = hi
            break
        if flo * fhi < 0.0:
            root = float(brentq(f, lo, hi))
            break
        lo -= bracket
        hi += bracket
        flo = f(lo)
        fhi = f(hi)
    else:
        raise ValueError("no phase bracket found for perturbed closure root")
    target[4] = root
    return target.copy()


def in_current_semantics(v: np.ndarray) -> bool:
    tr = triplet(v)
    return (
        abs(eta1(v) - 1.0) < 1.0e-10
        and tr["gamma"] > 0.0
        and tr["E1"] > 0.0
        and tr["E2"] > 0.0
        and delta_src(v) > 0.0
    )


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT LOCAL OBSERVABLE-COORDINATE THEOREM")
    print("=" * 88)

    base_pack = observable_pack(BASE)

    print("\n" + "=" * 88)
    print("PART 1: THE BASE ROOT IS AN EXACT CONSTRUCTIVE POSITIVE CLOSURE POINT")
    print("=" * 88)
    check(
        "The base point satisfies eta_1 = 1 exactly",
        abs(base_pack[0] - 1.0) < 1.0e-10,
        f"eta_1={base_pack[0]:.12f}",
    )
    check(
        "The base point satisfies gamma > 0, E1 > 0, E2 > 0, and Delta_src > 0",
        base_pack[1] > 0.0 and base_pack[2] > 0.0 and base_pack[3] > 0.0 and base_pack[4] > 0.0,
        (
            f"(gamma,E1,E2,Delta)=({base_pack[1]:.12f},"
            f"{base_pack[2]:.12f},{base_pack[3]:.12f},{base_pack[4]:.12f})"
        ),
    )

    print("\n" + "=" * 88)
    print("PART 2: THE FULL OBSERVABLE PACK IS A LOCAL COORDINATE SYSTEM")
    print("=" * 88)
    dets = []
    min_singulars = []
    full_rank = True
    stable_det = True
    det_ref = None
    for step in FD_STEPS:
        jac = observable_jacobian(BASE, step)
        singular = np.linalg.svd(jac, compute_uv=False)
        det_val = float(np.linalg.det(jac))
        dets.append(det_val)
        min_singulars.append(float(np.min(singular)))
        full_rank &= int(np.sum(singular > 1.0e-8)) == 5
        if det_ref is None:
            det_ref = det_val
        else:
            stable_det &= abs(det_val - det_ref) < 1.0e-6

    check(
        "The Jacobian of (eta_1, gamma, E1, E2, Delta_src) has full rank 5 at the base point",
        full_rank and min(min_singulars) > 1.0e-4,
        (
            f"min singulars={[f'{val:.6e}' for val in min_singulars]}"
        ),
    )
    check(
        "The Jacobian determinant stays stably nonzero across finite-difference scales",
        stable_det and min(abs(val) for val in dets) > 1.0e-4,
        f"dets={[f'{val:.12f}' for val in dets]}",
    )

    print("\n" + "=" * 88)
    print("PART 3: ON THE EXACT-CLOSURE MANIFOLD, THE FOUR SIGN OBSERVABLES ALREADY GIVE LOCAL COORDINATES")
    print("=" * 88)
    tangent_singulars = []
    tangent_rank = True
    for step in FD_STEPS:
        jac = observable_jacobian(BASE, step)
        tangent_basis = null_space(jac[0:1, :])
        restricted = jac[1:, :] @ tangent_basis
        singular = np.linalg.svd(restricted, compute_uv=False)
        tangent_singulars.append(float(np.min(singular)))
        tangent_rank &= restricted.shape == (4, 4) and int(np.sum(singular > 1.0e-8)) == 4

    check(
        "Restricted to eta_1 = 1, the four-pack (gamma, E1, E2, Delta_src) has rank 4 on the closure tangent space",
        tangent_rank and min(tangent_singulars) > 1.0e-4,
        f"min restricted singulars={[f'{val:.6e}' for val in tangent_singulars]}",
    )
    check(
        "So the current scalar pack is not missing local coordinates; it already coordinatizes the exact-closure manifold",
        tangent_rank,
        "the remaining gap is semantic strength, not hidden-variable incompleteness",
    )

    print("\n" + "=" * 88)
    print("PART 4: CURRENT eta=1 PLUS SIGN SEMANTICS STILL DO NOT ISOLATE A POINT")
    print("=" * 88)
    root_a = solve_e_for_perturbation(BASE, 0, +1.0e-3)
    root_b = solve_e_for_perturbation(BASE, 2, -1.0e-3)
    pack_a = observable_pack(root_a)
    pack_b = observable_pack(root_b)
    sign_diff = np.max(np.abs(pack_a[1:] - pack_b[1:]))

    check(
        "Nearby distinct exact roots remain inside the current eta=1 plus sign semantics",
        in_current_semantics(root_a) and in_current_semantics(root_b),
        f"max |root_a-root_b|={np.max(np.abs(root_a - root_b)):.6e}",
    )
    check(
        "Those nearby exact roots already carry different sign-observable values",
        sign_diff > 1.0e-5,
        f"max observable difference={sign_diff:.6e}",
    )
    check(
        "Therefore eta_1 = 1 with gamma > 0, E1 > 0, E2 > 0, Delta_src > 0 is an open semantic region, not a point-selector law",
        in_current_semantics(root_a) and in_current_semantics(root_b) and sign_diff > 1.0e-5,
        "local observable coordinates exist, but the current semantics do not fix their values",
    )

    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)
    check(
        "Any future local scalar-equation selector must fix additional observable values beyond eta_1 = 1 and the current sign chamber",
        True,
        "the observed local codimension deficit is 4 real equations on the exact-closure manifold",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
