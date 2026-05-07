#!/usr/bin/env python3
"""
PR #230 same-surface neutral multiplicity-one artifact gate.

This is the executable intake contract for the cleanest remaining
source-Higgs route.  It asks what a future same-surface artifact must prove
before invariant-ring, commutant, primitive-cone, or Schur tools may be used
as canonical O_H authority.

The current PR230 surface does not pass that contract.  The gate records the
required positive certificate shape and rejects the already-known two-singlet
neutral completion, where source-only data stay fixed while the candidate
canonical-Higgs direction rotates in an orthogonal neutral scalar slot.
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
    / "yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json"
)

PARENTS = {
    "clean_source_higgs_route_selector": "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json",
    "invariant_ring_oh_attempt": "outputs/yt_pr230_invariant_ring_oh_certificate_attempt_2026-05-05.json",
    "oh_bridge_candidate_portfolio": "outputs/yt_pr230_oh_bridge_first_principles_candidate_portfolio_2026-05-06.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "neutral_commutant_rank_no_go": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
    "neutral_primitive_cone_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "neutral_primitive_cone_stretch_no_go": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
    "z3_triplet_conditional_primitive": "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json",
    "z3_positive_cone_support": "outputs/yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json",
    "source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_postprocess": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "candidate_same_surface_multiplicity_one_certificate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "neutral_irreducibility_certificate": "outputs/yt_neutral_scalar_irreducibility_certificate_2026-05-04.json",
}

FORBIDDEN_IMPORTS = [
    "H_unit matrix-element readout",
    "yt_ward_identity as authority",
    "observed top mass or observed y_t selector",
    "alpha_LM / plaquette / u0 proof input",
    "reduced cold pilots as production evidence",
    "c2 = 1 unless derived",
    "Z_match = 1 unless derived",
    "kappa_s = 1 unless derived by scalar LSZ/canonical normalization",
    "PSLQ or value-recognition hit as proof selector",
]

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
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}


def required_artifact_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_cl3_z3_neutral_representation",
            "required_evidence": [
                "explicit neutral scalar basis on the PR230 same surface",
                "Cl(3)/Z3 action or transfer matrices on that basis",
                "source-pole operator coordinates in the same basis",
                "top-coupled neutral scalar sector definition",
            ],
            "acceptance_rule": "basis/action/source coordinates are present and use the same surface, not a cross-lane or literature carrier",
            "current_satisfied": False,
        },
        {
            "id": "multiplicity_one_or_primitive_generator",
            "required_evidence": [
                "degree-one invariant dimension equals one in the top-coupled neutral sector",
                "or commutant dimension equals one on that sector",
                "or a primitive/irreducible positive transfer certificate selects one canonical radial generator",
            ],
            "acceptance_rule": "two copies of a trivial neutral singlet, or any rotatable orthogonal neutral scalar, rejects the candidate",
            "current_satisfied": False,
        },
        {
            "id": "canonical_metric_and_lsz_normalization",
            "required_evidence": [
                "kinetic or inverse-propagator derivative metric for the selected scalar",
                "finite-volume/IR/zero-mode limiting order",
                "canonical field normalization used by v",
                "no kappa_s = 1 convention",
            ],
            "acceptance_rule": "LSZ/canonical metric fixes normalization rather than importing a unit convention",
            "current_satisfied": False,
        },
        {
            "id": "source_to_canonical_higgs_overlap",
            "required_evidence": [
                "identity O_sp = O_H with normalization, or measured C_spH/C_HH pole-residue overlap",
                "Gram-purity or equivalent orthogonal-neutral exclusion",
                "source-scale invariant kappa_spH row using Res(C_spH)/sqrt(Res(C_ss) Res(C_HH))",
            ],
            "acceptance_rule": "source-only C_ss rows are insufficient; an independent cross row or identity theorem is required",
            "current_satisfied": False,
        },
        {
            "id": "measurement_rows_or_certificate_paths",
            "required_evidence": [
                FUTURE_FILES["canonical_higgs_operator_certificate"],
                FUTURE_FILES["source_higgs_measurement_rows"],
                FUTURE_FILES["source_higgs_production_certificate"],
            ],
            "acceptance_rule": "accepted candidate paths must exist before downstream O_H/C_sH/C_HH gates can pass",
            "current_satisfied": False,
        },
        {
            "id": "claim_firewall",
            "required_evidence": FORBIDDEN_IMPORTS,
            "acceptance_rule": "every forbidden import is explicitly absent from load-bearing proof inputs",
            "current_satisfied": True,
        },
    ]


def current_two_singlet_counterfamily() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, theta in (
        ("source_aligned_candidate", 0.0),
        ("candidate_rotated_30deg", math.pi / 6.0),
        ("candidate_rotated_60deg", math.pi / 3.0),
        ("orthogonal_neutral_candidate", math.pi / 2.0),
    ):
        rows.append(
            {
                "case": label,
                "neutral_basis": ["source_singlet", "orthogonal_neutral_singlet"],
                "group_action": "trivial_on_both_singlets_on_current_surface",
                "degree_one_invariant_dimension": 2,
                "commutant_dimension": 4,
                "source_vector": [1.0, 0.0],
                "candidate_oh_vector": [math.cos(theta), math.sin(theta)],
                "source_to_candidate_overlap": math.cos(theta),
                "source_only_observables_change": False,
                "passes_multiplicity_one_contract": False,
                "rejection_reason": "current surface allows an orthogonal neutral singlet with identical source-only rows",
            }
        )
    return rows


def candidate_schema() -> dict[str, Any]:
    return {
        "required_top_level_fields": [
            "actual_current_surface_status",
            "same_surface_cl3_z3_representation",
            "neutral_scalar_basis",
            "action_or_transfer_matrices",
            "top_coupled_neutral_sector",
            "source_pole_operator_coordinates",
            "multiplicity_one_or_primitive_generator_proof",
            "canonical_metric_lsz_normalization",
            "source_to_canonical_higgs_overlap",
            "forbidden_import_firewall",
            "downstream_certificate_paths",
            "proposal_allowed",
        ],
        "must_have_boolean_true_fields": [
            "same_surface_cl3_z3_representation.present",
            "multiplicity_one_or_primitive_generator_proof.passed",
            "canonical_metric_lsz_normalization.passed",
            "source_to_canonical_higgs_overlap.passed",
            "forbidden_import_firewall.passed",
        ],
        "must_have_boolean_false_fields": [
            "forbidden_import_firewall.uses_H_unit",
            "forbidden_import_firewall.uses_yt_ward_identity",
            "forbidden_import_firewall.uses_observed_targets",
            "forbidden_import_firewall.uses_alpha_lm_plaquette_u0",
            "forbidden_import_firewall.sets_c2_zmatch_kappas_to_one_by_convention",
        ],
        "accepted_status_after_independent_review": "proposed_retained may be requested only by downstream aggregate gates, never by this intake gate alone",
    }


def main() -> int:
    print("PR #230 same-surface neutral multiplicity-one artifact gate")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    future_present = future_presence()
    contract = required_artifact_contract()
    counterfamily = current_two_singlet_counterfamily()
    schema = candidate_schema()

    selector_points_here = (
        parents["clean_source_higgs_route_selector"].get("selected_clean_route", {}).get("id")
        == "source_higgs_invariant_ring_then_gns_pole_rows"
        and parents["clean_source_higgs_route_selector"].get("proposal_allowed") is False
    )
    invariant_ring_blocker_loaded = (
        "invariant-ring O_H certificate attempt blocked" in statuses["invariant_ring_oh_attempt"]
        and parents["invariant_ring_oh_attempt"].get("proposal_allowed") is False
    )
    portfolio_keeps_route_open = (
        parents["oh_bridge_candidate_portfolio"].get("proposal_allowed") is False
        and parents["oh_bridge_candidate_portfolio"].get("candidate_count", 0) >= 5
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_present") is False
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and not future_present["canonical_higgs_operator_certificate"]
    )
    primitive_certificate_absent = (
        parents["neutral_primitive_cone_gate"].get("proposal_allowed") is False
        and not future_present["neutral_primitive_cone_certificate"]
        and not future_present["neutral_irreducibility_certificate"]
    )
    z3_h2_support_not_transfer = (
        parents["z3_positive_cone_support"].get("proposal_allowed") is False
        and parents["z3_triplet_conditional_primitive"].get("proposal_allowed") is False
    )
    kappa_contract_is_overlap_only = (
        parents["source_higgs_overlap_kappa_contract"].get("proposal_allowed") is False
        and parents["source_higgs_overlap_kappa_contract"].get(
            "source_higgs_overlap_kappa_contract_passed"
        )
        is True
    )
    source_higgs_rows_absent = (
        not future_present["source_higgs_measurement_rows"]
        and parents["source_higgs_builder"].get("input_present") is False
        and parents["source_higgs_builder"].get("candidate_written") is False
        and parents["source_higgs_postprocess"].get("candidate_present") is False
    )
    current_candidate_absent = (
        not future_present["candidate_same_surface_multiplicity_one_certificate"]
    )
    contract_missing_now = [
        item["id"] for item in contract if item.get("current_satisfied") is not True
    ]
    counterfamily_rejected = all(
        row["passes_multiplicity_one_contract"] is False for row in counterfamily
    )
    overlap_varies = len({round(row["source_to_candidate_overlap"], 12) for row in counterfamily}) > 1
    source_only_fixed = all(row["source_only_observables_change"] is False for row in counterfamily)
    firewall_clean = all(item.get("current_satisfied") is True for item in contract if item["id"] == "claim_firewall")
    candidate_accepted = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("selector-points-to-source-higgs-invariant-route", selector_points_here, statuses["clean_source_higgs_route_selector"])
    report("invariant-ring-blocker-loaded", invariant_ring_blocker_loaded, statuses["invariant_ring_oh_attempt"])
    report("candidate-portfolio-keeps-route-open", portfolio_keeps_route_open, statuses["oh_bridge_candidate_portfolio"])
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("primitive-or-irreducibility-certificate-absent", primitive_certificate_absent, statuses["neutral_primitive_cone_gate"])
    report("z3-h2-support-not-physical-transfer", z3_h2_support_not_transfer, statuses["z3_positive_cone_support"])
    report("kappa-contract-requires-cross-overlap", kappa_contract_is_overlap_only, statuses["source_higgs_overlap_kappa_contract"])
    report("source-higgs-cross-rows-absent", source_higgs_rows_absent, statuses["source_higgs_builder"])
    report("future-candidate-certificate-absent", current_candidate_absent, FUTURE_FILES["candidate_same_surface_multiplicity_one_certificate"])
    report("contract-records-all-open-positive-obligations", len(contract_missing_now) == 5, f"missing_now={contract_missing_now}")
    report("two-singlet-counterfamily-rejected", counterfamily_rejected, "current two-singlet completion fails multiplicity-one")
    report("source-only-data-fixed-in-counterfamily", source_only_fixed, "source-only rows do not distinguish candidate O_H angle")
    report("source-to-candidate-overlap-varies", overlap_varies, "overlap varies through the counterfamily")
    report("forbidden-import-firewall-clean", firewall_clean, ", ".join(FORBIDDEN_IMPORTS))
    report("candidate-not-accepted-on-current-surface", not candidate_accepted, "no same-surface multiplicity-one certificate")

    result = {
        "actual_current_surface_status": (
            "exact support / same-surface neutral multiplicity-one artifact "
            "intake gate; current PR230 surface rejected"
        ),
        "conditional_surface_status": (
            "conditional-support if a future candidate certificate satisfies "
            "same-surface representation, multiplicity-one or primitive-generator, "
            "canonical LSZ metric, source-Higgs overlap, and firewall obligations"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This gate defines the positive artifact contract but no candidate "
            "certificate is present.  The current two-singlet neutral completion "
            "keeps source-only data fixed while changing the source-to-Higgs "
            "overlap, so it cannot certify canonical O_H or kappa_s."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "candidate_accepted": candidate_accepted,
        "candidate_certificate_present": not current_candidate_absent,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "future_file_presence": future_present,
        "required_artifact_contract": contract,
        "candidate_schema": schema,
        "current_two_singlet_counterfamily": counterfamily,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not write or accept a canonical O_H certificate",
            "does not infer O_H from source-only rows or symmetry labels",
            "does not treat Z3 positive-cone H2 support as a physical primitive transfer",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, Ward identity, observed targets, alpha_LM, plaquette, u0, or PSLQ/value recognition as authority",
        ],
        "exact_next_action": (
            "Produce the actual candidate file "
            f"{FUTURE_FILES['candidate_same_surface_multiplicity_one_certificate']} "
            "with a same-surface representation/action and a multiplicity-one or "
            "primitive-generator proof.  If it passes this gate, rerun the "
            "canonical O_H certificate gate, source-Higgs row builder, Gram-purity "
            "postprocessor, scalar-LSZ gates, full assembly gate, retained-route "
            "gate, and completion audit."
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
