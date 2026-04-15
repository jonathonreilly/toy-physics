#!/usr/bin/env python3
"""
y_t Bridge Moment Closure
=========================

Purpose
-------
Reduce the remaining UV-localized bridge problem from a full function of scale
to a two-moment closure on the viable class.

Idea
----
The rearrangement runner established that the accepted endpoint response is
controlled by a positive kernel K(tau) that is monotone stronger toward the
IR. If K is also nearly affine on the viable UV-localized window, then the
weighted endpoint response depends only on two moments of the bridge surplus:

  I_2       = average surplus in g_3^2
  c_2       = UV centroid of that surplus

because

  integral K(tau) delta(g_3^2)(tau) d tau
    ~= a * I_2 + b * I_2 * c_2

inside that window.

This is still bounded support, but it means the remaining selection rule is no
longer about an arbitrary profile. It is about a small weighted moment band.
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


SHAPES = {
    "logistic": shape_logistic,
    "erf": shape_erf,
    "smoothstep": shape_smoothstep,
}


def bridge_family(shape_name: str, g3_sm, center_frac: float, width_frac: float):
    shape = SHAPES[shape_name]
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


print("=" * 78)
print("y_t BRIDGE MOMENT CLOSURE")
print("=" * 78)
print()
print("Fit the accepted response kernel on the viable UV-localized window and")
print("test whether the remaining bridge problem collapses to a two-moment")
print("closure in I2 and the UV centroid.")
print()
t0 = time.time()

g1_v, g2_v = ew_boundary_at_v()
g1_pl, g2_pl = run_ew_upward(g1_v, g2_v)
g3_sm = sm_like_g3_trajectory()
kernel = accepted_kernel(g1_pl, g2_pl, g3_sm)
tau_frac = TAU_GRID / LOG_SPAN

uv_mask = tau_frac >= 0.94
affine = np.polyfit(tau_frac[uv_mask], kernel[uv_mask], 1)
kernel_affine = np.polyval(affine, tau_frac)
max_rel_err = float(np.max(np.abs((kernel_affine[uv_mask] - kernel[uv_mask]) / kernel[uv_mask])))
rms_rel_err = float(np.sqrt(np.mean(((kernel_affine[uv_mask] - kernel[uv_mask]) / kernel[uv_mask]) ** 2)))

rows = []
best_rows = []
for shape_name in SHAPES:
    family_best = None
    for center_frac in np.linspace(0.955, 0.985, 7):
        for width_frac in np.linspace(0.012, 0.026, 8):
            g3_family = bridge_family(shape_name, g3_sm, float(center_frac), float(width_frac))

            def rhs(t, y):
                g1, g2, yt = y
                g3 = g3_family(t)
                return [
                    FAC * (41.0 / 10.0) * g1**3,
                    FAC * (-19.0 / 6.0) * g2**3,
                    FAC
                    * yt
                    * (
                        9.0 / 2.0 * yt**2
                        - 17.0 / 20.0 * g1**2
                        - 9.0 / 4.0 * g2**2
                        - 8.0 * g3**2
                    ),
                ]

            sol = solve_ivp(
                rhs,
                [T_PL, T_V],
                [g1_pl, g2_pl, YT_PL],
                method="RK45",
                rtol=1e-9,
                atol=1e-11,
                max_step=0.2,
            )
            if not sol.success:
                raise RuntimeError(sol.message)

            yt_v_phys = sol.y[2, -1] * np.sqrt(8.0 / 9.0)
            dev_pct = (yt_v_phys - TARGET_YT_PHYS) / TARGET_YT_PHYS * 100.0
            if abs(dev_pct) >= 0.5:
                continue

            g3_vals = np.array([g3_family(t) for t in TS_GRID])
            g3_sm_vals = np.array([g3_sm(t) for t in TS_GRID])
            diff2 = g3_vals**2 - g3_sm_vals**2
            i2 = float(np.trapezoid(diff2, TS_GRID) / LOG_SPAN)
            c2 = float(np.trapezoid(X_GRID * diff2, TS_GRID) / np.trapezoid(diff2, TS_GRID))
            j_aff = float(i2 * (affine[0] * c2 + affine[1]))
            row = {
                "shape": shape_name,
                "center_frac": float(center_frac),
                "width_frac": float(width_frac),
                "dev_pct": float(dev_pct),
                "i2": i2,
                "c2": c2,
                "j_aff": j_aff,
            }
            rows.append(row)
            if family_best is None or abs(dev_pct) < abs(family_best["dev_pct"]):
                family_best = row
    if family_best is not None:
        best_rows.append(family_best)

devs = np.array([r["dev_pct"] for r in rows])
i2_vals = np.array([r["i2"] for r in rows])
c2_vals = np.array([r["c2"] for r in rows])
j_aff_vals = np.array([r["j_aff"] for r in rows])
near_rows = [r for r in rows if abs(r["dev_pct"]) < 0.1]
near_j_aff = np.array([r["j_aff"] for r in near_rows])
best_j_aff = np.array([r["j_aff"] for r in best_rows])

print("Affine kernel fit on the UV-localized window x >= 0.94:")
print(f"  K(x) ~= {affine[0]:.6e} x + {affine[1]:.6e}")
print(f"  max relative error = {max_rel_err:.6e}")
print(f"  rms relative error = {rms_rel_err:.6e}")
print()

print(f"Viable profiles retained inside |dev| < 0.5%: {len(rows)}")
print(f"Near-target profiles retained inside |dev| < 0.1%: {len(near_rows)}")
print()

print("Best row per family:")
print(f"  {'shape':<12s} {'center':>8s} {'width':>8s} {'dev%':>10s} {'I2':>10s} {'c2':>10s} {'J_aff':>12s}")
for row in best_rows:
    print(
        f"  {row['shape']:<12s} {row['center_frac']:8.3f} {row['width_frac']:8.3f} "
        f"{row['dev_pct']:+10.4f} {row['i2']:10.6f} {row['c2']:10.6f} {row['j_aff']:12.8f}"
    )
print()

report(
    "1a-kernel-is-nearly-affine-on-the-uv-window",
    max_rel_err < 3.0e-3,
    f"max relative error = {max_rel_err:.6e}",
)
report(
    "1b-i2-still-controls-endpoint-on-the-viable-class",
    abs(np.corrcoef(i2_vals, devs)[0, 1]) > 0.999,
    f"corr(I2, dev) = {float(np.corrcoef(i2_vals, devs)[0, 1]):+.6f}",
)
report(
    "1c-affine-response-moment-collapses-the-near-target-band",
    float(np.max(near_j_aff) - np.min(near_j_aff)) < 1.0e-4,
    f"|dev|<0.1% rows have J_aff band width = {float(np.max(near_j_aff) - np.min(near_j_aff)):.6e}",
)
report(
    "1d-best-family-rows-share-a-common-response-moment",
    float(np.max(best_j_aff) - np.min(best_j_aff)) < 5.0e-5,
    f"best-family J_aff band width = {float(np.max(best_j_aff) - np.min(best_j_aff)):.6e}",
)
report(
    "1e-centroid-band-stays-tight-on-near-target-rows",
    float(np.max([r['c2'] for r in near_rows]) - np.min([r['c2'] for r in near_rows])) < 1.2e-2,
    f"|dev|<0.1% rows have c2 band width = {float(np.max([r['c2'] for r in near_rows]) - np.min([r['c2'] for r in near_rows])):.6e}",
)

print()
print("-" * 78)
print("Interpretation")
print("-" * 78)
print("On the viable UV-localized window, the accepted response kernel is nearly")
print("affine. So the remaining bridge selection problem is no longer a full")
print("functional problem even in proxy form.")
print()
print("It collapses to a two-moment closure:")
print("  1. the gauge-surplus action I2")
print("  2. the UV centroid c2")
print()
print("Equivalently, the near-target rows share one narrow response-weighted")
print("moment band J_aff = I2 * (a c2 + b) induced by the accepted kernel.")
print()
print("That does not yet derive why the exact lattice bridge picks this band.")
print("But it means the remaining theorem target is a weighted moment-selection")
print("rule, not a free profile-selection problem.")
print()
print("=" * 78)
print(f"FINAL TALLY: {PASS} PASS / {FAIL} FAIL")
print(f"Elapsed: {time.time() - t0:.2f} s")
print("=" * 78)
