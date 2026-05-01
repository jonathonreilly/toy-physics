#!/usr/bin/env python3
"""
Exact democratic Z_3 texture factor theorem for the reduced leptogenesis lane.

Question:
  Is the factor 1/3 used in the reduced Z_3 leptogenesis estimate merely a
  heuristic texture weight, or is it exact on the retained Z_3 basis bridge?

Answer:
  It is exact. The canonical Z_3 basis change is the 3x3 discrete Fourier
  transform U_Z3. Every entry has modulus 1/sqrt(3), so every overlap square
  between a Z_3 charge eigenstate and a flavor/site basis vector is exactly
  1/3.

Boundary:
  This closes the democratic texture factor in the reduced leptogenesis
  estimate. It does not yet derive the full CP-asymmetry tensor.
"""

from __future__ import annotations

import sys

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status} ({cls})] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def main() -> int:
    print("=" * 88)
    print("DM / NEUTRINO: EXACT Z3 TEXTURE-FACTOR THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/THREE_GENERATION_STRUCTURE_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  Is the 1/3 texture factor in the reduced leptogenesis estimate exact on")
    print("  the retained Z_3 basis bridge?")

    omega = np.exp(2j * np.pi / 3.0)
    uz3 = (1.0 / np.sqrt(3.0)) * np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, omega, omega * omega],
            [1.0, omega * omega, omega],
        ],
        dtype=complex,
    )

    abs_sq = np.abs(uz3) ** 2
    uniform = np.full((3, 3), 1.0 / 3.0)
    unitary_err = np.max(np.abs(uz3.conj().T @ uz3 - np.eye(3)))

    print()
    print("Canonical Z_3 basis bridge U_Z3:")
    print(uz3)
    print()
    print("Entrywise overlap squares |U_Z3|^2:")
    print(abs_sq)

    check("U_Z3 is exactly unitary", unitary_err < 1e-12, f"max err={unitary_err:.2e}")
    check(
        "Every overlap square on the Z_3 bridge is exactly 1/3",
        np.allclose(abs_sq, uniform, atol=1e-12),
        "all entries = 1/3",
    )
    check(
        "Every flavor/site basis vector sees the singlet and both doublet modes democratically",
        np.allclose(np.sum(abs_sq, axis=1), np.ones(3), atol=1e-12),
        "row sums = 1",
    )
    check(
        "Every Z_3 mode projects democratically onto the flavor/site basis",
        np.allclose(np.sum(abs_sq, axis=0), np.ones(3), atol=1e-12),
        "column sums = 1",
    )

    print()
    print("Result:")
    print("  The retained Z_3 basis bridge is exactly democratic. So the reduced")
    print("  leptogenesis texture factor is not heuristic on that bridge:")
    print()
    print("      texture factor = 1/3.")
    print()
    print("  What remains open is the full CP-asymmetry kernel, not this overlap.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
