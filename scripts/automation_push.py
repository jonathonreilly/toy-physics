#!/usr/bin/env python3
"""Retrying git push helper for flaky automation environments."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse


DNS_PATTERNS = (
    "Could not resolve host",
    "Name or service not known",
    "Temporary failure in name resolution",
)

AUTH_PATTERNS = (
    "Authentication failed",
    "Permission denied",
    "Repository not found",
    "could not read Username",
)

NONFASTFORWARD_PATTERNS = (
    "non-fast-forward",
    "[rejected]",
    "fetch first",
)


def run_git(workdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=workdir,
        capture_output=True,
        text=True,
        check=False,
    )


def current_branch(workdir: Path) -> str:
    result = run_git(workdir, "branch", "--show-current")
    branch = result.stdout.strip()
    return branch or "main"


def remote_host(workdir: Path) -> str:
    result = run_git(workdir, "remote", "get-url", "origin")
    url = result.stdout.strip()
    if "://" in url:
        return urlparse(url).hostname or "github.com"
    if "@" in url and ":" in url:
        return url.split("@", 1)[1].split(":", 1)[0]
    return "github.com"


def ahead_behind_counts(workdir: Path, branch: str) -> tuple[int, int] | None:
    verify = run_git(workdir, "rev-parse", "--verify", f"origin/{branch}")
    if verify.returncode != 0:
        return None
    result = run_git(workdir, "rev-list", "--left-right", "--count", f"origin/{branch}...{branch}")
    if result.returncode != 0:
        return None
    left, right = result.stdout.strip().split()
    return int(left), int(right)


def classify_failure(stderr: str) -> str:
    for pattern in DNS_PATTERNS:
        if pattern in stderr:
            return "dns_failure"
    for pattern in AUTH_PATTERNS:
        if pattern in stderr:
            return "auth_failure"
    for pattern in NONFASTFORWARD_PATTERNS:
        if pattern in stderr:
            return "non_fast_forward"
    if stderr.strip():
        return "push_failure"
    return "unknown_failure"


def emit(payload: dict[str, object]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return int(payload.get("exit_code", 0))


def push_if_ahead(workdir: Path, attempts: int, backoffs: list[int]) -> int:
    branch = current_branch(workdir)
    host = remote_host(workdir)
    counts = ahead_behind_counts(workdir, branch)
    ahead = counts[1] if counts else None
    behind = counts[0] if counts else None

    if ahead == 0:
        return emit(
            {
                "ahead": ahead,
                "behind": behind,
                "branch": branch,
                "host": host,
                "status": "nothing_to_push",
                "exit_code": 0,
            }
        )

    last_error = ""
    for attempt in range(1, attempts + 1):
        probe = run_git(workdir, "ls-remote", "origin", "HEAD")
        if probe.returncode != 0:
            last_error = probe.stderr.strip() or probe.stdout.strip() or f"ls-remote failed for {host}"
            failure_kind = classify_failure(last_error)
        else:
            push = run_git(workdir, "push", "origin", branch)
            if push.returncode == 0:
                final_counts = ahead_behind_counts(workdir, branch)
                return emit(
                    {
                        "ahead": final_counts[1] if final_counts else None,
                        "attempts_used": attempt,
                        "behind": final_counts[0] if final_counts else None,
                        "branch": branch,
                        "host": host,
                        "status": "pushed",
                        "exit_code": 0,
                    }
                )
            last_error = push.stderr.strip() or push.stdout.strip()
            failure_kind = classify_failure(last_error)

        if failure_kind == "unknown_failure" and "github.com" in last_error.lower():
            failure_kind = "dns_failure"

        if failure_kind in {"auth_failure", "non_fast_forward"}:
            return emit(
                {
                    "ahead": ahead,
                    "attempts_used": attempt,
                    "behind": behind,
                    "branch": branch,
                    "error": last_error,
                    "failure_kind": failure_kind,
                    "host": host,
                    "status": "failed",
                    "exit_code": 2,
                }
            )

        if attempt < attempts:
            time.sleep(backoffs[min(attempt - 1, len(backoffs) - 1)])

    return emit(
        {
            "ahead": ahead,
            "attempts_used": attempts,
            "behind": behind,
            "branch": branch,
            "error": last_error,
            "failure_kind": failure_kind,
            "host": host,
            "status": "failed",
            "exit_code": 1,
        }
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    push_parser = subparsers.add_parser("push-if-ahead")
    push_parser.add_argument("--workdir", default=".")
    push_parser.add_argument("--attempts", type=int, default=5)
    push_parser.add_argument("--backoff-seconds", default="2,5,15,30,60")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "push-if-ahead":
        backoffs = [int(part) for part in args.backoff_seconds.split(",") if part]
        if not backoffs:
            backoffs = [2, 5, 15, 30]
        return push_if_ahead(Path(args.workdir).resolve(), args.attempts, backoffs)
    return 1


if __name__ == "__main__":
    sys.exit(main())
