#!/usr/bin/env python3
"""
PR #230 higher-shell Schur/scalar-LSZ chunk checkpoint.

In completed mode this runner audits one L12_T24 higher-shell chunk under the
separate higher-shell roots.  With --allow-pending-active it can also record a
still-running chunk as active-pending run control.  Pending jobs, logs, pid
files, partial directories, and uncheckpointed outputs are not row evidence.
"""

from __future__ import annotations

import argparse
import json
import math
import shlex
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "yt_pr230_schur_higher_shell_rows"
ARTIFACT_ROOT = ROOT / "outputs" / "yt_direct_lattice_correlator_production_schur_higher_shell_rows"
ACTION_CERT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json"
CONTRACT = ROOT / "outputs" / "yt_pr230_schur_higher_shell_production_contract_2026-05-07.json"

EXPECTED_MODES = {
    "0,0,0",
    "1,0,0",
    "0,1,0",
    "0,0,1",
    "1,1,0",
    "1,0,1",
    "0,1,1",
    "1,1,1",
    "2,0,0",
    "0,2,0",
    "0,0,2",
}
EXPECTED_SOURCE_SHIFTS = {-0.01, 0.0, 0.01}
EXPECTED_MASSES = [0.45, 0.75, 1.05]
EXPECTED_SELECTED_MASS = 0.75
EXPECTED_MEASUREMENTS = 16
EXPECTED_THERM = 1000
EXPECTED_SEPARATION = 20
EXPECTED_SEED_BASE = 2026057000
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
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def approx_set(values: list[Any]) -> set[float]:
    out: set[float] = set()
    for value in values:
        if finite(value):
            out.add(round(float(value), 8))
    return out


def expected_seed(chunk_index: int) -> int:
    return EXPECTED_SEED_BASE + int(chunk_index)


def volume_seed(base_seed: int, spatial_l: int = 12, time_l: int = 24) -> int:
    return int(base_seed + 1000003 * spatial_l + 9176 * time_l)


def chunk_output(chunk_index: int, row_date: str) -> Path:
    return OUTPUT_ROOT / f"yt_pr230_schur_higher_shell_rows_L12_T24_chunk{chunk_index:03d}_{row_date}.json"


def chunk_artifact(chunk_index: int) -> Path:
    return ARTIFACT_ROOT / f"L12_T24_chunk{chunk_index:03d}" / "L12xT24" / "ensemble_measurement.json"


def default_checkpoint_output(chunk_index: int, checkpoint_date: str) -> Path:
    return ROOT / "outputs" / f"yt_pr230_schur_higher_shell_chunk{chunk_index:03d}_checkpoint_{checkpoint_date}.json"


