#!/usr/bin/env python3
"""Pattern A narrow runner for
`KOIDE_CIRCULANT_Q_TWO_THIRDS_ALGEBRAIC_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies, on abstract real symbols (v_0 > 0, delta in R), the standalone
trigonometric / algebraic identity that the three real positive numbers

    x_k := v_0 (1 + sqrt(2) cos(delta + 2 pi k / 3)),    k = 0, 1, 2,

satisfy
  (T1) sum_k cos(delta + 2 pi k / 3) = 0,
  (T2) sum_k cos^2(delta + 2 pi k / 3) = 3/2,
  (T3) (sum_k x_k^2) / (sum_k x_k)^2 = 2/3,    independent of (v_0, delta).

This narrow theorem treats (v_0, delta) as ABSTRACT SYMBOLS. It does
NOT identify x_k with sqrt(m_k) for any charged-lepton mass m_k, does
NOT derive or assume the sqrt(2) equipartition coefficient (BAE
condition), does NOT derive v_0 or delta, and does NOT consume any
PDG / literature / Wilson / spectrum-side selection-principle authority.

Companion role: not a new audit-companion; this is a Pattern A new
narrow claim row carving out the algebraic core of the existing
`koide_circulant_character_derivation_note_2026-04-18`
(claim_type=positive_theorem, load_bearing_step_class=A).
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import (
        Rational, sqrt, simplify, symbols, expand, expand_complex, factor,
        cos, sin, pi, trigsimp, exp, I, conjugate,
    )
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
section("Pattern A narrow theorem: Brannen/Rivero Q = 2/3 algebraic identity")
# ============================================================================

# Symbolic ingredients: delta (real), v_0 (positive real), and the three angles.
delta = symbols("delta", real=True)
v_0 = symbols("v_0", positive=True, real=True)


# ----------------------------------------------------------------------------
section("Part 1: root-of-unity sanity 1 + omega + omega^2 = 0 (omega = e^{2 pi i / 3})")
# ----------------------------------------------------------------------------
omega = exp(2 * pi * I / 3)
sum_omega = expand_complex(1 + omega + omega**2)
check("1 + omega + omega^2 = 0 (primitive cube root of unity)",
      simplify(sum_omega) == 0,
      detail=f"1 + omega + omega^2 = {sum_omega}")

# Equivalent: sum_k omega^{2 k} = 1 + omega^2 + omega^4 = 0 (since omega^4 = omega).
sum_omega_2k = expand_complex(1 + omega**2 + omega**4)
check("1 + omega^2 + omega^4 = 0 (re-indexed)",
      simplify(sum_omega_2k) == 0,
      detail=f"1 + omega^2 + omega^4 = {sum_omega_2k}")


# ----------------------------------------------------------------------------
section("Part 2 (T1): sum_k cos(delta + 2 pi k / 3) = 0")
# ----------------------------------------------------------------------------
theta = [delta + 2 * pi * k / 3 for k in (0, 1, 2)]
sum_cos = simplify(sum(cos(t) for t in theta))
check("sum_k cos(delta + 2 pi k / 3) = 0 symbolically",
      simplify(trigsimp(sum_cos)) == 0,
      detail=f"sum_k cos(theta_k) = {trigsimp(sum_cos)}")


# ----------------------------------------------------------------------------
section("Part 3 (T2): sum_k cos^2(delta + 2 pi k / 3) = 3/2")
# ----------------------------------------------------------------------------
sum_cos_sq = simplify(sum(cos(t)**2 for t in theta))
sum_cos_sq_red = simplify(trigsimp(sum_cos_sq) - Rational(3, 2))
check("sum_k cos^2(delta + 2 pi k / 3) = 3/2 symbolically",
      simplify(sum_cos_sq_red) == 0,
      detail=f"sum_k cos^2(theta_k) - 3/2 = {sum_cos_sq_red}")


# ----------------------------------------------------------------------------
section("Part 4 (T3): (sum_k x_k^2) / (sum_k x_k)^2 = 2/3")
# ----------------------------------------------------------------------------
x = [v_0 * (1 + sqrt(2) * cos(t)) for t in theta]

# sum_k x_k = 3 v_0 (T1).
sum_x = simplify(sum(x))
sum_x_red = simplify(trigsimp(sum_x) - 3 * v_0)
check("sum_k x_k = 3 v_0 symbolically (uses T1)",
      simplify(sum_x_red) == 0,
      detail=f"sum_k x_k - 3 v_0 = {sum_x_red}")

# sum_k x_k^2 = 6 v_0^2 (T1 + T2).
sum_x_sq = simplify(sum(xi**2 for xi in x))
# Expand: x_k^2 = v_0^2 (1 + 2 sqrt(2) cos(theta_k) + 2 cos^2(theta_k)).
# sum_k x_k^2 = v_0^2 (3 + 2 sqrt(2) * 0 + 2 * 3/2) = 6 v_0^2.
sum_x_sq_red = simplify(trigsimp(sum_x_sq) - 6 * v_0**2)
check("sum_k x_k^2 = 6 v_0^2 symbolically (uses T1 + T2)",
      simplify(sum_x_sq_red) == 0,
      detail=f"sum_k x_k^2 - 6 v_0^2 = {sum_x_sq_red}")

# Ratio = 6 v_0^2 / (3 v_0)^2 = 2/3 independent of v_0 and delta.
ratio = simplify(sum_x_sq / sum_x**2)
ratio_red = simplify(trigsimp(ratio) - Rational(2, 3))
check("(sum_k x_k^2) / (sum_k x_k)^2 = 2/3 symbolically",
      simplify(ratio_red) == 0,
      detail=f"ratio - 2/3 = {ratio_red}")


# ----------------------------------------------------------------------------
section("Part 5: independence of ratio from delta at 5 sample angles and 3 v_0 values")
# ----------------------------------------------------------------------------
# Sanity grid (no PDG values; v_0 and delta are abstract symbols):
delta_samples = [Rational(0), pi / 12, Rational(2, 9), pi / 3, pi / 2]
v0_samples = [Rational(1), pi, exp(1)]

count = 0
for d_val in delta_samples:
    for v0_val in v0_samples:
        count += 1
        x_subs = [v0_val * (1 + sqrt(2) * cos(d_val + 2 * pi * k / 3))
                  for k in (0, 1, 2)]
        sum_x_sub = simplify(sum(x_subs))
        sum_x_sq_sub = simplify(sum(xi**2 for xi in x_subs))
        ratio_sub = simplify(sum_x_sq_sub / sum_x_sub**2)
        # Demand exact 2/3 (sympy radical / pi-symbolic precision).
        ratio_diff = simplify(ratio_sub - Rational(2, 3))
        check(f"sample #{count}: delta={d_val}, v_0={v0_val} gives ratio = 2/3",
              simplify(ratio_diff) == 0,
              detail=f"ratio - 2/3 = {ratio_diff}")


# ----------------------------------------------------------------------------
section("Part 6: corollary - with m_k := x_k^2, (sum_k m_k) / (sum_k sqrt(m_k))^2 = 2/3")
# ----------------------------------------------------------------------------
# When x_k > 0 (which the runner does NOT assume globally, but the corollary
# is symbolic on x_k > 0), sqrt(m_k) = sqrt(x_k^2) = x_k, so
# (sum_k m_k) / (sum_k sqrt(m_k))^2 = (sum_k x_k^2) / (sum_k x_k)^2 = 2/3.
# The runner verifies this purely-algebraic identity:
# (sum_k x_k^2) / (sum_k x_k)^2 -- same expression as (T3).
print("\n  Corollary statement: with m_k := x_k^2 and assuming x_k > 0,")
print("  (sum_k m_k) / (sum_k sqrt(m_k))^2 = (sum_k x_k^2) / (sum_k x_k)^2 = 2/3.")
print("  The algebraic identity is identical to (T3); no new check required.")
check("corollary algebraic identity reduces to (T3) (no new content beyond (T3))",
      True, detail="corollary statement = (T3) under x_k > 0")


# ----------------------------------------------------------------------------
section("Part 7: parent / sibling row context (no ledger modification)")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
try:
    ledger = json.loads(LEDGER.read_text())
    parent = ledger['rows'].get(
        'koide_circulant_character_derivation_note_2026-04-18', {})
    sibling = ledger['rows'].get(
        'koide_circulant_character_bridge_narrow_theorem_note_2026-05-09', {})
    print(f"\n  Parent row state on origin/main:")
    print(f"    effective_status: {parent.get('effective_status')}")
    print(f"    claim_type:       {parent.get('claim_type')}")
    print(f"  Sister narrow row state on origin/main:")
    print(f"    effective_status: {sibling.get('effective_status')}")
    print(f"    claim_type:       {sibling.get('claim_type')}")

    check("parent row is unaudited (this narrow theorem is a rescope, not a promotion)",
          parent.get('effective_status') == 'unaudited',
          detail=f"effective_status = {parent.get('effective_status')}")
except Exception as e:
    check(f"parent-row ledger read (defensive)", False, detail=str(e))


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESES:
    Let v_0 > 0 and delta in R be abstract real symbols. Define
        x_k := v_0 (1 + sqrt(2) cos(delta + 2 pi k / 3)),  k = 0, 1, 2.

  CONCLUSIONS:
    (T1)  sum_k cos(delta + 2 pi k / 3) = 0   symbolic identity in delta.
    (T2)  sum_k cos^2(delta + 2 pi k / 3) = 3/2   symbolic identity in delta.
    (T3)  (sum_k x_k^2) / (sum_k x_k)^2 = 2/3   independent of (v_0, delta).

  Audit-lane class:
    (A) - pure trigonometric / algebraic identities on abstract real
    symbols. No PDG observed values, no literature numerical
    comparator, no fitted selectors, no admitted unit conventions,
    no sqrt(m) readout law, no equipartition selection principle.

  This narrow theorem isolates the algebraic Koide identity Q = 2/3
  of the parent KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18
  from its companion (i) sqrt(m) identification, (ii) sqrt(2)
  equipartition selection, and (iii) v_0/delta charged-lepton-scale
  identifications. The Open derivation gaps on those three
  identifications are preserved.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
print(f"PASS={PASS} FAIL={FAIL}")
sys.exit(1 if FAIL > 0 else 0)
