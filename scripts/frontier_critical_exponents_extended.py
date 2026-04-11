#!/usr/bin/env python3
"""
Critical Exponents Extended — Finite-Size Scaling Probe
========================================================
Extends frontier_critical_exponents.py with:
  - More sizes per family (4 each) for finite-size scaling
  - Proper G_crit detection (contraction threshold crossing)
  - Finite-size scaling collapse: contraction vs (G - G_crit) * n^(1/nu)
  - G_crit ~ n^alpha scaling check
  - beta convergence vs n

Graph families: random geometric, growing, layered cycle.
"""

from __future__ import annotations
import math, time, random, sys
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from scipy.optimize import curve_fit, minimize_scalar

MASS = 0.30
MU2 = 0.22
DT = 0.12
N_ITER = 30

G_SWEEP = np.array([1, 2, 5, 10, 20, 30, 50, 75, 100, 150, 200], dtype=float)


# --------------- graph builders ---------------

def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed, side):
    rng = random.Random(seed)
    coords = []
    colors = []
    index = {}
    adj = {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x + 0.08 * (rng.random() - 0.5),
                           y + 0.08 * (rng.random() - 0.5)))
            colors.append((x + y) % 2)
            index[(x, y)] = idx
            idx += 1
    pos = np.array(coords)
    col = np.array(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i, j)]
            for di, dj in ((1, 0), (0, 1), (1, 1), (1, -1)):
                ii, jj = i + di, j + dj
                if (ii, jj) not in index:
                    continue
                b = index[(ii, jj)]
                if col[a] == col[b]:
                    continue
                if math.hypot(pos[b, 0] - pos[a, 0], pos[b, 1] - pos[a, 1]) <= 1.28:
                    _ae(adj, a, b)
    return pos, col, {k: list(v) for k, v in adj.items()}


def make_growing(seed, n_target):
    rng = random.Random(seed)
    coords = [(0.0, 0.0), (1.0, 0.0)]
    colors = [0, 1]
    adj = {0: {1}, 1: {0}}
    cur = 2
    while cur < n_target:
        px = rng.uniform(-3, 3)
        py = rng.uniform(-3, 3)
        nc = cur % 2
        coords.append((px, py))
        colors.append(nc)
        opp = [i for i in range(cur) if colors[i] != nc]
        if opp:
            ds = sorted([(math.hypot(px - coords[i][0], py - coords[i][1]), i) for i in opp])
            for _, j in ds[:min(4, len(ds))]:
                _ae(adj, cur, j)
        cur += 1
    return (np.array(coords), np.array(colors, dtype=int),
            {k: list(v) for k, v in adj.items()})


def make_layered_cycle(seed, layers, width):
    rng = random.Random(seed)
    coords = []
    colors = []
    layer_nodes = []
    idx = 0
    for layer in range(layers):
        count = max(2, width)
        this_layer = []
        for k in range(count):
            coords.append((float(layer), float(k) + 0.05 * (rng.random() - 0.5)))
            colors.append(layer % 2)
            this_layer.append(idx)
            idx += 1
        layer_nodes.append(this_layer)
    pos = np.array(coords)
    col = np.array(colors, dtype=int)
    n = len(pos)
    adj = {i: set() for i in range(n)}
    for layer in range(layers - 1):
        curr = layer_nodes[layer]
        nxt = layer_nodes[layer + 1]
        for i_pos, i in enumerate(curr):
            j1 = nxt[i_pos % len(nxt)]
            adj[i].add(j1)
            adj[j1].add(i)
            j2 = nxt[(i_pos + 1) % len(nxt)]
            if j2 != j1:
                adj[i].add(j2)
                adj[j2].add(i)
    return pos, col, {k: list(v) for k, v in adj.items()}


# --------------- physics primitives ---------------

def build_laplacian(pos, adj, n):
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            L[i, j] -= w
            L[j, i] -= w
            L[i, i] += w
            L[j, j] += w
    return L.tocsr()


def build_H(pos, col, adj, n, phi=None):
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1.0, -1.0)
    diag = MASS * par
    if phi is not None:
        diag = diag + phi * par
    H.setdiag(diag)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w
    return H.tocsr()


def cn_step(H, psi, n):
    I = speye(n, format='csc')
    ap = (I + 1j * H * DT / 2).tocsc()
    am = I - 1j * H * DT / 2
    return spsolve(ap, am.dot(psi))


