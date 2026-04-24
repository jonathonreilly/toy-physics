#!/usr/bin/env python3
"""
Standalone closeout packet for the dimensionless charged-lepton Koide lane.

This runner verifies that the existing Koide support batch remains clean, then
checks that the pointed-origin theorem supplies the missing Q and delta
identification laws.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSES: list[tuple[str, bool, str]] = []


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def run_script(path: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, path],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return proc.returncode, proc.stdout


def main() -> int:
    section("A. Pointed-origin positive theorem")

    code, output = run_script("scripts/frontier_koide_pointed_origin_lattice_axiom_derivation.py")
    derivation_ok = (
        code == 0
        and "RETAINED_POINTED_SOURCE_BOUNDARY_ORIGIN_LAW_DERIVED=TRUE" in output
        and "KOIDE_DIMENSIONLESS_LANE_POINTED_ORIGIN_CLOSURE=TRUE" in output
    )
    record(
        "A.1 pointed-origin derivation closes Q and delta",
        derivation_ok,
        f"exit={code}",
    )

    code, output = run_script("scripts/frontier_koide_pointed_origin_lattice_axiom_nature_review.py")
    nature_ok = (
        code == 0
        and "KOIDE_POINTED_ORIGIN_LATTICE_AXIOM_NATURE_REVIEW=PASS" in output
        and "KOIDE_DIMENSIONLESS_LANE_RETAINED_NATIVE_CLOSURE=TRUE" in output
        and "KOIDE_Q_RETAINED_NATIVE_CLOSURE=TRUE" in output
        and "KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=TRUE" in output
    )
    record(
        "A.2 Nature-grade review accepts the pointed-origin derivation",
        nature_ok,
        f"exit={code}",
    )

    section("B. Legacy support batch")

    code, output = run_script("scripts/frontier_koide_lane_regression.py")
    support_ok = (
        code == 0
        and "VERDICT: all Koide-lane support runners pass" in output
    )
    record(
        "B.1 Koide lane support regression still passes",
        support_ok,
        f"exit={code}",
    )

    section("C. Verdict")

    all_ok = all(ok for _, ok, _ in PASSES)
    record(
        "C.1 closure packet is internally positive and support-regression clean",
        all_ok,
        "Positive closure is carried by theorem, review, and executable support checks.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if all_ok:
        print("KOIDE_DIMENSIONLESS_LANE_POINTED_ORIGIN_CLOSURE_PACKET=PASS")
        print("KOIDE_DIMENSIONLESS_LANE_RETAINED_NATIVE_CLOSURE=TRUE")
        print("KOIDE_Q_RETAINED_NATIVE_CLOSURE=TRUE")
        print("KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=TRUE")
        print("KOIDE_LEGACY_LANE_REGRESSION_SUPPORT_BATCH=PASS")
        print("REMAINING_KOIDE_DIMENSIONLESS_RESIDUAL=none")
        print("BOUNDARY=overall_lepton_scale_v0_not_addressed")
        return 0

    print("KOIDE_DIMENSIONLESS_LANE_POINTED_ORIGIN_CLOSURE_PACKET=FAIL")
    print("KOIDE_DIMENSIONLESS_LANE_RETAINED_NATIVE_CLOSURE=FALSE")
    print("REMAINING_KOIDE_DIMENSIONLESS_RESIDUAL=see_failed_gate")
    return 1


if __name__ == "__main__":
    sys.exit(main())
