#!/usr/bin/env python3
"""Auto-attempt to close missing-derivation rows via Codex CLI.

Reads `docs/audit/MISSING_DERIVATION_PROMPTS.md`, picks the next row that
hasn't been attempted yet, opens a clean worktree off origin/main, runs
`codex exec` against the prompt body, and — if codex made meaningful
edits — opens a PR for human review and re-audit.

Designed to be run as a background loop. It will:

  - skip rows that have already been attempted (state in
    `logs/science-fix-state.json`)
  - skip rows whose prior attempt timed out, errored, or punted
    (codex made no edits) — pass `--retry-failed` to retry them
  - atomically reserve rows as `in_progress` before work starts, so
    parallel workers do not claim the same row
  - guard each attempt with stale, edit-deadline, and absolute-max timeouts
    (`--codex-timeout-sec` defaults to 1800s = 30 min)
  - if codex makes ANY edit, commit it, push the branch, and open a PR
    titled `science-fix: <claim_id>` so the user can review

It deliberately does NOT try to:

  - Verify the new derivation closes the chain (that belongs to review-loop
    before landing and then to the independent audit lane after merge)
  - Run the modified runner (pre-commit hook + CI handle that)
  - Re-merge the new branch (the PR is for human review)

Usage:

    # Try the next 5 prompts, one per attempt
    python3 scripts/science_fix_loop.py --n 5

    # Dry run: show what would be attempted, no codex call
    python3 scripts/science_fix_loop.py --n 3 --dry-run

    # Retry rows that previously timed out / punted
    python3 scripts/science_fix_loop.py --n 5 --retry-failed

    # Explicitly recover old in-progress markers from a known-dead worker
    python3 scripts/science_fix_loop.py --n 5 --retry-failed --reclaim-stale-sec 7200

    # Restrict to one category
    python3 scripts/science_fix_loop.py --n 5 --category renaming

    # Pick a specific row
    python3 scripts/science_fix_loop.py --claim-id <claim_id>

State file (`logs/science-fix-state.json`):

    {
      "attempts": {
        "<claim_id>": {
          "attempted_at": "<utc iso>",
          "outcome": "in_progress" | "stale_in_progress" | "pr_opened" | "no_edits" | "declined_too_hard" | "stalled_no_edits" | "thinking_only" | "timeout_no_edits" | "pr_opened_partial_stalled" | "pr_opened_partial_thinking_only" | "pr_opened_partial_timeout" | "codex_failed" | "run_error" | "error" | "push_failed" | "pr_failed",
          "worker_id": "<pid-run_id>",
          "branch": "<branch>",
          "pr_url": "<url>",
          "elapsed_sec": <float>,
          "codex_stop_reason": "ok" | "stalled" | "thinking_only" | "timeout" | "error",
          "codex_stdout_tail": "<last 1k chars>",
          "error": "<short error string if applicable>"
        }
      }
    }
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_FILE = REPO_ROOT / "docs" / "audit" / "MISSING_DERIVATION_PROMPTS.md"
STATE_FILE = REPO_ROOT / "logs" / "science-fix-state.json"
WORKTREE_BASE = Path("/tmp") / "science-fix-worktrees"
LOG_DIR = REPO_ROOT / "logs" / "science-fix-runs"

# Three timeout thresholds for one codex attempt:
#
#   stale-kill (default 4 min)       — no progress signal at all (no
#                                      file edits AND no stream bytes
#                                      since last poll). Catches truly
#                                      stuck codex quickly.
#   edit-deadline (default 15 min)   — no file edits AT ALL by this
#                                      mark, even if codex is emitting
#                                      reasoning text. Codex is
#                                      "thinking-only" — likely
#                                      analyzing a problem too hard
#                                      for this loop. Kill and let a
#                                      human take it.
#   absolute max (default 30 min)    — hard backstop. Never extend
#                                      past this regardless.
#
# A legit physics problem solvable in ~15 min of code-writing fits
# inside all three. Hard physics that needs >15 min of pre-writing
# analysis is gated by edit-deadline. Truly runaway is gated by
# absolute max. Combined with the prompt's self-screen preamble (codex
# is asked to decline upfront if it judges the problem too hard for
# 15 min), most hard problems exit in <1 min via SCIENCE_FIX_DECLINED.
DEFAULT_CODEX_TIMEOUT = 1800     # 30 min absolute max
DEFAULT_EDIT_DEADLINE = 900      # 15 min: must have started editing
DEFAULT_STALE_AFTER = 240        # 4 min stale-kill
DEFAULT_MODEL = "gpt-5.5"
DEFAULT_REASONING = "xhigh"
DIFFICULTY_ORDER = {"easy": 0, "medium": 1, "hard": 2, "unknown": 3}

# Self-screen preamble: codex evaluates difficulty first and may
# decline cheaply. Detected via a marker string in stdout so the loop
# can record the decline as outcome=declined_too_hard without burning
# subscription minutes.
DECLINE_MARKER = "SCIENCE_FIX_DECLINED"
SCREENING_PREAMBLE = f"""You are about to attempt a missing-derivation closure as part of an
autonomous science-fix loop. Hard physics problems that need >15 min
of focused human-level analysis BEFORE writing any file edit should be
declined upfront — a human will take them.

