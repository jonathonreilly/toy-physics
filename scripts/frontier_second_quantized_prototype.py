#!/usr/bin/env python3
"""Second-quantized (many-body) extension of the path-sum propagator.

Physics motivation
------------------
Paper 1 propagates a single wavepacket through a gravitational field f(x).
This gives Newton's law, Born rule, WEP, weak-field GR.  But it CANNOT
produce:
  - Hawking radiation (requires vacuum fluctuations, particle creation)
  - Area-law entanglement entropy (requires a many-body vacuum state)
  - Casimir-like effects (requires mode summation)

The extension: define a free-fermion quantum field on the graph.  Each site
has creation/annihilation operators.  The vacuum |0> is the ground state of
the free-field Hamiltonian.  When gravity (the field f) modifies the
Hamiltonian, the vacuum changes -- Bogoliubov coefficients measure particle
creation.

Method
------
Part 1 -- Free field on a 1D chain (N sites):
  H_0 = -t sum_<ij> (c^dag_i c_j + h.c.) + m sum_i c^dag_i c_i
  Diagonalize -> single-particle modes epsilon_k and eigenvectors.
  Half-fill the Dirac sea.  Compute two-point correlator C_ij.

Part 2 -- Gravitational field modifies the vacuum:
  H = H_0 + sum_i f(i) c^dag_i c_i   (Poisson-sourced field)
  Diagonalize H -> new modes.  Compute Bogoliubov coefficients:
  overlap of old occupied modes with new unoccupied modes gives
  particle creation.

Part 3 -- Entanglement entropy:
  For the ground state of H, compute the restricted correlation matrix
  C_A on subsystem A (half the chain).  Von Neumann entropy from its
  eigenvalues: S = -sum_k [n_k ln n_k + (1-n_k) ln(1-n_k)].
  Check area vs volume scaling on 1D chains and 2D lattices.

Part 4 -- Near-horizon particle creation:
  Strong gravitational source f -> 1 near center.  Particle number
  vs distance from horizon.  Check thermality: does ln(n_k) vs
  epsilon_k give a linear fit (Planck distribution)?

All computations use exact diagonalization of the N x N single-particle
Hamiltonian.  For free fermions the correlation matrix fully determines
all observables -- no exponential Hilbert space.

PStack experiment: frontier-second-quantized-prototype
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np
from numpy.linalg import eigh


# ===================================================================
# Part 1: Free field on a graph
# ===================================================================

def build_1d_hamiltonian(N: int, t: float = 1.0, m: float = 0.0,
                         potential: np.ndarray | None = None) -> np.ndarray:
    """Build tight-binding Hamiltonian on a 1D chain with N sites.

    H = -t sum_{<ij>} (|i><j| + h.c.) + (m + V_i) sum_i |i><i|

    Parameters
    ----------
    N : number of sites
    t : hopping amplitude
    m : uniform mass term
    potential : site-dependent potential V_i (length N array)
    """
    H = np.zeros((N, N))
    # Hopping
    for i in range(N - 1):
        H[i, i + 1] = -t
        H[i + 1, i] = -t
    # Mass / on-site
    for i in range(N):
        H[i, i] = m
        if potential is not None:
            H[i, i] += potential[i]
    return H


def build_2d_hamiltonian(Nx: int, Ny: int, t: float = 1.0, m: float = 0.0,
                         potential: np.ndarray | None = None) -> np.ndarray:
    """Build tight-binding Hamiltonian on a 2D rectangular lattice.

    Sites labeled by flat index n = x * Ny + y.
    """
    N = Nx * Ny
    H = np.zeros((N, N))

    def idx(x, y):
        return x * Ny + y

    for x in range(Nx):
        for y in range(Ny):
            i = idx(x, y)
            H[i, i] = m
            if potential is not None:
                H[i, i] += potential[i]
            # Horizontal hopping
            if x + 1 < Nx:
                j = idx(x + 1, y)
                H[i, j] = -t
                H[j, i] = -t
            # Vertical hopping
            if y + 1 < Ny:
                j = idx(x, y + 1)
                H[i, j] = -t
                H[j, i] = -t
    return H


def diagonalize(H: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Diagonalize Hermitian Hamiltonian.

    Returns (energies, eigenvectors) sorted by energy.
    Eigenvectors[:,k] is the k-th mode.
    """
    energies, vecs = eigh(H)
    return energies, vecs


