#!/usr/bin/env python3
"""Verify the narrow g_bare canonical Wilson convention theorem.

Claim scope: GIVEN g_bare = 1 as admitted Wilson canonical-normalization
convention + retained graph_first_su3 N_c = 3, the Wilson action coefficient
β = 6 (class A algebraic substitution) and the lattice field strength
equals Cl(3) curvature without rescaling.
"""

from fractions import Fraction
from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md"

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
section("Part 1: note structure and convention discipline")
# ============================================================================
note_text = NOTE_PATH.read_text()
required = [
    "g_bare Canonical Wilson Normalization (Convention)",
    "Type:** bounded_theorem",
    "g_bare = 1",
    "an admitted convention",
    "NOT a derivation",
    "β  =  2 N_c / g_bare²  =  2 · 3 / 1  =  6",
    "graph_first_su3_integration_note",
    "class (A)",
    "convention-vs-derivation",
    "target_claim_type: bounded_theorem",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)

# Critical: the note must explicitly NOT claim derivation
forbidden = [
    "g_bare = 1 is uniquely derived",
    "g_bare = 1 is forced by",
    "Cl(3) axioms uniquely determine g_bare",
]
for f in forbidden:
    check(f"narrow scope avoids forbidden derivation claim: {f!r}",
          f not in note_text)


# ============================================================================
section("Part 2: β = 2 N_c / g_bare² for (N_c=3, g_bare=1) gives β = 6")
# ============================================================================
def beta_wilson(N_c, g_bare):
    return Fraction(2) * Fraction(N_c) / (Fraction(g_bare) ** 2)

beta_3_1 = beta_wilson(3, 1)
check("β(N_c=3, g_bare=1) = 6 exactly",
      beta_3_1 == Fraction(6),
      detail=f"β = 2·3/1² = {beta_3_1}")


# ============================================================================
section("Part 3: β formula consistency for various (N_c, g_bare)")
# ============================================================================
test_cases = [
    (2, 1, Fraction(4)),    # SU(2), unit coupling: β = 4
    (3, 1, Fraction(6)),    # SU(3), unit coupling: β = 6
    (4, 1, Fraction(8)),    # SU(4), unit coupling: β = 8
    (3, 2, Fraction(3, 2)), # SU(3), g_bare=2: β = 6/4 = 3/2
    (3, Fraction(1, 2), Fraction(24)),  # g_bare = 1/2: β = 6/(1/4) = 24
]
for N_c, g_bare, expected in test_cases:
    beta = beta_wilson(N_c, g_bare)
    check(f"β(N_c={N_c}, g_bare={g_bare}) = {expected}",
          beta == expected,
          detail=f"β = {beta}")


# ============================================================================
section("Part 4: at g_bare = 1, F^lattice = Ω^Cl(3) without rescaling")
# ============================================================================
# F^lattice = (1/g_bare) Ω + O(a²)
# At g_bare = 1, the rescaling factor 1/g_bare = 1.
g_bare = Fraction(1)
rescaling = Fraction(1) / g_bare
check("rescaling factor at g_bare = 1 is 1 (no rescaling)",
      rescaling == Fraction(1),
      detail=f"1/g_bare = {rescaling}")

# At g_bare ≠ 1, rescaling is nontrivial:
for g in [Fraction(2), Fraction(1, 3), Fraction(7, 11)]:
    r = Fraction(1) / g
    check(f"at g_bare = {g}, rescaling factor = {r} ≠ 1 (convention dependent)",
          r != Fraction(1),
          detail=f"shows g_bare = 1 is the rescaling-free point")


# ============================================================================
section("Part 5: cited authority is retained-grade")
# ============================================================================
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
rows = ledger['rows']

dep_id = "graph_first_su3_integration_note"
dep_es = rows.get(dep_id, {}).get("effective_status")
retained_grade = {'retained', 'retained_bounded', 'retained_no_go'}
check(f"{dep_id} effective_status retained-grade",
      dep_es in retained_grade,
      detail=f"observed = {dep_es!r}")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
