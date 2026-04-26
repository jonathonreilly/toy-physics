#!/usr/bin/env python3
"""Bounded Poisson-resource sweep for encoded teleportation.

Status: planning / first artifact. This runner hardens the narrow positive
result from `frontier_teleportation_resource_from_poisson.py` across a small,
runtime-reasonable parameter grid.

It audits only ordinary quantum state teleportation on the extracted encoded
two-qubit taste resource. It does not claim matter teleportation, mass
transport, charge transport, energy transport, or faster-than-light signaling.
"""

from __future__ import annotations

import argparse
import dataclasses
import sys
from collections import defaultdict
from pathlib import Path
from typing import Callable, Iterable

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_teleportation_resource_from_poisson import (  # noqa: E402
    AuditCase,
    amplitudes_by_logical_env,
    bell_state,
    best_bell_overlap,
    factor_sites,
    ground_state_resource,
    negativity,
    postselected_branch_scan,
    reduced_logical_resource,
    standard_teleportation_stats,
    two_qubit_chsh,
    verify_teleportation_convention,
)


CLASSICAL_AVG_FIDELITY = 2.0 / 3.0
DEFAULT_MASSES = (0.0, 0.1, 0.5, 1.0)
DEFAULT_G_VALUES = (0.0, 1.0, 10.0, 50.0, 100.0, 500.0, 1000.0)
DEFAULT_SURFACES = (
    ("1d_N8", 1, 8),
    ("2d_4x4", 2, 4),
)


@dataclasses.dataclass(frozen=True)
class SweepResult:
    surface: str
    dim: int
    side: int
    mass: float
    G: float
    n_sites: int
    n_env: int
    ground_energy: float
    full_chsh: float
    phi_plus_overlap: float
    best_bell_overlap: float
    best_bell_label: str
    exact_avg_fidelity: float
    sampled_mean_fidelity: float
    sampled_min_fidelity: float
    sampled_max_fidelity: float
    max_trace_error: float
    logical_chsh: float
    purity: float
    negativity: float
    post_bell_overlap: float
    post_bell_label: str
    post_probability: float
    post_logical_chsh: float
    post_negativity: float

    @property
    def is_null(self) -> bool:
        return abs(self.G) <= 1e-15


def parse_csv_floats(raw: str) -> tuple[float, ...]:
    values: list[float] = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        values.append(float(item))
    if not values:
        raise argparse.ArgumentTypeError("expected at least one numeric value")
    return tuple(values)


def selected_surfaces(names: Iterable[str] | None) -> tuple[tuple[str, int, int], ...]:
    requested = set(names or [])
    surfaces = tuple(
        surface for surface in DEFAULT_SURFACES if not requested or surface[0] in requested
    )
    if not surfaces:
        raise ValueError(f"no matching surfaces for {sorted(requested)}")
    return surfaces


def bell_overlap(rho: np.ndarray, z_bit: int, x_bit: int) -> float:
    bell = bell_state(z_bit, x_bit)
    return float(np.real(np.vdot(bell, rho @ bell)))


def fixed_protocol_avg_fidelity(phi_plus_overlap: float) -> float:
    """Exact average fidelity for the fixed Bell-basis Phi+ convention."""
    return float((1.0 + 2.0 * phi_plus_overlap) / 3.0)


def evaluate_case(
    surface: str,
    dim: int,
    side: int,
    mass: float,
    G: float,
    trials: int,
    seed: int,
    probability_floor: float,
) -> SweepResult:
    case = AuditCase(
        label=f"{surface}_m{mass:g}_G{G:g}",
        dim=dim,
        side=side,
        mass=mass,
        G=G,
    )
    resource = ground_state_resource(case)
    n_sites = int(resource["n"])
    factors = factor_sites(dim, side)
    amp = amplitudes_by_logical_env(resource["psi"], n_sites, factors)
    rho = reduced_logical_resource(amp)

    best_overlap, best_label = best_bell_overlap(rho)
    phi_plus = bell_overlap(rho, 0, 0)
    sampled = standard_teleportation_stats(rho, trials=trials, seed=seed)
    post = postselected_branch_scan(
        amp,
        factors.env_labels,
        probability_floor=probability_floor,
    )

    return SweepResult(
        surface=surface,
        dim=dim,
        side=side,
        mass=mass,
        G=G,
        n_sites=n_sites,
        n_env=len(factors.env_labels),
        ground_energy=float(resource["ground_energy"]),
        full_chsh=float(resource["full_chsh"]),
        phi_plus_overlap=phi_plus,
        best_bell_overlap=best_overlap,
        best_bell_label=best_label,
        exact_avg_fidelity=fixed_protocol_avg_fidelity(phi_plus),
        sampled_mean_fidelity=float(sampled["mean"]),
        sampled_min_fidelity=float(sampled["min"]),
        sampled_max_fidelity=float(sampled["max"]),
        max_trace_error=float(sampled["max_trace_error"]),
        logical_chsh=two_qubit_chsh(rho),
        purity=float(np.real(np.trace(rho @ rho))),
        negativity=negativity(rho),
        post_bell_overlap=float(post["bell_fidelity"]),
        post_bell_label=str(post["bell_label"]),
        post_probability=float(post["probability"]),
        post_logical_chsh=float(post["logical_chsh"]),
        post_negativity=float(post["negativity"]),
    )


