#!/usr/bin/env python3
"""3D operator-consistent Poisson-backed teleportation audit.

Status: planning / first artifact. This runner extends the retained-axis
operator-consistent end-to-end audit to a small 3D spatial Poisson resource
case with one directed classical/causal record.

The audited convention is unchanged:

1. trace cells and spectator tastes, retaining the last KS taste bit;
2. use retained-axis logical Z/X for Bell readout and Bob correction;
3. reject raw sublattice parity Z=xi_5 as a traced retained-bit Z in 3D;
4. report fixed-Phi+ protocol failures honestly, while also checking whether
   a known retained-axis Bell-frame correction turns the 3D resource into a
   usable ordinary quantum state teleportation resource.

This is ordinary quantum state teleportation planning only. It does not claim
matter teleportation, mass transfer, charge transfer, energy transfer, object
transport, or faster-than-light signaling.
"""

from __future__ import annotations

import argparse
import dataclasses
import sys
from pathlib import Path
from typing import Iterable

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_teleportation_end_to_end_poisson import (  # noqa: E402
    branch_bob_unnormalized,
    causal_record_demo,
    projector,
    probe_states,
)
from frontier_teleportation_operator_consistent_end_to_end import (  # noqa: E402
    OperatorConventionAudit,
    audit_operator_convention,
    fmt_float,
    operator_guard_passes,
    pair_guard_passes,
    status,
)
from frontier_teleportation_resource_fidelity import (  # noqa: E402
    I2,
    correction_operator,
    density_checks,
    exact_average_fidelity,
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
    best_bell_overlap,
    factor_sites,
    ground_state_resource,
    negativity,
    reduced_logical_resource,
    two_qubit_chsh,
)


BELL_BITS_BY_LABEL = {label: bits for bits, label in OUTCOME_LABELS.items()}
THREE_D_DIM = 3


@dataclasses.dataclass(frozen=True)
class ExtractedResource:
    case: AuditCase
    rho: np.ndarray
    n_sites: int
    n_env: int
    ground_energy: float
    full_chsh: float
    logical_chsh: float
    negativity: float
    raw_best_bell_overlap: float
    raw_best_bell_label: str


@dataclasses.dataclass(frozen=True)
class ProtocolRow:
    case: AuditCase
    row_label: str
    frame_label: str
    frame_bits: tuple[int, int]
    n_sites: int
    n_env: int
    ground_energy: float
    full_chsh: float
    logical_chsh: float
    resource_negativity: float
    raw_best_bell_overlap: float
    raw_best_bell_label: str
    best_bell_overlap: float
    best_bell_label: str
    phi_plus_overlap: float
    exact_avg_fidelity: float
    sampled_mean_fidelity: float
    sampled_min_fidelity: float
    sampled_max_fidelity: float
    min_branch_fidelity: float
    max_branch_fidelity: float
    min_branch_probability: float
    max_branch_probability: float
    max_trace_error: float
    max_no_record_to_marginal_distance: float
    max_pairwise_no_record_distance: float
    bob_marginal_bias: float
    outcomes_seen: tuple[str, ...]
    causal_record_ok: bool
    early_delivery_blocked: bool
    delivered_once: bool
    delivered_record_label: str
    delivered_record_fidelity: float

    @property
    def non_null(self) -> bool:
        return abs(self.case.G) > 1e-15

    @property
    def all_outcomes_seen(self) -> bool:
        return set(self.outcomes_seen) == {OUTCOME_LABELS[outcome] for outcome in OUTCOME_ORDER}


def parse_csv_floats(raw: str) -> tuple[float, ...]:
    values: list[float] = []
    for item in raw.split(","):
        stripped = item.strip()
        if stripped:
            values.append(float(stripped))
    if not values:
        raise argparse.ArgumentTypeError("expected at least one numeric value")
    return tuple(values)


def bob_frame_resource(resource_rho: np.ndarray, frame_bits: tuple[int, int]) -> np.ndarray:
    if frame_bits == (0, 0):
        return resource_rho.copy()
    frame = correction_operator(*frame_bits).conj().T
    transform = np.kron(I2, frame)
    return transform @ resource_rho @ transform.conj().T


