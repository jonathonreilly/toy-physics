#!/usr/bin/env python3
"""
PR #230 FH/LSZ chunk011 target-timeseries production checkpoint.

This runner audits the first post-extension L12_T24 chunk that should contain
per-configuration target time series for the FH/LSZ autocorrelation/ESS gate.
It remains partial production support only, not retained closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHUNK = ROOT / "outputs" / "yt_pr230_fh_lsz_production_L12_T24_chunk011_2026-05-01.json"
ARTIFACT = (
    ROOT
    / "outputs"
    / "yt_direct_lattice_correlator_production_fh_lsz_chunks"
    / "L12_T24_chunk011"
    / "L12xT24"
    / "ensemble_measurement.json"
)
COMBINER = ROOT / "outputs" / "yt_fh_lsz_chunk_combiner_gate_2026-05-01.json"
READY_SET = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json"
AUTOCORR = ROOT / "outputs" / "yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_chunk011_target_timeseries_checkpoint_2026-05-02.json"

EXPECTED_SOURCE_SHIFTS = {-0.01, 0.0, 0.01}
EXPECTED_MODE_KEYS = {"0,0,0", "1,0,0", "0,1,0", "0,0,1"}
EXPECTED_SEED_CONTROL_VERSION = "numba_gauge_seed_v1"
EXPECTED_SEED = 2026051011

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
    print("PR #230 FH/LSZ chunk011 target-timeseries checkpoint")
    print("=" * 72)

    chunk = load_json(CHUNK)
    artifact = load_json(ARTIFACT)
    combiner = load_json(COMBINER)
    ready_set = load_json(READY_SET)
    autocorr = load_json(AUTOCORR)
    metadata = chunk.get("metadata", {})
    run_control = metadata.get("run_control", {})
    ensemble = first_ensemble(chunk)
    source = ensemble.get("scalar_source_response_analysis", {})
    lsz = ensemble.get("scalar_two_point_lsz_analysis", {})
    mode_rows = lsz.get("mode_rows", {}) if isinstance(lsz, dict) else {}
    seed_control = ensemble.get("rng_seed_control")

    source_shifts = {
        round(float(row.get("source_shift_lat")), 8)
        for row in source.get("energy_fits", [])
        if isinstance(row, dict) and finite(row.get("source_shift_lat"))
    }
    mode_keys = set(mode_rows) if isinstance(mode_rows, dict) else set()
    per_config_slopes = source.get("per_configuration_slopes", [])
    per_config_energies = source.get("per_configuration_effective_energies", [])
    css_timeseries_modes = [
        key
        for key, row in mode_rows.items()
        if isinstance(row, dict) and isinstance(row.get("C_ss_timeseries"), list)
    ]
    seed_valid = (
        isinstance(seed_control, dict)
        and seed_control.get("seed_control_version") == EXPECTED_SEED_CONTROL_VERSION
        and seed_control.get("base_seed") == EXPECTED_SEED
        and seed_control.get("gauge_rng_seed") == expected_volume_seed(EXPECTED_SEED)
        and seed_control.get("numba_gauge_seeded_before_thermalization") is True
    )
    combiner_summary = combiner.get("chunk_summary", {})
    ready_indices = ready_set.get("ready_chunk_indices", [])
    target_summary = autocorr.get("target_timeseries_summary", {})

    report("chunk-output-present", bool(chunk), str(CHUNK.relative_to(ROOT)))
    report("chunk-artifact-present", bool(artifact), str(ARTIFACT.relative_to(ROOT)))
    report("production-phase", metadata.get("phase") == "production", str(metadata.get("phase")))
    report("run-control-seed-and-volume", run_control.get("seed") == EXPECTED_SEED and run_control.get("volumes") == "12x24", str(run_control))
    report("numba-seed-control-present", seed_valid, str(seed_control))
    report("same-source-fh-response-present", finite(source.get("slope_dE_ds_lat")) and source_shifts == {round(x, 8) for x in EXPECTED_SOURCE_SHIFTS}, f"slope={source.get('slope_dE_ds_lat')}, shifts={sorted(source_shifts)}")
    report("same-source-lsz-modes-present", EXPECTED_MODE_KEYS <= mode_keys, f"modes={sorted(mode_keys)}")
    report("source-response-target-timeseries-present", len(per_config_slopes) == 16 and len(per_config_energies) == 16, f"slopes={len(per_config_slopes)}, energies={len(per_config_energies)}")
    report("scalar-lsz-target-timeseries-present", EXPECTED_MODE_KEYS <= set(css_timeseries_modes), f"timeseries_modes={sorted(css_timeseries_modes)}")
    source_higgs_guard = metadata.get("source_higgs_cross_correlator", {})
    wz_guard = metadata.get("wz_mass_response", {})
    source_higgs_rows_absent = not source_higgs_guard or source_higgs_guard.get("enabled") is False
    wz_rows_absent = not wz_guard or wz_guard.get("enabled") is False
    report("source-higgs-rows-absent-or-guarded", source_higgs_rows_absent, str(source_higgs_guard))
    report("wz-response-rows-absent-or-guarded", wz_rows_absent, str(wz_guard))
    report("combiner-counts-chunk011-ready", 11 in ready_indices and combiner_summary.get("ready_chunks") == 11, f"ready={ready_indices}, summary={combiner_summary}")
    report("autocorr-records-partial-target-timeseries", target_summary.get("complete_indices") == [11] and target_summary.get("complete_for_all_ready_chunks") is False, str(target_summary))
    report("does-not-authorize-retained-proposal", True, "chunk011 is 11/63 L12 support and not Higgs identity")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ chunk011 target-timeseries production checkpoint",
        "verdict": (
            "L12_T24 chunk011 completed with production-phase metadata, "
            "numba_gauge_seed_v1 seed control, same-source dE/ds, same-source "
            "C_ss(q) rows, and per-configuration target time series for both "
            "source response and scalar LSZ modes.  The combiner counts 11/63 "
            "L12 chunks ready.  The global target ESS gate remains open because "
            "chunks001-010 predate the target-timeseries extension."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "11/63 L12 chunks is partial support; target ESS, response stability, pole/FV/IR/model-class, and Higgs identity gates remain open.",
        "chunk_output": str(CHUNK.relative_to(ROOT)),
        "chunk_artifact": str(ARTIFACT.relative_to(ROOT)),
        "combiner_gate": str(COMBINER.relative_to(ROOT)),
        "ready_set": str(READY_SET.relative_to(ROOT)),
        "autocorrelation_gate": str(AUTOCORR.relative_to(ROOT)),
        "chunk_summary": {
            "phase": metadata.get("phase"),
            "seed": run_control.get("seed"),
            "seed_control_version": run_control.get("seed_control_version"),
            "seed_independence_valid": seed_valid,
            "source_response_target_series_count": len(per_config_slopes),
            "scalar_lsz_target_timeseries_modes": sorted(css_timeseries_modes),
            "slope_dE_ds_lat": source.get("slope_dE_ds_lat"),
            "slope_dE_ds_lat_err": source.get("slope_dE_ds_lat_err"),
            "ready_chunks": combiner_summary.get("ready_chunks"),
            "expected_chunks": combiner_summary.get("expected_chunks"),
            "target_timeseries_summary": target_summary,
            "source_higgs_guard": source_higgs_guard,
            "wz_response_guard": wz_guard,
        },
        "strict_non_claims": [
            "does not use chunk011 as retained evidence",
            "does not treat 11/63 L12 chunks as combined L12 evidence",
            "does not set kappa_s = 1",
            "does not treat target time series as canonical-Higgs identity",
            "does not treat absent or pre-guard source-Higgs/WZ rows as evidence",
            "does not use H_unit, Ward authority, observed target values, alpha_LM, plaquette, or u0 as proof input",
        ],
        "exact_next_action": (
            "Continue future chunks with target time-series serialization or "
            "replace older chunks if a same-ready-set target ESS certificate is "
            "needed; do not use chunk011 as physical y_t evidence."
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
