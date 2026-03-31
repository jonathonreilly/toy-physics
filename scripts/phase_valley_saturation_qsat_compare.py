#!/usr/bin/env python3
"""Measure bounded phase-valley saturation diagnostics against retained Δky.

This is a bounded diagnostic on the retained unitary gravity lane. It does not
change the propagator or reopen a broad scan. Instead it asks whether the toy
observable proposed in the theory card,

    Q_sat = phase_gap / pooled_phase_spread

better compresses the near-constant downstream momentum kick than the raw
valley phase gap alone.

Operationally:
- use the current momentum-space setup
- sweep the same impact-parameter family used in the current Δky logs
- compare a tiny set of geometry-aware probe cuts:
  - downstream continuation split (`x = 45`, `y >= 0`)
  - downstream mass-aware split (`x = 45`, `y >= b/2`)
  - near-mass skirt split (`x = 34`, `y >= b`)
- compute weighted circular phase means and spreads in each valley
- compare tanh fits for `phase_gap`, `Q_sat`, and `Q_sat * valley_balance`
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import math
import multiprocessing as mp
import os
import statistics
import sys
from typing import Iterable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.momentum_space_gravity import (  # noqa: E402
    fourier_transform_y,
    prob_centroid_ky,
    propagate_geom_full,
)
from toy_event_physics import (  # noqa: E402
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
)


@dataclass(frozen=True)
class ProbeConfig:
    name: str
    probe_x: int
    cut_mode: str
    description: str


@dataclass(frozen=True)
class PropagationRow:
    impact_b: int
    delta_ky: float
    mass_amps: dict[tuple[int, int], complex]


@dataclass(frozen=True)
class TrialRow:
    impact_b: int
    delta_ky: float
    upper_weight: float
    lower_weight: float
    valley_balance: float
    upper_phase_mean: float
    lower_phase_mean: float
    upper_phase_sigma: float
    lower_phase_sigma: float
    phase_gap: float
    pooled_phase_sigma: float
    q_sat: float
    q_sat_balanced: float


@dataclass(frozen=True)
class FitSummary:
    feature: str
    best_scale: float
    best_gain: float
    r2: float
    mae: float

    def render(self) -> str:
        return (
            f"{self.feature}: Δky ~= {self.best_scale:.4f} * tanh({self.best_gain:.4f} * x) "
            f"(R²={self.r2:.4f}, MAE={self.mae:.4f})"
        )


def _angle_diff(a: float, b: float) -> float:
    return math.atan2(math.sin(a - b), math.cos(a - b))


def _circular_stats(weights: list[float], phases: list[float]) -> tuple[float, float]:
    total = sum(weights)
    if total <= 1e-12:
        return 0.0, float("inf")
    real = sum(weight * math.cos(phase) for weight, phase in zip(weights, phases))
    imag = sum(weight * math.sin(phase) for weight, phase in zip(weights, phases))
    mean_angle = math.atan2(imag, real)
    resultant = math.sqrt(real * real + imag * imag) / total
    if resultant <= 1e-12:
        return mean_angle, float("inf")
    sigma = math.sqrt(max(0.0, -2.0 * math.log(resultant)))
    return mean_angle, sigma


def _fit_tanh(feature: str, xs: list[float], ys: list[float]) -> FitSummary:
    best: FitSummary | None = None
    for gain in [10 ** (start / 10.0) for start in range(-10, 21)]:
        z = [math.tanh(gain * x) for x in xs]
        denom = sum(value * value for value in z)
        if denom <= 1e-12:
            continue
        scale = sum(value * target for value, target in zip(z, ys)) / denom
        preds = [scale * value for value in z]
        mean_y = statistics.fmean(ys)
        sse = sum((pred - target) ** 2 for pred, target in zip(preds, ys))
        sst = sum((target - mean_y) ** 2 for target in ys)
        r2 = 1.0 - sse / sst if sst > 1e-12 else 0.0
        mae = statistics.fmean(abs(pred - target) for pred, target in zip(preds, ys))
        candidate = FitSummary(
            feature=feature,
            best_scale=scale,
            best_gain=gain,
            r2=r2,
            mae=mae,
        )
        if best is None or (candidate.r2, -candidate.mae) > (best.r2, -best.mae):
            best = candidate
    assert best is not None
    return best


def _split_cut(impact_b: int, cut_mode: str) -> float:
    if cut_mode == "zero":
        return 0.0
    if cut_mode == "half_b":
        return impact_b / 2.0
    if cut_mode == "b":
        return float(impact_b)
    raise ValueError(f"Unsupported cut_mode: {cut_mode}")


def _probe_row(
    impact_b: int,
    delta_ky: float,
    amps: dict[tuple[int, int], complex],
    probe_x: int,
    height: int,
    cut_mode: str,
) -> TrialRow:
    cut = _split_cut(impact_b, cut_mode)
    screen_ys = list(range(-height, height + 1))
    upper_weights: list[float] = []
    upper_phases: list[float] = []
    lower_weights: list[float] = []
    lower_phases: list[float] = []
    for y in screen_ys:
        amp = amps.get((probe_x, y), 0.0 + 0.0j)
        weight = abs(amp) ** 2
        if weight <= 1e-20:
            continue
        phase = math.atan2(amp.imag, amp.real)
        if y >= cut:
            upper_weights.append(weight)
            upper_phases.append(phase)
        else:
            lower_weights.append(weight)
            lower_phases.append(phase)

    upper_mean, upper_sigma = _circular_stats(upper_weights, upper_phases)
    lower_mean, lower_sigma = _circular_stats(lower_weights, lower_phases)
    upper_weight = sum(upper_weights)
    lower_weight = sum(lower_weights)
    valley_balance = min(upper_weight, lower_weight) / max(upper_weight, lower_weight, 1e-12)
    phase_gap = abs(_angle_diff(upper_mean, lower_mean))
    pooled_phase_sigma = math.sqrt(upper_sigma ** 2 + lower_sigma ** 2)
    q_sat = phase_gap / pooled_phase_sigma if math.isfinite(pooled_phase_sigma) and pooled_phase_sigma > 1e-12 else 0.0
    q_sat_balanced = q_sat * valley_balance

    return TrialRow(
        impact_b=impact_b,
        delta_ky=delta_ky,
        upper_weight=upper_weight,
        lower_weight=lower_weight,
        valley_balance=valley_balance,
        upper_phase_mean=upper_mean,
        lower_phase_mean=lower_mean,
        upper_phase_sigma=upper_sigma,
        lower_phase_sigma=lower_sigma,
        phase_gap=phase_gap,
        pooled_phase_sigma=pooled_phase_sigma,
        q_sat=q_sat,
        q_sat_balanced=q_sat_balanced,
    )


def _evaluate_b(task: tuple[int, int, int, int, int]) -> PropagationRow:
    impact_b, width, height, det_x, phase_k = task
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))
    free_field = {node: 0.0 for node in nodes}
    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=1.0)

    mass_nodes = frozenset((30, y) for y in range(impact_b - 1, impact_b + 2))
    mass_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    mass_field = derive_node_field(nodes, mass_rule)

    free_amps = propagate_geom_full(nodes, source, free_field, phase_k, 1.0)
    mass_amps = propagate_geom_full(nodes, source, mass_field, phase_k, 1.0)

    ft_free = fourier_transform_y(free_amps, det_x, screen_ys)
    ft_mass = fourier_transform_y(mass_amps, det_x, screen_ys)
    delta_ky = prob_centroid_ky(ft_mass, len(screen_ys)) - prob_centroid_ky(ft_free, len(screen_ys))
    return PropagationRow(impact_b=impact_b, delta_ky=delta_ky, mass_amps=mass_amps)


def run_rows(
    impact_bs: Iterable[int],
    workers: int,
    width: int,
    height: int,
    det_x: int,
    phase_k: int,
) -> list[PropagationRow]:
    tasks = [(impact_b, width, height, det_x, phase_k) for impact_b in impact_bs]
    if workers <= 1:
        return [_evaluate_b(task) for task in tasks]
    ctx = mp.get_context("fork")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
        return list(pool.map(_evaluate_b, tasks))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    parser.add_argument("--width", type=int, default=60)
    parser.add_argument("--height", type=int, default=25)
    parser.add_argument("--det-x", type=int, default=45)
    parser.add_argument("--mass-x", type=int, default=30)
    parser.add_argument("--near-offset", type=int, default=4)
    parser.add_argument("--phase-k", type=int, default=2)
    args = parser.parse_args()

    impact_bs = [2, 4, 6, 8, 10, 12, 15, 18, 20]
    propagation_rows = run_rows(
        impact_bs=impact_bs,
        workers=max(1, args.workers),
        width=args.width,
        height=args.height,
        det_x=args.det_x,
        phase_k=args.phase_k,
    )
    propagation_rows.sort(key=lambda row: row.impact_b)

    probe_configs = [
        ProbeConfig(
            name="detector_y0",
            probe_x=args.det_x,
            cut_mode="zero",
            description=f"downstream continuation split at x={args.det_x}, y>=0",
        ),
        ProbeConfig(
            name="detector_half_b",
            probe_x=args.det_x,
            cut_mode="half_b",
            description=f"downstream mass-aware split at x={args.det_x}, y>=b/2",
        ),
        ProbeConfig(
            name="near_mass_b",
            probe_x=args.mass_x + args.near_offset,
            cut_mode="b",
            description=f"near-mass skirt split at x={args.mass_x + args.near_offset}, y>=b",
        ),
    ]

    summary_rows: list[tuple[ProbeConfig, list[TrialRow], list[FitSummary]]] = []
    ranked_fits: list[tuple[ProbeConfig, FitSummary]] = []
    for probe in probe_configs:
        rows = [
            _probe_row(
                impact_b=propagation_row.impact_b,
                delta_ky=propagation_row.delta_ky,
                amps=propagation_row.mass_amps,
                probe_x=probe.probe_x,
                height=args.height,
                cut_mode=probe.cut_mode,
            )
            for propagation_row in propagation_rows
        ]
        ys = [row.delta_ky for row in rows]
        fits = [
            _fit_tanh("phase_gap", [row.phase_gap for row in rows], ys),
            _fit_tanh("q_sat", [row.q_sat for row in rows], ys),
            _fit_tanh("q_sat_balanced", [row.q_sat_balanced for row in rows], ys),
        ]
        fits.sort(key=lambda fit: (fit.r2, -fit.mae), reverse=True)
        summary_rows.append((probe, rows, fits))
        ranked_fits.extend((probe, fit) for fit in fits)

    ranked_fits.sort(key=lambda item: (item[1].r2, -item[1].mae), reverse=True)

    print("=" * 88)
    print("PHASE-VALLEY SATURATION Q_SAT COMPARE")
    print("=" * 88)
    print(
        f"Detector x={args.det_x}, mass_x={args.mass_x}, phase_k={args.phase_k:.1f}, "
        f"impact parameters={impact_bs}, workers={max(1, args.workers)}"
    )
    print()
    for probe, rows, fits in summary_rows:
        print(f"Probe: {probe.name} ({probe.description})")
        print(
            f"{'b':>4s} {'Δky':>10s} {'gap':>9s} {'σ_pool':>9s} "
            f"{'Q_sat':>9s} {'balance':>9s} {'Q_bal':>9s}"
        )
        print("-" * 70)
        for row in rows:
            print(
                f"{row.impact_b:4d} {row.delta_ky:+10.4f} {row.phase_gap:9.4f} "
                f"{row.pooled_phase_sigma:9.4f} {row.q_sat:9.4f} "
                f"{row.valley_balance:9.4f} {row.q_sat_balanced:9.4f}"
            )
        print()
        print("  Best tanh fits:")
        for fit in fits:
            print(f"    {fit.render()}")
        print()

    print("Overall fit ranking:")
    for probe, fit in ranked_fits[:6]:
        print(f"  {probe.name}: {fit.render()}")
    print()
    print("Interpretation:")
    best_probe, best_fit = ranked_fits[0]
    if best_fit.feature == "phase_gap":
        print(
            f"  The best retained bounded diagnostic is the raw phase gap on {best_probe.name}, "
            "not normalized Q_sat."
        )
    elif best_fit.feature == "q_sat":
        print(
            f"  The normalized valley-bias observable Q_sat wins on {best_probe.name}, "
            "supporting the saturation-law picture."
        )
    else:
        print(
            f"  The best retained bounded diagnostic is balance-weighted Q_sat on {best_probe.name}, "
            "so normalization only helps once both valleys still carry live weight."
        )
    print(
        "  Geometry-aware valley cuts help the raw phase gap more than the normalized "
        "saturation ratios in this bounded compare."
    )
    print(
        "  A good next refinement would be to replace node phase by a truer near-mass "
        "path/action statistic while keeping the same retained propagator and Δky readout."
    )


if __name__ == "__main__":
    main()
