#!/usr/bin/env python3
"""
Effective Hamiltonian from DAG Transfer Matrix
===============================================
Extract dispersion relation E(k_y) from the single-layer transfer matrix M
of a 2D rectangular DAG propagator.

Physics:
  M maps y-amplitudes at layer x to layer x+1.
  Eigenvalues lambda_n = exp(-i E_n h) give effective energies E_n.
  Plotting E_n vs k_y^2 reveals whether the propagator encodes
  Schrodinger, Klein-Gordon, or lattice-Laplacian kinetics.

Hypothesis:
  The effective Hamiltonian has a dispersion relation that approaches
  a known form (Schrodinger, Klein-Gordon, or lattice Laplacian) in
  the continuum limit h -> 0.

Falsification:
  If no fit achieves R^2 > 0.8, or the dispersion does not converge
  with h, the propagator defines a novel kinetic operator.
"""

import numpy as np
from numpy.linalg import eig
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ── Parameters ──────────────────────────────────────────────────────
H_TRANSVERSE = 10          # half-height: y in [-H, +H], so 2H+1 sites
K_PHASE      = 5.0         # phase wavenumber k
P_ATTEN      = 1.0         # 1/L^p attenuation (p=1 for 2D)
F_VALLEY     = 0.0         # f=0 free space
H_VALUES     = [1.0, 0.5, 0.25]
MAX_DY       = None        # None = no cutoff (all dy allowed)

KERNELS = {
    "gauss": lambda theta: np.exp(-0.8 * theta**2),
    "cos2":  lambda theta: np.cos(theta)**2,
}


def build_transfer_matrix(H, h, k, p, f, kernel_fn, max_dy=None):
    """Build the single-layer transfer matrix M.

    M[y_out, y_in] = exp(i*k*S) * w(theta) * h / L^p
    where L = sqrt(h^2 + (dy*h)^2), S = L*(1-f), theta = atan2(|dy|*h, h).
    The extra factor of h is the lattice measure (discrete path integral weight).
    """
    n_y = 2 * H + 1
    M = np.zeros((n_y, n_y), dtype=complex)

    for y_out in range(n_y):
        for y_in in range(n_y):
            dy = (y_out - H) - (y_in - H)  # physical displacement in lattice units
            if max_dy is not None and abs(dy) > max_dy:
                continue

            phys_dy = dy * h          # physical transverse displacement
            L = np.sqrt(h**2 + phys_dy**2)   # geometric path length
            S = L * (1.0 - f)        # action (free space: S = L)
            theta = np.arctan2(abs(phys_dy), h)

            w = kernel_fn(theta)
            amplitude = np.exp(1j * k * S) * w * h / (L ** p)
            M[y_out, y_in] = amplitude

    return M


def extract_energies(M, h):
    """Eigendecompose M, extract effective energies E_n = (i/h) * ln(lambda_n)."""
    eigenvalues, eigenvectors = eig(M)

    # Sort by |lambda| descending (dominant modes first)
    idx = np.argsort(-np.abs(eigenvalues))
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Effective energies: M = exp(-i H h) => lambda = exp(-i E h) => E = i ln(lambda) / h
    E_n = 1j * np.log(eigenvalues) / h

    return eigenvalues, eigenvectors, E_n


def extract_ky(eigenvectors, H, h):
    """Extract dominant transverse wavenumber k_y for each eigenvector via FFT."""
    n_y = 2 * H + 1
    k_y_values = []

    for col in range(eigenvectors.shape[1]):
        v = eigenvectors[:, col]
        fft_v = np.fft.fft(v)
        power = np.abs(fft_v)**2

        # Frequencies in units of 2*pi/n_y per sample
        freqs = np.fft.fftfreq(n_y)

        # Only positive frequencies (skip DC)
        pos_mask = freqs > 0
        if not np.any(pos_mask):
            k_y_values.append(0.0)
            continue

        dominant_idx = np.argmax(power[pos_mask])
        dominant_freq = freqs[pos_mask][dominant_idx]

        # Convert to physical wavenumber: k_y = 2*pi*freq_index / (n_y * h)
        k_y = 2.0 * np.pi * dominant_freq / h
        k_y_values.append(abs(k_y))

    return np.array(k_y_values)


