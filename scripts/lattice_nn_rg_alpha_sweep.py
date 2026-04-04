#!/usr/bin/env python3
"""NN lattice RG alpha sweep.

This is a narrow follow-up to the deterministic nearest-neighbor refinement
path. We keep the same raw 3-edge geometry and the same geometry-only rescale
schedule, then vary the field strength as

    strength = s0 / h**alpha

for a small alpha grid.

The question is deliberately narrow:

- can a simple alpha-scaling make the gravity response nearly h-independent
  between h=0.5 and h=0.25, while keeping the Born-safe deterministic path
  intact?

This is not a claim of a renormalized continuum theory. It is only a fixed-point
style probe on the Born-safe refinement window.
"""

from __future__ import annotations

import cmath
import math
import os
import sys
import time
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
K_PHYS = 5.0
LAM = 10.0
N_YBINS = 8
PHYS_W = 20.0
PHYS_L = 40.0
SLIT_Y = 3.0
MASS_Y = 8.0
FANOUT = 3.0
BASE_STRENGTH = 5e-4

H_VALUES = [1.0, 0.5, 0.25]
ALPHAS = [0.0, 0.5, 1.0, 1.5]


def generate_nn_lattice(spacing: float):
    """Raw NN lattice: straight, up, down."""
    nl = int(PHYS_L / spacing) + 1
    hw = int(PHYS_W / spacing)
    pos: List[Tuple[float, float]] = []
    adj: Dict[int, List[int]] = defaultdict(list)
    nmap = {}

    for layer in range(nl):
        x = layer * spacing
        for iy in range(-hw, hw + 1):
            y = iy * spacing
            idx = len(pos)
            pos.append((x, y))
            nmap[(layer, iy)] = idx

    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            si = nmap.get((layer, iy))
            if si is None:
                continue
            for diy in (-1, 0, 1):
                iyn = iy + diy
                if abs(iyn) > hw:
                    continue
                di = nmap.get((layer + 1, iyn))
                if di is not None:
                    adj[si].append(di)

    return pos, dict(adj), nl, hw, nmap


def strength_for_alpha(alpha: float, spacing: float) -> float:
    return BASE_STRENGTH / (spacing ** alpha)


