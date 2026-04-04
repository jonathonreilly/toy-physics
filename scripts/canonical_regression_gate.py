#!/usr/bin/env python3
"""Bounded regression gate for the current canonical frontier.

This is not a physics-proof script. It is a cheap drift detector for the
artifact-backed frontier that the repo currently presents as canonical.

The gate intentionally checks only review-safe conditions:
  - machine-clean Born / k=0 thresholds where those are retained
  - retained verdict strings on narrow branch reconciliations
  - presence of hierarchy-aligned support where the notes depend on it
  - absence of obvious runtime / formatting regressions

It does not try to re-prove the science or replace the script/log/note chain.
"""

from __future__ import annotations

import math
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable


class GateFailure(RuntimeError):
    """Raised when a canonical regression check fails."""


def run_script(path: str) -> str:
    proc = subprocess.run(
        [PYTHON, str(REPO_ROOT / path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise GateFailure(
            f"{path} failed with exit code {proc.returncode}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateFailure(message)


def extract_float(pattern: str, text: str, label: str) -> float:
    match = re.search(pattern, text)
    if not match:
        raise GateFailure(f"missing {label}")
    return float(match.group(1))


def check_dense_3d_card() -> None:
    out = run_script("scripts/lattice_3d_dense_10prop.py")
    born = extract_float(r"1\. Born \|I3\|/P = ([0-9.eE+-]+)", out, "3D dense Born")
    k0 = extract_float(r"3\. k=0 = ([0-9.eE+-]+)", out, "3D dense k=0")
    mi = extract_float(r"7\. MI = ([0-9.eE+-]+) bits", out, "3D dense MI")
    decoh = extract_float(r"6\. Decoherence = ([0-9.eE+-]+)%", out, "3D dense decoherence")
    require(born < 1e-10, f"3D dense Born drifted: {born}")
    require(abs(k0) < 1e-12, f"3D dense k=0 drifted: {k0}")
    require(mi > 0.05, f"3D dense MI unexpectedly weak: {mi}")
    require(decoh > 5.0, f"3D dense decoherence unexpectedly weak: {decoh}%")
    require("Grows with N: YES  [PASS]" in out, "3D dense N-growth verdict changed")
    require("Hierarchy-aligned support: 4/4" in out, "3D dense hierarchy support changed")


def check_dense_3d_extension() -> None:
    out = run_script("scripts/lattice_3d_dense_window_extension.py")
    require("Decision: BOUNDED EXTENSION." in out, "3D dense extension verdict changed")
    require("z=6" in out, "3D dense extension no longer reports the z=6 boundary")
    require("z=7 is signal-free / mixed" in out, "3D dense extension boundary wording changed")
    require(
        re.search(r"^\s*6\s+\+0\.[0-9]+\s+\+0\.[0-9]+\s+\+0\.[0-9]+\s+6\.[0-9]+e-16", out, re.MULTILINE)
        is not None,
        "3D dense z=6 retained row missing",
    )
    require(
        re.search(r"^\s*7\s+\+0\.000000\s+\+0\.000000\s+\+nan", out, re.MULTILINE) is not None,
        "3D dense z=7 boundary row changed",
    )


def check_dense_3d_reconciliation() -> None:
    out = run_script("scripts/lattice_3d_dense_refinement_reconciliation.py")
    match_h1 = re.search(r"h = 1\.0.*?Born=([0-9.eE+-]+)", out, re.S)
    match_h05 = re.search(r"h = 0\.5.*?Born=([0-9.eE+-]+)", out, re.S)
    if not match_h1:
        raise GateFailure("missing reconciliation h=1 Born")
    if not match_h05:
        raise GateFailure("missing reconciliation h=0.5 Born")
    born_h1 = float(match_h1.group(1))
    born_h05 = float(match_h05.group(1))
    require(born_h1 < 1e-10, f"reconciliation h=1 Born drifted: {born_h1}")
    require(born_h05 < 1e-10, f"reconciliation h=0.5 Born drifted: {born_h05}")
    require("Verdict: FAILS." in out, "dense refinement reconciliation verdict changed")
    require("attractive distance rows=5/5" in out, "h=1.0 attraction-support count changed")
    require("attractive distance rows=0/5" in out, "h=0.5 attraction-support count changed")


def check_gravity_hierarchy() -> None:
    out = run_script("scripts/gravity_observable_hierarchy.py")
    require("2D dense spent-delay                ultra-weak retained" in out, "missing 2D retained hierarchy row")
    require("3D dense spent-delay                retained dense z=3" in out, "missing 3D dense z=3 hierarchy row")
    require("3D power-action close-slit barrier  retained barrier card" in out, "missing 3D power barrier hierarchy row")
    require("genuine attraction" in out, "missing attraction interpretation in hierarchy output")
    require("away / depletion" in out, "missing depletion interpretation in hierarchy output")


def check_structured_bridge() -> None:
    out = run_script("scripts/structured_chokepoint_bridge.py")
    born_values = [float(m) for m in re.findall(r"\s([0-9]+\.[0-9]+e[+-][0-9]+)\s+\+0\.00e\+00", out)]
    require(born_values, "structured bridge Born values missing")
    require(all(v < 1e-10 for v in born_values), f"structured bridge Born drifted: {born_values}")
    require("DECISION: retained structured bridge pocket" in out, "structured bridge verdict changed")
    require(re.search(r"^\s*60\s+0\.[0-9]+\s+0\.8030±0\.04", out, re.MULTILINE) is not None,
            "structured bridge retained N=60 row changed materially")


def main() -> None:
    checks = [
        ("dense 3D canonical card", check_dense_3d_card),
        ("dense 3D window extension", check_dense_3d_extension),
        ("dense 3D refinement reconciliation", check_dense_3d_reconciliation),
        ("gravity observable hierarchy", check_gravity_hierarchy),
        ("structured bridge", check_structured_bridge),
    ]

    print("=" * 88)
    print("CANONICAL REGRESSION GATE")
    print("  Cheap drift checks for the current canonical frontier.")
    print("=" * 88)

    failed = False
    for label, fn in checks:
        try:
            fn()
            print(f"[PASS] {label}")
        except GateFailure as exc:
            failed = True
            print(f"[FAIL] {label}: {exc}")

    print("=" * 88)
    if failed:
        print("REGRESSION GATE: FAIL")
        raise SystemExit(1)
    print("REGRESSION GATE: PASS")


if __name__ == "__main__":
    main()
