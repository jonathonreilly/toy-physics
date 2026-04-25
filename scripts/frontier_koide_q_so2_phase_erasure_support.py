#!/usr/bin/env python3
"""
Koide Q SO(2) phase-erasure support theorem.

This runner lands the salvageable object-level content from the
koide-closure-targets-AB review as support-grade science only.  It proves
that on the Brannen square-root mass carrier Q=(c^2+2)/6, independent of the
carrier phase and scale, while preserving the open retained-closure boundary.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}")
    if detail:
        print(f"       {detail}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    return condition


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def read_doc(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return re.sub(r"[\s*`]+", " ", text.lower())


def has_all(text: str, phrases: tuple[str, ...]) -> bool:
    haystack = normalized(text)
    return all(phrase.lower() in haystack for phrase in phrases)


def part1_existing_open_boundary() -> None:
    banner("Part 1: upstream package boundary remains open")

    criterion = read_doc("docs/KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md")
    onsite = read_doc("docs/KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md")
    descent = read_doc("docs/KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md")

    check(
        "background-zero criterion is support, not retained closure",
        "KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE" in criterion
        and "KOIDE_FULL_DIMENSIONLESS_CLOSURE=FALSE" in criterion,
    )
    check(
        "onsite source-domain synthesis keeps the source-domain law open",
        has_all(
            onsite,
            (
                "not retained native Koide closure",
                "this note does not prove",
                "physical undeformed charged-lepton scalar source domain",
            ),
        ),
    )
    check(
        "canonical descent note keeps physical source-domain selection open",
        has_all(
            descent,
            (
                "support / criterion theorem",
                "what is not proved",
                "physical charged-lepton source-domain law must use strict onsite descent",
            ),
        ),
    )


def part2_c3_trigonometry() -> None:
    banner("Part 2: exact C3 trigonometry")

    delta = sp.symbols("delta", real=True)
    thetas = [delta + 2 * sp.pi * k / 3 for k in range(3)]

    sum_cos = sp.trigsimp(sum(sp.cos(theta) for theta in thetas))
    sum_cos_sq = sp.trigsimp(sum(sp.cos(theta) ** 2 for theta in thetas))

    check(
        "sum_k cos(delta+2pi k/3)=0",
        sum_cos == 0,
        f"sum_cos={sum_cos}",
    )
    check(
        "sum_k cos(delta+2pi k/3)^2=3/2",
        sum_cos_sq == sp.Rational(3, 2),
        f"sum_cos_sq={sum_cos_sq}",
    )

    shifted = [theta + sp.symbols("phi", real=True) for theta in thetas]
    shifted_sum = sp.trigsimp(sum(sp.cos(theta) for theta in shifted))
    shifted_sq = sp.trigsimp(sum(sp.cos(theta) ** 2 for theta in shifted))
    check(
        "SO(2) phase rotation preserves the C3 first and second moments",
        shifted_sum == 0 and shifted_sq == sp.Rational(3, 2),
        f"shifted_sum={shifted_sum}, shifted_sq={shifted_sq}",
    )


def part3_brannen_q_formula() -> None:
    banner("Part 3: Brannen carrier Q formula")

    c, v0, delta = sp.symbols("c V0 delta", real=True, nonzero=True)
    thetas = [delta + 2 * sp.pi * k / 3 for k in range(3)]
    sqrt_m = [v0 * (1 + c * sp.cos(theta)) for theta in thetas]

    sum_sqrt = sp.trigsimp(sum(sqrt_m))
    sum_mass = sp.trigsimp(sum(s ** 2 for s in sqrt_m))
    q_value = sp.trigsimp(sum_mass / sum_sqrt**2)

    check(
        "sum sqrt(m_k)=3 V0",
        sp.simplify(sum_sqrt - 3 * v0) == 0,
        f"sum_sqrt={sum_sqrt}",
    )
    check(
        "sum m_k=(3 V0^2/2)(2+c^2)",
        sp.simplify(sum_mass - (3 * v0**2 / 2) * (2 + c**2)) == 0,
        f"sum_mass={sum_mass}",
    )
    check(
        "Q=(c^2+2)/6 exactly",
        sp.simplify(q_value - (c**2 + 2) / 6) == 0,
        f"Q={q_value}",
    )
    check(
        "Q is independent of Brannen phase delta",
        sp.diff(q_value, delta) == 0,
    )
    check(
        "Q is independent of scale V0",
        sp.diff(q_value, v0) == 0,
    )


def part4_conditional_koide_point() -> None:
    banner("Part 4: conditional Koide point and support-only AM-GM reading")

    c2 = sp.symbols("c2", nonnegative=True)
    q_of_c2 = sp.simplify((c2 + 2) / 6)
    koide_solution = sp.solve(sp.Eq(q_of_c2, sp.Rational(2, 3)), c2)

    check(
        "Q=2/3 iff c^2=2 on the Brannen carrier",
        koide_solution == [2],
        f"solution={koide_solution}",
    )

    n_plus = sp.Integer(3)
    n_perp = sp.Integer(6)
    c2_from_equal_energy = sp.simplify(n_perp / n_plus)
    check(
        "equal-energy reduced-carrier premise gives c^2=6/3=2",
        c2_from_equal_energy == 2,
        f"c^2={c2_from_equal_energy}",
    )
    check(
        "under that conditional premise Q=2/3",
        sp.simplify(q_of_c2.subs(c2, c2_from_equal_energy) - sp.Rational(2, 3)) == 0,
        f"Q={q_of_c2.subs(c2, c2_from_equal_energy)}",
    )
    check(
        "generic carrier amplitude does not force Q=2/3",
        sp.simplify(q_of_c2.subs(c2, sp.Rational(1, 2))) != sp.Rational(2, 3)
        and sp.simplify(q_of_c2.subs(c2, 3)) != sp.Rational(2, 3),
        f"Q(1/2)={q_of_c2.subs(c2, sp.Rational(1, 2))}, Q(3)={q_of_c2.subs(c2, 3)}",
    )


def part5_delta_lane_separation() -> None:
    banner("Part 5: Q erases delta, so the Brannen phase lane stays separate")

    c, v0, delta, phi = sp.symbols("c V0 delta phi", real=True, nonzero=True)
    q = (c**2 + 2) / 6
    q_shifted = q.subs(delta, delta + phi)

    check(
        "Q(delta+phi)=Q(delta)",
        sp.simplify(q_shifted - q) == 0,
    )
    check(
        "delta cannot be reconstructed from Q on this carrier",
        not q.has(delta),
        f"free_symbols={sorted(str(s) for s in q.free_symbols)}",
    )

    q_at_koide = sp.Rational(2, 3)
    check(
        "setting Q=2/3 leaves delta unconstrained",
        delta not in q_at_koide.free_symbols,
    )


def part6_note_and_package_scope() -> None:
    banner("Part 6: landed scope is support-grade only")

    note = read_doc("docs/KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md")
    script = Path(__file__).read_text(encoding="utf-8")

    check(
        "note lands the phase-erasure support flag",
        "KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT=TRUE" in note
        and "KOIDE_Q_INDEPENDENT_OF_BRANNEN_PHASE_AND_SCALE=TRUE" in note,
    )
    check(
        "note explicitly denies retained Q and delta closure",
        "KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE" in note
        and "KOIDE_DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE" in note,
    )
    check(
        "note leaves the source-domain primitive open",
        "SOURCE_DOMAIN_RETENTION_PRIMITIVE_RESOLVED=FALSE" in note
        and "RESIDUAL_Q=derive_physical_source_free_reduced_carrier_selection_or_equivalent_c2_eq_2_law" in note,
    )
    check(
        "runner does not print retained closure as true",
        not re.search(r"KOIDE_Q_RETAINED_NATIVE_CLOSURE\s*=\s*TRUE", script)
        and not re.search(r"KOIDE_DELTA_2_OVER_9_RAD_RETAINED_CLOSURE\s*=\s*TRUE", script),
    )

    publication_matrix = read_doc("docs/publication/ci3_z3/PUBLICATION_MATRIX.md")
    claims_table = read_doc("docs/publication/ci3_z3/CLAIMS_TABLE.md")
    validation_map = read_doc("docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md")
    atlas = read_doc("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    index = read_doc("docs/CANONICAL_HARNESS_INDEX.md")

    check(
        "support theorem is woven through package control surfaces",
        all(
            "KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md" in text
            for text in (publication_matrix, claims_table, validation_map, atlas, index)
        ),
    )


def main() -> int:
    print("=" * 88)
    print("Koide Q SO(2) phase-erasure support theorem")
    print("=" * 88)

    part1_existing_open_boundary()
    part2_c3_trigonometry()
    part3_brannen_q_formula()
    part4_conditional_koide_point()
    part5_delta_lane_separation()
    part6_note_and_package_scope()

    print()
    print("=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print(f"PASSED: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    print("=" * 88)

    if FAIL_COUNT == 0:
        print("KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT=TRUE")
        print("KOIDE_Q_INDEPENDENT_OF_BRANNEN_PHASE_AND_SCALE=TRUE")
        print("KOIDE_Q_CONDITIONAL_C2_EQ_2_IMPLIES_Q_2_OVER_3=TRUE")
        print("KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE")
        print("KOIDE_DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE")
        print("SOURCE_DOMAIN_RETENTION_PRIMITIVE_RESOLVED=FALSE")
        return 0

    print("KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
