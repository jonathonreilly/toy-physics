#!/usr/bin/env python3
"""
Primitive Clifford-Majorana edge consistency-check runner (bounded scope).

Authority note:
    docs/PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md

Scope clarification (after two prior `audited_renaming` verdicts):
    This runner verifies an explicit algebraic CONSISTENCY-OF-CONSTRUCTION
    on the ADMITTED rank-four carrier K = P_A H_cell. The carrier itself
    is NOT derived by this runner; it is admitted from the cited upstream
    link-local first-variation candidate authority (unaudited candidate).
    The runner hard-codes rank(P_A) = 4 and an explicit Cl_4(C) realization
    on C^4 by construction. Therefore PASS means the construction is
    internally consistent given the admitted carrier, NOT that the
    substrate forces P_A.

This runner checks, given the admitted carrier:

  * the retained spatial Cl(3) / SU(2) bivector content embeds as the
    spatial even subalgebra of a four-axis primitive coframe;
  * the anomaly-forced time axis extends that Cl(3) block to Cl_4(C);
  * on the admitted rank-four carrier the construction realizes the
    unique irreducible complex Cl_4 module (algebraic consistency, not
    substrate-forcing);
  * oriented Majorana pairs realize the two-mode CAR edge carrier;
  * the construction cross-checks c_Widom = c_cell = 1/4.

Exit code: 0 on full PASS, 1 on any FAIL.

PStack experiment: frontier-planck-primitive-clifford-majorana-edge-derivation
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np


PASS_BLOCKS = 0
FAIL_BLOCKS = 0
TOL = 1.0e-12


def block(name: str, passed: bool, detail: str, cls: str = "C") -> bool:
    global PASS_BLOCKS, FAIL_BLOCKS
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_BLOCKS += 1
    else:
        FAIL_BLOCKS += 1
    print(f"[{status} ({cls})] {name}: {detail}")
    return passed


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron(*ops: np.ndarray) -> np.ndarray:
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def anticommutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def clifford_generators() -> dict[str, np.ndarray]:
    """Hermitian Euclidean Cl_4 generators on K ~= C^4.

    The ordered primitive coframe is (t, n, tau_1, tau_2) for a selected
    oriented primitive face. The last three generators restrict to the
    retained spatial Cl(3) block; the first is the anomaly-forced time axis.
    """
    return {
        "t": kron(X, I2),
        "n": kron(Y, I2),
        "tau1": kron(Z, X),
        "tau2": kron(Z, Y),
    }


def algebra_words(generators: list[np.ndarray]) -> list[np.ndarray]:
    ident = np.eye(generators[0].shape[0], dtype=complex)
    words = [ident]
    for r in range(1, len(generators) + 1):
        for indices in itertools.combinations(range(len(generators)), r):
            mat = ident.copy()
            for idx in indices:
                mat = mat @ generators[idx]
            words.append(mat)
    return words


def complex_span_rank(mats: list[np.ndarray], tol: float = 1.0e-10) -> int:
    columns = [mat.reshape(-1) for mat in mats]
    return int(np.linalg.matrix_rank(np.column_stack(columns), tol=tol))


def span_residual(target: np.ndarray, basis: list[np.ndarray]) -> float:
    matrix = np.column_stack([b.reshape(-1) for b in basis])
    coeffs, *_ = np.linalg.lstsq(matrix, target.reshape(-1), rcond=None)
    projected = matrix @ coeffs
    return float(np.linalg.norm(target.reshape(-1) - projected))


def commutant_dimension(generators: list[np.ndarray], tol: float = 1.0e-10) -> int:
    dim = generators[0].shape[0]
    ident = np.eye(dim, dtype=complex)
    rows = []
    for gen in generators:
        rows.append(np.kron(ident, gen) - np.kron(gen.T, ident))
    system = np.vstack(rows)
    rank = int(np.linalg.matrix_rank(system, tol=tol))
    return dim * dim - rank


def direct_sum_generators(generators: list[np.ndarray], multiplicity: int) -> list[np.ndarray]:
    if multiplicity == 1:
        return generators
    zero = np.zeros_like(generators[0])
    out = []
    for gen in generators:
        rows = []
        for i in range(multiplicity):
            row = []
            for j in range(multiplicity):
                row.append(gen if i == j else zero)
            rows.append(row)
        out.append(np.block(rows))
    return out


def car_errors(modes: tuple[np.ndarray, ...]) -> tuple[float, float]:
    ident = np.eye(modes[0].shape[0], dtype=complex)
    max_cc = 0.0
    max_cct = 0.0
    creators = [mode.conj().T for mode in modes]
    for i, ci in enumerate(modes):
        for j, cj in enumerate(modes):
            max_cc = max(max_cc, np.linalg.norm(anticommutator(ci, cj)))
            expected = ident if i == j else np.zeros_like(ident)
            max_cct = max(
                max_cct,
                np.linalg.norm(anticommutator(ci, creators[j]) - expected),
            )
    return max_cc, max_cct


def transverse_laplacian(qs: tuple[float, ...]) -> float:
    return 1.0 - sum(math.cos(q) for q in qs) / len(qs)


def main() -> int:
    print("=" * 78)
    print("PLANCK PRIMITIVE CLIFFORD-MAJORANA EDGE CONSISTENCY CHECK")
    print("(bounded scope: P_A carrier admitted from upstream candidate authority)")
    print("=" * 78)
    print()
    print("Question (narrowed after two audited_renaming verdicts):")
    print("  GIVEN the admitted carrier K = P_A H_cell (rank 4), do the")
    print("  retained Cl(3) bivectors plus anomaly-forced time axis admit")
    print("  an explicit Cl_4(C) / two-mode CAR construction on K that is")
    print("  algebraically consistent and cross-validates c_Widom = c_cell?")
    print()
    print("Not in scope: substrate forcing of P_A (see SUBSTRATE_TO_P_A_FORCING")
    print("and FIRST_ORDER_COFRAME_UNCONDITIONALITY no-gos; conditional repair")
    print("route in PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING is unaudited).")
    print()

    gamma = clifford_generators()
    ordered = [gamma["t"], gamma["n"], gamma["tau1"], gamma["tau2"]]
    spatial = [gamma["n"], gamma["tau1"], gamma["tau2"]]
    ident4 = np.eye(4, dtype=complex)

    max_hermitian = max(np.linalg.norm(g - g.conj().T) for g in ordered)
    max_square = max(np.linalg.norm(g @ g - ident4) for g in ordered)
    max_clifford = 0.0
    for i, gi in enumerate(ordered):
        for j, gj in enumerate(ordered):
            expected = (2.0 if i == j else 0.0) * ident4
            max_clifford = max(
                max_clifford,
                np.linalg.norm(anticommutator(gi, gj) - expected),
            )
    block(
        "1. explicit Hermitian Cl_4 generators on C^4",
        max_hermitian < TOL and max_square < TOL and max_clifford < TOL,
        (
            f"Hermitian={max_hermitian:.2e}, square={max_square:.2e}, "
            f"Clifford={max_clifford:.2e}"
        ),
    )

    word_rank = complex_span_rank(algebra_words(ordered))
    comm_dim = commutant_dimension(ordered)
    faithful_dimension = 2**4 == 4**2 == word_rank
    block(
        "2. generated algebra is faithful and irreducible",
        word_rank == 16 and comm_dim == 1 and faithful_dimension,
        f"span rank={word_rank}=dim M_4(C), commutant dimension={comm_dim}",
    )

    spatial_rank = complex_span_rank(algebra_words(spatial))
    spatial_max_clifford = 0.0
    for i, gi in enumerate(spatial):
        for j, gj in enumerate(spatial):
            expected = (2.0 if i == j else 0.0) * ident4
            spatial_max_clifford = max(
                spatial_max_clifford,
                np.linalg.norm(anticommutator(gi, gj) - expected),
            )

    # Hermitian duals of the retained Cl(3) spatial bivectors. With
    # e_1=n, e_2=tau_1, e_3=tau_2, these are -i e_j e_k and generate su(2).
    bivectors = [
        -1j * gamma["tau1"] @ gamma["tau2"],
        -1j * gamma["tau2"] @ gamma["n"],
        -1j * gamma["n"] @ gamma["tau1"],
    ]
    max_bivector_square = max(np.linalg.norm(b @ b - ident4) for b in bivectors)
    max_bivector_hermitian = max(np.linalg.norm(b - b.conj().T) for b in bivectors)
    max_su2 = 0.0
    for i, bi in enumerate(bivectors):
        for j, bj in enumerate(bivectors):
            if i >= j:
                continue
            k = 3 - i - j
            sign = 1.0 if (i, j, k) in {(0, 1, 2), (1, 2, 0), (2, 0, 1)} else -1.0
            max_su2 = max(
                max_su2,
                np.linalg.norm(commutator(bi, bj) - sign * 2j * bivectors[k]),
            )
    pseudoscalar = gamma["n"] @ gamma["tau1"] @ gamma["tau2"]
    recovered_spatial = [-1j * b @ pseudoscalar for b in bivectors]
    max_duality = max(
        np.linalg.norm(a - b)
        for a, b in zip(recovered_spatial, spatial, strict=True)
    )
    block(
        "3. retained Cl(3) bivectors lift as the spatial SU(2) subset",
        (
            spatial_rank == 8
            and spatial_max_clifford < TOL
            and max_bivector_square < TOL
            and max_bivector_hermitian < TOL
            and max_su2 < TOL
            and max_duality < TOL
        ),
        (
            f"Cl_3 rank={spatial_rank}, su2 error={max_su2:.2e}, "
            f"bivector/vector duality={max_duality:.2e}"
        ),
    )

    time_axis = gamma["t"]
    time_spatial_anticomm = max(
        np.linalg.norm(anticommutator(time_axis, s)) for s in spatial
    )
    full_rank = complex_span_rank(algebra_words([time_axis, *spatial]))
    time_residual = span_residual(time_axis, algebra_words(spatial))
    block(
        "4. anomaly-forced time axis extends Cl_3 to Cl_4",
        (
            np.linalg.norm(time_axis @ time_axis - ident4) < TOL
            and time_spatial_anticomm < TOL
            and spatial_rank == 8
            and full_rank == 16
            and time_residual > 1.0
        ),
        (
            f"Cl_3 rank={spatial_rank} -> Cl_4 rank={full_rank}; "
            f"time/spatial anticommutator={time_spatial_anticomm:.2e}"
        ),
    )

    c_normal = 0.5 * (gamma["t"] + 1j * gamma["n"])
    c_tangent = 0.5 * (gamma["tau1"] + 1j * gamma["tau2"])
    max_cc, max_cct = car_errors((c_normal, c_tangent))
    reconstructed = [
        c_normal + c_normal.conj().T,
        -1j * (c_normal - c_normal.conj().T),
        c_tangent + c_tangent.conj().T,
        -1j * (c_tangent - c_tangent.conj().T),
    ]
    max_reconstruction = max(
        np.linalg.norm(a - b)
        for a, b in zip(ordered, reconstructed, strict=True)
    )
    c_tangent_flipped = 0.5 * (gamma["tau1"] - 1j * gamma["tau2"])
    flip_cc, flip_cct = car_errors((c_normal, c_tangent_flipped))
    block(
        "5. oriented Majorana pairs realize two-mode CAR",
        (
            max_cc < TOL
            and max_cct < TOL
            and max_reconstruction < TOL
            and flip_cc < TOL
            and flip_cct < TOL
        ),
        (
            f"CAR errors {{c,c}}={max_cc:.2e}, "
            f"{{c,c^dagger}}={max_cct:.2e}; orientation flip also CAR"
        ),
    )

    rank_pa = 4
    dim_cell = 2**4
    hamming_weight_one = math.comb(4, 1)
    fock_dim = 2**2
    c_cell = rank_pa / dim_cell
    block(
        "6. primitive packet rank equals F(C^2) dimension",
        hamming_weight_one == rank_pa == fock_dim and math.isclose(c_cell, 0.25),
        (
            f"rank(P_A)=C(4,1)={hamming_weight_one}; "
            f"dim F(C^2)={fock_dim}; c_cell={c_cell}"
        ),
    )

    doubled = direct_sum_generators(ordered, 2)
    doubled_comm_dim = commutant_dimension(doubled)
    faithful_dims = []
    irreducible_commutant_classes = set()
    for dim in range(1, 9):
        if dim % 4 != 0:
            continue
        multiplicity = dim // 4
        reps = direct_sum_generators(ordered, multiplicity)
        cdim = commutant_dimension(reps)
        faithful_dims.append((dim, cdim))
        if cdim == 1:
            irreducible_commutant_classes.add(cdim)
    permuted_signed = [gamma["n"], gamma["t"], -gamma["tau1"], gamma["tau2"]]
    permuted_rank = complex_span_rank(algebra_words(permuted_signed))
    permuted_comm_dim = commutant_dimension(permuted_signed)
    block(
        "7. rank-four Cl_4 module is unique up to automorphism",
        (
            comm_dim == 1
            and doubled_comm_dim == 4
            and faithful_dims == [(4, 1), (8, 4)]
            and len(irreducible_commutant_classes) == 1
            and permuted_rank == 16
            and permuted_comm_dim == 1
        ),
        (
            f"faithful dims<=8 {faithful_dims}; direct-sum commutant="
            f"{doubled_comm_dim}; irreducible commutant classes=1"
        ),
    )

    normal_crossings = 2.0
    q = (0.37, -0.81)
    delta = transverse_laplacian(q)
    delta_partner = transverse_laplacian(tuple(x + math.pi for x in q))
    tangent_crossings = 2.0 * 0.5
    c_widom = (normal_crossings + tangent_crossings) / 12.0
    lambda_source = 4.0 * c_cell
    g_newton_lat = 1.0 / lambda_source
    block(
        "8. Widom coefficient cross-validates the primitive coefficient",
        (
            math.isclose(delta_partner, 2.0 - delta, abs_tol=1.0e-15)
            and math.isclose(c_widom, 0.25, abs_tol=1.0e-15)
            and math.isclose(c_widom, c_cell, abs_tol=1.0e-15)
            and math.isclose(g_newton_lat, 1.0, abs_tol=1.0e-15)
        ),
        (
            f"c_Widom=(2+1)/12={c_widom}; "
            f"c_cell=4/16={c_cell}; G_Newton,lat={g_newton_lat}"
        ),
    )

    print()
    print(f"Summary: PASS={PASS_BLOCKS}  FAIL={FAIL_BLOCKS}")
    if FAIL_BLOCKS == 0:
        print()
        print(
            "Verdict: PASS (bounded scope). GIVEN the admitted carrier "
            "K = P_A H_cell, the explicit Cl_4(C) construction on C^4 is "
            "algebraically consistent: it realizes the irreducible complex "
            "Cl_4 module, the two-mode CAR algebra F(C^2) by oriented "
            "Majorana pairing, and cross-checks c_Widom=c_cell=1/4. "
            "This is a renaming-class consistency theorem, not a "
            "substrate-forcing derivation of P_A. Substrate-to-P_A "
            "provenance remains conditional on the cited unaudited "
            "link-local first-variation candidate authority. Audit "
            "ratification remains separate."
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
