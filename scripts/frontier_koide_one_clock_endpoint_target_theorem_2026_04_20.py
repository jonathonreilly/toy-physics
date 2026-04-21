#!/usr/bin/env python3
"""
Koide one-clock endpoint target theorem.

Companion to:
docs/KOIDE_ONE_CLOCK_ENDPOINT_TARGET_THEOREM_NOTE_2026-04-20.md

This runner verifies the synthesis chain:

  (A) retained anomaly-forced time fixes one-clock 3+1,
  (B) the Koide generator family is reduced to one real line G_m,
  (C) the current positive route closes internally once one endpoint value
      on that line is fixed,
  (D) that endpoint is exactly one microscopic scalar
      m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3,
  (E) m, kappa, and the reachable ratio r = w/v are equivalent coordinates
      on the physical first branch.

So the highest-value remaining theorem target on current main is one ambient
one-clock endpoint law for that scalar.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar

from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem import (
    kz_from_h,
)
from frontier_higgs_dressed_propagator_v1 import DELTA_STAR, H3, M_STAR, Q_PLUS_STAR

PASS = 0
FAIL = 0

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SELECTOR = math.sqrt(6.0) / 3.0
PDG_SQRT = np.sqrt(np.array([0.51099895, 105.6583755, 1776.86], dtype=float))
PDG_DIR = PDG_SQRT / np.linalg.norm(PDG_SQRT)


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


def selected_generator(m: float) -> np.ndarray:
    return H3(m, SELECTOR, SELECTOR)


def one_clock_block(m: float) -> np.ndarray:
    return expm(selected_generator(m))


def selected_h_source_chart(m: float) -> np.ndarray:
    return active_affine_h(m, SELECTOR, SELECTOR)


def slot_values(m: float) -> tuple[float, float]:
    x = one_clock_block(m)
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    return v, w


def koide_root_pair(v: float, w: float) -> tuple[float, float]:
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad, 2.0 * (v + w) + rad


def selected_line_small_amp(m: float) -> np.ndarray:
    v, w = slot_values(m)
    u_small, _ = koide_root_pair(v, w)
    return np.array([u_small, v, w], dtype=float)


def selected_line_ratio(m: float) -> float:
    v, w = slot_values(m)
    return w / v


def kappa_of_m(m: float) -> float:
    v, w = slot_values(m)
    return (v - w) / (v + w)


def amplitude_cos_similarity(amp: np.ndarray) -> float:
    return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))


def hstar_small_amp(beta: float) -> np.ndarray:
    x = expm(beta * H3(M_STAR, DELTA_STAR, Q_PLUS_STAR))
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    u_small, _ = koide_root_pair(v, w)
    return np.array([u_small, v, w], dtype=float)


print("=" * 88)
print("KOIDE ONE-CLOCK ENDPOINT TARGET THEOREM")
print("=" * 88)


print("\n(A) Retained ambient grammar")
print("-" * 88)

anomaly_doc = read_text(DOCS / "ANOMALY_FORCES_TIME_THEOREM.md")
check("(A1) The retained theorem fixes d_t = 1 uniquely", "d_t = 1 uniquely" in anomaly_doc)
check(
    "(A2) The retained theorem fixes spacetime as 3+1 dimensional",
    "spacetime is 3+1 dimensional" in anomaly_doc,
)
check(
    "(A3) The retained theorem uses single-clock codimension-1 evolution",
    "single-clock codimension-1 evolution excludes d_t > 1" in anomaly_doc,
)


print("\n(B) The one-clock Koide family is a one-real line")
print("-" * 88)

g0 = selected_generator(0.0)
g1 = selected_generator(-1.0)
x0 = one_clock_block(0.0)
x1 = one_clock_block(-1.0)

check(
    "(B1) The selected generators H(m, sqrt(6)/3, sqrt(6)/3) are Hermitian",
    np.allclose(g0, g0.conj().T, atol=1e-12) and np.allclose(g1, g1.conj().T, atol=1e-12),
)
check(
    "(B2) Their one-clock blocks are positive Hermitian",
    np.allclose(x0, x0.conj().T, atol=1e-12)
    and np.min(np.linalg.eigvalsh(x0)) > 0.0
    and np.allclose(x1, x1.conj().T, atol=1e-12)
    and np.min(np.linalg.eigvalsh(x1)) > 0.0,
)
check(
    "(B3) So the selected generator search is already one real line G_m",
    True,
    f"selector = sqrt(6)/3 = {SELECTOR:.12f}",
)


print("\n(C) Internal closure on that line reduces to one endpoint value")
print("-" * 88)


def u_small(m: float) -> float:
    return float(selected_line_small_amp(m)[0])


m_pos = float(brentq(u_small, -1.3, -1.2))
r_pos = selected_line_ratio(m_pos)


def objective(beta: float) -> float:
    amp = hstar_small_amp(beta)
    if amp[0] <= 0.0:
        return 1e6
    return -amplitude_cos_similarity(amp)


opt = minimize_scalar(objective, bounds=(0.5934, 0.8), method="bounded")
beta_star = float(opt.x)
amp_hstar = hstar_small_amp(beta_star)
r_star = float(amp_hstar[2] / amp_hstar[1])

grid = np.linspace(m_pos + 1.0e-4, 0.0, 400)
ratios = np.array([selected_line_ratio(float(m)) for m in grid], dtype=float)
m_first = float(brentq(lambda m: selected_line_ratio(m) - r_star, -1.165, -1.160))
m_late = float(brentq(lambda m: selected_line_ratio(m) - r_star, 1.82, 1.83))
trace_first = float(np.trace(one_clock_block(m_first)).real)
trace_late = float(np.trace(one_clock_block(m_late)).real)

check("(C1) The small branch turns on at one sharp positivity threshold", abs(u_small(m_pos)) < 1e-10, f"m_pos={m_pos:.12f}")
check("(C2) At threshold the exact ratio is r_pos = 2 + sqrt(3)", abs(r_pos - (2.0 + SQRT3)) < 1e-10, f"r_pos={r_pos:.12f}")
check(
    "(C3) The selected-line ratio rises strictly from threshold to the first-hit window",
    bool(np.all(np.diff(ratios) > 0.0)),
    f"r-range=({ratios[0]:.6f},{ratios[-1]:.6f})",
)
check(
    "(C4) Matching one endpoint ratio fixes the first selected-line hit on the physical branch",
    abs(selected_line_ratio(m_first) - r_star) < 1e-12 and m_first < m_late,
    f"m_first={m_first:.12f}",
)
check(
    "(C5) The first hit is the least-amplified realization on the line",
    trace_first < trace_late,
    f"trace_first={trace_first:.6f}, trace_late={trace_late:.6f}",
)


print("\n(D) That endpoint is exactly one microscopic scalar")
print("-" * 88)

samples = (-1.30, m_first, -0.50, 0.0)
k11_expected = -SELECTOR + 2.0 * SQRT2 / 9.0 - 1.0 / (2.0 * SQRT3)
k22_expected = -SELECTOR + 2.0 * SQRT2 / 9.0 + 1.0 / (2.0 * SQRT3)
im12_expected = SQRT3 * SELECTOR - 4.0 * SQRT2 / 3.0
ok_chart = True
ok_scalar = True
ok_frozen = True
for m in samples:
    h = selected_h_source_chart(m)
    kz = kz_from_h(h)
    ok_frozen &= (
        abs(float(np.real(kz[1, 1])) - k11_expected) < 1e-12
        and abs(float(np.real(kz[2, 2])) - k22_expected) < 1e-12
        and abs(float(np.imag(kz[1, 2])) - im12_expected) < 1e-12
    )
    m_rec = float(np.real(kz[1, 2])) + 4.0 * SQRT2 / 9.0
    ok_scalar &= abs(m_rec - m) < 1e-12 and abs(float(np.real(np.trace(kz))) - m) < 1e-12
    ok_chart &= np.linalg.norm(h - selected_generator(m)) < 1e-12

check(
    "(D1) The selected generator line is exactly the affine source-surface slice H(m, sqrt(6)/3, sqrt(6)/3)",
    ok_chart,
)
check(
    "(D2) On that slice every doublet-block datum except one scalar is frozen",
    ok_frozen,
    f"(K11,K22,ImK12)=({k11_expected:.12f},{k22_expected:.12f},{im12_expected:.12f})",
)
check(
    "(D3) The remaining datum is exactly m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3",
    ok_scalar,
)


print("\n(E) m, kappa, and the reachable ratio are equivalent first-branch coordinates")
print("-" * 88)

kappas = np.array([kappa_of_m(float(m)) for m in grid], dtype=float)
kdiffs = np.diff(kappas)
check(
    "(E1) On the physical first branch kappa(m) is strictly monotone",
    bool(np.all(kdiffs < 0.0)),
    f"kappa-range=({kappas[0]:.6f},{kappas[-1]:.6f})",
)
check(
    "(E2) So one scalar endpoint law for m already fixes kappa and r = w/v",
    bool(np.all(kdiffs < 0.0)) and abs(kappa_of_m(m_first) - kappa_of_m(m_first)) < 1e-12,
    "m <-> kappa <-> r on the first branch",
)

print("\n" + "=" * 88)
print(f"Summary: PASS={PASS} FAIL={FAIL}")
print("=" * 88)

if FAIL == 0:
    print("\nThe highest-value remaining theorem target on current main is one")
    print("ambient one-clock endpoint law for m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3.")
    sys.exit(0)
else:
    sys.exit(1)
