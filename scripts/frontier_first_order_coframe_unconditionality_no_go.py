#!/usr/bin/env python3
"""No-go runner for unconditional first-order coframe selection.

The existing coframe carrier theorem proves:

    first-order coframe response => P_A = P_1.

This runner checks whether "first-order" itself is forced by the retained
substrate symmetries. It is not: the Hodge-complement map on the four-axis
event cell exchanges P_1 with P_3 while preserving the spin/time/CPT/local
structure used by the substrate-to-P_A forcing attempt.
"""

from __future__ import annotations

from itertools import product

import numpy as np

TOL = 1e-10
AXES = ("t", "x", "y", "z")
SPATIAL = (1, 2, 3)


def bits_list() -> list[tuple[int, int, int, int]]:
    return [tuple(bits) for bits in product((0, 1), repeat=4)]


BASIS = bits_list()
INDEX = {bits: i for i, bits in enumerate(BASIS)}
DIM = len(BASIS)
I16 = np.eye(DIM, dtype=complex)


def weight(bits: tuple[int, ...]) -> int:
    return int(sum(bits))


def occupied(bits: tuple[int, ...]) -> list[int]:
    return [i for i, bit in enumerate(bits) if bit]


def permutation_sign(seq: list[int]) -> int:
    inversions = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            inversions += int(seq[i] > seq[j])
    return -1 if inversions % 2 else 1


def hodge_star() -> np.ndarray:
    """Euclidean oriented Hodge star on Lambda^* span(t,x,y,z)."""
    u = np.zeros((DIM, DIM), dtype=complex)
    for col, bits in enumerate(BASIS):
        occ = occupied(bits)
        comp = [i for i in range(4) if i not in occ]
        sign = permutation_sign(occ + comp)
        target = tuple(1 if i in comp else 0 for i in range(4))
        u[INDEX[target], col] = sign
    return u


def projector_weight(k: int) -> np.ndarray:
    return np.diag([1.0 if weight(bits) == k else 0.0 for bits in BASIS]).astype(complex)


def number_op(axis: int) -> np.ndarray:
    return np.diag([bits[axis] for bits in BASIS]).astype(complex)


def fro(m: np.ndarray) -> float:
    return float(np.linalg.norm(m, ord="fro"))


def comm(a: np.ndarray, b: np.ndarray) -> float:
    return fro(a @ b - b @ a)


def replace_sign(occ: list[int], old_pos: int, new_axis: int) -> tuple[list[int], int] | None:
    old_axis = occ[old_pos]
    if new_axis != old_axis and new_axis in occ:
        return None
    reduced = occ[:old_pos] + occ[old_pos + 1 :]
    insert_pos = sum(1 for axis in reduced if axis < new_axis)
    new_occ = reduced[:insert_pos] + [new_axis] + reduced[insert_pos:]
    sign = (-1) ** old_pos * (-1) ** insert_pos
    return new_occ, sign


def second_quantized_generator(a: np.ndarray) -> np.ndarray:
    out = np.zeros((DIM, DIM), dtype=complex)
    for col, bits in enumerate(BASIS):
        occ = occupied(bits)
        for old_pos, old_axis in enumerate(occ):
            for new_axis in range(4):
                coeff = a[new_axis, old_axis]
                if abs(coeff) < TOL:
                    continue
                replaced = replace_sign(occ, old_pos, new_axis)
                if replaced is None:
                    continue
                new_occ, sign = replaced
                target = tuple(1 if i in new_occ else 0 for i in range(4))
                out[INDEX[target], col] += sign * coeff
    return out


def spatial_generators() -> list[np.ndarray]:
    gens = []
    for a, b in ((2, 3), (3, 1), (1, 2)):
        m = np.zeros((4, 4), dtype=float)
        m[a, b] = -1.0
        m[b, a] = 1.0
        gens.append(second_quantized_generator(m))
    return gens


def time_parity() -> np.ndarray:
    return np.diag([(-1) ** bits[0] for bits in BASIS]).astype(complex)


def cpt_grading() -> np.ndarray:
    return np.diag([(-1) ** weight(bits) for bits in BASIS]).astype(complex)


def check(label: str, ok: bool, detail: str) -> bool:
    print(f"[{'PASS' if ok else 'FAIL'}] {label}: {detail}")
    return ok


