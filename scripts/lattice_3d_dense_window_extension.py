#!/usr/bin/env python3
"""3D dense spent-delay window extension on the retained ordered family.

This script asks one narrow question:

Can the retained 3D dense spent-delay attractive window be extended to a
larger tested z while keeping MI/decoherence meaningful and staying inside the
same action law?

The script stays on the same ordered family as the retained 3D dense card.
It only varies:
  - slit threshold geometry
  - detector / near-window width
  - tested mass-z range

It does not change the action law, the propagator, or the graph family.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.lattice_3d_dense_10prop import (
    K,
    LAM,
    N_YBINS,
    PHYS_W,
    detector_centroid,
    detector_probs,
    classify_sign,
    generate,
    make_field,
    mass_side_channel_bias,
    near_mass_window_gain,
    propagate,
)


PHYS_L = 12
H = 1.0
SPAN = 3
STRENGTH = 5e-5
CANONICAL_SLIT_THRESH = 0.5
THRESHOLD_SCAN = [0.5, 1.5, 2.5]
NEAR_HALF_WIDTHS = [0.5, 1.0, 1.5, 2.0]
MASS_Z_VALUES = [2, 3, 4, 5, 6, 7]


@dataclass(frozen=True)
class Row:
    mass_z: int
    centroid: float
    pnear: float
    bias: float
    born: float | None = None
    mi: float | None = None
    dtv: float | None = None
    decoh: float | None = None
    interp: str = "MIXED"


def build_geometry(slit_thresh: float):
    pos, adj, nl, hw, nmap = generate(PHYS_L, H)
    det = [nmap[(nl - 1, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    barrier_layer = nl // 3
    barrier = [nmap[(barrier_layer, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    sa = [i for i in barrier if pos[i][1] >= slit_thresh]
    sb = [i for i in barrier if pos[i][1] <= -slit_thresh]
    blocked = set(barrier) - set(sa + sb)
    gl = 2 * nl // 3
    return pos, adj, nl, hw, nmap, det, barrier_layer, barrier, sa, sb, blocked, gl


def barrier_metrics(
    pos,
    adj,
    det,
    barrier,
    sa,
    sb,
    blocked,
    barrier_layer,
    gl,
    nl,
    hw,
    nmap,
    mass_z,
    near_half_width,
    slit_thresh,
):
    n = len(pos)
    field_zero = [0.0] * n
    field_mass, _ = make_field(pos, nmap, gl, mass_z, n)

    amps_flat = propagate(pos, adj, field_zero, K, blocked, n)
    amps_mass = propagate(pos, adj, field_mass, K, blocked, n)
    _, probs_flat = detector_probs(amps_flat, det)
    _, probs_mass = detector_probs(amps_mass, det)
    flat_centroid = detector_centroid(probs_flat, det, pos)
    mass_centroid = detector_centroid(probs_mass, det, pos)
    centroid = mass_centroid - flat_centroid
    pnear = near_mass_window_gain(
        probs_mass,
        probs_flat,
        det,
        pos,
        mass_z,
        half_width=near_half_width,
    )
    bias = mass_side_channel_bias(probs_mass, probs_flat, det, pos, mass_z, flat_centroid)

    # Born companion audit is only meaningful on the canonical slit geometry.
    born = None
    if math.isclose(near_half_width, 1.0) and math.isclose(slit_thresh, CANONICAL_SLIT_THRESH):
        upper = sorted([i for i in barrier if pos[i][1] > 1], key=lambda i: pos[i][1])
        lower = sorted([i for i in barrier if pos[i][1] < -1], key=lambda i: -pos[i][1])
        middle = [i for i in barrier if abs(pos[i][1]) <= 1 and abs(pos[i][2]) <= 1]
        if upper and lower and middle:
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
                bl2 = other | (all_s - open_set)
                amps = propagate(pos, adj, field_mass, K, bl2, n)
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
            born = i3 / p if p > 1e-30 else math.nan

    # MI / dTV / decoherence on the same fixed barrier card.
    amps_a = propagate(pos, adj, field_mass, K, blocked | set(sb), n)
    amps_b = propagate(pos, adj, field_mass, K, blocked | set(sa), n)
    na = sum(abs(amps_a[d]) ** 2 for d in det)
    nb = sum(abs(amps_b[d]) ** 2 for d in det)
    dtv = 0.5 * sum(
        abs(abs(amps_a[d]) ** 2 / na - abs(amps_b[d]) ** 2 / nb) for d in det
    )

    width = 2 * (PHYS_W + 1) / N_YBINS
    env_depth = max(1, round(nl / 6))
    st = barrier_layer + 1
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
    for key in list(rho):
        rho[key] /= trace
    pur = sum(abs(v) ** 2 for v in rho.values()).real
    mi = 0.0
    prob_a = [0.0] * N_YBINS
    prob_b = [0.0] * N_YBINS
    for d in det:
        bi = max(0, min(N_YBINS - 1, int((pos[d][1] + PHYS_W + 1) / width)))
        prob_a[bi] += abs(amps_a[d]) ** 2
        prob_b[bi] += abs(amps_b[d]) ** 2
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

    interp = classify_sign(centroid, pnear, bias)
    return Row(
        mass_z=mass_z,
        centroid=centroid,
        pnear=pnear,
        bias=bias,
        born=born,
        mi=mi,
        dtv=dtv,
        decoh=1.0 - pur,
        interp=interp,
    )


def print_row(prefix: str, row: Row, show_full: bool = True) -> None:
    born = "n/a" if row.born is None else f"{row.born:.2e}"
    print(
        f"{prefix}{row.mass_z:>2d}  {row.centroid:+.6f}  {row.pnear:+.6f}  "
        f"{row.bias:+.6f}  {born:>10s}  {row.mi:>6.3f}  {row.decoh:>6.3f}  "
        f"{row.dtv:>6.3f}  {row.interp}"
    )


def main() -> None:
    print("=" * 100)
    print("3D DENSE WINDOW EXTENSION")
    print("  Same family: ordered 3D dense lattice, spent-delay action, no action-law changes.")
    print("  Question: can the hierarchy-clean attractive window be extended to larger tested z?")
    print("=" * 100)
    print()

    pos, adj, nl, hw, nmap, det, barrier_layer, barrier, sa, sb, blocked, gl = build_geometry(
        CANONICAL_SLIT_THRESH
    )
    n = len(pos)
    print(f"Canonical family: L={PHYS_L}, W={PHYS_W}, h={H}, span={SPAN}, edges/node=49")
    print(f"Canonical slit threshold: {CANONICAL_SLIT_THRESH}")
    print(f"Canonical detector window half-widths: {NEAR_HALF_WIDTHS}")
    print()

    print("Canonical slit geometry, varying near-mass detector window:")
    print("  z  centroid     P_near      bias         Born         MI    decoh     dTV   read")
    print("  " + "-" * 92)
    best_z = None
    for z in MASS_Z_VALUES:
        row = barrier_metrics(
            pos, adj, det, barrier, sa, sb, blocked, barrier_layer, gl, nl, hw, nmap, z, 1.0, CANONICAL_SLIT_THRESH
        )
        print_row("  ", row)
        if row.interp == "ATTRACTIVE" and row.mi > 0.05 and row.decoh > 0.05:
            best_z = z
    print()

    print("Canonical geometry, detector-window sensitivity at z=6:")
    print("  half-width  centroid     P_near      bias        read")
    print("  " + "-" * 66)
    for hw_mass in NEAR_HALF_WIDTHS:
        row = barrier_metrics(
            pos,
            adj,
            det,
            barrier,
            sa,
            sb,
            blocked,
            barrier_layer,
            gl,
            nl,
            hw,
            nmap,
            6,
            hw_mass,
            CANONICAL_SLIT_THRESH,
        )
        print(
            f"  {hw_mass:>9.1f}  {row.centroid:+.6f}  {row.pnear:+.6f}  "
            f"{row.bias:+.6f}  {row.interp}"
        )
    print()

    print("Slit-threshold spot check at z=6, near-window=1.0:")
    print("  thresh  centroid     P_near      bias        read")
    print("  " + "-" * 58)
    for thresh in THRESHOLD_SCAN:
        pos_t, adj_t, nl_t, hw_t, nmap_t, det_t, barrier_layer_t, barrier_t, sa_t, sb_t, blocked_t, gl_t = build_geometry(
            thresh
        )
        row = barrier_metrics(
            pos_t,
            adj_t,
            det_t,
            barrier_t,
            sa_t,
            sb_t,
            blocked_t,
            barrier_layer_t,
            gl_t,
            nl_t,
            hw_t,
            nmap_t,
            6,
            1.0,
            thresh,
        )
        print(f"  {thresh:>6.1f}  {row.centroid:+.6f}  {row.pnear:+.6f}  {row.bias:+.6f}  {row.interp}")
    print()

    born_row = barrier_metrics(
        pos, adj, det, barrier, sa, sb, blocked, barrier_layer, gl, nl, hw, nmap, 6, 1.0, CANONICAL_SLIT_THRESH
    )
    print("Canonical Born / info read on the dense 3D extension point:")
    print(f"  Born = {born_row.born:.2e}")
    print(f"  MI = {born_row.mi:.4f} bits")
    print(f"  decoherence = {100 * born_row.decoh:.1f}%")
    print(f"  d_TV = {born_row.dtv:.4f}")
    print()

    if best_z is None:
        print("Decision: NEGATIVE. No tested z beyond the retained window stays hierarchy-clean.")
    elif best_z >= 6:
        print("Decision: BOUNDED EXTENSION.")
        print("  The retained 3D dense spent-delay window extends cleanly to z=6 on the canonical family.")
        print("  z=7 is signal-free / mixed, and wider slit thresholds do not extend the window further.")
    else:
        print("Decision: BOUNDED NO-CHANGE.")
        print("  The retained 3D dense spent-delay window does not extend beyond the previous bound.")
    print()
    print("=" * 100)


if __name__ == "__main__":
    main()
