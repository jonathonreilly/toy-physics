#!/usr/bin/env python3
"""
Brannen δ = 2/9 physical bridge investigation — CORRECTED.

The Koide amplitude s(m) is NOT the ground-state eigenvector of H_sel(m).
Rather, following frontier_koide_berry_phase_theorem.py:

    v(m) = Re((expm(H3(m, √6/3, √6/3)))[2,2])
    w(m) = Re((expm(H3(m, √6/3, √6/3)))[1,1])
    u(m) = smaller root of Koide pair on (v, w)

The Koide state s(m) = (u,v,w)/||(u,v,w)||.
θ(m) = arg(<v_ω, s(m)>) the Fourier doublet phase.
δ(m) = θ(m) − 2π/3 the Brannen offset = Berry holonomy.

This script probes: what AXIOM-NATIVE CRITERION picks m_* = -1.160443...
such that δ(m_*) = 2/9 rad?
"""

import math
import sys

import numpy as np
from scipy.linalg import expm


GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0
SELECTOR = math.sqrt(6.0) / 3.0

T_M = np.array([[1.0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
T_DELTA = np.array([[0, -1, 1], [-1, 1, 0], [1, 0, -1]], dtype=complex)
T_Q = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], dtype=complex)
H_BASE = np.array(
    [
        [0.0, E1, -E1 - 1j * GAMMA],
        [E1, 0.0, -E2],
        [-E1 + 1j * GAMMA, -E2, 0.0],
    ],
    dtype=complex,
)

OMEGA = np.exp(2j * math.pi / 3.0)
UZ3 = (1.0 / math.sqrt(3.0)) * np.array(
    [[1, 1, 1], [1, OMEGA, OMEGA**2], [1, OMEGA**2, OMEGA]], dtype=complex
)


def H_sel(m: float) -> np.ndarray:
    return H_BASE + m * T_M + SELECTOR * (T_DELTA + T_Q)


def koide_amplitudes(m: float) -> tuple[float, float, float]:
    x = expm(H_sel(m))
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    u_small = 2.0 * (v + w) - rad
    return u_small, v, w


def doublet_phase(m: float) -> float:
    u, v, w = koide_amplitudes(m)
    amp = np.array([u, v, w], dtype=complex)
    s = amp / np.linalg.norm(amp)
    fourier = UZ3.conj().T @ s
    th = float(np.angle(fourier[1]))
    return th % (2 * math.pi)


def delta_brannen(m: float) -> float:
    return doublet_phase(m) - 2 * math.pi / 3


def koide_Q(m: float) -> float:
    u, v, w = koide_amplitudes(m)
    return (u**2 + v**2 + w**2) / (u + v + w) ** 2


def main() -> int:
    print("=" * 80)
    print("Brannen δ=2/9 physical-bridge investigation (CORRECTED)")
    print("=" * 80)

    m_0 = -0.265815998702
    m_star = -1.160443440065
    m_pos = -1.295794904067
    eta = 2.0 / 9.0

    print("\n(A) Verify framework's claimed values at anchor points")
    print(f"  {'m':>16} {'u':>10} {'v':>10} {'w':>10} {'Q':>12} {'θ(m)':>12} {'δ(m)':>12}")
    for name, m in [("m_0", m_0), ("m_*", m_star), ("m_pos", m_pos)]:
        u, v, w = koide_amplitudes(m)
        th = doublet_phase(m)
        d = delta_brannen(m)
        Q = koide_Q(m)
        print(f"  {name:>4}({m:>+9.4f}) {u:>10.6f} {v:>10.6f} {w:>10.6f} "
              f"{Q:>12.9f} {th:>12.9f} {d:>12.9f}")
    print(f"  target δ(m_*) = 2/9 = {eta:.9f}")
    print(f"  target δ(m_pos) = π/12 = {math.pi/12:.9f}")

    # === Search for natural-criterion candidates for m_* ===
    print("\n" + "=" * 80)
    print("(B) Search for axiom-native criterion that picks m_*")
    print("=" * 80)

    print("\n  Scan m in [m_pos, m_0] and tabulate natural invariants:")
    print(f"  {'m':>12} {'δ(m)':>10} {'Tr[exp H]':>12} {'det(exp H)':>14} "
          f"{'|b_F|²':>10} {'Tr[exp H·C]':>14}")

    # Cyclic shift C for trace with C-projection
    C_cyc = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)

    best = {}
    for m in np.linspace(m_pos + 1e-4, m_0 - 1e-4, 80):
        u, v, w = koide_amplitudes(m)
        d = delta_brannen(m)
        exp_H = expm(H_sel(m))
        tr_exp = float(np.real(np.trace(exp_H)))
        det_exp = float(np.real(np.linalg.det(exp_H)))
        # Fourier representation: b_F[1,2] off-diagonal of Fourier-transformed H
        H_F = UZ3.conj().T @ H_sel(m) @ UZ3
        b_F = H_F[1, 2]
        b_F2 = float(abs(b_F) ** 2)
        tr_cH = float(np.real(np.trace(C_cyc @ exp_H)))
        if abs(d - eta) < 5e-3:
            best[m] = (d, tr_exp, det_exp, b_F2, tr_cH)
        print(f"  {m:>+12.6f} {d:>10.6f} {tr_exp:>12.6f} {det_exp:>14.6f} "
              f"{b_F2:>10.6f} {tr_cH:>14.6f}")

    # === Check if Im(b_F) is truly topologically protected ===
    print("\n(C) Check |Im(b_F(m))|² claim (framework: = 2/9 constant)")
    for name, m in [("m_0", m_0), ("m_*", m_star), ("m_pos", m_pos)]:
        H_F = UZ3.conj().T @ H_sel(m) @ UZ3
        b_F = H_F[1, 2]
        print(f"  {name:>4}({m:>+9.4f}): Im(b_F) = {b_F.imag:+.9f}  "
              f"Re(b_F) = {b_F.real:+.9f}  |Im|² = {b_F.imag**2:.9f}")

    # === Scan to find critical m where specific quantities are stationary ===
    print("\n" + "=" * 80)
    print("(D) Numerical search for stationarity of various candidate actions")
    print("=" * 80)

    m_grid = np.linspace(m_pos + 1e-4, m_0 - 1e-4, 2000)
    candidates = {}

    # (D1) Tr(exp(H))
    tr_exp = np.array([float(np.real(np.trace(expm(H_sel(m))))) for m in m_grid])
    dtr = np.gradient(tr_exp, m_grid)
    z = np.where(np.diff(np.sign(dtr)))[0]
    if len(z):
        candidates["d/dm Tr(exp H) = 0"] = m_grid[z]

    # (D2) Tr(C·exp(H))
    tr_cH = np.array([float(np.real(np.trace(C_cyc @ expm(H_sel(m))))) for m in m_grid])
    dtr_c = np.gradient(tr_cH, m_grid)
    z = np.where(np.diff(np.sign(dtr_c)))[0]
    if len(z):
        candidates["d/dm Tr(C·exp H) = 0"] = m_grid[z]

    # (D3) log|det H_sel| stationarity
    ld = np.array([math.log(abs(np.linalg.det(H_sel(m)))) for m in m_grid])
    dld = np.gradient(ld, m_grid)
    z = np.where(np.diff(np.sign(dld)))[0]
    if len(z):
        candidates["d/dm log|det H| = 0"] = m_grid[z]

    # (D4) κ_sel extremum (v-w)/(v+w)
    kap = np.array(
        [
            (
                (lambda u, v, w: (v - w) / (v + w))
                (*koide_amplitudes(m))
            )
            for m in m_grid
        ]
    )
    dk = np.gradient(kap, m_grid)
    z = np.where(np.diff(np.sign(dk)))[0]
    if len(z):
        candidates["d/dm κ_sel = 0"] = m_grid[z]

    # (D5) Re(b_F(m)) = 0 zero crossing (Re(b_F) = m - 4√2/9 structurally)
    rebf = np.array(
        [
            float(np.real((UZ3.conj().T @ H_sel(m) @ UZ3)[1, 2]))
            for m in m_grid
        ]
    )
    z = np.where(np.diff(np.sign(rebf)))[0]
    if len(z):
        candidates["Re(b_F) = 0"] = m_grid[z]

    # (D6) u (smallest amplitude) = 0 (positivity threshold = m_pos)
    us = np.array([koide_amplitudes(m)[0] for m in m_grid])
    z = np.where(np.diff(np.sign(us)))[0]
    if len(z):
        candidates["u = 0 (positivity)"] = m_grid[z]

    # (D7) δ(m) - 2/9 = 0 (by definition this gives m_*)
    dls = np.array([delta_brannen(m) for m in m_grid])
    z = np.where(np.diff(np.sign(dls - eta)))[0]
    if len(z):
        candidates["δ(m) = 2/9 (definition of m_*)"] = m_grid[z]

    # (D8) δ(m) = |Im(b_F)|² directly (CPC)
    imbf2 = np.array(
        [
            float(np.imag((UZ3.conj().T @ H_sel(m) @ UZ3)[1, 2]) ** 2)
            for m in m_grid
        ]
    )
    z = np.where(np.diff(np.sign(dls - imbf2)))[0]
    if len(z):
        candidates["δ(m) = |Im(b_F(m))|² (CPC)"] = m_grid[z]

    # Report
    print(f"\n  Target m_* = {m_star:+.6f}")
    print(f"  Target δ(m_*) = {eta:.6f}")
    for crit, ms in candidates.items():
        diffs = [(m - m_star) for m in ms]
        best_idx = int(np.argmin(np.abs(diffs)))
        m_found = ms[best_idx]
        print(f"  [{crit:>35}]  found m = {m_found:+.6f}   Δm = {m_found - m_star:+.2e}")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
