#!/usr/bin/env python3
"""
PR #230 same-source top-response certificate builder.

The W/Z response adapter needs a matched top-response certificate, not just a
source-only support slope.  This runner wraps the existing production-grade
FH/LSZ common-window top response only after future identity and matched
top/W covariance certificates validate.  It does not claim that the current
source response is physical y_t evidence.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE_INPUT = ROOT / "outputs" / "yt_fh_lsz_common_window_response_gate_2026-05-04.json"
DEFAULT_POOLED_INPUT = ROOT / "outputs" / "yt_fh_lsz_common_window_pooled_response_estimator_2026-05-04.json"
DEFAULT_IDENTITY_INPUT = ROOT / "outputs" / "yt_same_source_top_response_identity_certificate_2026-05-04.json"
DEFAULT_COVARIANCE_INPUT = ROOT / "outputs" / "yt_top_wz_matched_covariance_certificate_2026-05-04.json"
DEFAULT_TOP_RESPONSE_OUTPUT = ROOT / "outputs" / "yt_same_source_top_response_certificate_2026-05-04.json"
DEFAULT_STATUS_OUTPUT = ROOT / "outputs" / "yt_same_source_top_response_certificate_builder_2026-05-04.json"
SCOUT_TOP_RESPONSE_OUTPUT = ROOT / "outputs" / "yt_same_source_top_response_certificate_builder_scout_certificate_2026-05-04.json"
SCOUT_STATUS_OUTPUT = ROOT / "outputs" / "yt_same_source_top_response_certificate_builder_scout_2026-05-04.json"

PARENTS = {
    "common_window_response_gate": "outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json",
    "pooled_response_estimator": "outputs/yt_fh_lsz_common_window_pooled_response_estimator_2026-05-04.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "higgs_identity_latest_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
    "same_source_top_response_identity_builder": "outputs/yt_same_source_top_response_identity_certificate_builder_2026-05-04.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
}

FIREWALL_FALSE_FIELDS = (
    "used_observed_top_or_yukawa_as_selector",
    "used_H_unit_or_Ward_authority",
    "used_alpha_lm_plaquette_or_u0",
    "used_c2_or_zmatch_equal_one",
)

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


def positive(value: Any) -> bool:
    return finite(value) and float(value) > 0.0


def has_negative_zero_positive(values: list[Any]) -> bool:
    numeric = [float(value) for value in values if finite(value)]
    return (
        any(value < 0.0 for value in numeric)
        and any(abs(value) <= 1.0e-15 for value in numeric)
        and any(value > 0.0 for value in numeric)
    )


def source_shifts_from_response(response: dict[str, Any]) -> list[float]:
    rows = response.get("common_window_summary", {}).get("source_shifts")
    if isinstance(rows, list) and has_negative_zero_positive(rows):
        return [float(value) for value in rows]
    return [-0.01, 0.0, 0.01]


def validate_response(response: dict[str, Any], pooled: dict[str, Any]) -> dict[str, Any]:
    if not response or not pooled:
        return {"present": False, "valid": False, "failed_checks": ["common-window top response inputs absent"]}
    summary = response.get("common_window_summary", {})
    slope = summary.get("common_window_slope_summary", {})
    checks = {
        "response_gate_passed_as_support": response.get("common_window_response_gate_passed") is True,
        "pooled_response_production_grade": pooled.get("pooled_common_window_response_production_grade") is True,
        "finite_slope_mean": finite(slope.get("mean")),
        "positive_empirical_standard_error": positive(pooled.get("empirical_standard_error")),
        "readout_switch_not_authorized": response.get("readout_switch_authorized") is False
        and pooled.get("readout_switch_authorized") is False,
        "proposal_not_authorized": response.get("proposal_allowed") is False
        and pooled.get("proposal_allowed") is False,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
        "slope_dE_top_ds": slope.get("mean"),
        "slope_error": pooled.get("empirical_standard_error"),
        "source_shifts": source_shifts_from_response(response),
    }


def validate_identity(candidate: dict[str, Any], *, require_production: bool) -> dict[str, Any]:
    if not candidate:
        return {"present": False, "valid": False, "failed_checks": ["same-source top-response identity certificate absent"]}
    firewall = candidate.get("firewall", {})
    checks = {
        "phase_allowed": candidate.get("phase") in {"scout", "production", "exact-support"},
        "production_or_exact_if_required": candidate.get("phase") in {"production", "exact-support"}
        if require_production
        else True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "sector_overlap_identity_passed": candidate.get("same_source_sector_overlap_identity_passed") is True,
        "canonical_higgs_pole_identity_passed": candidate.get("canonical_higgs_pole_identity_passed") is True,
        "retained_route_or_proposal_gate_passed": candidate.get("retained_route_or_proposal_gate_passed") is True,
        "proposal_not_authorized_by_candidate": candidate.get("proposal_allowed") is not True,
    }
    checks.update({f"{field}_false": firewall.get(field) is False for field in FIREWALL_FALSE_FIELDS})
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
    }


def validate_covariance(candidate: dict[str, Any], *, require_production: bool) -> dict[str, Any]:
    if not candidate:
        return {"present": False, "valid": False, "failed_checks": ["matched top/W covariance certificate absent"]}
    firewall = candidate.get("firewall", {})
    checks = {
        "phase_allowed": candidate.get("phase") in {"scout", "production"},
        "production_phase_if_required": candidate.get("phase") == "production" if require_production else True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "finite_covariance": finite(candidate.get("cov_dE_top_dM_W")),
        "matched_configuration_set": candidate.get("matched_configuration_set") is True,
        "no_observed_selector": firewall.get("used_observed_top_or_yukawa_as_selector") is False
        and firewall.get("used_observed_WZ_masses_as_selector") is False,
        "no_hunit_or_ward": firewall.get("used_H_unit_or_Ward_authority") is False,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
    }


def build_certificate(
    response_validation: dict[str, Any],
    identity: dict[str, Any],
    covariance: dict[str, Any],
    *,
    phase: str,
) -> dict[str, Any]:
    return {
        "certificate_kind": "same_source_top_response",
        "phase": phase,
        "same_source_coordinate": True,
        "source_coordinate": identity.get("source_coordinate", "same scalar source coordinate used by top FH/LSZ"),
        "source_shifts": response_validation["source_shifts"],
        "top_response": {
            "slope_dE_top_ds": float(response_validation["slope_dE_top_ds"]),
            "slope_error": float(response_validation["slope_error"]),
        },
        "matched_covariance": {
            "cov_dE_top_dM_W": float(covariance["cov_dE_top_dM_W"]),
            "certificate": covariance.get("certificate", "matched top/W covariance certificate"),
        },
        "identity_certificates": {
            "same_source_sector_overlap_identity_passed": identity.get(
                "same_source_sector_overlap_identity_passed"
            )
            is True,
            "canonical_higgs_pole_identity_passed": identity.get("canonical_higgs_pole_identity_passed")
            is True,
            "retained_route_or_proposal_gate_passed": identity.get(
                "retained_route_or_proposal_gate_passed"
            )
            is True,
        },
        "firewall": {field: False for field in FIREWALL_FALSE_FIELDS},
        "proposal_allowed": False,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat source-only dE_top/ds as physical y_t evidence",
            "does not set kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not use H_unit, yt_ward_identity, observed top/y_t, alpha_LM, plaquette, or u0",
        ],
    }


def synthetic_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    response = {
        "common_window_response_gate_passed": True,
        "readout_switch_authorized": False,
        "proposal_allowed": False,
        "common_window_summary": {
            "source_shifts": [-0.01, 0.0, 0.01],
            "common_window_slope_summary": {"mean": 1.4254},
        },
    }
    pooled = {
        "pooled_common_window_response_production_grade": True,
        "empirical_standard_error": 0.0011,
        "readout_switch_authorized": False,
        "proposal_allowed": False,
    }
    identity = {
        "phase": "scout",
        "same_source_coordinate": True,
        "source_coordinate": "synthetic_same_source_s",
        "same_source_sector_overlap_identity_passed": True,
        "canonical_higgs_pole_identity_passed": True,
        "retained_route_or_proposal_gate_passed": True,
        "proposal_allowed": False,
        "firewall": {field: False for field in FIREWALL_FALSE_FIELDS},
    }
    covariance = {
        "phase": "scout",
        "same_source_coordinate": True,
        "matched_configuration_set": True,
        "cov_dE_top_dM_W": 0.0007,
        "certificate": "synthetic matched covariance",
        "firewall": {
            "used_observed_top_or_yukawa_as_selector": False,
            "used_observed_WZ_masses_as_selector": False,
            "used_H_unit_or_Ward_authority": False,
        },
    }
    return response, pooled, identity, covariance


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--response-input", type=Path, default=DEFAULT_RESPONSE_INPUT)
    parser.add_argument("--pooled-input", type=Path, default=DEFAULT_POOLED_INPUT)
    parser.add_argument("--identity-input", type=Path, default=DEFAULT_IDENTITY_INPUT)
    parser.add_argument("--covariance-input", type=Path, default=DEFAULT_COVARIANCE_INPUT)
    parser.add_argument("--top-response-output", type=Path, default=DEFAULT_TOP_RESPONSE_OUTPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_STATUS_OUTPUT)
    parser.add_argument("--scout", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mode = "strict" if args.strict else "scout" if args.scout else "current"
    status_output = SCOUT_STATUS_OUTPUT if args.scout and args.output == DEFAULT_STATUS_OUTPUT else args.output
    top_response_output = (
        SCOUT_TOP_RESPONSE_OUTPUT
        if args.scout and args.top_response_output == DEFAULT_TOP_RESPONSE_OUTPUT
        else args.top_response_output
    )

    print("PR #230 same-source top-response certificate builder")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    parent_statuses = {name: status(cert) for name, cert in parents.items()}

    if args.scout:
        response, pooled, identity, covariance = synthetic_inputs()
    else:
        response = load_json(args.response_input)
        pooled = load_json(args.pooled_input)
        identity = load_json(args.identity_input)
        covariance = load_json(args.covariance_input)

    require_production = args.strict
    response_validation = validate_response(response, pooled)
    identity_validation = validate_identity(identity, require_production=require_production)
    covariance_validation = validate_covariance(covariance, require_production=require_production)
    inputs_valid = response_validation["valid"] and identity_validation["valid"] and covariance_validation["valid"]
    strict_gate_passed = args.strict and inputs_valid
    scout_gate_passed = args.scout and inputs_valid
    current_inputs_valid = (not args.strict) and (not args.scout) and inputs_valid

    certificate_written = False
    top_certificate: dict[str, Any] = {}
    if strict_gate_passed or scout_gate_passed or current_inputs_valid:
        top_certificate = build_certificate(
            response_validation,
            identity,
            covariance,
            phase="production" if args.strict or current_inputs_valid else "scout",
        )
        top_response_output.parent.mkdir(parents=True, exist_ok=True)
        top_response_output.write_text(json.dumps(top_certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        certificate_written = True

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("common-window-response-support-present", response_validation["present"], parent_statuses["common_window_response_gate"])
    report("sector-overlap-currently-blocked", "sector-overlap identity obstruction" in parent_statuses["same_source_sector_overlap"], parent_statuses["same_source_sector_overlap"])
    report("higgs-identity-currently-blocked", "Higgs-pole identity blocker" in parent_statuses["higgs_identity_latest_blocker"], parent_statuses["higgs_identity_latest_blocker"])
    report("top-response-identity-builder-currently-open", "same-source top-response identity" in parent_statuses["same_source_top_response_identity_builder"], parent_statuses["same_source_top_response_identity_builder"])
    report("top-wz-covariance-builder-currently-open", "matched top-W" in parent_statuses["top_wz_matched_covariance_builder"], parent_statuses["top_wz_matched_covariance_builder"])
    if args.scout:
        report("scout-response-valid", response_validation["valid"], str(response_validation.get("failed_checks", [])))
        report("scout-identity-valid", identity_validation["valid"], str(identity_validation.get("failed_checks", [])))
        report("scout-covariance-valid", covariance_validation["valid"], str(covariance_validation.get("failed_checks", [])))
        report("scout-top-response-certificate-written", certificate_written, display(top_response_output))
    elif args.strict:
        report("strict-response-valid", response_validation["valid"], str(response_validation.get("failed_checks", [])))
        report("strict-identity-valid", identity_validation["valid"], str(identity_validation.get("failed_checks", [])))
        report("strict-covariance-valid", covariance_validation["valid"], str(covariance_validation.get("failed_checks", [])))
        report("strict-top-response-certificate-written", certificate_written, display(top_response_output))
    else:
        report("current-response-valid-as-support", response_validation["valid"], str(response_validation.get("failed_checks", [])))
        report("future-identity-certificate-absent", not identity_validation["present"], display(args.identity_input))
        report("future-covariance-certificate-absent", not covariance_validation["present"], display(args.covariance_input))
        report("current-mode-does-not-write-top-response-certificate", not certificate_written, display(DEFAULT_TOP_RESPONSE_OUTPUT))
    report("strict-top-response-certificate-not-claimed" if not args.strict else "strict-top-response-certificate-passed", not strict_gate_passed if not args.strict else strict_gate_passed, f"strict_gate_passed={strict_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "scout-pass / same-source top-response certificate builder"
            if scout_gate_passed
            else "strict-pass / same-source top-response certificate built"
            if strict_gate_passed
            else "support / same-source top-response certificate built"
            if current_inputs_valid
            else "open / same-source top-response identity or covariance inputs absent"
        ),
        "mode": mode,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The builder wraps response-side support only after identity and "
            "matched covariance certificates exist.  It does not authorize a "
            "physical y_t readout by itself."
        ),
        "bare_retained_allowed": False,
        "same_source_top_response_certificate_builder_passed": scout_gate_passed
        or strict_gate_passed
        or current_inputs_valid,
        "strict_same_source_top_response_certificate_builder_passed": strict_gate_passed,
        "top_response_certificate_written": certificate_written,
        "top_response_certificate_output": display(top_response_output),
        "response_input": display(args.response_input),
        "pooled_input": display(args.pooled_input),
        "identity_input": display(args.identity_input),
        "covariance_input": display(args.covariance_input),
        "response_validation": response_validation,
        "identity_validation": identity_validation,
        "covariance_validation": covariance_validation,
        "top_response_certificate": top_certificate,
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat source-only dE_top/ds as physical y_t evidence",
            "does not set kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not use H_unit, yt_ward_identity, observed top/y_t, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            f"Supply {display(DEFAULT_IDENTITY_INPUT)} and "
            f"{display(DEFAULT_COVARIANCE_INPUT)}, rerun this builder in strict "
            f"mode to write {display(DEFAULT_TOP_RESPONSE_OUTPUT)}, then rerun "
            "the W/Z mass-fit response-row builder."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    status_output.parent.mkdir(parents=True, exist_ok=True)
    status_output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote status certificate: {display(status_output)}")
    if certificate_written:
        print(f"Wrote top-response certificate: {display(top_response_output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if args.strict and not strict_gate_passed:
        return 1
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
