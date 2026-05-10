#!/usr/bin/env python3
"""NN lattice deterministic-rescale + RG-style gravity probe.

Combines two existing retained pieces:

- the step-scale invariance theorem from
  `LATTICE_NN_HIGH_PRECISION_NOTE.md` (closure addendum 2026-05-07),
  applied as `step_scale = h / sqrt(FANOUT)` per edge — this lets the
  propagation reach h = 0.0625 Born-clean
  (`LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md`)

- the three field-strength schedules tested by
  `scripts/lattice_nn_rg_gravity.py` on the raw kernel: fixed,
  inv_h, inv_sqrt_h. The raw-kernel runner overflowed at h = 0.125,
  so the schedules were never tested on a Born-clean refinement
  window.

Question: does any of the three strength schedules give a clean
h-stable gravity centroid on the rescaled lane through h = 0.0625?

If yes, that is direct evidence that the deterministic-rescale lane
plus the schedule's renormalization choice has a continuum-limit
gravity, and the 19-row "lattice action / refinement /
continuum-limit" sub-lane has a mechanical promotion path.

If no (gravity continues to decay toward zero at finer h, or fits
remain weak), the bounded null result tightens: the simple 1/h
strength scaling is insufficient even on the Born-clean rescaled
lane.

Either outcome is publishable.
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
H_VALUES = [1.0, 0.5, 0.25, 0.125, 0.0625]
# The "inv_h_119" exponent comes from the empirical g_unit(h) ~ h^1.19
# fit on the fixed-strength rescaled lane (this runner, R^2 = 0.9998 on
# h ∈ {0.25, 0.125, 0.0625}). In the small-strength linear regime
# gravity(h, s) ≈ s · g_unit(h), so strength(h) ~ h^-1.19 should give
# h-stable gravity in the continuum limit. The other exponents probe
# either side of the predicted critical scaling so the result has a
# clear bracket.
SCHEMES = ["fixed", "inv_sqrt_h", "inv_h", "inv_h_119", "inv_h_150"]
INV_H_EXPONENT = {
    "inv_h_119": 1.19,
    "inv_h_150": 1.50,
}


def generate_nn_lattice(spacing: float):
    """Raw 3-edge NN lattice (straight, up, down)."""
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


def strength_for_scheme(scheme: str, spacing: float) -> float:
    if scheme == "fixed":
        return BASE_STRENGTH
    if scheme == "inv_h":
        return BASE_STRENGTH / spacing
    if scheme == "inv_sqrt_h":
        return BASE_STRENGTH / math.sqrt(spacing)
    if scheme in INV_H_EXPONENT:
        return BASE_STRENGTH * (spacing ** -INV_H_EXPONENT[scheme])
    raise ValueError(f"unknown scheme: {scheme}")


def propagate(pos, adj, field, k, blocked, n, spacing):
    """Path-sum propagation with deterministic per-step rescale.

    The rescale factor `step_scale = spacing / sqrt(FANOUT)` is the
    same one used by `lattice_nn_deterministic_rescale.py`. By the
    step-scale invariance theorem, every observable in this runner is
    invariant under this rescale on a fixed lattice; the rescale only
    controls float64 representability across refinements.
    """
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


def measure_full(spacing: float, scheme: str) -> Optional[Dict]:
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
    phys_strength = strength_for_scheme(scheme, spacing)
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

    return {
        "h": spacing, "scheme": scheme, "n": n, "nl": nl,
        "phys_strength": phys_strength,
        "gravity": gravity, "gk0": gk0, "born": born,
    }


def safe_power_fit(xs: List[float], ys: List[float]) -> Tuple[float, float, float]:
    """Return (exponent_alpha, prefactor_C, R^2) for |y| ~ C * x^alpha."""
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


def stability_score(values: List[float]) -> Tuple[float, float]:
    """Coefficient-of-variation-style stability score on the finest 3 points.

    Returns (mean, max_relative_deviation) over the last 3 values.
    A continuum-stable schedule has max_relative_deviation -> 0.
    """
    if len(values) < 3:
        return math.nan, math.nan
    last3 = values[-3:]
    mean = sum(last3) / 3
    if abs(mean) < 1e-30:
        return mean, math.nan
    max_rel = max(abs(v - mean) / abs(mean) for v in last3)
    return mean, max_rel


def main():
    print("=" * 110)
    print("NN LATTICE DETERMINISTIC-RESCALE + RG-STRENGTH GRAVITY PROBE")
    print(f"  3 edges/node + step_scale = h/sqrt(3)")
    print(f"  Physical: W={PHYS_W}, L={PHYS_L}, k={K_PHYS}, mass at y={MASS_Y}")
    print(f"  Strength schemes: {SCHEMES}")
    print(f"  h grid: {H_VALUES}")
    print("=" * 110)

    results: Dict[str, List[Dict]] = {s: [] for s in SCHEMES}
    for scheme in SCHEMES:
        print()
        print(f"--- scheme: {scheme} ---")
        print(f"  {'h':>7s}  {'strength':>11s}  {'nodes':>8s}  "
              f"{'gravity':>11s}  {'k=0':>10s}  {'Born':>10s}  {'time':>5s}")
        print(f"  {'-' * 73}")
        for h in H_VALUES:
            t0 = time.time()
            r = measure_full(h, scheme)
            dt = time.time() - t0
            if r is not None:
                born_s = (f"{r['born']:.2e}"
                          if not math.isnan(r['born']) else "       nan")
                print(f"  {h:7.4f}  {r['phys_strength']:11.6e}  "
                      f"{r['n']:8d}  {r['gravity']:+11.6f}  "
                      f"{r['gk0']:+10.2e}  {born_s}  {dt:4.0f}s")
                results[scheme].append(r)
            else:
                print(f"  {h:7.4f}  FAIL  {dt:4.0f}s")

    print()
    print("=" * 110)
    print("ANALYSIS")
    print("=" * 110)
    print()
    print("Born safety on the refinement window:")
    all_born_clean = True
    born_threshold = 1e-10
    for scheme in SCHEMES:
        max_born = max((r["born"] for r in results[scheme]
                        if not math.isnan(r["born"])), default=math.nan)
        clean = (not math.isnan(max_born)) and (max_born < born_threshold)
        all_born_clean = all_born_clean and clean
        print(f"  {scheme:12s}: max Born = {max_born:.2e}  "
              f"({'CLEAN' if clean else 'DIRTY'})")
    print(f"  threshold: {born_threshold:.0e}")

    print()
    print("k=0 control (gravity must vanish at k=0):")
    all_k0_clean = True
    k0_threshold = 1e-12
    for scheme in SCHEMES:
        max_k0 = max((abs(r["gk0"]) for r in results[scheme]), default=math.nan)
        clean = (not math.isnan(max_k0)) and (max_k0 < k0_threshold)
        all_k0_clean = all_k0_clean and clean
        print(f"  {scheme:12s}: max |k=0| = {max_k0:.2e}  "
              f"({'CLEAN' if clean else 'DIRTY'})")

    print()
    print("Power-law fit gravity ~ C * h^alpha (h ∈ {0.25, 0.125, 0.0625} only):")
    fits = {}
    for scheme in SCHEMES:
        # Restrict fit to fine-grid rows where the asymptotic regime can be read.
        rs = [r for r in results[scheme]
              if r["h"] in {0.25, 0.125, 0.0625} and abs(r["gravity"]) > 0]
        xs = [r["h"] for r in rs]
        ys = [r["gravity"] for r in rs]
        alpha, C, r2 = safe_power_fit(xs, ys)
        fits[scheme] = (alpha, C, r2)
        print(f"  {scheme:12s}: alpha = {alpha:+.4f}  "
              f"C = {C:.4e}  R^2 = {r2:.4f}")

    print()
    print("Continuum stability (mean and max-relative-deviation on h ∈ {0.25, 0.125, 0.0625}):")
    stabilities = {}
    for scheme in SCHEMES:
        rs = [r for r in results[scheme] if r["h"] in {0.25, 0.125, 0.0625}]
        rs.sort(key=lambda r: -r["h"])
        mean, max_rel = stability_score([r["gravity"] for r in rs])
        stabilities[scheme] = (mean, max_rel)
        print(f"  {scheme:12s}: mean gravity = {mean:+.6f}  "
              f"max rel dev = {max_rel:.4f}")

    print()
    print("VERDICT")
    print(f"  Born-clean refinement window: "
          f"{'PASS' if all_born_clean else 'FAIL'}")
    print(f"  k=0 control on all schemes: "
          f"{'PASS' if all_k0_clean else 'FAIL'}")
    print()

    # Promotion criterion: |alpha| close to 0 + small max_rel_dev + R^2 not
    # required to be high (R^2 is degenerate when gravity is h-stable, since
    # the variance in log(|gravity|) collapses).
    promotion_alpha_max = 0.15
    promotion_dev_max = 0.05
    promoted = []
    for scheme in SCHEMES:
        alpha, _C, _r2 = fits[scheme]
        _mean, max_rel = stabilities[scheme]
        if (not math.isnan(alpha)
                and abs(alpha) <= promotion_alpha_max
                and not math.isnan(max_rel)
                and max_rel <= promotion_dev_max):
            promoted.append(scheme)
    if promoted:
        print(f"  PROMOTION: scheme(s) {promoted} pass the h-stable criterion")
        print(f"    (|alpha| <= {promotion_alpha_max}, "
              f"max_rel_dev <= {promotion_dev_max})")
        print()
        print("  Interpretation: on the deterministic-rescale lane, the named")
        print("  schedule(s) give a gravity centroid that does not decay toward")
        print("  zero on the finest three points of the refinement window. This")
        print("  is direct numerical evidence that the schedule has a")
        print("  continuum-limit gravity response on this harness.")
    else:
        print(f"  NO PROMOTION: no scheme passes |alpha| <= {promotion_alpha_max}")
        print(f"    AND max_rel_dev <= {promotion_dev_max}")
        print()
        print("  Interpretation: simple 1/h-style strength scaling is")
        print("  insufficient on the rescaled lane to give a clean")
        print("  continuum-limit gravity. The bounded null result tightens.")
    print()


if __name__ == "__main__":
    main()
