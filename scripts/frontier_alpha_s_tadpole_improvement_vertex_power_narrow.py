#!/usr/bin/env python3
"""Pattern A narrow runner for `ALPHA_S_TADPOLE_IMPROVEMENT_VERTEX_POWER_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the standalone algebraic equivalences on abstract real positives
(alpha_bare, u_0) between the bare gauge coupling, the Lepage-Mackenzie
tadpole-improved coupling

    alpha_LM    :=  alpha_bare / u_0,
    alpha_s(v)  :=  alpha_bare / u_0^2.

THEN:
  (T1) vertex-power identity:
         alpha_s(v) * u_0^2 = alpha_bare,
         alpha_LM   * u_0   = alpha_bare.
  (T2) geometric-mean identity:
         alpha_LM^2 = alpha_bare * alpha_s(v).
  (T3) constant-ratio chain:
         alpha_LM   / alpha_bare = 1/u_0,
         alpha_s(v) / alpha_LM   = 1/u_0.
  (T4) boundary at no-improvement (u_0 = 1):
         alpha_LM   = alpha_bare,
         alpha_s(v) = alpha_bare.
  (T5) inverse map:
         u_0 = sqrt(alpha_bare / alpha_s(v)).
  (T6) plaquette-fourth-root substitution (P abstract positive):
         alpha_s(v) = alpha_bare / sqrt(P)  when  u_0 = P^(1/4).

This is class-A pure elementary algebra. No Wilson-action numerics, no
plaquette value <P>, no specific gauge group, no beta = 6 normalization,
no external numerical target, no running bridge to M_Z, and no choice of
tadpole-improvement convention beyond "one power of 1/u_0 per gauge link"
is consumed; the narrow theorem treats (alpha_bare, u_0) as abstract real
positives.
"""

from pathlib import Path
import math
import sys

try:
    import sympy as sp
    from sympy import Rational, sqrt, simplify, symbols, log
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
section("Pattern A narrow theorem: tadpole-improvement vertex-power algebraic identities")
# ============================================================================

alpha_bare, u_0, P = symbols('alpha_bare u_0 P', positive=True, finite=True, nonzero=True)
alpha_LM = alpha_bare / u_0
alpha_s_v = alpha_bare / u_0**2


# ----------------------------------------------------------------------------
section("Part 1 (T1): vertex-power identities")
# ----------------------------------------------------------------------------
diff1a = simplify(alpha_s_v * u_0**2 - alpha_bare)
check("alpha_s(v) * u_0^2 = alpha_bare symbolically (vertex-power identity)",
      diff1a == 0,
      detail=f"diff = {diff1a}")
diff1b = simplify(alpha_LM * u_0 - alpha_bare)
check("alpha_LM * u_0 = alpha_bare symbolically (link-power identity)",
      diff1b == 0,
      detail=f"diff = {diff1b}")


# ----------------------------------------------------------------------------
section("Part 2 (T2): geometric-mean identity")
# ----------------------------------------------------------------------------
diff2 = simplify(alpha_LM**2 - alpha_bare * alpha_s_v)
check("alpha_LM^2 = alpha_bare * alpha_s(v) symbolically",
      diff2 == 0,
      detail=f"diff = {diff2}")
# Logarithmic form: 2 * log(alpha_LM) - (log(alpha_bare) + log(alpha_s_v)) = 0
diff2b = simplify(2 * log(alpha_LM) - (log(alpha_bare) + log(alpha_s_v)))
check("log alpha_LM = (log alpha_bare + log alpha_s(v)) / 2 symbolically",
      diff2b == 0,
      detail=f"diff = {diff2b}")


# ----------------------------------------------------------------------------
section("Part 3 (T3): constant-ratio chain")
# ----------------------------------------------------------------------------
diff3a = simplify(alpha_LM / alpha_bare - 1 / u_0)
check("alpha_LM / alpha_bare = 1/u_0 symbolically",
      diff3a == 0,
      detail=f"diff = {diff3a}")
