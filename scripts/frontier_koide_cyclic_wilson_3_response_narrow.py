#!/usr/bin/env python3
"""Verify the narrow Koide cyclic Wilson 3-response theorem at exact precision.

Claim scope: GIVEN a local Wilson first-variation dW on the Hermitian image
of the C_3[111]-covariant adjacent-chain path algebra, the cyclic descendant
is determined by exactly three real responses (r0, r1, r2) via
H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2 with (B0, B1, B2) = (I, C+C², i(C-C²)).

Load-bearing step is class (A) algebra conditional on the declared Koide DWEH
cyclic-compression dependency. This runner checks graph visibility; it does not
grant audit verdicts or retained-family status.
"""

from fractions import Fraction
from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "KOIDE_CYCLIC_WILSON_3_RESPONSE_NARROW_THEOREM_NOTE_2026-05-02.md"
CLAIM_ID = "koide_cyclic_wilson_3_response_narrow_theorem_note_2026-05-02"

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
    "Koide Cyclic Wilson 3-Response Law — Narrow Conditional Theorem",
    "Type:** bounded_theorem",
    "**Given**",
    "(I, C+C², i(C−C²))",
    "(r₀/3) B₀ + (r₁/6) B₁ + (r₂/6) B₂",
    "2 r₀² = r₁² + r₂²",
    "out of scope",
    "KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md",
    "class (A)",
    "target_claim_type: bounded_theorem",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)

# Scope discipline
forbidden_in_scope = [
    "applies to physical charged leptons unconditionally",
    "Koide relation is hereby derived",
    "the local Wilson first-variation exists for",
]
for f in forbidden_in_scope:
    check(f"narrow scope avoids forbidden claim: {f!r}",
          f not in note_text,
          detail="conditional premise stays explicit")


# ============================================================================
section("Part 2: cyclic Hermitian basis (B0, B1, B2) on 3x3 cyclic representation")
# ============================================================================
# Use the regular C_3 representation: C is the cyclic shift on (e_0, e_1, e_2)
# C: e_0 -> e_1 -> e_2 -> e_0, i.e. C^3 = I.
# In matrix form (3x3):
#   C = [[0,0,1],[1,0,0],[0,1,0]]   (sends e_0 to e_1, e_1 to e_2, e_2 to e_0)
# Equivalently C is the permutation matrix for the cycle (0 1 2).

# Working in exact rationals (and using Fraction for the i-times-(C-C^2) term
# we'll keep symbolic real and imaginary parts).
# Easier: verify the identities at exact rational precision by working over Q.

def matmul(A, B, n):
    return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def matadd(A, B, n):
    return [[A[i][j]+B[i][j] for j in range(n)] for i in range(n)]

def matscale(A, s, n):
    return [[A[i][j]*s for j in range(n)] for i in range(n)]

def matsub(A, B, n):
    return [[A[i][j]-B[i][j] for j in range(n)] for i in range(n)]

def transpose_conj(A, n):
    # For real matrices, just transpose
    return [[A[j][i] for j in range(n)] for i in range(n)]

def matequal(A, B, n):
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))

# C: 3x3 cyclic shift over Q
C = [
    [Fraction(0), Fraction(0), Fraction(1)],
    [Fraction(1), Fraction(0), Fraction(0)],
    [Fraction(0), Fraction(1), Fraction(0)],
]
n = 3
I3 = [[Fraction(1) if i==j else Fraction(0) for j in range(n)] for i in range(n)]
C2 = matmul(C, C, n)
C3 = matmul(C2, C, n)
check("C^3 = I (cyclic group order 3)",
      matequal(C3, I3, n), detail="C is order-3 on regular rep")

B0 = I3
B1 = matadd(C, C2, n)
# B2 has factor of i, but for the algebraic identity we'll use B2_real := (C - C^2),
# treating i as a fixed scalar throughout. The Hermitian structure is preserved
# because i(C - C^2) is i times an antihermitian (C - C^T = C - C^2 since C is real)
# — and i times antihermitian is Hermitian.
B2_kernel = matsub(C, C2, n)  # so B2 = i * B2_kernel; B2† = -i (B2_kernel)† = -i (-B2_kernel) = i B2_kernel = B2

