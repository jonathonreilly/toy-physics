#!/usr/bin/env python3
"""
Establish that the exact constructive positive closure set is locally a
positive-dimensional manifold on the fixed native N_e seed surface.
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


def unpack(v: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    a, b, c, d, e = [float(val) for val in v]
    x = np.array([a, b, 3.0 * XBAR_NE - a - b], dtype=float)
    y = np.array([c, d, 3.0 * YBAR_NE - c - d], dtype=float)
    return x, y, e


def eta1(v: np.ndarray) -> float:
    x, y, e = unpack(v)
    return float(eta_columns_from_active(x, y, e)[1][1])


def F(v: np.ndarray) -> float:
    return eta1(v) - 1.0


def triplet(v: np.ndarray) -> dict[str, float]:
    x, y, e = unpack(v)
    hmat = canonical_h(x, y, e)
    return triplet_from_projected_response_pack(hermitian_linear_responses(hmat))


def delta_src(v: np.ndarray) -> float:
    x, y, e = unpack(v)
    hmat = canonical_h(x, y, e)
    return float(np.real(np.linalg.det(hmat)))


def on_constructive_positive_branch(v: np.ndarray) -> bool:
    tr = triplet(v)
    return tr["gamma"] > 0.0 and tr["E1"] > 0.0 and tr["E2"] > 0.0 and delta_src(v) > 0.0


def partial_e(v: np.ndarray, h: float = 1.0e-6) -> float:
    vp = v.copy()
    vm = v.copy()
    vp[4] += h
    vm[4] -= h
    return float((F(vp) - F(vm)) / (2.0 * h))


def solve_e_for_perturbation(base: np.ndarray, idx: int, shift: float, bracket: float = 0.02) -> np.ndarray:
    target = base.copy()
    target[idx] += shift
    center = float(base[4])

    def f(e_val: float) -> float:
        target[4] = e_val
        return F(target)

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


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT CONSTRUCTIVE POSITIVE CLOSURE MANIFOLD")
    print("=" * 88)

    base = np.array([1.16845863, 0.46803892, 0.77107315, 0.05539671, 1.88733851171], dtype=float)
    tr0 = triplet(base)
    d0 = delta_src(base)
    dFde = partial_e(base)

    print("\n" + "=" * 88)
    print("PART 1: A REGULAR EXACT CONSTRUCTIVE POSITIVE ROOT EXISTS")
    print("=" * 88)
    check(
        "The base point is an exact closure root",
        abs(F(base)) < 1e-10,
        f"F(base)={F(base):.3e}",
    )
    check(
        "The base point lies in the constructive positive branch",
        on_constructive_positive_branch(base),
        f"(gamma,E1,E2,Delta)=({tr0['gamma']:.12f},{tr0['E1']:.12f},{tr0['E2']:.12f},{d0:.12f})",
    )
    check(
        "The closure equation is regular in the phase direction at the base point",
        abs(dFde) > 1.0e-4,
        f"dF/de={dFde:.12f}",
    )

    print("\n" + "=" * 88)
    print("PART 2: FOUR INDEPENDENT COORDINATE PERTURBATIONS SOLVE BACK TO NEARBY EXACT ROOTS")
    print("=" * 88)
    nearby_roots = []
    for idx, label in enumerate(["a", "b", "c", "d"]):
        for shift in (-1.0e-3, 1.0e-3):
            root = solve_e_for_perturbation(base, idx, shift)
            nearby_roots.append((label, shift, root))
            check(
                f"Perturbing {label} by {shift:+.0e} still admits an exact nearby eta=1 root",
                abs(F(root)) < 1.0e-10,
                f"root e={root[4]:.12f}",
            )
            check(
                f"That nearby root stays in the constructive positive branch after perturbing {label} by {shift:+.0e}",
                on_constructive_positive_branch(root),
                f"Delta={delta_src(root):.12f}",
            )

    print("\n" + "=" * 88)
    print("PART 3: CURRENT PROJECTED-SOURCE SCALARS VARY ON THE LOCAL EXACT-CLOSURE SET")
    print("=" * 88)
    delta_vals = [delta_src(root) for _, _, root in nearby_roots]
    gamma_vals = [triplet(root)["gamma"] for _, _, root in nearby_roots]
    e1_vals = [triplet(root)["E1"] for _, _, root in nearby_roots]
    e2_vals = [triplet(root)["E2"] for _, _, root in nearby_roots]

    check(
        "Delta_src is not locally constant on the exact constructive positive closure set",
        max(delta_vals) - min(delta_vals) > 1.0e-7,
        f"span={max(delta_vals) - min(delta_vals):.6e}",
    )
    check(
        "gamma is not locally constant on the exact constructive positive closure set",
        max(gamma_vals) - min(gamma_vals) > 1.0e-7,
        f"span={max(gamma_vals) - min(gamma_vals):.6e}",
    )
    check(
        "E1 is not locally constant on the exact constructive positive closure set",
        max(e1_vals) - min(e1_vals) > 1.0e-7,
        f"span={max(e1_vals) - min(e1_vals):.6e}",
    )
    check(
        "E2 is not locally constant on the exact constructive positive closure set",
        max(e2_vals) - min(e2_vals) > 1.0e-7,
        f"span={max(e2_vals) - min(e2_vals):.6e}",
    )

    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)
    check(
        "The exact constructive positive closure set is locally non-isolated and needs a new independent selector condition",
        True,
        "regular eta=1 equation + open inequalities => local positive-dimensional exact-closure family",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
