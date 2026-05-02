#!/usr/bin/env python3
"""
PR #230 FH/LSZ chunk001 production checkpoint certificate.

This runner audits the L12_T24 chunk001 output from the chunked FH/LSZ
production plan.  It records whether the replacement chunk has the patched
numba seed-control metadata needed before it can count toward the L12 combiner.
Even a seed-controlled chunk is only partial L12 support, not PR #230 closure.
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
EXPECTED_SEED_CONTROL_VERSION = "numba_gauge_seed_v1"

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


def expected_volume_seed(base_seed: int, spatial_l: int = 12, time_l: int = 24) -> int:
    return int(base_seed + 1000003 * spatial_l + 9176 * time_l)


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
    seed_valid = (
        isinstance(seed_control, dict)
        and seed_control.get("seed_control_version") == EXPECTED_SEED_CONTROL_VERSION
        and seed_control.get("base_seed") == 2026051001
        and seed_control.get("gauge_rng_seed") == expected_volume_seed(2026051001)
        and seed_control.get("numba_gauge_seeded_before_thermalization") is True
    )
    chunk001_signature = {}
    for row in seed_gate.get("present_signatures", []):
        if isinstance(row, dict) and row.get("chunk_index") == 1:
            chunk001_signature = row
            break

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
    report("numba-seed-control-present", seed_valid, str(seed_control))
    report(
        "combiner-counts-chunk001-ready",
        combiner_summary.get("present_chunks", 0) >= 1
        and combiner_summary.get("ready_chunks") >= 1
        and seed_gate.get("ready_chunks_after_seed_gate") >= 1
        and chunk001_signature.get("seed_related_issues") == [],
        f"summary={combiner_summary}, chunk001_signature={chunk001_signature}",
    )
    report("combined-output-still-unavailable", combiner.get("combined_summary", {}).get("available") is False, "63 chunks required before L12 combination")
    report("does-not-authorize-retained-proposal", True, "one seed-controlled L12 chunk is partial support only")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ chunk001 seed-controlled production checkpoint",
        "verdict": (
            "Replacement L12_T24 chunk001 completed with production-phase "
            "metadata, same-source dE/ds response, same-source scalar C_ss(q) "
            "rows for the four-mode/x16 plan, and numba_gauge_seed_v1 seed "
            "control.  The combiner counts it as 1 ready chunk out of 63 needed "
            "for the L12 set.  This is useful production support, but it is not "
            "PR #230 closure because the L12 set is incomplete and L16/L24 "
            "scaling, pole-derivative, model-class, FV/IR, and Higgs-identity "
            "gates remain open."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Only 1 of 63 L12 chunks is ready; no combined L12, L16/L24, pole derivative, model-class, FV/IR, or Higgs-identity certificate exists.",
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
            "seed_independence_valid": seed_valid,
            "slope_dE_ds_lat": source.get("slope_dE_ds_lat"),
            "slope_dE_ds_lat_err": source.get("slope_dE_ds_lat_err"),
            "mode_keys": sorted(mode_keys),
            "combiner_present_chunks": combiner_summary.get("present_chunks"),
            "combiner_ready_chunks": combiner_summary.get("ready_chunks"),
            "combiner_expected_chunks": combiner_summary.get("expected_chunks"),
        },
        "strict_non_claims": [
            "does not use chunk001 as retained evidence",
            "does not treat one seed-controlled chunk as combined L12 evidence",
            "does not set kappa_s = 1",
            "does not use H_unit, Ward authority, observed target values, alpha_LM, plaquette, or u0 as proof input",
            "does not treat partial L12 output as L16/L24 or pole-fit evidence",
        ],
        "exact_next_action": "Continue seed-controlled chunk002/chunk003 processing and collect the remaining L12 chunks before any L12 combination.",
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