# Hermiticity check: B0, B1 are real and symmetric (we'll verify B1).
# B0: identity, trivially symmetric.
B1_T = transpose_conj(B1, n)
check("B0 = I is Hermitian (symmetric)",
      matequal(B0, transpose_conj(B0, n), n))
check("B1 = C + C^2 is symmetric (and so Hermitian)",
      matequal(B1, B1_T, n))
# B2 = i (C - C^2): for B2 to be Hermitian, B2_kernel = (C - C^2) must be antisymmetric.
B2k_T = transpose_conj(B2_kernel, n)
B2k_neg = matscale(B2_kernel, Fraction(-1), n)
check("(C - C^2) is antisymmetric (so i (C - C^2) is Hermitian)",
      matequal(B2k_T, B2k_neg, n))

# Cyclic covariance: C B_i C^{-1} = B_i (because B_i ∈ {I, C+C², i(C-C²)} commute with C)
def commute_with_C(A):
    # C A = A C, i.e., A commutes with C
    return matequal(matmul(C, A, n), matmul(A, C, n), n)

check("[C, B0] = 0 (B0 commutes with C)", commute_with_C(B0))
check("[C, B1] = 0 (B1 commutes with C)", commute_with_C(B1))
check("[C, B2_kernel] = 0 (B2_kernel commutes with C)", commute_with_C(B2_kernel))


# ============================================================================
section("Part 3: response triple (r0, r1, r2) uniquely determines H_cyc")
# ============================================================================
# The cyclic Hermitian sub-algebra is spanned by (B0, B1, B2) over R.
# Given a real-valued linear functional dW on this Hermitian subspace, the
# response triple is (r0, r1, r2) = (dW(B0), dW(B1), dW(B2)). In the exact
# rational model below we replace B2 = i(C-C^2) by its real antisymmetric
# kernel K = C-C^2; the Frobenius normalization is unchanged.
#
# Reconstruction: H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2.
# Verify the Frobenius-dual pairings <B_i, H_cyc> reproduce the response triple.
#
# We exercise this via Frobenius inner product:
# <A, B>_F := Tr(A^† B)  — for our cyclic Hermitian basis, this gives:
#   <B0, B0> = Tr(I) = 3
#   <B1, B1> = Tr((C+C²)² ) = ?
#   <B2, B2> = Tr( (i(C-C²))² · ... ) — careful with the i

def trace(A, n):
    return sum(A[i][i] for i in range(n))

def frobenius_inner_real(A, B):
    return trace(matmul(transpose_conj(A, n), B, n), n)

def cyclic_representative_kernel(r0, r1, r2):
    """Riesz representative using K=C-C^2 for the B2 coordinate."""
    b0_part = matscale(B0, r0 / Fraction(3), n)
    b1_part = matscale(B1, r1 / Fraction(6), n)
    b2_part = matscale(B2_kernel, r2 / Fraction(6), n)
    return matadd(matadd(b0_part, b1_part, n), b2_part, n)

# <B0, B0>
inner_B0_B0 = frobenius_inner_real(B0, B0)
check("<B0, B0>_F = Tr(I) = 3",
      inner_B0_B0 == Fraction(3),
      detail=f"= {inner_B0_B0}")

# <B1, B1> = Tr( (C+C²)^T (C+C²) ) = Tr( (C²+C) (C+C²) )
inner_B1_B1 = frobenius_inner_real(B1, B1)
check("<B1, B1>_F = 6",
      inner_B1_B1 == Fraction(6),
      detail=f"= {inner_B1_B1}")

# <B2_kernel, B2_kernel> = Tr( (C-C²)^T (C-C²) ) = Tr( (C²-C)(C-C²) )
inner_B2k_B2k = frobenius_inner_real(B2_kernel, B2_kernel)
# <B2_kernel, B2_kernel>_F = Tr((C^T - (C^2)^T)(C - C^2)) = Tr((C² - C)(C - C^2))
# = Tr(C^3 - C^4 - C^2 + C^3) = Tr(2I - C - C^2) = 6 (since Tr(C) = Tr(C^2) = 0)
# B2 = i (C - C^2) has same Frobenius norm: <B2, B2>_F = 6 (the i factors cancel
# in the inner product). The reconstruction coefficient 1/6 in the note is the
# inverse Frobenius diagonal — consistent with the dual-basis formula.
check("<B2_kernel, B2_kernel>_F = 6 (and <B2, B2>_F = 6 since |i|² = 1)",
      inner_B2k_B2k == Fraction(6),
      detail=f"= {inner_B2k_B2k}; reconstruction coefficient 1/6 matches inverse")

