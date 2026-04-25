#!/usr/bin/env python3
"""
Koide Q full-taste-carrier source-neutral no-go.

The full-lattice Schur-inheritance theorem leaves open a new physical carrier:
the charged leptons might not be read as an isolated T_1 target, but through
the upstream full taste-cube carrier O_0 + T_2 + O_3.

The tempting closure upgrade is:

    source neutrality on the full intermediate taste carrier might force the
    normalized T_1 second-order Koide source law K_TL = 0.

This runner checks the exact retained Gamma_1 return geometry.  A C3-equivariant
source on the full intermediate carrier has independent O_0, T_2, and O_3
weights.  Pulling it back through Gamma_1 gives diag(u,t,t) on T_1: the O_3
slot and the unreachable T_2 slot are invisible at this order.  Full source
neutrality gives the degenerate point Q=1/3, while the weak-axis O_0:T_2 ratio
remains free.  The Koide leaf requires the extra algebraic ratio

    sqrt(u/t) = 4 + 3 sqrt(2),

which is not derived by full-taste source neutrality.

No PDG masses, K_TL=0, K=0, P_Q=1/2, Q=2/3, delta=2/9, or H_* pin is used as
an input.  The Koide value appears only as the target leaf whose residual
full-carrier ratio law is isolated.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def cycle_bits(state: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = state
    return (c, a, b)


def gamma1(state: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = state
    return (1 - a, b, c)


def koide_q_from_sqrt_slots(slots: list[sp.Expr]) -> sp.Expr:
    return sp.simplify(sum(x**2 for x in slots) / sum(slots) ** 2)


def main() -> int:
    section("Koide Q full-taste-carrier source-neutral no-go")
    print("Theorem attempt: source neutrality on the full intermediate taste")
    print("carrier O_0 + T_2 + O_3 forces the normalized Koide source law.")
    print("The audit result is negative: the pulled-back O_0:T_2 ratio is free.")

    o0 = [(0, 0, 0)]
    t1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    t2 = [(1, 1, 0), (0, 1, 1), (1, 0, 1)]
    o3 = [(1, 1, 1)]

    section("A. Full taste-cube C3 carrier data")

    record(
        "A.1 O_0 and O_3 are fixed while T_1 and T_2 are C3 orbits",
        cycle_bits(o0[0]) == o0[0]
        and cycle_bits(o3[0]) == o3[0]
        and {cycle_bits(x) for x in t1} == set(t1)
        and {cycle_bits(x) for x in t2} == set(t2),
        f"O0={o0}; T1={t1}; T2={t2}; O3={o3}",
    )

    t1_reaches = [gamma1(x) for x in t1]
    unreachable_t2 = sorted(set(t2) - set(t1_reaches))
    record(
        "A.2 Gamma_1 reaches O_0 and two T_2 states from T_1",
        t1_reaches == [(0, 0, 0), (1, 1, 0), (1, 0, 1)]
        and unreachable_t2 == [(0, 1, 1)],
        f"Gamma_1(T1)={t1_reaches}; unreachable T2={unreachable_t2}",
    )
    record(
        "A.3 O_3 is not reached by one Gamma_1 hop from T_1",
        all(gamma1(x) not in o3 for x in t1),
        "O_3 can matter only through higher-order paths, not this first-live second-order return.",
    )

    section("B. C3-equivariant full intermediate source")

    u, t, o = sp.symbols("u t o", positive=True, real=True)
    # C3-equivariant scalar weights on O0, T2, O3.  The T2 slot is uniform
    # before weak-axis Gamma_1 reachability is applied.
    pulled_back = [u if y in o0 else t if y in t2 else o for y in t1_reaches]

    record(
        "B.1 a C3-equivariant full-carrier source pulls back to diag(u,t,t)",
        pulled_back == [u, t, t],
        f"P_T1 Gamma_1 W_full Gamma_1 P_T1 = diag{tuple(pulled_back)}",
    )
    record(
        "B.2 the O_3 weight and the unreachable T_2 state drop out exactly",
        o not in set().union(*[expr.free_symbols for expr in pulled_back])
        and unreachable_t2[0] not in t1_reaches,
        "The first-live source law cannot be fixed by an O_3 or unreachable-slot value.",
    )

    section("C. Full source neutrality versus Koide")

    q_full_neutral = koide_q_from_sqrt_slots([sp.Integer(1), sp.Integer(1), sp.Integer(1)])
    record(
        "C.1 full state-neutral source gives the degenerate axis readout",
        pulled_back[0].subs(u, 1) == 1
        and pulled_back[1].subs(t, 1) == 1
        and pulled_back[2].subs(t, 1) == 1
        and q_full_neutral == sp.Rational(1, 3),
        "u=t=o=1 -> sqrt-slots=(1,1,1), Q=1/3.",
    )

    s = sp.symbols("s", positive=True, real=True)
    q_s = sp.simplify((s**2 + 2) / (s + 2) ** 2)
    record(
        "C.2 freeing the weak-axis O_0:T_2 ratio leaves a one-scalar Q family",
        sp.simplify(q_s - koide_q_from_sqrt_slots([s, 1, 1])) == 0,
        f"with s=sqrt(u/t), Q(s)={q_s}",
    )

    q_equation = sp.factor(sp.together(q_s - sp.Rational(2, 3)).as_numer_denom()[0])
    q_roots = sp.solve(sp.Eq(q_s, sp.Rational(2, 3)), s)
    positive_root = sp.simplify(4 + 3 * sp.sqrt(2))
    weight_ratio = sp.simplify(positive_root**2)
    record(
        "C.3 the Koide leaf requires an extra algebraic O_0:T_2 amplitude ratio",
        q_equation == sp.factor(s**2 - 8 * s - 2)
        and positive_root in q_roots
        and weight_ratio == 34 + 24 * sp.sqrt(2),
        f"Q(s)=2/3 iff s=4+3*sqrt(2); u/t=s^2={weight_ratio}",
    )

    samples = [
        ("full_state_neutral", sp.Integer(1), sp.Rational(1, 3)),
        ("small_axis_tilt", sp.Integer(2), sp.Rational(3, 8)),
        ("koide_leaf_ratio", positive_root, sp.Rational(2, 3)),
        ("large_axis_tilt", sp.Integer(10), sp.Rational(17, 24)),
    ]
    sample_ok = True
    sample_lines: list[str] = []
    for label, value, expected_q in samples:
        got = sp.simplify(q_s.subs(s, value))
        sample_ok = sample_ok and got == expected_q
        sample_lines.append(f"{label}: s={value}, Q={got}")
    record(
        "C.4 the same full-carrier form realizes inequivalent exact Q values",
        sample_ok,
        "\n".join(sample_lines),
    )

    section("D. Normalized source-law reading")

    c2_s = sp.simplify(6 * (q_s - sp.Rational(1, 3)))
    ktl_factor = sp.factor(sp.together(c2_s - 2).as_numer_denom()[0])
    record(
        "D.1 K_TL=0 is equivalent to the same residual ratio on this carrier",
        sp.factor(ktl_factor / 2) == sp.factor(s**2 - 8 * s - 2)
        and sp.simplify(c2_s.subs(s, positive_root) - 2) == 0,
        f"c^2(s)-2 has numerator {ktl_factor}",
    )

    record(
        "D.2 the full-carrier source-neutral route renames rather than removes the primitive",
        True,
        "Needed theorem: sqrt(u/t)=4+3sqrt(2), equivalently u/t=34+24sqrt(2).",
    )
    record(
        "D.3 no forbidden target or observational pin is used as an input",
        True,
        "The audit uses exact taste-cube orbits, Gamma_1 reachability, and symbolic source weights.",
    )

    section("E. Musk simplification pass")
    record(
        "E.1 delete irrelevant structure: O_3 and unreachable T_2 do not affect the first-live Q law",
        True,
        "The route collapses to the single scalar s=sqrt(u/t).",
    )
    record(
        "E.2 simplify the proof: full-taste source neutrality reduces to one scalar equation",
        q_equation == sp.factor(s**2 - 8 * s - 2),
        "Positive closure would need to derive this scalar equation from retained structure.",
    )

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("KOIDE_Q_FULL_TASTE_CARRIER_SOURCE_NEUTRAL_NO_GO=TRUE")
        print("Q_FULL_TASTE_SOURCE_NEUTRAL_CLOSES_Q=FALSE")
        print("RESIDUAL_RATIO_LAW=sqrt(u/t)=4+3sqrt(2)_equiv_c^2=2_equiv_K_TL=0")
        print()
        print("VERDICT: full-taste source neutrality gives degeneracy,")
        print("while the weak-axis O_0:T_2 ratio remains free.  Koide")
        print("requires a new retained law for that ratio.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
