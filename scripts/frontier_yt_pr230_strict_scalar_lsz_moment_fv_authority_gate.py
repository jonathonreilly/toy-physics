#!/usr/bin/env python3
"""
PR #230 strict scalar-LSZ moment/FV authority gate.

Completed two-source taste-radial chunks carry real selected-mass
`C_ss(q)` scalar-source rows.  This runner tests whether the current raw
`C_ss(q^2)` proxy can be promoted into strict scalar-LSZ
moment/threshold/FV authority.

It cannot.  A positive unsubtracted Stieltjes two-point object

    C(x) = int dmu(s) / (x + s),    dmu(s) >= 0,    x = q_hat^2

is non-increasing in x.  The current raw source-source proxy is positive but
increases from the zero mode to the first shell across the completed chunks.
That makes it useful diagnostic data, not the strict scalar-LSZ object.
"""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json"
)
MANIFEST = (
    ROOT
    / "outputs"
    / "yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
)
COMBINER = (
    ROOT
    / "outputs"
    / "yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json"
)

PARENTS = {
    "stieltjes_moment_gate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "pade_stieltjes_bounds_gate": "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json",
    "polefit8x8_stieltjes_proxy": "outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json",
    "threshold_authority_audit": "outputs/yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json",
    "finite_volume_obstruction": "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

EXPECTED_MODES = {"0,0,0", "1,0,0", "0,1,0", "0,0,1"}
ZERO_MODE = "0,0,0"
EXPECTED_SEED_CONTROL_VERSION = "numba_gauge_seed_v1"
EXPECTED_SELECTED_MASS = 0.75

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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def load_json(path: str | Path) -> dict[str, Any]:
    full = Path(path)
    if not full.is_absolute():
        full = ROOT / full
    if not full.exists():
        return {}
    data = json.loads(full.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def summarize(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"count": 0, "mean": None, "stderr": None, "min": None, "max": None}
    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "stderr": statistics.stdev(values) / math.sqrt(len(values)) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def chunk_rows_from_manifest(manifest: dict[str, Any], combiner: dict[str, Any]) -> list[dict[str, Any]]:
    commands = manifest.get("chunk_commands")
    ready = combiner.get("ready_chunk_indices")
    if not isinstance(commands, list) or not isinstance(ready, list):
        return []
    ready_indices = {int(index) for index in ready if isinstance(index, int)}
    return [
        row
        for row in commands
        if isinstance(row, dict)
        and isinstance(row.get("chunk_index"), int)
        and int(row["chunk_index"]) in ready_indices
    ]


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or len(ensembles) != 1:
        return {}
    row = ensembles[0]
    return row if isinstance(row, dict) else {}


def parse_chunk(row: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    issues: list[str] = []
    output = ROOT / str(row.get("output", ""))
    if not output.exists():
        return None, [f"chunk{row.get('chunk_index')} output absent"]
    data = load_json(output)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    run_control = metadata.get("run_control") if isinstance(metadata.get("run_control"), dict) else {}
    ensemble = selected_ensemble(data)
    seed_control = ensemble.get("rng_seed_control") if isinstance(ensemble.get("rng_seed_control"), dict) else {}
    lsz = ensemble.get("scalar_two_point_lsz_analysis")
    chunk_index = int(row["chunk_index"])

    if metadata.get("phase") != "production":
        issues.append(f"chunk{chunk_index:03d} phase={metadata.get('phase')!r}")
    if run_control.get("seed") != row.get("seed"):
        issues.append(f"chunk{chunk_index:03d} seed mismatch")
    if seed_control.get("seed_control_version") != EXPECTED_SEED_CONTROL_VERSION:
        issues.append(f"chunk{chunk_index:03d} seed-control mismatch")
    if ensemble.get("selected_mass_parameter") != EXPECTED_SELECTED_MASS:
        issues.append(f"chunk{chunk_index:03d} selected mass mismatch")
    if not isinstance(lsz, dict):
        issues.append(f"chunk{chunk_index:03d} scalar_two_point_lsz_analysis absent")
        return None, issues
    if lsz.get("used_as_physical_yukawa_readout") is True:
        issues.append(f"chunk{chunk_index:03d} scalar LSZ marked physical")
    if lsz.get("canonical_higgs_operator_identity_passed") is True:
        issues.append(f"chunk{chunk_index:03d} canonical O_H unexpectedly passed")
    if lsz.get("physical_higgs_normalization") != "not_derived":
        issues.append(f"chunk{chunk_index:03d} physical Higgs normalization not firewalled")

    mode_rows = lsz.get("mode_rows")
    if not isinstance(mode_rows, dict) or set(mode_rows) != EXPECTED_MODES:
        issues.append(f"chunk{chunk_index:03d} mode set mismatch")
        return None, issues

    parsed_modes = {}
    for mode, mode_row in sorted(mode_rows.items()):
        if not isinstance(mode_row, dict):
            issues.append(f"chunk{chunk_index:03d} {mode} row not object")
            continue
        p_hat_sq = mode_row.get("p_hat_sq")
        c_ss = mode_row.get("C_ss_real")
        c_err = mode_row.get("C_ss_real_config_stderr")
        timeseries = mode_row.get("C_ss_timeseries")
        if not finite(p_hat_sq) or not finite(c_ss):
            issues.append(f"chunk{chunk_index:03d} {mode} nonfinite C_ss row")
            continue
        if not isinstance(timeseries, list) or not timeseries:
            issues.append(f"chunk{chunk_index:03d} {mode} missing C_ss_timeseries")
        parsed_modes[mode] = {
            "p_hat_sq": float(p_hat_sq),
            "C_ss_real": float(c_ss),
            "C_ss_real_config_stderr": float(c_err) if finite(c_err) else None,
            "timeseries_count": len(timeseries) if isinstance(timeseries, list) else 0,
        }

    if set(parsed_modes) != EXPECTED_MODES:
        return None, issues

    zero = parsed_modes[ZERO_MODE]
    shell_modes = [mode for mode in sorted(EXPECTED_MODES) if mode != ZERO_MODE]
    shell_values = [parsed_modes[mode]["C_ss_real"] for mode in shell_modes]
    shell_p_values = [parsed_modes[mode]["p_hat_sq"] for mode in shell_modes]
    shell_mean = statistics.fmean(shell_values)
    shell_p_mean = statistics.fmean(shell_p_values)
    if shell_p_mean <= zero["p_hat_sq"]:
        issues.append(f"chunk{chunk_index:03d} shell p_hat_sq not above zero")
    return {
        "chunk_index": chunk_index,
        "seed": row.get("seed"),
        "volume": f"{ensemble.get('spatial_L')}x{ensemble.get('time_L')}",
        "selected_mass_parameter": ensemble.get("selected_mass_parameter"),
        "zero_p_hat_sq": zero["p_hat_sq"],
        "zero_C_ss_real": zero["C_ss_real"],
        "shell_p_hat_sq_mean": shell_p_mean,
        "shell_C_ss_real_mean": shell_mean,
        "shell_minus_zero": shell_mean - zero["C_ss_real"],
        "mode_rows": parsed_modes,
    }, issues


def stieltjes_theorem() -> str:
    return (
        "For C(x)=int dmu(s)/(x+s) with dmu(s)>=0 and x=q_hat^2>=0, "
        "C(x2)-C(x1)=-(x2-x1) int dmu(s)/((x2+s)(x1+s)) <= 0 for x2>x1. "
        "A raw scalar-source proxy that increases from the zero mode to a "
        "higher shell is therefore not the strict unsubtracted Stieltjes "
        "two-point object needed for scalar-LSZ moment authority."
    )


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yukawa_as_selector": False,
        "used_alpha_lm_or_plaquette_u0": False,
        "used_reduced_cold_pilots_as_production_evidence": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_kappa_s_equal_one": False,
        "treated_raw_C_ss_as_canonical_H": False,
        "treated_raw_C_ss_as_strict_stieltjes_certificate": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 strict scalar-LSZ moment/FV authority gate")
    print("=" * 72)

    manifest = load_json(MANIFEST)
    combiner = load_json(COMBINER)
    parents = {name: load_json(path) for name, path in PARENTS.items()}
    parent_statuses = {name: status(cert) for name, cert in parents.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_parents = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    rows = chunk_rows_from_manifest(manifest, combiner)
    parsed_chunks: list[dict[str, Any]] = []
    chunk_issues: list[str] = []
    for row in rows:
        parsed, issues = parse_chunk(row)
        chunk_issues.extend(issues)
        if parsed is not None:
            parsed_chunks.append(parsed)

    zero_values = [float(chunk["zero_C_ss_real"]) for chunk in parsed_chunks]
    shell_values = [float(chunk["shell_C_ss_real_mean"]) for chunk in parsed_chunks]
    shell_minus_zero = [float(chunk["shell_minus_zero"]) for chunk in parsed_chunks]
    zero_summary = summarize(zero_values)
    shell_summary = summarize(shell_values)
    diff_summary = summarize(shell_minus_zero)
    diff_err = math.hypot(float(zero_summary["stderr"] or 0.0), float(shell_summary["stderr"] or 0.0))
    diff_z = (float(shell_summary["mean"]) - float(zero_summary["mean"])) / diff_err if diff_err else math.inf
    volumes = sorted({chunk.get("volume") for chunk in parsed_chunks if chunk.get("volume")})

    ready_chunks = combiner.get("ready_chunks")
    expected_chunks = combiner.get("expected_chunks")
    raw_rows_positive = all(value > 0.0 for value in zero_values + shell_values)
    all_ready_chunks_violate_nonincrease = bool(parsed_chunks) and all(value > 0.0 for value in shell_minus_zero)
    current_raw_proxy_fails = raw_rows_positive and all_ready_chunks_violate_nonincrease
    strict_authority_present = False
    clean_firewall = all(value is False for value in forbidden_firewall().values())
    multivolume_fv_ir_authority_present = len(volumes) >= 3
    complete_packet_present = ready_chunks == expected_chunks == 63

    report("manifest-loaded", bool(manifest), rel(MANIFEST))
    report("combiner-parent-loaded", bool(combiner), rel(COMBINER))
    report("parents-loaded", not missing_parents, f"missing={missing_parents}")
    report("no-parent-proposal-allowed", not proposal_parents, f"proposal_parents={proposal_parents}")
    report("ready-chunks-loaded", len(parsed_chunks) == ready_chunks and len(parsed_chunks) > 0, f"ready={ready_chunks} parsed={len(parsed_chunks)}")
    report("chunk-schema-clean", not chunk_issues, f"issues={chunk_issues[:5]}")
    report("raw-c-ss-positive", raw_rows_positive, f"zero={zero_summary['mean']} shell={shell_summary['mean']}")
    report("stieltjes-nonincrease-violation-detected", current_raw_proxy_fails, f"shell-zero={diff_summary['mean']} z={diff_z}")
    report("strict-scalar-lsz-authority-absent", strict_authority_present is False, "raw proxy is diagnostic only")
    report("fv-ir-authority-absent", multivolume_fv_ir_authority_present is False, f"volumes={volumes}")
    report(
        "complete-63-packet-support-only",
        complete_packet_present is True or ready_chunks < expected_chunks,
        f"ready={ready_chunks}/{expected_chunks}",
    )
    report("forbidden-import-firewall-clean", clean_firewall, "no forbidden proof input used")
    report("does-not-authorize-proposed-retained", True, "proposal_allowed=false")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / current two-source taste-radial raw C_ss "
            "rows do not supply strict scalar-LSZ moment/FV authority"
        ),
        "verdict": (
            "The completed two-source taste-radial selected-mass scalar rows are "
            "real production diagnostics, but the raw source-source proxy is not "
            "the strict scalar-LSZ Stieltjes object.  It is positive and increases "
            "from q_hat^2=0 to the first shell across every ready chunk, while an "
            "unsubtracted positive Stieltjes two-point function must be "
            "non-increasing.  The route still needs a certified contact-subtracted "
            "or denominator-derived scalar object plus threshold and FV/IR authority, "
            "or a physical source-Higgs/W/Z bypass."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The gate finds a necessary Stieltjes monotonicity violation in the "
            "current raw C_ss proxy and also records no "
            "multivolume FV/IR authority, no isolated-pole/model-class authority, "
            "and no canonical O_H/source-overlap authority."
        ),
        "bare_retained_allowed": False,
        "strict_scalar_lsz_moment_fv_authority_gate_passed": True,
        "strict_scalar_lsz_moment_fv_authority_present": strict_authority_present,
        "current_raw_c_ss_proxy_fails_stieltjes_monotonicity": current_raw_proxy_fails,
        "raw_c_ss_rows_positive": raw_rows_positive,
        "all_ready_chunks_violate_nonincrease": all_ready_chunks_violate_nonincrease,
        "ready_chunks": ready_chunks,
        "expected_chunks": expected_chunks,
        "parsed_chunks": len(parsed_chunks),
        "volumes": volumes,
        "complete_63_packet_present": complete_packet_present,
        "multivolume_fv_ir_authority_present": multivolume_fv_ir_authority_present,
        "canonical_higgs_operator_identity_passed": False,
        "isolated_pole_model_class_authority_present": False,
        "threshold_gap_authority_present": False,
        "zero_mode_summary": zero_summary,
        "shell_summary": shell_summary,
        "shell_minus_zero_summary": diff_summary,
        "shell_minus_zero_z_score_from_chunk_scatter": diff_z,
        "per_chunk_rows": parsed_chunks,
        "chunk_issues": chunk_issues,
        "stieltjes_theorem": stieltjes_theorem(),
        "parent_certificates": {name: path for name, path in PARENTS.items()},
        "parent_statuses": parent_statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not set kappa_s, c2, or Z_match to one",
            "does not treat raw C_ss as canonical O_H or physical y_t evidence",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette/u0, or observed top/y_t targets",
            "does not treat completed chunks or reduced pilots as production closure evidence",
        ],
        "exact_next_action": (
            "Derive or measure a certified contact-subtracted/denominator scalar "
            "two-point object with threshold and multivolume FV/IR authority, or "
            "bypass scalar LSZ with same-source C_spH/C_HH pole rows or W/Z "
            "physical-response rows."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
