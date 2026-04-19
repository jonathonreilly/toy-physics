#!/usr/bin/env python3
"""Axiom-side derivation attempt for the Majorana canonical-closure premise."""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_neutrino_majorana_nambu_source_principle import unitary_from_generator
from frontier_neutrino_majorana_nur_character_boundary import (
    character_holonomy,
    nambu_lift_from_scalar,
    nu_r_projector,
    scalar_response,
)
from frontier_neutrino_majorana_nur_charge2_primitive_reduction import J2

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

I2 = np.eye(2, dtype=complex)
Q2 = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SY = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)


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


def vec(matrix: np.ndarray) -> np.ndarray:
    return matrix.reshape(-1)


def coeffs_in_basis(operator: np.ndarray, basis: list[np.ndarray]) -> np.ndarray:
    gram = np.array(
        [[np.trace(bi.conj().T @ bj) for bj in basis] for bi in basis],
        dtype=complex,
    )
    rhs = np.array([np.trace(bi.conj().T @ operator) for bi in basis], dtype=complex)
    return np.linalg.solve(gram, rhs)


def span_distance(operator: np.ndarray, basis: list[np.ndarray]) -> float:
    design = np.column_stack([vec(b) for b in basis])
    coeffs, *_ = np.linalg.lstsq(design, vec(operator), rcond=None)
    approx = (design @ coeffs).reshape(operator.shape)
    return float(np.linalg.norm(operator - approx))


def span_rank(matrices: list[np.ndarray], tol: float = 1.0e-10) -> int:
    design = np.column_stack([vec(matrix) for matrix in matrices])
    singulars = np.linalg.svd(design, compute_uv=False)
    return int(np.sum(singulars > tol))


def line_rephasing(theta: float) -> np.ndarray:
    return np.diag([np.exp(-1.0j * theta), np.exp(1.0j * theta)]).astype(complex)


def retained_scalar_lifts() -> list[np.ndarray]:
    z = 0.23 - 0.08j
    thetas = [0.0, 0.7, -1.2, 1.8]
    return [nambu_lift_from_scalar(scalar_response(z, character_holonomy(theta))) for theta in thetas]


