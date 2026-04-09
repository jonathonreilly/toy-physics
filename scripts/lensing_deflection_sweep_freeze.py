#!/usr/bin/env python3
"""Freeze one lensing deflection sweep to a log file.

This is a thin logging-safe wrapper around `lensing_deflection_sweep.py`.
It captures stdout/stderr atomically, defaults the log path to
`logs/<today>-lensing-deflection-sweep.txt`, and forwards any extra args
directly to the underlying probe.
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
import tempfile
from pathlib import Path


def default_log_path(repo_root: Path) -> Path:
    today = dt.date.today().isoformat()
    return repo_root / "logs" / f"{today}-lensing-deflection-sweep.txt"


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--log",
        type=Path,
        default=default_log_path(repo_root),
        help="Log file path. Default: logs/<today>-lensing-deflection-sweep.txt",
    )
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Optional extra args forwarded to lensing_deflection_sweep.py.",
    )
    ns = parser.parse_args()

    forwarded = list(ns.args)
    if forwarded and forwarded[0] == "--":
        forwarded = forwarded[1:]

    target = repo_root / "scripts" / "lensing_deflection_sweep.py"
    cmd = [sys.executable, str(target), *forwarded]

    ns.log.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=str(ns.log.parent),
        prefix=ns.log.name + ".tmp.",
        delete=False,
    ) as tmp:
        proc = subprocess.run(
            cmd,
            cwd=str(repo_root),
            stdout=tmp,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        tmp_path = Path(tmp.name)

    tmp_path.replace(ns.log)
    print(f"log_path={ns.log}")
    print(f"exit_code={proc.returncode}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