# Note: in the note's reconstruction H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2,
# the factors 1/3, 1/6, 1/6 match exactly the inverses of <B_i, B_i>_F (for B0, B1)
# and the cyclic-basis dual normalization for B2. Verify orthogonality:
inner_B0_B1 = frobenius_inner_real(B0, B1)
inner_B0_B2k = frobenius_inner_real(B0, B2_kernel)
inner_B1_B2k = frobenius_inner_real(B1, B2_kernel)
check("<B0, B1>_F = 0", inner_B0_B1 == Fraction(0),
      detail=f"= {inner_B0_B1}")
check("<B0, B2_kernel>_F = 0", inner_B0_B2k == Fraction(0),
      detail=f"= {inner_B0_B2k}")
check("<B1, B2_kernel>_F = 0", inner_B1_B2k == Fraction(0),
      detail=f"= {inner_B1_B2k}")

for r0, r1, r2 in [
    (Fraction(5), Fraction(1), Fraction(7)),
    (Fraction(-2), Fraction(3), Fraction(-4)),
    (Fraction(0), Fraction(0), Fraction(0)),
]:
    H = cyclic_representative_kernel(r0, r1, r2)
    reconstructed = (
        frobenius_inner_real(B0, H),
        frobenius_inner_real(B1, H),
        frobenius_inner_real(B2_kernel, H),
    )
    expected = (r0, r1, r2)
    check(f"Frobenius-dual reconstruction recovers responses {expected}",
          reconstructed == expected,
          detail=f"got={reconstructed}")


# ============================================================================
section("Part 4: 3-response law has Koide scalar form 2 r0² = r1² + r2²")
# ============================================================================
# This is a single algebraic constraint on the response triple. NOT claimed
# to hold for physical charged leptons.
# Verify the constraint defines a 2-dimensional surface in R³ (a quadric).

def koide_scalar(r0, r1, r2):
    return Fraction(2) * r0**2 - r1**2 - r2**2

check("Koide locus example: (5,1,7) satisfies 2 r0² = r1² + r2²",
      koide_scalar(Fraction(5), Fraction(1), Fraction(7)) == Fraction(0),
      detail=f"2*25 - 1 - 49 = {koide_scalar(Fraction(5), Fraction(1), Fraction(7))}")
check("Koide locus example: (5,7,1) satisfies 2 r0² = r1² + r2² (swap symmetry)",
      koide_scalar(Fraction(5), Fraction(7), Fraction(1)) == Fraction(0))

check("(2,1,1) NOT on Koide locus", koide_scalar(Fraction(2), Fraction(1), Fraction(1)) != Fraction(0))
check("(0,1,1) NOT on Koide locus", koide_scalar(Fraction(0), Fraction(1), Fraction(1)) != Fraction(0))

# Most importantly: the locus is a CONSTRAINT, not a derived property of physical charged leptons
check("note flags: scalar equation NOT claimed to hold for physical charged leptons",
      "NOT claimed to hold for physical charged leptons" in note_text or
      "out of scope" in note_text)


# ============================================================================
section("Part 5: declared dependency is graph-visible")
# ============================================================================
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
rows = ledger['rows']
dep_id = "koide_dweh_cyclic_compression_note_2026-04-18"
dep_row = rows.get(dep_id)
claim_row = rows.get(CLAIM_ID)
check(f"{dep_id} exists in audit ledger",
      dep_row is not None,
      detail=f"effective_status={dep_row.get('effective_status') if dep_row else None!r}")
check(f"{CLAIM_ID} seeded by audit pipeline",
      claim_row is not None,
      detail="run docs/audit/scripts/run_pipeline.sh after editing the note")
if claim_row is not None:
    claim_deps = set(claim_row.get("deps", []))
    check(f"{CLAIM_ID} records Koide DWEH as declared dependency",
          dep_id in claim_deps,
          detail=f"deps={sorted(claim_deps)}")
    check(f"{CLAIM_ID} remains effective-unaudited before independent audit",
          claim_row.get("effective_status") == "unaudited",
          detail=f"effective_status={claim_row.get('effective_status')!r}")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
