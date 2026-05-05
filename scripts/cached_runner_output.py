#!/usr/bin/env python3
"""Cache-first runner output for analysis.

Use this instead of `python3 scripts/<runner>.py` when an analysis task needs
runner stdout. It prints the SHA-pinned cache when fresh; if the cache is
missing or stale, it executes the runner once, writes
`logs/runner-cache/<runner-stem>.txt`, and prints the resulting cache.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import runner_cache as rc

REPO_ROOT = Path(__file__).resolve().parent.parent


def repo_relative_runner(raw: str) -> str:
    p = Path(raw)
    if p.is_absolute():
        try:
            p = p.resolve().relative_to(REPO_ROOT)
        except ValueError as exc:
            raise SystemExit(f"runner must live inside repo: {raw}") from exc
    if not p.parts or p.parts[0] != "scripts":
        raise SystemExit(f"runner must be under scripts/: {raw}")
    if p.suffix != ".py":
        raise SystemExit(f"runner must be a Python file: {raw}")
    if not (REPO_ROOT / p).exists():
        raise SystemExit(f"runner missing on disk: {p.as_posix()}")
    return p.as_posix()


def print_cache_text(cache_text: str, tail_chars: int | None) -> None:
    if tail_chars is not None and tail_chars > 0 and len(cache_text) > tail_chars:
        cache_text = cache_text[-tail_chars:]
    sys.stdout.write(cache_text)
    if cache_text and not cache_text.endswith("\n"):
        sys.stdout.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print SHA-pinned runner output, refreshing the cache only when needed.",
    )
    parser.add_argument("runner", help="Runner path under scripts/, e.g. scripts/foo.py.")
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Re-run the runner even if its cache is already fresh.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Do not execute the runner; exit 1 if the cache is not fresh.",
    )
    parser.add_argument(
        "--timeout-sec",
        type=int,
        default=None,
        help="Override the runner's declared/cache-policy timeout for this refresh.",
    )
    parser.add_argument(
        "--tail-chars",
        type=int,
        default=None,
        help="Print only the last N characters of the cache text.",
    )
    args = parser.parse_args()

    runner = repo_relative_runner(args.runner)
    status = rc.cache_status(runner)
    cache_path, _header, cache_text = rc.load_cache(runner)

    if status == "fresh" and not args.refresh:
        if args.check_only:
            print(f"fresh {cache_path.relative_to(REPO_ROOT)}")
            return 0
        if cache_text is None:
            raise SystemExit(f"fresh cache could not be read: {cache_path}")
        print_cache_text(cache_text, args.tail_chars)
        return 0

    if args.check_only:
        print(f"{status} {cache_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    timeout_sec = args.timeout_sec or rc.runner_timeout_for(runner)
    print(
        f"[cache refresh] {runner} ({status}; timeout_sec={timeout_sec})",
        file=sys.stderr,
    )
    result = rc.execute_runner(runner, timeout_sec=timeout_sec)
    cache_path = rc.write_cache(runner, result)
    cache_text = cache_path.read_text(encoding="utf-8", errors="replace")
    print_cache_text(cache_text, args.tail_chars)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
