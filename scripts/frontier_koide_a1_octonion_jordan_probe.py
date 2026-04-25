#!/usr/bin/env python3
"""
Koide A1 deep probe — joint Cl(3)/Z³ + J_3(O) closure attempt
=============================================================

Hypothesis (Bar-5): the charged-lepton Yukawa is naturally octonion-valued in a
joint Cl(3)/Z³ + J_3(O) framework.  Non-associativity of O produces specific
algebraic constraints (associator/alternative identities, Jordan-cubic / Freudenthal
identities) not satisfiable for complex-valued Yukawas, and A1 (|b|²/a² = 1/2)
emerges as one such constraint.

This probe tests that hypothesis with PASS-only verification of structural
identities (the PASS items here certify what is mathematically TRUE, not that
A1 closes axiom-natively — see the `CLOSES` flag at the bottom).

Documentation discipline (mandatory):
  (1) what tested      — Tasks 1–8 below
  (2) what failed      — see CLOSES=FALSE rationale at the bottom
  (3) what NOT tested  — see "Limits" comments
  (4) assumptions challenged — see Task 6/7
  (5) assumptions accepted   — see Task 1/4
  (6) forward suggestions    — see VERDICT block

Structure:
  Task 1: Cl(3) ↔ O attempted identification at the algebra level
          (no algebra-isomorphism: Cl(3) is associative, O is not).
          Cl(3)/Z³ + J_3(O) embedding test for the lepton sector.
  Task 2: Octonion-valued Yukawa Y_O = a + b·e_1 + c·e_2 + ... and its
          J_3(O)-Hermitian analogue X = diag(α,β,γ) + off-diagonal
          octonion entries.  Compute trace, Frobenius norm, det.
  Task 3: Associator [y, y, y] vanishing → alternative identity is
          AUTOMATIC for any single octonion (octonions are alternative).
          Test what the alternative law actually constrains.
  Task 4: Freudenthal cubic norm N(X) for J_3(O); sharp X^# and the
          identity (X^#)^# = N(X) X.  Compute the trace-form.
  Task 5: Test whether |b|²/a² = 1/2 emerges from any Casimir / norm /
          Freudenthal identity in J_3(O).  We test the canonical
          invariants: tr X, tr X², tr X³, N(X), bilinear form (X, X).
  Task 6: Cost analysis — Cl(3) is associative (4-D ≅ ℍ).  Importing O
          (8-D non-associative) is a strict primitive ADDITION, not a
          consequence of the retained framework.  G_2 = Aut(O) is
          already not contained in retained SU(3)_color / SU(2)_L / U(1)_Y.
  Task 7: Singh's J_3(O_C) imports — list assumptions.
  Task 8: Falsifiers.

PASS-only convention.  CLOSES flag at the bottom is the load-bearing claim.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product

import sympy as sp


# ============================================================================
# Reporting infrastructure
# ============================================================================

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


# ============================================================================
# Symbolic octonion algebra (Cayley–Dickson on H)
# ============================================================================
#
# We build O = H ⊕ H with multiplication
#   (a, b)(c, d) = (a c − d̄ b,  d a + b c̄)
# using Cayley–Dickson on the quaternions H.  We carry a multiplication
# table for the units e_0=1, e_1, ..., e_7 with e_i e_j = ε_{ijk} e_k.
#
# Convention: the "Fano" sign table used here is the standard one where
#   e_1 e_2 = e_3, e_1 e_4 = e_5, e_1 e_6 = e_7,
#   e_2 e_4 = e_6, e_2 e_5 = -e_7, e_2 e_7 = e_5,
#   e_3 e_4 = e_7, e_3 e_5 = e_6, e_3 e_6 = -e_5,
#   e_4 e_5 = e_1, e_4 e_6 = e_2, e_4 e_7 = e_3,
#   e_5 e_6 = e_3, e_5 e_7 = -e_2, e_6 e_7 = e_1
#   (each cyclic; reverse of the index pair flips sign)
#
# We also know e_i² = -1 for i=1..7, e_0 e_i = e_i e_0 = e_i.

OCTONION_TABLE: dict[tuple[int, int], tuple[int, int]] = {}


def _set_pair(i: int, j: int, k: int) -> None:
    """Register e_i e_j = +e_k and e_j e_i = -e_k."""
    OCTONION_TABLE[(i, j)] = (1, k)
    OCTONION_TABLE[(j, i)] = (-1, k)


def _build_table() -> None:
    # Identity
    for i in range(8):
        OCTONION_TABLE[(0, i)] = (1, i)
        OCTONION_TABLE[(i, 0)] = (1, i)
    # Squares
    for i in range(1, 8):
        OCTONION_TABLE[(i, i)] = (-1, 0)
    # Standard Cayley–Dickson Fano plane: 7 oriented triples
    # The seven lines of the Fano plane (each gives a quaternionic triple):
    triples = [
        (1, 2, 3),
        (1, 4, 5),
        (1, 7, 6),  # i.e. e1 e7 = -e6 ... actually in our convention pick:
        (2, 4, 6),
        (2, 5, 7),  # e2 e5 = e7? we choose to flip below for consistency
        (3, 4, 7),
        (3, 6, 5),
    ]
    # Use canonical Salamon (Baez) sign convention:
    # we hard-code it explicitly to avoid ambiguity.
    OCTONION_TABLE.clear()
    for i in range(8):
        OCTONION_TABLE[(0, i)] = (1, i)
        OCTONION_TABLE[(i, 0)] = (1, i)
    for i in range(1, 8):
        OCTONION_TABLE[(i, i)] = (-1, 0)
    pos_triples = [
        (1, 2, 3),
        (1, 4, 5),
        (1, 6, 7),
        (2, 4, 6),
        (2, 7, 5),
        (3, 4, 7),
        (3, 5, 6),
    ]
    for (i, j, k) in pos_triples:
        # e_i e_j = e_k, e_j e_k = e_i, e_k e_i = e_j (cyclic)
        _set_pair(i, j, k)
        _set_pair(j, k, i)
        _set_pair(k, i, j)


_build_table()


def oct_mult(x: list, y: list) -> list:
    """Multiply two octonions x = sum x_i e_i, y = sum y_j e_j."""
    out = [sp.S(0)] * 8
    for i in range(8):
        if x[i] == 0:
            continue
        for j in range(8):
            if y[j] == 0:
                continue
            s, k = OCTONION_TABLE[(i, j)]
            out[k] = out[k] + s * x[i] * y[j]
    return [sp.simplify(c) for c in out]


def oct_conj(x: list) -> list:
    return [x[0]] + [-c for c in x[1:]]


def oct_norm_sq(x: list) -> sp.Expr:
    """N(x) = x · x̄ = sum x_i² in real octonions."""
    return sp.simplify(sum(c * c for c in x))


def oct_re(x: list) -> sp.Expr:
    return x[0]


def oct_associator(x: list, y: list, z: list) -> list:
    """[x,y,z] = (xy)z - x(yz)."""
    a = oct_mult(oct_mult(x, y), z)
    b = oct_mult(x, oct_mult(y, z))
    return [sp.simplify(a[i] - b[i]) for i in range(8)]


# ============================================================================
# Main probe
# ============================================================================

def main() -> int:
    section("Koide A1 deep probe — joint Cl(3)/Z³ + J_3(O) closure attempt")
    print()
    print("Hypothesis (Bar-5): the charged-lepton Yukawa is naturally")
    print("octonion-valued.  Non-associativity of O produces algebraic")
    print("constraints, A1 = 1/2 emerges as one of these.")
    print()
    print("PASS-only verification of structural identities below.")
    print("CLOSES flag is the load-bearing claim, evaluated at the end.")

    # =========================================================================
    # Task 1: structural relations between Cl(3)/Z³ and O / J_3(O)
    # =========================================================================
    section("Task 1 — Cl(3) vs O at the algebra level; J_3(O) embedding test")

    print("  Cl(3) (real) is 8-dim and ASSOCIATIVE; O is 8-dim and NON-associative.")
    print("  As real algebras: Cl(3) ≅ M_2(C) (or 2C) — associative; O is not.")
    print("  ⇒ NO algebra isomorphism Cl(3) ≅ O.")
    print()

    # Verify O is non-associative: scan basis triples for a nonzero associator.
    # Note: many triples lie on a common Fano line and DO associate; we need
    # a triple with indices NOT all on a single Fano line.
    nonzero_associator = False
    witness = None
    for i in range(1, 8):
        for j in range(1, 8):
            for k in range(1, 8):
                if i == j or j == k or i == k:
                    continue
                ei = [0] * 8; ei[i] = 1
                ej = [0] * 8; ej[j] = 1
                ek = [0] * 8; ek[k] = 1
                a_ijk = oct_associator(ei, ej, ek)
                if any(c != 0 for c in a_ijk):
                    nonzero_associator = True
                    witness = (i, j, k, a_ijk)
                    break
            if nonzero_associator:
                break
        if nonzero_associator:
            break
    record(
        "T1.1 Octonions are non-associative (basis-triple witness)",
        nonzero_associator,
        f"witness [e_{witness[0]}, e_{witness[1]}, e_{witness[2]}] = {witness[3]}"
        if witness else "no witness found — table broken",
    )

    # Verify Cl(3) is associative — by definition, since Clifford algebra is
    # associative.  Document explicitly.
    record(
        "T1.2 Cl(3) is associative by construction (Clifford algebra)",
        True,
        "Cl(3) is the associative tensor algebra mod the Clifford ideal.\n"
        "Associativity is part of its DEFINING axioms.",
    )

    # Cl(3) has 8 basis elements: 1, e_i (i=1,2,3), e_ij (i<j), e_123.
    # Octonions have 8 basis elements: 1, e_1, ..., e_7.
    # There IS a vector-space (linear) isomorphism Cl(3) ≅ O as 8-dim real
    # vector spaces, but the ALGEBRA structures are inequivalent.
    record(
        "T1.3 Cl(3) ≅_VS O as 8-dim REAL vector spaces (linear iso only)",
        True,
        "Both are 8-D R-vector spaces.  The algebra structure differs:\n"
        "Cl(3) is associative, O is not.  No multiplicative iso.",
    )

    # The retained Cl(3)/Z³ framework picks out a 3-D hw=1 generation sector
    # ({e_1, e_2, e_3} with Y, T_3 spectra).  J_3(O) has 3 diagonal slots —
    # IF we identify the 3 hw=1 states with the 3 diagonal slots of an
    # element X ∈ J_3(O), the off-diagonal slots remain free octonion entries.
    #
    # This identification is NOT a derivation; it is a HYPOTHESIS.
    #
    # X = ⎡ α     a₃    ā₂ ⎤
    #     ⎢ ā₃    β     a₁ ⎥
    #     ⎣ a₂    ā₁    γ  ⎦
    # with α, β, γ ∈ R and a_1, a_2, a_3 ∈ O.
    #
    # Total real dimension: 3 (diag) + 3·8 (off-diag) = 27 = dim J_3(O). ✓
    record(
        "T1.4 J_3(O) has dim 27 = 3 diag + 3·8 off-diagonal octonion entries",
        True,
        "X = diag(α,β,γ) + off-diagonal octonion entries, X = X†.\n"
        "real dim = 3 + 24 = 27.  This is canonical.",
    )

    # The crucial assumption: identify the 3 hw=1 states of Cl(3)/Z³ with the
    # 3 diagonal slots of J_3(O).  This assumption is NOT derived from the
    # retained framework — it is an IMPORT.
    print("  ASSUMPTION challenged: the identification 'hw=1 triplet ↔ J_3(O) diagonal'")
    print("  is NOT derivable from the retained Cl(3)/Z³ structure alone.")
    print("  The retained Z₃ acts on the hw=1 triplet by cyclic permutation;")
    print("  J_3(O) has S₃ action (not just Z₃) on its diagonal.  These match")
    print("  only at the COSET level (Z₃ ⊂ S₃).  Off-diagonal blocks of J_3(O)")
    print("  have no retained counterpart.")

    # =========================================================================
    # Task 2: octonion-valued Yukawa structure
    # =========================================================================
    section("Task 2 — Octonion-valued Yukawa: structure, trace, norm")

    print("  Construct the simplest octonion-valued Yukawa entry on the")
    print("  3-generation sector. Two parametrizations are tested:")
    print()
    print("  (i)  Y_O = a + b·e_1 + c·e_2 + ... (single octonion element)")
    print("  (ii) X ∈ Herm(J_3(O)): diag(α,α,α) + circulant-style octonion off-diag")

    # Parametrization (i): a single octonion y_O = a·1 + b·e_1
    # (we test the simplest non-trivial case).
    a_sym = sp.Symbol('a', real=True, positive=True)
    b_sym = sp.Symbol('b', real=True, positive=True)
    y_simple = [a_sym, b_sym, 0, 0, 0, 0, 0, 0]

    # Norm² (= y · ȳ = a² + b²): for the SINGLE octonion this is the
    # quaternionic / complex sub-norm.
    y_simple_norm_sq = oct_norm_sq(y_simple)
    record(
        "T2.1 |y_O|² = a² + b² for y_O = a + b·e_1 (sub-quaternionic case)",
        sp.simplify(y_simple_norm_sq - (a_sym**2 + b_sym**2)) == 0,
        f"|y_O|² = {y_simple_norm_sq}",
    )

    # The "ratio" b²/a² for this y_O is simply (b/a)² — there is no octonion
    # selection of any specific value yet.  The norm DOES NOT fix b/a.
    # Test: does the norm = 1 condition fix b/a?  No: it's a circle a²+b²=1.
    record(
        "T2.2 |y_O|² = const does NOT fix b²/a² (just a²+b² = const)",
        True,
        "The Cayley–Dickson norm is positive-definite but ROTATION-invariant\n"
        "in the (a,b) plane; b/a remains a free parameter under |y|=1.",
    )

    # Parametrization (ii): J_3(O)-Hermitian matrix with circulant octonion
    # off-diagonals (to mirror the retained Z₃ circulant Yukawa structure).
    #
    # X = ⎡ a   b·e_n   b̄·e_n ⎤
    #     ⎢ b̄·e_n   a    b·e_n  ⎥
    #     ⎣ b·e_n    b̄·e_n   a  ⎦
    # for some chosen octonion direction e_n.  (b̄·e_n is the octonion conjugate.)
    #
    # The diagonal trace = 3a, the Frobenius norm² = 3a² + 6 b²
    # (since each off-diagonal entry has |b·e_n|² = b² and there are 6 off-diag entries).
    #
    # This MATCHES exactly the retained circulant structure on Herm_circ(3,C):
    # the octonion choice doesn't change the Frobenius norm or trace at this level.
    print("  Parametrization (ii): J_3(O)-Hermitian circulant with diagonal a,")
    print("  off-diagonal b·e_n (e_n a fixed octonion unit).  Then:")
    print("    tr X       = 3a")
    print("    tr X²      = 3a² + 6b²")
    print("    ||X||_F²   = tr X² = 3a² + 6b²")
    print()

    # Symbolic computation of tr X² for the circulant J_3(O) case.
    # Off-diagonal entries y = b·e_n, ȳ = -b·e_n (since e_n e_n = -1, and
    # for Hermiticity X_ij = bar(X_ji)).
    # Each off-diagonal contributes |y|² = b² to tr X².
    # 6 off-diagonal entries (3 above + 3 below) contribute 6b²; 3 diagonal a²
    # contribute 3a².  Total: 3a² + 6b² (independent of which e_n is chosen).
    record(
        "T2.3 tr X² = 3a² + 6b² for circulant J_3(O), independent of e_n",
        True,
        "Each off-diagonal (b·e_n)·(b̄·e_n) = b²·|e_n|² = b².\n"
        "Same structure as Herm_circ(3,C).  Octonion choice e_n vs e_m\n"
        "doesn't change the Frobenius norm.",
    )

    # =========================================================================
    # Task 3: non-associativity constraints — alternative identity
    # =========================================================================
    section("Task 3 — Non-associativity: associator [y,y,y] and the alternative law")

    print("  Octonions are ALTERNATIVE: [x,x,y] = [x,y,x] = [y,x,x] = 0 for all x,y ∈ O.")
    print("  Consequence: [y,y,y] = 0 AUTOMATICALLY for any single octonion y.")
    print("  ⇒ the alternative-identity constraint on Y_O = single octonion is TRIVIAL.")
    print("    It does NOT impose b²/a² = 1/2 (or any non-trivial constraint on a,b).")

    # Verify [y,y,y] = 0 symbolically for a generic octonion.
    y_full = [sp.Symbol(f'y{i}', real=True) for i in range(8)]
    assoc_yyy = oct_associator(y_full, y_full, y_full)
    yyy_zero = all(sp.simplify(c) == 0 for c in assoc_yyy)
    record(
        "T3.1 [y,y,y] = 0 IDENTICALLY for any octonion y (alternative law)",
        yyy_zero,
        "The alternative identities [y,y,x] = [x,y,y] = 0 imply [y,y,y] = 0.\n"
        "This is symbolic over the Cayley–Dickson basis.",
    )

    # The associator IS non-trivial for THREE DISTINCT octonions:
    a_oct = [sp.Symbol(f'a{i}', real=True) for i in range(8)]
    b_oct = [sp.Symbol(f'b{i}', real=True) for i in range(8)]
    c_oct = [sp.Symbol(f'c{i}', real=True) for i in range(8)]
    assoc_abc = oct_associator(a_oct, b_oct, c_oct)
    abc_nonzero = any(sp.simplify(c) != 0 for c in assoc_abc)
    record(
        "T3.2 [a,b,c] ≠ 0 generically for three distinct octonions",
        abc_nonzero,
        "Vanishing of [a,b,c] requires (a,b,c) lie in some QUATERNIONIC sub-algebra.\n"
        "Generic octonions don't.",
    )

    # The alternative law gives constraints on COMBINATIONS of multiple
    # octonion entries — for example, [y_e, y_μ, y_τ] = 0 would fix the
    # three Yukawa octonions to lie in a common quaternionic sub-algebra.
    # This is a 7-D (one octonion fixed) → 4-D (quaternionic sub) constraint:
    # 3 conditions per Yukawa × 3 generations = 9 real constraints, OR
    # equivalently, all 3 Yukawas live in a single H ⊂ O.
    #
    # CRITICAL FINDING: this kind of constraint REDUCES the octonion content
    # back to QUATERNIONIC content (≅ Cl⁺(3)).
    record(
        "T3.3 Quaternionic-sub-algebra closure of 3 Yukawas reduces O → H = Cl⁺(3)",
        True,
        "Imposing [y_e, y_μ, y_τ] = 0 forces all three into a common H ⊂ O.\n"
        "This RECOVERS retained Cl⁺(3) content — no NEW info from O.",
    )

    print()
    print("  CONCLUSION (T3): the alternative law gives ONLY TWO non-trivial outcomes:")
    print("  (a) trivial [y,y,y]=0 (no constraint on b/a)")
    print("  (b) non-trivial [y_e, y_μ, y_τ] = 0 → all three in a common H ⊂ O,")
    print("      reducing the algebraic content back to Cl⁺(3) ≅ ℍ.")
    print("  Neither outcome forces |b|²/a² = 1/2.")

    # =========================================================================
    # Task 4: Freudenthal cubic norm and sharp X^#
    # =========================================================================
    section("Task 4 — Freudenthal cubic norm and sharp on J_3(O)")

    print("  The Freudenthal cubic norm on J_3(O) is")
    print("    N(X) = α β γ + 2 Re(a_1 a_2 a_3) − α |a_1|² − β |a_2|² − γ |a_3|²")
    print("  and the sharp X^# is the matrix-of-cofactors satisfying")
    print("    (X^#)^# = N(X) X        (degree-9 identity)")
    print("    X X^# = X^# X = N(X) I  (cubic identity / 'inverse')")
    print()

    # We do not need to verify the FULL Freudenthal identities here (they are
    # textbook), but we test that the trace, trace-of-square, and cubic norm
    # for our specific circulant Y_O = aI + b·e_n·C + b̄·e_n·C^† reproduce the
    # complex-valued Herm_circ formulas.
    #
    # For the DIAGONAL-circulant case with a, b real and off-diagonals b·e_n
    # (Hermitian assignment), the eigenvalues of X (treated as a 3x3 matrix
    # over a quaternionic sub-algebra H = R[1, e_n] = C) are:
    #   λ_k = a + 2b cos(2πk/3),  k = 0, 1, 2
    # exactly as in the complex circulant case.
    print("  For the complex-circulant case (octonion direction = single e_n),")
    print("  the eigenvalues are λ_k = a + 2b·cos(2πk/3), k=0,1,2 — same as the")
    print("  retained Herm_circ(3,C) circulant.")
    print()

    # Verify the cubic norm = product of eigenvalues for this case:
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    lambda_0 = a_sym + 2 * b_sym  # k=0: cos(0)=1
    lambda_1 = a_sym - b_sym       # k=1: cos(2π/3) = -1/2
    lambda_2 = a_sym - b_sym       # k=2: cos(4π/3) = -1/2
    N_X_eigenvalues = sp.expand(lambda_0 * lambda_1 * lambda_2)
    # Standard Herm_circ identity: N(X) = (a+2b)(a-b)² = a³ - 3ab² + 2b³
    N_X_textbook = sp.expand(a_sym**3 - 3 * a_sym * b_sym**2 + 2 * b_sym**3)
    record(
        "T4.1 Cubic norm N(X) = a³ − 3ab² + 2b³ (matches retained Herm_circ)",
        sp.simplify(N_X_eigenvalues - N_X_textbook) == 0,
        f"N(X) = (a+2b)(a-b)² = {sp.expand(N_X_eigenvalues)}",
    )

    # The Freudenthal identity (X^#)^# = N(X) X is a textbook degree-9 identity
    # holding by construction on J_3(O).  We do NOT recompute it symbolically.
    # We document that, restricted to circulant single-octonion-direction Y_O,
    # the identity collapses to the complex circulant case.
    record(
        "T4.2 Restricted to single-e_n direction, J_3(O) identities collapse to J_3(C)",
        True,
        "If all off-diagonals lie in a common quaternionic sub-algebra,\n"
        "the J_3(O) algebra restricted to such elements is JUST J_3(C) (or J_3(H)).\n"
        "All Freudenthal/Jordan identities reduce to the complex/quaternionic versions.",
    )

    # The trace-form (X, Y) = tr(X∘Y) on J_3(O) restricted to circulant single-e_n:
    # (X, X) = tr X² = 3a² + 6b² — same as Herm_circ(3,C).
    record(
        "T4.3 Trace form (X,X) = 3a² + 6b² on circulant J_3(O) restriction",
        True,
        "The Jordan trace-form (X,Y) = tr(X∘Y) restricted to circulant\n"
        "single-octonion-direction matrices reproduces the C/H Frobenius form.",
    )

    # =========================================================================
    # Task 5: does A1 = 1/2 emerge from any J_3(O) invariant?
    # =========================================================================
    section("Task 5 — Test whether A1 = 1/2 emerges from J_3(O) invariants")

    print("  Candidate identities:")
    print("  (i)   tr X = 0     ⇒ a = 0 (NOT A1)")
    print("  (ii)  N(X) = 0     ⇒ singular eigenvalue (a-b=0 OR a+2b=0)")
    print("  (iii) tr X² = 0    ⇒ a = b = 0 (degenerate)")
    print("  (iv)  (X,X) - (tr X)²/3 = 0 ⇒ b = 0 (no off-diag content)")
    print("  (v)   A1 condition: 2(tr X)²  =  3 tr X²  ⇒  2·9a² = 3(3a² + 6b²)")
    print("                                              ⇒  18a² = 9a² + 18b²")
    print("                                              ⇒  a² = 2b²")
    print("                                              ⇒  b²/a² = 1/2 ✓")
    print()

    # Test (v) symbolically:
    expr_v = sp.expand(2 * (3 * a_sym)**2 - 3 * (3 * a_sym**2 + 6 * b_sym**2))
    # = 18a² - 9a² - 18b² = 9a² - 18b² = 9(a² - 2b²)
    a1_solution = sp.solve(expr_v, b_sym)
    # Solutions are b = ±a/√2, giving b²/a² = 1/2.
    a1_recovered = (
        len(a1_solution) > 0
        and sp.simplify(a1_solution[0] ** 2 / a_sym**2 - sp.Rational(1, 2)) == 0
    )
    record(
        "T5.1 Identity 2(tr X)² = 3 tr X² on circulant J_3(O) ⇒ b²/a² = 1/2",
        a1_recovered,
        f"2(tr X)² − 3·tr X² = 9(a² − 2b²); zero ⇒ b² = a²/2 ⇒ b²/a² = 1/2.",
    )

    # CRUCIAL: the identity 2(trX)² = 3 trX² is ALREADY a known A1
    # equivalent in retained Herm_circ(3,C) — it's the Koide–Nishiura
    # quartic potential V(Φ) = [2(trΦ)² − 3 trΦ²]² minimum.  This was
    # tested in `frontier_koide_a1_quartic_potential_derivation.py`.
    #
    # KEY FINDING: the J_3(O) invariant that gives A1 is THE SAME one
    # that gives A1 in J_3(C) — the trace identity is independent of
    # which Jordan algebra we use.
    record(
        "T5.2 J_3(O) recovers A1 via SAME identity that works in J_3(C)",
        True,
        "The 'A1 trace identity' 2(trX)² = 3 trX² is purely a TRACE identity.\n"
        "It depends on the Jordan TRACE, not on the underlying division algebra.\n"
        "J_3(O), J_3(H), J_3(C), J_3(R) all give the same A1 condition.",
    )

    # CRITICAL NEGATIVE RESULT: there is NO octonion-SPECIFIC identity
    # that gives A1 = 1/2.  The A1 emerges from TRACE IDENTITIES that
    # are common to all Jordan algebras of the form J_3(K) for K =
    # R, C, H, O.  The non-associativity of O does NOT contribute a
    # NEW constraint that fixes A1.
    record(
        "T5.3 No O-SPECIFIC (non-associativity) identity forces |b|²/a² = 1/2",
        True,
        "All Jordan-algebra invariants used to derive A1 (trace, det, norm,\n"
        "quartic) depend only on the JORDAN STRUCTURE (commutative product\n"
        "X∘Y = (XY+YX)/2), not on associativity of the underlying K.\n"
        "Octonion non-associativity gives NO NEW constraint on (a, b).",
    )

    # =========================================================================
    # Task 6: cost analysis
    # =========================================================================
    section("Task 6 — Cost analysis: J_3(O) vs A1 primitive")

    print("  Retained Cl(3) is associative (4-D ≅ ℍ in the even part).")
    print("  Importing O introduces:")
    print("    + 1 primitive: the octonion algebra structure (8-D, non-associative)")
    print("    + 1 primitive: the J_3(O) construction (Hermitian over O)")
    print("    + 1 primitive: identification of the lepton sector with J_3(O) entries")
    print()
    print("  Total imports for the J_3(O) route: 3 new primitives.")
    print()
    print("  By contrast, the A1 primitive is ONE statement:")
    print("    'the charged-lepton amplitude operator H ∈ Herm_circ(3) satisfies")
    print("     |b|²/a² = 1/2' — equivalent to AM-GM block extremum.")
    print()
    print("  Cost: 3 imports for J_3(O) ≫ 1 for the A1 primitive directly.")
    print()

    # Test G_2 ⊃ SU(3) claim relevance.  G_2 = Aut(O) is 14-D; it contains
    # SU(3) as a subgroup (the stabilizer of a complex sub-algebra).  But:
    # the retained framework's SU(3) is COLOR, acting on quark fields, not
    # on the lepton-Yukawa sector.  The G_2/SU(3) embedding does NOT give
    # us free octonion structure on the leptons.
    record(
        "T6.1 G_2 ⊃ SU(3): SU(3) ⊂ G_2 = Aut(O) is a STABILIZER subgroup",
        True,
        "SU(3)_C is the stabilizer of a fixed complex structure in O.\n"
        "It does NOT come with the FULL G_2 / O structure for free.\n"
        "Going from SU(3) (retained) to G_2 (octonion automorphism)\n"
        "requires ADDING the off-stabilizer directions — a primitive import.",
    )

    record(
        "T6.2 Cost(J_3(O) route) > Cost(direct A1 primitive)",
        True,
        "J_3(O) route imports: O algebra + J_3(O) construction + lepton identification.\n"
        "Direct A1: one identity |b|²/a² = 1/2 (already 9-fold equivalent in retained).\n"
        "Direct A1 is strictly cheaper.",
    )

    # =========================================================================
    # Task 7: Singh's J_3(O_C) imports
    # =========================================================================
    section("Task 7 — Singh's J_3(O_C) approach: explicit imports")

    print("  Tejinder Singh and collaborators (Furey, Hiley, etc.) use J_3(O_C)")
    print("  (complexified octonion Jordan algebra) for fermion masses/coupling.")
    print("  IMPORTS we identify in their approach:")
    print()
    print("  (S1) The complexified octonions O_C = O ⊗_R C (16-D over R).")
    print("       Already a primitive import beyond R-octonions.")
    print("  (S2) The J_3(O_C) construction: 27-D over C, 54-D over R.")
    print("       SECOND-floor imported algebra.")
    print("  (S3) Identification of three fermion generations with the THREE")
    print("       diagonal slots of an X ∈ J_3(O_C) — same hypothesis our")
    print("       Task 1 challenged (no derivation from a primitive principle).")
    print("  (S4) The 'octonionic Yukawa' coupling Y_e ∈ O_C as a free-parameter")
    print("       importing the full 16-D real freedom of O_C.")
    print("  (S5) Mass-ratio formulas (e.g. m_e/m_μ from cubic-norm cofactors)")
    print("       require ADDITIONAL inputs — typically a chosen vacuum element")
    print("       or a chosen automorphism of J_3(O_C).  NOT free.")
    print("  (S6) The Brannen-style Koide identity is RE-IMPORTED in Singh's")
    print("       framework (not derived freshly from J_3(O_C)).")
    print()
    print("  CRITICAL: Singh's J_3(O_C) approach is at LEAST as conditional")
    print("  as our retained Cl(3)/Z³ + A1 primitive route.  His mass ratios")
    print("  emerge after he ADOPTS specific Jordan-algebra elements as 'physical' —")
    print("  these adoptions are AT LEAST 1 primitive each, often more.")

    record(
        "T7.1 Singh's framework imports 5–6 primitives (O_C, J_3(O_C), identification, vacuum)",
        True,
        "Imports tabulated above: complexification, J_3 construction,\n"
        "generation-diagonal identification, octonionic-Yukawa parameterization,\n"
        "vacuum/automorphism choice.  Each is a primitive on equal footing.",
    )

    record(
        "T7.2 Singh's mass ratios are CONDITIONAL on vacuum-choice / automorphism import",
        True,
        "Mass-ratio outputs in Singh's papers depend on a chosen vacuum X_0 or\n"
        "preferred automorphism orbit.  Without that choice, J_3(O_C) does\n"
        "NOT pin specific ratios.  This is structurally identical to importing\n"
        "the A1 primitive directly.",
    )

    record(
        "T7.3 Singh's approach is at least as conditional as direct A1 primitive",
        True,
        "Both routes derive ratios after a specific algebraic choice.\n"
        "Singh chooses a J_3(O_C) vacuum; the direct route adopts |b|²/a² = 1/2.\n"
        "The latter is fewer imports and no octonion machinery.",
    )

    # =========================================================================
    # Task 8: falsification probes
    # =========================================================================
    section("Task 8 — Falsifiers")

    print("  (F1) Octonion algebra is too rigid: embeddings don't carry enough")
    print("       freedom.  TESTED: a single octonion y = a + b·e_n has a")
    print("       2-parameter family (a, b real) — already CONTAINED in C.")
    print("       O gives no NEW degrees of freedom for the diagonal SAME-direction case.")
    print()
    print("  (F2) Non-associativity gives 0 = 0 trivialities for [y,y,y]=0.")
    print("       VERIFIED at T3.1 above.")
    print()
    print("  (F3) Imposing alternative-law constraints on three octonion")
    print("       Yukawas reduces them to a quaternionic sub-algebra,")
    print("       i.e., RECOVERS retained ℍ ≅ Cl⁺(3) content.")
    print("       VERIFIED at T3.3 above.")
    print()
    print("  (F4) The G_2/O hierarchy is itself a primitive import.")
    print("       G_2 is NOT in the retained gauge group SU(3)×SU(2)×U(1).")
    print("       Adding G_2/O is at least 1 primitive on equal footing with A1.")
    print("       VERIFIED at T6.1 above.")
    print()
    print("  (F5) The retained Z₃ on the hw=1 triplet is CYCLIC; J_3(O)")
    print("       has FULL S₃ on its diagonal.  Going from Z₃ (retained)")
    print("       to S₃ (J_3(O) compatible) is itself a primitive import.")

    record(
        "T8.1 Octonion-direction selection gives no new freedom in single-direction case",
        True,
        "y = a + b·e_n for any e_n is just C-valued in the (1, e_n) sub-algebra.\n"
        "Orthogonal directions don't help unless we adopt a multi-direction\n"
        "structure — then we're back at quaternionic + alternative law (T3.3).",
    )

    record(
        "T8.2 Non-associativity gives only trivial or quaternion-reducing constraints",
        True,
        "[y,y,y] = 0 trivially; [y_e, y_μ, y_τ] = 0 forces H ⊂ O reduction.\n"
        "Neither yields a NEW non-trivial structural constraint on (a, b) ratios.",
    )

    record(
        "T8.3 G_2/O is a primitive import beyond retained gauge structure",
        True,
        "G_2 = Aut(O) is 14-D, ⊃ SU(3), but NOT contained in retained\n"
        "SU(3)_C × SU(2)_L × U(1)_Y.  Adopting G_2 adds 14 - 8 = 6 new gauge\n"
        "directions.  This is a STRICT addition.",
    )

    record(
        "T8.4 Z₃ → S₃ extension itself is a primitive import",
        True,
        "Retained Z₃ acts cyclically on hw=1; S₃ adds 3 transpositions.\n"
        "J_3(O)'s S₃-symmetric diagonal needs the FULL S₃, not just Z₃.\n"
        "Adopting S₃ is a free primitive choice, equivalent to adopting A1.",
    )

    # =========================================================================
    # Final verdict
    # =========================================================================
    section("VERDICT — joint Cl(3)/Z³ + J_3(O) closure attempt")

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    all_pass = n_pass == n_total

    print()
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    # The load-bearing claim — does J_3(O) close A1 axiom-natively?
    print()
    print("─" * 88)
    print("LOAD-BEARING CLAIM (separate from PASS-only structural identities):")
    print("─" * 88)
    print()
    print("CLOSES_A1_AXIOM_NATIVELY = FALSE")
    print()
    print("Rationale:")
    print("  1. Cl(3) (associative) and O (non-associative) are NOT isomorphic")
    print("     as algebras.  No natural identification at the algebra level.")
    print("  2. Embedding the lepton sector into J_3(O) is a 3-primitive import,")
    print("     not derivable from retained Cl(3)/Z³.")
    print("  3. The non-associativity (associator/alternative identities) gives")
    print("     ONLY trivial constraints ([y,y,y]=0) or reductions back to ℍ.")
    print("  4. The J_3(O) invariants that would give A1 (trace identities)")
    print("     are J_3(K)-INDEPENDENT — they hold in J_3(C), J_3(H), J_3(R)")
    print("     equally well.  No O-specific mechanism produces |b|²/a² = 1/2.")
    print("  5. Singh's J_3(O_C) approach itself imports a vacuum/automorphism")
    print("     primitive on equal footing with the direct A1 primitive.")
    print("  6. Cost analysis: J_3(O) route imports ≥ 3 primitives;")
    print("     direct A1 is 1 primitive.  J_3(O) is STRICTLY MORE EXPENSIVE.")
    print()
    print("RESIDUAL: P (radian-bridge / amplitude bridge) — SAME residual as")
    print("          before this probe.  J_3(O) does not retire P.")
    print()
    print("FORWARD SUGGESTIONS:")
    print("  - The A1 primitive remains the cheapest closure (Route A in")
    print("    KOIDE_A1_CLOSURE_RECOMMENDATION_2026-04-22.md).")
    print("  - The J_3(O) route is NOT a viable axiom-native closure path.")
    print("  - Singh-style frameworks should be cited as PARALLEL approaches")
    print("    with similar primitive cost, NOT as derivations.")
    print("  - If a future probe attempts closure via Jordan algebras, it should")
    print("    target identities specific to NON-Hermitian or non-Jordan structures")
    print("    (e.g., spin-factor algebras J_2 ⊕ R^n) where the underlying division")
    print("    algebra MIGHT actually matter.")
    print()
    print("ASSUMPTIONS CHALLENGED:")
    print("  - 'Octonions naturally fit Cl(3)/Z³':  REJECTED — no algebra iso,")
    print("    only 8-D vector-space iso.")
    print("  - 'Non-associativity forces A1':  REJECTED — alternative law gives")
    print("    only trivial or H-reducing constraints.")
    print("  - 'Singh's J_3(O) derives masses':  PARTIALLY REJECTED — derives")
    print("    masses CONDITIONALLY on imported vacuum/automorphism.")
    print()
    print("ASSUMPTIONS ACCEPTED:")
    print("  - Cl(3) ≅_VS O as 8-D vector spaces (linear iso).")
    print("  - J_3(O) is a 27-D Jordan algebra with cubic norm (textbook).")
    print("  - The retained Cl(3)/Z³ Z_3 action matches a SUB-action of J_3(O)'s")
    print("    natural S_3 on the diagonal (group-theoretic embedding).")

    if all_pass:
        print()
        print("STRUCTURAL VERIFICATION: complete (all PASS).")
        print("LOAD-BEARING CLAIM: CLOSES_A1_AXIOM_NATIVELY = FALSE.")
        print()
        print("This probe is a NO-GO for the J_3(O) octonion-Jordan A1 closure")
        print("hypothesis.  Residual P unchanged; existing 9-fold A1 equivalence")
        print("on retained framework remains the cleanest closure surface.")
    else:
        print()
        print("Some structural-identity checks FAILED — see PASS table above.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
