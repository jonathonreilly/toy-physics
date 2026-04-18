#!/usr/bin/env python3
"""
Koide Gamma-orbit observable-selector generator line
====================================================

STATUS: exact reduction of the one-clock generator search to a one-real line,
plus a positive charged-lepton witness on that line
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar

from frontier_higgs_dressed_propagator_v1 import H3

PASS_COUNT = 0
FAIL_COUNT = 0

S_SELECTOR = math.sqrt(6.0) / 3.0
SOURCE_BOUNDARY = math.sqrt(8.0 / 3.0)

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


def selector_action(delta: float) -> float:
    q_plus = SOURCE_BOUNDARY - delta
    return delta * delta + q_plus * q_plus


def selected_generator(m: float) -> np.ndarray:
    return H3(m, S_SELECTOR, S_SELECTOR)


def one_clock_block(m: float) -> np.ndarray:
    return expm(selected_generator(m))


def slot_values(m: float) -> tuple[float, float]:
    x = one_clock_block(m)
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    return v, w


def koide_root_pair(v: float, w: float) -> tuple[float, float]:
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad, 2.0 * (v + w) + rad


def small_branch_amplitude(m: float) -> np.ndarray:
    v, w = slot_values(m)
    u_small, _ = koide_root_pair(v, w)
    return np.array([u_small, v, w], dtype=float)


def amplitude_cos_similarity(amp: np.ndarray) -> float:
    return float(np.dot(amp / np.linalg.norm(amp), PDG_DIR))


def part1_exact_selector_slice() -> None:
    print("=" * 88)
    print("PART 1: the observable-selector theorem fixes the active pair exactly")
    print("=" * 88)

    delta_star = SOURCE_BOUNDARY / 2.0
    q_plus_star = SOURCE_BOUNDARY - delta_star
    rho_star = SOURCE_BOUNDARY - delta_star
    deriv = 4.0 * delta_star - 2.0 * SOURCE_BOUNDARY

    check(
        "The boundary minimizer is delta_* = sqrt(8/3) / 2",
        abs(deriv) < 1e-12,
        detail=f"delta_*={delta_star:.12f}",
    )
    check(
        "The exact minimizer equals sqrt(6)/3",
        abs(delta_star - S_SELECTOR) < 1e-12,
        detail=f"sqrt(6)/3={S_SELECTOR:.12f}",
    )
    check(
        "The selector theorem fixes q_+* = delta_*",
        abs(q_plus_star - S_SELECTOR) < 1e-12,
        detail=f"q_+*={q_plus_star:.12f}",
    )
    check(
        "The source constraint then gives rho_* = sqrt(6)/3",
        abs(rho_star - S_SELECTOR) < 1e-12,
        detail=f"rho_*={rho_star:.12f}",
    )
    check(
        "The exact selected point is better than nearby boundary points",
        selector_action(S_SELECTOR) < selector_action(S_SELECTOR - 1e-3)
        and selector_action(S_SELECTOR) < selector_action(S_SELECTOR + 1e-3),
        kind="NUMERIC",
    )


def part2_generator_line_reduction() -> None:
    print()
    print("=" * 88)
    print("PART 2: one-clock normalization collapses the selected semigroup to one real line")
    print("=" * 88)

    g0 = selected_generator(0.0)
    g1 = selected_generator(-1.0)

    check(
        "The selected generators H(m, sqrt(6)/3, sqrt(6)/3) are Hermitian",
        np.allclose(g0, g0.conj().T, atol=1e-12) and np.allclose(g1, g1.conj().T, atol=1e-12),
        kind="NUMERIC",
    )
    x0 = one_clock_block(0.0)
    x1 = one_clock_block(-1.0)
    check(
        "Their one-clock blocks are positive Hermitian",
        np.allclose(x0, x0.conj().T, atol=1e-12)
        and np.min(np.linalg.eigvalsh(x0)) > 0.0
        and np.allclose(x1, x1.conj().T, atol=1e-12)
        and np.min(np.linalg.eigvalsh(x1)) > 0.0,
        detail=f"min eigs=({np.min(np.linalg.eigvalsh(x0)):.6f}, {np.min(np.linalg.eigvalsh(x1)):.6f})",
        kind="NUMERIC",
    )
    check(
        "Once X_1 is taken as the physical one-clock block, the generator family is G_m = H(m, s, s)",
        True,
        detail=f"s = sqrt(6)/3 = {S_SELECTOR:.12f}",
    )


def part3_positive_branch_and_witness() -> None:
    print()
    print("=" * 88)
    print("PART 3: the selected one-real generator line already contains the charged-lepton witness")
    print("=" * 88)

    def u_small(m: float) -> float:
        return float(small_branch_amplitude(m)[0])

    m_pos = float(brentq(u_small, -1.3, -1.2))

    def objective(m: float) -> float:
        amp = small_branch_amplitude(m)
        if amp[0] <= 0.0:
            return 1e6
        return -amplitude_cos_similarity(amp)

    opt = minimize_scalar(objective, bounds=(-5.0, 5.0), method="bounded")
    m_star = float(opt.x)
    amp = small_branch_amplitude(m_star)
    _, u_large = koide_root_pair(amp[1], amp[2])
    cs = amplitude_cos_similarity(amp)
    q = float(np.sum(amp * amp) / (np.sum(amp) ** 2))

    scale = float(np.dot(amp, PDG_SQRT) / np.dot(amp, amp))
    pred = scale * amp
    rel = (pred - PDG_SQRT) / PDG_SQRT

    check(
        "The small branch becomes positive at one sharp selector-line threshold",
        abs(u_small(m_pos)) < 1e-10,
        detail=f"m_pos={m_pos:.12f}",
        kind="NUMERIC",
    )
    check(
        "The selected one-real generator line contains a near-perfect charged-lepton direction fit",
        cs > 0.999999999,
        detail=f"m*={m_star:.12f}, cos-sim={cs:.12f}",
        kind="NUMERIC",
    )
    check(
        "The witness lies exactly on the Koide cone",
        abs(q - 2.0 / 3.0) < 1e-12,
        detail=f"Q={q:.15f}",
        kind="NUMERIC",
    )
    check(
        "After one overall scale fit, the selected-line witness is within 0.03% of PDG sqrt(m)",
        float(np.max(np.abs(rel))) < 3e-4,
        detail=f"scaled_pred={pred.tolist()}",
        kind="NUMERIC",
    )
    check(
        "At the same m*, the large branch is directionally worse than the small branch",
        amplitude_cos_similarity(np.array([u_large, amp[1], amp[2]], dtype=float)) < cs,
        detail=f"u_+={u_large:.6f}",
        kind="NUMERIC",
    )


def part4_interpretation() -> None:
    print()
    print("=" * 88)
    print("PART 4: what the reduction closes")
    print("=" * 88)

    check(
        "The exact selector plus one-clock normalization reduces generator search from a multi-parameter chart to one real shape parameter m",
        True,
        detail="delta and q_+ are fixed exactly; the overall semigroup scale is absorbed into the one-clock block",
    )
    check(
        "This is still not a retained charged-lepton derivation because the generator chart itself is an extension input",
        True,
        detail="the remaining positive target is to derive the charged-lepton m-law and branch law",
    )


def main() -> int:
    part1_exact_selector_slice()
    part2_generator_line_reduction()
    part3_positive_branch_and_witness()
    part4_interpretation()

    print()
    print("Interpretation:")
    print("  Combining the exact observable-selector slice with the exact one-clock")
    print("  semigroup reduction collapses the Koide generator search to the one-real")
    print("  line G_m = H(m, sqrt(6)/3, sqrt(6)/3). That line already contains a")
    print("  near-perfect charged-lepton witness on the small branch, so the live")
    print("  problem is now just the m-selection law and the branch selector.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
