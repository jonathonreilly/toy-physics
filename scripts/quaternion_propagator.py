#!/usr/bin/env python3
"""Quaternion path-sum propagator.

Hypothesis: quaternion-valued amplitudes with direction-dependent rotation
axes resist rank-1 convergence because quaternion multiplication is
non-commutative. Different paths through the graph accumulate different
rotation sequences, and these don't average out the same way complex
phases do.

The complex propagator: kernel = exp(i*k*action) * w/L
  → scalar phase rotation, commutative
  → products of phases commute: path order doesn't matter for the phase

The quaternion propagator: kernel = exp(k*action * n_hat) * w/L
  → rotation around axis n_hat determined by edge spatial direction
  → quaternion rotations DON'T commute: path order matters
  → different paths produce different rotation sequences

If this breaks rank-1 convergence, the detector distributions from
slits A and B will remain distinguishable at large N.

Measurement: single-k purity (D=0 floor) compared to complex baseline.
Also: Born check via three-slit Sorkin test on chokepoint DAGs.
"""

from __future__ import annotations
import math
import sys
import os
import random
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
K = 5.0
N_SEEDS = 16
N_LAYERS_LIST = [15, 25, 40, 60]
NPL = 30
XYZ_RANGE = 12.0
CONNECT_RADIUS = 4.0


# ---------- quaternion arithmetic ----------

def q_add(p, q):
    return (p[0]+q[0], p[1]+q[1], p[2]+q[2], p[3]+q[3])

def q_mul(p, q):
    """Hamilton product."""
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (
        a1*a2 - b1*b2 - c1*c2 - d1*d2,
        a1*b2 + b1*a2 + c1*d2 - d1*c2,
        a1*c2 - b1*d2 + c1*a2 + d1*b2,
        a1*d2 + b1*c2 - c1*b2 + d1*a2,
    )

def q_conj(q):
    return (q[0], -q[1], -q[2], -q[3])

def q_abs2(q):
    return q[0]*q[0] + q[1]*q[1] + q[2]*q[2] + q[3]*q[3]

def q_scale(q, s):
    return (q[0]*s, q[1]*s, q[2]*s, q[3]*s)

Q_ZERO = (0.0, 0.0, 0.0, 0.0)


# ---------- quaternion kernel ----------

def q_kernel(action, k, w, L, dx, dy, dz):
    """Quaternion propagation kernel.

    Rotation axis from edge spatial direction.
    Rotation angle from k*action.
    Scaled by w/L (directional measure / distance).

    exp(theta * n_hat) = cos(theta) + sin(theta) * n_hat
    where n_hat = (dx, dy, dz) / |(dx, dy, dz)| as a pure quaternion.
    """
    phase = k * action
    r = math.sqrt(dx*dx + dy*dy + dz*dz)
    if r < 1e-10:
        return q_scale((1.0, 0.0, 0.0, 0.0), w / L)
    nx, ny, nz = dx/r, dy/r, dz/r
    cp = math.cos(phase)
    sp = math.sin(phase)
    return q_scale((cp, sp*nx, sp*ny, sp*nz), w / L)


# ---------- complex kernel (baseline) ----------

def c_kernel(action, k, w, L):
    """Standard complex propagation kernel."""
    import cmath
    return cmath.exp(1j * k * action) * w / L


# ---------- graph generation ----------

def _topo_order(adj, n):
    in_deg = [0] * n
    for nbs in adj.values():
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
    return order


def generate_3d_dag(n_layers, npl, xyz_range, connect_radius, rng_seed):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), n_layers // 3


# ---------- propagation ----------

def propagate_quaternion(positions, adj, field, src, k, blocked=None):
    """Quaternion path-sum propagation."""
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [Q_ZERO] * n
    for s in src:
        amps[s] = q_scale((1.0, 0.0, 0.0, 0.0), 1.0 / len(src))

    for i in order:
        if q_abs2(amps[i]) < 1e-60 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            kern = q_kernel(act, k, w, L, dx, dy, dz)
            amps[j] = q_add(amps[j], q_mul(amps[i], kern))

    return amps


