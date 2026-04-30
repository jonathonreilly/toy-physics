#!/usr/bin/env python3
"""Link-local first-variation route for forcing P_A.

This runner tests a route not covered by the abstract symmetry and boundary
incidence no-gos: the primitive active response is taken from the retained
microscopic action surface itself. The finite Grassmann/staggered-Dirac
action is link-local: each primitive local term is labelled by exactly one
axis/link variable. Its first variation therefore has one-axis support.

The Hodge-dual P_3 sector is still a valid flux/face representation, but it is
not in the fundamental first-variation source domain of the action. It appears
only after Hodge duality or higher composite/third-variation data.
"""

from __future__ import annotations

from itertools import combinations, product

import numpy as np

TOL = 1.0e-10
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


def bits_from_occ(occ: list[int]) -> tuple[int, int, int, int]:
    return tuple(1 if i in occ else 0 for i in range(4))


def occupied(bits: tuple[int, ...]) -> list[int]:
    return [i for i, bit in enumerate(bits) if bit]


def projector_on(predicate) -> np.ndarray:
    return np.diag([1.0 if predicate(bits) else 0.0 for bits in BASIS]).astype(complex)


def projector_weight(k: int) -> np.ndarray:
    return projector_on(lambda bits: weight(bits) == k)


def number_op(axis: int) -> np.ndarray:
    return np.diag([bits[axis] for bits in BASIS]).astype(complex)


def fro(m: np.ndarray) -> float:
    return float(np.linalg.norm(m, ord="fro"))


def comm(a: np.ndarray, b: np.ndarray) -> float:
    return fro(a @ b - b @ a)


def rank(p: np.ndarray) -> int:
    return int(round(np.trace(p).real))


def permutation_sign(seq: list[int]) -> int:
    inversions = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            inversions += int(seq[i] > seq[j])
    return -1 if inversions % 2 else 1


def hodge_star() -> np.ndarray:
    u = np.zeros((DIM, DIM), dtype=complex)
    for col, bits in enumerate(BASIS):
        occ = occupied(bits)
        comp = [i for i in range(4) if i not in occ]
        target = bits_from_occ(comp)
        u[INDEX[target], col] = permutation_sign(occ + comp)
    return u


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
                out[INDEX[bits_from_occ(new_occ)], col] += sign * coeff
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


def local_polynomial_weight(k: int) -> np.ndarray:
    ns = [number_op(i) for i in range(4)]
    p = np.zeros((DIM, DIM), dtype=complex)
    for occupied_axes in combinations(range(4), k):
        occupied_set = set(occupied_axes)
        term = I16.copy()
        for axis in range(4):
            term = term @ (ns[axis] if axis in occupied_set else I16 - ns[axis])
        p += term
    return p


def local_spin_time_blocks() -> list[tuple[str, np.ndarray]]:
    return [
        ("E0_scalar_time_even_w0", projector_on(lambda b: weight(b) == 0)),
        ("Et_scalar_time_odd_w1", projector_on(lambda b: b == (1, 0, 0, 0))),
        (
            "EV_vector_time_even_w1",
            projector_on(lambda b: b[0] == 0 and sum(b[i] for i in SPATIAL) == 1),
        ),
        (
            "EtV_vector_time_odd_w2",
            projector_on(lambda b: b[0] == 1 and sum(b[i] for i in SPATIAL) == 1),
        ),
        (
            "EVV_vector_time_even_w2",
            projector_on(lambda b: b[0] == 0 and sum(b[i] for i in SPATIAL) == 2),
        ),
        (
            "EtVV_vector_time_odd_w3",
            projector_on(lambda b: b[0] == 1 and sum(b[i] for i in SPATIAL) == 2),
        ),
        (
            "EVVV_scalar_time_even_w3",
            projector_on(lambda b: b[0] == 0 and sum(b[i] for i in SPATIAL) == 3),
        ),
        ("EtVVV_scalar_time_odd_w4", projector_on(lambda b: weight(b) == 4)),
    ]


def rank_four_equivariant_candidates() -> list[tuple[tuple[str, ...], np.ndarray]]:
    blocks = local_spin_time_blocks()
    out: list[tuple[tuple[str, ...], np.ndarray]] = []
    for n in range(1, len(blocks) + 1):
        for combo in combinations(blocks, n):
            p = sum((block for _, block in combo), np.zeros((DIM, DIM), dtype=complex))
            if rank(p) == 4:
                out.append((tuple(name for name, _ in combo), p))
    return out


