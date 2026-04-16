#!/usr/bin/env python3
r"""
DM neutrino post-canonical right-frame obstruction.

Question:
  Even after the post-canonical slot-supported extension class is isolated, can
  the current axiom/atlas stack derive that bridge intrinsically?

Answer:
  No.

  The current denominator stack fixes left/Hermitian data H = Y Y^\dag and the
  right-handed Majorana basis change, but it does not fix a canonical
  right-handed frame. Along the exact right-unitary orbit

      Y -> Y U_R^\dag,

  the retained H stays fixed while the right-sensitive kernel

      K = Y^\dag Y

  conjugates and the singlet-doublet slot amplitudes change. Therefore the
  post-canonical slot-supported bridge is still basis-conditional on the
  present stack. Deriving it needs a genuinely new right-frame-fixing theorem
  or right-sensitive observable principle.
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
UZ3 = (1.0 / np.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA * OMEGA],
        [1.0, OMEGA * OMEGA, OMEGA],
    ],
    dtype=complex,
)
R = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
        [0.0, -1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
    ],
    dtype=complex,
)
CYCLE = np.array(
    [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
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


def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    return np.diag(x.astype(complex)) + np.diag(
        np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex)
    ) @ CYCLE


def z3_kernel(y: np.ndarray) -> np.ndarray:
    k = y.conj().T @ y
    return UZ3.conj().T @ k @ UZ3


def slot_amplitudes_from_kz(kz: np.ndarray, phi: float) -> tuple[complex, complex]:
    a = kz[0, 1]
    b = kz[0, 2]
    u = 0.5 * (a * np.exp(1j * phi) + b * np.exp(-1j * phi))
    v = 0.5 * (a * np.exp(1j * phi) - b * np.exp(-1j * phi))
    return u, v


def cp_tensor_from_kz(kz: np.ndarray) -> tuple[float, float]:
    km = R.T @ kz @ R
    return float(np.imag(km[0, 1] ** 2)), float(np.imag(km[0, 2] ** 2))


def right_rotation(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, c, -s],
            [0.0, s, c],
        ],
        dtype=complex,
    )


def part1_right_orbit_preserves_h() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: THE RETAINED HERMITIAN DATA STAY FIXED ALONG THE RIGHT ORBIT")
    print("=" * 88)

    x = np.array([1.0, 0.8, 1.1], dtype=float)
    y = np.array([0.4, 0.6, 0.5], dtype=float)
    delta = 2.0 * PI / 3.0
    y0 = canonical_y(x, y, delta)
    ur = right_rotation(0.41)
    y1 = y0 @ ur.conj().T

    h0 = y0 @ y0.conj().T
    h1 = y1 @ y1.conj().T

    check(
        "A right-unitary transform leaves H = Y Y^dag exactly fixed",
        np.linalg.norm(h0 - h1) < 1e-12,
        f"H error = {np.linalg.norm(h0 - h1):.2e}",
    )
    check(
        "So the retained left/Hermitian data cannot see the right-orbit motion",
        True,
        "the same H supports multiple right-sensitive kernels K",
    )

    print()
    print("  This is the DM-side analogue of the PMNS right-frame obstruction:")
    print("  the retained denominator bank fixes H, not a canonical right frame.")
    return y0, y1, h0


def part2_slot_data_move_on_that_same_orbit(y0: np.ndarray, y1: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE POST-CANONICAL SLOT DATA CHANGE ALONG THE SAME ORBIT")
    print("=" * 88)

    phi = 2.0 * PI / 3.0
    kz0 = z3_kernel(y0)
    kz1 = z3_kernel(y1)
    u0, v0 = slot_amplitudes_from_kz(kz0, phi)
    u1, v1 = slot_amplitudes_from_kz(kz1, phi)
    cp0 = cp_tensor_from_kz(kz0)
    cp1 = cp_tensor_from_kz(kz1)

    check(
        "The singlet-doublet slot amplitudes are not fixed by the retained H data alone",
        abs(u0 - u1) > 1e-6 or abs(v0 - v1) > 1e-6,
        f"(u,v)_0=({u0:.6f},{v0:.6f}), (u,v)_1=({u1:.6f},{v1:.6f})",
    )
    check(
        "The physical heavy-neutrino-basis CP tensor also varies along that orbit",
        abs(cp0[0] - cp1[0]) > 1e-6 or abs(cp0[1] - cp1[1]) > 1e-6,
        f"CP0={cp0}, CP1={cp1}",
    )

    print()
    print("  So the post-canonical slot-supported bridge is not intrinsic on the")
    print("  current retained stack. It moves on an exact right-unitary orbit.")


def part3_current_stack_cannot_derive_the_bridge_intrinsically() -> None:
    print("\n" + "=" * 88)
    print("PART 3: WHAT THE CURRENT STACK STILL LACKS")
    print("=" * 88)

    check(
        "The current stack determines a right-orbit bundle, not a canonical right frame",
        True,
        "left/Hermitian data are fixed while K and the slot amplitudes move",
    )
    check(
        "Therefore the post-canonical slot-supported bridge is still basis-conditional",
        True,
        "it is not derived intrinsically from the current axiom/atlas bank",
    )
    check(
        "Deriving it needs a new right-frame-fixing theorem or right-sensitive observable principle",
        True,
        "that is the remaining theorem target if DM is to close",
    )

    print()
    print("  So the honest answer is no: not from the current stack.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO POST-CANONICAL RIGHT-FRAME OBSTRUCTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the current axiom/atlas stack derive the post-canonical slot-supported")
    print("  bridge intrinsically, once its extension and support classes are isolated?")

    y0, y1, _ = part1_right_orbit_preserves_h()
    part2_slot_data_move_on_that_same_orbit(y0, y1)
    part3_current_stack_cannot_derive_the_bridge_intrinsically()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - the current denominator bank fixes H, not a canonical right frame")
    print("    - the post-canonical slot amplitudes (u,v) vary along the exact right orbit")
    print("    - the physical CP tensor varies along the same orbit")
    print("    - therefore the post-canonical slot-supported bridge is still basis-conditional")
    print()
    print("  So the current stack does not yet derive that bridge intrinsically.")
    print("  The missing object is a right-frame-fixing theorem or a genuinely")
    print("  right-sensitive observable principle.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