# ── Fitting functions ───────────────────────────────────────────────
def parabolic(k2, a, b):
    """E = a + b*k^2 (Schrodinger)"""
    return a + b * k2

def linear_disp(k, a, b):
    """E = a + b*|k| (massless relativistic)"""
    return a + b * k

def lattice_disp(k, a, b):
    """E = a + b*(1 - cos(k)) (lattice Laplacian)"""
    return a + b * (1.0 - np.cos(k))


def fit_dispersion(k_y, E_real):
    """Fit E vs k_y to three models, return R^2 for each."""
    results = {}

    # Filter out NaN/Inf
    mask = np.isfinite(k_y) & np.isfinite(E_real) & (k_y > 1e-10)
    ky = k_y[mask]
    Er = E_real[mask]

    if len(ky) < 3:
        return {"parabolic": (None, -1), "linear": (None, -1), "lattice": (None, -1)}

    ss_tot = np.sum((Er - np.mean(Er))**2)
    if ss_tot < 1e-30:
        return {"parabolic": (None, -1), "linear": (None, -1), "lattice": (None, -1)}

    # 1. Parabolic: E vs k^2
    try:
        popt, _ = curve_fit(parabolic, ky**2, Er, p0=[Er.min(), 1.0], maxfev=5000)
        ss_res = np.sum((Er - parabolic(ky**2, *popt))**2)
        r2 = 1.0 - ss_res / ss_tot
        results["parabolic"] = (popt, r2)
    except Exception:
        results["parabolic"] = (None, -1)

    # 2. Linear: E vs |k|
    try:
        popt, _ = curve_fit(linear_disp, ky, Er, p0=[Er.min(), 1.0], maxfev=5000)
        ss_res = np.sum((Er - linear_disp(ky, *popt))**2)
        r2 = 1.0 - ss_res / ss_tot
        results["linear"] = (popt, r2)
    except Exception:
        results["linear"] = (None, -1)

    # 3. Lattice: E vs 1-cos(k)
    try:
        popt, _ = curve_fit(lattice_disp, ky, Er, p0=[Er.min(), 1.0], maxfev=5000)
        ss_res = np.sum((Er - lattice_disp(ky, *popt))**2)
        r2 = 1.0 - ss_res / ss_tot
        results["lattice"] = (popt, r2)
    except Exception:
        results["lattice"] = (None, -1)

    return results


