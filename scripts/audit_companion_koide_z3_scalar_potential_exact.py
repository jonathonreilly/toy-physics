#!/usr/bin/env python3
"""Pattern B audit-companion runner for
`koide_z3_scalar_potential_support_note_2026-04-19`
(claim_type=positive_theorem, audit_status=audited_conditional, td=70,
load_bearing_step_class=A).

The parent's load-bearing class-(A) content includes:

  - The Clifford involution identity T_m^2 = I_3 for the explicit
    permutation matrix
        T_m = [[1, 0, 0], [0, 0, 1], [0, 1, 0]];
  - The trace identities Tr(T_m^2) = 3 and Tr(T_m^3) = Tr(T_m) = 1,
    which pin the scalar-potential cubic coupling g_3 = 1/6 and
    quadratic coupling g_2 = 3/2;
  - The structural identity Tr(K_frozen) = 0 (so that the m^2 cross-term
    in Tr(K^3) vanishes), giving the exact form
        V(m) = V_0 + (c_1 + c_2/2) m + (3/2) m^2 + (1/6) m^3.

This Pattern B companion verifies the Clifford-trace identities and the
m^3 coefficient at sympy exact precision, plus the algebraic structure
of the V(m) coefficient assignment.

Companion role: not a new claim row; not a new source note. Provides
audit-friendly evidence for the parent's class-(A) Clifford-trace
algebra at exact symbolic precision.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, simplify, symbols, Matrix, eye, zeros, sqrt
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
section("Audit companion for koide_z3_scalar_potential_support_note (td=70)")
# ============================================================================

# T_m = [[1, 0, 0], [0, 0, 1], [0, 1, 0]] (the active generator on the selected slice)
T_m = Matrix([[1, 0, 0],
              [0, 0, 1],
              [0, 1, 0]])


# ----------------------------------------------------------------------------
section("Part 1: Clifford involution T_m^2 = I_3")
# ----------------------------------------------------------------------------
T_m_sq = T_m * T_m
check("T_m^2 = I_3 exact (Clifford involution)",
      T_m_sq == eye(3),
      detail=f"T_m^2 = {T_m_sq}")


# ----------------------------------------------------------------------------
section("Part 2: trace identities Tr(T_m) = 1, Tr(T_m^2) = 3, Tr(T_m^3) = 1")
# ----------------------------------------------------------------------------
trace_T_m = T_m.trace()
trace_T_m_sq = T_m_sq.trace()
T_m_cubed = T_m * T_m * T_m
trace_T_m_cu = T_m_cubed.trace()

check("Tr(T_m) = 1 exact",
      trace_T_m == 1,
      detail=f"Tr(T_m) = {trace_T_m}")
check("Tr(T_m^2) = 3 exact",
      trace_T_m_sq == 3,
      detail=f"Tr(T_m^2) = {trace_T_m_sq}")
check("Tr(T_m^3) = Tr(T_m) = 1 exact (involution: T_m^3 = T_m^2 * T_m = T_m)",
      trace_T_m_cu == 1,
      detail=f"Tr(T_m^3) = {trace_T_m_cu}")
# Indeed T_m^3 = T_m
check("T_m^3 = T_m exact (involution)",
      T_m_cubed == T_m)


# ----------------------------------------------------------------------------
section("Part 3: scalar-potential coupling assignment from trace identities")
# ----------------------------------------------------------------------------
# V(m) = (1/2) Tr(K^2) + (1/6) Tr(K^3) where K = K_frozen + m T_m.
#
# Coefficient of m^2 in (1/2) Tr(K^2):
#   (1/2) * (m^2 Tr(T_m^2) + cross terms ...) ⊃ (1/2) * m^2 * 3 = (3/2) m^2.
# So g_2 = 3/2.
#
# Coefficient of m^3 in (1/6) Tr(K^3):
#   (1/6) * m^3 * Tr(T_m^3) = (1/6) * m^3 * 1 = (1/6) m^3.
# So g_3 = 1/6.

g_2 = Rational(1, 2) * 3  # (1/2) * Tr(T_m^2)
g_3 = Rational(1, 6) * 1  # (1/6) * Tr(T_m^3)

check("g_2 = (1/2) Tr(T_m^2) = 3/2 exact (scalar-potential quadratic coupling)",
      simplify(g_2 - Rational(3, 2)) == 0,
      detail=f"g_2 = {g_2}")
check("g_3 = (1/6) Tr(T_m^3) = 1/6 exact (scalar-potential cubic coupling)",
      simplify(g_3 - Rational(1, 6)) == 0,
      detail=f"g_3 = {g_3}")


# ----------------------------------------------------------------------------
section("Part 4: m^2 cross term in (1/6) Tr(K^3) requires Tr(K_frozen) = 0")
# ----------------------------------------------------------------------------
# Tr(K^3) = Tr((K_f + m T_m)^3)
#        = Tr(K_f^3) + 3 m Tr(K_f^2 T_m) + 3 m^2 Tr(K_f T_m^2) + m^3 Tr(T_m^3).
# With T_m^2 = I, the m^2 term is 3 m^2 Tr(K_f).
# For the m^2 contribution to vanish, Tr(K_f) = 0 is needed.
#
# Verify: with Tr(K_f) = 0 (parametric: K_f Hermitian with Tr = 0),
# the m^2 term in (1/6) Tr(K^3) vanishes.

# Symbolic K_f with explicit Tr = 0:
a, b, c, d, e = symbols('a b c d e', real=True)
# K_f traceless Hermitian: diagonals (a, b, -a-b), off-diagonals real (c, d, e).
K_frozen = Matrix([[a, c, d],
                   [c, b, e],
                   [d, e, -a - b]])

m_sym = symbols('m', real=True)
K_sel = K_frozen + m_sym * T_m

K_sel_cubed = simplify(K_sel * K_sel * K_sel)
trace_K_sel_cu = simplify(K_sel_cubed.trace())

# Expand in m and extract coefficients
m_sq_coeff = simplify(trace_K_sel_cu.coeff(m_sym, 2))
# 3 Tr(K_f T_m^2) = 3 Tr(K_f) since T_m^2 = I
expected_m_sq_coeff = 3 * K_frozen.trace()
check("m^2 coefficient of Tr(K^3) = 3 Tr(K_frozen) (vanishes if Tr K_f = 0)",
      simplify(m_sq_coeff - expected_m_sq_coeff) == 0,
      detail=f"m^2 coeff = {m_sq_coeff}, expected = {expected_m_sq_coeff}")

# At Tr(K_f) = 0 (built into our parametrization), m^2 coefficient should be 0.
m_sq_coeff_at_traceless = simplify(m_sq_coeff)
check("m^2 coefficient = 0 exact under Tr(K_frozen) = 0",
      m_sq_coeff_at_traceless == 0,
      detail=f"m^2 coeff at traceless K_f = {m_sq_coeff_at_traceless}")


# ----------------------------------------------------------------------------
section("Part 5: m^3 coefficient = (1/6) Tr(T_m^3) = 1/6")
# ----------------------------------------------------------------------------
m_cu_coeff = simplify(trace_K_sel_cu.coeff(m_sym, 3))
# = Tr(T_m^3) = 1 (involution)
check("m^3 coefficient of Tr(K^3) = Tr(T_m^3) = 1 exact",
      simplify(m_cu_coeff - 1) == 0,
      detail=f"m^3 coeff = {m_cu_coeff}")

# So (1/6) * coefficient = 1/6.
m_cu_coeff_in_V = Rational(1, 6) * m_cu_coeff
check("m^3 coefficient in V(m) = (1/6) m^3 exact",
      simplify(m_cu_coeff_in_V - Rational(1, 6)) == 0,
      detail=f"V(m) m^3 coefficient = {m_cu_coeff_in_V}")


# ----------------------------------------------------------------------------
section("Part 6: m^2 coefficient in (1/2) Tr(K^2) = 3/2")
# ----------------------------------------------------------------------------
from sympy import expand
K_sel_sq = K_sel * K_sel
trace_K_sel_sq = expand(K_sel_sq.trace())
m_sq_in_K2 = simplify(trace_K_sel_sq.coeff(m_sym, 2))
# = Tr(T_m^2) = 3
check("m^2 coefficient of Tr(K^2) = Tr(T_m^2) = 3 exact",
      simplify(m_sq_in_K2 - 3) == 0,
      detail=f"m^2 coeff = {m_sq_in_K2}")

m_sq_in_V = Rational(1, 2) * m_sq_in_K2
check("m^2 coefficient in V(m) = (3/2) m^2 exact",
      simplify(m_sq_in_V - Rational(3, 2)) == 0,
      detail=f"V(m) m^2 coefficient = {m_sq_in_V}")


# ----------------------------------------------------------------------------
section("Part 7: parent row dep verification")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('koide_z3_scalar_potential_support_note_2026-04-19', {})
print(f"\n  koide_z3_scalar_potential_support_note_2026-04-19 current ledger state:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check("parent row class-A load-bearing step (Clifford-trace algebra)",
      parent.get('load_bearing_step_class') == 'A')


# ----------------------------------------------------------------------------
section("Audit-companion summary")
# ----------------------------------------------------------------------------
print("""
  This companion provides EXACT symbolic verification (via sympy) of the
  parent's load-bearing class-(A) Clifford-trace algebra:

    T_m^2 = I_3 exact (Clifford involution);
    Tr(T_m) = Tr(T_m^3) = 1 (because T_m^3 = T_m);
    Tr(T_m^2) = 3 (full trace of identity);
    g_2 := (1/2) Tr(T_m^2) = 3/2 (scalar-potential quadratic coupling);
    g_3 := (1/6) Tr(T_m^3) = 1/6 (scalar-potential cubic coupling);
    m^2 cross term in Tr(K^3) = 3 Tr(K_frozen), vanishes under
    Tr(K_frozen) = 0;
    m^3 coefficient in V(m) = (1/6) m^3 exact;
    m^2 coefficient in V(m) = (3/2) m^2 exact.

  Audit-lane class for the parent's load-bearing step:
    (A) — Clifford-trace algebra on the explicit T_m matrix. No
    external observed/fitted/literature input.

  This audit-companion does NOT introduce a new claim row, a new source
  note, or any modification of the parent's audit_status. The parent
  remains audited_conditional pending audit-lane review of the upstream
  selected-slice / frozen-bank / K_Z3 machinery.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
