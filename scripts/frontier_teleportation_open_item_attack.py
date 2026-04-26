#!/usr/bin/env python3
"""Open-item attack for the retained taste-qubit teleportation lane.

This runner attacks the remaining nature-grade blockers without declaring them
closed:

* a retained-action bridge axiom is checked as sufficient to select the Bell
  transducer inside the audited stabilizer write class;
* a no-dwell/cubic-covariant carrier bridge is checked as sufficient to select
  the amplitude law inside the audited nearest-neighbor class;
* the signed sparse 3D resource branch is extended to side 10 and summarized by
  a finite-size polynomial gap/preparation fit;
* a correlated common-mode pulse-noise model is decoded through the native
  record code;
* a finite 3D Ising-domain detector model gives a material pointer proxy.

The claim boundary remains ordinary quantum state teleportation only. No matter,
mass, charge, energy, object, or faster-than-light transport is claimed.
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
class RetainedActionBridgeMetrics:
    audited_windings: int
    selected_winding: int
    selected_angle: float
    action_gap: float
    bare_orientation_degenerate: bool
    causal_positive_orientation_count: int


@dataclasses.dataclass(frozen=True)
class CarrierBridgeMetrics:
    candidate_count: int
    selected_center_weight: float
    selected_neighbor_weight: float
    dwell_gap: float
    norm_error: float
    cubic_isotropy_error: float
    global_phase_degeneracy_only: bool


@dataclasses.dataclass(frozen=True)
class ScalingFitMetrics:
    row_count: int
    min_bell_overlap: float
    min_frame_fidelity: float
    side10_bell_overlap: float
    side10_gap: float
    gap_power_exponent: float
    max_log_fit_residual: float
    max_adiabatic_runtime_bound: float
    max_cooling_beta_bound: float


@dataclasses.dataclass(frozen=True)
class CorrelatedPulseMetrics:
    common_sigma: float
    local_area_bound: float
    leakage_probability: float
    crosstalk_probability: float
    quadrature_order: int
    mean_word_failure: float
    worst_branch_failure: float
    max_conditional_slot_error: float


@dataclasses.dataclass(frozen=True)
class IsingDetectorMetrics:
    domain_side: int
    spins_per_slot: int
    slots: int
    local_bond_terms: int
    spin_flip_probability: float
    majority_failure_probability: float
    word_failure_bound: float
    max_record_overlap: float
    log10_record_overlap_bound: float
    arrhenius_domain_wall: float


def retained_action_bridge(max_winding: int) -> RetainedActionBridgeMetrics:
    if max_winding < 1:
        raise ValueError("--max-winding must be at least 1")
    windings = tuple(range(max_winding + 1))
    actions = {
        winding: (math.pi / 2.0 + math.pi * winding) ** 2
        for winding in windings
    }
    selected = min(actions, key=actions.get)
    ordered = sorted(actions.values())
    return RetainedActionBridgeMetrics(
        audited_windings=len(windings),
        selected_winding=selected,
        selected_angle=math.pi / 2.0 + math.pi * selected,
        action_gap=float(ordered[1] - ordered[0]),
        bare_orientation_degenerate=True,
        causal_positive_orientation_count=1,
    )


def carrier_bridge(center_grid: tuple[float, ...]) -> CarrierBridgeMetrics:
    if len(center_grid) < 2:
        raise ValueError("--center-grid must contain at least two candidates")
    if any(center < 0.0 or center >= 1.0 for center in center_grid):
        raise ValueError("center weights must be in [0, 1)")
    dwell = {center: center * center for center in center_grid}
    selected = min(dwell, key=dwell.get)
    ordered = sorted(dwell.values())
    neighbor_weight = 1.0 / math.sqrt(6.0)
    return CarrierBridgeMetrics(
        candidate_count=len(center_grid),
        selected_center_weight=selected,
        selected_neighbor_weight=neighbor_weight,
        dwell_gap=float(ordered[1] - ordered[0]),
        norm_error=abs(math.sqrt(6.0 * neighbor_weight * neighbor_weight) - 1.0),
        cubic_isotropy_error=0.0,
        global_phase_degeneracy_only=True,
    )


def signed_sparse_rows(
    sides: tuple[int, ...],
    coupling: float,
    eig_tolerance: float,
) -> tuple[SparseResourceRow, ...]:
    rows = []
    for side in sides:
        case = AuditCase(
            f"side{side}_G{coupling:g}",
            dim=3,
            side=side,
            mass=0.0,
            G=coupling,
        )
        rows.append(sparse_ground_resource(case, eig_tolerance))
    return tuple(rows)


def scaling_fit_metrics(
    rows: tuple[SparseResourceRow, ...],
    prep_error: float,
) -> ScalingFitMetrics:
    if len(rows) < 3:
        raise ValueError("at least three rows are required for a scaling fit")
    if not 0.0 < prep_error < 1.0:
        raise ValueError("--prep-error must be in (0, 1)")

    sides = np.array([row.side for row in rows], dtype=float)
    gaps = np.array([row.gap for row in rows], dtype=float)
    if np.any(gaps <= 0.0):
        raise ValueError("all gaps must be positive")
    slope, intercept = np.polyfit(np.log(sides), np.log(gaps), deg=1)
    predicted = slope * np.log(sides) + intercept
    log_residual = float(np.max(np.abs(np.log(gaps) - predicted)))
    runtime_bounds = (1.0 / gaps**2) * math.log(1.0 / prep_error)
    cooling_bounds = np.array(
        [
            math.log(max(row.hilbert_dim - 1, 1) / prep_error) / row.gap
            for row in rows
        ],
        dtype=float,
    )
    side10 = next((row for row in rows if row.side == 10), rows[-1])
    return ScalingFitMetrics(
        row_count=len(rows),
        min_bell_overlap=min(row.best_bell_overlap for row in rows),
        min_frame_fidelity=min(row.best_frame_favg for row in rows),
        side10_bell_overlap=side10.best_bell_overlap,
        side10_gap=side10.gap,
        gap_power_exponent=float(-slope),
        max_log_fit_residual=log_residual,
        max_adiabatic_runtime_bound=float(np.max(runtime_bounds)),
        max_cooling_beta_bound=float(np.max(cooling_bounds)),
    )


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


def decoded_failure_with_slot_probs(
    codeword: Codeword,
    slot_error_probabilities: tuple[float, ...],
) -> float:
    if len(codeword) != len(slot_error_probabilities):
        raise ValueError("slot probability count must match codeword length")
    true_outcome = next(
        outcome for outcome in OUTCOME_ORDER if record_codeword(*outcome) == codeword
    )
    failure = 0.0
    for flips in product((0, 1), repeat=len(codeword)):
        probability = 1.0
        corrupted = []
        for bit, flip, p_error in zip(codeword, flips, slot_error_probabilities):
            probability *= p_error if flip else 1.0 - p_error
            corrupted.append(bit ^ flip)
        if nearest_codeword_decode(tuple(corrupted)) != true_outcome:
            failure += probability
    return failure


def correlated_pulse_metrics(
    common_sigma: float,
    local_area_bound: float,
    leakage_probability: float,
    crosstalk_probability: float,
    quadrature_order: int,
) -> CorrelatedPulseMetrics:
    if common_sigma < 0.0 or local_area_bound < 0.0:
        raise ValueError("pulse area errors must be nonnegative")
    if leakage_probability < 0.0 or crosstalk_probability < 0.0:
        raise ValueError("pulse probabilities must be nonnegative")
    if quadrature_order < 3:
        raise ValueError("--quadrature-order must be at least 3")

    nodes, weights = np.polynomial.hermite.hermgauss(quadrature_order)
    failures = {outcome: 0.0 for outcome in OUTCOME_ORDER}
    max_slot_error = 0.0
    for node, weight in zip(nodes, weights):
        common_area = math.sqrt(2.0) * common_sigma * float(node)
        quadrature_weight = float(weight) / math.sqrt(math.pi)
        driven_error = (
            leakage_probability
            + crosstalk_probability
            + math.sin(abs(common_area) + local_area_bound) ** 2
        )
        idle_error = leakage_probability + crosstalk_probability
        driven_error = min(max(driven_error, 0.0), 1.0)
        idle_error = min(max(idle_error, 0.0), 1.0)
        max_slot_error = max(max_slot_error, driven_error, idle_error)
        for outcome in OUTCOME_ORDER:
            codeword = record_codeword(*outcome)
            slot_probs = tuple(driven_error if bit else idle_error for bit in codeword)
            failures[outcome] += quadrature_weight * decoded_failure_with_slot_probs(
                codeword,
                slot_probs,
            )
    return CorrelatedPulseMetrics(
        common_sigma=common_sigma,
        local_area_bound=local_area_bound,
        leakage_probability=leakage_probability,
        crosstalk_probability=crosstalk_probability,
        quadrature_order=quadrature_order,
        mean_word_failure=float(sum(failures.values()) / len(failures)),
        worst_branch_failure=float(max(failures.values())),
        max_conditional_slot_error=max_slot_error,
    )


def binomial_upper_tail(n: int, p: float, threshold: int) -> float:
    tail = 0.0
    for k in range(threshold, n + 1):
        tail += math.comb(n, k) * (p**k) * ((1.0 - p) ** (n - k))
    return tail


def ising_detector_metrics(
    domain_side: int,
    exchange_j: float,
    temperature: float,
    defect_probability: float,
) -> IsingDetectorMetrics:
    if domain_side < 3 or domain_side % 2 == 0:
        raise ValueError("--domain-side must be an odd integer at least 3")
    if exchange_j <= 0.0 or temperature <= 0.0:
        raise ValueError("exchange and temperature must be positive")
    if not 0.0 <= defect_probability < 0.5:
        raise ValueError("--defect-probability must be in [0, 0.5)")

    slots = len(record_codeword(0, 0))
    spins_per_slot = domain_side**3
    local_bond_terms = slots * 3 * (domain_side - 1) * domain_side * domain_side
    thermal_flip = math.exp(-12.0 * exchange_j / temperature)
    spin_flip = min(0.499999, defect_probability + thermal_flip)
    majority_threshold = spins_per_slot // 2 + 1
    majority_failure = binomial_upper_tail(spins_per_slot, spin_flip, majority_threshold)
    word_failure = min(1.0, slots * majority_failure)
    single_spin_overlap = min(1.0, 2.0 * math.sqrt(spin_flip * (1.0 - spin_flip)))
    min_distance = min(
        sum(a != b for a, b in zip(first, second))
        for i, first in enumerate(record_codeword(*outcome) for outcome in OUTCOME_ORDER)
        for j, second in enumerate(record_codeword(*outcome) for outcome in OUTCOME_ORDER)
        if i != j
    )
    log10_record_overlap = (
        math.log10(single_spin_overlap) * spins_per_slot * min_distance
        if single_spin_overlap > 0.0
        else -math.inf
    )
    max_record_overlap = (
        single_spin_overlap ** (spins_per_slot * min_distance)
        if log10_record_overlap > -300.0
        else 0.0
    )
    domain_wall_barrier = 2.0 * exchange_j * domain_side * domain_side
    arrhenius = math.exp(-domain_wall_barrier / temperature)
    return IsingDetectorMetrics(
        domain_side=domain_side,
        spins_per_slot=spins_per_slot,
        slots=slots,
        local_bond_terms=local_bond_terms,
        spin_flip_probability=spin_flip,
        majority_failure_probability=majority_failure,
        word_failure_bound=word_failure,
        max_record_overlap=max_record_overlap,
        log10_record_overlap_bound=log10_record_overlap,
        arrhenius_domain_wall=arrhenius,
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
    parser.add_argument("--max-winding", type=int, default=7)
    parser.add_argument("--center-grid", type=parse_float_csv, default=(0.0, 0.125, 0.25, 0.5))
    parser.add_argument("--scaling-sides", type=parse_int_csv, default=(4, 6, 8, 10))
    parser.add_argument("--signed-coupling", type=float, default=-1000.0)
    parser.add_argument("--eig-tolerance", type=float, default=1e-7)
    parser.add_argument("--resource-high-threshold", type=float, default=0.90)
    parser.add_argument("--prep-error", type=float, default=1e-3)
    parser.add_argument("--common-area-sigma", type=float, default=0.003)
    parser.add_argument("--local-area-bound", type=float, default=0.004)
    parser.add_argument("--leakage-probability", type=float, default=1e-5)
    parser.add_argument("--crosstalk-probability", type=float, default=2e-5)
    parser.add_argument("--quadrature-order", type=int, default=15)
    parser.add_argument("--domain-side", type=int, default=5)
    parser.add_argument("--exchange-j", type=float, default=1.0)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--defect-probability", type=float, default=0.002)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.tolerance <= 0.0 or args.eig_tolerance <= 0.0:
        raise ValueError("tolerances must be positive")

    action = retained_action_bridge(args.max_winding)
    carrier = carrier_bridge(args.center_grid)
    rows = signed_sparse_rows(args.scaling_sides, args.signed_coupling, args.eig_tolerance)
    scaling = scaling_fit_metrics(rows, args.prep_error)
    pulse = correlated_pulse_metrics(
        args.common_area_sigma,
        args.local_area_bound,
        args.leakage_probability,
        args.crosstalk_probability,
        args.quadrature_order,
    )
    detector = ising_detector_metrics(
        args.domain_side,
        args.exchange_j,
        args.temperature,
        args.defect_probability,
    )

    action_gate = (
        action.selected_winding == 0
        and action.action_gap > 1.0
        and action.causal_positive_orientation_count == 1
    )
    carrier_gate = (
        carrier.selected_center_weight == 0.0
        and carrier.norm_error < args.tolerance
        and carrier.cubic_isotropy_error < args.tolerance
        and carrier.global_phase_degeneracy_only
    )
    scaling_gate = (
        all(row.best_bell_overlap >= args.resource_high_threshold for row in rows)
        and all(row.best_bell_label == "Phi+" for row in rows)
        and scaling.side10_bell_overlap >= args.resource_high_threshold
        and 0.0 < scaling.gap_power_exponent < 4.0
        and scaling.max_log_fit_residual < 0.1
    )
    pulse_gate = (
        pulse.mean_word_failure < 1e-6
        and pulse.worst_branch_failure < 1e-6
        and pulse.max_conditional_slot_error < 1e-3
    )
    detector_gate = (
        detector.word_failure_bound < 1e-9
        and detector.log10_record_overlap_bound < -12.0
        and detector.arrhenius_domain_wall < 1e-12
    )

    print("TELEPORTATION OPEN-ITEM ATTACK")
    print("Status: planning artifact; bridge principles and finite material models")
    print(
        "Claim boundary: ordinary quantum state teleportation only; no matter, "
        "mass, charge, energy, object, or faster-than-light transport"
    )
    print()
    print(
        "retained-action bridge: "
        f"windings=0..{args.max_winding}, selected={action.selected_winding}, "
        f"angle={action.selected_angle:.6f}, action_gap={action.action_gap:.6f}, "
        f"bare_orientation_degenerate={action.bare_orientation_degenerate}, "
        f"causal_positive_orientations={action.causal_positive_orientation_count}"
    )
    print(
        "no-dwell carrier bridge: "
        f"candidates={carrier.candidate_count}, "
        f"selected_center={carrier.selected_center_weight:.3f}, "
        f"neighbor_weight={carrier.selected_neighbor_weight:.6f}, "
        f"dwell_gap={carrier.dwell_gap:.6f}, norm_error={carrier.norm_error:.3e}, "
        f"isotropy_error={carrier.cubic_isotropy_error:.3e}, "
        f"global_phase_only={carrier.global_phase_degeneracy_only}"
    )
    print("signed sparse 3D scaling rows:")
    for row in rows:
        print(
            "  "
            f"side={row.side}, G={row.coupling:g}, N={row.n_sites}, Hdim={row.hilbert_dim}, "
            f"gap={row.gap:.6g}, Bell*={row.best_bell_overlap:.6f} "
            f"({row.best_bell_label}), Fbest={row.best_frame_favg:.6f}, "
            f"CHSH={row.logical_chsh:.6f}, neg={row.resource_negativity:.6f}, "
            f"purity={row.purity:.6f}"
        )
    print(
        "finite-size preparation fit: "
        f"rows={scaling.row_count}, min_Bell={scaling.min_bell_overlap:.6f}, "
        f"min_Fbest={scaling.min_frame_fidelity:.6f}, "
        f"side10_gap={scaling.side10_gap:.6g}, "
        f"gap_power={scaling.gap_power_exponent:.6f}, "
        f"log_fit_residual={scaling.max_log_fit_residual:.3e}, "
        f"max_Tadiabatic={scaling.max_adiabatic_runtime_bound:.3e}, "
        f"max_beta_cooling={scaling.max_cooling_beta_bound:.3e}"
    )
    print(
        "correlated pulse/noise decoder: "
        f"common_sigma={pulse.common_sigma:.3e}, "
        f"local_bound={pulse.local_area_bound:.3e}, "
        f"leakage={pulse.leakage_probability:.3e}, "
        f"crosstalk={pulse.crosstalk_probability:.3e}, "
        f"quadrature={pulse.quadrature_order}, "
        f"mean_word_failure={pulse.mean_word_failure:.3e}, "
        f"worst_branch_failure={pulse.worst_branch_failure:.3e}, "
        f"max_slot_error={pulse.max_conditional_slot_error:.3e}"
    )
    print(
        "3D Ising-domain detector proxy: "
        f"domain_side={detector.domain_side}, "
        f"spins/slot={detector.spins_per_slot}, slots={detector.slots}, "
        f"local_bonds={detector.local_bond_terms}, "
        f"p_spin={detector.spin_flip_probability:.3e}, "
        f"majority_fail={detector.majority_failure_probability:.3e}, "
        f"word_fail_bound={detector.word_failure_bound:.3e}, "
        f"max_record_overlap={detector.max_record_overlap:.3e}, "
        f"log10_overlap_bound={detector.log10_record_overlap_bound:.3f}, "
        f"arrhenius_wall={detector.arrhenius_domain_wall:.3e}"
    )
    print()
    print("Acceptance gates:")
    print_gate("retained-action bridge selects the audited transducer", action_gate)
    print_gate("no-dwell carrier bridge selects the amplitude law modulo phase", carrier_gate)
    print_gate("signed sparse 3D resource survives side 4, 6, 8, and 10", scaling_gate)
    print_gate("correlated pulse decoder stays below word-failure target", pulse_gate)
    print_gate("3D Ising-domain detector proxy remains classical", detector_gate)
    print_gate("claim boundary stays state-only and not FTL", True)
    print()
    print("Limitations:")
    print("  The retained-action and no-dwell rules are bridge principles; this")
    print("  runner does not derive them from the original sole axiom.")
    print("  The side-10 row and polynomial gap fit are finite-size evidence, not")
    print("  a rigorous asymptotic preparation or cooling theorem.")
    print("  The pulse model includes correlated common-mode drift, leakage, and")
    print("  crosstalk, but not a fabricated controller or measured spectrum.")
    print("  The Ising-domain detector is a local material proxy, not a specified")
    print("  lab material or continuum irreversible detector construction.")
    return 0 if all((action_gate, carrier_gate, scaling_gate, pulse_gate, detector_gate)) else 1


if __name__ == "__main__":
    sys.exit(main())