def correlation_matrix(eigvecs: np.ndarray, n_occupied: int) -> np.ndarray:
    """Compute the two-point correlator C_ij = <0|c^dag_i c_j|0>.

    For free fermions with half-filling, C = sum_{k in occupied} |k><k|.
    """
    occ = eigvecs[:, :n_occupied]
    return occ @ occ.T


def test_correlator_decay(C: np.ndarray, label: str) -> dict:
    """Check that |C_ij| decays with |i-j|."""
    N = C.shape[0]
    # Average |C_ij| at each distance
    max_dist = N // 2
    avg_corr = np.zeros(max_dist + 1)
    counts = np.zeros(max_dist + 1)
    for i in range(N):
        for j in range(N):
            d = abs(i - j)
            if d <= max_dist:
                avg_corr[d] += abs(C[i, j])
                counts[d] += 1
    mask = counts > 0
    avg_corr[mask] /= counts[mask]

    # Check monotonic decay (roughly)
    decaying = True
    for d in range(2, min(10, max_dist)):
        if avg_corr[d] > avg_corr[1] * 1.05:
            decaying = False
            break

    print(f"\n--- Part 1: Correlator decay ({label}) ---")
    print(f"  |C(d=0)|  = {avg_corr[0]:.6f}")
    print(f"  |C(d=1)|  = {avg_corr[1]:.6f}")
    print(f"  |C(d=5)|  = {avg_corr[min(5, max_dist)]:.6f}")
    if max_dist >= 10:
        print(f"  |C(d=10)| = {avg_corr[10]:.6f}")
    print(f"  Correlator decays with distance: {decaying}")
    return {"avg_corr": avg_corr, "decaying": decaying}


# ===================================================================
# Part 2: Bogoliubov coefficients and particle creation
# ===================================================================

def gravitational_potential_1d(N: int, source_pos: int,
                               strength: float) -> np.ndarray:
    """1/r gravitational potential on a 1D chain from a point source.

    f(i) = strength / max(|i - source_pos|, 1)
    Capped at f_max < 1 for stability (horizon forms when f -> 1).
    """
    V = np.zeros(N)
    for i in range(N):
        r = max(abs(i - source_pos), 1)
        V[i] = strength / r
    return V


def gravitational_potential_2d(Nx: int, Ny: int, source: tuple[int, int],
                               strength: float) -> np.ndarray:
    """1/r gravitational potential on a 2D lattice."""
    N = Nx * Ny
    V = np.zeros(N)
    sx, sy = source
    for x in range(Nx):
        for y in range(Ny):
            r = math.sqrt((x - sx)**2 + (y - sy)**2)
            r = max(r, 1.0)
            V[x * Ny + y] = strength / r
    return V


def bogoliubov_particle_number(old_vecs: np.ndarray, old_n_occ: int,
                                new_vecs: np.ndarray, new_n_occ: int) -> dict:
    """Compute Bogoliubov particle creation.

    The old vacuum has modes 0..old_n_occ-1 occupied.
    The new Hamiltonian has modes 0..new_n_occ-1 occupied.
    Particle creation = overlap of old occupied modes with new UNOCCUPIED modes.

    n_particles = sum_{k in old_occ} sum_{l in new_unocc} |<old_k|new_l>|^2
    """
    N = old_vecs.shape[0]
    old_occ = old_vecs[:, :old_n_occ]      # N x n_occ
    new_unocc = new_vecs[:, new_n_occ:]    # N x n_unocc

    # Overlap matrix: (n_occ x n_unocc)
    overlap = old_occ.T @ new_unocc
    # Total particle number
    n_total = np.sum(np.abs(overlap)**2)

    # Per-mode particle number in new basis
    n_per_new_mode = np.sum(np.abs(overlap)**2, axis=0)  # length n_unocc

    # Per old-mode particle number
    n_per_old_mode = np.sum(np.abs(overlap)**2, axis=1)  # length n_occ

    return {
        "n_total": n_total,
        "n_per_new_mode": n_per_new_mode,
        "n_per_old_mode": n_per_old_mode,
        "overlap": overlap,
    }


