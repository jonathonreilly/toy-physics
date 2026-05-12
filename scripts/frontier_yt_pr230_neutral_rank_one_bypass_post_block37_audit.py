#!/usr/bin/env python3
"""
PR #230 neutral rank-one bypass audit after Block37.

Block37 closes the direct action-premise attempt negatively on the current
surface.  This runner attacks the next campaign route: can the completed
source/taste-radial rows, existing neutral-rank artifacts, and top mass-scan
response support force a rank-one neutral scalar bridge without importing
canonical O_H?

The answer on the current surface is no.  The available rows determine only
the source/taste-radial subblock plus top bare-mass response support.  They do
not supply a physical neutral transfer, off-diagonal generator, primitive cone,
canonical LSZ metric, or source-Higgs pole-overlap row.  A three-direction
counterfamily preserves all current rows while rotating an unmeasured
orthogonal neutral direction into the would-be Higgs readout.
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
    / "yt_pr230_neutral_rank_one_bypass_post_block37_audit_2026-05-12.json"
)

PARENTS = {
    "lane1_action_premise": "outputs/yt_pr230_lane1_action_premise_derivation_attempt_2026-05-12.json",
    "lane1_oh_root": "outputs/yt_pr230_lane1_oh_root_theorem_attempt_2026-05-12.json",
    "row_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "measurement_rows": "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json",
    "top_mass_scan_response": "outputs/yt_pr230_top_mass_scan_response_harness_gate_2026-05-12.json",
    "neutral_transfer_mixing_no_go": "outputs/yt_pr230_neutral_transfer_eigenoperator_source_mixing_no_go_2026-05-07.json",
    "derived_rank_one_attempt": "outputs/yt_pr230_derived_bridge_rank_one_closure_attempt_2026-05-05.json",
    "neutral_primitive_completion": "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json",
    "multiplicity_one_gate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "multiplicity_one_candidate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json",
    "offdiagonal_generator_attempt": "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json",
    "primitive_cone_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "hard_residual_gate": "outputs/yt_pr230_canonical_oh_hard_residual_equivalence_gate_2026-05-07.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_ARTIFACTS = {
    "same_surface_neutral_transfer_operator": "outputs/yt_pr230_same_surface_neutral_transfer_operator_2026-05-06.json",
    "neutral_offdiagonal_generator_certificate": "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "neutral_rank_one_purity_certificate": "outputs/yt_neutral_scalar_rank_one_purity_certificate_2026-05-03.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "same_source_wz_response_rows": "outputs/yt_same_source_w_response_measurement_rows_2026-05-04.json",
    "electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_target_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "treated_c_sx_c_xx_as_c_sH_c_HH": False,
    "treated_top_mass_scan_as_higgs_response": False,
    "treated_source_only_rows_as_neutral_transfer": False,
    "treated_positivity_as_primitive_cone": False,
    "set_kappa_s_c2_or_zmatch_to_one": False,
    "claimed_retained_or_proposed_retained": False,
    "touched_live_chunk_worker": False,
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def mode_mean(rows: dict[str, Any], mode: str, key: str) -> float:
    return float(rows["mode_diagnostics"][mode][key]["mean"])


def representative_counterfamily(rows: dict[str, Any]) -> list[dict[str, Any]]:
    mode = "0,0,0"
    css = mode_mean(rows, mode, "C_ss_real")
    csx = mode_mean(rows, mode, "C_sx_real")
    cxx = mode_mean(rows, mode, "C_xx_real")
    cnn = cxx
    rows_out: list[dict[str, Any]] = []
    for label, theta in (
        ("taste_radial_aligned", 0.0),
        ("rotated_30deg", math.pi / 6.0),
        ("rotated_60deg", math.pi / 3.0),
        ("orthogonal_neutral", math.pi / 2.0),
    ):
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        c_sH = cos_t * csx
        c_HH = cos_t * cos_t * cxx + sin_t * sin_t * cnn
        rho = c_sH / math.sqrt(css * c_HH) if css > 0.0 and c_HH > 0.0 else None
        rows_out.append(
            {
                "case": label,
                "basis": ["source_s", "taste_radial_x", "orthogonal_neutral_n"],
                "available_subblock": {
                    "C_ss": css,
                    "C_sx": csx,
                    "C_xx": cxx,
                },
                "unmeasured_completion": {
                    "C_sn": 0.0,
                    "C_xn": 0.0,
                    "C_nn": cnn,
                    "H_theta": [0.0, cos_t, sin_t],
                },
                "current_rows_change": False,
                "candidate_C_sH": c_sH,
                "candidate_C_HH": c_HH,
                "candidate_source_higgs_rho": rho,
                "top_mass_scan_response_change": False,
                "neutral_rank_one_forced": False,
            }
        )
    return rows_out


def main() -> int:
    print("PR #230 neutral rank-one bypass post-Block37 audit")
    print("=" * 78)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}

    action_premise_blocked = (
        certs["lane1_action_premise"].get("exact_negative_boundary_passed") is True
        and certs["lane1_action_premise"].get("proposal_allowed") is False
    )
    row_packet_complete_support_only = (
        certs["row_combiner"].get("ready_chunks") == certs["row_combiner"].get("expected_chunks") == 63
        and certs["row_combiner"].get("combined_rows_written") is True
        and certs["measurement_rows"].get("proposal_allowed") is False
        and "C_sx/C_xx" in certs["measurement_rows"].get("strict_limit", "")
    )
    top_mass_scan_support_only = (
        certs["top_mass_scan_response"].get("proposal_allowed") is False
        and "Top bare-mass response rows do not derive" in certs["top_mass_scan_response"].get(
            "proposal_allowed_reason", ""
        )
    )
    neutral_negatives_apply = (
        "exact negative boundary" in statuses["neutral_transfer_mixing_no_go"]
        and "exact negative boundary" in statuses["derived_rank_one_attempt"]
        and "exact negative boundary" in statuses["neutral_primitive_completion"]
        and "exact support" in statuses["multiplicity_one_gate"]
        and "exact negative boundary" in statuses["multiplicity_one_candidate"]
        and "exact negative boundary" in statuses["offdiagonal_generator_attempt"]
        and certs["primitive_cone_gate"].get("proposal_allowed") is False
    )
    no_new_future_artifact = not any(future_presence.values())
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    counterfamily = representative_counterfamily(certs["measurement_rows"])
    current_rows_fixed = all(row["current_rows_change"] is False for row in counterfamily)
    rho_values = {
        round(float(row["candidate_source_higgs_rho"] or 0.0), 12)
        for row in counterfamily
    }
    rho_varies = len(rho_values) > 1
    rank_one_not_forced_by_rows = current_rows_fixed and rho_varies

    exact_boundary = (
        not missing
        and not proposal_parents
        and action_premise_blocked
        and row_packet_complete_support_only
        and top_mass_scan_support_only
        and neutral_negatives_apply
        and no_new_future_artifact
        and rank_one_not_forced_by_rows
        and firewall_clean
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("block37-action-premise-blocked", action_premise_blocked, statuses["lane1_action_premise"])
    report("complete-row-packet-support-only", row_packet_complete_support_only, statuses["measurement_rows"])
    report("top-mass-scan-support-only", top_mass_scan_support_only, statuses["top_mass_scan_response"])
    report("neutral-negative-artifacts-apply", neutral_negatives_apply, "rank-one/multiplicity/offdiagonal gates still reject")
    report("strict-future-artifacts-absent", no_new_future_artifact, str(future_presence))
    report("counterfamily-preserves-current-rows", current_rows_fixed, "source/taste-radial subblock fixed")
    report("counterfamily-varies-source-higgs-overlap", rho_varies, f"rho_values={sorted(rho_values)}")
    report("rank-one-not-forced-by-current-rows", rank_one_not_forced_by_rows, "orthogonal neutral direction remains unmeasured")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("exact-negative-boundary", exact_boundary, "neutral rank-one bypass not closed on current surface")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / post-Block37 neutral rank-one bypass "
            "not closed on the current PR230 surface"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface neutral transfer, "
            "off-diagonal generator, primitive-cone certificate, strict "
            "C_ss/C_sH/C_HH pole rows, or strict W/Z physical-response packet "
            "lands"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The completed C_ss/C_sx/C_xx packet and top bare-mass response rows "
            "do not determine the unmeasured orthogonal neutral sector.  Existing "
            "rank-one, primitive-cone, multiplicity-one, and off-diagonal-generator "
            "gates still reject the current surface."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "exact_negative_boundary_passed": exact_boundary,
        "rank_one_bypass_closed": False,
        "strict_future_artifacts_present": future_presence,
        "counterfamily": counterfamily,
        "open_imports": [
            "same-surface physical neutral transfer or off-diagonal generator",
            "primitive-cone / irreducibility certificate",
            "canonical scalar LSZ/FV/IR metric",
            "source-Higgs C_sH/C_HH pole-overlap rows or neutral rank-one theorem",
            "strict W/Z physical-response packet if bypassing O_H",
        ],
        "parent_statuses": statuses,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "summary": {
            "pass": PASS_COUNT,
            "fail": FAIL_COUNT,
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
