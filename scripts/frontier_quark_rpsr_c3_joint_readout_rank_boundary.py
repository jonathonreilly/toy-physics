#!/usr/bin/env python3
"""Lane 3 RPSR-C3 joint up-type readout rank boundary.

This block-12 runner tests whether combining the exact STRC/RPSR reduced
up-amplitude scalar with the exact C3[111] Hermitian Ward carrier determines
the two independent up-type Yukawa ratios. It verifies the carrier inverse map
and then shows that one-scalar RPSR constraints still leave a one-parameter
family of C3-representable ordered ratio triples.

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
TOL = 1.0e-10


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

    queue: deque[str] = deque([start])
    seen = {start}
    while queue:
        node = queue.popleft()
        if node == goal:
            return True
        for nxt in graph.get(node, ()):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False


def c3_cycle() -> np.ndarray:
    return np.array(
        [
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=complex,
    )


def w_c3(a_coeff: float, b_coeff: float, c_coeff: float) -> np.ndarray:
    cycle = c3_cycle()
    cycle2 = cycle @ cycle
    ident = np.eye(3, dtype=complex)
    splitter = (cycle - cycle2) / (1j * math.sqrt(3.0))
    return a_coeff * ident + b_coeff * (cycle + cycle2) + c_coeff * splitter


def lambdas_from_coeffs(a_coeff: float, b_coeff: float, c_coeff: float) -> tuple[float, float, float]:
    return (
        a_coeff + 2.0 * b_coeff,
        a_coeff - b_coeff + c_coeff,
        a_coeff - b_coeff - c_coeff,
    )


def coeffs_from_lambdas(lambdas: tuple[float, float, float]) -> tuple[float, float, float]:
    l0, lp, lm = lambdas
    a_coeff = (l0 + lp + lm) / 3.0
    b_coeff = (2.0 * l0 - lp - lm) / 6.0
    c_coeff = (lp - lm) / 2.0
    return a_coeff, b_coeff, c_coeff


def rpsr_amplitude() -> float:
    return math.sqrt(5.0 / 6.0) * (1.0 - 48.0 / (49.0 * math.sqrt(42.0)))


def ratio_triple(r_uc: float, r_ct: float) -> tuple[float, float, float]:
    return (r_uc * r_ct, r_ct, 1.0)


def ratio_pair(triple: tuple[float, float, float]) -> tuple[float, float]:
    y_u, y_c, y_t = triple
    return y_u / y_c, y_c / y_t


def is_ordered_positive(triple: tuple[float, float, float]) -> bool:
    y_u, y_c, y_t = triple
    return 0.0 < y_u <= y_c <= y_t


def reconstructs(triple: tuple[float, float, float]) -> bool:
    coeffs = coeffs_from_lambdas(triple)
    closed = lambdas_from_coeffs(*coeffs)
    matrix = w_c3(*coeffs)
    eigs = tuple(float(x) for x in np.linalg.eigvalsh(matrix))
    return (
        all(abs(closed[i] - triple[i]) < TOL for i in range(3))
        and np.allclose(sorted(eigs), sorted(triple), atol=TOL)
    )


def main() -> int:
    print("=" * 88)
    print("LANE 3 RPSR-C3 JOINT READOUT RANK BOUNDARY")
    print("=" * 88)

    new_note = DOCS / "QUARK_RPSR_C3_JOINT_READOUT_RANK_BOUNDARY_NOTE_2026-04-28.md"
    block11_note = DOCS / "QUARK_RPSR_SINGLE_SCALAR_READOUT_UNDERDETERMINATION_NOTE_2026-04-28.md"
    block10_note = DOCS / "QUARK_UP_AMPLITUDE_RPSR_MASS_RETENTION_BOUNDARY_NOTE_2026-04-28.md"
    c3_note = DOCS / "QUARK_C3_ORIENTED_WARD_SPLITTER_SUPPORT_NOTE_2026-04-28.md"
    circulant_note = DOCS / "QUARK_C3_CIRCULANT_SOURCE_LAW_BOUNDARY_NOTE_2026-04-28.md"
    one_higgs_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"
    firewall_note = DOCS / "QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md"

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for path in (
        new_note,
        block11_note,
        block10_note,
        c3_note,
        circulant_note,
        one_higgs_note,
        firewall_note,
    ):
        check(f"{path.name} exists", path.exists(), str(path.relative_to(ROOT)))

    new_text = read(new_note)
    block11_text = read(block11_note)
    block10_text = read(block10_note)
    c3_text = read(c3_note)
    circulant_text = read(circulant_note)
    one_higgs_text = read(one_higgs_note)
    firewall_text = read(firewall_note)

    check("new note states joint rank boundary", "joint readout rank boundary" in new_text)
    check("block11 states single-scalar underdetermination", "single-scalar readout underdetermination" in block11_text)
    check("block10 states exact RPSR scalar", "sqrt(5/6) * (1 - 48" in block10_text)
    check("C3 note states exact normal form", "W(a,b,c)" in c3_text and "a I + b" in c3_text)
    check("C3 note leaves coefficients free", "coefficients" in c3_text and "remain free" in c3_text)
    check("circulant note says carrier can fit arbitrary triples", "arbitrary real generation spectrum" in circulant_text or "fit any real" in circulant_text)
    check("one-Higgs note leaves generation matrices free", "generation matrices remain" in one_higgs_text.lower() or "generation matrices" in one_higgs_text)
    check("firewall blocks mass retention shortcut", "not a retained" in firewall_text and "five-mass closure" in firewall_text)

    print()
    print("B. Exact RPSR scalar and C3 inverse map")
    print("-" * 72)
    a_u = rpsr_amplitude()
    rho = 1.0 / math.sqrt(42.0)
    sin_d = math.sqrt(5.0 / 6.0)
    lhs = a_u / sin_d + rho
    rhs = 1.0 + rho / 49.0
    check("RPSR scalar lies in (0,1)", 0.0 < a_u < 1.0, f"a_u={a_u:.12f}")
    check("RPSR identity closes", abs(lhs - rhs) < TOL, f"lhs={lhs:.12f}, rhs={rhs:.12f}")

    cycle = c3_cycle()
    ident = np.eye(3, dtype=complex)
    check("C3 cycle is unitary", np.allclose(cycle.conj().T @ cycle, ident))
    check("C3 cycle has order 3", np.allclose(cycle @ cycle @ cycle, ident))

    sample_coeffs = (1.4, -0.2, 0.35)
    sample_lambdas = lambdas_from_coeffs(*sample_coeffs)
    recovered_coeffs = coeffs_from_lambdas(sample_lambdas)
    sample_matrix = w_c3(*sample_coeffs)
    check("C3 sample is Hermitian", np.allclose(sample_matrix.conj().T, sample_matrix))
    check("C3 sample commutes with C3 cycle", np.max(np.abs(sample_matrix @ cycle - cycle @ sample_matrix)) < TOL)
    check("lambda->coefficient inverse recovers sample", all(abs(sample_coeffs[i] - recovered_coeffs[i]) < TOL for i in range(3)))
    check("sample matrix eigenvalues match closed form", np.allclose(sorted(np.linalg.eigvalsh(sample_matrix)), sorted(sample_lambdas)))

    arbitrary_triples = (
        (0.12, 0.42, 1.0),
        (0.25, 0.50, 1.0),
        (0.70, 0.88, 1.0),
    )
    for idx, triple in enumerate(arbitrary_triples, start=1):
        check(f"arbitrary triple {idx} is ordered positive", is_ordered_positive(triple), str(triple))
        check(f"arbitrary triple {idx} has exact C3 coefficients", reconstructs(triple))

    print()
    print("C. Two-ratio surface rank")
    print("-" * 72)
    pair_a = (0.25, 0.50)
    pair_b = (0.40, 0.50)
    pair_c = (0.25, 0.75)
    triple_a = ratio_triple(*pair_a)
    triple_b = ratio_triple(*pair_b)
    triple_c = ratio_triple(*pair_c)
    check("ratio triple reconstruction preserves pair A", all(abs(ratio_pair(triple_a)[i] - pair_a[i]) < TOL for i in range(2)))
    check("changing r_uc changes y_u/y_t at fixed r_ct", abs(triple_a[0] - triple_b[0]) > 1.0e-6)
    check("changing r_ct changes both y_u/y_t and y_c/y_t", abs(triple_a[0] - triple_c[0]) > 1.0e-6 and abs(triple_a[1] - triple_c[1]) > 1.0e-6)
    log_coords = (math.log(pair_a[0]), math.log(pair_a[1]))
    check("two-ratio surface has two log coordinates", len(log_coords) == 2 and log_coords[0] != log_coords[1])
    check("C3 carrier represents pair A", reconstructs(triple_a))
    check("C3 carrier represents pair B", reconstructs(triple_b))
    check("C3 carrier represents pair C", reconstructs(triple_c))
    check("new note names two independent ratios", "two independent positive ratios" in new_text)

    print()
    print("D. One-scalar RPSR constraints leave families")
    print("-" * 72)
    product_family_t = (0.80, 0.90, 0.98)
    product_pairs: list[tuple[float, float]] = []
    for idx, t_value in enumerate(product_family_t, start=1):
        r_ct = t_value
        r_uc = a_u / t_value
        triple = ratio_triple(r_uc, r_ct)
        product_pairs.append((r_uc, r_ct))
        check(f"product-family {idx} fixes y_u/y_t=a_u", abs(triple[0] - a_u) < TOL)
        check(f"product-family {idx} is ordered positive", is_ordered_positive(triple), str(triple))
        check(f"product-family {idx} has exact C3 coefficients", reconstructs(triple))
        check(f"product-family {idx} preserves ratios", abs(ratio_pair(triple)[0] - r_uc) < TOL and abs(ratio_pair(triple)[1] - r_ct) < TOL)

    middle_family_s = (0.20, 0.50, 0.90)
    middle_pairs: list[tuple[float, float]] = []
    for idx, s_value in enumerate(middle_family_s, start=1):
        r_uc = s_value
        r_ct = a_u
        triple = ratio_triple(r_uc, r_ct)
        middle_pairs.append((r_uc, r_ct))
        check(f"middle-family {idx} fixes y_c/y_t=a_u", abs(triple[1] - a_u) < TOL)
        check(f"middle-family {idx} is ordered positive", is_ordered_positive(triple), str(triple))
        check(f"middle-family {idx} has exact C3 coefficients", reconstructs(triple))
        check(f"middle-family {idx} preserves ratios", abs(ratio_pair(triple)[0] - r_uc) < TOL and abs(ratio_pair(triple)[1] - r_ct) < TOL)

    product_unique = {tuple(round(x, 12) for x in pair) for pair in product_pairs}
    middle_unique = {tuple(round(x, 12) for x in pair) for pair in middle_pairs}
    check("product one-scalar constraint leaves multiple ratio pairs", len(product_unique) == len(product_pairs))
    check("middle-gap one-scalar constraint leaves multiple ratio pairs", len(middle_unique) == len(middle_pairs))
    check("new note states one scalar fixes at most one relation", "one scalar" in new_text and "at\nmost one" in new_text and "one relation" in new_text)
    check("new note says C3 carrier does not remove missing readout law", "does not remove the missing RPSR" in new_text)

    print()
    print("E. Typed-edge boundary")
    print("-" * 72)
    existing_edges: set[tuple[str, str]] = {
        ("RPSR_reduced_amplitude", "up_amplitude_support"),
        ("C3_oriented_splitter", "C3_Fourier_carrier"),
        ("C3_Fourier_carrier", "arbitrary_ratio_representation"),
        ("top_Ward_anchor", "top_scale_anchor"),
        ("one_Higgs_gauge_selection", "Yukawa_operator_skeleton"),
        ("CKM_atlas", "mixing_support"),
    }
    target = "physical_up_yukawa_ratio_pair"
    check("RPSR reaches amplitude support", has_path(existing_edges, "RPSR_reduced_amplitude", "up_amplitude_support"))
    check("C3 reaches carrier representation", has_path(existing_edges, "C3_oriented_splitter", "arbitrary_ratio_representation"))
    check("RPSR alone does not reach ratio pair", not has_path(existing_edges, "RPSR_reduced_amplitude", target))
    check("C3 carrier alone does not reach ratio pair", not has_path(existing_edges, "C3_oriented_splitter", target))
    check("top scale alone does not reach ratio pair", not has_path(existing_edges, "top_Ward_anchor", target))
    proposed_edges = set(existing_edges)
    proposed_edges.update(
        {
            ("RPSR_reduced_amplitude", "C3_coefficient_source_law"),
            ("C3_coefficient_source_law", "C3_channel_assignment"),
            ("C3_channel_assignment", "sector_scale_bridge"),
            ("sector_scale_bridge", target),
        }
    )
    check("adding source law and assignment creates ratio path", has_path(proposed_edges, "RPSR_reduced_amplitude", target))
    check("missing source law is named as retained content", "retained source law for the C3 coefficients" in new_text)

    print()
    print("F. Import firewall")
    print("-" * 72)
    allowed_inputs = {
        "RPSR_reduced_amplitude",
        "C3_normal_form",
        "top_scale_normalization",
        "scale_covariance",
        "finite_dimensional_spectral_algebra",
    }
    forbidden_inputs = {
        "observed_quark_masses",
        "fitted_yukawa_entries",
        "CKM_singular_values_as_masses",
        "hidden_C3_source_law",
        "hidden_generation_gap_assignment",
        "one_scalar_as_two_coordinate_readout",
    }
    script_text = read(SCRIPTS / "frontier_quark_rpsr_c3_joint_readout_rank_boundary.py")
    mass_table_token = "P" + "DG"
    forbidden_numeric_tokens = ("2." + "16", "1." + "27", "172." + "76", "4." + "18")
    check("allowed and forbidden input sets are disjoint", allowed_inputs.isdisjoint(forbidden_inputs))
    check("new note forbids observed quark masses", "observed quark masses" in new_text and "Forbidden proof inputs" in new_text)
    check("new note forbids fitted Yukawa entries", "fitted Yukawa entries" in new_text)
    check("new note forbids CKM singular values", "CKM singular" in new_text)
    check("new note forbids hidden C3 source law", "hidden C3 source law" in new_text)
    check("new note forbids hidden generation-gap assignment", "hidden generation-gap assignment" in new_text)
    check("runner contains no named mass-table import", mass_table_token not in script_text)
    check("runner contains no observed mass constants", all(token not in script_text for token in forbidden_numeric_tokens))

    print()
    print("G. Boundary classification")
    print("-" * 72)
    check("new note retires joint shortcut", "retires the joint shortcut" in new_text)
    check("new note keeps both support surfaces", "does not retire either support surface" in new_text)
    check("new note requires C3 coefficient law", "C3 coefficient law" in new_text)
    check("new note requires physical channel assignment", "physical channel assignment" in new_text)
    check("new note requires top-compatible bridge", "top-compatible sector/scale bridge" in new_text)
    check("new note keeps Lane 3 open", "Lane 3 remains open" in new_text)
    check("new note does not claim retained up masses", "does not claim retained" in new_text)

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: exact RPSR plus exact C3 is carrier support, not retained")
        print("up-type two-ratio readout closure without a new source/readout theorem.")
        return 0
    print("VERDICT: RPSR-C3 joint readout rank verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
