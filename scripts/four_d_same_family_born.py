#!/usr/bin/env python3
"""4D same-family Born-rule test on retained modular DAGs.

Goal
----
Test whether the retained 4D modular family can support a Born-rule / Sorkin
pass without switching to a separate companion graph.

This script compares two views of the same modular-family instances:

  1. Raw modular graph: the retained 4D modular DAG as generated.
  2. Same-family chokepoint view: the same graph instance, but with all
     edges that skip across the barrier removed so the barrier behaves like a
     true chokepoint inside the same family.

The narrow claim is intentionally conservative:
  - If the raw modular graph still shows bypass contamination, that is not a
    Born pass.
  - If the same-family chokepoint view is machine-precision linear and has
    machine-precision Sorkin I_3, then the Born check is restored only for the
    restricted chokepoint subfamily inside the retained modular family.

This is stricter than the earlier companion-graph check because the barrier is
derived from the same modular instance rather than being generated separately.
"""

from __future__ import annotations

import math
import os
import random
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.four_d_decoherence_large_n import generate_4d_modular_dag  # type: ignore  # noqa: E402

BETA = 0.8
K_BAND = (3.0, 5.0)
NODES_PER_LAYER = 25
SPATIAL_RANGE = 8.0
CONNECT_RADIUS = 4.5
N_LAYERS_LIST = (12, 20, 40, 60, 80)
GAPS = (3.0, 5.0)
N_SEEDS = 8


def _topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order: list[int] = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)
    return order


def _copy_adj(adj: dict[int, list[int]]) -> dict[int, list[int]]:
    return {i: list(nbs) for i, nbs in adj.items()}


def _finite_ratio(i3: float, p: float) -> float | None:
    if p <= 1e-30:
        return None
    ratio = abs(i3) / p
    return ratio if math.isfinite(ratio) else None


def _layer_map(layer_indices: list[list[int]]) -> dict[int, int]:
    out: dict[int, int] = {}
    for li, nodes in enumerate(layer_indices):
        for idx in nodes:
            out[idx] = li
    return out


def _prune_bypass_edges(
    adj: dict[int, list[int]],
    layer_indices: list[list[int]],
    barrier_layer: int,
) -> dict[int, list[int]]:
    """Remove edges that jump across the barrier layer."""
    by_idx = _layer_map(layer_indices)
    pruned = defaultdict(list)
    for i, nbs in adj.items():
        li = by_idx.get(i, -1)
        for j in nbs:
            lj = by_idx.get(j, -1)
            if li < barrier_layer and lj > barrier_layer:
                continue
            pruned[i].append(j)
    return dict(pruned)


def _propagate(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    k: float,
    blocked: set[int] | None = None,
) -> list[complex]:
    """Same phase-valley propagation used by the Born checks."""
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        x1, y1, z1, w1 = positions[i]
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x2, y2, z2, w2 = positions[j]
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            dw = w2 - w1
            L = math.sqrt(dx * dx + dy * dy + dz * dz + dw * dw)
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx / L, -1), 1))
            wt = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(k * L), math.sin(k * L)) * wt / L
    return amps


def _slit_partition(
    positions: list[tuple[float, float, float, float]],
    layer_indices: list[list[int]],
) -> tuple[int, list[int], list[int], set[int], list[int], list[int], list[int]] | None:
    n_layers = len(layer_indices)
    if n_layers < 7:
        return None

    barrier_layer = n_layers // 3
    barrier = list(layer_indices[barrier_layer])
    ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(ys) / len(ys)

    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
    slit_b = [i for i in barrier if abs(positions[i][1] - cy) < 2][:5]
    slit_c = [i for i in barrier if positions[i][1] < cy - 3][:5]
    if not slit_a or not slit_b or not slit_c:
        return None

    all_slits = slit_a + slit_b + slit_c
    blocked = set(barrier) - set(all_slits)
    src = list(layer_indices[0])
    det_list = list(layer_indices[-1])
    if not src or not det_list:
        return None
    return barrier_layer, barrier, src, blocked, slit_a, slit_b, slit_c


