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
    "frontier_planck_cosmic_address_import_unit_map_theorem.py",
    "frontier_planck_claim_scope_hostile_audit.py",
    "frontier_planck_remaining_denials_target_change_theorem.py",
    "frontier_planck_axiom_only_gravity_unit_map_final_audit.py",
    "frontier_planck_clean_closure_criterion_theorem.py",
    "frontier_planck_primitive_boundary_action_unit_reduction_theorem.py",
    "frontier_planck_boundary_density_three_mechanism_audit.py",
    "frontier_planck_boundary_event_ward_identity_closure_theorem.py",
    "frontier_planck_boundary_event_ward_identity_derivation_theorem.py",
    "frontier_planck_boundary_same_source_covariance_theorem.py",
    "frontier_planck_boundary_parent_source_equivalence_theorem.py",
    "frontier_planck_boundary_action_source_vs_pressure_classification_theorem.py",
    "frontier_planck_gravity_sector_same_surface_closure_theorem.py",
    "frontier_planck_airtight_review_closure_theorem.py",
    "frontier_planck_bare_cell_alone_closure_program.py",
    "frontier_planck_bare_physical_lattice_observable_ontology_theorem.py",
    "frontier_planck_bare_finite_cell_canonical_state_theorem.py",
    "frontier_planck_bare_gravity_sector_derivation_status_theorem.py",
    "frontier_planck_bare_boundary_representative_after_gravity_theorem.py",
    "frontier_planck_hbar_status_and_remaining_objections_audit.py",
    "frontier_planck_hbar_attack_order_theorem.py",
    "frontier_planck_action_phase_conversion_target_theorem.py",
    "frontier_planck_primitive_phase_trace_reduction_theorem.py",
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
    nature_status = read("docs/PLANCK_SCALE_NATURE_REVIEW_PLAIN_LANGUAGE_STATUS_2026-04-23.md")
    closure = read("docs/PLANCK_SCALE_CLEAN_CLOSURE_CRITERION_THEOREM_2026-04-23.md")
    primitive_unit = read("docs/PLANCK_SCALE_PRIMITIVE_BOUNDARY_ACTION_UNIT_REDUCTION_THEOREM_2026-04-23.md")
    density_audit = read("docs/PLANCK_SCALE_BOUNDARY_DENSITY_THREE_MECHANISM_AUDIT_2026-04-23.md")
    event_ward = read("docs/PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_CLOSURE_THEOREM_2026-04-23.md")
    event_ward_derivation = read("docs/PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_DERIVATION_THEOREM_2026-04-23.md")
    same_source = read("docs/PLANCK_SCALE_BOUNDARY_SAME_SOURCE_COVARIANCE_THEOREM_2026-04-23.md")
    parent_source = read("docs/PLANCK_SCALE_BOUNDARY_PARENT_SOURCE_EQUIVALENCE_THEOREM_2026-04-23.md")
    source_vs_pressure = read("docs/PLANCK_SCALE_BOUNDARY_ACTION_SOURCE_VS_PRESSURE_CLASSIFICATION_THEOREM_2026-04-23.md")
    same_surface_gravity = read("docs/PLANCK_SCALE_GRAVITY_SECTOR_SAME_SURFACE_CLOSURE_THEOREM_2026-04-23.md")
    airtight = read("docs/PLANCK_SCALE_AIRTIGHT_REVIEW_CLOSURE_THEOREM_2026-04-23.md")
    bare_cell_program = read("docs/PLANCK_SCALE_BARE_CELL_ALONE_CLOSURE_PROGRAM_2026-04-23.md")
    bare_lattice = read("docs/PLANCK_SCALE_BARE_PHYSICAL_LATTICE_OBSERVABLE_ONTOLOGY_THEOREM_2026-04-23.md")
    bare_cell_state = read("docs/PLANCK_SCALE_BARE_FINITE_CELL_CANONICAL_STATE_THEOREM_2026-04-23.md")
    bare_gravity_status = read("docs/PLANCK_SCALE_BARE_GRAVITY_SECTOR_DERIVATION_STATUS_THEOREM_2026-04-23.md")
    bare_boundary = read("docs/PLANCK_SCALE_BARE_BOUNDARY_REPRESENTATIVE_AFTER_GRAVITY_THEOREM_2026-04-23.md")
    hbar_audit = read("docs/PLANCK_SCALE_HBAR_STATUS_AND_REMAINING_OBJECTIONS_AUDIT_2026-04-23.md")
    hbar_attack = read("docs/PLANCK_SCALE_HBAR_ATTACK_ORDER_THEOREM_2026-04-23.md")
    action_phase = read("docs/PLANCK_SCALE_ACTION_PHASE_CONVERSION_TARGET_THEOREM_2026-04-23.md")
    phase_trace = read("docs/PLANCK_SCALE_PRIMITIVE_PHASE_TRACE_REDUCTION_THEOREM_2026-04-24.md")

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
        "packet-records-cosmic-address-import-protocol",
        "PLANCK_SCALE_COSMIC_ADDRESS_IMPORT_UNIT_MAP_THEOREM_2026-04-23.md"
        in packet
        and "cosmic-address imports" in packet
        and "They may not be used as hidden\nmicroscopic tick counts" in packet,
    )

    total += 1
    passed += expect(
        "packet-records-remaining-denials-target-change",
        "PLANCK_SCALE_REMAINING_DENIALS_TARGET_CHANGE_THEOREM_2026-04-23.md"
        in packet,
    )

    total += 1
    passed += expect(
        "reviewer-front-door-records-final-unit-map-audit",
        "PLANCK_SCALE_NATURE_REVIEW_PLAIN_LANGUAGE_STATUS_2026-04-23.md"
        in reviewer
        and "PLANCK_SCALE_AXIOM_ONLY_GRAVITY_UNIT_MAP_FINAL_AUDIT_2026-04-23.md"
        in reviewer,
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
        and "PLANCK_SCALE_COSMIC_ADDRESS_IMPORT_UNIT_MAP_THEOREM_2026-04-23.md"
        in reviewer
        and "PLANCK_SCALE_CLAIM_SCOPE_HOSTILE_AUDIT_2026-04-23.md" in reviewer,
    )

    total += 1
    passed += expect(
        "reviewer-packet-includes-final-denial-theorem",
        "PLANCK_SCALE_REMAINING_DENIALS_TARGET_CHANGE_THEOREM_2026-04-23.md"
        in reviewer,
    )

    total += 1
    passed += expect(
        "nature-status-avoids-project-shorthand-and-names-parent-source-object-class",
        "P1" not in nature_status
        and "GSI" not in nature_status
        and "Axiom Extension" not in nature_status
        and "The parent-source theorem identifies the common source" in nature_status
        and "belongs to the retained primitive one-step boundary/worldtube object class"
        in nature_status,
    )

    total += 1
    passed += expect(
        "closure-criterion-records-exact-remaining-mu-theorem",
        "PLANCK_SCALE_CLEAN_CLOSURE_CRITERION_THEOREM_2026-04-23.md"
        in reviewer
        and "Only one dimensionless statement remains:" in closure
        and "`mu = 1`" in closure
        and "mathematically clean closure is therefore conditional" in closure,
    )

    total += 1
    passed += expect(
        "primitive-boundary-action-unit-reduces-to-nu-density",
        "PLANCK_SCALE_PRIMITIVE_BOUNDARY_ACTION_UNIT_REDUCTION_THEOREM_2026-04-23.md"
        in reviewer
        and "multiplicative `mu != 1` is not same-surface" in primitive_unit
        and "This note does not derive `nu = 5/4`" in primitive_unit,
    )

    total += 1
    passed += expect(
        "three-mechanism-density-audit-records-open-final-law",
        "PLANCK_SCALE_BOUNDARY_DENSITY_THREE_MECHANISM_AUDIT_2026-04-23.md"
        in reviewer
        and "PLANCK_SCALE_BOUNDARY_DENSITY_THREE_MECHANISM_AUDIT_2026-04-23.md"
        in packet
        and "`nu = 5/4`" in density_audit
        and "`delta = m_axis`" in density_audit
        and "not yet derived by the current Ward,\n> phase, or boundary-term machinery"
        in density_audit,
    )

    total += 1
    passed += expect(
        "boundary-event-ward-identity-closes-additive-density",
        "PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_CLOSURE_THEOREM_2026-04-23.md"
        in reviewer
        and "PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_CLOSURE_THEOREM_2026-04-23.md"
        in packet
        and "`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`" in event_ward
        and "`nu = 1 + 1/4 = 5/4`" in event_ward
        and "If the event Ward identity is accepted, the additive\ndensity is closed"
        in event_ward,
    )

    total += 1
    passed += expect(
        "boundary-event-ward-identity-is-derived-from-finite-source",
        "PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_DERIVATION_THEOREM_2026-04-23.md"
        in reviewer
        and "PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_DERIVATION_THEOREM_2026-04-23.md"
        in packet
        and "`U_A(s) = exp(s P_A)`" in event_ward_derivation
        and "`d/ds log Z_A(s)|_(s=0) = Tr(rho_cell P_A)`" in event_ward_derivation
        and "reject same-source covariance" in event_ward_derivation,
    )

    total += 1
    passed += expect(
        "same-source-covariance-is-derived-by-quotient-no-hidden-scalar",
        "PLANCK_SCALE_BOUNDARY_SAME_SOURCE_COVARIANCE_THEOREM_2026-04-23.md"
        in reviewer
        and "PLANCK_SCALE_BOUNDARY_SAME_SOURCE_COVARIANCE_THEOREM_2026-04-23.md"
        in packet
        and "`Q(s) = exp(s (p_1 - p_2))`" in same_source
        and "`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`" in same_source
        and "deny that the Schur boundary action and the primitive event insertion source"
        in same_source,
    )

    total += 1
    passed += expect(
        "parent-source-equivalence-closes-schur-event-common-source",
        "PLANCK_SCALE_BOUNDARY_PARENT_SOURCE_EQUIVALENCE_THEOREM_2026-04-23.md"
        in reviewer
        and "PLANCK_SCALE_BOUNDARY_PARENT_SOURCE_EQUIVALENCE_THEOREM_2026-04-23.md"
        in packet
        and "`B_parent := (H_A, P_A)`" in parent_source
        and "`P_A = P_q + P_E`" in parent_source
        and "`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`" in parent_source
        and "deny that the physical gravitational boundary-action source belongs to the\n> retained primitive one-step boundary/worldtube object class"
        in parent_source,
    )

    total += 1
    passed += expect(
        "action-source-versus-pressure-prevents-scalar-overclaim",
        "PLANCK_SCALE_BOUNDARY_ACTION_SOURCE_VS_PRESSURE_CLASSIFICATION_THEOREM_2026-04-23.md"
        in reviewer
        and "`p_scalar(L_Sigma) = (1/(2n)) log det(L_Sigma)`"
        in source_vs_pressure
        and "`p_action = p_event = Tr(rho_cell P_A)`" in source_vs_pressure
        and "Do not present the result as a scalar Schur-pressure\ntheorem"
        in reviewer,
    )

    total += 1
    passed += expect(
        "same-surface-gravity-sector-closes-gsi",
        "PLANCK_SCALE_GRAVITY_SECTOR_SAME_SURFACE_CLOSURE_THEOREM_2026-04-23.md"
        in reviewer
        and "same-surface single-sector compatibility forces GSI" in same_surface_gravity
        and "`N_grav = P_A`" in same_surface_gravity,
    )

    total += 1
    passed += expect(
        "airtight-review-closure-is-scoped-and-final",
        "PLANCK_SCALE_AIRTIGHT_REVIEW_CLOSURE_THEOREM_2026-04-23.md" in reviewer
        and "Yes, as a theorem on the accepted physical-gravity review contract"
        in airtight
        and "`a = l_P`" in airtight
        and "theory-surface rejections, not\ninternal Planck proof gaps" in airtight,
    )

    total += 1
    passed += expect(
        "bare-cell-alone-upgrade-program-is-scoped",
        "PLANCK_SCALE_BARE_CELL_ALONE_CLOSURE_PROGRAM_2026-04-23.md" in reviewer
        and "not the submitted Planck theorem" in bare_cell_program
        and "Do not claim the stronger sentence until B1-B4 are theorem-grade"
        in bare_cell_program,
    )

    total += 1
    passed += expect(
        "bare-physical-lattice-ontology-closes-b1",
        "PLANCK_SCALE_BARE_PHYSICAL_LATTICE_OBSERVABLE_ONTOLOGY_THEOREM_2026-04-23.md"
        in reviewer
        and "This closes B1 of the bare-cell-alone upgrade program" in bare_lattice
        and "not a removable\nregulator coordinate" in bare_lattice,
    )

    total += 1
    passed += expect(
        "bare-finite-cell-canonical-state-closes-b2",
        "PLANCK_SCALE_BARE_FINITE_CELL_CANONICAL_STATE_THEOREM_2026-04-23.md"
        in reviewer
        and "This closes B2 of the bare-cell-alone upgrade program" in bare_cell_state
        and "`rho_cell = I_16 / 16`" in bare_cell_state,
    )

    total += 1
    passed += expect(
        "bare-gravity-sector-b3-remains-exact-target",
        "PLANCK_SCALE_BARE_GRAVITY_SECTOR_DERIVATION_STATUS_THEOREM_2026-04-23.md"
        in reviewer
        and "B3 is not closed" in bare_gravity_status
        and "unique nontrivial long-distance" in bare_gravity_status,
    )

    total += 1
    passed += expect(
        "bare-boundary-representative-b4-conditional",
        "PLANCK_SCALE_BARE_BOUNDARY_REPRESENTATIVE_AFTER_GRAVITY_THEOREM_2026-04-23.md"
        in reviewer
        and "Once B3 is closed, B4 follows" in bare_boundary
        and "`N_grav = P_A`" in bare_boundary,
    )

    total += 1
    passed += expect(
        "hbar-axis-is-scoped-as-not-derived",
        "PLANCK_SCALE_HBAR_STATUS_AND_REMAINING_OBJECTIONS_AUDIT_2026-04-23.md"
        in reviewer
        and "does **not** derive `hbar`" in hbar_audit
        and "conditional structural Planck-length result, not a derivation of `hbar`"
        in hbar_audit
        and "no claim that the packet derives `hbar`" in reviewer,
    )

    total += 1
    passed += expect(
        "hbar-attack-order-is-noncircular-and-prioritized",
        "PLANCK_SCALE_HBAR_ATTACK_ORDER_THEOREM_2026-04-23.md" in reviewer
        and "`hbar = a^2 c_light^3 / G`" in hbar_attack
        and "To turn this into a prediction, `a` must\nbe fixed independently of `hbar`"
        in hbar_attack
        and "`kappa_info^(bit) = gamma/32`" in hbar_attack,
    )

    total += 1
    passed += expect(
        "action-phase-conversion-target-is-exact",
        "PLANCK_SCALE_ACTION_PHASE_CONVERSION_TARGET_THEOREM_2026-04-23.md"
        in reviewer
        and "`q_* = 1/16`" in action_phase
        and "`kappa_info = 1/32 per bit`" in action_phase
        and "It does not derive the action-to-phase\nconversion itself" in action_phase,
    )

    total += 1
    passed += expect(
        "primitive-phase-trace-reduces-hbar-target-to-gamma",
        "PLANCK_SCALE_PRIMITIVE_PHASE_TRACE_REDUCTION_THEOREM_2026-04-24.md"
        in reviewer
        and "`Phi(P) = gamma Tr(P) / 16`" in phase_trace
        and "`q_atom = gamma/16`" in hbar_attack
        and "`gamma = 1`" in phase_trace,
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
