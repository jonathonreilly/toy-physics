#!/usr/bin/env python3
"""Joint validation for the regular 2D lattice family.

This script freezes the strongest currently claimed single-family lattice story
in a review-safe way:
  - barrier-lattice: Born, MI, d_TV, CL-bath purity, gravity, k=0
  - no-barrier lattice: distance-law magnitude fit on the same ordered family

The goal is not to prove all ten project properties. The goal is to determine
which parts of the single-family lattice claim are actually retained on a
script/log chain in this checkout.
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.lattice_mirror_distance import compute_field_at_b, generate_lattice_mirror, propagate
from scripts.mirror_2d_validation import entropy

K = 5.0
LAM = 10.0
N_YBINS = 8
B_VALUES = [3, 5, 7, 10, 13, 16, 19]


def mutual_info_and_purity(amps_a, amps_b, det_list):
    pa = [abs(amps_a[d]) ** 2 for d in det_list]
    pb = [abs(amps_b[d]) ** 2 for d in det_list]
    na = sum(pa)
    nb = sum(pb)
    if na < 1e-30 or nb < 1e-30:
        return None
    pa = [p / na for p in pa]
    pb = [p / nb for p in pb]
    pd = [0.5 * a + 0.5 * b for a, b in zip(pa, pb)]
    mi = entropy(pd) - 0.5 * (entropy(pa) + entropy(pb))
    rho = {}
    for i, d1 in enumerate(det_list):
        for j, d2 in enumerate(det_list):
            rho[(i, j)] = (
                amps_a[d1].conjugate() * amps_a[d2] / na
                + amps_b[d1].conjugate() * amps_b[d2] / nb
            )
    tr = sum(rho[(i, i)] for i in range(len(det_list))).real
    if tr <= 1e-30:
        return None
    for key in rho:
        rho[key] /= tr
    pur_min = sum(abs(v) ** 2 for v in rho.values()).real
    return {"MI": mi, "pur_min": pur_min}


def bin_amplitudes(amps, positions, node_ids, half_width):
    bins = [0j] * N_YBINS
    width = 2.0 * half_width / N_YBINS
    for i in node_ids:
        y = positions[i][1]
        bi = int((y + half_width) / width)
        bi = max(0, min(N_YBINS - 1, bi))
        bins[bi] += amps[i]
    return bins


def cl_purity(amps_a, amps_b, positions, mid_nodes, det_list, half_width):
    ba = bin_amplitudes(amps_a, positions, mid_nodes, half_width)
    bb = bin_amplitudes(amps_b, positions, mid_nodes, half_width)
    s = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    na = sum(abs(a) ** 2 for a in ba)
    nb = sum(abs(b) ** 2 for b in bb)
    sn = s / (na + nb) if (na + nb) > 0 else 0.0
    d_cl = math.exp(-(LAM ** 2) * sn)
    rho = {}
    for i, d1 in enumerate(det_list):
        for j, d2 in enumerate(det_list):
            rho[(i, j)] = (
                amps_a[d1].conjugate() * amps_a[d2]
                + amps_b[d1].conjugate() * amps_b[d2]
                + d_cl * amps_a[d1].conjugate() * amps_b[d2]
                + d_cl * amps_b[d1].conjugate() * amps_a[d2]
            )
    tr = sum(rho[(i, i)] for i in range(len(det_list))).real
    if tr <= 1e-30:
        return math.nan, math.nan
    for key in rho:
        rho[key] /= tr
    pur_cl = sum(abs(v) ** 2 for v in rho.values()).real
    return pur_cl, sn


def sorkin_born(positions, adj, src, k, barrier_nodes, slit_a, slit_b, slit_c, det_list, field):
    all_slits = set(slit_a + slit_b + slit_c)
    other = set(barrier_nodes) - all_slits
    probs = {}
    for key, open_set in [
        ("abc", all_slits),
        ("ab", set(slit_a + slit_b)),
        ("ac", set(slit_a + slit_c)),
        ("bc", set(slit_b + slit_c)),
        ("a", set(slit_a)),
        ("b", set(slit_b)),
        ("c", set(slit_c)),
    ]:
        blocked = other | (all_slits - open_set)
        amps = propagate(positions, adj, field, src, k, blocked)
        probs[key] = [abs(amps[d]) ** 2 for d in det_list]
    i3 = 0.0
    p_abc = 0.0
    for idx in range(len(det_list)):
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
        p_abc += probs["abc"][idx]
    return i3 / p_abc if p_abc > 1e-30 else math.nan


def centroid_y(amps, positions, det_list):
    total = 0.0
    weighted = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        weighted += p * positions[d][1]
    return weighted / total if total > 1e-30 else math.nan


def fit_power_law(points):
    usable = [(b, v) for b, v in points if b > 0 and v > 0 and not math.isnan(v)]
    if len(usable) < 3:
        return None
    xs = [math.log(b) for b, _ in usable]
    ys = [math.log(v) for _, v in usable]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 1e-12 or syy <= 1e-12:
        return None
    alpha = sxy / sxx
    coeff = math.exp(my - alpha * mx)
    r2 = (sxy * sxy) / (sxx * syy)
    return coeff, alpha, r2


def main():
    n_layers = 40
    half_width = 20
    slit_gap = 2

    positions, adj, barrier_layer, node_map = generate_lattice_mirror(n_layers, half_width, 42)
    layers = sorted({round(p[0]) for p in positions})
    src = [node_map[(layers[0], 0)]]
    det_list = [node_map[(layers[-1], y)] for y in range(-half_width, half_width + 1)]
    grav_layer = layers[2 * len(layers) // 3]
    field_zero = [0.0] * len(positions)

    barrier_nodes = [node_map[(barrier_layer, y)] for y in range(-half_width, half_width + 1)]
    slit_a = [node_map[(barrier_layer, y)] for y in range(slit_gap + 1, half_width + 1)]
    slit_b = [node_map[(barrier_layer, y)] for y in range(-half_width, -slit_gap)]
    slit_c = [node_map[(barrier_layer, y)] for y in range(-1, 2) if (barrier_layer, y) in node_map]
    blocked = set(barrier_nodes) - set(slit_a + slit_b)

    field_m, _ = compute_field_at_b(positions, node_map, grav_layer, 7, n_mass=1)
    psi_a = propagate(positions, adj, field_m, src, K, blocked | set(slit_b))
    psi_b = propagate(positions, adj, field_m, src, K, blocked | set(slit_a))
    mi_row = mutual_info_and_purity(psi_a, psi_b, det_list)

    pa = {d: abs(psi_a[d]) ** 2 for d in det_list}
    pb = {d: abs(psi_b[d]) ** 2 for d in det_list}
    na = sum(pa.values())
    nb = sum(pb.values())
    dtv = 0.5 * sum(abs(pa[d] / na - pb[d] / nb) for d in det_list) if na > 1e-30 and nb > 1e-30 else math.nan

    bl_idx = len(layers) // 3
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(n_layers / 6)))
    mid_nodes = []
    for layer in layers[start:stop]:
        for y in range(-half_width, half_width + 1):
            mid_nodes.append(node_map[(layer, y)])
    pur_cl, s_norm = cl_purity(psi_a, psi_b, positions, mid_nodes, det_list, half_width)

    am = propagate(positions, adj, field_m, src, K, blocked)
    af = propagate(positions, adj, field_zero, src, K, blocked)
    grav = centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list)

    am0 = propagate(positions, adj, field_m, src, 0.0, blocked)
    af0 = propagate(positions, adj, field_zero, src, 0.0, blocked)
    grav0 = centroid_y(am0, positions, det_list) - centroid_y(af0, positions, det_list)

    born_a = [node_map[(barrier_layer, y)] for y in range(3, 6) if (barrier_layer, y) in node_map]
    born_b = [node_map[(barrier_layer, y)] for y in range(-5, -2) if (barrier_layer, y) in node_map]
    born_c = [node_map[(barrier_layer, y)] for y in range(-1, 2) if (barrier_layer, y) in node_map]
    born = sorkin_born(positions, adj, src, K, barrier_nodes, born_a, born_b, born_c, det_list, field_zero)

    print("=" * 88)
    print("LATTICE FAMILY VALIDATION")
    print("  regular 2D lattice family: barrier joint card + no-barrier distance law")
    print(f"  N={n_layers}, half_width={half_width}, k={K}")
    print("=" * 88)
    print()
    print("Barrier-lattice joint card (b=7 mass row):")
    print(f"  MI(bits)   = {mi_row['MI']:.6f}")
    print(f"  pur_min    = {mi_row['pur_min']:.6f}")
    print(f"  pur_cl     = {pur_cl:.6f}")
    print(f"  1-pur_cl   = {1.0 - pur_cl:.4f}")
    print(f"  d_TV       = {dtv:.6f}")
    print(f"  gravity    = {grav:+.6f}")
    print(f"  Born       = {born:.6e}")
    print(f"  k=0        = {grav0:+.6e}")
    print(f"  S_norm     = {s_norm:.6f}")
    print()

    print("No-barrier distance-law branch:")
    rows = []
    for b in B_VALUES:
        field_b, _ = compute_field_at_b(positions, node_map, grav_layer, b, n_mass=1)
        amb = propagate(positions, adj, field_b, src, K, set())
        afb = propagate(positions, adj, field_zero, src, K, set())
        delta = centroid_y(amb, positions, det_list) - centroid_y(afb, positions, det_list)
        rows.append((b, delta))
        print(f"  b={b:2d}  delta={delta:+.6f}  |delta|={abs(delta):.6f}")
    print()
    fit = fit_power_law([(b, abs(delta)) for b, delta in rows if b >= 7])
    if fit:
        coeff, alpha, r2 = fit
        print("Far-field |delta| fit on b >= 7:")
        print(f"  |delta| ~= {coeff:.4f} * b^({alpha:.3f})")
        print(f"  R^2 = {r2:.4f}")


if __name__ == "__main__":
    main()
