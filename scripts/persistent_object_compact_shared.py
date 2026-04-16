#!/usr/bin/env python3
"""Shared helpers for compact repeated-update exact-lattice object probes."""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


H = 0.25
SOURCE_CLUSTER = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
SOURCE_STRENGTHS = [0.001, 0.002, 0.004, 0.008]
N_UPDATES = 3
GREEN_EPS = 0.5
GREEN_MU = 0.08
FIELD_TARGET_MAX = 0.02
ALPHA_BAND = (0.95, 1.05)
OVERLAP_THRESHOLD = 0.90


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


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


def _normalize_weights(vals: list[float]) -> list[float]:
    total = sum(vals)
    if total <= 1e-30:
        return [1.0 / len(vals)] * len(vals)
    return [v / total for v in vals]


def _topk_weights(vals: list[float], k: int) -> list[float]:
    ranked = sorted(range(len(vals)), key=lambda i: vals[i], reverse=True)
    keep = set(ranked[: min(k, len(vals))])
    out = [vals[i] if i in keep else 0.0 for i in range(len(vals))]
    return _normalize_weights(out)


def _support_eff(weights: list[float]) -> tuple[float, float]:
    norm = _normalize_weights(weights)
    eff = math.exp(-sum(p * math.log(p) for p in norm if p > 0.0))
    support = sum(1 for p in norm if p > 1e-30)
    return eff, float(support)


def _source_cluster_nodes(lat: m.Lattice3D, source_z: float) -> list[int]:
    gl = lat.nl // 3
    src_y = lat.hw
    src_z = lat.hw + round(source_z / lat.h)
    nodes: list[int] = []
    for dy, dz in SOURCE_CLUSTER:
        y = src_y + dy
        z = src_z + dz
        if 0 <= y < lat.nw and 0 <= z < lat.nw:
            nodes.append(lat.nmap[(gl, y - lat.hw, z - lat.hw)])
    if len(nodes) != len(SOURCE_CLUSTER):
        raise ValueError(
            f"case source cluster clipped in bounds: expected {len(SOURCE_CLUSTER)} nodes, got {len(nodes)}"
        )
    return nodes


def _green_field_layers(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    weights: list[float],
) -> list[list[float]]:
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    source_pos = [lat.pos[i] for i in source_nodes]
    for layer in range(lat.nl):
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            x, y, z = lat.pos[ls + i]
            val = 0.0
            for w, (mx, my, mz) in zip(weights, source_pos):
                r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + GREEN_EPS
                val += w * source_strength * math.exp(-GREEN_MU * r) / r
            field[layer][i] = val
    return field


def _field_abs_max(layers: list[list[float]]) -> float:
    return max(abs(v) for row in layers for v in row) if layers else 0.0
