#!/usr/bin/env python3
"""Spectral dimension flow: UV to IR, analogous to CDT.

Does the spectral dimension d_s flow from ~2 (UV/free) to ~3-4 (IR/gravitating)
as a function of energy cutoff?

In Causal Dynamical Triangulations (Ambjorn-Jurkiewicz-Loll), d_s flows from
~2 in the UV to ~4 in the IR. The spectral geometry probe found d_s = 1.90
(free) and d_s = 2.89-4.09 (self-gravitating) on 2D staggered lattices.

TWO PROBES:
  1. Weyl counting: d_s(E_max) from eigenvalue counting N(E) ~ E^(d_s/2)
  2. Diffusion return probability: P(t) ~ t^(-d_s/2), short t = UV, long t = IR

GRAPH FAMILIES:
  - 2D periodic lattice (side = 8, 10, 12)
  - Random geometric (side = 8)
  - Growing graph (n = 64)
"""

from __future__ import annotations

import math
import random
import time
from collections import deque

import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve

# ── Parameters ────────────────────────────────────────────────
MASS = 0.30
MU2 = 0.22
DT = 0.12
G = 10.0
N_STEPS = 30

# ── Graph utilities ───────────────────────────────────────────

def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


# ── Graph families ────────────────────────────────────────────

def make_2d_periodic_lattice(side=10):
    """2D periodic (torus) lattice with checkerboard coloring."""
    n = side * side
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
    # Periodic boundary conditions
    for x in range(side):
        for y in range(side):
            a = index[(x, y)]
            for dx, dy in ((1, 0), (0, 1)):
                nx_ = (x + dx) % side
                ny_ = (y + dy) % side
                b = index[(nx_, ny_)]
                if a != b:
                    _ae(adj, a, b)
    adj_l = {k: list(v) for k, v in adj.items()}
    return f"2D_periodic_{side}x{side}", pos, col, adj_l, n


def make_random_geometric(seed=42, side=8):
    """Random geometric graph with jittered positions."""
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
    return "random_geometric_8x8", pos, col, adj_l, n


def make_growing(seed=42, n_target=64):
    """Growing graph with alternating colors."""
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
    return "growing_n64", pos, col, adj_l, len(pos)


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
    """Build staggered Hamiltonian with parity coupling."""
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


def _gauss_state(pos, n, sigma=1.15):
    """Gaussian wavepacket centered on the graph centroid."""
    center = np.mean(pos, axis=0)
    rel = pos - center
    psi = np.exp(-0.5 * np.sum(rel**2, axis=1) / sigma**2).astype(complex)
    return psi / np.linalg.norm(psi)


def evolve_cn(H, psi, dt, n_steps):
    """Crank-Nicolson time evolution."""
    I = speye(H.shape[0], format='csr')
    A = (I + 0.5j * dt * H).tocsc()
    B = I - 0.5j * dt * H
    for _ in range(n_steps):
        rhs = B @ psi
        psi = spsolve(A, rhs)
        psi /= np.linalg.norm(psi)
    return psi


def compute_spectra(pos, col, adj, n):
    """Compute eigenspectra for free and gravitating Hamiltonians."""
    L = _laplacian(pos, adj, n)
    psi0 = _gauss_state(pos, n)

    # Free Hamiltonian
    H_free = _build_H(pos, col, adj, n, MASS, np.zeros(n))
    evals_free = np.linalg.eigvalsh(H_free.toarray())

    # Gravitating: evolve with CN, compute self-consistent phi
    psi = psi0.copy()
    for step in range(N_STEPS):
        rho = np.abs(psi)**2
        phi = G * _solve_phi(L, n, rho)
        H_grav = _build_H(pos, col, adj, n, MASS, phi)
        psi = evolve_cn(H_grav, psi, DT, 1)

    # Final spectrum with converged phi
    rho = np.abs(psi)**2
    phi = G * _solve_phi(L, n, rho)
    H_grav = _build_H(pos, col, adj, n, MASS, phi)
    evals_grav = np.linalg.eigvalsh(H_grav.toarray())

    return evals_free, evals_grav, H_free, H_grav


# ── Probe 1: Weyl counting d_s(E_max) ────────────────────────

