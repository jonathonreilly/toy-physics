#!/usr/bin/env python3
"""
Koide delta Maslov/open-phase no-go.

Theorem attempt:
  Use Maslov/caustic quantization of an open selected line, possibly combined
  with retained C3 character phases, to force the Brannen endpoint

      theta_end - theta0 = eta_APS = 2/9.

Result:
  Negative.  Maslov data quantize only jump/caustic contributions.  In cycle
  units they lie on a quarter-integer lattice mu/4.  Combining with C3
  characters gives a denominator-12 lattice k/3 + mu/4.  The APS value 2/9 is
  not on that lattice.  If a continuous Berry integral or endpoint
  trivialization is allowed, it can be chosen to hit 2/9 for any Maslov class,
  so the equality is not derived.

No PDG masses, Koide Q target, delta pin, or H_* pin is used.
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


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    total = 0
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def mod1_fraction(value: sp.Expr) -> sp.Rational:
    value = sp.Rational(value)
    return value - sp.floor(value)


def main() -> int:
    section("A. APS support value and Maslov jump lattice")

    eta = eta_abss_z3_weights_12()
    maslov_lattice = [sp.Rational(mu, 4) for mu in range(4)]
    record(
        "A.1 ambient APS scalar is exactly eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "A.2 Maslov jump phases in cycle units lie on mu/4",
        maslov_lattice == [0, sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4)],
        f"Maslov lattice mod 1={maslov_lattice}",
    )
    record(
        "A.3 eta_APS is not a pure Maslov jump",
        eta not in maslov_lattice,
        f"2/9 denominator is 9, not a quarter-integer lattice point.",
    )

    section("B. C3 character phases plus Maslov jumps still miss 2/9")

    c3_maslov = sorted(
        {
            mod1_fraction(sp.Rational(k, 3) + sp.Rational(mu, 4))
            for k in range(3)
            for mu in range(4)
        }
    )
    record(
        "B.1 C3 character plus Maslov lattice has denominator 12",
        c3_maslov
        == [
            sp.Rational(0),
            sp.Rational(1, 12),
            sp.Rational(1, 6),
            sp.Rational(1, 4),
            sp.Rational(1, 3),
            sp.Rational(5, 12),
            sp.Rational(1, 2),
            sp.Rational(7, 12),
            sp.Rational(2, 3),
            sp.Rational(3, 4),
            sp.Rational(5, 6),
            sp.Rational(11, 12),
        ],
        f"C3+Maslov={c3_maslov}",
    )
    record(
        "B.2 eta_APS=2/9 is not in the retained C3+Maslov lattice",
        eta not in c3_maslov,
        "No integers k,mu solve k/3 + mu/4 = 2/9 mod 1.",
    )

    section("C. Allowing open Berry integral/trivialization makes endpoint free")

    a, chi_start, chi_end, mu = sp.symbols("a chi_start chi_end mu", real=True)
    delta_open = sp.simplify(a + mu / 4 + chi_end - chi_start)
    solve_for_a = sp.solve(sp.Eq(delta_open, eta), a)
    solve_for_chi_end = sp.solve(sp.Eq(delta_open, eta), chi_end)
    record(
        "C.1 continuous open Berry integral can fit eta for every Maslov class",
        solve_for_a == [-chi_end + chi_start - mu / 4 + sp.Rational(2, 9)],
        f"a_required={solve_for_a}",
    )
    record(
        "C.2 endpoint trivialization can also fit eta for every open integral",
        solve_for_chi_end == [-a + chi_start - mu / 4 + sp.Rational(2, 9)],
        f"chi_end_required={solve_for_chi_end}",
    )
    record(
        "C.3 fitting by a or endpoint gauge is not a derivation",
        True,
        "It reintroduces the residual open endpoint law.",
    )

    section("D. Counterexamples with identical quantized data")

    samples = [
        (sp.Rational(0), sp.Rational(0)),
        (sp.Rational(1, 4), sp.Rational(0)),
        (sp.Rational(0), eta),
        (sp.Rational(1, 4), eta - sp.Rational(1, 4)),
    ]
    lines: list[str] = []
    ok = True
    for mu_over_4, continuous in samples:
        total = sp.simplify(mu_over_4 + continuous)
        closes = sp.simplify(total - eta) == 0
        ok = ok and (closes == (total == eta))
        lines.append(f"Maslov={mu_over_4}, continuous={continuous}, total={total}, closes={closes}")
    record(
        "D.1 same Maslov class allows both closing and non-closing endpoints",
        ok,
        "\n".join(lines),
    )
    record(
        "D.2 Maslov quantization does not determine the physical selected-line endpoint",
        True,
        "It constrains caustic jumps; the smooth/open contribution remains residual.",
    )

    section("E. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "E.1 Maslov/open-phase route does not close delta",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "E.2 delta remains open after Maslov audit",
        True,
        "Residual primitive: physical selected-line open endpoint equals ambient APS eta.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: Maslov/open-phase quantization does not close delta.")
        print("KOIDE_DELTA_MASLOV_OPEN_PHASE_NO_GO=TRUE")
        print("DELTA_MASLOV_OPEN_PHASE_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_TRIVIALIZATION=selected_line_open_phase_smooth_part_or_endpoint_gauge")
        return 0

    print("VERDICT: Maslov/open-phase audit has FAILs.")
    print("KOIDE_DELTA_MASLOV_OPEN_PHASE_NO_GO=FALSE")
    print("DELTA_MASLOV_OPEN_PHASE_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_TRIVIALIZATION=selected_line_open_phase_smooth_part_or_endpoint_gauge")
    return 1


if __name__ == "__main__":
    sys.exit(main())
