#!/usr/bin/env python3
"""
PR #230 two-source taste-radial row production manifest.

This runner turns the completed taste-radial row contract into a guarded
production launch plan for C_sx/C_xx rows.  It does not launch jobs and it does
not treat a manifest, dry run, smoke row, or process table as physics evidence.
The planned rows remain second-source taste-radial rows, not canonical-Higgs
C_sH/C_HH rows, until a separate O_H/source-overlap or physical-response bridge
closes.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
ACTION_CERT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json"
ROW_CONTRACT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_contract_2026-05-06.json"
FUTURE_COMBINED_ROWS = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json"
CHUNK_OUTPUT_ROOT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_rows"
PRODUCTION_OUTPUT_ROOT = (
    ROOT / "outputs" / "yt_direct_lattice_correlator_production_two_source_taste_radial_rows"
)

CHUNK_COUNT = 63
MAX_CONCURRENT_RECOMMENDED = 3
MASS_SPEC = "0.45,0.75,1.05"
SOURCE_SHIFTS = "-0.01,0.0,0.01"
MOMENTUM_MODES = "0,0,0;1,0,0;0,1,0;0,0,1"
SCALAR_TWO_POINT_NOISES = 16
SOURCE_HIGGS_CROSS_NOISES = 16
THERM = 1000
MEASUREMENTS_PER_CHUNK = 16
SEPARATION = 20
SEED_BASE = 2026056000

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


def chunk_output(index: int) -> Path:
    return CHUNK_OUTPUT_ROOT / f"yt_pr230_two_source_taste_radial_rows_L12_T24_chunk{index:03d}_2026-05-06.json"


def chunk_production_dir(index: int) -> Path:
    return PRODUCTION_OUTPUT_ROOT / f"L12_T24_chunk{index:03d}"


def chunk_seed(index: int) -> int:
    return SEED_BASE + index


def production_command(index: int) -> list[str]:
    return [
        "python3",
        "scripts/yt_direct_lattice_correlator_production.py",
        "--volumes",
        "12x24",
        "--masses",
        MASS_SPEC,
        "--therm",
        str(THERM),
        "--measurements",
        str(MEASUREMENTS_PER_CHUNK),
        "--separation",
        str(SEPARATION),
        "--engine",
        "numba",
        "--production-targets",
        f"--scalar-source-shifts={SOURCE_SHIFTS}",
        "--scalar-two-point-modes",
        MOMENTUM_MODES,
        "--scalar-two-point-noises",
        str(SCALAR_TWO_POINT_NOISES),
        "--source-higgs-cross-modes",
        MOMENTUM_MODES,
        "--source-higgs-cross-noises",
        str(SOURCE_HIGGS_CROSS_NOISES),
        "--source-higgs-operator-certificate",
        rel(ACTION_CERT),
        "--production-output-dir",
        rel(chunk_production_dir(index)),
        "--seed",
        str(chunk_seed(index)),
        "--output",
        rel(chunk_output(index)),
    ]


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
    tokens = [
        "yt_direct_lattice_correlator_production.py",
        "yt_pr230_two_source_taste_radial_rows",
        "yt_direct_lattice_correlator_production_two_source_taste_radial_rows",
    ]
    for line in proc.stdout.splitlines():
        if not all(token in line for token in (tokens[0],)) or not any(
            token in line for token in tokens[1:]
        ):
            continue
        parts = line.strip().split(maxsplit=1)
        try:
            pid = int(parts[0])
        except (IndexError, ValueError):
            pid = -1
        command = parts[1] if len(parts) > 1 else line.strip()
        chunk = None
        for index in range(1, CHUNK_COUNT + 1):
            if f"chunk{index:03d}" in command:
                chunk = index
                break
        rows.append({"pid": pid, "chunk_index": chunk, "command": command})
    return rows


def chunk_state(index: int) -> dict[str, Any]:
    out = chunk_output(index)
    pdir = chunk_production_dir(index)
    entries = sorted(child.name for child in pdir.iterdir()) if pdir.exists() else []
    return {
        "chunk_index": index,
        "seed": chunk_seed(index),
        "output": rel(out),
        "output_present": out.exists(),
        "production_output_dir": rel(pdir),
        "production_output_dir_present": pdir.exists(),
        "production_output_dir_entries": entries,
        "empty_or_partial_dir_counts_as_evidence": False,
        "command": production_command(index),
    }


def main() -> int:
    print("PR #230 two-source taste-radial row production manifest")
    print("=" * 78)

    harness_text = HARNESS.read_text(encoding="utf-8") if HARNESS.exists() else ""
    action = load_json(ACTION_CERT)
    row_contract = load_json(ROW_CONTRACT)
    active_rows = active_process_rows()
    chunks = [chunk_state(index) for index in range(1, CHUNK_COUNT + 1)]
    completed_chunks = [row["chunk_index"] for row in chunks if row["output_present"]]
    partial_dirs = [
        row["chunk_index"]
        for row in chunks
        if row["production_output_dir_present"] and not row["output_present"]
    ]
    commands_have_no_resume = all("--resume" not in row["command"] for row in chunks)
    commands_use_distinct_outputs = len({row["output"] for row in chunks}) == CHUNK_COUNT
    commands_use_distinct_dirs = len({row["production_output_dir"] for row in chunks}) == CHUNK_COUNT
    operator_payload = action.get("operator_certificate_payload", {})
    sparse_vertex = action.get("sparse_vertex", {}) or operator_payload.get("sparse_vertex", {})

    harness_has_cli = all(
        token in harness_text
        for token in (
            "--source-higgs-cross-modes",
            "--source-higgs-cross-noises",
            "--source-higgs-operator-certificate",
            "source_higgs_cross_correlator_selected_mass_only",
            "C_sx_timeseries",
            "C_xx_timeseries",
        )
    )
    action_support_ok = (
        action.get("two_source_taste_radial_action_passed") is True
        and action.get("proposal_allowed") is False
        and action.get("canonical_higgs_operator_identity_passed") is False
        and sparse_vertex.get("kind") == "taste_radial_spatial_hypercube_flip"
        and operator_payload.get("canonical_higgs_operator_identity_passed") is False
    )
    row_contract_ok = (
        row_contract.get("two_source_taste_radial_row_contract_passed") is True
        and row_contract.get("proposal_allowed") is False
        and row_contract.get("future_file_presence", {}).get("taste_radial_production_rows")
        is False
    )
    future_combined_absent = not FUTURE_COMBINED_ROWS.exists()
    no_active_collision = not active_rows
    no_completed_chunk_overwrite = not completed_chunks
    no_partial_dir_collision = not partial_dirs

    report("harness-present", HARNESS.exists(), rel(HARNESS))
    report("harness-has-taste-radial-row-cli", harness_has_cli, rel(HARNESS))
    report("action-certificate-present", bool(action), rel(ACTION_CERT))
    report("action-certificate-support-only", action_support_ok, action.get("actual_current_surface_status", ""))
    report("row-contract-present", bool(row_contract), rel(ROW_CONTRACT))
    report("row-contract-support-only", row_contract_ok, row_contract.get("actual_current_surface_status", ""))
    report("future-combined-row-file-absent", future_combined_absent, rel(FUTURE_COMBINED_ROWS))
    report("process-table-has-no-active-row-collision", no_active_collision, f"active={len(active_rows)}")
    report("planned-chunk-count-is-production-wave", len(chunks) == CHUNK_COUNT, f"chunks={len(chunks)}")
    report("planned-commands-have-no-resume", commands_have_no_resume, "new row wave must not reuse old artifacts")
    report("planned-output-paths-distinct", commands_use_distinct_outputs, "one JSON per chunk")
    report("planned-production-dirs-distinct", commands_use_distinct_dirs, "one artifact dir per chunk")
    report("no-completed-chunk-would-be-overwritten", no_completed_chunk_overwrite, f"present={completed_chunks}")
    report("no-partial-output-dir-collision", no_partial_dir_collision, f"partial_dirs={partial_dirs}")
    report(
        "selected-mass-and-normal-cache-preserved",
        "selected_mass_only_for_scalar_fh_lsz" in harness_text
        and "normal_cache: dict[str, NormalEquationSystem]" in harness_text,
        "uses optimized FH/LSZ harness path",
    )
    report("does-not-authorize-retained-proposal", True, "manifest and run control only")

    launch_guard_allows_new_workers = (
        FAIL_COUNT == 0 and no_active_collision and no_completed_chunk_overwrite and no_partial_dir_collision
    )
    result = {
        "actual_current_surface_status": (
            "bounded-support / two-source taste-radial C_sx/C_xx production manifest; rows absent"
        ),
        "verdict": (
            "The taste-radial second-source operator and C_sx/C_xx row contract "
            "are now wired into a concrete L12_T24 production-row launch plan. "
            "The plan uses the optimized selected-mass FH/LSZ harness path, "
            "keeps the three-mass top scan, uses seed-controlled chunk outputs, "
            "forbids --resume, and records collision state.  No production "
            "row, pole residue, canonical O_H identity, scalar-LSZ "
            "normalization, or retained/proposed-retained closure is claimed."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "A production manifest is run-control support only.  The C_sx/C_xx "
            "rows are absent, and even completed taste-radial rows would remain "
            "second-source rows until canonical O_H/source-overlap or genuine "
            "physical-response authority closes."
        ),
        "bare_retained_allowed": False,
        "manifest_passed": FAIL_COUNT == 0,
        "launch_guard_allows_new_workers": launch_guard_allows_new_workers,
        "dry_run_only": True,
        "operator_id": action.get("operator_id"),
        "operator_certificate": rel(ACTION_CERT),
        "row_contract_certificate": rel(ROW_CONTRACT),
        "future_combined_rows": rel(FUTURE_COMBINED_ROWS),
        "future_combined_rows_present": FUTURE_COMBINED_ROWS.exists(),
        "production_policy": {
            "volume": "12x24",
            "chunk_count": CHUNK_COUNT,
            "measurements_per_chunk": MEASUREMENTS_PER_CHUNK,
            "total_planned_measurements": CHUNK_COUNT * MEASUREMENTS_PER_CHUNK,
            "masses": [float(x) for x in MASS_SPEC.split(",")],
            "selected_mass_parameter": 0.75,
            "scalar_source_shifts": [-0.01, 0.0, 0.01],
            "momentum_modes": [[int(x) for x in row.split(",")] for row in MOMENTUM_MODES.split(";")],
            "scalar_two_point_noises": SCALAR_TWO_POINT_NOISES,
            "source_higgs_cross_noises": SOURCE_HIGGS_CROSS_NOISES,
            "recommended_max_concurrent_workers": MAX_CONCURRENT_RECOMMENDED,
            "resume_allowed": False,
            "evidence_requires_completed_chunk_certificates": True,
        },
        "active_process_rows": active_rows,
        "completed_chunk_indices": completed_chunks,
        "partial_output_dir_indices": partial_dirs,
        "chunk_commands": chunks,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not launch jobs or fabricate row data",
            "does not treat a manifest, dry run, smoke row, process row, empty directory, or partial directory as physics evidence",
            "does not treat C_sx/C_xx as canonical-Higgs C_sH/C_HH rows",
            "does not identify the taste-radial source with canonical O_H",
            "does not set kappa_s = 1, c2 = 1, or Z_match = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Launch the missing chunks with max concurrency 2-3 using the recorded "
            "commands, then run per-chunk schema gates, combine C_sx/C_xx rows, "
            "extract pole residues/FV/IR diagnostics, and separately close "
            "canonical O_H/source-overlap or genuine physical-response authority "
            "before any proposal wording."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
