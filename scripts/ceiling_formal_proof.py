#!/usr/bin/env python3
"""Formal analysis of the CLT decoherence ceiling.

Formalizes: "Linear path-sum propagation on connected DAGs produces
single-slit detector distributions that converge in total variation
distance as depth N grows."

Approach:
  1. Extract per-layer transfer matrices T_l
  2. Compute Lyapunov exponent spectrum via QR iteration
  3. Measure d_TV(|ψ_A|², |ψ_B|²) at detector
  4. Measure overlap ⟨ψ_A|ψ_B⟩
  5. Check Lindeberg condition
  6. Fit power laws, verify shared exponent
  7. Report spectral gap λ₁ - λ₂

If spectral gap is large: the product T_N...T_1 is effectively rank-1,
meaning ALL initial conditions converge to the same direction —
this IS the CLT mechanism formalized as a spectral property.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import random
import time
from collections import defaultdict, deque

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag

BETA = 0.8
K = 5.0  # Single k — no band averaging
N_SEEDS = 16
N_LAYERS_LIST = [12, 15, 18, 22, 25, 30, 40, 60, 80]
NPL = 25
Y_RANGE = 10.0
CONNECT_RADIUS = 2.5
N_YBINS = 8


def build_layer_map(positions):
    """Map node indices to layers."""
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    return by_layer


def extract_transfer_matrices(positions, adj, field, k, by_layer):
    """Extract per-layer transfer matrices T_l.

    T_l[j_local, i_local] = kernel(i, j) if edge (i,j) exists, else 0.
    Returns list of (T_l, layer_from_indices, layer_to_indices).
    """
    layers = sorted(by_layer.keys())
    matrices = []

    for li in range(len(layers) - 1):
        from_nodes = by_layer[layers[li]]
        to_nodes = by_layer[layers[li + 1]]
        n_from = len(from_nodes)
        n_to = len(to_nodes)

        if n_from == 0 or n_to == 0:
            continue

        # Build local index maps
        from_map = {node: i for i, node in enumerate(from_nodes)}
        to_map = {node: j for j, node in enumerate(to_nodes)}

        T = np.zeros((n_to, n_from), dtype=complex)

        for i_global in from_nodes:
            i_local = from_map[i_global]
            for j_global in adj.get(i_global, []):
                if j_global in to_map:
                    j_local = to_map[j_global]
                    x1, y1 = positions[i_global]
                    x2, y2 = positions[j_global]
                    dx, dy = x2 - x1, y2 - y1
                    L = math.sqrt(dx * dx + dy * dy)
                    if L < 1e-10:
                        continue
                    lf = 0.5 * (field[i_global] + field[j_global])
                    dl = L * (1 + lf)
                    ret = math.sqrt(max(dl * dl - L * L, 0))
                    act = dl - ret
                    theta = math.atan2(abs(dy), max(dx, 1e-10))
                    w = math.exp(-BETA * theta * theta)
                    ea = cmath.exp(1j * k * act) * w / L
                    T[j_local, i_local] += ea

        matrices.append((T, from_nodes, to_nodes))

    return matrices


def compute_lyapunov_spectrum(matrices, n_exponents=5):
    """Compute Lyapunov exponents via QR iteration on square transfer matrices.

    Since layers may have different sizes, we work with the product
    M = T_N ... T_1 restricted to the common dimension. For layers
    with different node counts, pad with zeros.

    Alternative approach: compute singular values of the full product
    on the first few seeds and extract the spectrum from those.
    """
    if not matrices:
        return np.zeros(n_exponents)

    # Find the most common layer size
    sizes = [T.shape[1] for T, _, _ in matrices]
    common_size = max(set(sizes), key=sizes.count)
    n_track = min(n_exponents, common_size)

    # Build padded square matrices and multiply
    # Use SVD of accumulated product for stability
    product = np.eye(common_size, dtype=complex)
    log_sum = 0.0
    n_steps = 0

    for T, from_nodes, to_nodes in matrices:
        n_to, n_from = T.shape
        # Pad/crop to common_size × common_size
        T_sq = np.zeros((common_size, common_size), dtype=complex)
        r = min(n_to, common_size)
        c = min(n_from, common_size)
        T_sq[:r, :c] = T[:r, :c]

        product = T_sq @ product
        n_steps += 1

        # Periodically renormalize to avoid overflow/underflow
        if n_steps % 5 == 0:
            norm = np.linalg.norm(product)
            if norm > 1e-30:
                log_sum += math.log(norm)
                product /= norm

    # Final SVD
    try:
        s = np.linalg.svd(product, compute_uv=False)
        # Lyapunov exponents from singular values
        lyap = np.zeros(n_track)
        for i in range(min(n_track, len(s))):
            if s[i] > 1e-30:
                lyap[i] = (math.log(s[i]) + log_sum) / max(1, n_steps)
            else:
                lyap[i] = -float('inf')
        return lyap
    except Exception:
        return np.full(n_track, float('nan'))


def compute_tv_distance(psi_a, psi_b, positions, det_nodes):
    """Total variation distance between single-slit detector distributions."""
    pa = np.array([abs(psi_a[d]) ** 2 for d in det_nodes])
    pb = np.array([abs(psi_b[d]) ** 2 for d in det_nodes])
    na, nb = pa.sum(), pb.sum()
    if na < 1e-30 or nb < 1e-30:
        return float('nan')
    pa /= na
    pb /= nb
    return 0.5 * np.sum(np.abs(pa - pb))


def compute_overlap(psi_a, psi_b, det_nodes):
    """Overlap integral |⟨ψ_A|ψ_B⟩|² / (N_A * N_B)."""
    va = np.array([psi_a[d] for d in det_nodes])
    vb = np.array([psi_b[d] for d in det_nodes])
    na = np.sum(np.abs(va) ** 2)
    nb = np.sum(np.abs(vb) ** 2)
    if na < 1e-30 or nb < 1e-30:
        return float('nan')
    inner = np.abs(np.sum(np.conj(va) * vb)) ** 2
    return inner / (na * nb)


def check_lindeberg(matrices):
    """Check Lindeberg condition: max_l ||T_l||²_F / Σ_l ||T_l||²_F → 0."""
    frob_sq = []
    for T, _, _ in matrices:
        frob_sq.append(np.sum(np.abs(T) ** 2))
    if not frob_sq:
        return 0.0
    total = sum(frob_sq)
    if total < 1e-30:
        return 0.0
    return max(frob_sq) / total


def compute_pur_min(psi_a, psi_b, det_nodes):
    """Bath-independent purity floor (D=0)."""
    n_det = len(det_nodes)
    rho = np.zeros((n_det, n_det), dtype=complex)
    for i, d1 in enumerate(det_nodes):
        for j, d2 in enumerate(det_nodes):
            rho[i, j] = (np.conj(psi_a[d1]) * psi_a[d2]
                         + np.conj(psi_b[d1]) * psi_b[d2])
    tr = np.real(np.trace(rho))
    if tr < 1e-30:
        return float('nan')
    rho /= tr
    return np.real(np.trace(rho @ rho))


def propagate(positions, adj, field, src, k, blocked):
    """Standard linear 2D propagator."""
    n = len(positions)
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

    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def _mean_se(vals):
    vals = [v for v in vals if not math.isnan(v)]
    if not vals:
        return float('nan'), float('nan')
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def fit_power_law(xs, ys):
    """Log-log linear regression. Returns (A, alpha, R²)."""
    pairs = [(x, y) for x, y in zip(xs, ys) if y > 0 and not math.isnan(y)]
    if len(pairs) < 3:
        return float('nan'), float('nan'), float('nan')
    lx = [math.log(x) for x, _ in pairs]
    ly = [math.log(y) for _, y in pairs]
    n = len(lx)
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    if sxx < 1e-10:
        return float('nan'), float('nan'), float('nan')
    b = sxy / sxx
    a = my - b * mx
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my) ** 2 for y in ly)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return math.exp(a), b, r2


def main():
    print("=" * 100)
    print("FORMAL CLT CEILING ANALYSIS")
    print(f"  2D DAGs, npl={NPL}, connect_radius={CONNECT_RADIUS}, k={K}")
    print(f"  {N_SEEDS} seeds, N = {N_LAYERS_LIST}")
    print("=" * 100)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    # Collect per-N averages
    n_vals = []
    dtv_vals = []
    overlap_vals = []
    purmin_vals = []
    lyap_gap_vals = []
    lindeberg_vals = []

    print(f"  {'N':>4s}  {'d_TV':>10s}  {'overlap':>10s}  {'1-pur_min':>10s}  "
          f"{'lyap_gap':>10s}  {'lindeberg':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 75}")

    for nl in N_LAYERS_LIST:
        t0 = time.time()
        dtv_all, ovlp_all, pur_all, lgap_all, lind_all = [], [], [], [], []

        for seed in seeds:
            positions, adj, arrival = generate_causal_dag(
                n_layers=nl, nodes_per_layer=NPL,
                y_range=Y_RANGE, connect_radius=CONNECT_RADIUS,
                rng_seed=seed)
            n = len(positions)
            by_layer = build_layer_map(positions)
            layers = sorted(by_layer.keys())
            if len(layers) < 5:
                continue

            src = by_layer[layers[0]]
            det_nodes = by_layer[layers[-1]]
            if not det_nodes:
                continue

            # Barrier and slits
            cy = sum(p[1] for p in positions) / n
            bl_idx = len(layers) // 3
            bi = by_layer[layers[bl_idx]]
            sa = [i for i in bi if positions[i][1] > cy + 2][:3]
            sb = [i for i in bi if positions[i][1] < cy - 2][:3]
            if not sa or not sb:
                continue
            blocked = set(bi) - set(sa + sb)

            field = [0.0] * n  # flat field for ceiling analysis

            # Transfer matrices
            matrices = extract_transfer_matrices(positions, adj, field, K, by_layer)

            # Lyapunov spectrum
            lyap = compute_lyapunov_spectrum(matrices, n_exponents=5)
            if len(lyap) >= 2:
                gap = lyap[0] - lyap[1]
                lgap_all.append(gap)

            # Lindeberg condition
            lind = check_lindeberg(matrices)
            lind_all.append(lind)

            # Single-slit propagation
            psi_a = propagate(positions, adj, field, src, K, blocked | set(sb))
            psi_b = propagate(positions, adj, field, src, K, blocked | set(sa))

            # TV distance
            dtv = compute_tv_distance(psi_a, psi_b, positions, det_nodes)
            if not math.isnan(dtv):
                dtv_all.append(dtv)

            # Overlap
            ovlp = compute_overlap(psi_a, psi_b, det_nodes)
            if not math.isnan(ovlp):
                ovlp_all.append(ovlp)

            # Purity
            pur = compute_pur_min(psi_a, psi_b, det_nodes)
            if not math.isnan(pur):
                pur_all.append(1 - pur)

        dt = time.time() - t0
        mdtv, _ = _mean_se(dtv_all)
        movlp, _ = _mean_se(ovlp_all)
        mpur, _ = _mean_se(pur_all)
        mlgap, _ = _mean_se(lgap_all)
        mlind, _ = _mean_se(lind_all)
        n_ok = len(dtv_all)

        print(f"  {nl:4d}  {mdtv:10.4f}  {movlp:10.4f}  {mpur:10.4f}  "
              f"{mlgap:10.4f}  {mlind:10.4f}  {n_ok:3d}  {dt:4.0f}s")

        if not math.isnan(mdtv):
            n_vals.append(nl)
            dtv_vals.append(mdtv)
            overlap_vals.append(1 - movlp if not math.isnan(movlp) else float('nan'))
            purmin_vals.append(mpur)
            lyap_gap_vals.append(mlgap)
            lindeberg_vals.append(mlind)

    print()

    # Power law fits
    print("POWER LAW FITS: quantity = A × N^alpha")
    print(f"  {'quantity':>12s}  {'A':>8s}  {'alpha':>8s}  {'R²':>6s}")
    print(f"  {'-' * 38}")

    for name, vals in [("d_TV", dtv_vals), ("1-overlap", overlap_vals), ("1-pur_min", purmin_vals)]:
        A, alpha, r2 = fit_power_law(n_vals, vals)
        if not math.isnan(A):
            print(f"  {name:>12s}  {A:8.3f}  {alpha:8.2f}  {r2:6.3f}")
        else:
            print(f"  {name:>12s}  insufficient data")

    print()

    # Lyapunov analysis
    print("LYAPUNOV SPECTRAL GAP (λ₁ - λ₂)")
    print(f"  {'N':>4s}  {'gap':>10s}  {'interpretation':>40s}")
    print(f"  {'-' * 58}")
    for nl, gap in zip(n_vals, lyap_gap_vals):
        if math.isnan(gap):
            continue
        interp = "rank-1 convergence" if gap > 0.5 else ("moderate gap" if gap > 0.1 else "weak gap")
        print(f"  {nl:4d}  {gap:10.4f}  {interp:>40s}")

    print()

    # Lindeberg analysis
    print("LINDEBERG CONDITION (max ||T_l||² / Σ||T_l||²)")
    print(f"  {'N':>4s}  {'max_ratio':>10s}  {'interpretation':>30s}")
    print(f"  {'-' * 48}")
    for nl, lind in zip(n_vals, lindeberg_vals):
        if math.isnan(lind):
            continue
        interp = "CLT valid" if lind < 0.2 else ("marginal" if lind < 0.5 else "CLT may fail")
        print(f"  {nl:4d}  {lind:10.4f}  {interp:>30s}")

    print()
    print("THEOREM STRUCTURE:")
    print("  IF spectral gap is large AND Lindeberg holds:")
    print("    → Product T_N...T_1 drives ANY two initial vectors")
    print("      toward the same dominant direction")
    print("    → Single-slit distributions ψ_A and ψ_B converge")
    print("    → d_TV → 0, overlap → 1, pur_min → 1")
    print("    → Decoherence ceiling is a SPECTRAL PROPERTY")
    print("      of the transfer matrix product")
    print()
    print("  IF shared exponent across d_TV, overlap, 1-pur_min:")
    print("    → All three decay at the same rate")
    print("    → The CLT mechanism is the SOLE driver")
    print("    → No mechanism operating on the bath or propagator")
    print("      can change the exponent without changing the")
    print("      spectral gap of T_N...T_1")


if __name__ == "__main__":
    main()
