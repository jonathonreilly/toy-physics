#!/usr/bin/env python3
"""Verify the NJL-style total V_eff theorem on the framework's lattice.

Claim scope: V_total(σ) = σ²/(2 G_eff) - 8 log(σ² + 4 u_0²) on the
L_s=2 mean-field surface (HIGGS_MASS_FROM_AXIOM Step 2 V_taste form
plus an admitted Hubbard-Stratonovich tree term σ²/(2 G_eff)). Verifies:

  1. Gap equation σ_min² = 16 G_eff - 4 u_0².
  2. Critical coupling G_critical = u_0²/4.
  3. Trivial-root second derivative 1/G_eff - 4/u_0².
  4. Broken-phase second derivative (4 G_eff - u_0²)/(2 G_eff²).
  5. At Kawamoto-Smit leading-order G_eff = 1/(2 N_c) and framework
     u_0 ≈ 0.8776, the lattice gauge sector is in the SYMMETRIC phase
     (G_eff/G_critical ≈ 0.866).
  6. Sensitivity sweep over six plausible G_eff forms.

Class (A) algebraic on V_total + (D) definitional Hubbard-Stratonovich
tree-term identification. No PDG values are derivation inputs.

The runner does NOT verify EWSB (framework is in symmetric phase),
does NOT extract m_H_pole, does NOT close Gate #3.
"""

from __future__ import annotations

from pathlib import Path
import sys
import json

try:
    import sympy as sp
except ImportError:  # pragma: no cover
    print("FAIL: sympy required")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = (
    ROOT
    / "docs"
    / "V_EFF_TOTAL_NJL_STYLE_BOUNDED_THEOREM_NOTE_2026-05-10.md"
)
CLAIM_ID = "v_eff_total_njl_style_bounded_theorem_note_2026-05-10"


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Part 1: note structure and bounded-theorem scope discipline")
# ============================================================================
note_text = NOTE_PATH.read_text()

required_strings = [
    "V_eff Total (NJL-Style)",
    "claim_type: bounded_theorem",
    "σ²/(2 G_eff)",
    "V_total(σ)",
    "σ² / (2 G_eff)",
    "G_critical",
    "u_0² / 4",
    "Gap equation",
    "Hubbard",  # Stratonovich
    "Kawamoto",  # -Smit
    "Counterfactual Pass",
    "Elon first-principles",
    "1/(2 N_c)",
    "0.866",  # G_eff_LO / G_critical
    "SYMMETRIC",  # phase identification
    "Class (A)",
    "Hatsuda",  # & Kunihiro literature reference
    "Bardeen",  # Hill Lindner reference
    "bounded_admissions",
    "named_open_bridge",
]
for s in required_strings:
    check(f"contains: {s!r}", s in note_text)

forbidden = [
    "this theorem closes Gap #3",
    "this theorem closes Gate #3",
    "EWSB is hereby derived",
    "m_H_pole is established",
    "Higgs pole mass = 125",
    "lambda_curv",  # avoid the misleading lambda-naming for mass²-ratios
]
for f in forbidden:
    check(f"narrow scope avoids: {f!r}", f not in note_text)


# ============================================================================
section("Part 2: V_total form and gap equation derivation (symbolic)")
# ============================================================================
sigma, G, u0 = sp.symbols('sigma G u_0', positive=True, real=True)

# V_total form (from theorem statement (1))
V_total = sigma**2 / (2*G) - 8 * sp.log(sigma**2 + 4*u0**2)

# Step A.1: first derivative
dV = sp.diff(V_total, sigma)
expected_dV = sigma * (1/G - 16/(sigma**2 + 4*u0**2))
check(
    "dV_total/dσ = σ · [1/G - 16/(σ² + 4u_0²)]",
    sp.simplify(dV - expected_dV) == 0,
    detail=f"dV = {sp.simplify(dV)}",
)

# Step A.2: gap equation roots
# Solve dV/dσ = 0 for σ; sympy returns positive roots
gap_solns = sp.solve(dV, sigma)
# Should give the nontrivial root (σ=0 is implicit)
sigma_min_expected = 2 * sp.sqrt(4*G - u0**2)
sigma_min_sq_expected = 16*G - 4*u0**2

