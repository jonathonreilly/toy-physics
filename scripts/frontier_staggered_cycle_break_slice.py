#!/usr/bin/env python3
"""
Staggered Fermion Cycle-Bearing Break Slice
===========================================

Matched frontier slice around the first larger-graph break in the retained
cycle battery.

This probe keeps the retained battery rows unchanged and compares two families
at the same base graph size:
  - frontier branch: dense cross-color shortcuts added to random_geometric
  - quality-matched control: same edge-count scale, but local cross-color
    additions chosen by short distance and balanced degree rather than long
    shortcuts

The goal is to isolate whether the first break is specifically a gauge/current
collapse under shortcut density, or a broader graph-quality threshold.
"""

from __future__ import annotations

import math
import time
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit


SCRIPT_PATH = Path(__file__).resolve()
ROOT = SCRIPT_PATH.parents[1]
if str(ROOT / "scripts") not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT / "scripts"))

import frontier_staggered_cycle_battery as base  # noqa: E402


def _copy_graph(g, *, name=None, pos=None, colors=None, adj=None, src=None):
    pos = g.pos if pos is None else pos
    colors = g.colors if colors is None else colors
    adj = g.adj if adj is None else {k: sorted(v) for k, v in adj.items()}
    src = g.src if src is None else src
    depth = base._bfs(adj, src, len(pos))
    cycle_edge = base._find_cycle_edge(adj)
    return base.Graph(name or g.name, pos, colors, adj, len(pos), src, depth, cycle_edge)


def _add_edge(adj: dict[int, set[int]], i: int, j: int) -> None:
    if i == j:
        return
    adj.setdefault(i, set()).add(j)
    adj.setdefault(j, set()).add(i)


def _build_dense_shortcuts(graph, extra: int) -> base.Graph:
    adj = {i: set(nbs) for i, nbs in graph.adj.items()}
    pairs: list[tuple[float, int, int]] = []
    for i in range(graph.n):
        for j in range(i + 1, graph.n):
            if graph.colors[i] == graph.colors[j] or j in adj.get(i, set()):
                continue
            d = math.hypot(graph.pos[j, 0] - graph.pos[i, 0], graph.pos[j, 1] - graph.pos[i, 1])
            if d < 1.8:
                continue
            pairs.append((d, i, j))
    pairs.sort(reverse=True)
    for _, i, j in pairs[:extra]:
        _add_edge(adj, i, j)
    return _copy_graph(graph, name=f"{graph.name}_dense{extra}", adj=adj)


def _build_quality_matched_control(graph, extra: int) -> base.Graph:
    adj = {i: set(nbs) for i, nbs in graph.adj.items()}
    degrees = {i: len(nbs) for i, nbs in adj.items()}
    candidates: list[tuple[float, int, int, int, int]] = []
    for i in range(graph.n):
        for j in range(i + 1, graph.n):
            if graph.colors[i] == graph.colors[j] or j in adj.get(i, set()):
                continue
            d = math.hypot(graph.pos[j, 0] - graph.pos[i, 0], graph.pos[j, 1] - graph.pos[i, 1])
            deg_sum = degrees.get(i, 0) + degrees.get(j, 0)
            deg_gap = abs(degrees.get(i, 0) - degrees.get(j, 0))
            candidates.append((d, deg_sum, deg_gap, i, j))
    # Keep the control local and degree-balanced instead of shortcut-like.
    candidates.sort()
    for _, _, _, i, j in candidates[:extra]:
        _add_edge(adj, i, j)
    return _copy_graph(graph, name=f"{graph.name}_control{extra}", adj=adj)


def _gauge_metrics(graph) -> tuple[float | None, float | None, str]:
    if graph.cycle_edge is None:
        return None, None, "N/A"

    phi_vals = np.linspace(0.0, 2.0 * math.pi, 9)
    currents: list[float] = []
    i, j = graph.cycle_edge
    for phi in phi_vals:
        H_phi = base._build_H_flux(graph, base.MASS, graph.cycle_edge, phi)
        evals, evecs = np.linalg.eigh(H_phi.toarray())
        gs = evecs[:, 0]
        currents.append(float(np.imag(np.conj(gs[i]) * H_phi[i, j] * gs[j])))

    span = float(max(currents) - min(currents))
    try:
        def _sin(A, a, ph, b):
            return a * np.sin(A + ph) + b

        popt, _ = curve_fit(_sin, phi_vals, np.asarray(currents), p0=[span / 2, 0.0, np.mean(currents)])
        resid = np.asarray(currents) - _sin(phi_vals, *popt)
        sin_r2 = 1.0 - float(np.sum(resid**2) / np.sum((np.asarray(currents) - np.mean(currents)) ** 2))
    except Exception:
        sin_r2 = 0.0

    status = "PASS" if span > 1.0e-6 and sin_r2 > 0.9 else "FAIL"
    return span, sin_r2, status


def _gap_metrics(graph) -> tuple[float, float]:
    psi0 = base._probe_state(graph)
    rho_s = base._source_density(graph)
    phi_s = base._solve_phi(graph, rho_s)
    H_s = base._build_H(graph, base.MASS, phi_s)
    psi_s = base._cn_evolve(H_s, psi0, base.DT, base.N_STEPS_SINGLE)
    F_s = base._shell_force(graph, psi_s, phi_s)

    phi_ext = base._ext_phi(graph)
    H_ext = base._build_H(graph, base.MASS, phi_ext)
    psi_ext = base._cn_evolve(H_ext, psi0, base.DT, base.N_STEPS_SINGLE)
    F_ext = base._shell_force(graph, psi_ext, phi_ext)

    gap = abs(F_s - F_ext) / abs(F_ext) if abs(F_ext) > 1.0e-30 else 0.0
    G_eff = F_ext / F_s if abs(F_s) > 1.0e-30 else float("inf")
    return gap, G_eff


