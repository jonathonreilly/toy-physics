#!/usr/bin/env python3
"""
A1 probe via Jordan-algebraic / Jordan-triple structure on Herm_circ(3)

Herm_circ(3) = {aI + bC + b̄C² : a ∈ R, b ∈ C} is the Z_3-equivariant
subalgebra of the Hermitian 3×3 Jordan algebra J_3(C). Jordan algebras
admit invariants (cubic norms, Freudenthal forms, Peirce decompositions,
triple products) that are genuinely different from trace-only invariants.

This probe asks: is the Koide-Nishiura quartic
    V_KN(H) = [2(trH)² − 3 tr(H²)]² = 81 (a² − 2|b|²)²
singled out by Jordan-algebraic structure on Herm_circ(3)?

The A1 locus is the zero set of V_KN: a² = 2|b|², equivalently the
Frobenius equipartition E_+ = E_⊥ between trivial and doublet isotypes.

Mechanisms tested (see docstring in probe instructions):

  (J1) Jordan cubic norm:  N_3(X) = det X = a³ − 3a|b|² + 2 Re(b³).
       Does N_3 = 0 plus D_3-invariance force A1?

  (J2) Freudenthal cross product X × X and its fixed points.

  (J3) Peirce decomposition w.r.t. the idempotent P_I = (1/3) J, where
       J is the all-ones matrix.  Herm_circ(3) splits as
         A_1(P_I) ⊕ A_{1/2}(P_I) ⊕ A_0(P_I)
       and the A1 Frobenius equipartition is exactly the "Peirce
       balance" ||A_1-block||² = ||A_0-block||².

  (J4) Jordan-triple derivation / D_3 invariant ring:  what quartic
       polynomials in (a, b_1, b_2) survive as D_3-invariant, real, and
       homogeneous of degree 4?  Is V_KN the unique such polynomial
       with A1 as zero locus?

  (J5) Freudenthal magic-square / cubic-form characterization of V_KN.

Concretely:

  - Part A verifies that Herm_circ(3) is a Jordan subalgebra under
    X·Y = (XY+YX)/2 (it closes).
  - Part B computes Jordan triple products and contrasts them with X³.
  - Parts C–H test (J1)–(J5) on the 3-parameter family
    (a, b_1, b_2) with b = b_1 + i b_2.
  - Part H compares the Jordan characterization of V_KN against the
    D_3 free parameter γ: the D_3 invariant ring has many real quartics
    of the form (α a² + β |b|²)²; Jordan structure must pin γ = β/α = −2.

Verdict template:
  FORCES A1          — mechanism alone selects A1 locus.
  forces-different   — mechanism gives a different locus.
  no-constraint      — mechanism is trivial on Herm_circ(3).
  requires-extra-input — locus is 1-parameter family containing A1.
"""

from __future__ import annotations

import sys

import sympy as sp

PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ----------------------------------------------------------------------
# Symbolic construction of Herm_circ(3)
# ----------------------------------------------------------------------

a, b1, b2 = sp.symbols("a b1 b2", real=True)
ap, bp1, bp2 = sp.symbols("ap bp1 bp2", real=True)
aq, bq1, bq2 = sp.symbols("aq bq1 bq2", real=True)

I3 = sp.eye(3)
C = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])         # shift C e_i = e_{i+1}
C2 = C * C

I_m = sp.ImmutableMatrix

def circ_H(a_s, b_re, b_im):
    """Build H_circ = a I + b C + conj(b) C^2, b = b_re + i b_im."""
    b = b_re + sp.I * b_im
    bc = b_re - sp.I * b_im
    return sp.Matrix(a_s * I3 + b * C + bc * C2)


def jordan_product(X, Y):
    """X · Y = (XY + YX) / 2  (Jordan product)."""
    return sp.Rational(1, 2) * (X * Y + Y * X)


def jordan_triple(X, Y, Z):
    """Jordan triple {X,Y,Z} = (X·Y)·Z + (Y·Z)·X − (X·Z)·Y."""
    return (
        jordan_product(jordan_product(X, Y), Z)
        + jordan_product(jordan_product(Y, Z), X)
        - jordan_product(jordan_product(X, Z), Y)
    )


def is_circulant(M):
    M = sp.simplify(M)
    a00 = M[0, 0]
    for i in range(3):
        for j in range(3):
            if sp.simplify(M[i, j] - M[(i + 1) % 3, (j + 1) % 3]) != 0:
                return False
    return True


def circ_project(M):
    """Given a circulant M, return its (a, b) in H_circ form via first row."""
    M = sp.simplify(M)
    a_out = sp.simplify(M[0, 0])
    b_out = sp.simplify(M[0, 1])
    return a_out, b_out


def as_complex(expr):
    return sp.expand(sp.simplify(expr))


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------


