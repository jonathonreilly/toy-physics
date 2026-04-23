#!/usr/bin/env python3
"""Audit runner for the one-axiom acceptance hostile-review memo."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def expect(name: str, cond: bool, detail: str = "") -> int:
    if cond:
        suffix = f" -- {detail}" if detail else ""
        print(f"PASS: {name}{suffix}")
        return 1
    suffix = f" -- {detail}" if detail else ""
    print(f"FAIL: {name}{suffix}")
    return 0


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def main() -> int:
    passed = 0
    total = 0

    note = read("docs/PLANCK_SCALE_ONE_AXIOM_ACCEPTANCE_HOSTILE_REVIEW_MEMO_2026-04-23.md")
    one_axiom_info = read("docs/SINGLE_AXIOM_INFORMATION_NOTE.md")
    one_axiom_hilbert = read("docs/SINGLE_AXIOM_HILBERT_NOTE.md")
    bridge = read("docs/PLANCK_SCALE_MINIMAL_STACK_TO_PRIMITIVE_CELL_DATUM_THEOREM_2026-04-23.md")
    vac = read("docs/PLANCK_SCALE_UNIVERSAL_CELL_COEFFICIENT_NOT_VACUUM_EXPECTATION_THEOREM_2026-04-23.md")
    obj = read("docs/PLANCK_SCALE_PRIMITIVE_COEFFICIENT_OBJECT_CLASS_THEOREM_2026-04-23.md")
    datum = read("docs/PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md")

    total += 1
    passed += expect(
        "memo-distinguishes-one-axiom-from-minimal-ledger",
        "native close on the accepted one-axiom semantic surface" in note
        and "not yet front-door minimal-ledger retained" in note,
    )

    total += 1
    passed += expect(
        "one-axiom-notes-explicitly-scope-themselves-as-support",
        "not the load-bearing accepted input ledger" in one_axiom_info
        and "not the load-bearing accepted input ledger" in one_axiom_hilbert,
    )

    total += 1
    passed += expect(
        "primitive-cell-object-is-now-front-door-anchored",
        "The exact remaining gap is still the state-selection step" in bridge
        or "remaining gap is no longer object selection" in bridge,
    )

    total += 1
    passed += expect(
        "generic-vacuum-reading-boxed-out",
        "generic dynamical reduced-vacuum" in vac
        and "cannot coherently" in vac,
    )

    total += 1
    passed += expect(
        "object-class-theorem-makes-reclassification-a-category-change",
        "changes the object" in obj
        and "larger datum class" in obj,
    )

    total += 1
    passed += expect(
        "one-axiom-default-datum-theorem-closes-quarter",
        "rho_cell = I_16 / 16" in datum
        and "a = l_P" in datum,
    )

    total += 1
    passed += expect(
        "memo-keeps-package-boundary-move-explicit",
        "explicitly promote the one-axiom information / Hilbert / locality" in note,
    )

    total += 1
    passed += expect(
        "memo-does-not-overclaim-minimal-ledger-proof",
        "already retained by the front-door minimal ledger alone" in note
        and "still **not** defensible" in note,
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
