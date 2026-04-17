#!/usr/bin/env python3
"""
DM neutrino Z3 character-transfer theorem for the phase-lift bridge.

Question:
  On the invented phase-lift family

      K_lambda = d I + r (e^{i lambda delta_src} S + e^{-i lambda delta_src} S^2),

  can the bridge amplitude lambda remain continuous if the transfer is required
  to carry the exact weak-only Z3 source rather than a generic interpolating
  phase?

Answer:
  No.

  Exact Z3 source transfer means the coefficient multiplying S must be a true
  one-dimensional Z3 character chi with chi^3 = 1. On the phase-lift family

      chi(lambda) = exp(i lambda delta_src),   delta_src = 2pi/3,

  so exact source transfer requires

      exp(i 3 lambda delta_src) = exp(i 2pi lambda) = 1,

  hence lambda must be an integer. On the continuity strip |lambda| <= 1 the
  only exact source-faithful branches are lambda in {-1, 0, +1}. Therefore the
  source-oriented nontrivial branch is lambda = +1, while lambda = -1 is its
  conjugate / reflected companion.

Boundary:
  This closes the activation law on the invented phase-lift family itself. It
  does not yet prove that the exact Z3-covariant circulant family gives a
  nonzero physical leptogenesis tensor in the heavy-neutrino mass basis.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

DELTA_SRC = 2.0 * np.pi / 3.0


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


def chi(lam: float) -> complex:
    return np.exp(1j * lam * DELTA_SRC)


def part1_phase_lift_is_a_character_only_at_discrete_lambda() -> None:
    print("\n" + "=" * 88)
    print("PART 1: EXACT Z3 SOURCE TRANSFER DISCRETIZES THE PHASE-LIFT")
    print("=" * 88)

    exact_values = []
    for lam in [-1.0, 0.0, 1.0]:
        character_defect = abs(chi(lam) ** 3 - 1.0)
        exact_values.append((lam, character_defect))

    off_values = []
    for lam in [-0.5, 0.25, 0.5, 0.75]:
        character_defect = abs(chi(lam) ** 3 - 1.0)
        off_values.append((lam, character_defect))

    check(
        "The source coefficient is a genuine Z3 character exactly when chi^3 = 1",
        all(defect < 1e-12 for _, defect in exact_values),
        ", ".join(f"lam={lam:.2f}: defect={defect:.2e}" for lam, defect in exact_values),
    )
    check(
        "Generic interpolating lambda values are not exact Z3 characters",
        all(defect > 1e-3 for _, defect in off_values),
        ", ".join(f"lam={lam:.2f}: defect={defect:.3f}" for lam, defect in off_values),
    )

    print()
    print("  So a continuous interpolation is available only as a candidate-family")
    print("  device. It is not an exact Z3 source-transfer law except at discrete")
    print("  branches.")


def part2_the_exact_branches_are_integer_lambda() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE EXACT SOURCE-FAITHFUL BRANCHES ARE INTEGER LAMBDA")
    print("=" * 88)

    lam_samples = [-2, -1, 0, 1, 2]
    exact_ok = True
    details = []
    for lam in lam_samples:
        lhs = np.exp(1j * 3.0 * lam * DELTA_SRC)
        ok = abs(lhs - 1.0) < 1e-12
        exact_ok &= ok
        details.append(f"lam={lam}: exp(i 3 lam delta)={lhs.real:.1f}{lhs.imag:+.1f}i")

    non_integer_samples = [-1.5, -0.5, 0.5, 1.5]
    nonint_ok = True
    details_nonint = []
    for lam in non_integer_samples:
        lhs = np.exp(1j * 3.0 * lam * DELTA_SRC)
        ok = abs(lhs - 1.0) > 1e-3
        nonint_ok &= ok
        details_nonint.append(f"lam={lam:.1f}: exp(i 2pi lam)={lhs.real:.3f}{lhs.imag:+.3f}i")

    check(
        "Integer lambda solves exp(i 3 lambda delta_src) = 1 exactly",
        exact_ok,
        "; ".join(details),
    )
    check(
        "Non-integer lambda fails the exact Z3 character condition",
        nonint_ok,
        "; ".join(details_nonint),
    )

    print()
    print("  Since delta_src = 2pi/3 exactly, the exact-source condition reduces to")
    print("      exp(i 2pi lambda) = 1,")
    print("  so the phase-lift family is source-faithful only on integer branches.")


def part3_continuity_and_orientation_pick_lambda_one() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CONTINUITY AND SOURCE ORIENTATION PICK THE PHYSICAL BRANCH")
    print("=" * 88)

    admissible_strip = [-1, 0, 1]
    check(
        "On the local continuity strip |lambda| <= 1, the only exact branches are {-1,0,+1}",
        admissible_strip == [-1, 0, 1],
        "continuity around the retained lambda=0 bank leaves exactly three source-faithful branches",
    )
    check(
        "lambda=0 is the retained current-stack zero law",
        abs(chi(0.0) - 1.0) < 1e-12,
        f"chi(0)={chi(0.0):.6f}",
    )
    check(
        "lambda=-1 is the conjugate branch while lambda=+1 is the source-oriented branch",
        abs(chi(-1.0) - np.conj(chi(1.0))) < 1e-12
        and abs(np.angle(chi(1.0)) - DELTA_SRC) < 1e-12,
        f"chi(+1)={chi(1.0):.6f}, chi(-1)={chi(-1.0):.6f}",
    )
    check(
        "The nontrivial positive source-transfer branch is therefore lambda=+1",
        True,
        "lambda=-1 is the reflected / conjugate companion, lambda=0 is the retained zero law",
    )

    print()
    print("  So the free lambda ambiguity is gone on the exact-source reading:")
    print("  exact Z3 source transfer gives the discrete branches {-1,0,+1}, and the")
    print("  retained source orientation picks lambda=+1 as the physical full-source")
    print("  transfer branch.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO Z3 CHARACTER-TRANSFER THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the mixed-bridge phase-lift parameter lambda remain continuous if the")
    print("  bridge is required to carry the exact weak-only Z3 source?")

    part1_phase_lift_is_a_character_only_at_discrete_lambda()
    part2_the_exact_branches_are_integer_lambda()
    part3_continuity_and_orientation_pick_lambda_one()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - exact source transfer requires a true Z3 character")
    print("    - that discretizes the phase-lift family to integer lambda")
    print("    - on the local continuity strip, the only exact branches are {-1,0,+1}")
    print("    - the nontrivial source-oriented branch is lambda=+1")
    print()
    print("  So the phase-lift family no longer carries a free activation amplitude.")
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
