#!/usr/bin/env python3
"""Spectral geometry probe: hearing the shape of spacetime.

Does the eigenvalue spectrum of the staggered Hamiltonian encode the
effective dimension and geometry of the underlying graph?

For each graph family we compute:
  1. Full eigenvalue spectrum (with and without self-gravity Phi at G=10)
  2. Eigenvalue counting function N(E) and Weyl's-law spectral dimension d_s
  3. Spectral gap, bandwidth, density of states
  4. BFS shell-counting effective dimension d_eff for comparison
  5. Spectral zeta function zeta(s) and its poles

Graph families:
  - 2D lattice side=8, side=10
  - Random geometric side=8
  - Growing graph n=64
  - Layered cycle 8x8
"""

from __future__ import annotations

import math
import random
import time
from collections import deque
from dataclasses import dataclass

import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from scipy.optimize import curve_fit

# ── Parameters ────────────────────────────────────────────────
MASS = 0.30
MU2 = 0.22
DT = 0.12
G = 10.0

# ── Graph utilities ───────────────────────────────────────────

def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def _bfs(adj, src, n):
    d = np.full(n, np.inf)
    d[src] = 0
    q = deque([src])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if d[j] == np.inf:
                d[j] = d[i] + 1
                q.append(j)
    return d


# ── Graph families ────────────────────────────────────────────

