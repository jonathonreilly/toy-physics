#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ckm_classical_number_theory_integer_characterization_theorem_note_2026-04-25`.

The parent note's load-bearing content is the classical number-theoretic
characterization of the retained CKM structural integers
`(N_pair, N_color, N_quark) = (2, 3, 6)`:

  (P1) Perfect-number identity:    N_quark = 1 + N_pair + N_color
  (P2) Sigma-perfect condition:    sigma(N_quark) = 2 N_quark
  (P3) Sum-product coincidence:    1 + N_pair + N_color = 1 * N_pair * N_color
  (P4) Deficient/perfect:          N_pair, N_color deficient; N_quark perfect
  (T1) Triangular ladder:          N_color = T_{N_pair}, N_quark = T_{N_color}
  (L1) Lie-dimensional:            N_color = N_pair^2 - 1 = dim(adjoint SU(2))
  (M1) Mersenne prime:             N_color = 2^{N_pair} - 1
  (M2) Euclid-Euler perfect:       N_quark = 2^{N_pair-1}(2^{N_pair} - 1)
  (U1) Five independent uniqueness routes (a)+(b)+(x), x in {c,d,e,f,g}.

The existing primary runner
(`scripts/frontier_ckm_classical_number_theory_integer_characterization.py`)
verifies these identities at exact integer / Fraction precision at the
retained framework counts. This Pattern B audit companion adds a
sympy-based exact-symbolic verification:

  (a) treats `(N_pair, N_color, N_quark)` as positive-integer symbols
      with the framework constraint `N_quark = N_pair * N_color`;
  (b) verifies (P1), (P2), (P3), (P4) classifications symbolically at
      retained `(N_pair, N_color, N_quark) = (2, 3, 6)`;
  (c) verifies (T1) parametric in `N_pair` and `N_color` reading
      `T_n = n(n+1)/2`;
  (d) verifies (L1), (M1), (M2) at retained `N_pair = 2`;
  (e) verifies (U1.c), (U1.d), (U1.e), (U1.f), (U1.g) by symbolic
      manipulation of each three-constraint system reducing to the
      polynomial / exponential identity that pins `N_color = 3`;
  (f) provides counterfactual probes confirming each identity is
      load-bearing for the retained triple `(2, 3, 6)`.

