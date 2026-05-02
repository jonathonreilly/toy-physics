#!/usr/bin/env python3
"""Initial-state preparation audit for the Poisson teleportation ramp.

Status: planning / first artifact. This bounded diagnostic audits the
assumption used by the finite-time adiabatic ramp: the two-species ground
state of the native G=0 Hamiltonian is already available.

Scope boundary: ordinary quantum state teleportation resources only. This
does not claim matter transfer, mass transfer, charge transfer, energy
transfer, object transport, or faster-than-light signaling.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import eigh


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_bell_inequality import build_H1, build_H2_tensor, build_poisson  # noqa: E402
from frontier_teleportation_resource_from_poisson import (  # noqa: E402
    AuditCase,
    amplitudes_by_logical_env,
    best_bell_overlap,
    factor_sites,
    lattice_for_case,
    negativity,
    reduced_logical_resource,
    two_qubit_chsh,
)


DEFAULT_CASES = (
    AuditCase("1d_null_initial", dim=1, side=8, mass=0.0, G=0.0),
    AuditCase("2d_null_initial", dim=2, side=4, mass=0.0, G=0.0),
)


@dataclasses.dataclass(frozen=True)
class SpectrumDiagnostics:
    ground_energy: float
    first_excited_energy: float
    degeneracy: int
    gap_after_ground_space: float
    min_gap_unique: float


@dataclasses.dataclass(frozen=True)
class BipartitionDiagnostics:
    label: str
    entropy_bits: float
    purity: float
    max_schmidt_weight: float
    effective_rank: float
    numerical_rank: int


@dataclasses.dataclass(frozen=True)
class SupportDiagnostics:
    label: str
    dimension: int
    support_count: int
    participation_ratio: float
    participation_fraction: float
    max_probability: float
    shannon_bits: float


@dataclasses.dataclass(frozen=True)
class ResourceDiagnostics:
    phi_plus_overlap: float
    best_bell_overlap: float
    best_bell_label: str
    logical_chsh: float
    negativity: float
    purity: float


@dataclasses.dataclass(frozen=True)
class CandidateDiagnostics:
    label: str
    energy: float
    energy_excess: float
    ground_fidelity: float
    support: SupportDiagnostics
    species_entropy_bits: float
    logical_env_entropy_bits: float
    best_bell_overlap: float
    negativity: float


@dataclasses.dataclass(frozen=True)
class CaseDiagnostics:
    case: AuditCase
    n_sites: int
    n_env: int
    h1_spectrum: SpectrumDiagnostics
    h2_spectrum: SpectrumDiagnostics
    h1_tensor_ground_fidelity: float
    uniform_tensor_ground_fidelity: float
    ground_resource: ResourceDiagnostics
    bipartitions: tuple[BipartitionDiagnostics, ...]
    supports: tuple[SupportDiagnostics, ...]
    candidates: tuple[CandidateDiagnostics, ...]
    verdict: str


def fmt_float(value: float) -> str:
    if math.isinf(value):
        return "inf"
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e4:
        return f"{value:.6e}"
    return f"{value:.6f}"


def normalize(state: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(state))
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm


def spectrum_diagnostics(evals: np.ndarray, tolerance: float) -> SpectrumDiagnostics:
    degeneracy = int(np.sum(evals <= evals[0] + tolerance))
    if degeneracy >= len(evals):
        gap_after_ground_space = math.inf
    else:
        gap_after_ground_space = float(evals[degeneracy] - evals[0])
    first_excited = float(evals[1]) if len(evals) > 1 else math.inf
    min_gap_unique = float(evals[1] - evals[0]) if len(evals) > 1 else math.inf
    return SpectrumDiagnostics(
        ground_energy=float(evals[0]),
        first_excited_energy=first_excited,
        degeneracy=degeneracy,
        gap_after_ground_space=gap_after_ground_space,
        min_gap_unique=min_gap_unique,
    )


def probability_entropy_bits(probabilities: np.ndarray) -> float:
    positive = probabilities[probabilities > 0.0]
    if len(positive) == 0:
        return 0.0
    return float(-np.sum(positive * np.log2(positive)))


def support_diagnostics(
    label: str, state: np.ndarray, support_threshold: float
) -> SupportDiagnostics:
    probs = np.abs(state) ** 2
    norm = float(np.sum(probs))
    if norm <= 1e-15:
        raise ValueError(f"{label}: state has zero norm")
    probs = probs / norm
    ipr = float(np.sum(probs * probs))
    participation = math.inf if ipr <= 0.0 else 1.0 / ipr
    dimension = int(len(probs))
    return SupportDiagnostics(
        label=label,
        dimension=dimension,
        support_count=int(np.sum(probs > support_threshold)),
        participation_ratio=float(participation),
        participation_fraction=float(participation / dimension),
        max_probability=float(np.max(probs)),
        shannon_bits=probability_entropy_bits(probs),
    )


def bipartition_from_tensor(
    label: str,
    tensor: np.ndarray,
    left_axes: tuple[int, ...],
    tolerance: float,
) -> BipartitionDiagnostics:
    axes = tuple(range(tensor.ndim))
    right_axes = tuple(axis for axis in axes if axis not in left_axes)
    permuted = np.transpose(tensor, left_axes + right_axes)
    left_dim = int(np.prod([tensor.shape[axis] for axis in left_axes]))
    right_dim = int(np.prod([tensor.shape[axis] for axis in right_axes]))
    matrix = permuted.reshape(left_dim, right_dim)
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    weights = singular_values * singular_values
    total = float(np.sum(weights))
    if total <= 1e-15:
        raise ValueError(f"{label}: zero Schmidt weight")
    weights = weights / total
    purity = float(np.sum(weights * weights))
    return BipartitionDiagnostics(
        label=label,
        entropy_bits=probability_entropy_bits(weights),
        purity=purity,
        max_schmidt_weight=float(np.max(weights)),
        effective_rank=float(1.0 / purity),
        numerical_rank=int(np.sum(weights > tolerance)),
    )


def single_species_logical_env_tensor(
    state: np.ndarray, n_sites: int, factors
) -> np.ndarray:
    n_env = len(factors.env_labels)
    tensor = np.zeros((2, n_env), dtype=complex)
    for site in range(n_sites):
        tensor[factors.logical[site], factors.env[site]] = state[site]
    return tensor


def resource_diagnostics(psi: np.ndarray, n_sites: int, factors) -> ResourceDiagnostics:
    amp = amplitudes_by_logical_env(psi, n_sites, factors)
    rho = reduced_logical_resource(amp)
    best_overlap, best_label = best_bell_overlap(rho)
    phi_plus = float(np.real(rho[0, 0] + rho[0, 3] + rho[3, 0] + rho[3, 3]) / 2.0)
    return ResourceDiagnostics(
        phi_plus_overlap=phi_plus,
        best_bell_overlap=best_overlap,
        best_bell_label=best_label,
        logical_chsh=two_qubit_chsh(rho),
        negativity=negativity(rho),
        purity=float(np.real(np.trace(rho @ rho))),
    )


def logical_resource_simple_metrics(
    psi: np.ndarray, n_sites: int, factors
) -> tuple[float, float]:
    resource = resource_diagnostics(psi, n_sites, factors)
    return resource.best_bell_overlap, resource.negativity


def site_basis_state(n_sites: int, site: int) -> np.ndarray:
    state = np.zeros(n_sites, dtype=complex)
    state[site] = 1.0
    return state


def logical_plus_env_state(n_sites: int, factors, env_index: int = 0) -> np.ndarray:
    sites = [site for site in range(n_sites) if int(factors.env[site]) == env_index]
    if not sites:
        raise ValueError(f"no sites for env index {env_index}")
    state = np.zeros(n_sites, dtype=complex)
    for site in sites:
        state[site] = 1.0
    return normalize(state)


def candidate_diagnostics(
    label: str,
    state: np.ndarray,
    h2: np.ndarray,
    ground: np.ndarray,
    ground_energy: float,
    n_sites: int,
    factors,
    support_threshold: float,
    entropy_tolerance: float,
) -> CandidateDiagnostics:
    state = normalize(state)
    energy = float(np.real(np.vdot(state, h2 @ state)))
    species_tensor = state.reshape(n_sites, n_sites)
    species = bipartition_from_tensor(
        "species A | species B",
        species_tensor,
        left_axes=(0,),
        tolerance=entropy_tolerance,
    )
    amp = amplitudes_by_logical_env(state, n_sites, factors)
    logical_env = bipartition_from_tensor(
        "logical pair | environment pair",
        amp,
        left_axes=(0, 2),
        tolerance=entropy_tolerance,
    )
    best_bell, neg = logical_resource_simple_metrics(state, n_sites, factors)
    return CandidateDiagnostics(
        label=label,
        energy=energy,
        energy_excess=energy - ground_energy,
        ground_fidelity=float(abs(np.vdot(ground, state)) ** 2),
        support=support_diagnostics(label, state, support_threshold),
        species_entropy_bits=species.entropy_bits,
        logical_env_entropy_bits=logical_env.entropy_bits,
        best_bell_overlap=best_bell,
        negativity=neg,
    )


def run_case(
    case: AuditCase,
    degeneracy_tolerance: float,
    entropy_tolerance: float,
    support_threshold: float,
    localization_fraction_threshold: float,
    gap_threshold: float,
) -> CaseDiagnostics:
    n_sites, adj, parity, _coords = lattice_for_case(case)
    h1 = build_H1(n_sites, adj, parity, mass=case.mass)
    poisson = build_poisson(n_sites, adj)
    h2 = build_H2_tensor(h1, poisson, 0.0, n_sites)

    h1_evals, h1_evecs = eigh(h1)
    h2_evals, h2_evecs = eigh(h2)
    h1_spectrum = spectrum_diagnostics(h1_evals, degeneracy_tolerance)
    h2_spectrum = spectrum_diagnostics(h2_evals, degeneracy_tolerance)
    h1_ground = h1_evecs[:, 0]
    h2_ground = h2_evecs[:, 0]
    h1_tensor_ground = normalize(np.kron(h1_ground, h1_ground))
    uniform_single = np.full(n_sites, 1.0 / math.sqrt(n_sites), dtype=complex)
    uniform_tensor = np.kron(uniform_single, uniform_single)

    factors = factor_sites(case.dim, case.side)
    amp = amplitudes_by_logical_env(h2_ground, n_sites, factors)
    single_h1_tensor = single_species_logical_env_tensor(h1_ground, n_sites, factors)

    bipartitions = (
        bipartition_from_tensor(
            "species A | species B",
            h2_ground.reshape(n_sites, n_sites),
            left_axes=(0,),
            tolerance=entropy_tolerance,
        ),
        bipartition_from_tensor(
            "logical pair | environment pair",
            amp,
            left_axes=(0, 2),
            tolerance=entropy_tolerance,
        ),
        bipartition_from_tensor(
            "single H1 logical | single H1 environment",
            single_h1_tensor,
            left_axes=(0,),
            tolerance=entropy_tolerance,
        ),
    )
    supports = (
        support_diagnostics("single H1 ground in native sites", h1_ground, support_threshold),
        support_diagnostics("two-species G=0 ground in native site pairs", h2_ground, support_threshold),
    )

    localized_00 = np.kron(site_basis_state(n_sites, 0), site_basis_state(n_sites, 0))
    localized_far = np.kron(
        site_basis_state(n_sites, 0),
        site_basis_state(n_sites, n_sites // 2),
    )
    logical_plus = logical_plus_env_state(n_sites, factors, env_index=0)
    logical_plus_pair = np.kron(logical_plus, logical_plus)

    candidates = (
        candidate_diagnostics(
            "H1 ground tensor product",
            h1_tensor_ground,
            h2,
            h2_ground,
            h2_spectrum.ground_energy,
            n_sites,
            factors,
            support_threshold,
            entropy_tolerance,
        ),
        candidate_diagnostics(
            "uniform site product",
            uniform_tensor,
            h2,
            h2_ground,
            h2_spectrum.ground_energy,
            n_sites,
            factors,
            support_threshold,
            entropy_tolerance,
        ),
        candidate_diagnostics(
            "localized |0>_A |0>_B",
            localized_00,
            h2,
            h2_ground,
            h2_spectrum.ground_energy,
            n_sites,
            factors,
            support_threshold,
            entropy_tolerance,
        ),
        candidate_diagnostics(
            "localized separated sites",
            localized_far,
            h2,
            h2_ground,
            h2_spectrum.ground_energy,
            n_sites,
            factors,
            support_threshold,
            entropy_tolerance,
        ),
        candidate_diagnostics(
            "single-env logical |+> product",
            logical_plus_pair,
            h2,
            h2_ground,
            h2_spectrum.ground_energy,
            n_sites,
            factors,
            support_threshold,
            entropy_tolerance,
        ),
    )

    unique = h2_spectrum.degeneracy == 1 and h2_spectrum.gap_after_ground_space >= gap_threshold
    separable = all(row.entropy_bits <= 1e-8 for row in bipartitions)
    tensor_match = float(abs(np.vdot(h2_ground, h1_tensor_ground)) ** 2)
    product_simple = tensor_match >= 1.0 - 1e-10
    native_local = supports[1].participation_fraction <= localization_fraction_threshold
    if unique and separable and product_simple and native_local:
        verdict = "preparable candidate"
    elif unique and separable and product_simple:
        verdict = "unresolved gap: analytic product ground, but maximally delocalized in native site basis"
    else:
        verdict = "diagnostic no-go for the assumed initial state"

    return CaseDiagnostics(
        case=case,
        n_sites=n_sites,
        n_env=len(factors.env_labels),
        h1_spectrum=h1_spectrum,
        h2_spectrum=h2_spectrum,
        h1_tensor_ground_fidelity=tensor_match,
        uniform_tensor_ground_fidelity=float(abs(np.vdot(h2_ground, uniform_tensor)) ** 2),
        ground_resource=resource_diagnostics(h2_ground, n_sites, factors),
        bipartitions=bipartitions,
        supports=supports,
        candidates=candidates,
        verdict=verdict,
    )


def print_spectrum(label: str, spectrum: SpectrumDiagnostics) -> None:
    print(
        f"  {label}: "
        f"E0={fmt_float(spectrum.ground_energy)}, "
        f"E1={fmt_float(spectrum.first_excited_energy)}, "
        f"degeneracy={spectrum.degeneracy}, "
        f"gap_after_ground_space={fmt_float(spectrum.gap_after_ground_space)}"
    )


def print_case(result: CaseDiagnostics, localization_fraction_threshold: float) -> None:
    case = result.case
    print(f"Case: {case.label}")
    print(
        "  setup: "
        f"dim={case.dim} side={case.side} N={result.n_sites} "
        f"envs/logical_qubit={result.n_env} mass={case.mass:g} G={case.G:g}"
    )
    print_spectrum("single-species H1", result.h1_spectrum)
    print_spectrum("two-species H(G=0)", result.h2_spectrum)
    print(
        "  exact-product checks: "
        f"|<g_G0|g_H1 x g_H1>|^2={fmt_float(result.h1_tensor_ground_fidelity)}, "
        f"|<g_G0|uniform x uniform>|^2={fmt_float(result.uniform_tensor_ground_fidelity)}"
    )
    resource = result.ground_resource
    print(
        "  traced logical resource at G=0: "
        f"Phi+={resource.phi_plus_overlap:.6f}, "
        f"Bell*={resource.best_bell_overlap:.6f} ({resource.best_bell_label}), "
        f"CHSH={resource.logical_chsh:.6f}, "
        f"negativity={resource.negativity:.6f}, purity={resource.purity:.6f}"
    )
    print("  separability diagnostics:")
    print(
        "    "
        f"{'partition':39s} {'S(bits)':>10s} {'purity':>10s} "
        f"{'max weight':>11s} {'rank_eff':>10s} {'rank_num':>8s}"
    )
    for row in result.bipartitions:
        print(
            "    "
            f"{row.label:39s} "
            f"{fmt_float(row.entropy_bits):>10s} "
            f"{fmt_float(row.purity):>10s} "
            f"{fmt_float(row.max_schmidt_weight):>11s} "
            f"{fmt_float(row.effective_rank):>10s} "
            f"{row.numerical_rank:8d}"
        )
    print("  native site-basis support:")
    print(
        "    "
        f"{'state':45s} {'dim':>6s} {'support':>8s} {'PR':>10s} "
        f"{'PR/dim':>10s} {'max prob':>10s} {'Hsite(bits)':>12s}"
    )
    for row in result.supports:
        print(
            "    "
            f"{row.label:45s} "
            f"{row.dimension:6d} "
            f"{row.support_count:8d} "
            f"{fmt_float(row.participation_ratio):>10s} "
            f"{fmt_float(row.participation_fraction):>10s} "
            f"{fmt_float(row.max_probability):>10s} "
            f"{fmt_float(row.shannon_bits):>12s}"
        )
    print("  simple candidate comparison:")
    print(
        "    "
        f"{'candidate':30s} {'E-E0':>12s} {'|<g|c>|2':>11s} "
        f"{'PR/dim':>10s} {'S_AB':>10s} {'S_L|E':>10s} "
        f"{'Bell*':>9s} {'neg':>9s}"
    )
    for row in result.candidates:
        print(
            "    "
            f"{row.label:30s} "
            f"{fmt_float(row.energy_excess):>12s} "
            f"{fmt_float(row.ground_fidelity):>11s} "
            f"{fmt_float(row.support.participation_fraction):>10s} "
            f"{fmt_float(row.species_entropy_bits):>10s} "
            f"{fmt_float(row.logical_env_entropy_bits):>10s} "
            f"{row.best_bell_overlap:9.6f} "
            f"{row.negativity:9.6f}"
        )
    native_local = result.supports[1].participation_fraction <= localization_fraction_threshold
    print(
        "  local/native-basis preparation status: "
        f"{'localized' if native_local else 'not localized'} "
        f"(threshold PR/dim <= {localization_fraction_threshold:g})"
    )
    print(f"  verdict: {result.verdict}")
    print()


def selected_cases(requested: list[str] | None) -> tuple[AuditCase, ...]:
    if not requested:
        return DEFAULT_CASES
    by_label = {case.label: case for case in DEFAULT_CASES}
    return tuple(by_label[label] for label in requested)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        choices=[case.label for case in DEFAULT_CASES],
        action="append",
        help="case label to run; omit to run the default 1D and 2D G=0 cases",
    )
    parser.add_argument(
        "--degeneracy-tolerance",
        type=float,
        default=1e-9,
        help="energy tolerance for identifying spectral degeneracy",
    )
    parser.add_argument(
        "--entropy-tolerance",
        type=float,
        default=1e-12,
        help="Schmidt-weight tolerance for numerical rank",
    )
    parser.add_argument(
        "--support-threshold",
        type=float,
        default=1e-12,
        help="native-basis probability threshold counted as support",
    )
    parser.add_argument(
        "--gap-threshold",
        type=float,
        default=1e-6,
        help="minimum gap for the uniqueness/gap verdict",
    )
    parser.add_argument(
        "--localization-fraction-threshold",
        type=float,
        default=0.25,
        help="PR/dim threshold for calling a native-basis state localized",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.degeneracy_tolerance <= 0.0:
        raise ValueError("--degeneracy-tolerance must be positive")
    if args.entropy_tolerance <= 0.0:
        raise ValueError("--entropy-tolerance must be positive")
    if args.support_threshold < 0.0:
        raise ValueError("--support-threshold must be nonnegative")
    if args.gap_threshold < 0.0:
        raise ValueError("--gap-threshold must be nonnegative")
    if not (0.0 < args.localization_fraction_threshold <= 1.0):
        raise ValueError("--localization-fraction-threshold must be in (0, 1]")


def main() -> int:
    args = parse_args()
    validate_args(args)

    print("TELEPORTATION INITIAL-STATE PREPARATION PROBE")
    print("Status: planning / first artifact; ordinary quantum state teleportation only")
    print(
        "Claim boundary: no matter, mass, charge, energy, object, or faster-than-light transport"
    )
    print(
        "Question: is the G=0 two-species ground state unique, product-like, "
        "separable, native-basis simple/localized, and operationally plausible?"
    )
    print(
        "Thresholds: "
        f"degeneracy_tol={args.degeneracy_tolerance:g}, "
        f"support_prob>{args.support_threshold:g}, "
        f"gap>={args.gap_threshold:g}, "
        f"localized_PR_fraction<={args.localization_fraction_threshold:g}"
    )
    print()

    results = [
        run_case(
            case,
            degeneracy_tolerance=args.degeneracy_tolerance,
            entropy_tolerance=args.entropy_tolerance,
            support_threshold=args.support_threshold,
            localization_fraction_threshold=args.localization_fraction_threshold,
            gap_threshold=args.gap_threshold,
        )
        for case in selected_cases(args.case)
    ]
    for result in results:
        print_case(result, args.localization_fraction_threshold)

    unique_count = sum(result.h2_spectrum.degeneracy == 1 for result in results)
    product_count = sum(result.h1_tensor_ground_fidelity >= 1.0 - 1e-10 for result in results)
    localized_count = sum(
        result.supports[1].participation_fraction <= args.localization_fraction_threshold
        for result in results
    )
    unresolved = [result for result in results if result.verdict.startswith("unresolved")]
    no_go = [result for result in results if result.verdict.startswith("diagnostic no-go")]

    print("Conclusion:")
    print(f"  unique G=0 two-species ground states: {unique_count}/{len(results)}")
    print(f"  exactly H1-ground tensor products: {product_count}/{len(results)}")
    print(
        "  native-basis localized by participation threshold: "
        f"{localized_count}/{len(results)}"
    )
    if no_go:
        print("  diagnostic no-go cases: " + ", ".join(row.case.label for row in no_go))
    elif unresolved:
        print(
            "  verdict: unresolved preparation gap, not a spectral/product no-go. "
            "The assumed state is unique and separable on these small G=0 surfaces, "
            "but it is a fully delocalized coherent native-site superposition."
        )
    else:
        print("  verdict: preparable candidate under the current small-surface diagnostics")
    print(
        "  Operational read: preparing the state reduces to preparing two independent "
        "single-species H1 ground states. This is simple analytically, but this "
        "artifact does not supply a cooling/control/readout protocol, noise model, "
        "or scaling proof."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
