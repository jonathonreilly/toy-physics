#!/usr/bin/env python3
"""
Majorana source-response matching obstruction on the current exact stack.

Question:
  After the exact local self-dual point is fixed, could one match the exact
  local response values directly to current generation-side source-response
  observables and thereby derive the absolute Majorana staircase anchor?

Answer on the current exact stack:
  No. For the current generation pairing class, absolute source-response
  matches depend on the arbitrary normalization of the homogeneous generation
  representative, while normalized/relative response matches remove that
  normalization but also remove the absolute scale. So the present matching
  class does not fix the staircase anchor.

Boundary:
  This excludes the obvious current source-response matching class built from
  the exact local self-dual response and the current homogeneous generation
  pairing observables. It does NOT rule out a future genuinely new
  non-homogeneous bridge or absolute-scale datum.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
W_LOCAL = 0.5 * math.log(2.0)
Q_LOCAL = 1.0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def representative_texture() -> np.ndarray:
    return np.array(
        [[2.0, 0.0, 0.0], [0.0, 0.25, 1.0], [0.0, 1.0, 0.25]],
        dtype=float,
    )


def j2() -> np.ndarray:
    return np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=float)


def pairing_block(scale_lambda: float, rep_sigma: float) -> np.ndarray:
    m = scale_lambda * rep_sigma * representative_texture()
    return np.kron(m, j2())


def local_self_dual_values() -> tuple[float, float]:
    return W_LOCAL, Q_LOCAL


def generation_abs_logpf(scale_lambda: float, rep_sigma: float) -> float:
    m = scale_lambda * rep_sigma * representative_texture()
    return math.log(abs(np.linalg.det(m)))


def generation_abs_q2(scale_lambda: float, rep_sigma: float) -> float:
    delta = pairing_block(scale_lambda, rep_sigma)
    return float(np.linalg.norm(delta, ord="fro") ** 2)


def solve_abs_log_match(rep_sigma: float) -> float:
    det_hat = abs(np.linalg.det(representative_texture()))
    return math.exp((W_LOCAL - math.log(det_hat) - 3.0 * math.log(rep_sigma)) / 3.0)


def solve_abs_q2_match(rep_sigma: float) -> float:
    q0 = generation_abs_q2(1.0, 1.0)
    return math.sqrt(Q_LOCAL / (rep_sigma * rep_sigma * q0))


def generation_rel_logpf(scale_lambda: float, ref_lambda: float) -> float:
    return 3.0 * math.log(scale_lambda / ref_lambda)


def generation_rel_q2(scale_lambda: float, ref_lambda: float) -> float:
    return (scale_lambda / ref_lambda) ** 2


def solve_rel_log_match(ref_lambda: float) -> float:
    return ref_lambda * math.exp(W_LOCAL / 3.0)


def solve_rel_q2_match(ref_lambda: float) -> float:
    return ref_lambda * math.sqrt(Q_LOCAL)


def test_absolute_matches_depend_on_representative_normalization() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ABSOLUTE MATCHES DEPEND ON THE REPRESENTATIVE NORMALIZATION")
    print("=" * 88)

    sigmas = [0.5, 1.0, 2.0]
    lambdas_log = [solve_abs_log_match(sigma) for sigma in sigmas]
    lambdas_q = [solve_abs_q2_match(sigma) for sigma in sigmas]

    log_values = [generation_abs_logpf(lmbda, sigma) for lmbda, sigma in zip(lambdas_log, sigmas)]
    q_values = [generation_abs_q2(lmbda, sigma) for lmbda, sigma in zip(lambdas_q, sigmas)]

    lambda_log_spread = max(lambdas_log) - min(lambdas_log)
    lambda_q_spread = max(lambdas_q) - min(lambdas_q)
    log_match_error = max(abs(value - W_LOCAL) for value in log_values)
    q_match_error = max(abs(value - Q_LOCAL) for value in q_values)

    check("Absolute log-response matching selects different staircase scales for different representative normalizations",
          lambda_log_spread > 1e-3 and log_match_error < 1e-12,
          f"lambda spread={lambda_log_spread:.3e}, max error={log_match_error:.2e}")
    check("Absolute quadratic-response matching also selects different staircase scales for different representative normalizations",
          lambda_q_spread > 1e-3 and q_match_error < 1e-12,
          f"lambda spread={lambda_q_spread:.3e}, max error={q_match_error:.2e}")

    print()
    print("  So absolute matching to the exact local self-dual values can only fix")
    print("  the product of staircase scale and representative normalization, not")
    print("  the absolute staircase scale by itself.")


def test_relative_matches_remove_representative_normalization_but_not_anchor_scale() -> None:
    print("\n" + "=" * 88)
    print("PART 2: RELATIVE MATCHES REMOVE THE REPRESENTATIVE NORMALIZATION BUT ALSO")
    print("        REMOVE THE ABSOLUTE ANCHOR")
    print("=" * 88)

    ref_lambdas = [0.25, 1.0, 4.0]
    solved_log = [solve_rel_log_match(ref) for ref in ref_lambdas]
    solved_q = [solve_rel_q2_match(ref) for ref in ref_lambdas]

    log_errors = [abs(generation_rel_logpf(sol, ref) - W_LOCAL) for sol, ref in zip(solved_log, ref_lambdas)]
    q_errors = [abs(generation_rel_q2(sol, ref) - Q_LOCAL) for sol, ref in zip(solved_q, ref_lambdas)]
    log_ratio_spread = max(sol / ref for sol, ref in zip(solved_log, ref_lambdas)) - min(sol / ref for sol, ref in zip(solved_log, ref_lambdas))
    q_ratio_spread = max(sol / ref for sol, ref in zip(solved_q, ref_lambdas)) - min(sol / ref for sol, ref in zip(solved_q, ref_lambdas))
    lambda_log_spread = max(solved_log) - min(solved_log)
    lambda_q_spread = max(solved_q) - min(solved_q)

    check("Relative log-response matching fixes only the ratio to the chosen reference scale",
          max(log_errors) < 1e-12 and log_ratio_spread < 1e-12 and lambda_log_spread > 1e-3,
          f"max error={max(log_errors):.2e}, ratio spread={log_ratio_spread:.2e}, lambda spread={lambda_log_spread:.3e}")
    check("Relative quadratic-response matching also fixes only the ratio to the chosen reference scale",
          max(q_errors) < 1e-12 and q_ratio_spread < 1e-12 and lambda_q_spread > 1e-3,
          f"max error={max(q_errors):.2e}, ratio spread={q_ratio_spread:.2e}, lambda spread={lambda_q_spread:.3e}")

    print()
    print("  So normalized/relative response matching removes the arbitrary")
    print("  representative normalization, but it leaves the staircase anchor tied")
    print("  to an arbitrary reference scale instead of fixing it absolutely.")


def test_generation_pairing_observables_are_homogeneous() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT GENERATION PAIRING OBSERVABLES ARE HOMOGENEOUS")
    print("=" * 88)

    scales = [0.5, 1.0, 2.0]
    sigma = 1.0
    log_diffs = []
    q_ratios = []
    for scale in scales[1:]:
        log_diffs.append(generation_abs_logpf(scale, sigma) - generation_abs_logpf(1.0, sigma) - 3.0 * math.log(scale))
        q_ratios.append(generation_abs_q2(scale, sigma) / generation_abs_q2(1.0, sigma) - scale * scale)

    check("Absolute Pfaffian/logdet response is affine in log(scale)", max(abs(x) for x in log_diffs) < 1e-12,
          f"max residual={max(abs(x) for x in log_diffs):.2e}")
    check("Absolute quadratic comparator is degree-two in scale", max(abs(x) for x in q_ratios) < 1e-12,
          f"max residual={max(abs(x) for x in q_ratios):.2e}")

    print()
    print("  So the current generation-side source-response observables themselves")
    print("  already live on the same homogeneous scale family. Matching against")
    print("  the local self-dual constants cannot change that on the present stack.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: SOURCE-RESPONSE MATCHING OBSTRUCTION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_ALGEBRAIC_BRIDGE_OBSTRUCTION_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md")
    print()
    print("Question:")
    print("  Could one directly match the exact local self-dual Majorana response")
    print("  values to current generation-side source-response observables and")
    print("  thereby fix the absolute staircase anchor?")

    test_absolute_matches_depend_on_representative_normalization()
    test_relative_matches_remove_representative_normalization_but_not_anchor_scale()
    test_generation_pairing_observables_are_homogeneous()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. On the current exact stack, the obvious source-response matching")
    print("  class does not fix the absolute staircase anchor.")
    print()
    print("  Absolute matches depend on the arbitrary normalization of the")
    print("  homogeneous generation representative. Relative matches remove that")
    print("  arbitrariness but then fix only ratios to an arbitrary reference")
    print("  scale, not the absolute staircase anchor.")
    print()
    print("  So the missing object is sharper again: it must go beyond the current")
    print("  source-response matching class, or introduce a genuinely new")
    print("  non-homogeneous bridge or absolute-scale datum.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
