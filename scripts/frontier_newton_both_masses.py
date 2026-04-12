#!/usr/bin/env python3
"""
Open-Wilson both-masses test with independent inertial masses.

This is the first honest next-step observable for the Newton-closure lane:
  - open 3D Wilson lattice
  - weak screening (mu^2 = 0.001)
  - two separate orbitals at fixed separation
  - each orbital has its own physical mass M_A, M_B
  - the Poisson source uses the same masses
  - the Wilson Hamiltonians use separate inertial masses
  - the retained observable is early-time mutual momentum transfer
      P_A^mut = M_A * (v_A^shared - v_A^self)
      P_B^mut = M_B * (v_B^shared - v_B^self)

What this can test:
  - whether the A impulse is linear in the partner mass M_B
  - whether the B impulse is linear in the partner mass M_A
  - whether the mutual impulses are equal and opposite

What it still cannot prove by itself:
  - a full many-body Newton closure
  - a continuum action-reaction theorem
"""

from __future__ import annotations

import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


# ── parameters ──────────────────────────────────────────────────────────
SIDE = 15
N = SIDE ** 3
WILSON_R = 1.0
DT = 0.08
REG = 1e-6
N_STEPS = 18
SIGMA = 1.0
G_VAL = 5.0
MU2 = 0.001
D_SEP = 5
MASS_VALUES = [0.5, 1.0, 2.0, 3.0]
EARLY_START = 2
EARLY_END = 8


# ── lattice setup (open BC) ────────────────────────────────────────────
pos = np.zeros((N, 3))
adj: dict[int, list[int]] = {}

for x in range(SIDE):
    for y in range(SIDE):
        for z in range(SIDE):
            i = x * SIDE**2 + y * SIDE + z
            pos[i] = [x, y, z]
            adj[i] = []
            for dx, dy, dz in (
                (1, 0, 0),
                (-1, 0, 0),
                (0, 1, 0),
                (0, -1, 0),
                (0, 0, 1),
                (0, 0, -1),
            ):
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 <= nx < SIDE and 0 <= ny < SIDE and 0 <= nz < SIDE:
                    adj[i].append(nx * SIDE**2 + ny * SIDE + nz)


def build_laplacian():
    rows, cols, vals = [], [], []
    for i in range(N):
        rows.append(i)
        cols.append(i)
        vals.append(-len(adj[i]))
        for j in adj[i]:
            rows.append(i)
            cols.append(j)
            vals.append(1.0)
    return sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))


LAP = build_laplacian()
POISSON_OP = (LAP - MU2 * sparse.eye(N) - REG * sparse.eye(N)).tocsc()


def solve_poisson(rho):
    rhs = -4.0 * np.pi * G_VAL * rho
    return spsolve(POISSON_OP, rhs).real


def build_wilson_hamiltonian(phi, inertial_mass):
    rows, cols, vals = [], [], []
    for i in range(N):
        for j in adj[i]:
            if j <= i:
                continue
            rows.append(i)
            cols.append(j)
            vals.append(-0.5j + 0.5 * WILSON_R)
            rows.append(j)
            cols.append(i)
            vals.append(+0.5j + 0.5 * WILSON_R)
        diag = inertial_mass + phi[i] + 0.5 * WILSON_R * len(adj[i])
        rows.append(i)
        cols.append(i)
        vals.append(diag)
    return sparse.csc_matrix((vals, (rows, cols)), shape=(N, N))


def cn_step(psi, hamiltonian):
    half = 1j * hamiltonian * (DT / 2.0)
    eye = sparse.eye(N, format="csc")
    lhs = (eye + half).tocsc()
    rhs = (eye - half).dot(psi)
    psi_new = spsolve(lhs, rhs)
    psi_new /= np.linalg.norm(psi_new)
    return psi_new


