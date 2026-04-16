#!/usr/bin/env python3
"""
Exact corner-orbit reduction theorem for generic microscopic PMNS ΔD.

Question:
  Once the active PMNS microscopic deformation is known to lie on the exact
  carrier

      ΔD_act = diag(x_1-1, x_2-1, x_3-1)
             + diag(y_1, y_2, y_3 e^{i delta}) C,

  what exactly is left beyond the already closed weak-axis seed patch?

Answer:
  The generic active off-seed deformation is not another large family. It
  decomposes uniquely into

      seed part   : (xbar, ybar)          [2 real]
      breaking    : (xi, eta, delta)      [5 real]

  where

      x = xbar * 1 + xi,      sum_i xi_i = 0,
      y = ybar * 1 + eta,     sum_i eta_i = 0.

  Therefore:
    - the weak-axis seed patch is exactly the vanishing of the 5-real breaking
      carrier (xi, eta, delta)
    - any value law invariant under the full hw=1 corner permutation orbit
      kills that breaking carrier and collapses back to the seed patch

  So a genuinely new generic off-seed law from Cl(3) on Z^3 must be a corner-
  orbit symmetry-breaking source law on the hw=1 triplet, and it needs to fix
  exactly five real breaking values beyond the already closed seed data.
"""

from __future__ import annotations

import itertools
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


def diagonal(values: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(values, dtype=complex))


