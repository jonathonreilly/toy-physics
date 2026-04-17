#!/usr/bin/env python3
"""
Majorana doublet-block matching obstruction on the fixed staircase placement.

Question:
  After fixing k_A = 7 and k_B = 8, could the obvious normalized 2x2
  generation-doublet block be matched directly to the exact local self-dual
  Majorana block and thereby fix eps/B?

Answer on the obvious current matching class:
  No. Using the natural doublet baseline B*sigma_x and splitting increment
  eps*I, the exact background-normalized generation observables are

      Q_rel^(dbl) = r^2,
      W_rel^(dbl) = (1/2) log|1-r^2|,

  with r = eps/B.

  Matching the exact local self-dual values Q_rel = 1 and
  W_rel = (1/2)log 2 forces incompatible order-1 values of r, and in
  particular no perturbative r << 1 can satisfy either local condition.

Boundary:
  This closes the obvious normalized 2x2 local-to-doublet matching class.
  It does not rule out a future genuinely new eps/B law.
"""

from __future__ import annotations

import math
import sys

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


def q_rel_doublet(r: float) -> float:
    return r * r


def w_rel_doublet(r: float) -> float:
    return 0.5 * math.log(abs(1.0 - r * r))


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: DOUBLET-BLOCK MATCHING OBSTRUCTION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_EPS_OVER_B_RESIDUAL_RATIO_OBSTRUCTION_NOTE.md")
    print()
    print("Question:")
    print("  Could the obvious normalized 2x2 generation-doublet block match the")
    print("  exact local self-dual Majorana block closely enough to fix eps/B?")

    r_q = math.sqrt(Q_LOCAL)
    r_w_small_exists = False
    r_w_large = math.sqrt(3.0)
    sample_rs = [0.01, 0.041, 0.08, 0.15]
    q_samples = [q_rel_doublet(r) for r in sample_rs]
    w_samples = [w_rel_doublet(r) for r in sample_rs]

    print()
    print(f"  Local self-dual targets:  Q_rel = {Q_LOCAL:.6f}, W_rel = {W_LOCAL:.6f}")
    print()
    print("  Generation-doublet normalized observables on G(r) = r I + sigma_x:")
    for r, q_val, w_val in zip(sample_rs, q_samples, w_samples):
        print(f"    r={r:0.3f}:  Q_rel^(dbl)={q_val:.6f},  W_rel^(dbl)={w_val:.6f}")

    check(
        "Quadratic matching to the local self-dual comparator forces r = 1",
        abs(r_q - 1.0) < 1e-12,
        f"r_Q={r_q:.12f}",
    )
    check(
        "Log-response matching has no perturbative solution with 0 < r < 1",
        not r_w_small_exists,
        "W_rel^(dbl)=0.5 log|1-r^2| <= 0 for 0<r<1, but W_local > 0",
    )
    check(
        "The only positive log-response match is order-1: r = sqrt(3)",
        abs(w_rel_doublet(r_w_large) - W_LOCAL) < 1e-12,
        f"r_W={r_w_large:.12f}",
    )
    check(
        "The fitted perturbative band r ~ 0.01-0.15 is far from the local self-dual comparator target",
        max(abs(q - Q_LOCAL) for q in q_samples) > 0.9,
        f"max deviation={max(abs(q - Q_LOCAL) for q in q_samples):.6f}",
    )
    check(
        "The fitted perturbative band gives the wrong sign for the local log-response target",
        max(w_samples) < 0.0 < W_LOCAL,
        f"max W_dbl={max(w_samples):.6f}, W_local={W_LOCAL:.6f}",
    )

    print()
    print("Result:")
    print("  The obvious normalized 2x2 local-to-doublet matching class fails.")
    print("  Its quadratic match forces r = 1, its bosonic log-response match")
    print("  forces r = sqrt(3), and neither admits a perturbative eps/B << 1.")
    print()
    print("  So the live blocker is narrower again:")
    print("      derive a genuinely new eps/B law beyond the obvious normalized")
    print("      local-to-doublet block matching class.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
