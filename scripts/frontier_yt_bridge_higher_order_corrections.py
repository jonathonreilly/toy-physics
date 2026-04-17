#!/usr/bin/env python3
"""
y_t Bridge Higher-Order Corrections
===================================

Probe the next correction layer above the local-Hessian selector.

The previous branch result identified a positive local quadratic selector on
the forced UV-localized bridge window. This runner asks whether the next local
corrections, organized as cubic and quartic terms around the viable bridge
family, remain parametrically small.

Method
------
1. Reconstruct the viable UV-localized bridge family.
2. Pick the best representative bridge profile from the constructive scan.
3. Scale that bridge surplus by a one-parameter amplitude `a` around the
   selector point `a = 1`.
4. Fit the accepted low-energy endpoint `y_t(v)` as a polynomial in
   `delta = a - 1`.
5. Compare the cubic and quartic contributions to the quadratic leading term
   on a small neighborhood around the selector.

This is intentionally narrow. It does not try to prove the exact microscopic
selector. It only checks whether the higher-order local corrections above the
quadratic selector stay subleading on the viable bridge family.
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


def endpoint_yt_phys(g1_pl: float, g2_pl: float, g3_family) -> float:
    sol = solve_tau(g1_pl, g2_pl, g3_family)
    return float(sol.y[2, -1] * np.sqrt(8.0 / 9.0))


def best_constructive_bridge(g1_pl: float, g2_pl: float, g3_sm):
    best = None
    family_rows = []
    for shape_name in SHAPES:
        family_best = None
        for center_frac in np.linspace(0.955, 0.985, 7):
            for width_frac in np.linspace(0.012, 0.026, 8):
                g3_family = bridge_family(shape_name, g3_sm, float(center_frac), float(width_frac))
                yt_phys = endpoint_yt_phys(g1_pl, g2_pl, g3_family)
                dev_pct = (yt_phys - TARGET_YT_PHYS) / TARGET_YT_PHYS * 100.0
                row = {
                    "shape": shape_name,
                    "center_frac": float(center_frac),
                    "width_frac": float(width_frac),
                    "yt_phys": yt_phys,
                    "dev_pct": dev_pct,
                }
                if family_best is None or abs(dev_pct) < abs(family_best["dev_pct"]):
                    family_best = row
        family_rows.append(family_best)
        if best is None or abs(family_best["dev_pct"]) < abs(best["dev_pct"]):
            best = family_best
    return best, family_rows


def amplitude_scan(g1_pl: float, g2_pl: float, g3_sm, g3_ref):
    a_grid = np.linspace(0.90, 1.10, 21)
    yt_vals = []
    for a in a_grid:
        def g3_amp(t):
            return g3_sm(t) + float(a) * (g3_ref(t) - g3_sm(t))

        yt_vals.append(endpoint_yt_phys(g1_pl, g2_pl, g3_amp))
    yt_vals = np.array(yt_vals)
    delta = a_grid - 1.0
    coeffs = np.polynomial.polynomial.polyfit(delta, yt_vals, 4)
    fit = np.polynomial.polynomial.polyval(delta, coeffs)
    return a_grid, yt_vals, coeffs, fit


print("=" * 78)
print("y_t BRIDGE HIGHER-ORDER CORRECTIONS")
print("=" * 78)
print()
print(
    "Probe whether cubic and quartic local corrections stay parametrically small "
    "around the current UV-localized selector."
)
print()
t0 = time.time()

g1_v, g2_v = ew_boundary_at_v()
g1_pl, g2_pl = run_ew_upward(g1_v, g2_v)
g3_sm = sm_like_g3_trajectory()

best, family_rows = best_constructive_bridge(g1_pl, g2_pl, g3_sm)
g3_ref = bridge_family(best["shape"], g3_sm, best["center_frac"], best["width_frac"])
a_grid, yt_vals, coeffs, fit = amplitude_scan(g1_pl, g2_pl, g3_sm, g3_ref)
delta = a_grid - 1.0
resid = yt_vals - fit

quad = coeffs[2]
cubic = coeffs[3]
quartic = coeffs[4]

delta_probe = np.linspace(-0.10, 0.10, 81)
quad_term = quad * delta_probe**2
cubic_term = cubic * delta_probe**3
quartic_term = quartic * delta_probe**4
tail_term = cubic_term + quartic_term
ratio = np.max(np.abs(tail_term[delta_probe != 0.0]) / np.maximum(np.abs(quad_term[delta_probe != 0.0]), 1e-15))

rmse = float(np.sqrt(np.mean(resid**2)))
span = float(np.max(yt_vals) - np.min(yt_vals))
rmse_rel_span = rmse / max(span, 1e-15)

delta_01 = 0.10
quad_at_01 = abs(quad) * delta_01**2
cubic_at_01 = abs(cubic) * delta_01**3
quartic_at_01 = abs(quartic) * delta_01**4

print(f"Best constructive UV bridge: {best['shape']} center={best['center_frac']:.3f} width={best['width_frac']:.3f}")
print(f"  y_t(v) = {best['yt_phys']:.6f}")
print(f"  deviation = {best['dev_pct']:+.4f}%")
print()

print("Amplitude expansion around the selector point a = 1:")
print(
    "  y_t(a) = c0 + c1*δ + c2*δ^2 + c3*δ^3 + c4*δ^4, with δ = a - 1"
)
print(f"  c0 = {coeffs[0]:.8f}")
print(f"  c1 = {coeffs[1]:.8f}")
print(f"  c2 = {coeffs[2]:.8f}")
print(f"  c3 = {coeffs[3]:.8f}")
print(f"  c4 = {coeffs[4]:.8f}")
print()
print("Local correction sizes at |δ| = 0.10:")
print(f"  quadratic magnitude = {quad_at_01:.6e}")
print(f"  cubic magnitude     = {cubic_at_01:.6e}")
print(f"  quartic magnitude   = {quartic_at_01:.6e}")
print(f"  |cubic+quartic| / quadratic = {ratio:.6e}")
print()
print("Fit quality:")
print(f"  RMSE = {rmse:.6e}")
print(f"  RMSE / span = {rmse_rel_span:.6e}")
print()

report(
    "1a-best-constructive-bridge-still-close-to-the-accepted-endpoint",
    abs(best["dev_pct"]) < 0.1,
    f"best deviation = {best['dev_pct']:+.4f}%",
)
report(
    "1b-quadratic-leading-piece-remains-the-dominant-local-term",
    ratio < 0.10,
    f"max |cubic+quartic|/quadratic over |δ|<=0.10 = {ratio:.6e}",
)
report(
    "1c-cubic-term-is-parametrically-small-at-10-percent-amplitude",
    cubic_at_01 / max(quad_at_01, 1e-15) < 0.05,
    f"|cubic|/quadratic at |δ|=0.10 = {cubic_at_01 / max(quad_at_01, 1e-15):.6e}",
)
report(
    "1d-quartic-term-is-parametrically-smaller-still-at-10-percent-amplitude",
    quartic_at_01 / max(quad_at_01, 1e-15) < 0.01,
    f"|quartic|/quadratic at |δ|=0.10 = {quartic_at_01 / max(quad_at_01, 1e-15):.6e}",
)
report(
    "1e-fourth-order-fit-reconstructs-the-amplitude-scan-well",
    rmse_rel_span < 1.0e-2,
    f"RMSE/span = {rmse_rel_span:.6e}",
)

print()
print("-" * 78)
print("Interpretation")
print("-" * 78)
if ratio < 0.10 and cubic_at_01 / max(quad_at_01, 1e-15) < 0.05 and quartic_at_01 / max(quad_at_01, 1e-15) < 0.01:
    print(
        "On the viable UV-localized bridge family, the quadratic selector still "
        "dominates. The cubic correction is small and the quartic correction is "
        "smaller still on a 10% amplitude tube around the selector."
    )
    print(
        "So the higher-order local corrections are parametrically subleading at "
        "the level probed here, and the local-Hessian picture remains the right "
        "leading description."
    )
else:
    print(
        "On the viable UV-localized bridge family, higher-order corrections are "
        "not negligible enough to call the quadratic selector uniformly dominant."
    )
    print(
        "The leading Hessian picture still organizes the bridge, but cubic and "
        "quartic corrections must be treated as quantitatively important on this "
        "probe window."
    )

print()
print("This is a bounded-support result: it quantifies higher-order corrections")
print("around the current selector, but it does not prove the exact microscopic")
print("origin of the selector or remove the residual y_t bound.")
print()
print("=" * 78)
print(f"FINAL TALLY: {PASS} PASS / {FAIL} FAIL")
print(f"Elapsed: {time.time() - t0:.2f} s")
print("=" * 78)
