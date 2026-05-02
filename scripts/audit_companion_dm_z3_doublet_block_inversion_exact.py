#!/usr/bin/env python3
"""Pattern B audit-companion runner for
`dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16`
(claim_type=positive_theorem, audit_status=audited_conditional, td=126,
load_bearing_step_class=A).

The parent's load-bearing step is the linear-algebraic inversion of the
Z_3-doublet-block parametrization. Given the explicit affine
parametrization

    K11(q_+) = -q_+ + 2 sqrt(2) / 9 - 1 / (2 sqrt(3)),
    K22(q_+) = -q_+ + 2 sqrt(2) / 9 + 1 / (2 sqrt(3)),
    K12(m, delta) = m - 4 sqrt(2) / 9 + i (sqrt(3) delta - 4 sqrt(2) / 3),

the inversion formulas

    q_+   = 2 sqrt(2) / 9 - (K11 + K22) / 2,
    delta = (Im K12 + 4 sqrt(2) / 3) / sqrt(3),
    m     = Re K12 + 4 sqrt(2) / 9,

invert the parametrization correctly. The doublet-block contains the
moving microscopic datum.

This Pattern B companion verifies the inversion identities at sympy
exact symbolic precision, plus several derived identities:
  - K22 - K11 = 1 / sqrt(3) (independent of q_+, m, delta);
  - (K11 + K22) / 2 = -q_+ + 2 sqrt(2) / 9 (independent of m, delta);
  - inversion residuals identically zero.

Companion role: not a new claim row; not a new source note. Provides
audit-friendly evidence that the parent's class-(A) algebraic
inversion holds at exact symbolic precision.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, sqrt, simplify, symbols, im, re, I as sym_I
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


# Constants
c1 = 2 * sqrt(Rational(2)) / 9   # = 2 sqrt(2)/9 (appears in K11, K22 and inversion of q_+)
c2 = Rational(1) / (2 * sqrt(Rational(3)))  # = 1/(2 sqrt(3)) (split between K11, K22)
c3 = 4 * sqrt(Rational(2)) / 9   # = 4 sqrt(2)/9 (appears in K12)
c4 = 4 * sqrt(Rational(2)) / 3   # = 4 sqrt(2)/3 (appears in Im K12 inversion)


# ============================================================================
section("Audit companion for dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem (td=126)")
# ============================================================================

# ----------------------------------------------------------------------------
section("Part 1: parametric K11, K22, K12 in (m, delta, q_+)")
# ----------------------------------------------------------------------------
m_sym, delta_sym, q_sym = symbols('m delta q_+', real=True)

K11 = -q_sym + c1 - c2
K22 = -q_sym + c1 + c2
K12 = m_sym - c3 + sym_I * (sqrt(Rational(3)) * delta_sym - c4)

print(f"\n  K11(q_+) = {K11}")
print(f"  K22(q_+) = {K22}")
print(f"  K12(m, delta) = {K12}")


# ----------------------------------------------------------------------------
section("Part 2: K22 - K11 = 1/sqrt(3) (independent of q_+, m, delta)")
# ----------------------------------------------------------------------------
diff_22_11 = simplify(K22 - K11)
expected_diff = Rational(1) / sqrt(Rational(3))
check("K22 - K11 = 1/sqrt(3) exact",
      simplify(diff_22_11 - expected_diff) == 0,
      detail=f"K22 - K11 = {diff_22_11}")


# ----------------------------------------------------------------------------
section("Part 3: average (K11 + K22)/2 = -q_+ + 2 sqrt(2)/9")
# ----------------------------------------------------------------------------
avg_diag = simplify((K11 + K22) / 2)
expected_avg = -q_sym + c1
check("(K11 + K22)/2 = -q_+ + 2 sqrt(2)/9 exact",
      simplify(avg_diag - expected_avg) == 0,
      detail=f"avg = {avg_diag}")


# ----------------------------------------------------------------------------
section("Part 4: inversion formula q_+ = 2 sqrt(2)/9 - (K11 + K22)/2")
# ----------------------------------------------------------------------------
q_recovered = simplify(c1 - (K11 + K22) / 2)
check("inversion: q_+ = 2 sqrt(2)/9 - (K11 + K22)/2 recovers q_+ exactly",
      simplify(q_recovered - q_sym) == 0,
      detail=f"q_recovered = {q_recovered}")


# ----------------------------------------------------------------------------
section("Part 5: inversion formula delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3)")
# ----------------------------------------------------------------------------
Im_K12 = simplify(im(K12))
delta_recovered = simplify((Im_K12 + c4) / sqrt(Rational(3)))
check("Im(K12) = sqrt(3) delta - 4 sqrt(2)/3 (parametric form)",
      simplify(Im_K12 - (sqrt(Rational(3)) * delta_sym - c4)) == 0,
      detail=f"Im(K12) = {Im_K12}")
check("inversion: delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3) recovers delta exactly",
      simplify(delta_recovered - delta_sym) == 0,
      detail=f"delta_recovered = {delta_recovered}")


# ----------------------------------------------------------------------------
section("Part 6: inversion formula m = Re K12 + 4 sqrt(2)/9")
# ----------------------------------------------------------------------------
Re_K12 = simplify(re(K12))
m_recovered = simplify(Re_K12 + c3)
check("Re(K12) = m - 4 sqrt(2)/9 (parametric form)",
      simplify(Re_K12 - (m_sym - c3)) == 0,
      detail=f"Re(K12) = {Re_K12}")
check("inversion: m = Re K12 + 4 sqrt(2)/9 recovers m exactly",
      simplify(m_recovered - m_sym) == 0,
      detail=f"m_recovered = {m_recovered}")


# ----------------------------------------------------------------------------
section("Part 7: trace identity m = K11 + K22 + Re K12 ... no, m = Tr only if K is right")
# ----------------------------------------------------------------------------
# Source note also claims m = Tr(K_Z3). To verify this we'd need the singlet
# entry K00 of K_Z3, which the parent says equals a constant a_* (NOT
# parametrically dependent). For this Pattern B narrow check, we restrict to
# K11, K22, K12 — the three doublet-block entries — without claiming the
# K00 = a_* equality (that's a separate result of the intrinsic-slot theorem).
print("\n  (Note: source-note claim m = Tr(K_Z3) requires the intrinsic-slot")
print("   theorem's K00 = a_* result; out of scope of this Pattern B companion.)")


# ----------------------------------------------------------------------------
section("Part 8: concrete numerical instance (m, delta, q_+) = (1, 0, 0)")
# ----------------------------------------------------------------------------
sub_concrete = {m_sym: Rational(1), delta_sym: Rational(0), q_sym: Rational(0)}

K11_c = simplify(K11.subs(sub_concrete))
K22_c = simplify(K22.subs(sub_concrete))
K12_c = simplify(K12.subs(sub_concrete))

# At q_+ = 0: K11 = c1 - c2, K22 = c1 + c2 = 2 sqrt(2)/9 +/- 1/(2 sqrt(3)).
expected_K11 = c1 - c2
expected_K22 = c1 + c2
check("at q_+ = 0: K11 = 2 sqrt(2)/9 - 1/(2 sqrt(3))",
      simplify(K11_c - expected_K11) == 0,
      detail=f"K11 = {K11_c}")
check("at q_+ = 0: K22 = 2 sqrt(2)/9 + 1/(2 sqrt(3))",
      simplify(K22_c - expected_K22) == 0,
      detail=f"K22 = {K22_c}")
check("at (m, delta, q_+) = (1, 0, 0): K12 = 1 - 4 sqrt(2)/9 - i 4 sqrt(2)/3",
      simplify(K12_c - (Rational(1) - c3 - sym_I * c4)) == 0,
      detail=f"K12 = {K12_c}")

# Inversion at concrete values: should recover (1, 0, 0).
q_back = simplify(c1 - (K11_c + K22_c) / 2)
delta_back = simplify((im(K12_c) + c4) / sqrt(Rational(3)))
m_back = simplify(re(K12_c) + c3)
check("inversion at concrete values recovers (m, delta, q_+) = (1, 0, 0)",
      m_back == Rational(1) and delta_back == Rational(0) and q_back == Rational(0),
      detail=f"recovered (m, delta, q_+) = ({m_back}, {delta_back}, {q_back})")


# ----------------------------------------------------------------------------
section("Part 9: parent row dep verification")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16', {})
print(f"\n  dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16 current ledger state:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check("parent row class-A load-bearing step (algebraic inversion)",
      parent.get('load_bearing_step_class') == 'A',
      detail=f"class = {parent.get('load_bearing_step_class')}")


# ----------------------------------------------------------------------------
section("Audit-companion summary")
# ----------------------------------------------------------------------------
print("""
  This companion provides EXACT symbolic verification (via sympy) of the
  parent theorem's load-bearing class-(A) algebraic inversion of the
  Z_3-doublet-block parametrization:

    K11 - K22 difference: 1/sqrt(3) exact (independent of q_+, m, delta);
    diagonal average: (K11 + K22)/2 = -q_+ + 2 sqrt(2)/9 (independent
                       of m, delta);
    inversion of q_+ from diagonal average: exact;
    Im(K12) parametric form and inversion of delta: exact;
    Re(K12) parametric form and inversion of m: exact;
    concrete-value round-trip (m, delta, q_+) = (1, 0, 0): exact recovery.

  Audit-lane class for the parent's load-bearing step:
    (A) — algebraic inversion of an explicit linear-affine parametrization
    of K11, K22, K12 in (m, delta, q_+). No external observed/fitted/
    literature input.

  Out of scope: the singlet-doublet slot equalities K01 = a_*, K02 = b_*
  (intrinsic-slot theorem, separate authority); the m = Tr(K_Z3)
  identification (requires K00 = a_* from intrinsic-slot theorem); the
  upstream post-canonical positive-polar section / singlet-doublet CP
  slot tool / active-affine point-selection boundary authorities.

  This audit-companion does NOT introduce a new claim row, a new source
  note, or any modification of the parent's audit_status.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
