#!/usr/bin/env python3
"""
Majorana staircase-blindness theorem on the current exact source stack.

Question:
  Once the one-generation source ray and the three-generation Z3 texture class
  are fixed, does the current exact Majorana stack also fix the absolute
  Majorana staircase level?

Answer on the current exact source stack:
  No. The local canonical block and the Z3 texture lift are homogeneous under
  positive rescaling. They fix the source ray and the texture class, but not
  the absolute source scale. Therefore the current exact stack is blind to the
  absolute staircase anchor.

Boundary:
  This is an exact scale-boundary theorem on the current Majorana source stack.
  It does NOT rule out a future exact scale-setting principle beyond this
  stack.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
ALPHA_LM = 0.09067


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


def normalize(matrix: np.ndarray) -> np.ndarray:
    return matrix / np.linalg.norm(matrix)


def pair_operator_from_delta(delta: np.ndarray, cs: list[np.ndarray]) -> np.ndarray:
    n = len(cs)
    out = np.zeros_like(cs[0])
    for a in range(n):
        for b in range(a + 1, n):
            out += delta[a, b] * (cs[a] @ cs[b])
    return out


def z3_texture(a: complex, b: complex, eps: complex) -> np.ndarray:
    return np.array(
        [[a, 0.0, 0.0], [0.0, eps, b], [0.0, b, eps]],
        dtype=complex,
    )


def test_local_ray_is_scale_homogeneous() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ONE-GENERATION SOURCE RAY FIXES DIRECTION, NOT ABSOLUTE SCALE")
    print("=" * 88)

    j2 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    mus = [ALPHA_LM ** 4, ALPHA_LM ** 7, ALPHA_LM ** 8]

    normalized = [normalize(mu * j2) for mu in mus]
    max_diff = 0.0
    pf_logs = []
    for idx in range(len(mus) - 1):
        max_diff = max(max_diff, np.linalg.norm(normalized[idx] - normalized[idx + 1]))
    for mu in mus:
        pf_logs.append(math.log(abs(mu)))

    log_step_78 = pf_logs[2] - pf_logs[1]

    check("Normalized local canonical blocks are identical across staircase rescalings", max_diff < 1e-12,
          f"max normalized difference={max_diff:.2e}")
    check("The local Pfaffian generator shifts only by an additive log-scale constant", abs(log_step_78 - math.log(ALPHA_LM)) < 1e-12,
          f"log step={log_step_78:.6f}, log(alpha)={math.log(ALPHA_LM):.6f}")

    print()
    print("  The one-generation local source-ray theorem therefore fixes only a")
    print("  ray mu J_x, not an absolute mu. Rescaling moves along the same ray.")


def test_z3_texture_class_is_scale_homogeneous() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE THREE-GENERATION Z3 TEXTURE CLASS IS HOMOGENEOUS UNDER RESCALING")
    print("=" * 88)

    j2 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    m_ref = z3_texture(1.4, 0.52, 0.09 + 0.04j)
    scales = [ALPHA_LM ** 4, ALPHA_LM ** 7, ALPHA_LM ** 8]
    deltas = [scale * np.kron(m_ref, j2) for scale in scales]

    max_delta_diff = 0.0
    max_ratio_diff = 0.0
    ref_eigs = np.sort_complex(np.linalg.eigvals(m_ref))
    ref_normed = ref_eigs / np.linalg.norm(ref_eigs)
    for delta in deltas[1:]:
        max_delta_diff = max(max_delta_diff, np.linalg.norm(normalize(delta) - normalize(deltas[0])))
    for scale in scales:
        eigs = np.sort_complex(np.linalg.eigvals(scale * m_ref))
        normed = eigs / np.linalg.norm(eigs)
        max_ratio_diff = max(max_ratio_diff, np.linalg.norm(normed - ref_normed))

    check("Normalized Z3 pairing blocks are identical across staircase rescalings", max_delta_diff < 1e-12,
          f"max normalized block difference={max_delta_diff:.2e}")
    check("The singlet/doublet texture ratios are unchanged by overall rescaling", max_ratio_diff < 1e-12,
          f"max normalized eigenvalue difference={max_ratio_diff:.2e}")

    print()
    print("  So the exact current Z3 texture machinery fixes a class of matrices")
    print("  up to overall scale, not an absolute staircase anchor.")


def test_charge_sector_is_identical_across_staircase_levels() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE PAIRING CHARGE SECTOR DOES NOT DISTINGUISH STAIRCASE LEVELS")
    print("=" * 88)

    cs = annihilation_operators(6)
    n_tot = sum(c.conj().T @ c for c in cs)
    j2 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    m_ref = z3_texture(1.4, 0.52, 0.09 + 0.04j)

    charge_errors = []
    relative_norms = []
    for scale in [ALPHA_LM ** 4, ALPHA_LM ** 7, ALPHA_LM ** 8]:
        delta = scale * np.kron(m_ref, j2)
        q = pair_operator_from_delta(delta, cs)
        charge_errors.append(np.linalg.norm(commutator(n_tot, q) + 2.0 * q))
        relative_norms.append(np.linalg.norm(q) / scale)

    rel_var = max(relative_norms) - min(relative_norms)

    check("Every staircase-rescaled Z3 block remains a charge-minus-two pairing operator", max(charge_errors) < 1e-10,
          f"max charge error={max(charge_errors):.2e}")
    check("Operator norm scales linearly with the rescaling parameter", rel_var < 1e-10,
          f"spread in ||Q||/scale={rel_var:.2e}")

    print()
    print("  Nothing in the current charge classification separates k=7 from k=8.")
    print("  The current exact source stack sees one texture ray with a free scale.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: STAIRCASE-BLINDNESS THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  Once the one-generation source ray and the Z3 texture class are fixed,")
    print("  does the current exact Majorana source stack also fix the absolute")
    print("  staircase level?")

    test_local_ray_is_scale_homogeneous()
    test_z3_texture_class_is_scale_homogeneous()
    test_charge_sector_is_identical_across_staircase_levels()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. The current exact Majorana source stack is homogeneous under")
    print("  positive rescaling. It fixes the one-generation source ray and the")
    print("  three-generation Z3 texture class, but not the absolute staircase")
    print("  anchor.")
    print()
    print("  So the live DM blocker is now even narrower: an exact scale-setting")
    print("  / staircase-selection principle for the already-fixed Majorana source")
    print("  class.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
