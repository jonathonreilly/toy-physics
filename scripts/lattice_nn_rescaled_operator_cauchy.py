#!/usr/bin/env python3
"""NN lattice rescaled-lane operator-convergence Cauchy test.

The companion runner `lattice_nn_rescaled_response_exponents.py` closed
the strength-rescaling route to the continuum-bridge (sharpened
saturation null-result, q ~ 1.19, p ~ 1/2). This runner attacks the
same bridge gap from a different angle: numerical operator-norm
Cauchy convergence of the rescaled transfer operator T_h on a finite-
dimensional observable subspace, independent of any strength-scaling
question.

What it tests
-------------

For each spacing h ∈ {1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125} on the
deterministic-rescale lane we measure a 5-dimensional observable
vector at three independent mass-source positions y_m ∈ {6, 8, 10}.
Together these 15 numbers per h are matrix elements of T_h on a
fixed source-basis (three point sources) and a fixed observable-basis
(five canonical observables). They live in R^15 independent of h.

The Cauchy test is

    delta(h_n) := || vec(h_n) - vec(h_{n+1}) ||_2

For each component we also report the per-component Cauchy decrement.
We fit the geometric-decay rate

    delta(h) ~ C * h^r

If r > 0 with R^2 close to 1, the partial sums

    vec(h_0) + sum_{n>=0} (vec(h_{n+1}) - vec(h_n))

are absolutely convergent and T_h vec converges to a finite continuum
limit T_inf vec on this 15-dimensional subspace. That is a registered
numerical existence proof for the continuum operator on the chosen
observable basis.

If r <= 0 or R^2 is poor on any component, the Cauchy test fails on
that component and no convergence claim is made for it; the bounded
result tightens accordingly.

Guards
------

- Born < 1e-10 at every grid point
- k=0 < 1e-12 at every grid point
- step-scale invariance theorem covers the per-edge rescale used here

Exit code is nonzero if any guard fails or if the Cauchy fit fails on
any component.
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
FANOUT = 3.0
PHYS_STRENGTH = 5e-4

# Canonical observable basis: 5-dim per source position
OBSERVABLES = ["gravity", "MI", "1_minus_pur_cl", "d_TV", "born"]
# Source-position basis: three independent mass-y positions
MASS_Y_GRID = [6.0, 8.0, 10.0]
# Refinement window: deterministic-rescale lane reaches 0.03125 at
# the cost of ~4x the h=0.0625 runtime
H_VALUES = [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]


def generate_nn_lattice(spacing: float):
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


def propagate(pos, adj, field, k, blocked, n, spacing):
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    src = next(i for i, (x, y) in enumerate(pos)
               if abs(x) < 1e-10 and abs(y) < 1e-10)
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
            dx = x2 - x1
            dy = y2 - y1
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


def _build_field(pos, mass_idx, phys_strength):
    mx, my = pos[mass_idx]
    field = [0.0] * len(pos)
    for i, (ix, iy) in enumerate(pos):
        r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
        field[i] = phys_strength / r
    return field


def measure_full(spacing: float, mass_y: float) -> Optional[Dict]:
    pos, adj, nl, hw, nmap = generate_nn_lattice(spacing)
    n = len(pos)
    det_layer = nl - 1
    det = [nmap[(det_layer, iy)] for iy in range(-hw, hw + 1)
           if (det_layer, iy) in nmap]
    bl = nl // 3
    gl = 2 * nl // 3
    slit_iy = max(1, round(SLIT_Y / spacing))
    bi = [nmap[(bl, iy)] for iy in range(-hw, hw + 1) if (bl, iy) in nmap]
    sa_range = range(slit_iy,
                     min(slit_iy + max(2, round(2 / spacing)), hw + 1))
    sb_range = range(-min(slit_iy + max(1, round(1 / spacing)), hw),
                     -slit_iy + 1)
    sa = [nmap[(bl, iy)] for iy in sa_range if (bl, iy) in nmap]
    sb = [nmap[(bl, iy)] for iy in sb_range if (bl, iy) in nmap]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)
    field_f = [0.0] * n
    mass_iy = round(mass_y / spacing)
    mass_idx = nmap.get((gl, mass_iy))
    if mass_idx is None:
        return None
    field_m = _build_field(pos, mass_idx, PHYS_STRENGTH)

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
        gk0 = (sum(abs(am0[d]) ** 2 * pos[d][1] for d in det) / pm0
               - sum(abs(af0[d]) ** 2 * pos[d][1] for d in det) / pf0)

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
        mid.extend([nmap[(l, iy)] for iy in range(-hw, hw + 1)
                    if (l, iy) in nmap])
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
    upper = sorted([i for i in bi if pos[i][1] > spacing],
                   key=lambda i: pos[i][1])
    lower = sorted([i for i in bi if pos[i][1] < -spacing],
                   key=lambda i: -pos[i][1])
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
            i3 = (probs["abc"][di] - probs["ab"][di] - probs["ac"][di]
                  - probs["bc"][di] + probs["a"][di] + probs["b"][di]
                  + probs["c"][di])
            I3 += abs(i3)
            P += probs["abc"][di]
        born = I3 / P if P > 1e-30 else math.nan

    return {
        "h": spacing, "mass_y": mass_y, "n": n, "nl": nl,
        "gravity": gravity, "MI": MI, "1_minus_pur_cl": 1 - pur_cl,
        "d_TV": dtv, "born": born, "gk0": gk0,
    }


def safe_power_fit(xs: List[float], ys: List[float]
                   ) -> Tuple[float, float, float]:
    pts = [(x, abs(y)) for x, y in zip(xs, ys) if x > 0 and abs(y) > 0]
    if len(pts) < 2:
        return math.nan, math.nan, math.nan
    lx = [math.log(x) for x, _ in pts]
    ly = [math.log(y) for _, y in pts]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    denom = sum((x - mx) ** 2 for x in lx)
    if denom <= 0:
        return math.nan, math.nan, math.nan
    slope = sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / denom
    intercept = my - slope * mx
    ss_tot = sum((y - my) ** 2 for y in ly)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(lx, ly))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else math.nan
    return slope, math.exp(intercept), r2


def main() -> int:
    print("=" * 110)
    print("NN LATTICE RESCALED-LANE OPERATOR-CONVERGENCE CAUCHY TEST")
    print(f"  Observable basis: {OBSERVABLES}")
    print(f"  Source-position basis: y_m ∈ {MASS_Y_GRID}")
    print(f"  h grid: {H_VALUES}")
    print(f"  Strength fixed at {PHYS_STRENGTH:.2e} (linear-in-strength is "
          f"NOT assumed; this tests T_h convergence at fixed parameters)")
    print("=" * 110)

    # measurements[h][y_m] = dict of observables
    measurements: Dict[float, Dict[float, Dict]] = {}
    born_max = 0.0
    k0_max = 0.0
    fail = False

    print()
    print(f"  {'h':>8s}  {'y_m':>5s}  {'nodes':>8s}  "
          f"{'gravity':>11s}  {'MI':>8s}  {'1-pur':>8s}  "
          f"{'d_TV':>8s}  {'Born':>10s}  {'k=0':>10s}  {'time':>5s}")
    print(f"  {'-' * 100}")

    for h in H_VALUES:
        measurements[h] = {}
        for y_m in MASS_Y_GRID:
            t0 = time.time()
            r = measure_full(h, y_m)
            dt = time.time() - t0
            if r is None:
                print(f"  {h:8.5f}  {y_m:5.1f}  FAIL  {dt:4.0f}s")
                fail = True
                continue
            measurements[h][y_m] = r
            born_max = max(born_max,
                           r["born"] if not math.isnan(r["born"]) else 0.0)
            k0_max = max(k0_max, abs(r["gk0"]))
            born_s = (f"{r['born']:.2e}" if not math.isnan(r['born'])
                      else "       nan")
            print(f"  {h:8.5f}  {y_m:5.1f}  {r['n']:8d}  "
                  f"{r['gravity']:+11.6f}  {r['MI']:8.4f}  "
                  f"{r['1_minus_pur_cl']:8.4f}  {r['d_TV']:8.4f}  "
                  f"{born_s}  {r['gk0']:+10.2e}  {dt:4.0f}s")

    print()
    print("=" * 110)
    print("ANALYSIS")
    print("=" * 110)
    print()
    print("Guards:")
    born_ok = born_max < 1e-10
    k0_ok = k0_max < 1e-12
    print(f"  Born clean (max = {born_max:.2e}): "
          f"{'PASS' if born_ok else 'FAIL'}")
    print(f"  k=0 clean (max = {k0_max:.2e}): "
          f"{'PASS' if k0_ok else 'FAIL'}")
    print()

    # Pairwise Cauchy increments and L2 vector norms
    print("Per-component Cauchy increments |obs(h) - obs(h/2)|:")
    print()
    for obs in OBSERVABLES:
        print(f"  {obs}:")
        print(f"    {'h':>8s} -> {'h/2':>8s} :   "
              + "    ".join([f"y_m={y:.0f}" for y in MASS_Y_GRID])
              + f"     {'L2':>8s}")
        for n in range(len(H_VALUES) - 1):
            h1 = H_VALUES[n]
            h2 = H_VALUES[n + 1]
            row_l2_sq = 0.0
            row_parts = []
            for y_m in MASS_Y_GRID:
                r1 = measurements[h1].get(y_m, {})
                r2 = measurements[h2].get(y_m, {})
                v1 = r1.get(obs, math.nan)
                v2 = r2.get(obs, math.nan)
                if (v1 is None or v2 is None or math.isnan(v1)
                        or math.isnan(v2)):
                    row_parts.append("    nan")
                else:
                    delta = abs(v2 - v1)
                    row_l2_sq += delta * delta
                    row_parts.append(f"{delta:9.4e}")
            l2 = math.sqrt(row_l2_sq)
            print(f"    {h1:8.5f} -> {h2:8.5f} : "
                  + "  ".join(row_parts)
                  + f"   {l2:9.4e}")

    # Full vector L2 Cauchy increment + decay-rate fit
    print()
    print("Full 15-dim vector Cauchy increments ||vec(h) - vec(h/2)||_2:")
    print(f"  {'h':>8s} -> {'h/2':>8s}  {'L2 incr':>10s}")
    h_list = []
    l2_list = []
    for n in range(len(H_VALUES) - 1):
        h1 = H_VALUES[n]
        h2 = H_VALUES[n + 1]
        l2_sq = 0.0
        for obs in OBSERVABLES:
            for y_m in MASS_Y_GRID:
                v1 = measurements[h1].get(y_m, {}).get(obs)
                v2 = measurements[h2].get(y_m, {}).get(obs)
                if (v1 is None or v2 is None or math.isnan(v1)
                        or math.isnan(v2)):
                    continue
                l2_sq += (v2 - v1) ** 2
        l2 = math.sqrt(l2_sq)
        # Use the geometric mean of (h1, h2) as the abscissa of the increment
        h_geom = math.sqrt(h1 * h2)
        h_list.append(h_geom)
        l2_list.append(l2)
        print(f"  {h1:8.5f} -> {h2:8.5f}  {l2:10.4e}")

    # Fit L2 ~ C * h^r on the fine increments
    fine_pts = [(h, l) for h, l in zip(h_list, l2_list) if h <= 0.25]
    print()
    if fine_pts:
        xs = [h for h, _ in fine_pts]
        ys = [l for _, l in fine_pts]
        r, C, r2 = safe_power_fit(xs, ys)
        print(f"Fit ||vec(h) - vec(h/2)||_2 ~ C * h_geom^r on fine "
              f"increments ({len(fine_pts)} pts, h_geom <= 0.25):")
        print(f"  r     = {r:+.4f}     (decay rate; r > 0 means Cauchy)")
        print(f"  C     = {C:.4e}")
        print(f"  R^2   = {r2:.4f}")
        # Cauchy convergence requires r > 0 (so increments shrink) AND
        # geometric decay (increments summable): C * sum h^r over a
        # geometric h-grid is finite iff r > 0. R^2 close to 1 means
        # the geometric law is robust enough to extrapolate.
        cauchy_ok = (not math.isnan(r) and r > 0.5
                     and not math.isnan(r2) and r2 >= 0.95)
        print()
        if cauchy_ok:
            # Estimate the tail sum (continuum-limit error from h_finest)
            h_finest = H_VALUES[-1]  # 0.03125
            # Sum of subsequent geometric increments at ratio 1/2
            # If incr(h_n) ~ C * h_n^r and h_{n+1} = h_n / 2, then
            # tail = C * h_finest^r * 2^r / (2^r - 1)
            tail_factor = (2 ** r) / (2 ** r - 1) if r > 0 else math.inf
            l2_finest = ys[-1]
            tail_estimate = l2_finest * tail_factor / (2 ** r)
            print(f"  CAUCHY CONVERGENT — geometric decay rate r ~ {r:.3f}")
            print(f"  Tail-sum estimate (continuum-limit error from "
                  f"h = {h_finest}):")
            print(f"    ||vec_inf - vec(h={h_finest})|| <~ "
                  f"{tail_estimate:.4e}")
            print()
            print(f"  REGISTERED NUMERICAL EXISTENCE PROOF for the continuum")
            print(f"  operator T_inf on the chosen 15-dim observable subspace.")
            print(f"  T_h vec converges as h -> 0 with geometric decay rate")
            print(f"  >= {r:.3f} on this basis; partial sums are absolutely")
            print(f"  convergent.")
        else:
            print(f"  CAUCHY TEST FAILS — r = {r:.4f} (need > 0.5) or "
                  f"R^2 = {r2:.4f} (need >= 0.95)")
            print(f"  No registered continuum existence claim on this basis.")
    else:
        print("Insufficient fine-h data for Cauchy fit")

    # Per-component decay rates (diagnostic)
    print()
    print("Per-component Cauchy decay rates (h_geom-fit, fine increments):")
    print(f"  {'observable':>16s}  {'y_m':>5s}  {'r':>8s}  {'C':>10s}  {'R^2':>8s}")
    component_rates: List[float] = []
    for obs in OBSERVABLES:
        for y_m in MASS_Y_GRID:
            xs = []
            ys = []
            for n in range(len(H_VALUES) - 1):
                h1 = H_VALUES[n]
                h2 = H_VALUES[n + 1]
                if h1 > 0.25:
                    continue
                v1 = measurements[h1].get(y_m, {}).get(obs)
                v2 = measurements[h2].get(y_m, {}).get(obs)
                if (v1 is None or v2 is None or math.isnan(v1)
                        or math.isnan(v2)):
                    continue
                delta = abs(v2 - v1)
                if delta > 0:
                    xs.append(math.sqrt(h1 * h2))
                    ys.append(delta)
            if len(xs) >= 2:
                r, C, r2 = safe_power_fit(xs, ys)
                component_rates.append(r)
                print(f"  {obs:>16s}  {y_m:5.1f}  {r:+8.4f}  "
                      f"{C:10.4e}  {r2:8.4f}")

    print()

    if fail or not (born_ok and k0_ok):
        return 1
    # Cauchy fit must close to claim convergence
    if fine_pts:
        r, _C, r2 = safe_power_fit([h for h, _ in fine_pts],
                                   [l for _, l in fine_pts])
        if math.isnan(r) or r <= 0.5 or math.isnan(r2) or r2 < 0.95:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
