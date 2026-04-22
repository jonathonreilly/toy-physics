#!/usr/bin/env python3
"""
DM A-BCC corrected five-basin chamber+DPLE support theorem.

Purpose:
  update the older chamber+DPLE route to the corrected retained five-basin
  chart by explicitly checking the missing Basin 2 case.

This runner does NOT claim full native closure of the DM gate. It verifies the
sharper statement:

  on the corrected retained five-basin chart,
      chamber survivors = {Basin 1, Basin 2, Basin X}
      F_4 passers        = {Basin 1}
  so chamber ∩ F_4 still selects Basin 1 uniquely.
"""

from __future__ import annotations

import math
import sys
from typing import Tuple

import numpy as np

PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> bool:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))
    return cond


GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0

T_M = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
T_D = np.array([[0, -1, 1], [-1, 1, 0], [1, 0, -1]], dtype=complex)
T_Q = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], dtype=complex)
H_BASE = np.array(
    [
        [0, E1, -E1 - 1j * GAMMA],
        [E1, 0, -E2],
        [-E1 + 1j * GAMMA, -E2, 0],
    ],
    dtype=complex,
)

BASINS = {
    "Basin 1": (0.657061, 0.933806, 0.715042),
    "Basin N": (0.501997, 0.853543, 0.425916),
    "Basin P": (1.037883, 1.433019, -1.329548),
    "Basin X": (21.128264, 12.680028, 2.089235),
    "Basin 2": (28.006000, 20.722000, 5.012000),
}

F4_REFERENCE = {
    "Basin 1": True,
    "Basin N": False,
    "Basin P": False,
    "Basin X": False,
    "Basin 2": False,
}


def J_of(point: Tuple[float, float, float]) -> np.ndarray:
    m, d, q = point
    return m * T_M + d * T_D + q * T_Q


def H_of(point: Tuple[float, float, float]) -> np.ndarray:
    return H_BASE + J_of(point)


def cubic_coeffs(H0: np.ndarray, H1: np.ndarray) -> np.ndarray:
    ts = np.array([-1.0, 0.0, 0.5, 1.0])
    vals = np.array([np.linalg.det(H0 + t * H1).real for t in ts])
    A = np.vstack([ts ** k for k in range(4)]).T
    return np.linalg.solve(A, vals)


def F4_closed_form(point: Tuple[float, float, float]):
    J = J_of(point)
    c0, c1, c2, c3 = cubic_coeffs(H_BASE, J)
    delta = c2 * c2 - 3.0 * c1 * c3
    info = {"c0": c0, "c1": c1, "c2": c2, "c3": c3, "delta": delta, "tstar": None, "pstar": None}
    if delta <= 0 or abs(c3) < 1e-15:
        return False, info
    sqrtD = math.sqrt(delta)
    cands = [(-c2 + sqrtD) / (3.0 * c3), (-c2 - sqrtD) / (3.0 * c3)]
    for t in cands:
        ppp = 2.0 * c2 + 6.0 * c3 * t
        pstar = c0 + c1 * t + c2 * t**2 + c3 * t**3
        if ppp > 0 and 0.0 < t < 1.0 and pstar > 0 and (pstar > 0) == (c0 > 0):
            info["tstar"] = t
            info["pstar"] = pstar
            return True, info
    return False, info


def F4_newton(point: Tuple[float, float, float]):
    J = J_of(point)
    c0, c1, c2, c3 = cubic_coeffs(H_BASE, J)
    for t0 in [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]:
        t = t0
        ok = False
        for _ in range(200):
            f = c1 + 2 * c2 * t + 3 * c3 * t * t
            fp = 2 * c2 + 6 * c3 * t
            if abs(fp) < 1e-18:
                break
            t_new = t - f / fp
            if abs(t_new - t) < 1e-13:
                t = t_new
                ok = True
                break
            t = t_new
        if not ok:
            continue
        if abs(c1 + 2 * c2 * t + 3 * c3 * t * t) > 1e-8:
            continue
        if not (0.0 < t < 1.0):
            continue
        ppp = 2 * c2 + 6 * c3 * t
        if ppp <= 0:
            continue
        pstar = c0 + c1 * t + c2 * t**2 + c3 * t**3
        if pstar > 0 and (pstar > 0) == (c0 > 0):
            return True, {"t": t, "pstar": pstar}
    return False, {}


