#!/usr/bin/env python3
"""
Analytic Continuum Limit from Transfer-Matrix Fourier Structure
===============================================================
Instead of going to finer h (expensive), derive the continuum limit
ANALYTICALLY from the transfer matrix structure.

Physics:
  The single-layer transfer matrix M has elements:
    M[y_out, y_in] = exp(i*k*L) * w(theta) * h / L^p
  where L = sqrt(h^2 + dy^2), dy = (y_out - y_in)*h, theta = atan2(|dy|, h).

  With PERIODIC boundary conditions, M is exactly circulant (Toeplitz + periodic).
  A circulant matrix is diagonalised by the DFT: its eigenvalues are the DFT
  of its first row.

  The eigenvalue at transverse momentum k_y is:
    M_tilde(k_y) = sum_n K(n*h) * exp(-i * k_y * n * h)
  where K(dy) = exp(i*k*sqrt(h^2+dy^2)) * w(atan2(|dy|,h)) * h / (h^2+dy^2)^(p/2)

  The effective energy (dispersion) is:
    E(k_y) = i * ln(M_tilde(k_y)) / h

Approach:
  Part 1: Analytic small-k_y expansion of K(dy) => predict parabolic vs cone
  Part 2: Numerical FFT of M's first row at several h values
  Part 3: Extract dispersion E(k_y) and fit to parabolic / Klein-Gordon
  Part 4: Extrapolate coefficients c_2, c_4 to h->0

Hypothesis:
  The analytic continuum limit is Klein-Gordon (E^2 ~ m^2 + c^2*k_y^2)
  for any forward-biased kernel.

Falsification:
  If the leading correction is always E ~ k_y^2 (parabolic), the model
  is fundamentally non-relativistic.
"""

import numpy as np
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ── Parameters ──────────────────────────────────────────────────────
K_PHASE      = 5.0         # phase wavenumber k
P_ATTEN      = 1.0         # 1/L^p attenuation (p=1 for 1+1D spatial)
HEIGHT_PHYS  = 20.0        # physical transverse extent [-H, +H]
H_VALUES     = [1.0, 0.5, 0.25, 0.125]

KERNELS = {
    "cos":   lambda theta: np.cos(theta),
    "cos2":  lambda theta: np.cos(theta)**2,
    "gauss": lambda theta: np.exp(-0.8 * theta**2),
}


# ═══════════════════════════════════════════════════════════════════
# PART 1 — ANALYTIC SMALL-k_y EXPANSION
# ═══════════════════════════════════════════════════════════════════

def analytic_expansion():
    """
    For small transverse displacement dy:
      L = h*sqrt(1 + (dy/h)^2) ~ h + dy^2/(2h)
      theta = atan2(|dy|, h) ~ |dy|/h
      w(theta) ~ w(0) + w''(0)*theta^2/2 = 1 + w''(0)*dy^2/(2h^2)

    So K(dy) ~ exp(i*k*h) * exp(i*k*dy^2/(2h)) * [1 + w''(0)*dy^2/(2h^2)] * h^(1-p)

    The Fourier transform of exp(i*a*x^2)*(1 + b*x^2) is:
      sqrt(pi/(−i*a)) * exp(i*k_y^2/(4a)) * [1 + b*(i/(2a) + k_y^2/(4a^2)*(-i))]

    With a = k/(2h), this gives M_tilde(k_y) with:
      phase ~ k*h - k_y^2*h/(2k) + ...

    So E(k_y) = -phase/h = -k + k_y^2/(2k) + ...  => PARABOLIC (Schrodinger)!
    """
    print("=" * 72)
    print("PART 1: ANALYTIC SMALL-k_y EXPANSION")
    print("=" * 72)

    k = K_PHASE

    print(f"\nFor forward propagation with phase wavenumber k = {k}:")
    print(f"  L(dy) = h*sqrt(1 + (dy/h)^2) ~ h + dy^2/(2h) + ...")
    print(f"  Phase: k*L ~ k*h + k*dy^2/(2h)")
    print(f"  Fourier transform of exp(i*k*dy^2/(2h)) gives:")
    print(f"    M_tilde(k_y) ~ C * exp(-i*k_y^2*h/(2k))")
    print(f"  Therefore: E(k_y) = i*ln(M_tilde)/h")
    print(f"    = i*[i*k*h - i*k_y^2*h/(2k) + ln|C|]/h")
    print(f"    ~ -k + k_y^2/(2k) + ...")
    print(f"\n  PREDICTION: Re(E) is parabolic in k_y with coefficient 1/(2k) = {1/(2*k):.4f}")
    print(f"  This is the FREE SCHRODINGER dispersion: E = k_y^2/(2m) with m=k")
    print(f"\n  For Klein-Gordon, we would need E^2 = m^2 + c^2*k_y^2")
    print(f"  => E ~ m + c^2*k_y^2/(2m), also parabolic at small k_y")
    print(f"  The DISTINCTION is in the c_4 coefficient (quartic term).")
    print(f"  Schrodinger: c_4 = 0 (exactly parabolic)")
    print(f"  Klein-Gordon: c_4 = -c^4*k_y^4/(8m^3) (negative quartic correction)")