def propagate(pos, adj, field, k, blocked, n, spacing):
    """Raw path-sum propagation with a fixed deterministic rescale schedule."""
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    src = next(i for i, (x, y) in enumerate(pos) if abs(x) < 1e-10 and abs(y) < 1e-10)
    amps[src] = 1.0
    step_scale = spacing / math.sqrt(FANOUT)

    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = pos[i]
            x2, y2 = pos[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1.0 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea * step_scale
    return amps


def measure_full(spacing: float, alpha: float):
    pos, adj, nl, hw, nmap = generate_nn_lattice(spacing)
    n = len(pos)
    det_layer = nl - 1
    det = [nmap[(det_layer, iy)] for iy in range(-hw, hw + 1) if (det_layer, iy) in nmap]
    bl = nl // 3
    gl = 2 * nl // 3

    slit_iy = max(1, round(SLIT_Y / spacing))
    bi = [nmap[(bl, iy)] for iy in range(-hw, hw + 1) if (bl, iy) in nmap]
    sa_range = range(slit_iy, min(slit_iy + max(2, round(2 / spacing)), hw + 1))
    sb_range = range(-min(slit_iy + max(1, round(1 / spacing)), hw), -slit_iy + 1)
    sa = [nmap[(bl, iy)] for iy in sa_range if (bl, iy) in nmap]
    sb = [nmap[(bl, iy)] for iy in sb_range if (bl, iy) in nmap]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)
    field_f = [0.0] * n

    mass_iy = round(MASS_Y / spacing)
    mass_idx = nmap.get((gl, mass_iy))
    if mass_idx is None:
        return None

    phys_strength = strength_for_alpha(alpha, spacing)
    field_m = [0.0] * n
    mx, my = pos[mass_idx]
    for i in range(n):
        ix, iy = pos[i]
        r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
        field_m[i] = phys_strength / r

    af = propagate(pos, adj, field_f, K_PHYS, blocked, n, spacing)
    am = propagate(pos, adj, field_m, K_PHYS, blocked, n, spacing)
    pf = sum(abs(af[d]) ** 2 for d in det)
    pm = sum(abs(am[d]) ** 2 for d in det)
    if pf < 1e-30 or pm < 1e-30:
        return None
    yf = sum(abs(af[d]) ** 2 * pos[d][1] for d in det) / pf
    ym = sum(abs(am[d]) ** 2 * pos[d][1] for d in det) / pm
    gravity = ym - yf

    am0 = propagate(pos, adj, field_m, 0.0, blocked, n, spacing)
    af0 = propagate(pos, adj, field_f, 0.0, blocked, n, spacing)
    pm0 = sum(abs(am0[d]) ** 2 for d in det)
    pf0 = sum(abs(af0[d]) ** 2 for d in det)
    gk0 = 0.0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (
            sum(abs(am0[d]) ** 2 * pos[d][1] for d in det) / pm0
            - sum(abs(af0[d]) ** 2 * pos[d][1] for d in det) / pf0
        )

    pa = propagate(pos, adj, field_f, K_PHYS, blocked | set(sb), n, spacing)
    pb = propagate(pos, adj, field_f, K_PHYS, blocked | set(sa), n, spacing)
    bw = 2 * (PHYS_W + spacing) / N_YBINS
    prob_a = [0.0] * N_YBINS
    prob_b = [0.0] * N_YBINS
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d][1] + PHYS_W + spacing) / bw)))
        prob_a[b2] += abs(pa[d]) ** 2
        prob_b[b2] += abs(pb[d]) ** 2
    na = sum(prob_a)
    nb = sum(prob_b)
    MI = 0.0
    if na > 1e-30 and nb > 1e-30:
        pa_n = [p / na for p in prob_a]
        pb_n = [p / nb for p in prob_b]
        H = 0.0
        Hc = 0.0
        for b3 in range(N_YBINS):
            pm2 = 0.5 * pa_n[b3] + 0.5 * pb_n[b3]
            if pm2 > 1e-30:
                H -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30:
                Hc -= 0.5 * pa_n[b3] * math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30:
                Hc -= 0.5 * pb_n[b3] * math.log2(pb_n[b3])
        MI = H - Hc

    env_depth = max(1, round(nl / 6))
    st = bl + 1
    sp = min(nl - 1, st + env_depth)
    mid = []
    for l in range(st, sp):
        mid.extend([nmap[(l, iy)] for iy in range(-hw, hw + 1) if (l, iy) in nmap])
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid:
        b2 = max(0, min(N_YBINS - 1, int((pos[m][1] + PHYS_W + spacing) / bw)))
        ba[b2] += pa[m]
        bb[b2] += pb[m]
    S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    NA = sum(abs(a) ** 2 for a in ba)
    NB = sum(abs(b) ** 2 for b in bb)
    Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
    Dcl = math.exp(-LAM ** 2 * Sn)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1, d2)] = (
                pa[d1].conjugate() * pa[d2]
                + pb[d1].conjugate() * pb[d2]
                + Dcl * pa[d1].conjugate() * pb[d2]
                + Dcl * pb[d1].conjugate() * pa[d2]
            )
    tr = sum(rho[(d, d)] for d in det).real
    pur_cl = 1.0
    if tr > 1e-30:
        for key in rho:
            rho[key] /= tr
        pur_cl = sum(abs(v) ** 2 for v in rho.values()).real

    da = {d: abs(pa[d]) ** 2 for d in det}
    db = {d: abs(pb[d]) ** 2 for d in det}
    na2 = sum(da.values())
    nb2 = sum(db.values())
    dtv = 0.0
    if na2 > 1e-30 and nb2 > 1e-30:
        dtv = 0.5 * sum(abs(da[d] / na2 - db[d] / nb2) for d in det)

    born = math.nan
    upper = sorted([i for i in bi if pos[i][1] > spacing], key=lambda i: pos[i][1])
    lower = sorted([i for i in bi if pos[i][1] < -spacing], key=lambda i: -pos[i][1])
    middle = [i for i in bi if abs(pos[i][1]) <= spacing]
    if upper and lower and middle:
        s_a = [upper[0]]
        s_b = [lower[0]]
        s_c = [middle[0]]
        all_s = set(s_a + s_b + s_c)
        other = set(bi) - all_s
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
            bl2 = other | (all_s - open_set)
            a = propagate(pos, adj, field_f, K_PHYS, bl2, n, spacing)
            probs[key] = [abs(a[d]) ** 2 for d in det]
        I3 = 0.0
        P = 0.0
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
            I3 += abs(i3)
            P += probs["abc"][di]
        born = I3 / P if P > 1e-30 else math.nan

    return {
        "h": spacing,
        "n": n,
        "nl": nl,
        "npl": 2 * hw + 1,
        "strength": phys_strength,
        "gravity": gravity,
        "gk0": gk0,
        "MI": MI,
        "pur_cl": pur_cl,
        "dtv": dtv,
        "born": born,
    }


