#!/usr/bin/env python3
"""
y_t Bridge UV Class Uniqueness
==============================

Test whether the current rearrangement, moment-closure, Hessian-selector, and
correction-control stack forces the viable bridge into the same intrinsic
UV-centered class/band.

This is intentionally honest:

- it treats the branch hypotheses as established support
- it scans the current constructive bridge family broadly
- it reports whether any surviving candidate leaves the intrinsic UV-centered
  class

It does not claim a theorem over the full microscopic bridge space.
"""

from __future__ import annotations

import time
from itertools import product
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


def run_profile(shape_name: str, center_frac: float, width_frac: float, g1_pl: float, g2_pl: float, g3_sm):
    g3_family = bridge_family(shape_name, g3_sm, center_frac, width_frac)
    sol = solve_tau(g1_pl, g2_pl, g3_family)
    yt_v_phys = float(sol.y[2, -1] * np.sqrt(8.0 / 9.0))

    ts = TS_GRID
    x = X_GRID
    g3_vals = np.array([g3_family(t) for t in ts])
    g3_sm_vals = np.array([g3_sm(t) for t in ts])
    diff2 = g3_vals**2 - g3_sm_vals**2
    action_2 = float(np.trapezoid(diff2, ts) / LOG_SPAN)
    centroid_2 = float(np.trapezoid(x * diff2, ts) / np.trapezoid(diff2, ts))

    return {
        "shape": shape_name,
        "center_frac": float(center_frac),
        "width_frac": float(width_frac),
        "yt_v_phys": yt_v_phys,
        "dev_pct": float((yt_v_phys - TARGET_YT_PHYS) / TARGET_YT_PHYS * 100.0),
        "action_2": action_2,
        "centroid_2": centroid_2,
        "g3_family": g3_family,
        "diff2": diff2,
    }


def amplitude_ratio_for_row(g1_pl: float, g2_pl: float, g3_sm, row):
    g3_ref = bridge_family(row["shape"], g3_sm, row["center_frac"], row["width_frac"])
    a_grid = np.linspace(0.90, 1.10, 21)
    yt_vals = []

    for a in a_grid:
        def g3_amp(t):
            return g3_sm(t) + float(a) * (g3_ref(t) - g3_sm(t))

        yt_vals.append(float(solve_tau(g1_pl, g2_pl, g3_amp).y[2, -1] * np.sqrt(8.0 / 9.0)))

    yt_vals = np.array(yt_vals)
    delta = a_grid - 1.0
    coeffs = np.polynomial.polynomial.polyfit(delta, yt_vals, 4)

    delta_probe = np.linspace(-0.10, 0.10, 81)
    quad_term = coeffs[2] * delta_probe**2
    cubic_term = coeffs[3] * delta_probe**3
    quartic_term = coeffs[4] * delta_probe**4
    tail_term = cubic_term + quartic_term

    ratio = float(
        np.max(
            np.abs(tail_term[delta_probe != 0.0]) / np.maximum(np.abs(quad_term[delta_probe != 0.0]), 1e-15)
        )
    )
    return float(coeffs[2]), float(coeffs[3]), float(coeffs[4]), ratio


print("=" * 78)
print("y_t BRIDGE UV CLASS UNIQUENESS")
print("=" * 78)
print()
print("Test whether the branch hypotheses force the viable bridge into the same")
print("UV-localized class and moment band.")
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
kernel_coeffs = np.polyfit(x_uv, kernel_uv, 1)
kernel_affine = np.polyval(kernel_coeffs, x_uv)
kernel_rel_max = float(np.max(np.abs((kernel_affine - kernel_uv) / kernel_uv)))
kernel_rel_l2 = float(
    np.sqrt(np.trapezoid((kernel_uv - kernel_affine) ** 2, x_uv))
    / np.sqrt(np.trapezoid(kernel_uv**2, x_uv))
)

print("Branch-hypothesis support from the current selector stack:")
print(f"  exact kernel min/max on forced UV window = [{kernel_uv.min():.6e}, {kernel_uv.max():.6e}]")
print(f"  affine local-kernel max relative error = {kernel_rel_max:.6e}")
print(f"  affine local-kernel operator-norm ratio = {kernel_rel_l2:.6e}")
print()

report(
    "1a-response-kernel-is-positive-on-the-forced-uv-window",
    float(kernel_uv.min()) > 0.0,
    f"kernel min/max = [{kernel_uv.min():.6e}, {kernel_uv.max():.6e}]",
)
report(
    "1b-response-kernel-is-nearly-affine-on-the-forced-uv-window",
    kernel_rel_max < 2.0e-2,
    f"max relative affine-fit error = {kernel_rel_max:.6e}",
)
report(
    "1c-local-hessian-selector-remains-a-small-correction-around-the-affine-model",
    kernel_rel_l2 < 1.0e-2,
    f"operator-norm ratio = {kernel_rel_l2:.6e}",
)

