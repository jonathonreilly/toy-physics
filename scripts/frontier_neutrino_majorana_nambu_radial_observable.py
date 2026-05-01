#!/usr/bin/env python3
"""
Majorana Nambu radial observable theorem on the unique local block.

Question:
  Once the local Nambu-complete source family is admitted on the unique
  Majorana block, what is the minimal canonically invariant local bosonic
  observable on that block?

Answer:
  The local source family is one spin-1/2 pseudospin block. Any canonically
  invariant spectral scalar depends only on the radial pseudospin norm
  r = sqrt(x^2 + y^2 + z^2). The minimal additive CPT-even scalar is
  W_N(s) = 1/2 log|det H(s)| = log r + const for H(s) = x sigma_x + y sigma_y
  + z sigma_z.

Boundary:
  This is a positive beyond-retained-stack local bosonic observable on the
  admitted Nambu family. It does NOT fix a nonzero pairing amplitude or a
  staircase anchor. On the pure-pairing ray it reduces to log(mu). Later
  branch work adds the exact local quadratic comparator and the exact
  background-normalized local response curve, so the live blocker is now
  finite-point selection on that normalized curve.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
PAULIS = [SIGMA_X, SIGMA_Y, SIGMA_Z]


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


def hamiltonian(vec: np.ndarray) -> np.ndarray:
    return vec[0] * SIGMA_X + vec[1] * SIGMA_Y + vec[2] * SIGMA_Z


def su2_unitary(axis: np.ndarray, theta: float) -> np.ndarray:
    axis = axis / np.linalg.norm(axis)
    generator = axis[0] * SIGMA_X + axis[1] * SIGMA_Y + axis[2] * SIGMA_Z
    evals, evecs = np.linalg.eigh(generator)
    phases = np.diag(np.exp(-0.5j * theta * evals))
    return evecs @ phases @ evecs.conj().T


def rotation_matrix(axis: np.ndarray, theta: float) -> np.ndarray:
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c = math.cos(theta)
    s = math.sin(theta)
    t = 1.0 - c
    return np.array([
        [t * x * x + c, t * x * y - s * z, t * x * z + s * y],
        [t * x * y + s * z, t * y * y + c, t * y * z - s * x],
        [t * x * z - s * y, t * y * z + s * x, t * z * z + c],
    ], dtype=float)


def radial_generator(vec: np.ndarray) -> float:
    h = hamiltonian(vec)
    return 0.5 * math.log(abs(np.linalg.det(h)))


def test_spectral_block_depends_only_on_radius() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE LOCAL NAMBU BLOCK IS A RADIAL SPECTRAL FAMILY")
    print("=" * 88)

    vec = np.array([0.37, -0.41, 0.62], dtype=float)
    radius = np.linalg.norm(vec)
    h = hamiltonian(vec)
    evals = np.sort(np.real_if_close(np.linalg.eigvals(h)))
    target = np.array([-radius, radius], dtype=float)
    det_err = abs(np.linalg.det(h) + radius ** 2)

    check("Eigenvalues are exactly +/- ||s|| on the local Nambu block", np.linalg.norm(evals - target) < 1e-12,
          f"eig err={np.linalg.norm(evals - target):.2e}")
    check("The determinant is exactly -||s||^2", det_err < 1e-12,
          f"|det+r^2|={det_err:.2e}")

    print()
    print("  So the admitted local Nambu source family is one radial spectral")
    print("  family on the unique two-state pseudospin block.")


def test_canonical_rotations_preserve_radial_generator() -> None:
    print("\n" + "=" * 88)
    print("PART 2: CANONICAL BASIS CHANGES PRESERVE THE RADIAL GENERATOR")
    print("=" * 88)

    vec = np.array([0.37, -0.41, 0.62], dtype=float)
    axis = np.array([1.0, 2.0, -1.0], dtype=float)
    theta = 0.91
    u = su2_unitary(axis, theta)
    r = rotation_matrix(axis, theta)

    h = hamiltonian(vec)
    h_rot = u @ h @ u.conj().T
    target = hamiltonian(r @ vec)

    conj_err = np.linalg.norm(h_rot - target)
    w0 = radial_generator(vec)
    w1 = radial_generator(r @ vec)

    check("SU(2) conjugation rotates the local source vector exactly", conj_err < 1e-12,
          f"conjugation error={conj_err:.2e}")
    check("The minimal spectral scalar is invariant under canonical rotations", abs(w0 - w1) < 1e-12,
          f"|W-W_rot|={abs(w0 - w1):.2e}")

    print()
    print("  So any canonically invariant local bosonic observable on this")
    print("  admitted Nambu family can only depend on the radial norm ||s||.")


def test_pure_pairing_ray_reduces_to_log_mu() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE RADIAL OBSERVABLE REDUCES TO THE PAIRING LOG ON mu J_x")
    print("=" * 88)

    mu = 0.53
    vec = np.array([mu, 0.0, 0.0], dtype=float)
    w = radial_generator(vec)
    w_expected = math.log(mu)

    eps = 1e-7
    wp = radial_generator(np.array([mu + eps, 0.0, 0.0], dtype=float))
    wm = radial_generator(np.array([mu - eps, 0.0, 0.0], dtype=float))
    deriv_num = (wp - wm) / (2.0 * eps)
    deriv_exact = 1.0 / mu

    check("On the pure-pairing ray, the radial generator is log(mu)", abs(w - w_expected) < 1e-12,
          f"|W-log(mu)|={abs(w - w_expected):.2e}")
    check("Its pure-pairing derivative is 1/mu", abs(deriv_num - deriv_exact) < 1e-6,
          f"dW/dmu={deriv_num:.6f}, 1/mu={deriv_exact:.6f}")

    print()
    print("  So this positive local Nambu observable extends the Pfaffian lane,")
    print("  but it does not itself create a selected nonzero scale.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: NAMBU RADIAL OBSERVABLE THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md")
    print()
    print("Question:")
    print("  On the admitted local Nambu-complete source family, what is the")
    print("  minimal canonically invariant local bosonic observable?")

    test_spectral_block_depends_only_on_radius()
    test_canonical_rotations_preserve_radial_generator()
    test_pure_pairing_ray_reduces_to_log_mu()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The admitted local Nambu block is a radial spectral family. The")
    print("  minimal canonically invariant local bosonic observable is")
    print("  W_N(s) = 1/2 log|det H(s)| = log ||s|| + const.")
    print()
    print("  On the pure-pairing ray it reduces to log(mu). Later branch work")
    print("  adds the exact local quadratic comparator and the exact")
    print("  background-normalized response curve, so the live blocker is now")
    print("  finite-point selection on that normalized curve.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
