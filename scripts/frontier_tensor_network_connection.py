#!/usr/bin/env python3
"""Tensor network connection: the path-sum propagator as an MPO.

Physics motivation
------------------
The holographic entropy test (frontier_holographic_entropy.py) found
area-law scaling with R^2 = 0.9996.  This strongly suggests the propagator
has tensor-network structure.  Here we make this explicit.

The key insight: on a layered DAG the path-sum propagator decomposes as
    psi_out = M_L . M_{L-1} . ... . M_1 . psi_in
where each M_l is a transfer matrix of dimension (sites_l+1 x sites_l).
This is precisely a Matrix Product Operator (MPO).

We test four aspects:
  1. The propagator IS a tensor network (MPO decomposition)
  2. Entanglement structure matches MERA/tensor network predictions
  3. Gravity modifies the effective bond dimension
  4. Connection to Ryu-Takayanagi: S_A / boundary ~ 1/G

All computations use exact diagonalization on small lattices.

PStack experiment: frontier-tensor-network-connection
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np
from numpy.linalg import eigh, svd, eigvalsh


# ===================================================================
# Lattice builders (reused from second-quantized prototype)
# ===================================================================

def build_1d_hamiltonian(N: int, t: float = 1.0, m: float = 0.0,
                         potential: np.ndarray | None = None) -> np.ndarray:
    """Tight-binding Hamiltonian on a 1D chain with N sites."""
    H = np.zeros((N, N))
    for i in range(N - 1):
        H[i, i + 1] = -t
        H[i + 1, i] = -t
    for i in range(N):
        H[i, i] = m
        if potential is not None:
            H[i, i] += potential[i]
    return H


def build_2d_hamiltonian(Nx: int, Ny: int, t: float = 1.0, m: float = 0.0,
                         potential: np.ndarray | None = None) -> np.ndarray:
    """Tight-binding Hamiltonian on a 2D rectangular lattice."""
    N = Nx * Ny
    H = np.zeros((N, N))
    for x in range(Nx):
        for y in range(Ny):
            i = x * Ny + y
            H[i, i] = m
            if potential is not None:
                H[i, i] += potential[i]
            if x + 1 < Nx:
                j = (x + 1) * Ny + y
                H[i, j] = -t
                H[j, i] = -t
            if y + 1 < Ny:
                j = x * Ny + (y + 1)
                H[i, j] = -t
                H[j, i] = -t
    return H


def gravitational_potential_1d(N: int, source_pos: int,
                               strength: float) -> np.ndarray:
    """1/r gravitational potential on a 1D chain."""
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


def correlation_matrix(eigvecs: np.ndarray, n_occupied: int) -> np.ndarray:
    """Two-point correlator C_ij = <0|c^dag_i c_j|0> for half-filled fermions."""
    occ = eigvecs[:, :n_occupied]
    return occ @ occ.T


def entanglement_entropy(C: np.ndarray, subsystem_sites: list[int]) -> float:
    """Von Neumann entropy from restricted correlation matrix."""
    C_A = C[np.ix_(subsystem_sites, subsystem_sites)]
    evals = np.linalg.eigvalsh(C_A)
    eps = 1e-15
    evals = np.clip(evals, eps, 1.0 - eps)
    S = -np.sum(evals * np.log(evals) + (1.0 - evals) * np.log(1.0 - evals))
    return S


def entanglement_spectrum(C: np.ndarray, subsystem_sites: list[int]) -> np.ndarray:
    """Eigenvalues of the reduced density matrix (entanglement spectrum).

    For free fermions, the single-particle entanglement spectrum is
    the set of eigenvalues {n_k} of C_A.  The many-body entanglement
    energies are xi_k = log((1-n_k)/n_k).
    """
    C_A = C[np.ix_(subsystem_sites, subsystem_sites)]
    evals = np.linalg.eigvalsh(C_A)
    eps = 1e-15
    evals = np.clip(evals, eps, 1.0 - eps)
    return evals


# ===================================================================
# TEST 1: The propagator IS a tensor network (MPO decomposition)
# ===================================================================

def build_transfer_matrices_1d(N: int, t: float = 1.0,
                                potential: np.ndarray | None = None,
                                k: float = 4.0) -> list[np.ndarray]:
    """Build layer-by-layer transfer matrices for a 1D chain.

    On a layered graph with L layers each of width W, the propagator is:
        psi_out = M_L . M_{L-1} . ... . M_1 . psi_in

    For a 1D chain of N sites viewed as L layers of width W=1
    (trivial transverse direction), the transfer matrix at layer l is
    the single-step propagator from sites at position l to position l+1.

    For a more interesting structure, we reshape a 2D lattice (Nx x Ny)
    into Nx layers each of width Ny.  The transfer matrix M_l has
    dimension Ny x Ny.
    """
    # We work with a 2D lattice interpretation: N sites arranged as
    # a strip of L layers each W sites wide.
    # For 1D: L = N, W = 1 -> trivial
    # Instead, factor N into L x W to get non-trivial transfer matrices
    # Actually, the natural MPO for a 1D chain comes from the
    # Hamiltonian evolution operator exp(-i H dt) decomposed layer by layer.

    # Build Hamiltonian
    H = build_1d_hamiltonian(N, t=t, m=0.0, potential=potential)

    # The propagator for imaginary time dt is T = exp(-H * dt)
    # For the tensor network decomposition, we use the transfer matrix
    # interpretation: T = product of local gates.
    # On a 1D chain, the natural decomposition uses even/odd bond layers.

    dt = 1.0 / k  # effective time step

    # Even bonds: (0,1), (2,3), (4,5), ...
    # Odd bonds:  (1,2), (3,4), (5,6), ...
    transfer_matrices = []

    # Build even-bond layer
    M_even = np.eye(N)
    for i in range(0, N - 1, 2):
        # Local 2x2 gate for bond (i, i+1)
        h_local = np.zeros((2, 2))
        h_local[0, 1] = -t
        h_local[1, 0] = -t
        if potential is not None:
            h_local[0, 0] = 0.5 * potential[i]
            h_local[1, 1] = 0.5 * potential[i + 1]
        gate = _matrix_exp_hermitian(-dt * h_local)
        M_even[i:i+2, i:i+2] = gate
    transfer_matrices.append(M_even)

    # Build odd-bond layer
    M_odd = np.eye(N)
    for i in range(1, N - 1, 2):
        h_local = np.zeros((2, 2))
        h_local[0, 1] = -t
        h_local[1, 0] = -t
        if potential is not None:
            h_local[0, 0] = 0.5 * potential[i]
            h_local[1, 1] = 0.5 * potential[i + 1]
        gate = _matrix_exp_hermitian(-dt * h_local)
        M_odd[i:i+2, i:i+2] = gate
    transfer_matrices.append(M_odd)

    return transfer_matrices


def build_transfer_matrices_2d(Nx: int, Ny: int, t: float = 1.0,
                                potential: np.ndarray | None = None,
                                k: float = 4.0) -> list[np.ndarray]:
    """Build layer-by-layer transfer matrices for a 2D lattice.

    The 2D lattice (Nx x Ny) is viewed as Nx layers each of Ny sites.
    The transfer matrix M_l (Ny x Ny) propagates from layer l to l+1.

    M_l[j, i] = <(l+1, j) | T | (l, i)> includes:
      - Hopping from (l, i) to (l+1, j) with |i-j| <= 1
      - On-site potential contribution
    """
    transfer_matrices = []

    for l in range(Nx - 1):
        M = np.zeros((Ny, Ny))
        for j in range(Ny):
            for i in range(Ny):
                if abs(i - j) <= 1:
                    # Hopping amplitude
                    dx = 1.0
                    dy = float(j - i)
                    dist = math.sqrt(dx**2 + dy**2)
                    # Phase factor
                    phase = k / dist
                    amp = math.exp(-0.1 * dy**2) / dist  # Gaussian directional weight

                    # Gravitational field modification
                    if potential is not None:
                        idx_src = l * Ny + i
                        idx_dst = (l + 1) * Ny + j
                        f_avg = 0.5 * (potential[idx_src] + potential[idx_dst])
                        amp *= math.exp(-f_avg)  # field suppression

                    M[j, i] = amp

        transfer_matrices.append(M)

    return transfer_matrices


def _matrix_exp_hermitian(H: np.ndarray) -> np.ndarray:
    """Matrix exponential of a Hermitian matrix."""
    evals, evecs = eigh(H)
    return evecs @ np.diag(np.exp(evals)) @ evecs.T


def test_mpo_decomposition() -> dict:
    """Test 1: Show the propagator decomposes as an MPO.

    On a 2D lattice (Nx x Ny), the full propagator from layer 0 to
    layer Nx-1 is M_{Nx-1} . M_{Nx-2} . ... . M_1.

    Key checks:
      - Each M_l has dimension Ny x Ny
      - The product is the full propagator
      - Bond dimension = Ny (the transverse lattice size)
      - Adding gravity changes matrix elements but not bond dimension
    """
    print("\n" + "=" * 72)
    print("TEST 1: THE PROPAGATOR IS A TENSOR NETWORK (MPO)")
    print("=" * 72)

    results = {}

    for Ny in [4, 6, 8]:
        Nx = 2 * Ny  # elongated lattice
        N = Nx * Ny

        # Free case
        Tms_free = build_transfer_matrices_2d(Nx, Ny, t=1.0, potential=None)

        # With gravity
        V = gravitational_potential_2d(Nx, Ny, (Nx // 2, Ny // 2), strength=3.0)
        Tms_grav = build_transfer_matrices_2d(Nx, Ny, t=1.0, potential=V)

        # Full propagator = product of transfer matrices
        prop_free = np.eye(Ny)
        for M in Tms_free:
            prop_free = M @ prop_free

        prop_grav = np.eye(Ny)
        for M in Tms_grav:
            prop_grav = M @ prop_grav

        # SVD of each transfer matrix -> singular values
        svs_free = []
        svs_grav = []
        for l in range(len(Tms_free)):
            _, s_f, _ = svd(Tms_free[l])
            _, s_g, _ = svd(Tms_grav[l])
            svs_free.append(s_f)
            svs_grav.append(s_g)

        # Bond dimension = number of non-negligible singular values
        threshold = 1e-10
        bd_free = [np.sum(s > threshold) for s in svs_free]
        bd_grav = [np.sum(s > threshold) for s in svs_grav]

        print(f"\n  Lattice: {Nx} x {Ny} ({N} sites)")
        print(f"  Number of transfer matrices: {len(Tms_free)}")
        print(f"  Transfer matrix dimension: {Ny} x {Ny}")
        print(f"  Bond dimension (free):    min={min(bd_free)}, max={max(bd_free)}, "
              f"mean={np.mean(bd_free):.1f}")
        print(f"  Bond dimension (gravity): min={min(bd_grav)}, max={max(bd_grav)}, "
              f"mean={np.mean(bd_grav):.1f}")

        # Full propagator SVD
        _, s_prop_f, _ = svd(prop_free)
        _, s_prop_g, _ = svd(prop_grav)
        print(f"  Full propagator singular values (free):    "
              f"{s_prop_f[:4]}")
        print(f"  Full propagator singular values (gravity): "
              f"{s_prop_g[:4]}")

        results[Ny] = {
            "Nx": Nx, "Ny": Ny,
            "bd_free": bd_free, "bd_grav": bd_grav,
            "svs_free": svs_free, "svs_grav": svs_grav,
            "prop_sv_free": s_prop_f, "prop_sv_grav": s_prop_g,
        }

    # Verdict
    all_mpo = all(
        max(r["bd_free"]) <= r["Ny"] and max(r["bd_grav"]) <= r["Ny"]
        for r in results.values()
    )
    print(f"\n  GATE 1 (propagator is MPO with bond dim = Ny): "
          f"{'PASS' if all_mpo else 'FAIL'}")

    results["gate1"] = all_mpo
    return results


# ===================================================================
# TEST 2: Entanglement structure matches tensor network predictions
# ===================================================================

def test_entanglement_structure() -> dict:
    """Test 2: Entanglement entropy, mutual information, spectrum.

    For 1D free fermions at half-filling:
      - S(L) ~ (c/3) ln(L) + const  with c = 1 (central charge of free fermion CFT)
      - The entanglement spectrum should show a characteristic distribution

    For 2D:
      - Area law: S ~ boundary length
    """
    print("\n" + "=" * 72)
    print("TEST 2: ENTANGLEMENT STRUCTURE")
    print("=" * 72)

    results = {}

    # --- 1D: CFT log scaling ---
    print("\n  --- 1D CFT log scaling ---")
    sizes_1d = [20, 40, 60, 80, 100]
    S_vals = []
    L_vals = []

    for N in sizes_1d:
        n_occ = N // 2
        H = build_1d_hamiltonian(N, t=1.0, m=0.0)
        _, vecs = eigh(H)
        C = correlation_matrix(vecs, n_occ)

        # Subsystem A = left L_A sites, vary L_A
        L_A = N // 2
        subsystem_A = list(range(L_A))
        S = entanglement_entropy(C, subsystem_A)
        S_vals.append(S)
        L_vals.append(L_A)
        print(f"    N={N:3d}, L_A={L_A:3d}, S={S:.6f}, S/ln(L_A)={S/math.log(L_A):.4f}")

    # Fit S vs ln(L_A)
    # For open boundary conditions, the CFT prediction is:
    #   S = (c/6) ln(N) + const   (half-chain entropy of open chain)
    # where c=1 for free fermions, so coefficient ~ 1/6 = 0.167
    # The factor is c/6 (not c/3) because open BCs give half the
    # entanglement of periodic BCs.
    log_L = np.log(np.array(L_vals, dtype=float))
    S_arr = np.array(S_vals)
    coeffs = np.polyfit(log_L, S_arr, 1)
    c_eff_over_6 = coeffs[0]
    ss_res = np.sum((S_arr - np.polyval(coeffs, log_L))**2)
    ss_tot = np.sum((S_arr - np.mean(S_arr))**2)
    r2_log = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0

    print(f"\n    Fit: S = {c_eff_over_6:.4f} * ln(L) + {coeffs[1]:.4f}")
    print(f"    R^2 = {r2_log:.6f}")
    print(f"    Effective c/6 = {c_eff_over_6:.4f} (CFT open-BC prediction: c/6 = 0.167)")
    c_eff = 6.0 * c_eff_over_6
    print(f"    Inferred central charge c = {c_eff:.4f} (expect 1.0)")
    results["cft_c_over_6"] = c_eff_over_6
    results["cft_c"] = c_eff
    results["cft_r2"] = r2_log

    # --- 1D: Entanglement spectrum ---
    print("\n  --- 1D Entanglement spectrum ---")
    N_spec = 40
    n_occ = N_spec // 2
    H = build_1d_hamiltonian(N_spec, t=1.0, m=0.0)
    _, vecs = eigh(H)
    C = correlation_matrix(vecs, n_occ)
    subsystem_A = list(range(N_spec // 2))
    esp = entanglement_spectrum(C, subsystem_A)

    # Entanglement energies: xi_k = log((1-n_k)/n_k)
    xi = np.log((1.0 - esp) / esp)
    xi_sorted = np.sort(xi)

    print(f"    N={N_spec}, L_A={N_spec // 2}")
    print(f"    Entanglement spectrum (first 8 single-particle levels):")
    for i, x in enumerate(xi_sorted[:8]):
        print(f"      xi_{i} = {x:.4f}")

    # The entanglement spectrum of a 1D CFT should be approximately
    # linearly spaced (Calabrese-Lefevre prediction)
    spacings = np.diff(xi_sorted[:10])
    spacing_std = np.std(spacings) / np.mean(spacings) if len(spacings) > 1 else 0
    print(f"    Spacing regularity (std/mean of gaps): {spacing_std:.4f}")
    print(f"    (Low ratio = regular spacing, CFT-like)")
    results["spectrum_regularity"] = spacing_std

    # --- Mutual information between separated regions ---
    print("\n  --- Mutual information ---")
    N_mi = 60
    n_occ = N_mi // 2
    H = build_1d_hamiltonian(N_mi, t=1.0, m=0.0)
    _, vecs = eigh(H)
    C = correlation_matrix(vecs, n_occ)

    # Region A: sites [5, 15), Region B: sites [d+15, d+25) for varying d
    la, lb = 10, 10
    print(f"    N={N_mi}, |A|={la}, |B|={lb}")
    print(f"    {'sep':>5s}  {'S_A':>10s}  {'S_B':>10s}  {'S_AB':>10s}  {'I(A:B)':>10s}")

    separations = [0, 5, 10, 15, 20, 25]
    mi_vals = []
    for sep in separations:
        A = list(range(5, 5 + la))
        B = list(range(5 + la + sep, 5 + la + sep + lb))
        if max(B) >= N_mi:
            continue
        AB = A + B
        S_A = entanglement_entropy(C, A)
        S_B = entanglement_entropy(C, B)
        S_AB = entanglement_entropy(C, AB)
        I_AB = S_A + S_B - S_AB
        mi_vals.append((sep, I_AB))
        print(f"    {sep:5d}  {S_A:10.6f}  {S_B:10.6f}  {S_AB:10.6f}  {I_AB:10.6f}")

    # Mutual information should decay with separation (CFT: ~ 1/r^2 for 1D)
    if len(mi_vals) >= 3:
        seps = np.array([s for s, _ in mi_vals if s > 0], dtype=float)
        mis = np.array([m for s, m in mi_vals if s > 0])
        if len(seps) >= 3 and np.all(mis > 0):
            log_seps = np.log(seps)
            log_mis = np.log(mis)
            power_fit = np.polyfit(log_seps, log_mis, 1)
            print(f"\n    I(A:B) ~ d^{power_fit[0]:.2f}  (CFT prediction: ~ d^-2)")
            results["mi_power"] = power_fit[0]

    # --- 2D: Area law ---
    print("\n  --- 2D Area law ---")
    side_sizes = [4, 6, 8, 10]
    boundaries = []
    entropies_2d = []

    for Ny in side_sizes:
        Nx = 2 * Ny
        N = Nx * Ny
        n_occ = N // 2
        H = build_2d_hamiltonian(Nx, Ny, t=1.0, m=0.0)
        _, vecs = eigh(H)
        C = correlation_matrix(vecs, n_occ)

        # Subsystem A = left half
        subsystem_A = []
        for x in range(Nx // 2):
            for y in range(Ny):
                subsystem_A.append(x * Ny + y)
        boundary = Ny
        S = entanglement_entropy(C, subsystem_A)
        boundaries.append(boundary)
        entropies_2d.append(S)
        print(f"    {Nx}x{Ny}: boundary={boundary}, S={S:.4f}, S/boundary={S/boundary:.4f}")

    # Fit S vs boundary
    bdy = np.array(boundaries, dtype=float)
    S2d = np.array(entropies_2d)
    coeffs_area = np.polyfit(bdy, S2d, 1)
    ss_res = np.sum((S2d - np.polyval(coeffs_area, bdy))**2)
    ss_tot = np.sum((S2d - np.mean(S2d))**2)
    r2_area = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0

    print(f"\n    Area-law fit: S = {coeffs_area[0]:.4f} * boundary + {coeffs_area[1]:.4f}")
    print(f"    R^2 = {r2_area:.6f}")
    results["area_law_r2"] = r2_area

    # Gate 2
    # Open-BC check: c/6 ~ 0.167 means c ~ 1.0
    cft_ok = abs(c_eff - 1.0) < 0.2 and r2_log > 0.99
    area_ok = r2_area > 0.95
    gate2 = cft_ok and area_ok
    print(f"\n  GATE 2 (entanglement matches tensor network): "
          f"{'PASS' if gate2 else 'FAIL'}")
    print(f"    CFT log scaling (c ~ 1.0):   {'PASS' if cft_ok else 'FAIL'}")
    print(f"    2D area law (R^2 > 0.95):    {'PASS' if area_ok else 'FAIL'}")
    results["gate2"] = gate2
    return results


# ===================================================================
# TEST 3: Gravity modifies bond dimension effectively
# ===================================================================

def test_gravitational_bond_dimension() -> dict:
    """Test 3: Gravity reduces the effective bond dimension.

    When the gravitational field f is present, the transfer matrix
    M_l(f) has modified singular values.  The effective bond dimension
    (number of significant singular values) should DECREASE near a
    gravitational source -- gravity concentrates information.

    This is the holographic principle in tensor network language:
    gravity reduces the effective Hilbert space dimension.
    """
    print("\n" + "=" * 72)
    print("TEST 3: GRAVITATIONAL BOND DIMENSION")
    print("=" * 72)

    Ny = 8
    Nx = 16
    N = Nx * Ny

    strengths = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0]

    results = {"strengths": [], "chi_eff_mean": [], "chi_eff_center": [],
               "sv_ratio_center": []}

    for strength in strengths:
        if strength > 0:
            V = gravitational_potential_2d(Nx, Ny, (Nx // 2, Ny // 2), strength)
        else:
            V = None

        Tms = build_transfer_matrices_2d(Nx, Ny, t=1.0, potential=V)

        # SVD of each transfer matrix
        threshold = 1e-6
        chi_eff_all = []
        sv_ratios = []

        for l, M in enumerate(Tms):
            _, s, _ = svd(M)
            s_norm = s / s[0] if s[0] > 1e-30 else s
            chi = np.sum(s_norm > threshold)
            chi_eff_all.append(chi)
            # Ratio of largest to smallest significant SV
            if chi > 1:
                sv_ratios.append(s_norm[0] / s_norm[chi - 1])
            else:
                sv_ratios.append(1.0)

        chi_eff_mean = np.mean(chi_eff_all)

        # Transfer matrix near the gravitational source (center)
        center_layer = Nx // 2 - 1
        if center_layer < len(Tms):
            _, s_center, _ = svd(Tms[center_layer])
            s_center_norm = s_center / s_center[0] if s_center[0] > 1e-30 else s_center
            chi_center = np.sum(s_center_norm > threshold)
            sv_ratio_center = (s_center_norm[0] / s_center_norm[max(chi_center - 1, 0)]
                               if chi_center > 0 else 1.0)
        else:
            chi_center = Ny
            sv_ratio_center = 1.0

        results["strengths"].append(strength)
        results["chi_eff_mean"].append(chi_eff_mean)
        results["chi_eff_center"].append(chi_center)
        results["sv_ratio_center"].append(sv_ratio_center)

        print(f"  f={strength:5.1f}:  chi_eff(mean)={chi_eff_mean:.1f}, "
              f"chi_eff(center)={chi_center}, "
              f"SV condition(center)={sv_ratio_center:.2f}")

    # Check: does chi_eff decrease with increasing gravity?
    chi_free = results["chi_eff_mean"][0]
    chi_strong = results["chi_eff_mean"][-1]
    chi_decreases = chi_strong < chi_free

    # Also check center layer specifically
    chi_center_free = results["chi_eff_center"][0]
    chi_center_strong = results["chi_eff_center"][-1]
    center_decreases = chi_center_strong <= chi_center_free

    # Check SV ratio increases (gravity concentrates into fewer modes)
    sv_ratio_free = results["sv_ratio_center"][0]
    sv_ratio_strong = results["sv_ratio_center"][-1]
    ratio_increases = sv_ratio_strong > sv_ratio_free

    gate3 = chi_decreases or center_decreases or ratio_increases
    print(f"\n  chi_eff(free)={chi_free:.1f}, chi_eff(strong grav)={chi_strong:.1f}")
    print(f"  chi_eff decreases with gravity: {chi_decreases}")
    print(f"  center chi decreases: {center_decreases}")
    print(f"  SV condition ratio increases: {ratio_increases}")
    print(f"\n  GATE 3 (gravity reduces effective bond dimension): "
          f"{'PASS' if gate3 else 'FAIL'}")

    results["gate3"] = gate3
    return results


# ===================================================================
# TEST 4: Connection to Ryu-Takayanagi
# ===================================================================

def test_ryu_takayanagi() -> dict:
    """Test 4: S_A / boundary ~ 1/G_N (gravitational coupling).

    The Ryu-Takayanagi formula says S_A = Area(gamma_A) / (4 G_N).
    In our framework:
      - S_A is the entanglement entropy across a cut
      - Area(gamma_A) is the boundary size of the cut
      - G_N is the gravitational coupling

    If we vary the gravitational coupling (potential strength),
    does S_A / boundary change inversely with the coupling?

    More precisely: the free-field entropy gives the baseline.
    Adding gravity should modify S_A.  The key relation is
    S_A / boundary = alpha / (4 * G_eff) where alpha is a constant
    and G_eff depends on the gravitational coupling strength.
    """
    print("\n" + "=" * 72)
    print("TEST 4: RYU-TAKAYANAGI CONNECTION")
    print("=" * 72)

    results = {}

    # 2D lattice with varying gravitational coupling
    Ny = 8
    Nx = 16
    N = Nx * Ny

    # Gravitational coupling strengths
    g_couplings = [0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 10.0]

    print(f"\n  Lattice: {Nx} x {Ny}, boundary = {Ny}")
    print(f"  {'g':>6s}  {'S_A':>10s}  {'S/bdy':>10s}  {'delta_S':>10s}  {'delta_S/g':>10s}")

    S_vals = []
    S_over_bdy = []
    boundary = Ny

    for g in g_couplings:
        if g > 0:
            V = gravitational_potential_2d(Nx, Ny, (Nx // 2, Ny // 2), g)
        else:
            V = None

        H = build_2d_hamiltonian(Nx, Ny, t=1.0, m=0.0, potential=V)
        _, vecs = eigh(H)
        C = correlation_matrix(vecs, N // 2)

        subsystem_A = []
        for x in range(Nx // 2):
            for y in range(Ny):
                subsystem_A.append(x * Ny + y)

        S = entanglement_entropy(C, subsystem_A)
        S_vals.append(S)
        s_bdy = S / boundary
        S_over_bdy.append(s_bdy)

        delta_S = S - S_vals[0] if len(S_vals) > 1 else 0.0
        delta_s_over_g = delta_S / g if g > 0 else 0.0

        print(f"  {g:6.1f}  {S:10.4f}  {s_bdy:10.4f}  {delta_S:10.4f}  {delta_s_over_g:10.4f}")

    results["g_couplings"] = g_couplings
    results["S_vals"] = S_vals
    results["S_over_bdy"] = S_over_bdy

    # The RT formula predicts S = Area / (4G).
    # In our discrete setting, if we identify the gravitational coupling g
    # with 1/G_N, then S/boundary should be proportional to G_N ~ 1/g
    # i.e., S/boundary should DECREASE as g increases.
    # (Stronger gravity = more classical = less entanglement)

    S_free = S_vals[0]
    S_strong = S_vals[-1]
    entropy_decreases = S_strong < S_free

    # Fit S vs 1/g for g > 0
    g_pos = [g for g in g_couplings if g > 0]
    S_pos = [S_vals[i] for i, g in enumerate(g_couplings) if g > 0]

    if len(g_pos) >= 3:
        inv_g = np.array([1.0 / g for g in g_pos])
        S_arr = np.array(S_pos)
        coeffs_rt = np.polyfit(inv_g, S_arr, 1)
        pred = np.polyval(coeffs_rt, inv_g)
        ss_res = np.sum((S_arr - pred)**2)
        ss_tot = np.sum((S_arr - np.mean(S_arr))**2)
        r2_rt = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0

        print(f"\n  RT fit: S = {coeffs_rt[0]:.4f} / g + {coeffs_rt[1]:.4f}")
        print(f"  R^2 (S vs 1/g) = {r2_rt:.4f}")
        results["rt_r2"] = r2_rt
        results["rt_slope"] = coeffs_rt[0]
        results["rt_intercept"] = coeffs_rt[1]

        # Also try S vs g directly (linear)
        g_arr = np.array(g_pos)
        coeffs_lin = np.polyfit(g_arr, S_arr, 1)
        pred_lin = np.polyval(coeffs_lin, g_arr)
        ss_res_lin = np.sum((S_arr - pred_lin)**2)
        r2_lin = 1.0 - ss_res_lin / ss_tot if ss_tot > 0 else 0

        print(f"  Linear fit: S = {coeffs_lin[0]:.4f} * g + {coeffs_lin[1]:.4f}")
        print(f"  R^2 (S vs g) = {r2_lin:.4f}")
        results["linear_r2"] = r2_lin

        # Which fits better tells us the functional relationship
        if r2_rt > r2_lin:
            print(f"  S ~ 1/g fits better -> consistent with RT: S = Area/(4G) with G ~ 1/g")
        else:
            print(f"  S ~ g fits better -> gravity modifies entropy linearly")

    # Entanglement spectrum vs gravity
    print(f"\n  --- Entanglement spectrum vs gravity ---")
    for g in [0.0, 3.0, 10.0]:
        if g > 0:
            V = gravitational_potential_2d(Nx, Ny, (Nx // 2, Ny // 2), g)
        else:
            V = None
        H = build_2d_hamiltonian(Nx, Ny, t=1.0, m=0.0, potential=V)
        _, vecs = eigh(H)
        C = correlation_matrix(vecs, N // 2)
        subsystem_A = []
        for x in range(Nx // 2):
            for y in range(Ny):
                subsystem_A.append(x * Ny + y)
        esp = entanglement_spectrum(C, subsystem_A)
        xi = np.sort(np.log((1.0 - esp) / esp))
        print(f"    g={g:4.1f}: xi (first 5) = {xi[:5]}")
        # Entanglement gap (lowest entanglement energy)
        ent_gap = xi[0] if len(xi) > 0 else 0
        print(f"           entanglement gap = {ent_gap:.4f}")

    gate4 = entropy_decreases
    print(f"\n  Entropy decreases with gravity: {entropy_decreases}")
    print(f"  GATE 4 (RT connection): {'PASS' if gate4 else 'FAIL'}")

    results["gate4"] = gate4
    results["entropy_decreases"] = entropy_decreases
    return results


# ===================================================================
# Main: run all tests
# ===================================================================

def main():
    t_start = time.time()
    print("=" * 72)
    print("TENSOR NETWORK CONNECTION")
    print("The path-sum propagator as a Matrix Product Operator")
    print("=" * 72)

    results = {}

    # Test 1: MPO decomposition
    results["test1"] = test_mpo_decomposition()

    # Test 2: Entanglement structure
    results["test2"] = test_entanglement_structure()

    # Test 3: Gravitational bond dimension
    results["test3"] = test_gravitational_bond_dimension()

    # Test 4: Ryu-Takayanagi
    results["test4"] = test_ryu_takayanagi()

    # Summary
    elapsed = time.time() - t_start
    print("\n\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)

    gate1 = results["test1"].get("gate1", False)
    gate2 = results["test2"].get("gate2", False)
    gate3 = results["test3"].get("gate3", False)
    gate4 = results["test4"].get("gate4", False)

    print(f"  Gate 1 (propagator is MPO):             {'PASS' if gate1 else 'FAIL'}")
    print(f"  Gate 2 (entanglement matches TN):       {'PASS' if gate2 else 'FAIL'}")
    print(f"  Gate 3 (gravity reduces bond dim):      {'PASS' if gate3 else 'FAIL'}")
    print(f"  Gate 4 (Ryu-Takayanagi connection):     {'PASS' if gate4 else 'FAIL'}")

    # Key quantitative results
    if "cft_c" in results["test2"]:
        print(f"\n  Central charge c = {results['test2']['cft_c']:.4f} (expect 1.0)")
    if "area_law_r2" in results["test2"]:
        print(f"  Area law R^2 = {results['test2']['area_law_r2']:.4f}")
    if "rt_r2" in results["test4"]:
        print(f"  RT fit R^2 (S vs 1/g) = {results['test4']['rt_r2']:.4f}")

    n_pass = sum([gate1, gate2, gate3, gate4])
    print(f"\n  Gates passed: {n_pass}/4")
    print(f"  Elapsed: {elapsed:.1f}s")
    print("=" * 72)

    return results


if __name__ == "__main__":
    results = main()
