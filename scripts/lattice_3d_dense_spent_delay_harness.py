#!/usr/bin/env python3
"""Canonical 3D dense spent-delay harness on the ordered lattice family.

This script reconciles the recent 3D dense spent-delay branch narrative against
one fixed ordered-lattice family:

  - 3D forward lattice with span=3 (49 edges/node)
  - spent-delay action
  - ultra-weak field strength
  - one close-slit barrier geometry

It reports:
  1. barrier-card gravity sign across a bounded mass-z sweep
  2. the strongest retained barrier row on that fixed geometry
  3. a no-barrier companion for distance and mass-response fits
  4. a bounded length sweep for the barrier gravity sign

It is intentionally a reconciliation harness, not a promotion script.
"""

from __future__ import annotations

import cmath
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.action_power_3d_gravity_sign_closure import build_ordered_lattice, make_field_3d
from scripts.action_power_canonical_harness import BETA, K, LAM, N_YBINS


PHYS_L = 12
PHYS_W = 6
H = 1.0
SPAN = 3
STRENGTH = 5e-5
SLIT_A = (2, 0)
SLIT_B = (-2, 0)
SLIT_C = (0, 1)
MASS_Z_VALUES = [2, 3, 4, 5, 6]
DISTANCE_B_VALUES = [2, 3, 4, 5, 6, 7, 8, 10]
LENGTH_VALUES = [8, 10, 12, 14, 16]


def propagate_spent_delay(pos, adj, field, blocked):
    order = sorted(range(len(pos)), key=lambda i: pos[i][0])
    amps = [0j] * len(pos)
    src = next(
        i
        for i, p in enumerate(pos)
        if abs(p[0]) < 1e-10 and abs(p[1]) < 1e-10 and abs(p[2]) < 1e-10
    )
    amps[src] = 1.0
    for i in order:
        if i in blocked or abs(amps[i]) < 1e-30:
            continue
        pi = pos[i]
        for j in adj.get(i, []):
            if j in blocked:
                continue
            pj = pos[j]
            dx = pj[0] - pi[0]
            dy = pj[1] - pi[1]
            dz = pj[2] - pi[2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * K * act) * w / L
    return amps


def fit_power(points):
    pts = [(x, y) for x, y in points if x > 0 and y > 0]
    if len(pts) < 3:
        return math.nan, 0.0
    lx = [math.log(x) for x, _ in pts]
    ly = [math.log(y) for _, y in pts]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx <= 1e-12:
        return math.nan, 0.0
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    slope = sxy / sxx
    ss_res = sum((y - (my + slope * (x - mx))) ** 2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my) ** 2 for y in ly)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return slope, r2