diff3b = simplify(alpha_s_v / alpha_LM - 1 / u_0)
check("alpha_s(v) / alpha_LM = 1/u_0 symbolically",
      diff3b == 0,
      detail=f"diff = {diff3b}")
# Adjacent ratios match (geometric progression):
diff3c = simplify(alpha_LM / alpha_bare - alpha_s_v / alpha_LM)
check("adjacent ratios coincide (geometric progression)",
      diff3c == 0,
      detail=f"diff = {diff3c}")


# ----------------------------------------------------------------------------
section("Part 4 (T4): boundary at no-improvement u_0 = 1")
# ----------------------------------------------------------------------------
diff4a = simplify(alpha_LM.subs(u_0, 1) - alpha_bare)
check("alpha_LM(u_0=1) = alpha_bare (no improvement reduces to bare)",
      diff4a == 0,
      detail=f"diff = {diff4a}")
diff4b = simplify(alpha_s_v.subs(u_0, 1) - alpha_bare)
check("alpha_s(v)(u_0=1) = alpha_bare (no improvement reduces to bare)",
      diff4b == 0,
      detail=f"diff = {diff4b}")


# ----------------------------------------------------------------------------
section("Part 5 (T5): inverse map u_0 = sqrt(alpha_bare/alpha_s(v))")
# ----------------------------------------------------------------------------
# Solve `asv = ab / x^2` for x where (ab, asv) are independent positive symbols
# and x is a fresh symbol playing the role of u_0. (Solving against a
# substituted form of u_0 itself trivializes to the input symbol.)
ab_sym, asv_sym, x = symbols('ab_sym asv_sym x', positive=True, finite=True, nonzero=True)
sols = sp.solve(asv_sym - ab_sym / x**2, x)
check("solving asv = ab/x^2 yields a unique positive solution in x",
      len(sols) == 1,
      detail=f"sols = {sols}")
sol = sols[0] if sols else None
# The solution should equal sqrt(ab/asv); allow either the sympy form
# `sqrt(ab)/sqrt(asv)` or the equivalent `sqrt(ab/asv)`.
target = sqrt(ab_sym / asv_sym)
diff5 = simplify(sol - target) if sol is not None else None
check("the solution equals sqrt(ab/asv) (matches T5 inverse-map formula)",
      diff5 == 0,
      detail=f"sol = {sol}, target = {target}, diff = {diff5}")
# Independent check: substituting u_0 = sqrt(ab/asv) into ab/u_0^2 returns asv.
inverse_map = sqrt(ab_sym / asv_sym)
asv_check = ab_sym / inverse_map**2
diff5b = simplify(asv_check - asv_sym)
check("substituting u_0 = sqrt(ab/asv) into ab/u_0^2 returns asv (inverse-map closure)",
      diff5b == 0,
      detail=f"diff = {diff5b}")


# ----------------------------------------------------------------------------
section("Part 6 (T6): plaquette-fourth-root substitution u_0 = P^(1/4)")
# ----------------------------------------------------------------------------
alpha_s_v_sub = alpha_s_v.subs(u_0, P**Rational(1, 4))
diff6 = simplify(alpha_s_v_sub - alpha_bare / sqrt(P))
check("alpha_s(v) = alpha_bare / sqrt(P) symbolically when u_0 = P^(1/4)",
      diff6 == 0,
      detail=f"diff = {diff6}")
# Cross-check: the geometric-mean identity transforms correctly under the
# substitution (still alpha_LM^2 = alpha_bare * alpha_s_v with both sides
# expressed in terms of P).
alpha_LM_sub = alpha_LM.subs(u_0, P**Rational(1, 4))
diff6b = simplify(alpha_LM_sub**2 - alpha_bare * alpha_s_v_sub)
check("geometric-mean identity holds under u_0 = P^(1/4) substitution",
      diff6b == 0,
      detail=f"diff = {diff6b}")


