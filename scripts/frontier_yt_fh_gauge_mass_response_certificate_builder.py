#!/usr/bin/env python3
"""
Build/validate a PR #230 same-source W/Z mass-response certificate.

This is the executable input contract for the physical-response bypass.  It
does not manufacture W/Z data.  When future measurement rows exist, it checks
that W/Z masses were fit under the same scalar source used for dE_top/ds,
computes the gauge-normalized response ratio, and writes the candidate
certificate consumed by frontier_yt_same_source_wz_response_certificate_gate.py.
With no measurement rows present, it records the route as open.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json"
DEFAULT_OUTPUT = ROOT / "outputs" / "yt_fh_gauge_mass_response_certificate_2026-05-02.json"
STATUS_OUTPUT = ROOT / "outputs" / "yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json"

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


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def validate_measurement_input(data: dict[str, Any]) -> tuple[dict[str, bool], list[str]]:
    response = data.get("gauge_response", {})
    top = data.get("top_response", {})
    identity = data.get("identity_certificates", {})
    firewall = data.get("firewall", {})
    ew = data.get("electroweak_coupling", {})
    source_shifts = data.get("source_shifts", [])
    has_w_slope = finite(response.get("slope_dM_W_ds"))
    has_z_slope = finite(response.get("slope_dM_Z_ds"))
    checks = {
        "production_phase": data.get("phase") == "production",
        "same_source_coordinate": data.get("same_source_coordinate") is True,
        "has_source_coordinate": isinstance(data.get("source_coordinate"), str)
        and bool(data.get("source_coordinate")),
        "three_source_shifts": isinstance(source_shifts, list) and len(source_shifts) >= 3,
        "wz_mass_fits_from_correlators": data.get("wz_mass_fits_from_correlators") is True,
        "finite_top_slope": finite(top.get("slope_dE_top_ds")),
        "finite_top_slope_error": finite(top.get("slope_error")),
        "finite_w_or_z_slope": has_w_slope or has_z_slope,
        "finite_w_or_z_slope_error": finite(response.get("slope_error")),
        "top_wz_covariance": finite(response.get("cov_dE_top_dM_W"))
        or finite(response.get("cov_dE_top_dM_Z")),
        "finite_g2": finite(ew.get("g2")),
        "g2_certificate_present": isinstance(ew.get("g2_certificate"), str)
        and bool(ew.get("g2_certificate")),
        "sector_overlap_identity_passed": identity.get("same_source_sector_overlap_identity_passed") is True,
        "canonical_higgs_identity_passed": identity.get("canonical_higgs_pole_identity_passed") is True,
        "retained_route_gate_passed": identity.get("retained_route_or_proposal_gate_passed") is True,
        "no_observed_wz_selector": firewall.get("used_observed_WZ_masses_as_selector") is False,
        "no_observed_top_or_yt_selector": firewall.get("used_observed_top_or_yukawa_as_selector") is False,
        "no_static_v_selector": firewall.get("used_static_v_overlap_selector") is False,
        "no_hunit_or_ward": firewall.get("used_H_unit_or_Ward_authority") is False,
        "no_alpha_lm_plaquette_or_u0": firewall.get("used_alpha_lm_plaquette_or_u0") is False,
        "no_c2_or_zmatch_by_fiat": firewall.get("used_c2_or_zmatch_equal_one") is False,
        "no_observed_g2_selector": ew.get("used_observed_g2_as_selector") is False,
    }
    return checks, [key for key, ok in checks.items() if not ok]


def compute_ratio(data: dict[str, Any]) -> dict[str, Any]:
    top = data.get("top_response", {})
    response = data.get("gauge_response", {})
    ew = data.get("electroweak_coupling", {})
    g2 = float(ew["g2"])
    top_slope = float(top["slope_dE_top_ds"])
    if finite(response.get("slope_dM_W_ds")):
        gauge_slope = float(response["slope_dM_W_ds"])
        channel = "W"
        formula = "y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)"
    else:
        gauge_slope = float(response["slope_dM_Z_ds"])
        channel = "Z"
        formula = "Z-channel response recorded as a cross-check; W-channel physical-response ratio still preferred"
    ratio = g2 * top_slope / (math.sqrt(2.0) * gauge_slope) if gauge_slope != 0.0 else float("nan")
    return {
        "channel": channel,
        "formula": formula,
        "g2": g2,
        "slope_dE_top_ds": top_slope,
        "gauge_slope": gauge_slope,
        "gauge_normalized_yukawa_ratio": ratio,
        "strict_limit": (
            "This ratio is support only until production W/Z mass fits, sector-overlap, "
            "canonical-Higgs identity, and retained-route gates pass."
        ),
    }


def build_candidate(data: dict[str, Any], input_path: Path) -> tuple[dict[str, Any], dict[str, bool], list[str]]:
    checks, missing = validate_measurement_input(data)
    ratio = compute_ratio(data) if checks["finite_top_slope"] and checks["finite_w_or_z_slope"] and checks["finite_g2"] else {}
    firewall = data.get("firewall", {})
    ew = data.get("electroweak_coupling", {})
    candidate = {
        "metadata": {
            "artifact": "same_source_wz_response_candidate",
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "input_rows": display(input_path),
            "claim_boundary": "support_only_until_retained_route_gate_passes",
        },
        "phase": data.get("phase"),
        "same_source_coordinate": data.get("same_source_coordinate"),
        "source_coordinate": data.get("source_coordinate"),
        "source_shifts": data.get("source_shifts"),
        "wz_mass_fits_from_correlators": data.get("wz_mass_fits_from_correlators"),
        "top_response": data.get("top_response", {}),
        "gauge_response": data.get("gauge_response", {}),
        "electroweak_coupling": {
            "g2": ew.get("g2"),
            "g2_certificate": ew.get("g2_certificate"),
            "used_observed_g2_as_selector": ew.get("used_observed_g2_as_selector"),
        },
        "identity_certificates": data.get("identity_certificates", {}),
        "firewall": {
            "used_observed_WZ_masses_as_selector": firewall.get("used_observed_WZ_masses_as_selector"),
            "used_observed_top_or_yukawa_as_selector": firewall.get("used_observed_top_or_yukawa_as_selector"),
            "used_static_v_overlap_selector": firewall.get("used_static_v_overlap_selector"),
            "used_H_unit_or_Ward_authority": firewall.get("used_H_unit_or_Ward_authority"),
            "used_alpha_lm_plaquette_or_u0": firewall.get("used_alpha_lm_plaquette_or_u0"),
            "used_c2_or_zmatch_equal_one": firewall.get("used_c2_or_zmatch_equal_one"),
        },
        "gauge_normalized_response": ratio,
        "candidate_checks": checks,
        "candidate_missing_or_failed_checks": missing,
        "proposal_allowed": False,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not manufacture W/Z mass fits or source-response rows",
            "does not use observed W/Z, top, or y_t values as proof selectors",
            "does not set kappa_s, k_top/k_gauge, c2, or Z_match by fiat",
            "does not use H_unit matrix-element readout or yt_ward_identity",
        ],
    }
    return candidate, checks, missing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--status-output", type=Path, default=STATUS_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("PR #230 same-source W/Z mass-response certificate builder")
    print("=" * 72)

    data = load_json(args.input)
    input_present = bool(data)
    candidate_written = False
    checks: dict[str, bool] = {}
    missing: list[str] = []

    report("measurement-row-input-state-recorded", True, f"present={input_present}")
    if input_present:
        candidate, checks, missing = build_candidate(data, args.input)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        candidate_written = True
        report("candidate-certificate-written", True, display(args.output))
        report("candidate-schema-complete", not missing, f"missing_or_failed={missing}")
    else:
        report("measurement-row-input-absent", True, display(args.input))

    status = {
        "actual_current_surface_status": (
            "open / same-source WZ response rows absent"
            if not input_present
            else "bounded-support / same-source WZ response candidate certificate built"
        ),
        "verdict": (
            "No same-source W/Z mass-response measurement rows are present, so "
            "no candidate response certificate was written."
            if not input_present
            else (
                "A same-source W/Z response candidate certificate was written. "
                "It remains support only and must be evaluated by the W/Z "
                "response gate and retained-route gate."
            )
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Builder output is support only; retained-route gate remains authoritative.",
        "input_rows": display(args.input),
        "candidate_output": display(args.output),
        "input_present": input_present,
        "candidate_written": candidate_written,
        "candidate_checks": checks,
        "candidate_missing_or_failed_checks": missing,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not manufacture W/Z response data",
            "does not treat static EW algebra or observed masses as dM_W/ds",
            "does not set kappa_s = 1, k_top = k_gauge, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Produce production same-source W/Z mass-response rows with top "
            "response covariance and identity certificates, rerun this builder, "
            "then rerun the same-source W/Z response gate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    args.status_output.parent.mkdir(parents=True, exist_ok=True)
    args.status_output.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote status certificate: {display(args.status_output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
