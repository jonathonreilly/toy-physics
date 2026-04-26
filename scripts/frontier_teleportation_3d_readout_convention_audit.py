#!/usr/bin/env python3
"""3D retained-axis Z versus raw xi_5 readout convention audit.

Status: planning / first artifact. This runner makes the 3D+1 readout
convention explicit for ordinary encoded quantum-state teleportation:

    retained traced Z  = Z_r tensor I_spectator
    raw xi_5           = Z_x Z_y Z_z

Raw xi_5 restricts to a signed logical Z only after a fixed spectator taste
branch is selected. It is not the traced retained-bit Z operator because it
keeps spectator taste signs.

This is ordinary quantum state teleportation planning only. It does not claim
matter teleportation, mass transfer, charge transfer, energy transfer, object
transport, or faster-than-light signaling.
"""

from __future__ import annotations

import argparse
import dataclasses
import itertools
import sys
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_teleportation_taste_readout_operator_model import (  # noqa: E402
    OUTCOME_LABELS,
    OUTCOME_ORDER,
    X2,
    Z2,
    OperatorAudit,
    PairOperatorAudit,
    SiteFactorization,
    bell_projector,
    bell_terms,
    blocks_by_logical_env,
    build_axis_taste_operator,
    build_sublattice_z,
    factor_sites,
    factorization_audit,
    pair_factorization_audit,
)


DIM = 3
AXIS_NAMES = ("x", "y", "z")


@dataclasses.dataclass(frozen=True)
class BranchRestriction:
    spectator_bits: tuple[int, ...]
    sign: int
    env_count: int
    max_abs_error: float


@dataclasses.dataclass(frozen=True)
class AxisReadoutAudit:
    side: int
    retained_axis: int
    spectator_axes: tuple[int, ...]
    n_sites: int
    n_cells: int
    n_env: int
    retained_z: OperatorAudit
    retained_x: OperatorAudit
    raw_xi5: OperatorAudit
    branch_restrictions: tuple[BranchRestriction, ...]
    retained_bell_projectors: tuple[PairOperatorAudit, ...]
    raw_xi5_bell_projectors: tuple[PairOperatorAudit, ...]


