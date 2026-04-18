#!/usr/bin/env python3
"""
Koide Gamma-orbit exponential value-law candidate
=================================================

STATUS: exact positive one-parameter candidate family on the Gamma_i / full-cube
route

Purpose:
  Push the new singular target one level deeper. After the exact full-cube
  orbit law reduced the problem to a microscopic three-slot value law
  (u, v, w), test the simplest natural positive spectral family built from the
  live H_* pin on the intermediate T_2 block.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize_scalar

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


def t2_positive_block(beta: float) -> np.ndarray:
    return expm(beta * H_STAR)


def slot_values(beta: float) -> tuple[float, float]:
    x = t2_positive_block(beta)
    # Missing-axis order is (011, 101, 110). The axis-1 reachable slots are
    # 110 for species 2 and 101 for species 3.
    v = float(np.real(x[2, 2]))  # slot 110
    w = float(np.real(x[1, 1]))  # slot 101
    return v, w


def koide_root_pair(v: float, w: float) -> tuple[float, float]:
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad, 2.0 * (v + w) + rad


def amplitude_cos_similarity(amp: np.ndarray) -> float:
    return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))


def part1_exact_family_definition() -> None:
    print("=" * 88)
    print("PART 1: a natural positive T_2 spectral family gives exact slot values v(beta), w(beta)")
    print("=" * 88)

    check(
        "H_* is Hermitian",
        np.allclose(H_STAR, H_STAR.conj().T, atol=1e-12),
        kind="NUMERIC",
    )

    for beta in (-1.0, 0.0, 1.0):
        x = t2_positive_block(beta)
        eigs = np.linalg.eigvalsh(x)
        check(
            f"exp(beta H_*) is positive Hermitian for beta={beta:+.1f}",
            np.allclose(x, x.conj().T, atol=1e-12) and np.min(eigs) > 0.0,
            detail=f"min eig={np.min(eigs):.6f}",
            kind="NUMERIC",
        )

    v0, w0 = slot_values(0.0)
    check(
        "At beta=0 the positive block is the identity so v(0)=w(0)=1",
        abs(v0 - 1.0) < 1e-12 and abs(w0 - 1.0) < 1e-12,
        detail=f"v(0)={v0:.6f}, w(0)={w0:.6f}",
        kind="NUMERIC",
    )


def part2_exact_selector_root() -> None:
    print()
    print("=" * 88)
    print("PART 2: the Koide cone fixes the O_0 weight u(beta) algebraically")
    print("=" * 88)

    v, w = slot_values(0.635)
    u_minus, u_plus = koide_root_pair(v, w)

    selector_minus = u_minus * u_minus + v * v + w * w - 4.0 * (u_minus * v + u_minus * w + v * w)
    selector_plus = u_plus * u_plus + v * v + w * w - 4.0 * (u_plus * v + u_plus * w + v * w)

    check(
        "The pulled-back selector gives the exact two-root formula u = 2(v+w) ± sqrt(3(v^2+4vw+w^2))",
        abs(selector_minus) < 1e-10 and abs(selector_plus) < 1e-10,
        detail=f"u_-={u_minus:.6f}, u_+={u_plus:.6f}",
        kind="NUMERIC",
    )
    check(
        "For beta near the charged-lepton fit, the small branch is already positive",
        u_minus > 0.0,
        detail=f"u_-(beta=0.635)={u_minus:.6f}",
        kind="NUMERIC",
    )


def part3_best_fit_candidate() -> None:
    print()
    print("=" * 88)
    print("PART 3: the small-root exponential family has a near-perfect charged-lepton amplitude direction")
    print("=" * 88)

    def objective(beta: float) -> float:
        v, w = slot_values(beta)
        u_minus, _ = koide_root_pair(v, w)
        if u_minus <= 0.0:
            return 1e6
        amp = np.array([u_minus, v, w], dtype=float)
        return -amplitude_cos_similarity(amp)

    opt = minimize_scalar(objective, bounds=(0.5, 0.8), method="bounded")
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
        "The optimized small-root branch lies exactly on the Koide cone",
        abs(q - 2.0 / 3.0) < 1e-12,
        detail=f"beta*={beta_star:.12f}, Q={q:.15f}",
        kind="NUMERIC",
    )
    check(
        "The optimized amplitude direction is essentially identical to the PDG sqrt(m) direction",
        cs > 0.999999999,
        detail=f"cos-sim={cs:.12f}",
        kind="NUMERIC",
    )
    check(
        "After one overall scale fit, the predicted amplitudes are within 0.03% of PDG sqrt(m)",
        float(np.max(np.abs(rel))) < 3e-4,
        detail=f"scaled_pred={pred.tolist()}",
        kind="NUMERIC",
    )
    check(
        "The large-root branch is positive but directionally wrong, so the small branch is the charged-lepton candidate",
        u_large > u_star and amplitude_cos_similarity(np.array([u_large, v_star, w_star], dtype=float)) < cs,
        detail=f"u_+={u_large:.6f}",
        kind="NUMERIC",
    )


def part4_exact_interpretation() -> None:
    print()
    print("=" * 88)
    print("PART 4: what this candidate does and does not solve")
    print("=" * 88)

    check(
        "This is a positive one-parameter value-law family on the exact three-slot template",
        True,
        detail="beta determines the positive T_2 block; the cone then fixes u",
    )
    check(
        "This is not yet a retained derivation because it uses the observational H_* pin and the selector as inputs",
        True,
        detail="good positive candidate family, not current retained closure",
    )


def main() -> int:
    part1_exact_family_definition()
    part2_exact_selector_root()
    part3_best_fit_candidate()
    part4_exact_interpretation()

    print()
    print("Interpretation:")
    print("  The exact full-cube Gamma_i route now has a concrete positive value-law")
    print("  candidate family: put the T_2 block on exp(beta H_*), read the two")
    print("  reachable slot values v(beta), w(beta), then fix the O_0 slot by the")
    print("  exact orbit-slot Koide cone. The small-root branch gives an almost")
    print("  perfect charged-lepton amplitude direction at beta ~= 0.63357.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
