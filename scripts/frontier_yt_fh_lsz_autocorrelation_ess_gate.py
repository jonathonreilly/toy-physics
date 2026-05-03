#!/usr/bin/env python3
"""
PR #230 FH/LSZ autocorrelation and effective-sample-size gate.

Completed chunks cannot become production evidence until autocorrelation and
effective sample size are certified for the load-bearing observables.  This
runner checks the current ready chunk surface and records the target time-series
coverage requirement.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
READY_SET = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json"
RESPONSE_STABILITY = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json"
COMBINER = ROOT / "outputs" / "yt_fh_lsz_chunk_combiner_gate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json"

MIN_READY_CHUNKS_FOR_GATE = 8
MIN_TARGET_ESS_PER_VOLUME = 200.0

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


def first_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if isinstance(ensembles, list) and len(ensembles) == 1 and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def chunk_path(index: int) -> Path:
    return ROOT / "outputs" / f"yt_pr230_fh_lsz_production_L12_T24_chunk{index:03d}_2026-05-01.json"


def autocorrelation_tau_int(values: list[float], max_lag: int = 100) -> dict[str, Any]:
    n = len(values)
    if n < 8:
        return {"available": False, "n": n}
    mu = mean(values)
    centered = [x - mu for x in values]
    var = sum(x * x for x in centered) / n
    if var <= 0.0:
        return {"available": False, "n": n, "reason": "zero variance"}
    lag_limit = min(max_lag, n // 2)
    rho_values = []
    tau = 0.5
    window_lag = 0
    for lag in range(1, lag_limit + 1):
        cov = sum(centered[i] * centered[i + lag] for i in range(n - lag)) / (n - lag)
        rho = cov / var
        rho_values.append(rho)
        if rho <= 0.0:
            window_lag = lag
            break
        tau += rho
        window_lag = lag
    ess = n / max(2.0 * tau, 1.0)
    return {
        "available": True,
        "n": n,
        "tau_int_initial_positive": tau,
        "ess_initial_positive": ess,
        "window_lag": window_lag,
        "rho_first_lags": rho_values[:8],
    }


def has_target_timeseries(ensemble: dict[str, Any]) -> dict[str, bool]:
    source = ensemble.get("scalar_source_response_analysis")
    lsz = ensemble.get("scalar_two_point_lsz_analysis")
    source_measurements_present = False
    lsz_measurements_present = False
    if isinstance(source, dict):
        source_measurements_present = any(
            key in source
            for key in (
                "per_configuration_slopes",
                "source_response_measurements",
                "energy_fit_timeseries",
            )
        )
    if isinstance(lsz, dict):
        rows = lsz.get("mode_rows", {})
        if isinstance(rows, dict):
            lsz_measurements_present = any(
                isinstance(row, dict)
                and any(
                    key in row
                    for key in (
                        "per_configuration_C_ss",
                        "C_ss_timeseries",
                        "Gamma_ss_timeseries",
                    )
                )
                for row in rows.values()
            )
    return {
        "source_response_target_timeseries": source_measurements_present,
        "scalar_lsz_target_timeseries": lsz_measurements_present,
    }


def chunk_row(index: int) -> dict[str, Any]:
    data = load_json(chunk_path(index))
    ensemble = first_ensemble(data)
    metadata = data.get("metadata", {})
    history = [
        float(x)
        for x in ensemble.get("plaquette_history", [])
        if finite(x)
    ]
    # Keep the post-thermalized tail when thermalization metadata is available.
    thermalization = int(ensemble.get("thermalization_sweeps", 0) or 0)
    tail = history[thermalization:] if thermalization and len(history) > thermalization + 8 else history
    target_series = has_target_timeseries(ensemble)
    return {
        "chunk_index": index,
        "path": str(chunk_path(index).relative_to(ROOT)),
        "phase": metadata.get("phase"),
        "plaquette_history_count": len(history),
        "plaquette_tail_count": len(tail),
        "plaquette_tau_int": autocorrelation_tau_int(tail),
        "target_timeseries": target_series,
        "target_timeseries_complete": all(target_series.values()),
    }


def main() -> int:
    print("PR #230 FH/LSZ autocorrelation ESS gate")
    print("=" * 72)

    ready_set = load_json(READY_SET)
    response_stability = load_json(RESPONSE_STABILITY)
    combiner = load_json(COMBINER)
    ready_indices = [
        int(index)
        for index in ready_set.get("ready_chunk_indices", [])
        if isinstance(index, int) or (isinstance(index, str) and index.isdigit())
    ]
    rows = [chunk_row(index) for index in ready_indices]
    target_series_complete = bool(rows) and all(row["target_timeseries_complete"] for row in rows)
    target_complete_indices = [
        int(row["chunk_index"])
        for row in rows
        if row.get("target_timeseries_complete") is True
    ]
    target_incomplete_indices = [
        int(row["chunk_index"])
        for row in rows
        if row.get("target_timeseries_complete") is not True
    ]
    plaquette_ess_values = [
        float(row["plaquette_tau_int"].get("ess_initial_positive"))
        for row in rows
        if finite(row.get("plaquette_tau_int", {}).get("ess_initial_positive"))
    ]
    min_plaquette_ess = min(plaquette_ess_values) if plaquette_ess_values else None
    target_ess_available = False
    autocorrelation_gate_passed = False

    report("ready-set-loaded", bool(ready_set), str(READY_SET.relative_to(ROOT)))
    report("response-stability-loaded", bool(response_stability), str(RESPONSE_STABILITY.relative_to(ROOT)))
    report("combiner-gate-loaded", bool(combiner), str(COMBINER.relative_to(ROOT)))
    ready_count_reaches_threshold = len(ready_indices) >= MIN_READY_CHUNKS_FOR_GATE
    report(
        "ready-chunk-count-threshold-state-recorded",
        True,
        (
            f"ready_chunks={ready_indices}, "
            f"threshold={MIN_READY_CHUNKS_FOR_GATE}, "
            f"threshold_reached={ready_count_reaches_threshold}"
        ),
    )
    report(
        "plaquette-autocorrelation-diagnostic-available",
        len(plaquette_ess_values) == len(rows) and len(rows) > 0,
        f"min_plaquette_ess={min_plaquette_ess}",
    )
    report(
        "target-timeseries-coverage-state-recorded",
        True,
        (
            f"complete={target_series_complete}, "
            f"complete_indices={target_complete_indices}, "
            f"incomplete_indices={target_incomplete_indices}"
        ),
    )
    report(
        "target-ess-not-available",
        not target_ess_available,
        (
            "target time series are still incomplete for the ready set"
            if not target_series_complete
            else "target time series are complete for the ready set, but no predeclared target blocking/bootstrap ESS certificate is available"
        ),
    )
    report(
        "autocorrelation-ess-gate-not-passed",
        not autocorrelation_gate_passed,
        "target ESS cannot be certified from current outputs",
    )
    report(
        "does-not-authorize-production-evidence",
        combiner.get("proposal_allowed") is False
        and response_stability.get("proposal_allowed") is False,
        "combiner and response-stability gates remain non-evidence",
    )
    report("does-not-authorize-retained-proposal", True, "scalar LSZ and canonical-Higgs identity still open")

    complete_label = ", ".join(f"chunk{index:03d}" for index in target_complete_indices) or "none"
    incomplete_label = ", ".join(f"chunk{index:03d}" for index in target_incomplete_indices) or "none"
    result = {
        "actual_current_surface_status": "open / FH-LSZ autocorrelation ESS gate not passed",
        "verdict": (
            "The current ready chunks include plaquette histories, so a "
            "diagnostic plaquette autocorrelation can be estimated.  Target-series "
            f"coverage state: complete={complete_label}; incomplete={incomplete_label}.  "
            "The load-bearing FH/LSZ target effective sample size still cannot be "
            "certified for the ready set until target-observable blocking/bootstrap "
            "data or an equivalent autocorrelation certificate is available for the "
            "production set."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Target-observable autocorrelation and effective sample size are not certified.",
        "autocorrelation_ess_gate_passed": autocorrelation_gate_passed,
        "ready_chunk_indices": ready_indices,
        "ready_count_reaches_threshold": ready_count_reaches_threshold,
        "target_timeseries_summary": {
            "complete_for_all_ready_chunks": target_series_complete,
            "complete_indices": target_complete_indices,
            "incomplete_indices": target_incomplete_indices,
            "complete_count": len(target_complete_indices),
            "ready_count": len(rows),
        },
        "chunk_rows": rows,
        "gate_requirements": {
            "minimum_ready_chunks_for_gate": MIN_READY_CHUNKS_FOR_GATE,
            "minimum_target_ess_per_volume": MIN_TARGET_ESS_PER_VOLUME,
            "required_target_timeseries": [
                "per-configuration dE/ds or source-response energy samples",
                "per-configuration C_ss(q) or Gamma_ss(q) samples for accepted modes",
            ],
            "acceptable_alternative": "predeclared blocking/bootstrap certificate emitted by the production harness",
        },
        "strict_non_claims": [
            "does not treat plaquette ESS as target FH/LSZ ESS",
            "does not treat current chunks as production evidence",
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
        ],
        "exact_next_action": (
            "Continue future chunks with target time-series serialization, "
            "rerun or replace older chunks if target ESS is required for the "
            "ready set, or emit a predeclared blocking/bootstrap certificate; "
            "then rerun this gate before using chunked FH/LSZ output as "
            "production evidence."
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
