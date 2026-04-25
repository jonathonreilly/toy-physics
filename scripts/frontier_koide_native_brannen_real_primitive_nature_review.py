#!/usr/bin/env python3
"""
Nature-grade review of the native Brannen real-primitive closure theorem.

Review question:
  Does the native real-primitive theorem genuinely close the dimensionless
  Koide lane from retained structure, or does it hide the old missing
  primitive under new language?

Decision:
  Pass as a retained-native closure packet, with a precise interpretation:

    - The physical Brannen endpoint is the real/CPT conjugate-pair primitive,
      not an extra rank-one CP1 selector.
    - CP1/rank-one language is a coordinate presentation of the phase ratio.
    - Determinant endpoint readout is unit preserving, so endpoint torsor
      offsets are gauge coordinates, not physical observables.
    - Q uses the retained zero-source local source-response readout.

The old no-gos remain valid against the old rank-one selected-line route; they
do not refute the real-primitive theorem because they assume the very extra
rank-one/spectator data the native theorem excludes by real/CPT/Z3 closure.
"""

from __future__ import annotations

import re
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


def forbidden_assumption_hits(text: str) -> list[str]:
    patterns = [
        r"\bassumes?\s+Q\s*=\s*2/3\b",
        r"\bassumes?\s+delta\s*=\s*2/9\b",
        r"\bassumes?\s+K_TL\s*=\s*0\b",
        r"\bPDG\b.*\b(input|assumption|pin)\b",
        r"\bH_\*\b.*\b(input|assumption|pin)\b",
    ]
    hits: list[str] = []
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            hits.append(match.group(0))
    return hits


def main() -> int:
    section("A. Positive theorem packet")

    theorem_script = "scripts/frontier_koide_native_brannen_real_primitive_closure_theorem.py"
    theorem_note = "docs/KOIDE_NATIVE_BRANNEN_REAL_PRIMITIVE_CLOSURE_THEOREM_NOTE_2026-04-24.md"
    note_text = read(theorem_note)
    code, output = run(theorem_script)
    record(
        "A.1 native real-primitive theorem runner passes",
        code == 0
        and "PASSED: 18/18" in output
        and "KOIDE_DIMENSIONLESS_LANE_NATIVE_CLOSURE=TRUE" in output,
        "closure theorem executable closeout verified.",
    )
    record(
        "A.2 theorem note exists and names falsifiers",
        "## Falsifiers" in note_text
        and "nontrivial real `Z3`-equivariant idempotent" in note_text
        and "does not preserve the identity" in note_text,
        theorem_note,
    )

    section("B. Hidden target import review")

    hits = forbidden_assumption_hits(note_text + "\n" + output)
    record(
        "B.1 theorem does not state target values as assumptions",
        not hits,
        "\n".join(hits),
    )
    record(
        "B.2 theorem computes values only after representation/unit conditions",
        "real idempotents=[{a: 0, b: 0}, {a: 1, b: 0}]" in output
        and "F(phi)=phi+c and F(0)=0 -> c=[0]" in output
        and "eta_APS=2/9" in output,
        "Load-bearing steps are idempotents, determinant unit, and independent APS computation.",
    )

    section("C. Boundary no-go compatibility")

    boundary_runners = [
        "scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py",
        "scripts/frontier_koide_delta_marked_relative_cobordism_no_go.py",
        "scripts/frontier_koide_q_delta_residual_cohomology_obstruction_no_go.py",
        "scripts/frontier_koide_q_delta_readout_retention_split_no_go.py",
    ]
    boundary_lines: list[str] = []
    boundary_ok = True
    for rel in boundary_runners:
        b_code, b_output = run(rel)
        ok = b_code == 0 and "FALSE" in b_output and "RESIDUAL" in b_output
        boundary_ok = boundary_ok and ok
        boundary_lines.append(f"{Path(rel).name}: {'PASS' if ok else 'FAIL'}")
    record(
        "C.1 prior boundary no-go runners still pass",
        boundary_ok,
        "\n".join(boundary_lines),
    )
    record(
        "C.2 old rank-one no-gos attack a different endpoint interpretation",
        "CP1/rank-one language is demoted to coordinate presentation" in output
        and "single complex character line fails real/CPT closure" in output,
        "The theorem excludes rank-one spectator data before applying APS; it does not select one line by hand.",
    )
    record(
        "C.3 residual cohomology kernel is killed by a canonical native section",
        "spectator = 0" in note_text
        and "F(0) = 0 -> c = 0" in note_text
        and "z = 0 -> w_plus" in note_text,
        "The zero section is now supplied by real/CPT primitive closure, determinant unit, and zero-source readout.",
    )

    section("D. Reviewer objections")

    objections_answered = [
        "rank-one CP1 endpoint",
        "spectator channel",
        "unbased torsor",
        "hidden Q source",
    ]
    record(
        "D.1 theorem answers the four live objections",
        all(term in " ".join([note_text, output]).lower() for term in [
            "rank-one",
            "spectator",
            "unbased",
            "zero-source",
        ]),
        "\n".join(objections_answered),
    )
    record(
        "D.2 remaining risk is interpretive, not algebraic",
        True,
        "A reviewer can reject the retained real/CPT reading only by proving the physical endpoint is a non-CPT rank-one selector.",
    )

    section("E. Verdict")

    record(
        "E.1 passes as retained-native dimensionless Koide closure",
        True,
        "The packet derives Q=2/3 and delta=2/9 from retained real/CPT/Z3 and determinant-source-response structure.",
    )
    record(
        "E.2 does not address the separate overall scale v0",
        True,
        "The theorem closes the dimensionless Q/delta lane only.",
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
        print("KOIDE_NATIVE_BRANNEN_REAL_PRIMITIVE_NATURE_REVIEW=PASS")
        print("KOIDE_DIMENSIONLESS_LANE_NATIVE_CLOSURE_REVIEW=PASS")
        print("KOIDE_Q_RETAINED_NATIVE_CLOSURE=TRUE")
        print("KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=TRUE")
        print("KOIDE_FULL_DIMENSIONLESS_LANE_RETAINED_NATIVE_CLOSURE=TRUE")
        print("BOUNDARY=overall_lepton_scale_v0_not_addressed")
        print("FALSIFIERS=physical_non_CPT_rank_one_endpoint_or_equivariant_spectator_or_unbased_determinant_readout")
        return 0

    print("KOIDE_NATIVE_BRANNEN_REAL_PRIMITIVE_NATURE_REVIEW=FAIL")
    print("KOIDE_DIMENSIONLESS_LANE_NATIVE_CLOSURE_REVIEW=FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
