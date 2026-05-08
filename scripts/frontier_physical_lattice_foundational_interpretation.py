#!/usr/bin/env python3
"""Check the physical Cl(3) on Z^3 baseline-interpretation note.

This runner is a review-hygiene check, not a physics proof. It verifies
that the note restores existing repo semantics without adding an axiom,
writing an audit verdict, or promoting downstream theorem status.
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md"
MINIMAL_AXIOMS = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" | {detail}" if detail else ""
    print(f"{tag}: {label}{suffix}")


def main() -> int:
    if not NOTE.exists():
        print(f"missing note: {NOTE}")
        return 1
    if not MINIMAL_AXIOMS.exists():
        print(f"missing minimal axioms note: {MINIMAL_AXIOMS}")
        return 1

    note = NOTE.read_text()
    minimal = MINIMAL_AXIOMS.read_text()

    print("Physical Cl(3) on Z^3 baseline interpretation check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    check("source note is meta", "**Claim type:** meta" in note)
    effective_token = "effective" + "_status:"
    audit_clean_token = "audited" + "_clean"
    effective_label = "Effective" + " status"
    check("does not declare pipeline status", effective_label not in note and effective_token not in note)
    check("does not declare audit-clean verdict token", audit_clean_token not in note)
    check("does not call baseline a new axiom", "does not add a third mathematical axiom" in note)
    check("states physical local algebra Cl(3)", "physical local algebra is `Cl(3)`" in note)
    check("states physical spatial substrate Z^3", "physical spatial substrate is the cubic lattice `Z^3`" in note)
    check("states not a regulator/formal bookkeeping device", "regulator" in note and "formal bookkeeping device" in note)
    check("keeps downstream theorem promotion out of scope", "does not by itself promote any downstream theorem" in note)
    check("keeps audit lane authority explicit", "`claim_type`, `audit_status`, and\n`effective_status`" in note)
    check("keeps extra species/readout inputs explicit", "species or generation identification" in note and "readout bridges" in note)

    check("minimal axioms note has physical Cl(3) A1", "the physical local algebra is `Cl(3)`" in minimal)
    check("minimal axioms note has physical Z^3 A2", "the physical spatial substrate is the cubic" in minimal)

    forbidden_promotions = [
        ("bridge-gap count zero", r"bridge-gap admission count\s*(?:is|=|moves).*0"),
        ("physical baseline as positive theorem", "positive theorem under " + "physical"),
        ("physical baseline as effective status", "effective status under " + "physical-lattice"),
        ("AC closure by declaration", "AC" + "_" + r".*is closed"),
    ]
    for label, pattern in forbidden_promotions:
        check(
            f"forbidden promotion absent: {label}",
            re.search(pattern, note, flags=re.IGNORECASE | re.DOTALL) is None,
        )

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL:
        return 1
    print("Baseline semantics check passed: physical Cl(3) on Z^3 is restored as repo language, not promoted science.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
