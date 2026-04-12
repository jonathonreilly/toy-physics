#!/usr/bin/env python3
"""3D Bogoliubov quench with spherical horizon geometry.

Physics motivation
------------------
The 1D chain quench (frontier_hawking_bogoliubov_quench.py) demonstrated that
a sudden parameter change produces Bogoliubov particle creation with T
proportional to the hopping gradient (R^2 ~ 0.97).  However, a 1D chain has
no real horizon geometry -- there is no notion of a closed surface separating
an interior from an exterior.

This script upgrades to a 3D cubic lattice with a SPHERICAL quench boundary.
Inside a sphere of radius R_h, hopping is reduced (creating a "slow zone" --
analog of a black hole interior where the effective speed of light is reduced).
Outside the sphere, hopping is unchanged.  The spherical surface at r = R_h
is the discrete analog of a black hole horizon.

This is a Gaussian-state (free-fermion) calculation -- NOT a claim about
quantum gravity.  See docs/HAWKING_3D_QUENCH_NOTE.md for scope.

Method
------
1. H_in: uniform tight-binding on N^3 cubic lattice
2. H_out: same lattice but with reduced hopping inside a sphere of radius R_h
   - Smooth tanh transition over ~2 lattice spacings at the boundary
3. Diagonalize both (N^3 x N^3 dense or sparse matrices)
4. Fill the Fermi sea (half-filling)
5. Compute Bogoliubov coefficients: beta_{kl} = <k_out|l_in>
   for k above Fermi level (out), l below Fermi level (in)
6. Particle number: n_k = sum_l |beta_{kl}|^2

Tests
-----
- Null: H_out = H_in => n_k = 0
- Thermality: fit n_k vs epsilon_k to Fermi-Dirac
- T vs surface gravity (quench strength)
- T vs 1/R_h (larger horizon = colder)
- Spatial profile: particle creation concentrated near r = R_h

Tractability: N=10 => 1000 sites (~1s), N=12 => 1728 (~5s), N=14 => 2744 (~30s)

PStack experiment: frontier-hawking-3d-quench
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np
from numpy.linalg import eigh


# ===================================================================
# 3D lattice Hamiltonian
# ===================================================================

def site_index(x: int, y: int, z: int, L: int) -> int:
    """Flat index for site (x, y, z) on an L x L x L cubic lattice."""
    return x * L * L + y * L + z


def site_coords(idx: int, L: int) -> tuple[int, int, int]:
    """Recover (x, y, z) from flat index."""
    x = idx // (L * L)
    y = (idx % (L * L)) // L
    z = idx % L
    return x, y, z


def site_radius(x: int, y: int, z: int, L: int) -> float:
    """Distance from site (x, y, z) to the lattice center."""
    cx = (L - 1) / 2.0
    cy = (L - 1) / 2.0
    cz = (L - 1) / 2.0
    return math.sqrt((x - cx)**2 + (y - cy)**2 + (z - cz)**2)


def bond_radius(x1: int, y1: int, z1: int,
                x2: int, y2: int, z2: int, L: int) -> float:
    """Distance from the midpoint of bond (site1, site2) to the lattice center."""
    cx = (L - 1) / 2.0
    cy = (L - 1) / 2.0
    cz = (L - 1) / 2.0
    mx = (x1 + x2) / 2.0
    my = (y1 + y2) / 2.0
    mz = (z1 + z2) / 2.0
    return math.sqrt((mx - cx)**2 + (my - cy)**2 + (mz - cz)**2)


def hopping_factor(r: float, R_h: float, quench_strength: float,
                   sigma: float = 2.0) -> float:
    """Smooth hopping profile for the spherical quench.

    Inside r < R_h: hopping = t0 * (1 - quench_strength)
    Outside r > R_h: hopping = t0
    Smooth tanh transition of width sigma lattice spacings.

    Returns a multiplicative factor in [1 - quench_strength, 1].
    """
    # tanh goes from -1 (r << R_h) to +1 (r >> R_h)
    transition = 0.5 * (1.0 + math.tanh((r - R_h) / sigma))
    # factor = (1 - quench_strength) when r << R_h, 1 when r >> R_h
    return (1.0 - quench_strength) + quench_strength * transition


def build_3d_hamiltonian(L: int, t0: float = 1.0, m: float = 0.0,
                         R_h: float | None = None,
                         quench_strength: float = 0.0,
                         sigma: float = 2.0) -> np.ndarray:
    """Build tight-binding Hamiltonian on an L x L x L cubic lattice.

    H = -sum_{<ij>} t_ij (|i><j| + h.c.) + m * sum_i |i><i|

    If R_h is provided, bond hopping is modulated by the spherical profile:
    bonds inside the sphere get reduced hopping.

    Parameters
    ----------
    L : side length of cubic lattice
    t0 : base hopping amplitude
    m : uniform on-site mass
    R_h : horizon radius (None for uniform Hamiltonian)
    quench_strength : fraction by which hopping is reduced inside sphere
    sigma : tanh transition width in lattice spacings
    """
    N = L ** 3
    H = np.zeros((N, N))

    for x in range(L):
        for y in range(L):
            for z in range(L):
                i = site_index(x, y, z, L)
                H[i, i] = m

                # Nearest-neighbor bonds in +x, +y, +z directions
                neighbors = []
                if x + 1 < L:
                    neighbors.append((x + 1, y, z))
                if y + 1 < L:
                    neighbors.append((x, y + 1, z))
                if z + 1 < L:
                    neighbors.append((x, y, z + 1))

                for (nx, ny, nz) in neighbors:
                    j = site_index(nx, ny, nz, L)
                    if R_h is not None and quench_strength > 0:
                        r = bond_radius(x, y, z, nx, ny, nz, L)
                        t_eff = t0 * hopping_factor(r, R_h, quench_strength, sigma)
                    else:
                        t_eff = t0
                    H[i, j] = -t_eff
                    H[j, i] = -t_eff

    return H


# ===================================================================
# Bogoliubov calculation (reused from 1D with minor adaptation)
# ===================================================================

def diagonalize(H: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Diagonalize Hermitian H. Returns (energies, eigenvectors) sorted ascending."""
    energies, vecs = eigh(H)
    return energies, vecs


