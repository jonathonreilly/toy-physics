#!/usr/bin/env python3
"""Branch-local supervisor for a fixed-duration physics-loop campaign."""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time


LOOP = Path(__file__).resolve().parent
ROOT = LOOP.parents[3]
LOG = LOOP / "supervisor.log"
STATUS = LOOP / "supervisor_status.json"
LOCK = LOOP / "supervisor.lock"
LAST_MESSAGE = LOOP / "last_codex_message.md"
GLOBAL_STOP = LOOP / "CAMPAIGN_GLOBAL_STOP_ALLOWED"
USER_STOP = LOOP / "USER_STOP_REQUESTED"
CODEX = Path("/Users/jonBridger/.npm-global/bin/codex")
LAUNCH_ENV_PATH = (
    "/opt/homebrew/bin:"
    "/Users/jonBridger/.npm-global/bin:"
    "/usr/local/bin:"
    "/usr/bin:"
    "/bin:"
    "/usr/sbin:"
    "/sbin"
)


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso(ts: dt.datetime) -> str:
    return ts.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def append_log(message: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"[{iso(utc_now())}] {message}\n")
        fh.flush()


def write_status(**updates: object) -> None:
    data = {}
    if STATUS.exists():
        try:
            data = json.loads(STATUS.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {"status_parse_error": True}
    data.update(updates)
    data["updated_utc"] = iso(utc_now())
    STATUS.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_prompt(iteration: int, deadline: dt.datetime, model: str) -> str:
    remaining = max(0, int((deadline - utc_now()).total_seconds()))
    remaining_minutes = max(1, remaining // 60)
    return f"""Use the repo-native $physics-loop skill from docs/ai_methodology/skills/physics-loop/SKILL.md.

User request: run a physics-loop campaign for 4 hours on the most impactful open science lanes.

Current launch context:
- Worktree: {ROOT}
- Supervisor branch: physics-loop/impact-campaign-20260429
- Base: origin/main at 462696d1
- Loop pack: .claude/science/physics-loops/impact-campaign-20260429/
- This is supervisor iteration {iteration}; approximately {remaining_minutes} minutes remain before the hard deadline.
- Model requested by supervisor: {model}

Required behavior:
1. Reread docs/ai_methodology/skills/physics-loop/SKILL.md and references/long-running-execution.md.
2. Treat this as --mode campaign --runtime {remaining_minutes}m --target best-honest-status.
3. Refresh OPPORTUNITY_QUEUE.md from current repo surfaces before choosing the block.
4. Prefer the most impactful retained-grade positive opportunity, but use the narrowest honest status. Do not use bare retained/promoted in branch-local artifacts.
5. Use proposed_retained/proposed_promoted only if CLAIM_STATUS_CERTIFICATE.md permits a theorem-grade author proposal and explicitly says independent audit remains required.
6. If one lane hits no-go, support-only, human-judgment blocker, failed certificate, dirty PR, or GitHub/auth failure, checkpoint/demote/backlog, refresh the opportunity queue, and pivot. Do not end the campaign for a local stop.
7. At each coherent science-block closure, commit, push, and open a review PR, or write complete PR_BACKLOG.md if PR creation fails.
8. Keep science-run changes branch-local: do not weave into repo-wide authority surfaces.
9. If and only if every viable opportunity is globally exhausted before the deadline, write CAMPAIGN_GLOBAL_STOP_ALLOWED with a queue-based justification.
10. Before returning, update STATE.yaml and HANDOFF.md with the exact reason for return and the next action.

Do not ask the user mid-run. Work autonomously until either the remaining runtime is exhausted or a documented global stop condition is reached.
"""


def run_iteration(iteration: int, deadline: dt.datetime, model: str) -> int:
    prompt = build_prompt(iteration, deadline, model)
    cmd = [
        str(CODEX),
        "exec",
        "--full-auto",
        "-C",
        str(ROOT),
        "-m",
        model,
        "--output-last-message",
        str(LAST_MESSAGE),
        prompt,
    ]
    remaining = max(60, int((deadline - utc_now()).total_seconds()))
    append_log("starting codex iteration %d with %d seconds remaining" % (iteration, remaining))
    write_status(
        state="running_codex",
        iteration=iteration,
        deadline_utc=iso(deadline),
        model=model,
        pid=os.getpid(),
        last_command=" ".join(cmd[:7]) + " ...",
    )
    with LOG.open("a", encoding="utf-8") as log_fh:
        log_fh.write("\n=== codex iteration %d start %s ===\n" % (iteration, iso(utc_now())))
        log_fh.flush()
        env = os.environ.copy()
        env["PATH"] = LAUNCH_ENV_PATH
        env.setdefault("HOME", "/Users/jonBridger")
        env.setdefault("SHELL", "/bin/zsh")
        try:
            completed = subprocess.run(
                cmd,
                cwd=str(ROOT),
                env=env,
                stdout=log_fh,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=remaining,
                check=False,
            )
            rc = completed.returncode
        except subprocess.TimeoutExpired:
            log_fh.write("\n=== codex iteration %d timed out at campaign deadline ===\n" % iteration)
            log_fh.flush()
            rc = 124
    append_log("codex iteration %d exited rc=%d" % (iteration, rc))
    write_status(state="codex_exited", iteration=iteration, last_returncode=rc)
    return rc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration-hours", type=float, default=4.0)
    parser.add_argument("--model", default="gpt-5.5")
    parser.add_argument("--max-restarts", type=int, default=24)
    args = parser.parse_args()

    deadline = utc_now() + dt.timedelta(hours=args.duration_hours)
    LOOP.mkdir(parents=True, exist_ok=True)

    with LOCK.open("w", encoding="utf-8") as lock_fh:
        try:
            fcntl.flock(lock_fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            append_log("another supervisor holds the branch-local lock; exiting")
            write_status(state="lock_conflict", pid=os.getpid())
            return 2

        lock_fh.write("%s pid=%s deadline=%s\n" % (iso(utc_now()), os.getpid(), iso(deadline)))
        lock_fh.flush()
        append_log("supervisor acquired lock; deadline=%s" % iso(deadline))
        write_status(
            state="supervisor_started",
            pid=os.getpid(),
            deadline_utc=iso(deadline),
            root=str(ROOT),
            loop=str(LOOP),
            model=args.model,
        )

        iteration = 0
        while utc_now() < deadline:
            if USER_STOP.exists():
                append_log("USER_STOP_REQUESTED present; stopping supervisor")
                write_status(state="user_stop_requested", iteration=iteration)
                return 0
            if GLOBAL_STOP.exists():
                append_log("CAMPAIGN_GLOBAL_STOP_ALLOWED present; stopping supervisor")
                write_status(state="global_stop_allowed", iteration=iteration)
                return 0
            if iteration >= args.max_restarts:
                append_log("max restart count reached before deadline")
                write_status(state="max_restarts_reached", iteration=iteration)
                return 3
            iteration += 1
            rc = run_iteration(iteration, deadline, args.model)
            if utc_now() >= deadline:
                break
            if GLOBAL_STOP.exists() or USER_STOP.exists():
                continue
            append_log("iteration returned before deadline; restarting after short pause")
            time.sleep(20 if rc == 0 else 60)

        append_log("deadline reached; supervisor exiting")
        write_status(state="deadline_reached", iteration=iteration, deadline_utc=iso(deadline))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