def gaussian_wavepacket(center, sigma=SIGMA):
    psi = np.zeros(N, dtype=complex)
    cx, cy, cz = center
    for i in range(N):
        x, y, z = pos[i]
        r2 = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
        psi[i] = np.exp(-r2 / (2 * sigma**2))
    psi /= np.linalg.norm(psi)
    return psi


def center_of_mass_x(psi):
    rho = np.abs(psi) ** 2
    return float(np.sum(rho * pos[:, 0]) / max(np.sum(rho), 1e-30))


def run_pair(mode, center_a, center_b, mass_a, mass_b):
    psi_a = gaussian_wavepacket(center_a)
    psi_b = gaussian_wavepacket(center_b)

    cx_a = np.zeros(N_STEPS + 1)
    cx_b = np.zeros(N_STEPS + 1)
    cx_a[0] = center_of_mass_x(psi_a)
    cx_b[0] = center_of_mass_x(psi_b)

    for t in range(N_STEPS):
        if mode == "SHARED":
            rho_total = mass_a * np.abs(psi_a) ** 2 + mass_b * np.abs(psi_b) ** 2
            phi = solve_poisson(rho_total)
            h_a = build_wilson_hamiltonian(phi, mass_a)
            h_b = build_wilson_hamiltonian(phi, mass_b)
        elif mode == "SELF_ONLY":
            phi_a = solve_poisson(mass_a * np.abs(psi_a) ** 2)
            phi_b = solve_poisson(mass_b * np.abs(psi_b) ** 2)
            h_a = build_wilson_hamiltonian(phi_a, mass_a)
            h_b = build_wilson_hamiltonian(phi_b, mass_b)
        elif mode == "FREE":
            zeros = np.zeros(N)
            h_a = build_wilson_hamiltonian(zeros, mass_a)
            h_b = build_wilson_hamiltonian(zeros, mass_b)
        else:
            raise ValueError(f"Unknown mode: {mode}")

        psi_a = cn_step(psi_a, h_a)
        psi_b = cn_step(psi_b, h_b)
        cx_a[t + 1] = center_of_mass_x(psi_a)
        cx_b[t + 1] = center_of_mass_x(psi_b)

    return cx_a, cx_b


def velocity_array(cx):
    vel = np.zeros(len(cx))
    vel[1:] = (cx[1:] - cx[:-1]) / DT
    vel[0] = vel[1]
    return vel


def acceleration_array(cx):
    acc = np.zeros(len(cx))
    acc[1:-1] = (cx[2:] - 2 * cx[1:-1] + cx[:-2]) / DT**2
    acc[0] = acc[1]
    acc[-1] = acc[-2]
    return acc


def early_window(arr, start=EARLY_START, end=EARLY_END):
    return arr[start:min(end, len(arr))]


def mutual_metrics(cx_shared, cx_self, inertial_mass, direction):
    v_shared = velocity_array(cx_shared)
    v_self = velocity_array(cx_self)
    a_shared = acceleration_array(cx_shared)
    a_self = acceleration_array(cx_self)

    dv = v_shared - v_self
    da = a_shared - a_self
    if direction == "left":
        dv = -dv
        da = -da

    impulse = inertial_mass * float(np.mean(early_window(dv)))
    accel = float(np.mean(early_window(da)))
    return impulse, accel


