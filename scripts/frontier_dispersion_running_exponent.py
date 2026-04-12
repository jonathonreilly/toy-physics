#!/usr/bin/env python3
"""
Dispersion Running-Exponent Fingerprint
========================================

Extract the dispersion type (Schrodinger / linear / Klein-Gordon) from the
principal transfer-matrix branch on ordered 3D cubic lattices.

Instead of a single global R^2 polynomial fit, this script computes a
running exponent:

    alpha_eff(k) = d log|Omega(k) - Omega(0)| / d log k

evaluated in two windows:
    - alpha_lo : low-k window   (k < pi/4)
    - alpha_hi : high-k window  (pi/4 < k < pi/2, pre-aliasing)

Classification:
    - Schrodinger : alpha_lo ~ 2, alpha_hi ~ 2
    - Linear (relativistic) : alpha_lo ~ 1, alpha_hi ~ 1
    - Klein-Gordon : alpha_lo ~ 2, alpha_hi ~ 1, finite crossover k_*

Method:
    For each architecture (cubic, staggered, Wilson) at h = 0.5:
    1. Build the Fourier-space transfer function M_hat(k_y) for transverse
       wavenumber k_y.  For a translation-invariant kernel on a 1D
       transverse slice, M is Toeplitz and M_hat(k_y) is the eigenvalue
       of the k_y Fourier mode -- this IS the principal eigenvalue for
       each mode.
    2. Extract Omega(k) = -Im[log(M_hat(k))] / h.
    3. Compute alpha_eff(k) via log-log derivative of |Omega(k) - Omega(0)|.

Falsification:
    If neither window shows a clean integer exponent, or if architectures
    disagree on the classification, the propagator does not have a simple
    particle interpretation at this lattice spacing.
"""

from __future__ import annotations

import math
import time

import numpy as np

np.set_printoptions(precision=10, linewidth=120, suppress=True)


# -- Parameters ---------------------------------------------------------------
K_PHASE = 5.0           # longitudinal phase wavenumber
P_ATTEN = 1.0           # 1/L^p attenuation exponent
H = 0.5                 # lattice spacing (fixed for this study)
N_TRANSVERSE = 16       # transverse grid half-width
N_K_POINTS = 400        # number of k_y points for dispersion scan

KERNEL_FN = lambda theta: np.cos(theta)**2   # cos^2 angular kernel

# Window boundaries
K_LO_MAX = np.pi / 4.0
K_HI_MIN = np.pi / 4.0
K_HI_MAX = np.pi / 2.0


# -- Fourier-space transfer functions ----------------------------------------

def transfer_function_cubic(h: float, k: float, p: float,
                            n_half: int, n_k: int
                            ) -> tuple[np.ndarray, np.ndarray]:
    """Compute M_hat(k_y) = sum_dy M(dy) * exp(-i k_y dy h) for cubic lattice.

    M(dy) = exp(i k L) * w(theta) * h / L^p  where L = sqrt(h^2 + (dy*h)^2).

    Returns (k_y_array, M_hat_array).
    """
    k_y = np.linspace(0.01, np.pi / h, n_k, endpoint=False)
    M_hat = np.zeros(n_k, dtype=complex)

    for dy in range(-n_half, n_half + 1):
        phys_dy = dy * h
        L = math.sqrt(h**2 + phys_dy**2)
        theta = math.atan2(abs(phys_dy), h)
        w = KERNEL_FN(theta)
        amplitude = np.exp(1j * k * L) * w * h / (L ** p)
        M_hat += amplitude * np.exp(-1j * k_y * dy * h)

    return k_y, M_hat


def transfer_function_staggered(h: float, k: float, p: float,
                                n_half: int, n_k: int
                                ) -> tuple[np.ndarray, np.ndarray]:
    """Staggered lattice: (-1)^|dy| sign on each hop."""
    k_y = np.linspace(0.01, np.pi / h, n_k, endpoint=False)
    M_hat = np.zeros(n_k, dtype=complex)

    for dy in range(-n_half, n_half + 1):
        stagger_sign = (-1) ** abs(dy)
        phys_dy = dy * h
        L = math.sqrt(h**2 + phys_dy**2)
        theta = math.atan2(abs(phys_dy), h)
        w = KERNEL_FN(theta)
        amplitude = stagger_sign * np.exp(1j * k * L) * w * h / (L ** p)
        M_hat += amplitude * np.exp(-1j * k_y * dy * h)

    return k_y, M_hat


