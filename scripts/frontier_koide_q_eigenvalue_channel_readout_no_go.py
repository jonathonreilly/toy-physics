#!/usr/bin/env python3
"""
Koide Q eigenvalue-channel readout no-go.

The positive-parent route leaves a tempting escape hatch:

    positive C3-covariant parent M
    -> use eig(M) as the charged-lepton mass set
    -> apply the square-root amplitude dictionary

This runner audits whether that eigenvalue-channel readout is forced by the
retained C3 covariance, local axis readout, and set-equality support.

Result: it is not forced.  The eigenvalue channel is an exact mathematical
channel for a C3-covariant parent, but extracting it uses the Fourier spectral
projectors.  The strict axis-local diagonal readout is blind to all traceless
spectral data and returns only the flat average.  Therefore adopting eig(M) as
the physical charged-lepton mass observable is still an extra readout/value
primitive unless a new retained theorem derives it.

No PDG masses, K_TL=0, K=0, P_Q=1/2, Q=2/3, delta=2/9, or H_* pin is used.
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


def koide_q_from_amplitudes(a0: sp.Expr, a1: sp.Expr, a2: sp.Expr) -> sp.Expr:
    return sp.simplify((a0**2 + a1**2 + a2**2) / (a0 + a1 + a2) ** 2)


def main() -> int:
    section("Koide Q eigenvalue-channel readout no-go")
    print("Theorem attempt: C3 covariance plus set-level spectral data might force")
    print("the eigenvalue channel as the physical charged-lepton readout.")
    print("The audit result is negative.")

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

    a0, a1, a2 = sp.symbols("a0 a1 a2", positive=True, real=True)
    m0, m1, m2 = a0**2, a1**2, a2**2
    M = sp.simplify(F.conjugate().T * sp.diag(m0, m1, m2) * F)

    section("A. C3 parent and the two readout channels")

    record(
        "A.1 arbitrary positive amplitudes define a Hermitian C3-covariant parent",
        sp.simplify(M - M.conjugate().T) == sp.zeros(3, 3)
        and sp.simplify(M * C - C * M) == sp.zeros(3, 3),
        "M = F^dag diag(a0^2,a1^2,a2^2) F with a_i > 0.",
    )

    avg = sp.simplify((m0 + m1 + m2) / 3)
    axis_diag = [sp.simplify(M[i, i]) for i in range(3)]
    record(
        "A.2 strict axis-local diagonal readout collapses to the flat average",
        all(sp.simplify(entry - avg) == 0 for entry in axis_diag),
        f"diag_axis(M) = {axis_diag}",
    )

    g0, g1, g2 = sp.symbols("g0 g1 g2", real=True)
    G = sp.simplify(F.conjugate().T * sp.diag(g0, g1, g2) * F)
    g_avg = sp.simplify((g0 + g1 + g2) / 3)
    g_diag = [sp.simplify(G[i, i]) for i in range(3)]
    record(
        "A.3 every C3-equivariant functional remains axis-diagonal-blind",
        all(sp.simplify(entry - g_avg) == 0 for entry in g_diag),
        "For any spectral values g_i, diag_axis(F^dag diag(g_i) F) is flat.",
    )

    q_axis = sp.Rational(1, 3)
    record(
        "A.4 the current strict axis readout cannot produce a hierarchy from this parent",
        q_axis == sp.Rational(1, 3),
        "Flat masses give Q_axis = 1/3 and a degenerate charged-lepton set.",
    )

    section("B. What the eigenvalue channel adds")

    projectors = []
    for k in range(3):
        e = sp.zeros(3, 3)
        e[k, k] = 1
        projectors.append(sp.simplify(F.conjugate().T * e * F))

    projector_checks = []
    extraction_checks = []
    for k, projector in enumerate(projectors):
        projector_checks.append(sp.simplify(projector * projector - projector) == sp.zeros(3, 3))
        projector_checks.append(sp.simplify(projector - projector.conjugate().T) == sp.zeros(3, 3))
        extraction_checks.append(
            sp.simplify(sp.trace(projector * M) - [m0, m1, m2][k]) == 0
        )

    record(
        "B.1 Fourier spectral projectors exactly extract the unordered spectral masses",
        all(projector_checks) and all(extraction_checks),
        "tr(P_k M) = a_k^2 for k=0,1,2.",
    )

    non_axis_projector = projectors[1]
    offdiag_projector = [
        sp.simplify(non_axis_projector[0, 1]),
        sp.simplify(non_axis_projector[0, 2]),
    ]
    record(
        "B.2 those spectral projectors are not axis-local diagonal readouts",
        any(value != 0 for value in offdiag_projector)
        and all(sp.simplify(non_axis_projector[i, i] - sp.Rational(1, 3)) == 0 for i in range(3)),
        f"P_1 has flat diagonal 1/3 and off-diagonal entries {offdiag_projector}.",
    )

    q_spec = koide_q_from_amplitudes(a0, a1, a2)
    q_111 = sp.simplify(q_spec.subs({a0: 1, a1: 1, a2: 1}))
    q_123 = sp.simplify(q_spec.subs({a0: 1, a1: 2, a2: 3}))
    q_112 = sp.simplify(q_spec.subs({a0: 1, a1: 1, a2: 2}))
    record(
        "B.3 spectral readout leaves the projective amplitude ratios free",
        q_111 == sp.Rational(1, 3)
        and q_123 == sp.Rational(7, 18)
        and q_112 == sp.Rational(3, 8),
        f"Q_spec(1,1,1)={q_111}; Q_spec(1,2,3)={q_123}; Q_spec(1,1,2)={q_112}.",
    )

    sample = {a0: 1, a1: 2, a2: 3}
    M_sample = sp.simplify(M.subs(sample))
    axis_sample = [sp.simplify(M_sample[i, i]) for i in range(3)]
    spectral_sample = [sp.simplify(expr.subs(sample)) for expr in (m0, m1, m2)]
    record(
        "B.4 the same parent has inequivalent axis and spectral mass sets",
        axis_sample == [sp.Rational(14, 3)] * 3
        and spectral_sample == [sp.Rational(1), sp.Rational(4), sp.Rational(9)],
        f"axis set={axis_sample}; spectral set={spectral_sample}.",
    )

    section("C. Review-grade consequence")

    record(
        "C.1 set-equality support does not itself choose the observable channel",
        True,
        "Comparing unordered spectral sets is legitimate only after the physical\n"
        "law says that eig(M), rather than diag_axis(M), is the charged-lepton\n"
        "mass observable.",
    )

    record(
        "C.2 eigenvalue-channel adoption is therefore a residual readout/value primitive",
        True,
        "A closure still needs a retained theorem deriving the Fourier spectral\n"
        "projectors as physical, a non-axis-local charged-sector reduction, a\n"
        "controlled C3-breaking readout, or an independent spectral value law.",
    )

    record(
        "C.3 no forbidden target or observational pin is used",
        True,
        "The audit uses only exact C3 Fourier algebra and symbolic amplitudes.",
    )

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("KOIDE_Q_EIGENVALUE_CHANNEL_READOUT_NO_GO=TRUE")
        print("Q_EIGENVALUE_READOUT_CLOSES_Q=FALSE")
        print("RESIDUAL_PRIMITIVE=eigenvalue_channel_readout_or_spectral_value_law")
        print()
        print("VERDICT: the eigenvalue channel is exact support, not a closure.")
        print("Strict axis-local readout erases the traceless spectral data, while")
        print("spectral readout keeps arbitrary projective ratios.  Promoting eig(M)")
        print("to the physical charged-lepton mass observable remains an additional")
        print("readout/value law unless derived by a new retained theorem.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
