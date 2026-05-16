#!/usr/bin/env python3
"""Refresh the SHA-pinned runner output cache (`logs/runner-cache/`).

The audit lane stores one canonical cache file per runner at:

    logs/runner-cache/<runner-stem>.txt

The cache header pins each cache to the runner's content SHA-256. A cache
is fresh iff `runner_sha256` in the header equals the runner's current
SHA-256. This script ensures that every runner referenced from the audit
queue (or the full ledger) has a fresh cache, executing only the runners
whose caches are missing or stale.

Modes:

  precompute_audit_runners.py
      Refresh stale caches for runners in the queue.

  precompute_audit_runners.py --all
      Refresh stale caches for runners in the full ledger, not just queue.

  precompute_audit_runners.py --staged-only
      Refresh stale caches only for runners that are git-staged (for
      pre-commit hook use).

  precompute_audit_runners.py --pr-diff origin/main
      Cover only runners changed in this branch vs <base-ref>. PR-scoped
      analog of --staged-only; intended for the audit-lane PR CI check
      so unrelated PRs don't fail on pre-existing main-branch drift.

  precompute_audit_runners.py --check-only
      Do not execute anything; exit 1 with a list of stale caches if any
      exist. Used by CI gate and `--staged-only --check-only` pre-commit.

  precompute_audit_runners.py --runners scripts/foo.py,scripts/bar.py
      Refresh only the listed runners (comma-separated).

  precompute_audit_runners.py --force
      Re-run even fresh caches.

  precompute_audit_runners.py --cleanup-orphans
      Delete cache files whose runner no longer exists on disk.

Direct-to-main commit/push behavior is preserved for the bulk seeding
case (--push-mode=batch, default). Pre-commit / CI invocations use
--push-mode=none implicitly via --check-only.

The cache file format is documented in `scripts/runner_cache.py`.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import runner_cache as rc

REPO_ROOT = rc.REPO_ROOT
LEDGER_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
QUEUE_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_queue.json"
CACHE_DIR = rc.CACHE_DIR

# Timeout resolution lives in scripts/runner_cache.runner_timeout_for.
# It honors `AUDIT_TIMEOUT_SEC = N` declared at the top of the runner,
# falling back to a small legacy substring map and finally 120s. This
# script just calls into it.

def runner_timeout_for(runner_path: str) -> int:
    return rc.runner_timeout_for(runner_path)


def collect_runners_from_queue() -> list[str]:
    q = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    seen: dict[str, None] = {}
    for r in q.get("queue", []):
        rp = r.get("runner_path")
        if rp:
            seen.setdefault(rp, None)
    return list(seen.keys())


def collect_runners_from_ledger() -> list[str]:
    led = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    seen: dict[str, None] = {}
    for cid, r in led.get("rows", {}).items():
        rp = r.get("runner_path")
        if rp:
            seen.setdefault(rp, None)
    return list(seen.keys())


def collect_runners_from_staged() -> list[str]:
    """Return staged python files under scripts/ that are referenced as a
    primary runner by any ledger row. Skips staged files that aren't
    actually runners (e.g. scripts/codex_audit_runner.py, helpers).
    """
    res = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    )
    staged = [s for s in res.stdout.split("\n") if s.startswith("scripts/") and s.endswith(".py")]
    if not staged:
        return []
    known_runners = set(collect_runners_from_ledger())
    return [p for p in staged if p in known_runners]


# Helpers that, if changed, can invalidate every cache header at once.
# runner_cache.py owns the cache file format and the runner SHA-256
# computation — a change there can make every existing cache header
# semantically wrong. precompute_audit_runners.py is intentionally NOT
# in this set: it's an orchestrator, and changes to enumeration or
# dispatch logic don't invalidate the cache files themselves.
_CACHE_INVALIDATORS = {
    "scripts/runner_cache.py",
}


def collect_runners_from_pr_diff(base_ref: str) -> list[str]:
    """Return runners changed in this branch vs <base_ref>.

    Uses three-dot diff so we compare against the merge-base — intervening
    commits on the base branch don't pollute the diff. Filters changed
    scripts/*.py files down to those actually registered as runners in
    the ledger (matches `collect_runners_from_staged` semantics; helpers
    like runner_cache.py / precompute itself are excluded). If a
    cache-invalidator helper changed, escalates to the full ledger
    because every cache header is potentially stale.
    """
    res = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR",
         f"{base_ref}...HEAD"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    )
    if res.returncode != 0:
        print(
            f"ERROR: git diff against {base_ref!r} failed; cannot safely "
            "scope PR runner-cache checks.",
            file=sys.stderr,
        )
        if res.stderr.strip():
            print(res.stderr.strip(), file=sys.stderr)
        sys.exit(2)
    changed = [s for s in res.stdout.split("\n")
               if s.startswith("scripts/") and s.endswith(".py")]
    if any(c in _CACHE_INVALIDATORS for c in changed):
        return collect_runners_from_ledger()
    if not changed:
        return []
    known_runners = set(collect_runners_from_ledger())
    return [p for p in changed if p in known_runners]


# --- git helpers for direct-to-main commits ---

def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT, capture_output=True, text=True, check=check,
    )


def assert_main_and_clean_for_logs() -> str | None:
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if branch != "main":
        return f"not on main (currently on {branch!r})"
    porcelain = git("status", "--porcelain").stdout
    other_dirty = []
    for line in porcelain.splitlines():
        path = line[3:]
        if not path.startswith("logs/"):
            other_dirty.append(path)
    if other_dirty:
        return f"working tree dirty outside logs/: {other_dirty[:5]}"
    return None


def commit_and_push_logs(message: str, paths: list[Path],
                         max_attempts: int = 3) -> tuple[bool, str]:
    if not paths:
        return True, "no logs to commit"
    rel = [str(p.relative_to(REPO_ROOT)) for p in paths]
    add = git("add", "-f", *rel, check=False)
    if add.returncode != 0:
        return False, f"git add failed: {add.stderr.strip()[:200]}"
    diff = git("diff", "--cached", "--quiet", check=False)
    if diff.returncode == 0:
        return True, "no actual changes to commit"
    commit = git("commit", "-m", message, check=False)
    if commit.returncode != 0:
        return False, f"git commit failed: {(commit.stderr or commit.stdout).strip()[:200]}"
    for attempt in range(1, max_attempts + 1):
        push = git("push", "origin", "main", check=False)
        if push.returncode == 0:
            return True, f"pushed (attempt {attempt})"
        git("fetch", "origin", "main", check=False)
        rebase = git("rebase", "origin/main", check=False)
        if rebase.returncode != 0:
            git("rebase", "--abort", check=False)
            return False, f"push attempt {attempt} failed and rebase conflicted: {(push.stderr or push.stdout).strip()[:200]}"
    return False, f"push failed after {max_attempts} attempts"


def run_one(runner_path: str) -> dict:
    timeout_sec = runner_timeout_for(runner_path)
    result = rc.execute_runner(runner_path, timeout_sec=timeout_sec)
    if result["status"] == "missing":
        return result
    cache_p = rc.write_cache(runner_path, result)
    result["cache_path"] = str(cache_p.relative_to(REPO_ROOT))
    return result


def cleanup_orphans(known_runners: set[str], dry_run: bool = False) -> list[Path]:
    """Delete cache files whose runner is not in known_runners and whose
    runner file is missing from disk. Returns the list of paths deleted
    (or that would be deleted in dry_run)."""
    if not CACHE_DIR.is_dir():
        return []
    known_stems = {Path(r).stem for r in known_runners}
    orphans: list[Path] = []
    for p in CACHE_DIR.iterdir():
        if not p.is_file() or not p.name.endswith(".txt"):
            continue
        stem = p.stem
        if stem in known_stems:
            continue
        # Look for a runner with that stem on disk
        candidate = REPO_ROOT / "scripts" / f"{stem}.py"
        if candidate.exists():
            continue
        orphans.append(p)
        if not dry_run:
            p.unlink()
    return orphans


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--all", action="store_true",
                   help="Cover every runner referenced in the ledger, "
                        "not just the audit queue. Default: queue only.")
    p.add_argument("--staged-only", action="store_true",
                   help="Cover only runners that are git-staged (for "
                        "pre-commit hook use).")
    p.add_argument("--check-only", action="store_true",
                   help="Do not execute anything. Exit 1 if any cache is "
                        "stale, with a list of which runners need refresh. "
                        "Used by CI and --staged-only --check-only.")
    p.add_argument("--pr-diff", default="",
                   help="Cover only runners changed vs <base-ref> "
                        "(e.g. 'origin/main'). PR-scoped analog of "
                        "--staged-only; used by the audit-lane PR CI "
                        "check. Falls back to the full ledger if a "
                        "cache-invalidator helper changed.")
    p.add_argument("--runners", default="",
                   help="Comma-separated runner paths to refresh "
                        "(overrides queue/ledger/staged collection).")
    p.add_argument("--force", action="store_true",
                   help="Re-run even fresh caches.")
    p.add_argument("--cleanup-orphans", action="store_true",
                   help="Delete cache files for runners that no longer exist.")
    p.add_argument("--cleanup-orphans-dry-run", action="store_true",
                   help="Print orphan caches that would be deleted, do not delete.")
    p.add_argument("--concurrency", type=int, default=8,
                   help="Number of runners to execute in parallel.")
    p.add_argument("--push-mode",
                   choices=["batch", "none"], default="batch",
                   help="When to commit and push refreshed caches to main: "
                        "'batch' (default) or 'none'. Implicitly 'none' "
                        "with --check-only or --staged-only.")
    p.add_argument("--allow-non-main", action="store_true",
                   help="Permit running from a branch other than main.")
    p.add_argument("--commit-batch-size", type=int, default=200,
                   help="Maximum cache files per commit (default 200).")
    args = p.parse_args()

    # --check-only, --staged-only, and --pr-diff never push: the first
    # is read-only, the latter two run from a non-main branch.
    if args.check_only or args.staged_only or args.pr_diff:
        args.push_mode = "none"

    # Branch + cleanliness guard for direct-to-main pushes.
    if args.push_mode != "none":
        reason = assert_main_and_clean_for_logs()
        if reason and not args.allow_non_main:
            print(f"REFUSING to run with --push-mode={args.push_mode}: {reason}")
            return 2
        if reason and args.allow_non_main:
            print(f"WARNING: {reason}; --allow-non-main forces push-mode=none.")
            args.push_mode = "none"
        else:
            git("fetch", "origin", "main", check=False)
            rebase = git("rebase", "origin/main", check=False)
            if rebase.returncode != 0:
                git("rebase", "--abort", check=False)
                print("REFUSING: pre-run `git rebase origin/main` failed.")
                return 2

    # Determine target runner set.
    if args.runners.strip():
        runners = [r.strip() for r in args.runners.split(",") if r.strip()]
        source = "explicit --runners"
    elif args.staged_only:
        runners = collect_runners_from_staged()
        source = "git-staged"
    elif args.pr_diff:
        runners = collect_runners_from_pr_diff(args.pr_diff)
        source = f"pr-diff vs {args.pr_diff}"
    elif args.all:
        runners = collect_runners_from_ledger()
        source = "full ledger"
    else:
        runners = collect_runners_from_queue()
        source = "audit queue"
    runners = sorted(set(runners))
    print(f"Source: {source}.  Runners under consideration: {len(runners)}")

    # Optional orphan cleanup happens BEFORE staleness scan so we don't
    # report orphans as stale.
    if args.cleanup_orphans or args.cleanup_orphans_dry_run:
        all_known = set(collect_runners_from_ledger())
        orphans = cleanup_orphans(all_known, dry_run=args.cleanup_orphans_dry_run)
        verb = "Would delete" if args.cleanup_orphans_dry_run else "Deleted"
        print(f"\n{verb} {len(orphans)} orphan cache file(s):")
        for o in orphans[:20]:
            print(f"  {o.relative_to(REPO_ROOT)}")
        if len(orphans) > 20:
            print(f"  ... and {len(orphans) - 20} more")

    # Classify each runner: fresh / missing / sha_mismatch / corrupt.
    stale: list[tuple[str, str]] = []
    fresh: list[str] = []
    missing_on_disk: list[str] = []
    for rp in runners:
        if not (REPO_ROOT / rp).exists():
            missing_on_disk.append(rp)
            continue
        s = rc.cache_status(rp)
        if s == "fresh" and not args.force:
            fresh.append(rp)
        else:
            stale.append((rp, s if s != "fresh" else "force"))

    print(f"  fresh:           {len(fresh)}")
    print(f"  stale to refresh:{len(stale)}")
    print(f"  missing on disk: {len(missing_on_disk)}")

    if args.check_only:
        if stale:
            print("\nStale caches detected. The following runners need refresh:")
            for rp, reason in stale[:50]:
                print(f"  [{reason:13s}] {rp}")
            if len(stale) > 50:
                print(f"  ... and {len(stale) - 50} more")
            print("\nRun `python3 scripts/precompute_audit_runners.py "
                  "--runners <comma-sep-paths>` to refresh, or simply")
            print("`python3 scripts/precompute_audit_runners.py` for the queue, "
                  "or `--all` for the full ledger.")
            return 1
        print("\nAll relevant caches are fresh.")
        return 0

    if not stale:
        print("\nNothing to do — all relevant caches are fresh.")
        return 0

    print(f"\nExecuting {len(stale)} runner(s) with concurrency={args.concurrency}...")
    print(f"Live logs available under {rc.LIVE_LOG_DIR.relative_to(REPO_ROOT)}/<stem>.txt"
          " — `tail -F` any one to watch a specific runner mid-execution.")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    rc.LIVE_LOG_DIR.mkdir(parents=True, exist_ok=True)

    counts = {"ok": 0, "nonzero_exit": 0, "timeout": 0, "error": 0, "missing": 0}
    completed = 0
    written: list[Path] = []
    t0 = time.time()
    # Track when each runner started so the heartbeat thread can emit
    # "still alive" lines for runners that have been running > 60s.
    started_at: dict[str, float] = {}
    started_lock = __import__("threading").Lock()
    stop_heartbeat = __import__("threading").Event()

    def heartbeat_loop():
        # Print a per-runner heartbeat every 30s for in-progress runners
        # whose elapsed time has crossed 60s. Helps the operator see
        # which runners are still working vs which might be stuck.
        while not stop_heartbeat.wait(30):
            now = time.time()
            with started_lock:
                long_running = [
                    (rp, now - t)
                    for rp, t in started_at.items()
                    if now - t > 60
                ]
            if long_running:
                print(f"  [heartbeat] {len(long_running)} runner(s) > 60s in flight:")
                for rp, elapsed_sec in sorted(long_running, key=lambda x: -x[1])[:8]:
                    live = rc.live_log_path_for(rp)
                    size = live.stat().st_size if live.exists() else 0
                    print(f"    {elapsed_sec:6.0f}s  {size:>8d}b  {Path(rp).name}")

    hb_thread = __import__("threading").Thread(target=heartbeat_loop, daemon=True)
    hb_thread.start()

    def run_one_tracked(runner_path: str) -> dict:
        with started_lock:
            started_at[runner_path] = time.time()
        try:
            return run_one(runner_path)
        finally:
            with started_lock:
                started_at.pop(runner_path, None)

    try:
        with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
            futures = {ex.submit(run_one_tracked, rp): rp for rp, _ in stale}
            for fut in as_completed(futures):
                rp = futures[fut]
                try:
                    result = fut.result()
                except Exception as exc:
                    result = {"runner": rp, "status": "error",
                              "elapsed_sec": 0.0, "exit_code": None,
                              "cache_path": None}
                    print(f"  ! orchestrator error on {rp}: {exc!r}")
                counts[result["status"]] = counts.get(result["status"], 0) + 1
                completed += 1
                elapsed = result.get("elapsed_sec") or 0.0
                tag = {"ok": "OK", "nonzero_exit": "EXIT!=0", "timeout": "TIMEOUT",
                       "error": "ERROR", "missing": "MISSING"}.get(result["status"], "?")
                print(f"  [{completed:3d}/{len(stale)}] {tag:8s} {elapsed:6.1f}s  "
                      f"{Path(rp).name}")
                cache_rel = result.get("cache_path")
                if cache_rel:
                    written.append(REPO_ROOT / cache_rel)
    finally:
        stop_heartbeat.set()

    total_elapsed = time.time() - t0
    print(f"\nDone in {total_elapsed:.1f}s.")
    for k in ("ok", "nonzero_exit", "timeout", "error", "missing"):
        print(f"  {k:14s} {counts.get(k, 0)}")
    print(f"\nCache layout: {CACHE_DIR.relative_to(REPO_ROOT)}/<runner-stem>.txt")

    # Push refreshed caches to main if asked. The cache files are
    # version-controlled now — landing them is part of the runner change
    # that triggered the refresh.
    if args.push_mode == "batch" and written:
        utc_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        n_batches = (len(written) + args.commit_batch_size - 1) // args.commit_batch_size
        push_failed = 0
        for batch_idx in range(n_batches):
            start = batch_idx * args.commit_batch_size
            end = start + args.commit_batch_size
            batch_paths = written[start:end]
            msg = (
                f"audit: refresh runner cache batch {batch_idx + 1}/{n_batches} "
                f"({len(batch_paths)} runners) {utc_stamp} [skip ci]"
            )
            ok, push_msg = commit_and_push_logs(msg, batch_paths)
            if ok:
                print(f"  batch {batch_idx + 1}/{n_batches}: {push_msg}")
            else:
                push_failed += 1
                print(f"  batch {batch_idx + 1}/{n_batches} FAIL: {push_msg}")
        if push_failed:
            return 1
    return 0 if counts.get("error", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