def _shell_spectral_metrics(graph) -> tuple[float, float]:
    psi0 = base._probe_state(graph)
    rho_s = base._source_density(graph)
    phi_s = base._solve_phi(graph, rho_s)
    phi_ext = base._ext_phi(graph)
    H_ext = base._build_H(graph, base.MASS, phi_ext)
    psi_ext = base._cn_evolve(H_ext, psi0, base.DT, base.N_STEPS_SINGLE)
    _ = base._shell_force(graph, psi_ext, phi_ext)

    max_d = int(np.max(graph.depth[np.isfinite(graph.depth)])) if np.any(np.isfinite(graph.depth)) else 0
    ps_sh = np.zeros(max_d + 1)
    pe_sh = np.zeros(max_d + 1)
    cnt = np.zeros(max_d + 1)
    for i in range(graph.n):
        d_ = int(graph.depth[i]) if np.isfinite(graph.depth[i]) else -1
        if 0 <= d_ <= max_d:
            ps_sh[d_] += phi_s[i]
            pe_sh[d_] += phi_ext[i]
            cnt[d_] += 1
    for d_ in range(max_d + 1):
        if cnt[d_] > 0:
            ps_sh[d_] /= cnt[d_]
            pe_sh[d_] /= cnt[d_]

    shell_ratio = 0.0
    if max_d > 0 and abs(pe_sh[0] - pe_sh[min(1, max_d)]) > 1.0e-10:
        shell_ratio = float((ps_sh[0] - ps_sh[min(1, max_d)]) / (pe_sh[0] - pe_sh[min(1, max_d)]))

    L = base._graph_laplacian(graph)
    evals_L, evecs_L = np.linalg.eigh(L.toarray())
    spec_solve = evecs_L.T @ phi_s
    spec_ext = evecs_L.T @ phi_ext
    ratios = []
    for k in range(1, min(6, graph.n)):
        if abs(spec_ext[k]) > 1.0e-10:
            ratios.append(abs(spec_solve[k] / spec_ext[k]))
    spec_ratio = float(np.mean(ratios)) if ratios else 0.0
    return shell_ratio, spec_ratio


def _run_case(label: str, graph):
    score = base.run_battery(graph)
    j_span, sin_r2, gauge_status = _gauge_metrics(graph)
    gap, g_eff = _gap_metrics(graph)
    shell_ratio, spec_ratio = _shell_spectral_metrics(graph)
    return {
        "label": label,
        "name": graph.name,
        "n": graph.n,
        "score": score,
        "j_span": j_span,
        "sin_r2": sin_r2,
        "gauge_status": gauge_status,
        "gap": gap,
        "g_eff": g_eff,
        "shell_ratio": shell_ratio,
        "spec_ratio": spec_ratio,
    }


def _print_row(row, *, kind: str) -> None:
    print(
        f"{kind:<10s} {row['label']:<24s} "
        f"score={row['score']}/9 "
        f"gauge={row['gauge_status']:<4s} "
        f"J_span={row['j_span']:.3e} "
        f"gap={row['gap']:.3f} "
        f"G_eff={row['g_eff']:.1f} "
        f"shell={row['shell_ratio']:.3f} "
        f"spec={row['spec_ratio']:.3f}"
    )


def main() -> None:
    t0 = time.time()
    print("=" * 104)
    print("STAGGERED FERMION - MATCHED CYCLE BREAK SLICE")
    print("=" * 104)
    print("Base family: random_geometric, side=18")
    print("Sweep: extra=4,5,6")
    print("Control: same edge-count scale, but local / degree-balanced cross-color additions")
    print("Rows unchanged: retained cycle battery remains the canonical retained battery")
    print()

    frontier_rows = []
    control_rows = []
    for extra in (4, 5, 6):
        frontier_graph = _build_dense_shortcuts(base.make_random_geometric(seed=42, side=18), extra=extra)
        control_graph = _build_quality_matched_control(base.make_random_geometric(seed=42, side=18), extra=extra)
        frontier_rows.append(_run_case(f"frontier_extra={extra}", frontier_graph))
        control_rows.append(_run_case(f"control_extra={extra}", control_graph))

    print("FRONTIER")
    for row in frontier_rows:
        _print_row(row, kind="frontier")

    print("\nCONTROL")
    for row in control_rows:
        _print_row(row, kind="control")

    first_fail = next((row for row in frontier_rows if row["score"] < 9), None)
    control_fail = next((row for row in control_rows if row["score"] < 9), None)

    print("\nSUMMARY")
    if first_fail is None:
        print("Frontier slice: no failure found at extra=4,5,6.")
    else:
        print(
            "Frontier slice first failure: "
            f"extra={first_fail['label'].split('=')[1]} -> {first_fail['score']}/9, "
            f"gauge={first_fail['gauge_status']}, J_span={first_fail['j_span']:.3e}."
        )
    if control_fail is None:
        print("Control slice: no failure found at extra=4,5,6.")
    else:
        print(
            "Control slice first failure: "
            f"extra={control_fail['label'].split('=')[1]} -> {control_fail['score']}/9, "
            f"gauge={control_fail['gauge_status']}, J_span={control_fail['j_span']:.3e}."
        )
    print(f"Time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