def status(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def fmt_float(value: float) -> str:
    if value == 0.0 or abs(value) < 5e-16:
        return "0"
    if abs(value) < 1e-3:
        return f"{value:.3e}"
    return f"{value:.6f}"


def axis_label(axis: int) -> str:
    return AXIS_NAMES[axis]


def spectator_label(axes: tuple[int, ...]) -> str:
    return "".join(axis_label(axis) for axis in axes)


def operator_guard_passes(audit: OperatorAudit, tolerance: float) -> bool:
    expected_ok = audit.expected_error is None or audit.expected_error <= tolerance
    return bool(audit.passes and expected_ok)


def pair_guard_passes(audit: PairOperatorAudit, tolerance: float) -> bool:
    expected_ok = audit.expected_error is None or audit.expected_error <= tolerance
    return bool(audit.passes and expected_ok)


def sign_for_spectators(spectator_bits: tuple[int, ...]) -> int:
    return 1 if sum(spectator_bits) % 2 == 0 else -1


def fixed_branch_restrictions(
    raw_xi5: np.ndarray,
    factors: SiteFactorization,
    spectator_axes: tuple[int, ...],
) -> tuple[BranchRestriction, ...]:
    blocks = blocks_by_logical_env(raw_xi5, factors)
    restrictions: list[BranchRestriction] = []

    for spectator_bits in itertools.product((0, 1), repeat=len(spectator_axes)):
        sign = sign_for_spectators(tuple(spectator_bits))
        env_count = 0
        max_error = 0.0
        for env_index, (_cell, env_spectator_bits) in enumerate(factors.env_labels):
            if env_spectator_bits != tuple(spectator_bits):
                continue
            env_count += 1
            block = blocks[:, env_index, :, env_index]
            max_error = max(max_error, float(np.max(np.abs(block - sign * Z2))))
        restrictions.append(
            BranchRestriction(
                spectator_bits=tuple(spectator_bits),
                sign=sign,
                env_count=env_count,
                max_abs_error=max_error,
            )
        )

    return tuple(restrictions)


def audit_axis(side: int, retained_axis: int, tolerance: float) -> AxisReadoutAudit:
    spectator_axes = tuple(axis for axis in range(DIM) if axis != retained_axis)
    factors = factor_sites(DIM, side, logical_axis=retained_axis)

    retained_z_op = build_axis_taste_operator(DIM, side, retained_axis, Z2)
    retained_x_op = build_axis_taste_operator(DIM, side, retained_axis, X2)
    raw_xi5_op = build_sublattice_z(DIM, side)

    retained_z = factorization_audit(
        "retained-axis Z_r",
        "traced readout/correction",
        retained_z_op,
        factors,
        tolerance,
        Z2,
        "Z on the retained taste axis with identity on cells and spectator tastes.",
    )
    retained_x = factorization_audit(
        "retained-axis X_r",
        "traced Bell measurement/correction",
        retained_x_op,
        factors,
        tolerance,
        X2,
        "X on the retained taste axis with identity on cells and spectator tastes.",
    )
    raw_xi5 = factorization_audit(
        "raw xi_5 = Z_x Z_y Z_z",
        "invalid traced retained-Z control",
        raw_xi5_op,
        factors,
        tolerance,
        Z2,
        "Raw xi_5 is signed logical Z only after fixing spectator taste bits.",
    )

    retained_bell = tuple(
        pair_factorization_audit(
            f"retained-axis Bell {OUTCOME_LABELS[(z_bit, x_bit)]} projector",
            "Bell measurement",
            bell_terms(z_bit, x_bit, retained_z_op, retained_x_op),
            factors,
            tolerance,
            bell_projector(z_bit, x_bit),
            "Bell projector built from retained-axis Z_r and X_r.",
        )
        for z_bit, x_bit in OUTCOME_ORDER
    )
    raw_bell = tuple(
        pair_factorization_audit(
            f"raw-xi_5 Bell {OUTCOME_LABELS[(z_bit, x_bit)]} projector",
            "Bell measurement control",
            bell_terms(z_bit, x_bit, raw_xi5_op, retained_x_op),
            factors,
            tolerance,
            bell_projector(z_bit, x_bit),
            "Bell projector control built with raw xi_5 in place of retained-axis Z_r.",
        )
        for z_bit, x_bit in OUTCOME_ORDER
    )

    return AxisReadoutAudit(
        side=side,
        retained_axis=retained_axis,
        spectator_axes=spectator_axes,
        n_sites=factors.n_sites,
        n_cells=(side // 2) ** DIM,
        n_env=factors.n_env,
        retained_z=retained_z,
        retained_x=retained_x,
        raw_xi5=raw_xi5,
        branch_restrictions=fixed_branch_restrictions(raw_xi5_op, factors, spectator_axes),
        retained_bell_projectors=retained_bell,
        raw_xi5_bell_projectors=raw_bell,
    )


def build_audits(sides: list[int], tolerance: float) -> list[AxisReadoutAudit]:
    return [
        audit_axis(side=side, retained_axis=retained_axis, tolerance=tolerance)
        for side in sides
        for retained_axis in range(DIM)
    ]


def max_expected_error(items: tuple[PairOperatorAudit, ...]) -> float:
    return max(0.0 if item.expected_error is None else item.expected_error for item in items)


def print_operator_summary(audits: list[AxisReadoutAudit], tolerance: float) -> None:
    print("3D retained-axis operator summary:")
    print(
        "  "
        f"{'surface':11s} {'ret':>3s} {'envs':>4s} "
        f"{'Z_r':>5s} {'X_r':>5s} {'xi5':>5s} "
        f"{'xi5_rel':>9s} {'xi5_err':>9s} {'branch_err':>10s} "
        f"{'Bell4':>6s} {'rawBell4':>8s} {'rawBellRel':>10s}"
    )
    for audit in audits:
        retained_bell_ok = all(
            pair_guard_passes(item, tolerance) for item in audit.retained_bell_projectors
        )
        raw_bell_ok = all(
            pair_guard_passes(item, tolerance) for item in audit.raw_xi5_bell_projectors
        )
        max_branch_error = max(item.max_abs_error for item in audit.branch_restrictions)
        raw_bell_rel = max(item.relative_residual for item in audit.raw_xi5_bell_projectors)
        print(
            "  "
            f"3D side={audit.side:<2d} "
            f"{axis_label(audit.retained_axis):>3s} "
            f"{audit.n_env:4d} "
            f"{status(operator_guard_passes(audit.retained_z, tolerance)):>5s} "
            f"{status(operator_guard_passes(audit.retained_x, tolerance)):>5s} "
            f"{status(operator_guard_passes(audit.raw_xi5, tolerance)):>5s} "
            f"{fmt_float(audit.raw_xi5.relative_residual):>9s} "
            f"{fmt_float(audit.raw_xi5.expected_error or 0.0):>9s} "
            f"{fmt_float(max_branch_error):>10s} "
            f"{status(retained_bell_ok):>6s} "
            f"{status(raw_bell_ok):>8s} "
            f"{fmt_float(raw_bell_rel):>10s}"
        )
    print()


def print_branch_tables(audits: list[AxisReadoutAudit]) -> None:
    print("Fixed-branch raw xi_5 restrictions:")
    for audit in audits:
        label = spectator_label(audit.spectator_axes)
        signs = "; ".join(
            f"{label}={''.join(str(bit) for bit in item.spectator_bits)} "
            f"sign={item.sign:+d} envs={item.env_count} "
            f"err={fmt_float(item.max_abs_error)}"
            for item in audit.branch_restrictions
        )
        print(
            "  "
            f"3D side={audit.side} retained={axis_label(audit.retained_axis)} "
            f"spectators={label}: xi_5|branch = sign * Z_{axis_label(audit.retained_axis)}"
        )
        print(f"    {signs}")
    print()


def print_bell_details(audits: list[AxisReadoutAudit], tolerance: float) -> None:
    print("Bell projector consequences:")
    for audit in audits:
        retained_ok = all(
            pair_guard_passes(item, tolerance) for item in audit.retained_bell_projectors
        )
        retained_rel = max(item.relative_residual for item in audit.retained_bell_projectors)
        retained_err = max_expected_error(audit.retained_bell_projectors)
        raw_rel = max(item.relative_residual for item in audit.raw_xi5_bell_projectors)
        raw_err = max_expected_error(audit.raw_xi5_bell_projectors)
        raw_fail_count = sum(
            not pair_guard_passes(item, tolerance)
            for item in audit.raw_xi5_bell_projectors
        )
        print(
            "  "
            f"3D side={audit.side} retained={axis_label(audit.retained_axis)}: "
            f"retained Bell4 {status(retained_ok)} "
            f"max_rel={fmt_float(retained_rel)} max_expected_err={fmt_float(retained_err)}; "
            f"raw xi_5 Bell failures={raw_fail_count}/4 "
            f"max_rel={fmt_float(raw_rel)} max_expected_err={fmt_float(raw_err)}"
        )
    print()


def print_guard_language() -> None:
    print("Recommended guard language for scripts:")
    print("  fixed_branch_z: raw xi_5 restricted to an explicit spectator branch; track sign.")
    print("  traced_operator_z: use retained-axis Z_r tensor I_spectator for 3D readout/correction.")
    print("  native_xi5_as_traced_z: reject in 3D unless an environment measurement/heralding")
    print("    workflow and branch-conditioned correction rule are supplied.")
    print("  Bell projectors: build traced Bell measurements from retained-axis Z_r and X_r.")
    print()


def print_acceptance(audits: list[AxisReadoutAudit], sides: list[int], tolerance: float) -> bool:
    gates = {
        "3D side=2 and side=4 surfaces audited": {2, 4}.issubset(set(sides)),
        "all retained-axis Z_r operators factor as O_logical tensor I_env": all(
            operator_guard_passes(audit.retained_z, tolerance) for audit in audits
        ),
        "all retained-axis X_r operators factor as O_logical tensor I_env": all(
            operator_guard_passes(audit.retained_x, tolerance) for audit in audits
        ),
        "raw xi_5 fixed-branch restrictions are signed logical Z": all(
            item.max_abs_error <= tolerance
            for audit in audits
            for item in audit.branch_restrictions
        ),
        "raw xi_5 fails traced retained-axis Z factorization in 3D": all(
            not operator_guard_passes(audit.raw_xi5, tolerance) for audit in audits
        ),
        "retained-axis Bell projectors pass as traced Bell measurements": all(
            pair_guard_passes(item, tolerance)
            for audit in audits
            for item in audit.retained_bell_projectors
        ),
        "raw xi_5 Bell projectors fail as traced Bell measurements": all(
            not pair_guard_passes(item, tolerance)
            for audit in audits
            for item in audit.raw_xi5_bell_projectors
        ),
    }

    print("Acceptance gates:")
    for name, ok in gates.items():
        print(f"  {name}: {status(ok)}")
    print()
    print("Claim boundary:")
    print("  This is a 3D operator-convention audit for ordinary quantum state teleportation.")
    print("  It is not matter, mass, charge, energy, object, or faster-than-light transport.")
    print()
    print("Limitations:")
    print("  This is a finite side=2/side=4 operator audit, not a hardware readout design.")
    print("  Raw xi_5 can still be used in explicitly fixed spectator-branch algebra.")
    print("  A traced raw-xi_5 workflow would need extra environment measurement/heralding rules.")
    return all(gates.values())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--side",
        type=int,
        action="append",
        help="3D side length to audit; may be repeated. Default: 2 and 4.",
    )
    parser.add_argument("--tolerance", type=float, default=1e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sides = args.side if args.side is not None else [2, 4]
    sides = sorted(dict.fromkeys(sides))
    if any(side <= 0 or side % 2 != 0 for side in sides):
        raise ValueError("all audited side lengths must be positive even integers")
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")

    audits = build_audits(sides=sides, tolerance=args.tolerance)

    print("3D READOUT-CONVENTION AUDIT: RETAINED-AXIS Z_r VERSUS RAW xi_5")
    print("Status: planning / first artifact; quantum state teleportation only")
    print(
        "Convention: traced 3D readout must use Z_r tensor I_spectator; "
        "raw xi_5 = Z_x Z_y Z_z is fixed-branch signed Z only"
    )
    print(f"Audited sides: {', '.join(str(side) for side in sides)}")
    print(f"Tolerance: {args.tolerance:.1e}")
    print()

    print_operator_summary(audits, args.tolerance)
    print_branch_tables(audits)
    print_bell_details(audits, args.tolerance)
    print_guard_language()
    ok = print_acceptance(audits, sides, args.tolerance)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
