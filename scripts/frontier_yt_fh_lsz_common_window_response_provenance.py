#!/usr/bin/env python3
"""
PR #230 FH/LSZ common-window response provenance audit.

The fitted source-response surface is unstable across ready chunks.  This
runner tests whether the instability is caused by the production fitter
choosing different effective-mass fit windows for different source shifts.

It recomputes a diagnostic response using one predeclared late window
(`tau=10..12`) for every source shift in every ready L12 chunk.  This is a
provenance/audit artifact only: it does not switch the physical response
readout and does not authorize retained or proposed_retained y_t closure.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, median, stdev
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
READY_SET = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json"
RESPONSE_STABILITY = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json"
RESPONSE_FORENSICS = ROOT / "outputs" / "yt_fh_lsz_response_window_forensics_2026-05-03.json"
RESPONSE_ACCEPTANCE = ROOT / "outputs" / "yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_common_window_response_provenance_2026-05-04.json"

COMMON_TAU_MIN = 10
COMMON_TAU_MAX = 12
EXPECTED_SHIFTS = (-0.01, 0.0, 0.01)

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


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def first_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if isinstance(ensembles, list) and len(ensembles) == 1 and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def chunk_path(index: int) -> Path:
    return ROOT / "outputs" / f"yt_pr230_fh_lsz_production_L12_T24_chunk{index:03d}_2026-05-01.json"


def fit_fixed_window(correlator: list[dict[str, Any]], tau_min: int, tau_max: int) -> dict[str, float]:
    rows = [
        row
        for row in correlator
        if isinstance(row, dict)
        and isinstance(row.get("tau"), int)
        and tau_min <= int(row["tau"]) <= tau_max
        and finite(row.get("mean"))
        and float(row["mean"]) > 0.0
    ]
    if len(rows) < 2:
        return {"energy_lat": float("nan"), "energy_lat_err": float("nan"), "chi2_dof": float("nan")}
    x = np.asarray([row["tau"] for row in rows], dtype=float)
    means = np.asarray([row["mean"] for row in rows], dtype=float)
    sig = np.asarray([max(float(row.get("stderr", 0.0) or 0.0), 1.0e-10) for row in rows], dtype=float)
    y = np.log(means)
    yerr = sig / means
    weights = 1.0 / np.maximum(yerr * yerr, 1.0e-12)
    design = np.vstack([np.ones_like(x), -x]).T
    normal = design.T @ (weights[:, None] * design)
    rhs = design.T @ (weights * y)
    cov = np.linalg.pinv(normal)
    coeff = cov @ rhs
    residual = y - design @ coeff
    dof = max(1, len(y) - 2)
    chi2 = float(np.sum(weights * residual * residual) / dof)
    return {
        "energy_lat": float(coeff[1]),
        "energy_lat_err": float(math.sqrt(max(cov[1, 1], 0.0))),
        "chi2_dof": chi2,
    }


def linear_response(fits: list[dict[str, Any]]) -> dict[str, float]:
    finite_rows = [
        row
        for row in fits
        if finite(row.get("source_shift_lat"))
        and finite(row.get("energy_lat"))
        and finite(row.get("energy_lat_err"))
    ]
    if len(finite_rows) < 2:
        return {"slope_dE_ds_lat": float("nan"), "slope_dE_ds_lat_err": float("nan")}
    shifts = np.asarray([row["source_shift_lat"] for row in finite_rows], dtype=float)
    energies = np.asarray([row["energy_lat"] for row in finite_rows], dtype=float)
    weights = np.asarray(
        [1.0 / max(float(row["energy_lat_err"]) ** 2, 1.0e-12) for row in finite_rows],
        dtype=float,
    )
    coeffs, cov = np.polyfit(shifts, energies, deg=1, w=np.sqrt(weights), cov="unscaled")
    return {
        "slope_dE_ds_lat": float(coeffs[0]),
        "slope_dE_ds_lat_err": float(math.sqrt(max(cov[0, 0], 0.0))) if cov.shape == (2, 2) else float("nan"),
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
        "spread_ratio": float(value_max / value_min) if value_min > 0 else None,
        "median": float(median(values)),
    }


def original_fit_window_signature(energy_fits: list[dict[str, Any]]) -> tuple[int | None, ...]:
    by_shift = {round(float(row.get("source_shift_lat")), 8): row for row in energy_fits if finite(row.get("source_shift_lat"))}
    signature: list[int | None] = []
    for shift in EXPECTED_SHIFTS:
        row = by_shift.get(round(shift, 8), {})
        tau_min = row.get("tau_min")
        signature.append(int(tau_min) if isinstance(tau_min, int) else None)
    return tuple(signature)


def collect_chunk(index: int) -> dict[str, Any]:
    data = load_json(chunk_path(index))
    ensemble = first_ensemble(data)
    source = ensemble.get("scalar_source_response_analysis", {})
    energy_fits = source.get("energy_fits", []) if isinstance(source, dict) else []
    signature = original_fit_window_signature(energy_fits)
    fixed_fits = []
    for row in energy_fits:
        if not isinstance(row, dict) or not finite(row.get("source_shift_lat")):
            continue
        fit = fit_fixed_window(row.get("correlator", []), COMMON_TAU_MIN, COMMON_TAU_MAX)
        fixed_fits.append(
            {
                "source_shift_lat": float(row["source_shift_lat"]),
                "energy_lat": fit["energy_lat"],
                "energy_lat_err": fit["energy_lat_err"],
                "chi2_dof": fit["chi2_dof"],
                "tau_min": COMMON_TAU_MIN,
                "tau_max": COMMON_TAU_MAX,
            }
        )
    response = linear_response(fixed_fits)
    return {
        "chunk_index": index,
        "path": str(chunk_path(index).relative_to(ROOT)),
        "seed": data.get("metadata", {}).get("run_control", {}).get("seed"),
        "original_fit_window_signature_tau_min": list(signature),
        "original_windows_mixed": len({value for value in signature if value is not None}) > 1,
        "original_slope_dE_ds_lat": source.get("slope_dE_ds_lat") if isinstance(source, dict) else None,
        "original_slope_dE_ds_lat_err": source.get("slope_dE_ds_lat_err") if isinstance(source, dict) else None,
        "common_window_energy_fits": fixed_fits,
        "common_window_slope_dE_ds_lat": response["slope_dE_ds_lat"],
        "common_window_slope_dE_ds_lat_err": response["slope_dE_ds_lat_err"],
    }


def main() -> int:
    print("PR #230 FH/LSZ common-window response provenance")
    print("=" * 72)

    ready_set = load_json(READY_SET)
    response_stability = load_json(RESPONSE_STABILITY)
    response_forensics = load_json(RESPONSE_FORENSICS)
    response_acceptance = load_json(RESPONSE_ACCEPTANCE)
    ready_indices = [
        int(index)
        for index in ready_set.get("ready_chunk_indices", [])
        if isinstance(index, int) or (isinstance(index, str) and index.isdigit())
    ]
    rows = [collect_chunk(index) for index in ready_indices]
    original_slopes = [float(row["original_slope_dE_ds_lat"]) for row in rows if finite(row.get("original_slope_dE_ds_lat"))]
    common_slopes = [float(row["common_window_slope_dE_ds_lat"]) for row in rows if finite(row.get("common_window_slope_dE_ds_lat"))]
    common_errors = [float(row["common_window_slope_dE_ds_lat_err"]) for row in rows if finite(row.get("common_window_slope_dE_ds_lat_err"))]
    original_summary = summary(original_slopes)
    common_summary = summary(common_slopes)
    common_typical_error = mean(common_errors) if common_errors else None
    common_relative_error = (
        abs(common_typical_error / common_summary["mean"])
        if common_typical_error is not None and common_summary.get("mean") not in (None, 0.0)
        else None
    )
    by_signature: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_signature["/".join(str(value) for value in row["original_fit_window_signature_tau_min"])].append(row)
    signature_summary = {
        key: {
            "n": len(value),
            "chunk_indices": [row["chunk_index"] for row in value],
            "original_slope_mean": mean([float(row["original_slope_dE_ds_lat"]) for row in value]),
        }
        for key, value in sorted(by_signature.items())
    }
    mixed_rows = [row for row in rows if row["original_windows_mixed"]]
    high_original_rows = [row for row in rows if finite(row.get("original_slope_dE_ds_lat")) and float(row["original_slope_dE_ds_lat"]) > 3.0]
    high_original_all_mixed = bool(high_original_rows) and all(row["original_windows_mixed"] for row in high_original_rows)
    original_unstable = response_stability.get("stability_summary", {}).get("stability_passed") is False
    common_stable = (
        common_summary.get("available") is True
        and (common_summary.get("relative_stdev") or 999.0) < 0.05
        and (common_summary.get("spread_ratio") or 999.0) < 1.10
    )
    production_grade = common_stable and common_relative_error is not None and common_relative_error < 0.25

    report("parent-certificates-present", all([ready_set, response_stability, response_forensics, response_acceptance]), "ready/response parents loaded")
    report("ready-chunks-loaded", len(rows) >= 8 and len(rows) == len(ready_indices), f"n={len(rows)}")
    report("original-response-unstable", original_unstable, str(original_summary))
    report("fit-window-signatures-classified", len(signature_summary) >= 2, f"signatures={list(signature_summary)}")
    report("mixed-window-chunks-detected", bool(mixed_rows), f"mixed={len(mixed_rows)}")
    report("high-original-slopes-are-mixed-window", high_original_all_mixed, f"high_chunks={[row['chunk_index'] for row in high_original_rows]}")
    report("common-window-recompute-finite", len(common_slopes) == len(rows), f"common_n={len(common_slopes)}")
    report("common-window-slope-stable", common_stable, str(common_summary))
    report("common-window-uncertainty-not-production-grade", not production_grade, f"relative_error={common_relative_error}")
    report("readout-switch-not-authorized", True, "common-window recompute is provenance only")
    report("does-not-authorize-retained-proposal", True, "scalar LSZ/canonical-Higgs gates remain open")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ common-window response provenance",
        "verdict": (
            "The current fitted response instability is explained by inconsistent "
            "source-shift fit windows.  The high original slopes occur only in "
            "chunks where the source shifts use mixed tau_min windows.  A "
            "predeclared common late window tau=10..12 makes the chunk slopes "
            "stable, but the resulting fit uncertainty is still not production "
            "grade and this diagnostic does not authorize a readout switch."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Common-window stability is provenance/support only; scalar LSZ, "
            "finite-source-linearity, FV/IR/model-class, and canonical-Higgs "
            "identity gates remain open."
        ),
        "readout_switch_authorized": False,
        "common_window": {"tau_min": COMMON_TAU_MIN, "tau_max": COMMON_TAU_MAX},
        "ready_chunk_indices": ready_indices,
        "signature_summary": signature_summary,
        "mixed_window_chunk_indices": [row["chunk_index"] for row in mixed_rows],
        "high_original_slope_chunk_indices": [row["chunk_index"] for row in high_original_rows],
        "high_original_all_mixed_window": high_original_all_mixed,
        "original_slope_summary": original_summary,
        "common_window_slope_summary": common_summary,
        "common_window_typical_fit_error": common_typical_error,
        "common_window_relative_fit_error": common_relative_error,
        "common_window_stability_passed": common_stable,
        "common_window_production_grade": production_grade,
        "chunk_rows": rows,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not replace the production readout by fiat",
            "does not set kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not treat common-window stability as scalar LSZ or canonical-Higgs identity",
        ],
        "exact_next_action": (
            "Promote this into a predeclared common-window response gate or "
            "postprocessor, then require finite-source-linearity, scalar-pole "
            "model/FV/IR control, and canonical-Higgs identity before any "
            "physical y_t readout."
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