def spatial_width(psi, pos):
    rho = np.abs(psi) ** 2
    rho /= np.sum(rho)
    cx = np.sum(rho * pos[:, 0])
    cy = np.sum(rho * pos[:, 1])
    return np.sqrt(np.sum(rho * ((pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2)))


# --------------- measurement ---------------

def measure_width_ratio(pos, col, adj, n, G_val):
    """Run self-gravity at coupling G_val and return width_grav / width_free."""
    src = n // 2
    center = pos[src]
    sigma = 1.15
    psi0 = np.exp(-0.5 * ((pos[:, 0] - center[0]) ** 2 +
                           (pos[:, 1] - center[1]) ** 2) / sigma ** 2).astype(complex)
    psi0 /= np.linalg.norm(psi0)

    L = build_laplacian(pos, adj, n)
    H_free = build_H(pos, col, adj, n)
    reg = (L + MU2 * speye(n, format='csr')).tocsc()

    psi_g = psi0.copy()
    psi_f = psi0.copy()
    for _ in range(N_ITER):
        rho = np.abs(psi_g) ** 2
        phi = spsolve(reg, G_val * rho)
        psi_g = cn_step(build_H(pos, col, adj, n, phi), psi_g, n)
        psi_f = cn_step(H_free, psi_f, n)
    return spatial_width(psi_g, pos) / spatial_width(psi_f, pos)


def sweep_one_config(family_name, pos, col, adj, label):
    """Sweep G for one graph config, return (G_crit, beta, R2, ratios)."""
    n = len(pos)
    ratios = np.empty(len(G_SWEEP))
    for k, G_val in enumerate(G_SWEEP):
        ratios[k] = measure_width_ratio(pos, col, adj, n, G_val)

    # --- find G_crit: first G where ratio < 1.0 (contraction appears) ---
    crossed = np.where(ratios < 1.0)[0]
    if len(crossed) == 0:
        # No contraction at all: G_crit beyond sweep
        return float('nan'), float('nan'), float('nan'), ratios
    idx_cross = crossed[0]
    if idx_cross == 0:
        G_crit = G_SWEEP[0]
    else:
        # Linear interpolation for crossing point
        r0, r1 = ratios[idx_cross - 1], ratios[idx_cross]
        G0, G1 = G_SWEEP[idx_cross - 1], G_SWEEP[idx_cross]
        t = (1.0 - r0) / (r1 - r0) if abs(r1 - r0) > 1e-12 else 0.5
        G_crit = G0 + t * (G1 - G0)

    # --- fit contraction(G) = A * (G - G_crit)^beta for G > G_crit ---
    mask = G_SWEEP > G_crit
    G_above = G_SWEEP[mask]
    contraction = np.clip(1.0 - ratios[mask], 1e-12, None)

    beta_fit = float('nan')
    r2 = float('nan')
    if len(G_above) >= 4:
        try:
            def power_law(G, A, beta):
                return A * (G - G_crit) ** beta

            popt, _ = curve_fit(power_law, G_above, contraction,
                                p0=[0.01, 0.5], maxfev=8000,
                                bounds=([0, 0.05], [10, 3.0]))
            beta_fit = popt[1]
            pred = power_law(G_above, *popt)
            ss_res = np.sum((contraction - pred) ** 2)
            ss_tot = np.sum((contraction - np.mean(contraction)) ** 2)
            r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-20 else float('nan')
        except Exception:
            pass

    return G_crit, beta_fit, r2, ratios


def fit_scaling_exponent(sizes, values, label):
    """Fit values ~ sizes^alpha, return (alpha, R2)."""
    valid = np.isfinite(values) & (values > 0) & np.isfinite(sizes) & (sizes > 0)
    if np.sum(valid) < 3:
        return float('nan'), float('nan')
    x = np.log(sizes[valid])
    y = np.log(values[valid])
    try:
        coeffs = np.polyfit(x, y, 1)
        alpha = coeffs[0]
        pred = np.polyval(coeffs, x)
        ss_res = np.sum((y - pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-20 else float('nan')
        return alpha, r2
    except Exception:
        return float('nan'), float('nan')


def finite_size_collapse_quality(nu, family_data):
    """
    Given a trial nu, compute how well data from different sizes
    collapses onto a single curve when plotted as
      contraction vs (G - G_crit) * n^(1/nu).
    Lower is better (variance of binned means).
    """
    all_points = []
    for n_val, G_crit, ratios in family_data:
        if not np.isfinite(G_crit):
            continue
        for k, G_val in enumerate(G_SWEEP):
            if G_val <= G_crit:
                continue
            x_scaled = (G_val - G_crit) * n_val ** (1.0 / nu)
            y = max(1.0 - ratios[k], 0.0)
            all_points.append((x_scaled, y))
    if len(all_points) < 6:
        return 1e10

    all_points.sort(key=lambda p: p[0])
    xs = np.array([p[0] for p in all_points])
    ys = np.array([p[1] for p in all_points])

    # Bin into ~8 bins, compute variance of y within each bin
    n_bins = min(8, len(xs) // 2)
    if n_bins < 3:
        return 1e10
    edges = np.linspace(xs[0], xs[-1] + 1e-6, n_bins + 1)
    total_var = 0.0
    for b in range(n_bins):
        in_bin = (xs >= edges[b]) & (xs < edges[b + 1])
        if np.sum(in_bin) > 1:
            total_var += np.var(ys[in_bin])
    return total_var


# --------------- main ---------------

if __name__ == '__main__':
    t0 = time.time()
    print("=" * 78)
    print("CRITICAL EXPONENTS EXTENDED — FINITE-SIZE SCALING")
    print("=" * 78)
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, N_ITER={N_ITER}")
    print(f"G sweep: {list(G_SWEEP.astype(int))}")
    print()

    # --- define configurations ---
    families = {
        'random_geometric': [
            ('rg_6x6', 6, lambda s: make_random_geometric(42, s)),
            ('rg_8x8', 8, lambda s: make_random_geometric(42, s)),
            ('rg_10x10', 10, lambda s: make_random_geometric(42, s)),
            ('rg_12x12', 12, lambda s: make_random_geometric(42, s)),
        ],
        'growing': [
            ('grow_32', 32, lambda s: make_growing(42, s)),
            ('grow_48', 48, lambda s: make_growing(42, s)),
            ('grow_64', 64, lambda s: make_growing(42, s)),
            ('grow_96', 96, lambda s: make_growing(42, s)),
        ],
        'layered_cycle': [
            ('lay_6x4', (6, 4), lambda s: make_layered_cycle(42, *s)),
            ('lay_8x6', (8, 6), lambda s: make_layered_cycle(42, *s)),
            ('lay_8x8', (8, 8), lambda s: make_layered_cycle(42, *s)),
            ('lay_10x8', (10, 8), lambda s: make_layered_cycle(42, *s)),
        ],
    }

    # --- run sweeps ---
    all_results = {}  # family -> list of (label, n, G_crit, beta, R2, ratios)

    for fam_name, configs in families.items():
        print(f"--- {fam_name} ---")
        print(f"  {'label':<12s} {'n':>5s} {'G_crit':>8s} {'beta':>8s} {'R^2':>8s}")
        fam_results = []
        for label, size_param, builder in configs:
            pos, col, adj = builder(size_param)
            n = len(pos)
            G_crit, beta, r2, ratios = sweep_one_config(fam_name, pos, col, adj, label)

            gc_s = f"{G_crit:8.2f}" if np.isfinite(G_crit) else f"{'nan':>8s}"
            b_s = f"{beta:8.4f}" if np.isfinite(beta) else f"{'nan':>8s}"
            r2_s = f"{r2:8.4f}" if np.isfinite(r2) else f"{'nan':>8s}"
            print(f"  {label:<12s} {n:5d} {gc_s} {b_s} {r2_s}")
            fam_results.append((label, n, G_crit, beta, r2, ratios))
            sys.stdout.flush()
        all_results[fam_name] = fam_results
        print()

    # --- analysis ---
    print("=" * 78)
    print("SCALING ANALYSIS")
    print("=" * 78)
    print()

    # 1. G_crit vs n scaling
    print("1. G_crit vs n (power-law fit: G_crit ~ n^alpha)")
    print(f"   {'family':<20s} {'alpha':>8s} {'R^2':>8s}")
    for fam_name, results in all_results.items():
        ns = np.array([r[1] for r in results], dtype=float)
        gc = np.array([r[2] for r in results], dtype=float)
        alpha, r2 = fit_scaling_exponent(ns, gc, fam_name)
        a_s = f"{alpha:8.4f}" if np.isfinite(alpha) else f"{'nan':>8s}"
        r2_s = f"{r2:8.4f}" if np.isfinite(r2) else f"{'nan':>8s}"
        print(f"   {fam_name:<20s} {a_s} {r2_s}")
    print()

    # 2. beta convergence
    print("2. Beta convergence with system size")
    print(f"   {'family':<20s} {'n_min':>6s} {'beta_min':>9s} {'n_max':>6s} {'beta_max':>9s} {'delta':>8s}")
    for fam_name, results in all_results.items():
        valid = [(r[1], r[3]) for r in results if np.isfinite(r[3])]
        if len(valid) < 2:
            print(f"   {fam_name:<20s} insufficient fits")
            continue
        valid.sort()
        n_min, b_min = valid[0]
        n_max, b_max = valid[-1]
        delta = abs(b_max - b_min)
        print(f"   {fam_name:<20s} {n_min:6d} {b_min:9.4f} {n_max:6d} {b_max:9.4f} {delta:8.4f}")
    print()

    # 3. Finite-size scaling collapse
    print("3. Finite-size scaling collapse (optimal nu)")
    for fam_name, results in all_results.items():
        family_data = [(r[1], r[2], r[5]) for r in results]
        # Scan nu from 0.3 to 3.0
        best_nu = float('nan')
        best_cost = 1e10
        for nu_trial in np.linspace(0.3, 3.0, 100):
            cost = finite_size_collapse_quality(nu_trial, family_data)
            if cost < best_cost:
                best_cost = cost
                best_nu = nu_trial
        # Refine
        if np.isfinite(best_nu):
            res = minimize_scalar(
                lambda nu: finite_size_collapse_quality(nu, family_data),
                bounds=(max(0.2, best_nu - 0.3), min(4.0, best_nu + 0.3)),
                method='bounded'
            )
            if res.success:
                best_nu = res.x
                best_cost = res.fun
        nu_s = f"{best_nu:.3f}" if np.isfinite(best_nu) else "nan"
        print(f"   {fam_name:<20s}  nu = {nu_s}  (collapse residual = {best_cost:.6f})")
    print()

    # 4. Cross-family comparison
    print("4. Cross-family beta comparison (largest size per family)")
    print(f"   {'family':<20s} {'n':>5s} {'G_crit':>8s} {'beta':>8s} {'R^2':>8s}")
    for fam_name, results in all_results.items():
        # Pick largest-n result with valid fit
        valid = [r for r in results if np.isfinite(r[3]) and np.isfinite(r[4])]
        if not valid:
            print(f"   {fam_name:<20s} no valid fits")
            continue
        best = max(valid, key=lambda r: r[1])
        _, n, gc, beta, r2, _ = best
        print(f"   {fam_name:<20s} {n:5d} {gc:8.2f} {beta:8.4f} {r2:8.4f}")
    print()

    # 5. Full width-ratio table
    print("5. Width ratio table (columns = G values)")
    g_header = "  ".join(f"{int(g):>5d}" for g in G_SWEEP)
    print(f"   {'config':<12s} {'n':>4s}  {g_header}")
    for fam_name, results in all_results.items():
        for label, n, gc, beta, r2, ratios in results:
            row = "  ".join(f"{r:5.3f}" for r in ratios)
            print(f"   {label:<12s} {n:4d}  {row}")
    print()

    # Summary
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    total_configs = sum(len(v) for v in all_results.values())
    valid_fits = sum(1 for v in all_results.values()
                     for r in v if np.isfinite(r[3]) and np.isfinite(r[4]) and r[4] > 0.7)
    print(f"Configurations tested: {total_configs}")
    print(f"Valid fits (R^2 > 0.7): {valid_fits}")

    # Check universality
    best_betas = []
    for fam_name, results in all_results.items():
        valid = [r for r in results if np.isfinite(r[3]) and np.isfinite(r[4]) and r[4] > 0.7]
        if valid:
            best = max(valid, key=lambda r: r[1])
            best_betas.append((fam_name, best[3]))

    if len(best_betas) >= 2:
        betas = [b for _, b in best_betas]
        spread = max(betas) - min(betas)
        mean_beta = np.mean(betas)
        print(f"Beta range across families: {min(betas):.4f} - {max(betas):.4f} (spread {spread:.4f})")
        print(f"Mean beta: {mean_beta:.4f}")
        if spread < 0.15:
            print("Verdict: betas CONVERGE across families => possible universal exponent")
        elif spread < 0.4:
            print("Verdict: moderate spread => weak topology dependence")
        else:
            print("Verdict: large spread => topology-dependent exponents (distinct universality classes)")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")
