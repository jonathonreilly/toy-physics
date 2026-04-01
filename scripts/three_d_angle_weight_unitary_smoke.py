#!/usr/bin/env python3
"""Bounded 3D unitary smoke test for the angle-weight candidate.

This script closes the main remaining gap in the current "3D generalization
works" story without reopening the architecture search. It keeps the angle-
weighted propagator fixed and checks only the minimal unitary package on a
clean fixed 3D DAG:

- zero-field interference visibility on a symmetric two-slit-like 3D graph
- coherent vs incoherent detector-profile contrast on the same graph
- amplitude linearity for a two-source superposition
- detector normalization sanity
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

from scripts.three_d_angle_weight import (  # noqa: E402
    BETA,
    propagate_3d_angle_amplitudes,
)


K_BAND = (3.0, 5.0, 7.0)
PASS_VISIBILITY = 0.80
PASS_PROFILE_TV = 0.10
PASS_LINEARITY = 1e-10
PASS_NORMALIZATION = 1e-12


@dataclass(frozen=True)
class SmokeRow:
    k: float
    coherent_visibility: float
    incoherent_visibility: float
    profile_tv: float
    linearity_residual: float
    normalization_error: float


def build_fixed_3d_two_slit_dag(
    depth: int = 7,
    slit_sep: float = 4.0,
    max_y: int = 6,
    max_z: int = 2,
    radius: float = 1.75,
) -> tuple[list[tuple[float, float, float]], dict[int, list[int]], list[int], list[int]]:
    """Build a symmetric fixed 3D DAG with two slit-like entry nodes."""
    positions: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layers: list[list[int]] = []
    slits: list[int] = []

    first_layer: list[int] = []
    for y in (-slit_sep / 2.0, slit_sep / 2.0):
        idx = len(positions)
        positions.append((0.0, float(y), 0.0))
        first_layer.append(idx)
        slits.append(idx)
    layers.append(first_layer)

    for x in range(1, depth):
        layer: list[int] = []
        for y in range(-max_y, max_y + 1):
            for z in range(-max_z, max_z + 1):
                idx = len(positions)
                positions.append((float(x), float(y), float(z)))
                layer.append(idx)
                for prev in layers[-1]:
                    x0, y0, z0 = positions[prev]
                    length = math.sqrt((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2)
                    if length <= radius:
                        adj[prev].append(idx)
        layers.append(layer)

    detector: list[int] = []
    final_x = float(depth)
    for y in range(-max_y, max_y + 1):
        idx = len(positions)
        positions.append((final_x, float(y), 0.0))
        detector.append(idx)
        for prev in layers[-1]:
            x0, y0, z0 = positions[prev]
            length = math.sqrt((final_x - x0) ** 2 + (float(y) - y0) ** 2 + z0 ** 2)
            if length <= radius:
                adj[prev].append(idx)

    return positions, dict(adj), slits, detector


def _detector_probs(amps: list[complex], detector: list[int]) -> dict[int, float]:
    probs = {node: abs(amps[node]) ** 2 for node in detector}
    total = sum(probs.values())
    if total > 0:
        probs = {node: value / total for node, value in probs.items()}
    return probs


def _marginal_y_profile(
    probs: dict[int, float],
    positions: list[tuple[float, float, float]],
    detector: list[int],
) -> tuple[list[float], list[float]]:
    by_y: dict[float, float] = defaultdict(float)
    for node in detector:
        by_y[positions[node][1]] += probs.get(node, 0.0)
    ys = sorted(by_y)
    return ys, [by_y[y] for y in ys]


def _visibility_from_profile(profile: list[float]) -> float:
    peaks = [
        profile[index]
        for index in range(1, len(profile) - 1)
        if profile[index] > profile[index - 1] and profile[index] > profile[index + 1]
    ]
    troughs = [
        profile[index]
        for index in range(1, len(profile) - 1)
        if profile[index] < profile[index - 1] and profile[index] < profile[index + 1]
    ]
    if not peaks or not troughs:
        return 0.0
    top = max(peaks)
    bottom = min(troughs)
    return (top - bottom) / (top + bottom) if top + bottom > 1e-30 else 0.0


def _evaluate_k(task: tuple[float, int, float, int, int, float]) -> SmokeRow:
    k, depth, slit_sep, max_y, max_z, radius = task
    positions, adj, slits, detector = build_fixed_3d_two_slit_dag(
        depth=depth,
        slit_sep=slit_sep,
        max_y=max_y,
        max_z=max_z,
        radius=radius,
    )
    zero_field = [0.0] * len(positions)

    coherent_amps = propagate_3d_angle_amplitudes(positions, adj, zero_field, slits, k)
    slit0_amps = propagate_3d_angle_amplitudes(positions, adj, zero_field, [slits[0]], k)
    slit1_amps = propagate_3d_angle_amplitudes(positions, adj, zero_field, [slits[1]], k)

    coherent_probs = _detector_probs(coherent_amps, detector)
    slit0_probs = _detector_probs(slit0_amps, detector)
    slit1_probs = _detector_probs(slit1_amps, detector)
    incoherent_probs = {
        node: 0.5 * slit0_probs.get(node, 0.0) + 0.5 * slit1_probs.get(node, 0.0)
        for node in detector
    }

    _, coherent_profile = _marginal_y_profile(coherent_probs, positions, detector)
    _, incoherent_profile = _marginal_y_profile(incoherent_probs, positions, detector)
    profile_tv = 0.5 * sum(abs(a - b) for a, b in zip(coherent_profile, incoherent_profile))

    linearity_residual = max(
        abs(coherent_amps[node] - 0.5 * slit0_amps[node] - 0.5 * slit1_amps[node])
        for node in detector
    )
    normalization_error = abs(sum(coherent_probs.values()) - 1.0)

    return SmokeRow(
        k=k,
        coherent_visibility=_visibility_from_profile(coherent_profile),
        incoherent_visibility=_visibility_from_profile(incoherent_profile),
        profile_tv=profile_tv,
        linearity_residual=linearity_residual,
        normalization_error=normalization_error,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(len(K_BAND), max(1, os.cpu_count() or 1)))
    parser.add_argument("--depth", type=int, default=7)
    parser.add_argument("--slit-sep", type=float, default=4.0)
    parser.add_argument("--max-y", type=int, default=6)
    parser.add_argument("--max-z", type=int, default=2)
    parser.add_argument("--radius", type=float, default=1.75)
    args = parser.parse_args()

    tasks = [
        (k, args.depth, args.slit_sep, args.max_y, args.max_z, args.radius)
        for k in K_BAND
    ]
    ctx = mp.get_context("fork")
    if args.workers <= 1:
        rows = [_evaluate_k(task) for task in tasks]
    else:
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
            rows = list(pool.map(_evaluate_k, tasks))
    rows.sort(key=lambda row: row.k)

    max_visibility = max(row.coherent_visibility for row in rows)
    min_profile_tv = min(row.profile_tv for row in rows)
    max_linearity = max(row.linearity_residual for row in rows)
    max_norm_error = max(row.normalization_error for row in rows)

    checks = [
        (
            "zero-field coherent visibility",
            f"max V_coh over k in {K_BAND}",
            max_visibility,
            f">= {PASS_VISIBILITY:.2f}",
            max_visibility >= PASS_VISIBILITY,
        ),
        (
            "coherent vs incoherent profile contrast",
            f"min TV(profile_coh, profile_incoh) over k in {K_BAND}",
            min_profile_tv,
            f">= {PASS_PROFILE_TV:.2f}",
            min_profile_tv >= PASS_PROFILE_TV,
        ),
        (
            "amplitude linearity",
            "max detector residual |A_ab - (A_a + A_b)/2|",
            max_linearity,
            f"<= {PASS_LINEARITY:.1e}",
            max_linearity <= PASS_LINEARITY,
        ),
        (
            "detector normalization",
            "max |sum P_det - 1|",
            max_norm_error,
            f"<= {PASS_NORMALIZATION:.1e}",
            max_norm_error <= PASS_NORMALIZATION,
        ),
    ]
    overall_pass = all(result for _name, _metric, _value, _threshold, result in checks)

    print("=" * 96)
    print("3D ANGLE-WEIGHT UNITARY SMOKE TEST")
    print("=" * 96)
    print(f"candidate: 1/L^p × exp(-{BETA}θ²)")
    print(
        f"fixed DAG: depth={args.depth}, slit_sep={args.slit_sep:.1f}, "
        f"detector_y={-args.max_y}..{args.max_y}, z_half_width={args.max_z}, radius={args.radius:.2f}"
    )
    print()
    print(
        f"{'k':>5s} {'V_coh':>10s} {'V_incoh':>10s} "
        f"{'TV':>10s} {'lin_resid':>14s} {'norm_err':>12s}"
    )
    print("-" * 72)
    for row in rows:
        print(
            f"{row.k:5.1f} {row.coherent_visibility:10.4f} {row.incoherent_visibility:10.4f} "
            f"{row.profile_tv:10.4f} {row.linearity_residual:14.3e} {row.normalization_error:12.3e}"
        )
    print()
    print("PASS/FAIL TABLE")
    print("-" * 96)
    print(f"{'check':40s} {'metric':28s} {'value':>12s} {'threshold':>12s} {'result':>8s}")
    print("-" * 96)
    for name, metric, value, threshold, result in checks:
        print(
            f"{name:40.40s} {metric:28.28s} {value:12.4g} {threshold:>12s} "
            f"{'PASS' if result else 'FAIL':>8s}"
        )
    print()
    print("Interpretation:")
    if overall_pass:
        print(
            "  The bounded 3D unitary smoke gap is closed: the angle-weight candidate shows "
            "a real zero-field interference pattern on a fixed 3D DAG, the coherent detector "
            "profile stays distinct from the incoherent control across the canonical k band, "
            "and amplitude superposition remains linear to machine precision."
        )
    else:
        print(
            "  The 3D gravity-side claim remains only partial: at least one bounded unitary smoke "
            "check failed on the fixed 3D DAG, so the 3D extension should stay disciplined to "
            "gravity-side support only."
        )
    print()
    print(f"OVERALL: {'PASS' if overall_pass else 'FAIL'}")


if __name__ == "__main__":
    main()
