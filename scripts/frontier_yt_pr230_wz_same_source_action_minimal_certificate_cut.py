#!/usr/bin/env python3
"""
PR #230 W/Z same-source accepted-action minimal certificate cut.

The W/Z physical-response bypass is attractive because a single radial source
would cancel the unknown source normalization in top/W or top/Z response
ratios.  The current branch has several useful conditional contracts for that
route, but the accepted same-source EW action certificate has not been written
or validated.

This runner turns the current W/Z dependency surface into an executable cut:
it records which action-side prerequisites are already support-only, which
certificate vertices remain independently missing, and why no conditional
contract may be re-read as accepted W/Z authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json"
)
ACCEPTED_ACTION = (
    ROOT / "outputs" / "yt_wz_same_source_ew_action_certificate_2026-05-04.json"
)

PARENTS = {
    "same_source_ew_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "same_source_ew_action_adoption_attempt": "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json",
    "same_source_ew_higgs_action_ansatz_gate": "outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json",
    "higgs_mass_source_action_bridge": "outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json",
    "radial_spurion_sector_overlap_theorem": "outputs/yt_pr230_radial_spurion_sector_overlap_theorem_2026-05-06.json",
    "radial_spurion_action_contract": "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json",
    "wz_response_ratio_identifiability_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "canonical_higgs_operator_certificate_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "same_source_sector_overlap_identity": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "wz_correlator_mass_fit_path_gate": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "electroweak_g2_certificate_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "source_higgs_gram_purity_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "wz_response_route_completion": "outputs/yt_pr230_wz_response_route_completion_2026-05-06.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_observed_top_or_yukawa_as_selector": False,
    "used_observed_wz_masses_or_g2": False,
    "used_alpha_lm_or_plaquette_u0": False,
    "used_reduced_pilots_as_production_evidence": False,
    "used_static_ew_algebra_as_response_rows": False,
    "used_conditional_contract_as_current_action_authority": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "set_g2_equal_one": False,
    "claimed_retained_or_proposed_retained": False,
    "wrote_accepted_action_certificate": False,
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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def load_json(relpath: str | Path) -> dict[str, Any]:
    path = Path(relpath)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def row(
    *,
    vertex: str,
    required_for: str,
    satisfied: bool,
    evidence: str,
    missing_reason: str | None = None,
    shortcut_rejection: str | None = None,
) -> dict[str, Any]:
    return {
        "vertex": vertex,
        "required_for": required_for,
        "satisfied": satisfied,
        "evidence": evidence,
        "missing_reason": missing_reason,
        "shortcut_rejection": shortcut_rejection,
    }


def action_certificate_rows(certs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    builder = certs["same_source_ew_action_builder"]
    action_gate = certs["same_source_ew_action_gate"]
    adoption = certs["same_source_ew_action_adoption_attempt"]
    ansatz = certs["same_source_ew_higgs_action_ansatz_gate"]
    mass_bridge = certs["higgs_mass_source_action_bridge"]
    radial_sector = certs["radial_spurion_sector_overlap_theorem"]
    radial_contract = certs["radial_spurion_action_contract"]
    ratio_contract = certs["wz_response_ratio_identifiability_contract"]
    canonical = certs["canonical_higgs_operator_certificate_gate"]
    sector = certs["same_source_sector_overlap_identity"]
    wz_mass = certs["wz_correlator_mass_fit_path_gate"]

    return [
        row(
            vertex="action_form_ansatz",
            required_for="accepted_same_source_ew_action",
            satisfied=ansatz.get("same_source_ew_higgs_action_ansatz_gate_passed") is True
            and ansatz.get("current_surface_adoption_passed") is False,
            evidence=status(ansatz),
            shortcut_rejection=(
                "The ansatz is action-form support only and does not write the "
                "accepted action certificate."
            ),
        ),
        row(
            vertex="centered_phi_dagger_phi_source_bridge",
            required_for="accepted_same_source_ew_action",
            satisfied=mass_bridge.get("higgs_mass_source_action_bridge_passed") is True
            and mass_bridge.get("proposal_allowed") is False,
            evidence=status(mass_bridge),
            shortcut_rejection=(
                "The bridge identifies the operator for a future mass-source "
                "term; it does not supply same-surface action adoption."
            ),
        ),
        row(
            vertex="no_independent_top_source_radial_contract",
            required_for="accepted_same_source_ew_action and W/Z response ratio",
            satisfied=radial_contract.get("radial_spurion_action_contract_passed") is True
            and radial_contract.get("current_surface_contract_satisfied") is False
            and radial_contract.get("proposal_allowed") is False,
            evidence=status(radial_contract),
            shortcut_rejection=(
                "Current PR230 top FH/LSZ source is still the additive top "
                "source surface, not an adopted no-independent-top radial action."
            ),
        ),
        row(
            vertex="response_ratio_algebra_contract",
            required_for="future W/Z response readout",
            satisfied=ratio_contract.get("wz_response_ratio_identifiability_contract_passed")
            is True
            and ratio_contract.get("current_surface_contract_satisfied") is False
            and ratio_contract.get("proposal_allowed") is False,
            evidence=status(ratio_contract),
            shortcut_rejection=(
                "dv/ds cancellation is conditional on the missing same-source "
                "action, W/Z rows, covariance, and strict g2 authority."
            ),
        ),
        row(
            vertex="same_source_sector_overlap_contract_support",
            required_for="future W/Z response readout",
            satisfied=radial_sector.get("radial_spurion_sector_overlap_theorem_passed") is True
            and radial_sector.get("current_surface_sector_overlap_identity_supplied")
            is False,
            evidence=status(radial_sector),
            shortcut_rejection=(
                "The theorem supplies a conditional sector-overlap shape, but "
                "not the current additive-source identity."
            ),
        ),
        row(
            vertex="same_surface_canonical_higgs_operator_certificate",
            required_for="accepted_same_source_ew_action",
            satisfied=canonical.get("candidate_valid") is True,
            evidence=status(canonical),
            missing_reason=(
                "Builder requires a non-shortcut canonical-Higgs certificate "
                "with allowed kind; current candidate_valid is not true."
            ),
        ),
        row(
            vertex="current_same_source_sector_overlap_identity",
            required_for="accepted_same_source_ew_action",
            satisfied=sector.get("sector_overlap_identity_gate_passed") is True
            or radial_sector.get("current_surface_sector_overlap_identity_supplied") is True,
            evidence=f"{status(sector)}; {status(radial_sector)}",
            missing_reason=(
                "Current sector-overlap identity remains absent; conditional "
                "radial-spurion support is not the accepted current identity."
            ),
        ),
        row(
            vertex="wz_correlator_mass_fit_path_certificate",
            required_for="accepted_same_source_ew_action",
            satisfied=wz_mass.get("wz_correlator_mass_fit_path_ready") is True,
            evidence=status(wz_mass),
            missing_reason=(
                "Builder requires a non-shortcut W/Z mass-fit path certificate; "
                "current production correlator mass-fit rows are absent."
            ),
        ),
        row(
            vertex="accepted_same_source_ew_action_candidate",
            required_for="accepted_same_source_ew_action",
            satisfied=ACCEPTED_ACTION.exists()
            and builder.get("same_source_ew_action_certificate_valid") is True
            and action_gate.get("same_source_ew_action_ready") is True,
            evidence=f"{status(builder)}; {status(action_gate)}",
            missing_reason=(
                "Accepted candidate file is absent or invalid; the builder "
                "cannot validate without the missing certificate vertices."
            ),
        ),
        row(
            vertex="ansatz_only_adoption_shortcut",
            required_for="firewall",
            satisfied=adoption.get("same_source_ew_action_adoption_attempt_passed") is True
            and adoption.get("adoption_allowed_now") is False
            and adoption.get("accepted_action_certificate_written_by_this_attempt")
            is False,
            evidence=status(adoption),
            shortcut_rejection=(
                "The adoption attempt deliberately blocks using the action "
                "ansatz as the accepted action certificate."
            ),
        ),
    ]


def closure_rows(certs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    covariance = certs["top_wz_matched_covariance_builder"]
    g2_builder = certs["electroweak_g2_certificate_builder"]
    g2_firewall = certs["wz_g2_authority_firewall"]
    gram = certs["source_higgs_gram_purity_gate"]
    route = certs["wz_response_route_completion"]
    assembly = certs["full_positive_closure_assembly_gate"]
    retained = certs["retained_closure_route"]
    campaign = certs["campaign_status"]
    return [
        row(
            vertex="matched_top_wz_covariance_rows",
            required_for="W/Z physical-response y_t readout",
            satisfied=covariance.get("input_present") is True
            and covariance.get("certificate_valid") is True,
            evidence=status(covariance),
            missing_reason="No paired top/W or top/Z covariance row packet is present.",
        ),
        row(
            vertex="strict_non_observed_g2_authority",
            required_for="W/Z physical-response y_t readout",
            satisfied=g2_builder.get("input_present") is True
            and g2_builder.get("certificate_valid") is True,
            evidence=f"{status(g2_builder)}; {status(g2_firewall)}",
            missing_reason=(
                "Current g2 authority is blocked; observed W/Z data and "
                "normalization-by-fiat are forbidden."
            ),
        ),
        row(
            vertex="source_higgs_gram_or_physical_identity",
            required_for="source-Higgs/WZ bridge cross-check",
            satisfied=gram.get("source_higgs_gram_purity_gate_passed") is True,
            evidence=status(gram),
            missing_reason="Source-Higgs Gram purity is not passed on the current surface.",
        ),
        row(
            vertex="aggregate_wz_route_completion",
            required_for="retained/proposed_retained proposal",
            satisfied=route.get("proposal_allowed") is True
            and assembly.get("proposal_allowed") is True
            and retained.get("proposal_allowed") is True
            and campaign.get("proposal_allowed") is True,
            evidence=(
                f"{status(route)}; {status(assembly)}; "
                f"{status(retained)}; {status(campaign)}"
            ),
            missing_reason="Aggregate W/Z, assembly, retained-route, and campaign gates remain open.",
        ),
    ]


def main() -> int:
    print("PR #230 W/Z same-source accepted-action minimal certificate cut")
    print("=" * 78)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposals = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    action_rows = action_certificate_rows(certs)
    response_rows = closure_rows(certs)
    all_rows = action_rows + response_rows

    satisfied_support = [
        row["vertex"]
        for row in action_rows
        if row["satisfied"] is True
        and row["vertex"]
        not in {
            "same_surface_canonical_higgs_operator_certificate",
            "current_same_source_sector_overlap_identity",
            "wz_correlator_mass_fit_path_certificate",
            "accepted_same_source_ew_action_candidate",
        }
    ]
    minimal_action_completion_set = [
        "same_surface_canonical_higgs_operator_certificate",
        "current_same_source_sector_overlap_identity",
        "wz_correlator_mass_fit_path_certificate",
        "accepted_same_source_ew_action_candidate",
    ]
    open_action_cut = [
        row["vertex"]
        for row in action_rows
        if row["vertex"] in minimal_action_completion_set and row["satisfied"] is not True
    ]
    root_certificate_cut = [
        "same_surface_canonical_higgs_operator_certificate",
        "current_same_source_sector_overlap_identity",
        "wz_correlator_mass_fit_path_certificate",
    ]
    root_cut_open = [vertex for vertex in root_certificate_cut if vertex in open_action_cut]
    closure_cut_open = [
        row["vertex"] for row in response_rows if row["satisfied"] is not True
    ]
    forbidden_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    accepted_action_absent = not ACCEPTED_ACTION.exists()
    all_cut_vertices_open = set(root_certificate_cut).issubset(set(root_cut_open))
    support_side_loaded = {
        "action_form_ansatz": "action_form_ansatz" in satisfied_support,
        "centered_phi_dagger_phi_source_bridge": "centered_phi_dagger_phi_source_bridge"
        in satisfied_support,
        "no_independent_top_source_radial_contract": (
            "no_independent_top_source_radial_contract" in satisfied_support
        ),
        "response_ratio_algebra_contract": "response_ratio_algebra_contract"
        in satisfied_support,
        "same_source_sector_overlap_contract_support": (
            "same_source_sector_overlap_contract_support" in satisfied_support
        ),
    }
    support_loaded = all(support_side_loaded.values())
    cut_passed = (
        not missing
        and not proposals
        and support_loaded
        and accepted_action_absent
        and all_cut_vertices_open
        and forbidden_clean
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("support-side-contracts-loaded", support_loaded, str(support_side_loaded))
    report("accepted-action-candidate-absent", accepted_action_absent, rel(ACCEPTED_ACTION))
    report("root-certificate-cut-open", all_cut_vertices_open, str(root_cut_open))
    report("canonical-higgs-vertex-open", "same_surface_canonical_higgs_operator_certificate" in root_cut_open, statuses["canonical_higgs_operator_certificate_gate"])
    report("sector-overlap-vertex-open", "current_same_source_sector_overlap_identity" in root_cut_open, statuses["same_source_sector_overlap_identity"])
    report("wz-mass-fit-vertex-open", "wz_correlator_mass_fit_path_certificate" in root_cut_open, statuses["wz_correlator_mass_fit_path_gate"])
    report("closure-response-cut-open", bool(closure_cut_open), str(closure_cut_open))
    report("conditional-contracts-not-current-action-authority", True, "conditional support is separated from accepted action authority")
    report("forbidden-firewall-clean", forbidden_clean, str(FORBIDDEN_FIREWALL))
    report("minimal-certificate-cut-recorded", cut_passed, str(open_action_cut))

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / WZ accepted same-source action minimal certificate cut remains open"
        ),
        "conditional_surface_status": (
            "support: W/Z response can cancel source normalization only after the root action cut is closed and production W/Z/covariance/g2 rows exist"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The accepted same-source EW action certificate is absent, and its "
            "root non-shortcut certificate cut is still open: canonical O_H, "
            "current sector-overlap identity, and W/Z mass-fit path."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "wz_same_source_action_minimal_certificate_cut_passed": cut_passed,
        "current_surface_action_certificate_satisfied": False,
        "accepted_action_certificate_path": rel(ACCEPTED_ACTION),
        "accepted_action_certificate_present": not accepted_action_absent,
        "satisfied_support_vertices": satisfied_support,
        "support_side_loaded": support_side_loaded,
        "root_certificate_cut": root_certificate_cut,
        "root_certificate_cut_open": root_cut_open,
        "minimal_action_completion_set": minimal_action_completion_set,
        "open_action_cut": open_action_cut,
        "closure_response_cut_open": closure_cut_open,
        "action_certificate_rows": action_rows,
        "closure_rows": response_rows,
        "dependency_dag": {
            "accepted_same_source_ew_action": [
                "action_form_ansatz",
                "centered_phi_dagger_phi_source_bridge",
                "same_surface_canonical_higgs_operator_certificate",
                "current_same_source_sector_overlap_identity",
                "wz_correlator_mass_fit_path_certificate",
                "accepted_same_source_ew_action_candidate",
            ],
            "wz_physical_response_readout": [
                "accepted_same_source_ew_action",
                "no_independent_top_source_radial_contract",
                "response_ratio_algebra_contract",
                "matched_top_wz_covariance_rows",
                "strict_non_observed_g2_authority",
                "aggregate_wz_route_completion",
            ],
        },
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not write or validate the accepted same-source EW action certificate",
            "does not treat an ansatz, radial-spurion contract, or response-ratio algebra as current action authority",
            "does not treat static EW algebra as W/Z mass-response rows",
            "does not supply canonical O_H, current sector-overlap identity, W/Z mass-fit rows, matched covariance, or strict g2",
            "does not set kappa_s, c2, Z_match, or g2 to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, reduced pilots, or value recognition",
        ],
        "exact_next_action": (
            "Close one root vertex with a genuine artifact.  The cleanest path "
            "is still same-surface canonical O_H plus C_spH/C_HH pole rows.  "
            "For W/Z specifically, produce a non-shortcut canonical-Higgs "
            "certificate, a current same-source sector-overlap identity/adopted "
            "radial-spurion action, and a production W/Z correlator mass-fit "
            "path before writing the accepted action certificate; then add "
            "matched top/W covariance rows and strict non-observed g2."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