def extract_3d_resource(case: AuditCase) -> ExtractedResource:
    resource = ground_state_resource(case)
    n_sites = int(resource["n"])
    factors = factor_sites(case.dim, case.side)
    amp = amplitudes_by_logical_env(resource["psi"], n_sites, factors)
    rho = reduced_logical_resource(amp)
    raw_best_overlap, raw_best_label = best_bell_overlap(rho)
    return ExtractedResource(
        case=case,
        rho=rho,
        n_sites=n_sites,
        n_env=len(factors.env_labels),
        ground_energy=float(resource["ground_energy"]),
        full_chsh=float(resource["full_chsh"]),
        logical_chsh=two_qubit_chsh(rho),
        negativity=negativity(rho),
        raw_best_bell_overlap=raw_best_overlap,
        raw_best_bell_label=raw_best_label,
    )


def phi_plus_overlap(resource_rho: np.ndarray) -> float:
    state = np.array([1.0, 0.0, 0.0, 1.0], dtype=complex) / np.sqrt(2.0)
    return float(np.real(np.vdot(state, resource_rho @ state)))


def evaluate_protocol_row(
    extracted: ExtractedResource,
    row_label: str,
    frame_label: str,
    frame_bits: tuple[int, int],
    states: list[np.ndarray],
    seed: int,
    tolerance: float,
    probability_floor: float,
) -> ProtocolRow:
    resource_rho = bob_frame_resource(extracted.rho, frame_bits)
    checks = density_checks(resource_rho, tolerance)
    if not checks.valid:
        raise ValueError(
            f"{row_label} framed resource is not a valid density matrix: "
            f"trace_error={checks.trace_error:.3e}, "
            f"hermitian_error={checks.hermitian_error:.3e}, "
            f"min_eigenvalue={checks.min_eigenvalue:.3e}"
        )

    bob_marginal = partial_trace(resource_rho, dims=[2, 2], keep=[1])
    half_identity = 0.5 * I2
    reference_no_record: np.ndarray | None = None

    fidelities: list[float] = []
    branch_fidelities: list[float] = []
    branch_probabilities: list[float] = []
    outcomes_seen: set[str] = set()
    max_trace_error = 0.0
    max_no_record_to_marginal = 0.0
    max_pairwise_no_record = 0.0

    for input_state in states:
        input_rho = projector(input_state)
        corrected, no_record, probabilities = teleport_density(input_rho, resource_rho)
        fidelities.append(pure_state_fidelity(input_state, corrected))
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

        for outcome, probability in probabilities.items():
            branch_probabilities.append(probability)
            if probability <= probability_floor:
                continue
            outcomes_seen.add(OUTCOME_LABELS[outcome])
            branch = branch_bob_unnormalized(input_rho, resource_rho, *outcome)
            branch_rho = branch / probability
            correction = correction_operator(*outcome)
            corrected_branch = correction @ branch_rho @ correction.conj().T
            branch_fidelities.append(pure_state_fidelity(input_state, corrected_branch))

    reference_rng = np.random.default_rng(seed + 10_000)
    record_input = (
        reference_rng.standard_normal(2) + 1j * reference_rng.standard_normal(2)
    )
    record_input = record_input / np.linalg.norm(record_input)
    causal_ok, early_blocked, delivered_once, record_label, delivered_fidelity = causal_record_demo(
        record_input,
        resource_rho,
        probability_floor,
    )

    best_overlap, best_label = best_bell_overlap(resource_rho)
    return ProtocolRow(
        case=extracted.case,
        row_label=row_label,
        frame_label=frame_label,
        frame_bits=frame_bits,
        n_sites=extracted.n_sites,
        n_env=extracted.n_env,
        ground_energy=extracted.ground_energy,
        full_chsh=extracted.full_chsh,
        logical_chsh=two_qubit_chsh(resource_rho),
        resource_negativity=negativity(resource_rho),
        raw_best_bell_overlap=extracted.raw_best_bell_overlap,
        raw_best_bell_label=extracted.raw_best_bell_label,
        best_bell_overlap=best_overlap,
        best_bell_label=best_label,
        phi_plus_overlap=phi_plus_overlap(resource_rho),
        exact_avg_fidelity=exact_average_fidelity(resource_rho),
        sampled_mean_fidelity=float(np.mean(fidelities)),
        sampled_min_fidelity=float(np.min(fidelities)),
        sampled_max_fidelity=float(np.max(fidelities)),
        min_branch_fidelity=float(np.min(branch_fidelities)) if branch_fidelities else 0.0,
        max_branch_fidelity=float(np.max(branch_fidelities)) if branch_fidelities else 0.0,
        min_branch_probability=float(np.min(branch_probabilities)),
        max_branch_probability=float(np.max(branch_probabilities)),
        max_trace_error=max_trace_error,
        max_no_record_to_marginal_distance=max_no_record_to_marginal,
        max_pairwise_no_record_distance=max_pairwise_no_record,
        bob_marginal_bias=trace_distance(bob_marginal, half_identity),
        outcomes_seen=tuple(sorted(outcomes_seen)),
        causal_record_ok=causal_ok,
        early_delivery_blocked=early_blocked,
        delivered_once=delivered_once,
        delivered_record_label=record_label,
        delivered_record_fidelity=delivered_fidelity,
    )


