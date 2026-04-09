#!/usr/bin/env python3
"""
Dispersion at h=0.25: Cone vs Parabola
=======================================
Test whether the small-k_y dispersion becomes cone-like (relativistic)
at finer lattice spacing h=0.25, compared to h=0.5 and h=1.0.

Uses the momentum-space (Fourier) transfer matrix approach:
  M_hat(k_y) = sum_dy M(dy) exp(-i k_y dy h)
  E(k_y) = i ln(M_hat) / h

Then fits:
  Parabolic (Schrodinger): E = a + b k_y^2
  Cone (Klein-Gordon):     E^2 = a + b k_y^2

Hypothesis:
  At h=0.25, the cone fit wins at small k_y (|k_y| < pi/(4h)).

Falsification:
  If parabolic still wins at small k_y at h=0.25.
"""

import numpy as np
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ── Parameters ──────────────────────────────────────────────────────
PHYS_HEIGHT = 15          # physical half-extent in each direction
K_PHASE     = 5.0         # phase wavenumber
P_ATTEN     = 1.0         # 1/L^p attenuation
F_VALLEY    = 0.0         # free space
H_VALUES    = [1.0, 0.5, 0.25]

KERNELS = {
    "gauss": lambda theta: np.exp(-0.8 * theta**2),
    "cos2":  lambda theta: np.cos(theta)**2,
}


def build_transfer_matrix(hw, h, k, p, f, kernel_fn, max_dy=None):
    """Build single-layer transfer matrix M.

    hw = number of lattice sites in each direction from center.
    n_y = 2*hw + 1 total sites.
    """
    n_y = 2 * hw + 1
    M = np.zeros((n_y, n_y), dtype=complex)

    for y_out in range(n_y):
        for y_in in range(n_y):
            dy = (y_out - hw) - (y_in - hw)
            if max_dy is not None and abs(dy) > max_dy:
                continue

            phys_dy = dy * h
            L = np.sqrt(h**2 + phys_dy**2)
            S = L * (1.0 - f)
            theta = np.arctan2(abs(phys_dy), h)

            w = kernel_fn(theta)
            amplitude = np.exp(1j * k * S) * w * h / (L ** p)
            M[y_out, y_in] = amplitude

    return M


def momentum_space_dispersion(M, hw, h, n_k=200):
    """Compute E(k_y) via Fourier transform of the Toeplitz transfer matrix.

    Returns k_y array and complex E array.
    """
    n_y = 2 * hw + 1
    center_row = M[hw, :]  # row for y_out = 0
    y_positions = np.arange(n_y) - hw  # [-hw, ..., +hw]

    k_y_range = np.linspace(0, np.pi / h, n_k)
    M_hat = np.zeros(n_k, dtype=complex)

    for ik, ky in enumerate(k_y_range):
        M_hat[ik] = np.sum(center_row * np.exp(-1j * ky * y_positions * h))

    E_ky = 1j * np.log(M_hat) / h
    return k_y_range, E_ky, M_hat


