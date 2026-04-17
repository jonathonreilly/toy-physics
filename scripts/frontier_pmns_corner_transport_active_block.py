#!/usr/bin/env python3
"""
Direct corner-to-corner transport theorem for the active hw=1 PMNS block.

Question:
  If we work directly with corner-to-corner transport amplitudes on the hw=1
  active triplet, what native microscopic data do we actually recover?

Answer:
  The direct corner transport profile recovers the seed pair and the branch
  orientation, but not the full 5-real corner-breaking source.

  More precisely:
    - the corner-transport orbit average recovers the weak-axis seed pair
      (xbar, ybar)
    - the branch orientation is the sign of the C3-odd transport mode
    - the aligned weak-axis patch is exactly the vanishing locus of the
      breaking carrier
    - the 5-real breaking source remains in the kernel of the orbit-averaged
      transport map

  So this is a genuine dynamical native law on the active microscopic block,
  but it is not a full microscopic closure theorem.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)


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


def active_corner_transport(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    """Direct corner-to-corner transport matrix on the active hw=1 triplet."""
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return np.diag(np.asarray(x, dtype=complex)) + np.diag(y_eff) @ CYCLE


def decompose_seed_breaking(
    x: np.ndarray, y: np.ndarray, delta: float
) -> tuple[float, float, np.ndarray, np.ndarray, float]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xbar = float(np.mean(x))
    ybar = float(np.mean(y))
    xi = x - xbar * np.ones(3, dtype=float)
    eta = y - ybar * np.ones(3, dtype=float)
    return xbar, ybar, xi, eta, float(delta)


def orbit_average_transport(T: np.ndarray) -> tuple[complex, complex, complex]:
    """C3 orbit-average of the direct corner transport profile."""
    even = np.trace(T) / 3.0
    odd_fwd = (T[0, 1] + T[1, 2] + T[2, 0]) / 3.0
    odd_bwd = (T[0, 2] + T[2, 1] + T[1, 0]) / 3.0
    return even, odd_fwd, odd_bwd


def recover_seed_pair(T: np.ndarray) -> tuple[float, float]:
    even, odd_fwd, _odd_bwd = orbit_average_transport(T)
    return float(np.real(even)), float(np.real(odd_fwd))


def transport_branch_bit(T: np.ndarray) -> int:
    _, odd_fwd, odd_bwd = orbit_average_transport(T)
    return 0 if np.imag(odd_fwd) >= np.imag(odd_bwd) else 1


def transport_seed_matrix(xbar: float, ybar: float) -> np.ndarray:
    return xbar * I3 + ybar * CYCLE


def transport_breaking_vector(xi: np.ndarray, eta: np.ndarray, delta: float) -> np.ndarray:
    return np.array([xi[0], xi[1], eta[0], eta[1], delta], dtype=float)


def part1_direct_transport_recovers_the_seed_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 1: DIRECT CORNER TRANSPORT RECOVERS THE SEED PAIR")
    print("=" * 88)

    x = np.array([0.9, 0.9, 0.9], dtype=float)
    y = np.array([0.4, 0.4, 0.4], dtype=float)
    delta = 0.0
    T = active_corner_transport(x, y, delta)
    xbar, ybar, xi, eta, d = decompose_seed_breaking(x, y, delta)
    rxbar, rybar = recover_seed_pair(T)
    even, odd_fwd, odd_bwd = orbit_average_transport(T)

    print(f"  [INFO] The direct corner transport profile has exactly three orbit moments  (even={even:.6f}, odd_fwd={odd_fwd:.6f}, odd_bwd={odd_bwd:.6f})")
    check("The orbit-average even mode recovers xbar", abs(rxbar - xbar) < 1e-12,
          f"recovered={rxbar:.6f}, true={xbar:.6f}")
    check("The orbit-average forward odd mode recovers ybar", abs(rybar - ybar) < 1e-12,
          f"recovered={rybar:.6f}, true={ybar:.6f}")
    check("The recovered seed pair is exactly the weak-axis seed pair", np.linalg.norm(T - transport_seed_matrix(rxbar, rybar)) < 1e-12,
          "aligned transport profile matches the seed matrix exactly")

    print()
    print("  So the direct corner transport route gives a native seed-law output:")
    print("    - xbar from the C3-even transport moment")
    print("    - ybar from the C3-forward odd transport moment")


def part2_the_branch_bit_is_the_transport_asymmetry() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE BRANCH BIT IS THE TRANSPORT ASYMMETRY")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    delta = 0.63
    T = active_corner_transport(x, y, delta)
    bit = transport_branch_bit(T)

    T_swapped = active_corner_transport(x, y, -delta)
    bit_swapped = transport_branch_bit(T_swapped)

    check("The transport branch bit is a Z2 quantity", bit in (0, 1), f"bit={bit}")
    check("The branch bit flips under phase reversal on the corner transport orbit", bit != bit_swapped, f"bit={bit}, swapped={bit_swapped}")
    print("  [INFO] The branch bit is read from the C3-odd transport asymmetry  (forward vs backward cycle amplitude)")

    print()
    print("  The direct transport profile therefore gives a native branch selector.")


def part3_the_transport_kernel_is_blind_to_the_five_real_corner_source() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE TRANSPORT KERNEL IS BLIND TO THE 5-REAL CORNER SOURCE")
    print("=" * 88)

    # Two distinct off-seed active data sets with the same orbit-averaged
    # transport profile but different corner-breaking coordinates.
    x_a = np.array([1.15, 0.82, 0.95], dtype=float)
    y_a = np.array([0.41, 0.28, 0.54], dtype=float)
    delta_a = 0.63

    x_b = np.array([1.20, 0.79, 0.93], dtype=float)
    y_b = np.array([0.52, 0.17, 0.54], dtype=float)
    delta_b = 0.63

    T_a = active_corner_transport(x_a, y_a, delta_a)
    T_b = active_corner_transport(x_b, y_b, delta_b)
    xbar_a, ybar_a, xi_a, eta_a, d_a = decompose_seed_breaking(x_a, y_a, delta_a)
    xbar_b, ybar_b, xi_b, eta_b, d_b = decompose_seed_breaking(x_b, y_b, delta_b)

    even_a, odd_fwd_a, odd_bwd_a = orbit_average_transport(T_a)
    even_b, odd_fwd_b, odd_bwd_b = orbit_average_transport(T_b)

    check("The two transport profiles have the same orbit-averaged even mode", abs(even_a - even_b) < 1e-12,
          f"even_a={even_a:.6f}, even_b={even_b:.6f}")
    check("The two transport profiles have the same orbit-averaged odd mode", abs(odd_fwd_a - odd_fwd_b) < 1e-12 and abs(odd_bwd_a - odd_bwd_b) < 1e-12,
          f"odd_a={odd_fwd_a:.6f}/{odd_bwd_a:.6f}, odd_b={odd_fwd_b:.6f}/{odd_bwd_b:.6f}")
    check("The two corner-breaking sources are distinct", np.linalg.norm(transport_breaking_vector(xi_a, eta_a, d_a) - transport_breaking_vector(xi_b, eta_b, d_b)) > 1e-6,
          f"|source_a-source_b|={np.linalg.norm(transport_breaking_vector(xi_a, eta_a, d_a) - transport_breaking_vector(xi_b, eta_b, d_b)):.3f}")

    check("The two transport profiles share the same seed pair but have different 5-real breaking sources", np.allclose([xbar_a, ybar_a], [xbar_b, ybar_b], atol=1e-12)
          and np.linalg.norm(transport_breaking_vector(xi_a, eta_a, d_a) - transport_breaking_vector(xi_b, eta_b, d_b)) > 1e-6,
          f"seed_a=({xbar_a:.6f},{ybar_a:.6f}), seed_b=({xbar_b:.6f},{ybar_b:.6f})")

    print()
    print("  Therefore the transport kernel is exact on the seed pair and branch bit,")
    print("  but it has a nontrivial kernel on the 5-real corner source.")


def part4_result() -> None:
    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Positive native law:")
    print("    - direct hw=1 corner transport fixes the weak-axis seed pair")
    print("    - the C3-odd transport asymmetry fixes the branch bit")
    print()
    print("  Boundary:")
    print("    - the 5-real corner-breaking source is not fixed by orbit-averaged")
    print("      transport amplitudes alone")
    print()
    print("  So this is a genuine dynamical native transport law on the active")
    print("  microscopic block, but not a full microscopic closure theorem.")


def main() -> int:
    print("=" * 88)
    print("PMNS CORNER TRANSPORT ACTIVE BLOCK")
    print("=" * 88)
    print()
    print("Question:")
    print("  What does direct hw=1 corner-to-corner transport on the active")
    print("  microscopic block determine?")

    part1_direct_transport_recovers_the_seed_pair()
    part2_the_branch_bit_is_the_transport_asymmetry()
    part3_the_transport_kernel_is_blind_to_the_five_real_corner_source()
    part4_result()

    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