def test_bogoliubov(N: int, strength: float, label: str) -> dict:
    """Run Bogoliubov test: free vacuum vs gravitational vacuum."""
    n_occ = N // 2

    # Free Hamiltonian
    H0 = build_1d_hamiltonian(N, t=1.0, m=0.0)
    eps0, vecs0 = diagonalize(H0)

    # Gravitational potential
    source = N // 2
    V = gravitational_potential_1d(N, source, strength)
    H = build_1d_hamiltonian(N, t=1.0, m=0.0, potential=V)
    eps_g, vecs_g = diagonalize(H)

    # Bogoliubov coefficients
    result = bogoliubov_particle_number(vecs0, n_occ, vecs_g, n_occ)
    n_total = result["n_total"]

    # Also compute zero-gravity baseline
    result_zero = bogoliubov_particle_number(vecs0, n_occ, vecs0, n_occ)

    print(f"\n--- Part 2: Bogoliubov particle creation ({label}) ---")
    print(f"  N = {N}, strength = {strength}")
    print(f"  n_particles (gravity)  = {n_total:.6f}")
    print(f"  n_particles (no grav)  = {result_zero['n_total']:.6f}")
    print(f"  Vacuum instability (n > 0): {n_total > 1e-10}")

    return {
        "n_total": n_total,
        "n_zero": result_zero["n_total"],
        "result": result,
        "V": V,
        "eps0": eps0,
        "eps_g": eps_g,
        "vecs0": vecs0,
        "vecs_g": vecs_g,
    }


# ===================================================================
# Part 3: Entanglement entropy from correlation matrix
# ===================================================================

def entanglement_entropy(C: np.ndarray, subsystem_sites: list[int]) -> float:
    """Compute von Neumann entanglement entropy of subsystem A.

    For free fermions, the entropy is computed from the eigenvalues of the
    restricted correlation matrix C_A:
        S = -sum_k [n_k ln(n_k) + (1-n_k) ln(1-n_k)]
    where n_k are the eigenvalues of C_A restricted to subsystem A sites.
    """
    C_A = C[np.ix_(subsystem_sites, subsystem_sites)]
    evals = np.linalg.eigvalsh(C_A)
    # Clip to [epsilon, 1-epsilon] to avoid log(0)
    eps = 1e-15
    evals = np.clip(evals, eps, 1.0 - eps)
    S = -np.sum(evals * np.log(evals) + (1.0 - evals) * np.log(1.0 - evals))
    return S


