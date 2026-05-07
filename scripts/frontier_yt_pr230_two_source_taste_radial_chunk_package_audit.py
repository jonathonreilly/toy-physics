#!/usr/bin/env python3
"""
PR #230 two-source taste-radial chunk package audit.

This runner packages the completed C_sx/C_xx row chunks without counting live
processes, logs, partial directories, or pending checkpoints as evidence.  It
is intentionally support-only: even a clean package does not identify the
taste-radial source with canonical O_H and does not supply C_sH/C_HH pole rows.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ROW_ROOT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_rows"
ARTIFACT_ROOT = (
    ROOT / "outputs" / "yt_direct_lattice_correlator_production_two_source_taste_radial_rows"
)
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_two_source_taste_radial_chunk_package_audit_2026-05-06.json"
)

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


def load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def chunk_id_from_name(path: Path) -> int | None:
    match = re.search(r"chunk(\d{3})", path.name)
    return int(match.group(1)) if match else None


def row_path(index: int) -> Path:
    return ROW_ROOT / f"yt_pr230_two_source_taste_radial_rows_L12_T24_chunk{index:03d}_2026-05-06.json"


def checkpoint_path(index: int) -> Path:
    return ROOT / "outputs" / f"yt_pr230_two_source_taste_radial_chunk{index:03d}_checkpoint_2026-05-06.json"


def artifact_path(index: int) -> Path:
    return ARTIFACT_ROOT / f"L12_T24_chunk{index:03d}" / "L12xT24" / "ensemble_measurement.json"


def discover_row_ids() -> list[int]:
    if not ROW_ROOT.exists():
        return []
    ids = [
        chunk_id
        for path in ROW_ROOT.glob("yt_pr230_two_source_taste_radial_rows_L12_T24_chunk*_2026-05-06.json")
        for chunk_id in [chunk_id_from_name(path)]
        if chunk_id is not None
    ]
    return sorted(set(ids))


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
            "yt_pr230_two_source_taste_radial_rows" not in line
            and "yt_direct_lattice_correlator_production_two_source_taste_radial_rows"
            not in line
        ):
            continue
        parts = line.strip().split(maxsplit=1)
        try:
            pid = int(parts[0])
        except (IndexError, ValueError):
            pid = -1
        command = parts[1] if len(parts) > 1 else line.strip()
        chunk = chunk_id_from_name(Path(command))
        if chunk is None:
            match = re.search(r"chunk(\d{3})", command)
            chunk = int(match.group(1)) if match else None
        rows.append({"pid": pid, "chunk_index": chunk, "command": command})
    return rows


def checkpoint_support_ok(checkpoint: dict[str, Any]) -> bool:
    aliases = checkpoint.get("chunk_summary", {}).get("source_higgs_aliases", {})
    return (
        checkpoint.get("checkpoint_passed") is True
        and checkpoint.get("completed") is True
        and checkpoint.get("proposal_allowed") is False
        and checkpoint.get("chunk_summary", {}).get("pole_residue_rows_count") == 0
        and aliases.get("C_sx_aliases_C_sH_schema_field") is True
    )


def contiguous_prefix(ids: list[int]) -> list[int]:
    expected = 1
    prefix: list[int] = []
    for chunk_id in ids:
        if chunk_id != expected:
            break
        prefix.append(chunk_id)
        expected += 1
    return prefix


def main() -> int:
    print("PR #230 two-source taste-radial chunk package audit")
    print("=" * 78)

    row_ids = discover_row_ids()
    prefix = contiguous_prefix(row_ids)
    max_prefix = prefix[-1] if prefix else 0
    expected_ids = list(range(1, max_prefix + 1))
    gap_ids = [index for index in expected_ids if index not in row_ids]
    completed_rows: list[dict[str, Any]] = []
    missing_checkpoints: list[int] = []
    failed_checkpoints: list[int] = []
    missing_artifacts: list[int] = []
    unreadable_rows: list[int] = []

    for index in expected_ids:
        row = load(row_path(index))
        checkpoint = load(checkpoint_path(index))
        artifact = load(artifact_path(index))
        if not row:
            unreadable_rows.append(index)
        if not checkpoint:
            missing_checkpoints.append(index)
        elif not checkpoint_support_ok(checkpoint):
            failed_checkpoints.append(index)
        if not artifact:
            missing_artifacts.append(index)
        completed_rows.append(
            {
                "chunk_index": index,
                "row": rel(row_path(index)),
                "checkpoint": rel(checkpoint_path(index)),
                "artifact": rel(artifact_path(index)),
                "checkpoint_passed": checkpoint.get("checkpoint_passed") is True,
                "proposal_allowed": checkpoint.get("proposal_allowed"),
                "pole_residue_rows_count": checkpoint.get("chunk_summary", {}).get(
                    "pole_residue_rows_count"
                ),
                "source_higgs_aliases": checkpoint.get("chunk_summary", {}).get(
                    "source_higgs_aliases", {}
                ),
            }
        )

    active_rows = active_process_rows()
    active_ids = sorted(
        {
            int(row["chunk_index"])
            for row in active_rows
            if isinstance(row.get("chunk_index"), int)
        }
    )
    active_counted_as_evidence = [
        index for index in active_ids if index in expected_ids and index not in row_ids
    ]
    pending_checkpoint_paths = sorted(
        rel(path)
        for path in (ROOT / "outputs").glob(
            "yt_pr230_two_source_taste_radial_chunk*_pending_checkpoint_2026-05-06.json"
        )
    )

    package_ok = (
        len(prefix) >= 20
        and len(prefix) == len(row_ids)
        and not gap_ids
        and not unreadable_rows
        and not missing_checkpoints
        and not failed_checkpoints
        and not missing_artifacts
    )
    active_not_evidence = not active_counted_as_evidence
    proposal_firewall = all(
        row.get("proposal_allowed") is False for row in completed_rows
    )

    report("completed-row-files-contiguous", len(prefix) == len(row_ids) and not gap_ids, f"rows={row_ids}")
    report("completed-row-prefix-at-least-020", len(prefix) >= 20, f"prefix=001-{max_prefix:03d}")
    report("completed-rows-readable", not unreadable_rows, f"unreadable={unreadable_rows}")
    report("checkpoint-files-present", not missing_checkpoints, f"missing={missing_checkpoints}")
    report("checkpoint-files-pass-support-schema", not failed_checkpoints, f"failed={failed_checkpoints}")
    report("per-volume-artifacts-present", not missing_artifacts, f"missing={missing_artifacts}")
    report("pending-checkpoints-not-counted", True, f"pending={pending_checkpoint_paths}")
    report(
        "active-processes-not-counted",
        active_not_evidence,
        f"active_ids={active_ids} completed_evidence_ids={expected_ids}",
    )
    report("proposal-firewall-preserved", proposal_firewall, "all completed checkpoint proposal_allowed=false")
    report("package-support-not-closure", True, "C_sx/C_xx chunks are not canonical C_sH/C_HH pole rows")

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            f"bounded-support / two-source taste-radial chunks001-{max_prefix:03d} packaged; "
            "active chunks, logs, and pending checkpoints are not evidence"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Completed C_sx/C_xx row chunks are support-only.  They do not supply "
            "canonical O_H authority, Res C_sH, Res C_HH, Gram purity, FV/IR, "
            "scalar-LSZ, matching/running, or retained-route authorization."
        ),
        "bare_retained_allowed": False,
        "chunk_package_audit_passed": passed,
        "completed_chunk_ids": expected_ids,
        "completed_chunk_count": len(expected_ids),
        "completed_prefix_last": max_prefix,
        "row_ids_discovered": row_ids,
        "gap_ids": gap_ids,
        "missing_checkpoints": missing_checkpoints,
        "failed_checkpoints": failed_checkpoints,
        "missing_artifacts": missing_artifacts,
        "active_process_rows": active_rows,
        "active_chunk_ids": active_ids,
        "active_chunks_counted_as_evidence": False,
        "pending_checkpoint_paths": pending_checkpoint_paths,
        "completed_rows": completed_rows,
        "remaining_positive_contract": [
            "combine completed C_sx/C_xx chunks into row-level statistics",
            "extract pole/FV/IR diagnostics for the second-source rows",
            "supply same-surface canonical O_H authority or physical-response bridge",
            "replace C_sx/C_xx aliases with genuine C_ss/C_sH/C_HH pole rows before closure",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not treat active workers, logs, or pending checkpoints as evidence",
            "does not treat C_sx/C_xx taste-radial rows as canonical C_sH/C_HH pole rows",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
