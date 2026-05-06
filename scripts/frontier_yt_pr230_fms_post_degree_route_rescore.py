#!/usr/bin/env python3
"""
PR #230 FMS post-degree route rescore.

The degree-one premise gate closed the shortcut "degree-one taste radial source
therefore canonical O_H".  This runner records the productive follow-up from
the literature and existing PR230 gates: the clean source-Higgs route should be
action-first and gauge-invariant-composite/FMS-style, not a degree-label
shortcut.  Literature is route guidance only; it is not proof authority for the
current PR230 surface.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_fms_post_degree_route_rescore_2026-05-06.json"

PARENTS = {
    "fresh_literature_review": "outputs/yt_pr230_fresh_artifact_literature_route_review_2026-05-05.json",
    "degree_one_gate": "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json",
    "action_first_completion": "outputs/yt_pr230_action_first_route_completion_2026-05-06.json",
    "action_first_oh_attempt": "outputs/yt_pr230_action_first_oh_artifact_attempt_2026-05-05.json",
    "fms_oh_attempt": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
    "canonical_oh_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_gram_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "full_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_ARTIFACTS = {
    "same_source_ew_higgs_action": "outputs/yt_pr230_same_source_ew_higgs_action_certificate_2026-05-06.json",
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "gram_purity_certificate": "outputs/yt_source_higgs_gram_purity_certificate_2026-05-03.json",
}

LITERATURE_ROWS = [
    {
        "id": "weak_and_higgs_from_lattice_2026",
        "url": "https://arxiv.org/abs/2603.12882",
        "role": "Recent lattice review/context: manifest gauge-invariant weak/Higgs lattice formulation is connected to perturbative language through FMS.",
        "pr230_boundary": "Does not supply a PR230 same-source EW/Higgs action, canonical O_H certificate, or source-Higgs rows.",
    },
    {
        "id": "fms_bound_state_spectrum_2020",
        "url": "https://arxiv.org/abs/1912.08680",
        "role": "FMS relates gauge-invariant bound-state operators to elementary BEH variables after the gauge-Higgs theory/action is supplied.",
        "pr230_boundary": "Does not identify the current PR230 taste-radial source with canonical O_H.",
    },
    {
        "id": "observable_spectrum_beh_2019",
        "url": "https://arxiv.org/abs/1709.07477",
        "role": "Physical spectra in BEH gauge theories are built from gauge-invariant states; FMS can map them to elementary W/Z/Higgs states in suitable theories.",
        "pr230_boundary": "Does not replace same-surface operator identity, normalization, or pole-row production.",
    },
    {
        "id": "su3_fundamental_higgs_lattice_2018",
        "url": "https://arxiv.org/abs/1804.04453",
        "role": "Lattice gauge-Higgs examples show the gauge-invariant spectrum can differ from elementary perturbative spectra outside SM-like conditions.",
        "pr230_boundary": "Does not allow importing elementary-Higgs labels without the same-surface FMS/action checks.",
    },
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_literature_as_proof_authority": False,
        "used_degree_or_odd_parity_as_oh_authority": False,
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_targets_as_selectors": False,
        "used_alpha_lm_or_plaquette_or_u0": False,
        "used_reduced_pilots_as_production_evidence": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_kappa_s_equal_one": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 FMS post-degree route rescore")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}

    literature_primary_support = (
        len(LITERATURE_ROWS) == 4
        and all(row["url"].startswith("https://arxiv.org/abs/") for row in LITERATURE_ROWS)
        and all("Does not" in row["pr230_boundary"] for row in LITERATURE_ROWS)
    )
    fresh_review_selects_fms = (
        certs["fresh_literature_review"].get("selected_genuine_artifact_contract", {}).get("contract")
        == "O_H/C_sH/C_HH source-Higgs pole rows"
        and certs["fresh_literature_review"].get("proposal_allowed") is False
        and certs["fresh_literature_review"].get("genuine_artifact_found_on_current_surface") is False
    )
    degree_shortcut_closed = (
        certs["degree_one_gate"].get("degree_one_higgs_action_premise_gate_passed") is True
        and certs["degree_one_gate"].get("degree_one_filter_selects_e1") is True
        and certs["degree_one_gate"].get("degree_one_premise_authorized_on_current_surface") is False
        and certs["degree_one_gate"].get("proposal_allowed") is False
    )
    action_first_still_cleanest_not_current = (
        "action-first O_H/C_sH/C_HH route not complete" in statuses["action_first_completion"]
        and certs["action_first_completion"].get("proposal_allowed") is False
        and "FMS O_H certificate construction blocked" in statuses["fms_oh_attempt"]
        and certs["fms_oh_attempt"].get("proposal_allowed") is False
    )
    current_action_and_oh_absent = (
        "same-source EW action not defined" in statuses["same_source_ew_action_gate"]
        and certs["canonical_oh_gate"].get("candidate_present") is False
        and certs["canonical_oh_gate"].get("candidate_valid") is False
        and certs["source_higgs_readiness"].get("source_higgs_launch_ready") is False
    )
    source_higgs_rows_absent = (
        all(present is False for present in future_presence.values())
        and certs["source_higgs_gram_gate"].get("source_higgs_gram_purity_gate_passed") is False
    )
    assembly_still_open = (
        certs["full_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    recommended_contract = {
        "route_id": "fms_action_first_composite_oh_rows_after_degree_gate",
        "cleanest_next_artifact": "same-surface EW/Higgs action plus gauge-invariant composite O_H certificate",
        "why_after_degree_gate": "FMS/lattice literature points to gauge-invariant composite operators as the physical Higgs route; the degree-one source filter is only a target selector.",
        "minimum_future_artifacts": [
            FUTURE_ARTIFACTS["same_source_ew_higgs_action"],
            FUTURE_ARTIFACTS["canonical_oh_certificate"],
            FUTURE_ARTIFACTS["source_higgs_rows"],
            FUTURE_ARTIFACTS["gram_purity_certificate"],
        ],
        "forbidden_shortcut_retired": "degree, odd parity, Z3 invariance, or FMS method names as canonical O_H authority",
    }
    contract_complete = (
        recommended_contract["route_id"].startswith("fms_action_first")
        and len(recommended_contract["minimum_future_artifacts"]) == 4
        and "degree" in recommended_contract["forbidden_shortcut_retired"]
    )
    firewall_clean = all(value is False for value in forbidden_firewall().values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("literature-primary-support-not-proof", literature_primary_support, f"rows={len(LITERATURE_ROWS)}")
    report("fresh-review-selects-fms-contract", fresh_review_selects_fms, statuses["fresh_literature_review"])
    report("degree-shortcut-closed", degree_shortcut_closed, statuses["degree_one_gate"])
    report("action-first-still-cleanest-not-current", action_first_still_cleanest_not_current, statuses["action_first_completion"])
    report("current-action-and-oh-absent", current_action_and_oh_absent, statuses["same_source_ew_action_gate"])
    report("source-higgs-rows-absent", source_higgs_rows_absent, str(future_presence))
    report("assembly-retained-campaign-still-open", assembly_still_open, "proposal_allowed=false")
    report("recommended-contract-complete", contract_complete, recommended_contract["route_id"])
    report("forbidden-firewall-clean", firewall_clean, str(forbidden_firewall()))

    result = {
        "actual_current_surface_status": "bounded-support / FMS post-degree route rescore; action-first composite O_H route selected as cleanest future artifact, no current closure",
        "conditional_surface_status": "conditional-support if a future same-surface EW/Higgs action, gauge-invariant composite O_H certificate, source-Higgs pole rows, and Gram-purity certificate are supplied",
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "FMS literature supports the action-first gauge-invariant composite-O_H route "
            "as the cleanest way forward after the degree-one shortcut fails, but the "
            "current PR230 surface still lacks the same-source EW/Higgs action, canonical "
            "O_H identity/normalization, source-Higgs rows, and Gram-purity certificate."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "fms_post_degree_route_rescore_passed": FAIL_COUNT == 0,
        "literature_rows": LITERATURE_ROWS,
        "recommended_contract": recommended_contract,
        "future_artifact_presence": future_presence,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not use literature or FMS as proof authority",
            "does not identify the degree-one taste-radial source with canonical O_H",
            "does not write or imply source-Higgs production rows",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "forbidden_firewall": forbidden_firewall(),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