# ═══════════════════════════════════════════════════════════════════
# PART 2 — NUMERICAL: BUILD CIRCULANT M, FFT, EXTRACT DISPERSION
# ═══════════════════════════════════════════════════════════════════

def build_circulant_row(h, k, p, kernel_fn, n_y):
    """Build the first row of the circulant transfer matrix (periodic BC).

    M[0, j] = kernel for displacement from y_j to y_0 with periodic wrap.
    """
    row = np.zeros(n_y, dtype=complex)
    half = n_y // 2

    for j in range(n_y):
        # Signed displacement in lattice units, periodic
        dy_lattice = j if j <= half else j - n_y
        phys_dy = dy_lattice * h
        L = np.sqrt(h**2 + phys_dy**2)
        theta = np.arctan2(abs(phys_dy), h)

        w = kernel_fn(theta)
        row[j] = np.exp(1j * k * L) * w * h / (L ** p)

    return row


def dispersion_from_fft(row, h, k):
    """FFT the circulant row to get eigenvalues, then extract dispersion E(k_y)."""
    n_y = len(row)
    # Eigenvalues of circulant matrix = DFT of first row
    lambdas = np.fft.fft(row)

    # Transverse momenta
    ky_indices = np.fft.fftfreq(n_y, d=h)  # cycles per unit length
    ky = 2 * np.pi * ky_indices              # radians per unit length

    # Effective energy: lambda = exp(-i*E*h) => E = i*ln(lambda)/h
    E = 1j * np.log(lambdas) / h

    # Sort by k_y
    sort_idx = np.argsort(ky)
    ky = ky[sort_idx]
    E = E[sort_idx]
    lambdas = lambdas[sort_idx]

    return ky, E, lambdas


def numerical_dispersion():
    """Compute dispersion E(k_y) numerically for all kernels and h values."""
    print("\n" + "=" * 72)
    print("PART 2: NUMERICAL DISPERSION FROM FFT OF CIRCULANT MATRIX")
    print("=" * 72)

    results = {}

    for kname, kfn in KERNELS.items():
        print(f"\n--- Kernel: {kname} ---")
        results[kname] = {}

        for h in H_VALUES:
            n_y = int(2 * HEIGHT_PHYS / h) + 1
            row = build_circulant_row(h, K_PHASE, P_ATTEN, kfn, n_y)
            ky, E, lambdas = dispersion_from_fft(row, h, K_PHASE)

            # Store
            results[kname][h] = (ky, E, lambdas)

            # Focus on small k_y region
            mask = np.abs(ky) < 3.0
            ky_small = ky[mask]
            E_small = E[mask]

            # Real part of E (shifted by E(0))
            mid = len(ky_small) // 2
            E0 = np.real(E_small[mid])
            dE = np.real(E_small) - E0

            # Imaginary part of E (decay rate)
            Im_E = np.imag(E_small)

            print(f"\n  h = {h}:  n_y = {n_y}, E(0) = {E0:.6f}, "
                  f"Im(E(0)) = {np.imag(E_small[mid]):.6f}")

            # Fit parabolic: dE = c2 * ky^2
            try:
                def parabolic(x, c2):
                    return c2 * x**2
                popt_p, _ = curve_fit(parabolic, ky_small, dE, p0=[0.1])
                c2 = popt_p[0]

                # Fit quartic: dE = c2*ky^2 + c4*ky^4
                def quartic(x, c2, c4):
                    return c2 * x**2 + c4 * x**4
                popt_q, _ = curve_fit(quartic, ky_small, dE, p0=[c2, 0.0])
                c2_q, c4_q = popt_q

                # Residuals
                res_p = np.sum((dE - parabolic(ky_small, c2))**2)
                res_q = np.sum((dE - quartic(ky_small, *popt_q))**2)

                print(f"    Parabolic fit: c2 = {c2:.6f}  (analytic prediction: {1/(2*K_PHASE):.6f})")
                print(f"    Quartic fit:   c2 = {c2_q:.6f}, c4 = {c4_q:.8f}")
                print(f"    Residuals: parab = {res_p:.2e}, quartic = {res_q:.2e}")
                print(f"    Quartic improvement: {res_p/max(res_q, 1e-30):.1f}x")

                results[kname][h] = (ky, E, lambdas, c2, c2_q, c4_q, E0)
            except Exception as e:
                print(f"    Fit failed: {e}")
                results[kname][h] = (ky, E, lambdas, None, None, None, E0)

    return results


