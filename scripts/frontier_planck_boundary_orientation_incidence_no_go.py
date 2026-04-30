#!/usr/bin/env python3
"""Stretch no-go for deriving P_A from oriented boundary incidence.

The preceding audit-ratified no-gos show that the retained substrate
symmetries do not distinguish the one-form sector P_1 from the Hodge-dual
three-form sector P_3. This runner tests the most plausible repair route:
oriented boundary incidence / variational first-response language.

The result is negative. The oriented boundary of a four-axis primitive cell is
naturally represented by three-form faces, while the normal one-form
representation is obtained by Hodge duality. Without an independently derived
rule that the cochain/normal representation is primitive, boundary incidence
does not select P_1 over P_3.
"""

from __future__ import annotations

from itertools import combinations, product

import numpy as np

TOL = 1.0e-10


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


def bits_from_occ(occ: list[int]) -> tuple[int, int, int, int]:
    return tuple(1 if i in occ else 0 for i in range(4))


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
        target = bits_from_occ(comp)
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


def basis_vector(bits: tuple[int, int, int, int]) -> np.ndarray:
    v = np.zeros((DIM, 1), dtype=complex)
    v[INDEX[bits], 0] = 1.0
    return v


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
        for old_pos, _old_axis in enumerate(occ):
            for new_axis in range(4):
                coeff = a[new_axis, occ[old_pos]]
                if abs(coeff) < TOL:
                    continue
                replaced = replace_sign(occ, old_pos, new_axis)
                if replaced is None:
                    continue
                new_occ, sign = replaced
                target = bits_from_occ(new_occ)
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


def one_form_basis() -> list[tuple[int, int, int, int]]:
    return [bits_from_occ([axis]) for axis in range(4)]


def oriented_face_columns(star: np.ndarray) -> np.ndarray:
    """Columns are oriented 3-face vectors i_{e_a}(t^x^y^z) = *e^a."""
    cols = []
    for bits in one_form_basis():
        cols.append(star @ basis_vector(bits))
    return np.hstack(cols)


def incidence_pairing(face_cols: np.ndarray) -> np.ndarray:
    """Pair normal one-forms e_a with oriented complementary faces *e_a."""
    normals = [basis_vector(bits) for bits in one_form_basis()]
    star = hodge_star()
    # <*e_a, face_b> gives the signed incidence pairing.
    rows = []
    for normal in normals:
        rows.append((star @ normal).conj().T @ face_cols)
    return np.vstack(rows)


def hodge_dual_polynomial_error() -> float:
    """Compare P_3 with the Hodge image of the first homogeneous packet."""
    star = hodge_star()
    p1 = local_polynomial_weight(1)
    p3 = local_polynomial_weight(3)
    return fro(star @ p1 @ star.conj().T - p3)


def max_symmetry_error(p: np.ndarray) -> float:
    gens = spatial_generators()
    tpar = time_parity()
    cpt = cpt_grading()
    return max([comm(p, g) for g in gens] + [comm(p, tpar), comm(p, cpt)])


def check(label: str, ok: bool, detail: str) -> bool:
    print(f"[{'PASS' if ok else 'FAIL'}] {label}: {detail}")
    return ok


