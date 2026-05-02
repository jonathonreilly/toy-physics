#!/usr/bin/env python3
"""3D initial-state and ramp probe for Poisson teleportation preparation.

Status: planning / first artifact. This bounded diagnostic pressures the
2D ramp evidence on the smallest exact 3D lattice: three spatial directions
plus one finite ramp-time direction.

Scope boundary: ordinary quantum state teleportation resources only. This
does not claim matter transfer, mass transfer, charge transfer, energy
transfer, object transport, or faster-than-light signaling.
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


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_bell_inequality import build_H1, build_H2_tensor, build_poisson  # noqa: E402
from frontier_teleportation_resource_fidelity import (  # noqa: E402
    CLASSICAL_AVG_FIDELITY,
    exact_average_fidelity,
)
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


DEFAULT_DIM = 3
DEFAULT_SIDE = 2
DEFAULT_MASS = 0.0
DEFAULT_G_TARGET = 1000.0
DEFAULT_GRID_POINTS = 21
DEFAULT_RUNTIME = 40.0
DEFAULT_STEPS = 320
DEFAULT_SCHEDULE = "smoothstep"


@dataclasses.dataclass(frozen=True)
class Schedule:
    name: str
    description: str
    fn: Callable[[float], float]


@dataclasses.dataclass(frozen=True)
class HamiltonianData:
    case: AuditCase
    n_sites: int
    n_env: int
    h1: np.ndarray
    h_initial: np.ndarray
    h_target: np.ndarray
    d_hamiltonian: np.ndarray
    d_hamiltonian_norm: float


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
class InitialStateDiagnostics:
    case: AuditCase
    n_sites: int
    n_env: int
    h1_spectrum: SpectrumDiagnostics
    h2_spectrum: SpectrumDiagnostics
    h1_tensor_ground_fidelity: float
    uniform_tensor_ground_fidelity: float
    resource: ResourceMetrics
    bipartitions: tuple[BipartitionDiagnostics, ...]
    supports: tuple[SupportDiagnostics, ...]
    verdict: str


@dataclasses.dataclass(frozen=True)
class RampStepDiagnostics:
    s: float
    ground_energy: float
    gap: float
    target_ground_overlap: float
    resource: ResourceMetrics
    first_excited_adiabatic: float
    max_excited_adiabatic: float
    rss_adiabatic: float
    norm_bound_adiabatic: float
    dominant_level: int
    dominant_gap: float
    dominant_coupling: float


@dataclasses.dataclass(frozen=True)
class RampDiagnostics:
    data: HamiltonianData
    target_gap: float
    target_ground: np.ndarray = dataclasses.field(repr=False, compare=False)
    steps: tuple[RampStepDiagnostics, ...]

    @property
    def is_null(self) -> bool:
        return abs(self.data.case.G) <= 1e-15

    @property
    def final_step(self) -> RampStepDiagnostics:
        return self.steps[-1]

    @property
    def min_gap_step(self) -> RampStepDiagnostics:
        return min(self.steps, key=lambda row: row.gap)

    @property
    def max_exact_step(self) -> RampStepDiagnostics:
        return max(self.steps, key=lambda row: row.max_excited_adiabatic)

    @property
    def max_norm_step(self) -> RampStepDiagnostics:
        return max(self.steps, key=lambda row: row.norm_bound_adiabatic)


@dataclasses.dataclass(frozen=True)
class EvolutionDiagnostics:
    case: AuditCase
    schedule: str
    runtime: float
    steps: int
    dt: float
    final_norm_error: float
    target_ground_overlap: float
    diabatic_loss: float
    final_energy_excess: float
    support: SupportDiagnostics
    resource: ResourceMetrics

    @property
    def is_null(self) -> bool:
        return abs(self.case.G) <= 1e-15


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


def normalize(state: np.ndarray) -> np.ndarray:
    norm_value = float(np.linalg.norm(state))
    if norm_value <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm_value


def probability_entropy_bits(probabilities: np.ndarray) -> float:
    positive = probabilities[probabilities > 0.0]
    if len(positive) == 0:
        return 0.0
    return float(-np.sum(positive * np.log2(positive)))


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


def support_diagnostics(
    label: str, state: np.ndarray, support_threshold: float
) -> SupportDiagnostics:
    probabilities = np.abs(state) ** 2
    total = float(np.sum(probabilities))
    if total <= 1e-15:
        raise ValueError(f"{label}: state has zero norm")
    probabilities = probabilities / total
    ipr = float(np.sum(probabilities * probabilities))
    participation = math.inf if ipr <= 0.0 else 1.0 / ipr
    dimension = int(len(probabilities))
    return SupportDiagnostics(
        label=label,
        dimension=dimension,
        support_count=int(np.sum(probabilities > support_threshold)),
        participation_ratio=float(participation),
        participation_fraction=float(participation / dimension),
        max_probability=float(np.max(probabilities)),
        shannon_bits=probability_entropy_bits(probabilities),
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


def phi_plus_overlap(rho: np.ndarray) -> float:
    phi_plus = bell_state(0, 0)
    return float(np.real(np.vdot(phi_plus, rho @ phi_plus)))


def best_frame_avg_fidelity(best_overlap: float) -> float:
    return float((1.0 + 2.0 * best_overlap) / 3.0)


def logical_resource_density(psi: np.ndarray, n_sites: int, factors) -> np.ndarray:
    amp = amplitudes_by_logical_env(psi, n_sites, factors)
    return reduced_logical_resource(amp)


def resource_metrics(psi: np.ndarray, n_sites: int, factors) -> ResourceMetrics:
    rho = logical_resource_density(psi, n_sites, factors)
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


def make_case(label: str, side: int, mass: float, G: float) -> AuditCase:
    return AuditCase(label=label, dim=DEFAULT_DIM, side=side, mass=mass, G=G)


def build_hamiltonian_data(case: AuditCase) -> HamiltonianData:
    n_sites, adj, parity, _coords = lattice_for_case(case)
    h1 = build_H1(n_sites, adj, parity, mass=case.mass)
    poisson = build_poisson(n_sites, adj)
    h_initial = build_H2_tensor(h1, poisson, 0.0, n_sites)
    h_target = build_H2_tensor(h1, poisson, case.G, n_sites)
    d_hamiltonian = h_target - h_initial
    factors = factor_sites(case.dim, case.side)
    return HamiltonianData(
        case=case,
        n_sites=n_sites,
        n_env=len(factors.env_labels),
        h1=h1,
        h_initial=h_initial,
        h_target=h_target,
        d_hamiltonian=d_hamiltonian,
        d_hamiltonian_norm=float(norm(d_hamiltonian, 2)),
    )


def initial_state_diagnostics(
    data: HamiltonianData,
    degeneracy_tolerance: float,
    entropy_tolerance: float,
    support_threshold: float,
    localization_fraction_threshold: float,
    gap_threshold: float,
) -> InitialStateDiagnostics:
    h1_evals, h1_evecs = eigh(data.h1)
    h2_evals, h2_evecs = eigh(data.h_initial)
    h1_spectrum = spectrum_diagnostics(h1_evals, degeneracy_tolerance)
    h2_spectrum = spectrum_diagnostics(h2_evals, degeneracy_tolerance)
    h1_ground = h1_evecs[:, 0]
    h2_ground = h2_evecs[:, 0]
    h1_tensor_ground = normalize(np.kron(h1_ground, h1_ground))
    uniform_single = np.full(data.n_sites, 1.0 / math.sqrt(data.n_sites), dtype=complex)
    uniform_tensor = np.kron(uniform_single, uniform_single)

    factors = factor_sites(data.case.dim, data.case.side)
    amp = amplitudes_by_logical_env(h2_ground, data.n_sites, factors)
    single_tensor = single_species_logical_env_tensor(h1_ground, data.n_sites, factors)

    bipartitions = (
        bipartition_from_tensor(
            "species A | species B",
            h2_ground.reshape(data.n_sites, data.n_sites),
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
            single_tensor,
            left_axes=(0,),
            tolerance=entropy_tolerance,
        ),
    )
    supports = (
        support_diagnostics(
            "single H1 ground in native sites",
            h1_ground,
            support_threshold,
        ),
        support_diagnostics(
            "two-species G=0 ground in native site pairs",
            h2_ground,
            support_threshold,
        ),
    )

    unique = (
        h2_spectrum.degeneracy == 1
        and h2_spectrum.gap_after_ground_space >= gap_threshold
    )
    separable = all(row.entropy_bits <= 1e-8 for row in bipartitions)
    tensor_match = float(abs(np.vdot(h2_ground, h1_tensor_ground)) ** 2)
    product_simple = tensor_match >= 1.0 - 1e-10
    native_local = supports[1].participation_fraction <= localization_fraction_threshold
    if unique and separable and product_simple and native_local:
        verdict = "candidate"
    elif unique and separable and product_simple:
        verdict = "unresolved gap"
    else:
        verdict = "negative"

    return InitialStateDiagnostics(
        case=data.case,
        n_sites=data.n_sites,
        n_env=data.n_env,
        h1_spectrum=h1_spectrum,
        h2_spectrum=h2_spectrum,
        h1_tensor_ground_fidelity=tensor_match,
        uniform_tensor_ground_fidelity=float(abs(np.vdot(h2_ground, uniform_tensor)) ** 2),
        resource=resource_metrics(h2_ground, data.n_sites, factors),
        bipartitions=bipartitions,
        supports=supports,
        verdict=verdict,
    )


def path_grid(points: int) -> np.ndarray:
    if points < 2:
        raise ValueError("--grid-points must be at least 2")
    return np.linspace(0.0, 1.0, points)


def finite_ratio(numerator: float, denominator: float, gap_floor: float) -> float:
    if denominator <= gap_floor:
        return math.inf
    return numerator / (denominator * denominator)


def ramp_step_diagnostics(
    s: float,
    hamiltonian: np.ndarray,
    d_hamiltonian: np.ndarray,
    d_hamiltonian_norm: float,
    target_ground: np.ndarray,
    n_sites: int,
    factors,
    gap_floor: float,
) -> RampStepDiagnostics:
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
        max_exact = float(ratios[dominant_offset])
        dominant_gap = float(gaps[dominant_offset])
        dominant_coupling = float(couplings[dominant_offset])
        first_excited = float(ratios[0])
        finite_values = ratios[np.isfinite(ratios)]
        rss = math.inf if len(finite_values) != len(ratios) else float(np.sqrt(np.sum(ratios * ratios)))
    else:
        dominant_level = 0
        max_exact = 0.0
        dominant_gap = math.inf
        dominant_coupling = 0.0
        first_excited = 0.0
        rss = 0.0

    return RampStepDiagnostics(
        s=float(s),
        ground_energy=float(evals[0]),
        gap=gap,
        target_ground_overlap=float(abs(np.vdot(target_ground, ground)) ** 2),
        resource=resource_metrics(ground, n_sites, factors),
        first_excited_adiabatic=first_excited,
        max_excited_adiabatic=max_exact,
        rss_adiabatic=rss,
        norm_bound_adiabatic=finite_ratio(d_hamiltonian_norm, gap, gap_floor),
        dominant_level=dominant_level,
        dominant_gap=dominant_gap,
        dominant_coupling=dominant_coupling,
    )


def run_ramp_path(data: HamiltonianData, grid_points: int, gap_floor: float) -> RampDiagnostics:
    target_evals, target_evecs = eigh(data.h_target)
    target_ground = target_evecs[:, 0]
    factors = factor_sites(data.case.dim, data.case.side)
    steps = []
    for s in path_grid(grid_points):
        hamiltonian = data.h_initial + float(s) * data.d_hamiltonian
        steps.append(
            ramp_step_diagnostics(
                s=float(s),
                hamiltonian=hamiltonian,
                d_hamiltonian=data.d_hamiltonian,
                d_hamiltonian_norm=data.d_hamiltonian_norm,
                target_ground=target_ground,
                n_sites=data.n_sites,
                factors=factors,
                gap_floor=gap_floor,
            )
        )
    return RampDiagnostics(
        data=data,
        target_gap=float(target_evals[1] - target_evals[0]) if len(target_evals) > 1 else math.inf,
        target_ground=target_ground,
        steps=tuple(steps),
    )


def apply_step(hamiltonian: np.ndarray, psi: np.ndarray, dt: float) -> np.ndarray:
    evals, evecs = eigh(hamiltonian)
    coeff = evecs.conj().T @ psi
    return evecs @ (np.exp(-1j * evals * dt) * coeff)


def finite_time_evolution(
    data: HamiltonianData,
    target_ground: np.ndarray,
    schedule: Schedule,
    runtime: float,
    steps: int,
    support_threshold: float,
) -> EvolutionDiagnostics:
    initial_evals, initial_evecs = eigh(data.h_initial)
    target_evals = eigh(data.h_target, eigvals_only=True)
    initial_state = initial_evecs[:, 0]
    dt = runtime / steps
    if data.d_hamiltonian_norm <= 1e-14:
        psi = initial_state * np.exp(-1j * float(initial_evals[0]) * runtime)
    else:
        psi = initial_state.copy()
        for step in range(steps):
            u_mid = (step + 0.5) / steps
            s_mid = schedule.fn(float(u_mid))
            hamiltonian = data.h_initial + s_mid * data.d_hamiltonian
            psi = apply_step(hamiltonian, psi, dt)

    final_norm = float(np.linalg.norm(psi))
    if final_norm <= 1e-15:
        raise ValueError(f"{data.case.label}: finite-time evolution produced a zero state")
    psi = psi / final_norm
    final_energy = float(np.real(np.vdot(psi, data.h_target @ psi)))
    factors = factor_sites(data.case.dim, data.case.side)
    return EvolutionDiagnostics(
        case=data.case,
        schedule=schedule.name,
        runtime=runtime,
        steps=steps,
        dt=dt,
        final_norm_error=abs(final_norm - 1.0),
        target_ground_overlap=float(abs(np.vdot(target_ground, psi)) ** 2),
        diabatic_loss=max(0.0, 1.0 - float(abs(np.vdot(target_ground, psi)) ** 2)),
        final_energy_excess=max(0.0, final_energy - float(target_evals[0])),
        support=support_diagnostics(
            "finite-time final state in native site pairs",
            psi,
            support_threshold,
        ),
        resource=resource_metrics(psi, data.n_sites, factors),
    )


def sample_rows(steps: tuple[RampStepDiagnostics, ...]) -> tuple[RampStepDiagnostics, ...]:
    requested = (0.0, 0.25, 0.5, 0.75, 1.0)
    selected: list[RampStepDiagnostics] = []
    used_indices: set[int] = set()
    for value in requested:
        index = min(range(len(steps)), key=lambda item: abs(steps[item].s - value))
        if index not in used_indices:
            selected.append(steps[index])
            used_indices.add(index)
    return tuple(selected)


def print_spectrum(label: str, spectrum: SpectrumDiagnostics) -> None:
    print(
        f"  {label}: "
        f"E0={fmt_float(spectrum.ground_energy)}, "
        f"E1={fmt_float(spectrum.first_excited_energy)}, "
        f"degeneracy={spectrum.degeneracy}, "
        f"gap_after_ground_space={fmt_float(spectrum.gap_after_ground_space)}"
    )


def print_resource(prefix: str, metrics: ResourceMetrics) -> None:
    print(
        prefix
        + f"Phi+={metrics.phi_plus_overlap:.6f}, "
        + f"Bell*={metrics.best_bell_overlap:.6f} ({metrics.best_bell_label}), "
        + f"Favg(Phi frame)={metrics.exact_avg_fidelity:.6f}, "
        + f"Favg(best frame)={metrics.best_frame_avg_fidelity:.6f}, "
        + f"CHSH={metrics.logical_chsh:.6f}, "
        + f"neg={metrics.negativity:.6f}, purity={metrics.purity:.6f}"
    )


def print_initial(result: InitialStateDiagnostics, localization_fraction_threshold: float) -> None:
    print("3D G=0 initial-state diagnostics")
    print(
        "  setup: "
        f"dim={result.case.dim} side={result.case.side} N={result.n_sites} "
        f"envs/logical_qubit={result.n_env} mass={result.case.mass:g}"
    )
    print_spectrum("single-species H1", result.h1_spectrum)
    print_spectrum("two-species H(G=0)", result.h2_spectrum)
    print(
        "  exact-product checks: "
        f"|<g_G0|g_H1 x g_H1>|^2={fmt_float(result.h1_tensor_ground_fidelity)}, "
        f"|<g_G0|uniform x uniform>|^2={fmt_float(result.uniform_tensor_ground_fidelity)}"
    )
    print_resource("  traced logical resource at G=0: ", result.resource)
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
    native_local = result.supports[1].participation_fraction <= localization_fraction_threshold
    print(
        "  local/native-basis preparation status: "
        f"{'localized' if native_local else 'not localized'} "
        f"(threshold PR/dim <= {localization_fraction_threshold:g})"
    )
    print(f"  initial-state verdict: {result.verdict}")
    print()


def print_ramp(result: RampDiagnostics) -> None:
    case = result.data.case
    print(f"Ramp path: {case.label}")
    print(
        "  lattice/params: "
        f"dim={case.dim} side={case.side} N={result.data.n_sites} "
        f"envs/logical_qubit={result.data.n_env} mass={case.mass:g} "
        f"G_target={case.G:g}"
    )
    print(
        "  path: H(s)=H(G=0)+s*(H(G_target)-H(G=0)); "
        f"||dH/ds||_2={fmt_float(result.data.d_hamiltonian_norm)}"
    )
    print("  sampled path rows:")
    print(
        "    "
        f"{'s':>6s} {'gap':>12s} {'target|ov|2':>12s} {'Bell*':>10s} "
        f"{'label':>5s} {'Fbest':>10s} {'CHSH':>10s} {'neg':>10s} "
        f"{'Amax':>12s} {'norm/gap2':>12s}"
    )
    for row in sample_rows(result.steps):
        resource = row.resource
        print(
            "    "
            f"{row.s:6.3f} "
            f"{fmt_float(row.gap):>12s} "
            f"{fmt_float(row.target_ground_overlap):>12s} "
            f"{resource.best_bell_overlap:10.6f} "
            f"{resource.best_bell_label:>5s} "
            f"{resource.best_frame_avg_fidelity:10.6f} "
            f"{resource.logical_chsh:10.6f} "
            f"{resource.negativity:10.6f} "
            f"{fmt_float(row.max_excited_adiabatic):>12s} "
            f"{fmt_float(row.norm_bound_adiabatic):>12s}"
        )
    min_gap = result.min_gap_step
    max_exact = result.max_exact_step
    max_norm = result.max_norm_step
    print(
        "  path summary: "
        f"min gap={fmt_float(min_gap.gap)} at s={min_gap.s:.3f}; "
        f"target gap={fmt_float(result.target_gap)}; "
        f"max exact A={fmt_float(max_exact.max_excited_adiabatic)} at s={max_exact.s:.3f}; "
        f"max ||dH||/gap^2={fmt_float(max_norm.norm_bound_adiabatic)} at s={max_norm.s:.3f}"
    )
    print_resource("  endpoint resource: ", result.final_step.resource)
    print()


def print_evolution(result: EvolutionDiagnostics) -> None:
    print(f"Finite-time ramp: {result.case.label}")
    print(
        "  evolution: "
        f"schedule={result.schedule}, T={result.runtime:g}, steps={result.steps}, "
        f"dt={fmt_float(result.dt)}, norm_err={result.final_norm_error:.3e}"
    )
    print(
        "  target tracking: "
        f"|<g_target|psi(T)>|^2={fmt_float(result.target_ground_overlap)}, "
        f"diabatic_loss={fmt_float(result.diabatic_loss)}, "
        f"final_energy_excess={fmt_float(result.final_energy_excess)}"
    )
    print_resource("  final resource: ", result.resource)
    support = result.support
    print(
        "  final native support: "
        f"dim={support.dimension}, support={support.support_count}, "
        f"PR={fmt_float(support.participation_ratio)}, "
        f"PR/dim={fmt_float(support.participation_fraction)}, "
        f"max_prob={fmt_float(support.max_probability)}, "
        f"Hsite={fmt_float(support.shannon_bits)} bits"
    )
    print()


def null_control_clean(
    ramp: RampDiagnostics,
    evolution: EvolutionDiagnostics,
    tolerance: float,
) -> bool:
    return (
        ramp.is_null
        and evolution.is_null
        and ramp.data.d_hamiltonian_norm <= tolerance
        and ramp.final_step.resource.best_bell_overlap <= 0.5 + 10.0 * tolerance
        and ramp.final_step.resource.negativity <= 10.0 * tolerance
        and evolution.resource.best_bell_overlap <= 0.5 + 10.0 * tolerance
        and evolution.resource.negativity <= 10.0 * tolerance
        and evolution.resource.best_frame_avg_fidelity <= CLASSICAL_AVG_FIDELITY + 10.0 * tolerance
    )


def resource_candidate(
    ramp: RampDiagnostics,
    evolution: EvolutionDiagnostics,
    bell_threshold: float,
    ground_overlap_threshold: float,
    min_gap_threshold: float,
) -> bool:
    return (
        (not ramp.is_null)
        and ramp.final_step.resource.best_bell_overlap >= bell_threshold
        and ramp.min_gap_step.gap >= min_gap_threshold
        and evolution.resource.best_bell_overlap >= bell_threshold
        and evolution.target_ground_overlap >= ground_overlap_threshold
        and evolution.resource.best_frame_avg_fidelity > CLASSICAL_AVG_FIDELITY
    )


def combined_verdict(
    initial: InitialStateDiagnostics,
    null_clean: bool,
    target_candidate: bool,
    target_ramp: RampDiagnostics,
    min_gap_threshold: float,
) -> str:
    if not null_clean:
        return "negative: null control produced a resource-like signal"
    if initial.verdict == "negative":
        return "negative: G=0 initial state failed uniqueness/product/separability checks"
    if not target_candidate:
        return "negative: finite-time 3D ramp did not produce the logical resource"
    if target_ramp.min_gap_step.gap < min_gap_threshold:
        return "unresolved gap: sampled 3D target path falls below the gap threshold"
    if initial.verdict == "unresolved gap":
        return "unresolved gap: side-2 ramp is a resource candidate, but the G=0 state is maximally delocalized in the native basis"
    return "candidate"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", type=int, default=DEFAULT_SIDE, help="3D lattice side length")
    parser.add_argument("--mass", type=float, default=DEFAULT_MASS, help="single-species mass")
    parser.add_argument(
        "--G-target",
        type=float,
        default=DEFAULT_G_TARGET,
        help="Poisson coupling target for the non-null 3D ramp",
    )
    parser.add_argument(
        "--grid-points",
        type=int,
        default=DEFAULT_GRID_POINTS,
        help="number of uniformly spaced s values in [0, 1]",
    )
    parser.add_argument(
        "--runtime",
        type=float,
        default=DEFAULT_RUNTIME,
        help="finite-time ramp duration",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=DEFAULT_STEPS,
        help="finite-time midpoint steps",
    )
    parser.add_argument(
        "--schedule",
        choices=sorted(SCHEDULES),
        default=DEFAULT_SCHEDULE,
        help="finite-time schedule",
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
        help="minimum G=0 gap for the initial-state verdict",
    )
    parser.add_argument(
        "--min-ramp-gap-threshold",
        type=float,
        default=1e-3,
        help="minimum sampled ramp gap for a resource-candidate verdict",
    )
    parser.add_argument(
        "--logical-bell-threshold",
        type=float,
        default=0.90,
        help="best Bell overlap threshold for a logical resource candidate",
    )
    parser.add_argument(
        "--ground-overlap-threshold",
        type=float,
        default=0.99,
        help="finite-time target-ground overlap threshold",
    )
    parser.add_argument(
        "--localization-fraction-threshold",
        type=float,
        default=0.25,
        help="PR/dim threshold for calling a native-basis state localized",
    )
    parser.add_argument(
        "--gap-floor",
        type=float,
        default=1e-12,
        help="gap floor below which adiabatic ratios are reported as infinite",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.side < 2 or args.side % 2 != 0:
        raise ValueError("--side must be an even integer >= 2")
    if args.grid_points < 2:
        raise ValueError("--grid-points must be at least 2")
    if args.runtime <= 0.0:
        raise ValueError("--runtime must be positive")
    if args.steps < 1:
        raise ValueError("--steps must be positive")
    if args.degeneracy_tolerance <= 0.0:
        raise ValueError("--degeneracy-tolerance must be positive")
    if args.entropy_tolerance <= 0.0:
        raise ValueError("--entropy-tolerance must be positive")
    if args.support_threshold < 0.0:
        raise ValueError("--support-threshold must be nonnegative")
    if args.gap_threshold < 0.0:
        raise ValueError("--gap-threshold must be nonnegative")
    if args.min_ramp_gap_threshold < 0.0:
        raise ValueError("--min-ramp-gap-threshold must be nonnegative")
    if not (0.0 < args.logical_bell_threshold <= 1.0):
        raise ValueError("--logical-bell-threshold must be in (0, 1]")
    if not (0.0 < args.ground_overlap_threshold <= 1.0):
        raise ValueError("--ground-overlap-threshold must be in (0, 1]")
    if not (0.0 < args.localization_fraction_threshold <= 1.0):
        raise ValueError("--localization-fraction-threshold must be in (0, 1]")
    if args.gap_floor < 0.0:
        raise ValueError("--gap-floor must be nonnegative")


def main() -> int:
    args = parse_args()
    validate_args(args)

    null_case = make_case("3d_side2_null" if args.side == 2 else "3d_null", args.side, args.mass, 0.0)
    target_case = make_case(
        "3d_side2_poisson" if args.side == 2 else "3d_poisson",
        args.side,
        args.mass,
        args.G_target,
    )
    null_data = build_hamiltonian_data(null_case)
    target_data = build_hamiltonian_data(target_case)
    schedule = SCHEDULES[args.schedule]

    print("TELEPORTATION 3D INITIAL-STATE AND RAMP PROBE")
    print("Status: planning / first artifact; ordinary quantum state teleportation only")
    print(
        "Claim boundary: no matter, mass, charge, energy, object, or "
        "faster-than-light transport"
    )
    print(
        "Geometry: three spatial lattice directions plus one finite ramp-time "
        "diagnostic direction"
    )
    print(
        "Defaults: "
        f"side={args.side}, N={target_data.n_sites}, H2_dim={target_data.h_target.shape[0]}, "
        f"G_target={args.G_target:g}, grid_points={args.grid_points}, "
        f"schedule={schedule.name}, T={args.runtime:g}, steps={args.steps}"
    )
    print(
        "Thresholds: "
        f"Bell*>={args.logical_bell_threshold:.3f}, "
        f"ground_overlap>={args.ground_overlap_threshold:.3f}, "
        f"min_ramp_gap>={args.min_ramp_gap_threshold:g}, "
        f"localized_PR_fraction<={args.localization_fraction_threshold:g}"
    )
    print()

    initial = initial_state_diagnostics(
        target_data,
        degeneracy_tolerance=args.degeneracy_tolerance,
        entropy_tolerance=args.entropy_tolerance,
        support_threshold=args.support_threshold,
        localization_fraction_threshold=args.localization_fraction_threshold,
        gap_threshold=args.gap_threshold,
    )
    print_initial(initial, args.localization_fraction_threshold)

    null_ramp = run_ramp_path(null_data, grid_points=args.grid_points, gap_floor=args.gap_floor)
    target_ramp = run_ramp_path(target_data, grid_points=args.grid_points, gap_floor=args.gap_floor)
    print_ramp(null_ramp)
    print_ramp(target_ramp)

    null_evolution = finite_time_evolution(
        null_data,
        target_ground=null_ramp.target_ground,
        schedule=schedule,
        runtime=args.runtime,
        steps=args.steps,
        support_threshold=args.support_threshold,
    )
    target_evolution = finite_time_evolution(
        target_data,
        target_ground=target_ramp.target_ground,
        schedule=schedule,
        runtime=args.runtime,
        steps=args.steps,
        support_threshold=args.support_threshold,
    )
    print_evolution(null_evolution)
    print_evolution(target_evolution)

    null_clean = null_control_clean(null_ramp, null_evolution, args.degeneracy_tolerance)
    target_candidate = resource_candidate(
        target_ramp,
        target_evolution,
        bell_threshold=args.logical_bell_threshold,
        ground_overlap_threshold=args.ground_overlap_threshold,
        min_gap_threshold=args.min_ramp_gap_threshold,
    )
    verdict = combined_verdict(
        initial,
        null_clean=null_clean,
        target_candidate=target_candidate,
        target_ramp=target_ramp,
        min_gap_threshold=args.min_ramp_gap_threshold,
    )

    print("Conclusion:")
    print(f"  null control clean: {'YES' if null_clean else 'NO'}")
    print(
        "  3D Poisson endpoint resource: "
        f"Bell*={target_ramp.final_step.resource.best_bell_overlap:.6f} "
        f"({target_ramp.final_step.resource.best_bell_label}), "
        f"Favg(best frame)={target_ramp.final_step.resource.best_frame_avg_fidelity:.6f}, "
        f"target gap={fmt_float(target_ramp.target_gap)}"
    )
    print(
        "  finite-time resource: "
        f"ground_overlap={fmt_float(target_evolution.target_ground_overlap)}, "
        f"Bell*={target_evolution.resource.best_bell_overlap:.6f} "
        f"({target_evolution.resource.best_bell_label}), "
        f"Favg(best frame)={target_evolution.resource.best_frame_avg_fidelity:.6f}"
    )
    print(f"  resource-candidate checks passed: {'YES' if target_candidate else 'NO'}")
    print(f"  preparation verdict: {verdict}")
    print(
        "  Interpretation: side=2 exact 3D pressure test only. A favorable "
        "Bell-frame resource on this lattice does not prove scalable "
        "preparation, robustness, readout, or any non-teleportation transport claim."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
