#!/usr/bin/env python3
"""Tapered 3D refinement harness on the ordered lattice family.

This is a new topology branch, not a continuation of the retained dense card.
The question is deliberately narrow:

Can a y-tapered 3D ordered lattice keep the same-family Born / k=0 / MI /
decoherence / gravity hierarchy readouts when the lattice is refined from
h=1.0 to h=0.5?

The taper is y-only. z connectivity is kept uniform.
"""

from __future__ import annotations

import cmath
import math
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.lattice_3d_dense_10prop import (  # noqa: E402
    BETA,
    K,
    LAM,
    N_YBINS,
)


PHYS_L = 12.0
PHYS_W = 6.0
STRENGTH = 5e-5
H_VALUES = [1.0, 0.5]

SLIT_THRESH = 0.5
MASS_Z_VALUES = [2, 3, 4, 5, 6]
DISTANCE_B_VALUES = [2, 3, 4, 5, 6, 7]

Y_TAPER_PHYS = 4.0
Y_SPAN_CORE_PHYS = 3.0
Y_SPAN_EDGE_PHYS = 1.0
Z_SPAN_PHYS = 3.0


def build_tapered_lattice(phys_l: float, phys_w: float, h: float):
    nl = int(phys_l / h) + 1
    hw = int(phys_w / h)
    pos = []
    adj = defaultdict(list)
    nmap = {}
    for layer in range(nl):
        x = layer * h
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                idx = len(pos)
                pos.append((x, iy * h, iz * h))
                nmap[(layer, iy, iz)] = idx

    z_span = max(1, round(Z_SPAN_PHYS / h))
    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            y_phys = abs(iy * h)
            taper = min(1.0, y_phys / Y_TAPER_PHYS) if Y_TAPER_PHYS > 0 else 1.0
            span_y_phys = Y_SPAN_CORE_PHYS - (Y_SPAN_CORE_PHYS - Y_SPAN_EDGE_PHYS) * taper
            y_span = max(1, round(span_y_phys / h))
            for iz in range(-hw, hw + 1):
                src = nmap.get((layer, iy, iz))
                if src is None:
                    continue
                for diy in range(-y_span, y_span + 1):
                    iyn = iy + diy
                    if abs(iyn) > hw:
                        continue
                    for diz in range(-z_span, z_span + 1):
                        izn = iz + diz
                        if abs(izn) > hw:
                            continue
                        dst = nmap.get((layer + 1, iyn, izn))
                        if dst is not None:
                            adj[src].append(dst)
    return pos, dict(adj), nl, hw, nmap