def bogoliubov_beta(vecs_in: np.ndarray, n_occ_in: int,
                    vecs_out: np.ndarray, n_occ_out: int) -> np.ndarray:
    """Compute the Bogoliubov beta matrix.

    beta_{kl} = <u^in_k | u^out_l>
    where k in IN-occupied, l in OUT-unoccupied.
    """
    in_occ = vecs_in[:, :n_occ_in]
    out_unocc = vecs_out[:, n_occ_out:]
    beta = in_occ.T @ out_unocc
    return beta


def mode_occupations(beta: np.ndarray) -> np.ndarray:
    """Occupation per out-unoccupied mode: n_l = sum_k |beta_{kl}|^2."""
    return np.sum(np.abs(beta)**2, axis=0)


# ===================================================================
# Thermality analysis
# ===================================================================

def fit_fermi_dirac(energies: np.ndarray, occupations: np.ndarray,
                    min_occ: float = 1e-10) -> dict:
    """Fit occupations to Fermi-Dirac distribution.

    For Fermi-Dirac: n(eps) = 1/(exp((eps-mu)/T) + 1)
    => ln(1/n - 1) = (eps - mu)/T  (logit transform, linear in eps)
    """
    mask = (occupations > min_occ) & (occupations < 1.0 - min_occ)
    n_valid = int(np.sum(mask))

    result = {
        "n_valid": n_valid,
        "T_logit": float("nan"),
        "mu_logit": float("nan"),
        "r2_logit": float("nan"),
        "T_naive": float("nan"),
        "r2_naive": float("nan"),
    }

    if n_valid < 3:
        return result

    eps_sel = energies[mask]
    n_sel = occupations[mask]

    # Logit fit
    logit = np.log(1.0 / n_sel - 1.0)
    coeffs = np.polyfit(eps_sel, logit, 1)
    slope = coeffs[0]
    T_logit = 1.0 / slope if abs(slope) > 1e-12 else float("inf")
    mu_logit = -coeffs[1] * T_logit

    pred = np.polyval(coeffs, eps_sel)
    ss_res = np.sum((logit - pred)**2)
    ss_tot = np.sum((logit - np.mean(logit))**2)
    r2_logit = 1.0 - ss_res / ss_tot if ss_tot > 1e-20 else 0.0

    result["T_logit"] = T_logit
    result["mu_logit"] = mu_logit
    result["r2_logit"] = r2_logit

    # Naive fit: ln(n) = -eps/T + const
    log_n = np.log(n_sel)
    coeffs_n = np.polyfit(eps_sel, log_n, 1)
    slope_n = coeffs_n[0]
    T_naive = -1.0 / slope_n if abs(slope_n) > 1e-12 else float("inf")
    pred_n = np.polyval(coeffs_n, eps_sel)
    ss_res_n = np.sum((log_n - pred_n)**2)
    ss_tot_n = np.sum((log_n - np.mean(log_n))**2)
    r2_naive = 1.0 - ss_res_n / ss_tot_n if ss_tot_n > 1e-20 else 0.0

    result["T_naive"] = T_naive
    result["r2_naive"] = r2_naive

    return result


