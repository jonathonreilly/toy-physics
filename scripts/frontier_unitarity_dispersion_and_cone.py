#!/usr/bin/env python3
"""
Unitarity via Layer Normalization: Dispersion & Light Cone
==========================================================
Hypothesis:
  Layer normalization fixes the continuum limit (clean dispersion)
  and might produce a light cone (finite signal speed).

Part 1 - Normalized dispersion relation:
  Build single-layer transfer matrix M, normalize by spectral radius,
  then extract dispersion from PHASE: E(k_y) = arg(lambda(k_y)) / h.
  With |lambda| <= 1, E is purely real (no imaginary growth part).
  Fit E vs k_y^2 (Schrodinger) and E^2 vs k_y^2 (Klein-Gordon).
  Test at h = 1.0, 0.5, 0.25 for both Euclidean and Lorentzian kernels.

Part 2 - Signal speed from normalized propagator:
  Propagate delta source through normalized propagator for 40 layers.
  At each layer n, find edge of signal (y where |psi| drops below threshold).
  Track y_edge(n). Linear growth => light cone with speed c = y_edge/n.
  Compare un-normalized (diffusive, y_edge ~ sqrt(n)) vs normalized.
  Test for all four kernels: uniform, cos, cos^2, exp(-0.8*theta^2).

Falsification:
  If signal still fills the lattice even with normalization.
"""

import numpy as np
from numpy.linalg import eig
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ── Parameters ──────────────────────────────────────────────────────
H_TRANSVERSE = 15          # half-height: y in [-H, +H], so 2H+1 = 31 sites (Part 1)
H_SIGNAL     = 30          # half-height for signal speed: 2H+1 = 61 sites (Part 2)
K_PHASE      = 5.0         # phase wavenumber k
P_ATTEN      = 1.0         # 1/L^p attenuation (p=1 for 2D)
F_VALLEY     = 0.0         # f=0 free space
H_VALUES     = [1.0, 0.5, 0.25]
N_LAYERS     = 40          # layers for signal speed test
THRESHOLD    = 1e-3         # edge detection threshold

KERNELS = {
    "uniform": lambda theta: np.ones_like(theta),
    "cos":     lambda theta: np.cos(theta),
    "cos2":    lambda theta: np.cos(theta)**2,
    "gauss":   lambda theta: np.exp(-0.8 * theta**2),
}


def build_transfer_matrix(H, h, k, p, f, kernel_fn):
    """Build the single-layer transfer matrix M.

    M[y_out, y_in] = exp(i*k*S) * w(theta) * h / L^p
    where L = sqrt(h^2 + (dy*h)^2), S = L*(1-f), theta = atan2(|dy|*h, h).
    """
    n_y = 2 * H + 1
    M = np.zeros((n_y, n_y), dtype=complex)

    for y_out in range(n_y):
        for y_in in range(n_y):
            dy = (y_out - H) - (y_in - H)
            phys_dy = dy * h
            L = np.sqrt(h**2 + phys_dy**2)
            S = L * (1.0 - f)
            theta = np.arctan2(abs(phys_dy), h)

            w = kernel_fn(theta)
            amplitude = np.exp(1j * k * S) * w * h / (L ** p)
            M[y_out, y_in] = amplitude

    return M


# ══════════════════════════════════════════════════════════════════════
#  PART 1: NORMALIZED DISPERSION RELATION
# ══════════════════════════════════════════════════════════════════════

def parabolic(k2, a, b):
    """E = a + b*k^2 (Schrodinger)"""
    return a + b * k2

def kg_dispersion(k2, E0sq, c2):
    """E^2 = E0^2 + c^2 * k^2 (Klein-Gordon)"""
    return E0sq + c2 * k2