def weyl_dimension_flow(evals, window=10):
    """Compute d_s(E_max) using sliding-window Weyl's law fit.

    For eigenvalues sorted as E_1 < E_2 < ... < E_N/2 (positive only),
    N(E) ~ E^(d_s/2). Fit log(N) vs log(E) using a sliding window
    of the last `window` eigenvalues below each E_max.

    Returns (E_max_values, d_s_values).
    """
    pos_evals = np.sort(evals[evals > 1e-12])
    if len(pos_evals) < window + 2:
        return np.array([]), np.array([])

    N_count = np.arange(1, len(pos_evals) + 1, dtype=float)
    log_E = np.log(pos_evals)
    log_N = np.log(N_count)

    E_max_vals = []
    ds_vals = []

    for i in range(window, len(pos_evals)):
        lo = i - window
        hi = i + 1
        # Need at least 5 distinct values in the window
        if len(set(log_E[lo:hi])) < 4:
            continue
        try:
            coeffs = np.polyfit(log_E[lo:hi], log_N[lo:hi], 1)
            d_s = 2.0 * coeffs[0]
            E_max_vals.append(pos_evals[i])
            ds_vals.append(d_s)
        except (np.linalg.LinAlgError, ValueError):
            continue

    return np.array(E_max_vals), np.array(ds_vals)


# ── Probe 2: Diffusion return probability d_s(t) ─────────────

def diffusion_dimension_flow(evals, n, t_min=0.01, t_max=100.0, n_t=200):
    """Compute d_s(t) from the return probability P(t) = (1/n) sum exp(-t E_i^2).

    d_s(t) = -2 * d(log P) / d(log t)

    Short t = UV (high energy modes contribute), long t = IR (low energy modes).

    Returns (t_values, d_s_values, P_values).
    """
    E2 = evals**2
    t_vals = np.logspace(np.log10(t_min), np.log10(t_max), n_t)

    # P(t) = (1/n) * sum_i exp(-t * E_i^2)
    P_vals = np.array([np.mean(np.exp(-t * E2)) for t in t_vals])

    # Avoid log(0)
    mask = P_vals > 1e-30
    log_t = np.log(t_vals[mask])
    log_P = np.log(P_vals[mask])

    # d_s(t) = -2 * d(log P)/d(log t) via finite differences
    if len(log_t) < 5:
        return t_vals, np.full(len(t_vals), np.nan), P_vals

    d_log_P = np.gradient(log_P, log_t)
    d_s = -2.0 * d_log_P

    # Embed back into full array
    d_s_full = np.full(len(t_vals), np.nan)
    d_s_full[mask] = d_s

    return t_vals, d_s_full, P_vals


# ── Analysis for one graph family ─────────────────────────────

