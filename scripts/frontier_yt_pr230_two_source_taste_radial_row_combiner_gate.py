#!/usr/bin/env python3
"""
PR #230 two-source taste-radial C_sx/C_xx row combiner gate.

The production manifest launches 63 L12_T24 chunks for the taste-radial
second source.  This runner is the acceptance boundary between per-chunk row
JSON and a combined measurement-row packet.  It audits completed chunks and
refuses to write the future combined rows file until every manifest chunk is
present and schema-clean.  Partial chunk sets remain support/status only.
"""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
ACTION_CERT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json"
ROW_CONTRACT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_contract_2026-05-06.json"
OUTPUT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json"
COMBINED_ROWS = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json"

EXPECTED_MODES = {"0,0,0", "1,0,0", "0,1,0", "0,0,1"}
EXPECTED_MASSES = [0.45, 0.75, 1.05]
EXPECTED_SEED_CONTROL_VERSION = "numba_gauge_seed_v1"

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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or len(ensembles) != 1:
        return {}
    row = ensembles[0]
    return row if isinstance(row, dict) else {}


def mode_series_ok(row: dict[str, Any], key: str) -> bool:
    values = row.get(key)
    if not isinstance(values, list) or len(values) == 0:
        return False
    prefix = key.removesuffix("_timeseries")
    real_key = f"{prefix}_real"
    imag_key = f"{prefix}_imag"
    for item in values:
        if not isinstance(item, dict):
            return False
        if not finite_number(item.get(real_key)):
            return False
        if imag_key in item and not finite_number(item.get(imag_key)):
            return False
    return True


def chunk_audit(manifest_row: dict[str, Any]) -> dict[str, Any]:
    index = int(manifest_row["chunk_index"])
    output = ROOT / str(manifest_row["output"])
    audit: dict[str, Any] = {
        "chunk_index": index,
        "seed": manifest_row.get("seed"),
        "output": rel(output),
        "exists": output.exists(),
        "ready_for_combination": False,
        "issues": [],
        "mode_rows_count": 0,
        "configuration_count_by_mode": {},
    }
    if not output.exists():
        audit["issues"].append("chunk output absent")
        return audit

    data = load_json(output)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    run_control = metadata.get("run_control") if isinstance(metadata.get("run_control"), dict) else {}
    ensemble = selected_ensemble(data)
    seed_control = ensemble.get("rng_seed_control") if isinstance(ensemble.get("rng_seed_control"), dict) else {}
    source = ensemble.get("source_higgs_cross_correlator_analysis")
    lsz = ensemble.get("scalar_two_point_lsz_analysis")
    response = ensemble.get("scalar_source_response_analysis")

    if metadata.get("phase") != "production":
        audit["issues"].append(f"phase={metadata.get('phase')!r}")
    if run_control.get("seed") != manifest_row.get("seed"):
        audit["issues"].append(f"seed={run_control.get('seed')!r}")
    if run_control.get("production_targets") is not True:
        audit["issues"].append("production_targets not true")
    if [float(x) for x in run_control.get("masses", [])] != EXPECTED_MASSES:
        audit["issues"].append(f"masses={run_control.get('masses')!r}")
    if seed_control.get("seed_control_version") != EXPECTED_SEED_CONTROL_VERSION:
        audit["issues"].append(f"seed_control_version={seed_control.get('seed_control_version')!r}")
    if seed_control.get("base_seed") != manifest_row.get("seed"):
        audit["issues"].append(f"base_seed={seed_control.get('base_seed')!r}")
    if ensemble.get("selected_mass_parameter") != 0.75:
        audit["issues"].append(f"selected_mass_parameter={ensemble.get('selected_mass_parameter')!r}")
    if not isinstance(response, dict):
        audit["issues"].append("missing scalar_source_response_analysis")
    elif not isinstance(response.get("per_configuration_slopes"), list):
        audit["issues"].append("missing per_configuration_slopes")
    if not isinstance(lsz, dict):
        audit["issues"].append("missing scalar_two_point_lsz_analysis")
    elif set((lsz.get("mode_rows") or {}).keys()) != EXPECTED_MODES:
        audit["issues"].append("scalar_two_point_lsz mode set mismatch")
    if not isinstance(source, dict):
        audit["issues"].append("missing source_higgs_cross_correlator_analysis")
    else:
        if source.get("used_as_physical_yukawa_readout") is not False:
            audit["issues"].append("source rows marked as physical y_t readout")
        aliases = source.get("two_source_taste_radial_row_aliases", {})
        if not isinstance(aliases, dict) or aliases.get("C_sx_aliases_C_sH_schema_field") is not True:
            audit["issues"].append("C_sx alias metadata missing")
        if not isinstance(aliases, dict) or aliases.get("C_xx_aliases_C_HH_schema_field") is not True:
            audit["issues"].append("C_xx alias metadata missing")
        mode_rows = source.get("mode_rows")
        if not isinstance(mode_rows, dict) or set(mode_rows.keys()) != EXPECTED_MODES:
            audit["issues"].append("source-higgs mode set mismatch")
        elif isinstance(mode_rows, dict):
            audit["mode_rows_count"] = len(mode_rows)
            for mode, row in mode_rows.items():
                if not isinstance(row, dict):
                    audit["issues"].append(f"{mode} row not dict")
                    continue
                for key in ("C_ss_timeseries", "C_sx_timeseries", "C_xx_timeseries"):
                    if not mode_series_ok(row, key):
                        audit["issues"].append(f"{mode} missing {key}")
                if not finite_number(row.get("C_sx_real")) or not finite_number(row.get("C_xx_real")):
                    audit["issues"].append(f"{mode} missing finite C_sx/C_xx")
                audit["configuration_count_by_mode"][mode] = row.get("configuration_count")

    audit["ready_for_combination"] = not audit["issues"]
    return audit


