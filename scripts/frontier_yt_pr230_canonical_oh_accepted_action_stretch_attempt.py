#!/usr/bin/env python3
"""
PR #230 canonical O_H / accepted EW-Higgs action stretch attempt.

This runner attacks the rank-1 campaign opportunity after the common-cut
checkpoint: can the current same-surface support stack be composed into the
non-shortcut canonical O_H / accepted EW-Higgs action certificate needed by
both the source-Higgs and W/Z routes?

The answer on the actual current surface is no.  The runner records the
minimal allowed premise set, rejects the tempting import routes, and leaves a
specific pivot target for the next W/Z accepted-action block.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_canonical_oh_accepted_action_stretch_attempt_2026-05-07.json"
)

PARENTS = {
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_higgs_repo_authority_audit": "outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json",
    "degree_one_radial_tangent_oh": "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json",
    "degree_one_higgs_action_premise_gate": "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json",
    "sm_one_higgs_oh_import_boundary": "outputs/yt_sm_one_higgs_oh_import_boundary_2026-05-03.json",
    "one_higgs_taste_axis_completeness": "outputs/yt_pr230_one_higgs_taste_axis_completeness_attempt_2026-05-06.json",
    "two_source_taste_radial_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "taste_radial_to_source_higgs_promotion": "outputs/yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json",
    "source_higgs_pole_row_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "source_higgs_time_kernel_production_manifest": "outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json",
    "source_higgs_production_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "wz_same_source_action_cut": "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json",
    "wz_response_ratio_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "canonical_oh_wz_common_cut": "outputs/yt_pr230_canonical_oh_wz_common_action_cut_2026-05-07.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_observed_top_or_yukawa_as_selector": False,
    "used_observed_wz_masses_or_g2": False,
    "used_alpha_lm_or_plaquette_u0": False,
    "used_reduced_pilots_as_production_evidence": False,
    "used_static_ew_algebra_as_action_authority": False,
    "renamed_C_sx_C_xx_as_C_sH_C_HH": False,
    "identified_taste_radial_x_as_canonical_OH": False,
    "treated_support_contract_as_current_action_authority": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "set_g2_equal_one": False,
    "touched_live_chunk_worker": False,
    "claimed_retained_or_proposed_retained": False,
}

A_MIN = [
    "Cl(3)/Z^3 substrate and current PR230 same-surface source primitives",
    "same-surface two-source taste-radial action vertex as support only",
    "degree-one radial-tangent O_H theorem only under its explicit future action premise",
    "canonical-Higgs certificate schema and repo authority audit",
    "source-Higgs pole-row and promotion contracts as acceptance gates",
    "W/Z same-source action cut and response-ratio algebra as support gates",
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load(relpath: str) -> dict[str, Any]:
    path = ROOT / relpath
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def frame(
    name: str,
    *,
    route: str,
    support_loaded: bool,
    closes_root: bool,
    obstruction: str,
    evidence: list[str],
    next_move: str,
) -> dict[str, Any]:
    return {
        "name": name,
        "route": route,
        "support_loaded": support_loaded,
        "closes_canonical_oh_accepted_action_root": closes_root,
        "obstruction": obstruction,
        "evidence": evidence,
        "next_move": next_move,
    }


def stretch_frames(certs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    canonical = certs["canonical_higgs_operator_gate"]
    authority = certs["canonical_higgs_repo_authority_audit"]
    degree = certs["degree_one_radial_tangent_oh"]
    premise = certs["degree_one_higgs_action_premise_gate"]
    sm_one_higgs = certs["sm_one_higgs_oh_import_boundary"]
    one_higgs_axis = certs["one_higgs_taste_axis_completeness"]
    two_source = certs["two_source_taste_radial_action"]
    promotion = certs["taste_radial_to_source_higgs_promotion"]
    pole_contract = certs["source_higgs_pole_row_contract"]
    time_kernel_manifest = certs["source_higgs_time_kernel_production_manifest"]
    readiness = certs["source_higgs_production_readiness"]
    wz_cut = certs["wz_same_source_action_cut"]
    wz_ratio = certs["wz_response_ratio_contract"]

    return [
        frame(
            "schema_completion",
            route="supply canonical-Higgs operator certificate directly",
            support_loaded=canonical.get("candidate_present") is False
            and canonical.get("candidate_valid") is False,
            closes_root=False,
            obstruction=(
                "The accepted certificate file is absent; the schema is known, "
                "but no identity or normalization certificate satisfying it is present."
            ),
            evidence=[status(canonical), status(authority)],
            next_move=(
                "Write a genuine canonical-Higgs certificate with non-self "
                "identity and normalization references, or keep the gate open."
            ),
        ),
        frame(
            "degree_one_radial_tangent",
            route="promote the implemented taste-radial vertex to canonical O_H",
            support_loaded=degree.get("degree_one_radial_tangent_oh_theorem_passed")
            is True
            and two_source.get("two_source_taste_radial_action_passed") is True,
            closes_root=False,
            obstruction=(
                "The degree-one theorem is conditional on the missing same-surface "
                "EW/Higgs action premise; current Z3/source filters remain nonunique."
            ),
            evidence=[status(degree), status(premise), status(two_source)],
            next_move=(
                "Do not identify x with O_H until a same-surface action or "
                "canonical-operator theorem supplies the degree-one premise."
            ),
        ),
        frame(
            "sm_ew_one_higgs_import",
            route="import O_H from SM one-Higgs or EW gauge-mass algebra",
            support_loaded="one-Higgs" in status(sm_one_higgs)
            and one_higgs_axis.get("exact_negative_boundary_passed") is True,
            closes_root=False,
            obstruction=(
                "SM/EW theorems assume canonical H after it is supplied; they "
                "do not identify a PR230 taste/source operator or remove "
                "orthogonal neutral top couplings."
            ),
            evidence=[status(sm_one_higgs), status(one_higgs_axis)],
            next_move=(
                "Use SM/EW algebra only downstream of a same-surface PR230 "
                "operator/action certificate."
            ),
        ),
        frame(
            "source_higgs_pole_promotion",
            route="promote C_sx/C_xx rows into C_sH/C_HH rows",
            support_loaded=(
                promotion.get("promotion_contract_passed") is True
                and pole_contract.get("proposal_allowed") is False
                and time_kernel_manifest.get("proposal_allowed") is False
                and time_kernel_manifest.get("chunk_count") == 63
            ),
            closes_root=False,
            obstruction=(
                "The promotion contract explicitly blocks relabeling before "
                "x=canonical O_H, LSZ/metric normalization, pole rows, FV/IR, "
                "and Gram-purity authority exist."
            ),
            evidence=[
                status(promotion),
                status(pole_contract),
                status(time_kernel_manifest),
                status(readiness),
            ],
            next_move=(
                "Continue taste-radial rows only as bounded support until the "
                "canonical O_H identity and production pole gates pass."
            ),
        ),
        frame(
            "wz_accepted_action",
            route="bypass source-Higgs rows with W/Z same-source response",
            support_loaded=wz_cut.get("wz_same_source_action_minimal_certificate_cut_passed")
            is True
            and wz_ratio.get("wz_response_ratio_identifiability_contract_passed")
            is True,
            closes_root=False,
            obstruction=(
                "The W/Z cut still lacks canonical O_H, current same-source "
                "sector-overlap/adopted radial action, and W/Z mass-fit path; "
                "response rows, matched covariance, and strict g2 are also absent."
            ),
            evidence=[status(wz_cut), status(wz_ratio)],
            next_move=(
                "Pivot to one W/Z action-root vertex that can move without "
                "pretending the full physical response packet exists: current "
                "sector-overlap/adopted radial action or W/Z mass-fit path."
            ),
        ),
    ]


def main() -> int:
    print("PR #230 canonical O_H / accepted EW-Higgs action stretch attempt")
    print("=" * 78)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposals = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    frames = stretch_frames(certs)

    root_closures = [item["name"] for item in frames if item["closes_canonical_oh_accepted_action_root"]]
    support_frames_loaded = [item["name"] for item in frames if item["support_loaded"]]
    all_frames_blocked = not root_closures and len(frames) == 5
    forbidden_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    aggregate_denies = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
        and certs["canonical_oh_wz_common_cut"].get("proposal_allowed") is False
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("minimal-premise-set-recorded", len(A_MIN) == 6, str(A_MIN))
    report("schema-frame-loaded", "schema_completion" in support_frames_loaded, status(certs["canonical_higgs_operator_gate"]))
    report("degree-one-frame-loaded", "degree_one_radial_tangent" in support_frames_loaded, status(certs["degree_one_radial_tangent_oh"]))
    report("sm-ew-frame-loaded", "sm_ew_one_higgs_import" in support_frames_loaded, status(certs["sm_one_higgs_oh_import_boundary"]))
    report("source-higgs-frame-loaded", "source_higgs_pole_promotion" in support_frames_loaded, status(certs["taste_radial_to_source_higgs_promotion"]))
    report("wz-frame-loaded", "wz_accepted_action" in support_frames_loaded, status(certs["wz_same_source_action_cut"]))
    report("no-frame-closes-common-root", all_frames_blocked, str(root_closures))
    report("aggregate-gates-deny-proposal", aggregate_denies, "assembly/retained/campaign/common-cut proposal_allowed=false")
    report("forbidden-firewall-clean", forbidden_clean, str(FORBIDDEN_FIREWALL))

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "exact negative boundary / canonical O_H accepted-action root not "
            "derivable from the current PR230 support stack"
        ),
        "claim_type": "stretch_attempt_boundary",
        "conditional_surface_status": (
            "conditional-support if a future same-surface canonical O_H identity, "
            "accepted EW/Higgs action, or W/Z action-root certificate lands"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Every current route is support-only or blocked: canonical O_H "
            "candidate absent, degree-one premise unproved, SM/EW one-Higgs "
            "imports rejected, C_sx/C_xx promotion forbidden, and W/Z accepted "
            "action root vertices still open."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "stretch_attempt_passed": passed,
        "a_min": A_MIN,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "attack_frames": frames,
        "support_frames_loaded": support_frames_loaded,
        "root_closures_found": root_closures,
        "current_route_blocked": all_frames_blocked,
        "pivot_decision": {
            "rank_1_canonical_oh_root_status": "blocked_on_actual_surface",
            "next_queue_item": "W/Z accepted-action response root attack",
            "next_exact_action": (
                "Attack one W/Z action-root vertex without claiming physical "
                "response closure: current same-source sector-overlap/adopted "
                "radial action, or production W/Z correlator mass-fit path.  "
                "Canonical O_H remains a shared blocker and must not be assumed."
            ),
            "source_higgs_rows_status": (
                "continue only as bounded support until x=canonical O_H and "
                "source-Higgs pole/Gram/FV/IR gates pass"
            ),
        },
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not write or validate a canonical O_H or accepted EW-Higgs action certificate",
            "does not identify taste-radial x with canonical O_H",
            "does not relabel C_sx/C_xx as C_sH/C_HH",
            "does not treat the source-Higgs time-kernel production manifest as row evidence",
            "does not treat SM/EW one-Higgs algebra, support contracts, or static response formulas as current action authority",
            "does not use forbidden imports or touch the live chunk worker",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