def surface_gravity(L: int, R_h: float, quench_strength: float,
                    sigma: float = 2.0, t0: float = 1.0) -> float:
    """Compute the maximum hopping gradient at the horizon.

    This is the lattice analog of surface gravity kappa = |grad(t)| at r = R_h.
    We sample along a radial line and take the max |dt/dr|.
    """
    # Sample along a radial line from center to corner
    n_samples = max(L * 3, 100)
    r_max = L * math.sqrt(3) / 2.0
    rs = np.linspace(0, r_max, n_samples)
    ts = np.array([t0 * hopping_factor(r, R_h, quench_strength, sigma) for r in rs])
    dt_dr = np.abs(np.diff(ts) / np.diff(rs))
    return float(np.max(dt_dr))


# ===================================================================
# Spatial profile of particle creation
# ===================================================================

def radial_particle_profile(vecs_in: np.ndarray, n_occ_in: int,
                            vecs_out: np.ndarray, n_occ_out: int,
                            L: int) -> tuple[np.ndarray, np.ndarray]:
    """Compute radially-binned particle creation density.

    For each out-unoccupied mode l, the particle number is
    n_l = sum_k |beta_{kl}|^2.  We spatially resolve this by weighting
    each mode's contribution by its wavefunction amplitude at each site:
    delta_n(site_i) = sum_l n_l * |psi_l^out(i)|^2

    This gives the local density of created particles.

    Returns (radii, delta_n) where delta_n[i] is the average particle
    creation density at radius radii[i].
    """
    N = L ** 3

    # Bogoliubov particle numbers per out-unoccupied mode
    beta = bogoliubov_beta(vecs_in, n_occ_in, vecs_out, n_occ_out)
    n_per_mode = np.sum(np.abs(beta)**2, axis=0)  # per out-unoccupied mode

    # Spatial profile: weight by wavefunction amplitude of each mode
    out_unocc = vecs_out[:, n_occ_out:]  # N x n_unocc
    # delta_n(i) = sum_l n_l |psi_l(i)|^2
    delta_n = np.sum(n_per_mode[np.newaxis, :] * np.abs(out_unocc)**2, axis=1)

    # Bin by radius
    radii_all = np.array([site_radius(*site_coords(i, L), L) for i in range(N)])
    r_max = radii_all.max()
    n_bins = max(int(r_max) + 1, 10)
    bin_edges = np.linspace(0, r_max + 0.5, n_bins + 1)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    binned_delta = np.zeros(n_bins)
    counts = np.zeros(n_bins)
    for i in range(N):
        b = min(int(np.searchsorted(bin_edges, radii_all[i]) - 1), n_bins - 1)
        b = max(b, 0)
        binned_delta[b] += delta_n[i]
        counts[b] += 1

    mask = counts > 0
    binned_delta[mask] /= counts[mask]

    return bin_centers, binned_delta


# ===================================================================
# Test suite
# ===================================================================

def test_null(L: int = 8) -> bool:
    """Null test: H_out = H_in must give zero particle creation."""
    print("\n--- NULL TEST: H_out = H_in (3D) ---")
    N = L ** 3
    n_occ = N // 2

    H = build_3d_hamiltonian(L, t0=1.0, m=0.5)
    eps, vecs = diagonalize(H)

    beta = bogoliubov_beta(vecs, n_occ, vecs, n_occ)
    n_k = mode_occupations(beta)
    max_occ = float(np.max(n_k))
    total = float(np.sum(n_k))

    print(f"  L = {L}, N = {N}, n_occ = {n_occ}")
    print(f"  max |beta|^2 per mode = {max_occ:.2e}")
    print(f"  total particle number  = {total:.2e}")
    passed = max_occ < 1e-12
    print(f"  NULL PASS: {passed}")
    return passed


