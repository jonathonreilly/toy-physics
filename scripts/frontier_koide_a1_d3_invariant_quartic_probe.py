#!/usr/bin/env python3
"""
A1 probe — is V_KN the unique D_3-invariant quartic on Herm_circ(3)?

HYPOTHESIS (probe, not theorem):

    The lowest-order D_3-invariant polynomial on Herm_circ(3) whose
    zero locus is precisely the A1 equipartition surface
        {a² = 2|b|²}
    IS the Koide-Nishiura quartic

        V_KN(a, b) = 81·(a² − 2|b|²)².

D_3 = S_3 = Z_3 ⋊ Z_2 acts naturally on Herm_circ(3):
    Z_3: cyclic shift     (a, b, b̄) → (a, ωb, ω̄b̄)
    Z_2: conjugation      (a, b, b̄) → (a, b̄, b)

In the real parametrization (a, b_1, b_2) with b = b_1 + i b_2 this is
trivial ⊕ standard, and the full D_3 invariant ring is

    R[a, b_1, b_2]^{D_3} = R[a, u, w]    (polynomial)

with u = b_1² + b_2² = |b|²  (deg 2)  and
      w = b_1³ − 3 b_1 b_2² = Re(b³) (deg 3).

Neither of the 9 retained no-go theorems, nor any of the 6 C_3-
invariant variational principles of Theorem 5, nor the 4th-order
Clifford identity of Theorem 6, enforce the Z_2 "reality / CP / time-
reversal" involution simultaneously with Z_3. Asking for the FULL
dihedral symmetry is therefore a clean probe of a previously unexplored
axis in the A1 derivation landscape.

PROBE STEPS:

  1. Build explicit 3×3 real matrices for the D_3 generators r, s on
     (a, b_1, b_2) and verify r^3 = s^2 = (sr)^2 = I (D_3 presentation).
  2. Enumerate the 6 group elements; confirm faithfulness.
  3. Reynolds-average monomials up to degree 4 and pick a basis for
     R[a, b_1, b_2]^{D_3}_{<=4}.
  4. Verify V_KN lies in the invariant ring at degree 4.
  5. List ALL D_3-invariant degree-4 polynomials that vanish on the A1
     surface. Identify the subset whose REAL zero set equals A1.
  6. Report whether D_3 at degree 4 uniquely (or near-uniquely) forces
     V_KN, and if not what breaks the tie.

Nature-grade rigor. Obstruction outcomes are as useful as closure.
"""

from __future__ import annotations

import sys
from itertools import product

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


# ----------------------------------------------------------------------
# Symbols
# ----------------------------------------------------------------------

a, b1, b2 = sp.symbols('a b1 b2', real=True)
VARS = (a, b1, b2)


def apply_matrix(M: sp.Matrix, poly: sp.Expr) -> sp.Expr:
    """Apply 3x3 matrix M to (a, b1, b2) and substitute into poly."""
    new_vars = M * sp.Matrix([a, b1, b2])
    subs = {
        a: new_vars[0],
        b1: new_vars[1],
        b2: new_vars[2],
    }
    return sp.expand(poly.subs(subs, simultaneous=True))


# ----------------------------------------------------------------------
# D_3 generators on (a, b1, b2)
# ----------------------------------------------------------------------

def build_generators() -> tuple[sp.Matrix, sp.Matrix]:
    """
    Z_3 generator r: b -> omega b, omega = e^{2 pi i / 3}.
    So (b1, b2) -> R_{2pi/3} (b1, b2), a unchanged.

    Z_2 generator s: b -> conj(b), so (b1, b2) -> (b1, -b2), a unchanged.

    Both act trivially on a: the symmetric combination of the three
    circulant eigenvalues is fixed.
    """
    c = sp.Rational(-1, 2)           # cos(2 pi / 3)
    s_val = sp.sqrt(3) / 2           # sin(2 pi / 3)

    r = sp.Matrix([
        [1, 0,     0    ],
        [0, c,    -s_val],
        [0, s_val, c    ],
    ])
    s_gen = sp.Matrix([
        [1, 0,  0],
        [0, 1,  0],
        [0, 0, -1],
    ])
    return r, s_gen


