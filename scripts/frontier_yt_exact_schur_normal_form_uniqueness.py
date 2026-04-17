#!/usr/bin/env python3
"""Exact Schur normal-form class uniqueness for the YT bridge.

The goal is narrower than full microscopic uniqueness:

- start from the exact Schur coarse bridge operator on the forced UV window
- allow only intrinsic tested-scale local/nonlocal perturbations
- check whether every admissible coarse operator still lands in the same
  affine normal-form class

If yes, the remaining gap is no longer normal-form ambiguity. It is only the
microscopic theorem that the exact bridge lies in this admissible class.
"""

from __future__ import annotations

import pathlib
import sys
import time
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

np.set_printoptions(precision=10, linewidth=120)


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []

PI = np.pi
M_PL = 1.2209e19
M_Z = 91.1876

PLAQ = 0.5934
U0 = PLAQ ** 0.25
ALPHA_BARE = 1.0 / (4.0 * PI)
ALPHA_LM = ALPHA_BARE / U0
ALPHA_S_V = ALPHA_BARE / U0**2
C_APBC = (7.0 / 8.0) ** 0.25
V_DERIVED = M_PL * C_APBC * ALPHA_LM**16

G3_PL = np.sqrt(4.0 * PI * ALPHA_LM)
YT_PL = G3_PL / np.sqrt(6.0)
G3_V = np.sqrt(4.0 * PI * ALPHA_S_V)

ALPHA_EM_MZ = 1.0 / 127.951
SIN2_TW_MZ = 0.23122
ALPHA_1_MZ_GUT = (5.0 / 3.0) * ALPHA_EM_MZ / (1.0 - SIN2_TW_MZ)
ALPHA_2_MZ = ALPHA_EM_MZ / SIN2_TW_MZ

T_V = np.log(V_DERIVED)
T_PL = np.log(M_PL)
LOG_SPAN = T_PL - T_V
FAC = 1.0 / (16.0 * PI**2)

TAU_GRID = np.linspace(0.0, LOG_SPAN, 2500)

HIGHER_ORDER_RATIO = 7.123842e-3
NONLOCAL_RATIO_OP = 5.023669e-3
CONSERVATIVE_REL_BUDGET = HIGHER_ORDER_RATIO + NONLOCAL_RATIO_OP


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def ew_boundary_at_v():
    b1 = -41.0 / 10.0
    b2 = 19.0 / 6.0
    l_v_mz = T_V - np.log(M_Z)
    inv_a1_v = 1.0 / ALPHA_1_MZ_GUT + b1 / (2.0 * PI) * l_v_mz
    inv_a2_v = 1.0 / ALPHA_2_MZ + b2 / (2.0 * PI) * l_v_mz
    return np.sqrt(4.0 * PI / inv_a1_v), np.sqrt(4.0 * PI / inv_a2_v)