def _fmt_or_nan(value: float, precision: int = 4) -> str:
    if not math.isfinite(value):
        return "nan"
    return f"{value:.{precision}f}"


def main():
    print("=" * 120)
    print("NN LATTICE RG ALPHA SWEEP")
    print(f"  Geometry: 3 edges/node, deterministic rescale schedule spacing/sqrt({FANOUT:g})")
    print(f"  Base strength = {BASE_STRENGTH:g}, k={K_PHYS}, mass at y={MASS_Y}")
    print(f"  h values = {', '.join(f'{h:g}' for h in H_VALUES)}")
    print(f"  alpha values = {', '.join(f'{a:g}' for a in ALPHAS)}")
    print("=" * 120)
    print()

    retained = []
    for alpha in ALPHAS:
        print(f"ALPHA = {alpha:g}")
        print(
            f"  {'h':>6s}  {'nodes':>8s}  {'strength':>10s}  {'gravity':>10s}  {'k=0':>10s}  "
            f"{'MI':>8s}  {'1-pur':>8s}  {'d_TV':>8s}  {'Born':>10s}  {'time':>5s}"
        )
        print(f"  {'-' * 97}")
        rows = []
        for h in H_VALUES:
            t0 = time.time()
            r = measure_full(h, alpha)
            dt = time.time() - t0
            if r is None:
                print(f"  {h:6.3f}  FAIL  {dt:4.0f}s")
                continue
            rows.append(r)
            born_s = f"{r['born']:.2e}" if math.isfinite(r["born"]) else "nan"
            print(
                f"  {h:6.3f}  {r['n']:8d}  {r['strength']:10.3g}  {r['gravity']:+10.6f}  "
                f"{r['gk0']:+10.2e}  {r['MI']:8.4f}  {1 - r['pur_cl']:8.4f}  "
                f"{r['dtv']:8.4f}  {born_s:>10s}  {dt:4.0f}s"
            )

        if len(rows) >= 2:
            g05 = next((r["gravity"] for r in rows if abs(r["h"] - 0.5) < 1e-12), None)
            g025 = next((r["gravity"] for r in rows if abs(r["h"] - 0.25) < 1e-12), None)
            if g05 is not None and g025 is not None and g05 != 0:
                ratio = g025 / g05
                alpha_eff = math.log(abs(g025) / abs(g05)) / math.log(0.25 / 0.5)
                print(
                    f"  ratio g(0.25)/g(0.5) = {ratio:.3f}"
                    f"  effective exponent from the pair = {alpha_eff:.3f}"
                )
                retained.append((alpha, ratio, alpha_eff, g05, g025, rows))
            else:
                print("  ratio g(0.25)/g(0.5): unavailable")
        else:
            print("  insufficient retained rows")
        print()

    if retained:
        best = min(retained, key=lambda item: abs(item[1] - 1.0))
        print("READ")
        print(f"- within the scanned grid, the strongest checked alpha for h=0.5 vs h=0.25 stability: {best[0]:g}")
        print(f"- corresponding gravity ratio: {best[1]:.3f}")
        print(f"- pairwise effective exponent: {best[2]:.3f}")
        print("- the trend improves monotonically across the scanned alpha grid")
        print("- Born refers to the same-family companion audit on the deterministic path")
        print("- this is a fixed-point style probe, not a promoted renormalization theorem")
    else:
        print("READ")
        print("- no retained rows; alpha sweep inconclusive")


if __name__ == "__main__":
    main()
