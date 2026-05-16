#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`DM_NEUTRINO_BOSONIC_NORMALIZATION_OBSERVABLE_PRINCIPLE_BRIDGE_NARROW_THEOREM_NOTE_2026-05-16.md`.

The narrow theorem's load-bearing content is the observable-principle
bridge-selection statement that, given the retained upstream authorities
(X1) `OBSERVABLE_PRINCIPLE_REAL_D_BLOCK_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10`
and (X2) `CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10`,
the canonical Frobenius bridge ratio on the finite-dimensional bridge
algebra on C^16 with Y = P_R Γ_1 P_L is

  sqrt(Tr(Y^† Y) / Tr(Γ_1^† Γ_1))  =  sqrt(8 / 16)  =  1 / sqrt(2),

with the active-space ratio 1 excluded by (X1)'s block-local uniqueness
because Y carries zero W-source-response.

The proof steps verified at exact sympy precision are:

  (X3.N)  Y^2 = 0 on C^16.
  (X3.H)  Y + Y^† = Γ_1 on C^16.
  (X3.T1) Tr(Γ_1^† Γ_1) = 16.
  (X3.T2) Tr(Y^† Y) = 8.
  (DZ)    det(m I_{16} + j Y) = m^{16} identically in j (Y nilpotent).
  (DG)    det(m I_{16} + j Γ_1) = (m^2 - j^2)^8.
  (WG)    W[j Γ_1] = 8 log|1 - j^2/m^2| (closed-form match at exact rationals).
  (R)     sqrt(Tr Y^† Y / Tr Γ_1^† Γ_1) = 1/sqrt(2).
  (R1)    Active-space ratio Tr Y^† Y / Tr P_L = 1; flagged as
          non-admissible because Y is in the kernel of the (X1)
          source-response map.
  (R2)    Pseudoscalar companion i(Y - Y^†) is anti-Hermitian completion
          and is trace-orthogonal to Γ_1.

Counterfactual: a candidate Γ̃_1 with [γ_5, Γ̃_1] ≠ 0 breaks (X3.H),
confirming the anticommutation {γ_5, Γ_1} = 0 is load-bearing.

