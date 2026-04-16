#!/usr/bin/env python3
"""
DM neutrino no-go: exact Z3-covariant circulant bridges stay CP-empty in the
heavy-neutrino mass basis.

Question:
  Suppose the phase-lift family is promoted to exact source transfer, so the
  local bridge lands on the exact Z3-covariant circulant kernel

      K = d I + r (chi S + chi* S^2),

  with chi a true Z3 character. Does that already generate the physical
  leptogenesis tensor in the basis where M_R is diagonal?

Answer:
  No.

  Every such K is diagonalized by the Z3 Fourier matrix U_Z3 with a real
  diagonal spectrum. The current Majorana matrix

      M_R = [[A,0,0],[0,eps,B],[0,B,eps]]

  is block-diagonal in the same Z3 basis and is diagonalized inside its doublet
  block by a real orthogonal rotation. Therefore K in the heavy-neutrino mass
  basis is always real symmetric, so

      Im[(K_mass)_{1j}^2] = 0

  for all j. The entire exact Z3-covariant circulant bridge class is therefore
  still a no-go for physical leptogenesis CP on the current stack.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

PI = np.pi
OMEGA = np.exp(2j * PI / 3.0)

S = np.array(
    [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
    ],
    dtype=complex,
)
S2 = S @ S
UZ3 = (1.0 / np.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA * OMEGA],
        [1.0, OMEGA * OMEGA, OMEGA],
    ],
    dtype=complex,
)


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


def circulant_kernel(d: float, r: float, chi: complex) -> np.ndarray:
    return d * np.eye(3, dtype=complex) + r * (chi * S + np.conj(chi) * S2)


def z3_basis_kernel(k: np.ndarray) -> np.ndarray:
    return UZ3.conj().T @ k @ UZ3


def mass_basis_rotation() -> np.ndarray:
    # Current M_R doublet block [[eps,B],[B,eps]] diagonalizes by a real pi/4
    # rotation inside the doublet subspace.
    s = 1.0 / math.sqrt(2.0)
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, s, s],
            [0.0, -s, s],
        ],
        dtype=float,
    )


def cp_entries_in_mass_basis(k: np.ndarray) -> tuple[complex, complex]:
    k_z3 = z3_basis_kernel(k)
    rot = mass_basis_rotation()
    k_mass = rot.T @ k_z3 @ rot
    return k_mass[0, 1], k_mass[0, 2]


def part1_exact_circulant_family_is_real_diagonal_in_the_z3_basis() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT Z3-COVARIANT CIRCULANT FAMILY IS REAL-DIAGONAL IN U_Z3")
    print("=" * 88)

    d = 1.1366666666666667
    r = 0.45666666666666667
    ok_diag = True
    details = []
    for label, chi in [("1", 1.0 + 0.0j), ("omega", OMEGA), ("omega^2", np.conj(OMEGA))]:
        k = circulant_kernel(d, r, chi)
        kz3 = z3_basis_kernel(k)
        offdiag = np.linalg.norm(kz3 - np.diag(np.diag(kz3)))
        imag_diag = np.max(np.abs(np.imag(np.diag(kz3))))
        ok_diag &= offdiag < 1e-12 and imag_diag < 1e-12
        details.append(f"{label}: offdiag={offdiag:.2e}, imag_diag={imag_diag:.2e}")

    check(
        "Every exact Z3-covariant circulant bridge diagonalizes in the Z3 basis",
        ok_diag,
        "; ".join(details),
    )

    print()
    print("  So once the bridge is an exact Z3 character lift, its right-Gram kernel")
    print("  is not merely structured in the Z3 basis. It is real-diagonal there.")


def part2_the_majorana_doublet_diagonalization_is_real() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT MAJORANA DOUBLET DIAGONALIZATION IS REAL")
    print("=" * 88)

    eps = 0.2
    b = 1.3
    block = np.array([[eps, b], [b, eps]], dtype=float)
    rot = mass_basis_rotation()[1:, 1:]
    diag = rot.T @ block @ rot

    check(
        "The current Z3-basis doublet block diagonalizes by a real orthogonal rotation",
        np.linalg.norm(diag - np.diag(np.diag(diag))) < 1e-12,
        f"diag block = {np.round(diag, 6)}",
    )
    check(
        "That rotation carries no new complex CP phase",
        np.max(np.abs(np.imag(diag.astype(complex)))) < 1e-12,
        "purely real orthogonal pi/4 rotation on the doublet block",
    )

    print()
    print("  So the heavy-neutrino mass basis is obtained from the Z3 basis by a")
    print("  real change of basis inside the doublet sector.")


def part3_the_physical_cp_tensor_still_vanishes() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE STANDARD LEPTOGENESIS CP TENSOR STILL VANISHES")
    print("=" * 88)

    d = 1.1366666666666667
    r = 0.45666666666666667
    ok_zero = True
    details = []
    for label, chi in [("1", 1.0 + 0.0j), ("omega", OMEGA), ("omega^2", np.conj(OMEGA))]:
        k = circulant_kernel(d, r, chi)
        k_z3 = z3_basis_kernel(k)
        rot = mass_basis_rotation()
        k_mass = rot.T @ k_z3 @ rot
        imag_01 = float(np.imag(k_mass[0, 1] ** 2))
        imag_02 = float(np.imag(k_mass[0, 2] ** 2))
        is_real_symmetric = np.max(np.abs(np.imag(k_mass))) < 1e-12 and np.linalg.norm(k_mass - k_mass.T) < 1e-12
        ok_zero &= is_real_symmetric and abs(imag_01) < 1e-12 and abs(imag_02) < 1e-12
        details.append(
            f"{label}: Im(K01^2)={imag_01:.2e}, Im(K02^2)={imag_02:.2e}, real_sym={is_real_symmetric}"
        )

    check(
        "After moving to the heavy-neutrino mass basis, the circulant family stays real symmetric",
        ok_zero,
        "; ".join(details),
    )

    print()
    print("  Therefore exact Z3-covariant circulant bridges, including the full")
    print("  source-transfer branch chi=omega, do not generate the physical")
    print("  leptogenesis tensor on the current Majorana stack.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO Z3-CIRCULANT MASS-BASIS NO-GO")
    print("=" * 88)
    print()
    print("Question:")
    print("  If the mixed bridge is promoted to exact Z3 source transfer, is the")
    print("  resulting exact circulant family already enough for physical leptogenesis?")

    part1_exact_circulant_family_is_real_diagonal_in_the_z3_basis()
    part2_the_majorana_doublet_diagonalization_is_real()
    part3_the_physical_cp_tensor_still_vanishes()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - the exact Z3-covariant circulant bridge family is real-diagonal in U_Z3")
    print("    - the current Majorana doublet basis change is real")
    print("    - so the heavy-neutrino-basis kernel stays real symmetric")
    print("    - therefore Im[(K_mass)_{1j}^2] = 0 for all j")
    print()
    print("  The full-source circulant bridge is therefore not the last mile.")
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