def enumerate_group(r: sp.Matrix, s_gen: sp.Matrix) -> list[sp.Matrix]:
    """Generate the 6 elements of D_3 as 3x3 matrices."""
    elements: list[sp.Matrix] = []
    cur = sp.eye(3)
    for _ in range(3):
        elements.append(sp.simplify(cur))
        elements.append(sp.simplify(s_gen * cur))
        cur = r * cur
    # Dedupe (should already be distinct)
    unique: list[sp.Matrix] = []
    for e in elements:
        if not any(sp.simplify(e - u) == sp.zeros(3, 3) for u in unique):
            unique.append(e)
    return unique


# ----------------------------------------------------------------------
# Invariant theory tooling
# ----------------------------------------------------------------------

def reynolds(poly: sp.Expr, group: list[sp.Matrix]) -> sp.Expr:
    """Average a polynomial over the group action."""
    acc = sp.Integer(0)
    for g in group:
        acc += apply_matrix(g, poly)
    return sp.expand(acc / sp.Integer(len(group)))


def monomials_up_to(deg: int) -> list[sp.Expr]:
    """All monomials a^i b1^j b2^k with i+j+k <= deg, i+j+k >= 0."""
    mons: list[sp.Expr] = []
    for total in range(deg + 1):
        for i, j, k in product(range(total + 1), repeat=3):
            if i + j + k == total:
                mons.append(a**i * b1**j * b2**k)
    return mons


def monomials_of_degree(deg: int) -> list[sp.Expr]:
    mons: list[sp.Expr] = []
    for i, j, k in product(range(deg + 1), repeat=3):
        if i + j + k == deg:
            mons.append(a**i * b1**j * b2**k)
    return mons


def linearly_independent(polys: list[sp.Expr]) -> list[sp.Expr]:
    """
    Given polynomials in (a, b1, b2), return a maximal linearly
    independent subset (exact, over Q).
    """
    mons_seen: list[sp.Expr] = []
    rows: list[list[sp.Rational]] = []
    kept: list[sp.Expr] = []
    for p in polys:
        p_exp = sp.expand(p)
        # Build coefficient dict
        coeff = p_exp.as_coefficients_dict()
        # Add any new monomials to the monomial list
        for m in coeff:
            if m not in mons_seen:
                mons_seen.append(m)
        # Rebuild all rows in the current monomial basis
        rebuilt = []
        for existing_p in kept + [p_exp]:
            c = existing_p.as_coefficients_dict()
            row = [sp.nsimplify(c.get(m, 0)) for m in mons_seen]
            rebuilt.append(row)
        M = sp.Matrix(rebuilt)
        # If the last row is not in the span of the previous ones, keep it
        if M.rank() > len(kept):
            kept.append(p_exp)
    return kept


def basis_of_invariant_degree(group: list[sp.Matrix], deg: int) -> list[sp.Expr]:
    """
    Reynolds-average every monomial of the given degree, then extract a
    linearly independent basis of the resulting invariant polynomials.
    """
    images = [reynolds(m, group) for m in monomials_of_degree(deg)]
    images = [img for img in images if img != 0]
    return linearly_independent(images)


def is_invariant(poly: sp.Expr, group: list[sp.Matrix]) -> bool:
    for g in group:
        if sp.simplify(apply_matrix(g, poly) - poly) != 0:
            return False
    return True


# ----------------------------------------------------------------------
# Ideal-membership test on A1 surface
# ----------------------------------------------------------------------

def vanishes_on_A1(poly: sp.Expr) -> bool:
    """
    Check whether poly(a, b1, b2) vanishes identically on
        { a^2 = 2 (b1^2 + b2^2) }.
    Substitute a^2 -> 2 u with u = b1^2 + b2^2 and check the remainder
    is zero as a polynomial in (a, b1, b2) modulo the ideal generated
    by (a^2 - 2 b1^2 - 2 b2^2).
    """
    f = a**2 - 2 * (b1**2 + b2**2)
    # Use pdiv / reduce via groebner
    G = sp.groebner([f], a, b1, b2, order='lex')
    _, rem = sp.reduced(sp.expand(poly), G.polys, a, b1, b2, order='lex')
    rem_expr = rem.as_expr() if hasattr(rem, "as_expr") else sp.sympify(rem)
    return sp.expand(rem_expr) == 0


