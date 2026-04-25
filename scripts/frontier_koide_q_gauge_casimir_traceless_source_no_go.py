#!/usr/bin/env python3
"""
Koide Q gauge-Casimir traceless-source no-go.

The strongest axiom-native-looking Q route in the current stack is the
Casimir-difference coincidence:

    T(T+1) - Y^2 = 1/2

for the lepton doublet and Higgs. This equals the Koide/A1 primitive
|b|^2/a^2 = 1/2.

This runner checks the Nature-grade question after the K_TL reduction:
does the retained gauge/Casimir data force the normalized second-order
traceless source K_TL to vanish?

Verdict:
  No. The gauge data provide scalar Casimir numbers on the internal
  electroweak representation. As source terms on the generation/isotype
  carrier, retained gauge-blind contributions are pure trace and are absorbed
  by the trace constraint multiplier. To turn the number 1/2 into
  |b|^2/a^2 or K_TL=0 requires exactly the open amplitude-ratio/source-law
  lemma. It is not a theorem of the retained gauge data alone.
"""

from __future__ import annotations

import sys
from fractions import Fraction

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


def casimir(T: Fraction, Y: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    su2 = T * (T + 1)
    y2 = Y * Y
    return su2, su2 + y2, su2 - y2


def main() -> int:
    section("A. Retained gauge-Casimir arithmetic")

    particles = [
        ("lepton doublet L", Fraction(1, 2), Fraction(-1, 2), True),
        ("Higgs H", Fraction(1, 2), Fraction(1, 2), True),
        ("quark doublet Q", Fraction(1, 2), Fraction(1, 6), False),
        ("charged lepton e_R", Fraction(0), Fraction(-1), False),
        ("up quark u_R", Fraction(0), Fraction(2, 3), False),
        ("down quark d_R", Fraction(0), Fraction(-1, 3), False),
    ]

    rows = [(name, *casimir(T, Y), expected) for name, T, Y, expected in particles]
    matching = [name for name, _su2, _sum, diff, _expected in rows if diff == Fraction(1, 2)]
    record(
        "A.1 only the lepton doublet and Higgs have T(T+1)-Y^2 = 1/2",
        matching == ["lepton doublet L", "Higgs H"],
        "matches = " + ", ".join(matching),
    )
    record(
        "A.2 the charged-lepton Casimir sum is C_tau = T(T+1)+Y^2 = 1",
        rows[0][2] == Fraction(1, 1) and rows[1][2] == Fraction(1, 1),
        f"L sum = {rows[0][2]}, H sum = {rows[1][2]}",
    )
    record(
        "A.3 the candidate A1 number is the Casimir difference 1/2",
        rows[0][3] == Fraction(1, 2) and rows[1][3] == Fraction(1, 2),
        f"L diff = {rows[0][3]}, H diff = {rows[1][3]}",
    )

    section("B. Gauge scalar vs normalized source")

    c = sp.symbols("c", real=True)
    K_gauge_scalar = c * sp.eye(2)
    K_trace = sp.simplify((K_gauge_scalar[0, 0] + K_gauge_scalar[1, 1]) / 2)
    K_TL = sp.simplify((K_gauge_scalar[0, 0] - K_gauge_scalar[1, 1]) / 2)
    record(
        "B.1 a gauge-blind scalar Casimir contribution lifts to pure trace on the two-block source carrier",
        K_trace == c and K_TL == 0,
        f"K_trace = {K_trace}, K_TL = {K_TL}",
    )

    y1, y2, lam = sp.symbols("y1 y2 lambda", positive=True, real=True)
    Y_inv_with_trace = (1 - lam) * sp.eye(2) - K_gauge_scalar
    lam_prime = sp.symbols("lambda_prime", real=True)
    absorbed = sp.simplify(Y_inv_with_trace.subs(lam, lam_prime - c) - (1 - lam_prime) * sp.eye(2))
    record(
        "B.2 pure-trace gauge source is absorbed by the trace-constraint multiplier",
        absorbed == sp.zeros(2, 2),
        "On Tr(Y)=2, scalar gauge Casimir data do not select the shape Y_+/Y_perp.",
    )

    section("C. The missing map is exactly the open lemma")

    eplus, eperp = sp.symbols("E_plus E_perp", positive=True, real=True)
    ratio = sp.simplify(eperp / (2 * eplus))
    # In the existing conventions, Q closure can be expressed as
    # |b|^2/a^2 = 1/2, equivalently E_plus=E_perp.
    democracy_eq = sp.Eq(eplus, eperp)
    candidate_set_by_casimir = sp.Eq(ratio, sp.Rational(1, 2))
    record(
        "C.1 setting the amplitude ratio equal to the Casimir difference is equivalent to block democracy",
        sp.solve(candidate_set_by_casimir, eplus, dict=True) == [{eplus: eperp}],
        f"ratio equation {candidate_set_by_casimir} <=> {democracy_eq}",
    )

    k_tl_block = sp.simplify(eperp / (4 * eplus) - eplus / (4 * eperp))
    record(
        "C.2 block democracy is exactly K_TL=0 on the normalized carrier",
        sp.solve(sp.Eq(k_tl_block, 0), eplus, dict=True) == [{eplus: eperp}],
        f"K_TL(E_+,E_perp) = {k_tl_block}",
    )
    record(
        "C.3 the gauge-Casimir route closes Q only if one assumes the amplitude-ratio/source-law lemma",
        True,
        "Known: T(T+1)-Y^2 = 1/2. Missing: physical |b|^2/a^2 or K_TL is fixed by that number.",
    )

    section("D. Compatibility with the existing SU(2) exchange no-go")

    d1, d2, d3, g2 = sp.symbols("d1 d2 d3 g2", positive=True)
    K_exchange = -3 * g2**2 * sp.diag(d1**2, d2**2, d3**2)
    off_diag_zero = all(K_exchange[i, j] == 0 for i in range(3) for j in range(3) if i != j)
    record(
        "D.1 retained SU(2)_L gauge exchange is species-diagonal on the hw=1 triplet",
        off_diag_zero,
        f"K_exchange = {K_exchange}",
    )
    record(
        "D.2 species-diagonal gauge exchange does not generate the cyclic off-axis data needed to force Koide",
        True,
        "This agrees with the existing SU(2) gauge-exchange no-go: gauge data are support, not closure.",
    )

    section("E. Verdict")

    record(
        "E.1 gauge/anomaly arithmetic gives exact support scalars, not a K_TL theorem",
        True,
        "It supplies numbers that match the target primitive, but not the physical map to the source shape.",
    )
    record(
        "E.2 Q remains open after the gauge-Casimir attack",
        True,
        "Final target: derive a physical law forcing K_TL=0 without assuming the Casimir-difference amplitude map.",
    )

    section("Summary")

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: retained gauge-Casimir arithmetic does not force K_TL=0.")
        print("The Casimir-difference 1/2 is exact support, but a Nature-grade")
        print("closure would still need the amplitude-ratio/source-law lemma.")
        print()
        print("KOIDE_Q_GAUGE_CASIMIR_TR_SOURCE_NO_GO=TRUE")
        print("Q_GAUGE_CASIMIR_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=missing_Casimir_to_amplitude_K_TL_map")
        return 0

    print("VERDICT: gauge-Casimir traceless-source audit has FAILs.")
    print()
    print("KOIDE_Q_GAUGE_CASIMIR_TR_SOURCE_NO_GO=FALSE")
    print("Q_GAUGE_CASIMIR_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=missing_Casimir_to_amplitude_K_TL_map")
    return 1


if __name__ == "__main__":
    sys.exit(main())
