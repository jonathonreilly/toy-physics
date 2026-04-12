#!/usr/bin/env python3
"""
Modified Dispersion Relation from Discrete Graph Propagator
============================================================

Extract the dispersion relation omega(k) from the path-sum propagator on
ordered 3D cubic lattices.  On a continuum, omega^2 = k^2 (massless).
On a discrete lattice with spacing h the relation picks up corrections:

    omega^2 = k^2 + c_4 * k^4 + c_6 * k^6 + ...

The k^4 coefficient is a signature of discreteness.  If c_4 ~ h^2, the
correction is the standard lattice artifact.  The energy scale where it
becomes O(1) sets an effective Planck energy E_Planck_eff.

Method:
  Propagate plane waves exp(i k x) through one layer of the path-sum
  transfer kernel on a 3D cubic lattice.  The output phase gives
  omega(k) for that kernel.  Repeat at several lattice spacings h to
  extract how the k^4 coefficient scales.

Architecture comparison:
  - Standard cubic lattice
  - Staggered lattice (checkerboard even/odd sublattice coupling)
  - Wilson lattice (nearest-neighbor doubler-removal term)

Experimental bound:
  Fermi LAT constrains energy-dependent photon speed to
  |v(E) - 1| < O(1) * (E / E_QG)^n with E_QG > ~10^{17.9} GeV (n=1)
  and E_QG > ~10^{10.8} GeV (n=2, the relevant case for k^4 corrections).

Hypothesis:
  The k^4 coefficient scales as h^2 and the architecture dependence is
  bounded (varies by < factor 10 across lattice types).

Falsification:
  If c_4 does not scale as h^2, or if different architectures give
  wildly different coefficients, the model does not make a clean
  Lorentz-violation prediction.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.optimize import curve_fit

np.set_printoptions(precision=10, linewidth=120, suppress=True)


# ── Parameters ──────────────────────────────────────────────────────
K_PHASE = 5.0           # overall phase wavenumber
P_ATTEN = 1.0           # 1/L^p attenuation
H_VALUES = [1.0, 0.5, 0.25, 0.125]
N_TRANSVERSE = 16       # transverse grid half-width (sites: -N..+N)
N_K_POINTS = 200        # number of k_y points for dispersion scan

KERNELS = {
    "cos2":  lambda theta: np.cos(theta)**2,
    "gauss": lambda theta: np.exp(-0.8 * theta**2),
}

# Fermi LAT bounds (n=2, quadratic LIV):
#   E_QG > 10^{10.8} GeV  ~ 6.3e10 GeV
FERMI_LAT_EQG_N2_GEV = 6.3e10
PLANCK_ENERGY_GEV = 1.22e19


# ── Transfer kernel: one layer of path-sum propagator ───────────────

def transfer_kernel_row_cubic(h: float, k: float, p: float,
                              kernel_fn, n_half: int) -> np.ndarray:
    """Compute the Fourier-space transfer kernel M_hat(k_y) for a cubic lattice.

    For a translation-invariant kernel on a 1D transverse slice, the transfer
    matrix M is Toeplitz with entries M(dy).  Its Fourier transform gives
    M_hat(k_y) = sum_dy M(dy) * exp(-i k_y dy h).

    Returns M_hat as a complex array for k_y in [0, pi/h].
    """
    k_y_range = np.linspace(0, np.pi / h, N_K_POINTS, endpoint=False)
    M_hat = np.zeros(N_K_POINTS, dtype=complex)

    dy_range = np.arange(-n_half, n_half + 1)

    for dy in dy_range:
        phys_dy = dy * h
        L = math.sqrt(h**2 + phys_dy**2)
        theta = math.atan2(abs(phys_dy), h)
        w = kernel_fn(theta)
        amplitude = np.exp(1j * k * L) * w * h / (L ** p)
        M_hat += amplitude * np.exp(-1j * k_y_range * dy * h)

    return k_y_range, M_hat


def transfer_kernel_row_staggered(h: float, k: float, p: float,
                                  kernel_fn, n_half: int) -> np.ndarray:
    """Staggered (checkerboard) lattice: only even-parity hops contribute.

    On a staggered lattice, a site at layer x connects to layer x+1
    only at transverse offsets dy where (dy mod 2) == 0 (same sublattice)
    or (dy mod 2) == 1 (opposite sublattice, with sign flip).

    For dispersion: we use the even-sublattice-to-even-sublattice kernel,
    which has stride 2 in transverse direction (effective spacing 2h).
    """
    k_y_range = np.linspace(0, np.pi / h, N_K_POINTS, endpoint=False)
    M_hat = np.zeros(N_K_POINTS, dtype=complex)

    dy_range = np.arange(-n_half, n_half + 1)

    for dy in dy_range:
        # Staggered: even-to-even sublattice coupling
        # Only hops with even dy contribute; odd dy gets a (-1)^dy sign
        stagger_sign = (-1)**abs(dy)
        phys_dy = dy * h
        L = math.sqrt(h**2 + phys_dy**2)
        theta = math.atan2(abs(phys_dy), h)
        w = kernel_fn(theta)
        amplitude = stagger_sign * np.exp(1j * k * L) * w * h / (L ** p)
        M_hat += amplitude * np.exp(-1j * k_y_range * dy * h)

    return k_y_range, M_hat


def transfer_kernel_row_wilson(h: float, k: float, p: float,
                               kernel_fn, n_half: int,
                               r_wilson: float = 1.0) -> np.ndarray:
    """Wilson lattice: add a -r/(2h) * Delta_transverse doubler-removal term.

    Wilson's prescription adds (r/2) * h * k_y^2 to the naive kernel,
    which lifts doubler modes near k_y = pi/h.  In position space this is
    a nearest-neighbor correction to each M(dy) entry.
    """
    k_y_range = np.linspace(0, np.pi / h, N_K_POINTS, endpoint=False)
    M_hat = np.zeros(N_K_POINTS, dtype=complex)

    dy_range = np.arange(-n_half, n_half + 1)

    for dy in dy_range:
        phys_dy = dy * h
        L = math.sqrt(h**2 + phys_dy**2)
        theta = math.atan2(abs(phys_dy), h)
        w = kernel_fn(theta)
        amplitude = np.exp(1j * k * L) * w * h / (L ** p)

        # Wilson correction: multiply each mode by
        # (1 - r * (1 - cos(k_y h))) in Fourier space.
        # In position space, the dy=0 term gets +2r correction,
        # dy=+-1 get -r correction.  Here we apply it in k-space after.
        M_hat += amplitude * np.exp(-1j * k_y_range * dy * h)

    # Apply Wilson factor in Fourier space
    wilson_factor = 1.0 - r_wilson * (1.0 - np.cos(k_y_range * h))
    M_hat *= wilson_factor

    return k_y_range, M_hat


# ── Dispersion extraction ───────────────────────────────────────────

def extract_dispersion(k_y: np.ndarray, M_hat: np.ndarray,
                       h: float) -> tuple[np.ndarray, np.ndarray]:
    """Extract omega(k_y) from M_hat(k_y) = exp(-i omega h).

    omega_re = -arg(M_hat)/h  (use unwrap for continuity)
    omega_im = ln|M_hat|/h    (decay/growth rate)
    """
    # Use unwrapped phase for smooth omega(k)
    phase = np.unwrap(np.angle(M_hat))
    omega_real = -phase / h
    omega_imag = np.log(np.abs(M_hat)) / h
    return omega_real, omega_imag


# ── Polynomial fits for dispersion coefficients ─────────────────────

def fit_omega_poly(k_y: np.ndarray, omega_real: np.ndarray,
                   max_k_frac: float = 0.3) -> dict:
    """Fit omega(k) = omega_0 + a2*k^2 + a4*k^4 + a6*k^6 in the low-k regime.

    This directly fits omega (not omega^2) to avoid branch-cut issues.
    The k^4 term in omega corresponds to a k^4 term in omega^2 when
    omega ~ omega_0 + corrections.

    For the dispersion relation omega^2 = k^2 + c4*k^4:
      omega = sqrt(k^2 + c4*k^4) ~ k*(1 + c4*k^2/2 + ...)
    So c4_dispersion = 2*a4/a2 (approximately) when a2*k^2 dominates.

    We fit omega - omega(0) = a2*k^2 + a4*k^4 + a6*k^6
    """
    k_max = max_k_frac * k_y.max()
    mask = (k_y > 1e-10) & (k_y < k_max) & np.isfinite(omega_real)
    ky = k_y[mask]
    omega_r = omega_real[mask]

    if len(ky) < 6:
        return {"a2": np.nan, "a4": np.nan, "a6": np.nan, "r2": -1,
                "n_points": len(ky)}

    omega_0 = omega_real[0] if np.isfinite(omega_real[0]) else 0.0
    delta_omega = omega_r - omega_0

    # Fit delta_omega = a2*k^2 + a4*k^4 + a6*k^6
    X = np.column_stack([ky**2, ky**4, ky**6])
    try:
        coeffs, residuals, rank, sv = np.linalg.lstsq(X, delta_omega, rcond=None)
        a2, a4, a6 = coeffs

        ss_res = np.sum((delta_omega - X @ coeffs)**2)
        ss_tot = np.sum((delta_omega - np.mean(delta_omega))**2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else -1

        # Also fit omega^2 for comparison
        omega_sq = omega_r**2
        omega_sq_0 = omega_0**2
        delta_omega_sq = omega_sq - omega_sq_0

        X2 = np.column_stack([ky**2, ky**4, ky**6])
        coeffs2, _, _, _ = np.linalg.lstsq(X2, delta_omega_sq, rcond=None)
        c2, c4, c6 = coeffs2

        ss_res2 = np.sum((delta_omega_sq - X2 @ coeffs2)**2)
        ss_tot2 = np.sum((delta_omega_sq - np.mean(delta_omega_sq))**2)
        r2_sq = 1.0 - ss_res2 / ss_tot2 if ss_tot2 > 1e-30 else -1

        return {"a2": a2, "a4": a4, "a6": a6, "r2": r2,
                "c2": c2, "c4": c4, "c6": c6, "r2_sq": r2_sq,
                "n_points": len(ky), "omega_0": omega_0}
    except Exception:
        return {"a2": np.nan, "a4": np.nan, "a6": np.nan, "r2": -1,
                "c2": np.nan, "c4": np.nan, "c6": np.nan, "r2_sq": -1,
                "n_points": 0}


def fit_c4_scaling(h_values: list[float], c4_values: list[float]) -> dict:
    """Fit |c4| = A * h^alpha to extract the scaling exponent."""
    h_arr = np.array(h_values)
    c4_arr = np.abs(np.array(c4_values))

    # Filter valid entries
    mask = np.isfinite(c4_arr) & (c4_arr > 1e-30) & np.isfinite(h_arr)
    h_clean = h_arr[mask]
    c4_clean = c4_arr[mask]

    if len(h_clean) < 2:
        return {"alpha": np.nan, "A": np.nan, "r2": -1}

    log_h = np.log(h_clean)
    log_c4 = np.log(c4_clean)

    # Linear fit: log|c4| = log(A) + alpha * log(h)
    X = np.column_stack([np.ones_like(log_h), log_h])
    try:
        coeffs, residuals, rank, sv = np.linalg.lstsq(X, log_c4, rcond=None)
        log_A, alpha = coeffs
        A = np.exp(log_A)

        fitted = X @ coeffs
        ss_res = np.sum((log_c4 - fitted)**2)
        ss_tot = np.sum((log_c4 - np.mean(log_c4))**2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else -1

        return {"alpha": alpha, "A": A, "r2": r2}
    except Exception:
        return {"alpha": np.nan, "A": np.nan, "r2": -1}


def compute_planck_energy(c4: float, h: float) -> float:
    """Compute the energy where the k^4 correction becomes O(1).

    |c4| * k_Planck^4 ~ k_Planck^2  =>  k_Planck^2 ~ 1/|c4|
    In natural units where the lattice spacing h sets the scale:
    E_Planck_eff = h_bar * c * k_Planck ~ 1 / (h * sqrt(|c4|/h^2))

    If c4 ~ A * h^2, then k_Planck ~ 1/(h * sqrt(A)) and
    E_Planck_eff ~ 1/(h^2 * sqrt(A))  in lattice units.
    """
    if not np.isfinite(c4) or abs(c4) < 1e-30:
        return np.nan
    k_planck_sq = 1.0 / abs(c4)
    return math.sqrt(k_planck_sq)


# ── Main experiment ─────────────────────────────────────────────────

def run_experiment():
    t0 = time.time()

    print("=" * 78)
    print("MODIFIED DISPERSION RELATION FROM DISCRETE GRAPH PROPAGATOR")
    print("=" * 78)
    print(f"\nParameters: k_phase={K_PHASE}, p={P_ATTEN}")
    print(f"h values: {H_VALUES}")
    print(f"Transverse half-width: {N_TRANSVERSE} (sites: {2*N_TRANSVERSE+1})")
    print(f"k-points: {N_K_POINTS}")
    print(f"Kernels: {list(KERNELS.keys())}")

    architectures = {
        "cubic": transfer_kernel_row_cubic,
        "staggered": transfer_kernel_row_staggered,
        "wilson": transfer_kernel_row_wilson,
    }

    all_results = {}

    for arch_name, kernel_builder in architectures.items():
        all_results[arch_name] = {}

        for kern_name, kern_fn in KERNELS.items():
            all_results[arch_name][kern_name] = {}

            print(f"\n{'=' * 78}")
            print(f"ARCHITECTURE: {arch_name}   KERNEL: {kern_name}")
            print(f"{'=' * 78}")

            c4_list = []
            h_list_valid = []

            for h in H_VALUES:
                print(f"\n{'─' * 60}")
                print(f"  h = {h}")
                print(f"{'─' * 60}")

                n_half = min(N_TRANSVERSE, max(4, int(3.0 / h)))

                k_y, M_hat = kernel_builder(h, K_PHASE, P_ATTEN,
                                            kern_fn, n_half)

                omega_real, omega_imag = extract_dispersion(k_y, M_hat, h)

                # Show a few sample points
                print(f"\n  Sample dispersion (first 10 k-points with stride):")
                print(f"  {'k_y':>10}  {'omega_re':>14}  {'omega_im':>14}  "
                      f"{'|M_hat|':>12}  {'arg(M_hat)':>12}")
                stride = max(1, N_K_POINTS // 10)
                for i in range(0, min(N_K_POINTS, 10 * stride), stride):
                    print(f"  {k_y[i]:10.4f}  {omega_real[i]:14.6f}  "
                          f"{omega_imag[i]:14.6f}  "
                          f"{np.abs(M_hat[i]):12.6f}  "
                          f"{np.angle(M_hat[i]):12.6f}")

                # Fit dispersion coefficients
                fit = fit_omega_poly(k_y, omega_real)
                a2 = fit["a2"]
                a4 = fit["a4"]
                a6 = fit["a6"]
                c2 = fit.get("c2", np.nan)
                c4 = fit.get("c4", np.nan)
                c6 = fit.get("c6", np.nan)
                r2 = fit["r2"]

                print(f"\n  Polynomial fit (low-k, {fit['n_points']} pts):")
                print(f"    omega(k) - omega(0) = a2*k^2 + a4*k^4 + a6*k^6")
                print(f"    a2 = {a2:+.8e}")
                print(f"    a4 = {a4:+.8e}  <-- discreteness correction to omega")
                print(f"    a6 = {a6:+.8e}")
                print(f"    R^2(omega) = {r2:.6f}")
                print(f"    omega^2 fit: c2={c2:+.4e}  c4={c4:+.4e}  "
                      f"R^2={fit.get('r2_sq', -1):.4f}")

                if np.isfinite(c4) and abs(c4) > 1e-30:
                    k_planck = compute_planck_energy(c4, h)
                    print(f"    k_Planck (c4 becomes O(1)): {k_planck:.4f}  "
                          f"[k_max = pi/h = {np.pi/h:.4f}]")
                    c4_list.append(c4)
                    h_list_valid.append(h)
                else:
                    print(f"    c4 too small or invalid for Planck energy estimate")

                all_results[arch_name][kern_name][h] = {
                    "a2": a2, "a4": a4, "a6": a6,
                    "c2": c2, "c4": c4, "c6": c6, "r2": r2,
                    "omega_real": omega_real, "omega_imag": omega_imag,
                    "k_y": k_y,
                }

            # ── c4 scaling with h ────────────────────────────────────
            if len(c4_list) >= 2:
                scaling = fit_c4_scaling(h_list_valid, c4_list)
                print(f"\n  c4 SCALING with h:")
                print(f"    |c4| = {scaling['A']:.6e} * h^{scaling['alpha']:.4f}")
                print(f"    R^2 = {scaling['r2']:.4f}")
                if np.isfinite(scaling["alpha"]):
                    if abs(scaling["alpha"] - 2.0) < 0.5:
                        print(f"    => CONSISTENT with h^2 scaling "
                              f"(expected for standard lattice correction)")
                    else:
                        print(f"    => ANOMALOUS scaling exponent "
                              f"(expected ~2.0, got {scaling['alpha']:.2f})")

                all_results[arch_name][kern_name]["scaling"] = scaling
            else:
                print(f"\n  Insufficient valid c4 values for scaling fit.")
                all_results[arch_name][kern_name]["scaling"] = {
                    "alpha": np.nan, "A": np.nan, "r2": -1
                }

    # ── Summary table ──────────────────────────────────────────────
    print(f"\n\n{'=' * 78}")
    print("SUMMARY: c4 COEFFICIENTS ACROSS ARCHITECTURES AND KERNELS")
    print(f"{'=' * 78}")

    print(f"\n{'arch':>12}  {'kernel':>8}  ", end="")
    for h in H_VALUES:
        print(f"{'c4(h='+str(h)+')':>16}  ", end="")
    print(f"{'alpha':>8}  {'A':>12}  {'scaling_R2':>10}")

    for arch_name in architectures:
        for kern_name in KERNELS:
            res = all_results[arch_name][kern_name]
            sc = res.get("scaling", {})
            print(f"  {arch_name:>10}  {kern_name:>8}  ", end="")
            for h in H_VALUES:
                c4 = res.get(h, {}).get("c4", np.nan)
                if np.isfinite(c4):
                    print(f"{c4:+16.8e}  ", end="")
                else:
                    print(f"{'N/A':>16}  ", end="")
            alpha = sc.get("alpha", np.nan)
            A = sc.get("A", np.nan)
            r2 = sc.get("r2", -1)
            if np.isfinite(alpha):
                print(f"{alpha:8.3f}  {A:12.6e}  {r2:10.4f}")
            else:
                print(f"{'N/A':>8}  {'N/A':>12}  {'N/A':>10}")

    # ── Architecture comparison ────────────────────────────────────
    print(f"\n{'=' * 78}")
    print("ARCHITECTURE DEPENDENCE OF c4")
    print(f"{'=' * 78}")

    for kern_name in KERNELS:
        print(f"\n  Kernel: {kern_name}")
        for h in H_VALUES:
            c4_vals = {}
            for arch_name in architectures:
                c4 = all_results[arch_name][kern_name].get(h, {}).get("c4", np.nan)
                if np.isfinite(c4):
                    c4_vals[arch_name] = c4

            if len(c4_vals) >= 2:
                abs_vals = [abs(v) for v in c4_vals.values()]
                ratio = max(abs_vals) / min(abs_vals) if min(abs_vals) > 1e-30 else np.inf
                print(f"    h={h}: ", end="")
                for a, v in c4_vals.items():
                    print(f"{a}={v:+.4e}  ", end="")
                print(f"  max/min ratio = {ratio:.2f}")

    # ── Effective Planck energy and experimental comparison ─────────
    print(f"\n{'=' * 78}")
    print("EFFECTIVE PLANCK ENERGY AND FERMI LAT COMPARISON")
    print(f"{'=' * 78}")

    print(f"\nFermi LAT bound (n=2 LIV): E_QG > {FERMI_LAT_EQG_N2_GEV:.2e} GeV")
    print(f"Planck energy: E_Planck = {PLANCK_ENERGY_GEV:.2e} GeV")
    print(f"Ratio E_QG/E_Planck = {FERMI_LAT_EQG_N2_GEV/PLANCK_ENERGY_GEV:.4e}")

    print(f"\n  For the path-sum model, if the fundamental lattice spacing is")
    print(f"  h = l_Planck, then the k^4 correction has coefficient")
    print(f"  c4 ~ A * l_Planck^2  where A is the dimensionless prefactor.\n")

    for arch_name in architectures:
        for kern_name in KERNELS:
            sc = all_results[arch_name][kern_name].get("scaling", {})
            A = sc.get("A", np.nan)
            alpha = sc.get("alpha", np.nan)
            if np.isfinite(A) and np.isfinite(alpha):
                # If c4 = A * h^alpha, at h = l_Planck:
                # k_Planck_eff = 1/sqrt(|c4|) = 1/sqrt(A * l_Planck^alpha)
                # E_Planck_eff = k_Planck_eff * (hbar*c) = E_Planck / sqrt(A) * l_Planck^(1-alpha/2)
                # For alpha~2: E_Planck_eff = E_Planck / sqrt(A)
                if abs(alpha - 2.0) < 1.0:
                    E_eff = PLANCK_ENERGY_GEV / math.sqrt(A) if A > 0 else np.nan
                    print(f"  {arch_name:>10}/{kern_name:>6}: A = {A:.4e}, "
                          f"alpha = {alpha:.2f}")
                    if np.isfinite(E_eff):
                        print(f"    E_Planck_eff = E_Planck / sqrt(A) = {E_eff:.4e} GeV")
                        if E_eff > FERMI_LAT_EQG_N2_GEV:
                            print(f"    => CONSISTENT with Fermi LAT bound "
                                  f"(E_eff > E_QG)")
                        else:
                            print(f"    => TENSION with Fermi LAT bound "
                                  f"(E_eff < E_QG)")
                            print(f"    => Would require h < l_Planck * "
                                  f"(E_QG/E_eff)^(2/alpha) to satisfy bound")
                else:
                    print(f"  {arch_name:>10}/{kern_name:>6}: alpha = {alpha:.2f} "
                          f"(non-standard scaling, cannot directly compare)")

    # ── Photon speed prediction ────────────────────────────────────
    print(f"\n{'=' * 78}")
    print("PREDICTED ENERGY-DEPENDENT PHOTON SPEED")
    print(f"{'=' * 78}")

    print(f"\n  For a k^4 correction to the dispersion relation:")
    print(f"    omega^2 = k^2 + c4 * k^4")
    print(f"    v_group = d omega / dk = 1 + c4 * k^2 + O(k^4)")
    print(f"    |v - 1| = |c4| * (E/E_Planck_eff)^2")
    print(f"\n  At E = 10 GeV (typical Fermi LAT photon):")

    for arch_name in architectures:
        for kern_name in KERNELS:
            sc = all_results[arch_name][kern_name].get("scaling", {})
            A = sc.get("A", np.nan)
            alpha = sc.get("alpha", np.nan)
            if np.isfinite(A) and abs(alpha - 2.0) < 1.0 and A > 0:
                E_eff = PLANCK_ENERGY_GEV / math.sqrt(A)
                if np.isfinite(E_eff):
                    E_test = 10.0  # GeV
                    delta_v = (E_test / E_eff)**2
                    print(f"    {arch_name}/{kern_name}: |v-1| = "
                          f"{delta_v:.4e}  (E_eff = {E_eff:.4e} GeV)")

    # ── Hypothesis verdict ──────────────────────────────────────────
    print(f"\n{'=' * 78}")
    print("HYPOTHESIS VERDICT")
    print(f"{'=' * 78}")

    # Check 1: does c4 scale as h^2?
    scalings_valid = []
    for arch_name in architectures:
        for kern_name in KERNELS:
            sc = all_results[arch_name][kern_name].get("scaling", {})
            alpha = sc.get("alpha", np.nan)
            r2 = sc.get("r2", -1)
            if np.isfinite(alpha) and r2 > 0.8:
                scalings_valid.append((arch_name, kern_name, alpha, r2))

    h2_consistent = [s for s in scalings_valid if abs(s[2] - 2.0) < 0.5]

    # Check 2: architecture dependence bounded?
    arch_ratios = []
    for kern_name in KERNELS:
        for h in H_VALUES:
            c4_vals = []
            for arch_name in architectures:
                c4 = all_results[arch_name][kern_name].get(h, {}).get("c4", np.nan)
                if np.isfinite(c4) and abs(c4) > 1e-30:
                    c4_vals.append(abs(c4))
            if len(c4_vals) >= 2:
                arch_ratios.append(max(c4_vals) / min(c4_vals))

    arch_bounded = all(r < 10 for r in arch_ratios) if arch_ratios else False

    print(f"\n  1. c4 ~ h^alpha scaling:")
    if h2_consistent:
        for s in h2_consistent:
            print(f"     {s[0]}/{s[1]}: alpha = {s[2]:.3f} (R^2 = {s[3]:.4f})")
        print(f"     => {len(h2_consistent)}/{len(scalings_valid)} combinations "
              f"consistent with h^2")
    elif scalings_valid:
        for s in scalings_valid:
            print(f"     {s[0]}/{s[1]}: alpha = {s[2]:.3f} (R^2 = {s[3]:.4f})")
        print(f"     => NONE consistent with h^2 (all alpha deviate by >0.5)")
    else:
        print(f"     => No valid scaling fits (R^2 < 0.8 for all)")

    print(f"\n  2. Architecture dependence:")
    if arch_ratios:
        print(f"     max/min ratios across architectures: "
              f"{[f'{r:.2f}' for r in arch_ratios]}")
        if arch_bounded:
            print(f"     => BOUNDED (all ratios < 10)")
        else:
            print(f"     => LARGE architecture dependence (some ratios >= 10)")
    else:
        print(f"     => Insufficient data for comparison")

    if h2_consistent and arch_bounded:
        print(f"\n  VERDICT: SUPPORTED")
        print(f"    The discrete propagator produces a k^4 correction that")
        print(f"    scales as h^2 with bounded architecture dependence.")
        print(f"    This is a concrete, testable prediction for Lorentz")
        print(f"    invariance violation at the discreteness scale.")
    elif h2_consistent:
        print(f"\n  VERDICT: PARTIALLY SUPPORTED")
        print(f"    h^2 scaling confirmed but architecture dependence is large.")
        print(f"    The prediction is qualitative but the coefficient is")
        print(f"    architecture-dependent.")
    elif scalings_valid:
        print(f"\n  VERDICT: ANOMALOUS SCALING")
        print(f"    c4 scales with h but not as h^2.  The correction has a")
        print(f"    different character than standard lattice artifacts.")
    else:
        print(f"\n  VERDICT: INCONCLUSIVE")
        print(f"    Could not reliably extract c4 scaling behavior.")

    elapsed = time.time() - t0
    print(f"\n  Elapsed: {elapsed:.1f} s")
    print(f"\n{'=' * 78}")
    print("EXPERIMENT COMPLETE")
    print(f"{'=' * 78}")


if __name__ == "__main__":
    run_experiment()
