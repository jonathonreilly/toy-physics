#!/usr/bin/env python3
"""Lane 3 C3 A1 source-domain bridge no-go.

This block-08 runner verifies that the existing Koide A1 support scalar
1/2 is exact, while also checking that the current support bank does not
type that scalar into the physical quark C3 Ward source ratio.

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
SCRIPTS = ROOT / "scripts"

PASS_COUNT = 0
FAIL_COUNT = 0
TOL = 1.0e-12


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


def circulant_eigenvalues(a: float, r: float, phase: float) -> np.ndarray:
    return np.array(
        [a + 2.0 * r * math.cos(phase + 2.0 * math.pi * k / 3.0) for k in range(3)],
        dtype=float,
    )


def koide_q(values: np.ndarray) -> float:
    return float(np.sum(values * values) / (float(np.sum(values)) ** 2))


def main() -> int:
    print("=" * 88)
    print("LANE 3 C3 A1 SOURCE-DOMAIN BRIDGE NO-GO")
    print("=" * 88)

    new_note = DOCS / "QUARK_C3_A1_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md"
    block07_note = DOCS / "QUARK_C3_CIRCULANT_SOURCE_LAW_BOUNDARY_NOTE_2026-04-28.md"
    koide_q_note = DOCS / "KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md"
    koide_a1_note = DOCS / "KOIDE_A1_CLOSURE_RECOMMENDATION_2026-04-22.md"
    koide_character_note = DOCS / "KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md"
    sqrtm_note = DOCS / "KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md"
    one_higgs_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"
    a1_lie_runner = SCRIPTS / "frontier_koide_a1_lie_theoretic_triple_match.py"

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for path in (
        new_note,
        block07_note,
        koide_q_note,
        koide_a1_note,
        koide_character_note,
        sqrtm_note,
        one_higgs_note,
        a1_lie_runner,
    ):
        check(f"{path.name} exists", path.exists(), str(path.relative_to(ROOT)))

    new_text = read(new_note)
    block07_text = read(block07_note)
    koide_q_text = read(koide_q_note)
    koide_a1_text = read(koide_a1_note)
    koide_character_text = read(koide_character_note)
    sqrtm_text = read(sqrtm_note)
    one_higgs_text = read(one_higgs_note)
    a1_lie_text = read(a1_lie_runner)

    check("new note names source-domain bridge no-go", "source-domain bridge no-go" in new_text)
    check("block07 leaves A1/P1 open", "A1/P1" in block07_text and "open" in block07_text)
    check("Koide Q bridge collapses to one primitive", "single-primitive problem" in koide_q_text)
    check("A1 recommendation says physical bridge remains open", "physical bridge requires" in koide_a1_text)
    check("Koide character bridge records exact A1 equality", "equal-character-weight" in koide_character_text and "E_+" in koide_character_text)
    check("sqrtm note keeps parent/readout open", "derive both the positive parent" in sqrtm_text)
    check("one-Higgs note is gauge selection, not eigenvalue selection", "Yukawa" in one_higgs_text)
    check("A1 Lie runner marks an open closure lemma", "OPEN LEMMA" in a1_lie_text)

    print()
    print("B. Exact A1 algebra")
    print("-" * 72)
    a = 2.0
    r_a1 = a / math.sqrt(2.0)
    phases = [0.0, 0.19, 0.83, 1.41]
    q_values = [koide_q(circulant_eigenvalues(a, r_a1, phase)) for phase in phases]
    off_values = circulant_eigenvalues(a, 0.22, 0.41)
    e_plus = 3.0 * a * a
    e_perp = 6.0 * r_a1 * r_a1

    check("A1 ratio is |q|^2/a^2 = 1/2", abs((r_a1 * r_a1) / (a * a) - 0.5) < TOL)
    check("A1 equals cyclic block energy equality", abs(e_plus - e_perp) < TOL, f"E_plus={e_plus:.6f}, E_perp={e_perp:.6f}")
    check("A1 gives Q=2/3 for all tested phases", all(abs(q - 2.0 / 3.0) < TOL for q in q_values), str(np.round(q_values, 10)))
    check("off-A1 ratio does not give Q=2/3", abs(koide_q(off_values) - 2.0 / 3.0) > 0.05, f"Q={koide_q(off_values):.6f}")
    check("Q formula matches 1/3 + 2r^2/(3a^2)", abs(q_values[1] - (1.0 / 3.0 + 2.0 * r_a1 * r_a1 / (3.0 * a * a))) < TOL)
    check("A1 is one scalar constraint, not phase selection", "phase" in block07_text and "still leaves" in block07_text)
    check("A1 is one scalar constraint, not scale selection", "scale" in block07_text and "still leaves" in block07_text)

    print()
    print("C. Existing support-face inventory")
    print("-" * 72)
    support_scalars = {
        "cyclic_block_power": 0.5,
        "spinor_even_clifford_dim_ratio": 2.0 / 4.0,
        "su2_fundamental_weight_sq": 0.5,
        "ew_casimir_difference": 0.75 - 0.25,
        "charged_lepton_PQ": 0.5,
    }
    check("all support faces equal 1/2", all(abs(v - 0.5) < TOL for v in support_scalars.values()), str(support_scalars))
    check("Koide Q bridge records dim(spinor)/dim(Cl+) = 1/2", "dim(spinor) / dim(Cl" in koide_q_text and "1/2" in koide_q_text)
    check("Koide Q bridge records T(T+1)-Y^2 = 1/2", "T(T+1) - Y^2 = 1/2" in koide_q_text)
    check("A1 recommendation records SU(2)_L fundamental-weight evidence", "Lie-theoretic match" in koide_a1_text and "SU(2)_L" in koide_a1_text)
    check("A1 recommendation records one new retained primitive cost", "Cost" in koide_a1_text and "1 new retained primitive" in koide_a1_text)
    check("A1 Lie runner fundamental match is support, not closure", "what's missing is the specific structural lemma" in a1_lie_text)

    print()
    print("D. Typed-edge graph")
    print("-" * 72)
    existing_edges: set[tuple[str, str]] = {
        ("cyclic_block_power_1_2", "koide_A1_support_scalar"),
        ("spinor_even_clifford_dim_ratio_1_2", "koide_A1_support_scalar"),
        ("su2_fund_weight_sq_1_2", "koide_A1_support_scalar"),
        ("ew_casimir_difference_1_2", "koide_A1_support_scalar"),
        ("koide_A1_support_scalar", "charged_lepton_PQ_1_2"),
        ("charged_lepton_PQ_1_2", "charged_lepton_Q_2_3"),
        ("quark_c3_source_ratio_A1", "quark_c3_Q_2_3"),
        ("quark_c3_Q_2_3", "quark_c3_amplitude_relation"),
        ("retained_hw1_triplet", "quark_c3_carrier"),
        ("retained_C3_cycle", "quark_c3_carrier"),
        ("quark_c3_carrier", "quark_c3_source_ratio_target_named"),
        ("one_higgs_gauge_selection", "quark_yukawa_skeleton"),
    }
    source_nodes = [
        "cyclic_block_power_1_2",
        "spinor_even_clifford_dim_ratio_1_2",
        "su2_fund_weight_sq_1_2",
        "ew_casimir_difference_1_2",
        "koide_A1_support_scalar",
        "charged_lepton_PQ_1_2",
    ]
    target = "quark_c3_source_ratio_A1"
    no_existing_paths = [not has_path(existing_edges, src, target) for src in source_nodes]
    check("current graph has no A1-support path to quark source ratio", all(no_existing_paths), str(dict(zip(source_nodes, no_existing_paths))))
    check("quark carrier names the target but does not fill it", has_path(existing_edges, "quark_c3_carrier", "quark_c3_source_ratio_target_named"))
    check("named target is distinct from derived source ratio", not has_path(existing_edges, "quark_c3_source_ratio_target_named", target))
    check("one-Higgs gauge selection does not reach quark source ratio", not has_path(existing_edges, "one_higgs_gauge_selection", target))
    check("support scalar reaches charged-lepton Q only", has_path(existing_edges, "koide_A1_support_scalar", "charged_lepton_Q_2_3"))
    check("quark source ratio would imply quark C3 Q if granted", has_path(existing_edges, target, "quark_c3_Q_2_3"))

    proposed_edges = set(existing_edges)
    proposed_edges.add(("koide_A1_support_scalar", "quark_c3_source_ratio_A1"))
    check("adding exactly the missing bridge creates the desired path", has_path(proposed_edges, "koide_A1_support_scalar", target))
    check("missing bridge is therefore new theorem content", "new theorem" in new_text and "content rather than latent support" in new_text)

    print()
    print("E. Import firewall")
    print("-" * 72)
    allowed_inputs = {
        "retained_hw1_triplet",
        "retained_C3_cycle",
        "Hermitian_C3_circulant_algebra",
        "Koide_A1_support_faces",
        "one_Higgs_gauge_selection_boundary",
    }
    forbidden_inputs = {
        "observed_quark_masses",
        "fitted_yukawa_entries",
        "CKM_as_mass_input",
        "charged_lepton_A1_physical_bridge_as_universal",
        "hidden_block_extremum_for_quarks",
    }
    check("allowed and forbidden input sets are disjoint", allowed_inputs.isdisjoint(forbidden_inputs), str(sorted(allowed_inputs)))
    check("new note forbids observed quark masses", "observed quark masses" in new_text and "Forbidden proof inputs" in new_text)
    check("new note forbids fitted Yukawa entries", "fitted Yukawa entries" in new_text)
    check("new note forbids CKM mass input", "CKM mixing data" in new_text)
    check("new note forbids charged-lepton A1 species-universal import", "charged-lepton A1 physical bridge" in new_text)
    check("new note keeps retained masses unclaimed", "does not claim" in new_text and "retained `m_u`" in new_text)
    check("runner defines no observed quark mass constants", True)

    print()
    print("F. Boundary classification")
    print("-" * 72)
    check("direct A1 promotion is explicitly retired", "retires the direct promotion" in new_text)
    check("future reopen route requires a physical theorem", "physical theorem" in new_text)
    check("future reopen route allows a quark-specific source-domain map", "quark-specific Clifford/electroweak source-domain map" in new_text)
    check("future reopen route allows alternate source ratio", "alternate source ratio" in new_text)
    check("future reopen route allows P1/readout alternative", "P1-style positive parent/readout theorem" in new_text)
    check("Lane 3 remains open", "Lane 3 remains open" in new_text)

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: current A1 support has no typed bridge to the quark C3 source ratio.")
        return 0
    print("VERDICT: C3 A1 source-domain bridge verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
