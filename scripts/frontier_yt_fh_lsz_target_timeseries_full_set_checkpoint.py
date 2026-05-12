#!/usr/bin/env python3
"""
PR #230 FH/LSZ full target-timeseries set checkpoint.

This runner is packaging support only. It checks that the L12 FH/LSZ
target-timeseries replacement campaign has a complete 63-chunk ready set with
seed-controlled production metadata and the expected target-row schema.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_target_timeseries_full_set_checkpoint_2026-05-12.json"
COMBINER = ROOT / "outputs" / "yt_fh_lsz_chunk_combiner_gate_2026-05-01.json"
AUTOCORR = ROOT / "outputs" / "yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json"
TARGET_ESS = ROOT / "outputs" / "yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json"
QUEUE = ROOT / "outputs" / "yt_fh_lsz_target_timeseries_replacement_queue_2026-05-02.json"
EXPECTED_CHUNKS = 63
EXPECTED_MEASUREMENTS = 16
EXPECTED_MODES = {"0,0,0", "0,0,1", "0,1,0", "1,0,0"}
EXPECTED_SEED_VERSION = "numba_gauge_seed_v1"

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
    return json.loads(path.read_text(encoding="utf-8"))


def chunk_path(index: int) -> Path:
    return ROOT / "outputs" / f"yt_pr230_fh_lsz_production_L12_T24_chunk{index:03d}_2026-05-01.json"


def checkpoint_path(index: int) -> Path:
    return ROOT / "outputs" / f"yt_fh_lsz_chunk{index:03d}_target_timeseries_generic_checkpoint_2026-05-02.json"


def chunk_schema_summary(index: int) -> dict[str, Any]:
    artifact = load_json(chunk_path(index))
    ensembles = artifact.get("ensembles", [])
    ensemble = ensembles[0] if ensembles else {}
    run_control = artifact.get("metadata", {}).get("run_control", {})
    rng = ensemble.get("rng_seed_control", {})
    source = ensemble.get("scalar_source_response_analysis", {})
    lsz = ensemble.get("scalar_two_point_lsz_analysis", {})
    mode_rows = lsz.get("mode_rows", {})
    mode_keys = set(mode_rows) if isinstance(mode_rows, dict) else set()
    source_energies = source.get("per_configuration_effective_energies", [])
    source_slopes = source.get("per_configuration_slopes", [])
    mode_timeseries_lengths = {
        mode: len(row.get("C_ss_timeseries", []))
        for mode, row in mode_rows.items()
        if isinstance(row, dict)
    }
    return {
        "chunk": index,
        "path": str(chunk_path(index).relative_to(ROOT)),
        "checkpoint": str(checkpoint_path(index).relative_to(ROOT)),
        "seed": run_control.get("seed"),
        "seed_control_version": rng.get("seed_control_version"),
        "production_targets": run_control.get("production_targets"),
        "selected_mass_only": run_control.get("fh_lsz_selected_mass_only"),
        "selected_mass_parameter": run_control.get("fh_lsz_selected_mass_parameter"),
        "normal_equation_cache_enabled": run_control.get("normal_equation_cache_enabled"),
        "source_timeseries_count": len(source_energies),
        "slope_timeseries_count": len(source_slopes),
        "mode_keys": sorted(mode_keys),
        "mode_timeseries_lengths": mode_timeseries_lengths,
        "schema_ok": (
            rng.get("seed_control_version") == EXPECTED_SEED_VERSION
            and run_control.get("production_targets") is True
            and len(source_energies) == EXPECTED_MEASUREMENTS
            and len(source_slopes) == EXPECTED_MEASUREMENTS
            and mode_keys == EXPECTED_MODES
            and all(length == EXPECTED_MEASUREMENTS for length in mode_timeseries_lengths.values())
        ),
    }


def main() -> int:
    print("PR #230 FH/LSZ full target-timeseries set checkpoint")
    print("=" * 72)

    combiner = load_json(COMBINER)
    autocorr = load_json(AUTOCORR)
    target_ess = load_json(TARGET_ESS)
    queue = load_json(QUEUE)

    chunk_summary = combiner.get("chunk_summary", {})
    target_summary = autocorr.get("target_timeseries_summary", {})
    queue_summary = queue.get("target_timeseries_summary", {})
    ready_indices = combiner.get("combined_summary", {}).get("chunk_count")
    queue_ready = queue.get("ready_indices", [])

    report("combiner-complete-63", (
        chunk_summary.get("expected_chunks") == EXPECTED_CHUNKS
        and chunk_summary.get("present_chunks") == EXPECTED_CHUNKS
        and chunk_summary.get("ready_chunks") == EXPECTED_CHUNKS
        and chunk_summary.get("missing_chunks") == 0
        and ready_indices == EXPECTED_CHUNKS
    ), f"chunk_summary={chunk_summary}")
    report("autocorr-target-timeseries-complete", (
        target_summary.get("complete_count") == EXPECTED_CHUNKS
        and target_summary.get("ready_count") == EXPECTED_CHUNKS
        and target_summary.get("complete_for_all_ready_chunks") is True
        and target_summary.get("incomplete_indices") == []
    ), f"target_timeseries_summary={target_summary}")
    report("target-observable-ess-passed", (
        target_ess.get("target_observable_ess_gate_passed") is True
        and target_ess.get("ready_chunk_count") == EXPECTED_CHUNKS
        and float(target_ess.get("limiting_target_ess", 0.0)) >= float(
            target_ess.get("minimum_target_ess_per_volume", 1e100)
        )
    ), (
        f"limiting_target_ess={target_ess.get('limiting_target_ess')} "
        f"threshold={target_ess.get('minimum_target_ess_per_volume')}"
    ))
    report("replacement-queue-empty", (
        queue.get("replacement_queue") == []
        and queue.get("next_replacement_chunk") is None
        and queue_summary.get("complete_count") == EXPECTED_CHUNKS
        and len(queue_ready) == EXPECTED_CHUNKS
    ), f"replacement_queue={queue.get('replacement_queue')}")

    missing_chunks = [index for index in range(1, EXPECTED_CHUNKS + 1) if not chunk_path(index).exists()]
    missing_checkpoints = [
        index for index in range(1, EXPECTED_CHUNKS + 1) if not checkpoint_path(index).exists()
    ]
    report("all-production-artifacts-present", missing_chunks == [], f"missing={missing_chunks[:10]}")
    report("all-generic-checkpoints-present", missing_checkpoints == [], f"missing={missing_checkpoints[:10]}")

    schema_rows = [chunk_schema_summary(index) for index in range(1, EXPECTED_CHUNKS + 1)]
    bad_schema = [row["chunk"] for row in schema_rows if not row["schema_ok"]]
    seed_versions = sorted({row["seed_control_version"] for row in schema_rows})
    seeds = [row["seed"] for row in schema_rows]
    selected_mass_only_chunks = [
        row["chunk"] for row in schema_rows if row["selected_mass_only"] is True
    ]
    normal_cache_chunks = [
        row["chunk"] for row in schema_rows if row["normal_equation_cache_enabled"] is True
    ]
    report("chunk-schema-preserved", bad_schema == [], f"bad_schema_chunks={bad_schema[:10]}")
    report(
        "seed-control-preserved",
        seed_versions == [EXPECTED_SEED_VERSION] and len(set(seeds)) == EXPECTED_CHUNKS,
        f"seed_versions={seed_versions} unique_seeds={len(set(seeds))}",
    )
    report(
        "does-not-authorize-retained-proposal",
        True,
        "complete target-timeseries support still lacks scalar-LSZ denominator and canonical-Higgs/source-overlap authority",
    )

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ full L12 target-timeseries packet checkpoint",
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The full L12 target-timeseries packet is production-processing support only. "
            "It does not derive kappa_s, scalar-pole derivative/model-class/FV/IR authority, "
            "canonical O_H/source-Higgs overlap, W/Z response rows, or strict g2 authority."
        ),
        "bare_retained_allowed": False,
        "combiner_certificate": str(COMBINER.relative_to(ROOT)),
        "autocorrelation_certificate": str(AUTOCORR.relative_to(ROOT)),
        "target_observable_ess_certificate": str(TARGET_ESS.relative_to(ROOT)),
        "replacement_queue_certificate": str(QUEUE.relative_to(ROOT)),
        "chunk_summary": chunk_summary,
        "target_timeseries_summary": target_summary,
        "target_observable_ess_summary": {
            "target_observable_ess_gate_passed": target_ess.get("target_observable_ess_gate_passed"),
            "limiting_target_ess": target_ess.get("limiting_target_ess"),
            "minimum_target_ess_per_volume": target_ess.get("minimum_target_ess_per_volume"),
            "limiting_target_ess_observable": target_ess.get("limiting_target_ess_observable"),
        },
        "replacement_queue": queue.get("replacement_queue"),
        "schema_summary": {
            "checked_chunks": EXPECTED_CHUNKS,
            "bad_schema_chunks": bad_schema,
            "seed_control_versions": seed_versions,
            "unique_seed_count": len(set(seeds)),
            "selected_mass_parameter": 0.75,
            "selected_mass_only_chunks": selected_mass_only_chunks,
            "selected_mass_only_chunk_count": len(selected_mass_only_chunks),
            "normal_equation_cache_chunks": normal_cache_chunks,
            "normal_equation_cache_chunk_count": len(normal_cache_chunks),
            "mixed_optimization_metadata_reason": (
                "Some valid target-timeseries chunks predate the selected-mass/normal-cache "
                "optimization; the full-set checkpoint requires schema and seed control for "
                "all chunks and records the optimization split explicitly."
            ),
            "source_timeseries_count_per_chunk": EXPECTED_MEASUREMENTS,
            "scalar_lsz_modes": sorted(EXPECTED_MODES),
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not identify the scalar source pole with canonical O_H",
            "does not supply C_sH/C_HH pole rows",
            "does not supply same-source W/Z response rows or strict g2 authority",
            "does not turn L12-only finite-shell support into scalar-LSZ/FV closure",
        ],
        "exact_next_action": (
            "Use the 63/63 target-timeseries packet only as production support. "
            "Closure still needs a same-surface canonical O_H/source-overlap packet, "
            "genuine W/Z response rows with identity/covariance/g2 authority, strict "
            "scalar-LSZ moment/threshold/FV authority, Schur A/B/C pole rows, or a "
            "neutral primitive/off-diagonal-generator certificate."
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
