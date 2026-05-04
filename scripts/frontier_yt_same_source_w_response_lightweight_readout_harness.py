#!/usr/bin/env python3
"""
PR #230 lightweight same-source W-response readout harness.

This runner is the concrete small-compute contract for the W-response route.
It does not generate W configurations.  It validates the minimal production
row shape needed to turn same-source top and W mass slopes into a physical
canonical-Higgs top Yukawa readout:

    y_h = g_2 R_t / (sqrt(2) R_W) - delta_perp.

Scout mode builds synthetic rows to prove the algebra, error propagation, and
firewalls work.  Strict mode requires a real production row certificate and
fails honestly while that certificate is absent.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "yt_same_source_w_response_rows_2026-05-04.json"
DEFAULT_OUTPUT = (
    ROOT
    / "outputs"
    / "yt_same_source_w_response_lightweight_readout_harness_2026-05-04.json"
)

PARENTS = {
    "same_source_w_response_decomposition": "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json",
    "same_source_w_response_orthogonal_correction": "outputs/yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json",
    "one_higgs_completeness_orthogonal_null": "outputs/yt_one_higgs_completeness_orthogonal_null_gate_2026-05-04.json",
    "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "same_source_wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "matching_running_bridge": "outputs/yt_pr230_matching_running_bridge_gate_2026-05-04.json",
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

ALLOWED_DELTA_METHODS = {
    "measured_tomography_correction",
    "source_higgs_gram_purity",
    "one_higgs_completeness",
    "neutral_rank_one_theorem",
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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def positive(value: Any) -> bool:
    return finite(value) and float(value) > 0.0


def as_float(value: Any) -> float:
    return float(value)


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def readout_from_row(row: dict[str, Any]) -> dict[str, Any]:
    g2 = as_float(row["g_2"])
    rt = as_float(row["R_t"])
    rw = as_float(row["R_W"])
    delta = as_float(row["delta_perp"])
    sig_g2 = as_float(row.get("sigma_g_2", 0.0))
    sig_rt = as_float(row["sigma_R_t"])
    sig_rw = as_float(row["sigma_R_W"])
    sig_delta = as_float(row["sigma_delta_perp"])
    cov_rt_rw = as_float(row.get("cov_R_t_R_W", 0.0))

    raw = g2 * rt / (math.sqrt(2.0) * rw)
    corrected = raw - delta
    grad_g2 = rt / (math.sqrt(2.0) * rw)
    grad_rt = g2 / (math.sqrt(2.0) * rw)
    grad_rw = -g2 * rt / (math.sqrt(2.0) * rw * rw)
    variance = (
        grad_g2 * grad_g2 * sig_g2 * sig_g2
        + grad_rt * grad_rt * sig_rt * sig_rt
        + grad_rw * grad_rw * sig_rw * sig_rw
        + sig_delta * sig_delta
        + 2.0 * grad_rt * grad_rw * cov_rt_rw
    )
    sigma = math.sqrt(max(variance, 0.0))
    return {
        "volume": row.get("volume", "unknown"),
        "raw_same_source_w_readout": raw,
        "delta_perp": delta,
        "corrected_y_h": corrected,
        "sigma_corrected_y_h": sigma,
        "variance": variance,
    }


def combine_readouts(readouts: list[dict[str, Any]]) -> dict[str, Any]:
    weights = []
    for item in readouts:
        sigma = item["sigma_corrected_y_h"]
        if sigma <= 0.0:
            weights.append(0.0)
        else:
            weights.append(1.0 / (sigma * sigma))
    weight_sum = sum(weights)
    if weight_sum <= 0.0:
        return {"valid": False, "reason": "no positive readout weights"}
    mean = sum(w * item["corrected_y_h"] for w, item in zip(weights, readouts)) / weight_sum
    sigma = math.sqrt(1.0 / weight_sum)
    chi2 = sum(
        w * (item["corrected_y_h"] - mean) ** 2
        for w, item in zip(weights, readouts)
    )
    dof = max(len(readouts) - 1, 0)
    return {
        "valid": True,
        "combined_y_h": mean,
        "sigma_combined_y_h": sigma,
        "chi2": chi2,
        "dof": dof,
        "chi2_per_dof": chi2 / dof if dof else None,
        "weights": weights,
    }


def validate_firewall(candidate: dict[str, Any]) -> dict[str, Any]:
    firewall = candidate.get("firewall", {})
    checks = {field: firewall.get(field) is False for field in FORBIDDEN_FALSE_FIELDS}
    return {
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [field for field, ok in checks.items() if not ok],
    }


def validate_row(row: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "finite_g_2": positive(row.get("g_2")),
        "finite_R_t": finite(row.get("R_t")),
        "finite_R_W": finite(row.get("R_W")) and abs(float(row.get("R_W", 0.0))) > 0.0,
        "positive_sigma_R_t": positive(row.get("sigma_R_t")),
        "positive_sigma_R_W": positive(row.get("sigma_R_W")),
        "finite_sigma_g_2": finite(row.get("sigma_g_2", 0.0)) and float(row.get("sigma_g_2", 0.0)) >= 0.0,
        "finite_delta_perp": finite(row.get("delta_perp")),
        "finite_sigma_delta_perp": finite(row.get("sigma_delta_perp")) and float(row.get("sigma_delta_perp")) >= 0.0,
        "allowed_delta_method": row.get("delta_perp_method") in ALLOWED_DELTA_METHODS,
        "same_source_coordinate": row.get("same_source_coordinate") is True,
        "not_static_EW_algebra": row.get("row_kind") in {"production_mass_slope", "scout_synthetic_mass_slope"},
    }
    return {
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
    }


def validate_candidate(candidate: dict[str, Any], *, require_production: bool) -> dict[str, Any]:
    if not candidate:
        return {
            "present": False,
            "valid": False,
            "failed_checks": ["same-source W-response row certificate absent"],
        }

    rows = candidate.get("response_rows", [])
    row_validations = [validate_row(row) for row in rows if isinstance(row, dict)]
    readouts = [
        readout_from_row(row)
        for row, validation in zip(rows, row_validations)
        if validation["valid"]
    ]
    combined = combine_readouts(readouts) if readouts else {"valid": False, "reason": "no valid rows"}
    firewall = validate_firewall(candidate)
    checks = {
        "certificate_kind": candidate.get("certificate_kind") == "same_source_w_response_rows",
        "phase_allowed": candidate.get("phase") in {"scout", "production"},
        "production_phase_if_required": (candidate.get("phase") == "production") if require_production else True,
        "same_surface_cl3_z3": candidate.get("same_surface_cl3_z3") is True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "source_shifts_at_least_three": len(candidate.get("source_shifts", [])) >= 3,
        "rows_present": len(rows) > 0,
        "all_rows_valid": bool(row_validations) and all(row["valid"] for row in row_validations),
        "combined_readout_valid": combined.get("valid") is True,
        "firewall_valid": firewall["valid"],
        "proposal_not_authorized_by_input": candidate.get("proposal_allowed") is not True,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
        "row_validations": row_validations,
        "readouts": readouts,
        "combined_readout": combined,
        "firewall_validation": firewall,
    }


def synthetic_scout_certificate() -> dict[str, Any]:
    y_h = 0.9176
    g2 = 0.648
    rows = []
    cases = [
        ("L6_T12_scout_null", 0.0, 0.0005, "one_higgs_completeness", 1.00),
        ("L8_T16_scout_tomography", -0.031, 0.0030, "measured_tomography_correction", 0.74),
        ("L10_T20_scout_rank_one", 0.0, 0.0008, "neutral_rank_one_theorem", 1.22),
    ]
    for index, (volume, delta, sigma_delta, method, kappa_h) in enumerate(cases):
        rw = g2 * kappa_h / 2.0
        raw = y_h + delta
        rt = raw * math.sqrt(2.0) * rw / g2
        rows.append(
            {
                "volume": volume,
                "row_kind": "scout_synthetic_mass_slope",
                "same_source_coordinate": True,
                "g_2": g2,
                "sigma_g_2": 0.0015,
                "R_t": rt,
                "sigma_R_t": 0.004 + 0.001 * index,
                "R_W": rw,
                "sigma_R_W": 0.003 + 0.001 * index,
                "cov_R_t_R_W": 0.0,
                "delta_perp": delta,
                "sigma_delta_perp": sigma_delta,
                "delta_perp_method": method,
            }
        )
    return {
        "certificate_kind": "same_source_w_response_rows",
        "phase": "scout",
        "same_surface_cl3_z3": True,
        "same_source_coordinate": True,
        "source_shifts": [-0.01, 0.0, 0.01],
        "response_rows": rows,
        "proposal_allowed": False,
        "firewall": {field: False for field in FORBIDDEN_FALSE_FIELDS},
    }


def rejection_witnesses() -> dict[str, Any]:
    base = synthetic_scout_certificate()
    missing_delta = json.loads(json.dumps(base))
    missing_delta["response_rows"][0]["delta_perp_method"] = "assumed_zero"

    mismatched_source = json.loads(json.dumps(base))
    mismatched_source["same_source_coordinate"] = False
    mismatched_source["response_rows"][0]["same_source_coordinate"] = False

    observed_selector = json.loads(json.dumps(base))
    observed_selector["firewall"]["used_observed_y_t_or_m_t_as_selector"] = True

    static_ew = json.loads(json.dumps(base))
    static_ew["response_rows"][0]["row_kind"] = "static_EW_algebra"

    return {
        "missing-delta-authority": validate_candidate(missing_delta, require_production=False),
        "mismatched-source": validate_candidate(mismatched_source, require_production=False),
        "observed-selector": validate_candidate(observed_selector, require_production=False),
        "static-ew-algebra": validate_candidate(static_ew, require_production=False),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--scout", action="store_true", help="run synthetic scout validation")
    parser.add_argument("--strict", action="store_true", help="require production row certificate")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mode = "strict" if args.strict else "scout" if args.scout else "current"
    print("PR #230 lightweight same-source W-response readout harness")
    print("=" * 72)

    parents = {name: load_rel(path) for name, path in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    parent_statuses = {name: status(cert) for name, cert in parents.items()}

    decomposition_ok = (
        parents["same_source_w_response_decomposition"].get(
            "same_source_w_response_decomposition_theorem_passed"
        )
        is True
    )
    correction_theorem_ok = (
        parents["same_source_w_response_orthogonal_correction"].get(
            "orthogonal_correction_theorem_passed"
        )
        is True
    )
    one_higgs_conditional_ok = (
        parents["one_higgs_completeness_orthogonal_null"].get(
            "one_higgs_completeness_orthogonal_null_theorem_passed"
        )
        is True
    )
    current_wz_rows_absent = (
        parents["same_source_wz_response_gate"].get(
            "same_source_wz_response_certificate_gate_passed"
        )
        is False
    )

    candidate = synthetic_scout_certificate() if args.scout else load_json(args.input)
    validation = validate_candidate(candidate, require_production=args.strict)
    rejections = rejection_witnesses()
    rejections_ok = all(result["valid"] is False for result in rejections.values())
    scout_target_ok = False
    if args.scout and validation["valid"]:
        combined = validation["combined_readout"]
        scout_target_ok = abs(combined["combined_y_h"] - 0.9176) < 0.02

    strict_gate_passed = args.strict and validation["valid"]
    current_gate_passed = (not args.strict) and (not args.scout) and validation["valid"]

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("same-source-w-decomposition-available", decomposition_ok, parent_statuses["same_source_w_response_decomposition"])
    report("orthogonal-correction-theorem-available", correction_theorem_ok, parent_statuses["same_source_w_response_orthogonal_correction"])
    report("one-higgs-null-conditional-available", one_higgs_conditional_ok, parent_statuses["one_higgs_completeness_orthogonal_null"])
    report("current-wz-production-rows-absent", current_wz_rows_absent, parent_statuses["same_source_wz_response_gate"])
    if args.strict:
        report("strict-candidate-present", validation["present"], display(args.input))
        report("strict-candidate-schema-valid", validation["valid"], f"failed={validation.get('failed_checks', [])}")
        report(
            "strict-readout-combiner-valid",
            validation.get("combined_readout", {}).get("valid") is True,
            str(validation.get("combined_readout", {})),
        )
    elif args.scout:
        report("scout-candidate-built", validation["present"], "synthetic scout rows")
        report("scout-candidate-schema-valid", validation["valid"], f"failed={validation.get('failed_checks', [])}")
        report(
            "scout-readout-combiner-valid",
            validation.get("combined_readout", {}).get("valid") is True,
            str(validation.get("combined_readout", {})),
        )
    else:
        report("future-row-certificate-absent", not validation["present"], display(args.input))
        report(
            "current-mode-schema-valid-if-present",
            (not validation["present"]) or validation["valid"],
            f"failed={validation.get('failed_checks', [])}",
        )
        report(
            "current-mode-readout-not-claimed",
            not validation["present"] or validation.get("combined_readout", {}).get("valid") is True,
            str(validation.get("combined_readout", {})),
        )
    report("adversarial-shortcuts-rejected", rejections_ok, str({k: v.get("failed_checks", []) for k, v in rejections.items()}))
    if args.scout:
        report("scout-recovers-planted-yh", scout_target_ok, str(validation.get("combined_readout", {})))
    if args.strict:
        report("strict-production-certificate-passed", strict_gate_passed, f"input={display(args.input)}")
    else:
        report("strict-production-certificate-not-claimed", not strict_gate_passed, "strict mode not requested")

    result = {
        "actual_current_surface_status": (
            "scout-pass / lightweight same-source W-response readout harness"
            if args.scout and validation["valid"] and scout_target_ok
            else "strict-pass / lightweight same-source W-response production readout"
            if strict_gate_passed
            else "open / lightweight same-source W-response readout production rows absent"
        ),
        "mode": mode,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Scout mode validates the route mechanics only.  Production proposal "
            "still requires real same-source W rows plus correction authority, "
            "matching/running, and retained-route authorization."
        ),
        "bare_retained_allowed": False,
        "lightweight_readout_harness_passed": (
            validation["valid"] and rejections_ok and (not args.scout or scout_target_ok)
        ),
        "strict_lightweight_readout_gate_passed": strict_gate_passed,
        "current_lightweight_readout_gate_passed": current_gate_passed,
        "readout_formula": "y_h = g_2 R_t/(sqrt(2) R_W) - delta_perp",
        "input_certificate": display(args.input),
        "validation": validation,
        "rejection_witnesses": rejections,
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not generate W/Z production rows",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed selectors, alpha_LM, plaquette/u0, kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not set delta_perp to zero without a one-Higgs, rank-one, tomography, or Gram-purity certificate",
            "does not treat static EW algebra as a same-source W mass-response measurement",
        ],
        "exact_next_action": (
            "Run a small same-source EW/W correlator measurement that writes "
            f"{display(DEFAULT_INPUT)}, or supply a theorem certificate that "
            "sets delta_perp=0 through one-Higgs completeness / neutral rank one."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(args.output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if args.strict and not strict_gate_passed:
        return 1
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
