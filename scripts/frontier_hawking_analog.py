#!/usr/bin/env python3
"""Hawking analog: thermal spectrum near propagator horizon where f -> 1.

Physics
-------
The path-sum propagator uses action S = L(1 - f).  When f -> 1 the action
vanishes, phase freezes, and amplitude cannot propagate further inward.
The surface f = 1 is therefore a *propagator horizon*.

Near this horizon the phase gradient creates an effective surface gravity:
    kappa = |df/dr| evaluated at f = 1

If the framework produces Hawking-like radiation, an outgoing wavepacket
initialized just outside the horizon should thermalize with temperature
    T_H ~ kappa / (2 * pi)
and the outgoing energy spectrum should resemble a Planck/Bose-Einstein
distribution.

Method
------
1. Place a strong point mass at the center of a 3D lattice so the Poisson
   field f(r) = s / (4*pi*r) reaches f ~ 1 at some radius r_h.
2. Build layer-by-layer transfer matrices M(x) that encode the propagator
   amplitude for one step in the radial (x) direction at each transverse
   position (y, z), with the local field f(x, y, z) entering the action.
3. Initialize a Gaussian wavepacket in the transverse plane just outside r_h.
4. Evolve outward layer by layer: psi(x+1) = M(x) @ psi(x).
5. At a far-field "detector" plane, Fourier-transform the transverse
   wavefunction to get the momentum-space distribution |psi(k)|^2.
6. Test whether ln|psi(k)|^2 vs k^2 is linear (thermal / Gaussian).
7. Extract effective temperature T = 1 / (2 |slope|) and check T ~ kappa.
8. Repeat for a control wavepacket far from the horizon (should NOT thermalize).

Falsification
-------------
- If R^2(ln|psi|^2 vs k^2) < 0.5 near the horizon, no thermal spectrum.
- If T_near ~ T_far (control), any thermality is geometric, not horizon-induced.
- If T does not scale with kappa, Hawking scaling is falsified.

Infrastructure: Poisson solver from distance_law_3d_64_closure.py / emergent_gr.
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np

try:
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


# ===========================================================================
# Poisson solver (from existing infrastructure)
# ===========================================================================

def solve_poisson_sparse(N: int, mass_pos: tuple[int, int, int],
                         mass_strength: float = 1.0) -> np.ndarray:
    """Solve 3D Poisson equation with Dirichlet BC using sparse solver."""
    M_int = N - 2
    n_interior = M_int * M_int * M_int

    def idx(i, j, k):
        return i * M_int * M_int + j * M_int + k

    rows, cols, vals = [], [], []
    rhs = np.zeros(n_interior)
    mx, my, mz = mass_pos
    mi, mj, mk = mx - 1, my - 1, mz - 1

    for i in range(M_int):
        for j in range(M_int):
            for k in range(M_int):
                c = idx(i, j, k)
                rows.append(c); cols.append(c); vals.append(-6.0)
                if i > 0:
                    rows.append(c); cols.append(idx(i-1, j, k)); vals.append(1.0)
                if i < M_int - 1:
                    rows.append(c); cols.append(idx(i+1, j, k)); vals.append(1.0)
                if j > 0:
                    rows.append(c); cols.append(idx(i, j-1, k)); vals.append(1.0)
                if j < M_int - 1:
                    rows.append(c); cols.append(idx(i, j+1, k)); vals.append(1.0)
                if k > 0:
                    rows.append(c); cols.append(idx(i, j, k-1)); vals.append(1.0)
                if k < M_int - 1:
                    rows.append(c); cols.append(idx(i, j, k+1)); vals.append(1.0)
                if i == mi and j == mj and k == mk:
                    rhs[c] = -mass_strength

    A = sparse.csr_matrix((vals, (rows, cols)), shape=(n_interior, n_interior))
    phi_interior = spsolve(A, rhs)

    field = np.zeros((N, N, N))
    for i in range(M_int):
        for j in range(M_int):
            for k in range(M_int):
                field[i+1, j+1, k+1] = phi_interior[idx(i, j, k)]
    return field


def solve_poisson_jacobi(N: int, mass_pos: tuple[int, int, int],
                         mass_strength: float = 1.0,
                         max_iter: int = 8000, tol: float = 1e-7) -> np.ndarray:
    """Fallback Jacobi solver."""
    field = np.zeros((N, N, N))
    source = np.zeros((N, N, N))
    mx, my, mz = mass_pos
    source[mx, my, mz] = mass_strength
    for _ in range(max_iter):
        new = np.zeros_like(field)
        new[1:-1, 1:-1, 1:-1] = (
            field[2:, 1:-1, 1:-1] + field[:-2, 1:-1, 1:-1] +
            field[1:-1, 2:, 1:-1] + field[1:-1, :-2, 1:-1] +
            field[1:-1, 1:-1, 2:] + field[1:-1, 1:-1, :-2] +
            source[1:-1, 1:-1, 1:-1]
        ) / 6.0
        if np.max(np.abs(new - field)) < tol:
            field = new
            break
        field = new
    return field


def solve_poisson(N: int, mass_pos: tuple[int, int, int],
                  mass_strength: float = 1.0) -> np.ndarray:
    if HAS_SCIPY and N <= 50:
        return solve_poisson_sparse(N, mass_pos, mass_strength)
    return solve_poisson_jacobi(N, mass_pos, mass_strength)


# ===========================================================================
# Transfer matrix for one radial layer (x -> x+1)
# ===========================================================================

def build_layer_transfer_matrix(
    field_slice: np.ndarray,
    k_phase: float,
    atten_power: float,
    kernel_fn,
    max_dy: int | None = None,
) -> np.ndarray:
    """Build transfer matrix M for one x-step in a 2D transverse plane.

    field_slice: 2D array of f(y, z) at the current x-layer.
    M[out, in] = exp(i * k * S) * w(theta) / L^p
    where out = (y_out, z_out) flattened, in = (y_in, z_in) flattened,
    L = sqrt(1 + dy^2 + dz^2), S = L * (1 - f_avg), theta = arctan(|dy,dz|/1).
    f_avg = average of f at source and destination (trapezoidal).
    """
    ny, nz = field_slice.shape
    n_sites = ny * nz
    M = np.zeros((n_sites, n_sites), dtype=complex)

    for y_out in range(ny):
        for z_out in range(nz):
            idx_out = y_out * nz + z_out
            f_out = field_slice[y_out, z_out]

            for y_in in range(ny):
                for z_in in range(nz):
                    dy = y_out - y_in
                    dz = z_out - z_in

                    if max_dy is not None and (abs(dy) > max_dy or abs(dz) > max_dy):
                        continue

                    idx_in = y_in * nz + z_in
                    f_in = field_slice[y_in, z_in]

                    L = math.sqrt(1.0 + dy * dy + dz * dz)
                    f_avg = 0.5 * (f_in + f_out)
                    S = L * (1.0 - f_avg)
                    theta = math.atan2(math.sqrt(dy * dy + dz * dz), 1.0)

                    w = kernel_fn(theta)
                    amplitude = np.exp(1j * k_phase * S) * w / (L ** atten_power)
                    M[idx_out, idx_in] = amplitude

    return M


# ===========================================================================
# 1D radial transfer matrix (reduced problem for tractability)
# ===========================================================================

def build_1d_transfer_matrix(
    field_1d: np.ndarray,
    k_phase: float,
    atten_power: float,
    kernel_fn,
    max_dy: int | None = None,
) -> np.ndarray:
    """Transfer matrix for one x-step on a 1D transverse line.

    field_1d: 1D array of f(y) at this x.
    M[y_out, y_in] = exp(i * k * L * (1 - f_avg)) * w(theta) / L^p
    where L = sqrt(1 + dy^2), f_avg = (f[y_out] + f[y_in]) / 2.
    """
    ny = len(field_1d)
    M = np.zeros((ny, ny), dtype=complex)

    for y_out in range(ny):
        f_out = field_1d[y_out]
        for y_in in range(ny):
            dy = y_out - y_in
            if max_dy is not None and abs(dy) > max_dy:
                continue

            f_in = field_1d[y_in]
            L = math.sqrt(1.0 + dy * dy)
            f_avg = 0.5 * (f_in + f_out)
            S = L * (1.0 - f_avg)
            theta = math.atan2(abs(dy), 1.0)
            w = kernel_fn(theta)
            M[y_out, y_in] = np.exp(1j * k_phase * S) * w / (L ** atten_power)

    return M


# ===========================================================================
# Wavepacket construction
# ===========================================================================

def gaussian_wavepacket(ny: int, center: int, sigma: float, k0: float = 0.0) -> np.ndarray:
    """Normalized Gaussian wavepacket in 1D transverse space."""
    y = np.arange(ny, dtype=float)
    psi = np.exp(-0.5 * ((y - center) / sigma) ** 2) * np.exp(1j * k0 * y)
    norm = np.sqrt(np.sum(np.abs(psi) ** 2))
    if norm > 0:
        psi /= norm
    return psi


# ===========================================================================
# Spectral analysis
# ===========================================================================

def analyze_spectrum(psi: np.ndarray) -> dict:
    """Fourier-transform transverse wavefunction and test for thermal shape.

    Returns dict with:
      k_values, power, thermal_fit (a, b, r2), temperature
    """
    n = len(psi)
    fft_psi = np.fft.fft(psi)
    power = np.abs(fft_psi) ** 2

    # Use positive-frequency half
    freqs = np.fft.fftfreq(n)
    half = n // 2
    k_idx = np.arange(1, half)
    k_vals = 2 * np.pi * np.abs(freqs[k_idx])
    pk = power[k_idx]

    # Filter out zeros
    mask = pk > 1e-30
    if mask.sum() < 3:
        return {
            "k_values": k_vals,
            "power": pk,
            "thermal_fit": (0.0, 0.0, 0.0),
            "temperature": float("inf"),
            "label": "INSUFFICIENT DATA",
        }

    k2 = (k_vals[mask]) ** 2
    ln_pk = np.log(pk[mask])

    # Linear regression: ln(pk) = a + b * k^2
    n_pts = len(k2)
    sx = k2.sum()
    sy = ln_pk.sum()
    sxx = (k2 ** 2).sum()
    sxy = (k2 * ln_pk).sum()
    syy = (ln_pk ** 2).sum()

    denom = n_pts * sxx - sx * sx
    if abs(denom) < 1e-30:
        return {
            "k_values": k_vals,
            "power": pk,
            "thermal_fit": (0.0, 0.0, 0.0),
            "temperature": float("inf"),
            "label": "DEGENERATE",
        }

    b = (n_pts * sxy - sx * sy) / denom
    a = (sy - b * sx) / n_pts

    ss_res = ((ln_pk - (a + b * k2)) ** 2).sum()
    y_mean = sy / n_pts
    ss_tot = ((ln_pk - y_mean) ** 2).sum()
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

    temperature = 1.0 / (2.0 * abs(b)) if abs(b) > 1e-30 else float("inf")

    if r2 > 0.9:
        label = "THERMAL"
    elif r2 > 0.5:
        label = "MARGINAL"
    else:
        label = "NOT THERMAL"

    return {
        "k_values": k_vals,
        "power": pk,
        "thermal_fit": (a, b, r2),
        "temperature": temperature,
        "label": label,
    }


def analyze_spectrum_planck(psi: np.ndarray) -> dict:
    """Test for Planck/Bose-Einstein shape: P(k) ~ k^2 / (exp(k/T) - 1).

    In addition to the Gaussian thermal test, check if the power spectrum
    follows a Planck distribution (appropriate for bosonic modes).
    """
    n = len(psi)
    fft_psi = np.fft.fft(psi)
    power = np.abs(fft_psi) ** 2

    freqs = np.fft.fftfreq(n)
    half = n // 2
    k_idx = np.arange(1, half)
    k_vals = 2 * np.pi * np.abs(freqs[k_idx])
    pk = power[k_idx]

    mask = (pk > 1e-30) & (k_vals > 1e-10)
    if mask.sum() < 4:
        return {"planck_r2": 0.0, "planck_T": float("inf")}

    k_m = k_vals[mask]
    pk_m = pk[mask]

    # For Planck: P(k) = C * k^2 / (exp(k/T) - 1)
    # => ln(P/k^2) = ln(C) - ln(exp(k/T) - 1)
    # For large k/T: ln(P/k^2) ~ ln(C) - k/T  (Wien tail)
    # Test the Wien approximation: ln(P/k^2) vs k should be linear
    ln_ratio = np.log(pk_m / (k_m ** 2 + 1e-30))
    n_pts = len(k_m)
    sx = k_m.sum()
    sy = ln_ratio.sum()
    sxx = (k_m ** 2).sum()
    sxy = (k_m * ln_ratio).sum()

    denom = n_pts * sxx - sx * sx
    if abs(denom) < 1e-30:
        return {"planck_r2": 0.0, "planck_T": float("inf")}

    slope = (n_pts * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / n_pts

    ss_res = ((ln_ratio - (intercept + slope * k_m)) ** 2).sum()
    y_mean = sy / n_pts
    ss_tot = ((ln_ratio - y_mean) ** 2).sum()
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

    T_planck = -1.0 / slope if slope < 0 else float("inf")

    return {"planck_r2": r2, "planck_T": T_planck}


# ===========================================================================
# Surface gravity computation
# ===========================================================================

def compute_surface_gravity(field_radial: np.ndarray, r_values: np.ndarray) -> tuple[float, float]:
    """Compute surface gravity kappa = |df/dr| at the f=1 surface.

    Returns (kappa, r_horizon) where r_horizon is interpolated.
    If f never reaches 1, returns (kappa_at_max_f, r_of_max_f).
    """
    # Find where f crosses 1 (or gets closest)
    max_f = np.max(field_radial)
    if max_f < 1.0:
        # No true horizon; report gradient at location of max f
        idx_max = np.argmax(field_radial)
        if idx_max == 0 or idx_max >= len(field_radial) - 1:
            return 0.0, r_values[idx_max]
        df_dr = abs(field_radial[idx_max + 1] - field_radial[idx_max - 1]) / (
            r_values[idx_max + 1] - r_values[idx_max - 1]
        )
        return df_dr, r_values[idx_max]

    # Find first crossing from above 1 to below 1 (going outward)
    for i in range(len(field_radial) - 1):
        if field_radial[i] >= 1.0 and field_radial[i + 1] < 1.0:
            # Linear interpolation for horizon radius
            f0, f1 = field_radial[i], field_radial[i + 1]
            r0, r1 = r_values[i], r_values[i + 1]
            r_h = r0 + (1.0 - f0) * (r1 - r0) / (f1 - f0)
            df_dr = abs(f1 - f0) / (r1 - r0)
            return df_dr, r_h

    return 0.0, r_values[0]


# ===========================================================================
# Main experiment
# ===========================================================================

def run_experiment():
    t0 = time.time()

    # ---- Parameters ----
    N = 41                 # lattice size (odd for centered mass)
    mid = N // 2           # center index
    k_phase = 6.0          # wavenumber
    atten_power = 1.0      # 1/L^p with p=1 for 3D
    sigma_wavepacket = 3.0 # Gaussian width
    max_dy = 5             # transverse coupling range (for tractability)

    kernel_fn = lambda theta: np.cos(theta) ** 2  # cos^2 kernel

    # Mass strengths: we need f ~ 1 at some radius r_h
    # The Poisson solution on an N^3 grid with Dirichlet BC gives
    # f ~ mass_strength / (4*pi*r) near the center.
    # For f(r_h) = 1 we need mass_strength / (4*pi*r_h) ~ 1.
    # With r_h = 5, we need mass_strength ~ 4*pi*5 ~ 63.
    # We use several strengths to get different surface gravities.
    mass_strengths = [40.0, 60.0, 80.0, 120.0]

    print("=" * 78)
    print("HAWKING ANALOG: THERMAL SPECTRUM NEAR PROPAGATOR HORIZON")
    print("=" * 78)
    print()
    print(f"Lattice:       {N}^3 = {N**3} sites")
    print(f"Mass at:       ({mid}, {mid}, {mid})")
    print(f"Wavenumber:    k = {k_phase}")
    print(f"Attenuation:   p = {atten_power}")
    print(f"Kernel:        cos^2(theta)")
    print(f"Max dy:        {max_dy}")
    print(f"Wavepacket:    sigma = {sigma_wavepacket}")
    print(f"Mass strengths: {mass_strengths}")
    print()

    # We work in a 1D transverse slice at z = mid for tractability.
    # The full 3D field is solved, but propagation is done in the
    # (x, y) plane at z = mid.
    ny_slice = N  # transverse size in y at z = mid

    # ===================================================================
    # PART 0: Characterize the field profile
    # ===================================================================
    print("-" * 78)
    print("PART 0: FIELD PROFILE AND HORIZON LOCATION")
    print("-" * 78)
    print()

    field_data = {}  # mass_strength -> (field_3d, field_radial, r_values, kappa, r_h)

    for ms in mass_strengths:
        print(f"  Solving Poisson for mass_strength = {ms:.1f} ...")
        field_3d = solve_poisson(N, (mid, mid, mid), ms)

        # Extract radial profile along y=mid, z=mid (i.e., along x from center)
        r_values = []
        f_radial = []
        for x in range(mid + 1, N - 1):
            r = x - mid
            r_values.append(r)
            f_radial.append(field_3d[x, mid, mid])

        r_arr = np.array(r_values, dtype=float)
        f_arr = np.array(f_radial, dtype=float)

        max_f = np.max(f_arr) if len(f_arr) > 0 else 0.0
        kappa, r_h = compute_surface_gravity(f_arr, r_arr)

        field_data[ms] = (field_3d, f_arr, r_arr, kappa, r_h)

        print(f"    max f = {max_f:.4f}")
        print(f"    horizon? {'YES' if max_f >= 1.0 else 'NO (f < 1 everywhere)'}")
        print(f"    r_h = {r_h:.2f},  kappa = {kappa:.4f}")

        # Print radial profile
        print(f"    {'r':>4}  {'f(r)':>10}  {'1-f':>10}")
        for i in range(min(len(r_values), 15)):
            f_val = f_radial[i]
            print(f"    {r_values[i]:4d}  {f_val:10.4f}  {1.0 - f_val:10.4f}")
        print()

    # ===================================================================
    # PART 1: Evolve wavepacket near horizon (outward)
    # ===================================================================
    print("-" * 78)
    print("PART 1: WAVEPACKET EVOLUTION NEAR HORIZON")
    print("-" * 78)
    print()
    print("Method: initialize Gaussian wavepacket in transverse y just outside r_h.")
    print("Evolve outward layer by layer using the transfer matrix M(x).")
    print("Measure the transverse Fourier spectrum at the detector plane.")
    print()

    near_horizon_results = {}  # ms -> dict

    for ms in mass_strengths:
        field_3d, f_arr, r_arr, kappa, r_h = field_data[ms]

        # Start wavepacket just outside the horizon
        # x_start = mid + int(ceil(r_h)) + 1 (just outside horizon)
        r_h_int = int(math.ceil(r_h))
        x_start = mid + max(r_h_int + 1, 2)
        x_end = N - 2  # stop before boundary

        if x_start >= x_end - 3:
            print(f"  ms={ms:.1f}: horizon too close to boundary, skipping.")
            near_horizon_results[ms] = None
            continue

        n_layers = x_end - x_start

        # Initialize wavepacket centered on the transverse midpoint
        psi = gaussian_wavepacket(ny_slice, mid, sigma_wavepacket)

        # Evolve outward layer by layer
        norms = [np.sum(np.abs(psi) ** 2)]

        for x in range(x_start, x_end):
            # Extract the field along y at this x, z=mid
            field_1d = field_3d[x, :, mid].copy()

            # Build the transfer matrix for this layer
            M_layer = build_1d_transfer_matrix(
                field_1d, k_phase, atten_power, kernel_fn, max_dy=max_dy
            )

            # Evolve
            psi = M_layer @ psi
            norms.append(np.sum(np.abs(psi) ** 2))

        # Analyze the outgoing spectrum
        spec = analyze_spectrum(psi)
        planck = analyze_spectrum_planck(psi)

        near_horizon_results[ms] = {
            "x_start": x_start,
            "x_end": x_end,
            "n_layers": n_layers,
            "final_norm": norms[-1],
            "norm_ratio": norms[-1] / norms[0] if norms[0] > 0 else 0,
            "spectrum": spec,
            "planck": planck,
            "kappa": kappa,
            "r_h": r_h,
        }

        a, b, r2 = spec["thermal_fit"]
        print(f"  ms={ms:.1f}: x={x_start}->{x_end} ({n_layers} layers), r_h={r_h:.2f}")
        print(f"    kappa = {kappa:.4f}")
        print(f"    ||psi||^2 initial: {norms[0]:.6f}, final: {norms[-1]:.4e}")
        print(f"    Gaussian thermal: a={a:+.4f} b={b:+.6f} R^2={r2:.4f} T={spec['temperature']:.4f} [{spec['label']}]")
        print(f"    Planck (Wien):    R^2={planck['planck_r2']:.4f} T={planck['planck_T']:.4f}")
        print()

    # ===================================================================
    # PART 2: CONTROL -- Wavepacket far from horizon
    # ===================================================================
    print("-" * 78)
    print("PART 2: CONTROL -- WAVEPACKET FAR FROM HORIZON")
    print("-" * 78)
    print()
    print("Same lattice and field, but wavepacket starts in far-field where f ~ 0.")
    print()

    far_field_results = {}

    for ms in mass_strengths:
        field_3d, f_arr, r_arr, kappa, r_h = field_data[ms]

        if near_horizon_results.get(ms) is None:
            far_field_results[ms] = None
            continue

        # Start in far field: outer third of lattice
        x_start_far = N - 2 - (N - 2 - mid) // 3
        x_end_far = N - 2
        if x_start_far >= x_end_far - 3:
            x_start_far = x_end_far - 5

        n_layers_far = x_end_far - x_start_far

        psi_far = gaussian_wavepacket(ny_slice, mid, sigma_wavepacket)
        norms_far = [np.sum(np.abs(psi_far) ** 2)]

        for x in range(x_start_far, x_end_far):
            field_1d = field_3d[x, :, mid].copy()
            M_layer = build_1d_transfer_matrix(
                field_1d, k_phase, atten_power, kernel_fn, max_dy=max_dy
            )
            psi_far = M_layer @ psi_far
            norms_far.append(np.sum(np.abs(psi_far) ** 2))

        spec_far = analyze_spectrum(psi_far)
        planck_far = analyze_spectrum_planck(psi_far)

        far_field_results[ms] = {
            "x_start": x_start_far,
            "x_end": x_end_far,
            "n_layers": n_layers_far,
            "final_norm": norms_far[-1],
            "norm_ratio": norms_far[-1] / norms_far[0] if norms_far[0] > 0 else 0,
            "spectrum": spec_far,
            "planck": planck_far,
        }

        a_f, b_f, r2_f = spec_far["thermal_fit"]
        print(f"  ms={ms:.1f}: x={x_start_far}->{x_end_far} ({n_layers_far} layers)")
        print(f"    f at start: {field_3d[x_start_far, mid, mid]:.6f}")
        print(f"    Gaussian thermal: a={a_f:+.4f} b={b_f:+.6f} R^2={r2_f:.4f} T={spec_far['temperature']:.4f} [{spec_far['label']}]")
        print(f"    Planck (Wien):    R^2={planck_far['planck_r2']:.4f} T={planck_far['planck_T']:.4f}")
        print()

    # ===================================================================
    # PART 3: FREE-FIELD CONTROL (no mass at all)
    # ===================================================================
    print("-" * 78)
    print("PART 3: FREE-FIELD CONTROL (no gravitational field)")
    print("-" * 78)
    print()

    # Free field: f=0 everywhere
    field_free = np.zeros(ny_slice)
    M_free = build_1d_transfer_matrix(
        field_free, k_phase, atten_power, kernel_fn, max_dy=max_dy
    )

    # Same number of layers as the longest near-horizon run
    max_layers = max(
        (near_horizon_results[ms]["n_layers"]
         for ms in mass_strengths if near_horizon_results.get(ms) is not None),
        default=10,
    )

    psi_free = gaussian_wavepacket(ny_slice, mid, sigma_wavepacket)
    for _ in range(max_layers):
        psi_free = M_free @ psi_free

    spec_free = analyze_spectrum(psi_free)
    planck_free = analyze_spectrum_planck(psi_free)
    a0, b0, r2_0 = spec_free["thermal_fit"]

    print(f"  {max_layers} layers with f=0 everywhere")
    print(f"  Gaussian thermal: a={a0:+.4f} b={b0:+.6f} R^2={r2_0:.4f} T={spec_free['temperature']:.4f} [{spec_free['label']}]")
    print(f"  Planck (Wien):    R^2={planck_free['planck_r2']:.4f} T={planck_free['planck_T']:.4f}")
    print()

    # ===================================================================
    # PART 4: HAWKING SCALING -- T vs kappa
    # ===================================================================
    print("-" * 78)
    print("PART 4: HAWKING SCALING -- T vs SURFACE GRAVITY kappa")
    print("-" * 78)
    print()
    print("  Hawking prediction: T = kappa / (2*pi)")
    print("  Test: does T_near scale linearly with kappa?")
    print()

    kappa_T_pairs = []
    print(f"  {'ms':>8}  {'kappa':>10}  {'T_near':>10}  {'T_far':>10}  {'T_near/kappa':>14}  {'label':>12}")

    for ms in mass_strengths:
        if near_horizon_results.get(ms) is None:
            continue

        nr = near_horizon_results[ms]
        fr = far_field_results.get(ms)
        T_near = nr["spectrum"]["temperature"]
        T_far = fr["spectrum"]["temperature"] if fr is not None else float("inf")
        kappa_val = nr["kappa"]

        ratio = T_near / kappa_val if kappa_val > 1e-10 else float("inf")
        kappa_T_pairs.append((kappa_val, T_near))

        print(f"  {ms:8.1f}  {kappa_val:10.4f}  {T_near:10.4f}  {T_far:10.4f}  {ratio:14.4f}  [{nr['spectrum']['label']}]")

    print()

    # Fit T_near = c0 + c1 * kappa
    if len(kappa_T_pairs) >= 3:
        kappas = np.array([kv for kv, _ in kappa_T_pairs])
        temps = np.array([tv for _, tv in kappa_T_pairs])

        n_pts = len(kappas)
        sx = kappas.sum()
        sy = temps.sum()
        sxx = (kappas ** 2).sum()
        sxy = (kappas * temps).sum()
        denom = n_pts * sxx - sx * sx

        if abs(denom) > 1e-30:
            c1 = (n_pts * sxy - sx * sy) / denom
            c0 = (sy - c1 * sx) / n_pts
            ss_res = ((temps - (c0 + c1 * kappas)) ** 2).sum()
            y_mean = sy / n_pts
            ss_tot = ((temps - y_mean) ** 2).sum()
            r2_scaling = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

            print(f"  Linear fit: T = {c0:.4f} + {c1:.4f} * kappa")
            print(f"  R^2 = {r2_scaling:.4f}")
            print(f"  Hawking predicts c1 = 1/(2*pi) = {1/(2*math.pi):.4f}")
            print(f"  Measured c1 = {c1:.4f}")
            print()

            if r2_scaling > 0.9 and abs(c1) > 1e-6:
                print("  T vs kappa: LINEAR SCALING (R^2 > 0.9)")
            elif r2_scaling > 0.5:
                print("  T vs kappa: MARGINAL linear scaling")
            else:
                print("  T vs kappa: NO linear scaling (R^2 < 0.5)")
        else:
            r2_scaling = 0.0
            c1 = 0.0
            print("  Degenerate fit (all kappas identical)")
    else:
        r2_scaling = 0.0
        c1 = 0.0
        print("  Too few data points for scaling fit")

    print()

    # ===================================================================
    # PART 5: DETAILED SPECTRAL COMPARISON
    # ===================================================================
    print("-" * 78)
    print("PART 5: SPECTRAL COMPARISON (near-horizon vs far-field vs free)")
    print("-" * 78)
    print()

    # Pick the strongest mass for detailed comparison
    best_ms = max(
        (ms for ms in mass_strengths if near_horizon_results.get(ms) is not None),
        default=None,
    )

    if best_ms is not None:
        nr = near_horizon_results[best_ms]
        fr = far_field_results.get(best_ms)

        print(f"  Mass strength: {best_ms:.1f}")
        print()

        # Near-horizon spectrum
        spec_n = nr["spectrum"]
        print(f"  NEAR-HORIZON spectrum (x={nr['x_start']}->{nr['x_end']}):")
        n_show = min(10, len(spec_n["k_values"]))
        print(f"    {'k':>8}  {'|psi_k|^2':>12}  {'ln|psi_k|^2':>14}")
        for i in range(n_show):
            kv = spec_n["k_values"][i]
            pv = spec_n["power"][i]
            ln_pv = math.log(pv) if pv > 0 else float("-inf")
            print(f"    {kv:8.4f}  {pv:12.4e}  {ln_pv:14.4f}")
        print()

        # Far-field spectrum
        if fr is not None:
            spec_f = fr["spectrum"]
            print(f"  FAR-FIELD spectrum (x={fr['x_start']}->{fr['x_end']}):")
            n_show_f = min(10, len(spec_f["k_values"]))
            print(f"    {'k':>8}  {'|psi_k|^2':>12}  {'ln|psi_k|^2':>14}")
            for i in range(n_show_f):
                kv = spec_f["k_values"][i]
                pv = spec_f["power"][i]
                ln_pv = math.log(pv) if pv > 0 else float("-inf")
                print(f"    {kv:8.4f}  {pv:12.4e}  {ln_pv:14.4f}")
            print()

        # Free spectrum
        print(f"  FREE-FIELD spectrum ({max_layers} layers):")
        n_show_0 = min(10, len(spec_free["k_values"]))
        print(f"    {'k':>8}  {'|psi_k|^2':>12}  {'ln|psi_k|^2':>14}")
        for i in range(n_show_0):
            kv = spec_free["k_values"][i]
            pv = spec_free["power"][i]
            ln_pv = math.log(pv) if pv > 0 else float("-inf")
            print(f"    {kv:8.4f}  {pv:12.4e}  {ln_pv:14.4f}")
        print()

    # ===================================================================
    # SUMMARY
    # ===================================================================
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print()

    # Collect verdicts
    n_thermal_near = sum(
        1 for ms in mass_strengths
        if near_horizon_results.get(ms) is not None
        and near_horizon_results[ms]["spectrum"]["thermal_fit"][2] > 0.9
    )
    n_thermal_far = sum(
        1 for ms in mass_strengths
        if far_field_results.get(ms) is not None
        and far_field_results[ms]["spectrum"]["thermal_fit"][2] > 0.9
    )
    n_tested = sum(1 for ms in mass_strengths if near_horizon_results.get(ms) is not None)

    print(f"Near-horizon thermal spectra: {n_thermal_near}/{n_tested}")
    print(f"Far-field thermal spectra:    {n_thermal_far}/{n_tested}")
    print(f"Free-field thermal:           {'YES' if r2_0 > 0.9 else 'NO'} (R^2={r2_0:.4f})")
    print()

    # Key diagnostic: is near-horizon MORE thermal than far-field?
    if n_tested > 0:
        r2_near_vals = [
            near_horizon_results[ms]["spectrum"]["thermal_fit"][2]
            for ms in mass_strengths
            if near_horizon_results.get(ms) is not None
        ]
        r2_far_vals = [
            far_field_results[ms]["spectrum"]["thermal_fit"][2]
            for ms in mass_strengths
            if far_field_results.get(ms) is not None
        ]
        mean_r2_near = np.mean(r2_near_vals) if r2_near_vals else 0
        mean_r2_far = np.mean(r2_far_vals) if r2_far_vals else 0

        print(f"Mean R^2 near horizon: {mean_r2_near:.4f}")
        print(f"Mean R^2 far field:    {mean_r2_far:.4f}")
        print(f"Free-field R^2:        {r2_0:.4f}")
        print()

        # VERDICT
        print("VERDICT:")
        print()

        if mean_r2_near > 0.9 and mean_r2_far < 0.5:
            print("  SUPPORTED: Near-horizon spectrum is thermal, far-field is not.")
            print("  The propagator horizon produces thermal radiation.")
        elif mean_r2_near > 0.9 and mean_r2_far > 0.9:
            print("  AMBIGUOUS: Both near and far spectra are thermal-shaped.")
            print("  The thermal shape may be GEOMETRIC (lattice/kernel artifact),")
            print("  not horizon-induced.")
            if n_thermal_near > 0 and len(kappa_T_pairs) >= 3 and r2_scaling > 0.7:
                print("  However, T scales with kappa, suggesting a horizon contribution.")
            else:
                print("  And T does NOT scale with kappa, so the shape is likely geometric.")
        elif mean_r2_near > 0.5:
            print("  MARGINAL: Near-horizon shows partial thermal features.")
            print("  The signal is too weak for a definitive claim.")
        else:
            print("  FALSIFIED: No thermal spectrum near the horizon.")
            print("  The propagator horizon does NOT produce Hawking-like radiation")
            print("  at this lattice size and with these parameters.")

        # Temperature comparison
        print()
        if near_horizon_results.get(best_ms) is not None:
            T_near_best = near_horizon_results[best_ms]["spectrum"]["temperature"]
            T_free = spec_free["temperature"]
            print(f"  T(near-horizon, ms={best_ms}): {T_near_best:.4f}")
            print(f"  T(free-field):                {T_free:.4f}")
            if T_free < float("inf") and T_near_best < float("inf"):
                print(f"  Ratio T_near/T_free:          {T_near_best/T_free:.4f}")

    elapsed = time.time() - t0
    print()
    print(f"Total runtime: {elapsed:.1f}s")
    print("=" * 78)


if __name__ == "__main__":
    run_experiment()
