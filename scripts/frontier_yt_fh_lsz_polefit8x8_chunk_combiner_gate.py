#!/usr/bin/env python3
"""
PR #230 FH/LSZ eight-mode/x8 pole-fit chunk combiner gate.

This audits the separate polefit8x8 L12 stream.  It can write a combined
diagnostic support surface from ready chunks, but that surface is never a
retained y_t readout by itself.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_chunk_manifest_2026-05-04.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_chunk_combiner_gate_2026-05-04.json"
COMBINED_OUTPUT = ROOT / "outputs" / "yt_pr230_fh_lsz_polefit8x8_L12_T24_chunked_combined_2026-05-04.json"

EXPECTED_SOURCE_SHIFTS = {-0.01, 0.0, 0.01}
EXPECTED_MODE_KEYS = {"0,0,0", "1,0,0", "1,1,0", "1,1,1", "2,0,0", "2,1,0", "2,1,1", "2,2,0"}
EXPECTED_MASSES = [0.75]
EXPECTED_NOISES = 8
EXPECTED_THERM = 1000
EXPECTED_SEPARATION = 20
EXPECTED_CHUNK_MEASUREMENTS = 16
EXPECTED_VOLUME = "12x24"
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def manifest_chunks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [row for row in manifest.get("commands", []) if isinstance(row, dict)]


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or len(ensembles) != 1:
        return {}
    first = ensembles[0]
    return first if isinstance(first, dict) else {}


def expected_volume_seed(base_seed: int, spatial_l: int = 12, time_l: int = 24) -> int:
    return int(base_seed + 1000003 * spatial_l + 9176 * time_l)


def audit_run_control(metadata: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    run_control = metadata.get("run_control")
    if not isinstance(run_control, dict):
        return ["metadata.run_control missing"]
    if run_control.get("seed") != expected.get("seed"):
        issues.append(f"seed={run_control.get('seed')!r}, expected {expected.get('seed')}")
    if run_control.get("volumes") != EXPECTED_VOLUME:
        issues.append(f"volumes={run_control.get('volumes')!r}")
    if [float(x) for x in run_control.get("masses", [])] != EXPECTED_MASSES:
        issues.append(f"masses={run_control.get('masses')!r}")
    if run_control.get("thermalization_sweeps") != EXPECTED_THERM:
        issues.append(f"thermalization_sweeps={run_control.get('thermalization_sweeps')!r}")
    if run_control.get("measurement_sweeps") != EXPECTED_CHUNK_MEASUREMENTS:
        issues.append(f"measurement_sweeps={run_control.get('measurement_sweeps')!r}")
    if run_control.get("measurement_separation_sweeps") != EXPECTED_SEPARATION:
        issues.append(f"measurement_separation_sweeps={run_control.get('measurement_separation_sweeps')!r}")
    if run_control.get("production_targets") is not True:
        issues.append("production_targets is not true")
    shifts = {round(float(x), 8) for x in run_control.get("scalar_source_shifts", [])}
    if shifts != {round(x, 8) for x in EXPECTED_SOURCE_SHIFTS}:
        issues.append(f"scalar_source_shifts={run_control.get('scalar_source_shifts')!r}")
    modes = {
        ",".join(str(int(v)) for v in mode)
        for mode in run_control.get("scalar_two_point_modes", [])
        if isinstance(mode, list)
    }
    if modes != EXPECTED_MODE_KEYS:
        issues.append(f"scalar_two_point_modes={sorted(modes)}")
    if run_control.get("scalar_two_point_noises") != EXPECTED_NOISES:
        issues.append(f"scalar_two_point_noises={run_control.get('scalar_two_point_noises')!r}")
    if run_control.get("production_output_dir") != expected.get("production_output_dir"):
        issues.append(f"production_output_dir={run_control.get('production_output_dir')!r}")
    if run_control.get("seed_control_version") != EXPECTED_SEED_CONTROL_VERSION:
        issues.append(f"seed_control_version={run_control.get('seed_control_version')!r}")
    return issues


def audit_seed_control(ensemble: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    seed_control = ensemble.get("rng_seed_control")
    if not isinstance(seed_control, dict):
        return ["missing ensemble.rng_seed_control"]
    issues: list[str] = []
    if seed_control.get("seed_control_version") != EXPECTED_SEED_CONTROL_VERSION:
        issues.append(f"seed_control_version={seed_control.get('seed_control_version')!r}")
    if seed_control.get("base_seed") != expected.get("seed"):
        issues.append(f"base_seed={seed_control.get('base_seed')!r}, expected {expected.get('seed')}")
    expected_seed = expected_volume_seed(int(expected.get("seed", 0)))
    if seed_control.get("gauge_rng_seed") != expected_seed:
        issues.append(f"gauge_rng_seed={seed_control.get('gauge_rng_seed')!r}, expected {expected_seed}")
    if seed_control.get("numba_gauge_seeded_before_thermalization") is not True:
        issues.append("numba_gauge_seeded_before_thermalization is not true")
    return issues


def audit_source_response(ensemble: dict[str, Any]) -> list[str]:
    analysis = ensemble.get("scalar_source_response_analysis")
    if not isinstance(analysis, dict):
        return ["missing scalar_source_response_analysis"]
    issues: list[str] = []
    if analysis.get("fit_kind") != "linear_dE_ds":
        issues.append(f"fit_kind={analysis.get('fit_kind')!r}")
    shifts = {
        round(float(row.get("source_shift_lat")), 8)
        for row in analysis.get("energy_fits", [])
        if isinstance(row, dict) and finite_number(row.get("source_shift_lat"))
    }
    if shifts != {round(x, 8) for x in EXPECTED_SOURCE_SHIFTS}:
        issues.append(f"source shifts {sorted(shifts)}")
    if not finite_number(analysis.get("slope_dE_ds_lat")):
        issues.append("missing finite slope_dE_ds_lat")
    if analysis.get("physical_higgs_normalization") != "not_derived":
        issues.append("source response claims physical Higgs normalization")
    return issues


def audit_scalar_lsz(metadata: dict[str, Any], ensemble: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    meta = metadata.get("scalar_two_point_lsz")
    if not isinstance(meta, dict) or meta.get("enabled") is not True:
        issues.append("metadata.scalar_two_point_lsz.enabled is not true")
    if not isinstance(meta, dict) or meta.get("noise_vectors_per_configuration") != EXPECTED_NOISES:
        issues.append(f"noise_vectors_per_configuration={meta.get('noise_vectors_per_configuration') if isinstance(meta, dict) else None!r}")
    if isinstance(meta, dict) and meta.get("used_as_physical_yukawa_readout") is not False:
        issues.append("scalar_two_point_lsz used_as_physical_yukawa_readout is not false")
    analysis = ensemble.get("scalar_two_point_lsz_analysis")
    if not isinstance(analysis, dict):
        return issues + ["missing scalar_two_point_lsz_analysis"]
    if analysis.get("physical_higgs_normalization") != "not_derived":
        issues.append("scalar LSZ analysis claims physical Higgs normalization")
    rows = analysis.get("mode_rows")
    if not isinstance(rows, dict):
        return issues + ["missing mode_rows"]
    missing = sorted(EXPECTED_MODE_KEYS - set(rows))
    if missing:
        issues.append(f"missing modes {missing}")
    for key in sorted(EXPECTED_MODE_KEYS & set(rows)):
        row = rows.get(key, {})
        if not finite_number(row.get("C_ss_real")):
            issues.append(f"{key} missing finite C_ss_real")
        if not finite_number(row.get("Gamma_ss_real")):
            issues.append(f"{key} missing finite Gamma_ss_real")
        if int(row.get("configuration_count", 0)) <= 0:
            issues.append(f"{key} has no configurations")
    return issues


def audit_chunk(expected: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / str(expected.get("output", ""))
    data = load_json(path)
    if not data:
        return {**expected, "exists": False, "ready_for_polefit8x8_combination": False, "issues": ["chunk output absent"]}
    metadata = data.get("metadata", {})
    ensemble = selected_ensemble(data)
    issues: list[str] = []
    if metadata.get("phase") != "production":
        issues.append(f"phase={metadata.get('phase')!r}, expected production")
    if ensemble.get("spatial_L") != 12 or ensemble.get("time_L") != 24:
        issues.append(f"dims={ensemble.get('dims')!r}, expected 12^3x24")
    if ensemble.get("thermalization_sweeps") != EXPECTED_THERM:
        issues.append(f"thermalization_sweeps={ensemble.get('thermalization_sweeps')!r}")
    if ensemble.get("measurement_sweeps") != EXPECTED_CHUNK_MEASUREMENTS:
        issues.append(f"measurement_sweeps={ensemble.get('measurement_sweeps')!r}")
    issues.extend(audit_run_control(metadata, expected))
    issues.extend(audit_seed_control(ensemble, expected))
    issues.extend(audit_source_response(ensemble))
    issues.extend(audit_scalar_lsz(metadata, ensemble))
    return {
        **expected,
        "exists": True,
        "phase": metadata.get("phase"),
        "ready_for_polefit8x8_combination": not issues,
        "issues": issues,
    }


def weighted_mean(values: list[tuple[float, float]]) -> dict[str, float]:
    finite = [(v, e) for v, e in values if math.isfinite(v)]
    if not finite:
        return {"mean": float("nan"), "stderr": float("nan")}
    weights = [1.0 / (e * e) if math.isfinite(e) and e > 0.0 else 1.0 for _v, e in finite]
    total = sum(weights)
    mean = sum(v * w for (v, _e), w in zip(finite, weights)) / total
    stderr = math.sqrt(1.0 / total) if total > 0.0 else float("nan")
    return {"mean": float(mean), "stderr": float(stderr)}


def p_hat_sq_from_key(key: str) -> float:
    return sum((2.0 * math.sin(math.pi * int(n) / 12.0)) ** 2 for n in key.split(","))


def combine_ready(audits: list[dict[str, Any]]) -> dict[str, Any]:
    ready = [row for row in audits if row.get("ready_for_polefit8x8_combination")]
    if not ready:
        return {"available": False, "reason": "no ready polefit8x8 chunks"}
    source_values: list[tuple[float, float]] = []
    mode_values: dict[str, list[tuple[float, float]]] = {key: [] for key in EXPECTED_MODE_KEYS}
    for row in ready:
        data = load_json(ROOT / str(row["output"]))
        ensemble = selected_ensemble(data)
        source = ensemble.get("scalar_source_response_analysis", {})
        source_values.append(
            (
                float(source.get("slope_dE_ds_lat", float("nan"))),
                float(source.get("slope_dE_ds_lat_err", float("nan"))),
            )
        )
        modes = ensemble.get("scalar_two_point_lsz_analysis", {}).get("mode_rows", {})
        for key in EXPECTED_MODE_KEYS:
            mode = modes.get(key, {})
            err = float(mode.get("C_ss_real_config_stderr", float("nan")))
            mode_values[key].append((float(mode.get("C_ss_real", float("nan"))), err))

    mode_rows = {}
    for key, values in mode_values.items():
        c = weighted_mean(values)
        gamma = 1.0 / c["mean"] if math.isfinite(c["mean"]) and abs(c["mean"]) > 1.0e-30 else float("nan")
        mode_rows[key] = {
            "momentum_mode": [int(part) for part in key.split(",")],
            "p_hat_sq": p_hat_sq_from_key(key),
            "C_ss_real_weighted": c["mean"],
            "C_ss_real_weighted_stderr": c["stderr"],
            "Gamma_ss_real_proxy": gamma,
        }
    return {
        "available": True,
        "combined_output_target": rel(COMBINED_OUTPUT),
        "chunk_count": len(ready),
        "saved_configurations": len(ready) * EXPECTED_CHUNK_MEASUREMENTS,
        "complete_l12_target": len(ready) == len(audits),
        "source_response": weighted_mean(source_values),
        "mode_rows": mode_rows,
    }


def write_combined(summary: dict[str, Any], audits: list[dict[str, Any]]) -> None:
    if not summary.get("available"):
        return
    ready = [row for row in audits if row.get("ready_for_polefit8x8_combination")]
    payload = {
        "metadata": {
            "phase": "partial_l12_polefit8x8_chunk_summary"
            if not summary.get("complete_l12_target")
            else "combined_l12_polefit8x8_chunk_summary",
            "source": "frontier_yt_fh_lsz_polefit8x8_chunk_combiner_gate.py",
            "manifest": rel(MANIFEST),
            "chunk_count": summary.get("chunk_count"),
            "saved_configurations": summary.get("saved_configurations"),
            "complete_l12_target": summary.get("complete_l12_target"),
            "strict_limit": (
                "Eight-mode/x8 L12 rows are same-source scalar-LSZ support only. "
                "They do not supply L16/L24 scaling, FV/IR/zero-mode control, "
                "a model-class theorem, canonical-Higgs/source overlap, or "
                "retained-proposal authority."
            ),
        },
        "chunk_indices": [int(row["chunk_index"]) for row in ready],
        "source_response_summary": summary.get("source_response", {}),
        "combined_lsz_summary": {"mode_rows": summary.get("mode_rows", {})},
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s, c2, Z_match, or cos(theta) to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not mix this eight-mode/x8 stream with the four-mode/x16 L12 stream",
        ],
    }
    COMBINED_OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    print("PR #230 FH/LSZ eight-mode/x8 pole-fit chunk combiner gate")
    print("=" * 72)

    manifest = load_json(MANIFEST)
    chunks = manifest_chunks(manifest)
    audits = [audit_chunk(row) for row in chunks]
    present = [row for row in audits if row.get("exists")]
    ready = [row for row in audits if row.get("ready_for_polefit8x8_combination")]
    missing = [row for row in audits if not row.get("exists")]
    combined = combine_ready(audits)
    write_combined(combined, audits)
    shells = sorted({round(p_hat_sq_from_key(key), 12) for key in EXPECTED_MODE_KEYS})

    report("manifest-loaded", bool(manifest), rel(MANIFEST))
    report("chunk-grid-reconstructed", len(chunks) == 63, f"chunks={len(chunks)}")
    report("polefit8x8-mode-shape-recorded", len(shells) >= 4, f"shells={shells}")
    report("present-chunks-valid-or-absent", all(row.get("ready_for_polefit8x8_combination") or not row.get("exists") for row in audits), f"present={len(present)} ready={len(ready)}")
    report("combination-state-recorded", True, f"ready={len(ready)} missing={len(missing)} combined={combined.get('available')}")
    report("not-retained-closure", True, "polefit8x8 L12 rows are support only")

    complete = bool(chunks) and len(ready) == len(chunks)
    status = (
        "bounded-support / FH-LSZ complete L12 eight-mode-x8 pole-fit summary constructed"
        if complete
        else "bounded-support / FH-LSZ partial eight-mode-x8 pole-fit stream"
        if ready
        else "open / FH-LSZ eight-mode-x8 pole-fit combiner awaiting chunks"
    )
    result = {
        "actual_current_surface_status": status,
        "verdict": (
            "The separate eight-mode/x8 pole-fit stream has an auditable combiner "
            f"gate.  Present chunks={len(present)}, ready chunks={len(ready)}, "
            f"expected chunks={len(chunks)}.  The combiner writes a diagnostic "
            "L12 same-source scalar-LSZ support summary when ready chunks exist, "
            "but that summary is not physical y_t evidence and cannot be mixed "
            "with the four-mode/x16 L12 stream."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "L12 polefit8x8 rows do not close FV/IR, model-class, or canonical-Higgs/source-overlap gates.",
        "manifest": rel(MANIFEST),
        "combined_output_target": rel(COMBINED_OUTPUT),
        "chunk_summary": {
            "expected_chunks": len(chunks),
            "present_chunks": len(present),
            "ready_chunks": len(ready),
            "missing_chunks": len(missing),
            "target_saved_configurations": int(manifest.get("chunk_policy", {}).get("target_measurements", 0)) if manifest else 0,
            "available_saved_configurations": len(ready) * EXPECTED_CHUNK_MEASUREMENTS,
        },
        "first_missing_outputs": [row["output"] for row in missing[:10]],
        "first_blocking_issues": [
            {"chunk_index": row["chunk_index"], "output": row["output"], "issues": row.get("issues", [])[:5]}
            for row in audits
            if row.get("issues")
        ][:10],
        "combined_summary": combined,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s, c2, Z_match, or cos(theta) to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not mix eight-mode/x8 and four-mode/x16 chunks as one homogeneous ensemble",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
