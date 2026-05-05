"""
FINAL VERIFICATION & SUMMARY for V=1 SU(3) Wilson plaquette Picard-Fuchs ODE.

ODE for J(β) = ∫_{SU(3)} exp(β · Re Tr U / 3) dU :

   6 β² J'''(β) + β(60 − β) J''(β) + (−4β² − 2β + 120) J'(β) − β(β + 10) J(β) = 0

Order = 3, polynomial-coefficient degree = 2.
Indicial roots at β=0: ρ ∈ {0, −3, −4}. Regular point at β=0; irregular at β=∞.

⟨P⟩_1(β) = J'(β) / J(β)  (logarithmic derivative).

This script:
  (1) Verifies the ODE by series substitution.
  (2) Integrates numerically from initial conditions and reports ⟨P⟩_1(6).
  (3) Reports the symbolic Frobenius-series solution at β=0.
"""
import numpy as np
import sympy as sp
from sympy import Rational, Symbol, factorial, Poly, simplify, series, Function, dsolve

beta = Symbol('beta')
J = Function('J')

# ODE
ode = (6*beta**2 * J(beta).diff(beta, 3)
       + beta*(60 - beta) * J(beta).diff(beta, 2)
       + (-4*beta**2 - 2*beta + 120) * J(beta).diff(beta)
       + (-beta**2 - 10*beta) * J(beta))
ode_eq = sp.Eq(ode, 0)
print("Picard-Fuchs ODE:")
sp.pprint(ode_eq)
print()

# (1) Verify by Taylor series
# Build truncated J series from Bessel-determinant identity (re-derive for self-containment).
t = Symbol('t')

def I_series(n, order):
    n = abs(n)
    s = sp.S(0)
    for m in range(0, order - n + 1):
        if n + 2*m > order:
            break
        s += (t/2)**(n + 2*m) / (factorial(m) * factorial(n + m))
    return sp.expand(s)

def det3x3(M):
    a,b,c = M[0]; d,e,f = M[1]; g,h,i = M[2]
    return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)

order = 25
J_series_total = sp.S(0)
for k in range(-order, order+1):
    rows = [[I_series(i-j+k, order) for j in range(3)] for i in range(3)]
    d = det3x3(rows)
    d_beta = d.subs(t, beta/sp.S(3))
    J_series_total = sp.expand(J_series_total + d_beta)
J_poly = sp.S(0)
p = sp.Poly(J_series_total, beta)
for monom, c in p.terms():
    if monom[0] <= order:
        J_poly += c * beta**monom[0]
J_poly = sp.expand(J_poly)

ode_residual = (6*beta**2 * sp.diff(J_poly, beta, 3)
                + beta*(60-beta) * sp.diff(J_poly, beta, 2)
                + (-4*beta**2 - 2*beta + 120) * sp.diff(J_poly, beta)
                + (-beta**2 - 10*beta) * J_poly)
# Truncate to degree (order - 1) for fair comparison
res_poly = sp.Poly(sp.expand(ode_residual), beta)
res_low = sp.S(0)
for monom, c in res_poly.terms():
    if monom[0] <= order - 4:
        res_low += c * beta**monom[0]
print(f"ODE residual (truncated to degree {order - 4}):")
print(f"  = {sp.simplify(res_low)}")
print()

# (2) Numerical integration with high-precision initial conditions
import math
print("Numerical solution and verification at β=6:")
J0_at_1 = float(J_poly.subs(beta, 1))
Jp_at_1 = float(sp.diff(J_poly, beta).subs(beta, 1))
Jpp_at_1 = float(sp.diff(J_poly, beta, 2).subs(beta, 1))

from scipy.integrate import solve_ivp
def rhs(b, y):
    J_, Jp_, Jpp_ = y
    Jppp_ = (b*(b-60)*Jpp_ + (4*b*b + 2*b - 120)*Jp_ + b*(b+10)*J_) / (6*b*b)
    return [Jp_, Jpp_, Jppp_]

sol = solve_ivp(rhs, [1.0, 10.0], [J0_at_1, Jp_at_1, Jpp_at_1],
                method='DOP853', rtol=1e-13, atol=1e-15,
                t_eval=[2.0, 4.0, 6.0, 8.0, 10.0])

# Compare with direct Weyl integration
def J_weyl(beta_val, Ng=800):
    th = np.linspace(-np.pi, np.pi, Ng, endpoint=False)
    dth = (2*np.pi)/Ng
    T1, T2 = np.meshgrid(th, th, indexing='ij')
    chi = np.cos(T1) + np.cos(T2) + np.cos(T1+T2)
    a = 2.0*(1.0 - np.cos(T1 - T2))
    b = 2.0*(1.0 - np.cos(2.0*T1 + T2))
    c = 2.0*(1.0 - np.cos(T1 + 2.0*T2))
    measure = a*b*c
    norm = 1.0 / (6.0 * (2.0*np.pi)**2)
    expo = np.exp(beta_val*chi/3.0)
    return (norm * np.sum(measure * expo) * dth*dth,
            norm * np.sum((chi/3.0) * measure * expo) * dth*dth)

