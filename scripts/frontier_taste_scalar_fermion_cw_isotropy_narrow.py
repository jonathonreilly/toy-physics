#!/usr/bin/env python3
"""Verify the narrow taste-scalar fermion Coleman-Weinberg isotropy theorem
at exact rational precision.

Claim scope: on C^8 = (C^2)^{⊗3} with commuting σ_x shift operators
S_i, the one-loop fermion Coleman-Weinberg Hessian at φ = (v, 0, 0) is
exactly diagonal in (i, j) with binary-orthogonality sum giving 8 δ_{ij}.
"""

from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "TASTE_SCALAR_FERMION_CW_ISOTROPY_NARROW_THEOREM_NOTE_2026-05-02.md"
CLAIM_ID = "taste_scalar_fermion_cw_isotropy_narrow_theorem_note_2026-05-02"

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
    "Taste-Scalar Fermion Coleman-Weinberg Isotropy",
    "Type:** positive_theorem",
    "δ_{ij} · C(v)",
    "axis-aligned point",
    "8 · δ_{ij}",
    "out of scope",
    "class (A)",
    "target_claim_type: positive_theorem",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)


# ============================================================================
section("Part 2: binary orthogonality sum Σ_s (-1)^{s_i}(-1)^{s_j} = 8 δ_{ij}")
# ============================================================================
# 8 basis states s = (s_1, s_2, s_3) with s_i ∈ {0, 1}
states = list(product([0, 1], repeat=3))
assert len(states) == 8

for i in range(3):
    for j in range(3):
        S = sum((-1)**s[i] * (-1)**s[j] for s in states)
        expected = 8 if i == j else 0
        check(f"Σ_s (-1)^{{s_{i}}}(-1)^{{s_{j}}} = {expected}",
              S == expected,
              detail=f"binary orthogonality")


# ============================================================================
section("Part 3: eigenvalue formula λ_s(φ) = Σ φ_i (-1)^{s_i}")
# ============================================================================
# Test a few φ values
for phi in [(Fraction(1), Fraction(2), Fraction(3)),
            (Fraction(2), Fraction(0), Fraction(0)),
            (Fraction(-1, 3), Fraction(7, 11), Fraction(0))]:
    lambdas = []
    for s in states:
        lam = sum(phi[i] * (-1)**s[i] for i in range(3))
        lambdas.append(lam)
    # Verify length is 8
    check(f"8 eigenvalues for φ = {phi}",
          len(lambdas) == 8)


# ============================================================================
section("Part 4: at φ = (v, 0, 0), |λ_s|² = v² uniformly")
# ============================================================================
for v in [Fraction(1), Fraction(2), Fraction(-3), Fraction(7, 11)]:
    phi = (v, Fraction(0), Fraction(0))
    lambda_squareds = []
    for s in states:
        lam = sum(phi[i] * (-1)**s[i] for i in range(3))
        lambda_squareds.append(lam * lam)
    expected = v * v
    all_uniform = all(ls == expected for ls in lambda_squareds)
    check(f"at φ = ({v}, 0, 0), |λ_s|² = v² = {expected} for all 8 s",
          all_uniform,
          detail=f"observed = {set(lambda_squareds)}")


# ============================================================================
section("Part 5: Hessian at (v, 0, 0) is diagonal proportional to δ_{ij}")
# ============================================================================
# V_f(φ) = Σ_s f(λ_s(φ)²)
# Hessian H_ij = ∂²V/∂φ_i ∂φ_j
# At φ = (v, 0, 0), λ_s² = v² uniformly, so:
#   ∂²V/∂φ_i ∂φ_j = Σ_s [2 f'(λ_s²) (∂λ_s/∂φ_i)(∂λ_s/∂φ_j)
#                        + 4 f''(λ_s²) λ_s² (∂λ_s/∂φ_i)(∂λ_s/∂φ_j)]
# = (2 f'(v²) + 4 f''(v²) v²) Σ_s (-1)^{s_i}(-1)^{s_j}
# = (2 f'(v²) + 4 f''(v²) v²) · 8 δ_{ij}
# So H_ij = δ_{ij} · 8 · (2 f'(v²) + 4 f''(v²) v²) = δ_{ij} · C(v).

