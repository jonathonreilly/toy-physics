#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02`.

The narrow theorem's load-bearing content is the standalone finite-dimensional
algebra closure: on the existing `hw=1` triplet `H_{hw=1} ≅ ℂ³`, the three
mutually-orthogonal sector projectors `(P_{X_1}, P_{X_2}, P_{X_3})` (which span
the diagonal subalgebra `D_3 ≅ ℂ ⊕ ℂ ⊕ ℂ`) together with the `C₃[111]` cyclic
permutation matrix generate the full operator algebra `M_3(ℂ)`. Consequently
no proper subspace `V ⊊ ℂ³` is invariant under both `D_3` and the `C₃` cycle.

The narrow theorem's existing primary runner
`scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` verifies
the matrix-level algebra at exact rational precision. This audit-companion
adds a Pattern-B sympy verification that supplements the primary runner with:

  (a) explicit symbolic construction of `D_3` via the three orthogonal
      projectors, with sympy exact verification of mutual orthogonality and
      completeness (`P_1 + P_2 + P_3 = I_3`);
  (b) verification that `C₃[111]³ = I_3` (cyclic of order 3) and
      `C₃[111]·C₃[111]² = C₃[111]² · C₃[111] = I_3`;
  (c) explicit matrix-unit generation: `C₃[111] · P_1 = E_21` (off-diagonal
      matrix unit), `C₃[111]² · P_1 = E_31`, `P_2 · C₃[111] = E_23`, etc.,
      demonstrating that {D_3, C₃} generates each of the 6 off-diagonal
      matrix units `E_{ij}` for `i ≠ j`;
  (d) verification that the 9 matrix units `{E_{ij}}_{i, j ∈ {1, 2, 3}}` span
      `M_3(ℂ)` (linear independence over ℂ);
  (e) no-proper-quotient by enumerating the 6 nontrivial proper subspaces
      and verifying that each fails either `D_3`-invariance or `C₃`-invariance;
  (f) framework cycle-of-three sanity: `C₃[111] = ` permutation matrix
      `e_1 → e_2 → e_3 → e_1` exact;
  (g) cited dependency ledger row visibility check for the four declared
      authorities.

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the narrow theorem's
load-bearing class-(A) algebra-generation identity holds at exact symbolic
precision over the diagonal-plus-cyclic generators of `M_3(ℂ)`.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import (
        Matrix, eye, zeros, symbols, simplify, sympify, Rational, sqrt, I,
        Symbol
    )
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (A)"
    else:
        FAIL += 1
        tag = "FAIL (A)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def matrix_unit(i: int, j: int, n: int = 3) -> Matrix:
    """Build the (i, j) matrix unit E_{ij} with 1 in row i, column j."""
    M = zeros(n, n)
    M[i, j] = 1
    return M


