"""SHA-pinned runner output cache for the audit lane.

Each runner under `scripts/` has one canonical cache file at:

    logs/runner-cache/<runner-stem>.txt

The header pins the cache to the runner's content SHA-256. The cache is
considered fresh iff `runner_sha256` in the header matches the current
SHA-256 of the runner file. Pre-commit and CI gates enforce that no
runner change lands without an updated cache.

Format (no timestamps anywhere — gate-clean):

    ===== runner cache v1 =====
    runner: scripts/<name>.py
    runner_sha256: <hex>
    timeout_sec: 120
    exit_code: 0
    elapsed_sec: 12.34
    status: ok
    ----- stdout -----
    <stdout, capped at 200KB tail>
    ----- stderr -----
    <stderr, capped at 50KB tail>

The audit runner reads from this cache; pre-commit refreshes any cache
whose runner has been modified; CI fails any PR whose caches drift from
their runners' SHAs.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = REPO_ROOT / "logs" / "runner-cache"
LIVE_LOG_DIR = CACHE_DIR / ".in-progress"

CACHE_HEADER_PREFIX = "===== runner cache v1 ====="
SHA_RE = re.compile(r"^runner_sha256:\s*([0-9a-f]{64})\s*$", re.MULTILINE)
RUNNER_PATH_RE = re.compile(r"^runner:\s*(.+)$", re.MULTILINE)
STATUS_RE = re.compile(r"^status:\s*(\S+)\s*$", re.MULTILINE)
EXIT_CODE_RE = re.compile(r"^exit_code:\s*(\S+)\s*$", re.MULTILINE)

# Per-runner declared timeout. Authors who know their runner is slow
# add `AUDIT_TIMEOUT_SEC = N` near the top of the runner module. The
# precompute orchestrator and the audit runner both honor this value
# in preference to the legacy substring overrides and the default.
TIMEOUT_HEADER_RE = re.compile(
    r"^AUDIT_TIMEOUT_SEC\s*=\s*(\d+)\s*(?:#.*)?$",
    re.MULTILINE,
)
TIMEOUT_DEFAULT_SEC = 120

# Legacy substring map. Kept as a fallback only for runners that have
# not yet declared `AUDIT_TIMEOUT_SEC` in their source. New runners
# should declare directly; over time this list shrinks to zero.
TIMEOUT_LEGACY_OVERRIDES: list[tuple[str, int]] = [
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


def declared_timeout_for(runner_path: str | Path) -> int | None:
    """Return the runner-declared `AUDIT_TIMEOUT_SEC`, else None.

    The declaration is a top-level Python assignment somewhere in the
    file body (not inside a function). Parsing is regex-based for speed
    — the runner does not need to be importable for us to read its
    declared timeout.
    """
    p = runner_path if isinstance(runner_path, Path) and runner_path.is_absolute() \
        else REPO_ROOT / runner_path
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = TIMEOUT_HEADER_RE.search(text)
    if not m:
        return None
    try:
        val = int(m.group(1))
    except ValueError:
        return None
    return val if val > 0 else None


def runner_timeout_for(runner_path: str | Path,
                       default_sec: int = TIMEOUT_DEFAULT_SEC) -> int:
    """Resolve effective timeout for a runner.

    Priority:
      1. `AUDIT_TIMEOUT_SEC = N` declared at module top of the runner
      2. Legacy substring overrides (`frontier_*` patterns)
      3. `default_sec` (default 120)
    """
    declared = declared_timeout_for(runner_path)
    if declared is not None:
        return declared
    bn = Path(runner_path).name
    for needle, override in TIMEOUT_LEGACY_OVERRIDES:
        if needle in bn:
            return override
    return default_sec


def runner_sha256(runner_path: str | Path) -> str | None:
    """SHA-256 of the runner's source bytes; None if missing on disk."""
    p = runner_path if isinstance(runner_path, Path) and runner_path.is_absolute() \
        else REPO_ROOT / runner_path
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return None