def fit_normalized_dispersion(k_y_range, E_phase, h):
    """Fit E(k_y) from normalized eigenvalues.

    Returns dict with fit results for Schrodinger (E vs k^2) and
    Klein-Gordon (E^2 vs k^2).
    """
    results = {}
    mask = np.isfinite(k_y_range) & np.isfinite(E_phase) & (k_y_range > 1e-10)
    ky = k_y_range[mask]
    E = E_phase[mask]

    if len(ky) < 3:
        return {"schrodinger": (None, -1), "klein_gordon": (None, -1)}

    # Schrodinger: E vs k_y^2
    ss_tot = np.sum((E - np.mean(E))**2)
    if ss_tot > 1e-30:
        try:
            popt, _ = curve_fit(parabolic, ky**2, E, p0=[E.min(), 0.1], maxfev=5000)
            ss_res = np.sum((E - parabolic(ky**2, *popt))**2)
            r2 = 1.0 - ss_res / ss_tot
            results["schrodinger"] = (popt, r2)
        except Exception:
            results["schrodinger"] = (None, -1)
    else:
        results["schrodinger"] = (None, -1)

    # Klein-Gordon: E^2 vs k_y^2
    E2 = E**2
    ss_tot2 = np.sum((E2 - np.mean(E2))**2)
    if ss_tot2 > 1e-30:
        try:
            popt, _ = curve_fit(kg_dispersion, ky**2, E2, p0=[E2.min(), 1.0], maxfev=5000)
            ss_res = np.sum((E2 - kg_dispersion(ky**2, *popt))**2)
            r2 = 1.0 - ss_res / ss_tot2
            results["klein_gordon"] = (popt, r2)
        except Exception:
            results["klein_gordon"] = (None, -1)
    else:
        results["klein_gordon"] = (None, -1)

    return results


def run_part1():
    """Normalized dispersion relation."""
    print("=" * 78)
    print("PART 1: NORMALIZED DISPERSION RELATION")
    print("=" * 78)
    print(f"\nParameters: H={H_TRANSVERSE}, k={K_PHASE}, p={P_ATTEN}")
    print(f"Transverse sites: n_y = {2*H_TRANSVERSE+1}")
    print(f"h values: {H_VALUES}")
    print(f"Kernels: {list(KERNELS.keys())}")
    print(f"\nMethod: M_norm = M / spectral_radius(M)")
    print(f"        E(k_y) = arg(lambda) / h  [purely real from phase]")

    summary_rows = []

    for kernel_name, kernel_fn in KERNELS.items():
        for h in H_VALUES:
            print(f"\n{'─' * 78}")
            print(f"KERNEL: {kernel_name}   h = {h}")
            print(f"{'─' * 78}")

            # Build and normalize transfer matrix
            M = build_transfer_matrix(H_TRANSVERSE, h, K_PHASE, P_ATTEN, F_VALLEY, kernel_fn)
            eigenvalues_raw = np.linalg.eigvals(M)
            spec_radius = np.max(np.abs(eigenvalues_raw))

            M_norm = M / spec_radius

            # Eigendecompose normalized matrix
            eigenvalues, eigenvectors = eig(M_norm)

            # Sort by magnitude descending
            idx = np.argsort(-np.abs(eigenvalues))
            eigenvalues = eigenvalues[idx]
            eigenvectors = eigenvectors[:, idx]

            # All |lambda| <= 1 now
            mags = np.abs(eigenvalues)
            phases = np.angle(eigenvalues)

            print(f"\n  Spectral radius (raw): {spec_radius:.6f}")
            print(f"  After normalization: max|lambda| = {mags.max():.6f}")
            print(f"  |lambda| range: [{mags.min():.6f}, {mags.max():.6f}]")

            # Extract E from phase: E = arg(lambda) / h
            E_phase = phases / h

            # Show top eigenvalues
            print(f"\n  Top 15 normalized eigenvalues:")
            print(f"  {'n':>3}  {'|lambda|':>10}  {'arg(lam)':>10}  {'E=arg/h':>12}")
            for i in range(min(15, len(eigenvalues))):
                print(f"  {i:3d}  {mags[i]:10.6f}  {phases[i]:10.6f}  {E_phase[i]:12.4f}")

            # Momentum-space dispersion (Toeplitz / Fourier)
            # M is translation-invariant => Fourier diagonalizes it
            n_y = 2 * H_TRANSVERSE + 1
            center_row = M_norm[H_TRANSVERSE, :]
            y_positions = np.arange(n_y) - H_TRANSVERSE

            n_k = 100
            k_y_range = np.linspace(0, np.pi / h, n_k)
            M_hat = np.zeros(n_k, dtype=complex)

            for ik, ky in enumerate(k_y_range):
                M_hat[ik] = np.sum(center_row * np.exp(-1j * ky * y_positions * h))

            # E from phase of M_hat
            E_momentum = np.angle(M_hat) / h
            M_hat_mag = np.abs(M_hat)

            print(f"\n  Momentum-space dispersion (normalized):")
            print(f"  {'k_y':>8}  {'|M_hat|':>10}  {'E=arg/h':>12}")
            for i in range(0, n_k, 10):
                print(f"  {k_y_range[i]:8.3f}  {M_hat_mag[i]:10.6f}  {E_momentum[i]:12.4f}")

            # Fit
            fits = fit_normalized_dispersion(k_y_range, E_momentum, h)

            print(f"\n  Dispersion fits (normalized):")
            for model_name, (popt, r2) in fits.items():
                if popt is not None:
                    print(f"    {model_name:14s}: R^2 = {r2:8.4f}  params = {popt}")
                else:
                    print(f"    {model_name:14s}: fit failed")

            best_model = max(fits, key=lambda m: fits[m][1])
            best_r2 = fits[best_model][1]
            print(f"\n  Best fit: {best_model} (R^2 = {best_r2:.4f})")

            # Check magnitude uniformity (how close to unitary)
            prop_mask = mags > 0.1
            mag_cv = np.std(mags[prop_mask]) / np.mean(mags[prop_mask]) if np.sum(prop_mask) > 1 else 999
            print(f"  Magnitude CV (propagating modes): {mag_cv:.4f}")
            if mag_cv < 0.1:
                print(f"  => Near-UNITARY after normalization")
            else:
                print(f"  => Significant magnitude spread remains")

            summary_rows.append({
                "kernel": kernel_name, "h": h,
                "spec_radius": spec_radius, "best_model": best_model,
                "best_r2": best_r2, "mag_cv": mag_cv,
            })

    # Summary table
    print(f"\n\n{'=' * 78}")
    print("PART 1 SUMMARY: NORMALIZED DISPERSION")
    print(f"{'=' * 78}")
    print(f"\n  {'kernel':>8}  {'h':>5}  {'rho':>10}  {'best_model':>14}  {'R^2':>8}  {'mag_CV':>8}  {'unitary?':>8}")
    for r in summary_rows:
        unitary = "YES" if r["mag_cv"] < 0.1 else "no"
        print(f"  {r['kernel']:>8}  {r['h']:5.2f}  {r['spec_radius']:10.4f}  "
              f"{r['best_model']:>14}  {r['best_r2']:8.4f}  {r['mag_cv']:8.4f}  {unitary:>8}")

    return summary_rows


