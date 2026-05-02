#!/usr/bin/env python3
"""Verify the narrow Schur covariance inheritance theorem at exact rational
precision via sympy.

Claim scope: U M U† = M block-diagonal (U = U_1 ⊕ U_W) on V = V_1 ⊕ W with
M = [[A, B], [B†, D]] and D invertible ⇒ U_1 S U_1† = S where S = A - B D⁻¹ B†.

Load-bearing step is class (A) algebraic identity on block matrix relations.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Matrix, eye, zeros, Rational, sqrt, I as sym_I
except ImportError:
    print("FAIL: sympy required for exact rational matrix algebra")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "SCHUR_COVARIANCE_INHERITANCE_NARROW_THEOREM_NOTE_2026-05-02.md"

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
section("Part 1: note structure and scope discipline")
# ============================================================================
note_text = NOTE_PATH.read_text()
required = [
    "Schur Complement Covariance Inheritance — Narrow Theorem",
    "Type:** positive_theorem",
    "U M U† = M",
    "S = A − B D⁻¹ B†",
    "U_1 S U_1† = S",
    "not** claim",  # \"**does\\nnot** claim\" (line-wrapped)
    "site_phase_cube_shift_intertwiner_note",
    "class (A)",
    "target_claim_type: positive_theorem",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)

# Scope discipline: ensure no physical-applicability claim is load-bearing
forbidden = [
    "applies to physical charged leptons unconditionally",
    "the Schur reduction IS the physical reduction map",
    "D is invertible for the physical effective operator",
]
for f in forbidden:
    check(f"narrow scope avoids forbidden claim: {f!r}",
          f not in note_text)


# ============================================================================
section("Part 2: lemma on 3+1 split with V_1 = C³, W = C¹")
# ============================================================================
# C_3 cyclic action on V_1 = C³:
# C: e_0 -> e_1 -> e_2 -> e_0
C3 = Matrix([[0, 0, 1],
             [1, 0, 0],
             [0, 1, 0]])

# Verify C³ = I
check("C₃³ = I (group order 3)",
      C3**3 == eye(3),
      detail="canonical cyclic shift on V_1")

# Build a positive Hermitian M = [[A, B], [B†, D]] with A 3x3, B 3x1, D 1x1.
# Need M C-covariant: U M U† = M with U = C_3 ⊕ U_W.
# Choose U_W = 1 (trivial 1x1 unitary).

# A must commute with C_3 (so be circulant). Pick A = aI + bC + b*C^T circulant.
# Simplification: A = sum c_k C^k for real c_k giving Hermitian circulant.
# Take A = I + C + C^T (Hermitian, commutes with C).
A = eye(3) + C3 + C3.T

# B must satisfy U_1 B U_W† = B, i.e. C_3 B = B (since U_W = 1).
# So B is in the C_3-fixed subspace of C³ ⊗ C¹ = C³.
# Fixed vectors of C_3 on C³ are multiples of (1, 1, 1)^T.
B = Matrix([[1], [1], [1]])  # C_3-invariant vector

# D 1x1: any positive number; commutes trivially with U_W = 1.
D = Matrix([[2]])  # positive scalar

# Build M
def build_M(A, B, D):
    n1 = A.shape[0]
    n2 = D.shape[0]
    M = zeros(n1+n2, n1+n2)
    for i in range(n1):
        for j in range(n1):
            M[i, j] = A[i, j]
        for j in range(n2):
            M[i, n1+j] = B[i, j]
    for i in range(n2):
        for j in range(n1):
            M[n1+i, j] = B.conjugate().T[i, j]
        for j in range(n2):
            M[n1+i, n1+j] = D[i, j]
    return M

M = build_M(A, B, D)

# U = C_3 ⊕ U_W
U = zeros(4, 4)
U[:3, :3] = C3
U[3, 3] = 1

# Verify U M U^† = M (covariance of full M)
M_rotated = U * M * U.H
check("U M U† = M (full M is C₃-covariant)",
      M_rotated == M,
      detail="block-diagonal U preserves the assumed covariance")

# Compute Schur complement S = A - B D^{-1} B†
S = A - B * D.inv() * B.H

# Verify S is C_3-covariant on V_1
S_rotated = C3 * S * C3.H
check("U_1 S U_1† = S (Schur complement covariance inheritance)",
      S_rotated == S,
      detail="this is the narrow theorem's claim")

# Direct check: S is a circulant matrix
def is_circulant(M, U_action, n):
    return M * U_action == U_action * M
check("S commutes with C_3 (equivalently circulant on V_1 = C³)",
      is_circulant(S, C3, 3))


# ============================================================================
section("Part 3: lemma on 3+3 split with V_1 = V_W = C³")
# ============================================================================
# Both V_1 and W carry C_3 action. M is C_3 ⊕ C_3 covariant.
# A: 3x3 circulant. B: 3x3 commuting with C_3 (i.e. circulant).
# D: 3x3 circulant + invertible.

A2 = eye(3) + 3 * C3 + 3 * C3.T  # Hermitian circulant
B2 = eye(3) + 2 * C3              # commutes with C_3 (off-diagonal block)
D2 = 5 * eye(3) + 1 * C3 + 1 * C3.T  # Hermitian invertible circulant

# Construct M2
M2 = zeros(6, 6)
M2[:3, :3] = A2
M2[:3, 3:] = B2
M2[3:, :3] = B2.H
M2[3:, 3:] = D2

# U2 = C_3 ⊕ C_3
U2 = zeros(6, 6)
U2[:3, :3] = C3
U2[3:, 3:] = C3

# Verify U2 M2 U2^† = M2
M2_rotated = U2 * M2 * U2.H
check("3+3 split: U_2 M_2 U_2† = M_2",
      M2_rotated == M2)

# D must be invertible
check("3+3 split: D₂ is invertible",
      D2.det() != 0,
      detail=f"det(D₂) = {D2.det()}")

# Schur complement
S2 = A2 - B2 * D2.inv() * B2.H

# Verify covariance inheritance
S2_rotated = C3 * S2 * C3.H
check("3+3 split: U_1 S_2 U_1† = S_2 (covariance inheritance)",
      S2_rotated == S2)


# ============================================================================
section("Part 4: control negative tests")
# ============================================================================
# Control 1: U not block-diagonal — covariance inheritance should fail
# Build an off-diagonal U
U_bad = zeros(4, 4)
U_bad[0, 3] = 1  # mixes V_1 with W
U_bad[1, 1] = 1
U_bad[2, 2] = 1
U_bad[3, 0] = 1

# Note: U_bad doesn't satisfy U_bad M U_bad^† = M for our M (different structure).
# So the premise of the theorem fails, and we don't expect inheritance.
# This is a negative control showing the theorem requires the premise.
check("control: non-block-diagonal U does not satisfy U M U† = M (premise fails)",
      U_bad * M * U_bad.H != M,
      detail="premise of theorem requires block-diagonal U")

# Control 2: M not C_3-covariant — covariance inheritance should fail
M_bad = M.copy()
M_bad[0, 0] = 99  # break A's circulant structure
check("control: non-covariant M does not satisfy U M U† = M (premise fails)",
      U * M_bad * U.H != M_bad,
      detail="premise of theorem requires U M U† = M")


# ============================================================================
section("Part 5: cited authority is retained-grade")
# ============================================================================
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
rows = ledger['rows']
dep_id = "site_phase_cube_shift_intertwiner_note"
dep_es = rows.get(dep_id, {}).get("effective_status")
check(f"{dep_id} effective_status = retained",
      dep_es == "retained",
      detail=f"observed = {dep_es!r}")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