def transfer_function_wilson(h: float, k: float, p: float,
                             n_half: int, n_k: int,
                             r_wilson: float = 1.0
                             ) -> tuple[np.ndarray, np.ndarray]:
    """Wilson lattice: cubic + Wilson doubler-removal factor in k-space."""
    k_y, M_hat = transfer_function_cubic(h, k, p, n_half, n_k)
    wilson_factor = 1.0 - r_wilson * (1.0 - np.cos(k_y * h))
    M_hat *= wilson_factor
    return k_y, M_hat


# -- Dispersion extraction ----------------------------------------------------

def extract_dispersion(k_y: np.ndarray, M_hat: np.ndarray, h: float
                       ) -> np.ndarray:
    """Extract Omega(k_y) = -Im[log(M_hat(k_y))] / h.

    This is the frequency (energy) associated with the principal
    transfer-matrix branch.  Uses unwrapped phase for continuity.
    """
    phase = np.unwrap(np.angle(M_hat))
    Omega = -phase / h
    return Omega


# -- Running exponent ---------------------------------------------------------

def running_exponent(k: np.ndarray, Omega: np.ndarray
                     ) -> tuple[np.ndarray, np.ndarray]:
    """Compute alpha_eff(k) = d log|Omega(k) - Omega(0)| / d log k.

    Uses central finite differences on the log-log data.
    Returns (k_mid, alpha_mid) where k_mid are the midpoints.
    """
    Omega0 = Omega[0]
    dOmega = np.abs(Omega - Omega0)

    # Mask out points where dOmega is too small for stable log
    valid = dOmega > 1e-12
    if np.sum(valid) < 4:
        return np.array([]), np.array([])

    log_k = np.log(k[valid])
    log_dO = np.log(dOmega[valid])

    # Central differences
    alpha = np.diff(log_dO) / np.diff(log_k)
    k_mid = np.exp(0.5 * (log_k[:-1] + log_k[1:]))

    return k_mid, alpha


def fit_window(k_mid: np.ndarray, alpha: np.ndarray,
               k_lo: float, k_hi: float) -> dict:
    """Fit a constant alpha in a k-window.  Returns mean, std, n_pts."""
    mask = (k_mid >= k_lo) & (k_mid <= k_hi)
    if np.sum(mask) < 2:
        return {"alpha": np.nan, "std": np.nan, "n_pts": 0}
    a = alpha[mask]
    return {"alpha": float(np.mean(a)), "std": float(np.std(a)),
            "n_pts": int(np.sum(mask))}


def find_crossover(k_mid: np.ndarray, alpha: np.ndarray,
                   alpha_lo_val: float, alpha_hi_val: float) -> float:
    """Find k_* where alpha transitions from alpha_lo toward alpha_hi.
    Returns NaN if no clear crossover."""
    if len(k_mid) < 5:
        return np.nan
    if abs(alpha_lo_val - alpha_hi_val) < 0.3:
        return np.nan  # No real transition

    mid_alpha = 0.5 * (alpha_lo_val + alpha_hi_val)

    for i in range(len(alpha) - 1):
        if ((alpha[i] - mid_alpha) * (alpha[i + 1] - mid_alpha)) < 0:
            frac = (mid_alpha - alpha[i]) / (alpha[i + 1] - alpha[i])
            k_star = k_mid[i] + frac * (k_mid[i + 1] - k_mid[i])
            return float(k_star)

    return np.nan


# -- Classification -----------------------------------------------------------

def classify(alpha_lo: float, alpha_hi: float, k_star: float,
             tol: float = 0.4) -> str:
    """Classify the dispersion type from running exponents."""
    if np.isnan(alpha_lo) or np.isnan(alpha_hi):
        return "inconclusive"

    lo_is_2 = abs(alpha_lo - 2.0) < tol
    lo_is_1 = abs(alpha_lo - 1.0) < tol
    hi_is_2 = abs(alpha_hi - 2.0) < tol
    hi_is_1 = abs(alpha_hi - 1.0) < tol

    if lo_is_2 and hi_is_2:
        return "Schrodinger (alpha ~ 2 everywhere)"
    if lo_is_1 and hi_is_1:
        return "linear / relativistic (alpha ~ 1 everywhere)"
    if lo_is_2 and hi_is_1 and np.isfinite(k_star):
        return f"Klein-Gordon (alpha: 2 -> 1, k_* = {k_star:.4f})"
    if lo_is_1 and hi_is_2:
        return "anomalous (alpha: 1 -> 2)"

    return (f"non-standard (alpha_lo={alpha_lo:.2f}, "
            f"alpha_hi={alpha_hi:.2f})")


