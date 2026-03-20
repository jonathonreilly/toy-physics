#!/usr/bin/env python3
"""Run a generated-family mechanism ladder overnight."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import subprocess
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECKER = REPO_ROOT / "scripts" / "wider_generated_family_mechanism_check.py"
ENSEMBLES = ("ultra", "mega", "giga")


def banner(title: str) -> None:
    print()
    print(title)
    print("=" * len(title))


def main() -> None:
    print(
        "overnight generated-family ladder started "
        + datetime.now().isoformat(timespec="seconds"),
        flush=True,
    )
    print(f"checker={CHECKER}", flush=True)
    print(f"ensembles={ENSEMBLES}", flush=True)
    total_started = time.time()

    for index, ensemble_name in enumerate(ENSEMBLES, start=1):
        banner(f"[{index}/{len(ENSEMBLES)}] {ensemble_name}")
        started = time.time()
        subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                "--ensemble",
                ensemble_name,
            ],
            cwd=REPO_ROOT,
            check=True,
        )
        print(
            f"{ensemble_name} completed in {time.time() - started:.1f}s",
            flush=True,
        )

    print()
    print(
        "overnight generated-family ladder completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_started:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
