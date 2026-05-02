#!/usr/bin/env python3
"""Preparation/readout diagnostic for the Poisson-derived teleportation resource.

This is a bounded probe, not a dynamic preparation protocol.  It separates the
offline diagonalization/extraction result from what an operational story would
still need:

* spectral isolation of the ground state,
* overlap/projection probabilities into the ground manifold from simple
  reference states,
* deterministic traced logical resource diagnostics,
* fixed-environment postselection probabilities and branch quality,
* explicit preparation/readout limitations.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.linalg import eigh


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_bell_inequality import (  # noqa: E402
    build_H1,
    build_H2_tensor,
    build_pair_hop_X,
    build_poisson,
    build_sublattice_Z,
    chsh_horodecki,
)
from frontier_teleportation_resource_from_poisson import (  # noqa: E402
    AuditCase,
    DEFAULT_CASES,
    OUTCOME_LABELS,
    OUTCOME_ORDER,
    amplitudes_by_logical_env,
    bell_state,
    best_bell_overlap,
    coords_from_index,
    factor_sites,
    lattice_for_case,
    negativity,
    reduced_logical_resource,
    standard_teleportation_stats,
    two_qubit_chsh,
    verify_teleportation_convention,
)


@dataclasses.dataclass(frozen=True)
class SpectrumDiagnostics:
    ground_energy: float
    ground_multiplicity: int
    gap_to_next_distinct: float
    degeneracy_tolerance: float
    first_energies: tuple[float, ...]

    @property
    def isolated(self) -> bool:
        return self.ground_multiplicity == 1 and self.gap_to_next_distinct > 0.0


@dataclasses.dataclass(frozen=True)
class ProjectionDiagnostics:
    origin_pair_probability: float
    uniform_pair_probability: float
    best_site_pair_probability: float
    best_site_pair: tuple[int, int]


@dataclasses.dataclass(frozen=True)
class LogicalResourceDiagnostics:
    bell_fidelity: float
    bell_label: str
    bell_probabilities: tuple[tuple[str, float], ...]
    chsh: float
    purity: float
    negativity: float
    teleportation_mean: float
    teleportation_min: float
    teleportation_max: float
    teleportation_max_trace_error: float


@dataclasses.dataclass(frozen=True)
class BranchRecord:
    env_a: tuple[tuple[int, ...], tuple[int, ...]]
    env_b: tuple[tuple[int, ...], tuple[int, ...]]
    probability: float
    bell_fidelity: float
    bell_label: str
    chsh: float
    negativity: float


@dataclasses.dataclass(frozen=True)
class BranchScanDiagnostics:
    branch_count: int
    total_probability: float
    effective_branch_count: float
    high_fidelity_branch_count: int
    high_fidelity_total_probability: float
    best_fidelity_branch: BranchRecord | None
    most_likely_branch: BranchRecord | None


@dataclasses.dataclass(frozen=True)
class ProbeResult:
    case: AuditCase
    n_sites: int
    n_env: int
    full_state_chsh: float
    spectrum: SpectrumDiagnostics
    projections: ProjectionDiagnostics
    traced_resource: LogicalResourceDiagnostics
    manifold_average_resource: LogicalResourceDiagnostics | None
    branch_scan: BranchScanDiagnostics


def solve_case(
    case: AuditCase,
    energy_atol: float,
    energy_rtol: float,
) -> tuple[int, np.ndarray, np.ndarray, np.ndarray, np.ndarray, SpectrumDiagnostics]:
    n_sites, adj, parity, _coords = lattice_for_case(case)
    H1 = build_H1(n_sites, adj, parity, mass=case.mass)
    poisson = build_poisson(n_sites, adj)
    H2 = build_H2_tensor(H1, poisson, case.G, n_sites)
    evals, evecs = eigh(H2)

    ground_energy = float(evals[0])
    degeneracy_tolerance = energy_atol + energy_rtol * max(1.0, abs(ground_energy))
    ground_mask = evals <= evals[0] + degeneracy_tolerance
    ground_multiplicity = int(np.count_nonzero(ground_mask))
    if ground_multiplicity < len(evals):
        gap = float(evals[ground_multiplicity] - evals[0])
    else:
        gap = math.inf

    spectrum = SpectrumDiagnostics(
        ground_energy=ground_energy,
        ground_multiplicity=ground_multiplicity,
        gap_to_next_distinct=gap,
        degeneracy_tolerance=degeneracy_tolerance,
        first_energies=tuple(float(value) for value in evals[:8]),
    )
    return n_sites, adj, parity, evals, evecs, spectrum


def bell_probabilities(rho: np.ndarray) -> tuple[tuple[str, float], ...]:
    probabilities: list[tuple[str, float]] = []
    for z_bit, x_bit in OUTCOME_ORDER:
        state = bell_state(z_bit, x_bit)
        probability = float(np.real(state.conj() @ rho @ state))
        probabilities.append((OUTCOME_LABELS[(z_bit, x_bit)], probability))
    return tuple(probabilities)


def logical_resource_diagnostics(
    rho: np.ndarray,
    trials: int,
    seed: int,
) -> LogicalResourceDiagnostics:
    bell_fidelity, bell_label = best_bell_overlap(rho)
    teleportation = standard_teleportation_stats(rho, trials=trials, seed=seed)
    return LogicalResourceDiagnostics(
        bell_fidelity=bell_fidelity,
        bell_label=bell_label,
        bell_probabilities=bell_probabilities(rho),
        chsh=two_qubit_chsh(rho),
        purity=float(np.real(np.trace(rho @ rho))),
        negativity=negativity(rho),
        teleportation_mean=float(teleportation["mean"]),
        teleportation_min=float(teleportation["min"]),
        teleportation_max=float(teleportation["max"]),
        teleportation_max_trace_error=float(teleportation["max_trace_error"]),
    )


def manifold_average_logical_resource(
    evecs: np.ndarray,
    ground_multiplicity: int,
    n_sites: int,
    factors,
) -> np.ndarray:
    rho = np.zeros((4, 4), dtype=complex)
    for index in range(ground_multiplicity):
        amp = amplitudes_by_logical_env(evecs[:, index], n_sites, factors)
        rho += reduced_logical_resource(amp)
    return rho / float(ground_multiplicity)


def ground_projector_probabilities(
    evecs: np.ndarray,
    ground_multiplicity: int,
    n_sites: int,
) -> ProjectionDiagnostics:
    ground_basis = evecs[:, :ground_multiplicity]
    origin_pair = np.zeros(n_sites * n_sites, dtype=complex)
    origin_pair[0] = 1.0
    uniform_pair = np.ones(n_sites * n_sites, dtype=complex)
    uniform_pair /= np.linalg.norm(uniform_pair)

    origin_probability = float(
        np.sum(np.abs(ground_basis.conj().T @ origin_pair) ** 2)
    )
    uniform_probability = float(
        np.sum(np.abs(ground_basis.conj().T @ uniform_pair) ** 2)
    )
    site_pair_weights = np.sum(np.abs(ground_basis) ** 2, axis=1)
    best_flat_index = int(np.argmax(site_pair_weights))
    best_site_pair = divmod(best_flat_index, n_sites)

    return ProjectionDiagnostics(
        origin_pair_probability=origin_probability,
        uniform_pair_probability=uniform_probability,
        best_site_pair_probability=float(site_pair_weights[best_flat_index]),
        best_site_pair=best_site_pair,
    )


def branch_record(
    branch: np.ndarray,
    probability: float,
    env_a: tuple[tuple[int, ...], tuple[int, ...]],
    env_b: tuple[tuple[int, ...], tuple[int, ...]],
) -> BranchRecord:
    branch_state = (branch / math.sqrt(probability)).reshape(4)
    rho = np.outer(branch_state, branch_state.conj())
    bell_fidelity, bell_label = best_bell_overlap(rho)
    return BranchRecord(
        env_a=env_a,
        env_b=env_b,
        probability=probability,
        bell_fidelity=bell_fidelity,
        bell_label=bell_label,
        chsh=two_qubit_chsh(rho),
        negativity=negativity(rho),
    )


def fixed_env_branch_scan(
    amp: np.ndarray,
    env_labels: Iterable[tuple[tuple[int, ...], tuple[int, ...]]],
    high_fidelity_threshold: float,
    probability_floor: float,
) -> BranchScanDiagnostics:
    labels = tuple(env_labels)
    branch_count = len(labels) * len(labels)
    probabilities: list[float] = []
    high_fidelity_count = 0
    high_fidelity_probability = 0.0
    best_fidelity: BranchRecord | None = None
    most_likely: BranchRecord | None = None

    for env_a, label_a in enumerate(labels):
        for env_b, label_b in enumerate(labels):
            branch = amp[:, env_a, :, env_b]
            probability = float(np.real(np.vdot(branch, branch)))
            probabilities.append(probability)
            if probability < probability_floor:
                continue

            record = branch_record(branch, probability, label_a, label_b)
            if (
                best_fidelity is None
                or record.bell_fidelity > best_fidelity.bell_fidelity
            ):
                best_fidelity = record
            if most_likely is None or record.probability > most_likely.probability:
                most_likely = record
            if record.bell_fidelity >= high_fidelity_threshold:
                high_fidelity_count += 1
                high_fidelity_probability += record.probability

    probability_array = np.asarray(probabilities, dtype=float)
    total_probability = float(np.sum(probability_array))
    participation = float(np.sum(probability_array * probability_array))
    effective_branch_count = math.inf if participation <= 0.0 else 1.0 / participation

    return BranchScanDiagnostics(
        branch_count=branch_count,
        total_probability=total_probability,
        effective_branch_count=effective_branch_count,
        high_fidelity_branch_count=high_fidelity_count,
        high_fidelity_total_probability=high_fidelity_probability,
        best_fidelity_branch=best_fidelity,
        most_likely_branch=most_likely,
    )


def full_chsh_for_state(
    psi: np.ndarray,
    n_sites: int,
    parity: np.ndarray,
) -> float:
    sublattice_z = build_sublattice_Z(n_sites, parity)
    pair_hop_x = build_pair_hop_X(n_sites)
    chsh, _correlators = chsh_horodecki(
        psi,
        sublattice_z,
        pair_hop_x,
        sublattice_z,
        pair_hop_x,
        n_sites,
    )
    return float(chsh)


def run_probe_case(
    case: AuditCase,
    trials: int,
    seed: int,
    high_fidelity_threshold: float,
    probability_floor: float,
    energy_atol: float,
    energy_rtol: float,
) -> ProbeResult:
    n_sites, _adj, parity, _evals, evecs, spectrum = solve_case(
        case,
        energy_atol=energy_atol,
        energy_rtol=energy_rtol,
    )
    representative_ground_state = evecs[:, 0]
    factors = factor_sites(case.dim, case.side)
    amp = amplitudes_by_logical_env(representative_ground_state, n_sites, factors)
    traced_rho = reduced_logical_resource(amp)

    manifold_average = None
    if spectrum.ground_multiplicity > 1:
        manifold_rho = manifold_average_logical_resource(
            evecs,
            spectrum.ground_multiplicity,
            n_sites,
            factors,
        )
        manifold_average = logical_resource_diagnostics(
            manifold_rho,
            trials=trials,
            seed=seed + 100_000,
        )

    return ProbeResult(
        case=case,
        n_sites=n_sites,
        n_env=len(factors.env_labels),
        full_state_chsh=full_chsh_for_state(
            representative_ground_state,
            n_sites,
            parity,
        ),
        spectrum=spectrum,
        projections=ground_projector_probabilities(
            evecs,
            spectrum.ground_multiplicity,
            n_sites,
        ),
        traced_resource=logical_resource_diagnostics(
            traced_rho,
            trials=trials,
            seed=seed,
        ),
        manifold_average_resource=manifold_average,
        branch_scan=fixed_env_branch_scan(
            amp,
            factors.env_labels,
            high_fidelity_threshold=high_fidelity_threshold,
            probability_floor=probability_floor,
        ),
    )


def fmt_probability(value: float) -> str:
    if value == 0.0:
        return "0"
    if value < 1e-3:
        return f"{value:.6e}"
    return f"{value:.6f}"


def fmt_attempts(probability: float) -> str:
    if probability <= 0.0:
        return "inf"
    return f"{1.0 / probability:.6g}"


def fmt_env(label: tuple[tuple[int, ...], tuple[int, ...]]) -> str:
    cell, spectator = label
    return f"cell={cell}, spectator={spectator}"


def fmt_site_pair(
    site_pair: tuple[int, int],
    case: AuditCase,
) -> str:
    site_a, site_b = site_pair
    coords_a = coords_from_index(site_a, case.dim, case.side)
    coords_b = coords_from_index(site_b, case.dim, case.side)
    return f"({site_a}:{coords_a}, {site_b}:{coords_b})"


def print_logical_resource(prefix: str, diagnostics: LogicalResourceDiagnostics) -> None:
    bell_parts = ", ".join(
        f"{label}={fmt_probability(probability)}"
        for label, probability in diagnostics.bell_probabilities
    )
    print(
        f"  {prefix}: best Bell={diagnostics.bell_fidelity:.6f} "
        f"({diagnostics.bell_label}), CHSH={diagnostics.chsh:.6f}, "
        f"purity={diagnostics.purity:.6f}, negativity={diagnostics.negativity:.6f}"
    )
    print(f"    logical Bell projection probabilities: {bell_parts}")
    print(
        "    ideal-measurement teleportation with this resource: "
        f"mean={diagnostics.teleportation_mean:.6f}, "
        f"min={diagnostics.teleportation_min:.6f}, "
        f"max={diagnostics.teleportation_max:.6f}, "
        f"max trace error={diagnostics.teleportation_max_trace_error:.3e}"
    )


def print_branch_record(prefix: str, record: BranchRecord | None) -> None:
    if record is None:
        print(f"    {prefix}: none above probability floor")
        return
    print(
        f"    {prefix}: Bell={record.bell_fidelity:.6f} "
        f"({record.bell_label}), probability={fmt_probability(record.probability)}, "
        f"expected attempts={fmt_attempts(record.probability)}, "
        f"CHSH={record.chsh:.6f}, negativity={record.negativity:.6f}"
    )
    print(f"      env A={fmt_env(record.env_a)}")
    print(f"      env B={fmt_env(record.env_b)}")


def print_result(result: ProbeResult, high_fidelity_threshold: float, min_gap: float) -> None:
    case = result.case
    spectrum = result.spectrum
    projections = result.projections
    branch_scan = result.branch_scan

    print(f"Case: {case.label}")
    print(
        "  lattice/params: "
        f"dim={case.dim} side={case.side} N={result.n_sites} "
        f"envs/logical_qubit={result.n_env} mass={case.mass:g} G={case.G:g}"
    )
    print(
        "  spectrum: "
        f"E0={spectrum.ground_energy:.12g}, "
        f"ground multiplicity={spectrum.ground_multiplicity} "
        f"(tol={spectrum.degeneracy_tolerance:.3e}), "
        f"gap to next distinct={spectrum.gap_to_next_distinct:.6e}"
    )
    print(
        "    first energies: "
        + ", ".join(f"{energy:.9g}" for energy in spectrum.first_energies)
    )
    print(
        "  ground-manifold projection probabilities from simple references: "
        f"origin-pair={fmt_probability(projections.origin_pair_probability)}, "
        f"uniform-pair={fmt_probability(projections.uniform_pair_probability)}, "
        f"best site-pair={fmt_probability(projections.best_site_pair_probability)} "
        f"at {fmt_site_pair(projections.best_site_pair, case)}"
    )
    print(f"  representative ground-state full CHSH: {result.full_state_chsh:.6f}")
    print_logical_resource(
        "deterministic traced logical resource "
        "(trace environment; mathematical success probability=1)",
        result.traced_resource,
    )
    if result.manifold_average_resource is not None:
        print_logical_resource(
            "equal mixture over degenerate ground manifold "
            "(diagnostic; chosen physical mixture is unspecified)",
            result.manifold_average_resource,
        )

    print("  fixed-env postselection diagnostics:")
    print(
        f"    branches={branch_scan.branch_count}, "
        f"total probability={branch_scan.total_probability:.12f}, "
        f"effective branch count={branch_scan.effective_branch_count:.6f}"
    )
    print_branch_record("best-fidelity branch", branch_scan.best_fidelity_branch)
    print_branch_record("most-likely branch", branch_scan.most_likely_branch)
    print(
        "    aggregate high-fidelity branch mass "
        f"(Bell >= {high_fidelity_threshold:.3f}): "
        f"count={branch_scan.high_fidelity_branch_count}, "
        f"probability={fmt_probability(branch_scan.high_fidelity_total_probability)}, "
        f"expected attempts={fmt_attempts(branch_scan.high_fidelity_total_probability)}"
    )

    offline_resource = result.traced_resource.bell_fidelity >= high_fidelity_threshold
    isolated_enough = (
        spectrum.ground_multiplicity == 1 and spectrum.gap_to_next_distinct >= min_gap
    )
    print("  verdict:")
    print(f"    offline extracted traced resource: {'YES' if offline_resource else 'NO'}")
    print(
        f"    isolated ground state at min-gap {min_gap:.1e}: "
        f"{'YES' if isolated_enough else 'NO'}"
    )
    print("    preparation/readout protocol demonstrated: NO (diagnostic only)")
    print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=128, help="random teleportation inputs")
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument(
        "--high-fidelity-threshold",
        type=float,
        default=0.90,
        help="Bell-overlap threshold for high-fidelity resource diagnostics",
    )
    parser.add_argument(
        "--probability-floor",
        type=float,
        default=1e-14,
        help="ignore branch-quality diagnostics below this branch probability",
    )
    parser.add_argument(
        "--energy-atol",
        type=float,
        default=1e-9,
        help="absolute tolerance for ground-state degeneracy",
    )
    parser.add_argument(
        "--energy-rtol",
        type=float,
        default=1e-10,
        help="relative tolerance for ground-state degeneracy",
    )
    parser.add_argument(
        "--min-gap",
        type=float,
        default=1e-8,
        help="gap floor for the isolated-ground-state verdict",
    )
    parser.add_argument(
        "--case",
        choices=[case.label for case in DEFAULT_CASES],
        action="append",
        help="case label to run; omit to run the default diagnostic set",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.trials <= 0:
        raise ValueError("--trials must be positive")
    if not (0.0 < args.high_fidelity_threshold <= 1.0):
        raise ValueError("--high-fidelity-threshold must be in (0, 1]")
    if args.probability_floor < 0.0:
        raise ValueError("--probability-floor must be nonnegative")
    if args.energy_atol < 0.0 or args.energy_rtol < 0.0:
        raise ValueError("energy tolerances must be nonnegative")
    if args.min_gap < 0.0:
        raise ValueError("--min-gap must be nonnegative")

    requested = set(args.case or [])
    cases = [case for case in DEFAULT_CASES if not requested or case.label in requested]

    print("POISSON TELEPORTATION PREPARATION/READOUT PROBE")
    print("Status: bounded diagnostic; no dynamic cooling or adiabatic prep simulated")
    print(
        "Extraction context: diagonalize H2 offline, keep last KS taste bit per "
        "species, trace cells/spectator tastes for the deterministic resource"
    )
    sanity = verify_teleportation_convention(args.seed - 1)
    print(
        "Protocol sanity: ideal Phi+ resource "
        f"mean fidelity={sanity['mean']:.16f}, "
        f"min={sanity['min']:.16f}, "
        f"max trace error={sanity['max_trace_error']:.3e}"
    )
    print()

    results = [
        run_probe_case(
            case,
            trials=args.trials,
            seed=args.seed + index,
            high_fidelity_threshold=args.high_fidelity_threshold,
            probability_floor=args.probability_floor,
            energy_atol=args.energy_atol,
            energy_rtol=args.energy_rtol,
        )
        for index, case in enumerate(cases)
    ]
    for result in results:
        print_result(
            result,
            high_fidelity_threshold=args.high_fidelity_threshold,
            min_gap=args.min_gap,
        )

    positives = [
        result
        for result in results
        if result.case.G != 0.0
        and result.traced_resource.bell_fidelity >= args.high_fidelity_threshold
    ]
    print("Conclusion:")
    if positives:
        labels = ", ".join(result.case.label for result in positives)
        print(f"  Offline traced-resource positives on Poisson cases: {labels}.")
    else:
        print("  No Poisson case passed the offline traced-resource threshold.")
    print(
        "  Preparation/readout remains unproven: this probe does not construct a "
        "cooling schedule, adiabatic path, encoded Bell measurement, physical "
        "environment readout, or deterministic branch selection."
    )
    print(
        "  Fixed-env branches are useful diagnostics only unless their projection "
        "measurement, heralding cost, and post-measurement logical operations are "
        "specified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