def cache_path_for(runner_path: str | Path) -> Path:
    """Canonical cache path for a runner. One file per runner stem."""
    return CACHE_DIR / f"{Path(runner_path).stem}.txt"


def parse_cache_header(text: str) -> dict | None:
    """Parse a cache file body. Returns dict with keys
    runner_path, runner_sha256, status, exit_code (str), or None on bad header.
    """
    if not text.startswith(CACHE_HEADER_PREFIX):
        return None
    head = text.split("----- stdout -----", 1)[0]
    sha_m = SHA_RE.search(head)
    rp_m = RUNNER_PATH_RE.search(head)
    if not (sha_m and rp_m):
        return None
    return {
        "runner_path": rp_m.group(1).strip(),
        "runner_sha256": sha_m.group(1),
        "status": (STATUS_RE.search(head).group(1) if STATUS_RE.search(head) else None),
        "exit_code": (EXIT_CODE_RE.search(head).group(1) if EXIT_CODE_RE.search(head) else None),
    }


def load_cache(runner_path: str | Path) -> tuple[Path, dict | None, str | None]:
    """Return (cache_path, parsed_header_or_None, body_text_or_None)."""
    p = cache_path_for(runner_path)
    if not p.exists():
        return p, None, None
    try:
        body = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return p, None, None
    return p, parse_cache_header(body), body


def cache_status(runner_path: str | Path) -> str:
    """Return one of: 'fresh' | 'missing' | 'corrupt' | 'sha_mismatch'.

    'fresh' means cache exists with header SHA matching current runner SHA.
    Caller is responsible for handling the missing-runner case (the runner
    file itself absent from disk — those runners shouldn't have caches).
    """
    p = REPO_ROOT / runner_path
    if not p.exists():
        return "fresh"  # nothing to check; runner is gone, ignore
    cache_p, header, _ = load_cache(runner_path)
    if not cache_p.exists():
        return "missing"
    if not header:
        return "corrupt"
    cur = runner_sha256(runner_path)
    if cur is None or header.get("runner_sha256") != cur:
        return "sha_mismatch"
    return "fresh"


def stale_runners(runner_paths: Iterable[str]) -> list[tuple[str, str]]:
    """Return [(runner_path, reason)] for caches that need refreshing.
    Reason is one of 'missing' | 'corrupt' | 'sha_mismatch'.
    Runners absent from disk are excluded — orphan cache cleanup is a
    separate concern.
    """
    out: list[tuple[str, str]] = []
    for rp in runner_paths:
        s = cache_status(rp)
        if s != "fresh":
            out.append((rp, s))
    return out


def live_log_path_for(runner_path: str | Path) -> Path:
    """Path of the in-progress live log for a runner. Tail this during a
    precompute pass to watch a runner make progress mid-execution.
    """
    return LIVE_LOG_DIR / f"{Path(runner_path).stem}.txt"


