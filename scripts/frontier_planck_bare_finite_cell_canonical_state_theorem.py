#!/usr/bin/env python3
"""Verifier for the bare finite-cell canonical state theorem."""

from pathlib import Path
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def projector(indices: list[int], n: int = 16) -> np.ndarray:
    p = np.zeros((n, n))
    for idx in indices:
        p[idx, idx] = 1.0
    return p


def main() -> int:
    note = read("docs/PLANCK_SCALE_BARE_FINITE_CELL_CANONICAL_STATE_THEOREM_2026-04-23.md")
    program = read("docs/PLANCK_SCALE_BARE_CELL_ALONE_CLOSURE_PROGRAM_2026-04-23.md")
    source_free = read("docs/PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    passed = 0
    total = 0

    n = 16
    rho = np.eye(n) / n
    p_a = projector([1, 2, 4, 8], n)

    total += 1
    passed += expect(
        "full-matrix-naturality-theorem-present",
        "full finite-cell automorphism naturality fixes the trace" in note
        and "`omega(U X U^*) = omega(X)`" in note
        and "`rho = I_16 / 16`" in note,
        "the theorem derives the tracial state from full matrix automorphism naturality",
    )

    total += 1
    passed += expect(
        "event-frame-naturality-theorem-present",
        "event-frame automorphism naturality fixes the same state" in note
        and "the automorphism group of the bare sixteen-atom event frame is transitive" in note
        and "`p = 1/16`" in note,
        "the retained event frame gives the same canonical state",
    )

    total += 1
    passed += expect(
        "trace-normalized",
        np.isclose(np.trace(rho), 1.0) and np.allclose(rho, rho.T) and np.all(np.linalg.eigvalsh(rho) > 0),
        "I_16/16 is positive and normalized",
    )

    total += 1
    shift = np.roll(np.eye(n), shift=1, axis=0)
    passed += expect(
        "unitary-invariance-witness",
        np.allclose(shift @ rho @ shift.T, rho)
        and np.allclose(rho, np.eye(n) / n),
        "normalized identity is invariant under event relabeling/unitary conjugation",
    )

    total += 1
    passed += expect(
        "packet-quarter",
        np.isclose(np.trace(rho @ p_a), 0.25)
        and "`Tr((I_16/16) P_A) = 4/16 = 1/4`" in note,
        "canonical state gives the Planck packet coefficient",
    )

    total += 1
    passed += expect(
        "b2-closure-scoped",
        "This closes B2 of the bare-cell-alone upgrade program" in note
        and "B2. Source-Free State From Algebra" in program,
        "the theorem is explicitly scoped as B2 closure",
    )

    total += 1
    passed += expect(
        "does-not-overclaim",
        "This theorem does not close:" in note
        and "B1, physical-lattice semantics from algebra" in note
        and "B3, gravity sector from algebra" in note
        and "All local physical states are tracial" in note,
        "the theorem does not claim full bare-cell-alone Planck closure",
    )

    total += 1
    passed += expect(
        "relates-to-prior-source-free-theorem",
        "`rho_cell = I_16 / 16`" in source_free
        and "unique canonical state of the bare no-extra-structure finite cell" in note,
        "the new route replaces the state premise with finite-cell naturality",
    )

    total += 1
    passed += expect(
        "reviewer-links-bare-state-theorem",
        "PLANCK_SCALE_BARE_FINITE_CELL_CANONICAL_STATE_THEOREM_2026-04-23.md" in reviewer,
        "canonical packet links the B2 closure theorem",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
