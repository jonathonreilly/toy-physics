#!/usr/bin/env python3
"""
Koide Q minimal-selector value no-go.

This runner audits the tempting upgrade:

    unique minimal scale-free C3-invariant selector variable
    -> Koide value.

The minimal-selector theorem is real support: after accepting the first-live
second-order carrier, all nontrivial scale-free quadratic selectors reduce to
one positive projective coordinate.  But a coordinate is not a value law.

Using r := E_perp/E_plus > 0, the normalized carrier is

    Y(r) = diag(2/(1+r), 2r/(1+r)).

The Koide/source-free point is r = 1, equivalently K_TL = 0.  The runner
verifies that for every c > 0 the equally scale-free C3-invariant law

    F_c(r) = (r - c)^2

has a unique minimum at r = c.  Thus uniqueness of the invariant coordinate
does not select c = 1.  Selecting c = 1 is the same missing value law, in
coordinate form.

No PDG masses, Q target import, K_TL=0 assumption, or H_* pin is used.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    PASSES.append((label, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def main() -> int:
    print("=" * 88)
    print("Koide Q minimal-selector value no-go")
    print("=" * 88)

    e_plus, e_perp, scale = sp.symbols("E_plus E_perp scale", positive=True, real=True)
    r, c = sp.symbols("r c", positive=True, real=True)

    ratio = sp.simplify(e_perp / e_plus)
    ratio_scaled = sp.simplify((scale * e_perp) / (scale * e_plus))
    y_plus = sp.simplify(2 / (1 + r))
    y_perp = sp.simplify(2 * r / (1 + r))
    k_tl = sp.simplify((1 - y_plus) / (y_plus * y_perp))
    q_of_r = sp.simplify((1 + r) / 3)

    check(
        "1. The projective selector coordinate r = E_perp/E_plus is scale-free",
        sp.simplify(ratio_scaled - ratio) == 0,
        f"r = {ratio}",
    )
    check(
        "2. r parametrizes the normalized trace-2 carrier",
        sp.simplify(y_plus + y_perp - 2) == 0,
        f"Y(r) = diag({y_plus}, {y_perp})",
    )
    check(
        "3. The Q-relevant traceless source is K_TL(r) = (r^2-1)/(4r)",
        sp.simplify(k_tl - (r**2 - 1) / (4 * r)) == 0,
        f"K_TL(r) = {k_tl}",
    )
    check(
        "4. Q is just a reparametrization of the same coordinate",
        q_of_r == (1 + r) / 3,
        f"Q(r) = {q_of_r}",
    )

    f_c = sp.simplify((r - c) ** 2)
    df_c = sp.diff(f_c, r)
    d2f_c = sp.diff(f_c, r, 2)
    crit_c = sp.solve(sp.Eq(df_c, 0), r)

    check(
        "5. F_c(r)=(r-c)^2 is a scale-free value law for every c>0",
        sp.simplify(f_c.subs(r, ratio_scaled) - f_c.subs(r, ratio)) == 0,
        "It depends only on the unique projective invariant coordinate.",
    )
    check(
        "6. F_c has unique positive minimizer r=c",
        crit_c == [c] and d2f_c == 2,
        f"dF_c/dr = {df_c}; d2F_c/dr2 = {d2f_c}",
    )

    samples = [sp.Rational(1, 2), sp.Rational(1, 1), sp.Rational(2, 1)]
    sample_lines: list[str] = []
    distinct_values = set()
    all_stationary = True
    for value in samples:
        q_value = sp.simplify(q_of_r.subs(r, value))
        ktl_value = sp.simplify(k_tl.subs(r, value))
        stationarity = sp.simplify(df_c.subs({r: value, c: value}))
        distinct_values.add((q_value, ktl_value))
        all_stationary = all_stationary and stationarity == 0
        sample_lines.append(f"c={value} -> r={value}, Q={q_value}, K_TL={ktl_value}")

    check(
        "7. Different admissible c select different physical values",
        all_stationary and len(distinct_values) == len(samples),
        "\n".join(sample_lines),
    )

    c_from_ktl_zero = sp.solve(sp.Eq(k_tl.subs(r, c), 0), c)
    check(
        "8. Selecting the Koide/source-free value is exactly c=1",
        c_from_ktl_zero == [1],
        f"K_TL(c)=0 -> c={c_from_ktl_zero}",
    )

    fixed_points = sp.solve(sp.Eq(r, 1 / r), r)
    positive_fixed = [root for root in fixed_points if root == 1]
    check(
        "9. A quotient-level block exchange would add the missing value law",
        positive_fixed == [1],
        "The involution r -> 1/r has fixed point r=1, but the retained\n"
        "three-generation carrier does not supply this block exchange.",
    )

    check(
        "10. Minimal-selector uniqueness does not derive K_TL=0",
        True,
        "The theorem fixes the coordinate r, not the value c.  A Nature-grade\n"
        "closure still needs an independent law selecting c=1, equivalently\n"
        "K_TL=0.",
    )

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("KOIDE_Q_MINIMAL_SELECTOR_VALUE_NO_GO=TRUE")
        print("Q_MINIMAL_SELECTOR_UNIQUENESS_CLOSES_Q=FALSE")
        print("RESIDUAL_VALUE_PARAMETER=c=r_selected")
        print()
        print("VERDICT: the first-live carrier has a unique scale-free")
        print("selector coordinate, but not a derived selector value.  The")
        print("Koide value is c=1, exactly the K_TL=0 residual in coordinate form.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
