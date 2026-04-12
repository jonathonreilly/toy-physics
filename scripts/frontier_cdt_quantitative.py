#!/usr/bin/env python3
"""
CDT Quantitative Comparison — Spectral Dimension Flow
======================================================
Compare our spectral dimension flow to CDT (Ambjorn-Jurkiewicz-Loll 2005).

CDT result: d_s flows from ~1.8 (UV) to ~4.0 (IR) in 4D.
On a 2D lattice: expect d_s flowing from some UV value to ~2.0 in IR.
CDT scaling prediction: d_UV/d_IR = 1/2 (dimensional reduction by factor 2).

METHOD:
  1. Build 2D staggered lattices (side=10,14,18,22) with self-gravity
     G=10, mu2=0.001 (unscreened), 30 CN steps.
  2. Evolve wavepacket with self-gravity to obtain gravitational potential phi.
  3. Construct gravity-modified Laplacian: edge weights w_ij * exp(gamma * phi_avg).
  4. Full eigensolve of L_eff.
  5. Diffusion return probability: P(sigma) = (1/n) Tr(exp(-sigma * L_eff))
  6. Spectral dimension: d_s(sigma) = -2 sigma P'(sigma) / P(sigma)
  7. Fit sigmoid: d_s(sigma) = d_IR - (d_IR - d_UV) / (1 + (sigma/sigma*)^alpha)
  8. Extract d_UV, d_IR, sigma*, alpha for each lattice size.
  9. Check convergence and CDT universality ratio d_UV/d_IR = 1/2.

KEY PHYSICS:
  The spectral dimension probes GEOMETRY via diffusion on the graph Laplacian,
  not the matter Hamiltonian. Gravity modifies effective distances (edge weights)
  which changes the Laplacian spectrum. The Laplacian has a zero eigenvalue
  (constant mode), ensuring d_s saturates at large sigma.

Also: WITH vs WITHOUT gravity to isolate gravity's role.
"""

from __future__ import annotations

import math
import random
import time
import warnings

import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from scipy.optimize import curve_fit


# -- Physics parameters -------------------------------------------------------
MASS = 0.30
MU2 = 0.001       # unscreened -- correct physics
DT = 0.12
G = 10.0
N_STEPS = 30
GAMMA = 1.0        # coupling of potential to metric

# -- Diffusion sampling -------------------------------------------------------
N_SIGMA = 80
SIGMA_MIN = 0.01
SIGMA_MAX = 200.0

# -- Lattice sizes -------------------------------------------------------------
SIDES = [10, 14, 18, 22]


# ==============================================================================
# Graph construction
# ==============================================================================

def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_staggered_lattice(seed=42, side=10):
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


# ==============================================================================
# Physics: Laplacians, Hamiltonian, CN evolution
# ==============================================================================

def _laplacian(pos, adj, n):
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


def _gravity_laplacian(pos, adj, n, phi):
    """Gravity-modified Laplacian: w_ij -> w_ij * exp(gamma * phi_avg).

    Deeper potential wells increase connectivity, effectively making the
    geometry denser near mass concentrations. This is the mechanism by which
    gravity modifies the spectral dimension flow.
    """
    L = lil_matrix((n, n), dtype=float)
    # Normalize phi to avoid overflow: subtract mean so modification is relative
    phi_norm = phi - np.mean(phi)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w0 = 1.0 / max(d, 0.5)
            phi_avg = 0.5 * (phi_norm[i] + phi_norm[j])
            w = w0 * np.exp(GAMMA * phi_avg)
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