# ══════════════════════════════════════════════════════════════════════
#  PART 2: SIGNAL SPEED FROM NORMALIZED PROPAGATOR
# ══════════════════════════════════════════════════════════════════════

def measure_signal_edge(psi, center, threshold):
    """Find the furthest site from center where |psi| > threshold.

    Returns distance from center in lattice units.
    """
    amp = np.abs(psi)
    n = len(psi)
    max_dist = 0
    for i in range(n):
        if amp[i] > threshold:
            dist = abs(i - center)
            if dist > max_dist:
                max_dist = dist
    return max_dist


def run_signal_speed(kernel_name, kernel_fn, h, H, n_layers, threshold, normalize):
    """Propagate delta source and track signal edge.

    If normalize=True, normalize psi at each layer.
    Returns array of y_edge values for each layer.
    """
    n_y = 2 * H + 1
    center = H

    M = build_transfer_matrix(H, h, K_PHASE, P_ATTEN, F_VALLEY, kernel_fn)

    if normalize:
        spec_radius = np.max(np.abs(np.linalg.eigvals(M)))
        M = M / spec_radius

    psi = np.zeros(n_y, dtype=complex)
    psi[center] = 1.0

    edges = []
    for layer in range(n_layers):
        psi_new = M @ psi
        if normalize:
            norm = np.sqrt(np.sum(np.abs(psi_new)**2))
            if norm > 1e-30:
                psi_new /= norm
        psi = psi_new
        edge = measure_signal_edge(psi, center, threshold)
        edges.append(edge)

    return np.array(edges)


def fit_power_law(layers, edges):
    """Fit y_edge = a * n^alpha. Returns (a, alpha, R^2)."""
    mask = (edges > 0) & (layers > 0)
    if np.sum(mask) < 3:
        return None, None, -1

    log_n = np.log(layers[mask].astype(float))
    log_e = np.log(edges[mask].astype(float))

    ss_tot = np.sum((log_e - np.mean(log_e))**2)
    if ss_tot < 1e-30:
        return None, None, -1

    try:
        coeffs = np.polyfit(log_n, log_e, 1)
        alpha = coeffs[0]
        a = np.exp(coeffs[1])
        predicted = coeffs[0] * log_n + coeffs[1]
        ss_res = np.sum((log_e - predicted)**2)
        r2 = 1.0 - ss_res / ss_tot
        return a, alpha, r2
    except Exception:
        return None, None, -1


