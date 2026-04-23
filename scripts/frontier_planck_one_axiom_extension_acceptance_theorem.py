#!/usr/bin/env python3
"""Audit runner for explicit Planck-package one-axiom extension acceptance."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_ONE_AXIOM_EXTENSION_ACCEPTANCE_THEOREM_2026-04-23.md"
INFO = ROOT / "docs/SINGLE_AXIOM_INFORMATION_NOTE.md"
HILBERT = ROOT / "docs/SINGLE_AXIOM_HILBERT_NOTE.md"


def expect(name: str, cond: bool) -> int:
    if cond:
        print(f"PASS: {name}")
        return 1
    print(f"FAIL: {name}")
    return 0


def main() -> int:
    note = NOTE.read_text()
    info = INFO.read_text()
    hilbert = HILBERT.read_text()

    checks = [
        (
            "extension-is-explicitly-promoted",
            "explicitly promoted" in note and "Axiom Extension P1" in note,
        ),
        (
            "extension-is-load-bearing-not-support-only",
            "load-bearing axiom extension" in note,
        ),
        (
            "extension-introduces-no-scale",
            "no observed lattice spacing" in note
            and "no tunable parameter" in note
            and "no new numerical constant" in note,
        ),
        (
            "extension-states-no-preferred-event",
            "no preferred primitive event" in note,
        ),
        (
            "extension-keeps-minimal-ledger-caveat",
            "older minimal ledger alone" in note
            and "not be worded" in note,
        ),
        (
            "information-note-still-supplies-surface",
            "information flows between them" in info
            and "without being created or destroyed" in info,
        ),
        (
            "hilbert-note-still-supplies-event-semantics",
            "finite-dimensional Hilbert space with local tensor product structure"
            in hilbert,
        ),
    ]

    passed = 0
    for name, cond in checks:
        passed += expect(name, cond)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