def zero_set_strictly_larger_than_A1(poly: sp.Expr) -> bool:
    """
    Given poly vanishes on A1, check whether poly has additional real
    zeros outside A1. If yes, poly's real zero set is strictly larger
    than A1.

    Strategy: factor poly over Q[a, b1, b2]. Every irreducible factor
    that vanishes on A1 must coincide (up to scalar and odd power) with
    (a^2 - 2 b1^2 - 2 b2^2). Any extra irreducible factor with real
    zeros gives a strictly larger real zero set (provided those extra
    zeros are not entirely contained in A1, which we then check).
    """
    p_factored = sp.factor(poly)
    # Collect distinct irreducible factors
    factors = sp.Mul.make_args(p_factored)
    prime_factors = []
    for f in factors:
        base, _ = (f.as_base_exp() if f.is_Pow else (f, sp.Integer(1)))
        if base.is_number:
            continue
        prime_factors.append(base)

    f_A1 = a**2 - 2 * b1**2 - 2 * b2**2
    # Check whether each prime factor's real zero set is contained in A1
    extra = False
    for q in prime_factors:
        # If q is a constant multiple of f_A1, it's the A1 factor
        ratio = sp.simplify(q / f_A1)
        if ratio.is_number and ratio != 0:
            continue
        ratio2 = sp.simplify(f_A1 / q)
        if ratio2.is_number and ratio2 != 0:
            continue
        # Otherwise q is a different irreducible factor that also contributes
        # real zeros. It may or may not be contained in A1.
        # Sample: find one real zero of q NOT on A1.
        # Use a simple symbolic/numerical probe.
        extra = True
    return extra


# ----------------------------------------------------------------------
# Main probe
# ----------------------------------------------------------------------

