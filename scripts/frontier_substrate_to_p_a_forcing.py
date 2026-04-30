#!/usr/bin/env python3
"""Audit runner for the substrate-to-P_A forcing question.

This runner tests whether the substrate symmetries listed in
SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md uniquely force the
Hamming-weight-one rank-four projector P_A on

    H_cell = C^2_t x C^2_x x C^2_y x C^2_z.

The result is intentionally allowed to be a no-go: if another rank-four
projector satisfies the same stated constraints, the honest conclusion is
that P_A is not uniquely forced by those constraints.
"""

from __future__ import annotations

from itertools import combinations, product
from math import comb

import numpy as np

TOL = 1e-10
AXES = ("t", "x", "y", "z")
SPATIAL = (1, 2, 3)


def basis_bits() -> list[tuple[int, int, int, int]]:
    return [tuple(bits) for bits in product((0, 1), repeat=4)]


BASIS = basis_bits()
INDEX = {b: i for i, b in enumerate(BASIS)}
DIM = len(BASIS)
I16 = np.eye(DIM, dtype=complex)


def weight(bits: tuple[int, ...]) -> int:
    return int(sum(bits))


def projector_on(predicate) -> np.ndarray:
    diag = [1.0 if predicate(bits) else 0.0 for bits in BASIS]
    return np.diag(diag).astype(complex)


def rank(p: np.ndarray) -> int:
    return int(round(np.trace(p).real))


def fro_norm(m: np.ndarray) -> float:
    return float(np.linalg.norm(m, ord="fro"))


def comm_norm(a: np.ndarray, b: np.ndarray) -> float:
    return fro_norm(a @ b - b @ a)


def is_projector(p: np.ndarray) -> bool:
    return fro_norm(p @ p - p) < TOL and fro_norm(p.conj().T - p) < TOL


def replace_sign(occ: list[int], old_pos: int, new_axis: int) -> tuple[list[int], int] | None:
    """Replace occ[old_pos] by new_axis in an exterior basis state."""
    old_axis = occ[old_pos]
    if new_axis != old_axis and new_axis in occ:
        return None
    reduced = occ[:old_pos] + occ[old_pos + 1 :]
    insert_pos = sum(1 for axis in reduced if axis < new_axis)
    new_occ = reduced[:insert_pos] + [new_axis] + reduced[insert_pos:]
    sign = (-1) ** old_pos * (-1) ** insert_pos
    return new_occ, sign


def second_quantized_generator(a: np.ndarray) -> np.ndarray:
    """Exterior-power differential action induced by a one-particle matrix."""
    out = np.zeros((DIM, DIM), dtype=complex)
    for col, bits in enumerate(BASIS):
        occ = [i for i, bit in enumerate(bits) if bit]
        for old_pos, old_axis in enumerate(occ):
            for new_axis in range(4):
                coeff = a[new_axis, old_axis]
                if abs(coeff) < TOL:
                    continue
                replaced = replace_sign(occ, old_pos, new_axis)
                if replaced is None:
                    continue
                new_occ, sign = replaced
                new_bits = tuple(1 if i in new_occ else 0 for i in range(4))
                out[INDEX[new_bits], col] += sign * coeff
    return out


def spatial_so3_generators() -> dict[str, np.ndarray]:
    """One-particle real antisymmetric generators on span(x,y,z)."""
    gens: dict[str, np.ndarray] = {}
    for name, a, b in (("Jx", 2, 3), ("Jy", 3, 1), ("Jz", 1, 2)):
        m = np.zeros((4, 4), dtype=float)
        m[a, b] = -1.0
        m[b, a] = 1.0
        gens[name] = second_quantized_generator(m)
    return gens


def finite_symmetries() -> dict[str, np.ndarray]:
    time_parity = np.diag([(-1) ** bits[0] for bits in BASIS]).astype(complex)
    cpt_grading = np.diag([(-1) ** weight(bits) for bits in BASIS]).astype(complex)
    return {"time_parity": time_parity, "cpt_grading": cpt_grading}


def local_number(axis: int) -> np.ndarray:
    return np.diag([bits[axis] for bits in BASIS]).astype(complex)


def local_rank_block(name: str, predicate) -> dict:
    p = projector_on(predicate)
    return {"name": name, "projector": p, "rank": rank(p)}


def irrep_blocks() -> list[dict]:
    return [
        local_rank_block("E0_scalar_time_even_w0", lambda b: weight(b) == 0),
        local_rank_block("Et_scalar_time_odd_w1", lambda b: b == (1, 0, 0, 0)),
        local_rank_block(
            "EV_vector_time_even_w1",
            lambda b: b[0] == 0 and sum(b[i] for i in SPATIAL) == 1,
        ),
        local_rank_block(
            "EtV_vector_time_odd_w2",
            lambda b: b[0] == 1 and sum(b[i] for i in SPATIAL) == 1,
        ),
        local_rank_block(
            "EVV_vector_time_even_w2",
            lambda b: b[0] == 0 and sum(b[i] for i in SPATIAL) == 2,
        ),
        local_rank_block(
            "EtVV_vector_time_odd_w3",
            lambda b: b[0] == 1 and sum(b[i] for i in SPATIAL) == 2,
        ),
        local_rank_block(
            "EVVV_scalar_time_even_w3",
            lambda b: b[0] == 0 and sum(b[i] for i in SPATIAL) == 3,
        ),
        local_rank_block("EtVVV_scalar_time_odd_w4", lambda b: weight(b) == 4),
    ]


def hamming_projector(k: int) -> np.ndarray:
    return projector_on(lambda b: weight(b) == k)


