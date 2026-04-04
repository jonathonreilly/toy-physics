#!/usr/bin/env python3
"""Bounded regression gate for the current canonical lattice/NN frontier.

This is not a proof script. It is a cheap drift detector for the retained
review-facing harnesses so we can catch accidental code/report mismatches early.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def run_script(script: str, timeout: int = 180) -> str:
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / script)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    return proc.stdout


def require(pattern: str, text: str, label: str) -> re.Match[str]:
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if match is None:
        raise AssertionError(f"missing expected pattern for {label}: {pattern}")
    return match


def require_float_lt(pattern: str, text: str, threshold: float, label: str) -> None:
    match = require(pattern, text, label)
    value = float(match.group(1))
    if not value < threshold:
        raise AssertionError(f"{label} expected < {threshold}, got {value}")


def require_float_gt(pattern: str, text: str, threshold: float, label: str) -> None:
    match = require(pattern, text, label)
    value = float(match.group(1))
    if not value > threshold:
        raise AssertionError(f"{label} expected > {threshold}, got {value}")


def check_dense_3d_card() -> None:
    text = run_script("scripts/lattice_3d_dense_10prop.py")
    require_float_lt(r"Born \|I3\|/P = ([0-9.eE+-]+)", text, 1e-10, "dense-3D Born")
    require_float_gt(r"d_TV = ([0-9.]+)", text, 0.1, "dense-3D d_TV")
    require_float_lt(r"3\. k=0 = ([0-9.eE+-]+)", text, 1e-12, "dense-3D k=0")
    require_float_gt(r"Decoherence = ([0-9.]+)%", text, 5.0, "dense-3D decoherence")
    require_float_gt(r"MI = ([0-9.]+) bits", text, 0.05, "dense-3D MI")
    require(r"Grows with N: YES\s+\[PASS\]", text, "dense-3D grows-with-N")
    require(
        r"Hierarchy-aligned support: 4/4 points, b\^\(-1\.62\), R²=0\.976",
        text,
        "dense-3D hierarchy support",
    )


def check_dense_window_extension() -> None:
    text = run_script("scripts/lattice_3d_dense_window_extension.py")
    require(r"Decision: BOUNDED EXTENSION\.", text, "dense-window decision")
    require(r"^\s*6\s+\+[0-9.]+\s+\+[0-9.]+\s+\+[0-9.]+\s+[0-9.eE+-]+\s+0\.137\s+0\.138\s+0\.373\s+ATTRACTIVE$", text, "dense-window z=6 row")
    require(r"^\s*7\s+\+0\.000000\s+\+0\.000000\s+\+nan\s+[0-9.eE+-]+\s+0\.141\s+0\.135\s+0\.379\s+MIXED$", text, "dense-window z=7 row")
    require_float_lt(r"Born = ([0-9.eE+-]+)", text, 1e-10, "dense-window Born")


def check_dense_refinement_reconciliation() -> None:
    text = run_script("scripts/lattice_3d_dense_refinement_reconciliation.py")
    require(r"Verdict: FAILS\.", text, "dense-refinement verdict")
    require(r"h=1\.0: barrier read=MIXED, distance fit=b\^\(-0\.94\), R²=0\.934, attractive distance rows=5/5", text, "dense-refinement h=1.0 summary")
    require(r"h=0\.5: barrier read=MIXED, distance fit=n/a, attractive distance rows=0/5", text, "dense-refinement h=0.5 summary")
    require_float_lt(r"h = 1\.0.*?Born=([0-9.eE+-]+)", text, 1e-10, "dense-refinement h=1.0 Born")
    require_float_lt(r"h = 0\.5.*?Born=([0-9.eE+-]+)", text, 1e-10, "dense-refinement h=0.5 Born")


def check_gravity_hierarchy() -> None:
    text = run_script("scripts/gravity_observable_hierarchy.py")
    require(r"2D dense spent-delay\s+ultra-weak retained\s+\+[0-9.]+\s+\+[0-9.]+\s+\+[0-9.]+\s+genuine attraction", text, "hierarchy 2D positive")
    require(r"3D power-action close-slit barrier\s+retained barrier card\s+-[0-9.]+\s+-0\.000000\s+-0\.918368\s+away / depletion", text, "hierarchy 3D power negative")
    require(r"3D dense spent-delay\s+retained dense z=5\s+\+[0-9.]+\s+\+[0-9.]+\s+\+[0-9.]+\s+genuine attraction", text, "hierarchy dense-3D positive")


def check_nn_continuum() -> None:
    text = run_script("scripts/lattice_nn_continuum.py")
    require(r"SAFE CLAIM: Born-clean positive refinement trend through h = 0\.25", text, "nn safe claim")
    require(r"0\.250\s+25921\s+161\s+\+0\.077415\s+\+0\.00e\+00\s+0\.9470\s+0\.4989\s+0\.9878\s+3\.83e-16", text, "nn h=0.25 row")
    require(r"0\.125\s+FAIL", text, "nn h=0.125 fail row")


def check_nn_deterministic_rescale() -> None:
    text = run_script("scripts/lattice_nn_deterministic_rescale.py")
    require(r"0\.0625\s+410881\s+641\s+\+0\.014810\s+\+0\.00e\+00\s+1\.0000\s+0\.5000\s+1\.0000\s+3\.00e-16", text, "nn deterministic h=0.0625 row")
    require(r"Born-safe extension works only if the Born column stays machine-clean", text, "nn deterministic interpretation")


def main() -> None:
    checks = [
        ("dense-3D card", check_dense_3d_card),
        ("dense-3D window extension", check_dense_window_extension),
        ("dense-3D refinement reconciliation", check_dense_refinement_reconciliation),
        ("gravity hierarchy", check_gravity_hierarchy),
        ("NN raw continuum", check_nn_continuum),
        ("NN deterministic rescale", check_nn_deterministic_rescale),
    ]
    print("=" * 88)
    print("CANONICAL FRONTIER REGRESSION GATE")
    print("  Cheap drift detector for the retained lattice/NN frontier.")
    print("=" * 88)
    print()
    for label, fn in checks:
        fn()
        print(f"[PASS] {label}")
    print()
    print("All canonical frontier regression checks passed.")


if __name__ == "__main__":
    main()
