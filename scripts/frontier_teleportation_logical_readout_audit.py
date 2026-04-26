#!/usr/bin/env python3
"""Logical readout/extraction audit for Poisson taste-qubit teleportation.

Status: planning / first artifact. This runner audits the extraction used by
the current teleportation lane:

    full two-species state -> keep last KS taste bit per species -> trace cells
    and spectator tastes -> two-qubit logical resource.

The trace is a mathematically valid quantum operation and gives the right
statistics for taste-only observables of the form O_logical tensor I_env. This
runner asks the separate operational question: do the fixed-environment
branches look uniform enough that cells/spectators can simply be ignored, or
does the lane still need an explicit taste-only readout/apparatus argument?

It remains ordinary quantum state teleportation only. It does not claim matter
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
    density_checks,
    partial_trace,
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
    bell_state,
    best_bell_overlap,
    factor_sites,
    ground_state_resource,
    negativity,
    reduced_logical_resource,
    two_qubit_chsh,
)


HIGH_FIDELITY_DEFAULT = 0.90


@dataclasses.dataclass(frozen=True)
class BranchRecord:
    env_a: tuple[tuple[int, ...], tuple[int, ...]]
    env_b: tuple[tuple[int, ...], tuple[int, ...]]
    probability: float
    best_bell_fidelity: float
    best_bell_label: str
    traced_label_overlap: float
    chsh: float
    negativity: float
    bob_bias: float


@dataclasses.dataclass(frozen=True)
class BranchDiagnostics:
    branch_count: int
    active_branch_count: int
    total_probability: float
    active_probability: float
    effective_branch_count: float
    probability_min: float
    probability_max: float
    best_fidelity_min: float
    best_fidelity_max: float
    best_fidelity_weighted_mean: float
    best_fidelity_weighted_std: float
    traced_label_overlap_min: float
    traced_label_overlap_max: float
    traced_label_overlap_weighted_mean: float
    traced_label_overlap_weighted_std: float
    bob_bias_min: float
    bob_bias_max: float
    bob_bias_weighted_mean: float
    high_fidelity_branch_count: int
    high_fidelity_probability: float
    traced_label_high_fidelity_branch_count: int
    traced_label_high_fidelity_probability: float
    label_probability_mass: tuple[tuple[str, float, int], ...]
    most_likely_branch: BranchRecord | None
    best_fidelity_branch: BranchRecord | None
    worst_traced_label_branch: BranchRecord | None


@dataclasses.dataclass(frozen=True)
class BobNoMessageDiagnostics:
    bob_marginal_bias: float
    max_no_record_to_resource_marginal: float
    max_pairwise_no_record_distance: float
    max_branch_probability_span: float
    max_corrected_trace_error: float
    probe_count: int


@dataclasses.dataclass(frozen=True)
class AuditResult:
    case: AuditCase
    n_sites: int
    n_env: int
    ground_energy: float
    full_chsh: float
    trace_error: float
    hermitian_error: float
    min_eigenvalue: float
    trace_valid: bool
    traced_bell_fidelity: float
    traced_bell_label: str
    traced_chsh: float
    traced_purity: float
    traced_negativity: float
    branch: BranchDiagnostics
    bob_no_message: BobNoMessageDiagnostics


def poisson_cases(include_null: bool) -> list[AuditCase]:
    cases = [case for case in DEFAULT_CASES if include_null or abs(case.G) > 1e-15]
    return cases


def projector(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


def bell_overlap(rho: np.ndarray, z_bit: int, x_bit: int) -> float:
    state = bell_state(z_bit, x_bit)
    return float(np.real(np.vdot(state, rho @ state)))


def label_to_outcome(label: str) -> tuple[int, int]:
    for outcome, outcome_label in OUTCOME_LABELS.items():
        if outcome_label == label:
            return outcome
    raise ValueError(f"unknown Bell label: {label}")


def fmt_probability(value: float) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3:
        return f"{value:.6e}"
    return f"{value:.6f}"


def fmt_attempts(probability: float) -> str:
    if probability <= 0.0:
        return "inf"
    return f"{1.0 / probability:.6g}"


def fmt_env(label: tuple[tuple[int, ...], tuple[int, ...]]) -> str:
    cell, spectator = label
    return f"cell={cell}, spectator={spectator}"


def weighted_mean_std(values: list[float], weights: list[float]) -> tuple[float, float]:
    total = float(np.sum(weights))
    if total <= 0.0:
        return 0.0, 0.0
    value_array = np.asarray(values, dtype=float)
    weight_array = np.asarray(weights, dtype=float)
    mean = float(np.sum(weight_array * value_array) / total)
    variance = float(np.sum(weight_array * (value_array - mean) ** 2) / total)
    return mean, math.sqrt(max(variance, 0.0))


def effective_count(probabilities: list[float]) -> float:
    participation = float(np.sum(np.asarray(probabilities, dtype=float) ** 2))
    if participation <= 0.0:
        return math.inf
    return 1.0 / participation


def make_probe_states(seed: int, random_count: int) -> list[np.ndarray]:
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


def branch_record(
    branch: np.ndarray,
    probability: float,
    env_a: tuple[tuple[int, ...], tuple[int, ...]],
    env_b: tuple[tuple[int, ...], tuple[int, ...]],
    traced_label: str,
) -> BranchRecord:
    branch_state = (branch / math.sqrt(probability)).reshape(4)
    rho = np.outer(branch_state, branch_state.conj())
    best_fidelity, best_label = best_bell_overlap(rho)
    traced_outcome = label_to_outcome(traced_label)
    bob_marginal = partial_trace(rho, dims=[2, 2], keep=[1])
    return BranchRecord(
        env_a=env_a,
        env_b=env_b,
        probability=probability,
        best_bell_fidelity=best_fidelity,
        best_bell_label=best_label,
        traced_label_overlap=bell_overlap(rho, *traced_outcome),
        chsh=two_qubit_chsh(rho),
        negativity=negativity(rho),
        bob_bias=trace_distance(bob_marginal, 0.5 * I2),
    )


def scan_branches(
    amp: np.ndarray,
    env_labels: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
    traced_label: str,
    high_fidelity_threshold: float,
    probability_floor: float,
) -> BranchDiagnostics:
    probabilities: list[float] = []
    records: list[BranchRecord] = []

    for env_a, label_a in enumerate(env_labels):
        for env_b, label_b in enumerate(env_labels):
            branch = amp[:, env_a, :, env_b]
            probability = float(np.real(np.vdot(branch, branch)))
            probabilities.append(probability)
            if probability <= 0.0 or probability < probability_floor:
                continue
            records.append(
                branch_record(
                    branch=branch,
                    probability=probability,
                    env_a=label_a,
                    env_b=label_b,
                    traced_label=traced_label,
                )
            )

    total_probability = float(np.sum(probabilities))
    if not records:
        return BranchDiagnostics(
            branch_count=len(probabilities),
            active_branch_count=0,
            total_probability=total_probability,
            active_probability=0.0,
            effective_branch_count=effective_count(probabilities),
            probability_min=0.0,
            probability_max=0.0,
            best_fidelity_min=0.0,
            best_fidelity_max=0.0,
            best_fidelity_weighted_mean=0.0,
            best_fidelity_weighted_std=0.0,
            traced_label_overlap_min=0.0,
            traced_label_overlap_max=0.0,
            traced_label_overlap_weighted_mean=0.0,
            traced_label_overlap_weighted_std=0.0,
            bob_bias_min=0.0,
            bob_bias_max=0.0,
            bob_bias_weighted_mean=0.0,
            high_fidelity_branch_count=0,
            high_fidelity_probability=0.0,
            traced_label_high_fidelity_branch_count=0,
            traced_label_high_fidelity_probability=0.0,
            label_probability_mass=(),
            most_likely_branch=None,
            best_fidelity_branch=None,
            worst_traced_label_branch=None,
        )

    weights = [record.probability for record in records]
    best_values = [record.best_bell_fidelity for record in records]
    traced_values = [record.traced_label_overlap for record in records]
    bob_bias_values = [record.bob_bias for record in records]
    best_mean, best_std = weighted_mean_std(best_values, weights)
    traced_mean, traced_std = weighted_mean_std(traced_values, weights)
    bob_bias_mean, _bob_bias_std = weighted_mean_std(bob_bias_values, weights)

    high_records = [
        record
        for record in records
        if record.best_bell_fidelity >= high_fidelity_threshold
    ]
    traced_high_records = [
        record
        for record in records
        if record.traced_label_overlap >= high_fidelity_threshold
    ]

    label_entries: list[tuple[str, float, int]] = []
    for label in sorted(set(OUTCOME_LABELS.values())):
        matching = [record for record in records if record.best_bell_label == label]
        label_entries.append(
            (
                label,
                float(np.sum([record.probability for record in matching])),
                len(matching),
            )
        )

    return BranchDiagnostics(
        branch_count=len(probabilities),
        active_branch_count=len(records),
        total_probability=total_probability,
        active_probability=float(np.sum(weights)),
        effective_branch_count=effective_count(probabilities),
        probability_min=float(np.min(weights)),
        probability_max=float(np.max(weights)),
        best_fidelity_min=float(np.min(best_values)),
        best_fidelity_max=float(np.max(best_values)),
        best_fidelity_weighted_mean=best_mean,
        best_fidelity_weighted_std=best_std,
        traced_label_overlap_min=float(np.min(traced_values)),
        traced_label_overlap_max=float(np.max(traced_values)),
        traced_label_overlap_weighted_mean=traced_mean,
        traced_label_overlap_weighted_std=traced_std,
        bob_bias_min=float(np.min(bob_bias_values)),
        bob_bias_max=float(np.max(bob_bias_values)),
        bob_bias_weighted_mean=bob_bias_mean,
        high_fidelity_branch_count=len(high_records),
        high_fidelity_probability=float(
            np.sum([record.probability for record in high_records])
        ),
        traced_label_high_fidelity_branch_count=len(traced_high_records),
        traced_label_high_fidelity_probability=float(
            np.sum([record.probability for record in traced_high_records])
        ),
        label_probability_mass=tuple(label_entries),
        most_likely_branch=max(records, key=lambda record: record.probability),
        best_fidelity_branch=max(records, key=lambda record: record.best_bell_fidelity),
        worst_traced_label_branch=min(records, key=lambda record: record.traced_label_overlap),
    )


def bob_no_message_diagnostics(
    resource_rho: np.ndarray,
    states: list[np.ndarray],
) -> BobNoMessageDiagnostics:
    bob_marginal = partial_trace(resource_rho, dims=[2, 2], keep=[1])
    reference_no_record: np.ndarray | None = None
    max_no_record_to_marginal = 0.0
    max_pairwise_no_record = 0.0
    max_branch_probability_span = 0.0
    max_corrected_trace_error = 0.0

    for state in states:
        corrected, no_record, probabilities = teleport_density(projector(state), resource_rho)
        max_corrected_trace_error = max(
            max_corrected_trace_error,
            float(abs(np.trace(corrected) - 1.0)),
        )
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
        probability_values = list(probabilities.values())
        max_branch_probability_span = max(
            max_branch_probability_span,
            float(max(probability_values) - min(probability_values)),
        )

    return BobNoMessageDiagnostics(
        bob_marginal_bias=trace_distance(bob_marginal, 0.5 * I2),
        max_no_record_to_resource_marginal=max_no_record_to_marginal,
        max_pairwise_no_record_distance=max_pairwise_no_record,
        max_branch_probability_span=max_branch_probability_span,
        max_corrected_trace_error=max_corrected_trace_error,
        probe_count=len(states),
    )


def audit_case(
    case: AuditCase,
    states: list[np.ndarray],
    high_fidelity_threshold: float,
    probability_floor: float,
    tolerance: float,
) -> AuditResult:
    resource = ground_state_resource(case)
    n_sites = int(resource["n"])
    factors = factor_sites(case.dim, case.side)
    amp = amplitudes_by_logical_env(resource["psi"], n_sites, factors)
    rho = reduced_logical_resource(amp)
    checks = density_checks(rho, tolerance=tolerance)
    traced_fidelity, traced_label = best_bell_overlap(rho)
    branch = scan_branches(
        amp=amp,
        env_labels=factors.env_labels,
        traced_label=traced_label,
        high_fidelity_threshold=high_fidelity_threshold,
        probability_floor=probability_floor,
    )

    return AuditResult(
        case=case,
        n_sites=n_sites,
        n_env=len(factors.env_labels),
        ground_energy=float(resource["ground_energy"]),
        full_chsh=float(resource["full_chsh"]),
        trace_error=checks.trace_error,
        hermitian_error=checks.hermitian_error,
        min_eigenvalue=checks.min_eigenvalue,
        trace_valid=checks.valid and abs(branch.total_probability - 1.0) <= 10 * tolerance,
        traced_bell_fidelity=traced_fidelity,
        traced_bell_label=traced_label,
        traced_chsh=two_qubit_chsh(rho),
        traced_purity=float(np.real(np.trace(rho @ rho))),
        traced_negativity=negativity(rho),
        branch=branch,
        bob_no_message=bob_no_message_diagnostics(rho, states),
    )


def print_branch_record(prefix: str, record: BranchRecord | None) -> None:
    if record is None:
        print(f"    {prefix}: none above probability floor")
        return
    print(
        f"    {prefix}: p={fmt_probability(record.probability)} "
        f"(attempts {fmt_attempts(record.probability)}), "
        f"best Bell={record.best_bell_fidelity:.6f} ({record.best_bell_label}), "
        f"traced-label overlap={record.traced_label_overlap:.6f}, "
        f"CHSH={record.chsh:.6f}, negativity={record.negativity:.6f}, "
        f"Bob bias={record.bob_bias:.3e}"
    )
    print(f"      env A={fmt_env(record.env_a)}")
    print(f"      env B={fmt_env(record.env_b)}")


def print_result(result: AuditResult, high_fidelity_threshold: float) -> None:
    case = result.case
    branch = result.branch
    bob = result.bob_no_message

    print(f"Case: {case.label}")
    print(
        "  lattice/params: "
        f"dim={case.dim} side={case.side} N={result.n_sites} "
        f"envs/logical_qubit={result.n_env} mass={case.mass:g} G={case.G:g}"
    )
    print(
        "  full state: "
        f"E0={result.ground_energy:.12g}, CHSH={result.full_chsh:.6f}"
    )
    print(
        "  trace extraction validity: "
        f"trace error={result.trace_error:.3e}, "
        f"hermitian error={result.hermitian_error:.3e}, "
        f"min eig={result.min_eigenvalue:.3e}, "
        f"branch probability sum={branch.total_probability:.12f}, "
        f"valid={'YES' if result.trace_valid else 'NO'}"
    )
    print(
        "  traced logical resource: "
        f"best Bell={result.traced_bell_fidelity:.6f} "
        f"({result.traced_bell_label}), CHSH={result.traced_chsh:.6f}, "
        f"purity={result.traced_purity:.6f}, "
        f"negativity={result.traced_negativity:.6f}"
    )
    print("  fixed-env branch variation:")
    print(
        f"    branches={branch.branch_count}, active={branch.active_branch_count}, "
        f"active probability={branch.active_probability:.12f}, "
        f"effective branch count={branch.effective_branch_count:.6f}"
    )
    print(
        f"    branch probability range={fmt_probability(branch.probability_min)}.."
        f"{fmt_probability(branch.probability_max)}"
    )
    print(
        "    best-Bell fidelity range/weighted: "
        f"{branch.best_fidelity_min:.6f}..{branch.best_fidelity_max:.6f}, "
        f"mean={branch.best_fidelity_weighted_mean:.6f}, "
        f"std={branch.best_fidelity_weighted_std:.6f}"
    )
    print(
        f"    overlap with traced label {result.traced_bell_label}: "
        f"{branch.traced_label_overlap_min:.6f}.."
        f"{branch.traced_label_overlap_max:.6f}, "
        f"weighted mean={branch.traced_label_overlap_weighted_mean:.6f}, "
        f"std={branch.traced_label_overlap_weighted_std:.6f}"
    )
    print(
        "    branch Bob-bias range/weighted mean: "
        f"{branch.bob_bias_min:.3e}..{branch.bob_bias_max:.3e}, "
        f"mean={branch.bob_bias_weighted_mean:.3e}"
    )
    label_parts = ", ".join(
        f"{label}=p:{fmt_probability(probability)} n:{count}"
        for label, probability, count in branch.label_probability_mass
        if count > 0 or probability > 0.0
    )
    print(f"    branch best-label mass: {label_parts}")
    print(
        "    high-fidelity postselection mass "
        f"(best Bell >= {high_fidelity_threshold:.3f}): "
        f"count={branch.high_fidelity_branch_count}, "
        f"p={fmt_probability(branch.high_fidelity_probability)}, "
        f"attempts={fmt_attempts(branch.high_fidelity_probability)}"
    )
    print(
        "    high-fidelity mass for traced label "
        f"({result.traced_bell_label} >= {high_fidelity_threshold:.3f}): "
        f"count={branch.traced_label_high_fidelity_branch_count}, "
        f"p={fmt_probability(branch.traced_label_high_fidelity_probability)}, "
        f"attempts={fmt_attempts(branch.traced_label_high_fidelity_probability)}"
    )
    print_branch_record("most-likely fixed-env branch", branch.most_likely_branch)
    print_branch_record("best-fidelity postselected branch", branch.best_fidelity_branch)
    print_branch_record("worst traced-label branch", branch.worst_traced_label_branch)
    print(
        "  Bob before classical message under traced resource: "
        f"probe states={bob.probe_count}, "
        f"marginal bias from I/2={bob.bob_marginal_bias:.3e}, "
        f"max no-record to resource marginal={bob.max_no_record_to_resource_marginal:.3e}, "
        f"max pairwise input distance={bob.max_pairwise_no_record_distance:.3e}, "
        f"max branch probability span={bob.max_branch_probability_span:.3e}, "
        f"max corrected trace error={bob.max_corrected_trace_error:.3e}"
    )
    print("  operational readout status:")
    print("    mathematical trace extraction: ESTABLISHED for taste-only statistics")
    print("    native taste-only readout/apparatus: NOT ESTABLISHED by this audit")
    print("    cells/spectators ignorable only under a proved O_logical tensor I_env readout")
    print()


def print_gatekeeping() -> None:
    print("Gatekeeping language:")
    print(
        "  Established: tracing cells and spectator tastes gives a valid logical "
        "density matrix and the correct probabilities for measurements that are "
        "strictly taste-only, i.e. O_logical tensor I_env."
    )
    print(
        "  Not established: a native apparatus that measures, prepares, or corrects "
        "only the retained taste bit while remaining blind to cell/spectator "
        "degrees of freedom."
    )
    print(
        "  Fixed-env/postselected branches are diagnostics. They become protocol "
        "resources only after an environment measurement, heralding rule, and "
        "branch-conditioned logical operation are supplied."
    )
    print(
        "  Bob's pre-message marginal can be biased relative to I/2, but the audited "
        "quantity is input independence before the classical Bell record arrives."
    )
    print(
        "  Claim boundary: quantum state teleportation planning only; no matter, "
        "mass, charge, energy, object, or faster-than-light transport."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument(
        "--random-inputs",
        type=int,
        default=128,
        help="random input states for Bob no-message audit",
    )
    parser.add_argument(
        "--high-fidelity-threshold",
        type=float,
        default=HIGH_FIDELITY_DEFAULT,
        help="threshold for high-fidelity branch counts",
    )
    parser.add_argument(
        "--probability-floor",
        type=float,
        default=1e-15,
        help="ignore fixed-env branches below this probability for normalized diagnostics",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-10,
        help="density-matrix and trace-validity tolerance",
    )
    parser.add_argument(
        "--include-null",
        action="store_true",
        help="include the G=0 null control in addition to the 1D/2D Poisson cases",
    )
    parser.add_argument(
        "--case",
        choices=[case.label for case in DEFAULT_CASES],
        action="append",
        help="case label to run; omit for default Poisson cases",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.random_inputs < 0:
        raise ValueError("--random-inputs must be nonnegative")
    if not 0.0 < args.high_fidelity_threshold <= 1.0:
        raise ValueError("--high-fidelity-threshold must be in (0, 1]")
    if args.probability_floor < 0.0:
        raise ValueError("--probability-floor must be nonnegative")
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")

    requested = set(args.case or [])
    if requested:
        cases = [case for case in DEFAULT_CASES if case.label in requested]
    else:
        cases = poisson_cases(include_null=args.include_null)
    states = make_probe_states(args.seed, args.random_inputs)

    print("TELEPORTATION LOGICAL READOUT/EXTRACTION AUDIT")
    print("Status: planning / first artifact; quantum state teleportation only")
    print(
        "Extraction under audit: keep last KS taste bit per species; trace "
        "cells and spectator tastes"
    )
    print(
        "Question: valid reduced logical state versus operationally addressable "
        "taste-only readout"
    )
    print(
        f"Input probes for Bob no-message audit: {len(states)} "
        f"(seed={args.seed}, random={args.random_inputs})"
    )
    print()

    results = [
        audit_case(
            case=case,
            states=states,
            high_fidelity_threshold=args.high_fidelity_threshold,
            probability_floor=args.probability_floor,
            tolerance=args.tolerance,
        )
        for case in cases
    ]
    for result in results:
        print_result(result, high_fidelity_threshold=args.high_fidelity_threshold)

    print_gatekeeping()
    return 0


if __name__ == "__main__":
    sys.exit(main())