def analyze_flow(name, pos, col, adj, n):
    """Full dimensional flow analysis for one graph family."""
    print(f"\n{'='*72}")
    print(f"  {name}  (n = {n})")
    print(f"{'='*72}")

    t0 = time.time()

    evals_free, evals_grav, H_free, H_grav = compute_spectra(pos, col, adj, n)

    # ── Probe 1: Weyl counting ────────────────────────────────
    print(f"\n  --- Probe 1: Weyl counting d_s(E_max) ---")

    for tag, ev in [("free", evals_free), ("grav", evals_grav)]:
        E_max, ds = weyl_dimension_flow(ev, window=10)
        if len(ds) == 0:
            print(f"  {tag}: insufficient eigenvalues for Weyl fit")
            continue

        # Report at several energy scales
        n_pts = len(E_max)
        indices = [0, n_pts // 4, n_pts // 2, 3 * n_pts // 4, n_pts - 1]
        indices = sorted(set(min(i, n_pts - 1) for i in indices))

        print(f"\n  {tag} Weyl flow (window=10):")
        print(f"    {'E_max':>10s}  {'d_s':>8s}  {'regime':>8s}")
        for i in indices:
            regime = "IR" if i < n_pts // 3 else ("mid" if i < 2 * n_pts // 3 else "UV")
            print(f"    {E_max[i]:10.4f}  {ds[i]:8.3f}  {regime:>8s}")

        # Summary: IR vs UV averages
        n_third = max(1, n_pts // 3)
        ds_ir = np.mean(ds[:n_third])
        ds_uv = np.mean(ds[-n_third:])
        ds_mid = np.mean(ds[n_third:2*n_third])
        print(f"    IR  avg d_s = {ds_ir:.3f}  (lowest {n_third} E_max values)")
        print(f"    mid avg d_s = {ds_mid:.3f}")
        print(f"    UV  avg d_s = {ds_uv:.3f}  (highest {n_third} E_max values)")

        flow_direction = "UV->IR increase" if ds_ir > ds_uv else "UV->IR decrease"
        delta = ds_ir - ds_uv
        print(f"    Flow: {flow_direction} (delta = {delta:+.3f})")

    # ── Probe 2: Diffusion return probability ─────────────────
    print(f"\n  --- Probe 2: Diffusion d_s(t) ---")

    for tag, ev in [("free", evals_free), ("grav", evals_grav)]:
        t_vals, ds_t, P_vals = diffusion_dimension_flow(ev, n)

        # Report at several diffusion times
        # Short t = UV, long t = IR
        target_ts = [0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0]
        print(f"\n  {tag} diffusion flow:")
        print(f"    {'t':>10s}  {'d_s':>8s}  {'P(t)':>12s}  {'regime':>8s}")

        for t_target in target_ts:
            idx = np.argmin(np.abs(t_vals - t_target))
            if not np.isnan(ds_t[idx]):
                regime = "UV" if t_target < 0.1 else ("mid" if t_target < 5.0 else "IR")
                print(f"    {t_vals[idx]:10.4f}  {ds_t[idx]:8.3f}  {P_vals[idx]:12.6e}  {regime:>8s}")

        # Summary: UV (t < 0.1) vs IR (t > 5)
        uv_mask = (t_vals < 0.1) & (~np.isnan(ds_t))
        ir_mask = (t_vals > 5.0) & (~np.isnan(ds_t))
        mid_mask = (t_vals >= 0.1) & (t_vals <= 5.0) & (~np.isnan(ds_t))

        if np.any(uv_mask):
            ds_uv_diff = np.mean(ds_t[uv_mask])
            print(f"    UV  avg d_s (t<0.1)  = {ds_uv_diff:.3f}")
        if np.any(mid_mask):
            ds_mid_diff = np.mean(ds_t[mid_mask])
            print(f"    mid avg d_s (0.1-5)  = {ds_mid_diff:.3f}")
        if np.any(ir_mask):
            ds_ir_diff = np.mean(ds_t[ir_mask])
            print(f"    IR  avg d_s (t>5)    = {ds_ir_diff:.3f}")

        if np.any(uv_mask) and np.any(ir_mask):
            delta_diff = np.mean(ds_t[ir_mask]) - np.mean(ds_t[uv_mask])
            flow = "UV->IR increase" if delta_diff > 0 else "UV->IR decrease"
            print(f"    Flow: {flow} (delta = {delta_diff:+.3f})")

    # ── Eigenvalue summary ────────────────────────────────────
    print(f"\n  --- Eigenvalue summary ---")
    for tag, ev in [("free", evals_free), ("grav", evals_grav)]:
        pos_ev = np.sort(ev[ev > 1e-12])
        neg_ev = np.sort(ev[ev < -1e-12])
        print(f"  {tag}: {len(neg_ev)} neg, {np.sum(np.abs(ev) <= 1e-12)} zero, "
              f"{len(pos_ev)} pos, range [{ev.min():.4f}, {ev.max():.4f}]")

    elapsed = time.time() - t0
    print(f"\n  Elapsed: {elapsed:.1f}s")

    return {
        "name": name,
        "n": n,
        "evals_free": evals_free,
        "evals_grav": evals_grav,
    }


# ── Main ──────────────────────────────────────────────────────

def main():
    print("=" * 72)
    print("  SPECTRAL DIMENSION FLOW: UV to IR")
    print("  Analogy with CDT (Ambjorn-Jurkiewicz-Loll)")
    print("=" * 72)
    print(f"  MASS={MASS}, MU2={MU2}, DT={DT}, G={G}, N_STEPS={N_STEPS}")
    print(f"  CDT prediction: d_s flows from ~2 (UV) to ~4 (IR)")
    print()

    # ── Build graph families ──────────────────────────────────
    families = [
        make_2d_periodic_lattice(side=8),
        make_2d_periodic_lattice(side=10),
        make_2d_periodic_lattice(side=12),
        make_random_geometric(seed=42, side=8),
        make_growing(seed=42, n_target=64),
    ]

    all_results = []
    for name, pos, col, adj, n in families:
        r = analyze_flow(name, pos, col, adj, n)
        all_results.append(r)

    # ── Cross-family summary ──────────────────────────────────
    print(f"\n\n{'='*72}")
    print("  CROSS-FAMILY SUMMARY: WEYL COUNTING")
    print(f"{'='*72}")
    print()

    header = (f"  {'Family':<25s} {'n':>4s} | "
              f"{'d_s IR':>7s} {'d_s mid':>8s} {'d_s UV':>7s} {'delta':>7s} | "
              f"{'d_s IR':>7s} {'d_s mid':>8s} {'d_s UV':>7s} {'delta':>7s}")
    print(f"  {'':25s} {'':>4s} | {'--- Free ---':^31s} | {'--- Grav ---':^31s}")
    print(header)
    print("  " + "-" * (len(header) - 2))

    for r in all_results:
        row_parts = [f"  {r['name']:<25s} {r['n']:4d} |"]
        for ev in [r['evals_free'], r['evals_grav']]:
            E_max, ds = weyl_dimension_flow(ev, window=10)
            if len(ds) > 0:
                n_third = max(1, len(ds) // 3)
                ir = np.mean(ds[:n_third])
                mid = np.mean(ds[n_third:2*n_third])
                uv = np.mean(ds[-n_third:])
                delta = ir - uv
                row_parts.append(f" {ir:7.3f} {mid:8.3f} {uv:7.3f} {delta:+7.3f} |")
            else:
                row_parts.append(f" {'N/A':>7s} {'N/A':>8s} {'N/A':>7s} {'N/A':>7s} |")
        print("".join(row_parts))

    # ── Cross-family summary: diffusion ───────────────────────
    print(f"\n{'='*72}")
    print("  CROSS-FAMILY SUMMARY: DIFFUSION RETURN PROBABILITY")
    print(f"{'='*72}")
    print()

    print(f"  {'':25s} {'':>4s} | {'--- Free ---':^31s} | {'--- Grav ---':^31s}")
    print(header)
    print("  " + "-" * (len(header) - 2))

    for r in all_results:
        row_parts = [f"  {r['name']:<25s} {r['n']:4d} |"]
        for ev in [r['evals_free'], r['evals_grav']]:
            t_vals, ds_t, _ = diffusion_dimension_flow(ev, r['n'])
            uv_mask = (t_vals < 0.1) & (~np.isnan(ds_t))
            ir_mask = (t_vals > 5.0) & (~np.isnan(ds_t))
            mid_mask = (t_vals >= 0.1) & (t_vals <= 5.0) & (~np.isnan(ds_t))

            parts = []
            for m in [ir_mask, mid_mask, uv_mask]:
                if np.any(m):
                    parts.append(np.mean(ds_t[m]))
                else:
                    parts.append(np.nan)

            if not any(np.isnan(p) for p in parts):
                delta = parts[0] - parts[2]
                row_parts.append(f" {parts[0]:7.3f} {parts[1]:8.3f} {parts[2]:7.3f} {delta:+7.3f} |")
            else:
                row_parts.append(f" {'N/A':>7s} {'N/A':>8s} {'N/A':>7s} {'N/A':>7s} |")
        print("".join(row_parts))

    # ── CDT comparison ────────────────────────────────────────
    print(f"\n{'='*72}")
    print("  CDT COMPARISON AND INTERPRETATION")
    print(f"{'='*72}")
    print()

    # Collect flow data for lattice families
    lattice_results = [r for r in all_results if "periodic" in r["name"]]

    print("  CDT benchmark (Ambjorn-Jurkiewicz-Loll 2005):")
    print("    UV: d_s -> 2.0")
    print("    IR: d_s -> 4.0 (in 3+1D)")
    print("    Flow is monotonic from UV to IR")
    print()

    # Check if our model shows the same pattern
    weyl_flows = []
    diff_flows = []

    for r in lattice_results:
        # Weyl flow for gravitating
        E_max, ds = weyl_dimension_flow(r['evals_grav'], window=10)
        if len(ds) > 0:
            n_third = max(1, len(ds) // 3)
            weyl_flows.append({
                "name": r["name"],
                "ir": np.mean(ds[:n_third]),
                "uv": np.mean(ds[-n_third:]),
            })

        # Diffusion flow for gravitating
        t_vals, ds_t, _ = diffusion_dimension_flow(r['evals_grav'], r['n'])
        uv_mask = (t_vals < 0.1) & (~np.isnan(ds_t))
        ir_mask = (t_vals > 5.0) & (~np.isnan(ds_t))
        if np.any(uv_mask) and np.any(ir_mask):
            diff_flows.append({
                "name": r["name"],
                "ir": np.mean(ds_t[ir_mask]),
                "uv": np.mean(ds_t[uv_mask]),
            })

    print("  Our model (gravitating, periodic lattices):")
    print()

    if weyl_flows:
        print("  Weyl counting probe:")
        for f in weyl_flows:
            delta = f["ir"] - f["uv"]
            cdt_like = "YES" if delta > 0.1 else "NO" if delta < -0.1 else "MARGINAL"
            print(f"    {f['name']}: UV={f['uv']:.3f}, IR={f['ir']:.3f}, "
                  f"delta={delta:+.3f}, CDT-like={cdt_like}")

    if diff_flows:
        print()
        print("  Diffusion probe:")
        for f in diff_flows:
            delta = f["ir"] - f["uv"]
            cdt_like = "YES" if delta > 0.1 else "NO" if delta < -0.1 else "MARGINAL"
            print(f"    {f['name']}: UV={f['uv']:.3f}, IR={f['ir']:.3f}, "
                  f"delta={delta:+.3f}, CDT-like={cdt_like}")

    # ── Gravity effect on flow ────────────────────────────────
    print(f"\n{'='*72}")
    print("  GRAVITY EFFECT ON DIMENSIONAL FLOW")
    print(f"{'='*72}")
    print()
    print("  Does gravity change the flow pattern?")
    print()

    for r in lattice_results:
        print(f"  {r['name']}:")

        for probe_name, probe_fn in [("Weyl", lambda ev: weyl_dimension_flow(ev, window=10)),
                                      ("Diffusion", None)]:
            if probe_name == "Weyl":
                for tag, ev in [("free", r['evals_free']), ("grav", r['evals_grav'])]:
                    E_max, ds = probe_fn(ev)
                    if len(ds) > 0:
                        n_third = max(1, len(ds) // 3)
                        ir = np.mean(ds[:n_third])
                        uv = np.mean(ds[-n_third:])
                        print(f"    {probe_name} {tag}: UV={uv:.3f}, IR={ir:.3f}, delta={ir-uv:+.3f}")
            else:
                for tag, ev in [("free", r['evals_free']), ("grav", r['evals_grav'])]:
                    t_vals, ds_t, _ = diffusion_dimension_flow(ev, r['n'])
                    uv_m = (t_vals < 0.1) & (~np.isnan(ds_t))
                    ir_m = (t_vals > 5.0) & (~np.isnan(ds_t))
                    if np.any(uv_m) and np.any(ir_m):
                        uv = np.mean(ds_t[uv_m])
                        ir = np.mean(ds_t[ir_m])
                        print(f"    {probe_name} {tag}: UV={uv:.3f}, IR={ir:.3f}, delta={ir-uv:+.3f}")
        print()

    # ── Universality check ────────────────────────────────────
    print(f"{'='*72}")
    print("  UNIVERSALITY: Does the flow persist across graph families?")
    print(f"{'='*72}")
    print()

    all_weyl_deltas_free = []
    all_weyl_deltas_grav = []
    all_diff_deltas_free = []
    all_diff_deltas_grav = []

    for r in all_results:
        for tag, ev, weyl_list, diff_list in [
            ("free", r['evals_free'], all_weyl_deltas_free, all_diff_deltas_free),
            ("grav", r['evals_grav'], all_weyl_deltas_grav, all_diff_deltas_grav),
        ]:
            E_max, ds = weyl_dimension_flow(ev, window=10)
            if len(ds) > 5:
                n_third = max(1, len(ds) // 3)
                delta = np.mean(ds[:n_third]) - np.mean(ds[-n_third:])
                weyl_list.append((r['name'], delta))

            t_vals, ds_t, _ = diffusion_dimension_flow(ev, r['n'])
            uv_m = (t_vals < 0.1) & (~np.isnan(ds_t))
            ir_m = (t_vals > 5.0) & (~np.isnan(ds_t))
            if np.any(uv_m) and np.any(ir_m):
                delta = np.mean(ds_t[ir_m]) - np.mean(ds_t[uv_m])
                diff_list.append((r['name'], delta))

    print("  Weyl counting (IR - UV):")
    print(f"    {'Family':<25s} {'free':>8s} {'grav':>8s}")
    for (nf, df), (ng, dg) in zip(all_weyl_deltas_free, all_weyl_deltas_grav):
        print(f"    {nf:<25s} {df:+8.3f} {dg:+8.3f}")

    if all_weyl_deltas_grav:
        deltas = [d for _, d in all_weyl_deltas_grav]
        n_positive = sum(1 for d in deltas if d > 0.1)
        print(f"    CDT-like (IR > UV) in grav: {n_positive}/{len(deltas)}")

    print()
    print("  Diffusion (IR - UV):")
    print(f"    {'Family':<25s} {'free':>8s} {'grav':>8s}")
    for i in range(min(len(all_diff_deltas_free), len(all_diff_deltas_grav))):
        nf, df = all_diff_deltas_free[i]
        ng, dg = all_diff_deltas_grav[i]
        print(f"    {nf:<25s} {df:+8.3f} {dg:+8.3f}")

    if all_diff_deltas_grav:
        deltas = [d for _, d in all_diff_deltas_grav]
        n_positive = sum(1 for d in deltas if d > 0.1)
        print(f"    CDT-like (IR > UV) in grav: {n_positive}/{len(deltas)}")

    # ── Final verdict ─────────────────────────────────────────
    print(f"\n{'='*72}")
    print("  VERDICT")
    print(f"{'='*72}")
    print()

    # Count CDT-like flows across all probes and families
    all_grav_deltas = ([d for _, d in all_weyl_deltas_grav] +
                       [d for _, d in all_diff_deltas_grav])
    all_free_deltas = ([d for _, d in all_weyl_deltas_free] +
                       [d for _, d in all_diff_deltas_free])

    if all_grav_deltas:
        n_cdt_grav = sum(1 for d in all_grav_deltas if d > 0.1)
        n_anti_grav = sum(1 for d in all_grav_deltas if d < -0.1)
        n_flat_grav = len(all_grav_deltas) - n_cdt_grav - n_anti_grav
        print(f"  Gravitating: {n_cdt_grav} CDT-like, {n_anti_grav} anti-CDT, "
              f"{n_flat_grav} flat  (out of {len(all_grav_deltas)} tests)")

    if all_free_deltas:
        n_cdt_free = sum(1 for d in all_free_deltas if d > 0.1)
        n_anti_free = sum(1 for d in all_free_deltas if d < -0.1)
        n_flat_free = len(all_free_deltas) - n_cdt_free - n_anti_free
        print(f"  Free:        {n_cdt_free} CDT-like, {n_anti_free} anti-CDT, "
              f"{n_flat_free} flat  (out of {len(all_free_deltas)} tests)")

    if all_grav_deltas and all_free_deltas:
        mean_grav = np.mean(all_grav_deltas)
        mean_free = np.mean(all_free_deltas)
        print()
        print(f"  Mean IR-UV shift (grav): {mean_grav:+.3f}")
        print(f"  Mean IR-UV shift (free): {mean_free:+.3f}")

        if mean_grav > 0.1 and mean_grav > mean_free + 0.1:
            print()
            print("  FINDING: Gravity ENHANCES the CDT-like flow (d_s increases from UV to IR).")
            print("  This connects the staggered-lattice model to CDT dimensional reduction.")
        elif mean_grav > 0.1:
            print()
            print("  FINDING: CDT-like flow exists but is similar for free and gravitating.")
            print("  The flow may be a lattice artifact rather than a gravity effect.")
        elif mean_grav < -0.1:
            print()
            print("  FINDING: Anti-CDT flow (d_s decreases from UV to IR).")
            print("  This is opposite to the CDT prediction.")
        else:
            print()
            print("  FINDING: No significant dimensional flow detected.")

    print()


if __name__ == "__main__":
    main()
