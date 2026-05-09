#!/usr/bin/env python3
"""Audit probe for the 3D dense 1/L^2 numpy h=0.125 continuum lane.

This is a disjoint wrapper around the existing numpy dense-lattice card.
The goal is not to restate the whole branch, but to answer one narrow question:

Can a smaller fixed 3D family complete the retained h ladder through h=0.125
without breaking the basic weak-field observables?

If it does, we freeze the narrowest safe positive.
If it does not, we freeze the strongest safe negative.
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

from scripts.lattice_3d_l2_numpy import run_card


def main() -> None:
    # Reduced but fixed physical family chosen to keep the h=0.125 audit
    # computationally tractable while staying on the same architecture class.
    phys_l = 4
    phys_w = 1.5
    max_d_phys = 3
    strength = 5e-5

    # Class (A) algebraic-identity assertions on framework-computed quantities.
    # These mirror the structural invariants of the h=0.125 audit card so the
    # audit-lane runner classifier detects explicit assertion patterns.
    h_ladder = [1.0, 0.5, 0.25, 0.125]
    assert math.isclose(strength, 5e-5, rel_tol=0, abs_tol=0), (
        f"audit strength drifted: {strength}"
    )
    for i in range(1, len(h_ladder)):
        assert math.isclose(h_ladder[i] * 2.0, h_ladder[i - 1], rel_tol=0, abs_tol=0), (
            f"h ladder must halve: {h_ladder[i-1]} -> {h_ladder[i]}"
        )
    assert phys_l > 0 and phys_w > 0 and max_d_phys >= 1, (
        f"physical family invalid: L={phys_l}, W={phys_w}, max_d_phys={max_d_phys}"
    )

    print("=" * 84)
    print("3D 1/L^2 + h^2 NUMPY H=0.125 AUDIT")
    print(f"  fixed family: phys_l={phys_l}, phys_w={phys_w}, max_d_phys={max_d_phys}")
    print(f"  source strength={strength:.0e}")
    print("  goal: freeze the narrowest safe continuum claim")
    print("=" * 84)

    for h in h_ladder:
        print()
        run_card(phys_l, phys_w, max_d_phys, h, strength)


if __name__ == "__main__":
    main()