Companion role: not a new claim row beyond the source note; this script
provides audit-friendly evidence that the narrow theorem's load-bearing
algebra holds at exact symbolic precision on the canonical C^16
representation. (X1) and (X2) are imported from retained-bounded
upstream rows; this runner does not re-derive them but verifies the
bridge identities they apply to.
"""

from __future__ import annotations

import sys

try:
    import sympy
    from sympy import (
        I as sym_I,
        Matrix,
        Rational,
        Symbol,
        eye,
        log,
        simplify,
        symbols,
        zeros,
    )
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


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


def matrix_eq(A: Matrix, B: Matrix) -> bool:
    """Exact sympy matrix equality via sympy.simplify on every entry."""
    if A.shape != B.shape:
        return False
    diff = A - B
    for i in range(diff.rows):
        for j in range(diff.cols):
            if sympy.simplify(diff[i, j]) != 0:
                return False
    return True


def kron(*mats: Matrix) -> Matrix:
    """Iterated sympy Kronecker product."""
    out = mats[0]
    for m in mats[1:]:
        out = sympy.kronecker_product(out, m)
    return out


def main() -> int:
    print("=" * 88)
    print("Audit companion (exact-symbolic) for")
    print("DM_NEUTRINO_BOSONIC_NORMALIZATION_OBSERVABLE_PRINCIPLE_BRIDGE_NARROW_THEOREM_NOTE_2026-05-16")
    print("Goal: sympy verification of the bridge-selection algebra forcing")
    print("      sqrt(Tr Y^† Y / Tr Γ_1^† Γ_1) = 1/sqrt(2) on C^16")
    print("=" * 88)

    # =========================================================================
    section("Part 0: canonical (γ_5, Γ_1) representation on C^16")
    # =========================================================================
    #
    # Build the canonical Cl(1,3)-style representation mirroring the existing
    # primary runner `scripts/frontier_dm_neutrino_bosonic_normalization_theorem.py`,
    # but in sympy at exact precision.

    I2 = eye(2)
    SX = Matrix([[0, 1], [1, 0]])
    SZ = Matrix([[1, 0], [0, -1]])

    G0 = kron(SZ, SZ, SZ, SX)
    G1 = kron(SX, I2, I2, I2)
    G2 = kron(SZ, SX, I2, I2)
    G3 = kron(SZ, SZ, SX, I2)
    I16 = eye(16)

    GAMMA5 = G0 * G1 * G2 * G3
    # GAMMA5 is Hermitian and involutive and anticommutes with G0..G3.

    check(
        "G0 is Hermitian (G0 = G0^†)",
        matrix_eq(G0, G0.H),
    )
    check(
        "G1 is Hermitian",
        matrix_eq(G1, G1.H),
    )
    check(
        "G1^2 = I_{16} (Hermitian involution)",
        matrix_eq(G1 * G1, I16),
    )
    check(
        "γ_5 Hermitian",
        matrix_eq(GAMMA5, GAMMA5.H),
    )
    check(
        "γ_5^2 = I_{16}",
        matrix_eq(GAMMA5 * GAMMA5, I16),
    )
    check(
        "{γ_5, G1} = 0 (anticommutation)",
        matrix_eq(GAMMA5 * G1 + G1 * GAMMA5, zeros(16, 16)),
    )

    # Chiral projectors
    P_L = (I16 + GAMMA5) / 2
    P_R = (I16 - GAMMA5) / 2

    check(
        "P_L^2 = P_L (projector)",
        matrix_eq(P_L * P_L, P_L),
    )
    check(
        "P_R^2 = P_R (projector)",
        matrix_eq(P_R * P_R, P_R),
    )
    check(
        "P_L + P_R = I_{16}",
        matrix_eq(P_L + P_R, I16),
    )
    check(
        "P_L * P_R = 0 (orthogonal projectors)",
        matrix_eq(P_L * P_R, zeros(16, 16)),
    )
    check(
        "Tr P_L = 8 (half-rank chirality split)",
        sympy.simplify(P_L.trace() - 8) == 0,
        detail=f"Tr P_L = {sympy.simplify(P_L.trace())}",
    )
    check(
        "Tr P_R = 8",
        sympy.simplify(P_R.trace() - 8) == 0,
    )

    # =========================================================================
    section("Part 1: bridge definition Y = P_R Γ_1 P_L and identities (X3.N), (X3.H)")
    # =========================================================================

    Y = P_R * G1 * P_L
    Y_dag = Y.H

    # (X3.N): Y^2 = 0
    check(
        "(X3.N) Y^2 = 0 on C^16",
        matrix_eq(Y * Y, zeros(16, 16)),
    )

    # (X3.H): Y + Y^† = Γ_1
    check(
        "(X3.H) Y + Y^† = Γ_1 on C^16",
        matrix_eq(Y + Y_dag, G1),
    )

    # Also useful: pseudoscalar companion i(Y - Y^†)
    pseudo = sym_I * (Y - Y_dag)
    check(
        "i(Y - Y^†) is Hermitian (pseudoscalar companion)",
        matrix_eq(pseudo, pseudo.H),
    )

    # =========================================================================
    section("Part 2: trace ratios (X3.T1), (X3.T2)")
    # =========================================================================

    tr_G1G1 = sympy.simplify((G1.H * G1).trace())
    tr_YdagY = sympy.simplify((Y_dag * Y).trace())

    check(
        "(X3.T1) Tr(Γ_1^† Γ_1) = 16",
        sympy.simplify(tr_G1G1 - 16) == 0,
        detail=f"Tr(Γ_1^† Γ_1) = {tr_G1G1}",
    )
    check(
        "(X3.T2) Tr(Y^† Y) = 8",
        sympy.simplify(tr_YdagY - 8) == 0,
        detail=f"Tr(Y^† Y) = {tr_YdagY}",
    )

    # Step 6 of the proof: Y^† Y = P_L
    YdagY_mat = Y_dag * Y
    check(
        "Step 6: Y^† Y = P_L (chiral-projector identity)",
        matrix_eq(YdagY_mat, P_L),
    )

    # =========================================================================
    section("Part 3: determinant identities (DZ), (DG) symbolic in (m, j)")
    # =========================================================================

    m_sym = Symbol("m", real=True, nonzero=True)
    j_sym = Symbol("j", real=True)

    # (DZ): det(m I + j Y) = m^{16} identically in j (because Y^2 = 0 ⇒ Y is
    # nilpotent on every basis, hence eigenvalues of jY are all zero).
    det_mIjY = sympy.simplify((m_sym * I16 + j_sym * Y).det())
    check(
        "(DZ) det(m I_{16} + j Y) = m^{16} identically in j",
        sympy.simplify(det_mIjY - m_sym**16) == 0,
        detail=f"det(m I + j Y) = {det_mIjY}",
    )

    # Stronger expansion check: every j-power coefficient above j^0 vanishes.
    det_poly = sympy.expand(det_mIjY)
    poly_in_j = sympy.Poly(det_poly, j_sym)
    nonzero_coeffs_above_zero = [
        (k, c) for (k,), c in poly_in_j.as_dict().items() if k > 0 and sympy.simplify(c) != 0
    ]
    check(
        "(DZ) j-power coefficients of det(m I + j Y) above j^0 all vanish",
        len(nonzero_coeffs_above_zero) == 0,
        detail=f"nonzero higher-order coeffs: {nonzero_coeffs_above_zero}",
    )

    # (DG): det(m I + j Γ_1) = (m^2 - j^2)^8.
    det_mIjG = sympy.simplify((m_sym * I16 + j_sym * G1).det())
    target_DG = (m_sym**2 - j_sym**2) ** 8
    check(
        "(DG) det(m I_{16} + j Γ_1) = (m^2 - j^2)^8",
        sympy.simplify(det_mIjG - target_DG) == 0,
        detail=f"det form = {sympy.simplify(det_mIjG)}",
    )

    # Eigenvalue split: 8 of +1 and 8 of -1 for Γ_1.
    eigs_G1 = G1.eigenvals()
    n_plus = eigs_G1.get(sympy.Integer(1), 0)
    n_minus = eigs_G1.get(sympy.Integer(-1), 0)
    check(
        "Γ_1 has eigenvalue +1 with multiplicity 8",
        n_plus == 8,
        detail=f"multiplicities: {eigs_G1}",
    )
    check(
        "Γ_1 has eigenvalue -1 with multiplicity 8",
        n_minus == 8,
    )

    # =========================================================================
    section("Part 4: (WG) W[j Γ_1] = 8 log|1 - j^2/m^2| at exact rationals")
    # =========================================================================

    # Choose m = 1 and a few exact rational j; compare W against closed form.
    for j_val in (Rational(1, 10), Rational(1, 4), Rational(1, 3)):
        det_at = sympy.simplify(det_mIjG.subs({m_sym: 1, j_sym: j_val}))
        W_val = sympy.simplify(sympy.log(sympy.Abs(det_at)))
        target = sympy.simplify(8 * sympy.log(sympy.Abs(1 - j_val**2)))
        check(
            f"(WG) W[j Γ_1] = 8 log|1 - j^2/m^2| at (m, j) = (1, {j_val})",
            sympy.simplify(W_val - target) == 0,
            detail=f"W={W_val}, target={target}",
        )

    # And the W[j Y] = 0 identity:
    for j_val in (Rational(1, 10), Rational(1, 4), Rational(1, 3)):
        det_Y_at = sympy.simplify(det_mIjY.subs({m_sym: 1, j_sym: j_val}))
        W_Y_val = sympy.simplify(sympy.log(sympy.Abs(det_Y_at)))
        check(
            f"(WZ) W[j Y] = 0 at (m, j) = (1, {j_val})",
            sympy.simplify(W_Y_val) == 0,
            detail=f"W[jY] = {W_Y_val}",
        )

    # =========================================================================
    section("Part 5: (R) bridge ratio = 1/sqrt(2); (R1) active-space ratio = 1")
    # =========================================================================

    ratio_full = sympy.sqrt(tr_YdagY / tr_G1G1)
    target_full = 1 / sympy.sqrt(2)
    check(
        "(R) sqrt(Tr Y^† Y / Tr Γ_1^† Γ_1) = 1/sqrt(2)",
        sympy.simplify(ratio_full - target_full) == 0,
        detail=f"ratio = {sympy.simplify(ratio_full)}",
    )

    # Active-space comparator: Tr Y^† Y / Tr P_L
    tr_PL = sympy.simplify(P_L.trace())
    ratio_active = sympy.sqrt(tr_YdagY / tr_PL)
    check(
        "(R1) active-space ratio Tr Y^† Y / Tr P_L = 1 (comparator)",
        sympy.simplify(ratio_active - 1) == 0,
        detail=f"active = {sympy.simplify(ratio_active)}",
    )

    # The active-space comparator is excluded by the (X1) uniqueness on the
    # source direction Y, because W[j Y] = 0 identically (Step 5 of the proof):
    # this is the (R1) corollary — the active-space ratio is not an admissible
    # bosonic normalization because Y is in the kernel of the source-response.
    # Verified above via (WZ) at three rational j-values; we record one more
    # exact symbolic check:
    check(
        "(R1) active-space comparator non-admissible because W[j Y] ≡ 0 in j",
        len(nonzero_coeffs_above_zero) == 0,
        detail="Y is in kernel of the (X1) source-response on real-D blocks",
    )

    # =========================================================================
    section("Part 6: (R2) pseudoscalar companion algebra and orthogonality")
    # =========================================================================

    pseudo_sq = sympy.simplify((pseudo * pseudo).as_immutable())
    # (i(Y - Y^†))^2 should equal Γ_1^2 = I_{16}? Let's check what it equals.
    # (i(Y - Y^†))^2 = -1 * (Y - Y^†)^2 = -(Y^2 - Y Y^† - Y^† Y + (Y^†)^2)
    # Y^2 = 0, (Y^†)^2 = 0, so = -(-(Y Y^† + Y^† Y)) = Y Y^† + Y^† Y.
    # And Y + Y^† = Γ_1, so (Y + Y^†)^2 = Γ_1^2 = I, which expands to
    # Y^2 + Y Y^† + Y^† Y + (Y^†)^2 = Y Y^† + Y^† Y. So I = Y Y^† + Y^† Y.
    # Hence (i(Y - Y^†))^2 = I_{16}. Good — pseudoscalar is also a Hermitian
    # involution.
    check(
        "(R2.a) (i(Y - Y^†))^2 = I_{16}",
        matrix_eq(pseudo * pseudo, I16),
    )

    # Trace orthogonality of Γ_1 and pseudo: Tr(Γ_1^† * pseudo).
    tr_overlap = sympy.simplify((G1.H * pseudo).trace())
    check(
        "(R2.b) Tr(Γ_1^† · i(Y - Y^†)) = 0 (trace-orthogonality of scalar/pseudoscalar)",
        sympy.simplify(tr_overlap) == 0,
        detail=f"overlap = {tr_overlap}",
    )

    # Pseudoscalar has the same magnitude trace-norm as the scalar Γ_1:
    tr_pseudosq = sympy.simplify((pseudo.H * pseudo).trace())
    check(
        "(R2.c) Tr((i(Y - Y^†))^† · i(Y - Y^†)) = 16 (same magnitude as Γ_1)",
        sympy.simplify(tr_pseudosq - 16) == 0,
        detail=f"Tr(pseudo^† pseudo) = {tr_pseudosq}",
    )

    # =========================================================================
    section("Part 7: counterfactual — non-anticommuting Γ̃_1 breaks (X3.H)")
    # =========================================================================

    # Construct a candidate Γ̃_1 = γ_5 itself, which COMMUTES with γ_5 instead
    # of anticommuting. Then Y_tilde = P_R γ_5 P_L = P_R (P_L - P_R) P_L = 0
    # because γ_5 = P_L - P_R and P_R P_L = P_L P_R = 0.
    # So Y_tilde is identically zero on C^16; Y_tilde + Y_tilde^† = 0 ≠ γ_5
    # for γ_5 nonzero. This confirms (X3.H) requires the anticommutation.

    G1_tilde = GAMMA5  # commutes with γ_5 (in fact equals it)
    Y_tilde = P_R * G1_tilde * P_L
    check(
        "(cf.a) Γ̃_1 = γ_5 commutes with γ_5 instead of anticommuting",
        matrix_eq(GAMMA5 * G1_tilde - G1_tilde * GAMMA5, zeros(16, 16)),
    )
    check(
        "(cf.b) Y_tilde = P_R γ_5 P_L = 0 (chiral projector orthogonality)",
        matrix_eq(Y_tilde, zeros(16, 16)),
    )
    check(
        "(cf.c) (Y_tilde + Y_tilde^†) ≠ γ_5: (X3.H) breaks without anticommutation",
        not matrix_eq(Y_tilde + Y_tilde.H, GAMMA5),
        detail="confirms {γ_5, Γ_1} = 0 is load-bearing for the bridge identity",
    )

    # Also check that a different commuting candidate has trivial bridge.
    # Take Γ̃_1 = I_{16}: commutes with γ_5, but here Y_tilde = P_R I P_L = 0.
    G1_tilde2 = I16
    Y_tilde2 = P_R * G1_tilde2 * P_L
    check(
        "(cf.d) Γ̃_1 = I_{16} (commutes with γ_5) ⇒ Y_tilde = 0",
        matrix_eq(Y_tilde2, zeros(16, 16)),
    )

    # =========================================================================
    section("Part 8: cross-check — (X1) source-derivative consistency on Γ_1")
    # =========================================================================
    #
    # The (X1) uniqueness statement implies that ∂_j W[j Γ_1] at j=0 equals
    # c * d/dj [8 log|1 - j^2|] evaluated at j=0 = 0, and ∂^2_j W[j Γ_1] at j=0
    # equals c * d^2/dj^2 [8 log|1 - j^2|] at j=0 = -16. Verify symbolically.

    # Use real m = 1 for definiteness.
    W_sym = 8 * sympy.log(sympy.Abs(m_sym**2 - j_sym**2)) - 16 * sympy.log(sympy.Abs(m_sym))
    dW_dj = sympy.diff(W_sym, j_sym)
    d2W_dj2 = sympy.diff(W_sym, j_sym, 2)

    dW_at0 = sympy.simplify(dW_dj.subs({m_sym: 1, j_sym: 0}))
    d2W_at0 = sympy.simplify(d2W_dj2.subs({m_sym: 1, j_sym: 0}))

    check(
        "∂_j W[j Γ_1] at (m, j) = (1, 0) = 0 (parity)",
        sympy.simplify(dW_at0) == 0,
        detail=f"∂_j W = {dW_at0}",
    )
    check(
        "∂²_j W[j Γ_1] at (m, j) = (1, 0) = -16 (curvature consistent with (DG))",
        sympy.simplify(d2W_at0 - (-16)) == 0,
        detail=f"∂²_j W = {d2W_at0}",
    )

    # And ∂^2_j W[j Y] at j=0 = 0 because W[jY] ≡ 0:
    # (Already established by the polynomial coefficient check above.)
    check(
        "∂²_j W[j Y] at j = 0 = 0 (Y is in kernel of source-response)",
        len(nonzero_coeffs_above_zero) == 0,
        detail="follows from W[jY] ≡ 0 identically in j",
    )

    # =========================================================================
    section("Summary")
    # =========================================================================
    print("  Verified at exact sympy precision on the canonical C^16 representation:")
    print("    (X3.N) Y^2 = 0 (chiral nilpotency)")
    print("    (X3.H) Y + Y^† = Γ_1 (Hermitian completion via anticommutation)")
    print("    (X3.T1) Tr(Γ_1^† Γ_1) = 16")
    print("    (X3.T2) Tr(Y^† Y) = 8 (= Tr P_L)")
    print("    (DZ) det(m I + j Y) = m^{16} identically in j (Y nilpotent)")
    print("    (DG) det(m I + j Γ_1) = (m^2 - j^2)^8 (Hermitian involution)")
    print("    (WG) W[j Γ_1] = 8 log|1 - j^2/m^2| at exact rationals")
    print("    (WZ) W[j Y] = 0 at exact rationals")
    print("    (R)  sqrt(Tr Y^† Y / Tr Γ_1^† Γ_1) = 1/sqrt(2)")
    print("    (R1) active-space comparator = 1 is non-admissible because")
    print("         Y is in the kernel of the (X1) source-response on real-D blocks")
    print("    (R2) pseudoscalar companion is anti-Hermitian-completion partner;")
    print("         trace-orthogonal to Γ_1 and same magnitude")
    print("    Counterfactual: candidate Γ̃_1 commuting with γ_5 forces Y_tilde = 0")
    print("                     and (X3.H) breaks — anticommutation is load-bearing")
    print("    (X1) source-derivative consistency: ∂²_j W[j Γ_1]|_0 = -16, ∂²_j W[j Y]|_0 = 0")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
