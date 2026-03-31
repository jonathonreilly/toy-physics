#!/usr/bin/env python3
"""Compare generated-DAG visibility against small structural observables.

This stays on the mechanism-compression lane: instead of widening the
generated-DAG ladder, measure whether local slit-packet analogues explain the
seed-to-seed visibility spread better than raw edge count / density.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import math
import os
import statistics
import sys
from typing import Iterable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import (
    generate_causal_dag,
    path_sum_on_dag,
    visibility,
)


PHASE_PER_ACTION = 4.0
DEFAULT_PHASE_STEPS = 16
DEFAULT_DETECTOR_YS = [float(y) for y in range(-8, 9)]


@dataclass(frozen=True)
class Scenario:
    label: str
    n_layers: int = 25
    nodes_per_layer: int = 20
    y_range: float = 8.0
    connect_radius: float = 2.5
    barrier_layer: int = 12
    slit_ys: tuple[float, float] = (-3.0, 3.0)
    slit_width: float = 1.5
    detector_tol: float = 1.5

    @property
    def detector_layer(self) -> int:
        return self.n_layers - 1


@dataclass(frozen=True)
class SeedRow:
    scenario: str
    seed: int
    v_center: float
    mean_v: float
    edge_count: float
    edge_density: float
    reachable_nodes: float
    post_barrier_edge_count: float
    slit_cross_edge_count: float
    bypass_cross_edge_count: float
    center_upper_log_paths: float
    center_lower_log_paths: float
    center_bypass_log_paths: float
    center_balanced_log_paths: float
    center_path_balance: float
    center_slit_share: float
    center_retiming_gap: float
    center_retiming_alignment: float
    center_balance_share: float
    center_balance_share_retimed: float
    center_slit_load_retimed: float
    center_packet_completion: float


@dataclass(frozen=True)
class CandidateScore:
    name: str
    corr_v0: float
    corr_mean_v: float

    @property
    def summary_score(self) -> float:
        return (abs(self.corr_v0) + abs(self.corr_mean_v)) / 2.0


RAW_CANDIDATES = {
    "edge_count",
    "edge_density",
    "reachable_nodes",
    "post_barrier_edge_count",
}


def crossing_y(
    left: tuple[float, float],
    right: tuple[float, float],
    barrier_x: float,
) -> float:
    lx, ly = left
    rx, ry = right
    if math.isclose(lx, rx):
        return ry
    t = (barrier_x - lx) / (rx - lx)
    return ly + t * (ry - ly)


def crossing_sector(
    left: tuple[float, float],
    right: tuple[float, float],
    barrier_x: float,
    slit_ys: tuple[float, float],
    slit_width: float,
) -> str:
    cy = crossing_y(left, right, barrier_x)
    upper = max(slit_ys)
    lower = min(slit_ys)
    if abs(cy - upper) < slit_width:
        return "upper"
    if abs(cy - lower) < slit_width:
        return "lower"
    return "bypass"


def correlation(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        return 0.0
    mean_x = statistics.fmean(xs)
    mean_y = statistics.fmean(ys)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den_x = sum((x - mean_x) ** 2 for x in xs)
    den_y = sum((y - mean_y) ** 2 for y in ys)
    den = math.sqrt(den_x * den_y)
    return num / den if den else 0.0


def _log_count(value: int) -> float:
    return math.log10(value + 1.0)


def _balance(left: int, right: int) -> float:
    hi = max(left, right)
    lo = min(left, right)
    return lo / hi if hi else 0.0


def _evaluate_seed(args: tuple[Scenario, int, int]) -> SeedRow:
    scenario, seed, phase_steps = args
    positions, adj, arrival = generate_causal_dag(
        n_layers=scenario.n_layers,
        nodes_per_layer=scenario.nodes_per_layer,
        y_range=scenario.y_range,
        connect_radius=scenario.connect_radius,
        rng_seed=seed,
    )

    detector_ys = DEFAULT_DETECTOR_YS
    phases = [2.0 * math.pi * i / phase_steps for i in range(phase_steps)]
    probs_by_y = {dy: [] for dy in detector_ys}
    for phase in phases:
        dist = path_sum_on_dag(
            positions=positions,
            adj=adj,
            arrival=arrival,
            source_idx=0,
            detector_x=float(scenario.detector_layer),
            detector_ys=detector_ys,
            detector_tolerance=scenario.detector_tol,
            barrier_x=float(scenario.barrier_layer),
            slit_ys=list(scenario.slit_ys),
            slit_width=scenario.slit_width,
            phase_per_action=PHASE_PER_ACTION,
            phase_shift_upper=phase,
        )
        for dy in detector_ys:
            probs_by_y[dy].append(dist.get(dy, 0.0))

    vis_by_y: dict[float, float] = {}
    for dy, probs in probs_by_y.items():
        vis_by_y[dy] = visibility(probs) if any(prob > 0 for prob in probs) else -1.0
    active_vis = [value for value in vis_by_y.values() if value >= 0.0]
    mean_v = statistics.fmean(active_vis) if active_vis else 0.0
    v_center = vis_by_y.get(0.0, -1.0)

    barrier_x = float(scenario.barrier_layer)
    detector_x = float(scenario.detector_layer)
    order = sorted(range(len(positions)), key=lambda idx: (positions[idx][0], arrival[idx]))

    pre_counts: dict[int, int] = {0: 1}
    upper_counts: dict[int, int] = {}
    lower_counts: dict[int, int] = {}
    bypass_counts: dict[int, int] = {}
    upper_min_time: dict[int, float] = {}
    lower_min_time: dict[int, float] = {}

    edge_count = 0
    post_barrier_edge_count = 0
    slit_cross_edge_count = 0
    bypass_cross_edge_count = 0

    for idx in order:
        pre_count = pre_counts.get(idx, 0)
        upper_count = upper_counts.get(idx, 0)
        lower_count = lower_counts.get(idx, 0)
        bypass_count = bypass_counts.get(idx, 0)
        if not (pre_count or upper_count or lower_count or bypass_count):
            continue

        x, y = positions[idx]
        for child in adj.get(idx, []):
            edge_count += 1
            cx, cy = positions[child]
            dist = math.dist((x, y), (cx, cy))
            if x >= barrier_x or cx > barrier_x:
                post_barrier_edge_count += 1

            if x < barrier_x <= cx:
                sector = crossing_sector(
                    (x, y),
                    (cx, cy),
                    barrier_x=barrier_x,
                    slit_ys=scenario.slit_ys,
                    slit_width=scenario.slit_width,
                )
                if sector == "upper":
                    slit_cross_edge_count += 1
                    if pre_count:
                        upper_counts[child] = upper_counts.get(child, 0) + pre_count
                        candidate_time = arrival[idx] + dist
                        upper_min_time[child] = min(
                            upper_min_time.get(child, float("inf")),
                            candidate_time,
                        )
                elif sector == "lower":
                    slit_cross_edge_count += 1
                    if pre_count:
                        lower_counts[child] = lower_counts.get(child, 0) + pre_count
                        candidate_time = arrival[idx] + dist
                        lower_min_time[child] = min(
                            lower_min_time.get(child, float("inf")),
                            candidate_time,
                        )
                else:
                    bypass_cross_edge_count += 1
                    if pre_count:
                        bypass_counts[child] = bypass_counts.get(child, 0) + pre_count
                continue

            if cx <= barrier_x and pre_count:
                pre_counts[child] = pre_counts.get(child, 0) + pre_count
            if upper_count:
                upper_counts[child] = upper_counts.get(child, 0) + upper_count
                candidate_time = upper_min_time.get(idx, arrival[idx]) + dist
                upper_min_time[child] = min(
                    upper_min_time.get(child, float("inf")),
                    candidate_time,
                )
            if lower_count:
                lower_counts[child] = lower_counts.get(child, 0) + lower_count
                candidate_time = lower_min_time.get(idx, arrival[idx]) + dist
                lower_min_time[child] = min(
                    lower_min_time.get(child, float("inf")),
                    candidate_time,
                )
            if bypass_count:
                bypass_counts[child] = bypass_counts.get(child, 0) + bypass_count

    center_upper_paths = 0
    center_lower_paths = 0
    center_bypass_paths = 0
    center_upper_min = float("inf")
    center_lower_min = float("inf")
    center_detector_nodes = 0

    for idx, (x, y) in enumerate(positions):
        if abs(x - detector_x) >= 0.5 or abs(y - 0.0) >= scenario.detector_tol:
            continue
        center_detector_nodes += 1
        center_upper_paths += upper_counts.get(idx, 0)
        center_lower_paths += lower_counts.get(idx, 0)
        center_bypass_paths += bypass_counts.get(idx, 0)
        if idx in upper_min_time:
            center_upper_min = min(center_upper_min, upper_min_time[idx])
        if idx in lower_min_time:
            center_lower_min = min(center_lower_min, lower_min_time[idx])

    center_balanced_paths = min(center_upper_paths, center_lower_paths)
    center_total_paths = center_upper_paths + center_lower_paths + center_bypass_paths
    center_slit_paths = center_upper_paths + center_lower_paths
    center_slit_share = center_slit_paths / center_total_paths if center_total_paths else 0.0
    center_path_balance = _balance(center_upper_paths, center_lower_paths)
    if math.isfinite(center_upper_min) and math.isfinite(center_lower_min):
        center_retiming_gap = abs(center_upper_min - center_lower_min)
    else:
        center_retiming_gap = float("inf")
    center_retiming_alignment = (
        1.0 / (1.0 + center_retiming_gap) if math.isfinite(center_retiming_gap) else 0.0
    )
    center_packet_completion = (
        _log_count(center_balanced_paths)
        * center_path_balance
        * center_slit_share
        * center_retiming_alignment
    )
    center_balance_share = center_path_balance * center_slit_share
    center_balance_share_retimed = center_balance_share * center_retiming_alignment
    center_slit_load_retimed = _log_count(center_slit_paths) * center_retiming_alignment

    reachable_nodes = sum(1 for value in arrival if value < float("inf"))
    edge_density = edge_count / reachable_nodes if reachable_nodes else 0.0

    return SeedRow(
        scenario=scenario.label,
        seed=seed,
        v_center=v_center,
        mean_v=mean_v,
        edge_count=float(edge_count),
        edge_density=edge_density,
        reachable_nodes=float(reachable_nodes),
        post_barrier_edge_count=float(post_barrier_edge_count),
        slit_cross_edge_count=float(slit_cross_edge_count),
        bypass_cross_edge_count=float(bypass_cross_edge_count),
        center_upper_log_paths=_log_count(center_upper_paths),
        center_lower_log_paths=_log_count(center_lower_paths),
        center_bypass_log_paths=_log_count(center_bypass_paths),
        center_balanced_log_paths=_log_count(center_balanced_paths),
        center_path_balance=center_path_balance,
        center_slit_share=center_slit_share,
        center_retiming_gap=(
            center_retiming_gap if math.isfinite(center_retiming_gap) else float("nan")
        ),
        center_retiming_alignment=center_retiming_alignment,
        center_balance_share=center_balance_share,
        center_balance_share_retimed=center_balance_share_retimed,
        center_slit_load_retimed=center_slit_load_retimed,
        center_packet_completion=center_packet_completion,
    )


def score_candidates(rows: list[SeedRow]) -> list[CandidateScore]:
    candidates = [
        "edge_count",
        "edge_density",
        "reachable_nodes",
        "post_barrier_edge_count",
        "slit_cross_edge_count",
        "bypass_cross_edge_count",
        "center_balanced_log_paths",
        "center_path_balance",
        "center_slit_share",
        "center_retiming_alignment",
        "center_balance_share",
        "center_balance_share_retimed",
        "center_slit_load_retimed",
        "center_packet_completion",
    ]
    target_v0 = [row.v_center for row in rows]
    target_mean_v = [row.mean_v for row in rows]
    scores = []
    for name in candidates:
        values = [float(getattr(row, name)) for row in rows]
        scores.append(
            CandidateScore(
                name=name,
                corr_v0=correlation(values, target_v0),
                corr_mean_v=correlation(values, target_mean_v),
            )
        )
    return sorted(scores, key=lambda item: item.summary_score, reverse=True)


def top_rows(rows: list[SeedRow], count: int = 5) -> tuple[list[SeedRow], list[SeedRow]]:
    return (
        sorted(rows, key=lambda row: row.v_center, reverse=True)[:count],
        sorted(rows, key=lambda row: row.v_center)[:count],
    )


def run_rows(
    scenario: Scenario,
    seeds: Iterable[int],
    workers: int,
    phase_steps: int,
) -> list[SeedRow]:
    tasks = [(scenario, seed, phase_steps) for seed in seeds]
    if workers <= 1:
        return [_evaluate_seed(task) for task in tasks]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(_evaluate_seed, tasks))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", default="default")
    parser.add_argument("--seed-start", type=int, default=0)
    parser.add_argument("--seed-count", type=int, default=64)
    parser.add_argument("--phase-steps", type=int, default=DEFAULT_PHASE_STEPS)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    parser.add_argument("--n-layers", type=int, default=25)
    parser.add_argument("--nodes-per-layer", type=int, default=20)
    parser.add_argument("--y-range", type=float, default=8.0)
    parser.add_argument("--connect-radius", type=float, default=2.5)
    parser.add_argument("--barrier-layer", type=int, default=12)
    parser.add_argument("--slit-y", type=float, default=3.0)
    parser.add_argument("--slit-width", type=float, default=1.5)
    parser.add_argument("--detector-tol", type=float, default=1.5)
    args = parser.parse_args()

    scenario = Scenario(
        label=args.label,
        n_layers=args.n_layers,
        nodes_per_layer=args.nodes_per_layer,
        y_range=args.y_range,
        connect_radius=args.connect_radius,
        barrier_layer=args.barrier_layer,
        slit_ys=(-args.slit_y, args.slit_y),
        slit_width=args.slit_width,
        detector_tol=args.detector_tol,
    )
    seeds = range(args.seed_start, args.seed_start + args.seed_count)
    rows = run_rows(
        scenario=scenario,
        seeds=seeds,
        workers=max(1, args.workers),
        phase_steps=args.phase_steps,
    )
    rows.sort(key=lambda row: row.seed)
    scores = score_candidates(rows)
    raw_scores = [score for score in scores if score.name in RAW_CANDIDATES]
    local_scores = [score for score in scores if score.name not in RAW_CANDIDATES]
    high_rows, low_rows = top_rows(rows)

    print("=" * 72)
    print("GENERATIVE CAUSAL DAG VISIBILITY ORDER-PARAMETER COMPARE")
    print("=" * 72)
    print(
        f"Scenario: {scenario.label} "
        f"(layers={scenario.n_layers}, nodes/layer={scenario.nodes_per_layer}, "
        f"radius={scenario.connect_radius})"
    )
    print(
        f"Seeds: {args.seed_start}..{args.seed_start + args.seed_count - 1} "
        f"({args.seed_count} total), phase_steps={args.phase_steps}, workers={max(1, args.workers)}"
    )
    print()
    print("Candidate ranking by average |correlation| against V(y=0) and mean_V:")
    for rank, score in enumerate(scores, start=1):
        print(
            f"  {rank:2d}. {score.name:<26s} "
            f"corr_v0={score.corr_v0:+.4f} "
            f"corr_mean_V={score.corr_mean_v:+.4f} "
            f"summary={score.summary_score:.4f}"
        )

    winner = scores[0]
    raw_winner = raw_scores[0]
    local_winner = local_scores[0]
    print()
    print(
        "Top scalar: "
        f"{winner.name} (corr_v0={winner.corr_v0:+.4f}, "
        f"corr_mean_V={winner.corr_mean_v:+.4f})"
    )
    print(
        "Best raw baseline: "
        f"{raw_winner.name} (corr_v0={raw_winner.corr_v0:+.4f}, "
        f"corr_mean_V={raw_winner.corr_mean_v:+.4f})"
    )
    print(
        "Best local analogue: "
        f"{local_winner.name} (corr_v0={local_winner.corr_v0:+.4f}, "
        f"corr_mean_V={local_winner.corr_mean_v:+.4f})"
    )
    print()
    print("Highest center-visibility seeds:")
    for row in high_rows:
        print(
            f"  seed={row.seed:2d} V0={row.v_center:.6f} mean_V={row.mean_v:.6f} "
            f"packet={row.center_packet_completion:.6f} "
            f"balanced_log={row.center_balanced_log_paths:.3f} "
            f"slit_share={row.center_slit_share:.3f} "
            f"retime_align={row.center_retiming_alignment:.3f} "
            f"edge_density={row.edge_density:.3f}"
        )
    print()
    print("Lowest center-visibility seeds:")
    for row in low_rows:
        print(
            f"  seed={row.seed:2d} V0={row.v_center:.6f} mean_V={row.mean_v:.6f} "
            f"packet={row.center_packet_completion:.6f} "
            f"balanced_log={row.center_balanced_log_paths:.3f} "
            f"slit_share={row.center_slit_share:.3f} "
            f"retime_align={row.center_retiming_alignment:.3f} "
            f"edge_density={row.edge_density:.3f}"
        )

    print()
    print("Interpretation:")
    print(
        "  Compare whether local slit-packet completion proxies "
        "(balanced upper/lower center paths, slit-share, retiming alignment) "
        "track visibility more cleanly than raw size / density counts."
    )


if __name__ == "__main__":
    main()
