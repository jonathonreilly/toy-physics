#!/usr/bin/env python3
"""Type-B radian readout generation-selector no-go for charged leptons.

This runner grants a stronger Brannen-side premise than the prior unbased
selected-line audits:

    P_RADIAN := the Type-B rational 2/9 is read as the physical Brannen
                selected-line phase delta = 2/9 rad.

It also grants the strongest current non-PDG Q-side support:

    P_SOURCE => z = 0 => Q = 2/3.

The question is whether those scalar/readout premises select one physical
charged-lepton generation label, and therefore allow the radiative scale support
to be assigned to tau, without PDG charged-lepton masses.

The answer is no.  A scalar radian readout is still C3-invariant quotient data.
The generation labels carry a free C3 action.  A natural selector from invariant
quotient data to one label would have to return a fixed label, and no such label
exists.  A based endpoint/source/generation law is still additional physical
data.
"""

from __future__ import annotations

import itertools
import math
import re
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
NOTE = DOCS / "CHARGED_LEPTON_TYPEB_RADIAN_READOUT_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md"

PASS_COUNT = 0
FAIL_COUNT = 0

PDG_COMPARATORS_MEV = {
    "m_e_pdg_mev": 0.510998950,
    "m_mu_pdg_mev": 105.6583755,
    "m_tau_pdg_mev": 1776.86,
}


@dataclass(frozen=True)
class ScalarReadoutData:
    """C3-invariant quotient data granted by the stronger-premise audit."""

    q: Fraction
    delta: Fraction
    source_z: Fraction
    unit_law: str


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


def label_action(label: int, shift: int) -> int:
    return (label + shift) % 3


def scalar_readout_action(data: ScalarReadoutData, shift: int) -> ScalarReadoutData:
    """Cyclic relabeling does not move scalar quotient/readout data."""

    if shift not in (0, 1, 2):
        raise ValueError("C3 shift must be 0, 1, or 2")
    return data


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


def quotient_to_label_natural_selectors(data: ScalarReadoutData) -> list[int]:
    """Candidate natural maps from a fixed quotient point to one label."""

    return [
        label
        for label in (0, 1, 2)
        if all(
            scalar_readout_action(data, shift) == data
            and label_action(label, shift) == label
            for shift in (0, 1, 2)
        )
    ]


def equivariant_maps_between_based_torsors() -> list[dict[int, int]]:
    """Equivariant maps from a based endpoint C3 torsor to label torsor."""

    maps: list[dict[int, int]] = []
    for base_image in (0, 1, 2):
        candidate = {point: label_action(base_image, point) for point in (0, 1, 2)}
        if all(
            candidate[label_action(point, shift)] == label_action(candidate[point], shift)
            for point in (0, 1, 2)
            for shift in (0, 1, 2)
        ):
            maps.append(candidate)
    return maps


def rotate(values: tuple[float, float, float], shift: int) -> tuple[float, float, float]:
    shift %= 3
    return values[shift:] + values[:shift]


def brannen_sqrt_vector(
    phase: float, c: float = math.sqrt(2.0), scale: float = 1.0
) -> tuple[float, float, float]:
    return tuple(
        scale * (1.0 + c * math.cos(phase + 2.0 * math.pi * k / 3.0))
        for k in range(3)
    )


def koide_q_from_sqrt_vector(values: tuple[float, float, float]) -> float:
    return sum(value * value for value in values) / (sum(values) ** 2)


def sorted_normalized(values: tuple[float, float, float]) -> tuple[float, float, float]:
    total = sum(values)
    return tuple(sorted((value / total for value in values), reverse=True))


def rounded(values: tuple[float, ...], digits: int = 14) -> tuple[float, ...]:
    return tuple(round(value, digits) for value in values)