def propagate(pos, adj, field, k, blocked):
    order = sorted(range(len(pos)), key=lambda i: pos[i][0])
    amps = [0j] * len(pos)
    src = next(
        i for i, p in enumerate(pos)
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
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / L
    return amps


def make_field(pos, nmap, gl, mass_z_phys, h):
    mi = nmap.get((gl, 0, round(mass_z_phys / h)))
    if mi is None:
        return [0.0] * len(pos), None
    mx, my, mz = pos[mi]
    field = [0.0] * len(pos)
    for i, (x, y, z) in enumerate(pos):
        field[i] = STRENGTH / (math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1)
    return field, mi


def detector_probs(amps, det):
    raw = {d: abs(amps[d]) ** 2 for d in det}
    total = sum(raw.values())
    if total <= 1e-30:
        return 0.0, {d: 0.0 for d in det}
    return total, {d: p / total for d, p in raw.items()}


def detector_centroid(probs, det, pos):
    return sum(probs[d] * pos[d][2] for d in det)


def near_mass_window_gain(probs_mass, probs_flat, det, pos, mass_z_phys, half_width=1.0):
    gain = 0.0
    for d in det:
        if abs(pos[d][2] - mass_z_phys) <= half_width:
            gain += probs_mass[d] - probs_flat[d]
    return gain


def mass_side_channel_bias(probs_mass, probs_flat, det, pos, mass_z_phys, flat_centroid):
    ref = mass_z_phys - flat_centroid
    if abs(ref) <= 1e-12:
        return math.nan
    numer = 0.0
    denom = 0.0
    for d in det:
        side = 1.0 if (pos[d][2] - flat_centroid) * ref >= 0 else -1.0
        delta = probs_mass[d] - probs_flat[d]
        numer += delta * side
        denom += abs(delta)
    return numer / denom if denom > 1e-30 else math.nan


def classify_sign(delta_centroid, delta_pnear, delta_bias):
    if delta_centroid > 0 and delta_pnear > 0 and delta_bias > 0:
        return "ATTRACTIVE"
    if delta_centroid < 0 and delta_pnear < 0 and delta_bias < 0:
        return "AWAY"
    return "MIXED"


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


def count_positive(points):
    return sum(1 for _, y in points if y > 0), len(points)


def born_audit(pos, adj, det, barrier, sa, sb):
    field_zero = [0.0] * len(pos)
    upper = sorted([i for i in barrier if pos[i][1] > SLIT_THRESH], key=lambda i: pos[i][1])
    lower = sorted([i for i in barrier if pos[i][1] < -SLIT_THRESH], key=lambda i: -pos[i][1])
    middle = [i for i in barrier if abs(pos[i][1]) <= SLIT_THRESH and abs(pos[i][2]) <= 1.0]
    if not upper or not lower or not middle:
        return math.nan
    s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
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
        amps = propagate(pos, adj, field_zero, K, blocked)
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
    return i3 / p if p > 1e-30 else math.nan


def measure_h(h: float):
    pos, adj, nl, hw, nmap = build_tapered_lattice(PHYS_L, PHYS_W, h)
    det = [nmap[(nl - 1, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    bl = nl // 3
    gl = 2 * nl // 3
    barrier = [nmap[(bl, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    sa = [i for i in barrier if pos[i][1] >= SLIT_THRESH]
    sb = [i for i in barrier if pos[i][1] <= -SLIT_THRESH]
    blocked = set(barrier) - set(sa + sb)
    n = len(pos)
    field_f = [0.0] * n

    field_m, _ = make_field(pos, nmap, gl, 3, h)
    af = propagate(pos, adj, field_f, K, blocked)
    am = propagate(pos, adj, field_m, K, blocked)
    pf, probs_flat = detector_probs(af, det)
    pm, probs_mass = detector_probs(am, det)
    zf = detector_centroid(probs_flat, det, pos)
    zm = detector_centroid(probs_mass, det, pos)

    # k=0 control
    af0 = propagate(pos, adj, field_f, 0.0, blocked)
    am0 = propagate(pos, adj, field_m, 0.0, blocked)
    pf0, probs_f0 = detector_probs(af0, det)
    pm0, probs_m0 = detector_probs(am0, det)
    k0 = detector_centroid(probs_m0, det, pos) - detector_centroid(probs_f0, det, pos)

    # Born companion audit
    born = born_audit(pos, adj, det, barrier, sa, sb)

    # MI and decoherence
    pa = propagate(pos, adj, field_m, K, blocked | set(sb))
    pb = propagate(pos, adj, field_m, K, blocked | set(sa))
    na = sum(abs(pa[d]) ** 2 for d in det)
    nb = sum(abs(pb[d]) ** 2 for d in det)
    bw = 2 * (PHYS_W + h) / N_YBINS
    prob_a = [0.0] * N_YBINS
    prob_b = [0.0] * N_YBINS
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d][1] + PHYS_W + h) / bw)))
        prob_a[b2] += abs(pa[d]) ** 2
        prob_b[b2] += abs(pb[d]) ** 2
    mi = 0.0
    if na > 1e-30 and nb > 1e-30:
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

    # CL decoherence / dTV
    env_depth = max(1, round(nl / 6))
    st = bl + 1
    sp = min(nl - 1, st + env_depth)
    mid = [
        nmap[(l, iy, iz)]
        for l in range(st, sp)
        for iy in range(-hw, hw + 1)
        for iz in range(-hw, hw + 1)
    ]
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid:
        bi = max(0, min(N_YBINS - 1, int((pos[m][1] + PHYS_W + h) / bw)))
        ba[bi] += pa[m]
        bb[bi] += pb[m]
    s_norm = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    norm_a = sum(abs(a) ** 2 for a in ba)
    norm_b = sum(abs(b) ** 2 for b in bb)
    d_cl = math.exp(-(LAM ** 2) * (s_norm / (norm_a + norm_b) if norm_a + norm_b > 0 else 0.0))
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1, d2)] = (
                pa[d1].conjugate() * pa[d2]
                + pb[d1].conjugate() * pb[d2]
                + d_cl * pa[d1].conjugate() * pb[d2]
                + d_cl * pb[d1].conjugate() * pa[d2]
            )
    trace = sum(rho[(d, d)] for d in det).real
    for key in list(rho):
        rho[key] /= trace
    pur = sum(abs(v) ** 2 for v in rho.values()).real
    da = {d: abs(pa[d]) ** 2 for d in det}
    db = {d: abs(pb[d]) ** 2 for d in det}
    dtv = 0.5 * sum(abs(da[d] / na - db[d] / nb) for d in det) if na > 1e-30 and nb > 1e-30 else math.nan

    centroid = zm - zf
    pnear = near_mass_window_gain(probs_mass, probs_flat, det, pos, 3, half_width=1.0)
    bias = mass_side_channel_bias(probs_mass, probs_flat, det, pos, 3, zf)
    interp = classify_sign(centroid, pnear, bias)

    # Distance law companion
    b_data = []
    d_data = []
    for b in DISTANCE_B_VALUES:
        field_b, _ = make_field(pos, nmap, gl, b, h)
        am_b = propagate(pos, adj, field_b, K, blocked)
        pm_b, probs_b = detector_probs(am_b, det)
        if pm_b > 1e-30:
            zb = detector_centroid(probs_b, det, pos)
            delta = zb - zf
            if delta > 0:
                b_data.append(b)
                d_data.append(delta)
    pos_count, total_count = count_positive(list(zip(b_data, d_data)))
    slope, r2 = fit_power(list(zip(b_data, d_data)))

    return {
        "h": h,
        "born": born,
        "k0": k0,
        "mi": mi,
        "dtv": dtv,
        "decoh": 1.0 - pur,
        "centroid": centroid,
        "pnear": pnear,
        "bias": bias,
        "interp": interp,
        "distance_exp": slope,
        "distance_r2": r2,
        "distance_positive": pos_count,
        "distance_total": total_count,
    }


