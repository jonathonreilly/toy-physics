#!/usr/bin/env python3
"""Operator-consistent Poisson-backed teleportation audit.

Status: planning / first artifact. This runner hardens the existing end-to-end
Poisson lane after the taste-readout operator finding:

1. prove the traced retained-bit protocol uses retained-axis logical Z/X
   operators that factor as O_logical tensor I_env;
2. reject raw sublattice parity Z=xi_5 as a traced retained-bit logical Z in
   dim > 1;
3. run the ordinary Bell-measurement + Pauli-correction teleportation channel
   on selected Poisson-derived traced logical resources;
4. keep Bob's pre-message no-signaling check and the causal two-bit record
   check from the end-to-end lane.

This is ordinary quantum state teleportation planning only. It does not claim
matter teleportation, mass transfer, charge transfer, energy transfer, object
transport, or faster-than-light signaling.
"""

from __future__ import annotations

import argparse
import dataclasses
import sys
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_teleportation_end_to_end_poisson import (  # noqa: E402
    EndToEndResult,
    evaluate_case,
    passes_protocol,
    probe_states,
)
from frontier_teleportation_resource_from_poisson import (  # noqa: E402
    DEFAULT_CASES,
    OUTCOME_LABELS,
    OUTCOME_ORDER,
    AuditCase,
)
from frontier_teleportation_taste_readout_operator_model import (  # noqa: E402
    X2,
    Z2,
    OperatorAudit,
    PairOperatorAudit,
    bell_projector,
    bell_terms,
    build_axis_taste_operator,
    build_fixed_pair_hop_x,
    build_sublattice_z,
    factor_sites,
    factorization_audit,
    pair_factorization_audit,
)


@dataclasses.dataclass(frozen=True)
class OperatorConventionAudit:
    dim: int
    side: int
    retained_axis: int
    n_sites: int
    n_env: int
    axis_z: OperatorAudit
    axis_x: OperatorAudit
    axis_zx: OperatorAudit
    axis_bell_projectors: tuple[PairOperatorAudit, ...]
    raw_z: OperatorAudit
    raw_zx: OperatorAudit
    raw_bell_projectors: tuple[PairOperatorAudit, ...]

    def retained_axis_guard_passes(self, tolerance: float) -> bool:
        return all(
            operator_guard_passes(audit, tolerance)
            for audit in (self.axis_z, self.axis_x, self.axis_zx)
        ) and all(
            pair_guard_passes(audit, tolerance) for audit in self.axis_bell_projectors
        )

    def raw_z_rejected_when_required(self, tolerance: float) -> bool:
        if self.dim == 1:
            return operator_guard_passes(self.raw_z, tolerance)
        return not operator_guard_passes(self.raw_z, tolerance)

    def raw_bell_rejected_when_required(self, tolerance: float) -> bool:
        if self.dim == 1:
            return all(pair_guard_passes(audit, tolerance) for audit in self.raw_bell_projectors)
        return not all(pair_guard_passes(audit, tolerance) for audit in self.raw_bell_projectors)


@dataclasses.dataclass(frozen=True)
class CaseAudit:
    case: AuditCase
    operators: OperatorConventionAudit
    protocol: EndToEndResult
    protocol_passes: bool

    def passes(self, fidelity_threshold: float, protocol_tolerance: float, operator_tolerance: float) -> bool:
        return bool(
            self.protocol_passes
            and self.operators.retained_axis_guard_passes(operator_tolerance)
            and self.protocol.best_bell_overlap >= fidelity_threshold
            and self.protocol.max_pairwise_no_record_distance < protocol_tolerance
        )


def operator_guard_passes(audit: OperatorAudit, tolerance: float) -> bool:
    expected_ok = audit.expected_error is None or audit.expected_error <= tolerance
    return bool(audit.passes and expected_ok)


def pair_guard_passes(audit: PairOperatorAudit, tolerance: float) -> bool:
    expected_ok = audit.expected_error is None or audit.expected_error <= tolerance
    return bool(audit.passes and expected_ok)


def fmt_float(value: float) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3:
        return f"{value:.3e}"
    return f"{value:.6f}"


