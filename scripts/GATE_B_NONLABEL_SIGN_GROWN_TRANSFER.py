#!/usr/bin/env python3
"""Grown-row non-label sign-law transfer test.

This is the grown-geometry follow-on to the earlier Gate B non-label
connectivity work. The question is whether the old geometry-sector architecture
still carries the retained fixed-field signed-source response when we apply it
to the current retained grown row.

Scope:
  - retained grown row only: drift=0.2, restore=0.7
  - compare label-grown control vs position-based geometry-sector candidate
  - exact zero-source and neutral same-point cancellation checks
  - small source-charge linearity sanity pass

The result is intentionally narrow: it should tell us whether the old
architecture genuinely applies here, not whether it becomes a geometry-generic
field theory.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.gate_b_grown_joint_package import grow


H = 0.5
K = 5.0
BETA = 0.8
NL = 25
DRIFT = 0.2
RESTORE = 0.7
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
OFFSET = 1.0
MIN_EDGES = 5
SEEDS = [0]


@dataclass(frozen=True)
class Family:
    positions: list[tuple[float, float, float]]
    layers: list[list[int]]
    adj: dict[int, list[int]]


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _nearest_node_in_layer(
    pos: list[tuple[float, float, float]],
    layer_nodes: list[int],
    x_target: float,
    y_target: float,
    z_target: float,
) -> int | None:
    best = None
    best_d = float("inf")
    for idx in layer_nodes:
        x, y, z = pos[idx]
        d = (x - x_target) ** 2 + (y - y_target) ** 2 + (z - z_target) ** 2
        if d < best_d:
            best = idx
            best_d = d
    return best


def _field_from_sources(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
    sources: list[tuple[float, int]],
) -> list[float]:
    field = [0.0] * len(pos)
    source_layer = NL // 3
    x_target = source_layer * H
    for z_phys, charge in sources:
        node = _nearest_node_in_layer(pos, layers[source_layer], x_target, 0.0, z_phys)
        if node is None:
            continue
        mx, my, mz = pos[node]
        for i, (x, y, z) in enumerate(pos):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] += charge * SOURCE_STRENGTH / (r**FIELD_POWER)
    return field


def _propagate(pos: list[tuple[float, float, float]], adj: dict[int, list[int]], field: list[float]) -> list[complex]:
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H
    for i in order:
        ai = amps[i]
        if abs(ai) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1.0 + lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += ai * complex(math.cos(K * act), math.sin(K * act)) * w * hm / (L * L)
    return amps


def _centroid_z(amps: list[complex], pos: list[tuple[float, float, float]], det: list[int]) -> float:
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _build_geometry_sector_grown(fam: Family) -> Family:
    """Build a position-based sector stencil from the grown row itself."""

    pos, layers = fam.positions, fam.layers
    adj: dict[int, list[int]] = {}

    for layer in range(len(layers) - 1):
        dst_nodes = layers[layer + 1]
        dst_pos = [pos[i] for i in dst_nodes]
        for src in layers[layer]:
            sx, sy, sz = pos[src]
            sector_best: dict[tuple[int, int], tuple[float, int]] = {}
            ranked: list[tuple[float, int]] = []
            for dst, (dx, dy, dz) in zip(dst_nodes, dst_pos):
                by = max(-1, min(1, int(round((dy - sy) / H))))
                bz = max(-1, min(1, int(round((dz - sz) / H))))
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                ranked.append((dist2, dst))
                key = (by, bz)
                prev = sector_best.get(key)
                if prev is None or dist2 < prev[0]:
                    sector_best[key] = (dist2, dst)

            selected = [dst for _, dst in sorted(sector_best.values(), key=lambda item: item[0])]
            for _, dst in sorted(ranked, key=lambda item: item[0]):
                if len(selected) >= MIN_EDGES:
                    break
                if dst not in selected:
                    selected.append(dst)
            adj[src] = selected

    return Family(pos, layers, adj)


def _evaluate_family(fam: Family) -> dict[str, float]:
    pos, layers, adj = fam.positions, fam.layers, fam.adj
    det = layers[-1]
    free = _propagate(pos, adj, [0.0] * len(pos))
    z_free = _centroid_z(free, pos, det)

    cases = {
        "zero": [],
        "plus": [(SOURCE_Z, +1)],
        "minus": [(SOURCE_Z, -1)],
        "neutral": [(SOURCE_Z, +1), (SOURCE_Z, -1)],
        "double": [(SOURCE_Z, +2)],
    }
    out: dict[str, float] = {}
    for label, sources in cases.items():
        field = _field_from_sources(pos, layers, sources)
        amps = _propagate(pos, adj, field)
        out[label] = _centroid_z(amps, pos, det) - z_free
    out["alpha"] = math.log(abs(out["double"] / out["plus"])) / math.log(2.0) if abs(out["plus"]) > 1e-30 and abs(out["double"]) > 1e-30 else float("nan")
    return out


def _print_case(name: str, out: dict[str, float]) -> None:
    print(name)
    print(f"  zero-source delta_z        {out['zero']:+.6e}")
    print(f"  single +1 delta_z          {out['plus']:+.6e}")
    print(f"  single -1 delta_z          {out['minus']:+.6e}")
    print(f"  neutral +1/-1 delta_z      {out['neutral']:+.6e}")
    print(f"  double +2 delta_z          {out['double']:+.6e}")
    print(f"  charge exponent            {out['alpha']:.6f}")


def main() -> None:
    print("=" * 94)
    print("GROWN-ROW NON-LABEL SIGN-LAW TEST")
    print("  question: can the old geometry-sector architecture carry the fixed-field")
    print("  signed-source response on the retained grown row?")
    print("=" * 94)
    print(f"h={H}, NL={NL}, drift={DRIFT}, restore={RESTORE}, seeds={SEEDS}")
    print(f"source_z={SOURCE_Z}, offset={OFFSET}, strength={SOURCE_STRENGTH:g}")
    print()

    for seed in SEEDS:
        pos, adj, layers = grow(DRIFT, RESTORE, seed)
        label_family = Family(pos, layers, adj)
        sector_family = _build_geometry_sector_grown(label_family)

        label_out = _evaluate_family(label_family)
        sector_out = _evaluate_family(sector_family)

        print(f"seed={seed}")
        _print_case("label-grown control", label_out)
        _print_case("geometry-sector candidate", sector_out)
        print()

    print("SAFE READ")
    print("  - If the geometry-sector candidate keeps the zero/neutral controls at zero")
    print("    and preserves the charge-linear sign response, then the old architecture")
    print("    genuinely applies to the current grown-row fixed-field lane.")
    print("  - If it collapses to zero or loses charge linearity, the old architecture")
    print("    was specific to the earlier Gate B families and does not transplant cleanly.")


if __name__ == "__main__":
    main()
