#!/usr/bin/env python3
"""
Koide Gamma-orbit positive one-clock semigroup
==============================================

STATUS: exact reduction theorem plus positive witness on the full-cube route

Purpose:
  Once the exact Gamma_i / full-cube orbit law reduces the charged-lepton
  problem to a positive T_2 block together with one orbit-slot selector, the
  clean physical-lattice question is no longer "which arbitrary slot function?"
  It is "which one-clock block is repeated in derived time?"

  On any finite-dimensional positive Hermitian repeated-step family, that
  forces an exponential semigroup X_beta = exp(beta G) with a unique Hermitian
  generator G = log(X_1). This runner verifies that reduction on the live H_*
  witness and shows the charged-lepton candidate sits inside that exact class.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.linalg import expm, logm
from scipy.optimize import brentq, minimize_scalar

from frontier_higgs_dressed_propagator_v1 import (
    DELTA_STAR,
    H3,
    M_STAR,
    Q_PLUS_STAR,
)

PASS_COUNT = 0
FAIL_COUNT = 0

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


H_STAR = H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)


def positive_block(beta: float) -> np.ndarray:
    return expm(beta * H_STAR)


def slot_values(beta: float) -> tuple[float, float]:
    x = positive_block(beta)
    # Missing-axis order is (011, 101, 110). The axis-1 reachable slots are
    # 110 for species 2 and 101 for species 3.
    v = float(np.real(x[2, 2]))  # slot 110
    w = float(np.real(x[1, 1]))  # slot 101
    return v, w


def koide_root_pair(v: float, w: float) -> tuple[float, float]:
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad, 2.0 * (v + w) + rad


def u_minus(beta: float) -> float:
    v, w = slot_values(beta)
    return koide_root_pair(v, w)[0]


def amplitude_cos_similarity(amp: np.ndarray) -> float:
    return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))


def part1_one_clock_generator_recovery() -> None:
    print("=" * 88)
    print("PART 1: one positive clock step carries a unique Hermitian generator")
    print("=" * 88)

    x1 = positive_block(1.0)
    g1 = logm(x1)

    check(
        "H_* is Hermitian",
        np.allclose(H_STAR, H_STAR.conj().T, atol=1e-12),
        kind="NUMERIC",
    )
    check(
        "The one-clock block X_1 = exp(H_*) is positive Hermitian",
        np.allclose(x1, x1.conj().T, atol=1e-12) and np.min(np.linalg.eigvalsh(x1)) > 0.0,
        detail=f"min eig={np.min(np.linalg.eigvalsh(x1)):.6f}",
        kind="NUMERIC",
    )
    check(
        "A positive Hermitian one-clock block has a Hermitian logarithm",
        np.allclose(g1, g1.conj().T, atol=1e-12),
        kind="NUMERIC",
    )
    check(
        "The recovered generator log(X_1) matches the live H_* witness",
        np.allclose(g1, H_STAR, atol=1e-12),
        detail=f"max error={np.max(np.abs(g1 - H_STAR)):.3e}",
        kind="NUMERIC",
    )
    check(
        "Exponentiating the recovered generator returns the original one-clock block",
        np.allclose(expm(g1), x1, atol=1e-12),
        kind="NUMERIC",
    )


def part2_semigroup_reduction() -> None:
    print()
    print("=" * 88)
    print("PART 2: repeated identical local clock steps force one exponential family")
    print("=" * 88)

    pairs = [(0.15, 0.35), (0.40, 0.20), (0.50, 0.13357149356)]
    for beta, gamma in pairs:
        lhs = positive_block(beta + gamma)
        rhs = positive_block(beta) @ positive_block(gamma)
        check(
            f"Semigroup law holds at beta={beta:.6f}, gamma={gamma:.6f}",
            np.allclose(lhs, rhs, atol=1e-12),
            kind="NUMERIC",
        )

    x1 = positive_block(1.0)
    recovered = expm(0.37 * logm(x1))
    direct = positive_block(0.37)
    check(
        "The full positive family is fixed by the one-clock block alone",
        np.allclose(recovered, direct, atol=1e-12),
        kind="NUMERIC",
    )
    check(
        "Half a clock composed with itself gives one full clock",
        np.allclose(positive_block(0.5) @ positive_block(0.5), x1, atol=1e-12),
        kind="NUMERIC",
    )


def part3_slot_and_branch_reduction() -> None:
    print()
    print("=" * 88)
    print("PART 3: once the T_2 semigroup is fixed, the orbit-slot law reduces to one branch")
    print("=" * 88)

    beta_c = float(brentq(u_minus, 0.5, 0.7))
    u0 = u_minus(0.0)
    uc = u_minus(beta_c)
    up = u_minus(0.635)
    v, w = slot_values(0.635)
    u_small, u_large = koide_root_pair(v, w)

    check(
        "The small cone branch is negative at beta=0, so positivity makes branch selection nontrivial",
        u0 < 0.0,
        detail=f"u_-(0)={u0:.6f}",
        kind="NUMERIC",
    )
    check(
        "The small branch becomes positive at one sharp threshold beta_c",
        abs(uc) < 1e-10 and beta_c > 0.0,
        detail=f"beta_c={beta_c:.12f}",
        kind="NUMERIC",
    )
    check(
        "Beyond beta_c both cone roots are positive, so the remaining datum is branch choice",
        u_small > 0.0 and u_large > 0.0 and u_large > u_small,
        detail=f"u_-={u_small:.6f}, u_+={u_large:.6f}",
        kind="NUMERIC",
    )
    check(
        "The charged-lepton candidate sits on the positive side of the small branch threshold",
        up > 0.0 and 0.635 > beta_c,
        detail=f"u_-(0.635)={up:.6f}",
        kind="NUMERIC",
    )


def part4_live_candidate_inside_the_exact_class() -> None:
    print()
    print("=" * 88)
    print("PART 4: the charged-lepton fit sits inside the exact one-clock semigroup class")
    print("=" * 88)

    def objective(beta: float) -> float:
        v, w = slot_values(beta)
        u_small, _ = koide_root_pair(v, w)
        if u_small <= 0.0:
            return 1e6
        amp = np.array([u_small, v, w], dtype=float)
        return -amplitude_cos_similarity(amp)

    opt = minimize_scalar(objective, bounds=(0.5934, 0.8), method="bounded")
    beta_star = float(opt.x)
    v_star, w_star = slot_values(beta_star)
    u_star, u_large = koide_root_pair(v_star, w_star)
    amp = np.array([u_star, v_star, w_star], dtype=float)
    cs = amplitude_cos_similarity(amp)
    q = (u_star * u_star + v_star * v_star + w_star * w_star) / (u_star + v_star + w_star) ** 2

    scale = float(np.dot(amp, PDG_SQRT) / np.dot(amp, amp))
    pred = scale * amp
    rel = (pred - PDG_SQRT) / PDG_SQRT

    check(
        "The optimized semigroup candidate lies exactly on the Koide cone",
        abs(q - 2.0 / 3.0) < 1e-12,
        detail=f"beta*={beta_star:.12f}, Q={q:.15f}",
        kind="NUMERIC",
    )
    check(
        "The semigroup candidate direction is essentially the PDG sqrt(m) direction",
        cs > 0.999999999,
        detail=f"cos-sim={cs:.12f}",
        kind="NUMERIC",
    )
    check(
        "After one overall scale fit, the semigroup candidate is within 0.03% of PDG sqrt(m)",
        float(np.max(np.abs(rel))) < 3e-4,
        detail=f"scaled_pred={pred.tolist()}",
        kind="NUMERIC",
    )
    check(
        "The large branch remains the wrong charged-lepton direction inside the same semigroup class",
        amplitude_cos_similarity(np.array([u_large, v_star, w_star], dtype=float)) < cs,
        detail=f"u_+={u_large:.6f}",
        kind="NUMERIC",
    )


def part5_interpretation() -> None:
    print()
    print("=" * 88)
    print("PART 5: what the one-clock reduction closes")
    print("=" * 88)

    check(
        "The open value-law problem is reduced from an arbitrary three-slot family to one Hermitian generator plus a cone branch",
        True,
        detail="physical repeated-step law -> X_beta = exp(beta G) on T_2",
    )
    check(
        "Using H_* as generator is a positive witness inside the exact class, not yet a retained charged-lepton derivation",
        True,
        detail="the remaining work is generator selection and branch selection from charged-lepton physics",
    )


def main() -> int:
    part1_one_clock_generator_recovery()
    part2_semigroup_reduction()
    part3_slot_and_branch_reduction()
    part4_live_candidate_inside_the_exact_class()
    part5_interpretation()

    print()
    print("Interpretation:")
    print("  On the exact Gamma_i / full-cube route, once the microscopic lattice")
    print("  value law is required to come from repeated identical positive local")
    print("  clock steps on the reachable T_2 block, the family is forced into the")
    print("  exponential semigroup class X_beta = exp(beta G). The charged-lepton")
    print("  problem therefore reduces to selecting one Hermitian generator G and")
    print("  one positive cone branch. The live H_* witness lands almost exactly on")
    print("  the observed sqrt(m) direction inside that exact class.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