def _cn_step(H, n, psi):
    ap = (speye(n, format='csc') + 1j * H * DT / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * DT / 2
    return spsolve(ap, am.dot(psi))


def _gauss_state(pos, src, sigma=1.15):
    center = pos[src]
    rel = pos - center
    psi = np.exp(-0.5 * (rel[:, 0]**2 + rel[:, 1]**2) / sigma**2).astype(complex)
    return psi / np.linalg.norm(psi)


# ==============================================================================
# Self-gravity evolution
# ==============================================================================

def evolve_self_gravity(pos, col, adj, n, src):
    """Evolve Gaussian state with self-gravity for N_STEPS CN steps.
    Returns the final gravitational potential phi."""
    L = _laplacian(pos, adj, n)
    psi = _gauss_state(pos, src)
    phi = np.zeros(n)
    for _ in range(N_STEPS):
        rho = np.abs(psi)**2
        phi = _solve_phi(L, n, G * rho)
        H = _build_H(pos, col, adj, n, MASS, phi)
        psi = _cn_step(H, n, psi)
    return phi


# ==============================================================================
# Spectral dimension from Laplacian eigenvalues
# ==============================================================================

def spectral_dimension_flow(evals, sigmas):
    """Compute d_s(sigma) from eigenvalues of the graph Laplacian.

    P(sigma) = (1/n) sum_i exp(-sigma * lambda_i)
    d_s(sigma) = -2 sigma P'(sigma) / P(sigma)
    """
    # Laplacian eigenvalues >= 0; clip numerical noise
    evals = np.maximum(evals, 0.0)

    ds_values = np.zeros(len(sigmas))
    P_values = np.zeros(len(sigmas))

    for idx, sigma in enumerate(sigmas):
        boltz = np.exp(-sigma * evals)
        P = np.mean(boltz)
        dP = np.mean(-evals * boltz)
        P_values[idx] = P
        if P > 1e-30:
            ds_values[idx] = -2.0 * sigma * dP / P
        else:
            ds_values[idx] = np.nan

    return ds_values, P_values


# ==============================================================================
# Sigmoid fit
# ==============================================================================

def cdt_sigmoid(log_sigma, d_UV, d_IR, log_sigma_star, alpha):
    """d_s(sigma) = d_UV + (d_IR - d_UV) * x^a / (1 + x^a), x = sigma/sigma*

    Rises from d_UV at small sigma to d_IR at large sigma.
    """
    sigma = np.exp(log_sigma)
    sigma_star = np.exp(log_sigma_star)
    ratio = (sigma / sigma_star)**alpha
    return d_UV + (d_IR - d_UV) * ratio / (1.0 + ratio)


def fit_sigmoid(sigmas, ds_values):
    """Fit d_s(sigma) to CDT sigmoid. Only fit the rising portion up to peak."""
    valid = np.isfinite(ds_values) & (ds_values > 0.01)
    if np.sum(valid) < 8:
        return None

    ds_v = ds_values[valid]
    sig_v = sigmas[valid]
    peak_idx = np.argmax(ds_v)

    # Include up to peak + a few points past it
    end_idx = min(peak_idx + 8, len(ds_v))
    ds_fit = ds_v[:end_idx]
    sig_fit = sig_v[:end_idx]

    if len(ds_fit) < 6:
        return None

    log_sigma = np.log(sig_fit)
    peak_ds = float(np.max(ds_fit))
    min_ds = float(ds_fit[0])

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            popt, pcov = curve_fit(
                cdt_sigmoid,
                log_sigma,
                ds_fit,
                p0=[min_ds + 0.01, peak_ds, np.log(sig_fit[max(1, peak_idx // 2)]), 1.0],
                bounds=([0.0, 0.1, np.log(1e-4), 0.05],
                        [10.0, 20.0, np.log(1e4), 10.0]),
                maxfev=20000,
            )
        d_UV, d_IR, log_sigma_star, alpha = popt
        sigma_star = np.exp(log_sigma_star)
        ds_pred = cdt_sigmoid(log_sigma, *popt)
        ss_res = np.sum((ds_fit - ds_pred)**2)
        ss_tot = np.sum((ds_fit - np.mean(ds_fit))**2)
        R2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

        perr = np.sqrt(np.diag(pcov)) if pcov is not None else np.zeros(4)

        return {
            'd_UV': d_UV, 'd_IR': d_IR, 'sigma_star': sigma_star,
            'alpha': alpha, 'R2': R2, 'peak_ds': peak_ds,
            'd_UV_err': perr[0], 'd_IR_err': perr[1],
            'alpha_err': perr[3],
        }
    except Exception:
        return None


# ==============================================================================
# Main
# ==============================================================================

def main():
    t_start = time.time()

    print("=" * 76)
    print("CDT QUANTITATIVE COMPARISON — Spectral Dimension Flow")
    print("=" * 76)
    print()
    print(f"Physics: MASS={MASS}, MU2={MU2} (unscreened), DT={DT}, G={G}, "
          f"N_STEPS={N_STEPS}, GAMMA={GAMMA}")
    print(f"Lattice sizes: {SIDES}")
    print(f"Diffusion: {N_SIGMA} sigma points, [{SIGMA_MIN}, {SIGMA_MAX}] log-spaced")
    print()
    print("CDT reference (Ambjorn, Jurkiewicz, Loll 2005):")
    print("  4D: d_s flows from ~1.8 (UV) to ~4.0 (IR)")
    print("  2D lattice: expect d_s flowing to ~2.0 in IR")
    print("  Universality prediction: d_UV/d_IR = 1/2")
    print()
    print("METHOD: Diffusion on gravity-modified graph Laplacian.")
    print("  1. Evolve matter with self-gravity -> get phi")
    print("  2. Build L_eff with w_ij -> w_ij * exp(gamma * phi_avg)")
    print("  3. P(sigma) = (1/n) Tr(exp(-sigma * L_eff))")
    print("  4. d_s(sigma) = -2 sigma P'(sigma) / P(sigma)")
    print("  5. Fit: d_s = d_UV + (d_IR - d_UV) * x^a / (1 + x^a)")
    print()

    sigmas = np.logspace(np.log10(SIGMA_MIN), np.log10(SIGMA_MAX), N_SIGMA)

    results_grav = {}
    results_free = {}

    # ==========================================================================
    # PART 1: Compute for each lattice size
    # ==========================================================================
    print("-" * 76)
    print("PART 1: Spectral dimension flow for each lattice size")
    print("-" * 76)

    for side in SIDES:
        print(f"\n  --- side={side} ({side*side} nodes) ---")
        t0 = time.time()

        pos, col, adj, n, src = make_staggered_lattice(seed=42, side=side)

        # Free Laplacian (no gravity)
        L_free = _laplacian(pos, adj, n)
        L_free_dense = L_free.toarray()
        evals_free = np.linalg.eigvalsh(L_free_dense)
        ds_free, P_free = spectral_dimension_flow(evals_free, sigmas)

        # Self-gravity evolution to get potential
        phi = evolve_self_gravity(pos, col, adj, n, src)

        # Gravity-modified Laplacian
        L_grav = _gravity_laplacian(pos, adj, n, phi)
        L_grav_dense = L_grav.toarray()
        evals_grav = np.linalg.eigvalsh(L_grav_dense)
        ds_grav, P_grav = spectral_dimension_flow(evals_grav, sigmas)

        elapsed = time.time() - t0
        print(f"  Elapsed: {elapsed:.1f}s")

        # Eigenvalue summary
        evals_free_nz = evals_free[evals_free > 1e-10]
        evals_grav_nz = evals_grav[evals_grav > 1e-10]
        if len(evals_free_nz) > 0:
            print(f"  Free Laplacian: lambda_1={evals_free_nz[0]:.4f} (Fiedler), "
                  f"lambda_max={evals_free_nz[-1]:.4f}")
        if len(evals_grav_nz) > 0:
            print(f"  Grav Laplacian: lambda_1={evals_grav_nz[0]:.4f} (Fiedler), "
                  f"lambda_max={evals_grav_nz[-1]:.4f}")
        print(f"  Potential phi: min={phi.min():.4f}, max={phi.max():.4f}, "
              f"mean={phi.mean():.4f}, std={phi.std():.4f}")

        # Fit sigmoids
        fit_g = fit_sigmoid(sigmas, ds_grav)
        fit_f = fit_sigmoid(sigmas, ds_free)

        results_grav[side] = {
            'ds': ds_grav, 'P': P_grav, 'evals': evals_grav, 'fit': fit_g,
        }
        results_free[side] = {
            'ds': ds_free, 'P': P_free, 'evals': evals_free, 'fit': fit_f,
        }

        # d_s flow table (sampled)
        peak_grav = np.nanmax(ds_grav) if np.any(np.isfinite(ds_grav)) else 0
        peak_free = np.nanmax(ds_free) if np.any(np.isfinite(ds_free)) else 0
        print(f"  Peak d_s: free={peak_free:.4f}, grav={peak_grav:.4f}")

        print(f"\n  {'sigma':>10} | {'d_s(grav)':>10} | {'d_s(free)':>10} | "
              f"{'P(grav)':>12} | {'P(free)':>12}")
        print(f"  {'-' * 62}")
        step = max(1, len(sigmas) // 16)
        for i in range(0, len(sigmas), step):
            s = sigmas[i]
            dg = ds_grav[i]
            df = ds_free[i]
            pg = P_grav[i]
            pf = P_free[i]
            dg_s = f"{dg:>10.4f}" if np.isfinite(dg) else f"{'nan':>10}"
            df_s = f"{df:>10.4f}" if np.isfinite(df) else f"{'nan':>10}"
            print(f"  {s:>10.4f} | {dg_s} | {df_s} | "
                  f"{pg:>12.4e} | {pf:>12.4e}")

        # Print fit results
        for label, fit in [("gravitating", fit_g), ("free", fit_f)]:
            print(f"\n  Sigmoid fit ({label}):")
            if fit is not None:
                print(f"    d_UV      = {fit['d_UV']:.4f} +/- {fit['d_UV_err']:.4f}")
                print(f"    d_IR      = {fit['d_IR']:.4f} +/- {fit['d_IR_err']:.4f}")
                print(f"    sigma*    = {fit['sigma_star']:.4f}")
                print(f"    alpha     = {fit['alpha']:.4f} +/- {fit['alpha_err']:.4f}")
                print(f"    R^2       = {fit['R2']:.6f}")
                print(f"    peak d_s  = {fit['peak_ds']:.4f}")
                if fit['d_IR'] > 0:
                    print(f"    d_UV/d_IR = {fit['d_UV']/fit['d_IR']:.4f}")
            else:
                print(f"    Fit failed")

    # ==========================================================================
    # PART 2: Size convergence table
    # ==========================================================================
    print()
    print("-" * 76)
    print("PART 2: Size convergence of fit parameters")
    print("-" * 76)

    for label, results in [("GRAVITATING", results_grav), ("FREE", results_free)]:
        print(f"\n  {label}:")
        print(f"  {'side':>6} | {'n':>5} | {'d_UV':>8} | {'d_IR':>8} | "
              f"{'d_UV/d_IR':>9} | {'sigma*':>8} | {'alpha':>7} | {'R^2':>8} | {'peak':>8}")
        print(f"  {'-' * 82}")

        for side in SIDES:
            n = side * side
            fit = results[side]['fit']
            if fit is not None:
                ratio = fit['d_UV'] / fit['d_IR'] if fit['d_IR'] > 0 else float('nan')
                print(f"  {side:>6} | {n:>5} | {fit['d_UV']:>8.4f} | {fit['d_IR']:>8.4f} | "
                      f"{ratio:>9.4f} | {fit['sigma_star']:>8.4f} | {fit['alpha']:>7.4f} | "
                      f"{fit['R2']:>8.5f} | {fit['peak_ds']:>8.4f}")
            else:
                print(f"  {side:>6} | {n:>5} | {'FAIL':>8} |")

    # ==========================================================================
    # PART 3: CDT universality check
    # ==========================================================================
    print()
    print("-" * 76)
    print("PART 3: CDT universality -- d_UV/d_IR ratio")
    print("-" * 76)
    print()
    print("CDT prediction: d_UV/d_IR = 1/2 (dimensional reduction by factor 2)")
    print("In 4D CDT: d_UV ~ 2.0, d_IR ~ 4.0, ratio = 0.50")
    print("On 2D lattice: if universal, same ratio should emerge.")
    print()

    ratios_grav = []
    ratios_free = []

    for side in SIDES:
        fg = results_grav[side]['fit']
        ff = results_free[side]['fit']
        r_g = fg['d_UV'] / fg['d_IR'] if fg and fg['d_IR'] > 0 else float('nan')
        r_f = ff['d_UV'] / ff['d_IR'] if ff and ff['d_IR'] > 0 else float('nan')
        if np.isfinite(r_g):
            ratios_grav.append(r_g)
        if np.isfinite(r_f):
            ratios_free.append(r_f)
        r_g_s = f"{r_g:.4f}" if np.isfinite(r_g) else "FAIL"
        r_f_s = f"{r_f:.4f}" if np.isfinite(r_f) else "FAIL"
        print(f"  side={side:>2}: grav ratio={r_g_s}, free ratio={r_f_s}")

    if ratios_grav:
        mean_g = np.mean(ratios_grav)
        std_g = np.std(ratios_grav)
        print(f"\n  Gravitating: mean d_UV/d_IR = {mean_g:.4f} +/- {std_g:.4f}")
        print(f"    CDT target = 0.500, delta = {abs(mean_g - 0.5):.4f}")
    if ratios_free:
        mean_f = np.mean(ratios_free)
        std_f = np.std(ratios_free)
        print(f"  Free:        mean d_UV/d_IR = {mean_f:.4f} +/- {std_f:.4f}")
        print(f"    CDT target = 0.500, delta = {abs(mean_f - 0.5):.4f}")

    # ==========================================================================
    # PART 4: Gravity effect on spectral dimension
    # ==========================================================================
    print()
    print("-" * 76)
    print("PART 4: Effect of gravity on spectral dimension flow")
    print("-" * 76)
    print()
    print(f"  {'side':>6} | {'d_UV shift':>10} | {'d_IR shift':>10} | "
          f"{'peak shift':>10} | {'sigma* shift':>12}")
    print(f"  {'-' * 60}")

    for side in SIDES:
        fg = results_grav[side]['fit']
        ff = results_free[side]['fit']
        if fg and ff:
            dUV = fg['d_UV'] - ff['d_UV']
            dIR = fg['d_IR'] - ff['d_IR']
            dp = fg['peak_ds'] - ff['peak_ds']
            ds_shift = fg['sigma_star'] - ff['sigma_star']
            print(f"  {side:>6} | {dUV:>+10.4f} | {dIR:>+10.4f} | "
                  f"{dp:>+10.4f} | {ds_shift:>+12.4f}")
        else:
            print(f"  {side:>6} | fit(s) failed")

    # ==========================================================================
    # PART 5: Laplacian eigenvalue spectrum
    # ==========================================================================
    print()
    print("-" * 76)
    print("PART 5: Laplacian eigenvalue spectrum summary")
    print("-" * 76)
    print()
    print(f"  {'side':>6} | {'lam1(g)':>9} | {'lam_max(g)':>10} | "
          f"{'lam1(f)':>9} | {'lam_max(f)':>10} | "
          f"{'ratio_1':>8} | {'ratio_max':>9}")
    print(f"  {'-' * 72}")

    for side in SIDES:
        eg = results_grav[side]['evals']
        ef = results_free[side]['evals']
        eg_nz = eg[eg > 1e-10]
        ef_nz = ef[ef > 1e-10]
        if len(eg_nz) > 0 and len(ef_nz) > 0:
            r1 = eg_nz[0] / ef_nz[0]
            rmax = eg_nz[-1] / ef_nz[-1]
            print(f"  {side:>6} | {eg_nz[0]:>9.4f} | {eg_nz[-1]:>10.4f} | "
                  f"{ef_nz[0]:>9.4f} | {ef_nz[-1]:>10.4f} | "
                  f"{r1:>8.4f} | {rmax:>9.4f}")

    # ==========================================================================
    # SUMMARY AND VERDICT
    # ==========================================================================
    print()
    print("=" * 76)
    print("SUMMARY AND VERDICT")
    print("=" * 76)
    print()

    best_side = SIDES[-1]
    fg = results_grav[best_side]['fit']
    ff = results_free[best_side]['fit']

    if fg:
        print(f"Best estimate (side={best_side}, gravitating, mu2={MU2}):")
        print(f"  d_UV      = {fg['d_UV']:.4f} +/- {fg['d_UV_err']:.4f}")
        print(f"  d_IR      = {fg['d_IR']:.4f} +/- {fg['d_IR_err']:.4f}")
        print(f"  sigma*    = {fg['sigma_star']:.4f}")
        print(f"  alpha     = {fg['alpha']:.4f} +/- {fg['alpha_err']:.4f}")
        print(f"  R^2       = {fg['R2']:.6f}")
        if fg['d_IR'] > 0:
            print(f"  d_UV/d_IR = {fg['d_UV']/fg['d_IR']:.4f}")
        print()

    if ff:
        print(f"Best estimate (side={best_side}, free):")
        print(f"  d_UV      = {ff['d_UV']:.4f} +/- {ff['d_UV_err']:.4f}")
        print(f"  d_IR      = {ff['d_IR']:.4f} +/- {ff['d_IR_err']:.4f}")
        if ff['d_IR'] > 0:
            print(f"  d_UV/d_IR = {ff['d_UV']/ff['d_IR']:.4f}")
        print()

    # Convergence check
    print("Convergence check:")
    for label, results in [("grav", results_grav), ("free", results_free)]:
        fits = [(s, results[s]['fit']) for s in SIDES if results[s]['fit'] is not None]
        if len(fits) >= 2:
            d_UV_vals = [f['d_UV'] for _, f in fits]
            d_IR_vals = [f['d_IR'] for _, f in fits]
            if len(d_UV_vals) >= 2:
                conv_UV = abs(d_UV_vals[-1] - d_UV_vals[-2])
                conv_IR = abs(d_IR_vals[-1] - d_IR_vals[-2])
                print(f"  {label}: d_UV change (last two sizes) = {conv_UV:.4f}, "
                      f"d_IR change = {conv_IR:.4f}")
                ratio_vals = [f['d_UV']/f['d_IR'] for _, f in fits if f['d_IR'] > 0]
                if len(ratio_vals) >= 2:
                    conv_ratio = abs(ratio_vals[-1] - ratio_vals[-2])
                    print(f"  {label}: ratio change (last two sizes) = {conv_ratio:.4f}")

    print()

    # CDT criteria
    if fg:
        ratio_g = fg['d_UV'] / fg['d_IR'] if fg['d_IR'] > 0 else float('nan')

        cdt_ratio_match = np.isfinite(ratio_g) and abs(ratio_g - 0.5) < 0.15
        sigmoid_ok = fg['R2'] > 0.90
        alpha_reasonable = 0.3 < fg['alpha'] < 5.0
        flow_present = fg['d_IR'] > fg['d_UV'] + 0.1

        print("CDT criteria (gravitating, largest lattice):")
        print(f"  1. d_UV/d_IR near 0.5:       {'PASS' if cdt_ratio_match else 'FAIL'} "
              f"(ratio = {ratio_g:.4f}, delta = {abs(ratio_g - 0.5):.4f})")
        print(f"  2. Sigmoid shape (R^2>0.90):  {'PASS' if sigmoid_ok else 'FAIL'} "
              f"(R^2 = {fg['R2']:.5f})")
        print(f"  3. alpha reasonable (0.3-5):  {'PASS' if alpha_reasonable else 'FAIL'} "
              f"(alpha = {fg['alpha']:.4f})")
        print(f"  4. Genuine UV->IR flow:       {'PASS' if flow_present else 'FAIL'} "
              f"(d_IR - d_UV = {fg['d_IR'] - fg['d_UV']:.4f})")

        n_pass = sum([cdt_ratio_match, sigmoid_ok, alpha_reasonable, flow_present])
        print()
        print(f"VERDICT: {n_pass}/4 CDT criteria matched")
        if n_pass == 4:
            print("=> STRONG: Quantitative agreement with CDT universality")
        elif n_pass >= 3:
            print("=> GOOD: Qualitative agreement with CDT spectral dimension flow")
        elif n_pass >= 2:
            print("=> PARTIAL: Some features of CDT flow reproduced")
        else:
            print("=> WEAK: Limited agreement with CDT predictions")

        if ff:
            ratio_f = ff['d_UV'] / ff['d_IR'] if ff['d_IR'] > 0 else float('nan')
            if np.isfinite(ratio_g) and np.isfinite(ratio_f):
                grav_closer = abs(ratio_g - 0.5) < abs(ratio_f - 0.5)
                print()
                print(f"Gravity effect on CDT ratio:")
                print(f"  With gravity:    d_UV/d_IR = {ratio_g:.4f} "
                      f"(delta from 0.5 = {abs(ratio_g - 0.5):.4f})")
                print(f"  Without gravity: d_UV/d_IR = {ratio_f:.4f} "
                      f"(delta from 0.5 = {abs(ratio_f - 0.5):.4f})")
                print(f"  Gravity brings ratio {'CLOSER to' if grav_closer else 'FURTHER from'} "
                      f"CDT prediction")
    else:
        print("Sigmoid fit failed for largest lattice -- cannot evaluate CDT criteria")

    total = time.time() - t_start
    print()
    print("=" * 76)
    print(f"Total time: {total:.1f}s")
    print("=" * 76)


if __name__ == "__main__":
    main()
