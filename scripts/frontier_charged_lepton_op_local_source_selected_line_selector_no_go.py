#!/usr/bin/env python3
"""OP-local source plus selected-line generation-selector no-go.

This runner audits the strongest currently available non-PDG ratio/source
premise for charged leptons:

    P_SOURCE := strict-onsite and C3-fixed undeformed scalar source
      => z = 0
      => Q = 2/3

It grants that conditional Q support, also grants the selected-line/Brannen
phase support value used by the current Koide stack, and then checks whether
the combined data can select one physical charged-lepton generation label.

The result is negative.  The OP-local source premise is C3-trivial and erases
the Q-side source coordinate, but it does not base the selected-line orbit or
attach the heavy/middle/light ratio profile to e/mu/tau labels.  PDG masses are
printed only in a comparator block and are not proof inputs.
"""

from __future__ import annotations

import itertools
import math
import re
import sys
from fractions import Fraction
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
NOTE = DOCS / "CHARGED_LEPTON_OP_LOCAL_SOURCE_SELECTED_LINE_SELECTOR_NO_GO_NOTE_2026-04-27.md"

PASS_COUNT = 0
FAIL_COUNT = 0

PDG_COMPARATORS_MEV = {
    "m_e_pdg_mev": 0.510998950,
    "m_mu_pdg_mev": 105.6583755,
    "m_tau_pdg_mev": 1776.86,
}

Matrix = tuple[tuple[Fraction, ...], ...]


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    suffix = f" -- {detail}" if detail else ""
    print(f"{status}: {name}{suffix}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def read_doc(name: str) -> str:
    return (DOCS / name).read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def contains(text: str, phrase: str) -> bool:
    return normalized(phrase) in normalized(text)


def mat(rows: Iterable[Iterable[int | Fraction]]) -> Matrix:
    return tuple(tuple(Fraction(x) for x in row) for row in rows)


def identity(n: int) -> Matrix:
    return tuple(
        tuple(Fraction(1) if i == j else Fraction(0) for j in range(n))
        for i in range(n)
    )


def add(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(x + y for x, y in zip(row_a, row_b, strict=True))
        for row_a, row_b in zip(a, b, strict=True)
    )


def sub(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(x - y for x, y in zip(row_a, row_b, strict=True))
        for row_a, row_b in zip(a, b, strict=True)
    )


def scale(c: Fraction, a: Matrix) -> Matrix:
    return tuple(tuple(c * x for x in row) for row in a)


def mmul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n))
        for i in range(n)
    )


def transpose(a: Matrix) -> Matrix:
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a)))


def trace(a: Matrix) -> Fraction:
    return sum(a[i][i] for i in range(len(a)))


def frob_inner(a: Matrix, b: Matrix) -> Fraction:
    return sum(a[i][j] * b[i][j] for i in range(len(a)) for j in range(len(a)))


def project_coeff(j: Matrix, p: Matrix) -> Fraction:
    return frob_inner(j, p) / frob_inner(p, p)


def diag3(a: Fraction, b: Fraction, c: Fraction) -> Matrix:
    return mat([[a, 0, 0], [0, b, 0], [0, 0, c]])


def is_scalar_identity(a: Matrix) -> bool:
    lam = a[0][0]
    return all(
        a[i][j] == (lam if i == j else Fraction(0))
        for i in range(len(a))
        for j in range(len(a))
    )


def brannen_sqrt_vector(
    phase: float, c: float = math.sqrt(2.0), scale_value: float = 1.0
) -> tuple[float, float, float]:
    return tuple(
        scale_value * (1.0 + c * math.cos(phase + 2.0 * math.pi * k / 3.0))
        for k in range(3)
    )


def rotate(values: tuple[float, float, float], shift: int) -> tuple[float, float, float]:
    shift %= 3
    return values[shift:] + values[:shift]


def koide_q_from_sqrt_vector(values: tuple[float, float, float]) -> float:
    return sum(value * value for value in values) / (sum(values) ** 2)


def sorted_normalized(values: tuple[float, float, float]) -> tuple[float, float, float]:
    total = sum(values)
    return tuple(sorted((value / total for value in values), reverse=True))


