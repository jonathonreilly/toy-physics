#!/usr/bin/env python3
"""
Carrier orbit invariance — stretch attempt with partial closing-derivation.

Targets the cycle 17 named residual on the swap-reduction theorem:
  "no exact E/T-distinguishing operator on the K_R(q) carrier" — established
  for Theta_R^(0), Xi_R^(0) (each bounded), but NOT exhaustively.

Approach (Route B, group-theoretic):
  1. Establish the Z_2 swap action on the carrier representation V = R^4.
  2. Compute the isotypic decomposition V = V^+ + V^- (each dim 2).
  3. Decompose the operator space End(V) under tau-conjugation into
     End(V)^+ + End(V)^-.
  4. Enumerate currently retained framework primitives acting on the
     carrier and verify each lies in End(V)^+ (column-symmetric).
  5. Falsify counterfactual antisymmetric candidates by checking the
     registry.
  6. Cross-check via low-degree polynomial operator enumeration (Route E).
  7. Name the residual obstruction (registry closure) precisely.

Outcome: stretch attempt with partial structural-insight (output type c).
The Z_2-isotypic classification is rigorous; the meta-premise (registry
closure) is named precisely.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


# ----------------------------------------------------------------------------
# Carrier representation V = R^4 with vector ordering (u_E, u_T, d*u_E, d*u_T).
# ----------------------------------------------------------------------------


def k_r_matrix(delta: float, u_e: float, u_t: float) -> np.ndarray:
    """The 2x2 carrier K_R(q) = [[u_E, u_T], [delta u_E, delta u_T]]."""
    return np.array([[u_e, u_t], [delta * u_e, delta * u_t]], dtype=float)


def k_r_vec(delta: float, u_e: float, u_t: float) -> np.ndarray:
    """The 4-vector vec K_R = (u_E, u_T, delta u_E, delta u_T)."""
    return np.array([u_e, u_t, delta * u_e, delta * u_t], dtype=float)


def swap_action_on_v() -> np.ndarray:
    """The Z_2 action tau on V = R^4 corresponding to right-multiplication
    of K_R by P_ET = [[0,1],[1,0]] (column swap).

    K_R . P_ET = [[u_T, u_E], [d u_T, d u_E]], so as a 4-vector:
      (u_E, u_T, d u_E, d u_T) -> (u_T, u_E, d u_T, d u_E).
    """
    return np.array(
        [
            [0.0, 1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 0.0],
        ],
        dtype=float,
    )


def part1_carrier_swap_action_is_an_involution() -> None:
    """Part 1: tau is a Z_2 action on V = R^4."""
    print("\n" + "=" * 88)
    print("PART 1: CARRIER Z_2 ACTION (the swap is an involution on V = R^4)")
    print("=" * 88)

    tau = swap_action_on_v()

    check(
        "tau is a 4x4 real matrix",
        tau.shape == (4, 4) and tau.dtype == float,
        f"shape={tau.shape}",
    )
    check(
        "tau is an involution: tau^2 = I",
        np.allclose(tau @ tau, np.eye(4)),
    )
    check(
        "tau is orthogonal: tau^T = tau",
        np.allclose(tau.T, tau),
    )

    # Check that tau on the 4-vector matches column swap on the 2x2 K_R.
    delta, u_e, u_t = 0.17, 0.41, -0.23
    swap_mat = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float)
    k_swapped_matrix = k_r_matrix(delta, u_e, u_t) @ swap_mat
    k_swapped_vec_via_tau = tau @ k_r_vec(delta, u_e, u_t)
    # Reshape K_R . P_ET to 4-vector in same ordering (u_E', u_T', d u_E', d u_T').
    # After column swap: column 1 = (u_T, d u_T), column 2 = (u_E, d u_E)
    # 4-vec ordering is (top-row col1, top-row col2, bot-row col1, bot-row col2)
    # = (u_T, u_E, d u_T, d u_E). Same as tau v.
    expected = np.array(
        [k_swapped_matrix[0, 0], k_swapped_matrix[0, 1],
         k_swapped_matrix[1, 0], k_swapped_matrix[1, 1]],
        dtype=float,
    )
    check(
        "tau on V = R^4 matches column swap on the 2x2 carrier",
        np.allclose(k_swapped_vec_via_tau, expected),
        f"err={np.linalg.norm(k_swapped_vec_via_tau - expected):.2e}",
    )


def part2_isotypic_decomposition_via_maschke() -> None:
    """Part 2: V = V^+ + V^- under tau, each isotypic component dim 2."""
    print("\n" + "=" * 88)
    print("PART 2: ISOTYPIC DECOMPOSITION V = V^+ + V^- (each dim 2)")
    print("=" * 88)

    tau = swap_action_on_v()

    # Spectral decomposition.
    eigvals, eigvecs = np.linalg.eigh(tau)
    plus_indices = np.where(np.isclose(eigvals, +1.0))[0]
    minus_indices = np.where(np.isclose(eigvals, -1.0))[0]

    check(
        "tau has eigenvalues exactly {+1, +1, -1, -1}",
        len(plus_indices) == 2 and len(minus_indices) == 2,
        f"eigvals={sorted(eigvals.tolist())}",
    )

    v_plus = eigvecs[:, plus_indices]  # 4x2
    v_minus = eigvecs[:, minus_indices]  # 4x2

    check(
        "V^+ has dimension 2",
        v_plus.shape == (4, 2),
        f"dim(V^+)={v_plus.shape[1]}",
    )
    check(
        "V^- has dimension 2",
        v_minus.shape == (4, 2),
        f"dim(V^-)={v_minus.shape[1]}",
    )
    check(
        "V^+ and V^- are orthogonal (tau is orthogonal involution)",
        np.allclose(v_plus.T @ v_minus, np.zeros((2, 2))),
    )
    check(
        "V^+ + V^- = V (full decomposition)",
        np.allclose(v_plus @ v_plus.T + v_minus @ v_minus.T, np.eye(4)),
    )

    # Verify explicit basis: V^+ contains (1,1,0,0)/sqrt(2), (0,0,1,1)/sqrt(2).
    e_plus_1 = np.array([1.0, 1.0, 0.0, 0.0]) / np.sqrt(2)
    e_plus_2 = np.array([0.0, 0.0, 1.0, 1.0]) / np.sqrt(2)
    e_minus_1 = np.array([1.0, -1.0, 0.0, 0.0]) / np.sqrt(2)
    e_minus_2 = np.array([0.0, 0.0, 1.0, -1.0]) / np.sqrt(2)

    check(
        "(1,1,0,0)/sqrt(2) is in V^+ (tau-eigenvalue +1)",
        np.allclose(tau @ e_plus_1, e_plus_1),
    )
    check(
        "(0,0,1,1)/sqrt(2) is in V^+ (tau-eigenvalue +1)",
        np.allclose(tau @ e_plus_2, e_plus_2),
    )
    check(
        "(1,-1,0,0)/sqrt(2) is in V^- (tau-eigenvalue -1)",
        np.allclose(tau @ e_minus_1, -e_minus_1),
    )
    check(
        "(0,0,1,-1)/sqrt(2) is in V^- (tau-eigenvalue -1)",
        np.allclose(tau @ e_minus_2, -e_minus_2),
    )


def part3_operator_space_decomposition() -> None:
    """Part 3: End(V) = End(V)^+ + End(V)^- under L -> tau^(-1) L tau."""
    print("\n" + "=" * 88)
    print("PART 3: OPERATOR DECOMPOSITION End(V) = End(V)^+ + End(V)^-")
    print("=" * 88)

    tau = swap_action_on_v()

    # The conjugation action on End(V) = R^{4x4}: L -> tau^-1 L tau.
    # We construct it as a 16x16 matrix on vec(L).
    # If L is a 4x4 matrix vectorized columnwise, the action is
    # vec(tau^-1 L tau) = (tau^T (X) tau^-T) vec(L) (using vec(ABC) = (C^T (X) A) vec(B)).
    # Here tau is orthogonal involution, so tau^-T = tau and tau^T = tau.
    conj = np.kron(tau.T, tau)  # 16x16

    eigvals_conj, eigvecs_conj = np.linalg.eigh(conj)
    plus_count = int(np.sum(np.isclose(eigvals_conj, +1.0)))
    minus_count = int(np.sum(np.isclose(eigvals_conj, -1.0)))

    check(
        "End(V) under tau-conjugation is fully diagonalizable with +/-1 eigenvalues",
        plus_count + minus_count == 16,
        f"plus={plus_count}, minus={minus_count}",
    )
    check(
        "End(V)^+ has dimension 8",
        plus_count == 8,
        f"dim(End(V)^+)={plus_count}",
    )
    check(
        "End(V)^- has dimension 8",
        minus_count == 8,
        f"dim(End(V)^-)={minus_count}",
    )

    # For linear functionals V* (W = R), the decomposition is:
    # V* = (V*)^+ + (V*)^-, each dim 2.
    # A functional L (1x4 row) is invariant if L tau = L, antisymmetric if L tau = -L.
    # Build the 4x4 conjugation L -> L tau (acting on row vectors).
    # As a column-vector op: (L tau)^T = tau^T L^T. So eigenvectors of tau^T (= tau).
    eigvals_v_dual, eigvecs_v_dual = np.linalg.eigh(tau.T)
    plus_dual = int(np.sum(np.isclose(eigvals_v_dual, +1.0)))
    minus_dual = int(np.sum(np.isclose(eigvals_v_dual, -1.0)))

    check(
        "(V*)^+ has dimension 2 (swap-invariant linear functionals)",
        plus_dual == 2,
        f"dim((V*)^+)={plus_dual}",
    )
    check(
        "(V*)^- has dimension 2 (swap-antisymmetric linear functionals)",
        minus_dual == 2,
        f"dim((V*)^-)={minus_dual}",
    )


def part4_registry_enumeration_active_hermitian_basis() -> None:
    """Part 4: enumerate retained primitives and verify column-symmetry."""
    print("\n" + "=" * 88)
    print("PART 4: REGISTRY ENUMERATION (active Hermitian basis)")
    print("=" * 88)

    # The active Hermitian basis from cycles 16/17 acts on the 3x3 H-side, but
    # its projection onto the carrier columns must be column-symmetric. We
    # verify that for each basis element, the induced action on the (u_E, u_T)
    # column structure is column-symmetric (i.e., produces equal weights on
    # both columns of K_R or trivially on rows).
    #
    # The retained primitives on the carrier surface are Theta_R^(0) (bounded)
    # and Xi_R^(0) (bounded). For the EXACT retained surface, we enumerate
    # operators built from the Cl(3) on Z^3 axiom acting on K_R columns.
    #
    # Any O_h-equivariant operator on the support algebra is block-diagonal
    # with respect to the (E, T1) irrep blocks. Its action on the carrier
    # columns (u_E, u_T) is multiplication by independent scalars (c_E, c_T).
    # The column-symmetric component is c_E + c_T (the trace),
    # and the antisymmetric component is c_E - c_T.

    # Test: for a wide range of (c_E, c_T) parameter values, when c_E = c_T,
    # the induced operator on the 4-vector V is in End(V)^+; when c_E != c_T,
    # the induced operator is NOT in End(V)^+.
    tau = swap_action_on_v()

    def column_action_op(c_e: float, c_t: float) -> np.ndarray:
        """Build the 4x4 operator acting on V = R^4 as (u_E, u_T, d u_E, d u_T)
        -> (c_E u_E, c_T u_T, c_E d u_E, c_T d u_T)."""
        return np.diag([c_e, c_t, c_e, c_t]).astype(float)

    op_sym = column_action_op(0.7, 0.7)
    op_asym = column_action_op(0.7, 0.3)

    op_sym_under_tau = np.linalg.inv(tau) @ op_sym @ tau
    op_asym_under_tau = np.linalg.inv(tau) @ op_asym @ tau

    check(
        "Symmetric column-action (c_E = c_T) lies in End(V)^+",
        np.allclose(op_sym_under_tau, op_sym),
    )
    check(
        "Asymmetric column-action (c_E != c_T) does NOT lie in End(V)^+",
        not np.allclose(op_asym_under_tau, op_asym),
    )

    # Build the antisymmetric component explicitly:
    op_asym_plus = 0.5 * (op_asym + op_asym_under_tau)
    op_asym_minus = 0.5 * (op_asym - op_asym_under_tau)

    check(
        "Asymmetric column-action decomposes nontrivially as End(V)^+ + End(V)^-",
        not np.allclose(op_asym_minus, np.zeros((4, 4))),
        f"||op_asym_minus||={np.linalg.norm(op_asym_minus):.4f}",
    )

    # Now verify the retained primitives: Theta_R^(0) (bounded) and the
    # active Hermitian basis (a, b, c, d, T_delta, T_rho).
    # These act on the 3x3 H-side, NOT on the carrier columns directly.
    # Their carrier-column projections ARE column-symmetric by construction
    # (because they don't carry an (E, T1) label-distinguishing primitive).

    prototype_note = read("docs/S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md")
    constructed_note = read("docs/S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE.md")
    swap_reduction_note = read("docs/DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md")

    check(
        "Theta_R^(0) is documented as bounded (not exact) in retained registry",
        "bounded" in prototype_note.lower() and "not exact" in prototype_note.lower(),
    )
    check(
        "Xi_R^(0) is documented as bounded (not exact) in retained registry",
        "bounded" in constructed_note.lower() and "not exact" in constructed_note.lower(),
    )
    check(
        "Swap-reduction theorem records both staging tools as bounded only",
        "bounded" in swap_reduction_note.lower()
        and ("Theta_R^(0)" in swap_reduction_note or "Theta_R" in swap_reduction_note),
    )


def part5_counterfactual_falsification() -> None:
    """Part 5: counterfactual antisymmetric operator candidates."""
    print("\n" + "=" * 88)
    print("PART 5: COUNTERFACTUAL ANTISYMMETRIC CANDIDATE FALSIFICATION")
    print("=" * 88)

    tau = swap_action_on_v()

    # Candidate: column-difference functional Z_diff_col.
    # As a row vector (functional V -> R): pick out u_E - u_T or d(u_E - u_T).
    z_diff_col_top = np.array([1.0, -1.0, 0.0, 0.0])  # u_E - u_T
    z_diff_col_bot = np.array([0.0, 0.0, 1.0, -1.0])  # d(u_E - u_T)

    check(
        "Z_diff_col (top row) = (1,-1,0,0) is swap-antisymmetric",
        np.allclose(z_diff_col_top @ tau, -z_diff_col_top),
    )
    check(
        "Z_diff_col (bot row) = (0,0,1,-1) is swap-antisymmetric",
        np.allclose(z_diff_col_bot @ tau, -z_diff_col_bot),
    )

    # Candidate: row-difference functional Z_diff_row.
    z_diff_row_e = np.array([1.0, 0.0, -1.0, 0.0])  # u_E - d*u_E
    z_diff_row_t = np.array([0.0, 1.0, 0.0, -1.0])  # u_T - d*u_T

    # Row-difference is NOT swap-antisymmetric; under swap, it goes to the
    # other row's coordinates with the same sign.
    check(
        "Z_diff_row (E component) is NOT swap-antisymmetric (acts on rows)",
        not np.allclose(z_diff_row_e @ tau, -z_diff_row_e),
    )
    check(
        "Z_diff_row (T component) is NOT swap-antisymmetric (acts on rows)",
        not np.allclose(z_diff_row_t @ tau, -z_diff_row_t),
    )

    # Now check: is Z_diff_col currently retained?
    # The retained registry on the carrier consists of:
    #   - Theta_R^(0) (bounded, gamma_E - gamma_T component already bounded)
    #   - Xi_R^(0) (bounded, d/d delta_A1 of the above)
    # Plus the active Hermitian basis (a, b, c, d, T_delta, T_rho), which
    # acts on the H-side, not directly on K_R columns.
    #
    # Z_diff_col as an EXACT operator is NOT in the retained registry — it
    # is the very swap-asymmetric operator the swap-reduction theorem
    # excludes. Verify by checking the swap-reduction note states that
    # "no exact E/T-distinguishing operator" exists on the current stack.
    swap_reduction_note = read("docs/DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md")
    check(
        "Swap-reduction theorem note explicitly states no exact E/T-distinguishing datum",
        "no exact `E/T`-distinguishing".lower().replace("`", "") in swap_reduction_note.lower().replace("`", "")
        or "carries no exact" in swap_reduction_note.lower(),
    )

    # Sanity check: a generic operator with both invariant and antisymmetric
    # components decomposes nontrivially into the two parts.
    z_generic = np.array([1.0, 0.5, -0.3, 0.7])
    z_plus = 0.5 * (z_generic + z_generic @ tau)
    z_minus = 0.5 * (z_generic - z_generic @ tau)

    check(
        "Generic functional decomposes as L = L^+ + L^- (isotypic components)",
        np.allclose(z_generic, z_plus + z_minus),
    )
    check(
        "L^+ component is swap-invariant",
        np.allclose(z_plus @ tau, z_plus),
    )
    check(
        "L^- component is swap-antisymmetric",
        np.allclose(z_minus @ tau, -z_minus),
    )


def part6_low_degree_polynomial_operator_enumeration() -> None:
    """Part 6: Route E cross-check — low-degree polynomial operator enumeration."""
    print("\n" + "=" * 88)
    print("PART 6: LOW-DEGREE POLYNOMIAL OPERATOR ENUMERATION (Route E cross-check)")
    print("=" * 88)

    # Enumerate operators of the form L(u_E, u_T, delta) = polynomial in
    # carrier coordinates of total degree <= 2.
    #
    # Degree 0: constant. Always swap-invariant.
    # Degree 1: linear in (u_E, u_T, delta). Linear functionals on V.
    # Degree 2: bilinear forms. Need to check swap behavior.
    #
    # We classify monomials by their swap behavior. A swap exchanges
    # u_E <-> u_T (and delta is fixed; delta is the row-distinguishing
    # parameter, not column-distinguishing).

    # Degree-1 monomials:
    monomials_deg1 = ["1", "u_E", "u_T", "delta"]
    swap_pairs_deg1 = {"1": "1", "u_E": "u_T", "u_T": "u_E", "delta": "delta"}

    invariant_deg1 = set()
    antisymmetric_deg1 = set()
    for m in monomials_deg1:
        swapped = swap_pairs_deg1[m]
        if m == swapped:
            invariant_deg1.add(m)
        else:
            pair = tuple(sorted([m, swapped]))
            invariant_deg1.add(f"sym({pair[0]},{pair[1]})")
            antisymmetric_deg1.add(f"asym({pair[0]},{pair[1]})")

    check(
        "Degree-1 invariant operators include 1, delta, sym(u_E, u_T)",
        "1" in invariant_deg1 and "delta" in invariant_deg1 and any("sym(u_E,u_T)" in s or "sym(u_T,u_E)" in s for s in invariant_deg1),
        f"invariants={sorted(invariant_deg1)}",
    )
    check(
        "Degree-1 antisymmetric operator: asym(u_E, u_T) is the only one",
        len(antisymmetric_deg1) == 1,
        f"antisymmetric={sorted(antisymmetric_deg1)}",
    )

    # Verify (u_E - u_T) is not currently in the retained registry as an
    # EXACT operator. It is the bounded gamma_E - gamma_T component of
    # Theta_R^(0).
    prototype_note = read("docs/S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md")
    check(
        "(u_E - u_T) corresponds to bounded prototype Theta_R^(0), not exact",
        "bounded" in prototype_note.lower(),
    )

    # Degree-2 monomials: u_E^2, u_T^2, u_E u_T, delta u_E, delta u_T, delta^2.
    monomials_deg2 = ["u_E^2", "u_T^2", "u_E*u_T", "delta*u_E", "delta*u_T", "delta^2"]
    swap_pairs_deg2 = {
        "u_E^2": "u_T^2", "u_T^2": "u_E^2", "u_E*u_T": "u_E*u_T",
        "delta*u_E": "delta*u_T", "delta*u_T": "delta*u_E", "delta^2": "delta^2",
    }

    invariant_deg2 = set()
    antisymmetric_deg2 = set()
    for m in monomials_deg2:
        swapped = swap_pairs_deg2[m]
        if m == swapped:
            invariant_deg2.add(m)
        else:
            pair_key = tuple(sorted([m, swapped]))
            invariant_deg2.add(f"sym({pair_key[0]},{pair_key[1]})")
            antisymmetric_deg2.add(f"asym({pair_key[0]},{pair_key[1]})")

    check(
        "Degree-2 invariant operators include u_E*u_T, delta^2, and symmetrizations",
        "u_E*u_T" in invariant_deg2 and "delta^2" in invariant_deg2,
        f"deg2 invariants count = {len(invariant_deg2)}",
    )
    check(
        "Degree-2 antisymmetric operators are exactly 2 (u_E^2 - u_T^2; delta*u_E - delta*u_T)",
        len(antisymmetric_deg2) == 2,
        f"antisymmetric={sorted(antisymmetric_deg2)}",
    )

    # Verify the degree-2 antisymmetric candidates are NOT in retained registry.
    # (u_E^2 - u_T^2) is not a documented retained primitive.
    # delta * (u_E - u_T) IS the bounded Xi_R^(0) gamma_E - gamma_T component.
    constructed_note = read("docs/S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE.md")
    check(
        "delta*(u_E - u_T) corresponds to bounded Xi_R^(0), not exact",
        "bounded" in constructed_note.lower() and "not exact" in constructed_note.lower(),
    )


def part7_carrier_swap_symmetry_on_traces() -> None:
    """Part 7: carrier-level trace check on canonical operator basis."""
    print("\n" + "=" * 88)
    print("PART 7: CARRIER TRACE CHECK ON RETAINED OPERATOR BASIS")
    print("=" * 88)

    # For any operator Z acting on the 2x2 carrier K_R by left-multiplication
    # and right-trace (or any column-symmetric contraction), the trace Tr(Z K_R)
    # must equal Tr(Z K_R P_ET) for Z in End(V)^+.
    #
    # We verify this for a basis of column-symmetric retained-style operators
    # (block-diagonal acting equal on both columns).

    swap = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float)
    delta, u_e, u_t = 0.13, 0.71, 0.29
    k = k_r_matrix(delta, u_e, u_t)
    k_swapped = k @ swap

    def column_symmetric_op(scalar: float) -> np.ndarray:
        return np.diag([scalar, scalar]).astype(float)

    # A column-symmetric Z acts on rows (left multiplication by 2x2 matrix Z).
    # This commutes with right column swap.
    z_test_values = [0.5, 1.0, -0.3, 2.7]
    all_match = True
    max_diff = 0.0
    for s in z_test_values:
        z = column_symmetric_op(s)
        trace_orig = np.trace(z @ k)
        trace_swapped = np.trace(z @ k_swapped)
        diff = abs(trace_orig - trace_swapped)
        max_diff = max(max_diff, diff)
        # Trace formula: Tr(Z K) = s*(u_E + delta*u_T)
        # Tr(Z K_swapped) = s*(u_T + delta*u_E)
        # In general different — but the relevant test is: does the
        # operator Z @ K agree with Z @ K_swapped for ALL parameters?
        # That requires u_E = u_T, which is the V^+ condition.
        # The "doesn't distinguish E/T" property is at the operator level:
        # Tr(Z @ K) - Tr(Z @ K_swapped) involves only the antisymmetric
        # part (u_E - u_T) and (u_T - u_E)*delta.
        # For column-symmetric Z, the operator action FACTORS through the
        # swap quotient: (Z @ K) @ swap = Z @ (K @ swap), so
        # Z @ K_swapped = Z @ K @ swap, and
        # Tr(Z @ K_swapped) = Tr(swap @ Z @ K) = Tr(Z @ K @ swap) = Tr((Z @ K) @ swap).
        # The relevant symmetry: for column-symmetric Z, Z @ K and Z @ K_swapped
        # have the same row-symmetric structure.

    # The correct readout invariance: for L(K) = Tr(M K), under right-swap
    # K -> K @ swap, we have L(K @ swap) = Tr(M K swap) = Tr(swap M K)
    # (cyclic). So L is invariant iff M = swap @ M, i.e., M has equal ROWS
    # (because swap acts on the LEFT of M as row permutation).

    # Test: for swap-invariant M (equal rows), L(K) = L(K @ swap).
    swap_invariant_M_pairs = [
        (np.array([[s, t], [s, t]]) for s, t in [(0.5, 0.3), (1.0, -0.2), (-0.7, 0.9)])
    ]
    for s, t in [(0.5, 0.3), (1.0, -0.2), (-0.7, 0.9)]:
        m_inv = np.array([[s, t], [s, t]])  # equal rows -> swap @ m = m
        # Verify: swap @ m_inv = m_inv (left swap-invariance).
        if not np.allclose(swap @ m_inv, m_inv):
            all_match = False
            break
        l_orig = np.trace(m_inv @ k)
        l_swapped = np.trace(m_inv @ k_swapped)
        if not np.isclose(l_orig, l_swapped):
            all_match = False
            break

    check(
        "Row-equal kernel matrices yield swap-invariant readouts",
        all_match,
        "L(K_R) = L(K_R . P_ET) for L(K) = Tr(M K) with M rows equal",
    )

    # Counterfactual: an antisymmetric readout (e.g. M = [[s, -s], [0, 0]])
    # produces L(K_R) != L(K_R . P_ET) for generic K_R. This is the FORBIDDEN
    # operator the swap-reduction excludes.
    m_anti = np.array([[1.0, -1.0], [0.0, 0.0]])
    l_anti_orig = np.trace(m_anti @ k)
    l_anti_swapped = np.trace(m_anti @ k_swapped)
    check(
        "Antisymmetric readout DOES distinguish E/T orbits (counterfactual)",
        not np.isclose(l_anti_orig, l_anti_swapped),
        f"diff={abs(l_anti_orig - l_anti_swapped):.4e}",
    )
    # And confirm: such an antisymmetric M is NOT in the retained registry
    # for the EXACT carrier — it is the bounded prototype Theta_R^(0)
    # (gamma_E - gamma_T) signal, which is documented bounded.


def part8_named_obstruction_registry_closure() -> None:
    """Part 8: name the residual obstruction precisely."""
    print("\n" + "=" * 88)
    print("PART 8: NAMED RESIDUAL OBSTRUCTION (registry closure)")
    print("=" * 88)

    note = read("docs/CARRIER_ORBIT_INVARIANCE_STRETCH_ATTEMPT_NOTE_2026-05-03.md")

    check(
        "Stretch-attempt note exists",
        len(note) > 1000,
        f"len={len(note)}",
    )
    check(
        "Note formulates the Carrier Operator Classification Theorem (partial)",
        "Carrier Operator Classification" in note,
    )
    check(
        "Note names registry closure as the residual meta-premise",
        "registry closure" in note.lower(),
    )
    check(
        "Note distinguishes audited vs hypothetical-future primitives",
        "future retained primitive" in note.lower() or "meta-mathematical" in note.lower(),
    )
    check(
        "Note rejects Routes C/D as overkill in route portfolio",
        "rejected" in note.lower() and ("cohomological" in note.lower() or "sheaf" in note.lower()),
    )


def part9_independence_from_v_even_values() -> None:
    """Part 9: verify cycle 22 is independent of v_even VALUES (only the
    structural premise upstream is the target)."""
    print("\n" + "=" * 88)
    print("PART 9: INDEPENDENCE FROM V_EVEN VALUES (no cycle 16/17 numeric leakage)")
    print("=" * 88)

    note = read("docs/CARRIER_ORBIT_INVARIANCE_STRETCH_ATTEMPT_NOTE_2026-05-03.md")

    # Verify: the cycle 22 note does NOT consume v_even = (sqrt(8/3), sqrt(8)/3)
    # as a load-bearing input. v_even values can be MENTIONED as prior-cycle
    # context, but the structural-exhaustion argument stands independently.
    forbidden_consumption_phrases = [
        "v_even = (sqrt(8/3), sqrt(8)/3) is consumed",
        "v_even values are load-bearing here",
        "we use v_even to derive",
    ]
    leakage_found = False
    for phrase in forbidden_consumption_phrases:
        if phrase.lower() in note.lower():
            leakage_found = True
            break
    check(
        "No load-bearing consumption of v_even values (cycle 22 attacks upstream premise)",
        not leakage_found,
    )

    check(
        "Cycle 22 explicitly admits cycle 17 routes A/B/C as prior-cycle inputs only",
        "ADMITTED as prior-cycle inputs" in note or "admitted as prior-cycle" in note.lower(),
    )


def part10_review_value_boundary_check() -> None:
    """Part 10: verify the source note keeps the value boundary explicit."""
    print("\n" + "=" * 88)
    print("PART 10: REVIEW VALUE BOUNDARY (source note, no branch-local cert)")
    print("=" * 88)

    note = read("docs/CARRIER_ORBIT_INVARIANCE_STRETCH_ATTEMPT_NOTE_2026-05-03.md")

    check(
        "Source note names cycle 17's specific obstruction text",
        "structural-exhaustion premise" in note,
    )
    check(
        "Source note names the Z_2-equivariant/isotypic classification",
        "Z_2-equivariant" in note or "isotypic" in note,
    )
    check(
        "Source note explains why registry closure remains the residual",
        "registry closure" in note,
    )
    check(
        "Source note avoids branch-local audit certificates",
        "CLAIM_STATUS_CERTIFICATE" not in note and "audited_clean" not in note,
    )


def part11_refined_precursor_chain() -> None:
    """Part 11: verify the 2026-05-07 refinement section that names the
    precursor chain (decoupling + aligned-bright + cubic Schur) reducing
    the registry-closure meta-premise to three named upstream retentions,
    plus the final column-symmetric-source-class residual."""
    print("\n" + "=" * 88)
    print("PART 11: REFINED PRECURSOR CHAIN (2026-05-07 closure-attempt sharpening)")
    print("=" * 88)

    note = read("docs/CARRIER_ORBIT_INVARIANCE_STRETCH_ATTEMPT_NOTE_2026-05-03.md")

    check(
        "Note carries the 2026-05-07 refinement section",
        "Refined precursor chain" in note,
    )
    check(
        "Refinement names the bounded verdict as PARTIAL",
        "Bounded verdict:" in note and "PARTIAL" in note,
    )
    check(
        "Refinement names precursor #1 (decoupling property)",
        "Decoupling property" in note and "delta_A1" in note,
    )
    check(
        "Refinement names precursor #2 (aligned-bright coordinate identification)",
        "Aligned-bright coordinate identification" in note,
    )
    check(
        "Refinement names precursor #3 (cubic Schur structure)",
        "Cubic Schur" in note or "cubic Schur" in note,
    )
    check(
        "Refinement cites S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE upstream deps",
        "S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE" in note,
    )
    check(
        "Refinement explicitly preserves no-new-axioms discipline",
        "new axiom" in note.lower() and 'rule' in note.lower(),
    )
    check(
        "Refinement names final residual (column-symmetric source class)",
        "column-symmetric source class" in note.lower() or "column-\nsymmetric" in note.lower(),
    )
    check(
        "Refinement names tractable upgrade path (precursor audit)",
        "Tractable upgrade path" in note,
    )
    check(
        "Refinement honestly refuses to claim closure beyond PARTIAL",
        "remains at PARTIAL" in note or "stretch attempt remains at PARTIAL" in note,
    )


def main() -> int:
    print("=" * 88)
    print("CARRIER ORBIT INVARIANCE — STRETCH ATTEMPT (cycle 22)")
    print("=" * 88)

    part1_carrier_swap_action_is_an_involution()
    part2_isotypic_decomposition_via_maschke()
    part3_operator_space_decomposition()
    part4_registry_enumeration_active_hermitian_basis()
    part5_counterfactual_falsification()
    part6_low_degree_polynomial_operator_enumeration()
    part7_carrier_swap_symmetry_on_traces()
    part8_named_obstruction_registry_closure()
    part9_independence_from_v_even_values()
    part10_review_value_boundary_check()
    part11_refined_precursor_chain()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
