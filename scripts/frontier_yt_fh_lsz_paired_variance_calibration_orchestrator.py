#!/usr/bin/env python3
"""
PR #230 FH/LSZ paired x8/x16 variance calibration orchestrator.

This is run control for the scalar-pole support lane.  It reads the paired
variance-calibration manifest, detects completed or running x8/x16 calibration
jobs, optionally launches missing jobs without exceeding a global production
job cap, and reruns the paired variance gates after outputs land.

It is not physics evidence and never mixes the eight-mode calibration stream
with the current four-mode FH/LSZ chunk ensemble.
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
MANIFEST = ROOT / "outputs" / "yt_fh_lsz_variance_calibration_manifest_2026-05-01.json"
STATUS_OUTPUT = ROOT / "outputs" / "yt_fh_lsz_paired_variance_calibration_orchestrator_status_2026-05-04.json"
LOG_DIR = ROOT / "outputs" / "yt_direct_lattice_correlator_production_fh_lsz_variance_calibration" / "logs"

GATE_COMMANDS = [
    ["python3", "scripts/frontier_yt_fh_lsz_paired_variance_calibration_gate.py"],
    ["python3", "scripts/frontier_yt_fh_lsz_eight_mode_noise_variance_gate.py"],
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


def manifest_commands() -> dict[str, dict[str, Any]]:
    manifest = load_json(MANIFEST)
    rows: dict[str, dict[str, Any]] = {}
    for row in manifest.get("commands", []):
        if isinstance(row, dict) and row.get("label") in {"x8", "x16"}:
            rows[str(row["label"])] = row
    return rows


def output_path(row: dict[str, Any]) -> Path:
    return ROOT / str(row.get("output", ""))


def output_is_complete(path: Path) -> bool:
    if not path.exists() or path.stat().st_size <= 0:
        return False
    try:
        data = load_json(path)
    except Exception:
        return False
    return bool(data.get("ensembles")) and data.get("metadata", {}).get("run_control", {}).get(
        "production_targets"
    ) is True


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


def active_calibration_jobs(commands: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    jobs = production_jobs()
    active: dict[str, dict[str, Any]] = {}
    for label, row in commands.items():
        output = str(row.get("output", ""))
        full_output = str(output_path(row))
        for job in jobs:
            command = str(job.get("command", ""))
            if output and (output in command or full_output in command):
                active[label] = job
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
    parser.add_argument("--launch", action="store_true", help="Actually launch missing calibration jobs.")
    parser.add_argument("--dry-run", action="store_true", help="Plan only; overrides --launch.")
    parser.add_argument("--run-gates", action="store_true", help="Run paired variance gates after outputs appear.")
    parser.add_argument("--runtime-minutes", type=float, default=720.0)
    parser.add_argument("--poll-seconds", type=float, default=60.0)
    parser.add_argument("--max-concurrent", type=int, default=2)
    parser.add_argument("--global-max-production-jobs", type=int, default=6)
    parser.add_argument("--status-output", type=Path, default=STATUS_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    commands = manifest_commands()
    missing_labels = sorted({"x8", "x16"} - set(commands))
    dry_run = bool(args.dry_run)
    launch_enabled = bool(args.launch and not dry_run)
    deadline = time.monotonic() + max(0.0, float(args.runtime_minutes)) * 60.0
    max_concurrent = max(1, int(args.max_concurrent))
    global_cap = max(1, int(args.global_max_production_jobs))

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    launched: list[dict[str, Any]] = []
    gate_runs: list[dict[str, Any]] = []
    processed: set[str] = set()
    poll_count = 0

    print("PR #230 FH/LSZ paired variance calibration orchestrator", flush=True)
    print("=" * 72, flush=True)
    print(
        f"launch={launch_enabled} dry_run={dry_run} max_concurrent={max_concurrent} "
        f"global_cap={global_cap}",
        flush=True,
    )

    while True:
        poll_count += 1
        all_jobs = production_jobs()
        active = active_calibration_jobs(commands)
        completed = sorted(
            label for label, row in commands.items() if output_is_complete(output_path(row))
        )
        running = sorted(active)
        missing = sorted(
            label for label in commands if label not in completed and label not in active
        )
        newly_completed = [label for label in completed if label not in processed]

        if args.run_gates and newly_completed:
            gate_log = LOG_DIR / f"paired_variance_gates_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.log"
            with gate_log.open("a", encoding="utf-8") as handle:
                handle.write(f"\n[{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] paired gates\n")
                gate_runs.extend({"label": None, **row, "log": rel(gate_log)} for row in run_gates(handle))
        processed.update(newly_completed)

        local_slots = max_concurrent - len(running)
        global_slots = global_cap - len(all_jobs)
        available_slots = max(0, min(local_slots, global_slots))
        to_launch = missing[:available_slots]
        if launch_enabled and to_launch:
            for label in to_launch:
                row = commands[label]
                command = shlex.split(str(row.get("command", "")))
                log_path = LOG_DIR / f"L12_T24_{label}_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.log"
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
                        "label": label,
                        "pid": process.pid,
                        "output": row.get("output"),
                        "production_output_dir": row.get("production_output_dir"),
                        "log": rel(log_path),
                        "command": command,
                    }
                )
                print(f"launched {label} pid={process.pid} log={rel(log_path)}", flush=True)

        status = {
            "actual_current_surface_status": "bounded-support / paired x8/x16 variance calibration orchestration status",
            "proposal_allowed": False,
            "proposal_allowed_reason": "Calibration orchestration is run control only; variance gates and physics gates decide evidence status.",
            "manifest": rel(MANIFEST),
            "missing_manifest_labels": missing_labels,
            "poll_count": poll_count,
            "completed_labels": completed,
            "running_labels": running,
            "missing_labels": missing,
            "newly_completed_labels": newly_completed,
            "all_production_job_count": len(all_jobs),
            "global_max_production_jobs": global_cap,
            "available_launch_slots": available_slots,
            "launched": launched,
            "gate_runs": gate_runs[-40:],
            "strict_non_claims": [
                "does not claim retained or proposed_retained y_t closure",
                "does not treat variance calibration as scalar LSZ normalization",
                "does not mix eight-mode calibration with four-mode production chunks as one homogeneous ensemble",
                "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            ],
        }
        output = args.status_output if args.status_output.is_absolute() else ROOT / args.status_output
        write_status(status, output)
        print(
            f"poll={poll_count} completed={completed} running={running} missing={missing} "
            f"all_jobs={len(all_jobs)} launch_slots={available_slots}",
            flush=True,
        )

        if dry_run or (not launch_enabled and not args.run_gates):
            break
        if not missing and not running:
            print("paired calibration outputs complete", flush=True)
            break
        if time.monotonic() >= deadline:
            print("runtime deadline reached", flush=True)
            break
        time.sleep(max(1.0, float(args.poll_seconds)))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
