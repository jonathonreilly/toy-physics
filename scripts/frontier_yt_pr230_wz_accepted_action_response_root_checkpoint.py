#!/usr/bin/env python3
"""
PR #230 W/Z accepted-action response root checkpoint.

The W/Z physical-response route is only useful after an accepted same-source
EW/Higgs action exists.  This runner attacks the action-root level named by
the loop handoff: current same-source sector-overlap/adopted radial action, or
a production W/Z correlator mass-fit path.  It records the narrow current
boundary without claiming W/Z response closure.
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
    / "yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json"
)

PARENTS = {
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_oh_hard_residual_equivalence_gate": "outputs/yt_pr230_canonical_oh_hard_residual_equivalence_gate_2026-05-07.json",
    "same_source_sector_overlap_identity": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "radial_spurion_sector_overlap_theorem": "outputs/yt_pr230_radial_spurion_sector_overlap_theorem_2026-05-06.json",
    "radial_spurion_action_contract": "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json",
    "additive_source_radial_spurion_incompatibility": "outputs/yt_pr230_additive_source_radial_spurion_incompatibility_2026-05-07.json",
    "additive_top_subtraction_row_contract": "outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json",
    "source_higgs_direct_pole_row_contract": "outputs/yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json",
    "same_source_ew_higgs_action_ansatz_gate": "outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json",
    "same_source_ew_action_adoption_attempt": "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json",
    "same_source_ew_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_same_source_action_minimal_cut": "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json",
    "wz_correlator_mass_fit_path_gate": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_response_ratio_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "top_wz_covariance_import_audit": "outputs/yt_top_wz_covariance_theorem_import_audit_2026-05-05.json",
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "wz_correlator_mass_fit_rows": "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json",
    "wz_response_ratio_rows": "outputs/yt_pr230_wz_response_ratio_rows_2026-05-07.json",
    "additive_top_subtraction_rows": "outputs/yt_pr230_additive_top_subtraction_rows_2026-05-07.json",
    "same_source_top_response_certificate": "outputs/yt_same_source_top_response_certificate_2026-05-04.json",
    "top_wz_matched_covariance_certificate": "outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json",
    "strict_electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_observed_top_or_yukawa_as_selector": False,
    "used_observed_wz_masses_or_g2": False,
    "used_alpha_lm_or_plaquette_u0": False,
    "used_reduced_pilots_as_production_evidence": False,
    "used_static_ew_algebra_as_action_or_response_authority": False,
    "renamed_C_sx_C_xx_as_C_sH_C_HH": False,
    "identified_taste_radial_x_as_canonical_OH": False,
    "treated_conditional_radial_contract_as_current_action_authority": False,
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


def load(relpath: str) -> dict[str, Any]:
    path = ROOT / relpath
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / relpath).exists() for name, relpath in FUTURE_FILES.items()}


def frame(
    name: str,
    *,
    attack_target: str,
    support_loaded: bool,
    closes_action_root: bool,
    evidence: list[str],
    obstruction: str,
    next_admissible_artifact: str,
) -> dict[str, Any]:
    return {
        "name": name,
        "attack_target": attack_target,
        "support_loaded": support_loaded,
        "closes_wz_accepted_action_root": closes_action_root,
        "evidence": evidence,
        "obstruction": obstruction,
        "next_admissible_artifact": next_admissible_artifact,
    }


def root_frames(certs: dict[str, dict[str, Any]], futures: dict[str, bool]) -> list[dict[str, Any]]:
    canonical = certs["canonical_higgs_operator_gate"]
    hard_residual = certs["canonical_oh_hard_residual_equivalence_gate"]
    sector = certs["same_source_sector_overlap_identity"]
    radial = certs["radial_spurion_sector_overlap_theorem"]
    radial_contract = certs["radial_spurion_action_contract"]
    additive_incompat = certs["additive_source_radial_spurion_incompatibility"]
    additive_subtraction = certs["additive_top_subtraction_row_contract"]
    source_higgs_direct = certs["source_higgs_direct_pole_row_contract"]
    ansatz = certs["same_source_ew_higgs_action_ansatz_gate"]
    adoption = certs["same_source_ew_action_adoption_attempt"]
    builder = certs["same_source_ew_action_builder"]
    action_gate = certs["same_source_ew_action_gate"]
    cut = certs["wz_same_source_action_minimal_cut"]
    mass_fit = certs["wz_correlator_mass_fit_path_gate"]
    ratio = certs["wz_response_ratio_contract"]
    covariance = certs["top_wz_covariance_import_audit"]
    g2 = certs["wz_g2_authority_firewall"]

    return [
        frame(
            "same_source_sector_overlap_identity",
            attack_target="derive or directly measure k_top = k_gauge on the current source surface",
            support_loaded=(
                radial.get("radial_spurion_sector_overlap_theorem_passed") is True
                and radial.get("sector_overlap_identity_conditionally_supplied") is True
                and sector.get("sector_overlap_identity_gate_passed") is False
            ),
            closes_action_root=(
                sector.get("sector_overlap_identity_gate_passed") is True
                or radial.get("current_surface_sector_overlap_identity_supplied") is True
            ),
            evidence=[status(sector), status(radial)],
            obstruction=(
                "The radial-spurion theorem supplies only a conditional clean-action "
                "identity.  The current PR230 top FH/LSZ source remains an additive "
                "top mass shift, so k_top = k_gauge is not derived or measured."
            ),
            next_admissible_artifact=(
                "a same-surface sector-overlap theorem/row packet proving or "
                "measuring k_top = k_gauge without additive-top contamination"
            ),
        ),
        frame(
            "adopted_no_independent_top_radial_action",
            attack_target="promote the same-source EW/Higgs ansatz plus radial contract to accepted action",
            support_loaded=(
                ansatz.get("same_source_ew_higgs_action_ansatz_gate_passed") is True
                and radial_contract.get("radial_spurion_action_contract_passed") is True
                and additive_incompat.get("additive_source_radial_spurion_incompatibility_passed") is True
                and adoption.get("same_source_ew_action_adoption_attempt_passed") is True
            ),
            closes_action_root=(
                futures["accepted_same_source_ew_action"]
                and builder.get("same_source_ew_action_certificate_valid") is True
                and action_gate.get("same_source_ew_action_ready") is True
                and radial_contract.get("current_surface_contract_satisfied") is True
            ),
            evidence=[
                status(ansatz),
                status(radial_contract),
                status(additive_incompat),
                status(additive_subtraction),
                status(adoption),
                status(builder),
                status(action_gate),
            ],
            obstruction=(
                "The ansatz and radial contract are support only.  The accepted "
                "action certificate path is absent and the current radial contract "
                "is not satisfied on the additive-source surface; the additive "
                "source incompatibility block shows dS/ds contains O_top_additive + O_H. "
                "The additive-top subtraction contract is a future row contract, not "
                "current subtraction-row evidence."
            ),
            next_admissible_artifact=(
                "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json "
                "validated by the builder with canonical-Higgs, sector-overlap, "
                "and W/Z mass-fit references"
            ),
        ),
        frame(
            "production_wz_correlator_mass_fit_path",
            attack_target="supply production W/Z two-point correlator mass fits under source shifts",
            support_loaded=mass_fit.get("positive_witness_validation", {}).get("valid") is True
            or mass_fit.get("wz_correlator_mass_fit_path_ready") is False,
            closes_action_root=(
                mass_fit.get("wz_correlator_mass_fit_path_ready") is True
                and futures["wz_correlator_mass_fit_rows"]
            ),
            evidence=[status(mass_fit)],
            obstruction=(
                "The mass-fit gate validates a future schema and rejects the "
                "current QCD/top harness.  The production W/Z correlator mass-fit "
                "rows and response rows are absent."
            ),
            next_admissible_artifact=(
                "production W/Z mass-fit row packet with per-source-shift "
                "correlators, plateaus, fit windows, errors, and same-source "
                "coordinate certificate"
            ),
        ),
        frame(
            "response_ratio_packet_after_action",
            attack_target="convert action support into a physical top/W or top/Z response readout",
            support_loaded=ratio.get("wz_response_ratio_identifiability_contract_passed") is True,
            closes_action_root=(
                ratio.get("current_surface_contract_satisfied") is True
                and futures["wz_response_ratio_rows"]
                and futures["additive_top_subtraction_rows"]
                and futures["same_source_top_response_certificate"]
                and futures["top_wz_matched_covariance_certificate"]
                and futures["strict_electroweak_g2_certificate"]
            ),
            evidence=[status(ratio), status(additive_subtraction), status(covariance), status(g2)],
            obstruction=(
                "The algebra cancels dv/ds only after the accepted action and "
                "production row packet exist.  The additive-top subtraction contract "
                "shows what rows would repair the mixed source, but those rows are "
                "absent.  Same-source top rows, matched top/W covariance, and strict "
                "non-observed g2 remain absent."
            ),
            next_admissible_artifact=(
                "matched top/W or top/Z response packet on the accepted action, "
                "with covariance and strict non-observed g2 authority"
            ),
        ),
        frame(
            "canonical_oh_shared_action_root",
            attack_target="satisfy the canonical Higgs identity required by the action builder",
            support_loaded=(
                cut.get("wz_same_source_action_minimal_certificate_cut_passed") is True
                and hard_residual.get("canonical_oh_hard_residual_equivalence_gate_passed") is True
                and source_higgs_direct.get("source_higgs_direct_pole_row_contract_passed") is True
            ),
            closes_action_root=(
                canonical.get("candidate_valid") is True
                and futures["canonical_higgs_operator_certificate"]
            ),
            evidence=[status(canonical), status(hard_residual), status(source_higgs_direct), status(cut)],
            obstruction=(
                "The W/Z action builder still requires a non-shortcut canonical "
                "Higgs operator certificate.  The hard-residual equivalence gate "
                "shows the current O_sp/O_H bridge is not closed by positivity, "
                "primitive-cone, source-Higgs rows, or W/Z physical-response rows.  "
                "The direct source-Higgs pole-row contract is exact future "
                "infrastructure, but current taste-radial x and C_sx/C_xx support "
                "cannot be relabeled as canonical O_H or C_sH/C_HH."
            ),
            next_admissible_artifact=(
                "same-surface canonical O_H identity/normalization certificate, "
                "or source-Higgs pole rows after x=O_H is certified"
            ),
        ),
    ]


def main() -> int:
    print("PR #230 W/Z accepted-action response root checkpoint")
    print("=" * 78)

    certs = {name: load(path) for name, path in PARENTS.items()}
    futures = future_presence()
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposals = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    frames = root_frames(certs, futures)
    root_closures = [item["name"] for item in frames if item["closes_wz_accepted_action_root"]]
    support_frames = [item["name"] for item in frames if item["support_loaded"]]

    forbidden_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    future_root_files_absent = not any(futures.values())
    minimal_cut_loaded = (
        certs["wz_same_source_action_minimal_cut"].get(
            "wz_same_source_action_minimal_certificate_cut_passed"
        )
        is True
        and certs["wz_same_source_action_minimal_cut"].get("proposal_allowed") is False
    )
    aggregate_denies = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("minimal-action-cut-loaded", minimal_cut_loaded, status(certs["wz_same_source_action_minimal_cut"]))
    report("sector-overlap-frame-loaded", "same_source_sector_overlap_identity" in support_frames, status(certs["same_source_sector_overlap_identity"]))
    report("adopted-radial-action-frame-loaded", "adopted_no_independent_top_radial_action" in support_frames, status(certs["radial_spurion_action_contract"]))
    report("wz-mass-fit-frame-loaded", "production_wz_correlator_mass_fit_path" in support_frames, status(certs["wz_correlator_mass_fit_path_gate"]))
    report("response-ratio-frame-loaded", "response_ratio_packet_after_action" in support_frames, status(certs["wz_response_ratio_contract"]))
    report("canonical-oh-shared-root-frame-loaded", "canonical_oh_shared_action_root" in support_frames, status(certs["canonical_higgs_operator_gate"]))
    report("no-action-root-frame-closes", not root_closures, str(root_closures))
    report("future-root-files-absent", future_root_files_absent, str(futures))
    report("aggregate-gates-deny-proposal", aggregate_denies, "assembly/retained/campaign proposal_allowed=false")
    report("forbidden-firewall-clean", forbidden_clean, str(FORBIDDEN_FIREWALL))

    passed = FAIL_COUNT == 0
    result = {
        "metadata": {
            "artifact": "yt_pr230_wz_accepted_action_response_root_checkpoint",
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
        "actual_current_surface_status": (
            "exact negative boundary / WZ accepted-action response root not closed "
            "by current sector-overlap, radial-action, or mass-fit candidates"
        ),
        "claim_type": "action_root_checkpoint_boundary",
        "conditional_surface_status": (
            "conditional-support if a future same-surface no-independent-top "
            "radial action, sector-overlap identity, canonical O_H certificate, "
            "and production W/Z mass-fit path land; additive-top subtraction "
            "and source-Higgs direct pole-row contracts are support-only until "
            "their required rows/certificates exist, and the canonical O_H hard "
            "residual equivalence gate remains an exact negative boundary"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "All W/Z action-root attacks remain support-only or blocked: the "
            "current sector-overlap identity is not supplied, the radial action "
            "contract is not adopted on the actual surface, additive-top "
            "subtraction rows are absent, production W/Z mass fits are absent, "
            "canonical O_H is absent, and downstream covariance and strict g2 "
            "authority are absent; the hard-residual equivalence gate supplies no "
            "current closure disjunct."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "wz_accepted_action_response_root_checkpoint_passed": passed,
        "current_route_blocked": not root_closures,
        "root_closures_found": root_closures,
        "support_frames_loaded": support_frames,
        "root_frames": frames,
        "future_artifact_presence": futures,
        "blocked_root_vertices": [
            "current same-source sector-overlap identity",
            "adopted no-independent-top radial action",
            "additive-top subtraction rows",
            "production W/Z correlator mass-fit path",
            "same-source top/W covariance and strict non-observed g2",
            "canonical O_H shared action root",
        ],
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim physical W/Z response closure",
            "does not write or validate an accepted same-source EW/Higgs action certificate",
            "does not assume k_top = k_gauge or an adopted radial-spurion action",
            "does not use static EW algebra, observed targets, H_unit, Ward identity, alpha_LM, plaquette, or u0 as authority",
            "does not identify taste-radial x with canonical O_H",
            "does not relabel C_sx/C_xx as C_sH/C_HH",
            "does not touch or relaunch the live chunk worker",
        ],
        "campaign_pivot": {
            "wz_route_status": "blocked_on_actual_current_surface_at_action_root",
            "next_queue_item": "canonical O_H / source-Higgs bridge hard residual",
            "next_exact_action": (
                "Pivot to the same-surface canonical O_H certificate or neutral "
                "rank-one/irreducibility theorem that would make the direct "
                "source-Higgs pole-row contract launchable; without that, keep "
                "source-Higgs rows as bounded support and do not alias C_sx/C_xx."
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
