#!/usr/bin/env python3
"""Gate B non-label connectivity v1 joint-package companion.

This freezes one bounded question on the same no-restore grown family used by
gate_b_nonlabel_connectivity_v1.py:

  Does the geometry-sector stencil keep the Born / d_TV / MI / decoherence
  observables in the same qualitative regime as the exact grid on a cheap
  bounded replay?

The comparison is intentionally narrow:
  - exact grid control
  - geometry-sector stencil on the no-restore grown family

Only the joint package observables are measured here.
"""

from __future__ import annotations

import cmath
import math
import random
import time
from dataclasses import dataclass


BETA = 0.8
K = 5.0
H = 0.5
NL = 25
HALF = 10
SEEDS = list(range(4))
DRIFT = 0.2
MAX_D_PHYS = 3
LAM = 10.0
N_YBINS = 8


@dataclass
class Family:
    name: str
    positions: list[tuple[float, float, float]]
    layers: list[list[int]]
    adj: dict[int, list[int]]


@dataclass
class JointRow:
    label: str
    born: float
    d_tv: float
    mi: float
    decoh: float


def _grid_index(layer: int, iy: int, iz: int, half: int) -> int:
    span = 2 * half + 1
    return layer * span * span + (iy + half) * span + (iz + half)


def _build_exact_grid(n_layers: int, half: int) -> Family:
    positions: list[tuple[float, float, float]] = []
    layers: list[list[int]] = []
    adj: dict[int, list[int]] = {}

    for layer in range(n_layers):
        x = layer * H
        nodes: list[int] = []
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                idx = len(positions)
                positions.append((x, iy * H, iz * H))
                nodes.append(idx)
        layers.append(nodes)

    for layer in range(n_layers - 1):
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                src = _grid_index(layer, iy, iz, half)
                nbs: list[int] = []
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        jy = iy + dy
                        jz = iz + dz
                        if -half <= jy <= half and -half <= jz <= half:
                            nbs.append(_grid_index(layer + 1, jy, jz, half))
                adj[src] = nbs

    return Family("exact grid", positions, layers, adj)


def _build_no_restore_family(n_layers: int, half: int, drift: float, seed: int) -> Family:
    rng = random.Random(seed)
    positions: list[tuple[float, float, float]] = []
    layers: list[list[int]] = []
    state: dict[tuple[int, int], tuple[float, float]] = {}

    for layer in range(n_layers):
        x = layer * H
        nodes: list[int] = []
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                if layer == 0:
                    y, z = iy * H, iz * H
                else:
                    py, pz = state[(iy, iz)]
                    y = py + rng.gauss(0.0, drift * H)
                    z = pz + rng.gauss(0.0, drift * H)
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                state[(iy, iz)] = (y, z)
        layers.append(nodes)

    return Family(f"no-restore drift={drift:g}", positions, layers, {})


def _build_geometry_sector_connectivity(family: Family, half: int) -> Family:
    """Geometry-only forward stencil.

    For each source node, use the source's actual position and the next-layer
    node positions to select one representative in each of the local 3x3
    (dy,dz) sectors, then backfill to a small edge floor.
    """

    positions = family.positions
    layers = family.layers
    adj: dict[int, list[int]] = {}

    for layer in range(len(layers) - 1):
        dst_nodes = layers[layer + 1]
        dst_positions = [positions[i] for i in dst_nodes]
        for iy in range(-half, half + 1):
            for iz in range(-half, half + 1):
                src = _grid_index(layer, iy, iz, half)
                sx, sy, sz = positions[src]
                sector_best: dict[tuple[int, int], tuple[float, int]] = {}
                ranked: list[tuple[float, int]] = []
                for dst, (dx, dy, dz) in zip(dst_nodes, dst_positions):
                    dyc = dy - sy
                    dzc = dz - sz
                    by = max(-1, min(1, int(round(dyc / H))))
                    bz = max(-1, min(1, int(round(dzc / H))))
                    dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                    ranked.append((dist2, dst))
                    key = (by, bz)
                    prev = sector_best.get(key)
                    if prev is None or dist2 < prev[0]:
                        sector_best[key] = (dist2, dst)

                selected = [dst for _, dst in sorted(sector_best.values(), key=lambda item: item[0])]
                for _, dst in sorted(ranked, key=lambda item: item[0]):
                    if len(selected) >= 9:
                        break
                    if dst not in selected:
                        selected.append(dst)
                for _, dst in sorted(ranked, key=lambda item: item[0]):
                    if len(selected) >= 5:
                        break
                    if dst not in selected:
                        selected.append(dst)
                adj[src] = selected

    return Family(f"{family.name} + geometry-sector stencil", positions, layers, adj)


