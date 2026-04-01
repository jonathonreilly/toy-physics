#!/usr/bin/env python3
"""Test geometry-normalized mass-side observables on the directional b lane.

This bounded follow-on keeps the directional path measure fixed and reuses the
same generated-DAG family as ``directional_b_readout_compare.py``. Instead of
changing the propagator or the detector readout again, it asks whether the
wrong-direction raw trend is partly a geometry-labeling issue by normalizing
the mass-side response by:

- the mass-cluster center offset ``b_center``
- the nearest-edge offset ``b_edge = b_center - span/2``

The goal is not to declare a final force law, only to see whether a simple
geometry-normalized response density restores the desired decreasing trend with
actual impact parameter on the bounded family.
"""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import math
import multiprocessing as mp
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.directional_b_readout_compare import (  # noqa: E402
    ACTION_LIKE_METRICS,
    DEFAULT_IMPACT_BS,
    DEFAULT_N_LAYERS,
    NEGATIVE_SLOPE_EPS,
    TrialRow as BaseTrialRow,
    _evaluate_trial,
    _linear_slope,
    _oriented_strength,
    _select_mass_nodes,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402


EPS = 1e-9
EDGE_B_MIN = 0.5


@dataclass(frozen=True)
class TrialRow:
    n_layers: int
    target_b: float
    seed: int
    actual_b: float
    mass_span: float
    center_edge_b: float
    action_channel: float
    packet_flow_action: float
    action_over_b: float
    action_over_edge_b: float
    flow_over_b: float
    flow_over_edge_b: float
    visibility_guardrail: float


def _mass_geometry(task: tuple[int, float, int, float, float, int]) -> tuple[float, float]:
    n_layers, target_b, seed, _angle_beta, _retain_share, mass_nodes = task
    positions, _adj, _ = generate_causal_dag(
        n_layers=n_layers,
        nodes_per_layer=25,
        y_range=12.0,
        connect_radius=3.0,
        rng_seed=seed * 11 + 7,
    )
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, _y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    center_y = statistics.fmean(y for _x, y in positions)
    mid = len(layers) // 2
    grav_mass = _select_mass_nodes(
        positions=positions,
        layer_nodes=by_layer[layers[mid]],
        center_y=center_y,
        target_b=target_b,
        mass_nodes=mass_nodes,
    )
    ys = [positions[node][1] for node in grav_mass]
    span = (max(ys) - min(ys)) if ys else 0.0
    actual_b = statistics.fmean(ys) - center_y if ys else 0.0
    return actual_b, span


def _evaluate_geometry_trial(task: tuple[int, float, int, float, float, int]) -> TrialRow | None:
    base_row: BaseTrialRow | None = _evaluate_trial(task)
    if base_row is None:
        return None

    actual_b, mass_span = _mass_geometry(task)
    edge_b = max(actual_b - 0.5 * mass_span, EPS)

    action_strength = _oriented_strength("action_channel", base_row.action_channel)
    flow_strength = _oriented_strength("packet_flow_action", base_row.packet_flow_action)

    return TrialRow(
        n_layers=base_row.n_layers,
        target_b=base_row.target_b,
        seed=base_row.seed,
        actual_b=actual_b,
        mass_span=mass_span,
        center_edge_b=edge_b,
        action_channel=base_row.action_channel,
        packet_flow_action=base_row.packet_flow_action,
        action_over_b=action_strength / max(actual_b, EPS),
        action_over_edge_b=action_strength / edge_b if edge_b >= EDGE_B_MIN else float("nan"),
        flow_over_b=flow_strength / max(actual_b, EPS),
        flow_over_edge_b=flow_strength / edge_b if edge_b >= EDGE_B_MIN else float("nan"),
        visibility_guardrail=base_row.visibility_guardrail,
    )


def _print_trend_summary(rows: list[TrialRow], metric_names: list[str]) -> None:
    grouped: dict[float, list[TrialRow]] = defaultdict(list)
    for row in rows:
        grouped[row.target_b].append(row)

    actual_bs = [statistics.fmean(entry.actual_b for entry in grouped[target_b]) for target_b in sorted(grouped)]
    print("Trend summary (desired: normalized attraction density decreases as actual b increases):")
    for metric in metric_names:
        pairs = []
        for target_b in sorted(grouped):
            values = [getattr(entry, metric) for entry in grouped[target_b]]
            values = [value for value in values if not math.isnan(value)]
            if values:
                pairs.append((statistics.fmean(entry.actual_b for entry in grouped[target_b]), statistics.fmean(values)))
        if len(pairs) < 2:
            print(f"  {metric:>19s}: INSUF (too few non-singular points)")
            continue
        xs = [pair[0] for pair in pairs]
        strengths = [pair[1] for pair in pairs]
        slope = _linear_slope(xs, strengths)
        start = strengths[0]
        end = strengths[-1]
        status = "PASS" if slope < -NEGATIVE_SLOPE_EPS and end < start else "FAIL"
        print(
            f"  {metric:>19s}: {status} "
            f"(strength {start:+.4f} -> {end:+.4f}, slope {slope:+.4f})"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--n-layers", nargs="+", type=int, default=list(DEFAULT_N_LAYERS))
    parser.add_argument("--impact-bs", nargs="+", type=float, default=list(DEFAULT_IMPACT_BS))
    parser.add_argument("--angle-beta", type=float, default=0.8)
    parser.add_argument("--retain-share", type=float, default=0.5)
    parser.add_argument("--mass-nodes", type=int, default=3)
    args = parser.parse_args()

    tasks = [
        (n_layers, target_b, seed, args.angle_beta, args.retain_share, args.mass_nodes)
        for n_layers in args.n_layers
        for target_b in args.impact_bs
        for seed in range(args.seeds)
    ]

    ctx = mp.get_context("fork")
    if args.workers <= 1:
        rows = [_evaluate_geometry_trial(task) for task in tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
                rows = list(pool.map(_evaluate_geometry_trial, tasks))
        except (OSError, PermissionError):
            rows = [_evaluate_geometry_trial(task) for task in tasks]
    rows = [row for row in rows if row is not None]

    metric_names = [
        "action_over_b",
        "action_over_edge_b",
        "flow_over_b",
        "flow_over_edge_b",
    ]

    print("=" * 112)
    print("DIRECTIONAL-MEASURE B GEOMETRY-NORMALIZED COMPARE")
    print("=" * 112)
    print(
        "Transport fixed to exp(i k S_spent) / L^p × exp(-beta * theta^2); "
        f"beta={args.angle_beta:.3f}, seeds={args.seeds}, k_band fixed in directional_b_readout_compare"
    )
    print("Mass region is still chosen by nearest mid-layer nodes; only the mass-side response is normalized.")
    print(f"Nearest-edge normalization is reported only when edge_b >= {EDGE_B_MIN:.1f}; smaller values are singular.")
    print()

    for n_layers in args.n_layers:
        bucket = [row for row in rows if row.n_layers == n_layers]
        if not bucket:
            continue
        grouped: dict[float, list[TrialRow]] = defaultdict(list)
        for row in bucket:
            grouped[row.target_b].append(row)

        def render_mean(values: list[float]) -> str:
            values = [value for value in values if not math.isnan(value)]
            return f"{statistics.fmean(values):+9.4f}" if values else f"{'n/a':>9s}"

        print(f"N={n_layers}")
        print(
            f"{'target_b':>8s} {'actual_b':>8s} {'span':>8s} {'edge_b':>8s} "
            f"{'A_raw':>9s} {'F_raw':>9s} {'A/b':>9s} {'A/edge':>9s} {'F/b':>9s} {'F/edge':>9s}"
        )
        print("-" * 100)
        for target_b in sorted(grouped):
            sample = grouped[target_b]
            action_strength = statistics.fmean(_oriented_strength("action_channel", row.action_channel) for row in sample)
            flow_strength = statistics.fmean(_oriented_strength("packet_flow_action", row.packet_flow_action) for row in sample)
            print(
                f"{target_b:8.2f} "
                f"{statistics.fmean(row.actual_b for row in sample):8.3f} "
                f"{statistics.fmean(row.mass_span for row in sample):8.3f} "
                f"{statistics.fmean(row.center_edge_b for row in sample):8.3f} "
                f"{action_strength:+9.4f} "
                f"{flow_strength:+9.4f} "
                f"{statistics.fmean(row.action_over_b for row in sample):+9.4f} "
                f"{render_mean([row.action_over_edge_b for row in sample])} "
                f"{statistics.fmean(row.flow_over_b for row in sample):+9.4f} "
                f"{render_mean([row.flow_over_edge_b for row in sample])}"
            )
        _print_trend_summary(bucket, metric_names)
        print()

    print("Interpretation:")
    print("  Raw action-style reads still strengthen with b in the underlying compare.")
    print("  Here we ask whether response density per center offset or per nearest-edge offset restores")
    print("  the expected decreasing trend without changing transport or mass selection.")


if __name__ == "__main__":
    main()