def main() -> int:
    section("A. Source surfaces and stronger-premise boundary")

    source_files = [
        "CHARGED_LEPTON_SELECTED_LINE_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md",
        "CHARGED_LEPTON_OP_LOCAL_SOURCE_SELECTED_LINE_SELECTOR_NO_GO_NOTE_2026-04-27.md",
        "KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md",
        "KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md",
        "KOIDE_Q_DELTA_RESIDUAL_COHOMOLOGY_OBSTRUCTION_NO_GO_NOTE_2026-04-24.md",
        "KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md",
        "KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md",
        "KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md",
        "CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md",
    ]
    for name in source_files:
        check(f"source surface exists: {name}", (DOCS / name).exists())

    note_text = NOTE.read_text(encoding="utf-8") if NOTE.exists() else ""
    selected_line = read_doc(
        "CHARGED_LEPTON_SELECTED_LINE_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md"
    )
    op_selected = read_doc(
        "CHARGED_LEPTON_OP_LOCAL_SOURCE_SELECTED_LINE_SELECTOR_NO_GO_NOTE_2026-04-27.md"
    )
    a1_audit = read_doc("KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md")
    readout_split = read_doc("KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md")
    cohomology = read_doc("KOIDE_Q_DELTA_RESIDUAL_COHOMOLOGY_OBSTRUCTION_NO_GO_NOTE_2026-04-24.md")
    pointed_origin = read_doc("KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md")
    q_phase_erasure = read_doc("KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md")
    op_locality = read_doc("KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md")
    radiative_firewall = read_doc("CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md")

    check(
        "new note exists",
        NOTE.exists(),
        str(NOTE.relative_to(ROOT)) if NOTE.exists() else str(NOTE),
    )
    check(
        "new note records no retained mass closure and comparator firewall",
        "CHARGED_LEPTON_TYPEB_RADIAN_READOUT_GENERATION_SELECTOR_NO_GO=TRUE" in note_text
        and "CHARGED_LEPTON_MASS_RETENTION=FALSE" in note_text
        and "PDG_MASSES_USED_AS_COMPARATORS_ONLY=TRUE" in note_text,
    )
    check(
        "prior selected-line no-go requires based law",
        "BASED_ENDPOINT_OR_SOURCE_LAW_REQUIRED=TRUE" in selected_line
        and "UNBASED_C3_ORBIT_SELECTS_SINGLE_GENERATION_LABEL=FALSE" in selected_line,
    )
    check(
        "prior OP-local source cycle still requires based endpoint/source/tau selector",
        "OP_LOCAL_SOURCE_PLUS_SELECTED_LINE_SELECTS_GENERATION=FALSE" in op_selected
        and "BASED_ENDPOINT_SOURCE_OR_TAU_SCALE_SELECTOR_REQUIRED=TRUE" in op_selected,
    )
    check(
        "Type-B-to-radian law was open before this stronger-premise grant",
        "TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE=TRUE" in a1_audit
        and "RESIDUAL_PRIMITIVE=type_b_rational_to_radian_observable_law" in a1_audit,
    )
    check(
        "closed APS readout does not by itself remove endpoint split",
        "RESIDUAL_DELTA=selected_line_endpoint_transition_tau_not_removed_by_closed_readout"
        in readout_split,
    )
    check(
        "exact-sequence audit leaves canonical section as next theorem",
        contains(cohomology, "NEXT_THEOREM = retained_canonical_section_or_new_primitive_based_readout_law")
        or "NEXT_THEOREM=retained_canonical_section_or_new_primitive_based_readout_law"
        in cohomology,
    )
    check(
        "unpointed retained data do not force a pointed origin",
        "RETAINED_UNPOINTED_DATA_FORCE_POINTED_ORIGIN=FALSE" in pointed_origin,
    )
    check(
        "Q erases Brannen phase on the carrier",
        "KOIDE_Q_INDEPENDENT_OF_BRANNEN_PHASE_AND_SCALE=TRUE" in q_phase_erasure,
    )
    check(
        "OP-locality source support is conditional, not retained Q closure",
        "KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT=TRUE" in op_locality
        and "KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE" in op_locality,
    )

    section("B. Grant P_RADIAN and P_SOURCE as scalar quotient data")

    scalar_data = ScalarReadoutData(
        q=Fraction(2, 3),
        delta=Fraction(2, 9),
        source_z=Fraction(0),
        unit_law="Type-B rational read as radians",
    )
    c3_images = tuple(scalar_readout_action(scalar_data, shift) for shift in (0, 1, 2))
    alternate_unit_data = tuple(
        ScalarReadoutData(
            q=Fraction(2, 3),
            delta=Fraction(2, 9),
            source_z=Fraction(0),
            unit_law=unit_law,
        )
        for unit_law in (
            "period-1 radian convention",
            "canonical 2pi-period convention",
            "admitted Type-B-to-radian bridge",
        )
    )

    check("granted scalar Q value is 2/3", scalar_data.q == Fraction(2, 3))
    check("granted scalar Brannen readout is delta=2/9", scalar_data.delta == Fraction(2, 9))
    check("granted source coordinate is z=0", scalar_data.source_z == 0)
    check("scalar readout data are fixed by cyclic relabeling", len(set(c3_images)) == 1)
    check(
        "unit-law variants remain scalar C3-fixed data",
        all(
            scalar_readout_action(data, shift) == data
            for data in alternate_unit_data
            for shift in (0, 1, 2)
        ),
    )
    check(
        "scalar readout object carries no label field",
        not hasattr(scalar_data, "generation_label") and not hasattr(scalar_data, "tau_label"),
    )

    section("C. Selected-line carrier check without PDG inputs")

    delta = float(scalar_data.delta)
    vector = brannen_sqrt_vector(delta)
    rotations = tuple(rotate(vector, shift) for shift in (0, 1, 2))
    q_values = tuple(koide_q_from_sqrt_vector(rotation) for rotation in rotations)
    unordered_ratios = tuple(sorted_normalized(rotation) for rotation in rotations)
    heaviest_slots = tuple(rotation.index(max(rotation)) for rotation in rotations)

    check("granted selected-line vector is positive on the first branch", all(value > 0 for value in vector))
    check(
        "selected-line vector has Q=2/3 from c^2=2",
        abs(koide_q_from_sqrt_vector(vector) - 2.0 / 3.0) < 1.0e-12,
        f"Q={koide_q_from_sqrt_vector(vector):.15f}",
    )
    check(
        "cyclic relabelings preserve Q",
        all(abs(q_value - 2.0 / 3.0) < 1.0e-12 for q_value in q_values),
        f"Q_values={tuple(round(q_value, 15) for q_value in q_values)}",
    )
    check(
        "cyclic relabelings preserve unordered normalized ratios",
        len({rounded(ratio) for ratio in unordered_ratios}) == 1,
        f"ratio={rounded(unordered_ratios[0])}",
    )
    check(
        "cyclic relabelings move the heaviest slot through all labels",
        set(heaviest_slots) == {0, 1, 2},
        f"heaviest_slots={heaviest_slots}",
    )
    check(
        "scalar Type-B radian readout does not identify the heaviest physical label",
        set(heaviest_slots) == {0, 1, 2} and len(set(c3_images)) == 1,
    )

    section("D. Natural-selector obstruction")

    fixed_labels = invariant_single_labels()
    natural_selectors = quotient_to_label_natural_selectors(scalar_data)
    invariant_subsets = invariant_label_subsets()
    nonempty_invariant_subsets = [subset for subset in invariant_subsets if subset]
    singleton_subsets = [subset for subset in invariant_subsets if len(subset) == 1]
    based_maps = equivariant_maps_between_based_torsors()

    check(
        "generation labels carry a free C3 action",
        all(label_action(label, 1) != label for label in (0, 1, 2)),
    )
    check("no single label is fixed by C3", fixed_labels == [], f"fixed={fixed_labels}")
    check(
        "no natural selector exists from scalar quotient data to one label",
        natural_selectors == [],
        f"selectors={natural_selectors}",
    )
    check("no invariant singleton subset selects e, mu, or tau", singleton_subsets == [])
    check(
        "only nonempty invariant subset is the full generation orbit",
        nonempty_invariant_subsets == [frozenset({0, 1, 2})],
        f"subsets={nonempty_invariant_subsets}",
    )
    check(
        "based equivariant endpoint-to-label maps exist only after a basepoint choice",
        len(based_maps) == 3,
        f"maps={based_maps}",
    )
    check(
        "P_RADIAN narrows unit readout but not selected-line basepoint",
        natural_selectors == [] and len(based_maps) == 3,
    )

    section("E. Scale and comparator firewall")

    proof_inputs = {
        "P_SOURCE: z=0 source support",
        "P_RADIAN: scalar Type-B-to-radian readout",
        "C3 action on generation labels",
        "Brannen carrier c^2=2",
        "free selected-line orbit",
        "prior support/no-go closeout flags",
    }
    forbidden_inputs = set(PDG_COMPARATORS_MEV) | {
        "observed_tau_is_heaviest",
        "PDG_generation_label",
        "charged_lepton_mass_fit",
    }

    check(
        "radiative scale support still requires a generation selector",
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
        "Type-B radian readout plus source support is not a generation selector",
        scalar_data.q == Fraction(2, 3)
        and scalar_data.delta == Fraction(2, 9)
        and scalar_data.source_z == 0
        and natural_selectors == []
        and len(based_maps) == 3,
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
        print("VERDICT: Type-B radian readout generation-selector no-go.")
        print("CHARGED_LEPTON_TYPEB_RADIAN_READOUT_GENERATION_SELECTOR_NO_GO=TRUE")
        print("TYPEB_RADIAN_READOUT_PLUS_SOURCE_SUPPORT_SELECTS_GENERATION=FALSE")
        print("TYPEB_RADIAN_READOUT_RETIRES_PDG_MASS_PIN=FALSE")
        print("BASED_ENDPOINT_SOURCE_OR_TAU_SCALE_SELECTOR_REQUIRED=TRUE")
        print("PDG_MASSES_USED_AS_COMPARATORS_ONLY=TRUE")
        print("CHARGED_LEPTON_MASS_RETENTION=FALSE")
        return 0

    print("VERDICT: Type-B radian readout audit has failing checks.")
    print("CHARGED_LEPTON_TYPEB_RADIAN_READOUT_GENERATION_SELECTOR_NO_GO=FALSE")
    print("CHARGED_LEPTON_MASS_RETENTION=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