STEP 1. Read the prompt below and judge: can the closure plausibly be
done in roughly 15 minutes of code-writing time by an AI? Quick
indicators that the answer is NO:

  - the missing step requires inventing a new theorem or category
    of argument, not just spelling out an existing chain
  - the runner needs substantial new computation infrastructure
  - the load-bearing step is a known open problem in physics
  - the auditor's verdict_rationale explicitly notes that no-go
    obstructions block the natural path

If your honest answer is NO, exit immediately. Print exactly this
single line and STOP without making any file edits:

    {DECLINE_MARKER}: <one-sentence reason>

If your honest answer is YES, proceed to STEP 2.

STEP 2. Begin the prompt below. Use the physics-loop skill. Make
real edits. Do not over-prescribe approach — explore the framework
and let the skill drive.

============================== PROMPT ==============================
"""

CATEGORIES = (
    "renaming",
    "failed",
    "numerical_match",
    "open_gate",
    "conditional_runner_artifact_issue",
    "conditional_scope_too_broad",
    "conditional_missing_bridge_theorem",
)
CATEGORY_HEADER_RE = re.compile(r"^## audited_(\w+)|^## (open_gate)\b", re.MULTILINE)
ROW_BLOCK_RE = re.compile(
    r"^### `([^`]+)`\s*\n"
    r"\*\*Note:\*\* \[([^\]]+)\][^\n]*\|\s*\*\*Descendants:\*\* (\d+)\s*\|\s*\*\*Class:\*\* (\S+)\s*\n"
    r"\n```\n(.*?)\n```\s*$",
    re.MULTILINE | re.DOTALL,
)


def parse_prompts():
    """Return list of dicts: {category, claim_id, note_path, descendants, cls, prompt_body}."""
    text = PROMPTS_FILE.read_text(encoding="utf-8")
    # Find category headers + their byte spans
    categories = []
    header_pattern = (
        r"^## ("
        r"audited_renaming|audited_failed|audited_numerical_match|open_gate"
        r"|audited_conditional_runner_artifact_issue"
        r"|audited_conditional_scope_too_broad"
        r"|audited_conditional_missing_bridge_theorem"
        r")\b"
    )
    cat_normalize = {
        "audited_renaming": "renaming",
        "audited_failed": "failed",
        "audited_numerical_match": "numerical_match",
        "open_gate": "open_gate",
        "audited_conditional_runner_artifact_issue": "conditional_runner_artifact_issue",
        "audited_conditional_scope_too_broad": "conditional_scope_too_broad",
        "audited_conditional_missing_bridge_theorem": "conditional_missing_bridge_theorem",
    }
    for m in re.finditer(header_pattern, text, re.MULTILINE):
        cat_raw = m.group(1)
        categories.append((m.start(), cat_normalize[cat_raw]))
    categories.append((len(text), None))   # sentinel

    # For each category span, parse rows
    rows = []
    for i in range(len(categories) - 1):
        start, cat = categories[i]
        end = categories[i + 1][0]
        block = text[start:end]
        for rm in ROW_BLOCK_RE.finditer(block):
            rows.append({
                "category": cat,
                "claim_id": rm.group(1),
                "note_path": rm.group(2),
                "descendants": int(rm.group(3)),
                "cls": rm.group(4),
                "prompt_body": rm.group(5).strip(),
            })
    return rows


@contextmanager
def state_lock():
    """Acquire an exclusive flock on the state file for the duration of the
    block. Multiple workers running this loop on the same host will queue
    on this lock, so they won't pick the same rows or clobber each other's
    outcome writes. The lockfile lives next to the state file.
    """
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    lock_path = STATE_FILE.with_suffix(STATE_FILE.suffix + ".lock")
    with open(lock_path, "a+", encoding="utf-8") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


def _read_state_unlocked() -> dict:
    if not STATE_FILE.exists():
        return {"attempts": {}}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"attempts": {}}


def _write_state_unlocked(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")


def is_opened_outcome(outcome) -> bool:
    return isinstance(outcome, str) and (
        outcome == "pr_opened" or outcome.startswith("pr_opened_partial_")
    )


def is_active_or_opened_outcome(outcome) -> bool:
    return outcome == "in_progress" or is_opened_outcome(outcome)


def claim_targets(candidates: list[dict], n: int, retry_failed: bool,
                  worker_id: str) -> list[dict]:
    """Atomically reserve up to N candidates by marking them
    `outcome=in_progress` in the state file. Other workers running the
    loop will then skip these rows and pick from what's left.
    """
    with state_lock():
        state = _read_state_unlocked()
        attempts = state.get("attempts", {})
        if retry_failed:
            eligible = [
                r for r in candidates
                if not is_active_or_opened_outcome(
                    attempts.get(r["claim_id"], {}).get("outcome")
                )
            ]
        else:
            eligible = [r for r in candidates if r["claim_id"] not in attempts]
        targets = eligible[:n]
        now = datetime.now(timezone.utc).isoformat()
        for r in targets:
            attempts[r["claim_id"]] = {
                "attempted_at": now,
                "outcome": "in_progress",
                "worker_id": worker_id,
                "category": r["category"],
                "descendants": r["descendants"],
            }
        state["attempts"] = attempts
        _write_state_unlocked(state)
    return targets


def record_outcome(claim_id: str, outcome: dict) -> None:
    """Atomically write the final outcome for one claim, overwriting the
    in-progress marker. Other workers' state is preserved."""
    with state_lock():
        state = _read_state_unlocked()
        state.setdefault("attempts", {})[claim_id] = outcome
        _write_state_unlocked(state)