def _linearity_metric(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    blocked: set[int],
    slit_a: list[int],
    slit_c: list[int],
    k: float,
) -> float | None:
    non_slit = blocked
    amps_a = _propagate(positions, adj, src, k, non_slit | set(slit_c))
    amps_b = _propagate(positions, adj, src, k, non_slit | set(slit_a))
    amps_ab = _propagate(positions, adj, src, k, non_slit)

    max_rel = 0.0
    for d in det_list:
        psi_sum = amps_a[d] + amps_b[d]
        ref = max(abs(amps_ab[d]), abs(psi_sum))
        if ref > 1e-30:
            max_rel = max(max_rel, abs(amps_ab[d] - psi_sum) / ref)
    return max_rel


def _sorkin_metric(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    blocked: set[int],
    slit_a: list[int],
    slit_b: list[int],
    slit_c: list[int],
    k: float,
) -> tuple[float, float] | None:
    all_slits = set(slit_a) | set(slit_b) | set(slit_c)

    def prob(open_set: set[int]) -> float:
        closed = all_slits - open_set
        amps = _propagate(positions, adj, src, k, blocked | closed)
        return sum(abs(amps[d]) ** 2 for d in det_list)

    p_abc = prob(all_slits)
    p_ab = prob(set(slit_a) | set(slit_b))
    p_ac = prob(set(slit_a) | set(slit_c))
    p_bc = prob(set(slit_b) | set(slit_c))
    p_a = prob(set(slit_a))
    p_b = prob(set(slit_b))
    p_c = prob(set(slit_c))
    i3 = p_abc - p_ab - p_ac - p_bc + p_a + p_b + p_c
    return i3, p_abc


def _evaluate_graph(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    layer_indices: list[list[int]],
) -> dict[str, float] | None:
    info = _slit_partition(positions, layer_indices)
    if info is None:
        return None
    barrier_layer, barrier, src, blocked, slit_a, slit_b, slit_c = info
    det_list = list(layer_indices[-1])

    # Same-family chokepoint view: prune cross-barrier bypass edges only.
    ch_adj = _prune_bypass_edges(adj, layer_indices, barrier_layer)

    raw_lin_vals: list[float] = []
    raw_i3_vals: list[float] = []
    ch_lin_vals: list[float] = []
    ch_i3_vals: list[float] = []

    for k in K_BAND:
        raw_lin = _linearity_metric(positions, adj, src, det_list, blocked, slit_a, slit_c, k)
        raw_i3 = _sorkin_metric(positions, adj, src, det_list, blocked, slit_a, slit_b, slit_c, k)
        ch_lin = _linearity_metric(positions, ch_adj, src, det_list, blocked, slit_a, slit_c, k)
        ch_i3 = _sorkin_metric(positions, ch_adj, src, det_list, blocked, slit_a, slit_b, slit_c, k)

        if raw_lin is not None:
            raw_lin_vals.append(raw_lin)
        if raw_i3 is not None:
            ratio = _finite_ratio(raw_i3[0], raw_i3[1])
            if ratio is not None:
                raw_i3_vals.append(ratio)
        if ch_lin is not None:
            ch_lin_vals.append(ch_lin)
        if ch_i3 is not None:
            ratio = _finite_ratio(ch_i3[0], ch_i3[1])
            if ratio is not None:
                ch_i3_vals.append(ratio)

    if not raw_lin_vals or not raw_i3_vals or not ch_lin_vals or not ch_i3_vals:
        return None

    return {
        "raw_lin": sum(raw_lin_vals) / len(raw_lin_vals),
        "raw_i3": sum(raw_i3_vals) / len(raw_i3_vals),
        "ch_lin": sum(ch_lin_vals) / len(ch_lin_vals),
        "ch_i3": sum(ch_i3_vals) / len(ch_i3_vals),
    }


