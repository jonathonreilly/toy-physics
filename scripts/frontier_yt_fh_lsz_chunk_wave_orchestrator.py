#!/usr/bin/env python3
"""
PR #230 FH/LSZ chunk-wave orchestrator.

This is production engineering, not physics evidence.  It keeps the bounded
L12_T24 FH/LSZ chunk campaign moving without changing the claim surface:

* detect completed chunk JSON outputs;
* detect already-running production jobs by their output path;
* launch the next missing chunks up to a conservative concurrency cap;
* run the existing per-chunk and aggregate gates after outputs appear;
* write a status certificate that explicitly remains support-only.

The orchestrator never treats partial chunks as retained evidence and never
sets a physical Yukawa readout.  The existing combiner, response-stability,
source-Higgs/WZ/rank-one, retained-route, and campaign certificates remain the
authority surfaces.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outputs" / "yt_fh_lsz_chunked_production_manifest_2026-05-01.json"
STATUS_OUTPUT = ROOT / "outputs" / "yt_fh_lsz_chunk_wave_orchestrator_status_2026-05-04.json"
LOG_DIR = ROOT / "outputs" / "yt_direct_lattice_correlator_production_fh_lsz_chunks" / "logs"

MASS_SPEC = "0.45,0.75,1.05"
SOURCE_SHIFTS = "-0.01,0.0,0.01"
SCALAR_MODES = "0,0,0;1,0,0;0,1,0;0,0,1"

GATE_COMMANDS = [
    ["python3", "scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py"],
    ["python3", "scripts/frontier_yt_fh_lsz_ready_chunk_set_checkpoint_certificate.py"],
    ["python3", "scripts/frontier_yt_fh_lsz_target_observable_ess_certificate.py"],
    ["python3", "scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py"],
    ["python3", "scripts/frontier_yt_fh_lsz_ready_chunk_response_stability.py"],
    ["python3", "scripts/frontier_yt_fh_lsz_response_window_forensics.py"],
    ["python3", "scripts/frontier_yt_fh_lsz_common_window_response_provenance.py"],
    ["python3", "scripts/frontier_yt_fh_lsz_common_window_pooled_response_estimator.py"],
    ["python3", "scripts/frontier_yt_fh_lsz_common_window_response_gate.py"],
    ["python3", "scripts/frontier_yt_fh_lsz_response_window_acceptance_gate.py"],
    ["python3", "scripts/frontier_yt_fh_lsz_v2_target_response_stability.py"],
    ["python3", "scripts/frontier_yt_retained_closure_route_certificate.py"],
    ["python3", "scripts/frontier_yt_pr230_campaign_status_certificate.py"],
]


@dataclass(frozen=True)
class ChunkSpec:
    index: int
    seed: int
    output: Path
    production_output_dir: Path


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


def manifest_chunk_count() -> int:
    manifest = load_json(MANIFEST)
    return int(manifest.get("chunk_policy", {}).get("chunk_count", 63))


def chunk_spec(index: int) -> ChunkSpec:
    return ChunkSpec(
        index=index,
        seed=2026051000 + index,
        output=ROOT
        / "outputs"
        / f"yt_pr230_fh_lsz_production_L12_T24_chunk{index:03d}_2026-05-01.json",
        production_output_dir=ROOT
        / "outputs"
        / "yt_direct_lattice_correlator_production_fh_lsz_chunks"
        / f"L12_T24_chunk{index:03d}",
    )


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


def active_jobs() -> dict[int, dict[str, Any]]:
    result = subprocess.run(
        ["ps", "-Ao", "pid=,command="],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    jobs: dict[int, dict[str, Any]] = {}
    if result.returncode != 0:
        return jobs
    for line in result.stdout.splitlines():
        if "yt_direct_lattice_correlator_production.py" not in line:
            continue
        for index in range(1, manifest_chunk_count() + 1):
            spec = chunk_spec(index)
            output_token = rel(spec.output)
            if output_token in line or str(spec.output) in line:
                parts = line.strip().split(maxsplit=1)
                try:
                    pid = int(parts[0])
                except (IndexError, ValueError):
                    pid = -1
                jobs[index] = {"pid": pid, "command": parts[1] if len(parts) > 1 else line.strip()}
                break
    return jobs


def production_command(spec: ChunkSpec) -> list[str]:
    return [
        "python3",
        "scripts/yt_direct_lattice_correlator_production.py",
        "--volumes",
        "12x24",
        "--masses",
        MASS_SPEC,
        "--therm",
        "1000",
        "--measurements",
        "16",
        "--separation",
        "20",
        "--engine",
        "numba",
        "--production-targets",
        f"--scalar-source-shifts={SOURCE_SHIFTS}",
        "--scalar-two-point-modes",
        SCALAR_MODES,
        "--scalar-two-point-noises",
        "16",
        "--production-output-dir",
        rel(spec.production_output_dir),
        "--resume",
        "--seed",
        str(spec.seed),
        "--output",
        rel(spec.output),
    ]


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


def run_chunk_gates(index: int, log_handle: Any | None = None) -> list[dict[str, Any]]:
    commands = [
        ["python3", "scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py", "--chunk-index", str(index)],
        ["python3", "scripts/frontier_yt_fh_lsz_chunk_multitau_target_timeseries_checkpoint.py", "--chunk-index", str(index)],
    ]
    results = []
    for command in commands:
        rc = run_command(command, log_handle)
        results.append({"command": command, "returncode": rc})
    return results


def run_aggregate_gates(log_handle: Any | None = None) -> list[dict[str, Any]]:
    results = []
    for command in GATE_COMMANDS:
        rc = run_command(command, log_handle)
        results.append({"command": command, "returncode": rc})
    return results


def write_status(status: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-index", type=int, default=1)
    parser.add_argument("--end-index", type=int, default=0, help="0 means use manifest chunk_count.")
    parser.add_argument("--max-concurrent", type=int, default=6)
    parser.add_argument("--runtime-minutes", type=float, default=720.0)
    parser.add_argument("--poll-seconds", type=float, default=60.0)
    parser.add_argument("--launch", action="store_true", help="Actually launch missing chunks.")
    parser.add_argument("--dry-run", action="store_true", help="Plan only; overrides --launch.")
    parser.add_argument("--run-gates", action="store_true", help="Run gates for newly completed chunks.")
    parser.add_argument("--status-output", type=Path, default=STATUS_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    end_index = args.end_index or manifest_chunk_count()
    start = max(1, int(args.start_index))
    end = max(start, min(int(end_index), manifest_chunk_count()))
    max_concurrent = max(1, int(args.max_concurrent))
    deadline = time.monotonic() + max(0.0, float(args.runtime_minutes)) * 60.0
    dry_run = bool(args.dry_run)
    launch_enabled = bool(args.launch and not dry_run)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    processed: set[int] = set()
    launched: list[dict[str, Any]] = []
    gate_runs: list[dict[str, Any]] = []
    poll_count = 0

    print("PR #230 FH/LSZ chunk-wave orchestrator", flush=True)
    print("=" * 72, flush=True)
    print(
        f"range={start}-{end} max_concurrent={max_concurrent} "
        f"launch={launch_enabled} dry_run={dry_run}",
        flush=True,
    )

    while True:
        poll_count += 1
        jobs = active_jobs()
        completed = [idx for idx in range(start, end + 1) if output_is_complete(chunk_spec(idx).output)]
        all_running = sorted(jobs)
        running = sorted(idx for idx in jobs if start <= idx <= end)
        missing = [idx for idx in range(start, end + 1) if idx not in completed and idx not in jobs]

        newly_completed = [idx for idx in completed if idx not in processed]
        if args.run_gates and newly_completed:
            gate_log_path = LOG_DIR / f"orchestrator_gates_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.log"
            with gate_log_path.open("a", encoding="utf-8") as gate_log:
                for idx in newly_completed:
                    gate_log.write(f"\n[{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] chunk {idx:03d} gates\n")
                    gate_runs.extend(
                        {"chunk_index": idx, **row, "log": rel(gate_log_path)}
                        for row in run_chunk_gates(idx, gate_log)
                    )
                gate_log.write(f"\n[{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] aggregate gates\n")
                gate_runs.extend(
                    {"chunk_index": None, **row, "log": rel(gate_log_path)}
                    for row in run_aggregate_gates(gate_log)
                )
        processed.update(newly_completed)

        available_slots = max_concurrent - len(all_running)
        to_launch = missing[: max(0, available_slots)]
        if launch_enabled and to_launch:
            for idx in to_launch:
                spec = chunk_spec(idx)
                log_path = LOG_DIR / f"L12_T24_chunk{idx:03d}_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.log"
                log_handle = log_path.open("a", encoding="utf-8")
                command = production_command(spec)
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
                        "chunk_index": idx,
                        "pid": process.pid,
                        "seed": spec.seed,
                        "output": rel(spec.output),
                        "production_output_dir": rel(spec.production_output_dir),
                        "log": rel(log_path),
                        "command": command,
                    }
                )
                print(f"launched chunk{idx:03d} pid={process.pid} log={rel(log_path)}", flush=True)

        status = {
            "actual_current_surface_status": "bounded-support / FH-LSZ chunk-wave orchestration status",
            "proposal_allowed": False,
            "proposal_allowed_reason": "Chunk orchestration is run control only; production evidence and retained closure require downstream gates.",
            "range": {"start_index": start, "end_index": end},
            "poll_count": poll_count,
            "completed_chunks": completed,
            "all_running_chunks": all_running,
            "running_chunks": running,
            "missing_chunks": missing,
            "newly_completed_chunks": newly_completed,
            "launched_chunks": launched,
            "gate_runs": gate_runs[-80:],
            "strict_non_claims": [
                "does not claim retained or proposed_retained y_t closure",
                "does not treat partial chunks as complete volume evidence",
                "does not modify physical readout gates",
                "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            ],
        }
        write_status(status, args.status_output if args.status_output.is_absolute() else ROOT / args.status_output)
        print(
            f"poll={poll_count} completed={len(completed)} all_running={all_running} "
            f"range_running={running} missing={len(missing)} "
            f"launched_total={len(launched)}",
            flush=True,
        )

        if dry_run or (not launch_enabled and not args.run_gates):
            break
        if not missing and not running:
            print("all requested chunks complete", flush=True)
            break
        if time.monotonic() >= deadline:
            print("runtime deadline reached", flush=True)
            break
        time.sleep(max(1.0, float(args.poll_seconds)))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
