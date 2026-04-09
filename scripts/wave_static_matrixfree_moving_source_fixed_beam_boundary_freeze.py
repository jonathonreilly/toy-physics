#!/usr/bin/env python3
"""Atomic log wrapper for the moving-source fixed-beam exact-comparator probe."""

from __future__ import annotations

import argparse
from datetime import date
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def default_log_path() -> Path:
    root = Path(__file__).resolve().parent.parent
    stamp = os.environ.get("FREEZE_STAMP") or date.today().isoformat()
    return root / "logs" / f"{stamp}-wave-static-matrixfree-moving-source-fixed-beam-boundary.txt"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, default=None, help="Output log path. Defaults under logs/.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments forwarded after --")
    ns = parser.parse_args()

    extra = ns.args
    if extra and extra[0] == "--":
        extra = extra[1:]

    script = Path(__file__).resolve().with_name("wave_static_matrixfree_moving_source_fixed_beam_boundary.py")
    log_path = ns.log or default_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [sys.executable, str(script), *extra]
    with tempfile.NamedTemporaryFile("w", delete=False, dir=str(log_path.parent), prefix=".tmp-", suffix=".log") as tmp:
        proc = subprocess.run(cmd, stdout=tmp, stderr=subprocess.STDOUT, text=True)
        tmp_path = Path(tmp.name)

    tmp_path.replace(log_path)
    print(f"log_path={log_path}")
    print(f"exit_code={proc.returncode}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
