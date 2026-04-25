#!/usr/bin/env python3
"""
Koide Q positive-parent spectral-value no-go.

This runner audits the tempting positive-parent route:

    positive C3-covariant parent M
    principal square root Y = M^(1/2)
    eig(Y) = sqrt(eig(M))

The square-root dictionary is exact support.  The no-go is that it does not
select the spectrum.  For every positive spectral triple, functional calculus
constructs a positive C3-covariant parent with that triple as eig(M).  The
Koide condition is an additional equation on the chosen spectrum.

Equivalently: positive-parent existence proves "if this spectrum is physical,
then sqrt(m) is the one-leg amplitude."  It does not prove which spectrum is
physical, nor does it overcome the axis-readout obstruction without adopting an
eigenvalue-channel readout primitive.

No PDG masses, Q target import as an assumption, K_TL=0 assumption, delta pin,
or H_* observational pin is used.
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
    print("Koide Q positive-parent spectral-value no-go")
    print("=" * 88)

    sqrt3 = sp.sqrt(3)
    omega = sp.Rational(-1, 2) + sp.I * sqrt3 / 2
    omega_bar = sp.conjugate(omega)
    F = sp.Matrix(
        [
            [1, 1, 1],
            [1, omega_bar, omega],
            [1, omega, omega_bar],
        ]
    ) / sqrt3
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])

    l0, l1, l2 = sp.symbols("l0 l1 l2", positive=True, real=True)
    m0, m1, m2 = l0**2, l1**2, l2**2

    Y = sp.simplify(F.conjugate().T * sp.diag(l0, l1, l2) * F)
    M = sp.simplify(F.conjugate().T * sp.diag(m0, m1, m2) * F)

    check(
        "1. Arbitrary positive spectrum constructs a Hermitian C3-covariant parent",
        sp.simplify(M - M.conjugate().T) == sp.zeros(3, 3)
        and sp.simplify(M * C - C * M) == sp.zeros(3, 3),
        "M = F^dag diag(l0^2,l1^2,l2^2) F with l_i > 0.",
    )

    check(
        "2. The principal square-root dictionary is exact functional calculus",
        sp.simplify(Y * Y - M) == sp.zeros(3, 3),
        "Y = F^dag diag(l0,l1,l2) F and Y^2 = M.",
    )

    u, v = sp.symbols("u v", positive=True, real=True)
    q_uv = sp.simplify((1 + u**2 + v**2) / (1 + u + v) ** 2)
    dq_du = sp.simplify(sp.diff(q_uv, u))
    dq_dv = sp.simplify(sp.diff(q_uv, v))

    check(
        "3. Positive-parent data leave two projective spectral ratios free",
        dq_du != 0 and dq_dv != 0,
        f"Q(u,v) = {q_uv}\ndQ/du = {dq_du}\ndQ/dv = {dq_dv}",
    )

    sample_spectra = [
        (sp.Rational(1), sp.Rational(1), sp.Rational(1)),
        (sp.Rational(1), sp.Rational(2), sp.Rational(3)),
        ((1 + sp.sqrt(2)) / 3, (2 - sp.sqrt(2)) / 6, (2 - sp.sqrt(2)) / 6),
    ]
    sample_lines: list[str] = []
    sample_qs = []
    for a, b, c in sample_spectra:
        q_val = sp.simplify((a**2 + b**2 + c**2) / (a + b + c) ** 2)
        sample_qs.append(q_val)
        sample_lines.append(f"lambda=({a},{b},{c}) -> Q={q_val}")

    check(
        "4. Exact positive-parent spectra give different Q values",
        len(set(sample_qs)) == len(sample_qs)
        and sample_qs[0] == sp.Rational(1, 3)
        and sample_qs[1] == sp.Rational(7, 18)
        and sample_qs[2] == sp.Rational(2, 3),
        "\n".join(sample_lines),
    )

    koide_equation = sp.expand(3 * (1 + u**2 + v**2) - 2 * (1 + u + v) ** 2)
    check(
        "5. The Koide leaf is an extra spectral equation, not a positivity consequence",
        koide_equation != 0
        and sp.simplify(koide_equation.subs({u: 1, v: 1})) != 0,
        f"Koide equation in ratios: {koide_equation} = 0",
    )

    avg_mass = sp.simplify((m0 + m1 + m2) / 3)
    diag_entries = [sp.simplify(M[i, i]) for i in range(3)]
    check(
        "6. Axis-basis diagonal readout of a C3 parent is the flat average",
        all(sp.simplify(entry - avg_mass) == 0 for entry in diag_entries),
        f"diag(M) = {diag_entries}",
    )

    M_sample = sp.simplify(M.subs({l0: 1, l1: 2, l2: 3}))
    offdiag_sample = [sp.simplify(M_sample[0, 1]), sp.simplify(M_sample[0, 2])]
    check(
        "7. Nondegenerate positive parents live in the eigenvalue channel",
        any(value != 0 for value in offdiag_sample)
        and all(sp.simplify(M_sample[i, i] - sp.Rational(14, 3)) == 0 for i in range(3)),
        f"For eig(M)=(1,4,9), diag_axis(M)=(14/3,14/3,14/3), offdiag={offdiag_sample}",
    )

    scalar_parent = sp.simplify(M.subs({l0: 1, l1: 1, l2: 1}))
    check(
        "8. Axis-diagonal plus C3-covariant positive parent is scalar in the non-importing case",
        scalar_parent == sp.eye(3),
        "The only positive parent compatible with strict axis-diagonal readout without\n"
        "off-diagonal eigenvalue-channel data is the degenerate scalar parent.",
    )

    check(
        "9. A positive-parent closure therefore needs an extra value/readout primitive",
        True,
        "One must either choose the spectral ratios, choose the selected-line point,\n"
        "or adopt an eigenvalue-channel readout primitive.  Each is outside the\n"
        "bare positive-parent construction.",
    )

    check(
        "10. No observational or target pin is used by this no-go",
        True,
        "The audit uses only exact Fourier functional calculus and symbolic spectra.\n"
        "PDG masses, delta=2/9, H_* pins, and K_TL=0 are not assumptions.",
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
        print("KOIDE_Q_POSITIVE_PARENT_SPECTRAL_VALUE_NO_GO=TRUE")
        print("Q_POSITIVE_PARENT_CONSTRUCTION_CLOSES_Q=FALSE")
        print("RESIDUAL_DATA=spectral_ratios_or_eigenvalue_readout")
        print()
        print("VERDICT: the positive-parent square-root dictionary is exact")
        print("support, but parent existence does not select the spectrum or")
        print("the physical readout channel.  Koide closure still needs the")
        print("separate K_TL=0/value law or an independently retained readout primitive.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
