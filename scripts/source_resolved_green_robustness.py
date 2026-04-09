#!/usr/bin/env python3
"""Robustness sweep for the source-resolved exact Green pocket.

Question
--------
Is the exact-lattice Green-pocket architecture highly tuned to the baseline
source cluster / mu / eps choices, or does it have a real local robustness
region?

This sweep stays deliberately small:
  - same exact lattice family as the retained pocket
  - a local kernel neighborhood around the retained (mu, eps)
  - a local source-cluster neighborhood around the retained cross cluster
  - the same source-strength ladder and detector readout as the pocket

The result is only meant to answer the tuning question. It does not try to
promote the architecture into a full self-consistent field theory.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


H = 0.5
NL_PHYS = 20
PW = 3
SOURCE_STRENGTHS = m.SOURCE_STRENGTHS
TARGET_FIELD_MAX = 0.02

BASE_CLUSTER = [
    (0, 0),
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]

CLUSTER_VARIANTS: dict[str, list[tuple[int, int]]] = {
    "cross5": BASE_CLUSTER,
    "line3": [
        (0, 0),
        (1, 0),
        (-1, 0),
    ],
    "skew4": [
        (0, 0),
        (1, 0),
        (0, 1),
        (0, -1),
    ],
}

MU_VALUES = (0.04, 0.08, 0.12)
EPS_VALUES = (0.25, 0.50, 0.75)


@dataclass(frozen=True)
class CaseResult:
    label: str
    zero_shift: float
    toward: int
    alpha: float | None
    mean_ratio: float
    max_field: float
    pass_gate: bool


def _select_source_nodes(lat: m.Lattice3D, cluster: list[tuple[int, int]]) -> list[int]:
    gl = lat.nl // 3
    src_y = lat.hw
    src_z = lat.hw + round(m.SOURCE_Z / lat.h)
    nodes: list[int] = []
    for dy, dz in cluster:
        y = src_y + dy
        z = src_z + dz
        if 0 <= y < lat.nw and 0 <= z < lat.nw:
            nodes.append(lat.nmap[(gl, y - lat.hw, z - lat.hw)])
    return nodes


def _green_field(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    mu: float,
    eps: float,
) -> list[list[float]]:
    if not source_nodes:
        return [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]

    source_pos = [lat.pos[i] for i in source_nodes]
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    for layer in range(lat.nl):
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            x, y, z = lat.pos[ls + i]
            val = 0.0
            for mx, my, mz in source_pos:
                r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + eps
                val += source_strength * math.exp(-mu * r) / r
            field[layer][i] = val / len(source_pos)
    return field


def _field_abs_max(layers: list[list[float]]) -> float:
    return max(abs(v) for row in layers for v in row)


def _fit_power(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    lx = [math.log(x) for x, _ in pairs]
    ly = [math.log(y) for _, y in pairs]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def _evaluate_case(
    cluster_name: str,
    cluster: list[tuple[int, int]],
    mu: float,
    eps: float,
) -> CaseResult:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _select_source_nodes(lat, cluster)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, m.K)
    z_free = m._centroid_z(free, lat)

    ref_raw = _green_field(lat, max(SOURCE_STRENGTHS), source_nodes, mu, eps)
    ref_max = _field_abs_max(ref_raw)
    gain = TARGET_FIELD_MAX / ref_max if ref_max > 1e-30 else 1.0

    zero_dyn = [[gain * v for v in row] for row in _green_field(lat, 0.0, source_nodes, mu, eps)]
    zero_shift = m._centroid_z(lat.propagate(zero_dyn, m.K), lat) - z_free

    inst_vals: list[float] = []
    green_vals: list[float] = []
    ratios: list[float] = []
    for s in SOURCE_STRENGTHS:
        inst_field = m._instantaneous_field_layers(lat, s, m.SOURCE_Z)
        inst_delta = m._centroid_z(lat.propagate(inst_field, m.K), lat) - z_free

        green_field = [[gain * v for v in row] for row in _green_field(lat, s, source_nodes, mu, eps)]
        green_delta = m._centroid_z(lat.propagate(green_field, m.K), lat) - z_free

        inst_vals.append(inst_delta)
        green_vals.append(green_delta)
        ratios.append(abs(green_delta / inst_delta))

    alpha = _fit_power(list(SOURCE_STRENGTHS), green_vals)
    toward = sum(1 for v in green_vals if v > 0)
    mean_ratio = sum(ratios) / len(ratios)
    max_field = _field_abs_max([[gain * v for v in row] for row in _green_field(lat, max(SOURCE_STRENGTHS), source_nodes, mu, eps)])

    pass_gate = (
        abs(zero_shift) <= 1e-12
        and toward == len(SOURCE_STRENGTHS)
        and alpha is not None
        and 0.95 <= alpha <= 1.05
        and 0.5 <= mean_ratio <= 2.0
    )
    label = f"{cluster_name} mu={mu:.2f}, eps={eps:.2f}, nodes={len(source_nodes)}"
    return CaseResult(label, zero_shift, toward, alpha, mean_ratio, max_field, pass_gate)


def _print_result(result: CaseResult) -> None:
    alpha_str = f"{result.alpha:.3f}" if result.alpha is not None else "n/a"
    status = "PASS" if result.pass_gate else "FAIL"
    print(
        f"{result.label:24s}  zero={result.zero_shift:+.2e}  "
        f"TOWARD={result.toward}/4  F~M={alpha_str:>6s}  "
        f"|green/inst|={result.mean_ratio:5.3f}  max|f|={result.max_field:6.3e}  {status}"
    )


def main() -> None:
    print("=" * 92)
    print("SOURCE-RESOLVED GREEN ROBUSTNESS SWEEP")
    print("  exact 3D lattice local robustness around the retained Green pocket")
    print("=" * 92)
    print(f"lattice: h={H}, W={PW}, L={NL_PHYS}")
    print(f"source strengths: {SOURCE_STRENGTHS}")
    print(f"target max |f|: {TARGET_FIELD_MAX}")
    print()

    print("KERNEL NEIGHBORHOOD")
    kernel_results: list[CaseResult] = []
    for mu in MU_VALUES:
        for eps in EPS_VALUES:
            result = _evaluate_case("kernel", BASE_CLUSTER, mu, eps)
            kernel_results.append(result)
            _print_result(result)
    kernel_pass = sum(1 for r in kernel_results if r.pass_gate)
    print(f"kernel pass count: {kernel_pass}/{len(kernel_results)}")
    print()

    print("CLUSTER NEIGHBORHOOD")
    cluster_results: list[CaseResult] = []
    for label, cluster in CLUSTER_VARIANTS.items():
        result = _evaluate_case(f"cluster:{label}", cluster, 0.08, 0.50)
        cluster_results.append(result)
        _print_result(result)
    cluster_pass = sum(1 for r in cluster_results if r.pass_gate)
    print(f"cluster pass count: {cluster_pass}/{len(cluster_results)}")
    print()

    all_results = kernel_results + cluster_results
    all_pass = sum(1 for r in all_results if r.pass_gate)
    if all_pass >= 6:
        verdict = "real local robustness region"
    elif all_pass >= 3:
        verdict = "mixed local robustness with a clear tuned baseline"
    else:
        verdict = "highly tuned pocket"

    print("SAFE READ")
    print(f"  {verdict}")
    print("  the pocket is only interesting as moonshot material if a local neighborhood")
    print("  survives the hard gates, not just the exact baseline")


if __name__ == "__main__":
    main()
