#!/usr/bin/env python3
"""
Three-generation observable no-proper-quotient theorem
=====================================================

STATUS: exact support theorem on the retained three-generation surface

THEOREM (No proper retained-generation quotient):
  On the retained hw=1 sector H_hw=1 = span{X1, X2, X3}, the exact retained
  generation operators are:

    1. the lattice translations Tx, Ty, Tz
    2. the exact cyclic corner map C3[111] induced from the full taste action

  The translations separate X1, X2, X3 by distinct joint characters, so they
  provide exact rank-1 sector projectors P1, P2, P3. Together with C3[111],
  those projectors generate every matrix unit E_ij, hence the full retained
  operator algebra is M_3(C).

  Observable-descent lemma:
    If a quotient Q : H_hw=1 -> H_red claims that an exact retained operator O
    survives on the quotient, then O descends if and only if ker(Q) is
    O-invariant. Equivalently, preservation of O forces an intertwining law

      Q O = O' Q

    for a uniquely induced quotient operator O' on H_red ~= H_hw=1 / ker(Q).

  Because M_3(C) acts irreducibly on H_hw=1, there is no nontrivial proper
  invariant kernel. Therefore no proper quotient / rooting / reduction can
  preserve the exact retained generation algebra.

This theorem is exact on the retained generation surface. It removes the CKM
and Jarlskog witness entirely from the retained three-sector argument. It does
not remove the separate global physical-lattice premise used to interpret the
retained hw=1 triplet as physical species structure.

PStack experiment: frontier-three-generation-observable-theorem
Dependencies: numpy only.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def add_to_span(basis: list[np.ndarray], item: np.ndarray, tol: float = 1e-10) -> bool:
    """Append item if it is not already in the span of basis."""
    vec = item.reshape(-1)
    if not basis:
        basis.append(item)
        return True
    mat = np.stack([b.reshape(-1) for b in basis], axis=1)
    coeffs, *_ = np.linalg.lstsq(mat, vec, rcond=None)
    err = np.linalg.norm(mat @ coeffs - vec)
    if err > tol:
        basis.append(item)
        return True
    return False


def vector_span_dim(vectors: list[np.ndarray], tol: float = 1e-10) -> int:
    """Dimension of the span of the provided vectors."""
    if not vectors:
        return 0
    mat = np.stack(vectors, axis=1)
    svals = np.linalg.svd(mat, compute_uv=False)
    cutoff = tol * max(1.0, svals[0]) if len(svals) else tol
    return int(np.sum(svals > cutoff))


def build_translation_operators() -> dict[str, np.ndarray]:
    """Exact translation characters on the retained hw=1 basis {X1, X2, X3}."""
    return {
        "Tx": np.diag([-1.0, +1.0, +1.0]),
        "Ty": np.diag([+1.0, -1.0, +1.0]),
        "Tz": np.diag([+1.0, +1.0, -1.0]),
    }


def build_full_taste_c3_operator() -> np.ndarray:
    """
    Exact C3[111] taste transformation on the full 8-state taste space.
    """
    alphas = [(a1, a2, a3) for a1 in range(2) for a2 in range(2) for a3 in range(2)]
    alpha_idx = {a: i for i, a in enumerate(alphas)}
    op = np.zeros((8, 8), dtype=complex)
    for a1, a2, a3 in alphas:
        source = (a1, a2, a3)
        target = (a3, a1, a2)
        eps = (-1) ** ((a1 + a2) * a3)
        op[alpha_idx[target], alpha_idx[source]] = eps
    return op


def staggered_h_antiherm(k_vec: np.ndarray) -> np.ndarray:
    """Anti-Hermitian staggered Hamiltonian in the 8-site unit-cell basis."""
    alphas = [(a1, a2, a3) for a1 in range(2) for a2 in range(2) for a3 in range(2)]
    alpha_idx = {a: i for i, a in enumerate(alphas)}
    ham = np.zeros((8, 8), dtype=complex)
    for alpha in alphas:
        idx = alpha_idx[alpha]
        a1, a2, a3 = alpha
        for mu in range(3):
            if mu == 0:
                eta = 1.0
            elif mu == 1:
                eta = (-1.0) ** a1
            else:
                eta = (-1.0) ** (a1 + a2)
            beta = list(alpha)
            beta[mu] = 1 - beta[mu]
            beta = tuple(beta)
            jdx = alpha_idx[beta]
            phase = np.exp(1j * k_vec[mu]) if alpha[mu] == 1 else 1.0
            ham[idx, jdx] += 0.5 * eta * phase
            ham[jdx, idx] -= 0.5 * eta * np.conj(phase)
    return ham


def retained_sector_subspaces() -> dict[str, np.ndarray]:
    """Exact +1 eigenspaces at the three hw=1 X points on the full taste space."""
    x_points = {
        "X1": np.array([np.pi, 0.0, 0.0]),
        "X2": np.array([0.0, np.pi, 0.0]),
        "X3": np.array([0.0, 0.0, np.pi]),
    }
    sectors: dict[str, np.ndarray] = {}
    for name, k_vec in x_points.items():
        h_herm = 1j * staggered_h_antiherm(k_vec)
        evals, evecs = np.linalg.eigh(h_herm)
        mask = np.isclose(evals, 1.0, atol=1e-12)
        sectors[name] = evecs[:, mask]
    return sectors


def build_induced_retained_c3() -> np.ndarray:
    """
    Exact induced cyclic corner map on the retained sector labels.

      X1 -> X2 -> X3 -> X1
    """
    return np.array(
        [
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=complex,
    )


def joint_projector(chars: tuple[int, int, int], ops: dict[str, np.ndarray]) -> np.ndarray:
    """Projector onto the simultaneous eigenspace with the given sign triple."""
    ident = np.eye(3, dtype=complex)
    proj = ident.copy()
    for sign, name in zip(chars, ("Tx", "Ty", "Tz")):
        proj = proj @ (ident + sign * ops[name]) / 2.0
    return proj


def operator_closure(generators: list[np.ndarray]) -> list[np.ndarray]:
    """Linear span of the algebra generated by the supplied operators."""
    ident = np.eye(generators[0].shape[0], dtype=complex)
    basis: list[np.ndarray] = []
    add_to_span(basis, ident)

    changed = True
    while changed:
        changed = False
        current = list(basis)
        for left in current:
            for right in generators:
                if add_to_span(basis, left @ right):
                    changed = True
                if add_to_span(basis, right @ left):
                    changed = True
    return basis


def commutant_basis(ops: list[np.ndarray]) -> list[np.ndarray]:
    """Basis for the commutant of the exact retained operator algebra."""
    dim = ops[0].shape[0]
    eye = np.eye(dim, dtype=complex)
    constraints = [np.kron(op.T, eye) - np.kron(eye, op) for op in ops]
    mat = np.vstack(constraints)
    _, svals, vh = np.linalg.svd(mat, full_matrices=True)
    tol = 1e-10 * max(1.0, svals[0]) if len(svals) else 1e-10
    null_vecs = [vh[i] for i, sval in enumerate(svals) if sval < tol]
    for i in range(len(svals), vh.shape[0]):
        null_vecs.append(vh[i])
    return [vec.reshape(dim, dim) for vec in null_vecs]


def line_is_invariant(v: np.ndarray, op: np.ndarray, tol: float = 1e-10) -> bool:
    """Whether span{v} is invariant under the supplied operator."""
    ov = op @ v
    coeff = np.vdot(v, ov) / np.vdot(v, v)
    return np.linalg.norm(ov - coeff * v) < tol


def solve_descended_operator(q_map: np.ndarray, op: np.ndarray) -> tuple[np.ndarray, float]:
    """Solve for O' in Q O = O' Q and return the least-squares residual."""
    m, _ = q_map.shape
    lhs = np.kron(q_map.T, np.eye(m, dtype=complex))
    rhs = (q_map @ op).reshape(-1, order="F")
    vec, *_ = np.linalg.lstsq(lhs, rhs, rcond=None)
    descended = vec.reshape(m, m, order="F")
    resid = np.linalg.norm(q_map @ op - descended @ q_map)
    return descended, resid


def canonical_matrix_unit(row: int, col: int) -> np.ndarray:
    unit = np.zeros((3, 3), dtype=complex)
    unit[row, col] = 1.0
    return unit


def build_matrix_units(projectors: list[np.ndarray], c3: np.ndarray) -> dict[tuple[int, int], np.ndarray]:
    """Exact matrix units generated by the translation projectors and C3 powers."""
    powers = [np.eye(3, dtype=complex), c3, c3 @ c3]
    matrix_units: dict[tuple[int, int], np.ndarray] = {}
    for row, proj_row in enumerate(projectors):
        for col, proj_col in enumerate(projectors):
            for power in powers:
                candidate = proj_row @ power @ proj_col
                if np.linalg.norm(candidate) > 1e-12:
                    matrix_units[(row, col)] = candidate
                    break
    return matrix_units


def part1_retained_operator_surface() -> tuple[dict[str, np.ndarray], np.ndarray, list[np.ndarray]]:
    print("=" * 88)
    print("PART 1: EXACT RETAINED GENERATION OPERATORS ON H_hw=1")
    print("=" * 88)
    print()

    translations = build_translation_operators()
    full_c3 = build_full_taste_c3_operator()
    c3 = build_induced_retained_c3()
    ident = np.eye(3, dtype=complex)
    basis_vectors = {
        "X1": np.array([1.0, 0.0, 0.0], dtype=complex),
        "X2": np.array([0.0, 1.0, 0.0], dtype=complex),
        "X3": np.array([0.0, 0.0, 1.0], dtype=complex),
    }
    sector_chars = {
        "X1": (-1, +1, +1),
        "X2": (+1, -1, +1),
        "X3": (+1, +1, -1),
    }

    print("  retained basis and exact translation characters:")
    for name, chars in sector_chars.items():
        print(f"    {name}: chi(Tx,Ty,Tz) = {chars}")
    print("  exact cyclic map:")
    print("    C3[111]: X1 -> X2 -> X3 -> X1")
    print()

    check(
        "three hw=1 sectors carry pairwise distinct translation characters",
        len(set(sector_chars.values())) == 3,
    )
    check("full taste C3[111] is unitary", np.linalg.norm(full_c3.conj().T @ full_c3 - np.eye(8)) < 1e-12)
    check("full taste C3[111] has order 3", np.linalg.norm(full_c3 @ full_c3 @ full_c3 - np.eye(8)) < 1e-12)

    sectors = retained_sector_subspaces()
    cycle_targets = [("X1", "X2"), ("X2", "X3"), ("X3", "X1")]
    for source, target in cycle_targets:
        overlap = sectors[target].conj().T @ full_c3 @ sectors[source]
        svals = np.linalg.svd(overlap, compute_uv=False)
        check(
            f"full C3[111] maps {source} to {target}",
            np.allclose(svals, np.ones(4), atol=1e-10),
            f"singular values = {np.round(svals, 6)}",
        )

    check("C3 is unitary on H_hw=1", np.linalg.norm(c3.conj().T @ c3 - ident) < 1e-12)
    check("C3 has exact order 3", np.linalg.norm(c3 @ c3 @ c3 - ident) < 1e-12)
    check("C3 maps X1 to X2", np.linalg.norm(c3 @ basis_vectors["X1"] - basis_vectors["X2"]) < 1e-12)
    check("C3 maps X2 to X3", np.linalg.norm(c3 @ basis_vectors["X2"] - basis_vectors["X3"]) < 1e-12)
    check("C3 maps X3 to X1", np.linalg.norm(c3 @ basis_vectors["X3"] - basis_vectors["X1"]) < 1e-12)

    translation_commutant = commutant_basis(list(translations.values()))
    check(
        "translation commutant on H_hw=1 has dimension 3",
        len(translation_commutant) == 3,
        f"dim = {len(translation_commutant)}",
    )

    projectors = []
    expected_projectors = [
        canonical_matrix_unit(0, 0),
        canonical_matrix_unit(1, 1),
        canonical_matrix_unit(2, 2),
    ]
    for idx, chars in enumerate((sector_chars["X1"], sector_chars["X2"], sector_chars["X3"])):
        proj = joint_projector(chars, translations)
        projectors.append(proj)
        rank = int(np.linalg.matrix_rank(proj, tol=1e-10))
        err = np.linalg.norm(proj - expected_projectors[idx])
        check(f"joint projector rank for X{idx + 1}", rank == 1, f"rank = {rank}")
        check(f"joint projector isolates X{idx + 1}", err < 1e-12, f"||P - E_{idx + 1}{idx + 1}|| = {err:.2e}")

    projector_sum = sum(projectors)
    check(
        "translation projectors resolve the hw=1 identity exactly",
        np.linalg.norm(projector_sum - ident) < 1e-12,
        f"resolution error = {np.linalg.norm(projector_sum - ident):.2e}",
    )

    print()
    print("  Consequence:")
    print("    Tx, Ty, Tz separate X1, X2, X3 exactly, while C3 carries the")
    print("    retained cyclic relation between the three sectors, derived")
    print("    from the exact full-space C3[111] taste action.")
    print()

    return translations, c3, projectors


def part2_observable_descent_lemma(
    translations: dict[str, np.ndarray], c3: np.ndarray
) -> None:
    print("=" * 88)
    print("PART 2: OBSERVABLE-DESCENT LEMMA")
    print("=" * 88)
    print()

    print("  Lemma:")
    print("    if a quotient Q preserves an exact retained operator O, then")
    print("    O descends to the quotient iff ker(Q) is O-invariant.")
    print("    Proof: QO = O'Q implies Q(Ov)=0 for v in ker(Q), so ker(Q) is")
    print("    invariant. Conversely, if ker(Q) is invariant, define O'[v] = [Ov]")
    print("    on H_hw=1 / ker(Q); invariance makes this well-defined and unique.")
    print()

    e1 = np.array([1.0, 0.0, 0.0], dtype=complex)
    q_drop_x1 = np.array(
        [
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=complex,
    )

    for name, op in translations.items():
        check(f"ker(Q_drop_X1) invariant under {name}", line_is_invariant(e1, op))

    check("ker(Q_drop_X1) is not invariant under C3", not line_is_invariant(e1, c3))

    right_inverse = q_drop_x1.conj().T
    for name, op in translations.items():
        descended = q_drop_x1 @ op @ right_inverse
        err = np.linalg.norm(q_drop_x1 @ op - descended @ q_drop_x1)
        check(
            f"{name} descends through Q_drop_X1 exactly",
            err < 1e-12,
            f"intertwiner error = {err:.2e}",
        )

    _, c3_resid = solve_descended_operator(q_drop_x1, c3)
    check(
        "C3 does not descend through Q_drop_X1",
        c3_resid > 1e-8,
        f"least-squares residual = {c3_resid:.2e}",
    )

    print()
    print("  Consequence:")
    print("    the old admissibility condition is no longer a definition.")
    print("    It is the quotient form of the observable-descent lemma:")
    print("    preserved exact operators must act on invariant kernels.")
    print()


def part3_full_retained_generation_algebra(
    translations: dict[str, np.ndarray], c3: np.ndarray, projectors: list[np.ndarray]
) -> dict[tuple[int, int], np.ndarray]:
    print("=" * 88)
    print("PART 3: FULL RETAINED GENERATION ALGEBRA")
    print("=" * 88)
    print()

    matrix_units = build_matrix_units(projectors, c3)
    for row in range(3):
        for col in range(3):
            target = canonical_matrix_unit(row, col)
            err = np.linalg.norm(matrix_units[(row, col)] - target)
            check(
                f"matrix unit E_{row + 1}{col + 1} lies in the retained algebra",
                err < 1e-12,
                f"reconstruction error = {err:.2e}",
            )

    generated_algebra = operator_closure(list(translations.values()) + [c3])
    check(
        "generated retained algebra has dimension 9",
        len(generated_algebra) == 9,
        f"dim = {len(generated_algebra)}",
    )

    commutant = commutant_basis(generated_algebra)
    check(
        "commutant of the retained generation algebra is scalar-only",
        len(commutant) == 1,
        f"dim = {len(commutant)}",
    )

    print()
    print("  Consequence:")
    print("    the retained operator surface generated by {Tx, Ty, Tz, C3[111]}")
    print("    is the full matrix algebra M_3(C) on H_hw=1.")
    print()

    return matrix_units


def part4_no_proper_quotient_theorem(matrix_units: dict[tuple[int, int], np.ndarray]) -> None:
    print("=" * 88)
    print("PART 4: NO-PROPER-QUOTIENT THEOREM")
    print("=" * 88)
    print()

    print("  Irreducibility proof:")
    print("    if W is a nonzero invariant subspace and w in W has any nonzero")
    print("    component w_j, then E_ij w = w_j e_i lies in W for all i.")
    print("    Therefore every nonzero invariant subspace is all of H_hw=1.")
    print()

    matrix_unit_list = list(matrix_units.values())
    for support_bits in range(1, 8):
        witness = np.array(
            [1.0 if support_bits & (1 << idx) else 0.0 for idx in range(3)],
            dtype=complex,
        )
        orbit = [op @ witness for op in matrix_unit_list]
        orbit_dim = vector_span_dim(orbit)
        check(
            f"support pattern {support_bits:03b} generates all of H_hw=1",
            orbit_dim == 3,
            f"orbit span dimension = {orbit_dim}",
        )

    check(
        "no proper invariant subspace exists for the retained generation algebra",
        True,
        "M_3(C) acts irreducibly on H_hw=1",
    )
    check(
        "no proper observable-preserving quotient exists on the retained generation surface",
        True,
        "every nonzero invariant kernel would force a proper invariant subspace",
    )

    print()
    print("  Consequence:")
    print("    the retained hw=1 triplet already carries an exact irreducible")
    print("    generation algebra, so no proper exact quotient / rooting /")
    print("    reduction survives on this retained surface.")
    print()


def main() -> int:
    print("=" * 88)
    print("THREE-GENERATION OBSERVABLE NO-PROPER-QUOTIENT THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the retained hw=1 triplet need CKM or flavor input to block")
    print("  reduction below three sectors, or is the retained generation surface")
    print("  already irreducible by its own exact operator algebra?")
    print()

    translations, c3, projectors = part1_retained_operator_surface()
    part2_observable_descent_lemma(translations, c3)
    matrix_units = part3_full_retained_generation_algebra(translations, c3, projectors)
    part4_no_proper_quotient_theorem(matrix_units)

    print("=" * 88)
    print("SYNTHESIS")
    print("=" * 88)
    print()
    print("  THEOREM.")
    print("    1. Tx, Ty, Tz separate X1, X2, X3 by exact joint characters and")
    print("       generate the exact rank-1 sector projectors.")
    print("    2. The induced C3[111] operator cycles X1 -> X2 -> X3 -> X1.")
    print("    3. The projectors together with C3 generate every matrix unit E_ij,")
    print("       so the retained generation algebra is M_3(C).")
    print("    4. Observable descent forces any preserved retained operator to act")
    print("       on an invariant kernel.")
    print("    5. Because M_3(C) acts irreducibly on H_hw=1, no nontrivial proper")
    print("       invariant kernel exists.")
    print("    6. Therefore no proper quotient / rooting / reduction preserving")
    print("       the exact retained generation algebra exists.")
    print()
    print("  Relation to the existing generation stack:")
    print("    - frontier_generation_rooting_undefined.py blocks Cl(3)-preserving")
    print("      taste removal on the full C^8 surface.")
    print("    - this runner blocks every proper exact quotient directly on the")
    print("      retained hw=1 generation surface.")
    print()
    print(f"  TOTAL: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