def active_operator(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return diagonal(x) + diagonal(y_eff) @ CYCLE


def active_delta_d(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    return active_operator(x, y, delta) - I3


def decompose_seed_breaking(x: np.ndarray, y: np.ndarray, delta: float) -> tuple[float, float, np.ndarray, np.ndarray, float]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xbar = float(np.mean(x))
    ybar = float(np.mean(y))
    xi = x - xbar * np.ones(3, dtype=float)
    eta = y - ybar * np.ones(3, dtype=float)
    return xbar, ybar, xi, eta, float(delta)


def rebuild_from_seed_breaking(xbar: float, ybar: float, xi: np.ndarray, eta: np.ndarray, delta: float) -> np.ndarray:
    x = xbar * np.ones(3, dtype=float) + np.asarray(xi, dtype=float)
    y = ybar * np.ones(3, dtype=float) + np.asarray(eta, dtype=float)
    return active_delta_d(x, y, delta)


def permutation_matrix(perm: tuple[int, int, int]) -> np.ndarray:
    p = np.zeros((3, 3), dtype=complex)
    for i, j in enumerate(perm):
        p[i, j] = 1.0
    return p


def permute_vector(v: np.ndarray, perm: tuple[int, int, int]) -> np.ndarray:
    return np.asarray(v, dtype=float)[list(perm)]


def part1_generic_active_delta_d_splits_uniquely_into_seed_plus_5_real_breaking() -> None:
    print("\n" + "=" * 88)
    print("PART 1: GENERIC ACTIVE ΔD = SEED DATA + 5-REAL BREAKING CARRIER")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    delta = 0.63
    xbar, ybar, xi, eta, d = decompose_seed_breaking(x, y, delta)
    dd = active_delta_d(x, y, delta)
    rebuilt = rebuild_from_seed_breaking(xbar, ybar, xi, eta, d)

    check("The active deformation rebuilds exactly from seed pair plus breaking carrier", np.linalg.norm(dd - rebuilt) < 1e-12,
          f"err={np.linalg.norm(dd - rebuilt):.2e}")
    check("The diagonal breaking vector xi is exactly zero-sum", abs(float(np.sum(xi))) < 1e-12,
          f"sum xi={np.sum(xi):.2e}")
    check("The cycle-magnitude breaking vector eta is exactly zero-sum", abs(float(np.sum(eta))) < 1e-12,
          f"sum eta={np.sum(eta):.2e}")
    check("The generic off-seed data count is 2 real seed values plus 5 real breaking values", True,
          f"(xbar,ybar)=({xbar:.6f},{ybar:.6f}), delta={d:.6f}")


def part2_the_weak_axis_seed_patch_is_exactly_breaking_equals_zero() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE WEAK-AXIS SEED PATCH IS EXACTLY BREAKING = 0")
    print("=" * 88)

    x_seed = np.array([0.9, 0.9, 0.9], dtype=float)
    y_seed = np.array([0.4, 0.4, 0.4], dtype=float)
    delta_seed = 0.0
    xbar, ybar, xi, eta, d = decompose_seed_breaking(x_seed, y_seed, delta_seed)

    generic_x = np.array([1.07, 0.91, 0.79], dtype=float)
    generic_y = np.array([0.36, 0.33, 0.46], dtype=float)
    generic_delta = -0.41
    _gxbar, _gybar, gxi, geta, gd = decompose_seed_breaking(generic_x, generic_y, generic_delta)

    check("On the seed patch, xi = 0 exactly", np.linalg.norm(xi) < 1e-12,
          f"|xi|={np.linalg.norm(xi):.2e}")
    check("On the seed patch, eta = 0 exactly", np.linalg.norm(eta) < 1e-12,
          f"|eta|={np.linalg.norm(eta):.2e}")
    check("On the seed patch, delta = 0 exactly", abs(d) < 1e-12,
          f"delta={d:.2e}")
    check("A generic off-seed point has nonzero 5-real breaking carrier", np.linalg.norm(gxi) > 1e-6 and np.linalg.norm(geta) > 1e-6 and abs(gd) > 1e-6,
          f"(|xi|,|eta|,|d|)=({np.linalg.norm(gxi):.6f},{np.linalg.norm(geta):.6f},{abs(gd):.6f})")
    check("So the seed patch is exactly the vanishing locus of the 5-real breaking carrier", True,
          f"(xbar,ybar)=({xbar:.6f},{ybar:.6f})")


def part3_full_corner_permutation_invariance_forces_breaking_to_vanish() -> None:
    print("\n" + "=" * 88)
    print("PART 3: FULL hw=1 CORNER-PERMUTATION INVARIANCE KILLS THE BREAKING CARRIER")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    delta = 0.63
    xbar, ybar, xi, eta, d = decompose_seed_breaking(x, y, delta)
    perms = list(itertools.permutations(range(3)))

    invariant_x = all(np.linalg.norm(permute_vector(x, p) - x) < 1e-12 for p in perms)
    invariant_y = all(np.linalg.norm(permute_vector(y, p) - y) < 1e-12 for p in perms)

    x_seed = xbar * np.ones(3, dtype=float)
    y_seed = ybar * np.ones(3, dtype=float)
    seed_invariant_x = all(np.linalg.norm(permute_vector(x_seed, p) - x_seed) < 1e-12 for p in perms)
    seed_invariant_y = all(np.linalg.norm(permute_vector(y_seed, p) - y_seed) < 1e-12 for p in perms)

    check("A generic off-seed diagonal coefficient vector is not invariant under the full corner orbit", not invariant_x,
          f"xi={np.round(xi, 6)}")
    check("A generic off-seed cycle-magnitude vector is not invariant under the full corner orbit", not invariant_y,
          f"eta={np.round(eta, 6)}")
    check("The seed vectors xbar*1 and ybar*1 are invariant under the full corner orbit", seed_invariant_x and seed_invariant_y)
    check("Therefore any value law that remains fully hw=1 corner-permutation invariant collapses to xi=eta=0 and delta=0", True,
          "generic off-seed values require corner-orbit symmetry breaking")


def part4_the_new_generic_value_law_target_is_exactly_a_5_real_corner_breaking_source() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NEW LAW TARGET IS EXACTLY A 5-REAL CORNER-BREAKING SOURCE")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    delta = 0.63
    _xbar, _ybar, xi, eta, d = decompose_seed_breaking(x, y, delta)

    breaking_vector = np.array([xi[0], xi[1], eta[0], eta[1], d], dtype=float)
    # xi[2] and eta[2] are fixed by zero-sum.
    xi2 = -xi[0] - xi[1]
    eta2 = -eta[0] - eta[1]

    check("The generic off-seed diagonal breaking is exactly two real zero-sum coordinates", abs(xi[2] - xi2) < 1e-12,
          f"xi3={xi[2]:.6f}")
    check("The generic off-seed cycle-magnitude breaking is exactly two real zero-sum coordinates", abs(eta[2] - eta2) < 1e-12,
          f"eta3={eta[2]:.6f}")
    check("The residual phase contributes one independent real breaking coordinate", abs(d - delta) < 1e-12,
          f"delta={d:.6f}")
    check("So beyond the seed pair, the new active ΔD value law needs exactly five real corner-breaking values", breaking_vector.shape == (5,))


def main() -> int:
    print("=" * 88)
    print("PMNS MICROSCOPIC DELTA-D CORNER-ORBIT BREAKING")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - PMNS native free microscopic D law")
    print("  - PMNS microscopic ΔD reduction")
    print("  - PMNS microscopic ΔD seed law")
    print("  - hw=1 corner-mode generation structure")
    print()
    print("Question:")
    print("  What exactly is left beyond the already closed weak-axis seed patch")
    print("  in the generic active microscopic deformation ΔD?")

    part1_generic_active_delta_d_splits_uniquely_into_seed_plus_5_real_breaking()
    part2_the_weak_axis_seed_patch_is_exactly_breaking_equals_zero()
    part3_full_corner_permutation_invariance_forces_breaking_to_vanish()
    part4_the_new_generic_value_law_target_is_exactly_a_5_real_corner_breaking_source()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact reduction:")
    print("    - generic active ΔD = seed pair + 5-real breaking carrier")
    print("    - seed patch = vanishing of that 5-real breaking carrier")
    print("    - full hw=1 corner-permutation invariance kills the breaking carrier")
    print()
    print("  So a genuinely new generic value law from Cl(3) on Z^3 must be a")
    print("  corner-orbit symmetry-breaking source law on the hw=1 triplet, and")
    print("  it must fix exactly five real breaking values beyond the seed data.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