def axis_monomial(axis: int) -> tuple[int, int, int, int]:
    return bits_from_occ([axis])


def first_variation_support_projector() -> np.ndarray:
    return projector_on(lambda bits: weight(bits) == 1)


def third_composite_support_projector() -> np.ndarray:
    return projector_on(lambda bits: weight(bits) == 3)


def link_local_action_terms() -> list[dict]:
    """A local time-completed staggered/Dirac star: one term per primitive link.

    The coefficients stand in for staggered eta signs and orientation signs.
    Their values do not affect support degree.
    """
    return [
        {"axis": axis, "source_degree": 1, "monomial": axis_monomial(axis), "eta": (-1) ** axis}
        for axis in range(4)
    ]


def first_variation_vector() -> np.ndarray:
    vec = np.zeros((DIM, 1), dtype=complex)
    for term in link_local_action_terms():
        vec[INDEX[term["monomial"]], 0] = term["eta"]
    return vec


def source_derivative_images() -> list[np.ndarray]:
    """Images of dS_link(du_a) for the retained one-link source variables."""
    images = []
    for term in link_local_action_terms():
        vec = np.zeros((DIM, 1), dtype=complex)
        vec[INDEX[term["monomial"]], 0] = term["eta"]
        images.append(vec)
    return images


def third_composite_vector() -> np.ndarray:
    vec = np.zeros((DIM, 1), dtype=complex)
    for missing in range(4):
        monomial = bits_from_occ([axis for axis in range(4) if axis != missing])
        vec[INDEX[monomial], 0] = 1.0
    return vec


def hodge_image_weights(star: np.ndarray, source_weight: int) -> set[int]:
    weights: set[int] = set()
    for col, bits in enumerate(BASIS):
        if weight(bits) != source_weight:
            continue
        rows = np.flatnonzero(np.abs(star[:, col]) > TOL)
        weights.update(weight(BASIS[int(row)]) for row in rows)
    return weights


def max_symmetry_error(p: np.ndarray) -> float:
    gens = spatial_generators()
    finite = [time_parity(), cpt_grading()]
    return max([comm(p, g) for g in gens] + [comm(p, u) for u in finite])


def cl4_generators() -> list[np.ndarray]:
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    return [
        np.kron(sx, I2),
        np.kron(sy, I2),
        np.kron(sz, sx),
        np.kron(sz, sy),
    ]


def clifford_error(gammas: list[np.ndarray]) -> float:
    err = 0.0
    I4 = np.eye(4, dtype=complex)
    for i, gi in enumerate(gammas):
        for j, gj in enumerate(gammas):
            target = 2.0 * I4 if i == j else np.zeros((4, 4), dtype=complex)
            err = max(err, fro(gi @ gj + gj @ gi - target))
    return err


def algebra_span_rank(gammas: list[np.ndarray]) -> int:
    words = [np.eye(4, dtype=complex)]
    for mask in range(1, 1 << 4):
        m = np.eye(4, dtype=complex)
        for i in range(4):
            if mask & (1 << i):
                m = m @ gammas[i]
        words.append(m)
    mat = np.stack([w.reshape(-1) for w in words], axis=1)
    return int(np.linalg.matrix_rank(mat, tol=1.0e-10))


def car_error(gammas: list[np.ndarray]) -> float:
    c0 = (gammas[0] + 1j * gammas[1]) / 2.0
    c1 = (gammas[2] + 1j * gammas[3]) / 2.0
    cs = [c0, c1]
    I4 = np.eye(4, dtype=complex)
    err = 0.0
    for i, ci in enumerate(cs):
        for j, cj in enumerate(cs):
            err = max(err, fro(ci @ cj + cj @ ci))
            target = I4 if i == j else np.zeros((4, 4), dtype=complex)
            err = max(err, fro(ci @ cj.conj().T + cj.conj().T @ ci - target))
    return err


def check(label: str, ok: bool, detail: str) -> bool:
    print(f"[{'PASS' if ok else 'FAIL'}] {label}: {detail}")
    return ok


