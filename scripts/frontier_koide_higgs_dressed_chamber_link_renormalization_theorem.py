#!/usr/bin/env python3
"""
Frontier runner — Koide Higgs-dressed chamber-link renormalization theorem.

Companion to
`docs/KOIDE_HIGGS_DRESSED_CHAMBER_LINK_RENORMALIZATION_THEOREM_NOTE_2026-04-20.md`.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq

from frontier_higgs_dressed_propagator_v1 import (
    E1,
    GAMMA,
    H3,
    H_lift_missing_axis,
    M_STAR,
    DELTA_STAR,
    Q_PLUS_STAR,
    direction_cos,
    embed_4x4_to_16,
    koide_Q,
    sigma_with_weight_operator,
)


PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))


def hermitian_eigs(mat: np.ndarray) -> np.ndarray:
    herm = 0.5 * (mat + mat.conj().T)
    return np.linalg.eigvalsh(herm)


def sigma_and_resolvent(lambda_value: float, h0: float) -> tuple[np.ndarray, np.ndarray]:
    w4 = H_lift_missing_axis(h0)
    eigs, vecs = np.linalg.eigh(w4)
    if np.min(np.abs(lambda_value - eigs)) < 1.0e-10:
        raise ValueError("lambda at or too near a pole")
    resolvent = vecs @ np.diag(1.0 / (lambda_value - eigs)) @ vecs.conj().T
    sigma = sigma_with_weight_operator(embed_4x4_to_16(resolvent))
    return sigma, resolvent


def reached_principal_block(resolvent4: np.ndarray) -> np.ndarray:
    return np.array(
        [
            [resolvent4[3, 3], resolvent4[3, 2]],
            [resolvent4[2, 3], resolvent4[2, 2]],
        ],
        dtype=complex,
    )


def expected_sigma_from_resolvent(resolvent4: np.ndarray) -> np.ndarray:
    return np.array(
        [
            [resolvent4[0, 0], 0.0, 0.0],
            [0.0, resolvent4[3, 3], resolvent4[3, 2]],
            [0.0, resolvent4[2, 3], resolvent4[2, 2]],
        ],
        dtype=complex,
    )


def transport_scalars(lambda_value: float, h0: float) -> tuple[float, float, float, np.ndarray]:
    sigma, resolvent4 = sigma_and_resolvent(lambda_value, h0)
    block = reached_principal_block(resolvent4)
    x = 1.0 / (lambda_value - h0)
    t = float(np.trace(block).real)
    d = float(np.linalg.det(block).real)
    return x, t, d, sigma


def koide_balance_single_sqrt(x: float, t: float, d: float) -> float:
    root_d = math.sqrt(d)
    return (x + t - 4.0 * root_d) ** 2 - 16.0 * x * (t + 2.0 * root_d)


def koide_balance_quartic(x: float, t: float, d: float) -> float:
    return (
        x**4
        - 28.0 * t * x**3
        + (198.0 * t * t - 1568.0 * d) * x**2
        - (28.0 * t**3 + 1088.0 * d * t) * x
        + t**4
        - 32.0 * d * t * t
        + 256.0 * d * d
    )


def q_residual(lambda_value: float, h0: float) -> float:
    _, _, _, sigma = transport_scalars(lambda_value, h0)
    masses = np.abs(hermitian_eigs(sigma))
    return koide_Q(masses) - 2.0 / 3.0


def small_h0_root(lambda_value: float, lo: float = -2.0e-4, hi: float = 2.0e-4) -> float:
    grid = np.linspace(lo, hi, 2001)
    prev_x = None
    prev_v = None
    roots: list[float] = []
    for x in grid:
        v = q_residual(lambda_value, x)
        if not np.isfinite(v):
            prev_x = None
            prev_v = None
            continue
        if prev_v is not None and prev_v * v < 0.0:
            roots.append(brentq(lambda h0: q_residual(lambda_value, h0), prev_x, x))
        prev_x = x
        prev_v = v
    if len(roots) != 1:
        raise ValueError(f"expected unique small local h0 root, got {roots}")
    return roots[0]


def main() -> None:
    print("=" * 88)
    print("Koide Higgs-dressed chamber-link renormalization theorem")
    print("=" * 88)

    H_STAR = H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)
    lambda_slack = Q_PLUS_STAR + DELTA_STAR - E1
    lambda_star = 0.01580870328539511
    h0_slack = 4.489898313255e-05

    check(
        "The chamber slack scalar is exactly the visible real chamber-link entry Re(H_*[0,2])",
        abs(float(H_STAR[0, 2].real) - lambda_slack) < 1.0e-15,
        detail=f"Re(H13)={H_STAR[0,2].real:.15f}, lambda_slack={lambda_slack:.15f}",
    )
    check(
        "That same chamber-link entry carries the fixed imaginary half-gamma component",
        abs(float(H_STAR[0, 2].imag) + GAMMA) < 1.0e-15,
        detail=f"Im(H13)={H_STAR[0,2].imag:.15f}",
    )

    sigma_star, resolvent4_star = sigma_and_resolvent(lambda_star, 0.0)
    sigma_expected_star = expected_sigma_from_resolvent(resolvent4_star)
    check(
        "The species block is exactly the scalar O_0 channel plus the reached 2x2 principal resolvent block",
        np.allclose(sigma_star, sigma_expected_star, atol=1.0e-12),
    )

    block_star = reached_principal_block(resolvent4_star)
    chi_star = np.linalg.det(lambda_star * np.eye(3) - H_STAR)
    check(
        "Jacobi complement identity fixes det(B_lambda) by the complementary scalar channel",
        abs(np.linalg.det(block_star) - (lambda_star - M_STAR) / chi_star) < 1.0e-12,
        detail=f"det(B)={np.linalg.det(block_star).real:.12f}",
    )

    x_star, t_star, d_star, sigma_star = transport_scalars(lambda_star, 0.0)
    eigs_star = np.abs(hermitian_eigs(sigma_star))
    q_star = koide_Q(eigs_star)
    check(
        "The physical small positive root has positive transport spectrum",
        np.min(eigs_star) > 0.0,
        detail=f"eigs={np.round(eigs_star, 12).tolist()}",
    )
    check(
        "At that root the exact Koide condition holds on the transport spectrum",
        abs(q_star - 2.0 / 3.0) < 1.0e-12,
        detail=f"Q={q_star:.15f}, cos={direction_cos(eigs_star):.12f}",
    )
    check(
        "On the positive branch Koide is equivalent to the single-sqrt principal-block balance law",
        abs(koide_balance_single_sqrt(x_star, t_star, d_star)) < 1.0e-8,
        detail=f"balance={koide_balance_single_sqrt(x_star, t_star, d_star):+.3e}",
    )
    check(
        "The squared form is the quartic transport balance polynomial",
        abs(koide_balance_quartic(x_star, t_star, d_star)) < 1.0e-4,
        detail=f"quartic={koide_balance_quartic(x_star, t_star, d_star):+.3e}",
    )

    x_slack, t_slack, d_slack, sigma_slack = transport_scalars(lambda_slack, 0.0)
    q_slack = koide_Q(np.abs(hermitian_eigs(sigma_slack)))
    check(
        "The visible chamber-link scalar alone is only a near-hit and does not satisfy the balance law",
        abs(q_slack - 2.0 / 3.0) > 1.0e-5 and abs(koide_balance_single_sqrt(x_slack, t_slack, d_slack)) > 1.0e-5,
        detail=f"Q_slack={q_slack:.12f}",
    )

    x_slack_fix, t_slack_fix, d_slack_fix, sigma_slack_fix = transport_scalars(lambda_slack, h0_slack)
    q_slack_fix = koide_Q(np.abs(hermitian_eigs(sigma_slack_fix)))
    check(
        "A microscopic positive O_0 renormalization restores exact Koide at the visible chamber-link scalar",
        abs(q_slack_fix - 2.0 / 3.0) < 1.0e-12 and h0_slack > 0.0,
        detail=f"h0_small={h0_slack:.12e}",
    )
    check(
        "That corrected chamber-link point satisfies the same principal-block balance law",
        abs(koide_balance_single_sqrt(x_slack_fix, t_slack_fix, d_slack_fix)) < 1.0e-8,
        detail=f"balance={koide_balance_single_sqrt(x_slack_fix, t_slack_fix, d_slack_fix):+.3e}",
    )

    lambda_samples = [
        lambda_star - 8.0e-5,
        lambda_star - 4.0e-5,
        lambda_star,
        lambda_star + 4.0e-5,
        lambda_star + 8.0e-5,
    ]
    h0_branch = [small_h0_root(lam) for lam in lambda_samples]
    check(
        "Near the physical positive root there is a unique small local h_0 branch solving Koide",
        all(abs(h) < 1.0e-4 for h in h0_branch),
        detail=f"h0(lambda)={[round(h, 12) for h in h0_branch]}",
    )
    check(
        "The local chamber-link renormalization branch is monotone increasing in lambda",
        all(h0_branch[i] < h0_branch[i + 1] for i in range(len(h0_branch) - 1)),
    )

    eps = 1.0e-7
    fl = (q_residual(lambda_star + eps, 0.0) - q_residual(lambda_star - eps, 0.0)) / (2.0 * eps)
    fh = (q_residual(lambda_star, eps) - q_residual(lambda_star, -eps)) / (2.0 * eps)
    slope = -fl / fh
    check(
        "The physical root is nondegenerate in the O_0 direction, so the local Koide branch exists by implicit-function logic",
        abs(fh) > 1.0,
        detail=f"dF/dh0={fh:+.6f}",
    )
    check(
        "The local branch slope is close to one: h_0 acts as a renormalization of the visible chamber scalar",
        0.9 < slope < 1.05,
        detail=f"dh0/dlambda={slope:.12f}",
    )

    print()
    print("Interpretation:")
    print("  The missing-axis Higgs-dressed transport route is not hiding another")
    print("  free selector parameter. The visible chamber scalar is already present as")
    print("  Re(H_*[0,2]) = lambda_slack, and exact Koide lives on a local O_0")
    print("  renormalization branch of that chamber-link entry.")
    print("  So the remaining open microscopic object is sharper again:")
    print("      derive the O_0 renormalization law for the visible chamber link.")
    print()
    print(f"  lambda_star          = {lambda_star:.15f}")
    print(f"  lambda_slack         = {lambda_slack:.15f}")
    print(f"  h0_small(slack)      = {h0_slack:.12e}")
    print(f"  local branch slope   = {slope:.12f}")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    if FAIL:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
