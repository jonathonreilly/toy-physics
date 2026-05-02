#!/usr/bin/env python3
"""
PR #230 FH/LSZ chunk combiner gate.

This runner turns the L12 chunked launch manifest into an auditable acceptance
boundary.  It does not launch production and does not treat absent or partial
chunks as evidence.  If chunks exist, it audits that each output has production
phase metadata, same-source FH/LSZ observables, and run-control provenance
before it even constructs a combined L12 summary.  L12 combination still cannot
authorize retained closure by itself because L16/L24, isolated scalar pole
derivative, and FV/IR/zero-mode control remain open.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outputs" / "yt_fh_lsz_chunked_production_manifest_2026-05-01.json"
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_chunk_combiner_gate_2026-05-01.json"
COMBINED_OUTPUT = ROOT / "outputs" / "yt_pr230_fh_lsz_production_L12_T24_chunked_combined_2026-05-01.json"

EXPECTED_SOURCE_SHIFTS = {-0.01, 0.0, 0.01}
EXPECTED_MODE_KEYS = {"0,0,0", "1,0,0", "0,1,0", "0,0,1"}
EXPECTED_MASSES = [0.45, 0.75, 1.05]
EXPECTED_NOISES = 16
EXPECTED_THERM = 1000
EXPECTED_SEPARATION = 20
EXPECTED_CHUNK_MEASUREMENTS = 16
EXPECTED_VOLUME = "12x24"

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


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def expected_chunks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    policy = manifest.get("chunk_policy", {})
    count = int(policy.get("chunk_count", 0))
    measurements = int(policy.get("chunk_measurements", 0))
    rows = []
    for index in range(1, count + 1):
        rows.append(
            {
                "chunk_index": index,
                "seed": 2026051000 + index,
                "volume": EXPECTED_VOLUME,
                "measurements": measurements,
                "output": (
                    "outputs/yt_pr230_fh_lsz_production_L12_T24_"
                    f"chunk{index:03d}_2026-05-01.json"
                ),
            }
        )
    return rows


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or len(ensembles) != 1:
        return {}
    first = ensembles[0]
    return first if isinstance(first, dict) else {}


def audit_run_control(metadata: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    run_control = metadata.get("run_control")
    if not isinstance(run_control, dict):
        return ["metadata.run_control missing; seed/command provenance cannot be audited"]

    if run_control.get("seed") != expected["seed"]:
        issues.append(f"seed={run_control.get('seed')!r}, expected {expected['seed']}")
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
    if {round(float(x), 8) for x in run_control.get("scalar_source_shifts", [])} != {
        round(x, 8) for x in EXPECTED_SOURCE_SHIFTS
    }:
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
    return issues


def audit_source_response(ensemble: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    analysis = ensemble.get("scalar_source_response_analysis")
    if not isinstance(analysis, dict):
        return ["missing scalar_source_response_analysis"]
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
    if not finite_number(analysis.get("slope_dE_ds_lat_err")):
        issues.append("missing finite slope_dE_ds_lat_err")
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
    path = ROOT / expected["output"]
    data = load_json(path)
    if not data:
        return {
            **expected,
            "exists": False,
            "ready_for_l12_combination": False,
            "issues": ["chunk output absent"],
        }

    metadata = data.get("metadata", {})
    ensemble = selected_ensemble(data)
    issues: list[str] = []
    if metadata.get("phase") != "production":
        issues.append(f"phase={metadata.get('phase')!r}, expected production")
    if metadata.get("scalar_source_response", {}).get("used_as_physical_yukawa_readout") is not False:
        issues.append("scalar_source_response used_as_physical_yukawa_readout is not false")
    if ensemble.get("spatial_L") != 12 or ensemble.get("time_L") != 24:
        issues.append(f"dims={ensemble.get('dims')!r}, expected 12^3x24")
    if ensemble.get("thermalization_sweeps") != EXPECTED_THERM:
        issues.append(f"thermalization_sweeps={ensemble.get('thermalization_sweeps')!r}")
    if ensemble.get("measurement_sweeps") != EXPECTED_CHUNK_MEASUREMENTS:
        issues.append(f"measurement_sweeps={ensemble.get('measurement_sweeps')!r}")
    if ensemble.get("measurement_separation_sweeps") != EXPECTED_SEPARATION:
        issues.append(f"measurement_separation_sweeps={ensemble.get('measurement_separation_sweeps')!r}")
    issues.extend(audit_run_control(metadata, expected))
    issues.extend(audit_source_response(ensemble))
    issues.extend(audit_scalar_lsz(metadata, ensemble))

    return {
        **expected,
        "exists": True,
        "phase": metadata.get("phase"),
        "ready_for_l12_combination": not issues,
        "issues": issues,
    }


def weighted_mean(values: list[tuple[float, float]]) -> dict[str, float]:
    finite = [(v, e) for v, e in values if math.isfinite(v)]
    if not finite:
        return {"mean": float("nan"), "stderr": float("nan")}
    weights = []
    for _value, err in finite:
        if math.isfinite(err) and err > 0.0:
            weights.append(1.0 / (err * err))
        else:
            weights.append(1.0)
    total_w = sum(weights)
    mean = sum(value * weight for (value, _err), weight in zip(finite, weights)) / total_w
    stderr = math.sqrt(1.0 / total_w) if total_w > 0.0 else float("nan")
    return {"mean": float(mean), "stderr": float(stderr)}


def combine_if_ready(audits: list[dict[str, Any]]) -> dict[str, Any]:
    if not audits or not all(row.get("ready_for_l12_combination") for row in audits):
        return {"available": False, "reason": "not all expected chunks are ready for L12 combination"}

    source_values: list[tuple[float, float]] = []
    mode_values: dict[str, list[tuple[float, float]]] = {key: [] for key in EXPECTED_MODE_KEYS}
    for row in audits:
        data = load_json(ROOT / row["output"])
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
        nvec = [int(x) for x in key.split(",")]
        p_hat_sq = sum((2.0 * math.sin(math.pi * n / 12.0)) ** 2 for n in nvec)
        mode_rows[key] = {
            "momentum_mode": nvec,
            "p_hat_sq": p_hat_sq,
            "C_ss_real_weighted": c["mean"],
            "C_ss_real_weighted_stderr": c["stderr"],
            "Gamma_ss_real_proxy": gamma,
        }

    zero = mode_rows.get("0,0,0", {})
    first = mode_rows.get("0,0,1", {})
    derivative = float("nan")
    residue_proxy = float("nan")
    if zero and first and first.get("p_hat_sq", 0.0) > 0.0:
        derivative = (first["Gamma_ss_real_proxy"] - zero["Gamma_ss_real_proxy"]) / first["p_hat_sq"]
        residue_proxy = 1.0 / abs(derivative) if abs(derivative) > 1.0e-30 else float("nan")

    return {
        "available": True,
        "combined_output_target": str(COMBINED_OUTPUT.relative_to(ROOT)),
        "source_response": weighted_mean(source_values),
        "mode_rows": mode_rows,
        "finite_difference_residue_proxy": {
            "available": math.isfinite(derivative),
            "reference_modes": [[0, 0, 0], [0, 0, 1]],
            "dGamma_dp_hat_sq": derivative,
            "finite_residue_proxy": residue_proxy,
            "strict_limit": "finite L12 proxy is not kappa_s without isolated pole, FV/IR/zero-mode control, L16/L24, and retained-proposal gate",
        },
    }


def main() -> int:
    print("PR #230 FH/LSZ chunk combiner gate")
    print("=" * 72)

    manifest = load_json(MANIFEST)
    chunks = expected_chunks(manifest) if manifest else []
    audits = [audit_chunk(row) for row in chunks]
    present = [row for row in audits if row.get("exists")]
    ready = [row for row in audits if row.get("ready_for_l12_combination")]
    missing = [row for row in audits if not row.get("exists")]
    partial_present = 0 < len(present) < len(chunks)
    all_ready = bool(chunks) and len(ready) == len(chunks)
    harness_has_provenance = '"run_control"' in HARNESS.read_text(encoding="utf-8")
    combined_summary = combine_if_ready(audits)

    policy = manifest.get("chunk_policy", {}) if manifest else {}
    report("manifest-loaded", bool(manifest), str(MANIFEST.relative_to(ROOT)))
    report(
        "l12-grid-reconstructed",
        len(chunks) == int(policy.get("chunk_count", -1)) == 63
        and int(policy.get("chunk_measurements", -1)) == EXPECTED_CHUNK_MEASUREMENTS,
        f"chunks={len(chunks)} measurements_per_chunk={policy.get('chunk_measurements')}",
    )
    report("harness-records-run-control", harness_has_provenance, "future chunks expose seed and command provenance")
    report("current-chunk-set-incomplete", not all_ready, f"present={len(present)} ready={len(ready)} expected={len(chunks)}")
    report(
        "chunk-readiness-consistent-with-combiner",
        all_ready == bool(combined_summary.get("available")),
        f"partial_present={partial_present} combined_available={combined_summary.get('available')}",
    )
    report("no-forbidden-physical-readout-in-present-chunks", all(not row.get("issues") or "used_as_physical_yukawa_readout" not in " ".join(row.get("issues", [])) for row in present), f"present={len(present)}")
    report("l12-alone-not-retained-closure", True, "L16/L24 and pole derivative/FV/IR gates remain required")

    result = {
        "actual_current_surface_status": "open / FH-LSZ chunk combiner gate blocks partial evidence",
        "verdict": (
            "The L12 chunked FH/LSZ path now has an auditable combiner gate. "
            "No current chunk outputs are ready.  Future chunks must expose "
            "production phase, same-source dE/ds and C_ss(q), scalar-source "
            "non-readout metadata, and run-control provenance before an L12 "
            "combined summary can be constructed.  Even a complete L12 "
            "combination is not PR #230 closure because L16/L24 scaling, an "
            "isolated scalar pole inverse-derivative fit, FV/IR/zero-mode "
            "control, and the retained-proposal certificate remain open."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The combiner is an acceptance boundary for future chunks; it supplies no completed production data and no scalar pole derivative.",
        "manifest": str(MANIFEST.relative_to(ROOT)),
        "combined_output_target": str(COMBINED_OUTPUT.relative_to(ROOT)),
        "chunk_summary": {
            "expected_chunks": len(chunks),
            "present_chunks": len(present),
            "ready_chunks": len(ready),
            "missing_chunks": len(missing),
            "target_saved_configurations": int(policy.get("target_measurements", 0)) if policy else 0,
            "available_saved_configurations": len(ready) * EXPECTED_CHUNK_MEASUREMENTS,
        },
        "first_missing_outputs": [row["output"] for row in missing[:10]],
        "first_blocking_issues": [
            {"chunk_index": row["chunk_index"], "output": row["output"], "issues": row.get("issues", [])[:5]}
            for row in audits
            if row.get("issues")
        ][:10],
        "combined_summary": combined_summary,
        "acceptance_requirements": [
            "all 63 L12 chunk outputs must exist",
            "each chunk must declare metadata.phase == production",
            "each chunk must record run_control.seed and command settings matching the manifest",
            "each chunk must contain same-source linear dE/ds with shifts -0.01, 0.0, 0.01",
            "each chunk must contain same-source scalar C_ss(q) modes 0,100,010,001 with 16 noises",
            "the combined L12 summary remains non-retained until L16/L24 and isolated-pole/FV/IR gates pass",
        ],
        "strict_non_claims": [
            "does not launch production",
            "does not treat missing or partial chunks as evidence",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, or u0 as proof selectors",
            "does not set c2, Z_match, or kappa_s to one",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