# -- Main experiment ----------------------------------------------------------

def run_experiment():
    t0 = time.time()

    print("=" * 78)
    print("DISPERSION RUNNING-EXPONENT FINGERPRINT")
    print("=" * 78)
    print(f"\nParameters: k_phase={K_PHASE}, p={P_ATTEN}, h={H}")
    print(f"Transverse half-width: {N_TRANSVERSE}")
    print(f"k-points: {N_K_POINTS}")
    print(f"Low-k window:  k < {K_LO_MAX:.4f}")
    print(f"High-k window: {K_HI_MIN:.4f} < k < {K_HI_MAX:.4f}")

    architectures = {
        "cubic": transfer_function_cubic,
        "staggered": transfer_function_staggered,
        "wilson": transfer_function_wilson,
    }

    n_half = min(N_TRANSVERSE, max(4, int(3.0 / H)))
    print(f"Effective n_half: {n_half}  (transverse sites: {2*n_half+1})")

    results = {}

    for arch_name, tf_fn in architectures.items():
        print(f"\n{'=' * 78}")
        print(f"ARCHITECTURE: {arch_name}")
        print(f"{'=' * 78}")

        k_y, M_hat = tf_fn(H, K_PHASE, P_ATTEN, n_half, N_K_POINTS)
        Omega = extract_dispersion(k_y, M_hat, H)

        # Show raw dispersion
        print(f"\n  Raw dispersion Omega(k_y) -- samples:")
        print(f"  {'k_y':>10}  {'Omega':>14}  {'|M_hat|':>12}  "
              f"{'arg(M_hat)':>12}")
        stride = max(1, N_K_POINTS // 20)
        for i in range(0, N_K_POINTS, stride):
            print(f"  {k_y[i]:10.4f}  {Omega[i]:14.6f}  "
                  f"{np.abs(M_hat[i]):12.6f}  "
                  f"{np.angle(M_hat[i]):12.6f}")

        # Omega range diagnostic
        print(f"\n  Omega range: [{Omega.min():.6f}, {Omega.max():.6f}]")
        print(f"  Omega(0): {Omega[0]:.6f}")
        print(f"  |Omega - Omega(0)| max: {np.max(np.abs(Omega - Omega[0])):.6e}")

        # Running exponent
        k_mid, alpha = running_exponent(k_y, Omega)

        if len(k_mid) < 5:
            print(f"\n  WARNING: too few valid points for running exponent "
                  f"({len(k_mid)} pts)")
            results[arch_name] = {
                "alpha_lo": np.nan, "alpha_hi": np.nan,
                "k_star": np.nan, "classification": "inconclusive"
            }
            continue

        # Show running exponent samples
        print(f"\n  Running exponent alpha_eff(k) -- samples:")
        print(f"  {'k':>10}  {'alpha_eff':>12}")
        stride = max(1, len(k_mid) // 20)
        for i in range(0, len(k_mid), stride):
            print(f"  {k_mid[i]:10.4f}  {alpha[i]:12.4f}")

        # Fit windows
        lo_fit = fit_window(k_mid, alpha, 0.01, K_LO_MAX)
        hi_fit = fit_window(k_mid, alpha, K_HI_MIN, K_HI_MAX)

        alpha_lo = lo_fit["alpha"]
        alpha_hi = hi_fit["alpha"]

        print(f"\n  Window fits:")
        print(f"    alpha_lo = {alpha_lo:.4f} +/- {lo_fit['std']:.4f}  "
              f"({lo_fit['n_pts']} pts, k < {K_LO_MAX:.4f})")
        print(f"    alpha_hi = {alpha_hi:.4f} +/- {hi_fit['std']:.4f}  "
              f"({hi_fit['n_pts']} pts, "
              f"{K_HI_MIN:.4f} < k < {K_HI_MAX:.4f})")

        # Crossover
        k_star = find_crossover(k_mid, alpha, alpha_lo, alpha_hi)
        if np.isfinite(k_star):
            print(f"    k_* (crossover) = {k_star:.4f}")
        else:
            print(f"    k_* (crossover) = not detected")

        # Classification
        label = classify(alpha_lo, alpha_hi, k_star)
        print(f"\n  CLASSIFICATION: {label}")

        results[arch_name] = {
            "alpha_lo": alpha_lo, "alpha_lo_std": lo_fit["std"],
            "alpha_hi": alpha_hi, "alpha_hi_std": hi_fit["std"],
            "k_star": k_star, "classification": label,
            "n_pts_lo": lo_fit["n_pts"], "n_pts_hi": hi_fit["n_pts"],
        }

    # -- Summary table --------------------------------------------------------
    print(f"\n\n{'=' * 78}")
    print("SUMMARY: RUNNING-EXPONENT FINGERPRINT")
    print(f"{'=' * 78}")

    print(f"\n{'arch':>12}  {'alpha_lo':>10}  {'alpha_hi':>10}  "
          f"{'k_*':>8}  {'classification'}")
    print(f"{'-'*12}  {'-'*10}  {'-'*10}  {'-'*8}  {'-'*30}")

    for arch_name in architectures:
        r = results[arch_name]
        al = r["alpha_lo"]
        ah = r["alpha_hi"]
        ks = r["k_star"]
        cl = r["classification"]
        al_s = f"{al:.4f}" if np.isfinite(al) else "N/A"
        ah_s = f"{ah:.4f}" if np.isfinite(ah) else "N/A"
        ks_s = f"{ks:.4f}" if np.isfinite(ks) else "none"
        print(f"  {arch_name:>10}  {al_s:>10}  {ah_s:>10}  "
              f"{ks_s:>8}  {cl}")

    # -- Architecture agreement -----------------------------------------------
    print(f"\n{'=' * 78}")
    print("ARCHITECTURE AGREEMENT")
    print(f"{'=' * 78}")

    classifications = [results[a]["classification"] for a in architectures
                       if results[a]["classification"] != "inconclusive"]

    if len(set(classifications)) == 1 and len(classifications) > 0:
        print(f"\n  All architectures agree: {classifications[0]}")
        print(f"  => Architecture-independent particle type identification")
    elif len(classifications) > 0:
        print(f"\n  Architectures DISAGREE on classification:")
        for arch_name in architectures:
            r = results[arch_name]
            print(f"    {arch_name}: {r['classification']}")
        print(f"  => Architecture-dependent dispersion -- no universal "
              f"particle type")
    else:
        print(f"\n  All classifications inconclusive")

    # -- Hypothesis verdict ---------------------------------------------------
    print(f"\n{'=' * 78}")
    print("HYPOTHESIS VERDICT")
    print(f"{'=' * 78}")

    alpha_los = [results[a]["alpha_lo"] for a in architectures
                 if np.isfinite(results[a]["alpha_lo"])]
    alpha_his = [results[a]["alpha_hi"] for a in architectures
                 if np.isfinite(results[a]["alpha_hi"])]

    if alpha_los:
        mean_lo = np.mean(alpha_los)
        mean_hi = np.mean(alpha_his) if alpha_his else np.nan
        print(f"\n  Mean alpha_lo across architectures: {mean_lo:.4f}")
        if alpha_his:
            print(f"  Mean alpha_hi across architectures: {mean_hi:.4f}")

        if abs(mean_lo - 2.0) < 0.4:
            print(f"  Low-k regime: compatible with quadratic dispersion "
                  f"(Schrodinger-type)")
        elif abs(mean_lo - 1.0) < 0.4:
            print(f"  Low-k regime: compatible with linear dispersion "
                  f"(relativistic)")
        else:
            print(f"  Low-k regime: non-standard exponent")

        if alpha_his and abs(mean_hi - 1.0) < 0.4 and abs(mean_lo - 2.0) < 0.4:
            print(f"  => Klein-Gordon signature: quadratic at low k, "
                  f"linear at high k")
        elif alpha_his and abs(mean_hi - mean_lo) < 0.3:
            print(f"  => Single power law across both windows")
        elif alpha_his:
            print(f"  => Running exponent changes across windows")
    else:
        print(f"\n  No valid running exponents extracted")

    print(f"\n  NOTE: This is a bounded proxy study at h={H}. The running")
    print(f"  exponent replaces the earlier global-R^2 polynomial fit and")
    print(f"  provides a cleaner discriminator for the particle type.")
    print(f"  The classification is specific to (h={H}, k_phase={K_PHASE},")
    print(f"  p={P_ATTEN}, cos^2 kernel) and does not generalize without")
    print(f"  a continuum-limit study.")

    elapsed = time.time() - t0
    print(f"\n  Elapsed: {elapsed:.1f} s")
    print(f"\n{'=' * 78}")
    print("EXPERIMENT COMPLETE")
    print(f"{'=' * 78}")


if __name__ == "__main__":
    run_experiment()
