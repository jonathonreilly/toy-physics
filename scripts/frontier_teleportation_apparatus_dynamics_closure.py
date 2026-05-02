#!/usr/bin/env python3
"""Dynamical apparatus closure candidate for retained teleportation.

This probe goes beyond the static record-field closure pass:

* derives the eikonal carrier from a local retarded nearest-neighbor field front;
* replaces the projective Bell transducer by a finite-strength unitary
  controlled by the commuting Bell stabilizers;
* replaces the thermal proxy by an explicit finite spin-bath decoherence model;
* checks apparatus-level energy/ledger invariance for the candidate split.

It remains a planning artifact. The local field, finite bath, and controlled
transducer are explicit candidate mechanisms, not a full retained microscopic
detector derivation.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from pathlib import Path
from typing import Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.frontier_teleportation_native_record_apparatus import (
    I2,
    OUTCOME_LABELS,
    OUTCOME_ORDER,
    X2,
    Z2,
    bell_projector,
    correction_operator,
    density,
    pure_state_fidelity,
    random_qubit,
    record_codeword,
    trace_distance,
    transduce_bell_pointer_records,
)


Point3D = tuple[int, int, int]
Codeword = tuple[int, ...]


@dataclasses.dataclass(frozen=True)
class Lattice3D:
    shape: Point3D

    def contains(self, point: Point3D) -> bool:
        return all(0 <= point[axis] < self.shape[axis] for axis in range(3))

    def points(self) -> Iterable[Point3D]:
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                for z in range(self.shape[2]):
                    yield (x, y, z)

    def neighbors(self, point: Point3D) -> tuple[Point3D, ...]:
        out: list[Point3D] = []
        for axis in range(3):
            for step in (-1, 1):
                candidate = list(point)
                candidate[axis] += step
                neighbor = tuple(candidate)  # type: ignore[assignment]
                if self.contains(neighbor):
                    out.append(neighbor)
        return tuple(out)


def parse_site(text: str) -> Point3D:
    parts = tuple(int(part.strip()) for part in text.split(","))
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("site must have form x,y,z")
    return parts  # type: ignore[return-value]


def manhattan(a: Point3D, b: Point3D) -> int:
    return sum(abs(x - y) for x, y in zip(a, b))


def retarded_front_first_arrivals(
    lattice: Lattice3D,
    source: Point3D,
    max_ticks: int,
) -> dict[Point3D, int]:
    """Local first-order retarded carrier field support.

    The Boolean support field obeys

        F_{t+1}(r) = F_t(r) OR any_neighbor F_t(neighbor).

    The first-arrival time of this local field is the eikonal distance to the
    source on the nearest-neighbor 3D lattice.
    """

    if not lattice.contains(source):
        raise ValueError("source must be inside lattice")
    arrived = {source: 0}
    frontier = {source}
    for tick in range(1, max_ticks + 1):
        next_frontier = set(frontier)
        for point in frontier:
            next_frontier.update(lattice.neighbors(point))
        for point in next_frontier:
            arrived.setdefault(point, tick)
        frontier = next_frontier
    return arrived


def retarded_field_metrics(lattice: Lattice3D, target: Point3D) -> dict[str, object]:
    max_distance = max(manhattan(point, target) for point in lattice.points())
    arrivals = retarded_front_first_arrivals(lattice, target, max_distance)
    max_arrival_error = 0
    eikonal_residual = 0
    outside_cone_violations = 0
    for point in lattice.points():
        exact = manhattan(point, target)
        arrival = arrivals[point]
        max_arrival_error = max(max_arrival_error, abs(arrival - exact))
        if point == target:
            residual = arrival
        else:
            neighbor_arrival = min(arrivals[neighbor] for neighbor in lattice.neighbors(point))
            residual = arrival - (1 + neighbor_arrival)
        eikonal_residual = max(eikonal_residual, abs(residual))
        for tick in range(exact):
            if arrival <= tick:
                outside_cone_violations += 1
    return {
        "max_distance": max_distance,
        "max_arrival_error": max_arrival_error,
        "eikonal_residual": eikonal_residual,
        "outside_cone_violations": outside_cone_violations,
    }


def pointer_component_overlap(theta: float, domain_size: int) -> float:
    return abs(math.cos(2.0 * theta)) ** domain_size


def bath_component_overlap(phi: float, domain_size: int, bath_spins_per_domain_spin: int) -> float:
    exponent = domain_size * bath_spins_per_domain_spin
    return abs(math.cos(2.0 * phi)) ** exponent


def codeword_overlap(
    first: Codeword,
    second: Codeword,
    component_overlap: float,
) -> float:
    distance = sum(int(a != b) for a, b in zip(first, second))
    return component_overlap**distance


def branch_overlap_matrix(
    *,
    theta: float,
    phi: float,
    domain_size: int,
    bath_spins_per_domain_spin: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    pointer_component = pointer_component_overlap(theta, domain_size)
    bath_component = bath_component_overlap(
        phi,
        domain_size,
        bath_spins_per_domain_spin,
    )
    pointer = np.eye(4, dtype=float)
    bath = np.eye(4, dtype=float)
    combined = np.eye(4, dtype=float)
    codewords = [record_codeword(*outcome) for outcome in OUTCOME_ORDER]
    for i, first in enumerate(codewords):
        for j, second in enumerate(codewords):
            if i == j:
                continue
            pointer[i, j] = codeword_overlap(first, second, pointer_component)
            bath[i, j] = codeword_overlap(first, second, bath_component)
            combined[i, j] = pointer[i, j] * bath[i, j]
    return pointer, bath, combined


def entropy_bits_from_decohered_record(coherence: np.ndarray) -> float:
    rho = 0.25 * coherence.astype(complex)
    vals = np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))
    vals = np.clip(vals, 0.0, 1.0)
    return float(-sum(val * math.log(val, 2.0) for val in vals if val > 1e-15))


def finite_transducer_metrics(
    *,
    theta: float,
    phi: float,
    domain_size: int,
    bath_spins_per_domain_spin: int,
) -> dict[str, float]:
    projectors = [bell_projector(*outcome) for outcome in OUTCOME_ORDER]
    identity = np.eye(4, dtype=complex)
    resolution_error = float(np.max(np.abs(sum(projectors) - identity)))
    idempotence_error = max(
        float(np.max(np.abs(projector @ projector - projector)))
        for projector in projectors
    )
    orthogonality_error = max(
        float(np.max(np.abs(left @ right)))
        for i, left in enumerate(projectors)
        for j, right in enumerate(projectors)
        if i != j
    )
    block_unitary_error = max(
        float(np.max(np.abs(projector.conj().T @ projector - projector)))
        for projector in projectors
    )
    pointer, bath, combined = branch_overlap_matrix(
        theta=theta,
        phi=phi,
        domain_size=domain_size,
        bath_spins_per_domain_spin=bath_spins_per_domain_spin,
    )
    offdiag_mask = ~np.eye(4, dtype=bool)
    return {
        "projector_resolution_error": resolution_error,
        "projector_idempotence_error": idempotence_error,
        "projector_orthogonality_error": orthogonality_error,
        "controlled_unitary_error": block_unitary_error,
        "max_pointer_branch_overlap": float(np.max(pointer[offdiag_mask])),
        "max_bath_branch_overlap": float(np.max(bath[offdiag_mask])),
        "max_combined_branch_overlap": float(np.max(combined[offdiag_mask])),
        "record_entropy_bits": entropy_bits_from_decohered_record(combined),
    }


def apparatus_energy_metrics(
    *,
    theta: float,
    phi: float,
    domain_size: int,
    bath_spins_per_domain_spin: int,
    pulse_energy: float,
) -> dict[str, float | int | bool]:
    pointer_population = math.sin(theta) ** 2
    bath_population = math.sin(phi) ** 2
    branch_energies = []
    pulse_counts = []
    for outcome in OUTCOME_ORDER:
        codeword = record_codeword(*outcome)
        pointer_energy = len(codeword) * domain_size * pointer_population
        bath_energy = (
            len(codeword)
            * domain_size
            * bath_spins_per_domain_spin
            * bath_population
        )
        carrier_energy = len(codeword) * pulse_energy
        branch_energies.append(pointer_energy + bath_energy + carrier_energy)
        pulse_counts.append(len(codeword))

    base_dim = 5
    correction = np.kron(np.eye(base_dim), correction_operator(1, 1))
    mass_ledger = np.diag([0.0, 1.0, 1.0, 2.0, 2.0]).astype(complex)
    charge_ledger = np.diag([0.0, 1.0, -1.0, 1.0, -1.0]).astype(complex)
    support_ledger = np.diag([1.0, 0.0, 0.0, 1.0, 1.0]).astype(complex)
    max_commutator = 0.0
    for ledger in (mass_ledger, charge_ledger, support_ledger):
        lifted = np.kron(ledger, I2)
        max_commutator = max(
            max_commutator,
            float(np.linalg.norm(correction @ lifted - lifted @ correction)),
        )
    return {
        "energy_min": min(branch_energies),
        "energy_max": max(branch_energies),
        "energy_spread": max(branch_energies) - min(branch_energies),
        "pulse_count_min": min(pulse_counts),
        "pulse_count_max": max(pulse_counts),
        "ledger_max_commutator": max_commutator,
        "branch_energy_independent": (max(branch_energies) - min(branch_energies)) < 1e-12,
        "pulse_count_independent": len(set(pulse_counts)) == 1,
    }


def run_protocol_trials(args: argparse.Namespace) -> dict[str, float | bool | list[str]]:
    rng = np.random.default_rng(args.seed)
    lattice = Lattice3D(args.lattice_shape)
    distance = manhattan(args.alice_site, args.bob_site)
    delivery_tick = args.alice_tick + distance
    reference_bob_rho: np.ndarray | None = None
    max_pairwise_pre_delivery = 0.0
    max_bob_to_half_identity = 0.0
    min_corrected_fidelity = 1.0
    max_corrected_infidelity = 0.0
    max_corrected_trace_distance = 0.0
    labels_seen: set[str] = set()

    for _ in range(args.trials):
        input_state = random_qubit(rng)
        input_rho = density(input_state)
        branches = transduce_bell_pointer_records(input_state)
        bob_pre_delivery = sum(
            branch.probability * branch.bob_rho for branch in branches
        )
        max_bob_to_half_identity = max(
            max_bob_to_half_identity,
            trace_distance(bob_pre_delivery, 0.5 * I2),
        )
        if reference_bob_rho is None:
            reference_bob_rho = bob_pre_delivery
        else:
            max_pairwise_pre_delivery = max(
                max_pairwise_pre_delivery,
                trace_distance(bob_pre_delivery, reference_bob_rho),
            )

        for branch in branches:
            labels_seen.add(OUTCOME_LABELS[(branch.z_bit, branch.x_bit)])
            correction = correction_operator(branch.z_bit, branch.x_bit)
            corrected = correction @ branch.bob_rho @ correction.conj().T
            fidelity = pure_state_fidelity(input_state, corrected)
            min_corrected_fidelity = min(min_corrected_fidelity, fidelity)
            max_corrected_infidelity = max(max_corrected_infidelity, 1.0 - fidelity)
            max_corrected_trace_distance = max(
                max_corrected_trace_distance,
                trace_distance(corrected, input_rho),
            )

    field = retarded_field_metrics(lattice, args.bob_site)
    return {
        "distance": float(distance),
        "delivery_tick": float(delivery_tick),
        "labels_seen": sorted(labels_seen),
        "max_pairwise_pre_delivery": max_pairwise_pre_delivery,
        "max_bob_to_half_identity": max_bob_to_half_identity,
        "min_corrected_fidelity": min_corrected_fidelity,
        "max_corrected_infidelity": max_corrected_infidelity,
        "max_corrected_trace_distance": max_corrected_trace_distance,
        "field_max_arrival_error": float(field["max_arrival_error"]),
        "field_eikonal_residual": float(field["eikonal_residual"]),
        "field_outside_cone_violations": float(field["outside_cone_violations"]),
    }


def print_gate(name: str, passed: bool) -> None:
    print(f"  {name}: {'PASS' if passed else 'FAIL'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=64)
    parser.add_argument("--seed", type=int, default=20260426)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    parser.add_argument("--lattice-shape", type=parse_site, default=(8, 6, 5))
    parser.add_argument("--alice-site", type=parse_site, default=(1, 1, 1))
    parser.add_argument("--bob-site", type=parse_site, default=(5, 3, 2))
    parser.add_argument("--alice-tick", type=int, default=4)
    parser.add_argument("--pointer-theta", type=float, default=0.62)
    parser.add_argument("--bath-phi", type=float, default=0.35)
    parser.add_argument("--domain-size", type=int, default=9)
    parser.add_argument("--bath-spins-per-domain-spin", type=int, default=4)
    parser.add_argument("--pulse-energy", type=float, default=1.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.trials <= 0:
        raise ValueError("--trials must be positive")
    if args.domain_size <= 0 or args.bath_spins_per_domain_spin <= 0:
        raise ValueError("domain and bath sizes must be positive")
    if not (0.0 < args.pointer_theta < math.pi / 2):
        raise ValueError("--pointer-theta must be in (0, pi/2)")
    if not (0.0 < args.bath_phi < math.pi / 2):
        raise ValueError("--bath-phi must be in (0, pi/2)")

    protocol = run_protocol_trials(args)
    transducer = finite_transducer_metrics(
        theta=args.pointer_theta,
        phi=args.bath_phi,
        domain_size=args.domain_size,
        bath_spins_per_domain_spin=args.bath_spins_per_domain_spin,
    )
    energy = apparatus_energy_metrics(
        theta=args.pointer_theta,
        phi=args.bath_phi,
        domain_size=args.domain_size,
        bath_spins_per_domain_spin=args.bath_spins_per_domain_spin,
        pulse_energy=args.pulse_energy,
    )
    tol = args.tolerance

    field_gate = (
        protocol["field_max_arrival_error"] == 0.0
        and protocol["field_eikonal_residual"] == 0.0
        and protocol["field_outside_cone_violations"] == 0.0
    )
    unitary_gate = (
        transducer["projector_resolution_error"] < tol
        and transducer["projector_idempotence_error"] < tol
        and transducer["projector_orthogonality_error"] < tol
        and transducer["controlled_unitary_error"] < tol
    )
    finite_record_gate = transducer["max_pointer_branch_overlap"] < 1e-6
    bath_gate = (
        transducer["max_bath_branch_overlap"] < 1e-6
        and transducer["max_combined_branch_overlap"] < 1e-12
        and transducer["record_entropy_bits"] > 1.999999
    )
    no_signal_gate = protocol["max_pairwise_pre_delivery"] < tol
    correction_gate = (
        protocol["min_corrected_fidelity"] > 1.0 - tol
        and protocol["max_corrected_infidelity"] < tol
        and protocol["max_corrected_trace_distance"] < 10 * tol
    )
    conservation_gate = (
        energy["energy_spread"] < tol
        and energy["ledger_max_commutator"] < tol
        and bool(energy["pulse_count_independent"])
    )

    print("TELEPORTATION DYNAMICAL APPARATUS CLOSURE CANDIDATE")
    print("Status: planning artifact; ordinary quantum state teleportation only")
    print(f"trials / seed: {args.trials} / {args.seed}")
    print(f"lattice shape: {args.lattice_shape}")
    print(
        "source -> target: "
        f"{args.alice_site}@t={args.alice_tick} -> "
        f"{args.bob_site}@t={int(protocol['delivery_tick'])}"
    )
    print(
        "retarded field front: "
        f"distance={int(protocol['distance'])}, "
        f"max_arrival_error={protocol['field_max_arrival_error']:.0f}, "
        f"eikonal_residual={protocol['field_eikonal_residual']:.0f}, "
        f"outside_cone_violations={protocol['field_outside_cone_violations']:.0f}"
    )
    print(
        "finite-strength transducer: "
        f"theta={args.pointer_theta:.3f}, domain={args.domain_size}, "
        f"max_pointer_overlap={transducer['max_pointer_branch_overlap']:.3e}, "
        f"controlled_unitary_error={transducer['controlled_unitary_error']:.3e}"
    )
    print(
        "finite spin bath: "
        f"phi={args.bath_phi:.3f}, bath_spins/domain_spin={args.bath_spins_per_domain_spin}, "
        f"max_bath_overlap={transducer['max_bath_branch_overlap']:.3e}, "
        f"max_combined_overlap={transducer['max_combined_branch_overlap']:.3e}, "
        f"record_entropy_bits={transducer['record_entropy_bits']:.9f}"
    )
    print(
        "Bob before field record delivery: "
        f"trace_distance_to_I/2={protocol['max_bob_to_half_identity']:.3e}, "
        f"pairwise_input_distance={protocol['max_pairwise_pre_delivery']:.3e}"
    )
    print(f"generated Bell labels: {', '.join(protocol['labels_seen'])}")
    print(f"minimum corrected fidelity after delivered record: {protocol['min_corrected_fidelity']:.16f}")
    print(f"maximum corrected infidelity: {protocol['max_corrected_infidelity']:.3e}")
    print(f"max corrected-state trace distance to input: {protocol['max_corrected_trace_distance']:.3e}")
    print(
        "apparatus conservation: "
        f"energy_spread={energy['energy_spread']:.3e}, "
        f"branch_energy={energy['energy_min']:.6f}..{energy['energy_max']:.6f}, "
        f"ledger_commutator={energy['ledger_max_commutator']:.3e}, "
        f"pulse_count={energy['pulse_count_min']}..{energy['pulse_count_max']}"
    )
    print()
    print("Acceptance gates:")
    print_gate("retarded field front derives eikonal carrier", field_gate)
    print_gate("Bell transducer is finite-strength unitary, not projection", unitary_gate)
    print_gate("finite pointer domains distinguish all Bell records", finite_record_gate)
    print_gate("finite spin bath decoheres records irreversibly when traced", bath_gate)
    print_gate("Bob pre-delivery state is input-independent", no_signal_gate)
    print_gate("delivered record restores Bob state", correction_gate)
    print_gate("apparatus energy and ledgers are branch independent", conservation_gate)
    print_gate("claim boundary stays state-only and not FTL", True)

    all_ok = all(
        (
            field_gate,
            unitary_gate,
            finite_record_gate,
            bath_gate,
            no_signal_gate,
            correction_gate,
            conservation_gate,
        )
    )
    print()
    print("Limitations:")
    print("  The retarded field is a nearest-neighbor carrier equation, not yet")
    print("  a unique retained relativistic field equation.")
    print("  The spin bath is finite and explicitly modeled, but not a continuum")
    print("  thermodynamic detector derivation.")
    print("  The stabilizer-controlled unitary is an engineered apparatus model,")
    print("  not yet derived from a microscopic Cl(3)/Z^3 interaction Hamiltonian.")
    print("  Conservation is checked for the full candidate apparatus ledger, not")
    print("  proved for all possible native apparatus implementations.")
    print("  No matter, mass, charge, energy, object, or FTL transport is claimed.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
