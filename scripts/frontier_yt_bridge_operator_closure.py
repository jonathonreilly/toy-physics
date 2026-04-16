#!/usr/bin/env python3
"""
y_t Bridge Operator Closure Proxy
=================================

Purpose
-------
Test whether subleading operator-side deformations can rescue a diffuse
interacting bridge once the exact endpoint data are fixed.

This is a bounded support runner, not the final bridge theorem.

Question
--------
Given:
  - exact endpoints g_3(v), g_3(M_Pl), y_t(M_Pl)
  - a smooth bridge profile for g_3(t)

can wide electroweak-side deformations in g_1(v), g_2(v) repair a diffuse
bridge and bring it back to the accepted low-energy endpoint y_t(v)=0.9176?

If not, the remaining bridge is controlled primarily by the dominant
gauge/Yukawa channel plus UV localization, which is the operator-closure
direction the theorem program actually needs.

Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import sys
import time

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
TARGET_MT_POLE_2L = 172.57
POLE_FACTOR = TARGET_MT_POLE_2L / (TARGET_YT_PHYS * V_DERIVED / np.sqrt(2.0))

ALPHA_EM_MZ = 1.0 / 127.951
SIN2_TW_MZ = 0.23122
ALPHA_1_MZ_GUT = (5.0 / 3.0) * ALPHA_EM_MZ / (1.0 - SIN2_TW_MZ)
ALPHA_2_MZ = ALPHA_EM_MZ / SIN2_TW_MZ

T_V = np.log(V_DERIVED)
T_PL = np.log(M_PL)
LOG_SPAN = T_PL - T_V
FAC = 1.0 / (16.0 * PI**2)


def sigmoid(x: float) -> float:
    x = np.clip(x, -60.0, 60.0)
    return 1.0 / (1.0 + np.exp(-x))


def derived_ew_boundary():
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


def bridge_family(g3_sm, center_frac: float, width_frac: float):
    t_center = T_V + center_frac * LOG_SPAN
    t_width = max(width_frac * LOG_SPAN, 1e-6)
    w_v = sigmoid((T_V - t_center) / t_width)
    w_pl = sigmoid((T_PL - t_center) / t_width)
    norm = w_pl - w_v

    def g3_family(t: float) -> float:
        w = (sigmoid((t - t_center) / t_width) - w_v) / norm
        return g3_sm(t) + w * (lattice_bridge_profile(t) - g3_sm(t))

    return g3_family


def run_profile(center_frac: float, width_frac: float, g1_v: float, g2_v: float, g3_sm):
    g1_pl, g2_pl = run_ew_upward(g1_v, g2_v)
    g3_family = bridge_family(g3_sm, center_frac, width_frac)

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
    yt_v_ward = sol.y[2, -1]
    yt_v_phys = yt_v_ward * np.sqrt(8.0 / 9.0)
    mt_proxy = yt_v_phys * V_DERIVED / np.sqrt(2.0) * POLE_FACTOR
    return yt_v_phys, mt_proxy


def scan_profile(name: str, center_frac: float, width_frac: float, g3_sm, g1_scan, g2_scan):
    rows = []
    for g1_v in g1_scan:
        for g2_v in g2_scan:
            yt_v_phys, mt_proxy = run_profile(center_frac, width_frac, g1_v, g2_v, g3_sm)
            rows.append(
                {
                    "g1_v": g1_v,
                    "g2_v": g2_v,
                    "yt_v_phys": yt_v_phys,
                    "mt_proxy": mt_proxy,
                    "dev_pct": (yt_v_phys - TARGET_YT_PHYS) / TARGET_YT_PHYS * 100.0,
                }
            )

    rows_sorted = sorted(rows, key=lambda r: abs(r["dev_pct"]))
    best = rows_sorted[0]
    worst = max(rows, key=lambda r: abs(r["dev_pct"]))
    print(f"{name}:")
    print(
        f"  best  : g1(v)={best['g1_v']:.4f}, g2(v)={best['g2_v']:.4f}, "
        f"y_t(v)={best['yt_v_phys']:.6f}, dev={best['dev_pct']:+.2f}%, "
        f"m_t~{best['mt_proxy']:.2f} GeV"
    )
    print(
        f"  worst : g1(v)={worst['g1_v']:.4f}, g2(v)={worst['g2_v']:.4f}, "
        f"y_t(v)={worst['yt_v_phys']:.6f}, dev={worst['dev_pct']:+.2f}%"
    )
    return rows


print("=" * 78)
print("y_t BRIDGE OPERATOR CLOSURE PROXY")
print("=" * 78)
print()
print("Test whether wide EW-side deformations can rescue a diffuse bridge once")
print("the exact endpoint data are fixed.")
print()
t0 = time.time()

g1_derived, g2_derived = derived_ew_boundary()
g3_sm = sm_like_g3_trajectory()

print("Derived reference boundary:")
print(f"  g_1(v) = {g1_derived:.6f}")
print(f"  g_2(v) = {g2_derived:.6f}")
print(f"  target y_t(v, physical) = {TARGET_YT_PHYS:.4f}")
print()

g1_scan = np.linspace(0.30, 0.60, 7)
g2_scan = np.linspace(0.40, 0.90, 6)

print("EW scan window:")
print(f"  g_1(v) in [{g1_scan[0]:.2f}, {g1_scan[-1]:.2f}]")
print(f"  g_2(v) in [{g2_scan[0]:.2f}, {g2_scan[-1]:.2f}]")
print()

diffuse_rows = scan_profile("Diffuse bridge (center=0.75, width=0.05)", 0.75, 0.05, g3_sm, g1_scan, g2_scan)
print()
localized_rows = scan_profile("UV-localized bridge (center=0.97, width=0.02)", 0.97, 0.02, g3_sm, g1_scan, g2_scan)
print()

diffuse_best = min(diffuse_rows, key=lambda r: abs(r["dev_pct"]))
localized_best = min(localized_rows, key=lambda r: abs(r["dev_pct"]))

diffuse_span = max(r["yt_v_phys"] for r in diffuse_rows) - min(r["yt_v_phys"] for r in diffuse_rows)
localized_span = max(r["yt_v_phys"] for r in localized_rows) - min(r["yt_v_phys"] for r in localized_rows)

report(
    "1a-diffuse-not-rescued",
    abs(diffuse_best["dev_pct"]) > 5.0,
    f"best diffuse profile still misses target by {diffuse_best['dev_pct']:+.2f}%",
)

report(
    "1b-localized-stays-close",
    abs(localized_best["dev_pct"]) < 1.0,
    f"best localized profile lands at {localized_best['dev_pct']:+.2f}%",
)

report(
    "1c-ew-cannot-mimic-localization",
    abs(diffuse_best["dev_pct"]) > 5.0 and abs(localized_best["dev_pct"]) < 1.0,
    f"even after EW scan, diffuse best={diffuse_best['dev_pct']:+.2f}% while localized best={localized_best['dev_pct']:+.2f}%",
)

report(
    "1d-localization-dominates-subleading-operators",
    abs(diffuse_best["dev_pct"]) - abs(localized_best["dev_pct"]) > 4.0,
    f"best diffuse vs localized gap in |dev| = {abs(diffuse_best['dev_pct']) - abs(localized_best['dev_pct']):.2f} percentage points",
)

print()
print("-" * 78)
print("Interpretation")
print("-" * 78)
print("Within this proxy, wide EW-side deformations do not rescue a diffuse bridge.")
print("The dominant control parameter is still where the lattice correction enters")
print("the gauge/Yukawa transport. That supports an operator-closure reading:")
print()
print("  the missing bridge is not being hidden in broad electroweak-side")
print("  operator freedom; the theorem target really is the dominant")
print("  gauge/Yukawa bridge structure plus UV localization.")
print()
print("This is still bounded support, not full closure.")

elapsed = time.time() - t0
print()
print("=" * 78)
print(f"FINAL TALLY: {PASS} PASS / {FAIL} FAIL")
print(f"Elapsed: {elapsed:.2f} s")
print("=" * 78)

if FAIL:
    sys.exit(1)