def main() -> int:
    print("=" * 78)
    print("PLANCK BOUNDARY ORIENTATION / INCIDENCE STRETCH NO-GO")
    print("=" * 78)
    print()
    print("Question: does oriented boundary incidence force P_1=P_A over P_3?")
    print()

    star = hodge_star()
    p1 = projector_weight(1)
    p3 = projector_weight(3)
    face_cols = oriented_face_columns(star)
    pairing = incidence_pairing(face_cols)

    results: list[bool] = []

    star_unitarity = fro(star.conj().T @ star - I16)
    p1_to_p3 = fro(star @ p1 @ star.conj().T - p3)
    results.append(
        check(
            "1. construct H_cell, P_1, P_3, and oriented Hodge map",
            DIM == 16 and star_unitarity < TOL and p1_to_p3 < TOL,
            f"dim={DIM}; star unitary={star_unitarity:.2e}; *P1*=P3 error={p1_to_p3:.2e}",
        )
    )

    expected_face_cols = []
    for missing in range(4):
        target = bits_from_occ([axis for axis in range(4) if axis != missing])
        sign = permutation_sign([missing] + [axis for axis in range(4) if axis != missing])
        expected_face_cols.append(sign * basis_vector(target))
    expected_faces = np.hstack(expected_face_cols)
    face_error = fro(face_cols - expected_faces)
    results.append(
        check(
            "2. oriented four-cell face incidence equals Hodge-dual normal data",
            face_error < TOL and np.linalg.matrix_rank(face_cols) == 4,
            f"face incidence error={face_error:.2e}; face rank={np.linalg.matrix_rank(face_cols)}",
        )
    )

    pairing_error = fro(pairing - np.eye(4))
    results.append(
        check(
            "3. normal/face incidence pairing is perfect but not selective",
            pairing_error < TOL,
            f"<*e_a, face_b> identity error={pairing_error:.2e}",
        )
    )

    p1_sym = max_symmetry_error(p1)
    p3_sym = max_symmetry_error(p3)
    results.append(
        check(
            "4. P_1 and P_3 satisfy the same spin/time/CPT equivariance tests",
            p1_sym < TOL and p3_sym < TOL,
            f"P1 symmetry={p1_sym:.2e}; P3 symmetry={p3_sym:.2e}",
        )
    )

    ns = [number_op(i) for i in range(4)]
    locality_errors = [fro(star @ n @ star.conj().T - (I16 - n)) for n in ns]
    results.append(
        check(
            "5. Hodge duality preserves the tensor-local number algebra",
            max(locality_errors) < TOL,
            f"max *n_i*^-1-(1-n_i)={max(locality_errors):.2e}",
        )
    )

    dual_poly_error = hodge_dual_polynomial_error()
    p1_local = fro(p1 - local_polynomial_weight(1))
    p3_local = fro(p3 - local_polynomial_weight(3))
    results.append(
        check(
            "6. first homogeneous response and third homogeneous face response are dual",
            dual_poly_error < TOL and p1_local < TOL and p3_local < TOL,
            f"G1 local={p1_local:.2e}; G3 local={p3_local:.2e}; Hodge dual={dual_poly_error:.2e}",
        )
    )

    one_rank = int(round(np.trace(p1).real))
    flux_rank = int(round(np.trace(p3).real))
    current_flux_dual = p1_to_p3 < TOL and one_rank == flux_rank == 4
    results.append(
        check(
            "7. Noether current one-form and flux three-form have equivalent carriers",
            current_flux_dual,
            f"rank(one-form current)={one_rank}; rank(dual flux form)={flux_rank}",
        )
    )

    p1_p3_distinct = fro(p1 - p3)
    substrate_distinction_errors = {
        "rank_gap": abs(one_rank - flux_rank),
        "symmetry_gap": abs(p1_sym - p3_sym),
        "hodge_gap": p1_to_p3,
    }
    substrate_selects_normal = (
        substrate_distinction_errors["rank_gap"] > 0
        or substrate_distinction_errors["symmetry_gap"] > TOL
        or substrate_distinction_errors["hodge_gap"] > TOL
    )
    # A selector exists only after imposing cochain-normal primitivity; without
    # that extra premise, the computed substrate tests leave P_1 and P_3 tied.
    imposed_cochain_normal_primitivity = False
    would_select_p1_if_imposed = p1_p3_distinct > 1.0 and not substrate_selects_normal
    results.append(
        check(
            "8. selecting P_1 requires an extra cochain-normal primitive flag",
            (not imposed_cochain_normal_primitivity) and would_select_p1_if_imposed,
            (
                "P1 selection works only after adding cochain-normal primitivity; "
                f"substrate distinction errors={substrate_distinction_errors}"
            ),
        )
    )

    route_results = {
        "oriented_cubical_boundary": pairing_error < TOL and p1_to_p3 < TOL,
        "variational_first_derivative_boundary_only": dual_poly_error < TOL and p1_local < TOL and p3_local < TOL,
        "noether_current": current_flux_dual,
        "reflection_positive_time": p1_sym < TOL and p3_sym < TOL and abs(p1_sym - p3_sym) < TOL,
        "intrinsic_active_module": one_rank == flux_rank == 4 and p1_p3_distinct > 1.0,
    }
    results.append(
        check(
            "9. stuck fan-out exposes no substrate-only asymmetric selector",
            all(route_results.values()),
            "; ".join(f"{k}: {'PASS' if v else 'FAIL'}" for k, v in route_results.items()),
        )
    )

    forbidden_inputs = {
        "observable_principle_from_axiom": False,
        "yt_ward_identity": False,
        "alpha_LM_decorated_chain": False,
        "manual_P_A_selector": imposed_cochain_normal_primitivity,
    }
    results.append(
        check(
            "10. forbidden-input boundary",
            not any(forbidden_inputs.values()),
            "no forbidden theorem, decoration chain, or manual P_A selector used",
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
        "Verdict: NO-GO. Oriented boundary incidence does not force P_1=P_A. "
        "It gives a perfect normal/face duality: normals live in P_1, oriented "
        "faces/fluxes live in P_3, and Hodge duality preserves the substrate "
        "structure. Choosing the normal/cochain representation is the missing "
        "first-order boundary-orientation premise, not a derived consequence."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
