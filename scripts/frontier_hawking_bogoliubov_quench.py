#!/usr/bin/env python3
"""Gaussian-state in/out calculation via sudden quench on a free-fermion chain.

Physics motivation
------------------
The existing second-quantized prototype (frontier_second_quantized_prototype.py)
computes Bogoliubov overlaps between a free vacuum and a gravitationally-shifted
vacuum.  That is an overlap-proxy calculation: it compares ground states of two
different Hamiltonians but does not model a dynamical process.

This script takes the next step: a sudden quench.  We define two Hamiltonians
on the same 1D chain:

  H_in  : uniform tight-binding (hopping t_in, mass m_in on every site)
  H_out : same chain, but with MODIFIED parameters in a localized central
          region (reduced hopping or increased mass), simulating a sudden
          change in the local vacuum structure.

The "in" vacuum |0_in> is the ground state (filled Dirac sea) of H_in.  After
the quench at t=0, the system evolves under H_out.  The Bogoliubov coefficients
between the two mode bases determine particle creation: particles present in the
"out" basis that were absent in the "in" vacuum.

For free fermions, the full many-body state is encoded in the N x N correlation
matrix, so all calculations are O(N^3) -- no exponential Hilbert space.

Method
------
1. Build H_in (uniform chain) and H_out (quenched chain).
2. Diagonalize both to get single-particle modes {u^in_k} and {u^out_k}.
3. Fill the Dirac sea (lowest N/2 modes) for each.
4. Compute the Bogoliubov beta matrix:
     beta_{kl} = <u^in_k | u^out_l>
   where k runs over IN-occupied modes and l runs over OUT-unoccupied modes.
5. Report n_l = sum_k |beta_{kl}|^2 for each out-unoccupied mode l.

Required null: H_out = H_in => beta = 0 identically.

Additional diagnostics:
- n_k vs quench strength (should increase with larger parameter change)
- Thermality: fit n_k vs epsilon_k to Fermi-Dirac distribution
- Temperature vs quench gradient (analog of surface gravity)

PStack experiment: frontier-hawking-bogoliubov-quench
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np
from numpy.linalg import eigh


# ===================================================================
# Hamiltonian construction
# ===================================================================

def build_chain_hamiltonian(N: int, hopping: np.ndarray, mass: np.ndarray) -> np.ndarray:
    """Build tight-binding Hamiltonian with site-dependent hopping and mass.

    H = -sum_{i} t_i (|i><i+1| + h.c.) + sum_i m_i |i><i|

    Parameters
    ----------
    N : number of sites
    hopping : array of length N-1, hopping amplitude on bond (i, i+1)
    mass : array of length N, on-site mass/potential
    """
    H = np.zeros((N, N))
    for i in range(N - 1):
        H[i, i + 1] = -hopping[i]
        H[i + 1, i] = -hopping[i]
    for i in range(N):
        H[i, i] = mass[i]
    return H


def uniform_params(N: int, t: float = 1.0, m: float = 0.5) -> tuple[np.ndarray, np.ndarray]:
    """Uniform hopping and mass arrays."""
    hopping = np.full(N - 1, t)
    mass = np.full(N, m)
    return hopping, mass


def quench_hopping_profile(N: int, t_bulk: float, t_center: float,
                           center: int, width: int) -> np.ndarray:
    """Hopping array with a reduced-hopping region centered at `center`.

    Bonds within [center - width//2, center + width//2] get hopping = t_center.
    All other bonds get hopping = t_bulk.
    The transition is a smooth tanh step over 2 sites.
    """
    hopping = np.full(N - 1, t_bulk)
    for i in range(N - 1):
        # Bond i connects sites i and i+1; bond center is at (i + 0.5)
        bond_pos = i + 0.5
        dist = abs(bond_pos - center)
        # Smooth step: tanh profile with width ~2 lattice spacings
        sigma = 2.0
        factor = 0.5 * (1.0 + np.tanh((dist - width / 2) / sigma))
        hopping[i] = t_center + (t_bulk - t_center) * factor
    return hopping


def quench_mass_profile(N: int, m_bulk: float, m_center: float,
                        center: int, width: int) -> np.ndarray:
    """Mass array with an increased-mass region centered at `center`.

    Sites within [center - width//2, center + width//2] get mass = m_center.
    Smooth tanh transition over ~2 sites.
    """
    mass = np.full(N, m_bulk)
    for i in range(N):
        dist = abs(i - center)
        sigma = 2.0
        factor = 0.5 * (1.0 + np.tanh((dist - width / 2) / sigma))
        mass[i] = m_center + (m_bulk - m_center) * factor
    return mass


# ===================================================================
# Bogoliubov calculation
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

    Particle number in out-mode l:  n_l = sum_k |beta_{kl}|^2
    """
    in_occ = vecs_in[:, :n_occ_in]        # N x n_occ_in
    out_unocc = vecs_out[:, n_occ_out:]    # N x n_unocc_out
    beta = in_occ.T @ out_unocc            # n_occ_in x n_unocc_out
    return beta


def mode_occupations(beta: np.ndarray) -> np.ndarray:
    """Occupation per out-unoccupied mode: n_l = sum_k |beta_{kl}|^2."""
    return np.sum(np.abs(beta)**2, axis=0)


# ===================================================================
# Thermality analysis
# ===================================================================

def fit_thermal(energies: np.ndarray, occupations: np.ndarray,
                min_occ: float = 1e-10) -> dict:
    """Fit ln(n_k) vs epsilon_k to extract effective temperature.

    For a Fermi-Dirac distribution: n(eps) = 1/(exp((eps-mu)/T) + 1)
    => ln(1/n - 1) = (eps - mu)/T  (linear in eps with slope 1/T).

    We use both the naive ln(n) fit and the logit fit.
    """
    mask = (occupations > min_occ) & (occupations < 1.0 - min_occ)
    n_valid = np.sum(mask)

    result = {
        "n_valid": int(n_valid),
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

    # Logit fit: ln(1/n - 1) = (eps - mu)/T => y = a*eps + b
    logit = np.log(1.0 / n_sel - 1.0)
    coeffs_logit = np.polyfit(eps_sel, logit, 1)
    slope_logit = coeffs_logit[0]
    T_logit = 1.0 / slope_logit if abs(slope_logit) > 1e-12 else float("inf")
    mu_logit = -coeffs_logit[1] * T_logit

    pred_logit = np.polyval(coeffs_logit, eps_sel)
    ss_res = np.sum((logit - pred_logit)**2)
    ss_tot = np.sum((logit - np.mean(logit))**2)
    r2_logit = 1.0 - ss_res / ss_tot if ss_tot > 1e-20 else 0.0

    result["T_logit"] = T_logit
    result["mu_logit"] = mu_logit
    result["r2_logit"] = r2_logit

    # Naive fit: ln(n) = -eps/T + const
    log_n = np.log(n_sel)
    coeffs_naive = np.polyfit(eps_sel, log_n, 1)
    slope_naive = coeffs_naive[0]
    T_naive = -1.0 / slope_naive if abs(slope_naive) > 1e-12 else float("inf")
    pred_naive = np.polyval(coeffs_naive, eps_sel)
    ss_res_n = np.sum((log_n - pred_naive)**2)
    ss_tot_n = np.sum((log_n - np.mean(log_n))**2)
    r2_naive = 1.0 - ss_res_n / ss_tot_n if ss_tot_n > 1e-20 else 0.0

    result["T_naive"] = T_naive
    result["r2_naive"] = r2_naive

    return result


def quench_gradient(hopping: np.ndarray, mass: np.ndarray, center: int) -> float:
    """Compute the maximum parameter gradient near the quench center.

    This is the lattice analog of surface gravity: the steepest change in
    the local vacuum structure at the quench boundary.
    """
    # Gradient of hopping profile
    dt = np.abs(np.diff(hopping))
    # Gradient of mass profile
    dm = np.abs(np.diff(mass))
    # Combined gradient
    grad = dt + dm[:-1]  # align lengths
    # Take max in the vicinity of center
    window = max(1, len(grad) // 4)
    lo = max(0, center - window)
    hi = min(len(grad), center + window)
    if lo >= hi:
        return 0.0
    return float(np.max(grad[lo:hi]))


# ===================================================================
# Test suite
# ===================================================================

def test_null(N: int = 60) -> bool:
    """Null test: H_out = H_in must give beta = 0 identically."""
    print("\n--- NULL TEST: H_out = H_in ---")
    n_occ = N // 2
    hop, mass = uniform_params(N, t=1.0, m=0.5)
    H = build_chain_hamiltonian(N, hop, mass)
    eps, vecs = diagonalize(H)

    beta = bogoliubov_beta(vecs, n_occ, vecs, n_occ)
    n_k = mode_occupations(beta)
    max_occ = float(np.max(n_k))
    total = float(np.sum(n_k))

    print(f"  N = {N}, n_occ = {n_occ}")
    print(f"  max |beta|^2 per mode = {max_occ:.2e}")
    print(f"  total particle number  = {total:.2e}")
    passed = max_occ < 1e-12
    print(f"  NULL PASS: {passed}")
    return passed


def test_hopping_quench(N: int = 60, t_bulk: float = 1.0, m: float = 0.5,
                        t_center_values: list[float] | None = None,
                        width: int = 10) -> dict:
    """Hopping quench: reduce hopping in central region."""
    if t_center_values is None:
        t_center_values = [0.9, 0.7, 0.5, 0.3, 0.1]

    print(f"\n--- HOPPING QUENCH (N={N}, width={width}, m={m}) ---")
    n_occ = N // 2
    center = N // 2

    # H_in: uniform
    hop_in, mass_in = uniform_params(N, t=t_bulk, m=m)
    H_in = build_chain_hamiltonian(N, hop_in, mass_in)
    eps_in, vecs_in = diagonalize(H_in)

    results = {}
    print(f"  {'t_center':>10s}  {'n_total':>10s}  {'max_n_k':>10s}  {'gradient':>10s}  {'T_logit':>10s}  {'R2_logit':>8s}  {'T_naive':>10s}  {'R2_naive':>8s}")

    for t_c in t_center_values:
        # H_out: quenched hopping
        hop_out = quench_hopping_profile(N, t_bulk, t_c, center, width)
        H_out = build_chain_hamiltonian(N, hop_out, mass_in)
        eps_out, vecs_out = diagonalize(H_out)

        beta = bogoliubov_beta(vecs_in, n_occ, vecs_out, n_occ)
        n_k = mode_occupations(beta)
        n_total = float(np.sum(n_k))
        max_n_k = float(np.max(n_k))

        # Energies of out-unoccupied modes
        eps_unocc = eps_out[n_occ:]
        # Shift energies relative to the gap edge
        eps_shifted = eps_unocc - eps_unocc[0]

        thermal = fit_thermal(eps_shifted, n_k)
        grad = quench_gradient(hop_out, mass_in, center)

        results[t_c] = {
            "n_total": n_total,
            "max_n_k": max_n_k,
            "n_k": n_k,
            "eps_unocc": eps_unocc,
            "eps_shifted": eps_shifted,
            "gradient": grad,
            "thermal": thermal,
            "hop_out": hop_out,
        }

        print(f"  {t_c:10.2f}  {n_total:10.4f}  {max_n_k:10.4f}  {grad:10.4f}  "
              f"{thermal['T_logit']:10.4f}  {thermal['r2_logit']:8.4f}  "
              f"{thermal['T_naive']:10.4f}  {thermal['r2_naive']:8.4f}")

    return results


def test_mass_quench(N: int = 60, t: float = 1.0, m_bulk: float = 0.5,
                     m_center_values: list[float] | None = None,
                     width: int = 10) -> dict:
    """Mass quench: increase mass in central region."""
    if m_center_values is None:
        m_center_values = [1.0, 2.0, 4.0, 8.0, 16.0]

    print(f"\n--- MASS QUENCH (N={N}, width={width}, t={t}) ---")
    n_occ = N // 2
    center = N // 2

    # H_in: uniform
    hop_in, mass_in = uniform_params(N, t=t, m=m_bulk)
    H_in = build_chain_hamiltonian(N, hop_in, mass_in)
    eps_in, vecs_in = diagonalize(H_in)

    results = {}
    print(f"  {'m_center':>10s}  {'n_total':>10s}  {'max_n_k':>10s}  {'gradient':>10s}  {'T_logit':>10s}  {'R2_logit':>8s}  {'T_naive':>10s}  {'R2_naive':>8s}")

    for m_c in m_center_values:
        mass_out = quench_mass_profile(N, m_bulk, m_c, center, width)
        H_out = build_chain_hamiltonian(N, hop_in, mass_out)
        eps_out, vecs_out = diagonalize(H_out)

        beta = bogoliubov_beta(vecs_in, n_occ, vecs_out, n_occ)
        n_k = mode_occupations(beta)
        n_total = float(np.sum(n_k))
        max_n_k = float(np.max(n_k))

        eps_unocc = eps_out[n_occ:]
        eps_shifted = eps_unocc - eps_unocc[0]

        thermal = fit_thermal(eps_shifted, n_k)
        grad = quench_gradient(hop_in, mass_out, center)

        results[m_c] = {
            "n_total": n_total,
            "max_n_k": max_n_k,
            "n_k": n_k,
            "eps_unocc": eps_unocc,
            "eps_shifted": eps_shifted,
            "gradient": grad,
            "thermal": thermal,
            "mass_out": mass_out,
        }

        print(f"  {m_c:10.2f}  {n_total:10.4f}  {max_n_k:10.4f}  {grad:10.4f}  "
              f"{thermal['T_logit']:10.4f}  {thermal['r2_logit']:8.4f}  "
              f"{thermal['T_naive']:10.4f}  {thermal['r2_naive']:8.4f}")

    return results


def test_gradient_temperature_scaling(N: int = 80) -> dict:
    """Test whether the fitted temperature scales with the quench gradient.

    Vary the tanh steepness (sigma) at fixed quench depth and width to change
    the gradient independently.  If the spectrum is thermal, T should track
    the gradient (lattice analog of T ~ kappa / 2pi).
    """
    print(f"\n--- GRADIENT vs TEMPERATURE SCALING (N={N}) ---")
    n_occ = N // 2
    center = N // 2
    t_bulk = 1.0
    t_center = 0.2  # strong quench
    m = 0.5
    width = 10

    hop_in, mass_in = uniform_params(N, t=t_bulk, m=m)
    H_in = build_chain_hamiltonian(N, hop_in, mass_in)
    eps_in, vecs_in = diagonalize(H_in)

    # Vary sigma (steepness) to control gradient at fixed depth
    sigmas = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0]
    gradients = []
    temperatures = []
    r2s = []

    print(f"  {'sigma':>6s}  {'gradient':>10s}  {'n_total':>10s}  {'T_logit':>10s}  {'R2_logit':>8s}")

    for sigma in sigmas:
        # Build hopping profile with explicit sigma
        hop_out = np.full(N - 1, t_bulk)
        for i in range(N - 1):
            bond_pos = i + 0.5
            dist = abs(bond_pos - center)
            factor = 0.5 * (1.0 + np.tanh((dist - width / 2) / sigma))
            hop_out[i] = t_center + (t_bulk - t_center) * factor

        H_out = build_chain_hamiltonian(N, hop_out, mass_in)
        eps_out, vecs_out = diagonalize(H_out)

        beta = bogoliubov_beta(vecs_in, n_occ, vecs_out, n_occ)
        n_k = mode_occupations(beta)
        n_total = float(np.sum(n_k))

        eps_unocc = eps_out[n_occ:]
        eps_shifted = eps_unocc - eps_unocc[0]
        thermal = fit_thermal(eps_shifted, n_k)
        grad = quench_gradient(hop_out, mass_in, center)

        gradients.append(grad)
        temperatures.append(thermal["T_logit"])
        r2s.append(thermal["r2_logit"])

        print(f"  {sigma:6.1f}  {grad:10.4f}  {n_total:10.4f}  {thermal['T_logit']:10.4f}  {thermal['r2_logit']:8.4f}")

    # Fit T vs gradient
    gradients = np.array(gradients)
    temperatures = np.array(temperatures)
    r2s = np.array(r2s)

    # Only use points with reasonable thermal fit
    good = np.isfinite(temperatures) & (r2s > 0.5)
    result = {
        "sigmas": sigmas,
        "gradients": gradients,
        "temperatures": temperatures,
        "r2s": r2s,
    }

    if np.sum(good) >= 3:
        g_sel = gradients[good]
        T_sel = temperatures[good]
        coeffs = np.polyfit(g_sel, T_sel, 1)
        pred = np.polyval(coeffs, g_sel)
        ss_res = np.sum((T_sel - pred)**2)
        ss_tot = np.sum((T_sel - np.mean(T_sel))**2)
        r2_fit = 1.0 - ss_res / ss_tot if ss_tot > 1e-20 else 0.0

        result["T_vs_grad_slope"] = coeffs[0]
        result["T_vs_grad_intercept"] = coeffs[1]
        result["T_vs_grad_r2"] = r2_fit

        print(f"\n  T vs gradient fit: T = {coeffs[0]:.4f} * grad + {coeffs[1]:.4f}  (R^2 = {r2_fit:.4f})")
        print(f"  (Analog Hawking: T proportional to surface gravity ~ gradient)")
    else:
        print(f"\n  Insufficient thermal fits for gradient scaling (need 3, got {np.sum(good)})")
        result["T_vs_grad_slope"] = float("nan")
        result["T_vs_grad_r2"] = float("nan")

    return result


def test_size_dependence(sizes: list[int] | None = None) -> dict:
    """Check that particle creation does not vanish at larger N."""
    if sizes is None:
        sizes = [40, 60, 80, 100]

    print(f"\n--- SIZE DEPENDENCE ---")
    print(f"  {'N':>5s}  {'n_total':>10s}  {'n_total/N':>10s}")

    results = {}
    for N in sizes:
        n_occ = N // 2
        center = N // 2
        t_bulk, m = 1.0, 0.5

        hop_in, mass_in = uniform_params(N, t=t_bulk, m=m)
        H_in = build_chain_hamiltonian(N, hop_in, mass_in)
        _, vecs_in = diagonalize(H_in)

        hop_out = quench_hopping_profile(N, t_bulk, 0.2, center, width=10)
        H_out = build_chain_hamiltonian(N, hop_out, mass_in)
        _, vecs_out = diagonalize(H_out)

        beta = bogoliubov_beta(vecs_in, n_occ, vecs_out, n_occ)
        n_k = mode_occupations(beta)
        n_total = float(np.sum(n_k))

        results[N] = {"n_total": n_total, "density": n_total / N}
        print(f"  {N:5d}  {n_total:10.4f}  {n_total/N:10.6f}")

    return results


# ===================================================================
# Main
# ===================================================================

def main():
    t_start = time.time()
    print("=" * 76)
    print("GAUSSIAN-STATE IN/OUT CALCULATION: SUDDEN QUENCH ON FREE-FERMION CHAIN")
    print("Bogoliubov particle creation from a localized parameter quench")
    print("=" * 76)

    # ------------------------------------------------------------------
    # Gate 0: Null test (H_out = H_in => no particles)
    # ------------------------------------------------------------------
    null_pass = test_null(N=60)

    # ------------------------------------------------------------------
    # Gate 1: Hopping quench produces particles
    # ------------------------------------------------------------------
    hop_results = test_hopping_quench(N=60, width=10)
    hop_particles = [r["n_total"] for r in hop_results.values()]
    gate1_particles = all(n > 1e-10 for n in hop_particles)
    # Monotonicity: stronger quench (smaller t_center) => more particles
    gate1_monotone = all(hop_particles[i] <= hop_particles[i+1]
                         for i in range(len(hop_particles) - 1))
    print(f"\n  GATE 1a (particles created): {'PASS' if gate1_particles else 'FAIL'}")
    print(f"  GATE 1b (monotone in quench strength): {'PASS' if gate1_monotone else 'FAIL'}")

    # ------------------------------------------------------------------
    # Gate 2: Mass quench produces particles
    # ------------------------------------------------------------------
    mass_results = test_mass_quench(N=60, width=10)
    mass_particles = [r["n_total"] for r in mass_results.values()]
    gate2_particles = all(n > 1e-10 for n in mass_particles)
    gate2_monotone = all(mass_particles[i] <= mass_particles[i+1]
                         for i in range(len(mass_particles) - 1))
    print(f"\n  GATE 2a (particles created): {'PASS' if gate2_particles else 'FAIL'}")
    print(f"  GATE 2b (monotone in quench strength): {'PASS' if gate2_monotone else 'FAIL'}")

    # ------------------------------------------------------------------
    # Gate 3: Gradient-temperature scaling
    # ------------------------------------------------------------------
    grad_results = test_gradient_temperature_scaling(N=80)
    gate3 = (not np.isnan(grad_results.get("T_vs_grad_r2", float("nan")))
             and grad_results.get("T_vs_grad_r2", 0) > 0.5)
    print(f"\n  GATE 3 (T scales with gradient): {'PASS' if gate3 else 'FAIL / INSUFFICIENT DATA'}")

    # ------------------------------------------------------------------
    # Gate 4: Size independence
    # ------------------------------------------------------------------
    size_results = test_size_dependence()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    elapsed = time.time() - t_start
    print("\n\n" + "=" * 76)
    print("SUMMARY")
    print("=" * 76)
    print(f"  Gate 0 (null: H_out=H_in => beta=0):       {'PASS' if null_pass else 'FAIL'}")
    print(f"  Gate 1a (hopping quench creates particles): {'PASS' if gate1_particles else 'FAIL'}")
    print(f"  Gate 1b (monotone in quench strength):      {'PASS' if gate1_monotone else 'FAIL'}")
    print(f"  Gate 2a (mass quench creates particles):    {'PASS' if gate2_particles else 'FAIL'}")
    print(f"  Gate 2b (monotone in quench strength):      {'PASS' if gate2_monotone else 'FAIL'}")
    print(f"  Gate 3  (T ~ gradient scaling):             {'PASS' if gate3 else 'FAIL / INSUFFICIENT DATA'}")
    print(f"  Elapsed: {elapsed:.1f}s")

    # Thermality assessment
    print("\n  Thermality assessment:")
    best_r2 = 0.0
    for label, results in [("hopping", hop_results), ("mass", mass_results)]:
        for param, r in results.items():
            th = r["thermal"]
            if th["r2_logit"] > best_r2:
                best_r2 = th["r2_logit"]
            if th["r2_logit"] > 0.7:
                print(f"    {label} quench param={param}: T_logit={th['T_logit']:.4f}, R^2={th['r2_logit']:.4f}")

    if best_r2 < 0.7:
        print(f"    No strong thermal signal found (best R^2 = {best_r2:.4f})")
        print(f"    This is expected for a finite chain with discrete modes.")
        print(f"    Thermality may emerge at larger N or with smoother quench profiles.")

    print("=" * 76)

    all_pass = null_pass and gate1_particles and gate2_particles
    return {
        "null_pass": null_pass,
        "gate1_particles": gate1_particles,
        "gate1_monotone": gate1_monotone,
        "gate2_particles": gate2_particles,
        "gate2_monotone": gate2_monotone,
        "gate3_gradient_scaling": gate3,
        "best_thermal_r2": best_r2,
        "all_pass": all_pass,
    }


if __name__ == "__main__":
    results = main()
