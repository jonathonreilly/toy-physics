#!/usr/bin/env python3
"""3D inverse-square kernel branch on the ordered lattice family.

This is a new propagator branch, not a continuation of the retained dense 3D
spent-delay card. The only transport change is the free-kernel attenuation:

    w / L  ->  w / L^2

The action remains the original spent-delay action. The graph family and
physical geometry are matched to the retained 3D dense spent-delay family.

The goal is a bounded head-to-head audit:
  - same 3D ordered family
  - same barrier geometry
  - corrected physical mass-position mapping
  - same gravity-observable hierarchy
  - compare h=1.0 vs h=0.5
"""

from __future__ import annotations

import cmath
import math
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.action_power_canonical_harness import BETA, K, LAM, N_YBINS  # noqa: E402


PHYS_L = 12.0
PHYS_W = 6.0
PHYS_CONNECTIVITY = 3.0
STRENGTH = 5e-5
MASS_Z_VALUES = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
H_VALUES = [1.0, 0.5]
SLITS_PHYS = [(2.0, 0.0), (-2.0, 0.0), (0.0, 1.0)]


def phys_to_index(value: float, h: float) -> int:
    return int(round(value / h))


def build_ordered_lattice(phys_l: float, phys_w: float, h: float, span: int):
    nl = int(round(phys_l / h)) + 1
    hw = int(round(phys_w / h))
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

    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                src = nmap[(layer, iy, iz)]
                for diy in range(-span, span + 1):
                    iyn = iy + diy
                    if abs(iyn) > hw:
                        continue
                    for diz in range(-span, span + 1):
                        izn = iz + diz
                        if abs(izn) > hw:
                            continue
                        dst = nmap[(layer + 1, iyn, izn)]
                        adj[src].append(dst)

    return pos, dict(adj), nl, hw, nmap


def make_field(pos, nmap, gl: int, mass_z_phys: float, strength: float, h: float):
    mi = nmap.get((gl, phys_to_index(0.0, h), phys_to_index(mass_z_phys, h)))
    field = [0.0] * len(pos)
    if mi is None:
        return field, None
    mx, my, mz = pos[mi]
    for i, (x, y, z) in enumerate(pos):
        field[i] = strength / (math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1)
    return field, mi


