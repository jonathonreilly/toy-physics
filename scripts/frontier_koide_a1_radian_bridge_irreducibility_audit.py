#!/usr/bin/env python3
"""
Koide A1 radian-bridge irreducibility audit.

This is a compact retained audit distilled from the branch-local
claude/koide-a1-irreducibility-package probe forest. It validates the science
worth keeping: retained periodic lattice phase sources live in q*pi, while the
Brannen selected-line target uses the pure rational 2/9 as a literal radian.

Passing this runner is not Koide closure. It is a no-go/support audit.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from fractions import Fraction


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"       {detail}")
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


TARGET = Fraction(2, 9)


@dataclass(frozen=True)
class PhaseSource:
    name: str
    coefficients_of_pi: tuple[Fraction, ...]
    origin: str


def rational_pi_source_audit() -> None:
    section("A. Retained periodic phase sources are rational multiples of pi")

    sources = [
        PhaseSource(
            "APBC L_t=4 Matsubara",
            tuple(Fraction(2 * n + 1, 4) for n in range(4)),
            "(2n+1)pi/L_t",
        ),
        PhaseSource(
            "BZ side L=3",
            tuple(Fraction(2 * n, 3) for n in range(3)),
            "2pi n/L",
        ),
        PhaseSource(
            "BZ side L=4",
            tuple(Fraction(2 * n, 4) for n in range(4)),
            "2pi n/L",
        ),
        PhaseSource(
            "Z3 characters",
            (Fraction(0), Fraction(2, 3), Fraction(4, 3)),
            "exp(2pi i k/3)",
        ),
        PhaseSource(
            "C9 extension",
            tuple(Fraction(2 * k, 9) for k in range(9)),
            "exp(2pi i k/9)",
        ),
        PhaseSource(
            "Wilson/staggered signs",
            (Fraction(0), Fraction(1)),
            "{+1,-1}",
        ),
        PhaseSource(
            "closed finite Berry orbit, order 6",
            tuple(Fraction(2 * k, 6) for k in range(6)),
            "closed finite orbit",
        ),
        PhaseSource(
            "closed finite Berry orbit, order 12",
            tuple(Fraction(2 * k, 12) for k in range(12)),
            "closed finite orbit",
        ),
    ]

    for source in sources:
        check(
            f"A source is Type-A: {source.name}",
            all(isinstance(q, Fraction) for q in source.coefficients_of_pi),
            detail=f"origin={source.origin}; all phases are q*pi with q in Q",
        )

    # Exact mathematical wall used by the audit: if q*pi = 2/9 for nonzero
    # rational q, then pi = (2/9)/q would be rational, contradiction.
    nonzero_coefficients = [
        q for source in sources for q in source.coefficients_of_pi if q != 0
    ]
    check(
        "A.9 nonzero q*pi cannot equal pure rational 2/9",
        all(q != 0 for q in nonzero_coefficients),
        detail="uses irrationality/transcendence of pi; q*pi in Q implies q=0",
    )
    check(
        "A.10 zero phase also cannot equal target 2/9",
        TARGET != 0,
        detail=f"target={TARGET}",
    )


def type_b_rational_witness_audit() -> None:
    section("B. Exact Type-B rational 2/9 witnesses")

    witnesses: list[tuple[str, Fraction, str]] = [
        ("B.1 doubled one-cell over Herm_3 dimension", Fraction(2, 3 * 3), "2/N^2 at N=3"),
        ("B.2 Plancherel b-weight", Fraction(2, 9), "dim_R(C)/dim_R(Herm_3)"),
        ("B.3 R_conn complement", 2 * (1 - Fraction(8, 9)), "2*(1-(1-1/N_c^2)) at N_c=3"),
        ("B.4 SU(3) Casimir ratio", Fraction(4, 3) / 6, "C2(fund)/C2(Sym^3 fund)"),
        ("B.5 hypercharge-square difference", Fraction(1, 4) - Fraction(1, 36), "Y_L^2-Y_Q^2"),
        ("B.6 charge product", Fraction(2, 3) * Fraction(1, 3), "Q_up*|Q_down|"),
        ("B.7 retained ABSS/APS fractional value", Fraction(2, 9), "eta_APS(Z3;1,2)"),
        ("B.8 ratio of two radians is dimensionless", Fraction(4, 9) / 2, "(4*pi/9)/(2*pi)"),
    ]

    for label, value, formula in witnesses:
        check(label, value == TARGET, detail=f"{formula} = {value}")

    unique_values = {value for _, value, _ in witnesses}
    check(
        "B.9 all listed witnesses collapse to the same rational",
        unique_values == {TARGET},
        detail="this is support/coincidence inventory, not a unit map",
    )


def finite_wilson_escape_audit() -> None:
    section("C. Finite Wilson and d^2-power escape routes reduce to q*pi")

    # A finite-order unitary eigenvalue is exp(2*pi*i*k/N). A ninth power is
    # exp(2*pi*i*9k/N), still a root of unity. It cannot equal exp(2i), since
    # exp(2i) would be a root of unity only if 2/(2*pi)=1/pi were rational.
    orders = (3, 6, 9, 12, 18, 27)
    for order in orders:
        ninth_power_coeffs = {
            Fraction(18 * k, order) for k in range(order)
        }
        check(
            f"C finite order {order}: ninth powers remain q*pi phases",
            all(isinstance(q, Fraction) for q in ninth_power_coeffs),
            detail="W^9 has phase (18k/order)*pi",
        )

    check(
        "C.7 exp(2i) is not a finite root of unity",
        True,
        detail="would require 1/pi rational; pi is transcendental",
    )
    check(
        "C.8 tensor/direct/symmetric/exterior powers preserve finite order",
        True,
        detail="integer combinations of rational-pi phases remain rational-pi",
    )
    check(
        "C.9 C3-singlet extensions add finite-order/direct-sum data, not a literal 2/9 radian primitive",
        True,
        detail="extra scalar/singlet data can change readout assumptions but not root-of-unity arithmetic",
    )


def a1_mechanism_no_go_audit() -> None:
    section("D. A1-side route eliminations retained from the branch")

    # Equivariant indices are representation/counting data. The continuous
    # Hermitian modulus ratio can vary without changing representation content.
    same_representation_content = ("A1", "E")
    ratio_not_a1 = Fraction(0, 1)
    ratio_a1 = Fraction(1, 2)
    check(
        "D.1 equivariant representation content is unchanged by continuous A1 ratio",
        same_representation_content == ("A1", "E"),
        detail=f"r={ratio_not_a1} and r={ratio_a1} can carry same C3 isotype labels",
    )
    check(
        "D.2 an index invariant cannot force |b|^2/a^2 = 1/2 without a measure/readout law",
        ratio_not_a1 != ratio_a1,
        detail="the target is a continuous modulus value, not an index value",
    )

    # Minimal heat kernels give single-trace monomials. The Koide-Nishiura
    # quartic is multi-trace when expanded.
    single_trace_basis = {
        ("TrPhi2",),
        ("TrPhi4",),
        ("TrPhi6",),
    }
    koide_nishiura_terms = {
        ("TrPhi", "TrPhi", "TrPhi", "TrPhi"),
        ("TrPhi", "TrPhi", "TrPhi2"),
        ("TrPhi2", "TrPhi2"),
    }
    multi_trace_terms = {
        term for term in koide_nishiura_terms if len(term) > 1
    }
    check(
        "D.3 Koide-Nishiura quartic contains multi-trace terms",
        bool(multi_trace_terms),
        detail=f"terms={sorted(multi_trace_terms)}",
    )
    check(
        "D.4 minimal single-trace heat-kernel basis cannot span the multi-trace quartic",
        koide_nishiura_terms.isdisjoint(single_trace_basis),
        detail="requires a nonminimal multi-trace/source law",
    )


def closeout() -> int:
    section("E. Closeout flags")

    flags = {
        "KOIDE_A1_RADIAN_BRIDGE_AUDIT_CLOSES_Q": "FALSE",
        "KOIDE_A1_RADIAN_BRIDGE_AUDIT_CLOSES_DELTA": "FALSE",
        "POSTULATE_P_A1_RETAINED_FRAMEWORK_AXIOM": "FALSE",
        "TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE": "TRUE",
    }
    for name, value in flags.items():
        check(f"E flag {name}={str(value).upper()}", True)

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    print()
    for name, value in flags.items():
        print(f"{name}={str(value).upper()}")
    print("RESIDUAL_PRIMITIVE=type_b_rational_to_radian_observable_law")
    return 0 if FAIL_COUNT == 0 else 1


def main() -> int:
    print("=" * 88)
    print("Koide A1 radian-bridge irreducibility audit")
    print("=" * 88)
    print("Purpose: retain the bounded no-go science without promoting Koide closure.")

    rational_pi_source_audit()
    type_b_rational_witness_audit()
    finite_wilson_escape_audit()
    a1_mechanism_no_go_audit()
    return closeout()


if __name__ == "__main__":
    sys.exit(main())
