#!/usr/bin/env python3
"""Gate B complex-action falsifier on the retained grown row.

This is intentionally tiny.

Question:
  Does a minimal complex-action / absorptive factor change detector escape
  on the retained Gate B moderate-drift grown row, while exactly recovering
  the baseline at gamma = 0?

Scope:
  - retained grown geometry row: drift=0.2, restore=0.7
  - one far-field source position: z=3
  - one detector observable: P_det on the final layer
  - one escape ratio: escape(gamma) = P_det(gamma) / P_det(0)
  - gamma=0 is a required guardrail

This does not try to claim a new complex-action theory. It only asks whether
the simplest absorptive extension changes the retained Gate B row in a way
that is not bookkeeping drift.
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


H = 0.5
K = 5.0
MAX_D_PHYS = 3
NL = 25
PW = 8

STRENGTH = 5e-5
DRIFT = 0.2
RESTORE = 0.7
SEEDS = list(range(4))
GAMMAS = [0.0, 0.05, 0.1, 0.2, 0.5]


@dataclass(frozen=True)
class Row:
    seed: int
    p0: float
    p_gamma: dict[float, float]
    escape: dict[float, float]
    delta_z: dict[float, float]


def grow(seed: int):
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(MAX_D_PHYS / H))
    pos: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = {}
    nmap: dict[tuple[int, int, int], int] = {}
    layers: list[list[int]] = []

    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    layers.append([0])

    for layer in range(1, NL):
        x = layer * H
        nodes: list[int] = []
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y = iy * H
                    z = iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0, DRIFT * H)
                    z = pz + rng.gauss(0, DRIFT * H)
                    y = y * (1 - RESTORE) + (iy * H) * RESTORE
                    z = z * (1 - RESTORE) + (iz * H) * RESTORE
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
                nodes.append(idx)
        layers.append(nodes)

        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                edges: list[int] = []
                for dy in range(-2, 3):
                    for dz in range(-2, 3):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            edges.append(di)
                adj[si] = adj.get(si, []) + edges

    return pos, adj, layers, nmap


def setup_slits(pos, layers):
    bl = NL // 3
    barrier = layers[bl]
    sa = [i for i in barrier if pos[i][1] >= 0.5]
    sb = [i for i in barrier if pos[i][1] <= -0.5]
    blocked = set(barrier) - set(sa + sb)
    return barrier, sa, sb, blocked, bl


def source_field(pos, nmap, z_mass: float):
    gl = 2 * NL // 3
    iz_m = round(z_mass / H)
    mi = nmap.get((gl, 0, iz_m))
    if mi is None:
        raise RuntimeError(f"no source node for z={z_mass}")
    field = [0.0] * len(pos)
    mx, my, mz = pos[mi]
    for i in range(len(pos)):
        r = math.sqrt((pos[i][0] - mx) ** 2 + (pos[i][1] - my) ** 2 + (pos[i][2] - mz) ** 2) + 0.1
        field[i] = STRENGTH / r
    return field


def propagate_gamma(pos, adj, field, gamma: float, blocked):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1.0 - lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-0.8 * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * K * act - gamma * act) * w * hm / (L * L)
    return amps


def detector_prob(amps, det):
    return sum(abs(amps[d]) ** 2 for d in det)


def centroid_z(amps, pos, det):
    probs = [abs(amps[d]) ** 2 for d in det]
    tot = sum(probs)
    if tot <= 1e-30:
        return 0.0
    return sum(p * pos[d][2] for p, d in zip(probs, det)) / tot


def main() -> None:
    print("=" * 96)
    print("GATE B COMPLEX-ACTION FALSIFIER")
    print("  retained grown row only: drift=0.2, restore=0.7")
    print("  observable: escape(gamma) = P_det(gamma) / P_det(0)")
    print("  guardrail: gamma=0 must exactly reproduce the baseline on the same row")
    print("=" * 96)
    print(f"h={H}, W={PW}, NL={NL}, seeds={SEEDS}, source_strength={STRENGTH:g}, source_z=3.0")
    print(f"gamma sweep: {GAMMAS}")
    print()

    rows: list[Row] = []
    for seed in SEEDS:
        pos, adj, layers, nmap = grow(seed)
        _, _, _, blocked, _ = setup_slits(pos, layers)
        det = layers[-1]
        field = source_field(pos, nmap, 3.0)

        p0 = detector_prob(propagate_gamma(pos, adj, field, 0.0, blocked), det)
        p_gamma: dict[float, float] = {}
        escape: dict[float, float] = {}
        delta_z: dict[float, float] = {}

        z0 = centroid_z(propagate_gamma(pos, adj, field, 0.0, blocked), pos, det)
        for gamma in GAMMAS:
            amps = propagate_gamma(pos, adj, field, gamma, blocked)
            pg = detector_prob(amps, det)
            p_gamma[gamma] = pg
            escape[gamma] = pg / p0 if p0 > 1e-30 else 0.0
            delta_z[gamma] = centroid_z(amps, pos, det) - z0
        rows.append(Row(seed=seed, p0=p0, p_gamma=p_gamma, escape=escape, delta_z=delta_z))

    print(f"{'seed':>4s} {'P_det(0)':>14s} " + " ".join(f"{g:>10.2f}" for g in GAMMAS[1:]))
    print("-" * 96)
    for row in rows:
        parts = [f"{row.seed:4d}", f"{row.p0:14.6e}"]
        for g in GAMMAS[1:]:
            parts.append(f"{row.escape[g]:10.3f}")
        print(" ".join(parts))

    print()
    print("AGGREGATE")
    p0_mean = sum(r.p0 for r in rows) / len(rows)
    print(f"  mean P_det(0) = {p0_mean:.6e}")
    for g in GAMMAS[1:]:
        pg_mean = sum(r.p_gamma[g] for r in rows) / len(rows)
        esc_mean = sum(r.escape[g] for r in rows) / len(rows)
        dz_mean = sum(r.delta_z[g] for r in rows) / len(rows)
        direction = "TOWARD" if dz_mean > 0 else "AWAY"
        print(
            f"  gamma={g:>4.2f}  mean P_det={pg_mean:.6e}  "
            f"escape={esc_mean:.3f}  delta_z={dz_mean:+.6e} ({direction})"
        )

    print()
    print("SAFE READ")
    print("  gamma=0 is exactly the retained Gate B baseline by construction.")
    print("  The probe only asks whether a minimal absorptive/complex-action term")
    print("  changes the detector escape on the retained grown row.")
    print("  Any stronger interpretation would need a separate retained note.")


if __name__ == "__main__":
    main()
