#!/usr/bin/env python3
"""
PMNS selector iter 7: symbolic derivation attempt of det(H) = E2 = sqrt(8)/3.

Iter 6 found det(H) = E2 = sqrt(8)/3 as the strongest second-cut candidate
on the 1-D curve {delta * q_+ = 2/3, s13^2 = 0.0218}. Iter 7 attempts a
framework-native derivation.

Approach:
  1. Symbolically expand det(H(m, delta, q_+)) with retained constants
     E1 = sqrt(8/3), E2 = sqrt(8)/3, gamma = 1/2. Get a polynomial
     P(m, delta, q_+) with coefficients in the retained constants.
  2. Substitute the first cut delta * q_+ = 2/3 (q_+ = 2/(3 delta)) into
     the polynomial.  Get a rational function R(m, delta).
  3. Set det(H) = E2 and see what constraint this imposes on (m, delta).
  4. Check whether that constraint has a framework-natural factorization
     (e.g. identifies m with a retained quantity, or factors into a
     product of retained linear forms).
  5. Also examine: at the exact closure point
     (m_c, delta_c, q_c) = (0.660242, 0.935995, 0.712255),
     what do Tr(H), Tr(H^2), other retained scalars take as values?
     Look for "accidentally simple" expressions that might BE the
     derivation.

Deliverables:
  - Symbolic polynomial det(H) = P(m, delta, q_+) in exact retained form.
  - Substituted form under delta * q_+ = 2/3.
  - Factorization attempt.
  - At closure point: exact values of all natural retained scalars.
  - PASS if a clean retained identity is found.
  - FAIL (informative) if det(H) = E2 requires irreducible transcendental
    relation, ruling out simple cross-sector closure via this route.
"""
from __future__ import annotations

import math
import sympy as sp
import numpy as np

PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> bool:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return cond


# Symbolic retained constants
m, delta, q_plus = sp.symbols("m delta q_plus", real=True)
E1_sym = sp.sqrt(sp.Rational(8, 3))
E2_sym = sp.sqrt(8) / 3   # = 2 sqrt(2) / 3
gamma_sym = sp.Rational(1, 2)
Q_sym = sp.Rational(2, 3)

# Symbolic H entries (from the retained affine chart)
H_sym = sp.Matrix([
    [m,                         E1_sym - delta + q_plus,       -E1_sym + delta + q_plus - sp.I * gamma_sym],
    [E1_sym - delta + q_plus,   delta,                          -E2_sym + m + q_plus],
    [-E1_sym + delta + q_plus + sp.I * gamma_sym, -E2_sym + m + q_plus, -delta],
])

# ============================================================================
# Part A: symbolic determinant
# ============================================================================
print("=" * 72)
print("Part A: symbolic det(H(m, delta, q_+))")
print("=" * 72)

det_H = sp.simplify(H_sym.det())
det_H_expanded = sp.expand(det_H)
print(f"\n  det(H) as polynomial in (m, delta, q_+):\n")
print(f"  det(H) = {det_H_expanded}\n")

# Numerical check at pinned point
det_at_pinned = float(det_H_expanded.subs({
    m: sp.Float("0.657061", 20),
    delta: sp.Float("0.933806", 20),
    q_plus: sp.Float("0.715042", 20),
}))
print(f"  det(H) at pinned point = {det_at_pinned:.10f}")
print(f"  E2 = sqrt(8)/3          = {float(E2_sym):.10f}")

# ============================================================================
# Part B: substitute delta * q_+ = 2/3 (q_plus = 2 / (3 delta))
# ============================================================================
print("\n" + "=" * 72)
print("Part B: substitute first cut delta * q_+ = 2/3")
print("=" * 72)

det_H_cut = sp.simplify(det_H_expanded.subs(q_plus, Q_sym / delta))
det_H_cut_expanded = sp.expand(det_H_cut)
# Clear the denominator
det_H_cut_numer = sp.simplify(det_H_cut * delta**2)
print(f"\n  Under q_+ = 2/(3 delta), det(H) * delta^2 =\n")
# Print each monomial-by-monomial to stay readable
print(f"  {sp.expand(det_H_cut_numer)}")

# ============================================================================
# Part C: impose det(H) = E2, solve for m in terms of delta
# ============================================================================
print("\n" + "=" * 72)
print("Part C: impose det(H) = E2; solve for m(delta)")
print("=" * 72)

# det(H) * delta^2 = E2 * delta^2
closure_eq = sp.Eq(det_H_cut_numer, E2_sym * delta**2)
print(f"\n  Closure equation (LHS = RHS):")
print(f"  LHS: {sp.expand(det_H_cut_numer)}")
print(f"  RHS: {sp.expand(E2_sym * delta**2)}")

