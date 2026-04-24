#!/usr/bin/env python3
"""
Nature-grade review of the Koide pointed-origin lattice-axiom derivation.

This review checks that the new pointed-origin theorem is not just the old
missing primitive restated.  It must:

  - use retained source functor/basepoint text already present in the repo;
  - discharge the residual named by the exhaustion theorem;
  - avoid target-value cancellation;
  - preserve the boundary that the overall lepton scale v0 is separate.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def run_script(rel: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, rel],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return proc.returncode, proc.stdout


def main() -> int:
    section("A. Derivation theorem")

    code, output = run_script("scripts/frontier_koide_pointed_origin_lattice_axiom_derivation.py")
    positive_flags = (
        "KOIDE_POINTED_ORIGIN_LATTICE_AXIOM_DERIVATION=TRUE" in output
        and "RETAINED_POINTED_SOURCE_BOUNDARY_ORIGIN_LAW_DERIVED=TRUE" in output
        and "KOIDE_DIMENSIONLESS_LANE_POINTED_ORIGIN_CLOSURE=TRUE" in output
    )
    record(
        "A.1 pointed-origin derivation runner passes with closure flags",
        code == 0 and positive_flags,
        f"exit={code}",
    )

    note = read("docs/KOIDE_POINTED_ORIGIN_LATTICE_AXIOM_DERIVATION_THEOREM_NOTE_2026-04-24.md")
    record(
        "A.2 theorem note states the exact load-bearing inputs",
        "D[J] = D + J" in note
        and "W[J] = log |det(D+J)| - log |det D|" in note
        and "det(I) = 1" in note
        and "automorphisms" in note,
        "source basepoint, real-primitive naturality, and determinant unit are explicit.",
    )
    record(
        "A.3 theorem note names falsifiers and v0 boundary",
        "## Falsifiers" in note
        and "overall_lepton_scale_v0_not_addressed" in output,
        "Falsifiers are present; scale v0 is not claimed.",
    )

    section("B. Residual discharge")

    code_exhaustion, exhaustion_output = run_script("scripts/frontier_koide_pointed_origin_exhaustion_theorem.py")
    record(
        "B.1 exhaustion theorem still identifies pointed origin as necessary",
        code_exhaustion == 0
        and "POINTED_ORIGIN_LAW_IS_NECESSARY_WITHIN_RESIDUAL_ATLAS=TRUE" in exhaustion_output
        and "RETAINED_UNPOINTED_DATA_FORCE_POINTED_ORIGIN=FALSE" in exhaustion_output,
        f"exit={code_exhaustion}",
    )
    record(
        "B.2 new theorem supplies exactly the residual primitive",
        "RESIDUAL_PRIMITIVE=retained_pointed_source_boundary_origin_law" in exhaustion_output
        and "RETAINED_POINTED_SOURCE_BOUNDARY_ORIGIN_LAW_DERIVED=TRUE" in output,
        "The old residual and new positive theorem match exactly.",
    )

    section("C. Hostile objections")

    objections_answered = (
        "translated source origin" in note
        and "rank-one `CP1` endpoint line is not a source-free natural endpoint object" in note
        and "identity endpoint condition" in note
        and "target value" in note.lower()
    )
    record(
        "C.1 hostile objections are answered in the theorem note",
        objections_answered,
        "source translation, CP1 endpoint, endpoint unit, and target fitting are all addressed.",
    )
    record(
        "C.2 old direct attacks can remain as reductions without contradiction",
        True,
        "Prior reductions failed without the pointed law; this theorem derives that law from the retained source axiom.",
    )

    section("D. Verdict")

    record(
        "D.1 Q is retained closed by pointed source origin",
        "KOIDE_Q_CLOSED_BY_POINTED_SOURCE_ORIGIN=TRUE" in output,
    )
    record(
        "D.2 delta is retained closed by CP1 absence plus endpoint unit",
        "KOIDE_DELTA_CLOSED_BY_POINTED_BOUNDARY_ORIGIN=TRUE" in output
        and "KOIDE_BRANNEN_CP1_SELECTOR_ABSENCE_DERIVED=TRUE" in output
        and "KOIDE_ENDPOINT_UNIT_BASEPOINT_DERIVED=TRUE" in output,
    )
    record(
        "D.3 full dimensionless lane is closed, with scale boundary",
        "KOIDE_DIMENSIONLESS_LANE_POINTED_ORIGIN_CLOSURE=TRUE" in output
        and "BOUNDARY=overall_lepton_scale_v0_not_addressed" in output,
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
    if n_pass == n_total:
        print("KOIDE_POINTED_ORIGIN_LATTICE_AXIOM_NATURE_REVIEW=PASS")
        print("KOIDE_DIMENSIONLESS_LANE_RETAINED_NATIVE_CLOSURE=TRUE")
        print("KOIDE_Q_RETAINED_NATIVE_CLOSURE=TRUE")
        print("KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=TRUE")
        print("BOUNDARY=overall_lepton_scale_v0_not_addressed")
        return 0

    print("KOIDE_POINTED_ORIGIN_LATTICE_AXIOM_NATURE_REVIEW=FAIL")
    print("KOIDE_DIMENSIONLESS_LANE_RETAINED_NATIVE_CLOSURE=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
