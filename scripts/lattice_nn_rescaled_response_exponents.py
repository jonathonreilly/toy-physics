#!/usr/bin/env python3
"""NN lattice rescaled-lane gravity response exponents.

Sharpens the diagnosis from `lattice_nn_rescaled_rg_gravity.py`.

Key finding to verify: the per-edge action

    act = dl - ret = L * (1 + lf) - sqrt(L^2 * (1 + lf)^2 - L^2)
                   = L * (1 + lf) - L * sqrt(2 * lf + lf^2)

has a `sqrt(lf)` leading order in the small-field limit (NOT linear in
lf). So the gravity response on this harness is intrinsically sublinear
in field strength.

To pin down the bridge gap quantitatively, we measure gravity on a
2-D grid of (strength, h) on the deterministic-rescale lane and
extract the response surface

    |gravity(h, s)| = A * h^q * s^p     ( + saturation at large s )

via a joint log-linear fit. Then:

- p tells us the strength-response exponent (expected ~0.5 leading
  order from the sqrt(lf) propagator structure)
- q tells us the h-scaling exponent at fixed strength

For continuum-stable gravity we would need strength scaling
s(h) = BASE * h^(-q/p). The runner reports whether that strength at
h = 0.0625 stays below the saturation threshold ~0.01 (where lf
exits the leading-sqrt regime).

The runner also records the reduced-rank LATTICE_NN_HIGH_PRECISION
step-scale invariance theorem still holds at every grid point: Born
< 1e-10 and k=0 < 1e-12.

The only physics input is the choice of strength grid and h grid.
The fit is descriptive of the harness, not assumed.
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
PHYS_W = 20.0
PHYS_L = 40.0
SLIT_Y = 3.0
MASS_Y = 8.0
FANOUT = 3.0
H_VALUES = [0.5, 0.25, 0.125, 0.0625]
S_VALUES = [1.25e-4, 2.5e-4, 5e-4, 1e-3, 2e-3]
SAT_THRESHOLD = 0.01  # rough field-strength threshold above which lf
                     # exits the leading-sqrt regime at typical r ~ 5


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


def measure_gravity(spacing: float, phys_strength: float
                    ) -> Optional[Dict]:
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
    mass_iy = round(MASS_Y / spacing)
    mass_idx = nmap.get((gl, mass_iy))
    if mass_idx is None:
        return None
    field_m = _build_field(pos, mass_idx, phys_strength)

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

    return {"h": spacing, "phys_strength": phys_strength,
            "gravity": gravity, "gk0": gk0, "born": born}


def joint_log_fit(rows: List[Dict]) -> Tuple[float, float, float, float]:
    """Fit log|gravity| = log(A) + q * log(h) + p * log(s) by ordinary
    least squares. Returns (q, p, log_A, R^2)."""
    pts = [(r["h"], r["phys_strength"], r["gravity"]) for r in rows
           if r is not None and r["h"] > 0 and r["phys_strength"] > 0
           and abs(r["gravity"]) > 0]
    n = len(pts)
    if n < 3:
        return math.nan, math.nan, math.nan, math.nan

    lh = [math.log(h) for h, s, g in pts]
    ls = [math.log(s) for h, s, g in pts]
    lg = [math.log(abs(g)) for h, s, g in pts]

    # Center for numerical stability
    mh = sum(lh) / n
    ms = sum(ls) / n
    mg = sum(lg) / n
    dh = [x - mh for x in lh]
    ds = [x - ms for x in ls]
    dg = [x - mg for x in lg]

    # Normal equations:
    # [Sum dh*dh, Sum dh*ds] [q]   [Sum dh*dg]
    # [Sum ds*dh, Sum ds*ds] [p] = [Sum ds*dg]
    sdhh = sum(x * x for x in dh)
    sdss = sum(x * x for x in ds)
    sdhs = sum(a * b for a, b in zip(dh, ds))
    sdhg = sum(a * b for a, b in zip(dh, dg))
    sdsg = sum(a * b for a, b in zip(ds, dg))

    det = sdhh * sdss - sdhs * sdhs
    if abs(det) < 1e-30:
        return math.nan, math.nan, math.nan, math.nan
    q = (sdss * sdhg - sdhs * sdsg) / det
    p = (sdhh * sdsg - sdhs * sdhg) / det
    log_A = mg - q * mh - p * ms

    ss_tot = sum(x * x for x in dg)
    ss_res = sum((dg[i] - q * dh[i] - p * ds[i]) ** 2 for i in range(n))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else math.nan
    return q, p, log_A, r2


def main() -> int:
    print("=" * 100)
    print("NN LATTICE RESCALED-LANE GRAVITY RESPONSE-EXPONENT FIT")
    print(f"  Joint fit:  |gravity(h, s)| = A * h^q * s^p")
    print(f"  Grid: h ∈ {H_VALUES}, s ∈ {[f'{s:.2e}' for s in S_VALUES]}")
    print(f"  Born guard < 1e-10. k=0 guard < 1e-12.")
    print("=" * 100)
    print()

    rows: List[Dict] = []
    born_max = 0.0
    k0_max = 0.0
    fail = False

    print(f"  {'h':>7s}  {'strength':>11s}  {'gravity':>11s}  "
          f"{'k=0':>10s}  {'Born':>10s}  {'time':>5s}")
    print(f"  {'-' * 70}")
    for h in H_VALUES:
        for s in S_VALUES:
            t0 = time.time()
            r = measure_gravity(h, s)
            dt = time.time() - t0
            if r is None:
                print(f"  {h:7.4f}  {s:11.4e}  FAIL  {dt:4.0f}s")
                fail = True
                continue
            rows.append(r)
            born = r["born"] if not math.isnan(r["born"]) else 0.0
            born_max = max(born_max, born)
            k0_max = max(k0_max, abs(r["gk0"]))
            born_s = (f"{r['born']:.2e}"
                      if not math.isnan(r['born']) else "       nan")
            print(f"  {h:7.4f}  {s:11.4e}  {r['gravity']:+11.6f}  "
                  f"{r['gk0']:+10.2e}  {born_s}  {dt:4.0f}s")

    print()
    print("=" * 100)
    print("ANALYSIS")
    print("=" * 100)
    print()
    print("Guards:")
    born_ok = born_max < 1e-10
    k0_ok = k0_max < 1e-12
    print(f"  Born clean (max = {born_max:.2e}): "
          f"{'PASS' if born_ok else 'FAIL'}")
    print(f"  k=0 clean (max = {k0_max:.2e}): "
          f"{'PASS' if k0_ok else 'FAIL'}")
    print()

    # Joint fit on the full grid
    q_all, p_all, lA_all, r2_all = joint_log_fit(rows)
    print(f"Joint fit on the full grid ({len(rows)} points):")
    print(f"  |gravity(h, s)| = A * h^q * s^p")
    print(f"  q     = {q_all:+.4f}")
    print(f"  p     = {p_all:+.4f}")
    print(f"  log A = {lA_all:+.4f}     (A = {math.exp(lA_all):.4e})")
    print(f"  R^2   = {r2_all:.4f}")
    print()

    # Joint fit on the fine-h subset
    fine_rows = [r for r in rows if r["h"] in {0.25, 0.125, 0.0625}]
    q, p, lA, r2 = joint_log_fit(fine_rows)
    print(f"Joint fit on fine-h subset ({len(fine_rows)} points, "
          f"h ∈ {{0.25, 0.125, 0.0625}}):")
    print(f"  q     = {q:+.4f}")
    print(f"  p     = {p:+.4f}")
    print(f"  log A = {lA:+.4f}     (A = {math.exp(lA):.4e})")
    print(f"  R^2   = {r2:.4f}")
    print()

    if not (math.isnan(q) or math.isnan(p) or p == 0):
        # Critical strength scaling: s_critical(h) = const * h^(-q/p) gives
        # h-stable gravity in this fit regime
        crit_exp = -q / p
        print(f"Critical strength scaling (from fine-h fit):")
        print(f"  s_critical(h) ~ h^({crit_exp:+.4f})")
        print(f"  At h = 0.0625, with prefactor chosen so that")
        print(f"    s_critical(h=0.5) = 5e-4:")
        prefactor = 5e-4 / (0.5 ** crit_exp)
        s_at_finest = prefactor * (0.0625 ** crit_exp)
        print(f"    s_critical(0.0625) = {s_at_finest:.4e}")
        print()
        print(f"Saturation check (linear-sqrt regime requires "
              f"s < {SAT_THRESHOLD} at finest h):")
        if abs(s_at_finest) < SAT_THRESHOLD:
            print(f"  PASS — s_critical(0.0625) = {s_at_finest:.4e} "
                  f"< {SAT_THRESHOLD}")
            print(f"  CONTINUUM-STABLE STRENGTH SCALING FOUND ON THIS HARNESS.")
        else:
            print(f"  FAIL — s_critical(0.0625) = {s_at_finest:.4e} "
                  f">= {SAT_THRESHOLD}")
            print(f"  Continuum-limit gravity blocked by saturation, NOT by")
            print(f"  strength scaling. Tightens the bounded null-result:")
            print(f"  no simple s ~ h^(-q/p) scaling reaches the continuum")
            print(f"  on this harness; deeper structural change needed.")
    print()

    if fail or not (born_ok and k0_ok):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