def reclaim_stale_in_progress(stale_after_sec: int) -> int:
    """Sweep state for `outcome=in_progress` markers older than the cutoff
    and demote them to `outcome=stale_in_progress` so a later
    --retry-failed run picks them up. Crashes leave in-progress markers
    that would otherwise block the row forever; this is the explicit
    recovery path and should not be used while another worker may still be
    alive."""
    cutoff_iso = (
        datetime.now(timezone.utc).timestamp() - stale_after_sec
    )
    reclaimed = 0
    with state_lock():
        state = _read_state_unlocked()
        for cid, a in state.get("attempts", {}).items():
            if a.get("outcome") != "in_progress":
                continue
            try:
                ts = datetime.fromisoformat(
                    a.get("attempted_at", "").replace("Z", "+00:00")
                ).timestamp()
            except Exception:
                continue
            if ts < cutoff_iso:
                a["outcome"] = "stale_in_progress"
                reclaimed += 1
        if reclaimed:
            _write_state_unlocked(state)
    return reclaimed


def git(*args, cwd=None, check=True):
    return subprocess.run(["git", *args], cwd=cwd or REPO_ROOT,
                          capture_output=True, text=True, check=check)


def make_worktree(claim_id: str, run_id: str) -> tuple[Path, str]:
    """Create a fresh worktree off origin/main on a new branch.

    Returns (worktree_path, branch_name).
    """
    # Sanitize claim_id for filesystem + git ref
    slug = re.sub(r"[^a-zA-Z0-9_]", "-", claim_id)[:60]
    branch = f"claude/science-fix/{slug}-{run_id}"
    path = WORKTREE_BASE / f"{slug}-{run_id}"
    WORKTREE_BASE.mkdir(parents=True, exist_ok=True)
    if path.exists():
        # Stale leftover; force-remove
        try:
            git("worktree", "remove", "--force", str(path), check=False)
        except Exception:
            pass
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
    git("fetch", "origin", "main", check=False)
    git("worktree", "add", "-b", branch, str(path), "origin/main")
    return path, branch


def cleanup_worktree(path: Path) -> None:
    git("worktree", "remove", "--force", str(path), check=False)
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)


def _newest_mtime(worktree: Path) -> float:
    """Walk the worktree and return the newest mtime found, ignoring noise
    files (.git, __pycache__, etc.). Used as a proxy for whether codex is
    actively making progress.
    """
    SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache",
                 ".ipynb_checkpoints", "node_modules"}
    newest = 0.0
    for root, dirs, files in os.walk(worktree):
        # In-place prune so we don't descend into junk
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            try:
                m = os.path.getmtime(os.path.join(root, f))
            except OSError:
                continue
            if m > newest:
                newest = m
    return newest


