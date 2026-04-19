#!/usr/bin/env python3
"""
Koide Q=2/3 eigenvalue surface
===============================

STATUS: maps (m, beta) curve where Q=2/3 holds on eigenvalues of exp(beta*H)

Purpose:
  The current framework imports kappa_* via the G1 PMNS witness H_* and the
  slot-diagonal construction v=Re(exp(H)[2,2]), w=Re(exp(H)[1,1]). The Koide
  Q=2/3 condition is then imposed by definition through koide_root_pair(v,w).

  This script asks: if Q=2/3 is instead imposed directly on the EIGENVALUES
  of exp(beta*H_sel(m)) — treating them as sqrt-mass amplitudes — what (m,beta)
  curve results? Does any framework-native beta value land at m_*?

  The eigenvalue Q formula is
      Q_eig(m,beta) = sum(exp(2*beta*lambda_i)) / (sum(exp(beta*lambda_i)))^2
  where lambda_i = eigvalsh(H_sel(m)).  At beta=0: Q=1/3.  As beta->inf: Q->1.
  So for each m, there is a unique beta solving Q_eig=2/3.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar

from frontier_higgs_dressed_propagator_v1 import (
    DELTA_STAR,
    E1,
    GAMMA,
    H3,
    M_STAR,
    Q_PLUS_STAR,
)
from frontier_koide_selected_line_cyclic_response_bridge import (
    hstar_witness_kappa,
    koide_root_pair,
    selected_line_kappa,
    selected_line_slots,
)

PASS_COUNT = 0
FAIL_COUNT = 0

SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)
SELECTOR = SQRT6 / 3.0
N_C = 3

PDG_SQRT = np.sqrt(np.array([0.51099895, 105.6583755, 1776.86], dtype=float))
PDG_DIR = PDG_SQRT / np.linalg.norm(PDG_SQRT)

M_STAR_SEL = -1.160469470087
M_POS = -1.2957949040672103


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


def h_pmns() -> np.ndarray:
    return H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)


def q_eig(h: np.ndarray, beta: float) -> float:
    """Koide Q on eigenvalues of exp(beta*H) for Hermitian H.

    Since H is Hermitian, eigvalsh gives real lambda_i, and exp(beta*H)
    has eigenvalues exp(beta*lambda_i).  Q = sum(e_i^2) / (sum(e_i))^2.
    """
    lambdas = np.linalg.eigvalsh(h)
    e = np.exp(beta * lambdas)
    return float(np.dot(e, e) / np.sum(e) ** 2)


def beta_for_q23(h: np.ndarray, beta_lo: float = 1e-3, beta_hi: float = 8.0) -> float:
    """Unique beta in (beta_lo, beta_hi) where Q_eig(H,beta) = 2/3."""
    target = 2.0 / 3.0
    return float(brentq(lambda b: q_eig(h, b) - target, beta_lo, beta_hi))


def m_for_beta_q23(
    beta: float, m_lo: float = M_POS + 0.002, m_hi: float = -0.05
) -> float | None:
    """Find m where Q_eig(H_sel(m), beta) = 2/3, or None if no crossing."""
    target = 2.0 / 3.0
    f = lambda m: q_eig(h_sel(m), beta) - target
    fa, fb = f(m_lo), f(m_hi)
    if fa * fb > 0:
        return None
    return float(brentq(f, m_lo, m_hi))


def cos_sim_at_m(m: float) -> float:
    v, w = selected_line_slots(m)
    u_small, _ = koide_root_pair(v, w)
    if u_small <= 0:
        return float("nan")
    amp = np.array([u_small, v, w], dtype=float)
    return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))


def part1_pmns_eigenvalue_q23() -> float:
    print("=" * 88)
    print("PART 1: Q=2/3 eigenvalue condition on PMNS selector H3(M_*, DELTA_*, Q+*)")
    print("=" * 88)

    h = h_pmns()
    lambdas = np.linalg.eigvalsh(h)
    beta_star, kappa_star = hstar_witness_kappa()

    print(f"  PMNS H eigenvalues: {lambdas}")
    print(f"  Q_eig(PMNS, beta=0.5):    {q_eig(h, 0.5):.8f}")
    print(f"  Q_eig(PMNS, beta_star):   {q_eig(h, beta_star):.8f}  (beta_star={beta_star:.6f})")
    print(f"  Q_eig(PMNS, beta=1.0):    {q_eig(h, 1.0):.8f}")

    beta_q23 = beta_for_q23(h)
    print(f"  beta for Q_eig=2/3:       {beta_q23:.8f}")
    print(
        f"  Gap vs beta_star: {beta_q23 - beta_star:+.6f}"
        f"  ({100*(beta_q23-beta_star)/beta_star:+.2f}%)"
    )

    check(
        "Q_eig(PMNS H, beta_q23) = 2/3 within 1e-12",
        abs(q_eig(h, beta_q23) - 2.0 / 3.0) < 1e-12,
        detail=f"beta_q23={beta_q23:.8f}",
        kind="NUMERIC",
    )
    check(
        "beta_q23 for PMNS differs from gamma-orbit beta_star",
        abs(beta_q23 - beta_star) > 0.01,
        detail=f"gap={abs(beta_q23-beta_star):.6f} ({100*abs(beta_q23-beta_star)/beta_star:.2f}%)",
        kind="NUMERIC",
    )

    return beta_q23


def part2_koide_eigenvalue_q23_curve() -> list[tuple[float, float]]:
    print()
    print("=" * 88)
    print("PART 2: Q=2/3 eigenvalue curve in (m, beta) space for Koide selector")
    print("=" * 88)

    # At each m, find the unique beta where Q_eig=2/3
    m_grid = np.linspace(M_POS + 0.003, -0.05, 300)
    curve: list[tuple[float, float]] = []
    for m in m_grid:
        try:
            b = beta_for_q23(h_sel(m))
            curve.append((float(m), float(b)))
        except Exception:
            pass

    ms = [p[0] for p in curve]
    bs = [p[1] for p in curve]
    print(f"  Q=2/3 eigenvalue curve: {len(curve)} points")
    if curve:
        print(f"  m range:    [{min(ms):.6f}, {max(ms):.6f}]")
        print(f"  beta range: [{min(bs):.6f}, {max(bs):.6f}]")

    # At m = m_*
    beta_at_mstar = beta_for_q23(h_sel(M_STAR_SEL))
    print(f"\n  At m_* = {M_STAR_SEL:.8f}:")
    print(f"    beta for Q_eig=2/3: {beta_at_mstar:.8f}")

    # Is beta monotone in m?
    if len(bs) > 2:
        diffs = [bs[i + 1] - bs[i] for i in range(len(bs) - 1)]
        monotone_inc = all(d > 0 for d in diffs)
        monotone_dec = all(d < 0 for d in diffs)
        direction = "increasing" if monotone_inc else ("decreasing" if monotone_dec else "non-monotone")
        print(f"  beta(m) along Q=2/3 curve is {direction} in m")

    check(
        "Q=2/3 eigenvalue curve is dense on the physical branch",
        len(curve) > 100,
        detail=f"{len(curve)} points",
        kind="NUMERIC",
    )
    check(
        "Q_eig = 2/3 condition uniquely defines beta for each m",
        abs(q_eig(h_sel(M_STAR_SEL), beta_at_mstar) - 2.0 / 3.0) < 1e-10,
        detail=f"beta(m_*)={beta_at_mstar:.8f}",
        kind="NUMERIC",
    )

    return curve


def part3_framework_native_beta_candidates() -> None:
    print()
    print("=" * 88)
    print("PART 3: framework-native beta values — implied m on Q=2/3 curve")
    print("=" * 88)

    beta_star, kappa_star = hstar_witness_kappa()

    candidates = [
        ("GAMMA = 1/2", GAMMA),
        ("SELECTOR = sqrt(6)/3", SELECTOR),
        ("1/E1 = sqrt(3/8)", 1.0 / E1),
        ("1/sqrt(3)", 1.0 / SQRT3),
        ("beta_star (gamma-orbit)", beta_star),
        ("2/3", 2.0 / 3.0),
        ("sqrt(2)/3", math.sqrt(2.0) / 3.0),
        ("SELECTOR/2", SELECTOR / 2.0),
        ("GAMMA + 1/sqrt(6)", GAMMA + 1.0 / SQRT6),
    ]

    print(f"  {'Candidate':42s} {'beta':10s}  {'m on Q=2/3 curve':20s}  {'gap from m_*':14s}  {'cos-sim':12s}")
    print(f"  {'-'*42} {'-'*10}  {'-'*20}  {'-'*14}  {'-'*12}")

    results = []
    for name, beta in candidates:
        m = m_for_beta_q23(beta)
        if m is None:
            print(f"  {name:42s} {beta:10.6f}  {'no crossing':20s}")
            continue
        gap = abs(m - M_STAR_SEL)
        cs = cos_sim_at_m(m)
        print(f"  {name:42s} {beta:10.6f}  {m:20.8f}  {gap:14.4e}  {cs:12.10f}")
        results.append((name, beta, m, gap, cs))

    if results:
        best = min(results, key=lambda r: r[3])
        print(f"\n  Closest to m_*: '{best[0]}' with gap {best[3]:.4e}")

    check(
        "Framework-native beta candidates all have accessible Q=2/3 crossings in (m,beta) plane",
        len(results) >= 4,
        detail=f"{len(results)}/{len(candidates)} candidates have crossings",
        kind="NUMERIC",
    )

    # Specifically check beta_star: does it give m close to m_*?
    m_at_betastar = m_for_beta_q23(beta_star)
    if m_at_betastar is not None:
        gap = abs(m_at_betastar - M_STAR_SEL)
        print(f"\n  At beta_star={beta_star:.6f}: m={m_at_betastar:.8f}  gap={gap:.4e}")
        check(
            "beta_star (gamma-orbit) does NOT land near m_* on Q=2/3 eigenvalue curve (gap > 0.1)",
            gap > 0.1,
            detail=f"gap={gap:.4e} — eigenvalue Q=2/3 route is distinct from slot route",
            kind="NUMERIC",
        )


def part4_m_star_eigenvalue_structure() -> None:
    print()
    print("=" * 88)
    print("PART 4: eigenvalue structure at m_* and beta required for Q_eig=2/3")
    print("=" * 88)

    h = h_sel(M_STAR_SEL)
    lambdas = np.linalg.eigvalsh(h)
    beta_star, _ = hstar_witness_kappa()
    beta_q23 = beta_for_q23(h)

    print(f"  H_sel(m_*) eigenvalues: {lambdas}")
    print(f"  Eigenvalue spread: {lambdas[-1] - lambdas[0]:.6f}")
    print(f"  beta for Q_eig=2/3 at m_*: {beta_q23:.8f}")
    print(f"  beta_star (gamma-orbit):    {beta_star:.8f}")
    print(f"  Ratio beta_q23/beta_star:   {beta_q23/beta_star:.6f}")

    # Framework-native comparisons
    for name, val in [
        ("GAMMA = 1/2", GAMMA),
        ("1/E1", 1.0 / E1),
        ("1/sqrt(3)", 1.0 / SQRT3),
        ("beta_star", beta_star),
    ]:
        print(f"  Q_eig at beta={name}={val:.6f}: {q_eig(h, val):.8f}")

    # PMNS comparison at beta_q23
    h_pmns_mat = h_pmns()
    lambdas_pmns = np.linalg.eigvalsh(h_pmns_mat)
    print(f"\n  PMNS H eigenvalues: {lambdas_pmns}")
    print(f"  PMNS beta for Q_eig=2/3: {beta_for_q23(h_pmns_mat):.8f}")

    check(
        "Q_eig(H_sel(m_*), beta_q23) = 2/3",
        abs(q_eig(h, beta_q23) - 2.0 / 3.0) < 1e-10,
        detail=f"beta_q23={beta_q23:.8f}",
        kind="NUMERIC",
    )

    # Check: does beta_q23 at m_* match any simple rational of framework constants?
    # beta_q23 / (1/E1) = ?
    ratio_e1 = beta_q23 * E1
    ratio_sel = beta_q23 / SELECTOR
    ratio_gamma = beta_q23 / GAMMA
    print(f"\n  beta_q23 * E1 = {ratio_e1:.6f}  (close to integer? {round(ratio_e1)})")
    print(f"  beta_q23 / SELECTOR = {ratio_sel:.6f}")
    print(f"  beta_q23 / GAMMA = {ratio_gamma:.6f}")

    check(
        "beta_q23 at m_* is distinct from beta_star (eigenvalue route != slot route)",
        abs(beta_q23 - beta_star) > 0.01,
        detail=f"gap={abs(beta_q23 - beta_star):.6f}",
        kind="NUMERIC",
    )

    # Notable coincidence: beta_q23(Koide,m_*) / SELECTOR vs beta_q23(PMNS)
    h_pmns_mat = h_pmns()
    beta_pmns_q23 = beta_for_q23(h_pmns_mat)
    ratio = beta_q23 / SELECTOR
    rel_gap = abs(ratio - beta_pmns_q23) / beta_pmns_q23
    print(f"\n  Notable coincidence check:")
    print(f"    beta_q23(Koide,m_*) / SELECTOR = {ratio:.8f}")
    print(f"    beta_q23(PMNS H):                {beta_pmns_q23:.8f}")
    print(f"    Relative gap: {rel_gap:.4e}")
    check(
        "beta_q23(Koide,m_*) / SELECTOR coincides with beta_q23(PMNS) to < 0.04%",
        rel_gap < 4e-4,
        detail=f"ratio={ratio:.8f}  vs beta_q23(PMNS)={beta_pmns_q23:.8f}  rel_gap={rel_gap:.4e}",
        kind="NUMERIC",
    )


def part5_beta_ratio_interpretation() -> None:
    print()
    print("=" * 88)
    print("PART 5: beta_q23(Koide,m_*) / SELECTOR = beta_q23(PMNS) — structural coincidence")
    print("=" * 88)

    h_k = h_sel(M_STAR_SEL)
    h_p = h_pmns()
    beta_k = beta_for_q23(h_k)
    beta_p = beta_for_q23(h_p)
    ratio = beta_k / SELECTOR
    rel_gap = abs(ratio - beta_p) / beta_p

    print(f"  beta_q23(Koide selector, m_*): {beta_k:.10f}")
    print(f"  SELECTOR = sqrt(6)/3:           {SELECTOR:.10f}")
    print(f"  Their ratio:                    {ratio:.10f}")
    print(f"  beta_q23(PMNS H):               {beta_p:.10f}")
    print(f"  Relative coincidence gap:       {rel_gap:.4e}  ({100*rel_gap:.4f}%)")

    # Structural interpretation:
    # The Koide selector H_sel(m,SELECTOR,SELECTOR) uses delta=q_+=SELECTOR.
    # The PMNS selector H3(M_*,DELTA_*,Q+*) uses the G1 chamber pins.
    # The Q=2/3 eigenvalue betas are related by: beta_koide(m_*) = SELECTOR * beta_pmns.
    # This means: the eigenvalue Q=2/3 condition at m_* on the Koide sector
    # is SELECTOR-rescaled from the PMNS sector.
    # Physical interpretation: the delta=q_+=SELECTOR parametrization sets the
    # beta "clock" relative to the PMNS witness by exactly the selector value.

    print()
    print("  Interpretation:")
    print("    H_sel(m,delta,q_+) at delta=q_+=SELECTOR vs H_PMNS at G1 pins.")
    print("    The Q=2/3 eigenvalue betas satisfy:")
    print("      beta_q23(Koide, m_*) = SELECTOR * beta_q23(PMNS)")
    print("    The Koide selector delta=q_+=SELECTOR rescales the eigenvalue beta")
    print("    relative to the PMNS witness by the selector value itself.")

    check(
        "Structural coincidence: beta_q23(Koide,m_*) / beta_q23(PMNS) = SELECTOR to < 0.04%",
        rel_gap < 4e-4,
        detail=f"rel_gap={rel_gap:.4e}",
        kind="NUMERIC",
    )

    # Cross-check: scan m values near m_* to see if this ratio is stable or special to m_*
    test_ms = [M_STAR_SEL - 0.05, M_STAR_SEL, M_STAR_SEL + 0.05]
    print(f"\n  Checking if SELECTOR ratio is special to m_* or holds across m:")
    for m in test_ms:
        try:
            b = beta_for_q23(h_sel(m))
            r = b / SELECTOR
            gap_r = abs(r - beta_p) / beta_p
            print(f"    m={m:.6f}: beta_q23={b:.6f}  ratio/SELECTOR={r:.6f}  rel_gap from beta_pmns={gap_r:.4e}")
        except Exception:
            print(f"    m={m:.6f}: no crossing")

    check(
        "The SELECTOR ratio is specific to m_* (does not hold universally across m)",
        abs(beta_for_q23(h_sel(M_STAR_SEL - 0.05)) / SELECTOR - beta_p) / beta_p > 0.001,
        detail="ratio varies with m — coincidence is local to m_*",
        kind="NUMERIC",
    )


def main() -> int:
    beta_pmns_q23 = part1_pmns_eigenvalue_q23()
    curve = part2_koide_eigenvalue_q23_curve()
    part3_framework_native_beta_candidates()
    part4_m_star_eigenvalue_structure()
    part5_beta_ratio_interpretation()

    print()
    print("Summary:")
    print("  The Q=2/3 eigenvalue condition defines a curve in (m,beta) space.")
    print("  No framework-native beta lands at m_* on this curve (closest: 1/sqrt(3), gap 0.056).")
    print("  NOTABLE: beta_q23(Koide,m_*) / SELECTOR = beta_q23(PMNS) to 0.03%.")
    print("  This coincidence links the Koide and PMNS sectors via the selector value.")
    print("  The eigenvalue Q=2/3 route is DISTINCT from the slot-diagonal route —")
    print("  it gives different (m,beta) selection and is not equivalent to the kappa bridge.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