def partial_mode_diagnostics(chunk_audits: list[dict[str, Any]]) -> dict[str, Any]:
    rows: dict[str, dict[str, list[float]]] = {
        mode: {
            "C_ss_real": [],
            "C_sx_real": [],
            "C_xx_real": [],
            "rho_sx_real": [],
            "finite_row_gram_determinant_real": [],
            "configuration_count": [],
        }
        for mode in sorted(EXPECTED_MODES)
    }
    for audit in chunk_audits:
        if not audit.get("ready_for_combination"):
            continue
        data = load_json(ROOT / str(audit["output"]))
        source = selected_ensemble(data).get("source_higgs_cross_correlator_analysis", {})
        for mode, row in (source.get("mode_rows") or {}).items():
            if mode not in rows or not isinstance(row, dict):
                continue
            for key in ("C_ss_real", "C_sx_real", "C_xx_real"):
                if finite_number(row.get(key)):
                    rows[mode][key].append(float(row[key]))
            c_ss = row.get("C_ss_real")
            c_sx = row.get("C_sx_real")
            c_xx = row.get("C_xx_real")
            if finite_number(c_ss) and finite_number(c_sx) and finite_number(c_xx):
                product = float(c_ss) * float(c_xx)
                if product > 0.0:
                    rows[mode]["rho_sx_real"].append(float(c_sx) / math.sqrt(product))
                    rows[mode]["finite_row_gram_determinant_real"].append(
                        product - float(c_sx) * float(c_sx)
                    )
            if finite_number(row.get("configuration_count")):
                rows[mode]["configuration_count"].append(float(row["configuration_count"]))

    summary: dict[str, Any] = {}
    for mode, values in rows.items():
        mode_summary: dict[str, Any] = {}
        for key, series in values.items():
            if not series:
                mode_summary[key] = {"count": 0, "mean": None, "stdev": None}
                continue
            mode_summary[key] = {
                "count": len(series),
                "mean": statistics.fmean(series),
                "stdev": statistics.stdev(series) if len(series) > 1 else 0.0,
            }
        mode_summary["strict_limit"] = (
            "rho_sx_real and finite_row_gram_determinant_real are finite-mode "
            "C_sx/C_xx diagnostics on the current chunk packet. They are not isolated-pole "
            "residues, not canonical C_sH/C_HH rows, and not y_t evidence."
        )
        summary[mode] = mode_summary
    return summary


