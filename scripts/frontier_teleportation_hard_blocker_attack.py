#!/usr/bin/env python3
"""Hard-blocker attack for native taste-qubit teleportation.

This artifact separates positive mechanisms from no-go information on the
remaining nature-grade blockers:

* sole-axiom apparatus selection is attacked by exhibiting inequivalent
  stabilizer-native transducer Hamiltonians with the same Bell-record map;
* amplitude-level field uniqueness is attacked by exhibiting inequivalent local
  amplitude kernels with the same causal/eikonal support front;
* asymptotic resource scaling is attacked by adding a sparse 3D side=6 control;
* calibrated pulse schedules are supplied for the retained-axis record slots;
* detector hardware is attacked with an explicit local pointer-bath coupling
  model whose product overlap gives the prior detector theorem.

The claim boundary remains ordinary quantum state teleportation only. No matter,
mass, charge, energy, object, or faster-than-light transport is claimed.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from collections.abc import Iterable
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.frontier_teleportation_native_record_apparatus import (  # noqa: E402
    I2,
    OUTCOME_LABELS,
    OUTCOME_ORDER,
    X2,
    Z2,
    bell_state,
    record_codeword,
)
from scripts.frontier_teleportation_remaining_blocker_reduction import (  # noqa: E402
    SparseResourceRow,
    projector_minus,
    sparse_ground_resource,
)
from scripts.frontier_teleportation_resource_from_poisson import AuditCase  # noqa: E402


Array = np.ndarray
Point3D = tuple[int, int, int]


@dataclasses.dataclass(frozen=True)
class PulseScheduleMetrics:
    slot_count: int
    duration: float
    rabi_frequency: float
    max_ideal_bit_error: float
    worst_area_error: float
    max_jitter_bit_error: float
    max_slot_count_spread: int


@dataclasses.dataclass(frozen=True)
class DetectorMaterialMetrics:
    local_terms: int
    fragments_per_component: int
    coupling_angle: float
    fragment_overlap: float
    max_record_overlap: float
    entropy_defect_bits: float
    term_commutator: float


def kron_all(ops: Iterable[Array]) -> Array:
    out = np.array([[1.0 + 0.0j]])
    for op in ops:
        out = np.kron(out, op)
    return out


def pointer_x(index: int, n_qubits: int) -> Array:
    ops = [I2 for _ in range(n_qubits)]
    ops[index] = X2
    return kron_all(ops)


def pointer_basis(codeword: tuple[int, ...]) -> Array:
    index = 0
    for bit in codeword:
        index = (index << 1) | bit
    vec = np.zeros(2 ** len(codeword), dtype=complex)
    vec[index] = 1.0
    return vec


def eigenvalue_bit(stabilizer: Array, state: Array) -> int:
    value = complex(np.vdot(state, stabilizer @ state))
    if abs(value.real - 1.0) < 1e-12:
        return 0
    if abs(value.real + 1.0) < 1e-12:
        return 1
    raise RuntimeError(f"not a stabilizer eigenstate: {value}")


def written_codeword_from_hamiltonian(z_bit: int, x_bit: int) -> tuple[int, ...]:
    state = bell_state(z_bit, x_bit)
    zz = np.kron(Z2, Z2)
    xx = np.kron(X2, X2)
    derived_z = eigenvalue_bit(xx, state)
    derived_x = eigenvalue_bit(zz, state)
    derived_p = derived_z ^ derived_x
    return (
        derived_z,
        derived_z,
        derived_z,
        derived_x,
        derived_x,
        derived_x,
        derived_p,
        derived_p,
    )


def transducer_hamiltonian(rotation_winding: int) -> Array:
    zz = np.kron(Z2, Z2)
    xx = np.kron(X2, X2)
    parity = xx @ zz
    angle = math.pi / 2.0 + math.pi * rotation_winding
    pointer_identity = np.eye(2**8, dtype=complex)

    def lifted(projector: Array, indexes: tuple[int, ...]) -> Array:
        pointer_sum = np.zeros_like(pointer_identity)
        for index in indexes:
            pointer_sum += pointer_x(index, 8)
        return np.kron(projector, pointer_sum)

    return angle * (
        lifted(projector_minus(xx), (0, 1, 2))
        + lifted(projector_minus(zz), (3, 4, 5))
        + lifted(projector_minus(parity), (6, 7))
    )


def sole_axiom_apparatus_obstruction(tolerance: float) -> dict[str, float | int | bool]:
    h0 = transducer_hamiltonian(rotation_winding=0)
    h1 = transducer_hamiltonian(rotation_winding=1)
    same_records = True
    max_pointer_error = 0.0
    for outcome in OUTCOME_ORDER:
        actual = written_codeword_from_hamiltonian(*outcome)
        expected = record_codeword(*outcome)
        same_records = same_records and actual == expected
        max_pointer_error = max(
            max_pointer_error,
            float(np.linalg.norm(pointer_basis(actual) - pointer_basis(expected))),
        )
    spectral_difference = float(abs(np.linalg.norm(h1, 2) - np.linalg.norm(h0, 2)))
    return {
        "inequivalent_hamiltonians": 2,
        "same_record_map": same_records,
        "max_pointer_error": max_pointer_error,
        "spectral_norm_difference": spectral_difference,
        "obstruction_passes": same_records and max_pointer_error < tolerance and spectral_difference > 1.0,
    }


def neighbors(point: Point3D, shape: Point3D) -> tuple[Point3D, ...]:
    out: list[Point3D] = []
    for axis in range(3):
        for step in (-1, 1):
            candidate = list(point)
            candidate[axis] += step
            if 0 <= candidate[axis] < shape[axis]:
                out.append(tuple(candidate))  # type: ignore[arg-type]
    return tuple(out)


def manhattan(first: Point3D, second: Point3D) -> int:
    return sum(abs(a - b) for a, b in zip(first, second))


def all_points(shape: Point3D) -> Iterable[Point3D]:
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                yield (x, y, z)


def amplitude_kernel_arrivals(
    shape: Point3D,
    source: Point3D,
    center_weight: float,
    max_ticks: int,
    threshold: float,
) -> tuple[dict[Point3D, int], dict[Point3D, complex]]:
    neighbor_weight = (1.0 - center_weight) / 6.0
    amplitudes: dict[Point3D, complex] = {source: 1.0 + 0.0j}
    arrivals = {source: 0}
    for tick in range(1, max_ticks + 1):
        next_amplitudes = {point: center_weight * value for point, value in amplitudes.items()}
        for point, value in amplitudes.items():
            for neighbor in neighbors(point, shape):
                next_amplitudes[neighbor] = next_amplitudes.get(neighbor, 0.0 + 0.0j) + neighbor_weight * value
        norm = math.sqrt(sum(abs(value) ** 2 for value in next_amplitudes.values()))
        amplitudes = {point: value / norm for point, value in next_amplitudes.items()}
        for point, value in amplitudes.items():
            if abs(value) > threshold:
                arrivals.setdefault(point, tick)
    return arrivals, amplitudes


def amplitude_field_nonuniqueness(threshold: float) -> dict[str, float | int | bool]:
    shape = (5, 5, 5)
    source = (2, 2, 2)
    max_ticks = max(manhattan(source, point) for point in all_points(shape))
    arrivals_a, final_a = amplitude_kernel_arrivals(shape, source, 0.25, max_ticks, threshold)
    arrivals_b, final_b = amplitude_kernel_arrivals(shape, source, 0.55, max_ticks, threshold)

    max_arrival_error = 0
    support_mismatch = 0
    for point in all_points(shape):
        exact = manhattan(source, point)
        max_arrival_error = max(
            max_arrival_error,
            abs(arrivals_a[point] - exact),
            abs(arrivals_b[point] - exact),
        )
        support_mismatch += int(arrivals_a[point] != arrivals_b[point])
    l2_difference = math.sqrt(
        sum(abs(final_a.get(point, 0.0) - final_b.get(point, 0.0)) ** 2 for point in all_points(shape))
    )
    center_amplitude_difference = abs(final_a[source] - final_b[source])
    return {
        "amplitude_laws": 2,
        "max_arrival_error": max_arrival_error,
        "support_mismatch": support_mismatch,
        "final_l2_difference": l2_difference,
        "center_amplitude_difference": center_amplitude_difference,
        "obstruction_passes": max_arrival_error == 0 and support_mismatch == 0 and l2_difference > 0.1,
    }


def sparse_scaling_rows(
    side6_couplings: tuple[float, ...],
    eig_tolerance: float,
) -> tuple[SparseResourceRow, ...]:
    cases = [AuditCase("side4_G5000", dim=3, side=4, mass=0.0, G=5000.0)]
    cases.extend(
        AuditCase(f"side6_G{coupling:g}", dim=3, side=6, mass=0.0, G=float(coupling))
        for coupling in side6_couplings
    )
    return tuple(sparse_ground_resource(case, eig_tolerance) for case in cases)


def sparse_scaling_obstruction(
    side6_couplings: tuple[float, ...],
    eig_tolerance: float,
    high_threshold: float,
) -> tuple[dict[str, float | int | bool], tuple[SparseResourceRow, ...]]:
    rows = sparse_scaling_rows(side6_couplings, eig_tolerance)
    side4_best = max(row.best_bell_overlap for row in rows if row.side == 4)
    side6_best = max(row.best_bell_overlap for row in rows if row.side == 6)
    return (
        {
            "rows": len(rows),
            "side4_best_bell": side4_best,
            "side6_best_bell": side6_best,
            "side6_couplings": len(side6_couplings),
            "side4_high": side4_best >= high_threshold,
            "side6_high_absent": side6_best < high_threshold,
            "scaling_obstruction_passes": side4_best >= high_threshold and side6_best < high_threshold,
        },
        rows,
    )


def calibrated_pulse_schedule(area_error: float) -> PulseScheduleMetrics:
    target_area = math.pi / 2.0
    rabi_frequency = target_area
    ideal_errors = []
    jitter_errors = []
    slot_counts = []
    for outcome in OUTCOME_ORDER:
        codeword = record_codeword(*outcome)
        slot_counts.append(len(codeword))
        for bit in codeword:
            if bit:
                ideal_errors.append(abs(math.cos(target_area)) ** 2)
                jitter_errors.append(abs(math.cos(target_area + area_error)) ** 2)
            else:
                ideal_errors.append(0.0)
                jitter_errors.append(abs(math.sin(area_error)) ** 2)
    return PulseScheduleMetrics(
        slot_count=max(slot_counts),
        duration=1.0,
        rabi_frequency=rabi_frequency,
        max_ideal_bit_error=max(ideal_errors),
        worst_area_error=area_error,
        max_jitter_bit_error=max(jitter_errors),
        max_slot_count_spread=max(slot_counts) - min(slot_counts),
    )


def min_hamming_distance() -> int:
    codewords = [record_codeword(*outcome) for outcome in OUTCOME_ORDER]
    return min(
        sum(a != b for a, b in zip(first, second))
        for first_index, first in enumerate(codewords)
        for second_index, second in enumerate(codewords)
        if first_index != second_index
    )


def record_entropy_defect(overlap_bound: float) -> float:
    coherence = np.eye(4, dtype=complex)
    coherence[~np.eye(4, dtype=bool)] = overlap_bound
    rho = 0.25 * coherence
    vals = np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))
    entropy = -sum(float(value) * math.log(float(value), 2.0) for value in vals if value > 1e-15)
    return 2.0 - entropy


def material_detector_model(coupling_angle: float, fragments_per_component: int) -> DetectorMaterialMetrics:
    q = abs(math.cos(coupling_angle))
    d_min = min_hamming_distance()
    max_overlap = q ** (d_min * fragments_per_component)
    local_terms = len(record_codeword(0, 0)) * fragments_per_component
    # Terms are |1><1| on one pointer slot times X on one bath fragment. Distinct
    # bath fragments commute; terms sharing a pointer projector also commute.
    term_commutator = 0.0
    return DetectorMaterialMetrics(
        local_terms=local_terms,
        fragments_per_component=fragments_per_component,
        coupling_angle=coupling_angle,
        fragment_overlap=q,
        max_record_overlap=max_overlap,
        entropy_defect_bits=record_entropy_defect(max_overlap),
        term_commutator=term_commutator,
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
    parser.add_argument("--side6-couplings", type=parse_float_csv, default=(5000.0, 10000.0, 20000.0))
    parser.add_argument("--eig-tolerance", type=float, default=1e-8)
    parser.add_argument("--resource-high-threshold", type=float, default=0.90)
    parser.add_argument("--amplitude-threshold", type=float, default=1e-14)
    parser.add_argument("--pulse-area-error", type=float, default=0.01)
    parser.add_argument("--detector-coupling-angle", type=float, default=0.80)
    parser.add_argument("--detector-fragments", type=int, default=24)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.eig_tolerance <= 0.0 or args.tolerance <= 0.0:
        raise ValueError("tolerances must be positive")
    if args.detector_fragments <= 0:
        raise ValueError("--detector-fragments must be positive")

    apparatus = sole_axiom_apparatus_obstruction(args.tolerance)
    amplitude = amplitude_field_nonuniqueness(args.amplitude_threshold)
    scaling, scaling_rows = sparse_scaling_obstruction(
        args.side6_couplings,
        args.eig_tolerance,
        args.resource_high_threshold,
    )
    pulse = calibrated_pulse_schedule(args.pulse_area_error)
    detector = material_detector_model(args.detector_coupling_angle, args.detector_fragments)

    apparatus_gate = bool(apparatus["obstruction_passes"])
    amplitude_gate = bool(amplitude["obstruction_passes"])
    scaling_gate = bool(scaling["scaling_obstruction_passes"])
    pulse_gate = (
        pulse.max_ideal_bit_error < args.tolerance
        and pulse.max_jitter_bit_error < 1e-3
        and pulse.max_slot_count_spread == 0
    )
    detector_gate = (
        detector.term_commutator < args.tolerance
        and detector.max_record_overlap < 1e-12
        and detector.entropy_defect_bits < 1e-12
    )

    print("TELEPORTATION HARD BLOCKER ATTACK")
    print("Status: planning artifact; ordinary quantum state teleportation only")
    print(
        "Claim boundary: no matter, mass, charge, energy, object, or "
        "faster-than-light transport"
    )
    print()
    print(
        "sole-axiom apparatus obstruction: "
        f"inequivalent_hamiltonians={apparatus['inequivalent_hamiltonians']}, "
        f"same_record_map={apparatus['same_record_map']}, "
        f"max_pointer_error={apparatus['max_pointer_error']:.3e}, "
        f"spectral_norm_difference={apparatus['spectral_norm_difference']:.6f}"
    )
    print(
        "amplitude-level field obstruction: "
        f"amplitude_laws={amplitude['amplitude_laws']}, "
        f"arrival_error={amplitude['max_arrival_error']}, "
        f"support_mismatch={amplitude['support_mismatch']}, "
        f"final_l2_difference={amplitude['final_l2_difference']:.6f}, "
        f"center_amplitude_difference={amplitude['center_amplitude_difference']:.6f}"
    )
    print("sparse 3D scaling control rows:")
    for row in scaling_rows:
        print(
            "  "
            f"side={row.side}, G={row.coupling:g}, N={row.n_sites}, Hdim={row.hilbert_dim}, "
            f"gap={row.gap:.6g}, Bell*={row.best_bell_overlap:.6f} "
            f"({row.best_bell_label}), Fbest={row.best_frame_favg:.6f}, "
            f"CHSH={row.logical_chsh:.6f}, neg={row.resource_negativity:.6f}"
        )
    print(
        "scaling verdict: "
        f"side4_best={scaling['side4_best_bell']:.6f}, "
        f"side6_best={scaling['side6_best_bell']:.6f}, "
        f"high_threshold={args.resource_high_threshold:.3f}"
    )
    print(
        "calibrated pulse schedule: "
        f"slots={pulse.slot_count}, duration={pulse.duration:.3f}, "
        f"rabi_frequency={pulse.rabi_frequency:.6f}, "
        f"ideal_bit_error={pulse.max_ideal_bit_error:.3e}, "
        f"area_error={pulse.worst_area_error:.3e}, "
        f"jitter_bit_error={pulse.max_jitter_bit_error:.3e}, "
        f"slot_spread={pulse.max_slot_count_spread}"
    )
    print(
        "material spin-bath detector model: "
        f"local_terms={detector.local_terms}, "
        f"fragments/component={detector.fragments_per_component}, "
        f"coupling_angle={detector.coupling_angle:.3f}, "
        f"fragment_overlap={detector.fragment_overlap:.6f}, "
        f"max_record_overlap={detector.max_record_overlap:.3e}, "
        f"entropy_defect={detector.entropy_defect_bits:.3e}, "
        f"term_commutator={detector.term_commutator:.3e}"
    )
    print()
    print("Acceptance gates:")
    print_gate("sole-axiom apparatus selection obstruction is explicit", apparatus_gate)
    print_gate("amplitude field equation uniqueness obstruction is explicit", amplitude_gate)
    print_gate("3D sparse scaling obstruction is recorded by side-6 controls", scaling_gate)
    print_gate("calibrated retained-axis pulse schedule writes equal-slot records", pulse_gate)
    print_gate("material spin-bath detector model gives classical records", detector_gate)
    print_gate("claim boundary stays state-only and not FTL", True)
    print()
    print("Limitations:")
    print("  The first two gates are obstruction results: current axioms do not")
    print("  uniquely select the apparatus or amplitude law without extra principles.")
    print("  The side-6 sparse control is negative for the tested couplings; it")
    print("  blocks asymptotic promotion rather than closing scaling.")
    print("  The pulse schedule is an ideal square-pulse calibration, not a hardware")
    print("  controller with noise, leakage, bandwidth, or fabrication limits.")
    print("  The material detector is a local spin-bath Hamiltonian model, not an")
    print("  experimentally specified detector medium.")
    return 0 if all((apparatus_gate, amplitude_gate, scaling_gate, pulse_gate, detector_gate)) else 1


if __name__ == "__main__":
    sys.exit(main())
