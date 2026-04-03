#!/usr/bin/env python3
"""Continuum limit test: does the lattice physics survive refinement?

Generate lattices at decreasing spacing (same physical extent W=20):
  spacing=1.0: 41 nodes/layer (current)
  spacing=0.5: 81 nodes/layer
  spacing=0.25: 161 nodes/layer

At each resolution, measure all 10 properties. If the results
converge to stable values as spacing → 0, the model has a
genuine continuum limit.

Key predictions:
  - Born should stay at machine precision (mathematical property)
  - k=0 should stay zero (mathematical)
  - Gravity, MI, decoherence: should converge to finite values
  - Distance law exponent: should stabilize
  - F∝M exponent: should stabilize
  - Purity exponent: should stabilize

If any property DIVERGES or VANISHES as spacing → 0, it's a
lattice artifact, not physics.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
K = 5.0
LAM = 10.0
N_YBINS = 8
PHYS_WIDTH = 20.0  # Fixed physical extent
PHYS_LENGTH = 40.0  # Fixed physical length (number of layers × spacing)
MAX_DY_PHYS = 5.0  # Physical transverse reach (max_dy × spacing)
SLIT_Y = 3.0  # Slit position in physical units
MASS_Y = 8.0  # Mass position in physical units


def generate_lattice(spacing, phys_width, phys_length, max_dy_phys):
    """Generate lattice at given spacing with fixed physical dimensions."""
    n_layers = int(phys_length / spacing) + 1
    half_width_nodes = int(phys_width / spacing)
    max_dy_nodes = max(1, int(max_dy_phys / spacing))

    pos = []
    adj = defaultdict(list)
    nmap = {}

    for layer in range(n_layers):
        x = layer * spacing
        for iy in range(-half_width_nodes, half_width_nodes + 1):
            y = iy * spacing
            idx = len(pos)
            pos.append((x, y))
            nmap[(layer, iy)] = idx

    for layer in range(n_layers - 1):
        for iy in range(-half_width_nodes, half_width_nodes + 1):
            si = nmap.get((layer, iy))
            if si is None:
                continue
            for dy in range(-max_dy_nodes, max_dy_nodes + 1):
                iyn = iy + dy
                if abs(iyn) > half_width_nodes:
                    continue
                di = nmap.get((layer + 1, iyn))
                if di is not None:
                    adj[si].append(di)

    bl = n_layers // 3
    gl = 2 * n_layers // 3

    return pos, dict(adj), n_layers, half_width_nodes, max_dy_nodes, bl, gl, nmap


def propagate(pos, adj, field, k, blocked, n):
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    # Source at (0, 0)
    src = next(i for i, (x, y) in enumerate(pos) if abs(x) < 1e-10 and abs(y) < 1e-10)
    amps[src] = 1.0
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
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def make_field(pos, nmap, gl, mass_y_phys, spacing, hw_nodes, strength):
    """Field from mass at physical position mass_y_phys."""
    mass_iy = round(mass_y_phys / spacing)
    mass_iy = max(-hw_nodes, min(hw_nodes, mass_iy))
    mass_idx = nmap.get((gl, mass_iy))
    if mass_idx is None:
        return [0.0] * len(pos), None
    n = len(pos)
    field = [0.0] * n
    mx, my = pos[mass_idx]
    for i in range(n):
        ix, iy = pos[i]
        r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
        field[i] = strength / r
    return field, mass_idx


def measure_all(spacing):
    """Full measurement at given spacing."""
    pos, adj, nl, hw, max_dy, bl, gl, nmap = generate_lattice(
        spacing, PHYS_WIDTH, PHYS_LENGTH, MAX_DY_PHYS)
    n = len(pos)
    det_layer = nl - 1
    det = [nmap[(det_layer, iy)] for iy in range(-hw, hw + 1) if (det_layer, iy) in nmap]

    # Slits at physical y = ±SLIT_Y
    slit_iy = max(1, round(SLIT_Y / spacing))
    bi = [nmap[(bl, iy)] for iy in range(-hw, hw + 1) if (bl, iy) in nmap]
    sa = [nmap[(bl, iy)] for iy in range(slit_iy, min(slit_iy + max(2, round(2/spacing)), hw + 1))
          if (bl, iy) in nmap]
    sb = [nmap[(bl, iy)] for iy in range(-min(slit_iy + max(1, round(1/spacing)), hw), -slit_iy + 1)
          if (bl, iy) in nmap]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    field_f = [0.0] * n
    # Scale field strength with spacing to keep physical effect constant
    # Phase shift ~ strength × n_layers. As spacing → 0, n_layers ∝ 1/spacing.
    # To keep total phase shift constant: strength ∝ spacing
    phys_strength = 0.0005 * spacing  # Scale with spacing

    # 1. Gravity at b = MASS_Y
    field_m, _ = make_field(pos, nmap, gl, MASS_Y, spacing, hw, phys_strength)
    af = propagate(pos, adj, field_f, K, blocked, n)
    am = propagate(pos, adj, field_m, K, blocked, n)
    pf = sum(abs(af[d]) ** 2 for d in det)
    pm = sum(abs(am[d]) ** 2 for d in det)
    if pf < 1e-30 or pm < 1e-30:
        return None
    yf = sum(abs(af[d]) ** 2 * pos[d][1] for d in det) / pf
    ym = sum(abs(am[d]) ** 2 * pos[d][1] for d in det) / pm
    gravity = ym - yf

    # 2. k=0 control
    am0 = propagate(pos, adj, field_m, 0.0, blocked, n)
    af0 = propagate(pos, adj, field_f, 0.0, blocked, n)
    pm0 = sum(abs(am0[d]) ** 2 for d in det)
    pf0 = sum(abs(af0[d]) ** 2 for d in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d]) ** 2 * pos[d][1] for d in det) / pm0
               - sum(abs(af0[d]) ** 2 * pos[d][1] for d in det) / pf0)

    # 3. MI + decoherence
    pa = propagate(pos, adj, field_f, K, blocked | set(sb), n)
    pb = propagate(pos, adj, field_f, K, blocked | set(sa), n)
    bw = 2 * (PHYS_WIDTH + spacing) / N_YBINS
    prob_a = [0] * N_YBINS
    prob_b = [0] * N_YBINS
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d][1] + PHYS_WIDTH + spacing) / bw)))
        prob_a[b2] += abs(pa[d]) ** 2
        prob_b[b2] += abs(pb[d]) ** 2
    na = sum(prob_a)
    nb = sum(prob_b)
    MI = 0
    if na > 1e-30 and nb > 1e-30:
        prob_a = [p / na for p in prob_a]
        prob_b = [p / nb for p in prob_b]
        H = 0
        Hc = 0
        for b3 in range(N_YBINS):
            pm2 = 0.5 * prob_a[b3] + 0.5 * prob_b[b3]
            if pm2 > 1e-30:
                H -= pm2 * math.log2(pm2)
            if prob_a[b3] > 1e-30:
                Hc -= 0.5 * prob_a[b3] * math.log2(prob_a[b3])
            if prob_b[b3] > 1e-30:
                Hc -= 0.5 * prob_b[b3] * math.log2(prob_b[b3])
        MI = H - Hc

    # CL purity
    env_depth = max(1, round(nl / 6))
    st = bl + 1
    sp = min(nl - 1, st + env_depth)
    mid = []
    for l in range(st, sp):
        mid.extend([nmap[(l, iy)] for iy in range(-hw, hw + 1) if (l, iy) in nmap])
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid:
        b2 = max(0, min(N_YBINS - 1, int((pos[m][1] + PHYS_WIDTH + spacing) / bw)))
        ba[b2] += pa[m]
        bb[b2] += pb[m]
    S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    NA = sum(abs(a) ** 2 for a in ba)
    NB = sum(abs(b) ** 2 for b in bb)
    Sn = S / (NA + NB) if (NA + NB) > 0 else 0
    Dcl = math.exp(-LAM ** 2 * Sn)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1, d2)] = (pa[d1].conjugate() * pa[d2] + pb[d1].conjugate() * pb[d2]
                             + Dcl * pa[d1].conjugate() * pb[d2]
                             + Dcl * pb[d1].conjugate() * pa[d2])
    tr = sum(rho[(d, d)] for d in det).real
    pur_cl = 1.0
    if tr > 1e-30:
        for key in rho:
            rho[key] /= tr
        pur_cl = sum(abs(v) ** 2 for v in rho.values()).real

    # 4. d_TV
    da = {d: abs(pa[d]) ** 2 for d in det}
    db = {d: abs(pb[d]) ** 2 for d in det}
    na2 = sum(da.values())
    nb2 = sum(db.values())
    dtv = 0
    if na2 > 1e-30 and nb2 > 1e-30:
        dtv = 0.5 * sum(abs(da[d] / na2 - db[d] / nb2) for d in det)

    return {
        "spacing": spacing,
        "n_nodes": n,
        "n_layers": nl,
        "nodes_per_layer": 2 * hw + 1,
        "gravity": gravity,
        "gk0": gk0,
        "MI": MI,
        "pur_cl": pur_cl,
        "dtv": dtv,
    }


def main():
    print("=" * 90)
    print("CONTINUUM LIMIT TEST")
    print(f"  Physical extent: W={PHYS_WIDTH}, L={PHYS_LENGTH}")
    print(f"  Mass at y={MASS_Y}, slits at y=±{SLIT_Y}")
    print("=" * 90)
    print()

    spacings = [2.0, 1.0, 0.5]

    print(f"  {'spacing':>7s}  {'nodes':>7s}  {'npl':>5s}  {'gravity':>10s}  {'k=0':>10s}  "
          f"{'MI':>8s}  {'1-pur':>8s}  {'d_TV':>8s}  {'time':>5s}")
    print(f"  {'-' * 80}")

    for sp in spacings:
        t0 = time.time()
        r = measure_all(sp)
        dt = time.time() - t0
        if r:
            print(f"  {sp:7.2f}  {r['n_nodes']:7d}  {r['nodes_per_layer']:5d}  "
                  f"{r['gravity']:+10.6f}  {r['gk0']:+10.2e}  "
                  f"{r['MI']:8.4f}  {1-r['pur_cl']:8.4f}  {r['dtv']:8.4f}  {dt:4.0f}s")
        else:
            print(f"  {sp:7.2f}  FAIL  {dt:4.0f}s")

    print()
    print("CONVERGENCE CHECK:")
    print("  If values stabilize as spacing → 0: continuum limit EXISTS")
    print("  If values diverge or vanish: lattice artifact")
    print("  Key: gravity, MI, decoherence should converge to finite nonzero values")


if __name__ == "__main__":
    main()