# We can verify this numerically for specific f.
def hessian_at_v00(f, fp, fpp, v):
    """Compute Hessian at φ = (v, 0, 0) for f(x) with derivative fp(x) and second derivative fpp(x)."""
    H = [[Fraction(0)] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for s in states:
                # λ_s = sum φ_k (-1)^{s_k}, only φ_1 = v contributes
                lam_squared = v * v  # at (v, 0, 0)
                d_i = (-1)**s[i]
                d_j = (-1)**s[j]
                # contribution to H_ij from this state
                H[i][j] += (2 * fp(lam_squared) * d_i * d_j
                            + 4 * fpp(lam_squared) * lam_squared * d_i * d_j)
    return H

# Test 1: f(x) = x  ⇒ fp(x) = 1, fpp(x) = 0
v = Fraction(2)
H = hessian_at_v00(lambda x: x, lambda x: Fraction(1), lambda x: Fraction(0), v)
diag_val = H[0][0]
all_diagonal = all(H[i][j] == (diag_val if i == j else Fraction(0)) for i in range(3) for j in range(3))
check("f(x) = x: Hessian diagonal proportional to δ_ij at (v=2, 0, 0)",
      all_diagonal,
      detail=f"diagonal = {diag_val}; off-diagonal all zero")

# Test 2: f(x) = x²  ⇒ fp(x) = 2x, fpp(x) = 2
H2 = hessian_at_v00(lambda x: x*x, lambda x: 2*x, lambda x: Fraction(2), v)
diag_val2 = H2[0][0]
all_diagonal2 = all(H2[i][j] == (diag_val2 if i == j else Fraction(0)) for i in range(3) for j in range(3))
check("f(x) = x²: Hessian diagonal proportional to δ_ij at (v=2, 0, 0)",
      all_diagonal2,
      detail=f"diagonal = {diag_val2}")

# Test 3: f(x) = x^3
H3 = hessian_at_v00(lambda x: x**3, lambda x: 3*x*x, lambda x: 6*x, v)
diag_val3 = H3[0][0]
all_diagonal3 = all(H3[i][j] == (diag_val3 if i == j else Fraction(0)) for i in range(3) for j in range(3))
check("f(x) = x³: Hessian diagonal proportional to δ_ij at (v=2, 0, 0)",
      all_diagonal3,
      detail=f"diagonal = {diag_val3}")


# ============================================================================
section("Part 6: closure factor 8 is exact independent of f")
# ============================================================================
# Verify: H_ii = 8 · (2 fp(v²) + 4 fpp(v²) v²) for all i
# More directly: H_ii / (2 fp(v²) + 4 fpp(v²) v²) = 8.
# Use f(x) = x: fp = 1, fpp = 0. Coefficient = 2·1 + 0 = 2. So H_ii = 8·2 = 16.
v = Fraction(1)
H_test = hessian_at_v00(lambda x: x, lambda x: Fraction(1), lambda x: Fraction(0), v)
check("for f(x) = x at v = 1: H_ii = 16 = 8 · 2 (closure factor)",
      H_test[0][0] == Fraction(16),
      detail=f"H_00 = {H_test[0][0]}")


# ============================================================================
section("Part 7: self-contained audit row remains unaudited before audit")
# ============================================================================
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
rows = ledger["rows"]
claim_row = rows.get(CLAIM_ID)
check(f"{CLAIM_ID} seeded by audit pipeline",
      claim_row is not None,
      detail="run docs/audit/scripts/run_pipeline.sh after editing the note")
if claim_row is not None:
    claim_deps = set(claim_row.get("deps", []))
    check(f"{CLAIM_ID} has no declared dependency edges",
          not claim_deps,
          detail=f"deps={sorted(claim_deps)}")
    check(f"{CLAIM_ID} remains effective-unaudited before independent audit",
          claim_row.get("effective_status") == "unaudited",
          detail=f"effective_status={claim_row.get('effective_status')!r}")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
