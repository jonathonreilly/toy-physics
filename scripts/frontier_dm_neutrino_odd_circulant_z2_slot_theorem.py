#!/usr/bin/env python3
"""
DM odd-circulant residual-Z2 slot theorem.

Question:
  On the DM Hermitian circulant right-Gram family, what is the exact local slot
  that carries the CP-supporting deformation?

Answer:
  There is exactly one residual-Z2-odd slot.

  Writing the Hermitian circulant kernel as

      K = d I + c_even (S + S^2) + i c_odd (S - S^2),

  the exchange P23 swaps S <-> S^2, leaves I and S+S^2 invariant, and flips
  the sign of i(S-S^2). So c_odd is the unique local residual-Z2-odd slot.

  The leptogenesis CP kernel on this family is proportional to
      Im[(K_01)^2] = 2 c_even c_odd,
  so the odd slot is exactly the piece that must be activated away from zero.

Boundary:
  This identifies the exact missing local coefficient slot. It does not yet
  derive a nonzero activation law for it.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

S = np.array(
    [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
    ],
    dtype=complex,
)
S2 = S @ S
P23 = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
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


def z3_bridge() -> np.ndarray:
    omega = np.exp(2j * np.pi / 3.0)
    return (1.0 / np.sqrt(3.0)) * np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, omega, omega * omega],
            [1.0, omega * omega, omega],
        ],
        dtype=complex,
    )


def build_kernel(d: float, c_even: float, c_odd: float) -> np.ndarray:
    return d * np.eye(3, dtype=complex) + c_even * (S + S2) + 1j * c_odd * (S - S2)


def decompose_kernel(k: np.ndarray) -> tuple[float, float, float]:
    return float(np.real(k[0, 0])), float(np.real(k[0, 1])), float(np.imag(k[0, 1]))


def cp_tensor(k: np.ndarray) -> float:
    return float(np.imag(k[0, 1] ** 2))


def even_slice_from_split(a: complex, b: complex, uz3: np.ndarray) -> np.ndarray:
    d = np.diag([a, b, b]).astype(complex)
    return uz3.conj().T @ d @ uz3


def part1_residual_z2_even_odd_decomposition_is_exact() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE HERMITIAN CIRCULANT KERNEL HAS ONE UNIQUE RESIDUAL-Z2-ODD SLOT")
    print("=" * 88)

    k = build_kernel(1.2, 0.4, 0.3)
    d, c_even, c_odd = decompose_kernel(k)
    k_reflected = P23 @ k @ P23.conj().T

    check(
        "P23 exchanges the two cyclic generators",
        np.linalg.norm(P23 @ S @ P23.conj().T - S2) < 1e-12
        and np.linalg.norm(P23 @ S2 @ P23.conj().T - S) < 1e-12,
        "P23 S P23 = S^2 and P23 S^2 P23 = S",
    )
    check(
        "The even generator S+S^2 is residual-Z2 even while i(S-S^2) is odd",
        np.linalg.norm(P23 @ (S + S2) @ P23.conj().T - (S + S2)) < 1e-12
        and np.linalg.norm(P23 @ (1j * (S - S2)) @ P23.conj().T + 1j * (S - S2)) < 1e-12,
        "even part invariant, odd part flips sign",
    )
    check(
        "The kernel coefficients read off exactly as (d, c_even, c_odd)",
        abs(d - 1.2) < 1e-12 and abs(c_even - 0.4) < 1e-12 and abs(c_odd - 0.3) < 1e-12,
        f"(d,c_even,c_odd)=({d:.6f},{c_even:.6f},{c_odd:.6f})",
    )
    check(
        "Reflecting the kernel flips only the odd slot",
        np.linalg.norm(k_reflected - build_kernel(1.2, 0.4, -0.3)) < 1e-12,
        f"reflection error={np.linalg.norm(k_reflected - build_kernel(1.2, 0.4, -0.3)):.2e}",
    )

    print()
    print("  So the DM local coefficient problem has a unique residual-Z2-odd slot:")
    print("  the odd circulant coefficient c_odd.")


def part2_the_cp_kernel_is_exactly_driven_by_that_odd_slot() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE LEPTOGENESIS CP KERNEL IS EXACTLY DRIVEN BY THE ODD SLOT")
    print("=" * 88)

    k = build_kernel(1.1, 0.35, 0.22)
    _, c_even, c_odd = decompose_kernel(k)
    cp = cp_tensor(k)
    expected = 2.0 * c_even * c_odd

    k_even = build_kernel(1.1, 0.35, 0.0)
    k_odd_only = build_kernel(1.1, 0.0, 0.22)

    check(
        "On the Hermitian circulant family Im[(K01)^2] = 2 c_even c_odd",
        abs(cp - expected) < 1e-12,
        f"cp={cp:.6f}, expected={expected:.6f}",
    )
    check(
        "If the odd slot vanishes, the standard CP tensor vanishes",
        abs(cp_tensor(k_even)) < 1e-12,
        f"cp_even={cp_tensor(k_even):.2e}",
    )
    check(
        "The odd slot is necessary but needs even support to contribute",
        abs(cp_tensor(k_odd_only)) < 1e-12 and abs(cp) > 1e-6,
        f"cp_odd_only={cp_tensor(k_odd_only):.2e}, cp_full={cp:.6f}",
    )

    print()
    print("  So c_odd is not a cosmetic parameter.")
    print("  It is exactly the CP-supporting slot that must be activated away from zero.")


def part3_the_exact_weak_axis_bridge_fills_only_the_even_slot() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE EXACT WEAK-AXIS 1+2 SPLIT FILLS ONLY THE EVEN SLOT")
    print("=" * 88)

    uz3 = z3_bridge()
    a = 1.4 + 0.3j
    b = 0.8 - 0.2j
    y_even = even_slice_from_split(a, b, uz3)
    h_even = y_even.conj().T @ y_even
    d, c_even, c_odd = decompose_kernel(h_even)

    check(
        "The exact 1+2 split lifts through U_Z3 to the even circulant Dirac slice",
        np.max(np.abs(y_even - (np.eye(3, dtype=complex) * ((a + 2.0 * b) / 3.0) + (S + S2) * ((a - b) / 3.0)))) < 1e-12,
        f"lift error={np.max(np.abs(y_even - (np.eye(3, dtype=complex) * ((a + 2.0 * b) / 3.0) + (S + S2) * ((a - b) / 3.0)))):.2e}",
    )
    check(
        "Its Hermitian kernel has zero odd slot exactly",
        abs(c_odd) < 1e-12,
        f"(d,c_even,c_odd)=({d:.6f},{c_even:.6f},{c_odd:.2e})",
    )
    check(
        "Therefore the exact weak-axis bridge is CP-degenerate at the kernel level",
        abs(cp_tensor(h_even)) < 1e-12,
        f"cp_even={cp_tensor(h_even):.2e}",
    )

    print()
    print("  So the retained weak-axis 1+2 split already fixes the even slot,")
    print("  but it does not activate the odd one.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO ODD-CIRCULANT RESIDUAL-Z2 SLOT THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - DM minimal Z3 circulant CP tool")
    print("  - DM two-Higgs right-Gram bridge")
    print("  - exact weak-axis 1+2 split")
    print()
    print("Question:")
    print("  What exact local coefficient slot carries the CP-supporting deformation")
    print("  on the DM Hermitian circulant family?")

    part1_residual_z2_even_odd_decomposition_is_exact()
    part2_the_cp_kernel_is_exactly_driven_by_that_odd_slot()
    part3_the_exact_weak_axis_bridge_fills_only_the_even_slot()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact local answer:")
    print("    - the DM Hermitian circulant family has one unique residual-Z2-odd slot")
    print("    - that slot is the odd circulant coefficient c_odd")
    print("    - the exact weak-axis bridge fixes the even slot but leaves c_odd at zero")
    print()
    print("  So the last denominator coefficient problem is now even sharper:")
    print("  derive the activation law for that one odd slot.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())

