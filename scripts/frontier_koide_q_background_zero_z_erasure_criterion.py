#!/usr/bin/env python3
"""
Koide Q background-zero / Z-erasure criterion theorem.

This runner validates the exact algebraic criterion landed from the
high-impact-retain-native review without promoting it to retained native
Koide closure.  It proves that, on the admitted normalized reduced carrier,
zero source, Z-erasure, Y=I_2, and Q=2/3 are equivalent, while the physical
selection of that source-free carrier remains open.
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


def has_phrase(text: str, phrase: str) -> bool:
    return phrase.lower() in text.lower()


def has_all(text: str, phrases: tuple[str, ...]) -> bool:
    normalized = re.sub(r"[\s*`]+", " ", text.lower())
    return all(phrase.lower() in normalized for phrase in phrases)


def part1_upstream_scope() -> None:
    banner("Part 1: upstream support notes keep the bridge open")

    reduced = read_doc("docs/KOIDE_Q_REDUCED_OBSERVABLE_RESTRICTION_THEOREM_2026-04-22.md")
    no_hidden = read_doc("docs/KOIDE_Q_NO_HIDDEN_SOURCE_AUDIT_2026-04-22.md")
    normalized = read_doc("docs/KOIDE_Q_NORMALIZED_SECOND_ORDER_EFFECTIVE_ACTION_THEOREM_2026-04-22.md")

    check(
        "reduced-carrier note is explicitly support, not closure",
        has_phrase(reduced, "not a closure theorem"),
    )
    check(
        "reduced-carrier note keeps physical carrier identification open",
        has_all(
            reduced,
            (
                "does not prove that the physical charged-lepton observable principle must",
                "reduced two-generator block algebra",
            ),
        ),
    )
    check(
        "no-hidden-source audit is explicitly support, not closure",
        has_all(no_hidden, ("not a closure theorem",)),
    )
    check(
        "no-hidden-source audit keeps physical source-freeness open",
        has_all(no_hidden, ("does not yet prove", "source-free")),
    )
    check(
        "normalized effective-action note keeps selector source-freeness open",
        has_phrase(normalized, "does not prove from retained charged-lepton physics")
        and has_phrase(normalized, "source-free"),
    )


def part2_source_response_algebra() -> None:
    banner("Part 2: exact reduced source-response algebra")

    kp, kperp = sp.symbols("k_plus k_perp", real=True)
    w_red = sp.log(1 + kp) + sp.log(1 + kperp)
    y_plus = sp.diff(w_red, kp)
    y_perp = sp.diff(w_red, kperp)

    check(
        "dW_red/dK gives Y = diag(1/(1+k_+), 1/(1+k_perp))",
        sp.simplify(y_plus - 1 / (1 + kp)) == 0
        and sp.simplify(y_perp - 1 / (1 + kperp)) == 0,
        f"Y=diag({y_plus}, {y_perp})",
    )

    yp, yq = sp.symbols("y_plus y_perp", positive=True)
    k_from_y = (sp.simplify(1 / yp - 1), sp.simplify(1 / yq - 1))
    check(
        "inverting the response gives K = Y^(-1) - I",
        sp.simplify(k_from_y[0] - (1 / yp - 1)) == 0
        and sp.simplify(k_from_y[1] - (1 / yq - 1)) == 0,
        f"K=diag({k_from_y[0]}, {k_from_y[1]})",
    )

    z = sp.symbols("z", real=True)
    y_z = (1 + z, 1 - z)
    check(
        "Y_Z(z)=diag(1+z,1-z) has fixed trace 2",
        sp.simplify(y_z[0] + y_z[1] - 2) == 0,
    )

    z_expectation = sp.simplify((y_z[0] - y_z[1]) / (y_z[0] + y_z[1]))
    check(
        "normalized Z expectation equals z",
        sp.simplify(z_expectation - z) == 0,
        f"<Z>={z_expectation}",
    )

    k_z = (sp.simplify(1 / (1 + z) - 1), sp.simplify(1 / (1 - z) - 1))
    check(
        "dual source for Y_Z is K_Z=diag(-z/(1+z), z/(1-z))",
        sp.simplify(k_z[0] + z / (1 + z)) == 0
        and sp.simplify(k_z[1] - z / (1 - z)) == 0,
        f"K_Z=diag({k_z[0]}, {k_z[1]})",
    )

    zero_source_solution = sp.solve([sp.Eq(k_z[0], 0), sp.Eq(k_z[1], 0)], [z], dict=True)
    check(
        "K_Z=0 iff z=0",
        zero_source_solution == [{z: 0}],
        f"solution={zero_source_solution}",
    )

    z_erasure_solution = sp.solve(sp.Eq(z_expectation, 0), z)
    check(
        "Z-erasure <Z>=0 iff z=0",
        z_erasure_solution == [0],
        f"solution={z_erasure_solution}",
    )


def part3_q_equivalence() -> None:
    banner("Part 3: exact Q equivalence")

    z, q = sp.symbols("z q", real=True)
    q_z = sp.simplify((1 + (1 - z) / (1 + z)) / 3)

    check(
        "Q(z) simplifies to 2/(3(1+z))",
        sp.simplify(q_z - 2 / (3 * (1 + z))) == 0,
        f"Q(z)={q_z}",
    )
    check(
        "Z-erasure gives Q=2/3",
        sp.simplify(q_z.subs(z, 0) - sp.Rational(2, 3)) == 0,
        f"Q(0)={q_z.subs(z, 0)}",
    )

    z_for_koide = sp.solve(sp.Eq(q_z, sp.Rational(2, 3)), z)
    check(
        "Q=2/3 iff z=0",
        z_for_koide == [0],
        f"solution={z_for_koide}",
    )

    z_inverse = sp.solve(sp.Eq(q, q_z), z)
    check(
        "the inverse selector map is z(Q)=2/(3Q)-1",
        len(z_inverse) == 1 and sp.simplify(z_inverse[0] - (2 / (3 * q) - 1)) == 0,
        f"z(Q)={z_inverse[0]}",
    )

    dq_dz = sp.diff(q_z, z)
    check(
        "Q is monotone on the physical open interval -1<z<1",
        sp.simplify(dq_dz + 2 / (3 * (1 + z) ** 2)) == 0,
        f"dQ/dz={dq_dz}",
    )

    q_pos = sp.simplify(q_z.subs(z, sp.Rational(1, 4)))
    q_neg = sp.simplify(q_z.subs(z, sp.Rational(-1, 4)))
    check(
        "nonzero positive and negative Z sources move Q away from 2/3",
        q_pos != sp.Rational(2, 3)
        and q_neg != sp.Rational(2, 3)
        and q_pos != q_neg,
        f"Q(1/4)={q_pos}, Q(-1/4)={q_neg}",
    )


def part4_hidden_source_reconstruction() -> None:
    banner("Part 4: nonzero Z is hidden selector data")

    z, kp, kperp = sp.symbols("z k_plus k_perp", real=True)
    k_z_plus = sp.simplify(-z / (1 + z))
    k_z_perp = sp.simplify(z / (1 - z))

    z_from_kp = sp.solve(sp.Eq(kp, k_z_plus), z)
    z_from_kperp = sp.solve(sp.Eq(kperp, k_z_perp), z)
    check(
        "either reduced source component reconstructs z",
        len(z_from_kp) == 1
        and sp.simplify(z_from_kp[0] + kp / (kp + 1)) == 0
        and len(z_from_kperp) == 1
        and sp.simplify(z_from_kperp[0] - kperp / (1 + kperp)) == 0,
        f"z(k_+)={z_from_kp[0]}, z(k_perp)={z_from_kperp[0]}",
    )

    q_from_kp = sp.simplify(2 / (3 * (1 + z_from_kp[0])))
    q_from_kperp = sp.simplify(2 / (3 * (1 + z_from_kperp[0])))
    check(
        "a nonzero reduced source reconstructs the chosen Q value",
        sp.simplify(q_from_kp - 2 * (1 + kp) / 3) == 0
        and sp.simplify(q_from_kperp - 2 * (1 + kperp) / (3 * (1 + 2 * kperp))) == 0,
        f"Q(k_+)={q_from_kp}, Q(k_perp)={q_from_kperp}",
    )

    example_z = sp.Rational(1, 5)
    k_example = (
        sp.simplify(k_z_plus.subs(z, example_z)),
        sp.simplify(k_z_perp.subs(z, example_z)),
    )
    q_example = sp.simplify(2 / (3 * (1 + example_z)))
    check(
        "explicit nonzero source example changes Q and is not datum-free",
        k_example != (0, 0) and q_example != sp.Rational(2, 3),
        f"z={example_z}, K={k_example}, Q={q_example}",
    )


def part5_note_scope() -> None:
    banner("Part 5: landed note preserves the open-bridge boundary")

    note = read_doc("docs/KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md")
    script = Path(__file__).read_text(encoding="utf-8")

    check(
        "note marks the criterion as support, not retained native closure",
        "KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION=TRUE" in note
        and "KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE" in note,
    )
    check(
        "note names the remaining Q residual as physical source-free carrier selection",
        "RESIDUAL_Q=derive_physical_source_free_reduced_carrier_selection" in note,
    )
    check(
        "runner does not print a positive retained-native Koide closeout flag",
        not re.search(r"KOIDE_Q_RETAINED_NATIVE_CLOSURE\s*=\s*TRUE", script),
    )
    check(
        "note does not claim delta or full dimensionless closure",
        "KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=FALSE" in note
        and "KOIDE_FULL_DIMENSIONLESS_CLOSURE=FALSE" in note,
    )


def main() -> int:
    print("=" * 88)
    print("Koide Q background-zero / Z-erasure criterion theorem")
    print("=" * 88)

    part1_upstream_scope()
    part2_source_response_algebra()
    part3_q_equivalence()
    part4_hidden_source_reconstruction()
    part5_note_scope()

    print()
    print("=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print(f"PASSED: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    print("=" * 88)

    if FAIL_COUNT == 0:
        print("KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION=TRUE")
        print("KOIDE_Q_SOURCE_FREE_CRITERION_SUPPORT=TRUE")
        print("KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE")
        print("KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=FALSE")
        print("KOIDE_FULL_DIMENSIONLESS_CLOSURE=FALSE")
        print("RESIDUAL_Q=derive_physical_source_free_reduced_carrier_selection")
        print("RESIDUAL_DELTA=derive_selected_line_local_boundary_source_and_based_endpoint_plus_Type_B_radian_readout")
        return 0

    print("KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