def run_codex(prompt_body: str, worktree: Path, timeout_sec: int,
              model: str, reasoning: str,
              run_log: Path,
              stale_after_sec: int = DEFAULT_STALE_AFTER,
              edit_deadline_sec: int = DEFAULT_EDIT_DEADLINE,
              poll_interval_sec: int = 30,
              progress_callback=None) -> tuple[bool, str, str, float, str]:
    """Run codex exec against the worktree with three progress guards.

    Returns (ok, stdout, stderr, elapsed, stop_reason).

    Behavior:
      - Stale-kill at `stale_after_sec` (default 240s = 4 min): no
        progress signal at all (no file-mtime advance AND no codex
        stream-byte advance) since last poll → kill.
      - Edit-deadline at `edit_deadline_sec` (default 900s = 15 min):
        codex hasn't made ANY file edit yet by this point → kill.
        Codex is "thinking-only" — likely a hard problem.
      - Hard timeout at `timeout_sec` (default 1800s = 30 min):
        absolute backstop, never extended.
      - Self-screen preamble (added at call-time) lets codex decline
        upfront via a SCIENCE_FIX_DECLINED marker; the loop detects
        that string in stdout and records outcome=declined_too_hard.

    `stop_reason` values:
      - "ok"             codex finished naturally
      - "stalled"        no progress signal for stale_after_sec
      - "thinking_only"  no file edits by edit_deadline_sec
      - "timeout"        hit the absolute hard backstop
      - "error"          exception raised
    """
    wrapped_prompt = SCREENING_PREAMBLE + prompt_body
    cmd = [
        "codex", "exec",
        "-C", str(worktree),
        "-s", "workspace-write",
        "-m", model,
        "-c", f'model_reasoning_effort="{reasoning}"',
        wrapped_prompt,
    ]
    t0 = time.time()
    baseline_mtime = _newest_mtime(worktree)
    initial_mtime = baseline_mtime
    last_progress_time = t0
    last_progress_kind = "init"
    last_stream_bytes = 0
    stop_reason = "ok"
    stale_enabled = stale_after_sec > 0 and stale_after_sec < timeout_sec
    edit_deadline_enabled = edit_deadline_sec > 0 and edit_deadline_sec < timeout_sec

    def _terminate_tree(proc: subprocess.Popen, sig: int) -> None:
        try:
            os.killpg(proc.pid, sig)
        except ProcessLookupError:
            pass
        except Exception:
            try:
                proc.send_signal(sig)
            except Exception:
                pass

    try:
        with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as stdout_fh, \
             tempfile.TemporaryFile(mode="w+", encoding="utf-8") as stderr_fh:
            proc = subprocess.Popen(
                cmd,
                stdout=stdout_fh,
                stderr=stderr_fh,
                text=True,
                env=os.environ,
                start_new_session=True,
            )
            while True:
                # Wait poll_interval_sec, then check status.
                try:
                    proc.wait(timeout=poll_interval_sec)
                    # Process exited within the poll interval.
                    break
                except subprocess.TimeoutExpired:
                    pass

                now = time.time()
                elapsed = now - t0

                # Progress signal #1: any file in the worktree touched.
                cur_mtime = _newest_mtime(worktree)
                if cur_mtime > baseline_mtime:
                    last_progress_time = now
                    last_progress_kind = "mtime"
                    baseline_mtime = cur_mtime

                # Progress signal #2: codex stdout/stderr stream grew
                # (codex is THINKING — emitting reasoning text or
                # tool-call traces). Counts as progress so we don't
                # kill an actively-thinking codex.
                try:
                    cur_stream_bytes = (
                        os.fstat(stdout_fh.fileno()).st_size
                        + os.fstat(stderr_fh.fileno()).st_size
                    )
                except Exception:
                    cur_stream_bytes = last_stream_bytes
                if cur_stream_bytes > last_stream_bytes:
                    last_progress_time = now
                    last_progress_kind = "stream"
                    last_stream_bytes = cur_stream_bytes

                stale_for = now - last_progress_time
                files_touched = baseline_mtime > initial_mtime

                if progress_callback:
                    progress_callback(elapsed, stale_for, last_progress_kind,
                                       cur_stream_bytes, files_touched)

                # Three kill conditions, checked in order of severity:
                if stale_enabled and stale_for >= stale_after_sec:
                    stop_reason = "stalled"
                    break
                if (edit_deadline_enabled
                        and elapsed >= edit_deadline_sec
                        and not files_touched):
                    stop_reason = "thinking_only"
                    break
                if elapsed >= timeout_sec:
                    stop_reason = "timeout"
                    break

            if stop_reason in ("stalled", "timeout", "thinking_only"):
                _terminate_tree(proc, signal.SIGTERM)
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    _terminate_tree(proc, signal.SIGKILL)
                    proc.wait(timeout=5)
            elapsed = time.time() - t0
            stdout_fh.seek(0)
            stderr_fh.seek(0)
            stdout = stdout_fh.read()
            stderr = stderr_fh.read()

        if stop_reason == "ok":
            ok = proc.returncode == 0
            return ok, stdout, stderr, elapsed, "ok"
        # Annotate stderr with reason for downstream visibility
        annot = f"\n[codex_{stop_reason} after {elapsed:.0f}s "\
                f"(stale_after={stale_after_sec}s, hard_timeout={timeout_sec}s)]"
        return False, stdout, (stderr or "") + annot, elapsed, stop_reason

    except Exception as exc:
        try:
            if "proc" in locals():
                _terminate_tree(proc, signal.SIGKILL)
        except Exception:
            pass
        elapsed = time.time() - t0
        return False, "", f"[run_codex error: {exc!r}]", elapsed, "error"


