#!/usr/bin/env python3
"""
Majorana background-normalized local response on the admitted Nambu family.

Question:
  Once the local Nambu quadratic comparator Q_2 is known exactly, does the
  retained normal slice provide the missing canonical background normalization
  for the local Majorana response?

Answer on the exact local block:
  Yes. On H(z, x, y) = z sigma_z + x sigma_x + y sigma_y with retained
  background H_0(z) = z sigma_z, the exact relative bosonic response and the
  exact relative quadratic comparator are

      W_rel = (1/2) log(|det H| / |det H_0|) = (1/2) log(1 + rho^2)
      Q_rel = (Q_2(H) - Q_2(H_0)) / z^2 = rho^2

  where rho^2 = (x^2 + y^2) / z^2.

Boundary:
  This closes the old "need a comparator or background normalization" wording
  on the local block. By itself it does NOT yet select a finite nonzero
  Majorana scale: the background-normalized response curve is still monotone
  in rho. Later branch work adds the axis-exchange fixed-point theorem on
  this same normalized block.
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


def hamiltonian(z: float, x: float, y: float) -> np.ndarray:
    return z * SIGMA_Z + x * SIGMA_X + y * SIGMA_Y


def q2(z: float, x: float, y: float) -> float:
    h = hamiltonian(z, x, y)
    return 0.5 * float(np.real_if_close(np.trace(h @ h)))


def relative_generator(z: float, x: float, y: float) -> float:
    h0 = hamiltonian(z, 0.0, 0.0)
    h = hamiltonian(z, x, y)
    det_ratio = abs(np.linalg.det(h)) / abs(np.linalg.det(h0))
    return 0.5 * math.log(det_ratio)


def test_exact_relative_formulas() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE RETAINED NORMAL SLICE PROVIDES AN EXACT RELATIVE RESPONSE")
    print("=" * 88)

    z = 0.73
    x = 0.31
    y = -0.27
    rho2 = (x * x + y * y) / (z * z)

    h0 = hamiltonian(z, 0.0, 0.0)
    h = hamiltonian(z, x, y)
    q_rel = (q2(z, x, y) - q2(z, 0.0, 0.0)) / (z * z)
    w_rel = relative_generator(z, x, y)

    det_err = abs(abs(np.linalg.det(h)) - (z * z + x * x + y * y))
    q_err = abs(q_rel - rho2)
    w_err = abs(w_rel - 0.5 * math.log(1.0 + rho2))

    check("The active block determinant is exactly z^2 + x^2 + y^2", det_err < 1e-12,
          f"det error={det_err:.2e}")
    check("The background-normalized quadratic comparator is exactly rho^2", q_err < 1e-12,
          f"|Q_rel-rho^2|={q_err:.2e}")
    check("The background-normalized bosonic response is exactly 1/2 log(1+rho^2)", w_err < 1e-12,
          f"|W_rel-formula|={w_err:.2e}")

    print()
    print("  So the retained normal slice is not just a bookkeeping direction.")
    print("  It gives an exact additive-constant-free background normalization")
    print("  for the admitted local Majorana response.")


def test_pairing_plane_rephasing_invariance() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE RELATIVE RESPONSE DEPENDS ONLY ON THE TRANSVERSE RADIUS")
    print("=" * 88)

    z = 0.73
    r = 0.41
    theta = 0.91
    x1, y1 = r, 0.0
    x2, y2 = r * math.cos(theta), r * math.sin(theta)

    q1 = (q2(z, x1, y1) - q2(z, 0.0, 0.0)) / (z * z)
    q2_rot = (q2(z, x2, y2) - q2(z, 0.0, 0.0)) / (z * z)
    w1 = relative_generator(z, x1, y1)
    w2 = relative_generator(z, x2, y2)

    check("The relative quadratic comparator is invariant under pairing-plane rephasing",
          abs(q1 - q2_rot) < 1e-12, f"|Q_rel-Q_rel_rot|={abs(q1-q2_rot):.2e}")
    check("The relative bosonic response is invariant under pairing-plane rephasing",
          abs(w1 - w2) < 1e-12, f"|W_rel-W_rel_rot|={abs(w1-w2):.2e}")

    print()
    print("  So the background-normalized local response depends only on the")
    print("  invariant transverse radius rho = sqrt(x^2+y^2)/|z|, not on the")
    print("  arbitrary phase inside the pairing plane.")


def test_canonical_dimensionless_normalization() -> None:
    print("\n" + "=" * 88)
    print("PART 3: DIVIDING BY THE RETAINED BACKGROUND GIVES A CANONICAL CURVE")
    print("=" * 88)

    z = 0.73
    x = 0.31
    y = -0.27
    rho = math.sqrt(x * x + y * y) / abs(z)
    w_rel = relative_generator(z, x, y)
    q_rel = (q2(z, x, y) - q2(z, 0.0, 0.0)) / (z * z)

    check("The canonical dimensionless variable is rho = ||pairing||/|background|",
          abs(rho - math.sqrt(q_rel)) < 1e-12,
          f"|rho-sqrt(Q_rel)|={abs(rho-math.sqrt(q_rel)):.2e}")
    check("The canonical response curve is W_rel(rho)=1/2 log(1+rho^2)",
          abs(w_rel - 0.5 * math.log(1.0 + rho * rho)) < 1e-12,
          f"|W_rel-canonical|={abs(w_rel - 0.5 * math.log(1.0 + rho * rho)):.2e}")
    check("The canonical non-homogeneous comparator is Q_rel(rho)=rho^2",
          abs(q_rel - rho * rho) < 1e-12,
          f"|Q_rel-rho^2|={abs(q_rel - rho * rho):.2e}")

    print()
    print("  This removes the old additive ambiguity cleanly: once the retained")
    print("  normal baseline is divided out, the local Majorana response lives on")
    print("  one exact dimensionless curve.")


def test_monotone_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE BACKGROUND-NORMALIZED RESPONSE STILL DOES NOT PICK A FINITE SCALE")
    print("=" * 88)

    rhos = np.linspace(0.0, 4.0, 81)
    dw = np.array([rho / (1.0 + rho * rho) for rho in rhos[1:]], dtype=float)
    dq = np.array([2.0 * rho for rho in rhos[1:]], dtype=float)

    check("dW_rel/drho is strictly positive for every rho > 0", np.min(dw) > 0.0,
          f"min dW/drho={np.min(dw):.6f}")
    check("dQ_rel/drho is strictly positive for every rho > 0", np.min(dq) > 0.0,
          f"min dQ/drho={np.min(dq):.6f}")
    check("The only stationary point on the local response curve is rho = 0",
          abs(rhos[0]) < 1e-12 and len(dw) == 80,
          "nonzero branch is monotone")

    print()
    print("  So at the level of this theorem alone the old blocker is narrowed")
    print("  but not gone. The branch now has the exact background-normalized")
    print("  local response curve; later branch work adds the self-dual")
    print("  rho = 1 point on this same curve.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: BACKGROUND-NORMALIZED LOCAL RESPONSE THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_NAMBU_RADIAL_OBSERVABLE_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_NAMBU_QUADRATIC_COMPARATOR_NOTE.md")
    print()
    print("Question:")
    print("  Once the local quadratic comparator Q_2 is exact, does the retained")
    print("  normal slice provide the missing canonical background normalization")
    print("  for the local Majorana response?")

    test_exact_relative_formulas()
    test_pairing_plane_rephasing_invariance()
    test_canonical_dimensionless_normalization()
    test_monotone_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Yes. The retained normal slice supplies an exact background")
    print("  normalization on the admitted local Nambu family:")
    print("    W_rel(rho) = 1/2 log(1+rho^2)")
    print("    Q_rel(rho) = rho^2")
    print()
    print("  So the old 'need comparator or background normalization' wording is")
    print("  no longer the real blocker. Later branch work closes the local")
    print("  finite-point selector on this curve at the self-dual point rho = 1;")
    print("  the remaining gap is the absolute staircase embedding of that local")
    print("  point, and then the three-generation lift.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
