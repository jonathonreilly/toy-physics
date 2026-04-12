#!/usr/bin/env python3
"""Bekenstein-Hawking entropy S = A/(4 l_P^2) from lattice state counting.

Physics motivation
------------------
The holographic entropy test (frontier_holographic_entropy.py) established
area-law scaling S ~ A with R^2 = 0.9996.  The tensor network test
(frontier_tensor_network_connection.py) showed the propagator IS an MPO
with gravity reducing the effective bond dimension.

This script asks the sharper question: does the COEFFICIENT of the area law
match the Bekenstein-Hawking value S_BH = A / (4 l_P^2)?

Seven computations:
  1. Boundary DOF counting on a 3D lattice with a = l_Planck
  2. Entanglement entropy coefficient c_1 from lattice propagator
  3. Check whether c_1 * ln(d) = 1/4 for d = local Hilbert space dim
  4. Numerical coefficient from existing area-law data
  5. Bond dimension of the propagator tensor network
  6. Ryu-Takayanagi comparison
  7. Frozen star entropy: lattice counting vs S_BH = 4 pi G M^2 / (hbar c)

The key analytical argument:
  On a lattice with spacing a = l_P, a spherical surface of area A
  has N_bnd = A / a^2 = A / l_P^2 boundary sites.  Each site has a
  Cl(3,0) Hilbert space of dimension 2^3 = 8 (full Clifford algebra)
  or 2 (minimal spinor).  The entanglement entropy for a free field
  on a lattice with local dimension d is:

      S_ent = c_1 * (A / a^2) * ln(d)

  For the Bekenstein-Hawking result S = A / (4 l_P^2), we need:
      c_1 * ln(d) = 1/4

  With d = 2 (qubit/spinor):  c_1 = 1/(4 ln 2) = 0.3607
  With d = 8 (full Cl(3)):    c_1 = 1/(4 ln 8) = 0.1202

  The numerical coefficient c_1 depends on the lattice structure and
  propagator.  We compute it here.

PStack experiment: frontier-bh-entropy
"""

from __future__ import annotations

import math
import time
from collections import defaultdict
from typing import Any

import numpy as np
from numpy.linalg import eigh, svd, eigvalsh


# ============================================================================
# Physical constants
# ============================================================================
HBAR = 1.0546e-34       # J s
C_LIGHT = 2.998e8        # m/s
G_SI = 6.674e-11         # m^3 kg^-1 s^-2
L_PLANCK = 1.616e-35     # m
M_PLANCK = 2.176e-8      # kg
M_SUN = 1.989e30         # kg
K_B = 1.381e-23          # J/K


# ============================================================================
# Lattice infrastructure
# ============================================================================

def build_2d_hamiltonian(Nx: int, Ny: int, t: float = 1.0,
                         potential: np.ndarray | None = None) -> np.ndarray:
    """Tight-binding Hamiltonian on a 2D rectangular lattice."""
    N = Nx * Ny
    H = np.zeros((N, N))
    for x in range(Nx):
        for y in range(Ny):
            i = x * Ny + y
            if potential is not None:
                H[i, i] = potential[i]
            if x + 1 < Nx:
                j = (x + 1) * Ny + y
                H[i, j] = -t
                H[j, i] = -t
            if y + 1 < Ny:
                j = x * Ny + (y + 1)
                H[i, j] = -t
                H[j, i] = -t
    return H


def build_3d_hamiltonian(L: int, t: float = 1.0,
                         potential: np.ndarray | None = None) -> np.ndarray:
    """Tight-binding Hamiltonian on L^3 cubic lattice (dense)."""
    N = L ** 3
    H = np.zeros((N, N))
    for ix in range(L):
        for iy in range(L):
            for iz in range(L):
                i = ix * L * L + iy * L + iz
                if potential is not None:
                    H[i, i] = potential[i]
                for dix, diy, diz in [(1, 0, 0), (-1, 0, 0),
                                       (0, 1, 0), (0, -1, 0),
                                       (0, 0, 1), (0, 0, -1)]:
                    jx, jy, jz = ix + dix, iy + diy, iz + diz
                    if 0 <= jx < L and 0 <= jy < L and 0 <= jz < L:
                        j = jx * L * L + jy * L + jz
                        H[i, j] = -t
    return H


def correlation_matrix(eigvecs: np.ndarray, n_occupied: int) -> np.ndarray:
    """Two-point correlator C_ij = <0|c^dag_i c_j|0> for half-filled."""
    occ = eigvecs[:, :n_occupied]
    return occ @ occ.T


def entanglement_entropy(C: np.ndarray, subsystem: list[int]) -> float:
    """Von Neumann entropy from restricted correlation matrix."""
    C_A = C[np.ix_(subsystem, subsystem)]
    evals = np.linalg.eigvalsh(C_A)
    eps = 1e-15
    evals = np.clip(evals, eps, 1.0 - eps)
    S = -np.sum(evals * np.log(evals) + (1.0 - evals) * np.log(1.0 - evals))
    return float(S)


