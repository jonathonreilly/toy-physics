#!/usr/bin/env python3
"""Classify AWAY / repulsive-looking signed-gravity rows by mechanism.

The script is intentionally conservative. A locked-chi row is promoted to
SIGNED_RESPONSE_CANDIDATE only when selector, source, locking, action-reaction,
and positive-inertial gates are all explicitly passed.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


MECHANISMS = (
    "locked_chi_response",
    "lensing_phase_flip",
    "complex_absorptive_away",
    "boundary/proxy",
    "inserted_control_no_go",
)


@dataclass(frozen=True)
class Classification:
    mechanism: str
    tag: str
    mechanism_class: str
    promotable: bool
    reason: str


def passed(value: str) -> bool:
    return value == "pass"


def classify(args: argparse.Namespace) -> Classification:
    mechanism = args.mechanism

    if mechanism == "lensing_phase_flip":
        return Classification(
            mechanism,
            "LENSING_PHASE_ONLY",
            "interference",
            False,
            "k*h phase windows or centroid interference are not chi_g selector evidence",
        )

    if mechanism == "complex_absorptive_away":
        return Classification(
            mechanism,
            "COMPLEX_ABSORPTIVE_ONLY",
            "absorptive",
            False,
            "AWAY read is path-selection under imaginary action, not conservative repulsive gravity",
        )

    if mechanism == "boundary/proxy":
        return Classification(
            mechanism,
            "BOUNDARY_PROXY_ONLY",
            "boundary_or_proxy",
            False,
            "readout depends on a boundary window, proxy observable, or family-specific diagnostic",
        )

    if mechanism == "inserted_control_no_go":
        return Classification(
            mechanism,
            "CONTROL_NO_GO",
            "inserted_control",
            False,
            "inserted signs or source-only/response-only rows are controls, not derived sectors",
        )

    required = {
        "selector_gate": passed(args.selector_gate),
        "source_gate": passed(args.source_gate),
        "locked_source_response": args.locked_source_response,
        "two_body_action_reaction": args.two_body_action_reaction,
        "positive_inertial_mass": args.positive_inertial_mass,
    }
    missing = [name for name, ok in required.items() if not ok]
    if missing:
        return Classification(
            mechanism,
            "CLAIM_SURFACE_BLOCKED",
            "conservative_candidate_blocked",
            False,
            "missing required gates: " + ", ".join(missing),
        )

    return Classification(
        mechanism,
        "SIGNED_RESPONSE_CANDIDATE",
        "conservative_candidate",
        True,
        "selector/source gates and locked two-body closure are explicitly passed",
    )


def print_taxonomy() -> None:
    rows = [
        ("locked_chi_response", "requires all gates", "CLAIM_SURFACE_BLOCKED unless all gates pass"),
        ("lensing_phase_flip", "interference", "LENSING_PHASE_ONLY"),
        ("complex_absorptive_away", "absorptive", "COMPLEX_ABSORPTIVE_ONLY"),
        ("boundary/proxy", "boundary_or_proxy", "BOUNDARY_PROXY_ONLY"),
        ("inserted_control_no_go", "inserted_control", "CONTROL_NO_GO"),
    ]
    print("SIGNED GRAVITY MECHANISM SEPARATOR")
    print("not negative mass, shielding, propulsion, or physical antigravity")
    print()
    print(f"{'mechanism':28s} {'class':22s} tag")
    print("-" * 82)
    for mechanism, mechanism_class, tag in rows:
        print(f"{mechanism:28s} {mechanism_class:22s} {tag}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Classify AWAY rows before any signed-gravity interpretation.",
    )
    parser.add_argument(
        "--mechanism",
        choices=MECHANISMS,
        help="Mechanism bucket for the AWAY or repulsive-looking row.",
    )
    parser.add_argument(
        "--selector-gate",
        choices=("pass", "blocked", "missing"),
        default="missing",
        help="Native/protected chi_g selector status.",
    )
    parser.add_argument(
        "--source-gate",
        choices=("pass", "blocked", "missing"),
        default="missing",
        help="Branch-stable signed source primitive status.",
    )
    parser.add_argument(
        "--locked-source-response",
        action="store_true",
        help="Require source and response signs to be locked by one label.",
    )
    parser.add_argument(
        "--two-body-action-reaction",
        action="store_true",
        help="Require two-body action-reaction closure.",
    )
    parser.add_argument(
        "--positive-inertial-mass",
        action="store_true",
        help="Require positive inertial mass in both branches.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.mechanism is None:
        print_taxonomy()
        return

    result = classify(args)
    print(f"MECHANISM: {result.mechanism}")
    print(f"CLASS: {result.mechanism_class}")
    print(f"TAG: {result.tag}")
    print(f"PROMOTABLE: {'yes' if result.promotable else 'no'}")
    print(f"REASON: {result.reason}")


if __name__ == "__main__":
    main()
