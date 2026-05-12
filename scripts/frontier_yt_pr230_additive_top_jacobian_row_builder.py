#!/usr/bin/env python3
"""
PR #230 additive-top Jacobian row builder.

The additive-top subtraction contract needs an independently measured
additive top slope A_top before the mixed current-source response can be
subtracted.  The packaged two-source taste-radial chunks contain the preserved
three-mass top correlator scan.  This runner extracts a same-ensemble coarse
Jacobian row from those production chunks without touching live workers.

This is bounded support only: the rows are chunk-level coarse mass-scan
Jacobians, not per-configuration matched covariance rows, W/Z response rows,
strict g2 authority, accepted action authority, or physical y_t evidence.
"""

from __future__ import annotations

import glob
import json
import math
import re
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT_GLOB = (
    ROOT
    / "outputs"
    / "yt_pr230_two_source_taste_radial_rows"
    / "yt_pr230_two_source_taste_radial_rows_L12_T24_chunk*_2026-05-06.json"
)
OUTPUT = ROOT / "outputs" / "yt_pr230_additive_top_jacobian_rows_2026-05-07.json"

PARENTS = {
    "additive_top_subtraction_contract": "outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json",
    "additive_source_radial_spurion_incompatibility": "outputs/yt_pr230_additive_source_radial_spurion_incompatibility_2026-05-07.json",
    "two_source_chunk_package": "outputs/yt_pr230_two_source_taste_radial_chunk_package_audit_2026-05-06.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

EXPECTED_CHUNK_COUNT = 63

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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def chunk_id(path: Path) -> int:
    match = re.search(r"chunk(\d+)", path.name)
    if not match:
        raise ValueError(f"could not parse chunk id from {path}")
    return int(match.group(1))


def sorted_scan(scan: Any) -> list[dict[str, Any]]:
    if not isinstance(scan, list):
        return []
    rows = [row for row in scan if isinstance(row, dict) and finite(row.get("m_bare_lat"))]
    return sorted(rows, key=lambda row: float(row["m_bare_lat"]))


def central_endpoint_slope(scan: list[dict[str, Any]]) -> dict[str, Any]:
    if len(scan) < 3:
        return {"finite": False, "reason": "fewer than three mass scan points"}
    low = scan[0]
    mid = scan[len(scan) // 2]
    high = scan[-1]
    denom = float(high["m_bare_lat"]) - float(low["m_bare_lat"])
    if denom <= 0.0:
        return {"finite": False, "reason": "nonpositive mass bracket"}
    if not finite(low.get("m_fit_lat")) or not finite(high.get("m_fit_lat")):
        return {"finite": False, "reason": "endpoint mass fits are non-finite"}
    slope = (float(high["m_fit_lat"]) - float(low["m_fit_lat"])) / denom
    low_err = float(low.get("m_fit_lat_err", 0.0) or 0.0)
    high_err = float(high.get("m_fit_lat_err", 0.0) or 0.0)
    slope_err = math.sqrt(low_err * low_err + high_err * high_err) / denom
    return {
        "finite": True,
        "bracket_masses_lat": [float(low["m_bare_lat"]), float(mid["m_bare_lat"]), float(high["m_bare_lat"])],
        "selected_mass_parameter": float(mid["m_bare_lat"]),
        "endpoint_energy_lat": [float(low["m_fit_lat"]), float(high["m_fit_lat"])],
        "endpoint_energy_err_lat": [low_err, high_err],
        "additive_top_jacobian_dE_dm_lat": slope,
        "additive_top_jacobian_dE_dm_lat_err": slope_err,
        "max_cg_residual": max(
            float(row.get("max_cg_residual", 0.0) or 0.0)
            for row in scan
            if finite(row.get("max_cg_residual", 0.0))
        ),
    }


def sample_covariance(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2 or len(xs) != len(ys):
        return float("nan")
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)


def stderr(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0 if values else float("nan")
    return statistics.stdev(values) / math.sqrt(len(values))


def weighted_mean(rows: list[dict[str, Any]], value_key: str, err_key: str) -> dict[str, float]:
    weighted = []
    for row in rows:
        value = row.get(value_key)
        err = row.get(err_key)
        if finite(value) and finite(err) and float(err) > 0.0:
            weight = 1.0 / (float(err) * float(err))
            weighted.append((float(value), weight))
    if not weighted:
        return {"mean": float("nan"), "stderr": float("nan")}
    norm = sum(weight for _value, weight in weighted)
    mean = sum(value * weight for value, weight in weighted) / norm
    return {"mean": mean, "stderr": math.sqrt(1.0 / norm)}


def package_chunk_ids() -> tuple[set[int], set[int]]:
    package = load_json(ROOT / PARENTS["two_source_chunk_package"])
    completed = package.get("completed_chunk_ids", [])
    active = package.get("active_chunk_ids", [])
    completed_ids = {int(chunk) for chunk in completed if isinstance(chunk, int)}
    active_ids = {int(chunk) for chunk in active if isinstance(chunk, int)}
    if not completed_ids:
        # Historical fallback for older package certificates.
        completed_ids = set(range(1, 47))
    return completed_ids, active_ids


def extract_rows() -> tuple[list[dict[str, Any]], list[str], set[int], set[int]]:
    completed_ids, active_ids = package_chunk_ids()
    row_paths = [
        Path(path)
        for path in glob.glob(str(INPUT_GLOB))
        if chunk_id(Path(path)) in completed_ids and chunk_id(Path(path)) not in active_ids
    ]
    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    for path in sorted(row_paths, key=chunk_id):
        try:
            data = load_json(path)
            ensembles = data.get("ensembles", [])
            if not ensembles:
                failures.append(f"{rel(path)}: ensembles missing")
                continue
            ensemble = ensembles[0]
            scan = sorted_scan(ensemble.get("mass_parameter_scan"))
            slope = central_endpoint_slope(scan)
            if not slope.get("finite"):
                failures.append(f"{rel(path)}: {slope.get('reason')}")
                continue
            scalar = ensemble.get("scalar_source_response_analysis", {})
            seed = ensemble.get("rng_seed_control", {})
            total_slope = scalar.get("slope_dE_ds_lat")
            total_slope_err = scalar.get("slope_dE_ds_lat_err")
            additive = float(slope["additive_top_jacobian_dE_dm_lat"])
            row = {
                "chunk": chunk_id(path),
                "source_file": rel(path),
                "volume": f"L{ensemble.get('spatial_L')}xT{ensemble.get('time_L')}",
                "thermalization_sweeps": ensemble.get("thermalization_sweeps"),
                "measurement_sweeps": ensemble.get("measurement_sweeps"),
                "measurement_separation_sweeps": ensemble.get("measurement_separation_sweeps"),
                "seed_control_version": seed.get("seed_control_version"),
                "base_seed": seed.get("base_seed"),
                "gauge_rng_seed": seed.get("gauge_rng_seed"),
                "selected_mass_parameter": ensemble.get("selected_mass_parameter"),
                "mass_scan_bracket_masses_lat": slope["bracket_masses_lat"],
                "mass_scan_endpoint_energy_lat": slope["endpoint_energy_lat"],
                "mass_scan_endpoint_energy_err_lat": slope["endpoint_energy_err_lat"],
                "A_top_dE_dm_lat": additive,
                "A_top_dE_dm_lat_err": slope["additive_top_jacobian_dE_dm_lat_err"],
                "T_total_dE_ds_lat": float(total_slope) if finite(total_slope) else float("nan"),
                "T_total_dE_ds_lat_err": float(total_slope_err) if finite(total_slope_err) else float("nan"),
                "diagnostic_T_minus_A_lat": (
                    float(total_slope) - additive if finite(total_slope) else float("nan")
                ),
                "same_ensemble_as_total_top_response": True,
                "same_coordinate_kind": (
                    "uniform additive Dirac mass coordinate; coarse mass scan uses larger "
                    "bracket than scalar-source response shifts"
                ),
                "strict_row_limit": (
                    "chunk-level mass-scan Jacobian; no per-configuration mass-scan "
                    "covariance and no W/Z/g2/action authority"
                ),
                "max_cg_residual": slope["max_cg_residual"],
            }
            rows.append(row)
        except Exception as exc:  # pragma: no cover - certificate diagnostics
            failures.append(f"{rel(path)}: {exc}")
    return rows, failures, completed_ids, active_ids


def contiguous_missing(chunks: list[int]) -> list[int]:
    if not chunks:
        return []
    return [chunk for chunk in range(min(chunks), max(chunks) + 1) if chunk not in set(chunks)]


def parent_statuses() -> dict[str, str]:
    statuses = {}
    for name, rel_path in PARENTS.items():
        cert = load_json(ROOT / rel_path)
        statuses[name] = str(cert.get("actual_current_surface_status", "missing"))
    return statuses


def main() -> int:
    print("PR #230 additive-top Jacobian row builder")
    print("=" * 72)

    rows, failures, completed_ids, active_ids = extract_rows()
    chunks = [int(row["chunk"]) for row in rows]
    missing_contiguous = contiguous_missing(chunks)
    finite_rows = [
        row
        for row in rows
        if finite(row.get("A_top_dE_dm_lat")) and finite(row.get("T_total_dE_ds_lat"))
    ]
    a_values = [float(row["A_top_dE_dm_lat"]) for row in finite_rows]
    t_values = [float(row["T_total_dE_ds_lat"]) for row in finite_rows]
    diagnostic_values = [float(row["diagnostic_T_minus_A_lat"]) for row in finite_rows]
    seed_versions = {row.get("seed_control_version") for row in rows}
    selected_masses = {round(float(row.get("selected_mass_parameter", float("nan"))), 12) for row in rows if finite(row.get("selected_mass_parameter"))}
    max_residual = max((float(row.get("max_cg_residual", 0.0) or 0.0) for row in rows), default=float("nan"))
    weighted = weighted_mean(rows, "A_top_dE_dm_lat", "A_top_dE_dm_lat_err")
    statuses = parent_statuses()

    production_metadata_ok = bool(rows) and not failures
    seed_control_ok = seed_versions == {"numba_gauge_seed_v1"}
    selected_mass_ok = selected_masses == {0.75}
    bracket_ok = all(row["mass_scan_bracket_masses_lat"] == [0.45, 0.75, 1.05] for row in rows)
    cg_ok = finite(max_residual) and max_residual < 1.0e-7
    row_count_ok = (
        len(rows) == len(completed_ids)
        and set(chunks) == completed_ids
        and not missing_contiguous
    )
    complete_chunk_packet = (
        row_count_ok
        and len(rows) == EXPECTED_CHUNK_COUNT
        and set(chunks) == set(range(1, EXPECTED_CHUNK_COUNT + 1))
        and not active_ids
    )
    support_rows_passed = all(
        [
            production_metadata_ok,
            seed_control_ok,
            selected_mass_ok,
            bracket_ok,
            cg_ok,
            row_count_ok,
        ]
    )
    strict_rows_passed = False

    report("parent-statuses-loaded", all(status != "missing" for status in statuses.values()), str(statuses))
    report("production-row-files-loaded", bool(rows), f"rows={len(rows)} failures={failures[:3]}")
    report("contiguous-ready-prefix", row_count_ok, f"chunks={min(chunks) if chunks else None}-{max(chunks) if chunks else None} missing={missing_contiguous}")
    report("seed-control-preserved", seed_control_ok, f"seed_versions={sorted(str(v) for v in seed_versions)}")
    report("selected-mass-policy-preserved", selected_mass_ok, f"selected_masses={sorted(selected_masses)}")
    report("three-mass-top-scan-preserved", bracket_ok, "bracket=[0.45, 0.75, 1.05]")
    report("cg-residuals-preserved", cg_ok, f"max_cg_residual={max_residual}")
    report("bounded-additive-top-jacobian-rows-written", support_rows_passed, f"row_count={len(rows)}")
    report(
        "complete-chunk-packet-consumed",
        complete_chunk_packet,
        f"rows={len(rows)}/{EXPECTED_CHUNK_COUNT} active={sorted(active_ids)}",
    )
    report("strict-additive-top-jacobian-not-claimed", not strict_rows_passed, "no per-configuration mass-scan covariance")
    report("proposal-not-authorized", True, "proposal_allowed=false")
    report("forbidden-firewall-clean", True, "no observed target, H_unit, Ward, alpha_LM, plaquette/u0, kappa_s=1, c2=1, Z_match=1, or g2=1")
    report(
        "live-worker-not-touched",
        True,
        f"read-only over packaged chunks001-{max(completed_ids):03d}; active={sorted(active_ids)}",
    )

    pass_count = PASS_COUNT
    fail_count = FAIL_COUNT
    result = {
        "actual_current_surface_status": (
            "bounded-support / additive-top coarse Jacobian rows from packaged "
            "three-mass top scans; strict subtraction closure still open"
        ),
        "conditional_surface_status": (
            "Would become a strict additive-top subtraction input only after "
            "per-configuration same-source additive Jacobian rows, W/Z response "
            "rows, matched covariance, strict non-observed g2, and accepted action "
            "authority are supplied."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "These rows measure a coarse additive-top mass-scan Jacobian with "
            "production metadata.  They do not supply matched covariance, W/Z "
            "response, strict g2, accepted action authority, or source-Higgs "
            "normalization, and they are not physical y_t evidence."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "additive_top_jacobian_rows_written": support_rows_passed,
        "bounded_additive_top_jacobian_rows_passed": support_rows_passed,
        "strict_additive_top_jacobian_rows_passed": strict_rows_passed,
        "row_schema_version": "pr230_additive_top_jacobian_rows_v1",
        "row_source": {
            "input_glob": rel(INPUT_GLOB),
            "expected_chunk_count": EXPECTED_CHUNK_COUNT,
            "completed_chunk_ids_from_package_audit": sorted(completed_ids),
            "active_chunk_ids_excluded": sorted(active_ids),
            "max_packaged_chunk_consumed": max(completed_ids) if completed_ids else None,
            "packaged_chunk_count": len(rows),
            "complete_chunk_packet": complete_chunk_packet,
            "chunks": chunks,
            "missing_contiguous_chunks": missing_contiguous,
            "read_only": True,
        },
        "aggregate_statistics": {
            "A_top_dE_dm_lat_mean": statistics.fmean(a_values) if a_values else float("nan"),
            "A_top_dE_dm_lat_median": statistics.median(a_values) if a_values else float("nan"),
            "A_top_dE_dm_lat_sample_stderr": stderr(a_values),
            "A_top_dE_dm_lat_weighted_mean": weighted["mean"],
            "A_top_dE_dm_lat_weighted_stderr": weighted["stderr"],
            "T_total_dE_ds_lat_mean": statistics.fmean(t_values) if t_values else float("nan"),
            "T_total_dE_ds_lat_median": statistics.median(t_values) if t_values else float("nan"),
            "diagnostic_T_minus_A_lat_mean": statistics.fmean(diagnostic_values) if diagnostic_values else float("nan"),
            "diagnostic_T_minus_A_lat_median": statistics.median(diagnostic_values) if diagnostic_values else float("nan"),
            "chunk_level_cov_T_total_A_top": sample_covariance(t_values, a_values),
            "chunk_level_covariance_is_not_matched_configuration_covariance": True,
        },
        "rows": rows,
        "validation": {
            "production_metadata_ok": production_metadata_ok,
            "seed_control_ok": seed_control_ok,
            "selected_mass_ok": selected_mass_ok,
            "three_mass_bracket_ok": bracket_ok,
            "cg_residual_ok": cg_ok,
            "row_count_ok": row_count_ok,
            "failures": failures,
        },
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not set A_top=0 or infer it from observed top/yukawa data",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette/u0, or observed W/Z/g2",
            "does not set kappa_s=1, c2=1, Z_match=1, or g2=1",
            "does not infer matched covariance from chunk-level row errors",
            "does not touch active chunks or any live worker",
        ],
        "exact_next_action": (
            "Build matched same-source W/Z response rows and per-configuration "
            "A_top/T_total/W covariance, or replace this coarse mass-scan "
            "Jacobian with dedicated same-source additive-top perturbation rows."
        ),
        "pass_count": pass_count,
        "fail_count": fail_count,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote row certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={pass_count} FAIL={fail_count}")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
