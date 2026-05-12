#!/usr/bin/env python3
"""
PR #230 FH/LSZ ready chunk-set production checkpoint certificate.

This runner records the current seed-controlled L12_T24 FH/LSZ ready chunk set
as bounded production support.  It derives the ready indices from the combiner
gate instead of hardcoding a fixed checkpoint.  It treats both partial and
complete L12 states as support only: no retained or proposed-retained claim is
allowed until L16/L24 scaling, scalar-pole derivative, FV/IR, and
canonical-Higgs identity gates pass.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMBINER = ROOT / "outputs" / "yt_fh_lsz_chunk_combiner_gate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json"

MIN_READY_INDICES = [1, 2, 3, 4]
EXPECTED_SEED_CONTROL_VERSION = "numba_gauge_seed_v1"
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


def chunk_output(index: int) -> Path:
    return ROOT / "outputs" / f"yt_pr230_fh_lsz_production_L12_T24_chunk{index:03d}_2026-05-01.json"


def chunk_artifact(index: int) -> Path:
    return (
        ROOT
        / "outputs"
        / "yt_direct_lattice_correlator_production_fh_lsz_chunks"
        / f"L12_T24_chunk{index:03d}"
        / "L12xT24"
        / "ensemble_measurement.json"
    )


def expected_volume_seed(base_seed: int, spatial_l: int = 12, time_l: int = 24) -> int:
    return int(base_seed + 1000003 * spatial_l + 9176 * time_l)


def audit_chunk(index: int) -> dict[str, Any]:
    path = chunk_output(index)
    artifact = chunk_artifact(index)
    chunk = load_json(path)
    artifact_data = load_json(artifact)
    metadata = chunk.get("metadata", {})
    run_control = metadata.get("run_control", {}) if isinstance(metadata, dict) else {}
    ensemble = first_ensemble(chunk)
    source = ensemble.get("scalar_source_response_analysis", {})
    lsz = ensemble.get("scalar_two_point_lsz_analysis", {})
    mode_rows = lsz.get("mode_rows", {}) if isinstance(lsz, dict) else {}
    seed_control = ensemble.get("rng_seed_control")
    expected_seed = 2026051000 + index

    source_shifts = {
        round(float(row.get("source_shift_lat")), 8)
        for row in source.get("energy_fits", [])
        if isinstance(row, dict) and finite(row.get("source_shift_lat"))
    }
    mode_keys = set(mode_rows) if isinstance(mode_rows, dict) else set()

    issues: list[str] = []
    if not chunk:
        issues.append("chunk output absent")
    if not artifact_data:
        issues.append("chunk artifact absent")
    if metadata.get("phase") != "production":
        issues.append(f"phase={metadata.get('phase')!r}")
    if run_control.get("seed") != expected_seed:
        issues.append(f"seed={run_control.get('seed')!r}, expected {expected_seed}")
    if run_control.get("volumes") != "12x24":
        issues.append(f"volumes={run_control.get('volumes')!r}")
    if run_control.get("measurement_sweeps") != 16:
        issues.append(f"measurement_sweeps={run_control.get('measurement_sweeps')!r}")
    if run_control.get("seed_control_version") != EXPECTED_SEED_CONTROL_VERSION:
        issues.append(f"run_control.seed_control_version={run_control.get('seed_control_version')!r}")
    if not isinstance(seed_control, dict):
        issues.append("missing ensemble.rng_seed_control")
    else:
        if seed_control.get("seed_control_version") != EXPECTED_SEED_CONTROL_VERSION:
            issues.append(f"seed_control_version={seed_control.get('seed_control_version')!r}")
        if seed_control.get("base_seed") != expected_seed:
            issues.append(f"base_seed={seed_control.get('base_seed')!r}, expected {expected_seed}")
        if seed_control.get("gauge_rng_seed") != expected_volume_seed(expected_seed):
            issues.append(f"gauge_rng_seed={seed_control.get('gauge_rng_seed')!r}")
        if seed_control.get("numba_gauge_seeded_before_thermalization") is not True:
            issues.append("numba_gauge_seeded_before_thermalization is not true")
    if not finite(source.get("slope_dE_ds_lat")):
        issues.append("missing finite slope_dE_ds_lat")
    if source_shifts != {round(x, 8) for x in EXPECTED_SOURCE_SHIFTS}:
        issues.append(f"source shifts {sorted(source_shifts)}")
    if not EXPECTED_MODE_KEYS <= mode_keys:
        issues.append(f"missing modes {sorted(EXPECTED_MODE_KEYS - mode_keys)}")
    if metadata.get("scalar_source_response", {}).get("used_as_physical_yukawa_readout") is not False:
        issues.append("scalar source response readout flag is not false")
    if metadata.get("scalar_two_point_lsz", {}).get("used_as_physical_yukawa_readout") is not False:
        issues.append("scalar LSZ readout flag is not false")

    return {
        "chunk_index": index,
        "output": str(path.relative_to(ROOT)),
        "artifact": str(artifact.relative_to(ROOT)),
        "seed": run_control.get("seed"),
        "seed_control": seed_control,
        "slope_dE_ds_lat": source.get("slope_dE_ds_lat") if isinstance(source, dict) else None,
        "slope_dE_ds_lat_err": source.get("slope_dE_ds_lat_err") if isinstance(source, dict) else None,
        "mode_keys": sorted(mode_keys),
        "issues": issues,
        "ready": not issues,
    }


def main() -> int:
    print("PR #230 FH/LSZ ready chunk-set production checkpoint certificate")
    print("=" * 72)

    combiner = load_json(COMBINER)
    summary = combiner.get("chunk_summary", {})
    seed_gate = combiner.get("seed_independence_gate", {})
    signatures = seed_gate.get("present_signatures", [])
    signature_indices = [row.get("chunk_index") for row in signatures if isinstance(row, dict)]
    ready_signature_indices = sorted(
        int(row.get("chunk_index"))
        for row in signatures
        if isinstance(row, dict)
        and isinstance(row.get("chunk_index"), int)
        and row.get("seed_related_issues") == []
    )
    ready_count = int(summary.get("ready_chunks", 0))
    expected_count = int(summary.get("expected_chunks", 1))
    complete_l12 = ready_count == expected_count and expected_count > 0
    combined_available = combiner.get("combined_summary", {}).get("available") is True
    chunk_rows = [audit_chunk(index) for index in ready_signature_indices]
    chunk_issues = {row["chunk_index"]: row["issues"] for row in chunk_rows if row["issues"]}

    report("combiner-present", bool(combiner), str(COMBINER.relative_to(ROOT)))
    report(
        "ready-indices-derived-from-combiner",
        all(index in ready_signature_indices for index in MIN_READY_INDICES)
        and ready_count == len(ready_signature_indices),
        f"ready_signature_indices={ready_signature_indices}, summary={summary}",
    )
    report(
        "seed-gate-clean-for-present-set",
        seed_gate.get("present_chunks_pass_seed_independence_gate") is True
        and all(isinstance(row, dict) and row.get("seed_related_issues") == [] for row in signatures),
        f"signature_indices={signature_indices}",
    )
    report("chunk-outputs-and-artifacts-ready", not chunk_issues, f"issues={chunk_issues}")
    report(
        "combined-output-state-consistent",
        combined_available == complete_l12,
        str(combiner.get("combined_summary", {})),
    )
    report(
        "l12-set-completeness-state-recorded",
        True,
        f"ready={ready_count} expected={expected_count} complete={complete_l12}",
    )
    report(
        "no-physical-yukawa-readout",
        all(row["ready"] for row in chunk_rows),
        "chunk metadata keeps scalar response/LSZ as non-readout support",
    )
    report(
        "does-not-authorize-retained-proposal",
        True,
        f"{ready_count}/{expected_count} L12 chunks is production support only",
    )

    if complete_l12:
        actual_status = "bounded-support / FH-LSZ complete L12 ready chunk-set checkpoint"
        readiness_sentence = (
            f"all {ready_count} of {expected_count} required L12 chunks are ready "
            "and the combiner has written the combined L12 support summary"
        )
        proposal_reason = (
            "The L12 chunk set is complete, but L12 support does not supply "
            "L16/L24 scaling, an isolated scalar-pole derivative, model-class "
            "control, FV/IR control, or Higgs-identity authority."
        )
        exact_next_action = (
            "Do not relitigate L12 chunk completeness.  Switch foreground "
            "effort to response stability, analytic Higgs-identity/scalar-"
            "denominator authority, strict W/Z response, or another same-"
            "surface bridge."
        )
    else:
        actual_status = "bounded-support / FH-LSZ ready chunk-set production checkpoint"
        readiness_sentence = (
            f"only {ready_count} of {expected_count} required L12 chunks are ready "
            "and no combined L12 output exists"
        )
        proposal_reason = (
            "The ready chunk set is partial L12 production support only; no combined "
            "L12, L16/L24, pole derivative, model-class, FV/IR, or Higgs-identity "
            "certificate exists."
        )
        exact_next_action = (
            "Continue collecting seed-controlled L12 chunks and rerun this "
            "dynamic checkpoint as each chunk finishes; switch foreground "
            "effort to a higher-probability analytic Higgs-identity/scalar-"
            "denominator route while production chunks run."
        )

    result = {
        "actual_current_surface_status": actual_status,
        "verdict": (
            f"Seed-controlled L12_T24 chunks{ready_signature_indices} are present and combiner-ready. "
            "They supply production-format same-source dE/ds and C_ss(q) support, "
            f"but {readiness_sentence}.  The scalar-pole derivative/model-class/"
            "FV/IR/canonical-Higgs identity gates remain open."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": proposal_reason,
        "combiner_gate": str(COMBINER.relative_to(ROOT)),
        "chunk_summary": summary,
        "seed_independence_gate": seed_gate,
        "ready_chunk_indices": ready_signature_indices,
        "minimum_expected_ready_indices": MIN_READY_INDICES,
        "chunk_rows": chunk_rows,
        "strict_non_claims": [
            "does not use L12 chunks as closure evidence",
            "does not set kappa_s = 1",
            "does not use H_unit, Ward authority, observed target values, alpha_LM, plaquette, or u0 as proof input",
            "does not treat source response as a physical Higgs readout",
            "does not bypass pole derivative, model-class, FV/IR, or canonical-Higgs identity gates",
        ],
        "exact_next_action": exact_next_action,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
