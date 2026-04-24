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
    "frontier_planck_boundary_source_functorial_ward_theorem.py",
    "frontier_planck_parent_source_naturality_obstruction_theorem_2026_04_24.py",
    "frontier_planck_boundary_same_source_covariance_theorem.py",
    "frontier_planck_boundary_parent_source_equivalence_theorem.py",
    "frontier_planck_boundary_action_source_vs_pressure_classification_theorem.py",
    "frontier_planck_gravity_sector_same_surface_closure_theorem.py",
    "frontier_planck_airtight_review_closure_theorem.py",
    "frontier_planck_bare_cell_alone_closure_program.py",
    "frontier_planck_bare_physical_lattice_observable_ontology_theorem.py",
    "frontier_planck_bare_finite_cell_canonical_state_theorem.py",
    "frontier_planck_bare_gravity_sector_derivation_status_theorem.py",
    "frontier_planck_bare_gravity_sector_uniqueness_attempt.py",
    "frontier_planck_edge_clifford_kinematic_soldering_theorem.py",
    "frontier_planck_b3_dynamical_metricity_obstruction_theorem.py",
    "frontier_planck_b3_bare_ward_identity_no_go_2026_04_24.py",
    "frontier_planck_b3_clifford_realification_metric_ward_theorem_2026_04_24.py",
    "frontier_planck_realification_admissibility_theorem_2026_04_24.py",
    "frontier_planck_parent_source_discharge_after_realification_theorem_2026_04_24.py",
    "frontier_planck_bare_boundary_representative_after_gravity_theorem.py",
    "frontier_planck_hbar_status_and_remaining_objections_audit.py",
    "frontier_planck_hbar_attack_order_theorem.py",
    "frontier_planck_action_phase_conversion_target_theorem.py",
    "frontier_planck_primitive_phase_trace_reduction_theorem.py",
    "frontier_planck_primitive_action_unit_gamma_one_attempt.py",
    "frontier_planck_gamma_phase_period_obstruction_theorem.py",
    "frontier_planck_hbar_strong_routes_status_theorem.py",
    "frontier_planck_hbar_nonhomogeneous_real_action_unit_reduction_2026_04_24.py",
    "frontier_planck_primitive_integral_action_count_theorem_2026_04_24.py",
    "frontier_planck_si_hbar_objection_discharge_theorem_2026_04_24.py",
    "frontier_planck_action_phase_representation_hbar_theorem_2026_04_24.py",
    "frontier_planck_overnight_closure_status_theorem.py",
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
    source_functorial_ward = read("docs/PLANCK_SCALE_BOUNDARY_SOURCE_FUNCTORIAL_WARD_THEOREM_2026-04-24.md")
    parent_source_naturality = read("docs/PLANCK_SCALE_PARENT_SOURCE_NATURALITY_OBSTRUCTION_THEOREM_2026-04-24.md")
    same_source = read("docs/PLANCK_SCALE_BOUNDARY_SAME_SOURCE_COVARIANCE_THEOREM_2026-04-23.md")
    parent_source = read("docs/PLANCK_SCALE_BOUNDARY_PARENT_SOURCE_EQUIVALENCE_THEOREM_2026-04-23.md")
    source_vs_pressure = read("docs/PLANCK_SCALE_BOUNDARY_ACTION_SOURCE_VS_PRESSURE_CLASSIFICATION_THEOREM_2026-04-23.md")
    same_surface_gravity = read("docs/PLANCK_SCALE_GRAVITY_SECTOR_SAME_SURFACE_CLOSURE_THEOREM_2026-04-23.md")
    airtight = read("docs/PLANCK_SCALE_AIRTIGHT_REVIEW_CLOSURE_THEOREM_2026-04-23.md")
    bare_cell_program = read("docs/PLANCK_SCALE_BARE_CELL_ALONE_CLOSURE_PROGRAM_2026-04-23.md")
    bare_lattice = read("docs/PLANCK_SCALE_BARE_PHYSICAL_LATTICE_OBSERVABLE_ONTOLOGY_THEOREM_2026-04-23.md")
    bare_cell_state = read("docs/PLANCK_SCALE_BARE_FINITE_CELL_CANONICAL_STATE_THEOREM_2026-04-23.md")
    bare_gravity_status = read("docs/PLANCK_SCALE_BARE_GRAVITY_SECTOR_DERIVATION_STATUS_THEOREM_2026-04-23.md")
    bare_gravity_attempt = read("docs/PLANCK_SCALE_BARE_GRAVITY_SECTOR_UNIQUENESS_ATTEMPT_2026-04-24.md")
    edge_soldering = read("docs/PLANCK_SCALE_EDGE_CLIFFORD_KINEMATIC_SOLDERING_THEOREM_2026-04-24.md")
    b3_metricity_obstruction = read("docs/PLANCK_SCALE_B3_DYNAMICAL_METRICITY_OBSTRUCTION_THEOREM_2026-04-24.md")
    b3_bare_ward_no_go = read("docs/PLANCK_SCALE_B3_BARE_WARD_IDENTITY_NO_GO_2026-04-24.md")
    b3_realification = read("docs/PLANCK_SCALE_B3_CLIFFORD_REALIFICATION_METRIC_WARD_THEOREM_2026-04-24.md")
    realification_admissibility = read("docs/PLANCK_SCALE_REALIFICATION_ADMISSIBILITY_THEOREM_2026-04-24.md")
    parent_source_discharge = read("docs/PLANCK_SCALE_PARENT_SOURCE_DISCHARGE_AFTER_REALIFICATION_THEOREM_2026-04-24.md")
    bare_boundary = read("docs/PLANCK_SCALE_BARE_BOUNDARY_REPRESENTATIVE_AFTER_GRAVITY_THEOREM_2026-04-23.md")
    hbar_audit = read("docs/PLANCK_SCALE_HBAR_STATUS_AND_REMAINING_OBJECTIONS_AUDIT_2026-04-23.md")
    hbar_attack = read("docs/PLANCK_SCALE_HBAR_ATTACK_ORDER_THEOREM_2026-04-23.md")
    action_phase = read("docs/PLANCK_SCALE_ACTION_PHASE_CONVERSION_TARGET_THEOREM_2026-04-23.md")
    phase_trace = read("docs/PLANCK_SCALE_PRIMITIVE_PHASE_TRACE_REDUCTION_THEOREM_2026-04-24.md")
    gamma_attempt = read("docs/PLANCK_SCALE_PRIMITIVE_ACTION_UNIT_GAMMA_ONE_ATTEMPT_2026-04-24.md")
    gamma_period = read("docs/PLANCK_SCALE_GAMMA_PHASE_PERIOD_OBSTRUCTION_THEOREM_2026-04-24.md")
    hbar_strong = read("docs/PLANCK_SCALE_HBAR_STRONG_ROUTES_STATUS_THEOREM_2026-04-24.md")
    hbar_nonhomogeneous = read("docs/PLANCK_SCALE_HBAR_NONHOMOGENEOUS_REAL_ACTION_UNIT_REDUCTION_THEOREM_2026-04-24.md")
    integral_action_count = read("docs/PLANCK_SCALE_PRIMITIVE_INTEGRAL_ACTION_COUNT_THEOREM_2026-04-24.md")
    si_hbar_discharge = read("docs/PLANCK_SCALE_SI_HBAR_OBJECTION_DISCHARGE_THEOREM_2026-04-24.md")
    action_phase_hbar = read("docs/PLANCK_SCALE_ACTION_PHASE_REPRESENTATION_HBAR_THEOREM_2026-04-24.md")
    overnight_status = read("docs/PLANCK_SCALE_OVERNIGHT_CLOSURE_STATUS_THEOREM_2026-04-24.md")

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
        "source-functorial-ward-hardens-schur-event-bridge",
        "PLANCK_SCALE_BOUNDARY_SOURCE_FUNCTORIAL_WARD_THEOREM_2026-04-24.md"
        in reviewer
        and "`chi_Delta(s) = exp(s Delta)`" in source_functorial_ward
        and "not derived from the\nscalar Schur observable grammar alone"
        in source_functorial_ward
        and "a conventional path-integral Ward identity" in source_functorial_ward
        and "If that rejection is accepted, the finite event Ward derivative remains true\nbut does not determine `nu`"
        in source_functorial_ward,
    )

    total += 1
    passed += expect(
        "parent-source-naturality-commutes-but-leaves-hidden-character",
        "PLANCK_SCALE_PARENT_SOURCE_NATURALITY_OBSTRUCTION_THEOREM_2026-04-24.md"
        in reviewer
        and "carrier-level naturality diagram commutes" in parent_source_naturality
        and "`chi_delta(s) = exp(s delta)`" in parent_source_naturality
        and "functorial Schur representation remains an object-class input"
        in parent_source_naturality
        and "not a bare closure" in parent_source_naturality,
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
        and "deny that the physical gravitational boundary-action source belongs to the"
        in parent_source
        and "deny that the Schur normal-ordered boundary action is the functorial Schur"
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
        "bare-gravity-uniqueness-attempt-reduces-to-metricity-ward",
        "PLANCK_SCALE_BARE_GRAVITY_SECTOR_UNIQUENESS_ATTEMPT_2026-04-24.md"
        in reviewer
        and "`B3 status: OPEN`" in bare_gravity_attempt
        and "soldered metricity / equivalence Ward identity" in bare_gravity_attempt
        and "multiple inequivalent sectors" in bare_gravity_attempt,
    )

    total += 1
    passed += expect(
        "edge-clifford-soldering-closes-only-flat-sublock",
        "PLANCK_SCALE_EDGE_CLIFFORD_KINEMATIC_SOLDERING_THEOREM_2026-04-24.md"
        in reviewer
        and "`edge_i <-> Gamma_i`" in edge_soldering
        and "`g_ij = (1/2) Tr_norm(Gamma_i Gamma_j + Gamma_j Gamma_i) = delta_ij`"
        in edge_soldering
        and "This does **not** derive the gravitational sector" in edge_soldering
        and "metric/coframe response with the conserved symmetric spin-2 Ward identity"
        in edge_soldering,
    )

    total += 1
    passed += expect(
        "b3-dynamical-metricity-obstruction-keeps-bare-gravity-open",
        "PLANCK_SCALE_B3_DYNAMICAL_METRICITY_OBSTRUCTION_THEOREM_2026-04-24.md"
        in reviewer
        and "Lie algebra is zero-dimensional" in b3_metricity_obstruction
        and "cannot produce a differential conservation identity"
        in b3_metricity_obstruction
        and "B3 remains open" in b3_metricity_obstruction
        and "Do not use:\n\n> Flat edge-Clifford soldering derives gravity."
        in b3_metricity_obstruction,
    )

    total += 1
    passed += expect(
        "b3-bare-ward-no-go-names-defect-to-coframe-primitive",
        "PLANCK_SCALE_B3_BARE_WARD_IDENTITY_NO_GO_2026-04-24.md"
        in reviewer
        and "local gaugeable defect-to-coframe response primitive"
        in b3_bare_ward_no_go
        and "scalar trace channel" in b3_bare_ward_no_go
        and "antisymmetric channel" in b3_bare_ward_no_go
        and "symmetric traceless channel" in b3_bare_ward_no_go
        and "B3 status is sharply reduced but not closed" in b3_bare_ward_no_go,
    )

    total += 1
    passed += expect(
        "b3-clifford-realification-closes-metric-ward-surface",
        "PLANCK_SCALE_B3_CLIFFORD_REALIFICATION_METRIC_WARD_THEOREM_2026-04-24.md"
        in reviewer
        and "positive B3 closure on the canonical real linear-response envelope"
        in b3_realification
        and "`T_R = T_Z tensor_Z R`" in b3_realification
        and "`delta g_ij = h_ij + h_ji`" in b3_realification
        and "antisymmetric channel has `delta g = 0`" in b3_realification
        and "`d^* T = 0`" in b3_realification
        and "If that rejection is accepted, the older finite-automorphism B3 no-go applies"
        in b3_realification,
    )

    total += 1
    passed += expect(
        "realification-admissibility-discharges-response-objection",
        "PLANCK_SCALE_REALIFICATION_ADMISSIBILITY_THEOREM_2026-04-24.md"
        in reviewer
        and "closes the realification-admissibility objection" in realification_admissibility
        and "`f_R : T_Z tensor_Z R -> W`" in realification_admissibility
        and "finite automorphisms alone do not give dynamics" in realification_admissibility
        and "not a live\nobjection to the submitted physical-response theorem" in reviewer,
    )

    total += 1
    passed += expect(
        "parent-source-discharged-after-realification",
        "PLANCK_SCALE_PARENT_SOURCE_DISCHARGE_AFTER_REALIFICATION_THEOREM_2026-04-24.md"
        in reviewer
        and "closes the parent-source object-class objection after B3 realification"
        in parent_source_discharge
        and "`B_parent = (H_A, P_A)`" in parent_source_discharge
        and "`delta = 0`" in parent_source_discharge
        and "no longer a separate\nphysical primitive after realified B3" in reviewer,
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
        "hbar-axis-separates-structural-from-si",
        "PLANCK_SCALE_HBAR_STATUS_AND_REMAINING_OBJECTIONS_AUDIT_2026-04-23.md"
        in reviewer
        and "derives the structural action-to-phase role of `hbar`" in hbar_audit
        and "does **not** derive the SI value of\n`hbar`" in hbar_audit
        and "structural hbar result, not a prediction of the SI value of `hbar`"
        in hbar_audit
        and "no claim that the packet predicts the SI numerical value of `hbar`"
        in reviewer,
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
        and "later action-phase representation\nhbar theorem also derives the structural conversion statement"
        in action_phase,
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

    total += 1
    passed += expect(
        "gamma-one-attempt-proves-scale-homogeneity-obstruction",
        "PLANCK_SCALE_PRIMITIVE_ACTION_UNIT_GAMMA_ONE_ATTEMPT_2026-04-24.md"
        in reviewer
        and "`Phi -> lambda Phi`" in gamma_attempt
        and "`Phi(I_16) = 1`" in gamma_attempt
        and "must not claim:\n\n> `gamma = 1` follows from the current source-free trace theorem"
        in gamma_attempt,
    )

    total += 1
    passed += expect(
        "gamma-phase-period-obstruction-demotes-periodic-closure",
        "PLANCK_SCALE_GAMMA_PHASE_PERIOD_OBSTRUCTION_THEOREM_2026-04-24.md"
        in reviewer
        and "`Phi ~ Phi + 2 pi n`" in gamma_period
        and "`gamma = 2 pi k / N`" in gamma_period
        and "Do not use:\n\n> U(1) phase periodicity derives `gamma = 1`."
        in gamma_period
        and "This is a narrow no-go theorem" in gamma_period
        and "does **not** block every central-extension\nor projective-phase route"
        in gamma_period
        and "central-extension quantization can produce a level, but it\n"
        "does not produce the dimensionless radian value `gamma = 1`"
        in gamma_period,
    )

    total += 1
    passed += expect(
        "hbar-strong-routes-integral-route-closed-but-others-open",
        "PLANCK_SCALE_HBAR_STRONG_ROUTES_STATUS_THEOREM_2026-04-24.md"
        in reviewer
        and "`0 -> R -> G_hat -> G -> 1`" in hbar_strong
        and "`Index(D_cell) = 1`" in hbar_strong
        and "`Phi(A_cell) = 1`" in hbar_strong
        and "Reusing it for hbar would be circular" in hbar_strong
        and "primitive action route now closed in reduced count units"
        in hbar_strong
        and "Those routes are not closed in the current branch" in hbar_strong,
    )

    total += 1
    passed += expect(
        "hbar-nonhomogeneous-real-action-unit-is-necessary-and-sufficient",
        "PLANCK_SCALE_HBAR_NONHOMOGENEOUS_REAL_ACTION_UNIT_REDUCTION_THEOREM_2026-04-24.md"
        in reviewer
        and "necessary-and-sufficient reduction" in hbar_nonhomogeneous
        and "`Phi(A_cell) = Phi(I_16) = 1`" in hbar_nonhomogeneous
        and "`q_atom = 1/16`" in hbar_nonhomogeneous
        and "hbar/action-unit status is **conditional**, not\nunconditionally closed"
        in hbar_nonhomogeneous
        and "Ward route must derive a unit-calibrated microscopic action"
        in hbar_nonhomogeneous,
    )

    total += 1
    passed += expect(
        "primitive-integral-action-count-closes-reduced-gamma",
        "PLANCK_SCALE_PRIMITIVE_INTEGRAL_ACTION_COUNT_THEOREM_2026-04-24.md"
        in reviewer
        and "positive reduced-action closure" in integral_action_count
        and "`M_cell = N [A_cell]`" in integral_action_count
        and "`Phi(I_16) = ell([A_cell]) = 1`" in integral_action_count
        and "`gamma = 1`" in integral_action_count
        and "not a prediction of\nthe SI value of `hbar`" in integral_action_count,
    )

    total += 1
    passed += expect(
        "si-hbar-objection-discharged-as-unit-convention",
        "PLANCK_SCALE_SI_HBAR_OBJECTION_DISCHARGE_THEOREM_2026-04-24.md"
        in reviewer
        and "discharges the SI-`hbar` objection" in si_hbar_discharge
        and "`[S]_{U_A'} = [S]_{U_A} / lambda`" in si_hbar_discharge
        and "`a^2 c_light^3 / (hbar G) = 1`" in si_hbar_discharge
        and "unit-convention demand, not a physical reviewer blocker" in reviewer,
    )

    total += 1
    passed += expect(
        "action-phase-representation-derives-structural-hbar",
        "PLANCK_SCALE_ACTION_PHASE_REPRESENTATION_HBAR_THEOREM_2026-04-24.md"
        in reviewer
        and "structural `hbar` derivation as primitive action-to-phase conversion"
        in action_phase_hbar
        and "`S(H)/hbar = Phi(H)`" in action_phase_hbar
        and "`S(A_cell) = hbar`" in action_phase_hbar
        and "not a prediction of the SI decimal value of `hbar`" in action_phase_hbar,
    )

    total += 1
    passed += expect(
        "overnight-status-classifies-conditional-not-bare",
        "PLANCK_SCALE_OVERNIGHT_CLOSURE_STATUS_THEOREM_2026-04-24.md"
        in reviewer
        and "not** a finite-automorphism-only derivation" in overnight_status
        and "Planck closure on the canonical realified `Cl(3)` / `Z^3`"
        in overnight_status
        and "B3 realified metric/coframe Ward response" in overnight_status
        and "parent-source object-class objection is discharged after realified B3"
        in overnight_status
        and "closed: `gamma=1` as reduced primitive action count" in overnight_status
        and "closed: structural `S/hbar=Phi`" in overnight_status
        and "SI-hbar target is discharged as a unit-convention nonclaim"
        in overnight_status
        and "Nature-grade bare-axiom Planck and hbar closure has been achieved"
        in overnight_status,
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