def first_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if isinstance(ensembles, list) and len(ensembles) == 1 and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def active_process_rows() -> list[dict[str, Any]]:
    proc = subprocess.run(
        ["ps", "-Ao", "pid=,command="],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if proc.returncode != 0:
        return []
    rows: list[dict[str, Any]] = []
    for line in proc.stdout.splitlines():
        if "yt_direct_lattice_correlator_production.py" not in line:
            continue
        if (
            "yt_pr230_schur_higher_shell_rows" not in line
            and "yt_direct_lattice_correlator_production_schur_higher_shell_rows" not in line
        ):
            continue
        parts = line.strip().split(maxsplit=1)
        try:
            pid = int(parts[0])
        except (IndexError, ValueError):
            pid = -1
        command = parts[1] if len(parts) > 1 else line.strip()
        try:
            argv = shlex.split(command)
        except ValueError:
            argv = []
        if not any(token.endswith("yt_direct_lattice_correlator_production.py") for token in argv):
            continue
        chunk = None
        for index in range(1, 64):
            if f"chunk{index:03d}" in command:
                chunk = index
                break
        rows.append({"pid": pid, "chunk_index": chunk, "command": command})
    return rows


def mode_rows_with_timeseries(rows: dict[str, Any], labels: tuple[str, ...]) -> dict[str, bool]:
    status: dict[str, bool] = {}
    for mode in EXPECTED_MODES:
        row = rows.get(mode, {}) if isinstance(rows, dict) else {}
        ok = isinstance(row, dict)
        for label in labels:
            series = row.get(f"{label}_timeseries") if ok else None
            ok = ok and isinstance(series, list) and len(series) == EXPECTED_MEASUREMENTS
            ok = ok and finite(row.get(f"{label}_real")) and finite(row.get(f"{label}_imag"))
        status[mode] = bool(ok)
    return status


def contract_row(contract: dict[str, Any], chunk_index: int) -> dict[str, Any]:
    rows = contract.get("future_noncollision_preview", [])
    if not isinstance(rows, list):
        return {}
    for row in rows:
        if isinstance(row, dict) and row.get("chunk_index") == chunk_index:
            return row
    return {}


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunk-index", type=int, required=True)
    parser.add_argument("--row-date", default="2026-05-07", help="Date suffix on the chunk row JSON.")
    parser.add_argument("--checkpoint-date", default="2026-05-12", help="Date suffix on checkpoint JSON.")
    parser.add_argument("--output", help="Optional checkpoint JSON path.")
    parser.add_argument(
        "--allow-pending-active",
        action="store_true",
        help="Pass with active-pending status if the chunk output has not been written yet.",
    )
    return parser


def pending_result(
    chunk_index: int,
    chunk_path: Path,
    artifact_path: Path,
    active_for_chunk: list[dict[str, Any]],
    pending_allowed: bool,
) -> dict[str, Any]:
    report(
        "chunk-output-present-or-active-pending",
        pending_allowed,
        f"output={rel(chunk_path)} active_pids={[row.get('pid') for row in active_for_chunk]}",
    )
    report("does-not-authorize-retained-proposal", True, "pending active chunk is run-control only")
    return {
        "actual_current_surface_status": (
            f"run-control / higher-shell Schur scalar-LSZ chunk{chunk_index:03d} active-pending checkpoint; "
            "no completed row JSON present"
            if pending_allowed
            else f"open / higher-shell Schur scalar-LSZ chunk{chunk_index:03d} missing row JSON"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "A pending active higher-shell chunk is run-control state only.  It is not row evidence, "
            "complete monotonicity, scalar-pole authority, canonical O_H authority, or y_t closure."
        ),
        "bare_retained_allowed": False,
        "chunk_index": chunk_index,
        "completed": False,
        "pending_active": bool(active_for_chunk),
        "active_process_rows": active_for_chunk,
        "chunk_output": rel(chunk_path),
        "chunk_artifact": rel(artifact_path),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat active processes, logs, pid files, or partial directories as row evidence",
            "does not treat C_sx/C_xx as canonical-Higgs C_sH/C_HH",
            "does not claim complete monotonicity, scalar pole authority, FV/IR authority, canonical O_H, source-overlap, or W/Z response",
            "does not set kappa_s = 1, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Wait for completed chunk JSON, then rerun without --allow-pending-active "
            "to validate production row schema and seed control."
        ),
        "checkpoint_passed": FAIL_COUNT == 0,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }


