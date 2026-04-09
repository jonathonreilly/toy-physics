#!/usr/bin/env python3
"""Continuum limit via FAN-OUT NORMALIZED kernel (Approach 3 from the plan).

The default lattice_continuum_limit.py applies a `spacing²` kernel factor
to keep amplitude norm O(1) per layer. That's a lattice-spacing hack.
This script replaces it with a fan-out normalization:

    ea = exp(i·k·act) · w / (L · sqrt(fan_out[i]))

where fan_out[i] is the number of outgoing edges from node i. This is
still strictly linear (pure topology, no amplitude-dependent feedback)
but preserves total outgoing amplitude norm per node regardless of
fan-out: if each edge carries amp/sqrt(fan_out), the sum of |edge|²
over the fan-out equals |amp|² (ignoring the 1/L and w factors).

The key questions:
  1. Is the kernel Born-clean (|I₃|/P < 1e-10)? This MUST be verified
     because fan-out normalization changes the kernel.
  2. Does the physics (gravity, MI, decoherence) converge as h → 0?
  3. Does the scheme survive h=0.25 and ideally h=0.125?

If all three pass, this is the continuum-limit unlock the plan targets.
If Born fails, the scheme is physics-invalid and we learn the
normalization can't be arbitrary.

Cost: same as lattice_continuum_limit at each h. Tests h ∈ {2, 1, 0.5, 0.25}.
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
PHYS_WIDTH = 20.0
PHYS_LENGTH = 40.0
MAX_DY_PHYS = 5.0
SLIT_Y = 3.0
MASS_Y = 8.0


def generate_lattice(spacing, phys_width, phys_length, max_dy_phys):
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


def propagate_fanout(pos, adj, field, k, blocked, n):
    """Fan-out normalized propagator: each edge scales by 1/sqrt(fan_out[i])."""
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    src = next(i for i, (x, y) in enumerate(pos) if abs(x) < 1e-10 and abs(y) < 1e-10)
    amps[src] = 1.0
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        out = adj.get(i, [])
        # Fan-out COUNTING unblocked targets so the normalization
        # reflects the actual available branches
        valid_targets = [j for j in out if j not in blocked]
        fo = len(valid_targets)
        if fo == 0:
            continue
        fo_sqrt = math.sqrt(fo)
        for j in valid_targets:
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
            # Fan-out normalization: the only spacing scaling is the
            # geometric 1/L (which captures the kernel's natural weight)
            ea = cmath.exp(1j * k * act) * w / (L * fo_sqrt)
            amps[j] += amps[i] * ea
    return amps


def make_field(pos, nmap, gl, mass_y_phys, spacing, hw_nodes, strength):
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


def born_audit(pa, pb, det):
    """Born audit: interference term |I3| vs total probability P.

    Two path-sets a and b that are complementary (a+b). For a linear
    (Born-clean) propagator, |pa+pb|² = |pa|² + |pb|² + 2·Re(pa*·pb)
    and P_total when BOTH slits are open equals sum |pa+pb|² over det.
    |I3|/P measures how far from Born the kernel is.
    """
    num = 0.0
    den = 0.0
    for d in det:
        psum = pa[d] + pb[d]
        p_interf = abs(psum) ** 2
        p_noint = abs(pa[d]) ** 2 + abs(pb[d]) ** 2
        cross = p_interf - p_noint
        num += abs(cross)
        den += p_interf
    if den < 1e-30:
        return float('nan')
    # Cross terms ARE Born-allowed (they ARE the interference).
    # The I3 audit is three-way: (p_a+p_b+p_c) vs sum of two-ways.
    # For our 2-slit setup, the honest Born check is the sum rule:
    # P_open = P_a + P_b + 2·Re(pa·pb*)   (this is automatically true)
    # A sharper check: does |pa|²+|pb|² equal P_no_interference?
    # Here we report ratio of interference to total as a sanity value;
    # true I3 Born violation needs a 3-slit geometry, not reported here.
    return num / den


def measure_all(spacing):
    pos, adj, nl, hw, max_dy, bl, gl, nmap = generate_lattice(
        spacing, PHYS_WIDTH, PHYS_LENGTH, MAX_DY_PHYS)
    n = len(pos)
    det_layer = nl - 1
    det = [nmap[(det_layer, iy)] for iy in range(-hw, hw + 1) if (det_layer, iy) in nmap]

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
    phys_strength = 0.0005 * spacing

    # Gravity
    field_m, _ = make_field(pos, nmap, gl, MASS_Y, spacing, hw, phys_strength)
    af = propagate_fanout(pos, adj, field_f, K, blocked, n)
    am = propagate_fanout(pos, adj, field_m, K, blocked, n)
    pf = sum(abs(af[d]) ** 2 for d in det)
    pm = sum(abs(am[d]) ** 2 for d in det)
    if pf < 1e-30 or pm < 1e-30:
        return None
    yf = sum(abs(af[d]) ** 2 * pos[d][1] for d in det) / pf
    ym = sum(abs(am[d]) ** 2 * pos[d][1] for d in det) / pm
    gravity = ym - yf

    # k=0 control
    am0 = propagate_fanout(pos, adj, field_m, 0.0, blocked, n)
    af0 = propagate_fanout(pos, adj, field_f, 0.0, blocked, n)
    pm0 = sum(abs(am0[d]) ** 2 for d in det)
    pf0 = sum(abs(af0[d]) ** 2 for d in det)
    gk0 = 0.0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d]) ** 2 * pos[d][1] for d in det) / pm0
               - sum(abs(af0[d]) ** 2 * pos[d][1] for d in det) / pf0)

    # Single-slit runs for Born audit and MI
    pa = propagate_fanout(pos, adj, field_f, K, blocked | set(sb), n)
    pb = propagate_fanout(pos, adj, field_f, K, blocked | set(sa), n)

    # Born audit
    born_ratio = born_audit(pa, pb, det)

    # MI
    bw = 2 * (PHYS_WIDTH + spacing) / N_YBINS
    prob_a = [0.0] * N_YBINS
    prob_b = [0.0] * N_YBINS
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d][1] + PHYS_WIDTH + spacing) / bw)))
        prob_a[b2] += abs(pa[d]) ** 2
        prob_b[b2] += abs(pb[d]) ** 2
    na = sum(prob_a)
    nb = sum(prob_b)
    MI = 0.0
    if na > 1e-30 and nb > 1e-30:
        prob_a = [p / na for p in prob_a]
        prob_b = [p / nb for p in prob_b]
        H = 0.0
        Hc = 0.0
        for b3 in range(N_YBINS):
            pm2 = 0.5 * prob_a[b3] + 0.5 * prob_b[b3]
            if pm2 > 1e-30:
                H -= pm2 * math.log2(pm2)
            if prob_a[b3] > 1e-30:
                Hc -= 0.5 * prob_a[b3] * math.log2(prob_a[b3])
            if prob_b[b3] > 1e-30:
                Hc -= 0.5 * prob_b[b3] * math.log2(prob_b[b3])
        MI = H - Hc

    # d_TV
    da = {d: abs(pa[d]) ** 2 for d in det}
    db = {d: abs(pb[d]) ** 2 for d in det}
    na2 = sum(da.values())
    nb2 = sum(db.values())
    dtv = 0.0
    if na2 > 1e-30 and nb2 > 1e-30:
        dtv = 0.5 * sum(abs(da[d] / na2 - db[d] / nb2) for d in det)

    # Amplitude magnitudes (overflow watch)
    max_amp = max(abs(a) for a in af)
    total_prob = pf

    return {
        "spacing": spacing,
        "n_nodes": n,
        "n_layers": nl,
        "nodes_per_layer": 2 * hw + 1,
        "gravity": gravity,
        "gk0": gk0,
        "MI": MI,
        "dtv": dtv,
        "born": born_ratio,
        "max_amp": max_amp,
        "P_total": total_prob,
    }


def main():
    print("=" * 100)
    print("FAN-OUT NORMALIZED CONTINUUM LIMIT (Approach 3)")
    print(f"  Physical extent: W={PHYS_WIDTH}, L={PHYS_LENGTH}, mass at y={MASS_Y}")
    print(f"  Kernel: exp(i·k·act) · w / (L · sqrt(fan_out))")
    print("=" * 100)
    print()

    spacings = [2.0, 1.0, 0.5, 0.25]

    print(f"  {'h':>6s}  {'n_nodes':>8s}  {'npl':>5s}  {'gravity':>11s}  {'k=0':>10s}  "
          f"{'MI':>7s}  {'d_TV':>7s}  {'born':>10s}  {'max|A|':>10s}  {'P_tot':>10s}  {'t':>5s}")
    print(f"  {'-' * 110}")

    results = []
    for sp in spacings:
        t0 = time.time()
        try:
            r = measure_all(sp)
        except (OverflowError, MemoryError) as e:
            print(f"  {sp:6.3f}  FAIL ({type(e).__name__})  {time.time()-t0:4.0f}s")
            continue
        dt = time.time() - t0
        if r:
            results.append(r)
            print(f"  {sp:6.3f}  {r['n_nodes']:8d}  {r['nodes_per_layer']:5d}  "
                  f"{r['gravity']:+11.6f}  {r['gk0']:+10.2e}  "
                  f"{r['MI']:7.4f}  {r['dtv']:7.4f}  {r['born']:10.2e}  "
                  f"{r['max_amp']:10.2e}  {r['P_total']:10.2e}  {dt:4.0f}s", flush=True)
        else:
            print(f"  {sp:6.3f}  FAIL  {dt:4.0f}s")

    print()
    print("=" * 100)
    print("VERDICT")
    print("=" * 100)
    if len(results) < 2:
        print("  Insufficient data to judge convergence.")
        return

    # Check overflow
    max_amps = [r['max_amp'] for r in results]
    if max(max_amps) / min(max_amps) > 1e6:
        print(f"  OVERFLOW — amplitude range {min(max_amps):.1e} to {max(max_amps):.1e}")
    else:
        print(f"  Amplitude stable: max|A| range {min(max_amps):.2e} to {max(max_amps):.2e}")

    # Gravity convergence
    gravs = [r['gravity'] for r in results]
    print(f"  Gravity values: {['%+.4f' % g for g in gravs]}")
    if all(g > 0 for g in gravs[-2:]):
        print("    sign stable (attractive in last two refinements)")
    elif all(g < 0 for g in gravs[-2:]):
        print("    sign stable (repulsive in last two refinements)")
    else:
        print("    sign NOT stable across refinements")

    # Born check (this is a 2-slit cross-term report, not 3-slit I3)
    borns = [r['born'] for r in results]
    print(f"  Born interference ratio: {['%.2e' % b for b in borns]}")
    print(f"    (this is a 2-slit cross-term magnitude, not 3-slit I3;")
    print(f"     a true 3-slit Born audit needs a 3-path geometry)")

    # MI / dTV convergence
    mis = [r['MI'] for r in results]
    dtvs = [r['dtv'] for r in results]
    print(f"  MI values:  {['%.4f' % m for m in mis]}")
    print(f"  d_TV values:{['%.4f' % d for d in dtvs]}")

    # Ratio test for convergence
    if len(results) >= 3:
        g_deltas = [abs(gravs[i+1] - gravs[i]) for i in range(len(gravs)-1)]
        print(f"  Gravity step deltas: {['%.4f' % d for d in g_deltas]}")
        if g_deltas[-1] < g_deltas[0] * 0.5:
            print("    → gravity appears to be CONVERGING")
        elif g_deltas[-1] > g_deltas[0] * 2:
            print("    → gravity appears to be DIVERGING")
        else:
            print("    → gravity deltas roughly constant (slow/no convergence)")


if __name__ == "__main__":
    main()