def status(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def audit_operator_convention(dim: int, side: int, tolerance: float) -> OperatorConventionAudit:
    retained_axis = dim - 1
    factors = factor_sites(dim, side, logical_axis=retained_axis)

    axis_z = build_axis_taste_operator(dim, side, retained_axis, Z2)
    axis_x = build_axis_taste_operator(dim, side, retained_axis, X2)
    axis_zx = axis_z @ axis_x

    raw_z = build_sublattice_z(dim, side)
    fixed_x = build_fixed_pair_hop_x(dim, side)
    raw_zx = raw_z @ fixed_x

    axis_z_audit = factorization_audit(
        "retained-axis logical Z",
        "readout/correction",
        axis_z,
        factors,
        tolerance,
        Z2,
        "Z on the retained KS taste axis, blind to cells and spectator tastes.",
    )
    axis_x_audit = factorization_audit(
        "retained-axis logical X",
        "readout/correction",
        axis_x,
        factors,
        tolerance,
        X2,
        "X on the retained KS taste axis, blind to cells and spectator tastes.",
    )
    axis_zx_audit = factorization_audit(
        "retained-axis ZX correction",
        "correction",
        axis_zx,
        factors,
        tolerance,
        Z2 @ X2,
        "Composite retained-bit Pauli correction.",
    )

    raw_z_audit = factorization_audit(
        "raw sublattice Z=xi_5",
        "readout/correction control",
        raw_z,
        factors,
        tolerance,
        Z2,
        "Invalid as traced retained-bit Z in dim > 1 because spectator taste signs remain.",
    )
    raw_zx_audit = factorization_audit(
        "raw-Z/fixed-X ZX correction",
        "correction control",
        raw_zx,
        factors,
        tolerance,
        Z2 @ X2,
        "Composite control inherits the raw xi_5 spectator dependence in dim > 1.",
    )

    axis_bell = tuple(
        pair_factorization_audit(
            f"retained-axis Bell {OUTCOME_LABELS[(z_bit, x_bit)]} projector",
            "Bell measurement",
            bell_terms(z_bit, x_bit, axis_z, axis_x),
            factors,
            tolerance,
            bell_projector(z_bit, x_bit),
            "Bell projector built from retained-axis Z/X stabilizers.",
        )
        for z_bit, x_bit in OUTCOME_ORDER
    )
    raw_bell = tuple(
        pair_factorization_audit(
            f"raw-Z/fixed-X Bell {OUTCOME_LABELS[(z_bit, x_bit)]} projector",
            "Bell measurement control",
            bell_terms(z_bit, x_bit, raw_z, fixed_x),
            factors,
            tolerance,
            bell_projector(z_bit, x_bit),
            "Control Bell projector built with raw xi_5 in place of retained-axis Z.",
        )
        for z_bit, x_bit in OUTCOME_ORDER
    )

    return OperatorConventionAudit(
        dim=dim,
        side=side,
        retained_axis=retained_axis,
        n_sites=factors.n_sites,
        n_env=factors.n_env,
        axis_z=axis_z_audit,
        axis_x=axis_x_audit,
        axis_zx=axis_zx_audit,
        axis_bell_projectors=axis_bell,
        raw_z=raw_z_audit,
        raw_zx=raw_zx_audit,
        raw_bell_projectors=raw_bell,
    )


def raw_control_surfaces(cases: list[AuditCase]) -> list[tuple[int, int]]:
    surfaces = {(case.dim, case.side) for case in cases}
    surfaces.add((3, 2))
    return sorted(surfaces)


def print_operator_summary(audits: list[OperatorConventionAudit], tolerance: float) -> None:
    print("Operator-consistency guards:")
    print(
        "  "
        f"{'surface':10s} {'envs':>5s} {'axis Z':>7s} {'axis X':>7s} "
        f"{'axis Bell4':>10s} {'raw Z':>7s} {'raw Bell4':>10s} "
        f"{'raw expected':>13s}"
    )
    for audit in audits:
        axis_bell_ok = all(pair_guard_passes(item, tolerance) for item in audit.axis_bell_projectors)
        raw_bell_ok = all(pair_guard_passes(item, tolerance) for item in audit.raw_bell_projectors)
        raw_expected = (
            "valid in 1D"
            if audit.dim == 1
            else "rejected"
        )
        print(
            "  "
            f"{audit.dim}D side={audit.side:<2d} "
            f"{audit.n_env:5d} "
            f"{status(operator_guard_passes(audit.axis_z, tolerance)):>7s} "
            f"{status(operator_guard_passes(audit.axis_x, tolerance)):>7s} "
            f"{status(axis_bell_ok):>10s} "
            f"{status(operator_guard_passes(audit.raw_z, tolerance)):>7s} "
            f"{status(raw_bell_ok):>10s} "
            f"{raw_expected:>13s}"
        )
    print()


def print_raw_control_details(audits: list[OperatorConventionAudit], tolerance: float) -> None:
    print("Raw xi_5 controls:")
    for audit in audits:
        raw_bell_residual = max(item.relative_residual for item in audit.raw_bell_projectors)
        raw_bell_expected = max(
            0.0 if item.expected_error is None else item.expected_error
            for item in audit.raw_bell_projectors
        )
        print(
            "  "
            f"{audit.dim}D side={audit.side}: "
            f"raw Z {status(operator_guard_passes(audit.raw_z, tolerance))} "
            f"rel={fmt_float(audit.raw_z.relative_residual)} "
            f"expected_err={fmt_float(audit.raw_z.expected_error or 0.0)}; "
            f"raw Bell4 {status(all(pair_guard_passes(item, tolerance) for item in audit.raw_bell_projectors))} "
            f"max_rel={fmt_float(raw_bell_residual)} "
            f"max_expected_err={fmt_float(raw_bell_expected)}"
        )
    print()


def print_case_table(
    cases: list[CaseAudit],
    fidelity_threshold: float,
    protocol_tolerance: float,
    operator_tolerance: float,
) -> None:
    print("End-to-end retained-axis case table:")
    print(
        "  "
        f"{'case':18s} {'Sfull':>8s} {'Bell*':>8s} {'label':>5s} "
        f"{'Favg':>8s} {'Fmin':>8s} {'Bmin':>8s} {'noSig':>9s} "
        f"{'axisOp':>7s} {'pass':>5s}"
    )
    for case in cases:
        result = case.protocol
        ok = case.passes(fidelity_threshold, protocol_tolerance, operator_tolerance)
        print(
            "  "
            f"{result.label[:18]:18s} "
            f"{result.full_chsh:8.5f} "
            f"{result.best_bell_overlap:8.5f} "
            f"{result.best_bell_label:>5s} "
            f"{result.exact_avg_fidelity:8.5f} "
            f"{result.sampled_min_fidelity:8.5f} "
            f"{result.min_branch_fidelity:8.5f} "
            f"{result.max_pairwise_no_record_distance:9.3e} "
            f"{status(case.operators.retained_axis_guard_passes(operator_tolerance)):>7s} "
            f"{'yes' if ok else 'no':>5s}"
        )
    print()


def print_case_details(cases: list[CaseAudit]) -> None:
    for case in cases:
        result = case.protocol
        print(f"Case: {result.label}")
        print(
            "  resource: "
            f"dim={result.dim} side={result.side} G={result.G:g}, "
            f"full CHSH={result.full_chsh:.6f}, logical CHSH={result.logical_chsh:.6f}, "
            f"Bell*={result.best_bell_overlap:.6f} ({result.best_bell_label}), "
            f"negativity={result.resource_negativity:.6f}"
        )
        print(
            "  fidelity: "
            f"exact F_avg={result.exact_avg_fidelity:.6f}, "
            f"sample mean/min/max={result.sampled_mean_fidelity:.6f}/"
            f"{result.sampled_min_fidelity:.6f}/{result.sampled_max_fidelity:.6f}, "
            f"conditional branch min/max={result.min_branch_fidelity:.6f}/"
            f"{result.max_branch_fidelity:.6f}"
        )
        print(
            "  Bell branches: "
            f"outcomes={', '.join(result.outcomes_seen)}, "
            f"probability min/max={result.min_branch_probability:.6e}/"
            f"{result.max_branch_probability:.6e}"
        )
        print(
            "  Bob before record: "
            f"distance to resource marginal={result.max_no_record_to_marginal_distance:.3e}, "
            f"pairwise input distance={result.max_pairwise_no_record_distance:.3e}, "
            f"marginal bias from I/2={result.bob_marginal_bias:.3e}"
        )
        print(
            "  causal record: "
            f"label={result.delivered_record_label}, early blocked={result.early_delivery_blocked}, "
            f"delivered once={result.delivered_once}, "
            f"delivered-branch fidelity={result.delivered_record_fidelity:.6f}"
        )
    print()


def print_acceptance(
    cases: list[CaseAudit],
    operator_controls: list[OperatorConventionAudit],
    fidelity_threshold: float,
    protocol_tolerance: float,
    operator_tolerance: float,
) -> bool:
    nulls = [case for case in cases if not case.protocol.non_null]
    non_null = [case for case in cases if case.protocol.non_null]
    passing = [
        case
        for case in non_null
        if case.passes(fidelity_threshold, protocol_tolerance, operator_tolerance)
    ]
    all_outcomes = {OUTCOME_LABELS[outcome] for outcome in OUTCOME_ORDER}
    dim_gt_one_controls = [audit for audit in operator_controls if audit.dim > 1]
    raw_dims_seen = {audit.dim for audit in dim_gt_one_controls}

    gates = {
        "selected non-null Poisson cases pass retained-axis end-to-end": bool(non_null)
        and all(case in passing for case in non_null),
        "null controls do not pass high-fidelity protocol": all(
            not case.passes(fidelity_threshold, protocol_tolerance, operator_tolerance)
            for case in nulls
        ),
        "retained-axis operator guard passes for all selected cases": all(
            case.operators.retained_axis_guard_passes(operator_tolerance) for case in cases
        ),
        "2D and 3D raw xi_5 controls are rejected": {2, 3}.issubset(raw_dims_seen)
        and all(
            audit.raw_z_rejected_when_required(operator_tolerance)
            and audit.raw_bell_rejected_when_required(operator_tolerance)
            for audit in dim_gt_one_controls
        ),
        "Bob pre-message input-independence is clean for passing cases": bool(passing)
        and all(
            case.protocol.max_pairwise_no_record_distance < protocol_tolerance
            and case.protocol.max_no_record_to_marginal_distance < protocol_tolerance
            for case in passing
        ),
        "all four Bell outcomes are represented for passing cases": bool(passing)
        and all(set(case.protocol.outcomes_seen) == all_outcomes for case in passing),
        "random input-state fidelity is represented for passing cases": bool(passing)
        and all(case.protocol.sampled_min_fidelity >= fidelity_threshold for case in passing),
        "causal two-bit record remains clean for passing cases": bool(passing)
        and all(case.protocol.causal_record_ok for case in passing),
    }

    print("Acceptance gates:")
    for name, ok in gates.items():
        print(f"  {name}: {status(ok)}")
    print()
    print("Claim boundary:")
    print("  This is an operator-consistent audit of ordinary quantum state teleportation.")
    print("  It uses retained-axis logical Z/X operators for the traced taste qubit.")
    print("  It is not matter, mass, charge, energy, object, or faster-than-light transport.")
    print()
    print("Limitations:")
    print("  Poisson resources are still obtained by offline diagonalization and tracing.")
    print("  Bell measurement, readout, feed-forward, and correction are ideal logical operators.")
    print("  Raw xi_5 rejection is an operator-factorization control, not a hardware model.")
    return all(gates.values())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=128, help="random input states per case")
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument("--fidelity-threshold", type=float, default=0.90)
    parser.add_argument("--protocol-tolerance", type=float, default=1e-10)
    parser.add_argument("--operator-tolerance", type=float, default=1e-12)
    parser.add_argument("--probability-floor", type=float, default=1e-12)
    parser.add_argument(
        "--case",
        choices=[case.label for case in DEFAULT_CASES],
        action="append",
        help="case label to run; omit for default cases",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
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

    requested = set(args.case or [])
    selected_cases = [case for case in DEFAULT_CASES if not requested or case.label in requested]
    states = probe_states(args.seed, args.trials)

    print("OPERATOR-CONSISTENT POISSON END-TO-END TELEPORTATION AUDIT")
    print("Status: planning / first artifact; quantum state teleportation only")
    print(
        "Convention: trace cells/spectator tastes and use retained-axis logical "
        "Z/X for readout, Bell measurement, and correction"
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

    operator_cache = {
        surface: audit_operator_convention(*surface, tolerance=args.operator_tolerance)
        for surface in raw_control_surfaces(selected_cases)
    }

    case_audits: list[CaseAudit] = []
    for index, case in enumerate(selected_cases):
        operators = operator_cache[(case.dim, case.side)]
        protocol = evaluate_case(
            case=case,
            states=states,
            seed=args.seed + index,
            tolerance=args.protocol_tolerance,
            probability_floor=args.probability_floor,
        )
        case_audits.append(
            CaseAudit(
                case=case,
                operators=operators,
                protocol=protocol,
                protocol_passes=passes_protocol(
                    protocol,
                    fidelity_threshold=args.fidelity_threshold,
                    tolerance=args.protocol_tolerance,
                ),
            )
        )

    operator_controls = [operator_cache[surface] for surface in sorted(operator_cache)]
    print_operator_summary(operator_controls, args.operator_tolerance)
    print_raw_control_details(operator_controls, args.operator_tolerance)
    print_case_table(
        case_audits,
        fidelity_threshold=args.fidelity_threshold,
        protocol_tolerance=args.protocol_tolerance,
        operator_tolerance=args.operator_tolerance,
    )
    print_case_details(case_audits)
    ok = print_acceptance(
        case_audits,
        operator_controls,
        fidelity_threshold=args.fidelity_threshold,
        protocol_tolerance=args.protocol_tolerance,
        operator_tolerance=args.operator_tolerance,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