def has_changes(worktree: Path) -> bool:
    res = git("status", "--porcelain", cwd=worktree, check=False)
    return bool(res.stdout.strip())


def diff_summary(worktree: Path) -> str:
    res = git("diff", "--stat", "HEAD", cwd=worktree, check=False)
    return (res.stdout or "").strip()


def commit_and_push(claim_id: str, worktree: Path, branch: str,
                    summary: str) -> tuple[bool, str]:
    add = git("add", "-A", cwd=worktree, check=False)
    if add.returncode != 0:
        return False, f"git add failed: {(add.stderr or '').strip()[:200]}"
    diff = git("diff", "--cached", "--quiet", cwd=worktree, check=False)
    if diff.returncode == 0:
        return False, "nothing to commit"
    msg = (
        f"science-fix: attempt to close {claim_id} derivation\n\n"
        f"Automated by scripts/science_fix_loop.py.\n"
        f"Codex GPT-5.5 at xhigh attempted the derivation per the prompt in\n"
        f"docs/audit/MISSING_DERIVATION_PROMPTS.md. Review carefully — the\n"
        f"independent audit only runs after merge.\n\n"
        f"Diff summary:\n{summary}\n"
    )
    commit = git("commit", "-m", msg, cwd=worktree, check=False)
    if commit.returncode != 0:
        return False, f"commit failed: {(commit.stderr or commit.stdout).strip()[:200]}"
    push = git("push", "-u", "origin", branch, cwd=worktree, check=False)
    if push.returncode != 0:
        return False, f"push failed: {(push.stderr or '').strip()[:200]}"
    return True, "pushed"


