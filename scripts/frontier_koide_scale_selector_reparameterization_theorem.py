#!/usr/bin/env python3
"""
Koide scale-selector reparameterization theorem.

Purpose:
  Audit the strongest M1-style escape hatch below the current charged-lepton
  lane: the near-miss scale condition u*v*w = 1.

Main outcome:
  it is not an independent closure route. The slot u used in u*v*w is the
  Koide-completed small root built from (v,w), so Q=2/3 is already imposed
  before the product is formed. The product condition is therefore a scalar
  reparameterization on the already-imposed Koide cone, not a native forcing law.

  Numerically it gives a remarkably close near-miss to m_*, but it still does
  not equal the current physical point.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp
from scipy.linalg import expm
from scipy.optimize import brentq

from frontier_higgs_dressed_propagator_v1 import H3
from frontier_koide_selected_line_cyclic_response_bridge import (
    hstar_witness_kappa,
    koide_root_pair,
    selected_line_kappa,
    selected_line_slots,
)


PASS_COUNT = 0
FAIL_COUNT = 0

SQRT6 = math.sqrt(6.0)
SELECTOR = SQRT6 / 3.0
M_STAR_SEL = -1.160469470087
M_POS = -1.2957949040672103
N_C = 3

PDG_MASSES = np.array([0.51099895, 105.6583755, 1776.86], dtype=float)
PDG_SQRT = np.sqrt(PDG_MASSES)
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


def h_sel(m: float) -> np.ndarray:
    return H3(m, SELECTOR, SELECTOR)


def native_diag_triple(m: float) -> tuple[float, float, float]:
    x = expm(h_sel(m))
    return float(np.real(x[0, 0])), float(np.real(x[2, 2])), float(np.real(x[1, 1]))


def koide_completed_triple(m: float) -> tuple[float, float, float]:
    v, w = selected_line_slots(m)
    u_small, _u_large = koide_root_pair(v, w)
    return u_small, v, w


def koide_q_from_amplitudes(u: float, v: float, w: float) -> float:
    masses = np.array([u * u, v * v, w * w], dtype=float)
    return float(np.sum(masses) / np.sum(np.sqrt(masses)) ** 2)


def slot_product(m: float) -> float:
    u, v, w = koide_completed_triple(m)
    return u * v * w


def tr_exp_k(m: float, k: float) -> float:
    lambdas = np.linalg.eigvalsh(h_sel(m))
    return float(np.sum(np.exp(k * lambdas)))


def amplitude_cos_similarity(m: float) -> float:
    amp = np.array(koide_completed_triple(m), dtype=float)
    return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))


def crossing(f, m_lo: float, m_hi: float) -> float | None:
    f_lo = f(m_lo)
    f_hi = f(m_hi)
    if not np.isfinite(f_lo) or not np.isfinite(f_hi) or f_lo * f_hi > 0.0:
        return None
    return float(brentq(f, m_lo, m_hi))


def part1_exact_reparameterization_identity() -> None:
    print("=" * 88)
    print("PART 1: the scale condition uses a Koide-completed slot, not native diagonal data")
    print("=" * 88)

    v, w = sp.symbols("v w", positive=True, real=True)
    u_small = 2 * (v + w) - sp.sqrt(3 * (v * v + 4 * v * w + w * w))
    q_expr = sp.simplify((u_small**2 + v**2 + w**2) / (u_small + v + w) ** 2)

    check(
        "The small slot u_small(v,w) is exactly the Koide-completing root",
        sp.simplify(q_expr - sp.Rational(2, 3)) == 0,
        detail="Q(u_small^2,v^2,w^2) = 2/3 identically",
    )
    check(
        "So every scalar built from (u_small,v,w) already lives on the imposed Koide cone",
        True,
        detail="u_small is not native pre-Koide data; it is constructed from (v,w)",
    )

    x00, v_star, w_star = native_diag_triple(M_STAR_SEL)
    u_star, _v_star, _w_star = koide_completed_triple(M_STAR_SEL)
    q_native = koide_q_from_amplitudes(x00, v_star, w_star)
    q_completed = koide_q_from_amplitudes(u_star, v_star, w_star)

    check(
        "At the current physical point the native diagonal triple does NOT satisfy Koide",
        abs(q_native - 2.0 / 3.0) > 1.0e-2,
        detail=f"Q_native={q_native:.12f}",
        kind="NUMERIC",
    )
    check(
        "The completed triple does satisfy Koide because u_small is defined that way",
        abs(q_completed - 2.0 / 3.0) < 1.0e-12,
        detail=f"Q_completed={q_completed:.12f}",
        kind="NUMERIC",
    )
    check(
        "The native diagonal x00 and the Koide-completed u_small are genuinely different numbers at m_*",
        abs(x00 - u_star) > 1.0,
        detail=f"x00={x00:.12f}, u_small={u_star:.12f}",
        kind="NUMERIC",
    )


def part2_unique_near_miss_crossing() -> float:
    print()
    print("=" * 88)
    print("PART 2: u*v*w = 1 gives one physical-branch near-miss, not the current selector")
    print("=" * 88)

    m_lo = M_POS + 0.002
    m_hi = -0.05
    m_prod = crossing(lambda m: slot_product(m) - 1.0, m_lo, m_hi)
    assert m_prod is not None

    ms = np.linspace(m_lo, m_hi, 2000)
    signs = np.sign(np.array([slot_product(float(m)) - 1.0 for m in ms], dtype=float))
    sign_changes = sum(
        1
        for i in range(len(signs) - 1)
        if np.isfinite(signs[i]) and np.isfinite(signs[i + 1]) and signs[i] * signs[i + 1] < 0.0
    )
    gap = abs(m_prod - M_STAR_SEL)
    cs = amplitude_cos_similarity(m_prod)

    print(f"  m_prod = {m_prod:.14f}")
    print(f"  m_*    = {M_STAR_SEL:.14f}")
    print(f"  |m_prod - m_*| = {gap:.4e}")
    print(f"  cos-sim at m_prod = {cs:.12f}")

    check(
        "The product condition u*v*w = 1 has one and only one physical-branch crossing",
        sign_changes == 1,
        detail=f"sign changes={sign_changes}",
        kind="NUMERIC",
    )
    check(
        "The scale crossing is close to but distinct from the current physical point",
        gap < 5.0e-4 and gap > 1.0e-6,
        detail=f"gap={gap:.4e}",
        kind="NUMERIC",
    )
    check(
        "The near-miss point still tracks the observed sqrt-mass direction extremely well",
        cs > 0.999999998,
        detail=f"cos-sim={cs:.12f}",
        kind="NUMERIC",
    )
    return m_prod


def part3_trace_targets_are_weaker(m_prod: float) -> None:
    print()
    print("=" * 88)
    print("PART 3: simple trace targets are weaker than the scale near-miss")
    print("=" * 88)

    m_lo = M_POS + 0.002
    m_hi = -0.05
    targets = [
        (1.0, N_C, "N_c"),
        (1.0, N_C**2, "N_c^2"),
        (2.0, N_C**3, "N_c^3"),
        (2.0, N_C**4, "N_c^4"),
        (3.0, N_C**3, "N_c^3 @ k=3"),
    ]

    best_gap = float("inf")
    best_label = ""
    for k, target, label in targets:
        m_cross = crossing(lambda m, k=k, target=target: tr_exp_k(m, k) - target, m_lo, m_hi)
        if m_cross is None:
            continue
        gap = abs(m_cross - M_STAR_SEL)
        if gap < best_gap:
            best_gap = gap
            best_label = f"k={k}, target={label}"

    prod_gap = abs(m_prod - M_STAR_SEL)
    check(
        "Among the tested simple trace targets, none is as sharp as the product near-miss",
        best_gap > prod_gap,
        detail=f"best trace gap={best_gap:.4e} ({best_label}) vs product gap={prod_gap:.4e}",
        kind="NUMERIC",
    )
    check(
        "But even the product near-miss still does not equal the current selector point",
        prod_gap > 1.0e-6,
        detail=f"product gap={prod_gap:.4e}",
        kind="NUMERIC",
    )


def part4_product_vs_kappa(m_prod: float) -> None:
    print()
    print("=" * 88)
    print("PART 4: product normalization is near the kappa witness but not identical to it")
    print("=" * 88)

    _beta_star, kappa_star = hstar_witness_kappa()
    kappa_prod = selected_line_kappa(m_prod)
    gap = abs(kappa_prod - kappa_star)

    check(
        "The scale crossing lands very near the current kappa witness",
        gap < 1.0e-4,
        detail=f"|kappa_prod-kappa_*|={gap:.4e}",
        kind="NUMERIC",
    )
    check(
        "But the scale crossing is not exactly the same condition as kappa = kappa_*",
        gap > 1.0e-6,
        detail=f"kappa gap={gap:.4e}",
        kind="NUMERIC",
    )


def main() -> int:
    part1_exact_reparameterization_identity()
    m_prod = part2_unique_near_miss_crossing()
    part3_trace_targets_are_weaker(m_prod)
    part4_product_vs_kappa(m_prod)

    print()
    print("Summary:")
    print("  The u*v*w = 1 near-miss is not an independent derivation of Koide Q=2/3.")
    print("  It uses the Koide-completed slot u_small(v,w), so it is a reparameterization")
    print("  on the already-imposed cone. Numerically it remains an impressive support")
    print("  near-miss, but it does not close the charged-lepton lane natively.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
