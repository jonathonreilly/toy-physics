#!/usr/bin/env python3
"""
Exact interacting bridge transport law
======================================

Package-native UV->IR transport statement for the exact interacting bridge on
the forced UV window.

This is not another family scan. It consolidates the current selector and
correction results into a transport law with explicit higher-order and
nonlocal remainder terms.
"""

from __future__ import annotations

import time
from math import erf, sqrt

import numpy as np
from scipy.integrate import solve_ivp

np.set_printoptions(precision=10, linewidth=120)

PASS = 0
FAIL = 0


def report(tag: str, ok: bool, msg: str):
    global PASS, FAIL
    if ok:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


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

TARGET_YT_PHYS = 0.9176

ALPHA_EM_MZ = 1.0 / 127.951
SIN2_TW_MZ = 0.23122
ALPHA_1_MZ_GUT = (5.0 / 3.0) * ALPHA_EM_MZ / (1.0 - SIN2_TW_MZ)
ALPHA_2_MZ = ALPHA_EM_MZ / SIN2_TW_MZ

T_V = np.log(V_DERIVED)
T_PL = np.log(M_PL)
LOG_SPAN = T_PL - T_V
FAC = 1.0 / (16.0 * PI**2)

TAU_GRID = np.linspace(0.0, LOG_SPAN, 2500)
TS_GRID = np.linspace(T_V, T_PL, 1500)
X_GRID = (TS_GRID - T_V) / LOG_SPAN


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


def shape_erf(z: float) -> float:
    return 0.5 * (1.0 + erf(np.clip(z, -8.0, 8.0) / sqrt(2.0)))


def shape_smoothstep(z: float) -> float:
    u = np.clip((z + 1.0) / 2.0, 0.0, 1.0)
    return u * u * (3.0 - 2.0 * u)


def bridge_family(shape_name: str, g3_sm, center_frac: float, width_frac: float):
    shapes = {
        "logistic": shape_logistic,
        "erf": shape_erf,
        "smoothstep": shape_smoothstep,
    }
    shape = shapes[shape_name]
    t_center = T_V + center_frac * LOG_SPAN
    t_width = max(width_frac * LOG_SPAN, 1e-6)

    def raw_weight(t: float) -> float:
        return shape((t - t_center) / t_width)

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
    g3_acc = bridge_family("logistic", g3_sm, 0.975, 0.020)
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


def amplitude_scan(g1_pl: float, g2_pl: float, g3_sm, g3_ref):
    a_grid = np.linspace(0.90, 1.10, 21)
    yt_vals = []
    for a in a_grid:
        def g3_amp(t):
            return g3_sm(t) + float(a) * (g3_ref(t) - g3_sm(t))

        sol = solve_ivp(
            lambda t, y: [
                FAC * (41.0 / 10.0) * y[0] ** 3,
                FAC * (-19.0 / 6.0) * y[1] ** 3,
                FAC
                * y[2]
                * (
                    9.0 / 2.0 * y[2] ** 2
                    - 17.0 / 20.0 * y[0] ** 2
                    - 9.0 / 4.0 * y[1] ** 2
                    - 8.0 * g3_amp(t) ** 2
                ),
            ],
            [T_PL, T_V],
            [g1_pl, g2_pl, YT_PL],
            method="RK45",
            rtol=1e-9,
            atol=1e-11,
            max_step=0.2,
        )
        if not sol.success:
            raise RuntimeError(sol.message)
        yt_vals.append(float(sol.y[2, -1] * np.sqrt(8.0 / 9.0)))

    yt_vals = np.array(yt_vals)
    delta = a_grid - 1.0
    coeffs = np.polynomial.polynomial.polyfit(delta, yt_vals, 4)
    fit = np.polynomial.polynomial.polyval(delta, coeffs)
    return a_grid, yt_vals, coeffs, fit


print("=" * 78)
print("y_t EXACT INTERACTING BRIDGE TRANSPORT")
print("=" * 78)
print()
print("Package-native UV->IR transport law on the forced UV window.")
print()
t0 = time.time()

g1_v, g2_v = ew_boundary_at_v()
g1_pl, g2_pl = run_ew_upward(g1_v, g2_v)
g3_sm = sm_like_g3_trajectory()
kernel = accepted_kernel(g1_pl, g2_pl, g3_sm)

tau_frac = TAU_GRID / LOG_SPAN
x_kernel = 1.0 - tau_frac
uv_cut = 0.95
uv_mask = x_kernel >= uv_cut
order = np.argsort(x_kernel[uv_mask])
x_uv = x_kernel[uv_mask][order]
kernel_uv = kernel[uv_mask][order]

affine = np.polyfit(x_uv, kernel_uv, 1)
kernel_loc = np.polyval(affine, x_uv)
kernel_res = kernel_uv - kernel_loc
kernel_rel_max = float(np.max(np.abs(kernel_res / kernel_uv)))
kernel_rel_l2 = float(
    np.sqrt(np.trapezoid(kernel_res * kernel_res, x_uv))
    / np.sqrt(np.trapezoid(kernel_uv * kernel_uv, x_uv))
)

reference = bridge_family("logistic", g3_sm, 0.975, 0.020)
g3_ref = np.array([reference(T_V + x * LOG_SPAN) for x in x_uv])
g3_sm_uv = np.array([g3_sm(T_V + x * LOG_SPAN) for x in x_uv])
delta_q = g3_ref**2 - g3_sm_uv**2