def run_sweep(args: argparse.Namespace) -> list[SweepResult]:
    masses = args.masses
    G_values = args.G_values
    surfaces = selected_surfaces(args.surface)

    results: list[SweepResult] = []
    case_index = 0
    for surface, dim, side in surfaces:
        for mass in masses:
            for G in G_values:
                results.append(
                    evaluate_case(
                        surface=surface,
                        dim=dim,
                        side=side,
                        mass=mass,
                        G=G,
                        trials=args.trials,
                        seed=args.seed + case_index,
                        probability_floor=args.probability_floor,
                    )
                )
                case_index += 1
    return results


def passes_high_resource(result: SweepResult, args: argparse.Namespace) -> bool:
    return (
        result.best_bell_label == "Phi+"
        and result.best_bell_overlap >= args.bell_threshold
        and result.exact_avg_fidelity >= args.teleport_threshold
        and result.negativity > args.negativity_threshold
    )


def has_chsh_violation(value: float, args: argparse.Namespace) -> bool:
    return value > 2.0 + args.chsh_margin


def first_g(
    rows: Iterable[SweepResult],
    predicate: Callable[[SweepResult], bool],
) -> str:
    passing = sorted(row.G for row in rows if predicate(row))
    if not passing:
        return "none"
    return f"{passing[0]:g}"


def print_case_table(results: list[SweepResult], args: argparse.Namespace) -> None:
    print("Case rows:")
    print(
        "  "
        f"{'surface':7s} {'m':>5s} {'G':>7s} {'S_full':>8s} "
        f"{'Bell*':>8s} {'label':>5s} {'pPhi+':>8s} {'F_avg':>8s} "
        f"{'S_log':>8s} {'neg':>8s} {'post*':>8s} {'post_p':>10s} {'pass':>5s}"
    )
    for row in results:
        mark = "yes" if passes_high_resource(row, args) else ""
        print(
            "  "
            f"{row.surface:7s} "
            f"{row.mass:5.2f} "
            f"{row.G:7.1f} "
            f"{row.full_chsh:8.5f} "
            f"{row.best_bell_overlap:8.5f} "
            f"{row.best_bell_label:>5s} "
            f"{row.phi_plus_overlap:8.5f} "
            f"{row.exact_avg_fidelity:8.5f} "
            f"{row.logical_chsh:8.5f} "
            f"{row.negativity:8.5f} "
            f"{row.post_bell_overlap:8.5f} "
            f"{row.post_probability:10.3e} "
            f"{mark:>5s}"
        )
    print()


def grouped_by_surface_mass(results: Iterable[SweepResult]) -> dict[tuple[str, float], list[SweepResult]]:
    grouped: dict[tuple[str, float], list[SweepResult]] = defaultdict(list)
    for row in results:
        grouped[(row.surface, row.mass)].append(row)
    return dict(grouped)


def print_threshold_summary(results: list[SweepResult], args: argparse.Namespace) -> None:
    grouped = grouped_by_surface_mass(results)

    print("Threshold summary by surface and mass:")
    print(
        "  "
        f"{'surface':7s} {'m':>5s} {'Bell*>=thr':>11s} {'Favg>=thr':>10s} "
        f"{'Favg>2/3':>9s} {'Sfull>2':>8s} {'Slog>2':>7s} {'neg>0':>6s} "
        f"{'high pass':>9s}"
    )
    for key in sorted(grouped):
        rows = sorted(grouped[key], key=lambda item: item.G)
        surface, mass = key
        print(
            "  "
            f"{surface:7s} "
            f"{mass:5.2f} "
            f"{first_g(rows, lambda row: row.best_bell_overlap >= args.bell_threshold):>11s} "
            f"{first_g(rows, lambda row: row.exact_avg_fidelity >= args.teleport_threshold):>10s} "
            f"{first_g(rows, lambda row: row.exact_avg_fidelity > CLASSICAL_AVG_FIDELITY + 1e-10):>9s} "
            f"{first_g(rows, lambda row: has_chsh_violation(row.full_chsh, args)):>8s} "
            f"{first_g(rows, lambda row: has_chsh_violation(row.logical_chsh, args)):>7s} "
            f"{first_g(rows, lambda row: row.negativity > args.negativity_threshold):>6s} "
            f"{first_g(rows, lambda row: passes_high_resource(row, args)):>9s}"
        )
    print()


