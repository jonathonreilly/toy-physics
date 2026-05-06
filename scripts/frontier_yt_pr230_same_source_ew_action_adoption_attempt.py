#!/usr/bin/env python3
"""
PR #230 same-source EW action adoption attempt.

This runner asks a narrow question after the EW/Higgs action ansatz gate:
can that ansatz be promoted into the accepted same-source EW action
certificate path on the actual PR230 surface?

The answer is intentionally checked against the existing certificate builder
schema.  The ansatz supplies the action-form side of the contract, but the
accepted action certificate still requires independent canonical-Higgs,
sector-overlap, and W/Z mass-fit path certificates.  This runner does not write
the accepted certificate path and does not authorize closure wording.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json"
)
ACCEPTED_ACTION_CERT = (
    ROOT / "outputs" / "yt_wz_same_source_ew_action_certificate_2026-05-04.json"
)

PARENTS = {
    "same_source_ew_higgs_action_ansatz_gate": "outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json",
    "wz_same_source_ew_action_certificate_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "canonical_higgs_operator_certificate_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "same_source_sector_overlap_identity": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "wz_correlator_mass_fit_path_gate": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "higgs_mass_source_action_bridge": "outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json",
    "post_fms_source_overlap_necessity_gate": "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json",
    "source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
}

FORBIDDEN_FALSE_FIELDS = {
    "used_hunit_matrix_element_readout": False,
    "used_hunit_as_operator": False,
    "used_yt_ward_identity": False,
    "used_observed_masses_or_couplings_as_selectors": False,
    "used_static_ew_algebra_as_measurement": False,
    "used_alpha_lm_or_plaquette_u0": False,
    "set_kappa_s_equal_one": False,
    "set_cos_theta_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "wrote_accepted_action_certificate": False,
    "claimed_closure": False,
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


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def adoption_prerequisites(certs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    ansatz = certs["same_source_ew_higgs_action_ansatz_gate"]
    builder = certs["wz_same_source_ew_action_certificate_builder"]
    gate = certs["wz_same_source_ew_action_gate"]
    canonical = certs["canonical_higgs_operator_certificate_gate"]
    sector = certs["same_source_sector_overlap_identity"]
    wz_mass = certs["wz_correlator_mass_fit_path_gate"]
    mass_bridge = certs["higgs_mass_source_action_bridge"]

    return [
        {
            "id": "action_form_from_ansatz",
            "satisfied": ansatz.get("same_source_ew_higgs_action_ansatz_gate_passed")
            is True
            and ansatz.get("current_surface_adoption_passed") is False,
            "evidence": status(ansatz),
        },
        {
            "id": "centered_phi_dagger_phi_source_bridge",
            "satisfied": mass_bridge.get("higgs_mass_source_action_bridge_passed")
            is True
            and mass_bridge.get("proposal_allowed") is False,
            "evidence": status(mass_bridge),
        },
        {
            "id": "canonical_higgs_operator_certificate",
            "satisfied": canonical.get("candidate_valid") is True,
            "evidence": status(canonical),
        },
        {
            "id": "same_source_sector_overlap_identity",
            "satisfied": sector.get("sector_overlap_identity_gate_passed") is True,
            "evidence": status(sector),
        },
        {
            "id": "wz_correlator_mass_fit_path_certificate",
            "satisfied": wz_mass.get("wz_correlator_mass_fit_path_ready") is True,
            "evidence": status(wz_mass),
        },
        {
            "id": "accepted_action_certificate_input",
            "satisfied": builder.get("input_present") is True
            and builder.get("same_source_ew_action_certificate_valid") is True,
            "evidence": status(builder),
        },
        {
            "id": "current_action_gate_ready",
            "satisfied": gate.get("same_source_ew_action_ready") is True,
            "evidence": status(gate),
        },
    ]


def main() -> int:
    print("PR #230 same-source EW action adoption attempt")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    parent_statuses = {name: status(cert) for name, cert in certs.items()}
    proposal_allowed = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    prerequisites = adoption_prerequisites(certs)
    missing_prereqs = [
        row["id"]
        for row in prerequisites
        if row["id"] not in {"action_form_from_ansatz", "centered_phi_dagger_phi_source_bridge"}
        and row["satisfied"] is not True
    ]
    ansatz_side_satisfied = all(
        row["satisfied"] is True
        for row in prerequisites
        if row["id"] in {"action_form_from_ansatz", "centered_phi_dagger_phi_source_bridge"}
    )
    schema_side_satisfied = not missing_prereqs
    accepted_path_present = ACCEPTED_ACTION_CERT.exists()
    accepted_path_written_by_this_attempt = False
    forbidden_clean = all(value is False for value in FORBIDDEN_FALSE_FIELDS.values())
    adoption_allowed_now = (
        not missing
        and not proposal_allowed
        and ansatz_side_satisfied
        and schema_side_satisfied
        and accepted_path_present
    )
    ansatz_only_shortcut_blocked = (
        not missing
        and not proposal_allowed
        and ansatz_side_satisfied
        and not schema_side_satisfied
        and not accepted_path_present
        and forbidden_clean
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("ansatz-action-form-side-satisfied", ansatz_side_satisfied, str([row for row in prerequisites if row["id"] in {"action_form_from_ansatz", "centered_phi_dagger_phi_source_bridge"}]))
    report("accepted-builder-schema-side-not-satisfied", not schema_side_satisfied, f"missing={missing_prereqs}")
    report("accepted-action-certificate-path-absent", not accepted_path_present, display(ACCEPTED_ACTION_CERT))
    report("accepted-action-certificate-not-written", not accepted_path_written_by_this_attempt, "runner is read-only for accepted future path")
    report("ansatz-only-adoption-shortcut-blocked", ansatz_only_shortcut_blocked, "ansatz lacks canonical-Higgs/sector-overlap/WZ mass-fit certificates")
    report("adoption-not-allowed-now", not adoption_allowed_now, f"adoption_allowed_now={adoption_allowed_now}")
    report("forbidden-firewall-clean", forbidden_clean, str(FORBIDDEN_FALSE_FIELDS))

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / ansatz-only same-source EW action adoption shortcut blocked"
        ),
        "conditional_surface_status": (
            "support if canonical-Higgs, sector-overlap, and W/Z mass-fit path certificates are supplied and the accepted action certificate validates"
        ),
        "hypothetical_axiom_status": "hypothetical action adoption remains unavailable on the actual current surface",
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The ansatz supplies the action-form side only.  The accepted "
            "same-source EW action certificate still lacks canonical-Higgs, "
            "sector-overlap, W/Z mass-fit path, and valid certificate inputs."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "same_source_ew_action_adoption_attempt_passed": ansatz_only_shortcut_blocked,
        "ansatz_side_satisfied": ansatz_side_satisfied,
        "schema_side_satisfied": schema_side_satisfied,
        "adoption_allowed_now": adoption_allowed_now,
        "accepted_action_certificate_path": display(ACCEPTED_ACTION_CERT),
        "accepted_action_certificate_present": accepted_path_present,
        "accepted_action_certificate_written_by_this_attempt": accepted_path_written_by_this_attempt,
        "missing_schema_prerequisites": missing_prereqs,
        "prerequisite_rows": prerequisites,
        "parent_statuses": parent_statuses,
        "forbidden_firewall": FORBIDDEN_FALSE_FIELDS,
        "strict_non_claims": [
            "does not write the accepted same-source EW action certificate path",
            "does not promote the ansatz to current action authority",
            "does not supply canonical O_H, sector-overlap, W/Z rows, or source-Higgs pole rows",
            "does not set kappa_s, c2, Z_match, or cos(theta) to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Attack the first missing schema prerequisite directly: a real "
            "canonical-Higgs operator certificate, a same-source sector-overlap "
            "identity theorem, or a W/Z correlator mass-fit path certificate.  "
            "Only after those exist should the accepted same-source EW action "
            "certificate path be written."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
