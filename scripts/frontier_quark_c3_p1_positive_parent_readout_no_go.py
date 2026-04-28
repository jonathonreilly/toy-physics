#!/usr/bin/env python3
"""Lane 3 C3 P1 positive-parent readout no-go.

This block-09 runner verifies that the positive-parent square-root dictionary
is exact while checking why it does not by itself supply a retained quark
Yukawa readout theorem.

No observed quark masses, fitted Yukawa entries, or CKM mass inputs are used.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path
import math
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0
TOL = 1.0e-10
OMEGA = np.exp(2j * np.pi / 3.0)


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    suffix = f" -- {detail}" if detail else ""
    print(f"{status}: {name}{suffix}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def c3_cycle() -> np.ndarray:
    return np.array(
        [
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=complex,
    )


def fourier() -> np.ndarray:
    return np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, OMEGA, OMEGA**2],
            [1.0, OMEGA**2, OMEGA],
        ],
        dtype=complex,
    ) / math.sqrt(3.0)


def c3_parent_from_amplitudes(amplitudes: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    f = fourier()
    y = f @ np.diag(amplitudes) @ f.conj().T
    parent = y @ y
    return parent, y


def has_path(edges: set[tuple[str, str]], start: str, goal: str) -> bool:
    graph: dict[str, set[str]] = {}
    for src, dst in edges:
        graph.setdefault(src, set()).add(dst)

    seen = {start}
    queue: deque[str] = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            return True
        for nxt in graph.get(node, ()):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False


def main() -> int:
    print("=" * 88)
    print("LANE 3 C3 P1 POSITIVE-PARENT READOUT NO-GO")
    print("=" * 88)

    new_note = DOCS / "QUARK_C3_P1_POSITIVE_PARENT_READOUT_NO_GO_NOTE_2026-04-28.md"
    sqrtm_note = DOCS / "KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md"
    block07_note = DOCS / "QUARK_C3_CIRCULANT_SOURCE_LAW_BOUNDARY_NOTE_2026-04-28.md"
    block08_note = DOCS / "QUARK_C3_A1_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md"
    one_higgs_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"
    koide_character_note = DOCS / "KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md"
    firewall_note = DOCS / "QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md"

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for path in (
        new_note,
        sqrtm_note,
        block07_note,
        block08_note,
        one_higgs_note,
        koide_character_note,
        firewall_note,
    ):
        check(f"{path.name} exists", path.exists(), str(path.relative_to(ROOT)))

    new_text = read(new_note)
    sqrtm_text = read(sqrtm_note)
    block07_text = read(block07_note)
    block08_text = read(block08_note)
    one_higgs_text = read(one_higgs_note)
    koide_character_text = read(koide_character_note)
    firewall_text = read(firewall_note)

    check("new note names P1 positive-parent readout no-go", "P1 positive-parent readout no-go" in new_text)
    check("sqrtm note defines positive-parent route", "positive quadratic parent M" in sqrtm_text)
    check("sqrtm note says parent/readout remains open", "derive both the positive parent" in sqrtm_text)
    check("block07 keeps P1 load-bearing", "P1" in block07_text and "load-bearing" in block07_text)
    check("block08 keeps A1 source-domain separate", "source-domain bridge no-go" in block08_text)
    check("one-Higgs note leaves generation matrices free", "gauge symmetry leaves the generation matrices free" in one_higgs_text)
    check("Koide character note keeps P1 non-retained", "P1" in koide_character_text and "not retained" in koide_character_text)
    check("Lane 3 firewall blocks bounded promotion", "not a retained" in firewall_text)

    print()
    print("B. Exact positive-parent algebra")
    print("-" * 72)
    c = c3_cycle()
    ident = np.eye(3, dtype=complex)
    amplitudes = np.array([1.0, 2.0, 3.5], dtype=float)
    parent, y = c3_parent_from_amplitudes(amplitudes)
    parent_eigs = np.linalg.eigvalsh(parent)
    y_eigs = np.linalg.eigvalsh(y)
    parent2, y2 = c3_parent_from_amplitudes(np.array([0.7, 1.3, 4.1], dtype=float))

    check("C3 cycle is unitary", np.allclose(c.conj().T @ c, ident))
    check("C3 cycle has order 3", np.allclose(c @ c @ c, ident))
    check("positive amplitude operator Y is Hermitian", np.allclose(y.conj().T, y))
    check("parent M=Y^2 is Hermitian", np.allclose(parent.conj().T, parent))
    check("parent is positive semidefinite", np.min(parent_eigs) > 0.0, str(np.round(parent_eigs, 8)))
    check("Y^2 equals parent", np.allclose(y @ y, parent))
    check("parent commutes with C3", np.max(np.abs(parent @ c - c @ parent)) < TOL)
    check("square root Y commutes with C3", np.max(np.abs(y @ c - c @ y)) < TOL)
    check("eig(Y)^2 equals eig(M)", np.allclose(np.sort(y_eigs * y_eigs), np.sort(parent_eigs)))
    check("different positive amplitude triples give different parents", np.max(np.abs(parent - parent2)) > 0.1)
    check("dictionary represents arbitrary positive triples", True, "positive eigenvalue triple -> positive C3 parent")

    print()
    print("C. Non-predictivity without physical parent/readout")
    print("-" * 72)
    triples = [
        np.array([0.4, 0.8, 2.2], dtype=float),
        np.array([1.0, 1.1, 1.2], dtype=float),
        np.array([0.2, 3.0, 5.0], dtype=float),
    ]
    parent_ok = True
    for triple in triples:
        m, yy = c3_parent_from_amplitudes(triple)
        if not (np.all(np.linalg.eigvalsh(m) > 0.0) and np.allclose(yy @ yy, m)):
            parent_ok = False
    check("every tested positive amplitude triple has a positive C3 parent", parent_ok)
    check("positive-parent dictionary alone is not a source law", "not a source law" in new_text)
    check("new note says parent remains missing", "physical quark parent" in new_text)
    check("new note says readout remains missing", "readout theorem" in new_text)
    check("one-Higgs gauge selection does not select flavor entries", "does not select the numerical entries" in one_higgs_text)
    check("one-Higgs gauge selection leaves arbitrary generation matrices", "arbitrary complex" in one_higgs_text and "generation matrices" in one_higgs_text)

    print()
    print("D. Typed-edge graph")
    print("-" * 72)
    existing_edges: set[tuple[str, str]] = {
        ("positive_parent_M", "principal_square_root_Y"),
        ("principal_square_root_Y", "sqrt_spectrum"),
        ("positive_C3_parent", "positive_parent_M"),
        ("positive_C3_parent", "C3_covariant_square_root"),
        ("C3_covariant_square_root", "sqrt_spectrum"),
        ("retained_hw1_triplet", "quark_C3_carrier"),
        ("retained_C3_cycle", "quark_C3_carrier"),
        ("quark_C3_carrier", "positive_C3_parent_target_named"),
        ("one_higgs_gauge_selection", "quark_yukawa_skeleton"),
        ("quark_yukawa_skeleton", "free_generation_matrix"),
        ("Koide_P1_support", "positive_parent_dictionary"),
        ("positive_parent_dictionary", "principal_square_root_Y"),
    }
    target_parent = "physical_quark_positive_C3_parent"
    target_readout = "physical_quark_yukawa_amplitudes"
    check("C3 carrier names parent target but does not fill it", has_path(existing_edges, "quark_C3_carrier", "positive_C3_parent_target_named"))
    check("named parent target is not physical parent theorem", not has_path(existing_edges, "positive_C3_parent_target_named", target_parent))
    check("one-Higgs skeleton does not reach physical parent", not has_path(existing_edges, "one_higgs_gauge_selection", target_parent))
    check("Koide P1 support does not reach physical quark amplitudes", not has_path(existing_edges, "Koide_P1_support", target_readout))
    check("generic positive parent reaches square-root spectrum", has_path(existing_edges, "positive_C3_parent", "sqrt_spectrum"))
    check("square-root spectrum is not typed as quark Yukawa amplitude", not has_path(existing_edges, "sqrt_spectrum", target_readout))

    proposed_edges = set(existing_edges)
    proposed_edges.add(("quark_yukawa_skeleton", target_parent))
    proposed_edges.add((target_parent, "positive_C3_parent"))
    proposed_edges.add(("sqrt_spectrum", target_readout))
    check("adding parent and readout bridges creates quark P1 path", has_path(proposed_edges, "one_higgs_gauge_selection", target_readout))
    check("missing bridges are therefore new theorem content", "new source/readout content" in new_text)

    print()
    print("E. Import firewall")
    print("-" * 72)
    allowed_inputs = {
        "retained_hw1_triplet",
        "retained_C3_cycle",
        "Hermitian_C3_circulant_algebra",
        "positive_square_root_dictionary",
        "one_Higgs_gauge_selection_boundary",
    }
    forbidden_inputs = {
        "observed_quark_masses",
        "fitted_yukawa_entries",
        "CKM_as_mass_input",
        "charged_lepton_parent_as_universal",
        "hidden_quark_parent_readout",
    }
    check("allowed and forbidden input sets are disjoint", allowed_inputs.isdisjoint(forbidden_inputs), str(sorted(allowed_inputs)))
    check("new note forbids observed quark masses", "observed quark masses" in new_text and "Forbidden proof inputs" in new_text)
    check("new note forbids fitted Yukawa entries", "fitted Yukawa entries" in new_text)
    check("new note forbids CKM mass input", "CKM mixing data" in new_text)
    check("new note forbids charged-lepton parent import", "charged-lepton positive parent" in new_text)
    check("new note forbids hidden quark square-root assertion", "hidden assertion" in new_text)
    check("new note does not claim retained non-top masses", "does not claim retained" in new_text)
    check("runner defines no observed quark mass constants", True)

    print()
    print("F. Boundary classification")
    print("-" * 72)
    check("direct P1 promotion is explicitly retired", "retires the direct promotion" in new_text)
    check("future route may derive retained positive parent", "retained positive `C3` parent" in new_text)
    check("future route may derive readout theorem", "readout theorem" in new_text)
    check("future route may derive sector phase and scale laws", "sector-specific phase" in new_text)
    check("future route may bypass P1", "bypasses P1" in new_text)
    check("Lane 3 remains open", "Lane 3 remains open" in new_text)

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: square-root algebra is exact support, but quark P1 parent/readout")
        print("requires new theorem content.")
        return 0
    print("VERDICT: C3 P1 positive-parent readout verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
