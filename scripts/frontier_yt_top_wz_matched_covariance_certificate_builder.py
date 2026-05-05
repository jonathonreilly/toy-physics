#!/usr/bin/env python3
"""
PR #230 matched top/W covariance certificate builder.

The same-source top-response certificate needs a covariance between the top
source response and the W/Z source response on a matched configuration set.
This runner defines that input contract.  It can compute the covariance from
future paired rows, but on the current surface it remains open because no W/Z
matched response rows exist.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import fmean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROWS_INPUT = ROOT / "outputs" / "yt_top_wz_matched_response_rows_2026-05-04.json"
DEFAULT_COVARIANCE_OUTPUT = ROOT / "outputs" / "yt_top_wz_matched_covariance_certificate_2026-05-04.json"
DEFAULT_STATUS_OUTPUT = ROOT / "outputs" / "yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json"
SCOUT_COVARIANCE_OUTPUT = ROOT / "outputs" / "yt_top_wz_matched_covariance_certificate_builder_scout_certificate_2026-05-04.json"
SCOUT_STATUS_OUTPUT = ROOT / "outputs" / "yt_top_wz_matched_covariance_certificate_builder_scout_2026-05-04.json"

PARENTS = {
    "common_window_response_gate": "outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json",
    "wz_mass_fit_path_gate": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "same_source_top_response_identity_builder": "outputs/yt_same_source_top_response_identity_certificate_builder_2026-05-04.json",
}

FIREWALL_FALSE_FIELDS = (
    "used_observed_top_or_yukawa_as_selector",
    "used_observed_WZ_masses_as_selector",
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


def paired_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows = data.get("matched_response_rows", data.get("rows", []))
    return rows if isinstance(rows, list) else []


def numeric_pair(row: dict[str, Any]) -> tuple[float, float] | None:
    top = row.get("dE_top_ds", row.get("top_response", {}).get("dE_top_ds"))
    w = row.get("dM_W_ds", row.get("w_response", {}).get("dM_W_ds"))
    if not finite(w):
        w = row.get("dM_Z_ds", row.get("z_response", {}).get("dM_Z_ds"))
    if finite(top) and finite(w):
        return float(top), float(w)
    return None


def covariance(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2:
        return float("nan")
    mx = fmean(xs)
    my = fmean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)


def validate_rows(data: dict[str, Any], *, require_production: bool) -> dict[str, Any]:
    if not data:
        return {"present": False, "valid": False, "failed_checks": ["matched top/W response rows absent"]}
    rows = paired_rows(data)
    pairs = [pair for row in rows if (pair := numeric_pair(row)) is not None]
    xs = [pair[0] for pair in pairs]
    ys = [pair[1] for pair in pairs]
    firewall = data.get("firewall", {})
    phase = data.get("phase")
    computed_cov = covariance(xs, ys) if len(xs) >= 2 else data.get("cov_dE_top_dM_W")
    checks = {
        "phase_allowed": phase in {"scout", "production"},
        "production_phase_if_required": phase == "production" if require_production else True,
        "same_source_coordinate": data.get("same_source_coordinate") is True,
        "matched_configuration_set": data.get("matched_configuration_set") is True,
        "wz_mass_fits_from_correlators": data.get("wz_mass_fits_from_correlators") is True,
        "has_three_or_more_pairs": len(pairs) >= 3,
        "finite_covariance": finite(computed_cov),
        "finite_top_mean": finite(fmean(xs)) if xs else False,
        "finite_w_mean": finite(fmean(ys)) if ys else False,
        "no_observed_top_or_yukawa_selector": firewall.get("used_observed_top_or_yukawa_as_selector") is False,
        "no_observed_wz_selector": firewall.get("used_observed_WZ_masses_as_selector") is False,
        "no_hunit_or_ward": firewall.get("used_H_unit_or_Ward_authority") is False,
        "no_alpha_lm_plaquette_or_u0": firewall.get("used_alpha_lm_plaquette_or_u0") is False,
        "no_c2_or_zmatch_by_fiat": firewall.get("used_c2_or_zmatch_equal_one") is False,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
        "pair_count": len(pairs),
        "mean_dE_top_ds": fmean(xs) if xs else None,
        "mean_dM_W_ds": fmean(ys) if ys else None,
        "cov_dE_top_dM_W": computed_cov,
    }


def build_certificate(validation: dict[str, Any], *, phase: str) -> dict[str, Any]:
    return {
        "certificate_kind": "top_wz_matched_covariance",
        "phase": phase,
        "same_source_coordinate": True,
        "matched_configuration_set": True,
        "wz_mass_fits_from_correlators": True,
        "pair_count": validation["pair_count"],
        "mean_dE_top_ds": validation["mean_dE_top_ds"],
        "mean_dM_W_ds": validation["mean_dM_W_ds"],
        "cov_dE_top_dM_W": validation["cov_dE_top_dM_W"],
        "certificate": "matched top/W covariance certificate",
        "firewall": {field: False for field in FIREWALL_FALSE_FIELDS},
        "proposal_allowed": False,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use observed W/Z/top/y_t selectors",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette, or u0",
            "does not set c2=1, Z_match=1, kappa_s=1, or k_top/k_gauge=1",
        ],
    }


def synthetic_rows() -> dict[str, Any]:
    rows = []
    for idx, (top, w) in enumerate(
        [
            (1.421, 0.512),
            (1.425, 0.517),
            (1.429, 0.521),
            (1.423, 0.515),
        ]
    ):
        rows.append({"configuration_id": f"scout-{idx}", "dE_top_ds": top, "dM_W_ds": w})
    return {
        "phase": "scout",
        "same_source_coordinate": True,
        "matched_configuration_set": True,
        "wz_mass_fits_from_correlators": True,
        "matched_response_rows": rows,
        "firewall": {field: False for field in FIREWALL_FALSE_FIELDS},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows-input", type=Path, default=DEFAULT_ROWS_INPUT)
    parser.add_argument("--covariance-output", type=Path, default=DEFAULT_COVARIANCE_OUTPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_STATUS_OUTPUT)
    parser.add_argument("--scout", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mode = "strict" if args.strict else "scout" if args.scout else "current"
    status_output = SCOUT_STATUS_OUTPUT if args.scout and args.output == DEFAULT_STATUS_OUTPUT else args.output
    covariance_output = (
        SCOUT_COVARIANCE_OUTPUT
        if args.scout and args.covariance_output == DEFAULT_COVARIANCE_OUTPUT
        else args.covariance_output
    )

    print("PR #230 matched top/W covariance certificate builder")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    parent_statuses = {name: status(cert) for name, cert in parents.items()}

    data = synthetic_rows() if args.scout else load_json(args.rows_input)
    validation = validate_rows(data, require_production=args.strict)
    scout_gate_passed = args.scout and validation["valid"] and not missing_parents
    strict_gate_passed = args.strict and validation["valid"] and not missing_parents
    current_gate_passed = False

    certificate_written = False
    covariance_certificate: dict[str, Any] = {}
    if scout_gate_passed or strict_gate_passed:
        covariance_certificate = build_certificate(
            validation,
            phase="scout" if args.scout else "production",
        )
        covariance_output.parent.mkdir(parents=True, exist_ok=True)
        covariance_output.write_text(
            json.dumps(covariance_certificate, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        certificate_written = True

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("top-response-support-present", "common-window response" in parent_statuses["common_window_response_gate"], parent_statuses["common_window_response_gate"])
    report("wz-mass-fit-path-currently-absent", "WZ correlator mass-fit path absent" in parent_statuses["wz_mass_fit_path_gate"], parent_statuses["wz_mass_fit_path_gate"])
    report("top-response-identity-builder-currently-open", "same-source top-response identity" in parent_statuses["same_source_top_response_identity_builder"], parent_statuses["same_source_top_response_identity_builder"])
    if args.scout:
        report("scout-matched-rows-valid", validation["valid"], str(validation.get("failed_checks", [])))
        report("scout-covariance-certificate-written", certificate_written, display(covariance_output))
    elif args.strict:
        report("strict-matched-rows-valid", validation["valid"], str(validation.get("failed_checks", [])))
        report("strict-covariance-certificate-written", certificate_written, display(covariance_output))
    else:
        report("future-matched-response-rows-absent", not validation["present"], display(args.rows_input))
        report("current-mode-does-not-write-covariance-certificate", not certificate_written, display(DEFAULT_COVARIANCE_OUTPUT))
    report("strict-covariance-certificate-not-claimed" if not args.strict else "strict-covariance-certificate-passed", not strict_gate_passed if not args.strict else strict_gate_passed, f"strict_gate_passed={strict_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "scout-pass / matched top-W covariance certificate builder"
            if scout_gate_passed
            else "strict-pass / matched top-W covariance certificate built"
            if strict_gate_passed
            else "open / matched top-W response rows absent"
        ),
        "mode": mode,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The builder only certifies covariance from matched response rows; "
            "it does not authorize a physical y_t readout or retained proposal."
        ),
        "bare_retained_allowed": False,
        "top_wz_matched_covariance_builder_passed": scout_gate_passed or strict_gate_passed,
        "strict_top_wz_matched_covariance_builder_passed": strict_gate_passed,
        "covariance_certificate_written": certificate_written,
        "covariance_certificate_output": display(covariance_output),
        "rows_input": display(args.rows_input),
        "row_validation": validation,
        "covariance_certificate": covariance_certificate,
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use observed W/Z/top/y_t selectors",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette, or u0",
            "does not set c2=1, Z_match=1, kappa_s=1, or k_top/k_gauge=1",
        ],
        "exact_next_action": (
            f"Produce {display(DEFAULT_ROWS_INPUT)} from matched same-source "
            "top and W/Z response measurements, then rerun this builder in "
            f"strict mode to emit {display(DEFAULT_COVARIANCE_OUTPUT)}."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    status_output.parent.mkdir(parents=True, exist_ok=True)
    status_output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote status certificate: {display(status_output)}")
    if certificate_written:
        print(f"Wrote covariance certificate: {display(covariance_output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if args.strict and not strict_gate_passed:
        return 1
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