def main():
    print("=" * 92)
    print("TAPERED 3D REFINEMENT")
    print("  New topology branch: y-only taper, z connectivity uniform")
    print("  Question: does the same-family 3D branch survive refinement at h=0.5?")
    print("=" * 92)
    print()
    print(f"Physical setup: L={PHYS_L}, W={PHYS_W}, strength={STRENGTH}")
    print(f"Taper: y core={Y_SPAN_CORE_PHYS}, y edge={Y_SPAN_EDGE_PHYS}, y taper radius={Y_TAPER_PHYS}, z span={Z_SPAN_PHYS}")
    print(f"Slits: |y| >= {SLIT_THRESH} open on the barrier layer")
    print()

    rows = []
    for h in H_VALUES:
        row = measure_h(h)
        rows.append(row)
        print(f"h={h:.1f}")
        print(f"  Born = {row['born']:.2e}")
        print(f"  k=0 = {row['k0']:+.6f}")
        print(f"  MI = {row['mi']:.4f}")
        print(f"  d_TV = {row['dtv']:.4f}")
        print(f"  Decoherence = {100 * row['decoh']:.1f}%")
        print(f"  Gravity hierarchy: centroid={row['centroid']:+.6f}, P_near={row['pnear']:+.6f}, bias={row['bias']:+.6f} [{row['interp']}]")
        if row["distance_positive"] >= 3:
            print(f"  Distance law: b^({row['distance_exp']:.2f}), R²={row['distance_r2']:.3f}")
        else:
            print(
                f"  Distance law: insufficient positive support "
                f"({row['distance_positive']}/{row['distance_total']})"
            )
        print()

    if len(rows) == 2:
        r1, r05 = rows
        print("Refinement summary:")
        print(f"  Born: h=1.0 -> {r1['born']:.2e}, h=0.5 -> {r05['born']:.2e}")
        print(f"  Gravity hierarchy: h=1.0 {r1['interp']}, h=0.5 {r05['interp']}")
        if r1["distance_positive"] >= 3 or r05["distance_positive"] >= 3:
            print(f"  Distance exponent: h=1.0 {r1['distance_exp']:.2f}, h=0.5 {r05['distance_exp']:.2f}")
        else:
            print(
                f"  Distance support: h=1.0 {r1['distance_positive']}/{r1['distance_total']}, "
                f"h=0.5 {r05['distance_positive']}/{r05['distance_total']}"
            )
        print(f"  MI: h=1.0 {r1['mi']:.4f}, h=0.5 {r05['mi']:.4f}")
        print(f"  Decoherence: h=1.0 {100*r1['decoh']:.1f}%, h=0.5 {100*r05['decoh']:.1f}%")
        print()
        if r1["interp"] == "ATTRACTIVE" and r05["interp"] == "ATTRACTIVE":
            print("Conclusion: tapered 3D survives refinement on the tested window.")
        elif r1["interp"] != "ATTRACTIVE" and r05["interp"] != "ATTRACTIVE":
            print("Conclusion: tapered 3D does not recover hierarchy-clean attraction.")
        else:
            print("Conclusion: mixed refinement result; the branch is not yet a clean rescue.")


if __name__ == "__main__":
    main()
