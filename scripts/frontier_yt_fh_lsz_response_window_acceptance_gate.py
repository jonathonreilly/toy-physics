#!/usr/bin/env python3
"""
PR #230 FH/LSZ response-window acceptance gate.

Response-window forensics found a stable tau=1 diagnostic but did not
authorize changing the load-bearing FH response readout.  This runner records
the predeclared acceptance gate for any future response-window switch and
checks the current chunks against the parts that are actually available.

The current surface has stable chunk-level source-shift effective-mass slopes
over several tau windows, but a readout switch still requires full ready-set
per-configuration multi-tau target rows, multiple source radii, and production
response stability.  Therefore the gate remains open unless all subgates pass.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, stdev
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
READY_SET = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json"
RESPONSE_STABILITY = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json"
RESPONSE_FORENSICS = ROOT / "outputs" / "yt_fh_lsz_response_window_forensics_2026-05-03.json"
FINITE_SOURCE_LINEARITY = ROOT / "outputs" / "yt_fh_lsz_finite_source_linearity_gate_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json"

TAU_WINDOW_MAX = 9
STABLE_REL_STDEV_MAX = 0.05
STABLE_SPREAD_MAX = 1.10
TAU_WINDOW_MEAN_SPREAD_MAX = 1.05
EXPECTED_SCHEMA_VERSION = "fh_lsz_target_timeseries_v2_multitau"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def chunk_path(index: int) -> Path:
    return ROOT / "outputs" / f"yt_pr230_fh_lsz_production_L12_T24_chunk{index:03d}_2026-05-01.json"


def first_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if isinstance(ensembles, list) and len(ensembles) == 1 and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def source_shift_key(value: float) -> str:
    if value == 0.0:
        return "0"
    return f"{value:g}"


def effective_energy(correlator: list[dict[str, Any]], tau: int) -> float | None:
    if tau < 0 or tau + 1 >= len(correlator):
        return None
    c0 = correlator[tau].get("mean")
    c1 = correlator[tau + 1].get("mean")
    if not finite(c0) or not finite(c1) or float(c0) <= 0.0 or float(c1) <= 0.0:
        return None
    return float(math.log(float(c0) / float(c1)))


def chunk_tau_slopes(index: int) -> dict[int, float]:
    data = load_json(chunk_path(index))
    source = first_ensemble(data).get("scalar_source_response_analysis", {})
    fits = source.get("energy_fits", [])
    by_shift = {
        source_shift_key(float(row.get("source_shift_lat"))): row
        for row in fits
        if isinstance(row, dict) and finite(row.get("source_shift_lat"))
    }
    minus = by_shift.get("-0.01")
    plus = by_shift.get("0.01")
    if not minus or not plus:
        return {}
    minus_corr = minus.get("correlator", [])
    plus_corr = plus.get("correlator", [])
    slopes: dict[int, float] = {}
    for tau in range(0, TAU_WINDOW_MAX + 1):
        e_minus = effective_energy(minus_corr, tau)
        e_plus = effective_energy(plus_corr, tau)
        if e_minus is not None and e_plus is not None:
            slopes[tau] = float((e_plus - e_minus) / 0.02)
    return slopes


def chunk_multi_tau_target_summary(index: int) -> dict[str, Any]:
    data = load_json(chunk_path(index))
    metadata = data.get("metadata", {})
    run_control = metadata.get("run_control", {}) if isinstance(metadata, dict) else {}
    source = first_ensemble(data).get("scalar_source_response_analysis", {})
    rows = source.get("per_configuration_multi_tau_slopes", []) if isinstance(source, dict) else []
    measurements = int(run_control.get("measurement_sweeps") or 16)
    finite_values = 0
    tau_keys: set[str] = set()
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            slopes = row.get("slope_effective_energy_by_tau", {})
            if not isinstance(slopes, dict):
                continue
            for key, value in slopes.items():
                tau_keys.add(str(key))
                if finite(value):
                    finite_values += 1
    schema_version = source.get("target_timeseries_schema_version") if isinstance(source, dict) else None
    present = (
        schema_version == EXPECTED_SCHEMA_VERSION
        and isinstance(rows, list)
        and len(rows) == measurements
        and finite_values > 0
    )
    return {
        "chunk_index": index,
        "schema_version": schema_version,
        "row_count": len(rows) if isinstance(rows, list) else 0,
        "expected_rows": measurements,
        "finite_multi_tau_slope_values": finite_values,
        "tau_keys": sorted(tau_keys, key=lambda value: int(value) if value.isdigit() else value),
        "multi_tau_target_rows_present": present,
    }


def summary(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"available": False}
    value_mean = mean(values)
    value_stdev = stdev(values) if len(values) > 1 else 0.0
    value_min = min(values)
    value_max = max(values)
    return {
        "available": True,
        "n": len(values),
        "mean": float(value_mean),
        "stdev": float(value_stdev),
        "relative_stdev": float(value_stdev / abs(value_mean)) if value_mean else None,
        "min": float(value_min),
        "max": float(value_max),
        "spread_ratio": float(value_max / value_min) if value_min > 0.0 else None,
        "stable_by_rule": (
            value_mean != 0.0
            and value_min > 0.0
            and value_stdev / abs(value_mean) < STABLE_REL_STDEV_MAX
            and value_max / value_min < STABLE_SPREAD_MAX
        ),
    }


def main() -> int:
    print("PR #230 FH/LSZ response-window acceptance gate")
    print("=" * 72)

    ready_set = load_json(READY_SET)
    response_stability = load_json(RESPONSE_STABILITY)
    response_forensics = load_json(RESPONSE_FORENSICS)
    finite_source_linearity = load_json(FINITE_SOURCE_LINEARITY)
    ready_indices = [
        int(index)
        for index in ready_set.get("ready_chunk_indices", [])
        if isinstance(index, int) or (isinstance(index, str) and index.isdigit())
    ]
    chunk_rows = []
    tau_values: dict[int, list[float]] = {tau: [] for tau in range(0, TAU_WINDOW_MAX + 1)}
    multi_tau_target_rows = []
    for index in ready_indices:
        slopes = chunk_tau_slopes(index)
        multi_tau_summary = chunk_multi_tau_target_summary(index)
        multi_tau_target_rows.append(multi_tau_summary)
        for tau, value in slopes.items():
            tau_values[tau].append(value)
        chunk_rows.append(
            {
                "chunk_index": index,
                "path": str(chunk_path(index).relative_to(ROOT)),
                "available_tau_windows": sorted(slopes),
                "tau_window_slopes": {str(tau): value for tau, value in sorted(slopes.items())},
                "multi_tau_target_summary": multi_tau_summary,
            }
        )
    tau_summaries = {str(tau): summary(values) for tau, values in sorted(tau_values.items())}
    available_summaries = [row for row in tau_summaries.values() if row.get("available")]
    stable_tau_windows = [
        int(tau)
        for tau, row in tau_summaries.items()
        if row.get("stable_by_rule") is True and row.get("n") == len(ready_indices)
    ]
    tau_means = [float(row["mean"]) for row in available_summaries if finite(row.get("mean"))]
    tau_mean_spread = max(tau_means) / min(tau_means) if tau_means and min(tau_means) > 0 else None

    response_stability_passed = (
        response_stability.get("stability_summary", {}).get("stability_passed") is True
    )
    response_forensics_available = (
        "response-window forensics" in response_forensics.get("actual_current_surface_status", "")
        and response_forensics.get("readout_switch_authorized") is False
    )
    tau_window_central_support = (
        bool(stable_tau_windows)
        and len(stable_tau_windows) == len(available_summaries)
        and tau_mean_spread is not None
        and tau_mean_spread < TAU_WINDOW_MEAN_SPREAD_MAX
    )

    multi_tau_ready_indices = [
        int(row["chunk_index"])
        for row in multi_tau_target_rows
        if row.get("multi_tau_target_rows_present") is True
    ]
    multi_tau_missing_indices = [
        int(row["chunk_index"])
        for row in multi_tau_target_rows
        if row.get("multi_tau_target_rows_present") is not True
    ]
    # The rows are the minimum serialized data needed to compute a same-chunk
    # multi-tau covariance.  The acceptance gate requires full ready-set
    # coverage, not just partial v2 chunks.
    per_configuration_multi_tau_covariance_present = (
        bool(ready_indices) and len(multi_tau_ready_indices) == len(ready_indices)
    )
    multiple_source_radii_present = (
        finite_source_linearity.get("finite_source_linearity_gate_passed") is True
    )
    readout_switch_authorized = (
        tau_window_central_support
        and per_configuration_multi_tau_covariance_present
        and multiple_source_radii_present
        and response_stability_passed
    )
    gate_passed = False

    report("ready-set-loaded", bool(ready_set), str(READY_SET.relative_to(ROOT)))
    report("response-stability-loaded", bool(response_stability), str(RESPONSE_STABILITY.relative_to(ROOT)))
    report("response-forensics-loaded", response_forensics_available, str(RESPONSE_FORENSICS.relative_to(ROOT)))
    report("finite-source-linearity-loaded", bool(finite_source_linearity), str(FINITE_SOURCE_LINEARITY.relative_to(ROOT)))
    report("chunk-level-tau-window-support-stable", tau_window_central_support, f"stable_tau_windows={stable_tau_windows}")
    report(
        "tau-window-mean-spread-state-recorded",
        tau_mean_spread is not None,
        f"tau_mean_spread={tau_mean_spread}",
    )
    report(
        "per-configuration-multi-tau-covariance-state-recorded",
        True,
        (
            f"complete={per_configuration_multi_tau_covariance_present}, "
            f"v2_indices={multi_tau_ready_indices}, missing={multi_tau_missing_indices}"
        ),
    )
    report(
        "multiple-source-radii-missing",
        not multiple_source_radii_present,
        "finite-source-linearity gate is not passed",
    )
    report("production-response-stability-still-open", not response_stability_passed, f"passed={response_stability_passed}")
    report("readout-switch-not-authorized", not readout_switch_authorized, f"readout_switch_authorized={readout_switch_authorized}")
    report("response-window-acceptance-gate-not-passed", not gate_passed, "acceptance gate remains open")
    report("does-not-authorize-retained-proposal", True, "response-window gate is not scalar LSZ/canonical-Higgs closure")

    result = {
        "actual_current_surface_status": "open / FH-LSZ response-window acceptance gate not passed",
        "verdict": (
            "The current chunks give stable chunk-level symmetric source-shift "
            "effective-mass slopes across tau windows 0-9, so the forensics "
            "diagnostic is reproducible beyond tau=1.  The acceptance gate still "
            "does not pass: per-configuration multi-tau target rows are not yet "
            "complete for the full ready set, the finite-source-linearity gate is "
            "not passed, and the production fitted-slope response-stability gate "
            "remains open."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No production response readout switch is authorized, and scalar "
            "LSZ/canonical-Higgs gates remain separate blockers."
        ),
        "response_window_acceptance_gate_passed": gate_passed,
        "readout_switch_authorized": readout_switch_authorized,
        "ready_chunk_indices": ready_indices,
        "tau_window_summaries": tau_summaries,
        "stable_tau_windows": stable_tau_windows,
        "tau_window_mean_spread_ratio": tau_mean_spread,
        "per_configuration_multi_tau_covariance_present": per_configuration_multi_tau_covariance_present,
        "multi_tau_target_timeseries_schema_version": EXPECTED_SCHEMA_VERSION,
        "multi_tau_ready_indices": multi_tau_ready_indices,
        "multi_tau_missing_indices": multi_tau_missing_indices,
        "multi_tau_target_rows": multi_tau_target_rows,
        "multiple_source_radii_present": multiple_source_radii_present,
        "response_stability_passed": response_stability_passed,
        "chunk_rows": chunk_rows,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not replace the production response readout",
            "does not treat chunk-level tau-window stability as covariance",
            "does not treat one source radius as the zero-source FH derivative",
            "does not set kappa_s = 1 or identify the source pole with canonical Higgs",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Complete v2 multi-tau production rows for the full ready set and run "
            "a multi-radius source-response calibration, or continue the "
            "non-source-only canonical-Higgs identity routes."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
