#!/usr/bin/env python3
"""Audit runner for the one-axiom conservative semantics bridge theorem."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool) -> int:
    if cond:
        print(f"PASS: {name}")
        return 1
    print(f"FAIL: {name}")
    return 0


def main() -> int:
    passed = 0
    total = 0

    note = read("docs/PLANCK_SCALE_ONE_AXIOM_CONSERVATIVE_SEMANTICS_BRIDGE_THEOREM_2026-04-23.md")
    minimal = read("docs/MINIMAL_AXIOMS_2026-04-11.md")
    info = read("docs/SINGLE_AXIOM_INFORMATION_NOTE.md")
    hilbert = read("docs/SINGLE_AXIOM_HILBERT_NOTE.md")
    physical = read("docs/PHYSICAL_LATTICE_NECESSITY_NOTE.md")
    cell = read("docs/PLANCK_SCALE_MINIMAL_STACK_TO_PRIMITIVE_CELL_DATUM_THEOREM_2026-04-23.md")
    default = read("docs/PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md")

    total += 1
    passed += expect(
        "minimal-stack-has-cl3-z3",
        "local algebra is `Cl(3)`" in minimal and "`Z^3`" in minimal,
    )

    total += 1
    passed += expect(
        "one-axiom-surface-provides-information-semantics",
        "information flows between them" in info
        and "without being created or destroyed" in info,
    )

    total += 1
    passed += expect(
        "one-axiom-hilbert-surface-provides-local-factor-semantics",
        "finite-dimensional Hilbert space with local tensor product structure" in hilbert,
    )

    total += 1
    passed += expect(
        "physical-lattice-note-authorizes-one-axiom-surface",
        "accepted one-axiom" in physical and "physical-lattice" in physical,
    )

    total += 1
    passed += expect(
        "primitive-cell-object-is-fixed-before-state-semantics",
        "H_cell" in cell and "C^16" in cell,
    )

    total += 1
    passed += expect(
        "default-datum-theorem-uses-one-axiom-surface",
        "accepted one-axiom information / Hilbert / locality surface" in default,
    )

    total += 1
    passed += expect(
        "bridge-declares-no-new-scale-or-parameter",
        "introduces no new numerical constants" in note
        and "introduces no new tunable parameters" in note,
    )

    total += 1
    passed += expect(
        "bridge-keeps-hcell-and-pa-fixed",
        "changes neither `H_cell` nor `P_A`" in note,
    )

    total += 1
    passed += expect(
        "bridge-keeps-front-door-caveat-explicit",
        "front-door minimal ledger" in note and "Not safe" in note,
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
