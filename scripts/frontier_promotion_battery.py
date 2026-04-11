#!/usr/bin/env python3
"""
Frontier Promotion Battery
===========================
Five critical tests to PROMOTE exploratory results or FIX known negatives.

Test 1 — CDT Flow Size Scaling: sigma_*(L) constant => promote, ~ L^2 => kill
Test 2 — Multifractal Size Scaling: D_2(L) constant => promote, -> 0 or 1 => kill
Test 3 — Memory with mu=0: fix the large-N memory vanishing
Test 4 — Eigenvalue Statistics: Poisson => gravitational, Wigner-Dyson => generic
Test 5 — Entanglement Crossover Finite-Size Scaling: collapse => promote

Physics: MASS=0.30, MU2=0.22 (except Test 3: mu=0), DT=0.12, parity coupling.
"""

from __future__ import annotations

import math
import random
import time
import warnings

import numpy as np
from scipy.sparse import lil_matrix, eye as speye, csc_matrix
from scipy.sparse.linalg import spsolve
from scipy.optimize import curve_fit
from scipy.stats import linregress, ks_2samp
from collections import deque

# ============================================================================
# Global physics parameters
# ============================================================================
MASS = 0.30
MU2 = 0.22
DT = 0.12
G_DEFAULT = 10.0
N_STEPS = 30
SEED = 42


# ============================================================================
# Graph construction (shared)
# ============================================================================

def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_staggered_lattice(seed, side):
    """2D staggered lattice with bipartite coloring and jittered positions."""
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
    return pos, col, adj_l, n, src


def build_periodic_lattice(side):
    """2D periodic lattice for entanglement tests."""
    n = side * side
    pos = np.zeros((n, 2))
    adj = {i: [] for i in range(n)}
    col = np.zeros(n, dtype=int)
    for ix in range(side):
        for iy in range(side):
            idx = ix * side + iy
            pos[idx] = (ix, iy)
            col[idx] = (ix + iy) % 2
            for dix, diy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                jx = (ix + dix) % side
                jy = (iy + diy) % side
                jdx = jx * side + jy
                adj[idx].append(jdx)
    return n, pos, adj, col


# ============================================================================
# Physics operators (shared)
# ============================================================================

def graph_laplacian(pos, adj, n):
    """Graph Laplacian with distance-weighted edges."""
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


def solve_phi(L, n, rho, mu2=MU2):
    """Solve screened Poisson: (L + mu^2 I) phi = rho."""
    if np.allclose(rho, 0):
        return np.zeros(n)
    A = (L + mu2 * speye(n, format='csr')).tocsc()
    return spsolve(A, rho)


def build_hamiltonian(pos, col, adj, n, mass, phi):
    """Staggered Hamiltonian with parity-coupled gravitational potential."""
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((mass + phi) * par)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            hop = -0.5j * w
            H[i, j] += hop
            H[j, i] += np.conj(hop)
    return H.tocsr()


def cn_step(H, n, psi, dt=DT):
    """Crank-Nicolson time step."""
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def gauss_state(pos, src, sigma=1.15):
    center = pos[src]
    rel = pos - center
    psi = np.exp(-0.5 * np.sum(rel**2, axis=1) / sigma**2).astype(complex)
    return psi / np.linalg.norm(psi)


def evolve_self_gravity(pos, col, adj, n, src, G=G_DEFAULT, mu2=MU2):
    """Evolve Gaussian under self-gravity. Return (psi_final, H_final, phi_final)."""
    L = graph_laplacian(pos, adj, n)
    psi = gauss_state(pos, src)
    phi = np.zeros(n)
    H = None
    for _ in range(N_STEPS):
        rho = np.abs(psi)**2
        phi = solve_phi(L, n, G * rho, mu2=mu2)
        H = build_hamiltonian(pos, col, adj, n, MASS, phi)
        psi = cn_step(H, n, psi)
    return psi, H, phi


def gravity_laplacian(pos, adj, n, phi):
    """Gravity-modified Laplacian: edges weighted by exp(gamma * phi_avg)."""
    gamma = 1.0
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w0 = 1.0 / max(d, 0.5)
            phi_avg = 0.5 * (phi[i] + phi[j])
            w = w0 * np.exp(gamma * phi_avg)
            L[i, j] -= w
            L[j, i] -= w
            L[i, i] += w
            L[j, j] += w
    return L.tocsr()


# ============================================================================
# TEST 1: CDT Flow Size Scaling
# ============================================================================

def cdt_sigmoid(log_sigma, d_UV, d_IR, log_sigma_star, alpha):
    sigma = np.exp(log_sigma)
    sigma_star = np.exp(log_sigma_star)
    ratio = (sigma / sigma_star)**alpha
    return d_UV + (d_IR - d_UV) * ratio / (1.0 + ratio)


