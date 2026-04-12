#!/usr/bin/env python3
"""
Full Multifractal f(alpha) Spectrum at Self-Gravity Critical Point
==================================================================

Compute the full multifractal spectrum f(alpha) via Legendre transform
of tau(q) = D_q*(q-1) to determine if the gravitational localization
transition belongs to a known Anderson universality class.

Protocol:
  1. Random geometric graphs (side=6,8,10,12), evolve under self-gravity
     at G=1 (extended), G=2 (critical), G=5 (localized) for 30 steps.
  2. Compute generalized dimensions D_q for extended q range including
     negative q (probing rare low-density regions).
  3. f(alpha) via Legendre transform: alpha = dtau/dq, f = q*alpha - tau.
  4. Compare spectrum shape to known Anderson universality classes.
"""

from __future__ import annotations

import math
import random
import time

import numpy as np
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

# ── Physics constants ──────────────────────────────────────────────────
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_ITER = 30

# ── Sweep parameters ──────────────────────────────────────────────────
G_VALUES = [1, 2, 5]
SIDES = [6, 8, 10, 12]
Q_VALUES = [-5.0, -4.0, -3.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
SEED = 42


# ── Graph construction ─────────────────────────────────────────────────
def _add_edge(adj, i, j):
    if i == j:
        return
    adj.setdefault(i, set()).add(j)
    adj.setdefault(j, set()).add(i)


def _finalize_adj(adj_sets):
    return {i: sorted(list(nbs)) for i, nbs in adj_sets.items()}


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
    pos = np.array(coords, dtype=float)
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
                    _add_edge(adj, a, b)
    return pos, col, _finalize_adj(adj)


# ── Physics operators ──────────────────────────────────────────────────
def laplacian(pos, adj, n):
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


def solve_phi(lap, rho):
    if np.allclose(rho, 0.0):
        return np.zeros_like(rho)
    A = (lap + MU2 * speye(lap.shape[0], format="csr")).tocsc()
    return spsolve(A, rho).astype(float)


def build_hamiltonian(pos, colors, adj, n, phi):
    H = lil_matrix((n, n), dtype=complex)
    parity = np.where(colors == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * parity)
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


def cn_step(H, psi, n):
    ap = (speye(n, format="csc") + 1j * H * DT / 2).tocsc()
    am = speye(n, format="csr") - 1j * H * DT / 2
    return spsolve(ap, am.dot(psi))


def gauss_state(pos, n, sigma=1.15):
    center = np.mean(pos, axis=0)
    rel = pos - center
    psi = np.exp(-0.5 * np.sum(rel**2, axis=1) / sigma**2).astype(complex)
    norm = np.linalg.norm(psi)
    return psi / norm if norm > 0 else psi


# ── Self-gravity evolution ─────────────────────────────────────────────
def evolve_self_gravity(pos, col, adj, n, G):
    lap = laplacian(pos, adj, n)
    psi = gauss_state(pos, n)
    for _ in range(N_ITER):
        rho = np.abs(psi)**2
        phi = solve_phi(lap, G * rho)
        H = build_hamiltonian(pos, col, adj, n, phi)
        psi = cn_step(H, psi, n)
    return psi


# ── Multifractal analysis ─────────────────────────────────────────────
def compute_ipr(psi, q_values):
    """Compute IPR_q = sum_i rho_i^q for each q."""
    rho = np.abs(psi)**2
    rho_sum = np.sum(rho)
    if rho_sum <= 0:
        return {q: 0.0 for q in q_values}
    rho /= rho_sum

    # Regularize: clamp tiny values to avoid 0^negative
    rho_reg = np.clip(rho, 1e-30, None)

    result = {}
    for q in q_values:
        if q == 1.0:
            # Shannon entropy: S = -sum rho*log(rho)
            mask = rho > 1e-30
            result[q] = float(-np.sum(rho[mask] * np.log(rho[mask])))
        elif q == 0.0:
            # IPR_0 = number of sites with non-zero weight
            result[q] = float(np.sum(rho > 1e-15))
        else:
            result[q] = float(np.sum(rho_reg**q))
    return result


def fit_tau_q(ipr_by_size, q_values):
    """
    Fit tau_q from IPR_q ~ N^{-tau_q} across sizes.
    For q=1, use Shannon entropy S ~ D_1 * ln(N).
    For q=0, use log(support) ~ D_0 * log(N).
    Returns dict q -> tau_q.
    """
    sizes = sorted(ipr_by_size.keys())
    if len(sizes) < 2:
        return {q: 0.0 for q in q_values}

    log_n = np.log(np.array(sizes, dtype=float))
    tau = {}

    for q in q_values:
        if q == 1.0:
            # S = D_1 * ln(N) + const => slope = D_1 = tau_1 / (q-1) but q-1=0
            # Actually tau_1 = lim_{q->1} D_q*(q-1). Use S ~ D_1 * ln(N).
            entropies = np.array([ipr_by_size[n][q] for n in sizes])
            A = np.vstack([log_n, np.ones_like(log_n)]).T
            result = np.linalg.lstsq(A, entropies, rcond=None)
            tau[q] = float(result[0][0])  # This is D_1
        elif q == 0.0:
            # IPR_0 = support ~ N^{D_0} => log(support) = D_0 * log(N)
            log_support = np.log(np.array([ipr_by_size[n][q] for n in sizes]))
            A = np.vstack([log_n, np.ones_like(log_n)]).T
            result = np.linalg.lstsq(A, log_support, rcond=None)
            tau[q] = float(result[0][0])  # This is D_0 = tau_0 / (0-1) => tau_0 = -D_0
            # Actually tau_0 = D_0 * (0-1) = -D_0. Store D_0 here, convert later.
        else:
            log_ipr = np.log(np.array([max(ipr_by_size[n][q], 1e-300) for n in sizes]))
            A = np.vstack([log_n, np.ones_like(log_n)]).T
            result = np.linalg.lstsq(A, log_ipr, rcond=None)
            tau[q] = float(-result[0][0])  # -slope = tau_q

    return tau


def compute_dq_and_tau(ipr_by_size, q_values):
    """Compute D_q and properly defined tau_q = D_q * (q-1)."""
    raw_tau = fit_tau_q(ipr_by_size, q_values)

    dq = {}
    tau_proper = {}

    for q in q_values:
        if q == 1.0:
            dq[q] = raw_tau[q]  # D_1 from entropy fit
            tau_proper[q] = 0.0  # tau_1 = D_1 * 0 = 0 by definition
        elif q == 0.0:
            dq[q] = raw_tau[q]  # D_0 from support fit
            tau_proper[q] = -dq[q]  # tau_0 = D_0 * (-1)
        else:
            dq[q] = raw_tau[q] / (q - 1.0)
            tau_proper[q] = raw_tau[q]  # already tau_q

    return dq, tau_proper


def legendre_transform(q_values, tau_values):
    """
    Compute f(alpha) via Legendre transform of tau(q).
    alpha(q) = dtau/dq (numerical derivative)
    f(q) = q * alpha(q) - tau(q)

    Returns arrays: q_arr, alpha_arr, f_arr
    """
    q_arr = np.array(q_values)
    tau_arr = np.array([tau_values[q] for q in q_values])

    # Numerical derivative dtau/dq using central differences
    alpha_arr = np.gradient(tau_arr, q_arr)

    # Legendre transform
    f_arr = q_arr * alpha_arr - tau_arr

    return q_arr, alpha_arr, f_arr


def analyze_spectrum(alpha_arr, f_arr, label):
    """Analyze the f(alpha) spectrum shape."""
    # Find peak (maximum of f)
    peak_idx = np.argmax(f_arr)
    alpha_0 = alpha_arr[peak_idx]
    f_max = f_arr[peak_idx]

    # Width
    alpha_min = np.min(alpha_arr)
    alpha_max = np.max(alpha_arr)
    delta_alpha = alpha_max - alpha_min

    # Check for parabolic shape: fit parabola around peak
    # f(alpha) ~ f_max - C*(alpha - alpha_0)^2
    valid = f_arr > -10  # exclude extreme tails
    if np.sum(valid) >= 3:
        alpha_v = alpha_arr[valid]
        f_v = f_arr[valid]
        # Fit: f = a*(alpha - alpha_0)^2 + b*(alpha - alpha_0) + c
        x = alpha_v - alpha_0
        A = np.vstack([x**2, x, np.ones_like(x)]).T
        result = np.linalg.lstsq(A, f_v, rcond=None)
        curvature = result[0][0]
        residual = np.sqrt(np.mean((f_v - A @ result[0])**2))
    else:
        curvature = 0.0
        residual = float('inf')

    # Asymmetry: compare left and right width from peak
    left_width = alpha_0 - alpha_min
    right_width = alpha_max - alpha_0
    asymmetry = (right_width - left_width) / max(delta_alpha, 1e-10)

    return {
        'label': label,
        'alpha_0': alpha_0,
        'f_max': f_max,
        'alpha_min': alpha_min,
        'alpha_max': alpha_max,
        'delta_alpha': delta_alpha,
        'curvature': curvature,
        'parabolic_residual': residual,
        'asymmetry': asymmetry,
        'left_width': left_width,
        'right_width': right_width,
    }


# ── Main ───────────────────────────────────────────────────────────────
def main():
    t0 = time.time()
    print("=" * 80)
    print("FULL MULTIFRACTAL f(alpha) SPECTRUM AT SELF-GRAVITY CRITICAL POINT")
    print("=" * 80)
    print(f"MASS={MASS}, MU2={MU2}, DT={DT}, N_ITER={N_ITER}")
    print(f"G values: {G_VALUES}  (extended / critical / localized)")
    print(f"Sides: {SIDES} => N = {[s*s for s in SIDES]}")
    print(f"q values: {Q_VALUES}")
    print(f"Seed: {SEED}")
    print()

    all_dq = {}
    all_tau = {}
    all_spectra = {}
    all_analysis = {}

    for G in G_VALUES:
        print(f"{'='*80}")
        print(f"  G = {G}  ({'extended' if G == 1 else 'CRITICAL' if G == 2 else 'localized'})")
        print(f"{'='*80}")

        # ipr_by_size[N] = {q: IPR_q}
        ipr_by_size = {}

        for side in SIDES:
            n = side * side
            pos, col, adj = make_random_geometric(SEED, side)
            actual_n = pos.shape[0]

            psi = evolve_self_gravity(pos, col, adj, actual_n, float(G))
            ipr = compute_ipr(psi, Q_VALUES)
            ipr_by_size[n] = ipr

            # Monitor
            rho = np.abs(psi)**2
            rho /= np.sum(rho)
            ipr2 = np.sum(rho**2)
            print(f"  side={side:2d}  N={n:3d}  IPR_2={ipr2:.6f}  "
                  f"max(rho)={np.max(rho):.4f}  support={np.sum(rho > 1e-6):d}")

        # Compute D_q and tau_q
        dq, tau = compute_dq_and_tau(ipr_by_size, Q_VALUES)
        all_dq[G] = dq
        all_tau[G] = tau

        # Print D_q
        print()
        print("  D_q spectrum:")
        for q in Q_VALUES:
            marker = " <-- D_2" if q == 2.0 else ""
            print(f"    q={q:+5.1f}:  D_q = {dq[q]:+7.4f}  tau_q = {tau[q]:+7.4f}{marker}")

        # Legendre transform -> f(alpha)
        q_arr, alpha_arr, f_arr = legendre_transform(Q_VALUES, tau)
        all_spectra[G] = (q_arr, alpha_arr, f_arr)

        print()
        print("  f(alpha) spectrum:")
        print(f"    {'q':>6s}  {'alpha':>8s}  {'f(alpha)':>10s}")
        print(f"    {'-'*6}  {'-'*8}  {'-'*10}")
        for i, q in enumerate(Q_VALUES):
            print(f"    {q:+6.1f}  {alpha_arr[i]:+8.4f}  {f_arr[i]:+10.4f}")

        # Analyze spectrum
        info = analyze_spectrum(alpha_arr, f_arr, f"G={G}")
        all_analysis[G] = info

        print()
        print(f"  Spectrum analysis:")
        print(f"    alpha_0 (peak)     = {info['alpha_0']:.4f}")
        print(f"    f_max              = {info['f_max']:.4f}")
        print(f"    Delta_alpha (width)= {info['delta_alpha']:.4f}")
        print(f"    Asymmetry          = {info['asymmetry']:+.4f}  "
              f"(left={info['left_width']:.4f}, right={info['right_width']:.4f})")
        print(f"    Curvature          = {info['curvature']:.4f}")
        print(f"    Parabolic residual = {info['parabolic_residual']:.4f}")
        print()

    # ── Comparison across G values ─────────────────────────────────────
    print()
    print("=" * 80)
    print("COMPARISON: D_q SPECTRA ACROSS G")
    print("=" * 80)
    header = f"{'q':>6s}"
    for G in G_VALUES:
        header += f"  {'G='+str(G):>10s}"
    print(header)
    print("-" * (6 + 12 * len(G_VALUES)))
    for q in Q_VALUES:
        line = f"{q:+6.1f}"
        for G in G_VALUES:
            line += f"  {all_dq[G][q]:+10.4f}"
        print(line)

    # ── f(alpha) comparison ────────────────────────────────────────────
    print()
    print("=" * 80)
    print("COMPARISON: f(alpha) SPECTRA")
    print("=" * 80)
    header = f"{'q':>6s}"
    for G in G_VALUES:
        header += f"  {'a(G='+str(G)+')':>10s}  {'f(G='+str(G)+')':>10s}"
    print(header)
    print("-" * (6 + 22 * len(G_VALUES)))
    for i, q in enumerate(Q_VALUES):
        line = f"{q:+6.1f}"
        for G in G_VALUES:
            _, alpha, f = all_spectra[G]
            line += f"  {alpha[i]:+10.4f}  {f[i]:+10.4f}"
        print(line)

    # ── Spectrum shape summary ─────────────────────────────────────────
    print()
    print("=" * 80)
    print("SPECTRUM SHAPE ANALYSIS")
    print("=" * 80)
    print(f"{'G':>4s}  {'alpha_0':>8s}  {'f_max':>6s}  {'Delta_a':>8s}  "
          f"{'Asym':>6s}  {'Curv':>8s}  {'Resid':>6s}  {'Shape':>20s}")
    print("-" * 80)

    for G in G_VALUES:
        info = all_analysis[G]
        # Classify shape
        if info['delta_alpha'] < 0.3:
            shape = "DELTA (localized)"
        elif abs(info['asymmetry']) < 0.15 and info['parabolic_residual'] < 0.5:
            shape = "PARABOLIC (standard)"
        elif info['asymmetry'] > 0.15:
            shape = "RIGHT-SKEWED"
        elif info['asymmetry'] < -0.15:
            shape = "LEFT-SKEWED"
        else:
            shape = "BROAD (anomalous)"

        print(f"{G:4d}  {info['alpha_0']:+8.4f}  {info['f_max']:+6.3f}  "
              f"{info['delta_alpha']:8.4f}  {info['asymmetry']:+6.3f}  "
              f"{info['curvature']:+8.4f}  {info['parabolic_residual']:6.3f}  "
              f"{shape:>20s}")

    # ── Anderson universality class comparison ─────────────────────────
    print()
    print("=" * 80)
    print("ANDERSON UNIVERSALITY CLASS COMPARISON")
    print("=" * 80)

    crit = all_analysis.get(2, None)
    dq_crit = all_dq.get(2, None)
    if crit and dq_crit:
        d2 = dq_crit[2.0]
        d0 = dq_crit[0.0]
        d1 = dq_crit[1.0]

        print()
        print("Known Anderson transitions (reference values):")
        print("  3D Orthogonal (GOE):  D_2 ~ 1.3,  alpha_0 ~ 4.0,  Delta_alpha ~ 6")
        print("  3D Unitary (GUE):     D_2 ~ 1.3,  alpha_0 ~ 3.2,  Delta_alpha ~ 4")
        print("  3D Symplectic (GSE):  D_2 ~ 1.3,  alpha_0 ~ 2.8,  Delta_alpha ~ 3")
        print("  2D Unitary (QHE):     D_2 ~ 1.0,  alpha_0 ~ 2.3,  weak multifractality")
        print("  2D Symplectic:        D_2 ~ 1.0,  alpha_0 ~ 2.2")
        print()
        print(f"This model (2D staggered + self-gravity, G=2):")
        print(f"  D_0 = {d0:.4f}  (information dimension)")
        print(f"  D_1 = {d1:.4f}  (entropy dimension)")
        print(f"  D_2 = {d2:.4f}  (correlation dimension)")
        print(f"  alpha_0 = {crit['alpha_0']:.4f}")
        print(f"  Delta_alpha = {crit['delta_alpha']:.4f}")
        print(f"  Asymmetry = {crit['asymmetry']:+.4f}")
        print(f"  Parabolic residual = {crit['parabolic_residual']:.4f}")

        print()
        print("Classification:")

        # Check if D_q monotonically decreasing
        dq_vals = [dq_crit[q] for q in Q_VALUES if q > 0 and q != 1.0]
        q_pos = [q for q in Q_VALUES if q > 0 and q != 1.0]
        monotonic = all(dq_vals[i] >= dq_vals[i+1] for i in range(len(dq_vals)-1))

        print(f"  D_q monotonically decreasing (q>0): {monotonic}")

        if d2 < 0.15:
            print("  => LOCALIZED PHASE (D_2 ~ 0)")
            print("  Not at a critical point.")
        elif d2 > 1.5:
            print("  => EXTENDED PHASE (D_2 ~ d)")
            print("  Not at a critical point.")
        elif 0.8 < d2 < 1.2 and crit['delta_alpha'] > 2:
            print("  => Consistent with 2D UNITARY CLASS (QHE-like)")
            print("  D_2 ~ 1, moderate multifractal width.")
        elif d2 < 0.8 and monotonic and crit['delta_alpha'] > 1:
            print("  => NOVEL UNIVERSALITY CLASS")
            print(f"  D_2 = {d2:.3f} is below known 2D Anderson values.")
            print("  Strong multifractality with anomalously small D_2.")
            print("  Self-gravity introduces a new localization mechanism.")
        elif d2 < 0.8 and crit['delta_alpha'] < 1:
            print("  => STRONG LOCALIZATION (approaching delta function)")
            print("  Narrow spectrum suggests near-complete localization.")
        else:
            print("  => ANOMALOUS CRITICAL POINT")
            print(f"  D_2 = {d2:.3f} does not match standard Anderson classes.")

        # Singularity strength analysis
        print()
        print("Singularity strength analysis:")
        print(f"  alpha_min = {crit['alpha_min']:.4f}  (densest regions)")
        print(f"  alpha_max = {crit['alpha_max']:.4f}  (rarefied regions)")
        print(f"  alpha_0   = {crit['alpha_0']:.4f}  (typical)")
        if crit['alpha_0'] > 0:
            print(f"  alpha_0/d  = {crit['alpha_0']/2.0:.4f}  (ratio to spatial dim)")

    # ── Evolution across G ─────────────────────────────────────────────
    print()
    print("=" * 80)
    print("EVOLUTION OF SPECTRUM WITH G")
    print("=" * 80)
    print("Expected: spectrum narrows from extended -> critical -> localized")
    print()
    for G in G_VALUES:
        info = all_analysis[G]
        d2 = all_dq[G][2.0]
        print(f"  G={G}: Delta_alpha={info['delta_alpha']:.4f}, "
              f"alpha_0={info['alpha_0']:.4f}, D_2={d2:.4f}")

    # Check narrowing
    widths = [all_analysis[G]['delta_alpha'] for G in G_VALUES]
    if len(widths) >= 2:
        if widths[-1] < widths[0]:
            print("  => Spectrum NARROWS with increasing G (expected for localization)")
        else:
            print("  => Spectrum does NOT narrow with G (unexpected)")

    # ── Final verdict ──────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    if crit and dq_crit:
        d2 = dq_crit[2.0]
        da = crit['delta_alpha']

        print(f"D_2 = {d2:.4f} at G=2 (critical coupling)")
        print(f"Delta_alpha = {da:.4f} (multifractal width)")
        print()

        if d2 < 0.15:
            print("The system is LOCALIZED at G=2. The critical point may be at lower G.")
        elif d2 > 1.5:
            print("The system is EXTENDED at G=2. The critical point may be at higher G.")
        elif 0.3 < d2 < 0.8 and monotonic:
            print("CONCLUSION: The self-gravity localization at G=2 shows ANOMALOUS")
            print("MULTIFRACTALITY that does NOT match any known Anderson class:")
            print(f"  - D_2 = {d2:.3f} is well below the 2D Anderson value (~1.0)")
            print(f"  - The spectrum width Delta_alpha = {da:.3f} indicates genuine multifractality")
            print("  - D_q is monotonically decreasing, as at an Anderson critical point")
            print("  - But the anomalously low D_2 suggests a GRAVITY-DRIVEN universality class")
            print()
            print("This is a NEW prediction: self-gravitating quantum walks on random")
            print("geometric graphs define a novel multifractal critical point distinct")
            print("from all three Wigner-Dyson classes (orthogonal, unitary, symplectic).")
        elif 0.8 < d2 < 1.2:
            print("CONCLUSION: D_2 is consistent with 2D Anderson transition.")
            print("Further analysis of symmetry class needed to determine GOE/GUE/GSE.")
        else:
            print(f"CONCLUSION: D_2 = {d2:.3f} -- anomalous value.")
            print("The transition may represent a new universality class.")

    elapsed = time.time() - t0
    print(f"\nElapsed: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
