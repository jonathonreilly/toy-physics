#!/usr/bin/env python3
"""
PR #230 FMS O_H candidate/action packet.

This runner turns the block16 open-surface route into an explicit, auditable
candidate packet.  It is deliberately not a current-surface closure proof:
the PR230 branch still lacks an adopted same-surface EW/Higgs action, a
canonical O_H certificate, and production C_ss/C_sH/C_HH pole rows.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json"

PARENTS = {
    "open_surface_bridge_intake": "outputs/yt_pr230_open_surface_bridge_intake_2026-05-07.json",
    "fms_composite_oh_conditional_theorem": "outputs/yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json",
    "action_first_route_completion": "outputs/yt_pr230_action_first_route_completion_2026-05-06.json",
    "source_higgs_time_kernel_manifest": "outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json",
    "source_higgs_pole_row_acceptance_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "post_fms_source_overlap_necessity_gate": "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "accepted_same_surface_ew_higgs_action": "outputs/yt_pr230_same_surface_ew_higgs_action_certificate_2026-05-07.json",
    "canonical_oh_certificate": "outputs/yt_pr230_canonical_oh_certificate_2026-05-07.json",
    "source_higgs_pole_rows": "outputs/yt_pr230_source_higgs_pole_rows_2026-05-06.json",
    "source_higgs_time_kernel_combined_rows": "outputs/yt_pr230_source_higgs_time_kernel_combined_rows_2026-05-07.json",
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


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_hunit_as_operator": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yt": False,
        "used_observed_wz_or_g2": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "used_reduced_cold_pilots_as_production": False,
        "used_fms_literature_as_proof_authority": False,
        "used_taste_radial_axis_as_canonical_oh": False,
        "aliased_c_sx_to_c_sh": False,
        "set_kappa_s_equal_one": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "claimed_retained_or_proposed_retained": False,
        "launched_or_touched_live_rows": False,
    }


def candidate_packet(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": "pr230_fms_gauge_higgs_oh_candidate_action_packet_v1",
        "claim_class": "candidate_action_contract_only",
        "current_surface_classification": {
            "same_surface_cl3_z3_derived": False,
            "accepted_current_surface": False,
            "external_extension_required": True,
            "external_extension_kind": "gauge-Higgs/FMS candidate action surface",
            "reason": (
                "The packet specifies the operator/action needed for the FMS route, "
                "but PR230 has not derived or adopted that action from the Cl(3)/Z^3 "
                "substrate."
            ),
        },
        "action_surface_contract": {
            "required_fields": [
                "dynamic Higgs doublet Phi with gauge-covariant lattice kinetic term",
                "Higgs radial potential or equivalent substrate derivation producing nonzero v",
                "canonical radial field h with LSZ/kinetic normalization",
                "same-source scalar perturbation coupled to O_H, not to O_top_additive + O_H",
                "gauge action and update/ensemble semantics on the same PR230 configurations",
            ],
            "required_source_derivative": "dS/ds = sum_x O_H(x) after additive-top subtraction or a no-independent-top source theorem",
            "normalizations_not_assumed": ["kappa_s", "c2", "Z_match", "g2"],
        },
        "operator_contract": {
            "operator_id": "O_H_fms_composite_candidate",
            "definition": "O_H(x) = Phi(x)^dagger Phi(x) - <Phi^dagger Phi>",
            "gauge_invariance_condition": "Phi transforms in the accepted EW/Higgs representation and Phi^dagger Phi is a gauge singlet",
            "fms_local_expansion": "O_H = v h + h^2/2 + pi^a pi^a/2 after choosing radial variables on an accepted BEH surface",
            "one_particle_residue_shape": "Res C_HH = v^2 Z_h; source overlap still requires Res C_sH or a source-coordinate theorem",
        },
        "time_kernel_binding": {
            "manifest": str(
                (ROOT / PARENTS["source_higgs_time_kernel_manifest"]).relative_to(ROOT)
            ),
            "schema_version": manifest.get("time_kernel_schema_version"),
            "chunk_count": manifest.get("chunk_count"),
            "launch_authorized_now": False,
            "operator_certificate_is_canonical_oh_now": False,
            "required_rows": ["C_ss(t)", "C_sH(t)", "C_HH(t)"],
            "required_analysis": [
                "same-ensemble covariance",
                "GEVP or isolated-pole residue extraction",
                "FV/IR and zero-mode limiting order",
                "Gram-flatness or equivalent source-overlap theorem",
                "strict scalar-LSZ/model-class authority before physical y_t readout",
            ],
        },
        "acceptance_contract": {
            "must_pass": [
                "accepted same-surface EW/Higgs action or native Cl(3)/Z^3 derivation",
                "canonical O_H identity and normalization certificate",
                "production C_ss/C_sH/C_HH time-kernel rows",
                "pole-residue and covariance certificate",
                "Gram-flatness or non-overlap-exclusion theorem",
                "aggregate retained-route and completion-audit gates",
            ],
            "must_not_use": [
                "H_unit matrix-element readout",
                "yt_ward_identity",
                "observed top/y_t or W/Z/g2 selectors",
                "alpha_LM, plaquette, u0",
                "kappa_s=1, c2=1, Z_match=1, or g2=1 by convention",
            ],
        },
    }


def main() -> int:
    print("PR #230 FMS O_H candidate/action packet")
    print("=" * 72)

    certs = {name: load_json(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}
    firewall = forbidden_firewall()
    packet = candidate_packet(certs["source_higgs_time_kernel_manifest"])

    open_surface_selects_fms = (
        certs["open_surface_bridge_intake"].get("proposal_allowed") is False
        and certs["open_surface_bridge_intake"]
        .get("recommended_next_non_chunk_route", {})
        .get("route_id")
        == "fms_gauge_invariant_higgs_operator_rows"
    )
    fms_theorem_available_but_conditional = (
        "FMS composite O_H theorem"
        in statuses["fms_composite_oh_conditional_theorem"]
        and certs["fms_composite_oh_conditional_theorem"].get(
            "fms_composite_oh_conditional_theorem_passed"
        )
        is True
        and certs["fms_composite_oh_conditional_theorem"].get(
            "current_closure_authority_present"
        )
        is False
    )
    action_first_current_route_blocked = (
        "action-first O_H/C_sH/C_HH route not complete"
        in statuses["action_first_route_completion"]
        and certs["action_first_route_completion"].get(
            "action_first_route_completion_passed"
        )
        is True
        and certs["action_first_route_completion"].get("proposal_allowed") is False
    )
    manifest_wired_but_not_launchable = (
        "source-Higgs time-kernel production manifest"
        in statuses["source_higgs_time_kernel_manifest"]
        and certs["source_higgs_time_kernel_manifest"].get("proposal_allowed")
        is False
        and certs["source_higgs_time_kernel_manifest"].get(
            "closure_launch_authorized_now"
        )
        is False
        and certs["source_higgs_time_kernel_manifest"].get(
            "operator_certificate_is_canonical_oh"
        )
        is False
        and certs["source_higgs_time_kernel_manifest"].get(
            "time_kernel_schema_version"
        )
        == "source_higgs_time_kernel_v1"
        and certs["source_higgs_time_kernel_manifest"].get("chunk_count") == 63
    )
    pole_row_contract_required_and_absent = (
        "source-Higgs C_ss/C_sH/C_HH pole-row acceptance contract"
        in statuses["source_higgs_pole_row_acceptance_contract"]
        and certs["source_higgs_pole_row_acceptance_contract"].get(
            "source_higgs_pole_row_acceptance_contract_passed"
        )
        is True
        and certs["source_higgs_pole_row_acceptance_contract"].get("rows_present")
        is False
        and certs["source_higgs_pole_row_acceptance_contract"].get(
            "closure_contract_satisfied"
        )
        is False
    )
    post_fms_overlap_still_required = (
        "post-FMS source-overlap not derivable"
        in statuses["post_fms_source_overlap_necessity_gate"]
        and certs["post_fms_source_overlap_necessity_gate"].get(
            "post_fms_source_overlap_necessity_gate_passed"
        )
        is True
        and certs["post_fms_source_overlap_necessity_gate"].get(
            "current_source_overlap_authority_present"
        )
        is False
    )
    canonical_oh_absent = (
        certs["canonical_higgs_operator_gate"].get("candidate_present") is False
        and certs["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and future_presence["canonical_oh_certificate"] is False
    )
    same_source_action_absent = (
        certs["same_source_ew_action_gate"].get("same_source_ew_action_ready")
        is False
        and certs["same_source_ew_action_gate"].get("future_action_certificate_present")
        is False
        and future_presence["accepted_same_surface_ew_higgs_action"] is False
    )
    packet_explicit = (
        packet["operator_contract"]["definition"].startswith("O_H")
        and "C_sH(t)" in packet["time_kernel_binding"]["required_rows"]
        and "dynamic Higgs doublet Phi with gauge-covariant lattice kinetic term"
        in packet["action_surface_contract"]["required_fields"]
        and "accepted same-surface EW/Higgs action or native Cl(3)/Z^3 derivation"
        in packet["acceptance_contract"]["must_pass"]
    )
    packet_not_current_surface = (
        packet["current_surface_classification"]["same_surface_cl3_z3_derived"]
        is False
        and packet["current_surface_classification"]["accepted_current_surface"]
        is False
        and packet["current_surface_classification"]["external_extension_required"]
        is True
    )
    aggregate_firewalls_hold = (
        certs["campaign_status"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in firewall.values())

    report("parents-present", not missing, f"missing={missing}")
    report("open-surface-selects-fms-route", open_surface_selects_fms, statuses["open_surface_bridge_intake"])
    report("fms-theorem-available-but-conditional", fms_theorem_available_but_conditional, statuses["fms_composite_oh_conditional_theorem"])
    report("action-first-current-route-blocked", action_first_current_route_blocked, statuses["action_first_route_completion"])
    report("time-kernel-manifest-wired-not-launchable", manifest_wired_but_not_launchable, statuses["source_higgs_time_kernel_manifest"])
    report("pole-row-contract-required-rows-absent", pole_row_contract_required_and_absent, statuses["source_higgs_pole_row_acceptance_contract"])
    report("post-fms-overlap-still-required", post_fms_overlap_still_required, statuses["post_fms_source_overlap_necessity_gate"])
    report("canonical-oh-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("same-source-ew-action-absent", same_source_action_absent, statuses["same_source_ew_action_gate"])
    report("candidate-packet-explicit", packet_explicit, packet["packet_id"])
    report("packet-marked-not-current-surface", packet_not_current_surface, str(packet["current_surface_classification"]))
    report("aggregate-firewalls-hold", aggregate_firewalls_hold, "campaign/retained proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(firewall))

    packet_passed = FAIL_COUNT == 0
    result = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "actual_current_surface_status": (
            "conditional-support / FMS O_H candidate/action packet; current "
            "PR230 surface has no adopted same-surface EW/Higgs action, "
            "canonical O_H certificate, or C_ss/C_sH/C_HH pole rows"
        ),
        "conditional_surface_status": (
            "exact-support only after the packet is converted into an accepted "
            "same-surface Cl(3)/Z^3 EW/Higgs action or explicitly admitted "
            "extension, a canonical O_H certificate, production C_ss/C_sH/C_HH "
            "time-kernel rows, pole/Gram/FV/IR authority, and aggregate route gates"
        ),
        "hypothetical_axiom_status": (
            "external gauge-Higgs extension candidate if the action is adopted "
            "rather than derived from Cl(3)/Z^3"
        ),
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This packet makes the FMS O_H route concrete but does not adopt or "
            "derive the EW/Higgs action on the current PR230 surface, does not "
            "supply canonical O_H authority, and does not supply C_ss/C_sH/C_HH "
            "pole rows or Gram flatness."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "fms_oh_candidate_action_packet_passed": packet_passed,
        "candidate_packet_written": True,
        "accepted_current_surface": False,
        "same_surface_cl3_z3_derived": False,
        "external_extension_required": True,
        "time_kernel_manifest_wired": manifest_wired_but_not_launchable,
        "strict_rows_required": pole_row_contract_required_and_absent,
        "closure_authorized": False,
        "launch_authorized_now": False,
        "packet": packet,
        "future_file_presence": future_presence,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "forbidden_firewall": firewall,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
