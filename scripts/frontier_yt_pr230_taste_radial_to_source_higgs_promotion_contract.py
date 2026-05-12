#!/usr/bin/env python3
"""
PR #230 taste-radial-to-source-Higgs promotion contract.

The two-source row campaign has completed the finite C_sx/C_xx rows for the
exact taste-radial source x.  This runner records the only honest promotion
rule: those rows become C_sH/C_HH source-Higgs rows only after a same-surface
certificate identifies x with canonical O_H, including action, canonical
LSZ/metric normalization, and pole/FV/IR authority.

The current surface does not supply that identity.  This is support
infrastructure for the clean source-Higgs route, not top-Yukawa closure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json"
)

PARENTS = {
    "two_source_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "degree_one_radial_tangent": "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json",
    "row_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "source_higgs_pole_row_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
    "canonical_higgs_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "full_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_observed_top_or_yukawa_as_selector": False,
    "used_alpha_lm_or_plaquette_u0": False,
    "used_reduced_pilot_as_production_evidence": False,
    "treated_c_sx_as_c_sH_without_identity_certificate": False,
    "treated_c_xx_as_c_HH_without_identity_certificate": False,
    "treated_taste_radial_source_as_canonical_O_H": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "claimed_retained_or_proposed_retained": False,
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def count_or_value(value: Any) -> int | None:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, int):
        return value
    return None


def main() -> int:
    print("PR #230 taste-radial-to-source-Higgs promotion contract")
    print("=" * 78)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]

    action_axis_realized = (
        certs["two_source_action"].get("two_source_taste_radial_action_passed") is True
        and certs["two_source_action"].get("operator_id")
        == "pr230_taste_radial_hypercube_flip_source_v1"
        and certs["two_source_action"].get("canonical_higgs_operator_identity_passed")
        is False
    )
    degree_one_support_only = (
        "degree-one radial-tangent O_H uniqueness theorem"
        in statuses["degree_one_radial_tangent"]
        and certs["degree_one_radial_tangent"].get(
            "degree_one_radial_tangent_oh_theorem_passed"
        )
        is True
        and certs["degree_one_radial_tangent"].get("degree_one_tangent_unique") is True
        and certs["degree_one_radial_tangent"].get(
            "same_surface_linear_tangent_premise_derived"
        )
        is False
        and certs["degree_one_radial_tangent"].get("canonical_oh_identity_derived")
        is False
        and certs["degree_one_radial_tangent"].get("source_higgs_pole_rows_present")
        is False
    )
    ready_chunks = count_or_value(certs["row_combiner"].get("ready_chunks"))
    ready_indices = certs["row_combiner"].get("ready_chunk_indices", [])
    expected_chunks = count_or_value(certs["row_combiner"].get("expected_chunks"))
    row_packet_is_complete_taste_radial = (
        ready_chunks is not None
        and expected_chunks == 63
        and ready_chunks == expected_chunks
        and len(ready_indices) == ready_chunks
        and certs["row_combiner"].get("combined_rows_written") is True
        and "C_sx/C_xx" in statuses["row_combiner"]
    )
    strict_pole_contract_open = (
        "strict acceptance contract" in statuses["source_higgs_pole_row_contract"]
        or "strict rows absent" in statuses["source_higgs_pole_row_contract"]
    ) and certs["source_higgs_pole_row_contract"].get("proposal_allowed") is False
    overlap_contract_support_only = (
        "source-Higgs overlap-kappa row contract"
        in statuses["source_higgs_overlap_kappa_contract"]
        and certs["source_higgs_overlap_kappa_contract"].get("proposal_allowed")
        is False
    )
    canonical_identity_absent = (
        certs["canonical_higgs_gate"].get("candidate_present") is False
        and certs["canonical_higgs_gate"].get("candidate_valid") is False
        and "canonical-Higgs operator certificate absent"
        in statuses["canonical_higgs_gate"]
    )
    source_higgs_launch_blocked = (
        certs["source_higgs_readiness"].get("source_higgs_launch_ready") is False
        and "blocked by missing O_H certificate" in statuses["source_higgs_readiness"]
    )
    aggregate_rejects_closure = (
        certs["full_assembly"].get("proposal_allowed") is False
        and "not passed" in statuses["full_assembly"]
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    promotion_rule = {
        "source_label_map_after_identity_certificate": {
            "C_ss": "C_ss",
            "C_sx": "C_sH",
            "C_xx": "C_HH",
        },
        "required_before_map_can_be_used": [
            "same-surface canonical O_H identity/normalization certificate for x",
            "same-surface EW/Higgs action or equivalent canonical-operator theorem",
            "canonical LSZ/metric normalization and limiting order",
            "isolated-pole residue extraction with FV/IR/model-class authority",
            "source-Higgs pole-row acceptance contract passes with no C_sx/C_xx aliasing",
            "O_sp-Higgs Gram purity or measured kappa_spH row",
            "full assembly, retained-route, and campaign proposal gates pass",
        ],
        "kappa_formula_after_promotion": (
            "kappa_spH = Res(C_sx)/sqrt(Res(C_ss) Res(C_xx)) only after x=O_H "
            "is certified; before that the same expression is a taste-radial "
            "diagnostic and not physical kappa_s"
        ),
    }

    contract_passed = (
        not missing
        and not proposal_allowed
        and action_axis_realized
        and degree_one_support_only
        and row_packet_is_complete_taste_radial
        and strict_pole_contract_open
        and overlap_contract_support_only
        and canonical_identity_absent
        and source_higgs_launch_blocked
        and aggregate_rejects_closure
        and firewall_clean
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("two-source-taste-radial-axis-realized", action_axis_realized, statuses["two_source_action"])
    report("degree-one-theorem-support-only", degree_one_support_only, statuses["degree_one_radial_tangent"])
    report(
        "row-packet-is-complete-taste-radial",
        row_packet_is_complete_taste_radial,
        f"ready={ready_chunks}/{expected_chunks}",
    )
    report("source-higgs-pole-contract-open", strict_pole_contract_open, statuses["source_higgs_pole_row_contract"])
    report("overlap-kappa-contract-support-only", overlap_contract_support_only, statuses["source_higgs_overlap_kappa_contract"])
    report("canonical-oh-identity-absent", canonical_identity_absent, statuses["canonical_higgs_gate"])
    report("source-higgs-launch-blocked", source_higgs_launch_blocked, statuses["source_higgs_readiness"])
    report("aggregate-gates-reject-closure", aggregate_rejects_closure, "assembly/retained/campaign deny proposal")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))

    result = {
        "actual_current_surface_status": (
            "exact-support / taste-radial-to-source-Higgs promotion contract; "
            "current promotion blocked by absent canonical O_H identity/action/LSZ premise"
        ),
        "conditional_surface_status": (
            "conditional-support for reusing completed C_sx/C_xx rows as "
            "C_sH/C_HH only after x=canonical O_H is certified with action, "
            "canonical LSZ, isolated-pole residue, FV/IR/model-class, and "
            "Gram-purity authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The branch has the complete finite taste-radial C_sx/C_xx packet "
            "and an exact degree-one axis theorem, but it lacks the identity "
            "x=canonical O_H, source-Higgs pole rows, LSZ/FV/IR authority, and "
            "aggregate proposal gates."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "promotion_contract_passed": contract_passed,
        "current_promotion_allowed": False,
        "current_promotion_blockers": [
            "same_surface_canonical_O_H_identity_absent",
            "same_surface_EW_Higgs_action_or_canonical_operator_theorem_absent",
            "canonical_LSZ_metric_and_limiting_order_absent",
            "source_higgs_C_sH_C_HH_pole_rows_absent",
            "source_higgs_Gram_purity_absent",
            "scalar_LSZ_FV_IR_model_class_authority_absent",
            "aggregate_proposal_gates_reject_closure",
        ],
        "promotion_rule": promotion_rule,
        "row_packet_status": {
            "ready_chunks": ready_chunks,
            "expected_chunks": expected_chunks,
            "combined_rows_written": certs["row_combiner"].get(
                "combined_rows_written"
            ),
            "complete_packet": row_packet_is_complete_taste_radial,
            "row_kind": "taste_radial_C_sx_C_xx",
            "canonical_source_higgs_rows_present": False,
        },
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not relabel C_sx/C_xx as C_sH/C_HH on the current surface",
            "does not identify the taste-radial source x with canonical O_H",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, reduced pilots, or value recognition",
        ],
        "exact_next_action": (
            "The finite taste-radial packet is complete.  For promotion, supply "
            "same-surface x=canonical O_H identity/action/LSZ authority, then "
            "rerun the source-Higgs pole-row acceptance contract, Gram-purity "
            "postprocessor, scalar-LSZ gates, full assembly, retained-route, and "
            "campaign gates."
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
