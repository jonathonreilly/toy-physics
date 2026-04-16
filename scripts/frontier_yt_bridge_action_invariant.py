#!/usr/bin/env python3
"""
y_t Bridge Action Invariant
===========================

Purpose
-------
Reduce the constructive UV-localized bridge class to a small set of
shape-invariant quantitative descriptors.

Key claim tested here
---------------------
Within the viable UV-localized bridge class, the low-energy endpoint is
controlled almost entirely by the normalized gauge-surplus action

    I_2 := (1 / Delta t) * integral_{v}^{M_Pl} (g_3(t)^2 - g_3,SM(t)^2) dt

rather than by arbitrary profile details.

If true, the remaining theorem target becomes:

  derive why the exact interacting bridge selects the observed action
  invariant and UV centroid

instead of:

  derive an arbitrary full function of t.
"""

from __future__ import annotations

import sys
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


def ew_boundary_at_v():
    b1 = -41.0 / 10.0
    b2 = 19.0 / 6.0
    L_v_MZ = T_V - np.log(M_Z)
    inv_a1_v = 1.0 / ALPHA_1_MZ_GUT + b1 / (2.0 * PI) * L_v_MZ
    inv_a2_v = 1.0 / ALPHA_2_MZ + b2 / (2.0 * PI) * L_v_MZ
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


def run_profile(shape_name: str, center_frac: float, width_frac: float, g1_pl: float, g2_pl: float, g3_sm):
    g3_family = bridge_family(shape_name, g3_sm, center_frac, width_frac)

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
    ts = np.linspace(T_V, T_PL, 1000)
    x = (ts - T_V) / LOG_SPAN
    g3_vals = np.array([g3_family(t) for t in ts])
    g3_sm_vals = np.array([g3_sm(t) for t in ts])
    diff = g3_vals - g3_sm_vals
    diff2 = g3_vals**2 - g3_sm_vals**2
    action_1 = np.trapezoid(diff, ts) / LOG_SPAN
    action_2 = np.trapezoid(diff2, ts) / LOG_SPAN
    centroid_1 = np.trapezoid(x * diff, ts) / np.trapezoid(diff, ts)
    centroid_2 = np.trapezoid(x * diff2, ts) / np.trapezoid(diff2, ts)
    return {
        "shape": shape_name,
        "center_frac": center_frac,
        "width_frac": width_frac,
        "yt_v_phys": yt_v_phys,
        "dev_pct": (yt_v_phys - TARGET_YT_PHYS) / TARGET_YT_PHYS * 100.0,
        "action_1": action_1,
        "action_2": action_2,
        "centroid_1": centroid_1,
        "centroid_2": centroid_2,
    }


def corrcoef(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.corrcoef(x, y)[0, 1])


print("=" * 78)
print("y_t BRIDGE ACTION INVARIANT")
print("=" * 78)
print()
print("Scan the constructive UV-localized bridge class and test whether the")
print("low-energy endpoint collapses onto a small set of bridge invariants.")
print()
t0 = time.time()

g1_v, g2_v = ew_boundary_at_v()
g1_pl, g2_pl = run_ew_upward(g1_v, g2_v)
g3_sm = sm_like_g3_trajectory()

rows = []
family_summaries = {}
for shape_name in SHAPES:
    family_rows = []
    for center_frac in np.linspace(0.955, 0.985, 7):
        for width_frac in np.linspace(0.012, 0.026, 8):
            row = run_profile(shape_name, float(center_frac), float(width_frac), g1_pl, g2_pl, g3_sm)
            if abs(row["dev_pct"]) < 0.5:
                rows.append(row)
                family_rows.append(row)
    family_rows_sorted = sorted(family_rows, key=lambda r: r["action_2"])
    diffs = np.diff([r["yt_v_phys"] for r in family_rows_sorted])
    family_summaries[shape_name] = {
        "count": len(family_rows_sorted),
        "violations": int(np.sum(diffs < -1e-6)),
        "i2_min": min(r["action_2"] for r in family_rows_sorted),
        "i2_max": max(r["action_2"] for r in family_rows_sorted),
    }

devs = np.array([r["dev_pct"] for r in rows])
action_1 = np.array([r["action_1"] for r in rows])
action_2 = np.array([r["action_2"] for r in rows])
centroid_1 = np.array([r["centroid_1"] for r in rows])
centroid_2 = np.array([r["centroid_2"] for r in rows])

print(f"Profiles retained inside |dev| < 0.5%: {len(rows)}")
print()