def propagate_complex(positions, adj, field, src, k, blocked=None):
    """Standard complex propagation (baseline)."""
    import cmath
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def compute_field_3d(positions, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my, mz = positions[m]
        for i in range(n):
            ix, iy, iz = positions[i]
            r = math.sqrt((ix-mx)**2 + (iy-my)**2 + (iz-mz)**2) + 0.1
            field[i] += 0.1 / r
    return field


# ---------- measurement ----------

def compute_pur_min(probs_a, probs_b, det_nodes):
    """Bath-independent purity floor from Born probabilities.

    ρ = diag(p_A) + diag(p_B)  (D=0, no cross terms)
    pur_min = Tr(ρ²) = Σ_d (p_A(d) + p_B(d))²  / (Σ_d p_A(d) + p_B(d))²
    """
    total = sum(probs_a[d] + probs_b[d] for d in det_nodes)
    if total < 1e-30:
        return float('nan')
    # Normalized
    pur = sum((probs_a[d] + probs_b[d])**2 for d in det_nodes) / total**2
    return pur


def compute_tv_distance(probs_a, probs_b, det_nodes):
    """Total variation distance between slit distributions."""
    na = sum(probs_a[d] for d in det_nodes)
    nb = sum(probs_b[d] for d in det_nodes)
    if na < 1e-30 or nb < 1e-30:
        return float('nan')
    return 0.5 * sum(abs(probs_a[d]/na - probs_b[d]/nb) for d in det_nodes)


def _mean_se(vals):
    vals = [v for v in vals if not math.isnan(v)]
    if not vals: return float('nan'), float('nan')
    m = sum(vals) / len(vals)
    if len(vals) < 2: return m, 0.0
    var = sum((v - m)**2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 100)
    print("QUATERNION vs COMPLEX PROPAGATOR")
    print(f"  3D DAGs, npl={NPL}, k={K}, {N_SEEDS} seeds")
    print("=" * 100)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    print(f"  {'N':>4s}  {'mode':>10s}  {'d_TV':>8s}  {'1-pur_min':>10s}  "
          f"{'gravity':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 60}")

    for nl in N_LAYERS_LIST:
        for mode in ["complex", "quaternion"]:
            t0 = time.time()
            dtv_all, pur_all, grav_all = [], [], []

            for seed in seeds:
                pos, adj, bl = generate_3d_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                n = len(pos)
                by_layer = defaultdict(list)
                for idx, (x, y, z) in enumerate(pos):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 7: continue
                src = by_layer[layers[0]]
                det_nodes = by_layer[layers[-1]]
                if not det_nodes: continue
                cy = sum(pos[i][1] for i in range(n)) / n
                bl_idx = len(layers) // 3
                bi = by_layer[layers[bl_idx]]
                sa = [i for i in bi if pos[i][1] > cy + 3][:3]
                sb = [i for i in bi if pos[i][1] < cy - 3][:3]
                if not sa or not sb: continue
                blocked = set(bi) - set(sa + sb)
                grav_layer = layers[2 * len(layers) // 3]
                mass_nodes = [i for i in by_layer[grav_layer] if pos[i][1] > cy + 1]
                if not mass_nodes: continue

                field_m = compute_field_3d(pos, mass_nodes)
                field_f = [0.0] * n

                if mode == "quaternion":
                    psi_a = propagate_quaternion(pos, adj, field_m, src, K, blocked | set(sb))
                    psi_b = propagate_quaternion(pos, adj, field_m, src, K, blocked | set(sa))
                    pa = {d: q_abs2(psi_a[d]) for d in det_nodes}
                    pb = {d: q_abs2(psi_b[d]) for d in det_nodes}
                    # Gravity
                    am = propagate_quaternion(pos, adj, field_m, src, K, blocked)
                    af = propagate_quaternion(pos, adj, field_f, src, K, blocked)
                    pm = sum(q_abs2(am[d]) for d in det_nodes)
                    pf = sum(q_abs2(af[d]) for d in det_nodes)
                else:
                    psi_a = propagate_complex(pos, adj, field_m, src, K, blocked | set(sb))
                    psi_b = propagate_complex(pos, adj, field_m, src, K, blocked | set(sa))
                    pa = {d: abs(psi_a[d])**2 for d in det_nodes}
                    pb = {d: abs(psi_b[d])**2 for d in det_nodes}
                    am = propagate_complex(pos, adj, field_m, src, K, blocked)
                    af = propagate_complex(pos, adj, field_f, src, K, blocked)
                    pm = sum(abs(am[d])**2 for d in det_nodes)
                    pf = sum(abs(af[d])**2 for d in det_nodes)

                dtv = compute_tv_distance(pa, pb, det_nodes)
                pur = compute_pur_min(pa, pb, det_nodes)
                if not math.isnan(dtv): dtv_all.append(dtv)
                if not math.isnan(pur): pur_all.append(1 - pur)

                if pm > 1e-30 and pf > 1e-30:
                    if mode == "quaternion":
                        ym = sum(q_abs2(am[d]) * pos[d][1] for d in det_nodes) / pm
                        yf = sum(q_abs2(af[d]) * pos[d][1] for d in det_nodes) / pf
                    else:
                        ym = sum(abs(am[d])**2 * pos[d][1] for d in det_nodes) / pm
                        yf = sum(abs(af[d])**2 * pos[d][1] for d in det_nodes) / pf
                    grav_all.append(ym - yf)

            dt = time.time() - t0
            mdtv, _ = _mean_se(dtv_all)
            mpur, _ = _mean_se(pur_all)
            mg, seg = _mean_se(grav_all)
            n_ok = len(dtv_all)
            print(f"  {nl:4d}  {mode:>10s}  {mdtv:8.4f}  {mpur:10.4f}  "
                  f"{mg:+7.4f}±{seg:.3f}  {n_ok:3d}  {dt:4.0f}s")

        print()

    print("KEY:")
    print("  If quaternion d_TV decays SLOWER than complex:")
    print("    → Non-commutativity resists rank-1 convergence")
    print("    → Quaternion amplitudes preserve slit distinguishability")
    print("  If quaternion d_TV decays at SAME rate:")
    print("    → Non-commutativity doesn't help; CLT still applies")
    print("    → Need a different algebraic structure")


if __name__ == "__main__":
    main()