def run_part2():
    """Signal speed from normalized vs un-normalized propagator."""
    print(f"\n\n{'=' * 78}")
    print("PART 2: SIGNAL SPEED FROM NORMALIZED PROPAGATOR")
    print(f"{'=' * 78}")
    print(f"\nParameters: H={H_SIGNAL} (n_y={2*H_SIGNAL+1}), h=0.5, k={K_PHASE}, p={P_ATTEN}")
    print(f"Layers: {N_LAYERS}, threshold: {THRESHOLD}")
    print(f"Kernels: {list(KERNELS.keys())}")
    print(f"\nMethod: propagate delta source, track y_edge(n)")
    print(f"  Diffusive: y_edge ~ n^0.5")
    print(f"  Light cone: y_edge ~ n^1.0 (linear)")
    print(f"  Saturated: y_edge ~ n^0 (fills lattice)")

    h = 0.5
    layers = np.arange(1, N_LAYERS + 1)
    max_possible = H_SIGNAL  # maximum edge distance

    summary_rows = []

    for kernel_name, kernel_fn in KERNELS.items():
        print(f"\n{'─' * 78}")
        print(f"KERNEL: {kernel_name}")
        print(f"{'─' * 78}")

        for normalize in [False, True]:
            label = "NORMALIZED" if normalize else "UN-NORMALIZED"
            edges = run_signal_speed(kernel_name, kernel_fn, h, H_SIGNAL,
                                     N_LAYERS, THRESHOLD, normalize)

            # Check if signal saturated (reached boundary)
            n_saturated = np.sum(edges >= max_possible - 1)

            print(f"\n  {label}:")
            print(f"  {'layer':>6}  {'y_edge':>8}  {'y_edge/layer':>12}")
            for i in [0, 4, 9, 14, 19, 24, 29, 34, 39]:
                if i < len(edges):
                    ratio = edges[i] / (i + 1) if edges[i] > 0 else 0
                    sat = " *SAT*" if edges[i] >= max_possible - 1 else ""
                    print(f"  {i+1:6d}  {edges[i]:8d}  {ratio:12.4f}{sat}")

            # Fit power law to non-saturated portion
            non_sat_mask = edges < max_possible - 1
            if np.sum(non_sat_mask) > 3:
                a, alpha, r2 = fit_power_law(layers[non_sat_mask], edges[non_sat_mask])
                if alpha is not None:
                    print(f"\n  Power law fit (non-saturated): y_edge = {a:.3f} * n^{alpha:.3f}  (R^2={r2:.4f})")
                    if alpha > 0.8:
                        behavior = "LINEAR (light cone)"
                    elif alpha > 0.4:
                        behavior = "DIFFUSIVE"
                    else:
                        behavior = "SUB-DIFFUSIVE"
                    print(f"  Behavior: {behavior}")
                else:
                    alpha = -1
                    behavior = "FIT FAILED"
                    print(f"  Power law fit failed")
            else:
                alpha = -1
                behavior = "SATURATED EARLY"
                print(f"  Signal saturated too quickly for power law fit")

            # Effective speed at layer 20 (if available)
            if len(edges) >= 20 and edges[19] > 0:
                c_eff = edges[19] * h / (20 * h)  # y_edge * h / (n * h) = y_edge/n
                print(f"  Effective speed at layer 20: c_eff = {c_eff:.4f} (lattice units/layer)")
            else:
                c_eff = 0

            summary_rows.append({
                "kernel": kernel_name, "normalized": normalize,
                "alpha": alpha if alpha is not None else -1,
                "behavior": behavior,
                "n_saturated": n_saturated,
                "c_eff": c_eff,
                "final_edge": edges[-1] if len(edges) > 0 else 0,
            })

    # Summary table
    print(f"\n\n{'=' * 78}")
    print("PART 2 SUMMARY: SIGNAL SPEED")
    print(f"{'=' * 78}")
    print(f"\n  {'kernel':>8}  {'norm?':>6}  {'alpha':>8}  {'behavior':>20}  "
          f"{'c_eff':>8}  {'final_edge':>10}  {'saturated':>9}")
    for r in summary_rows:
        norm_str = "YES" if r["normalized"] else "no"
        alpha_str = f"{r['alpha']:.3f}" if r["alpha"] > -0.5 else "N/A"
        print(f"  {r['kernel']:>8}  {norm_str:>6}  {alpha_str:>8}  {r['behavior']:>20}  "
              f"{r['c_eff']:8.4f}  {r['final_edge']:10d}  {r['n_saturated']:9d}")

    return summary_rows


