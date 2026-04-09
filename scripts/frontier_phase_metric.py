#!/usr/bin/env python3
"""Phase-sensitive metric tensor: can the propagator's phase produce Lorentzian signature?

BACKGROUND:
  The amplitude-weighted metric (frontier_emergent_metric.py) is always
  Euclidean because edge weights w(theta)/L^p are non-negative, making
  the outer-product sum positive-semidefinite by construction.

  The Lorentzian/causal structure must live in the PHASE exp(i*k*S).
  This script computes metric tensors using phase-sensitive observables
  that CAN produce negative eigenvalues.

THREE APPROACHES:

  1. Phase-weighted second-moment tensor:
     g_ij = sum_edges Re(exp(i*k*S)) * w(theta)/L^p * dx_i*dx_j / L^2
     Since Re(exp(i*k*S)) can be NEGATIVE, this tensor can have negative
     eigenvalues → potential Lorentzian signature.

  2. Green's function pole structure:
     Build the full propagator matrix G(y_out, y_in) over multiple layers.
     Fourier transform to momentum space G(k_y).
     The pole structure determines the effective dispersion and metric.

  3. Retarded vs advanced propagator:
     Compare forward-propagating (x increasing) and backward-propagating
     (x decreasing) Green's functions. In a Lorentzian theory these differ
     (retarded vs advanced). In Euclidean theory they're the same.

HYPOTHESIS:
  The phase-weighted metric tensor has Lorentzian signature (-,+,+) in
  2+1D: one negative eigenvalue (causal direction) and two positive
  (spatial directions).

FALSIFICATION:
  If all eigenvalues are positive (or all negative) for all tested k
  values and kernels, the phase does not produce Lorentzian structure
  at the metric tensor level.
"""

from __future__ import annotations
import math
import numpy as np


def compute_phase_metric_2plus1d(h, max_d_phys, k, weight_fn, p=2):
    """Compute phase-weighted second-moment tensor in 2+1D.

    g_ij = sum_offsets Re(exp(i*k*S)) * w(theta) * h^2 / L^p * (dx_i dx_j) / L^2

    where S = L (free-space valley-linear action).
    """
    max_d = max(1, round(max_d_phys / h))
    metric = np.zeros((3, 3))  # (x_causal, y, z)
    norm = 0.0

    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dx_vec = np.array([h, dy * h, dz * h])
            L = np.linalg.norm(dx_vec)
            theta = math.atan2(math.sqrt((dy*h)**2 + (dz*h)**2), h)
            w = weight_fn(theta)

            # Valley-linear free-space action: S = L
            S = L
            phase_factor = math.cos(k * S)  # Re(exp(i*k*S))

            measure = h ** 2  # 2 spatial dims
            contribution = phase_factor * w * measure / (L ** p)
            metric += contribution * np.outer(dx_vec, dx_vec) / (L ** 2)
            norm += abs(contribution)

    if norm > 1e-30:
        metric /= norm

    return metric


def compute_phase_metric_3plus1d(h, max_d_phys, k, weight_fn, p=3):
    """Compute phase-weighted second-moment tensor in 3+1D."""
    max_d = max(1, round(max_d_phys / h))
    metric = np.zeros((4, 4))  # (x_causal, y, z, w)
    norm = 0.0

    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            for dw in range(-max_d, max_d + 1):
                dx_vec = np.array([h, dy*h, dz*h, dw*h])
                L = np.linalg.norm(dx_vec)
                r_trans = math.sqrt((dy*h)**2 + (dz*h)**2 + (dw*h)**2)
                theta = math.atan2(r_trans, h)
                w = weight_fn(theta)

                S = L
                phase_factor = math.cos(k * S)

                measure = h ** 3
                contribution = phase_factor * w * measure / (L ** p)
                metric += contribution * np.outer(dx_vec, dx_vec) / (L ** 2)
                norm += abs(contribution)

    if norm > 1e-30:
        metric /= norm

    return metric


def classify_signature(eigenvalues, tol=1e-10):
    """Classify metric signature from eigenvalues."""
    n_pos = sum(1 for e in eigenvalues if e > tol)
    n_neg = sum(1 for e in eigenvalues if e < -tol)
    n_zero = sum(1 for e in eigenvalues if abs(e) <= tol)

    if n_neg == 0:
        return f"Euclidean ({n_pos}+)"
    elif n_neg == 1 and n_pos >= 1:
        return f"Lorentzian (-,{'+' * n_pos})"
    elif n_neg == n_pos:
        return f"Split ({n_neg}-,{n_pos}+)"
    else:
        return f"Mixed ({n_neg}-,{n_pos}+,{n_zero}o)"


