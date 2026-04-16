#!/usr/bin/env python3
"""
y_t Interacting Bridge Locality Proxy
=====================================

Purpose
-------
Scan a controlled family of smooth bridge profiles between:

1. the SM-like gauge trajectory anchored by the derived low-energy
   `alpha_s(v)`, and
2. the lattice-side UV endpoint `g_3(M_Pl) = sqrt(4 pi alpha_LM)`.

Every profile in the family satisfies the exact endpoint data:

- `g_3(v)` fixed by the coupling-map theorem
- `g_3(M_Pl)` fixed by the lattice coupling
- `y_t(M_Pl) = g_3(M_Pl) / sqrt(6)` from the Ward identity

This is not the final bridge theorem. It is a bounded proxy asking a narrower
question:

  If the true interacting bridge is a smooth deformation between the SM-like
  transport and the lattice UV endpoint, how localized must that deformation
  be in log-scale to preserve the accepted low-energy `y_t(v)`?

Headline result
---------------
Diffuse bridge profiles overshoot the accepted `y_t(v) = 0.9176` badly.
Profiles that stay within 1% of the accepted central value exist only when the
lattice correction is concentrated in the top few percent of the `log(mu)`
interval near `M_Pl`.

So this runner does not unbound the lane. It sharpens the remaining target:
the successful interacting bridge must be strongly UV-localized / SM-like over
most of `[v, M_Pl]`.

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
    # One-loop proxy is enough here because the question is bridge locality,
    # not the final precision top mass.
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
    # Log-linear bridge between the exact endpoints.
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


def run_family(center_frac: float, width_frac: float, g1_pl: float, g2_pl: float, g3_sm):
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
    mt_pole_proxy = yt_v_phys * V_DERIVED / np.sqrt(2.0) * POLE_FACTOR
    return {
        "center_frac": center_frac,
        "width_frac": width_frac,
        "yt_v_ward": yt_v_ward,
        "yt_v_phys": yt_v_phys,
        "mt_pole_proxy": mt_pole_proxy,
        "dev_pct": (yt_v_phys - TARGET_YT_PHYS) / TARGET_YT_PHYS * 100.0,
        "g3_v": g3_family(T_V),
        "g3_pl": g3_family(T_PL),
    }


print("=" * 78)
print("y_t INTERACTING BRIDGE LOCALITY PROXY")
print("=" * 78)
print()
print("Scan smooth UV-to-IR bridge profiles satisfying exact endpoint data:")
print(f"  g_3(v)     = {G3_V:.6f}")
print(f"  g_3(M_Pl)  = {G3_PL:.6f}")
print(f"  y_t(M_Pl)  = {YT_PL:.6f}  [Ward identity]")
print(f"  target y_t(v, physical) = {TARGET_YT_PHYS:.4f}")
print()
t0 = time.time()

g1_v, g2_v = ew_boundary_at_v()
g1_pl, g2_pl = run_ew_upward(g1_v, g2_v)
g3_sm = sm_like_g3_trajectory()

print("Boundary summary:")
print(f"  g_1(v) = {g1_v:.6f}, g_2(v) = {g2_v:.6f}")
print(f"  g_1(M_Pl) = {g1_pl:.6f}, g_2(M_Pl) = {g2_pl:.6f}")
print(f"  SM-like g_3(M_Pl) from low-energy anchor = {g3_sm(T_PL):.6f}")
print(f"  lattice-side g_3(M_Pl) endpoint          = {G3_PL:.6f}")
print(f"  UV endpoint ratio lattice/SM-like        = {G3_PL / g3_sm(T_PL):.3f}")
print()

center_grid = [0.45, 0.55, 0.65, 0.75, 0.85, 0.92, 0.95, 0.97, 0.98, 0.99]
width_grid = [0.01, 0.02, 0.03, 0.05, 0.10, 0.15, 0.22]

rows = []
for center_frac in center_grid:
    for width_frac in width_grid:
        rows.append(run_family(center_frac, width_frac, g1_pl, g2_pl, g3_sm))

print("-" * 78)
print("Representative scan rows")
print("-" * 78)
print(f"  {'center':>8s} {'width':>8s} {'y_t(phys)':>12s} {'dev%':>10s} {'m_t proxy':>12s}")
for row in sorted(rows, key=lambda r: (r["center_frac"], r["width_frac"])):
    if row["center_frac"] in {0.45, 0.75, 0.92, 0.97, 0.99} and row["width_frac"] in {0.02, 0.05, 0.15}:
        print(
            f"  {row['center_frac']:8.2f} {row['width_frac']:8.2f} "
            f"{row['yt_v_phys']:12.6f} {row['dev_pct']:+10.2f} "
            f"{row['mt_pole_proxy']:12.2f}"
        )
print()

rows_sorted = sorted(rows, key=lambda r: abs(r["dev_pct"]))
best = rows_sorted[:10]

print("Best-fit smooth profiles:")
print(f"  {'center':>8s} {'width':>8s} {'y_t(phys)':>12s} {'dev%':>10s} {'m_t proxy':>12s}")
for row in best:
    print(
        f"  {row['center_frac']:8.2f} {row['width_frac']:8.2f} "
        f"{row['yt_v_phys']:12.6f} {row['dev_pct']:+10.2f} "
        f"{row['mt_pole_proxy']:12.2f}"
    )
print()

within_1pct = [r for r in rows if abs(r["dev_pct"]) < 1.0]
within_3pct = [r for r in rows if abs(r["dev_pct"]) < 3.0]
diffuse_bad = [r for r in rows if r["center_frac"] <= 0.85]
uv_localized = [
    r
    for r in rows
    if r["center_frac"] >= 0.95 and r["width_frac"] <= 0.05
]

print("Window summary:")
print(f"  Profiles scanned: {len(rows)}")
print(f"  Within 1% of accepted y_t(v): {len(within_1pct)}")
print(f"  Within 3% of accepted y_t(v): {len(within_3pct)}")
if within_1pct:
    min_center_1pct = min(r["center_frac"] for r in within_1pct)
    max_width_1pct = max(r["width_frac"] for r in within_1pct)
    print(f"  Smallest center fraction among 1% profiles: {min_center_1pct:.2f}")
    print(f"  Largest width fraction among 1% profiles: {max_width_1pct:.2f}")
else:
    print("  No 1% profiles found in scan.")
print()

report(
    "1a-endpoints-preserved",
    all(abs(r["g3_v"] - G3_V) < 1e-10 and abs(r["g3_pl"] - G3_PL) < 1e-10 for r in rows),
    "all scanned bridge families preserve exact g_3(v) and g_3(M_Pl) endpoints",
)

report(
    "1b-diffuse-bridges-overshoot",
    all(r["dev_pct"] > 5.0 for r in diffuse_bad),
    "all diffuse / early bridge profiles overshoot accepted y_t(v) by more than 5%",
)

report(
    "1c-uv-localized-window-exists",
    len(within_1pct) > 0 and all(r["center_frac"] >= 0.95 and r["width_frac"] <= 0.03 for r in within_1pct),
    "profiles within 1% exist only in the UV-localized window center>=0.95, width<=0.03",
)

report(
    "1d-best-profile-near-target",
    abs(best[0]["dev_pct"]) < 0.5,
    f"best smooth profile gives y_t(v)={best[0]['yt_v_phys']:.6f} ({best[0]['dev_pct']:+.2f}%)",
)

print()
print("-" * 78)
print("Interpretation")
print("-" * 78)
print("This proxy does NOT prove the final bridge theorem.")
print("It does show a sharper structural fact:")
print()
print("  A successful interacting bridge cannot be a broad deformation of the")
print("  SM-like transport over the full [v, M_Pl] interval.")
print()
print("  To preserve the accepted low-energy y_t endpoint, the lattice-side")
print("  correction must be concentrated in a narrow UV window near M_Pl,")
print("  leaving the bridge SM-like over most of the interval.")
print()
print("That materially narrows the remaining theorem target.")

elapsed = time.time() - t0
print()
print("=" * 78)
print(f"FINAL TALLY: {PASS} PASS / {FAIL} FAIL")
print(f"Elapsed: {elapsed:.2f} s")
print("=" * 78)

if FAIL:
    sys.exit(1)