def test_spherical_quench(L: int = 10, R_h: float = 3.0,
                          quench_strengths: list[float] | None = None) -> dict:
    """Spherical quench: reduce hopping inside a sphere of radius R_h."""
    if quench_strengths is None:
        quench_strengths = [0.1, 0.3, 0.5, 0.7, 0.9]

    N = L ** 3
    n_occ = N // 2
    t0 = 1.0
    m = 0.5

    print(f"\n--- SPHERICAL QUENCH (L={L}, N={N}, R_h={R_h:.1f}) ---")

    # H_in: uniform
    t_diag_start = time.time()
    H_in = build_3d_hamiltonian(L, t0=t0, m=m)
    eps_in, vecs_in = diagonalize(H_in)
    t_diag = time.time() - t_diag_start
    print(f"  H_in diagonalization: {t_diag:.2f}s")

    results = {}
    print(f"  {'quench':>8s}  {'n_total':>10s}  {'max_nk':>10s}  {'kappa':>8s}  "
          f"{'T_logit':>10s}  {'R2_logit':>8s}  {'T_naive':>10s}  {'R2_naive':>8s}")

    for qs in quench_strengths:
        H_out = build_3d_hamiltonian(L, t0=t0, m=m, R_h=R_h,
                                     quench_strength=qs)
        eps_out, vecs_out = diagonalize(H_out)

        beta = bogoliubov_beta(vecs_in, n_occ, vecs_out, n_occ)
        n_k = mode_occupations(beta)
        n_total = float(np.sum(n_k))
        max_nk = float(np.max(n_k))

        eps_unocc = eps_out[n_occ:]
        eps_shifted = eps_unocc - eps_unocc[0]

        thermal = fit_fermi_dirac(eps_shifted, n_k)
        kappa = surface_gravity(L, R_h, qs)

        results[qs] = {
            "n_total": n_total,
            "max_nk": max_nk,
            "n_k": n_k,
            "eps_unocc": eps_unocc,
            "eps_shifted": eps_shifted,
            "kappa": kappa,
            "thermal": thermal,
        }

        print(f"  {qs:8.2f}  {n_total:10.4f}  {max_nk:10.4f}  {kappa:8.4f}  "
              f"{thermal['T_logit']:10.4f}  {thermal['r2_logit']:8.4f}  "
              f"{thermal['T_naive']:10.4f}  {thermal['r2_naive']:8.4f}")

    return results