print(f"{'beta':>5} {'J_ODE':>16} {'Jp_ODE':>16} {'<P>_1_ODE':>14} {'<P>_1_Weyl':>14}")
for i, b in enumerate(sol.t):
    J_o, Jp_o = sol.y[0,i], sol.y[1,i]
    P_o = Jp_o/J_o
    J_w, Jp_w = J_weyl(b)
    P_w = Jp_w/J_w
    print(f"{b:5.2f} {J_o:16.10e} {Jp_o:16.10e} {P_o:14.10f} {P_w:14.10f}")

# Highlight β=6
J_w, Jp_w = J_weyl(6.0, Ng=1200)
print(f"\n*** ⟨P⟩_1(β=6) = {Jp_w/J_w:.12f} (direct integration, Ng=1200)")

# (3) Symbolic Frobenius solution at β=0 (regular singular point)
print("\nFrobenius solution at β=0 (regular sing. point, indices ρ=0,-3,-4):")
print("  Solution analytic at β=0 is the 'physical' J(β); two singular ones grow as 1/β^3, 1/β^4 near 0.")
print("  Series J(β) = sum_n a_n β^n with a_0=1, a_1=0, a_2=1/36, a_3=1/648, a_4=1/2592, ...")
print("  Recurrence (extracted from ODE on Taylor coefficients):")
# Convert ODE to recurrence on a_n: substitute J = sum a_n β^n.
# Coeff of β^N:
#   6 β² · J''' contributes: a_{N+1} · (N+1)N(N-1) · ?? careful: J''' has powers β^{n-3}, mult by 6β² -> β^{n-1}, so coef of β^N gets a_{N+1} · (N+1)N(N-1) · 6.
#   β(60-β) · J'' = (60β - β²) J'' has β^{n-1} from 60β · J'' (which has β^{n-2}) and β^n from -β² J''.
#       60β·J'' coef β^N: 60 · (N+1)N · a_{N+1}
#       -β²·J'' coef β^N: -(N)(N-1) · a_N
#   (-4β² - 2β + 120) · J'  -> J' has β^{n-1}.
#       -4β² · J' coef β^N: -4 · (N-1) · a_{N-1}    [from a_{N-1}·(N-1)·β^{N-2} · β² ... wait let me redo]
# Cleaner: J' = sum n a_n β^{n-1}. β^j J' has coef of β^N: (N-j+1) a_{N-j+1} for n=N-j+1.
# β^j J'' has coef of β^N: (N-j+2)(N-j+1) a_{N-j+2}.
# β^j J''' has coef of β^N: (N-j+3)(N-j+2)(N-j+1) a_{N-j+3}.
# β^j J has coef of β^N: a_{N-j}.
# Our P_k coefficients (already cleared, integer):
#   P_0(β) = -β² -10β:  j=1 with coef -10, j=2 with coef -1 (multiplying J)
#   P_1(β) = -4β² -2β +120: j=0 coef 120, j=1 coef -2, j=2 coef -4 (multiplying J')
#   P_2(β) = 60β -β²:  j=1 coef 60, j=2 coef -1 (multiplying J'')
#   P_3(β) = 6β²:      j=2 coef 6 (multiplying J''')

# Coef of β^N in ODE = 0:
# from P_0 J: -10 a_{N-1} - a_{N-2}
# from P_1 J': 120 (N+1) a_{N+1} - 2 N a_N - 4 (N-1) a_{N-1}
# from P_2 J'': 60 (N+1) N a_{N+1}  -  (N)(N-1) a_N
# from P_3 J''': 6 (N+1) N (N-1) a_{N+1}

# Sum = 0:
#   a_{N+1} [120(N+1) + 60(N+1)N + 6(N+1)N(N-1)] + a_N [-2N - N(N-1)] + a_{N-1}[-10 - 4(N-1)] + a_{N-2}[-1] = 0
# Simplify a_{N+1} coef:
#   = 6(N+1) [ 20 + 10 N + N(N-1) ]
#   = 6(N+1) [ 20 + 10N + N² - N ]
#   = 6(N+1) [ N² + 9N + 20 ]
#   = 6(N+1)(N+4)(N+5)
# a_N coef: -2N -N² + N = -N² - N = -N(N+1)
# a_{N-1} coef: -10 - 4N + 4 = -4N - 6 = -2(2N+3)
# a_{N-2} coef: -1

print("  6(N+1)(N+4)(N+5) a_{N+1} = N(N+1) a_N + 2(2N+3) a_{N-1} + a_{N-2}")
print()

# Verify recurrence
print("Recurrence verification (with a_0=1, a_1=0, a_2=1/36):")
a = [Rational(1), Rational(0), Rational(1, 36)]  # known
for N in range(2, 12):
    # 6(N+1)(N+4)(N+5) a_{N+1} = N(N+1) a_N + 2(2N+3) a_{N-1} + a_{N-2}
    rhs_val = N*(N+1)*a[N] + 2*(2*N+3)*a[N-1] + (a[N-2] if N>=2 else Rational(0))
    a_next = rhs_val / (6*(N+1)*(N+4)*(N+5))
    a.append(sp.simplify(a_next))
    print(f"  a_{N+1} = {a[-1]}")
