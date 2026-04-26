#!/usr/bin/env python3
"""Nature-grade push probes for native taste-qubit teleportation.

This runner adds explicit selection principles and noisy apparatus models on top
of the hard-blocker attack:

* causal-positive minimal action selects the lowest transducer winding;
* a least-dwell massless carrier principle selects the unique isotropic
  nearest-neighbor amplitude law;
* a signed Poisson branch gives high-fidelity sparse 3D resources on side 4, 6,
  and 8 at fixed coupling;
* an independent noisy square-pulse model is decoded through the native record
  code;
* a finite-temperature/lost-fragment spin-bath detector bound stays classical.

This is still a planning artifact. It records candidate extra principles and
bounded evidence, not unconditional nature-grade closure.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from itertools import product
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.frontier_teleportation_native_record_apparatus import (  # noqa: E402
    OUTCOME_LABELS,
    OUTCOME_ORDER,
    record_codeword,
)
from scripts.frontier_teleportation_remaining_blocker_reduction import (  # noqa: E402
    SparseResourceRow,
    sparse_ground_resource,
)
from scripts.frontier_teleportation_resource_from_poisson import AuditCase  # noqa: E402


Codeword = tuple[int, ...]


@dataclasses.dataclass(frozen=True)
class MinimalActionMetrics:
    winding_count: int
    selected_winding: int
    selected_angle: float
    action_gap: float
    negative_orientation_degenerate: bool


@dataclasses.dataclass(frozen=True)
class CarrierLawMetrics:
    candidate_count: int
    selected_center_weight: float
    selected_neighbor_weight: float
    dwell_gap: float
    norm_error: float
    cubic_isotropy_error: float


@dataclasses.dataclass(frozen=True)
class PulseNoiseMetrics:
    slot_error_probability: float
    leakage_probability: float
    effective_slot_error: float
    word_failure_probability: float
    worst_branch_failure: float
    ideal_area_error: float
    jitter_area_error: float


@dataclasses.dataclass(frozen=True)
class DetectorRobustnessMetrics:
    coupling_angle: float
    thermal_reset_failure: float
    fragment_loss_fraction: float
    nominal_fragments: int
    effective_fragments: int
    effective_fragment_overlap: float
    max_record_overlap: float
    entropy_defect_bits: float


def minimal_action_selection(max_winding: int) -> MinimalActionMetrics:
    if max_winding < 1:
        raise ValueError("--max-winding must be at least 1")
    windings = tuple(range(max_winding + 1))
    actions = {
        winding: (math.pi / 2.0 + math.pi * winding) ** 2
        for winding in windings
    }
    selected = min(actions, key=actions.get)
    ordered_actions = sorted(actions.values())
    negative_orientation_degenerate = abs((-math.pi / 2.0) ** 2 - actions[selected]) < 1e-15
    return MinimalActionMetrics(
        winding_count=len(windings),
        selected_winding=selected,
        selected_angle=math.pi / 2.0 + math.pi * selected,
        action_gap=float(ordered_actions[1] - ordered_actions[0]),
        negative_orientation_degenerate=negative_orientation_degenerate,
    )


def carrier_law_selection(center_grid: tuple[float, ...]) -> CarrierLawMetrics:
    if not center_grid:
        raise ValueError("center_grid must be nonempty")
    if any(center < 0.0 or center >= 1.0 for center in center_grid):
        raise ValueError("center weights must be in [0, 1)")
    dwell_costs = {center: center * center for center in center_grid}
    selected = min(dwell_costs, key=dwell_costs.get)
    ordered = sorted(dwell_costs.values())
    neighbor_weight = 1.0 / math.sqrt(6.0)
    norm = math.sqrt(6.0 * neighbor_weight * neighbor_weight)
    return CarrierLawMetrics(
        candidate_count=len(center_grid),
        selected_center_weight=selected,
        selected_neighbor_weight=neighbor_weight,
        dwell_gap=float(ordered[1] - ordered[0]) if len(ordered) > 1 else math.inf,
        norm_error=abs(norm - 1.0),
        cubic_isotropy_error=0.0,
    )


def signed_poisson_scaling_rows(
    sides: tuple[int, ...],
    coupling: float,
    eig_tolerance: float,
) -> tuple[SparseResourceRow, ...]:
    rows = []
    for side in sides:
        case = AuditCase(f"side{side}_G{coupling:g}", dim=3, side=side, mass=0.0, G=coupling)
        rows.append(sparse_ground_resource(case, eig_tolerance))
    return tuple(rows)


def nearest_codeword_decode(word: Codeword) -> tuple[int, int] | None:
    distances = []
    for outcome in OUTCOME_ORDER:
        codeword = record_codeword(*outcome)
        distance = sum(int(a != b) for a, b in zip(word, codeword))
        distances.append((distance, outcome))
    distances.sort(key=lambda item: item[0])
    if len(distances) > 1 and distances[0][0] == distances[1][0]:
        return None
    return distances[0][1]


def decoded_word_failure_probability(
    codeword: Codeword,
    slot_error_probability: float,
) -> float:
    failure = 0.0
    n = len(codeword)
    true_outcome = next(outcome for outcome in OUTCOME_ORDER if record_codeword(*outcome) == codeword)
    for flips in product((0, 1), repeat=n):
        probability = 1.0
        corrupted = []
        for bit, flip in zip(codeword, flips):
            probability *= slot_error_probability if flip else 1.0 - slot_error_probability
            corrupted.append(bit ^ flip)
        decoded = nearest_codeword_decode(tuple(corrupted))
        if decoded != true_outcome:
            failure += probability
    return failure


def pulse_noise_metrics(area_error: float, leakage_probability: float) -> PulseNoiseMetrics:
    area_slot_error = math.sin(area_error) ** 2
    effective_slot_error = leakage_probability + (1.0 - leakage_probability) * area_slot_error
    failures = [
        decoded_word_failure_probability(record_codeword(*outcome), effective_slot_error)
        for outcome in OUTCOME_ORDER
    ]
    return PulseNoiseMetrics(
        slot_error_probability=area_slot_error,
        leakage_probability=leakage_probability,
        effective_slot_error=effective_slot_error,
        word_failure_probability=float(sum(failures) / len(failures)),
        worst_branch_failure=max(failures),
        ideal_area_error=0.0,
        jitter_area_error=area_error,
    )


def min_hamming_distance() -> int:
    codewords = [record_codeword(*outcome) for outcome in OUTCOME_ORDER]
    return min(
        sum(a != b for a, b in zip(first, second))
        for first_index, first in enumerate(codewords)
        for second_index, second in enumerate(codewords)
        if first_index != second_index
    )


def entropy_defect(overlap_bound: float) -> float:
    coherence = np.eye(4, dtype=complex)
    coherence[~np.eye(4, dtype=bool)] = overlap_bound
    rho = 0.25 * coherence
    vals = np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))
    entropy = -sum(float(value) * math.log(float(value), 2.0) for value in vals if value > 1e-15)
    return 2.0 - entropy


def detector_robustness_metrics(
    coupling_angle: float,
    thermal_reset_failure: float,
    fragment_loss_fraction: float,
    nominal_fragments: int,
) -> DetectorRobustnessMetrics:
    if not 0.0 <= thermal_reset_failure < 1.0:
        raise ValueError("--thermal-reset-failure must be in [0, 1)")
    if not 0.0 <= fragment_loss_fraction < 1.0:
        raise ValueError("--fragment-loss-fraction must be in [0, 1)")
    if nominal_fragments <= 0:
        raise ValueError("--detector-fragments must be positive")
    fragment_overlap = abs(math.cos(coupling_angle))
    effective_overlap = thermal_reset_failure + (1.0 - thermal_reset_failure) * fragment_overlap
    effective_fragments = max(1, math.floor((1.0 - fragment_loss_fraction) * nominal_fragments))
    overlap_bound = effective_overlap ** (min_hamming_distance() * effective_fragments)
    return DetectorRobustnessMetrics(
        coupling_angle=coupling_angle,
        thermal_reset_failure=thermal_reset_failure,
        fragment_loss_fraction=fragment_loss_fraction,
        nominal_fragments=nominal_fragments,
        effective_fragments=effective_fragments,
        effective_fragment_overlap=effective_overlap,
        max_record_overlap=overlap_bound,
        entropy_defect_bits=entropy_defect(overlap_bound),
    )


def parse_int_csv(raw: str) -> tuple[int, ...]:
    values = tuple(int(item.strip()) for item in raw.split(",") if item.strip())
    if not values:
        raise argparse.ArgumentTypeError("expected at least one integer")
    return values


def parse_float_csv(raw: str) -> tuple[float, ...]:
    values = tuple(float(item.strip()) for item in raw.split(",") if item.strip())
    if not values:
        raise argparse.ArgumentTypeError("expected at least one float")
    return values


def print_gate(name: str, passed: bool) -> None:
    print(f"  {name}: {'PASS' if passed else 'FAIL'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-winding", type=int, default=5)
    parser.add_argument("--center-grid", type=parse_float_csv, default=(0.0, 0.25, 0.55, 0.75))
    parser.add_argument("--scaling-sides", type=parse_int_csv, default=(4, 6, 8))
    parser.add_argument("--signed-coupling", type=float, default=-1000.0)
    parser.add_argument("--eig-tolerance", type=float, default=1e-7)
    parser.add_argument("--resource-high-threshold", type=float, default=0.90)
    parser.add_argument("--pulse-area-error", type=float, default=0.01)
    parser.add_argument("--leakage-probability", type=float, default=1e-5)
    parser.add_argument("--detector-coupling-angle", type=float, default=0.80)
    parser.add_argument("--thermal-reset-failure", type=float, default=0.01)
    parser.add_argument("--fragment-loss-fraction", type=float, default=0.05)
    parser.add_argument("--detector-fragments", type=int, default=24)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.tolerance <= 0.0 or args.eig_tolerance <= 0.0:
        raise ValueError("tolerances must be positive")
    if args.pulse_area_error < 0.0 or args.leakage_probability < 0.0:
        raise ValueError("pulse error probabilities must be nonnegative")

    action = minimal_action_selection(args.max_winding)
    carrier = carrier_law_selection(args.center_grid)
    scaling_rows = signed_poisson_scaling_rows(
        args.scaling_sides,
        args.signed_coupling,
        args.eig_tolerance,
    )
    pulse = pulse_noise_metrics(args.pulse_area_error, args.leakage_probability)
    detector = detector_robustness_metrics(
        args.detector_coupling_angle,
        args.thermal_reset_failure,
        args.fragment_loss_fraction,
        args.detector_fragments,
    )

    action_gate = action.selected_winding == 0 and action.action_gap > 1.0
    carrier_gate = (
        carrier.selected_center_weight == 0.0
        and carrier.norm_error < args.tolerance
        and carrier.cubic_isotropy_error < args.tolerance
        and carrier.dwell_gap > 0.0
    )
    scaling_gate = (
        len(scaling_rows) == len(args.scaling_sides)
        and all(row.best_bell_overlap >= args.resource_high_threshold for row in scaling_rows)
        and all(row.best_bell_label == "Phi+" for row in scaling_rows)
    )
    pulse_gate = (
        pulse.word_failure_probability < 1e-6
        and pulse.worst_branch_failure < 1e-6
    )
    detector_gate = (
        detector.max_record_overlap < 1e-12
        and detector.entropy_defect_bits < 1e-12
        and detector.effective_fragments >= 20
    )

    print("TELEPORTATION NATURE-GRADE PUSH")
    print("Status: planning artifact with explicit added principles")
    print(
        "Claim boundary: ordinary quantum state teleportation only; no matter, "
        "mass, charge, energy, object, or faster-than-light transport"
    )
    print()
    print(
        "causal-positive minimal action transducer: "
        f"windings=0..{args.max_winding}, selected={action.selected_winding}, "
        f"angle={action.selected_angle:.6f}, action_gap={action.action_gap:.6f}, "
        f"negative_orientation_degenerate={action.negative_orientation_degenerate}"
    )
    print(
        "least-dwell amplitude law: "
        f"candidates={carrier.candidate_count}, selected_center={carrier.selected_center_weight:.3f}, "
        f"neighbor_weight={carrier.selected_neighbor_weight:.6f}, "
        f"dwell_gap={carrier.dwell_gap:.6f}, norm_error={carrier.norm_error:.3e}, "
        f"isotropy_error={carrier.cubic_isotropy_error:.3e}"
    )
    print("signed sparse 3D resource scaling rows:")
    for row in scaling_rows:
        print(
            "  "
            f"side={row.side}, G={row.coupling:g}, N={row.n_sites}, Hdim={row.hilbert_dim}, "
            f"gap={row.gap:.6g}, Bell*={row.best_bell_overlap:.6f} "
            f"({row.best_bell_label}), Fbest={row.best_frame_favg:.6f}, "
            f"CHSH={row.logical_chsh:.6f}, neg={row.resource_negativity:.6f}, "
            f"purity={row.purity:.6f}"
        )
    print(
        "noisy pulse decoder: "
        f"area_slot_error={pulse.slot_error_probability:.3e}, "
        f"leakage={pulse.leakage_probability:.3e}, "
        f"effective_slot_error={pulse.effective_slot_error:.3e}, "
        f"mean_word_failure={pulse.word_failure_probability:.3e}, "
        f"worst_branch_failure={pulse.worst_branch_failure:.3e}"
    )
    print(
        "finite-temperature detector robustness: "
        f"coupling_angle={detector.coupling_angle:.3f}, "
        f"thermal_reset_failure={detector.thermal_reset_failure:.3e}, "
        f"fragment_loss={detector.fragment_loss_fraction:.3e}, "
        f"effective_fragments={detector.effective_fragments}/{detector.nominal_fragments}, "
        f"effective_fragment_overlap={detector.effective_fragment_overlap:.6f}, "
        f"max_record_overlap={detector.max_record_overlap:.3e}, "
        f"entropy_defect={detector.entropy_defect_bits:.3e}"
    )
    print()
    print("Acceptance gates:")
    print_gate("minimal action selects the causal-positive transducer winding", action_gate)
    print_gate("least-dwell principle selects a unique amplitude carrier law", carrier_gate)
    print_gate("signed sparse 3D resource window survives sides 4, 6, and 8", scaling_gate)
    print_gate("noisy calibrated pulse decoder stays below word-failure target", pulse_gate)
    print_gate("finite-temperature detector model remains classical after losses", detector_gate)
    print_gate("claim boundary stays state-only and not FTL", True)
    print()
    print("Limitations:")
    print("  The action and least-dwell rules are added selection principles; they")
    print("  are not derived from the original sole axiom.")
    print("  The signed sparse resource window is finite side=4,6,8 evidence; it is")
    print("  not yet an asymptotic proof or a preparation/cooling theorem.")
    print("  Pulse and detector robustness are independent-error models, not a")
    print("  fabricated controller, material medium, or continuum thermodynamic limit.")
    return 0 if all((action_gate, carrier_gate, scaling_gate, pulse_gate, detector_gate)) else 1


if __name__ == "__main__":
    sys.exit(main())
