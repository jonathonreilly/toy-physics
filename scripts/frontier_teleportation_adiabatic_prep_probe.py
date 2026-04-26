#!/usr/bin/env python3
"""Adiabatic/gap preparation probe for the Poisson teleportation resource.

Status: planning / first artifact. This is a bounded diagnostic for ordinary
quantum state teleportation resources only. It does not claim matter transfer,
mass transfer, charge transfer, energy transfer, or faster-than-light transport.

The probe asks whether a simple native coupling ramp,

    H(s) = H_uncoupled + s * (H_poisson_target - H_uncoupled),  s in [0, 1],

has a finite sampled gap and reasonable adiabatic-condition diagnostics while
ending at the Poisson-derived encoded Bell resource from the previous
teleportation artifacts. It is not a time-evolution simulation and not a
preparation proof.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import eigh, norm


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_bell_inequality import build_H1, build_H2_tensor, build_poisson  # noqa: E402
from frontier_teleportation_resource_from_poisson import (  # noqa: E402
    AuditCase,
    amplitudes_by_logical_env,
    bell_state,
    best_bell_overlap,
    factor_sites,
    lattice_for_case,
    negativity,
    reduced_logical_resource,
    two_qubit_chsh,
)


DEFAULT_CASES = (
    AuditCase("1d_null", dim=1, side=8, mass=0.0, G=0.0),
    AuditCase("1d_poisson_chsh", dim=1, side=8, mass=0.0, G=1000.0),
    AuditCase("2d_null", dim=2, side=4, mass=0.0, G=0.0),
    AuditCase("2d_poisson_chsh", dim=2, side=4, mass=0.0, G=1000.0),
)


@dataclasses.dataclass(frozen=True)
class StepDiagnostics:
    s: float
    ground_energy: float
    gap: float
    target_ground_overlap: float
    phi_plus_overlap: float
    best_bell_overlap: float
    best_bell_label: str
    logical_chsh: float
    negativity: float
    first_excited_adiabatic: float
    max_excited_adiabatic: float
    rss_adiabatic: float
    norm_bound_adiabatic: float
    dominant_level: int
    dominant_gap: float
    dominant_coupling: float


@dataclasses.dataclass(frozen=True)
class PathResult:
    case: AuditCase
    n_sites: int
    n_env: int
    h_derivative_norm: float
    steps: tuple[StepDiagnostics, ...]

    @property
    def is_null(self) -> bool:
        return abs(self.case.G) <= 1e-15

    @property
    def final_step(self) -> StepDiagnostics:
        return self.steps[-1]

    @property
    def min_gap_step(self) -> StepDiagnostics:
        return min(self.steps, key=lambda row: row.gap)

    @property
    def max_exact_step(self) -> StepDiagnostics:
        return max(self.steps, key=lambda row: row.max_excited_adiabatic)

    @property
    def max_rss_step(self) -> StepDiagnostics:
        return max(self.steps, key=lambda row: row.rss_adiabatic)

    @property
    def max_norm_bound_step(self) -> StepDiagnostics:
        return max(self.steps, key=lambda row: row.norm_bound_adiabatic)


def phi_plus_overlap(rho: np.ndarray) -> float:
    phi_plus = bell_state(0, 0)
    return float(np.real(np.vdot(phi_plus, rho @ phi_plus)))


def path_grid(points: int) -> np.ndarray:
    if points < 2:
        raise ValueError("--grid-points must be at least 2")
    return np.linspace(0.0, 1.0, points)


def build_endpoint_hamiltonians(case: AuditCase) -> tuple[int, np.ndarray, np.ndarray]:
    n_sites, adj, parity, _coords = lattice_for_case(case)
    h1 = build_H1(n_sites, adj, parity, mass=case.mass)
    poisson = build_poisson(n_sites, adj)
    h_uncoupled = build_H2_tensor(h1, poisson, 0.0, n_sites)
    h_target = build_H2_tensor(h1, poisson, case.G, n_sites)
    return n_sites, h_uncoupled, h_target


def finite_ratio(numerator: float, denominator: float, gap_floor: float) -> float:
    if denominator <= gap_floor:
        return math.inf
    return numerator / (denominator * denominator)


def logical_resource_at_state(
    psi: np.ndarray,
    n_sites: int,
    factors,
) -> tuple[float, float, str, float, float]:
    amp = amplitudes_by_logical_env(psi, n_sites, factors)
    rho = reduced_logical_resource(amp)
    best_overlap, best_label = best_bell_overlap(rho)
    return (
        phi_plus_overlap(rho),
        best_overlap,
        best_label,
        two_qubit_chsh(rho),
        negativity(rho),
    )


def step_diagnostics(
    s: float,
    hamiltonian: np.ndarray,
    d_hamiltonian: np.ndarray,
    h_derivative_norm: float,
    target_ground_state: np.ndarray,
    n_sites: int,
    factors,
    gap_floor: float,
) -> StepDiagnostics:
    evals, evecs = eigh(hamiltonian)
    ground = evecs[:, 0]
    gaps = evals[1:] - evals[0]
    gap = float(gaps[0]) if len(gaps) else math.inf

    d_ground = d_hamiltonian @ ground
    couplings = np.abs(evecs[:, 1:].conj().T @ d_ground)
    ratios = np.array(
        [
            finite_ratio(float(coupling), float(excited_gap), gap_floor)
            for coupling, excited_gap in zip(couplings, gaps)
        ],
        dtype=float,
    )
    if len(ratios):
        dominant_offset = int(np.argmax(ratios))
        dominant_level = dominant_offset + 1
        max_excited_adiabatic = float(ratios[dominant_offset])
        dominant_gap = float(gaps[dominant_offset])
        dominant_coupling = float(couplings[dominant_offset])
        first_excited = float(ratios[0])
        finite_values = ratios[np.isfinite(ratios)]
        rss_adiabatic = (
            math.inf
            if len(finite_values) != len(ratios)
            else float(np.sqrt(np.sum(ratios * ratios)))
        )
    else:
        dominant_level = 0
        max_excited_adiabatic = 0.0
        dominant_gap = math.inf
        dominant_coupling = 0.0
        first_excited = 0.0
        rss_adiabatic = 0.0

    target_overlap = float(abs(np.vdot(target_ground_state, ground)) ** 2)
    phi_overlap, best_overlap, best_label, logical_chsh, neg = logical_resource_at_state(
        ground,
        n_sites,
        factors,
    )

    return StepDiagnostics(
        s=float(s),
        ground_energy=float(evals[0]),
        gap=gap,
        target_ground_overlap=target_overlap,
        phi_plus_overlap=phi_overlap,
        best_bell_overlap=best_overlap,
        best_bell_label=best_label,
        logical_chsh=logical_chsh,
        negativity=neg,
        first_excited_adiabatic=first_excited,
        max_excited_adiabatic=max_excited_adiabatic,
        rss_adiabatic=rss_adiabatic,
        norm_bound_adiabatic=finite_ratio(h_derivative_norm, gap, gap_floor),
        dominant_level=dominant_level,
        dominant_gap=dominant_gap,
        dominant_coupling=dominant_coupling,
    )


def run_case(case: AuditCase, grid_points: int, gap_floor: float) -> PathResult:
    n_sites, h_initial, h_target = build_endpoint_hamiltonians(case)
    d_hamiltonian = h_target - h_initial
    h_derivative_norm = float(norm(d_hamiltonian, 2))

    target_evals, target_evecs = eigh(h_target)
    target_ground = target_evecs[:, 0]
    factors = factor_sites(case.dim, case.side)

    steps = []
    for s in path_grid(grid_points):
        hamiltonian = h_initial + float(s) * d_hamiltonian
        steps.append(
            step_diagnostics(
                s=float(s),
                hamiltonian=hamiltonian,
                d_hamiltonian=d_hamiltonian,
                h_derivative_norm=h_derivative_norm,
                target_ground_state=target_ground,
                n_sites=n_sites,
                factors=factors,
                gap_floor=gap_floor,
            )
        )

    return PathResult(
        case=case,
        n_sites=n_sites,
        n_env=len(factors.env_labels),
        h_derivative_norm=h_derivative_norm,
        steps=tuple(steps),
    )


def selected_cases(names: list[str] | None) -> tuple[AuditCase, ...]:
    requested = set(names or [])
    cases = tuple(case for case in DEFAULT_CASES if not requested or case.label in requested)
    if not cases:
        raise ValueError(f"no matching cases for {sorted(requested)}")
    return cases


def sample_rows(steps: tuple[StepDiagnostics, ...]) -> tuple[StepDiagnostics, ...]:
    requested = (0.0, 0.25, 0.5, 0.75, 1.0)
    selected: list[StepDiagnostics] = []
    used_indices: set[int] = set()
    for value in requested:
        index = min(range(len(steps)), key=lambda item: abs(steps[item].s - value))
        if index not in used_indices:
            selected.append(steps[index])
            used_indices.add(index)
    return tuple(selected)


def fmt_float(value: float) -> str:
    if math.isinf(value):
        return "inf"
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e4:
        return f"{value:.6e}"
    return f"{value:.6f}"


def print_step_table(result: PathResult) -> None:
    print("  sampled path rows:")
    print(
        "    "
        f"{'s':>6s} {'gap':>12s} {'target|ov|2':>12s} {'Phi+':>10s} "
        f"{'Bell*':>10s} {'label':>5s} {'Amax':>12s} {'Arss':>12s} {'norm/gap2':>12s}"
    )
    for row in sample_rows(result.steps):
        print(
            "    "
            f"{row.s:6.3f} "
            f"{fmt_float(row.gap):>12s} "
            f"{fmt_float(row.target_ground_overlap):>12s} "
            f"{fmt_float(row.phi_plus_overlap):>10s} "
            f"{fmt_float(row.best_bell_overlap):>10s} "
            f"{row.best_bell_label:>5s} "
            f"{fmt_float(row.max_excited_adiabatic):>12s} "
            f"{fmt_float(row.rss_adiabatic):>12s} "
            f"{fmt_float(row.norm_bound_adiabatic):>12s}"
        )


def null_control_clean(result: PathResult, resource_threshold: float) -> bool:
    final = result.final_step
    return (
        result.is_null
        and result.h_derivative_norm <= 1e-12
        and final.best_bell_overlap < resource_threshold
        and final.negativity <= 1e-10
    )


def exact_path_plausible(
    result: PathResult,
    resource_threshold: float,
    min_gap_threshold: float,
    exact_adiabatic_threshold: float,
) -> bool:
    final = result.final_step
    return (
        not result.is_null
        and final.phi_plus_overlap >= resource_threshold
        and result.min_gap_step.gap >= min_gap_threshold
        and result.max_exact_step.max_excited_adiabatic <= exact_adiabatic_threshold
    )


def print_result(
    result: PathResult,
    resource_threshold: float,
    min_gap_threshold: float,
    exact_adiabatic_threshold: float,
    norm_bound_threshold: float,
) -> None:
    case = result.case
    final = result.final_step
    min_gap = result.min_gap_step
    max_exact = result.max_exact_step
    max_rss = result.max_rss_step
    max_norm = result.max_norm_bound_step

    print(f"Case: {case.label}")
    print(
        "  lattice/params: "
        f"dim={case.dim} side={case.side} N={result.n_sites} "
        f"envs/logical_qubit={result.n_env} mass={case.mass:g} "
        f"G_target={case.G:g}"
    )
    print(
        "  path: H(s)=H(G=0)+s*(H(G_target)-H(G=0)); "
        f"||dH/ds||_2={fmt_float(result.h_derivative_norm)}"
    )
    print_step_table(result)
    print(
        "  path summary: "
        f"min gap={fmt_float(min_gap.gap)} at s={min_gap.s:.3f}; "
        f"final gap={fmt_float(final.gap)}; "
        f"initial target-ground overlap={fmt_float(result.steps[0].target_ground_overlap)}; "
        f"final target-ground overlap={fmt_float(final.target_ground_overlap)}"
    )
    print(
        "  final resource: "
        f"Phi+ overlap={final.phi_plus_overlap:.6f}, "
        f"best Bell={final.best_bell_overlap:.6f} ({final.best_bell_label}), "
        f"logical CHSH={final.logical_chsh:.6f}, negativity={final.negativity:.6f}"
    )
    print(
        "  adiabatic diagnostic: "
        f"max_k |<k|dH/ds|0>|/gap_k^2={fmt_float(max_exact.max_excited_adiabatic)} "
        f"at s={max_exact.s:.3f}, level={max_exact.dominant_level}, "
        f"level_gap={fmt_float(max_exact.dominant_gap)}, "
        f"coupling={fmt_float(max_exact.dominant_coupling)}"
    )
    print(
        "    "
        f"max RSS exact diagnostic={fmt_float(max_rss.rss_adiabatic)} "
        f"at s={max_rss.s:.3f}; "
        f"max conservative ||dH||/gap_1^2={fmt_float(max_norm.norm_bound_adiabatic)} "
        f"at s={max_norm.s:.3f}"
    )

    if result.is_null:
        print(
            "  verdict: "
            f"null/control path clean: {'YES' if null_control_clean(result, resource_threshold) else 'NO'}"
        )
    else:
        exact_ok = exact_path_plausible(
            result,
            resource_threshold=resource_threshold,
            min_gap_threshold=min_gap_threshold,
            exact_adiabatic_threshold=exact_adiabatic_threshold,
        )
        robust_ok = max_norm.norm_bound_adiabatic <= norm_bound_threshold
        print("  verdict:")
        print(
            f"    high Phi+ endpoint (>= {resource_threshold:.3f}): "
            f"{'YES' if final.phi_plus_overlap >= resource_threshold else 'NO'}"
        )
        print(
            f"    sampled gap floor (>= {min_gap_threshold:g}): "
            f"{'YES' if min_gap.gap >= min_gap_threshold else 'NO'}"
        )
        print(
            f"    clean-path exact adiabatic diagnostic (<= {exact_adiabatic_threshold:g}): "
            f"{'YES' if max_exact.max_excited_adiabatic <= exact_adiabatic_threshold else 'NO'}"
        )
        print(
            f"    conservative norm-bound diagnostic (<= {norm_bound_threshold:g}): "
            f"{'YES' if robust_ok else 'NO'}"
        )
        print(
            "    preparation proof demonstrated: NO "
            f"({'plausible diagnostic path' if exact_ok else 'diagnostic no-go under current thresholds'})"
        )
    print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--grid-points",
        type=int,
        default=41,
        help="number of uniformly spaced s values in [0, 1]",
    )
    parser.add_argument(
        "--case",
        choices=[case.label for case in DEFAULT_CASES],
        action="append",
        help="case label to run; omit to run all default 1D/2D cases",
    )
    parser.add_argument(
        "--resource-threshold",
        type=float,
        default=0.90,
        help="Phi+ overlap threshold for a high-resource endpoint",
    )
    parser.add_argument(
        "--min-gap-threshold",
        type=float,
        default=1e-3,
        help="minimum sampled spectral gap for the path verdict",
    )
    parser.add_argument(
        "--exact-adiabatic-threshold",
        type=float,
        default=1e3,
        help="threshold for max exact eigenbasis adiabatic diagnostic",
    )
    parser.add_argument(
        "--norm-bound-threshold",
        type=float,
        default=1e5,
        help="threshold for conservative ||dH||/gap_1^2 warning",
    )
    parser.add_argument(
        "--gap-floor",
        type=float,
        default=1e-12,
        help="gap floor below which adiabatic ratios are reported as infinite",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.grid_points < 2:
        raise ValueError("--grid-points must be at least 2")
    if not (0.0 < args.resource_threshold <= 1.0):
        raise ValueError("--resource-threshold must be in (0, 1]")
    if args.min_gap_threshold < 0.0:
        raise ValueError("--min-gap-threshold must be nonnegative")
    if args.exact_adiabatic_threshold < 0.0:
        raise ValueError("--exact-adiabatic-threshold must be nonnegative")
    if args.norm_bound_threshold < 0.0:
        raise ValueError("--norm-bound-threshold must be nonnegative")
    if args.gap_floor < 0.0:
        raise ValueError("--gap-floor must be nonnegative")


def main() -> int:
    args = parse_args()
    validate_args(args)
    cases = selected_cases(args.case)

    print("POISSON TELEPORTATION ADIABATIC PREP PROBE")
    print("Status: planning / first artifact; quantum state teleportation resource only")
    print(
        "Claim boundary: no matter, mass, charge, energy, or faster-than-light "
        "transport; no preparation proof from this diagnostic"
    )
    print(
        "Path family: native uncoupled two-species Hamiltonian at G=0 ramped "
        "linearly in s to the Poisson target"
    )
    print(
        "Diagnostics: sampled spectral gap, target-ground overlap, Phi+ resource "
        "overlap, exact eigenbasis adiabatic ratio, and conservative norm bound"
    )
    print(
        "Grid/thresholds: "
        f"grid_points={args.grid_points}, "
        f"resource>={args.resource_threshold:.3f}, "
        f"min_gap>={args.min_gap_threshold:g}, "
        f"exact_A<={args.exact_adiabatic_threshold:g}, "
        f"norm_bound<={args.norm_bound_threshold:g}"
    )
    print()

    results = [
        run_case(case, grid_points=args.grid_points, gap_floor=args.gap_floor)
        for case in cases
    ]
    for result in results:
        print_result(
            result,
            resource_threshold=args.resource_threshold,
            min_gap_threshold=args.min_gap_threshold,
            exact_adiabatic_threshold=args.exact_adiabatic_threshold,
            norm_bound_threshold=args.norm_bound_threshold,
        )

    null_results = [result for result in results if result.is_null]
    poisson_results = [result for result in results if not result.is_null]
    clean_nulls = [result for result in null_results if null_control_clean(result, args.resource_threshold)]
    plausible = [
        result
        for result in poisson_results
        if exact_path_plausible(
            result,
            resource_threshold=args.resource_threshold,
            min_gap_threshold=args.min_gap_threshold,
            exact_adiabatic_threshold=args.exact_adiabatic_threshold,
        )
    ]
    robust = [
        result
        for result in plausible
        if result.max_norm_bound_step.norm_bound_adiabatic <= args.norm_bound_threshold
    ]

    print("Conclusion:")
    print(f"  null/control paths clean: {len(clean_nulls)}/{len(null_results)}")
    print(
        "  Poisson paths with high endpoint resource, finite sampled gap, and "
        f"exact diagnostic within threshold: {len(plausible)}/{len(poisson_results)}"
    )
    if plausible:
        labels = ", ".join(result.case.label for result in plausible)
        print(f"  clean-path plausible diagnostics: {labels}")
    else:
        print("  clean-path plausible diagnostics: none")
    if robust:
        labels = ", ".join(result.case.label for result in robust)
        print(f"  also below conservative norm-bound threshold: {labels}")
    else:
        print("  also below conservative norm-bound threshold: none")
    print(
        "  Interpretation: this is a bounded adiabatic/gap planning artifact. "
        "Finite sampled gaps and favorable endpoint overlaps make the path worth "
        "probing further, but they do not prove preparation without a schedule, "
        "runtime/error bound, control-noise model, and encoded readout operations."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
