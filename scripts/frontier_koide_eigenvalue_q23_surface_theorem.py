#!/usr/bin/env python3
"""
Koide eigenvalue Q=2/3 surface theorem.

Purpose:
  Test the strongest M2-style escape hatch below the current charged-lepton
  lane: replace the slot-diagonal readout by the eigenvalues of exp(beta H_sel(m))
  and impose Koide Q=2/3 there.

Main outcome:
  this does not close Koide natively. For every fixed selected-line H_sel(m)
  with non-scalar spectrum, the eigenvalue purity

      Q_eig(beta) = sum_i exp(2 beta lambda_i) / (sum_i exp(beta lambda_i))^2

  is strictly increasing in beta, so Q_eig = 2/3 cuts a unique beta value.
  On the physical selected line this yields a 1-real monotone surface
  beta = beta_q23(m), not a distinguished point m_*.

  So the eigenvalue route is an exact reparameterized support surface that still
  needs an independent beta-law. It does not derive Q=2/3 from retained data.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

from frontier_higgs_dressed_propagator_v1 import DELTA_STAR, E1, GAMMA, H3, M_STAR, Q_PLUS_STAR
from frontier_koide_selected_line_cyclic_response_bridge import (
    hstar_witness_kappa,
    koide_root_pair,
    selected_line_slots,
)


PASS_COUNT = 0
FAIL_COUNT = 0

SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)
SELECTOR = SQRT6 / 3.0
M_STAR_SEL = -1.160469470087
M_POS = -1.2957949040672103

PDG_SQRT = np.sqrt(np.array([0.51099895, 105.6583755, 1776.86], dtype=float))
PDG_DIR = PDG_SQRT / np.linalg.norm(PDG_SQRT)


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT", cls: str = "A") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status} ({cls})]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def h_sel(m: float) -> np.ndarray:
    return H3(m, SELECTOR, SELECTOR)


def q_eig_from_lambdas(lambdas: np.ndarray, beta: float) -> float:
    weights = np.exp(beta * np.asarray(lambdas, dtype=float))
    return float(np.dot(weights, weights) / np.sum(weights) ** 2)


def q_eig_derivative_from_lambdas(lambdas: np.ndarray, beta: float) -> float:
    lambdas = np.asarray(lambdas, dtype=float)
    weights = np.exp(beta * lambdas)
    z = float(np.sum(weights))
    pair_sum = 0.0
    for i in range(len(lambdas)):
        for j in range(i + 1, len(lambdas)):
            pair_sum += (
                2.0
                * (lambdas[j] - lambdas[i])
                * weights[i]
                * weights[j]
                * (weights[j] - weights[i])
            )
    return pair_sum / (z**3)


def q_eig(h: np.ndarray, beta: float) -> float:
    return q_eig_from_lambdas(np.linalg.eigvalsh(h), beta)


def beta_for_q23(h: np.ndarray, beta_lo: float = 1.0e-4, beta_hi: float = 8.0) -> float:
    target = 2.0 / 3.0
    return float(brentq(lambda beta: q_eig(h, beta) - target, beta_lo, beta_hi))


def m_for_beta_q23(
    beta: float, m_lo: float = M_POS + 0.003, m_hi: float = -0.05
) -> float | None:
    target = 2.0 / 3.0
    f_lo = q_eig(h_sel(m_lo), beta) - target
    f_hi = q_eig(h_sel(m_hi), beta) - target
    if not np.isfinite(f_lo) or not np.isfinite(f_hi) or f_lo * f_hi > 0.0:
        return None
    return float(brentq(lambda m: q_eig(h_sel(m), beta) - target, m_lo, m_hi))


def amplitude_cos_similarity(m: float) -> float:
    v, w = selected_line_slots(m)
    u_small, _ = koide_root_pair(v, w)
    amp = np.array([u_small, v, w], dtype=float)
    return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))


def part1_exact_monotonicity_identity() -> None:
    print("=" * 88)
    print("PART 1: exact monotonicity identity for the eigenvalue Q surface")
    print("=" * 88)

    a1, a2, a3, l1, l2, l3 = sp.symbols("a1 a2 a3 l1 l2 l3", positive=True, real=True)
    a = [a1, a2, a3]
    l = [l1, l2, l3]
    z = sum(a)
    q_num = sum(x * x for x in a)
    dq_num = 2 * (sum(li * ai * ai for li, ai in zip(l, a)) * z - q_num * sum(li * ai for li, ai in zip(l, a)))
    pair_form = 2 * sum(
        (l[j] - l[i]) * a[i] * a[j] * (a[j] - a[i])
        for i in range(3)
        for j in range(i + 1, 3)
    )

    check(
        "For three eigenvalues, dQ_eig/dbeta has the exact pairwise-positive numerator form",
        sp.expand(dq_num - pair_form) == 0,
        detail="dQ = 2 sum_{i<j} (lambda_j-lambda_i) a_i a_j (a_j-a_i) / Z^3",
    )
    sample_spectra = [
        np.array([-1.7, -0.4, 0.9], dtype=float),
        np.array([-2.1, -0.3, 1.2], dtype=float),
        np.array([-0.9, 0.2, 1.7], dtype=float),
    ]
    beta_grid = np.linspace(0.05, 1.50, 16)
    check(
        "So any fixed non-scalar spectrum gives a strictly increasing eigenvalue Q curve in beta > 0",
        all(
            q_eig_derivative_from_lambdas(lambdas, float(beta)) > 0.0
            for lambdas in sample_spectra
            for beta in beta_grid
        ),
        detail="verified numerically on representative ordered non-scalar spectra",
        kind="NUMERIC",
    )


def part2_selected_line_surface_uniqueness() -> None:
    print()
    print("=" * 88)
    print("PART 2: on the selected line, Q_eig = 2/3 gives a unique beta surface")
    print("=" * 88)

    ms = np.linspace(M_POS + 0.003, -0.05, 120)
    beta_samples = np.linspace(0.02, 2.00, 80)

    strict_top_gap = float("inf")
    derivative_min = float("inf")
    curve = []
    monotone_ok = True
    endpoint_ok = True

    for m in ms:
        lambdas = np.linalg.eigvalsh(h_sel(float(m)))
        strict_top_gap = min(strict_top_gap, float(lambdas[-1] - lambdas[-2]))
        derivative_vals = [q_eig_derivative_from_lambdas(lambdas, float(beta)) for beta in beta_samples]
        derivative_min = min(derivative_min, min(derivative_vals))
        monotone_ok &= all(val > 0.0 for val in derivative_vals)

        q0 = q_eig_from_lambdas(lambdas, 0.0)
        qhi = q_eig_from_lambdas(lambdas, 8.0)
        endpoint_ok &= abs(q0 - 1.0 / 3.0) < 1.0e-14 and qhi > 0.999

        beta_q23 = beta_for_q23(h_sel(float(m)))
        curve.append((float(m), beta_q23))

    betas = np.array([beta for _m, beta in curve], dtype=float)

    check(
        "The selected-line spectrum keeps a simple largest eigenvalue on the whole physical branch",
        strict_top_gap > 1.0e-3,
        detail=f"min top-gap={strict_top_gap:.6e}",
        kind="NUMERIC",
        cls="C",
    )
    check(
        "For every tested selected-line spectrum, dQ_eig/dbeta stays strictly positive on beta in [0.02, 2]",
        monotone_ok and derivative_min > 0.0,
        detail=f"min derivative={derivative_min:.6e}",
        kind="NUMERIC",
        cls="C",
    )
    check(
        "Hence each selected-line point has one unique beta with Q_eig = 2/3",
        endpoint_ok and len(curve) == len(ms),
        detail=f"{len(curve)} unique roots on {len(ms)} tested m values",
        kind="NUMERIC",
        cls="C",
    )
    check(
        "The eigenvalue condition is a dense one-real surface beta_q23(m), not a singled-out point",
        float(np.max(betas) - np.min(betas)) > 0.1,
        detail=f"beta range=[{np.min(betas):.6f}, {np.max(betas):.6f}]",
        kind="NUMERIC",
        cls="C",
    )


def part3_no_framework_beta_closure() -> None:
    print()
    print("=" * 88)
    print("PART 3: tested framework-native beta values do not close the surface at m_*")
    print("=" * 88)

    beta_star, _kappa_star = hstar_witness_kappa()
    candidates = [
        ("GAMMA = 1/2", GAMMA),
        ("SELECTOR = sqrt(6)/3", SELECTOR),
        ("1/E1 = sqrt(3/8)", 1.0 / E1),
        ("1/sqrt(3)", 1.0 / SQRT3),
        ("beta_star (gamma-orbit witness)", beta_star),
        ("2/3", 2.0 / 3.0),
        ("sqrt(2)/3", math.sqrt(2.0) / 3.0),
    ]

    print(f"  {'Candidate':38s} {'beta':>10s}  {'m on Q_eig=2/3':>16s}  {'|m-m_*|':>12s}  {'cos-sim':>10s}")
    print(f"  {'-'*38} {'-'*10}  {'-'*16}  {'-'*12}  {'-'*10}")

    gaps = []
    for name, beta in candidates:
        m = m_for_beta_q23(beta)
        if m is None:
            print(f"  {name:38s} {beta:10.6f}  {'no crossing':>16s}")
            continue
        gap = abs(m - M_STAR_SEL)
        gaps.append(gap)
        cs = amplitude_cos_similarity(m)
        print(f"  {name:38s} {beta:10.6f}  {m:16.8f}  {gap:12.4e}  {cs:10.8f}")

    best_gap = min(gaps)
    check(
        "No tested framework-native beta constant lands on m_* along the eigenvalue Q surface",
        best_gap > 4.0e-2,
        detail=f"best gap={best_gap:.4e}",
        kind="NUMERIC",
        cls="C",
    )

    h = h_sel(M_STAR_SEL)
    beta_q23 = beta_for_q23(h)
    print()
    print(f"  At m_* = {M_STAR_SEL:.12f}: beta_q23 = {beta_q23:.10f}, beta_star = {beta_star:.10f}")
    check(
        "The eigenvalue-surface beta at m_* is distinct from the current slot-route beta witness",
        abs(beta_q23 - beta_star) > 1.0e-2,
        detail=f"|beta_q23-beta_star|={abs(beta_q23-beta_star):.6f}",
        kind="NUMERIC",
        cls="C",
    )


def main() -> int:
    part1_exact_monotonicity_identity()
    part2_selected_line_surface_uniqueness()
    part3_no_framework_beta_closure()

    print()
    print("Summary:")
    print("  The M2 eigenvalue escape hatch does not natively close Koide Q=2/3.")
    print("  It yields an exact monotone surface beta = beta_q23(m) on the selected line,")
    print("  and still needs an independent beta-law to isolate m_*.")
    print("  So this route is a support surface, not a retained derivation.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