def spectral_dimension_flow(L_dense, sigmas):
    """d_s(sigma) from Laplacian eigenvalues."""
    evals = np.linalg.eigvalsh(L_dense)
    evals = np.maximum(evals, 0.0)
    ds = np.zeros(len(sigmas))
    for idx, s in enumerate(sigmas):
        boltz = np.exp(-s * evals)
        P = np.mean(boltz)
        dP = np.mean(-evals * boltz)
        ds[idx] = -2.0 * s * dP / P if P > 1e-30 else np.nan
    return ds, evals


def fit_sigmoid(sigmas, ds_values):
    """Fit d_s(sigma) to CDT sigmoid. Return (d_UV, d_IR, sigma_star, alpha, R2) or None."""
    valid = np.isfinite(ds_values) & (ds_values > 0)
    if np.sum(valid) < 8:
        return None
    ds_v = ds_values[valid]
    sig_v = sigmas[valid]
    peak_idx = np.argmax(ds_v)
    end_idx = min(peak_idx + 5, len(ds_v))
    ds_fit = ds_v[:end_idx]
    sig_fit = sig_v[:end_idx]
    if len(ds_fit) < 6:
        return None
    log_sigma = np.log(sig_fit)
    peak_ds = np.max(ds_fit)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            popt, _ = curve_fit(
                cdt_sigmoid, log_sigma, ds_fit,
                p0=[ds_fit[0] + 0.01, peak_ds, np.log(sig_fit[peak_idx // 2]), 1.0],
                bounds=([0.0, 0.5, np.log(0.001), 0.1],
                        [5.0, 10.0, np.log(1000.0), 5.0]),
                maxfev=10000,
            )
        d_UV, d_IR, log_ss, alpha = popt
        sigma_star = np.exp(log_ss)
        ds_pred = cdt_sigmoid(log_sigma, *popt)
        ss_res = np.sum((ds_fit - ds_pred)**2)
        ss_tot = np.sum((ds_fit - np.mean(ds_fit))**2)
        R2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
        return d_UV, d_IR, sigma_star, alpha, R2
    except Exception:
        return None


def test1_cdt_flow_scaling():
    """CDT spectral dimension flow size scaling."""
    print("\n" + "=" * 76)
    print("TEST 1: CDT FLOW SIZE SCALING (Promote or Kill)")
    print("=" * 76)
    print("If sigma_*(L) -> constant: GENUINE flow (promote)")
    print("If sigma_*(L) ~ L^2:      FINITE-SIZE artifact (kill)")
    print()

    sides = [8, 10, 12, 14]
    sigmas = np.logspace(-2, 2, 50)
    results = {}

    for side in sides:
        t0 = time.time()
        pos, col, adj, n, src = make_staggered_lattice(SEED, side)
        _, _, phi = evolve_self_gravity(pos, col, adj, n, src)
        L_grav = gravity_laplacian(pos, adj, n, phi)
        ds, _ = spectral_dimension_flow(L_grav.toarray(), sigmas)
        fit = fit_sigmoid(sigmas, ds)
        elapsed = time.time() - t0

        if fit is not None:
            d_UV, d_IR, sigma_star, alpha, R2 = fit
            results[side] = {'sigma_star': sigma_star, 'R2': R2,
                             'd_UV': d_UV, 'd_IR': d_IR, 'alpha': alpha}
            print(f"  side={side:2d}  n={n:3d}  sigma_*={sigma_star:.4f}  "
                  f"R2={R2:.5f}  d_UV={d_UV:.3f}  d_IR={d_IR:.3f}  "
                  f"[{elapsed:.1f}s]")
        else:
            results[side] = None
            print(f"  side={side:2d}  n={n:3d}  FIT FAILED  [{elapsed:.1f}s]")

    # Verdict: check if sigma_* scales with L^2
    valid_sides = [s for s in sides if results[s] is not None]
    if len(valid_sides) >= 3:
        L_arr = np.array(valid_sides, dtype=float)
        ss_arr = np.array([results[s]['sigma_star'] for s in valid_sides])
        log_L = np.log(L_arr)
        log_ss = np.log(np.maximum(ss_arr, 1e-10))
        slope, intercept, r_value, _, _ = linregress(log_L, log_ss)

        print()
        print(f"  sigma_* vs L power-law: exponent = {slope:.3f}  "
              f"(R2={r_value**2:.4f})")
        ss_strs = [f'{results[s]["sigma_star"]:.4f}' for s in valid_sides]
        print(f"  sigma_* values: {ss_strs}")

        # Check variation
        ss_min, ss_max = np.min(ss_arr), np.max(ss_arr)
        variation = (ss_max - ss_min) / np.mean(ss_arr) if np.mean(ss_arr) > 0 else 999

        if slope > 1.5 and r_value**2 > 0.8:
            verdict = "KILL"
            reason = f"sigma_* ~ L^{slope:.1f} (finite-size artifact)"
        elif variation < 0.5:
            verdict = "PROMOTE"
            reason = f"sigma_* varies by {variation:.0%} (converging)"
        elif slope < 0.5:
            verdict = "PROMOTE"
            reason = f"sigma_* ~ L^{slope:.2f} (weak or no scaling)"
        else:
            verdict = "INCONCLUSIVE"
            reason = f"slope={slope:.2f}, variation={variation:.1%}"
    else:
        verdict = "INCONCLUSIVE"
        reason = "Too few valid fits"

    print()
    print(f"  VERDICT: {verdict} -- {reason}")
    return verdict, reason


# ============================================================================
# TEST 2: Multifractal Size Scaling
# ============================================================================

def test2_multifractal_scaling():
    """D_2 size scaling at G=2."""
    print("\n" + "=" * 76)
    print("TEST 2: MULTIFRACTAL SIZE SCALING (Promote or Kill)")
    print("=" * 76)
    print("If D_2(L) -> constant: genuine critical dimension (promote)")
    print("If D_2(L) -> 0 or 1:  finite-size crossover (kill)")
    print()

    G = 2.0
    sides = [6, 8, 10, 12]
    ipr_by_n = {}

    for side in sides:
        t0 = time.time()
        n = side * side
        pos, col, adj, actual_n, src = make_staggered_lattice(SEED, side)
        psi, _, _ = evolve_self_gravity(pos, col, adj, actual_n, src, G=G)

        rho = np.abs(psi)**2
        rho /= np.sum(rho)
        rho_reg = np.clip(rho, 1e-30, None)
        ipr2 = float(np.sum(rho_reg**2))
        ipr_by_n[actual_n] = ipr2
        elapsed = time.time() - t0
        print(f"  side={side:2d}  N={actual_n:3d}  IPR_2={ipr2:.6f}  [{elapsed:.1f}s]")

    # Fit D_2 from IPR_2 ~ N^{-tau_2}, where D_2 = tau_2
    # log(IPR_2) = -tau_2 * log(N) + const
    sizes = sorted(ipr_by_n.keys())
    log_n = np.log(np.array(sizes, dtype=float))
    log_ipr = np.log(np.array([ipr_by_n[n] for n in sizes]))
    slope, intercept, r_value, _, _ = linregress(log_n, log_ipr)
    D_2 = -slope  # tau_2 = -slope, D_2 = tau_2

    print()
    print(f"  D_2 (from size scaling) = {D_2:.4f}  (R2={r_value**2:.4f})")
    print(f"  IPR_2 values: {[f'{ipr_by_n[n]:.6f}' for n in sizes]}")

    # Also compute D_2 at each size individually (using largest two sizes)
    if len(sizes) >= 2:
        for i in range(len(sizes) - 1):
            n1, n2 = sizes[i], sizes[i + 1]
            d2_pair = -(np.log(ipr_by_n[n2]) - np.log(ipr_by_n[n1])) / \
                       (np.log(n2) - np.log(n1))
            print(f"  D_2 (N={n1}->{n2}) = {d2_pair:.4f}")

    # Verdict
    if D_2 < 0.1:
        verdict = "KILL"
        reason = f"D_2={D_2:.3f} -> 0 (full localization, not critical)"
    elif D_2 > 0.9:
        verdict = "KILL"
        reason = f"D_2={D_2:.3f} -> 1 (extended, not critical)"
    elif r_value**2 < 0.7:
        verdict = "INCONCLUSIVE"
        reason = f"Poor fit R2={r_value**2:.3f}"
    else:
        # Check if D_2 is stable: compare first-half vs second-half slope
        if len(sizes) >= 4:
            mid = len(sizes) // 2
            _, _, r1, _, _ = linregress(log_n[:mid+1], log_ipr[:mid+1])
            _, _, r2, _, _ = linregress(log_n[mid:], log_ipr[mid:])
            s1 = -linregress(log_n[:mid+1], log_ipr[:mid+1]).slope
            s2 = -linregress(log_n[mid:], log_ipr[mid:]).slope
            drift = abs(s2 - s1) / max(abs(D_2), 0.01)
            print(f"  D_2 stability: first-half={s1:.4f}, second-half={s2:.4f}, "
                  f"drift={drift:.2%}")
            if drift > 0.5:
                verdict = "INCONCLUSIVE"
                reason = f"D_2 drifting ({drift:.0%} change between halves)"
            else:
                verdict = "PROMOTE"
                reason = f"D_2={D_2:.3f} stable across sizes (drift {drift:.0%})"
        else:
            verdict = "PROMOTE"
            reason = f"D_2={D_2:.3f} in critical range"

    print()
    print(f"  VERDICT: {verdict} -- {reason}")
    return verdict, reason


# ============================================================================
# TEST 3: Memory with mu=0 (Fix Negative)
# ============================================================================

def test3_memory_mu0():
    """Memory effect with mu=0 (massless field) to fix large-N vanishing."""
    print("\n" + "=" * 76)
    print("TEST 3: MEMORY WITH mu=0 (Fix Negative)")
    print("=" * 76)
    print("Memory vanishes at large N because mu=0.22 Yukawa screening.")
    print("Fix: set mu=0 in wave equation (massless field).")
    print()

    ring_sizes = [41, 61, 81, 101]
    pulse_amp = 1.0
    dt_matter = 0.12
    dt_field = 0.03
    n_field_sub = 4
    n_steps = 60
    c_speed = 1.0
    gamma = 0.05
    beta = 5.0
    pulse_start = 10
    pulse_end = 20

    def build_ring_laplacian(n):
        L = lil_matrix((n, n), dtype=float)
        for i in range(n):
            ip = (i + 1) % n
            im = (i - 1) % n
            L[i, i] += 2.0
            L[i, ip] -= 1.0
            L[i, im] -= 1.0
        return L.tocsr()

    def ring_centroid(psi, n):
        prob = np.abs(psi)**2
        prob /= prob.sum() + 1e-30
        angles = 2 * np.pi * np.arange(n) / n
        cx = np.sum(prob * np.cos(angles))
        cy = np.sum(prob * np.sin(angles))
        return np.arctan2(cy, cx) / (2 * np.pi) * n % n

    def ring_distance(c1, c2, n):
        d = abs(c1 - c2)
        return min(d, n - d)

    def make_wavepacket(center, n, sigma=2.0):
        x = np.arange(n)
        dx = x - center
        dx = dx - n * np.round(dx / n)
        psi = np.exp(-dx**2 / (2 * sigma**2)).astype(complex)
        psi /= np.linalg.norm(psi)
        return psi

    def run_memory_sim(n, mu2_field, use_pulse):
        par = np.array([(-1)**i for i in range(n)], dtype=float)
        L = build_ring_laplacian(n)

        # Field operator: -c^2 * (L + mu^2 I) -- mu=0 for test
        field_op = -c_speed**2 * (L + mu2_field * speye(n, format='csr'))

        phi = np.zeros(n)
        pi_field = np.zeros(n)
        source_pos = n // 2
        source_profile = np.zeros(n)
        source_profile[source_pos] = 1.0

        pos_a = n // 4
        pos_b = 3 * n // 4
        psi_a = make_wavepacket(pos_a, n)
        psi_b = make_wavepacket(pos_b, n)

        sep_history = []
        for step in range(n_steps):
            ca = ring_centroid(psi_a, n)
            cb = ring_centroid(psi_b, n)
            sep_history.append(ring_distance(ca, cb, n))

            pulse_active = use_pulse and (pulse_start <= step < pulse_end)
            for _ in range(n_field_sub):
                source = beta * pulse_amp * source_profile if pulse_active else np.zeros(n)
                acc = field_op.dot(phi) - gamma * pi_field + source
                pi_field += 0.5 * dt_field * acc
                phi += dt_field * pi_field
                acc = field_op.dot(phi) - gamma * pi_field + source
                pi_field += 0.5 * dt_field * acc

            H = lil_matrix((n, n), dtype=complex)
            H.setdiag((MASS + phi) * par)
            for i in range(n):
                ip = (i + 1) % n
                H[i, ip] += -0.5j
                H[ip, i] += 0.5j
            H = H.tocsr()
            psi_a = cn_step(H, n, psi_a, dt_matter)
            psi_b = cn_step(H, n, psi_b, dt_matter)

        ca = ring_centroid(psi_a, n)
        cb = ring_centroid(psi_b, n)
        sep_history.append(ring_distance(ca, cb, n))
        return np.array(sep_history)

    # Run for both mu=0.22 (original) and mu=0 (fix)
    print(f"  {'N':>5}  {'mu2':>6}  {'Memory(net)':>12}  {'Ctrl_drift':>12}  {'Signal?':>8}")
    print(f"  {'-' * 55}")

    memory_results = {}
    for mu2_label, mu2_val in [("0.22", 0.22), ("0.00", 0.0)]:
        memory_results[mu2_label] = {}
        for n in ring_sizes:
            t0 = time.time()
            ctrl = run_memory_sim(n, mu2_val, use_pulse=False)
            pulse = run_memory_sim(n, mu2_val, use_pulse=True)
            ctrl_drift = ctrl[-1] - ctrl[0]
            pulse_drift = pulse[-1] - pulse[0]
            memory_net = pulse_drift - ctrl_drift
            memory_results[mu2_label][n] = {
                'memory_net': memory_net,
                'ctrl_drift': ctrl_drift,
            }
            has_signal = abs(memory_net) > 2 * abs(ctrl_drift) and abs(memory_net) > 1e-6
            elapsed = time.time() - t0
            print(f"  {n:5d}  {mu2_label:>6}  {memory_net:+12.6f}  "
                  f"{ctrl_drift:+12.6f}  {'YES' if has_signal else 'no':>8}  "
                  f"[{elapsed:.1f}s]")

    # Verdict
    print()
    mu0_mems = [memory_results["0.00"][n]['memory_net'] for n in ring_sizes]
    mu22_mems = [memory_results["0.22"][n]['memory_net'] for n in ring_sizes]
    mu0_ctrls = [memory_results["0.00"][n]['ctrl_drift'] for n in ring_sizes]

    # Check if mu=0 memory persists at large N
    large_n_signal = abs(mu0_mems[-1]) > 2 * abs(mu0_ctrls[-1]) and abs(mu0_mems[-1]) > 1e-6

    # Check if mu=0.22 memory vanishes while mu=0 persists
    mu22_persists = abs(mu22_mems[-1]) > 1e-6
    mu0_persists = abs(mu0_mems[-1]) > 1e-6

    print(f"  mu=0.22 memory at N={ring_sizes[-1]}: {mu22_mems[-1]:+.6f}  "
          f"{'persists' if mu22_persists else 'VANISHES'}")
    print(f"  mu=0.00 memory at N={ring_sizes[-1]}: {mu0_mems[-1]:+.6f}  "
          f"{'persists' if mu0_persists else 'VANISHES'}")

    if mu0_persists and large_n_signal:
        verdict = "FIX CONFIRMED"
        reason = "mu=0 restores memory at large N"
    elif mu0_persists and not large_n_signal:
        verdict = "PARTIAL FIX"
        reason = "mu=0 has signal but weak relative to control drift"
    elif not mu0_persists and not mu22_persists:
        verdict = "FIX FAILED"
        reason = "Memory vanishes at large N even with mu=0"
    else:
        verdict = "INCONCLUSIVE"
        reason = "Mixed results"

    print()
    print(f"  VERDICT: {verdict} -- {reason}")
    return verdict, reason


# ============================================================================
# TEST 4: Eigenvalue Statistics (Falsification)
# ============================================================================

def wigner_surmise_goe(s):
    """Wigner surmise for GOE: P(s) = (pi/2)*s*exp(-pi*s^2/4)."""
    return (np.pi / 2) * s * np.exp(-np.pi * s**2 / 4)


def wigner_surmise_gue(s):
    """Wigner surmise for GUE: P(s) = (32/pi^2)*s^2*exp(-4*s^2/pi)."""
    return (32 / np.pi**2) * s**2 * np.exp(-4 * s**2 / np.pi)


def poisson_spacing(s):
    """Poisson level spacing: P(s) = exp(-s)."""
    return np.exp(-s)


def test4_eigenvalue_statistics():
    """Check if gravitational Hamiltonian matches RMT or Poisson."""
    print("\n" + "=" * 76)
    print("TEST 4: EIGENVALUE STATISTICS (Falsification)")
    print("=" * 76)
    print("Wigner-Dyson (GOE/GUE) => generic chaotic spectrum")
    print("Poisson                 => integrable/gravitational")
    print()

    side = 10
    pos, col, adj, n, src = make_staggered_lattice(SEED, side)

    # Free Hamiltonian (control)
    t0 = time.time()
    H_free = build_hamiltonian(pos, col, adj, n, MASS, np.zeros(n))
    evals_free = np.sort(np.linalg.eigvalsh(H_free.toarray()))
    t_free = time.time() - t0

    # Gravitational Hamiltonian
    t0 = time.time()
    _, H_grav, _ = evolve_self_gravity(pos, col, adj, n, src)
    evals_grav = np.sort(np.linalg.eigvalsh(H_grav.toarray()))
    t_grav = time.time() - t0

    print(f"  Free Hamiltonian: {n} evals in [{evals_free[0]:.4f}, {evals_free[-1]:.4f}]  [{t_free:.1f}s]")
    print(f"  Grav Hamiltonian: {n} evals in [{evals_grav[0]:.4f}, {evals_grav[-1]:.4f}]  [{t_grav:.1f}s]")
    print()

    verdicts = {}
    for label, evals in [("Free", evals_free), ("Gravity", evals_grav)]:
        # Unfolding: use local mean spacing
        # Simple approach: normalize spacings by local mean
        spacings = np.diff(evals)
        # Remove zero spacings (degeneracies)
        spacings = spacings[spacings > 1e-12]
        if len(spacings) < 20:
            print(f"  {label}: too few spacings ({len(spacings)})")
            verdicts[label] = "INCONCLUSIVE"
            continue

        # Local unfolding with sliding window
        window = max(5, len(spacings) // 10)
        unfolded = np.zeros_like(spacings)
        for i in range(len(spacings)):
            lo = max(0, i - window)
            hi = min(len(spacings), i + window + 1)
            local_mean = np.mean(spacings[lo:hi])
            unfolded[i] = spacings[i] / local_mean if local_mean > 0 else 0
        unfolded = unfolded[unfolded > 0]
        s = unfolded

        # Generate reference samples
        n_ref = 10000
        s_goe = np.random.default_rng(42).weibull(2, n_ref)
        s_goe *= np.sqrt(np.pi) / 2  # scale for Wigner surmise GOE
        s_poisson = np.random.default_rng(42).exponential(1.0, n_ref)

        # KS test against GOE and Poisson
        ks_goe, p_goe = ks_2samp(s, s_goe)
        ks_poisson, p_poisson = ks_2samp(s, s_poisson)

        # Also compute <r> ratio (ratio of consecutive spacings)
        # <r> = 0.386 for Poisson, 0.530 for GOE, 0.603 for GUE
        if len(spacings) > 2:
            r_vals = np.minimum(spacings[1:], spacings[:-1]) / \
                     np.maximum(spacings[1:], spacings[:-1])
            r_mean = np.mean(r_vals[np.isfinite(r_vals)])
        else:
            r_mean = 0.0

        print(f"  {label}:")
        print(f"    N spacings (unfolded): {len(s)}")
        print(f"    KS vs GOE:     D={ks_goe:.4f}  p={p_goe:.4f}")
        print(f"    KS vs Poisson: D={ks_poisson:.4f}  p={p_poisson:.4f}")
        print(f"    <r> ratio:     {r_mean:.4f}  "
              f"(Poisson=0.386, GOE=0.530, GUE=0.603)")

        # Classify
        if ks_poisson < ks_goe:
            closest = "Poisson"
        else:
            closest = "GOE/GUE"

        if r_mean < 0.44:
            r_class = "Poisson-like"
        elif r_mean < 0.57:
            r_class = "GOE-like"
        else:
            r_class = "GUE-like"

        print(f"    KS closest: {closest}  |  <r> class: {r_class}")
        verdicts[label] = (closest, r_class, r_mean, ks_goe, ks_poisson)

    # Final verdict
    print()
    grav_v = verdicts.get("Gravity")
    free_v = verdicts.get("Free")
    if isinstance(grav_v, tuple):
        grav_closest, grav_r_class, grav_r, _, _ = grav_v
        if grav_closest == "Poisson" and "Poisson" in grav_r_class:
            verdict = "PASS (integrable)"
            reason = (f"Gravity spectrum is Poisson-like (<r>={grav_r:.3f}), "
                      "consistent with integrable/gravitational system")
        elif "GOE" in grav_closest or "GUE" in grav_closest:
            # Check if free is also GOE/GUE
            if isinstance(free_v, tuple) and ("GOE" in free_v[0] or "GUE" in free_v[0]):
                verdict = "FAIL (generic)"
                reason = ("Both free and gravity spectra are Wigner-Dyson; "
                          "gravity spectrum is generic chaotic")
            else:
                verdict = "NOTABLE"
                reason = (f"Gravity spectrum is {grav_r_class} while free is different; "
                          "gravity introduces chaos")
        else:
            verdict = "INCONCLUSIVE"
            reason = f"Mixed signals: KS={grav_closest}, <r>={grav_r_class}"
    else:
        verdict = "INCONCLUSIVE"
        reason = "Could not classify"

    print(f"  VERDICT: {verdict} -- {reason}")
    return verdict, reason


# ============================================================================
# TEST 5: Entanglement Crossover Finite-Size Scaling
# ============================================================================

def bfs_ball(adj, center, radius, n):
    dist = np.full(n, -1, dtype=int)
    dist[center] = 0
    queue = deque([center])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                if dist[v] <= radius:
                    queue.append(v)
    A_set = set(i for i in range(n) if 0 <= dist[i] <= radius)
    A_nodes = sorted(A_set)
    bnd = sum(1 for i in A_nodes for j in adj[i] if j not in A_set)
    return A_nodes, len(A_nodes), bnd


def entanglement_entropy(C, A_nodes):
    if len(A_nodes) == 0:
        return 0.0
    ix = np.ix_(A_nodes, A_nodes)
    C_A = C[ix]
    C_A = 0.5 * (C_A + C_A.conj().T)
    nu = np.linalg.eigvalsh(C_A).real
    nu = np.clip(nu, 1e-15, 1.0 - 1e-15)
    return float(-np.sum(nu * np.log(nu) + (1 - nu) * np.log(1 - nu)))


def dirac_sea_correlation(H):
    H_dense = H.toarray()
    H_dense = 0.5 * (H_dense + H_dense.conj().T)
    eigenvalues, eigenvectors = np.linalg.eigh(H_dense)
    filled = eigenvalues < 0
    n_filled = np.sum(filled)
    if n_filled == 0:
        n_filled = len(eigenvalues) // 2
        filled = np.zeros(len(eigenvalues), dtype=bool)
        filled[:n_filled] = True
    V = eigenvectors[:, filled]
    return V @ V.conj().T


def test5_entanglement_crossover():
    """Entanglement area-to-volume crossover finite-size scaling."""
    print("\n" + "=" * 76)
    print("TEST 5: ENTANGLEMENT CROSSOVER FINITE-SIZE SCALING (Promote or Kill)")
    print("=" * 76)
    print("If FSS collapse works: genuine phase transition (promote)")
    print("If crossing drifts with L: finite-size artifact (kill)")
    print()

    sides = [8, 10, 12, 14]
    G_values = [5.0, 7.0, 9.0, 10.0, 11.0, 13.0, 15.0]
    radii = [1, 2, 3, 4]

    # delta_R2(G, L) = R2_area - R2_vol
    delta_R2 = {}

    for side in sides:
        n, pos, adj, col = build_periodic_lattice(side)
        center = (side // 2) * side + (side // 2)

        balls = {}
        for R in radii:
            A_nodes, nA, bnd = bfs_ball(adj, center, R, n)
            if nA < n:
                balls[R] = (A_nodes, nA, bnd)

        delta_R2[side] = {}
        for G in G_values:
            t0 = time.time()
            # Evolve
            cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
            cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
            r2 = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
            psi = np.exp(-r2 / (2 * 1.5**2)).astype(complex)
            psi /= np.linalg.norm(psi)

            L_graph = lil_matrix((n, n), dtype=float)
            for i in range(n):
                degree = len(adj[i])
                L_graph[i, i] = float(degree)
                for j in adj[i]:
                    L_graph[i, j] = -1.0
            L_graph = L_graph.tocsr()

            H_final = None
            for _ in range(N_STEPS):
                rho = np.abs(psi)**2
                if G > 0:
                    A_mat = (L_graph + MU2 * speye(n, format='csr')).tocsc()
                    phi = spsolve(A_mat, G * rho)
                else:
                    phi = np.zeros(n)
                H = lil_matrix((n, n), dtype=complex)
                par = np.where(col == 0, 1.0, -1.0)
                H.setdiag((MASS + phi) * par)
                for i, nbs in adj.items():
                    for j in nbs:
                        if i >= j:
                            continue
                        d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
                        d = min(d, 2.0)
                        w = 1.0 / max(d, 0.5)
                        H[i, j] += -0.5j * w
                        H[j, i] += 0.5j * w
                H = H.tocsc()
                psi = spsolve(
                    (speye(n, format='csc') + 1j * H * DT / 2).tocsc(),
                    (speye(n, format='csr') - 1j * H * DT / 2).dot(psi)
                )
                psi /= np.linalg.norm(psi)
                H_final = H

            C = dirac_sea_correlation(H_final)

            # Compute entanglement for each radius
            S_list = []
            nA_list = []
            bnd_list = []
            for R in radii:
                if R not in balls:
                    continue
                A_nodes, nA, bnd = balls[R]
                S = entanglement_entropy(C, A_nodes)
                S_list.append(S)
                nA_list.append(nA)
                bnd_list.append(bnd)

            if len(S_list) < 3:
                delta_R2[side][G] = 0.0
                continue

            S_arr = np.array(S_list)
            nA_arr = np.array(nA_list, dtype=float)
            bnd_arr = np.array(bnd_list, dtype=float)

            # R2 for area law: S vs |bnd|
            if np.std(bnd_arr) > 0:
                r_area = linregress(bnd_arr, S_arr).rvalue**2
            else:
                r_area = 0.0
            # R2 for volume law: S vs |A|
            if np.std(nA_arr) > 0:
                r_vol = linregress(nA_arr, S_arr).rvalue**2
            else:
                r_vol = 0.0

            dr2 = r_area - r_vol
            delta_R2[side][G] = dr2
            elapsed = time.time() - t0
            print(f"  side={side:2d}  G={G:5.1f}  R2_area={r_area:.4f}  "
                  f"R2_vol={r_vol:.4f}  delta={dr2:+.4f}  [{elapsed:.1f}s]")

    # Analysis: find crossing point G_c for each size
    print()
    print("  Crossing analysis (delta_R2 = 0 => G_c):")
    crossings = {}
    for side in sides:
        g_arr = np.array(G_values)
        dr2_arr = np.array([delta_R2[side].get(g, 0.0) for g in G_values])

        # Find zero crossing by linear interpolation
        gc = None
        for i in range(len(g_arr) - 1):
            if dr2_arr[i] * dr2_arr[i + 1] < 0:
                # Linear interpolation
                gc = g_arr[i] - dr2_arr[i] * (g_arr[i + 1] - g_arr[i]) / \
                     (dr2_arr[i + 1] - dr2_arr[i])
                break
        crossings[side] = gc
        if gc is not None:
            print(f"    side={side:2d}: G_c = {gc:.2f}")
        else:
            # Report closest to zero
            min_idx = np.argmin(np.abs(dr2_arr))
            print(f"    side={side:2d}: no crossing, closest delta_R2={dr2_arr[min_idx]:+.4f} "
                  f"at G={g_arr[min_idx]:.1f}")

    # Check if G_c is stable
    valid_gc = {s: gc for s, gc in crossings.items() if gc is not None}
    if len(valid_gc) >= 2:
        gc_vals = list(valid_gc.values())
        gc_mean = np.mean(gc_vals)
        gc_std = np.std(gc_vals)
        gc_spread = gc_std / gc_mean if gc_mean > 0 else 999

        print()
        print(f"  G_c values: {[f'{gc:.2f}' for gc in gc_vals]}")
        print(f"  G_c mean={gc_mean:.2f}, std={gc_std:.2f}, spread={gc_spread:.1%}")

        # Attempt scaling collapse: (G - G_c) * L^(1/nu)
        # Try nu = 0.5, 1.0, 1.5, 2.0 and find best collapse
        best_nu = None
        best_collapse_quality = float('inf')

        for nu_trial in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
            # For each side, compute x = (G - gc_mean) * side^(1/nu)
            all_x = []
            all_y = []
            for side in sides:
                for g in G_values:
                    x = (g - gc_mean) * side**(1.0 / nu_trial)
                    y = delta_R2[side].get(g, 0.0)
                    all_x.append(x)
                    all_y.append(y)

            # Quality: variance of y at similar x values
            all_x = np.array(all_x)
            all_y = np.array(all_y)
            # Bin x and compute variance within bins
            x_sorted = np.sort(np.unique(all_x))
            if len(x_sorted) < 3:
                continue
            x_bins = np.linspace(all_x.min(), all_x.max(), 8)
            total_var = 0.0
            n_bins = 0
            for i in range(len(x_bins) - 1):
                mask = (all_x >= x_bins[i]) & (all_x < x_bins[i + 1])
                if mask.sum() >= 2:
                    total_var += np.var(all_y[mask])
                    n_bins += 1
            avg_var = total_var / max(n_bins, 1)

            if avg_var < best_collapse_quality:
                best_collapse_quality = avg_var
                best_nu = nu_trial

        if best_nu is not None:
            print(f"  Best scaling collapse: nu={best_nu:.2f}  "
                  f"(bin variance={best_collapse_quality:.6f})")

        if gc_spread < 0.15:
            verdict = "PROMOTE"
            reason = f"G_c={gc_mean:.1f}+/-{gc_std:.1f} stable across sizes"
        elif gc_spread < 0.30:
            verdict = "INCONCLUSIVE"
            reason = f"G_c spread {gc_spread:.0%} -- need larger sizes"
        else:
            verdict = "KILL"
            reason = f"G_c drifts with L (spread {gc_spread:.0%})"
    elif len(valid_gc) == 1:
        verdict = "INCONCLUSIVE"
        reason = "Only one size shows crossing"
    else:
        # Check if all delta_R2 have same sign (no transition in range)
        all_positive = all(
            all(delta_R2[s].get(g, 0) > 0 for g in G_values) for s in sides
        )
        all_negative = all(
            all(delta_R2[s].get(g, 0) < 0 for g in G_values) for s in sides
        )
        if all_positive:
            verdict = "KILL"
            reason = "Area law dominates at all G (no transition in range)"
        elif all_negative:
            verdict = "KILL"
            reason = "Volume law dominates at all G (no transition in range)"
        else:
            verdict = "INCONCLUSIVE"
            reason = "No clean crossing found"

    print()
    print(f"  VERDICT: {verdict} -- {reason}")
    return verdict, reason


# ============================================================================
# Main: run all tests and produce summary
# ============================================================================

def main():
    t_total = time.time()

    print("=" * 76)
    print("FRONTIER PROMOTION BATTERY")
    print("=" * 76)
    print(f"Physics: MASS={MASS}, MU2={MU2}, DT={DT}, G={G_DEFAULT}")
    print(f"Parity coupling, {N_STEPS} CN steps, seed={SEED}")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    results = {}

    # Test 1
    v1, r1 = test1_cdt_flow_scaling()
    results['CDT Flow Scaling'] = (v1, r1)

    # Test 2
    v2, r2 = test2_multifractal_scaling()
    results['Multifractal D_2'] = (v2, r2)

    # Test 3
    v3, r3 = test3_memory_mu0()
    results['Memory mu=0 Fix'] = (v3, r3)

    # Test 4
    v4, r4 = test4_eigenvalue_statistics()
    results['Eigenvalue Stats'] = (v4, r4)

    # Test 5
    v5, r5 = test5_entanglement_crossover()
    results['Entanglement FSS'] = (v5, r5)

    # Summary table
    elapsed = time.time() - t_total
    print()
    print("=" * 76)
    print("SUMMARY TABLE")
    print("=" * 76)
    print(f"{'Test':.<35} {'Verdict':.<20} {'Reason'}")
    print("-" * 76)
    for name, (verdict, reason) in results.items():
        print(f"{name:.<35} {verdict:.<20} {reason}")

    print()
    print(f"Total elapsed: {elapsed:.0f}s")

    # Counts
    promoted = sum(1 for v, _ in results.values() if 'PROMOTE' in v)
    killed = sum(1 for v, _ in results.values() if 'KILL' in v)
    fixed = sum(1 for v, _ in results.values() if 'FIX' in v)
    failed = sum(1 for v, _ in results.values() if 'FAIL' in v)
    inconclusive = sum(1 for v, _ in results.values() if 'INCONCLUSIVE' in v)

    print(f"Promoted: {promoted}  |  Killed: {killed}  |  Fixed: {fixed}  |  "
          f"Failed: {failed}  |  Inconclusive: {inconclusive}")
    print("=" * 76)


if __name__ == "__main__":
    main()
