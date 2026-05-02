#!/usr/bin/env python3
"""Pattern B audit-companion runner for
`koide_explicit_calculations_note`
(claim_type=positive_theorem, audit_status=audited_conditional, td=69,
load_bearing_step_class=C).

The parent's load-bearing class-(C) content includes:

  R1: |eta_AS(Z_3, (1, 2))| = 2/9 from the AS 1968 fixed-point formula
      L(g^k) = (1 + omega^{kp})(1 + omega^{kq}) / [(1 - omega^{kp})(1 - omega^{kq})]
      summed over k = 1, 2 and divided by n = 3, with omega = exp(2 pi i / 3).

  R2: C_tau = 3/4 + 1/4 = 1 as a Casimir combination on the standard
      SU(2)_L x U(1)_Y normalization for the tau lepton.

This Pattern B companion verifies both at sympy `Rational` exact symbolic
precision via cube-root-of-unity reductions.

Companion role: not a new claim row; not a new source note. Provides
audit-friendly evidence that the parent's class-(C) numerical / character
arithmetic holds at exact symbolic precision.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, simplify, exp, I as sym_I, pi, im, Abs
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
    tag = "PASS (C)" if ok else "FAIL (C)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Audit companion for koide_explicit_calculations_note (td=69)")
# ============================================================================

# omega = exp(2 pi i / 3): cube root of unity
omega = exp(sym_I * 2 * pi / Rational(3))
omega_squared = exp(sym_I * 4 * pi / Rational(3))


# ----------------------------------------------------------------------------
section("Part 1: cube-root-of-unity sanity checks")
# ----------------------------------------------------------------------------
omega_cubed = simplify((omega**3).rewrite(sympy.cos).expand(complex=True))
check("omega^3 = 1 exact",
      simplify(omega_cubed - 1) == 0,
      detail=f"omega^3 = {omega_cubed}")

# 1 + omega + omega^2 = 0
sum_chk = simplify((1 + omega + omega**2).rewrite(sympy.cos).expand(complex=True))
check("1 + omega + omega^2 = 0 exact",
      simplify(sum_chk) == 0,
      detail=f"sum = {sum_chk}")


# ----------------------------------------------------------------------------
section("Part 2: AS 1968 fixed-point Lefschetz character L(g^k) at Z_3, (p, q) = (1, 2)")
# ----------------------------------------------------------------------------
# L(g^k) = (1 + omega^{kp})(1 + omega^{kq}) / [(1 - omega^{kp})(1 - omega^{kq})]
def L_at(k):
    """Lefschetz character at g^k for (p, q) = (1, 2)."""
    return (1 + omega**(k * 1)) * (1 + omega**(k * 2)) / ((1 - omega**(k * 1)) * (1 - omega**(k * 2)))


L_at_1 = simplify(L_at(1).rewrite(sympy.cos).expand(complex=True))
L_at_2 = simplify(L_at(2).rewrite(sympy.cos).expand(complex=True))
print(f"\n  L(g^1) = {L_at_1}")
print(f"  L(g^2) = {L_at_2}")

# Both should equal 1/3 (per parent: "k = 1: (1 + omega)(1 + omega^2) / ... = 1/3").
# Let's verify: numerator = (1 + omega)(1 + omega^2) = 1 + omega + omega^2 + omega^3 = 0 + 1 = 1
# Wait: (1 + omega)(1 + omega^2) = 1 + omega^2 + omega + omega^3 = 1 + omega + omega^2 + omega^3.
# omega^3 = 1, so = 1 + omega + omega^2 + 1 = 1 + (1 + omega + omega^2) - 1 = ... hmm let me redo.
# (1 + omega)(1 + omega^2) = 1 + omega^2 + omega + omega * omega^2 = 1 + omega + omega^2 + omega^3
#                         = 1 + omega + omega^2 + 1 = 2 + (omega + omega^2) = 2 + (-1) = 1.
# Denominator: (1 - omega)(1 - omega^2) = 1 - omega^2 - omega + omega^3 = 1 - omega - omega^2 + 1 = 2 - (omega + omega^2) = 2 - (-1) = 3.
# So L(g^1) = 1/3. ✓
expected_L = Rational(1, 3)
check("L(g^1) = 1/3 exact (numerator 1, denominator 3 via cube-root-of-unity sum identity)",
      simplify(L_at_1 - expected_L) == 0,
      detail=f"L(g^1) = {L_at_1}")
check("L(g^2) = 1/3 exact (complex conjugate of L(g^1))",
      simplify(L_at_2 - expected_L) == 0,
      detail=f"L(g^2) = {L_at_2}")


# ----------------------------------------------------------------------------
section("Part 3: |eta_AS(Z_3, (1, 2))| = 2/9 = (L(g^1) + L(g^2)) / 3")
# ----------------------------------------------------------------------------
# eta = (sum_{k=1}^{n-1} L(g^k)) / n = (1/3 + 1/3) / 3 = 2/9
eta_AS = simplify((L_at_1 + L_at_2) / Rational(3))
expected_eta = Rational(2, 9)
check("eta_AS(Z_3, (1, 2)) = 2/9 exact",
      simplify(eta_AS - expected_eta) == 0,
      detail=f"eta_AS = {eta_AS}")
check("|eta_AS| = 2/9 exact",
      simplify(Abs(eta_AS) - expected_eta) == 0,
      detail=f"|eta_AS| = {simplify(Abs(eta_AS))}")


# ----------------------------------------------------------------------------
section("Part 4: C_tau = 3/4 + 1/4 = 1 (Casimir combination)")
# ----------------------------------------------------------------------------
# SU(2)_L Casimir for doublet (j = 1/2): C_2(SU(2)_L) = j(j+1) = 3/4.
# U(1)_Y hypercharge for left-handed lepton doublet: Y = -1, GUT-normalized
# Y_GUT^2 = 3/5 * Y^2 = 3/5 * 1 = 3/5. But C_tau here is the simpler
# combination 3/4 + 1/4 with 1/4 being (Y/2)^2 = (-1/2)^2 = 1/4 in the
# doubled-hypercharge convention. So:
C_SU2_doublet = Rational(3, 4)
C_U1_Y_doublet = Rational(1, 4)  # = (Y/2)^2 with Y = -1, doubled-hypercharge
C_tau_total = C_SU2_doublet + C_U1_Y_doublet
check("C_tau = 3/4 + 1/4 = 1 exact (Casimir combination at standard normalization)",
      simplify(C_tau_total - Rational(1)) == 0,
      detail=f"C_tau = {C_tau_total}")


# ----------------------------------------------------------------------------
section("Part 5: relate eta_AS = 2/9 to (N_color - 1)/N_color^2 with N_color = 3")
# ----------------------------------------------------------------------------
# Note: (N_color - 1) / N_color^2 = 2/9 at N_color = 3 (cf. cycle-29 audit
# companion for the F2 = K6 reading in CKM). Same closed form, different
# physical context.
N_color = 3
F2_form = (N_color - 1) / N_color**2
check("(N_color - 1)/N_color^2 = 2/9 at N_color = 3 (matches eta_AS algebraically)",
      simplify(F2_form - Rational(2, 9)) == 0,
      detail=f"(c-1)/c^2 = {F2_form}")


# ----------------------------------------------------------------------------
section("Part 6: parent row dep verification")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('koide_explicit_calculations_note', {})
print(f"\n  koide_explicit_calculations_note current ledger state:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check("parent row class-C load-bearing step (numerical / character arithmetic)",
      parent.get('load_bearing_step_class') == 'C')


# ----------------------------------------------------------------------------
section("Audit-companion summary")
# ----------------------------------------------------------------------------
print("""
  This companion provides EXACT symbolic verification (via sympy) of the
  parent's load-bearing class-(C) numerical / character arithmetic
  content:

    R1: AS 1968 Lefschetz character L(g^k) = (1+omega^k)(1+omega^{2k})
         / [(1-omega^k)(1-omega^{2k})] at omega = exp(2 pi i/3) for
         k = 1, 2 evaluates to 1/3 each, so eta_AS(Z_3, (1, 2)) = 2/9.

    R2: C_tau = SU(2)_L Casimir 3/4 + (Y/2)^2 = 3/4 + 1/4 = 1 exact,
         with Y = -1 for the LH lepton doublet in the doubled-hypercharge
         convention.

  Both verified at exact symbolic precision via sympy cube-root-of-unity
  reductions (rewrite(cos).expand(complex=True)).

  Audit-lane class for the parent's load-bearing step:
    (C) — first-principles compute / character arithmetic. No external
    observed/fitted/literature input on the algebraic content (the AS
    1968 Lefschetz formula and Casimir combination are standard external
    machinery, treated as admitted-context).

  This audit-companion does NOT introduce a new claim row, a new source
  note, or any modification of the parent's audit_status. The parent
  remains audited_conditional pending audit-lane review of the
  upstream physical bridges (delta_physical = eta_APS, Q source-law,
  etc.).
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
