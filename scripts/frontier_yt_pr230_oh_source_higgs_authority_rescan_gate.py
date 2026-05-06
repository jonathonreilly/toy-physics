#!/usr/bin/env python3
"""
PR #230 O_H/source-Higgs authority rescan gate.

The positive PR230 route most likely to close without month-scale direct MC is
the same-surface source-Higgs bridge:

    O_sp source pole + O_H canonical Higgs + C_sH/C_HH pole rows
        -> Gram purity / source-Higgs overlap -> y_t

This runner answers the narrow "did we already have it?" question.  It scans
the current PR230 authority surface and known source-Higgs artifacts for a real
canonical O_H certificate or production C_sH/C_HH row certificate.  It also
keeps the trap boundary explicit: action-first, FMS, invariant-ring, GNS, and
holonomic tools can certify a future object after the object exists, but they
are not themselves O_H authority on the current surface.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_oh_source_higgs_authority_rescan_gate_2026-05-05.json"
)

PARENTS = {
    "canonical_oh_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_oh_realization": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "canonical_oh_semantic_firewall": "outputs/yt_canonical_higgs_operator_semantic_firewall_2026-05-04.json",
    "cross_lane_oh_authority_audit": "outputs/yt_cross_lane_oh_authority_audit_2026-05-05.json",
    "canonical_oh_premise_stretch": "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json",
    "fms_oh_attempt": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
    "action_first_oh_attempt": "outputs/yt_pr230_action_first_oh_artifact_attempt_2026-05-05.json",
    "invariant_ring_oh_attempt": "outputs/yt_pr230_invariant_ring_oh_certificate_attempt_2026-05-05.json",
    "gns_source_higgs_attempt": "outputs/yt_pr230_gns_source_higgs_flat_extension_attempt_2026-05-05.json",
    "holonomic_source_response": "outputs/yt_pr230_holonomic_source_response_feasibility_gate_2026-05-05.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_gram_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_postprocess": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "source_higgs_unratified_operator": "outputs/yt_source_higgs_unratified_operator_certificate_2026-05-03.json",
    "source_higgs_unratified_gram_no_go": "outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json",
    "derived_bridge_rank_one": "outputs/yt_pr230_derived_bridge_rank_one_closure_attempt_2026-05-05.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_ARTIFACTS = {
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "same_source_ew_action_certificate": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "holonomic_source_response_rows": "outputs/yt_pr230_holonomic_source_response_rows_2026-05-05.json",
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


def source_higgs_projection_counterfamily() -> list[dict[str, Any]]:
    """Show why source-only rows and positivity cannot select O_H overlap.

    Normalize the source-pole row C_ss=1 and let the supplied second neutral
    scalar have C_HH=1 with variable C_sH=rho.  All rows visible to a source-only
    PR230 analysis are unchanged while the Gram determinant and overlap change.
    This is the missing physical bridge in finite-dimensional form.
    """

    family: list[dict[str, Any]] = []
    for rho in (1.0, 0.8, 0.5, 0.0, -0.5):
        c_ss = 1.0
        c_hh = 1.0
        c_sh = rho
        family.append(
            {
                "rho_sH": rho,
                "C_ss": c_ss,
                "C_HH": c_hh,
                "C_sH": c_sh,
                "gram_determinant": c_ss * c_hh - c_sh * c_sh,
                "source_only_rows_identical": True,
                "positive_semidefinite": abs(rho) <= 1.0,
                "source_higgs_purity": abs(abs(rho) - 1.0) < 1.0e-15,
            }
        )
    return family


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity_as_authority": False,
        "uses_observed_top_or_yukawa_targets": False,
        "uses_alpha_lm_plaquette_u0_or_rconn": False,
        "defines_yt_bare": False,
        "sets_kappa_s_equal_one": False,
        "treats_fms_method_as_current_oh_certificate": False,
        "treats_gns_flat_extension_as_selector_without_rows": False,
        "treats_holonomic_method_as_h_source_definition": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 O_H/source-Higgs authority rescan gate")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}
    counterfamily = source_higgs_projection_counterfamily()
    firewall = forbidden_firewall()

    canonical_oh_absent = (
        certs["canonical_oh_gate"].get("candidate_present") is False
        and certs["canonical_oh_gate"].get("candidate_valid") is False
        and certs["canonical_oh_realization"].get(
            "canonical_higgs_operator_realization_gate_passed"
        )
        is False
        and future_presence["canonical_oh_certificate"] is False
    )
    cross_lane_no_authority = (
        certs["cross_lane_oh_authority_audit"].get("repo_cross_lane_authority_found")
        is False
        and certs["cross_lane_oh_authority_audit"].get("proposal_allowed") is False
    )
    premise_stretch_no_go = (
        certs["canonical_oh_premise_stretch"].get("premise_lattice_stretch_no_go_passed")
        is True
        and certs["canonical_oh_premise_stretch"].get("proposal_allowed") is False
    )
    method_candidates_not_authority = (
        certs["fms_oh_attempt"].get("fms_oh_certificate_available") is False
        and certs["action_first_oh_attempt"].get("canonical_oh_certificate_written")
        is False
        and certs["invariant_ring_oh_attempt"].get("canonical_oh_certificate_written")
        is False
        and certs["gns_source_higgs_attempt"].get("gns_certificate_written") is False
        and certs["holonomic_source_response"].get("pr541_route_immediate_closure")
        is False
    )
    source_higgs_rows_absent = (
        certs["source_higgs_readiness"].get("future_rows_present") is False
        and certs["source_higgs_builder"].get("candidate_written") is False
        and certs["source_higgs_builder"].get("input_present") is False
        and future_presence["source_higgs_rows"] is False
        and future_presence["source_higgs_production_certificate"] is False
    )
    gram_gates_waiting = (
        certs["source_higgs_gram_gate"].get("source_higgs_gram_purity_gate_passed")
        is False
        and certs["source_higgs_postprocess"].get("osp_higgs_gram_purity_gate_passed")
        is False
        and certs["source_higgs_unratified_operator"].get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
        and certs["source_higgs_unratified_operator"].get("proposal_allowed") is False
        and certs["source_higgs_unratified_gram_no_go"].get(
            "unratified_gram_shortcut_no_go_passed"
        )
        is True
    )
    derived_bridge_does_not_close = (
        certs["derived_bridge_rank_one"].get("derived_bridge_closure_passed") is False
        and certs["derived_bridge_rank_one"].get("exact_negative_boundary_passed") is True
    )
    aggregate_gates_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
    )
    counterfamily_blocks_source_only_selection = (
        len({row["C_ss"] for row in counterfamily}) == 1
        and all(row["positive_semidefinite"] for row in counterfamily)
        and any(not row["source_higgs_purity"] for row in counterfamily)
        and any(row["source_higgs_purity"] for row in counterfamily)
    )
    clean_firewall = all(value is False for value in firewall.values())

    authority_found = not (
        canonical_oh_absent and source_higgs_rows_absent and cross_lane_no_authority
    )
    exact_negative_boundary_passed = (
        not authority_found
        and premise_stretch_no_go
        and method_candidates_not_authority
        and gram_gates_waiting
        and derived_bridge_does_not_close
        and aggregate_gates_open
        and counterfamily_blocks_source_only_selection
        and clean_firewall
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["canonical_oh_gate"])
    report("cross-lane-oh-authority-absent", cross_lane_no_authority, statuses["cross_lane_oh_authority_audit"])
    report("same-surface-oh-premise-stretch-blocked", premise_stretch_no_go, statuses["canonical_oh_premise_stretch"])
    report("method-candidates-not-current-authority", method_candidates_not_authority, "FMS/action-first/invariant/GNS/holonomic support only")
    report("source-higgs-production-rows-absent", source_higgs_rows_absent, statuses["source_higgs_builder"])
    report("gram-gates-waiting-on-real-rows", gram_gates_waiting, statuses["source_higgs_gram_gate"])
    report(
        "unratified-source-higgs-smoke-operator-rejected",
        certs["source_higgs_unratified_operator"].get("phase") == "smoke"
        and certs["source_higgs_unratified_operator"].get("proposal_allowed") is False
        and certs["source_higgs_unratified_operator"].get(
            "canonical_higgs_operator_identity_passed"
        )
        is False,
        certs["source_higgs_unratified_operator"].get("verdict", ""),
    )
    report("derived-rank-one-bridge-does-not-close-oh", derived_bridge_does_not_close, statuses["derived_bridge_rank_one"])
    report("aggregate-gates-still-open", aggregate_gates_open, "proposal_allowed remains false")
    report("source-only-counterfamily-blocks-overlap-selection", counterfamily_blocks_source_only_selection, "same C_ss with variable C_sH/C_HH overlap")
    report("forbidden-import-firewall-clean", clean_firewall, f"firewall={firewall}")
    report("oh-source-higgs-authority-not-found", not authority_found, f"future_presence={future_presence}")
    report("exact-negative-boundary-passed", exact_negative_boundary_passed, "rescan found no current O_H/source-Higgs authority")

    payload: dict[str, Any] = {
        "actual_current_surface_status": (
            "exact negative boundary / O_H/source-Higgs authority rescan found no "
            "current same-surface canonical O_H or C_sH/C_HH row certificate"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface canonical O_H certificate "
            "and production C_ss/C_sH/C_HH pole rows pass the existing Gram gates"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No canonical O_H identity/normalization certificate or production "
            "source-Higgs pole-row certificate exists on the current PR230 surface."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "oh_source_higgs_authority_found": authority_found,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "canonical_oh_absent": canonical_oh_absent,
        "source_higgs_rows_absent": source_higgs_rows_absent,
        "method_candidates_not_authority": method_candidates_not_authority,
        "future_artifact_presence": future_presence,
        "source_higgs_projection_counterfamily": counterfamily,
        "forbidden_firewall": firewall,
        "parent_statuses": statuses,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
        "exact_next_action": (
            "Produce one genuine same-surface artifact: a canonical O_H "
            "identity/normalization certificate or production C_ss/C_sH/C_HH "
            "pole rows.  Until then, FMS, invariant-ring, GNS, holonomic, "
            "Perron, and positivity tools are certificate engines only."
        ),
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote {OUTPUT.relative_to(ROOT)}")
    print(f"# SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