def print_null_summary(results: list[SweepResult], args: argparse.Namespace) -> bool:
    nulls = [row for row in results if row.is_null]
    if not nulls:
        print("Null controls: no G=0 rows were included.")
        return False

    max_full = max(row.full_chsh for row in nulls)
    max_logical = max(row.logical_chsh for row in nulls)
    max_bell = max(row.best_bell_overlap for row in nulls)
    max_fidelity = max(row.exact_avg_fidelity for row in nulls)
    max_negativity = max(row.negativity for row in nulls)
    high_passes = sum(passes_high_resource(row, args) for row in nulls)
    chsh_hits = sum(has_chsh_violation(row.full_chsh, args) for row in nulls)
    neg_hits = sum(row.negativity > args.negativity_threshold for row in nulls)
    clean = high_passes == 0 and chsh_hits == 0 and neg_hits == 0

    print("Null controls (G=0):")
    print(f"  rows: {len(nulls)}")
    print(f"  max full-state CHSH: {max_full:.6f}")
    print(f"  max logical CHSH: {max_logical:.6f}")
    print(f"  max best Bell overlap: {max_bell:.6f}")
    print(f"  max exact fixed-protocol F_avg: {max_fidelity:.6f}")
    print(f"  max negativity: {max_negativity:.6e}")
    print(f"  high-resource passes: {high_passes}")
    print(f"  CHSH violations above margin: {chsh_hits}")
    print(f"  negativity hits above threshold: {neg_hits}")
    print(f"  null-control status: {'clean' if clean else 'failed'}")
    print()
    return clean


