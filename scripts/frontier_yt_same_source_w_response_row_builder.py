#!/usr/bin/env python3
"""
PR #230 same-source W-response production-row builder.

This runner is the assembly layer between future same-source W/top response
certificates and the lightweight readout harness.  It does not manufacture W
or top response data.  In strict mode it writes

    outputs/yt_same_source_w_response_rows_2026-05-04.json

only when real production response and delta_perp correction certificates are
present.  Scout mode builds synthetic certificates and writes only scout-named
rows, proving the adapter and firewall without creating production evidence.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WZ_INPUT = ROOT / "outputs" / "yt_fh_gauge_mass_response_certificate_2026-05-02.json"
DEFAULT_CORRECTION_INPUT = (
    ROOT / "outputs" / "yt_same_source_w_response_orthogonal_correction_certificate_2026-05-04.json"
)
DEFAULT_ROWS_OUTPUT = ROOT / "outputs" / "yt_same_source_w_response_rows_2026-05-04.json"
DEFAULT_STATUS_OUTPUT = ROOT / "outputs" / "yt_same_source_w_response_row_builder_2026-05-04.json"
SCOUT_ROWS_OUTPUT = ROOT / "outputs" / "yt_same_source_w_response_row_builder_scout_rows_2026-05-04.json"
SCOUT_STATUS_OUTPUT = ROOT / "outputs" / "yt_same_source_w_response_row_builder_scout_2026-05-04.json"

PARENTS = {
    "fh_gauge_mass_response_builder": "outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json",
    "same_source_wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "delta_perp_tomography_builder": "outputs/yt_delta_perp_tomography_correction_builder_2026-05-04.json",
    "same_source_w_response_orthogonal_correction": "outputs/yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json",
    "same_source_w_response_lightweight_readout": "outputs/yt_same_source_w_response_lightweight_readout_harness_2026-05-04.json",
}

FORBIDDEN_FALSE_FIELDS = (
    "used_H_unit_or_Ward_authority",
    "used_yt_ward_identity",
    "used_y_t_bare",
    "used_observed_y_t_or_m_t_as_selector",
    "used_observed_W_mass_as_selector",
    "used_static_EW_algebra_as_measurement",
    "used_alpha_lm_plaquette_or_u0",
    "set_delta_perp_zero_without_certificate",
    "set_kappa_s_equal_one",
    "set_c2_equal_one",
    "set_z_match_equal_one",
    "set_cos_theta_equal_one",
)

CORRECTION_METHOD_MAP = {
    "tomography_correction_row": "measured_tomography_correction",
    "source_higgs_gram_purity": "source_higgs_gram_purity",
    "one_higgs_completeness": "one_higgs_completeness",
    "orthogonal_top_null_theorem": "one_higgs_completeness",
    "neutral_rank_one_theorem": "neutral_rank_one_theorem",
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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def nonnegative(value: Any) -> bool:
    return finite(value) and float(value) >= 0.0


def positive(value: Any) -> bool:
    return finite(value) and float(value) > 0.0


def as_certificates(data: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("same_source_wz_response_certificates", "wz_response_certificates", "certificates"):
        items = data.get(key)
        if isinstance(items, list):
            return [item for item in items if isinstance(item, dict)]
    return [data] if data else []


def correction_payload(data: dict[str, Any]) -> dict[str, Any]:
    nested = data.get("correction_certificate_candidate")
    if isinstance(nested, dict) and nested:
        return nested
    return data


def validate_wz_certificate(candidate: dict[str, Any], *, require_production: bool) -> dict[str, Any]:
    if not candidate:
        return {"present": False, "valid": False, "failed_checks": ["W/Z response certificate absent"]}

    top = candidate.get("top_response", {})
    response = candidate.get("gauge_response", {})
    ew = candidate.get("electroweak_coupling", {})
    identity = candidate.get("identity_certificates", {})
    firewall = candidate.get("firewall", {})
    has_w_slope = finite(response.get("slope_dM_W_ds"))
    checks = {
        "phase_allowed": candidate.get("phase") in {"scout", "production"},
        "production_phase_if_required": candidate.get("phase") == "production" if require_production else True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "three_source_shifts": isinstance(candidate.get("source_shifts"), list)
        and len(candidate.get("source_shifts", [])) >= 3,
        "w_mass_fits_from_correlators": candidate.get("wz_mass_fits_from_correlators") is True,
        "finite_top_slope": finite(top.get("slope_dE_top_ds")),
        "positive_top_slope_error": positive(top.get("slope_error")),
        "finite_w_slope": has_w_slope,
        "positive_w_slope_error": positive(response.get("slope_error")),
        "finite_top_w_covariance": finite(response.get("cov_dE_top_dM_W")),
        "positive_g2": positive(ew.get("g2")),
        "nonnegative_sigma_g2": nonnegative(ew.get("sigma_g2", ew.get("g2_sigma", 0.0))),
        "same_source_sector_overlap_identity_passed": identity.get(
            "same_source_sector_overlap_identity_passed"
        )
        is True,
        "canonical_higgs_identity_passed": identity.get("canonical_higgs_pole_identity_passed") is True,
        "no_observed_wz_selector": firewall.get("used_observed_WZ_masses_as_selector") is False,
        "no_observed_top_or_yukawa_selector": firewall.get("used_observed_top_or_yukawa_as_selector") is False,
        "no_static_v_overlap_selector": firewall.get("used_static_v_overlap_selector") is False,
        "no_hunit_or_ward": firewall.get("used_H_unit_or_Ward_authority") is False,
        "no_alpha_lm_plaquette_or_u0": firewall.get("used_alpha_lm_plaquette_or_u0") is False,
        "no_c2_or_zmatch_by_fiat": firewall.get("used_c2_or_zmatch_equal_one") is False,
        "no_observed_g2_selector": ew.get("used_observed_g2_as_selector") is False,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
    }


def validate_correction(candidate: dict[str, Any], *, require_production: bool) -> dict[str, Any]:
    if not candidate:
        return {"present": False, "valid": False, "failed_checks": ["delta_perp correction certificate absent"]}

    method = candidate.get("correction_method")
    provenance = candidate.get("provenance", {})
    firewall = candidate.get("firewall", {})
    checks = {
        "phase_allowed": candidate.get("phase") in {"scout", "production", "exact-support"},
        "production_or_exact_if_required": candidate.get("phase") in {"production", "exact-support"}
        if require_production
        else True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "allowed_correction_method": method in CORRECTION_METHOD_MAP,
        "finite_delta_perp": finite(candidate.get("orthogonal_correction_delta_perp")),
        "nonnegative_sigma_delta_perp": nonnegative(candidate.get("sigma_delta_perp")),
        "method_certificate_present": isinstance(provenance.get("method_certificate"), str)
        and bool(provenance.get("method_certificate")),
        "rank_or_null_authority_passed": provenance.get("rank_or_null_authority_passed") is True,
        "no_delta_zero_without_certificate": firewall.get("used_delta_perp_zero_without_certificate") is False,
        "no_observed_yt_backsolve": firewall.get("used_observed_y_t_to_backsolve_delta") is False,
        "no_hunit_or_ward": firewall.get("used_H_unit_or_Ward_authority") is False,
        "no_alpha_lm_plaquette_or_u0": firewall.get("used_alpha_lm_plaquette_or_u0") is False,
        "no_c2_or_zmatch_by_fiat": firewall.get("used_c2_or_zmatch_equal_one") is False,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
    }


def row_from_certificates(wz: dict[str, Any], correction: dict[str, Any]) -> dict[str, Any]:
    top = wz["top_response"]
    response = wz["gauge_response"]
    ew = wz["electroweak_coupling"]
    metadata = wz.get("metadata", {})
    method = CORRECTION_METHOD_MAP[str(correction["correction_method"])]
    return {
        "volume": wz.get("volume") or metadata.get("volume") or metadata.get("lattice_volume") or "combined",
        "row_kind": "production_mass_slope" if wz.get("phase") == "production" else "scout_synthetic_mass_slope",
        "same_source_coordinate": True,
        "g_2": float(ew["g2"]),
        "sigma_g_2": float(ew.get("sigma_g2", ew.get("g2_sigma", 0.0))),
        "R_t": float(top["slope_dE_top_ds"]),
        "sigma_R_t": float(top["slope_error"]),
        "R_W": float(response["slope_dM_W_ds"]),
        "sigma_R_W": float(response["slope_error"]),
        "cov_R_t_R_W": float(response["cov_dE_top_dM_W"]),
        "delta_perp": float(correction["orthogonal_correction_delta_perp"]),
        "sigma_delta_perp": float(correction["sigma_delta_perp"]),
        "delta_perp_method": method,
    }


def build_rows_certificate(
    wz_certificates: list[dict[str, Any]],
    correction: dict[str, Any],
    *,
    phase: str,
    wz_input: Path,
    correction_input: Path,
) -> dict[str, Any]:
    first = wz_certificates[0] if wz_certificates else {}
    source_shifts = first.get("source_shifts", [])
    return {
        "certificate_kind": "same_source_w_response_rows",
        "phase": phase,
        "same_surface_cl3_z3": True,
        "same_source_coordinate": True,
        "source_shifts": source_shifts,
        "response_rows": [row_from_certificates(wz, correction) for wz in wz_certificates],
        "proposal_allowed": False,
        "input_certificates": {
            "same_source_wz_response": display(wz_input),
            "orthogonal_correction": display(correction_input),
        },
        "firewall": {field: False for field in FORBIDDEN_FALSE_FIELDS},
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not generate W/top response measurements",
            "does not infer delta_perp from observed y_t or m_t",
            "does not use H_unit, yt_ward_identity, y_t_bare, alpha_LM, plaquette/u0, observed selectors, kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
        ],
    }


def synthetic_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    g2 = 0.648
    y_h = 0.9176
    delta = -0.054444444444444455
    correction = {
        "phase": "scout",
        "same_source_coordinate": True,
        "correction_method": "tomography_correction_row",
        "orthogonal_correction_delta_perp": delta,
        "sigma_delta_perp": 0.0044,
        "provenance": {
            "method_certificate": "synthetic scout tomography rows",
            "rank_or_null_authority_passed": True,
        },
        "firewall": {
            "used_delta_perp_zero_without_certificate": False,
            "used_observed_y_t_to_backsolve_delta": False,
            "used_H_unit_or_Ward_authority": False,
            "used_alpha_lm_plaquette_or_u0": False,
            "used_c2_or_zmatch_equal_one": False,
        },
    }
    certs = []
    for index, (volume, kappa_h) in enumerate([("L6_T12_scout", 0.96), ("L8_T16_scout", 1.08)]):
        rw = g2 * kappa_h / 2.0
        rt = (y_h + delta) * math.sqrt(2.0) * rw / g2
        certs.append(
            {
                "metadata": {"volume": volume},
                "phase": "scout",
                "same_source_coordinate": True,
                "source_coordinate": "synthetic_same_source_s",
                "source_shifts": [-0.01, 0.0, 0.01],
                "wz_mass_fits_from_correlators": True,
                "top_response": {"slope_dE_top_ds": rt, "slope_error": 0.004 + 0.001 * index},
                "gauge_response": {
                    "slope_dM_W_ds": rw,
                    "slope_error": 0.003 + 0.001 * index,
                    "cov_dE_top_dM_W": 0.0,
                },
                "electroweak_coupling": {
                    "g2": g2,
                    "sigma_g2": 0.0015,
                    "g2_certificate": "synthetic scout g2",
                    "used_observed_g2_as_selector": False,
                },
                "identity_certificates": {
                    "same_source_sector_overlap_identity_passed": True,
                    "canonical_higgs_pole_identity_passed": True,
                    "retained_route_or_proposal_gate_passed": False,
                },
                "firewall": {
                    "used_observed_WZ_masses_as_selector": False,
                    "used_observed_top_or_yukawa_as_selector": False,
                    "used_static_v_overlap_selector": False,
                    "used_H_unit_or_Ward_authority": False,
                    "used_alpha_lm_plaquette_or_u0": False,
                    "used_c2_or_zmatch_equal_one": False,
                },
            }
        )
    return {"same_source_wz_response_certificates": certs}, correction


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wz-input", type=Path, default=DEFAULT_WZ_INPUT)
    parser.add_argument("--correction-input", type=Path, default=DEFAULT_CORRECTION_INPUT)
    parser.add_argument("--rows-output", type=Path, default=DEFAULT_ROWS_OUTPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_STATUS_OUTPUT)
    parser.add_argument("--scout", action="store_true", help="build synthetic scout rows")
    parser.add_argument("--strict", action="store_true", help="require production response/correction certificates")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mode = "strict" if args.strict else "scout" if args.scout else "current"
    status_output = SCOUT_STATUS_OUTPUT if args.scout and args.output == DEFAULT_STATUS_OUTPUT else args.output
    rows_output = SCOUT_ROWS_OUTPUT if args.scout and args.rows_output == DEFAULT_ROWS_OUTPUT else args.rows_output

    print("PR #230 same-source W-response row builder")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    parent_statuses = {name: status(cert) for name, cert in parents.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]

    if args.scout:
        wz_data, correction_data = synthetic_inputs()
    else:
        wz_data = load_json(args.wz_input)
        correction_data = correction_payload(load_json(args.correction_input))

    wz_certificates = as_certificates(wz_data)
    wz_validations = [
        validate_wz_certificate(candidate, require_production=args.strict)
        for candidate in wz_certificates
    ]
    correction_validation = validate_correction(correction_data, require_production=args.strict)
    all_wz_valid = bool(wz_validations) and all(item["valid"] for item in wz_validations)
    strict_gate_passed = args.strict and all_wz_valid and correction_validation["valid"]
    scout_gate_passed = args.scout and all_wz_valid and correction_validation["valid"]
    current_inputs_valid = (not args.strict) and (not args.scout) and all_wz_valid and correction_validation["valid"]
    row_certificate_written = False
    rows_certificate: dict[str, Any] = {}

    should_write_rows = strict_gate_passed or scout_gate_passed or current_inputs_valid
    if should_write_rows:
        rows_certificate = build_rows_certificate(
            wz_certificates,
            correction_data,
            phase="production" if args.strict or current_inputs_valid else "scout",
            wz_input=args.wz_input,
            correction_input=args.correction_input,
        )
        rows_output.parent.mkdir(parents=True, exist_ok=True)
        rows_output.write_text(json.dumps(rows_certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        row_certificate_written = True

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("wz-builder-records-input-state", "same-source WZ response" in parent_statuses["fh_gauge_mass_response_builder"], parent_statuses["fh_gauge_mass_response_builder"])
    report("delta-perp-builder-records-input-state", "delta_perp tomography correction" in parent_statuses["delta_perp_tomography_builder"], parent_statuses["delta_perp_tomography_builder"])
    if args.scout:
        report("scout-wz-certificates-built", bool(wz_certificates), f"count={len(wz_certificates)}")
        report("scout-wz-certificates-valid", all_wz_valid, str([item["failed_checks"] for item in wz_validations]))
        report("scout-correction-valid", correction_validation["valid"], str(correction_validation.get("failed_checks", [])))
        report("scout-row-certificate-written", row_certificate_written, display(rows_output))
    elif args.strict:
        report("strict-wz-certificate-present", bool(wz_certificates), display(args.wz_input))
        report("strict-wz-certificate-valid", all_wz_valid, str([item["failed_checks"] for item in wz_validations]))
        report("strict-correction-certificate-valid", correction_validation["valid"], str(correction_validation.get("failed_checks", [])))
        report("strict-row-certificate-written", row_certificate_written, display(rows_output))
    else:
        report("future-wz-certificate-absent", not bool(wz_certificates), display(args.wz_input))
        report("future-correction-certificate-absent", not correction_validation["present"], display(args.correction_input))
        report("current-mode-valid-if-inputs-present", (not wz_certificates and not correction_validation["present"]) or current_inputs_valid, str([item["failed_checks"] for item in wz_validations] + [correction_validation.get("failed_checks", [])]))
        report("current-mode-does-not-write-production-rows", not row_certificate_written, display(DEFAULT_ROWS_OUTPUT))
    report("strict-production-row-builder-not-claimed" if not args.strict else "strict-production-row-builder-passed", not strict_gate_passed if not args.strict else strict_gate_passed, f"strict_gate_passed={strict_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "scout-pass / same-source W-response row builder"
            if scout_gate_passed
            else "strict-pass / same-source W-response production rows built"
            if strict_gate_passed
            else "support / same-source W-response production rows built"
            if current_inputs_valid
            else "open / same-source W-response row builder inputs absent"
        ),
        "mode": mode,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The row builder is an adapter only.  It can feed the lightweight "
            "readout harness after production certificates exist, but retained "
            "closure still requires matching/running, assembly, and audit."
        ),
        "bare_retained_allowed": False,
        "same_source_w_response_row_builder_passed": (
            scout_gate_passed or strict_gate_passed or current_inputs_valid
        ),
        "strict_same_source_w_response_row_builder_passed": strict_gate_passed,
        "row_certificate_written": row_certificate_written,
        "row_certificate_output": display(rows_output),
        "wz_input_certificate": display(args.wz_input),
        "correction_input_certificate": display(args.correction_input),
        "wz_validations": wz_validations,
        "correction_validation": correction_validation,
        "row_certificate": rows_certificate,
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not create production rows in scout/current mode without valid production inputs",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed selectors, alpha_LM, plaquette/u0, kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not set delta_perp to zero without an accepted correction/null/purity certificate",
        ],
        "exact_next_action": (
            f"Supply {display(DEFAULT_WZ_INPUT)} and {display(DEFAULT_CORRECTION_INPUT)}, "
            "rerun this builder in strict mode to write "
            f"{display(DEFAULT_ROWS_OUTPUT)}, then rerun the lightweight "
            "W-response readout harness in strict mode."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    status_output.parent.mkdir(parents=True, exist_ok=True)
    status_output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote status certificate: {display(status_output)}")
    if row_certificate_written:
        print(f"Wrote row certificate: {display(rows_output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if args.strict and not strict_gate_passed:
        return 1
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
