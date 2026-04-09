#!/usr/bin/env python3
"""Freeze one shared-geometry exact-comparator batch to a log file.

This is a thin logging-safe wrapper around
`wave_static_matrixfree_shared_geometry_compare.py`.

Use this when you want a retained exact-comparator run without an ad hoc
`tee` pipeline. The default log path is:

  logs/<today>-wave-static-matrixfree-shared-geometry-compare.txt

The wrapper forwards any extra args to the underlying probe, so the run
command stays simple and the frozen log is easy to replay.
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path


def _default_log_path() -> Path:
    return Path("logs") / f"{dt.date.today().isoformat()}-wave-static-matrixfree-shared-geometry-compare.txt"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--log",
        type=Path,
        default=None,
        help="Log file path. Default: logs/<today>-wave-static-matrixfree-shared-geometry-compare.txt",
    )
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Optional extra args forwarded to wave_static_matrixfree_shared_geometry_compare.py.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    log_path = args.log or _default_log_path()
    if not log_path.is_absolute():
        log_path = repo_root / log_path
    log_path.parent.mkdir(parents=True, exist_ok=True)

    forwarded = args.args
    if forwarded and forwarded[0] == "--":
        forwarded = forwarded[1:]

    cmd = [
        sys.executable,
        "-u",
        str(repo_root / "scripts" / "wave_static_matrixfree_shared_geometry_compare.py"),
        *forwarded,
    ]

    with log_path.open("w", encoding="utf-8") as fh:
        proc = subprocess.run(
            cmd,
            cwd=repo_root,
            stdout=fh,
            stderr=subprocess.STDOUT,
            check=False,
            text=True,
        )

    print(f"log_path={log_path}")
    print(f"exit_code={proc.returncode}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
