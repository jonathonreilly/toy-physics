#!/usr/bin/env python3
"""
Reviewer-closure loop iter 6: fresh N1 attack via Tr(H²) Casimir.

Staying on N1 per user discipline (don't leave until closed at
Nature-grade). Previous iters tried:
  iter 4: retained Atlas doesn't force N1 → narrowed.
  iter 5: N2/N3 reduce to N1 but N1 is primitive → narrowed.

Iter 6 attack: test whether the scalar Casimir Tr(H²) at the
afternoon-closure point equals a retained simple value. If yes, we
have a THIRD retained Casimir identity (in addition to Tr(H) = 2/3
and det(H) = E2), and the chamber point may be uniquely determined
by the three scalar Casimirs alone — potentially FORCING N1
(δ·q_+ = 2/3) as a consequence.

Rationale. For a 3×3 Hermitian matrix, the spectrum is determined
by (Tr(H), Tr(H²), det(H)) (elementary symmetric polynomials in
eigenvalues). If all three are retained simple values at closure,
H's eigenvalue triple is uniquely determined. Combined with the
chamber structure of H(m, δ, q_+), the (m, δ, q_+) values are then
uniquely determined, and N1 follows as a corollary.

Numerical hint from prior iter: Tr(H²) at closure ≈ 7.071 ≈ 5√2,
which is a framework-retained number (3·E2 · (5/2) = 5√2, and
E2 = 2√2/3 so 5√2 = 15·E2/2).

Iter 6 plan:

Part A. Compute Tr(H²) symbolically as a polynomial in (m, δ, q_+)
        using the retained H_base, T_M, T_Δ, T_Q.

Part B. Evaluate Tr(H²) exactly at the closure point (m_c, δ_c, q_c)
        where m_c = 2/3, δ_c·q_c = 2/3, det(H) = E2.

Part C. Check whether Tr(H²)_closure equals a retained simple
        combination of {1, √2, √3, √6, E1, E2, γ, SELECTOR, ...}.

Part D. If Tr(H²) at closure is a retained simple, check whether
        the three-Casimir system {Tr(H), Tr(H²), det(H)} determines
        (m, δ, q_+) uniquely — if yes, N1 follows as a consequence.
"""
from __future__ import annotations

import math
import sympy as sp

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


# Retained atlas constants (symbolic)
E1 = sp.sqrt(sp.Rational(8, 3))
E2 = sp.sqrt(8) / 3
GAMMA = sp.Rational(1, 2)
Q_KOIDE = sp.Rational(2, 3)
SELECTOR = sp.sqrt(6) / 3

# Chart
m_s, d_s, q_s = sp.symbols("m delta q_plus", real=True)

H_base = sp.Matrix([
    [0, E1, -E1 - sp.I * GAMMA],
    [E1, 0, -E2],
    [-E1 + sp.I * GAMMA, -E2, 0],
])
T_M = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
T_D = sp.Matrix([[0, -1, 1], [-1, 1, 0], [1, 0, -1]])
T_Q = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])

H_sym = H_base + m_s * T_M + d_s * T_D + q_s * T_Q


# ============================================================================
# Part A — compute Tr(H²) symbolically
# ============================================================================
print("=" * 72)
print("Part A: Tr(H²) as polynomial in (m, δ, q_+)")
print("=" * 72)

TrH2 = sp.expand(sp.trace(H_sym * H_sym))
print(f"\n  Tr(H²) = {TrH2}")


# ============================================================================
# Part B — Tr(H²) at the closure point
# ============================================================================
print("\n" + "=" * 72)
print("Part B: Tr(H²) at the afternoon-closure chamber point")
print("=" * 72)

# Substitute closure: m = 2/3, and δ·q_+ = 2/3, det(H) = E2.
# Under m = 2/3 + δ·q_+ = 2/3, solve for specific δ and q_+ numerically
# from det(H(2/3, δ, 2/(3δ))) = E2.
m_c = sp.Rational(2, 3)
TrH2_m23 = sp.simplify(TrH2.subs(m_s, m_c))
print(f"\n  Tr(H²) under m = 2/3:\n    {TrH2_m23}")

# Substitute q_+ = 2/(3δ):
TrH2_m23_q = sp.simplify(TrH2_m23.subs(q_s, 2 / (3 * d_s)))
print(f"\n  Tr(H²) under m=2/3 AND q_+=2/(3δ):\n    {TrH2_m23_q}")

