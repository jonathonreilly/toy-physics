#!/usr/bin/env python3
"""
Transfer-operator dominant-mode route for the active PMNS microscopic block.

Question:
  Can a genuinely dynamical native law on the hw=1 triplet recover any of the
  active microscopic PMNS data from corner-to-corner transport?

Answer:
  Yes. On the aligned hw=1 active patch, the native positive transfer kernel

      T_seed = xbar I + ybar (C + C^2)

  has one dominant symmetric mode and one doubly-degenerate orthogonal mode.
  Those two eigenvalues reconstruct the active seed pair exactly:

      lambda_+ = xbar + 2 ybar
      lambda_- = xbar - ybar

      xbar = (lambda_+ + 2 lambda_-)/3
      ybar = (lambda_+ - lambda_-)/3

  This is a genuine positive dynamical law for the active microscopic block on
  the hw=1 triplet. It fixes the aligned seed pair and therefore reproduces the
  weak-axis seed patch. It does not determine the 5-real off-seed breaking
  source.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=8, suppress=True, linewidth=120)

PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
CYCLE2 = CYCLE @ CYCLE
FOURIER = np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, np.exp(2j * np.pi / 3), np.exp(4j * np.pi / 3)],
        [1.0, np.exp(4j * np.pi / 3), np.exp(2j * np.pi / 3)],
    ],
    dtype=complex,
) / np.sqrt(3.0)


def check(name: str, condition: bool, detail: str = "", cls: str = "A") -> bool:
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


def active_seed_transfer_kernel(xbar: float, ybar: float) -> np.ndarray:
    """Positive aligned transfer kernel on the hw=1 triplet."""
    return xbar * I3 + ybar * (CYCLE + CYCLE2)


def eig_sorted(m: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    vals, vecs = np.linalg.eigh(m)
    idx = np.argsort(vals)[::-1]
    return vals[idx], vecs[:, idx]


def reconstruct_seed_pair_from_transfer_kernel(t: np.ndarray) -> tuple[float, float]:
    vals, _ = eig_sorted(t)
    lam_plus = float(vals[0])
    lam_minus = float(vals[1])
    xbar = (lam_plus + 2.0 * lam_minus) / 3.0
    ybar = (lam_plus - lam_minus) / 3.0
    return xbar, ybar


def orbit_average(m: np.ndarray) -> np.ndarray:
    return (m + CYCLE @ m @ CYCLE2 + CYCLE2 @ m @ CYCLE) / 3.0


def aligned_active_block(xbar: float, ybar: float) -> np.ndarray:
    return np.diag(np.array([xbar, xbar, xbar], dtype=complex)) + ybar * CYCLE


def transport_shadow_from_active_block(a: np.ndarray) -> np.ndarray:
    """Corner-transport shadow used by this route.

    The native dynamical quantity is the symmetrized, C3-averaged transfer
    kernel on the hw=1 triplet. On the aligned seed patch it reduces exactly
    to the positive circulant kernel above.
    """
    return orbit_average(a + a.conj().T)


def projected_transfer_kernel_from_active_block(a: np.ndarray) -> np.ndarray:
    """The dominant-mode transfer projection.

    This is the part of the transfer shadow that the dominant-mode route keeps:
    the C3-even diagonal stay weight and the C3-even hop weight. It is the
    exact seed-pair carrier.
    """
    xbar = float(np.real(np.trace(a)) / 3.0)
    ybar = float(np.real((a[0, 1] + a[1, 2] + a[2, 0])) / 3.0)
    return active_seed_transfer_kernel(2.0 * xbar, ybar)


def part1_the_aligned_hw1_transfer_kernel_has_exact_dominant_and_subdominant_modes() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ALIGNED HW=1 TRANSFER KERNEL HAS EXACT DOMINANT AND SUBDOMINANT MODES")
    print("=" * 88)

    xbar = 0.90
    ybar = 0.40
    t = active_seed_transfer_kernel(xbar, ybar)
    vals, vecs = eig_sorted(t)
    u0 = np.ones(3, dtype=complex) / np.sqrt(3.0)

    check("The transfer kernel is Hermitian", np.linalg.norm(t - t.conj().T) < 1e-12,
          f"Hermitian error={np.linalg.norm(t - t.conj().T):.2e}")
    check("The transfer kernel is positive on the chosen aligned patch", np.min(vals) > 0.0,
          f"eigenvalues={np.round(vals, 8).tolist()}")
    check("The dominant eigenvector is the symmetric hw=1 mode", np.abs(np.vdot(u0, vecs[:, 0])) > 1 - 1e-12,
          f"|<u0,v0>|={abs(np.vdot(u0, vecs[:,0])):.12f}")
    check("The two orthogonal modes are exactly degenerate", abs(vals[1] - vals[2]) < 1e-12,
          f"lambda_- split={abs(vals[1]-vals[2]):.2e}")
    check("The dominant and subdominant eigenvalues match the exact seed formulas",
          abs(vals[0] - (xbar + 2.0 * ybar)) < 1e-12 and abs(vals[1] - (xbar - ybar)) < 1e-12,
          f"vals={np.round(vals, 8).tolist()}")


def part2_the_seed_pair_is_reconstructed_exactly_from_the_transfer_modes() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE SEED PAIR IS RECONSTRUCTED EXACTLY FROM THE TRANSFER MODES")
    print("=" * 88)

    xbar = 0.90
    ybar = 0.40
    t = active_seed_transfer_kernel(xbar, ybar)
    rec_xbar, rec_ybar = reconstruct_seed_pair_from_transfer_kernel(t)

    check("The transfer kernel reconstructs xbar exactly", abs(rec_xbar - xbar) < 1e-12,
          f"reconstructed={rec_xbar:.12f}")
    check("The transfer kernel reconstructs ybar exactly", abs(rec_ybar - ybar) < 1e-12,
          f"reconstructed={rec_ybar:.12f}")
    print(f"  [INFO] The dominant-mode law fixes the aligned active seed pair  ((xbar,ybar)=({rec_xbar:.6f},{rec_ybar:.6f}))")


def part3_the_route_is_blind_to_the_5_real_corner_breaking_source() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THIS ROUTE IS BLIND TO THE ZERO-SUM CORNER-BREAKING CARRIER")
    print("=" * 88)

    # Two distinct off-seed microscopic samples with the same seed averages.
    xbar = 0.90
    ybar = 0.40

    x1 = np.array([1.15, 0.82, 0.73], dtype=float)
    y1 = np.array([0.50, 0.25, 0.45], dtype=float)
    x2 = np.array([1.05, 0.88, 0.77], dtype=float)
    y2 = np.array([0.39, 0.36, 0.45], dtype=float)

    # Force the same seed averages while retaining distinct breaking vectors.
    x1 += xbar - float(np.mean(x1))
    x2 += xbar - float(np.mean(x2))
    y1 += ybar - float(np.mean(y1))
    y2 += ybar - float(np.mean(y2))

    a1 = np.diag(x1) + np.diag(y1) @ CYCLE
    a2 = np.diag(x2) + np.diag(y2) @ CYCLE

    t1 = projected_transfer_kernel_from_active_block(a1)
    t2 = projected_transfer_kernel_from_active_block(a2)
    t_seed = active_seed_transfer_kernel(2.0 * xbar, ybar)

    check("The two off-seed microscopic samples are genuinely different", np.linalg.norm(a1 - a2) > 1e-6,
          f"operator distance={np.linalg.norm(a1 - a2):.6f}")
    check("Their dominant-mode transfer projections collapse to the same aligned seed kernel",
          np.linalg.norm(t1 - t_seed) < 1e-10 and np.linalg.norm(t2 - t_seed) < 1e-10,
          f"projection errors=({np.linalg.norm(t1 - t_seed):.2e}, {np.linalg.norm(t2 - t_seed):.2e})")
    print("  [INFO] The transfer-operator route fixes the aligned seed pair but not the breaking carrier  (zero-sum off-seed carrier is outside the transfer image)")


def part4_the_existing_weak_axis_seed_patch_is_recovered_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE WEAK-AXIS SEED PATCH IS RECOVERED EXACTLY")
    print("=" * 88)

    xbar = 0.90
    ybar = 0.40
    a_seed = aligned_active_block(xbar, ybar)
    t_seed = transport_shadow_from_active_block(a_seed)

    expected = active_seed_transfer_kernel(2.0 * xbar, ybar)  # A + A^dagger on aligned seed patch
    check("The aligned active block gives the exact transfer kernel on the seed patch",
          np.linalg.norm(t_seed - expected) < 1e-12,
          f"transfer error={np.linalg.norm(t_seed - expected):.2e}")
    print("  [INFO] The transfer kernel reproduces the existing weak-axis seed law structurally  (dominant and subdominant modes reconstruct the seed pair)")


def main() -> int:
    print("=" * 88)
    print("PMNS TRANSFER OPERATOR DOMINANT MODE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can a genuinely dynamical native law on the hw=1 triplet recover any")
    print("  of the active microscopic PMNS data from corner-to-corner transport?")

    part1_the_aligned_hw1_transfer_kernel_has_exact_dominant_and_subdominant_modes()
    part2_the_seed_pair_is_reconstructed_exactly_from_the_transfer_modes()
    part3_the_route_is_blind_to_the_5_real_corner_breaking_source()
    part4_the_existing_weak_axis_seed_patch_is_recovered_exactly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Positive native transfer-operator law:")
    print("    - on the aligned hw=1 active patch, the transfer kernel has an")
    print("      exact dominant symmetric mode and one degenerate orthogonal mode")
    print("    - those two modes reconstruct the active seed pair (xbar, ybar)")
    print("    - the aligned weak-axis seed patch is recovered exactly")
    print()
    print("  Boundary:")
    print("    - the route does not determine the 5-real off-seed corner-breaking")
    print("      source")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
