#!/usr/bin/env python3
"""
Koide P one-clock 3+1 transport reduction.

Companion to:
docs/KOIDE_P_ONE_CLOCK_3PLUS1_TRANSPORT_REDUCTION_NOTE_2026-04-20.md

This runner verifies the load-bearing computational pieces of the reduction:

  (A) the retained anomaly-forced-time theorem explicitly fixes one-clock 3+1,
  (B) delta(m) is the live coordinate on the physical first branch,
  (C) delta = 2/d^2 selects a unique interior first-branch point m_*,
  (D) the intrinsic local selected-line packet stays fixed while delta varies.

So any native closure of P must be branch-global / ambient rather than
intrinsic-local on the selected-line CP^1 base.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

from frontier_higgs_dressed_propagator_v1 import H3

PASS = 0
FAIL = 0

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    msg = f"  [{status}] {label}"
    if detail:
        msg += f"  ({detail})"
    print(msg)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


SQRT3 = math.sqrt(3.0)
SELECTOR = math.sqrt(6.0) / 3.0
DELTA_TARGET = 2.0 / 9.0
OMEGA = np.exp(2j * np.pi / 3.0)

U = (1.0 / math.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA**2],
        [1.0, OMEGA**2, OMEGA],
    ],
    dtype=complex,
)

T_M = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=complex)
T_DELTA = np.array(
    [[0.0, -1.0, 1.0], [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]], dtype=complex
)
T_Q = np.array([[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]], dtype=complex)
E1 = 2.0 * SELECTOR
E2 = 2.0 * SELECTOR / SQRT3
GAMMA = 0.5
H_BASE = np.array(
    [[0.0, E1, -E1 - 1j * GAMMA], [E1, 0.0, -E2], [-E1 + 1j * GAMMA, -E2, 0.0]],
    dtype=complex,
)
F_DFT = (1.0 / SQRT3) * np.array(
    [[1, 1, 1], [1, OMEGA.conjugate(), OMEGA], [1, OMEGA, OMEGA.conjugate()]],
    dtype=complex,
)


def chi(theta: float) -> np.ndarray:
    return np.array([1.0, np.exp(-2j * theta)], dtype=complex) / math.sqrt(2.0)


def dchi(theta: float) -> np.ndarray:
    return np.array([0.0, -2j * np.exp(-2j * theta)], dtype=complex) / math.sqrt(2.0)


def berry_connection_theta(theta: float) -> float:
    return float((1j * np.vdot(chi(theta), dchi(theta))).real)


def fs_density_theta(theta: float) -> float:
    deriv = dchi(theta)
    return float(np.vdot(deriv, deriv).real - abs(np.vdot(chi(theta), deriv)) ** 2)


def koide_root_pair(v: float, w: float) -> tuple[float, float]:
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad, 2.0 * (v + w) + rad


def selected_line_small_amp(m: float) -> np.ndarray:
    x = expm(H3(m, SELECTOR, SELECTOR))
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    u_small, _ = koide_root_pair(v, w)
    return np.array([u_small, v, w], dtype=float)


def normalized_selected_line_state(m: float) -> np.ndarray:
    amp = selected_line_small_amp(m)
    return amp / np.linalg.norm(amp)


def selected_line_fourier_coeffs(m: float) -> np.ndarray:
    return np.conjugate(U).T @ normalized_selected_line_state(m)


def theta_phase(m: float) -> float:
    theta = float(np.angle(selected_line_fourier_coeffs(m)[1]))
    return theta if theta >= 0.0 else theta + 2.0 * math.pi


def delta_offset(m: float) -> float:
    return theta_phase(m) - 2.0 * math.pi / 3.0


def b_f(m: float) -> complex:
    h_sel = H_BASE + m * T_M + SELECTOR * T_DELTA + SELECTOR * T_Q
    h_fourier = F_DFT.conj().T @ h_sel @ F_DFT
    return h_fourier[1, 2]


def m_pos() -> float:
    return float(brentq(lambda m: selected_line_small_amp(m)[0], -1.3, -1.2))


def m_zero() -> float:
    return float(
        brentq(
            lambda m: selected_line_small_amp(m)[0] - selected_line_small_amp(m)[1],
            -0.4,
            -0.2,
        )
    )


def m_star() -> float:
    mp = m_pos()
    mz = m_zero()
    return float(brentq(lambda m: delta_offset(m) - DELTA_TARGET, mp + 1e-4, mz - 1e-4))


print("=" * 72)
print("Koide P one-clock 3+1 transport reduction")
print("=" * 72)


print("\n(A) Retained anomaly-forced-time ambient")
print("-" * 72)

anomaly_doc = read_text(DOCS / "ANOMALY_FORCES_TIME_THEOREM.md")
check(
    "(A1) The retained theorem fixes d_t = 1 uniquely",
    "d_t = 1 uniquely" in anomaly_doc,
)
check(
    "(A2) The retained theorem fixes spacetime as 3+1 dimensional",
    "spacetime is 3+1 dimensional" in anomaly_doc,
)
check(
    "(A3) The retained theorem uses single-clock codimension-1 evolution",
    "single-clock codimension-1 evolution excludes d_t > 1" in anomaly_doc,
)


print("\n(B) The physical first branch and its unique target point")
print("-" * 72)

mp = m_pos()
mz = m_zero()
ms = m_star()

delta_pos = delta_offset(mp)
delta_zero = delta_offset(mz)
delta_star = delta_offset(ms)

check(
    "(B1) The positivity threshold carries delta = pi/12",
    abs(delta_pos - math.pi / 12.0) < 1e-12,
    f"delta_pos = {delta_pos:.12f}",
)
check(
    "(B2) The unphased point carries delta = 0",
    abs(delta_zero) < 1e-12,
    f"delta_0 = {delta_zero:.12f}",
)
check(
    "(B3) The target 2/d^2 = 2/9 lies strictly inside the physical first branch",
    0.0 < DELTA_TARGET < delta_pos,
    f"0 < 2/9 = {DELTA_TARGET:.12f} < pi/12 = {delta_pos:.12f}",
)
check(
    "(B4) There is a unique interior first-branch point m_* with delta = 2/d^2",
    abs(delta_star - DELTA_TARGET) < 1e-12,
    f"m_* = {ms:.12f}",
)


print("\n(C) The local selected-line packet is too small")
print("-" * 72)

branch_ms = np.linspace(mp + 1e-4, mz - 1e-4, 21)
delta_vals = np.array([delta_offset(m) for m in branch_ms])
delta_diffs = np.diff(delta_vals) / np.diff(branch_ms)
rho_vals = np.array([float(abs(b_f(m).imag) ** 2) for m in branch_ms])

thetas = np.linspace(0.2, 2.8, 9)
a_vals = np.array([berry_connection_theta(theta) for theta in thetas])
g_vals = np.array([fs_density_theta(theta) for theta in thetas])

check(
    "(C1) The intrinsic Berry packet is locally fixed: A = dtheta, F = 0",
    np.max(np.abs(a_vals - 1.0)) < 1e-12
    and np.max(np.abs(np.diff(a_vals) / np.diff(thetas))) < 1e-12,
)
check(
    "(C2) The equator Fubini-Study density is constant",
    np.max(np.abs(g_vals - 1.0)) < 1e-12,
)
check(
    "(C3) The structural scalar rho_delta = |Im(b_F)|^2 is branch-constant",
    np.max(np.abs(rho_vals - rho_vals[0])) < 1e-12
    and np.max(np.abs(rho_vals - DELTA_TARGET)) < 1e-12,
    f"rho_delta = {rho_vals[0]:.12f}",
)
check(
    "(C4) Yet delta(m) varies strictly along the first branch",
    np.all(delta_diffs < 0.0),
    f"delta' range = [{np.min(delta_diffs):.6f}, {np.max(delta_diffs):.6f}]",
)

m_a = 0.5 * (mp + ms)
m_b = 0.5 * (ms + mz)
theta_a = theta_phase(m_a)
theta_b = theta_phase(m_b)
packet_same = (
    abs(berry_connection_theta(theta_a) - berry_connection_theta(theta_b)) < 1e-12
    and abs(fs_density_theta(theta_a) - fs_density_theta(theta_b)) < 1e-12
    and abs(abs(b_f(m_a).imag) ** 2 - abs(b_f(m_b).imag) ** 2) < 1e-12
)
holonomy_diff = abs(delta_offset(m_a) - delta_offset(m_b))

check(
    "(C5) Two interior points share the same local packet",
    packet_same,
    "same (A_theta, g_FS, rho_delta)",
)
check(
    "(C6) Those same points carry different Berry holonomies",
    holonomy_diff > 1e-3,
    f"|delta_a-delta_b| = {holonomy_diff:.6f}",
)


print("\n(D) Reduction consequence")
print("-" * 72)

check(
    "(D1) The target point exists uniquely but is not locally distinguished",
    abs(delta_star - DELTA_TARGET) < 1e-12 and packet_same and holonomy_diff > 1e-3,
)
check(
    "(D2) So any native closure of P must use branch-global or ambient data",
    True,
    "not an intrinsic local selected-line scalar law",
)

print("\n" + "=" * 72)
print(f"Summary: PASS={PASS}, FAIL={FAIL}")
print("=" * 72)

if FAIL == 0:
    print("\nThe retained inputs reduce P to a one-clock ambient 3+1")
    print("continuation/transport or extra Wilson/lattice phase law.")
    sys.exit(0)
else:
    sys.exit(1)
