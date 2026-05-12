#!/usr/bin/env python3
"""
PR #230 top-mass-scan subtraction-contract applicability audit.

This block checks a narrow W/Z repair shortcut after the top mass-scan response
harness landed: whether the new dE/dm_bare rows satisfy the additive-top
subtraction row contract.  They do not.  The rows are useful support for future
same-ensemble subtraction/covariance work, but the strict contract still needs
mixed-source total top rows, additive-top rows in the same coordinate
convention, W/Z response rows, matched covariance, strict g2/v authority, and
accepted action authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_top_mass_scan_subtraction_contract_applicability_audit_2026-05-12.json"
)

PARENTS = {
    "top_mass_scan_response_harness_gate": "outputs/yt_pr230_top_mass_scan_response_harness_gate_2026-05-12.json",
    "top_mass_scan_response_smoke": "outputs/yt_pr230_top_mass_scan_response_harness_smoke_2026-05-12.json",
    "additive_top_subtraction_row_contract": "outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json",
    "additive_top_jacobian_rows": "outputs/yt_pr230_additive_top_jacobian_rows_2026-05-07.json",
    "block35_physical_bridge_admission": "outputs/yt_pr230_block35_post_block34_physical_bridge_admission_checkpoint_2026-05-11.json",
    "wz_physical_response_packet_intake": "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json",
    "wz_accepted_action_response_root": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
    "wz_response_ratio_identifiability_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "electroweak_g2_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

REQUIRED_STRICT_ROWS = {
    "mixed_source_total_top_rows": "outputs/yt_pr230_mixed_source_total_top_response_rows_2026-05-12.json",
    "strict_additive_top_rows": "outputs/yt_pr230_strict_additive_top_response_rows_2026-05-12.json",
    "wz_response_rows": "outputs/yt_pr230_wz_response_ratio_rows_2026-05-07.json",
    "matched_subtraction_covariance": "outputs/yt_pr230_top_additive_wz_matched_covariance_2026-05-07.json",
    "strict_electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "subtracted_response_readout": "outputs/yt_pr230_additive_top_subtracted_response_readout_2026-05-07.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_top_or_yukawa_as_selector": False,
    "used_observed_wz_or_g2": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "treated_dE_dm_bare_as_dE_dh": False,
    "treated_mass_scan_as_wz_response": False,
    "treated_bounded_additive_rows_as_strict_subtraction": False,
    "assumed_matched_covariance": False,
    "set_additive_top_slope_to_zero": False,
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


def load(rel: str | Path) -> dict[str, Any]:
    path = Path(rel)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def path_present(rel: str) -> bool:
    return (ROOT / rel).exists()


def first_ensemble(smoke: dict[str, Any]) -> dict[str, Any]:
    ensembles = smoke.get("ensembles")
    if isinstance(ensembles, list) and ensembles and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def top_mass_scan_payload(smoke: dict[str, Any]) -> dict[str, Any]:
    ensemble = first_ensemble(smoke)
    payload = ensemble.get("top_mass_scan_response_analysis", {})
    return payload if isinstance(payload, dict) else {}


def metadata_payload(smoke: dict[str, Any]) -> dict[str, Any]:
    metadata = smoke.get("metadata", {})
    if not isinstance(metadata, dict):
        return {}
    top_meta = metadata.get("top_mass_scan_response", {})
    return top_meta if isinstance(top_meta, dict) else {}


def row_keys(payload: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    for field in ("per_configuration_slopes", "per_configuration_multi_tau_slopes"):
        rows = payload.get(field, [])
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict):
                    keys.update(str(key) for key in row)
                    by_tau = row.get("slope_dE_dm_bare_by_tau")
                    if isinstance(by_tau, dict):
                        keys.add("slope_dE_dm_bare_by_tau")
    return keys


def main() -> int:
    print("PR #230 top-mass-scan subtraction-contract applicability audit")
    print("=" * 82)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    failing = [
        name
        for name, cert in certs.items()
        if int(cert.get("fail_count", cert.get("fails", 0)) or 0) != 0
    ]
    proposal_parents = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    smoke = certs["top_mass_scan_response_smoke"]
    top_payload = top_mass_scan_payload(smoke)
    top_meta = metadata_payload(smoke)
    keys = row_keys(top_payload)
    strict_presence = {name: path_present(path) for name, path in REQUIRED_STRICT_ROWS.items()}

    top_harness_support_only = (
        "top mass-scan response harness schema gate"
        in statuses["top_mass_scan_response_harness_gate"]
        and certs["top_mass_scan_response_harness_gate"].get("proposal_allowed") is False
        and certs["top_mass_scan_response_harness_gate"].get(
            "top_mass_scan_response_harness_gate_passed"
        )
        is True
        and certs["top_mass_scan_response_harness_gate"].get("row_schema_version")
        == "top_mass_scan_response_v1"
    )
    top_rows_are_additive_bare_mass = (
        top_payload.get("source_coordinate") == "uniform additive Dirac bare mass m_bare"
        and top_meta.get("source_coordinate") == "uniform additive Dirac bare mass m_bare"
        and "slope_dE_dm_bare_tau1" in keys
        and "slope_dE_dm_bare_by_tau" in keys
        and "dE_dh" not in keys
        and "T_total" not in keys
        and "A_top" not in keys
        and "W" not in keys
    )
    top_rows_not_physical_higgs = (
        top_payload.get("physical_higgs_normalization") == "not_derived"
        and top_payload.get("used_as_physical_yukawa_readout") is False
        and "not dE/dh" in str(top_payload.get("strict_limit", ""))
        and top_meta.get("extra_solve_count") == 0
        and top_meta.get("uses_existing_three_mass_top_correlator_scan") is True
    )
    subtraction_contract_open = (
        "additive-top subtraction row contract"
        in statuses["additive_top_subtraction_row_contract"]
        and certs["additive_top_subtraction_row_contract"].get(
            "additive_top_subtraction_row_contract_passed"
        )
        is True
        and certs["additive_top_subtraction_row_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and certs["additive_top_subtraction_row_contract"].get("proposal_allowed")
        is False
    )
    additive_rows_bounded_not_strict = (
        "bounded-support / additive-top coarse Jacobian rows"
        in statuses["additive_top_jacobian_rows"]
        and certs["additive_top_jacobian_rows"].get(
            "bounded_additive_top_jacobian_rows_passed"
        )
        is True
        and certs["additive_top_jacobian_rows"].get(
            "strict_additive_top_jacobian_rows_passed"
        )
        is False
        and certs["additive_top_jacobian_rows"].get("proposal_allowed") is False
    )
    strict_packet_absent = not any(strict_presence.values())
    block35_not_admitted = (
        certs["block35_physical_bridge_admission"].get(
            "block35_post_block34_physical_bridge_admission_checkpoint_passed"
        )
        is True
        and certs["block35_physical_bridge_admission"].get("checks", {}).get(
            "top-mass-scan-response-committed-support-only"
        )
        is True
        and certs["block35_physical_bridge_admission"].get("checks", {}).get(
            "wz-physical-response-not-admitted"
        )
        is True
        and certs["block35_physical_bridge_admission"].get("proposal_allowed")
        is False
    )
    wz_packet_absent = (
        "WZ physical-response packet not present"
        in statuses["wz_physical_response_packet_intake"]
        and certs["wz_physical_response_packet_intake"].get(
            "wz_physical_response_packet_intake_checkpoint_passed"
        )
        is True
        and certs["wz_physical_response_packet_intake"].get("proposal_allowed")
        is False
    )
    covariance_absent = (
        "matched top-W response rows absent"
        in statuses["top_wz_matched_covariance_builder"]
        and certs["top_wz_matched_covariance_builder"].get(
            "strict_top_wz_matched_covariance_builder_passed"
        )
        is False
    )
    g2_absent = (
        "electroweak g2 certificate builder inputs absent"
        in statuses["electroweak_g2_builder"]
        and certs["electroweak_g2_builder"].get(
            "strict_electroweak_g2_certificate_passed"
        )
        is False
    )
    aggregate_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    audit_passed = all(
        [
            not missing,
            not failing,
            not proposal_parents,
            top_harness_support_only,
            top_rows_are_additive_bare_mass,
            top_rows_not_physical_higgs,
            subtraction_contract_open,
            additive_rows_bounded_not_strict,
            strict_packet_absent,
            block35_not_admitted,
            wz_packet_absent,
            covariance_absent,
            g2_absent,
            aggregate_still_open,
            firewall_clean,
        ]
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("parent-certificates-have-no-fails", not failing, f"failing={failing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("top-mass-scan-harness-support-only", top_harness_support_only, statuses["top_mass_scan_response_harness_gate"])
    report("top-rows-are-additive-bare-mass", top_rows_are_additive_bare_mass, str(sorted(keys)))
    report("top-rows-not-physical-higgs", top_rows_not_physical_higgs, str(top_payload.get("strict_limit", "")))
    report("subtraction-contract-still-open", subtraction_contract_open, statuses["additive_top_subtraction_row_contract"])
    report("additive-rows-bounded-not-strict", additive_rows_bounded_not_strict, statuses["additive_top_jacobian_rows"])
    report("strict-subtraction-packet-absent", strict_packet_absent, str(strict_presence))
    report("block35-did-not-admit-top-mass-scan-bridge", block35_not_admitted, statuses["block35_physical_bridge_admission"])
    report("wz-physical-packet-absent", wz_packet_absent, statuses["wz_physical_response_packet_intake"])
    report("matched-covariance-absent", covariance_absent, statuses["top_wz_matched_covariance_builder"])
    report("strict-g2-absent", g2_absent, statuses["electroweak_g2_builder"])
    report("aggregate-gates-still-open", aggregate_still_open, statuses["full_positive_assembly"])
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("top-mass-scan-subtraction-contract-applicability-audit", audit_passed, "mass-scan rows do not satisfy strict subtraction packet")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / top mass-scan response harness does not "
            "satisfy the additive-top subtraction row contract"
        ),
        "conditional_surface_status": (
            "conditional-support if future same-ensemble rows provide mixed-source "
            "T_total, strict A_top, W/Z response, matched covariance, strict g2/v, "
            "and accepted action authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current top mass-scan rows are dE/dm_bare support under the "
            "uniform additive Dirac bare-mass coordinate.  They are not dE/dh, "
            "do not include W/Z response rows, do not provide matched covariance, "
            "and do not supply strict g2/v or accepted action authority."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "top_mass_scan_subtraction_contract_applicability_audit_passed": audit_passed,
        "top_mass_scan_payload_summary": {
            "row_schema_version": top_payload.get("row_schema_version"),
            "source_coordinate": top_payload.get("source_coordinate"),
            "physical_higgs_normalization": top_payload.get("physical_higgs_normalization"),
            "used_as_physical_yukawa_readout": top_payload.get("used_as_physical_yukawa_readout"),
            "configuration_count": top_payload.get("configuration_count"),
            "row_keys": sorted(keys),
        },
        "strict_row_presence": strict_presence,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "open_imports": [
            "mixed-source total top response rows T_total",
            "strict additive-top rows A_top in the same coordinate convention",
            "production W/Z response rows",
            "matched covariance for T_total, A_top, W/Z, and g2/v",
            "strict non-observed g2 or explicit v authority",
            "accepted same-source EW/Higgs action authority",
        ],
        "exact_next_action": (
            "Use top mass-scan rows only as support for a future subtraction "
            "packet.  Do not admit the W/Z repair route until mixed-source "
            "T_total, strict A_top, W/Z response rows, matched covariance, "
            "strict g2/v, and accepted action authority are all present."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 and audit_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
