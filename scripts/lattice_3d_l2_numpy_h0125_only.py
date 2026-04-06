#!/usr/bin/env python3
"""Single-row replay for the decisive wide-family h=0.125 bridge test.

This is intentionally narrower than the full bridge wrapper. The wide-family
bridge has already replayed cleanly through the coarser rows; the only open
question is whether the decisive h=0.125 row itself can be completed cleanly
on the same retained family.

The script uses the shared numpy replay bootstrap so it lands on the same
interpreter convention as the retained bridge wrappers on this machine.
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

from scripts.lattice_3d_l2_numpy import run_card


def main() -> None:
    phys_l = 6
    phys_w = 3
    max_d_phys = 3
    strength = 5e-5
    h = 0.125

    print("=" * 84)
    print("3D 1/L^2 + h^2 NUMPY H=0.125 SINGLE-ROW DECISION TEST")
    print(f"  fixed family: phys_l={phys_l}, phys_w={phys_w}, max_d_phys={max_d_phys}")
    print(f"  source strength={strength:.0e}")
    print("  goal: decide whether the decisive h=0.125 row can be retained")
    print("=" * 84)
    print()
    run_card(phys_l, phys_w, max_d_phys, h, strength)


if __name__ == "__main__":
    main()