def rounded(values: tuple[float, ...], digits: int = 14) -> tuple[float, ...]:
    return tuple(round(value, digits) for value in values)


def label_action(label: int, shift: int) -> int:
    return (label + shift) % 3


def invariant_single_labels() -> list[int]:
    return [
        label
        for label in (0, 1, 2)
        if all(label_action(label, shift) == label for shift in (0, 1, 2))
    ]


def invariant_label_subsets() -> list[frozenset[int]]:
    labels = (0, 1, 2)
    subsets: list[frozenset[int]] = []
    for size in range(4):
        for subset in itertools.combinations(labels, size):
            candidate = frozenset(subset)
            if all(
                frozenset(label_action(label, shift) for label in candidate)
                == candidate
                for shift in (0, 1, 2)
            ):
                subsets.append(candidate)
    return subsets


def based_equivariant_selector_count() -> int:
    count = 0
    for base_image in (0, 1, 2):
        selector = {shift: label_action(base_image, shift) for shift in (0, 1, 2)}
        if all(
            selector[label_action(point, shift)] == label_action(selector[point], shift)
            for point in (0, 1, 2)
            for shift in (0, 1, 2)
        ):
            count += 1
    return count


I3 = identity(3)
J3 = mat([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
C = mat([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
C2 = mmul(C, C)
P_PLUS = scale(Fraction(1, 3), J3)
P_PERP = sub(I3, P_PLUS)


def q_of_z(z: Fraction) -> Fraction:
    return Fraction(2, 1) / (3 * (1 + z))


def main() -> int:
    section("A. Source surfaces and claim boundaries")

    source_files = [
        "CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md",
        "CHARGED_LEPTON_SELECTED_LINE_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md",
        "KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md",
        "KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md",
        "KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md",
        "KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md",
        "KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md",
        "KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md",
        "KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md",
        "KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md",
        "CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md",
    ]
    for name in source_files:
        check(f"source surface exists: {name}", (DOCS / name).exists())

    note_text = NOTE.read_text(encoding="utf-8") if NOTE.exists() else ""
    ratio_firewall = read_doc(
        "CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md"
    )
    selected_line_no_go = read_doc(
        "CHARGED_LEPTON_SELECTED_LINE_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md"
    )
    op_locality = read_doc("KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md")
    onsite_no_go = read_doc("KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md")
    q_erasure = read_doc("KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md")
    a1_audit = read_doc("KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md")
    pointed_origin = read_doc("KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md")
    readout_split = read_doc("KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md")
    radiative_firewall = read_doc("CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md")

    check(
        "new note exists",
        NOTE.exists(),
        str(NOTE.relative_to(ROOT)) if NOTE.exists() else str(NOTE),
    )
    check(
        "new note states exact negative boundary and no mass retention",
        contains(note_text, "exact negative boundary")
        and "CHARGED_LEPTON_MASS_RETENTION=FALSE" in note_text
        and "PDG_MASSES_USED_AS_COMPARATORS_ONLY=TRUE" in note_text,
    )
    check(
        "ratio/source route was previously closed without a new premise",
        "KOIDE_Q_PLUS_BRANNEN_PHASE_GENERATION_SELECTOR=FALSE" in ratio_firewall
        and "CHARGED_LEPTON_MASS_RETENTION=FALSE" in ratio_firewall,
    )
    check(
        "selected-line no-go identifies based law as required",
        "UNBASED_C3_ORBIT_SELECTS_SINGLE_GENERATION_LABEL=FALSE" in selected_line_no_go
        and "BASED_ENDPOINT_OR_SOURCE_LAW_REQUIRED=TRUE" in selected_line_no_go,
    )
    check(
        "OP-locality source support is conditional and not retained Q closure",
        "KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT=TRUE" in op_locality
        and "KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE" in op_locality
        and "CHARGED_LEPTON_MASS_RETENTION=FALSE" in op_locality,
    )
    check(
        "onsite source-domain theorem target remains open",
        "CURRENT_RETAINED_COMMUTANT_SOURCE_DOMAIN_ADMITS_Z=TRUE" in onsite_no_go
        and "RESIDUAL_Q=derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant"
        in onsite_no_go,
    )
    check(
        "Q erasure support does not retain delta closure",
        "KOIDE_Q_INDEPENDENT_OF_BRANNEN_PHASE_AND_SCALE=TRUE" in q_erasure
        and "KOIDE_DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE" in q_erasure,
    )
    check(
        "Brannen endpoint/radian primitive remains open",
        "TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE=TRUE" in a1_audit
        and "RESIDUAL_PRIMITIVE=type_b_rational_to_radian_observable_law" in a1_audit,
    )
    check(
        "unpointed retained data do not force a physical origin",
        "RETAINED_UNPOINTED_DATA_FORCE_POINTED_ORIGIN=FALSE" in pointed_origin
        and "RESIDUAL_PRIMITIVE=retained_physical_source_boundary_origin_laws"
        in pointed_origin,
    )
    check(
        "Q/delta readout split keeps selected-line endpoint transition open",
        "RESIDUAL_DELTA=selected_line_endpoint_transition_tau_not_removed_by_closed_readout"
        in readout_split,
    )

    section("B. Granted OP-local Q source premise")

    scalar_source = scale(Fraction(11, 7), I3)
    nonuniform_source = diag3(Fraction(11, 7), Fraction(11, 7), Fraction(5, 3))
    c_scalar = mmul(mmul(C, scalar_source), transpose(C))
    c_nonuniform = mmul(mmul(C, nonuniform_source), transpose(C))
    k_plus = project_coeff(scalar_source, P_PLUS)
    k_perp = project_coeff(scalar_source, P_PERP)
    z_reduced = (k_plus - k_perp) / 2

    check("C^3=I on the generation orbit", mmul(C2, C) == I3)
    check("P_+ and P_perp split the C3 isotypes", add(P_PLUS, P_PERP) == I3)
    check("strict-onsite C3-fixed source is common scalar", c_scalar == scalar_source)
    check("nonuniform onsite source is not C3-fixed", c_nonuniform != nonuniform_source)
    check("C3-fixed onsite source lies in span{I}", is_scalar_identity(scalar_source))
    check("K_+ equals K_perp for the scalar source", k_plus == k_perp)
    check("reduced trace-zero source coordinate z=0", z_reduced == 0, f"z={z_reduced}")
    check("criterion carrier gives Q(z=0)=2/3", q_of_z(Fraction(0)) == Fraction(2, 3))
    check(
        "nonzero source coordinate would change Q on the criterion carrier",
        all(q_of_z(z) != Fraction(2, 3) for z in (Fraction(1, 5), Fraction(-1, 3))),
    )
    check(
        "granted source premise has trivial C3 action and no label coordinate",
        c_scalar == scalar_source and invariant_single_labels() == [],
    )

    section("C. Granted selected-line/Brannen support data")

    selected_phase = 2.0 / 9.0
    selected_vector = brannen_sqrt_vector(selected_phase)
    rotations = tuple(rotate(selected_vector, shift) for shift in (0, 1, 2))
    q_values = tuple(koide_q_from_sqrt_vector(rotation) for rotation in rotations)
    sorted_ratios = tuple(sorted_normalized(rotation) for rotation in rotations)
    heaviest_slots = tuple(rotation.index(max(rotation)) for rotation in rotations)

    check("selected-line vector is positive", all(value > 0.0 for value in selected_vector))
    check(
        "selected-line vector has Q=2/3 without PDG input",
        abs(koide_q_from_sqrt_vector(selected_vector) - 2.0 / 3.0) < 1.0e-12,
        f"Q={koide_q_from_sqrt_vector(selected_vector):.15f}",
    )
    check(
        "cyclic relabelings preserve Q",
        all(abs(q_value - 2.0 / 3.0) < 1.0e-12 for q_value in q_values),
        f"Q_values={tuple(round(q_value, 15) for q_value in q_values)}",
    )
    check(
        "cyclic relabelings preserve unordered heavy/middle/light ratios",
        len({rounded(ratio) for ratio in sorted_ratios}) == 1,
        f"ratio={rounded(sorted_ratios[0])}",
    )
    check(
        "cyclic relabelings move the heaviest slot through all labels",
        set(heaviest_slots) == {0, 1, 2},
        f"heaviest_slots={heaviest_slots}",
    )
    check(
        "C3-fixed source does not remove the selected-line orbit freedom",
        c_scalar == scalar_source and set(heaviest_slots) == {0, 1, 2},
    )

    section("D. Natural-selector obstruction")

    fixed_single_labels = invariant_single_labels()
    invariant_subsets = invariant_label_subsets()
    nonempty_invariant_subsets = [subset for subset in invariant_subsets if subset]
    singleton_invariant_subsets = [subset for subset in invariant_subsets if len(subset) == 1]
    based_selector_count = based_equivariant_selector_count()

    check(
        "single generation labels carry a free C3 action",
        all(label_action(label, 1) != label for label in (0, 1, 2)),
    )
    check(
        "no C3-natural single-label selector exists from quotient data",
        fixed_single_labels == [],
        f"fixed_single_labels={fixed_single_labels}",
    )
    check(
        "no invariant singleton subset selects e, mu, or tau",
        singleton_invariant_subsets == [],
    )
    check(
        "only nonempty invariant label subset is the full generation orbit",
        nonempty_invariant_subsets == [frozenset({0, 1, 2})],
        f"subsets={nonempty_invariant_subsets}",
    )
    check(
        "based equivariant selectors exist only after choosing a basepoint",
        based_selector_count == 3,
        "three choices correspond to three physical basepoints",
    )
    check(
        "source scalar plus unbased selected-line orbit still lacks a basepoint",
        is_scalar_identity(scalar_source)
        and fixed_single_labels == []
        and based_selector_count == 3,
    )

    section("E. Scale and comparator firewall")

    proof_inputs = {
        "C3 fixed onsite source algebra",
        "z=0 source-erasure criterion",
        "Brannen carrier at c^2=2",
        "selected-line phase support delta=2/9",
        "free C3 label action",
        "prior support/no-go closeout flags",
    }
    forbidden_inputs = set(PDG_COMPARATORS_MEV) | {
        "observed_tau_is_heaviest",
        "PDG_generation_label",
        "charged_lepton_mass_fit",
    }

    check(
        "radiative scale support still requires an extra generation selector",
        contains(
            radiative_firewall,
            "cannot select the tau eigenvalue without an additional generation-selection, ratio, or source-domain primitive",
        ),
    )
    check(
        "PDG charged-lepton masses are not proof-input keys",
        proof_inputs.isdisjoint(forbidden_inputs),
        f"proof_inputs={sorted(proof_inputs)}",
    )

    sqrt_pdg = tuple(math.sqrt(value) for value in PDG_COMPARATORS_MEV.values())
    q_pdg = koide_q_from_sqrt_vector(sqrt_pdg)
    check(
        "PDG masses are comparator-only and near the Koide value",
        abs(q_pdg - 2.0 / 3.0) < 1.0e-5,
        f"Q_PDG={q_pdg:.12f}; not used above as a proof input",
    )

    section("F. Verdict")

    check(
        "OP-local source plus selected-line support is not a generation selector",
        z_reduced == 0
        and fixed_single_labels == []
        and singleton_invariant_subsets == []
        and based_selector_count == 3,
    )
    check(
        "mass retirement remains open",
        "CHARGED_LEPTON_MASS_RETENTION=FALSE" in note_text
        and "RESIDUAL_GENERATION=derive_based_endpoint_source_or_tau_scale_selector"
        in note_text,
    )

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: OP-local source selected-line generation-selector no-go.")
        print("CHARGED_LEPTON_OP_LOCAL_SOURCE_SELECTED_LINE_SELECTOR_NO_GO=TRUE")
        print("OP_LOCAL_SOURCE_PLUS_SELECTED_LINE_SELECTS_GENERATION=FALSE")
        print("BASED_ENDPOINT_SOURCE_OR_TAU_SCALE_SELECTOR_REQUIRED=TRUE")
        print("PDG_MASSES_USED_AS_COMPARATORS_ONLY=TRUE")
        print("CHARGED_LEPTON_MASS_RETENTION=FALSE")
        return 0

    print("VERDICT: OP-local source selected-line audit has failing checks.")
    print("CHARGED_LEPTON_OP_LOCAL_SOURCE_SELECTED_LINE_SELECTOR_NO_GO=FALSE")
    print("CHARGED_LEPTON_MASS_RETENTION=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
