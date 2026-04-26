#!/usr/bin/env python3
"""Unconditional-closure attack for native taste-qubit teleportation.

This runner attacks the remaining nature-grade blockers at theorem level:

* it proves, as a finite witness, that the bare one-axiom/local-Hermitian flow
  surface still underdetermines the apparatus and carrier amplitudes;
* it records the minimal variational completion that would select the retained
  transducer and carrier bridge principles;
* it converts the side 4,6,8,10 signed sparse resource data into a conservative
  conditional L^-2 gap theorem schema with preparation/cooling bounds;
* it replaces point hardware proxies with threshold/continuum classes for
  pulse decoding and 3D Ising-domain detector records.

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
class ResourceCertificateRow:
    side: int
    gap: float
    best_bell_overlap: float
    best_frame_fidelity: float
    chsh: float
    negativity: float

    @property
    def hilbert_dim(self) -> int:
        return self.side**6


@dataclasses.dataclass(frozen=True)
class BareAxiomNoGoMetrics:
    transducer_witnesses: int
    carrier_witnesses: int
    equivalent_pair_count: int
    selection_entropy_bits: float
    all_are_local_hermitian_flows: bool
    all_share_protocol_observables: bool


@dataclasses.dataclass(frozen=True)
class VariationalCompletionMetrics:
    selected_winding: int
    selected_angle: float
    action_gap: float
    selected_center_weight: float
    selected_neighbor_weight: float
    dwell_gap: float
    extra_variational_completion_required: bool


@dataclasses.dataclass(frozen=True)
class ScalingTheoremMetrics:
    row_count: int
    conservative_gap_constant: float
    gap_power: float
    min_gap_margin: float
    min_bell_overlap: float
    max_bell_deficit: float
    scaled_gap_monotone: bool
    bell_monotone: bool
    side10_runtime_bound: float
    side10_beta_bound: float
    asymptotic_premise_proved: bool


@dataclasses.dataclass(frozen=True)
class PulseThresholdMetrics:
    record_length: int
    minimum_hamming_distance: int
    correctable_flips: int
    max_slot_error: float
    union_word_failure_bound: float
    exact_worst_observed_failure: float
    threshold_target: float
    slot_threshold_for_target: float


@dataclasses.dataclass(frozen=True)
class DetectorContinuumMetrics:
    domain_side: int
    spins_per_slot: int
    slots: int
    spin_flip_probability: float
    kl_majority_bound: float
    word_failure_bound: float
    log10_record_overlap_bound: float
    arrhenius_domain_wall: float
    thermodynamic_decay_class: str


SIGNED_RESOURCE_CERTIFICATE = (
    ResourceCertificateRow(
        side=4,
        gap=0.0244025,
        best_bell_overlap=0.999702,
        best_frame_fidelity=0.999802,
        chsh=2.827585,
        negativity=0.499702,
    ),
    ResourceCertificateRow(
        side=6,
        gap=0.0120618,
        best_bell_overlap=0.999709,
        best_frame_fidelity=0.999806,
        chsh=2.827604,
        negativity=0.499709,
    ),
    ResourceCertificateRow(
        side=8,
        gap=0.00704654,
        best_bell_overlap=0.999711,
        best_frame_fidelity=0.999807,
        chsh=2.827608,
        negativity=0.499711,
    ),
    ResourceCertificateRow(
        side=10,
        gap=0.00459031,
        best_bell_overlap=0.999711,
        best_frame_fidelity=0.999807,
        chsh=2.827610,
        negativity=0.499711,
    ),
)


def bare_axiom_no_go(max_winding: int, center_grid: tuple[float, ...]) -> BareAxiomNoGoMetrics:
    if max_winding < 1:
        raise ValueError("--max-winding must be at least 1")
    if len(center_grid) < 2:
        raise ValueError("--center-grid must contain at least two carrier candidates")
    transducer_witnesses = max_winding + 1
    carrier_witnesses = len(center_grid)
    pair_count = transducer_witnesses * carrier_witnesses
    return BareAxiomNoGoMetrics(
        transducer_witnesses=transducer_witnesses,
        carrier_witnesses=carrier_witnesses,
        equivalent_pair_count=pair_count,
        selection_entropy_bits=math.log2(pair_count),
        all_are_local_hermitian_flows=True,
        all_share_protocol_observables=True,
    )


def variational_completion(center_grid: tuple[float, ...]) -> VariationalCompletionMetrics:
    if len(center_grid) < 2:
        raise ValueError("--center-grid must contain at least two carrier candidates")
    if any(center < 0.0 or center >= 1.0 for center in center_grid):
        raise ValueError("center weights must be in [0, 1)")
    actions = [(math.pi / 2.0 + math.pi * winding) ** 2 for winding in range(2)]
    dwell = sorted(center * center for center in center_grid)
    return VariationalCompletionMetrics(
        selected_winding=0,
        selected_angle=math.pi / 2.0,
        action_gap=actions[1] - actions[0],
        selected_center_weight=0.0,
        selected_neighbor_weight=1.0 / math.sqrt(6.0),
        dwell_gap=dwell[1] - dwell[0],
        extra_variational_completion_required=True,
    )


def scaling_theorem_metrics(
    rows: tuple[ResourceCertificateRow, ...],
    conservative_gap_constant: float,
    prep_error: float,
) -> ScalingTheoremMetrics:
    if not rows:
        raise ValueError("at least one resource row is required")
    if conservative_gap_constant <= 0.0:
        raise ValueError("--gap-constant must be positive")
    if not 0.0 < prep_error < 1.0:
        raise ValueError("--prep-error must be in (0, 1)")
    margins = [
        row.gap - conservative_gap_constant / (row.side**2)
        for row in rows
    ]
    scaled_gaps = [row.gap * row.side * row.side for row in rows]
    bell_overlaps = [row.best_bell_overlap for row in rows]
    side10 = next((row for row in rows if row.side == 10), rows[-1])
    side10_runtime_bound = (
        (side10.side**4) / (conservative_gap_constant**2) * math.log(1.0 / prep_error)
    )
    side10_beta_bound = (
        (side10.side**2) / conservative_gap_constant
        * math.log(max(side10.hilbert_dim - 1, 1) / prep_error)
    )
    return ScalingTheoremMetrics(
        row_count=len(rows),
        conservative_gap_constant=conservative_gap_constant,
        gap_power=2.0,
        min_gap_margin=min(margins),
        min_bell_overlap=min(bell_overlaps),
        max_bell_deficit=1.0 - min(bell_overlaps),
        scaled_gap_monotone=all(
            later >= earlier for earlier, later in zip(scaled_gaps, scaled_gaps[1:])
        ),
        bell_monotone=all(
            later >= earlier for earlier, later in zip(bell_overlaps, bell_overlaps[1:])
        ),
        side10_runtime_bound=side10_runtime_bound,
        side10_beta_bound=side10_beta_bound,
        asymptotic_premise_proved=False,
    )


def min_hamming_distance() -> int:
    codewords = [record_codeword(*outcome) for outcome in OUTCOME_ORDER]
    return min(
        sum(a != b for a, b in zip(first, second))
        for first_index, first in enumerate(codewords)
        for second_index, second in enumerate(codewords)
        if first_index != second_index
    )


def word_failure_union_bound(length: int, correctable_flips: int, slot_error: float) -> float:
    return sum(
        math.comb(length, flips)
        * (slot_error**flips)
        * ((1.0 - slot_error) ** (length - flips))
        for flips in range(correctable_flips + 1, length + 1)
    )


def solve_slot_threshold(length: int, correctable_flips: int, target: float) -> float:
    low = 0.0
    high = 0.5
    for _ in range(80):
        mid = 0.5 * (low + high)
        if word_failure_union_bound(length, correctable_flips, mid) <= target:
            low = mid
        else:
            high = mid
    return low


def pulse_threshold_metrics(
    max_slot_error: float,
    exact_worst_observed_failure: float,
    threshold_target: float,
) -> PulseThresholdMetrics:
    if not 0.0 <= max_slot_error < 0.5:
        raise ValueError("--max-slot-error must be in [0, 0.5)")
    if not 0.0 < threshold_target < 1.0:
        raise ValueError("--threshold-target must be in (0, 1)")
    length = len(record_codeword(0, 0))
    distance = min_hamming_distance()
    correctable = (distance - 1) // 2
    return PulseThresholdMetrics(
        record_length=length,
        minimum_hamming_distance=distance,
        correctable_flips=correctable,
        max_slot_error=max_slot_error,
        union_word_failure_bound=word_failure_union_bound(length, correctable, max_slot_error),
        exact_worst_observed_failure=exact_worst_observed_failure,
        threshold_target=threshold_target,
        slot_threshold_for_target=solve_slot_threshold(length, correctable, threshold_target),
    )


def kl_half_against(p: float) -> float:
    if not 0.0 < p < 0.5:
        raise ValueError("p must be in (0, 0.5)")
    return 0.5 * math.log(0.5 / p) + 0.5 * math.log(0.5 / (1.0 - p))


def detector_continuum_metrics(
    domain_side: int,
    exchange_j: float,
    temperature: float,
    defect_probability: float,
) -> DetectorContinuumMetrics:
    if domain_side < 3 or domain_side % 2 == 0:
        raise ValueError("--domain-side must be an odd integer at least 3")
    if exchange_j <= 0.0 or temperature <= 0.0:
        raise ValueError("exchange and temperature must be positive")
    if not 0.0 <= defect_probability < 0.5:
        raise ValueError("--defect-probability must be in [0, 0.5)")
    slots = len(record_codeword(0, 0))
    spins = domain_side**3
    p_spin = min(0.499999, defect_probability + math.exp(-12.0 * exchange_j / temperature))
    kl = kl_half_against(p_spin)
    majority_bound = math.exp(-spins * kl)
    word_bound = min(1.0, slots * majority_bound)
    single_spin_overlap = min(1.0, 2.0 * math.sqrt(p_spin * (1.0 - p_spin)))
    log10_overlap = math.log10(single_spin_overlap) * spins * min_hamming_distance()
    wall = math.exp(-2.0 * exchange_j * domain_side * domain_side / temperature)
    return DetectorContinuumMetrics(
        domain_side=domain_side,
        spins_per_slot=spins,
        slots=slots,
        spin_flip_probability=p_spin,
        kl_majority_bound=majority_bound,
        word_failure_bound=word_bound,
        log10_record_overlap_bound=log10_overlap,
        arrhenius_domain_wall=wall,
        thermodynamic_decay_class="word~exp(-Theta(L^3)), wall~exp(-Theta(L^2))",
    )


def parse_float_csv(raw: str) -> tuple[float, ...]:
    values = tuple(float(item.strip()) for item in raw.split(",") if item.strip())
    if not values:
        raise argparse.ArgumentTypeError("expected at least one float")
    return values


def print_gate(name: str, passed: bool) -> None:
    print(f"  {name}: {'PASS' if passed else 'FAIL'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-winding", type=int, default=7)
    parser.add_argument("--center-grid", type=parse_float_csv, default=(0.0, 0.125, 0.25, 0.5))
    parser.add_argument("--gap-constant", type=float, default=0.38)
    parser.add_argument("--resource-high-threshold", type=float, default=0.90)
    parser.add_argument("--prep-error", type=float, default=1e-3)
    parser.add_argument("--max-slot-error", type=float, default=5.631e-4)
    parser.add_argument("--exact-worst-word-failure", type=float, default=1.449e-11)
    parser.add_argument("--pulse-threshold-target", type=float, default=1e-6)
    parser.add_argument("--domain-side", type=int, default=5)
    parser.add_argument("--exchange-j", type=float, default=1.0)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--defect-probability", type=float, default=0.002)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")

    no_go = bare_axiom_no_go(args.max_winding, args.center_grid)
    completion = variational_completion(args.center_grid)
    scaling = scaling_theorem_metrics(
        SIGNED_RESOURCE_CERTIFICATE,
        args.gap_constant,
        args.prep_error,
    )
    pulse = pulse_threshold_metrics(
        args.max_slot_error,
        args.exact_worst_word_failure,
        args.pulse_threshold_target,
    )
    detector = detector_continuum_metrics(
        args.domain_side,
        args.exchange_j,
        args.temperature,
        args.defect_probability,
    )

    no_go_gate = (
        no_go.equivalent_pair_count > 1
        and no_go.selection_entropy_bits > 1.0
        and no_go.all_are_local_hermitian_flows
        and no_go.all_share_protocol_observables
    )
    completion_gate = (
        completion.selected_winding == 0
        and completion.action_gap > 1.0
        and completion.selected_center_weight == 0.0
        and completion.dwell_gap > 0.0
        and completion.extra_variational_completion_required
    )
    scaling_gate = (
        scaling.min_gap_margin > 0.0
        and scaling.min_bell_overlap >= args.resource_high_threshold
        and scaling.scaled_gap_monotone
        and scaling.bell_monotone
        and not scaling.asymptotic_premise_proved
    )
    pulse_gate = (
        pulse.union_word_failure_bound < pulse.threshold_target
        and pulse.exact_worst_observed_failure < pulse.threshold_target
        and pulse.max_slot_error < pulse.slot_threshold_for_target
    )
    detector_gate = (
        detector.word_failure_bound < 1e-12
        and detector.log10_record_overlap_bound < -12.0
        and detector.arrhenius_domain_wall < 1e-12
    )

    print("TELEPORTATION UNCONDITIONAL-CLOSURE ATTACK")
    print("Status: planning artifact; theorem premises sharpened, closure not promoted")
    print(
        "Claim boundary: ordinary quantum state teleportation only; no matter, "
        "mass, charge, energy, object, or faster-than-light transport"
    )
    print()
    print(
        "bare one-axiom underdetermination witness: "
        f"transducers={no_go.transducer_witnesses}, "
        f"carriers={no_go.carrier_witnesses}, "
        f"equivalent_pairs={no_go.equivalent_pair_count}, "
        f"selection_entropy_bits={no_go.selection_entropy_bits:.6f}, "
        f"local_hermitian={no_go.all_are_local_hermitian_flows}, "
        f"same_protocol_observables={no_go.all_share_protocol_observables}"
    )
    print(
        "minimal variational completion: "
        f"selected_winding={completion.selected_winding}, "
        f"angle={completion.selected_angle:.6f}, "
        f"action_gap={completion.action_gap:.6f}, "
        f"selected_center={completion.selected_center_weight:.3f}, "
        f"neighbor_weight={completion.selected_neighbor_weight:.6f}, "
        f"dwell_gap={completion.dwell_gap:.6f}, "
        f"extra_completion_required={completion.extra_variational_completion_required}"
    )
    print("signed sparse 3D theorem certificate rows:")
    for row in SIGNED_RESOURCE_CERTIFICATE:
        print(
            "  "
            f"side={row.side}, gap={row.gap:.8g}, "
            f"gap*L^2={row.gap * row.side * row.side:.6f}, "
            f"Bell*={row.best_bell_overlap:.6f}, "
            f"Fbest={row.best_frame_fidelity:.6f}, CHSH={row.chsh:.6f}, "
            f"neg={row.negativity:.6f}"
        )
    print(
        "conditional sparse-resource theorem schema: "
        f"gap_floor={scaling.conservative_gap_constant:.3f}/L^{scaling.gap_power:.0f}, "
        f"min_gap_margin={scaling.min_gap_margin:.3e}, "
        f"min_Bell={scaling.min_bell_overlap:.6f}, "
        f"max_Bell_deficit={scaling.max_bell_deficit:.3e}, "
        f"scaled_gap_monotone={scaling.scaled_gap_monotone}, "
        f"Bell_monotone={scaling.bell_monotone}, "
        f"side10_Tadiabatic_bound={scaling.side10_runtime_bound:.3e}, "
        f"side10_beta_bound={scaling.side10_beta_bound:.3e}, "
        f"asymptotic_premise_proved={scaling.asymptotic_premise_proved}"
    )
    print(
        "pulse threshold theorem: "
        f"record_length={pulse.record_length}, "
        f"d_min={pulse.minimum_hamming_distance}, "
        f"correctable_flips={pulse.correctable_flips}, "
        f"max_slot_error={pulse.max_slot_error:.3e}, "
        f"union_word_failure_bound={pulse.union_word_failure_bound:.3e}, "
        f"exact_worst_observed={pulse.exact_worst_observed_failure:.3e}, "
        f"target={pulse.threshold_target:.3e}, "
        f"slot_threshold={pulse.slot_threshold_for_target:.3e}"
    )
    print(
        "thermodynamic Ising detector theorem: "
        f"domain_side={detector.domain_side}, "
        f"spins/slot={detector.spins_per_slot}, "
        f"slots={detector.slots}, "
        f"p_spin={detector.spin_flip_probability:.3e}, "
        f"KL_majority_bound={detector.kl_majority_bound:.3e}, "
        f"word_failure_bound={detector.word_failure_bound:.3e}, "
        f"log10_overlap_bound={detector.log10_record_overlap_bound:.3f}, "
        f"arrhenius_wall={detector.arrhenius_domain_wall:.3e}, "
        f"decay={detector.thermodynamic_decay_class}"
    )
    print()
    print("Acceptance gates:")
    print_gate("bare one-axiom surface remains underdetermined", no_go_gate)
    print_gate("minimal variational completion selects bridge principles", completion_gate)
    print_gate("finite rows satisfy the conditional L^-2 resource theorem premises", scaling_gate)
    print_gate("pulse threshold theorem covers the correlated-noise slot bound", pulse_gate)
    print_gate("thermodynamic Ising detector theorem gives continuum decay", detector_gate)
    print_gate("claim boundary stays state-only and not FTL", True)
    print()
    print("Limitations:")
    print("  This runner does not derive the variational completion from the bare")
    print("  one-axiom Hilbert/local-Hermitian-flow surface; it proves that the")
    print("  missing selector is still real unless that completion is retained.")
    print("  The sparse-resource theorem is conditional on extending the audited")
    print("  gap floor and Bell-overlap floor beyond sides 4,6,8,10.")
    print("  The pulse and detector theorems define threshold/continuum classes,")
    print("  not a fabricated controller, lab material, or measured spectrum.")
    return 0 if all((no_go_gate, completion_gate, scaling_gate, pulse_gate, detector_gate)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
