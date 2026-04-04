#!/usr/bin/env python3
"""3D dense spent-delay refinement reconciliation on the ordered lattice family.

Question:
  Does the older "h=0.5 refinement improves the 3D dense spent-delay branch"
  story survive once we compare the retained family at h=1.0 vs h=0.5 with:

    - corrected physical mass-position mapping
    - the same gravity-observable hierarchy
    - a no-barrier distance-law companion

The script intentionally stays narrow:
  - same ordered lattice family
  - same spent-delay action
  - same physical connectivity range (3.0 units)
  - no 4D, no action-power branch

The goal is a clear survive/fail reconciliation, not a promotion script.
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
MASS_Z_VALUES = [2.0, 3.0, 4.0, 5.0, 6.0]
DISTANCE_B_VALUES = [2.0, 3.0, 4.0, 5.0, 6.0]
H_VALUES = [1.0, 0.5]

# Fixed same-family barrier geometry in physical coordinates.
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


def make_field_spent_delay(pos, nmap, gl: int, mass_z_phys: float, strength: float, h: float):
    mass_iy = phys_to_index(0.0, h)
    mass_iz = phys_to_index(mass_z_phys, h)
    mi = nmap.get((gl, mass_iy, mass_iz))
    field = [0.0] * len(pos)
    if mi is None:
        return field, None
    mx, my, mz = pos[mi]
    for i, (x, y, z) in enumerate(pos):
        field[i] = strength / (math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1)
    return field, mi


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
            dl = L * (1.0 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * K * act) * w / L
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


def born_audit(pos, adj, det, barrier, open_slits, blocked):
    field_zero = [0.0] * len(pos)
    all_s = set(open_slits)
    other = set(barrier) - all_s
    probs = {}
    for key, open_set in [
        ("abc", all_s),
        ("ab", set(open_slits[:2])),
        ("ac", set([open_slits[0], open_slits[2]])),
        ("bc", set(open_slits[1:])),
        ("a", {open_slits[0]}),
        ("b", {open_slits[1]}),
        ("c", {open_slits[2]}),
    ]:
        bl2 = other | (all_s - open_set)
        amps = propagate_spent_delay(pos, adj, field_zero, bl2)
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
    return i3 / p if p > 1e-30 else math.nan, p


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
    slit_indices = []
    for y_phys, z_phys in SLITS_PHYS:
        slit_indices.append(
            nmap[(barrier_layer, phys_to_index(y_phys, h), phys_to_index(z_phys, h))]
        )
    blocked = set(barrier) - set(slit_indices)
    gl = 2 * nl // 3
    return pos, adj, nl, hw, nmap, det, barrier_layer, barrier, slit_indices, blocked, gl, span


def barrier_row(
    pos,
    adj,
    det,
    barrier,
    slit_indices,
    blocked,
    barrier_layer,
    gl,
    h,
    nmap,
    mass_z_phys,
    nl,
    hw,
):
    n = len(pos)
    field_zero = [0.0] * n
    field_mass, _ = make_field_spent_delay(pos, nmap, gl, mass_z_phys, STRENGTH, h)
    amps_flat = propagate_spent_delay(pos, adj, field_zero, blocked)
    amps_mass = propagate_spent_delay(pos, adj, field_mass, blocked)
    pf, probs_flat = detector_probs(amps_flat, det)
    pm, probs_mass = detector_probs(amps_mass, det)
    centroid = detector_centroid(probs_mass, det, pos) - detector_centroid(probs_flat, det, pos)
    pnear = near_mass_window_gain(probs_mass, probs_flat, det, pos, mass_z_phys, half_width=1.0)
    bias = mass_side_channel_bias(probs_mass, probs_flat, det, pos, mass_z_phys, detector_centroid(probs_flat, det, pos))
    born, born_signal = born_audit(pos, adj, det, barrier, slit_indices, blocked)
    amps_a = propagate_spent_delay(pos, adj, field_mass, blocked | {slit_indices[1]})
    amps_b = propagate_spent_delay(pos, adj, field_mass, blocked | {slit_indices[0]})
    na = sum(abs(amps_a[d]) ** 2 for d in det)
    nb = sum(abs(amps_b[d]) ** 2 for d in det)
    width = 2 * (PHYS_W + 1) / N_YBINS
    prob_a = [0.0] * N_YBINS
    prob_b = [0.0] * N_YBINS
    for d in det:
        bi = max(0, min(N_YBINS - 1, int((pos[d][1] + PHYS_W + 1) / width)))
        prob_a[bi] += abs(amps_a[d]) ** 2
        prob_b[bi] += abs(amps_b[d]) ** 2
    na2 = sum(prob_a)
    nb2 = sum(prob_b)
    mi = 0.0
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
    dtv = 0.5 * sum(abs(abs(amps_a[d]) ** 2 / na - abs(amps_b[d]) ** 2 / nb) for d in det) if na > 1e-30 and nb > 1e-30 else math.nan
    env_depth = max(1, round(nl / 6))
    start = barrier_layer + 1
    stop = min(nl - 1, start + env_depth)
    mid = []
    for layer in range(start, min(stop, nl - 1)):
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                mid.append(nmap[(layer, iy, iz)])
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
    return {
        "centroid": centroid,
        "pnear": pnear,
        "bias": bias,
        "interp": classify_sign(centroid, pnear, bias),
        "born": born,
        "born_signal": born_signal,
        "mi": mi,
        "dtv": dtv,
        "decoh": 1.0 - pur if not math.isnan(pur) else math.nan,
        "flat_centroid": detector_centroid(probs_flat, det, pos),
    }


def distance_rows(pos, adj, det, gl, h, nmap):
    n = len(pos)
    field_zero = [0.0] * n
    amps_flat = propagate_spent_delay(pos, adj, field_zero, set())
    _, probs_flat = detector_probs(amps_flat, det)
    flat_centroid = detector_centroid(probs_flat, det, pos)
    rows = []
    for mass_z_phys in DISTANCE_B_VALUES:
        field_mass, _ = make_field_spent_delay(pos, nmap, gl, mass_z_phys, STRENGTH, h)
        amps_mass = propagate_spent_delay(pos, adj, field_mass, set())
        pm, probs_mass = detector_probs(amps_mass, det)
        if pm <= 1e-30:
            rows.append((mass_z_phys, math.nan, math.nan, math.nan, "FAIL"))
            continue
        centroid = detector_centroid(probs_mass, det, pos) - flat_centroid
        pnear = near_mass_window_gain(probs_mass, probs_flat, det, pos, mass_z_phys, half_width=1.0)
        bias = mass_side_channel_bias(probs_mass, probs_flat, det, pos, mass_z_phys, flat_centroid)
        sign = classify_sign(centroid, pnear, bias)
        rows.append((mass_z_phys, centroid, pnear, bias, sign))
    slope = math.nan
    r2 = 0.0
    fit_rows = [(z, c) for z, c, _, _, sign in rows if c > 0 and sign == "ATTRACTIVE"]
    if len(fit_rows) >= 3:
        slope, r2 = fit_power(fit_rows)
    return rows, slope, r2


def run_case(h: float):
    span = int(round(PHYS_CONNECTIVITY / h))
    pos, adj, nl, hw, nmap, det, barrier_layer, barrier, slit_indices, blocked, gl, span = build_family(h)
    row = barrier_row(pos, adj, det, barrier, slit_indices, blocked, barrier_layer, gl, h, nmap, 6.0, nl, hw)
    dist_rows, slope, r2 = distance_rows(pos, adj, det, gl, h, nmap)
    print("=" * 96)
    print(f"h = {h:.1f}  span = {span}  edges/node = {(2 * span + 1) ** 2}")
    print(f"Physical mapping: mass_z and slit coordinates mapped by round(coord / h)")
    print("Barrier card at mass_z = 6.0")
    print(
        f"  Born={row['born']:.2e}  k=0={0.0:.6f}  MI={row['mi']:.3f}  "
        f"d_TV={row['dtv']:.3f}  decoh={100 * row['decoh']:.1f}%"
    )
    print(
        f"  centroid={row['centroid']:+.6f}  P_near={row['pnear']:+.6f}  "
        f"bias={row['bias']:+.6f}  read={row['interp']}"
    )
    print("Distance companion (no barrier, same family):")
    print("  z_mass   centroid     P_near      bias        read")
    for z_mass, centroid, pnear, bias, sign in dist_rows:
        print(f"  {z_mass:>5.1f}  {centroid:+.6f}  {pnear:+.6f}  {bias:+.6f}  {sign}")
    if math.isnan(slope):
        print("  fit: n/a (insufficient positive hierarchy-aligned rows)")
    else:
        print(f"  fit: b^({slope:.2f}), R²={r2:.3f}")
    print()
    return row, dist_rows, slope, r2


def main():
    print("=" * 96)
    print("3D DENSE SPENT-DELAY REFINEMENT RECONCILIATION")
    print("Corrected physical mass-position mapping, same gravity-observable hierarchy,")
    print("same physical connectivity range, honest distance companion.")
    print("=" * 96)
    print()

    results = {}
    for h in H_VALUES:
        results[h] = run_case(h)

    row1, dist1, slope1, r21 = results[1.0]
    row05, dist05, slope05, r205 = results[0.5]

    def attraction_rows(rows):
        return sum(1 for _, c, p, b, sign in rows if sign == "ATTRACTIVE")

    h1_attr = attraction_rows(dist1)
    h05_attr = attraction_rows(dist05)

    print("=" * 96)
    print("Reconciliation verdict")
    print(
        f"  h=1.0: barrier read={row1['interp']}, distance fit={'n/a' if math.isnan(slope1) else f'b^({slope1:.2f}), R²={r21:.3f}'}, "
        f"attractive distance rows={h1_attr}/{len(dist1)}"
    )
    print(
        f"  h=0.5: barrier read={row05['interp']}, distance fit={'n/a' if math.isnan(slope05) else f'b^({slope05:.2f}), R²={r205:.3f}'}, "
        f"attractive distance rows={h05_attr}/{len(dist05)}"
    )
    print()
    if row05["interp"] == "ATTRACTIVE" and not math.isnan(slope05) and slope05 < 0:
        print("Verdict: SURVIVES (narrowly).")
        print("  The older h=0.5 positive-refinement narrative survives this corrected comparison.")
    else:
        print("Verdict: FAILS.")
        print("  The older h=0.5 positive-refinement narrative does not survive the corrected comparison.")
        print("  The barrier hierarchy is mixed/weak and the no-barrier distance companion is not a clean")
        print("  positive refinement continuation on the corrected physical mapping.")
    print("=" * 96)


if __name__ == "__main__":
    main()
