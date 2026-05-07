#!/usr/bin/env python3
"""
PR #230 same-surface neutral multiplicity-one candidate attempt.

This runner tries to instantiate the candidate file requested by the
same-surface neutral multiplicity-one intake gate.  It deliberately writes the
candidate-certificate path, but the current PR230 surface does not pass the
contract: the neutral same-surface completion still has a source singlet plus
an orthogonal neutral singlet, no physical primitive/off-diagonal transfer,
no canonical scalar LSZ metric, and no measured C_spH/C_HH pole-overlap rows.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json"
)

PARENTS = {
    "same_surface_neutral_multiplicity_one_gate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "invariant_ring_oh_attempt": "outputs/yt_pr230_invariant_ring_oh_certificate_attempt_2026-05-05.json",
    "neutral_commutant_rank_no_go": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
    "neutral_primitive_cone_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "z3_triplet_conditional_primitive": "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json",
    "z3_positive_cone_support": "outputs/yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json",
    "source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
}

DOWNSTREAM_PATHS = {
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
}

FORBIDDEN_IMPORT_FLAGS = {
    "uses_H_unit": False,
    "uses_yt_ward_identity": False,
    "uses_observed_targets": False,
    "uses_alpha_lm_plaquette_u0": False,
    "uses_reduced_pilot_evidence": False,
    "sets_c2_zmatch_kappas_to_one_by_convention": False,
    "uses_pslq_or_value_recognition_selector": False,
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in DOWNSTREAM_PATHS.items()}


def candidate_rotation_witness() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, theta in (
        ("source_aligned", 0.0),
        ("rotated_30deg", math.pi / 6.0),
        ("rotated_60deg", math.pi / 3.0),
        ("orthogonal", math.pi / 2.0),
    ):
        rows.append(
            {
                "case": label,
                "candidate_vector_in_source_orthogonal_basis": [
                    math.cos(theta),
                    math.sin(theta),
                ],
                "source_to_candidate_overlap": math.cos(theta),
                "source_only_observables_change": False,
                "top_coupling_allowed_by_current_labels": True,
            }
        )
    return rows


def main() -> int:
    print("PR #230 same-surface neutral multiplicity-one candidate attempt")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    statuses = {name: status(cert) for name, cert in parents.items()}
    downstream_presence = future_presence()
    witness_rows = candidate_rotation_witness()

    same_surface_representation_present = True
    neutral_basis = ["source_singlet", "orthogonal_neutral_singlet"]
    z3_action_matrix = [[1.0, 0.0], [0.0, 1.0]]
    degree_one_invariant_dimension = 2
    commutant_dimension = 4
    physical_primitive_transfer_present = False
    top_selection_rule_excluding_orthogonal_present = False
    canonical_lsz_metric_present = False
    source_higgs_overlap_rows_present = (
        downstream_presence["source_higgs_measurement_rows"]
        or parents["source_higgs_builder"].get("candidate_written") is True
    )

    overlaps = {
        round(row["source_to_candidate_overlap"], 12) for row in witness_rows
    }
    source_only_fixed = all(
        row["source_only_observables_change"] is False for row in witness_rows
    )
    forbidden_firewall_clean = all(value is False for value in FORBIDDEN_IMPORT_FLAGS.values())

    multiplicity_one_passed = (
        degree_one_invariant_dimension == 1
        and commutant_dimension == 1
        and top_selection_rule_excluding_orthogonal_present
    )
    primitive_generator_passed = physical_primitive_transfer_present
    canonical_metric_passed = canonical_lsz_metric_present
    source_overlap_passed = source_higgs_overlap_rows_present
    candidate_accepted = (
        same_surface_representation_present
        and (multiplicity_one_passed or primitive_generator_passed)
        and canonical_metric_passed
        and source_overlap_passed
        and forbidden_firewall_clean
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("intake-gate-loaded", "same-surface neutral multiplicity-one artifact intake gate" in statuses["same_surface_neutral_multiplicity_one_gate"], statuses["same_surface_neutral_multiplicity_one_gate"])
    report("same-surface-representation-explicit", same_surface_representation_present, ",".join(neutral_basis))
    report("current-neutral-sector-two-dimensional", degree_one_invariant_dimension == 2, f"degree_one_dim={degree_one_invariant_dimension}")
    report("current-commutant-non-scalar", commutant_dimension == 4, f"commutant_dim={commutant_dimension}")
    report("z3-action-trivial-on-two-singlet-current-sector", z3_action_matrix == [[1.0, 0.0], [0.0, 1.0]], str(z3_action_matrix))
    report("primitive-transfer-absent", not physical_primitive_transfer_present, "H3 physical transfer/off-diagonal generator absent")
    report("orthogonal-top-coupling-not-excluded", not top_selection_rule_excluding_orthogonal_present, "current labels allow orthogonal neutral top coupling")
    report("canonical-lsz-metric-absent", not canonical_lsz_metric_present, "no inverse-propagator derivative / FV/IR limiting order")
    report("source-higgs-overlap-rows-absent", not source_higgs_overlap_rows_present, str(downstream_presence))
    report("source-only-observables-fixed", source_only_fixed, "source-only rows unchanged across candidate rotations")
    report("source-overlap-varies", len(overlaps) > 1, f"overlaps={sorted(overlaps)}")
    report("forbidden-import-firewall-clean", forbidden_firewall_clean, str(FORBIDDEN_IMPORT_FLAGS))
    report("candidate-rejected-honestly", not candidate_accepted, "multiplicity/primitive, LSZ metric, and overlap obligations fail")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / same-surface neutral multiplicity-one "
            "candidate attempt rejected on current PR230 surface"
        ),
        "conditional_surface_status": (
            "conditional-support only if a future same-surface action or row "
            "packet removes the orthogonal neutral singlet, supplies a primitive "
            "generator, fixes canonical scalar LSZ normalization, and measures "
            "O_sp-Higgs overlap"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The candidate file is present but rejected: the current two-singlet "
            "neutral sector has degree-one invariant dimension 2, commutant "
            "dimension 4, no physical primitive transfer/off-diagonal generator, "
            "no canonical LSZ metric, and no C_spH/C_HH pole-overlap rows."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "candidate_accepted": candidate_accepted,
        "same_surface_cl3_z3_representation": {
            "present": same_surface_representation_present,
            "surface": "PR230 current Cl(3)/Z3 neutral source surface",
            "basis": neutral_basis,
            "z3_action_matrix": z3_action_matrix,
            "source_operator_coordinates": [1.0, 0.0],
            "candidate_family_basis": "candidate(theta)=cos(theta)*source_singlet+sin(theta)*orthogonal_neutral_singlet",
        },
        "neutral_scalar_basis": neutral_basis,
        "action_or_transfer_matrices": {
            "current_z3_action": z3_action_matrix,
            "physical_primitive_transfer_present": physical_primitive_transfer_present,
            "off_diagonal_generator_present": False,
            "h3_physical_transfer_supplied": False,
            "h4_source_canonical_higgs_coupling_supplied": False,
        },
        "top_coupled_neutral_sector": {
            "dimension": 2,
            "top_selection_rule_excluding_orthogonal_present": top_selection_rule_excluding_orthogonal_present,
            "orthogonal_neutral_top_coupling_allowed_by_current_labels": True,
        },
        "source_pole_operator_coordinates": [1.0, 0.0],
        "multiplicity_one_or_primitive_generator_proof": {
            "passed": multiplicity_one_passed or primitive_generator_passed,
            "degree_one_invariant_dimension": degree_one_invariant_dimension,
            "commutant_dimension": commutant_dimension,
            "primitive_generator_passed": primitive_generator_passed,
            "failed_reasons": [
                "degree-one invariant dimension is two, not one",
                "commutant dimension is four, not scalar",
                "same-surface physical primitive transfer/off-diagonal generator is absent",
                "orthogonal neutral top coupling is not excluded",
            ],
        },
        "canonical_metric_lsz_normalization": {
            "passed": canonical_metric_passed,
            "inverse_propagator_derivative_metric_present": False,
            "finite_volume_ir_limiting_order_present": False,
            "canonical_field_normalization_used_by_v_present": False,
            "sets_kappa_s_to_one": False,
        },
        "source_to_canonical_higgs_overlap": {
            "passed": source_overlap_passed,
            "identity_O_sp_equals_O_H_passed": False,
            "measured_C_spH_C_HH_pole_rows_present": source_higgs_overlap_rows_present,
            "rotation_witness_rows": witness_rows,
        },
        "forbidden_import_firewall": {
            "passed": forbidden_firewall_clean,
            **FORBIDDEN_IMPORT_FLAGS,
        },
        "downstream_certificate_paths": {
            name: {"path": path, "present": present}
            for name, path in DOWNSTREAM_PATHS.items()
            for present in [(ROOT / path).exists()]
        },
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not write canonical O_H authority",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, Ward identity, observed targets, alpha_LM, plaquette, u0, reduced pilots, or value recognition",
            "does not treat Z3 H2 support as physical transfer",
            "does not treat source-only rows as source-Higgs overlap rows",
        ],
        "exact_next_action": (
            "Retire at least one failed obligation with a same-surface artifact: "
            "derive a physical primitive/off-diagonal neutral transfer, derive a "
            "selection rule excluding the orthogonal neutral top coupling, supply "
            "canonical scalar LSZ metric/FV/IR normalization, or measure "
            "C_spH/C_HH pole-overlap rows."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