print("Invariant statistics on the viable class:")
print(f"  action_1 mean/std/cv = {action_1.mean():.6f} / {action_1.std():.6f} / {action_1.std() / action_1.mean() * 100:.2f}%")
print(f"  action_2 mean/std/cv = {action_2.mean():.6f} / {action_2.std():.6f} / {action_2.std() / action_2.mean() * 100:.2f}%")
print(f"  centroid_1 mean/std  = {centroid_1.mean():.6f} / {centroid_1.std():.6f}")
print(f"  centroid_2 mean/std  = {centroid_2.mean():.6f} / {centroid_2.std():.6f}")
print()

print("Correlation with endpoint deviation:")
print(f"  corr(action_1, dev)   = {corrcoef(action_1, devs):+.6f}")
print(f"  corr(action_2, dev)   = {corrcoef(action_2, devs):+.6f}")
print(f"  corr(centroid_1, dev) = {corrcoef(centroid_1, devs):+.6f}")
print(f"  corr(centroid_2, dev) = {corrcoef(centroid_2, devs):+.6f}")
print()

print("Per-family monotonicity in I2:")
for shape_name, summary in family_summaries.items():
    print(
        f"  {shape_name:<12s} rows={summary['count']:3d} "
        f"violations={summary['violations']:2d} "
        f"I2 range=[{summary['i2_min']:.6f}, {summary['i2_max']:.6f}]"
    )
print()

rows_sorted = sorted(rows, key=lambda r: abs(r["dev_pct"]))
print("Closest viable rows:")
print(f"  {'shape':<12s} {'center':>8s} {'width':>8s} {'dev%':>10s} {'I2':>10s} {'c2':>10s}")
for row in rows_sorted[:10]:
    print(
        f"  {row['shape']:<12s} {row['center_frac']:8.3f} {row['width_frac']:8.3f} "
        f"{row['dev_pct']:+10.4f} {row['action_2']:10.6f} {row['centroid_2']:10.6f}"
    )
print()

report(
    "1a-action2-dominates-endpoint",
    abs(corrcoef(action_2, devs)) > 0.99,
    f"corr(action_2, dev) = {corrcoef(action_2, devs):+.6f}",
)

report(
    "1b-viable-class-has-tight-uv-centroid",
    centroid_2.std() < 0.01,
    f"centroid_2 = {centroid_2.mean():.6f} +/- {centroid_2.std():.6f}",
)

report(
    "1c-viable-class-has-finite-action-band",
    action_2.std() / action_2.mean() < 0.15,
    f"action_2 coefficient of variation = {action_2.std() / action_2.mean() * 100:.2f}%",
)

report(
    "1d-best-rows-collapse-near-common-I2",
    max(abs(r["action_2"] - rows_sorted[0]["action_2"]) for r in rows_sorted[:10]) < 0.001,
    f"top-10 action_2 band width = {max(abs(r['action_2'] - rows_sorted[0]['action_2']) for r in rows_sorted[:10]):.6f}",
)

report(
    "1e-I2-ordering-is-nearly-family-monotone",
    all(summary["violations"] <= 3 for summary in family_summaries.values()),
    "; ".join(f"{shape}: violations={summary['violations']}" for shape, summary in family_summaries.items()),
)

near_target_rows = [r for r in rows if abs(r["dev_pct"]) < 0.1]
near_i2 = np.array([r["action_2"] for r in near_target_rows])
report(
    "1f-near-target-rows-share-common-I2-band",
    (near_i2.max() - near_i2.min()) < 0.003,
    f"|dev|<0.1% rows have I2 band width = {near_i2.max() - near_i2.min():.6f}",
)

print()
print("-" * 78)
print("Interpretation")
print("-" * 78)
print("Inside the constructive UV-localized class, the endpoint is not being")
print("set by arbitrary profile details. It is overwhelmingly controlled by a")
print("single bridge functional, the normalized gauge-surplus action I2, plus")
print("a tight UV centroid.")
print()
print("That means the remaining theorem problem can be stated more sharply:")
print()
print("  derive why the exact interacting bridge selects the observed action")
print("  invariant and UV centroid, rather than derive an arbitrary function")
print("  of scale.")

elapsed = time.time() - t0
print()
print("=" * 78)
print(f"FINAL TALLY: {PASS} PASS / {FAIL} FAIL")
print(f"Elapsed: {elapsed:.2f} s")
print("=" * 78)

if FAIL:
    sys.exit(1)