# ═══════════════════════════════════════════════════════════════════
# PART 3 — KLEIN-GORDON vs SCHRODINGER TEST
# ═══════════════════════════════════════════════════════════════════

def kg_vs_schrodinger(results):
    """Test whether dispersion matches Klein-Gordon or Schrodinger.

    Schrodinger: E - E0 = k_y^2/(2m)           => c4 = 0
    Klein-Gordon: E^2 = E0^2 + c^2*k_y^2       => E ~ E0 + c^2*k_y^2/(2*E0)
                  with quartic: -c^4*k_y^4/(8*E0^3)

    Key test: fit E^2 vs k_y^2. If linear => Klein-Gordon. If curved => Schrodinger.
    """
    print("\n" + "=" * 72)
    print("PART 3: KLEIN-GORDON vs SCHRODINGER DISPERSION TEST")
    print("=" * 72)

    for kname in KERNELS:
        print(f"\n{'─'*60}")
        print(f"Kernel: {kname}")
        print(f"{'─'*60}")

        for h in H_VALUES:
            data = results[kname][h]
            if len(data) < 7 or data[3] is None:
                continue

            ky, E, lambdas, c2, c2_q, c4_q, E0 = data
            mask = np.abs(ky) < 3.0
            ky_s = ky[mask]
            E_real = np.real(E[mask])

            # Method 1: Fit E^2 = a + b*ky^2
            E2 = E_real**2
            try:
                def linear_E2(x, a, b):
                    return a + b * x**2
                popt, _ = curve_fit(linear_E2, ky_s, E2, p0=[E0**2, 1.0])
                a_fit, b_fit = popt
                res_lin = np.sum((E2 - linear_E2(ky_s, *popt))**2)

                # Fit E^2 = a + b*ky^2 + d*ky^4
                def quad_E2(x, a, b, d):
                    return a + b * x**2 + d * x**4
                popt2, _ = curve_fit(quad_E2, ky_s, E2, p0=[a_fit, b_fit, 0.0])
                a2, b2, d2 = popt2
                res_quad = np.sum((E2 - quad_E2(ky_s, *popt2))**2)

                # If d2 ~ 0 => E^2 is linear in ky^2 => Klein-Gordon
                # If d2 significant => not Klein-Gordon
                print(f"\n  h = {h}:")
                print(f"    E(0) = {E0:.6f}")
                print(f"    E^2 = {a_fit:.4f} + {b_fit:.4f}*ky^2  "
                      f"(residual: {res_lin:.2e})")
                print(f"    E^2 = {a2:.4f} + {b2:.4f}*ky^2 + {d2:.6f}*ky^4  "
                      f"(residual: {res_quad:.2e})")

                # Predicted Klein-Gordon parameters
                m_kg = np.sqrt(abs(a_fit))
                if b_fit > 0:
                    c_kg = np.sqrt(abs(b_fit))
                else:
                    c_kg = 0.0

                print(f"    Klein-Gordon: m = {m_kg:.4f}, c = {c_kg:.4f}")
                print(f"    Quartic/quadratic ratio: |d2*9|/|b2| = "
                      f"{abs(d2*9)/max(abs(b2), 1e-30):.4f}")

                # Schrodinger prediction: E = E0 + ky^2/(2k) => E^2 = E0^2 + E0*ky^2/k + ky^4/(4k^2)
                sch_b = E0 / K_PHASE        # predicted b from Schrodinger
                sch_d = 1.0 / (4 * K_PHASE**2)  # predicted d from Schrodinger
                print(f"    Schrodinger prediction: b = {sch_b:.4f}, d = {sch_d:.6f}")
                print(f"    Measured vs Schrodinger: b ratio = {b_fit/max(abs(sch_b), 1e-30):.4f}, "
                      f"d ratio = {d2/max(abs(sch_d), 1e-30):.4f}")

            except Exception as e:
                print(f"  h = {h}: E^2 fit failed: {e}")