def analyze_metric(metric, label):
    """Print metric tensor analysis."""
    eigenvalues = np.sort(np.linalg.eigvalsh(metric))
    sig = classify_signature(eigenvalues)

    print(f"\n  {label}:")
    print(f"    Metric tensor:")
    n = metric.shape[0]
    for i in range(n):
        row = "      [" + ", ".join(f"{metric[i,j]:+.6f}" for j in range(n)) + "]"
        print(row)
    print(f"    Eigenvalues: {eigenvalues}")
    print(f"    Signature: {sig}")

    # Ratio of causal to spatial eigenvalues
    if n >= 2:
        ratio = eigenvalues[-1] / eigenvalues[0] if abs(eigenvalues[0]) > 1e-15 else float('inf')
        print(f"    Max/min eigenvalue ratio: {ratio:.4f}")

    return eigenvalues, sig


def greens_function_pole_analysis(h, height, width, k, weight_fn, p=1):
    """Build propagator G over multiple layers, Fourier transform, find poles.

    The propagator G(y_out, y_in; n_layers) = M^n_layers.
    In momentum space: G(k_y; n) = sum_y G(y,0;n) exp(-i k_y y).
    The dispersion relation E(k_y) comes from the eigenvalues of M:
      lambda(k_y) = exp(-i E(k_y) h)
    """
    max_d = max(1, round(2 / h))
    n_y = 2 * height + 1

    # Build single-layer transfer matrix M
    M = np.zeros((n_y, n_y), dtype=complex)
    for y_out in range(n_y):
        for y_in in range(n_y):
            dy = (y_out - height) - (y_in - height)
            if abs(dy) > max_d:
                continue
            dx_vec = np.array([h, dy * h])
            L = np.linalg.norm(dx_vec)
            theta = math.atan2(abs(dy * h), h)
            w = weight_fn(theta)
            S = L  # free-space valley-linear
            amplitude = np.exp(1j * k * S) * w * h / (L ** p)
            M[y_out, y_in] = amplitude

    # Eigendecomposition of M
    eigenvalues_M, eigenvectors_M = np.linalg.eig(M)

    # Sort by magnitude (dominant modes first)
    idx = np.argsort(-np.abs(eigenvalues_M))
    eigenvalues_M = eigenvalues_M[idx]
    eigenvectors_M = eigenvectors_M[:, idx]

    # Extract effective energies: E_n = i * ln(lambda_n) / h
    E_n = np.zeros(len(eigenvalues_M), dtype=complex)
    for i, lam in enumerate(eigenvalues_M):
        if abs(lam) > 1e-30:
            E_n[i] = 1j * np.log(lam) / h
        else:
            E_n[i] = complex('nan')

    # For each eigenmode, compute dominant transverse wavenumber
    k_y_dominant = np.zeros(len(eigenvalues_M))
    for i in range(len(eigenvalues_M)):
        v = eigenvectors_M[:, i]
        fft_v = np.fft.fft(v)
        power = np.abs(fft_v) ** 2
        # Map FFT indices to physical wavenumbers
        freqs = np.fft.fftfreq(n_y, d=h)
        k_y_dominant[i] = freqs[np.argmax(power)]

    return eigenvalues_M, E_n, k_y_dominant, M


def retarded_vs_advanced_test(h, height, k, weight_fn, p=1):
    """Compare forward and backward propagators.

    In Lorentzian theory: G_retarded != G_advanced (causal asymmetry).
    In Euclidean theory: G_retarded = G_advanced (time-symmetric).

    Build M_forward (x → x+1) and M_backward (x+1 → x) and compare.
    """
    max_d = max(1, round(2 / h))
    n_y = 2 * height + 1

    # Forward transfer matrix (standard)
    M_fwd = np.zeros((n_y, n_y), dtype=complex)
    for y_out in range(n_y):
        for y_in in range(n_y):
            dy = (y_out - height) - (y_in - height)
            if abs(dy) > max_d:
                continue
            L = math.sqrt(h**2 + (dy*h)**2)
            theta = math.atan2(abs(dy*h), h)
            w = weight_fn(theta)
            S = L
            M_fwd[y_out, y_in] = np.exp(1j * k * S) * w * h / (L ** p)

    # Backward transfer matrix (reverse the causal direction)
    # In the backward direction, dx = -h (going from x+1 to x)
    # The angle theta is now measured from -x direction
    M_bwd = np.zeros((n_y, n_y), dtype=complex)
    for y_out in range(n_y):
        for y_in in range(n_y):
            dy = (y_out - height) - (y_in - height)
            if abs(dy) > max_d:
                continue
            L = math.sqrt(h**2 + (dy*h)**2)
            # Backward: theta from -x direction = pi - theta_forward
            theta_fwd = math.atan2(abs(dy*h), h)
            theta_bwd = math.pi - theta_fwd
            w_bwd = weight_fn(theta_bwd)
            S = L
            M_bwd[y_out, y_in] = np.exp(1j * k * S) * w_bwd * h / (L ** p)

    # Compare: Frobenius norm of difference
    diff = M_fwd - M_bwd
    fwd_norm = np.linalg.norm(M_fwd, 'fro')
    diff_norm = np.linalg.norm(diff, 'fro')
    asymmetry = diff_norm / fwd_norm if fwd_norm > 1e-30 else 0.0

    # Also compare eigenvalue spectra
    eig_fwd = np.sort(np.abs(np.linalg.eigvals(M_fwd)))[::-1]
    eig_bwd = np.sort(np.abs(np.linalg.eigvals(M_bwd)))[::-1]
    eig_diff = np.linalg.norm(eig_fwd - eig_bwd) / np.linalg.norm(eig_fwd)

    return asymmetry, eig_diff, M_fwd, M_bwd