def test_T_vs_surface_gravity(L: int = 10, R_h: float = 3.0) -> dict:
    """Test whether fitted temperature scales with surface gravity kappa.

    Vary quench_strength at fixed R_h.  Surface gravity kappa = max |grad t|
    at the horizon.  Hawking analog predicts T proportional to kappa.
    """
    print(f"\n--- T vs SURFACE GRAVITY (L={L}, R_h={R_h:.1f}) ---")

    N = L ** 3
    n_occ = N // 2
    t0 = 1.0
    m = 0.5

    H_in = build_3d_hamiltonian(L, t0=t0, m=m)
    eps_in, vecs_in = diagonalize(H_in)

    quench_strengths = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    kappas = []
    temperatures = []
    r2s = []

    print(f"  {'quench':>8s}  {'kappa':>10s}  {'n_total':>10s}  {'T_logit':>10s}  {'R2_logit':>8s}")

    for qs in quench_strengths:
        H_out = build_3d_hamiltonian(L, t0=t0, m=m, R_h=R_h,
                                     quench_strength=qs)
        eps_out, vecs_out = diagonalize(H_out)

        beta = bogoliubov_beta(vecs_in, n_occ, vecs_out, n_occ)
        n_k = mode_occupations(beta)
        n_total = float(np.sum(n_k))

        eps_unocc = eps_out[n_occ:]
        eps_shifted = eps_unocc - eps_unocc[0]
        thermal = fit_fermi_dirac(eps_shifted, n_k)
        kappa = surface_gravity(L, R_h, qs)

        kappas.append(kappa)
        temperatures.append(thermal["T_logit"])
        r2s.append(thermal["r2_logit"])

        print(f"  {qs:8.2f}  {kappa:10.4f}  {n_total:10.4f}  "
              f"{thermal['T_logit']:10.4f}  {thermal['r2_logit']:8.4f}")

    kappas = np.array(kappas)
    temperatures = np.array(temperatures)
    r2s = np.array(r2s)

    # Fit T vs kappa for points with reasonable thermal fit
    good = np.isfinite(temperatures) & (r2s > 0.3) & (temperatures > 0)
    result = {
        "quench_strengths": quench_strengths,
        "kappas": kappas,
        "temperatures": temperatures,
        "r2s": r2s,
    }

    if np.sum(good) >= 3:
        k_sel = kappas[good]
        T_sel = temperatures[good]
        coeffs = np.polyfit(k_sel, T_sel, 1)
        pred = np.polyval(coeffs, k_sel)
        ss_res = np.sum((T_sel - pred)**2)
        ss_tot = np.sum((T_sel - np.mean(T_sel))**2)
        r2_fit = 1.0 - ss_res / ss_tot if ss_tot > 1e-20 else 0.0

        result["T_vs_kappa_slope"] = coeffs[0]
        result["T_vs_kappa_intercept"] = coeffs[1]
        result["T_vs_kappa_r2"] = r2_fit

        print(f"\n  T vs kappa fit: T = {coeffs[0]:.4f} * kappa + {coeffs[1]:.4f}  "
              f"(R^2 = {r2_fit:.4f})")
        print(f"  (Hawking analog: T proportional to surface gravity)")
    else:
        n_good = int(np.sum(good))
        print(f"\n  Insufficient thermal fits for T vs kappa (need 3, got {n_good})")
        result["T_vs_kappa_slope"] = float("nan")
        result["T_vs_kappa_r2"] = float("nan")

    return result


def test_T_vs_horizon_radius(L: int = 12) -> dict:
    """Test whether T scales as 1/R_h (larger horizon = colder).

    Hawking predicts T = kappa / (2 pi) and for Schwarzschild kappa ~ 1/R_s,
    so T ~ 1/R_h.  On a lattice we fix quench_strength and vary R_h.
    """
    print(f"\n--- T vs HORIZON RADIUS (L={L}) ---")

    N = L ** 3
    n_occ = N // 2
    t0 = 1.0
    m = 0.5
    quench_strength = 0.7  # strong enough for signal

    H_in = build_3d_hamiltonian(L, t0=t0, m=m)
    eps_in, vecs_in = diagonalize(H_in)

    # R_h values: from small to near the lattice boundary
    max_R = (L - 1) / 2.0 - 1.0  # stay away from boundary
    R_values = np.linspace(1.5, max_R, 6)

    radii = []
    temperatures = []
    kappas = []
    r2s = []

    print(f"  {'R_h':>6s}  {'kappa':>10s}  {'n_total':>10s}  {'T_logit':>10s}  "
          f"{'R2_logit':>8s}  {'1/R_h':>8s}")

    for R_h in R_values:
        H_out = build_3d_hamiltonian(L, t0=t0, m=m, R_h=R_h,
                                     quench_strength=quench_strength)
        eps_out, vecs_out = diagonalize(H_out)

        beta = bogoliubov_beta(vecs_in, n_occ, vecs_out, n_occ)
        n_k = mode_occupations(beta)
        n_total = float(np.sum(n_k))

        eps_unocc = eps_out[n_occ:]
        eps_shifted = eps_unocc - eps_unocc[0]
        thermal = fit_fermi_dirac(eps_shifted, n_k)
        kappa = surface_gravity(L, R_h, quench_strength)

        radii.append(R_h)
        temperatures.append(thermal["T_logit"])
        kappas.append(kappa)
        r2s.append(thermal["r2_logit"])

        print(f"  {R_h:6.2f}  {kappa:10.4f}  {n_total:10.4f}  "
              f"{thermal['T_logit']:10.4f}  {thermal['r2_logit']:8.4f}  {1.0/R_h:8.4f}")

    radii = np.array(radii)
    temperatures = np.array(temperatures)
    kappas = np.array(kappas)
    r2s = np.array(r2s)

    result = {
        "radii": radii,
        "temperatures": temperatures,
        "kappas": kappas,
        "r2s": r2s,
    }

    # Fit T vs 1/R_h
    good = np.isfinite(temperatures) & (r2s > 0.3) & (temperatures > 0)
    if np.sum(good) >= 3:
        inv_R = 1.0 / radii[good]
        T_sel = temperatures[good]
        coeffs = np.polyfit(inv_R, T_sel, 1)
        pred = np.polyval(coeffs, inv_R)
        ss_res = np.sum((T_sel - pred)**2)
        ss_tot = np.sum((T_sel - np.mean(T_sel))**2)
        r2_fit = 1.0 - ss_res / ss_tot if ss_tot > 1e-20 else 0.0

        result["T_vs_invR_slope"] = coeffs[0]
        result["T_vs_invR_intercept"] = coeffs[1]
        result["T_vs_invR_r2"] = r2_fit

        print(f"\n  T vs 1/R_h fit: T = {coeffs[0]:.4f} / R_h + {coeffs[1]:.4f}  "
              f"(R^2 = {r2_fit:.4f})")
        print(f"  (Hawking predicts T proportional to 1/R_h for Schwarzschild)")
    else:
        n_good = int(np.sum(good))
        print(f"\n  Insufficient thermal fits for T vs 1/R_h (need 3, got {n_good})")
        result["T_vs_invR_slope"] = float("nan")
        result["T_vs_invR_r2"] = float("nan")

    return result