def run_gap(gap: float) -> list[dict[str, float | int | str]]:
    print(f"[4D modular gap={gap}] same-family Born on raw graph vs chokepoint view")
    print(
        f"  {'N':>4s}  {'raw_err':>10s}  {'raw_I3/P':>10s}  {'cp_err':>10s}  "
        f"{'cp_I3/P':>10s}  {'n_ok':>4s}  verdict"
    )
    print(f"  {'-' * 70}")

    rows: list[dict[str, float | int | str]] = []
    for nl in N_LAYERS_LIST:
        raw_lin_vals: list[float] = []
        raw_i3_vals: list[float] = []
        cp_lin_vals: list[float] = []
        cp_i3_vals: list[float] = []
        n_ok = 0

        for seed in range(N_SEEDS):
            positions, adj, layer_indices = generate_4d_modular_dag(
                n_layers=nl,
                nodes_per_layer=NODES_PER_LAYER,
                spatial_range=SPATIAL_RANGE,
                connect_radius=CONNECT_RADIUS,
                rng_seed=seed * 13 + 5,
                gap=gap,
            )
            metrics = _evaluate_graph(positions, adj, layer_indices)
            if metrics is None:
                continue

            raw_lin_vals.append(metrics["raw_lin"])
            raw_i3_vals.append(metrics["raw_i3"])
            cp_lin_vals.append(metrics["ch_lin"])
            cp_i3_vals.append(metrics["ch_i3"])
            n_ok += 1

        if not n_ok:
            print(f"  {nl:4d}  FAIL")
            continue

        raw_err = sum(raw_lin_vals) / len(raw_lin_vals)
        raw_i3 = sum(raw_i3_vals) / len(raw_i3_vals)
        cp_err = sum(cp_lin_vals) / len(cp_lin_vals)
        cp_i3 = sum(cp_i3_vals) / len(cp_i3_vals)
        raw_pass = raw_i3 < 1e-10
        cp_pass = cp_i3 < 1e-10

        if cp_pass and cp_err < 1e-10:
            verdict = "FULL PASS"
        elif cp_pass:
            verdict = "SORKIN PASS"
        elif raw_pass:
            verdict = "RAW ONLY"
        else:
            verdict = "FAIL"

        print(
            f"  {nl:4d}  {raw_err:10.2e}  {raw_i3:10.2e}  {cp_err:10.2e}  "
            f"{cp_i3:10.2e}  {n_ok:4d}  {verdict}"
        )
        rows.append(
            {
                "gap": gap,
                "N": nl,
                "raw_err": raw_err,
                "raw_i3": raw_i3,
                "cp_err": cp_err,
                "cp_i3": cp_i3,
                "n_ok": n_ok,
                "verdict": verdict,
            }
        )

    return rows


def main() -> None:
    print("=" * 86)
    print("4D SAME-FAMILY BORN PASS")
    print("  Retained family: dense 4D modular DAGs")
    print("  Comparison: raw modular graph vs same-family chokepoint-pruned view")
    print("  Goal: keep the Born check inside the retained family, not a companion graph")
    print("=" * 86)
    print()

    all_rows: list[dict[str, float | int | str]] = []
    for gap in GAPS:
        all_rows.extend(run_gap(gap))
        print()

    best_cp = next((r for r in all_rows if r["verdict"] == "SORKIN PASS"), None)
    best_any = next((r for r in all_rows if r["verdict"] in {"FULL PASS", "SORKIN PASS", "RAW ONLY"}), None)

    print("=" * 86)
    print("OVERALL SAFE CLAIM")
    if best_cp is not None:
        print(
            f"  gap={best_cp['gap']:.1f}, N={best_cp['N']}: "
            f"raw linearity={best_cp['raw_err']:.2e}, raw |I_3|/P={best_cp['raw_i3']:.2e}; "
            f"same-family chokepoint linearity={best_cp['cp_err']:.2e}, "
            f"|I_3|/P={best_cp['cp_i3']:.2e}"
        )
        print(
            "  Narrow headline: the same-family chokepoint view restores machine-"
            "precision Sorkin I_3 on a restricted low-N modular subfamily."
        )
    elif best_any is not None:
        print(
            f"  gap={best_any['gap']:.1f}, N={best_any['N']}: "
            f"raw linearity={best_any['raw_err']:.2e}, raw |I_3|/P={best_any['raw_i3']:.2e}; "
            f"chokepoint linearity={best_any['cp_err']:.2e}, |I_3|/P={best_any['cp_i3']:.2e}"
        )
        print(
            "  Narrow headline: at least one retained modular row is Sorkin-clean in "
            "the chokepoint view, but the claim should remain restricted."
        )
    else:
        print("  No retained modular row reached machine-precision Born cleanliness.")

    print("=" * 86)
    print("SAFE CLAIM GUIDE")
    print("  - Use 'same-family chokepoint Born pass' only if the chokepoint view is")
    print("    machine-precision clean and the raw modular graph is not.")
    print("  - Do not promote companion-graph language from the older strict joint lane.")
    print("  - If only a subset of gaps/N values pass, keep the claim restricted to")
    print("    that subfamily.")
    print("=" * 86)


if __name__ == "__main__":
    main()
