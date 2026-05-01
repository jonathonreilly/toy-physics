#!/usr/bin/env python3
"""Lane 2 atomic Autoresearch packet verifier.

This is a process runner for the parked Autoresearch packet, not a physics
theorem runner. It verifies that the preserved loop pack is present and then
replays the six Lane 2 atomic artifact runners that the Autoresearch block
produced.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / ".claude/science/physics-loops/lane2-atomic-scale-20260428"

REQUIRED_PACK_FILES = [
    "GOAL.md",
    "ASSUMPTIONS_AND_IMPORTS.md",
    "NO_GO_LEDGER.md",
    "ROUTE_PORTFOLIO.md",
    "ARTIFACT_PLAN.md",
    "LITERATURE_BRIDGES.md",
    "REVIEW_HISTORY.md",
    "HANDOFF.md",
    "STATE.yaml",
    "STOP_REQUESTED",
    "PR_BODY_block01.md",
]

REQUIRED_NOTES = [
    "ATOMIC_QED_THRESHOLD_BRIDGE_FIREWALL_NOTE_2026-05-01.md",
    "ATOMIC_NR_COULOMB_SCALE_BRIDGE_STRETCH_NOTE_2026-05-01.md",
    "ATOMIC_RYDBERG_GATE_FACTORIZATION_FANOUT_NOTE_2026-05-01.md",
    "ATOMIC_PLANCK_UNIT_MAP_FIREWALL_NOTE_2026-05-01.md",
    "ATOMIC_ALPHA0_THRESHOLD_MOMENT_NO_GO_NOTE_2026-05-01.md",
    "ATOMIC_MASSIVE_NR_LIMIT_BRIDGE_NOTE_2026-05-01.md",
]

SCIENCE_RUNNERS = [
    "scripts/frontier_atomic_qed_threshold_bridge_firewall.py",
    "scripts/frontier_atomic_nr_coulomb_scale_bridge.py",
    "scripts/frontier_atomic_rydberg_gate_factorization_fanout.py",
    "scripts/frontier_atomic_planck_unit_firewall.py",
    "scripts/frontier_atomic_alpha0_threshold_moment_no_go.py",
    "scripts/frontier_atomic_massive_nr_limit_bridge.py",
]

REQUIRED_STATE_MARKERS = [
    "loop_slug: \"lane2-atomic-scale-20260428\"",
    "target: \"best-honest-status\"",
    "claim_state:",
    "open_imports:",
    "forbidden_imports:",
    "commands_run:",
    "pr_status:",
]


class CheckLog:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0

    def check(self, condition: bool, name: str, detail: str = "") -> None:
        if condition:
            self.passed += 1
            status = "PASS"
        else:
            self.failed += 1
            status = "FAIL"
        suffix = f"  ({detail})" if detail else ""
        print(f"  [{status}] {name}{suffix}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def parse_pass_fail(output: str) -> tuple[int, int] | None:
    matches = re.findall(r"PASS=(\d+)\s+FAIL=(\d+)", output)
    if not matches:
        return None
    passed, failed = matches[-1]
    return int(passed), int(failed)


def run_python(path: str, log: CheckLog) -> None:
    env = os.environ.copy()
    scripts_path = str(ROOT / "scripts")
    env["PYTHONPATH"] = scripts_path + os.pathsep + env.get("PYTHONPATH", "")

    rel = Path(path)
    cmd = [sys.executable, str(ROOT / rel)]
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    parsed = parse_pass_fail(proc.stdout)
    detail = "no PASS/FAIL summary found"
    ok = proc.returncode == 0 and parsed is not None
    if parsed is not None:
        passed, failed = parsed
        ok = ok and passed > 0 and failed == 0
        detail = f"return={proc.returncode}, PASS={passed}, FAIL={failed}"
    else:
        detail = f"return={proc.returncode}, {detail}"
    log.check(ok, f"run {path}", detail)


def compile_python(path: str, log: CheckLog) -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "py_compile", str(ROOT / path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    log.check(proc.returncode == 0, f"compile {path}", f"return={proc.returncode}")
    if proc.returncode != 0:
        print(proc.stdout)


def main() -> int:
    log = CheckLog()

    section("Lane 2 Atomic Autoresearch Packet")
    log.check(PACK.is_dir(), "loop pack exists", str(PACK.relative_to(ROOT)))

    for name in REQUIRED_PACK_FILES:
        path = PACK / name
        log.check(path.is_file(), f"pack file {name} exists")

    for name in REQUIRED_NOTES:
        path = PACK / "notes" / name
        log.check(path.is_file(), f"artifact note {name} exists")

    state_path = PACK / "STATE.yaml"
    if state_path.is_file():
        state = state_path.read_text(encoding="utf-8")
        for marker in REQUIRED_STATE_MARKERS:
            log.check(marker in state, f"STATE.yaml contains {marker}")

    section("Preserved Log Summaries")
    for log_path in sorted((PACK / "logs").glob("atomic_*_2026-05-01.log")):
        text = log_path.read_text(encoding="utf-8")
        parsed = parse_pass_fail(text)
        ok = parsed is not None and parsed[0] > 0 and parsed[1] == 0
        detail = "no PASS/FAIL summary found"
        if parsed is not None:
            detail = f"PASS={parsed[0]}, FAIL={parsed[1]}"
        log.check(ok, f"saved log {log_path.name}", detail)

    section("Science Runner Replay")
    for runner in SCIENCE_RUNNERS:
        log.check((ROOT / runner).is_file(), f"runner exists {runner}")
        compile_python(runner, log)
        run_python(runner, log)

    section("Summary")
    print(f"PASS={log.passed} FAIL={log.failed}")
    if log.failed:
        print("STATUS: parked packet verification failed.")
        return 1
    print("STATUS: parked Lane 2 Autoresearch packet verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