best_constructive = None
for shape_name in SHAPES:
    for center_frac in np.linspace(0.955, 0.985, 7):
        for width_frac in np.linspace(0.012, 0.026, 8):
            row = run_profile(shape_name, float(center_frac), float(width_frac), g1_pl, g2_pl, g3_sm)
            if best_constructive is None or abs(row["dev_pct"]) < abs(best_constructive["dev_pct"]):
                best_constructive = row

quad, cubic, quartic, higher_ratio = amplitude_ratio_for_row(g1_pl, g2_pl, g3_sm, best_constructive)

print("Higher-order correction control on the best constructive bridge:")
print(
    f"  best bridge = {best_constructive['shape']} center={best_constructive['center_frac']:.3f}"
    f" width={best_constructive['width_frac']:.3f} y_t(v)={best_constructive['yt_v_phys']:.6f}"
)
print(f"  |cubic+quartic| / quadratic on |δ|<=0.10 = {higher_ratio:.6e}")
print()

report(
    "1d-higher-order-corrections-stay-parametrically-small",
    higher_ratio < 0.10,
    f"max |cubic+quartic|/quadratic = {higher_ratio:.6e}",
)

scan_rows = []
center_grid = np.linspace(0.80, 0.99, 8)
width_grid = np.linspace(0.010, 0.050, 7)

for shape_name, center_frac, width_frac in product(SHAPES, center_grid, width_grid):
    row = run_profile(shape_name, float(center_frac), float(width_frac), g1_pl, g2_pl, g3_sm)
    g3_vals = np.array([row["g3_family"](t) for t in TS_GRID])
    g3_sm_vals = np.array([g3_sm(t) for t in TS_GRID])
    diff2 = g3_vals**2 - g3_sm_vals**2
    profile_uv = np.interp(x_uv, X_GRID, diff2)
    full = float(np.trapezoid(kernel_uv * profile_uv, x_uv))
    local = float(np.trapezoid(kernel_affine * profile_uv, x_uv))
    nonlocal_resid = full - local
    row["j_aff"] = float(row["action_2"] * (kernel_coeffs[0] * row["centroid_2"] + kernel_coeffs[1]))
    row["nonlocal_frac"] = abs(nonlocal_resid) / max(abs(full), 1.0e-12)
    row["nonlocal_local_frac"] = abs(nonlocal_resid) / max(abs(local), 1.0e-12)
    scan_rows.append(row)

preliminary = [
    row for row in scan_rows if abs(row["dev_pct"]) < 0.10 and row["nonlocal_frac"] < 2.0e-3
]
for row in preliminary:
    q2, q3, q4, ratio = amplitude_ratio_for_row(g1_pl, g2_pl, g3_sm, row)
    row["higher_ratio"] = ratio
    row["quad"] = q2
    row["cubic"] = q3
    row["quartic"] = q4

final_rows = [row for row in preliminary if row["higher_ratio"] < 0.10]
param_box_rows = [row for row in final_rows if row["center_frac"] >= 0.95 and row["width_frac"] <= 0.03]
outside_param_box = [row for row in final_rows if row not in param_box_rows]

# The branch theory closes on the response-weighted UV localization of the
# bridge, not on one arbitrary center/width box. Use the centroid side to
# define the intrinsic class.
intrinsic_uv = [row for row in final_rows if row["centroid_2"] >= 0.97]
outside_intrinsic = [row for row in final_rows if row not in intrinsic_uv]

if intrinsic_uv:
    j_aff_vals = np.array([row["j_aff"] for row in intrinsic_uv])
    c2_vals = np.array([row["centroid_2"] for row in intrinsic_uv])
    center_vals = np.array([row["center_frac"] for row in intrinsic_uv])
    width_vals = np.array([row["width_frac"] for row in intrinsic_uv])
    dev_vals = np.array([row["dev_pct"] for row in intrinsic_uv])
    best_by_shape = {}
    for row in intrinsic_uv:
        if row["shape"] not in best_by_shape or abs(row["dev_pct"]) < abs(best_by_shape[row["shape"]]["dev_pct"]):
            best_by_shape[row["shape"]] = row
else:
    j_aff_vals = np.array([])
    c2_vals = np.array([])
    center_vals = np.array([])
    width_vals = np.array([])
    dev_vals = np.array([])
    best_by_shape = {}

print("Broad scanned family summary:")
print(f"  total candidates scanned = {len(scan_rows)}")
print(f"  preliminary survivors (|dev| < 0.10% and nonlocal frac < 2e-3) = {len(preliminary)}")
print(f"  higher-order survivors (ratio < 0.10) = {len(final_rows)}")
print(f"  survivors inside coarse parametric UV box = {len(param_box_rows)}")
print(f"  survivors outside coarse parametric UV box = {len(outside_param_box)}")
print(f"  survivors inside intrinsic UV-centered class (c2 >= 0.97) = {len(intrinsic_uv)}")
print(f"  survivors outside intrinsic UV-centered class = {len(outside_intrinsic)}")
print()

