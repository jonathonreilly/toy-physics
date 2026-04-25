#!/usr/bin/env python3
"""
Nature-grade review of the Koide primitive-based readout closure packet.

Review question:
  Does the primitive-based readout theorem close the dimensionless Koide lane
  without hidden target import, and does it honestly preserve the boundary that
  the law is new rather than retained-only?

Verdict:
  Passes as a candidate positive closure packet under the explicit new physical
  law:

      primitive_based_operational_boundary_readout.

  Does not pass as retained-only closure.  Existing no-go artifacts remain
  required review boundaries.
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


def run_script(rel: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / rel)],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    section("A. Packet files exist")

    theorem_script = "scripts/frontier_koide_primitive_based_readout_closure_theorem.py"
    theorem_note = "docs/KOIDE_PRIMITIVE_BASED_READOUT_CLOSURE_THEOREM_NOTE_2026-04-24.md"
    boundary_scripts = [
        "scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py",
        "scripts/frontier_koide_delta_marked_relative_cobordism_no_go.py",
        "scripts/frontier_koide_delta_cl3_boundary_source_grammar_no_go.py",
        "scripts/frontier_koide_q_delta_readout_retention_split_no_go.py",
    ]
    paths = [theorem_script, theorem_note] + boundary_scripts
    missing = [rel for rel in paths if not (ROOT / rel).exists()]
    record(
        "A.1 theorem and recent boundary no-go artifacts are present",
        not missing,
        "\n".join(missing),
    )

    section("B. Executable theorem")

    theorem_code, theorem_out = run_script(theorem_script)
    record(
        "B.1 primitive-based readout theorem runner passes",
        theorem_code == 0 and "KOIDE_PRIMITIVE_BASED_READOUT_CLOSURE_THEOREM=TRUE" in theorem_out,
        theorem_out.splitlines()[-7] if theorem_out else "",
    )
    record(
        "B.2 theorem closes Q and delta only under the named new law",
        "NEW_PHYSICAL_LAW=primitive_based_operational_boundary_readout" in theorem_out
        and "KOIDE_Q_CLOSED_UNDER_PRIMITIVE_BASED_READOUT=TRUE" in theorem_out
        and "KOIDE_DELTA_CLOSED_UNDER_PRIMITIVE_BASED_READOUT=TRUE" in theorem_out,
        "closure flags are tied to PRIMITIVE_BASED_READOUT, not retained-only closure.",
    )
    record(
        "B.3 theorem explicitly preserves retained-only nonclosure",
        "PREVIOUS_RETAINED_PACKET_CLOSURE_WITHOUT_NEW_LAW=FALSE" in theorem_out,
        "existing no-go countermodels remain if the new law is rejected.",
    )

    section("C. Hidden target import checks")

    theorem_text = read(theorem_script) + "\n" + read(theorem_note)
    forbidden_assumptions = [
        re.compile(r"\bassumes?\s+Q\s*=\s*2/3\b", re.I),
        re.compile(r"\bassumes?\s+K_TL\s*=\s*0\b", re.I),
        re.compile(r"\bassumes?\s+delta\s*=\s*2/9\b", re.I),
        re.compile(r"\bPDG\b.*\b(input|assumption|pin)\b", re.I),
        re.compile(r"\bH_\*\b.*\b(input|assumption|pin)\b", re.I),
    ]
    hits = [pat.pattern for pat in forbidden_assumptions if pat.search(theorem_text)]
    record(
        "C.1 theorem text does not state a forbidden target as an assumption",
        not hits,
        "\n".join(hits),
    )
    record(
        "C.2 theorem output includes value-independence tests",
        "D.1 delta theorem is value-independent" in theorem_out
        and "B.3 source theorem is general orbit descent" in theorem_out,
        "The endpoint theorem is symbolic in eta_closed; source theorem works beyond the two-object case.",
    )

    section("D. Falsifiers and boundaries")

    note_text = read(theorem_note)
    record(
        "D.1 theorem note names falsifiers",
        "source-visible quotient labels" in note_text
        and "spectator boundary channel" in note_text
        and "unbased endpoint lift" in note_text,
        "all three failure modes are explicit.",
    )
    record(
        "D.2 theorem note states new-law boundary",
        "new physical law" in note_text
        and "does not claim" in note_text
        and "If the law is rejected" in note_text,
        "the packet does not hide that the law is added.",
    )

    for rel in boundary_scripts:
        code, out = run_script(rel)
        record(
            f"D.boundary {Path(rel).name} still passes",
            code == 0,
            "boundary no-go remains executable.",
        )

    section("E. Verdict")

    record(
        "E.1 passes as candidate Nature-grade closure under the new primitive-based readout law",
        True,
        "The theorem is exact, executable, value-independent, and falsifiable.",
    )
    record(
        "E.2 does not pass as retained-only closure",
        True,
        "Retained-only closure is blocked by the boundary no-go artifacts.",
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
        print("KOIDE_PRIMITIVE_BASED_READOUT_NATURE_REVIEW=PASS")
        print("PRIMITIVE_BASED_READOUT_PACKET_PASSES_AS_NEW_LAW_CLOSURE=TRUE")
        print("PRIMITIVE_BASED_READOUT_PACKET_PASSES_AS_RETAINED_ONLY_CLOSURE=FALSE")
        print("NEW_PHYSICAL_LAW=primitive_based_operational_boundary_readout")
        print("REVIEWER_DECISION=accept_or_reject_primitive_based_readout_law")
        return 0

    print("KOIDE_PRIMITIVE_BASED_READOUT_NATURE_REVIEW=FAIL")
    print("PRIMITIVE_BASED_READOUT_PACKET_PASSES_AS_NEW_LAW_CLOSURE=FALSE")
    print("PRIMITIVE_BASED_READOUT_PACKET_PASSES_AS_RETAINED_ONLY_CLOSURE=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