i2 = float(np.trapezoid(delta_q, x_uv))
c2 = float(np.trapezoid(x_uv * delta_q, x_uv) / np.trapezoid(delta_q, x_uv))
j_aff = float(i2 * (affine[0] * c2 + affine[1]))
t_exact = float(np.trapezoid(kernel_uv * delta_q, x_uv))
t_loc = float(np.trapezoid(kernel_loc * delta_q, x_uv))
t_res = t_exact - t_loc
t_res_rel = abs(t_res) / max(abs(t_exact), 1.0e-15)

g3_ref_tau = bridge_family("logistic", g3_sm, 0.975, 0.020)
sol_ref = solve_tau(g1_pl, g2_pl, g3_ref_tau)
yt_phys_ref = float(sol_ref.y[2, -1] * np.sqrt(8.0 / 9.0))
dev_ref = (yt_phys_ref - TARGET_YT_PHYS) / TARGET_YT_PHYS * 100.0

a_grid, yt_vals, coeffs, fit = amplitude_scan(g1_pl, g2_pl, g3_sm, g3_ref_tau)
delta = a_grid - 1.0
resid = yt_vals - fit
quad = coeffs[2]
cubic = coeffs[3]
quartic = coeffs[4]
delta_01 = 0.10
quad_at_01 = abs(quad) * delta_01**2
cubic_at_01 = abs(cubic) * delta_01**3
quartic_at_01 = abs(quartic) * delta_01**4
higher_ratio = float(
    np.max(
        np.abs((cubic * delta**3 + quartic * delta**4)[delta != 0.0])
        / np.maximum(np.abs(quad * delta**2)[delta != 0.0], 1.0e-15)
    )
)

print(f"Forced UV window: x >= {uv_cut:.2f}")
print(f"  K_exact(x) ~= {affine[0]:.6e} x + {affine[1]:.6e}")
print(f"  affine-fit max relative error = {kernel_rel_max:.6e}")
print(f"  residual operator norm ratio = {kernel_rel_l2:.6e}")
print()
print("Reference constructive bridge:")
print(f"  y_t(v) = {yt_phys_ref:.6f}")
print(f"  deviation from accepted target = {dev_ref:+.4f}%")
print(f"  I2 = {i2:.6f}")
print(f"  c2 = {c2:.6f}")
print(f"  J_aff = {j_aff:.8f}")
print(f"  exact transport integral = {t_exact:.8f}")
print(f"  local transport integral = {t_loc:.8f}")
print(f"  exact-local residual = {t_res:.8e}")
print(f"  exact-local residual / exact = {t_res_rel:.6e}")
print()
print("Higher-order local correction probe:")
print(f"  c0 = {coeffs[0]:.8f}")
print(f"  c1 = {coeffs[1]:.8f}")
print(f"  c2 = {coeffs[2]:.8f}")
print(f"  c3 = {coeffs[3]:.8f}")
print(f"  c4 = {coeffs[4]:.8f}")
print(f"  |cubic+quartic| / quadratic over |delta|<=0.10 = {higher_ratio:.6e}")
print(f"  RMSE/span = {float(np.sqrt(np.mean(resid**2)) / max(np.max(yt_vals) - np.min(yt_vals), 1e-15)):.6e}")
print()

combined_budget = higher_ratio + kernel_rel_l2

report(
    "1a-kernel-is-positive-and-nearly-affine-on-the-forced-uv-window",
    float(kernel_uv.min()) > 0.0 and kernel_rel_max < 2.0e-2,
    f"kernel min/max = [{kernel_uv.min():.6e}, {kernel_uv.max():.6e}]",
)
report(
    "1b-moment-transport-reduces-to-the-affine-projection",
    abs(t_exact - j_aff) / max(abs(t_exact), 1.0e-15) < 2.0e-3,
    f"|T_exact - J_aff|/|T_exact| = {abs(t_exact - j_aff) / max(abs(t_exact), 1.0e-15):.6e}",
)
report(
    "1c-higher-order-local-corrections-stay-subleading",
    higher_ratio < 1.0e-2,
    f"|cubic+quartic|/quadratic = {higher_ratio:.6e}",
)
report(
    "1d-nonlocal-tail-remains-small",
    kernel_rel_l2 < 1.0e-2,
    f"residual operator norm ratio = {kernel_rel_l2:.6e}",
)
report(
    "1e-reference-transport-law-is-correct-within-the-explicit-budget",
    t_res_rel <= combined_budget * 1.5,
    f"reference residual/exact = {t_res_rel:.6e}, combined budget = {combined_budget:.6e}",
)
report(
    "1f-remainder-budget-remains-microscopic-but-nonzero",
    combined_budget < 2.0e-2,
    f"combined higher-order + nonlocal budget = {combined_budget:.6e}",
)

print()
print("-" * 78)
print("Interpretation")
print("-" * 78)
print("The current package now has a package-native UV->IR transport law on the forced UV")
print("window:")
print()
print("  delta y_t(v) = integral K_loc(x) delta q(x) dx + Delta_higher + Delta_nonlocal")
print()
print("with an affine local kernel on the forced window, an explicit higher-order")
print("tube correction, and an explicit nonlocal tail correction.")
print()
print("This is the strongest honest statement currently supported:")
print("the exact interacting bridge is controlled by a positive local affine")
print("transport kernel on the forced UV window, but the bridge is still not")
print("fully unbounded because the remainder has not been proven to vanish.")
print()
print("If a future theorem kills or fully enumerates the remainder, the same")
print("transport law promotes directly to unbounded closure.")
print()
print("=" * 78)
print(f"FINAL TALLY: {PASS} PASS / {FAIL} FAIL")
print(f"Elapsed: {time.time() - t0:.2f} s")
print("=" * 78)