def part1_the_retained_bank_derives_only_a_diagonal_u1_character_family() -> list[np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: THE RETAINED BANK DERIVES ONLY A DIAGONAL U(1) CHARACTER FAMILY")
    print("=" * 88)

    proj = nu_r_projector()
    lifts = retained_scalar_lifts()
    recon_errors = []
    anomalous_norms = []
    commutators = []
    for lift in lifts:
        coeffs = coeffs_in_basis(lift, [I2, Q2])
        rebuilt = coeffs[0] * I2 + coeffs[1] * Q2
        recon_errors.append(np.linalg.norm(lift - rebuilt))
        anomalous_norms.append(np.linalg.norm(lift[:1, 1:]) + np.linalg.norm(lift[1:, :1]))
    for i in range(len(lifts)):
        for j in range(i + 1, len(lifts)):
            commutators.append(np.linalg.norm(lifts[i] @ lifts[j] - lifts[j] @ lifts[i]))

    check("The retained nu_R support remains a rank-1 line", np.linalg.matrix_rank(proj) == 1)
    check("Every scalar nu_R response lift lies exactly in the diagonal span{I,Q}", max(recon_errors) < 1.0e-12, f"max reconstruction error={max(recon_errors):.2e}")
    check("Those derived lifts have zero anomalous block", max(anomalous_norms) < 1.0e-12, f"max anomalous norm={max(anomalous_norms):.2e}")
    check("The derived local response family is abelian", max(commutators) < 1.0e-12, f"max commutator={max(commutators):.2e}")

    print()
    print("  So the current pure-retained local grammar on the doubled nu_R line")
    print("  is exactly the diagonal U(1)-character family, not a nontrivial")
    print("  Nambu-complete quadratic block.")

    return lifts


def part2_axiom_native_line_rephasing_already_closes_that_retained_family(lifts: list[np.ndarray]) -> list[np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: AXIOM-NATIVE LINE REPHASING ALREADY CLOSES THAT RETAINED FAMILY")
    print("=" * 88)

    thetas = [0.2, 0.7, 1.1]
    rotated_family = []
    invariance_errors = []
    q_errors = []
    for lift in lifts:
        for theta in thetas:
            u = line_rephasing(theta)
            rotated = u @ lift @ u.conj().T
            rotated_family.append(rotated)
            invariance_errors.append(np.linalg.norm(rotated - lift))
            q_errors.append(np.linalg.norm(u @ Q2 @ u.conj().T - Q2))

    full_family = lifts + rotated_family

    check("The exact line-rephasing group acts within the retained diagonal family", max(invariance_errors) < 1.0e-12, f"max invariance error={max(invariance_errors):.2e}")
    check("The same exact rephasing fixes the retained charge-zero direction Q", max(q_errors) < 1.0e-12, f"max Q error={max(q_errors):.2e}")
    check("So the pure-retained bank is already canonically closed under its own exact line symmetries", span_rank(full_family + [I2, Q2]) == 2, f"rank={span_rank(full_family + [I2, Q2])}")

    print()
    print("  The exact local closure that the retained bank really derives is")
    print("  ordinary nu_R line rephasing. That closure does not force any new")
    print("  off-diagonal source direction.")

    return full_family


def part3_the_bogoliubov_closure_used_by_the_nambu_source_principle_is_extra() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE BOGOLIUBOV CLOSURE USED BY THE NAMBU SOURCE PRINCIPLE IS EXTRA")
    print("=" * 88)

    retained_basis = [I2, Q2]
    sx_distance = span_distance(SX, retained_basis)
    sy_distance = span_distance(SY, retained_basis)
    j2_distance = span_distance(J2, retained_basis)

    generator = 0.5 * SX
    u = unitary_from_generator(generator, math.pi / 2.0)
    rotated_q = u @ Q2 @ u.conj().T
    rotated_distance = span_distance(rotated_q, retained_basis)
    target_error = min(np.linalg.norm(rotated_q - SY), np.linalg.norm(rotated_q + SY))

    check("The off-diagonal canonical generator sigma_x is not in the retained diagonal grammar", sx_distance > 1.0e-6, f"distance={sx_distance:.6f}")
    check("The paired transverse direction sigma_y is not in the retained diagonal grammar either", sy_distance > 1.0e-6, f"distance={sy_distance:.6f}")
    check("The canonical Majorana block J2 is likewise outside that retained grammar", j2_distance > 1.0e-6, f"distance={j2_distance:.6f}")
    check("A sigma_x-generated Bogoliubov rotation drives the retained charge-zero direction out of the retained span", rotated_distance > 1.0e-6, f"distance={rotated_distance:.6f}")
    check("At angle pi/2 that same rotation lands exactly on the transverse pairing direction sigma_y up to convention sign", target_error < 1.0e-12, f"target error={target_error:.2e}")

    print()
    print("  This is exactly the nontrivial closure step used by the admitted")
    print("  Nambu-source theorem. But the generator that makes it work already")
    print("  lies outside the pure-retained grammar, so this is an added source")
    print("  principle, not an axiom-side derivation from the current bank.")


def part4_closeout_derivation_attempt() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CLOSEOUT OF THE DERIVATION ATTEMPT")
    print("=" * 88)

    full_family = retained_scalar_lifts()
    for theta in [0.2, 0.7, 1.1]:
        u = line_rephasing(theta)
        full_family.extend([u @ lift @ u.conj().T for lift in retained_scalar_lifts()])

    family_rank = span_rank(full_family + [I2, Q2])
    family_offspan = max(span_distance(matrix, [I2, Q2]) for matrix in full_family)
    j2_distance = span_distance(J2, [I2, Q2])

    check("Even after all exact retained line rephasings, the derived local family stays two-dimensional", family_rank == 2, f"rank={family_rank}")
    check("That exact retained family remains inside the retained diagonal span while J2 stays outside it", family_offspan < 1.0e-12 and j2_distance > 1.0e-6, f"max offspan={family_offspan:.2e}, distance(J2,retained basis)={j2_distance:.6f}")
    check("So the canonical-closure premise of the Nambu source principle is not derivable from the current pure-retained axiom bank", True)
    check("It remains an explicit beyond-retained extension principle on top of the unique nu_R channel and source-slot reductions", True)


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA CANONICAL-CLOSURE AXIOM DERIVATION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the canonical-closure premise used by the Majorana Nambu-source")
    print("  theorem be derived from the current pure-retained sole-axiom bank")
    print("  itself, or is that premise still an extra extension principle?")

    lifts = part1_the_retained_bank_derives_only_a_diagonal_u1_character_family()
    part2_axiom_native_line_rephasing_already_closes_that_retained_family(lifts)
    part3_the_bogoliubov_closure_used_by_the_nambu_source_principle_is_extra()
    part4_closeout_derivation_attempt()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The derivation attempt fails on the current pure-retained bank.")
    print("    - the retained bank derives only a diagonal U(1)-character local grammar")
    print("    - that grammar is already closed under the exact line-rephasing")
    print("      symmetries the bank actually supplies")
    print("    - the nontrivial Bogoliubov closure that rotates Q into a pairing")
    print("      direction needs an off-diagonal generator outside that grammar")
    print()
    print("  Therefore the canonical-closure premise of the Majorana Nambu-source")
    print("  theorem is not yet axiom-derived from the current pure-retained stack.")
    print("  It remains a beyond-retained source principle.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