def execute_runner(runner_path: str, timeout_sec: int) -> dict:
    """Run a single runner; return result dict with stdout/stderr/status.

    During execution the runner's stdout+stderr are streamed to a live
    log file at `logs/runner-cache/.in-progress/<stem>.txt` (gitignored)
    so an operator can `tail -f` any in-progress runner. The live log is
    cleaned up when the canonical cache file is written.
    """
    p = REPO_ROOT / runner_path
    if not p.exists():
        return {"runner": runner_path, "status": "missing", "exit_code": None,
                "stdout": "", "stderr": "", "elapsed_sec": 0.0,
                "timeout_sec": timeout_sec}
    LIVE_LOG_DIR.mkdir(parents=True, exist_ok=True)
    live_log = live_log_path_for(runner_path)
    t0 = time.time()
    status = "ok"
    exit_code: int | None = None

    # Write a header to the live log so a tail -F shows context.
    live_log.write_text(
        f"# in-progress live log for {runner_path}\n"
        f"# timeout_sec: {timeout_sec}\n"
        f"# started: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
        f"# (this file is replaced by the canonical cache when the run completes)\n"
        f"\n",
        encoding="utf-8",
    )

    proc = None
    try:
        # Open the live log in append mode after the header so we can
        # see streaming output via tail -F. stderr is merged into stdout
        # to preserve interleaving.
        with live_log.open("a", encoding="utf-8") as live_fh:
            proc = subprocess.Popen(
                [sys.executable, "-u", str(p)],
                cwd=REPO_ROOT,
                stdout=live_fh,
                stderr=subprocess.STDOUT,
                env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "scripts")},
            )
            try:
                exit_code = proc.wait(timeout=timeout_sec)
                if exit_code != 0:
                    status = "nonzero_exit"
            except subprocess.TimeoutExpired:
                status = "timeout"
                proc.kill()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass
                exit_code = proc.returncode
    except Exception as exc:
        status = "error"
        try:
            with live_log.open("a", encoding="utf-8") as live_fh:
                live_fh.write(f"\n[orchestrator caught: {exc!r}]\n")
        except OSError:
            pass

    elapsed = time.time() - t0
    # Read the live log tail back as the result body. The merged
    # stdout+stderr stream is what the audit prompt needs.
    try:
        body = live_log.read_text(encoding="utf-8", errors="replace")
    except OSError:
        body = ""
    # Strip our header (first 4 lines + blank) so the cache contains
    # only the runner's actual output.
    lines = body.split("\n", 5)
    stdout = lines[5] if len(lines) > 5 else ""

    return {
        "runner": runner_path,
        "status": status,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": "",  # merged into stdout via STDOUT redirect
        "elapsed_sec": elapsed,
        "timeout_sec": timeout_sec,
        "live_log": str(live_log),
    }


def write_cache(runner_path: str, result: dict, runner_sha: str | None = None) -> Path:
    """Write the result of execute_runner to the canonical cache path.
    Pure function of runner SHA + execution result — no timestamps."""
    if runner_sha is None:
        runner_sha = runner_sha256(runner_path)
    if runner_sha is None:
        raise FileNotFoundError(f"runner missing on disk: {runner_path}")
    cache_p = cache_path_for(runner_path)
    cache_p.parent.mkdir(parents=True, exist_ok=True)

    stdout = result.get("stdout") or ""
    stderr = result.get("stderr") or ""
    stdout_tail = stdout[-200_000:]
    stderr_tail = stderr[-50_000:]
    elapsed = result.get("elapsed_sec") or 0.0
    body = (
        f"{CACHE_HEADER_PREFIX}\n"
        f"runner: {runner_path}\n"
        f"runner_sha256: {runner_sha}\n"
        f"timeout_sec: {result.get('timeout_sec')}\n"
        f"exit_code: {result.get('exit_code')}\n"
        f"elapsed_sec: {elapsed:.2f}\n"
        f"status: {result.get('status')}\n"
        f"----- stdout -----\n"
        f"{stdout_tail}\n"
        f"----- stderr -----\n"
        f"{stderr_tail}\n"
    )
    cache_p.write_text(body, encoding="utf-8")
    # Now that the canonical cache has the result, the in-progress live
    # log can go away. Best-effort cleanup; nothing depends on it.
    live = live_log_path_for(runner_path)
    try:
        if live.exists():
            live.unlink()
    except OSError:
        pass
    return cache_p


def cache_excerpt_for_audit(runner_path: str | Path,
                            tail_chars: int = 6000) -> str | None:
    """Return cache content suitable for the audit prompt's Section 3.
    Returns None if no cache exists or if the cache is stale.
    """
    p, header, body = load_cache(runner_path)
    if not (header and body):
        return None
    cur_sha = runner_sha256(runner_path)
    if cur_sha is None or header.get("runner_sha256") != cur_sha:
        return None
    excerpt = body[-tail_chars:] if len(body) > tail_chars else body
    return f"[runner cache hit: {p.name}, sha {header['runner_sha256'][:12]}]\n{excerpt}"