def _propagate(
    positions: list[tuple[float, float, float]],
    layers: list[list[int]],
    adj: dict[int, list[int]],
    field: list[float],
) -> list[complex]:
    amps = [0j] * len(positions)
    source = layers[0][len(layers[0]) // 2]
    amps[source] = 1.0
    hm = H * H
    for layer in range(len(layers) - 1):
        for i in layers[layer]:
            ai = amps[i]
            if abs(ai) < 1e-30:
                continue
            xi, yi, zi = positions[i]
            for j in adj.get(i, []):
                xj, yj, zj = positions[j]
                dx = xj - xi
                dy = yj - yi
                dz = zj - zi
                L = math.sqrt(dx * dx + dy * dy + dz * dz)
                if L < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                act = L * (1.0 - lf)
                theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                amps[j] += ai * cmath.exp(1j * K * act) * w * hm / (L * L)
    return amps


def _setup_slits(pos: list[tuple[float, float, float]], layers: list[list[int]]):
    bl = NL // 3
    barrier = layers[bl]
    sa = [i for i in barrier if pos[i][1] >= 0.5]
    sb = [i for i in barrier if pos[i][1] <= -0.5]
    blocked = set(barrier) - set(sa + sb)
    return barrier, sa, sb, blocked, bl


def _born_measure(pos: list[tuple[float, float, float]], adj: dict[int, list[int]], barrier: list[int], det: list[int], layers: list[list[int]]) -> float:
    upper = sorted([i for i in barrier if pos[i][1] > 1.0], key=lambda i: pos[i][1])
    lower = sorted([i for i in barrier if pos[i][1] < -1.0], key=lambda i: -pos[i][1])
    middle = sorted(
        [i for i in barrier if abs(pos[i][1]) <= 1.0 and abs(pos[i][2]) <= 1.0],
        key=lambda i: abs(pos[i][1]) + abs(pos[i][2]),
    )
    if not upper or not lower or not middle:
        return float("nan")
    s_a = [upper[0]]
    s_b = [lower[0]]
    s_c = [middle[0]]
    all_s = set(s_a + s_b + s_c)
    other = set(barrier) - all_s
    probs = {}
    for key, open_set in [
        ("abc", all_s),
        ("ab", set(s_a + s_b)),
        ("ac", set(s_a + s_c)),
        ("bc", set(s_b + s_c)),
        ("a", set(s_a)),
        ("b", set(s_b)),
        ("c", set(s_c)),
    ]:
        blocked = other | (all_s - open_set)
        adj2 = {k: [j for j in v if j not in blocked] for k, v in adj.items()}
        amps = _propagate(pos, layers, adj2, [0.0] * len(pos))
        probs[key] = [abs(amps[d]) ** 2 for d in det]
    i3_sum = 0.0
    p_sum = 0.0
    for di in range(len(det)):
        i3 = (
            probs["abc"][di]
            - probs["ab"][di]
            - probs["ac"][di]
            - probs["bc"][di]
            + probs["a"][di]
            + probs["b"][di]
            + probs["c"][di]
        )
        i3_sum += abs(i3)
        p_sum += probs["abc"][di]
    return i3_sum / p_sum if p_sum > 1e-30 else float("nan")


def _measure_joint_row(family: Family) -> JointRow:
    pos = family.positions
    layers = family.layers
    adj = family.adj
    det = layers[-1]
    barrier, sa, sb, blocked, bl = _setup_slits(pos, layers)

    born = _born_measure(pos, adj, barrier, det, layers)

    # Use the same slit-opening split as the grown-geometry harness.
    pa = _propagate(pos, layers, {k: [j for j in v if j not in set(sb)] for k, v in adj.items()}, [0.0] * len(pos))
    pb = _propagate(pos, layers, {k: [j for j in v if j not in set(sa)] for k, v in adj.items()}, [0.0] * len(pos))

    da = [abs(pa[d]) ** 2 for d in det]
    db = [abs(pb[d]) ** 2 for d in det]
    na = sum(da)
    nb = sum(db)
    d_tv = 0.0
    if na > 1e-30 and nb > 1e-30:
        d_tv = 0.5 * sum(abs(a / na - b / nb) for a, b in zip(da, db))

    bw = 2 * (HALF + 1) / N_YBINS
    ed = max(1, round(NL / 6))
    st = bl + 1
    sp = min(NL - 1, st + ed)
    mid = []
    for layer in range(st, sp):
        mid.extend(layers[layer])
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid:
        b2 = max(0, min(N_YBINS - 1, int((pos[m][1] + HALF + 1) / bw)))
        ba[b2] += pa[m]
        bb[b2] += pb[m]
    s_overlap = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    na3 = sum(abs(a) ** 2 for a in ba)
    nb3 = sum(abs(b) ** 2 for b in bb)
    sn = s_overlap / (na3 + nb3) if (na3 + nb3) > 0 else 0.0
    dcl = math.exp(-LAM**2 * sn)

    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1, d2)] = (
                pa[d1].conjugate() * pa[d2]
                + pb[d1].conjugate() * pb[d2]
                + dcl * pa[d1].conjugate() * pb[d2]
                + dcl * pb[d1].conjugate() * pa[d2]
            )
    tr = sum(rho[(d, d)] for d in det).real
    pur = 1.0
    if tr > 1e-30:
        for key in rho:
            rho[key] /= tr
        pur = float(sum(abs(v) ** 2 for v in rho.values()).real)
    decoh = 100 * (1 - pur)

    mi = 0.0
    prob_a = [0.0] * N_YBINS
    prob_b = [0.0] * N_YBINS
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d][1] + HALF + 1) / bw)))
        prob_a[b2] += abs(pa[d]) ** 2
        prob_b[b2] += abs(pb[d]) ** 2
    na_prob = sum(prob_a)
    nb_prob = sum(prob_b)
    if na_prob > 1e-30 and nb_prob > 1e-30:
        pa_n = [v / na_prob for v in prob_a]
        pb_n = [v / nb_prob for v in prob_b]
        h_val = 0.0
        hc = 0.0
        for b2 in range(N_YBINS):
            pmix = 0.5 * pa_n[b2] + 0.5 * pb_n[b2]
            if pmix > 1e-30:
                h_val -= pmix * math.log2(pmix)
            if pa_n[b2] > 1e-30:
                hc -= 0.5 * pa_n[b2] * math.log2(pa_n[b2])
            if pb_n[b2] > 1e-30:
                hc -= 0.5 * pb_n[b2] * math.log2(pb_n[b2])
        mi = h_val - hc

    return JointRow(family.name, born, d_tv, mi, decoh)


