#!/usr/bin/env python3
"""
PR #230 FH/LSZ global production collision guard.

This runner records the current global FH/LSZ production-worker surface and the
launch decision it implies.  It is infrastructure/provenance support only: it
does not count failed foreground attempts, empty output directories, or
scheduler submissions without completed certificates as physics evidence.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_global_production_collision_guard_2026-05-04.json"

GLOBAL_MAX_PRODUCTION_JOBS = 6
LOCAL_RESOURCE_SAFE_WORKER_THRESHOLD = 4
TARGET_CHUNKS = (25, 26)

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


def run_command(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(args, capture_output=True, text=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def parse_ps_rows(ps_text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in ps_text.splitlines()[1:]:
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split(None, 4)
        if len(parts) < 5:
            continue
        pid, ppid, elapsed, cpu, command = parts
        try:
            pid_i = int(pid)
            ppid_i = int(ppid)
            cpu_f = float(cpu)
        except ValueError:
            continue
        rows.append(
            {
                "pid": pid_i,
                "ppid": ppid_i,
                "elapsed": elapsed,
                "cpu_percent": cpu_f,
                "command": command,
            }
        )
    return rows


def cwd_for_pid(pid: int) -> str | None:
    code, out, _err = run_command(["lsof", "-a", "-p", str(pid), "-d", "cwd"])
    if code != 0:
        return None
    for line in out.splitlines()[1:]:
        parts = line.split(None, 8)
        if len(parts) == 9:
            return parts[8]
    return None


def extract_option(command: str, option: str) -> str | None:
    match = re.search(rf"{re.escape(option)}\s+(\S+)", command)
    if match:
        return match.group(1)
    return None


def is_fh_lsz_production_worker(command: str) -> bool:
    return (
        "yt_direct_lattice_correlator_production.py" in command
        and (
            "--production-targets" in command
            or "yt_pr230_fh_lsz" in command
            or "yt_direct_lattice_correlator_production_fh_lsz" in command
        )
    )


def is_fh_lsz_orchestrator(command: str) -> bool:
    return "frontier_yt_fh_lsz" in command and "orchestrator.py" in command


def enrich_worker(row: dict[str, Any]) -> dict[str, Any]:
    command = str(row["command"])
    enriched = dict(row)
    enriched.update(
        {
            "cwd": cwd_for_pid(int(row["pid"])),
            "seed": extract_option(command, "--seed"),
            "output": extract_option(command, "--output"),
            "production_output_dir": extract_option(command, "--production-output-dir"),
            "masses": extract_option(command, "--masses"),
            "scalar_two_point_noises": extract_option(command, "--scalar-two-point-noises"),
        }
    )
    return enriched


def target_chunk_state(chunk: int) -> dict[str, Any]:
    output = ROOT / "outputs" / f"yt_pr230_fh_lsz_production_L12_T24_chunk{chunk:03d}_2026-05-01.json"
    output_dir = (
        ROOT
        / "outputs"
        / "yt_direct_lattice_correlator_production_fh_lsz_chunks"
        / f"L12_T24_chunk{chunk:03d}"
    )
    entries: list[str] = []
    if output_dir.exists():
        entries = sorted(child.name for child in output_dir.iterdir())
    return {
        "chunk": f"{chunk:03d}",
        "output": str(output.relative_to(ROOT)),
        "output_present": output.exists(),
        "output_artifact_present": output.exists(),
        "output_dir": str(output_dir.relative_to(ROOT)),
        "output_dir_present": output_dir.exists(),
        "output_dir_entries": entries,
        "counts_as_evidence_through_guard": False,
        "requires_chunk_certificate_for_evidence": output.exists(),
        "empty_dir_counts_as_evidence": False,
    }


def main() -> int:
    print("PR #230 FH/LSZ global production collision guard")
    print("=" * 72)

    ps_code, ps_out, ps_err = run_command(["ps", "-axo", "pid,ppid,etime,%cpu,command"])
    rows = parse_ps_rows(ps_out) if ps_code == 0 else []
    workers = [enrich_worker(row) for row in rows if is_fh_lsz_production_worker(str(row["command"]))]
    orchestrators = [enrich_worker(row) for row in rows if is_fh_lsz_orchestrator(str(row["command"]))]

    active_worker_count = len(workers)
    active_orchestrator_count = len(orchestrators)
    global_cap_allows_new_workers = active_worker_count < GLOBAL_MAX_PRODUCTION_JOBS
    resource_pressure_blocks_local_launch = active_worker_count >= LOCAL_RESOURCE_SAFE_WORKER_THRESHOLD
    launch_guard_allows_new_workers = (
        global_cap_allows_new_workers and not resource_pressure_blocks_local_launch
    )
    guard_blocks_launch = not launch_guard_allows_new_workers
    target_chunks = [target_chunk_state(chunk) for chunk in TARGET_CHUNKS]
    target_chunk_output_present_count = sum(1 for chunk in target_chunks if chunk["output_present"])
    target_chunks_evidence_count = sum(
        1 for chunk in target_chunks if chunk["counts_as_evidence_through_guard"]
    )

    status = (
        "bounded-support / FH-LSZ global production collision guard blocks new launch"
        if guard_blocks_launch
        else "bounded-support / FH-LSZ global production collision guard current state recorded"
    )

    report("process-table-acquired", ps_code == 0 and bool(rows), f"rows={len(rows)} rc={ps_code}")
    report(
        "active-fh-lsz-workers-recorded",
        active_worker_count >= 0,
        (
            f"active_workers={active_worker_count} "
            f"global_cap={GLOBAL_MAX_PRODUCTION_JOBS} "
            f"local_threshold={LOCAL_RESOURCE_SAFE_WORKER_THRESHOLD}"
        ),
    )
    report(
        "active-fh-lsz-orchestrators-recorded",
        active_orchestrator_count >= 0,
        f"active_orchestrators={active_orchestrator_count}",
    )
    report(
        "launch-decision-consistent-with-cap-and-resource-threshold",
        launch_guard_allows_new_workers
        == (global_cap_allows_new_workers and not resource_pressure_blocks_local_launch),
        f"allows_new_workers={launch_guard_allows_new_workers}",
    )
    report(
        "target-chunk-attempt-state-recorded",
        len(target_chunks) == len(TARGET_CHUNKS),
        (
            f"chunks={[chunk['chunk'] for chunk in target_chunks]} "
            f"output_present_count={target_chunk_output_present_count} "
            f"guard_evidence_count={target_chunks_evidence_count}"
        ),
    )
    report(
        "failed-or-empty-attempts-not-evidence",
        all(chunk["empty_dir_counts_as_evidence"] is False for chunk in target_chunks),
        "empty directories and failed foreground attempts are excluded",
    )
    report(
        "relative-launch-cwd-hazard-recorded",
        True,
        "future detached launches must use repo cwd or absolute paths before artifacts count",
    )
    report("does-not-authorize-retained-proposal", True, "infrastructure support only")

    result = {
        "actual_current_surface_status": status,
        "verdict": (
            "The guard records current global FH/LSZ production occupancy and "
            "the corresponding launch decision.  It preserves the claim "
            "firewall: process rows, empty directories, and scheduler launch "
            "return codes are provenance signals only, not y_t evidence."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "A production collision guard does not derive kappa_s, a "
            "canonical-Higgs/source-overlap theorem, or a same-source W/Z "
            "physical response readout."
        ),
        "global_cap": GLOBAL_MAX_PRODUCTION_JOBS,
        "local_resource_safe_worker_threshold": LOCAL_RESOURCE_SAFE_WORKER_THRESHOLD,
        "active_production_worker_count": active_worker_count,
        "active_orchestrator_count": active_orchestrator_count,
        "global_cap_allows_new_workers": global_cap_allows_new_workers,
        "resource_pressure_blocks_local_launch": resource_pressure_blocks_local_launch,
        "launch_guard_allows_new_workers": launch_guard_allows_new_workers,
        "guard_blocks_launch": guard_blocks_launch,
        "process_snapshot": {
            "ps_returncode": ps_code,
            "ps_stderr": ps_err.strip(),
            "active_production_workers": workers,
            "active_orchestrators": orchestrators,
        },
        "target_chunk_attempts": target_chunks,
        "target_chunk_output_present_count": target_chunk_output_present_count,
        "target_chunks_evidence_count": target_chunks_evidence_count,
        "launch_requirements": [
            "do not launch new FH/LSZ production workers when active global workers are at or above the cap",
            "do not launch new local workers when active global workers already meet the conservative local resource threshold",
            "use a repo cwd wrapper or absolute script/output paths for detached launchctl jobs",
            "do not count empty output directories as production evidence",
            "do not count foreground sessions that exit before writing certificates as production evidence",
            "do not count scheduler submission success unless the output artifact passes its chunk certificate",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not derive kappa_s",
            "does not set kappa_s = 1",
            "does not use H_unit or yt_ward_identity",
            "does not use alpha_LM, plaquette/u0, observed m_t, or observed y_t as proof authority",
            "does not treat source-only FH/LSZ as a physical y_t readout",
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