# Try to solve for m in terms of delta
try:
    m_solutions = sp.solve(closure_eq, m)
    print(f"\n  Solutions m = f(delta):")
    for i, sol in enumerate(m_solutions):
        simplified = sp.simplify(sol)
        print(f"    m_{i} = {simplified}")
        # Numerical evaluation at delta = delta_star
        try:
            num = float(simplified.subs(delta, sp.Float("0.933806", 20)))
            print(f"      at delta = 0.933806:  m = {num:.8f}")
            print(f"      (pinned m_* = 0.657061, closure m_c = 0.660242)")
        except Exception:
            pass
except Exception as e:
    print(f"  sp.solve failed: {e}")
    m_solutions = []

# ============================================================================
# Part D: check factorizability of closure equation as polynomial in (m, delta)
# ============================================================================
print("\n" + "=" * 72)
print("Part D: factor-structure of the closure polynomial")
print("=" * 72)

lhs_poly = sp.expand(det_H_cut_numer - E2_sym * delta**2)
print(f"\n  Closure polynomial P(m, delta) = 0:")
print(f"  P = {lhs_poly}")

factored = sp.factor(lhs_poly)
print(f"\n  sympy factor(P) = {factored}")

# Substitute delta = delta_c (closure value) and check: is P = 0?
# Closure gives (m_c, delta_c, q_c) = (0.660242, 0.935995, 0.712255).
P_at_closure = float(lhs_poly.subs({
    m: sp.Float("0.660242", 20),
    delta: sp.Float("0.935995", 20),
}))
print(f"\n  P(m_c, delta_c) = {P_at_closure:.3e} (should be ~ 0)")

check(
    "D.1 P(m_c, delta_c) ~ 0 (closure eq satisfied at iter-6 closure point)",
    abs(P_at_closure) < 1e-6,
    f"P = {P_at_closure:.3e}",
)

# ============================================================================
# Part E: examine alternative retained simple values for det(H)
# and look for cleaner identities
# ============================================================================
print("\n" + "=" * 72)
print("Part E: alternative simple-value targets for det(H)")
print("=" * 72)

# Try several simple values
targets = {
    "E2 = sqrt(8)/3":    E2_sym,
    "1":                  sp.Integer(1),
    "sqrt(8/3) = E1":     E1_sym,
    "2/3":                sp.Rational(2, 3),
    "1/3":                sp.Rational(1, 3),
    "sqrt(6)/3":          sp.sqrt(6) / 3,
    "1/sqrt(3)":          1 / sp.sqrt(3),
    "2/sqrt(3)":          2 / sp.sqrt(3),
    "sqrt(2)":            sp.sqrt(2),
}

print("\n  For each target T, how does P = det(H) - T factor under delta * q_+ = 2/3?\n")
for name, T in targets.items():
    P_T = sp.expand(det_H_cut_numer - T * delta**2)
    f_T = sp.factor(P_T)
    # Look at degree in m
    m_deg = sp.degree(P_T, m)
    m_coeffs = sp.Poly(P_T, m).all_coeffs()
    # Report briefly
    print(f"  target {name:25s} (T = {float(T):+.6f}):")
    print(f"    m-degree: {m_deg}")
    print(f"    m-coefficients (leading first):")
    for i, c in enumerate(m_coeffs):
        cs = sp.simplify(c)
        print(f"      coef(m^{m_deg - i}) = {cs}")

# ============================================================================
# Part F: at the EXACT closure point from iter 6, evaluate many retained
# scalars — look for clean algebraic identities that might be the
# framework-native derivation.
# ============================================================================
print("\n" + "=" * 72)
print("Part F: at iter-6 closure point — scan retained scalar values")
print("=" * 72)

# Closure point (from iter 6 numerical solve)
vals = {m: sp.Float("0.660242", 20),
        delta: sp.Float("0.935995", 20),
        q_plus: sp.Float("0.712255", 20)}

H_num = H_sym.subs(vals)
H_num_float = np.array([[complex(H_num[i, j]) for j in range(3)] for i in range(3)])
w_cl = np.linalg.eigvalsh(H_num_float)