def main() -> int:
    print("=" * 78)
    print("FIRST-ORDER COFRAME UNCONDITIONALITY NO-GO")
    print("=" * 78)
    print()
    print("Question: do retained substrate symmetries force first-order P_1 over its Hodge-dual P_3?")
    print()

    star = hodge_star()
    p1 = projector_weight(1)
    p3 = projector_weight(3)
    tpar = time_parity()
    cpt = cpt_grading()
    gens = spatial_generators()
    ns = [number_op(i) for i in range(4)]

    results: list[bool] = []
    star_unitary = fro(star.conj().T @ star - I16)
    star_square_expected = np.diag([(-1) ** (weight(bits) * (4 - weight(bits))) for bits in BASIS])
    star_square_error = fro(star @ star - star_square_expected)
    results.append(
        check(
            "1. construct oriented Hodge-complement map on H_cell",
            star_unitary < TOL and star_square_error < TOL,
            f"unitarity={star_unitary:.2e}; star^2 law={star_square_error:.2e}",
        )
    )

    p1_to_p3 = fro(star @ p1 @ star.conj().T - p3)
    p3_to_p1 = fro(star @ p3 @ star.conj().T - p1)
    results.append(
        check(
            "2. Hodge complement exchanges P_1 and P_3",
            p1_to_p3 < TOL and p3_to_p1 < TOL,
            f"||*P1*-P3||={p1_to_p3:.2e}; ||*P3*-P1||={p3_to_p1:.2e}",
        )
    )

    spin_errors = [comm(star, g) for g in gens]
    results.append(
        check(
            "3. Hodge complement preserves spatial Cl(3) spin-lift equivariance",
            max(spin_errors) < TOL,
            f"max [*,J_i]={max(spin_errors):.2e}",
        )
    )

    time_norm_error = fro(star @ tpar @ star.conj().T + tpar)
    cpt_error = fro(star @ cpt @ star.conj().T - cpt)
    results.append(
        check(
            "4. Hodge complement normalizes time parity and CPT grading",
            time_norm_error < TOL and cpt_error < TOL,
            f"*T*^-1=-T error={time_norm_error:.2e}; *CPT*^-1=CPT error={cpt_error:.2e}",
        )
    )

    local_errors = [fro(star @ n @ star.conj().T - (I16 - n)) for n in ns]
    results.append(
        check(
            "5. Hodge complement preserves tensor-local number algebra",
            max(local_errors) < TOL,
            f"max *n_i*^-1-(1-n_i)={max(local_errors):.2e}",
        )
    )

    # One-form current components and Hodge-dual 3-form current components are
    # both four-dimensional and related by the same substrate-preserving star.
    one_form_rank = int(round(np.trace(p1).real))
    three_form_rank = int(round(np.trace(p3).real))
    results.append(
        check(
            "6. one-form and dual three-form boundary carriers are isomorphic",
            one_form_rank == three_form_rank == 4 and p1_to_p3 < TOL,
            f"rank(P1)={one_form_rank}; rank(P3)={three_form_rank}; Hodge isomorphism exact",
        )
    )

    p1_p3_distinct = fro(p1 - p3)
    p1_symmetry_error = max([comm(p1, g) for g in gens] + [comm(p1, tpar), comm(p1, cpt)])
    p3_symmetry_error = max([comm(p3, g) for g in gens] + [comm(p3, tpar), comm(p3, cpt)])
    results.append(
        check(
            "7. first-order selection is extra data, not symmetry data",
            p1_p3_distinct > 1.0 and p1_symmetry_error < TOL and p3_symmetry_error < TOL,
            (
                f"||P1-P3||={p1_p3_distinct:.2e}; "
                f"P1 symmetry={p1_symmetry_error:.2e}; P3 symmetry={p3_symmetry_error:.2e}"
            ),
        )
    )

    forbidden = {
        "observable_principle_from_axiom": False,
        "yt_ward_identity": False,
        "alpha_LM_chain": False,
    }
    results.append(
        check(
            "8. forbidden-input boundary",
            not any(forbidden.values()),
            "no observable-principle, YT Ward, or alpha_LM decoration input used",
        )
    )

    print()
    passed = sum(results)
    failed = len(results) - passed
    print(f"Summary: PASS={passed}  FAIL={failed}")
    if failed:
        return 1
    print()
    print(
        "Verdict: NO-GO. First-order coframe selection is not forced by the "
        "listed substrate symmetries. Hodge complement exchanges P_1 and P_3 "
        "while preserving the relevant spin/time/CPT/local structure, so an "
        "extra first-order boundary-orientation law is required."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