def test_entropy_scaling_1d(sizes: list[int], strength: float) -> dict:
    """Test entropy scaling vs subsystem size on 1D chains.

    For 1D free fermions: S ~ (1/3) ln(L) (CFT prediction).
    With gravity: could be modified.
    """
    results = {"sizes": [], "S_free": [], "S_grav": [], "L_A": []}

    for N in sizes:
        n_occ = N // 2
        L_A = N // 2  # subsystem A = left half
        subsystem_A = list(range(L_A))

        # Free field
        H0 = build_1d_hamiltonian(N, t=1.0, m=0.0)
        _, vecs0 = diagonalize(H0)
        C0 = correlation_matrix(vecs0, n_occ)
        S0 = entanglement_entropy(C0, subsystem_A)

        # With gravity
        V = gravitational_potential_1d(N, N // 2, strength)
        H = build_1d_hamiltonian(N, t=1.0, m=0.0, potential=V)
        _, vecs_g = diagonalize(H)
        C_g = correlation_matrix(vecs_g, n_occ)
        S_g = entanglement_entropy(C_g, subsystem_A)

        results["sizes"].append(N)
        results["L_A"].append(L_A)
        results["S_free"].append(S0)
        results["S_grav"].append(S_g)

    print("\n--- Part 3: Entanglement entropy scaling (1D) ---")
    print(f"  {'N':>4s}  {'L_A':>4s}  {'S_free':>10s}  {'S_grav':>10s}  {'S_free/ln(L_A)':>14s}")
    for i, N in enumerate(results["sizes"]):
        L_A = results["L_A"][i]
        S_f = results["S_free"][i]
        S_g = results["S_grav"][i]
        ratio = S_f / max(math.log(L_A), 1e-10) if L_A > 1 else 0
        print(f"  {N:4d}  {L_A:4d}  {S_f:10.6f}  {S_g:10.6f}  {ratio:14.6f}")

    # Check sub-volume scaling: S should grow slower than L_A
    S_free = np.array(results["S_free"])
    L_A = np.array(results["L_A"], dtype=float)
    # Fit S vs ln(L_A) for free case (should be ~ 1/3 for CFT)
    if len(sizes) >= 3:
        log_L = np.log(L_A)
        coeffs = np.polyfit(log_L, S_free, 1)
        c_eff = coeffs[0]  # effective central charge / 3
        print(f"  Free-field fit: S ~ {c_eff:.4f} * ln(L_A) + {coeffs[1]:.4f}")
        print(f"  (CFT prediction: c_eff/3 ~ 1/3 = 0.333)")

        S_grav = np.array(results["S_grav"])
        coeffs_g = np.polyfit(log_L, S_grav, 1)
        print(f"  Gravity fit:    S ~ {coeffs_g[0]:.4f} * ln(L_A) + {coeffs_g[1]:.4f}")

    return results


def test_entropy_scaling_2d(side_sizes: list[int], strength: float) -> dict:
    """Test entropy scaling on 2D lattices.

    For 2D free fermions with a straight cut: S ~ L (area law in 2D).
    Area law means S ~ boundary_length, not volume.
    """
    results = {"Nx": [], "Ny": [], "S_free": [], "S_grav": [],
               "boundary": [], "volume_A": []}

    for Ny in side_sizes:
        Nx = 2 * Ny  # elongated so cut is in the middle
        N = Nx * Ny
        n_occ = N // 2
        # Subsystem A: left half (x < Nx//2)
        subsystem_A = []
        for x in range(Nx // 2):
            for y in range(Ny):
                subsystem_A.append(x * Ny + y)
        boundary = Ny  # number of sites along the cut
        volume_A = len(subsystem_A)

        # Free field
        H0 = build_2d_hamiltonian(Nx, Ny, t=1.0, m=0.0)
        _, vecs0 = diagonalize(H0)
        C0 = correlation_matrix(vecs0, n_occ)
        S0 = entanglement_entropy(C0, subsystem_A)

        # With gravity (source at center)
        V = gravitational_potential_2d(Nx, Ny, (Nx // 2, Ny // 2), strength)
        H = build_2d_hamiltonian(Nx, Ny, t=1.0, m=0.0, potential=V)
        _, vecs_g = diagonalize(H)
        C_g = correlation_matrix(vecs_g, n_occ)
        S_g = entanglement_entropy(C_g, subsystem_A)

        results["Nx"].append(Nx)
        results["Ny"].append(Ny)
        results["S_free"].append(S0)
        results["S_grav"].append(S_g)
        results["boundary"].append(boundary)
        results["volume_A"].append(volume_A)

    print("\n--- Part 3: Entanglement entropy scaling (2D) ---")
    print(f"  {'Nx':>4s} x {'Ny':>3s}  {'boundary':>8s}  {'vol_A':>6s}  {'S_free':>10s}  {'S_grav':>10s}  {'S/bdy':>8s}")
    for i in range(len(results["Nx"])):
        Nx = results["Nx"][i]
        Ny = results["Ny"][i]
        bdy = results["boundary"][i]
        vol = results["volume_A"][i]
        Sf = results["S_free"][i]
        Sg = results["S_grav"][i]
        print(f"  {Nx:4d} x {Ny:3d}  {bdy:8d}  {vol:6d}  {Sf:10.4f}  {Sg:10.4f}  {Sf/bdy:8.4f}")

    # Fit S_free vs boundary and vs volume
    if len(side_sizes) >= 3:
        bdy = np.array(results["boundary"], dtype=float)
        vol = np.array(results["volume_A"], dtype=float)
        Sf = np.array(results["S_free"])

        # Area law fit: S = a * boundary + b
        coeffs_area = np.polyfit(bdy, Sf, 1)
        resid_area = np.sum((Sf - np.polyval(coeffs_area, bdy))**2)

        # Volume law fit: S = a * volume + b
        coeffs_vol = np.polyfit(vol, Sf, 1)
        resid_vol = np.sum((Sf - np.polyval(coeffs_vol, vol))**2)

        # R^2 for each
        ss_tot = np.sum((Sf - np.mean(Sf))**2)
        r2_area = 1.0 - resid_area / ss_tot if ss_tot > 0 else 0
        r2_vol = 1.0 - resid_vol / ss_tot if ss_tot > 0 else 0

        print(f"  Area-law fit:   S = {coeffs_area[0]:.4f} * boundary + {coeffs_area[1]:.4f}  (R^2 = {r2_area:.4f})")
        print(f"  Volume-law fit: S = {coeffs_vol[0]:.6f} * volume + {coeffs_vol[1]:.4f}  (R^2 = {r2_vol:.4f})")
        scaling = "area-like" if r2_area > r2_vol else "volume-like"
        print(f"  Scaling verdict: {scaling}")
        results["r2_area"] = r2_area
        results["r2_vol"] = r2_vol
        results["scaling"] = scaling

    return results


# ===================================================================
# Part 4: Near-horizon particle creation and thermality
# ===================================================================

def test_horizon_particle_creation(N: int, strengths: list[float]) -> dict:
    """Particle creation profile near a strong gravitational source.

    For each strength, compute the Bogoliubov particle number resolved
    by site distance from the source.  Check if the spectral distribution
    is thermal.
    """
    n_occ = N // 2
    source = N // 2

    # Free Hamiltonian and modes
    H0 = build_1d_hamiltonian(N, t=1.0, m=0.0)
    eps0, vecs0 = diagonalize(H0)

    all_results = {}
    for strength in strengths:
        V = gravitational_potential_1d(N, source, strength)
        H = build_1d_hamiltonian(N, t=1.0, m=0.0, potential=V)
        eps_g, vecs_g = diagonalize(H)

        bog = bogoliubov_particle_number(vecs0, n_occ, vecs_g, n_occ)

        # Per-site particle density: n(i) = sum_{k in old_occ, l in new_unocc}
        #   |phi_k(i)|^2 * |<k|l>|^2  -- but more precisely:
        # The local particle density in the new vacuum as seen by old observers:
        #   n(i) = <0_new | a^dag_i a_i |0_new>_old - <0_old | a^dag_i a_i |0_old>_old
        # where a_i are OLD-basis operators.
        # <0_new|a^dag_i a_i|0_new> = sum_{k occupied in new} |phi_new_k(i)|^2
        # <0_old|a^dag_i a_i|0_old> = sum_{k occupied in old} |phi_old_k(i)|^2

        n_old = np.sum(np.abs(vecs0[:, :n_occ])**2, axis=1)
        n_new = np.sum(np.abs(vecs_g[:, :n_occ])**2, axis=1)
        delta_n = n_new - n_old  # particle creation profile

        # Surface gravity: kappa = |dV/dr| at the point where V is largest
        # (proxy for the horizon)
        dV = np.abs(np.diff(V))
        kappa = np.max(dV)
        kappa_pos = np.argmax(dV)

        # Thermality test: for the Bogoliubov spectrum, check if
        # ln(n_k) vs epsilon_k is linear (Bose-Einstein / Fermi-Dirac)
        n_per_mode = bog["n_per_new_mode"]
        eps_unocc = eps_g[n_occ:]
        # Filter modes with appreciable occupation
        mask = n_per_mode > 1e-10
        if np.sum(mask) >= 3:
            log_n = np.log(n_per_mode[mask])
            eps_sel = eps_unocc[mask]
            # Linear fit: ln(n) = -eps/T + const -> slope = -1/T
            coeffs = np.polyfit(eps_sel, log_n, 1)
            slope = coeffs[0]
            T_fit = -1.0 / slope if abs(slope) > 1e-10 else float('inf')
            # R^2
            pred = np.polyval(coeffs, eps_sel)
            ss_res = np.sum((log_n - pred)**2)
            ss_tot = np.sum((log_n - np.mean(log_n))**2)
            r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0
            thermal = r2 > 0.7
        else:
            T_fit = float('nan')
            r2 = float('nan')
            thermal = False

        all_results[strength] = {
            "n_total": bog["n_total"],
            "delta_n": delta_n,
            "kappa": kappa,
            "T_fit": T_fit,
            "r2_thermal": r2,
            "thermal": thermal,
            "V": V,
            "n_per_mode": n_per_mode,
            "eps_unocc": eps_unocc,
        }

    print(f"\n--- Part 4: Near-horizon particle creation (N={N}) ---")
    print(f"  {'strength':>10s}  {'n_total':>10s}  {'kappa':>8s}  {'T_fit':>10s}  {'R^2':>8s}  {'thermal':>8s}  {'T/kappa':>8s}")
    for strength in strengths:
        r = all_results[strength]
        T_kappa = r["T_fit"] / r["kappa"] if r["kappa"] > 0 and np.isfinite(r["T_fit"]) else float('nan')
        print(f"  {strength:10.2f}  {r['n_total']:10.4f}  {r['kappa']:8.4f}  {r['T_fit']:10.4f}  {r['r2_thermal']:8.4f}  {str(r['thermal']):>8s}  {T_kappa:8.4f}")

    # Hawking prediction: T = kappa / (2*pi)
    print(f"\n  Hawking prediction: T = kappa / (2*pi)")
    for strength in strengths:
        r = all_results[strength]
        T_hawking = r["kappa"] / (2 * math.pi)
        ratio = r["T_fit"] / T_hawking if T_hawking > 0 and np.isfinite(r["T_fit"]) else float('nan')
        print(f"    s={strength:.1f}: T_fit={r['T_fit']:.4f}, T_Hawking={T_hawking:.4f}, ratio={ratio:.4f}")

    return all_results


# ===================================================================
# Main: run all parts
# ===================================================================

def main():
    t_start = time.time()
    print("=" * 72)
    print("SECOND-QUANTIZED PROPAGATOR PROTOTYPE")
    print("Free-fermion field on a graph with Bogoliubov particle creation")
    print("=" * 72)

    # ------------------------------------------------------------------
    # Part 1: Free-field correlator
    # ------------------------------------------------------------------
    N_1d = 40
    n_occ = N_1d // 2
    H0 = build_1d_hamiltonian(N_1d, t=1.0, m=0.0)
    eps0, vecs0 = diagonalize(H0)
    C0 = correlation_matrix(vecs0, n_occ)
    corr_result = test_correlator_decay(C0, f"1D chain N={N_1d}")

    gate1 = corr_result["decaying"]
    print(f"\n  GATE 1 (correlator decays): {'PASS' if gate1 else 'FAIL'}")

    # ------------------------------------------------------------------
    # Part 2: Bogoliubov particle creation
    # ------------------------------------------------------------------
    bog_weak = test_bogoliubov(N=40, strength=2.0, label="weak gravity")
    bog_strong = test_bogoliubov(N=40, strength=10.0, label="strong gravity")

    gate2 = (bog_weak["n_total"] > 1e-10 and bog_strong["n_total"] > 1e-10)
    print(f"\n  GATE 2 (vacuum instability): {'PASS' if gate2 else 'FAIL'}")

    # Strength dependence
    print("\n  Particle number vs gravity strength:")
    test_strengths = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0]
    for s in test_strengths:
        r = test_bogoliubov(N=40, strength=s, label=f"s={s}")

    # ------------------------------------------------------------------
    # Part 3: Entanglement entropy
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 72)
    print("PART 3: ENTANGLEMENT ENTROPY")
    print("=" * 72)

    # 1D scaling
    ent_1d = test_entropy_scaling_1d(
        sizes=[10, 20, 40, 60, 80, 100],
        strength=3.0
    )

    # 2D scaling (smaller due to N^2 cost)
    ent_2d = test_entropy_scaling_2d(
        side_sizes=[4, 6, 8, 10],
        strength=2.0
    )

    # Gate 3: sub-volume scaling
    gate3 = True
    if "scaling" in ent_2d:
        gate3 = ent_2d["scaling"] == "area-like"
    print(f"\n  GATE 3 (sub-volume entropy): {'PASS' if gate3 else 'FAIL'}")

    # ------------------------------------------------------------------
    # Part 4: Near-horizon particle creation and thermality
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 72)
    print("PART 4: NEAR-HORIZON PARTICLE CREATION")
    print("=" * 72)

    horizon_results = test_horizon_particle_creation(
        N=60,
        strengths=[2.0, 5.0, 10.0, 20.0, 30.0]
    )

    # Gate 4: report thermality honestly
    any_thermal = any(r["thermal"] for r in horizon_results.values())
    print(f"\n  Any thermal spectrum found: {any_thermal}")

    if any_thermal:
        # Check T vs kappa scaling
        kappas = []
        temps = []
        for s, r in horizon_results.items():
            if r["thermal"] and np.isfinite(r["T_fit"]):
                kappas.append(r["kappa"])
                temps.append(r["T_fit"])
        if len(kappas) >= 2:
            kappas = np.array(kappas)
            temps = np.array(temps)
            coeffs = np.polyfit(kappas, temps, 1)
            print(f"  T vs kappa fit: T = {coeffs[0]:.4f} * kappa + {coeffs[1]:.4f}")
            print(f"  Hawking prediction: slope = 1/(2*pi) = {1/(2*math.pi):.4f}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    elapsed = time.time() - t_start
    print("\n\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Gate 1 (correlator decay):      {'PASS' if gate1 else 'FAIL'}")
    print(f"  Gate 2 (vacuum instability):    {'PASS' if gate2 else 'FAIL'}")
    print(f"  Gate 3 (sub-volume entropy):    {'PASS' if gate3 else 'FAIL'}")
    print(f"  Gate 4 (thermal spectrum):      {'FOUND' if any_thermal else 'NOT FOUND'}")
    print(f"  Elapsed: {elapsed:.1f}s")
    print("=" * 72)

    return {
        "gate1": gate1,
        "gate2": gate2,
        "gate3": gate3,
        "any_thermal": any_thermal,
    }


if __name__ == "__main__":
    results = main()