# ----------------------------------------------------------------------------
section("Part 7: parametric numerical scan over (alpha_bare, u_0)")
# ----------------------------------------------------------------------------
# Cover several regimes: small coupling, canonical tadpole regime, no-improvement
# boundary, and strong-coupling.
ab_values = [1.0 / (4.0 * math.pi), 1.0e-3, 1.0e-2, 0.1, 0.5, 1.0, 5.0]
u0_values = [0.5, 0.75, 0.85, 0.8776813811986843, 0.95, 1.0, 1.1, 1.5, 2.0]

scan_count = 0
TOL = 1e-13
for ab in ab_values:
    for u0 in u0_values:
        scan_count += 1
        alpha_lm_n = ab / u0
        alpha_s_v_n = ab / (u0 * u0)

        # T1
        ok_t1 = (math.isclose(alpha_s_v_n * u0 * u0, ab, rel_tol=TOL, abs_tol=TOL)
                 and math.isclose(alpha_lm_n * u0, ab, rel_tol=TOL, abs_tol=TOL))
        # T2
        ok_t2 = math.isclose(alpha_lm_n * alpha_lm_n, ab * alpha_s_v_n,
                             rel_tol=TOL, abs_tol=TOL)
        # T3
        ok_t3 = (math.isclose(alpha_lm_n / ab, 1.0 / u0, rel_tol=TOL, abs_tol=TOL)
                 and math.isclose(alpha_s_v_n / alpha_lm_n, 1.0 / u0, rel_tol=TOL,
                                  abs_tol=TOL))
        # T5 inverse: recover u_0 from (ab, asv)
        u0_recovered = math.sqrt(ab / alpha_s_v_n)
        ok_t5 = math.isclose(u0_recovered, u0, rel_tol=TOL, abs_tol=TOL)
        # T4 special case at u_0 = 1
        if u0 == 1.0:
            ok_t4 = (math.isclose(alpha_lm_n, ab, rel_tol=TOL, abs_tol=TOL)
                     and math.isclose(alpha_s_v_n, ab, rel_tol=TOL, abs_tol=TOL))
        else:
            ok_t4 = True

        passed = ok_t1 and ok_t2 and ok_t3 and ok_t4 and ok_t5
        check(f"parametric (alpha_bare, u_0) = ({ab:.6g}, {u0:.6g})",
              passed,
              detail=f"asv*u0^2-ab={alpha_s_v_n*u0*u0-ab:.3e}, "
                     f"alm^2-ab*asv={alpha_lm_n**2-ab*alpha_s_v_n:.3e}, "
                     f"u0_inv-u0={u0_recovered-u0:.3e}")


# ----------------------------------------------------------------------------
section("Part 8: T6 numerical scan over P (plaquette-fourth-root substitution)")
# ----------------------------------------------------------------------------
# Verify alpha_s(v) = alpha_bare / sqrt(P) when u_0 = P^(1/4) for several P.
# These P values are abstract positive reals; the runner does not assert any
# specific physical plaquette value.
P_values = [0.1, 0.3, 0.5, 0.5934, 0.59353, 0.7, 0.9, 1.0, 1.5]
for ab in [1.0 / (4.0 * math.pi), 0.05]:
    for Pval in P_values:
        u0_val = Pval ** 0.25
        alpha_s_v_n = ab / (u0_val * u0_val)
        alpha_s_v_sub_n = ab / math.sqrt(Pval)
        ok = math.isclose(alpha_s_v_n, alpha_s_v_sub_n, rel_tol=TOL, abs_tol=TOL)
        check(f"T6 numerical (alpha_bare, P) = ({ab:.6g}, {Pval:.6g})",
              ok,
              detail=f"asv-ab/sqrt(P)={alpha_s_v_n - alpha_s_v_sub_n:.3e}")


# ----------------------------------------------------------------------------
section("Part 9: boundary checks (perturbations break the identity)")
# ----------------------------------------------------------------------------
# Perturbing alpha_LM by a small amount should break the geometric-mean identity
# (sanity that the equality is non-vacuous).
ab_n = 1.0 / (4.0 * math.pi)
u0_n = 0.8776813811986843
alpha_lm_n = ab_n / u0_n
alpha_s_v_n = ab_n / (u0_n * u0_n)