def _aggregate(rows: list[JointRow], label: str) -> JointRow:
    return JointRow(
        label=label,
        born=sum(r.born for r in rows) / len(rows),
        d_tv=sum(r.d_tv for r in rows) / len(rows),
        mi=sum(r.mi for r in rows) / len(rows),
        decoh=sum(r.decoh for r in rows) / len(rows),
    )


def main() -> None:
    t0 = time.time()
    print("=" * 74)
    print("GATE B NON-LABEL CONNECTIVITY V1 JOINT PACKAGE")
    print("  Born / d_TV / MI / decoherence on exact grid vs geometry-sector stencil")
    print("=" * 74)
    print(f"h={H}, W={HALF}, NL={NL}, seeds={len(SEEDS)}, drift={DRIFT}")
    print("growth rule: template previous layer + drift, then geometry-sector connectivity")
    print()
    print(f"{'geometry':<24} {'Born':>10} {'d_TV':>8} {'MI':>8} {'Decoh':>8}")

    exact_family = _build_exact_grid(NL, HALF)
    exact_rows = [_measure_joint_row(exact_family) for _ in SEEDS]
    exact = _aggregate(exact_rows, "exact grid")
    print(f"{exact.label:<24} {exact.born:>10.2e} {exact.d_tv:>8.3f} {exact.mi:>8.3f} {exact.decoh:>7.1f}%")

    sector_rows: list[JointRow] = []
    for seed in SEEDS:
        grown = _build_no_restore_family(NL, HALF, DRIFT, seed)
        sector_family = _build_geometry_sector_connectivity(grown, HALF)
        sector_rows.append(_measure_joint_row(sector_family))
    sector = _aggregate(sector_rows, "geometry-sector stencil")
    print(f"{sector.label:<24} {sector.born:>10.2e} {sector.d_tv:>8.3f} {sector.mi:>8.3f} {sector.decoh:>7.1f}%")

    print()
    print("SAFE INTERPRETATION")
    print("  This harness freezes one geometry-only joint-package candidate.")
    print("  It should be read as a bounded comparison on the no-restore grown family,")
    print("  not as a full Gate B closure or a universal non-label connectivity theorem.")
    print(f"\nTotal time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
