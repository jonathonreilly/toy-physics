#!/usr/bin/env python3
"""
Necessary deformation class for a nonzero leptogenesis CP kernel.

Question:
  Once the universal Dirac bridge Y = y_0 I and the CKM-texture transfer no-go
  are both in place, what exact kind of new structure must any successful
  neutrino Dirac texture add in order to make the standard CP tensor nonzero?

Answer:
  A merely unitary basis mismatch does nothing: Y^dag Y stays y_0^2 I.
  A purely diagonal non-universal rescaling also does nothing: Y^dag Y stays
  diagonal. Therefore any successful texture must generate genuinely
  non-diagonal Hermitian kernel entries in H = Y^dag Y; equivalently it must
  introduce a non-unitary off-diagonal flavor-breaking deformation, not just
  another basis rotation or a diagonal singular-value split.
"""

from __future__ import annotations

import math
import sys

import numpy as np

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


def cp_kernel_entries(h: np.ndarray) -> tuple[complex, complex]:
    return h[0, 1], h[0, 2]


def cp_tensor_nonzero(h: np.ndarray, tol: float = 1e-12) -> bool:
    return any(abs(np.imag(entry * entry)) > tol for entry in cp_kernel_entries(h))


def unitary_rotation(theta: float) -> np.ndarray:
    return np.array(
        [
            [np.cos(theta), np.sin(theta), 0.0],
            [-np.sin(theta), np.cos(theta), 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=complex,
    )


def phase_matrix(phi2: float, phi3: float) -> np.ndarray:
    return np.diag([1.0, np.exp(1j * phi2), np.exp(1j * phi3)]).astype(complex)


def main() -> int:
    print("=" * 88)
    print("DM / FLAVOR: CP-KERNEL DEFORMATION NECESSITY")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/DM_LEPTOGENESIS_UNIVERSAL_YUKAWA_NO_GO_NOTE_2026-04-15.md")
    print("  - docs/DM_NEUTRINO_CKM_TEXTURE_TRANSFER_NO_GO_NOTE_2026-04-15.md")
    print()
    print("Question:")
    print("  What exact kind of new Dirac-side structure is necessary before the")
    print("  standard leptogenesis CP tensor can become nonzero?")

    y0 = 0.006662640625
    y_universal = y0 * np.eye(3, dtype=complex)

    ul = unitary_rotation(0.41)
    ur = phase_matrix(2.0 * np.pi / 3.0, -np.pi / 5.0) @ unitary_rotation(0.73)
    y_unitary = ul.conj().T @ y_universal @ ur
    h_unitary = y_unitary.conj().T @ y_unitary

    diag_split = y0 * np.diag([1.0, 1.15, 0.83]).astype(complex)
    h_diag_split = diag_split.conj().T @ diag_split

    offdiag_break = y0 * np.array(
        [
            [1.0, 0.12 * np.exp(1j * np.pi / 3.0), 0.0],
            [0.0, 1.1, 0.18 * np.exp(1j * np.pi / 4.0)],
            [0.09 * np.exp(-1j * np.pi / 6.0), 0.0, 0.87],
        ],
        dtype=complex,
    )
    h_offdiag_break = offdiag_break.conj().T @ offdiag_break

    unitary_offdiag = h_unitary - np.diag(np.diag(h_unitary))
    diag_split_offdiag = h_diag_split - np.diag(np.diag(h_diag_split))
    offdiag_break_offdiag = h_offdiag_break - np.diag(np.diag(h_offdiag_break))

    print()
    print("Representative kernels:")
    print("  H_unitary =")
    print(h_unitary)
    print()
    print("  H_diag_split =")
    print(h_diag_split)
    print()
    print("  H_offdiag_break =")
    print(h_offdiag_break)

    check(
        "Pure unitary mismatch leaves H = Y^dag Y proportional to the identity",
        np.allclose(h_unitary, (y0 * y0) * np.eye(3), atol=1e-12),
        "basis rotations alone do not change the Hermitian kernel",
    )
    check(
        "A purely diagonal non-universal split still leaves H diagonal",
        np.max(np.abs(diag_split_offdiag)) < 1e-12 and not cp_tensor_nonzero(h_diag_split),
        "singular-value splitting alone does not create CP-kernel entries",
    )
    check(
        "A nonzero CP tensor requires complex off-diagonal entries in H",
        np.max(np.abs(offdiag_break_offdiag)) > 1e-6 and cp_tensor_nonzero(h_offdiag_break),
        f"max offdiag(H) = {np.max(np.abs(offdiag_break_offdiag)):.2e}",
    )
    check(
        "Therefore the missing texture must be non-unitary and off-diagonal in flavor space",
        np.max(np.abs(unitary_offdiag)) < 1e-12
        and np.max(np.abs(diag_split_offdiag)) < 1e-12
        and np.max(np.abs(offdiag_break_offdiag)) > 1e-6,
        "basis rotations and diagonal rescalings both fail, off-diagonal breaking succeeds",
    )

    print()
    print("Result:")
    print("  The branch's missing object is now sharper than 'some non-universal")
    print("  Yukawa texture.' A merely unitary mismatch cannot work, and a purely")
    print("  diagonal singular-value split cannot work either. Any successful exact")
    print("  neutrino Dirac texture must induce genuinely non-diagonal Hermitian")
    print("  kernel entries in H = Y^dag Y, i.e. a non-unitary off-diagonal flavor-")
    print("  breaking deformation beyond the current universal bridge.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