def propagate_inverse_square(pos, adj, field, blocked, k: float = K):
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
            dl = L * (1.0 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / (L * L)
    return amps


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


def classify_sign(centroid, pnear, bias):
    if centroid > 0 and pnear > 0 and bias > 0:
        return "ATTRACTIVE"
    if centroid < 0 and pnear < 0 and bias < 0:
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


def build_family(h: float):
    span = int(round(PHYS_CONNECTIVITY / h))
    pos, adj, nl, hw, nmap = build_ordered_lattice(PHYS_L, PHYS_W, h, span)
    det = [nmap[(nl - 1, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    barrier_layer = nl // 3
    barrier = [nmap[(barrier_layer, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    slit_indices = [
        nmap[(barrier_layer, phys_to_index(y_phys, h), phys_to_index(z_phys, h))]
        for y_phys, z_phys in SLITS_PHYS
    ]
    blocked = set(barrier) - set(slit_indices)
    gl = 2 * nl // 3
    return pos, adj, nl, hw, nmap, det, barrier_layer, barrier, slit_indices, blocked, gl, span


def born_audit(pos, adj, det, barrier, open_slits):
    field_zero = [0.0] * len(pos)
    all_s = set(open_slits)
    other = set(barrier) - all_s
    probs = {}
    for key, open_set in [
        ("abc", all_s),
        ("ab", set(open_slits[:2])),
        ("ac", {open_slits[0], open_slits[2]}),
        ("bc", set(open_slits[1:])),
        ("a", {open_slits[0]}),
        ("b", {open_slits[1]}),
        ("c", {open_slits[2]}),
    ]:
        blocked = other | (all_s - open_set)
        amps = propagate_inverse_square(pos, adj, field_zero, blocked)
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


def barrier_metrics(pos, adj, det, barrier, slit_indices, blocked, gl, nmap, mass_z_phys, h):
    n = len(pos)
    field_zero = [0.0] * n
    field_mass, _ = make_field(pos, nmap, gl, mass_z_phys, STRENGTH, h)
    amps_flat = propagate_inverse_square(pos, adj, field_zero, blocked)
    amps_mass = propagate_inverse_square(pos, adj, field_mass, blocked)

    _, probs_flat = detector_probs(amps_flat, det)
    _, probs_mass = detector_probs(amps_mass, det)
    zf = detector_centroid(probs_flat, det, pos)
    zm = detector_centroid(probs_mass, det, pos)
    centroid = zm - zf
    pnear = near_mass_window_gain(probs_mass, probs_flat, det, pos, mass_z_phys, half_width=1.0)
    bias = mass_side_channel_bias(probs_mass, probs_flat, det, pos, mass_z_phys, zf)
    interp = classify_sign(centroid, pnear, bias)

    born = born_audit(pos, adj, det, barrier, slit_indices)

    slit_a, slit_b = slit_indices[:2]
    amps_a = propagate_inverse_square(pos, adj, field_mass, blocked | {slit_b})
    amps_b = propagate_inverse_square(pos, adj, field_mass, blocked | {slit_a})
    pa = {d: abs(amps_a[d]) ** 2 for d in det}
    pb = {d: abs(amps_b[d]) ** 2 for d in det}
    na = sum(pa.values())
    nb = sum(pb.values())
    dtv = 0.5 * sum(abs(pa[d] / na - pb[d] / nb) for d in det) if na > 1e-30 and nb > 1e-30 else math.nan

    width = 2 * (PHYS_W + 1) / N_YBINS
    barrier_layer = min(p[0] for p in pos if p[0] > 0)
    bl = round((len({p[0] for p in pos}) - 1) / 3)
    # Use the same downstream environment depth rule as the dense harness.
    nl = int(round(PHYS_L / h)) + 1
    hw = int(round(PHYS_W / h))
    env_depth = max(1, round(nl / 6))
    st = nl // 3 + 1
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
        bi = max(0, min(N_YBINS - 1, int((pos[m][1] + PHYS_W + 1) / width)))
        ba[bi] += amps_a[m]
        bb[bi] += amps_b[m]
    s_norm = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    norm_a = sum(abs(a) ** 2 for a in ba)
    norm_b = sum(abs(b) ** 2 for b in bb)
    d_cl = math.exp(-(LAM ** 2) * (s_norm / (norm_a + norm_b) if norm_a + norm_b > 0 else 0.0))
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
    pur = math.nan
    if trace > 1e-30:
        for key in list(rho):
            rho[key] /= trace
        pur = sum(abs(v) ** 2 for v in rho.values()).real

    prob_a = [0.0] * N_YBINS
    prob_b = [0.0] * N_YBINS
    for d in det:
        bi = max(0, min(N_YBINS - 1, int((pos[d][1] + PHYS_W + 1) / width)))
        prob_a[bi] += abs(amps_a[d]) ** 2
        prob_b[bi] += abs(amps_b[d]) ** 2
    mi = 0.0
    na2 = sum(prob_a)
    nb2 = sum(prob_b)
    if na2 > 1e-30 and nb2 > 1e-30:
        pa_n = [p / na2 for p in prob_a]
        pb_n = [p / nb2 for p in prob_b]
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

    # k=0 control
    amps_f0 = propagate_inverse_square(pos, adj, field_zero, blocked, k=0.0)
    amps_m0 = propagate_inverse_square(pos, adj, field_mass, blocked, k=0.0)
    _, probs_f0 = detector_probs(amps_f0, det)
    _, probs_m0 = detector_probs(amps_m0, det)
    k0 = detector_centroid(probs_m0, det, pos) - detector_centroid(probs_f0, det, pos)

    return {
        "born": born,
        "k0": k0,
        "mi": mi,
        "dtv": dtv,
        "decoh": 1.0 - pur if not math.isnan(pur) else math.nan,
        "centroid": centroid,
        "pnear": pnear,
        "bias": bias,
        "interp": interp,
    }


def no_barrier_distance(pos, adj, det, gl, nmap, h):
    n = len(pos)
    blocked = set()
    field_zero = [0.0] * n
    amps_flat = propagate_inverse_square(pos, adj, field_zero, blocked)
    _, probs_flat = detector_probs(amps_flat, det)
    zf = detector_centroid(probs_flat, det, pos)
    rows = []
    aligned = []
    for mass_z in MASS_Z_VALUES:
        field_mass, _ = make_field(pos, nmap, gl, mass_z, STRENGTH, h)
        amps_mass = propagate_inverse_square(pos, adj, field_mass, blocked)
        _, probs_mass = detector_probs(amps_mass, det)
        zm = detector_centroid(probs_mass, det, pos)
        centroid = zm - zf
        pnear = near_mass_window_gain(probs_mass, probs_flat, det, pos, mass_z, half_width=1.0)
        bias = mass_side_channel_bias(probs_mass, probs_flat, det, pos, mass_z, zf)
        interp = classify_sign(centroid, pnear, bias)
        rows.append((mass_z, centroid, pnear, bias, interp))
        if interp == "ATTRACTIVE":
            aligned.append((mass_z, centroid))
    slope, r2 = fit_power(aligned)
    return rows, aligned, slope, r2


def main():
    print("=" * 100)
    print("3D INVERSE-SQUARE KERNEL BRANCH")
    print("  New propagator branch: same 3D ordered family, same spent-delay action, kernel w/L^2.")
    print("  Goal: bounded h=1.0 vs h=0.5 audit on the same physical geometry.")
    print("=" * 100)
    print()

    print("h    span  Born        k=0        MI      dTV     decoh   centroid    P_near    bias      read")
    print("-" * 108)
    summary = []
    for h in H_VALUES:
        pos, adj, nl, hw, nmap, det, barrier_layer, barrier, slit_indices, blocked, gl, span = build_family(h)
        row = barrier_metrics(pos, adj, det, barrier, slit_indices, blocked, gl, nmap, 3.0, h)
        print(
            f"{h:>3.1f}  {span:>4d}  {row['born']:.2e}  {row['k0']:+.6f}  "
            f"{row['mi']:.3f}  {row['dtv']:.3f}  {row['decoh']:.3f}  "
            f"{row['centroid']:+.6f}  {row['pnear']:+.6f}  {row['bias']:+.6f}  {row['interp']}"
        )
        rows, aligned, slope, r2 = no_barrier_distance(pos, adj, det, gl, nmap, h)
        summary.append((h, rows, len(aligned), slope, r2))

    print()
    print("No-barrier distance companion:")
    for h, rows, n_aligned, slope, r2 in summary:
        print(f"h={h:.1f}")
        print("  z    centroid     P_near      bias        read")
        for mass_z, centroid, pnear, bias, interp in rows:
            print(f"  {mass_z:>3.0f}  {centroid:+.6f}  {pnear:+.6f}  {bias:+.6f}  {interp}")
        if n_aligned >= 3:
            print(f"  hierarchy-aligned support: {n_aligned}/{len(rows)}  fit=b^({slope:.2f})  R^2={r2:.3f}")
        else:
            print(f"  hierarchy-aligned support: {n_aligned}/{len(rows)}  fit=n/a")
        print()

    print("Decision:")
    print("  Promote only if the branch keeps Born/k=0 clean and shows a meaningful attractive")
    print("  hierarchy-aligned distance tail under refinement. Otherwise keep it isolated.")


if __name__ == "__main__":
    main()
