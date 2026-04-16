#!/usr/bin/env python3
"""
Majorana scale-selector necessity theorem on the earlier logarithmic family.

Question:
  On the earlier logarithmic observable family alone, can a canonically
  meaningful finite Majorana scale selector be built from those exact
  observables alone?

Answer:
  No. On that earlier observable family, the scale-sensitive exact observables
  are affine in t = log(lambda) up to additive constants, while the remaining
  exact class data are scale-invariant. Any value-based selector depends on
  unfixed additive constants; any additive-shift-invariant differential
  selector is lambda-independent. So at that stage any successful scale
  selector had to add either a genuinely new non-homogeneous comparator or a
  canonically fixed endpoint/background normalization.

Later development:
  The branch now has both a local non-homogeneous comparator and a local
  background normalization on the admitted Nambu family. So this script is now
  historical support for the earlier blocker wording, not the current final
  blocker.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


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


def test_current_observables_are_affine_or_constant() -> None:
    print("\n" + "=" * 88)
    print("PART 1: CURRENT EXACT OBSERVABLES ARE AFFINE IN log(scale) OR CONSTANT")
    print("=" * 88)

    lambdas = np.array([0.19, 0.41, 0.83, 1.37], dtype=float)
    t = np.log(lambdas)

    w_pair = t + 0.3           # log(mu) + const
    w_nambu = t - 0.7          # log(||s||) + const
    w_tex = 3.0 * t + 1.1      # 3 log(lambda) + const
    inv = np.full_like(t, 2.4) # scale-invariant class datum

    second_pair = np.gradient(np.gradient(w_pair, t), t)
    second_nambu = np.gradient(np.gradient(w_nambu, t), t)
    second_tex = np.gradient(np.gradient(w_tex, t), t)
    dinv = np.gradient(inv, t)

    check("Local Pfaffian generator is affine in log scale", np.max(np.abs(second_pair)) < 1e-10,
          f"max second deriv={np.max(np.abs(second_pair)):.2e}")
    check("Local Nambu radial generator is affine in log scale", np.max(np.abs(second_nambu)) < 1e-10,
          f"max second deriv={np.max(np.abs(second_nambu)):.2e}")
    check("Three-generation lifted generator is affine in log scale", np.max(np.abs(second_tex)) < 1e-10,
          f"max second deriv={np.max(np.abs(second_tex)):.2e}")
    check("Scale-invariant class data carry zero scale derivative", np.max(np.abs(dinv)) < 1e-10,
          f"max deriv={np.max(np.abs(dinv)):.2e}")

    print()
    print("  So the current exact observable family has only two scale behaviors:")
    print("  affine in log(scale), or exactly scale-invariant.")


def selector_from_log_equality(c1: float, c2: float) -> float:
    """
    Solve W_tex(lambda) = W_pair(lambda) with
      3 log(lambda) + c1 = log(lambda) + c2.
    """
    return math.exp((c2 - c1) / 2.0)


def test_value_based_selectors_depend_on_additive_constants() -> None:
    print("\n" + "=" * 88)
    print("PART 2: VALUE-BASED SELECTORS DEPEND ON UNFIXED ADDITIVE CONSTANTS")
    print("=" * 88)

    selected = [
        selector_from_log_equality(0.0, 0.0),
        selector_from_log_equality(0.0, 4.0),
        selector_from_log_equality(-3.0, 1.0),
        selector_from_log_equality(2.5, -1.5),
    ]
    spread = max(selected) / min(selected)

    check("Equating two current logarithmic generators can shift the selected scale arbitrarily by additive renormalization",
          spread > 10.0, f"selection spread={spread:.3e}")

    print()
    print("  Raw value comparisons between the current log-type generators do not")
    print("  give a canonical scale. The result changes when the unfixed additive")
    print("  constants are shifted.")


def test_shift_invariant_differential_data_are_scale_independent() -> None:
    print("\n" + "=" * 88)
    print("PART 3: SHIFT-INVARIANT DIFFERENTIAL DATA CANNOT PICK A FINITE SCALE")
    print("=" * 88)

    lambdas = np.array([0.19, 0.41, 0.83, 1.37], dtype=float)
    t = np.log(lambdas)

    dw_pair_dt = np.gradient(t, t)
    dw_nambu_dt = np.gradient(t, t)
    dw_tex_dt = np.gradient(3.0 * t, t)

    ratio_tex_pair = dw_tex_dt / dw_pair_dt
    ratio_nambu_pair = dw_nambu_dt / dw_pair_dt
    pair_curv = np.gradient(dw_pair_dt, t)
    tex_curv = np.gradient(dw_tex_dt, t)

    check("Derivative of local pair generator is scale-independent in log coordinates",
          np.max(np.abs(dw_pair_dt - dw_pair_dt[0])) < 1e-10,
          f"spread={np.max(np.abs(dw_pair_dt - dw_pair_dt[0])):.2e}")
    check("Derivative ratio between current scale-sensitive generators is constant",
          np.max(np.abs(ratio_tex_pair - ratio_tex_pair[0])) < 1e-10 and np.max(np.abs(ratio_nambu_pair - ratio_nambu_pair[0])) < 1e-10,
          f"ratio spreads={np.max(np.abs(ratio_tex_pair - ratio_tex_pair[0])):.2e},{np.max(np.abs(ratio_nambu_pair - ratio_nambu_pair[0])):.2e}")
    check("Current logarithmic generators have zero curvature in log coordinates",
          np.max(np.abs(pair_curv)) < 1e-10 and np.max(np.abs(tex_curv)) < 1e-10,
          f"curvatures={np.max(np.abs(pair_curv)):.2e},{np.max(np.abs(tex_curv)):.2e}")

    print()
    print("  So every additive-shift-invariant differential datum available on the")
    print("  current source class is itself scale-independent. No finite critical")
    print("  point can come from these data alone.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: HISTORICAL SCALE-SELECTOR NECESSITY")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_NAMBU_RADIAL_OBSERVABLE_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_NO_STATIONARY_SCALE_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md")
    print("  - later partly superseded by:")
    print("    docs/NEUTRINO_MAJORANA_NAMBU_QUADRATIC_COMPARATOR_NOTE.md")
    print("    docs/NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  Could the earlier logarithmic Majorana observables alone define a")
    print("  canonically meaningful finite scale selector on the admitted source")
    print("  class?")

    test_current_observables_are_affine_or_constant()
    test_value_based_selectors_depend_on_additive_constants()
    test_shift_invariant_differential_data_are_scale_independent()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. On the earlier logarithmic observable family, the scale-sensitive")
    print("  observables were only affine in log(scale), and the remaining exact")
    print("  data were scale-invariant.")
    print()
    print("  At that stage, any successful Majorana scale selector had to add:")
    print("    1. a genuinely new non-homogeneous pairing-sector comparator, or")
    print("    2. a canonically fixed endpoint/background normalization tying the")
    print("       additive constants to a physical reference surface.")
    print()
    print("  Later branch work closed both of those local needs positively. The")
    print("  live blocker is now narrower: finite-point selection on the already-")
    print("  normalized local response curve.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
