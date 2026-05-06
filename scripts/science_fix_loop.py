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
  - cap each attempt at `--codex-timeout-sec` (default 900s = 15 min)
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
          "outcome": "in_progress" | "stale_in_progress" | "pr_opened" | "no_edits" | "stalled_no_edits" | "timeout_no_edits" | "pr_opened_partial_stalled" | "pr_opened_partial_timeout" | "codex_failed" | "run_error" | "push_failed",
          "worker_id": "<pid-run_id>",
          "branch": "<branch>",
          "pr_url": "<url>",
          "elapsed_sec": <float>,
          "codex_stop_reason": "ok" | "stalled" | "timeout" | "error",
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

DEFAULT_CODEX_TIMEOUT = 900   # 15 min
DEFAULT_MODEL = "gpt-5.5"
DEFAULT_REASONING = "xhigh"

CATEGORIES = ("renaming", "failed", "numerical_match", "open_gate")
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
    for m in re.finditer(r"^## (audited_renaming|audited_failed|audited_numerical_match|open_gate)\b",
                         text, re.MULTILINE):
        cat_raw = m.group(1)
        # Normalize to short names
        cat = {
            "audited_renaming": "renaming",
            "audited_failed": "failed",
            "audited_numerical_match": "numerical_match",
            "open_gate": "open_gate",
        }[cat_raw]
        categories.append((m.start(), cat))
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
                if attempts.get(r["claim_id"], {}).get("outcome") not in
                ("pr_opened", "in_progress")
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
              stale_after_sec: int = 240,
              poll_interval_sec: int = 30,
              progress_callback=None) -> tuple[bool, str, str, float, str]:
    """Run codex exec against the worktree with a progress-check guard.

    Returns (ok, stdout, stderr, elapsed, stop_reason).

    Behavior:
      - Hard timeout at `timeout_sec` (default 900s = 15 min) — backstop.
      - Stale-kill at `stale_after_sec` (default 240s = 4 min) — if no
        file in the worktree has been touched within this window,
        codex is considered stuck on a hard physics problem and is
        terminated. Captured cleanly so the partial diff (if any) is
        preserved.
      - Poll every `poll_interval_sec` seconds (default 30s).
      - `progress_callback(elapsed, stale_for, last_kind, stream_bytes)` is called on each poll
        if provided, for live-status output.

    `stop_reason` values:
      - "ok"          codex finished naturally
      - "stalled"     killed because no file was touched for stale_after_sec
      - "timeout"     hit the hard backstop
      - "error"       exception raised
    """
    cmd = [
        "codex", "exec",
        "-C", str(worktree),
        "-s", "workspace-write",
        "-m", model,
        "-c", f'model_reasoning_effort="{reasoning}"',
        prompt_body,
    ]
    t0 = time.time()
    baseline_mtime = _newest_mtime(worktree)
    last_progress_time = t0  # wall time of last detected progress signal
    last_progress_kind = "init"  # "mtime" | "stream" — which signal moved last
    last_stream_bytes = 0
    stop_reason = "ok"
    stale_enabled = stale_after_sec > 0 and stale_after_sec < timeout_sec

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

                # Progress signal #1: any tracked file in the worktree
                # touched since last poll.
                cur_mtime = _newest_mtime(worktree)
                if cur_mtime > baseline_mtime:
                    last_progress_time = now
                    last_progress_kind = "mtime"
                    baseline_mtime = cur_mtime

                # Progress signal #2: codex's combined stdout+stderr
                # stream grew since last poll. This catches the case
                # where codex is THINKING (emitting reasoning text /
                # tool-call traces) but hasn't yet produced a file
                # edit — that's still real progress, not a stall.
                try:
                    cur_stream_bytes = stdout_fh.tell() + stderr_fh.tell()
                except Exception:
                    cur_stream_bytes = last_stream_bytes
                if cur_stream_bytes > last_stream_bytes:
                    last_progress_time = now
                    last_progress_kind = "stream"
                    last_stream_bytes = cur_stream_bytes

                stale_for = now - last_progress_time

                if progress_callback:
                    progress_callback(elapsed, stale_for, last_progress_kind,
                                       cur_stream_bytes)

                if stale_enabled and stale_for >= stale_after_sec:
                    stop_reason = "stalled"
                    break
                if elapsed >= timeout_sec:
                    stop_reason = "timeout"
                    break

            if stop_reason in ("stalled", "timeout"):
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
                   help=f"Hard backstop timeout for codex exec (default "
                        f"{DEFAULT_CODEX_TIMEOUT}s = 15 min)")
    p.add_argument("--stale-after-sec", type=int, default=240,
                   help="Kill codex early if no file in the worktree has "
                        "been touched within this window (default 240s = "
                        "4 min). This catches HARD physics problems where "
                        "codex stops making edits and is just thinking; it "
                        "lets us bail out faster than the hard backstop. "
                        "Set to a value >= --codex-timeout-sec to disable.")
    p.add_argument("--poll-interval-sec", type=int, default=30,
                   help="How often to check codex's progress (default 30s).")
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help=f"Codex model (default {DEFAULT_MODEL})")
    p.add_argument("--reasoning", default=DEFAULT_REASONING,
                   help=f"Codex reasoning effort (default {DEFAULT_REASONING})")
    p.add_argument("--category",
                   choices=CATEGORIES, default=None,
                   help="Restrict to one category")
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

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex[:8]
    run_log = LOG_DIR / f"loop-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{run_id}.jsonl"
    print(f"Loop run log: {run_log}")
    print(f"Codex model: {args.model}  reasoning: {args.reasoning}  "
          f"timeout: {args.codex_timeout_sec}s  stale_after: "
          f"{args.stale_after_sec}s  poll: {args.poll_interval_sec}s")

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
                if attempts.get(r["claim_id"], {}).get("outcome")
                not in ("pr_opened", "in_progress")
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
            print(f"  [{r['category']:<15s}] desc={r['descendants']:4d}  {r['claim_id']}")
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
            def _progress(elapsed_, stale_, last_kind, stream_bytes):
                # Live status to stdout so the operator can see progress
                # without having to tail the codex stderr. last_kind is
                # "init" / "mtime" / "stream" — telling them whether codex
                # is editing files or just thinking.
                print(f"    [progress] elapsed={elapsed_:5.0f}s  "
                      f"stalled_for={stale_:5.0f}s  "
                      f"last={last_kind}  bytes={stream_bytes}  "
                      f"(stale_kill@{args.stale_after_sec}s, hard@{args.codex_timeout_sec}s)",
                      flush=True)

            ok, stdout, stderr, elapsed, stop_reason = run_codex(
                r["prompt_body"], worktree,
                args.codex_timeout_sec, args.model, args.reasoning,
                run_log,
                stale_after_sec=args.stale_after_sec,
                poll_interval_sec=args.poll_interval_sec,
                progress_callback=_progress,
            )
            outcome["elapsed_sec"] = round(elapsed, 1)
            outcome["codex_returncode_ok"] = ok
            outcome["codex_stop_reason"] = stop_reason
            outcome["codex_stdout_tail"] = (stdout or "")[-1000:]
            outcome["codex_stderr_tail"] = (stderr or "")[-500:]

            # Decide whether this attempt produced anything worth promoting
            # to a PR. Order: structural codex failures first (no edits to
            # promote), then check the worktree.
            promote_edits = False
            if stop_reason == "error":
                print(f"  RUN ERROR: {(stderr or '').strip()[:200]}")
                outcome["outcome"] = "run_error"
                errored += 1
            elif stop_reason == "ok" and not ok:
                print(f"  codex exec failed (rc!=0): {(stderr or '').strip()[:200]}")
                outcome["outcome"] = "codex_failed"
                errored += 1
            else:
                # stop_reason in {ok, timeout, stalled} — codex either
                # finished or was killed early. Any of these can still
                # have produced useful partial edits.
                worktree_has_changes = has_changes(worktree)
                if stop_reason == "stalled" and not worktree_has_changes:
                    print(f"  STALLED with no edits after {elapsed:.0f}s — "
                          f"likely a HARD physics problem")
                    outcome["outcome"] = "stalled_no_edits"
                    punted += 1
                elif stop_reason == "timeout" and not worktree_has_changes:
                    print(f"  HARD TIMEOUT with no edits after {elapsed:.0f}s")
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
                tag = {"ok": "edits made", "stalled": "STALLED but partial edits",
                       "timeout": "HARD TIMEOUT but partial edits"}[stop_reason]
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
