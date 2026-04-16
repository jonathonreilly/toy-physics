#!/usr/bin/env python3
"""
y_t Bridge Rearrangement Principle
=================================

Purpose
-------
Derive why the accepted interacting bridge must be UV-localized once the
bridge surplus is known to be positive.

Core statement
--------------
Write the downward flow in UV-to-IR time `tau` so that the accepted endpoint
is obtained by evolving from `tau = 0` (UV) to `tau = Delta tau` (IR). For a
perturbation `delta q(tau) = delta(g_3^2)(tau)` around the accepted bridge,
the linearized endpoint response has the Volterra form

    delta y_t(v) = integral_0^{Delta tau} K(tau) delta q(tau) d tau

with a positive kernel `K(tau)`.

If `K(tau)` is monotone increasing toward the IR, then any nonnegative bridge
surplus of fixed total action gives the smallest endpoint shift when it is
placed as far toward the UV as allowed. That is the rearrangement principle.

This does not finish the unbounded theorem, but it upgrades UV localization
from an empirical pattern to the natural consequence of the endpoint-response
ordering.
"""

from __future__ import annotations

import time
from math import pi

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

ALPHA_EM_MZ = 1.0 / 127.951
SIN2_TW_MZ = 0.23122
ALPHA_1_MZ_GUT = (5.0 / 3.0) * ALPHA_EM_MZ / (1.0 - SIN2_TW_MZ)
ALPHA_2_MZ = ALPHA_EM_MZ / SIN2_TW_MZ

T_V = np.log(V_DERIVED)
T_PL = np.log(M_PL)
LOG_SPAN = T_PL - T_V
FAC = 1.0 / (16.0 * PI**2)

TAU_GRID = np.linspace(0.0, LOG_SPAN, 2500)


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


def accepted_bridge(g3_sm, center_frac: float = 0.975, width_frac: float = 0.020):
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


def solve_downward(g1_pl: float, g2_pl: float, g3_profile, q_modifier=None):
    def rhs(tau, y):
        t = T_PL - tau
        g1, g2, yt = y
        q = g3_profile(t) ** 2
        if q_modifier is not None:
            q += q_modifier(tau)
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


def gaussian_bump(center_frac: float, width_frac: float, amplitude: float):
    tau_center = center_frac * LOG_SPAN
    tau_width = width_frac * LOG_SPAN
    norm = tau_width * np.sqrt(2.0 * PI)

    def modifier(tau: float) -> float:
        z = (tau - tau_center) / tau_width
        return amplitude * np.exp(-0.5 * z * z) / norm

    return modifier


print("=" * 78)
print("y_t BRIDGE REARRANGEMENT PRINCIPLE")
print("=" * 78)
print()
print("Derive the endpoint ordering of bridge surplus under the accepted")
print("downward flow and test whether UV localization follows as the")
print("minimal-response rearrangement.")
print()
t0 = time.time()

g1_v, g2_v = ew_boundary_at_v()
g1_pl, g2_pl = run_ew_upward(g1_v, g2_v)
g3_sm = sm_like_g3_trajectory()
g3_profile = accepted_bridge(g3_sm)
baseline = solve_downward(g1_pl, g2_pl, g3_profile)

g1_vals = baseline.y[0]
g2_vals = baseline.y[1]
yt_vals = baseline.y[2]
q_vals = np.array([g3_profile(T_PL - tau) ** 2 for tau in TAU_GRID])

# Linearized downward flow:
#   d(delta y)/d tau = A(tau) delta y + 8 FAC y_*(tau) delta q(tau)
A = FAC * (
    -27.0 / 2.0 * yt_vals**2
    + 17.0 / 20.0 * g1_vals**2
    + 9.0 / 4.0 * g2_vals**2
    + 8.0 * q_vals
)

lam = np.zeros_like(TAU_GRID)
lam[-1] = 1.0
for i in range(len(TAU_GRID) - 2, -1, -1):
    dt = TAU_GRID[i + 1] - TAU_GRID[i]
    a_mid = 0.5 * (A[i + 1] + A[i])
    lam[i] = lam[i + 1] * np.exp(-a_mid * dt)

