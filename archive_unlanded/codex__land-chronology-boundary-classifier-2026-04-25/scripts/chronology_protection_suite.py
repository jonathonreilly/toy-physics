#!/usr/bin/env python3
"""Chronology protection suite runner.

This runner compiles and executes the retained chronology-protection probes as
one review packet. It does not prove a stronger claim than the individual
probes. Its job is to keep the lane reproducible and to print the retained
boundary statement:

  reversible reconstruction is allowed; operational past signaling to an
  earlier durable record is not available on the retained single-clock,
  local-data surface.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROBES = [
    "scripts/chronology_cycle_insertion_probe.py",
    "scripts/loschmidt_echo_record_probe.py",
    "scripts/advanced_vs_retarded_field_probe.py",
    "scripts/causal_cycle_fixed_point_dimension_probe.py",
    "scripts/postselection_ctc_nonlinearity_probe.py",
    "scripts/future_boundary_import_index.py",
    "scripts/partial_loschmidt_record_lower_bound.py",
    "scripts/chronology_import_budget.py",
    "scripts/ctc_fixed_point_taxonomy_probe.py",
    "scripts/postselection_no_signaling_audit.py",
    "scripts/multi_time_support_constraint_probe.py",
    "scripts/chronology_operator_algebra_no_past_signal_probe.py",
    "scripts/durable_record_formation_boundary_probe.py",
]


def compile_probe(rel_path: str) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "py_compile", rel_path],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode == 0, proc.stdout.strip()


def run_probe(rel_path: str) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, rel_path],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = proc.stdout.strip()
    tail = "\n".join(output.splitlines()[-8:])
    return proc.returncode == 0, tail


def main() -> int:
    print("=" * 88)
    print("CHRONOLOGY PROTECTION SUITE")
    print("  Review packet for no operational past signaling on the retained surface.")
    print("=" * 88)
    print()

    failures: list[str] = []
    for rel_path in PROBES:
        if not (ROOT / rel_path).exists():
            print(f"[FAIL] {rel_path}")
            print("missing required chronology probe")
            print()
            failures.append(rel_path)
            continue

        compile_ok, compile_output = compile_probe(rel_path)
        if not compile_ok:
            print(f"[FAIL] {rel_path}")
            print("py_compile failed")
            if compile_output:
                print(compile_output)
            print()
            failures.append(rel_path)
            continue

        ok, tail = run_probe(rel_path)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {rel_path}")
        print(tail)
        print()
        if not ok:
            failures.append(rel_path)

    print("RETAINED CONCLUSION")
    print(
        "  The framework admits equation-level reversibility and closed-state "
        "reconstruction."
    )
    print(
        "  Apparent late-to-early mechanisms are classified by imported "
        "non-retained structure."
    )
    print(
        "  No operation at t1 alters an earlier durable record at t0 < t1 on "
        "the retained single-clock local-data surface."
    )
    print()
    print(f"PROBES_RUN = {len(PROBES)}")
    print(f"FAILURES = {len(failures)}")
    if failures:
        for rel_path in failures:
            print(f"FAILED: {rel_path}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