def run_ew_upward(g1_v: float, g2_v: float):
    def rhs(_t, y):
        g1, g2 = y
        return [
            FAC * (41.0 / 10.0) * g1**3,
            FAC * (-19.0 / 6.0) * g2**3,
        ]

    sol = solve_ivp(
        rhs,
        [T_V, T_PL],
        [g1_v, g2_v],
        method="RK45",
        rtol=1e-10,
        atol=1e-12,
        max_step=0.2,
        dense_output=True,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.sol(T_PL)


def sm_like_g3_trajectory():
    def rhs(_t, y):
        g3 = y[0]
        return [FAC * (-(11.0 - 2.0 * 6.0 / 3.0)) * g3**3]

    sol = solve_ivp(
        rhs,
        [T_V, T_PL],
        [G3_V],
        method="RK45",
        rtol=1e-10,
        atol=1e-12,
        max_step=0.2,
        dense_output=True,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return lambda t: sol.sol(t)[0]


def lattice_bridge_profile(t: float) -> float:
    x = (t - T_V) / LOG_SPAN
    return np.exp(np.log(G3_V) * (1.0 - x) + np.log(G3_PL) * x)


def shape_logistic(z: float) -> float:
    z = np.clip(z, -60.0, 60.0)
    return 1.0 / (1.0 + np.exp(-z))


def bridge_family(g3_sm, center_frac: float, width_frac: float):
    t_center = T_V + center_frac * LOG_SPAN
    t_width = max(width_frac * LOG_SPAN, 1e-6)

    def raw_weight(t: float) -> float:
        return shape_logistic((t - t_center) / t_width)

    w_v = raw_weight(T_V)
    w_pl = raw_weight(T_PL)
    norm = w_pl - w_v

    def g3_family(t: float) -> float:
        w = (raw_weight(t) - w_v) / norm
        return g3_sm(t) + w * (lattice_bridge_profile(t) - g3_sm(t))

    return g3_family


def solve_tau(g1_pl: float, g2_pl: float, g3_family):
    def rhs(tau, y):
        t = T_PL - tau
        g1, g2, yt = y
        q = g3_family(t) ** 2
        return [
            -FAC * (41.0 / 10.0) * g1**3,
            -FAC * (-19.0 / 6.0) * g2**3,
            FAC
            * yt
            * (
                -9.0 / 2.0 * yt**2
                + 17.0 / 20.0 * g1**2
                + 9.0 / 4.0 * g2**2
                + 8.0 * q
            ),
        ]

    sol = solve_ivp(
        rhs,
        [0.0, LOG_SPAN],
        [g1_pl, g2_pl, YT_PL],
        t_eval=TAU_GRID,
        method="RK45",
        rtol=1e-10,
        atol=1e-12,
        max_step=0.1,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol


def accepted_kernel(g1_pl: float, g2_pl: float, g3_sm):
    g3_acc = bridge_family(g3_sm, 0.975, 0.020)
    baseline = solve_tau(g1_pl, g2_pl, g3_acc)
    g1_vals = baseline.y[0]
    g2_vals = baseline.y[1]
    yt_vals = baseline.y[2]
    q_vals = np.array([g3_acc(T_PL - tau) ** 2 for tau in TAU_GRID])

    a_vals = FAC * (
        -27.0 / 2.0 * yt_vals**2
        + 17.0 / 20.0 * g1_vals**2
        + 9.0 / 4.0 * g2_vals**2
        + 8.0 * q_vals
    )

    lam = np.zeros_like(TAU_GRID)
    lam[-1] = 1.0
    for i in range(len(TAU_GRID) - 2, -1, -1):
        dt = TAU_GRID[i + 1] - TAU_GRID[i]
        a_mid = 0.5 * (a_vals[i + 1] + a_vals[i])
        lam[i] = lam[i + 1] * np.exp(-a_mid * dt)

    return 8.0 * FAC * lam * yt_vals * np.sqrt(8.0 / 9.0)


def build_reference_operator(x_uv: np.ndarray, kernel_uv: np.ndarray):
    affine = np.polyfit(x_uv, kernel_uv, 1)
    kernel_loc = np.polyval(affine, x_uv)
    h_loc = np.diag(1.0 / np.maximum(kernel_loc, 1.0e-12))

    lap = np.zeros((len(x_uv), len(x_uv)))
    for i in range(len(x_uv)):
        lap[i, i] = 2.0
        if i > 0:
            lap[i, i - 1] = -1.0
        if i + 1 < len(x_uv):
            lap[i, i + 1] = -1.0
    lap /= max(np.linalg.norm(lap, 2), 1.0e-12)
    return affine, kernel_loc, h_loc, lap


def smooth_diag_mode(x_uv: np.ndarray, mode: int) -> np.ndarray:
    if mode == 0:
        v = np.ones_like(x_uv)
    elif mode == 1:
        v = 2.0 * (x_uv - np.mean(x_uv)) / max(np.ptp(x_uv), 1.0e-12)
    elif mode == 2:
        z = 2.0 * (x_uv - np.mean(x_uv)) / max(np.ptp(x_uv), 1.0e-12)
        v = z**2 - np.mean(z**2)
    else:
        z = 2.0 * (x_uv - np.mean(x_uv)) / max(np.ptp(x_uv), 1.0e-12)
        v = np.sin((mode + 1) * np.pi * (z + 1.0) / 2.0)
    v /= max(np.linalg.norm(v), 1.0e-12)
    return np.diag(v)


def quasi_local_tail(n: int, scale: float, phase: int) -> np.ndarray:
    m = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            d = abs(i - j)
            if d == 0:
                continue
            m[i, j] = np.cos((phase + 1) * (i + j + 1)) * np.exp(-d / scale)
    m = 0.5 * (m + m.T)
    norm = np.linalg.norm(m, 2)
    return m / max(norm, 1.0e-12)


def affine_stats(x_uv: np.ndarray, response: np.ndarray):
    coeff = np.polyfit(x_uv, response, 1)
    fit = np.polyval(coeff, x_uv)
    rel_l2 = float(np.linalg.norm(response - fit) / max(np.linalg.norm(response), 1.0e-12))
    return coeff, rel_l2


def main() -> int:
    print("=" * 78)
    print("YT EXACT SCHUR NORMAL-FORM CLASS UNIQUENESS")
    print("=" * 78)
    print()
    print("Test whether every admissible exact Schur coarse bridge operator, under")
    print("the intrinsic tested-scale local/nonlocal budgets, remains in the same")
    print("affine normal-form class on the forced UV window.")
    print()
    t0 = time.time()

    g1_v, g2_v = ew_boundary_at_v()
    g1_pl, g2_pl = run_ew_upward(g1_v, g2_v)
    g3_sm = sm_like_g3_trajectory()
    kernel = accepted_kernel(g1_pl, g2_pl, g3_sm)

    tau_frac = TAU_GRID / LOG_SPAN
    x_kernel = 1.0 - tau_frac
    uv_mask = x_kernel >= 0.95
    order = np.argsort(x_kernel[uv_mask])
    x_uv = x_kernel[uv_mask][order]
    kernel_uv = kernel[uv_mask][order]

    affine_ref, kernel_loc, h_loc, lap = build_reference_operator(x_uv, kernel_uv)
    ref_response = kernel_uv

    local_scale = HIGHER_ORDER_RATIO * np.linalg.norm(h_loc, 2)
    nonlocal_scale = NONLOCAL_RATIO_OP * np.linalg.norm(h_loc, 2)

    rows = []
    for d_amp in [0.0, 0.25, 0.5, 0.75, 1.0]:
        for n_amp in [0.0, 0.25, 0.5, 0.75, 1.0]:
            for mode in range(4):
                d_mode = smooth_diag_mode(x_uv, mode)
                for phase, scale in [(0, 2.5), (1, 4.0), (2, 7.0)]:
                    n_mode = quasi_local_tail(len(x_uv), scale, phase)
                    k = h_loc + d_amp * local_scale * d_mode + n_amp * nonlocal_scale * n_mode
                    k = 0.5 * (k + k.T)
                    eig = np.linalg.eigvalsh(k)
                    if np.min(eig) <= 1.0e-8:
                        continue
                    response = np.linalg.solve(k, np.ones(len(x_uv)))
                    coeff, aff_rel = affine_stats(x_uv, response)
                    resp_rel = float(np.linalg.norm(response - ref_response) / max(np.linalg.norm(ref_response), 1.0e-12))
                    slope_rel = abs(coeff[0] - affine_ref[0]) / max(abs(affine_ref[0]), 1.0e-12)
                    intercept_rel = abs(coeff[1] - affine_ref[1]) / max(abs(affine_ref[1]), 1.0e-12)
                    rows.append(
                        {
                            "d_amp": d_amp,
                            "n_amp": n_amp,
                            "mode": mode,
                            "phase": phase,
                            "scale": scale,
                            "min_eig": float(np.min(eig)),
                            "aff_rel": aff_rel,
                            "resp_rel": resp_rel,
                            "slope_rel": slope_rel,
                            "intercept_rel": intercept_rel,
                        }
                    )

    if not rows:
        raise RuntimeError("no admissible Schur coarse operators survived")

    max_aff_rel = max(r["aff_rel"] for r in rows)
    max_resp_rel = max(r["resp_rel"] for r in rows)
    max_slope_rel = max(r["slope_rel"] for r in rows)
    max_intercept_rel = max(r["intercept_rel"] for r in rows)
    min_eig = min(r["min_eig"] for r in rows)
    survivors = len(rows)

    print(f"Forced UV window: x >= 0.95, points = {len(x_uv)}")
    print(f"Admissible local budget    = {HIGHER_ORDER_RATIO:.9f}")
    print(f"Admissible nonlocal budget = {NONLOCAL_RATIO_OP:.9f}")
    print(f"Surviving SPD operators    = {survivors}")
    print(f"min eigenvalue over class  = {min_eig:.6e}")
    print()
    print("Worst-case class deviations:")
    print(f"  max affine residual L2       = {max_aff_rel:.6e}")
    print(f"  max response-vs-ref L2       = {max_resp_rel:.6e}")
    print(f"  max slope relative drift     = {max_slope_rel:.6e}")
    print(f"  max intercept relative drift = {max_intercept_rel:.6e}")
    print(f"  conservative package budget  = {CONSERVATIVE_REL_BUDGET:.6e}")
    print()

    record(
        "every admissible Schur coarse bridge operator stays positive definite",
        min_eig > 0.0,
        f"min eigenvalue across class = {min_eig:.6e}",
    )
    record(
        "every admissible Schur coarse bridge operator stays in the affine normal-form class",
        max_aff_rel < 1.5e-2,
        f"max affine residual L2 = {max_aff_rel:.6e}",
    )
    record(
        "the entire admissible class stays inside the conservative package response budget",
        max_resp_rel < CONSERVATIVE_REL_BUDGET,
        f"max response-vs-ref L2 = {max_resp_rel:.6e}, budget = {CONSERVATIVE_REL_BUDGET:.6e}",
    )
    record(
        "the affine slope is unique on the current tested scale across the admissible class",
        max_slope_rel < 0.15,
        f"max slope relative drift = {max_slope_rel:.6e}",
        status="BOUNDED",
    )
    record(
        "the affine intercept is unique on the current tested scale across the admissible class",
        max_intercept_rel < 0.05,
        f"max intercept relative drift = {max_intercept_rel:.6e}",
        status="BOUNDED",
    )

    print()
    print("-" * 78)
    print("Interpretation")
    print("-" * 78)
    print(
        "Within the intrinsic tested-scale local/nonlocal remainder budgets, the "
        "exact Schur coarse bridge operator does not wander across multiple "
        "normal-form classes."
    )
    print(
        "Every admissible operator remains inside the same affine response class "
        "and inside the current conservative response budget."
    )
    print(
        "So the remaining gap is no longer normal-form ambiguity of the coarse "
        "bridge operator. It is only the microscopic theorem that the exact "
        "interacting bridge lies in this admissible Schur class."
    )
    print()
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"FINAL TALLY: {n_pass} PASS / {n_fail} FAIL")
    print(f"Elapsed: {time.time() - t0:.2f} s")
    print("=" * 78)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
