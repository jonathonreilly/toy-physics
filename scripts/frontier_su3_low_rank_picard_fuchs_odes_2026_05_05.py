"""
Part A: Derive Picard-Fuchs ODEs for c_(p,q)(beta) for low-rank SU(3) irreps.

Method (creative-telescoping by ansatz):

  1. Construct the Bessel-determinant series for c_(p,q)(beta) as a high-order
     Taylor expansion in beta (rational coefficients).
  2. For each candidate (order r, polynomial-coefficient degree d), assemble
     the linear ansatz:
         sum_(k=0..r) P_k(beta) c^(k)(beta) = 0
     where P_k(beta) = sum_(m=0..d) p_(k,m) beta^m, and the unknowns are
     {p_(k,m)}.
  3. Match Taylor coefficients of beta -> 0 in the ansatz; this gives a
     linear system on {p_(k,m)} over Q.
  4. Find the smallest (r,d) for which a non-trivial null vector exists,
     pick a primitive integer normalization, and verify by:
       (i) substituting back into more series coefficients than were used to
           solve;
       (ii) numerically integrating the ODE from beta=1 initial conditions
           against the Bessel-determinant numerical c_(p,q)(beta) at
           several beta values.

Saves ODE coefficient lists per rep to outputs/su3_low_rank_pf_odes_2026_05_05.json.
"""

import json
import numpy as np
import sympy as sp
from sympy import Rational, Symbol, Poly, factorial, simplify
from scipy.integrate import solve_ivp
from scipy.special import iv

beta = Symbol('beta')
t = Symbol('t')


# ---------- Modified Bessel I_n(t) Taylor series ----------
def I_series(n, order):
    """ I_n(t) Taylor series up to t^order, as sympy poly in t. """
    n = abs(n)
    s = sp.S(0)
    for m in range(0, order - n + 1):
        if n + 2*m > order:
            break
        s += (t/2)**(n + 2*m) / (factorial(m) * factorial(n + m))
    return sp.expand(s)


def det3(M):
    a,b,c = M[0]; d,e,f = M[1]; g,h,i = M[2]
    return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)


def c_pq_taylor(p, q, order):
    """Build c_(p,q)(beta) Taylor series in beta to given order, in Q[beta]."""
    lam = [p+q, q, 0]
    # number of modes contributing within Taylor order: bounded by order itself.
    # det entry has minimum index |n + lam_j + i - j|; smallest power of t is
    # at least that. So we need only n with |n + lam_j + i - j| <= order/2 ish.
    # Use mode_max = order//2 + 5 for safety.
    mode_max = order
    Jt = sp.S(0)
    for n in range(-mode_max, mode_max+1):
        rows = [[I_series(n + lam[j] + i - j, order) for j in range(3)]
                for i in range(3)]
        d = det3(rows)
        Jt = sp.expand(Jt + d)
    # substitute t = beta/3
    Jb = sp.expand(Jt.subs(t, beta/sp.S(3)))
    # truncate to deg <= order
    pp = Poly(Jb, beta)
    out = sp.S(0)
    for monom, c in pp.terms():
        if monom[0] <= order:
            out += c * beta**monom[0]
    return sp.expand(out)


def derivs(f, k):
    """Return list of [f, f', ..., f^(k)] in beta."""
    out = [f]
    for _ in range(k):
        out.append(sp.expand(sp.diff(out[-1], beta)))
    return out


