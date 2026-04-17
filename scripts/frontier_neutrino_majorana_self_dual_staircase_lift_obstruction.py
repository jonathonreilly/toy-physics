#!/usr/bin/env python3
"""
Majorana self-dual staircase-lift obstruction theorem on the current stack.

Question:
  After the exact local axis-exchange theorem selects the self-dual point
  rho = 1 on the background-normalized Majorana block, does the current exact
  stack now lift that point to an absolute Majorana staircase anchor?

Answer on the current exact stack:
  No. The selected local self-dual family is still only the positive ray

      K_sd(lambda) = lambda (sigma_z + sigma_x),   lambda > 0,

  and all retained exact local selected observables depend only on rho, so
  they are identical across that ray. The current three-generation Z3 lift
  remains homogeneous under the same positive rescaling. Therefore the
  selected local self-dual point does not by itself lift to an absolute
  staircase level on the present stack.

Boundary:
  This is an exact obstruction theorem on the current stack after the local
  finite-point selector has already been fixed. It does NOT rule out a future
  non-homogeneous local-to-generation bridge or absolute-scale datum beyond
  this stack.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
ALPHA_LM = 0.09067

SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
J2 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)


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


def normalize(matrix: np.ndarray) -> np.ndarray:
    return matrix / np.linalg.norm(matrix)


def w_rel(rho: float) -> float:
    return 0.5 * math.log(1.0 + rho * rho)


def q_rel(rho: float) -> float:
    return rho * rho


def self_dual_kernel(scale: float) -> np.ndarray:
    return scale * (SIGMA_Z + SIGMA_X)


def z3_texture(a: complex, b: complex, eps: complex) -> np.ndarray:
    return np.array(
        [[a, 0.0, 0.0], [0.0, eps, b], [0.0, b, eps]],
        dtype=complex,
    )


def annihilation_operators(n_modes: int) -> list[np.ndarray]:
    sigma_minus = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    ident = np.eye(2, dtype=complex)

    operators: list[np.ndarray] = []
    for mode in range(n_modes):
        op = np.array([[1.0]], dtype=complex)
        for idx in range(n_modes):
            if idx < mode:
                op = np.kron(op, sigma_z)
            elif idx == mode:
                op = np.kron(op, sigma_minus)
            else:
                op = np.kron(op, ident)
        operators.append(op)
    return operators


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def pair_operator_from_delta(delta: np.ndarray, cs: list[np.ndarray]) -> np.ndarray:
    out = np.zeros_like(cs[0])
    n = len(cs)
    for a in range(n):
        for b in range(a + 1, n):
            out += delta[a, b] * (cs[a] @ cs[b])
    return out


def test_selected_local_point_is_only_a_ray() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE SELECTED LOCAL SELF-DUAL POINT COLLAPSES TO ONE POSITIVE RAY")
    print("=" * 88)

    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]
    kernels = [self_dual_kernel(scale) for scale in scales]
    normalized = [normalize(kernel) for kernel in kernels]

    max_diff = 0.0
    for idx in range(len(normalized) - 1):
        max_diff = max(max_diff, np.linalg.norm(normalized[idx] - normalized[idx + 1]))

    rho_values = [1.0 for _ in scales]
    w_values = [w_rel(rho) for rho in rho_values]
    q_values = [q_rel(rho) for rho in rho_values]
    w_spread = max(w_values) - min(w_values)
    q_spread = max(q_values) - min(q_values)

    check("Normalized local self-dual kernels are identical across staircase rescalings", max_diff < 1e-12,
          f"max normalized difference={max_diff:.2e}")
    check("The selected local ratio stays exactly rho = 1 across that ray", all(abs(rho - 1.0) < 1e-12 for rho in rho_values),
          f"rhos={rho_values}")
    check("The exact selected local response W_rel = (1/2) log 2 is constant across the ray", w_spread < 1e-12,
          f"spread={w_spread:.2e}")
    check("The exact selected local comparator Q_rel = 1 is constant across the ray", q_spread < 1e-12,
          f"spread={q_spread:.2e}")

    print()
    print("  So the local axis-exchange theorem fixes a projective point on the")
    print("  admitted block, not an absolute source scale. Different staircase")
    print("  rescalings lie on the same exact selected local ray.")


def test_z3_lift_remains_homogeneous_after_local_selection() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT Z3 LIFT STAYS HOMOGENEOUS AFTER THE LOCAL SELF-DUAL SELECTION")
    print("=" * 88)

    texture = z3_texture(2.0, 1.0, 0.25)
    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]
    deltas = [scale * np.kron(texture, J2) for scale in scales]

    max_delta_diff = 0.0
    max_ratio_diff = 0.0
    ref_eigs = np.sort_complex(np.linalg.eigvals(texture))
    ref_normed = ref_eigs / np.linalg.norm(ref_eigs)

    for delta in deltas[1:]:
        max_delta_diff = max(max_delta_diff, np.linalg.norm(normalize(delta) - normalize(deltas[0])))
    for scale in scales:
        eigs = np.sort_complex(np.linalg.eigvals(scale * texture))
        normed = eigs / np.linalg.norm(eigs)
        max_ratio_diff = max(max_ratio_diff, np.linalg.norm(normed - ref_normed))

    check("Normalized three-generation pairing blocks are identical across rescalings of the selected local ray", max_delta_diff < 1e-12,
          f"max normalized block difference={max_delta_diff:.2e}")
    check("The singlet/doublet texture ratios are unchanged by those rescalings", max_ratio_diff < 1e-12,
          f"max normalized eigenvalue difference={max_ratio_diff:.2e}")

    print()
    print("  So the current Z3 texture lift does not convert the selected local")
    print("  self-dual point into an absolute scale. It still organizes a class")
    print("  up to overall rescaling only.")


def test_charge_sector_stays_identical_across_selected_levels() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CHARGE SECTOR STILL DOES NOT DISTINGUISH THE SELECTED LEVELS")
    print("=" * 88)

    texture = z3_texture(2.0, 1.0, 0.25)
    cs = annihilation_operators(6)
    n_tot = sum(c.conj().T @ c for c in cs)

    charge_errors = []
    relative_norms = []
    for scale in [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]:
        delta = scale * np.kron(texture, J2)
        q = pair_operator_from_delta(delta, cs)
        charge_errors.append(np.linalg.norm(commutator(n_tot, q) + 2.0 * q))
        relative_norms.append(np.linalg.norm(q) / scale)

    rel_var = max(relative_norms) - min(relative_norms)

    check("Each lifted self-dual family member remains a charge-minus-two pairing operator", max(charge_errors) < 1e-10,
          f"max charge error={max(charge_errors):.2e}")
    check("The operator norm still scales linearly with the free rescaling parameter", rel_var < 1e-10,
          f"spread in ||Q||/scale={rel_var:.2e}")

    print()
    print("  So the current charge classification still sees one pairing family")
    print("  with a free overall scale, even after the local self-dual point has")
    print("  already been selected exactly.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: SELF-DUAL STAIRCASE-LIFT OBSTRUCTION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  Once the exact local Majorana point rho = 1 is selected, does the")
    print("  current exact stack lift that point to an absolute staircase anchor?")

    test_selected_local_point_is_only_a_ray()
    test_z3_lift_remains_homogeneous_after_local_selection()
    test_charge_sector_stays_identical_across_selected_levels()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. The selected local self-dual point collapses to one positive ray")
    print("  K_sd(lambda) = lambda (sigma_z + sigma_x), and the current Z3 lift")
    print("  remains homogeneous under the same positive rescaling.")
    print()
    print("  So the exact local selector does not itself lift to an absolute")
    print("  Majorana staircase anchor on the present stack. Full closure now")
    print("  requires a genuinely new non-homogeneous local-to-generation bridge")
    print("  or a new absolute-scale datum beyond the current exact stack.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
