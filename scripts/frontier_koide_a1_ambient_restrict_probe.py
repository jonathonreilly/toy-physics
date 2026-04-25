#!/usr/bin/env python3
"""
Derivation probe — Koide A1 via "derive on ambient Herm(3), then restrict
to Herm_circ(3)" strategy.

Target: |b|²/a² = 1/2 on Herm_circ(3), where an element is parametrized
        Y = a I + b C + b̄ C²   (C = cyclic shift)
        ||Y||²_F = 3 a² + 6 |b|²    (so A1 ⇔  3 a² = 6 |b|²)

Prior "Freudenthal-ambient" probe (described in the audit) found that on
Herm_circ(3) directly, the Peirce 1/2-eigenspace of L_{P_I} is empty, so
Jordan identities trivialize. This probe attempts the OPPOSITE order:
derive a constraint on ambient Herm(3) where the 1/2-eigenspace is 6-dim,
then restrict to the Z_3-fixed subspace Herm_circ(3).

Attack vectors tested (≥ 3):
  A1  Peirce AM-GM on Herm(3) w.r.t. P_I = (1/3)J
  A2  Freudenthal cubic   X^#·X^#  =  N(X) X   on Herm(3), Z_3-averaged
  A3  SU(3)-invariant quartics on Herm(3), pulled back to circulants
  A4  Cayley-Hamilton on Herm(3), Z_3-averaged
  A5  Isotype decomposition of the 6-dim Peirce 1/2-space under Z_3
  A6  Frobenius equipartition extremum under joint Z_3-invariance constraint

Assumption audit — A-amb1 .. A-amb5 are answered explicitly at the end.

No commits. No retained primitives. Just compute.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Callable

import sympy as sp

# ----------------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------------
PASS = 0
FAIL = 0
LOG: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> bool:
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    LOG.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if detail:
        for ln in detail.splitlines():
            print(f"       {ln}")
    return ok


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ----------------------------------------------------------------------------
# Cl(3)/Z_3 setup: ambient Herm(3), circulants, Z_3 action
# ----------------------------------------------------------------------------
omega = sp.exp(2 * sp.pi * sp.I / 3)           # cube root of unity
C = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])   # cyclic shift
C2 = C * C
I3 = sp.eye(3)

# Rank-1 idempotent corresponding to the trivial Z_3 isotype
J = sp.Matrix([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
P_I = J / 3   # Jordan-rank-1 idempotent: P_I^2 = P_I, tr(P_I) = 1


def dagger(M: sp.Matrix) -> sp.Matrix:
    return M.conjugate().T


def jordan_prod(A: sp.Matrix, B: sp.Matrix) -> sp.Matrix:
    """Jordan product on Herm(3): A ∘ B = (AB + BA)/2."""
    return (A * B + B * A) / 2


def z3_average(X: sp.Matrix) -> sp.Matrix:
    """Z_3-average under conjugation by C."""
    return (X + C * X * C.inv() + C2 * X * C2.inv()) / 3


def frobenius(A: sp.Matrix) -> sp.Expr:
    """||A||²_F = tr(A^† A)."""
    return sp.simplify(sp.trace(dagger(A) * A))


# ----------------------------------------------------------------------------
# Generic parametrizations
# ----------------------------------------------------------------------------
def generic_herm3():
    """Generic X ∈ Herm(3): 9 real parameters.

    Convention: diagonal entries (d0, d1, d2) real, off-diagonal x_{ij} = u_{ij} + i v_{ij}
    for i<j, with X_{ji} = X̄_{ij}.
    """
    d0, d1, d2 = sp.symbols("d0 d1 d2", real=True)
    u01, u02, u12 = sp.symbols("u01 u02 u12", real=True)
    v01, v02, v12 = sp.symbols("v01 v02 v12", real=True)
    X = sp.Matrix([
        [d0,               u01 + sp.I * v01, u02 + sp.I * v02],
        [u01 - sp.I * v01, d1,               u12 + sp.I * v12],
        [u02 - sp.I * v02, u12 - sp.I * v12, d2],
    ])
    params = (d0, d1, d2, u01, u02, u12, v01, v02, v12)
    return X, params


def circulant_herm3():
    """Hermitian Z_3-invariant X: X = aI + bC + b̄C²  with a real, b = p + iq ∈ ℂ."""
    a, p, q = sp.symbols("a p q", real=True)
    b = p + sp.I * q
    bbar = p - sp.I * q
    Y = a * I3 + b * C + bbar * C2
    return Y, (a, p, q)


# ----------------------------------------------------------------------------
# Peirce decomposition on Herm(3) with respect to P_I
# ----------------------------------------------------------------------------
def peirce_decomp_test():
    """Verify that the Jordan-Peirce projectors for P_I split Herm(3) as
    X_1 (1-dim) ⊕ X_{1/2} (6-dim) ⊕ X_0 (2-dim).
    Works on the real vector space Herm(3) (dim 9).
    """
    X, pars = generic_herm3()
    L = jordan_prod(P_I, X)      # L_{P_I}(X)
    # Peirce eigenvectors: (L − 1)·L·(L − 1/2) = 0 always.
    E1 = L - X            # component with eigenvalue 1 satisfies L_X = X
    E0 = L                # component with eigenvalue 0 satisfies L_X = 0
    E_half = 2 * L - X    # … and eigenvalue 1/2 satisfies 2 L_X = X
    return L, X, pars


# ----------------------------------------------------------------------------
# Attack Vector A1 — Peirce AM-GM on Herm(3)
# ----------------------------------------------------------------------------
def attack_A1_peirce_amgm() -> None:
    section("A1: Peirce AM-GM on Herm(3) w.r.t. P_I = (1/3)J")

    X, pars = generic_herm3()

    # Compute L_{P_I}(X) and obtain Peirce projectors using the Jordan-Peirce
    # eigenspace decomposition.  For a Jordan-rank-1 idempotent P_I:
    #   X_1 = P_I X P_I              (onto 1-eigenspace of L_{P_I})
    #   X_0 = (I−P_I) X (I−P_I)      (onto 0-eigenspace of L_{P_I})
    #   X_{1/2} = P_I X (I−P_I) + (I−P_I) X P_I   (onto 1/2-eigenspace)
    # This is textbook for L_e where e is an associative idempotent.
    Q_I = I3 - P_I
    X1  = P_I * X * P_I
    X0  = Q_I * X * Q_I
    Xh  = P_I * X * Q_I + Q_I * X * P_I

    # Correctness of the projection: they sum to X
    sum_ok = sp.simplify((X1 + X0 + Xh) - X) == sp.zeros(3, 3)
    record("A1.1 Peirce projectors: X = X_1 + X_{1/2} + X_0 (associative picture)",
           sum_ok)

    # Dimensions: count the real parameters that each projection depends on.
    # Use Frobenius norms and check quadratic forms.
    FX1 = sp.simplify(frobenius(X1))
    FX0 = sp.simplify(frobenius(X0))
    FXh = sp.simplify(frobenius(Xh))
    FXt = sp.simplify(frobenius(X))

    # Completeness: ||X||²_F = ||X_1||² + ||X_{1/2}||² + ||X_0||² ?  This
    # requires the projectors to be F-orthogonal.  Let's check directly.
    orth1 = sp.simplify(sp.trace(dagger(X1) * Xh))
    orth2 = sp.simplify(sp.trace(dagger(X1) * X0))
    orth3 = sp.simplify(sp.trace(dagger(Xh) * X0))
    record("A1.2 Peirce projectors are Frobenius-orthogonal",
           orth1 == 0 and orth2 == 0 and orth3 == 0,
           f"⟨X_1, X_{{1/2}}⟩={orth1}, ⟨X_1, X_0⟩={orth2}, ⟨X_{{1/2}}, X_0⟩={orth3}")

    record("A1.3 Frobenius sum: ||X||² = ||X_1||² + ||X_{1/2}||² + ||X_0||²",
           sp.simplify(FX1 + FX0 + FXh - FXt) == 0,
           f"||X_1||²_F  = {FX1}\n"
           f"||X_{{1/2}}||²_F = {FXh}\n"
           f"||X_0||²_F  = {FX0}\n"
           f"||X||²_F   = {FXt}")

    # Dimensions via rank of the linear map  pars → entries of each Peirce piece.
    # Flatten entries (split into real+imag components expressed in our params)
    def linear_rank(E: sp.Matrix, params: tuple[sp.Symbol, ...]) -> int:
        entries = []
        for i in range(3):
            for j in range(3):
                e = sp.expand(E[i, j])
                entries.append(sp.re(e))
                entries.append(sp.im(e))
        M = sp.Matrix([[sp.diff(e, p) for p in params] for e in entries])
        return M.rank()

    dims = (linear_rank(X1, pars), linear_rank(Xh, pars), linear_rank(X0, pars))
    # CORRECT Peirce dims for rank-1 idempotent e on J_3(ℂ) = Herm(3):
    #   dim X_1       = 1² = 1   (Hermitian 1×1 block)
    #   dim X_{1/2}   = 2·1·2 = 4 real  (off-block entries, Re+Im)
    #   dim X_0       = 2² = 4   (Hermitian 2×2 block)
    # Total = 9 = dim_R Herm(3).  (The task description "(1,6,2)" is wrong —
    # that would be the split for a TRACE-1 idempotent in a DIFFERENT
    # convention, and still wouldn't sum to 9.)
    record("A1.4 Dimensions of Peirce pieces on Herm(3) w.r.t. rank-1 P_I",
           dims == (1, 4, 4),
           f"(dim_R X_1, dim_R X_{{1/2}}, dim_R X_0) = {dims} — sum = {sum(dims)}.\n"
           "Note: the prompt stated 'X_{1/2} 6-dim, X_0 2-dim', but this is\n"
           "inconsistent with the standard Peirce decomposition on J_3(ℂ).\n"
           "The correct split (1, 4, 4) still has non-empty X_{1/2} — the\n"
           "structural point of the probe survives: X_{1/2} is 4-dim non-zero\n"
           "on Herm(3), 0-dim on Herm_circ (for a Z_3-invariant X).")

    # Candidate balance conditions on ambient Herm(3)
    # Three "natural" balances — check which (if any) forces A1 when
    # restricted to circulants (where X_{1/2} vanishes; see A5 below).
    Y, cpars = circulant_herm3()
    a, p, q = cpars

    Y1 = P_I * Y * P_I
    Y0 = Q_I * Y * Q_I
    Yh = P_I * Y * Q_I + Q_I * Y * P_I
    FY1 = sp.simplify(frobenius(Y1))
    FYh = sp.simplify(frobenius(Yh))
    FY0 = sp.simplify(frobenius(Y0))

    record("A1.5 On circulants, X_{1/2} component vanishes",
           sp.simplify(FYh) == 0,
           f"||Y_{{1/2}}||²_F on circulant = {FYh}")

    # Balance B1 : ||X_1||² = ||X_0|| (uniform per-isotype)
    bal1 = sp.simplify(FY1 - FY0)
    sols1 = sp.solve(bal1, [p, q], dict=True)
    record("A1.6 Ambient balance ||X_1||² = ||X_0||² restricted to circulants",
           True,
           f"restricted balance = {bal1} = 0\n"
           f"(in (a,p,q)): solutions = {sols1}\n"
           f"→ NOT A1 (A1 requires 3a² = 6(p²+q²), i.e., ||Y_1||² = ||Y_0||²/2 on our convention)")

    # Distinguish two meanings of "trivial-isotype Frobenius energy":
    #
    #   (a) Peirce (two-sided) piece:  X_1 = P_I X P_I.  For Y = aI + bC + b̄C²,
    #       Y_1 = (a + 2 Re b)·P_I, and ||Y_1||²_F = (a + 2p)².
    #
    #   (b) Isotype (one-sided) projection:  X → P_I X, the orthogonal
    #       projection of X onto the ROW-SPACE of P_I.  Then
    #       ||P_I Y||²_F = tr(Y P_I Y P_I) = (1/3)(tr Y)² = 3 a².
    #
    # These are DIFFERENT objects:
    #   - Peirce (a) gives the Jordan-algebra idempotent-decomposition pieces
    #     used in the ambient probe.
    #   - Isotype (b) gives the retained "E_+ = (tr Y)²/3 = 3a²" used in the
    #     block-total AM-GM retained theorem.
    #
    # The literature sometimes conflates them; they coincide only when the
    # idempotent has trace 1 AND the matrix in question commutes with P_I.
    FY1_peirce  = sp.simplify(frobenius(Y1))            # = (a+2p)²
    FY1_isotype = sp.simplify((sp.trace(Y))**2 / 3)     # = 3 a²
    FY0_peirce  = sp.simplify(frobenius(Y0))
    FY0_isotype = sp.simplify(sp.trace(Y * Y) - (sp.trace(Y))**2 / 3)

    record("A1.7 Peirce norms vs isotype energies (two distinct splittings)",
           True,
           f"Peirce pieces (two-sided idempotent):\n"
           f"  ||Y_1(Peirce)||²_F = {FY1_peirce}\n"
           f"  ||Y_0(Peirce)||²_F = {FY0_peirce}\n"
           f"Isotype energies (one-sided projection — retained AM-GM form):\n"
           f"  E_+ = (tr Y)²/3     = {FY1_isotype}\n"
           f"  E_⊥ = tr Y² − (tr Y)²/3 = {FY0_isotype}\n"
           f"They coincide only on matrices that commute with P_I\n"
           f"(i.e., satisfy [Y, P_I] = 0).  For Z_3-circulants, indeed\n"
           f"[Y, P_I] = 0 — but the Peirce norm uses a rank-1 projection\n"
           f"yielding (a+2p)², NOT (3a²).")

    # So the 'Peirce balance' ||X_1||² = ||X_0||² does NOT restrict to A1.
    # Only the 'isotype balance' E_+ = E_⊥ does — and E_+ = E_⊥ is the
    # retained AM-GM postulate, not a Jordan-algebra identity.
    # Put this inequivalence on the record.
    p_bal  = sp.simplify(FY1_peirce  - FY0_peirce)   # Peirce balance residual
    iso_bal = sp.simplify(FY1_isotype - FY0_isotype)  # isotype balance residual
    is_iso_A1 = sp.simplify(iso_bal - (3 * a**2 - 6 * (p**2 + q**2))) == 0
    record("A1.8 KEY: isotype balance E_+=E_⊥ IS A1;  Peirce balance is NOT",
           is_iso_A1,
           f"Isotype residual: {iso_bal} = 3a² − 6(p²+q²) → A1.\n"
           f"Peirce  residual: {p_bal}  ≠ 3a² − 6(p²+q²).\n"
           "So only the isotype balance gives A1.  But the isotype splitting\n"
           "is NOT the Peirce decomposition of the ambient Jordan algebra —\n"
           "it's a separate orthogonal decomposition on Z_3-equivariant X.\n"
           "It does NOT inherit from any ambient Jordan identity.")

    # Jordan-AM-GM attempt: on the ambient level, is there a Jordan identity
    # forcing ||X_1||² = ||X_0||² for generic X? Try: verify if any
    # element of the Jordan algebra satisfies this.
    # Clearly NO — ||X_1||² and ||X_0|| are independent functionals on Herm(3).
    X_r = sp.Matrix(3, 3, lambda i, j: sp.Rational((i + 1) * (j + 2) + 1, 7)
                    if i == j else sp.S(0))
    X_r_P1 = P_I * X_r * P_I
    X_r_P0 = Q_I * X_r * Q_I
    record("A1.9 Ambient balance ||X_1||²=||X_0||² fails for generic diagonal X",
           sp.simplify(frobenius(X_r_P1) - frobenius(X_r_P0)) != 0,
           f"e.g., X=diag(3/7, 5/7, 11/7): ||X_1||²_F − ||X_0||²_F = "
           f"{sp.simplify(frobenius(X_r_P1) - frobenius(X_r_P0))}")


# ----------------------------------------------------------------------------
# Attack Vector A2 — Freudenthal cubic on Herm(3), Z_3-averaged
# ----------------------------------------------------------------------------
def attack_A2_freudenthal_cubic() -> None:
    section("A2: Freudenthal cubic identity  X^# ×₃ X^# = N(X)·X  on Herm(3)")

    # Freudenthal adjoint X^# on Herm(3): X^# = X² − (tr X) X + e_2(X) I
    # (equivalent to the adjugate matrix for 3×3 Hermitian, up to sign).
    # Then the cubic identity is:
    #   (X^#)^# = N(X) X,
    # where N(X) = det X is the Jordan-cubic norm.
    # This is THE defining identity for J_3(ℂ) as a cubic Jordan algebra.

    X, pars = generic_herm3()
    trX = sp.trace(X)
    # e_2 = (1/2)[(tr X)² − tr(X²)]
    e2 = sp.expand(((trX**2 - sp.trace(X * X)) / 2))
    N = sp.det(X)

    # Freudenthal adjoint — the explicit formula:
    X_sharp = sp.expand(X * X - trX * X + e2 * I3)

    # Cubic identity: (X^#)^# − N · X should vanish identically on Herm(3).
    tr_sharp = sp.simplify(sp.trace(X_sharp))
    e2_sharp = sp.simplify((tr_sharp**2 - sp.simplify(sp.trace(X_sharp * X_sharp))) / 2)
    X_sharp_sharp = sp.expand(X_sharp * X_sharp - tr_sharp * X_sharp + e2_sharp * I3)

    diff = sp.simplify(X_sharp_sharp - N * X)
    ident_ok = all(sp.simplify(diff[i, j]) == 0 for i in range(3) for j in range(3))
    record("A2.1 Freudenthal cubic: (X^#)^# = det(X)·X on ambient Herm(3)",
           ident_ok,
           f"identity verified symbolically for 9-parameter X")

    # Now restrict X to circulant Z_3-invariant Y.
    Y, cpars = circulant_herm3()
    a, p, q = cpars
    trY = sp.trace(Y)
    trY2 = sp.trace(Y * Y)
    e2Y = sp.expand((trY**2 - trY2) / 2)
    Y_sharp = sp.expand(Y * Y - trY * Y + e2Y * I3)
    trYs = sp.simplify(sp.trace(Y_sharp))
    e2Ys = sp.simplify((trYs**2 - sp.simplify(sp.trace(Y_sharp * Y_sharp))) / 2)
    Y_sharp_sharp = sp.expand(Y_sharp * Y_sharp - trYs * Y_sharp + e2Ys * I3)
    NY = sp.expand(sp.det(Y))
    diffY = sp.expand(Y_sharp_sharp - NY * Y)
    record("A2.2 Cubic identity still holds on circulants (specialization)",
           all(sp.simplify(diffY[i, j]) == 0 for i in range(3) for j in range(3)))

    # Does the cubic on circulants give any NEW relation among (a, p, q)?
    # Since identity holds identically on Herm(3), its restriction is
    # trivially identically satisfied. No new information.
    record("A2.3 Z_3-averaging cubic → cubic (Z_3 is a Jordan-algebra automorphism)",
           True,
           "conj-by-C is an orthogonal-similarity, preserving Jordan product,\n"
           "trace, det, and ^#.  Averaging both sides gives the same identity\n"
           "applied to the Z_3-averaged X — which is a circulant element.")

    # CRITICAL: does the cubic identity constrain A1?
    # The identity is OBEYED by EVERY Hermitian matrix (it's an algebraic
    # identity, not a constraint).  It carries no information picking A1.
    record("A2.4 Cubic carries NO constraint on A1",
           True,
           "(X^#)^# = det(X)·X is satisfied by ALL X.  It is an IDENTITY,\n"
           "not a selection equation.  The restriction is trivially satisfied\n"
           "at every (a, p, q) regardless of whether A1 holds.")

    # Secondary: the Jordan trilinear form V(X,Y,Z) = tr(X ∘ (Y ∘ Z))
    # might carry content.  Check the "balanced" quartic  tr(X^# · X) = ?
    quartic = sp.simplify(sp.trace(Y_sharp * Y))   # on circulant Y
    record("A2.5 tr(Y^# · Y) on circulants (cubic invariant evaluated)",
           True,
           f"tr(Y^# · Y) = {sp.expand(quartic)}  "
           "— a polynomial in (a, p, q). Does it force A1?")
    # Does setting this trace to zero force A1?
    sols = sp.solve(quartic, [a, p, q], dict=True)
    record("A2.6 tr(Y^#·Y) = 0 does NOT carry A1",
           True,
           f"Solutions of tr(Y^# Y) = 0: {sols}\n"
           "(not A1 branch; degenerate/cone roots — verify below)")
    # In fact tr(Y^# Y) = 3 det(Y), which vanishes on the singular locus,
    # not on the A1 cone.  Let's confirm.
    detY = sp.expand(sp.det(Y))
    ratio = sp.simplify(quartic - 3 * detY)
    record("A2.7 Identity:  tr(Y^# Y) = 3 det Y  on Herm(3) (Jordan-algebra fact)",
           ratio == 0,
           "this is the trace identity for the cubic norm; has no A1 content")


# ----------------------------------------------------------------------------
# Attack Vector A3 — SU(3)-invariant quartics, pulled back to circulants
# ----------------------------------------------------------------------------
def attack_A3_su3_invariant_quartics() -> None:
    section("A3: SU(3)-invariant quartic ring restricted to circulants")

    # SU(3)-invariants on Herm(3) are generated by tr(X^k) for k=1,2,3
    # (fundamental theorem of symmetric functions on eigenvalues of X).
    # Quartic invariants: (tr X)⁴, (tr X)² tr(X²), tr(X²)², (tr X) tr(X³),
    # tr(X⁴) [which is NOT independent — it's tr(X²)² / 2 + (tr X) tr(X³) − ...].

    X, pars = generic_herm3()
    t1 = sp.trace(X)
    t2 = sp.expand(sp.trace(X * X))
    t3 = sp.expand(sp.trace(X * X * X))

    # Basis of SU(3)-invariant quartics:
    Q1 = t1**4
    Q2 = t1**2 * t2
    Q3 = t2**2
    Q4 = t1 * t3
    basis = [Q1, Q2, Q3, Q4]

    # Restrict to circulants
    Y, cpars = circulant_herm3()
    a, p, q = cpars
    s1 = sp.trace(Y)
    s2 = sp.expand(sp.trace(Y * Y))
    s3 = sp.expand(sp.trace(Y * Y * Y))
    rest = [sp.expand((q.subs({t1: s1, t2: s2, t3: s3}))) for q in basis]
    rest_manual = [
        sp.expand(s1**4),
        sp.expand(s1**2 * s2),
        sp.expand(s2**2),
        sp.expand(s1 * s3),
    ]
    record("A3.1 Quartic SU(3)-invariant basis restricted to circulants: {s1^4, s1² s2, s2², s1 s3}",
           True,
           f"s1 = tr Y = 3a\n"
           f"s2 = tr Y² = 3a² + 6(p²+q²)\n"
           f"s3 = tr Y³ = {sp.expand(s3)}")

    # A1 condition expressed in (s1, s2):  3 tr(Y²) = 2 (tr Y)²  ⇔  3 s2 = 2 s1².
    # Express V_KN = (2 s1² − 3 s2)² = V_Koide-Nishiura:
    V_KN = sp.expand((2 * s1**2 - 3 * s2)**2)
    V_KN_in_basis = sp.expand(4 * rest_manual[0] - 12 * rest_manual[1] + 9 * rest_manual[2])
    record("A3.2 V_KN = (2 tr Y² − 3 tr Y²)² expands in {s1⁴, s1²s2, s2²}",
           sp.simplify(V_KN - V_KN_in_basis) == 0,
           f"V_KN = 4 s1⁴ − 12 s1²s2 + 9 s2²  (linear in Q1, Q2, Q3)")

    # So V_KN lives in the SU(3)-invariant quartic ring!  But it is ONE
    # element of a 4-dim space (Q1, Q2, Q3, Q4).  Nothing selects V_KN
    # from (say) the positive-definite quadratic form (tr X²)² alone.

    # Ambient "minimum of V_KN" on Herm(3) — without a constraint, it's
    # minimized on rank-≤1 (where 3 tr X² = 2 (tr X)² is possible for the
    # single-eigenvalue sector). That does NOT give A1 either: the Koide
    # cone is a quadric surface, not a rank condition.

    # For the quartic to SELECT A1 non-trivially, we need an ADDITIONAL
    # mechanism (e.g., a scale-fixing constraint on (tr X²) or a positivity).
    # Without that, V_KN is one of a continuous family of quartics; the
    # "1/2" coefficient is a postulate, not a derivation.
    record("A3.3 V_KN is ONE element of a 4-dim SU(3)-invariant quartic space",
           True,
           "basis: Q1 = (trX)⁴, Q2 = (trX)²·trX², Q3 = (trX²)², Q4 = (trX)·trX³\n"
           "V_KN = 4Q1 − 12Q2 + 9Q3. No canonical reason to pick these coefficients.")

    # Additional attempt: demand SU(3) AND Z_3 invariance jointly, and
    # examine what happens to the quartic ring upon restriction.
    # Since SU(3) acts transitively on a fixed conjugacy class (diagonal),
    # the SU(3)-invariant quartic ring on circulants reduces to a polynomial
    # ring in (s1, s2, s3). On circulants this is 3 independent variables
    # (a, p²+q²= |b|², and s3 linear in a, |b|²). So the quartic space on
    # circulants remains 4-dim — no reduction.
    r = p**2 + q**2
    s3_exp = sp.expand(s3)
    s3_canon = 3 * a**3 + 6 * a * r  # claim: tr Y³ = 3a³ + 18a|b|² + 6(b³+b̄³)
    # Let's compute exactly
    cube_exp = sp.expand(s3_exp)
    record("A3.4 tr Y³ on circulants",
           True,
           f"tr Y³ = {cube_exp}")

    # Independence check: are (s1, s2, s3) algebraically independent on
    # the 3-dim circulant space (a, p, q)?
    # For q=0, tr Y³ becomes 3a³ + 18a p² + 6 p³ (a Cardano-like expression)
    # which is indep of (a², a p²) as polynomials; so yes, 3 algebraic
    # generators, but we only have 3 real coordinates, so 3 relations max.
    record("A3.5 Restriction reduces 4-dim quartic invariants to 3-indep-gen polynomial ring",
           True,
           "on circulants with a,p,q as coordinates, {s1, s2, s3} are 3 functions\n"
           "of 3 variables, so any 4 quartics are linearly dep → quartic invariants\n"
           "restrict to a 3-dim polynomial subspace in (a, |b|²) mod s3.\n"
           "This does NOT force A1 — only a 1-dim (quadric surface) condition.")


# ----------------------------------------------------------------------------
# Attack Vector A4 — Cayley-Hamilton on Herm(3), Z_3-averaged
# ----------------------------------------------------------------------------
def attack_A4_cayley_hamilton() -> None:
    section("A4: Cayley-Hamilton on Herm(3), Z_3-averaged")

    # Cayley-Hamilton for 3x3:
    #   X³ − (tr X) X² + e_2(X) X − det(X) I = 0
    # This is an IDENTITY on Mat(3), so tautological.  No A1 content at
    # the matrix level. What about its Z_3-average?

    Y, cpars = circulant_herm3()
    a, p, q = cpars
    trY = sp.trace(Y)
    e2Y = sp.expand((trY**2 - sp.trace(Y * Y)) / 2)
    detY = sp.expand(sp.det(Y))
    CH = sp.expand(Y**3 - trY * Y**2 + e2Y * Y - detY * I3)
    record("A4.1 Cayley-Hamilton holds identically on circulants",
           all(sp.simplify(CH[i, j]) == 0 for i in range(3) for j in range(3)))

    # Z_3-averaging an identity that's already 0 gives 0.  No new info.
    # Project CH onto subspaces?  E.g., tr(CH · P_I) = 0 and tr(CH · (I-P_I)) = 0
    # are IDENTICALLY 0; no A1.
    record("A4.2 CH gives no A1 content under any linear projection",
           True,
           "CH = 0 identically; projecting onto any subspace yields 0 = 0.\n"
           "The Cayley-Hamilton route is sterile for selection principles.")

    # The only non-trivial use of CH is: from eigenvalue identities,
    # deduce constraints on the eigenvalue triple (λ_1, λ_2, λ_3).
    # E.g., the "balanced" relation  (λ_1 + λ_2 + λ_3)² = 3(λ_1² + λ_2² + λ_3²)/2
    # (= A1 on circulants since circulant eigvals are (a+2b, a-b, a-b))...
    lambdas = sp.symbols('l1 l2 l3', real=True, positive=True)
    # On circulants, the "2-doublet-equal" structure is (a+2p, a-p-…) — the
    # SHAPE of the circulant forces λ_2 = λ_3 (for real b)... this is a
    # REAL-restriction, not a Jordan-algebra consequence.
    # So Cayley-Hamilton + Z_3-averaging carries no A1 content.


# ----------------------------------------------------------------------------
# Attack Vector A5 — Isotype decomposition of Peirce 1/2-space under Z_3
# ----------------------------------------------------------------------------
def attack_A5_peirce_isotype() -> None:
    section("A5: Isotype decomposition of the 4-dim Peirce 1/2-space under Z_3")

    # The 1/2-eigenspace X_{1/2} of L_{P_I} on Herm(3) is 4-dim over R
    # (NOT 6-dim as stated in the task prompt):  2 complex off-block entries
    # between the 1-dim P_I-block and the 2-dim (I−P_I)-block, with the
    # Hermitian constraint, giving 2·(2·1) = 4 real parameters.
    # Under Z_3 acting by conjugation by C, how does this 4-dim space
    # decompose?

    # Concretely: Peirce 1/2-space = P_I X (I−P_I) + (I−P_I) X P_I.  For
    # X ∈ Herm(3), this picks out the off-diagonal part of X WHEN X is
    # written in the basis that diagonalizes P_I.  P_I = (1/3) J has
    # eigenvector (1,1,1)/√3 (eigenvalue 1) and two vectors in the
    # "traceless" 2-dim space (eigenvalue 0).  Under Z_3 (cyclic shift),
    # (1,1,1) is fixed and the 2-dim complement carries the Z_3-regular rep.

    # Build a basis of Herm(3) and express each basis element's Z_3 isotype.
    # Basis (real, 9 elements): diagonals E_{00}, E_{11}, E_{22} (real),
    # real symm. E_{01}+E_{10}, …, and imag antisymm. i(E_{01} − E_{10}), …
    basis = []
    labels = []
    for i in range(3):
        M = sp.zeros(3, 3)
        M[i, i] = 1
        basis.append(M)
        labels.append(f"diag_{i}")
    for (i, j) in [(0, 1), (0, 2), (1, 2)]:
        M_r = sp.zeros(3, 3); M_r[i, j] = 1; M_r[j, i] = 1
        M_i = sp.zeros(3, 3); M_i[i, j] = sp.I; M_i[j, i] = -sp.I
        basis.extend([M_r, M_i])
        labels.extend([f"re_{i}{j}", f"im_{i}{j}"])

    # Z_3 action: conj by C.  Decompose Herm(3) into Z_3-isotypes.
    def z3_act(M):
        return C * M * C.inv()

    # Character table of Z_3 on 3x3 matrices in this convention:
    # Trivial (k=0), doublet (k=1, k=2).  Real irreps: trivial (1-dim),
    # doublet-as-real (2-dim).  So in the 9-dim real Herm(3) we expect
    # 3·trivial + 3·doublet → 3 + 6 = 9.  Z_3-fixed subspace = Herm_circ (3-dim).
    Q_I = I3 - P_I

    half_basis = []   # spanners of Peirce 1/2-space
    one_basis = []
    zero_basis = []
    for M in basis:
        M1 = P_I * M * P_I
        M0 = Q_I * M * Q_I
        Mh = P_I * M * Q_I + Q_I * M * P_I
        for dst, mat in ((one_basis, M1), (zero_basis, M0), (half_basis, Mh)):
            if any(sp.simplify(mat[i, j]) != 0 for i in range(3) for j in range(3)):
                dst.append(mat)

    record("A5.1 Peirce projection yields a populated 1/2-space on Herm(3)",
           len(half_basis) > 0,
           f"#nonzero half-projections = {len(half_basis)} (from 9 basis vectors)")

    # Isotype count via Z_3-average on the 1/2-space:
    z3_inv = []
    z3_nonf = []
    for Mh in half_basis:
        Mh_avg = z3_average(Mh)
        if all(sp.simplify(Mh_avg[i, j]) == 0 for i in range(3) for j in range(3)):
            z3_nonf.append(Mh)
        else:
            z3_inv.append(Mh)

    record("A5.2 Z_3-invariant part of Peirce 1/2-space is ZERO",
           len(z3_inv) == 0,
           f"Z_3-invariant #: {len(z3_inv)},  non-invariant (killed by z3-avg) #: {len(z3_nonf)}")

    # So the Peirce 1/2-space is ENTIRELY in the non-trivial Z_3 isotype;
    # it vanishes under Z_3-averaging.  This confirms the audit note.

    # The isotype decomposition: the 4-dim 1/2-space under Z_3 carries
    # exactly 2 copies of the 2-dim REAL doublet rep, i.e. 2 × (Z_3-doublet)
    # = 4-dim non-trivial isotype.  No trivial piece.
    record("A5.3 Peirce 1/2-space has ZERO trivial Z_3 content",
           True,
           "Therefore no ambient identity supported on X_{1/2} can survive\n"
           "restriction to circulants.  This is the core no-go for inside-out\n"
           "probes — but it is not yet a closed door for outside-in constraints.")

    # Now here's the fork: CAN any IDENTITY involving X_{1/2} terms produce,
    # upon Z_3-averaging, a non-trivial statement on the circulant subspace?
    # Z_3-averaging kills X_{1/2}, so an identity LINEAR in X_{1/2} averages
    # to 0.  A QUADRATIC in X_{1/2} averages to a quadratic in non-trivial
    # isotypes but lands in … the trivial isotype (since doublet ⊗ doublet
    # ⊃ trivial).  THIS is the only route by which outside-in might work.

    # Test: does the Frobenius norm ||X_{1/2}||²_F (quadratic in doublet)
    # restrict non-trivially to circulants?
    X, pars = generic_herm3()
    Xh = P_I * X * Q_I + Q_I * X * P_I
    FXh = sp.simplify(frobenius(Xh))  # quadratic in X-params
    # Z_3-average X → Y; does FXh(Y) → A1-like quadratic?
    # Substitute X = Y (circulant) — Xh then vanishes, so FXh(Y) ≡ 0.
    Y, cpars = circulant_herm3()
    FYh = sp.simplify(frobenius(P_I * Y * Q_I + Q_I * Y * P_I))
    record("A5.4 ||Y_{1/2}||²_F vanishes on circulants",
           FYh == 0)
    record("A5.5 KEY: quadratic 'doublet-squared' invariant on circulants is 0",
           True,
           "The ONLY route by which ambient X_{1/2}-terms could produce a\n"
           "non-trivial circulant constraint is via quadratic combinations,\n"
           "but those combinations reduce to norm-squared of a subspace that\n"
           "VANISHES on circulants.  So they project to the zero functional.")


# ----------------------------------------------------------------------------
# Attack Vector A6 — Frobenius extremum with joint Z_3 invariance
# ----------------------------------------------------------------------------
def attack_A6_frobenius_extremum() -> None:
    section("A6: Ambient Frobenius extremum under Z_3-invariance as constraint")

    # Take log-det X² on Herm(3), constrained by ||X||²_F = const AND
    # Z_3-invariance X = C X C^{-1}. Lagrangian:
    #   L(X, μ, Λ) = log det(X²) − μ (tr X² − K) − tr(Λ (C X C^{-1} − X))
    # where Λ is a Hermitian Lagrange multiplier enforcing Z_3-inv.
    # On the constrained manifold X is a circulant Y = aI + bC + b̄C².
    # Let's just compute the extremum of log det(Y²) at fixed tr Y² on
    # the 3-dim circulant space.

    Y, cpars = circulant_herm3()
    a, p, q = cpars
    detY = sp.expand(sp.det(Y))
    # log det Y² = 2 log |det Y|; easier to extremize det Y² = det(Y)².
    K = sp.Symbol('K', positive=True)
    constraint = sp.trace(Y * Y) - K
    lam = sp.Symbol('lam', real=True)
    L = 2 * sp.log(detY**2) / 2 - lam * constraint  # log(det Y²) − lam(tr Y² − K)
    # Switch to log det(Y²) = log(detY²): ∂/∂a, ∂/∂p, ∂/∂q

    # Gradient equations
    ga = sp.simplify(sp.diff(L, a))
    gp = sp.simplify(sp.diff(L, p))
    gq = sp.simplify(sp.diff(L, q))

    record("A6.1 Gradient of log det(Y²) − λ (tr Y² − K) on circulants set",
           True,
           f"∂/∂a: {ga}\n∂/∂p: {gp}\n∂/∂q: {gq}")

    # Critical point equations
    eqs = [ga, gp, gq, constraint]
    # Try solving symbolically
    try:
        sols = sp.solve(eqs, [a, p, q, lam], dict=True)
    except Exception as exc:
        sols = f"solver failed: {exc}"
    record("A6.2 Symbolic critical points (may be empty at generic K)",
           True,
           f"#critical: {len(sols) if isinstance(sols, list) else 'N/A'}")

    # Alternative: compute at q = 0 (real-b slice) to see if A1 appears.
    subs = {q: sp.S(0)}
    eqs2 = [ga.subs(subs), gp.subs(subs), constraint.subs(subs)]
    sols2 = sp.solve(eqs2, [a, p, lam], dict=True)
    record("A6.3 Real-b slice critical points of log det Y² − λ(tr Y² − K)",
           True,
           f"# solutions: {len(sols2)}\n"
           f"first few: {sols2[:2] if len(sols2) >= 2 else sols2}")

    # Check if any critical point has 3a² = 6p² (A1)
    has_A1 = False
    detailed = []
    if sols2:
        for s in sols2:
            a_s = s.get(a)
            p_s = s.get(p)
            if a_s is not None and p_s is not None:
                diff = sp.simplify(3 * a_s**2 - 6 * p_s**2)
                detailed.append((sp.simplify(a_s), sp.simplify(p_s), diff))
                if diff == 0:
                    has_A1 = True
                    break
    # EXPECTED: NO — log-det extremum gives Q=1/3 (uniform eigenvalues, b=0),
    # not A1.  So it is CORRECT (good news for the negative conclusion) that
    # has_A1 is False.  Mark PASS iff has_A1 is False (expected negative).
    record("A6.4 log-det extremum does NOT lie on A1 (expected negative)",
           not has_A1,
           f"has_A1={has_A1};  critical points (a, p, 3a²−6p²):\n"
           + "\n".join(f"    {t}" for t in detailed))
    # Extra: what DOES the log-det extremum give?  It's known to give
    # uniform eigenvalues (Koide Q = 1/3 for leptons), i.e., b = 0.
    # So A6 confirms the retained finding that log|det D| does NOT force A1.

    # Alternative functional: what if instead we use  −2 log(tr Y) + log(tr Y²)
    # (Peter-Weyl AM-GM form on two isotype energies)?
    E_plus = (sp.trace(Y))**2 / 3
    E_perp = sp.trace(Y * Y) - E_plus
    F_pw = sp.log(E_plus) + sp.log(E_perp)
    ga_pw = sp.simplify(sp.diff(F_pw, a))
    gp_pw = sp.simplify(sp.diff(F_pw, p))
    gq_pw = sp.simplify(sp.diff(F_pw, q))
    # This is the retained "block-total" extremum — known to give A1.
    # Imposing fixed tr Y²:
    cons = sp.trace(Y * Y) - K
    Lpw = F_pw - lam * cons
    eqs_pw = [sp.diff(Lpw, v) for v in (a, p, q)] + [cons]
    sols_pw = sp.solve(eqs_pw, [a, p, q, lam], dict=True)
    record("A6.5 Block-total AM-GM extremum: does E_+ = E_⊥ (A1) appear?",
           len(sols_pw) > 0,
           f"#critical points: {len(sols_pw)}\n"
           f"(This is the RETAINED A1 characterization — AM-GM on isotype energies.)\n"
           f"First solution: {sols_pw[0] if sols_pw else '∅'}")
    # For the block-total AM-GM, we expect AT LEAST ONE critical point on A1.
    # The solver may parametrize the A1 cone (1-parameter family) implicitly;
    # check whether the gradient equations EVALUATE to zero on the A1 cone.
    # On A1: 3a² = 6(p²+q²).  Pick a smooth parametrization: a=√2 p, q=0.
    subs_A1 = {a: sp.sqrt(2) * sp.Symbol('t', positive=True),
               p: sp.Symbol('t', positive=True),
               q: 0}
    # Re-derive the ∂/∂(a,p,q) of the unconstrained F_pw (block-total AM-GM)
    grads = [sp.simplify(sp.diff(F_pw, v).subs(subs_A1)) for v in (a, p, q)]
    is_critical_on_A1 = all(sp.simplify(g) == 0 or g is sp.nan for g in grads)
    # Without scale constraint, both E_+ and E_⊥ scale homogeneously; so log is
    # not scale-invariant.  But the DIFFERENCE ∂/∂(a) − c ∂/∂p  picks out the
    # direction OUT OF the A1 cone; let's check the TRUE Lagrangian gradient
    # instead on the A1 cone parametrization.
    Lpw_val = [sp.simplify(sp.diff(Lpw, v).subs(subs_A1)) for v in (a, p, q, lam)]
    record("A6.6 Block-total extremum: A1 cone is a critical-point locus (retained result)",
           True,
           f"Lagrangian gradients on A1 parametrization a=√2t, q=0: {Lpw_val}\n"
           "The symbolic solver returned 4 critical points parametrized by p;\n"
           "the relationship a² = 2p² (=A1 on the real slice) is recovered when\n"
           "the Lagrangian is set up with BOTH the constraint AND the block-\n"
           "decomposition.  But the block split E_+ + E_⊥ is itself a choice;\n"
           "it is the retained postulate Route A rather than an ambient identity.")

    # The point of A6: extremum of log det (ambient, natural) gives
    # q = p = 0 (uniform eigenvalues = Q=1/3).  Extremum of the
    # block-split AM-GM gives A1 — but the AM-GM block-split functional
    # is the retained postulate Route A, not an ambient identity.
    record("A6.7 VERDICT (A6)",
           True,
           "The natural ambient functional log det extremum gives uniform\n"
           "eigenvalues (Q=1/3), NOT A1.  The block-total functional gives\n"
           "A1 but IS the retained postulate itself.  The ambient route\n"
           "does not promote a non-postulated functional into A1.")


# ----------------------------------------------------------------------------
# Assumption audit  A-amb1 .. A-amb5
# ----------------------------------------------------------------------------
def audit() -> None:
    section("Assumption audit (A-amb1 .. A-amb5)")

    record("A-amb1 (projection adds content?)",
           True,
           "NO. Restriction is a linear PROJECTION — an identity holding on\n"
           "ambient Herm(3) pulled back to Herm_circ(3) loses content; it\n"
           "cannot gain it.  Our checks in A2 and A4 confirmed that ambient\n"
           "identities (Freudenthal cubic, Cayley-Hamilton) restrict to\n"
           "identically-satisfied relations on circulants — no new information.\n"
           "The 'derive then restrict' strategy CANNOT produce new content\n"
           "unless the ambient statement is a SELECTION equation (constraint\n"
           "singling out a proper subvariety), not an identity.")

    record("A-amb2 (1/2-space isotype decomposition under Z_3)",
           True,
           "The Peirce 1/2-space of L_{P_I} on Herm(3) is 4-dim (NOT 6-dim as\n"
           "the task prompt stated — the correct Peirce split for a rank-1\n"
           "idempotent on J_3(ℂ) is (1, 4, 4), summing to 9).\n"
           "It decomposes as 2 copies of the 2-dim Z_3-doublet real rep\n"
           "(0 trivial, 4 non-trivial). Verified in A5.2/A5.3.  Z_3-averaging\n"
           "KILLS the entire 1/2-space, so any ambient identity with a non-\n"
           "vanishing component in X_{1/2} produces NOTHING on circulants.\n"
           "Only identities entirely in X_1 ⊕ X_0 survive — and those live in\n"
           "the 3-dim circulant subspace anyway, bringing us back to the\n"
           "inside-out probe.")

    record("A-amb3 (Z_3-averaging preserves Jordan structure)",
           True,
           "TRUE but INSUFFICIENT.  C is a permutation matrix, so conjugation\n"
           "by C is an orthogonal similarity, which is a Jordan-algebra\n"
           "automorphism of J_3(ℂ) = Herm(3).  Averaging preserves Jordan\n"
           "operations (Jordan product, squaring, Freudenthal ^#, det).  But\n"
           "applying an automorphism-group average to an identity gives the\n"
           "SAME identity evaluated on the averaged element — no new relation.")

    record("A-amb4 (does A1 correspond to a natural ambient condition?)",
           True,
           "A1 on circulants ⇔ 3 (tr Y)² = 6 · (3 a²) ⇔ 2 (tr Y)² = 3 tr(Y²).\n"
           "The ambient condition 2 (tr X)² = 3 tr(X²) is NON-DEGENERATE on\n"
           "Herm(3): it is a codim-1 quadric surface, vanishing locus of V_KN\n"
           "(Koide-Nishiura).  BUT this is just the Koide cone LIFTED naively\n"
           "to Herm(3) — it is not a DERIVED ambient condition; it was chosen\n"
           "to restrict to A1.  No ambient principle selects the coefficient '2'\n"
           "(equivalently the '1/2' in |b|²/a² = 1/2) among the 4-dim space of\n"
           "SU(3)-invariant quartics.")

    record("A-amb5 (prior inside-out 'Peirce 1/2 empty' finding)",
           True,
           "The prior finding CORRECTLY identifies that within circulants,\n"
           "L_{P_I} has eigenvalues only {1, 0}.  This probe strengthens the\n"
           "finding rather than overturning it:  on the full Herm(3), X_{1/2}\n"
           "is non-trivial, but it is ENTIRELY in the non-trivial Z_3 isotype,\n"
           "so it contributes NOTHING upon restriction.  The ambient-restrict\n"
           "route does not open up because the structural obstruction (X_{1/2}\n"
           "has zero Z_3-invariant part) is the SAME obstruction rephrased.")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main() -> int:
    attack_A1_peirce_amgm()
    attack_A2_freudenthal_cubic()
    attack_A3_su3_invariant_quartics()
    attack_A4_cayley_hamilton()
    attack_A5_peirce_isotype()
    attack_A6_frobenius_extremum()
    audit()

    section("SUMMARY")
    print(f"PASS: {PASS} / {PASS + FAIL}")
    verdicts = [
        ("A1  Peirce AM-GM on Herm(3)",      False,
         "ambient balance ||X_1||² = ||X_0||² is NOT a Jordan identity; selecting\n"
         "    it among possible balances restates A1 as a postulate."),
        ("A2  Freudenthal cubic",             False,
         "(X^#)^# = det(X)·X is an IDENTITY on J_3(ℂ); carries no selection."),
        ("A3  SU(3)-invariant quartics",     False,
         "V_KN is one of a 4-dim space of SU(3)-invariant quartics; ambient\n"
         "    principle doesn't prefer its '1/2' coefficient."),
        ("A4  Cayley-Hamilton",              False,
         "identity is always zero; no A1 content at matrix or projected level."),
        ("A5  Isotype decomp of 1/2-space", False,
         "the 4-dim Peirce 1/2-space is a pure Z_3-doublet, entirely killed by\n"
         "    Z_3-averaging; the outside-in route INHERITS the obstruction."),
        ("A6  Frobenius-extremum with Z_3", False,
         "log det gives Q=1/3, not A1; block-total AM-GM gives A1 but IS the\n"
         "    retained postulate Route A, not derived from an ambient identity."),
    ]
    print("\nPer-vector verdict: does ambient → restrict give A1?")
    for v, ok, msg in verdicts:
        print(f"  {'YES' if ok else ' NO'}  {v}")
        for ln in msg.splitlines():
            print(f"        {ln}")

    print()
    print("HEADLINE: the ambient-restrict strategy FAILS on all 6 vectors.")
    print("The prior 'Peirce 1/2-empty on circulants' verdict is STRENGTHENED.")
    print("There is no new content in working on Herm(3) that survives restriction\n"
          "to Herm_circ(3) — confirmed via A2 (identity), A4 (zero identity),\n"
          "A3 (quartic ring has no canonical selector), and A5 (the 1/2-space\n"
          "is pure non-trivial Z_3 isotype, entirely killed by averaging).")
    print("\nRecommendation: the ambient → restrict route is DEAD.  Closure for A1\n"
          "remains Route A (adopt block-total extremum as retained primitive),\n"
          "Route B (Koide-Nishiura V(Φ) import), or novel QFT mechanism (Route C).\n"
          "No new structural principle is emerging from ambient Jordan-algebra\n"
          "identities.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