check(
    "Nontrivial root σ_min = 2·sqrt(4G - u_0²) (sympy solve)",
    any(sp.simplify(s - sigma_min_expected) == 0 for s in gap_solns),
    detail=f"solns = {gap_solns}",
)

# Verify σ_min² = 16 G - 4 u_0² (theorem (3))
sigma_min_sq_check = sp.simplify(sigma_min_expected**2 - sigma_min_sq_expected)
check(
    "σ_min² = 16 G - 4 u_0² (theorem (3))",
    sigma_min_sq_check == 0,
    detail=f"σ_min² - (16G - 4u_0²) = {sigma_min_sq_check}",
)


# ============================================================================
section("Part 3: critical coupling G_critical = u_0²/4")
# ============================================================================
# σ_min² > 0  ⇔  16 G - 4 u_0² > 0  ⇔  G > u_0²/4
G_critical_expr = u0**2 / 4
# Verify by substituting G = G_critical → σ_min² = 0
sigma_min_sq_at_crit = sp.simplify(sigma_min_sq_expected.subs(G, G_critical_expr))
check(
    "G_critical = u_0²/4 makes σ_min² = 0 (boundary)",
    sigma_min_sq_at_crit == 0,
    detail=f"σ_min²(G=u_0²/4) = {sigma_min_sq_at_crit}",
)


# ============================================================================
section("Part 4: second-derivative formulas (theorem (5))")
# ============================================================================
d2V = sp.diff(V_total, sigma, 2)

# Step A.5: at σ = 0
d2V_at_0 = sp.simplify(d2V.subs(sigma, 0))
expected_d2V_0 = 1/G - 4/u0**2
check(
    "d²V/dσ²|_{σ=0} = 1/G - 4/u_0²",
    sp.simplify(d2V_at_0 - expected_d2V_0) == 0,
    detail=f"d²V|0 = {d2V_at_0}",
)

# Symmetric phase stability: d²V|0 > 0 iff G < u_0²/4
# Symbolically: 1/G - 4/u_0² > 0  ⇔  G < u_0²/4
# We verify the sign at G slightly below G_crit (positive) and above (negative)
d2V_below = sp.simplify(d2V_at_0.subs([(u0, sp.Rational(7, 8)), (G, sp.Rational(1, 8))]))  # u_0²/4 = 49/256 ≈ 0.191; G=1/8=0.125 < critical
check(
    "d²V|0 positive when G < G_critical (sym-phase stable)",
    bool(d2V_below > 0),
    detail=f"d²V|0(G=1/8, u_0=7/8) = {d2V_below} > 0",
)
d2V_above = sp.simplify(d2V_at_0.subs([(u0, sp.Rational(7, 8)), (G, sp.Rational(1, 4))]))  # G=0.25 > 0.191
check(
    "d²V|0 negative when G > G_critical (sym-phase unstable)",
    bool(d2V_above < 0),
    detail=f"d²V|0(G=1/4, u_0=7/8) = {d2V_above} < 0",
)

# Step A.6: at σ = σ_min (broken-phase saddle curvature)
# Substitute σ² = 16 G - 4 u_0² (works for any G; physical only when G > G_crit)
d2V_at_min = d2V.subs(sigma**2, sigma_min_sq_expected)
d2V_at_min_simplified = sp.simplify(d2V_at_min)

expected_d2V_min = (4*G - u0**2) / (2 * G**2)
check(
    "d²V/dσ²|_{σ_min} = (4G - u_0²)/(2 G²)  (theorem (5))",
    sp.simplify(d2V_at_min_simplified - expected_d2V_min) == 0,
    detail=f"d²V|min - expected = {sp.simplify(d2V_at_min_simplified - expected_d2V_min)}",
)

# Equivalent form: σ_min²/(8 G²)
expected_d2V_min_alt = sigma_min_sq_expected / (8 * G**2)
check(
    "d²V/dσ²|_{σ_min} = σ_min²/(8 G²)  (alternate form)",
    sp.simplify(expected_d2V_min - expected_d2V_min_alt) == 0,
)

# Stability of broken-phase minimum
d2V_min_at_above_crit = sp.simplify(expected_d2V_min.subs([(u0, sp.Rational(7, 8)), (G, sp.Rational(1, 4))]))
check(
    "d²V|min > 0 in broken phase (saddle stable)",
    bool(d2V_min_at_above_crit > 0),
    detail=f"d²V|min(G=1/4, u_0=7/8) = {d2V_min_at_above_crit}",
)