def test_spatial_profile(L: int = 10, R_h: float = 3.0,
                         quench_strength: float = 0.7) -> dict:
    """Test that particle creation is concentrated near r = R_h."""
    print(f"\n--- SPATIAL PROFILE (L={L}, R_h={R_h:.1f}, qs={quench_strength}) ---")

    N = L ** 3
    n_occ = N // 2
    t0 = 1.0
    m = 0.5

    H_in = build_3d_hamiltonian(L, t0=t0, m=m)
    eps_in, vecs_in = diagonalize(H_in)

    H_out = build_3d_hamiltonian(L, t0=t0, m=m, R_h=R_h,
                                 quench_strength=quench_strength)
    eps_out, vecs_out = diagonalize(H_out)

    bin_centers, delta_n = radial_particle_profile(
        vecs_in, n_occ, vecs_out, n_occ, L)

    # Find the radius with maximum particle creation
    peak_idx = np.argmax(delta_n)
    peak_r = bin_centers[peak_idx]
    peak_dn = delta_n[peak_idx]

    print(f"  Radial bins: {len(bin_centers)}")
    print(f"  Peak particle creation at r = {peak_r:.2f} (R_h = {R_h:.1f})")
    print(f"  Peak |delta_n| = {peak_dn:.6f}")

    # Check if peak is near the horizon
    peak_near_horizon = abs(peak_r - R_h) < 2.0  # within 2 lattice spacings

    # Print radial profile
    print(f"\n  {'r':>6s}  {'delta_n':>14s}  {'bar':>20s}")
    max_dn = max(delta_n.max(), 1e-15)
    for i in range(len(bin_centers)):
        bar_len = int(40 * delta_n[i] / max_dn)
        marker = " <-- R_h" if abs(bin_centers[i] - R_h) < 0.5 else ""
        print(f"  {bin_centers[i]:6.2f}  {delta_n[i]:14.8f}  {'#' * bar_len}{marker}")

    print(f"\n  Peak near horizon (|r_peak - R_h| < 2): {peak_near_horizon}")

    return {
        "bin_centers": bin_centers,
        "delta_n": delta_n,
        "peak_r": peak_r,
        "peak_near_horizon": peak_near_horizon,
    }


# ===================================================================
# Main
# ===================================================================

