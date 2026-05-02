#!/usr/bin/env python3
"""End-to-end Poisson-backed taste-qubit teleportation audit.

Status: planning / first artifact. This runner combines the existing bounded
pieces into one protocol-level check:

1. build a Poisson/CHSH two-species ground state;
2. trace cells and spectator tastes to obtain the encoded two-qubit resource;
3. run the Bell-measurement + Pauli-correction teleportation channel;
4. audit Bob's pre-record reduced state for input-independence;
5. send a concrete two-bit Bell record on the directed classical channel.

It remains an audit of ordinary quantum state teleportation only. It does not
claim matter teleportation, mass transfer, charge transfer, energy transfer, or
faster-than-light signaling. It also does not solve native preparation/readout:
the Poisson resource is still obtained by offline ground-state extraction.
"""

from __future__ import annotations

import argparse
import dataclasses
import sys
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_teleportation_causal_channel import (  # noqa: E402
    CausalBellRecordChannel,
    DirectedLatticeDAG,
)
from frontier_teleportation_resource_fidelity import (  # noqa: E402
    CLASSICAL_AVG_FIDELITY,
    I2,
    bell_projector,
    bell_state,
    correction_operator,
    density_checks,
    exact_average_fidelity,
    partial_trace,
    pure_state_fidelity,
    random_qubit,
    teleport_density,
    trace_distance,
)
from frontier_teleportation_resource_from_poisson import (  # noqa: E402
    DEFAULT_CASES,
    OUTCOME_LABELS,
    OUTCOME_ORDER,
    AuditCase,
    amplitudes_by_logical_env,
    best_bell_overlap,
    factor_sites,
    ground_state_resource,
    negativity,
    reduced_logical_resource,
    two_qubit_chsh,
)


@dataclasses.dataclass(frozen=True)
class EndToEndResult:
    label: str
    dim: int
    side: int
    mass: float
    G: float
    full_chsh: float
    best_bell_overlap: float
    best_bell_label: str
    phi_plus_overlap: float
    exact_avg_fidelity: float
    sampled_mean_fidelity: float
    sampled_min_fidelity: float
    sampled_max_fidelity: float
    min_branch_fidelity: float
    max_branch_fidelity: float
    min_branch_probability: float
    max_branch_probability: float
    max_trace_error: float
    max_no_record_to_marginal_distance: float
    max_pairwise_no_record_distance: float
    bob_marginal_bias: float
    outcomes_seen: tuple[str, ...]
    logical_chsh: float
    resource_negativity: float
    resource_min_eigenvalue: float
    causal_record_ok: bool
    early_delivery_blocked: bool
    delivered_once: bool
    delivered_record_label: str
    delivered_record_fidelity: float

    @property
    def non_null(self) -> bool:
        return abs(self.G) > 1e-15


