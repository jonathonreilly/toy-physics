#!/usr/bin/env python3
"""Complex-action sweep for the alternative connectivity family.

This asks whether the parity-rotated sector-transition family also carries the
complex-action companion on the no-restore grown slice.
"""

from __future__ import annotations

import math
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP import (
    Family,
    _build_alt_connectivity,
    _field_from_sources,
    _mean,
    H,
    K,
    NL,
    SOURCE_Z,
)
from gate_b_no_restore_farfield import grow


DRIFTS = [0.15, 0.20, 0.25]
SEEDS = [0, 1, 2]
GAMMAS = [0.0, 0.1, 0.2, 0.5]
SOURCE_STRENGTH = 0.1


def _propagate(pos, adj, field, gamma):
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
            act = L * (1.0 - lf)
            decay = -gamma * L * lf
            if decay < -50:
                damp = 0.0
            elif decay > 50:
                damp = math.exp(50)
            else:
                damp = math.exp(decay)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-0.8 * theta * theta)
            amps[j] += ai * complex(math.cos(K * act), math.sin(K * act)) * damp * w * hm / (L * L)
    return amps


def _centroid_z(amps, pos, det):
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _det_prob(amps, det):
    return sum(abs(amps[i]) ** 2 for i in det)


def _measure(drift: float, seed: int):
    pos, adj, layers, _nmap = grow(drift, seed)
    fam = Family(pos, layers, adj)
    alt = _build_alt_connectivity(fam)
    det = alt.layers[-1]
    free = _propagate(alt.positions, alt.adj, [0.0] * len(alt.positions), 0.0)
    z_free = _centroid_z(free, alt.positions, det)

    field = _field_from_sources(alt.positions, alt.layers, [(SOURCE_Z, +1)])

    zero = _centroid_z(_propagate(alt.positions, alt.adj, field, 0.0), alt.positions, det) - z_free
    g01 = _centroid_z(_propagate(alt.positions, alt.adj, field, 0.1), alt.positions, det) - z_free
    g02 = _centroid_z(_propagate(alt.positions, alt.adj, field, 0.2), alt.positions, det) - z_free
    g05 = _centroid_z(_propagate(alt.positions, alt.adj, field, 0.5), alt.positions, det) - z_free
    p_free = _det_prob(free, det)
    esc01 = _det_prob(_propagate(alt.positions, alt.adj, field, 0.1), det) / p_free if p_free > 1e-30 else 0.0
    esc05 = _det_prob(_propagate(alt.positions, alt.adj, field, 0.5), det) / p_free if p_free > 1e-30 else 0.0

    weak_deltas_0 = []
    weak_deltas_05 = []
    for s in [1e-6, 1e-5]:
        weak_field = _field_from_sources(alt.positions, alt.layers, [(SOURCE_Z, +1)])
        weak_field = [v * (s / 1e-6) for v in weak_field]
        weak_deltas_0.append(abs(_centroid_z(_propagate(alt.positions, alt.adj, weak_field, 0.0), alt.positions, det) - z_free))
        weak_deltas_05.append(abs(_centroid_z(_propagate(alt.positions, alt.adj, weak_field, 0.5), alt.positions, det) - z_free))
    fm0 = math.log(weak_deltas_0[1] / weak_deltas_0[0]) / math.log(10.0) if weak_deltas_0[0] > 1e-15 and weak_deltas_0[1] > 1e-15 else math.nan
    fm05 = math.log(weak_deltas_05[1] / weak_deltas_05[0]) / math.log(10.0) if weak_deltas_05[0] > 1e-15 and weak_deltas_05[1] > 1e-15 else math.nan

    return zero, g01, g02, g05, esc01, esc05, fm0, fm05


def main() -> None:
    print("=" * 96)
    print("ALT CONNECTIVITY FAMILY COMPLEX SWEEP")
    print("  parity-rotated sector-transition family on the no-restore grown slice")
    print("=" * 96)
    print(f"drifts={DRIFTS}, seeds={SEEDS}, gammas={GAMMAS}")
    print()
    print(f"{'drift':>5s} {'seed':>4s} {'g0':>12s} {'g01':>12s} {'g02':>12s} {'g05':>12s} {'e01':>8s} {'e05':>8s} {'fm0':>7s} {'fm05':>7s} {'ok':>4s}")
    print("-" * 110)

    rows = []
    for drift in DRIFTS:
        for seed in SEEDS:
            row = _measure(drift, seed)
            rows.append((drift, seed, *row))
            zero, g01, g02, g05, esc01, esc05, fm0, fm05 = row
            ok = (
                abs(zero) < 1e-12
                and g01 > 0.0
                and g05 < 0.0
                and not math.isnan(fm0)
                and not math.isnan(fm05)
                and abs(fm0 - 1.0) < 0.05
                and abs(fm05 - 1.0) < 0.05
            )
            print(
                f"{drift:5.2f} {seed:4d} {zero:+12.3e} {g01:+12.3e} {g02:+12.3e} {g05:+12.3e} "
                f"{esc01:8.3f} {esc05:8.3f} {fm0:7.3f} {fm05:7.3f} {'YES' if ok else 'no':>4s}"
            )

    print()
    print("SAFE READ")
    print("  complex-action on the alternative family is a boundary test, not yet a retained claim")


if __name__ == "__main__":
    main()
