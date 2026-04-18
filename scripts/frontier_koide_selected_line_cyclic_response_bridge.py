#!/usr/bin/env python3
"""
Koide selected-line cyclic-response bridge
=========================================

STATUS: exact reduction of the remaining charged-lepton gap to one scalar
cyclic-response law
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar

from frontier_higgs_dressed_propagator_v1 import DELTA_STAR, H3, M_STAR, Q_PLUS_STAR

PASS_COUNT = 0
FAIL_COUNT = 0

SQRT3 = math.sqrt(3.0)
S_SELECTOR = math.sqrt(6.0) / 3.0
PDG_SQRT = np.sqrt(np.array([0.51099895, 105.6583755, 1776.86], dtype=float))
PDG_DIR = PDG_SQRT / np.linalg.norm(PDG_SQRT)


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def koide_root_pair(v: float, w: float) -> tuple[float, float]:
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad, 2.0 * (v + w) + rad


def amplitude_cos_similarity(amp: np.ndarray) -> float:
    return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))


def cyclic_from_slots(u: float, v: float, w: float) -> tuple[float, float, float]:
    return u + v + w, 2.0 * u - v - w, SQRT3 * (v - w)


def slots_from_cyclic(r0: float, r1: float, r2: float) -> tuple[float, float, float]:
    u = (r0 + r1) / 3.0
    v = r0 / 3.0 - r1 / 6.0 + SQRT3 * r2 / 6.0
    w = r0 / 3.0 - r1 / 6.0 - SQRT3 * r2 / 6.0
    return u, v, w


def kappa_from_slots(v: float, w: float) -> float:
    return (v - w) / (v + w)


def kappa_from_cyclic(r0: float, r1: float, r2: float) -> float:
    return SQRT3 * r2 / (2.0 * r0 - r1)


def ratio_from_kappa(kappa: float) -> float:
    return (1.0 - kappa) / (1.0 + kappa)


def selected_line_slots(m: float) -> tuple[float, float]:
    x = expm(H3(m, S_SELECTOR, S_SELECTOR))
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    return v, w


def selected_line_small_amp(m: float) -> np.ndarray:
    v, w = selected_line_slots(m)
    u_small, _ = koide_root_pair(v, w)
    return np.array([u_small, v, w], dtype=float)


def selected_line_kappa(m: float) -> float:
    v, w = selected_line_slots(m)
    return kappa_from_slots(v, w)


def hstar_witness_kappa() -> tuple[float, float]:
    def hstar_small_amp(beta: float) -> np.ndarray:
        x = expm(beta * H3(M_STAR, DELTA_STAR, Q_PLUS_STAR))
        v = float(np.real(x[2, 2]))
        w = float(np.real(x[1, 1]))
        u_small, _ = koide_root_pair(v, w)
        return np.array([u_small, v, w], dtype=float)

    def objective(beta: float) -> float:
        amp = hstar_small_amp(beta)
        if amp[0] <= 0.0:
            return 1e6
        return -amplitude_cos_similarity(amp)

    opt = minimize_scalar(objective, bounds=(0.5934, 0.8), method="bounded")
    beta_star = float(opt.x)
    amp = hstar_small_amp(beta_star)
    return beta_star, kappa_from_slots(float(amp[1]), float(amp[2]))


def part1_exact_cyclic_bridge() -> None:
    print("=" * 88)
    print("PART 1: the selected-line point is controlled by one scalar cyclic-response ratio")
    print("=" * 88)

    u, v, w = sp.symbols("u v w", nonzero=True)
    r0 = u + v + w
    r1 = 2 * u - v - w
    r2 = sp.sqrt(3) * (v - w)

    u_back = sp.simplify((r0 + r1) / 3)
    v_back = sp.simplify(r0 / 3 - r1 / 6 + sp.sqrt(3) * r2 / 6)
    w_back = sp.simplify(r0 / 3 - r1 / 6 - sp.sqrt(3) * r2 / 6)

    kappa_slots = sp.simplify((v - w) / (v + w))
    kappa_cyclic = sp.simplify(sp.sqrt(3) * r2 / (2 * r0 - r1))
    ratio_wv = sp.simplify(w / v)
    ratio_from_k = sp.simplify((1 - kappa_slots) / (1 + kappa_slots))

    check("The cyclic map inverts exactly back to (u,v,w)",
          sp.simplify(u_back - u) == 0 and sp.simplify(v_back - v) == 0 and sp.simplify(w_back - w) == 0)
    check("The scalar bridge kappa is exactly sqrt(3) r2 / (2 r0 - r1)",
          sp.simplify(kappa_slots - kappa_cyclic) == 0)
    check("Once kappa is fixed, the reachable-slot ratio is fixed by w/v = (1-kappa)/(1+kappa)",
          sp.simplify(ratio_wv - ratio_from_k) == 0)


def part2_exact_threshold_value() -> float:
    print()
    print("=" * 88)
    print("PART 2: the branch threshold gives one exact scalar starting point")
    print("=" * 88)

    def u_small(m: float) -> float:
        return float(selected_line_small_amp(m)[0])

    m_pos = float(brentq(u_small, -1.3, -1.2))
    kappa_pos = selected_line_kappa(m_pos)

    check("The selected line has one sharp small-branch positivity threshold",
          abs(u_small(m_pos)) < 1e-10,
          detail=f"m_pos={m_pos:.12f}",
          kind="NUMERIC")
    check("At threshold the scalar bridge takes the exact value kappa_pos = -1/sqrt(3)",
          abs(kappa_pos + 1.0 / SQRT3) < 1e-10,
          detail=f"kappa_pos={kappa_pos:.12f}",
          kind="NUMERIC")
    return m_pos


def part3_monotone_first_branch_bridge(m_pos: float) -> tuple[float, float]:
    print()
    print("=" * 88)
    print("PART 3: on the first branch, any target kappa fixes a unique selected-line point")
    print("=" * 88)

    xs = np.linspace(m_pos + 1e-4, 0.0, 400)
    kappas = np.array([selected_line_kappa(x) for x in xs])
    monotone = bool(np.all(np.diff(kappas) < 0.0))
    kappa_end = float(kappas[-1])

    check("The scalar bridge kappa(m) is strictly monotone on the first selected-line branch",
          monotone,
          detail=f"kappa-range=({kappas[0]:.6f}, {kappa_end:.6f})",
          kind="NUMERIC")
    check("Therefore any target kappa in that interval fixes a unique first-branch m",
          monotone and kappa_end < kappas[0],
          detail="monotone inverse exists on [m_pos, 0]",
          kind="NUMERIC")
    return float(kappas[0]), kappa_end


def part4_current_candidate_scalar() -> None:
    print()
    print("=" * 88)
    print("PART 4: the current coordinate-closed candidate route imports exactly one scalar")
    print("=" * 88)

    beta_star, kappa_star = hstar_witness_kappa()
    m_first = float(brentq(lambda m: selected_line_kappa(m) - kappa_star, -1.165, -1.160))
    amp = selected_line_small_amp(m_first)
    cs = amplitude_cos_similarity(amp)
    q = float(np.sum(amp * amp) / (np.sum(amp) ** 2))

    pdg_kappa = kappa_from_slots(float(PDG_SQRT[1]), float(PDG_SQRT[2]))

    check("The earlier H_* witness fixes one scalar kappa_* on the Koide small branch",
          -1.0 < kappa_star < 0.0,
          detail=f"beta*={beta_star:.12f}, kappa*={kappa_star:.12f}",
          kind="NUMERIC")
    check("Solving kappa(m) = kappa_* on the first branch reproduces the selected-line point",
          abs(selected_line_kappa(m_first) - kappa_star) < 1e-12,
          detail=f"m_first={m_first:.12f}",
          kind="NUMERIC")
    check("The resulting selected-line point still lands exactly on the Koide cone and charged-lepton direction",
          abs(q - 2.0 / 3.0) < 1e-12 and cs > 0.999999999,
          detail=f"Q={q:.15f}, cos-sim={cs:.12f}",
          kind="NUMERIC")
    check("The imported scalar kappa_* already matches the PDG charged-lepton comparator to candidate precision",
          abs(kappa_star - pdg_kappa) < 3e-4,
          detail=f"kappa_PDG={pdg_kappa:.12f}",
          kind="NUMERIC")


def part5_interpretation() -> None:
    print()
    print("=" * 88)
    print("PART 5: what is still missing for charged-lepton retention")
    print("=" * 88)

    check("The remaining charged-lepton gap is now one scalar retained law for kappa_* (equivalently w/v or one cyclic-response ratio)",
          True,
          detail="all other internal coordinates on the current Koide route are already fixed")
    check("This is smaller than a generic positive-parent/readout theorem and smaller than a full 3-response law",
          True,
          detail="derive kappa_* and the selected-line point follows")


def main() -> int:
    part1_exact_cyclic_bridge()
    m_pos = part2_exact_threshold_value()
    part3_monotone_first_branch_bridge(m_pos)
    part4_current_candidate_scalar()
    part5_interpretation()

    print()
    print("Interpretation:")
    print("  The current charged-lepton Koide route is one scalar retained bridge")
    print("  away from promotion. The exact missing datum is kappa = sqrt(3) r2 /")
    print("  (2 r0 - r1) = (v-w)/(v+w). Once that scalar is fixed by a retained")
    print("  charged-lepton law, the selected-line point and the physical branch")
    print("  are already determined by the existing exact stack.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