# ══════════════════════════════════════════════════════════════════════
#  HYPOTHESIS VERDICT
# ══════════════════════════════════════════════════════════════════════

def run_verdict(part1_results, part2_results):
    print(f"\n\n{'=' * 78}")
    print("HYPOTHESIS VERDICT")
    print(f"{'=' * 78}")

    # Part 1: Clean dispersion?
    print(f"\n  Part 1: Clean dispersion from normalization?")
    good_fits = [r for r in part1_results if r["best_r2"] > 0.8]
    n_total = len(part1_results)
    print(f"    {len(good_fits)}/{n_total} cases have R^2 > 0.8")
    if len(good_fits) > n_total / 2:
        print(f"    => SUPPORTED: normalization produces classifiable dispersion")
        part1_verdict = True
    else:
        print(f"    => FALSIFIED: dispersion remains messy even after normalization")
        part1_verdict = False

    near_unitary = [r for r in part1_results if r["mag_cv"] < 0.1]
    print(f"    {len(near_unitary)}/{n_total} cases are near-unitary (mag CV < 0.1)")

    # Part 2: Light cone?
    print(f"\n  Part 2: Finite signal speed (light cone)?")
    norm_results = [r for r in part2_results if r["normalized"]]
    unnorm_results = [r for r in part2_results if not r["normalized"]]

    linear_norm = [r for r in norm_results if "LINEAR" in r["behavior"]]
    diffusive_unnorm = [r for r in unnorm_results if "DIFFUSIVE" in r["behavior"]]

    print(f"    Normalized:   {len(linear_norm)}/{len(norm_results)} show LINEAR (light cone)")
    print(f"    Un-normalized: {len(diffusive_unnorm)}/{len(unnorm_results)} show DIFFUSIVE")

    if len(linear_norm) > 0:
        speeds = [r["c_eff"] for r in linear_norm if r["c_eff"] > 0]
        if speeds:
            print(f"    Light cone speeds: {[f'{s:.4f}' for s in speeds]}")
        print(f"    => SUPPORTED: normalization creates finite signal speed")
        part2_verdict = True
    else:
        # Check if normalization at least changes the exponent
        norm_alphas = [r["alpha"] for r in norm_results if r["alpha"] > 0]
        unnorm_alphas = [r["alpha"] for r in unnorm_results if r["alpha"] > 0]
        if norm_alphas and unnorm_alphas:
            mean_norm = np.mean(norm_alphas)
            mean_unnorm = np.mean(unnorm_alphas)
            print(f"    Mean alpha: normalized={mean_norm:.3f}, un-normalized={mean_unnorm:.3f}")
            if mean_norm > mean_unnorm + 0.1:
                print(f"    => PARTIAL: normalization increases spreading exponent but not to linear")
                part2_verdict = "partial"
            else:
                print(f"    => FALSIFIED: normalization does not create light cone")
                part2_verdict = False
        else:
            print(f"    => FALSIFIED: insufficient data to determine")
            part2_verdict = False

    # Overall
    print(f"\n  OVERALL VERDICT:")
    if part1_verdict and part2_verdict is True:
        print(f"    HYPOTHESIS SUPPORTED: Normalization gives clean dispersion AND light cone")
    elif part1_verdict and part2_verdict == "partial":
        print(f"    PARTIALLY SUPPORTED: Clean dispersion YES, light cone PARTIAL")
    elif part1_verdict:
        print(f"    PARTIALLY SUPPORTED: Clean dispersion YES, but no light cone")
    elif part2_verdict:
        print(f"    PARTIALLY SUPPORTED: Light cone YES, but dispersion not clean")
    else:
        print(f"    FALSIFIED: Neither clean dispersion nor light cone from normalization")

    print(f"\n{'=' * 78}")
    print("EXPERIMENT COMPLETE")
    print(f"{'=' * 78}")


# ── Main ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    part1_results = run_part1()
    part2_results = run_part2()
    run_verdict(part1_results, part2_results)
