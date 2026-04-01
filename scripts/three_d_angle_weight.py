#!/usr/bin/env python3
"""3D generalization of the directional path measure.

In 2D: θ = atan2(|dy|, dx), weight = exp(-β θ²)
In 3D: θ = acos(dx/L), penalizes deviation from forward in any
       transverse direction (y or z).

       θ_3d = acos(dx / sqrt(dx²+dy²+dz²))

This is the natural 3D generalization: penalize the polar angle
relative to the forward (layer) direction.

Test: gravity scaling, gravity sign, k=0→0 on 3D DAGs.

PStack experiment: three-d-angle-weight
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.three_d_gravity import generate_3d_causal_dag, compute_field_3d


BETA = 0.8


def propagate_3d_angle(positions, adj, field, src, det, k):
    """3D propagator with directional angle weight."""
    n = len(positions)
    in_deg = [0]*n
    for i, nbs in adj.items():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)

    amps = [0.0+0.0j]*n
    for s in src:
        amps[s] = 1.0/len(src)
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx = x2-x1
            dy = y2-y1
            dz = z2-z1
            L = math.sqrt(dx*dx+dy*dy+dz*dz)
            if L < 1e-10:
                continue
            # 3D angle: polar angle relative to forward (x) direction
            cos_theta = dx / L
            theta = math.acos(min(max(cos_theta, -1), 1))
            weight = math.exp(-BETA * theta * theta)

            lf = 0.5*(field[i]+field[j])
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0))
            act = dl-ret
            ea = cmath.exp(1j*k*act) * weight / (L**1.0)
            amps[j] += amps[i]*ea

    probs = {d: abs(amps[d])**2 for d in det}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def centroid_y_3d(probs, positions):
    total = sum(probs.values())
    if total == 0:
        return 0.0
    return sum(positions[d][1]*p for d, p in probs.items()) / total


def main():
    k_band = [3.0, 5.0, 7.0]
    n_seeds = 6

    print("=" * 70)
    print("3D DIRECTIONAL PATH MEASURE")
    print(f"  θ = acos(dx/L), weight = exp(-{BETA}×θ²)")
    print("=" * 70)
    print()

    # Gravity scaling
    print("GRAVITY SCALING (3D)")
    print(f"  {'N':>4s}  {'R_std':>7s}  {'R_angle':>7s}")
    print(f"  {'-' * 20}")

    for nl in [8, 12, 16, 20]:
        rs, ra = [], []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_3d_causal_dag(
                n_layers=nl, nodes_per_layer=30, xyz_range=8.0,
                connect_radius=3.0, rng_seed=seed*11+7)
            n = len(positions)
            src = layer_indices[0]
            det = set(layer_indices[-1])
            if not det:
                continue

            all_ys = [y for _, y, _ in positions]
            cy = sum(all_ys)/len(all_ys)
            mid = len(layer_indices)//2
            gm = [i for i in layer_indices[mid] if positions[i][1] > cy+2]
            if len(gm) < 2:
                continue

            free_f = [0.0]*n
            field = compute_field_3d(positions, adj, gm)

            # Standard 3D
            from scripts.three_d_gravity import pathsum_3d
            std_s, ang_s = [], []
            for k in k_band:
                fp = pathsum_3d(positions, adj, free_f, src, det, k)
                mp = pathsum_3d(positions, adj, field, src, det, k)
                std_s.append(centroid_y_3d(mp, positions)-centroid_y_3d(fp, positions))

                fpa = propagate_3d_angle(positions, adj, free_f, src, det, k)
                mpa = propagate_3d_angle(positions, adj, field, src, det, k)
                ang_s.append(centroid_y_3d(mpa, positions)-centroid_y_3d(fpa, positions))

            # Beam width
            fp0 = pathsum_3d(positions, adj, free_f, src, det, 5.0)
            t = sum(fp0.values())
            w = 1.0
            if t > 0:
                mean = sum(positions[d][1]*p for d, p in fp0.items())/t
                var = sum(positions[d][1]**2*p for d, p in fp0.items())/t - mean**2
                w = max(var**0.5, 0.1)

            rs.append(sum(std_s)/len(std_s)/w)
            ra.append(sum(ang_s)/len(ang_s)/w)

        if rs:
            print(f"  {nl:4d}  {sum(rs)/len(rs):+7.3f}  {sum(ra)/len(ra):+7.3f}")

    # k=0 check
    print()
    print("k=0 CHECK (3D)")
    positions, adj, layer_indices = generate_3d_causal_dag(
        n_layers=12, nodes_per_layer=30, xyz_range=8.0,
        connect_radius=3.0, rng_seed=7)
    n = len(positions)
    src = layer_indices[0]
    det = set(layer_indices[-1])
    all_ys = [y for _, y, _ in positions]
    cy = sum(all_ys)/len(all_ys)
    mid = len(layer_indices)//2
    gm = [i for i in layer_indices[mid] if positions[i][1] > cy+2]
    free_f = [0.0]*n
    field = compute_field_3d(positions, adj, gm) if gm else free_f

    fp0 = propagate_3d_angle(positions, adj, free_f, src, det, 0.0)
    mp0 = propagate_3d_angle(positions, adj, field, src, det, 0.0)
    shift0 = centroid_y_3d(mp0, positions) - centroid_y_3d(fp0, positions)
    print(f"  k=0 shift: {shift0:.6f} ({'PASS' if abs(shift0) < 0.01 else 'FAIL'})")

    # Gravity sign check
    print()
    print("GRAVITY SIGN (3D, angle weight)")
    attract = 0
    total = 0
    for seed in range(8):
        positions, adj, layer_indices = generate_3d_causal_dag(
            n_layers=12, nodes_per_layer=30, xyz_range=8.0,
            connect_radius=3.0, rng_seed=seed*11+7)
        n = len(positions)
        src = layer_indices[0]
        det = set(layer_indices[-1])
        if not det: continue
        all_ys = [y for _, y, _ in positions]
        cy = sum(all_ys)/len(all_ys)
        mid = len(layer_indices)//2
        gm = [i for i in layer_indices[mid] if positions[i][1] > cy+2]
        if len(gm) < 2: continue
        mass_cy = sum(positions[i][1] for i in gm)/len(gm)
        free_f = [0.0]*n
        field = compute_field_3d(positions, adj, gm)

        shifts = []
        for k in k_band:
            fpa = propagate_3d_angle(positions, adj, free_f, src, det, k)
            mpa = propagate_3d_angle(positions, adj, field, src, det, k)
            shifts.append(centroid_y_3d(mpa, positions)-centroid_y_3d(fpa, positions))
        avg = sum(shifts)/len(shifts)
        total += 1
        if (mass_cy-cy > 0 and avg > 0.05):
            attract += 1

    print(f"  Attract: {attract}/{total}")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
