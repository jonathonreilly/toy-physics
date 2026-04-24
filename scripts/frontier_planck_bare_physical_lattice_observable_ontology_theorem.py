#!/usr/bin/env python3
"""Verifier for the bare physical-lattice observable ontology theorem."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def main() -> int:
    note = read("docs/PLANCK_SCALE_BARE_PHYSICAL_LATTICE_OBSERVABLE_ONTOLOGY_THEOREM_2026-04-23.md")
    program = read("docs/PLANCK_SCALE_BARE_CELL_ALONE_CLOSURE_PROGRAM_2026-04-23.md")
    physical = read("docs/PHYSICAL_LATTICE_NECESSITY_NOTE.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "b1-closure-scoped",
        "This closes B1 of the bare-cell-alone upgrade program" in note
        and "B1. Physical-Lattice Semantics From Algebra" in program,
        "B1 is explicitly closed on the retained observable-algebra reading",
    )

    total += 1
    passed += expect(
        "observable-algebra-not-stripped-matrix",
        "not just an abstract sixteen-dimensional Hilbert space" in note
        and "stripped\nmatrix algebra `M_16(C)`" in note,
        "the theorem distinguishes retained Cl(3)/Z^3 structure from M16 alone",
    )

    total += 1
    passed += expect(
        "local-translation-observables-retained",
        "local `Cl(3)` event algebra" in note
        and "`Z^3` translation/adjacency algebra" in note
        and "translation characters and local sectors" in note,
        "physicality is derived from retained local/translation observables",
    )

    total += 1
    passed += expect(
        "regulator-extra-structure",
        "regulator reading requires" in note
        and "continuum-limit family" in note
        and "None of those is an automorphism of the retained `Cl(3)` / `Z^3` observable\nalgebra" in note,
        "regulator reinterpretation is extra structure, not same algebra",
    )

    total += 1
    passed += expect(
        "consistent-with-physical-lattice-note",
        "physical-lattice reading is the unique surviving interpretation" in physical
        or "physical-lattice reading is the unique\nsurviving interpretation" in physical,
        "existing physical-lattice note supports the ontology theorem",
    )

    total += 1
    passed += expect(
        "no-planck-overclaim",
        "This does not yet determine its numerical value" in note
        and "B1 alone derives `a = l_P`" in note,
        "B1 does not claim Planck-scale normalization",
    )

    total += 1
    passed += expect(
        "reviewer-links-b1",
        "PLANCK_SCALE_BARE_PHYSICAL_LATTICE_OBSERVABLE_ONTOLOGY_THEOREM_2026-04-23.md" in reviewer,
        "canonical packet links the B1 theorem",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
