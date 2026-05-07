#!/usr/bin/env python3
"""
PR #230 W/Z physical-response packet intake checkpoint.

This runner asks the post-block10 question directly: does the current branch
contain a production W/Z physical-response packet that can reopen the W/Z
bypass route?  It distinguishes strict production roots from scout/schema
artifacts and support contracts, then writes the narrow current boundary.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json"
)

PARENTS = {
    "wz_same_source_action_minimal_cut": "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json",
    "wz_accepted_action_root_checkpoint": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
    "wz_response_ratio_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "wz_smoke_to_production_no_go": "outputs/yt_pr230_wz_smoke_to_production_promotion_no_go_2026-05-05.json",
    "same_source_ew_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_correlator_mass_fit_path_gate": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "same_source_top_response_builder": "outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "electroweak_g2_certificate_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "same_source_wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "same_source_w_response_row_builder": "outputs/yt_same_source_w_response_row_builder_2026-05-04.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

PRODUCTION_ROOTS = {
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "wz_correlator_mass_fit_rows": "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json",
    "same_source_top_response_certificate": "outputs/yt_same_source_top_response_certificate_2026-05-04.json",
    "strict_electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
    "fh_gauge_mass_response_measurement_rows": "outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json",
    "fh_gauge_mass_response_certificate": "outputs/yt_fh_gauge_mass_response_certificate_2026-05-02.json",
    "top_wz_matched_covariance_certificate": "outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json",
    "delta_perp_correction_certificate": "outputs/yt_same_source_w_response_orthogonal_correction_certificate_2026-05-04.json",
    "same_source_w_response_rows": "outputs/yt_same_source_w_response_rows_2026-05-04.json",
}

SCOUT_ARTIFACTS = {
    "wz_mass_fit_response_row_builder_scout": "outputs/yt_wz_mass_fit_response_row_builder_scout_2026-05-04.json",
    "wz_mass_fit_response_row_builder_scout_rows": "outputs/yt_wz_mass_fit_response_row_builder_scout_rows_2026-05-04.json",
    "same_source_w_response_row_builder_scout": "outputs/yt_same_source_w_response_row_builder_scout_2026-05-04.json",
    "same_source_w_response_row_builder_scout_rows": "outputs/yt_same_source_w_response_row_builder_scout_rows_2026-05-04.json",
    "same_source_top_response_builder_scout_certificate": "outputs/yt_same_source_top_response_certificate_builder_scout_certificate_2026-05-04.json",
    "top_wz_matched_covariance_builder_scout_certificate": "outputs/yt_top_wz_matched_covariance_certificate_builder_scout_certificate_2026-05-04.json",
    "wz_harness_smoke_schema": "outputs/yt_pr230_wz_harness_smoke_schema_smoke_2026-05-05.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_top_or_yukawa_as_selector": False,
    "used_observed_wz_masses_or_g2": False,
    "used_alpha_lm_or_plaquette_u0": False,
    "used_static_ew_algebra_as_physical_response_rows": False,
    "used_scout_or_smoke_rows_as_production_evidence": False,
    "used_conditional_contract_as_current_action_authority": False,
    "renamed_C_sx_C_xx_as_C_sH_C_HH": False,
    "identified_taste_radial_x_as_canonical_OH": False,
    "assumed_k_top_equals_k_gauge": False,
    "assumed_top_wz_covariance_or_factorization": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "set_g2_equal_one": False,
    "touched_live_chunk_worker": False,
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


def display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(relpath: str) -> dict[str, Any]:
    path = ROOT / relpath
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def present_map(paths: dict[str, str]) -> dict[str, bool]:
    return {name: (ROOT / relpath).exists() for name, relpath in paths.items()}


def current_mode_open(cert: dict[str, Any], *, mode_key: str = "mode") -> bool:
    return cert.get(mode_key) == "current" and cert.get("proposal_allowed") is False


def production_requirements(
    certs: dict[str, dict[str, Any]], roots: dict[str, bool]
) -> list[dict[str, Any]]:
    action_cut = certs["wz_same_source_action_minimal_cut"]
    root_checkpoint = certs["wz_accepted_action_root_checkpoint"]
    row_builder = certs["wz_mass_fit_response_row_builder"]
    top_builder = certs["same_source_top_response_builder"]
    covariance_builder = certs["top_wz_matched_covariance_builder"]
    g2_builder = certs["electroweak_g2_certificate_builder"]
    g2_firewall = certs["wz_g2_authority_firewall"]
    wz_gate = certs["same_source_wz_response_gate"]
    w_response_rows = certs["same_source_w_response_row_builder"]

    return [
        {
            "root": "accepted_same_source_ew_action",
            "satisfied": roots["accepted_same_source_ew_action"]
            and action_cut.get("current_surface_action_certificate_satisfied") is True,
            "current_evidence": status(action_cut),
            "missing_reason": (
                "The accepted action certificate file is absent and the minimal "
                "certificate cut keeps canonical O_H, sector-overlap, and W/Z "
                "mass-fit roots open."
            ),
        },
        {
            "root": "canonical_higgs_operator_certificate",
            "satisfied": roots["canonical_higgs_operator_certificate"],
            "current_evidence": status(root_checkpoint),
            "missing_reason": (
                "The W/Z action root still depends on a non-shortcut canonical "
                "Higgs certificate; the current root checkpoint finds no closure."
            ),
        },
        {
            "root": "wz_correlator_mass_fit_rows",
            "satisfied": roots["wz_correlator_mass_fit_rows"],
            "current_evidence": status(certs["wz_correlator_mass_fit_path_gate"]),
            "missing_reason": (
                "The W/Z mass-fit path gate remains negative and no production "
                "correlator mass-fit row file exists."
            ),
        },
        {
            "root": "same_source_top_response_certificate",
            "satisfied": roots["same_source_top_response_certificate"]
            and top_builder.get("top_response_certificate_written") is True,
            "current_evidence": status(top_builder),
            "missing_reason": (
                "The current same-source top response builder is open; only "
                "scout certificates exist."
            ),
        },
        {
            "root": "strict_electroweak_g2_certificate",
            "satisfied": roots["strict_electroweak_g2_certificate"]
            and g2_builder.get("strict_certificate_written") is True,
            "current_evidence": f"{status(g2_builder)}; {status(g2_firewall)}",
            "missing_reason": (
                "The strict non-observed g2 certificate is absent; the authority "
                "firewall blocks observed g2 and generator-convention shortcuts."
            ),
        },
        {
            "root": "fh_gauge_mass_response_measurement_rows",
            "satisfied": roots["fh_gauge_mass_response_measurement_rows"]
            and row_builder.get("measurement_rows_written") is True
            and row_builder.get("mode") == "current",
            "current_evidence": status(row_builder),
            "missing_reason": (
                "The current W/Z mass-fit response-row builder records absent "
                "W/Z mass-fit rows, top-response certificate, and g2 certificate; "
                "it writes no strict measurement rows."
            ),
        },
        {
            "root": "fh_gauge_mass_response_certificate",
            "satisfied": roots["fh_gauge_mass_response_certificate"]
            and wz_gate.get("same_source_wz_response_certificate_gate_passed") is True,
            "current_evidence": status(wz_gate),
            "missing_reason": (
                "The same-source W/Z gate is still open because the strict W/Z "
                "mass-response certificate is absent."
            ),
        },
        {
            "root": "top_wz_matched_covariance_certificate",
            "satisfied": roots["top_wz_matched_covariance_certificate"]
            and covariance_builder.get("covariance_certificate_written") is True,
            "current_evidence": status(covariance_builder),
            "missing_reason": (
                "The matched covariance builder is open; current production top/W "
                "or top/Z covariance rows are absent."
            ),
        },
        {
            "root": "delta_perp_correction_certificate",
            "satisfied": roots["delta_perp_correction_certificate"],
            "current_evidence": status(w_response_rows),
            "missing_reason": (
                "The final W-response row builder also lacks the orthogonal "
                "correction certificate; it cannot set delta_perp by fiat."
            ),
        },
        {
            "root": "same_source_w_response_rows",
            "satisfied": roots["same_source_w_response_rows"]
            and w_response_rows.get("row_certificate_written") is True
            and w_response_rows.get("mode") == "current",
            "current_evidence": status(w_response_rows),
            "missing_reason": (
                "The final production W-response row file is absent; only scout "
                "row-builder artifacts exist."
            ),
        },
    ]


def main() -> int:
    print("PR #230 W/Z physical-response packet intake checkpoint")
    print("=" * 78)

    certs = {name: load_json(relpath) for name, relpath in PARENTS.items()}
    parent_statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    roots = present_map(PRODUCTION_ROOTS)
    scouts = present_map(SCOUT_ARTIFACTS)
    requirements = production_requirements(certs, roots)
    missing_requirements = [
        item["root"] for item in requirements if item["satisfied"] is not True
    ]
    all_requirements_satisfied = not missing_requirements

    action_cut_open = (
        certs["wz_same_source_action_minimal_cut"].get(
            "wz_same_source_action_minimal_certificate_cut_passed"
        )
        is True
        and certs["wz_same_source_action_minimal_cut"].get(
            "current_surface_action_certificate_satisfied"
        )
        is False
    )
    action_root_blocked = (
        certs["wz_accepted_action_root_checkpoint"].get("current_route_blocked")
        is True
        and certs["wz_accepted_action_root_checkpoint"].get("root_closures_found")
        == []
    )
    response_ratio_support_only = (
        certs["wz_response_ratio_contract"].get(
            "wz_response_ratio_identifiability_contract_passed"
        )
        is True
        and certs["wz_response_ratio_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
    )
    row_builders_open = (
        current_mode_open(certs["wz_mass_fit_response_row_builder"])
        and certs["wz_mass_fit_response_row_builder"].get("measurement_rows_written")
        is False
        and current_mode_open(certs["same_source_w_response_row_builder"])
        and certs["same_source_w_response_row_builder"].get("row_certificate_written")
        is False
    )
    smoke_no_go_loaded = (
        certs["wz_smoke_to_production_no_go"].get(
            "wz_smoke_to_production_promotion_no_go_passed"
        )
        is True
    )
    scouts_are_non_production = (
        all(scouts.values())
        and smoke_no_go_loaded
        and certs["wz_mass_fit_response_row_builder"].get("measurement_rows_written")
        is False
        and certs["same_source_w_response_row_builder"].get("row_certificate_written")
        is False
    )
    aggregate_denies = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    forbidden_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("accepted-action-cut-open", action_cut_open, parent_statuses["wz_same_source_action_minimal_cut"])
    report("accepted-action-root-blocked", action_root_blocked, parent_statuses["wz_accepted_action_root_checkpoint"])
    report("response-ratio-support-only", response_ratio_support_only, parent_statuses["wz_response_ratio_contract"])
    report("strict-row-builders-open", row_builders_open, "W/Z and final W-response builders write no current production rows")
    report("scouts-present-but-non-production", scouts_are_non_production, str(scouts))
    report("no-production-root-file-complete", not all_requirements_satisfied, str(roots))
    report("aggregate-gates-deny-proposal", aggregate_denies, "assembly/retained/campaign proposal_allowed=false")
    report("forbidden-firewall-clean", forbidden_clean, str(FORBIDDEN_FIREWALL))

    passed = FAIL_COUNT == 0
    result = {
        "metadata": {
            "artifact": "yt_pr230_wz_physical_response_packet_intake_checkpoint",
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
        "actual_current_surface_status": (
            "exact negative boundary / WZ physical-response packet not present "
            "on current PR230 surface; only scout/schema and support-contract "
            "artifacts exist"
        ),
        "claim_type": "open_gate",
        "conditional_surface_status": (
            "exact support if future same-surface artifacts supply an accepted "
            "EW/Higgs action, canonical O_H/sector-overlap authority, production "
            "W/Z correlator mass-fit rows, same-source top-response rows, matched "
            "top/W or top/Z covariance, strict non-observed g2, and the final "
            "W-response row packet without scout/smoke promotion"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current branch lacks every strict production root needed for "
            "the W/Z physical-response packet.  Existing W/Z artifacts are "
            "action/ratio contracts, negative gates, or scout/schema rows; "
            "none validates an accepted action, production W/Z mass-response "
            "rows, matched covariance, strict g2, or final W-response rows."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "wz_physical_response_packet_intake_checkpoint_passed": passed,
        "current_route_blocked": True,
        "production_packet_present": all_requirements_satisfied,
        "production_roots_present": roots,
        "scout_artifacts_present": scouts,
        "production_requirements": requirements,
        "missing_production_roots": missing_requirements,
        "support_only_surfaces_loaded": [
            "wz_response_ratio_identifiability_contract",
            "wz_same_source_action_minimal_certificate_cut",
            "wz_accepted_action_response_root_checkpoint",
            "wz_smoke_to_production_promotion_no_go",
            "wz_mass_fit_response_row_builder_current_open_gate",
            "same_source_w_response_row_builder_current_open_gate",
        ],
        "blocked_root_vertices": [
            "accepted same-source EW/Higgs action",
            "canonical O_H / same-source sector-overlap identity",
            "production W/Z correlator mass-fit rows",
            "same-source top-response rows",
            "matched top/W or top/Z covariance",
            "strict non-observed g2",
            "delta_perp correction or accepted neutral rank-one/Gram authority",
            "final same-source W-response production rows",
        ],
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim physical W/Z response closure",
            "does not promote scout, smoke, or synthetic rows to production evidence",
            "does not use static EW mass algebra as dM_W/ds or dM_Z/ds",
            "does not assume k_top = k_gauge or top/W covariance",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed targets, observed g2, alpha_LM, plaquette, or u0",
            "does not set kappa_s, c2, Z_match, g2, or delta_perp to one or zero by convention",
            "does not identify taste-radial x with canonical O_H or relabel C_sx/C_xx as C_sH/C_HH",
            "does not touch or relaunch the live chunk worker",
        ],
        "campaign_pivot": {
            "wz_route_status": "blocked_on_current_surface_at_physical_response_packet_intake",
            "next_queue_item": "canonical O_H / source-Higgs production bridge",
            "next_exact_action": (
                "Pivot back to the canonical O_H/source-Higgs bridge only if a "
                "fresh same-surface O_H certificate or production C_ss/C_sH/C_HH "
                "pole-row packet appears; otherwise keep the W/Z row packet as "
                "a future production task requiring the missing strict roots."
            ),
        },
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
