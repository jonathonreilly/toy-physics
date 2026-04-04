#!/usr/bin/env python3
"""Detector-channel observable harness for the source-projected gravity seam.

Question
--------
Are we under-reading the current gravity signal by focusing only on detector
centroid shift, or do channel-bundle observables tell the same story?

This pilot stays deliberately bounded:
  - retained 3D modular family only
  - source-projected best nominal cell vs Laplacian baseline
  - identical code path at two seed counts (32 and 64)
  - fixed mass count across the b sweep

We measure, for each b:
  - centroid shift (current gravity readout)
  - bundle bias: signed / absolute detector-channel response
  - cancellation: 1 - |net| / abs_net
  - effective detector channel count (eff_ch)

The goal is not a new gravity claim. The goal is to test whether a channel-
space observable remains cleaner than centroid when the source-projected seam
softens under higher seed counts.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.source_projected_field_reaudit import (  # type: ignore  # noqa: E402
    CONNECT_RADIUS,
    GAP,
    K_BAND,
    MASS_COUNT_FIXED,
    MASS_LAYER_OFFSET,
    N_LAYERS,
    NODES_PER_LAYER,
    TARGET_BS,
    XYZ_RANGE,
    centroid_y,
    field_laplacian,
    field_source_projected,
    generate_3d_modular_dag,
    propagate,
)


BEST_STRENGTH = 0.16
BEST_EPS = 1.00
SEED_COUNTS = (32, 64)


@dataclass(frozen=True)
class MetricRow:
    centroid: float
    bundle_bias: float
    cancellation: float
    eff_ch: float


def _mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else math.nan


def _pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2 or len(ys) < 2:
        return math.nan
    xm = statistics.fmean(xs)
    ym = statistics.fmean(ys)
    num = sum((x - xm) * (y - ym) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - xm) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - ym) ** 2 for y in ys))
    if den_x <= 1e-30 or den_y <= 1e-30:
        return math.nan
    return num / (den_x * den_y)


def _select_fixed_mass_nodes(
    layer_nodes: list[int],
    positions: list[tuple[float, float, float]],
    target_y: float,
    count: int,
) -> list[int]:
    ranked = sorted(
        layer_nodes,
        key=lambda i: (abs(positions[i][1] - target_y), abs(positions[i][2]), i),
    )
    return ranked[:count] if len(ranked) >= count else []


def _detector_metrics(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
    field_fn,
) -> MetricRow:
    center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
    field_with = field_fn(positions, adj, mass_nodes)
    field_without = [0.0] * len(positions)

    centroid_vals: list[float] = []
    bias_vals: list[float] = []
    cancel_vals: list[float] = []
    eff_vals: list[float] = []

    for k in K_BAND:
        amps_with = propagate(positions, adj, field_with, src, k)
        amps_without = propagate(positions, adj, field_without, src, k)

        centroid_vals.append(
            centroid_y(amps_with, positions, det_list)
            - centroid_y(amps_without, positions, det_list)
        )

        signed: list[float] = []
        for d in det_list:
            pm = abs(amps_with[d]) ** 2
            pf = abs(amps_without[d]) ** 2
            dy = positions[d][1] - center_y
            signed.append((pm - pf) * dy)

        net = sum(signed)
        abs_net = sum(abs(v) for v in signed)
        if abs_net > 1e-30:
            bias_vals.append(net / abs_net)
            cancel_vals.append(1.0 - min(1.0, abs(net) / abs_net))
            probs = [abs(v) / abs_net for v in signed if abs(v) > 1e-30]
            entropy = -sum(p * math.log(p) for p in probs)
            eff_vals.append(math.exp(entropy))
        else:
            bias_vals.append(0.0)
            cancel_vals.append(0.0)
            eff_vals.append(0.0)

    return MetricRow(
        centroid=_mean(centroid_vals),
        bundle_bias=_mean(bias_vals),
        cancellation=_mean(cancel_vals),
        eff_ch=_mean(eff_vals),
    )


def _measure(seed_count: int, field_fn) -> dict[int, list[MetricRow]]:
    out: dict[int, list[MetricRow]] = {b: [] for b in TARGET_BS}
    for seed in range(seed_count):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 17 + 3,
            gap=GAP,
        )
        if len(layer_indices) < 7:
            continue

        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue

        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        mass_layer = layer_indices[MASS_LAYER_OFFSET]

        for b in TARGET_BS:
            mass_nodes = _select_fixed_mass_nodes(
                mass_layer, positions, center_y + b, MASS_COUNT_FIXED
            )
            if len(mass_nodes) != MASS_COUNT_FIXED:
                continue
            out[b].append(_detector_metrics(positions, adj, src, det_list, mass_nodes, field_fn))
    return out


def _print_mode(seed_count: int, label: str, field_fn) -> None:
    by_b = _measure(seed_count, field_fn)
    print(f"[{seed_count} seeds] {label}")
    print(
        f"{'b':>3s}  {'n':>3s}  {'centroid':>10s}  {'bundle_bias':>12s}  "
        f"{'cancel':>8s}  {'eff_ch':>8s}"
    )
    print(f"{'-' * 60}")

    bs: list[float] = []
    centroids: list[float] = []
    biases: list[float] = []
    cancels: list[float] = []
    effs: list[float] = []

    for b in TARGET_BS:
        rows = by_b[b]
        if not rows:
            print(f"{b:3d}  FAIL")
            continue
        centroid = _mean([r.centroid for r in rows])
        bias = _mean([r.bundle_bias for r in rows])
        cancel = _mean([r.cancellation for r in rows])
        eff = _mean([r.eff_ch for r in rows])
        print(f"{b:3d}  {len(rows):3d}  {centroid:+10.4f}  {bias:+12.4f}  {cancel:8.4f}  {eff:8.3f}")
        bs.append(float(b))
        centroids.append(centroid)
        biases.append(bias)
        cancels.append(cancel)
        effs.append(eff)

    if len(bs) >= 3:
        print(
            "  corr(metric, b): "
            f"centroid={_pearson(bs, centroids):+.3f}, "
            f"bundle_bias={_pearson(bs, biases):+.3f}, "
            f"cancel={_pearson(bs, cancels):+.3f}, "
            f"eff_ch={_pearson(bs, effs):+.3f}"
        )
    print()


def main() -> None:
    print("=" * 100)
    print("GRAVITY OBSERVABLE HARNESS PILOT")
    print("  retained 3D modular family, best nominal source-projected cell")
    print(f"  gap={GAP}, npl={NODES_PER_LAYER}, strength={BEST_STRENGTH:.2f}, eps={BEST_EPS:.2f}")
    print(f"  k-band={K_BAND}, fixed mass count={MASS_COUNT_FIXED}")
    print("=" * 100)
    print()

    for seeds in SEED_COUNTS:
        _print_mode(seeds, "Laplacian baseline", field_laplacian)
        _print_mode(
            seeds,
            "Source-projected",
            lambda p, a, m: field_source_projected(
                p, a, m, strength=BEST_STRENGTH, eps=BEST_EPS
            ),
        )

    print("=" * 100)
    print("Interpretation:")
    print("  If bundle_bias / eff_ch stay cleaner than centroid at 64 seeds, centroid-only may be under-reading the seam.")
    print("  If all observables soften together, the seam is genuinely washing out rather than being mismeasured.")
    print("=" * 100)


if __name__ == "__main__":
    main()
