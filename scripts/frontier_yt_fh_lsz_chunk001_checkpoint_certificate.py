#!/usr/bin/env python3
"""
PR #230 FH/LSZ chunk001 production checkpoint certificate.

This runner audits the historical L12_T24 chunk001 output from the chunked
FH/LSZ production plan.  It records that a production-format chunk exists, but
the numba seed-independence audit demotes it from independent evidence until it
is rerun under the patched seed-control harness or excluded.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHUNK = ROOT / "outputs" / "yt_pr230_fh_lsz_production_L12_T24_chunk001_2026-05-01.json"
ARTIFACT = (
    ROOT
    / "outputs"
    / "yt_direct_lattice_correlator_production_fh_lsz_chunks"
    / "L12_T24_chunk001"
    / "L12xT24"
    / "ensemble_measurement.json"
)
COMBINER = ROOT / "outputs" / "yt_fh_lsz_chunk_combiner_gate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_chunk001_checkpoint_certificate_2026-05-02.json"

EXPECTED_SOURCE_SHIFTS = {-0.01, 0.0, 0.01}
EXPECTED_MODE_KEYS = {"0,0,0", "1,0,0", "0,1,0", "0,0,1"}

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


def main() -> int:
    print("PR #230 FH/LSZ chunk001 production checkpoint certificate")
    print("=" * 72)

    chunk = load_json(CHUNK)
    artifact = load_json(ARTIFACT)
    combiner = load_json(COMBINER)
    metadata = chunk.get("metadata", {})
    run_control = metadata.get("run_control", {})
    ensemble = first_ensemble(chunk)
    source = ensemble.get("scalar_source_response_analysis", {})
    lsz = ensemble.get("scalar_two_point_lsz_analysis", {})
    mode_rows = lsz.get("mode_rows", {}) if isinstance(lsz, dict) else {}
    combiner_summary = combiner.get("chunk_summary", {})
    seed_gate = combiner.get("seed_independence_gate", {})
    seed_control = ensemble.get("rng_seed_control")

    source_shifts = {
        round(float(row.get("source_shift_lat")), 8)
        for row in source.get("energy_fits", [])
        if isinstance(row, dict) and finite(row.get("source_shift_lat"))
    }
    mode_keys = set(mode_rows) if isinstance(mode_rows, dict) else set()

    report("chunk-output-present", bool(chunk), str(CHUNK.relative_to(ROOT)))
    report("chunk-artifact-present", bool(artifact), str(ARTIFACT.relative_to(ROOT)))
    report("production-phase", metadata.get("phase") == "production", str(metadata.get("phase")))
    report("run-control-seed-and-volume", run_control.get("seed") == 2026051001 and run_control.get("volumes") == "12x24", str(run_control))
    report("same-source-fh-response-present", finite(source.get("slope_dE_ds_lat")) and source_shifts == {round(x, 8) for x in EXPECTED_SOURCE_SHIFTS}, f"slope={source.get('slope_dE_ds_lat')}, shifts={sorted(source_shifts)}")
    report("same-source-lsz-modes-present", EXPECTED_MODE_KEYS <= mode_keys, f"modes={sorted(mode_keys)}")
    report("physical-higgs-normalization-not-derived", metadata.get("scalar_source_response", {}).get("used_as_physical_yukawa_readout") is False and metadata.get("scalar_two_point_lsz", {}).get("used_as_physical_yukawa_readout") is False, "readout flags false")
    report("historical-numba-seed-control-missing", not isinstance(seed_control, dict), "historical output predates numba_gauge_seed_v1")
    report(
        "combiner-demotes-historical-chunks",
        combiner_summary.get("present_chunks", 0) >= 1
        and combiner_summary.get("ready_chunks") == 0
        and seed_gate.get("present_chunks_pass_seed_independence_gate") is False,
        str(combiner_summary),
    )
    report("combined-output-still-unavailable", combiner.get("combined_summary", {}).get("available") is False, "63 chunks required before L12 combination")
    report("does-not-authorize-retained-proposal", True, "seed-invalid partial L12 chunk is not retained evidence")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ chunk001 production checkpoint seed-invalid diagnostic",
        "verdict": (
            "Historical L12_T24 chunk001 completed with production-phase metadata, "
            "same-source dE/ds response, and same-source scalar C_ss(q) rows for "
            "the four-mode/x16 plan.  It is not independent production evidence "
            "on the current surface because it lacks the numba_gauge_seed_v1 "
            "seed-control marker and the combiner now demotes historical chunks "
            "with duplicate gauge-evolution signatures.  This is a seed-invalid "
            "production-format diagnostic only."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Historical chunk001 lacks auditable numba gauge seed control; no combined L12, L16/L24, pole derivative, model-class, or FV/IR certificate exists.",
        "chunk_output": str(CHUNK.relative_to(ROOT)),
        "chunk_artifact": str(ARTIFACT.relative_to(ROOT)),
        "combiner_gate": str(COMBINER.relative_to(ROOT)),
        "chunk_summary": {
            "phase": metadata.get("phase"),
            "seed": run_control.get("seed"),
            "volumes": run_control.get("volumes"),
            "measurement_sweeps": run_control.get("measurement_sweeps"),
            "scalar_source_shifts": run_control.get("scalar_source_shifts"),
            "scalar_two_point_modes": run_control.get("scalar_two_point_modes"),
            "scalar_two_point_noises": run_control.get("scalar_two_point_noises"),
            "seed_control_version": run_control.get("seed_control_version"),
            "ensemble_rng_seed_control": seed_control,
            "seed_independence_valid": False,
            "slope_dE_ds_lat": source.get("slope_dE_ds_lat"),
            "slope_dE_ds_lat_err": source.get("slope_dE_ds_lat_err"),
            "mode_keys": sorted(mode_keys),
            "combiner_present_chunks": combiner_summary.get("present_chunks"),
            "combiner_ready_chunks": combiner_summary.get("ready_chunks"),
            "combiner_expected_chunks": combiner_summary.get("expected_chunks"),
        },
        "strict_non_claims": [
            "does not use chunk001 as retained evidence",
            "does not count historical chunk001 as independent production evidence",
            "does not set kappa_s = 1",
            "does not use H_unit, Ward authority, observed target values, alpha_LM, plaquette, or u0 as proof input",
            "does not treat partial L12 output as L16/L24 or pole-fit evidence",
        ],
        "exact_next_action": "Rerun a replacement chunk001 under numba_gauge_seed_v1 before counting it toward L12 combination.",
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
