#!/usr/bin/env python3
"""
Full 2D Dispersion Surface from DAG Propagator
================================================
Compute the FULL 2D dispersion E(k_x, k_y) by analyzing how the propagator
matrix M^n behaves for different numbers of layers n.

Physics:
  The transfer matrix M maps amplitudes from layer x to layer x+1.
  After n layers, the propagator is M^n. The effective energy for mode j
  after propagating n layers is E_j = i * ln(lambda_j) / h.

  k_x (longitudinal momentum) is implicit: it is the propagation direction.
  The phase accumulated per layer is arg(lambda_j), so k_x relates to the
  number of layers traversed.

  For a free particle with dispersion E(k) = omega(k), the propagator in
  momentum space is G(k_y, omega) = 1/(omega - omega(k_y)). Poles of
  |G(k_y, omega)|^2 in the (k_y, omega) plane reveal the dispersion surface.

Key question:
  Does the dispersion surface have a LIGHT CONE shape (E^2 = k_x^2 + k_y^2,
  Lorentzian) or a parabolic shape (E = k_x^2 + k_y^2, Euclidean)?

Hypothesis:
  The 2D dispersion surface has a light-cone shape (omega^2 ~ k_y^2) at
  fine lattice spacing.

Falsification:
  If omega is always parabolic in k_y (Schrodinger, not relativistic),
  no light cone emerges.
"""

import numpy as np
from numpy.linalg import eig, matrix_power
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ── Parameters ──────────────────────────────────────────────────────
H_TRANSVERSE = 15          # half-height: y in [-H, +H], so 2H+1 = 31 sites
K_PHASE      = 5.0         # phase wavenumber k
P_ATTEN      = 1.0         # 1/L^p attenuation (p=1 for 1+1D spatial)
F_VALLEY     = 0.0         # f=0 free space
H_STEP       = 0.5         # lattice spacing
N_LAYERS_MAX = 20          # propagate up to this many layers for Green's fn

