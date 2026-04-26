#!/usr/bin/env python3
"""
Planck Target 3 relaxed-wu support audit.

This lands the useful algebra from origin/claude/relaxed-wu-a56584 as
support-grade science only. It intentionally does not promote the Planck pin
to a minimal-stack retained closure.
"""

from __future__ import annotations

import itertools
import math
import re
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0
TOL = 1.0e-10


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}")
    if detail:
        print(f"       {detail}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    return condition


def read_doc(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return re.sub(r"[\s*`]+", " ", text.lower())


def has_all(text: str, phrases: tuple[str, ...]) -> bool:
    haystack = normalized(text)
    return all(phrase.lower() in haystack for phrase in phrases)


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_all(*ops: np.ndarray) -> np.ndarray:
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def jw_cl4() -> list[np.ndarray]:
    return [
        kron_all(X, I2, I2, I2),
        kron_all(Z, X, I2, I2),
        kron_all(Z, Z, X, I2),
        kron_all(Z, Z, Z, X),
    ]


def hamming_indices(weight: int) -> list[int]:
    return [idx for idx in range(16) if idx.bit_count() == weight]


def creation_operator(mode: int) -> np.ndarray:
    op = np.zeros((16, 16), dtype=complex)
    for idx in range(16):
        if (idx >> mode) & 1:
            continue
        lower_occupied = sum((idx >> j) & 1 for j in range(mode))
        sign = -1 if lower_occupied % 2 else 1
        out = idx | (1 << mode)
        op[out, idx] = sign
    return op


def projector(indices: list[int]) -> np.ndarray:
    p = np.zeros((16, 16), dtype=complex)
    for idx in indices:
        p[idx, idx] = 1.0
    return p


def bit_permutation_matrix(sigma: tuple[int, int, int, int]) -> np.ndarray:
    mat = np.zeros((16, 16), dtype=complex)
    for idx in range(16):
        out = 0
        for old_axis in range(4):
            if (idx >> old_axis) & 1:
                out |= 1 << sigma[old_axis]
        mat[out, idx] = 1.0
    return mat


def schur_complement(matrix: np.ndarray, keep: list[int]) -> np.ndarray:
    drop = sorted(set(range(matrix.shape[0])) - set(keep))
    a = matrix[np.ix_(keep, keep)]
    f = matrix[np.ix_(drop, drop)]
    b = matrix[np.ix_(keep, drop)]
    c = matrix[np.ix_(drop, keep)]
    return a - b @ np.linalg.inv(f) @ c


def part1_authority_boundary() -> None:
    banner("Part 1: authority boundary")

    status = read_doc("docs/PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md")
    coframe = read_doc("docs/PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md")
    source = read_doc("docs/PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md")
    bridge = read_doc("docs/PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md")
    note = read_doc("docs/PLANCK_TARGET3_RELAXED_WU_SUPPORT_AUDIT_NOTE_2026-04-26.md")

    check(
        "Planck status note keeps the absolute scale as package pin",
        has_all(status, ("a^(-1) = M_Pl", "not yet derived", "open program")),
    )
    check(
        "primitive coframe carrier note is support, not standalone closure",
        has_all(coframe, ("positive support theorem", "not a standalone minimal-stack derivation")),
    )
    check(
        "source-unit normalization remains support on conditional packet",
        has_all(source, ("retained support theorem", "not a standalone minimal-stack closure")),
    )
    check(
        "Clifford phase bridge remains conditional",
        has_all(bridge, ("conditional structural target 3 bridge", "not a standalone retained closure")),
    )
    check(
        "new relaxed-wu note denies minimal-stack closure",
        "PLANCK_PIN_MINIMAL_STACK_CLOSURE=FALSE" in note
        and "P1_OVER_P3_SELECTOR_CLOSED=FALSE" in note,
    )


def part2_car_vacuum_one_tick() -> None:
    banner("Part 2: CAR/vacuum one-tick support")

    vacuum = np.zeros((16,), dtype=complex)
    vacuum[0] = 1.0
    creators = [creation_operator(mode) for mode in range(4)]

    b_one = np.zeros((16, 16), dtype=complex)
    one_tick_states = []
    for cdag in creators:
        state = cdag @ vacuum
        one_tick_states.append(state)
        b_one += np.outer(state, state.conj())

    p1 = projector(hamming_indices(1))
    p3 = projector(hamming_indices(3))
    rho = np.eye(16, dtype=complex) / 16.0

    check(
        "one creation from vacuum spans exactly the HW=1 packet P_1",
        np.linalg.norm(b_one - p1) < TOL,
        f"||B_one-P_1||={np.linalg.norm(b_one - p1):.2e}",
    )
    check(
        "source-free trace of the one-tick carrier is 1/4",
        abs(np.trace(rho @ b_one).real - 0.25) < TOL,
        f"Tr(rho B_one)={np.trace(rho @ b_one).real:.12f}",
    )
    check(
        "P_3 has the same rank and trace, so rank alone cannot select P_1",
        int(round(np.trace(p3).real)) == 4
        and abs(np.trace(rho @ p3).real - 0.25) < TOL,
        f"rank(P_3)={np.trace(p3).real:.0f}, Tr(rho P_3)={np.trace(rho @ p3).real:.12f}",
    )

    # Reaching a representative HW=3 state from the vacuum requires three
    # creation operators; one or two cannot produce HW=3.
    target = np.zeros((16,), dtype=complex)
    target[(1 << 0) | (1 << 1) | (1 << 2)] = 1.0
    one_step_overlap = max(abs(np.vdot(target, state)) for state in one_tick_states)
    two_step_overlap = 0.0
    three_step_overlap = 0.0
    for a, b in itertools.permutations(range(4), 2):
        two_step_overlap = max(two_step_overlap, abs(np.vdot(target, creators[a] @ creators[b] @ vacuum)))
    for a, b, c in itertools.permutations(range(4), 3):
        three_step_overlap = max(three_step_overlap, abs(np.vdot(target, creators[a] @ creators[b] @ creators[c] @ vacuum)))
    check(
        "HW=3 is inaccessible in one or two creations but accessible in three",
        one_step_overlap < TOL and two_step_overlap < TOL and three_step_overlap > 1.0 - TOL,
        f"max overlaps: one={one_step_overlap:.1e}, two={two_step_overlap:.1e}, three={three_step_overlap:.1e}",
    )


def part3_s4_clifford_and_packet_controls() -> None:
    banner("Part 3: S_4 Clifford uniqueness and packet caveat")

    basis_keys: list[tuple[int, ...]] = []
    for r in range(5):
        basis_keys.extend(tuple(combo) for combo in itertools.combinations(range(4), r))

    def sigma_action_on_subset(sigma: tuple[int, ...], subset: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
        axes = [sigma[a] for a in subset]
        sign = 1
        arr = list(axes)
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    arr[i], arr[j] = arr[j], arr[i]
                    sign *= -1
        return tuple(sorted(axes)), sign

    def representation_matrix(sigma: tuple[int, ...]) -> np.ndarray:
        mat = np.zeros((16, 16), dtype=complex)
        for j, subset in enumerate(basis_keys):
            image, sign = sigma_action_on_subset(sigma, subset)
            i = basis_keys.index(image)
            mat[i, j] = sign
        return mat

    s4 = list(itertools.permutations(range(4)))
    sym = sum(representation_matrix(sigma) for sigma in s4) / len(s4)

    total_dim = int(np.linalg.matrix_rank(sym, tol=1.0e-9))
    grade_dims = {}
    for grade in range(5):
        indices = [i for i, subset in enumerate(basis_keys) if len(subset) == grade]
        grade_dims[grade] = int(np.linalg.matrix_rank(sym[np.ix_(indices, indices)], tol=1.0e-9))

    check(
        "abstract signed S_4 invariants in Cl_4 have dimensions {0:1,1:1,2:0,3:0,4:0}",
        total_dim == 2
        and grade_dims == {0: 1, 1: 1, 2: 0, 3: 0, 4: 0},
        f"total={total_dim}, grade_dims={grade_dims}",
    )

    p1 = projector(hamming_indices(1))
    p3 = projector(hamming_indices(3))
    max_p1_comm = 0.0
    max_p3_comm = 0.0
    for sigma in s4:
        perm = bit_permutation_matrix(sigma)
        max_p1_comm = max(max_p1_comm, np.linalg.norm(perm @ p1 @ perm.conj().T - p1))
        max_p3_comm = max(max_p3_comm, np.linalg.norm(perm @ p3 @ perm.conj().T - p3))
    check(
        "both Hamming packets P_1 and P_3 are S_4-symmetric packet candidates",
        max_p1_comm < TOL and max_p3_comm < TOL,
        f"max symmetry errors: P1={max_p1_comm:.2e}, P3={max_p3_comm:.2e}",
    )
    check(
        "therefore S_4 grade-1 uniqueness is a first-order-source result, not a packet selector",
        grade_dims[1] == 1 and max_p3_comm < TOL,
        "P_3 remains symmetric as a packet even though grade-3 Clifford words have no invariant vector",
    )


def part4_cubic_bivector_schur() -> None:
    banner("Part 4: cubic-bivector Schur spectrum")

    gammas = jw_cl4()
    h_biv = sum(1j * gammas[a] @ gammas[b] for a in range(4) for b in range(a + 1, 4))
    check(
        "H_biv is Hermitian",
        np.linalg.norm(h_biv - h_biv.conj().T) < TOL,
        f"Hermitian error={np.linalg.norm(h_biv - h_biv.conj().T):.2e}",
    )

    low = 4.0 * (2.0 - math.sqrt(2.0))
    high = 4.0 * (2.0 + math.sqrt(2.0))
    expected = np.array([-high, -low, low, high])

    spectra = {}
    traces = {}
    for weight in (1, 3):
        keep = hamming_indices(weight)
        schur = schur_complement(h_biv, keep)
        eigs = np.linalg.eigvalsh(schur)
        spectra[weight] = eigs
        traces[weight] = float(np.sum(1.0 / np.abs(eigs)))
        check(
            f"P_{weight} Schur spectrum is +/-4(2 +/- sqrt(2))",
            np.allclose(eigs, expected, atol=1.0e-9),
            f"eigs={np.round(eigs, 10)}",
        )
        check(
            f"Tr(|L_K|^-1)=1 on P_{weight}",
            abs(traces[weight] - 1.0) < TOL,
            f"trace={traces[weight]:.12f}",
        )

    check(
        "P_1 and P_3 Schur spectra are identical, so Schur data do not select P_1",
        np.allclose(spectra[1], spectra[3], atol=1.0e-9),
        "Hodge-dual packet has same control spectrum",
    )


def part5_conditional_wald_match() -> None:
    banner("Part 5: conditional Wald/BH coefficient match")

    c_cell = 0.25
    g_newton_lat = 1.0 / (4.0 * c_cell)
    a_over_l_planck = 1.0 / math.sqrt(g_newton_lat)

    check(
        "if c_cell=1/(4G_lat), then c_cell=1/4 gives G_lat=1",
        abs(g_newton_lat - 1.0) < TOL,
        f"G_lat={g_newton_lat:.12f}",
    )
    check(
        "with conventional l_P^2=G_phys and G_phys=a^2 G_lat, the conditional map gives a/l_P=1",
        abs(a_over_l_planck - 1.0) < TOL,
        f"a/l_P={a_over_l_planck:.12f}",
    )

    note = read_doc("docs/PLANCK_TARGET3_RELAXED_WU_SUPPORT_AUDIT_NOTE_2026-04-26.md")
    check(
        "note marks the Wald/BH match as conditional on carrier and universal physics",
        "BH_WALD_MATCH_CONDITIONAL_ON_CARRIER_AND_UNIVERSAL_PHYSICS=TRUE" in note,
    )
    check(
        "note keeps the Schur trace/source-coupling bridge open",
        "SCHUR_TRACE_SOURCE_COUPLING_IDENTIFICATION_CLOSED=FALSE" in note,
    )


def main() -> int:
    print("Planck Target 3 relaxed-wu support audit")
    print("Status: support/control packet only; no minimal-stack Planck closure.")

    part1_authority_boundary()
    part2_car_vacuum_one_tick()
    part3_s4_clifford_and_packet_controls()
    part4_cubic_bivector_schur()
    part5_conditional_wald_match()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
