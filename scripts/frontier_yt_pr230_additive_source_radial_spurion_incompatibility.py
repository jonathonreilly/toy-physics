#!/usr/bin/env python3
"""
PR #230 additive-source / radial-spurion incompatibility gate.

This runner attacks the shared canonical O_H / accepted EW-Higgs action root
directly.  The tempting move is to keep the current PR230 additive top scalar
source S_top[m+s] and add an EW/Higgs source term with the same coordinate s,
then call that a same-source accepted action.

That is not enough.  The W/Z response route needs s to be a single canonical
Higgs radial spurion: top, W, and Z masses all respond only through v(s), with
no independent additive top-mass component.  If the current additive source is
kept, dS/ds contains an independent top scalar operator in addition to O_H,
and the response-ratio readout is contaminated by an unconstrained additive
top slope.

The result is an exact support/boundary artifact: it sharpens the action root
target.  It does not close PR #230 and does not authorize retained wording.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_additive_source_radial_spurion_incompatibility_2026-05-07.json"
)

PARENTS = {
    "same_source_ew_higgs_action_ansatz_gate": "outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json",
    "same_source_ew_action_adoption_attempt": "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json",
    "radial_spurion_sector_overlap_theorem": "outputs/yt_pr230_radial_spurion_sector_overlap_theorem_2026-05-06.json",
    "radial_spurion_action_contract": "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json",
    "wz_same_source_action_minimal_cut": "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json",
    "canonical_oh_wz_common_action_cut": "outputs/yt_pr230_canonical_oh_wz_common_action_cut_2026-05-07.json",
    "wz_same_source_ew_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "same_source_sector_overlap_obstruction": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "wz_response_ratio_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "source_higgs_pole_row_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def derivative_decomposition(ansatz: dict[str, Any]) -> dict[str, Any]:
    terms = ansatz.get("action_ansatz", {}).get("action_terms", [])
    additive_top = any("S_PR230_top[s]" in term and "additive top" in term for term in terms)
    higgs_source = any("s * sum_x" in term and "Phi" in term for term in terms)
    return {
        "same_coordinate": ansatz.get("action_ansatz", {})
        .get("source_derivative", {})
        .get("same_source_coordinate_as_top_fh_lsz")
        is True,
        "contains_current_additive_top_source": additive_top,
        "contains_higgs_composite_source": higgs_source,
        "dS_ds_if_both_present": "O_top_additive + O_H",
        "dS_ds_equals_canonical_OH_only": higgs_source and not additive_top,
        "obstruction": (
            "A same source label does not make dS/ds canonical O_H when the "
            "current additive top source remains in the same derivative."
        ),
    }


def radial_response_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for y_t, g2, dv_ds in ((0.7, 0.6, 0.25), (1.1, 0.8, 1.75)):
        dm = y_t * dv_ds / math.sqrt(2.0)
        d_w = g2 * dv_ds / 2.0
        rows.append(
            {
                "input_y_t": y_t,
                "input_g2": g2,
                "dv_ds": dv_ds,
                "additive_top_slope": 0.0,
                "dm_top_ds": dm,
                "dM_W_ds": d_w,
                "yt_from_topW": g2 * dm / (math.sqrt(2.0) * d_w),
            }
        )
    return rows


def additive_counter_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    y_t = 0.92
    g2 = 0.63
    dv_ds = 1.4
    d_w = g2 * dv_ds / 2.0
    for additive in (-0.4, -0.1, 0.0, 0.2, 0.5):
        dm = y_t * dv_ds / math.sqrt(2.0) + additive
        rows.append(
            {
                "input_y_t": y_t,
                "input_g2": g2,
                "dv_ds": dv_ds,
                "additive_top_slope": additive,
                "dm_top_ds": dm,
                "dM_W_ds": d_w,
                "yt_from_topW_if_unsubtracted": g2 * dm / (math.sqrt(2.0) * d_w),
            }
        )
    return rows


def pure_radial_recovers_yt(rows: list[dict[str, float]]) -> bool:
    return all(abs(row["yt_from_topW"] - row["input_y_t"]) < 1.0e-12 for row in rows)


def additive_contaminates(rows: list[dict[str, float]]) -> bool:
    values = [round(row["yt_from_topW_if_unsubtracted"], 12) for row in rows]
    return len(set(values)) > 1 and any(
        abs(row["yt_from_topW_if_unsubtracted"] - row["input_y_t"]) > 1.0e-12
        for row in rows
    )


def accepted_action_repair_options() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "repair": "replace the current additive top source with a true radial-spurion action",
            "required_payload": [
                "same-surface EW/Higgs action certificate",
                "top Yukawa term whose mass branch is m_t(s)=y_t v(s)/sqrt(2)",
                "no independent s * tbar t additive source",
                "W/Z mass-fit rows or source-Higgs C_sH/C_HH pole rows",
            ],
            "status": "open",
        },
        {
            "rank": 2,
            "repair": "measure and subtract the independent additive top component",
            "required_payload": [
                "separate source-coordinate Jacobian rows for additive top and radial Higgs directions",
                "matched covariance of the subtraction",
                "strict non-observed g2 if using W/Z response",
                "source-Higgs Gram or W/Z sector-overlap authority",
            ],
            "status": "open",
        },
        {
            "rank": 3,
            "repair": "bypass W/Z response with direct canonical O_H pole rows",
            "required_payload": [
                "same-surface canonical O_H certificate",
                "production C_ss/C_sH/C_HH pole rows",
                "Gram purity or orthogonal-neutral exclusion",
                "FV/IR/model-class and scalar-LSZ authority",
            ],
            "status": "open",
        },
    ]


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yukawa_as_selector": False,
        "used_observed_wz_masses_or_g2": False,
        "used_alpha_lm_or_plaquette_u0": False,
        "renamed_C_sx_C_xx_as_C_sH_C_HH": False,
        "set_kappa_s_equal_one": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_g2_equal_one": False,
        "claimed_retained_or_proposed_retained": False,
        "wrote_accepted_action_certificate": False,
        "touched_live_chunk_worker": False,
    }


def main() -> int:
    print("PR #230 additive-source / radial-spurion incompatibility gate")
    print("=" * 76)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposals = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    ansatz = certs["same_source_ew_higgs_action_ansatz_gate"]
    decomp = derivative_decomposition(ansatz)
    radial_rows = radial_response_rows()
    additive_rows = additive_counter_rows()
    firewall = forbidden_firewall()

    ansatz_present_support_only = (
        ansatz.get("same_source_ew_higgs_action_ansatz_gate_passed") is True
        and ansatz.get("current_surface_adoption_passed") is False
        and ansatz.get("proposal_allowed") is False
    )
    derivative_contains_two_operators = (
        decomp["same_coordinate"]
        and decomp["contains_current_additive_top_source"]
        and decomp["contains_higgs_composite_source"]
        and not decomp["dS_ds_equals_canonical_OH_only"]
    )
    radial_theorem_supports_clean_case = (
        certs["radial_spurion_sector_overlap_theorem"].get(
            "radial_spurion_sector_overlap_theorem_passed"
        )
        is True
        and certs["radial_spurion_sector_overlap_theorem"].get(
            "current_surface_sector_overlap_identity_supplied"
        )
        is False
    )
    action_contract_names_no_independent_source = (
        "no-independent-top-source radial-spurion action contract"
        in statuses["radial_spurion_action_contract"]
        and certs["radial_spurion_action_contract"].get("proposal_allowed") is False
    )
    adoption_shortcut_blocked = (
        certs["same_source_ew_action_adoption_attempt"].get("adoption_allowed_now")
        is False
        and certs["same_source_ew_action_adoption_attempt"].get(
            "same_source_ew_action_adoption_attempt_passed"
        )
        is True
    )
    common_cut_open = (
        certs["canonical_oh_wz_common_action_cut"].get("common_action_cut_passed")
        is True
        and certs["canonical_oh_wz_common_action_cut"].get(
            "common_canonical_oh_vertex_open"
        )
        is True
    )
    builder_rejects_current_action = (
        certs["wz_same_source_ew_action_builder"].get(
            "same_source_ew_action_certificate_valid"
        )
        is False
    )
    sector_overlap_obstructed = (
        certs["same_source_sector_overlap_obstruction"].get(
            "sector_overlap_identity_gate_passed"
        )
        is False
    )
    source_higgs_rows_absent = (
        certs["source_higgs_pole_row_contract"].get("closure_contract_satisfied")
        is False
    )
    aggregate_denies_proposal = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    pure_case_ok = pure_radial_recovers_yt(radial_rows)
    additive_case_bad = additive_contaminates(additive_rows)
    firewall_clean = not any(firewall.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("same-source-ansatz-present-support-only", ansatz_present_support_only, statuses["same_source_ew_higgs_action_ansatz_gate"])
    report("current-derivative-is-Otop-plus-OH", derivative_contains_two_operators, decomp["dS_ds_if_both_present"])
    report("pure-radial-spurion-response-recovers-yt", pure_case_ok, "a_top=0 witness rows")
    report("additive-top-source-contaminates-response", additive_case_bad, "a_top varied witness rows")
    report("radial-spurion-theorem-supports-clean-case", radial_theorem_supports_clean_case, statuses["radial_spurion_sector_overlap_theorem"])
    report("action-contract-requires-no-independent-top-source", action_contract_names_no_independent_source, statuses["radial_spurion_action_contract"])
    report("ansatz-only-adoption-shortcut-blocked", adoption_shortcut_blocked, statuses["same_source_ew_action_adoption_attempt"])
    report("common-canonical-OH-action-vertex-still-open", common_cut_open, statuses["canonical_oh_wz_common_action_cut"])
    report("accepted-action-builder-rejects-current-surface", builder_rejects_current_action, statuses["wz_same_source_ew_action_builder"])
    report("sector-overlap-identity-still-obstructed", sector_overlap_obstructed, statuses["same_source_sector_overlap_obstruction"])
    report("source-Higgs-pole-rows-absent", source_higgs_rows_absent, statuses["source_higgs_pole_row_contract"])
    report("aggregate-gates-deny-proposal", aggregate_denies_proposal, "proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(firewall))

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "exact support/boundary / current additive source is incompatible "
            "with accepted radial-spurion action closure"
        ),
        "claim_type": "open_gate",
        "audit_status_authority": "independent audit lane only",
        "conditional_surface_status": (
            "exact-support for future accepted action: closure may proceed if "
            "the action either removes the independent additive top source or "
            "measures/subtracts it with same-surface row authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current PR230 same-source ansatz keeps the additive top source "
            "and adds an O_H source under the same coordinate.  The resulting "
            "dS/ds is O_top_additive + O_H, not canonical O_H alone, and the "
            "top/W response ratio is contaminated unless the additive top "
            "component is removed or separately measured."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "additive_source_radial_spurion_incompatibility_passed": passed,
        "derivative_decomposition": decomp,
        "pure_radial_response_witness_rows": radial_rows,
        "additive_top_counterexample_rows": additive_rows,
        "accepted_action_repair_options": accepted_action_repair_options(),
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not write or validate an accepted EW/Higgs action certificate",
            "does not identify the current additive top source with canonical O_H",
            "does not relabel C_sx/C_xx as C_sH/C_HH",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, or unit normalization conventions",
            "does not touch the live chunk worker",
        ],
        "next_exact_action": (
            "Try a replacement-action certificate in which s is a true radial "
            "spurion for the top Yukawa branch, or build row-level subtraction "
            "authority for the additive top component.  Direct ansatz adoption "
            "with both O_top_additive and O_H under the same derivative is "
            "blocked."
        ),
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
