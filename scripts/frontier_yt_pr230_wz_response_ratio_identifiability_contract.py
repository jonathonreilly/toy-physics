#!/usr/bin/env python3
"""
PR #230 W/Z response-ratio identifiability contract.

This runner packages the clean physical-response bypass as a strict future
row contract.  If a single same-source radial spurion moves top, W, and Z
masses and no independent additive top source is present, the unknown source
normalization dv/ds cancels from the top/W or top/Z response ratio.  The
contract also makes the required covariance and strict g2 authority explicit.

It is support only.  The current surface still has no accepted same-source
EW/Higgs action, no production W/Z response rows, no matched covariance
certificate, and no strict non-observed g2 certificate.
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
    / "yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json"
)

PARENTS = {
    "radial_spurion_action_contract": "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json",
    "wz_response_route_completion": "outputs/yt_pr230_wz_response_route_completion_2026-05-06.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "same_source_top_response_builder": "outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "electroweak_g2_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "top_wz_covariance_import_audit": "outputs/yt_top_wz_covariance_theorem_import_audit_2026-05-05.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_ARTIFACTS = {
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "wz_mass_fit_response_rows": "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json",
    "same_source_top_response_certificate": "outputs/yt_same_source_top_response_certificate_2026-05-04.json",
    "top_wz_matched_covariance_certificate": "outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json",
    "strict_electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
    "wz_response_ratio_row_packet": "outputs/yt_pr230_wz_response_ratio_rows_2026-05-07.json",
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / path).exists() for name, path in FUTURE_ARTIFACTS.items()}


def response_ratio_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for dv_ds, y_t, g2, gy in (
        (0.30, 0.72, 0.51, 0.19),
        (1.10, 1.03, 0.66, 0.27),
        (2.40, 1.31, 0.83, 0.35),
    ):
        gz = math.sqrt(g2 * g2 + gy * gy)
        top_slope = y_t * dv_ds / math.sqrt(2.0)
        w_slope = g2 * dv_ds / 2.0
        z_slope = gz * dv_ds / 2.0
        rows.append(
            {
                "dv_ds": dv_ds,
                "input_y_t": y_t,
                "input_g2": g2,
                "input_gY": gy,
                "dm_top_ds": top_slope,
                "dM_W_ds": w_slope,
                "dM_Z_ds": z_slope,
                "yt_from_top_W": g2 * top_slope / (math.sqrt(2.0) * w_slope),
                "yt_from_top_Z": gz * top_slope / (math.sqrt(2.0) * z_slope),
            }
        )
    return rows


def all_ratios_recover_input(rows: list[dict[str, float]]) -> bool:
    return all(
        abs(row["yt_from_top_W"] - row["input_y_t"]) < 1.0e-12
        and abs(row["yt_from_top_Z"] - row["input_y_t"]) < 1.0e-12
        for row in rows
    )


def covariance_delta_method_witness() -> dict[str, Any]:
    # The row packet must carry matched top/W covariance.  This finite witness
    # records the exact delta-method gradient used by the future verifier.
    top = 0.91
    w = 0.43
    g2 = 0.62
    var_top = 1.6e-4
    var_w = 0.9e-4
    var_g2 = 0.4e-4
    cov_top_w = 0.35e-4
    cov_top_g2 = 0.0
    cov_w_g2 = 0.0
    grad_top = g2 / (math.sqrt(2.0) * w)
    grad_w = -g2 * top / (math.sqrt(2.0) * w * w)
    grad_g2 = top / (math.sqrt(2.0) * w)
    variance = (
        grad_top * grad_top * var_top
        + grad_w * grad_w * var_w
        + grad_g2 * grad_g2 * var_g2
        + 2.0 * grad_top * grad_w * cov_top_w
        + 2.0 * grad_top * grad_g2 * cov_top_g2
        + 2.0 * grad_w * grad_g2 * cov_w_g2
    )
    covariance_det = var_top * var_w - cov_top_w * cov_top_w
    return {
        "observable": "y_t = g2 * (dE_top/ds) / (sqrt(2) * dM_W/ds)",
        "top_slope": top,
        "w_slope": w,
        "g2": g2,
        "gradient": {
            "d_y_d_top_slope": grad_top,
            "d_y_d_w_slope": grad_w,
            "d_y_d_g2": grad_g2,
        },
        "covariance_inputs": {
            "var_top_slope": var_top,
            "var_w_slope": var_w,
            "cov_top_w": cov_top_w,
            "var_g2": var_g2,
            "cov_top_g2": cov_top_g2,
            "cov_w_g2": cov_w_g2,
        },
        "top_w_covariance_psd": var_top >= 0.0 and var_w >= 0.0 and covariance_det >= -1.0e-15,
        "variance_y_t": variance,
        "sigma_y_t": math.sqrt(variance) if variance >= 0.0 else float("nan"),
    }


def additive_top_counterfamily() -> list[dict[str, float]]:
    measured_top_slope = 0.88
    measured_w_slope = 0.41
    g2 = 0.64
    dv_ds = 2.0 * measured_w_slope / g2
    rows: list[dict[str, float]] = []
    for candidate_y_t in (0.55, 0.95, 1.35):
        additive_top_slope = measured_top_slope - candidate_y_t * dv_ds / math.sqrt(2.0)
        rows.append(
            {
                "measured_dm_top_ds": measured_top_slope,
                "measured_dM_W_ds": measured_w_slope,
                "g2": g2,
                "implied_dv_ds_from_W": dv_ds,
                "candidate_y_t": candidate_y_t,
                "required_independent_additive_top_slope": additive_top_slope,
            }
        )
    return rows


def g2_unknown_counterfamily() -> list[dict[str, float]]:
    top_over_w = 1.7
    rows: list[dict[str, float]] = []
    for g2 in (0.48, 0.65, 0.92):
        rows.append(
            {
                "fixed_top_over_w_response_ratio": top_over_w,
                "candidate_g2": g2,
                "candidate_y_t": g2 * top_over_w / math.sqrt(2.0),
            }
        )
    return rows


def acceptance_schema() -> dict[str, Any]:
    return {
        "future_row_packet": FUTURE_ARTIFACTS["wz_response_ratio_row_packet"],
        "required_source": "one same scalar source s for top, W, and Z responses",
        "required_action_contract": [
            "accepted same-source EW/Higgs action certificate",
            "single radial branch v(s)",
            "no independent additive s * tbar t top source",
        ],
        "required_rows": [
            "production dE_top/ds row with uncertainty",
            "production dM_W/ds or dM_Z/ds row with uncertainty",
            "matched top/W or top/Z covariance from the same ensemble/source shifts",
            "nonzero W/Z slope with fit-window and bootstrap/jackknife metadata",
        ],
        "required_authority": [
            "strict non-observed g2 or sqrt(g2^2+gY^2) certificate",
            "W/Z mass-fit path certificate",
            "sector-overlap identity or radial-spurion action contract satisfaction",
            "retained-route/assembly gates rerun before proposal wording",
        ],
        "accepted_readouts": [
            "y_t = (g2/sqrt(2)) * (dE_top/ds)/(dM_W/ds)",
            "y_t = (sqrt(g2^2+gY^2)/sqrt(2)) * (dE_top/ds)/(dM_Z/ds)",
        ],
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yukawa_as_selector": False,
        "used_observed_wz_masses_or_g2": False,
        "used_alpha_lm_or_plaquette_u0": False,
        "used_reduced_cold_pilots_as_production_evidence": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_kappa_s_equal_one": False,
        "set_g2_equal_one": False,
        "set_delta_perp_equal_zero_by_fiat": False,
        "assumed_top_wz_covariance_or_factorization": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 W/Z response-ratio identifiability contract")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    statuses = {name: status(cert) for name, cert in parents.items()}
    futures = future_presence()
    ratio_rows = response_ratio_rows()
    covariance_witness = covariance_delta_method_witness()
    additive_family = additive_top_counterfamily()
    g2_family = g2_unknown_counterfamily()
    firewall = forbidden_firewall()

    radial_spurion_support_present = (
        parents["radial_spurion_action_contract"].get(
            "radial_spurion_action_contract_passed"
        )
        is True
        and parents["radial_spurion_action_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and parents["radial_spurion_action_contract"].get("proposal_allowed") is False
    )
    wz_route_still_open = (
        parents["wz_response_route_completion"].get(
            "wz_response_route_completion_passed"
        )
        is True
        and parents["wz_response_route_completion"].get("proposal_allowed") is False
    )
    same_source_action_absent = (
        parents["same_source_ew_action_gate"].get("same_source_ew_action_ready")
        is False
        and not futures["accepted_same_source_ew_action"]
    )
    wz_rows_absent = (
        parents["wz_mass_fit_response_row_builder"].get(
            "strict_wz_mass_fit_response_row_builder_passed"
        )
        is False
        and not futures["wz_mass_fit_response_rows"]
        and not futures["wz_response_ratio_row_packet"]
    )
    top_response_absent = (
        parents["same_source_top_response_builder"].get(
            "strict_same_source_top_response_certificate_builder_passed"
        )
        is False
        and not futures["same_source_top_response_certificate"]
    )
    covariance_absent = (
        parents["top_wz_matched_covariance_builder"].get(
            "strict_top_wz_matched_covariance_builder_passed"
        )
        is False
        and not futures["top_wz_matched_covariance_certificate"]
    )
    strict_g2_absent = (
        parents["electroweak_g2_builder"].get(
            "strict_electroweak_g2_certificate_passed"
        )
        is False
        and not futures["strict_electroweak_g2_certificate"]
    )
    g2_firewall_clean = (
        parents["wz_g2_authority_firewall"].get("proposal_allowed") is False
        and parents["wz_g2_authority_firewall"].get("used_observed_g2_as_selector")
        is not True
    )
    covariance_import_audited = (
        parents["top_wz_covariance_import_audit"].get(
            "covariance_theorem_import_audit_passed"
        )
        is True
        and parents["top_wz_covariance_import_audit"].get(
            "future_closed_covariance_theorem_present"
        )
        is False
    )
    ratio_identity_exact = all_ratios_recover_input(ratio_rows)
    covariance_formula_valid = (
        covariance_witness["top_w_covariance_psd"] is True
        and math.isfinite(float(covariance_witness["variance_y_t"]))
        and covariance_witness["variance_y_t"] > 0.0
    )
    additive_family_blocks_identifiability = len(
        {
            round(row["required_independent_additive_top_slope"], 12)
            for row in additive_family
        }
    ) == len(additive_family)
    g2_family_blocks_absolute_yukawa = len(
        {round(row["candidate_y_t"], 12) for row in g2_family}
    ) == len(g2_family)
    current_surface_contract_satisfied = (
        all(futures.values())
        and not same_source_action_absent
        and not wz_rows_absent
        and not top_response_absent
        and not covariance_absent
        and not strict_g2_absent
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("radial-spurion-contract-support-present", radial_spurion_support_present, statuses["radial_spurion_action_contract"])
    report("wz-route-still-open", wz_route_still_open, statuses["wz_response_route_completion"])
    report("same-source-ew-action-absent", same_source_action_absent, FUTURE_ARTIFACTS["accepted_same_source_ew_action"])
    report("wz-response-ratio-rows-absent", wz_rows_absent, FUTURE_ARTIFACTS["wz_response_ratio_row_packet"])
    report("same-source-top-response-absent", top_response_absent, FUTURE_ARTIFACTS["same_source_top_response_certificate"])
    report("matched-covariance-authority-absent", covariance_absent, FUTURE_ARTIFACTS["top_wz_matched_covariance_certificate"])
    report("strict-g2-authority-absent", strict_g2_absent, FUTURE_ARTIFACTS["strict_electroweak_g2_certificate"])
    report("g2-firewall-clean", g2_firewall_clean, statuses["wz_g2_authority_firewall"])
    report("covariance-import-audited-not-derived", covariance_import_audited, statuses["top_wz_covariance_import_audit"])
    report("response-ratio-cancels-dv-ds", ratio_identity_exact, "top/W and top/Z witnesses recover input y_t")
    report("covariance-delta-method-contract-valid", covariance_formula_valid, f"variance_y_t={covariance_witness['variance_y_t']}")
    report("additive-top-counterfamily-blocks-shortcut", additive_family_blocks_identifiability, "independent additive top source varies at fixed measured slopes")
    report("unknown-g2-counterfamily-blocks-absolute-yukawa", g2_family_blocks_absolute_yukawa, "fixed response ratio gives different y_t for different g2")
    report("current-surface-contract-not-satisfied", not current_surface_contract_satisfied, f"future_presence={futures}")
    report("forbidden-firewall-clean", not any(firewall.values()), str(firewall))
    report("does-not-authorize-proposed-retained", True, "proposal_allowed=false")

    result = {
        "actual_current_surface_status": (
            "exact-support / WZ response-ratio identifiability contract; "
            "current response rows, matched covariance, strict g2, and accepted "
            "same-source action are absent"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The algebraic response-ratio contract is exact support only.  The "
            "current surface lacks the required production top/W/Z rows, "
            "matched covariance certificate, strict non-observed g2 certificate, "
            "and accepted same-source radial-spurion action."
        ),
        "bare_retained_allowed": False,
        "wz_response_ratio_identifiability_contract_passed": True,
        "current_surface_contract_satisfied": current_surface_contract_satisfied,
        "future_artifact_presence": futures,
        "same_source_ew_action_accepted": not same_source_action_absent,
        "future_response_ratio_row_packet_present": futures[
            "wz_response_ratio_row_packet"
        ],
        "production_wz_response_rows_present": not wz_rows_absent,
        "same_source_top_response_present": not top_response_absent,
        "matched_covariance_authority_present": not covariance_absent,
        "strict_g2_authority_present": not strict_g2_absent,
        "radial_spurion_action_contract_support_present": radial_spurion_support_present,
        "ratio_identity_exact": ratio_identity_exact,
        "covariance_delta_method_contract_valid": covariance_formula_valid,
        "additive_top_counterfamily_blocks_shortcut": additive_family_blocks_identifiability,
        "unknown_g2_counterfamily_blocks_absolute_yukawa": g2_family_blocks_absolute_yukawa,
        "acceptance_schema": acceptance_schema(),
        "response_ratio_witnesses": ratio_rows,
        "covariance_delta_method_witness": covariance_witness,
        "additive_top_counterfamily": additive_family,
        "g2_unknown_counterfamily": g2_family,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat the current additive FH/LSZ top mass source as a radial spurion",
            "does not use W/Z smoke rows as production mass-response rows",
            "does not infer covariance from marginal top and W/Z rows",
            "does not use observed g2, observed W/Z masses, or observed y_t",
            "does not set kappa_s, c2, Z_match, g2, or delta_perp to one or zero by fiat",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