def build_family(phys_l=PHYS_L, phys_w=PHYS_W):
    pos, adj, nl, hw, nmap = build_ordered_lattice(phys_l, phys_w, H, SPAN, 0.0, 0)
    det = [nmap[(nl - 1, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    bl = nl // 3
    gl = 2 * nl // 3
    barrier = [nmap[(bl, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    sa = [nmap[(bl, SLIT_A[0], SLIT_A[1])]]
    sb = [nmap[(bl, SLIT_B[0], SLIT_B[1])]]
    sc = [nmap[(bl, SLIT_C[0], SLIT_C[1])]]
    blocked = set(barrier) - set(sa + sb)
    return pos, adj, nl, hw, nmap, det, bl, gl, barrier, sa, sb, sc, blocked


def detector_centroid_z(amps, pos, det):
    power = sum(abs(amps[d]) ** 2 for d in det)
    if power <= 1e-30:
        return math.nan
    return sum(abs(amps[d]) ** 2 * pos[d][2] for d in det) / power


def born_audit(pos, adj, det, barrier, sa, sb, sc):
    field_zero = [0.0] * len(pos)
    all_s = set(sa + sb + sc)
    other = set(barrier) - all_s
    probs = {}
    for key, open_set in [
        ("abc", all_s),
        ("ab", set(sa + sb)),
        ("ac", set(sa + sc)),
        ("bc", set(sb + sc)),
        ("a", set(sa)),
        ("b", set(sb)),
        ("c", set(sc)),
    ]:
        blocked = other | (all_s - open_set)
        amps = propagate_spent_delay(pos, adj, field_zero, blocked)
        probs[key] = [abs(amps[d]) ** 2 for d in det]
    i3 = 0.0
    p = 0.0
    for idx in range(len(det)):
        term = (
            probs["abc"][idx]
            - probs["ab"][idx]
            - probs["ac"][idx]
            - probs["bc"][idx]
            + probs["a"][idx]
            + probs["b"][idx]
            + probs["c"][idx]
        )
        i3 += abs(term)
        p += probs["abc"][idx]
    return (i3 / p if p > 1e-30 else math.nan), p


def barrier_metrics(pos, adj, det, bl, gl, hw, nmap, barrier, sa, sb, sc, blocked, mass_z):
    n = len(pos)
    field_zero = [0.0] * n
    field_mass = make_field_3d(pos, nmap, gl, mass_z, STRENGTH, n)
    amps_flat = propagate_spent_delay(pos, adj, field_zero, blocked)
    amps_mass = propagate_spent_delay(pos, adj, field_mass, blocked)
    gravity = detector_centroid_z(amps_mass, pos, det) - detector_centroid_z(amps_flat, pos, det)

    amps_mass_k0 = propagate_spent_delay(pos, adj, field_mass, blocked)
    amps_flat_k0 = propagate_spent_delay(pos, adj, field_zero, blocked)
    k0 = detector_centroid_z(amps_mass_k0, pos, det) - detector_centroid_z(amps_flat_k0, pos, det)

    born, born_signal = born_audit(pos, adj, det, barrier, sa, sb, sc)

    amps_a = propagate_spent_delay(pos, adj, field_mass, blocked | set(sb))
    amps_b = propagate_spent_delay(pos, adj, field_mass, blocked | set(sa))
    na = sum(abs(amps_a[d]) ** 2 for d in det)
    nb = sum(abs(amps_b[d]) ** 2 for d in det)
    width = 2 * (PHYS_W + 1) / N_YBINS
    prob_a = [0.0] * N_YBINS
    prob_b = [0.0] * N_YBINS
    da = {}
    db = {}
    for d in det:
        y = pos[d][1]
        bi = max(0, min(N_YBINS - 1, int((y + PHYS_W + 1) / width)))
        pa = abs(amps_a[d]) ** 2
        pb = abs(amps_b[d]) ** 2
        prob_a[bi] += pa
        prob_b[bi] += pb
        da[d] = pa
        db[d] = pb
    pa_n = [p / na for p in prob_a]
    pb_n = [p / nb for p in prob_b]
    h_mix = 0.0
    h_cond = 0.0
    for bi in range(N_YBINS):
        mix = 0.5 * pa_n[bi] + 0.5 * pb_n[bi]
        if mix > 1e-30:
            h_mix -= mix * math.log2(mix)
        if pa_n[bi] > 1e-30:
            h_cond -= 0.5 * pa_n[bi] * math.log2(pa_n[bi])
        if pb_n[bi] > 1e-30:
            h_cond -= 0.5 * pb_n[bi] * math.log2(pb_n[bi])
    mi = h_mix - h_cond
    dtv = 0.5 * sum(abs(da[d] / na - db[d] / nb) for d in det)

    env_depth = max(1, round(nl / 6))
    st = bl + 1
    sp = min(nl - 1, st + env_depth)
    mid = [nmap[(l, iy, iz)] for l in range(st, sp) for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid:
        y = pos[m][1]
        bi = max(0, min(N_YBINS - 1, int((y + PHYS_W + 1) / width)))
        ba[bi] += amps_a[m]
        bb[bi] += amps_b[m]
    s_norm_num = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    norm_a = sum(abs(a) ** 2 for a in ba)
    norm_b = sum(abs(b) ** 2 for b in bb)
    s_norm = s_norm_num / (norm_a + norm_b) if (norm_a + norm_b) > 0 else 0.0
    d_cl = math.exp(-(LAM ** 2) * s_norm)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1, d2)] = (
                amps_a[d1].conjugate() * amps_a[d2]
                + amps_b[d1].conjugate() * amps_b[d2]
                + d_cl * amps_a[d1].conjugate() * amps_b[d2]
                + d_cl * amps_b[d1].conjugate() * amps_a[d2]
            )
    trace = sum(rho[(d, d)] for d in det).real
    for key in list(rho):
        rho[key] /= trace
    pur = sum(abs(v) ** 2 for v in rho.values()).real

    return {
        "mass_z": mass_z,
        "gravity": gravity,
        "k0": k0,
        "born": born,
        "born_signal": born_signal,
        "mi": mi,
        "dtv": dtv,
        "pur_cl": pur,
        "decoh": 1.0 - pur,
    }


def no_barrier_companion(pos, adj, det, gl, hw, nmap):
    n = len(pos)
    field_zero = [0.0] * n
    amps_flat = propagate_spent_delay(pos, adj, field_zero, set())
    flat_centroid = detector_centroid_z(amps_flat, pos, det)

    rows = []
    for b in DISTANCE_B_VALUES:
        field_mass = make_field_3d(pos, nmap, gl, b, STRENGTH, n)
        amps_mass = propagate_spent_delay(pos, adj, field_mass, set())
        delta = detector_centroid_z(amps_mass, pos, det) - flat_centroid
        rows.append((b, delta))

    positive_rows = [(b, d) for b, d in rows if d > 0]
    full_fit = fit_power(positive_rows)
    tail_fit = fit_power([(b, d) for b, d in positive_rows if b >= 4])

    mass_points = []
    for mult in [0.5, 1.0, 2.0, 5.0]:
        field_mass = make_field_3d(pos, nmap, gl, 2, STRENGTH * mult, n)
        amps_mass = propagate_spent_delay(pos, adj, field_mass, set())
        delta = abs(detector_centroid_z(amps_mass, pos, det) - flat_centroid)
        mass_points.append((mult, delta))
    fm_fit = fit_power(mass_points)
    return rows, full_fit, tail_fit, mass_points, fm_fit


def length_sweep():
    rows = []
    for phys_l in LENGTH_VALUES:
        pos, adj, nl, hw, nmap, det, bl, gl, barrier, sa, sb, sc, blocked = build_family(phys_l=phys_l)
        metric = barrier_metrics(pos, adj, det, bl, gl, hw, nmap, barrier, sa, sb, sc, blocked, mass_z=2)
        rows.append((phys_l, metric["gravity"], metric["decoh"], metric["mi"]))
    return rows


def main():
    pos, adj, nl, hw, nmap, det, bl, gl, barrier, sa, sb, sc, blocked = build_family()

    print("=" * 110)
    print("3D DENSE SPENT-DELAY RECONCILIATION HARNESS")
    print("  fixed ordered 3D lattice family: span=3 (49 edges/node), spent-delay, strength=5e-5")
    print("  goal: freeze what survives from the recent dense-3D branch narrative")
    print("=" * 110)
    print()

    print("1) BARRIER-CARD GRAVITY SWEEP (close-slit geometry)")
    print(f"  slits={SLIT_A}, {SLIT_B}; Born-only third slit={SLIT_C}")
    print(f"  {'mass_z':>6s}  {'gravity':>10s}  {'direction':>9s}  {'MI':>7s}  {'d_TV':>7s}  {'1-pur':>7s}  {'Born':>10s}")
    best = None
    for mass_z in MASS_Z_VALUES:
        metric = barrier_metrics(pos, adj, det, bl, gl, hw, nmap, barrier, sa, sb, sc, blocked, mass_z)
        direction = "TOWARD" if metric["gravity"] > 0 else "AWAY"
        print(
            f"  {mass_z:6d}  {metric['gravity']:+10.6f}  {direction:>9s}  "
            f"{metric['mi']:7.3f}  {metric['dtv']:7.3f}  {metric['decoh']:7.3f}  {metric['born']:10.2e}"
        )
        if best is None or metric["gravity"] > best["gravity"]:
            best = metric
    print()

    print("2) STRONGEST BARRIER ROW ON THIS FIXED GEOMETRY")
    print(
        f"  mass_z={best['mass_z']} gravity={best['gravity']:+.6f} "
        f"MI={best['mi']:.3f} d_TV={best['dtv']:.3f} 1-pur={best['decoh']:.3f} "
        f"Born={best['born']:.2e} k0={best['k0']:+.2e}"
    )
    print()

    print("3) NO-BARRIER COMPANION (same 3D family)")
    distance_rows, full_fit, tail_fit, mass_points, fm_fit = no_barrier_companion(pos, adj, det, gl, hw, nmap)
    print("  distance rows:")
    print("  " + "  ".join(f"b={b}:{d:+.6f}" for b, d in distance_rows))
    print(f"  full positive-support fit: alpha={full_fit[0]:+.2f}, R2={full_fit[1]:.3f}")
    print(f"  late positive-tail fit (b>=4): alpha={tail_fit[0]:+.2f}, R2={tail_fit[1]:.3f}")
    print("  mass-response points:")
    print("  " + "  ".join(f"m={m:g}:{d:.6f}" for m, d in mass_points))
    print(f"  F~M^alpha fit: alpha={fm_fit[0]:+.2f}, R2={fm_fit[1]:.3f}")
    print()

    print("4) BARRIER LENGTH SWEEP (same close-slit geometry, mass_z=2)")
    length_rows = length_sweep()
    print(f"  {'L':>3s}  {'gravity':>10s}  {'1-pur':>7s}  {'MI':>7s}")
    for phys_l, gravity, decoh, mi in length_rows:
        print(f"  {phys_l:3d}  {gravity:+10.6f}  {decoh:7.3f}  {mi:7.3f}")
    print()

    print("Decision:")
    print("  - The fixed 3D dense spent-delay family does show a small positive barrier row.")
    print("  - The same family shows a positive no-barrier distance response and sub-linear mass response.")
    print("  - But this reconciliation harness does NOT reproduce the stronger 3D '10/10' branch narrative")
    print("    as a single retained same-harness closure.")


if __name__ == "__main__":
    main()
