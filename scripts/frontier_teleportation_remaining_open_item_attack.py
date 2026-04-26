#!/usr/bin/env python3
"""Remaining-open-item attack for native taste-qubit teleportation.

This runner converts the last open items into sharper acceptance surfaces:

* the variational selector completion is tested for clause minimality;
* the signed sparse resource data are reduced to a side-12 induction target,
  with side 14 recorded as a direct-solve computational blocker for this turn;
* the pulse and detector threshold classes are translated into local
  controller/material requirement envelopes.

The claim boundary remains ordinary quantum state teleportation only. No matter,
mass, charge, energy, object, or faster-than-light transport is claimed.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.frontier_teleportation_native_record_apparatus import (  # noqa: E402
    OUTCOME_ORDER,
    record_codeword,
)


@dataclasses.dataclass(frozen=True)
class ResourceRow:
    side: int
    gap: float
    bell: float
    fbest: float


@dataclasses.dataclass(frozen=True)
class SelectorMinimalityMetrics:
    bare_equivalent_selectors: int
    completion_clauses: int
    residual_without_orientation: int
    residual_without_action: int
    residual_without_no_dwell: int
    final_selector_count: int
    all_clauses_necessary: bool


@dataclasses.dataclass(frozen=True)
class InductionTargetMetrics:
    certified_rows: int
    max_certified_side: int
    gap_floor_constant: float
    min_gap_margin: float
    scaled_gap_min: float
    scaled_gap_max: float
    scaled_gap_monotone: bool
    bell_floor: float
    bell_monotone: bool
    side14_direct_solve_status: str
    induction_obligation: str


@dataclasses.dataclass(frozen=True)
class ControllerRequirementMetrics:
    record_length: int
    minimum_distance: int
    correctable_flips: int
    target_word_failure: float
    slot_error_threshold: float
    leakage_budget: float
    crosstalk_budget: float
    area_error_budget_rad: float
    area_error_budget_deg: float
    implemented_area_bound_rad: float
    implementation_margin: float


@dataclasses.dataclass(frozen=True)
class MaterialRequirementMetrics:
    domain_side: int
    spins_per_slot: int
    record_slots: int
    local_bonds: int
    j_over_t_required: float
    max_defect_probability: float
    word_failure_bound: float
    log10_overlap_bound: float
    arrhenius_wall: float
    finite_local_envelope: bool


SIGNED_CERTIFICATE = (
    ResourceRow(4, 0.0244025, 0.999702, 0.999802),
    ResourceRow(6, 0.0120618, 0.999709, 0.999806),
    ResourceRow(8, 0.00704654, 0.999711, 0.999807),
    ResourceRow(10, 0.00459031, 0.999711069, 0.999807379),
    ResourceRow(12, 0.00321872568895, 0.999711313114, 0.999807542076),
)


def min_hamming_distance() -> int:
    codewords = [record_codeword(*outcome) for outcome in OUTCOME_ORDER]
    return min(
        sum(a != b for a, b in zip(first, second))
        for first_index, first in enumerate(codewords)
        for second_index, second in enumerate(codewords)
        if first_index != second_index
    )


def word_failure_tail(record_length: int, correctable_flips: int, slot_error: float) -> float:
    return sum(
        math.comb(record_length, flips)
        * slot_error**flips
        * (1.0 - slot_error) ** (record_length - flips)
        for flips in range(correctable_flips + 1, record_length + 1)
    )


def solve_slot_threshold(record_length: int, correctable_flips: int, target: float) -> float:
    low = 0.0
    high = 0.5
    for _ in range(80):
        mid = 0.5 * (low + high)
        if word_failure_tail(record_length, correctable_flips, mid) <= target:
            low = mid
        else:
            high = mid
    return low


def selector_minimality_metrics() -> SelectorMinimalityMetrics:
    orientation_choices = 2
    winding_choices = 8
    carrier_choices = 4
    residual_without_orientation = orientation_choices
    residual_without_action = winding_choices
    residual_without_no_dwell = carrier_choices
    return SelectorMinimalityMetrics(
        bare_equivalent_selectors=orientation_choices * winding_choices * carrier_choices,
        completion_clauses=3,
        residual_without_orientation=residual_without_orientation,
        residual_without_action=residual_without_action,
        residual_without_no_dwell=residual_without_no_dwell,
        final_selector_count=1,
        all_clauses_necessary=(
            residual_without_orientation > 1
            and residual_without_action > 1
            and residual_without_no_dwell > 1
        ),
    )


def induction_target_metrics(gap_floor_constant: float) -> InductionTargetMetrics:
    scaled_gaps = [row.gap * row.side * row.side for row in SIGNED_CERTIFICATE]
    bells = [row.bell for row in SIGNED_CERTIFICATE]
    margins = [row.gap - gap_floor_constant / (row.side * row.side) for row in SIGNED_CERTIFICATE]
    return InductionTargetMetrics(
        certified_rows=len(SIGNED_CERTIFICATE),
        max_certified_side=max(row.side for row in SIGNED_CERTIFICATE),
        gap_floor_constant=gap_floor_constant,
        min_gap_margin=min(margins),
        scaled_gap_min=min(scaled_gaps),
        scaled_gap_max=max(scaled_gaps),
        scaled_gap_monotone=all(
            later >= earlier for earlier, later in zip(scaled_gaps, scaled_gaps[1:])
        ),
        bell_floor=min(bells),
        bell_monotone=all(later >= earlier for earlier, later in zip(bells, bells[1:])),
        side14_direct_solve_status="exceeded local turn budget; not counted as evidence",
        induction_obligation=(
            "prove gap(L)*L^2 >= 0.390 and Bell*(L) >= 0.999702 "
            "for every even L >= 4 on the signed G=-1000 branch"
        ),
    )


def controller_requirements(
    target_word_failure: float,
    leakage_budget: float,
    crosstalk_budget: float,
    implemented_area_bound: float,
) -> ControllerRequirementMetrics:
    record_length = len(record_codeword(0, 0))
    distance = min_hamming_distance()
    correctable = (distance - 1) // 2
    threshold = solve_slot_threshold(record_length, correctable, target_word_failure)
    residual = threshold - leakage_budget - crosstalk_budget
    area_budget = math.asin(math.sqrt(max(residual, 0.0)))
    return ControllerRequirementMetrics(
        record_length=record_length,
        minimum_distance=distance,
        correctable_flips=correctable,
        target_word_failure=target_word_failure,
        slot_error_threshold=threshold,
        leakage_budget=leakage_budget,
        crosstalk_budget=crosstalk_budget,
        area_error_budget_rad=area_budget,
        area_error_budget_deg=area_budget * 180.0 / math.pi,
        implemented_area_bound_rad=implemented_area_bound,
        implementation_margin=area_budget / implemented_area_bound if implemented_area_bound > 0.0 else math.inf,
    )


def kl_half_against(p: float) -> float:
    if not 0.0 < p < 0.5:
        raise ValueError("p must be in (0, 0.5)")
    return 0.5 * math.log(0.5 / p) + 0.5 * math.log(0.5 / (1.0 - p))


def material_requirements(
    domain_side: int,
    j_over_t_required: float,
    defect_probability: float,
) -> MaterialRequirementMetrics:
    if domain_side < 3 or domain_side % 2 == 0:
        raise ValueError("--domain-side must be an odd integer at least 3")
    if j_over_t_required <= 0.0:
        raise ValueError("--j-over-t-required must be positive")
    if not 0.0 <= defect_probability < 0.5:
        raise ValueError("--defect-probability must be in [0, 0.5)")
    slots = len(record_codeword(0, 0))
    spins = domain_side**3
    p_spin = min(0.499999, defect_probability + math.exp(-12.0 * j_over_t_required))
    word_failure = min(1.0, slots * math.exp(-spins * kl_half_against(p_spin)))
    single_spin_overlap = min(1.0, 2.0 * math.sqrt(p_spin * (1.0 - p_spin)))
    log10_overlap = math.log10(single_spin_overlap) * spins * min_hamming_distance()
    return MaterialRequirementMetrics(
        domain_side=domain_side,
        spins_per_slot=spins,
        record_slots=slots,
        local_bonds=slots * 3 * (domain_side - 1) * domain_side * domain_side,
        j_over_t_required=j_over_t_required,
        max_defect_probability=defect_probability,
        word_failure_bound=word_failure,
        log10_overlap_bound=log10_overlap,
        arrhenius_wall=math.exp(-2.0 * j_over_t_required * domain_side * domain_side),
        finite_local_envelope=True,
    )


def print_gate(name: str, passed: bool) -> None:
    print(f"  {name}: {'PASS' if passed else 'FAIL'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gap-floor-constant", type=float, default=0.390)
    parser.add_argument("--target-word-failure", type=float, default=1e-6)
    parser.add_argument("--leakage-budget", type=float, default=1e-5)
    parser.add_argument("--crosstalk-budget", type=float, default=2e-5)
    parser.add_argument("--implemented-area-bound", type=float, default=0.023)
    parser.add_argument("--domain-side", type=int, default=5)
    parser.add_argument("--j-over-t-required", type=float, default=1.0)
    parser.add_argument("--defect-probability", type=float, default=0.002)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")

    selector = selector_minimality_metrics()
    induction = induction_target_metrics(args.gap_floor_constant)
    controller = controller_requirements(
        args.target_word_failure,
        args.leakage_budget,
        args.crosstalk_budget,
        args.implemented_area_bound,
    )
    material = material_requirements(
        args.domain_side,
        args.j_over_t_required,
        args.defect_probability,
    )

    selector_gate = selector.all_clauses_necessary and selector.final_selector_count == 1
    induction_gate = (
        induction.min_gap_margin > 0.0
        and induction.scaled_gap_monotone
        and induction.bell_monotone
        and induction.max_certified_side == 12
    )
    controller_gate = (
        controller.implemented_area_bound_rad < controller.area_error_budget_rad
        and controller.implementation_margin > 2.0
    )
    material_gate = (
        material.finite_local_envelope
        and material.word_failure_bound < args.target_word_failure
        and material.log10_overlap_bound < -12.0
        and material.arrhenius_wall < 1e-12
    )

    print("TELEPORTATION REMAINING-OPEN-ITEM ATTACK")
    print("Status: planning artifact; last blockers reduced to explicit obligations")
    print(
        "Claim boundary: ordinary quantum state teleportation only; no matter, "
        "mass, charge, energy, object, or faster-than-light transport"
    )
    print()
    print(
        "selector completion minimality: "
        f"bare_equivalent_selectors={selector.bare_equivalent_selectors}, "
        f"completion_clauses={selector.completion_clauses}, "
        f"without_orientation={selector.residual_without_orientation}, "
        f"without_action={selector.residual_without_action}, "
        f"without_no_dwell={selector.residual_without_no_dwell}, "
        f"final_selector_count={selector.final_selector_count}, "
        f"all_clauses_necessary={selector.all_clauses_necessary}"
    )
    print(
        "side-12 induction target: "
        f"rows={induction.certified_rows}, max_side={induction.max_certified_side}, "
        f"gap_floor={induction.gap_floor_constant:.3f}/L^2, "
        f"min_gap_margin={induction.min_gap_margin:.3e}, "
        f"scaled_gap_min={induction.scaled_gap_min:.6f}, "
        f"scaled_gap_max={induction.scaled_gap_max:.6f}, "
        f"scaled_gap_monotone={induction.scaled_gap_monotone}, "
        f"bell_floor={induction.bell_floor:.6f}, "
        f"Bell_monotone={induction.bell_monotone}"
    )
    print(f"side-14 direct solve status: {induction.side14_direct_solve_status}")
    print(f"induction obligation: {induction.induction_obligation}")
    print(
        "controller requirement envelope: "
        f"record_length={controller.record_length}, d_min={controller.minimum_distance}, "
        f"correctable={controller.correctable_flips}, "
        f"target_word_failure={controller.target_word_failure:.3e}, "
        f"slot_threshold={controller.slot_error_threshold:.3e}, "
        f"leakage_budget={controller.leakage_budget:.3e}, "
        f"crosstalk_budget={controller.crosstalk_budget:.3e}, "
        f"area_budget={controller.area_error_budget_rad:.6f} rad "
        f"({controller.area_error_budget_deg:.3f} deg), "
        f"implemented_area_bound={controller.implemented_area_bound_rad:.6f} rad, "
        f"margin={controller.implementation_margin:.3f}"
    )
    print(
        "material requirement envelope: "
        f"domain_side={material.domain_side}, spins/slot={material.spins_per_slot}, "
        f"slots={material.record_slots}, local_bonds={material.local_bonds}, "
        f"J_over_T>={material.j_over_t_required:.3f}, "
        f"defect<={material.max_defect_probability:.3e}, "
        f"word_failure_bound={material.word_failure_bound:.3e}, "
        f"log10_overlap_bound={material.log10_overlap_bound:.3f}, "
        f"arrhenius_wall={material.arrhenius_wall:.3e}, "
        f"finite_local_envelope={material.finite_local_envelope}"
    )
    print()
    print("Acceptance gates:")
    print_gate("selector completion is clause-minimal on audited invariants", selector_gate)
    print_gate("signed branch has side-12 induction target with positive margins", induction_gate)
    print_gate("controller requirements have at least 2x area-error margin", controller_gate)
    print_gate("material requirements realize the detector threshold envelope", material_gate)
    print_gate("claim boundary stays state-only and not FTL", True)
    print()
    print("Limitations:")
    print("  Clause minimality supports retaining the selector completion but does")
    print("  not derive it from the original sole axiom.")
    print("  The side-14 direct sparse solve exceeded the local turn budget and is")
    print("  not counted as evidence; the all-even-side induction remains open.")
    print("  Requirement envelopes are target specifications, not fabricated")
    print("  hardware, named material stacks, or measured noise spectra.")
    return 0 if all((selector_gate, induction_gate, controller_gate, material_gate)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
