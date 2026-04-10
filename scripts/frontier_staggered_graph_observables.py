#!/usr/bin/env python3
"""Graph-native observables for staggered / Kahler-Dirac lanes.

This probe keeps the portability families from
`frontier_staggered_graph_portability.py` but splits observables into:

- retained: force/current observables that should survive on graph families
  with cycles, plus Born/linearity, norm, F∝M, achromatic force,
  equivalence, and robustness
- secondary: centroid and shell diagnostics, which are useful but recurrence-
  sensitive on non-cubic graphs

The script is intentionally narrow. It is a classification probe, not a new
canonical card.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts import frontier_staggered_graph_portability as port  # noqa: E402


@dataclass
class ObsResult:
    family: str
    n: int
    retained_passes: int
    retained_total: int
    secondary_centroid_shift: float
    secondary_shell_bias: float
    gauge_status: str
    gauge_j_range: float | None


def _mean_depth(graph: port.GraphFamily, psi: np.ndarray) -> float:
    rho = np.abs(psi) ** 2
    mask = np.isfinite(graph.depth)
    return float(np.sum(rho[mask] * graph.depth[mask]) / max(np.sum(rho[mask]), 1e-30))


def _shell_bias(graph: port.GraphFamily, psi: np.ndarray) -> float:
    rho = np.abs(psi) ** 2
    source_mass = float(rho[graph.source])
    detector_mass = float(np.sum(rho[graph.detector])) if graph.detector else 0.0
    return detector_mass - source_mass


def _measure(graph: port.GraphFamily) -> ObsResult:
    n = graph.positions.shape[0]
    psi0 = port._probe_state(n, graph.positions, graph.source, k0=0.0)
    psi1 = port._probe_state(n, graph.positions, graph.source, k0=0.31)
    H_free = port._build_hamiltonian(graph, port.MASS, 0.0)

    born_lin = port._lin_residual(H_free, psi0, psi1)
    psi_free = port._evolve_cn(H_free, psi0, port.DT, port.N_STEPS)
    norm_drift = abs(np.linalg.norm(psi_free) - 1.0)

    force, _, psi_grav = port._force_metrics(graph, 0.18, port.MASS, port.SOURCE_STRENGTH)
    force_sign = force > 0.0

    strengths = [1.0, 2.0, 4.0, 8.0]
    f_vals = []
    for s in strengths:
        f, _, _ = port._force_metrics(graph, 0.18, port.MASS, port.SOURCE_STRENGTH * s)
        f_vals.append(f)
    coeff = np.polyfit(strengths, f_vals, 1)
    pred = np.polyval(coeff, strengths)
    denom = np.sum((np.array(f_vals) - np.mean(f_vals)) ** 2)
    fm_r2 = 1.0 - float(np.sum((np.array(f_vals) - pred) ** 2) / denom) if denom > 0 else 1.0

    force_vals = []
    for k0 in port.ACHROM_K:
        force_k, _, _ = port._force_metrics(graph, k0, port.MASS, port.SOURCE_STRENGTH)
        force_vals.append(force_k)
    achrom_cv = float(np.std(force_vals) / max(abs(np.mean(force_vals)), 1e-30))

    masses = [0.12, 0.18, 0.30, 0.42]
    accels = []
    for m in masses:
        f_m, _, _ = port._force_metrics(graph, 0.18, m, port.SOURCE_STRENGTH)
        accels.append(f_m / m)
    equiv_cv = float(np.std(accels) / max(abs(np.mean(accels)), 1e-30))

    robust_total = 0
    robust_toward = 0
    for k0 in (0.0, 0.2, 0.4):
        f_k, _, _ = port._force_metrics(graph, k0, port.MASS, port.SOURCE_STRENGTH)
        robust_total += 1
        robust_toward += int(f_k > 0)

    retained_passes = sum(
        [
            born_lin < 1e-10,
            norm_drift < 1e-10,
            force > 0.0,
            fm_r2 > 0.9,
            achrom_cv < 0.05,
            equiv_cv < 0.05,
            robust_toward == robust_total,
            (not graph.has_cycle) or graph.cycle_edge is not None,
        ]
    )

    return ObsResult(
        family=graph.name,
        n=n,
        retained_passes=retained_passes,
        retained_total=8,
        secondary_centroid_shift=_mean_depth(graph, psi_grav) - _mean_depth(graph, psi0),
        secondary_shell_bias=_shell_bias(graph, psi_grav),
        gauge_status="PASS" if graph.has_cycle else "N/A",
        gauge_j_range=None,
    )


def _gauge_current(graph: port.GraphFamily) -> float | None:
    if not graph.has_cycle or graph.cycle_edge is None:
        return None
    phi_vals = np.linspace(0.0, 2.0 * np.pi, 7)
    currents = []
    for phi in phi_vals:
        H_phi = port._build_hamiltonian(
            graph,
            port.MASS,
            port.SOURCE_STRENGTH,
            flux=phi,
            flux_edge=graph.cycle_edge,
        )
        evals, evecs = np.linalg.eigh(H_phi.toarray())
        gs = evecs[:, 0]
        i, j = graph.cycle_edge
        hop = H_phi[i, j]
        currents.append(float(np.imag(np.conj(gs[i]) * hop * gs[j])))
    return float(max(currents) - min(currents))


def main() -> None:
    print("=" * 92)
    print("STAGGERED GRAPH OBSERVABLES")
    print("  Retained: Born/linearity, norm, force sign, F∝M, achromatic force,")
    print("  equivalence, robustness, gauge/current when cycles exist")
    print("  Secondary: centroid shift, shell bias")
    print("=" * 92)
    print(f"  dt={port.DT}, steps={port.N_STEPS}, mass={port.MASS}, source={port.SOURCE_STRENGTH}")
    print()

    results: list[ObsResult] = []
    for graph in port._make_graphs():
        result = _measure(graph)
        current = _gauge_current(graph)
        result.gauge_j_range = current
        if current is not None:
            result.gauge_status = "PASS" if current > 1e-4 else "FAIL"
        results.append(result)

        gauge_txt = "N/A" if current is None else f"{current:.3e} [{result.gauge_status}]"
        print(
            f"{result.family:<26} "
            f"n={result.n:<3d} "
            f"retained={result.retained_passes}/{result.retained_total} "
            f"centroid_shift={result.secondary_centroid_shift:+.3e} "
            f"shell_bias={result.secondary_shell_bias:+.3e} "
            f"gauge={gauge_txt}"
        )

    print()
    print("READOUT")
    for r in results:
        retained_label = "RETAINED" if r.retained_passes == r.retained_total else "PARTIAL"
        print(
            f"  {r.family:<26} {retained_label} "
            f"centroid/shell are secondary; gauge={r.gauge_status}"
        )

    print()
    print("Interpretation:")
    print("  - Force/current are the retained observables on these graph families.")
    print("  - Centroid and shell diagnostics are informative but recurrence-sensitive.")
    print("  - Gauge/current is only scored on cycle-bearing families.")


if __name__ == "__main__":
    main()
