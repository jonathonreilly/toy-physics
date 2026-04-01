#!/usr/bin/env python3
"""Strict 3D same-graph single-vs-double-slit visibility lane.

This is the review-safe visibility companion to the retained 3D modular
gravity/decoherence work.

Goal
----
Measure a true single-vs-double-slit visibility gain on the same retained
3D modular DAG instances used for the gravity/decoherence-style reads.
The comparison uses:
  - the same modular graph family
  - the same propagator and mass field setting
  - fixed y-binned detector profiles
  - a small envelope smoothing step

The claim is intentionally narrow:
  - report coherent two-slit visibility
  - report the incoherent single-slit average visibility
  - report visibility gain = V_coh - V_single
  - keep the conclusion limited to the retained 3D modular family

PStack experiment: three-d-joint-visibility-strict
"""

from __future__ import annotations

import math
import os
import sys
import time
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.three_d_joint_test import (  # type: ignore  # noqa: E402
    compute_field_3d,
    generate_3d_dag,
    propagate_3d,
)

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)
GAP = 3.0
CONNECT_RADIUS = 4.0
N_SEEDS = 8
N_LAYERS_LIST = (12, 18, 25, 40, 60, 80, 100)
NODES_PER_LAYER = 30
XYZ_RANGE = 12.0
N_BINS = 12
Y_MIN = -12.0
Y_MAX = 12.0
SMOOTH_RADIUS = 1


def _detector_probs(amps: list[complex], det_list: list[int]) -> dict[int, float]:
    probs = {d: abs(amps[d]) ** 2 for d in det_list}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p / total for d, p in probs.items()}
    return probs


def _binned_profile(
    probs: dict[int, float],
    positions: list[tuple[float, float, float]],
    det_list: list[int],
    *,
    y_min: float = Y_MIN,
    y_max: float = Y_MAX,
    n_bins: int = N_BINS,
) -> list[float]:
    bw = (y_max - y_min) / n_bins
    bins = [0.0] * n_bins
    for d in det_list:
        y = positions[d][1]
        b = int((y - y_min) / bw)
        b = max(0, min(n_bins - 1, b))
        bins[b] += probs.get(d, 0.0)
    return bins


def _smooth(profile: list[float], radius: int = SMOOTH_RADIUS) -> list[float]:
    if radius <= 0 or len(profile) < 3:
        return profile[:]
    out = []
    for i in range(len(profile)):
        lo = max(0, i - radius)
        hi = min(len(profile), i + radius + 1)
        window = profile[lo:hi]
        out.append(sum(window) / len(window))
    return out


def _profile_visibility(profile: list[float]) -> float:
    smooth = _smooth(profile)
    if len(smooth) < 3:
        return 0.0
    peaks = [
        smooth[i]
        for i in range(1, len(smooth) - 1)
        if smooth[i] > smooth[i - 1] and smooth[i] > smooth[i + 1]
    ]
    troughs = [
        smooth[i]
        for i in range(1, len(smooth) - 1)
        if smooth[i] < smooth[i - 1] and smooth[i] < smooth[i + 1]
    ]
    if not peaks or not troughs:
        return 0.0
    top = max(peaks)
    bottom = min(troughs)
    return (top - bottom) / (top + bottom) if top + bottom > 1e-30 else 0.0


def _setup_graph(
    n_layers: int,
    seed: int,
):
    positions, adj = generate_3d_dag(
        n_layers=n_layers,
        nodes_per_layer=NODES_PER_LAYER,
        xyz_range=XYZ_RANGE,
        connect_radius=CONNECT_RADIUS,
        rng_seed=seed,
        gap=GAP,
    )[:2]

    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = sum(positions[i][1] for i in range(len(positions))) / len(positions)
    bl_idx = len(layers) // 3
    barrier = by_layer[layers[bl_idx]]
    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:3]
    slit_b = [i for i in barrier if positions[i][1] < cy - 3][:3]
    if not slit_a or not slit_b:
        return None
    blocked = set(barrier) - set(slit_a + slit_b)

    env_depth = max(1, round(n_layers / 6))
    start = bl_idx + 1
    stop = min(len(layers), start + env_depth)
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])
    if not mid:
        return None

    mass_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[mass_layer] if positions[i][1] > cy + 1][:8]
    if not mass_nodes:
        return None

    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * len(positions)

    return {
        "positions": positions,
        "adj": adj,
        "src": src,
        "det_list": det_list,
        "blocked": blocked,
        "slit_a": slit_a,
        "slit_b": slit_b,
        "mid": mid,
        "field_m": field_m,
        "field_f": field_f,
    }


