#!/usr/bin/env python3
"""
PR #230 FH/LSZ eight-mode/x8 pole-fit wave orchestrator.

This keeps the separate polefit8x8 chunk stream moving.  It is run control,
not physics evidence: completed chunks must still pass the polefit8x8 combiner,
postprocess, model-class, FV/IR, and source-Higgs identity gates.
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_chunk_manifest_2026-05-04.json"
STATUS_OUTPUT = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_wave_orchestrator_status_2026-05-04.json"
LOG_DIR = ROOT / "outputs" / "yt_direct_lattice_correlator_production_fh_lsz_polefit8x8" / "logs"

GATE_COMMANDS = [
    ["python3", "scripts/frontier_yt_fh_lsz_polefit8x8_chunk_combiner_gate.py"],
    ["python3", "scripts/frontier_yt_fh_lsz_polefit8x8_postprocessor.py"],
    ["python3", "scripts/frontier_yt_retained_closure_route_certificate.py"],
    ["python3", "scripts/frontier_yt_pr230_campaign_status_certificate.py"],
]


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


def manifest_chunks() -> list[dict[str, Any]]:
    manifest = load_json(MANIFEST)
    return [row for row in manifest.get("commands", []) if isinstance(row, dict)]


def output_is_complete(path: Path) -> bool:
    if not path.exists() or path.stat().st_size <= 0:
        return False
    try:
        data = load_json(path)
    except Exception:
        return False
    return bool(data.get("ensembles")) and data.get("metadata", {}).get("run_control", {}).get("production_targets") is True


def production_jobs() -> list[dict[str, Any]]:
    result = subprocess.run(
        ["ps", "-Ao", "pid=,command="],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    jobs: list[dict[str, Any]] = []
    if result.returncode != 0:
        return jobs
    for line in result.stdout.splitlines():
        if "yt_direct_lattice_correlator_production.py" not in line:
            continue
        parts = line.strip().split(maxsplit=1)
        try:
            pid = int(parts[0])
        except (IndexError, ValueError):
            pid = -1
        jobs.append({"pid": pid, "command": parts[1] if len(parts) > 1 else line.strip()})
    return jobs


def active_polefit_jobs(chunks: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    jobs = production_jobs()
    active: dict[int, dict[str, Any]] = {}
    for row in chunks:
        output = str(row.get("output", ""))
        full_output = str(ROOT / output)
        for job in jobs:
            command = str(job.get("command", ""))
            if output and (output in command or full_output in command):
                active[int(row["chunk_index"])] = job
                break
    return active


def run_command(command: list[str], log_handle: Any | None = None) -> int:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=log_handle if log_handle is not None else None,
        stderr=subprocess.STDOUT if log_handle is not None else None,
        check=False,
    )
    return int(completed.returncode)


def run_gates(log_handle: Any | None = None) -> list[dict[str, Any]]:
    rows = []
    for command in GATE_COMMANDS:
        rc = run_command(command, log_handle)
        rows.append({"command": command, "returncode": rc})
    return rows


def write_status(status: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-index", type=int, default=1)
    parser.add_argument("--end-index", type=int, default=0, help="0 means use manifest chunk_count.")
    parser.add_argument("--max-concurrent", type=int, default=6)
    parser.add_argument("--global-max-production-jobs", type=int, default=6)
    parser.add_argument("--runtime-minutes", type=float, default=720.0)
    parser.add_argument("--poll-seconds", type=float, default=60.0)
    parser.add_argument("--launch", action="store_true", help="Actually launch missing chunks.")
    parser.add_argument("--dry-run", action="store_true", help="Plan only; overrides --launch.")
    parser.add_argument("--run-gates", action="store_true", help="Run combiner/postprocess gates as chunks complete.")
    parser.add_argument("--status-output", type=Path, default=STATUS_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    chunks = manifest_chunks()
    if not chunks:
        print(f"missing manifest: {rel(MANIFEST)}", flush=True)
        return 2

    max_index = max(int(row["chunk_index"]) for row in chunks)
    start = max(1, int(args.start_index))
    end = args.end_index or max_index
    end = max(start, min(int(end), max_index))
    chunk_by_index = {int(row["chunk_index"]): row for row in chunks}
    selected = [chunk_by_index[index] for index in range(start, end + 1) if index in chunk_by_index]
    launch_enabled = bool(args.launch and not args.dry_run)
    deadline = time.monotonic() + max(0.0, float(args.runtime_minutes)) * 60.0
    max_concurrent = max(1, int(args.max_concurrent))
    global_cap = max(1, int(args.global_max_production_jobs))

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    launched: list[dict[str, Any]] = []
    gate_runs: list[dict[str, Any]] = []
    processed: set[int] = set()
    poll_count = 0

    print("PR #230 FH/LSZ eight-mode/x8 pole-fit wave orchestrator", flush=True)
    print("=" * 72, flush=True)
    print(
        f"range={start}-{end} launch={launch_enabled} dry_run={bool(args.dry_run)} "
        f"max_concurrent={max_concurrent} global_cap={global_cap}",
        flush=True,
    )

    while True:
        poll_count += 1
        all_jobs = production_jobs()
        active = active_polefit_jobs(selected)
        completed = sorted(
            int(row["chunk_index"])
            for row in selected
            if output_is_complete(ROOT / str(row.get("output", "")))
        )
        running = sorted(active)
        missing = sorted(
            int(row["chunk_index"])
            for row in selected
            if int(row["chunk_index"]) not in completed and int(row["chunk_index"]) not in active
        )
        newly_completed = [index for index in completed if index not in processed]

        if args.run_gates and newly_completed:
            gate_log = LOG_DIR / f"polefit8x8_gates_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.log"
            with gate_log.open("a", encoding="utf-8") as handle:
                handle.write(f"\n[{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] polefit8x8 gates\n")
                gate_runs.extend({**row, "log": rel(gate_log)} for row in run_gates(handle))
        processed.update(newly_completed)

        local_slots = max_concurrent - len(running)
        global_slots = global_cap - len(all_jobs)
        available_slots = max(0, min(local_slots, global_slots))
        if launch_enabled and missing and available_slots > 0:
            for index in missing[:available_slots]:
                row = chunk_by_index[index]
                command = shlex.split(str(row.get("command", "")))
                log_path = LOG_DIR / f"L12_T24_chunk{index:03d}_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.log"
                log_handle = log_path.open("a", encoding="utf-8")
                process = subprocess.Popen(
                    command,
                    cwd=ROOT,
                    stdout=log_handle,
                    stderr=subprocess.STDOUT,
                    text=True,
                    start_new_session=True,
                )
                launched.append(
                    {
                        "chunk_index": index,
                        "pid": process.pid,
                        "seed": row.get("seed"),
                        "output": row.get("output"),
                        "production_output_dir": row.get("production_output_dir"),
                        "log": rel(log_path),
                        "command": command,
                    }
                )
                print(f"launched polefit8x8 chunk{index:03d} pid={process.pid} log={rel(log_path)}", flush=True)

        status = {
            "actual_current_surface_status": "bounded-support / FH-LSZ eight-mode-x8 pole-fit wave orchestration status",
            "proposal_allowed": False,
            "proposal_allowed_reason": "Wave orchestration is run control only; pole-fit and retained gates decide evidence status.",
            "manifest": rel(MANIFEST),
            "range": {"start_index": start, "end_index": end},
            "poll_count": poll_count,
            "completed_chunks": completed,
            "running_chunks": running,
            "missing_chunks": missing,
            "newly_completed_chunks": newly_completed,
            "all_production_job_count": len(all_jobs),
            "global_max_production_jobs": global_cap,
            "available_launch_slots": available_slots,
            "launched_chunks": launched,
            "gate_runs": gate_runs[-80:],
            "strict_non_claims": [
                "does not claim retained or proposed_retained y_t closure",
                "does not mix eight-mode/x8 chunks with the four-mode/x16 L12 ensemble",
                "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            ],
        }
        output = args.status_output if args.status_output.is_absolute() else ROOT / args.status_output
        write_status(status, output)
        print(
            f"poll={poll_count} completed={len(completed)} running={running} "
            f"missing={len(missing)} all_jobs={len(all_jobs)} launched_total={len(launched)}",
            flush=True,
        )

        if args.dry_run or (not launch_enabled and not args.run_gates):
            break
        if not missing and not running:
            print("all requested polefit8x8 chunks complete", flush=True)
            break
        if time.monotonic() >= deadline:
            print("runtime deadline reached", flush=True)
            break
        time.sleep(max(1.0, float(args.poll_seconds)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
