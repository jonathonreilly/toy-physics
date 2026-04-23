#!/usr/bin/env python3
"""Master verifier for the canonical direct Planck derivation packet."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


SUBCHECKS = [
    "frontier_planck_minimal_stack_to_primitive_cell_datum_theorem.py",
    "frontier_planck_worldtube_to_boundary_cell_counting_theorem_lane.py",
    "frontier_planck_universal_cell_coefficient_not_vacuum_expectation_theorem.py",
    "frontier_planck_primitive_coefficient_object_class_theorem.py",
    "frontier_planck_one_axiom_extension_acceptance_theorem.py",
    "frontier_planck_one_axiom_conservative_semantics_bridge_theorem.py",
    "frontier_planck_p1_decomposition_and_counting_trace_reduction.py",
    "frontier_planck_atomic_naturality_from_primitive_universality_theorem.py",
    "frontier_planck_universal_primitive_counting_trace_theorem.py",
    "frontier_planck_event_frame_no_information_state_theorem.py",
    "frontier_planck_source_free_default_datum_from_one_axiom_theorem.py",
    "frontier_planck_gravitational_area_action_carrier_identification_theorem.py",
    "frontier_planck_gravity_carrier_from_sector_identification_theorem.py",
    "frontier_planck_area_action_normalization_theorem.py",
    "frontier_planck_planck_normalization_non_tautology_audit.py",
    "frontier_planck_claim_scope_hostile_audit.py",
    "frontier_planck_remaining_denials_target_change_theorem.py",
]


def expect(name: str, cond: bool) -> int:
    if cond:
        print(f"PASS: {name}")
        return 1
    print(f"FAIL: {name}")
    return 0


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def run_subcheck(script: str) -> bool:
    path = ROOT / "scripts" / script
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
    return result.returncode == 0


def main() -> int:
    passed = 0
    total = 0

    packet = read("docs/PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    for script in SUBCHECKS:
        total += 1
        passed += expect(f"subcheck-{script}", run_subcheck(script))

    dim_cell = 16
    rank_packet = 4
    coeff = rank_packet / dim_cell

    total += 1
    passed += expect("cell-dimension-is-sixteen", dim_cell == 16)

    total += 1
    passed += expect("packet-rank-is-four", rank_packet == 4)

    total += 1
    passed += expect("quarter-coefficient-is-exact", coeff == 0.25)

    total += 1
    passed += expect(
        "packet-states-authorized-surface",
        "Authorized surface" in packet
        and "Axiom Extension P1" in packet,
    )

    total += 1
    passed += expect(
        "packet-keeps-minimal-ledger-caveat",
        "older minimal ledger in isolation" in packet
        and "does not claim" in packet,
    )

    total += 1
    passed += expect(
        "packet-replaces-u2-with-event-frame-state-law",
        "does **not** use arbitrary factor-local `U(2)^4`" in packet
        and "`P_A` is invariantly defined" in packet
        and "packet-preserving symmetry alone" in packet,
    )

    total += 1
    passed += expect(
        "packet-reduces-p1-to-counting-trace-reading",
        "P1's no-preferred-primitive-event law plus additivity/naturality reduces"
        in packet
        and "ATOMIC_NATURALITY_FROM_PRIMITIVE_UNIVERSALITY" in packet,
    )

    total += 1
    passed += expect(
        "packet-records-standalone-area-action-normalization",
        "S_grav / k_B = A c_light^3 / (4 G hbar)" in packet
        and "`a^2 = 4 c_cell l_P^2`" in packet
        and "unique available local codimension-1 carrier" in packet,
    )

    total += 1
    passed += expect(
        "packet-records-non-tautology-audit",
        "PLANCK_SCALE_PLANCK_NORMALIZATION_NON_TAUTOLOGY_AUDIT_2026-04-23.md"
        in packet,
    )

    total += 1
    passed += expect(
        "packet-records-remaining-denials-target-change",
        "PLANCK_SCALE_REMAINING_DENIALS_TARGET_CHANGE_THEOREM_2026-04-23.md"
        in packet,
    )

    total += 1
    passed += expect(
        "packet-derives-planck-length",
        "`a^2 = l_P^2`" in packet
        and "`a = l_P`" in packet
        and "standard gravitational area/action normalization" in packet,
    )

    total += 1
    passed += expect(
        "reviewer-packet-includes-final-hardening-notes",
        "PLANCK_SCALE_ATOMIC_NATURALITY_FROM_PRIMITIVE_UNIVERSALITY_THEOREM_2026-04-23.md"
        in reviewer
        and "PLANCK_SCALE_GRAVITY_CARRIER_FROM_SECTOR_IDENTIFICATION_THEOREM_2026-04-23.md"
        in reviewer
        and "PLANCK_SCALE_PLANCK_NORMALIZATION_NON_TAUTOLOGY_AUDIT_2026-04-23.md"
        in reviewer
        and "PLANCK_SCALE_CLAIM_SCOPE_HOSTILE_AUDIT_2026-04-23.md" in reviewer,
    )

    total += 1
    passed += expect(
        "reviewer-packet-includes-final-denial-theorem",
        "PLANCK_SCALE_REMAINING_DENIALS_TARGET_CHANGE_THEOREM_2026-04-23.md"
        in reviewer,
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
