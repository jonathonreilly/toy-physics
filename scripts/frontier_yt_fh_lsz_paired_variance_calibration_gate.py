#!/usr/bin/env python3
"""
PR #230 FH/LSZ paired x8/x16 variance calibration gate.

The eight-mode pole-fit lane can only trade scalar-LSZ stochastic noises for
momentum shells if a same-source production calibration shows that x8 and x16
give stable C_ss(q), Gamma_ss(q), and pole-proxy rows.  This runner consumes
the paired calibration manifest and records whether the calibration outputs are
absent, present-but-unstable, or accepted as launch support.

It is not a physical y_t readout and never authorizes retained wording.
"""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outputs" / "yt_fh_lsz_variance_calibration_manifest_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_paired_variance_calibration_gate_2026-05-04.json"

EXPECTED_MODE_KEYS = {
    "0,0,0",
    "1,0,0",
    "1,1,0",
    "1,1,1",
    "2,0,0",
    "2,1,0",
    "2,1,1",
    "2,2,0",
}
EXPECTED_LABELS = {"x8": 8, "x16": 16}
MIN_CONFIGS = 16
MAX_ROW_Z = 4.0
MAX_CSS_RELATIVE_DELTA = 0.03
MAX_GAMMA_RELATIVE_DELTA = 0.03
MAX_NOISE_HALF_DELTA_OVER_STDERR = 6.0

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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def manifest_commands(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in manifest.get("commands", []):
        if isinstance(row, dict) and row.get("label") in EXPECTED_LABELS:
            rows[str(row["label"])] = row
    return rows


def first_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles", [])
    if isinstance(ensembles, list) and ensembles and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def scalar_rows(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    analysis = first_ensemble(data).get("scalar_two_point_lsz_analysis", {})
    rows = analysis.get("mode_rows", {}) if isinstance(analysis, dict) else {}
    return {str(k): v for k, v in rows.items() if isinstance(v, dict)}


def scalar_meta(data: dict[str, Any]) -> dict[str, Any]:
    meta = data.get("metadata", {}).get("scalar_two_point_lsz", {})
    return meta if isinstance(meta, dict) else {}


def run_control(data: dict[str, Any]) -> dict[str, Any]:
    control = data.get("metadata", {}).get("run_control", {})
    return control if isinstance(control, dict) else {}


def series_stderr(row: dict[str, Any], field: str) -> float:
    values = [
        float(item[field])
        for item in row.get("C_ss_timeseries", [])
        if isinstance(item, dict) and field in item and math.isfinite(float(item[field]))
    ]
    if len(values) < 2:
        return float("nan")
    return statistics.stdev(values) / math.sqrt(len(values))


def combined_z(a: float, ea: float, b: float, eb: float) -> float:
    denom = math.hypot(ea, eb)
    if denom <= 0.0 or not math.isfinite(denom):
        return float("inf")
    return abs(a - b) / denom


def relative_delta(a: float, b: float) -> float:
    denom = max(abs(a), abs(b), 1.0e-300)
    return abs(a - b) / denom


def row_value(row: dict[str, Any], key: str) -> float:
    try:
        return float(row.get(key, float("nan")))
    except (TypeError, ValueError):
        return float("nan")


def validate_output(label: str, command: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
    expected_noises = EXPECTED_LABELS[label]
    path = ROOT / str(command.get("output", ""))
    if not data:
        return {
            "label": label,
            "path": rel(path),
            "exists": False,
            "ready": False,
            "issues": ["output absent"],
        }

    metadata = data.get("metadata", {}) if isinstance(data.get("metadata", {}), dict) else {}
    control = run_control(data)
    meta = scalar_meta(data)
    rows = scalar_rows(data)
    mode_keys = set(rows)
    config_counts = [
        int(row.get("configuration_count", 0))
        for row in rows.values()
        if isinstance(row, dict)
    ]
    half_delta_values = [
        row_value(row.get("noise_subsample_stability", {}), "C_ss_real_half_delta_over_stderr_max")
        for row in rows.values()
        if isinstance(row.get("noise_subsample_stability", {}), dict)
    ]
    finite_half_delta = [value for value in half_delta_values if math.isfinite(value)]
    issues: list[str] = []

    if metadata.get("phase") != "production":
        issues.append(f"phase={metadata.get('phase')!r}")
    if control.get("production_targets") is not True:
        issues.append("production_targets is not true")
    if control.get("scalar_two_point_noises") != expected_noises:
        issues.append(
            f"run_control.scalar_two_point_noises={control.get('scalar_two_point_noises')!r}"
        )
    if meta.get("noise_vectors_per_configuration") != expected_noises:
        issues.append(
            "metadata.scalar_two_point_lsz.noise_vectors_per_configuration="
            f"{meta.get('noise_vectors_per_configuration')!r}"
        )
    missing_modes = sorted(EXPECTED_MODE_KEYS - mode_keys)
    extra_modes = sorted(mode_keys - EXPECTED_MODE_KEYS)
    if missing_modes:
        issues.append(f"missing_modes={missing_modes}")
    if extra_modes:
        issues.append(f"extra_modes={extra_modes}")
    min_configs = min(config_counts) if config_counts else 0
    if min_configs < MIN_CONFIGS:
        issues.append(f"configuration_count_min={min_configs}")
    if not finite_half_delta:
        issues.append("noise_subsample_stability absent")
    elif max(finite_half_delta) > MAX_NOISE_HALF_DELTA_OVER_STDERR:
        issues.append(f"noise_half_delta_over_stderr_max={max(finite_half_delta):.6g}")

    return {
        "label": label,
        "path": rel(path),
        "exists": True,
        "ready": not issues,
        "phase": metadata.get("phase"),
        "run_control": control,
        "noise_vectors_per_configuration": meta.get("noise_vectors_per_configuration"),
        "mode_keys": sorted(mode_keys),
        "configuration_count_min": min_configs,
        "noise_half_delta_over_stderr_max": max(finite_half_delta) if finite_half_delta else None,
        "issues": issues,
    }


def comparable_run_controls(x8: dict[str, Any], x16: dict[str, Any]) -> dict[str, Any]:
    allowed_differences = {"scalar_two_point_noises", "production_output_dir"}
    left = dict(x8)
    right = dict(x16)
    keys = sorted(set(left) | set(right))
    differences = [
        key
        for key in keys
        if key not in allowed_differences and left.get(key) != right.get(key)
    ]
    return {
        "matched": not differences,
        "allowed_differences": sorted(allowed_differences),
        "unexpected_differences": differences,
    }


def slope_proxy(rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    points: list[tuple[float, float]] = []
    for row in rows.values():
        p2 = row_value(row, "p_hat_sq")
        gamma = row_value(row, "Gamma_ss_real")
        if math.isfinite(p2) and math.isfinite(gamma):
            points.append((p2, gamma))
    if len(points) < 2:
        return {"available": False, "reason": "fewer than two finite points"}
    mean_x = statistics.fmean(p[0] for p in points)
    mean_y = statistics.fmean(p[1] for p in points)
    denom = sum((x - mean_x) ** 2 for x, _ in points)
    if denom <= 0.0:
        return {"available": False, "reason": "zero p_hat_sq variance"}
    slope = sum((x - mean_x) * (y - mean_y) for x, y in points) / denom
    intercept = mean_y - slope * mean_x
    return {"available": True, "slope": slope, "intercept": intercept, "point_count": len(points)}


def compare_outputs(x8_data: dict[str, Any], x16_data: dict[str, Any]) -> dict[str, Any]:
    rows8 = scalar_rows(x8_data)
    rows16 = scalar_rows(x16_data)
    row_comparisons = []
    css_z_values: list[float] = []
    gamma_z_values: list[float] = []
    css_rel_values: list[float] = []
    gamma_rel_values: list[float] = []

    for mode in sorted(EXPECTED_MODE_KEYS):
        row8 = rows8.get(mode, {})
        row16 = rows16.get(mode, {})
        c8 = row_value(row8, "C_ss_real")
        c16 = row_value(row16, "C_ss_real")
        c8_err = row_value(row8, "C_ss_real_config_stderr")
        c16_err = row_value(row16, "C_ss_real_config_stderr")
        g8 = row_value(row8, "Gamma_ss_real")
        g16 = row_value(row16, "Gamma_ss_real")
        g8_err = series_stderr(row8, "Gamma_ss_real")
        g16_err = series_stderr(row16, "Gamma_ss_real")
        css_z = combined_z(c8, c8_err, c16, c16_err)
        gamma_z = combined_z(g8, g8_err, g16, g16_err)
        css_rel = relative_delta(c8, c16)
        gamma_rel = relative_delta(g8, g16)
        css_z_values.append(css_z)
        gamma_z_values.append(gamma_z)
        css_rel_values.append(css_rel)
        gamma_rel_values.append(gamma_rel)
        row_comparisons.append(
            {
                "mode": mode,
                "C_ss_real_x8": c8,
                "C_ss_real_x16": c16,
                "C_ss_real_combined_z": css_z,
                "C_ss_real_relative_delta": css_rel,
                "Gamma_ss_real_x8": g8,
                "Gamma_ss_real_x16": g16,
                "Gamma_ss_real_combined_z": gamma_z,
                "Gamma_ss_real_relative_delta": gamma_rel,
            }
        )

    finite_css_z = [value for value in css_z_values if math.isfinite(value)]
    finite_gamma_z = [value for value in gamma_z_values if math.isfinite(value)]
    slope8 = slope_proxy(rows8)
    slope16 = slope_proxy(rows16)
    slope_rel = (
        relative_delta(float(slope8["slope"]), float(slope16["slope"]))
        if slope8.get("available") and slope16.get("available")
        else float("nan")
    )
    stable = (
        len(finite_css_z) == len(EXPECTED_MODE_KEYS)
        and len(finite_gamma_z) == len(EXPECTED_MODE_KEYS)
        and max(finite_css_z) <= MAX_ROW_Z
        and max(finite_gamma_z) <= MAX_ROW_Z
        and max(css_rel_values) <= MAX_CSS_RELATIVE_DELTA
        and max(gamma_rel_values) <= MAX_GAMMA_RELATIVE_DELTA
    )
    return {
        "stable": stable,
        "thresholds": {
            "max_row_z": MAX_ROW_Z,
            "max_C_ss_relative_delta": MAX_CSS_RELATIVE_DELTA,
            "max_Gamma_ss_relative_delta": MAX_GAMMA_RELATIVE_DELTA,
            "max_noise_half_delta_over_stderr": MAX_NOISE_HALF_DELTA_OVER_STDERR,
        },
        "max_C_ss_real_combined_z": max(finite_css_z) if finite_css_z else None,
        "max_Gamma_ss_real_combined_z": max(finite_gamma_z) if finite_gamma_z else None,
        "max_C_ss_real_relative_delta": max(css_rel_values) if css_rel_values else None,
        "max_Gamma_ss_real_relative_delta": max(gamma_rel_values) if gamma_rel_values else None,
        "slope_proxy_x8": slope8,
        "slope_proxy_x16": slope16,
        "slope_proxy_relative_delta": slope_rel,
        "row_comparisons": row_comparisons,
    }


def main() -> int:
    print("PR #230 FH/LSZ paired x8/x16 variance calibration gate")
    print("=" * 72)

    manifest = load_json(MANIFEST)
    commands = manifest_commands(manifest)
    missing_labels = sorted(set(EXPECTED_LABELS) - set(commands))
    data = {
        label: load_json(ROOT / str(command.get("output", "")))
        for label, command in commands.items()
    }
    validations = {
        label: validate_output(label, command, data.get(label, {}))
        for label, command in commands.items()
    }
    outputs_present = all(validations.get(label, {}).get("exists") for label in EXPECTED_LABELS)
    outputs_ready = all(validations.get(label, {}).get("ready") for label in EXPECTED_LABELS)
    control_match = (
        comparable_run_controls(
            validations["x8"].get("run_control", {}),
            validations["x16"].get("run_control", {}),
        )
        if outputs_present and "x8" in validations and "x16" in validations
        else {"matched": False, "unexpected_differences": ["outputs absent"]}
    )
    comparison = (
        compare_outputs(data["x8"], data["x16"])
        if outputs_ready and control_match.get("matched") is True
        else {"stable": False, "reason": "paired outputs absent, invalid, or run controls unmatched"}
    )
    gate_passed = outputs_ready and control_match.get("matched") is True and comparison.get("stable") is True

    report("manifest-present", bool(manifest), rel(MANIFEST))
    report("manifest-has-x8-x16-commands", not missing_labels, f"missing_labels={missing_labels}")
    report("paired-output-state-recorded", True, f"present={outputs_present}")
    report(
        "x8-output-absent-or-valid",
        "x8" in validations and (not validations["x8"].get("exists") or validations["x8"].get("ready")),
        "; ".join(validations.get("x8", {}).get("issues", [])),
    )
    report(
        "x16-output-absent-or-valid",
        "x16" in validations and (not validations["x16"].get("exists") or validations["x16"].get("ready")),
        "; ".join(validations.get("x16", {}).get("issues", [])),
    )
    report(
        "run-control-match-when-present",
        not outputs_present or control_match.get("matched") is True,
        f"unexpected_differences={control_match.get('unexpected_differences')}",
    )
    report(
        "paired-stability-accepted-or-awaiting-data",
        not outputs_present or comparison.get("stable") is True,
        f"stable={comparison.get('stable')}",
    )
    report("not-retained-closure", True, "variance calibration is launch support, not physical y_t evidence")

    status = (
        "bounded-support / paired x8/x16 variance calibration passed as launch support"
        if gate_passed
        else "open / paired x8/x16 variance calibration awaiting production outputs"
        if not outputs_present
        else "open / paired x8/x16 variance calibration not accepted"
    )
    result = {
        "actual_current_surface_status": status,
        "verdict": (
            "The paired x8/x16 calibration outputs are absent, so the x8 "
            "noise reduction remains unaccepted."
            if not outputs_present
            else (
                "The paired x8/x16 calibration outputs satisfy the same-source "
                "run-control, eight-mode, stochastic stability, and row-stability "
                "checks.  This accepts x8 only as pole-fit launch support."
                if gate_passed
                else (
                    "The paired x8/x16 calibration outputs are present but do "
                    "not satisfy the same-source variance acceptance checks.  "
                    "The pole-fit lane must keep x16 noise or collect a new "
                    "calibration."
                )
            )
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Variance calibration does not derive scalar LSZ normalization or physical y_t.",
        "variance_calibration_gate_passed": gate_passed,
        "x8_noise_reduction_accepted_for_polefit_launch": gate_passed,
        "eight_mode_x8_launch_allowed_as_retained_evidence": False,
        "manifest": rel(MANIFEST),
        "validations": validations,
        "run_control_match": control_match,
        "comparison": comparison,
        "acceptance_requirements": [
            "both manifest x8 and x16 outputs complete as production phase",
            "run controls match except scalar_two_point_noises and artifact directory",
            "both outputs expose exactly the eight pole-fit scalar-LSZ modes",
            "each mode has at least 16 configurations and noise-subsample diagnostics",
            "C_ss(q) and Gamma_ss(q) agree within the recorded z and relative-delta thresholds",
            "accepted x8 is launch support only and does not close model-class, FV/IR, or O_H identity gates",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s, c2, Z_match, or cos(theta) to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not combine four-mode chunks with eight-mode calibration as one homogeneous ensemble",
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