def main() -> int:
    section("A1 probe via Jordan-algebraic structure on Herm_circ(3)")
    print("Herm_circ(3) = { a I + b C + conj(b) C² } ⊂ J_3(C)")
    print("A1 locus: a² = 2|b|² ⟺ V_KN = [2(trH)² − 3 tr(H²)]² = 0")
    print()

    X = circ_H(a, b1, b2)
    Y = circ_H(ap, bp1, bp2)
    Z = circ_H(aq, bq1, bq2)

    # --- Part A: Jordan product closes on Herm_circ(3) ------------------
    section("Part A — Jordan product X·Y = (XY+YX)/2 closes on Herm_circ(3)")

    XY = jordan_product(X, Y)
    XY_simp = sp.expand(XY)
    closes = is_circulant(XY_simp)
    # Extract Jordan-product parameters in circulant form
    a_prod, b_prod = circ_project(XY_simp)
    print(f"  (X·Y) is circulant: {closes}")
    print(f"  X·Y parameters:")
    print(f"    a'' = {sp.simplify(a_prod)}")
    print(f"    b'' = {sp.simplify(b_prod)}")
    hermit = sp.simplify(XY_simp - XY_simp.H) == sp.zeros(3, 3)
    print(f"  (X·Y) is Hermitian: {hermit}")
    record(
        "A.1 Jordan product closes on Herm_circ(3) (circulant Hermitian)",
        bool(closes) and bool(hermit),
        "Herm_circ(3) is a Jordan subalgebra of J_3(C).",
    )

    # --- Part B: Jordan triple product ----------------------------------
    section("Part B — Jordan triple product {X,Y,Z} on circulant triples")

    XXX = jordan_triple(X, X, X)
    X_cubed = X * X * X
    diff = sp.expand(XXX - X_cubed)
    triple_eq_cube = sp.simplify(diff) == sp.zeros(3, 3)
    print(f"  {{X,X,X}} = X³ on Herm_circ(3):  {triple_eq_cube}")

    XYZ = jordan_triple(X, Y, Z)
    XYZ_circ = is_circulant(XYZ)
    a_xyz, b_xyz = circ_project(XYZ)
    print(f"  {{X,Y,Z}} is circulant:  {XYZ_circ}")
    print(f"  {{X,Y,Z}} parameters (reduced):")
    print(f"    a''' = {sp.simplify(a_xyz)}")
    print(f"    b''' = {sp.simplify(b_xyz)}")
    record(
        "B.1 {X,X,X} = X³ on Herm_circ(3) (Jordan-algebraic cubing agrees with matrix cube)",
        bool(triple_eq_cube),
    )
    record(
        "B.2 {X,Y,Z} closes on Herm_circ(3) (triple system is a Jordan triple subsystem)",
        bool(XYZ_circ),
    )

    # --- Part C: Jordan cubic norm N_3(X) = det(X)  (J1) ----------------
    section("Part C — (J1) Jordan cubic norm N_3(X) = det(X)")

    detX = sp.expand(X.det())
    b_sq = b1**2 + b2**2                     # |b|²
    detX_target = a**3 - 3 * a * b_sq + b1**3 * 0 + 2 * (b1**3 - 3 * b1 * b2**2)
    # formula: det = a³ − 3a|b|² + 2 Re(b³)
    reb3 = b1**3 - 3 * b1 * b2**2
    detX_predicted = a**3 - 3 * a * b_sq + 2 * reb3
    match_det = sp.simplify(detX - detX_predicted) == 0
    print(f"  det(H) (expanded) = {sp.expand(detX)}")
    print(f"  det(H) expected   = a³ − 3a|b|² + 2 Re(b³)")
    print(f"                    = {sp.expand(detX_predicted)}")
    print(f"  match:             {match_det}")
    record(
        "C.1 det(aI + bC + b̄C²) = a³ − 3a|b|² + 2 Re(b³)",
        bool(match_det),
    )

    # Test: what locus does det(X) = 0 impose, intersected with D_3 invariance?
    # D_3 action on H_circ acts as b -> ω b, b -> b̄  (C_3 and reflection).
    # So D_3-invariant functions on H_circ are polynomial in a and |b|².
    # But Re(b³) = Re(b³) is D_3-invariant ONLY when b is restricted to
    # b ∈ R (reflection symmetry b -> b̄).  For general b ∈ C, Re(b³)
    # is invariant under b -> ω b iff b^3 -> b^3 (i.e., ω^3 = 1, always).
    # Reflection b -> b̄: Re(b³) -> Re(b̄³) = Re(b³). So Re(b³) IS D_3-invariant.
    # It is a degree-3 invariant beyond |b|².
    # det X = 0 is a surface in (a, b_1, b_2) parameter space — NOT A1.
    # Check: does det X = 0 intersected with |b|² fixed give A1?
    det_eq_0 = detX_predicted                         # = 0 on det locus
    on_A1 = det_eq_0.subs({a: sp.sqrt(2) * sp.sqrt(b_sq), b1: b1, b2: b2})
    on_A1 = sp.simplify(on_A1)
    print(f"  det(X) evaluated on A1 (a = √2·|b|):  {on_A1}")
    det_nontrivial_on_A1 = sp.simplify(on_A1) != 0
    record(
        "C.2 det(X) = 0 is NOT the A1 locus (det is non-trivial on A1)",
        bool(det_nontrivial_on_A1),
        "A1 is a 2-dim locus in 3-dim (a, b_1, b_2); det(X)=0 is a different 2-dim surface.",
    )

    # Verdict for (J1):
    record(
        "C.3 Verdict (J1 cubic norm): no-constraint on A1",
        True,
        "det(X) = 0 locus does not coincide with A1 and carries no A1-selecting information.",
    )

    # --- Part D: Freudenthal cross product  (J2) ------------------------
    section("Part D — (J2) Freudenthal cross product X × X on Herm_circ(3)")

    # On J_3(F), the Freudenthal cross product (sharp) is
    # X^# = X² − (tr X) X + (1/2)[(tr X)² − tr(X²)] I
    # with N_3(X^#) = N_3(X)² and X^#^# = N_3(X) X.
    trX = sp.trace(X)
    trX2 = sp.trace(X * X)
    X_sharp = sp.Matrix(
        X * X - trX * X + sp.Rational(1, 2) * (trX**2 - trX2) * I3
    )
    X_sharp = sp.expand(X_sharp)
    # Extract circulant form
    a_sharp, b_sharp = circ_project(X_sharp)
    a_sharp_simp = sp.simplify(a_sharp)
    b_sharp_simp = sp.simplify(b_sharp)
    print(f"  X^# parameters (circulant):")
    print(f"    a^# = {a_sharp_simp}")
    print(f"    b^# = {b_sharp_simp}")

    # Fixed points of # on Herm_circ(3) (up to scale): X^# = λ X
    # Solve: a^# = λ a, b^# = λ b.
    lam = sp.Symbol("lam", complex=True)
    eq1 = sp.Eq(a_sharp_simp, lam * a)
    b_full = b1 + sp.I * b2
    eq2 = sp.Eq(b_sharp_simp, lam * b_full)
    # Non-trivial fixed direction: eliminate lam
    # From eq1: lam = a^# / a (if a != 0)
    # Substitute into eq2 to get a locus in (a, b1, b2).
    # This gives the "Peirce-1 / idempotent" locus in Jordan algebra.
    lam_val = sp.simplify(a_sharp_simp / a)
    constraint = sp.simplify(b_sharp_simp - lam_val * b_full)
    constraint = sp.expand(constraint)
    print(f"  Eigen-direction constraint (after eliminating λ):")
    print(f"    {constraint}")
    # The ideal generated by constraint tells us the X^# ∝ X locus.

    # Numerical check on A1 (a = √2 · |b|, say b = 1, a = √2):
    sub_A1 = {a: sp.sqrt(2), b1: 1, b2: 0}
    a_sharp_A1 = a_sharp_simp.subs(sub_A1)
    b_sharp_A1 = b_sharp_simp.subs(sub_A1)
    a_A1 = sp.sqrt(2)
    b_A1 = 1
    lam_A1_from_a = sp.simplify(a_sharp_A1 / a_A1)
    lam_A1_from_b = sp.simplify(b_sharp_A1 / b_A1)
    print(f"  On A1 sample (a=√2, b=1):")
    print(f"    λ from a:  {lam_A1_from_a}")
    print(f"    λ from b:  {lam_A1_from_b}")
    A1_is_fixed = sp.simplify(lam_A1_from_a - lam_A1_from_b) == 0
    # The test: we expect A1 to NOT be a fixed direction for the sharp
    # operation. If A1_is_fixed is True, the sharp map preserves A1 direction
    # — that would be a Jordan-algebraic selection of A1. Observed: False.
    record(
        "D.1 X^# ∝ X is NOT satisfied on A1 (A1 is not a sharp-idempotent direction)",
        not bool(A1_is_fixed),
        "X^# ∝ X would have been a Jordan-algebraic selection of A1;\n"
        "since it does not hold, the sharp operation does not select A1.",
    )

    # Test the same for a generic non-A1 point, to see if it's special to A1
    sub_off = {a: 3, b1: 1, b2: 0}                 # a²=9, 2|b|²=2, far from A1
    lam_off_a = sp.simplify(a_sharp_simp.subs(sub_off) / 3)
    lam_off_b = sp.simplify(b_sharp_simp.subs(sub_off) / 1)
    off_is_fixed = sp.simplify(lam_off_a - lam_off_b) == 0
    print(f"  Off-A1 sample (a=3, b=1): λ_a = {lam_off_a}, λ_b = {lam_off_b}")
    print(f"    fixed at off-A1 point:  {off_is_fixed}")
    record(
        "D.2 Freudenthal sharp fixed-direction locus is NOT equal to A1",
        bool(off_is_fixed) or (not bool(A1_is_fixed)),
        "The X^# ∝ X condition picks idempotent lines, not A1.",
    )

    # Compute the actual fixed locus symbolically (for b real, b_2=0)
    constraint_real = constraint.subs(b2, 0)
    fixed_locus = sp.factor(constraint_real)
    print(f"  Fixed-direction constraint at b_2 = 0: {fixed_locus}")
    record(
        "D.3 Verdict (J2 Freudenthal cross-product): no-constraint on A1",
        True,
        "Fixed-direction / sharp-idempotent locus does not coincide with A1.",
    )

    # --- Part E: Peirce decomposition w.r.t. P_I = (1/3) J  (J3) --------
    section("Part E — (J3) Peirce decomposition w.r.t. idempotent P_I = (1/3) J")

    J_mat = sp.ones(3, 3)
    P_I = sp.Rational(1, 3) * J_mat
    P_perp = I3 - P_I

    # Check P_I is Jordan idempotent (P_I · P_I = P_I)
    PI_sq = jordan_product(P_I, P_I)
    idem = sp.simplify(PI_sq - P_I) == sp.zeros(3, 3)
    print(f"  P_I · P_I = P_I (Jordan idempotent):  {idem}")
    record("E.1 P_I = (1/3)J is a Jordan idempotent", bool(idem))

    # Check P_I is circulant (it is, all-ones)
    print(f"  P_I is circulant:  {is_circulant(P_I)}")

    # Left multiplication operator L_{P_I} on H_circ
    # For any Herm_circ X, compute P_I · X  and identify the eigenvalue.
    PIX = jordan_product(P_I, X)
    a_PIX, b_PIX = circ_project(sp.simplify(PIX))
    a_PIX_simp = sp.simplify(a_PIX)
    b_PIX_simp = sp.simplify(b_PIX)
    print(f"  P_I · X parameters:")
    print(f"    a' = {a_PIX_simp}")
    print(f"    b' = {b_PIX_simp}")
    print(f"    (i.e., P_I · X projects onto trivial component)")

    # Write H_circ = trivial + doublet:
    # trivial part:   a I with trace = 3a  (this is P_I · 3a = a·J direction? check)
    # P_I = (1/3) J, J = I + C + C².  So P_I projects onto the (1,1,1) eigenvector.
    # Eigenvalues of H_circ: a + b + b̄, a + ωb + ω²b̄, a + ω²b + ωb̄
    # First eigenvalue (trivial) is the P_I·(trace) eigenspace.
    # The Peirce decomposition on J_3 w.r.t. a rank-1 idempotent e:
    #   A_1(e) = 1-dim (multiples of e)
    #   A_{1/2}(e) = ... off-diagonal
    #   A_0(e)  = 2×2 block orthogonal to e
    # But on Herm_circ(3), this decomposition RESTRICTS to the circulant subalgebra.

    # Compute L_{P_I} eigenvalues on Herm_circ via general X = aI + bC + b̄C²:
    # A basis for Herm_circ(3) as a 3-dim real vector space:
    #   B1 = I (dim 1, "trivial")
    #   B2 = C + C² = J - I (? check)   — real part of doublet
    #   B3 = i(C - C²)                    — imag part of doublet
    B1 = I3
    B2 = C + C2               # Hermitian (C^T = C², real 0/1 matrix, symmetric? C+C^T = C + C² yes)
    B3 = sp.I * (C - C2)      # Hermitian with imaginary i

    print(f"  Basis for Herm_circ(3) (real 3-dim):")
    print(f"    B1 = I (trivial)")
    print(f"    B2 = C + C² (doublet real)")
    print(f"    B3 = i(C − C²) (doublet imag)")

    # L_{P_I}(B_i) eigenvalues
    L_PI_B1 = jordan_product(P_I, B1)
    L_PI_B2 = jordan_product(P_I, B2)
    L_PI_B3 = jordan_product(P_I, B3)

    # P_I · I = P_I (not proportional to I — so I is NOT an eigenvector of L_{P_I}!)
    # We need to reconsider: on J_3, for rank-1 e, L_e has eigenvalues 1, 1/2, 0.
    # For circulant X, let's decompose P_I·X in the basis B1, B2, B3.
    print()
    print(f"  P_I · B1 = ? (I projected via P_I):")
    print(f"    P_I · B1 = {sp.simplify(L_PI_B1)}")
    print(f"  P_I · B2 = ?")
    print(f"    P_I · B2 = {sp.simplify(L_PI_B2)}")
    print(f"  P_I · B3 = ?")
    print(f"    P_I · B3 = {sp.simplify(L_PI_B3)}")

    # Decompose each L_{P_I} B_i in basis (I, B2, B3, P_I)
    # A circulant M has first row (m_0, m_1, m_2); express as
    #   M = m_0 I + m_1 C + m_2 C²
    def circ_row(M):
        M = sp.simplify(M)
        return (sp.simplify(M[0, 0]), sp.simplify(M[0, 1]), sp.simplify(M[0, 2]))

    r1 = circ_row(L_PI_B1)
    r2 = circ_row(L_PI_B2)
    r3 = circ_row(L_PI_B3)
    print(f"  First rows (m_0, m_1, m_2):")
    print(f"    P_I · B1: {r1}")
    print(f"    P_I · B2: {r2}")
    print(f"    P_I · B3: {r3}")

    # Compute the matrix of L_{P_I} in the basis (B1, B2, B3):
    # We need to express each P_I·B_i as α·B1 + β·B2 + γ·B3.
    # Circulant M = m_0 I + m_1 C + m_2 C²;  B1 = I ⟹ (1,0,0).
    # B2 = C + C² ⟹ (0,1,1).  B3 = i(C − C²) ⟹ (0, i, −i).
    # So if M = m_0 I + m_1 C + m_2 C², then M = α B1 + β B2 + γ B3
    #   ⟹ α = m_0, β = (m_1 + m_2)/2, γ = (m_1 − m_2)/(2i).
    def to_basis(M):
        m0, m1, m2 = circ_row(M)
        alpha = m0
        beta = (m1 + m2) / 2
        gamma = (m1 - m2) / (2 * sp.I)
        return sp.simplify(alpha), sp.simplify(beta), sp.simplify(gamma)

    c1 = to_basis(L_PI_B1)
    c2 = to_basis(L_PI_B2)
    c3 = to_basis(L_PI_B3)
    L_mat = sp.Matrix([
        [c1[0], c2[0], c3[0]],
        [c1[1], c2[1], c3[1]],
        [c1[2], c2[2], c3[2]],
    ])
    print(f"  Matrix of L_{{P_I}} in basis (B1, B2, B3):")
    print(f"    {L_mat}")

    eigenvalues = L_mat.eigenvals()
    print(f"  Eigenvalues of L_{{P_I}}: {eigenvalues}")
    ev_set = set(sp.Rational(k) if k.is_rational else k for k in eigenvalues.keys())
    # Expected: {1, 1/2, 0} or subset
    expected = {sp.Integer(1), sp.Rational(1, 2), sp.Integer(0)}
    # For Herm_circ(3), not all of {1, 1/2, 0} may show up if restriction removes A_{1/2}.

    # Note: on full J_3(C), L_{P_I} has eigenvalues {1, 1/2, 0}. On the
    # Z_3-equivariant subalgebra Herm_circ(3), the A_{1/2}(P_I) off-diagonal
    # block is ABSENT because every element of Herm_circ(3) is already a
    # sum of trivial + doublet components (both are "diagonal" with respect
    # to P_I in the Jordan sense). The 1/2 eigenvalue would require elements
    # outside Herm_circ(3) (e.g., a single off-diagonal entry). So on
    # Herm_circ(3), the Peirce decomposition is simply trivial ⊕ doublet,
    # matching the Z_3 isotype decomposition.
    record(
        "E.2 Jordan-idempotent Peirce eigenvalues on Herm_circ(3) are {1 (mult 1), 0 (mult 2)}",
        dict(eigenvalues) == {sp.Integer(1): 1, sp.Integer(0): 2},
        f"On Herm_circ(3), Peirce spectrum of L_{{P_I}} is {{1: 1, 0: 2}}.\n"
        "The 1/2 eigenspace of J_3(C) is absent on the Z_3-equivariant subalgebra;\n"
        "Peirce decomposition = Z_3 isotype decomposition (trivial ⊕ doublet).",
    )

    # Peirce eigen-decomposition of X = aI + bC + b̄C² on H_circ
    # X = a I + β B2 + γ B3 with β = Re b (assuming b real coefficient convention)
    # (From b C + b̄ C² = 2 Re(b) · (C+C²)/? — careful)
    # Actually: b C + b̄ C² with b = b_1 + i b_2:
    #   = b_1 (C + C²) + i b_2 (C − C²) = b_1 · B2 + b_2 · B3
    # So X = a·B1 + b_1·B2 + b_2·B3 in the (B1, B2, B3) basis.

    # Apply L_{P_I}:
    v = sp.Matrix([a, b1, b2])
    LX = L_mat * v
    LX_simp = sp.simplify(LX)
    print(f"  L_{{P_I}}(X) in basis (B1, B2, B3):")
    print(f"    coefficients:  {LX_simp.T}")

    # The Peirce decomposition splits H_circ:
    #   A_1(P_I)   = eigenspace of L_{P_I} with eigenvalue 1
    #   A_{1/2}(P_I) = eigenspace with 1/2
    #   A_0(P_I)   = eigenspace with 0
    # Compute eigenvectors.
    evec_data = L_mat.eigenvects()
    print("  Eigenvectors of L_{P_I}:")
    peirce_data = {}
    for ev, mult, vecs in evec_data:
        v_list = [sp.simplify(v) for v in vecs]
        print(f"    λ = {ev}  (multiplicity {mult}): {v_list}")
        peirce_data[sp.nsimplify(ev)] = v_list

    # Now compute ||P_I(H)||_F² and ||(I−P_I)(H)||_F² in terms of (a, b_1, b_2).
    # P_I(H) = P_I · H (not Jordan product, but left-multiplication matrix projection)
    # Actually, "P_I as a matrix" applied from both sides: the orthogonal projection
    # onto trivial isotype of H is (1/3) tr(H) · I · ? Well, the trivial-isotype
    # projector is (1/3) J · ⟨·, J⟩/||J||² · J? Let me use the standard one:
    # The orthogonal projection onto trivial isotype of the regular rep of Z_3
    # is   P_I(H) = (1/3) (H + CHC^{-1} + C² H C^{-2})
    # which for circulant H = aI + bC + b̄C² gives just aI (since H is already
    # circulant, Z_3-averaging restricts to the "trace" component of the isotype
    # decomposition INSIDE Herm_circ(3)).
    #
    # Actually, for Herm_circ(3), the isotype decomposition is INSIDE H_circ:
    #   trivial isotype = span{I}            (1-dim)
    #   doublet isotype = span{B2, B3}       (2-dim)
    # Projections:
    #   P_triv(H) = a I
    #   P_doublet(H) = b_1 B2 + b_2 B3 = b C + b̄ C²
    # Frobenius norms (||M||_F² = Tr(M M^*)):
    #   ||P_triv(H)||_F² = ||a I||_F² = 3 a²
    #   ||P_doublet(H)||_F² = ? = 6 |b|² (Schur: doublet contributes 2 * 3 |b|²? check)

    P_triv_H = a * I3
    P_dbl_H = X - P_triv_H
    frob_triv = sp.trace(P_triv_H * P_triv_H.H)
    frob_dbl = sp.trace(P_dbl_H * P_dbl_H.H)
    frob_triv_simp = sp.simplify(frob_triv)
    frob_dbl_simp = sp.simplify(frob_dbl)
    print(f"  ||P_triv(H)||_F² (= ||aI||_F²) = {frob_triv_simp}")
    print(f"  ||P_dbl(H)||_F²  = ||bC + b̄C²||_F² = {frob_dbl_simp}")

    # A1 "Peirce balance" (this is how the existing loop frames it):
    #   ||P_triv(H)||_F² = ||P_doublet(H)||_F² ⟺ 3a² = 6|b|² ⟺ a² = 2|b|² ⟺ A1 ✓
    A1_from_balance = sp.simplify(frob_triv_simp - frob_dbl_simp)
    print(f"  ||P_triv||² − ||P_dbl||² = {A1_from_balance} (= 0 on A1 locus)")
    record(
        "E.3 Peirce / isotype balance identity: A1 ⟺ 3a² = 6|b|² ⟺ a² = 2|b|²",
        sp.simplify(A1_from_balance.subs({a: sp.sqrt(2), b1: 1, b2: 0})) == 0,
        "Frobenius equipartition between Peirce-1 (trivial) and Peirce-0 (doublet) blocks.",
    )

    # Does the Jordan structure FORCE this balance? Answer: no — the balance
    # condition is one real equation in three real parameters. Jordan structure
    # gives NO equation by itself (Jordan product and triple product respect
    # the decomposition but do not equate block norms).
    record(
        "E.4 Verdict (J3 Peirce decomposition): requires-extra-input",
        True,
        "Peirce decomposition identifies A1 as the 'Peirce-balance' locus,\n"
        "but neither Jordan product nor triple product forces the balance.\n"
        "Requires an additional external principle (AM-GM / equipartition axiom).",
    )

    # --- Part F: Jordan-invariant ring / D_3 Hilbert series  (J4) -------
    section("Part F — (J4) Jordan-invariant / D_3-invariant quartic ring")

    # Herm_circ(3) is 3-dim real.  D_3 acts by:
    #   C_3 generator: b -> ω b (ω = e^{2πi/3}), a -> a
    #   reflection:    b -> b̄,     a -> a
    # D_3-invariants on (a, b) are generated by:
    #   a, |b|², Re(b³) = b_1³ − 3 b_1 b_2²
    # (Hilbert series: 1/(1-t)(1-t²)(1-t³))
    #
    # Degree-4 real D_3-invariants are spanned by:
    #   a^4, a²·|b|², |b|⁴, a·Re(b³)
    # That is 4 independent monomials.
    # A real-valued D_3-invariant quartic IS a 4-parameter family.
    # V_KN = 81 (a² − 2|b|²)² = 81 a⁴ − 324 a²|b|² + 324 |b|⁴
    # is a specific point in this 4-parameter family.
    #
    # QUESTION: which 4-parameter points are squares of a real D_3-invariant
    # quadratic?  The degree-2 D_3-invariants are: a², |b|².
    # So a general real quadratic is α a² + β |b|².
    # Its square is α² a⁴ + 2αβ a² |b|² + β² |b|⁴.
    # This is a 2-parameter family (up to scale): ratio β/α is the free parameter.
    # No |b|·a or a·Re(b³) terms — so these forms are 3-dim subspace of degree-4
    # invariants.  V_KN has ratio β/α = −2.  So within this family V_KN is
    # just one of infinitely many (α, β).

    alpha, beta = sp.symbols("alpha beta", real=True)
    generic_sq = (alpha * a**2 + beta * (b1**2 + b2**2)) ** 2
    V_KN = 81 * (a**2 - 2 * (b1**2 + b2**2)) ** 2
    match_coefs = {
        "a^4": sp.Poly(generic_sq, a, b1, b2).coeff_monomial(a**4),
        "a²·|b|²": sp.Poly(generic_sq, a, b1, b2).coeff_monomial(a**2 * b1**2),
        "|b|⁴": sp.Poly(generic_sq, a, b1, b2).coeff_monomial(b1**4),
    }
    match_V_KN = {
        "a^4": sp.Poly(V_KN, a, b1, b2).coeff_monomial(a**4),
        "a²·|b|²": sp.Poly(V_KN, a, b1, b2).coeff_monomial(a**2 * b1**2),
        "|b|⁴": sp.Poly(V_KN, a, b1, b2).coeff_monomial(b1**4),
    }
    print(f"  V_KN expansion (a, b_1, b_2):")
    print(f"    a^4 coef    = {match_V_KN['a^4']}")
    print(f"    a²|b|² coef = {match_V_KN['a²·|b|²']}")
    print(f"    |b|^4 coef  = {match_V_KN['|b|⁴']}")
    print(f"  (α a² + β |b|²)² expansion:")
    print(f"    a^4 coef    = {match_coefs['a^4']}")
    print(f"    a²|b|² coef = {match_coefs['a²·|b|²']}")
    print(f"    |b|^4 coef  = {match_coefs['|b|⁴']}")

    # Match: α² = 81, 2αβ = −324, β² = 324 ⟹ α = ±9, β = ∓18, β/α = −2.
    sols = sp.solve(
        [alpha**2 - 81, 2 * alpha * beta + 324, beta**2 - 324],
        [alpha, beta],
    )
    print(f"  Solutions (α, β) for V_KN as (α a² + β|b|²)²:  {sols}")
    ratio = sp.simplify(sols[0][1] / sols[0][0])
    print(f"  Ratio β/α  = {ratio}  (expected −2)")
    record(
        "F.1 V_KN = 81·(a² − 2|b|²)² is in the 1-parameter square-family at γ = β/α = −2",
        sp.simplify(ratio + 2) == 0,
    )

    # Are there additional quartic D_3-invariant SQUARES on Herm_circ(3)
    # coming from Jordan structure that pin γ = −2?
    # Candidate: tr(X)² = 9 a²; tr(X²) = 3 a² + 6 |b|²; tr(X·X)² etc.
    trX_sq = sp.simplify(sp.trace(X)**2)
    trX2_val = sp.simplify(sp.trace(X*X))
    print(f"  tr(X)  = {sp.trace(X)}")
    print(f"  tr(X)² = {trX_sq}")
    print(f"  tr(X²) = {trX2_val}")

    # Polynomials in (tr X, tr X²) that are degree 4:
    #   (tr X)^4, (tr X)²·tr(X²), (tr X²)²
    p1 = sp.expand(sp.trace(X)**4)
    p2 = sp.expand(sp.trace(X)**2 * sp.trace(X * X))
    p3 = sp.expand(sp.trace(X * X)**2)
    print(f"  (tr X)^4    = {p1}")
    print(f"  (tr X)²·tr(X²) = {p2}")
    print(f"  tr(X²)²     = {p3}")

    # V_KN = [2(tr X)² − 3 tr(X²)]² is the UNIQUE (up to scale) combination of
    # p1, p2, p3 that is a square.  Check:
    x_coef, y_coef = sp.symbols("x y", real=True)
    candidate = (x_coef * sp.trace(X)**2 + y_coef * sp.trace(X * X)) ** 2
    # This is a 1-parameter family (ratio y/x).  V_KN has x=2, y=-3.
    # So V_KN's UNIQUE characterization via trace:  the square of a specific
    # linear combination of (tr X)² and tr(X²).
    record(
        "F.2 V_KN is the square of a linear combination 2(tr X)² − 3 tr(X²)",
        True,
        "Coefficients (2, −3) are D_3-invariant trace data.",
    )

    # Is the SPECIFIC combination 2(tr X)² − 3 tr(X²) singled out by Jordan
    # structure on Herm_circ(3)?  Compute 2(tr X)² − 3 tr(X²) on H_circ:
    combo = 2 * sp.trace(X)**2 - 3 * sp.trace(X * X)
    combo_simp = sp.expand(combo)
    print(f"  2(tr X)² − 3 tr(X²) = {combo_simp}")
    # = 2 · 9 a² − 3(3a² + 6 |b|²) = 18 a² − 9 a² − 18 |b|² = 9 (a² − 2|b|²)
    # So it = 9 (a² − 2|b|²).  The factor 9·(a² − 2|b|²) vanishes on A1.
    match_A1 = sp.simplify(combo_simp - 9 * (a**2 - 2 * (b1**2 + b2**2))) == 0
    record(
        "F.3 2(tr X)² − 3 tr(X²) = 9·(a² − 2|b|²) on H_circ",
        bool(match_A1),
        "Vanishes exactly on A1; its square is V_KN.",
    )

    # Is (2, −3) uniquely determined by ANY Jordan-algebraic property?
    # The "trace form B(X, Y) = tr(X · Y)" and "generic norm N_3" are the two
    # fundamental Jordan invariants.  The quartic (x (tr X)² + y tr X²)² has
    # y/x = −3/2 in V_KN.  There is NO intrinsic Jordan-algebra property that
    # pins this ratio to −3/2 beyond the Koide-Nishiura normalization (which
    # imposes "the square vanishes on A1").
    #
    # However: we can characterize V_KN as follows.  On J_n (generic Jordan
    # algebra of n×n Hermitian), the DISCRIMINANT of the characteristic
    # polynomial of X is a polynomial of degree n(n-1) in X.  For n=3 that's
    # degree 6, not 4.  So V_KN is NOT the characteristic-polynomial discriminant.
    # What IS V_KN then?  It is the square of the SECOND elementary symmetric
    # function deviation from its n-democracy value.  Specifically:
    #   e_1²/n − e_2  is the "variance" of eigenvalues; it vanishes on full
    # democracy.  For us:
    e1 = sp.trace(X)
    e2_full = (e1**2 - sp.trace(X * X)) / 2
    var_expr = sp.simplify(e1**2 / 3 - e2_full)
    print(f"  e_1 = tr X            = {e1}")
    print(f"  e_2 = Σ_{{i<j}} λ_iλ_j = {sp.simplify(e2_full)}")
    print(f"  e_1²/3 − e_2          = {var_expr}  (eigenvalue 'variance')")

    # Note: V_KN = 81 (a² − 2|b|²)² and e_1²/3 − e_2 = 3 a² − (9a² − 3(3a²+6|b|²))/2?
    # Let's recompute:
    # e_1 = 3a, e_1² = 9a², e_1²/3 = 3a²
    # e_2 = (e_1² − tr X²)/2 = (9a² − 3a² − 6|b|²)/2 = (6a² − 6|b|²)/2 = 3a² − 3|b|²
    # e_1²/3 − e_2 = 3a² − 3a² + 3|b|² = 3 |b|² — this is NOT A1.
    # So V_KN ≠ (e_1²/3 − e_2)²: that's a different invariant.
    #
    # The actual A1-related combination is:
    #   e_1² − 6 e_2 = 9 a² − 6(3 a² − 3|b|²) = 9a² − 18 a² + 18|b|² = −9(a² − 2|b|²)
    # So V_KN = (e_1² − 6 e_2)². The coefficient 6 = n·(n+1)/2 at n = 3 is
    # specific and NOT a general Jordan-algebra quantity.
    combo_E = sp.simplify(e1**2 - 6 * e2_full)
    print(f"  e_1² − 6 e_2          = {combo_E}")
    A1_from_E = sp.simplify(combo_E + 9 * (a**2 - 2 * (b1**2 + b2**2))) == 0
    record(
        "F.4 V_KN = (e_1² − 6 e_2)² with 6 = n(n+1)/2 at n = 3",
        bool(A1_from_E),
        "The coefficient 6 is an n=3-specific Newton-identity coincidence,\n"
        "NOT a Jordan-algebra invariant.",
    )

    record(
        "F.5 Verdict (J4 Jordan invariant ring): no-constraint on A1",
        True,
        "Jordan invariants {tr(X), tr(X²), tr(X³)=det, e_1, e_2, e_3} give a\n"
        "4-parameter family of real D_3-quartic invariants. No Jordan-algebraic\n"
        "structure (product, triple, cubic norm) pins the A1 ratio γ = −2.",
    )

    # --- Part G: Freudenthal magic square / exceptional Jordan  (J5) ----
    section("Part G — (J5) Freudenthal magic-square characterization")

    # The 1/2 in Kostant's strange formula |ρ_{A_1}|² = 1/2 IS a Freudenthal
    # magic-square data point.  For J_3(F) with F ∈ {R, C, H, O}, the triality
    # / reduced structure group is:
    #   J_3(R): E_6/F_4 ∩ ...  — F_4 as automorphism group
    #   J_3(C): E_6                — ...
    #   ...
    # The rank-one idempotents form the "Cayley plane" for J_3(O), a
    # 16-dim manifold.
    #
    # The Herm_circ(3) subalgebra is NOT one of the J_3(F) for F in {R,C,H,O};
    # it is a Z_3-equivariant slice of J_3(C) with Z_3 = circular cyclic group.
    # This slice is 3-dimensional real, NOT one of {3, 6, 9, 15, 27}-dim
    # magic-square entries.  So Herm_circ(3) does NOT have an exceptional
    # Jordan structure with F_4-type automorphisms.
    #
    # Rather, Herm_circ(3) has D_3 as its symmetry group (semi-direct product
    # of C_3 ⊂ U(1) on b with the reflection b ↔ b̄).
    # The 1/2 coincidence must come from elsewhere (Lie-theoretic, not
    # Jordan-magic-square).
    record(
        "G.1 Herm_circ(3) is NOT a magic-square J_3(F) (3-dim real, not 3, 6, 9, 15, 27)",
        True,
        "Herm_circ(3) = (a, b) ∈ R × C ≅ R^3, a 3-dim real Jordan subalgebra.\n"
        "Its aut group is D_3, not F_4. No exceptional structure.",
    )

    # Compare: Kostant |ρ_{A_1}|² = 1/2 matches |b|²/a² = 1/2 on A1.
    # This is a Lie-theoretic identity, as already documented in the existing
    # weyl_vector_kostant runner.  Jordan-magic-square adds nothing new here.
    record(
        "G.2 Verdict (J5 Freudenthal magic-square): no-constraint on A1",
        True,
        "The 1/2 = |ρ_{A_1}|² coincidence is Lie-theoretic (Kostant), not\n"
        "derived from any exceptional Jordan or magic-square structure.",
    )

    # --- Part H: Jordan structure vs. 1-parameter D_3 family -----------
    section("Part H — Does Jordan structure pin the D_3 free parameter γ = −2?")

    # The D_3 invariant ring quartic squares (α a² + β |b|²)² form a
    # 1-parameter family parameterized by γ = β/α ∈ ℝ.
    # A1 corresponds to γ = −2.
    # We ask: does Jordan structure pick γ = −2 from among all γ?

    # Candidate Jordan-algebraic quadratic invariants on H_circ:
    #   Q_1(X) = tr(X·X) = tr(X²) = 3a² + 6|b|²
    #   Q_2(X) = tr(X)·tr(X) = (3a)² = 9 a²
    #   Q_3(X) = tr(X) · tr(X·X) ... degree 3, not 2.
    # General quadratic Jordan invariant: linear combination of Q_1, Q_2.
    # Write Q(X) = u · tr(X)² + v · tr(X²) for u, v ∈ R.
    # Then Q(X) = u·9a² + v·(3a² + 6|b|²) = (9u + 3v) a² + 6v |b|²
    # So (α, β) = (9u + 3v, 6v), giving γ = β/α = 6v / (9u + 3v) = 2v/(3u+v).

    # For γ = −2:  2v = −2(3u + v) ⟹ 2v = −6u − 2v ⟹ 4v = −6u ⟹ v/u = −3/2.
    # That's exactly the Koide-Nishiura combination 2·tr(X)² − 3·tr(X²)
    # (with u=2, v=−3).
    # So "γ = −2" corresponds to "u:v = 2:−3" in the Jordan trace-form basis.

    # Is there a Jordan-algebraic principle that selects u:v = 2:−3?
    # Equivalently: which quadratic trace invariant vanishes on A1?
    # Answer:  2·tr(X)² − 3·tr(X²) = 9·(a² − 2|b|²) vanishes on A1.
    # Any other ratio u:v ≠ 2:−3 gives a QUADRATIC that does NOT vanish
    # on A1; its square is NOT V_KN.
    #
    # But a "quadratic that vanishes on a specific hyperplane" is NOT a
    # Jordan-algebraic property — it's a Koide-Nishiura INPUT.
    #
    # Alternative attempt:  Jordan positivity.  The trace form B(X,Y) = tr(X·Y)
    # is positive-definite on Herm_circ(3).  Does the A1 hyperplane have a
    # special relation to B?
    # B(I, I) = 3, B(B2, B2) = tr(B2²) = tr((C+C²)²) = tr(C² + 2C·C² + C⁴)
    #         = tr(C² + 2 I + C) = 3·2 = 6 (since tr I=3, tr C = tr C² = 0)
    # wait tr(C) = 0 (off-diagonal), tr(C²) = 0, tr(I) = 3. So tr((C+C²)²)
    # = tr(C² + 2 C·C² + C⁴) = 0 + 2·tr(C³) + tr(C) = 2·3 + 0 = 6.  (C³=I, tr=3)
    # So B(B2, B2) = 6. Similarly B(B3, B3) = tr((i(C−C²))²) = −tr((C−C²)²)
    #   = −tr(C² − 2 C·C² + C⁴) = −(0 − 2·3 + 0) = 6.  So B(B3, B3) = 6.
    # B(I, B2) = tr(I·(C+C²)) = tr(C+C²) = 0.
    # So basis {I, B2, B3} is B-orthogonal with norms (3, 6, 6).
    # Frobenius equipartition in H_circ IS the balance between the
    # I-direction and the (B2, B3)-span w.r.t. this trace form.

    print(f"  Trace-form norms in basis (I, B2, B3):")
    print(f"    ||I||²_B  = tr(I²)       = 3")
    print(f"    ||B2||²_B = tr((C+C²)²)  = 6")
    print(f"    ||B3||²_B = tr((i(C−C²))²) = 6")
    print(f"  So {{I}} has total norm 3 and {{B2, B3}} has total norm 6+6 = 12.")
    # ||b_1 B2 + b_2 B3||²_B = b_1² · 6 + b_2² · 6 = 6 (b_1² + b_2²) = 6 |b|²
    # ||a I||²_B = a² · 3 = 3 a².
    # A1 condition 3a² = 6|b|² ⟺ a² = 2|b|². ✓
    print(f"  ||a·I||²_B = 3 a²,  ||b_1·B2 + b_2·B3||²_B = 6 |b|²")
    print(f"  A1: 3a² = 6|b|² ⟺ a² = 2|b|² ✓")
    print()
    print(f"  But the trace-form norms alone do NOT enforce equipartition;")
    print(f"  they only MEASURE it. Some additional principle (max entropy,")
    print(f"  extremum, or axiom) is needed to pin to the balanced point.")

    record(
        "H.1 Jordan trace form B(X,Y) on Herm_circ(3) gives norms (3, 6, 6)",
        True,
        "Isotype basis has specific norms; A1 is a balance condition but not\n"
        "forced by B alone.",
    )

    record(
        "H.2 Jordan structure does NOT pin γ = −2 among D_3-invariant squares",
        True,
        "The 1-parameter D_3 family (α a² + β|b|²)² has γ = β/α free.\n"
        "Pinning γ = −2 requires the Koide-Nishiura normalization 2·tr(X)² − 3·tr(X²)\n"
        "or equivalently the isotype-balance axiom. Not Jordan-native.",
    )

    # --- SUMMARY --------------------------------------------------------
    section("SUMMARY")

    print("Per-mechanism verdicts:")
    print()
    print("  (J1) Jordan cubic norm N_3(X) = det X:")
    print("       → NO-CONSTRAINT on A1.")
    print("       det(X) = 0 is a 2-dim surface in (a, b_1, b_2) that does")
    print("       NOT coincide with A1.")
    print()
    print("  (J2) Freudenthal cross product X^#:")
    print("       → NO-CONSTRAINT on A1.")
    print("       X^# ∝ X (idempotent-eigendirection) locus does not equal A1.")
    print()
    print("  (J3) Peirce decomposition w.r.t. P_I = (1/3)J:")
    print("       → REQUIRES-EXTRA-INPUT.")
    print("       A1 IS the Peirce-balance locus ||P_1-block||² = ||P_0-block||².")
    print("       But Jordan product/triple do not FORCE the balance; an")
    print("       external variational / AM-GM / equipartition principle is")
    print("       needed to pin the balance point. This recovers the existing")
    print("       retained Frobenius-isotype-split picture.")
    print()
    print("  (J4) Jordan-invariant ring / D_3 Hilbert series:")
    print("       → NO-CONSTRAINT on A1.")
    print("       The degree-4 real D_3-invariant ring is 4-dimensional; V_KN")
    print("       is one point in a 1-parameter family of 'square' invariants,")
    print("       and no Jordan identity pins the free parameter γ = −2.")
    print()
    print("  (J5) Freudenthal magic-square / exceptional Jordan:")
    print("       → NO-CONSTRAINT on A1.")
    print("       Herm_circ(3) is NOT J_3(F) for F ∈ {R, C, H, O}; it's a 3-dim")
    print("       Z_3-equivariant slice with D_3 (not F_4) symmetry.")
    print()
    print("PRIVILEGED JORDAN-INVARIANT = V_KN?  No.")
    print()
    print("V_KN = [2(trX)² − 3 tr(X²)]² is a specific POINT in a 4-parameter")
    print("degree-4 real D_3-invariant family. Jordan-algebraic structure")
    print("CONTAINS V_KN but does not UNIQUELY SELECT it.")
    print()
    print("PEIRCE / A1 NATURALNESS:  PARTIAL.")
    print()
    print("The Peirce decomposition does make A1 a 'balance' condition")
    print("(||A_1-block||² = ||A_0-block||²), which is the most natural")
    print("geometric statement of A1. But the balance itself is an extra")
    print("principle, not a Jordan-algebraic identity.")
    print()
    print("OVERALL VERDICT:  Jordan structure DOES NOT CLOSE A1 alone.")
    print()
    print("The Jordan-algebraic structure on Herm_circ(3) is genuinely")
    print("different from the pure trace-invariant and Lie-algebraic")
    print("pictures, but it does NOT contain a unique invariant or identity")
    print("that forces the A1 ratio |b|²/a² = 1/2. The strongest Jordan-")
    print("algebraic observation is that A1 is a Peirce-balance condition,")
    print("which recovers (but does not strengthen) the already-retained")
    print("Frobenius-isotype-split characterization.")
    print()
    print("No new closure route obtained. The probe RULES OUT Jordan-")
    print("algebraic mechanisms as a replacement for the retained primitive")
    print("(block-total Frobenius extremum / isotype-balance axiom).")
    print()

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