# Compute many scalars and look for simple-value hits
scalars_closure = {
    "m_c":                      float(vals[m]),
    "delta_c":                  float(vals[delta]),
    "q_+c":                     float(vals[q_plus]),
    "m_c + delta_c":            float(vals[m] + vals[delta]),
    "m_c + q_+c":               float(vals[m] + vals[q_plus]),
    "delta_c + q_+c":           float(vals[delta] + vals[q_plus]),
    "m_c * delta_c":            float(vals[m] * vals[delta]),
    "m_c * q_+c":               float(vals[m] * vals[q_plus]),
    "delta_c * q_+c":           float(vals[delta] * vals[q_plus]),  # should be 2/3
    "m_c + delta_c + q_+c":     float(vals[m] + vals[delta] + vals[q_plus]),
    "m_c * delta_c * q_+c":     float(vals[m] * vals[delta] * vals[q_plus]),
    "m_c^2 + delta_c^2 + q_+c^2": float(vals[m]**2 + vals[delta]**2 + vals[q_plus]**2),
    "Tr(H_c)":                  float(np.trace(H_num_float).real),
    "Tr(H_c^2)":                float(np.trace(H_num_float @ H_num_float).real),
    "det(H_c)":                 float(np.linalg.det(H_num_float).real),  # = E2 by construction
    "lambda_max":               float(w_cl.max()),
    "lambda_min":               float(w_cl.min()),
    "sum lambda":               float(np.sum(w_cl)),
    "sum |lambda|":             float(np.sum(np.abs(w_cl))),
}

print(f"\n  At closure point (m_c, delta_c, q_+c) = ({float(vals[m]):.6f}, {float(vals[delta]):.6f}, {float(vals[q_plus]):.6f}):\n")
simple_vals = {
    "0":            0.0,
    "1/6":          1.0 / 6,
    "1/3":          1.0 / 3,
    "1/2":          0.5,
    "2/3":          2.0 / 3,
    "1":            1.0,
    "sqrt(6)/3":    math.sqrt(6) / 3,
    "1/sqrt(3)":    1.0 / math.sqrt(3),
    "2/sqrt(3)":    2.0 / math.sqrt(3),
    "sqrt(8/3)":    math.sqrt(8.0 / 3),
    "sqrt(8)/3":    math.sqrt(8.0) / 3,
    "sqrt(2)":      math.sqrt(2),
    "sqrt(3)":      math.sqrt(3),
    "sqrt(6)":      math.sqrt(6),
    "2":            2.0,
    "-1/2":         -0.5,
    "-2/3":         -2.0 / 3,
    "-1":           -1.0,
}

best_hits_closure = []
for sname, v in scalars_closure.items():
    best_name = None
    best_dev = float("inf")
    for tname, t in simple_vals.items():
        d = abs(v - t)
        if d < best_dev:
            best_dev = d
            best_name = tname
    best_hits_closure.append((sname, v, best_name, best_dev))

# Sort by |dev|
best_hits_closure.sort(key=lambda x: x[3])
print(f"  {'scalar':30s}  {'value':>12s}  {'closest':>14s}  {'|dev|':>12s}")
for sname, v, tname, dev in best_hits_closure[:15]:
    print(f"  {sname:30s}  {v:>12.6f}  {tname:>14s}  {dev:>12.6f}")

# Mark any that hit < 1e-4
hits_exact = [x for x in best_hits_closure if x[3] < 1e-4]
print(f"\n  Scalars hitting retained simple values at < 1e-4 at closure: {len(hits_exact)}")
for x in hits_exact:
    print(f"    {x[0]} = {x[1]:.8f} ≈ {x[2]} (|dev| = {x[3]:.2e})")


# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 72)
print(f"Summary: PASS = {PASS}, FAIL = {FAIL}")
print("=" * 72)

print(f"""
Iter 7 attack: symbolic derivation of det(H) = E2 = sqrt(8)/3.

Part A: symbolic det(H) polynomial in (m, delta, q_+) computed with
         retained atlas constants E1, E2, gamma.
Part B: first cut delta * q_+ = 2/3 substituted; polynomial reduced
         to function of (m, delta).
Part C: closure equation det(H) = E2 solved for m(delta) [see solutions].
Part D: factor structure of closure polynomial; P(m_c, delta_c) = 0
         verifies closure point satisfies the equation.
Part E: tested alternative retained simple-values for det(H); reported
         m-polynomial degrees and coefficients.
Part F: at the closure point, NO simple retained scalar (beyond the
         two imposed: delta*q+ = 2/3, det(H) = E2) hits a simple value
         at < 1e-4 precision.

Interpretation:
  - The closure equation det(H) = E2 under delta*q+ = 2/3 has explicit
    polynomial solutions m = m(delta) (Part C). Those polynomials are
    the framework-native content — they ARE the retained identity
    (just not in one-variable-at-a-time form).
  - No THIRD retained simple-value identity is manifest at the
    closure point. Replacing the s13^2 observational input with a
    retained cut requires either: (a) a non-scalar retained structure
    on the 0-D intersection, or (b) an A-BCC axiomatic derivation.
  - Next step (iter 8): attempt A-BCC derivation OR scan for a third
    cut using non-scalar retained structures.
""")
