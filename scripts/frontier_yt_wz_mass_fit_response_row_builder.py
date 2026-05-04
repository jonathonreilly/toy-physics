#!/usr/bin/env python3
"""
PR #230 W/Z mass-fit to response-row builder.

This is the missing adapter between future W/Z correlator mass fits and the
existing same-source W/Z response certificate builder.  It does not measure
W/Z correlators and it does not synthesize response rows.  In strict mode it
writes

    outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json

only when future production W/Z mass-fit rows, matched top-response rows,
identity certificates, and an electroweak coupling certificate all validate.
Scout mode proves the slope extraction, covariance plumbing, and firewalls in
a scout-only output namespace.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WZ_MASS_FIT_INPUT = ROOT / "outputs" / "yt_wz_correlator_mass_fit_rows_2026-05-04.json"
DEFAULT_TOP_RESPONSE_INPUT = ROOT / "outputs" / "yt_same_source_top_response_certificate_2026-05-04.json"
DEFAULT_G2_INPUT = ROOT / "outputs" / "yt_electroweak_g2_certificate_2026-05-04.json"
DEFAULT_ROWS_OUTPUT = ROOT / "outputs" / "yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json"
DEFAULT_STATUS_OUTPUT = ROOT / "outputs" / "yt_wz_mass_fit_response_row_builder_2026-05-04.json"
SCOUT_ROWS_OUTPUT = ROOT / "outputs" / "yt_wz_mass_fit_response_row_builder_scout_rows_2026-05-04.json"
SCOUT_STATUS_OUTPUT = ROOT / "outputs" / "yt_wz_mass_fit_response_row_builder_scout_2026-05-04.json"

PARENTS = {
    "wz_correlator_mass_fit_path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_response_measurement_row_contract": "outputs/yt_wz_response_measurement_row_contract_gate_2026-05-03.json",
    "fh_gauge_mass_response_builder": "outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json",
    "same_source_wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "same_source_w_response_row_builder": "outputs/yt_same_source_w_response_row_builder_2026-05-04.json",
    "same_source_w_response_lightweight_readout": "outputs/yt_same_source_w_response_lightweight_readout_harness_2026-05-04.json",
}

FIREWALL_FALSE_FIELDS = (
    "used_observed_WZ_masses_as_selector",
    "used_observed_top_or_yukawa_as_selector",
    "used_static_v_overlap_selector",
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


def nonnegative(value: Any) -> bool:
    return finite(value) and float(value) >= 0.0


def source_shift_key(value: Any) -> str:
    return f"{float(value):.15g}" if finite(value) else str(value)


def has_negative_zero_positive(values: list[Any]) -> bool:
    numeric = [float(value) for value in values if finite(value)]
    return (
        any(value < 0.0 for value in numeric)
        and any(abs(value) <= 1.0e-15 for value in numeric)
        and any(value > 0.0 for value in numeric)
    )


def mass_fit_from_correlator(row: dict[str, Any]) -> tuple[str | None, dict[str, Any]]:
    for boson, key in (("W", "w_mass_fit"), ("Z", "z_mass_fit")):
        fit = row.get(key)
        if isinstance(fit, dict) and finite(fit.get("mass_lat")) and fit.get("from_correlator") is True:
            return boson, fit
    return None, {}


def validate_wz_mass_fits(candidate: dict[str, Any], *, require_production: bool) -> dict[str, Any]:
    if not candidate:
        return {"present": False, "valid": False, "failed_checks": ["W/Z mass-fit rows absent"]}

    source_shifts = candidate.get("source_shifts", [])
    rows = candidate.get("per_source_shift_mass_fits", candidate.get("per_source_shift_rows", []))
    firewall = candidate.get("firewall", {})
    row_shift_set = {
        source_shift_key(row.get("source_shift"))
        for row in rows
        if isinstance(row, dict) and finite(row.get("source_shift"))
    }
    source_shift_set = {source_shift_key(value) for value in source_shifts if finite(value)}
    bosons: list[str] = []
    row_checks = []
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            row_checks.append(False)
            continue
        boson, fit = mass_fit_from_correlator(row)
        if boson:
            bosons.append(boson)
        row_checks.append(
            finite(row.get("source_shift"))
            and boson in {"W", "Z"}
            and positive(fit.get("mass_lat_err", fit.get("mass_error", fit.get("stderr", 0.0))))
            and finite(row.get("jackknife_or_bootstrap_block_count"))
            and bool(row.get("fit_window") or row.get("effective_mass_method"))
        )
    checks = {
        "phase_allowed": candidate.get("phase") in {"scout", "production"},
        "production_phase_if_required": candidate.get("phase") == "production" if require_production else True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "source_coordinate_named": isinstance(candidate.get("source_coordinate"), str)
        and bool(candidate.get("source_coordinate")),
        "source_shifts_neg_zero_pos": isinstance(source_shifts, list)
        and has_negative_zero_positive(source_shifts),
        "rows_present": isinstance(rows, list) and len(rows) >= max(3, len(source_shift_set)),
        "rows_cover_source_shifts": bool(source_shift_set) and source_shift_set.issubset(row_shift_set),
        "rows_are_correlator_mass_fits": bool(row_checks) and all(row_checks),
        "single_w_or_z_channel": len(set(bosons)) == 1 if bosons else False,
        "no_static_ew_mass_algebra": firewall.get("used_static_EW_mass_algebra") is False,
        "no_observed_wz_selector": firewall.get("used_observed_WZ_masses_as_selector") is False,
        "no_hunit_or_ward": firewall.get("used_H_unit_or_Ward_authority") is False,
        "no_alpha_lm_plaquette_or_u0": firewall.get("used_alpha_lm_plaquette_or_u0") is False,
        "not_yukawa_readout": candidate.get("used_as_physical_yukawa_readout") is False,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
        "boson_channel": bosons[0] if bosons and len(set(bosons)) == 1 else None,
    }


def validate_top_response(candidate: dict[str, Any], *, require_production: bool) -> dict[str, Any]:
    if not candidate:
        return {"present": False, "valid": False, "failed_checks": ["same-source top response certificate absent"]}

    top = candidate.get("top_response", candidate)
    identity = candidate.get("identity_certificates", {})
    covariance = candidate.get("matched_covariance", {})
    firewall = candidate.get("firewall", {})
    source_shifts = candidate.get("source_shifts", [])
    checks = {
        "phase_allowed": candidate.get("phase") in {"scout", "production"},
        "production_phase_if_required": candidate.get("phase") == "production" if require_production else True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "source_coordinate_named": isinstance(candidate.get("source_coordinate"), str)
        and bool(candidate.get("source_coordinate")),
        "source_shifts_neg_zero_pos": isinstance(source_shifts, list)
        and has_negative_zero_positive(source_shifts),
        "finite_top_slope": finite(top.get("slope_dE_top_ds")),
        "positive_top_slope_error": positive(top.get("slope_error")),
        "finite_top_w_covariance": finite(covariance.get("cov_dE_top_dM_W"))
        or finite(candidate.get("cov_dE_top_dM_W")),
        "sector_overlap_identity_passed": identity.get("same_source_sector_overlap_identity_passed") is True,
        "canonical_higgs_identity_passed": identity.get("canonical_higgs_pole_identity_passed") is True,
        "retained_route_gate_passed": identity.get("retained_route_or_proposal_gate_passed") is True,
        "no_observed_top_or_yukawa_selector": firewall.get("used_observed_top_or_yukawa_as_selector") is False,
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


def validate_g2(candidate: dict[str, Any], *, require_production: bool) -> dict[str, Any]:
    if not candidate:
        return {"present": False, "valid": False, "failed_checks": ["electroweak g2 certificate absent"]}
    checks = {
        "phase_allowed": candidate.get("phase") in {"scout", "production", "exact-support"},
        "production_or_exact_if_required": candidate.get("phase") in {"production", "exact-support"}
        if require_production
        else True,
        "positive_g2": positive(candidate.get("g2")),
        "nonnegative_sigma_g2": nonnegative(candidate.get("sigma_g2", 0.0)),
        "certificate_reference_present": isinstance(candidate.get("g2_certificate"), str)
        and bool(candidate.get("g2_certificate")),
        "not_observed_selector": candidate.get("used_observed_g2_as_selector") is False,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
    }


def weighted_linear_slope(points: list[tuple[float, float, float]]) -> dict[str, Any]:
    weights = [1.0 / (sigma * sigma) for _, _, sigma in points]
    sw = sum(weights)
    sx = sum(weight * x for weight, (x, _, _) in zip(weights, points))
    sy = sum(weight * y for weight, (_, y, _) in zip(weights, points))
    sxx = sum(weight * x * x for weight, (x, _, _) in zip(weights, points))
    sxy = sum(weight * x * y for weight, (x, y, _) in zip(weights, points))
    denom = sw * sxx - sx * sx
    if denom <= 0.0:
        return {"valid": False, "reason": "singular weighted linear fit"}
    slope = (sw * sxy - sx * sy) / denom
    intercept = (sxx * sy - sx * sxy) / denom
    slope_error = math.sqrt(sw / denom)
    chi2 = sum(weight * (y - (intercept + slope * x)) ** 2 for weight, (x, y, _) in zip(weights, points))
    dof = max(len(points) - 2, 0)
    return {
        "valid": True,
        "slope": slope,
        "intercept": intercept,
        "slope_error": slope_error,
        "chi2": chi2,
        "dof": dof,
        "chi2_per_dof": chi2 / dof if dof else None,
    }


def extract_mass_fit_points(wz_rows: dict[str, Any]) -> tuple[str, list[tuple[float, float, float]], list[dict[str, Any]]]:
    rows = wz_rows.get("per_source_shift_mass_fits", wz_rows.get("per_source_shift_rows", []))
    points = []
    copied_rows = []
    channel = "W"
    for row in rows:
        boson, fit = mass_fit_from_correlator(row)
        if boson is None:
            continue
        channel = boson
        mass_error = float(fit.get("mass_lat_err", fit.get("mass_error", fit.get("stderr"))))
        points.append((float(row["source_shift"]), float(fit["mass_lat"]), mass_error))
        copied_rows.append(row)
    points.sort(key=lambda item: item[0])
    return channel, points, copied_rows


def build_measurement_rows(
    wz_rows: dict[str, Any],
    top_response: dict[str, Any],
    g2_cert: dict[str, Any],
    *,
    phase: str,
) -> dict[str, Any]:
    channel, points, copied_rows = extract_mass_fit_points(wz_rows)
    slope = weighted_linear_slope(points)
    top = top_response.get("top_response", top_response)
    covariance = top_response.get("matched_covariance", {})
    cov_value = covariance.get("cov_dE_top_dM_W", top_response.get("cov_dE_top_dM_W", 0.0))
    gauge_response = {
        "slope_error": slope["slope_error"],
        "cov_dE_top_dM_W": float(cov_value),
    }
    if channel == "W":
        gauge_response["slope_dM_W_ds"] = slope["slope"]
    else:
        gauge_response["slope_dM_Z_ds"] = slope["slope"]
        gauge_response["cov_dE_top_dM_Z"] = float(cov_value)
    identity = top_response.get("identity_certificates", {})
    source_shifts = wz_rows.get("source_shifts", top_response.get("source_shifts", []))
    return {
        "phase": phase,
        "same_source_coordinate": True,
        "source_coordinate": wz_rows.get("source_coordinate") or top_response.get("source_coordinate"),
        "source_shifts": source_shifts,
        "wz_mass_fits_from_correlators": True,
        "per_source_shift_rows": copied_rows,
        "top_response": {
            "slope_dE_top_ds": float(top["slope_dE_top_ds"]),
            "slope_error": float(top["slope_error"]),
        },
        "gauge_response": gauge_response,
        "gauge_response_fit": {
            "channel": channel,
            "weighted_linear_fit": slope,
            "fit_points": [
                {"source_shift": x, "mass_lat": y, "mass_lat_err": sigma}
                for x, y, sigma in points
            ],
        },
        "electroweak_coupling": {
            "g2": float(g2_cert["g2"]),
            "sigma_g2": float(g2_cert.get("sigma_g2", 0.0)),
            "g2_certificate": g2_cert["g2_certificate"],
            "used_observed_g2_as_selector": False,
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
            "does not generate W/Z mass fits",
            "does not use static EW algebra as dM_W/ds",
            "does not use observed W/Z, top, y_t, or g2 selectors",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette/u0, c2=1, Z_match=1, or kappa_s=1",
        ],
    }


def synthetic_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    shifts = [-0.01, 0.0, 0.01]
    rows = []
    for shift in shifts:
        mass = 0.318 + 0.46 * shift
        rows.append(
            {
                "source_shift": shift,
                "configuration_count": 256,
                "w_mass_fit": {
                    "mass_lat": mass,
                    "mass_lat_err": 0.004,
                    "from_correlator": True,
                    "fit_window": [4, 10],
                },
                "effective_mass_method": "single_state_plateau_scout",
                "jackknife_or_bootstrap_block_count": 64,
            }
        )
    wz = {
        "phase": "scout",
        "same_source_coordinate": True,
        "source_coordinate": "synthetic_same_source_s",
        "source_shifts": shifts,
        "per_source_shift_mass_fits": rows,
        "firewall": {
            "used_static_EW_mass_algebra": False,
            "used_observed_WZ_masses_as_selector": False,
            "used_H_unit_or_Ward_authority": False,
            "used_alpha_lm_plaquette_or_u0": False,
        },
        "used_as_physical_yukawa_readout": False,
    }
    top = {
        "phase": "scout",
        "same_source_coordinate": True,
        "source_coordinate": "synthetic_same_source_s",
        "source_shifts": shifts,
        "top_response": {"slope_dE_top_ds": 1.31, "slope_error": 0.04},
        "matched_covariance": {"cov_dE_top_dM_W": 0.0007},
        "identity_certificates": {
            "same_source_sector_overlap_identity_passed": True,
            "canonical_higgs_pole_identity_passed": True,
            "retained_route_or_proposal_gate_passed": True,
        },
        "firewall": {
            "used_observed_top_or_yukawa_as_selector": False,
            "used_H_unit_or_Ward_authority": False,
            "used_alpha_lm_plaquette_or_u0": False,
            "used_c2_or_zmatch_equal_one": False,
        },
    }
    g2 = {
        "phase": "scout",
        "g2": 0.65,
        "sigma_g2": 0.0015,
        "g2_certificate": "synthetic scout g2",
        "used_observed_g2_as_selector": False,
    }
    return wz, top, g2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wz-mass-fit-input", type=Path, default=DEFAULT_WZ_MASS_FIT_INPUT)
    parser.add_argument("--top-response-input", type=Path, default=DEFAULT_TOP_RESPONSE_INPUT)
    parser.add_argument("--g2-input", type=Path, default=DEFAULT_G2_INPUT)
    parser.add_argument("--rows-output", type=Path, default=DEFAULT_ROWS_OUTPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_STATUS_OUTPUT)
    parser.add_argument("--scout", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mode = "strict" if args.strict else "scout" if args.scout else "current"
    status_output = SCOUT_STATUS_OUTPUT if args.scout and args.output == DEFAULT_STATUS_OUTPUT else args.output
    rows_output = SCOUT_ROWS_OUTPUT if args.scout and args.rows_output == DEFAULT_ROWS_OUTPUT else args.rows_output

    print("PR #230 W/Z mass-fit response-row builder")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    parent_statuses = {name: status(cert) for name, cert in parents.items()}

    if args.scout:
        wz_rows, top_response, g2_cert = synthetic_inputs()
    else:
        wz_rows = load_json(args.wz_mass_fit_input)
        top_response = load_json(args.top_response_input)
        g2_cert = load_json(args.g2_input)

    require_production = args.strict
    wz_validation = validate_wz_mass_fits(wz_rows, require_production=require_production)
    top_validation = validate_top_response(top_response, require_production=require_production)
    g2_validation = validate_g2(g2_cert, require_production=require_production)
    inputs_valid = wz_validation["valid"] and top_validation["valid"] and g2_validation["valid"]
    strict_gate_passed = args.strict and inputs_valid
    scout_gate_passed = args.scout and inputs_valid
    current_inputs_valid = (not args.strict) and (not args.scout) and inputs_valid

    rows_written = False
    measurement_rows: dict[str, Any] = {}
    if strict_gate_passed or scout_gate_passed or current_inputs_valid:
        measurement_rows = build_measurement_rows(
            wz_rows,
            top_response,
            g2_cert,
            phase="production" if args.strict or current_inputs_valid else "scout",
        )
        rows_output.parent.mkdir(parents=True, exist_ok=True)
        rows_output.write_text(json.dumps(measurement_rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        rows_written = True

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("mass-fit-path-gate-open", "WZ correlator mass-fit path absent" in parent_statuses["wz_correlator_mass_fit_path"], parent_statuses["wz_correlator_mass_fit_path"])
    report("response-row-contract-available", "WZ response measurement-row contract gate" in parent_statuses["wz_response_measurement_row_contract"], parent_statuses["wz_response_measurement_row_contract"])
    if args.scout:
        report("scout-wz-mass-fit-rows-valid", wz_validation["valid"], str(wz_validation.get("failed_checks", [])))
        report("scout-top-response-valid", top_validation["valid"], str(top_validation.get("failed_checks", [])))
        report("scout-g2-valid", g2_validation["valid"], str(g2_validation.get("failed_checks", [])))
        report("scout-measurement-rows-written", rows_written, display(rows_output))
    elif args.strict:
        report("strict-wz-mass-fit-rows-valid", wz_validation["valid"], str(wz_validation.get("failed_checks", [])))
        report("strict-top-response-valid", top_validation["valid"], str(top_validation.get("failed_checks", [])))
        report("strict-g2-valid", g2_validation["valid"], str(g2_validation.get("failed_checks", [])))
        report("strict-measurement-rows-written", rows_written, display(rows_output))
    else:
        report("future-wz-mass-fit-rows-absent", not wz_validation["present"], display(args.wz_mass_fit_input))
        report("future-top-response-certificate-absent", not top_validation["present"], display(args.top_response_input))
        report("future-g2-certificate-absent", not g2_validation["present"], display(args.g2_input))
        report("current-mode-does-not-write-production-rows", not rows_written, display(DEFAULT_ROWS_OUTPUT))
    report("strict-production-response-row-builder-not-claimed" if not args.strict else "strict-production-response-row-builder-passed", not strict_gate_passed if not args.strict else strict_gate_passed, f"strict_gate_passed={strict_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "scout-pass / WZ mass-fit response-row builder"
            if scout_gate_passed
            else "strict-pass / WZ response measurement rows built"
            if strict_gate_passed
            else "support / WZ response measurement rows built"
            if current_inputs_valid
            else "open / WZ mass-fit response-row builder inputs absent"
        ),
        "mode": mode,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The builder only adapts future W/Z mass fits into the row schema "
            "for the existing W/Z certificate builder.  Closure still requires "
            "strict rows, W/Z gate pass, W-response rows, correction authority, "
            "matching/running, and audit."
        ),
        "bare_retained_allowed": False,
        "wz_mass_fit_response_row_builder_passed": scout_gate_passed
        or strict_gate_passed
        or current_inputs_valid,
        "strict_wz_mass_fit_response_row_builder_passed": strict_gate_passed,
        "measurement_rows_written": rows_written,
        "measurement_rows_output": display(rows_output),
        "wz_mass_fit_input": display(args.wz_mass_fit_input),
        "top_response_input": display(args.top_response_input),
        "g2_input": display(args.g2_input),
        "wz_validation": wz_validation,
        "top_response_validation": top_validation,
        "g2_validation": g2_validation,
        "measurement_rows": measurement_rows,
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not produce W/Z correlator mass fits",
            "does not use static EW algebra as dM_W/ds",
            "does not use observed W/Z, top, y_t, or g2 selectors",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette/u0, c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            f"Supply {display(DEFAULT_WZ_MASS_FIT_INPUT)}, "
            f"{display(DEFAULT_TOP_RESPONSE_INPUT)}, and {display(DEFAULT_G2_INPUT)}, "
            f"rerun this builder in strict mode to write {display(DEFAULT_ROWS_OUTPUT)}, "
            "then rerun the W/Z response certificate builder and same-source W/Z gate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    status_output.parent.mkdir(parents=True, exist_ok=True)
    status_output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote status certificate: {display(status_output)}")
    if rows_written:
        print(f"Wrote measurement rows: {display(rows_output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if args.strict and not strict_gate_passed:
        return 1
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