def protocol_passes(row: ProtocolRow, fidelity_threshold: float, tolerance: float) -> bool:
    return bool(
        row.best_bell_label == "Phi+"
        and row.best_bell_overlap >= fidelity_threshold
        and row.phi_plus_overlap >= fidelity_threshold
        and row.exact_avg_fidelity >= fidelity_threshold
        and row.sampled_min_fidelity >= fidelity_threshold
        and row.min_branch_fidelity >= fidelity_threshold
        and row.all_outcomes_seen
        and row.max_no_record_to_marginal_distance < tolerance
        and row.max_pairwise_no_record_distance < tolerance
        and row.max_trace_error < 10 * tolerance
        and row.causal_record_ok
        and row.delivered_record_fidelity >= fidelity_threshold
    )


def case_label(side: int, mass: float, G: float) -> str:
    if abs(G) <= 1e-15:
        return f"3d_side{side}_null"
    return f"3d_side{side}_poisson_G{G:g}_m{mass:g}"


def build_cases(side: int, mass: float, candidate_g: Iterable[float]) -> tuple[AuditCase, ...]:
    cases = [AuditCase(case_label(side, mass, 0.0), dim=THREE_D_DIM, side=side, mass=mass, G=0.0)]
    for G in candidate_g:
        if abs(G) <= 1e-15:
            continue
        cases.append(
            AuditCase(case_label(side, mass, G), dim=THREE_D_DIM, side=side, mass=mass, G=G)
        )
    return tuple(cases)


def print_operator_summary(audit: OperatorConventionAudit, tolerance: float) -> None:
    axis_bell_ok = all(pair_guard_passes(item, tolerance) for item in audit.axis_bell_projectors)
    raw_bell_ok = all(pair_guard_passes(item, tolerance) for item in audit.raw_bell_projectors)
    raw_bell_residual = max(item.relative_residual for item in audit.raw_bell_projectors)
    raw_bell_expected = max(
        0.0 if item.expected_error is None else item.expected_error
        for item in audit.raw_bell_projectors
    )

    print("3D operator-consistency guards:")
    print(
        "  "
        f"surface=3D side={audit.side}, retained_axis={audit.retained_axis}, "
        f"sites={audit.n_sites}, envs={audit.n_env}"
    )
    print(
        "  "
        f"retained-axis Z={status(operator_guard_passes(audit.axis_z, tolerance))} "
        f"rel={fmt_float(audit.axis_z.relative_residual)} "
        f"expected_err={fmt_float(audit.axis_z.expected_error or 0.0)}"
    )
    print(
        "  "
        f"retained-axis X={status(operator_guard_passes(audit.axis_x, tolerance))} "
        f"rel={fmt_float(audit.axis_x.relative_residual)} "
        f"expected_err={fmt_float(audit.axis_x.expected_error or 0.0)}"
    )
    print(f"  retained-axis Bell projectors={status(axis_bell_ok)}")
    print(
        "  "
        f"raw xi_5 as retained-bit Z={status(operator_guard_passes(audit.raw_z, tolerance))} "
        f"rel={fmt_float(audit.raw_z.relative_residual)} "
        f"expected_err={fmt_float(audit.raw_z.expected_error or 0.0)}"
    )
    print(
        "  "
        f"raw-Z/fixed-X Bell projectors={status(raw_bell_ok)} "
        f"max_rel={fmt_float(raw_bell_residual)} "
        f"max_expected_err={fmt_float(raw_bell_expected)}"
    )
    print()


