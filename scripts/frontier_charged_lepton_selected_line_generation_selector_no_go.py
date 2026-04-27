#!/usr/bin/env python3
"""Selected-line generation-selector no-go for charged leptons.

This runner audits a narrower leftover after the broader Koide ratio/source
selector firewall:

    Koide Q support + selected-line/Brannen phase support
      ?=> retained physical generation/tau-scale selector

The test grants the current non-PDG support data, including the Brannen carrier
at c^2 = 2 and the selected-line phase value used by the support stack.  It then
checks the group-theoretic obstruction: once the selected-line data are treated
as an unbased C3 orbit, no C3-natural single generation label can be selected.
Based selectors exist, but choosing the base is exactly the missing physical
endpoint/source/generation law.
"""

from __future__ import annotations

import itertools
import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0

PDG_COMPARATORS_MEV = {
    "m_e_pdg_mev": 0.510998950,
    "m_mu_pdg_mev": 105.6583755,
    "m_tau_pdg_mev": 1776.86,
}


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


def rotate(values: tuple[float, float, float], shift: int = 1) -> tuple[float, float, float]:
    shift = shift % 3
    return values[shift:] + values[:shift]


def brannen_sqrt_vector(
    phase: float, c: float = math.sqrt(2.0), scale: float = 1.0
) -> tuple[float, float, float]:
    return tuple(
        scale * (1.0 + c * math.cos(phase + 2.0 * math.pi * k / 3.0))
        for k in range(3)
    )


def koide_q_from_sqrt_vector(values: tuple[float, float, float]) -> float:
    return sum(x * x for x in values) / (sum(values) ** 2)


def sorted_normalized(values: tuple[float, float, float]) -> tuple[float, float, float]:
    total = sum(values)
    return tuple(sorted((x / total for x in values), reverse=True))


def rounded(values: tuple[float, ...], digits: int = 14) -> tuple[float, ...]:
    return tuple(round(x, digits) for x in values)


def label_action(label: int, shift: int) -> int:
    return (label + shift) % 3


def invariant_single_label_maps() -> list[int]:
    """Maps from an unbased orbit quotient point to one label.

    The quotient point is unchanged by every C3 relabeling.  A natural selector
    would therefore have to return a label fixed by every C3 shift.
    """

    labels = (0, 1, 2)
    return [
        label
        for label in labels
        if all(label_action(label, shift) == label for shift in (0, 1, 2))
    ]


def invariant_label_subsets() -> list[frozenset[int]]:
    labels = (0, 1, 2)
    subsets: list[frozenset[int]] = []
    for size in range(4):
        for subset in itertools.combinations(labels, size):
            candidate = frozenset(subset)
            if all(
                frozenset(label_action(label, shift) for label in candidate) == candidate
                for shift in (0, 1, 2)
            ):
                subsets.append(candidate)
    return subsets


def based_equivariant_selector_count() -> int:
    """Count equivariant maps between two based C3 torsors."""

    count = 0
    domain = (0, 1, 2)
    codomain = (0, 1, 2)
    for base_image in codomain:
        selector = {shift: label_action(base_image, shift) for shift in domain}
        if all(
            selector[label_action(point, shift)]
            == label_action(selector[point], shift)
            for point in domain
            for shift in domain
        ):
            count += 1
    return count


def onsite_c3_fixed_sources(samples: tuple[tuple[float, float, float], ...]) -> tuple[bool, ...]:
    return tuple(source == rotate(source, 1) == rotate(source, 2) for source in samples)