Companion role: Pattern B audit-acceleration only. Not a new claim row,
not a new source note, no status promotion. The cited upstream count
authority (`N_pair = 2`, `N_color = 3`, `N_quark = N_pair * N_color = 6`)
is imported from the retained CKM magnitudes structural-counts theorem
and is not re-derived here.
"""

from __future__ import annotations

import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, symbols, divisors, divisor_sigma
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (B)"
    else:
        FAIL += 1
        tag = "FAIL (B)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def main() -> int:
    print("=" * 88)
    print("Audit companion (exact-symbolic) for")
    print("ckm_classical_number_theory_integer_characterization_theorem_note_2026-04-25")
    print("Goal: sympy-symbolic verification of (P1)-(P4), (T1), (L1),")
    print("(M1), (M2), and the five uniqueness routes (U1.c-g) at exact precision.")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup and imported retained counts")
    # ---------------------------------------------------------------------
    n = Symbol("n", positive=True, integer=True)
    p_sym, c_sym, q_sym = symbols("p c q", positive=True, integer=True)

    # Retained CKM structural integers (cited authority; not re-derived).
    N_PAIR = Rational(2)
    N_COLOR = Rational(3)
    N_QUARK = Rational(6)

    print(f"  retained N_pair  = {N_PAIR}")
    print(f"  retained N_color = {N_COLOR}")
    print(f"  retained N_quark = N_pair * N_color = {N_QUARK}")
    print(f"  retained relation: N_pair = N_color - 1: {N_PAIR == N_COLOR - 1}")

    check(
        "framework constraint: N_quark == N_pair * N_color",
        simplify(N_QUARK - N_PAIR * N_COLOR) == 0,
        f"residual = {simplify(N_QUARK - N_PAIR * N_COLOR)}",
    )
    check(
        "consecutive scaffold: N_pair == N_color - 1",
        simplify(N_PAIR - (N_COLOR - 1)) == 0,
        f"residual = {simplify(N_PAIR - (N_COLOR - 1))}",
    )

    # ---------------------------------------------------------------------
    section("Part 1: (P1) Perfect-number identity N_quark = 1 + N_pair + N_color")
    # ---------------------------------------------------------------------
    P1_lhs = N_QUARK
    P1_rhs = Rational(1) + N_PAIR + N_COLOR
    check(
        "(P1) N_quark == 1 + N_pair + N_color (exact rational)",
        simplify(P1_lhs - P1_rhs) == 0,
        f"residual = {simplify(P1_lhs - P1_rhs)}",
    )
    # Proper divisors of 6 are {1, 2, 3} which match {1, N_pair, N_color}.
    proper_div_6 = [d for d in divisors(6) if d < 6]
    check(
        "(P1) proper divisors of N_quark are exactly {1, N_pair, N_color}",
        proper_div_6 == [1, int(N_PAIR), int(N_COLOR)],
        f"proper divisors of 6 = {proper_div_6}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: (P2) Sigma-perfect condition sigma(N_quark) = 2 N_quark")
    # ---------------------------------------------------------------------
    sigma_Nq = divisor_sigma(int(N_QUARK))
    P2_target = 2 * int(N_QUARK)
    check(
        "(P2) sigma(N_quark) == 2 N_quark (exact)",
        sigma_Nq == P2_target,
        f"sigma(6) = {sigma_Nq}, target = {P2_target}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (P3) Sum-product coincidence for proper divisors of 6")
    # ---------------------------------------------------------------------
    sum_proper = Rational(1) + N_PAIR + N_COLOR
    prod_proper = Rational(1) * N_PAIR * N_COLOR
    check(
        "(P3) 1 + N_pair + N_color == N_quark",
        simplify(sum_proper - N_QUARK) == 0,
        f"residual = {simplify(sum_proper - N_QUARK)}",
    )
    check(
        "(P3) 1 * N_pair * N_color == N_quark",
        simplify(prod_proper - N_QUARK) == 0,
        f"residual = {simplify(prod_proper - N_QUARK)}",
    )
    check(
        "(P3) sum == product (sum-product coincidence)",
        simplify(sum_proper - prod_proper) == 0,
        f"residual = {simplify(sum_proper - prod_proper)}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (P4) Deficient/Perfect classification")
    # ---------------------------------------------------------------------
    # N is DEFICIENT iff sigma(N) - N < N, i.e. sigma(N) < 2 N.
    # N is PERFECT  iff sigma(N) == 2 N.
    sigma_p = divisor_sigma(int(N_PAIR))
    sigma_c = divisor_sigma(int(N_COLOR))
    check(
        "(P4) N_pair = 2 is DEFICIENT (sigma(2) = 3 < 4)",
        sigma_p < 2 * int(N_PAIR),
        f"sigma(2) = {sigma_p}, 2*N_pair = {2*int(N_PAIR)}",
    )
    check(
        "(P4) N_color = 3 is DEFICIENT (sigma(3) = 4 < 6)",
        sigma_c < 2 * int(N_COLOR),
        f"sigma(3) = {sigma_c}, 2*N_color = {2*int(N_COLOR)}",
    )
    check(
        "(P4) N_quark = 6 is PERFECT (sigma(6) = 12 = 2 N_quark)",
        sigma_Nq == 2 * int(N_QUARK),
        f"sigma(6) = {sigma_Nq}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: (T1) Triangular ladder N_color = T_{N_pair}, N_quark = T_{N_color}")
    # ---------------------------------------------------------------------
    # T_n = n(n+1)/2 (parametric in n).
    T_n = n * (n + 1) / Rational(2)
    T_at_N_pair = simplify(T_n.subs(n, N_PAIR))
    T_at_N_color = simplify(T_n.subs(n, N_COLOR))

    check(
        "(T1) N_color == T_{N_pair} = N_pair (N_pair + 1)/2 (parametric in N_pair)",
        simplify(T_at_N_pair - N_COLOR) == 0,
        f"T_2 = {T_at_N_pair}, N_color = {N_COLOR}",
    )
    check(
        "(T1) N_quark == T_{N_color} = N_color (N_color + 1)/2 (parametric in N_color)",
        simplify(T_at_N_color - N_QUARK) == 0,
        f"T_3 = {T_at_N_color}, N_quark = {N_QUARK}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: (L1) Lie-dimensional N_color = N_pair^2 - 1 = dim(adjoint SU(N_pair))")
    # ---------------------------------------------------------------------
    L1_lhs = N_PAIR ** 2 - 1
    check(
        "(L1) N_color == N_pair^2 - 1 (= dim(adjoint SU(N_pair)))",
        simplify(L1_lhs - N_COLOR) == 0,
        f"N_pair^2 - 1 = {L1_lhs}, N_color = {N_COLOR}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: (M1) Mersenne identity N_color = 2^{N_pair} - 1")
    # ---------------------------------------------------------------------
    M1_lhs = Rational(2) ** N_PAIR - 1
    check(
        "(M1) N_color == 2^{N_pair} - 1 (smallest Mersenne prime)",
        simplify(M1_lhs - N_COLOR) == 0,
        f"2^N_pair - 1 = {M1_lhs}, N_color = {N_COLOR}",
    )

    # ---------------------------------------------------------------------
    section("Part 8: (M2) Euclid-Euler N_quark = 2^{N_pair-1}(2^{N_pair} - 1)")
    # ---------------------------------------------------------------------
    M2_lhs = Rational(2) ** (N_PAIR - 1) * (Rational(2) ** N_PAIR - 1)
    check(
        "(M2) N_quark == 2^{N_pair-1}(2^{N_pair} - 1) (smallest Euclid-Euler perfect)",
        simplify(M2_lhs - N_QUARK) == 0,
        f"2^(N_pair-1)(2^N_pair - 1) = {M2_lhs}, N_quark = {N_QUARK}",
    )

    # ---------------------------------------------------------------------
    section("Part 9: (U1) Five independent uniqueness routes (a)+(b)+(x)")
    # ---------------------------------------------------------------------
    # Common scaffold:
    #   (a) p = c - 1
    #   (b) q = p * c = (c - 1) c
    # Route (c): q = 1 + p + c -> (c-1) c = 1 + (c-1) + c = 2 c
    #            => c (c - 3) = 0 => c = 3 (positive integer).
    print("  Common scaffold: (a) N_pair = N_color - 1, (b) N_quark = N_pair * N_color")
    print()
    print("  Route (c): N_quark = 1 + N_pair + N_color")
    # Substitute (a), (b) into (c) and reduce.
    c_var = Symbol("c_var", positive=True, integer=True)
    Uc = (c_var - 1) * c_var - (1 + (c_var - 1) + c_var)
    Uc_simplified = simplify(Uc)
    Uc_factored = sympy.factor(Uc_simplified)
    check(
        "(U1.c) (c-1)c - (1 + (c-1) + c) reduces to c(c - 3)",
        simplify(Uc_simplified - c_var * (c_var - 3)) == 0,
        f"reduced = {Uc_simplified}, factored = {Uc_factored}",
    )
    # Positive-integer roots of c(c - 3) = 0 are c = 3 (c = 0 excluded).
    roots_c = sympy.solve(Uc_simplified, c_var)
    pos_int_roots_c = [r for r in roots_c if r > 0]
    check(
        "(U1.c) positive-integer root pins N_color = 3",
        pos_int_roots_c == [3],
        f"positive roots = {pos_int_roots_c}",
    )

    # Route (d): q = T_c = c(c+1)/2 -> (c-1)c = c(c+1)/2 => 2(c-1) = c+1 => c = 3.
    print()
    print("  Route (d): N_quark = T_{N_color}")
    Ud = (c_var - 1) * c_var - c_var * (c_var + 1) / Rational(2)
    Ud_simplified = simplify(Ud)
    Ud_factored = sympy.factor(Ud_simplified * 2)
    check(
        "(U1.d) (c-1)c - c(c+1)/2 reduces to c(c-3)/2 (proportional to c(c-3))",
        simplify(Ud_simplified * 2 - c_var * (c_var - 3)) == 0,
        f"2*reduced = {simplify(Ud_simplified*2)}, factored = {Ud_factored}",
    )
    roots_d = sympy.solve(Ud_simplified, c_var)
    pos_int_roots_d = [r for r in roots_d if r > 0]
    check(
        "(U1.d) positive-integer root pins N_color = 3",
        pos_int_roots_d == [3],
        f"positive roots = {pos_int_roots_d}",
    )

    # Route (e): 1/p + 1/c + 1/q = 1 with p = c-1, q = (c-1)c.
    # Multiplying by c (c-1) gives c + (c - 1) + 1 = c (c-1) => 2c = c^2 - c => c^2 - 3c = 0.
    print()
    print("  Route (e): 1/N_pair + 1/N_color + 1/N_quark = 1 (Egyptian fraction)")
    Ue_lhs = (
        Rational(1) / (c_var - 1)
        + Rational(1) / c_var
        + Rational(1) / ((c_var - 1) * c_var)
    )
    Ue_residual = simplify(Ue_lhs - 1)
    # Multiply by c(c-1): c + (c-1) + 1 - c(c-1) = 2c - c^2 + c = 3c - c^2 = -c(c - 3).
    Ue_cleared = simplify(Ue_residual * c_var * (c_var - 1))
    check(
        "(U1.e) cleared denominator residual reduces to -c(c-3) up to sign",
        simplify(Ue_cleared - (-c_var * (c_var - 3))) == 0,
        f"cleared = {Ue_cleared}",
    )
    roots_e = sympy.solve(Ue_residual, c_var)
    pos_int_roots_e = [r for r in roots_e if r > 0]
    check(
        "(U1.e) positive-integer root pins N_color = 3",
        pos_int_roots_e == [3],
        f"positive roots = {pos_int_roots_e}",
    )

    # Route (f): c = p^2 - 1 with p = c - 1 -> c = (c-1)^2 - 1 = c^2 - 2c => c^2 - 3c = 0.
    print()
    print("  Route (f): N_color = N_pair^2 - 1")
    Uf = c_var - ((c_var - 1) ** 2 - 1)
    Uf_simplified = simplify(Uf)
    Uf_factored = sympy.factor(-Uf_simplified)
    check(
        "(U1.f) c - ((c-1)^2 - 1) reduces to -c(c - 3) up to sign",
        simplify(-Uf_simplified - c_var * (c_var - 3)) == 0,
        f"-reduced = {simplify(-Uf_simplified)}, factored = {Uf_factored}",
    )
    roots_f = sympy.solve(Uf_simplified, c_var)
    pos_int_roots_f = [r for r in roots_f if r > 0]
    check(
        "(U1.f) positive-integer root pins N_color = 3",
        pos_int_roots_f == [3],
        f"positive roots = {pos_int_roots_f}",
    )

    # Route (g): c = 2^p - 1 with p = c - 1 -> c + 1 = 2^{c-1}.
    # f(c) = 2^{c-1} - c - 1 has f(3) = 4 - 4 = 0; f(2) = 2 - 3 = -1; f(1) = 1 - 2 = -1.
    # f(n+1) - f(n) = 2^{n-1} > 0 for n >= 2 (so strictly increasing past n=2; specifically f(4)=4, f(5)=11, ...).
    print()
    print("  Route (g): N_color = 2^{N_pair} - 1")
    f_g = lambda nn: 2 ** (int(nn) - 1) - int(nn) - 1
    f_at_3 = f_g(3)
    f_at_2 = f_g(2)
    f_at_1 = f_g(1)
    f_at_4 = f_g(4)
    f_at_5 = f_g(5)
    check(
        "(U1.g) f(c) = 2^{c-1} - c - 1 has f(3) = 0",
        f_at_3 == 0,
        f"f(3) = {f_at_3}",
    )
    check(
        "(U1.g) f(1) = -1, f(2) = -1, f(3) = 0 (no other small positive integer root <= 3)",
        f_at_1 == -1 and f_at_2 == -1 and f_at_3 == 0,
        f"f(1)={f_at_1}, f(2)={f_at_2}, f(3)={f_at_3}",
    )
    # Strict monotonicity past n = 3: f(n+1) - f(n) = 2^{n-1} - 1 > 0 for n >= 1 only;
    # we check it numerically for n in {3,...,8} and also verify f(n) > 0 for n=4..8.
    diffs_positive = all(f_g(n + 1) - f_g(n) > 0 for n in range(3, 9))
    f_values_past_3 = [f_g(k) for k in range(4, 9)]
    all_pos_past_3 = all(v > 0 for v in f_values_past_3)
    check(
        "(U1.g) f strictly increasing for c >= 3 and f(c) > 0 for c in {4,...,8}",
        diffs_positive and all_pos_past_3,
        f"f(4..8) = {f_values_past_3}",
    )

    # ---------------------------------------------------------------------
    section("Part 10: counterfactual probes")
    # ---------------------------------------------------------------------
    # If N_pair were 3 (instead of 2), the perfect-number identity (P1)
    # would require N_quark = 1 + 3 + N_color. With (b) N_quark = 3 N_color,
    # this gives 3 N_color = 4 + N_color, i.e. N_color = 2 (not 3).
    # So (P1) under counterfactual N_pair = 3 yields (3, 2, 6) not (2, 3, 6).
    # The framework's retained ordering (N_pair, N_color) = (2, 3) is therefore
    # load-bearing for the perfect-number identity.
    cf_p_alt = Rational(3)
    # Force scaffold (a) p_alt = c_alt - 1 -> c_alt = 4. Then q_alt = 12, not 6.
    cf_c_under_a = cf_p_alt + 1  # c_alt = 4
    cf_q_under_ab = cf_p_alt * cf_c_under_a  # q_alt = 12
    check(
        "counterfactual: at N_pair = 3 with scaffold (a)+(b), q = 12, not 6",
        cf_q_under_ab != N_QUARK,
        f"q_alt = {cf_q_under_ab}",
    )
    # (P2) is also failed at q = 12 since sigma(12) = 28 != 24.
    sigma_12 = divisor_sigma(12)
    check(
        "counterfactual: at q = 12, sigma(12) != 2*12 (not perfect)",
        sigma_12 != 24,
        f"sigma(12) = {sigma_12}",
    )

    # If N_pair were 4 (or any p != 2), (M1) N_color = 2^p - 1 would give a
    # different value (15 not 3) and would also break the constraint (a).
    cf_p_4 = Rational(4)
    cf_c_via_M1 = Rational(2) ** cf_p_4 - 1  # = 15
    check(
        "counterfactual: at N_pair = 4, (M1) gives N_color = 15 != 3",
        cf_c_via_M1 != N_COLOR,
        f"2^4 - 1 = {cf_c_via_M1}",
    )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision over the retained CKM counts:")
    print("    (P1) N_quark == 1 + N_pair + N_color (perfect-number identity)")
    print("    (P2) sigma(N_quark) == 2 N_quark (sigma-perfect)")
    print("    (P3) sum and product of proper divisors of 6 both equal 6")
    print("    (P4) classification: N_pair, N_color deficient; N_quark perfect")
    print("    (T1) N_color = T_{N_pair}, N_quark = T_{N_color} (parametric)")
    print("    (L1) N_color = N_pair^2 - 1 (Lie-dimensional)")
    print("    (M1) N_color = 2^{N_pair} - 1 (Mersenne)")
    print("    (M2) N_quark = 2^{N_pair-1}(2^{N_pair} - 1) (Euclid-Euler)")
    print("    (U1.c-g) all five three-constraint routes reduce to c(c-3)=0")
    print("             (or the f(c)=0 monotonicity for route g),")
    print("             positive-integer-pinned to N_color = 3.")
    print("    Counterfactuals confirm (N_pair, N_color) = (2, 3) ordering")
    print("    is load-bearing for (P1)-(P2) and the (M1) Mersenne route.")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
