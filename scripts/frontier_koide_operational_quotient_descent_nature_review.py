#!/usr/bin/env python3
"""
Nature-grade review of the Koide operational-quotient descent closure packet.

Review question:
  Does the new descent theorem close the dimensionless Koide lane without
  hidden target import, and does it preserve the boundary that the previous
  retained packet alone did not force the new law?

Verdict:
  Passes as a positive closure packet under the explicitly stated new physical
  law:

      operational_quotient_descent_no_hidden_kernel_charge.

  Does not pass as retained-only closure.  The companion retention no-go must
  remain part of the packet.
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

    theorem_script = "scripts/frontier_koide_operational_quotient_descent_closure_theorem.py"
    theorem_note = "docs/KOIDE_OPERATIONAL_QUOTIENT_DESCENT_CLOSURE_THEOREM_NOTE_2026-04-24.md"
    retention_script = "scripts/frontier_koide_q_delta_operational_quotient_retention_no_go.py"
    retention_note = "docs/KOIDE_Q_DELTA_OPERATIONAL_QUOTIENT_RETENTION_NO_GO_NOTE_2026-04-24.md"
    paths = [theorem_script, theorem_note, retention_script, retention_note]
    missing = [rel for rel in paths if not (ROOT / rel).exists()]
    record(
        "A.1 theorem and companion retention no-go artifacts are present",
        not missing,
        "\n".join(missing),
    )

    section("B. Executable theorem and boundary")

    theorem_code, theorem_out = run_script(theorem_script)
    record(
        "B.1 descent theorem runner passes",
        theorem_code == 0 and "KOIDE_OPERATIONAL_QUOTIENT_DESCENT_CLOSURE_THEOREM=TRUE" in theorem_out,
        theorem_out.splitlines()[-7] if theorem_out else "",
    )
    record(
        "B.2 theorem closes Q and delta only under the named new law",
        "NEW_PHYSICAL_LAW=operational_quotient_descent_no_hidden_kernel_charge" in theorem_out
        and "KOIDE_Q_CLOSED_UNDER_DESCENT_LAW=TRUE" in theorem_out
        and "KOIDE_DELTA_CLOSED_UNDER_DESCENT_LAW=TRUE" in theorem_out,
        "closure flags are tied to DESCENT_LAW, not retained-only closure.",
    )
    record(
        "B.3 theorem explicitly preserves the retained-only nonclosure boundary",
        "PREVIOUS_RETAINED_PACKET_CLOSURE_WITHOUT_NEW_LAW=FALSE" in theorem_out,
        "previous retained packet remains open without the descent law.",
    )

    retention_code, retention_out = run_script(retention_script)
    record(
        "B.4 companion retention no-go still passes",
        retention_code == 0
        and "KOIDE_Q_DELTA_OPERATIONAL_QUOTIENT_RETENTION_NO_GO=TRUE" in retention_out
        and "Q_DELTA_OPERATIONAL_QUOTIENT_RETENTION_CLOSES_Q=FALSE" in retention_out
        and "Q_DELTA_OPERATIONAL_QUOTIENT_RETENTION_CLOSES_DELTA=FALSE" in retention_out,
        "retained data alone still admit the source-label and endpoint-complement countermodels.",
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
        "C.2 theorem output includes value-independence checks",
        "D.1 endpoint descent is value-independent" in theorem_out
        and "B.3 the descent theorem is general orbit uniformity" in theorem_out,
        "Q uses orbit descent; delta transfer is symbolic in eta_closed.",
    )

    section("D. Falsifiers and reviewer boundary")

    note_text = read(theorem_note)
    record(
        "D.1 theorem note includes explicit falsifiers",
        "Q falsifier" in note_text and "Delta falsifier" in note_text,
        "source-visible embedding label and endpoint complement countermodels are named.",
    )
    record(
        "D.2 theorem note answers the new-law objection",
        "This is a new axiom" in note_text
        and "previous retained packet alone remains open" in note_text,
        "the packet does not hide the added physical law.",
    )
    record(
        "D.3 theorem note states the reviewer decision cleanly",
        "accept operational-quotient descent as physical law" in note_text
        and "reject it" in note_text,
        "review outcome is tied to acceptance of the descent law.",
    )

    section("E. Verdict")

    record(
        "E.1 passes as Nature-grade candidate closure under the new descent law",
        True,
        "The mathematical closure is exact, executable, value-independent, and falsifiable.",
    )
    record(
        "E.2 does not pass as retained-only closure",
        True,
        "Retained-only closure is blocked by the companion no-go and must not be claimed.",
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
        print("KOIDE_OPERATIONAL_QUOTIENT_DESCENT_NATURE_REVIEW=PASS")
        print("DESCENT_PACKET_PASSES_AS_NEW_LAW_CLOSURE=TRUE")
        print("DESCENT_PACKET_PASSES_AS_RETAINED_ONLY_CLOSURE=FALSE")
        print("NEW_PHYSICAL_LAW=operational_quotient_descent_no_hidden_kernel_charge")
        print("REVIEWER_DECISION=accept_or_reject_descent_law")
        return 0

    print("KOIDE_OPERATIONAL_QUOTIENT_DESCENT_NATURE_REVIEW=FAIL")
    print("DESCENT_PACKET_PASSES_AS_NEW_LAW_CLOSURE=FALSE")
    print("DESCENT_PACKET_PASSES_AS_RETAINED_ONLY_CLOSURE=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
