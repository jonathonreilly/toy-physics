#!/usr/bin/env python3
"""Emergent metric tensor from angular kernel + 1/L^p attenuation.

HYPOTHESIS: The angular kernel induces an effective metric with Lorentzian
signature, distinguishing a timelike (causal) direction from spacelike
(spatial) directions — without explicitly assuming special relativity.

OBSERVABLE: The second-moment tensor of propagator edge weights,
    g_ij = <w * dx_i dx_j / L^(p+2)> / <w / L^p>
has eigenvalues with mixed sign (Lorentzian) rather than all-positive
(Euclidean).

EXPERIMENT:
  Part 1 (2+1D): Metric tensor for cos^2(theta) kernel, h=0.5, W=6
  Part 2: Compare kernels — uniform, cos, cos^2, exp(-0.8t^2)
  Part 3 (3+1D): Metric tensor for 4D lattice, h=1.0
  Part 4: Metric signature vs h (continuum limit) in 2+1D
  Part 5: Effective light cone / signal speed if Lorentzian

FALSIFICATION: If all eigenvalues are positive (Euclidean signature) for
all tested kernels, the propagator does not distinguish time from space
at the metric level.
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc

np.set_printoptions(precision=8, linewidth=120, suppress=True)

# =========================================================================
# Edge-weight metric computation
# =========================================================================

def compute_metric_2plus1d(h, phys_w, max_d_phys, p, weight_fn):
    """Compute the effective metric tensor from edge weights in 2+1D.

    Parameters
    ----------
    h : float
        Lattice spacing.
    phys_w : float
        Physical half-width of the lattice (used only for max_d).
    max_d_phys : float
        Maximum physical offset in spatial directions.
    p : int
        Power-law exponent for 1/L^p attenuation.
    weight_fn : callable
        Angular kernel w(theta).

    Returns
    -------
    metric : ndarray, shape (3, 3)
        The effective metric tensor (causal, y, z).
    eigenvalues : ndarray
        Sorted eigenvalues.
    """
    max_d = max(1, round(max_d_phys / h))
    d_spatial = 2

    metric = np.zeros((3, 3))
    norm = 0.0

    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dx = np.array([h, dy * h, dz * h])
            L = np.linalg.norm(dx)
            theta = math.atan2(math.sqrt((dy * h)**2 + (dz * h)**2), h)
            w = weight_fn(theta)

            contribution = w * h**d_spatial / L**p
            metric += contribution * np.outer(dx, dx) / L**2
            norm += contribution

    if norm > 0:
        metric /= norm

    evals = np.linalg.eigvalsh(metric)
    return metric, np.sort(evals)


def compute_metric_3plus1d(h, phys_w, max_d_phys, p, weight_fn):
    """Compute the effective metric tensor from edge weights in 3+1D.

    Returns
    -------
    metric : ndarray, shape (4, 4)
        The effective metric tensor (causal, y, z, w).
    eigenvalues : ndarray
        Sorted eigenvalues.
    """
    max_d = max(1, round(max_d_phys / h))
    d_spatial = 3

    metric = np.zeros((4, 4))
    norm = 0.0

    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            for dw in range(-max_d, max_d + 1):
                dx = np.array([h, dy * h, dz * h, dw * h])
                L = np.linalg.norm(dx)
                r_perp = math.sqrt((dy * h)**2 + (dz * h)**2 + (dw * h)**2)
                theta = math.atan2(r_perp, h)
                w = weight_fn(theta)

                contribution = w * h**d_spatial / L**p
                metric += contribution * np.outer(dx, dx) / L**2
                norm += contribution

    if norm > 0:
        metric /= norm

    evals = np.linalg.eigvalsh(metric)
    return metric, np.sort(evals)


def classify_signature(evals, tol=1e-10):
    """Classify the metric signature from eigenvalues."""
    n_neg = np.sum(evals < -tol)
    n_zero = np.sum(np.abs(evals) <= tol)
    n_pos = np.sum(evals > tol)
    if n_neg == 0 and n_pos == len(evals):
        return f"Euclidean (+{'+' * (n_pos - 1)})"
    elif n_neg == 1 and n_pos == len(evals) - 1:
        return f"Lorentzian (-{'+' * n_pos})"
    elif n_neg == 1 and n_zero > 0:
        return f"Degenerate Lorentzian (-{'0' * n_zero}{'+' * n_pos})"
    else:
        return f"Other (neg={n_neg}, zero={n_zero}, pos={n_pos})"


def effective_signal_speed(metric):
    """If metric has Lorentzian signature, compute effective signal speed.

    For ds^2 = g_00 dt^2 + g_ii dx_i^2 = 0 (light cone),
    c_eff = sqrt(-g_00 / g_spatial_avg) where g_spatial_avg is the
    average of spatial diagonal elements.
    """
    g00 = metric[0, 0]
    d = metric.shape[0]
    g_spatial = np.array([metric[i, i] for i in range(1, d)])
    g_spatial_avg = np.mean(g_spatial)

    if g00 < 0 and g_spatial_avg > 0:
        # Signature (-,+,+,...): g00 < 0, spatial > 0
        return math.sqrt(-g00 / g_spatial_avg)
    elif g00 > 0 and g_spatial_avg < 0:
        # Signature (+,-,-,...): g00 > 0, spatial < 0
        return math.sqrt(g00 / (-g_spatial_avg))
    else:
        return None


# =========================================================================
# Kernel definitions
# =========================================================================
KERNELS = {
    "uniform":        lambda t: 1.0,
    "cos(t)":         lambda t: max(0.0, math.cos(t)),
    "cos^2(t)":       lambda t: math.cos(t)**2,
    "exp(-0.8t^2)":   lambda t: math.exp(-0.8 * t * t),
}


# =========================================================================
# Main experiment
# =========================================================================
def main():
    t0 = time.time()
    print("=" * 80)
    print("EMERGENT METRIC TENSOR FROM ANGULAR KERNEL")
    print("=" * 80)

    # ------------------------------------------------------------------
    # Part 1: 2+1D metric tensor with cos^2 kernel
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART 1: 2+1D METRIC TENSOR (cos^2 kernel, h=0.5, W=6)")
    print("=" * 80)

    h = 0.5
    phys_w = 6
    max_d_phys = 3
    p = 2  # 1/L^2 for 2 spatial dims

    wfn = KERNELS["cos^2(t)"]
    metric, evals = compute_metric_2plus1d(h, phys_w, max_d_phys, p, wfn)
    sig = classify_signature(evals)

    print(f"\nParameters: h={h}, W={phys_w}, max_d_phys={max_d_phys}, p={p}")
    print(f"\nMetric tensor g_ij (indices: causal, y, z):")
    print(metric)
    print(f"\nEigenvalues: {evals}")
    print(f"Signature: {sig}")

    c_eff = effective_signal_speed(metric)
    if c_eff is not None:
        print(f"Effective signal speed: c_eff = {c_eff:.6f}")
    else:
        print("Effective signal speed: N/A (not cleanly Lorentzian from diag)")

    # Compute eigenvectors for interpretation
    evals_full, evecs = np.linalg.eigh(metric)
    sort_idx = np.argsort(evals_full)
    evals_full = evals_full[sort_idx]
    evecs = evecs[:, sort_idx]
    print(f"\nEigenvectors (columns, sorted by eigenvalue):")
    for i, ev in enumerate(evals_full):
        print(f"  lambda={ev:+.8f}  vec={evecs[:, i]}")

    # ------------------------------------------------------------------
    # Part 2: Compare kernels in 2+1D
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART 2: KERNEL COMPARISON (2+1D, h=0.5)")
    print("=" * 80)

    results_2d = {}
    for name, wfn in KERNELS.items():
        m, ev = compute_metric_2plus1d(h, phys_w, max_d_phys, p, wfn)
        sig = classify_signature(ev)
        c = effective_signal_speed(m)
        results_2d[name] = (m, ev, sig, c)
        print(f"\n--- {name} ---")
        print(f"  Metric diagonal: [{m[0,0]:.8f}, {m[1,1]:.8f}, {m[2,2]:.8f}]")
        print(f"  Off-diagonal:    g01={m[0,1]:.2e}, g02={m[0,2]:.2e}, g12={m[1,2]:.2e}")
        print(f"  Eigenvalues: {ev}")
        print(f"  Signature: {sig}")
        if c is not None:
            print(f"  Signal speed: c_eff = {c:.6f}")

    # Summary table
    print(f"\n{'Kernel':<16} {'evals[0]':>12} {'evals[1]':>12} {'evals[2]':>12} {'Signature':<20} {'c_eff':>10}")
    print("-" * 90)
    for name in KERNELS:
        m, ev, sig, c = results_2d[name]
        c_str = f"{c:.4f}" if c is not None else "N/A"
        print(f"{name:<16} {ev[0]:>12.8f} {ev[1]:>12.8f} {ev[2]:>12.8f} {sig:<20} {c_str:>10}")

    # ------------------------------------------------------------------
    # Part 3: 3+1D metric tensor
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART 3: 3+1D METRIC TENSOR (h=1.0)")
    print("=" * 80)

    h4 = 1.0
    phys_w_4d = 4
    max_d_phys_4d = 2
    p4 = 3  # 1/L^3 for 3 spatial dims

    results_3d = {}
    for name, wfn in KERNELS.items():
        m, ev = compute_metric_3plus1d(h4, phys_w_4d, max_d_phys_4d, p4, wfn)
        sig = classify_signature(ev)
        c = effective_signal_speed(m)
        results_3d[name] = (m, ev, sig, c)

    # Print full tensor for cos^2
    m_cos2, ev_cos2, sig_cos2, c_cos2 = results_3d["cos^2(t)"]
    print(f"\ncos^2 kernel metric tensor (4x4):")
    print(m_cos2)
    print(f"\nEigenvalues: {ev_cos2}")
    print(f"Signature: {sig_cos2}")
    if c_cos2 is not None:
        print(f"Signal speed: c_eff = {c_cos2:.6f}")

    # Summary table
    print(f"\n{'Kernel':<16} {'ev[0]':>10} {'ev[1]':>10} {'ev[2]':>10} {'ev[3]':>10} {'Signature':<20} {'c_eff':>10}")
    print("-" * 100)
    for name in KERNELS:
        m, ev, sig, c = results_3d[name]
        c_str = f"{c:.4f}" if c is not None else "N/A"
        print(f"{name:<16} {ev[0]:>10.6f} {ev[1]:>10.6f} {ev[2]:>10.6f} {ev[3]:>10.6f} {sig:<20} {c_str:>10}")

    # ------------------------------------------------------------------
    # Part 4: Metric signature vs h (continuum limit)
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART 4: CONTINUUM LIMIT — EIGENVALUES vs h (2+1D, cos^2 kernel)")
    print("=" * 80)

    h_values = [2.0, 1.0, 0.5, 0.25, 0.125]
    wfn_cos2 = KERNELS["cos^2(t)"]

    print(f"\n{'h':>6} {'max_d':>6} {'n_edges':>8} {'ev[0]':>12} {'ev[1]':>12} {'ev[2]':>12} {'Signature':<20} {'c_eff':>10}")
    print("-" * 100)
    for h_val in h_values:
        md = max(1, round(max_d_phys / h_val))
        n_edges = (2 * md + 1)**2
        m, ev = compute_metric_2plus1d(h_val, phys_w, max_d_phys, p, wfn_cos2)
        sig = classify_signature(ev)
        c = effective_signal_speed(m)
        c_str = f"{c:.6f}" if c is not None else "N/A"
        print(f"{h_val:>6.3f} {md:>6d} {n_edges:>8d} {ev[0]:>12.8f} {ev[1]:>12.8f} {ev[2]:>12.8f} {sig:<20} {c_str:>10}")

    # Also do continuum limit for ALL kernels
    print(f"\n--- Continuum limit for all kernels at h=0.125 ---")
    h_fine = 0.125
    print(f"\n{'Kernel':<16} {'ev[0]':>12} {'ev[1]':>12} {'ev[2]':>12} {'Signature':<20} {'c_eff':>10}")
    print("-" * 90)
    for name, wfn in KERNELS.items():
        m, ev = compute_metric_2plus1d(h_fine, phys_w, max_d_phys, p, wfn)
        sig = classify_signature(ev)
        c = effective_signal_speed(m)
        c_str = f"{c:.4f}" if c is not None else "N/A"
        print(f"{name:<16} {ev[0]:>12.8f} {ev[1]:>12.8f} {ev[2]:>12.8f} {sig:<20} {c_str:>10}")

    # ------------------------------------------------------------------
    # Part 5: Effective light cone analysis
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART 5: EFFECTIVE LIGHT CONE ANALYSIS")
    print("=" * 80)

    # Use the best kernel at finest resolution
    for dim_label, results in [("2+1D", results_2d), ("3+1D", results_3d)]:
        print(f"\n--- {dim_label} ---")
        for name in KERNELS:
            m, ev, sig, c = results[name]
            d = m.shape[0]
            print(f"\n  {name}:")
            print(f"    g_00 (causal-causal) = {m[0,0]:.8f}")
            spatial_diag = [m[i,i] for i in range(1, d)]
            print(f"    g_ii (spatial diag)   = {[f'{v:.8f}' for v in spatial_diag]}")
            ratio = m[0, 0] / np.mean(spatial_diag) if np.mean(spatial_diag) != 0 else float('inf')
            print(f"    g_00 / <g_spatial>    = {ratio:.8f}")
            print(f"    Anisotropy ratio: causal vs spatial = {abs(ratio):.4f}")
            if c is not None:
                print(f"    Light cone speed c_eff = {c:.6f}")
            # Check how close off-diagonals are to zero (isotropy in spatial sector)
            off_diag_max = 0.0
            for i in range(d):
                for j in range(i + 1, d):
                    off_diag_max = max(off_diag_max, abs(m[i, j]))
            print(f"    Max off-diagonal = {off_diag_max:.2e}")

    # ------------------------------------------------------------------
    # Part 6: Eigenvalue ratio analysis
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PART 6: EIGENVALUE RATIO ANALYSIS")
    print("=" * 80)

    print("\nIf Lorentzian, the ratio |lambda_min| / lambda_max measures")
    print("how strongly the metric distinguishes time from space.")
    print("Ratio = 1 means isotropic conformal Minkowski.")

    for dim_label, results in [("2+1D", results_2d), ("3+1D", results_3d)]:
        print(f"\n--- {dim_label} ---")
        print(f"{'Kernel':<16} {'|ev_min|/ev_max':>16} {'Interpretation':<30}")
        print("-" * 65)
        for name in KERNELS:
            m, ev, sig, c = results[name]
            if ev[0] < 0 and ev[-1] > 0:
                ratio = abs(ev[0]) / ev[-1]
                if 0.9 < ratio < 1.1:
                    interp = "~ conformal Minkowski"
                elif ratio < 0.5:
                    interp = "weakly Lorentzian"
                else:
                    interp = f"anisotropic Lorentzian"
            else:
                ratio = float('nan')
                interp = "not Lorentzian"
            print(f"{name:<16} {ratio:>16.6f} {interp:<30}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    elapsed = time.time() - t0
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    any_lorentzian = False
    for dim_label, results in [("2+1D", results_2d), ("3+1D", results_3d)]:
        for name in KERNELS:
            m, ev, sig, c = results[name]
            if "Lorentzian" in sig:
                any_lorentzian = True

    if any_lorentzian:
        print("\nRESULT: At least one kernel produces LORENTZIAN signature.")
        print("The angular kernel + 1/L^p attenuation induces an effective")
        print("metric that distinguishes timelike from spacelike directions.")
        print("HYPOTHESIS SUPPORTED.")
    else:
        print("\nRESULT: ALL kernels produce EUCLIDEAN signature.")
        print("The propagator does not distinguish time from space at the")
        print("metric level. HYPOTHESIS FALSIFIED.")

    print(f"\nElapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