def open_pr(claim_id: str, branch: str, prompt_body: str,
            descendants: int, category: str, codex_tail: str,
            worktree: Path) -> tuple[bool, str]:
    title = f"science-fix: attempt to close {claim_id}"
    if len(title) > 70:
        title = title[:67] + "..."
    body = f"""## Summary

Automated attempt by `scripts/science_fix_loop.py` to close the missing
derivation in `{claim_id}`.

- **Category:** `{category}`
- **Transitive descendants if closed:** {descendants}
- **Original prompt:** see `docs/audit/MISSING_DERIVATION_PROMPTS.md` (search for `{claim_id}`)

## What this PR does

Codex GPT-5.5 at xhigh reasoning was given the missing-derivation
prompt in a clean worktree off `origin/main` and asked to close the
chain. It made the diff in this PR.

## Review checklist

- [ ] Run the repo-native review-loop before landing; automated science
      attempts can be wrong
- [ ] If the new derivation survives review-loop, land it through the normal
      path and let the independent audit batch re-audit the row after merge
- [ ] If the diff is wrong-headed, close this PR; the loop won't retry
      automatically (state file: `logs/science-fix-state.json`)

## Codex output tail

```
{codex_tail[-2000:]}
```

🤖 Generated by `scripts/science_fix_loop.py` (codex GPT-5.5, xhigh)
"""
    res = subprocess.run(
        ["gh", "pr", "create", "--title", title, "--body", body],
        cwd=worktree,
        capture_output=True,
        text=True,
        check=False,
    )
    if res.returncode != 0:
        return False, f"gh pr create failed: {(res.stderr or '').strip()[:200]}"
    url = (res.stdout or "").strip().split("\n")[-1]
    return True, url


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=5,
                   help="How many prompts to attempt this run (default 5)")
    p.add_argument("--codex-timeout-sec", type=int, default=DEFAULT_CODEX_TIMEOUT,
                   help=f"Absolute max budget per attempt — never extended. "
                        f"Default {DEFAULT_CODEX_TIMEOUT}s = 30 min. "
                        f"This is just a runaway safety net; the typical "
                        f"kill condition is stale-kill or edit-deadline.")
    p.add_argument("--edit-deadline-sec", type=int, default=DEFAULT_EDIT_DEADLINE,
                   help=f"Kill codex if no file edit has been made by "
                        f"this many elapsed seconds, even if codex is "
                        f"emitting reasoning text. Default "
                        f"{DEFAULT_EDIT_DEADLINE}s = 15 min. Codex is "
                        f"considered 'thinking-only' past this point — "
                        f"likely a HARD problem. Set to a value "
                        f">= --codex-timeout-sec to disable.")
    p.add_argument("--stale-after-sec", type=int, default=DEFAULT_STALE_AFTER,
                   help=f"Kill codex if NO progress signal at all "
                        f"(no file edit AND no stream byte) within this "
                        f"window. Default {DEFAULT_STALE_AFTER}s = 4 min. "
                        f"This is the fastest kill — catches truly stuck "
                        f"codex. Set to a value >= --codex-timeout-sec to "
                        f"disable.")
    p.add_argument("--poll-interval-sec", type=int, default=30,
                   help="How often to check codex's progress (default 30s).")
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help=f"Codex model (default {DEFAULT_MODEL})")
    p.add_argument("--reasoning", default=DEFAULT_REASONING,
                   help=f"Codex reasoning effort (default {DEFAULT_REASONING})")
    p.add_argument("--category",
                   choices=CATEGORIES, default=None,
                   help="Restrict to one category")
    p.add_argument("--difficulty",
                   default="easy,medium,unknown",
                   help="Comma-separated difficulty buckets to attempt. "
                        "Default 'easy,medium,unknown' — skips hard rows "
                        "(those need human review). Pass "
                        "'easy,medium,hard,unknown' to attempt everything, "
                        "or 'easy' for the smallest fast-win batch. Rows "
                        "without a rating are treated as 'unknown'. The "
                        "ratings file is produced by "
                        "scripts/classify_missing_derivations.py.")
    p.add_argument("--claim-id", default=None,
                   help="Run on this specific claim_id only")
    p.add_argument("--retry-failed", action="store_true",
                   help="Re-attempt rows whose prior attempt did not open a PR")
    p.add_argument("--dry-run", action="store_true",
                   help="Show targets and exit without invoking codex")
    p.add_argument("--keep-worktrees", action="store_true",
                   help="Don't remove worktrees after each attempt (for debugging)")
    p.add_argument("--reclaim-stale-sec", type=int, default=-1,
                   help="Sweep `outcome=in_progress` markers older than this "
                        "many seconds and demote them to `stale_in_progress` "
                        "before the run starts, so a crashed worker's "
                        "abandoned rows can be retried via --retry-failed. "
                        "Disabled by default. Use only when no older worker is "
                        "still alive, or set a cutoff longer than the maximum "
                        "live worker runtime.")
    args = p.parse_args()
    if args.codex_timeout_sec <= 0:
        p.error("--codex-timeout-sec must be positive")
    if args.stale_after_sec < 0:
        p.error("--stale-after-sec must be non-negative")
    if args.poll_interval_sec <= 0:
        p.error("--poll-interval-sec must be positive")
    allowed_difficulties = {
        d.strip().lower() for d in args.difficulty.split(",") if d.strip()
    }
    invalid_difficulties = allowed_difficulties - set(DIFFICULTY_ORDER)
    if invalid_difficulties:
        bad = ", ".join(sorted(invalid_difficulties))
        p.error(f"--difficulty contains invalid bucket(s): {bad}")
    if not allowed_difficulties:
        p.error("--difficulty must include at least one bucket")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex[:8]
    run_log = LOG_DIR / f"loop-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{run_id}.jsonl"
    print(f"Loop run log: {run_log}")
    print(f"Codex model: {args.model}  reasoning: {args.reasoning}  "
          f"timeout: {args.codex_timeout_sec}s  stale_after: "
          f"{args.stale_after_sec}s  edit_deadline: "
          f"{args.edit_deadline_sec}s  poll: {args.poll_interval_sec}s")

    rows = parse_prompts()
    if not rows:
        print(f"No prompts found in {PROMPTS_FILE.relative_to(REPO_ROOT)}")
        return 1

    # Optional: sweep stale in-progress markers from prior crashed runs. This
    # is disabled by default because a fixed cutoff can create overlaps if a
    # long-running live worker has pre-reserved later rows.
    if args.reclaim_stale_sec >= 0:
        n_reclaim = reclaim_stale_in_progress(args.reclaim_stale_sec)
        if n_reclaim:
            print(f"Reclaimed {n_reclaim} stale in-progress marker(s) (older than "
                  f"{args.reclaim_stale_sec}s) -> outcome=stale_in_progress")

    # Filter pre-claim (non-locking, just for messaging).
    candidates = rows
    if args.category:
        candidates = [r for r in candidates if r["category"] == args.category]
    if args.claim_id:
        candidates = [r for r in candidates if r["claim_id"] == args.claim_id]

    # Difficulty filtering + sort. If a difficulty file exists, attach the
    # rating to each row, restrict to allowed difficulties (default
    # easy+medium+unknown), and sort easy → medium → hard → unknown so
    # we attempt fast wins first. Rows without a rating are treated as
    # "unknown" and included unless --difficulty explicitly excludes them.
    difficulty_file = REPO_ROOT / "docs" / "audit" / "data" / "missing_derivation_difficulty.json"
    ratings: dict = {}
    if difficulty_file.exists():
        try:
            ratings = (json.loads(difficulty_file.read_text(encoding="utf-8"))
                       .get("ratings", {}))
        except Exception:
            ratings = {}
    for r in candidates:
        rating = ratings.get(r["claim_id"]) or {}
        difficulty = str(rating.get("difficulty", "unknown")).strip().lower()
        r["difficulty"] = difficulty if difficulty in DIFFICULTY_ORDER else "unknown"

    # Filter by allowed difficulties.
    candidates = [r for r in candidates if r["difficulty"] in allowed_difficulties]

    # Sort: easy (rank 0) → medium (1) → hard (2) → unknown (3),
    # then descendants desc so highest-leverage easy attempted first.
    candidates.sort(key=lambda r: (
        DIFFICULTY_ORDER.get(r["difficulty"], 99),
        -r["descendants"],
    ))

    # Atomic claim: takes the lock, marks N rows as in_progress, and
    # returns them. Other workers running this loop in parallel will skip
    # rows we've claimed (and we'll skip theirs).
    worker_id = f"pid{os.getpid()}-{run_id}"
    if args.dry_run:
        # Dry-run reads state but does not claim — just shows what WOULD
        # be picked up.
        with state_lock():
            state = _read_state_unlocked()
        attempts = state.get("attempts", {})
        if args.retry_failed:
            eligible = [
                r for r in candidates
                if not is_active_or_opened_outcome(
                    attempts.get(r["claim_id"], {}).get("outcome")
                )
            ]
        else:
            eligible = [r for r in candidates if r["claim_id"] not in attempts]
        targets = eligible[: args.n]
    else:
        targets = claim_targets(candidates, args.n, args.retry_failed, worker_id)

    print(f"Total prompts: {len(rows)}; selected: {len(targets)}")
    if targets and not args.dry_run:
        print(f"Worker id: {worker_id}")

    if not targets:
        print("Nothing to do.")
        return 0

    if args.dry_run:
        print("\n[dry-run] Would attempt:")
        for r in targets:
            print(f"  [{r['category']:<15s}] diff={r['difficulty']:<7s} "
                  f"desc={r['descendants']:4d}  {r['claim_id']}")
        return 0

    applied = punted = errored = pr_failed = 0
    for i, r in enumerate(targets, 1):
        cid = r["claim_id"]
        print(f"\n[{i}/{len(targets)}] [{r['category']}] desc={r['descendants']}  {cid}")
        outcome: dict = {
            "attempted_at": datetime.now(timezone.utc).isoformat(),
            "worker_id": worker_id,
            "category": r["category"],
            "descendants": r["descendants"],
        }
        try:
            worktree, branch = make_worktree(cid, run_id)
        except Exception as e:
            print(f"  ! worktree create failed: {e!r}")
            outcome["outcome"] = "error"
            outcome["error"] = f"worktree create: {e!r}"
            errored += 1
            record_outcome(cid, outcome)
            continue

        try:
            def _progress(elapsed_, stale_, last_kind, stream_bytes, files_touched):
                # Live status to stdout. last_kind is "init" / "mtime" /
                # "stream" — telling them whether codex is editing files
                # or just thinking. files_touched flips True when codex
                # has made any file edit at all in this attempt; it
                # gates the edit-deadline.
                touched = "Y" if files_touched else "N"
                print(f"    [progress] elapsed={elapsed_:5.0f}s  "
                      f"stalled_for={stale_:5.0f}s  "
                      f"last={last_kind}  bytes={stream_bytes}  "
                      f"edited={touched}  "
                      f"(stale@{args.stale_after_sec}s, "
                      f"edit_deadline@{args.edit_deadline_sec}s, "
                      f"max@{args.codex_timeout_sec}s)",
                      flush=True)

            ok, stdout, stderr, elapsed, stop_reason = run_codex(
                r["prompt_body"], worktree,
                args.codex_timeout_sec, args.model, args.reasoning,
                run_log,
                stale_after_sec=args.stale_after_sec,
                edit_deadline_sec=args.edit_deadline_sec,
                poll_interval_sec=args.poll_interval_sec,
                progress_callback=_progress,
            )

            # Detect codex's self-screen decline — if the prompt's
            # screening preamble caused codex to print
            # SCIENCE_FIX_DECLINED at the top, mark this row as
            # declined cheaply (it'll be retried only via
            # --retry-failed since it's not punted on a real attempt).
            decline_match = None
            if stdout and DECLINE_MARKER in stdout:
                # Extract the one-line reason after the marker
                m = re.search(rf"{re.escape(DECLINE_MARKER)}:\s*([^\n]+)", stdout)
                decline_match = m.group(1).strip() if m else "(no reason given)"
            outcome["elapsed_sec"] = round(elapsed, 1)
            outcome["codex_returncode_ok"] = ok
            outcome["codex_stop_reason"] = stop_reason
            outcome["codex_stdout_tail"] = (stdout or "")[-1000:]
            outcome["codex_stderr_tail"] = (stderr or "")[-500:]

            # Decide whether this attempt produced anything worth promoting
            # to a PR. Order: codex's self-screen decline first (cheap
            # exit), then structural codex failures, then check the
            # worktree state.
            promote_edits = False
            if decline_match is not None:
                print(f"  DECLINED self-screen ({elapsed:.0f}s): {decline_match}")
                outcome["outcome"] = "declined_too_hard"
                outcome["decline_reason"] = decline_match
                punted += 1
            elif stop_reason == "error":
                print(f"  RUN ERROR: {(stderr or '').strip()[:200]}")
                outcome["outcome"] = "run_error"
                errored += 1
            elif stop_reason == "ok" and not ok:
                print(f"  codex exec failed (rc!=0): {(stderr or '').strip()[:200]}")
                outcome["outcome"] = "codex_failed"
                errored += 1
            else:
                # stop_reason in {ok, timeout, stalled, thinking_only}
                # — codex either finished or was killed early. Any of
                # these can still have produced useful partial edits.
                worktree_has_changes = has_changes(worktree)
                if stop_reason == "stalled" and not worktree_has_changes:
                    print(f"  STALLED with no edits after {elapsed:.0f}s — "
                          f"likely a HARD physics problem")
                    outcome["outcome"] = "stalled_no_edits"
                    punted += 1
                elif stop_reason == "thinking_only" and not worktree_has_changes:
                    # By definition: no file edit by edit_deadline_sec.
                    print(f"  THINKING-ONLY past {elapsed:.0f}s — codex "
                          f"never started editing; treating as HARD")
                    outcome["outcome"] = "thinking_only"
                    punted += 1
                elif stop_reason == "timeout" and not worktree_has_changes:
                    print(f"  ABSOLUTE MAX with no edits after {elapsed:.0f}s")
                    outcome["outcome"] = "timeout_no_edits"
                    punted += 1
                elif not worktree_has_changes:
                    print(f"  no edits (codex punted) in {elapsed:.0f}s")
                    outcome["outcome"] = "no_edits"
                    punted += 1
                else:
                    promote_edits = True

            if promote_edits:
                summary = diff_summary(worktree)
                tag = {"ok": "edits made",
                       "stalled": "STALLED but partial edits",
                       "thinking_only": "THINKING-ONLY but partial edits",
                       "timeout": "ABSOLUTE MAX but partial edits"}[stop_reason]
                print(f"  {tag} in {elapsed:.0f}s; diff:\n    {summary}")
                ok2, msg = commit_and_push(cid, worktree, branch, summary)
                if not ok2:
                    print(f"  push failed: {msg}")
                    outcome["outcome"] = "push_failed"
                    outcome["push_error"] = msg
                    pr_failed += 1
                else:
                    pr_ok, pr_msg = open_pr(
                        cid, branch, r["prompt_body"],
                        r["descendants"], r["category"],
                        stdout or "",
                        worktree,
                    )
                    if not pr_ok:
                        print(f"  PR create failed: {pr_msg}")
                        outcome["outcome"] = "pr_failed"
                        outcome["pr_error"] = pr_msg
                        outcome["branch"] = branch
                        pr_failed += 1
                    else:
                        # If codex was stalled or hard-timed-out but produced
                        # edits, the PR is real but the verdict_rationale that
                        # attached can record it as a partial attempt for the
                        # human reviewer.
                        verdict = "pr_opened" if stop_reason == "ok" else f"pr_opened_partial_{stop_reason}"
                        print(f"  PR opened ({verdict}): {pr_msg}")
                        outcome["outcome"] = verdict
                        outcome["pr_url"] = pr_msg
                        outcome["branch"] = branch
                        applied += 1
        except Exception as e:
            print(f"  ! attempt error: {e!r}")
            outcome["outcome"] = "error"
            outcome["error"] = repr(e)
            errored += 1
        finally:
            with run_log.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"claim_id": cid, **outcome}) + "\n")
            record_outcome(cid, outcome)
            if not args.keep_worktrees:
                cleanup_worktree(worktree)

    print(f"\nDone. attempted={len(targets)} pr_opened={applied} punted={punted} errored={errored} pr_failed={pr_failed}")
    print(f"State: {STATE_FILE.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