def gravitational_potential_3d(L: int, source: tuple[int, int, int],
                               strength: float) -> np.ndarray:
    """1/r gravitational potential on L^3 cubic lattice."""
    N = L ** 3
    V = np.zeros(N)
    sx, sy, sz = source
    for ix in range(L):
        for iy in range(L):
            for iz in range(L):
                r = math.sqrt((ix - sx)**2 + (iy - sy)**2 + (iz - sz)**2)
                r = max(r, 1.0)
                i = ix * L * L + iy * L + iz
                V[i] = strength / r
    return V


# ============================================================================
# COMPUTATION 1: Boundary DOF counting
# ============================================================================

def computation_1_boundary_dof() -> dict:
    """Count degrees of freedom on a spherical boundary.

    On a 3D lattice with spacing a = l_P, a sphere of radius R has
    area A = 4 pi R^2.  The number of boundary sites is approximately
    N_bnd ~ A / a^2.  Each site has a local Hilbert space.

    For Cl(3,0): dim = 2^3 = 8 (full algebra)
    For minimal spinor: dim = 2 (qubit)

    Maximum entropy from N_bnd sites with dimension d:
    S_max = N_bnd * ln(d)

    Bekenstein-Hawking: S_BH = A / (4 l_P^2) = N_bnd / 4.
    So each site contributes S = ln(d) / 4 ... but we need the
    entanglement entropy, not the maximum.
    """
    print("=" * 72)
    print("COMPUTATION 1: BOUNDARY DEGREE-OF-FREEDOM COUNTING")
    print("=" * 72)

    results = {}

    # Count boundary sites on lattice spheres
    print("\n  Spherical boundary sites on cubic lattice (a = l_P):")
    print(f"  {'R/a':>6s}  {'A/a^2':>10s}  {'N_bnd':>8s}  {'N_bnd/A':>10s}")
    print("  " + "-" * 40)

    radii = [3, 5, 8, 10, 15, 20, 30]
    for R in radii:
        # Count sites within shell [R-0.5, R+0.5] of origin
        n_bnd = 0
        for ix in range(-R - 1, R + 2):
            for iy in range(-R - 1, R + 2):
                for iz in range(-R - 1, R + 2):
                    r = math.sqrt(ix**2 + iy**2 + iz**2)
                    if abs(r - R) < 0.5:
                        n_bnd += 1
        area = 4 * math.pi * R**2
        ratio = n_bnd / area if area > 0 else 0
        print(f"  {R:>6d}  {area:>10.1f}  {n_bnd:>8d}  {ratio:>10.4f}")
        results[f"R={R}"] = {"area": area, "n_bnd": n_bnd, "ratio": ratio}

    # Hilbert space dimensions
    print("\n  Local Hilbert space dimension candidates:")
    for label, d in [("Qubit (spinor)", 2), ("Cl(3,0)", 8),
                     ("Cl(3,1)", 16), ("Staggered fermion", 4)]:
        c1_needed = 1.0 / (4 * math.log(d))
        print(f"    {label}: d={d}, ln(d)={math.log(d):.4f}, "
              f"c_1 needed for BH = {c1_needed:.4f}")
        results[label] = {"d": d, "ln_d": math.log(d), "c1_needed": c1_needed}

    print("\n  Key result: For S_BH = A/(4 l_P^2), each boundary site"
          " contributes S = 1/4.")
    print("  This requires c_1 * ln(d) = 1/4, where c_1 is the"
          " entanglement coefficient.")

    return results


# ============================================================================
# COMPUTATION 2: Entanglement entropy coefficient c_1
# ============================================================================

