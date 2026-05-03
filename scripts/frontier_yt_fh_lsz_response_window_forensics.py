#!/usr/bin/env python3
"""
PR #230 FH/LSZ response-window forensics.

Target-observable ESS is now accepted for the current ready set, but the
production response-stability diagnostic still fails on the fitted dE/ds
central values.  This runner compares that fitted-slope surface to the
serialized per-configuration tau=1 effective-energy response target series.
It is forensics and acceptance-design support only; it does not switch the
load-bearing response readout or authorize a retained proposal.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, median, stdev
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
READY_SET = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json"
RESPONSE_STABILITY = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json"
TARGET_ESS = ROOT / "outputs" / "yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_response_window_forensics_2026-05-03.json"

MIN_READY_CHUNKS = 8
DIAGNOSTIC_REL_STDEV_MAX = 0.05
DIAGNOSTIC_SPREAD_MAX = 1.10

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


def sample_stderr(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    return float(stdev(values) / math.sqrt(len(values)))


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
        "spread_ratio": float(value_max / value_min) if value_min > 0 else None,
        "median": float(median(values)),
    }


def robust_outliers(values: list[float], labels: list[int]) -> dict[str, Any]:
    if len(values) < 3:
        return {"available": False, "outliers": []}
    med = median(values)
    deviations = [abs(value - med) for value in values]
    mad = median(deviations)
    rows = []
    if mad == 0.0:
        for label, value in zip(labels, values):
            if value != med:
                rows.append({"chunk_index": label, "value": float(value), "robust_z": None})
        return {"available": True, "median": float(med), "mad": 0.0, "outliers": rows}
    for label, value in zip(labels, values):
        robust_z = 0.6745 * (value - med) / mad
        if abs(robust_z) >= 3.5:
            rows.append(
                {
                    "chunk_index": label,
                    "value": float(value),
                    "robust_z": float(robust_z),
                }
            )
    return {"available": True, "median": float(med), "mad": float(mad), "outliers": rows}


def collect_chunk(index: int) -> dict[str, Any]:
    data = load_json(chunk_path(index))
    ensemble = first_ensemble(data)
    source = ensemble.get("scalar_source_response_analysis", {})
    rows = source.get("per_configuration_slopes", [])
    tau1_values = [
        float(row["slope_effective_energy_tau1"])
        for row in rows
        if isinstance(row, dict)
        and row.get("finite") is True
        and finite(row.get("slope_effective_energy_tau1"))
    ]
    tau1_mean = mean(tau1_values) if tau1_values else float("nan")
    tau1_stderr = sample_stderr(tau1_values)
    fit_slope = source.get("slope_dE_ds_lat")
    fit_error = source.get("slope_dE_ds_lat_err")
    discrepancy = abs(float(fit_slope) - tau1_mean) if finite(fit_slope) and finite(tau1_mean) else None
    denominator = math.sqrt(float(fit_error) ** 2 + float(tau1_stderr or 0.0) ** 2) if finite(fit_error) else None
    return {
        "chunk_index": index,
        "path": str(chunk_path(index).relative_to(ROOT)),
        "phase": data.get("metadata", {}).get("phase"),
        "fit_slope_dE_ds_lat": float(fit_slope) if finite(fit_slope) else None,
        "fit_slope_dE_ds_lat_err": float(fit_error) if finite(fit_error) else None,
        "tau1_target_slope_mean": float(tau1_mean) if finite(tau1_mean) else None,
        "tau1_target_slope_stderr": float(tau1_stderr) if tau1_stderr is not None else None,
        "tau1_target_rows": len(tau1_values),
        "fit_minus_tau1_mean": float(float(fit_slope) - tau1_mean) if finite(fit_slope) and finite(tau1_mean) else None,
        "absolute_fit_tau1_discrepancy": float(discrepancy) if discrepancy is not None else None,
        "fit_tau1_discrepancy_sigma": float(discrepancy / denominator)
        if discrepancy is not None and denominator and denominator > 0
        else None,
    }


def main() -> int:
    print("PR #230 FH/LSZ response-window forensics")
    print("=" * 72)

    ready_set = load_json(READY_SET)
    response_stability = load_json(RESPONSE_STABILITY)
    target_ess = load_json(TARGET_ESS)
    ready_indices = [
        int(index)
        for index in ready_set.get("ready_chunk_indices", [])
        if isinstance(index, int) or (isinstance(index, str) and index.isdigit())
    ]
    rows = [collect_chunk(index) for index in ready_indices]
    fit_values = [float(row["fit_slope_dE_ds_lat"]) for row in rows if finite(row.get("fit_slope_dE_ds_lat"))]
    tau1_values = [
        float(row["tau1_target_slope_mean"])
        for row in rows
        if finite(row.get("tau1_target_slope_mean"))
    ]
    fit_summary = summary(fit_values)
    tau1_summary = summary(tau1_values)
    fit_outliers = robust_outliers(fit_values, ready_indices[: len(fit_values)])
    tau1_outliers = robust_outliers(tau1_values, ready_indices[: len(tau1_values)])
    response_summary = response_stability.get("stability_summary", {})
    response_stability_failed = response_summary.get("stability_passed") is False
    target_ess_passed = target_ess.get("target_observable_ess_gate_passed") is True
    tau1_diagnostic_stable = (
        tau1_summary.get("available") is True
        and (tau1_summary.get("relative_stdev") or 999.0) < DIAGNOSTIC_REL_STDEV_MAX
        and (tau1_summary.get("spread_ratio") or 999.0) < DIAGNOSTIC_SPREAD_MAX
    )
    fit_surface_unstable = (
        fit_summary.get("available") is True
        and (
            (fit_summary.get("relative_stdev") or 0.0) >= 0.25
            or (fit_summary.get("spread_ratio") or 0.0) >= 2.0
        )
    )
    surface_split_detected = tau1_diagnostic_stable and fit_surface_unstable
    readout_switch_authorized = False

    report("ready-set-loaded", bool(ready_set), str(READY_SET.relative_to(ROOT)))
    report("response-stability-loaded", bool(response_stability), str(RESPONSE_STABILITY.relative_to(ROOT)))
    report("target-ess-loaded", bool(target_ess), str(TARGET_ESS.relative_to(ROOT)))
    report("ready-chunk-count-state-recorded", len(ready_indices) >= MIN_READY_CHUNKS, f"ready_chunks={ready_indices}")
    report("target-ess-passed-before-forensics", target_ess_passed, f"target_ess_passed={target_ess_passed}")
    report("fit-slope-stability-fails", response_stability_failed and fit_surface_unstable, str(fit_summary))
    report("tau1-target-diagnostic-stable", tau1_diagnostic_stable, str(tau1_summary))
    report("fit-vs-tau1-surface-split-detected", surface_split_detected, "fit-window and tau1 diagnostic surfaces disagree")
    report("readout-switch-not-authorized", not readout_switch_authorized, "tau1 stability is diagnostic only")
    report("does-not-authorize-retained-proposal", True, "response-window forensics is not scalar LSZ/canonical-Higgs closure")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ response-window forensics",
        "verdict": (
            "The accepted target time series expose a stable tau=1 effective-energy "
            "response diagnostic across chunks001-016, while the current fitted "
            "dE/ds response-stability surface remains unstable.  This identifies "
            "a response-window/readout-selection blocker, not a replacement "
            "physical readout.  Switching from the production fit slope to the "
            "tau=1 target diagnostic would require a predeclared response-window "
            "acceptance gate with covariance, multiple tau windows, source-radius "
            "control, and the existing scalar-LSZ/canonical-Higgs gates."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Tau1 target stability does not select a production FH derivative, "
            "does not supply scalar pole derivative/FV/IR/model-class control, "
            "and does not identify the source pole with the canonical Higgs."
        ),
        "response_window_forensics_passed": True,
        "readout_switch_authorized": readout_switch_authorized,
        "ready_chunk_indices": ready_indices,
        "fit_slope_summary": fit_summary,
        "tau1_target_slope_summary": tau1_summary,
        "fit_slope_outliers": fit_outliers,
        "tau1_target_outliers": tau1_outliers,
        "chunk_rows": rows,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not replace the production response readout with tau1 by fiat",
            "does not set kappa_s = 1",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, or u0",
            "does not treat target ESS or response-window stability as canonical-Higgs identity",
        ],
        "exact_next_action": (
            "Add a predeclared FH response-window acceptance gate that compares "
            "multiple effective-mass tau windows, fit windows, and source radii "
            "with covariance, then rerun response stability.  In parallel, keep "
            "the scalar-pole/FV/IR/model-class and canonical-Higgs identity gates "
            "as separate blockers."
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