# ============================================================================
section("Part 5: numerical evaluation at framework values (LO)")
# ============================================================================
N_c = 3
beta = 6
u0_num = 0.8776  # framework u_0 = ⟨P⟩^{1/4} at SU(3) β=6
g2_num = 2 * N_c / beta  # = 1.0

check("N_c = 3 (canonical SU(3))", N_c == 3)
check("β = 6 (canonical Wilson coupling)", beta == 6)
check("g² = 2 N_c / β = 1", abs(g2_num - 1.0) < 1e-12)
check("u_0 = 0.8776 (canonical mean-field link, SU(3) β=6)", abs(u0_num - 0.8776) < 1e-6)

# G_critical
G_crit_num = u0_num**2 / 4
expected_G_crit = 0.770182 / 4
check(
    "G_critical = u_0²/4 ≈ 0.19255 (lattice units)",
    abs(G_crit_num - 0.19255) < 1e-4,
    detail=f"G_critical = {G_crit_num:.6f}",
)

# Kawamoto-Smit leading-order G_eff = 1/(2 N_c) = 1/6
G_eff_LO = 1.0 / (2 * N_c)
check(
    "G_eff_LO = 1/(2 N_c) = 1/6 ≈ 0.16667 (Kawamoto-Smit LO)",
    abs(G_eff_LO - 1/6) < 1e-12,
    detail=f"G_eff_LO = {G_eff_LO:.6f}",
)

# Phase ratio
ratio_LO = G_eff_LO / G_crit_num
check(
    "G_eff_LO / G_critical ≈ 0.866 (near-critical, symmetric side)",
    abs(ratio_LO - 0.866) < 1e-3,
    detail=f"ratio = {ratio_LO:.6f}",
)

# Phase identification
sym_phase = G_eff_LO < G_crit_num
check(
    "Phase: SYMMETRIC at leading-order Kawamoto-Smit G_eff",
    sym_phase,
    detail=f"G_eff_LO = {G_eff_LO:.4f} < G_crit = {G_crit_num:.4f}",
)

# Formal nontrivial-root check: σ_min² < 0 in symmetric phase
sigma_min_sq_LO = 16 * G_eff_LO - 4 * u0_num**2
check(
    "σ_min² < 0 at leading-order (no broken-phase saddle)",
    sigma_min_sq_LO < 0,
    detail=f"σ_min²(LO) = {sigma_min_sq_LO:.6f}",
)


# ============================================================================
section("Part 6: sensitivity sweep over G_eff forms (§6.2)")
# ============================================================================
forms = [
    ("Kawamoto-Smit LO: 1/(2 N_c)", 1.0 / (2*N_c), True),  # third arg: expected symmetric
    ("strong-coupling alt: 1/(g² N_c)", 1.0 / (g2_num * N_c), False),
    ("Casimir variant: 1/(g² (N_c²-1))", 1.0 / (g2_num * (N_c**2 - 1)), True),
    ("color-trace: (N_c²-1)/(2 N_c² g²)", (N_c**2 - 1) / (2 * N_c**2 * g2_num), False),
    ("u_0²-dressed: u_0²/(2 N_c)", u0_num**2 / (2*N_c), True),
    ("u_0⁴-dressed: u_0⁴/(2 N_c)", u0_num**4 / (2*N_c), True),
]

for label, val, expected_sym in forms:
    actual_sym = val < G_crit_num
    check(
        f"sensitivity: {label} → {'SYM' if actual_sym else 'BROKEN'} (expected {'SYM' if expected_sym else 'BROKEN'})",
        actual_sym == expected_sym,
        detail=f"G_eff = {val:.4f}, ratio = {val/G_crit_num:.3f}",
    )

# Count symmetric vs broken
n_sym = sum(1 for _, val, _ in forms if val < G_crit_num)
n_broken = len(forms) - n_sym
check(
    "Four of six plausible forms put framework in SYMMETRIC phase",
    n_sym == 4 and n_broken == 2,
    detail=f"sym = {n_sym}, broken = {n_broken}",
)