def print_case_table(rows: list[ProtocolRow], fidelity_threshold: float, tolerance: float) -> None:
    print("3D retained-axis end-to-end rows:")
    print(
        "  "
        f"{'case':24s} {'frame':12s} {'raw*':>8s} {'raw':>5s} "
        f"{'Bell*':>8s} {'label':>5s} {'Phi+':>8s} {'Favg':>8s} "
        f"{'Fmin':>8s} {'Bmin':>8s} {'noSig':>9s} {'out':>4s} {'pass':>5s}"
    )
    for row in rows:
        ok = protocol_passes(row, fidelity_threshold, tolerance)
        print(
            "  "
            f"{row.case.label[:24]:24s} "
            f"{row.frame_label[:12]:12s} "
            f"{row.raw_best_bell_overlap:8.5f} "
            f"{row.raw_best_bell_label:>5s} "
            f"{row.best_bell_overlap:8.5f} "
            f"{row.best_bell_label:>5s} "
            f"{row.phi_plus_overlap:8.5f} "
            f"{row.exact_avg_fidelity:8.5f} "
            f"{row.sampled_min_fidelity:8.5f} "
            f"{row.min_branch_fidelity:8.5f} "
            f"{row.max_pairwise_no_record_distance:9.3e} "
            f"{len(row.outcomes_seen):4d} "
            f"{'yes' if ok else 'no':>5s}"
        )
    print()


def print_case_details(rows: list[ProtocolRow]) -> None:
    for row in rows:
        frame_bits = f"({row.frame_bits[0]},{row.frame_bits[1]})"
        print(f"Case row: {row.case.label} [{row.frame_label}]")
        print(
            "  resource: "
            f"dim={row.case.dim} side={row.case.side} N={row.n_sites} envs={row.n_env} "
            f"mass={row.case.mass:g} G={row.case.G:g}, "
            f"ground={row.ground_energy:.12g}, full CHSH={row.full_chsh:.6f}, "
            f"logical CHSH={row.logical_chsh:.6f}, negativity={row.resource_negativity:.6f}"
        )
        print(
            "  Bell/fidelity: "
            f"raw best={row.raw_best_bell_overlap:.6f} ({row.raw_best_bell_label}), "
            f"frame_bits={frame_bits}, framed best={row.best_bell_overlap:.6f} "
            f"({row.best_bell_label}), Phi+={row.phi_plus_overlap:.6f}, "
            f"exact F_avg={row.exact_avg_fidelity:.6f}, sample mean/min/max="
            f"{row.sampled_mean_fidelity:.6f}/{row.sampled_min_fidelity:.6f}/"
            f"{row.sampled_max_fidelity:.6f}"
        )
        print(
            "  Bell branches: "
            f"outcomes={', '.join(row.outcomes_seen)}, "
            f"probability min/max={row.min_branch_probability:.6e}/"
            f"{row.max_branch_probability:.6e}, "
            f"conditional corrected fidelity min/max={row.min_branch_fidelity:.6f}/"
            f"{row.max_branch_fidelity:.6f}"
        )
        print(
            "  Bob before record: "
            f"distance to resource marginal={row.max_no_record_to_marginal_distance:.3e}, "
            f"pairwise input distance={row.max_pairwise_no_record_distance:.3e}, "
            f"marginal bias from I/2={row.bob_marginal_bias:.3e}"
        )
        print(
            "  causal record: "
            f"label={row.delivered_record_label}, early blocked={row.early_delivery_blocked}, "
            f"delivered once={row.delivered_once}, "
            f"delivered-branch fidelity={row.delivered_record_fidelity:.6f}"
        )
    print()


