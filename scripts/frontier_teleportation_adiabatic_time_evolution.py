#!/usr/bin/env python3
"""Finite-time adiabatic evolution for the Poisson teleportation resource.

Status: planning / first artifact. This is a bounded closed-system diagnostic
for ordinary quantum state teleportation resources only. It does not claim
matter transfer, mass transfer, charge transfer, energy transfer, object
transport, or faster-than-light signaling.

The runner takes the native Poisson coupling path from the adiabatic prep
probe,

    H(s) = H(G=0) + s(t) * (H(G_target) - H(G=0)),

starts in the G=0 ground state, and performs finite-time Schrodinger evolution
under one or more schedules. The final state is traced to the logical
taste-qubit sector and audited as a two-qubit teleportation resource.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from collections.abc import Callable
from pathlib import Path

import numpy as np
from scipy.linalg import eigh, norm
from scipy.sparse.linalg import expm_multiply


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_teleportation_adiabatic_prep_probe import (  # noqa: E402
    AuditCase,
    build_endpoint_hamiltonians,
)
from frontier_teleportation_resource_fidelity import (  # noqa: E402
    CLASSICAL_AVG_FIDELITY,
    I2,
    exact_average_fidelity,
    partial_trace,
    probe_states,
    projector,
    pure_state_fidelity,
    teleport_density,
    trace_distance,
)
from frontier_teleportation_resource_from_poisson import (  # noqa: E402
    amplitudes_by_logical_env,
    bell_state,
    best_bell_overlap,
    factor_sites,
    negativity,
    reduced_logical_resource,
    two_qubit_chsh,
)


BASE_CASES = (
    AuditCase("2d_null", dim=2, side=4, mass=0.0, G=0.0),
    AuditCase("2d_poisson_chsh", dim=2, side=4, mass=0.0, G=1000.0),
)
OPTIONAL_1D_CASES = (
    AuditCase("1d_null", dim=1, side=8, mass=0.0, G=0.0),
    AuditCase("1d_poisson_chsh", dim=1, side=8, mass=0.0, G=1000.0),
)
ALL_CASES = BASE_CASES + OPTIONAL_1D_CASES


@dataclasses.dataclass(frozen=True)
class Schedule:
    name: str
    description: str
    fn: Callable[[float], float]


@dataclasses.dataclass(frozen=True)
class ResourceMetrics:
    phi_plus_overlap: float
    best_bell_overlap: float
    best_bell_label: str
    exact_avg_fidelity: float
    best_frame_avg_fidelity: float
    logical_chsh: float
    negativity: float
    purity: float


@dataclasses.dataclass(frozen=True)
class CaseData:
    case: AuditCase
    n_sites: int
    n_env: int
    h_initial: np.ndarray
    h_target: np.ndarray
    d_hamiltonian: np.ndarray
    d_hamiltonian_norm: float
    initial_energy: float
    initial_gap: float
    initial_ground_degeneracy: int
    initial_state: np.ndarray
    initial_state_mode: str
    target_energy: float
    target_gap: float
    target_ground: np.ndarray
    target_metrics: ResourceMetrics


@dataclasses.dataclass(frozen=True)
class EvolutionResult:
    case: AuditCase
    schedule: str
    runtime: float
    steps: int
    dt: float
    method: str
    final_norm_error: float
    final_ground_overlap: float
    diabatic_loss: float
    final_energy_excess: float
    metrics: ResourceMetrics
    resource_rho: np.ndarray = dataclasses.field(repr=False, compare=False)

    @property
    def is_null(self) -> bool:
        return abs(self.case.G) <= 1e-15


@dataclasses.dataclass(frozen=True)
class NoSignalAudit:
    sampled_mean_fidelity: float
    sampled_min_fidelity: float
    sampled_max_fidelity: float
    max_trace_error: float
    max_no_record_to_marginal_distance: float
    max_pairwise_no_record_distance: float
    bob_marginal_bias: float


def schedule_linear(u: float) -> float:
    return u


def schedule_smoothstep(u: float) -> float:
    return u * u * (3.0 - 2.0 * u)


def schedule_sine(u: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * u)


SCHEDULES = {
    "linear": Schedule("linear", "s(t)=t/T", schedule_linear),
    "smoothstep": Schedule(
        "smoothstep",
        "s(u)=3u^2-2u^3 with zero endpoint velocity",
        schedule_smoothstep,
    ),
    "sine": Schedule(
        "sine",
        "s(u)=(1-cos(pi*u))/2 with zero endpoint velocity",
        schedule_sine,
    ),
}


def fmt_float(value: float) -> str:
    if math.isinf(value):
        return "inf"
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e4:
        return f"{value:.6e}"
    return f"{value:.6f}"


def phi_plus_overlap(rho: np.ndarray) -> float:
    phi_plus = bell_state(0, 0)
    return float(np.real(np.vdot(phi_plus, rho @ phi_plus)))


def best_frame_avg_fidelity(best_overlap: float) -> float:
    return float((1.0 + 2.0 * best_overlap) / 3.0)


def resource_metrics(rho: np.ndarray) -> ResourceMetrics:
    best_overlap, best_label = best_bell_overlap(rho)
    return ResourceMetrics(
        phi_plus_overlap=phi_plus_overlap(rho),
        best_bell_overlap=best_overlap,
        best_bell_label=best_label,
        exact_avg_fidelity=exact_average_fidelity(rho),
        best_frame_avg_fidelity=best_frame_avg_fidelity(best_overlap),
        logical_chsh=two_qubit_chsh(rho),
        negativity=negativity(rho),
        purity=float(np.real(np.trace(rho @ rho))),
    )


def logical_resource_from_state(
    psi: np.ndarray, n_sites: int, case: AuditCase
) -> np.ndarray:
    factors = factor_sites(case.dim, case.side)
    amp = amplitudes_by_logical_env(psi, n_sites, factors)
    return reduced_logical_resource(amp)


def spectral_gap(evals: np.ndarray, degeneracy: int) -> float:
    if degeneracy >= len(evals):
        return math.inf
    return float(evals[degeneracy] - evals[0])


def initial_state_from_ground_space(
    initial_evals: np.ndarray,
    initial_evecs: np.ndarray,
    target_ground: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, int, str]:
    degeneracy = int(np.sum(initial_evals <= initial_evals[0] + tolerance))
    if degeneracy <= 1:
        return initial_evecs[:, 0], degeneracy, "unique G=0 ground state"

    ground_space = initial_evecs[:, :degeneracy]
    projected = ground_space @ (ground_space.conj().T @ target_ground)
    projected_norm = float(np.linalg.norm(projected))
    if projected_norm > tolerance:
        return (
            projected / projected_norm,
            degeneracy,
            "target-compatible vector in degenerate G=0 ground space",
        )
    return (
        initial_evecs[:, 0],
        degeneracy,
        "first vector in degenerate G=0 ground space",
    )


def build_case_data(case: AuditCase, degeneracy_tolerance: float) -> CaseData:
    n_sites, h_initial, h_target = build_endpoint_hamiltonians(case)
    d_hamiltonian = h_target - h_initial

    initial_evals, initial_evecs = eigh(h_initial)
    target_evals, target_evecs = eigh(h_target)
    target_ground = target_evecs[:, 0]
    initial_state, initial_degeneracy, initial_mode = initial_state_from_ground_space(
        initial_evals,
        initial_evecs,
        target_ground,
        degeneracy_tolerance,
    )

    target_rho = logical_resource_from_state(target_ground, n_sites, case)

    return CaseData(
        case=case,
        n_sites=n_sites,
        n_env=len(factor_sites(case.dim, case.side).env_labels),
        h_initial=h_initial,
        h_target=h_target,
        d_hamiltonian=d_hamiltonian,
        d_hamiltonian_norm=float(norm(d_hamiltonian, 2)),
        initial_energy=float(initial_evals[0]),
        initial_gap=spectral_gap(initial_evals, initial_degeneracy),
        initial_ground_degeneracy=initial_degeneracy,
        initial_state=initial_state,
        initial_state_mode=initial_mode,
        target_energy=float(target_evals[0]),
        target_gap=float(target_evals[1] - target_evals[0]),
        target_ground=target_ground,
        target_metrics=resource_metrics(target_rho),
    )


def chosen_method(method: str, dimension: int) -> str:
    if method == "auto":
        return "eigh" if dimension <= 128 else "expm_multiply"
    return method


def apply_step(
    hamiltonian: np.ndarray, psi: np.ndarray, dt: float, method: str
) -> np.ndarray:
    if method == "eigh":
        evals, evecs = eigh(hamiltonian)
        coeff = evecs.conj().T @ psi
        return evecs @ (np.exp(-1j * evals * dt) * coeff)
    if method == "expm_multiply":
        return expm_multiply((-1j * dt) * hamiltonian, psi)
    raise ValueError(f"unsupported propagation method: {method}")


def evolve_case(
    data: CaseData,
    schedule: Schedule,
    runtime: float,
    steps_per_unit: float,
    min_steps: int,
    method: str,
) -> EvolutionResult:
    step_method = chosen_method(method, data.h_initial.shape[0])
    steps = max(min_steps, int(math.ceil(runtime * steps_per_unit)))
    dt = runtime / steps

    if data.d_hamiltonian_norm <= 1e-14:
        psi = data.initial_state * np.exp(-1j * data.initial_energy * runtime)
    else:
        psi = data.initial_state.copy()
        for step in range(steps):
            u_mid = (step + 0.5) / steps
            s_mid = schedule.fn(float(u_mid))
            hamiltonian = data.h_initial + s_mid * data.d_hamiltonian
            psi = apply_step(hamiltonian, psi, dt, step_method)

    final_norm = float(np.linalg.norm(psi))
    if final_norm <= 1e-15:
        raise ValueError(f"{data.case.label}: evolution produced a zero state")
    norm_error = abs(final_norm - 1.0)
    psi = psi / final_norm

    rho = logical_resource_from_state(psi, data.n_sites, data.case)
    ground_overlap = float(abs(np.vdot(data.target_ground, psi)) ** 2)
    final_energy = float(np.real(np.vdot(psi, data.h_target @ psi)))

    return EvolutionResult(
        case=data.case,
        schedule=schedule.name,
        runtime=runtime,
        steps=steps,
        dt=dt,
        method=step_method,
        final_norm_error=norm_error,
        final_ground_overlap=ground_overlap,
        diabatic_loss=max(0.0, 1.0 - ground_overlap),
        final_energy_excess=max(0.0, final_energy - data.target_energy),
        metrics=resource_metrics(rho),
        resource_rho=rho,
    )


def no_signal_audit(
    resource_rho: np.ndarray,
    random_inputs: int,
    seed: int,
) -> NoSignalAudit:
    rng = np.random.default_rng(seed)
    states = probe_states(rng, random_inputs)
    bob_marginal = partial_trace(resource_rho, dims=[2, 2], keep=[1])
    half_identity = 0.5 * I2

    fidelities: list[float] = []
    reference_no_record: np.ndarray | None = None
    max_trace_error = 0.0
    max_no_record_to_marginal = 0.0
    max_pairwise_no_record = 0.0

    for state in states:
        corrected, no_record, _probabilities = teleport_density(
            projector(state),
            resource_rho,
        )
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

    return NoSignalAudit(
        sampled_mean_fidelity=float(np.mean(fidelities)),
        sampled_min_fidelity=float(np.min(fidelities)),
        sampled_max_fidelity=float(np.max(fidelities)),
        max_trace_error=max_trace_error,
        max_no_record_to_marginal_distance=max_no_record_to_marginal,
        max_pairwise_no_record_distance=max_pairwise_no_record,
        bob_marginal_bias=trace_distance(bob_marginal, half_identity),
    )


def parse_float_list(raw: str, option_name: str) -> tuple[float, ...]:
    values: list[float] = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        values.append(float(item))
    if not values:
        raise ValueError(f"{option_name} must include at least one value")
    return tuple(values)


def parse_schedule_list(raw: str) -> tuple[Schedule, ...]:
    names = tuple(item.strip() for item in raw.split(",") if item.strip())
    if not names:
        raise ValueError("--schedules must include at least one schedule")
    unknown = [name for name in names if name not in SCHEDULES]
    if unknown:
        raise ValueError(
            f"unknown schedule(s): {', '.join(unknown)}; "
            f"valid schedules are {', '.join(SCHEDULES)}"
        )
    return tuple(SCHEDULES[name] for name in names)


def selected_cases(requested: list[str] | None, include_1d: bool) -> tuple[AuditCase, ...]:
    if requested:
        by_label = {case.label: case for case in ALL_CASES}
        return tuple(by_label[label] for label in requested)
    if include_1d:
        return BASE_CASES + OPTIONAL_1D_CASES
    return BASE_CASES


def null_control_clean(result: EvolutionResult, tolerance: float) -> bool:
    return (
        result.is_null
        and result.metrics.best_bell_overlap <= 0.5 + 10.0 * tolerance
        and result.metrics.negativity <= 10.0 * tolerance
        and result.metrics.exact_avg_fidelity <= CLASSICAL_AVG_FIDELITY + 10.0 * tolerance
    )


def choose_candidate(results: list[EvolutionResult]) -> EvolutionResult | None:
    candidates = [
        result
        for result in results
        if result.case.dim == 2 and not result.is_null
    ]
    if not candidates:
        candidates = [result for result in results if not result.is_null]
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda result: (
            result.metrics.exact_avg_fidelity,
            result.final_ground_overlap,
            result.runtime,
        ),
    )


def print_case_header(data: CaseData) -> None:
    case = data.case
    metrics = data.target_metrics
    print(f"Case: {case.label}")
    print(
        "  setup: "
        f"dim={case.dim} side={case.side} N={data.n_sites} envs={data.n_env}, "
        f"mass={case.mass:g}, G_target={case.G:g}, "
        f"||dH/ds||_2={fmt_float(data.d_hamiltonian_norm)}"
    )
    print(
        "  start/target: "
        f"initial E0={fmt_float(data.initial_energy)}, initial gap={fmt_float(data.initial_gap)}, "
        f"initial degeneracy={data.initial_ground_degeneracy}, "
        f"target gap={fmt_float(data.target_gap)}"
    )
    print(f"  start mode: {data.initial_state_mode}")
    print(
        "  target ground resource: "
        f"Phi+={metrics.phi_plus_overlap:.6f}, "
        f"Bell*={metrics.best_bell_overlap:.6f} ({metrics.best_bell_label}), "
        f"Favg={metrics.exact_avg_fidelity:.6f}, "
        f"CHSH={metrics.logical_chsh:.6f}, neg={metrics.negativity:.6f}"
    )


def print_result_table(results: list[EvolutionResult]) -> None:
    print("  finite-time rows:")
    print(
        "    "
        f"{'sched':10s} {'T':>7s} {'steps':>6s} {'dt':>9s} "
        f"{'|<gT|psi>|2':>12s} {'loss':>11s} {'Phi+':>9s} "
        f"{'Bell*':>9s} {'label':>5s} {'Favg':>9s} {'neg':>9s}"
    )
    for result in results:
        metrics = result.metrics
        print(
            "    "
            f"{result.schedule[:10]:10s} "
            f"{result.runtime:7.3f} "
            f"{result.steps:6d} "
            f"{fmt_float(result.dt):>9s} "
            f"{fmt_float(result.final_ground_overlap):>12s} "
            f"{fmt_float(result.diabatic_loss):>11s} "
            f"{metrics.phi_plus_overlap:9.6f} "
            f"{metrics.best_bell_overlap:9.6f} "
            f"{metrics.best_bell_label:>5s} "
            f"{metrics.exact_avg_fidelity:9.6f} "
            f"{metrics.negativity:9.6f}"
        )


def print_case_results(
    data: CaseData,
    results: list[EvolutionResult],
    high_fidelity_threshold: float,
    tolerance: float,
) -> None:
    print_case_header(data)
    print_result_table(results)

    best_ground = max(results, key=lambda result: result.final_ground_overlap)
    best_fidelity = max(results, key=lambda result: result.metrics.exact_avg_fidelity)
    print(
        "  best final-ground overlap: "
        f"{best_ground.final_ground_overlap:.6f} "
        f"({best_ground.schedule}, T={best_ground.runtime:g}, "
        f"loss={fmt_float(best_ground.diabatic_loss)})"
    )
    print(
        "  best standard teleportation fidelity: "
        f"{best_fidelity.metrics.exact_avg_fidelity:.6f} "
        f"({best_fidelity.schedule}, T={best_fidelity.runtime:g}, "
        f"Phi+={best_fidelity.metrics.phi_plus_overlap:.6f}, "
        f"energy excess={fmt_float(best_fidelity.final_energy_excess)})"
    )

    if abs(data.case.G) <= 1e-15:
        clean = all(null_control_clean(result, tolerance) for result in results)
        print(f"  null/control non-resource check: {'PASS' if clean else 'FAIL'}")
    else:
        high_rows = [
            result
            for result in results
            if result.metrics.exact_avg_fidelity >= high_fidelity_threshold
        ]
        low_loss_rows = [result for result in results if result.diabatic_loss <= 1e-3]
        print(
            "  finite-time sensitivity: "
            f"{len(high_rows)}/{len(results)} rows have Favg >= "
            f"{high_fidelity_threshold:.3f}; "
            f"{len(low_loss_rows)}/{len(results)} rows have diabatic loss <= 1e-3"
        )
    print()


def print_candidate_audit(
    candidate: EvolutionResult | None,
    audit: NoSignalAudit | None,
    random_inputs: int,
    seed: int,
    tolerance: float,
) -> None:
    print("Final candidate audit:")
    if candidate is None or audit is None:
        print("  no non-null candidate was selected")
        return

    pairwise_ok = audit.max_pairwise_no_record_distance <= 10.0 * tolerance
    marginal_ok = audit.max_no_record_to_marginal_distance <= 10.0 * tolerance
    print(
        "  selected by best available standard mean fidelity "
        "(preferring 2D when present): "
        f"{candidate.case.label}, schedule={candidate.schedule}, T={candidate.runtime:g}, "
        f"steps={candidate.steps}, method={candidate.method}"
    )
    print(
        "  resource: "
        f"ground overlap={candidate.final_ground_overlap:.6f}, "
        f"diabatic loss={fmt_float(candidate.diabatic_loss)}, "
        f"Phi+={candidate.metrics.phi_plus_overlap:.6f}, "
        f"Favg={candidate.metrics.exact_avg_fidelity:.6f}, "
        f"Bell*={candidate.metrics.best_bell_overlap:.6f} "
        f"({candidate.metrics.best_bell_label})"
    )
    print(
        "  sampled teleportation/no-message audit: "
        f"{6 + random_inputs} inputs (seed={seed}), "
        f"mean/min/max fidelity={audit.sampled_mean_fidelity:.6f}/"
        f"{audit.sampled_min_fidelity:.6f}/{audit.sampled_max_fidelity:.6f}, "
        f"trace error={audit.max_trace_error:.3e}"
    )
    print(
        "  Bob before message: "
        f"distance to resource marginal="
        f"{audit.max_no_record_to_marginal_distance:.3e}, "
        f"pairwise input distance={audit.max_pairwise_no_record_distance:.3e}, "
        f"marginal bias from I/2={audit.bob_marginal_bias:.3e}, "
        f"input-independence={'PASS' if pairwise_ok and marginal_ok else 'FAIL'}"
    )


def print_conclusion(
    results: list[EvolutionResult],
    candidate: EvolutionResult | None,
    audit: NoSignalAudit | None,
    high_fidelity_threshold: float,
    tolerance: float,
) -> None:
    nulls = [result for result in results if result.is_null]
    clean_nulls = [result for result in nulls if null_control_clean(result, tolerance)]
    non_null = [result for result in results if not result.is_null]
    high_non_null = [
        result
        for result in non_null
        if result.metrics.exact_avg_fidelity >= high_fidelity_threshold
    ]

    print()
    print("Conclusion:")
    print(f"  null/control paths non-resource: {len(clean_nulls)}/{len(nulls)}")
    print(
        f"  non-null finite-time rows above Favg {high_fidelity_threshold:.3f}: "
        f"{len(high_non_null)}/{len(non_null)}"
    )

    if candidate is None:
        verdict = "negative result: no non-null finite-time candidate was selected"
    elif audit is not None and (
        audit.max_pairwise_no_record_distance > 10.0 * tolerance
        or audit.max_no_record_to_marginal_distance > 10.0 * tolerance
    ):
        verdict = "diagnostic only: candidate failed Bob pre-message input-independence"
    elif (
        candidate.metrics.exact_avg_fidelity >= high_fidelity_threshold
        and candidate.diabatic_loss <= 1e-3
    ):
        verdict = (
            "useful preparation candidate diagnostic on this small ideal model; "
            "not a preparation proof"
        )
    elif candidate.metrics.exact_avg_fidelity >= high_fidelity_threshold:
        verdict = "useful resource diagnostic, but runtime is still diabatic"
    else:
        verdict = "diagnostic/negative under the current finite-time grid"
    print(f"  verdict: {verdict}")
    print(
        "  Claim boundary: ordinary quantum state teleportation only; no matter, "
        "mass, charge, energy, object, or faster-than-light transport."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        choices=[case.label for case in ALL_CASES],
        action="append",
        help="case label to run; omit for the default 2D null and 2D Poisson cases",
    )
    parser.add_argument(
        "--include-1d",
        action="store_true",
        help="also run the bounded 1D N=8 null and Poisson cases",
    )
    parser.add_argument(
        "--runtimes",
        default="1,2,5,10,20,40,80",
        help="comma-separated finite runtimes for non-null paths",
    )
    parser.add_argument(
        "--null-runtime",
        type=float,
        default=20.0,
        help="runtime used for G=0 null controls",
    )
    parser.add_argument(
        "--schedules",
        default="linear,smoothstep",
        help=f"comma-separated schedules from: {', '.join(SCHEDULES)}",
    )
    parser.add_argument(
        "--steps-per-unit",
        type=float,
        default=8.0,
        help="minimum midpoint unitary slices per runtime unit",
    )
    parser.add_argument(
        "--min-steps",
        type=int,
        default=160,
        help="minimum midpoint unitary slices per evolution",
    )
    parser.add_argument(
        "--method",
        choices=("auto", "expm_multiply", "eigh"),
        default="auto",
        help="piecewise-constant unitary propagation method",
    )
    parser.add_argument(
        "--high-fidelity-threshold",
        type=float,
        default=0.90,
        help="standard mean teleportation-fidelity threshold for row counts",
    )
    parser.add_argument(
        "--random-inputs",
        type=int,
        default=64,
        help="random qubit inputs for the final candidate Bob pre-message audit",
    )
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-10,
        help="numerical tolerance for null/no-signaling checks",
    )
    parser.add_argument(
        "--degeneracy-tolerance",
        type=float,
        default=1e-9,
        help="energy tolerance for identifying a degenerate initial ground space",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> tuple[tuple[float, ...], tuple[Schedule, ...]]:
    runtimes = parse_float_list(args.runtimes, "--runtimes")
    if any(runtime <= 0.0 for runtime in runtimes):
        raise ValueError("--runtimes must contain only positive values")
    if args.null_runtime <= 0.0:
        raise ValueError("--null-runtime must be positive")
    schedules = parse_schedule_list(args.schedules)
    if args.steps_per_unit <= 0.0:
        raise ValueError("--steps-per-unit must be positive")
    if args.min_steps < 1:
        raise ValueError("--min-steps must be positive")
    if not (0.0 < args.high_fidelity_threshold <= 1.0):
        raise ValueError("--high-fidelity-threshold must be in (0, 1]")
    if args.random_inputs < 0:
        raise ValueError("--random-inputs must be nonnegative")
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")
    if args.degeneracy_tolerance <= 0.0:
        raise ValueError("--degeneracy-tolerance must be positive")
    return runtimes, schedules


def main() -> int:
    args = parse_args()
    runtimes, schedules = validate_args(args)
    cases = selected_cases(args.case, args.include_1d)

    print("FINITE-TIME ADIABATIC TASTE-QUBIT TELEPORTATION RESOURCE EVOLUTION")
    print("Status: planning / first artifact; ordinary quantum state teleportation only")
    print(
        "Evolution: midpoint piecewise-unitary Schrodinger evolution under "
        "H(s)=H(G=0)+s(t)*(H(G_target)-H(G=0))"
    )
    print(
        "Extraction: trace cells/spectator tastes, keep the last KS taste bit "
        "per species"
    )
    print(
        "Schedules: "
        + "; ".join(f"{schedule.name}: {schedule.description}" for schedule in schedules)
    )
    print(
        "Numerics: "
        f"runtimes={','.join(fmt_float(value) for value in runtimes)}, "
        f"null_runtime={args.null_runtime:g}, "
        f"steps_per_unit={args.steps_per_unit:g}, min_steps={args.min_steps}, "
        f"method={args.method}"
    )
    print()

    all_results: list[EvolutionResult] = []
    for case in cases:
        data = build_case_data(case, args.degeneracy_tolerance)
        case_schedules = schedules
        case_runtimes = runtimes
        if abs(case.G) <= 1e-15:
            case_schedules = schedules[:1]
            case_runtimes = (args.null_runtime,)

        case_results: list[EvolutionResult] = []
        for schedule in case_schedules:
            for runtime in case_runtimes:
                case_results.append(
                    evolve_case(
                        data,
                        schedule=schedule,
                        runtime=runtime,
                        steps_per_unit=args.steps_per_unit,
                        min_steps=args.min_steps,
                        method=args.method,
                    )
                )

        all_results.extend(case_results)
        print_case_results(
            data,
            case_results,
            high_fidelity_threshold=args.high_fidelity_threshold,
            tolerance=args.tolerance,
        )

    candidate = choose_candidate(all_results)
    audit = (
        no_signal_audit(candidate.resource_rho, args.random_inputs, args.seed)
        if candidate is not None
        else None
    )
    print_candidate_audit(
        candidate,
        audit,
        random_inputs=args.random_inputs,
        seed=args.seed,
        tolerance=args.tolerance,
    )
    print_conclusion(
        all_results,
        candidate,
        audit,
        high_fidelity_threshold=args.high_fidelity_threshold,
        tolerance=args.tolerance,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