def main():
    t_start = time.time()
    print("=" * 76)
    print("3D BOGOLIUBOV QUENCH WITH SPHERICAL HORIZON GEOMETRY")
    print("Gaussian-state particle creation from a spherical slow zone")
    print("=" * 76)

    # ------------------------------------------------------------------
    # Gate 0: Null test
    # ------------------------------------------------------------------
    null_pass = test_null(L=8)

    # ------------------------------------------------------------------
    # Gate 1: Spherical quench produces particles with monotone behavior
    # ------------------------------------------------------------------
    quench_results = test_spherical_quench(L=10, R_h=3.0)
    n_totals = [r["n_total"] for r in quench_results.values()]
    gate1_particles = all(n > 1e-10 for n in n_totals)
    gate1_monotone = all(n_totals[i] <= n_totals[i + 1]
                         for i in range(len(n_totals) - 1))
    print(f"\n  GATE 1a (particles created): {'PASS' if gate1_particles else 'FAIL'}")
    print(f"  GATE 1b (monotone in quench strength): {'PASS' if gate1_monotone else 'FAIL'}")

    # ------------------------------------------------------------------
    # Gate 2: T vs surface gravity
    # ------------------------------------------------------------------
    kappa_results = test_T_vs_surface_gravity(L=10, R_h=3.0)
    gate2 = (not np.isnan(kappa_results.get("T_vs_kappa_r2", float("nan")))
             and kappa_results.get("T_vs_kappa_r2", 0) > 0.5)
    print(f"\n  GATE 2 (T proportional to kappa): {'PASS' if gate2 else 'FAIL / INSUFFICIENT DATA'}")

    # ------------------------------------------------------------------
    # Gate 3: T vs 1/R_h
    # ------------------------------------------------------------------
    radius_results = test_T_vs_horizon_radius(L=12)
    gate3 = (not np.isnan(radius_results.get("T_vs_invR_r2", float("nan")))
             and radius_results.get("T_vs_invR_r2", 0) > 0.5)
    print(f"\n  GATE 3 (T proportional to 1/R_h): {'PASS' if gate3 else 'FAIL / INSUFFICIENT DATA'}")

    # ------------------------------------------------------------------
    # Gate 4: Spatial profile peaks near horizon
    # ------------------------------------------------------------------
    profile = test_spatial_profile(L=10, R_h=3.0, quench_strength=0.7)
    gate4 = profile["peak_near_horizon"]
    print(f"\n  GATE 4 (creation peaks near horizon): {'PASS' if gate4 else 'FAIL'}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    elapsed = time.time() - t_start
    print("\n\n" + "=" * 76)
    print("SUMMARY")
    print("=" * 76)
    print(f"  Gate 0 (null: H_out=H_in => beta=0):       {'PASS' if null_pass else 'FAIL'}")
    print(f"  Gate 1a (spherical quench creates particles):{'PASS' if gate1_particles else 'FAIL'}")
    print(f"  Gate 1b (monotone in quench strength):      {'PASS' if gate1_monotone else 'FAIL'}")
    print(f"  Gate 2  (T proportional to kappa):          {'PASS' if gate2 else 'FAIL / INSUFFICIENT'}")
    print(f"  Gate 3  (T proportional to 1/R_h):          {'PASS' if gate3 else 'FAIL / INSUFFICIENT'}")
    print(f"  Gate 4  (creation peaks near horizon):      {'PASS' if gate4 else 'FAIL'}")
    print(f"  Elapsed: {elapsed:.1f}s")

    # Thermality assessment
    print("\n  Thermality assessment (3D spherical):")
    best_r2 = 0.0
    for qs, r in quench_results.items():
        th = r["thermal"]
        if th["r2_logit"] > best_r2:
            best_r2 = th["r2_logit"]
        if th["r2_logit"] > 0.5:
            print(f"    quench={qs:.1f}: T_logit={th['T_logit']:.4f}, "
                  f"R^2={th['r2_logit']:.4f}")

    if best_r2 < 0.5:
        print(f"    No strong thermal signal (best R^2 = {best_r2:.4f})")
        print(f"    This may require larger L or smoother profiles.")

    print("=" * 76)

    all_pass = null_pass and gate1_particles
    return {
        "null_pass": null_pass,
        "gate1_particles": gate1_particles,
        "gate1_monotone": gate1_monotone,
        "gate2_T_vs_kappa": gate2,
        "gate3_T_vs_invR": gate3,
        "gate4_spatial_peak": gate4,
        "best_thermal_r2": best_r2,
        "all_pass": all_pass,
    }


if __name__ == "__main__":
    results = main()