def _visibility_gain_for_graph(positions, adj, src, det_list, blocked, slit_a, slit_b, field, k):
    amps_both = propagate_3d(positions, adj, field, src, k, blocked)
    amps_a = propagate_3d(positions, adj, field, src, k, blocked | set(slit_b))
    amps_b = propagate_3d(positions, adj, field, src, k, blocked | set(slit_a))

    probs_both = _detector_probs(amps_both, det_list)
    probs_a = _detector_probs(amps_a, det_list)
    probs_b = _detector_probs(amps_b, det_list)

    probs_single_avg = {
        d: 0.5 * probs_a.get(d, 0.0) + 0.5 * probs_b.get(d, 0.0)
        for d in det_list
    }

    prof_both = _binned_profile(probs_both, positions, det_list)
    prof_single = _binned_profile(probs_single_avg, positions, det_list)
    v_coh = _profile_visibility(prof_both)
    v_single = _profile_visibility(prof_single)
    return v_coh, v_single, v_coh - v_single


def main() -> None:
    print("=" * 78)
    print("3D STRICT SAME-GRAPH VISIBILITY")
    print("  retained family: 3D modular DAG, gap=3.0")
    print("  metric: binned single-vs-double-slit visibility gain on same graph")
    print("  detector profiles: fixed y-bins with light envelope smoothing")
    print("=" * 78)
    print()
    print(f"  seeds per N: {N_SEEDS}")
    print(f"  k-band: {list(K_BAND)}")
    print(f"  y-bins: {N_BINS} over [{Y_MIN:.1f}, {Y_MAX:.1f}]")
    print(f"  smoothing radius: {SMOOTH_RADIUS}")
    print()

    seeds = [7 * s + 3 for s in range(N_SEEDS)]
    rows = []

    print("  N   V_coh   V_single   V_gain    n_ok   time")
    print("  " + "-" * 50)
    for nl in N_LAYERS_LIST:
        t0 = time.time()
        v_coh_list = []
        v_single_list = []
        v_gain_list = []

        for seed in seeds:
            setup = _setup_graph(nl, seed)
            if setup is None:
                continue

            for k in K_BAND:
                v_coh, v_single, v_gain = _visibility_gain_for_graph(
                    setup["positions"],
                    setup["adj"],
                    setup["src"],
                    setup["det_list"],
                    setup["blocked"],
                    setup["slit_a"],
                    setup["slit_b"],
                    setup["field_m"],
                    k,
                )
                v_coh_list.append(v_coh)
                v_single_list.append(v_single)
                v_gain_list.append(v_gain)

        dt = time.time() - t0
        if not v_gain_list:
            print(f"  {nl:4d}  FAIL")
            continue

        avg_v_coh = sum(v_coh_list) / len(v_coh_list)
        avg_v_single = sum(v_single_list) / len(v_single_list)
        avg_v_gain = sum(v_gain_list) / len(v_gain_list)
        rows.append((nl, avg_v_coh, avg_v_single, avg_v_gain, len(v_gain_list)))
        print(
            f"  {nl:4d}  {avg_v_coh:6.3f}   {avg_v_single:7.3f}   {avg_v_gain:+7.3f}   "
            f"{len(v_gain_list):4d}  {dt:4.0f}s"
        )

    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    if rows:
        tail = [r for r in rows if r[0] >= 40]
        if tail:
            tail_gain = sum(r[3] for r in tail) / len(tail)
            tail_coh = sum(r[1] for r in tail) / len(tail)
            tail_single = sum(r[2] for r in tail) / len(tail)
            print(f"  Large-N mean V_coh (N>=40): {tail_coh:.4f}")
            print(f"  Large-N mean V_single (N>=40): {tail_single:.4f}")
            print(f"  Large-N mean V_gain (N>=40): {tail_gain:+.4f}")
            if tail_gain > 0.01:
                print("  Verdict: retained 3D lane shows a positive strict visibility gain.")
            elif tail_gain > -0.01:
                print("  Verdict: retained 3D lane is effectively flat under the strict metric.")
            else:
                print("  Verdict: retained 3D lane loses visibility under the strict metric.")
    print("  Claim boundary: same retained 3D modular family only.")
    print("=" * 78)


if __name__ == "__main__":
    main()
