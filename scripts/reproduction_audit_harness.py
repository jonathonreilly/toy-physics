#!/usr/bin/env python3
"""Reproduction audit harness for the current canonical frontier.

This is a skeptical-reader entry point, not a physics-proof script.
It does three things:

  1. runs the bounded canonical regression gate
  2. runs one bounded cross-family retained comparison
  3. prints a short inventory of what should be treated as canonical vs
     exploratory

The default cross-family comparison is deliberately narrow:
- exact 2D mirror validation
- structured chokepoint bridge

Both are retained harnesses on different families, so they are a good
reproducibility check without turning this into a broad search.

Optional:
- ``--full-cross-family`` runs the heavier 3D family sweep from the existing
  exploratory benchmark, but that is not part of the default audit path.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable


class AuditFailure(RuntimeError):
    """Raised when the audit harness detects a drift or missing artifact."""


def run_script(path: str, *args: str, timeout: int = 240) -> str:
    proc = subprocess.run(
        [PYTHON, str(REPO_ROOT / path), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if proc.returncode != 0:
        raise AuditFailure(
            f"{path} failed with exit code {proc.returncode}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def extract_float(pattern: str, text: str, label: str) -> float:
    match = re.search(pattern, text)
    if not match:
        raise AuditFailure(f"missing {label}")
    return float(match.group(1))


def run_canonical_gate() -> None:
    print("=" * 88)
    print("CANONICAL GATE")
    print("  Cheap drift checks for the retained frontier.")
    print("=" * 88)
    print(run_script("scripts/canonical_regression_gate.py").rstrip())
    print()


def run_cross_family_retained_comparison() -> None:
    print("=" * 88)
    print("CROSS-FAMILY RETAINED COMPARISON")
    print("  exact 2D mirror vs structured chokepoint bridge")
    print("=" * 88)

    mirror = run_script("scripts/mirror_2d_validation.py")
    structured = run_script("scripts/structured_chokepoint_bridge.py")

    mirror_born = extract_float(r"Born audit: max \|I3\|/P = ([0-9.eE+-]+)", mirror, "mirror 2D Born")
    require(mirror_born < 1e-10, f"mirror 2D Born drifted: {mirror_born}")
    require("seeds=8" in mirror, "mirror 2D validation seed count drifted")

    structured_borns = [float(m) for m in re.findall(r"\s([0-9]+\.[0-9]+e[+-][0-9]+)\s+\+0\.00e\+00", structured)]
    require(structured_borns, "structured bridge Born values missing")
    require(all(v < 1e-10 for v in structured_borns), f"structured bridge Born drifted: {structured_borns}")
    require("DECISION: retained structured bridge pocket" in structured, "structured bridge verdict changed")

    mirror_row = re.search(
        r"^\s*60\s+0\.756118\s+0\.4420\s+0\.8572\s+\+2\.5687\s+1\.08e-15\s+\+0\.00e\+00\s+8$",
        mirror,
        re.MULTILINE,
    )
    require(mirror_row is not None, "mirror 2D retained row changed")

    bridge_row = re.search(
        r"^\s*60\s+0\.6440\s+0\.8030±0\.04\s+1\.0043\s+\+5\.7613±0\.892\s+0\.0000±0\.00\s+\+0\.00e\+00\s+16$",
        structured,
        re.MULTILINE,
    )
    require(bridge_row is not None, "structured bridge retained row changed")

    print(f"mirror 2D: Born {mirror_born:.2e}, retained N=60 row still present")
    print("structured chokepoint: Born machine-clean, retained N=60 row still present")
    print("comparison read: two retained families, same review-safe control logic, distinct geometry")
    print()


def run_full_cross_family() -> None:
    print("=" * 88)
    print("OPTIONAL HEAVIER CROSS-FAMILY BENCHMARK")
    print("  existing 3D family sweep from the exploratory robustness lane")
    print("=" * 88)
    out = run_script("scripts/cross_family_robustness.py", timeout=900)
    require("INTERPRETATION:" in out, "cross-family robustness footer missing")
    require("MODULAR" in out and "HIERARCHICAL" in out, "cross-family family labels missing")
    print(out.rstrip())
    print()


def print_inventory() -> None:
    print("=" * 88)
    print("REPRODUCTION INVENTORY")
    print("  canonical harnesses vs exploratory drivers")
    print("=" * 88)
    print("Canonical entry points:")
    print("  - scripts/canonical_regression_gate.py")
    print("  - scripts/reproduction_audit_harness.py")
    print("  - docs/CANONICAL_HARNESS_INDEX.md")
    print("  - docs/START_HERE.md")
    print("  - docs/REVIEW_HARDENING_BACKLOG.md")
    print("Exploratory drivers kept separate:")
    print("  - scripts/cross_family_robustness.py")
    print("  - scripts/lattice_4d_kernel_test.py")
    print("  - scripts/transfer_norm_and_born.py")
    print("  - scripts/evolving_network_prototype.py")
    print("  - scripts/self_regulating_gap_3d.py")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full-cross-family",
        action="store_true",
        help="run the heavier 3D family sweep from the exploratory robustness lane",
    )
    args = parser.parse_args()

    print_inventory()
    run_canonical_gate()
    run_cross_family_retained_comparison()
    if args.full_cross_family:
        run_full_cross_family()
    print("=" * 88)
    print("REPRODUCTION AUDIT: PASS")
    print("=" * 88)


if __name__ == "__main__":
    main()