KERNELS = {
    "gauss": lambda theta: np.exp(-0.8 * theta**2),
    "cos2":  lambda theta: np.cos(theta)**2,
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


def extract_energies(M, h):
    """Eigendecompose M, extract effective energies E_n = (i/h) * ln(lambda_n)."""
    eigenvalues, eigenvectors = eig(M)
    idx = np.argsort(-np.abs(eigenvalues))
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
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
        freqs = np.fft.fftfreq(n_y)

        # Use full spectrum (positive and negative) for signed k_y
        # Skip DC component
        power_no_dc = power.copy()
        power_no_dc[0] = 0

        if np.max(power_no_dc) < 1e-30:
            k_y_values.append(0.0)
            continue

        dominant_idx = np.argmax(power_no_dc)
        dominant_freq = freqs[dominant_idx]

        # Convert to physical wavenumber: k_y = 2*pi*freq / h
        k_y = 2.0 * np.pi * dominant_freq / h
        k_y_values.append(k_y)

    return np.array(k_y_values)


# ── Fitting functions ───────────────────────────────────────────────
def lorentzian_fit(ky2, m2, c2):
    """omega^2 = m^2 + c^2 * k_y^2  (light cone)"""
    return m2 + c2 * ky2

def schrodinger_fit(ky2, E0, alpha):
    """omega = E0 + alpha * k_y^2  (parabolic)"""
    return E0 + alpha * ky2

def linear_fit(ky, E0, v):
    """omega = E0 + v * |k_y|  (massless cone)"""
    return E0 + v * np.abs(ky)


def compute_r2(y_data, y_pred):
    """Compute R^2."""
    ss_tot = np.sum((y_data - np.mean(y_data))**2)
    if ss_tot < 1e-30:
        return -1.0
    ss_res = np.sum((y_data - y_pred)**2)
    return 1.0 - ss_res / ss_tot


# ── Part 1: Eigenvalue dispersion ──────────────────────────────────
def eigenvalue_dispersion(kernel_name, kernel_fn, h):
    """Extract E(k_y) from eigenvalues of M."""
    print(f"\n{'─' * 78}")
    print(f"PART 1: EIGENVALUE DISPERSION — kernel={kernel_name}, h={h}")
    print(f"{'─' * 78}")

    M = build_transfer_matrix(H_TRANSVERSE, h, K_PHASE, P_ATTEN, F_VALLEY, kernel_fn)
    n_y = M.shape[0]

    print(f"\n  Transfer matrix M: {n_y}x{n_y}")
    print(f"  ||M||_F = {np.linalg.norm(M, 'fro'):.6f}")

    eigenvalues, eigenvectors, E_n = extract_energies(M, h)
    k_y = extract_ky(eigenvectors, H_TRANSVERSE, h)

    # Print mode table
    spec_radius = np.max(np.abs(eigenvalues))
    threshold = 0.1 * spec_radius
    prop_mask = np.abs(eigenvalues) > threshold

    print(f"\n  Spectral radius: {spec_radius:.6f}")
    print(f"  Propagating modes (|lam| > {threshold:.4f}): {np.sum(prop_mask)}")

    print(f"\n  {'mode':>4}  {'|lam|':>10}  {'arg(lam)/h':>12}  {'k_y':>10}  "
          f"{'Re(E)':>12}  {'Im(E)':>12}")
    for i in range(min(20, len(eigenvalues))):
        lam = eigenvalues[i]
        E = E_n[i]
        print(f"  {i:4d}  {abs(lam):10.6f}  {np.angle(lam)/h:12.6f}  "
              f"{k_y[i]:10.4f}  {E.real:12.4f}  {E.imag:12.4f}")

    # Return propagating modes for fitting
    k_y_prop = k_y[prop_mask]
    E_prop = E_n[prop_mask]
    lam_prop = eigenvalues[prop_mask]

    return k_y_prop, E_prop, lam_prop, eigenvalues, eigenvectors


# ── Part 2: Green's function G(y,n) and spectral function ─────────
def greens_function_spectrum(kernel_name, kernel_fn, h, n_layers):
    """Compute G(y,n) = <y| M^n |0> and its 2D Fourier transform."""
    print(f"\n{'─' * 78}")
    print(f"PART 2: GREEN'S FUNCTION SPECTRUM — kernel={kernel_name}, h={h}")
    print(f"{'─' * 78}")

    M = build_transfer_matrix(H_TRANSVERSE, h, K_PHASE, P_ATTEN, F_VALLEY, kernel_fn)
    n_y = M.shape[0]
    center = H_TRANSVERSE  # index of y=0

    # Compute G(y, n) for n = 0, 1, ..., n_layers
    # G(y, n) = (M^n)[y, center]
    G = np.zeros((n_y, n_layers + 1), dtype=complex)
    G[center, 0] = 1.0  # delta source at y=0, n=0

    M_power = np.eye(n_y, dtype=complex)
    for n in range(1, n_layers + 1):
        M_power = M_power @ M
        G[:, n] = M_power[:, center]

    # Print G(y,n) amplitudes at selected points
    print(f"\n  |G(y, n)| at selected (y, n):")
    print(f"  {'y\\n':>4}", end="")
    for n in range(0, n_layers + 1, 2):
        print(f"  {n:>8}", end="")
    print()
    for y_idx in range(0, n_y, 5):
        y_phys = (y_idx - H_TRANSVERSE) * h
        print(f"  {y_phys:4.1f}", end="")
        for n in range(0, n_layers + 1, 2):
            print(f"  {np.abs(G[y_idx, n]):8.4f}", end="")
        print()

    # 2D Fourier transform: G_hat(k_y, omega)
    # k_y grid
    n_ky = 64
    n_omega = 128
    ky_max = np.pi / h
    omega_max = np.pi / h
    k_y_grid = np.linspace(-ky_max, ky_max, n_ky)
    omega_grid = np.linspace(-omega_max, omega_max, n_omega)

    # Compute spectral function A(k_y, omega) = |G_hat(k_y, omega)|^2
    y_positions = (np.arange(n_y) - H_TRANSVERSE) * h  # physical y positions
    n_times = np.arange(n_layers + 1) * h  # "time" = n * h

    G_hat = np.zeros((n_ky, n_omega), dtype=complex)
    for iky, ky in enumerate(k_y_grid):
        for iw, omega in enumerate(omega_grid):
            # G_hat = sum_{y,n} G(y,n) * exp(-i*ky*y) * exp(-i*omega*n*h)
            phase_y = np.exp(-1j * ky * y_positions)  # (n_y,)
            phase_t = np.exp(-1j * omega * n_times)   # (n_layers+1,)
            G_hat[iky, iw] = np.sum(G * phase_y[:, None] * phase_t[None, :])

    A = np.abs(G_hat)**2

    # Find peaks in spectral function (dispersion surface)
    print(f"\n  Spectral function A(k_y, omega) = |G_hat|^2")
    print(f"  k_y range: [{k_y_grid[0]:.3f}, {k_y_grid[-1]:.3f}]")
    print(f"  omega range: [{omega_grid[0]:.3f}, {omega_grid[-1]:.3f}]")
    print(f"  max(A) = {np.max(A):.6f}")

    # Extract dispersion curve: for each k_y, find omega that maximizes A
    omega_peaks = np.zeros(n_ky)
    A_peak_vals = np.zeros(n_ky)
    for iky in range(n_ky):
        idx = np.argmax(A[iky, :])
        omega_peaks[iky] = omega_grid[idx]
        A_peak_vals[iky] = A[iky, idx]

    print(f"\n  Dispersion from spectral peaks:")
    print(f"  {'k_y':>8}  {'omega_peak':>12}  {'A_peak':>12}")
    for i in range(0, n_ky, 4):
        print(f"  {k_y_grid[i]:8.3f}  {omega_peaks[i]:12.4f}  {A_peak_vals[i]:12.4f}")

    return k_y_grid, omega_grid, A, omega_peaks, A_peak_vals


# ── Part 3: Momentum-space transfer (Toeplitz/Fourier) ────────────
def momentum_space_dispersion(kernel_name, kernel_fn, h):
    """Exploit translation invariance: Fourier transform the kernel row."""
    print(f"\n{'─' * 78}")
    print(f"PART 3: MOMENTUM-SPACE DISPERSION — kernel={kernel_name}, h={h}")
    print(f"{'─' * 78}")

    M = build_transfer_matrix(H_TRANSVERSE, h, K_PHASE, P_ATTEN, F_VALLEY, kernel_fn)
    n_y = M.shape[0]

    # M is approximately Toeplitz. Extract center row.
    center_row = M[H_TRANSVERSE, :]
    y_positions = np.arange(n_y) - H_TRANSVERSE

    # Compute M_hat(k_y) = sum_j M[0,j] * exp(-i * k_y * y_j * h)
    n_k = 200
    k_y_range = np.linspace(0, np.pi / h, n_k)
    M_hat = np.zeros(n_k, dtype=complex)

    for ik, ky in enumerate(k_y_range):
        M_hat[ik] = np.sum(center_row * np.exp(-1j * ky * y_positions * h))

    # Effective energy: E(k_y) = i * ln(M_hat(k_y)) / h
    E_ky = 1j * np.log(M_hat) / h

    omega = np.angle(M_hat) / h  # phase velocity = arg(M_hat)/h
    decay = -np.log(np.abs(M_hat)) / h  # decay rate

    print(f"\n  Momentum-space transfer function M_hat(k_y):")
    print(f"  {'k_y':>8}  {'|M_hat|':>10}  {'omega':>12}  {'decay':>10}  "
          f"{'Re(E)':>12}  {'Im(E)':>12}")
    for i in range(0, n_k, 20):
        print(f"  {k_y_range[i]:8.3f}  {np.abs(M_hat[i]):10.6f}  "
              f"{omega[i]:12.6f}  {decay[i]:10.6f}  "
              f"{E_ky[i].real:12.4f}  {E_ky[i].imag:12.4f}")

    return k_y_range, omega, decay, E_ky, M_hat


# ── Part 4: Light cone vs parabola fitting ─────────────────────────
def fit_dispersion_surface(k_y, omega_data, label=""):
    """Fit omega(k_y) to light-cone and parabolic models."""
    print(f"\n  Dispersion fits ({label}):")

    # Clean data
    mask = np.isfinite(k_y) & np.isfinite(omega_data)
    ky = k_y[mask]
    om = omega_data[mask]

    if len(ky) < 5:
        print("    Too few data points for fitting.")
        return {}

    results = {}

    # 1. Lorentzian: omega^2 = m^2 + c^2 * k_y^2
    #    => fit omega^2 vs k_y^2 linearly
    om2 = om**2
    ky2 = ky**2
    mask_pos = om2 > 0  # need positive omega^2
    if np.sum(mask_pos) > 3:
        try:
            popt, _ = curve_fit(lorentzian_fit, ky2[mask_pos], om2[mask_pos],
                                p0=[om2[mask_pos].min(), 1.0], maxfev=5000)
            pred = lorentzian_fit(ky2[mask_pos], *popt)
            r2 = compute_r2(om2[mask_pos], pred)
            results["lorentzian"] = {"params": popt, "R2": r2,
                                     "desc": f"omega^2 = {popt[0]:.4f} + {popt[1]:.4f}*k_y^2"}
            print(f"    Lorentzian (omega^2 = m^2 + c^2*ky^2): R^2 = {r2:.6f}")
            print(f"      m^2 = {popt[0]:.6f}, c^2 = {popt[1]:.6f}")
            if popt[0] > 0:
                print(f"      effective mass m = {np.sqrt(abs(popt[0])):.6f}")
            if popt[1] > 0:
                print(f"      effective speed c = {np.sqrt(abs(popt[1])):.6f}")
        except Exception as e:
            print(f"    Lorentzian fit failed: {e}")
            results["lorentzian"] = {"R2": -1}

    # 2. Schrodinger: omega = E0 + alpha * k_y^2
    try:
        popt, _ = curve_fit(schrodinger_fit, ky2, om,
                            p0=[om.min(), 0.1], maxfev=5000)
        pred = schrodinger_fit(ky2, *popt)
        r2 = compute_r2(om, pred)
        results["schrodinger"] = {"params": popt, "R2": r2,
                                   "desc": f"omega = {popt[0]:.4f} + {popt[1]:.4f}*k_y^2"}
        print(f"    Schrodinger (omega = E0 + alpha*ky^2): R^2 = {r2:.6f}")
        print(f"      E0 = {popt[0]:.6f}, alpha = {popt[1]:.6f}")
    except Exception as e:
        print(f"    Schrodinger fit failed: {e}")
        results["schrodinger"] = {"R2": -1}

    # 3. Massless cone: omega = E0 + v*|k_y|
    try:
        popt, _ = curve_fit(linear_fit, ky, om,
                            p0=[om.min(), 1.0], maxfev=5000)
        pred = linear_fit(ky, *popt)
        r2 = compute_r2(om, pred)
        results["linear_cone"] = {"params": popt, "R2": r2,
                                   "desc": f"omega = {popt[0]:.4f} + {popt[1]:.4f}*|k_y|"}
        print(f"    Linear cone (omega = E0 + v*|ky|): R^2 = {r2:.6f}")
        print(f"      E0 = {popt[0]:.6f}, v = {popt[1]:.6f}")
    except Exception as e:
        print(f"    Linear cone fit failed: {e}")
        results["linear_cone"] = {"R2": -1}

    # 4. Lattice: omega = E0 + b*(1 - cos(k_y * h)) / h^2
    try:
        def lattice_fn(ky_arr, E0, b):
            return E0 + b * (1.0 - np.cos(ky_arr * H_STEP)) / H_STEP**2
        popt, _ = curve_fit(lattice_fn, ky, om,
                            p0=[om.min(), 0.1], maxfev=5000)
        pred = lattice_fn(ky, *popt)
        r2 = compute_r2(om, pred)
        results["lattice"] = {"params": popt, "R2": r2,
                               "desc": f"omega = {popt[0]:.4f} + {popt[1]:.4f}*(1-cos(ky*h))/h^2"}
        print(f"    Lattice (omega = E0 + b*(1-cos(ky*h))/h^2): R^2 = {r2:.6f}")
        print(f"      E0 = {popt[0]:.6f}, b = {popt[1]:.6f}")
    except Exception as e:
        print(f"    Lattice fit failed: {e}")
        results["lattice"] = {"R2": -1}

    # Best fit
    if results:
        best = max(results, key=lambda m: results[m].get("R2", -1))
        best_r2 = results[best]["R2"]
        print(f"\n    BEST FIT: {best} (R^2 = {best_r2:.6f})")
        if best_r2 > 0.95:
            print(f"    => EXCELLENT fit")
        elif best_r2 > 0.8:
            print(f"    => GOOD fit")
        elif best_r2 > 0.5:
            print(f"    => MODERATE fit")
        else:
            print(f"    => POOR fit — dispersion may be novel")

    return results


# ── Part 5: ASCII dispersion map ──────────────────────────────────
def ascii_dispersion_map(k_y_grid, omega_grid, A):
    """Print a crude ASCII heatmap of the spectral function."""
    print(f"\n  ASCII spectral function A(k_y, omega) [log scale]:")
    print(f"  (rows = omega, cols = k_y, brighter = stronger)")

    # Downsample for display
    n_rows = 30
    n_cols = 40
    n_ky = len(k_y_grid)
    n_om = len(omega_grid)

    ky_idx = np.linspace(0, n_ky - 1, n_cols).astype(int)
    om_idx = np.linspace(0, n_om - 1, n_rows).astype(int)

    A_sub = A[np.ix_(ky_idx, om_idx)].T  # (n_rows, n_cols)
    log_A = np.log10(A_sub + 1e-30)

    vmin = np.percentile(log_A[np.isfinite(log_A)], 10)
    vmax = np.max(log_A[np.isfinite(log_A)])

    chars = " .:-=+*#@"
    n_chars = len(chars)

    # Header
    print(f"  omega\\k_y", end="")
    for j in range(0, n_cols, 10):
        print(f"  {k_y_grid[ky_idx[j]]:6.2f}", end="")
    print()

    for i in range(n_rows - 1, -1, -1):
        omega_val = omega_grid[om_idx[i]]
        print(f"  {omega_val:6.2f} |", end="")
        for j in range(n_cols):
            val = log_A[i, j]
            if not np.isfinite(val):
                print(" ", end="")
                continue
            normalized = (val - vmin) / max(vmax - vmin, 1e-10)
            normalized = np.clip(normalized, 0, 1)
            char_idx = int(normalized * (n_chars - 1))
            print(chars[char_idx], end="")
        print("|")

    print(f"         ", end="")
    print("-" * (n_cols + 2))


# ── Main experiment ─────────────────────────────────────────────────
def run_experiment():
    print("=" * 78)
    print("FULL 2D DISPERSION SURFACE FROM DAG PROPAGATOR")
    print("=" * 78)
    print(f"\nParameters:")
    print(f"  H_transverse = {H_TRANSVERSE} (n_y = {2*H_TRANSVERSE+1})")
    print(f"  k_phase = {K_PHASE}")
    print(f"  p = {P_ATTEN}")
    print(f"  h = {H_STEP}")
    print(f"  n_layers_max = {N_LAYERS_MAX}")
    print(f"  Kernels: {list(KERNELS.keys())}")

    all_results = {}

    for kernel_name, kernel_fn in KERNELS.items():
        print(f"\n\n{'=' * 78}")
        print(f"KERNEL: {kernel_name}")
        print(f"{'=' * 78}")

        # ── Part 1: Eigenvalue dispersion
        k_y_eig, E_eig, lam_eig, all_lam, all_evec = eigenvalue_dispersion(
            kernel_name, kernel_fn, H_STEP)

        # Fit eigenvalue dispersion
        omega_eig = E_eig.real
        mask_prop = np.abs(k_y_eig) > 0.01  # skip near-zero k_y
        if np.sum(mask_prop) > 3:
            eig_fits = fit_dispersion_surface(
                np.abs(k_y_eig[mask_prop]), omega_eig[mask_prop],
                label="eigenvalue modes")
        else:
            eig_fits = {}
            print("    Too few modes with nonzero k_y for eigenvalue fit.")

        # ── Part 2: Green's function spectrum
        ky_gf, omega_gf, A_gf, omega_peaks, A_peaks = greens_function_spectrum(
            kernel_name, kernel_fn, H_STEP, N_LAYERS_MAX)

        # ASCII map
        ascii_dispersion_map(ky_gf, omega_gf, A_gf)

        # Fit spectral peaks (positive k_y half)
        pos_mask = ky_gf > 0.1
        if np.sum(pos_mask) > 5:
            gf_fits = fit_dispersion_surface(
                ky_gf[pos_mask], omega_peaks[pos_mask],
                label="spectral peaks (positive k_y)")
        else:
            gf_fits = {}

        # ── Part 3: Momentum-space dispersion
        ky_mom, omega_mom, decay_mom, E_mom, Mhat = momentum_space_dispersion(
            kernel_name, kernel_fn, H_STEP)

        # Fit momentum-space dispersion (use phase velocity omega)
        mask_valid = np.isfinite(omega_mom) & (ky_mom > 0.1)
        if np.sum(mask_valid) > 5:
            mom_fits = fit_dispersion_surface(
                ky_mom[mask_valid], omega_mom[mask_valid],
                label="momentum-space phase velocity")
        else:
            mom_fits = {}

        # ── Light cone test: check omega vs |k_y| at small k_y
        print(f"\n{'─' * 78}")
        print(f"LIGHT CONE TEST — kernel={kernel_name}")
        print(f"{'─' * 78}")

        # Use momentum-space data (cleanest)
        small_k_mask = (ky_mom > 0.1) & (ky_mom < np.pi / (2 * H_STEP))
        ky_small = ky_mom[small_k_mask]
        om_small = omega_mom[small_k_mask]

        if len(ky_small) > 5:
            # Test: is omega^2 linear in k_y^2?
            om2 = om_small**2
            ky2 = ky_small**2

            # Linear fit: omega^2 = a + b * k_y^2
            coeffs = np.polyfit(ky2, om2, 1)
            pred = np.polyval(coeffs, ky2)
            r2_cone = compute_r2(om2, pred)

            # Quadratic fit: omega = a + b * k_y^2
            coeffs2 = np.polyfit(ky2, om_small, 1)
            pred2 = np.polyval(coeffs2, ky2)
            r2_para = compute_r2(om_small, pred2)

            print(f"\n  Small-k regime (k_y in [{ky_small[0]:.3f}, {ky_small[-1]:.3f}]):")
            print(f"  Light cone (omega^2 = a + b*ky^2): R^2 = {r2_cone:.6f}")
            print(f"    a = {coeffs[1]:.6f}, b = {coeffs[0]:.6f}")
            print(f"  Parabolic (omega = E0 + alpha*ky^2): R^2 = {r2_para:.6f}")
            print(f"    E0 = {coeffs2[1]:.6f}, alpha = {coeffs2[0]:.6f}")

            if r2_cone > r2_para and r2_cone > 0.9:
                print(f"\n  => LIGHT CONE detected (omega^2 ~ k_y^2)")
                print(f"     Effective speed c = {np.sqrt(abs(coeffs[0])):.6f}")
            elif r2_para > r2_cone and r2_para > 0.9:
                print(f"\n  => PARABOLIC dispersion (omega ~ k_y^2)")
                print(f"     Effective mass parameter alpha = {coeffs2[0]:.6f}")
            else:
                print(f"\n  => AMBIGUOUS: neither model dominates")
                print(f"     R^2 difference: {abs(r2_cone - r2_para):.6f}")

            # Additional: check curvature of omega(k_y)
            d_omega = np.gradient(om_small, ky_small)
            d2_omega = np.gradient(d_omega, ky_small)
            mean_curvature = np.mean(d2_omega)
            print(f"\n  Mean curvature d^2(omega)/dk_y^2 = {mean_curvature:.6f}")
            if abs(mean_curvature) < 0.1 * abs(np.mean(d_omega)):
                print(f"  => Nearly LINEAR omega(k_y) — consistent with light cone")
            else:
                print(f"  => Significant curvature — not a simple cone")

        all_results[kernel_name] = {
            "eig_fits": eig_fits,
            "gf_fits": gf_fits,
            "mom_fits": mom_fits,
        }

    # ── FINAL SUMMARY ──────────────────────────────────────────────────
    print(f"\n\n{'=' * 78}")
    print("FINAL SUMMARY: 2D DISPERSION CLASSIFICATION")
    print(f"{'=' * 78}")

    for kernel_name in KERNELS:
        r = all_results[kernel_name]
        print(f"\n  Kernel: {kernel_name}")

        for method_name, fits in [("eigenvalue", r["eig_fits"]),
                                   ("Green's fn", r["gf_fits"]),
                                   ("momentum-space", r["mom_fits"])]:
            if not fits:
                print(f"    {method_name}: no fit data")
                continue

            best = max(fits, key=lambda m: fits[m].get("R2", -1))
            best_r2 = fits[best].get("R2", -1)
            print(f"    {method_name}: best = {best} (R^2 = {best_r2:.4f})")

    # ── HYPOTHESIS VERDICT ─────────────────────────────────────────────
    print(f"\n{'=' * 78}")
    print("HYPOTHESIS VERDICT")
    print(f"{'=' * 78}")
    print(f"\nHypothesis: The 2D dispersion surface has a light-cone shape")
    print(f"  (omega^2 ~ k_y^2) at fine lattice spacing.\n")

    # Check all momentum-space fits for lorentzian dominance
    light_cone_count = 0
    parabolic_count = 0
    total_tests = 0

    for kernel_name in KERNELS:
        r = all_results[kernel_name]
        for method_name, fits in [("eigenvalue", r["eig_fits"]),
                                   ("Green's fn", r["gf_fits"]),
                                   ("momentum-space", r["mom_fits"])]:
            if not fits:
                continue
            total_tests += 1
            best = max(fits, key=lambda m: fits[m].get("R2", -1))
            if best in ("lorentzian", "linear_cone"):
                light_cone_count += 1
            elif best in ("schrodinger", "lattice"):
                parabolic_count += 1

    print(f"  Tests performed: {total_tests}")
    print(f"  Light-cone wins: {light_cone_count}")
    print(f"  Parabolic wins:  {parabolic_count}")

    if light_cone_count > parabolic_count and light_cone_count > 0:
        print(f"\n  SUPPORTED: Dispersion is predominantly light-cone-like.")
        print(f"  The propagator encodes Lorentzian (relativistic) geometry.")
    elif parabolic_count > light_cone_count and parabolic_count > 0:
        print(f"\n  FALSIFIED: Dispersion is predominantly parabolic.")
        print(f"  The propagator encodes Euclidean (Schrodinger) geometry at h={H_STEP}.")
        print(f"  Light cone may emerge only at smaller h.")
    elif total_tests == 0:
        print(f"\n  INCONCLUSIVE: No valid fits obtained.")
    else:
        print(f"\n  MIXED: Results depend on method. No clear winner.")
        print(f"  Both Lorentzian and Euclidean features present.")

    print(f"\n{'=' * 78}")
    print("EXPERIMENT COMPLETE")
    print(f"{'=' * 78}")


if __name__ == "__main__":
    run_experiment()
