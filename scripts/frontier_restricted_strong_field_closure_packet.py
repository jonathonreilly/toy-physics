#!/usr/bin/env python3
"""Packet runner for the restricted strong-field closure note.

This is a thin packet harness: it executes the canonical shell-source,
static-lift, Schur-action, Dirichlet-principle, star-supported sanity, and
reduced-shell-law runners and fails if any component fails or omits its summary.
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


SUMMARY_RE = re.compile(r"PASS=(?P<pass>\d+) FAIL=(?P<fail>\d+) TOTAL=(?P<total>\d+)")


@dataclass(frozen=True)
class Component:
    path: str
    role: str


COMPONENTS = [
    Component("scripts/frontier_sewing_shell_source.py", "exact shell source"),
    Component("scripts/frontier_oh_static_constraint_lift.py", "static conformal lift"),
    Component("scripts/frontier_oh_schur_boundary_action.py", "Schur boundary action"),
    Component(
        "scripts/frontier_microscopic_dirichlet_bridge_principle.py",
        "Dirichlet bridge minimizer",
    ),
    Component("scripts/frontier_star_supported_bridge_class.py", "finite-rank support sanity"),
    Component("scripts/frontier_one_parameter_reduced_shell_law.py", "reduced shell law"),
]


def run_component(repo: Path, component: Component) -> tuple[int, int, int]:
    cmd = [sys.executable, component.path]
    proc = subprocess.run(cmd, cwd=repo, text=True, capture_output=True, check=False)

    print("=" * 72)
    print(f"COMPONENT: {component.path}")
    print(f"ROLE: {component.role}")
    print("=" * 72)
    print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n")
    if proc.stderr:
        print("STDERR:")
        print(proc.stderr, end="" if proc.stderr.endswith("\n") else "\n")

    if proc.returncode != 0:
        raise SystemExit(f"{component.path} exited with {proc.returncode}")

    matches = SUMMARY_RE.findall(proc.stdout)
    if not matches:
        raise SystemExit(f"{component.path} did not print a PASS/FAIL summary")

    passed, failed, total = (int(x) for x in matches[-1])
    if failed != 0 or passed != total:
        raise SystemExit(
            f"{component.path} summary not clean: PASS={passed} FAIL={failed} TOTAL={total}"
        )
    return passed, failed, total


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    grand_pass = 0
    grand_total = 0

    print("Restricted strong-field closure packet")
    print("=" * 72)
    for component in COMPONENTS:
        passed, _failed, total = run_component(repo, component)
        grand_pass += passed
        grand_total += total

    print("=" * 72)
    print("PACKET SUMMARY")
    print("=" * 72)
    print(f"PASS={grand_pass} FAIL=0 TOTAL={grand_total}")
    print("[EXACT] PASS: restricted strong-field closure packet runners all passed")


if __name__ == "__main__":
    main()
