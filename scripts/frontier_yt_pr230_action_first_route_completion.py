#!/usr/bin/env python3
"""
PR #230 action-first O_H/C_sH/C_HH route completion gate.

After closing the source-coordinate transport shortcut on the current surface,
this runner works the next candidate lane to conclusion: can the current PR230
surface complete the action-first route by supplying a same-source EW/Higgs
action, a canonical O_H identity/normalization certificate, and production
C_ss/C_sH/C_HH rows?

The result is a current-surface negative boundary.  It does not reject the
future FMS/action-first route; it records the exact missing artifacts that
would reopen it.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_action_first_route_completion_2026-05-06.json"

PARENTS = {
    "source_coordinate_transport_completion": "outputs/yt_pr230_source_coordinate_transport_completion_attempt_2026-05-06.json",
    "action_first_oh_artifact_attempt": "outputs/yt_pr230_action_first_oh_artifact_attempt_2026-05-05.json",
    "fms_oh_certificate_construction_attempt": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
    "same_source_ew_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "radial_spurion_action_contract": "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json",
    "canonical_oh_premise_stretch": "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_gram_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "source_higgs_unratified_gram_no_go": "outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json",
    "candidate_portfolio": "outputs/yt_pr230_oh_bridge_first_principles_candidate_portfolio_2026-05-06.json",
}

TEXTS = {
    "minimal_axioms": "docs/MINIMAL_AXIOMS_2026-04-11.md",
    "ew_gauge_mass": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
    "sm_one_higgs": "docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md",
    "production_harness": "scripts/yt_direct_lattice_correlator_production.py",
    "fms_note": "docs/YT_FMS_OH_CERTIFICATE_CONSTRUCTION_ATTEMPT_NOTE_2026-05-04.md",
    "action_first_note": "docs/YT_PR230_ACTION_FIRST_OH_ARTIFACT_ATTEMPT_NOTE_2026-05-05.md",
}

FUTURE_ARTIFACTS = {
    "same_source_ew_action_certificate": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_gram_purity_certificate": "outputs/yt_source_higgs_gram_purity_certificate_2026-05-03.json",
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


def load_rel(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def read_rel(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_targets": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "defined_oh_by_notation": False,
        "treated_static_ew_algebra_as_action": False,
        "treated_unratified_source_higgs_rows_as_evidence": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 action-first O_H/C_sH/C_HH route completion gate")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    texts = {name: read_rel(rel) for name, rel in TEXTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    missing_texts = [name for name, text in texts.items() if not text]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    futures = future_presence()

    source_transport_closed = (
        parents["source_coordinate_transport_completion"].get(
            "source_coordinate_transport_completion_passed"
        )
        is True
        and parents["source_coordinate_transport_completion"].get("proposal_allowed") is False
    )
    action_attempt_closed = (
        "action-first O_H artifact not constructible"
        in statuses["action_first_oh_artifact_attempt"]
        and parents["action_first_oh_artifact_attempt"].get("exact_negative_boundary_passed") is True
    )
    fms_attempt_closed = (
        "FMS O_H certificate construction blocked"
        in statuses["fms_oh_certificate_construction_attempt"]
        and parents["fms_oh_certificate_construction_attempt"].get("proposal_allowed") is False
    )
    same_source_action_absent = (
        "same-source EW action certificate absent" in statuses["same_source_ew_action_builder"]
        and parents["same_source_ew_action_builder"].get(
            "same_source_ew_action_certificate_valid"
        )
        is False
        and "same-source EW action not defined" in statuses["same_source_ew_action_gate"]
        and parents["same_source_ew_action_gate"].get("same_source_ew_action_ready")
        is False
        and not futures["same_source_ew_action_certificate"]
    )
    radial_spurion_action_contract_support_only = (
        "no-independent-top-source radial-spurion action contract"
        in statuses["radial_spurion_action_contract"]
        and parents["radial_spurion_action_contract"].get(
            "radial_spurion_action_contract_passed"
        )
        is True
        and parents["radial_spurion_action_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and parents["radial_spurion_action_contract"].get(
            "accepted_action_certificate_written"
        )
        is False
        and parents["radial_spurion_action_contract"].get("proposal_allowed") is False
    )
    canonical_oh_absent = (
        "canonical-Higgs operator certificate absent" in statuses["canonical_higgs_operator_gate"]
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and "same-surface O_H identity and normalization"
        in statuses["canonical_oh_premise_stretch"]
        and parents["canonical_oh_premise_stretch"].get(
            "premise_lattice_stretch_no_go_passed"
        )
        is True
        and not futures["canonical_oh_certificate"]
    )
    source_higgs_rows_absent = (
        "source-Higgs production launch blocked" in statuses["source_higgs_readiness"]
        and parents["source_higgs_readiness"].get("proposal_allowed") is False
        and "source-Higgs cross-correlator rows absent" in statuses["source_higgs_builder"]
        and parents["source_higgs_builder"].get("proposal_allowed") is False
        and not futures["source_higgs_measurement_rows"]
    )
    gram_purity_absent = (
        "source-Higgs Gram purity gate not passed" in statuses["source_higgs_gram_gate"]
        and parents["source_higgs_gram_gate"].get("source_higgs_gram_purity_gate_passed")
        is False
        and "Gram-purity postprocess awaiting production" in statuses["source_higgs_postprocessor"]
        and parents["source_higgs_postprocessor"].get(
            "source_higgs_gram_purity_gate_passed"
        )
        is False
        and not futures["source_higgs_gram_purity_certificate"]
    )
    unratified_gram_shortcut_closed = (
        parents["source_higgs_unratified_gram_no_go"].get(
            "unratified_gram_shortcut_no_go_passed"
        )
        is True
        and parents["source_higgs_unratified_gram_no_go"].get("proposal_allowed") is False
    )
    structural_notes_not_action = (
        "staggered-Dirac partition" in texts["minimal_axioms"]
        and "Assume a neutral Higgs vacuum" in texts["ew_gauge_mass"]
        and "does not select the numerical entries" in texts["sm_one_higgs"]
        and "smoke_schema_enabled_not_ew_production" in texts["production_harness"]
    )
    fms_note_records_missing_action = (
        "no same-surface EW gauge-Higgs production action" in texts["fms_note"]
        and "no production `C_sH/C_HH` pole-residue rows" in texts["fms_note"]
    )
    action_note_records_hypothetical_boundary = (
        "Writing down the standard EW/Higgs action is only a hypothetical new surface"
        in texts["action_first_note"]
    )
    clean_firewall = all(value is False for value in forbidden_firewall().values())

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("source-coordinate-transport-current-surface-closed", source_transport_closed, statuses["source_coordinate_transport_completion"])
    report("action-first-artifact-attempt-closed", action_attempt_closed, statuses["action_first_oh_artifact_attempt"])
    report("fms-oh-certificate-attempt-closed", fms_attempt_closed, statuses["fms_oh_certificate_construction_attempt"])
    report("same-source-ew-action-absent", same_source_action_absent, statuses["same_source_ew_action_gate"])
    report("radial-spurion-action-contract-support-only", radial_spurion_action_contract_support_only, statuses["radial_spurion_action_contract"])
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("source-higgs-production-rows-absent", source_higgs_rows_absent, statuses["source_higgs_builder"])
    report("source-higgs-gram-purity-absent", gram_purity_absent, statuses["source_higgs_gram_gate"])
    report("unratified-gram-shortcut-closed", unratified_gram_shortcut_closed, statuses["source_higgs_unratified_gram_no_go"])
    report("structural-notes-not-current-ew-action", structural_notes_not_action, "minimal axioms/EW notes/harness checked")
    report("fms-note-records-missing-load-bearing-artifacts", fms_note_records_missing_action, TEXTS["fms_note"])
    report("action-note-records-hypothetical-action-boundary", action_note_records_hypothetical_boundary, TEXTS["action_first_note"])
    report("forbidden-firewall-clean", clean_firewall, str(forbidden_firewall()))

    exact_negative_boundary_passed = (
        not missing_parents
        and not missing_texts
        and not proposal_allowed
        and source_transport_closed
        and action_attempt_closed
        and fms_attempt_closed
        and same_source_action_absent
        and radial_spurion_action_contract_support_only
        and canonical_oh_absent
        and source_higgs_rows_absent
        and gram_purity_absent
        and unratified_gram_shortcut_closed
        and structural_notes_not_action
        and fms_note_records_missing_action
        and action_note_records_hypothetical_boundary
        and clean_firewall
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / action-first O_H/C_sH/C_HH route not complete on current PR230 surface"
        ),
        "conditional_surface_status": (
            "The action-first FMS route remains a valid future route after a "
            "same-source EW/Higgs action certificate, canonical O_H "
            "identity/normalization certificate, and production C_ss/C_sH/C_HH "
            "rows with Gram-purity/isolated-pole authority are supplied."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Current PR230 artifacts supply structural EW context and a guarded "
            "source-Higgs row shell, but not the same-source action, canonical "
            "O_H, source-Higgs rows, or Gram-purity certificate needed for a "
            "physical y_t readout."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "action_first_route_completion_passed": exact_negative_boundary_passed,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "future_artifact_presence": futures,
        "blocked_requirements": {
            "same_source_ew_action_certificate": not same_source_action_absent,
            "radial_spurion_action_contract_currently_unadopted": radial_spurion_action_contract_support_only,
            "canonical_oh_certificate": not canonical_oh_absent,
            "source_higgs_rows": not source_higgs_rows_absent,
            "source_higgs_gram_purity_certificate": not gram_purity_absent,
        },
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define O_H by notation, H_unit, or static EW algebra",
            "does not treat source-Higgs smoke/guard rows as production evidence",
            "does not use yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Treat action-first O_H/C_sH/C_HH as closed on the current surface. "
            "Proceed to the next candidate lane: W/Z same-source response with "
            "strict g2 and covariance, Schur A/B/C rows, or neutral "
            "primitive/rank-one theorem."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
