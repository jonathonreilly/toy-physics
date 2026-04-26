#!/usr/bin/env python3
"""Bounded non-ideal Bell-resource teleportation-fidelity harness.

Status: planning / first artifact. This runner tests ordinary quantum state
teleportation with imperfect or arbitrary two-qubit resource density matrices.
It does not claim matter teleportation, mass transfer, charge transfer, or
faster-than-light transport.

The protocol is the standard three-qubit teleportation circuit:

    A = Alice unknown qubit
    R = Alice resource half
    B = Bob resource half

Alice measures A,R in the Bell basis, sends two classical bits, and Bob applies
Z^z X^x. The harness keeps the measurement and correction ideal so the only
object under stress is the shared two-qubit resource rho_RB.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import math
import sys
from pathlib import Path
from collections.abc import Callable, Iterable

import numpy as np


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
CLASSICAL_AVG_FIDELITY = 2.0 / 3.0


@dataclasses.dataclass(frozen=True)
class DensityChecks:
    trace_error: float
    hermitian_error: float
    min_eigenvalue: float
    valid: bool


@dataclasses.dataclass(frozen=True)
class ResourceDiagnostics:
    label: str
    checks: DensityChecks
    phi_plus_overlap: float
    max_bell_overlap: float
    max_bell_label: str
    exact_avg_fidelity: float
    predicted_avg_fidelity: float
    sampled_avg_fidelity: float
    sampled_min_fidelity: float
    sampled_max_fidelity: float
    negativity: float
    chsh_smax: float
    bob_bias_trace_distance: float
    max_no_record_change: float
    max_pairwise_no_record_distance: float
    max_branch_probability_span: float
    max_trace_error_after_correction: float

    @property
    def verdict(self) -> str:
        margin = self.exact_avg_fidelity - CLASSICAL_AVG_FIDELITY
        if margin > 1e-10:
            return "beats 2/3"
        if abs(margin) <= 1e-10:
            return "at 2/3"
        return "below 2/3"


def normalize_state(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm


def projector(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


def hermitian_part(matrix: np.ndarray) -> np.ndarray:
    return 0.5 * (matrix + matrix.conj().T)


def clean_density_matrix(rho: np.ndarray) -> np.ndarray:
    rho = hermitian_part(np.asarray(rho, dtype=complex))
    trace = np.trace(rho)
    if abs(trace) <= 1e-15:
        raise ValueError("density matrix trace is zero")
    return rho / trace


def density_checks(rho: np.ndarray, tolerance: float) -> DensityChecks:
    trace_error = float(abs(np.trace(rho) - 1.0))
    hermitian_error = float(np.max(np.abs(rho - rho.conj().T)))
    eigvals = np.linalg.eigvalsh(hermitian_part(rho))
    min_eigenvalue = float(np.min(eigvals))
    valid = (
        trace_error <= tolerance
        and hermitian_error <= tolerance
        and min_eigenvalue >= -tolerance
    )
    return DensityChecks(
        trace_error=trace_error,
        hermitian_error=hermitian_error,
        min_eigenvalue=min_eigenvalue,
        valid=valid,
    )


def bell_state(z_bit: int, x_bit: int) -> np.ndarray:
    """Bell state |Bell(z,x)> with x=bit-flip and z=phase bit."""
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


def partial_transpose_two_qubit(rho: np.ndarray, system: int) -> np.ndarray:
    if system not in (0, 1):
        raise ValueError("system must be 0 or 1")
    tensor = rho.reshape(2, 2, 2, 2)
    tensor = np.swapaxes(tensor, system, system + 2)
    return tensor.reshape(4, 4)


def trace_distance(first: np.ndarray, second: np.ndarray) -> float:
    diff = hermitian_part(first - second)
    eigvals = np.linalg.eigvalsh(diff)
    return float(0.5 * np.sum(np.abs(eigvals)))


def pure_state_fidelity(state: np.ndarray, rho: np.ndarray) -> float:
    value = np.vdot(state, rho @ state)
    return float(np.clip(np.real(value), 0.0, 1.0))


def random_qubit(rng: np.random.Generator) -> np.ndarray:
    return normalize_state(rng.standard_normal(2) + 1j * rng.standard_normal(2))


def probe_states(rng: np.random.Generator, n_random: int) -> list[np.ndarray]:
    base = [
        np.array([1, 0], dtype=complex),
        np.array([0, 1], dtype=complex),
        normalize_state(np.array([1, 1], dtype=complex)),
        normalize_state(np.array([1, -1], dtype=complex)),
        normalize_state(np.array([1, 1j], dtype=complex)),
        normalize_state(np.array([1, -1j], dtype=complex)),
    ]
    base.extend(random_qubit(rng) for _ in range(n_random))
    return base


def teleport_density(
    input_rho: np.ndarray, resource_rho: np.ndarray
) -> tuple[np.ndarray, np.ndarray, dict[tuple[int, int], float]]:
    """Return corrected Bob state, Bob no-record state, and branch probabilities."""
    joint = np.kron(input_rho, resource_rho)
    corrected_output = np.zeros((2, 2), dtype=complex)
    no_record_output = np.zeros((2, 2), dtype=complex)
    branch_probabilities: dict[tuple[int, int], float] = {}

    for z_bit, x_bit in OUTCOME_ORDER:
        projector_ar = bell_projector(z_bit, x_bit)
        measurement = np.kron(projector_ar, I2)
        branch = measurement @ joint @ measurement
        bob_unnormalized = partial_trace(branch, dims=[2, 2, 2], keep=[2])
        probability = float(np.real(np.trace(bob_unnormalized)))
        branch_probabilities[(z_bit, x_bit)] = probability
        no_record_output += bob_unnormalized

        correction = correction_operator(z_bit, x_bit)
        corrected_output += correction @ bob_unnormalized @ correction.conj().T

    return corrected_output, no_record_output, branch_probabilities


def teleport_channel_apply(input_op: np.ndarray, resource_rho: np.ndarray) -> np.ndarray:
    corrected_output, _, _ = teleport_density(input_op, resource_rho)
    return corrected_output


def choi_matrix(resource_rho: np.ndarray) -> np.ndarray:
    choi = np.zeros((4, 4), dtype=complex)
    for row in range(2):
        for col in range(2):
            basis_op = np.zeros((2, 2), dtype=complex)
            basis_op[row, col] = 1.0
            choi += 0.5 * np.kron(basis_op, teleport_channel_apply(basis_op, resource_rho))
    return choi


def exact_average_fidelity(resource_rho: np.ndarray) -> float:
    choi = choi_matrix(resource_rho)
    phi = bell_state(0, 0)
    entanglement_fidelity = float(np.real(np.vdot(phi, choi @ phi)))
    return float((2.0 * entanglement_fidelity + 1.0) / 3.0)


def bell_overlaps(resource_rho: np.ndarray) -> dict[tuple[int, int], float]:
    overlaps: dict[tuple[int, int], float] = {}
    for z_bit, x_bit in OUTCOME_ORDER:
        bell = bell_state(z_bit, x_bit)
        overlaps[(z_bit, x_bit)] = float(np.real(np.vdot(bell, resource_rho @ bell)))
    return overlaps


def negativity(resource_rho: np.ndarray) -> float:
    eigvals = np.linalg.eigvalsh(hermitian_part(partial_transpose_two_qubit(resource_rho, 1)))
    return float(np.sum(np.abs(eigvals[eigvals < 0.0])))


def chsh_smax(resource_rho: np.ndarray) -> float:
    correlation = np.zeros((3, 3), dtype=float)
    for i, left in enumerate(PAULIS):
        for j, right in enumerate(PAULIS):
            correlation[i, j] = float(np.real(np.trace(resource_rho @ np.kron(left, right))))
    eigvals = np.linalg.eigvalsh(correlation.T @ correlation)
    two_largest = np.sort(eigvals)[-2:]
    return float(2.0 * math.sqrt(max(0.0, float(np.sum(two_largest)))))


def evaluate_resource(
    label: str,
    resource_rho: np.ndarray,
    states: list[np.ndarray],
    tolerance: float,
) -> ResourceDiagnostics:
    checks = density_checks(resource_rho, tolerance)
    if not checks.valid:
        raise ValueError(
            f"{label} is not a valid density matrix: "
            f"trace_error={checks.trace_error:.3e}, "
            f"hermitian_error={checks.hermitian_error:.3e}, "
            f"min_eigenvalue={checks.min_eigenvalue:.3e}"
        )

    overlaps = bell_overlaps(resource_rho)
    phi_plus_overlap = overlaps[(0, 0)]
    max_bell_bits = max(overlaps, key=overlaps.__getitem__)
    max_bell_overlap = overlaps[max_bell_bits]
    predicted_avg = (1.0 + 2.0 * phi_plus_overlap) / 3.0
    exact_avg = exact_average_fidelity(resource_rho)
    bob_marginal = partial_trace(resource_rho, dims=[2, 2], keep=[1])

    fidelities: list[float] = []
    branch_probabilities: dict[tuple[int, int], list[float]] = {
        outcome: [] for outcome in OUTCOME_ORDER
    }
    no_record_reference: np.ndarray | None = None
    max_no_record_change = 0.0
    max_pairwise_no_record_distance = 0.0
    max_trace_error_after_correction = 0.0

    for state in states:
        input_rho = projector(state)
        corrected, no_record, probabilities = teleport_density(input_rho, resource_rho)
        fidelities.append(pure_state_fidelity(state, corrected))
        max_trace_error_after_correction = max(
            max_trace_error_after_correction,
            float(abs(np.trace(corrected) - 1.0)),
        )
        max_no_record_change = max(
            max_no_record_change, trace_distance(no_record, bob_marginal)
        )
        if no_record_reference is None:
            no_record_reference = no_record
        else:
            max_pairwise_no_record_distance = max(
                max_pairwise_no_record_distance,
                trace_distance(no_record, no_record_reference),
            )
        for outcome, probability in probabilities.items():
            branch_probabilities[outcome].append(probability)

    max_branch_probability_span = max(
        max(values) - min(values) for values in branch_probabilities.values()
    )

    return ResourceDiagnostics(
        label=label,
        checks=checks,
        phi_plus_overlap=phi_plus_overlap,
        max_bell_overlap=max_bell_overlap,
        max_bell_label=OUTCOME_LABELS[max_bell_bits],
        exact_avg_fidelity=exact_avg,
        predicted_avg_fidelity=predicted_avg,
        sampled_avg_fidelity=float(np.mean(fidelities)),
        sampled_min_fidelity=float(np.min(fidelities)),
        sampled_max_fidelity=float(np.max(fidelities)),
        negativity=negativity(resource_rho),
        chsh_smax=chsh_smax(resource_rho),
        bob_bias_trace_distance=trace_distance(bob_marginal, 0.5 * I2),
        max_no_record_change=max_no_record_change,
        max_pairwise_no_record_distance=max_pairwise_no_record_distance,
        max_branch_probability_span=max_branch_probability_span,
        max_trace_error_after_correction=max_trace_error_after_correction,
    )


def ideal_bell_resource() -> np.ndarray:
    return projector(bell_state(0, 0))


def isotropic_resource(visibility: float) -> np.ndarray:
    if not 0.0 <= visibility <= 1.0:
        raise ValueError("visibility must lie in [0, 1]")
    return visibility * ideal_bell_resource() + (1.0 - visibility) * np.eye(4) / 4.0


def bell_dephased_resource(phase_flip_probability: float) -> np.ndarray:
    if not 0.0 <= phase_flip_probability <= 1.0:
        raise ValueError("phase flip probability must lie in [0, 1]")
    return (
        (1.0 - phase_flip_probability) * projector(bell_state(0, 0))
        + phase_flip_probability * projector(bell_state(1, 0))
    )


def coherent_bell_axis_resource(theta: float) -> np.ndarray:
    state = math.cos(theta) * bell_state(0, 0) + math.sin(theta) * bell_state(1, 0)
    return projector(normalize_state(state))


def amplitude_damping_kraus(gamma: float) -> tuple[np.ndarray, np.ndarray]:
    if not 0.0 <= gamma <= 1.0:
        raise ValueError("gamma must lie in [0, 1]")
    return (
        np.array([[1.0, 0.0], [0.0, math.sqrt(1.0 - gamma)]], dtype=complex),
        np.array([[0.0, math.sqrt(gamma)], [0.0, 0.0]], dtype=complex),
    )


def apply_local_kraus(
    resource_rho: np.ndarray,
    left_kraus: Iterable[np.ndarray],
    right_kraus: Iterable[np.ndarray],
) -> np.ndarray:
    output = np.zeros_like(resource_rho, dtype=complex)
    for left in left_kraus:
        for right in right_kraus:
            op = np.kron(left, right)
            output += op @ resource_rho @ op.conj().T
    return clean_density_matrix(output)


def amplitude_damped_resource(gamma: float, both_halves: bool) -> np.ndarray:
    kraus = amplitude_damping_kraus(gamma)
    identity_channel = (I2,)
    if both_halves:
        return apply_local_kraus(ideal_bell_resource(), kraus, kraus)
    return apply_local_kraus(ideal_bell_resource(), identity_channel, kraus)


def random_density_matrix(rng: np.random.Generator, dim: int = 4) -> np.ndarray:
    matrix = rng.standard_normal((dim, dim)) + 1j * rng.standard_normal((dim, dim))
    rho = matrix @ matrix.conj().T
    return clean_density_matrix(rho)


def parse_complex_scalar(value: object) -> complex:
    if isinstance(value, (int, float)):
        return complex(float(value), 0.0)
    if isinstance(value, str):
        return complex(value.replace("i", "j"))
    if isinstance(value, list) and len(value) == 2:
        return complex(float(value[0]), float(value[1]))
    if isinstance(value, dict):
        return complex(float(value.get("re", 0.0)), float(value.get("im", 0.0)))
    raise TypeError(f"unsupported complex scalar encoding: {value!r}")


def load_density_matrix_json(path: Path) -> np.ndarray:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    matrix = np.array(
        [[parse_complex_scalar(value) for value in row] for row in data],
        dtype=complex,
    )
    if matrix.shape != (4, 4):
        raise ValueError(f"custom resource must be a 4x4 matrix, got {matrix.shape}")
    return matrix


def resource_suite(
    rng: np.random.Generator,
    random_resource_count: int,
    custom_matrix_path: Path | None,
) -> list[tuple[str, np.ndarray]]:
    resources = [
        ("ideal Phi+ resource", ideal_bell_resource()),
        ("isotropic v=0.90", isotropic_resource(0.90)),
        ("isotropic v=1/sqrt(2)", isotropic_resource(1.0 / math.sqrt(2.0))),
        ("isotropic v=1/3 boundary", isotropic_resource(1.0 / 3.0)),
        ("isotropic v=0.30", isotropic_resource(0.30)),
        ("Bell phase-flip p=0.25", bell_dephased_resource(0.25)),
        ("Bell phase-flip p=0.50 boundary", bell_dephased_resource(0.50)),
        ("coherent Bell-axis theta=pi/8", coherent_bell_axis_resource(math.pi / 8.0)),
        (
            "coherent Bell-axis theta=pi/4 boundary",
            coherent_bell_axis_resource(math.pi / 4.0),
        ),
        ("amplitude damping both gamma=0.20", amplitude_damped_resource(0.20, True)),
        ("amplitude damping both gamma=0.50", amplitude_damped_resource(0.50, True)),
        ("amplitude damping Bob gamma=0.50", amplitude_damped_resource(0.50, False)),
    ]
    for index in range(random_resource_count):
        resources.append((f"random two-qubit rho #{index + 1}", random_density_matrix(rng)))
    if custom_matrix_path is not None:
        resources.append(
            (
                f"custom rho from {custom_matrix_path}",
                load_density_matrix_json(custom_matrix_path),
            )
        )
    return resources


def bisection_threshold(
    fidelity_at: Callable[[float], float],
    low: float = 0.0,
    high: float = 1.0,
    iterations: int = 80,
) -> float | None:
    low_margin = fidelity_at(low) - CLASSICAL_AVG_FIDELITY
    high_margin = fidelity_at(high) - CLASSICAL_AVG_FIDELITY
    if low_margin < 0.0 or high_margin > 0.0:
        return None
    for _ in range(iterations):
        middle = 0.5 * (low + high)
        margin = fidelity_at(middle) - CLASSICAL_AVG_FIDELITY
        if margin >= 0.0:
            low = middle
        else:
            high = middle
    return low


def print_resource_table(diagnostics: list[ResourceDiagnostics]) -> None:
    print("Resource diagnostics:")
    print(
        "  "
        f"{'resource':42s} {'F_avg':>9s} {'F_min':>9s} {'p_Phi+':>9s} "
        f"{'p_Bell*':>9s} {'neg':>9s} {'S_CHSH':>8s} {'BobBias':>9s} "
        f"{'noSig':>9s} {'branchSpan':>10s} {'verdict':>10s}"
    )
    for item in diagnostics:
        print(
            "  "
            f"{item.label[:42]:42s} "
            f"{item.exact_avg_fidelity:9.6f} "
            f"{item.sampled_min_fidelity:9.6f} "
            f"{item.phi_plus_overlap:9.6f} "
            f"{item.max_bell_overlap:9.6f} "
            f"{item.negativity:9.3e} "
            f"{item.chsh_smax:8.5f} "
            f"{item.bob_bias_trace_distance:9.3e} "
            f"{item.max_pairwise_no_record_distance:9.3e} "
            f"{item.max_branch_probability_span:10.3e} "
            f"{item.verdict:>10s}"
        )
    print()
    print("  p_Bell* is only the best overlap among the four Bell labels, not a full")
    print("  local-unitary optimization. noSig is sampled pairwise Bob-state distance")
    print("  before the classical Bell record is available.")


def print_thresholds(diagnostics: list[ResourceDiagnostics]) -> None:
    amplitude_both_threshold = bisection_threshold(
        lambda gamma: exact_average_fidelity(amplitude_damped_resource(gamma, True))
    )
    amplitude_bob_threshold = bisection_threshold(
        lambda gamma: exact_average_fidelity(amplitude_damped_resource(gamma, False))
    )
    formula_error = max(
        abs(item.exact_avg_fidelity - item.predicted_avg_fidelity)
        for item in diagnostics
    )
    random_items = [item for item in diagnostics if item.label.startswith("random two-qubit")]
    random_above = sum(
        item.exact_avg_fidelity > CLASSICAL_AVG_FIDELITY + 1e-10
        for item in random_items
    )

    print("Thresholds and limitations:")
    print(f"  classical qubit average-fidelity benchmark: {CLASSICAL_AVG_FIDELITY:.10f}")
    print("  fixed Bell-basis protocol uses F_avg = (1 + 2 * <Phi+|rho|Phi+>) / 3")
    print("  fixed-protocol quantum-useful threshold: <Phi+|rho|Phi+> > 0.5")
    print("  isotropic rho(v)=v|Phi+><Phi+|+(1-v)I/4 threshold: v > 1/3")
    print(f"  isotropic CHSH Horodecki threshold: v > {1.0 / math.sqrt(2.0):.10f}")
    if amplitude_both_threshold is not None:
        print(
            "  amplitude damping on both halves numeric fixed-protocol threshold: "
            f"gamma < {amplitude_both_threshold:.10f}"
        )
    if amplitude_bob_threshold is not None:
        print(
            "  amplitude damping on Bob half numeric fixed-protocol threshold: "
            f"gamma < {amplitude_bob_threshold:.10f}"
        )
    print(
        "  max exact-vs-Bell-overlap formula error in this run: "
        f"{formula_error:.3e}"
    )
    if random_items:
        print(
            "  random arbitrary resources beating 2/3 in this seed: "
            f"{random_above}/{len(random_items)}"
        )
    print("  Bell relabeling may rescue a resource whose largest Bell overlap is not Phi+;")
    print("  this first harness reports that limitation but does not optimize measurements.")


def print_no_signaling_summary(diagnostics: list[ResourceDiagnostics]) -> None:
    max_no_record_change = max(item.max_no_record_change for item in diagnostics)
    max_pairwise = max(item.max_pairwise_no_record_distance for item in diagnostics)
    max_branch_span = max(item.max_branch_probability_span for item in diagnostics)
    max_bob_bias = max(item.bob_bias_trace_distance for item in diagnostics)

    print("No-signaling diagnostics:")
    print(
        "  max trace distance between Bob no-record state and resource Bob marginal: "
        f"{max_no_record_change:.3e}"
    )
    print(
        "  max pairwise Bob no-record distance across sampled inputs: "
        f"{max_pairwise:.3e}"
    )
    print(
        "  max Bob marginal bias from I/2 across resources: "
        f"{max_bob_bias:.3e}"
    )
    print(
        "  max Bell-outcome probability span across sampled inputs: "
        f"{max_branch_span:.3e}"
    )
    print("  A biased Bob marginal or input-dependent Alice outcome distribution is")
    print("  not a pre-message signaling channel; Bob lacks Alice's two-bit record.")


def print_acceptance_gates(
    diagnostics: list[ResourceDiagnostics],
    tolerance: float,
) -> bool:
    by_label = {item.label: item for item in diagnostics}
    ideal = by_label["ideal Phi+ resource"]
    below = by_label["isotropic v=0.30"]
    boundary = by_label["isotropic v=1/3 boundary"]
    above = by_label["isotropic v=0.90"]
    max_formula_error = max(
        abs(item.exact_avg_fidelity - item.predicted_avg_fidelity)
        for item in diagnostics
    )
    max_pairwise = max(item.max_pairwise_no_record_distance for item in diagnostics)
    max_no_record_change = max(item.max_no_record_change for item in diagnostics)
    max_trace_error = max(item.max_trace_error_after_correction for item in diagnostics)

    gates = {
        "all resource matrices physical": all(item.checks.valid for item in diagnostics),
        "ideal resource fidelity": abs(ideal.exact_avg_fidelity - 1.0) <= 10 * tolerance,
        "fixed Bell-overlap formula": max_formula_error <= 10 * tolerance,
        "isotropic threshold bracket": (
            below.exact_avg_fidelity < CLASSICAL_AVG_FIDELITY
            and abs(boundary.exact_avg_fidelity - CLASSICAL_AVG_FIDELITY) <= 10 * tolerance
            and above.exact_avg_fidelity > CLASSICAL_AVG_FIDELITY
        ),
        "Bob pre-message input-independence": (
            max_pairwise <= 10 * tolerance and max_no_record_change <= 10 * tolerance
        ),
        "corrected channel trace preservation": max_trace_error <= 10 * tolerance,
    }

    print("Acceptance gates:")
    for name, ok in gates.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print()
    print("Claim boundary:")
    print("  This is quantum state teleportation on a two-qubit resource only.")
    print("  It is not matter teleportation, mass transfer, charge transfer, or FTL transport.")
    return all(gates.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=128, help="number of random input states")
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument(
        "--random-resources",
        type=int,
        default=4,
        help="number of arbitrary random two-qubit density matrices to include",
    )
    parser.add_argument(
        "--matrix-json",
        type=Path,
        default=None,
        help=(
            "optional 4x4 resource density matrix JSON; entries may be numbers, "
            "[re, im], strings accepted by complex(), or {'re': ..., 'im': ...}"
        ),
    )
    parser.add_argument("--tolerance", type=float, default=1e-10, help="pass/fail tolerance")
    args = parser.parse_args()

    if args.trials <= 0:
        raise ValueError("--trials must be positive")
    if args.random_resources < 0:
        raise ValueError("--random-resources must be non-negative")
    if args.tolerance <= 0:
        raise ValueError("--tolerance must be positive")

    rng = np.random.default_rng(args.seed)
    states = probe_states(rng, args.trials)
    resources = resource_suite(rng, args.random_resources, args.matrix_json)
    diagnostics = [
        evaluate_resource(label, resource, states, args.tolerance)
        for label, resource in resources
    ]

    print("BOUNDED NON-IDEAL BELL-RESOURCE TELEPORTATION-FIDELITY HARNESS")
    print("Status: planning / first artifact; quantum state teleportation only")
    print(f"Random input states: {args.trials} plus 6 Pauli-axis probes (seed={args.seed})")
    print(f"Random arbitrary resource matrices: {args.random_resources}")
    print()

    print_resource_table(diagnostics)
    print()
    print_thresholds(diagnostics)
    print()
    print_no_signaling_summary(diagnostics)
    print()

    ok = print_acceptance_gates(diagnostics, args.tolerance)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
