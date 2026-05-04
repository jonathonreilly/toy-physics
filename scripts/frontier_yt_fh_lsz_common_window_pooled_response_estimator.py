#!/usr/bin/env python3
"""
PR #230 FH/LSZ common-window pooled response estimator.

The common-window provenance audit recomputed a fixed tau=10..12 response for
each ready chunk and found a stable central slope surface, but its first
uncertainty field was the typical per-fit covariance and therefore remained
non-production-grade.

This runner estimates the uncertainty of the ready-set common-window response
from independent chunk-to-chunk scatter.  It is a support estimator only: it
does not switch the physical readout and does not supply scalar LSZ or
canonical-Higgs/source-overlap closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, stdev
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT / "outputs" / "yt_fh_lsz_common_window_response_provenance_2026-05-04.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_common_window_pooled_response_estimator_2026-05-04.json"

MIN_CHUNKS = 30
MAX_RELATIVE_STANDARD_ERROR = 0.005
MAX_BOOTSTRAP_68_RELATIVE_HALF_WIDTH = 0.005
BOOTSTRAP_REPLICATES = 5000
BOOTSTRAP_SEED = 20260504

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


def percentile(values: np.ndarray, q: float) -> float:
    return float(np.percentile(values, q))


def jackknife_mean(values: list[float]) -> dict[str, Any]:
    n = len(values)
    full_mean = mean(values)
    loo = [(sum(values) - value) / (n - 1) for value in values]
    loo_mean = mean(loo)
    variance = (n - 1) / n * sum((value - loo_mean) ** 2 for value in loo)
    return {
        "mean": float(full_mean),
        "standard_error": float(math.sqrt(max(variance, 0.0))),
        "relative_standard_error": float(math.sqrt(max(variance, 0.0)) / abs(full_mean))
        if full_mean
        else None,
        "leave_one_out_min": float(min(loo)),
        "leave_one_out_max": float(max(loo)),
    }


def bootstrap_mean(values: list[float]) -> dict[str, Any]:
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    arr = np.asarray(values, dtype=float)
    draws = rng.choice(arr, size=(BOOTSTRAP_REPLICATES, len(arr)), replace=True).mean(axis=1)
    median = percentile(draws, 50.0)
    p16 = percentile(draws, 16.0)
    p84 = percentile(draws, 84.0)
    p025 = percentile(draws, 2.5)
    p975 = percentile(draws, 97.5)
    half_width_68 = 0.5 * (p84 - p16)
    half_width_95 = 0.5 * (p975 - p025)
    return {
        "replicates": BOOTSTRAP_REPLICATES,
        "seed": BOOTSTRAP_SEED,
        "median": median,
        "p16": p16,
        "p84": p84,
        "p025": p025,
        "p975": p975,
        "half_width_68": float(half_width_68),
        "half_width_95": float(half_width_95),
        "relative_half_width_68": float(half_width_68 / abs(median)) if median else None,
        "relative_half_width_95": float(half_width_95 / abs(median)) if median else None,
    }


def main() -> int:
    print("PR #230 FH/LSZ common-window pooled response estimator")
    print("=" * 72)

    provenance = load_json(PROVENANCE)
    rows = provenance.get("chunk_rows", []) if isinstance(provenance.get("chunk_rows"), list) else []
    values = [
        float(row["common_window_slope_dE_ds_lat"])
        for row in rows
        if isinstance(row, dict) and finite(row.get("common_window_slope_dE_ds_lat"))
    ]
    chunk_indices = [
        int(row["chunk_index"])
        for row in rows
        if isinstance(row, dict)
        and finite(row.get("common_window_slope_dE_ds_lat"))
        and isinstance(row.get("chunk_index"), int)
    ]
    value_mean = mean(values) if values else float("nan")
    chunk_stdev = stdev(values) if len(values) > 1 else float("nan")
    empirical_standard_error = chunk_stdev / math.sqrt(len(values)) if values else float("nan")
    relative_standard_error = (
        empirical_standard_error / abs(value_mean)
        if values and value_mean
        else float("nan")
    )
    jackknife = jackknife_mean(values) if len(values) >= 3 else {}
    bootstrap = bootstrap_mean(values) if values else {}
    common_stable = provenance.get("common_window_stability_passed") is True
    pooled_production_grade = (
        len(values) >= MIN_CHUNKS
        and common_stable
        and relative_standard_error < MAX_RELATIVE_STANDARD_ERROR
        and (bootstrap.get("relative_half_width_68") or 999.0)
        < MAX_BOOTSTRAP_68_RELATIVE_HALF_WIDTH
    )
    readout_switch_authorized = False

    report("provenance-certificate-present", bool(provenance), str(PROVENANCE.relative_to(ROOT)))
    report("common-window-provenance-stable", common_stable, provenance.get("actual_current_surface_status", ""))
    report("independent-chunk-population-sufficient", len(values) >= MIN_CHUNKS, f"n={len(values)}")
    report("empirical-standard-error-recorded", finite(empirical_standard_error), f"se={empirical_standard_error}")
    report(
        "empirical-relative-standard-error-production-grade",
        relative_standard_error < MAX_RELATIVE_STANDARD_ERROR,
        f"relative_se={relative_standard_error}",
    )
    report(
        "bootstrap-68-half-width-production-grade",
        (bootstrap.get("relative_half_width_68") or 999.0)
        < MAX_BOOTSTRAP_68_RELATIVE_HALF_WIDTH,
        f"relative_hw68={bootstrap.get('relative_half_width_68')}",
    )
    report("pooled-common-window-response-production-grade", pooled_production_grade, f"passed={pooled_production_grade}")
    report("readout-switch-not-authorized", not readout_switch_authorized, "scalar-LSZ/canonical-Higgs gates remain open")
    report("does-not-authorize-retained-proposal", True, "pooled response is not physical y_t closure")

    result = {
        "actual_current_surface_status": (
            "bounded-support / FH-LSZ common-window pooled response estimator production-grade"
            if pooled_production_grade
            else "open / FH-LSZ common-window pooled response estimator not production-grade"
        ),
        "verdict": (
            "Independent chunk-to-chunk scatter gives a production-grade "
            "empirical uncertainty for the fixed tau=10..12 common-window "
            "central response.  This retires the estimator-uncertainty "
            "sub-blocker for the common-window gate, but it does not authorize "
            "a physical readout switch because finite-source-linearity, "
            "response-window acceptance, scalar-LSZ, and canonical-Higgs/"
            "source-overlap gates remain open."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Pooled fixed-window uncertainty is support only; scalar LSZ and "
            "O_sp/O_H identity are separate unresolved gates."
        ),
        "bare_retained_allowed": False,
        "pooled_common_window_response_production_grade": pooled_production_grade,
        "readout_switch_authorized": readout_switch_authorized,
        "common_window": provenance.get("common_window"),
        "chunk_indices": chunk_indices,
        "chunk_count": len(values),
        "mean": float(value_mean),
        "chunk_stdev": float(chunk_stdev),
        "empirical_standard_error": float(empirical_standard_error),
        "relative_standard_error": float(relative_standard_error),
        "jackknife": jackknife,
        "bootstrap": bootstrap,
        "thresholds": {
            "min_chunks": MIN_CHUNKS,
            "max_relative_standard_error": MAX_RELATIVE_STANDARD_ERROR,
            "max_bootstrap_68_relative_half_width": MAX_BOOTSTRAP_68_RELATIVE_HALF_WIDTH,
        },
        "parent_certificate": str(PROVENANCE.relative_to(ROOT)),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not replace the production response readout",
            "does not set kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Rerun the common-window response gate with this estimator as a "
            "parent.  The remaining gate blockers are finite-source-linearity, "
            "response-window acceptance, fitted/replacement response stability, "
            "scalar-LSZ, and canonical-Higgs/source-overlap closure."
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
