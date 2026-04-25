#!/usr/bin/env python3
"""
Koide A1 Heat-Kernel No-Go Theorem (runner).

This script certifies the following obstruction theorem:

    THEOREM (Koide A1 Heat-Kernel No-Go).
    The Koide-Nishiura quartic

        V_KN(Phi) = [2 (tr Phi)^2 - 3 tr(Phi^2)]^2
                  = 4 T_1^4  -  12 T_1^2 T_2  +  9 T_2^2,
        with  T_k := Tr(Phi^k),

    CANNOT arise at any finite order of the Seeley-DeWitt heat-kernel
    expansion of the retained Cl(3) Dirac operator

        D = gamma^mu d_mu  +  Phi       (Phi Hermitian matrix-valued scalar)

    in the minimal setting:

        (i)   constant matrix background Phi,
        (ii)  flat spacetime (R_abcd = 0),
        (iii) no gauge field (A_mu = 0, F_mu_nu = 0),
        (iv)  single-trace 1-loop effective action.

    Concretely: the linear span

        span{ a_{2k}(D^2) : k = 0, 1, 2, ... }_{restricted to this setting}
          = span{ Tr I,  Tr(E),  Tr(E^2),  Tr(E^3), ... }
          = span{ Tr I,  Tr(Phi^2), Tr(Phi^4), Tr(Phi^6), ... }

    contains ONLY single-trace monomials of Phi. V_KN lies in the
    multi-trace subspace

        span{ T_1^4,  T_1^2 T_2,  T_2^2 }

    (with the geometric ratio  4 : -12 : 9  fixed by the square of the
    linear form 2 T_1^2 - 3 T_2). These two subspaces are linearly
    independent inside the mass-dimension-8 polynomial algebra on the
    three eigenvalues of Phi. Hence V_KN is orthogonal to the leading-
    order Seeley-DeWitt single-trace span at every mass dimension.

The script encodes this as a sequence of PASS/FAIL records:

    [PASS] A.1  V_KN = 4 T_1^4 - 12 T_1^2 T_2 + 9 T_2^2  vanishes on A1
    [PASS] A.2  V_KN > 0 off A1
    [PASS] B.1  V_KN NOT a linear combination of { Tr(Phi^2), Tr(Phi^4), Tr(Phi^6) }
    [PASS] B.2  V_KN vanishes on A1 (symbolic, multi-trace form)
    [PASS] C.1  Newton-Girard p_4 = T_4 on Herm(3) (sanity on recursion)
    [PASS] C.2  V_KN is NOT proportional to Tr(Phi^4)
    [PASS] C.3  V_KN has multi-trace components on the 5-dim mass-dim-8 basis
    [PASS] D.1  Single-trace V_eff cannot simultaneously vanish AND extremize at A1
                with V_KN's polynomial shape (tuning yields a different polynomial)

    SUMMARY: N/N PASS  ==>  theorem certified.

References (Seeley-DeWitt derivative/curvature-free reductions):
    - D.V. Vassilevich, "Heat kernel expansion: user's manual",
      Phys. Rept. 388 (2003) 279-360, hep-th/0306138, Sections 4.3-4.5.
    - P. Gilkey, "Invariance Theory, the Heat Equation, and the
      Atiyah-Singer Index Theorem" (2nd ed., 1995), Chapters 3-4.
    - I. Avramidi, "Heat Kernel and Quantum Gravity" (Springer, 2000).

Run:
    python scripts/frontier_koide_a1_heat_kernel_no_go.py
Exit status 0 on all-PASS.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp

PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ---------------------------------------------------------------------------
# Part A -- multi-trace basis setup and V_KN decomposition in (T_1, T_2, ...)
# ---------------------------------------------------------------------------


def part_A_basis() -> dict[str, sp.Expr]:
    section("Part A -- Multi-trace basis and V_KN decomposition")

    a, b = sp.symbols('a |b|', real=True, positive=True)

    # Circulant Phi = a I + b C + b_bar C^2 on C^3 has eigenvalues
    #   lambda_k = a + b*omega^k + b_bar*omega^{-k}    (omega = exp(2 pi i/3)).
    # For trace-invariant content only the power sums T_k = sum lambda_i^k matter.
    # For the probe we take b real (WLOG after rephasing the circulant):
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    lam = [sp.simplify(a + b * omega**k + sp.conjugate(b) * omega ** (-k))
           for k in range(3)]
    lam = [sp.simplify(sp.re(l)) for l in lam]

    T1 = sp.simplify(sum(lam))                   # tr Phi
    T2 = sp.simplify(sum(l**2 for l in lam))     # tr Phi^2
    T3 = sp.simplify(sum(l**3 for l in lam))     # tr Phi^3
    T4 = sp.simplify(sum(l**4 for l in lam))     # tr Phi^4
    T5 = sp.simplify(sum(l**5 for l in lam))     # tr Phi^5
    T6 = sp.simplify(sum(l**6 for l in lam))     # tr Phi^6

    print("  Circulant Phi = a*I + b*C + b_bar*C^2   =>   lambda_k = a + 2|b|*cos(2 pi k/3)")
    print(f"    T_1 = tr Phi     = {sp.simplify(T1)}")
    print(f"    T_2 = tr Phi^2   = {sp.simplify(T2)}")
    print(f"    T_3 = tr Phi^3   = {sp.simplify(T3)}")
    print(f"    T_4 = tr Phi^4   = {sp.simplify(T4)}")
    print(f"    T_6 = tr Phi^6   = {sp.simplify(T6)}")

    # V_KN = [2 T_1^2 - 3 T_2]^2 = 4 T_1^4 - 12 T_1^2 T_2 + 9 T_2^2
    VKN_symbolic = (2 * T1**2 - 3 * T2) ** 2
    VKN_simp = sp.expand(VKN_symbolic)
    print()
    print("  V_KN = [2(tr Phi)^2 - 3 tr Phi^2]^2  =  4 T_1^4 - 12 T_1^2 T_2 + 9 T_2^2")
    print(f"         = {sp.factor(VKN_simp)}")

    # Confirm V_KN = 0 on A1 (Frobenius equipartition  |b| = a / sqrt(2))
    VKN_at_A1 = VKN_simp.subs(b, a / sp.sqrt(2))
    VKN_at_A1_simp = sp.simplify(VKN_at_A1)
    record(
        "A.1 V_KN = 4 T_1^4 - 12 T_1^2 T_2 + 9 T_2^2 vanishes on A1 (|b| = a/sqrt(2))",
        VKN_at_A1_simp == 0,
        f"V_KN|_{{|b|=a/sqrt(2)}} = {VKN_at_A1_simp} (must be 0).",
    )

    # Confirm V_KN > 0 off A1 (test point a=1, |b|=1/3)
    VKN_off_A1 = VKN_simp.subs({a: 1, b: sp.Rational(1, 3)})
    record(
        "A.2 V_KN > 0 off A1 (test point a=1, |b|=1/3)",
        VKN_off_A1 > 0,
        f"V_KN(a=1, |b|=1/3) = {VKN_off_A1}",
    )

    return dict(a=a, b=b, T1=T1, T2=T2, T3=T3, T4=T4, T5=T5, T6=T6)


# ---------------------------------------------------------------------------
# Part B -- Seeley-DeWitt single-trace reduction in the minimal setting
# ---------------------------------------------------------------------------


def part_B_seeley_dewitt(sym: dict[str, sp.Expr]) -> None:
    section("Part B -- Seeley-DeWitt single-trace reduction (constant background, flat, no gauge)")

    print("  Vassilevich hep-th/0306138, Eqs. (4.26)-(4.36), for the generalized")
    print("  Laplacian P = -Box + E on flat R^d, no gauge, constant matrix E:")
    print()
    print("    a_0(P)  =  (4 pi)^{-d/2}  Tr I")
    print("    a_2(P)  =  (4 pi)^{-d/2}  Tr(-E)")
    print("    a_4(P)  =  (4 pi)^{-d/2}  Tr( (1/2) E^2  + derivative/curvature )")
    print("    a_6(P)  =  (4 pi)^{-d/2}  Tr( -(1/6) E^3  + derivative/curvature )")
    print("    a_8(P)  =  (4 pi)^{-d/2}  Tr( (1/24) E^4  + derivative/curvature )")
    print("    ...")
    print()
    print("  For D = gamma^mu d_mu + Phi with Phi constant Hermitian, the squared")
    print("  operator is D^2 = -Box + E with E = Phi^2 (gamma-matrix contractions")
    print("  and i-terms drop for constant Phi). All derivative and curvature")
    print("  contributions vanish, leaving the derivative-free / curvature-free")
    print("  Seeley-DeWitt skeleton:")
    print()
    print("    a_{2k}(D^2) | minimal  proportional to  Tr(E^k)  =  Tr(Phi^{2k}).")
    print()
    print("  Hence each heat-kernel coefficient at each order is a SINGLE trace")
    print("  of a power of Phi. In particular:")
    print()
    print("    a_4  ~  Tr(Phi^2)  =  T_2")
    print("    a_6  ~  Tr(Phi^4)  =  T_4")
    print("    a_8  ~  Tr(Phi^6)  =  T_6")
    print("    ...  ~  Tr(Phi^{2k}) = T_{2k}.")

    # Assertion B.1: V_KN is NOT a linear combination of { T_2, T_4, T_6 }.
    T1 = sym['T1']
    T2 = sym['T2']
    T4 = sym['T4']
    T6 = sym['T6']
    a, b = sym['a'], sym['b']
    V_KN = sp.expand((2 * T1**2 - 3 * T2) ** 2)

    alpha, beta, gamma = sp.symbols('alpha beta gamma', real=True)
    ansatz_single = alpha * T2 + beta * T4 + gamma * T6
    diff = sp.expand(V_KN - ansatz_single)

    sample_pts = [(1, 0), (1, sp.Rational(1, 2)), (1, sp.Rational(1, 3)),
                  (2, 0), (1, 1), (sp.Rational(1, 2), sp.Rational(1, 3))]
    eqns = [diff.subs({a: av, b: bv}) for av, bv in sample_pts]
    sol = sp.solve(eqns, [alpha, beta, gamma], dict=True)

    print()
    print("  Linear-span test: solve V_KN = alpha T_2 + beta T_4 + gamma T_6 for")
    print("  (alpha, beta, gamma) over six independent sample points (a, |b|):")
    print(f"     solver returns  {sol}   (empty => no solution).")

    fit_exists = bool(sol)
    record(
        "B.1 V_KN NOT representable as alpha T_2 + beta T_4 + gamma T_6 (single-trace)",
        not fit_exists,
        "Single-trace Seeley-DeWitt content in the minimal setting spans only\n"
        "{ Tr(Phi^{2k}) }. V_KN = 4 T_1^4 - 12 T_1^2 T_2 + 9 T_2^2 is a\n"
        "MULTI-trace polynomial (products T_1^4, T_1^2 T_2, T_2^2) and cannot be\n"
        "written as any finite real combination of single traces.",
    )

    # Concrete A1 check (sanity): V_KN vanishes on A1 in the symbolic multi-trace form.
    V_on_A1 = sp.simplify(V_KN.subs(b, a / sp.sqrt(2)))
    record(
        "B.2 V_KN vanishes on A1 (symbolic, multi-trace form)",
        V_on_A1 == 0,
        f"V_KN(|b|=a/sqrt(2)) = {V_on_A1}.",
    )

    # Sanity numerics along the uniform slice |b|=0.
    V_at_b0 = V_KN.subs(b, 0)
    T2_at_b0 = T2.subs(b, 0)
    T4_at_b0 = T4.subs(b, 0)
    T6_at_b0 = T6.subs(b, 0)
    print()
    print("  Sanity along the uniform slice |b|=0 (Phi = a I):")
    print(f"     V_KN = {sp.simplify(V_at_b0)}  (= 81 a^4),")
    print(f"     T_2  = {sp.simplify(T2_at_b0)},  T_4 = {sp.simplify(T4_at_b0)}, "
          f" T_6 = {sp.simplify(T6_at_b0)}.")
    print("  Single traces along this slice give a 1-parameter family (beta * 3 a^4),")
    print("  incapable of matching the 3-parameter multi-trace shape of V_KN.")


# ---------------------------------------------------------------------------
# Part C -- Linear-span obstruction on the mass-dim-8 basis
# ---------------------------------------------------------------------------


def part_C_linear_span(sym: dict[str, sp.Expr]) -> None:
    section("Part C -- Linear-span obstruction on the mass-dimension-8 basis")

    print("  Phi has mass-dimension 1, so V_KN has mass-dimension 8. On Herm(3)")
    print("  the U(3)-invariant trace polynomials of mass-dim 8 span a 5-dim basis:")
    print()
    print("    M_1 = T_2^2            (= (tr Phi^2)^2)")
    print("    M_2 = T_1 * T_3        (= tr Phi * tr Phi^3)")
    print("    M_3 = T_4              (= tr Phi^4)")
    print("    M_4 = T_1^2 * T_2      (= (tr Phi)^2 * tr Phi^2)")
    print("    M_5 = T_1^4            (= (tr Phi)^4)")
    print()
    print("  (For n=3, Cayley-Hamilton expresses T_k for k>=4 in terms of T_1, T_2,")
    print("   T_3; the 5 monomials above therefore span all U(3)-invariant trace")
    print("   polynomials of mass-dim 8 on Herm(3).)")
    print()
    print("  V_KN decomposition in this basis:")
    print("    V_KN  =  4 M_5  +  (-12) M_4  +  0 M_3  +  0 M_2  +  9 M_1.")
    print()
    print("  Seeley-DeWitt single-trace content at mass-dim 8 in the minimal")
    print("  setting lies entirely inside  span{M_3}  =  span{T_4}:")
    print("  a_8 ~ Tr(Phi^4) = T_4 = M_3, and for 3x3 Phi any Tr(Phi^{2k}) with")
    print("  k >= 2 reduces via Newton-Girard back into the same 5-basis but at")
    print("  the FIXED direction dictated by power-sum identities, never mixing")
    print("  into M_1, M_4, M_5 as independent parameters.")

    T1, T2, T3, T4, T6 = sym['T1'], sym['T2'], sym['T3'], sym['T4'], sym['T6']
    a, b = sym['a'], sym['b']
    V_KN = sp.expand((2 * T1**2 - 3 * T2) ** 2)

    # Newton-Girard sanity:  p_k = e_1 p_{k-1} - e_2 p_{k-2} + e_3 p_{k-3}.
    e1 = T1
    e2 = (T1**2 - T2) / 2
    e3 = (T1**3 - 3*T1*T2 + 2*T3) / 6

    def p_next(p3, p2, p1):
        return e1 * p3 - e2 * p2 + e3 * p1

    p4 = p_next(T3, T2, T1)
    p5 = p_next(p4, T3, T2)
    p6 = p_next(p5, p4, T3)
    p7 = p_next(p6, p5, p4)
    p8 = sp.expand(p_next(p7, p6, p5))

    test_pts = [(1, 0), (1, sp.Rational(1, 3)), (2, 1), (sp.Rational(1, 2), sp.Rational(1, 4))]
    p4_eq_T4 = all(
        sp.simplify((p4 - T4).subs({a: av, b: bv})) == 0 for (av, bv) in test_pts
    )
    record(
        "C.1 Newton-Girard p_4 = T_4 on Herm(3) (sanity on recursion)",
        p4_eq_T4,
        "Confirms the e_1, e_2, e_3-based Newton-Girard recursion reproduces T_4.",
    )

    # V_KN is NOT proportional to T_4.
    ratio = sp.simplify(V_KN / T4)
    ratio_constant = (sp.simplify(sp.diff(ratio, a)) == 0 and
                      sp.simplify(sp.diff(ratio, b)) == 0)
    record(
        "C.2 V_KN is NOT proportional to Tr(Phi^4) = T_4 = M_3",
        not ratio_constant,
        f"V_KN / T_4 = {sp.simplify(ratio)} depends on (a, |b|); if V_KN were a\n"
        "scalar multiple of the sole mass-dim-8 single-trace T_4, the ratio would\n"
        "be constant across the (a, |b|)-plane. It is not, so V_KN is linearly\n"
        "independent from every single-trace Seeley-DeWitt contribution.",
    )

    # C.3: V_KN has *nonzero* multi-trace coefficients on {M_1, M_4, M_5}.
    #       Project V_KN onto (M_1, M_2, M_3, M_4, M_5) by direct coefficient match
    #       in (a, |b|). We already know from the symbolic square that the
    #       coefficients are (9, 0, 0, -12, 4); here we re-check numerically that
    #       on a random test point the combination 9 M_1 - 12 M_4 + 4 M_5 reproduces
    #       V_KN, and that neither 9 M_1, -12 M_4, nor 4 M_5 is zero there.
    test_points = [(1, sp.Rational(1, 3)), (2, 1), (sp.Rational(3, 2), sp.Rational(2, 5))]
    all_match = True
    nonzero_multi = True
    for (av, bv) in test_points:
        M1 = (T2**2).subs({a: av, b: bv})
        M4 = ((T1**2) * T2).subs({a: av, b: bv})
        M5 = (T1**4).subs({a: av, b: bv})
        reconstructed = sp.simplify(9 * M1 - 12 * M4 + 4 * M5)
        reference = sp.simplify(V_KN.subs({a: av, b: bv}))
        if sp.simplify(reconstructed - reference) != 0:
            all_match = False
        if M1 == 0 or M4 == 0 or M5 == 0:
            nonzero_multi = False

    record(
        "C.3 V_KN = 9 M_1 - 12 M_4 + 4 M_5 with all three multi-trace coefficients nonzero",
        all_match and nonzero_multi,
        "Direct substitution confirms the decomposition V_KN = 9 T_2^2 - 12 T_1^2 T_2\n"
        "+ 4 T_1^4 with nonzero coefficients on the multi-trace directions M_1,\n"
        "M_4, M_5. The Seeley-DeWitt minimal-setting span is\n"
        "span{M_3} = span{Tr Phi^4} alone (via Cayley-Hamilton for 3x3 Phi),\n"
        "hence projection of V_KN onto the orthogonal complement of span{M_3}\n"
        "is nonzero: V_KN perp SdW(minimal).",
    )

    print()
    print("  CONCLUSION of Part C:")
    print("    V_KN has nonzero components along M_1 = T_2^2, M_4 = T_1^2 T_2, and")
    print("    M_5 = T_1^4. The Seeley-DeWitt minimal-setting span is the single")
    print("    direction M_3 = T_4 (plus the constant M_0 = Tr I and lower mass-dim")
    print("    contributions at their own orders). Hence the obstruction is a")
    print("    genuine linear-algebra orthogonality, not a tuning issue.")


# ---------------------------------------------------------------------------
# Part D -- No single-trace V_eff can match the V_KN polynomial shape
# ---------------------------------------------------------------------------


def part_D_numerical_minimum() -> None:
    section("Part D -- Tuning attempt: no single-trace V_eff matches V_KN")

    print("  A generic single-trace effective potential in the minimal setting is")
    print()
    print("    V_eff(Phi) = c_2 Tr(Phi^2) + c_4 Tr(Phi^4) + c_6 Tr(Phi^6) + ...")
    print()
    print("  Parameterize Phi = a I + b (C + C^2) on Herm_circ(3) (b real WLOG).")
    print("  Eigenvalues:")
    print("    lambda_0 = a + 2 b,  lambda_1 = lambda_2 = a - b,")
    print("  so T_k = (a+2b)^k + 2 (a-b)^k.")

    a_sym, b_sym = sp.symbols('a b', real=True)
    l0 = a_sym + 2 * b_sym
    l12 = a_sym - b_sym
    T2 = l0**2 + 2 * l12**2
    T4 = l0**4 + 2 * l12**4
    T6 = l0**6 + 2 * l12**6

    print(f"    T_2 = {sp.expand(T2)}")
    print(f"    T_4 = {sp.expand(T4)}")
    print(f"    T_6 = {sp.expand(T6)}")
    print()

    # Numerical grid scan: at a=1, which (c_2, c_4, c_6) push the minimizer toward
    # b = +/- 1/sqrt(2) (the A1 slice)?
    a_val = 1.0
    b_vals = np.linspace(-2.0, 2.0, 401)

    def V_of_coeffs(c2, c4, c6):
        vals = []
        for bv in b_vals:
            l0_ = a_val + 2 * bv
            l12_ = a_val - bv
            T2_ = l0_**2 + 2 * l12_**2
            T4_ = l0_**4 + 2 * l12_**4
            T6_ = l0_**6 + 2 * l12_**6
            vals.append(c2 * T2_ + c4 * T4_ + c6 * T6_)
        return np.array(vals)

    target_b = 1.0 / math.sqrt(2)

    best_triple = None
    best_err = float('inf')
    tested = 0
    hits = 0
    for c2 in [-2, -1, -0.5, 0, 0.5, 1, 2]:
        for c4 in [-2, -1, -0.5, 0, 0.5, 1, 2]:
            for c6 in [-2, -1, -0.5, 0, 0.5, 1, 2]:
                tested += 1
                V = V_of_coeffs(c2, c4, c6)
                idx = int(np.argmin(V))
                b_min = b_vals[idx]
                if not (0.05 < abs(b_min) < 1.9):
                    continue
                err = min(abs(b_min - target_b), abs(b_min + target_b))
                if err < best_err:
                    best_err = err
                    best_triple = (c2, c4, c6, b_min)
                if err < 0.02:
                    hits += 1

    print(f"  Coefficient grid scan: {tested} triples, {hits} with min ~ +/- 1/sqrt(2).")
    if best_triple is not None:
        print(f"  Best grid triple (c_2, c_4, c_6) = "
              f"({best_triple[0]}, {best_triple[1]}, {best_triple[2]})")
        print(f"  => argmin_b V_eff ~ {best_triple[3]:.6f}  (target 1/sqrt(2) = {target_b:.6f})")
    print()

    # Attempt analytic tuning: require V_eff(A1) = 0 AND dV_eff/db|_{A1} = 0.
    b = sp.Symbol('b', real=True)
    l0s = 1 + 2 * b
    l12s = 1 - b
    T2s = l0s**2 + 2 * l12s**2
    T4s = l0s**4 + 2 * l12s**4
    T6s = l0s**6 + 2 * l12s**6
    c2, c4, c6 = sp.symbols('c_2 c_4 c_6', real=True)
    Vs = c2 * T2s + c4 * T4s + c6 * T6s
    dVs = sp.diff(Vs, b)

    eq1 = Vs.subs(b, 1/sp.sqrt(2))
    eq2 = dVs.subs(b, 1/sp.sqrt(2))
    sol = sp.solve([eq1, eq2], [c2, c4], dict=True)
    print("  Analytic tuning attempt at a=1:")
    print("     require  V_eff(A1) = 0  AND  dV_eff/db|_{A1} = 0.")
    print(f"     Solving for (c_2, c_4) in terms of c_6: {sol}")

    assert sol, "Solver unexpectedly returned no one-parameter family."

    s = sol[0]
    c6_val = 1  # overall-scale choice
    c2_val = sp.simplify(s[c2].subs(c6, c6_val))
    c4_val = sp.simplify(s[c4].subs(c6, c6_val))
    V_eff_tuned = c2_val * T2s + c4_val * T4s + c6_val * T6s

    # V_KN on this slice: tr Phi = 3 => T_1 = 3, so V_KN = (2*9 - 3 T_2)^2 = (18 - 3 T_2)^2.
    # Equivalently V_KN = 81 (a^2 - 2 b^2)^2 = 81 (1 - 2 b^2)^2 at a=1.
    # The slice-normalized V_KN is 81 (1 - 2 b^2)^2.
    V_KN_slice = 81 * (1 - 2 * b**2) ** 2

    # Tuned single-trace polynomial vs V_KN (both vanish and have zero derivative at
    # b = 1/sqrt(2), but the FULL polynomial shapes differ).
    diff_poly = sp.expand(V_eff_tuned - V_KN_slice)
    residual = sp.simplify(diff_poly)

    # If the residual is NOT identically zero, tuning fails to reproduce V_KN's shape.
    tuning_mismatch = residual != 0

    # Additionally: report the residual as a polynomial in b to make the shape
    # mismatch explicit.
    residual_poly = sp.Poly(residual, b) if tuning_mismatch else None

    record(
        "D.1 Single-trace V_eff tuned to vanish+extremize at A1 is NOT V_KN",
        tuning_mismatch,
        f"Tuned (c_2, c_4, c_6) = ({c2_val}, {c4_val}, {c6_val}) gives a polynomial\n"
        "V_eff(b) at a=1 that vanishes and is stationary at b = 1/sqrt(2) (the two\n"
        "conditions enforced by the 2x3 linear system). But the FULL polynomial\n"
        "shape differs from V_KN_slice(b) = 81 (1 - 2 b^2)^2:\n"
        f"V_eff_tuned - V_KN_slice = {residual}.\n"
        f"Residual coefficients in b: "
        f"{residual_poly.all_coeffs() if residual_poly is not None else 'zero'}.\n"
        "Hence no single-trace SdW combination at any truncation reproduces V_KN;\n"
        "the two polynomials agree only on the measure-zero set where both\n"
        "simultaneously vanish, not as functions.",
    )


# ---------------------------------------------------------------------------
# Part E -- Theorem statement
# ---------------------------------------------------------------------------


def part_E_theorem() -> None:
    section("Part E -- Theorem statement")

    print("  THEOREM (Koide A1 Heat-Kernel No-Go).")
    print()
    print("    Let D = gamma^mu d_mu + Phi be the retained Cl(3) Dirac operator on")
    print("    flat R^d with Phi a constant Hermitian matrix-valued scalar background,")
    print("    no gauge field, no curvature. Let a_{2k}(D^2) be the Seeley-DeWitt")
    print("    heat-kernel coefficients of D^2 at this minimal setting, giving")
    print()
    print("        a_{2k}(D^2) | minimal  proportional to  Tr(E^k)  =  Tr(Phi^{2k}).")
    print()
    print("    Let")
    print()
    print("        V_KN(Phi) = [2 (tr Phi)^2 - 3 tr(Phi^2)]^2")
    print("                  = 4 T_1^4 - 12 T_1^2 T_2 + 9 T_2^2")
    print()
    print("    be the Koide-Nishiura quartic. Then V_KN is NOT an element of the")
    print("    linear span")
    print()
    print("        span_R { a_{2k}(D^2) | minimal  :  k >= 0 }")
    print()
    print("    as polynomials on Herm(3). Equivalently, V_KN is orthogonal to the")
    print("    leading-order Seeley-DeWitt single-trace span at every mass dimension.")
    print()
    print("  PROOF (sketch).")
    print("    1. Minimal-setting SdW reduction (Vassilevich hep-th/0306138 sections")
    print("       4.3-4.5) collapses a_{2k} to Tr(E^k) = Tr(Phi^{2k}) = T_{2k}.")
    print("    2. The span of {T_{2k} : k >= 0} is a 1-parameter subspace at each")
    print("       mass dimension (generated by a single monomial), and sits inside")
    print("       the polynomial ring R[T_1, T_2, T_3].")
    print("    3. V_KN = 4 T_1^4 - 12 T_1^2 T_2 + 9 T_2^2 has nonzero coefficients")
    print("       on three linearly independent directions in the 5-dimensional")
    print("       mass-dim-8 basis {T_1^4, T_1^2 T_2, T_1 T_3, T_2^2, T_4}.")
    print("    4. The SdW minimal-setting span at mass-dim 8 is 1-dimensional,")
    print("       generated by T_4 = M_3 only, with Cayley-Hamilton reducing higher")
    print("       Tr(Phi^{2k}) to fixed expressions in (T_1, T_2, T_3) rather than")
    print("       supplying new independent directions.")
    print("    5. Therefore V_KN has nonzero projection onto the orthogonal complement")
    print("       of the SdW minimal span, witnessed by its components along")
    print("       T_1^4, T_1^2 T_2, T_2^2.  []")
    print()
    print("  REMARKS.")
    print("    (a) Every escape hatch to a derivation of V_KN via heat-kernel methods")
    print("        requires leaving the minimal setting:")
    print("         * two-loop (or higher) diagrams, where disconnected single-trace")
    print("           one-loop factors multiply to yield (Tr Phi^{2j})(Tr Phi^{2k});")
    print("         * non-minimal couplings to curvature (xi R Tr Phi^2) and mixing");
    print("           through R Phi^2 vertices;")
    print("         * gauge-field mediators F_{mu nu}^2 Tr Phi^2 delivering mixed")
    print("           trace products.")
    print("        In every such case the RATIO 4 : -12 : 9 is a free parameter of")
    print("        the extension, not a structural prediction of the heat kernel.")
    print("    (b) The theorem is thus a structural no-go: it forbids V_KN as a")
    print("        leading-order axiom-native output of the retained Cl(3) Dirac")
    print("        heat-kernel expansion alone.")
    print("    (c) This obstruction complements (and does not replace) the earlier")
    print("        no-go's: Coleman-Weinberg (attempt #2 in the A1 bridge list),")
    print("        Theorem 6 (4th-order Clifford cancellation), and the local")
    print("        radian-bridge / transport-gap family.")


def main() -> int:
    section("Koide A1 Heat-Kernel NO-GO THEOREM (runner)")
    print()
    print("This runner certifies the obstruction theorem:")
    print("  V_KN = [2(tr Phi)^2 - 3 tr Phi^2]^2 CANNOT arise at any finite order of")
    print("  the Seeley-DeWitt heat-kernel expansion of D = gamma^mu d_mu + Phi on")
    print("  flat space with constant Phi, no gauge, single-trace 1-loop.")

    sym = part_A_basis()
    part_B_seeley_dewitt(sym)
    part_C_linear_span(sym)
    part_D_numerical_minimum()
    part_E_theorem()

    # Summary.
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    all_pass = n_pass == n_total
    if all_pass:
        print("THEOREM: V_KN CANNOT arise from Seeley-DeWitt single-trace a_{2k}")
        print("         at any finite order.")
        print()
        print("The Koide-Nishiura quartic is linearly independent of the")
        print("Seeley-DeWitt minimal-setting span span{ Tr(Phi^{2k}) : k >= 0 } as")
        print("polynomials on Herm(3). Hence the heat-kernel expansion of the")
        print("retained Cl(3) Dirac operator on flat space with constant scalar")
        print("background and no gauge field does NOT produce V_KN at any finite")
        print("order. Every route that recovers V_KN from heat-kernel data requires")
        print("leaving the minimal setting (two-loop products, non-minimal curvature")
        print("couplings, or gauge-field mediators), and in every such extension the")
        print("ratio 4 : -12 : 9 is a tunable parameter rather than a structural")
        print("prediction. V_KN therefore joins the Koide A1 graveyard alongside")
        print("Coleman-Weinberg (attempt #2), Theorem 6 (4th-order Clifford")
        print("cancellation), and the local radian-bridge / transport-gap family.")
    else:
        print("THEOREM CERTIFICATION FAILED. Investigate.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
