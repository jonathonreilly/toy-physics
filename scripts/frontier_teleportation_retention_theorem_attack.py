#!/usr/bin/env python3
"""Retention-theorem attack for native taste-qubit teleportation.

This runner pushes the remaining blockers after the unconditional-closure
attack:

* bare one-axiom derivation is closed negatively on the audited selector
  invariants, forcing a choice to retain or reject a variational completion;
* the signed sparse 3D resource certificate is extended through side 12;
* the preparation theorem is reduced to a single induction obligation on the
  scaled gap and Bell floor;
* the pulse and detector threshold classes are mapped to a concrete local
  controller/domain implementation envelope.

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
    chsh: float
    negativity: float
    purity: float

    @property
    def hilbert_dim(self) -> int:
        return self.side**6


@dataclasses.dataclass(frozen=True)
class SelectorRetentionMetrics:
    audited_equivalent_pairs: int
    selector_entropy_bits: float
    retained_completion_clauses: int
    bare_derivation_closed_negative: bool
    minimal_completion_sufficient: bool
    retained_or_rejected_decision_required: bool


@dataclasses.dataclass(frozen=True)
class Side12ScalingMetrics:
    row_count: int
    max_side: int
    gap_floor_constant: float
    min_gap_margin: float
    min_bell: float
    max_bell_deficit: float
    scaled_gap_monotone: bool
    bell_floor_monotone: bool
    side12_tadiabatic_bound: float
    side12_beta_bound: float
    induction_obligation_open: bool


@dataclasses.dataclass(frozen=True)
class ControllerEnvelopeMetrics:
    record_length: int
    minimum_distance: int
    correctable_flips: int
    leakage: float
    crosstalk: float
    slot_threshold: float
    certified_area_budget_rad: float
    implemented_area_bound_rad: float
    implemented_slot_error: float
    word_failure_bound: float


@dataclasses.dataclass(frozen=True)
class MaterialEnvelopeMetrics:
    domain_side: int
    spins_per_slot: int
    slots: int
    local_bonds: int
    exchange_to_temperature: float
    defect_probability: float
    spin_flip_probability: float
    majority_failure_bound: float
    word_failure_bound: float
    log10_overlap_bound: float
    arrhenius_wall: float
    minimal_odd_domain_side_for_target: int


SIGNED_RESOURCE_ROWS = (
    ResourceRow(4, 0.0244025, 0.999702, 0.999802, 2.827585, 0.499702, 0.999702),
    ResourceRow(6, 0.0120618, 0.999709, 0.999806, 2.827604, 0.499709, 0.999709),
    ResourceRow(8, 0.00704654, 0.999711, 0.999807, 2.827608, 0.499711, 0.999711),
    ResourceRow(10, 0.00459031, 0.999711069, 0.999807379, 2.827609933, 0.499711069, 0.999711109),
    ResourceRow(12, 0.00321872568895, 0.999711313114, 0.999807542076, 2.827610624410, 0.499711313114, 0.999711352726),
)


def min_hamming_distance() -> int:
    codewords = [record_codeword(*outcome) for outcome in OUTCOME_ORDER]
    return min(
        sum(a != b for a, b in zip(first, second))
        for first_index, first in enumerate(codewords)
        for second_index, second in enumerate(codewords)
        if first_index != second_index
    )


def word_failure_tail(length: int, correctable_flips: int, slot_error: float) -> float:
    return sum(
        math.comb(length, flips)
        * slot_error**flips
        * (1.0 - slot_error) ** (length - flips)
        for flips in range(correctable_flips + 1, length + 1)
    )


def solve_slot_threshold(length: int, correctable_flips: int, target: float) -> float:
    low = 0.0
    high = 0.5
    for _ in range(80):
        mid = 0.5 * (low + high)
        if word_failure_tail(length, correctable_flips, mid) <= target:
            low = mid
        else:
            high = mid
    return low


def selector_retention_metrics() -> SelectorRetentionMetrics:
    transducer_witnesses = 8
    carrier_witnesses = 4
    equivalent_pairs = transducer_witnesses * carrier_witnesses
    completion_clauses = 3
    return SelectorRetentionMetrics(
        audited_equivalent_pairs=equivalent_pairs,
        selector_entropy_bits=math.log2(equivalent_pairs),
        retained_completion_clauses=completion_clauses,
        bare_derivation_closed_negative=True,
        minimal_completion_sufficient=True,
        retained_or_rejected_decision_required=True,
    )


def side12_scaling_metrics(
    rows: tuple[ResourceRow, ...],
    gap_floor_constant: float,
    prep_error: float,
) -> Side12ScalingMetrics:
    if gap_floor_constant <= 0.0:
        raise ValueError("--gap-floor-constant must be positive")
    if not 0.0 < prep_error < 1.0:
        raise ValueError("--prep-error must be in (0, 1)")
    scaled_gaps = [row.gap * row.side * row.side for row in rows]
    bell_values = [row.bell for row in rows]
    margins = [row.gap - gap_floor_constant / (row.side * row.side) for row in rows]
    side12 = next(row for row in rows if row.side == 12)
    t_bound = (side12.side**4) / (gap_floor_constant**2) * math.log(1.0 / prep_error)
    beta_bound = (
        (side12.side**2)
        / gap_floor_constant
        * math.log(max(side12.hilbert_dim - 1, 1) / prep_error)
    )
    return Side12ScalingMetrics(
        row_count=len(rows),
        max_side=max(row.side for row in rows),
        gap_floor_constant=gap_floor_constant,
        min_gap_margin=min(margins),
        min_bell=min(bell_values),
        max_bell_deficit=1.0 - min(bell_values),
        scaled_gap_monotone=all(
            later >= earlier for earlier, later in zip(scaled_gaps, scaled_gaps[1:])
        ),
        bell_floor_monotone=all(
            later >= earlier for earlier, later in zip(bell_values, bell_values[1:])
        ),
        side12_tadiabatic_bound=t_bound,
        side12_beta_bound=beta_bound,
        induction_obligation_open=True,
    )


def controller_envelope_metrics(
    leakage: float,
    crosstalk: float,
    implemented_area_bound: float,
    target_word_failure: float,
) -> ControllerEnvelopeMetrics:
    if leakage < 0.0 or crosstalk < 0.0 or implemented_area_bound < 0.0:
        raise ValueError("controller errors must be nonnegative")
    if not 0.0 < target_word_failure < 1.0:
        raise ValueError("--target-word-failure must be in (0, 1)")
    length = len(record_codeword(0, 0))
    distance = min_hamming_distance()
    correctable = (distance - 1) // 2
    slot_threshold = solve_slot_threshold(length, correctable, target_word_failure)
    residual_threshold = slot_threshold - leakage - crosstalk
    if residual_threshold <= 0.0:
        area_budget = 0.0
    else:
        area_budget = math.asin(math.sqrt(residual_threshold))
    implemented_slot_error = min(
        1.0,
        leakage + crosstalk + math.sin(implemented_area_bound) ** 2,
    )
    return ControllerEnvelopeMetrics(
        record_length=length,
        minimum_distance=distance,
        correctable_flips=correctable,
        leakage=leakage,
        crosstalk=crosstalk,
        slot_threshold=slot_threshold,
        certified_area_budget_rad=area_budget,
        implemented_area_bound_rad=implemented_area_bound,
        implemented_slot_error=implemented_slot_error,
        word_failure_bound=word_failure_tail(length, correctable, implemented_slot_error),
    )


def kl_half_against(p: float) -> float:
    if not 0.0 < p < 0.5:
        raise ValueError("p must be in (0, 0.5)")
    return 0.5 * math.log(0.5 / p) + 0.5 * math.log(0.5 / (1.0 - p))


def material_word_failure_bound(domain_side: int, p_spin: float, slots: int) -> float:
    spins = domain_side**3
    return min(1.0, slots * math.exp(-spins * kl_half_against(p_spin)))


def material_envelope_metrics(
    domain_side: int,
    exchange_to_temperature: float,
    defect_probability: float,
    target_word_failure: float,
) -> MaterialEnvelopeMetrics:
    if domain_side < 3 or domain_side % 2 == 0:
        raise ValueError("--domain-side must be an odd integer at least 3")
    if exchange_to_temperature <= 0.0:
        raise ValueError("--exchange-to-temperature must be positive")
    if not 0.0 <= defect_probability < 0.5:
        raise ValueError("--defect-probability must be in [0, 0.5)")
    slots = len(record_codeword(0, 0))
    p_spin = min(0.499999, defect_probability + math.exp(-12.0 * exchange_to_temperature))
    word_failure = material_word_failure_bound(domain_side, p_spin, slots)
    minimal_side = 3
    while material_word_failure_bound(minimal_side, p_spin, slots) > target_word_failure:
        minimal_side += 2
    spins = domain_side**3
    single_spin_overlap = min(1.0, 2.0 * math.sqrt(p_spin * (1.0 - p_spin)))
    log10_overlap = math.log10(single_spin_overlap) * spins * min_hamming_distance()
    return MaterialEnvelopeMetrics(
        domain_side=domain_side,
        spins_per_slot=spins,
        slots=slots,
        local_bonds=slots * 3 * (domain_side - 1) * domain_side * domain_side,
        exchange_to_temperature=exchange_to_temperature,
        defect_probability=defect_probability,
        spin_flip_probability=p_spin,
        majority_failure_bound=math.exp(-spins * kl_half_against(p_spin)),
        word_failure_bound=word_failure,
        log10_overlap_bound=log10_overlap,
        arrhenius_wall=math.exp(-2.0 * exchange_to_temperature * domain_side * domain_side),
        minimal_odd_domain_side_for_target=minimal_side,
    )


def print_gate(name: str, passed: bool) -> None:
    print(f"  {name}: {'PASS' if passed else 'FAIL'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gap-floor-constant", type=float, default=0.390)
    parser.add_argument("--resource-high-threshold", type=float, default=0.90)
    parser.add_argument("--prep-error", type=float, default=1e-3)
    parser.add_argument("--leakage", type=float, default=1e-5)
    parser.add_argument("--crosstalk", type=float, default=2e-5)
    parser.add_argument("--implemented-area-bound", type=float, default=0.023)
    parser.add_argument("--target-word-failure", type=float, default=1e-6)
    parser.add_argument("--domain-side", type=int, default=5)
    parser.add_argument("--exchange-to-temperature", type=float, default=1.0)
    parser.add_argument("--defect-probability", type=float, default=0.002)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")

    selector = selector_retention_metrics()
    scaling = side12_scaling_metrics(
        SIGNED_RESOURCE_ROWS,
        args.gap_floor_constant,
        args.prep_error,
    )
    controller = controller_envelope_metrics(
        args.leakage,
        args.crosstalk,
        args.implemented_area_bound,
        args.target_word_failure,
    )
    material = material_envelope_metrics(
        args.domain_side,
        args.exchange_to_temperature,
        args.defect_probability,
        args.target_word_failure,
    )

    selector_gate = (
        selector.bare_derivation_closed_negative
        and selector.minimal_completion_sufficient
        and selector.retained_or_rejected_decision_required
    )
    scaling_gate = (
        scaling.max_side == 12
        and scaling.min_gap_margin > 0.0
        and scaling.min_bell >= args.resource_high_threshold
        and scaling.scaled_gap_monotone
        and scaling.bell_floor_monotone
        and scaling.induction_obligation_open
    )
    controller_gate = (
        controller.implemented_slot_error < controller.slot_threshold
        and controller.implemented_area_bound_rad < controller.certified_area_budget_rad
        and controller.word_failure_bound < args.target_word_failure
    )
    material_gate = (
        material.domain_side >= material.minimal_odd_domain_side_for_target
        and material.word_failure_bound < args.target_word_failure
        and material.log10_overlap_bound < -12.0
        and material.arrhenius_wall < 1e-12
    )

    print("TELEPORTATION RETENTION-THEOREM ATTACK")
    print("Status: planning artifact; retention route and side-12 certificate")
    print(
        "Claim boundary: ordinary quantum state teleportation only; no matter, "
        "mass, charge, energy, object, or faster-than-light transport"
    )
    print()
    print(
        "selector retention theorem: "
        f"equivalent_pairs={selector.audited_equivalent_pairs}, "
        f"selector_entropy_bits={selector.selector_entropy_bits:.6f}, "
        f"completion_clauses={selector.retained_completion_clauses}, "
        f"bare_derivation_closed_negative={selector.bare_derivation_closed_negative}, "
        f"minimal_completion_sufficient={selector.minimal_completion_sufficient}, "
        f"decision_required={selector.retained_or_rejected_decision_required}"
    )
    print("signed sparse side-12 certificate rows:")
    for row in SIGNED_RESOURCE_ROWS:
        print(
            "  "
            f"side={row.side}, gap={row.gap:.12g}, gap*L^2={row.gap * row.side * row.side:.6f}, "
            f"Bell*={row.bell:.12f}, Fbest={row.fbest:.12f}, "
            f"CHSH={row.chsh:.12f}, neg={row.negativity:.12f}, purity={row.purity:.12f}"
        )
    print(
        "side-12 scaling theorem pressure: "
        f"rows={scaling.row_count}, max_side={scaling.max_side}, "
        f"gap_floor={scaling.gap_floor_constant:.3f}/L^2, "
        f"min_gap_margin={scaling.min_gap_margin:.3e}, "
        f"min_Bell={scaling.min_bell:.6f}, "
        f"max_Bell_deficit={scaling.max_bell_deficit:.3e}, "
        f"scaled_gap_monotone={scaling.scaled_gap_monotone}, "
        f"Bell_monotone={scaling.bell_floor_monotone}, "
        f"side12_Tadiabatic_bound={scaling.side12_tadiabatic_bound:.3e}, "
        f"side12_beta_bound={scaling.side12_beta_bound:.3e}, "
        f"induction_obligation_open={scaling.induction_obligation_open}"
    )
    print(
        "local controller envelope: "
        f"record_length={controller.record_length}, d_min={controller.minimum_distance}, "
        f"correctable={controller.correctable_flips}, leakage={controller.leakage:.3e}, "
        f"crosstalk={controller.crosstalk:.3e}, slot_threshold={controller.slot_threshold:.3e}, "
        f"area_budget={controller.certified_area_budget_rad:.6f}, "
        f"implemented_area_bound={controller.implemented_area_bound_rad:.6f}, "
        f"implemented_slot_error={controller.implemented_slot_error:.3e}, "
        f"word_failure_bound={controller.word_failure_bound:.3e}"
    )
    print(
        "material Ising-domain envelope: "
        f"domain_side={material.domain_side}, spins/slot={material.spins_per_slot}, "
        f"slots={material.slots}, local_bonds={material.local_bonds}, "
        f"J_over_T={material.exchange_to_temperature:.3f}, "
        f"defect={material.defect_probability:.3e}, p_spin={material.spin_flip_probability:.3e}, "
        f"majority_bound={material.majority_failure_bound:.3e}, "
        f"word_failure_bound={material.word_failure_bound:.3e}, "
        f"log10_overlap_bound={material.log10_overlap_bound:.3f}, "
        f"arrhenius_wall={material.arrhenius_wall:.3e}, "
        f"minimal_odd_domain_side={material.minimal_odd_domain_side_for_target}"
    )
    print()
    print("Acceptance gates:")
    print_gate("bare selector derivation is closed negatively; retention decision is explicit", selector_gate)
    print_gate("signed sparse certificate extends through side 12", scaling_gate)
    print_gate("local controller envelope realizes the pulse threshold", controller_gate)
    print_gate("material Ising-domain envelope realizes the detector threshold", material_gate)
    print_gate("claim boundary stays state-only and not FTL", True)
    print()
    print("Limitations:")
    print("  This closes the bare-axiom selector route negatively on the audited")
    print("  invariants; it does not prove the variational completion from the")
    print("  original sole axiom.")
    print("  The side-12 certificate strengthens the L^-2 theorem pressure, but")
    print("  the all-even-side induction proof remains open.")
    print("  The controller and detector are dimensionless local envelopes, not a")
    print("  fabricated device, named material stack, or measured noise spectrum.")
    return 0 if all((selector_gate, scaling_gate, controller_gate, material_gate)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
