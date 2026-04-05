#!/usr/bin/env python3
"""Gate B grown frontier probe.

This is a narrow follow-up to the retained grown trapping transport probe.

Question:
  Can the same retained Gate B grown row support one stronger frontier
  observable than plain detector escape, while still reducing exactly back
  to the retained grown baseline at eta = 0?

Scope:
  - retained grown geometry row only: drift=0.2, restore=0.7
  - one static source field on the same row
  - one narrow trap slab near the middle of the transport path
  - two observables:
      * escape(eta) = P_det(eta) / P_det(0)
      * frontier_bias(eta) = (P_frontier - P_core) / P_det
  - exact eta = 0 reduction check

The promoted frontier observable is the detector-layer core/frontier contrast.
The escape ratio remains as the transport control.
"""

from __future__ import annotations

import cmath
import math
import random
import time
from dataclasses import dataclass

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
H = 0.5
NL = 25
PW = 8
DRIFT = 0.2
RESTORE = 0.7
SEEDS = list(range(4))
TRAP_ETAS = [0.0, 0.05, 0.1, 0.2, 0.35, 0.5]
Z_MASS = 3.0
FIELD_STRENGTH = 5e-5
FIELD_EPS = 0.1
TRAP_LAYERS = {NL // 2 - 1, NL // 2, NL // 2 + 1}
TRAP_RADIUS = 2.0
CORE_Z = 2.0
FRONTIER_Z = 5.0


@dataclass(frozen=True)
class SeedResult:
    seed: int
    p0: float
    escape: dict[float, float]
    frontier_bias: dict[float, float]
    frontier_share: dict[float, float]


def _mean(values):
    return sum(values) / len(values) if values else math.nan


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
                    y = py + rng.gauss(0.0, DRIFT * H)
                    z = pz + rng.gauss(0.0, DRIFT * H)
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


def source_field(pos, nmap):
    gl = 2 * NL // 3
    iz_m = round(Z_MASS / H)
    mi = nmap.get((gl, 0, iz_m))
    if mi is None:
        raise RuntimeError(f"no source node for z={Z_MASS}")
    field = [0.0] * len(pos)
    mx, my, mz = pos[mi]
    for i in range(len(pos)):
        r = math.sqrt((pos[i][0] - mx) ** 2 + (pos[i][1] - my) ** 2 + (pos[i][2] - mz) ** 2) + FIELD_EPS
        field[i] = FIELD_STRENGTH / r
    return field


def trap_nodes(pos, layers):
    out = set()
    for layer in TRAP_LAYERS:
        if layer < 0 or layer >= len(layers):
            continue
        for idx in layers[layer]:
            _, y, z = pos[idx]
            if abs(y) <= TRAP_RADIUS and abs(z) <= TRAP_RADIUS:
                out.add(idx)
    return out


def propagate(pos, adj, field, blocked, trap, eta: float):
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
            w = math.exp(-BETA * theta * theta)
            contrib = amps[i] * cmath.exp(1j * K * act) * w * hm / (L * L)
            if eta > 0.0 and j in trap:
                contrib *= (1.0 - eta)
            amps[j] += contrib
    return amps


def detector_prob(amps, det):
    return sum(abs(amps[d]) ** 2 for d in det)


def detector_band_probs(amps, pos, det):
    core = []
    frontier = []
    for d in det:
        _, _, z = pos[d]
        p = abs(amps[d]) ** 2
        if abs(z) <= CORE_Z:
            core.append(p)
        if abs(z) >= FRONTIER_Z:
            frontier.append(p)
    p_core = sum(core)
    p_frontier = sum(frontier)
    p_mid = sum(
        abs(amps[d]) ** 2
        for d in det
        if abs(pos[d][2]) > CORE_Z and abs(pos[d][2]) < FRONTIER_Z
    )
    p_det = p_core + p_mid + p_frontier
    return p_det, p_core, p_frontier


def main() -> None:
    t0 = time.time()
    print("=" * 96)
    print("GATE B GROWN FRONTIER PROBE")
    print("  retained grown row only: drift=0.2, restore=0.7")
    print("  promoted observable: frontier_bias(eta) = (P_frontier - P_core) / P_det")
    print("  transport control: escape(eta) = P_det(eta) / P_det(0)")
    print("  guardrail: eta=0 must exactly reproduce the retained grown baseline")
    print("=" * 96)
    print(
        f"h={H}, W={PW}, NL={NL}, seeds={SEEDS}, "
        f"trap_layers={sorted(TRAP_LAYERS)}, trap_radius={TRAP_RADIUS}, "
        f"core_z={CORE_Z}, frontier_z={FRONTIER_Z}"
    )
    print(f"eta sweep: {TRAP_ETAS}")
    print()

    rows: list[SeedResult] = []
    for seed in SEEDS:
        pos, adj, layers, nmap = grow(seed)
        det = layers[-1]
        field = source_field(pos, nmap)
        blocked = set()
        trap = trap_nodes(pos, layers)

        base = propagate(pos, adj, field, blocked, trap, 0.0)
        p0 = detector_prob(base, det)
        p_det0, p_core0, p_front0 = detector_band_probs(base, pos, det)
        if abs(p_det0 - p0) > 1e-12:
            raise RuntimeError("detector band partition does not match total detector mass")
        base_frontier_bias = (p_front0 - p_core0) / p_det0 if p_det0 > 1e-30 else 0.0

        escape: dict[float, float] = {}
        frontier_bias: dict[float, float] = {}
        frontier_share: dict[float, float] = {}
        for eta in TRAP_ETAS:
            amps = propagate(pos, adj, field, blocked, trap, eta)
            p_eta = detector_prob(amps, det)
            _, p_core, p_front = detector_band_probs(amps, pos, det)
            escape[eta] = p_eta / p0 if p0 > 1e-30 else 0.0
            frontier_share[eta] = p_front / p_eta if p_eta > 1e-30 else 0.0
            frontier_bias[eta] = ((p_front - p_core) / p_eta - base_frontier_bias) if p_eta > 1e-30 else 0.0

        rows.append(
            SeedResult(
                seed=seed,
                p0=p0,
                escape=escape,
                frontier_bias=frontier_bias,
                frontier_share=frontier_share,
            )
        )

    print("eta=0 exact reduction: escape=1.000 and frontier_bias=0.000 by construction on the retained grown baseline")
    print()
    print(f"{'seed':>4s} {'P_det(0)':>14s} " + " ".join(f"{eta:>10.2f}" for eta in TRAP_ETAS[1:]))
    print("-" * 96)
    for row in rows:
        vals = [f"{row.seed:4d}", f"{row.p0:14.6e}"]
        for eta in TRAP_ETAS[1:]:
            vals.append(f"{row.escape[eta]:10.3f}")
        print(" ".join(vals))

    print()
    print("AGGREGATE")
    p0_mean = _mean([r.p0 for r in rows])
    print(f"  mean P_det(0) = {p0_mean:.6e}")
    for eta in TRAP_ETAS[1:]:
        esc = [r.escape[eta] for r in rows]
        fb = [r.frontier_bias[eta] for r in rows]
        fs = [r.frontier_share[eta] for r in rows]
        esc_mean = _mean(esc)
        fb_mean = _mean(fb)
        fs_mean = _mean(fs)
        trapped = 1.0 - esc_mean
        print(
            f"  eta={eta:>4.2f}  escape={esc_mean:6.3f}  trapped={trapped:6.3f}  "
            f"frontier_share={fs_mean:6.3f}  frontier_bias={fb_mean:+7.4f}"
        )

    print()
    print("SAFE READ")
    print("  eta=0 reproduces the retained grown baseline exactly by construction.")
    print("  The promoted observable is the detector frontier bias, not just escape.")
    print("  Escape tells us how much transport survives; frontier bias tells us")
    print("  whether the surviving mass shifts toward the outer detector shell.")
    print("  If frontier_bias moves steadily with eta, the trap is doing more than")
    print("  simple attenuation.")
    print()
    print(f"Total time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