# ── Main experiment ─────────────────────────────────────────────────
def run_experiment():
    print("=" * 78)
    print("EFFECTIVE HAMILTONIAN FROM DAG TRANSFER MATRIX")
    print("=" * 78)
    print(f"\nParameters: H={H_TRANSVERSE}, k={K_PHASE}, p={P_ATTEN}, f={F_VALLEY}")
    print(f"Transverse sites: n_y = {2*H_TRANSVERSE+1}")
    print(f"h values: {H_VALUES}")
    print(f"Kernels: {list(KERNELS.keys())}")

    all_results = {}

    for kernel_name, kernel_fn in KERNELS.items():
        all_results[kernel_name] = {}

        for h in H_VALUES:
            print(f"\n{'─' * 78}")
            print(f"KERNEL: {kernel_name}   h = {h}")
            print(f"{'─' * 78}")

            # Build transfer matrix
            M = build_transfer_matrix(H_TRANSVERSE, h, K_PHASE, P_ATTEN, F_VALLEY,
                                       kernel_fn, max_dy=MAX_DY)

            print(f"\nTransfer matrix M: {M.shape}")
            print(f"  ||M||_F = {np.linalg.norm(M, 'fro'):.6f}")
            print(f"  max|M_ij| = {np.max(np.abs(M)):.6f}")
            print(f"  M is symmetric: {np.allclose(M, M.T)}")

            # Eigendecomposition
            eigenvalues, eigenvectors, E_n = extract_energies(M, h)

            # Table of eigenvalues
            print(f"\nTop 10 eigenvalues:")
            print(f"  {'n':>3}  {'|lambda|':>12}  {'arg(lambda)':>12}  "
                  f"{'Re(E)':>12}  {'Im(E)':>12}")
            for i in range(min(10, len(eigenvalues))):
                lam = eigenvalues[i]
                E = E_n[i]
                print(f"  {i:3d}  {abs(lam):12.6f}  {np.angle(lam):12.6f}  "
                      f"{E.real:12.4f}  {E.imag:12.4f}")

            # Spectral radius and decay
            spec_radius = np.max(np.abs(eigenvalues))
            n_propagating = np.sum(np.abs(eigenvalues) > 0.5 * spec_radius)
            print(f"\n  Spectral radius: {spec_radius:.6f}")
            print(f"  Propagating modes (|lambda| > 0.5*rho): {n_propagating}")

            # Extract k_y from eigenvectors
            k_y = extract_ky(eigenvectors, H_TRANSVERSE, h)

            # Use only modes with reasonable amplitude (propagating modes)
            threshold = 0.1 * spec_radius
            prop_mask = np.abs(eigenvalues) > threshold
            k_y_prop = k_y[prop_mask]
            E_prop = E_n[prop_mask]
            E_real_prop = E_prop.real
            E_imag_prop = E_prop.imag

            print(f"\n  Modes above threshold ({threshold:.4f}): {np.sum(prop_mask)}")

            if np.sum(prop_mask) >= 3:
                # Sort by k_y for display
                sort_idx = np.argsort(k_y_prop)
                k_sorted = k_y_prop[sort_idx]
                E_sorted = E_real_prop[sort_idx]
                Ei_sorted = E_imag_prop[sort_idx]

                print(f"\n  Dispersion data (sorted by k_y):")
                print(f"  {'k_y':>10}  {'k_y^2':>10}  {'Re(E)':>12}  {'Im(E)':>12}")
                for i in range(len(k_sorted)):
                    print(f"  {k_sorted[i]:10.4f}  {k_sorted[i]**2:10.4f}  "
                          f"{E_sorted[i]:12.4f}  {Ei_sorted[i]:12.4f}")

                # Fit dispersion
                fits = fit_dispersion(k_sorted, E_sorted)

                print(f"\n  Dispersion fits:")
                for model_name, (popt, r2) in fits.items():
                    if popt is not None:
                        print(f"    {model_name:12s}: R^2 = {r2:8.4f}  params = {popt}")
                    else:
                        print(f"    {model_name:12s}: fit failed")

                best_model = max(fits, key=lambda m: fits[m][1])
                best_r2 = fits[best_model][1]
                print(f"\n  Best fit: {best_model} (R^2 = {best_r2:.4f})")

                all_results[kernel_name][h] = {
                    "k_y": k_sorted,
                    "E_real": E_sorted,
                    "E_imag": Ei_sorted,
                    "fits": fits,
                    "best_model": best_model,
                    "best_r2": best_r2,
                    "n_modes": len(k_sorted),
                    "spec_radius": spec_radius,
                }
            else:
                print("  Too few propagating modes for dispersion fit.")
                all_results[kernel_name][h] = {
                    "n_modes": int(np.sum(prop_mask)),
                    "spec_radius": spec_radius,
                    "fits": {},
                    "best_model": "N/A",
                    "best_r2": -1,
                }

    # ── Summary ─────────────────────────────────────────────────────
    print(f"\n\n{'=' * 78}")
    print("SUMMARY: DISPERSION CLASSIFICATION")
    print(f"{'=' * 78}")
    print(f"\n{'kernel':>8}  {'h':>6}  {'#modes':>6}  {'best_model':>12}  "
          f"{'R^2':>8}  {'rho':>10}")
    for kernel_name in KERNELS:
        for h in H_VALUES:
            r = all_results[kernel_name].get(h, {})
            print(f"  {kernel_name:>6}  {h:6.2f}  {r.get('n_modes',0):6d}  "
                  f"{r.get('best_model','N/A'):>12}  "
                  f"{r.get('best_r2',-1):8.4f}  "
                  f"{r.get('spec_radius',0):10.6f}")

    # ── Convergence check ───────────────────────────────────────────
    print(f"\n{'=' * 78}")
    print("CONVERGENCE CHECK: does dispersion stabilize as h -> 0?")
    print(f"{'=' * 78}")

    for kernel_name in KERNELS:
        print(f"\n  Kernel: {kernel_name}")
        models_seen = []
        for h in H_VALUES:
            r = all_results[kernel_name].get(h, {})
            bm = r.get("best_model", "N/A")
            br = r.get("best_r2", -1)
            models_seen.append((bm, br))
            print(f"    h={h:.2f}: {bm} (R^2={br:.4f})")

        # Check if same model wins across h values
        model_names = [m[0] for m in models_seen if m[0] != "N/A"]
        if len(set(model_names)) == 1 and model_names:
            r2_vals = [m[1] for m in models_seen if m[1] > 0]
            if r2_vals and all(r > 0.8 for r in r2_vals):
                print(f"    => CONVERGED to {model_names[0]} dispersion (all R^2 > 0.8)")
            elif r2_vals and r2_vals[-1] > r2_vals[0]:
                print(f"    => IMPROVING toward {model_names[0]} (R^2 increasing with smaller h)")
            else:
                print(f"    => Same model ({model_names[0]}) but R^2 not improving")
        else:
            print(f"    => NOT CONVERGED: best model changes across h values")

    # ── Hypothesis verdict ──────────────────────────────────────────
    print(f"\n{'=' * 78}")
    print("HYPOTHESIS VERDICT")
    print(f"{'=' * 78}")

    any_classified = False
    any_converged = False
    for kernel_name in KERNELS:
        for h in H_VALUES:
            r = all_results[kernel_name].get(h, {})
            if r.get("best_r2", -1) > 0.8:
                any_classified = True
        # Check convergence
        model_set = set()
        for h in H_VALUES:
            r = all_results[kernel_name].get(h, {})
            bm = r.get("best_model", "N/A")
            if bm != "N/A":
                model_set.add(bm)
        if len(model_set) == 1:
            any_converged = True

    if any_classified and any_converged:
        print("\n  SUPPORTED: The effective Hamiltonian has a classifiable dispersion")
        print("  relation that converges in the continuum limit.")
    elif any_classified:
        print("\n  PARTIALLY SUPPORTED: Classifiable dispersion at some h values,")
        print("  but convergence with h not established.")
    else:
        print("\n  FALSIFIED: No dispersion fit achieves R^2 > 0.8.")
        print("  The propagator may define a NOVEL kinetic operator.")

    # ── Additional analysis: eigenvalue spectrum structure ──────────
    print(f"\n{'=' * 78}")
    print("BONUS: EIGENVALUE SPECTRUM STRUCTURE")
    print(f"{'=' * 78}")

    for kernel_name, kernel_fn in KERNELS.items():
        h = 0.5  # representative
        M = build_transfer_matrix(H_TRANSVERSE, h, K_PHASE, P_ATTEN, F_VALLEY,
                                   kernel_fn, max_dy=MAX_DY)
        eigenvalues, _, _ = extract_energies(M, h)

        magnitudes = np.abs(eigenvalues)
        phases = np.angle(eigenvalues)

        print(f"\n  Kernel: {kernel_name}, h={h}")
        print(f"    |lambda| range: [{magnitudes.min():.6f}, {magnitudes.max():.6f}]")
        print(f"    |lambda| spread (max/min): {magnitudes.max()/max(magnitudes.min(),1e-30):.2f}")
        print(f"    Phase range: [{phases.min():.4f}, {phases.max():.4f}]")
        print(f"    Phase spread: {phases.max() - phases.min():.4f}")

        # Check if eigenvalues lie on a circle (unitary-like)
        mean_mag = np.mean(magnitudes)
        mag_std = np.std(magnitudes)
        print(f"    Mean |lambda|: {mean_mag:.6f}, std: {mag_std:.6f}")
        print(f"    Coefficient of variation: {mag_std/mean_mag:.4f}")
        if mag_std / mean_mag < 0.1:
            print(f"    => Approximately UNITARY (eigenvalues near circle)")
        else:
            print(f"    => NON-UNITARY (significant magnitude spread)")

    # ── Alternative: direct momentum-space analysis ─────────────────
    print(f"\n{'=' * 78}")
    print("BONUS: DIRECT MOMENTUM-SPACE TRANSFER MATRIX")
    print(f"{'=' * 78}")
    print("\nBuild M in Fourier basis to get E(k_y) directly.\n")

    for kernel_name, kernel_fn in KERNELS.items():
        for h in [0.5]:
            n_y = 2 * H_TRANSVERSE + 1
            M = build_transfer_matrix(H_TRANSVERSE, h, K_PHASE, P_ATTEN, F_VALLEY,
                                       kernel_fn, max_dy=MAX_DY)

            # M is translation-invariant (Toeplitz) in the bulk.
            # Its Fourier transform diagonalizes it (approximately for finite systems).
            # M_hat(k_y) = sum_dy M(dy) * exp(-i k_y dy)

            # Extract the "kernel" row: M[H, :] gives amplitudes from center
            center_row = M[H_TRANSVERSE, :]  # row corresponding to y_out = 0

            # Compute M_hat(k_y) for a range of k_y
            n_k = 100
            k_y_range = np.linspace(0, np.pi / h, n_k)
            M_hat = np.zeros(n_k, dtype=complex)

            y_positions = np.arange(n_y) - H_TRANSVERSE  # [-H, ..., +H]

            for ik, ky in enumerate(k_y_range):
                # M_hat(k_y) = sum_j M[0,j] * exp(-i * k_y * y_j * h)
                M_hat[ik] = np.sum(center_row * np.exp(-1j * ky * y_positions * h))

            # Effective energy from M_hat
            E_ky = 1j * np.log(M_hat) / h

            print(f"  Kernel: {kernel_name}, h={h}")
            print(f"  {'k_y':>8}  {'|M_hat|':>10}  {'arg(M_hat)':>12}  "
                  f"{'Re(E)':>12}  {'Im(E)':>12}")
            for i in range(0, n_k, 10):
                print(f"  {k_y_range[i]:8.3f}  {np.abs(M_hat[i]):10.6f}  "
                      f"{np.angle(M_hat[i]):12.6f}  "
                      f"{E_ky[i].real:12.4f}  {E_ky[i].imag:12.4f}")

            # Fit the momentum-space dispersion
            E_real_ky = E_ky.real
            mask = np.isfinite(E_real_ky)
            ky_clean = k_y_range[mask]
            Er_clean = E_real_ky[mask]

            if len(ky_clean) > 5:
                fits = fit_dispersion(ky_clean, Er_clean)
                print(f"\n  Momentum-space dispersion fits:")
                for model_name, (popt, r2) in fits.items():
                    if popt is not None:
                        print(f"    {model_name:12s}: R^2 = {r2:8.4f}  params = {popt}")
                    else:
                        print(f"    {model_name:12s}: fit failed")

                best_model = max(fits, key=lambda m: fits[m][1])
                best_r2 = fits[best_model][1]
                print(f"  Best fit: {best_model} (R^2 = {best_r2:.4f})")

                # Check: does Re(E) increase with k_y?
                dE = np.diff(Er_clean)
                n_increasing = np.sum(dE > 0)
                n_decreasing = np.sum(dE < 0)
                print(f"\n  Monotonicity: {n_increasing} increasing, {n_decreasing} decreasing segments")
                if n_increasing > n_decreasing:
                    print(f"  => Re(E) is PREDOMINANTLY INCREASING with k_y (normal dispersion)")
                elif n_decreasing > n_increasing:
                    print(f"  => Re(E) is PREDOMINANTLY DECREASING with k_y (anomalous)")
                else:
                    print(f"  => Re(E) is OSCILLATORY")

    print(f"\n{'=' * 78}")
    print("EXPERIMENT COMPLETE")
    print(f"{'=' * 78}")


if __name__ == "__main__":
    run_experiment()