def r_squared(y_true, y_pred):
    """Compute R^2."""
    ss_res = np.sum((y_true - y_pred)**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    if ss_tot < 1e-30:
        return -1.0
    return 1.0 - ss_res / ss_tot


def fit_both(k_y, E_real):
    """Fit parabolic E = a + b*k_y^2 and cone E^2 = a + b*k_y^2.

    Returns dict with R^2 for each.
    """
    mask = np.isfinite(k_y) & np.isfinite(E_real) & (k_y > 1e-10)
    ky = k_y[mask]
    Er = E_real[mask]

    results = {"parabolic_R2": -1.0, "cone_R2": -1.0,
               "parabolic_params": None, "cone_params": None}

    if len(ky) < 3:
        return results

    # Parabolic: E = a + b*k_y^2
    try:
        def para(k2, a, b):
            return a + b * k2
        popt, _ = curve_fit(para, ky**2, Er, p0=[Er[0], 0.1], maxfev=5000)
        pred = para(ky**2, *popt)
        results["parabolic_R2"] = r_squared(Er, pred)
        results["parabolic_params"] = popt
    except Exception:
        pass

    # Cone: E^2 = a + b*k_y^2  =>  fit E^2 vs k_y^2
    try:
        E2 = Er**2
        def cone(k2, a, b):
            return a + b * k2
        popt, _ = curve_fit(cone, ky**2, E2, p0=[E2[0], 1.0], maxfev=5000)
        pred = cone(ky**2, *popt)
        results["cone_R2"] = r_squared(E2, pred)
        results["cone_params"] = popt
    except Exception:
        pass

    return results


def run_experiment():
    print("=" * 90)
    print("DISPERSION AT h=0.25: CONE vs PARABOLA")
    print("=" * 90)
    print(f"\nPhysical half-extent: {PHYS_HEIGHT}")
    print(f"k={K_PHASE}, p={P_ATTEN}, f={F_VALLEY}")
    print(f"h values: {H_VALUES}")

    for h in H_VALUES:
        hw = int(round(PHYS_HEIGHT / h))
        n_y = 2 * hw + 1
        max_d = max(1, int(round(3 / h)))
        small_k_cut = np.pi / (4 * h)
        print(f"\n  h={h}: hw={hw}, n_y={n_y}, max_dy={max_d}, small_k_cut={small_k_cut:.3f}")

    # Collect results for summary table
    summary_rows = []

    for kernel_name, kernel_fn in KERNELS.items():
        for h in H_VALUES:
            hw = int(round(PHYS_HEIGHT / h))
            n_y = 2 * hw + 1
            max_d = max(1, int(round(3 / h)))
            small_k_cut = np.pi / (4 * h)

            print(f"\n{'─' * 90}")
            print(f"KERNEL: {kernel_name}   h={h}   n_y={n_y}   max_dy={max_d}")
            print(f"{'─' * 90}")

            # Build transfer matrix
            M = build_transfer_matrix(hw, h, K_PHASE, P_ATTEN, F_VALLEY,
                                       kernel_fn, max_dy=max_d)

            print(f"  ||M||_F = {np.linalg.norm(M, 'fro'):.6f}")

            # Momentum-space dispersion
            k_y, E_ky, M_hat = momentum_space_dispersion(M, hw, h, n_k=300)
            E_real = E_ky.real

            # Global fit (all k_y > 0)
            global_fit = fit_both(k_y, E_real)

            # Small-k fit (|k_y| < pi/(4h))
            small_mask = k_y < small_k_cut
            small_fit = fit_both(k_y[small_mask], E_real[small_mask])

            # Print sample dispersion data
            print(f"\n  Sample E(k_y) [every 30th point]:")
            print(f"  {'k_y':>8}  {'Re(E)':>12}  {'Im(E)':>12}  {'|M_hat|':>10}")
            for i in range(0, len(k_y), 30):
                print(f"  {k_y[i]:8.3f}  {E_real[i]:12.4f}  {E_ky[i].imag:12.4f}  "
                      f"{np.abs(M_hat[i]):10.6f}")

            # Print fit results
            print(f"\n  GLOBAL fits (all k_y):")
            print(f"    Parabolic  R^2 = {global_fit['parabolic_R2']:.6f}  "
                  f"params = {global_fit['parabolic_params']}")
            print(f"    Cone       R^2 = {global_fit['cone_R2']:.6f}  "
                  f"params = {global_fit['cone_params']}")
            g_winner = "CONE" if global_fit['cone_R2'] > global_fit['parabolic_R2'] else "PARABOLIC"
            g_margin = abs(global_fit['cone_R2'] - global_fit['parabolic_R2'])
            print(f"    Winner: {g_winner} (margin: {g_margin:.6f})")

            print(f"\n  SMALL-k fits (k_y < {small_k_cut:.3f}):")
            n_small = np.sum(small_mask)
            print(f"    Points in small-k region: {n_small}")
            print(f"    Parabolic  R^2 = {small_fit['parabolic_R2']:.6f}  "
                  f"params = {small_fit['parabolic_params']}")
            print(f"    Cone       R^2 = {small_fit['cone_R2']:.6f}  "
                  f"params = {small_fit['cone_params']}")
            s_winner = "CONE" if small_fit['cone_R2'] > small_fit['parabolic_R2'] else "PARABOLIC"
            s_margin = abs(small_fit['cone_R2'] - small_fit['parabolic_R2'])
            print(f"    Winner: {s_winner} (margin: {s_margin:.6f})")

            summary_rows.append({
                "h": h,
                "kernel": kernel_name,
                "g_para": global_fit['parabolic_R2'],
                "g_cone": global_fit['cone_R2'],
                "s_para": small_fit['parabolic_R2'],
                "s_cone": small_fit['cone_R2'],
                "g_winner": g_winner,
                "s_winner": s_winner,
            })

    # ── Summary Table ──────────────────────────────────────────────
    print(f"\n\n{'=' * 90}")
    print("SUMMARY TABLE")
    print(f"{'=' * 90}")
    print(f"\n{'h':>5}  {'kernel':>8}  {'glob_para_R2':>12}  {'glob_cone_R2':>12}  "
          f"{'sm_para_R2':>12}  {'sm_cone_R2':>12}  {'glob_win':>10}  {'sm_win':>10}")
    print(f"{'─'*5}  {'─'*8}  {'─'*12}  {'─'*12}  {'─'*12}  {'─'*12}  {'─'*10}  {'─'*10}")

    for r in summary_rows:
        print(f"{r['h']:5.2f}  {r['kernel']:>8}  {r['g_para']:12.6f}  {r['g_cone']:12.6f}  "
              f"{r['s_para']:12.6f}  {r['s_cone']:12.6f}  {r['g_winner']:>10}  {r['s_winner']:>10}")

    # ── Trend Analysis ─────────────────────────────────────────────
    print(f"\n\n{'=' * 90}")
    print("TREND ANALYSIS: Does cone gain as h -> 0?")
    print(f"{'=' * 90}")

    for kernel_name in KERNELS:
        print(f"\n  Kernel: {kernel_name}")
        rows = [r for r in summary_rows if r['kernel'] == kernel_name]

        # Small-k cone advantage = cone_R2 - para_R2
        print(f"    {'h':>5}  {'cone_R2 - para_R2 (small-k)':>30}  {'cone_R2 - para_R2 (global)':>30}")
        for r in rows:
            sm_adv = r['s_cone'] - r['s_para']
            gl_adv = r['g_cone'] - r['g_para']
            print(f"    {r['h']:5.2f}  {sm_adv:30.6f}  {gl_adv:30.6f}")

        # Check monotonicity of cone advantage
        sm_advs = [r['s_cone'] - r['s_para'] for r in rows]
        if len(sm_advs) >= 2:
            if all(sm_advs[i+1] > sm_advs[i] for i in range(len(sm_advs)-1)):
                print(f"    => Cone advantage INCREASING with finer h (relativistic trend)")
            elif all(sm_advs[i+1] < sm_advs[i] for i in range(len(sm_advs)-1)):
                print(f"    => Cone advantage DECREASING with finer h (Schrodinger wins)")
            else:
                print(f"    => Non-monotonic trend")

    # ── Hypothesis Verdict ─────────────────────────────────────────
    print(f"\n\n{'=' * 90}")
    print("HYPOTHESIS VERDICT")
    print(f"{'=' * 90}")

    h025_rows = [r for r in summary_rows if r['h'] == 0.25]
    any_cone_wins = any(r['s_winner'] == 'CONE' for r in h025_rows)

    if any_cone_wins:
        winners = [r['kernel'] for r in h025_rows if r['s_winner'] == 'CONE']
        print(f"\n  SUPPORTED: At h=0.25, cone wins at small k_y for: {', '.join(winners)}")
        print(f"  The continuum limit appears RELATIVISTIC for these kernels.")
    else:
        print(f"\n  FALSIFIED: Parabolic still wins at small k_y at h=0.25 for all kernels.")
        print(f"  The model is NON-RELATIVISTIC (Schrodinger-like).")

    # Check if cone is at least gaining
    for kernel_name in KERNELS:
        rows = [r for r in summary_rows if r['kernel'] == kernel_name]
        sm_advs = [r['s_cone'] - r['s_para'] for r in rows]
        if len(sm_advs) >= 2 and sm_advs[-1] > sm_advs[0]:
            print(f"  Note: {kernel_name} cone advantage is growing ({sm_advs[0]:.6f} -> {sm_advs[-1]:.6f})")
            print(f"    Even if parabolic wins now, cone may prevail at smaller h.")

    print(f"\n{'=' * 90}")
    print("EXPERIMENT COMPLETE")
    print(f"{'=' * 90}")


if __name__ == "__main__":
    run_experiment()