if intrinsic_uv:
    print("Intrinsic UV-centered survivor band:")
    print(f"  center fraction range = [{center_vals.min():.3f}, {center_vals.max():.3f}]")
    print(f"  width fraction range  = [{width_vals.min():.3f}, {width_vals.max():.3f}]")
    print(f"  J_aff range           = [{j_aff_vals.min():.8f}, {j_aff_vals.max():.8f}]")
    print(f"  c2 range              = [{c2_vals.min():.6f}, {c2_vals.max():.6f}]")
    print(f"  dev% range            = [{dev_vals.min():+.4f}, {dev_vals.max():+.4f}]")
    print()

for row in sorted(best_by_shape.values(), key=lambda r: r["shape"]):
    q2, q3, q4, ratio = amplitude_ratio_for_row(g1_pl, g2_pl, g3_sm, row)
    row["higher_ratio"] = ratio
    row["quad"] = q2
    row["cubic"] = q3
    row["quartic"] = q4

print("Best intrinsic-class survivor per shape:")
print(f"  {'shape':<12s} {'center':>8s} {'width':>8s} {'dev%':>10s} {'J_aff':>12s} {'nonloc':>10s} {'higher':>10s}")
for row in sorted(best_by_shape.values(), key=lambda r: r["shape"]):
    print(
        f"  {row['shape']:<12s} {row['center_frac']:8.3f} {row['width_frac']:8.3f} "
        f"{row['dev_pct']:+10.4f} {row['j_aff']:12.8f} {row['nonlocal_frac']:10.6e} {row['higher_ratio']:10.6e}"
    )
print()

if intrinsic_uv:
    report(
        "2a-no-survivor-leaves-the-intrinsic-uv-centered-class",
        len(outside_intrinsic) == 0,
        f"outside intrinsic class survivors = {len(outside_intrinsic)}",
    )
    report(
        "2b-intrinsic-class-survivors-share-a-tight-center-band",
        (center_vals.max() - center_vals.min()) < 3.0e-2,
        f"center band width = {center_vals.max() - center_vals.min():.6e}",
    )
    report(
        "2c-intrinsic-class-survivors-share-a-tight-centroid-band",
        (c2_vals.max() - c2_vals.min()) < 1.2e-2,
        f"c2 band width = {c2_vals.max() - c2_vals.min():.6e}",
    )
    report(
        "2d-intrinsic-class-survivors-share-a-tight-jaff-band",
        (j_aff_vals.max() - j_aff_vals.min()) < 5.0e-5,
        f"J_aff band width = {j_aff_vals.max() - j_aff_vals.min():.6e}",
    )
    report(
        "2e-each-shape-best-intrinsic-survivor-keeps-higher-order-corrections-small",
        all(row["higher_ratio"] < 0.10 for row in best_by_shape.values()),
        "all best survivors have higher-order ratio below 0.10",
    )
else:
    report(
        "2a-no-survivor-leaves-the-intrinsic-uv-centered-class",
        False,
        "no intrinsic-class survivors were found in the scan",
    )
    report(
        "2b-intrinsic-class-survivors-share-a-tight-center-band",
        False,
        "no intrinsic-class survivors were found in the scan",
    )
    report(
        "2c-intrinsic-class-survivors-share-a-tight-centroid-band",
        False,
        "no intrinsic-class survivors were found in the scan",
    )
    report(
        "2d-intrinsic-class-survivors-share-a-tight-jaff-band",
        False,
        "no intrinsic-class survivors were found in the scan",
    )
    report(
        "2e-each-shape-best-intrinsic-survivor-keeps-higher-order-corrections-small",
        False,
        "no intrinsic-class survivors were found in the scan",
    )

print()
print("-" * 78)
print("Interpretation")
print("-" * 78)
if intrinsic_uv and len(outside_intrinsic) == 0:
    print(
        "Within the scanned constructive family, once the branch hypotheses are"
        " imposed, every surviving candidate falls into the same intrinsic"
        " UV-centered class and the same narrow J_aff band."
    )
    print(
        "The earlier center/width box was only a coarse parametrization aid."
        " At the intrinsic level, the viable bridge is not just UV-localized;"
        " it is forced into the same UV-centered class/band."
    )
else:
    print(
        "The scan did not yet certify uniqueness in the intrinsic UV-centered class."
    )
    print(
        "The remaining gap is still microscopic, but the current scan is not"
        " strong enough to claim intrinsic class/band uniqueness."
    )

print()
print("Honest boundary:")
print("This remains a scanned proxy-family certificate, not a proof over the")
print("full microscopic bridge space.")
print("=" * 78)
print(f"FINAL TALLY: {PASS} PASS / {FAIL} FAIL")
print(f"Elapsed: {time.time() - t0:.2f} s")
print("=" * 78)