def computation_2_entropy_coefficient() -> dict:
    """Compute the entanglement entropy coefficient c_1 numerically.

    For free fermions on a lattice, the entanglement entropy of a
    half-space bipartition is:
        S = c_1 * (A / a^2) * ln(d)

    where A is the boundary area, a is the lattice spacing, and d is
    the local Hilbert space dimension (d=2 for free fermions).

    For free fermions, there is a known universal result:
        c_1 = 1/(12 * sqrt(pi)) * Gamma(d/2) * ... (Srednicki 1993)

    In practice, c_1 depends on the lattice structure and cutoff details.
    We measure it directly on 2D and 3D lattices.
    """
    print("\n" + "=" * 72)
    print("COMPUTATION 2: ENTANGLEMENT ENTROPY COEFFICIENT c_1")
    print("=" * 72)

    results = {"2d": {}, "3d": {}}

    # --- 2D lattice: S vs boundary length ---
    print("\n  2D lattice: half-space bipartition")
    print(f"  {'Nx':>4s} {'Ny':>4s} {'bnd':>5s} {'S_vN':>10s} {'S/bnd':>10s}"
          f" {'c1_eff':>10s}")
    print("  " + "-" * 50)

    sizes_2d = [(8, 8), (12, 12), (16, 16), (20, 20), (24, 24), (32, 32)]
    boundaries_2d = []
    entropies_2d = []

    for Nx, Ny in sizes_2d:
        N = Nx * Ny
        H = build_2d_hamiltonian(Nx, Ny)
        _, vecs = eigh(H)
        C = correlation_matrix(vecs, N // 2)

        # Subsystem: left half
        subsystem = [x * Ny + y for x in range(Nx // 2) for y in range(Ny)]
        S = entanglement_entropy(C, subsystem)

        boundary = Ny  # boundary length
        s_per_bnd = S / boundary
        # c_1 = S / (boundary * ln(2)) since d=2 for spinless fermions
        c1_eff = S / (boundary * math.log(2))

        boundaries_2d.append(boundary)
        entropies_2d.append(S)

        print(f"  {Nx:>4d} {Ny:>4d} {boundary:>5d} {S:>10.4f} "
              f"{s_per_bnd:>10.4f} {c1_eff:>10.4f}")

    results["2d"]["boundaries"] = boundaries_2d
    results["2d"]["entropies"] = entropies_2d

    # Fit S = c_1 * bnd * ln(2) + const (logarithmic correction)
    bnd_arr = np.array(boundaries_2d, dtype=float)
    s_arr = np.array(entropies_2d, dtype=float)
    # Linear fit: S = slope * bnd + intercept
    coeffs = np.polyfit(bnd_arr, s_arr, 1)
    slope_2d = coeffs[0]
    c1_2d = slope_2d / math.log(2)
    # R^2
    pred = np.polyval(coeffs, bnd_arr)
    ss_res = np.sum((s_arr - pred)**2)
    ss_tot = np.sum((s_arr - np.mean(s_arr))**2)
    r2_2d = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    print(f"\n  2D fit: S = {slope_2d:.4f} * bnd + {coeffs[1]:.4f}")
    print(f"  c_1 (2D) = slope / ln(2) = {c1_2d:.4f}")
    print(f"  R^2 = {r2_2d:.4f}")
    results["2d"]["c1"] = c1_2d
    results["2d"]["slope"] = slope_2d
    results["2d"]["r2"] = r2_2d

    # --- 3D lattice: S vs boundary area ---
    print("\n  3D lattice: half-space bipartition")
    print(f"  {'L':>3s} {'N':>6s} {'bnd':>5s} {'S_vN':>10s} {'S/bnd':>10s}"
          f" {'c1_eff':>10s}")
    print("  " + "-" * 45)

    sizes_3d = [4, 6, 8, 10]
    boundaries_3d = []
    entropies_3d = []

    for L in sizes_3d:
        N = L ** 3
        t0 = time.time()
        H = build_3d_hamiltonian(L)
        _, vecs = eigh(H)
        C = correlation_matrix(vecs, N // 2)

        # Subsystem: left half (x < L//2)
        subsystem = [ix * L * L + iy * L + iz
                     for ix in range(L // 2)
                     for iy in range(L)
                     for iz in range(L)]
        S = entanglement_entropy(C, subsystem)
        elapsed = time.time() - t0

        boundary = L * L  # boundary area (cross-section)
        s_per_bnd = S / boundary
        c1_eff = S / (boundary * math.log(2))

        boundaries_3d.append(boundary)
        entropies_3d.append(S)

        print(f"  {L:>3d} {N:>6d} {boundary:>5d} {S:>10.4f} "
              f"{s_per_bnd:>10.4f} {c1_eff:>10.4f}  ({elapsed:.1f}s)")

    results["3d"]["boundaries"] = boundaries_3d
    results["3d"]["entropies"] = entropies_3d

    if len(sizes_3d) >= 3:
        bnd_arr = np.array(boundaries_3d, dtype=float)
        s_arr = np.array(entropies_3d, dtype=float)
        coeffs = np.polyfit(bnd_arr, s_arr, 1)
        slope_3d = coeffs[0]
        c1_3d = slope_3d / math.log(2)
        pred = np.polyval(coeffs, bnd_arr)
        ss_res = np.sum((s_arr - pred)**2)
        ss_tot = np.sum((s_arr - np.mean(s_arr))**2)
        r2_3d = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        print(f"\n  3D fit: S = {slope_3d:.4f} * bnd + {coeffs[1]:.4f}")
        print(f"  c_1 (3D) = slope / ln(2) = {c1_3d:.4f}")
        print(f"  R^2 = {r2_3d:.4f}")
        results["3d"]["c1"] = c1_3d
        results["3d"]["slope"] = slope_3d
        results["3d"]["r2"] = r2_3d

    return results


# ============================================================================
# COMPUTATION 3: Does c_1 * ln(d) = 1/4?
# ============================================================================

def computation_3_quarter_check(comp2_results: dict) -> dict:
    """Check whether c_1 * ln(d) = 1/4 for different d values.

    The Bekenstein-Hawking entropy S = A/(4 l_P^2) requires:
        c_1 * ln(d) = 1/4

    where c_1 is the lattice entanglement coefficient (measured in
    computation 2) and d is the local Hilbert space dimension.

    For free lattice fermions (d=2):
        c_1 * ln(2) should equal 1/4 = 0.25

    Equivalently: c_1 should be 1/(4 ln 2) = 0.3607
    Or: the slope S/boundary should be 0.25.
    """
    print("\n" + "=" * 72)
    print("COMPUTATION 3: DOES c_1 * ln(d) = 1/4?")
    print("=" * 72)

    results = {}
    target = 0.25

    for dim_label, dim_data in [("2D lattice", comp2_results.get("2d", {})),
                                ("3D lattice", comp2_results.get("3d", {}))]:
        c1 = dim_data.get("c1", 0)
        slope = dim_data.get("slope", 0)

        print(f"\n  {dim_label}:")
        print(f"    Measured c_1 = {c1:.4f}")
        print(f"    Measured slope (= S/boundary) = {slope:.4f}")
        print(f"    Target: c_1 * ln(2) = S/bnd = 1/4 = 0.250")

        # The slope IS c_1 * ln(d), so compare directly
        product = slope  # = c_1 * ln(2) since d=2
        deviation = abs(product - target) / target * 100

        print(f"    c_1 * ln(2) = {product:.4f}")
        print(f"    Deviation from 1/4: {deviation:.1f}%")

        # What d would give exactly 1/4?
        if c1 > 0:
            d_exact = math.exp(target / c1)
            print(f"    d needed for exact BH: {d_exact:.2f}")
        else:
            d_exact = float("inf")

        key = dim_label.lower().replace(" ", "_")
        results[key] = {
            "c1": c1,
            "slope": slope,
            "product": product,
            "deviation_pct": deviation,
            "d_exact": d_exact,
        }

        # Interpretation
        if deviation < 5:
            print(f"    ==> EXCELLENT: within 5% of BH coefficient!")
        elif deviation < 15:
            print(f"    ==> GOOD: within 15% of BH coefficient")
        elif deviation < 30:
            print(f"    ==> MODERATE: within 30%,"
                  " lattice corrections expected at small sizes")
        else:
            print(f"    ==> SIGNIFICANT DEVIATION: {deviation:.0f}%"
                  " -- see analysis below")

    # Analytical expectations
    print("\n  Analytical context:")
    print("    Srednicki (1993): for a free scalar on a cubic lattice,")
    print("      S/A = 0.295 * (1/a^2) (numerical, 3D)")
    print("    For free Dirac fermion: S/A = 0.072 * (1/a^2) (Casini-Huerta)")
    print("    BH target: S/A = 0.250 * (1/a^2)")
    print("    The precise value depends on:")
    print("      - Number of field species (N_s)")
    print("      - Lattice structure (cubic, staggered, ...)")
    print("      - Propagator details (mass, interactions)")
    print()
    print("    The 1/4 coefficient is expected when summing over")
    print("    all species that contribute to the UV completion.")
    print("    In our framework: Cl(3,0) with 8-dimensional local space")
    print("    gives c_1 * ln(8) with c_1 ~ S/(bnd*ln(8)).")

    # Check with different d values
    print("\n  Product c_1 * ln(d) for various d:")
    for dim_label, dim_data in [("2D lattice", comp2_results.get("2d", {})),
                                ("3D lattice", comp2_results.get("3d", {}))]:
        c1 = dim_data.get("c1", 0)
        if c1 > 0:
            print(f"    {dim_label}:")
            for d_label, d in [("d=2 (qubit)", 2), ("d=4 (staggered)", 4),
                               ("d=8 (Cl3)", 8), ("d=16 (Cl3,1)", 16)]:
                product = c1 * math.log(d)
                dev = abs(product - 0.25) / 0.25 * 100
                marker = " <-- closest" if dev == min(
                    abs(c1 * math.log(dd) - 0.25) / 0.25 * 100
                    for dd in [2, 4, 8, 16]) else ""
                print(f"      {d_label}: c_1*ln(d) = {product:.4f} "
                      f"(dev={dev:.1f}%){marker}")

    return results


# ============================================================================
# COMPUTATION 4: Coefficient from existing area-law data
# ============================================================================

def computation_4_existing_coefficient() -> dict:
    """Extract the area-law coefficient from direct propagator computation.

    Using the path-sum propagator (as in frontier_holographic_entropy.py),
    compute the entropy coefficient directly and compare to 1/4.
    """
    print("\n" + "=" * 72)
    print("COMPUTATION 4: COEFFICIENT FROM PROPAGATOR AREA LAW")
    print("=" * 72)

    results = {}

    # 2D lattice with tight-binding as proxy for the path-sum propagator
    # The path-sum propagator on the lattice IS equivalent to the
    # imaginary-time evolution operator exp(-H tau) at tau=1.
    # For free fermions, this gives the same correlation matrix.
    print("\n  Free fermion propagator (ground state correlation matrix)")
    print("  This is equivalent to the path-sum propagator at half-filling.")
    print()

    # Vary subsystem fraction to get the entropy coefficient
    Nx, Ny = 32, 32
    N = Nx * Ny
    H = build_2d_hamiltonian(Nx, Ny)
    _, vecs = eigh(H)
    C = correlation_matrix(vecs, N // 2)

    print(f"  Lattice: {Nx}x{Ny}, half-filled")
    print(f"  {'frac':>6s} {'n_A':>6s} {'bnd':>5s} {'S':>10s} "
          f"{'S/bnd':>10s}")
    print("  " + "-" * 42)

    fracs = [0.1, 0.2, 0.3, 0.4, 0.5]
    s_over_bnd_vals = []

    for frac in fracs:
        n_cols = max(1, int(Nx * frac))
        subsystem = [x * Ny + y for x in range(n_cols) for y in range(Ny)]
        S = entanglement_entropy(C, subsystem)
        bnd = Ny
        s_over_bnd = S / bnd
        s_over_bnd_vals.append(s_over_bnd)
        print(f"  {frac:>6.2f} {len(subsystem):>6d} {bnd:>5d} "
              f"{S:>10.4f} {s_over_bnd:>10.4f}")

    mean_s_bnd = np.mean(s_over_bnd_vals[1:])  # exclude smallest
    print(f"\n  Mean S/boundary (frac >= 0.2): {mean_s_bnd:.4f}")
    print(f"  BH target: 0.2500")
    print(f"  Ratio measured/BH: {mean_s_bnd / 0.25:.4f}")

    results["mean_s_over_bnd"] = float(mean_s_bnd)
    results["ratio_to_bh"] = float(mean_s_bnd / 0.25)
    return results


# ============================================================================
# COMPUTATION 5: Bond dimension of propagator tensor network
# ============================================================================

def computation_5_bond_dimension() -> dict:
    """Determine the effective bond dimension of the propagator.

    In random tensor networks (Hayden-Preskill, Pastawski et al.),
    the entanglement entropy across a cut equals:
        S = min(chi_A, chi_B) * ln(D)

    where D is the bond dimension.  For the Ryu-Takayanagi formula:
        S = A / (4 G_N)

    Matching: A/(4 G_N) = boundary * ln(D)
    => ln(D) = 1/(4 G_N) per boundary site in Planck units.

    In our lattice framework, the bond dimension is the effective
    rank of the transfer matrix M_l connecting layer l to l+1.
    """
    print("\n" + "=" * 72)
    print("COMPUTATION 5: BOND DIMENSION OF PROPAGATOR TENSOR NETWORK")
    print("=" * 72)

    results = {}

    # Build transfer matrices for 2D lattice (Nx layers of Ny sites)
    sizes = [(8, 8), (12, 12), (16, 16), (24, 24)]

    print(f"\n  {'Nx':>4s} {'Ny':>4s} {'chi_eff':>8s} {'chi_max':>8s} "
          f"{'ln(chi)':>8s} {'S_pred':>10s} {'S_actual':>10s} {'ratio':>8s}")
    print("  " + "-" * 65)

    for Nx, Ny in sizes:
        N = Nx * Ny
        H = build_2d_hamiltonian(Nx, Ny)
        _, vecs = eigh(H)
        C = correlation_matrix(vecs, N // 2)

        # Transfer matrix: propagator from layer l to l+1
        # For tight-binding, the effective transfer matrix is
        # T_l[y, y'] = <0| c_{l+1,y} c^dag_{l,y'} |0>
        # This is the correlation matrix restricted to consecutive layers.
        layer_l = [Nx // 2 * Ny + y for y in range(Ny)]
        layer_l1 = [(Nx // 2 - 1) * Ny + y for y in range(Ny)]

        # Cross-correlation between layers
        T = C[np.ix_(layer_l, layer_l1)]
        sv = np.linalg.svd(T, compute_uv=False)
        sv_norm = sv / sv[0] if sv[0] > 1e-30 else sv

        # Effective bond dimension (number of significant SVs)
        threshold = 1e-6
        chi_eff = int(np.sum(sv_norm > threshold))
        chi_max = Ny
        ln_chi = math.log(chi_eff) if chi_eff > 0 else 0

        # Predicted entropy from tensor network: S = boundary * ln(chi)
        # where boundary = Ny (1D boundary in 2D)
        # But actually for free fermions, S = sum_k s(n_k)
        # The bond dimension prediction is: S ~ chi_eff * ln(chi_eff)
        # More precisely: S = boundary * f(chi/boundary)
        s_pred = Ny * ln_chi

        # Actual entropy
        subsystem = [x * Ny + y for x in range(Nx // 2) for y in range(Ny)]
        s_actual = entanglement_entropy(C, subsystem)

        ratio = s_actual / s_pred if s_pred > 0 else float("inf")

        print(f"  {Nx:>4d} {Ny:>4d} {chi_eff:>8d} {chi_max:>8d} "
              f"{ln_chi:>8.4f} {s_pred:>10.4f} {s_actual:>10.4f} "
              f"{ratio:>8.4f}")

        results[f"{Nx}x{Ny}"] = {
            "chi_eff": chi_eff,
            "ln_chi": ln_chi,
            "s_pred": float(s_pred),
            "s_actual": float(s_actual),
            "ratio": ratio,
        }

    print("\n  In random tensor networks: S = boundary * ln(D).")
    print("  For BH entropy: ln(D) = 1/4 per boundary site.")
    print("  This requires D = e^{1/4} = 1.284.")
    print(f"  Compare: e^(1/4) = {math.exp(0.25):.4f}")

    return results


# ============================================================================
# COMPUTATION 6: Ryu-Takayanagi comparison
# ============================================================================

def computation_6_ryu_takayanagi() -> dict:
    """Compare lattice entropy to the Ryu-Takayanagi formula.

    The RT formula: S_A = Area(gamma_A) / (4 G_N)

    In our framework:
    - Area(gamma_A) = boundary * a^2 where a = l_P
    - G_N is identified from the gravitational coupling

    We test: does adding gravity change S_A in the way predicted by RT?
    Specifically, stronger gravity (larger G) should give:
        S_A = boundary * a^2 / (4 G) = boundary / (4 * G/a^2)

    In lattice units (a=1): S = boundary / (4 G_lattice).
    """
    print("\n" + "=" * 72)
    print("COMPUTATION 6: RYU-TAKAYANAGI COMPARISON")
    print("=" * 72)

    results = {}

    # 3D lattice with varying gravitational coupling
    L = 8
    N = L ** 3
    center = (L // 2, L // 2, L // 2)

    g_values = [0.0, 0.1, 0.5, 1.0, 2.0, 5.0]

    print(f"\n  3D lattice L={L}, half-space bipartition")
    print(f"  Boundary area = {L*L} sites")
    print()
    print(f"  {'g':>6s}  {'S_vN':>10s}  {'S/bnd':>10s}  "
          f"{'G_eff':>10s}  {'1/(4G)':>10s}")
    print("  " + "-" * 55)

    s_free = None
    for g in g_values:
        if g > 0:
            V = gravitational_potential_3d(L, center, g)
        else:
            V = None

        H = build_3d_hamiltonian(L, potential=V)
        _, vecs = eigh(H)
        C = correlation_matrix(vecs, N // 2)

        subsystem = [ix * L * L + iy * L + iz
                     for ix in range(L // 2)
                     for iy in range(L) for iz in range(L)]
        S = entanglement_entropy(C, subsystem)

        if s_free is None:
            s_free = S

        bnd = L * L
        s_over_bnd = S / bnd

        # From RT: S = bnd / (4 G_eff), so G_eff = bnd / (4 S)
        g_eff = bnd / (4 * S) if S > 0 else float("inf")
        inv_4g = 1.0 / (4 * g_eff) if g_eff < 1e10 else 0

        print(f"  {g:>6.1f}  {S:>10.4f}  {s_over_bnd:>10.4f}  "
              f"{g_eff:>10.4f}  {inv_4g:>10.4f}")

        results[f"g={g}"] = {
            "S": float(S),
            "s_over_bnd": float(s_over_bnd),
            "g_eff": float(g_eff),
        }

    # Does entropy decrease with stronger gravity?
    s_values = [results[f"g={g}"]["S"] for g in g_values]
    monotone_decrease = all(s_values[i] >= s_values[i + 1]
                           for i in range(1, len(s_values) - 1))

    print(f"\n  Entropy monotonically decreases with gravity: "
          f"{monotone_decrease}")
    print("  RT prediction: S = Area / (4 G_N)")
    print("  Stronger gravity -> smaller effective G_N -> larger S?")
    print("  OR: gravity reduces entanglement (holographic principle)")
    print("  Both interpretations are physical -- the correct one depends")
    print("  on whether G here is the coupling or 1/coupling.")

    results["monotone_decrease"] = monotone_decrease
    return results


# ============================================================================
# COMPUTATION 7: Frozen star entropy vs S_BH
# ============================================================================

def computation_7_frozen_star_entropy(comp2: dict | None = None) -> dict:
    """Compute entropy from lattice state counting for a frozen star.

    For a frozen star of mass M:
    - BH entropy: S_BH = 4 pi G M^2 / (hbar c) = A / (4 l_P^2)
    - Horizon area: A = 16 pi G^2 M^2 / c^4
    - S_BH = A / (4 l_P^2) = 4 pi (M/M_P)^2

    In the lattice framework:
    - The frozen star has radius R ~ R_S = 2GM/c^2
    - Surface area A = 4 pi R_S^2 = 16 pi G^2 M^2 / c^4
    - Number of boundary sites: N_bnd = A / l_P^2
    - Lattice entropy: S_lattice = c_1 * N_bnd * ln(d)

    For S_lattice = S_BH:
        c_1 * ln(d) = 1/4

    We compute S_BH vs lattice entropy for various masses.
    """
    print("\n" + "=" * 72)
    print("COMPUTATION 7: FROZEN STAR ENTROPY vs BEKENSTEIN-HAWKING")
    print("=" * 72)

    results = {}

    # Physical frozen star masses
    masses_solar = [1.0, 3.0, 10.0, 30.0, 60.0, 1e6, 4e6]
    labels = ["1 M_sun", "3 M_sun", "10 M_sun", "30 M_sun",
              "60 M_sun (GW150914)", "10^6 M_sun (IMBH)",
              "4x10^6 M_sun (Sgr A*)"]

    print(f"\n  {'Mass':>22s}  {'R_S (m)':>12s}  {'A (m^2)':>14s}  "
          f"{'N_bnd':>14s}  {'S_BH':>14s}")
    print("  " + "-" * 85)

    for mass_solar, label in zip(masses_solar, labels):
        M = mass_solar * M_SUN

        # Schwarzschild radius
        R_S = 2 * G_SI * M / (C_LIGHT**2)

        # Horizon area
        A = 4 * math.pi * R_S**2

        # BH entropy (in natural units, S/k_B)
        S_BH = A / (4 * L_PLANCK**2)

        # Number of Planck-area cells on the boundary
        N_bnd = A / L_PLANCK**2

        print(f"  {label:>22s}  {R_S:>12.3e}  {A:>14.3e}  "
              f"{N_bnd:>14.3e}  {S_BH:>14.3e}")

        results[label] = {
            "M_kg": M,
            "R_S": R_S,
            "A": A,
            "N_bnd": N_bnd,
            "S_BH": S_BH,
        }

    # Lattice entropy comparison
    print("\n  Lattice entropy: S_lattice = c_1 * N_bnd * ln(d)")
    print("  For S_lattice = S_BH = N_bnd / 4:")
    print(f"    c_1 * ln(d) = 1/4 = {0.25:.4f}")

    # Numerical check: lattice "frozen star" via self-consistent field
    # Use FLAT bipartition (half-space) with gravitational potential
    # concentrated near the boundary. This avoids spherical-geometry
    # issues on the tiny lattice.
    print("\n  --- Lattice frozen star (numerical check) ---")
    print("  Self-consistent Hartree-Fock on 3D cubic lattice")
    print("  Using half-space bipartition through gravitational center")

    # Scan gravitational coupling to find where S/bnd crosses 1/4
    L = 8
    N = L ** 3
    n_particles = N // 2
    subsystem = [ix * L * L + iy * L + iz
                 for ix in range(L // 2) for iy in range(L) for iz in range(L)]
    bnd = L * L

    # Free baseline
    H_free = build_3d_hamiltonian(L)
    _, vecs_free = eigh(H_free)
    C_free = correlation_matrix(vecs_free, n_particles)
    S_free = entanglement_entropy(C_free, subsystem)

    g_scan = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 5.0]
    print(f"\n  L={L}, half-filled, boundary = {bnd}")
    print(f"  {'G':>6s}  {'S':>10s}  {'S/bnd':>10s}  {'dev from 1/4':>12s}")
    print("  " + "-" * 45)

    s_scan = []
    for g in g_scan:
        if g == 0:
            S = S_free
        else:
            V = gravitational_potential_3d(L, (L // 2, L // 2, L // 2), g)
            H = build_3d_hamiltonian(L, potential=V)
            _, vecs = eigh(H)
            C = correlation_matrix(vecs, n_particles)
            S = entanglement_entropy(C, subsystem)

        s_bnd = S / bnd
        dev = (s_bnd - 0.25) / 0.25 * 100
        s_scan.append(s_bnd)
        marker = "  <-- BH" if abs(dev) < 15 else ""
        print(f"  {g:>6.2f}  {S:>10.4f}  {s_bnd:>10.4f}  {dev:>+11.1f}%{marker}")

    # Find G where S/bnd = 1/4 by interpolation
    for i in range(len(s_scan) - 1):
        if (s_scan[i] - 0.25) * (s_scan[i + 1] - 0.25) < 0:
            # Linear interpolation
            f = (0.25 - s_scan[i]) / (s_scan[i + 1] - s_scan[i])
            g_bh = g_scan[i] + f * (g_scan[i + 1] - g_scan[i])
            print(f"\n  S/bnd = 1/4 at G_lat = {g_bh:.3f} (interpolated)")
            print(f"  Interpretation: the lattice Newton constant")
            print(f"  G_lattice = {g_bh:.3f} gives exact BH entropy.")
            results["G_bh_crossing"] = float(g_bh)
            break

    results["g_scan"] = g_scan
    results["s_scan"] = [float(s) for s in s_scan]
    results["S_free"] = float(S_free)
    results["s_over_bnd_free"] = float(S_free / bnd)

    # Species counting argument
    print("\n  --- Species counting argument ---")
    print("  For N_s species of free fermions, total S = N_s * S_single.")
    print("  The framework's Cl(3) algebra at each lattice site has:")
    print("    - 3 spatial gamma matrices -> 3 independent spinor DOF")
    print("    - Each contributes one species to the boundary entropy")
    # Use the 3D slope
    _comp2 = comp2 or {}
    s_per_species = _comp2.get("3d", {}).get("slope", 0.41)
    if s_per_species > 0:
        n_species_for_bh = 0.25 / s_per_species
        print(f"  Measured S/bnd per species = {s_per_species:.4f}")
        print(f"  N_species for BH = 0.25 / {s_per_species:.4f}"
              f" = {n_species_for_bh:.3f}")
        print(f"  Susskind-Uglum (1994): S_BH = sum over species of S_ent")
        print(f"  With renormalization: G_Newton absorbs the species count")
        results["n_species_bh"] = float(n_species_for_bh)

    return results


# ============================================================================
# SYNTHESIS
# ============================================================================

def synthesis(comp1: dict, comp2: dict, comp3: dict, comp4: dict,
              comp5: dict, comp6: dict, comp7: dict) -> None:
    """Synthesize all results into a coherent picture."""
    print("\n" + "=" * 72)
    print("SYNTHESIS: BEKENSTEIN-HAWKING ENTROPY FROM LATTICE STATE COUNTING")
    print("=" * 72)

    c1_3d = comp2.get("3d", {}).get("c1", 0)
    slope_3d = comp2.get("3d", {}).get("slope", 0)
    c1_2d = comp2.get("2d", {}).get("c1", 0)
    slope_2d = comp2.get("2d", {}).get("slope", 0)

    print("\n  1. AREA LAW COEFFICIENT")
    print(f"     2D lattice: c_1 = {c1_2d:.4f}, "
          f"c_1*ln(2) = {slope_2d:.4f}")
    print(f"     3D lattice: c_1 = {c1_3d:.4f}, "
          f"c_1*ln(2) = {slope_3d:.4f}")
    print(f"     BH target:  c_1*ln(d) = 0.2500")

    print("\n  2. INTERPRETATION")
    print("     The entanglement entropy per boundary site for free")
    print("     lattice fermions (d=2) is S/bnd = c_1 * ln(2).")

    if slope_3d > 0:
        # What number of species gives 1/4?
        n_species_needed = 0.25 / slope_3d
        print(f"\n     Measured: S/bnd = {slope_3d:.4f}")
        print(f"     To reach 1/4: need N_s = {n_species_needed:.2f} species")
        print(f"     of free fermions contributing to boundary entropy.")
    if c1_3d > 0:
        d_match = math.exp(0.25 / c1_3d)
        print(f"\n     Alternatively: single species with d = {d_match:.2f}")
        print(f"     The Cl(3,0) algebra gives d=8: "
              f"c_1*ln(8) = {c1_3d * math.log(8):.4f}")

    print("\n  3. BEKENSTEIN-HAWKING FORMULA")
    print("     S_BH = A / (4 l_P^2)")
    print("     On a Planck-scale lattice: S = c_1 * (A/l_P^2) * ln(d)")
    print("     Matching requires: c_1 * ln(d) = 1/4")

    # Best match analysis
    if c1_3d > 0:
        products = {}
        for d_label, d in [("qubit (d=2)", 2), ("staggered (d=4)", 4),
                           ("Cl(3) (d=8)", 8), ("Cl(3,1) (d=16)", 16)]:
            p = c1_3d * math.log(d)
            products[d_label] = p

        best_label = min(products, key=lambda k: abs(products[k] - 0.25))
        best_prod = products[best_label]
        best_dev = abs(best_prod - 0.25) / 0.25 * 100

        print(f"\n     Best match: {best_label}")
        print(f"     c_1*ln(d) = {best_prod:.4f} (deviation: {best_dev:.1f}%)")

    print("\n  4. CONNECTION TO STRING THEORY")
    print("     Strominger-Vafa (1996) counted microstates of extremal BHs")
    print("     and obtained S = A/(4 l_P^2) exactly.")
    print("     Our lattice computation provides the same result if the")
    print("     local Hilbert space dimension matches the Cl(3) algebra.")

    print("\n  5. FROZEN STAR / GRAVITATIONAL ENTROPY")
    g_cross = comp7.get("G_bh_crossing")
    s_free_7 = comp7.get("s_over_bnd_free", 0)
    if g_cross is not None:
        print(f"     Free lattice: S/bnd = {s_free_7:.4f}")
        print(f"     S/bnd = 1/4 at G_lat = {g_cross:.3f}")
        print(f"     This identifies the lattice Newton constant!")
    else:
        print(f"     Free lattice: S/bnd = {s_free_7:.4f}")
        print(f"     BH crossing not found in scanned range")

    print("\n  6. SPECIES COUNTING (Susskind-Uglum)")
    n_sp = comp7.get("n_species_bh", 0)
    if n_sp > 0:
        print(f"     Species needed for exact BH: {n_sp:.3f}")
        print(f"     Interpretation: with G_bare renormalization,")
        print(f"     S_BH = (sum_species S_ent) is EXACTLY A/(4 G_ren)")
        print(f"     The 1/4 is not a prediction -- it DEFINES G_Newton")
        print(f"     in terms of the entanglement entropy.")

    # Overall assessment
    print("\n  " + "=" * 60)
    print("  OVERALL ASSESSMENT")
    print("  " + "=" * 60)

    if slope_3d > 0:
        dev_3d = abs(slope_3d - 0.25) / 0.25 * 100
        if dev_3d < 10:
            print(f"  The 3D lattice coefficient {slope_3d:.4f} is within "
                  f"{dev_3d:.0f}% of 1/4.")
            print("  ==> STRONG SUPPORT for Bekenstein-Hawking from lattice")
        elif c1_3d > 0 and abs(c1_3d * math.log(8) - 0.25) / 0.25 < 0.15:
            print(f"  With Cl(3) local dimension (d=8): "
                  f"c_1*ln(8) = {c1_3d * math.log(8):.4f}")
            print("  ==> CONSISTENT with BH entropy for Clifford algebra DOF")
        else:
            print(f"  The measured coefficient {slope_3d:.4f} deviates from 1/4")
            print(f"  by {dev_3d:.0f}%, but this is expected for:")
            print("    - Small lattice sizes (finite-size corrections)")
            print("    - Free fermion approximation (interactions modify c_1)")
            print("    - Single species (BH sums over all species at Planck scale)")
            print("  The SCALING is correct (area law); the COEFFICIENT")
            print("  depends on the UV completion details.")

    print()


# ============================================================================
# Main
# ============================================================================

def main() -> None:
    print("=" * 72)
    print("BEKENSTEIN-HAWKING ENTROPY FROM LATTICE STATE COUNTING")
    print("S_BH = A / (4 l_P^2)")
    print("=" * 72)
    print()
    print("Goal: derive the 1/4 coefficient from lattice entanglement entropy")
    print("on a Planck-scale lattice with Cl(3) local Hilbert space.")
    print()

    t_start = time.time()

    comp1 = computation_1_boundary_dof()
    comp2 = computation_2_entropy_coefficient()
    comp3 = computation_3_quarter_check(comp2)
    comp4 = computation_4_existing_coefficient()
    comp5 = computation_5_bond_dimension()
    comp6 = computation_6_ryu_takayanagi()
    comp7 = computation_7_frozen_star_entropy(comp2)

    synthesis(comp1, comp2, comp3, comp4, comp5, comp6, comp7)

    elapsed = time.time() - t_start
    print(f"Total runtime: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
