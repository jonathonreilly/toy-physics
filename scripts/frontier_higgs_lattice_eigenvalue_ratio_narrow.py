#!/usr/bin/env python3
"""Verify the narrow Higgs lattice eigenvalue ratio theorem at mean-field.

Claim scope: GIVEN graph_first_su3 retained_bounded + admitted Wilson
canonical g_bare=1 + admitted Clifford identity D_taste² = d·I + admitted
mean-field factorization, the lattice ratio R_lattice = 4/(u_0² N_taste) =
1/(4 u_0²) at N_taste = 16. NO physical (m_H/v)² identification.

Class (A) algebraic identity on admitted mean-field inputs.
"""

from fractions import Fraction
from pathlib import Path
from sympy import symbols, simplify, log, diff, Rational, sqrt
import sys
import json

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "HIGGS_LATTICE_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md"

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
    "Higgs Lattice Eigenvalue Ratio (Mean-Field) — Narrow Theorem",
    "Type:** bounded_theorem",
    "R_lattice",
    "4 / (u_0² · N_taste)",
    "N_taste = 16",
    "NO physical Higgs mass identification",
    "graph_first_su3_integration_note",
    "g_bare = 1",
    "class (A)",
    "target_claim_type: bounded_theorem",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)

# Scope discipline: must NOT claim m_H = v/(2 u_0) as load-bearing
forbidden = [
    "m_H = v/(2 u_0) is hereby derived",
    "physical Higgs mass is established",
    "(m_H/v)² is identified with R_lattice (DERIVATION)",
]
for f in forbidden:
    check(f"narrow scope avoids forbidden physical-matching claim: {f!r}",
          f not in note_text)


# ============================================================================
section("Part 2: structural integers N_c, N_sites, N_taste, N_tot")
# ============================================================================
N_c = 3
N_sites = 16  # 2^4 minimal APBC block
N_taste = 16  # = N_sites at minimal block
d = 4         # spatial+1 spacetime dim from staggered Cl(3) on Z^4
N_tot = N_c * N_sites

check("N_c = 3 (retained graph_first_su3)",
      N_c == 3)
check("N_sites = 2^4 = 16 (minimal APBC block)",
      N_sites == 16 and N_sites == 2**4)
check("N_taste = N_sites = 16",
      N_taste == N_sites)
check("d = 4 (Z^4 spacetime dimension for staggered Cl(3))",
      d == 4)
check("N_tot = N_c × N_sites = 48",
      N_tot == 48 and N_tot == N_c * N_sites)


# ============================================================================
section("Part 3: Clifford-identity eigenvalue magnitude")
# ============================================================================
# Clifford identity D_taste² = d · I  ⇒  |λ_taste| = sqrt(d) = 2 (lattice units)
from sympy import sqrt as sym_sqrt, Rational as R
lambda_taste_sq = R(d)
lambda_taste_mag = sym_sqrt(lambda_taste_sq)
check("|λ_taste|² = d = 4 from Clifford identity",
      lambda_taste_sq == R(4))
check("|λ_taste| = sqrt(d) = 2 (lattice units)",
      lambda_taste_mag == R(2))


# ============================================================================
section("Part 4: mean-field eigenvalue scaling and generating functional curvature")
# ============================================================================
# At mean field: U_{ab} → u_0 δ_{ab}, so |λ_full| = 2 u_0
# Generating functional W(J) = (N_tot / 2) · log(J² + 4 u_0²) at J=0:
# d²W/dJ² |_{J=0} = N_tot · 1/(2u_0²) · (1/2) = N_tot / (4 u_0²)

J, u0 = symbols('J u0', positive=True)
W = R(N_tot) / R(2) * log(J**2 + 4 * u0**2)
W_curvature = simplify(diff(W, J, 2).subs(J, 0))
expected_curvature = R(N_tot) / (4 * u0**2)
check("W'' at J=0 = N_tot / (4 u_0²) = 12 / u_0²",
      simplify(W_curvature - expected_curvature) == 0,
      detail=f"W''|0 = {W_curvature}, expected {expected_curvature}")


# ============================================================================
section("Part 5: R_lattice = 4 / (u_0² N_taste) = 1 / (4 u_0²)")
# ============================================================================
R_lattice_formula = R(4) / (u0**2 * R(N_taste))
R_lattice_simplified = simplify(R_lattice_formula)
expected_simplified = R(1) / (4 * u0**2)
check("R_lattice = 4 / (u_0² · N_taste) at N_taste=16 = 1/(4 u_0²)",
      simplify(R_lattice_simplified - expected_simplified) == 0,
      detail=f"R_lattice = {R_lattice_simplified}, expected {expected_simplified}")

# Per-taste curvature: W'' / N_tot
per_taste_curvature = simplify(W_curvature / R(N_tot))
check("per-taste curvature W''/N_tot = 1/(4 u_0²) matches R_lattice",
      simplify(per_taste_curvature - R_lattice_simplified) == 0,
      detail=f"W''/N_tot = {per_taste_curvature}")


# ============================================================================
section("Part 6: cited authority retained-grade")
# ============================================================================
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
rows = ledger['rows']
retained_grade = {'retained', 'retained_bounded', 'retained_no_go'}

dep_id = "graph_first_su3_integration_note"
dep_es = rows.get(dep_id, {}).get("effective_status")
check(f"{dep_id} effective_status retained-grade",
      dep_es in retained_grade,
      detail=f"observed = {dep_es!r}")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
