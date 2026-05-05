#!/usr/bin/env python3
"""
PR #230 fresh artifact route review.

This runner records the refreshed goal after the route-option review:
find one genuinely admissible artifact inside the listed PR230 contracts,
using the physics-loop assumption exercise and a targeted literature pass.

It is deliberately not a closure certificate.  It selects the cleanest next
artifact contract and documents why the current surface still has no
retained/proposed-retained authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_fresh_artifact_literature_route_review_2026-05-05.json"
)

PARENTS = {
    "assumption_stress": "outputs/yt_pr230_assumption_import_stress_2026-05-01.json",
    "osp_oh_literature_bridge": "outputs/yt_osp_oh_literature_bridge_2026-05-04.json",
    "fms_oh_certificate_construction_attempt": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
    "clean_source_higgs_math_tool_selector": "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json",
    "canonical_higgs_operator_certificate_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_production_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_g2_bare_running_bridge_attempt": "outputs/yt_pr230_wz_g2_bare_running_bridge_attempt_2026-05-05.json",
    "schur_abc_definition_derivation_attempt": "outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json",
    "scalar_lsz_carleman_tauberian_attempt": "outputs/yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt_2026-05-05.json",
    "neutral_offdiagonal_generator_derivation_attempt": "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json",
    "full_positive_closure_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_ARTIFACTS = {
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_cross_correlator_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "top_wz_matched_response_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
    "schur_kernel_rows": "outputs/yt_schur_kernel_rows_2026-05-03.json",
    "scalar_lsz_stieltjes_moment_certificate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_2026-05-05.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
}

LITERATURE_ROWS = [
    {
        "id": "fms_bound_state_spectrum",
        "url": "https://arxiv.org/abs/1912.08680",
        "role": (
            "FMS gives the right operator language: physical Higgs states are "
            "handled through gauge-invariant composite operators once the "
            "gauge-Higgs action is supplied."
        ),
        "pr230_boundary": (
            "It does not identify the current PR230 scalar source with O_H and "
            "does not supply C_sH/C_HH rows."
        ),
    },
    {
        "id": "fms_higgs_resonance",
        "url": "https://arxiv.org/abs/2009.06671",
        "role": (
            "FMS pole matching motivates an O_H pole-residue certificate rather "
            "than a source-only scalar readout."
        ),
        "pr230_boundary": (
            "Pole matching in an EW Higgs theory is not a current-surface "
            "Cl(3)/Z3 source-overlap theorem."
        ),
    },
    {
        "id": "feynman_hellmann_qft",
        "url": "https://doi.org/10.1103/PhysRevD.96.014504",
        "role": (
            "FH justifies measuring matrix elements from energy shifts and "
            "two-point functions."
        ),
        "pr230_boundary": (
            "FH does not normalize the scalar source into the canonical Higgs "
            "field; kappa_s remains load-bearing."
        ),
    },
    {
        "id": "lellouch_luscher_fv_matrix_elements",
        "url": "https://cds.cern.ch/record/432699",
        "role": (
            "Finite-volume matrix-element machinery is relevant to strict "
            "LSZ/FV normalization if the required spectra and row identities exist."
        ),
        "pr230_boundary": (
            "It does not create source-Higgs identity and cannot act on the "
            "current finite source-only row set as closure."
        ),
    },
    {
        "id": "rome_southampton_ri_mom",
        "url": "https://cds.cern.ch/record/271679",
        "role": (
            "Nonperturbative operator renormalization can normalize composite "
            "operators in a chosen scheme."
        ),
        "pr230_boundary": (
            "A scalar-density renormalization scheme is not the canonical-Higgs "
            "identity or source-pole purity certificate."
        ),
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}


def contract_rows(parent_statuses: dict[str, str]) -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "contract": "O_H/C_sH/C_HH source-Higgs pole rows",
            "selected_as_cleanest": True,
            "why": (
                "This is the only option that attacks the missing "
                "source-to-canonical-Higgs normalization directly."
            ),
            "current_blocker": parent_statuses["source_higgs_production_readiness"],
            "first_genuine_artifact": FUTURE_ARTIFACTS[
                "canonical_higgs_operator_certificate"
            ],
            "second_genuine_artifact": FUTURE_ARTIFACTS[
                "source_higgs_cross_correlator_rows"
            ],
            "fresh_route": (
                "Action-first FMS route: define a same-source EW/Higgs action "
                "on the PR230 surface, construct gauge-invariant O_H with "
                "canonical pole normalization, then measure C_ss/C_sH/C_HH."
            ),
            "current_admissible_for_closure": False,
        },
        {
            "rank": 2,
            "contract": "genuine same-source W/Z response rows",
            "selected_as_cleanest": False,
            "why": (
                "Physical-response fallback, but it adds same-source EW action, "
                "identity/covariance, strict g2, and correction obligations."
            ),
            "current_blocker": parent_statuses["wz_g2_bare_running_bridge_attempt"],
            "first_genuine_artifact": FUTURE_ARTIFACTS["top_wz_matched_response_rows"],
            "current_admissible_for_closure": False,
        },
        {
            "rank": 3,
            "contract": "strict scalar-LSZ moment/threshold/FV authority",
            "selected_as_cleanest": False,
            "why": (
                "Needed downstream, but finite source-only rows cannot determine "
                "the source-Higgs overlap or pole residue."
            ),
            "current_blocker": parent_statuses["scalar_lsz_carleman_tauberian_attempt"],
            "first_genuine_artifact": FUTURE_ARTIFACTS[
                "scalar_lsz_stieltjes_moment_certificate"
            ],
            "current_admissible_for_closure": False,
        },
        {
            "rank": 4,
            "contract": "Schur A/B/C kernel rows",
            "selected_as_cleanest": False,
            "why": (
                "Useful for K-prime/orthogonal-sector control, but the current "
                "surface lacks row definitions and source/orthogonal projectors."
            ),
            "current_blocker": parent_statuses["schur_abc_definition_derivation_attempt"],
            "first_genuine_artifact": FUTURE_ARTIFACTS["schur_kernel_rows"],
            "current_admissible_for_closure": False,
        },
        {
            "rank": 5,
            "contract": "neutral primitive-cone or irreducibility certificate",
            "selected_as_cleanest": False,
            "why": (
                "Could collapse the neutral sector, but current rows remain "
                "source-only or block diagonal."
            ),
            "current_blocker": parent_statuses[
                "neutral_offdiagonal_generator_derivation_attempt"
            ],
            "first_genuine_artifact": FUTURE_ARTIFACTS[
                "neutral_primitive_cone_certificate"
            ],
            "current_admissible_for_closure": False,
        },
    ]


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity_as_authority": False,
        "used_observed_top_mass_or_yt_selector": False,
        "used_alpha_lm_plaquette_u0_or_rconn": False,
        "used_reduced_pilots_as_production_evidence": False,
        "set_c2_equal_one_without_derivation": False,
        "set_z_match_equal_one_without_derivation": False,
        "set_kappa_s_equal_one_without_derivation": False,
        "used_g2_by_convention": False,
        "used_pslq_or_method_name_as_proof_selector": False,
    }


def main() -> int:
    print("PR #230 fresh artifact route review")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    future_present = future_presence()
    contracts = contract_rows(statuses)
    selected = contracts[0]
    firewall = forbidden_firewall()

    assumption_stress_loaded = (
        "assumption-import stress" in statuses["assumption_stress"]
        and parents["assumption_stress"].get("proposal_allowed") is False
    )
    prior_literature_loaded = (
        "O_sp/O_H literature bridge" in statuses["osp_oh_literature_bridge"]
        and parents["osp_oh_literature_bridge"].get("literature_bridge_passed") is True
        and parents["osp_oh_literature_bridge"].get("proposal_allowed") is False
    )
    fms_current_surface_blocked = (
        "FMS O_H certificate construction blocked"
        in statuses["fms_oh_certificate_construction_attempt"]
        and parents["fms_oh_certificate_construction_attempt"].get(
            "fms_oh_certificate_available"
        )
        is False
    )
    clean_selector_loaded = (
        "clean source-Higgs outside-math route selector"
        in statuses["clean_source_higgs_math_tool_selector"]
        and parents["clean_source_higgs_math_tool_selector"].get(
            "clean_physics_priority"
        )
        == "source_higgs"
        and parents["clean_source_higgs_math_tool_selector"].get("proposal_allowed")
        is False
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_certificate_gate"].get("candidate_present")
        is False
        and parents["canonical_higgs_operator_certificate_gate"].get("candidate_valid")
        is False
        and not future_present["canonical_higgs_operator_certificate"]
    )
    source_higgs_rows_absent = not future_present["source_higgs_cross_correlator_rows"]
    same_source_ew_action_absent = (
        parents["same_source_ew_action_gate"].get("same_source_ew_action_ready")
        is False
    )
    assembly_open = (
        parents["full_positive_closure_assembly"].get("proposal_allowed") is False
        and parents["full_positive_closure_assembly"].get("closure_allowed") is not True
    )
    retained_open = (
        parents["retained_route"].get("proposal_allowed") is False
        and parents["retained_route"].get("bare_retained_allowed") is not True
    )
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False
    no_forbidden_imports = all(value is False for value in firewall.values())
    literature_context_only = all(
        "does not" in row["pr230_boundary"].lower()
        or "not" in row["pr230_boundary"].lower()
        for row in LITERATURE_ROWS
    )
    one_selected_contract = sum(
        1 for row in contracts if row["selected_as_cleanest"] is True
    ) == 1
    all_contracts_not_current_closure = all(
        row["current_admissible_for_closure"] is False for row in contracts
    )
    current_surface_has_genuine_artifact = any(future_present.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("assumption-stress-loaded", assumption_stress_loaded, statuses["assumption_stress"])
    report("prior-literature-bridge-loaded", prior_literature_loaded, statuses["osp_oh_literature_bridge"])
    report("fms-current-surface-blocked", fms_current_surface_blocked, statuses["fms_oh_certificate_construction_attempt"])
    report("clean-source-higgs-selector-loaded", clean_selector_loaded, statuses["clean_source_higgs_math_tool_selector"])
    report("canonical-oh-artifact-absent", canonical_oh_absent, FUTURE_ARTIFACTS["canonical_higgs_operator_certificate"])
    report("source-higgs-row-artifact-absent", source_higgs_rows_absent, FUTURE_ARTIFACTS["source_higgs_cross_correlator_rows"])
    report("same-source-ew-action-absent", same_source_ew_action_absent, statuses["same_source_ew_action_gate"])
    report("literature-context-only", literature_context_only, f"sources={len(LITERATURE_ROWS)}")
    report("one-contract-selected", one_selected_contract, selected["contract"])
    report("all-contracts-not-current-closure", all_contracts_not_current_closure, "all reviewed options remain future-only")
    report("current-surface-has-no-listed-genuine-artifact", not current_surface_has_genuine_artifact, str(future_present))
    report("full-assembly-still-open", assembly_open, statuses["full_positive_closure_assembly"])
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))

    review_passed = (
        not missing
        and not proposal_allowed
        and assumption_stress_loaded
        and prior_literature_loaded
        and fms_current_surface_blocked
        and clean_selector_loaded
        and canonical_oh_absent
        and source_higgs_rows_absent
        and same_source_ew_action_absent
        and literature_context_only
        and one_selected_contract
        and all_contracts_not_current_closure
        and not current_surface_has_genuine_artifact
        and assembly_open
        and retained_open
        and campaign_open
        and no_forbidden_imports
    )

    result = {
        "actual_current_surface_status": (
            "bounded-support / fresh artifact literature route review; "
            "selected O_H/C_sH/C_HH action-first FMS contract, no current closure"
        ),
        "goal_refresh": (
            "Find one genuinely admissible artifact inside the PR230 contracts; "
            "do not claim retained/proposed_retained closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No listed current-surface artifact is present.  The review selects "
            "the source-Higgs O_H/C_sH/C_HH contract as the cleanest artifact "
            "target, but the first required certificate is still absent."
        ),
        "bare_retained_allowed": False,
        "review_passed": review_passed,
        "genuine_artifact_found_on_current_surface": current_surface_has_genuine_artifact,
        "selected_genuine_artifact_contract": selected,
        "contract_ranking": contracts,
        "future_artifact_presence": future_present,
        "literature_rows": LITERATURE_ROWS,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not write or imply an O_H certificate",
            "does not treat FMS, FH, Lellouch-Luscher, RI/MOM, PSLQ, or any method name as proof authority",
            "does not import H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, R_conn, c2=1, Z_match=1, kappa_s=1, or g2 by convention",
            "does not treat source-only rows, reduced pilots, finite shells, or absent guards as physics evidence",
        ],
        "exact_next_action": (
            "Start from the O_H/C_sH/C_HH contract, not from another source-only "
            "shortcut: derive or implement a same-source EW/Higgs action on the "
            "PR230 surface, construct a gauge-invariant FMS-style O_H with "
            "canonical pole normalization, write the canonical O_H certificate, "
            "then produce C_ss/C_sH/C_HH pole rows and rerun the Gram-purity, "
            "scalar-LSZ, full assembly, retained-route, and campaign gates."
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
