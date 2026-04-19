#!/usr/bin/env python3
"""
Local nilpotent reduction on the one-generation Majorana lane.

Question:
  Could a future local nonlinear fermionic charge-2 primitive on the
  one-generation lane arise as a higher polynomial in the unique local seed?

Answer:
  No.

  The unique one-generation local seed S_unique is Grassmann-nilpotent, so
  S_unique^2 = 0. Any local polynomial in S_unique truncates to a0 + a1 S.
  Requiring fermion-number charge -2 removes the constant term, leaving only
  a linear seed direction.

Boundary:
  This is a one-generation local-polynomial reduction theorem only. It does
  NOT rule out nonlocal, multi-generation, or spectator-coupled extensions.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


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


def number_operator(cs: list[np.ndarray]) -> np.ndarray:
    dim = cs[0].shape[0]
    out = np.zeros((dim, dim), dtype=complex)
    for c in cs:
        out += c.conj().T @ c
    return out


def test_seed_is_nilpotent() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: THE UNIQUE LOCAL CHARGE-TWO SEED IS NILPOTENT")
    print("=" * 88)

    cs = annihilation_operators(2)
    s_unique = cs[0] @ cs[1]
    square = s_unique @ s_unique
    cube = square @ s_unique
    rank = np.linalg.matrix_rank(s_unique, tol=1e-10)

    check("The canonical local charge-two seed is nonzero", np.linalg.norm(s_unique) > 1e-12,
          f"norm={np.linalg.norm(s_unique):.2e}")
    check("The seed squares to zero exactly", np.linalg.norm(square) < 1e-12,
          f"||S^2||={np.linalg.norm(square):.2e}")
    check("Higher local powers also vanish", np.linalg.norm(cube) < 1e-12,
          f"||S^3||={np.linalg.norm(cube):.2e}")
    check("The seed still has nontrivial rank before nilpotency kills higher powers", rank == 1,
          f"rank={rank}")

    print()
    print("  So the one-generation local fermionic seed is real and nontrivial,")
    print("  but it cannot support a higher local power tower.")
    return s_unique


def test_polynomial_truncation() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ANY LOCAL POLYNOMIAL TRUNCATES TO a0 + a1 S_unique")
    print("=" * 88)

    cs = annihilation_operators(2)
    s_unique = cs[0] @ cs[1]

    a0 = 1.2 - 0.3j
    a1 = -0.7 + 0.4j
    a2 = 2.1 - 0.8j
    a3 = -1.4 + 0.6j

    polynomial = a0 * np.eye(s_unique.shape[0], dtype=complex) + a1 * s_unique + a2 * (s_unique @ s_unique) + a3 * (s_unique @ s_unique @ s_unique)
    reduced = a0 * np.eye(s_unique.shape[0], dtype=complex) + a1 * s_unique

    check("Higher local polynomial terms vanish exactly", np.linalg.norm(polynomial - reduced) < 1e-12,
          f"reduction error={np.linalg.norm(polynomial - reduced):.2e}")

    print()
    print("  Local polynomial dependence on the one-generation seed stops after")
    print("  first order. There is no genuinely nonlinear local fermionic tower.")


def test_charge_minus_two_projection_keeps_only_linear_seed() -> None:
    print("\n" + "=" * 88)
    print("PART 3: A LOCAL CHARGE-MINUS-TWO PRIMITIVE KEEPS ONLY THE LINEAR TERM")
    print("=" * 88)

    cs = annihilation_operators(2)
    n_tot = number_operator(cs)
    s_unique = cs[0] @ cs[1]
    identity = np.eye(s_unique.shape[0], dtype=complex)

    a0 = 0.9
    a1 = -0.55 + 0.2j
    candidate = a0 * identity + a1 * s_unique

    comm_identity = np.linalg.norm(n_tot @ identity - identity @ n_tot)
    comm_seed = np.linalg.norm((n_tot @ s_unique - s_unique @ n_tot) + 2.0 * s_unique)
    overlap_constant = np.trace(s_unique.conj().T @ identity)
    overlap_seed = np.trace(s_unique.conj().T @ s_unique)
    overlap_candidate = np.trace(s_unique.conj().T @ candidate)

    check("The constant term is charge-zero, not charge-minus-two", comm_identity < 1e-12 and abs(overlap_constant) < 1e-12,
          f"comm={comm_identity:.2e}, overlap={overlap_constant}")
    check("The seed has charge minus two exactly", comm_seed < 1e-12,
          f"||[N,S]+2S||={comm_seed:.2e}")
    check("Only the linear seed term contributes to the local charge-minus-two probe", abs(overlap_candidate - a1 * overlap_seed) < 1e-12,
          f"projection error={abs(overlap_candidate - a1 * overlap_seed):.2e}")

    print()
    print("  So once charge-minus-two is required, the local primitive collapses")
    print("  exactly to one linear seed direction.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: LOCAL NILPOTENT REDUCTION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("    rows: Framework axiom; Anomaly-forced time; Native weak algebra;")
    print("          Structural SU(3) closure; One-generation matter closure")
    print("  - docs/NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_QUADRATIC_PFAFFIAN_UNIQUENESS_NOTE.md")
    print()
    print("Question:")
    print("  Could a future one-generation local nonlinear fermionic charge-two")
    print("  primitive arise as a higher polynomial in the unique local seed?")

    test_seed_is_nilpotent()
    test_polynomial_truncation()
    test_charge_minus_two_projection_keeps_only_linear_seed()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. On the one-generation local lane, the unique charge-two seed is")
    print("  nilpotent, so every local fermionic charge-two polynomial primitive")
    print("  reduces exactly to one linear seed direction.")
    print()
    print("  Any future alternative route must therefore come from nonlocal,")
    print("  multi-generation, or spectator-coupled structure rather than a")
    print("  higher local fermionic polynomial in S_unique.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