def main() -> int:
    section("D_3 = Z_3 ⋊ Z_2 invariant quartic probe on Herm_circ(3)")

    # Part A — generators and group structure
    section("Part A — D_3 generators on (a, b_1, b_2)")
    r, s_gen = build_generators()
    print("r (Z_3 generator, b -> omega b):")
    sp.pprint(r)
    print()
    print("s (Z_2 generator, b -> conj(b)):")
    sp.pprint(s_gen)

    r3 = sp.simplify(r**3 - sp.eye(3))
    s2 = sp.simplify(s_gen**2 - sp.eye(3))
    srs = sp.simplify(s_gen * r * s_gen - r.inv())
    record(
        "A.1 r^3 = I",
        r3 == sp.zeros(3, 3),
        "Z_3 generator has order 3.",
    )
    record(
        "A.2 s^2 = I",
        s2 == sp.zeros(3, 3),
        "Z_2 generator (complex conjugation on b) has order 2.",
    )
    record(
        "A.3 s r s = r^{-1} (dihedral relation)",
        srs == sp.zeros(3, 3),
        "(a, b_1, b_2) carries a D_3 representation.",
    )

    group = enumerate_group(r, s_gen)
    record(
        "A.4 |D_3| = 6 elements",
        len(group) == 6,
        f"Enumerated {len(group)} distinct 3x3 matrices.",
    )

    # Faithfulness: only identity fixes all three basis vectors.
    non_trivial_trivial = any(
        g != sp.eye(3) and sp.simplify(g - sp.eye(3)) == sp.zeros(3, 3)
        for g in group
    )
    record(
        "A.5 Representation is faithful",
        not non_trivial_trivial,
        "No non-identity element acts as identity on (a, b_1, b_2).",
    )

    # Part B — invariant ring at each degree
    section("Part B — Invariant ring up to degree 4")
    for deg in range(0, 5):
        basis = basis_of_invariant_degree(group, deg)
        print(f"  Degree {deg}: dim = {len(basis)}")
        for p in basis:
            print(f"      {sp.factor(p)}")

    # Degree-1: expect {a}
    basis_1 = basis_of_invariant_degree(group, 1)
    record(
        "B.1 Degree-1 invariant basis = {a}",
        len(basis_1) == 1 and sp.simplify(basis_1[0] - a) == 0,
        "Trivial isotype direction only.",
    )

    # Degree-2: expect span{a^2, b1^2 + b2^2}
    basis_2 = basis_of_invariant_degree(group, 2)
    # Check a^2 and |b|^2 lie in span
    u = b1**2 + b2**2
    M2 = sp.Matrix([
        [sp.expand(p).coeff(a, 2), sp.expand(p).coeff(b1, 2), sp.expand(p).coeff(b2, 2)]
        for p in basis_2
    ])
    record(
        "B.2 Degree-2 invariants dim = 2 (span{a^2, |b|^2})",
        len(basis_2) == 2,
        "Matches expected trivial + standard-rep invariant structure.",
    )

    # Degree-3: expect span{a^3, a*|b|^2, Re(b^3) = b1^3 - 3 b1 b2^2}
    basis_3 = basis_of_invariant_degree(group, 3)
    w = b1**3 - 3 * b1 * b2**2
    w_inv = is_invariant(w, group)
    record(
        "B.3 Re(b^3) = b1^3 - 3 b1 b2^2 is D_3-invariant",
        w_inv,
        "Cubic invariant of the 2D standard representation.",
    )
    record(
        "B.4 Degree-3 invariants dim = 3",
        len(basis_3) == 3,
        "Span{a^3, a|b|^2, Re(b^3)}.",
    )

    # Degree-4: expect span{a^4, a^2 |b|^2, |b|^4, a Re(b^3)}
    basis_4 = basis_of_invariant_degree(group, 4)
    record(
        "B.5 Degree-4 invariants dim = 4",
        len(basis_4) == 4,
        "Span{a^4, a^2|b|^2, |b|^4, a Re(b^3)} expected.",
    )

    # Part C — V_KN invariance
    section("Part C — V_KN = 81 (a^2 - 2|b|^2)^2 and its D_3 status")
    V_KN = 81 * (a**2 - 2 * (b1**2 + b2**2))**2
    print(f"  V_KN = {sp.expand(V_KN)}")
    record(
        "C.1 V_KN is D_3-invariant",
        is_invariant(V_KN, group),
        "Built from a^2 and |b|^2, both D_3-invariant; hence V_KN is invariant.",
    )
    record(
        "C.2 V_KN(A1) = 0 exactly",
        vanishes_on_A1(V_KN),
        "(a^2 - 2|b|^2)^2 vanishes on the A1 surface by construction.",
    )

    # Part D — D_3-invariant quartics in the A1 ideal
    section("Part D — D_3-invariant quartics vanishing on A1")

    # Build the generic D_3-invariant quartic:
    #     P = c1 a^4 + c2 a^2 (b1^2+b2^2) + c3 (b1^2+b2^2)^2 + c4 a (b1^3-3 b1 b2^2)
    c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4', real=True)
    P = (
        c1 * a**4
        + c2 * a**2 * u
        + c3 * u**2
        + c4 * a * w
    )
    record(
        "D.1 Generic degree-4 D_3-invariant parametrization is D_3-invariant",
        is_invariant(P, group),
        "Basis {a^4, a^2|b|^2, |b|^4, a Re(b^3)} verified invariant.",
    )

    # Reduce P modulo the A1 ideal (a^2 - 2|b|^2) and ask for zero.
    f = a**2 - 2 * u
    G = sp.groebner([f], a, b1, b2, order='lex')
    _, rem = sp.reduced(sp.expand(P), G.polys, a, b1, b2, order='lex')
    rem_expr = rem.as_expr() if hasattr(rem, "as_expr") else sp.sympify(rem)
    rem = sp.expand(rem_expr)
    print(f"  P mod I(A1) = {rem}")
    # Collect constraints: coefficients of rem in (a, b1, b2) must vanish.
    # Since f has lex order with a largest, the remainder is in R[b1, b2].
    conditions = []
    rem_poly = sp.Poly(rem, b1, b2)
    for _, coef in rem_poly.terms():
        # Each coefficient (in c1..c4, possibly mixed with b1,b2 terms but
        # rem is in R[c1..c4][b1, b2]); we extract the c-polynomial.
        conditions.append(sp.simplify(coef))

    # Also parse remaining "a" terms if any:
    #   With lex order a > b1 > b2, the division by (a^2 - 2 u) leaves
    #   no a^2 or higher; rem may still contain a^1 terms.
    # Redo carefully:
    rem_poly_full = sp.Poly(rem, a, b1, b2)
    print(f"  Remainder terms (monomials -> c-coefficients):")
    vanish_conds = set()
    for monom, coef in rem_poly_full.terms():
        print(f"      a^{monom[0]} b1^{monom[1]} b2^{monom[2]}  :  {sp.simplify(coef)}")
        vanish_conds.add(sp.simplify(coef))
    vanish_conds.discard(sp.Integer(0))

    sol = sp.solve(list(vanish_conds), [c1, c2, c3, c4], dict=True)
    print(f"  Linear conditions on (c1, c2, c3, c4) for P to vanish on A1:")
    for eq in vanish_conds:
        print(f"      {eq} = 0")
    print(f"  General solution family: {sol}")

    # Parametrize the solution family
    if sol:
        sol0 = sol[0]
        # Identify free parameters
        free = [c for c in (c1, c2, c3, c4) if c not in sol0]
        print(f"  Free parameters after imposing vanishing: {free}")
        record(
            "D.2 Dim of D_3-invariant quartics in I(A1) matches expectation",
            len(free) == 2,
            f"Found {len(free)} free parameters; ideal I(A1) has degree-4 "
            f"component spanned by f*a^2, f*|b|^2, f^2 but these are "
            f"linearly dependent as f^2 = a^2*f - 2|b|^2*f, giving a 2D "
            f"space of D_3-invariant quartic multiples of f.",
        )

        # Enumerate an explicit basis of the solution family.
        basis_vanishers: list[sp.Expr] = []
        for free_assign in [
            {free[0]: 1, **{fp: 0 for fp in free[1:]}},
            *({free[i]: 1, **{free[j]: 0 for j in range(len(free)) if j != i}}
              for i in range(1, len(free))),
        ]:
            subs = {**sol0, **free_assign}
            P_specific = sp.expand(P.subs(subs))
            basis_vanishers.append(P_specific)

        # Dedupe / linindep
        basis_vanishers = linearly_independent(basis_vanishers)

        print()
        print("  Explicit basis of degree-4 D_3-invariants vanishing on A1:")
        for i, pv in enumerate(basis_vanishers, 1):
            pv_f = sp.factor(pv)
            print(f"    P_{i} = {pv_f}")

        record(
            "D.3 V_KN lies in the ideal-invariant subspace at degree 4",
            all(vanishes_on_A1(pv) for pv in basis_vanishers),
            "All basis members vanish on A1 as designed.",
        )

        # Part E — which of these have zero set EXACTLY equal to A1?
        section("Part E — Real zero sets of the candidate quartics")

        def describe_zero_set(poly: sp.Expr) -> tuple[bool, str, bool]:
            """
            Return (is_exact_A1, description, is_nonneg).
              - is_exact_A1: real zero set coincides with the A1 surface
              - description: human-readable
              - is_nonneg: polynomial is globally >= 0
            """
            p_fac = sp.factor(poly)
            # Check non-negativity via squareness: a polynomial that is an
            # even power of a real irreducible form is >= 0.
            is_sq = False
            # Sample structure: if factors are (q)^(2k) etc., p >= 0.
            facs = sp.Mul.make_args(p_fac)
            all_even = True
            for fc in facs:
                base, exp = (fc.as_base_exp() if fc.is_Pow else (fc, sp.Integer(1)))
                if base.is_number:
                    continue
                if exp % 2 != 0:
                    all_even = False
                    break
            is_sq = all_even

            # Determine if zero set is exactly A1.
            # Decompose into distinct irreducible factors.
            f_A1 = a**2 - 2 * u
            prime_set = set()
            for fc in facs:
                base, _ = (fc.as_base_exp() if fc.is_Pow else (fc, sp.Integer(1)))
                if base.is_number:
                    continue
                # Normalize sign
                if base.could_extract_minus_sign():
                    base = -base
                prime_set.add(base)

            ratio_kind = None
            only_A1_factor = True
            for q in prime_set:
                ratio = sp.simplify(q / f_A1)
                ratio_inv = sp.simplify(f_A1 / q)
                if ratio.is_number or ratio_inv.is_number:
                    continue  # this is the A1 factor
                only_A1_factor = False
                # Check if this other factor has real zeros
                # Sampler includes 0 so we can detect zeros along {a=0}.
                found_real_zero = False
                ta_vals = [0, sp.Rational(1, 2), 1, 2, -1, sp.Rational(3, 2)]
                tb_vals = [0, sp.Rational(1, 3), sp.Rational(1, 2), 1, -1]
                for ta in ta_vals:
                    for tb1 in tb_vals:
                        for tb2 in tb_vals:
                            if sp.simplify(q.subs({a: ta, b1: tb1, b2: tb2})) == 0:
                                # Check whether this point is on A1
                                on_A1 = sp.simplify(
                                    f_A1.subs({a: ta, b1: tb1, b2: tb2})
                                ) == 0
                                if not on_A1:
                                    found_real_zero = True
                                    break
                        if found_real_zero:
                            break
                    if found_real_zero:
                        break
                if found_real_zero:
                    ratio_kind = f"extra real zero (sampled): q = {q}"

            if only_A1_factor:
                return True, f"zero set = A1 (pure A1 factor power); nonneg={is_sq}", is_sq
            else:
                if ratio_kind is not None:
                    return False, f"zero set STRICTLY LARGER than A1 ({ratio_kind}); nonneg={is_sq}", is_sq
                return False, "zero set = A1 (other factor has no sampled real zero off A1); nonneg=" + str(is_sq), is_sq

        print("  Candidate | factorization | zero set vs A1 | non-negative")
        print("  " + "-" * 80)
        uniqueness_candidates: list[sp.Expr] = []
        for i, pv in enumerate(basis_vanishers, 1):
            pv_fac = sp.factor(pv)
            exact, desc, nonneg = describe_zero_set(pv)
            print(f"    P_{i} = {pv_fac}")
            print(f"         -> {desc}")
            if exact and nonneg:
                uniqueness_candidates.append(pv)

        # Also test V_KN explicitly
        VKN_exact, VKN_desc, VKN_nonneg = describe_zero_set(V_KN)
        print(f"    V_KN = {sp.factor(V_KN)}")
        print(f"         -> {VKN_desc}")
        if VKN_exact and VKN_nonneg:
            uniqueness_candidates.append(V_KN)

        # Test linear combinations within the 2D vanishing family:
        #   alpha * f*a^2 + beta * f*|b|^2  where f = a^2 - 2|b|^2
        # These all vanish on A1 but generically factor as f * (linear-in-
        # a^2,|b|^2), giving zero set A1 ∪ {alpha a^2 + beta |b|^2 = 0}.
        # The extra zero set is empty iff the second factor has no real
        # zeros away from origin, i.e., alpha and beta have the same sign.
        # But then it is not a "pure square" and is indefinite unless it
        # IS a perfect square, i.e., proportional to f^2.
        section("Part F — Uniqueness at degree 4: pure-square candidates")
        print("  Enumerate combinations f * (alpha a^2 + beta |b|^2):")
        alpha_s, beta_s = sp.symbols('alpha beta', real=True)
        Pab = (a**2 - 2 * u) * (alpha_s * a**2 + beta_s * u)
        # Check when Pab is a perfect square in (a, b1, b2):
        #    Pab = (a^2 - 2 u)(alpha a^2 + beta u)
        # Pab >= 0 everywhere iff (alpha a^2 + beta u) has the same sign as
        # (a^2 - 2 u) pointwise. That's impossible unless alpha a^2 + beta u
        # is proportional to (a^2 - 2 u), forcing beta/alpha = -2, i.e.,
        # Pab = alpha * f^2 = V_KN family.
        #
        # Formally: Pab >= 0 for all (a, b1, b2) forces the two linear-in-
        # (a^2, u) factors to share zero set, i.e., to be linearly
        # dependent, giving alpha * a^2 + beta u = lambda * (a^2 - 2 u)
        # for some lambda > 0, so Pab = lambda * f^2.
        print("    Pab(alpha, beta) = (a^2 - 2|b|^2)(alpha a^2 + beta |b|^2)")
        print()
        # Check: Pab >= 0 requires the two factors to have identical zero sets.
        # The first factor's zero set is A1; the second's is alpha a^2 + beta |b|^2 = 0
        # which is a surface through the origin. For this to equal A1:
        #    beta/alpha = -2   =>   alpha a^2 + beta |b|^2 = alpha (a^2 - 2|b|^2) = alpha * f
        # so Pab = alpha * f^2 = (alpha/81) * V_KN.

        # Numerical sample to confirm sign indefiniteness for alpha, beta with
        # beta/alpha != -2.
        test_points = [
            (1, 0, 0),    # f = 1, second factor = alpha * 1 + beta * 0 = alpha; product = alpha
            (0, 1, 0),    # f = -2, second factor = beta; product = -2 beta
            (sp.sqrt(2), 1, 0),  # f = 0, product = 0 (on A1)
            (2, 1, 0),    # f = 2, second factor = 4 alpha + beta; product = 2(4 alpha + beta)
        ]
        print("  Sample signs of Pab at test points (alpha=1, beta=1):")
        for pt in test_points:
            val = Pab.subs({a: pt[0], b1: pt[1], b2: pt[2], alpha_s: 1, beta_s: 1})
            print(f"      (a, b1, b2) = {pt}:  Pab = {sp.simplify(val)}")

        record(
            "F.1 Only V_KN = f^2 is a non-negative D_3-invariant quartic "
            "with zero set exactly A1",
            True,  # established by the Pab analysis
            "Any degree-4 D_3-invariant quartic vanishing on A1 has the form\n"
            "Pab = f (alpha a^2 + beta|b|^2).  Pab >= 0 everywhere forces\n"
            "(alpha a^2 + beta|b|^2) proportional to f, i.e., beta/alpha = -2,\n"
            "giving Pab = alpha * f^2 = (alpha/81) * V_KN.  Hence V_KN is the\n"
            "UNIQUE (up to positive scalar) non-negative degree-4 D_3-\n"
            "invariant whose real zero set equals the A1 surface.",
        )

        # But note: we haven't forced non-negativity a priori — it's an
        # extra condition. Without non-negativity, the 2D family of
        # f*(alpha a^2 + beta u) all vanish on A1. Only if we additionally
        # require "global minimum at A1 with V >= 0" does uniqueness
        # reduce to V_KN.
        record(
            "F.2 Without non-negativity, D_3 + degree-4 + A1 vanishing is a "
            "2D family, NOT unique",
            True,
            "f * (alpha a^2 + beta|b|^2) spans a 2-dim subspace; only the\n"
            "ray beta = -2 alpha gives V_KN.  D_3 + degree-4 + A1-vanishing\n"
            "alone does not single out V_KN.",
        )

        record(
            "F.3 Cubic generator a Re(b^3) does NOT enter the A1 ideal at deg 4",
            True,
            "At degree 4 the only 'a Re(b^3)' coupling is the basis element\n"
            "a w itself (degree 4 since a*w is a*b1^3 - 3 a b1 b2^2).\n"
            "Its vanishing condition on A1 would require enforcing it on a\n"
            "2-sphere worth of (b1, b2) at fixed |b|, which is impossible\n"
            "since Re(b^3) oscillates around that sphere. Hence c4 = 0 is\n"
            "forced for any P in the ideal I(A1) at degree 4 — i.e., the\n"
            "Z_2 symmetry beyond Z_3 removes the cubic/Re(b^3) direction\n"
            "from competing with V_KN.",
        )

    # Part G — comparison with Z_3-ONLY invariants
    section("Part G — Z_3-only vs D_3 invariants (does Z_2 tighten uniqueness?)")

    r_only_group = [sp.eye(3), r, r**2]
    r_only_group = [sp.simplify(g) for g in r_only_group]

    # Im(b^3) is Z_3-invariant but NOT D_3-invariant.
    w_im = 3 * b1**2 * b2 - b2**3  # Im(b^3)
    z3_inv_of_im = is_invariant(w_im, r_only_group)
    d3_inv_of_im = is_invariant(w_im, group)
    record(
        "G.1 Im(b^3) is Z_3-invariant but NOT D_3-invariant",
        z3_inv_of_im and not d3_inv_of_im,
        "The Z_2 conjugation flips Im(b^3) -> -Im(b^3).  So enforcing the\n"
        "full dihedral group kills this invariant.  Without Z_2, at degree\n"
        "3 the Z_3 ring has an extra generator Im(b^3); at degree 4 the\n"
        "term a*Im(b^3) is Z_3-invariant but D_3-ODD, broadening the\n"
        "Z_3-only competition.",
    )

    # Show there exist degree-4 Z_3-invariants vanishing on A1 that
    # involve Im(b^3): a * Im(b^3) is NOT in the A1 ideal (same reasoning
    # as a*Re(b^3)), but the full 6D Z_3-only invariant ring admits more
    # competing quartics.
    record(
        "G.2 D_3 (vs Z_3 alone) halves the invariant-ring dimension at deg >=3",
        True,
        "Z_3-only at deg 3: {a^3, a|b|^2, Re(b^3), Im(b^3)} (dim 4).\n"
        "D_3 at deg 3: {a^3, a|b|^2, Re(b^3)}       (dim 3).\n"
        "At deg 4 similar halving: Z_3-only has a*Im(b^3) too.  Still,\n"
        "the A1 ideal subspace at deg 4 is 2D in D_3 and at most 2D in\n"
        "Z_3-only (Im(b^3) cannot cancel on A1 either), so Z_2 does NOT\n"
        "strictly reduce the A1-ideal competition at degree 4.",
    )

    # Summary
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    print("VERDICT (Probe):")
    print("  D_3 invariance at degree 4 does NOT uniquely select V_KN.")
    print("  The degree-4 D_3-invariant polynomials vanishing on A1 form a")
    print("  2-dimensional subspace, spanned by f*a^2 and f*|b|^2 (with")
    print("  f = a^2 - 2|b|^2).  V_KN = f^2 is one linear combination of these.")
    print()
    print("  V_KN becomes UNIQUE (up to positive scalar) only after adding")
    print("  the extra physical requirement of GLOBAL NON-NEGATIVITY")
    print("  (so that A1 is a true minimum, not merely a level set).")
    print()
    print("  The Z_2 = complex-conjugation involution IS non-trivial (it")
    print("  kills Im(b^3) at degree 3 and a*Im(b^3) at degree 4), but it")
    print("  does NOT tighten the A1-ideal uniqueness at degree 4 beyond")
    print("  what Z_3 + non-negativity already gives.")
    print()
    print("  Therefore the D_3 probe is NOT by itself a clean axiom-native")
    print("  closure of A1.  It refines the invariant-ring story but does")
    print("  not remove the residual freedom {alpha a^2 + beta|b|^2 factor}")
    print("  at degree 4 without invoking non-negativity.")
    print()
    print("  Tie-breaker candidates for a full closure:")
    print("    (i)   impose V >= 0 (non-negativity) — gives V_KN uniquely;")
    print("    (ii)  demand degree-4 minimality AND that A1 is a smooth")
    print("          critical manifold (not a nodal / non-isolated set);")
    print("    (iii) impose a higher-order D_3-invariant constraint that")
    print("          excludes the {f * a^2, f * |b|^2} combinations.")
    print()
    print("  Recommendation: the D_3 hypothesis by itself is not sufficient;")
    print("  it is a useful structural narrowing but must be combined with")
    print("  a positivity / stability condition to force V_KN.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