def find_pf_ode(c_taylor, order, max_r=4, max_d=4, equations_extra=20):
    """
    Find smallest holonomic ODE: sum_k P_k(beta) c^(k) = 0 with deg P_k <= max_d.
    Returns (r_found, d_found, [P_0(beta),..., P_r(beta)]) primitive integer
    normalization.
    """
    p_taylor = Poly(c_taylor, beta)
    # available Taylor coefficients
    coeffs = [Rational(p_taylor.nth(i)) for i in range(order+1)]

    for r in range(1, max_r+1):
        # derivatives' Taylor coefficients
        ds = [coeffs]  # c
        for k in range(1, r+1):
            prev = ds[-1]
            new = [Rational(0)] * (order+1)
            for i in range(order):
                new[i] = (i+1) * prev[i+1]
            ds.append(new)
        for d in range(0, max_d+1):
            # ansatz unknowns: p_{k,m} for k=0..r, m=0..d  --> (r+1)*(d+1) total
            num_unknowns = (r+1) * (d+1)
            # equations: coefficient of beta^N in sum_k (sum_m p_{k,m} beta^m) c^{(k)}(beta) = 0
            # For N from 0 to (order - r - 1) but safer: from 0 to (order - max_d - r)
            N_max = order - r - max_d - 1  # leave margin
            if N_max < num_unknowns:
                continue
            rows = []
            for N in range(N_max+1):
                row = []
                for k in range(r+1):
                    for m in range(d+1):
                        # coefficient of beta^N in beta^m * c^(k) = c^(k)[N-m] for N >= m
                        if N - m >= 0 and N - m < len(ds[k]):
                            row.append(ds[k][N-m])
                        else:
                            row.append(Rational(0))
                rows.append(row)
            # solve sympy nullspace
            M = sp.Matrix(rows)
            ns = M.nullspace()
            if not ns:
                continue
            # found at least one nontrivial relation; pick the first
            v = ns[0]
            # rebuild polynomials P_k
            P = []
            for k in range(r+1):
                P_k = sp.S(0)
                for m in range(d+1):
                    idx = k*(d+1) + m
                    P_k += v[idx] * beta**m
                P.append(sp.expand(P_k))
            # primitive integer normalization
            # multiply through by lcm of denominators, then divide by gcd of int coeffs
            from sympy import lcm, gcd
            all_coeffs = []
            for Pk in P:
                pp = Poly(Pk, beta)
                for _, c in pp.terms():
                    all_coeffs.append(sp.Rational(c))
            denoms = [c.q for c in all_coeffs]
            L = denoms[0]
            for dd in denoms[1:]:
                L = lcm(L, dd)
            P = [sp.expand(L * Pk) for Pk in P]
            # gcd of integer coeffs
            ints = []
            for Pk in P:
                pp = Poly(Pk, beta)
                for _, c in pp.terms():
                    ints.append(int(c))
            g = ints[0]
            for ii in ints[1:]:
                g = gcd(g, ii)
            if g == 0: g = 1
            P = [sp.expand(Pk / g) for Pk in P]
            # leading sign positive
            r_lead = Poly(P[r], beta)
            if r_lead.LC() < 0:
                P = [sp.expand(-Pk) for Pk in P]
            # verify on extra Taylor coefficients
            verify_ok = True
            for N in range(N_max+1, min(order - r, N_max+1+equations_extra)):
                tot = Rational(0)
                for k in range(r+1):
                    pk = Poly(P[k], beta)
                    for m, cval in pk.all_terms():
                        # m is a tuple; sympy convention
                        mm = m[0] if isinstance(m, tuple) else m
                        if N - mm >= 0 and N - mm < len(ds[k]):
                            tot += cval * ds[k][N-mm]
                if tot != 0:
                    verify_ok = False
                    break
            if not verify_ok:
                continue
            return (r, d, P)
    return None


# ---------- Numerical verification ----------

def c_pq_numeric(p, q, beta_val, mode_max=160):
    arg = beta_val / 3.0
    lam = [p+q, q, 0]
    total = 0.0
    for n in range(-mode_max, mode_max+1):
        M = np.array([[iv(n + lam[j] + i - j, arg) for j in range(3)] for i in range(3)])
        total += float(np.linalg.det(M))
    return total


