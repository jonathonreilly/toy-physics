#!/usr/bin/env python3
"""Bridge probe for the 3D dense 1/L^2 numpy continuum lane at h=0.125.

This wrapper does not edit the existing continuum harness. It freezes one
disjoint replay that asks the only question that matters here:

Can the retained 3D 1/L^2 + h^2 measure lane still complete at h=0.125 on a
smaller but fixed physical family, and if so what is the narrowest safe
continuum claim?

The probe prints the completed h rows, Born if measured, the gravity sign, and
the F~M readout from the existing numpy card.
"""

from __future__ import annotations

# Heavy compute / 3D continuum bridge replay — exceeds the 120s default
# audit timeout. Measured wall-clock at 2026-05-10: ~501s on the canonical
# Python 3.12 machine (CPU was 72% — most time in numpy linear-algebra
# work); declaring 700s here gives ~40% margin while keeping the
# audit-cache budget bounded. Without this declaration the audit lane
# caches an empty stdout under `status: timeout`, blocking the audit
# verdict (the cited row was UNAUDITED on origin/main).
AUDIT_TIMEOUT_SEC = 700

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

from scripts.lattice_3d_l2_numpy import run_card


def main() -> None:
    # Fixed physical box used across all spacings. The h=0.125 row is the
    # decisive continuation test; the coarser rows are the same-family bridge.
    phys_l = 6
    phys_w = 3
    max_d_phys = 3
    strength = 5e-5

    print("=" * 84)
    print("3D 1/L^2 + h^2 NUMPY H=0.125 BRIDGE")
    print(f"  fixed family: phys_l={phys_l}, phys_w={phys_w}, max_d_phys={max_d_phys}")
    print(f"  source strength={strength:.0e}")
    print("  goal: retain the continuum bridge or freeze a bounded failure")
    print("=" * 84)

    for h in [1.0, 0.5, 0.25, 0.125]:
        print()
        run_card(phys_l, phys_w, max_d_phys, h, strength)


if __name__ == "__main__":
    main()