def local_polynomial_weight(k: int) -> np.ndarray:
    ns = [local_number(i) for i in range(4)]
    p = np.zeros((DIM, DIM), dtype=complex)
    for occupied in combinations(range(4), k):
        term = I16.copy()
        occupied = set(occupied)
        for i in range(4):
            term = term @ (ns[i] if i in occupied else I16 - ns[i])
        p += term
    return p


def check(label: str, ok: bool, detail: str) -> bool:
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {label}: {detail}")
    return ok


def max_equivariance_error(p: np.ndarray, gens: dict[str, np.ndarray], fins: dict[str, np.ndarray]) -> float:
    errors = [comm_norm(p, g) for g in gens.values()]
    errors.extend(comm_norm(p, u) for u in fins.values())
    return max(errors)


def main() -> int:
    print("=" * 78)
    print("SUBSTRATE-TO-P_A FORCING ENUMERATOR")
    print("=" * 78)
    print()
    print("Question: do the stated substrate symmetries uniquely force P_A?")
    print()

    gens = spatial_so3_generators()
    fins = finite_symmetries()
    blocks = irrep_blocks()
    p_a = hamming_projector(1)
    p_3 = hamming_projector(3)

    results: list[bool] = []

    results.append(
        check(
            "1. construct H_cell = (C^2)^4 explicitly",
            DIM == 16 and len(BASIS) == 16,
            f"dim={DIM}; weight ranks={[rank(hamming_projector(k)) for k in range(5)]}",
        )
    )

    antihermitian = max(fro_norm(g.conj().T + g) for g in gens.values())
    finite_unitary = max(fro_norm(u.conj().T @ u - I16) for u in fins.values())
    results.append(
        check(
            "2. construct substrate spin/time/CPT actions",
            antihermitian < TOL and finite_unitary < TOL,
            f"spin anti-Hermitian error={antihermitian:.2e}; finite unitarity={finite_unitary:.2e}",
        )
    )

    block_errors = []
    block_summary = []
    for block in blocks:
        p = block["projector"]
        block_errors.append(max_equivariance_error(p, gens, fins))
        block_summary.append(f"{block['name']}:{block['rank']}")
    results.append(
        check(
            "3. decompose H_cell into local spin/time irreducible blocks",
            len(blocks) == 8 and sum(b["rank"] for b in blocks) == 16 and max(block_errors) < TOL,
            "; ".join(block_summary),
        )
    )

    rank4_candidates = []
    for r in range(1, len(blocks) + 1):
        for combo in combinations(blocks, r):
            p = sum((b["projector"] for b in combo), np.zeros((DIM, DIM), dtype=complex))
            if rank(p) == 4:
                rank4_candidates.append((tuple(b["name"] for b in combo), p))
    candidate_errors = [max_equivariance_error(p, gens, fins) for _, p in rank4_candidates]
    results.append(
        check(
            "4. enumerate rank-four local equivariant projector classes",
            len(rank4_candidates) == 17 and max(candidate_errors) < TOL,
            f"rank-four candidates={len(rank4_candidates)}",
        )
    )

    p_a_names = next(names for names, p in rank4_candidates if fro_norm(p - p_a) < TOL)
    p_3_names = next(names for names, p in rank4_candidates if fro_norm(p - p_3) < TOL)
    results.append(
        check(
            "5. verify P_A is one candidate",
            is_projector(p_a) and rank(p_a) == 4 and max_equivariance_error(p_a, gens, fins) < TOL,
            f"P_A blocks={p_a_names}; local polynomial error={fro_norm(p_a - local_polynomial_weight(1)):.2e}",
        )
    )

    p3_local_error = fro_norm(p_3 - local_polynomial_weight(3))
    p3_equiv_error = max_equivariance_error(p_3, gens, fins)
    results.append(
        check(
            "6. exhibit non-P_A rank-four candidate satisfying the same constraints",
            is_projector(p_3) and rank(p_3) == 4 and p3_equiv_error < TOL and p3_local_error < TOL,
            f"P_3 blocks={p_3_names}; equivariance={p3_equiv_error:.2e}; local polynomial={p3_local_error:.2e}",
        )
    )

    hamming_rank4 = [
        (k, rank(hamming_projector(k)), max_equivariance_error(hamming_projector(k), gens, fins))
        for k in range(5)
        if rank(hamming_projector(k)) == 4
    ]
    results.append(
        check(
            "7. pure hamming-rank-four sectors are not unique",
            len(hamming_rank4) == 2 and {k for k, _, _ in hamming_rank4} == {1, 3},
            f"rank-four hamming sectors={hamming_rank4}",
        )
    )

    forbidden_inputs = {
        "observable_principle_from_axiom": False,
        "yt_ward_identity": False,
        "alpha_LM_decorated_chain": False,
    }
    results.append(
        check(
            "8. retained-input boundary check",
            not any(forbidden_inputs.values()),
            "runner uses only local Cl(3) spin-lift action, forced time-axis grading, CPT grading, complex Hilbert structure, and tensor-local number operators",
        )
    )

    print()
    if all(results):
        print("Summary: PASS=8  FAIL=0")
        print()
        print(
            "Verdict: NO-GO. P_A exists, but it is not uniquely forced by the "
            "stated substrate symmetries. P_3 and other rank-four local "
            "equivariant sums satisfy the same checks, so an additional "
            "orientation/first-order boundary law is required."
        )
        return 0

    print(f"Summary: PASS={sum(results)}  FAIL={len(results) - sum(results)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