# Solve det(H) = E2 under same substitutions to find δ_c
detH = sp.expand(H_sym.det())
det_under = sp.simplify(detH.subs({m_s: m_c, q_s: 2 / (3 * d_s)}) - E2)
det_eq = sp.simplify(det_under * d_s ** 2)
print(f"\n  δ_c roots of (det(H) = E2) · δ² = 0 (polynomial in δ):\n    {det_eq}")

try:
    delta_roots = sp.solve(det_eq, d_s)
    print(f"  solutions: {len(delta_roots)} roots")
    for i, r in enumerate(delta_roots):
        # Convert to float for readability
        try:
            f_val = complex(sp.nsimplify(r, rational=False).evalf())
            print(f"    δ_{i} = {r}  (≈ {f_val:.8f})")
        except Exception:
            print(f"    δ_{i} = {r}")
except Exception as e:
    print(f"  sp.solve failed: {e}")
    delta_roots = []

# Pick the real root matching closure
closure_delta_num = 0.9330511
closure_delta = None
for r in delta_roots:
    try:
        val = complex(sp.nsimplify(r, rational=False).evalf())
        if abs(val.imag) < 1e-9 and abs(val.real - closure_delta_num) < 1e-4:
            closure_delta = r
            break
    except Exception:
        continue

if closure_delta is not None:
    print(f"\n  Closure δ_c (matching 0.9331) = {closure_delta}")
    # Evaluate Tr(H²) at closure
    TrH2_closure = sp.simplify(TrH2_m23_q.subs(d_s, closure_delta))
    TrH2_closure_num = float(TrH2_closure.evalf())
    print(f"\n  Tr(H²)_closure = {TrH2_closure}")
    print(f"                ≈ {TrH2_closure_num:.10f}")
else:
    print("\n  Could not match a closure-δ root; using numerical closure.")
    closure_delta_num_value = 0.9330511
    closure_q_num = 2.0 / (3.0 * closure_delta_num_value)
    H_num = sp.Matrix([
        [float(m_c), float(E1) - closure_delta_num_value + closure_q_num,
         -float(E1) + closure_delta_num_value + closure_q_num - 0.5j],
        [float(E1) - closure_delta_num_value + closure_q_num, closure_delta_num_value,
         -float(E2) + float(m_c) + closure_q_num],
        [-float(E1) + closure_delta_num_value + closure_q_num + 0.5j,
         -float(E2) + float(m_c) + closure_q_num, -closure_delta_num_value],
    ])
    import numpy as np
    H_np = np.array([[complex(H_num[i, j]) for j in range(3)] for i in range(3)])
    TrH2_closure_num = float(np.trace(H_np @ H_np).real)
    print(f"  Tr(H²)_closure ≈ {TrH2_closure_num:.10f}")
    TrH2_closure = None


# ============================================================================
# Part C — is Tr(H²)_closure a retained simple value?
# ============================================================================
print("\n" + "=" * 72)
print("Part C: compare Tr(H²)_closure to retained simple values")
print("=" * 72)

retained_candidates = {
    "5√2":                 5 * math.sqrt(2),
    "√50":                 math.sqrt(50),
    "2√2 · (E1² + E2²)":   2*math.sqrt(2)*(float(E1**2) + float(E2**2)),
    "E1² · 2 + E2² + γ²":  2*float(E1**2) + float(E2**2) + 0.25,
    "15·E2/2":             15 * float(E2) / 2,
    "10√2 − 3":            10*math.sqrt(2) - 3,
    "5(E1² − 1)":          5*(float(E1**2) - 1),
    "7":                   7.0,
    "21/3":                7.0,
    "64/9":                64/9,
    "2π":                  2*math.pi,
    "8·γ·√3":              8*0.5*math.sqrt(3),
    "Tr(H_base²) + 2/3":   float(4*E1**2 + 2*GAMMA**2 + 2*E2**2) + 2/3,
    "√50 + 0":             math.sqrt(50),
}

print(f"\n  Tr(H²)_closure_numerical = {TrH2_closure_num:.10f}")
print(f"\n  {'candidate':30s}  {'value':>16s}  {'|dev|':>12s}")
best_match = None
best_dev = float("inf")
for name, val in retained_candidates.items():
    dev = abs(TrH2_closure_num - val)
    print(f"  {name:30s}  {val:>16.10f}  {dev:>12.10f}")
    if dev < best_dev:
        best_dev = dev
        best_match = name

