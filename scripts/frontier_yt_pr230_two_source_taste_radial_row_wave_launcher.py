#!/usr/bin/env python3
"""
PR #230 two-source taste-radial row wave launcher/status certificate.

This runner consumes the no-resume production manifest and either reports the
next bounded wave or, with --launch, starts only the currently safe chunk
commands.  It is run-control infrastructure only.  Active processes, logs,
empty directories, partial directories, manifests, and launch certificates are
not C_sx/C_xx row evidence and never authorize y_t closure wording.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shlex
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SCRIPT = ROOT / "scripts" / "frontier_yt_pr230_two_source_taste_radial_row_production_manifest.py"
DEFAULT_MANIFEST = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
DEFAULT_OUTPUT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_wave_launcher_2026-05-06.json"
DEFAULT_LOG_DIR = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_rows" / "logs"

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


def load_manifest_module() -> Any:
    spec = importlib.util.spec_from_file_location("pr230_taste_radial_manifest", MANIFEST_SCRIPT)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def active_process_rows() -> list[dict[str, Any]]:
    module = load_manifest_module()
    if module is not None and hasattr(module, "active_process_rows"):
        rows = module.active_process_rows()
        if isinstance(rows, list):
            return rows
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
            and "yt_direct_lattice_correlator_production_two_source_taste_radial_rows" not in line
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


def repo_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def command_ok(row: dict[str, Any]) -> tuple[bool, str]:
    command = row.get("command")
    if not isinstance(command, list):
        return False, "missing command list"
    if "--resume" in command:
        return False, "forbidden --resume present"
    joined = " ".join(str(part) for part in command)
    chunk = int(row["chunk_index"])
    required = [
        "scripts/yt_direct_lattice_correlator_production.py",
        "--production-targets",
        "--engine numba",
        "--scalar-source-shifts=-0.01,0.0,0.01",
        "--source-higgs-cross-noises 16",
        "--scalar-two-point-noises 16",
        f"chunk{chunk:03d}",
    ]
    missing = [token for token in required if token not in joined]
    if missing:
        return False, f"missing command token(s): {missing}"
    return True, "no-resume production row command"


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
    }


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=rel(DEFAULT_MANIFEST), help="Manifest JSON to consume.")
    parser.add_argument("--output", default=rel(DEFAULT_OUTPUT), help="Launcher/status certificate JSON.")
    parser.add_argument("--log-dir", default=rel(DEFAULT_LOG_DIR), help="Directory for launched chunk logs.")
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=2,
        help="Maximum active row workers allowed by this launcher invocation.",
    )
    parser.add_argument(
        "--chunk-indices",
        help="Optional comma/range subset such as 1,2,5-8. Defaults to all manifest launchable rows.",
    )
    parser.add_argument("--launch", action="store_true", help="Actually launch the safe next wave.")
    parser.add_argument(
        "--verify-seconds",
        type=float,
        default=2.0,
        help="Seconds to wait before checking launched PIDs for early exit.",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    manifest_path = repo_path(args.manifest)
    output_path = repo_path(args.output)
    log_dir = repo_path(args.log_dir)
    requested_indices = parse_indices(args.chunk_indices)

    print("PR #230 two-source taste-radial row wave launcher")
    print("=" * 78)

    manifest = load_json(manifest_path)
    policy = manifest.get("production_policy", {}) if isinstance(manifest.get("production_policy"), dict) else {}
    active_rows = active_process_rows()
    active_chunks = [
        int(row["chunk_index"]) for row in active_rows if isinstance(row.get("chunk_index"), int)
    ]
    active_chunk_set = set(active_chunks)
    duplicate_active_chunks = sorted(chunk for chunk in active_chunk_set if active_chunks.count(chunk) > 1)
    unknown_active_rows = [row for row in active_rows if row.get("chunk_index") is None]
    rows = manifest.get("chunk_commands", []) if isinstance(manifest.get("chunk_commands"), list) else []

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
        considered = {
            "chunk_index": chunk,
            "output": row.get("output"),
            "output_present": output_present,
            "production_output_dir": row.get("production_output_dir"),
            "production_output_dir_present": pdir_present,
            "active": chunk in active_chunk_set,
            "command_ok": command_passed,
            "command_reason": command_reason,
        }
        considered_rows.append(considered)
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

    manifest_passed = manifest.get("manifest_passed") is True and manifest.get("proposal_allowed") is False
    resume_forbidden = policy.get("resume_allowed") is False
    chunk_count_ok = policy.get("chunk_count") == 63 and len(rows) == 63
    command_boundaries_ok = not blocked_by_command
    active_state_ok = not duplicate_active_chunks and not unknown_active_rows
    partial_state_ok = not blocking_partial_dirs
    max_concurrent_ok = args.max_concurrent > 0 and args.max_concurrent <= 3
    active_within_limit = len(active_chunk_set) <= args.max_concurrent
    launch_capacity = max(args.max_concurrent - len(active_chunk_set), 0)
    launchable_rows = eligible_rows[:launch_capacity]
    launch_allowed = (
        manifest_passed
        and resume_forbidden
        and chunk_count_ok
        and command_boundaries_ok
        and active_state_ok
        and partial_state_ok
        and max_concurrent_ok
        and active_within_limit
        and launch_capacity > 0
        and bool(launchable_rows)
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

    report("manifest-present", bool(manifest), rel(manifest_path))
    report("manifest-passed-support-only", manifest_passed, manifest.get("actual_current_surface_status", ""))
    report("manifest-forbids-resume", resume_forbidden, "replacement row wave must not use --resume")
    report("manifest-chunk-count", chunk_count_ok, f"rows={len(rows)} policy_chunk_count={policy.get('chunk_count')}")
    report("row-commands-are-no-resume-production-commands", command_boundaries_ok, f"blocked={blocked_by_command}")
    report(
        "active-row-processes-without-collision",
        active_state_ok,
        f"active_chunks={sorted(active_chunk_set)} duplicates={duplicate_active_chunks} unknown={len(unknown_active_rows)}",
    )
    report("no-blocking-partial-output-dirs", partial_state_ok, f"blocking_partial_dirs={blocking_partial_dirs}")
    report("concurrency-cap-is-conservative", max_concurrent_ok, f"max_concurrent={args.max_concurrent}")
    report("active-workers-within-cap", active_within_limit, f"active={len(active_chunk_set)} cap={args.max_concurrent}")
    report("launch-mode-explicit", no_unrequested_launch, f"launch_flag={args.launch}")
    report("launched-processes-survived-initial-check", launched_alive, f"launched={launched}")
    report("does-not-authorize-retained-proposal", True, "run-control support only")

    verdict = (
        "The wave launcher consumed the PR #230 two-source taste-radial row manifest, "
        "checked active process occupancy, completed outputs, partial output dirs, "
        "no-resume commands, and a conservative concurrency cap.  It is run-control "
        "support only and does not create C_sx/C_xx row evidence unless the harness "
        "later writes completed chunk certificates."
    )
    all_manifest_outputs_present = (
        len(rows) == 63
        and len(completed_chunks) == 63
        and not eligible_rows
        and not active_chunk_set
        and not blocking_partial_dirs
    )
    exact_next_action = (
        "All manifest row chunks are complete and no row workers are active; do "
        "not launch another wave.  Use the existing chunk package audit and row "
        "combiner gates as bounded C_sx/C_xx support only, then pursue canonical "
        "O_H/source-Higgs, scalar pole/FV/IR, Schur, or physical-response authority."
        if all_manifest_outputs_present
        else (
            "When the active chunks finish, rerun this launcher with --launch and "
            "--max-concurrent 2, then run the row schema/checkpoint gates on each "
            "completed chunk.  Only completed chunk JSON plus pole/FV/IR and "
            "canonical-source authority can become physics evidence."
        )
    )
    result = {
        "actual_current_surface_status": (
            "bounded-support / two-source taste-radial C_sx/C_xx row wave launcher status; "
            "run-control only, not physics evidence"
        ),
        "verdict": verdict,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "A launcher/status certificate cannot identify the taste-radial source "
            "with canonical O_H, cannot supply kappa_s, and cannot turn active or "
            "partial jobs into C_sx/C_xx pole evidence."
        ),
        "bare_retained_allowed": False,
        "launch_mode": bool(args.launch),
        "launch_allowed_before_action": launch_allowed,
        "max_concurrent": args.max_concurrent,
        "manifest_recommended_max_concurrent": policy.get("recommended_max_concurrent_workers"),
        "active_chunk_indices": sorted(active_chunk_set),
        "active_process_count": len(active_rows),
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
            "does not treat active processes, logs, empty directories, partial directories, or launch status as row evidence",
            "does not use --resume for row replacement chunks",
            "does not overwrite completed chunk outputs",
            "does not treat C_sx/C_xx as canonical-Higgs C_sH/C_HH",
            "does not set kappa_s = 1, c2 = 1, or Z_match = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": exact_next_action,
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
