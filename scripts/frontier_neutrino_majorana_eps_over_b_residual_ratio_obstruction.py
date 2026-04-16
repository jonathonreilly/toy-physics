#!/usr/bin/env python3
"""
Majorana eps/B residual-ratio obstruction on the fixed staircase placement.

Question:
  Once the branch fixes the staircase placement k_A = 7, k_B = 8, does the
  current exact stack also fix the remaining doublet splitting ratio eps/B?

Answer on the current exact stack:
  No. After the placement is fixed, r = eps/B remains a dimensionless
  deformation parameter inside the same exact Z3 texture class. The symmetry,
  charge sector, and singlet/doublet decomposition remain intact for every
  admissible r, while the normalized doublet spectrum varies continuously.

Boundary:
  This sharpens the live blocker to the residual texture-amplitude law. It
  does not rule out a future theorem that fixes eps/B.
"""

from __future__ import annotations

import sys

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0

ALPHA_LM = 0.09067
A_OVER_B = 1.0 / ALPHA_LM  # k_A = 7, k_B = 8 fixed
J2 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)


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


def z3_texture(a: complex, b: complex, eps: complex) -> np.ndarray:
    return np.array(
        [[a, 0.0, 0.0], [0.0, eps, b], [0.0, b, eps]],
        dtype=complex,
    )


def normalized_doublet_spectrum(r: complex) -> np.ndarray:
    vals = np.array([1.0 + r, 1.0 - r], dtype=complex)
    return np.sort(np.abs(vals) / np.linalg.norm(np.abs(vals)))


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: EPS/B RESIDUAL-RATIO OBSTRUCTION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_ENDPOINT_EXCHANGE_MIDPOINT_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  After fixing k_A = 7 and k_B = 8, does the current exact stack also")
    print("  fix the residual doublet-splitting ratio eps/B?")

    r_values = [0.01, 0.041, 0.08, 0.15]
    charge_errors = []
    symmetry_errors = []
    eig_errors = []
    ab_ratios = []
    spectra = []

    for r in r_values:
        a = A_OVER_B
        b = 1.0
        eps = r * b
        m = z3_texture(a, b, eps)
        delta = np.kron(m, J2)
        symmetry_errors.append(np.linalg.norm(m - m.T))
        charge_errors.append(np.linalg.norm(delta + delta.T))
        eigs = np.sort_complex(np.linalg.eigvals(m))
        target = np.sort_complex(np.array([a, eps + b, eps - b], dtype=complex))
        eig_errors.append(np.linalg.norm(eigs - target))
        ab_ratios.append(abs(a / b))
        spectra.append(normalized_doublet_spectrum(r))

        print()
        print(f"  r = eps/B = {r:.3f}")
        print(f"    eigenvalues = {target}")
        print(f"    normalized doublet spectrum = {spectra[-1]}")

    max_symmetry = max(symmetry_errors)
    max_charge = max(charge_errors)
    max_eig_err = max(eig_errors)
    ab_spread = max(ab_ratios) - min(ab_ratios)
    spec_spread = max(np.linalg.norm(spec - spectra[0]) for spec in spectra[1:])

    check(
        "The fixed-placement Z3 matrix stays symmetric for every tested eps/B",
        max_symmetry < 1e-12,
        f"max symmetry error={max_symmetry:.2e}",
    )
    check(
        "The lifted pairing block stays antisymmetric for every tested eps/B",
        max_charge < 1e-12,
        f"max pairing antisymmetry error={max_charge:.2e}",
    )
    check(
        "The texture always organizes one singlet and one doublet pair of eigenvalues",
        max_eig_err < 1e-12,
        f"max eigenvalue error={max_eig_err:.2e}",
    )
    check(
        "The staircase placement ratio A/B is fixed independently of eps/B",
        ab_spread < 1e-12,
        f"spread in A/B={ab_spread:.2e}",
    )
    check(
        "The normalized doublet spectrum varies across admissible eps/B choices",
        spec_spread > 1e-3,
        f"spectrum spread={spec_spread:.3e}",
    )

    print()
    print("Result:")
    print("  Once k_A = 7 and k_B = 8 are fixed, eps/B remains a residual")
    print("  dimensionless deformation of the same exact Z3 texture class.")
    print("  The current exact stack fixes the placement, not the splitting.")
    print()
    print("  So the live denominator blocker is now exact and narrow:")
    print("      derive eps/B (or prove a no-go), then close the remaining")
    print("      texture amplitudes downstream.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
