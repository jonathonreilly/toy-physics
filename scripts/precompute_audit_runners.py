#!/usr/bin/env python3
"""Pre-compute audit-runner outputs and cache them as `logs/` files.

The audit lane's `codex_audit_runner.py` prefers cached runner output
over re-executing — its `find_cached_runner_output` greps `logs/` for
`<runner-stem>*` and uses the most recent matching file. This script
populates that cache by running every primary-runner referenced from
the audit queue (or the full ledger) in parallel ONCE, with appropriate
per-runner timeouts.

After a pre-compute pass, the next codex audit batch is mostly cache
hits: codex sees runner stdout immediately without subprocess waits, and
the per-row audit-loop wall-clock collapses to the codex call itself.

Idempotent: skips any runner whose `logs/<stem>-precompute-*.txt` exists
within --max-age-hours (default 24h). Re-run safely.

Output format:
  logs/<runner-stem>-precompute-<utcZ>.txt

  ===== precompute audit runner =====
  runner: scripts/<name>.py
  command: python3 scripts/<name>.py
  timeout_sec: <N>
  started_at: <utc iso>
  ----- stdout -----
  <stdout>
  ----- stderr -----
  <stderr>
  ===== summary =====
  exit_code: <int>
  elapsed_sec: <float>
  status: ok | timeout | nonzero_exit | error

Usage:
  python3 scripts/precompute_audit_runners.py
  python3 scripts/precompute_audit_runners.py --all          # full ledger, not just queue
  python3 scripts/precompute_audit_runners.py --max-age-hours 6  # tighter cache
  python3 scripts/precompute_audit_runners.py --concurrency 8
  python3 scripts/precompute_audit_runners.py --dry-run     # list what would run
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
QUEUE_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_queue.json"
LOGS_DIR = REPO_ROOT / "logs"

# Per-runner timeout overrides for known-heavy compute lanes. Substring
# match against the runner basename. Keep in sync with the same map in
# scripts/codex_audit_runner.py — long timeouts here trade wall-clock for
# completeness on lanes that need it.
RUNNER_TIMEOUT_OVERRIDES: list[tuple[str, int]] = [
    ("frontier_alpha_s", 900),
    ("frontier_confinement", 900),
    ("frontier_gauge_vacuum_plaquette_perron", 900),
    ("frontier_gauge_vacuum_plaquette_reduction", 900),
    ("frontier_gauge_vacuum_plaquette_spectral", 900),
    ("frontier_gauge_vacuum_plaquette_susceptibility", 900),
    ("frontier_yt_uv_to_ir", 900),
    ("frontier_yt_p1_delta_r_master", 900),
    ("frontier_higgs_mass_full", 900),
    ("frontier_dm_neutrino_source_surface", 600),
    ("frontier_ckm_atlas", 600),
    ("frontier_self_consistent_field", 600),
    ("frontier_emergent_lorentz", 600),
]
DEFAULT_TIMEOUT_SEC = 120


def runner_timeout_for(runner_path: str) -> int:
    bn = Path(runner_path).name
    for needle, override in RUNNER_TIMEOUT_OVERRIDES:
        if needle in bn:
            return override
    return DEFAULT_TIMEOUT_SEC


def collect_runners_from_queue() -> list[str]:
    """Distinct runner_paths referenced by audit_queue.json rows."""
    q = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    seen: dict[str, None] = {}
    for r in q.get("queue", []):
        rp = r.get("runner_path")
        if rp:
            seen.setdefault(rp, None)
    return list(seen.keys())


def collect_runners_from_ledger() -> list[str]:
    """Distinct runner_paths referenced by any ledger row."""
    led = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    seen: dict[str, None] = {}
    for cid, r in led.get("rows", {}).items():
        rp = r.get("runner_path")
        if rp:
            seen.setdefault(rp, None)
    return list(seen.keys())


def runner_log_pattern(runner_path: str) -> str:
    return f"{Path(runner_path).stem}-precompute-*.txt"


def has_fresh_cached_log(runner_path: str, max_age_hours: float) -> Path | None:
    """Return the path to a fresh enough precompute log, else None."""
    stem = Path(runner_path).stem
    if not LOGS_DIR.is_dir():
        return None
    cutoff = time.time() - max_age_hours * 3600
    candidates = []
    try:
        for p in LOGS_DIR.iterdir():
            if not p.is_file():
                continue
            if p.name.startswith(f"{stem}-precompute-") and p.name.endswith(".txt"):
                if p.stat().st_mtime >= cutoff:
                    candidates.append(p)
    except OSError:
        return None
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def run_one(runner_path: str) -> dict:
    """Execute a single runner; write its output to a log file. Returns a
    summary dict for the orchestrator's progress report."""
    p = REPO_ROOT / runner_path
    if not p.exists():
        return {
            "runner": runner_path,
            "status": "missing",
            "elapsed_sec": 0.0,
            "log_path": None,
        }
    timeout_sec = runner_timeout_for(runner_path)
    utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = LOGS_DIR / f"{Path(runner_path).stem}-precompute-{utc}.txt"
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    started = datetime.now(timezone.utc).isoformat()
    t0 = time.time()
    status = "ok"
    exit_code: int | None = None
    stdout = ""
    stderr = ""
    try:
        res = subprocess.run(
            [sys.executable, str(p)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "scripts")},
        )
        exit_code = res.returncode
        stdout = res.stdout
        stderr = res.stderr
        if exit_code != 0:
            status = "nonzero_exit"
    except subprocess.TimeoutExpired as e:
        status = "timeout"
        # subprocess.TimeoutExpired captures partial output on Python 3.12+
        stdout = (e.stdout or b"").decode("utf-8", errors="replace") if isinstance(e.stdout, (bytes, bytearray)) else (e.stdout or "")
        stderr = (e.stderr or b"").decode("utf-8", errors="replace") if isinstance(e.stderr, (bytes, bytearray)) else (e.stderr or "")
    except Exception as exc:
        status = "error"
        stderr = f"[orchestrator caught: {exc!r}]"

    elapsed = time.time() - t0

    # Cap to keep log size sane; tail is most relevant.
    stdout_tail = stdout[-200_000:]
    stderr_tail = stderr[-50_000:]

    log_path.write_text(
        f"===== precompute audit runner =====\n"
        f"runner: {runner_path}\n"
        f"command: python3 {runner_path}\n"
        f"timeout_sec: {timeout_sec}\n"
        f"started_at: {started}\n"
        f"----- stdout -----\n"
        f"{stdout_tail}\n"
        f"----- stderr -----\n"
        f"{stderr_tail}\n"
        f"===== summary =====\n"
        f"exit_code: {exit_code}\n"
        f"elapsed_sec: {elapsed:.2f}\n"
        f"status: {status}\n",
        encoding="utf-8",
    )

    return {
        "runner": runner_path,
        "status": status,
        "exit_code": exit_code,
        "elapsed_sec": elapsed,
        "log_path": str(log_path.relative_to(REPO_ROOT)),
        "timeout_sec": timeout_sec,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--all", action="store_true",
                   help="Pre-compute every runner referenced in the ledger, "
                        "not just the audit queue. Default: queue only.")
    p.add_argument("--max-age-hours", type=float, default=24.0,
                   help="Skip runners whose precompute log is younger than this. "
                        "Default 24h. Use --max-age-hours 0 to force re-run.")
    p.add_argument("--concurrency", type=int, default=8,
                   help="Number of runners to execute in parallel (default 8).")
    p.add_argument("--dry-run", action="store_true",
                   help="List runners that would be executed; do not run them.")
    p.add_argument("--include", action="append", default=[],
                   help="Substring filter on runner basenames; only matching "
                        "runners are scheduled. Repeatable.")
    p.add_argument("--exclude", action="append", default=[],
                   help="Substring filter on runner basenames; matching runners "
                        "are skipped. Repeatable.")
    args = p.parse_args()

    runners = collect_runners_from_ledger() if args.all else collect_runners_from_queue()
    runners = sorted(set(runners))
    print(f"Discovered {len(runners)} distinct runner paths "
          f"({'ledger-wide' if args.all else 'queue-only'}).")

    if args.include:
        runners = [r for r in runners if any(s in r for s in args.include)]
        print(f"  After --include filter: {len(runners)}")
    if args.exclude:
        runners = [r for r in runners if not any(s in r for s in args.exclude)]
        print(f"  After --exclude filter: {len(runners)}")

    to_run: list[str] = []
    cached: list[tuple[str, Path]] = []
    missing: list[str] = []
    for rp in runners:
        if not (REPO_ROOT / rp).exists():
            missing.append(rp)
            continue
        cached_log = has_fresh_cached_log(rp, args.max_age_hours)
        if cached_log:
            cached.append((rp, cached_log))
        else:
            to_run.append(rp)

    print(f"Cached (fresh within {args.max_age_hours}h, skipping):  {len(cached)}")
    print(f"Missing on disk (cannot run):                 {len(missing)}")
    print(f"To run:                                       {len(to_run)}")

    if args.dry_run:
        print("\nDry-run; runners that WOULD be executed (first 30):")
        for rp in to_run[:30]:
            t = runner_timeout_for(rp)
            print(f"  timeout={t:4d}s  {rp}")
        if len(to_run) > 30:
            print(f"  ... and {len(to_run)-30} more")
        return 0

    if not to_run:
        print("\nNothing to do — all runners are cached or missing.")
        return 0

    print(f"\nExecuting with concurrency={args.concurrency}...")
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    counts = {"ok": 0, "nonzero_exit": 0, "timeout": 0, "error": 0, "missing": 0}
    completed = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = {ex.submit(run_one, rp): rp for rp in to_run}
        for fut in as_completed(futures):
            rp = futures[fut]
            try:
                result = fut.result()
            except Exception as exc:
                result = {"runner": rp, "status": "error",
                          "elapsed_sec": 0.0, "exit_code": None,
                          "log_path": None}
                print(f"  ! orchestrator error on {rp}: {exc!r}")
            counts[result["status"]] = counts.get(result["status"], 0) + 1
            completed += 1
            elapsed = result.get("elapsed_sec") or 0.0
            tag = {"ok": "OK", "nonzero_exit": "EXIT≠0", "timeout": "TIMEOUT",
                   "error": "ERROR", "missing": "MISSING"}.get(result["status"], "?")
            print(f"  [{completed:3d}/{len(to_run)}] {tag:7s} {elapsed:6.1f}s  "
                  f"{Path(rp).name}")

    total_elapsed = time.time() - t0
    print(f"\nDone in {total_elapsed:.1f}s.")
    for k in ("ok", "nonzero_exit", "timeout", "error", "missing"):
        print(f"  {k:14s} {counts.get(k, 0)}")
    print(f"\nCache populated under {LOGS_DIR.relative_to(REPO_ROOT)}/")
    print("Subsequent codex_audit_runner.py runs will use these as cache hits.")
    return 0 if counts.get("error", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