# ═══════════════════════════════════════════════════════════════════
# PART 4 — CONTINUUM EXTRAPOLATION: c2(h) and c4(h) as h->0
# ═══════════════════════════════════════════════════════════════════

def continuum_extrapolation(results):
    """Track how c2 and c4 behave as h->0 for each kernel."""
    print("\n" + "=" * 72)
    print("PART 4: CONTINUUM LIMIT EXTRAPOLATION (h -> 0)")
    print("=" * 72)

    analytic_c2 = 1.0 / (2 * K_PHASE)
    print(f"\nAnalytic prediction for Schrodinger: c2 = 1/(2k) = {analytic_c2:.6f}")
    print(f"If c2 -> 1/(2k) as h->0 and c4 -> 0, model is Schrodinger.")
    print(f"If c2 -> c^2/(2*E0) and c4 -> -c^4/(8*E0^3), model is Klein-Gordon.")

    for kname in KERNELS:
        print(f"\n--- Kernel: {kname} ---")
        print(f"  {'h':>6s}  {'c2':>10s}  {'c2/predicted':>12s}  "
              f"{'c4':>12s}  {'E0':>10s}  {'|c4|*9/|c2|':>12s}")

        for h in H_VALUES:
            data = results[kname][h]
            if len(data) < 7 or data[3] is None:
                print(f"  {h:6.3f}  {'FAILED':>10s}")
                continue

            _, _, _, c2, c2_q, c4_q, E0 = data
            ratio = c2 / analytic_c2 if analytic_c2 != 0 else float('inf')
            q_ratio = abs(c4_q * 9) / abs(c2_q) if abs(c2_q) > 1e-30 else float('inf')

            print(f"  {h:6.3f}  {c2_q:10.6f}  {ratio:12.6f}  "
                  f"{c4_q:12.8f}  {E0:10.4f}  {q_ratio:12.6f}")

        # Richardson extrapolation of c2 to h=0
        c2_vals = []
        h_vals = []
        for h in H_VALUES:
            data = results[kname][h]
            if len(data) >= 7 and data[4] is not None:
                c2_vals.append(data[4])  # c2 from quartic fit
                h_vals.append(h)

        if len(c2_vals) >= 2:
            # Linear extrapolation: c2(h) = c2(0) + a*h^2
            h_arr = np.array(h_vals)
            c2_arr = np.array(c2_vals)
            try:
                def extrap(x, c0, a):
                    return c0 + a * x**2
                popt, _ = curve_fit(extrap, h_arr, c2_arr, p0=[c2_arr[-1], 0.0])
                print(f"  Richardson extrapolation: c2(h->0) = {popt[0]:.6f} "
                      f"(analytic: {analytic_c2:.6f}, ratio: {popt[0]/analytic_c2:.4f})")
            except Exception:
                print(f"  Richardson extrapolation failed")


# ═══════════════════════════════════════════════════════════════════
# PART 5 — DECAY RATE (IMAGINARY PART) ANALYSIS
# ═══════════════════════════════════════════════════════════════════

def decay_analysis(results):
    """Analyze the imaginary part of E(k_y) — modes that decay."""
    print("\n" + "=" * 72)
    print("PART 5: DECAY RATE Im(E) vs k_y")
    print("=" * 72)
    print("Modes with Im(E) < 0 are decaying. Physical modes have Im(E) ~ 0.")

    for kname in KERNELS:
        print(f"\n--- Kernel: {kname} ---")
        for h in [H_VALUES[0], H_VALUES[-1]]:
            data = results[kname].get(h)
            if data is None or len(data) < 3:
                continue

            ky, E, lambdas = data[0], data[1], data[2]
            mask = np.abs(ky) < 3.0
            ky_s = ky[mask]
            Im_E = np.imag(E[mask])
            abs_lam = np.abs(lambdas[mask])

            # Count modes with |lambda| > 0.99 (nearly non-decaying)
            near_unit = np.sum(abs_lam > 0.99)
            total = len(abs_lam)

            print(f"  h = {h}: {near_unit}/{total} modes with |lambda|>0.99 in |ky|<3")
            print(f"    Im(E) range: [{np.min(Im_E):.4f}, {np.max(Im_E):.4f}]")
            print(f"    |lambda| range: [{np.min(abs_lam):.6f}, {np.max(abs_lam):.6f}]")


# ═══════════════════════════════════════════════════════════════════
# PART 6 — OVERALL VERDICT
# ═══════════════════════════════════════════════════════════════════

