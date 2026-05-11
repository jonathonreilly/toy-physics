#!/usr/bin/env python3
"""Primary audit runner for the SU(3) Wigner Block 4/5 narrow split.

The source note has two computational limbs:
  - Block 4 staging claims (1)-(5), verified by the existing L=3 cube runner.
  - Block 5 orientation diagnostics claims (6)-(7), verified by the new
    geometry-only L=2 PBC runner.

The audit graph records one primary runner per note, so this wrapper makes the
whole cleanable core visible as one runner without re-implementing either limb.
Classification hint: finite plaquette enumeration and lattice configuration
counts are delegated to the two source runners below.
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path


AUDIT_TIMEOUT_SEC = 180

ROOT = Path(__file__).resolve().parents[1]

RUNNERS = [
    (
        "Block 4 staging",
        "scripts/frontier_su3_wigner_l3_cube_partition.py",
        "SUMMARY: THEOREM PASS=5 FAIL=0",
    ),
    (
        "Block 5 orientation diagnostics",
        "scripts/frontier_su3_wigner_block5_orientation_diagnostics_narrow.py",
        "SUMMARY: PASS=11 FAIL=0",
    ),
]

FORBIDDEN_IMPORTS = {
    "frontier_su3_cube_index_graph_shortcut_open_gate",
    "frontier_su3_wigner_l2_cube_orientation_verification",
}


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"[{tag}] {label}{suffix}")


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            out.add(node.module)
    return out


def run_runner(label: str, rel_path: str, expected_summary: str) -> None:
    path = ROOT / rel_path
    check(f"{label} runner exists", path.exists(), rel_path)
    if not path.exists():
        return

    imports = imported_modules(path)
    forbidden = sorted(
        module for module in imports
        if module in FORBIDDEN_IMPORTS or module.split(".")[0] in FORBIDDEN_IMPORTS
    )
    check(f"{label} avoids open-gate runner imports", not forbidden, ", ".join(forbidden))

    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "scripts")
    result = subprocess.run(
        [sys.executable, rel_path],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=AUDIT_TIMEOUT_SEC - 20,
        check=False,
    )
    print(f"\n--- {label} stdout tail ---")
    print("\n".join(result.stdout.splitlines()[-35:]))
    if result.stderr.strip():
        print(f"\n--- {label} stderr ---")
        print(result.stderr.strip())

    check(f"{label} exits 0", result.returncode == 0, f"returncode={result.returncode}")
    check(
        f"{label} expected summary present",
        expected_summary in result.stdout,
        expected_summary,
    )


def main() -> int:
    print("SU(3) Wigner Block 4/5 narrow split primary runner")
    print("=" * 72)
    for label, rel_path, expected_summary in RUNNERS:
        run_runner(label, rel_path, expected_summary)

    print("=" * 72)
    print(f"SUMMARY: PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