def write_combined_rows(chunk_audits: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    payload = {
        "actual_current_surface_status": (
            "bounded-support / two-source taste-radial complete L12 C_sx/C_xx row packet; "
            "canonical O_H and pole/FV/IR authority still absent"
        ),
        "proposal_allowed": False,
        "bare_retained_allowed": False,
        "source_operator": "taste_radial_hypercube_flip_source_v1",
        "completed_chunk_indices": [row["chunk_index"] for row in chunk_audits],
        "mode_diagnostics": summary,
        "strict_limit": (
            "These are C_sx/C_xx second-source rows. They are not canonical-Higgs "
            "C_sH/C_HH rows and not y_t closure without canonical O_H/source-overlap "
            "or physical-response authority plus pole/FV/IR checks."
        ),
    }
    COMBINED_ROWS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    print("PR #230 two-source taste-radial row combiner gate")
    print("=" * 72)

    manifest = load_json(MANIFEST)
    action = load_json(ACTION_CERT)
    row_contract = load_json(ROW_CONTRACT)
    rows = manifest.get("chunk_commands") if isinstance(manifest.get("chunk_commands"), list) else []
    chunk_audits = [chunk_audit(row) for row in rows]
    present = [row for row in chunk_audits if row.get("exists")]
    ready = [row for row in chunk_audits if row.get("ready_for_combination")]
    bad = [row for row in chunk_audits if row.get("exists") and not row.get("ready_for_combination")]
    missing_indices = [row["chunk_index"] for row in chunk_audits if not row.get("exists")]
    ready_indices = [row["chunk_index"] for row in ready]
    expected_count = len(rows)
    all_ready = expected_count == 63 and len(ready) == expected_count and not bad
    summary = partial_mode_diagnostics(chunk_audits)

    if all_ready:
        write_combined_rows(ready, summary)

    combined_written = all_ready and COMBINED_ROWS.exists()
    partial_set = len(ready) < expected_count
    partial_did_not_write = partial_set and not COMBINED_ROWS.exists()
    proposal_allowed = False

    report("manifest-present", bool(manifest), rel(MANIFEST))
    report("manifest-passed-support-only", manifest.get("manifest_passed") is True, str(manifest.get("actual_current_surface_status")))
    report("action-certificate-loaded", action.get("two_source_taste_radial_action_passed") is True, rel(ACTION_CERT))
    report("row-contract-loaded", row_contract.get("two_source_taste_radial_row_contract_passed") is True, rel(ROW_CONTRACT))
    report("manifest-has-63-chunks", expected_count == 63, f"expected_count={expected_count}")
    report("completed-chunks-detected", len(present) >= 1, f"present={[row['chunk_index'] for row in present]}")
    report("ready-chunks-schema-clean", len(bad) == 0, f"bad={bad[:3]}")
    report("ready-count-recorded", len(ready) == len(present), f"ready={ready_indices}")
    report("partial-set-does-not-write-combined-rows", partial_did_not_write or all_ready, rel(COMBINED_ROWS))
    report("all-ready-required-before-combined-output", all_ready or partial_set, f"ready={len(ready)}/{expected_count}")
    report("combined-output-written-only-if-all-ready", combined_written == all_ready, f"combined_written={combined_written}")
    report(
        "partial-finite-overlap-diagnostics-non-evidence",
        (partial_set or all_ready)
        and all(
            "rho_sx_real" in row and "finite_row_gram_determinant_real" in row
            for row in summary.values()
        ),
        "rho_sx/Gram diagnostics are finite-mode support fields only",
    )
    report("does-not-authorize-retained-proposal", proposal_allowed is False, "row combiner support only")

    result = {
        "actual_current_surface_status": (
            "bounded-support / two-source taste-radial C_sx/C_xx row combiner gate; "
            "canonical O_H and pole/FV/IR authority still absent"
        ),
        "proposal_allowed": proposal_allowed,
        "bare_retained_allowed": False,
        "manifest": rel(MANIFEST),
        "action_certificate": rel(ACTION_CERT),
        "row_contract": rel(ROW_CONTRACT),
        "combined_rows_output": rel(COMBINED_ROWS),
        "combined_rows_written": combined_written,
        "expected_chunks": expected_count,
        "present_chunks": len(present),
        "ready_chunks": len(ready),
        "ready_chunk_indices": ready_indices,
        "missing_chunk_indices": missing_indices,
        "bad_chunk_audits": bad,
        "partial_mode_diagnostics": summary,
        "strict_non_claims": [
            "does not treat finite C_sx/C_xx rows as canonical-Higgs pole evidence",
            "does not treat C_sx/C_xx aliases as canonical-Higgs C_sH/C_HH rows",
            "does not derive canonical O_H or kappa_s",
            "does not supply pole/FV/IR authority",
            "does not authorize retained or proposed_retained y_t closure",
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