def verdict(results):
    """Summarise: is the continuum limit Schrodinger, Klein-Gordon, or other?"""
    print("\n" + "=" * 72)
    print("PART 6: VERDICT — CONTINUUM LIMIT CLASSIFICATION")
    print("=" * 72)

    analytic_c2 = 1.0 / (2 * K_PHASE)

    for kname in KERNELS:
        print(f"\n{'─'*60}")
        print(f"Kernel: {kname}")

        # Gather finest-h data
        finest_h = H_VALUES[-1]
        data = results[kname].get(finest_h)
        if data is None or len(data) < 7 or data[3] is None:
            print(f"  No valid data at h={finest_h}")
            continue

        _, _, _, c2, c2_q, c4_q, E0 = data

        # Test 1: Is c2 close to 1/(2k)?
        c2_ratio = c2_q / analytic_c2
        c2_match = abs(c2_ratio - 1.0) < 0.1

        # Test 2: Is c4 negligible?
        if abs(c2_q) > 1e-30:
            c4_significance = abs(c4_q * 9) / abs(c2_q)  # at ky=3
        else:
            c4_significance = float('inf')
        c4_small = c4_significance < 0.1

        # Test 3: E^2 vs ky^2 linearity
        ky = data[0]
        E = data[1]
        mask = np.abs(ky) < 3.0
        ky_s = ky[mask]
        E_real = np.real(E[mask])
        E2 = E_real**2

        try:
            def lin(x, a, b):
                return a + b * x**2
            popt, _ = curve_fit(lin, ky_s, E2, p0=[E0**2, 1.0])
            E2_pred = lin(ky_s, *popt)
            ss_res = np.sum((E2 - E2_pred)**2)
            ss_tot = np.sum((E2 - np.mean(E2))**2)
            R2_E2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

            # Schrodinger predicts E^2 = E0^2 + E0/k * ky^2 + ky^4/(4k^2)
            # Klein-Gordon predicts E^2 = m^2 + c^2 * ky^2 (exactly linear)
            E2_sch = E0**2 + E0 / K_PHASE * ky_s**2 + ky_s**4 / (4 * K_PHASE**2)
            ss_sch = np.sum((E2 - E2_sch)**2)
            R2_sch = 1 - ss_sch / ss_tot if ss_tot > 0 else 0

        except Exception:
            R2_E2 = 0
            R2_sch = 0

        print(f"  At h = {finest_h}:")
        print(f"    c2 = {c2_q:.6f}, analytic = {analytic_c2:.6f}, "
              f"ratio = {c2_ratio:.4f} {'MATCH' if c2_match else 'MISMATCH'}")
        print(f"    c4 significance at ky=3: {c4_significance:.4f} "
              f"{'SMALL' if c4_small else 'SIGNIFICANT'}")
        print(f"    E^2 linear fit R^2: {R2_E2:.6f}")
        print(f"    Schrodinger E^2 prediction R^2: {R2_sch:.6f}")

        if R2_sch > 0.99:
            label = "SCHRODINGER (parabolic, non-relativistic)"
        elif R2_E2 > 0.999 and not c4_small:
            label = "KLEIN-GORDON (linear E^2, relativistic)"
        elif c2_match and c4_small:
            label = "SCHRODINGER (c2 matches, c4 negligible)"
        else:
            label = "AMBIGUOUS (needs finer h)"

        print(f"  => CLASSIFICATION: {label}")

    # Global summary
    print(f"\n{'='*72}")
    print("GLOBAL SUMMARY")
    print(f"{'='*72}")
    print(f"Analytic prediction: E(ky) ~ E0 + ky^2/(2k) = Schrodinger dispersion")
    print(f"  c2 = 1/(2k) = {analytic_c2:.6f}")
    print(f"  Effective mass: m_eff = k = {K_PHASE}")
    print(f"\nThe DAG propagator's continuum limit is a FREE PARTICLE")
    print(f"Schrodinger equation with mass m = k (the phase wavenumber).")
    print(f"\nFor Klein-Gordon, one would need the LATTICE structure to generate")
    print(f"a different leading term. The kernel w(theta) modifies the effective")
    print(f"mass and higher-order corrections but does NOT change the leading")
    print(f"Schrodinger structure.")
    print(f"\nHYPOTHESIS STATUS: Check results above for kernel-dependent verdicts.")


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Analytic Continuum Limit from Transfer-Matrix Fourier Structure")
    print("=" * 72)

    analytic_expansion()
    results = numerical_dispersion()
    kg_vs_schrodinger(results)
    continuum_extrapolation(results)
    decay_analysis(results)
    verdict(results)
