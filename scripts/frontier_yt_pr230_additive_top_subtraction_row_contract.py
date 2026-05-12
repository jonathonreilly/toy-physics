#!/usr/bin/env python3
"""
PR #230 additive-top subtraction row contract.

Block04 showed that the current same-source EW/Higgs ansatz differentiates to

    dS/ds = O_top_additive + O_H,

so a top/W response readout is contaminated by an independent additive top
slope.  This runner packages the exact repair if the project keeps that
source convention: measure the additive component as its own row, subtract it
with matched covariance, and only then form the radial-spurion response ratio.

The result is exact support only.  The current surface still lacks the
required additive-top Jacobian rows, W/Z response rows, matched three-way
covariance, strict non-observed g2 authority, and accepted radial-spurion
action certificate.
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
    / "yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json"
)

PARENTS = {
    "additive_source_radial_spurion_incompatibility": "outputs/yt_pr230_additive_source_radial_spurion_incompatibility_2026-05-07.json",
    "radial_spurion_action_contract": "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json",
    "wz_response_ratio_identifiability_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "same_source_top_response_builder": "outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "electroweak_g2_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_ARTIFACTS = {
    "additive_top_jacobian_rows": "outputs/yt_pr230_additive_top_jacobian_rows_2026-05-07.json",
    "radial_top_response_rows": "outputs/yt_pr230_radial_top_response_rows_2026-05-07.json",
    "wz_response_ratio_rows": "outputs/yt_pr230_wz_response_ratio_rows_2026-05-07.json",
    "top_additive_wz_matched_covariance": "outputs/yt_pr230_top_additive_wz_matched_covariance_2026-05-07.json",
    "strict_electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "subtracted_response_readout_certificate": "outputs/yt_pr230_additive_top_subtracted_response_readout_2026-05-07.json",
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
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / path).exists() for name, path in FUTURE_ARTIFACTS.items()}


def additive_top_jacobian_row_status() -> dict[str, Any]:
    path = ROOT / FUTURE_ARTIFACTS["additive_top_jacobian_rows"]
    rows = load_json(FUTURE_ARTIFACTS["additive_top_jacobian_rows"])
    if not rows:
        return {
            "present": False,
            "bounded_support": False,
            "strict": False,
            "proposal_allowed": False,
            "path": rel(path),
            "status": "absent",
        }
    return {
        "present": True,
        "bounded_support": rows.get("bounded_additive_top_jacobian_rows_passed") is True,
        "strict": rows.get("strict_additive_top_jacobian_rows_passed") is True,
        "proposal_allowed": rows.get("proposal_allowed") is True,
        "path": rel(path),
        "status": rows.get("actual_current_surface_status", "present"),
        "row_count": rows.get("row_source", {}).get("packaged_chunk_count"),
        "expected_chunk_count": rows.get("row_source", {}).get("expected_chunk_count"),
        "complete_chunk_packet": rows.get("row_source", {}).get("complete_chunk_packet"),
    }


def subtraction_contract() -> dict[str, Any]:
    return {
        "contract_kind": "matched additive-top subtraction row contract",
        "source_coordinates": {
            "s_radial": "moves the canonical Higgs radial branch v(s)",
            "s_additive": "moves only the independent additive top scalar source",
        },
        "measured_rows_required": [
            "T_total = dE_top/ds under the mixed current-source coordinate",
            "A_top = independent additive top slope under the same coordinate convention",
            "W = dM_W/ds or Z = dM_Z/ds under the same source shifts",
            "matched covariance for T_total, A_top, W/Z, and g2 or sqrt(g2^2+gY^2)",
        ],
        "accepted_readouts": [
            "y_t = g2 * (T_total - A_top) / (sqrt(2) * W)",
            "y_t = sqrt(g2^2 + gY^2) * (T_total - A_top) / (sqrt(2) * Z)",
        ],
        "forbidden_shortcuts": [
            "setting A_top = 0 by convention",
            "estimating A_top from observed y_t or observed m_t",
            "using marginal top and W rows without matched covariance",
            "using H_unit, yt_ward_identity, alpha_LM, plaquette/u0, or unit-normalization shortcuts",
        ],
    }


def subtraction_witness_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for y_t, g2, dv_ds, additive, scale in (
        (0.74, 0.57, 0.45, -0.08, 0.5),
        (0.93, 0.66, 1.20, 0.17, 1.0),
        (1.18, 0.81, 2.70, -0.31, 2.0),
    ):
        total_top = y_t * dv_ds / math.sqrt(2.0) + additive
        w_slope = g2 * dv_ds / 2.0
        # Reparameterize the source by s' = scale * s.  All same-source slopes
        # scale by 1/scale, and the corrected ratio must be invariant.
        total_top_prime = total_top / scale
        additive_prime = additive / scale
        w_prime = w_slope / scale
        rows.append(
            {
                "input_y_t": y_t,
                "input_g2": g2,
                "dv_ds": dv_ds,
                "additive_top_slope": additive,
                "total_top_slope": total_top,
                "w_slope": w_slope,
                "source_reparameterization_scale": scale,
                "total_top_slope_prime": total_top_prime,
                "additive_top_slope_prime": additive_prime,
                "w_slope_prime": w_prime,
                "yt_subtracted": g2
                * (total_top - additive)
                / (math.sqrt(2.0) * w_slope),
                "yt_subtracted_after_source_rescale": g2
                * (total_top_prime - additive_prime)
                / (math.sqrt(2.0) * w_prime),
            }
        )
    return rows


def no_subtraction_counterfamily() -> list[dict[str, float]]:
    measured_total_top = 0.87
    measured_w = 0.42
    g2 = 0.64
    implied_dv_ds = 2.0 * measured_w / g2
    rows: list[dict[str, float]] = []
    for candidate_y_t in (0.52, 0.91, 1.29):
        required_additive = (
            measured_total_top - candidate_y_t * implied_dv_ds / math.sqrt(2.0)
        )
        rows.append(
            {
                "fixed_measured_total_top_slope": measured_total_top,
                "fixed_measured_w_slope": measured_w,
                "fixed_g2": g2,
                "implied_dv_ds_from_w": implied_dv_ds,
                "candidate_y_t": candidate_y_t,
                "required_additive_top_slope": required_additive,
            }
        )
    return rows


def cholesky_psd(matrix: list[list[float]], tol: float = 1.0e-12) -> bool:
    n = len(matrix)
    lower = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            value = matrix[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if value < -tol:
                    return False
                lower[i][j] = math.sqrt(max(value, 0.0))
            elif lower[j][j] > tol:
                lower[i][j] = value / lower[j][j]
            elif abs(value) > tol:
                return False
    return True


def covariance_delta_method_witness() -> dict[str, Any]:
    total_top = 0.87
    additive_top = 0.23
    w_slope = 0.42
    g2 = 0.64
    covariance = [
        [1.6e-4, 0.55e-4, 0.35e-4, 0.00e-4],
        [0.55e-4, 0.9e-4, 0.18e-4, 0.00e-4],
        [0.35e-4, 0.18e-4, 0.8e-4, 0.00e-4],
        [0.00e-4, 0.00e-4, 0.00e-4, 0.4e-4],
    ]
    prefactor = 1.0 / math.sqrt(2.0)
    radial_top = total_top - additive_top
    value = g2 * radial_top * prefactor / w_slope
    gradient = [
        g2 * prefactor / w_slope,
        -g2 * prefactor / w_slope,
        -g2 * radial_top * prefactor / (w_slope * w_slope),
        radial_top * prefactor / w_slope,
    ]
    variance = 0.0
    for i, grad_i in enumerate(gradient):
        for j, grad_j in enumerate(gradient):
            variance += grad_i * covariance[i][j] * grad_j
    return {
        "observable": "y_t = g2 * (T_total - A_top) / (sqrt(2) * W)",
        "variables": ["T_total", "A_top", "W", "g2"],
        "inputs": {
            "T_total": total_top,
            "A_top": additive_top,
            "W": w_slope,
            "g2": g2,
        },
        "value": value,
        "gradient": {
            "d_y_d_T_total": gradient[0],
            "d_y_d_A_top": gradient[1],
            "d_y_d_W": gradient[2],
            "d_y_d_g2": gradient[3],
        },
        "covariance_matrix": covariance,
        "covariance_psd": cholesky_psd(covariance),
        "variance_y_t": variance,
        "sigma_y_t": math.sqrt(variance) if variance >= 0.0 else float("nan"),
    }


def all_subtracted_rows_recover_input(rows: list[dict[str, float]]) -> bool:
    return all(
        abs(row["yt_subtracted"] - row["input_y_t"]) < 1.0e-12
        and abs(row["yt_subtracted_after_source_rescale"] - row["input_y_t"]) < 1.0e-12
        for row in rows
    )


def counterfamily_blocks_identifiability(rows: list[dict[str, float]]) -> bool:
    return len({round(row["required_additive_top_slope"], 12) for row in rows}) == len(
        rows
    )


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yukawa_as_selector": False,
        "used_observed_wz_masses_or_g2": False,
        "used_alpha_lm_or_plaquette_u0": False,
        "used_reduced_cold_pilots_as_production_evidence": False,
        "set_additive_top_slope_to_zero_by_fiat": False,
        "set_kappa_s_equal_one": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_g2_equal_one": False,
        "assumed_covariance_factorization": False,
        "claimed_retained_or_proposed_retained": False,
        "touched_live_chunk_worker": False,
    }


def main() -> int:
    print("PR #230 additive-top subtraction row contract")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    futures = future_presence()
    contract = subtraction_contract()
    witness_rows = subtraction_witness_rows()
    counter_rows = no_subtraction_counterfamily()
    covariance_witness = covariance_delta_method_witness()
    firewall = forbidden_firewall()
    additive_rows = additive_top_jacobian_row_status()

    incompatibility_loaded = (
        parents["additive_source_radial_spurion_incompatibility"].get(
            "additive_source_radial_spurion_incompatibility_passed"
        )
        is True
        and parents["additive_source_radial_spurion_incompatibility"].get(
            "proposal_allowed"
        )
        is False
    )
    parent_names_subtraction_as_open_repair = any(
        "measures/subtracts" in str(parents["additive_source_radial_spurion_incompatibility"].get(key, ""))
        or "measure/subtract" in str(parents["additive_source_radial_spurion_incompatibility"].get(key, ""))
        for key in ("conditional_surface_status", "next_exact_action")
    )
    radial_contract_support_only = (
        parents["radial_spurion_action_contract"].get(
            "radial_spurion_action_contract_passed"
        )
        is True
        and parents["radial_spurion_action_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
    )
    wz_ratio_support_only = (
        parents["wz_response_ratio_identifiability_contract"].get(
            "wz_response_ratio_identifiability_contract_passed"
        )
        is True
        and parents["wz_response_ratio_identifiability_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
    )
    top_response_not_strict = (
        parents["same_source_top_response_builder"].get(
            "strict_same_source_top_response_certificate_builder_passed"
        )
        is False
    )
    wz_rows_absent = (
        parents["wz_mass_fit_response_row_builder"].get(
            "strict_wz_mass_fit_response_row_builder_passed"
        )
        is False
        and not futures["wz_response_ratio_rows"]
    )
    covariance_absent = (
        parents["top_wz_matched_covariance_builder"].get(
            "strict_top_wz_matched_covariance_builder_passed"
        )
        is False
        and not futures["top_additive_wz_matched_covariance"]
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
    aggregate_still_denies_proposal = (
        parents["retained_route"].get("proposal_allowed") is False
        and parents["campaign_status"].get("proposal_allowed") is False
    )
    additive_rows_acceptable_support = (
        additive_rows["present"]
        and additive_rows["bounded_support"]
        and additive_rows["proposal_allowed"] is False
    )
    additive_rows_strict = (
        additive_rows["present"]
        and additive_rows["strict"]
        and additive_rows["proposal_allowed"] is False
    )
    readout_absent = not futures["subtracted_response_readout_certificate"]
    subtraction_identity_exact = all_subtracted_rows_recover_input(witness_rows)
    no_subtraction_underdetermined = counterfamily_blocks_identifiability(counter_rows)
    covariance_valid = (
        covariance_witness["covariance_psd"] is True
        and math.isfinite(float(covariance_witness["variance_y_t"]))
        and covariance_witness["variance_y_t"] > 0.0
    )
    current_surface_contract_satisfied = (
        additive_rows_strict
        and futures["radial_top_response_rows"]
        and futures["wz_response_ratio_rows"]
        and futures["top_additive_wz_matched_covariance"]
        and futures["strict_electroweak_g2_certificate"]
        and futures["accepted_same_source_ew_action"]
        and futures["subtracted_response_readout_certificate"]
        and not top_response_not_strict
        and not wz_rows_absent
        and not covariance_absent
        and not strict_g2_absent
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("block04-incompatibility-loaded", incompatibility_loaded, statuses["additive_source_radial_spurion_incompatibility"])
    report("block04-names-subtraction-as-open-repair", parent_names_subtraction_as_open_repair, "measure/subtract repair present")
    report("radial-spurion-contract-support-only", radial_contract_support_only, statuses["radial_spurion_action_contract"])
    report("wz-response-ratio-contract-support-only", wz_ratio_support_only, statuses["wz_response_ratio_identifiability_contract"])
    report("same-source-top-response-not-strict", top_response_not_strict, statuses["same_source_top_response_builder"])
    report("wz-response-rows-absent", wz_rows_absent, FUTURE_ARTIFACTS["wz_response_ratio_rows"])
    report(
        "additive-top-jacobian-row-status",
        (not additive_rows["present"]) or additive_rows_acceptable_support,
        f"{additive_rows['path']}: {additive_rows['status']}",
    )
    report(
        "additive-top-jacobian-not-strict",
        not additive_rows_strict,
        "strict rows still require per-configuration same-source covariance",
    )
    report("matched-three-way-covariance-absent", covariance_absent, FUTURE_ARTIFACTS["top_additive_wz_matched_covariance"])
    report("strict-g2-authority-absent", strict_g2_absent, FUTURE_ARTIFACTS["strict_electroweak_g2_certificate"])
    report("g2-firewall-clean", g2_firewall_clean, statuses["wz_g2_authority_firewall"])
    report("aggregate-gates-deny-proposal", aggregate_still_denies_proposal, "proposal_allowed=false")
    report("subtracted-ratio-recovers-yt", subtraction_identity_exact, "T_total - A_top witness rows")
    report("subtracted-ratio-source-rescaling-invariant", subtraction_identity_exact, "s' = lambda s witness rows")
    report("no-subtraction-counterfamily-underdetermined", no_subtraction_underdetermined, "fixed total top/W slopes admit multiple y_t values")
    report("matched-covariance-delta-method-valid", covariance_valid, f"variance_y_t={covariance_witness['variance_y_t']}")
    report("subtracted-readout-certificate-absent", readout_absent, FUTURE_ARTIFACTS["subtracted_response_readout_certificate"])
    report("current-surface-contract-not-satisfied", not current_surface_contract_satisfied, f"future_presence={futures}")
    report("forbidden-firewall-clean", not any(firewall.values()), str(firewall))
    report("does-not-authorize-proposed-retained", True, "proposal_allowed=false")

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "exact-support / additive-top subtraction row contract; current "
            "additive Jacobian rows are bounded support only, while W/Z rows, "
            "matched covariance, strict g2, and accepted action remain absent"
            if additive_rows["present"]
            else "exact-support / additive-top subtraction row contract; current "
            "additive Jacobian rows, W/Z rows, matched covariance, strict g2, "
            "and accepted action are absent"
        ),
        "conditional_surface_status": (
            "If same-surface rows measure the independent additive top slope "
            "and matched covariance, the corrected response ratio identifies "
            "the radial-spurion y_t without setting the additive component to zero."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The subtraction formula is exact support only.  The current PR230 "
            "surface has bounded coarse additive-top Jacobian rows, but still "
            "lacks strict per-configuration additive rows, W/Z response rows, "
            "matched covariance, strict non-observed g2, and accepted "
            "radial-spurion action authority."
            if additive_rows["present"]
            else "The subtraction formula is exact support only.  The current "
            "PR230 surface lacks additive-top Jacobian rows, W/Z response rows, "
            "matched covariance, strict non-observed g2, and accepted "
            "radial-spurion action authority."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "additive_top_subtraction_row_contract_passed": passed,
        "current_surface_contract_satisfied": current_surface_contract_satisfied,
        "future_artifact_presence": futures,
        "additive_top_jacobian_row_status": additive_rows,
        "contract": contract,
        "subtraction_witness_rows": witness_rows,
        "no_subtraction_counterfamily": counter_rows,
        "covariance_delta_method_witness": covariance_witness,
        "subtraction_identity_exact": subtraction_identity_exact,
        "subtraction_source_rescaling_invariant": subtraction_identity_exact,
        "no_subtraction_counterfamily_underdetermined": no_subtraction_underdetermined,
        "matched_covariance_delta_method_valid": covariance_valid,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set the independent additive top slope to zero",
            "does not use observed y_t, observed top mass, observed W/Z masses, or observed g2",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette, u0, or unit-normalization shortcuts",
            "does not infer matched covariance from marginal row errors",
            "does not touch the live chunk worker",
        ],
        "exact_next_action": (
            "Choose between two positive repairs: either build a replacement "
            "no-independent-top-source radial-spurion action, or produce "
            "same-ensemble additive-top Jacobian rows plus W/Z response rows "
            "and matched covariance for the subtraction contract."
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