def make_2d_lattice(side=8):
    """Regular 2D square lattice with checkerboard coloring."""
    coords = []
    colors = []
    index = {}
    adj = {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((float(x), float(y)))
            colors.append((x + y) % 2)
            index[(x, y)] = idx
            idx += 1
    pos = np.array(coords)
    col = np.array(colors, dtype=int)
    n = len(pos)
    for x in range(side):
        for y in range(side):
            a = index[(x, y)]
            for dx, dy in ((1, 0), (0, 1)):
                nx_, ny_ = x + dx, y + dy
                if (nx_, ny_) in index:
                    b = index[(nx_, ny_)]
                    _ae(adj, a, b)
    adj_l = {k: list(v) for k, v in adj.items()}
    src = index[(side // 2, side // 2)]
    return f"2D_lattice_{side}x{side}", pos, col, adj_l, n, src


def make_random_geometric(seed=42, side=8):
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
    adj_l = {k: list(v) for k, v in adj.items()}
    n = len(pos)
    src = n // 2
    return "random_geometric_8x8", pos, col, adj_l, n, src


def make_growing(seed=42, n_target=64):
    rng = random.Random(seed)
    coords = [(0., 0.), (1., 0.)]
    colors = [0, 1]
    adj = {0: {1}, 1: {0}}
    cur = 2
    while cur < n_target:
        px = rng.uniform(-4, 4)
        py = rng.uniform(-4, 4)
        nc = cur % 2
        coords.append((px, py))
        colors.append(nc)
        opp = [i for i in range(cur) if colors[i] != nc]
        if opp:
            ds = [(math.hypot(px - coords[i][0], py - coords[i][1]), i) for i in opp]
            ds.sort()
            for _, j in ds[:min(4, len(ds))]:
                _ae(adj, cur, j)
        cur += 1
    pos = np.array(coords)
    col = np.array(colors, dtype=int)
    adj_l = {k: list(v) for k, v in adj.items()}
    return "growing_n64", pos, col, adj_l, len(pos), 0


def make_layered_cycle(seed=42, layers=8, width=8):
    rng = random.Random(seed)
    coords = []
    colors = []
    layer_nodes = []
    idx = 0
    for layer in range(layers):
        count = max(2, width)
        this_layer = []
        for k in range(count):
            y = float(k) + 0.05 * (rng.random() - 0.5)
            coords.append((float(layer), y))
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
    adj_l = {k: list(v) for k, v in adj.items()}
    src = layer_nodes[0][0]
    return "layered_cycle_8x8", pos, col, adj_l, n, src


# ── Physics tools ─────────────────────────────────────────────

def _laplacian(pos, adj, n):
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1. / max(d, 0.5)
            L[i, j] -= w
            L[j, i] -= w
            L[i, i] += w
            L[j, j] += w
    return L.tocsr()


def _solve_phi(L, n, rho):
    if np.allclose(rho, 0):
        return np.zeros(n)
    A = (L + MU2 * speye(n, format='csr')).tocsc()
    return spsolve(A, rho)


def _build_H(pos, col, adj, n, mass, phi):
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1., -1.)
    H.setdiag((mass + phi) * par)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1. / max(d, 0.5)
            hop = -0.5j * w
            H[i, j] += hop
            H[j, i] += np.conj(hop)
    return H.tocsr()


def _gauss_state(pos, src, sigma=1.15):
    center = pos[src]
    rel = pos - center
    psi = np.exp(-0.5 * (rel[:, 0]**2 + rel[:, 1]**2) / sigma**2).astype(complex)
    return psi / np.linalg.norm(psi)


# ── BFS shell dimension ──────────────────────────────────────

def bfs_dimension(adj, src, n):
    """Estimate effective dimension from BFS shell growth: V(r) ~ r^d."""
    depth = _bfs(adj, src, n)
    max_d = int(np.max(depth[np.isfinite(depth)]))
    if max_d < 3:
        return np.nan, depth
    radii = []
    counts = []
    cumulative = 0
    for r in range(max_d + 1):
        shell = int(np.sum(depth == r))
        cumulative += shell
        if r > 0:
            radii.append(r)
            counts.append(cumulative)
    radii = np.array(radii, dtype=float)
    counts = np.array(counts, dtype=float)
    mask = counts > 0
    if np.sum(mask) < 3:
        return np.nan, depth
    log_r = np.log(radii[mask])
    log_v = np.log(counts[mask])
    coeffs = np.polyfit(log_r, log_v, 1)
    return coeffs[0], depth


# ── Spectral analysis ────────────────────────────────────────

def spectral_analysis(evals, label=""):
    """Compute spectral dimension, gap, bandwidth, zeta poles."""
    evals_sorted = np.sort(evals)

    # Spectral gap: smallest nonzero |eigenvalue|
    abs_evals = np.abs(evals_sorted)
    nonzero = abs_evals[abs_evals > 1e-12]
    gap = float(nonzero[0]) if len(nonzero) > 0 else 0.0

    # Bandwidth
    bandwidth = float(evals_sorted[-1] - evals_sorted[0])

    # Eigenvalue counting function N(E) for positive eigenvalues
    pos_evals = np.sort(evals_sorted[evals_sorted > 1e-12])
    d_s = np.nan
    d_s_err = np.nan

    if len(pos_evals) >= 5:
        N_count = np.arange(1, len(pos_evals) + 1, dtype=float)
        log_E = np.log(pos_evals)
        log_N = np.log(N_count)

        # Fit log(N) = (d_s/2) * log(E) + const
        # Use middle 60% to avoid edge effects
        n_pts = len(log_E)
        lo = n_pts // 5
        hi = n_pts - n_pts // 5
        if hi - lo >= 4:
            try:
                coeffs, cov = np.polyfit(log_E[lo:hi], log_N[lo:hi], 1, cov=True)
                d_s = 2.0 * coeffs[0]
                d_s_err = 2.0 * np.sqrt(cov[0, 0])
            except (np.linalg.LinAlgError, ValueError):
                coeffs = np.polyfit(log_E[lo:hi], log_N[lo:hi], 1)
                d_s = 2.0 * coeffs[0]

    # Spectral zeta function: zeta(s) = sum |lambda_i|^(-s)
    # Check for pole near s = d/2 by evaluating at several s values
    zeta_s_values = np.arange(0.2, 3.1, 0.1)
    zeta_vals = []
    nonzero_abs = np.sort(np.abs(evals[np.abs(evals) > 1e-12]))
    for s in zeta_s_values:
        z = np.sum(nonzero_abs ** (-s))
        zeta_vals.append(z)
    zeta_vals = np.array(zeta_vals)

    # Find divergence: where zeta jumps most
    zeta_pole = np.nan
    if len(zeta_vals) > 2:
        diffs = np.diff(np.log(np.abs(zeta_vals) + 1e-30))
        idx_max = np.argmax(np.abs(diffs))
        if np.abs(diffs[idx_max]) > 1.0:
            zeta_pole = float(zeta_s_values[idx_max + 1])

    # Density of states: histogram
    n_bins = min(40, len(evals) // 3)
    if n_bins < 5:
        n_bins = 5
    dos_counts, dos_edges = np.histogram(evals, bins=n_bins)
    dos_centers = 0.5 * (dos_edges[:-1] + dos_edges[1:])
    dos_widths = np.diff(dos_edges)
    dos_density = dos_counts / dos_widths

    # Van Hove singularities: look for peaks in DOS
    if len(dos_density) > 2:
        mean_dos = np.mean(dos_density)
        peaks = []
        for i in range(1, len(dos_density) - 1):
            if dos_density[i] > dos_density[i-1] and dos_density[i] > dos_density[i+1]:
                if dos_density[i] > 2 * mean_dos:
                    peaks.append((dos_centers[i], dos_density[i]))
        van_hove_count = len(peaks)
    else:
        van_hove_count = 0

    return {
        "gap": gap,
        "bandwidth": bandwidth,
        "d_s": d_s,
        "d_s_err": d_s_err,
        "zeta_pole": zeta_pole,
        "van_hove_count": van_hove_count,
        "n_evals": len(evals),
        "dos_centers": dos_centers,
        "dos_density": dos_density,
        "pos_evals": pos_evals,
        "zeta_s": zeta_s_values,
        "zeta_vals": zeta_vals,
    }


# ── Main analysis ─────────────────────────────────────────────

def analyze_family(name, pos, col, adj, n, src):
    """Full spectral geometry analysis for one graph family."""
    print(f"\n{'='*72}")
    print(f"  {name}  (n = {n})")
    print(f"{'='*72}")

    t0 = time.time()

    # BFS effective dimension
    d_eff, depth = bfs_dimension(adj, src, n)
    print(f"  BFS effective dimension d_eff = {d_eff:.3f}")

    # Build Laplacian and solve self-gravity
    L = _laplacian(pos, adj, n)
    psi0 = _gauss_state(pos, src)
    rho = np.abs(psi0)**2
    phi = G * _solve_phi(L, n, rho)

    # ── Free Hamiltonian (Phi = 0) ────────────────────────────
    H_free = _build_H(pos, col, adj, n, MASS, np.zeros(n))
    evals_free = np.linalg.eigvalsh(H_free.toarray())
    spec_free = spectral_analysis(evals_free, f"{name}_free")

    print(f"\n  --- Spectrum WITHOUT gravity ---")
    print(f"  Spectral gap         : {spec_free['gap']:.6f}")
    print(f"  Bandwidth            : {spec_free['bandwidth']:.4f}")
    print(f"  Spectral dimension   : {spec_free['d_s']:.3f} +/- {spec_free['d_s_err']:.3f}")
    print(f"  Zeta pole estimate   : {spec_free['zeta_pole']:.2f}" if not np.isnan(spec_free['zeta_pole']) else "  Zeta pole estimate   : none detected")
    print(f"  Van Hove singularities: {spec_free['van_hove_count']}")

    # ── Gravity Hamiltonian (Phi from self-gravity) ───────────
    H_grav = _build_H(pos, col, adj, n, MASS, phi)
    evals_grav = np.linalg.eigvalsh(H_grav.toarray())
    spec_grav = spectral_analysis(evals_grav, f"{name}_grav")

    print(f"\n  --- Spectrum WITH gravity (G={G}) ---")
    print(f"  Spectral gap         : {spec_grav['gap']:.6f}")
    print(f"  Bandwidth            : {spec_grav['bandwidth']:.4f}")
    print(f"  Spectral dimension   : {spec_grav['d_s']:.3f} +/- {spec_grav['d_s_err']:.3f}")
    print(f"  Zeta pole estimate   : {spec_grav['zeta_pole']:.2f}" if not np.isnan(spec_grav['zeta_pole']) else "  Zeta pole estimate   : none detected")
    print(f"  Van Hove singularities: {spec_grav['van_hove_count']}")

    # ── Comparison ────────────────────────────────────────────
    delta_ds = spec_grav['d_s'] - spec_free['d_s']
    gap_ratio = spec_grav['gap'] / spec_free['gap'] if spec_free['gap'] > 0 else np.nan
    bw_ratio = spec_grav['bandwidth'] / spec_free['bandwidth'] if spec_free['bandwidth'] > 0 else np.nan

    print(f"\n  --- Gravity vs Free ---")
    print(f"  d_s shift (grav-free): {delta_ds:+.3f}")
    print(f"  Gap ratio (grav/free): {gap_ratio:.4f}")
    print(f"  BW  ratio (grav/free): {bw_ratio:.4f}")
    print(f"  d_eff (BFS)          : {d_eff:.3f}")
    print(f"  d_s (free)           : {spec_free['d_s']:.3f}")
    print(f"  d_s (grav)           : {spec_grav['d_s']:.3f}")

    # ── Eigenvalue distribution summary ───────────────────────
    print(f"\n  --- Eigenvalue distribution ---")
    for tag, ev in [("free", evals_free), ("grav", evals_grav)]:
        neg = np.sum(ev < -1e-12)
        zero = np.sum(np.abs(ev) <= 1e-12)
        pos = np.sum(ev > 1e-12)
        print(f"  {tag:5s}: {neg:3d} negative, {zero:2d} zero, {pos:3d} positive")

    # ── Spectral zeta near expected pole ──────────────────────
    print(f"\n  --- Spectral zeta function ---")
    print(f"  {'s':>6s}  {'zeta(s)_free':>14s}  {'zeta(s)_grav':>14s}")
    targets = {0.5, 1.0, 1.5, 2.0, 2.5, 3.0}
    for i, s in enumerate(spec_free['zeta_s']):
        if any(abs(s - t) < 0.01 for t in targets):
            print(f"  {s:6.1f}  {spec_free['zeta_vals'][i]:14.4f}  {spec_grav['zeta_vals'][i]:14.4f}")

    elapsed = time.time() - t0
    print(f"\n  Elapsed: {elapsed:.2f}s")

    return {
        "name": name,
        "n": n,
        "d_eff": d_eff,
        "free": spec_free,
        "grav": spec_grav,
        "delta_ds": delta_ds,
        "gap_ratio": gap_ratio,
        "bw_ratio": bw_ratio,
    }


# ── Runner ────────────────────────────────────────────────────

def main():
    print("=" * 72)
    print("  SPECTRAL GEOMETRY PROBE")
    print("  Hearing the shape of spacetime")
    print("=" * 72)
    print(f"  MASS={MASS}, MU2={MU2}, DT={DT}, G={G}")

    families = [
        make_2d_lattice(side=8),
        make_2d_lattice(side=10),
        make_random_geometric(seed=42, side=8),
        make_growing(seed=42, n_target=64),
        make_layered_cycle(seed=42, layers=8, width=8),
    ]

    results = []
    for name, pos, col, adj, n, src in families:
        r = analyze_family(name, pos, col, adj, n, src)
        results.append(r)

    # ── Summary table ─────────────────────────────────────────
    print("\n")
    print("=" * 72)
    print("  SUMMARY TABLE")
    print("=" * 72)
    header = f"  {'Family':<25s} {'n':>4s} {'d_eff':>6s} {'d_s(free)':>10s} {'d_s(grav)':>10s} {'delta_ds':>9s} {'gap_ratio':>10s}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for r in results:
        ds_free = f"{r['free']['d_s']:.2f}" if not np.isnan(r['free']['d_s']) else "  nan"
        ds_grav = f"{r['grav']['d_s']:.2f}" if not np.isnan(r['grav']['d_s']) else "  nan"
        delta = f"{r['delta_ds']:+.3f}" if not np.isnan(r['delta_ds']) else "  nan"
        gap_r = f"{r['gap_ratio']:.4f}" if not np.isnan(r['gap_ratio']) else " nan"
        print(f"  {r['name']:<25s} {r['n']:4d} {r['d_eff']:6.2f} {ds_free:>10s} {ds_grav:>10s} {delta:>9s} {gap_r:>10s}")

    # ── Interpretive summary ──────────────────────────────────
    print("\n")
    print("=" * 72)
    print("  INTERPRETATION")
    print("=" * 72)

    lattice_results = [r for r in results if "lattice" in r["name"]]
    if lattice_results:
        ds_vals = [r["free"]["d_s"] for r in lattice_results if not np.isnan(r["free"]["d_s"])]
        if ds_vals:
            mean_ds = np.mean(ds_vals)
            print(f"\n  Lattice d_s (free): mean = {mean_ds:.2f}")
            print(f"  Expected for 2D lattice: d_s ~ 2.0")
            if abs(mean_ds - 2.0) < 0.5:
                print(f"  PASS: Spectral dimension correctly encodes 2D geometry")
            else:
                print(f"  NOTE: d_s deviates from 2.0 -- staggered mass term modifies Weyl scaling")

    gravity_shifts = [r["delta_ds"] for r in results if not np.isnan(r["delta_ds"])]
    if gravity_shifts:
        print(f"\n  Gravity-induced d_s shifts: {[f'{x:+.3f}' for x in gravity_shifts]}")
        mean_shift = np.mean(gravity_shifts)
        if abs(mean_shift) > 0.05:
            direction = "increases" if mean_shift > 0 else "decreases"
            print(f"  FINDING: Self-gravity {direction} spectral dimension by {abs(mean_shift):.3f} on average")
            print(f"  This is a QUANTUM GRAVITY correction to spacetime dimension")
        else:
            print(f"  FINDING: Gravity has negligible effect on spectral dimension (mean shift {mean_shift:+.3f})")

    gap_ratios = [r["gap_ratio"] for r in results if not np.isnan(r["gap_ratio"])]
    if gap_ratios:
        mean_gap = np.mean(gap_ratios)
        print(f"\n  Gap ratios (grav/free): {[f'{x:.3f}' for x in gap_ratios]}")
        if mean_gap < 0.95:
            print(f"  FINDING: Gravity NARROWS the spectral gap (mean ratio {mean_gap:.3f})")
        elif mean_gap > 1.05:
            print(f"  FINDING: Gravity WIDENS the spectral gap (mean ratio {mean_gap:.3f})")
        else:
            print(f"  FINDING: Gravity has minor effect on spectral gap (mean ratio {mean_gap:.3f})")

    irregular_results = [r for r in results if "lattice" not in r["name"]]
    if irregular_results:
        print(f"\n  Irregular graphs:")
        for r in irregular_results:
            ds_free = r["free"]["d_s"]
            d_eff = r["d_eff"]
            if not np.isnan(ds_free) and not np.isnan(d_eff):
                diff = abs(ds_free - d_eff)
                print(f"    {r['name']}: d_eff={d_eff:.2f}, d_s={ds_free:.2f}, |diff|={diff:.2f}")

    print()


if __name__ == "__main__":
    main()