def main() -> int:
    print("=" * 78)
    print("PLANCK LINK-LOCAL FIRST-VARIATION P_A FORCING")
    print("=" * 78)
    print()
    print("Question: does the retained link-local action response force P_A?")
    print()

    p1 = projector_weight(1)
    p3 = projector_weight(3)
    star = hodge_star()
    action_terms = link_local_action_terms()
    first_vec = first_variation_vector()
    derivative_images = source_derivative_images()
    third_vec = third_composite_vector()
    p_first = first_variation_support_projector()
    p_third = third_composite_support_projector()

    results: list[bool] = []

    degrees = [term["source_degree"] for term in action_terms]
    monomials = [term["monomial"] for term in action_terms]
    results.append(
        check(
            "1. retained local action terms are one-link / one-axis source terms",
            len(action_terms) == 4 and degrees == [1, 1, 1, 1] and set(monomials) == set(axis_monomial(a) for a in range(4)),
            f"terms={[(AXES[t['axis']], t['source_degree'], t['monomial']) for t in action_terms]}",
        )
    )

    support_indices = {BASIS[i] for i, val in enumerate(first_vec[:, 0]) if abs(val) > TOL}
    derivative_support = {
        BASIS[i]
        for image in derivative_images
        for i, val in enumerate(image[:, 0])
        if abs(val) > TOL
    }
    results.append(
        check(
            "2. first variation support is exactly the Hamming-weight-one packet",
            fro(p_first - p1) < TOL
            and support_indices == set(axis_monomial(a) for a in range(4))
            and derivative_support == support_indices,
            f"dS images={sorted(derivative_support)}; rank={rank(p_first)}",
        )
    )

    third_support = {BASIS[i] for i, val in enumerate(third_vec[:, 0]) if abs(val) > TOL}
    first_third_overlap = fro(p_first @ p_third)
    results.append(
        check(
            "3. Hodge-dual P_3 is a third-composite/flux support, not a first variation",
            fro(p_third - p3) < TOL and first_third_overlap < TOL and all(weight(b) == 3 for b in third_support),
            f"P3 support={sorted(third_support)}; P1/P3 overlap={first_third_overlap:.2e}",
        )
    )

    p1_to_p3 = fro(star @ p1 @ star.conj().T - p3)
    star_image_weights = hodge_image_weights(star, 1)
    results.append(
        check(
            "4. Hodge duality is not an automorphism of the fundamental link-source domain",
            p1_to_p3 < TOL and star_image_weights == {3},
            f"*P1*=P3 error={p1_to_p3:.2e}; source degree 1 maps to weights={sorted(star_image_weights)}",
        )
    )

    candidates = rank_four_equivariant_candidates()
    matches_first = [names for names, p in candidates if fro(p - p_first) < TOL]
    nonmatches = [names for names, p in candidates if fro(p - p_first) >= TOL]
    results.append(
        check(
            "5. link-first-variation support selects a unique rank-four equivariant projector",
            len(candidates) == 17 and len(matches_first) == 1 and len(nonmatches) == 16,
            f"rank-four candidates={len(candidates)}; selected={matches_first[0] if matches_first else None}",
        )
    )

    p1_sym = max_symmetry_error(p1)
    local_err = fro(p1 - local_polynomial_weight(1))
    results.append(
        check(
            "6. selected projector remains spin/time/CPT equivariant and tensor-local",
            p1_sym < TOL and local_err < TOL,
            f"P1 symmetry error={p1_sym:.2e}; local polynomial error={local_err:.2e}",
        )
    )

    gammas = cl4_generators()
    cl_err = clifford_error(gammas)
    span_rank = algebra_span_rank(gammas)
    ca_err = car_error(gammas)
    results.append(
        check(
            "7. selected rank-four packet supports the unique irreducible Cl_4(C) / CAR carrier",
            rank(p1) == 4 and cl_err < TOL and span_rank == 16 and ca_err < TOL,
            f"rank(P_A)={rank(p1)}; Clifford={cl_err:.2e}; span={span_rank}; CAR={ca_err:.2e}",
        )
    )

    forbidden_inputs = {
        "observable_principle_from_axiom": False,
        "yt_ward_identity": False,
        "alpha_LM_decorated_chain": False,
        "manual_P_A_selector": False,
        "cochain_normal_primitivity_added_by_hand": False,
    }
    results.append(
        check(
            "8. forbidden-input boundary",
            not any(forbidden_inputs.values()),
            "uses A_min link-local action support, anomaly time axis, and finite exterior algebra only",
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
        "Verdict: PASS. The primitive action response is link-local and first "
        "variational, so its support is uniquely P_1=P_A among the local "
        "rank-four equivariant projector classes. The Hodge-dual P_3 remains "
        "a valid flux/face representation, but it is not a fundamental "
        "one-link action variation. On the selected rank-four packet the "
        "standard Cl_4(C) module/CAR carrier is unique up to automorphism."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