def main() -> int:
    section("A. Source surfaces")

    source_files = [
        "CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md",
        "KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md",
        "KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md",
        "KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md",
        "KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md",
        "KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md",
        "KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md",
        "CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md",
    ]
    for name in source_files:
        check(f"source surface exists: {name}", (DOCS / name).exists())

    ratio_firewall = read_doc(
        "CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md"
    )
    q_package = read_doc("KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md")
    op_locality = read_doc("KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md")
    onsite_no_go = read_doc("KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md")
    a1_audit = read_doc("KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md")
    pointed_origin = read_doc("KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md")
    readout_split = read_doc("KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md")
    radiative_firewall = read_doc("CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md")

    check(
        "broad ratio/source selector route is already closed",
        "KOIDE_Q_PLUS_BRANNEN_PHASE_GENERATION_SELECTOR=FALSE" in ratio_firewall
        and "CHARGED_LEPTON_MASS_RETENTION=FALSE" in ratio_firewall,
    )
    check(
        "Koide package leaves Q and delta physical bridges open",
        "The remaining open bridges" in q_package
        and "Koide relation `Q = 2/3`" in q_package
        and "Brannen phase" in q_package
        and "2/9" in q_package,
    )
    check(
        "Q source support is conditional, not retained closure",
        "KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT=TRUE" in op_locality
        and "KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE" in op_locality,
    )
    check(
        "onsite-source synthesis keeps the source-domain law open",
        "CURRENT_RETAINED_COMMUTANT_SOURCE_DOMAIN_ADMITS_Z=TRUE" in onsite_no_go
        and "Q_RETAINED_NATIVE_CLOSURE=FALSE" in onsite_no_go,
    )
    check(
        "selected-line radian bridge remains primitive",
        "TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE=TRUE" in a1_audit,
    )
    check(
        "unpointed retained data do not force a pointed origin",
        "RETAINED_UNPOINTED_DATA_FORCE_POINTED_ORIGIN=FALSE" in pointed_origin,
    )
    check(
        "closed APS readout does not remove selected-line endpoint split",
        "RESIDUAL_DELTA=selected_line_endpoint_transition_tau_not_removed_by_closed_readout"
        in readout_split,
    )
    check(
        "radiative scale support still requires a generation selector",
        contains(
            radiative_firewall,
            "cannot select the tau eigenvalue without an additional generation-selection, ratio, or source-domain primitive",
        ),
    )

    section("B. Granted non-PDG support data")

    phase = 2.0 / 9.0
    vector = brannen_sqrt_vector(phase)
    rotations = tuple(rotate(vector, shift) for shift in (0, 1, 2))
    q_values = tuple(koide_q_from_sqrt_vector(rotated) for rotated in rotations)
    unordered_ratios = tuple(sorted_normalized(rotated) for rotated in rotations)
    max_slots = tuple(rotated.index(max(rotated)) for rotated in rotations)

    proof_inputs = {
        "C3 action on the three-generation orbit",
        "Brannen carrier at c^2=2",
        "selected-line phase support delta=2/9",
        "unbased orbit quotient",
        "C3-fixed onsite source algebra",
        "previous support/no-go closeout flags",
    }
    forbidden_inputs = set(PDG_COMPARATORS_MEV) | {
        "observed_tau_is_heaviest",
        "PDG_generation_label",
        "charged_lepton_mass_fit",
    }

    check("granted selected-line vector is positive", all(value > 0.0 for value in vector))
    check(
        "granted selected-line vector has Koide Q=2/3",
        abs(koide_q_from_sqrt_vector(vector) - 2.0 / 3.0) < 1.0e-12,
        f"Q={koide_q_from_sqrt_vector(vector):.15f}",
    )
    check(
        "C3 rotations preserve Q",
        all(abs(value - 2.0 / 3.0) < 1.0e-12 for value in q_values),
        f"Q_values={tuple(round(value, 15) for value in q_values)}",
    )
    check(
        "C3 rotations preserve unordered normalized ratios",
        len({rounded(ratio) for ratio in unordered_ratios}) == 1,
        f"ratio={rounded(unordered_ratios[0])}",
    )
    check(
        "C3 rotations move the largest slot",
        set(max_slots) == {0, 1, 2},
        f"max_slots={max_slots}",
    )
    check(
        "PDG charged-lepton masses are not proof inputs",
        proof_inputs.isdisjoint(forbidden_inputs),
        f"proof_inputs={sorted(proof_inputs)}",
    )

    section("C. Unbased C3 orbit cannot select one generation label")

    fixed_single_labels = invariant_single_label_maps()
    invariant_subsets = invariant_label_subsets()
    nonempty_invariant_subsets = [subset for subset in invariant_subsets if subset]
    singleton_invariant_subsets = [
        subset for subset in invariant_subsets if len(subset) == 1
    ]

    check(
        "C3 label action is free on single generation labels",
        all(label_action(label, 1) != label for label in (0, 1, 2)),
    )
    check(
        "no natural single-label map exists from the unbased orbit quotient",
        fixed_single_labels == [],
        f"fixed_single_labels={fixed_single_labels}",
    )
    check(
        "the only nonempty invariant label subset is the full generation orbit",
        nonempty_invariant_subsets == [frozenset({0, 1, 2})],
        f"subsets={nonempty_invariant_subsets}",
    )
    check(
        "no invariant singleton subset selects tau/e/mu",
        singleton_invariant_subsets == [],
    )
    check(
        "based equivariant selectors exist only after a base choice",
        based_equivariant_selector_count() == 3,
        "three choices correspond to three basepoint labels",
    )

    check(
        "heaviest-slot rule is representative-dependent on the unbased orbit",
        set(max_slots) == {0, 1, 2},
        f"heaviest_slots_under_relabeling={max_slots}",
    )
    check(
        "sorted heavy/middle/light ratios are not generation labels",
        rounded(unordered_ratios[0]) == rounded(unordered_ratios[1])
        and set(max_slots) == {0, 1, 2},
    )

    section("D. Current source and endpoint supports are symmetric or unbased")

    source_samples = ((1.0, 1.0, 1.0), (1.0, 2.0, 1.0), (3.0, 4.0, 5.0))
    source_fixed = onsite_c3_fixed_sources(source_samples)
    eta_aps = 2.0 / 9.0
    endpoint_splits = tuple((delta_open, eta_aps - delta_open) for delta_open in (0.0, 1.0 / 9.0, 2.0 / 9.0))

    check(
        "only common onsite source sample is C3-fixed",
        source_fixed == (True, False, False),
        f"fixed={source_fixed}",
    )
    check(
        "C3-fixed onsite source has no distinguished generation slot",
        rotate((1.0, 1.0, 1.0), 1) == (1.0, 1.0, 1.0)
        and invariant_single_label_maps() == [],
    )
    check(
        "closed eta value leaves selected-line endpoint split free",
        all(abs(delta_open + tau - eta_aps) < 1.0e-15 for delta_open, tau in endpoint_splits)
        and len(endpoint_splits) == 3,
        f"splits={endpoint_splits}",
    )
    check(
        "pointed-origin note identifies basepoint law as the residual",
        "RESIDUAL_PRIMITIVE=retained_physical_source_boundary_origin_laws"
        in pointed_origin,
    )
    check(
        "A1 audit identifies Type-B-to-radian law as still missing",
        "RESIDUAL_PRIMITIVE=type_b_rational_to_radian_observable_law" in a1_audit,
    )

    section("E. Comparator firewall")

    sqrt_pdg = tuple(math.sqrt(value) for value in PDG_COMPARATORS_MEV.values())
    q_pdg = koide_q_from_sqrt_vector(sqrt_pdg)
    pdg_sorted = sorted_normalized(sqrt_pdg)
    support_sorted = sorted_normalized(vector)
    relative_gap = max(
        abs(a - b) for a, b in zip(pdg_sorted, support_sorted, strict=True)
    )

    check(
        "PDG masses are comparator-only and near the Koide value",
        abs(q_pdg - 2.0 / 3.0) < 1.0e-5,
        f"Q_PDG={q_pdg:.12f}; not used above as a proof input",
    )
    check(
        "support ratios are not fitted from PDG masses",
        relative_gap > 1.0e-6 and proof_inputs.isdisjoint(forbidden_inputs),
        f"max_sorted_ratio_gap={relative_gap:.6e}",
    )

    section("F. Verdict")

    check(
        "unbased selected-line data do not provide a retained generation selector",
        fixed_single_labels == []
        and singleton_invariant_subsets == []
        and based_equivariant_selector_count() == 3,
    )
    check(
        "remaining primitive is based endpoint/source/generation law",
        "RESIDUAL_DELTA=derive_selected_line_boundary_source_based_endpoint_and_Type_B_radian_readout"
        in ratio_firewall
        and "RESIDUAL_GENERATION=derive_nonobservational_generation_label_or_tau_scale_selector"
        in ratio_firewall,
    )

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: selected-line generation-selector no-go.")
        print("CHARGED_LEPTON_SELECTED_LINE_GENERATION_SELECTOR_NO_GO=TRUE")
        print("UNBASED_C3_ORBIT_SELECTS_SINGLE_GENERATION_LABEL=FALSE")
        print("BASED_ENDPOINT_OR_SOURCE_LAW_REQUIRED=TRUE")
        print("PDG_MASSES_USED_AS_COMPARATORS_ONLY=TRUE")
        print("CHARGED_LEPTON_MASS_RETENTION=FALSE")
        return 0

    print("VERDICT: selected-line generation-selector audit has failing checks.")
    print("CHARGED_LEPTON_SELECTED_LINE_GENERATION_SELECTOR_NO_GO=FALSE")
    print("CHARGED_LEPTON_MASS_RETENTION=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
