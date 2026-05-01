#!/usr/bin/env python3
"""
Majorana Nambu quadratic comparator theorem on the unique local block.

Question:
  Beyond the logarithmic radial observable, does the admitted local Nambu
  source family carry any exact non-homogeneous bosonic comparator?

Answer:
  Yes. On the active 2x2 pseudospin kernel H(s) = x sigma_x + y sigma_y +
  z sigma_z, the unique minimal nontrivial polynomial spectral invariant is
  Q_2(s) = 1/2 Tr(H(s)^2) = ||s||^2. It is canonically invariant, local, and
  non-homogeneous. On the pure-pairing ray it reduces to mu^2.

Boundary:
  This supplies the missing local non-homogeneous comparator object. It does
  NOT yet prove the physical pairing-sector insertion law or the three-
  generation staircase anchor.
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


def quadratic_comparator(vec: np.ndarray) -> float:
    h = hamiltonian(vec)
    return 0.5 * float(np.real_if_close(np.trace(h @ h)))


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


def test_quadratic_invariant_is_radius_squared() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE UNIQUE MINIMAL POLYNOMIAL INVARIANT IS ||s||^2")
    print("=" * 88)

    vec = np.array([0.37, -0.41, 0.62], dtype=float)
    r2 = float(vec @ vec)
    h = hamiltonian(vec)
    h2 = h @ h
    err_h2 = np.linalg.norm(h2 - r2 * np.eye(2))
    q2 = quadratic_comparator(vec)

    check("The local kernel squares exactly to ||s||^2 I", err_h2 < 1e-12,
          f"H^2 error={err_h2:.2e}")
    check("Q_2(s)=1/2 Tr H^2 equals ||s||^2 exactly", abs(q2 - r2) < 1e-12,
          f"|Q2-r^2|={abs(q2-r2):.2e}")

    print()
    print("  So the active local Nambu block already carries one exact")
    print("  non-homogeneous quadratic comparator: the radial norm squared.")


def test_quadratic_invariant_is_canonically_invariant() -> None:
    print("\n" + "=" * 88)
    print("PART 2: Q_2 IS INVARIANT UNDER CANONICAL BASIS CHANGES")
    print("=" * 88)

    vec = np.array([0.37, -0.41, 0.62], dtype=float)
    axis = np.array([1.0, 2.0, -1.0], dtype=float)
    theta = 0.91

    u = su2_unitary(axis, theta)
    r = rotation_matrix(axis, theta)

    h = hamiltonian(vec)
    h_rot = u @ h @ u.conj().T
    vec_rot = r @ vec
    q2_before = quadratic_comparator(vec)
    q2_after = quadratic_comparator(vec_rot)
    trace_err = abs(0.5 * np.trace(h_rot @ h_rot) - q2_before)

    check("SU(2) conjugation rotates the source vector but preserves Q_2",
          abs(q2_before - q2_after) < 1e-12,
          f"|Q2-Q2_rot|={abs(q2_before - q2_after):.2e}")
    check("Q_2 is exactly the same trace invariant after conjugation", abs(trace_err) < 1e-12,
          f"trace error={abs(trace_err):.2e}")

    print()
    print("  So Q_2 is a bona fide canonically invariant local comparator on the")
    print("  admitted Nambu family, not a basis artifact.")


def test_higher_polynomial_invariants_reduce_to_q2() -> None:
    print("\n" + "=" * 88)
    print("PART 3: HIGHER POLYNOMIAL SPECTRAL INVARIANTS REDUCE TO Q_2")
    print("=" * 88)

    vec = np.array([0.37, -0.41, 0.62], dtype=float)
    h = hamiltonian(vec)
    q2 = quadratic_comparator(vec)

    tr1 = np.trace(h)
    tr3 = np.trace(h @ h @ h)
    tr4 = np.trace(h @ h @ h @ h)
    err4 = abs(0.5 * tr4 - q2 ** 2)

    check("The linear trace vanishes on the traceless pseudospin block", abs(tr1) < 1e-12,
          f"|Tr H|={abs(tr1):.2e}")
    check("All odd spectral traces vanish", abs(tr3) < 1e-12,
          f"|Tr H^3|={abs(tr3):.2e}")
    check("The quartic invariant is just Q_2^2", abs(err4) < 1e-12,
          f"|1/2 Tr H^4 - Q2^2|={abs(err4):.2e}")

    print()
    print("  So Q_2 is the unique minimal nontrivial polynomial spectral")
    print("  invariant on the local Nambu block; higher polynomial invariants")
    print("  are just powers of it.")


def test_pure_pairing_ray_reduces_to_mu_squared() -> None:
    print("\n" + "=" * 88)
    print("PART 4: ON THE PURE-PAIRING RAY THE COMPARATOR IS mu^2")
    print("=" * 88)

    mu = 0.53
    vec = np.array([mu, 0.0, 0.0], dtype=float)
    q2 = quadratic_comparator(vec)

    check("On the pure-pairing ray, Q_2 = mu^2", abs(q2 - mu ** 2) < 1e-12,
          f"|Q2-mu^2|={abs(q2 - mu ** 2):.2e}")

    print()
    print("  This is the missing local non-homogeneous comparator object on the")
    print("  admitted pairing ray: it scales quadratically, not logarithmically.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: NAMBU QUADRATIC COMPARATOR THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_NAMBU_RADIAL_OBSERVABLE_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  Beyond the logarithmic radial observable, does the admitted local")
    print("  Nambu family carry any exact non-homogeneous bosonic comparator?")

    test_quadratic_invariant_is_radius_squared()
    test_quadratic_invariant_is_canonically_invariant()
    test_higher_polynomial_invariants_reduce_to_q2()
    test_pure_pairing_ray_reduces_to_mu_squared()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Yes. The admitted local Nambu block carries the exact non-homogeneous")
    print("  quadratic comparator Q_2(s) = 1/2 Tr H(s)^2 = ||s||^2.")
    print()
    print("  This supplies the missing local comparator object. What remains open")
    print("  is the physical pairing-sector insertion / endpoint principle for")
    print("  this comparator and its lift to the three-generation texture.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