def print_acceptance(
    rows: list[ProtocolRow],
    operator_audit: OperatorConventionAudit,
    fidelity_threshold: float,
    protocol_tolerance: float,
    operator_tolerance: float,
) -> bool:
    null_rows = [row for row in rows if not row.non_null]
    non_null_rows = [row for row in rows if row.non_null]
    fixed_rows = [row for row in rows if row.frame_bits == (0, 0)]
    frame_rows = [row for row in rows if row.frame_bits != (0, 0)]
    passing_non_null = [
        row for row in non_null_rows if protocol_passes(row, fidelity_threshold, protocol_tolerance)
    ]
    fixed_frame_failures = [
        row
        for row in fixed_rows
        if row.non_null and row.raw_best_bell_label != "Phi+" and not protocol_passes(
            row, fidelity_threshold, protocol_tolerance
        )
    ]

    gates = {
        "3D retained-axis operator guard passes": operator_audit.retained_axis_guard_passes(
            operator_tolerance
        ),
        "3D raw xi_5 as traced retained-bit Z rejects": not operator_guard_passes(
            operator_audit.raw_z, operator_tolerance
        ),
        "3D raw xi_5 Bell controls reject": not all(
            pair_guard_passes(item, operator_tolerance)
            for item in operator_audit.raw_bell_projectors
        ),
        "3D null rows do not pass high-fidelity protocol": bool(null_rows)
        and all(not protocol_passes(row, fidelity_threshold, protocol_tolerance) for row in null_rows),
        "3D non-null retained-axis resource has a passing row": bool(passing_non_null),
        "fixed Phi+ frame failures are reported when the resource lands elsewhere": bool(
            fixed_frame_failures
        )
        or not any(row.non_null and row.raw_best_bell_label != "Phi+" for row in fixed_rows),
        "Bob pre-message input-independence is clean for runnable rows": bool(rows)
        and all(
            row.max_pairwise_no_record_distance < protocol_tolerance
            and row.max_no_record_to_marginal_distance < protocol_tolerance
            for row in rows
        ),
        "all four Bell outcomes are represented for runnable rows": bool(rows)
        and all(row.all_outcomes_seen for row in rows),
        "causal two-bit record remains clean for passing rows": bool(passing_non_null)
        and all(row.causal_record_ok for row in passing_non_null),
    }

    print("Acceptance gates:")
    for name, ok in gates.items():
        print(f"  {name}: {status(ok)}")
    print()

    if passing_non_null:
        best = max(passing_non_null, key=lambda row: row.exact_avg_fidelity)
        print(
            "3D resource status: "
            f"high-fidelity retained-axis row found for {best.case.label} "
            f"with frame {best.frame_label} "
            f"(Bell*={best.best_bell_overlap:.6f}, F_avg={best.exact_avg_fidelity:.6f})."
        )
    else:
        best = max(non_null_rows, key=lambda row: row.exact_avg_fidelity) if non_null_rows else None
        if best is None:
            print("3D resource status: no non-null 3D candidate rows were run.")
        else:
            print(
                "3D resource status: no high-fidelity retained-axis end-to-end row found; "
                f"best candidate was {best.case.label} [{best.frame_label}] with "
                f"Bell*={best.best_bell_overlap:.6f}, F_avg={best.exact_avg_fidelity:.6f}, "
                f"sample min={best.sampled_min_fidelity:.6f}."
            )

    if frame_rows:
        print(
            "Frame note: Bell-frame rows apply a known Bob-side retained-axis Pauli "
            "before the standard Z^z X^x feed-forward correction."
        )
    print("Claim boundary:")
    print("  Ordinary quantum state teleportation only; no matter, mass, charge, energy,")
    print("  object transport, or faster-than-light signaling is claimed.")
    print("Limitations:")
    print("  Default 3D resource is the dense-diagonalized side=2 case (N=8 sites).")
    print("  The measurement, feed-forward, and correction remain ideal logical operations.")
    print("  Raw xi_5 rejection is an operator-factorization control, not detector hardware.")
    return all(gates.values())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", type=int, default=2, help="3D lattice side length")
    parser.add_argument("--mass", type=float, default=0.0)
    parser.add_argument(
        "--candidate-g",
        type=parse_csv_floats,
        default=(1000.0,),
        help="comma-separated non-null Poisson couplings to audit",
    )
    parser.add_argument("--trials", type=int, default=128, help="random input states per row")
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument("--fidelity-threshold", type=float, default=0.90)
    parser.add_argument("--protocol-tolerance", type=float, default=1e-10)
    parser.add_argument("--operator-tolerance", type=float, default=1e-12)
    parser.add_argument("--probability-floor", type=float, default=1e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.side <= 0 or args.side % 2 != 0:
        raise ValueError("--side must be a positive even integer")
    if args.trials <= 0:
        raise ValueError("--trials must be positive")
    if not 0.0 < args.fidelity_threshold <= 1.0:
        raise ValueError("--fidelity-threshold must be in (0, 1]")
    if args.protocol_tolerance <= 0.0:
        raise ValueError("--protocol-tolerance must be positive")
    if args.operator_tolerance <= 0.0:
        raise ValueError("--operator-tolerance must be positive")
    if args.probability_floor < 0.0:
        raise ValueError("--probability-floor must be nonnegative")

    states = probe_states(args.seed, args.trials)
    cases = build_cases(args.side, args.mass, args.candidate_g)

    print("3D OPERATOR-CONSISTENT POISSON END-TO-END TELEPORTATION AUDIT")
    print("Status: planning / first artifact; quantum state teleportation only")
    print(
        "Geometry: 3 spatial dimensions with one directed classical/causal record; "
        "retained logical bit is the last KS taste axis"
    )
    print(
        f"Input probes: {len(states)} states "
        f"(six Pauli-axis probes + {args.trials} random, seed={args.seed})"
    )
    print(
        f"Thresholds: fidelity>={args.fidelity_threshold:.3f}, "
        f"protocol tol={args.protocol_tolerance:.1e}, "
        f"operator tol={args.operator_tolerance:.1e}"
    )
    print()

    operator_audit = audit_operator_convention(
        THREE_D_DIM,
        args.side,
        tolerance=args.operator_tolerance,
    )
    print_operator_summary(operator_audit, args.operator_tolerance)

    rows: list[ProtocolRow] = []
    for index, case in enumerate(cases):
        extracted = extract_3d_resource(case)
        rows.append(
            evaluate_protocol_row(
                extracted=extracted,
                row_label=f"{case.label}:fixed_phi_plus",
                frame_label="fixed Phi+",
                frame_bits=(0, 0),
                states=states,
                seed=args.seed + index,
                tolerance=args.protocol_tolerance,
                probability_floor=args.probability_floor,
            )
        )
        if case.G != 0.0 and extracted.raw_best_bell_label != "Phi+":
            frame_bits = BELL_BITS_BY_LABEL[extracted.raw_best_bell_label]
            rows.append(
                evaluate_protocol_row(
                    extracted=extracted,
                    row_label=f"{case.label}:best_bell_frame",
                    frame_label=f"{extracted.raw_best_bell_label}->Phi+",
                    frame_bits=frame_bits,
                    states=states,
                    seed=args.seed + index + 1000,
                    tolerance=args.protocol_tolerance,
                    probability_floor=args.probability_floor,
                )
            )

    print_case_table(rows, args.fidelity_threshold, args.protocol_tolerance)
    print_case_details(rows)
    ok = print_acceptance(
        rows=rows,
        operator_audit=operator_audit,
        fidelity_threshold=args.fidelity_threshold,
        protocol_tolerance=args.protocol_tolerance,
        operator_tolerance=args.operator_tolerance,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
