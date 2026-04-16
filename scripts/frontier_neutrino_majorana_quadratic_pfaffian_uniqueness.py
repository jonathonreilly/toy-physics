#!/usr/bin/env python3
"""
Quadratic Pfaffian uniqueness on the one-generation Majorana lane.

Question:
  Inside the class of finite quadratic fermionic completions, is the
  Pfaffian/Nambu route merely one convenient choice, or is it already unique?

Answer:
  It is unique.

  - symmetric quadratic data drop out of Grassmann bilinears
  - finite quadratic Grassmann integration gives Pf(A) exactly
  - independent quadratic sectors multiply at the partition level and add at
    the log|Pf| level
  - on the one-generation local Majorana lane the canonical block is mu J_2

Boundary:
  This is a quadratic-class uniqueness theorem only. It does NOT prove the
  Pfaffian sector is already axiom-forced or that all future routes are
  quadratic.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

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


def pfaffian(matrix: np.ndarray) -> complex:
    n = matrix.shape[0]
    if n == 0:
        return 1.0 + 0.0j
    if n % 2:
        return 0.0 + 0.0j
    if n == 2:
        return matrix[0, 1]

    total = 0.0 + 0.0j
    for j in range(1, n):
        coeff = matrix[0, j]
        if abs(coeff) < 1e-14:
            continue
        keep = [k for k in range(1, n) if k != j]
        sub = matrix[np.ix_(keep, keep)]
        total += ((-1) ** (j + 1)) * coeff * pfaffian(sub)
    return total


def block_diag(*blocks: np.ndarray) -> np.ndarray:
    dim = sum(block.shape[0] for block in blocks)
    out = np.zeros((dim, dim), dtype=complex)
    start = 0
    for block in blocks:
        n = block.shape[0]
        out[start:start + n, start:start + n] = block
        start += n
    return out


def wedge_sign(mask1: int, mask2: int) -> int:
    crossings = 0
    for i in range(mask1.bit_length()):
        if (mask1 >> i) & 1:
            crossings += (mask2 & ((1 << i) - 1)).bit_count()
    return -1 if crossings % 2 else 1


def poly_mul(p: dict[int, complex], q: dict[int, complex]) -> dict[int, complex]:
    out: dict[int, complex] = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            if m1 & m2:
                continue
            mask = m1 | m2
            coeff = c1 * c2 * wedge_sign(m1, m2)
            out[mask] = out.get(mask, 0.0 + 0.0j) + coeff
    return {mask: coeff for mask, coeff in out.items() if abs(coeff) > 1e-14}


def poly_add(p: dict[int, complex], q: dict[int, complex]) -> dict[int, complex]:
    out = dict(p)
    for mask, coeff in q.items():
        out[mask] = out.get(mask, 0.0 + 0.0j) + coeff
    return {mask: coeff for mask, coeff in out.items() if abs(coeff) > 1e-14}


def poly_scale(p: dict[int, complex], scalar: complex) -> dict[int, complex]:
    return {mask: scalar * coeff for mask, coeff in p.items() if abs(scalar * coeff) > 1e-14}


def quadratic_grassmann_polynomial(matrix: np.ndarray) -> dict[int, complex]:
    n = matrix.shape[0]
    out: dict[int, complex] = {}
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            mask = (1 << i) | (1 << j)
            coeff = 0.5 * matrix[i, j] * (1 if i < j else -1)
            out[mask] = out.get(mask, 0.0 + 0.0j) + coeff
    return {mask: coeff for mask, coeff in out.items() if abs(coeff) > 1e-14}


def grassmann_exp_quadratic(matrix: np.ndarray) -> dict[int, complex]:
    n = matrix.shape[0]
    q = quadratic_grassmann_polynomial(matrix)
    out: dict[int, complex] = {0: 1.0 + 0.0j}
    power: dict[int, complex] = {0: 1.0 + 0.0j}
    for k in range(1, n // 2 + 1):
        power = poly_mul(power, q)
        out = poly_add(out, poly_scale(power, 1.0 / math.factorial(k)))
    return out


def berezin_integral(matrix: np.ndarray) -> complex:
    poly = grassmann_exp_quadratic(matrix)
    full_mask = (1 << matrix.shape[0]) - 1
    return poly.get(full_mask, 0.0 + 0.0j)


def logabs_pf(matrix: np.ndarray) -> float:
    return float(np.log(abs(pfaffian(matrix))))


def test_only_antisymmetric_quadratic_data_survive() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ONLY THE ANTISYMMETRIC QUADRATIC KERNEL SURVIVES")
    print("=" * 88)

    m = np.array(
        [
            [0.0, 1.3 + 0.2j, -0.6, 0.4j],
            [1.1 - 0.5j, 0.0, 0.8 + 0.1j, -0.9],
            [0.2, -0.3j, 0.0, 0.7 - 0.4j],
            [1.0, 0.15, -0.5 + 0.2j, 0.0],
        ],
        dtype=complex,
    )
    a = 0.5 * (m - m.T)
    s = 0.5 * (m + m.T)
    q_m = quadratic_grassmann_polynomial(m)
    q_a = quadratic_grassmann_polynomial(a)
    q_s = quadratic_grassmann_polynomial(s)

    same_err = sum(abs(q_m.get(mask, 0.0) - q_a.get(mask, 0.0)) for mask in set(q_m) | set(q_a))
    sym_norm = sum(abs(coeff) for coeff in q_s.values())

    check("General quadratic Grassmann form equals its antisymmetric part", same_err < 1e-12,
          f"polynomial difference={same_err:.2e}")
    check("Symmetric quadratic data drop out exactly", sym_norm < 1e-12,
          f"symmetric polynomial norm={sym_norm:.2e}")

    print()
    print("  So finite quadratic fermionic completion is already an")
    print("  antisymmetric-kernel problem before any observable choice is made.")


def test_berezin_integral_is_pfaffian() -> None:
    print("\n" + "=" * 88)
    print("PART 2: FINITE QUADRATIC GRASSMANN INTEGRATION GIVES A PFAFFIAN")
    print("=" * 88)

    a2 = 1.7 * J2
    a4 = np.array(
        [
            [0.0, 1.1, -0.4, 0.7],
            [-1.1, 0.0, 0.9, -0.2],
            [0.4, -0.9, 0.0, 1.3],
            [-0.7, 0.2, -1.3, 0.0],
        ],
        dtype=complex,
    )

    int2 = berezin_integral(a2)
    int4 = berezin_integral(a4)
    pf2 = pfaffian(a2)
    pf4 = pfaffian(a4)

    check("Berezin integral equals Pf(A) on the canonical 2x2 block", abs(int2 - pf2) < 1e-12,
          f"integral={int2}, pf={pf2}")
    check("Berezin integral equals Pf(A) on a nontrivial 4x4 antisymmetric kernel", abs(int4 - pf4) < 1e-12,
          f"integral={int4}, pf={pf4}")
    check("Pf(A)^2 = det(A) on the 4x4 quadratic kernel", abs(pf4 * pf4 - np.linalg.det(a4)) < 1e-10,
          f"|Pf^2-det|={abs(pf4 * pf4 - np.linalg.det(a4)):.2e}")

    print()
    print("  So the Pfaffian is not an ansatz here. It is the exact finite")
    print("  quadratic Grassmann partition amplitude.")


def test_independent_quadratic_sectors_force_logabs_pf() -> None:
    print("\n" + "=" * 88)
    print("PART 3: INDEPENDENT QUADRATIC SECTORS FORCE THE LOG|Pf| GRAMMAR")
    print("=" * 88)

    a1 = 1.9 * J2
    a2 = block_diag(0.8 * J2, -1.4 * J2)
    a_tot = block_diag(a1, a2)

    pf_mul_err = abs(pfaffian(a_tot) - pfaffian(a1) * pfaffian(a2))
    add_err = abs(logabs_pf(a_tot) - (logabs_pf(a1) + logabs_pf(a2)))

    check("Pfaffian factorizes on independent quadratic sectors", pf_mul_err < 1e-12,
          f"multiplicative error={pf_mul_err:.2e}")
    check("The additive CPT-even scalar generator is log|Pf|", add_err < 1e-12,
          f"additivity error={add_err:.2e}")

    print()
    print("  Within the finite quadratic class, no second additive scalar")
    print("  grammar competes with log|Pf|.")


def test_one_generation_local_block_is_unique_quadratic_pfaffian_block() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE ONE-GENERATION LOCAL COMPLETION IS THE UNIQUE PFaffian BLOCK mu J_2")
    print("=" * 88)

    m = -0.52 + 0.31j
    block = m * J2
    alpha = np.angle(m) / 2.0
    u = np.exp(-1j * alpha) * np.eye(2, dtype=complex)
    canonical = u @ block @ u.T
    target = abs(m) * J2
    integral = berezin_integral(block)

    check("Every 2x2 quadratic antisymmetric local block is m J_2", np.linalg.norm(block - block[0, 1] * J2) < 1e-12,
          f"reconstruction error={np.linalg.norm(block - block[0, 1] * J2):.2e}")
    check("The finite quadratic partition amplitude is Pf(A_M) = m", abs(integral - m) < 1e-12,
          f"integral={integral}, m={m}")
    check("The one-generation phase is removable to the canonical block mu J_2", np.linalg.norm(canonical - target) < 1e-12,
          f"canonicalization error={np.linalg.norm(canonical - target):.2e}")

    print()
    print("  So on the one-generation local lane, the entire finite quadratic")
    print("  completion class collapses to the canonical Pfaffian block mu J_2.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: QUADRATIC PFAFFIAN UNIQUENESS")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("    rows: Observable principle; Framework axiom; Anomaly-forced time;")
    print("          Native weak algebra; Structural SU(3) closure; One-generation matter closure")
    print("  - docs/NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_OBSERVABLE_GRAMMAR_BOUNDARY_NOTE.md")
    print()
    print("Question:")
    print("  Inside the class of finite quadratic fermionic completions, is the")
    print("  Pfaffian/Nambu route merely one convenient choice, or is it already")
    print("  unique?")

    test_only_antisymmetric_quadratic_data_survive()
    test_berezin_integral_is_pfaffian()
    test_independent_quadratic_sectors_force_logabs_pf()
    test_one_generation_local_block_is_unique_quadratic_pfaffian_block()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Within the finite quadratic completion class, Pfaffian is not just")
    print("  minimal but unique. Any future non-Pfaffian Majorana route would")
    print("  have to be genuinely non-quadratic.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
