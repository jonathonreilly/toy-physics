#!/usr/bin/env python3
"""
Frontier: Born Rule from Gravitational Self-Consistency
========================================================

Does self-consistent gravitational backreaction REQUIRE the Born rule
p = |psi|^2 (alpha=2)?

The self-consistency condition is: V = G * K * rho, where rho = |psi|^alpha
is the generalized "probability" measure. The standard Born rule has alpha=2.
If alpha=2 is the UNIQUE value that produces a stable self-consistent fixed
point, then gravity selects the Born rule.

Protocol on 2D staggered lattice (side=10, n=100):

For each alpha in [1.0, 1.2, 1.5, 1.8, 1.9, 1.95, 2.0, 2.05, 2.1, 2.2,
2.5, 3.0, 4.0]:

1. Initialize Gaussian wavepacket at center
2. Run self-consistent Hartree loop for 100 iterations
3. Measure convergence metrics: norm stability, phi convergence, energy
   stability, width stability
4. Compute Lyapunov exponent of the iteration
5. Test sign selectivity at each alpha
6. Sweep G = [5, 10, 50] for G-dependence

HYPOTHESIS: alpha=2 is the unique stable fixed point of the self-consistent
Hartree iteration — other alpha values show divergent or oscillatory behavior.

FALSIFICATION: If multiple alpha values show equal convergence quality, the
Born rule is not uniquely selected by self-consistency.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy import sparse
from scipy.sparse import eye as speye, lil_matrix
from scipy.sparse.linalg import spsolve

# ── Physical parameters ────────────────────────────────────────────
MASS = 0.30
MU2 = 0.22
DT = 0.12
SIGMA = 1.5
SIDE = 10
N_ITER = 100

ALPHAS = [1.0, 1.2, 1.5, 1.8, 1.9, 1.95, 2.0, 2.05, 2.1, 2.2, 2.5, 3.0, 4.0]
G_VALUES = [5.0, 10.0, 50.0]
SIGN_ITER = 40


# ── Lattice ────────────────────────────────────────────────────────

def build_lattice_2d(side: int):
    """2D periodic square lattice with checkerboard parity."""
    n = side * side
    pos = np.zeros((n, 2))
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    col = np.zeros(n, dtype=int)

    for ix in range(side):
        for iy in range(side):
            idx = ix * side + iy
            pos[idx] = (ix, iy)
            col[idx] = (ix + iy) % 2
            for dix, diy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                jx = (ix + dix) % side
                jy = (iy + diy) % side
                adj[idx].append(jx * side + jy)

    return n, pos, adj, col


# ── Hamiltonian and evolution ──────────────────────────────────────

def build_laplacian(adj: dict[int, list[int]], n: int):
    L = lil_matrix((n, n), dtype=float)
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            L[i, j] -= 1.0
            L[j, i] -= 1.0
            L[i, i] += 1.0
            L[j, j] += 1.0
    return L.tocsr()


def build_hamiltonian(pos: np.ndarray, col: np.ndarray,
                      adj: dict[int, list[int]], n: int,
                      phi: np.ndarray) -> sparse.csc_matrix:
    """Staggered-fermion Hamiltonian with parity coupling."""
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * par)

    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            d = min(d, 2.0)
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w

    return H.tocsc()


def cn_step(H: sparse.csc_matrix, psi: np.ndarray, dt: float) -> np.ndarray:
    """Crank-Nicolson time step."""
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def make_gaussian(pos: np.ndarray, n: int) -> np.ndarray:
    cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
    cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
    r2 = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
    psi = np.exp(-r2 / (2 * SIGMA**2)).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


def rms_width(psi: np.ndarray, pos: np.ndarray) -> float:
    rho = np.abs(psi)**2
    rho /= np.sum(rho)
    cx = np.sum(rho * pos[:, 0])
    cy = np.sum(rho * pos[:, 1])
    return float(np.sqrt(np.sum(rho * ((pos[:, 0] - cx)**2 +
                                        (pos[:, 1] - cy)**2))))


# ── BFS for sign selectivity ──────────────────────────────────────

def bfs_depth(adj: dict[int, list[int]], src: int, n: int):
    from collections import deque
    depth = np.full(n, np.inf)
    depth[src] = 0
    q = deque([src])
    while q:
        i = q.popleft()
        for j in adj[i]:
            if depth[j] == np.inf:
                depth[j] = depth[i] + 1
                q.append(j)
    return depth


def shell_force_toward(depth: np.ndarray, n: int,
                       psi: np.ndarray, phi: np.ndarray) -> bool:
    finite = depth[np.isfinite(depth)]
    max_d = int(np.max(finite)) if finite.size else 0
    if max_d <= 0:
        return False

    rho = np.abs(psi)**2
    rho_n = rho / np.sum(rho)
    shell_phi = np.zeros(max_d + 1)
    shell_count = np.zeros(max_d + 1)
    shell_prob = np.zeros(max_d + 1)

    for i in range(n):
        d = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d <= max_d:
            shell_phi[d] += phi[i]
            shell_prob[d] += rho_n[i]
            shell_count[d] += 1
    for d in range(max_d + 1):
        if shell_count[d] > 0:
            shell_phi[d] /= shell_count[d]

    grad = np.zeros(max_d + 1)
    for d in range(max_d + 1):
        if d == 0:
            grad[d] = shell_phi[0] - shell_phi[min(1, max_d)]
        elif d == max_d:
            grad[d] = shell_phi[d - 1] - shell_phi[d]
        else:
            grad[d] = 0.5 * (shell_phi[d - 1] - shell_phi[d + 1])

    force = float(np.sum(shell_prob * grad))
    return force > 0


# ═══════════════════════════════════════════════════════════════════
# TEST 1: Hartree self-consistency convergence vs alpha
# ═══════════════════════════════════════════════════════════════════

def run_hartree_loop(alpha: float, G: float, pos: np.ndarray,
                     col: np.ndarray, adj: dict[int, list[int]],
                     n: int, L_csr, solve_op) -> dict:
    """Run N_ITER self-consistent Hartree steps at given alpha and G.

    Returns convergence metrics: norm history, phi_change history,
    energy history, width history.
    """
    psi = make_gaussian(pos, n)
    phi = np.zeros(n)

    norms = []
    phi_changes = []
    energies = []
    widths = []

    for step in range(N_ITER):
        # Generalized density
        rho_alpha = np.abs(psi)**alpha
        rho_sum = np.sum(rho_alpha)
        if rho_sum > 1e-30:
            rho_alpha /= rho_sum
        else:
            rho_alpha = np.ones(n) / n

        # Solve for potential
        phi_new = spsolve(solve_op, G * rho_alpha)

        # Track phi convergence
        phi_change = np.linalg.norm(phi_new - phi)
        phi_changes.append(phi_change)
        phi = phi_new

        # Build Hamiltonian with parity coupling
        H = build_hamiltonian(pos, col, adj, n, phi)

        # Crank-Nicolson step
        psi = cn_step(H, psi, DT)

        # Track metrics
        norm = np.linalg.norm(psi)
        norms.append(norm)

        energy = float(np.real(np.conj(psi) @ H @ psi))
        energies.append(energy)

        width = rms_width(psi, pos)
        widths.append(width)

    return {
        'norms': np.array(norms),
        'phi_changes': np.array(phi_changes),
        'energies': np.array(energies),
        'widths': np.array(widths),
        'final_psi': psi,
        'final_phi': phi,
    }


# ═══════════════════════════════════════════════════════════════════
# TEST 2: Lyapunov exponent of the Hartree iteration
# ═══════════════════════════════════════════════════════════════════

def lyapunov_exponent(alpha: float, G: float, pos: np.ndarray,
                      col: np.ndarray, adj: dict[int, list[int]],
                      n: int, solve_op) -> float:
    """Estimate Lyapunov exponent by perturbing the self-consistent loop.

    Run two copies of the Hartree loop starting from slightly different
    initial conditions and track the divergence rate.
    """
    psi1 = make_gaussian(pos, n)

    # Perturb: add small random perturbation
    rng = np.random.RandomState(42)
    eps = 1e-8
    delta = rng.randn(n) + 1j * rng.randn(n)
    delta *= eps / np.linalg.norm(delta)
    psi2 = psi1 + delta
    psi2 /= np.linalg.norm(psi2)

    phi1 = np.zeros(n)
    phi2 = np.zeros(n)

    log_ratios = []

    for step in range(N_ITER):
        # Path 1
        rho1 = np.abs(psi1)**alpha
        s1 = np.sum(rho1)
        if s1 > 1e-30:
            rho1 /= s1
        phi1 = spsolve(solve_op, G * rho1)
        H1 = build_hamiltonian(pos, col, adj, n, phi1)
        psi1 = cn_step(H1, psi1, DT)

        # Path 2
        rho2 = np.abs(psi2)**alpha
        s2 = np.sum(rho2)
        if s2 > 1e-30:
            rho2 /= s2
        phi2 = spsolve(solve_op, G * rho2)
        H2 = build_hamiltonian(pos, col, adj, n, phi2)
        psi2 = cn_step(H2, psi2, DT)

        # Track separation
        sep = np.linalg.norm(psi1 - psi2)
        if sep > 1e-30:
            log_ratios.append(np.log(sep / eps))

    if len(log_ratios) < 10:
        return float('nan')

    # Lyapunov exponent = slope of log(separation) vs time
    from scipy.stats import linregress
    steps = np.arange(len(log_ratios))
    res = linregress(steps, log_ratios)
    return res.slope


# ═══════════════════════════════════════════════════════════════════
# TEST 3: Sign selectivity vs alpha
# ═══════════════════════════════════════════════════════════════════

def sign_selectivity_at_alpha(alpha: float, G: float, pos: np.ndarray,
                              col: np.ndarray, adj: dict[int, list[int]],
                              n: int, solve_op) -> tuple[int, int, int]:
    """Measure attract vs repulse toward-counts at given alpha."""
    center_idx = (SIDE // 2) * SIDE + (SIDE // 2)
    depth = bfs_depth(adj, center_idx, n)

    results = {}
    for label, sign in [("attract", +1.0), ("repulse", -1.0)]:
        psi = make_gaussian(pos, n)
        phi = np.zeros(n)
        tw = 0
        for step in range(SIGN_ITER):
            rho_alpha = np.abs(psi)**alpha
            s = np.sum(rho_alpha)
            if s > 1e-30:
                rho_alpha /= s
            phi = spsolve(solve_op, G * rho_alpha)
            if shell_force_toward(depth, n, psi, sign * phi):
                tw += 1
            H = build_hamiltonian(pos, col, adj, n, sign * phi)
            psi = cn_step(H, psi, DT)
        results[label] = tw

    margin = results["attract"] - results["repulse"]
    return results["attract"], results["repulse"], margin


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    t0 = time.time()

    print("=" * 78)
    print("FRONTIER: BORN RULE FROM GRAVITATIONAL SELF-CONSISTENCY")
    print("Does alpha=2 (Born rule) uniquely produce stable backreaction?")
    print("=" * 78)
    print()
    print(f"Lattice: {SIDE}x{SIDE} periodic staggered (n={SIDE**2})")
    print(f"MASS={MASS}, MU2={MU2}, DT={DT}, SIGMA={SIGMA}")
    print(f"N_ITER={N_ITER}, SIGN_ITER={SIGN_ITER}")
    print(f"Alphas: {ALPHAS}")
    print(f"G values: {G_VALUES}")
    print()

    n, pos, adj, col = build_lattice_2d(SIDE)
    L = build_laplacian(adj, n)
    solve_op = (L + MU2 * speye(n, format='csr')).tocsc()

    # ═══════════════════════════════════════════════════════════════
    # SWEEP 1: Convergence metrics vs alpha for each G
    # ═══════════════════════════════════════════════════════════════

    all_results = {}  # (alpha, G) -> metrics dict

    for G in G_VALUES:
        print("=" * 78)
        print(f"G = {G}")
        print("=" * 78)
        print()

        print(f"{'alpha':>6s}  {'phi_chg_final':>13s}  {'phi_chg_mean':>12s}  "
              f"{'norm_dev':>10s}  {'E_std':>10s}  {'w_std':>10s}  "
              f"{'w_final':>8s}  {'Lyapunov':>10s}")
        print("-" * 100)

        for alpha in ALPHAS:
            metrics = run_hartree_loop(alpha, G, pos, col, adj, n, L, solve_op)
            lyap = lyapunov_exponent(alpha, G, pos, col, adj, n, solve_op)

            # Convergence indicators
            phi_chg_final = metrics['phi_changes'][-1]
            phi_chg_mean_last10 = np.mean(metrics['phi_changes'][-10:])
            norm_dev = np.std(metrics['norms'])
            energy_std = np.std(metrics['energies'][-20:])
            width_std = np.std(metrics['widths'][-20:])
            width_final = metrics['widths'][-1]

            all_results[(alpha, G)] = {
                'phi_chg_final': phi_chg_final,
                'phi_chg_mean_last10': phi_chg_mean_last10,
                'norm_dev': norm_dev,
                'energy_std': energy_std,
                'width_std': width_std,
                'width_final': width_final,
                'lyapunov': lyap,
                'metrics': metrics,
            }

            print(f"{alpha:>6.2f}  {phi_chg_final:>13.6e}  "
                  f"{phi_chg_mean_last10:>12.6e}  "
                  f"{norm_dev:>10.6e}  {energy_std:>10.6e}  "
                  f"{width_std:>10.6e}  {width_final:>8.4f}  "
                  f"{lyap:>10.6f}")

        print()

    # ═══════════════════════════════════════════════════════════════
    # SWEEP 2: Sign selectivity vs alpha
    # ═══════════════════════════════════════════════════════════════

    print("=" * 78)
    print("SIGN SELECTIVITY VS ALPHA (G=5)")
    print("=" * 78)
    print()

    G_sel = 5.0
    sel_results = {}

    print(f"{'alpha':>6s}  {'attract':>8s}  {'repulse':>8s}  {'margin':>8s}  "
          f"{'selectivity':>12s}")
    print("-" * 55)

    for alpha in ALPHAS:
        tw_a, tw_r, margin = sign_selectivity_at_alpha(
            alpha, G_sel, pos, col, adj, n, solve_op)
        sel_pct = tw_a / SIGN_ITER * 100
        sel_results[alpha] = {
            'attract': tw_a, 'repulse': tw_r, 'margin': margin,
            'selectivity': sel_pct,
        }
        print(f"{alpha:>6.2f}  {tw_a:>8d}  {tw_r:>8d}  {margin:>+8d}  "
              f"{sel_pct:>11.1f}%")

    print()

    # ═══════════════════════════════════════════════════════════════
    # COMPOSITE STABILITY SCORE
    # ═══════════════════════════════════════════════════════════════

    print("=" * 78)
    print("COMPOSITE STABILITY SCORE")
    print("(lower = more stable self-consistent fixed point)")
    print("=" * 78)
    print()

    for G in G_VALUES:
        print(f"--- G = {G} ---")
        print(f"{'alpha':>6s}  {'phi_conv':>10s}  {'E_stab':>10s}  "
              f"{'w_stab':>10s}  {'|lyap|':>10s}  {'SCORE':>10s}")
        print("-" * 65)

        scores = {}
        for alpha in ALPHAS:
            r = all_results[(alpha, G)]
            # Composite: weighted sum of instability indicators
            # Each metric: lower = more stable
            phi_conv = r['phi_chg_mean_last10']
            e_stab = r['energy_std']
            w_stab = r['width_std']
            lyap_abs = abs(r['lyapunov']) if not np.isnan(r['lyapunov']) else 10.0

            # Normalize by scale: use log for wide-range quantities
            score = (np.log10(max(phi_conv, 1e-20)) +
                     np.log10(max(e_stab, 1e-20)) +
                     np.log10(max(w_stab, 1e-20)) +
                     lyap_abs)

            scores[alpha] = score
            print(f"{alpha:>6.2f}  {phi_conv:>10.3e}  {e_stab:>10.3e}  "
                  f"{w_stab:>10.3e}  {lyap_abs:>10.6f}  {score:>10.4f}")

        best_alpha = min(scores, key=scores.get)
        print(f"\n  Best alpha (lowest score): {best_alpha:.2f}")
        print()

    # ═══════════════════════════════════════════════════════════════
    # VERDICT
    # ═══════════════════════════════════════════════════════════════

    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    print()

    # Check if alpha=2.0 is uniquely best across all G values
    best_alphas = {}
    for G in G_VALUES:
        scores_g = {}
        for alpha in ALPHAS:
            r = all_results[(alpha, G)]
            phi_conv = r['phi_chg_mean_last10']
            e_stab = r['energy_std']
            w_stab = r['width_std']
            lyap_abs = abs(r['lyapunov']) if not np.isnan(r['lyapunov']) else 10.0
            scores_g[alpha] = (np.log10(max(phi_conv, 1e-20)) +
                               np.log10(max(e_stab, 1e-20)) +
                               np.log10(max(w_stab, 1e-20)) +
                               lyap_abs)
        best_alphas[G] = min(scores_g, key=scores_g.get)

    all_born = all(ba == 2.0 for ba in best_alphas.values())

    if all_born:
        print("  HYPOTHESIS CONFIRMED: alpha=2.0 (Born rule) is the unique")
        print("  stable fixed point of the self-consistent Hartree iteration")
        print("  across all tested G values.")
    else:
        print("  HYPOTHESIS STATUS: alpha=2.0 is NOT uniquely best across all G.")
        for G in G_VALUES:
            print(f"    G={G:>5.1f}: best alpha = {best_alphas[G]:.2f}")

    print()

    # Check sign selectivity
    sel_at_2 = sel_results[2.0]['margin']
    perfect_sel = sel_results[2.0]['selectivity']
    other_sels = [(a, sel_results[a]['margin']) for a in ALPHAS if a != 2.0]
    best_other_sel = max(other_sels, key=lambda x: x[1])

    print(f"  Sign selectivity at alpha=2.0: margin={sel_at_2:+d} "
          f"({perfect_sel:.0f}%)")
    print(f"  Best non-2.0 selectivity: alpha={best_other_sel[0]:.2f}, "
          f"margin={best_other_sel[1]:+d}")

    if sel_at_2 > 0 and sel_at_2 >= best_other_sel[1]:
        print("  Sign selectivity supports Born rule selection.")
    elif sel_at_2 > 0:
        print("  Sign selectivity present but not uniquely best at alpha=2.")
    else:
        print("  Sign selectivity ABSENT at alpha=2 -- unexpected.")

    # Check Lyapunov
    print()
    lyap_at_2 = all_results[(2.0, G_VALUES[0])]['lyapunov']
    print(f"  Lyapunov exponent at alpha=2.0 (G={G_VALUES[0]}): {lyap_at_2:.6f}")
    if lyap_at_2 < 0:
        print("  Negative Lyapunov => STABLE fixed point at alpha=2.")
    elif lyap_at_2 > 0:
        print("  Positive Lyapunov => UNSTABLE at alpha=2.")
    else:
        print("  Lyapunov ~ 0 => MARGINAL stability at alpha=2.")

    elapsed = time.time() - t0
    print(f"\n  Total time: {elapsed:.1f}s")

    # ═══════════════════════════════════════════════════════════════
    # PLOTS
    # ═══════════════════════════════════════════════════════════════

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Born Rule from Gravitational Self-Consistency\n'
                     'Does alpha=2 uniquely produce stable backreaction?',
                     fontsize=14, fontweight='bold')

        colors_g = {5.0: '#d62728', 10.0: '#ff7f0e', 50.0: '#2ca02c'}

        # (a) Phi convergence vs alpha
        ax = axes[0, 0]
        for G in G_VALUES:
            vals = [all_results[(a, G)]['phi_chg_mean_last10'] for a in ALPHAS]
            ax.semilogy(ALPHAS, vals, 'o-', color=colors_g[G], label=f'G={G}')
        ax.axvline(2.0, color='gray', linestyle='--', alpha=0.5, label='Born rule')
        ax.set_xlabel('alpha')
        ax.set_ylabel('mean |delta phi| (last 10 steps)')
        ax.set_title('(a) Phi Convergence')
        ax.legend()

        # (b) Energy stability vs alpha
        ax = axes[0, 1]
        for G in G_VALUES:
            vals = [all_results[(a, G)]['energy_std'] for a in ALPHAS]
            ax.semilogy(ALPHAS, vals, 'o-', color=colors_g[G], label=f'G={G}')
        ax.axvline(2.0, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlabel('alpha')
        ax.set_ylabel('std(E) over last 20 steps')
        ax.set_title('(b) Energy Stability')
        ax.legend()

        # (c) Width stability vs alpha
        ax = axes[0, 2]
        for G in G_VALUES:
            vals = [all_results[(a, G)]['width_std'] for a in ALPHAS]
            ax.semilogy(ALPHAS, vals, 'o-', color=colors_g[G], label=f'G={G}')
        ax.axvline(2.0, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlabel('alpha')
        ax.set_ylabel('std(width) over last 20 steps')
        ax.set_title('(c) Width Stability')
        ax.legend()

        # (d) Lyapunov exponent vs alpha
        ax = axes[1, 0]
        for G in G_VALUES:
            vals = [all_results[(a, G)]['lyapunov'] for a in ALPHAS]
            ax.plot(ALPHAS, vals, 'o-', color=colors_g[G], label=f'G={G}')
        ax.axvline(2.0, color='gray', linestyle='--', alpha=0.5)
        ax.axhline(0.0, color='black', linestyle='-', alpha=0.3)
        ax.set_xlabel('alpha')
        ax.set_ylabel('Lyapunov exponent')
        ax.set_title('(d) Lyapunov Exponent (negative = stable)')
        ax.legend()

        # (e) Sign selectivity vs alpha
        ax = axes[1, 1]
        margins = [sel_results[a]['margin'] for a in ALPHAS]
        ax.bar(range(len(ALPHAS)), margins, color='steelblue', alpha=0.8)
        ax.set_xticks(range(len(ALPHAS)))
        ax.set_xticklabels([f'{a:.2f}' for a in ALPHAS], rotation=45, fontsize=8)
        born_idx = ALPHAS.index(2.0)
        ax.get_children()[born_idx].set_color('#d62728')
        ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlabel('alpha')
        ax.set_ylabel('Sign margin (attract - repulse)')
        ax.set_title(f'(e) Sign Selectivity (G={G_sel})')

        # (f) Composite score vs alpha
        ax = axes[1, 2]
        for G in G_VALUES:
            scores_plot = []
            for alpha in ALPHAS:
                r = all_results[(alpha, G)]
                phi_conv = r['phi_chg_mean_last10']
                e_stab = r['energy_std']
                w_stab = r['width_std']
                lyap_abs = abs(r['lyapunov']) if not np.isnan(r['lyapunov']) else 10.0
                sc = (np.log10(max(phi_conv, 1e-20)) +
                      np.log10(max(e_stab, 1e-20)) +
                      np.log10(max(w_stab, 1e-20)) +
                      lyap_abs)
                scores_plot.append(sc)
            ax.plot(ALPHAS, scores_plot, 'o-', color=colors_g[G], label=f'G={G}')
        ax.axvline(2.0, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlabel('alpha')
        ax.set_ylabel('Composite instability score (lower = better)')
        ax.set_title('(f) Composite Stability Score')
        ax.legend()

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\nDone.")


if __name__ == '__main__':
    main()
