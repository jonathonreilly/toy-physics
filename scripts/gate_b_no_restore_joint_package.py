#!/usr/bin/env python3
"""Gate B no-restore joint package harness.

Freeze the bounded Born / d_TV / MI / decoherence comparison on the same
grown-geometry family with restore fixed to 0. This asks how much of the
non-gravity package survives when the restoring pull toward the grid is
removed entirely.

The comparison is intentionally narrow:
- exact grid reference
- no-restore grown rows at a few drift values

This is a companion to gate_b_grown_joint_package.py, but it isolates the
no-restore lane the user asked for.
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
PW = 10
MAX_D_PHYS = 3
LAM = 10.0
N_YBINS = 8
SEEDS = [0]
ROWS = [
    ("exact grid", 0.0, 1.0),
    ("no restore drift=0.0", 0.0, 0.0),
    ("no restore drift=0.2", 0.2, 0.0),
    ("no restore drift=0.5", 0.5, 0.0),
]


@dataclass
class JointRow:
    label: str
    born: float
    d_tv: float
    mi: float
    decoh: float


def grow(drift: float, restore: float, seed: int):
    rng = random.Random(seed)
    hw = int(PW / H)
    nl = NL
    md = max(1, round(MAX_D_PHYS / H))
    pos: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = {}
    nmap: dict[tuple[int, int, int], int] = {}
    layers: list[list[int]] = []

    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    layers.append([0])

    for layer in range(1, nl):
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
                    y = py + rng.gauss(0, drift * H)
                    z = pz + rng.gauss(0, drift * H)
                    y = y * (1 - restore) + (iy * H) * restore
                    z = z * (1 - restore) + (iz * H) * restore
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
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            edges.append(di)
                adj[si] = adj.get(si, []) + edges

    return pos, adj, layers


def propagate(pos, adj, blocked):
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
            act = L
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * K * act) * w * hm / (L * L)
    return amps


def setup_slits(pos, layers):
    bl = NL // 3
    barrier = layers[bl]
    sa = [i for i in barrier if pos[i][1] >= 0.5]
    sb = [i for i in barrier if pos[i][1] <= -0.5]
    blocked = set(barrier) - set(sa + sb)
    return barrier, sa, sb, blocked, bl


def born_measure(pos, adj, barrier, det):
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
        amps = propagate(pos, adj, blocked)
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


def measure_row(label: str, drift: float, restore: float) -> JointRow:
    born_vals = []
    dtv_vals = []
    mi_vals = []
    decoh_vals = []

    for seed in SEEDS:
        pos, adj, layers = grow(drift, restore, seed)
        det = layers[-1]
        barrier, sa, sb, blocked, bl = setup_slits(pos, layers)

        born_vals.append(born_measure(pos, adj, barrier, det))

        pa = propagate(pos, adj, blocked | set(sb))
        pb = propagate(pos, adj, blocked | set(sa))

        da = [abs(pa[d]) ** 2 for d in det]
        db = [abs(pb[d]) ** 2 for d in det]
        na = sum(da)
        nb = sum(db)
        if na > 1e-30 and nb > 1e-30:
            dtv = 0.5 * sum(abs(a / na - b / nb) for a, b in zip(da, db))
            dtv_vals.append(dtv)

        bw = 2 * (PW + 1) / N_YBINS
        ed = max(1, round(NL / 6))
        st = bl + 1
        sp = min(NL - 1, st + ed)
        mid = []
        for layer in range(st, sp):
            mid.extend(layers[layer])
        ba = [0j] * N_YBINS
        bb = [0j] * N_YBINS
        for m in mid:
            b2 = max(0, min(N_YBINS - 1, int((pos[m][1] + PW + 1) / bw)))
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
        decoh_vals.append(100 * (1 - pur))

        prob_a = [0.0] * N_YBINS
        prob_b = [0.0] * N_YBINS
        for d in det:
            b2 = max(0, min(N_YBINS - 1, int((pos[d][1] + PW + 1) / bw)))
            prob_a[b2] += abs(pa[d]) ** 2
            prob_b[b2] += abs(pb[d]) ** 2
        na_prob = sum(prob_a)
        nb_prob = sum(prob_b)
        mi = 0.0
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
        mi_vals.append(mi)

    return JointRow(
        label=label,
        born=sum(born_vals) / len(born_vals),
        d_tv=sum(dtv_vals) / len(dtv_vals),
        mi=sum(mi_vals) / len(mi_vals),
        decoh=sum(decoh_vals) / len(decoh_vals),
    )


def main():
    t0 = time.time()
    print("=" * 76)
    print("GATE B NO-RESTORE JOINT PACKAGE HARNESS")
    print("  Born / d_TV / MI / decoherence with restore fixed to 0")
    print("=" * 76)
    print(f"h={H}, W={PW}, L={int((NL - 1) * H)}, seeds={len(SEEDS)}, LAM={LAM}")
    print("growth rule: template + drift + no restore + NN connectivity from grid labels")
    print()
    print(f"{'geometry':<20} {'Born':>10} {'d_TV':>8} {'MI':>8} {'Decoh':>8}")

    for label, drift, restore in ROWS:
        row = measure_row(label, drift, restore)
        print(
            f"{row.label:<20} {row.born:>10.2e} {row.d_tv:>8.3f} "
            f"{row.mi:>8.3f} {row.decoh:>7.1f}%"
        )

    print()
    print("SAFE INTERPRETATION")
    print("  This harness isolates the no-restore lane only.")
    print("  The exact grid is the reference row; the no-restore rows show how")
    print("  much of the joint package survives without the restoring pull.")
    print("  Treat this as bounded evidence, not a full generated-geometry closure.")
    print(f"\nTotal time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
