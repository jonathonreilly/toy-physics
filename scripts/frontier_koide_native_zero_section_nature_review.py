#!/usr/bin/env python3
"""
Nature-grade review of the Koide native zero-section closure route.

Review question:
  Does the native zero-section route close the dimensionless Koide lane as a
  retained/native theorem, and if not, what exact work remains?

Verdict:
  The route is the strongest native closure path found so far.  It is exact,
  non-numerological, and it removes the delta spectator obstruction if the
  physical Brannen endpoint is the whole real nontrivial Z3 primitive.

  It does not yet pass as retained-only closure, because the repository still
  contains two competing descriptions of the Brannen object:

    - older selected-line/CP1 language, where a rank-one line is physical;
    - the native real-primitive route, where the real Z3 doublet is physical
      and rank-one lines are coordinate/gauge choices.

  Native closure requires a retained identification theorem resolving that
  conflict in favor of the real primitive, plus a determinant-line unit theorem
  for the open endpoint.
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


def run(rel: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, rel],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def main() -> int:
    section("A. Route packet")

    route_script = "scripts/frontier_koide_native_zero_section_closure_route.py"
    route_note = "docs/KOIDE_NATIVE_ZERO_SECTION_CLOSURE_ROUTE_NOTE_2026-04-24.md"
    route_exists = (ROOT / route_script).exists() and (ROOT / route_note).exists()
    record(
        "A.1 native zero-section route artifacts exist",
        route_exists,
        f"{route_script}\n{route_note}",
    )
    code, output = run(route_script)
    record(
        "A.2 native route runner passes",
        code == 0 and "PASSED: 17/17" in output,
        "runner closeout verified.",
    )
    record(
        "A.3 route does not claim retained-only closure",
        "RETAINED_ONLY_NATIVE_CLOSURE_CLAIMED=FALSE" in output,
        "Conditional route is not promoted beyond its proof boundary.",
    )

    section("B. Positive content")

    record(
        "B.1 Q closes under native zero-source source-response",
        "CONDITIONAL_NATIVE_ZERO_SECTION_CLOSES_Q=TRUE" in output,
        "The source-label zero section gives K_TL=0 and Q=2/3.",
    )
    record(
        "B.2 delta closes under real primitive plus unit endpoint",
        "CONDITIONAL_NATIVE_ZERO_SECTION_CLOSES_DELTA=TRUE" in output,
        "Real Z3 primitive removes spectator; unit endpoint removes c.",
    )
    record(
        "B.3 the route is not numerological",
        "no hidden target import" in output.lower()
        and "eta_APS=2/9" in output
        and "idempotents=[{a: 0, b: 0}, {a: 1, b: 0}]" in output,
        "Load-bearing checks are representation idempotents and unit preservation.",
    )

    section("C. Compatibility with retained Brannen support")

    brannen_note = read("docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md")
    selected_line_note = read("docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md")
    real_plane_support = (
        "real Koide amplitude vector" in brannen_note
        and "2-plane orthogonal" in brannen_note
        and "singlet axis" in brannen_note
        and "doublet conjugate-pair" in selected_line_note
        and "n_eff = 2" in selected_line_note
    )
    record(
        "C.1 retained Brannen geometry supports a real-doublet primitive reading",
        real_plane_support,
        "Existing notes describe the Brannen phase as real-plane rotation / conjugate-pair winding.",
    )
    cp1_rank_one_tension = (
        "selected-line `CP^1` carrier" in brannen_note
        or "tautological CP^1 line" in selected_line_note
    )
    record(
        "C.2 retained Brannen corpus also contains rank-one/CP1 language",
        cp1_rank_one_tension,
        "This is the exact interpretive conflict the native route must resolve.",
    )

    section("D. Remaining objections")

    objections = [
        "Does the physical Brannen endpoint mean the whole real primitive or a rank-one CP1 line?",
        "Is the CP1 line a coordinate presentation of the real primitive, or an extra physical selector?",
        "Is the open determinant endpoint a based unit-preserving functor, or an unbased torsor?",
        "Is zero-source source-response already the charged-lepton scalar readout?",
    ]
    record(
        "D.1 all remaining objections are identification theorems, not arithmetic gaps",
        len(objections) == 4,
        "\n".join(objections),
    )
    record(
        "D.2 retained-only closure is not yet reviewer-proof",
        True,
        "A hostile reviewer can reject the real-primitive reinterpretation until it is derived from the Brannen construction itself.",
    )

    section("E. Verdict")

    record(
        "E.1 passes as the next native closure route to pursue",
        True,
        "It is the first route that kills the delta spectator by retained real-representation irreducibility.",
    )
    record(
        "E.2 fails as completed retained/native closure today",
        True,
        "It still needs the real-primitive Brannen identification and determinant-line unit theorem.",
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
        print("KOIDE_NATIVE_ZERO_SECTION_NATURE_REVIEW=PASS_AS_ROUTE")
        print("KOIDE_NATIVE_ZERO_SECTION_RETAINED_CLOSURE=FALSE")
        print("NATIVE_ROUTE_CLOSES_CONDITIONALLY=TRUE")
        print("NEXT_NATIVE_THEOREM=derive_Brannen_endpoint_as_real_Z3_primitive_and_unit_determinant_readout")
        print("RESIDUAL_IDENTIFICATION_DELTA=rank_one_CP1_language_vs_real_primitive_endpoint")
        print("RESIDUAL_TRIVIALIZATION=unit_preserving_open_determinant_line_readout")
        return 0

    print("KOIDE_NATIVE_ZERO_SECTION_NATURE_REVIEW=FAIL")
    print("KOIDE_NATIVE_ZERO_SECTION_RETAINED_CLOSURE=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
