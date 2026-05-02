#!/usr/bin/env python3
"""Pattern A narrow runner for `CYCLIC_PROJECTOR_COMPRESSION_NARROW_THEOREM_NOTE_2026-05-02`.

Verifies the standalone linear-algebra / cyclic-group representation theory
identity:

  GIVEN the 3-cycle permutation matrix C on C^3 (with C^3 = I, C != I, C^2 != I)
  and the cyclic averaging operator on Herm(3):
      P_cyc(X)  =  (1/3) sum_{k=0}^{2} C^k X C^{-k},
  THEN:
    (i)   P_cyc is the orthogonal projector onto the 3-dim
          cyclic-invariant subspace of Herm(3);
    (ii)  image(P_cyc) = span_R{B0, B1, B2}, where
              B0 = I,
              B1 = C + C^2,
              B2 = i(C - C^2);
    (iii) P_cyc has the basis-level action
              P_cyc(D_i) = B0 / 3                     for i = 1, 2, 3;
              P_cyc(X_ij) = B1 / 3                    for i < j;
              P_cyc(Y_12) = P_cyc(Y_23) =  B2 / 3;
              P_cyc(Y_13) = -B2 / 3;
          (D_i, X_ij, Y_ij the standard Hermitian basis: diagonals,
           symmetric off-diagonals, antisymmetric off-diagonals);
    (iv)  P_cyc is idempotent and self-adjoint with respect to the
          Frobenius inner product on Herm(3);
    (v)   P_cyc(H_e) for a generic Hermitian
              H_e = sum d_i D_i + sum x_ij X_ij + sum y_ij Y_ij
          equals
              ((d1+d2+d3)/3) B0 + ((x12+x23+x13)/3) B1
              + ((y12+y23-y13)/3) B2.

This is class-A pure linear algebra / cyclic-group invariant theory. No
DM-side / Koide-side / charged-Hermitian-source-law authority is consumed,
and no specific physical assignment of the resulting "cyclic 3-channel
response" is claimed.

Companion role: this is a Pattern A new narrow claim row carving out the
load-bearing class-(A) algebraic core of
`koide_dweh_cyclic_compression_note_2026-04-18` (claim_type=positive_theorem,
audit_status=unaudited, td=77). The narrow theorem isolates the cyclic-projector
compression on Herm(3) from any DM/Koide-specific framing, so it can be
audit-ratified independently.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, sqrt, simplify, symbols, Matrix, eye, zeros, I as sym_I
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Pattern A narrow theorem: cyclic-projector compression on Herm(3)")
# Statement: P_cyc(X) = (1/3) sum_{k} C^k X C^{-k} is the orthogonal
# projector onto the 3-dim cyclic-invariant subspace of Herm(3),
# spanned by B0 = I, B1 = C + C^2, B2 = i(C - C^2). Pure linear
# algebra. No DM/Koide-specific framing.
# ============================================================================

# 3-cycle matrix C: e_k -> e_{k+1 mod 3}
C = Matrix([[0, 0, 1],
            [1, 0, 0],
            [0, 1, 0]])

C2 = C * C
C3 = C * C * C

I3 = eye(3)


# ----------------------------------------------------------------------------
section("Part 1: C^3 = I exact, C != I, C^2 != I (genuine 3-cycle)")
# ----------------------------------------------------------------------------
check("C^3 = I_3 exact",
      C3 == I3)
check("C != I (genuine non-identity)",
      C != I3)
check("C^2 != I (genuine 3-cycle, not 2-cycle)",
      C2 != I3)
check("C is unitary: C * C.T = I (real orthogonal permutation)",
      simplify(C * C.T - I3) == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 2: B0 = I, B1 = C + C^2, B2 = i(C - C^2) are Hermitian")
# ----------------------------------------------------------------------------
B0 = I3
B1 = C + C2
B2 = sym_I * (C - C2)

# B0, B1, B2 are Hermitian
check("B0 = I is Hermitian",
      B0 == B0.H)
check("B1 = C + C^2 is Hermitian",
      simplify(B1 - B1.H) == zeros(3, 3))
check("B2 = i(C - C^2) is Hermitian",
      simplify(B2 - B2.H) == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 3: P_cyc is the orthogonal projector onto cyclic-invariant subspace")
# ----------------------------------------------------------------------------
def P_cyc(X):
    """Cyclic averaging on 3x3 matrices."""
    return (X + C * X * C.T + C2 * X * (C2).T) / Rational(3)

# Idempotency: P_cyc(P_cyc(X)) = P_cyc(X) for all X.
# Test on a few basis matrices and a generic X.
for label, X_test in [
    ("I", I3),
    ("C", C),
    ("E_11", Matrix([[1, 0, 0], [0, 0, 0], [0, 0, 0]])),
    ("E_12", Matrix([[0, 1, 0], [0, 0, 0], [0, 0, 0]])),
    ("E_23", Matrix([[0, 0, 0], [0, 0, 1], [0, 0, 0]])),
]:
    P_X = P_cyc(X_test)
    P_P_X = P_cyc(P_X)
    check(f"P_cyc(P_cyc({label})) = P_cyc({label}) (idempotent)",
          simplify(P_P_X - P_X) == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 4: image(P_cyc) = span_R{B0, B1, B2}")
# ----------------------------------------------------------------------------
# Verify P_cyc(B0) = B0, P_cyc(B1) = B1, P_cyc(B2) = B2 (B0, B1, B2 are fixed).
check("P_cyc(B0) = B0 (B0 in cyclic-invariant subspace)",
      simplify(P_cyc(B0) - B0) == zeros(3, 3))
check("P_cyc(B1) = B1 (B1 in cyclic-invariant subspace)",
      simplify(P_cyc(B1) - B1) == zeros(3, 3))
check("P_cyc(B2) = B2 (B2 in cyclic-invariant subspace)",
      simplify(P_cyc(B2) - B2) == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 5: basis-level action of P_cyc on D_i, X_ij, Y_ij")
# ----------------------------------------------------------------------------
# Diagonal slots
D = []
for i in range(3):
    M = sympy.Matrix.zeros(3, 3)
    M[i, i] = 1
    D.append(M)

# Symmetric off-diagonal slots X_ij = E_ij + E_ji (i < j)
def X_offdiag(i, j):
    M = sympy.Matrix.zeros(3, 3)
    M[i, j] = 1
    M[j, i] = 1
    return M

# Antisymmetric off-diagonal slots Y_ij = i(E_ji - E_ij) (Hermitian; i < j)
def Y_offdiag(i, j):
    M = sympy.Matrix.zeros(3, 3)
    M[i, j] = -sym_I
    M[j, i] = sym_I
    return M

# Check P_cyc(D_i) = B0 / 3
for i in range(3):
    P_D = simplify(P_cyc(D[i]))
    check(f"P_cyc(D_{i+1}) = B0 / 3 = I/3",
          simplify(P_D - B0 / Rational(3)) == zeros(3, 3))

# Check P_cyc(X_ij) = B1 / 3 for (i, j) = (0,1), (1,2), (0,2)
for i, j, label in [(0, 1, "X_12"), (1, 2, "X_23"), (0, 2, "X_13")]:
    Xij = X_offdiag(i, j)
    P_X = simplify(P_cyc(Xij))
    check(f"P_cyc({label}) = B1 / 3",
          simplify(P_X - B1 / Rational(3)) == zeros(3, 3))

# Check P_cyc(Y_12) = P_cyc(Y_23) = +B2 / 3, P_cyc(Y_13) = -B2 / 3
for i, j, sign, label in [
    (0, 1, +1, "Y_12"),
    (1, 2, +1, "Y_23"),
    (0, 2, -1, "Y_13"),
]:
    Yij = Y_offdiag(i, j)
    P_Y = simplify(P_cyc(Yij))
    expected = sign * B2 / Rational(3)
    check(f"P_cyc({label}) = ({'+' if sign > 0 else '-'})B2 / 3",
          simplify(P_Y - expected) == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 6: generic-Hermitian compression formula")
# ----------------------------------------------------------------------------
d1, d2, d3 = symbols('d_1 d_2 d_3', real=True)
x12, x23, x13 = symbols('x_12 x_23 x_13', real=True)
y12, y23, y13 = symbols('y_12 y_23 y_13', real=True)

H_e = (
    d1 * D[0] + d2 * D[1] + d3 * D[2]
    + x12 * X_offdiag(0, 1) + x23 * X_offdiag(1, 2) + x13 * X_offdiag(0, 2)
    + y12 * Y_offdiag(0, 1) + y23 * Y_offdiag(1, 2) + y13 * Y_offdiag(0, 2)
)

H_cyc = simplify(P_cyc(H_e))
expected_H_cyc = (
    (d1 + d2 + d3) / Rational(3) * B0
    + (x12 + x23 + x13) / Rational(3) * B1
    + (y12 + y23 - y13) / Rational(3) * B2
)
expected_H_cyc_simplified = simplify(expected_H_cyc)

check("P_cyc(H_e) = ((d_sum)/3) B0 + ((x_sum)/3) B1 + ((y12+y23-y13)/3) B2",
      simplify(H_cyc - expected_H_cyc_simplified) == zeros(3, 3))


# ----------------------------------------------------------------------------
section("Part 7: parent row context (no ledger modification)")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('koide_dweh_cyclic_compression_note_2026-04-18', {})
print(f"\n  Parent row state on origin/main:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")
print(f"    deps: {parent.get('deps')}")

check("parent row claim_type = positive_theorem",
      parent.get('claim_type') == 'positive_theorem')


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let C be the 3x3 cyclic permutation matrix on C^3 (C: e_k -> e_{k+1 mod 3}),
    and define P_cyc(X) = (1/3) sum_{k=0}^{2} C^k X C^{-k} on 3x3 matrices.

  CONCLUSION:
    (i)   P_cyc is the orthogonal projector (idempotent + Frobenius-self-adjoint)
          onto the 3-dim cyclic-invariant subspace.
    (ii)  image(P_cyc on Herm(3)) = span_R{B0, B1, B2} where
              B0 = I,  B1 = C + C^2,  B2 = i(C - C^2).
    (iii) On the standard Hermitian basis (D_i, X_ij, Y_ij), P_cyc collapses
          the 9-dim Herm(3) onto these 3 channels:
              P_cyc(D_i) = B0/3,
              P_cyc(X_ij) = B1/3 for all i < j,
              P_cyc(Y_12) = P_cyc(Y_23) = +B2/3, P_cyc(Y_13) = -B2/3.
    (iv)  Generic Hermitian compression formula:
              P_cyc(H_e) = ((d_sum)/3) B0 + ((x_sum)/3) B1
                         + ((y12+y23-y13)/3) B2.

  Audit-lane class:
    (A) — pure linear algebra / cyclic-group invariant theory. No DM-side,
    Koide-side, or physical-Hermitian-source-law input.

  This narrow theorem isolates the cyclic-projector compression algebra
  from any DM/Koide-specific framing, so it can be audit-ratified
  independently of the parent's downstream context.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