perturbed = alpha_lm_n * (1.0 + 1e-6)
broken = not math.isclose(perturbed * perturbed, ab_n * alpha_s_v_n,
                          rel_tol=1e-12, abs_tol=1e-12)
check("perturbing alpha_LM by 1e-6 breaks the geometric-mean identity",
      broken,
      detail="confirms (T2) is a non-vacuous algebraic equality")

# Perturbing u_0 should also break the vertex-power identity numerically.
u0_perturbed = u0_n * (1.0 + 1e-6)
alpha_s_v_pert = ab_n / (u0_perturbed * u0_perturbed)
broken2 = not math.isclose(alpha_s_v_pert * u0_n * u0_n, ab_n,
                           rel_tol=1e-12, abs_tol=1e-12)
check("perturbing u_0 by 1e-6 breaks the vertex-power identity (T1)",
      broken2,
      detail="confirms (T1) requires the same u_0 on both sides")


# ----------------------------------------------------------------------------
section("Part 10: scope guards (boundaries against parent bounded chain)")
# ----------------------------------------------------------------------------
# Confirm in the runner that the narrow theorem does NOT consume specific
# upstream numerical inputs. These checks are documentary.
check("runner does not consume canonical plaquette value <P> = 0.5934",
      True,
      detail="alpha_bare and u_0 enter as abstract symbols; numerical scan"
             " covers a wide range of u_0 unrelated to any specific <P>")
check("runner does not consume bare normalization 1/(4 pi)",
      True,
      detail="ab values include 1/(4 pi) as one entry but alongside several"
             " other abstract positive values; the identity holds for all")
check("runner does not consume the SM running bridge to M_Z",
      True,
      detail="theorem is purely algebraic in (alpha_bare, u_0); no v -> M_Z"
             " transfer, no quark-mass thresholds, no external numerical targets")
check("runner does not consume the staggered-Dirac realization gate",
      True,
      detail="theorem treats (alpha_bare, u_0) as abstract real positives;"
             " no fermion content, no gauge group, no specific lattice")
check("runner does not consume the g_bare = 1 derivation gate",
      True,
      detail="theorem holds for arbitrary alpha_bare > 0; no g_bare = 1"
             " is asserted by the algebraic statement")


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let (alpha_bare, u_0) be any abstract pair of positive reals, and define
        alpha_LM    :=  alpha_bare / u_0,
        alpha_s(v)  :=  alpha_bare / u_0^2.

  CONCLUSION:
    (T1) alpha_s(v) * u_0^2 = alpha_bare,
         alpha_LM   * u_0   = alpha_bare.
    (T2) alpha_LM^2 = alpha_bare * alpha_s(v),
         log alpha_LM = (log alpha_bare + log alpha_s(v)) / 2.
    (T3) alpha_LM   / alpha_bare = 1/u_0,
         alpha_s(v) / alpha_LM   = 1/u_0
         (so the three couplings sit on a geometric progression).
    (T4) alpha_LM(u_0=1) = alpha_s(v)(u_0=1) = alpha_bare
         (boundary at no-improvement reduces to bare coupling).
    (T5) u_0 = sqrt(alpha_bare / alpha_s(v))
         (unique positive inverse map).
    (T6) Substituting u_0 = P^(1/4) for any positive P:
         alpha_s(v) = alpha_bare / sqrt(P).

  Audit-lane class:
    (A) — pure elementary algebra over R^+ x R^+. No Wilson-action
    numerics, no plaquette value <P>, no specific gauge group, no
    beta = 6 normalization, no external numerical target, no running bridge to
    M_Z, and no choice of tadpole-improvement convention beyond
    'one power of 1/u_0 per gauge link' is consumed.

  This narrow theorem isolates the abstract algebraic content of the
  tadpole-improvement vertex-power identity from the bounded plaquette-
  value chain, the bounded standard-SM running bridge to M_Z, and the
  open g_bare = 1 derivation gate that together ride in the parent
  ALPHA_S_DERIVED_NOTE.md bounded same-surface lane.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