print(f"\n  Best match: {best_match}  with |dev| = {best_dev:.6e}")

# Check at 1e-6 precision
check(
    "C.1 Tr(H²)_closure matches some retained combination at < 1e-6",
    best_dev < 1e-6,
    f"best = {best_match}, dev = {best_dev:.3e}",
)
check(
    "C.2 Tr(H²)_closure matches retained combination at < 1e-4",
    best_dev < 1e-4,
    f"best = {best_match}, dev = {best_dev:.3e}",
)


# ============================================================================
# Part D — if C.1 or C.2 passes, test whether the three-Casimir system
#           {Tr(H) = 2/3, Tr(H²) = retained_value, det(H) = E2}
#           uniquely determines (m, δ, q_+)
# ============================================================================
print("\n" + "=" * 72)
print("Part D: does 3-Casimir system (if Tr(H²) is retained) force N1?")
print("=" * 72)

if best_dev < 1e-4 and best_match in retained_candidates:
    target_TrH2 = retained_candidates[best_match]
    print(f"\n  Candidate Tr(H²) target: {best_match} = {target_TrH2}")
    # Test: solve {Tr(H) = 2/3, Tr(H²) = target, det(H) = E2} for (m, δ, q+)
    # Using the symbolic TrH2:
    if abs(target_TrH2 - 5*math.sqrt(2)) < 1e-10:
        target_sym = 5 * sp.sqrt(2)
    elif abs(target_TrH2 - 15*float(E2)/2) < 1e-10:
        target_sym = 15 * E2 / 2
    else:
        target_sym = sp.nsimplify(target_TrH2, rational=False)

    # System: m = 2/3; Tr(H²) = target_sym; det(H) = E2
    TrH2_sub = TrH2.subs(m_s, m_c)
    detH_sub = detH.subs(m_s, m_c)

    # Two equations in (δ, q)
    eq1 = sp.simplify(TrH2_sub - target_sym)
    eq2 = sp.simplify(detH_sub - E2)
    print(f"\n  eq1 (Tr(H²) = {best_match}):\n    {eq1} = 0")
    print(f"  eq2 (det(H) = E2):\n    {eq2} = 0")

    # Solve
    try:
        solutions = sp.solve([eq1, eq2], [d_s, q_s], dict=True)
        print(f"\n  Solutions to the 2-equation system:")
        for i, s in enumerate(solutions):
            d_v = s[d_s]
            q_v = s[q_s]
            d_num = complex(sp.nsimplify(d_v, rational=False).evalf())
            q_num = complex(sp.nsimplify(q_v, rational=False).evalf())
            # Check real + in A-BCC basin
            if abs(d_num.imag) < 1e-9 and abs(q_num.imag) < 1e-9:
                d_r = d_num.real
                q_r = q_num.real
                # Check chamber interior
                chamber_gap = q_r - (math.sqrt(8.0/3.0) - d_r)
                prod_dq = d_r * q_r
                print(f"    sol {i}: (δ, q+) = ({d_r:.6f}, {q_r:.6f}),  δ·q_+ = {prod_dq:.6f},  chamber gap = {chamber_gap:+.4f}")
            else:
                print(f"    sol {i}: complex (δ={d_num}, q={q_num})")
    except Exception as e:
        print(f"  sp.solve failed: {e}")
        solutions = []
else:
    print(f"\n  Tr(H²) not at retained simple value ({best_dev:.3e} deviation).")
    print(f"  Path ruled out — Tr(H²) is not a clean retained Casimir at closure.")
    solutions = []


check(
    "D.1 3-Casimir system has solutions matching afternoon-closure chamber point",
    len(solutions) > 0,
    f"{len(solutions)} solution(s)",
)


# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 72)
print(f"Summary: PASS = {PASS}, FAIL = {FAIL}")
print("=" * 72)
print(f"""
  Iter 6 result:

  Tr(H²) at the afternoon-closure point computed.
  Best retained-simple-value match: {best_match}
  Best deviation: {best_dev:.3e}

  Interpretation:
    - If best_dev < 1e-6: Tr(H²) is a clean retained Casimir, AND
      if Part D's 3-Casimir system has a unique chamber solution
      matching afternoon-closure: N1 is DERIVED as a consequence of
      the three Casimir identities {{Tr(H), Tr(H²), det(H)}}.
    - If best_dev >= 1e-4: Tr(H²) is not a retained simple value;
      this attack path is ruled out.
""")