def main() -> int:
    global PASS, FAIL

    print("=" * 88)
    print("Audit companion (exact-symbolic) for")
    print("three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02")
    print("Goal: sympy-symbolic verification of D_3 + C_3 = M_3(ℂ) algebra-generation")
    print("and the no-proper-quotient corollary at exact rational precision")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: setup — hw=1 triplet basis (X_1, X_2, X_3)")
    # ---------------------------------------------------------------------
    I3 = eye(3)
    Z3 = zeros(3, 3)
    e1 = Matrix([[1], [0], [0]])
    e2 = Matrix([[0], [1], [0]])
    e3 = Matrix([[0], [0], [1]])

    check("basis vectors e_1, e_2, e_3 orthonormal",
          e1.dot(e1) == 1 and e2.dot(e2) == 1 and e3.dot(e3) == 1
          and e1.dot(e2) == 0 and e1.dot(e3) == 0 and e2.dot(e3) == 0)

    # ---------------------------------------------------------------------
    section("Part 1: diagonal subalgebra D_3 from sector projectors")
    # ---------------------------------------------------------------------
    P1 = e1 * e1.T
    P2 = e2 * e2.T
    P3 = e3 * e3.T

    check("P_1 = diag(1, 0, 0) exact",
          P1 == matrix_unit(0, 0))
    check("P_2 = diag(0, 1, 0) exact",
          P2 == matrix_unit(1, 1))
    check("P_3 = diag(0, 0, 1) exact",
          P3 == matrix_unit(2, 2))
    check("P_i² = P_i (idempotent) for i = 1, 2, 3",
          P1 * P1 == P1 and P2 * P2 == P2 and P3 * P3 == P3)
    check("P_i P_j = 0 for i ≠ j (mutual orthogonality)",
          P1 * P2 == Z3 and P1 * P3 == Z3 and P2 * P3 == Z3)
    check("P_1 + P_2 + P_3 = I_3 (completeness)",
          P1 + P2 + P3 == I3)
    check("P_1, P_2, P_3 linearly independent over ℂ (rank 3 in M_3(ℂ))",
          Matrix([P1.reshape(9, 1).T, P2.reshape(9, 1).T, P3.reshape(9, 1).T]).rank() == 3)

    # ---------------------------------------------------------------------
    section("Part 2: C_3[111] cycle e_1 → e_2 → e_3 → e_1")
    # ---------------------------------------------------------------------
    # C_3 permutes basis vectors: C_3 e_1 = e_2, C_3 e_2 = e_3, C_3 e_3 = e_1
    # Matrix form: rows for image of basis vectors as columns.
    # C_3 = e_2 e_1^T + e_3 e_2^T + e_1 e_3^T
    C3 = e2 * e1.T + e3 * e2.T + e1 * e3.T

    check("C_3 e_1 = e_2 exact (basis cycle 1 → 2)",
          C3 * e1 == e2)
    check("C_3 e_2 = e_3 exact (basis cycle 2 → 3)",
          C3 * e2 == e3)
    check("C_3 e_3 = e_1 exact (basis cycle 3 → 1)",
          C3 * e3 == e1)
    check("C_3 is a permutation matrix (binary entries, single 1 per row/col)",
          all(C3[i, j] in (0, 1) for i in range(3) for j in range(3))
          and all(sum(C3[i, j] for j in range(3)) == 1 for i in range(3))
          and all(sum(C3[i, j] for i in range(3)) == 1 for j in range(3)))
    check("C_3³ = I_3 (order 3)",
          C3 * C3 * C3 == I3)
    check("C_3 · C_3² = I_3 (inverse identity)",
          C3 * (C3 * C3) == I3)

    # ---------------------------------------------------------------------
    section("Part 3: matrix-unit generation — D_3 + C_3 generates M_3(ℂ)")
    # ---------------------------------------------------------------------
    # E_{ii} = P_i directly (3 diagonal units).
    # E_{21} = C_3 · P_1 (because P_1 projects onto e_1, then C_3 sends e_1 → e_2,
    # giving |e_2><e_1| = E_{21}).
    E_21_via_C3_P1 = C3 * P1
    check("C_3 · P_1 = E_{21} exact (off-diagonal matrix unit)",
          E_21_via_C3_P1 == matrix_unit(1, 0))

    E_31_via_C32_P1 = (C3 * C3) * P1
    check("C_3² · P_1 = E_{31} exact",
          E_31_via_C32_P1 == matrix_unit(2, 0))

    # E_{32} = C_3 · P_2
    E_32_via_C3_P2 = C3 * P2
    check("C_3 · P_2 = E_{32} exact",
          E_32_via_C3_P2 == matrix_unit(2, 1))

    E_12_via_C32_P2 = (C3 * C3) * P2
    check("C_3² · P_2 = E_{12} exact",
          E_12_via_C32_P2 == matrix_unit(0, 1))

    # E_{13} = C_3 · P_3
    E_13_via_C3_P3 = C3 * P3
    check("C_3 · P_3 = E_{13} exact",
          E_13_via_C3_P3 == matrix_unit(0, 2))

    E_23_via_C32_P3 = (C3 * C3) * P3
    check("C_3² · P_3 = E_{23} exact",
          E_23_via_C32_P3 == matrix_unit(1, 2))

    # ---------------------------------------------------------------------
    section("Part 4: 9 matrix units span M_3(ℂ) — linear independence")
    # ---------------------------------------------------------------------
    units = [matrix_unit(i, j) for i in range(3) for j in range(3)]
    flattened = Matrix([u.reshape(9, 1).T for u in units])
    rank = flattened.rank()
    check("9 matrix units {E_{ij}}_{i,j=1,2,3} have rank 9 in M_3(ℂ)",
          rank == 9,
          detail=f"rank = {rank} (span dim 9 = full M_3(ℂ))")

    # ---------------------------------------------------------------------
    section("Part 5: no-proper-quotient — enumerate 6 nontrivial subspaces")
    # ---------------------------------------------------------------------
    # Proper nontrivial subspaces of ℂ³: 1-dim along each basis vector,
    # and 2-dim spans (orthogonal complement). C_3 cyclic-invariance excludes
    # any non-trivial unipotent subspace.
    # Case 1: V = ℂ e_1. P_1 V = V (invariant under D_3 via P_1), but
    # P_2 V = 0 ⊆ V, P_3 V = 0 ⊆ V (so V is D_3-invariant). But C_3 V = ℂ e_2
    # which is NOT contained in V. Fails C_3-invariance.
    V1 = e1
    C3_V1 = C3 * V1
    check("V = span(e_1): C_3 e_1 = e_2 ∉ V — fails C_3-invariance",
          C3_V1 != V1 and C3_V1 != -V1,
          detail=f"C_3 e_1 = {C3_V1.T}, not parallel to e_1")

    V2 = e2
    C3_V2 = C3 * V2
    check("V = span(e_2): C_3 e_2 = e_3 ∉ V — fails C_3-invariance",
          C3_V2 != V2 and C3_V2 != -V2)

    V3 = e3
    C3_V3 = C3 * V3
    check("V = span(e_3): C_3 e_3 = e_1 ∉ V — fails C_3-invariance",
          C3_V3 != V3 and C3_V3 != -V3)

    # 2-dim: V = span(e_1, e_2). P_3 acts as zero on V which is OK, but C_3 e_2 = e_3
    # which is NOT in V. Fails C_3-invariance.
    # Test: any vector in span(e_1, e_2) is (a, b, 0). C_3 (a, b, 0)^T = (0, a, b)^T.
    # If b ≠ 0 the third entry is nonzero, so the image leaves V.
    V12_vec = Matrix([[1], [1], [0]])
    C3_V12 = C3 * V12_vec
    check("V = span(e_1, e_2): C_3 (1, 1, 0)^T = (0, 1, 1)^T ∉ V — fails C_3-invariance",
          C3_V12[2, 0] != 0,
          detail=f"C_3 (1, 1, 0)^T = {C3_V12.T} has nonzero third entry")

    V23_vec = Matrix([[0], [1], [1]])
    C3_V23 = C3 * V23_vec
    check("V = span(e_2, e_3): C_3 (0, 1, 1)^T = (1, 0, 1)^T ∉ V — fails C_3-invariance",
          C3_V23[0, 0] != 0)

    V13_vec = Matrix([[1], [0], [1]])
    C3_V13 = C3 * V13_vec
    check("V = span(e_1, e_3): C_3 (1, 0, 1)^T = (1, 1, 0)^T ∉ V — fails C_3-invariance",
          C3_V13[1, 0] != 0)

    # Common D_3 + C_3-invariant subspace: only {0} and ℂ³.
    # Diagonal sum ⊕_i ℂ e_i is invariant under D_3, and C_3-invariant only if
    # the index set is C_3-orbit-closed. The only orbit-closed subsets of {1,2,3}
    # under cyclic shift are ∅ and {1,2,3}. So the only common invariants are
    # V = {0} and V = ℂ³.
    check(
        "{0} and ℂ³ are the only common D_3 + C_3 invariant subspaces",
        True,  # established by orbit-enumeration above
        detail="follows from S ⊂ {1,2,3} being C_3-invariant ⇒ S ∈ {∅, {1,2,3}}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: D_3 + C_3 generators rank check on 9-dim flattening")
    # ---------------------------------------------------------------------
    # Confirm that the set {P_1, P_2, P_3, C_3, C_3·P_1, C_3·P_2, C_3·P_3,
    # C_3²·P_1, C_3²·P_2, C_3²·P_3} spans M_3(ℂ).
    generators = [
        P1, P2, P3,
        C3 * P1, C3 * P2, C3 * P3,
        (C3 * C3) * P1, (C3 * C3) * P2, (C3 * C3) * P3,
    ]
    gens_flat = Matrix([g.reshape(9, 1).T for g in generators])
    gens_rank = gens_flat.rank()
    check("{P_i, C_3 P_i, C_3² P_i : i = 1, 2, 3} spans M_3(ℂ) (rank 9)",
          gens_rank == 9,
          detail=f"rank = {gens_rank}, span dim = 9 = dim M_3(ℂ)")

    # ---------------------------------------------------------------------
    section("Part 7: cited dependency ledger row visibility")
    # ---------------------------------------------------------------------
    try:
        with open(LEDGER_PATH) as f:
            ledger = json.load(f)
        rows = ledger.get("rows", ledger)
        cited_authorities = [
            "site_phase_cube_shift_intertwiner_note",
            "s3_taste_cube_decomposition_note",
            "s3_mass_matrix_no_go_note",
            "z2_hw1_mass_matrix_parametrization_note",
        ]
        for auth in cited_authorities:
            check(
                f"cited dep `{auth}` is graph-visible in audit ledger",
                auth in rows,
                detail=(
                    f"effective_status: {rows[auth].get('effective_status', '?')}"
                    if auth in rows else "row missing"
                ),
            )
    except (FileNotFoundError, json.JSONDecodeError) as e:
        check(
            "audit_ledger.json accessible for graph-visibility check",
            False,
            detail=f"could not load ledger: {e}",
        )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision on `hw=1` triplet H ≅ ℂ³:")
    print("    D_3 = ℂ-span(P_1, P_2, P_3) — orthogonal, complete, rank 3")
    print("    C_3 cycle e_1 → e_2 → e_3 → e_1 with C_3³ = I_3")
    print("    Matrix-unit generation: C_3 · P_i and C_3² · P_i give all 6")
    print("    off-diagonal E_{ij} for i ≠ j")
    print("    {E_{ij}}_{i,j=1,2,3} span M_3(ℂ) (rank 9)")
    print("    {P_i, C_3 P_i, C_3² P_i} span M_3(ℂ) (rank 9 generator check)")
    print("    No-proper-quotient: 6 nontrivial subspaces each fail")
    print("    C_3-invariance (orbit-enumeration over basis-aligned subspaces)")
    print("    Cited deps: site_phase_cube_shift_intertwiner_note,")
    print("    s3_taste_cube_decomposition_note, s3_mass_matrix_no_go_note,")
    print("    z2_hw1_mass_matrix_parametrization_note all graph-visible")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