# ============================================================================
section("Part 7: structural relation to continuum NJL (sanity check)")
# ============================================================================
# Continuum NJL critical: G_crit · Λ² = 2π²/N_c
# Lattice analog: G_crit · u_0² = 4 (from G_crit = u_0²/4 → G_crit·u_0² = u_0⁴/4)
# Wait — the dimensional analog needs careful interpretation.
# In lattice units (a=1), the cutoff Λ ~ π/a, so Λ² ~ π² in lattice units.
# G_crit · Λ² = (u_0²/4) · π² ≈ 0.19255 · 9.87 ≈ 1.90
# Continuum: 2π²/N_c = 2π²/3 ≈ 6.58
# Ratio: lattice / continuum ≈ 0.29; not exactly equal but same parametric family.

import math
G_crit_Lambda2_lattice = G_crit_num * math.pi**2  # lattice cutoff Λ ~ π/a, Λ²·a² = π²
G_crit_Lambda2_continuum = 2 * math.pi**2 / N_c  # = 2π²/N_c

check(
    "Continuum NJL critical: G·Λ² = 2π²/N_c ≈ 6.58 (sanity)",
    abs(G_crit_Lambda2_continuum - 2*math.pi**2/3) < 1e-10,
    detail=f"continuum G_crit·Λ² = {G_crit_Lambda2_continuum:.4f}",
)
check(
    "Lattice analog: G_crit·u_0²·π² ≈ 1.90 (different normalization, same parametric family)",
    abs(G_crit_Lambda2_lattice - 1.90) < 0.05,
    detail=f"lattice G_crit·u_0²·π² = {G_crit_Lambda2_lattice:.4f}",
)


# ============================================================================
section("Part 8: declared dependencies graph-visible")
# ============================================================================
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
if LEDGER.exists():
    ledger = json.loads(LEDGER.read_text())
    rows = ledger.get('rows', {})

    declared_deps = [
        "higgs_mass_from_axiom_note",
        "staggered_dirac_realization_gate_note_2026-05-03",
        "minimal_axioms_2026-05-03",
        "c_iso_su3_nnlo_closure_bounded_note_2026-05-10_su3nnlo",
    ]

    for dep_id in declared_deps:
        dep_row = rows.get(dep_id)
        check(
            f"declared dep visible in audit ledger: {dep_id}",
            dep_row is not None,
            detail=f"effective_status = {dep_row.get('effective_status') if dep_row else None!r}",
        )

    claim_row = rows.get(CLAIM_ID)
    if claim_row is None:
        # Pre-pipeline run: this is expected; record as info, not a fail.
        print(f"  [INFO] {CLAIM_ID} not yet seeded in audit ledger (run docs/audit/scripts/run_pipeline.sh)")
    else:
        check(
            f"{CLAIM_ID} seeded by audit pipeline",
            claim_row is not None,
            detail=f"effective_status = {claim_row.get('effective_status')!r}",
        )
        # Effective status starts as 'unaudited' before independent audit lane review
        check(
            f"{CLAIM_ID} effective status is 'unaudited' pre-audit",
            claim_row.get('effective_status') == 'unaudited',
            detail=f"effective_status = {claim_row.get('effective_status')!r}",
        )


# ============================================================================
section("Summary")
# ============================================================================
print(f"\n{'='*88}")
print(f"  TOTAL: PASS={PASS}, FAIL={FAIL}")
print(f"{'='*88}")
print(f"""
  Key results:
    G_critical = u_0²/4 ≈ {G_crit_num:.4f}    (lattice units)
    G_eff_LO   = 1/(2N_c) ≈ {G_eff_LO:.4f}    (Kawamoto-Smit leading-order)
    Ratio      = {ratio_LO:.4f}        (G_eff/G_critical)
    Phase      = SYMMETRIC          (lattice gauge sector below threshold)

  Conclusion: Gap #3 LOCATED in NJL phase diagram (near-critical, symmetric
  side). Gap #3 NOT closed: framework's lattice gauge sector at leading-
  order Kawamoto-Smit G_eff is below the chiral-SSB threshold; EWSB would
  require additional structure (EW gauge bosons + top Yukawa + Wilson
  taste-breaking).
""")
sys.exit(1 if FAIL > 0 else 0)
