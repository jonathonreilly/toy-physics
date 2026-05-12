#!/usr/bin/env python3
"""
PR #230 FH/LSZ ready chunk response-stability diagnostic.

This runner checks the same-source dE/ds slopes in the current seed-controlled
ready L12 chunk set.  It is a production diagnostic only.  A stable slope would
still need the scalar LSZ/canonical-Higgs gates before physical y_t closure;
an unstable complete or partial L12 set blocks using the current ready chunks
as anything stronger than bounded support.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, stdev
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
READY_SET = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json"
EXPECTED_SOURCE_SHIFTS = {-0.01, 0.0, 0.01}

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


def chunk_response_row(index: int) -> dict[str, Any]:
    chunk = load_json(chunk_path(index))
    metadata = chunk.get("metadata", {})
    ensemble = first_ensemble(chunk)
    source = ensemble.get("scalar_source_response_analysis", {})
    energy_fits = source.get("energy_fits", []) if isinstance(source, dict) else []
    source_shifts = {
        round(float(row.get("source_shift_lat")), 8)
        for row in energy_fits
        if isinstance(row, dict) and finite(row.get("source_shift_lat"))
    }
    mass_fit = ensemble.get("mass_fit", {})
    return {
        "chunk_index": index,
        "path": str(chunk_path(index).relative_to(ROOT)),
        "phase": metadata.get("phase"),
        "seed": metadata.get("run_control", {}).get("seed") if isinstance(metadata, dict) else None,
        "slope_dE_ds_lat": source.get("slope_dE_ds_lat") if isinstance(source, dict) else None,
        "slope_dE_ds_lat_err": source.get("slope_dE_ds_lat_err") if isinstance(source, dict) else None,
        "mass_fit_m_lat": mass_fit.get("m_lat") if isinstance(mass_fit, dict) else None,
        "source_shifts": sorted(source_shifts),
        "ready": (
            metadata.get("phase") == "production"
            and finite(source.get("slope_dE_ds_lat") if isinstance(source, dict) else None)
            and finite(source.get("slope_dE_ds_lat_err") if isinstance(source, dict) else None)
            and source_shifts == {round(x, 8) for x in EXPECTED_SOURCE_SHIFTS}
        ),
    }


def main() -> int:
    print("PR #230 FH/LSZ ready chunk response-stability diagnostic")
    print("=" * 72)

    ready_set = load_json(READY_SET)
    ready_summary = ready_set.get("chunk_summary", {}) if isinstance(ready_set.get("chunk_summary"), dict) else {}
    expected_chunks = int(ready_summary.get("expected_chunks", 63))
    complete_l12 = len(ready_set.get("ready_chunk_indices", [])) >= expected_chunks > 0
    ready_indices = [
        int(index)
        for index in ready_set.get("ready_chunk_indices", [])
        if isinstance(index, int) or (isinstance(index, str) and index.isdigit())
    ]
    rows = [chunk_response_row(index) for index in ready_indices]
    slopes = [float(row["slope_dE_ds_lat"]) for row in rows if finite(row.get("slope_dE_ds_lat"))]
    errors = [float(row["slope_dE_ds_lat_err"]) for row in rows if finite(row.get("slope_dE_ds_lat_err"))]
    slope_mean = mean(slopes) if slopes else None
    slope_stdev = stdev(slopes) if len(slopes) > 1 else 0.0
    relative_stdev = abs(slope_stdev / slope_mean) if slope_mean not in (None, 0.0) else None
    min_slope = min(slopes) if slopes else None
    max_slope = max(slopes) if slopes else None
    spread_ratio = abs(max_slope / min_slope) if min_slope not in (None, 0.0) else None
    typical_fit_error = mean(errors) if errors else None
    relative_fit_error = abs(typical_fit_error / slope_mean) if slope_mean not in (None, 0.0) else None
    stability_passed = (
        len(slopes) >= 8
        and relative_stdev is not None
        and relative_stdev < 0.25
        and spread_ratio is not None
        and spread_ratio < 2.0
    )
    set_label = "complete L12 set" if complete_l12 else f"{len(slopes)}/{expected_chunks} partial L12 set"

    report("ready-set-certificate-present", bool(ready_set), str(READY_SET.relative_to(ROOT)))
    report("ready-chunks-loaded", len(rows) >= 4 and all(row["ready"] for row in rows), f"ready_indices={ready_indices}")
    report("finite-source-slopes", len(slopes) == len(rows) and len(slopes) >= 4, f"slopes={slopes}")
    report(
        "ready-set-stability-not-passed",
        not stability_passed,
        f"relative_stdev={relative_stdev}, spread_ratio={spread_ratio}, n={len(slopes)}",
    )
    report(
        "response-uncertainty-not-production-grade",
        relative_fit_error is not None
        and relative_stdev is not None
        and (relative_fit_error > 0.25 or relative_stdev > 0.25),
        f"relative_fit_error={relative_fit_error}, relative_stdev={relative_stdev}",
    )
    report("does-not-authorize-retained-proposal", True, "response stability is diagnostic, not scalar LSZ/canonical-Higgs closure")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ ready chunk response-stability diagnostic",
        "verdict": (
            "The current seed-controlled ready chunks expose same-source dE/ds, "
            f"but the {set_label} is not stable enough to use as production "
            "response evidence beyond bounded support.  The chunk slopes are "
            "finite but have large chunk-to-chunk spread.  Even a stable slope "
            "would still require scalar LSZ pole derivative, model-class/FV/IR "
            "control, and canonical-Higgs identity before physical y_t closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The ready L12 set response stability is not passed; scalar LSZ/canonical-Higgs gates remain open.",
        "ready_set_certificate": str(READY_SET.relative_to(ROOT)),
        "response_rows": rows,
        "stability_summary": {
            "n_chunks": len(slopes),
            "slope_mean": slope_mean,
            "slope_stdev": slope_stdev,
            "relative_stdev": relative_stdev,
            "min_slope": min_slope,
            "max_slope": max_slope,
            "spread_ratio": spread_ratio,
            "typical_fit_error": typical_fit_error,
            "relative_fit_error": relative_fit_error,
            "stability_acceptance_rule": "n>=8, relative_stdev<0.25, spread_ratio<2",
            "stability_passed": stability_passed,
        },
        "strict_non_claims": [
            "does not treat dE/ds as physical dE/dh",
            "does not set kappa_s = 1",
            "does not use observed top mass, observed y_t, H_unit, Ward authority, alpha_LM, plaquette, or u0",
            "does not treat an L12-only ready set as production closure",
        ],
        "exact_next_action": (
            "Do not relitigate L12 chunk completeness.  Either improve the "
            "response-stability estimator with a justified same-surface method "
            "or continue the canonical-Higgs identity / same-source W/Z "
            "response route."
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
