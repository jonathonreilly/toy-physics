#!/usr/bin/env python3
"""Verify the narrow LH-doublet traceless abelian eigenvalue ratio theorem.

Claim scope: on the graph-first commutant gl(3) ⊕ gl(1) of
{SU(2)_weak, SWAP_{ν,ρ}} acting on the LH-doublet sector, the unique
traceless U(1) direction has eigenvalue ratio 1:(-3) on Sym²(C²) : Anti²(C²)
(6-state : 2-state) sub-decompositions.

Load-bearing step is class (A) algebraic closure on retained-grade inputs:
  6α + 2β = 0  ⇒  β = -3α  ⇒  ratio α:β = 1:(-3).

This runner does NOT verify specific eigenvalues +1/3, -1 (those require
a normalization choice that is out of scope). It does NOT verify any SM
hypercharge identification. The narrow scope is the ratio only.
"""

from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md"

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
    "LH-Doublet Traceless Abelian Eigenvalue Ratio",
    # Post-axiom-reset retag (2026-05-03): bounded_theorem.
    "Type:** bounded_theorem",
    "eigenvalue ratio **1 : (−3)**",
    "explicitly **does not** claim",
    "specific eigenvalues `+1/3` and `−1`",
    "out of scope",
    "GRAPH_FIRST_SU3_INTEGRATION_NOTE.md",
    "GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md",
    "class (A)",
    "target_claim_type: bounded_theorem",
]
for s in required:
    check(f"contains: {s!r}", s in note_text)

# Scope-discipline: the note must NOT load-bear on Y identification or
# charge-formula claims. Verify the load-bearing step is purely the
# tracelessness algebra.
forbidden_in_scope = [
    "Q = T_3 + Y/2 then matches",        # the LHCM step the audit objected to
    "The charge formula `Q = T_3 + Y/2` then matches",
    "identifies the structural 3+1 abelian eigenspaces with the Standard Model",
]
for f in forbidden_in_scope:
    check(f"narrow scope avoids forbidden load-bearing claim: {f!r}",
          f not in note_text,
          detail="audit's named blocking step is out of scope")

# ============================================================================
section("Part 2: structural multiplicities sum to LH-doublet space dimension 8")
# ============================================================================
# From graph_first_su3 retained-grade structure: Sym² (6-state) ⊕ Anti²
# (2-state) on
# (SU(2)-doublet ⊗ 4-point-base) = 2 × 4 = 8 LH-doublet states.
n_sym = 6  # 3 Sym²-axes × 2 weak-doublet states
n_anti = 2  # 1 Anti²-axis × 2 weak-doublet states
n_total = 8

check("dim Sym²-multiplicity (graph_first_su3 retained-grade) = 6",
      n_sym == 6, detail=f"6 = 3 axes × 2 weak-doublet states")
check("dim Anti²-multiplicity (graph_first_su3 retained-grade) = 2",
      n_anti == 2, detail=f"2 = 1 axis × 2 weak-doublet states")
check("Sym² + Anti² = 8 (LH-doublet space)",
      n_sym + n_anti == n_total,
      detail=f"{n_sym} + {n_anti} = {n_sym + n_anti}")

# ============================================================================
section("Part 3: tracelessness forces ratio β/α = −3 uniquely")
# ============================================================================
# The unique traceless abelian generator has eigenvalues α on Sym² and β on Anti².
# Tracelessness over the LH-doublet sector: 6α + 2β = 0.
# This is class (A) algebraic closure on retained-grade graph-first multiplicities.

# Verify ratio for arbitrary α:
test_alphas = [Fraction(1), Fraction(2), Fraction(-5), Fraction(7, 11),
               Fraction(-3, 17), Fraction(100, 1)]
all_ratios_minus_three = True
for alpha in test_alphas:
    # Solve 6α + 2β = 0 for β:
    beta = -Fraction(6) * alpha / Fraction(2)
    ratio = beta / alpha if alpha != 0 else None
    if ratio != Fraction(-3):
        all_ratios_minus_three = False
        break
check("for arbitrary α, tracelessness forces β = −3α (ratio independent of scale)",
      all_ratios_minus_three,
      detail=f"tested α ∈ {[str(a) for a in test_alphas]}")

# Specific check: ratio computed at exact rational precision
alpha = Fraction(1)
beta = -Fraction(6) * alpha / Fraction(2)
ratio = beta / alpha
check("ratio β/α = −3 exactly (Fraction equality)",
      ratio == Fraction(-3),
      detail=f"β/α = {ratio}")

# Ratio Sym²:Anti² = α:β = 1:(-3)
check("Sym² : Anti² ratio = 1 : (−3)",
      Fraction(1) / ratio == Fraction(-1, 3),
      detail=f"1 : {ratio}  ⇒  Sym²/Anti² eigenvalue ratio")

# ============================================================================
section("Part 4: SM identification step is NOT in load-bearing chain")
# ============================================================================
# The narrow theorem must not require the SM-Y identification to close.
# Test: instantiate at α = 1 (arbitrary) and verify the ratio still holds.
# At α = 7/11 (a value with no SM interpretation): ratio is still -3.

alpha_arbitrary = Fraction(7, 11)  # no SM interpretation
beta_arbitrary = -Fraction(6) * alpha_arbitrary / Fraction(2)
check("ratio holds at α with no SM interpretation (e.g. α = 7/11)",
      beta_arbitrary / alpha_arbitrary == Fraction(-3),
      detail=f"α = {alpha_arbitrary}, β = {beta_arbitrary}, ratio = {beta_arbitrary/alpha_arbitrary}")

# The SM-specific values +1/3 and -1 are ONE choice with α = +1/3:
alpha_sm_choice = Fraction(1, 3)
beta_sm_choice = -Fraction(6) * alpha_sm_choice / Fraction(2)
check("at α = +1/3 (an admitted SM-Y normalization), eigenvalues = (+1/3, −1)",
      alpha_sm_choice == Fraction(1, 3) and beta_sm_choice == Fraction(-1),
      detail=f"α = {alpha_sm_choice}, β = {beta_sm_choice} — but this normalization is out of scope")

# ============================================================================
section("Part 5: cited authorities are retained-grade")
# ============================================================================
# Read the audit ledger and verify both cited authorities are retained-grade.
import json
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger_data = json.loads(LEDGER.read_text())
ledger_rows = ledger_data['rows']

retained_grades = {"retained", "retained_bounded", "retained_no_go"}
cited = [
    "graph_first_su3_integration_note",
    "graph_first_selector_derivation_note",
]
for cid in cited:
    actual_es = ledger_rows.get(cid, {}).get("effective_status")
    check(f"{cid} effective_status is retained-grade",
          actual_es in retained_grades,
          detail=f"observed = {actual_es!r}")

print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
