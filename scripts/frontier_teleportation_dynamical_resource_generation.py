#!/usr/bin/env python3
"""Dynamic Poisson resource generation from product states.

Status: planning / first artifact. This runner asks a narrow question:

    If two distinguishable species start in simple product site states and
    evolve under the existing small Poisson-derived Hamiltonian, does the
    traced logical taste-qubit sector ever become a high-fidelity Bell
    resource for ordinary quantum state teleportation?

It does not claim matter teleportation, mass transfer, charge transfer, energy
transfer, object transport, or faster-than-light signaling. The audited object
is only a two-qubit quantum-state teleportation resource extracted from the
time-evolved two-species state.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from collections.abc import Iterable
from pathlib import Path

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
    lattice_1d,
    lattice_2d,
    lattice_3d,
)


I2 = np.eye(2, dtype=complex)
X2 = np.array([[0, 1], [1, 0]], dtype=complex)
Y2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z2 = np.array([[1, 0], [0, -1]], dtype=complex)
PAULIS = (X2, Y2, Z2)

OUTCOME_ORDER = ((0, 0), (1, 0), (0, 1), (1, 1))
OUTCOME_LABELS = {
    (0, 0): "Phi+",
    (1, 0): "Phi-",
    (0, 1): "Psi+",
    (1, 1): "Psi-",
}
USEFUL_BELL_THRESHOLD = 0.5
CLASSICAL_AVG_FIDELITY = 2.0 / 3.0


@dataclasses.dataclass(frozen=True)
class DynamicCase:
    label: str
    dim: int
    side: int
    mass: float
    G: float
    initial_sites: tuple[int, int]
    t_max: float
    samples: int


@dataclasses.dataclass(frozen=True)
class SiteFactorization:
    logical: np.ndarray
    env: np.ndarray
    env_labels: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]


@dataclasses.dataclass(frozen=True)
class TimePoint:
    t: float
    bell_overlap: float
    bell_label: str
    bell_bits: tuple[int, int]
    framed_mean_fidelity: float
    standard_mean_fidelity: float
    logical_chsh: float
    negativity: float
    purity: float


@dataclasses.dataclass(frozen=True)
class ThresholdWindow:
    start: float
    end: float
    peak_t: float
    peak_value: float
    samples: int


@dataclasses.dataclass(frozen=True)
class NoSignalAudit:
    sampled_mean_fidelity: float
    sampled_min_fidelity: float
    sampled_max_fidelity: float
    max_trace_error: float
    max_no_record_to_marginal_distance: float
    max_pairwise_no_record_distance: float
    bob_marginal_bias: float


@dataclasses.dataclass(frozen=True)
class CaseResult:
    case: DynamicCase
    n_sites: int
    n_env: int
    dt: float
    best: TimePoint
    best_full_chsh: float
    max_negativity: float
    useful_windows: tuple[ThresholdWindow, ...]
    high_fidelity_windows: tuple[ThresholdWindow, ...]
    no_signal: NoSignalAudit
    null_control_ok: bool | None


DEFAULT_CASES = (
    DynamicCase(
        label="1d_null_site01",
        dim=1,
        side=8,
        mass=0.0,
        G=0.0,
        initial_sites=(0, 1),
        t_max=20.0,
        samples=401,
    ),
    DynamicCase(
        label="1d_poisson_site01_G50",
        dim=1,
        side=8,
        mass=0.0,
        G=50.0,
        initial_sites=(0, 1),
        t_max=20.0,
        samples=401,
    ),
    DynamicCase(
        label="1d_poisson_site03_G100",
        dim=1,
        side=8,
        mass=0.0,
        G=100.0,
        initial_sites=(0, 3),
        t_max=20.0,
        samples=401,
    ),
)


def lattice_for_case(case: DynamicCase):
    if case.dim == 1:
        return lattice_1d(case.side)
    if case.dim == 2:
        return lattice_2d(case.side)
    if case.dim == 3:
        return lattice_3d(case.side)
    raise ValueError(f"unsupported dimension: {case.dim}")


def coords_from_index(index: int, dim: int, side: int) -> tuple[int, ...]:
    coords: list[int] = []
    remaining = index
    for power in range(dim - 1, -1, -1):
        stride = side**power
        coord = remaining // stride
        coords.append(coord)
        remaining %= stride
    return tuple(coords)


def factor_sites(dim: int, side: int, logical_axis: int | None = None) -> SiteFactorization:
    if side % 2 != 0:
        raise ValueError("KS taste factorization requires an even side length")
    if logical_axis is None:
        logical_axis = dim - 1
    if logical_axis < 0 or logical_axis >= dim:
        raise ValueError("logical_axis is outside the spatial dimension")

    n_sites = side**dim
    logical = np.zeros(n_sites, dtype=int)
    env_raw: list[tuple[tuple[int, ...], tuple[int, ...]]] = []

    for site in range(n_sites):
        coords = coords_from_index(site, dim, side)
        cell = tuple(coord // 2 for coord in coords)
        eta = tuple(coord % 2 for coord in coords)
        spectator = tuple(bit for axis, bit in enumerate(eta) if axis != logical_axis)
        logical[site] = eta[logical_axis]
        env_raw.append((cell, spectator))

    env_labels = tuple(dict.fromkeys(env_raw))
    env_index = {label: index for index, label in enumerate(env_labels)}
    env = np.array([env_index[label] for label in env_raw], dtype=int)
    return SiteFactorization(logical=logical, env=env, env_labels=env_labels)


def amplitudes_by_logical_env(
    psi: np.ndarray, n_sites: int, factors: SiteFactorization
) -> np.ndarray:
    n_env = len(factors.env_labels)
    amp = np.zeros((2, n_env, 2, n_env), dtype=complex)
    for site_a in range(n_sites):
        logical_a = factors.logical[site_a]
        env_a = factors.env[site_a]
        for site_b in range(n_sites):
            logical_b = factors.logical[site_b]
            env_b = factors.env[site_b]
            amp[logical_a, env_a, logical_b, env_b] = psi[site_a * n_sites + site_b]
    return amp


def reduced_logical_resource(amp: np.ndarray) -> np.ndarray:
    rho = np.einsum("aebf,cedf->abcd", amp, amp.conj(), optimize=True)
    rho = rho.reshape(4, 4)
    trace = np.trace(rho)
    if abs(trace) <= 1e-15:
        raise ValueError("logical resource has zero trace")
    rho = rho / trace
    return 0.5 * (rho + rho.conj().T)


def projector(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


def normalize_state(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm


def random_qubit(rng: np.random.Generator) -> np.ndarray:
    return normalize_state(rng.standard_normal(2) + 1j * rng.standard_normal(2))


def probe_states(seed: int, random_inputs: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    states = [
        np.array([1.0, 0.0], dtype=complex),
        np.array([0.0, 1.0], dtype=complex),
        np.array([1.0, 1.0], dtype=complex) / math.sqrt(2.0),
        np.array([1.0, -1.0], dtype=complex) / math.sqrt(2.0),
        np.array([1.0, 1.0j], dtype=complex) / math.sqrt(2.0),
        np.array([1.0, -1.0j], dtype=complex) / math.sqrt(2.0),
    ]
    states.extend(random_qubit(rng) for _ in range(random_inputs))
    return states


def bell_state(z_bit: int, x_bit: int) -> np.ndarray:
    sign = -1.0 if z_bit else 1.0
    state = np.zeros(4, dtype=complex)
    if x_bit == 0:
        state[0] = 1.0 / math.sqrt(2.0)
        state[3] = sign / math.sqrt(2.0)
    else:
        state[1] = 1.0 / math.sqrt(2.0)
        state[2] = sign / math.sqrt(2.0)
    return state


def bell_projector(z_bit: int, x_bit: int) -> np.ndarray:
    return projector(bell_state(z_bit, x_bit))


def correction_operator(z_bit: int, x_bit: int) -> np.ndarray:
    z_op = Z2 if z_bit else I2
    x_op = X2 if x_bit else I2
    return z_op @ x_op


def bell_overlaps(rho: np.ndarray) -> dict[tuple[int, int], float]:
    overlaps: dict[tuple[int, int], float] = {}
    for z_bit, x_bit in OUTCOME_ORDER:
        state = bell_state(z_bit, x_bit)
        overlaps[(z_bit, x_bit)] = float(np.real(np.vdot(state, rho @ state)))
    return overlaps


def best_bell_overlap(rho: np.ndarray) -> tuple[float, tuple[int, int], str]:
    overlaps = bell_overlaps(rho)
    bits = max(overlaps, key=overlaps.__getitem__)
    return overlaps[bits], bits, OUTCOME_LABELS[bits]


def two_qubit_chsh(rho: np.ndarray) -> float:
    correlation = np.zeros((3, 3), dtype=float)
    for i, op_a in enumerate(PAULIS):
        for j, op_b in enumerate(PAULIS):
            correlation[i, j] = float(np.real(np.trace(rho @ np.kron(op_a, op_b))))
    eigvals = np.linalg.eigvalsh(correlation.T @ correlation)
    two_largest = np.sort(eigvals)[-2:]
    return float(2.0 * math.sqrt(max(0.0, float(np.sum(two_largest)))))


def negativity(rho: np.ndarray) -> float:
    partial_transpose_b = rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)
    eigvals = np.linalg.eigvalsh(0.5 * (partial_transpose_b + partial_transpose_b.conj().T))
    return float(np.sum(np.abs(eigvals[eigvals < 0.0])))


def partial_trace(rho: np.ndarray, dims: Iterable[int], keep: Iterable[int]) -> np.ndarray:
    dims = list(dims)
    keep = sorted(keep)
    trace_out = [axis for axis in range(len(dims)) if axis not in keep]
    tensor = rho.reshape(*(dims + dims))
    current_dims = list(dims)
    for axis in sorted(trace_out, reverse=True):
        tensor = np.trace(tensor, axis1=axis, axis2=axis + len(current_dims))
        current_dims.pop(axis)
    final_dim = int(np.prod(current_dims))
    return tensor.reshape(final_dim, final_dim)


def trace_distance(first: np.ndarray, second: np.ndarray) -> float:
    diff = 0.5 * (first - second + (first - second).conj().T)
    eigvals = np.linalg.eigvalsh(diff)
    return float(0.5 * np.sum(np.abs(eigvals)))


def pure_state_fidelity(state: np.ndarray, rho: np.ndarray) -> float:
    value = np.vdot(state, rho @ state)
    return float(np.clip(np.real(value), 0.0, 1.0))


def framed_teleport_density(
    input_rho: np.ndarray, resource_rho: np.ndarray, frame_bits: tuple[int, int]
) -> tuple[np.ndarray, np.ndarray, dict[tuple[int, int], float]]:
    """Teleport with a fixed Bell-resource Pauli frame.

    frame_bits=(0,0) is the standard Phi+ convention. If the resource's largest
    Bell component is another Bell state, xor-ing the frame into Bob's Pauli
    correction is the pre-agreed local correction convention for that resource.
    """
    joint = np.kron(input_rho, resource_rho)
    corrected_output = np.zeros((2, 2), dtype=complex)
    no_record_output = np.zeros((2, 2), dtype=complex)
    branch_probabilities: dict[tuple[int, int], float] = {}

    for z_bit, x_bit in OUTCOME_ORDER:
        measurement = np.kron(bell_projector(z_bit, x_bit), I2)
        branch = measurement @ joint @ measurement
        bob_unnormalized = partial_trace(branch, dims=[2, 2, 2], keep=[2])
        probability = float(np.real(np.trace(bob_unnormalized)))
        branch_probabilities[(z_bit, x_bit)] = probability
        no_record_output += bob_unnormalized

        correction = correction_operator(z_bit ^ frame_bits[0], x_bit ^ frame_bits[1])
        corrected_output += correction @ bob_unnormalized @ correction.conj().T

    return corrected_output, no_record_output, branch_probabilities


def no_signal_audit(
    resource_rho: np.ndarray,
    frame_bits: tuple[int, int],
    states: list[np.ndarray],
) -> NoSignalAudit:
    bob_marginal = partial_trace(resource_rho, dims=[2, 2], keep=[1])
    half_identity = 0.5 * I2
    reference_no_record: np.ndarray | None = None

    fidelities: list[float] = []
    max_trace_error = 0.0
    max_no_record_to_marginal = 0.0
    max_pairwise_no_record = 0.0

    for state in states:
        input_rho = projector(state)
        corrected, no_record, _probabilities = framed_teleport_density(
            input_rho, resource_rho, frame_bits
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


def framed_mean_fidelity_from_overlap(overlap: float) -> float:
    return float((1.0 + 2.0 * overlap) / 3.0)


def time_point_from_rho(t: float, rho: np.ndarray) -> TimePoint:
    overlaps = bell_overlaps(rho)
    best_bits = max(overlaps, key=overlaps.__getitem__)
    best_overlap = overlaps[best_bits]
    phi_plus_overlap = overlaps[(0, 0)]
    return TimePoint(
        t=float(t),
        bell_overlap=best_overlap,
        bell_label=OUTCOME_LABELS[best_bits],
        bell_bits=best_bits,
        framed_mean_fidelity=framed_mean_fidelity_from_overlap(best_overlap),
        standard_mean_fidelity=framed_mean_fidelity_from_overlap(phi_plus_overlap),
        logical_chsh=two_qubit_chsh(rho),
        negativity=negativity(rho),
        purity=float(np.real(np.trace(rho @ rho))),
    )


def threshold_windows(
    points: list[TimePoint],
    values: list[float],
    mask: list[bool],
) -> tuple[ThresholdWindow, ...]:
    windows: list[ThresholdWindow] = []
    start_index: int | None = None

    for index, active in enumerate(mask + [False]):
        if active and start_index is None:
            start_index = index
        if not active and start_index is not None:
            end_index = index - 1
            segment = range(start_index, end_index + 1)
            peak_index = max(segment, key=lambda item: values[item])
            windows.append(
                ThresholdWindow(
                    start=points[start_index].t,
                    end=points[end_index].t,
                    peak_t=points[peak_index].t,
                    peak_value=values[peak_index],
                    samples=end_index - start_index + 1,
                )
            )
            start_index = None

    return tuple(windows)


def validate_case(case: DynamicCase) -> None:
    if case.side % 2 != 0:
        raise ValueError(f"{case.label}: side must be even")
    if case.samples < 2:
        raise ValueError(f"{case.label}: samples must be at least 2")
    if case.t_max <= 0.0:
        raise ValueError(f"{case.label}: t_max must be positive")
    n_sites = case.side**case.dim
    for site in case.initial_sites:
        if site < 0 or site >= n_sites:
            raise ValueError(
                f"{case.label}: initial site {site} outside lattice with N={n_sites}"
            )


def with_overrides(
    case: DynamicCase, samples_override: int | None, t_max_override: float | None
) -> DynamicCase:
    return dataclasses.replace(
        case,
        samples=samples_override if samples_override is not None else case.samples,
        t_max=t_max_override if t_max_override is not None else case.t_max,
    )


def scan_case(
    case: DynamicCase,
    states: list[np.ndarray],
    high_fidelity_threshold: float,
    tolerance: float,
) -> CaseResult:
    validate_case(case)
    n_sites, adj, parity, _coords = lattice_for_case(case)
    factors = factor_sites(case.dim, case.side)
    H1 = build_H1(n_sites, adj, parity, mass=case.mass)
    poisson = build_poisson(n_sites, adj)
    H2 = build_H2_tensor(H1, poisson, case.G, n_sites)
    evals, evecs = eigh(H2)

    psi0 = np.zeros(n_sites * n_sites, dtype=complex)
    psi0[case.initial_sites[0] * n_sites + case.initial_sites[1]] = 1.0
    coeff = evecs.conj().T @ psi0
    times = np.linspace(0.0, case.t_max, case.samples)

    points: list[TimePoint] = []
    best_rho: np.ndarray | None = None
    best_psi: np.ndarray | None = None
    best_point: TimePoint | None = None

    for t in times:
        psi = evecs @ (np.exp(-1j * evals * t) * coeff)
        amp = amplitudes_by_logical_env(psi, n_sites, factors)
        rho = reduced_logical_resource(amp)
        point = time_point_from_rho(float(t), rho)
        points.append(point)
        if best_point is None or point.bell_overlap > best_point.bell_overlap + 1e-12:
            best_point = point
            best_rho = rho
            best_psi = psi

    assert best_point is not None
    assert best_rho is not None
    assert best_psi is not None

    bell_values = [point.bell_overlap for point in points]
    useful_mask = [
        point.bell_overlap > USEFUL_BELL_THRESHOLD + tolerance for point in points
    ]
    high_mask = [
        point.bell_overlap >= high_fidelity_threshold - tolerance for point in points
    ]
    useful_windows = threshold_windows(points, bell_values, useful_mask)
    high_windows = threshold_windows(points, bell_values, high_mask)

    Z = build_sublattice_Z(n_sites, parity)
    X = build_pair_hop_X(n_sites)
    best_full_chsh, _correlation = chsh_horodecki(best_psi, Z, X, Z, X, n_sites)
    max_neg = max(point.negativity for point in points)
    null_control_ok: bool | None
    if abs(case.G) <= 1e-15:
        null_control_ok = (
            best_point.bell_overlap <= USEFUL_BELL_THRESHOLD + 10.0 * tolerance
            and max_neg <= 10.0 * tolerance
            and len(useful_windows) == 0
            and len(high_windows) == 0
        )
    else:
        null_control_ok = None

    return CaseResult(
        case=case,
        n_sites=n_sites,
        n_env=len(factors.env_labels),
        dt=float(times[1] - times[0]),
        best=best_point,
        best_full_chsh=float(best_full_chsh),
        max_negativity=max_neg,
        useful_windows=useful_windows,
        high_fidelity_windows=high_windows,
        no_signal=no_signal_audit(best_rho, best_point.bell_bits, states),
        null_control_ok=null_control_ok,
    )


def format_window(window: ThresholdWindow | None) -> str:
    if window is None:
        return "none"
    return (
        f"[{window.start:.3f}, {window.end:.3f}] "
        f"peak={window.peak_value:.6f} at t={window.peak_t:.3f} "
        f"({window.samples} samples)"
    )


def best_window(windows: tuple[ThresholdWindow, ...]) -> ThresholdWindow | None:
    if not windows:
        return None
    return max(windows, key=lambda window: window.peak_value)


def print_result_table(
    results: list[CaseResult],
    high_fidelity_threshold: float,
    tolerance: float,
) -> None:
    print("Dynamic resource scan table:")
    print(
        "  "
        f"{'case':25s} {'G':>8s} {'init':>8s} {'best_t':>7s} "
        f"{'Bell*':>8s} {'label':>5s} {'Fmean*':>8s} {'Slog':>7s} "
        f"{'neg':>7s} {'use':>4s} {'high':>5s} {'noSig':>8s}"
    )
    for result in results:
        no_sig_ok = result.no_signal.max_pairwise_no_record_distance <= 10.0 * tolerance
        print(
            "  "
            f"{result.case.label[:25]:25s} "
            f"{result.case.G:8.3g} "
            f"{str(result.case.initial_sites):>8s} "
            f"{result.best.t:7.3f} "
            f"{result.best.bell_overlap:8.6f} "
            f"{result.best.bell_label:>5s} "
            f"{result.best.framed_mean_fidelity:8.6f} "
            f"{result.best.logical_chsh:7.4f} "
            f"{result.best.negativity:7.4f} "
            f"{len(result.useful_windows):4d} "
            f"{len(result.high_fidelity_windows):5d} "
            f"{'pass' if no_sig_ok else 'FAIL':>8s}"
        )
    print(
        f"  useful means Bell* > {USEFUL_BELL_THRESHOLD:.1f} "
        f"(mean fidelity > {CLASSICAL_AVG_FIDELITY:.6f} after fixed Bell-frame alignment)"
    )
    print(f"  high means Bell* >= {high_fidelity_threshold:.3f}")


def print_details(results: list[CaseResult]) -> None:
    print()
    for result in results:
        case = result.case
        null = ""
        if result.null_control_ok is not None:
            null = f", null_control={'PASS' if result.null_control_ok else 'FAIL'}"
        print(f"Case: {case.label}")
        print(
            "  setup: "
            f"dim={case.dim} side={case.side} N={result.n_sites} envs={result.n_env}, "
            f"mass={case.mass:g}, G={case.G:g}, init={case.initial_sites}, "
            f"t=[0,{case.t_max:g}], samples={case.samples}, dt={result.dt:.6g}{null}"
        )
        print(
            "  best candidate: "
            f"t={result.best.t:.6f}, Bell*={result.best.bell_overlap:.6f} "
            f"({result.best.bell_label}), framed mean fidelity="
            f"{result.best.framed_mean_fidelity:.6f}, standard Phi+ mean fidelity="
            f"{result.best.standard_mean_fidelity:.6f}"
        )
        print(
            "  candidate diagnostics: "
            f"logical CHSH={result.best.logical_chsh:.6f}, "
            f"full-state CHSH={result.best_full_chsh:.6f}, "
            f"purity={result.best.purity:.6f}, negativity={result.best.negativity:.6f}, "
            f"max negativity over scan={result.max_negativity:.6f}"
        )
        print(
            "  windows: "
            f"useful={len(result.useful_windows)} best {format_window(best_window(result.useful_windows))}; "
            f"high={len(result.high_fidelity_windows)} best "
            f"{format_window(best_window(result.high_fidelity_windows))}"
        )
        print(
            "  sampled teleportation at best candidate: "
            f"mean/min/max={result.no_signal.sampled_mean_fidelity:.6f}/"
            f"{result.no_signal.sampled_min_fidelity:.6f}/"
            f"{result.no_signal.sampled_max_fidelity:.6f}, "
            f"trace error={result.no_signal.max_trace_error:.3e}"
        )
        print(
            "  Bob before message: "
            f"distance to resource marginal="
            f"{result.no_signal.max_no_record_to_marginal_distance:.3e}, "
            f"pairwise input distance={result.no_signal.max_pairwise_no_record_distance:.3e}, "
            f"marginal bias from I/2={result.no_signal.bob_marginal_bias:.3e}"
        )
        print()


def print_conclusion(results: list[CaseResult], high_fidelity_threshold: float) -> None:
    high_found = any(result.high_fidelity_windows for result in results if result.case.G != 0.0)
    useful_found = any(result.useful_windows for result in results if result.case.G != 0.0)
    null_failures = [result.case.label for result in results if result.null_control_ok is False]
    no_signal_failures = [
        result.case.label
        for result in results
        if result.no_signal.max_pairwise_no_record_distance > 1e-8
    ]

    print("Conclusion:")
    if high_found:
        print(
            f"  At least one interacting product-state trajectory reaches the "
            f"high-fidelity Bell threshold {high_fidelity_threshold:.3f}."
        )
    else:
        print(
            f"  No interacting product-state trajectory in this bounded scan reaches "
            f"the high-fidelity Bell threshold {high_fidelity_threshold:.3f}."
        )
    if useful_found:
        print(
            "  Some interacting trajectories cross the useful teleportation threshold "
            "after fixed Bell-frame alignment, but this is not a high-fidelity resource."
        )
    else:
        print("  No interacting trajectory crosses the useful teleportation threshold.")
    if null_failures:
        print(f"  Null-control failures: {', '.join(null_failures)}")
    else:
        print("  The G=0/null controls stay non-useful in the audited extraction.")
    if no_signal_failures:
        print(f"  No-signaling audit failures: {', '.join(no_signal_failures)}")
    else:
        print("  Bob's pre-message state remains input-independent for every candidate.")
    print("  Scope remains quantum state teleportation only; no transfer of matter or FTL claim.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        choices=[case.label for case in DEFAULT_CASES],
        action="append",
        help="case label to run; omit to run the default bounded audit set",
    )
    parser.add_argument(
        "--samples",
        type=int,
        help="override the number of time samples for every selected case",
    )
    parser.add_argument(
        "--t-max",
        type=float,
        help="override the maximum time for every selected case",
    )
    parser.add_argument(
        "--high-fidelity-threshold",
        type=float,
        default=0.90,
        help="Bell-overlap threshold for a high-fidelity resource window",
    )
    parser.add_argument(
        "--random-inputs",
        type=int,
        default=64,
        help="random qubit inputs for sampled teleportation/no-signaling audit",
    )
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-10,
        help="numerical tolerance for threshold/null/no-signaling checks",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.samples is not None and args.samples < 2:
        raise ValueError("--samples must be at least 2")
    if args.t_max is not None and args.t_max <= 0.0:
        raise ValueError("--t-max must be positive")
    if not (USEFUL_BELL_THRESHOLD < args.high_fidelity_threshold <= 1.0):
        raise ValueError("--high-fidelity-threshold must be in (0.5, 1]")
    if args.random_inputs < 0:
        raise ValueError("--random-inputs must be nonnegative")
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")

    requested = set(args.case or [])
    cases = [
        with_overrides(case, args.samples, args.t_max)
        for case in DEFAULT_CASES
        if not requested or case.label in requested
    ]
    states = probe_states(args.seed, args.random_inputs)

    print("DYNAMIC POISSON TASTE-QUBIT RESOURCE GENERATION")
    print("Status: planning / first artifact; ordinary quantum state teleportation only")
    print("Initial states: simple product site states of two distinguishable species")
    print(
        "Evolution: H = H1 x I + I x H1 + G V_Poisson on a small periodic lattice"
    )
    print(
        "Extraction: trace cells/spectator tastes, keep the last KS taste bit per species"
    )
    print(
        f"Input probes for candidate teleportation checks: {len(states)} "
        f"(6 axis states + {args.random_inputs} random, seed={args.seed})"
    )
    print()

    results = [
        scan_case(
            case,
            states=states,
            high_fidelity_threshold=args.high_fidelity_threshold,
            tolerance=args.tolerance,
        )
        for case in cases
    ]

    print_result_table(results, args.high_fidelity_threshold, args.tolerance)
    print_details(results)
    print_conclusion(results, args.high_fidelity_threshold)
    return 0


if __name__ == "__main__":
    sys.exit(main())
