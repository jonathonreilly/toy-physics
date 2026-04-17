#!/usr/bin/env python3
"""Freeze one H=0.25 direct-dM control ladder to a log file.

This is a thin logging-safe wrapper around
`wave_direct_dm_h025_control_batch.py`.
It exists so we can capture a control artifact without manual `tee`
pipelines or ad hoc shell redirection.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _default_log_path(family: str, seed: int, h_val: float) -> Path:
    h_tag = f"h{str(h_val).replace('.', '')}"
    return Path("logs") / f"2026-04-08-wave-direct-dm-{h_tag}-control-{family.lower()}-seed{seed}.txt"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", default="Fam1", help="Family label to freeze. Default: Fam1")
    parser.add_argument("--seed", type=int, default=0, help="Grow seed to freeze. Default: 0")
    parser.add_argument("--h", type=float, default=0.25, help="Resolution to freeze. Default: 0.25")
    parser.add_argument(
        "--log",
        type=Path,
        default=None,
        help="Log file path. Default: logs/2026-04-08-wave-direct-dm-h025-control-<family>-seed<seed>.txt",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    log_path = args.log or _default_log_path(args.family, args.seed, args.h)
    if not log_path.is_absolute():
        log_path = repo_root / log_path
    log_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-u",
        str(repo_root / "scripts" / "wave_direct_dm_h025_control_batch.py"),
        "--family",
        args.family,
        "--seed",
        str(args.seed),
        "--h",
        f"{args.h:.3f}",
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