def projector(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


def phi_plus_overlap(resource_rho: np.ndarray) -> float:
    phi = bell_state(0, 0)
    return float(np.real(np.vdot(phi, resource_rho @ phi)))


def extract_poisson_resource(case: AuditCase) -> tuple[np.ndarray, dict[str, object]]:
    resource = ground_state_resource(case)
    n_sites = int(resource["n"])
    factors = factor_sites(case.dim, case.side)
    amp = amplitudes_by_logical_env(resource["psi"], n_sites, factors)
    rho = reduced_logical_resource(amp)
    return rho, resource


def branch_bob_unnormalized(
    input_rho: np.ndarray, resource_rho: np.ndarray, z_bit: int, x_bit: int
) -> np.ndarray:
    joint = np.kron(input_rho, resource_rho)
    measurement = np.kron(bell_projector(z_bit, x_bit), I2)
    branch = measurement @ joint @ measurement
    return partial_trace(branch, dims=[2, 2, 2], keep=[2])


def probe_states(seed: int, random_trials: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    states = [
        np.array([1.0, 0.0], dtype=complex),
        np.array([0.0, 1.0], dtype=complex),
        np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0),
        np.array([1.0, -1.0], dtype=complex) / np.sqrt(2.0),
        np.array([1.0, 1.0j], dtype=complex) / np.sqrt(2.0),
        np.array([1.0, -1.0j], dtype=complex) / np.sqrt(2.0),
    ]
    states.extend(random_qubit(rng) for _ in range(random_trials))
    return states


def causal_record_demo(
    input_state: np.ndarray,
    resource_rho: np.ndarray,
    probability_floor: float,
) -> tuple[bool, bool, bool, str, float]:
    input_rho = projector(input_state)
    probabilities = {
        outcome: float(np.real(np.trace(branch_bob_unnormalized(input_rho, resource_rho, *outcome))))
        for outcome in OUTCOME_ORDER
    }
    outcome = max(probabilities, key=probabilities.__getitem__)
    if probabilities[outcome] <= probability_floor:
        return False, False, False, OUTCOME_LABELS[outcome], 0.0

    branch = branch_bob_unnormalized(input_rho, resource_rho, *outcome)
    branch_rho = branch / probabilities[outcome]

    dag = DirectedLatticeDAG(width=4, height=2)
    channel = CausalBellRecordChannel(dag)
    alice_node = (0, 0)
    bob_node = (3, 1)
    channel.advance_to(5)
    sent = channel.send(
        record_id="poisson-end-to-end-record",
        sender="Alice",
        receiver="Bob",
        z_bit=outcome[0],
        x_bit=outcome[1],
        source=alice_node,
        target=bob_node,
    )

    channel.advance_to(sent.deliver_at_tick - 1)
    early = channel.receive(receiver="Bob", at_node=bob_node)
    early_blocked = len(early) == 0 and channel.pending_count() == 1

    channel.advance_to(sent.deliver_at_tick)
    delivered = channel.receive(receiver="Bob", at_node=bob_node)
    duplicate = channel.receive(receiver="Bob", at_node=bob_node)
    delivered_once = len(delivered) == 1 and len(duplicate) == 0 and channel.pending_count() == 0

    record = delivered[0] if delivered else sent
    correction = correction_operator(record.z_bit, record.x_bit)
    corrected = correction @ branch_rho @ correction.conj().T
    fidelity = pure_state_fidelity(input_state, corrected)
    return early_blocked and delivered_once, early_blocked, delivered_once, record.label, fidelity


def evaluate_case(
    case: AuditCase,
    states: list[np.ndarray],
    seed: int,
    tolerance: float,
    probability_floor: float,
) -> EndToEndResult:
    resource_rho, resource = extract_poisson_resource(case)
    checks = density_checks(resource_rho, tolerance)
    if not checks.valid:
        raise ValueError(f"{case.label} extracted resource is not a valid density matrix")

    bob_marginal = partial_trace(resource_rho, dims=[2, 2], keep=[1])
    half_identity = 0.5 * I2
    reference_no_record: np.ndarray | None = None

    fidelities: list[float] = []
    branch_fidelities: list[float] = []
    branch_probabilities: list[float] = []
    outcomes_seen: set[str] = set()
    max_trace_error = 0.0
    max_no_record_to_marginal = 0.0
    max_pairwise_no_record = 0.0

    for input_state in states:
        input_rho = projector(input_state)
        corrected, no_record, probabilities = teleport_density(input_rho, resource_rho)
        fidelities.append(pure_state_fidelity(input_state, corrected))
        max_trace_error = max(max_trace_error, float(abs(np.trace(corrected) - 1.0)))
        max_no_record_to_marginal = max(
            max_no_record_to_marginal,
            trace_distance(no_record, bob_marginal),
        )
        if reference_no_record is None:
            reference_no_record = no_record
        else:
            max_pairwise_no_record = max(
                max_pairwise_no_record,
                trace_distance(no_record, reference_no_record),
            )

        for outcome, probability in probabilities.items():
            branch_probabilities.append(probability)
            if probability > probability_floor:
                outcomes_seen.add(OUTCOME_LABELS[outcome])
                branch = branch_bob_unnormalized(input_rho, resource_rho, *outcome)
                branch_rho = branch / probability
                correction = correction_operator(*outcome)
                corrected_branch = correction @ branch_rho @ correction.conj().T
                branch_fidelities.append(pure_state_fidelity(input_state, corrected_branch))

    reference_rng = np.random.default_rng(seed + 10_000)
    record_input = random_qubit(reference_rng)
    causal_ok, early_blocked, delivered_once, record_label, delivered_fidelity = causal_record_demo(
        record_input,
        resource_rho,
        probability_floor,
    )

    best_overlap, best_label = best_bell_overlap(resource_rho)
    return EndToEndResult(
        label=case.label,
        dim=case.dim,
        side=case.side,
        mass=case.mass,
        G=case.G,
        full_chsh=float(resource["full_chsh"]),
        best_bell_overlap=best_overlap,
        best_bell_label=best_label,
        phi_plus_overlap=phi_plus_overlap(resource_rho),
        exact_avg_fidelity=exact_average_fidelity(resource_rho),
        sampled_mean_fidelity=float(np.mean(fidelities)),
        sampled_min_fidelity=float(np.min(fidelities)),
        sampled_max_fidelity=float(np.max(fidelities)),
        min_branch_fidelity=float(np.min(branch_fidelities)) if branch_fidelities else 0.0,
        max_branch_fidelity=float(np.max(branch_fidelities)) if branch_fidelities else 0.0,
        min_branch_probability=float(np.min(branch_probabilities)),
        max_branch_probability=float(np.max(branch_probabilities)),
        max_trace_error=max_trace_error,
        max_no_record_to_marginal_distance=max_no_record_to_marginal,
        max_pairwise_no_record_distance=max_pairwise_no_record,
        bob_marginal_bias=trace_distance(bob_marginal, half_identity),
        outcomes_seen=tuple(sorted(outcomes_seen)),
        logical_chsh=two_qubit_chsh(resource_rho),
        resource_negativity=negativity(resource_rho),
        resource_min_eigenvalue=checks.min_eigenvalue,
        causal_record_ok=causal_ok,
        early_delivery_blocked=early_blocked,
        delivered_once=delivered_once,
        delivered_record_label=record_label,
        delivered_record_fidelity=delivered_fidelity,
    )


def passes_protocol(result: EndToEndResult, fidelity_threshold: float, tolerance: float) -> bool:
    return bool(
        result.best_bell_label == "Phi+"
        and result.best_bell_overlap >= fidelity_threshold
        and result.exact_avg_fidelity >= fidelity_threshold
        and result.sampled_min_fidelity >= fidelity_threshold
        and set(result.outcomes_seen) == {OUTCOME_LABELS[outcome] for outcome in OUTCOME_ORDER}
        and result.max_no_record_to_marginal_distance < tolerance
        and result.max_pairwise_no_record_distance < tolerance
        and result.max_trace_error < 10 * tolerance
        and result.causal_record_ok
        and result.delivered_record_fidelity >= fidelity_threshold
    )


def print_table(results: list[EndToEndResult], fidelity_threshold: float, tolerance: float) -> None:
    print("End-to-end case table:")
    print(
        "  "
        f"{'case':18s} {'Sfull':>8s} {'Bell*':>8s} {'label':>5s} "
        f"{'Favg':>8s} {'Fmin':>8s} {'Bmin':>8s} {'noSig':>9s} "
        f"{'record':>6s} {'pass':>5s}"
    )
    for result in results:
        ok = passes_protocol(result, fidelity_threshold, tolerance)
        print(
            "  "
            f"{result.label[:18]:18s} "
            f"{result.full_chsh:8.5f} "
            f"{result.best_bell_overlap:8.5f} "
            f"{result.best_bell_label:>5s} "
            f"{result.exact_avg_fidelity:8.5f} "
            f"{result.sampled_min_fidelity:8.5f} "
            f"{result.min_branch_fidelity:8.5f} "
            f"{result.max_pairwise_no_record_distance:9.3e} "
            f"{'yes' if result.causal_record_ok else 'no':>6s} "
            f"{'yes' if ok else '':>5s}"
        )


def print_details(results: list[EndToEndResult]) -> None:
    print()
    for result in results:
        print(f"Case: {result.label}")
        print(
            "  resource: "
            f"dim={result.dim} side={result.side} mass={result.mass:g} G={result.G:g}, "
            f"full CHSH={result.full_chsh:.6f}, logical CHSH={result.logical_chsh:.6f}, "
            f"negativity={result.resource_negativity:.6f}, "
            f"min eig={result.resource_min_eigenvalue:.3e}"
        )
        print(
            "  Bell overlaps/fidelity: "
            f"best={result.best_bell_overlap:.6f} ({result.best_bell_label}), "
            f"Phi+={result.phi_plus_overlap:.6f}, "
            f"exact F_avg={result.exact_avg_fidelity:.6f}, "
            f"sample mean/min/max={result.sampled_mean_fidelity:.6f}/"
            f"{result.sampled_min_fidelity:.6f}/{result.sampled_max_fidelity:.6f}"
        )
        print(
            "  Bell branches: "
            f"outcomes={', '.join(result.outcomes_seen)}, "
            f"probability min/max={result.min_branch_probability:.6e}/"
            f"{result.max_branch_probability:.6e}, "
            f"conditional corrected fidelity min/max={result.min_branch_fidelity:.6f}/"
            f"{result.max_branch_fidelity:.6f}"
        )
        print(
            "  Bob before record: "
            f"distance to resource marginal={result.max_no_record_to_marginal_distance:.3e}, "
            f"pairwise input distance={result.max_pairwise_no_record_distance:.3e}, "
            f"Bob marginal bias from I/2={result.bob_marginal_bias:.3e}"
        )
        print(
            "  causal record: "
            f"label={result.delivered_record_label}, early blocked={result.early_delivery_blocked}, "
            f"delivered once={result.delivered_once}, "
            f"delivered-branch fidelity={result.delivered_record_fidelity:.6f}"
        )


def print_acceptance(results: list[EndToEndResult], fidelity_threshold: float, tolerance: float) -> bool:
    nulls = [result for result in results if not result.non_null]
    non_null = [result for result in results if result.non_null]
    passing = [result for result in non_null if passes_protocol(result, fidelity_threshold, tolerance)]

    gates = {
        "null controls do not pass high-fidelity protocol": all(
            not passes_protocol(result, fidelity_threshold, tolerance) for result in nulls
        ),
        "at least one Poisson case passes end-to-end gates": bool(passing),
        "all passing cases keep Bob pre-record input-independence": all(
            result.max_pairwise_no_record_distance < tolerance
            and result.max_no_record_to_marginal_distance < tolerance
            for result in passing
        ),
        "all passing cases exercise four Bell outcomes": all(
            set(result.outcomes_seen) == {OUTCOME_LABELS[outcome] for outcome in OUTCOME_ORDER}
            for result in passing
        ),
        "all passing cases have causal record delivery": all(
            result.causal_record_ok for result in passing
        ),
    }

    print()
    print("Acceptance gates:")
    for name, ok in gates.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print()
    print("Claim boundary:")
    print("  This is Poisson-backed quantum state teleportation on a traced encoded resource.")
    print("  It is not a preparation/readout derivation and not matter, mass, charge,")
    print("  energy, or faster-than-light transport.")
    return all(gates.values())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=128, help="random input states per case")
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument("--fidelity-threshold", type=float, default=0.90)
    parser.add_argument("--tolerance", type=float, default=1e-10)
    parser.add_argument("--probability-floor", type=float, default=1e-12)
    parser.add_argument(
        "--case",
        choices=[case.label for case in DEFAULT_CASES],
        action="append",
        help="case label to run; omit for default cases",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.trials <= 0:
        raise ValueError("--trials must be positive")
    if not 0.0 < args.fidelity_threshold <= 1.0:
        raise ValueError("--fidelity-threshold must be in (0, 1]")
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")
    if args.probability_floor < 0.0:
        raise ValueError("--probability-floor must be nonnegative")

    requested = set(args.case or [])
    cases = [case for case in DEFAULT_CASES if not requested or case.label in requested]
    states = probe_states(args.seed, args.trials)

    print("POISSON-BACKED END-TO-END TASTE-QUBIT TELEPORTATION AUDIT")
    print("Status: planning / integration artifact; quantum state teleportation only")
    print(
        "Protocol: Poisson ground-state extraction -> traced logical resource -> "
        "Bell measurement -> causal two-bit record -> Bob correction"
    )
    print(f"Input probes: {len(states)} states (seed={args.seed})")
    print(f"High-fidelity threshold: {args.fidelity_threshold:.3f}")
    print()

    results = [
        evaluate_case(
            case=case,
            states=states,
            seed=args.seed + index,
            tolerance=args.tolerance,
            probability_floor=args.probability_floor,
        )
        for index, case in enumerate(cases)
    ]
    print_table(results, args.fidelity_threshold, args.tolerance)
    print_details(results)
    ok = print_acceptance(results, args.fidelity_threshold, args.tolerance)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