def linear_fit(xs, ys):
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    slope, intercept = np.polyfit(xs, ys, 1)
    fit = slope * xs + intercept
    ss_res = float(np.sum((ys - fit) ** 2))
    ss_tot = float(np.sum((ys - np.mean(ys)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return slope, intercept, r2


def coefficient_of_variation(values):
    values = np.asarray(values, dtype=float)
    mean = float(np.mean(values))
    std = float(np.std(values))
    if abs(mean) < 1e-30:
        return float("inf"), mean, std
    return abs(std / mean), mean, std


def main():
    center = SIDE // 2
    x_a = center - D_SEP // 2
    x_b = center + (D_SEP - D_SEP // 2)
    center_a = (x_a, center, center)
    center_b = (x_b, center, center)

    print("=" * 92)
    print("OPEN WILSON BOTH-MASSES MOMENTUM-TRANSFER TEST")
    print("=" * 92)
    print(f"Lattice: {SIDE}^3 = {N} sites, open BC")
    print(f"Wilson: r={WILSON_R}, DT={DT}, sigma={SIGMA}")
    print(f"Gravity: G={G_VAL}, mu2={MU2}, REG={REG}")
    print(f"Separation d={D_SEP}, positions A@x={x_a}, B@x={x_b}")
    print(f"Mass grid: {MASS_VALUES}")
    print()
    print("Observable:")
    print("  P_A^mut = M_A * <v_A^shared - v_A^self>")
    print("  P_B^mut = M_B * <v_B^self - v_B^shared>   (same inward-positive sign)")
    print("  action-reaction proxy uses signed impulses: P_A^mut + P_B^signed")
    print()

    results = {}
    header = (
        f"{'M_A':>5s} {'M_B':>5s} | "
        f"{'P_A^mut':>12s} {'P_B^mut':>12s} | "
        f"{'a_A':>10s} {'a_B':>10s} | "
        f"{'P_A+P_B':>11s} {'PA/MB':>10s} {'PB/MA':>10s}"
    )
    print(header)
    print("-" * len(header))

    t_total = time.time()
    for mass_a in MASS_VALUES:
        for mass_b in MASS_VALUES:
            cx_a_sh, cx_b_sh = run_pair("SHARED", center_a, center_b, mass_a, mass_b)
            cx_a_so, cx_b_so = run_pair("SELF_ONLY", center_a, center_b, mass_a, mass_b)

            impulse_a, accel_a = mutual_metrics(cx_a_sh, cx_a_so, mass_a, direction="right")
            impulse_b_mag, accel_b_mag = mutual_metrics(cx_b_sh, cx_b_so, mass_b, direction="left")

            signed_impulse_b = -impulse_b_mag

            results[(mass_a, mass_b)] = {
                "impulse_a": impulse_a,
                "impulse_b_mag": impulse_b_mag,
                "signed_impulse_b": signed_impulse_b,
                "accel_a": accel_a,
                "accel_b_mag": accel_b_mag,
                "action_balance": impulse_a + signed_impulse_b,
                "p_a_per_mb": impulse_a / mass_b,
                "p_b_per_ma": impulse_b_mag / mass_a,
            }

            print(
                f"{mass_a:5.1f} {mass_b:5.1f} | "
                f"{impulse_a:+12.6e} {impulse_b_mag:+12.6e} | "
                f"{accel_a:+10.6e} {accel_b_mag:+10.6e} | "
                f"{impulse_a + signed_impulse_b:+11.3e} "
                f"{impulse_a / mass_b:+10.3e} {impulse_b_mag / mass_a:+10.3e}"
            )

    print(f"\nTotal grid time: {time.time() - t_total:.1f}s")

    print()
    print("=" * 92)
    print("ANCHOR SLICE 1: P_A^mut vs M_B  (M_A = 1.0)")
    print("=" * 92)
    mb_vals = []
    pa_vals = []
    for mass_b in MASS_VALUES:
        value = results[(1.0, mass_b)]["impulse_a"]
        mb_vals.append(mass_b)
        pa_vals.append(value)
        print(f"  M_B={mass_b:.1f}: P_A^mut = {value:+.6e}")
    slope_a, intercept_a, r2_a = linear_fit(mb_vals, pa_vals)
    print(f"  fit: P_A^mut = {slope_a:+.6e} * M_B + {intercept_a:+.6e}   R^2={r2_a:.6f}")

    print()
    print("=" * 92)
    print("ANCHOR SLICE 2: P_B^mut vs M_A  (M_B = 1.0)")
    print("=" * 92)
    ma_vals = []
    pb_vals = []
    for mass_a in MASS_VALUES:
        value = results[(mass_a, 1.0)]["impulse_b_mag"]
        ma_vals.append(mass_a)
        pb_vals.append(value)
        print(f"  M_A={mass_a:.1f}: P_B^mut = {value:+.6e}")
    slope_b, intercept_b, r2_b = linear_fit(ma_vals, pb_vals)
    print(f"  fit: P_B^mut = {slope_b:+.6e} * M_A + {intercept_b:+.6e}   R^2={r2_b:.6f}")

    print()
    print("=" * 92)
    print("FULL-GRID NORMALIZATION CHECKS")
    print("=" * 92)
    pa_norm = [results[key]["p_a_per_mb"] for key in results]
    pb_norm = [results[key]["p_b_per_ma"] for key in results]
    pa_cv, pa_mean, pa_std = coefficient_of_variation(pa_norm)
    pb_cv, pb_mean, pb_std = coefficient_of_variation(pb_norm)
    print(f"  P_A^mut / M_B: mean={pa_mean:+.6e}, std={pa_std:.6e}, CV={pa_cv:.3%}")
    print(f"  P_B^mut / M_A: mean={pb_mean:+.6e}, std={pb_std:.6e}, CV={pb_cv:.3%}")

    print()
    print("=" * 92)
    print("ACTION-REACTION CHECK")
    print("=" * 92)
    signed_pairs = []
    rel_balance = []
    for mass_a in MASS_VALUES:
        for mass_b in MASS_VALUES:
            row = results[(mass_a, mass_b)]
            signed_pairs.append(row["action_balance"])
            denom = max(abs(row["impulse_a"]) + abs(row["impulse_b_mag"]), 1e-30)
            rel = abs(row["action_balance"]) / denom
            rel_balance.append(rel)
            status = "PASS" if rel < 0.10 else ("MARGINAL" if rel < 0.25 else "FAIL")
            print(
                f"  M_A={mass_a:.1f}, M_B={mass_b:.1f}: "
                f"P_A + P_B(signed) = {row['action_balance']:+.6e}, "
                f"relative imbalance={rel:.3%} [{status}]"
            )
    rel_mean = float(np.mean(rel_balance))
    rel_max = float(np.max(rel_balance))
    print(f"\n  mean relative imbalance = {rel_mean:.3%}")
    print(f"  max  relative imbalance = {rel_max:.3%}")

    print()
    print("=" * 92)
    print("SUMMARY")
    print("=" * 92)
    print(f"1. Anchor slice P_A^mut vs M_B: R^2={r2_a:.6f}")
    print(f"2. Anchor slice P_B^mut vs M_A: R^2={r2_b:.6f}")
    print(f"3. Full-grid CV for P_A^mut/M_B: {pa_cv:.3%}")
    print(f"4. Full-grid CV for P_B^mut/M_A: {pb_cv:.3%}")
    print(f"5. Mean action-reaction imbalance: {rel_mean:.3%}")

    pass_anchor = r2_a > 0.95 and r2_b > 0.95
    pass_grid = pa_cv < 0.15 and pb_cv < 0.15
    pass_reaction = rel_mean < 0.10 and rel_max < 0.25

    if pass_anchor and pass_grid and pass_reaction:
        print("\nOVERALL: retained both-masses closure survives on this surface.")
    else:
        print("\nOVERALL: full Newton-style both-masses closure still fails on this surface.")
        if not pass_anchor:
            print("  - anchor slice linearity already breaks")
        if not pass_grid:
            print("  - full-grid normalization is not stable once both masses vary")
        if not pass_reaction:
            print("  - equal-and-opposite mutual momentum transfer does not hold cleanly")
        print("  - this means the current open weak-screening Wilson lane still supports")
        print("    only slice-wise source/response linearity, not a retained M_A*M_B law")


if __name__ == "__main__":
    main()
