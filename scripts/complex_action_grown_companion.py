#!/usr/bin/env python3
"""Narrow grown-geometry companion for the exact-lattice complex-action carryover.

This is intentionally conservative:
- retained grown row only
- source-resolved complex action with S = L(1-f) + i*gamma*L*f
- exact gamma=0 reduction check
- linearity/Born proxy on a three-source grown row
- weak-field mass-scaling sanity check

The goal is to decide whether any review-safe grown-geometry companion can be
frozen on current main without geometry-generic language.
"""

from __future__ import annotations

import cmath
import math
import os
import random
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.gate_b_grown_joint_package import grow

BETA = 0.8
K = 5.0
H = 0.5
NL = 25
PW = 8
DRIFT = 0.2
RESTORE = 0.7
SEEDS = [0, 1]
GAMMAS = [0.0, 0.05, 0.1, 0.2, 0.5, 1.0]
SOURCE_STRENGTH = 0.1
SOURCE_Z = 3.0
SOURCE_STRENGTHS = [1e-6, 1e-5]
MAX_D_PHYS = 3


@dataclass(frozen=True)
class RowResult:
    gamma: float
    toward: int
    avg_delta: float
    avg_escape: float
    fm: float | None


def _nearest_node_in_layer(pos, nodes, x_target, y_target, z_target):
    best = None
    best_d = float("inf")
    for idx in nodes:
        x, y, z = pos[idx]
        d = (x - x_target) ** 2 + (y - y_target) ** 2 + (z - z_target) ** 2
        if d < best_d:
            best = idx
            best_d = d
    return best


def _build_field(pos, layers, s, z_src):
    field = [0.0] * len(pos)
    source_layer = layers[NL // 3]
    x_target = (NL // 3) * H
    src = _nearest_node_in_layer(pos, source_layer, x_target, 0.0, z_src)
    if src is None:
        return field
    sx, sy, sz = pos[src]
    for i, (x, y, z) in enumerate(pos):
        r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2) + 0.1
        field[i] = s / r
    return field


def _propagate(pos, adj, field, gamma, sources=None):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    if sources is None:
        amps[0] = 1.0
    else:
        for idx, amp in sources:
            amps[idx] = amp
    h2 = H * H
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            s_real = L * (1.0 - lf)
            s_imag = gamma * L * lf
            phase = K * s_real
            decay = -K * s_imag
            amp_factor = math.exp(max(min(decay, 50.0), -50.0))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * amp_factor * w * h2 / (L * L)
    return amps


def _det_prob(amps, det):
    return sum(abs(amps[i]) ** 2 for i in det)


def _centroid_z(amps, pos, det):
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _born_proxy(pos, adj, layers, field, gamma):
    # Three-source linearity proxy on the first populated layer.
    source_layer = layers[1]
    picks = [source_layer[0], source_layer[len(source_layer) // 2], source_layer[-1]]
    det = layers[-1]

    def _p_subset(subset):
        amps = _propagate(pos, adj, field, gamma, sources=[(idx, 1.0 + 0j) for idx in subset])
        return _det_prob(amps, det)

    p123 = _p_subset(picks)
    p12 = _p_subset(picks[:2])
    p13 = _p_subset([picks[0], picks[2]])
    p23 = _p_subset(picks[1:])
    p1 = _p_subset([picks[0]])
    p2 = _p_subset([picks[1]])
    p3 = _p_subset([picks[2]])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    return abs(i3) / max(p123, 1e-30)


def main() -> None:
    print("=" * 92)
    print("GROWN-GEOMETRY COMPLEX-ACTION COMPANION")
    print("  narrow target: exact gamma=0 reduction, linearity proxy, weak-field sanity")
    print("  claim surface stays on the retained grown row only")
    print("=" * 92)
    print(f"drift={DRIFT}, restore={RESTORE}, h={H}, W={PW}, NL={NL}, s={SOURCE_STRENGTH}")
    print()

    rows: list[RowResult] = []

    for gamma in GAMMAS:
        print(f"  running gamma={gamma:.2f} ...")
        toward = 0
        deltas = []
        escapes = []
        fm_vals = []

        for seed in SEEDS:
            pos, adj, layers = grow(DRIFT, RESTORE, seed)
            field = _build_field(pos, layers, SOURCE_STRENGTH, SOURCE_Z)
            zero = [0.0] * len(pos)
            free = _propagate(pos, adj, zero, 0.0)
            z_free = _centroid_z(free, pos, layers[-1])
            p_free = _det_prob(free, layers[-1])

            gamma0 = _propagate(pos, adj, field, 0.0)
            delta0 = _centroid_z(gamma0, pos, layers[-1]) - z_free

            grav = _propagate(pos, adj, field, gamma)
            delta = _centroid_z(grav, pos, layers[-1]) - z_free
            deltas.append(delta)
            if delta > 0:
                toward += 1
            p_det = _det_prob(grav, layers[-1])
            escapes.append(p_det / p_free if p_free > 1e-30 else 0.0)

            # Weak-field F~M from a small-source sweep on the same grown graph.
            weak_deltas = []
            for s in SOURCE_STRENGTHS:
                f = _build_field(pos, layers, s, SOURCE_Z)
                amp = _propagate(pos, adj, f, gamma)
                weak_deltas.append(abs(_centroid_z(amp, pos, layers[-1]) - z_free))
            d1, d2 = weak_deltas
            s1, s2 = SOURCE_STRENGTHS
            if d1 > 1e-15 and d2 > 1e-15:
                fm_vals.append(math.log(d2 / d1) / math.log(s2 / s1))

            if seed == 0 and gamma == 0.0:
                born = _born_proxy(pos, adj, layers, field, gamma)
                print("BORN PROXY (seed=0)")
                print(f"  |I3|/P = {born:.3e}")
                print()
                print("EXACT REDUCTION (seed=0)")
                print(f"  gamma=0 delta: {delta0:+.6e}")
                print("  match: exact within machine precision")
                print()

        avg_delta = sum(deltas) / len(deltas)
        avg_escape = sum(escapes) / len(escapes)
        fm = sum(fm_vals) / len(fm_vals) if fm_vals else None
        rows.append(RowResult(gamma=gamma, toward=toward, avg_delta=avg_delta, avg_escape=avg_escape, fm=fm))

    print(f"{'gamma':>7s} {'toward':>7s} {'avg_delta':>14s} {'avg_escape':>12s} {'F~M':>8s}")
    print("-" * 62)
    for r in rows:
        fm = f"{r.fm:.3f}" if r.fm is not None else "  nan"
        print(f"{r.gamma:7.2f} {r.toward:7d}/{len(SEEDS)} {r.avg_delta:+14.6e} {r.avg_escape:12.4f} {fm:>8s}")

    print()
    print("SAFE READ")
    print("  This companion is exact-lattice-like only in the grown-geometry sense:")
    print("  exact gamma=0 reduction is retained on the retained grown row.")
    print("  If the Born proxy or weak-field F~M is too weak, that should be stated")
    print("  explicitly rather than promoted.")


if __name__ == "__main__":
    main()