def main() -> int:
    args = build_arg_parser().parse_args()
    chunk_index = int(args.chunk_index)
    output_path = (
        Path(args.output)
        if args.output
        else default_checkpoint_output(chunk_index, args.checkpoint_date)
    )
    chunk_path = chunk_output(chunk_index, args.row_date)
    artifact_path = chunk_artifact(chunk_index)
    base_seed = expected_seed(chunk_index)

    print(f"PR #230 higher-shell Schur/scalar-LSZ chunk{chunk_index:03d} checkpoint")
    print("=" * 78)

    chunk = load_json(chunk_path)
    artifact = load_json(artifact_path)
    action = load_json(ACTION_CERT)
    contract = load_json(CONTRACT)
    active_rows = active_process_rows()
    active_for_chunk = [row for row in active_rows if row.get("chunk_index") == chunk_index]
    completed = bool(chunk)
    pending_active = (not completed) and bool(active_for_chunk)
    pending_allowed = bool(args.allow_pending_active and pending_active)

    if not completed:
        result = pending_result(
            chunk_index, chunk_path, artifact_path, active_for_chunk, pending_allowed
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"\nWrote certificate: {rel(output_path)}")
        print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
        return 0 if FAIL_COUNT == 0 else 1

    metadata = chunk.get("metadata", {})
    run_control = metadata.get("run_control", {}) if isinstance(metadata.get("run_control"), dict) else {}
    ensemble = first_ensemble(chunk)
    source = ensemble.get("scalar_source_response_analysis", {})
    lsz = ensemble.get("scalar_two_point_lsz_analysis", {})
    source_higgs = ensemble.get("source_higgs_cross_correlator_analysis", {})
    seed_control = ensemble.get("rng_seed_control", {})
    source_higgs_meta = metadata.get("source_higgs_cross_correlator", {})
    source_meta = metadata.get("scalar_source_response", {})
    lsz_meta = metadata.get("scalar_two_point_lsz", {})
    policy = metadata.get("fh_lsz_measurement_policy", {})

    source_energy_fits = source.get("energy_fits", []) if isinstance(source, dict) else []
    source_shifts = approx_set(
        [row.get("source_shift_lat") for row in source_energy_fits if isinstance(row, dict)]
    )
    lsz_mode_rows = lsz.get("mode_rows", {}) if isinstance(lsz, dict) else {}
    source_higgs_mode_rows = source_higgs.get("mode_rows", {}) if isinstance(source_higgs, dict) else {}
    lsz_timeseries_status = mode_rows_with_timeseries(lsz_mode_rows, ("C_ss",))
    source_higgs_timeseries_status = mode_rows_with_timeseries(
        source_higgs_mode_rows, ("C_ss", "C_sx", "C_xx")
    )
    legacy_timeseries_status = mode_rows_with_timeseries(
        source_higgs_mode_rows, ("C_sH", "C_HH")
    )
    alias_meta = (
        source_higgs.get("two_source_taste_radial_row_aliases", {})
        if isinstance(source_higgs, dict)
        else {}
    )
    firewall = source_higgs_meta.get("firewall", {}) if isinstance(source_higgs_meta, dict) else {}
    action_firewall = action.get("forbidden_firewall", {})
    contract_entry = contract_row(contract, chunk_index)

    run_control_ok = (
        metadata.get("phase") == "production"
        and run_control.get("seed") == base_seed
        and run_control.get("volumes") == "12x24"
        and run_control.get("thermalization_sweeps") == EXPECTED_THERM
        and run_control.get("measurement_sweeps") == EXPECTED_MEASUREMENTS
        and run_control.get("measurement_separation_sweeps") == EXPECTED_SEPARATION
        and run_control.get("engine") == "numba"
        and run_control.get("production_targets") is True
    )
    seed_ok = (
        isinstance(seed_control, dict)
        and seed_control.get("seed_control_version") == EXPECTED_SEED_CONTROL_VERSION
        and seed_control.get("base_seed") == base_seed
        and seed_control.get("gauge_rng_seed") == volume_seed(base_seed)
        and seed_control.get("numba_gauge_seeded_before_thermalization") is True
    )
    selected_mass_ok = (
        ensemble.get("selected_mass_parameter") == EXPECTED_SELECTED_MASS
        and policy.get("selected_mass_parameter") == EXPECTED_SELECTED_MASS
        and policy.get("scalar_source_response_selected_mass_only") is True
        and policy.get("scalar_two_point_lsz_selected_mass_only") is True
        and policy.get("source_higgs_cross_correlator_selected_mass_only") is True
    )
    mass_scan = ensemble.get("mass_parameter_scan", [])
    mass_scan_ok = (
        isinstance(mass_scan, list)
        and approx_set([row.get("m_bare_lat") for row in mass_scan if isinstance(row, dict)])
        == {round(x, 8) for x in EXPECTED_MASSES}
    )
    source_ok = (
        isinstance(source, dict)
        and source_shifts == {round(x, 8) for x in EXPECTED_SOURCE_SHIFTS}
        and isinstance(source.get("per_configuration_slopes"), list)
        and len(source.get("per_configuration_slopes")) == EXPECTED_MEASUREMENTS
        and isinstance(source.get("per_configuration_effective_energies"), list)
        and len(source.get("per_configuration_effective_energies")) == EXPECTED_MEASUREMENTS
        and (
            source.get("used_as_physical_yukawa_readout") is False
            or (
                source.get("used_as_physical_yukawa_readout") is None
                and isinstance(source_meta, dict)
                and source_meta.get("used_as_physical_yukawa_readout") is False
            )
        )
    )
    lsz_ok = (
        isinstance(lsz, dict)
        and EXPECTED_MODES <= set(lsz_mode_rows)
        and all(lsz_timeseries_status.values())
        and lsz.get("physical_higgs_normalization") == "not_derived"
        and (
            lsz.get("used_as_physical_yukawa_readout") is False
            or (
                lsz.get("used_as_physical_yukawa_readout") is None
                and isinstance(lsz_meta, dict)
                and lsz_meta.get("used_as_physical_yukawa_readout") is False
            )
        )
    )
    source_higgs_ok = (
        isinstance(source_higgs, dict)
        and EXPECTED_MODES <= set(source_higgs_mode_rows)
        and all(source_higgs_timeseries_status.values())
        and all(legacy_timeseries_status.values())
        and alias_meta.get("available") is True
        and source_higgs.get("canonical_higgs_operator_identity_passed") is False
        and source_higgs.get("used_as_physical_yukawa_readout") is False
        and isinstance(source_higgs.get("pole_residue_rows"), list)
        and len(source_higgs.get("pole_residue_rows")) == 0
    )
    metadata_source_higgs_ok = (
        isinstance(source_higgs_meta, dict)
        and source_higgs_meta.get("enabled") is True
        and source_higgs_meta.get("selected_mass_only") is True
        and source_higgs_meta.get("selected_mass_parameter") == EXPECTED_SELECTED_MASS
        and source_higgs_meta.get("used_as_physical_yukawa_readout") is False
        and isinstance(source_higgs_meta.get("operator"), dict)
        and source_higgs_meta.get("operator", {}).get("operator_id")
        == "pr230_taste_radial_hypercube_flip_source_v1"
    )
    firewall_ok = (
        isinstance(firewall, dict)
        and all(value is False for value in firewall.values())
        and isinstance(action_firewall, dict)
        and all(value is False for value in action_firewall.values())
    )
    contract_ok = (
        contract.get("higher_shell_schur_production_contract_passed") is True
        and isinstance(contract_entry, dict)
        and contract_entry.get("seed") == base_seed
        and contract_entry.get("output") == rel(chunk_path)
        and "--resume" not in list(contract_entry.get("command") or [])
    )
    artifact_consistent = bool(artifact) and artifact == ensemble
    proposal_firewall_ok = (
        chunk.get("metadata", {}).get("uses_prior_ward_chain") is False
        and chunk.get("metadata", {}).get("uses_composite_matrix_element_route") is False
        and chunk.get("metadata", {}).get("uses_coupling_definition_route") is False
    )

    report("chunk-output-present", bool(chunk), rel(chunk_path))
    report("volume-artifact-present", bool(artifact), rel(artifact_path))
    report("volume-artifact-matches-certificate-ensemble", artifact_consistent, rel(artifact_path))
    report("production-run-control", run_control_ok, str(run_control))
    report("numba-seed-control", seed_ok, str(seed_control))
    report("three-mass-scan-preserved", mass_scan_ok, str(mass_scan))
    report("selected-mass-only-policy", selected_mass_ok, str(policy))
    report("scalar-source-response-timeseries", source_ok, f"shifts={sorted(source_shifts)}")
    report("higher-shell-scalar-lsz-Css-timeseries", lsz_ok, str(lsz_timeseries_status))
    report("higher-shell-source-higgs-Csx-Cxx-timeseries", source_higgs_ok, str(source_higgs_timeseries_status))
    report("source-higgs-metadata-firewall", metadata_source_higgs_ok, str(source_higgs_meta))
    report("forbidden-input-firewalls-clean", firewall_ok, f"source={firewall} action={action_firewall}")
    report("contract-row-consistent", contract_ok, str(contract_entry))
    report("proposal-firewall-preserved", proposal_firewall_ok, str(metadata))
    report("does-not-authorize-retained-proposal", True, "single higher-shell chunk is support only")

    result = {
        "actual_current_surface_status": (
            f"bounded-support / higher-shell Schur scalar-LSZ chunk{chunk_index:03d} row checkpoint"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "A single completed higher-shell chunk is partial row support only.  "
            "It does not identify the taste-radial source with canonical O_H, "
            "does not derive kappa_s, and does not provide complete monotonicity, "
            "pole/FV/IR, or retained-route authority."
        ),
        "bare_retained_allowed": False,
        "chunk_index": chunk_index,
        "completed": True,
        "checkpoint_passed": FAIL_COUNT == 0,
        "chunk_output": rel(chunk_path),
        "chunk_artifact": rel(artifact_path),
        "contract": rel(CONTRACT),
        "action_certificate": rel(ACTION_CERT),
        "chunk_summary": {
            "phase": metadata.get("phase"),
            "seed": run_control.get("seed"),
            "expected_seed": base_seed,
            "seed_control_version": seed_control.get("seed_control_version")
            if isinstance(seed_control, dict)
            else None,
            "selected_mass_parameter": ensemble.get("selected_mass_parameter"),
            "mass_scan_count": len(mass_scan) if isinstance(mass_scan, list) else None,
            "scalar_lsz_modes": sorted(lsz_mode_rows) if isinstance(lsz_mode_rows, dict) else [],
            "source_higgs_modes": sorted(source_higgs_mode_rows)
            if isinstance(source_higgs_mode_rows, dict)
            else [],
            "source_higgs_aliases": alias_meta,
            "pole_residue_rows_count": len(source_higgs.get("pole_residue_rows", []))
            if isinstance(source_higgs, dict)
            else None,
            "active_process_rows_for_chunk": active_for_chunk,
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat one higher-shell chunk as a complete scalar-LSZ row packet",
            "does not treat C_sx/C_xx as canonical-Higgs C_sH/C_HH",
            "does not claim complete monotonicity, scalar pole authority, FV/IR authority, canonical O_H, source-overlap, or W/Z response",
            "does not set kappa_s = 1, c2 = 1, or Z_match = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Accumulate completed higher-shell chunks, run this checkpoint on each, "
            "combine higher-shell rows, then run complete-monotonicity, "
            "threshold/model-class/pole/FV/IR, and canonical-source bridge gates."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(output_path)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
