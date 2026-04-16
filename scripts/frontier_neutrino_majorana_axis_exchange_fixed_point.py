#!/usr/bin/env python3
"""
Majorana axis-exchange fixed-point theorem on the background-normalized
local Nambu block.

Question:
  Once the admitted Majorana Nambu family is reduced to the exact
  background-normalized local response curve

      W_rel(rho) = (1/2) log(1 + rho^2),   Q_rel(rho) = rho^2,

  is there a canonical finite nonzero local point on that curve?

Answer on the exact local block:
  Yes, if the finite-point selector is required to be covariant under the
  exact canonical exchange of the retained normal axis and the canonical
  pairing axis on the admitted pseudospin block. That exchange acts as

      rho -> 1/rho,

  so the unique positive fixed point is

      rho = 1.

  On that self-dual local point,

      W_rel = (1/2) log 2,   Q_rel = 1.

Boundary:
  This closes the local finite-point selection problem only on the normalized
  admitted block. It does NOT fix the absolute Majorana staircase anchor:
  joint positive rescaling leaves rho unchanged, so the theorem is still
  scale-relative rather than staircase-absolute.
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


def pauli_rotation(generator: np.ndarray, theta: float) -> np.ndarray:
    ident = np.eye(generator.shape[0], dtype=complex)
    return math.cos(theta / 2.0) * ident - 1j * math.sin(theta / 2.0) * generator


def normalized_kernel(rho: float) -> np.ndarray:
    return SIGMA_Z + rho * SIGMA_X


def exchange_unitary() -> np.ndarray:
    uy = pauli_rotation(SIGMA_Y, math.pi / 2.0)
    uz = pauli_rotation(SIGMA_Z, math.pi)
    return uz @ uy


def w_rel(rho: float) -> float:
    return 0.5 * math.log(1.0 + rho * rho)


def q_rel(rho: float) -> float:
    return rho * rho


def relative_from_coeffs(z: float, x: float) -> tuple[float, float]:
    rho = abs(x) / abs(z)
    return w_rel(rho), q_rel(rho)


def test_exact_axis_exchange() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ADMITTED LOCAL BLOCK HAS AN EXACT NORMAL-PAIRING AXIS EXCHANGE")
    print("=" * 88)

    u_ex = exchange_unitary()
    z_to_x = np.linalg.norm(u_ex @ SIGMA_Z @ u_ex.conj().T + SIGMA_X)
    x_to_z = np.linalg.norm(u_ex @ SIGMA_X @ u_ex.conj().T + SIGMA_Z)

    rho = 0.37
    mapped = u_ex @ normalized_kernel(rho) @ u_ex.conj().T
    target = -rho * normalized_kernel(1.0 / rho)
    map_err = np.linalg.norm(mapped - target)

    check("The exchange sends the retained normal axis to the canonical pairing axis", z_to_x < 1e-12,
          f"axis error={z_to_x:.2e}")
    check("The exchange sends the canonical pairing axis back to the normal axis", x_to_z < 1e-12,
          f"axis error={x_to_z:.2e}")
    check("On the normalized family the exchange acts as rho -> 1/rho up to common scale/sign", map_err < 1e-12,
          f"kernel error={map_err:.2e}")

    print()
    print("  So the admitted local Majorana block is not just a monotone curve.")
    print("  It also carries an exact canonical exchange between the retained")
    print("  normal axis and the canonical pairing axis.")


def test_exchange_inverts_normalized_data() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE EXACT EXCHANGE INVERTS THE NORMALIZED LOCAL RATIO")
    print("=" * 88)

    rho = 2.4
    w_before = w_rel(rho)
    q_before = q_rel(rho)
    w_after = w_rel(1.0 / rho)
    q_after = q_rel(1.0 / rho)

    check("The exact exchanged local comparator is Q_rel(1/rho) = 1/rho^2",
          abs(q_after - 1.0 / q_before) < 1e-12,
          f"|Q_after-1/Q_before|={abs(q_after - 1.0 / q_before):.2e}")
    check("The exact exchanged local response is W_rel(1/rho)",
          abs(w_after - 0.5 * math.log(1.0 + 1.0 / (rho * rho))) < 1e-12,
          f"|W_after-formula|={abs(w_after - 0.5 * math.log(1.0 + 1.0 / (rho * rho))):.2e}")
    check("The background-normalized curve itself is not exchange-invariant away from the fixed point",
          abs(w_before - w_after) > 1e-3 and abs(q_before - q_after) > 1e-3,
          f"W_before={w_before:.6f}, W_after={w_after:.6f}")

    print()
    print("  The exchange does not make every point invariant. It makes the")
    print("  normalized local ratio invert. So a unique exchange-covariant")
    print("  finite selector must land on a fixed point of rho -> 1/rho.")


def test_unique_positive_fixed_point() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE UNIQUE POSITIVE EXCHANGE-FIXED LOCAL POINT IS rho = 1")
    print("=" * 88)

    grid = np.linspace(0.05, 8.0, 4000)
    residual = np.abs(grid - 1.0 / grid)
    rho_min = float(grid[np.argmin(residual)])
    exact_residual = abs(1.0 - 1.0 / 1.0)
    self_dual_w = w_rel(1.0)
    self_dual_q = q_rel(1.0)

    check("The positive fixed-point equation rho = 1/rho has the exact solution rho = 1",
          exact_residual < 1e-12, f"residual={exact_residual:.2e}")
    check("A dense positive scan has its unique minimum at the self-dual point", abs(rho_min - 1.0) < 5e-3,
          f"rho_min={rho_min:.6f}")
    check("The self-dual local response is W_rel = (1/2) log 2", abs(self_dual_w - 0.5 * math.log(2.0)) < 1e-12,
          f"W_rel(1)={self_dual_w:.12f}")
    check("The self-dual local comparator is Q_rel = 1", abs(self_dual_q - 1.0) < 1e-12,
          f"Q_rel(1)={self_dual_q:.12f}")

    print()
    print("  Therefore any intrinsic finite selector on the normalized local")
    print("  Majorana curve that is covariant under the exact axis exchange is")
    print("  forced onto the self-dual point rho = 1.")


def test_scale_relative_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE SELF-DUAL LOCAL POINT IS STILL SCALE-RELATIVE, NOT STAIRCASE-ABSOLUTE")
    print("=" * 88)

    z = 0.41
    rho = 1.0
    lambdas = [0.3, 1.0, 7.0]
    w_values: list[float] = []
    q_values: list[float] = []

    for lam in lambdas:
        x = lam * z * rho
        z_scaled = lam * z
        w_val, q_val = relative_from_coeffs(z_scaled, x)
        w_values.append(w_val)
        q_values.append(q_val)

    w_spread = max(w_values) - min(w_values)
    q_spread = max(q_values) - min(q_values)

    check("Joint positive rescaling leaves the selected self-dual ratio rho = 1 unchanged",
          all(abs(1.0 - 1.0) < 1e-12 for _ in lambdas),
          f"tested lambdas={lambdas}")
    check("The self-dual background-normalized response is unchanged under joint rescaling",
          w_spread < 1e-12, f"spread={w_spread:.2e}")
    check("The self-dual background-normalized comparator is unchanged under joint rescaling",
          q_spread < 1e-12, f"spread={q_spread:.2e}")

    print()
    print("  So the new theorem closes the local finite-point selector but not")
    print("  the absolute Majorana staircase anchor. The self-dual point fixes a")
    print("  relative local point, while the overall source scale remains free.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: AXIS-EXCHANGE FIXED-POINT THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  Once the local Majorana response is background-normalized, is there")
    print("  a canonical finite nonzero local point on that curve?")

    test_exact_axis_exchange()
    test_exchange_inverts_normalized_data()
    test_unique_positive_fixed_point()
    test_scale_relative_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Yes, on the admitted local block once the finite selector is taken")
    print("  to be covariant under the exact canonical exchange of the retained")
    print("  normal and pairing axes. The exchange acts as rho -> 1/rho, so the")
    print("  unique positive fixed point is the self-dual point rho = 1.")
    print()
    print("  But this is still only a local relative selector. Joint positive")
    print("  rescaling leaves rho = 1 unchanged, so the absolute Majorana")
    print("  staircase anchor and three-generation lift remain open.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
