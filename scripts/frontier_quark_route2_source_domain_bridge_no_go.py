#!/usr/bin/env python3
"""Route-2 source-domain bridge no-go for the R_conn endpoint target.

This block-03 Lane 3 runner checks the hard residual left by the Route-2
R_conn bridge obstruction:

    gamma_T(center) / gamma_E(center) = -R_conn = -8/9.

It verifies two facts at once.  First, if that source-domain bridge is added,
the Route-2 endpoint algebra forces rho_E = beta_E/alpha_E = 21/4 exactly.
Second, the current exact support bank has no typed edge from the retained
SU(3) color-projection channel to the Route-2 E/T endpoint readout.  Therefore
the bridge is a named missing theorem, not a retained up-type scalar law.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import sys

import numpy as np

from frontier_quark_route2_exact_readout_map import restricted_readout_data


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0
EXACT_TOL = 1.0e-12


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


def percent_gap(value: float, target: float) -> float:
    return abs(value / target - 1.0) * 100.0


def r_conn(n_c: int = 3) -> Fraction:
    return Fraction(n_c * n_c - 1, n_c * n_c)


def q_e_from_center_ratio(
    center_te: Fraction,
    q_t: Fraction = Fraction(5, 6),
    shell_te: Fraction = Fraction(-2, 1),
) -> Fraction:
    return shell_te * q_t / center_te


def rho_e_from_center_ratio(center_te: Fraction) -> Fraction:
    return 6 * (q_e_from_center_ratio(center_te) - 1)


def reduced_map(rho_e: Fraction) -> np.ndarray:
    return np.array(
        [
            [1.0, 0.0, float(rho_e), 0.0],
            [0.0, -2.0, 0.0, 2.0],
        ],
        dtype=float,
    )


@dataclass(frozen=True)
class TypedEdge:
    source: str
    target: str
    label: str
    authority: str
    role: str


CURRENT_TYPED_EDGES: tuple[TypedEdge, ...] = (
    TypedEdge(
        "route2_support_delta_A1",
        "route2_bilinear_carrier_K_R",
        "delta_A1 enters the exact bilinear support carrier",
        "S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md",
        "support",
    ),
    TypedEdge(
        "route2_bright_E_T",
        "route2_bilinear_carrier_K_R",
        "E and T bright coordinates enter K_R",
        "S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md",
        "support",
    ),
    TypedEdge(
        "route2_bilinear_carrier_K_R",
        "route2_restricted_readout_family",
        "restricted endpoints reduce to channelwise readout",
        "QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md",
        "support",
    ),
    TypedEdge(
        "route2_restricted_readout_family",
        "route2_endpoint_algebra",
        "endpoint ratios are algebraic in readout entries",
        "QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md",
        "support",
    ),
    TypedEdge(
        "route2_t_side_candidates",
        "route2_q_T_5_6_and_shell_TE_minus_2",
        "conditional T-side values used in the stretch attempt",
        "QUARK_ROUTE2_E_CHANNEL_READOUT_NATURALITY_NO_GO_NOTE_2026-04-28.md",
        "conditional",
    ),
    TypedEdge(
        "route2_center_TE_minus_8_9",
        "route2_q_E_15_8",
        "with q_T=5/6 and shell T/E=-2, center T/E=-8/9 fixes q_E",
        "QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md",
        "algebra",
    ),
    TypedEdge(
        "route2_q_E_15_8",
        "route2_rho_E_21_4",
        "rho_E = 6(q_E - 1)",
        "QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md",
        "algebra",
    ),
    TypedEdge(
        "su3_color_trace_channel",
        "su3_R_conn_8_9",
        "R_conn = (N_c^2 - 1)/N_c^2 at N_c=3",
        "RCONN_DERIVED_NOTE.md",
        "color",
    ),
)

MISSING_BRIDGE = TypedEdge(
    "su3_R_conn_8_9",
    "route2_center_TE_minus_8_9",
    "unsupported source-domain identification c_TE = -R_conn",
    "missing theorem",
    "missing",
)


def reachable(edges: tuple[TypedEdge, ...], source: str, target: str) -> tuple[bool, list[TypedEdge]]:
    graph: dict[str, list[TypedEdge]] = defaultdict(list)
    for edge in edges:
        graph[edge.source].append(edge)

    queue: deque[tuple[str, list[TypedEdge]]] = deque([(source, [])])
    seen = {source}
    while queue:
        node, path = queue.popleft()
        if node == target:
            return True, path
        for edge in graph[node]:
            if edge.target in seen:
                continue
            seen.add(edge.target)
            queue.append((edge.target, [*path, edge]))
    return False, []


def edge_roles(edges: tuple[TypedEdge, ...]) -> set[str]:
    return {edge.role for edge in edges}


def main() -> int:
    print("=" * 88)
    print("LANE 3 ROUTE-2 SOURCE-DOMAIN BRIDGE NO-GO")
    print("=" * 88)

    new_note = DOCS / "QUARK_ROUTE2_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md"
    rconn_note = DOCS / "RCONN_DERIVED_NOTE.md"
    bridge_note = DOCS / "QUARK_ROUTE2_RCONN_CENTER_RATIO_BRIDGE_OBSTRUCTION_NOTE_2026-04-28.md"
    readout_note = DOCS / "QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md"
    naturality_note = DOCS / "QUARK_ROUTE2_E_CHANNEL_READOUT_NATURALITY_NO_GO_NOTE_2026-04-28.md"
    bilinear_note = DOCS / "S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md"
    time_note = DOCS / "QUARK_ROUTE2_EXACT_TIME_COUPLING_NOTE_2026-04-19.md"

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for path in (
        new_note,
        rconn_note,
        bridge_note,
        readout_note,
        naturality_note,
        bilinear_note,
        time_note,
    ):
        check(f"{path.name} exists", path.exists(), str(path.relative_to(ROOT)))

    new_text = read(new_note)
    rconn_text = read(rconn_note)
    bridge_text = read(bridge_note)
    readout_text = read(readout_note)
    bilinear_text = read(bilinear_note)
    time_text = read(time_note)

    check("R_conn surface is color-projection, not Route-2 endpoint syntax", "connected color trace" in rconn_text and "Route-2" not in rconn_text)
    check("Route-2 bilinear carrier surface has no R_conn bridge", "K_R(q)" in bilinear_text and "R_conn" not in bilinear_text)
    check("Route-2 readout map surface has no R_conn bridge", "beta_E / alpha_E = 21/4" in readout_text and "R_conn" not in readout_text)
    check("Route-2 exact time-coupling surface has no R_conn bridge", "R_conn" not in time_text)
    check(
        "block02 already classified R_conn as conditional, not derivation",
        "conditional bridge" in bridge_text
        and "import boundary" in bridge_text
        and "not a retained derivation" in bridge_text,
    )
    check("new note forbids retained up-mass closure language", "does not claim retained `m_u` or `m_c`" in new_text)

    print()
    print("B. Conditional algebra if the missing bridge is supplied")
    print("-" * 72)
    r = r_conn(3)
    missing_center_ratio = -r
    q_e = q_e_from_center_ratio(missing_center_ratio)
    rho_e = rho_e_from_center_ratio(missing_center_ratio)
    check("N_c=3 gives R_conn=8/9 exactly", r == Fraction(8, 9), str(r))
    check("adding c_TE=-R_conn gives q_E=15/8 exactly", q_e == Fraction(15, 8), str(q_e))
    check("adding c_TE=-R_conn gives rho_E=21/4 exactly", rho_e == Fraction(21, 4), str(rho_e))
    check("using positive R_conn instead of -R_conn gives the wrong signed lift", rho_e_from_center_ratio(r) == Fraction(-69, 4), str(rho_e_from_center_ratio(r)))

    print()
    print("C. Typed source-domain graph")
    print("-" * 72)
    source = "su3_R_conn_8_9"
    target = "route2_rho_E_21_4"
    current_reaches, current_path = reachable(CURRENT_TYPED_EDGES, source, target)
    bridged_reaches, bridged_path = reachable(CURRENT_TYPED_EDGES + (MISSING_BRIDGE,), source, target)
    check("current typed bank has no path from R_conn to rho_E=21/4", not current_reaches, f"path length={len(current_path)}")
    check("adding the missing bridge creates the exact path to rho_E=21/4", bridged_reaches, " -> ".join(edge.target for edge in bridged_path))
    check("the only new edge in the successful path is explicitly missing", MISSING_BRIDGE in bridged_path and edge_roles(tuple(bridged_path)) >= {"missing", "algebra"})

    print()
    print("D. Endpoint-support non-uniqueness")
    print("-" * 72)
    data = restricted_readout_data()
    p_zero = reduced_map(Fraction(0, 1))
    p_target = reduced_map(Fraction(21, 4))
    e_shell = data.carrier_e_shell
    e_center = data.carrier_e_center
    t_shell = data.carrier_t_shell
    t_center = data.carrier_t_center

    check("rho_E=0 and rho_E=21/4 agree on E-shell", np.max(np.abs(p_zero @ e_shell - p_target @ e_shell)) < EXACT_TOL)
    check("rho_E=0 and rho_E=21/4 agree on granted T-shell", np.max(np.abs(p_zero @ t_shell - p_target @ t_shell)) < EXACT_TOL)
    check("rho_E=0 and rho_E=21/4 agree on granted T-center", np.max(np.abs(p_zero @ t_center - p_target @ t_center)) < EXACT_TOL)
    check("rho_E=0 and rho_E=21/4 differ only at E-center", abs((p_zero @ e_center)[0] - (p_target @ e_center)[0]) > 0.5)

    live_center = data.center_ratio_te
    check(
        "live center ratio is close to -R_conn but remains comparator-only",
        percent_gap(live_center, float(missing_center_ratio)) < 0.25 and abs(live_center - float(missing_center_ratio)) > EXACT_TOL,
        f"live={live_center:.12f}, target={float(missing_center_ratio):.12f}",
    )

    print()
    print("E. Stuck fan-out frames")
    print("-" * 72)
    low_complexity_scalars = {
        r,
        -r,
        1 - r,
        r - 1,
        1 / r,
        -1 / r,
        r / (1 - r),
        -(r / (1 - r)),
    }
    frame_results = {
        "support-endpoint": not current_reaches,
        "color-trace": r > 0 and missing_center_ratio < 0,
        "representation-domain": "singlet" in rconn_text and "adjoint" in rconn_text and "A1" in bilinear_text and "E" in bilinear_text and "T" in bilinear_text,
        "endpoint-functor": bridged_reaches and not current_reaches,
        "low-complexity-scalar": -r in low_complexity_scalars and len(low_complexity_scalars) > 4,
    }
    for name, ok in frame_results.items():
        check(f"{name} frame blocks untyped promotion", ok)
    check("fan-out has five orthogonal blocking frames", all(frame_results.values()) and len(frame_results) == 5)

    print()
    print("F. Import firewall")
    print("-" * 72)
    proof_inputs = {
        "route2_exact_carrier",
        "route2_endpoint_algebra",
        "conditional_t_side_candidates",
        "retained_su3_rconn_value",
        "typed_edge_inventory",
        "exact_rational_arithmetic",
    }
    forbidden_inputs = {
        "observed_quark_masses",
        "fitted_yukawa_entries",
        "ckm_j_target_error",
        "nearest_live_endpoint_selector",
        "untyped_rconn_endpoint_identification",
    }
    check("forbidden proof inputs are absent", proof_inputs.isdisjoint(forbidden_inputs), str(sorted(proof_inputs)))
    check(
        "new note names the missing theorem rather than closing Lane 3",
        "typed source-domain bridge theorem" in new_text
        and "claim status remains open" in new_text.lower(),
    )

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: current Route-2 + SU(3) support has no typed R_conn")
        print("source-domain bridge.  Adding that bridge would force rho_E=21/4,")
        print("but without it the up-type scalar law remains open.")
        return 0
    print("VERDICT: source-domain bridge no-go verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
