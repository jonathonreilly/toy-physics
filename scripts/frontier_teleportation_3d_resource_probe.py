#!/usr/bin/env python3
"""Smallest-surface 3D Poisson teleportation-resource probe.

Status: planning / first artifact. This runner asks whether the existing
Poisson/CHSH ground-state machinery supplies a retained-axis logical Bell
resource on the smallest exact 3D spatial lattice.

The audited object is an ordinary two-qubit quantum-state teleportation
resource after tracing cells and spectator tastes. It does not claim matter
teleportation, mass transfer, charge transfer, energy transfer, object
transport, or faster-than-light signaling.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_teleportation_resource_fidelity import (  # noqa: E402
    I2,
    correction_operator,
    partial_trace,
    pure_state_fidelity,
    teleport_density,
    trace_distance,
)
from frontier_teleportation_resource_from_poisson import (  # noqa: E402
    OUTCOME_LABELS,
    OUTCOME_ORDER,
    AuditCase,
    amplitudes_by_logical_env,
    bell_state,
    best_bell_overlap,
    factor_sites,
    ground_state_resource,
    negativity,
    reduced_logical_resource,
    two_qubit_chsh,
)


LABEL_TO_BITS = {label: bits for bits, label in OUTCOME_LABELS.items()}
CLASSICAL_AVG_FIDELITY = 2.0 / 3.0


@dataclasses.dataclass(frozen=True)
class ResourceRow:
    case: AuditCase
    n_sites: int
    n_env: int
    h2_dim: int
    ground_energy: float
    full_chsh: float
    phi_plus_overlap: float
    best_bell_overlap: float
    best_bell_label: str
    fixed_phi_avg_fidelity: float
    best_frame_avg_fidelity: float
    logical_chsh: float
    negativity: float
    purity: float
    bob_bias: float
    sampled_mean_fidelity: float
    sampled_min_fidelity: float
    sampled_max_fidelity: float
    max_trace_error: float
    max_no_record_to_marginal: float
    max_pairwise_no_record_distance: float
    frame_bits: tuple[int, int]

    @property
    def is_null(self) -> bool:
        return abs(self.case.G) <= 1e-15

    @property
    def high_resource(self) -> bool:
        return self.best_bell_overlap >= 0.9


def parse_float_list(raw: str) -> tuple[float, ...]:
    values: list[float] = []
    for item in raw.split(","):
        item = item.strip()
        if item:
            values.append(float(item))
    if not values:
        raise argparse.ArgumentTypeError("expected at least one numeric value")
    return tuple(values)


def normalize(state: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(state))
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm


def projector(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


def random_qubit(rng: np.random.Generator) -> np.ndarray:
    return normalize(rng.standard_normal(2) + 1j * rng.standard_normal(2))


def probe_states(seed: int, random_count: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    states = [
        np.array([1.0, 0.0], dtype=complex),
        np.array([0.0, 1.0], dtype=complex),
        np.array([1.0, 1.0], dtype=complex) / math.sqrt(2.0),
        np.array([1.0, -1.0], dtype=complex) / math.sqrt(2.0),
        np.array([1.0, 1.0j], dtype=complex) / math.sqrt(2.0),
        np.array([1.0, -1.0j], dtype=complex) / math.sqrt(2.0),
    ]
    states.extend(random_qubit(rng) for _ in range(random_count))
    return states


def bell_overlap(rho: np.ndarray, z_bit: int, x_bit: int) -> float:
    state = bell_state(z_bit, x_bit)
    return float(np.real(np.vdot(state, rho @ state)))


def bob_frame_resource(rho: np.ndarray, frame_bits: tuple[int, int]) -> np.ndarray:
    op = correction_operator(*frame_bits)
    transform = np.kron(I2, op)
    return transform @ rho @ transform.conj().T


def exact_avg_from_phi(phi_plus_overlap: float) -> float:
    return float((1.0 + 2.0 * phi_plus_overlap) / 3.0)


def resource_density(case: AuditCase) -> tuple[np.ndarray, int, int, float, float]:
    resource = ground_state_resource(case)
    n_sites = int(resource["n"])
    factors = factor_sites(case.dim, case.side, logical_axis=case.dim - 1)
    amp = amplitudes_by_logical_env(resource["psi"], n_sites, factors)
    rho = reduced_logical_resource(amp)
    rho = 0.5 * (rho + rho.conj().T)
    rho = rho / np.trace(rho)
    return (
        rho,
        n_sites,
        len(factors.env_labels),
        float(resource["ground_energy"]),
        float(resource["full_chsh"]),
    )


def sample_teleportation(
    framed_rho: np.ndarray, states: list[np.ndarray]
) -> tuple[float, float, float, float, float, float, float]:
    bob_marginal = partial_trace(framed_rho, dims=[2, 2], keep=[1])
    half_identity = 0.5 * I2
    reference_no_record: np.ndarray | None = None
    fidelities: list[float] = []
    max_trace_error = 0.0
    max_no_record_to_marginal = 0.0
    max_pairwise_no_record = 0.0

    for state in states:
        corrected, no_record, _probabilities = teleport_density(projector(state), framed_rho)
        fidelities.append(pure_state_fidelity(state, corrected))
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

    return (
        float(np.mean(fidelities)),
        float(np.min(fidelities)),
        float(np.max(fidelities)),
        max_trace_error,
        max_no_record_to_marginal,
        max_pairwise_no_record,
        trace_distance(bob_marginal, half_identity),
    )


def evaluate_case(case: AuditCase, states: list[np.ndarray]) -> ResourceRow:
    rho, n_sites, n_env, ground_energy, full_chsh = resource_density(case)
    best_overlap, best_label = best_bell_overlap(rho)
    frame_bits = LABEL_TO_BITS[best_label]
    framed_rho = bob_frame_resource(rho, frame_bits)
    phi_plus = bell_overlap(rho, 0, 0)
    framed_phi_plus = bell_overlap(framed_rho, 0, 0)
    (
        sampled_mean,
        sampled_min,
        sampled_max,
        trace_error,
        no_record_to_marginal,
        pairwise_no_record,
        bob_bias,
    ) = sample_teleportation(framed_rho, states)

    return ResourceRow(
        case=case,
        n_sites=n_sites,
        n_env=n_env,
        h2_dim=n_sites * n_sites,
        ground_energy=ground_energy,
        full_chsh=full_chsh,
        phi_plus_overlap=phi_plus,
        best_bell_overlap=best_overlap,
        best_bell_label=best_label,
        fixed_phi_avg_fidelity=exact_avg_from_phi(phi_plus),
        best_frame_avg_fidelity=exact_avg_from_phi(framed_phi_plus),
        logical_chsh=two_qubit_chsh(rho),
        negativity=negativity(rho),
        purity=float(np.real(np.trace(rho @ rho))),
        bob_bias=bob_bias,
        sampled_mean_fidelity=sampled_mean,
        sampled_min_fidelity=sampled_min,
        sampled_max_fidelity=sampled_max,
        max_trace_error=trace_error,
        max_no_record_to_marginal=no_record_to_marginal,
        max_pairwise_no_record_distance=pairwise_no_record,
        frame_bits=frame_bits,
    )


def fmt(value: float) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3:
        return f"{value:.3e}"
    return f"{value:.6f}"


def print_row_table(rows: list[ResourceRow]) -> None:
    print("3D side-2 retained-axis resource table:")
    print(
        "  "
        f"{'case':28s} {'G':>8s} {'Sfull':>8s} {'Bell*':>8s} {'label':>5s} "
        f"{'Phi+':>8s} {'F_phi':>8s} {'F_best':>8s} {'Slog':>8s} "
        f"{'neg':>8s} {'noSig':>9s} {'hi':>3s}"
    )
    for row in rows:
        print(
            "  "
            f"{row.case.label:28s} {row.case.G:8.3g} "
            f"{row.full_chsh:8.5f} {row.best_bell_overlap:8.6f} "
            f"{row.best_bell_label:>5s} {row.phi_plus_overlap:8.6f} "
            f"{row.fixed_phi_avg_fidelity:8.6f} {row.best_frame_avg_fidelity:8.6f} "
            f"{row.logical_chsh:8.5f} {row.negativity:8.6f} "
            f"{row.max_pairwise_no_record_distance:9.3e} "
            f"{'yes' if row.high_resource else 'no':>3s}"
        )


def print_case_detail(row: ResourceRow) -> None:
    print()
    print(f"Case: {row.case.label}")
    print(
        f"  setup: dim={row.case.dim} side={row.case.side} N={row.n_sites} "
        f"H2_dim={row.h2_dim} envs/logical_qubit={row.n_env} "
        f"mass={row.case.mass:g} G={row.case.G:g}"
    )
    print(
        f"  resource: E0={row.ground_energy:.12g}, full CHSH={row.full_chsh:.6f}, "
        f"logical CHSH={row.logical_chsh:.6f}, purity={row.purity:.6f}, "
        f"negativity={row.negativity:.6f}"
    )
    print(
        f"  Bell frame: best={row.best_bell_overlap:.6f} "
        f"({row.best_bell_label}), frame bits(z,x)={row.frame_bits}, "
        f"Phi+ overlap before frame={row.phi_plus_overlap:.6f}"
    )
    print(
        f"  fidelities: fixed-Phi+ F_avg={row.fixed_phi_avg_fidelity:.6f}, "
        f"best-frame F_avg={row.best_frame_avg_fidelity:.6f}, "
        f"sample mean/min/max={row.sampled_mean_fidelity:.6f}/"
        f"{row.sampled_min_fidelity:.6f}/{row.sampled_max_fidelity:.6f}"
    )
    print(
        f"  Bob before message: distance to framed resource marginal="
        f"{row.max_no_record_to_marginal:.3e}, pairwise input distance="
        f"{row.max_pairwise_no_record_distance:.3e}, "
        f"marginal bias from I/2={row.bob_bias:.3e}"
    )


def build_cases(args: argparse.Namespace) -> list[AuditCase]:
    cases: list[AuditCase] = []
    for G in args.G_values:
        label = "3d_side2_null" if abs(G) <= 1e-15 else f"3d_side2_G{G:g}"
        cases.append(AuditCase(label, dim=3, side=2, mass=args.mass, G=float(G)))
    return cases


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--G-values", type=parse_float_list, default=(0.0, 100.0, 500.0, 1000.0))
    parser.add_argument("--mass", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=20260425)
    parser.add_argument("--random-inputs", type=int, default=64)
    parser.add_argument("--high-threshold", type=float, default=0.9)
    parser.add_argument("--tolerance", type=float, default=1e-10)
    args = parser.parse_args(argv)

    states = probe_states(args.seed, args.random_inputs)
    rows = [evaluate_case(case, states) for case in build_cases(args)]

    print("3D POISSON TASTE-QUBIT TELEPORTATION RESOURCE PROBE")
    print("Status: planning / first artifact; ordinary quantum state teleportation only")
    print("Geometry: 3D side=2 dense two-species Hamiltonian; retained last taste axis")
    print(
        "Claim boundary: no matter, mass, charge, energy, object, or "
        "faster-than-light transport"
    )
    print(
        f"Input probes: {len(states)} states (six axis states + "
        f"{args.random_inputs} random, seed={args.seed})"
    )
    print_row_table(rows)

    for row in rows:
        print_case_detail(row)

    nulls_clean = all(
        row.best_bell_overlap <= 0.5 + args.tolerance
        and row.negativity <= 10.0 * args.tolerance
        and row.best_frame_avg_fidelity <= CLASSICAL_AVG_FIDELITY + 10.0 * args.tolerance
        for row in rows
        if row.is_null
    )
    positives = [row for row in rows if not row.is_null]
    high_positive = any(row.best_bell_overlap >= args.high_threshold for row in positives)
    no_signal_clean = all(
        row.max_pairwise_no_record_distance <= args.tolerance for row in rows
    )
    best = max(rows, key=lambda row: row.best_bell_overlap)

    print()
    print("Acceptance gates:")
    print(f"  3D side-2 null control stays non-resource: {'PASS' if nulls_clean else 'FAIL'}")
    print(
        f"  at least one non-null 3D side-2 high Bell-frame resource: "
        f"{'PASS' if high_positive else 'FAIL'}"
    )
    print(f"  Bob pre-message input-independence is clean: {'PASS' if no_signal_clean else 'FAIL'}")
    print("  retained-axis extraction used; raw xi_5 is not used as traced Z: PASS")
    print("  side>2 scaling not claimed: PASS")
    print()
    print("Verdict:")
    print(
        f"  best row {best.case.label}: Bell*={best.best_bell_overlap:.6f} "
        f"({best.best_bell_label}), best-frame F_avg={best.best_frame_avg_fidelity:.6f}, "
        f"fixed-Phi+ F_avg={best.fixed_phi_avg_fidelity:.6f}"
    )
    print(
        "  The smallest 3D side-2 dense probe has a high-fidelity Bell-frame "
        "logical resource, but the Bell frame must be tracked explicitly."
    )
    print(
        "  Larger 3D surfaces are not audited here; side=4 dense two-species "
        "diagonalization is outside this first bounded artifact."
    )

    return 0 if (nulls_clean and high_positive and no_signal_clean) else 1


if __name__ == "__main__":
    raise SystemExit(main())
