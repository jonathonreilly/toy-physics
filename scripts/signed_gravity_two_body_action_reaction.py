#!/usr/bin/env python3
"""Two-body action-reaction audit for signed gravitational response.

This is a focused front end for gravity_signed_sector_harness.py. It keeps
the inertial masses positive and compares source-only, response-only, and
source/response-locked signs across mixed chi_g pairs and mass ratios.
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.gravity_signed_sector_harness import MODES, PAIRS, _label_pair, _passfail, two_body_result


def main() -> None:
    mass_cases = ((1.0, 1.0), (1.0, 3.0), (3.0, 1.0), (2.0, 5.0))
    separations = (2.0, 3.0, 5.0)

    print("=" * 92)
    print("SIGNED GRAVITY TWO-BODY ACTION-REACTION AUDIT")
    print("  positive inertial mass throughout; signed branch affects source/response only")
    print("=" * 92)
    print()

    for mode in MODES:
        max_resid = 0.0
        mixed_resids = []
        print(f"MODE: {mode}")
        print(
            f"  {'pair':>4s} {'m_A':>5s} {'m_B':>5s} {'sep':>5s}  "
            f"{'F_A':>11s} {'F_B':>11s} {'resid':>9s}  read"
        )
        print("  " + "-" * 75)
        for chi_a, chi_b in PAIRS:
            for mass_a, mass_b in mass_cases:
                for sep in separations:
                    row = two_body_result(
                        mode,
                        chi_a,
                        chi_b,
                        inertial_mass_a=mass_a,
                        inertial_mass_b=mass_b,
                        z_a=-0.5 * sep,
                        z_b=+0.5 * sep,
                    )
                    max_resid = max(max_resid, row.balance_residual)
                    if chi_a != chi_b:
                        mixed_resids.append(row.balance_residual)
                    print(
                        f"  {_label_pair(chi_a, chi_b):>4s} {mass_a:5.1f} {mass_b:5.1f} {sep:5.1f}  "
                        f"{row.force_a:+11.4e} {row.force_b:+11.4e} "
                        f"{row.balance_residual:9.2e}  {row.readout}"
                    )
        if mode == "locked":
            ok = max_resid < 1e-12
            print(f"  summary: locked momentum balance {_passfail(ok)}  max_resid={max_resid:.3e}")
        else:
            control_ok = max(mixed_resids) > 1.0 if mixed_resids else False
            print(
                "  summary: control fails mixed-pair momentum balance "
                f"{_passfail(control_ok)}  max_resid={max_resid:.3e}"
            )
        print()

    print("SAFE READ")
    print("  The locked sign is the only one of these three algebraic options that")
    print("  passes action-reaction for all four chi_g pairs with positive inertial mass.")
    print("  Source-only and response-only signs remain useful no-go controls.")


if __name__ == "__main__":
    main()
