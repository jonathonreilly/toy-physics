#!/usr/bin/env python3
"""Memory-feasibility probe for the wave-retardation static/comparator lane.

This is a planning probe, not a physics result.

Goal:
  Estimate how the current continuum harness scales in memory as H gets
  smaller, and compare the current Python-native approach to reduced-memory
  routes:

  - current Python-native dense history + adjacency map
  - packed sparse adjacency (CSR-like topology only)
  - matrix-free / streamed static solve (no cached full history)

The probe uses the same coarse geometry assumptions as
`wave_retardation_continuum_limit.py`:
  - T_phys = 15.0
  - PW_phys = 6.0
  - source travels from z=3.0 to z=0.0
  - max neighbor reach in the grown DAG = 3 physical units

The output is intended to answer one concrete question:

  "What is the cheapest feasible refinement path for pushing the
  retardation continuum lane further?"

The script prints:
  - lattice counts for candidate H values
  - estimated memory for the current Python-native representation
  - estimated memory for a packed sparse route
  - estimated memory for a matrix-free streamed route
  - a recommendation based on a user-supplied budget

No existing repo files are modified by this probe.
"""

from __future__ import annotations

import argparse
import math
import struct
import sys
from dataclasses import dataclass


T_PHYS = 15.0
PW_PHYS = 6.0
IZ_START_PHYS = 3.0
IZ_END_PHYS = 0.0
SRC_LAYER_FRAC = 1.0 / 3.0
MAX_D_PHYS = 3.0


PTR_BYTES = struct.calcsize("P")
FLOAT_BYTES = sys.getsizeof(0.0)
INT_BYTES = sys.getsizeof(0)
TUPLE3_BYTES = sys.getsizeof((0.0, 0.0, 0.0))
LIST_BYTES = sys.getsizeof([])
DICT_BYTES = sys.getsizeof({})


@dataclass(frozen=True)
class ProbeRow:
    h: float
    nl: int
    hw: int
    nw: int
    nodes: int
    slice_cells: int
    md: int
    avg_deg: int
    edges_est: int
    current_python_bytes: int
    sparse_packed_bytes: int
    matrix_free_packed_bytes: int


def mib(nbytes: int) -> float:
    return nbytes / (1024.0 * 1024.0)


def counts_for_h(h: float) -> tuple[int, int, int, int, int, int, int, int]:
    """Return NL, hw, nw, nodes, slice_cells, md, avg_deg, edge_est."""
    nl = max(3, round(T_PHYS / h))
    hw = int(PW_PHYS / h)
    nw = 2 * hw + 1
    slice_cells = nw * nw
    nodes = 1 + (nl - 1) * slice_cells
    md = max(1, round(MAX_D_PHYS / h))
    avg_deg = (2 * md + 1) ** 2
    edges_est = (nl - 1) * slice_cells * avg_deg
    return nl, hw, nw, nodes, slice_cells, md, avg_deg, edges_est


def estimate_python_current_bytes(
    nodes: int, nw: int, nl: int, edges_est: int
) -> int:
    """Estimate the current Python-native representation.

    This models:
      - positions as a list of 3-float tuples
      - history as NL nested Python lists of Python floats
      - adjacency as dict[int, list[int]]

    It is intentionally conservative. The goal is to show the order
    of magnitude, not the exact resident set size.
    """
    pos_bytes = LIST_BYTES + nodes * PTR_BYTES + nodes * (TUPLE3_BYTES + 3 * FLOAT_BYTES)
    slice_bytes = LIST_BYTES + nw * (LIST_BYTES + nw * (FLOAT_BYTES + PTR_BYTES))
    history_bytes = nl * slice_bytes

    source_nodes = max(0, nodes - nw * nw)
    # One dict entry per source node, one list object per source node,
    # and one Python int object per stored edge.
    adj_bytes = (
        DICT_BYTES
        + source_nodes * (INT_BYTES + PTR_BYTES + LIST_BYTES)
        + edges_est * (INT_BYTES + PTR_BYTES)
    )
    return pos_bytes + history_bytes + adj_bytes


def estimate_sparse_packed_bytes(nodes: int, edges_est: int) -> int:
    """Estimate a compact CSR-like topology with 32-bit indices."""
    # indptr (nodes + 1) and indices (edges)
    return 4 * (nodes + 1 + edges_est)


def estimate_matrix_free_packed_bytes(nodes: int, slice_cells: int) -> int:
    """Estimate a streamed matrix-free route using packed double buffers.

    Two field buffers plus one work buffer is a good upper bound for a
    streamed static solve or direct matrix-free comparator.
    """
    field_buffers = 3 * slice_cells * 8
    # Positions are still needed by the beam propagator, but adjacency is not.
    pos_bytes = LIST_BYTES + nodes * PTR_BYTES + nodes * (TUPLE3_BYTES + 3 * FLOAT_BYTES)
    return pos_bytes + field_buffers


