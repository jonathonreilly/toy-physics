#!/usr/bin/env python3
"""Matrix-free direct-static comparator probe for the wave-retardation lane.

This probe answers one narrow question:

  Can the exact discrete static comparator be solved at H = 0.125
  without the current Python adjacency / cached-state route?

It uses the same physical setup as the wave-retardation continuum lane,
but solves the finite (y, z) static problem directly with a matrix-free
red-black SOR iteration:

  lap(f) + src = 0

No cached adjacency map, no cached source-position history, no beam DAG
state beyond the current iterate. The probe reports:

  - rough memory estimates for the current Python route vs matrix-free
  - iteration count and residual for the direct static solve
  - a viability verdict for H = 0.125

The output is intended to compare iteration behavior against the direct
probe and answer whether the matrix-free route is feasible enough to
replace the current cached/static approach.
"""

from __future__ import annotations

import argparse
import math
import struct
from dataclasses import dataclass

T_PHYS = 15.0
PW_PHYS = 6.0
IZ_START_PHYS = 3.0
IZ_END_PHYS = 0.0
SRC_LAYER_FRAC = 1.0 / 3.0
MAX_D_PHYS = 3.0
S_PHYS = 0.004

PTR_BYTES = struct.calcsize("P")
FLOAT_BYTES = 24
INT_BYTES = 28
TUPLE3_BYTES = 64
LIST_BYTES = 56
DICT_BYTES = 64


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
    current_python_mib: float
    matrix_free_mib: float
    iterations: int
    residual: float
    runtime_s: float


def mib(nbytes: int) -> float:
    return nbytes / (1024.0 * 1024.0)


def counts_for_h(h: float) -> tuple[int, int, int, int, int, int, int, int]:
    nl = max(3, round(T_PHYS / h))
    hw = int(PW_PHYS / h)
    nw = 2 * hw + 1
    slice_cells = nw * nw
    nodes = 1 + (nl - 1) * slice_cells
    md = max(1, round(MAX_D_PHYS / h))
    avg_deg = (2 * md + 1) ** 2
    edges_est = (nl - 1) * slice_cells * avg_deg
    return nl, hw, nw, nodes, slice_cells, md, avg_deg, edges_est


def estimate_python_current_bytes(nodes: int, nw: int, nl: int, edges_est: int) -> int:
    pos_bytes = LIST_BYTES + nodes * PTR_BYTES + nodes * (TUPLE3_BYTES + 3 * FLOAT_BYTES)
    slice_bytes = LIST_BYTES + nw * (LIST_BYTES + nw * (FLOAT_BYTES + PTR_BYTES))
    history_bytes = nl * slice_bytes
    source_nodes = max(0, nodes - nw * nw)
    adj_bytes = (
        DICT_BYTES
        + source_nodes * (INT_BYTES + PTR_BYTES + LIST_BYTES)
        + edges_est * (INT_BYTES + PTR_BYTES)
    )
    return pos_bytes + history_bytes + adj_bytes


def estimate_matrix_free_bytes(nodes: int, slice_cells: int) -> int:
    # Two buffers for the current solve plus one scratch buffer.
    return LIST_BYTES + nodes * PTR_BYTES + nodes * (TUPLE3_BYTES + 3 * FLOAT_BYTES) + 3 * slice_cells * 8


def solve_static_poisson_matrix_free(
    PW: float,
    H: float,
    strength: float,
    iz_now: int,
    tol: float = 1e-10,
    max_iter: int = 6000,
) -> tuple[float, int]:
    """Solve lap(f) + src = 0 on the finite (y, z) grid with zero boundaries."""
    hw = int(PW / H)
    nw = 2 * hw + 1
    sy = nw // 2
    sz = nw // 2 + iz_now
    f = [[0.0] * nw for _ in range(nw)]
    omega = 2.0 / (1.0 + math.sin(math.pi / nw))

    for it in range(max_iter):
        max_delta = 0.0
        for parity in (0, 1):
            for iy in range(1, nw - 1):
                row = f[iy]
                up = f[iy - 1]
                dn = f[iy + 1]
                startz = 1 + ((iy + parity) & 1)
                for iz in range(startz, nw - 1, 2):
                    src = strength if (iy == sy and iz == sz) else 0.0
                    target = 0.25 * (up[iz] + dn[iz] + row[iz - 1] + row[iz + 1] + src)
                    new = row[iz] + omega * (target - row[iz])
                    delta = abs(new - row[iz])
                    if delta > max_delta:
                        max_delta = delta
                    row[iz] = new
        if max_delta < tol:
            return max_delta, it + 1

    return max_delta, max_iter


def build_rows(h_values: list[float]) -> list[ProbeRow]:
    rows: list[ProbeRow] = []
    for h in h_values:
        nl, hw, nw, nodes, slice_cells, md, avg_deg, edges_est = counts_for_h(h)
        current_python_bytes = estimate_python_current_bytes(nodes, nw, nl, edges_est)
        matrix_free_bytes = estimate_matrix_free_bytes(nodes, slice_cells)
        iz_now = round(IZ_START_PHYS / h)
        residual, iterations = solve_static_poisson_matrix_free(PW_PHYS, h, S_PHYS, iz_now)
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
                current_python_mib=mib(current_python_bytes),
                matrix_free_mib=mib(matrix_free_bytes),
                iterations=iterations,
                residual=residual,
                runtime_s=0.0,
            )
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--hs",
        type=float,
        nargs="*",
        default=[0.5, 0.35, 0.25, 0.125],
        help="Candidate lattice spacings to probe.",
    )
    args = parser.parse_args()

    rows = build_rows(args.hs)

    print("=" * 108)
    print("WAVE STATIC MATRIX-FREE DIRECT-COMPARATOR PROBE")
    print("=" * 108)
    print(f"Physical setup: T_phys={T_PHYS}, PW_phys={PW_PHYS}, z:[{IZ_START_PHYS}→{IZ_END_PHYS}]")
    print(f"Source source strength: {S_PHYS}")
    print(f"Red-black SOR solve on the finite (y,z) grid; no cached adjacency/state")
    print()
    print(
        f"{'H':>6s} {'NL':>4s} {'nw':>4s} {'nodes':>10s} {'edges~':>13s} "
        f"{'current_py MiB':>12s} {'matrix_free':>12s} {'iters':>8s} {'resid':>12s}"
    )
    print("-" * 108)
    for row in rows:
        print(
            f"{row.h:6.3f} {row.nl:4d} {row.nw:4d} {row.nodes:10d} {row.edges_est:13d} "
            f"{row.current_python_mib:12.1f} {row.matrix_free_mib:12.1f} "
            f"{row.iterations:8d} {row.residual:12.3e}"
        )

    print()
    print("Interpretation:")
    for row in rows:
        py_ok = "OK" if row.current_python_mib < 2048 else "OOM"
        mf_ok = "OK" if row.matrix_free_mib < 2048 else "OOM"
        solve_ok = "OK" if row.residual < 1e-8 else "WARN"
        print(
            f"  H={row.h:.3f}: current_python={py_ok}, matrix_free={mf_ok}, "
            f"solver={solve_ok}, iters={row.iterations}"
        )

    fine = rows[-1]
    print()
    if fine.residual < 1e-8 and fine.matrix_free_mib < 2048:
        print(
            "Verdict: matrix-free direct static solve looks viable for H=0.125. "
            "The solver converged cleanly and stays far below a 2 GiB budget."
        )
    else:
        print(
            "Verdict: matrix-free direct static solve is not yet clean enough for H=0.125 "
            "under this probe."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
