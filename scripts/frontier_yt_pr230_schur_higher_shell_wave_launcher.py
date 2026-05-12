#!/usr/bin/env python3
"""
PR #230 higher-shell Schur/scalar-LSZ wave launcher/status certificate.

This runner consumes the higher-shell production contract and reports or
launches a bounded non-colliding wave under the separate higher-shell roots.
It is run-control infrastructure only.  Active processes, logs, pid files,
empty directories, partial directories, launch certificates, and completed
row files before completed-mode checkpointing are not physics evidence and
never authorize retained or proposed_retained top-Yukawa closure wording.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = (
    ROOT / "outputs" / "yt_pr230_schur_higher_shell_production_contract_2026-05-07.json"
)
DEFAULT_OUTPUT = ROOT / "outputs" / "yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json"
DEFAULT_LOG_DIR = ROOT / "outputs" / "yt_pr230_schur_higher_shell_rows" / "logs"
EXPECTED_SEED_BASE = 2026057000
EXPECTED_CHUNK_COUNT = 63
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


def repo_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def parse_indices(raw: str | None) -> set[int] | None:
    if not raw:
        return None
    values: set[int] = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            values.update(range(int(start), int(end) + 1))
        else:
            values.add(int(part))
    return values


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
        for index in range(1, EXPECTED_CHUNK_COUNT + 1):
            if f"chunk{index:03d}" in command:
                chunk = index
                break
        rows.append({"pid": pid, "chunk_index": chunk, "command": command})
    return rows


def expected_seed(chunk_index: int) -> int:
    return EXPECTED_SEED_BASE + int(chunk_index)


def command_ok(row: dict[str, Any]) -> tuple[bool, str]:
    command = row.get("command")
    if not isinstance(command, list):
        return False, "missing command list"
    if "--resume" in command:
        return False, "forbidden --resume present"
    chunk = int(row["chunk_index"])
    joined = " ".join(str(part) for part in command)
    required = [
        "scripts/yt_direct_lattice_correlator_production.py",
        "--production-targets",
        "--engine numba",
        "--scalar-source-shifts=-0.01,0.0,0.01",
        "--scalar-two-point-noises 16",
        "--source-higgs-cross-noises 16",
        f"--seed {expected_seed(chunk)}",
        f"chunk{chunk:03d}",
        "yt_pr230_schur_higher_shell_rows",
        "yt_direct_lattice_correlator_production_schur_higher_shell_rows",
    ]
    missing = [token for token in required if token not in joined]
    mode_values: list[str] = []
    for flag in ("--scalar-two-point-modes", "--source-higgs-cross-modes"):
        if flag not in command:
            return False, f"missing {flag}"
        try:
            mode_values.append(str(command[command.index(flag) + 1]))
        except IndexError:
            return False, f"missing value for {flag}"
    parsed_mode_sets = [set(value.split(";")) for value in mode_values]
    if any(modes != EXPECTED_MODES for modes in parsed_mode_sets):
        missing.append("expected 11 higher-shell modes")
    if missing:
        return False, f"missing command token(s): {missing}"
    if int(row.get("seed", -1)) != expected_seed(chunk):
        return False, f"seed mismatch: {row.get('seed')} != {expected_seed(chunk)}"
    return True, "no-resume higher-shell production command"


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


def launch_row(row: dict[str, Any], log_dir: Path) -> dict[str, Any]:
    chunk = int(row["chunk_index"])
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"L12_T24_chunk{chunk:03d}_{stamp}.log"
    log_fh = open(log_path, "ab", buffering=0)
    try:
        proc = subprocess.Popen(
            row["command"],
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=log_fh,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    finally:
        log_fh.close()
    return {
        "chunk_index": chunk,
        "pid": proc.pid,
        "log": rel(log_path),
        "output": row["output"],
        "production_output_dir": row["production_output_dir"],
        "seed": row.get("seed"),
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=rel(DEFAULT_CONTRACT), help="Higher-shell contract JSON.")
    parser.add_argument("--output", default=rel(DEFAULT_OUTPUT), help="Launcher/status certificate JSON.")
    parser.add_argument("--log-dir", default=rel(DEFAULT_LOG_DIR), help="Directory for launched chunk logs.")
    parser.add_argument("--max-concurrent", type=int, default=2, help="Maximum active higher-shell workers.")
    parser.add_argument("--chunk-indices", help="Optional comma/range subset such as 1,2 or 3-6.")
    parser.add_argument("--launch", action="store_true", help="Actually launch the safe next wave.")
    parser.add_argument("--verify-seconds", type=float, default=2.0)
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    contract_path = repo_path(args.contract)
    output_path = repo_path(args.output)
    log_dir = repo_path(args.log_dir)
    requested_indices = parse_indices(args.chunk_indices)

    print("PR #230 higher-shell Schur/scalar-LSZ wave launcher")
    print("=" * 78)

    contract = load_json(contract_path)
    rows = (
        contract.get("future_noncollision_preview", [])
        if isinstance(contract.get("future_noncollision_preview"), list)
        else []
    )
    active_rows = active_process_rows()
    active_chunks = [
        int(row["chunk_index"]) for row in active_rows if isinstance(row.get("chunk_index"), int)
    ]
    active_chunk_set = set(active_chunks)
    duplicate_active_chunks = sorted(chunk for chunk in active_chunk_set if active_chunks.count(chunk) > 1)
    unknown_active_rows = [row for row in active_rows if row.get("chunk_index") is None]

    completed_chunks: list[int] = []
    blocking_partial_dirs: list[int] = []
    blocked_by_command: list[dict[str, Any]] = []
    eligible_rows: list[dict[str, Any]] = []
    considered_rows: list[dict[str, Any]] = []

    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("chunk_index"), int):
            continue
        chunk = int(row["chunk_index"])
        if requested_indices is not None and chunk not in requested_indices:
            continue
        output = repo_path(str(row.get("output", "")))
        pdir = repo_path(str(row.get("production_output_dir", "")))
        output_present = output.exists()
        pdir_present = pdir.exists()
        command_passed, command_reason = command_ok(row)
        considered_rows.append(
            {
                "chunk_index": chunk,
                "output": row.get("output"),
                "output_present": output_present,
                "production_output_dir": row.get("production_output_dir"),
                "production_output_dir_present": pdir_present,
                "active": chunk in active_chunk_set,
                "command_ok": command_passed,
                "command_reason": command_reason,
                "seed": row.get("seed"),
            }
        )
        if output_present:
            completed_chunks.append(chunk)
            continue
        if pdir_present and chunk not in active_chunk_set:
            blocking_partial_dirs.append(chunk)
            continue
        if not command_passed:
            blocked_by_command.append({"chunk_index": chunk, "reason": command_reason})
            continue
        if chunk in active_chunk_set:
            continue
        eligible_rows.append(row)

    contract_passed = (
        "higher-shell Schur scalar-LSZ production contract"
        in str(contract.get("actual_current_surface_status"))
        and contract.get("proposal_allowed") is False
        and contract.get("higher_shell_schur_production_contract_passed") is True
        and contract.get("launch_allowed_now") is True
        and contract.get("rows_written_by_contract") is False
        and contract.get("current_four_mode_campaign_must_remain_unmixed") is True
    )
    chunk_count_ok = len(rows) == EXPECTED_CHUNK_COUNT
    command_boundaries_ok = not blocked_by_command
    active_state_ok = not duplicate_active_chunks and not unknown_active_rows
    partial_state_ok = not blocking_partial_dirs
    max_concurrent_ok = args.max_concurrent > 0 and args.max_concurrent <= 3
    active_within_limit = len(active_chunk_set) <= args.max_concurrent
    launch_capacity = max(args.max_concurrent - len(active_chunk_set), 0)
    launchable_rows = eligible_rows[:launch_capacity]
    launch_allowed = (
        contract_passed
        and chunk_count_ok
        and command_boundaries_ok
        and active_state_ok
        and partial_state_ok
        and max_concurrent_ok
        and active_within_limit
        and launch_capacity > 0
    )

    launched: list[dict[str, Any]] = []
    if args.launch and launch_allowed:
        for row in launchable_rows:
            launched.append(launch_row(row, log_dir))
        if launched and args.verify_seconds > 0:
            time.sleep(args.verify_seconds)
            for item in launched:
                item["alive_after_verify_seconds"] = pid_alive(int(item["pid"]))

    launched_alive = all(item.get("alive_after_verify_seconds", True) for item in launched)
    no_unrequested_launch = bool(args.launch) or not launched
    active_or_completed = sorted(active_chunk_set | set(completed_chunks))

    report("contract-present", bool(contract), rel(contract_path))
    report("contract-passed-support-only", contract_passed, contract.get("actual_current_surface_status", ""))
    report("preview-chunk-count", chunk_count_ok, f"rows={len(rows)}")
    report("row-commands-are-no-resume-higher-shell-commands", command_boundaries_ok, f"blocked={blocked_by_command}")
    report(
        "active-higher-shell-processes-without-collision",
        active_state_ok,
        f"active_chunks={sorted(active_chunk_set)} duplicates={duplicate_active_chunks} unknown={len(unknown_active_rows)}",
    )
    report("no-blocking-partial-output-dirs", partial_state_ok, f"blocking_partial_dirs={blocking_partial_dirs}")
    report("concurrency-cap-is-conservative", max_concurrent_ok, f"max_concurrent={args.max_concurrent}")
    report("active-workers-within-cap", active_within_limit, f"active={len(active_chunk_set)} cap={args.max_concurrent}")
    report("launch-mode-explicit", no_unrequested_launch, f"launch_flag={args.launch}")
    report("launched-processes-survived-initial-check", launched_alive, f"launched={launched}")
    report("does-not-authorize-retained-proposal", True, "run-control support only")

    result = {
        "actual_current_surface_status": (
            "run-control / higher-shell Schur scalar-LSZ wave launcher status; "
            "active or launched jobs are not physics evidence"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Higher-shell launch status cannot supply completed row evidence, "
            "complete monotonicity, scalar pole authority, FV/IR authority, "
            "canonical O_H/source-overlap authority, W/Z response, or y_t closure."
        ),
        "bare_retained_allowed": False,
        "launch_mode": bool(args.launch),
        "launch_allowed_before_action": launch_allowed,
        "max_concurrent": args.max_concurrent,
        "contract": rel(contract_path),
        "active_chunk_indices": sorted(active_chunk_set),
        "active_or_completed_chunk_indices": active_or_completed,
        "active_process_count": len(active_rows),
        "active_process_rows": active_rows,
        "completed_chunk_indices": sorted(completed_chunks),
        "blocking_partial_output_dir_indices": sorted(blocking_partial_dirs),
        "blocked_by_command": blocked_by_command,
        "eligible_chunk_indices_before_capacity": [int(row["chunk_index"]) for row in eligible_rows],
        "launch_capacity": launch_capacity,
        "planned_launch_chunk_indices": [int(row["chunk_index"]) for row in launchable_rows],
        "launched": launched,
        "completed_outputs_are_not_overwritten": True,
        "partial_directories_count_as_non_evidence": True,
        "considered_rows": considered_rows,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat active processes, logs, pid files, empty directories, partial directories, or launch status as row evidence",
            "does not use --resume for higher-shell row chunks",
            "does not overwrite completed chunk outputs",
            "does not treat C_sx/C_xx as canonical-Higgs C_sH/C_HH",
            "does not claim complete monotonicity, scalar pole authority, FV/IR authority, canonical O_H, source-overlap, or W/Z response",
            "does not set kappa_s = 1, c2 = 1, or Z_match = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "When active higher-shell chunks finish, run completed-mode chunk "
            "checkpoints before combining rows or making any scalar-LSZ/Schur "
            "authority claim."
        ),
        "wave_launcher_passed": FAIL_COUNT == 0,
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