kernel = 8.0 * FAC * lam * yt_vals * np.sqrt(8.0 / 9.0)
tau_frac = TAU_GRID / LOG_SPAN

print("Linearized kernel statistics:")
print(f"  K_min = {kernel.min():.6e}")
print(f"  K_max = {kernel.max():.6e}")
print(f"  IR/UV leverage ratio = {kernel[-1] / kernel[0]:.6f}")
print(
    "  kernel centroid (0=UV, 1=IR) = "
    f"{np.trapezoid(tau_frac * kernel, tau_frac) / np.trapezoid(kernel, tau_frac):.6f}"
)
print()

bump_centers = np.linspace(0.10, 0.95, 8)
bump_width = 0.02
bump_area = 2.0e-4
rows = []

for center_frac in bump_centers:
    bump_modifier = gaussian_bump(center_frac, bump_width, bump_area)
    bump_profile = np.array([bump_modifier(tau) for tau in TAU_GRID])
    predicted_delta = np.trapezoid(kernel * bump_profile, TAU_GRID)
    perturbed = solve_downward(g1_pl, g2_pl, g3_profile, q_modifier=bump_modifier)
    observed_delta = (perturbed.y[2, -1] - baseline.y[2, -1]) * np.sqrt(8.0 / 9.0)
    rows.append(
        {
            "center_frac": center_frac,
            "predicted_delta": predicted_delta,
            "observed_delta": observed_delta,
        }
    )

print("Equal-area Gaussian perturbations of q = g_3^2:")
print(f"  {'center':>8s} {'pred_dyt':>14s} {'obs_dyt':>14s}")
for row in rows:
    print(
        f"  {row['center_frac']:8.3f} "
        f"{row['predicted_delta']:14.6e} "
        f"{row['observed_delta']:14.6e}"
    )
print()

observed = np.array([row["observed_delta"] for row in rows])
predicted = np.array([row["predicted_delta"] for row in rows])

report(
    "1a-linearized-kernel-is-positive",
    bool(np.all(kernel > 0.0)),
    f"K(tau) > 0 on all {len(kernel)} sampled points",
)
report(
    "1b-kernel-is-monotone-toward-ir",
    bool(np.all(np.diff(kernel) >= 0.0)),
    f"monotonicity violations = {int(np.sum(np.diff(kernel) < 0.0))}",
)
report(
    "1c-ir-surplus-has-materially-larger-leverage-than-uv-surplus",
    kernel[-1] / kernel[0] > 1.8,
    f"IR/UV leverage ratio = {kernel[-1] / kernel[0]:.3f}",
)
report(
    "1d-finite-perturbations-follow-the-kernel-ordering",
    bool(np.all(np.diff(observed) > 0.0)),
    f"observed ordering violations = {int(np.sum(np.diff(observed) <= 0.0))}",
)
report(
    "1e-linear-kernel-predicts-the-finite-response-ordering",
    float(np.corrcoef(predicted, observed)[0, 1]) > 0.995,
    f"corr(predicted, observed) = {float(np.corrcoef(predicted, observed)[0, 1]):.6f}",
)
report(
    "1f-uv-placement-is-the-minimal-response-rearrangement",
    observed[0] < observed[-1] and observed[-1] / observed[0] > 2.0,
    f"equal-area IR/UV response ratio = {observed[-1] / observed[0]:.3f}",
)

print()
print("-" * 78)
print("Interpretation")
print("-" * 78)
print("The downward endpoint response to positive bridge surplus is ordered.")
print("For a fixed nonnegative surplus action, the response kernel is weakest")
print("near the UV endpoint and strongest near the IR endpoint.")
print()
print("So once the bridge surplus is known to be positive, any viable bridge")
print("that must preserve the accepted low-energy endpoint is forced into the")
print("smallest-response rearrangement: push the surplus as far toward the UV")
print("as the operator content allows.")
print()
print("This does not yet derive the exact selected invariant value. But it does")
print("explain why the bridge must be UV-localized rather than broadly spread")
print("across the full interval.")
print()
print("=" * 78)
print(f"FINAL TALLY: {PASS} PASS / {FAIL} FAIL")
print(f"Elapsed: {time.time() - t0:.2f} s")
print("=" * 78)