def print_global_summary(results: list[SweepResult], args: argparse.Namespace, nulls_clean: bool) -> None:
    non_null = [row for row in results if not row.is_null]
    high_rows = [row for row in non_null if passes_high_resource(row, args)]
    full_chsh_rows = [row for row in non_null if has_chsh_violation(row.full_chsh, args)]
    logical_chsh_rows = [row for row in non_null if has_chsh_violation(row.logical_chsh, args)]
    entangled_rows = [row for row in non_null if row.negativity > args.negativity_threshold]
    quantum_useful_rows = [
        row
        for row in non_null
        if row.exact_avg_fidelity > CLASSICAL_AVG_FIDELITY + 1e-10
    ]

    best_bell = max(non_null, key=lambda row: row.best_bell_overlap)
    best_fidelity = max(non_null, key=lambda row: row.exact_avg_fidelity)
    best_full_chsh = max(non_null, key=lambda row: row.full_chsh)
    best_logical_chsh = max(non_null, key=lambda row: row.logical_chsh)
    best_negativity = max(non_null, key=lambda row: row.negativity)
    worst_high = min(high_rows, key=lambda row: row.exact_avg_fidelity) if high_rows else None

    print("Global non-null summary:")
    print(f"  non-null rows: {len(non_null)}")
    print(
        "  high-resource passes "
        f"(Phi+ best, Bell*>={args.bell_threshold:.3f}, "
        f"F_avg>={args.teleport_threshold:.3f}, neg>{args.negativity_threshold:g}): "
        f"{len(high_rows)}/{len(non_null)}"
    )
    print(
        "  exact fixed-protocol F_avg above classical 2/3: "
        f"{len(quantum_useful_rows)}/{len(non_null)}"
    )
    print(f"  full-state CHSH violations: {len(full_chsh_rows)}/{len(non_null)}")
    print(f"  logical-resource CHSH violations: {len(logical_chsh_rows)}/{len(non_null)}")
    print(f"  negativity-positive rows: {len(entangled_rows)}/{len(non_null)}")
    print(
        "  best Bell*: "
        f"{best_bell.best_bell_overlap:.6f} at {best_bell.surface} "
        f"m={best_bell.mass:g}, G={best_bell.G:g} ({best_bell.best_bell_label})"
    )
    print(
        "  best fixed F_avg: "
        f"{best_fidelity.exact_avg_fidelity:.6f} at {best_fidelity.surface} "
        f"m={best_fidelity.mass:g}, G={best_fidelity.G:g}"
    )
    print(
        "  best full CHSH: "
        f"{best_full_chsh.full_chsh:.6f} at {best_full_chsh.surface} "
        f"m={best_full_chsh.mass:g}, G={best_full_chsh.G:g}"
    )
    print(
        "  best logical CHSH: "
        f"{best_logical_chsh.logical_chsh:.6f} at {best_logical_chsh.surface} "
        f"m={best_logical_chsh.mass:g}, G={best_logical_chsh.G:g}"
    )
    print(
        "  best negativity: "
        f"{best_negativity.negativity:.6f} at {best_negativity.surface} "
        f"m={best_negativity.mass:g}, G={best_negativity.G:g}"
    )
    if worst_high is not None:
        print(
            "  weakest high-resource pass by F_avg: "
            f"{worst_high.exact_avg_fidelity:.6f} at {worst_high.surface} "
            f"m={worst_high.mass:g}, G={worst_high.G:g}"
        )
    print()

    survives_as_window = bool(high_rows) and nulls_clean
    uniform = len(high_rows) == len(non_null) if non_null else False
    print("Conclusion:")
    print(
        "  Positive Poisson-resource result survives bounded sweep as a "
        f"parameter-window result: {'YES' if survives_as_window else 'NO'}"
    )
    print(f"  Positive across every non-null sweep point: {'YES' if uniform else 'NO'}")
    print(
        "  Claim boundary: planning/first artifact; quantum state teleportation "
        "resource only. Postselected branches remain diagnostic only."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--masses",
        type=parse_csv_floats,
        default=DEFAULT_MASSES,
        help="comma-separated mass values",
    )
    parser.add_argument(
        "--G-values",
        dest="G_values",
        type=parse_csv_floats,
        default=DEFAULT_G_VALUES,
        help="comma-separated Poisson coupling values",
    )
    parser.add_argument(
        "--surface",
        choices=[surface[0] for surface in DEFAULT_SURFACES],
        action="append",
        help="surface to include; omit for all defaults",
    )
    parser.add_argument("--trials", type=int, default=64, help="sampled teleportation probes per case")
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument("--bell-threshold", type=float, default=0.90)
    parser.add_argument("--teleport-threshold", type=float, default=0.90)
    parser.add_argument(
        "--chsh-margin",
        type=float,
        default=1e-3,
        help="count CHSH only when S > 2 + margin",
    )
    parser.add_argument("--negativity-threshold", type=float, default=1e-10)
    parser.add_argument("--probability-floor", type=float, default=1e-12)
    parser.add_argument(
        "--no-case-table",
        action="store_true",
        help="suppress the per-case sweep table",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.trials <= 0:
        raise ValueError("--trials must be positive")
    if not (0.0 < args.bell_threshold <= 1.0):
        raise ValueError("--bell-threshold must be in (0, 1]")
    if not (0.0 < args.teleport_threshold <= 1.0):
        raise ValueError("--teleport-threshold must be in (0, 1]")
    if args.chsh_margin < 0.0:
        raise ValueError("--chsh-margin must be nonnegative")
    if args.negativity_threshold < 0.0:
        raise ValueError("--negativity-threshold must be nonnegative")
    if args.probability_floor < 0.0:
        raise ValueError("--probability-floor must be nonnegative")


def main() -> int:
    args = parse_args()
    validate_args(args)

    print("POISSON TELEPORTATION RESOURCE BOUNDED SWEEP")
    print("Status: planning / first artifact; quantum state teleportation only")
    print(
        "Grid: "
        f"surfaces={[surface[0] for surface in selected_surfaces(args.surface)]}, "
        f"masses={[f'{mass:g}' for mass in args.masses]}, "
        f"G={[f'{value:g}' for value in args.G_values]}"
    )
    print(
        "Thresholds: "
        f"Bell*>={args.bell_threshold:.3f}, "
        f"fixed F_avg>={args.teleport_threshold:.3f}, "
        f"CHSH>2+{args.chsh_margin:g}, "
        f"neg>{args.negativity_threshold:g}"
    )
    sanity = verify_teleportation_convention(args.seed - 1)
    print(
        "Protocol sanity: ideal Phi+ sampled mean fidelity="
        f"{sanity['mean']:.16f}, min={sanity['min']:.16f}, "
        f"max trace error={sanity['max_trace_error']:.3e}"
    )
    print()

    results = run_sweep(args)
    if not args.no_case_table:
        print_case_table(results, args)
    print_threshold_summary(results, args)
    nulls_clean = print_null_summary(results, args)
    print_global_summary(results, args, nulls_clean)
    return 0


if __name__ == "__main__":
    sys.exit(main())
