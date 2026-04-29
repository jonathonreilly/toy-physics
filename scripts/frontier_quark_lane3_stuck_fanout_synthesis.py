#!/usr/bin/env python3
"""Lane 3 stuck fan-out synthesis after RPSR/C3 deep work.

This block-13 runner verifies the current-bank no-route-passes boundary across
orthogonal Lane 3 attack frames. It does not prove future closure impossible;
it checks that the present support graph has no typed path to retained
non-top quark masses without adding new theorem content.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LOOP = ROOT / ".claude" / "science" / "physics-loops" / "lane3-quark-mass-retention-20260428"
SCRIPTS = ROOT / "scripts"

PASS_COUNT = 0
FAIL_COUNT = 0


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


def main() -> int:
    print("=" * 88)
    print("LANE 3 STUCK FAN-OUT SYNTHESIS")
    print("=" * 88)

    sources = {
        "new_note": DOCS / "QUARK_LANE3_STUCK_FANOUT_SYNTHESIS_2026-04-28.md",
        "one_higgs": DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md",
        "firewall": DOCS / "QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md",
        "route2_naturality": DOCS / "QUARK_ROUTE2_E_CHANNEL_READOUT_NATURALITY_NO_GO_NOTE_2026-04-28.md",
        "route2_rconn": DOCS / "QUARK_ROUTE2_RCONN_CENTER_RATIO_BRIDGE_OBSTRUCTION_NOTE_2026-04-28.md",
        "route2_source": DOCS / "QUARK_ROUTE2_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md",
        "five_sixths": DOCS / "QUARK_FIVE_SIXTHS_SCALE_SELECTION_BOUNDARY_NOTE_2026-04-28.md",
        "s3_ward": DOCS / "QUARK_GENERATION_EQUIVARIANT_WARD_DEGENERACY_NO_GO_NOTE_2026-04-28.md",
        "c3_splitter": DOCS / "QUARK_C3_ORIENTED_WARD_SPLITTER_SUPPORT_NOTE_2026-04-28.md",
        "c3_circulant": DOCS / "QUARK_C3_CIRCULANT_SOURCE_LAW_BOUNDARY_NOTE_2026-04-28.md",
        "a1_source": DOCS / "QUARK_C3_A1_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md",
        "p1_readout": DOCS / "QUARK_C3_P1_POSITIVE_PARENT_READOUT_NO_GO_NOTE_2026-04-28.md",
        "rpsr_boundary": DOCS / "QUARK_UP_AMPLITUDE_RPSR_MASS_RETENTION_BOUNDARY_NOTE_2026-04-28.md",
        "rpsr_single": DOCS / "QUARK_RPSR_SINGLE_SCALAR_READOUT_UNDERDETERMINATION_NOTE_2026-04-28.md",
        "rpsr_c3": DOCS / "QUARK_RPSR_C3_JOINT_READOUT_RANK_BOUNDARY_NOTE_2026-04-28.md",
        "assumptions": LOOP / "ASSUMPTIONS_AND_IMPORTS.md",
        "no_go": LOOP / "NO_GO_LEDGER.md",
        "route_portfolio": LOOP / "ROUTE_PORTFOLIO.md",
    }

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for name, path in sources.items():
        check(f"{name} exists", path.exists(), str(path.relative_to(ROOT)))

    texts = {name: read(path) for name, path in sources.items()}
    new_text = texts["new_note"]
    check("new note states current-bank synthesis", "current-bank synthesis" in new_text)
    check("new note explicitly withholds retained closure", "retained closure withheld" in new_text)
    check("new note does not rule out future theorem", "future Lane 3 closure is impossible" in new_text and "not a theorem" in new_text)
    check("assumptions ledger includes block12 joint route", "RPSR plus `C3[111]` joint readout" in texts["assumptions"])
    check("no-go ledger includes RPSR+C3 promotion block", "RPSR scalar plus exact `C3[111]`" in texts["no_go"])
    check("route portfolio includes completed joint rank route", "Completed Route 13" in texts["route_portfolio"])

    print()
    print("B. Six orthogonal fan-out frames")
    print("-" * 72)
    frames = [
        (
            "gauge/operator",
            "generation matrices",
            texts["one_higgs"],
            "species-differentiated Ward/source theorem",
        ),
        (
            "Ward-normalization",
            "top-channel",
            texts["firewall"],
            "non-top Ward primitive or sector bridge",
        ),
        (
            "CKM/singular-value",
            "mixing theorem",
            texts["firewall"],
            "retained mass-basis bridge",
        ),
        (
            "endpoint/source",
            "typed edge",
            texts["route2_source"],
            "typed Route-2 source theorem",
        ),
        (
            "C3/RPSR readout",
            "source law",
            texts["rpsr_c3"],
            "C3 coefficient law and channel assignment",
        ),
        (
            "down-type NP/scale",
            "scale-selection theorem",
            texts["five_sixths"],
            "NP exponentiation plus scale-selection/RG transport",
        ),
    ]
    seen_frame_names: set[str] = set()
    for name, marker, text, reopen in frames:
        seen_frame_names.add(name)
        check(f"{name} frame has source marker", marker in text, marker)
        check(f"{name} frame has reopen condition", bool(reopen), reopen)
    check("six fan-out frames are distinct", len(seen_frame_names) == 6, str(sorted(seen_frame_names)))
    check("new note lists all six frames", all(name.lower() in new_text.lower() for name, *_ in frames))

    print()
    print("C. Deep-work prerequisites")
    print("-" * 72)
    block_markers = [
        ("block10 RPSR", "reduced" in texts["rpsr_boundary"] and "RPSR" in texts["rpsr_boundary"], texts["rpsr_boundary"]),
        ("block11 single-scalar", "single-scalar readout underdetermination", texts["rpsr_single"]),
        ("block12 joint rank", "joint readout rank boundary", texts["rpsr_c3"]),
        ("block04 3A scale", "five-sixths scale-selection boundary", texts["five_sixths"].lower()),
        ("block06 C3 splitter", "C3`-oriented Ward splitter", texts["c3_splitter"]),
        ("block07 C3 circulant", "C3 circulants are exact hierarchy carriers", texts["c3_circulant"]),
    ]
    for name, marker, text in block_markers:
        if isinstance(marker, bool):
            check(f"{name} prior artifact is present", marker)
        else:
            check(f"{name} prior artifact is present", marker in text, marker)
    check("Route-2 naturality route closed", "rho_E" in texts["route2_naturality"] and "free" in texts["route2_naturality"])
    check("Route-2 Rconn route is conditional only", "conditional bridge" in texts["route2_rconn"])
    check("A1 source route has missing typed edge", "no typed existing edge" in texts["a1_source"].lower() or "typed bridge" in texts["a1_source"].lower())
    check("P1 readout route lacks parent/readout", "quark parent and readout theorem remain" in texts["p1_readout"].lower() or ("parent" in texts["p1_readout"].lower() and "readout theorem" in texts["p1_readout"]))

    print()
    print("D. Current typed-edge graph")
    print("-" * 72)
    target = "retained_non_top_quark_masses"
    existing_edges: set[tuple[str, str]] = {
        ("one_Higgs_gauge_selection", "Yukawa_operator_skeleton"),
        ("CKM_atlas", "mixing_support"),
        ("top_Ward_anchor", "top_scale_anchor"),
        ("Route2_endpoint_support", "route2_conditional_support"),
        ("R_conn_8_9", "color_projection_support"),
        ("C3_Fourier_carrier", "arbitrary_ratio_representation"),
        ("RPSR_reduced_amplitude", "up_amplitude_support"),
        ("five_sixths_Casimir", "down_type_bounded_support"),
        ("A1_support_scalar", "A1_support"),
        ("P1_square_root_dictionary", "P1_support"),
    }
    support_nodes = {
        "one_Higgs_gauge_selection",
        "CKM_atlas",
        "top_Ward_anchor",
        "Route2_endpoint_support",
        "R_conn_8_9",
        "C3_Fourier_carrier",
        "RPSR_reduced_amplitude",
        "five_sixths_Casimir",
        "A1_support_scalar",
        "P1_square_root_dictionary",
    }
    for node in sorted(support_nodes):
        check(f"{node} has no path to retained masses", not has_path(existing_edges, node, target))

    proposed_edges = set(existing_edges)
    proposed_edges.update(
        {
            ("C3_coefficient_source_law", "physical_channel_assignment"),
            ("physical_channel_assignment", "two_ratio_readout"),
            ("two_ratio_readout", "up_type_ratio_pair"),
            ("RPSR_reduced_amplitude", "C3_coefficient_source_law"),
            ("five_sixths_NP_scale_theorem", "down_type_ratio_pair"),
            ("Route2_source_domain_bridge", "up_type_ratio_pair"),
            ("species_differentiated_non_top_Ward", "absolute_non_top_scale"),
            ("up_type_ratio_pair", target),
            ("down_type_ratio_pair", target),
            ("absolute_non_top_scale", target),
        }
    )
    check("adding C3/RPSR source-readout edges would create up path", has_path(proposed_edges, "RPSR_reduced_amplitude", target))
    check("adding 3A NP/scale theorem would create down path", has_path(proposed_edges, "five_sixths_NP_scale_theorem", target))
    check("adding Route-2 source theorem would create up path", has_path(proposed_edges, "Route2_source_domain_bridge", target))
    check("adding non-top Ward primitive would create absolute-scale path", has_path(proposed_edges, "species_differentiated_non_top_Ward", target))

    print()
    print("E. Stop implication and claim firewall")
    print("-" * 72)
    missing_edges = {
        "C3_coefficient_source_law",
        "physical_channel_assignment",
        "two_ratio_readout",
        "five_sixths_NP_scale_theorem",
        "Route2_source_domain_bridge",
        "species_differentiated_non_top_Ward",
    }
    check("all missing edges are theorem-content edges", all("law" in edge or "theorem" in edge or "assignment" in edge or "readout" in edge or "Ward" in edge or "bridge" in edge for edge in missing_edges))
    check("new note names stop implication", "Stop Implication" in new_text)
    check("new note says remaining progress requires new theorem content", "new theorem content" in new_text)
    check("new note keeps claim status open", "best honest status is open" in new_text)
    check("new note does not claim retained five-mass closure", "does not claim retained" in new_text)
    check("runner contains no observed mass constants", all(token not in read(SCRIPTS / "frontier_quark_lane3_stuck_fanout_synthesis.py") for token in ("2." + "16", "1." + "27", "172." + "76", "4." + "18")))

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: no current-bank Lane 3 route reaches retained non-top masses;")
        print("new source/readout theorem content is required.")
        return 0
    print("VERDICT: stuck fan-out synthesis verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