def main():
    print("=" * 72)
    print("PHASE-SENSITIVE METRIC TENSOR")
    print("=" * 72)
    print()
    print("Can the propagator's PHASE produce Lorentzian signature?")
    print()
    print("The amplitude-weighted metric is always Euclidean (non-negative")
    print("weights → positive-semidefinite). This script tests whether")
    print("Re(exp(i*k*S)) weighting — which CAN be negative — produces")
    print("a metric with Lorentzian signature.")
    print()

    kernels = [
        ("uniform",      lambda t: 1.0),
        ("cos(theta)",   lambda t: math.cos(t)),
        ("cos^2(theta)", lambda t: math.cos(t) ** 2),
        ("exp(-0.8t^2)", lambda t: math.exp(-0.8 * t * t)),
    ]

    # ==================================================================
    # APPROACH 1: Phase-weighted second-moment tensor
    # ==================================================================
    print("=" * 72)
    print("APPROACH 1: Phase-weighted second-moment tensor")
    print("  g_ij = sum Re(exp(ikS)) * w/L^p * dx_i dx_j / L^2")
    print("=" * 72)

    # Sweep k values — the phase factor Re(exp(ikL)) oscillates with k,
    # so the signature may depend on k
    k_values = [0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 10.0]

    print("\n--- 2+1D (h=0.5, max_d=3) ---")
    for name, wfn in kernels:
        print(f"\n  Kernel: {name}")
        print(f"  {'k':>6s} | {'eigenvalues':>40s} | {'signature':>20s}")
        print(f"  {'-'*72}")
        for kk in k_values:
            g = compute_phase_metric_2plus1d(0.5, 3, kk, wfn, p=2)
            evals = np.sort(np.linalg.eigvalsh(g))
            sig = classify_signature(evals)
            ev_str = ", ".join(f"{e:+.6f}" for e in evals)
            print(f"  {kk:>6.1f} | {ev_str:>40s} | {sig:>20s}")

    print("\n\n--- 3+1D (h=1.0, max_d=2) ---")
    for name, wfn in [("cos^2(theta)", lambda t: math.cos(t)**2),
                       ("exp(-0.8t^2)", lambda t: math.exp(-0.8*t*t))]:
        print(f"\n  Kernel: {name}")
        print(f"  {'k':>6s} | {'eigenvalues':>55s} | {'signature':>20s}")
        print(f"  {'-'*90}")
        for kk in k_values:
            g = compute_phase_metric_3plus1d(1.0, 2, kk, wfn, p=3)
            evals = np.sort(np.linalg.eigvalsh(g))
            sig = classify_signature(evals)
            ev_str = ", ".join(f"{e:+.6f}" for e in evals)
            print(f"  {kk:>6.1f} | {ev_str:>55s} | {sig:>20s}")

    # ==================================================================
    # APPROACH 2: Green's function dispersion relation
    # ==================================================================
    print("\n\n" + "=" * 72)
    print("APPROACH 2: Green's function dispersion E(k_y)")
    print("  Extract from transfer matrix eigenvalues")
    print("=" * 72)

    for name, wfn in [("cos^2(theta)", lambda t: math.cos(t)**2),
                       ("exp(-0.8t^2)", lambda t: math.exp(-0.8*t*t))]:
        print(f"\n  Kernel: {name}, h=0.5, height=10, k=5.0")
        evals_M, E_n, k_y, M = greens_function_pole_analysis(0.5, 10, 20, 5.0, wfn, p=1)

        # Print top modes
        print(f"  {'mode':>4} | {'|lambda|':>10} | {'arg(lam)':>10} | {'Re(E)':>10} | {'Im(E)':>10} | {'k_y':>8}")
        print(f"  {'-'*60}")
        for i in range(min(10, len(evals_M))):
            lam = evals_M[i]
            E = E_n[i]
            if not np.isnan(E):
                print(f"  {i:>4} | {abs(lam):>10.4f} | {np.angle(lam):>+10.4f} | "
                      f"{E.real:>10.4f} | {E.imag:>10.4f} | {k_y[i]:>8.4f}")

        # Check dispersion: is Re(E) vs k_y^2 hyperbolic or parabolic?
        valid = [(k_y[i], E_n[i].real) for i in range(len(E_n))
                 if not np.isnan(E_n[i]) and abs(k_y[i]) > 0.01]
        if len(valid) >= 3:
            ks = np.array([v[0] for v in valid])
            Es = np.array([v[1] for v in valid])

            # Fit E = a + b*k^2 (parabolic/Schrödinger)
            X_para = np.column_stack([np.ones(len(ks)), ks**2])
            coeff_para, res_para, _, _ = np.linalg.lstsq(X_para, Es, rcond=None)
            pred_para = X_para @ coeff_para
            ss_res_p = np.sum((Es - pred_para)**2)
            ss_tot = np.sum((Es - np.mean(Es))**2)
            r2_para = 1 - ss_res_p / ss_tot if ss_tot > 0 else 0

            # Fit E^2 = a + b*k^2 (relativistic: E^2 = m^2 + k^2)
            Es2 = Es ** 2
            X_rel = np.column_stack([np.ones(len(ks)), ks**2])
            coeff_rel, _, _, _ = np.linalg.lstsq(X_rel, Es2, rcond=None)
            pred_rel = X_rel @ coeff_rel
            ss_res_r = np.sum((Es2 - pred_rel)**2)
            ss_tot_r = np.sum((Es2 - np.mean(Es2))**2)
            r2_rel = 1 - ss_res_r / ss_tot_r if ss_tot_r > 0 else 0

            print(f"\n  Dispersion fits:")
            print(f"    E = {coeff_para[0]:.4f} + {coeff_para[1]:.4f}*k^2  (Schrodinger)  R^2={r2_para:.4f}")
            print(f"    E^2 = {coeff_rel[0]:.4f} + {coeff_rel[1]:.4f}*k^2  (relativistic)  R^2={r2_rel:.4f}")

            if r2_rel > r2_para and r2_rel > 0.8:
                m_sq = coeff_rel[0]
                c_sq = coeff_rel[1]
                print(f"    ==> Relativistic (Klein-Gordon) fit is better")
                print(f"    ==> Effective mass^2 = {m_sq:.4f}, c^2 = {c_sq:.4f}")
                if c_sq > 0:
                    print(f"    ==> This is LORENTZIAN: E^2 = m^2 + c^2*k^2")
                else:
                    print(f"    ==> c^2 < 0: not standard Lorentzian")
            elif r2_para > 0.8:
                print(f"    ==> Parabolic (Schrodinger) fit is better")
                print(f"    ==> Non-relativistic regime")
            else:
                print(f"    ==> Neither fit is strong (R^2 < 0.8)")

    # ==================================================================
    # APPROACH 3: Causal asymmetry (retarded vs advanced)
    # ==================================================================
    print("\n\n" + "=" * 72)
    print("APPROACH 3: Causal asymmetry (forward vs backward propagator)")
    print("  Lorentzian: G_retarded != G_advanced (causal arrow)")
    print("  Euclidean: G_retarded = G_advanced (time-symmetric)")
    print("=" * 72)

    for name, wfn in kernels:
        asym, eig_diff, M_fwd, M_bwd = retarded_vs_advanced_test(
            0.5, 6, 5.0, wfn, p=1
        )
        label = "CAUSAL (Lorentzian)" if asym > 0.1 else "SYMMETRIC (Euclidean)" if asym < 0.01 else "WEAK ASYMMETRY"
        print(f"  {name:<15s}: asymmetry={asym:.4f}, eig_diff={eig_diff:.4f}  [{label}]")

    # ==================================================================
    # VERDICT
    # ==================================================================
    print("\n\n" + "=" * 72)
    print("VERDICT")
    print("=" * 72)
    print()
    print("  APPROACH 1 (phase-weighted metric): Check results above.")
    print("  If Lorentzian signature appears at any k value, the phase")
    print("  structure CAN produce a timelike/spacelike distinction.")
    print()
    print("  APPROACH 2 (Green's function): If E^2 = m^2 + c^2*k^2 fits")
    print("  better than E = a + b*k^2, the dispersion is relativistic")
    print("  (Lorentzian light-cone structure in momentum space).")
    print()
    print("  APPROACH 3 (causal asymmetry): If forward != backward")
    print("  propagator, the model has a causal arrow (time direction).")
    print("  Any decreasing angular kernel w(theta) creates this asymmetry")
    print("  because w(theta) != w(pi - theta) in general.")
    print()


if __name__ == "__main__":
    main()