def numerically_verify_ode(P_polys, p, q, beta_targets):
    """Integrate the ODE forward from beta=1 with initial conds from c_pq_numeric,
    compare at beta_targets to direct Bessel-det numerics. Returns max absolute error."""
    r = len(P_polys) - 1
    # express ODE: P_r(b) c^(r) = -P_{r-1} c^(r-1) - ... - P_0 c
    Pl = [sp.lambdify(beta, P_polys[k], 'numpy') for k in range(r+1)]
    # Initial conditions at beta=1 via a small finite-difference Bessel computation:
    # c, c', c'', ..., c^(r-1) at beta=1.
    # Use central FD of order O(h^4) on c_pq_numeric.
    def num_deriv(p, q, b0, k, h=1e-3, mode_max=160):
        # k-th derivative via FD coefs (5-point, 7-point depending on k)
        if k == 0:
            return c_pq_numeric(p, q, b0, mode_max)
        elif k == 1:
            return (-c_pq_numeric(p,q,b0+2*h,mode_max) + 8*c_pq_numeric(p,q,b0+h,mode_max)
                    - 8*c_pq_numeric(p,q,b0-h,mode_max) + c_pq_numeric(p,q,b0-2*h,mode_max))/(12*h)
        elif k == 2:
            return (-c_pq_numeric(p,q,b0+2*h,mode_max) + 16*c_pq_numeric(p,q,b0+h,mode_max)
                    - 30*c_pq_numeric(p,q,b0,mode_max) + 16*c_pq_numeric(p,q,b0-h,mode_max)
                    - c_pq_numeric(p,q,b0-2*h,mode_max))/(12*h*h)
        elif k == 3:
            return (-c_pq_numeric(p,q,b0+3*h,mode_max) + 8*c_pq_numeric(p,q,b0+2*h,mode_max)
                    - 13*c_pq_numeric(p,q,b0+h,mode_max) + 13*c_pq_numeric(p,q,b0-h,mode_max)
                    - 8*c_pq_numeric(p,q,b0-2*h,mode_max) + c_pq_numeric(p,q,b0-3*h,mode_max))/(8*h**3)
        else:
            raise NotImplementedError(f"order {k}")
    b0 = 1.0
    y0 = [num_deriv(p, q, b0, k) for k in range(r)]
    def rhs(b, y):
        # y = [c, c', ..., c^(r-1)]; compute c^(r)
        coeffs = [Pl[k](b) for k in range(r+1)]
        # cr*c^(r) = -sum_{k<r} c_k c^(k)
        rhs_val = -sum(coeffs[k]*y[k] for k in range(r))
        cr = coeffs[r]
        ddt = list(y[1:]) + [rhs_val/cr]
        return ddt
    max_err = 0.0
    sol = solve_ivp(rhs, [b0, max(beta_targets)+0.1], y0,
                    t_eval=beta_targets, method='DOP853', rtol=1e-12, atol=1e-14)
    for i, b in enumerate(sol.t):
        c_ode = sol.y[0,i]
        c_true = c_pq_numeric(p, q, b)
        err = abs(c_ode - c_true) / max(abs(c_true), 1e-20)
        max_err = max(max_err, err)
    return max_err


# ---------- Main ----------

def format_poly(P, beta):
    return sp.expand(P)


def main():
    reps = [(0,0), (1,0), (1,1), (2,0), (2,1), (2,2), (3,0)]
    # (0,1)=(1,0)*, (1,2)=(2,1)*, (0,2)=(2,0)*, (0,3)=(3,0)*: all conjugates equal
    # by chi_(p,q)* = chi_(q,p) and reality of beta·ReTrU/3.

    order = 50
    results = {}
    for (p, q) in reps:
        print(f"\n--- Deriving PF ODE for c_({p},{q})(beta) ---")
        c = c_pq_taylor(p, q, order)
        print(f"  Taylor leading: {sp.series(c, beta, 0, 6).removeO()}")
        out = find_pf_ode(c, order, max_r=6, max_d=8)
        if out is None:
            print(f"  NO ODE FOUND with r<=4, d<=4 at order {order}")
            continue
        r, d, P = out
        print(f"  Found: order r = {r}, polynomial degree d <= {d}")
        for k in range(r+1):
            print(f"    P_{k}(beta) = {sp.expand(P[k])}")
        # Numerical verification
        try:
            err = numerically_verify_ode(P, p, q, [2.0, 4.0, 6.0, 8.0])
            print(f"  Max relative error vs Bessel-det numerics on [1,8]: {err:.3e}")
        except Exception as e:
            print(f"  Numerical verification failed: {e}")
            err = None
        results[f"({p},{q})"] = {
            "order": r,
            "max_poly_deg": d,
            "P_polys": [str(sp.expand(Pk)) for Pk in P],
            "verify_max_rel_err": err
        }
    import os
    out_path = os.path.join("outputs", "su3_low_rank_pf_odes_2026_05_05.json")
    os.makedirs("outputs", exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