def F4_sampling(point: Tuple[float, float, float], n: int = 4001):
    J = J_of(point)
    ts = np.linspace(0.0, 1.0, n)
    ps = np.array([np.linalg.det(H_BASE + t * J).real for t in ts])
    if ps[0] <= 0:
        return False, {}
    i_min = int(np.argmin(ps))
    if i_min in (0, n - 1):
        return False, {}
    if not (ps[i_min - 1] > ps[i_min] < ps[i_min + 1]):
        return False, {}
    if ps[i_min] <= 0:
        return False, {}
    return True, {"t": float(ts[i_min]), "pstar": float(ps[i_min])}


def task_chamber() -> dict[str, bool]:
    print("\n--- T1: corrected chamber survivors on the five-basin chart ---")
    in_chamber: dict[str, bool] = {}
    for name, (_, d, q) in BASINS.items():
        val = d + q
        in_chamber[name] = val >= E1
        print(f"    {name:<8} q+delta={val:.6f}  [{'IN' if in_chamber[name] else 'OUT'}]")

    survivors = {name for name, ok in in_chamber.items() if ok}
    check(
        "Corrected chamber survivors are exactly {Basin 1, Basin 2, Basin X}",
        survivors == {"Basin 1", "Basin 2", "Basin X"},
        f"survivors={sorted(survivors)}",
    )
    return in_chamber


def task_f4() -> tuple[dict[str, bool], dict[str, bool], dict[str, bool]]:
    print("\n--- T2: F_4 on the corrected five-basin chart ---")
    closed_form: dict[str, bool] = {}
    newton: dict[str, bool] = {}
    sampled: dict[str, bool] = {}
    for name, point in BASINS.items():
        cf, info = F4_closed_form(point)
        nw, _ = F4_newton(point)
        sm, _ = F4_sampling(point)
        closed_form[name] = cf
        newton[name] = nw
        sampled[name] = sm
        check(
            f"{name}: closed-form F_4 matches corrected reference",
            cf == F4_REFERENCE[name],
            f"Δ={info['delta']:+.6e}",
        )
        check(
            f"{name}: Newton F_4 matches corrected reference",
            nw == F4_REFERENCE[name],
        )
        check(
            f"{name}: sampled F_4 matches corrected reference",
            sm == F4_REFERENCE[name],
        )

    b2_info = F4_closed_form(BASINS["Basin 2"])[1]
    check(
        "Basin 2 has negative DPLE discriminant",
        b2_info["delta"] < 0,
        f"Δ_2={b2_info['delta']:+.6e}",
    )
    return closed_form, newton, sampled


def task_composition(in_chamber: dict[str, bool], f4_cf: dict[str, bool], f4_nw: dict[str, bool], f4_sm: dict[str, bool]) -> None:
    print("\n--- T3: corrected composition ---")
    for name in BASINS:
        check(
            f"{name}: all three F_4 routes agree",
            f4_cf[name] == f4_nw[name] == f4_sm[name],
            f"cf={f4_cf[name]}, nw={f4_nw[name]}, sm={f4_sm[name]}",
        )

    chamber_survivors = {name for name, ok in in_chamber.items() if ok}
    f4_passers = {name for name, ok in f4_cf.items() if ok}
    closure = chamber_survivors & f4_passers
    check(
        "Corrected chamber ∩ F_4 still selects Basin 1 uniquely",
        closure == {"Basin 1"},
        f"chamber={sorted(chamber_survivors)}, F4={sorted(f4_passers)}, ∩={sorted(closure)}",
    )

    det_b2 = float(np.linalg.det(H_of(BASINS["Basin 2"])).real)
    check(
        "Basin 2 is still a C_neg endpoint",
        det_b2 < 0,
        f"det(Basin 2)={det_b2:+.6f}",
    )


def main() -> int:
    print("=" * 78)
    print("DM A-BCC corrected five-basin chamber+DPLE support theorem")
    print("=" * 78)
    in_chamber = task_chamber()
    f4_cf, f4_nw, f4_sm = task_f4()
    task_composition(in_chamber, f4_cf, f4_nw, f4_sm)
    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