def build_rows(h_values: list[float]) -> list[ProbeRow]:
    rows: list[ProbeRow] = []
    for h in h_values:
        nl, hw, nw, nodes, slice_cells, md, avg_deg, edges_est = counts_for_h(h)
        current_python_bytes = estimate_python_current_bytes(nodes, nw, nl, edges_est)
        sparse_packed_bytes = estimate_sparse_packed_bytes(nodes, edges_est)
        matrix_free_packed_bytes = estimate_matrix_free_packed_bytes(nodes, slice_cells)
        rows.append(
            ProbeRow(
                h=h,
                nl=nl,
                hw=hw,
                nw=nw,
                nodes=nodes,
                slice_cells=slice_cells,
                md=md,
                avg_deg=avg_deg,
                edges_est=edges_est,
                current_python_bytes=current_python_bytes,
                sparse_packed_bytes=sparse_packed_bytes,
                matrix_free_packed_bytes=matrix_free_packed_bytes,
            )
        )
    return rows


def format_row(row: ProbeRow) -> str:
    return (
        f"{row.h:>6.3f} {row.nl:>4d} {row.nw:>4d} {row.nodes:>10d} "
        f"{row.edges_est:>13d} {mib(row.current_python_bytes):>12.1f} "
        f"{mib(row.sparse_packed_bytes):>11.1f} {mib(row.matrix_free_packed_bytes):>13.1f}"
    )


def recommend(rows: list[ProbeRow], budget_mib: float) -> str:
    budget_bytes = int(budget_mib * 1024 * 1024)
    feasible = [row for row in rows if row.matrix_free_packed_bytes <= budget_bytes]
    if feasible:
        smallest = min(feasible, key=lambda r: r.h)
        return (
            f"matrix-free / streamed comparator is feasible through H={smallest.h:.3f} "
            f"under {budget_mib:.0f} MiB; do not use Python adjacency caching"
        )
    return (
        f"no candidate fits under {budget_mib:.0f} MiB with the current assumptions; "
        f"reduce H only after a matrix-free rewrite"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--budget-mib",
        type=float,
        default=2048.0,
        help="Memory budget used for the recommendation (MiB). Default: 2048",
    )
    parser.add_argument(
        "--hs",
        type=float,
        nargs="*",
        default=[0.5, 0.35, 0.25, 0.125],
        help="Candidate lattice spacings to estimate.",
    )
    args = parser.parse_args()

    rows = build_rows(args.hs)

    print("=" * 104)
    print("WAVE STATIC-SOLVER MEMORY FEASIBILITY PROBE")
    print("=" * 104)
    print(f"Physical setup: T_phys={T_PHYS}, PW_phys={PW_PHYS}, z:[{IZ_START_PHYS}→{IZ_END_PHYS}]")
    print(f"Current harness assumption: max neighbor reach = {MAX_D_PHYS} physical units")
    print(f"Python object sizes: float={FLOAT_BYTES}B, int={INT_BYTES}B, tuple3={TUPLE3_BYTES}B, ptr={PTR_BYTES}B")
    print(f"Recommendation budget: {args.budget_mib:.0f} MiB")
    print()
    print(
        f"{'H':>6s} {'NL':>4s} {'nw':>4s} {'nodes':>10s} {'edges~':>13s} "
        f"{'current_py MiB':>12s} {'packed_csr':>11s} {'matrix_free':>13s}"
    )
    print("-" * 104)
    for row in rows:
        print(format_row(row))

    print()
    print("Interpretation:")
    for row in rows:
        current = "OK" if row.current_python_bytes <= args.budget_mib * 1024 * 1024 else "OOM"
        sparse = "OK" if row.sparse_packed_bytes <= args.budget_mib * 1024 * 1024 else "OOM"
        mf = "OK" if row.matrix_free_packed_bytes <= args.budget_mib * 1024 * 1024 else "OOM"
        print(
            f"  H={row.h:.3f}: current_python={current}, packed_csr={sparse}, "
            f"matrix_free={mf}"
        )

    print()
    print("Cheapest feasible refinement path:")
    print(f"  {recommend(rows, args.budget_mib)}")
    print("  If the target is H=0.125, the dense Python adjacency route is not viable;")
    print("  matrix-free neighbor generation is the minimum structural change that")
    print("  removes the O(E) Python adjacency cost.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
