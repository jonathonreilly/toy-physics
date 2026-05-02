#!/usr/bin/env python3
"""Pattern A narrow runner for `KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02`.

Verifies the standalone three-form algebraic equivalence on abstract real
triples (u, v, w):

  Form 1 (orbit-slot quadratic):
      F_orbit(u, v, w)  :=  4 (u v + u w + v w) - (u^2 + v^2 + w^2)  =  0.

  Form 2 (cyclic basis-change quadratic):
      With  r0 = u + v + w,  r1 = 2u - v - w,  r2 = sqrt(3) (v - w),
      F_cyclic(r0, r1, r2)  :=  2 r0^2 - r1^2 - r2^2  =  0.

  Form 3 (standard Koide ratio):
      F_ratio(u, v, w)  :=  3 (u^2 + v^2 + w^2) - 2 (u + v + w)^2  =  0,
      equivalently
      (u^2 + v^2 + w^2) / (u + v + w)^2  =  2/3   (provided u + v + w != 0).

  THEN:
    (i)  the three forms are pairwise equivalent on (u, v, w) ∈ R^3;
    (ii) the algebraic identity
             2 r0^2 - r1^2 - r2^2  =  2 [4 (u v + u w + v w) - (u^2 + v^2 + w^2)]
         holds for ALL (u, v, w) ∈ R^3 (not just on the Koide cone).

This is class-A pure polynomial algebra. No Koide / charged-lepton mass /
sqrt(m) physical identification is consumed; the narrow theorem treats
(u, v, w) as abstract real symbols.

Companion role: this is a Pattern A new narrow claim row carving out
the load-bearing class-(A) algebraic core of
`koide_gamma_orbit_selector_bridge_note_2026-04-18` (claim_type=
positive_theorem, audit_status=audited_conditional, td=74,
load_bearing_step_class=A). The narrow theorem isolates the three-form
algebraic equivalence from any Koide / charged-lepton / Gamma-orbit-return
upstream framing.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, sqrt, simplify, symbols, expand, factor, solve, Eq
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
section("Pattern A narrow theorem: Koide-cone three-form algebraic equivalence")
# ============================================================================

u, v, w = symbols('u v w', real=True)
r0 = u + v + w
r1 = 2 * u - v - w
r2 = sqrt(Rational(3)) * (v - w)


# ----------------------------------------------------------------------------
section("Part 1: identity 2 r0^2 - r1^2 - r2^2 = 2 [4(uv + uw + vw) - (u^2 + v^2 + w^2)]")
# ----------------------------------------------------------------------------
F_cyclic = simplify(2 * r0**2 - r1**2 - r2**2)
F_orbit = 4 * (u * v + u * w + v * w) - (u**2 + v**2 + w**2)
F_cyclic_expected = simplify(2 * F_orbit)

check("2 r0^2 - r1^2 - r2^2 = 2 [4(uv + uw + vw) - (u^2 + v^2 + w^2)] symbolically",
      simplify(F_cyclic - F_cyclic_expected) == 0,
      detail=f"diff = {simplify(F_cyclic - F_cyclic_expected)}")


# ----------------------------------------------------------------------------
section("Part 2: equivalence Form 1 (orbit) <=> Form 2 (cyclic)")
# ----------------------------------------------------------------------------
# F_cyclic = 2 F_orbit  =>  F_cyclic = 0  iff  F_orbit = 0.
check("F_cyclic = 0  iff  F_orbit = 0 (proportional, ratio = 2)",
      simplify(F_cyclic / F_orbit - 2) == 0,
      detail=f"F_cyclic / F_orbit = {simplify(F_cyclic / F_orbit)}")


# ----------------------------------------------------------------------------
section("Part 3: equivalence Form 1 (orbit) <=> Form 3 (ratio)")
# ----------------------------------------------------------------------------
# F_ratio = 3 (u^2 + v^2 + w^2) - 2 (u + v + w)^2
F_ratio = simplify(3 * (u**2 + v**2 + w**2) - 2 * (u + v + w)**2)
# Expand: 3(u^2 + v^2 + w^2) - 2(u^2 + v^2 + w^2 + 2(uv + uw + vw))
#       = (u^2 + v^2 + w^2) - 4(uv + uw + vw)
#       = -F_orbit
check("F_ratio = -F_orbit symbolically (3(u^2+v^2+w^2) - 2(u+v+w)^2 = -F_orbit)",
      simplify(F_ratio + F_orbit) == 0,
      detail=f"F_ratio + F_orbit = {simplify(F_ratio + F_orbit)}")
check("F_ratio = 0  iff  F_orbit = 0",
      True,
      detail="follows from F_ratio = -F_orbit")


# ----------------------------------------------------------------------------
section("Part 4: ratio form when u + v + w != 0")
# ----------------------------------------------------------------------------
# F_ratio = 0  iff  (u^2 + v^2 + w^2) / (u + v + w)^2 = 2/3  (when u+v+w != 0).
# Verify by direct substitution at concrete (u, v, w).
ratio_form = (u**2 + v**2 + w**2) / (u + v + w)**2

# At a Koide-cone point (e.g., u = 0, v = 1, w = sqrt(2) - 1, normalized).
# Easier: pick u = 1, v = 1, w arbitrary and solve F_orbit = 0.
sol_w = solve(F_orbit.subs({u: Rational(1), v: Rational(1)}), w)
print(f"\n  Solving F_orbit = 0 at u = v = 1: w = {sol_w}")
# Expect w = 4 - sqrt(13) or w = 4 + sqrt(13)... let me verify.
# At u = v = 1: 4(uv + uw + vw) - (u^2 + v^2 + w^2)
#             = 4(1 + w + w) - (1 + 1 + w^2)
#             = 4 + 8w - 2 - w^2
#             = -w^2 + 8w + 2
# Solving -w^2 + 8w + 2 = 0  =>  w^2 - 8w - 2 = 0  =>  w = (8 +/- sqrt(64 + 8)) / 2
#                              = 4 +/- sqrt(18) = 4 +/- 3 sqrt(2).

# Verify ratio at one solution:
for w_sol in sol_w:
    if w_sol.is_real:
        ratio_val = simplify(ratio_form.subs({u: Rational(1), v: Rational(1), w: w_sol}))
        check(f"at (u, v, w) = (1, 1, {w_sol}): (sum sq) / (sum)^2 = 2/3",
              simplify(ratio_val - Rational(2, 3)) == 0,
              detail=f"ratio = {ratio_val}")


# ----------------------------------------------------------------------------
section("Part 5: F_orbit = 0 has nontrivial solutions (Koide cone is non-empty)")
# ----------------------------------------------------------------------------
# At u = v = 1, the cone has w = 4 +/- 3 sqrt(2). The "+" branch is positive.
# (4 - 3 sqrt(2)) ≈ -0.24 is negative.
w_pos = 4 + 3 * sqrt(Rational(2))
w_neg = 4 - 3 * sqrt(Rational(2))

F_at_pos = simplify(F_orbit.subs({u: Rational(1), v: Rational(1), w: w_pos}))
F_at_neg = simplify(F_orbit.subs({u: Rational(1), v: Rational(1), w: w_neg}))
check("F_orbit(1, 1, 4 + 3 sqrt(2)) = 0 exact",
      F_at_pos == 0)
check("F_orbit(1, 1, 4 - 3 sqrt(2)) = 0 exact",
      F_at_neg == 0)


# ----------------------------------------------------------------------------
section("Part 6: (u, v, w) = (1, 1, 1) is OFF the cone (shows non-trivial constraint)")
# ----------------------------------------------------------------------------
F_at_111 = F_orbit.subs({u: Rational(1), v: Rational(1), w: Rational(1)})
# 4(1 + 1 + 1) - (1 + 1 + 1) = 12 - 3 = 9
check("F_orbit(1, 1, 1) = 9 != 0 (uniform triple is OFF the Koide cone)",
      F_at_111 == 9,
      detail=f"F_orbit(1,1,1) = {F_at_111}")
F_ratio_at_111 = ratio_form.subs({u: Rational(1), v: Rational(1), w: Rational(1)})
check("(u^2+v^2+w^2)/(u+v+w)^2 = 1/3 at (1,1,1) (NOT 2/3)",
      simplify(F_ratio_at_111 - Rational(1, 3)) == 0,
      detail=f"ratio at (1,1,1) = {F_ratio_at_111}")


# ----------------------------------------------------------------------------
section("Part 7: parent row context (no ledger modification)")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('koide_gamma_orbit_selector_bridge_note_2026-04-18', {})
print(f"\n  Parent row state on origin/main:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check("parent row class-A load-bearing step (algebraic identity)",
      parent.get('load_bearing_step_class') == 'A')


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let (u, v, w) be any abstract real triple, and define
        r0 = u + v + w,
        r1 = 2u - v - w,
        r2 = sqrt(3) (v - w).

  CONCLUSION:
    (i)   2 r0^2 - r1^2 - r2^2 = 2 [4(uv + uw + vw) - (u^2 + v^2 + w^2)]
          symbolic identity (holds for ALL (u, v, w) ∈ R^3).

    (ii)  Three-form equivalence on the cone:
              4(uv + uw + vw) - (u^2 + v^2 + w^2) = 0
              <=>  2 r0^2 = r1^2 + r2^2
              <=>  3(u^2 + v^2 + w^2) = 2(u + v + w)^2
              <=>  (u^2 + v^2 + w^2) / (u + v + w)^2 = 2/3
                   (when u + v + w != 0).

    (iii) The Koide cone is nontrivial: e.g., (u, v, w) = (1, 1, 4 + 3 sqrt(2))
          satisfies the cone exactly; (u, v, w) = (1, 1, 1) does NOT.

  Audit-lane class:
    (A) — pure polynomial algebra over R^3. No Koide / charged-lepton /
    Gamma-orbit-return / sqrt(m_i) physical identification.

  This narrow theorem isolates the algebraic three-form equivalence from
  any physical Koide / charged-lepton / Gamma-orbit-return upstream
  framing.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
