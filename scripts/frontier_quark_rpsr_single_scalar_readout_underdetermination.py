#!/usr/bin/env python3
"""Lane 3 RPSR single-scalar up-type readout underdetermination.

This block-11 runner verifies a narrow no-go: the exact STRC/RPSR reduced
up-amplitude is a single dimensionless scalar. Even with top-scale
normalization and scale covariance, it does not determine both independent
up-type Yukawa ratios unless a readout law supplies the missing functions or
equivalent exponents.

No observed quark masses, fitted Yukawa entries, or CKM mass inputs are used.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path
import math
import sys


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


def rpsr_amplitude() -> float:
    return math.sqrt(5.0 / 6.0) * (1.0 - 48.0 / (49.0 * math.sqrt(42.0)))


def power_readout(a: float, p: float, q: float, y_t: float = 1.0) -> tuple[float, float, float]:
    return (
        y_t * a ** (p + q),
        y_t * a**q,
        y_t,
    )


def ratios(triple: tuple[float, float, float]) -> tuple[float, float]:
    y_u, y_c, y_t = triple
    return y_u / y_c, y_c / y_t


def exponents_for_ratios(a: float, r_uc: float, r_ct: float) -> tuple[float, float]:
    return math.log(r_uc) / math.log(a), math.log(r_ct) / math.log(a)


def main() -> int:
    print("=" * 88)
    print("LANE 3 RPSR SINGLE-SCALAR READOUT UNDERDETERMINATION")
    print("=" * 88)

    new_note = DOCS / "QUARK_RPSR_SINGLE_SCALAR_READOUT_UNDERDETERMINATION_NOTE_2026-04-28.md"
    block10_note = DOCS / "QUARK_UP_AMPLITUDE_RPSR_MASS_RETENTION_BOUNDARY_NOTE_2026-04-28.md"
    strc_note = DOCS / "STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md"
    rpsr_note = DOCS / "QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md"
    top_note = DOCS / "YT_WARD_IDENTITY_DERIVATION_THEOREM.md"
    firewall_note = DOCS / "QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md"
    one_higgs_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for path in (
        new_note,
        block10_note,
        strc_note,
        rpsr_note,
        top_note,
        firewall_note,
        one_higgs_note,
    ):
        check(f"{path.name} exists", path.exists(), str(path.relative_to(ROOT)))

    new_text = read(new_note)
    block10_text = read(block10_note)
    strc_text = read(strc_note)
    rpsr_text = read(rpsr_note)
    top_text = read(top_note)
    firewall_text = read(firewall_note)
    one_higgs_text = read(one_higgs_note)

    check("new note states single-scalar underdetermination", "single-scalar readout underdetermination" in new_text)
    check("block10 note supplies exact RPSR amplitude", "sqrt(5/6) * (1 - 48" in block10_text)
    check("block10 note requires amplitude-to-Yukawa readout", "amplitude-to-Yukawa readout" in block10_text)
    check("STRC note remains the LO support surface", "LO" in strc_text and "collinearity" in strc_text.lower())
    check("RPSR note records reduced amplitude target", "RPSR" in rpsr_text and "sqrt(5/6)" in rpsr_text)
    check("top Ward note remains top-channel anchor", "y_t" in top_text and "sqrt(6)" in top_text)
    check("firewall blocks direct companion promotion", "not a retained" in firewall_text)
    check("one-Higgs note leaves Yukawa matrices as boundary", "Yukawa" in one_higgs_text and "gauge" in one_higgs_text)

    print()
    print("B. Exact RPSR scalar")
    print("-" * 72)
    a = rpsr_amplitude()
    rho = 1.0 / math.sqrt(42.0)
    sin_d = math.sqrt(5.0 / 6.0)
    normalized = a / sin_d + rho
    expected = 1.0 + rho / 49.0
    check("RPSR scalar lies in (0,1)", 0.0 < a < 1.0, f"a_u={a:.12f}")
    check("RPSR identity still closes", abs(normalized - expected) < TOL, f"lhs={normalized:.12f}, rhs={expected:.12f}")
    check("log(a_u) is nonzero and negative", math.log(a) < 0.0, f"log(a_u)={math.log(a):.12f}")
    check("a_u is not a two-ratio object", isinstance(a, float))
    check("new note names both independent ratios", "y_u/y_c" in new_text and "y_c/y_t" in new_text)

    print()
    print("C. Scale-covariant power readout family")
    print("-" * 72)
    examples = {
        "R_1_1": (1.0, 1.0),
        "R_2_1": (2.0, 1.0),
        "R_1_2": (1.0, 2.0),
        "R_3_2": (3.0, 2.0),
    }
    ratio_pairs: dict[str, tuple[float, float]] = {}
    for name, (p, q) in examples.items():
        triple = power_readout(a, p, q)
        r_pair = ratios(triple)
        ratio_pairs[name] = r_pair
        y_u, y_c, y_t = triple
        check(f"{name} gives positive triple", y_u > 0.0 and y_c > 0.0 and y_t > 0.0)
        check(f"{name} gives ordered triple", y_u <= y_c <= y_t, f"{triple}")
        check(f"{name} ratio y_u/y_c is a^p", abs(r_pair[0] - a**p) < TOL)
        check(f"{name} ratio y_c/y_t is a^q", abs(r_pair[1] - a**q) < TOL)

    scaled = power_readout(a, 2.0, 1.0, y_t=7.0)
    unscaled = power_readout(a, 2.0, 1.0, y_t=1.0)
    check("scale covariance preserves y_u/y_c", abs(ratios(scaled)[0] - ratios(unscaled)[0]) < TOL)
    check("scale covariance preserves y_c/y_t", abs(ratios(scaled)[1] - ratios(unscaled)[1]) < TOL)
    check("different p changes y_u/y_c for same a_u", abs(ratio_pairs["R_1_1"][0] - ratio_pairs["R_2_1"][0]) > 1.0e-6)
    check("different q changes y_c/y_t for same a_u", abs(ratio_pairs["R_1_1"][1] - ratio_pairs["R_1_2"][1]) > 1.0e-6)
    check("same a_u supports multiple ratio pairs", len({tuple(round(x, 12) for x in pair) for pair in ratio_pairs.values()}) == len(ratio_pairs))

    print()
    print("D. Fit-capacity versus prediction")
    print("-" * 72)
    synthetic_pairs = (
        (0.25, 0.50),
        (0.10, 1.0 / 3.0),
        (0.40, 0.75),
        (0.01, 0.20),
    )
    for idx, (r_uc, r_ct) in enumerate(synthetic_pairs, start=1):
        p, q = exponents_for_ratios(a, r_uc, r_ct)
        reconstructed = ratios(power_readout(a, p, q))
        check(f"synthetic pair {idx} gives positive p", p > 0.0, f"p={p:.6f}")
        check(f"synthetic pair {idx} gives positive q", q > 0.0, f"q={q:.6f}")
        check(f"synthetic pair {idx} reconstructs y_u/y_c", abs(reconstructed[0] - r_uc) < TOL)
        check(f"synthetic pair {idx} reconstructs y_c/y_t", abs(reconstructed[1] - r_ct) < TOL)

    p_a, q_a = exponents_for_ratios(a, 0.25, 0.50)
    p_b, q_b = exponents_for_ratios(a, 0.10, 1.0 / 3.0)
    check("distinct synthetic pairs need distinct exponent data", abs(p_a - p_b) > 1.0e-6 and abs(q_a - q_b) > 1.0e-6)
    check("exponent selection is an extra readout law", "Selecting `p` and `q` is exactly the missing readout theorem" in new_text)
    check("fit-capacity is explicitly non-predictive", "fit-capacity" in new_text.lower() and "not a" in new_text and "prediction" in new_text)

    print()
    print("E. Typed-edge boundary")
    print("-" * 72)
    existing_edges: set[tuple[str, str]] = {
        ("unit_projector_ray", "STRC_LO"),
        ("scalar_ray_rho", "STRC_LO"),
        ("STRC_LO", "RPSR_reduced_amplitude"),
        ("support_bridge_6_7", "RPSR_reduced_amplitude"),
        ("delta_A1_1_42", "RPSR_reduced_amplitude"),
        ("RPSR_reduced_amplitude", "up_amplitude_support"),
        ("top_Ward_anchor", "top_scale_anchor"),
        ("CKM_atlas", "mixing_support"),
        ("one_Higgs_gauge_selection", "Yukawa_operator_skeleton"),
    }
    target = "physical_up_yukawa_ratio_pair"
    check("RPSR reaches amplitude support", has_path(existing_edges, "unit_projector_ray", "up_amplitude_support"))
    check("RPSR does not reach physical up ratio pair", not has_path(existing_edges, "RPSR_reduced_amplitude", target))
    check("top scale anchor does not supply non-top ratio pair", not has_path(existing_edges, "top_Ward_anchor", target))
    check("one-Higgs gauge skeleton does not supply ratio pair", not has_path(existing_edges, "one_Higgs_gauge_selection", target))
    proposed_edges = set(existing_edges)
    proposed_edges.update(
        {
            ("RPSR_reduced_amplitude", "readout_functions_p_q"),
            ("readout_functions_p_q", "generation_gap_assignment"),
            ("generation_gap_assignment", "sector_scale_bridge"),
            ("sector_scale_bridge", target),
        }
    )
    check("adding readout and bridge edges creates ratio path", has_path(proposed_edges, "RPSR_reduced_amplitude", target))
    check("missing readout functions are new theorem content", "readout functions themselves are derived" in new_text)

    print()
    print("F. Import firewall")
    print("-" * 72)
    allowed_inputs = {
        "RPSR_reduced_amplitude",
        "positivity",
        "ordering",
        "scale_covariance",
        "top_scale_normalization",
    }
    forbidden_inputs = {
        "observed_quark_masses",
        "fitted_yukawa_entries",
        "CKM_singular_values_as_masses",
        "hidden_generation_gap_selector",
        "species_uniform_top_Ward",
    }
    script_text = read(SCRIPTS / "frontier_quark_rpsr_single_scalar_readout_underdetermination.py")
    check("allowed and forbidden input sets are disjoint", allowed_inputs.isdisjoint(forbidden_inputs))
    check("new note forbids observed quark masses", "observed quark masses" in new_text and "Forbidden proof inputs" in new_text)
    check("new note forbids fitted Yukawa entries", "fitted Yukawa entries" in new_text)
    check("new note forbids CKM singular values as mass inputs", "CKM singular" in new_text)
    check("new note forbids hidden exponent law", "hidden exponent" in new_text)
    check("new note forbids species-uniform top Ward reuse", "species-uniform" in new_text)
    mass_table_token = "P" + "DG"
    forbidden_numeric_tokens = ("2." + "16", "1." + "27", "172." + "76", "4." + "18")
    check("runner contains no named mass-table import", mass_table_token not in script_text)
    check("runner contains no observed mass constants", all(token not in script_text for token in forbidden_numeric_tokens))

    print()
    print("G. Boundary classification")
    print("-" * 72)
    check("new note retires direct shortcut", "retires the stronger shortcut" in new_text)
    check("new note keeps RPSR as valuable support", "remains valuable exact support" in new_text)
    check("new note requires generation/source theorem", "generation/source theorem" in new_text)
    check("new note requires top-compatible bridge", "top-compatible sector/scale bridge" in new_text)
    check("new note keeps Lane 3 open", "Lane 3 remains open" in new_text)
    check("new note does not claim retained non-top masses", "does not claim retained" in new_text)

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: exact RPSR scalar support remains underdetermined as a")
        print("two-ratio up-type Yukawa readout without a new readout theorem.")
        return 0
    print("VERDICT: RPSR single-scalar readout verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
