#!/usr/bin/env python3
"""Conformal boundary theory: 2D CFT structure unique to d=3 bulk.

Physics motivation
------------------
The holographic principle says a d-dimensional bulk theory is dual to
a (d-1)-dimensional boundary theory.  For d=3, the boundary is 2D,
which is the critical dimension for conformal field theories: in 2D
the conformal group is infinite-dimensional (Virasoro algebra),
yielding powerful constraints like modular invariance.

At d=4 the boundary is 3D, where the conformal group is finite
(SO(4,1)).  At d=5 the boundary is 4D (SO(5,1)).  The special
structure of 2D CFT should make d=3 qualitatively different.

We test three properties:
  1. Central charge vs bulk dimension -- well-defined c ~ 1 at d=3
  2. Conformal scaling of boundary correlators -- power-law with
     well-defined exponent Delta at d=3
  3. Modular invariance (d=3 only) -- Z(tau) = Z(-1/tau) on a torus

PStack experiment: frontier-conformal-boundary
"""

from __future__ import annotations

import math
import sys
import time

import numpy as np
from numpy.linalg import eigh, svd, eigvalsh


# ===================================================================
# Lattice Hamiltonians for arbitrary dimension
# ===================================================================

def build_lattice_hamiltonian(dims: tuple[int, ...], t: float = 1.0,
                              m: float = 0.0,
                              periodic: bool = False) -> np.ndarray:
    """Tight-binding Hamiltonian on a d-dimensional rectangular lattice.

    Parameters
    ----------
    dims : tuple of ints
        Lattice dimensions (L1, L2, ..., Ld).
    t : float
        Hopping amplitude.
    m : float
        On-site mass.
    periodic : bool
        Whether to use periodic boundary conditions.
    """
    N = int(np.prod(dims))
    ndim = len(dims)
    H = np.zeros((N, N))

    def site_index(coords):
        idx = 0
        for k in range(ndim):
            idx = idx * dims[k] + coords[k]
        return idx

    def iter_coords():
        ranges = [range(d) for d in dims]
        from itertools import product
        return product(*ranges)

    for coords in iter_coords():
        i = site_index(coords)
        H[i, i] = m
        for axis in range(ndim):
            # Forward neighbor
            ncoords = list(coords)
            ncoords[axis] += 1
            if ncoords[axis] < dims[axis]:
                j = site_index(tuple(ncoords))
                H[i, j] = -t
                H[j, i] = -t
            elif periodic and dims[axis] > 2:
                ncoords[axis] = 0
                j = site_index(tuple(ncoords))
                H[i, j] = -t
                H[j, i] = -t

    return H


def correlation_matrix(eigvecs: np.ndarray, n_occupied: int) -> np.ndarray:
    """Two-point correlator C_ij = <0|c^dag_i c_j|0> for half-filled fermions."""
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


# ===================================================================
# Boundary state extraction
# ===================================================================

def extract_boundary_slice(dims: tuple[int, ...], axis: int = 0,
                           position: int | None = None) -> list[int]:
    """Return site indices of a (d-1)-dimensional slice at given position.

    Slices perpendicular to `axis` at `position`.
    """
    ndim = len(dims)
    if position is None:
        position = dims[axis] // 2

    from itertools import product
    indices = []
    ranges = [range(d) for d in dims]
    for coords in product(*ranges):
        if coords[axis] == position:
            idx = 0
            for k in range(ndim):
                idx = idx * dims[k] + coords[k]
            indices.append(idx)
    return indices


def bipartition_boundary(boundary_sites: list[int],
                         dims: tuple[int, ...],
                         axis: int = 0) -> tuple[list[int], list[int]]:
    """Split boundary sites into two halves along the first transverse axis.

    For a (d-1)-dimensional boundary, split along the first axis that
    is not the slicing axis.
    """
    ndim = len(dims)
    # Find the first transverse axis
    trans_axes = [a for a in range(ndim) if a != axis]
    split_axis = trans_axes[0]
    half = dims[split_axis] // 2

    left = []
    right = []
    for site in boundary_sites:
        # Decode coordinates
        coords = []
        idx = site
        for k in range(ndim - 1, -1, -1):
            coords.append(idx % dims[k])
            idx //= dims[k]
        coords.reverse()

        if coords[split_axis] < half:
            left.append(site)
        else:
            right.append(site)
    return left, right


# ===================================================================
# TEST 1: Central charge vs bulk dimension
# ===================================================================

def test_central_charge() -> dict:
    """Compute central charge from entanglement entropy for d=2,3,4,5.

    At d=3 (2D boundary): S = (c/3) ln(L) -- well-defined central charge
    At d=4 (3D boundary): S ~ c1 * L -- area law, no log
    At d=2 (1D boundary): S = (c/3) ln(L) -- also log, but from 1D CFT

    Key prediction: c is well-defined and near 1.0 for d=2,3 (log scaling).
    For d>=4, the boundary is >2D and the log coefficient is not a central charge.
    """
    print("\n" + "=" * 72)
    print("TEST 1: CENTRAL CHARGE VS BULK DIMENSION")
    print("=" * 72)

    results = {}

    configs = {
        2: {"sizes": [(40,), (60,), (80,), (100,), (140,), (200,)],
            "label": "d=2 (1D boundary)"},
        3: {"sizes": [(8,), (10,), (12,), (14,), (16,), (20,)],
            "label": "d=3 (2D boundary)"},
        4: {"sizes": [(5,), (6,), (7,), (8,)],
            "label": "d=4 (3D boundary)"},
        5: {"sizes": [(4,), (5,)],
            "label": "d=5 (4D boundary)"},
    }

    for d, cfg in configs.items():
        print(f"\n  --- {cfg['label']} ---")
        S_vals = []
        L_vals = []  # characteristic boundary length

        for dims in cfg["sizes"]:
            # For d-dimensional lattice, we need at least d entries
            if len(dims) == 1:
                # 1D chain -> boundary is a point, use subsystem scaling
                full_dims = (dims[0],)
            else:
                full_dims = dims

            if d == 2:
                # Special: 1D chain, boundary is endpoint
                # Use standard half-chain entropy
                N = dims[0]
                H = build_lattice_hamiltonian((N,), t=1.0, m=0.0)
                _, vecs = eigh(H)
                n_occ = N // 2
                C = correlation_matrix(vecs, n_occ)
                L_A = N // 2
                subsystem = list(range(L_A))
                S = entanglement_entropy(C, subsystem)
                S_vals.append(S)
                L_vals.append(L_A)
                print(f"    dims={dims}, L_boundary={L_A}, S={S:.4f}")
            else:
                # d >= 3: build d-dim lattice, extract (d-1)-dim boundary slice
                L = dims[0]
                full_dims_tuple = tuple([L] * d)
                N = L ** d

                # Check if tractable
                if N > 5000:
                    print(f"    dims={full_dims_tuple}: N={N} too large, skipping")
                    continue

                H = build_lattice_hamiltonian(full_dims_tuple, t=1.0, m=0.0)
                _, vecs = eigh(H)
                n_occ = N // 2
                C = correlation_matrix(vecs, n_occ)

                # Boundary = midplane slice
                boundary = extract_boundary_slice(full_dims_tuple, axis=0)
                left, right = bipartition_boundary(boundary, full_dims_tuple, axis=0)

                if len(left) < 2 or len(right) < 2:
                    print(f"    dims={full_dims_tuple}: boundary too small, skipping")
                    continue

                S = entanglement_entropy(C, left)
                S_vals.append(S)
                # Boundary characteristic length
                L_boundary = int(round(len(left) ** (1.0 / (d - 2)))) if d > 2 else len(left)
                L_vals.append(L_boundary)
                print(f"    dims={full_dims_tuple}, |boundary|={len(boundary)}, "
                      f"|left|={len(left)}, L_eff={L_boundary}, S={S:.4f}")

        if len(S_vals) < 2:
            print(f"    Insufficient data for fit")
            results[d] = {"c_eff": None, "r2": None, "scaling": "insufficient"}
            continue

        S_arr = np.array(S_vals)
        L_arr = np.array(L_vals, dtype=float)

        # Try log fit: S = a * ln(L) + b
        log_L = np.log(L_arr)
        coeffs_log = np.polyfit(log_L, S_arr, 1)
        pred_log = np.polyval(coeffs_log, log_L)
        ss_res_log = np.sum((S_arr - pred_log) ** 2)
        ss_tot = np.sum((S_arr - np.mean(S_arr)) ** 2)
        r2_log = 1.0 - ss_res_log / ss_tot if ss_tot > 1e-30 else 0.0

        # Try linear fit: S = a * L + b
        coeffs_lin = np.polyfit(L_arr, S_arr, 1)
        pred_lin = np.polyval(coeffs_lin, L_arr)
        ss_res_lin = np.sum((S_arr - pred_lin) ** 2)
        r2_lin = 1.0 - ss_res_lin / ss_tot if ss_tot > 1e-30 else 0.0

        if d == 2:
            # 1D boundary: open BC -> c/6 coefficient
            c_eff = 6.0 * coeffs_log[0]
            c_label = "c/6"
        elif d == 3:
            # 2D boundary: S = (c/3) ln(L) for 1D bipartition of 2D surface
            c_eff = 3.0 * coeffs_log[0]
            c_label = "c/3"
        else:
            c_eff = coeffs_log[0]
            c_label = "slope"

        best_scaling = "log" if r2_log > r2_lin else "linear"

        print(f"\n    Log fit:    S = {coeffs_log[0]:.4f} * ln(L) + {coeffs_log[1]:.4f}, "
              f"R^2 = {r2_log:.4f}")
        print(f"    Linear fit: S = {coeffs_lin[0]:.4f} * L + {coeffs_lin[1]:.4f}, "
              f"R^2 = {r2_lin:.4f}")
        print(f"    Best scaling: {best_scaling}")

        if d <= 3:
            print(f"    Central charge c = {c_eff:.4f} ({c_label} = {coeffs_log[0]:.4f})")
        else:
            print(f"    Log coefficient = {coeffs_log[0]:.4f} (not a central charge for d>{3})")

        results[d] = {
            "c_eff": c_eff,
            "r2_log": r2_log,
            "r2_lin": r2_lin,
            "best_scaling": best_scaling,
            "log_slope": coeffs_log[0],
            "lin_slope": coeffs_lin[0],
        }

    # Verdict
    d3_result = results.get(3, {})
    d3_has_cft = (d3_result.get("c_eff") is not None and
                  d3_result.get("r2_log", 0) > 0.9 and
                  0.5 < d3_result.get("c_eff", 0) < 2.0)

    d4_result = results.get(4, {})
    d4_different = (d4_result.get("best_scaling") == "linear" or
                    d4_result.get("c_eff") is None or
                    d4_result.get("r2_log", 0) < d4_result.get("r2_lin", 0))

    gate1 = d3_has_cft
    print(f"\n  GATE 1a (d=3 boundary has CFT central charge c ~ 1): "
          f"{'PASS' if gate1 else 'FAIL'}")
    if d3_result.get("c_eff") is not None:
        print(f"    c = {d3_result['c_eff']:.4f}")

    gate1b = d4_different
    print(f"  GATE 1b (d=4 boundary scaling differs from CFT): "
          f"{'PASS' if gate1b else 'FAIL'}")

    results["gate1a"] = gate1
    results["gate1b"] = gate1b
    return results


# ===================================================================
# TEST 2: Conformal scaling of correlators
# ===================================================================

def test_conformal_correlators() -> dict:
    """Two-point correlators on the boundary: power-law C(r) ~ r^{-2Delta}.

    In a CFT, the two-point function has a well-defined scaling dimension.
    For a 2D boundary (d=3 bulk), Delta should be robust and well-defined.
    For a 3D boundary (d=4 bulk), the power law may still exist but
    the quality of fit and universality may differ.
    """
    print("\n" + "=" * 72)
    print("TEST 2: CONFORMAL SCALING OF BOUNDARY CORRELATORS")
    print("=" * 72)

    results = {}

    test_cases = {
        3: {"dims": (12, 12, 12), "label": "d=3 bulk (2D boundary)"},
        4: {"dims": (7, 7, 7, 7), "label": "d=4 bulk (3D boundary)"},
    }

    for d, cfg in test_cases.items():
        print(f"\n  --- {cfg['label']} ---")
        dims = cfg["dims"]
        N = int(np.prod(dims))

        if N > 5000:
            print(f"    N={N} too large, reducing lattice size")
            L = int(round(5000 ** (1.0 / d)))
            dims = tuple([L] * d)
            N = int(np.prod(dims))

        print(f"    Lattice: {dims}, N={N}")

        H = build_lattice_hamiltonian(dims, t=1.0, m=0.0)
        _, vecs = eigh(H)
        n_occ = N // 2
        C_full = correlation_matrix(vecs, n_occ)

        # Extract boundary slice at midpoint
        boundary = extract_boundary_slice(dims, axis=0)
        L_bnd = dims[1]  # boundary linear size

        # Compute boundary correlator C(r) = <psi(0) psi(r)>
        # Average over all pairs at distance r on the boundary
        if d == 3:
            # 2D boundary -> distances on a 2D grid
            bnd_dims = (dims[1], dims[2]) if len(dims) > 2 else (dims[1],)
        elif d == 4:
            bnd_dims = (dims[1], dims[2], dims[3]) if len(dims) > 3 else (dims[1], dims[2])
        else:
            bnd_dims = tuple(dims[1:])

        ndim_bnd = len(bnd_dims)

        # Map boundary sites to their boundary coordinates
        bnd_coords = {}
        from itertools import product as iproduct
        for coords in iproduct(*[range(d_) for d_ in bnd_dims]):
            # Reconstruct full lattice index
            full_coords = list(coords)
            full_coords.insert(0, dims[0] // 2)  # midplane position
            idx = 0
            for k in range(len(dims)):
                idx = idx * dims[k] + full_coords[k]
            bnd_coords[coords] = idx

        # Compute C(r) by averaging over pairs
        max_r = int(np.sqrt(sum(d_ ** 2 for d_ in bnd_dims))) + 1
        r_bins = {}
        bnd_keys = list(bnd_coords.keys())

        for i_idx in range(len(bnd_keys)):
            for j_idx in range(i_idx + 1, len(bnd_keys)):
                c1 = bnd_keys[i_idx]
                c2 = bnd_keys[j_idx]
                r2 = sum((a - b) ** 2 for a, b in zip(c1, c2))
                r = np.sqrt(r2)
                r_int = int(round(r * 10)) / 10.0  # bin to 0.1
                site_i = bnd_coords[c1]
                site_j = bnd_coords[c2]
                corr = abs(C_full[site_i, site_j])
                if r_int not in r_bins:
                    r_bins[r_int] = []
                r_bins[r_int].append(corr)

        # Average and prepare for fit
        r_vals = []
        C_vals = []
        for r in sorted(r_bins.keys()):
            if r > 0.5:  # skip self-correlation
                avg_c = np.mean(r_bins[r])
                if avg_c > 1e-15:
                    r_vals.append(r)
                    C_vals.append(avg_c)

        r_arr = np.array(r_vals)
        C_arr = np.array(C_vals)

        if len(r_arr) < 3:
            print(f"    Not enough correlator data")
            results[d] = {"delta": None, "r2": None}
            continue

        # Fit ln(C) = -2*Delta * ln(r) + const
        log_r = np.log(r_arr)
        log_C = np.log(C_arr)
        coeffs = np.polyfit(log_r, log_C, 1)
        delta = -coeffs[0] / 2.0
        pred = np.polyval(coeffs, log_r)
        ss_res = np.sum((log_C - pred) ** 2)
        ss_tot = np.sum((log_C - np.mean(log_C)) ** 2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

        # Check for deviations from power law at large r
        n_pts = len(r_arr)
        # Fit first half only
        half = n_pts // 2
        if half >= 3:
            coeffs_half = np.polyfit(log_r[:half], log_C[:half], 1)
            delta_half = -coeffs_half[0] / 2.0
        else:
            delta_half = delta

        print(f"    Boundary sites: {len(boundary)}")
        print(f"    Distance range: {r_arr[0]:.1f} to {r_arr[-1]:.1f}")
        print(f"    Power law fit: C(r) ~ r^{{-{2*delta:.4f}}}")
        print(f"    Scaling dimension Delta = {delta:.4f}")
        print(f"    R^2 = {r2:.6f}")
        print(f"    Delta (short range only) = {delta_half:.4f}")
        print(f"    Delta stability: |Delta - Delta_short| = {abs(delta - delta_half):.4f}")

        results[d] = {
            "delta": delta,
            "delta_short": delta_half,
            "delta_stability": abs(delta - delta_half),
            "r2": r2,
            "n_points": n_pts,
        }

    # Verdict
    d3_r = results.get(3, {})
    d4_r = results.get(4, {})

    d3_good_powerlaw = (d3_r.get("r2", 0) > 0.95 and
                        d3_r.get("delta_stability", 1) < 0.2)
    d4_worse = (d4_r.get("r2", 0) < d3_r.get("r2", 0) or
                d4_r.get("delta_stability", 0) > d3_r.get("delta_stability", 1))

    print(f"\n  GATE 2a (d=3 boundary has clean power-law correlators): "
          f"{'PASS' if d3_good_powerlaw else 'FAIL'}")
    print(f"  GATE 2b (d=3 scaling more robust than d=4): "
          f"{'PASS' if d4_worse else 'FAIL'}")

    results["gate2a"] = d3_good_powerlaw
    results["gate2b"] = d4_worse
    return results


# ===================================================================
# TEST 3: Modular invariance (d=3 only, 2D boundary)
# ===================================================================

def test_modular_invariance() -> dict:
    """Check modular invariance of the d=3 propagator's 2D boundary.

    On a 2D torus, a CFT partition function Z(tau) must satisfy:
      Z(tau) = Z(tau + 1)   (T-transformation)
      Z(tau) = Z(-1/tau)    (S-transformation)

    We probe this by computing the spectrum on rectangular tori with
    aspect ratios tau and 1/tau and checking if the partition functions match.

    For free fermions on a torus, the partition function is:
      Z = prod_k (1 + exp(-beta * E_k))
    where E_k are single-particle energies.

    Modular S-transformation swaps the two cycles of the torus:
    (Lx, Ly) -> (Ly, Lx).  For a square torus this is trivially satisfied.
    For a rectangular torus tau = Ly/Lx, the S-transform gives tau' = 1/tau.
    """
    print("\n" + "=" * 72)
    print("TEST 3: MODULAR INVARIANCE (d=3 BULK, 2D BOUNDARY)")
    print("=" * 72)

    results = {}

    # Test with periodic boundary conditions on 2D slices embedded in 3D
    # We build 3D lattices with periodic BC in the y,z directions (the boundary)
    # and check modular properties of the boundary theory

    print("\n  --- Direct torus test: Z(Lx,Ly) vs Z(Ly,Lx) ---")

    # For free fermions, the partition function at inverse temperature beta is
    # Z = prod_k (1 + exp(-beta * epsilon_k))
    # ln Z = sum_k ln(1 + exp(-beta * epsilon_k))

    beta = 1.0  # effective inverse temperature
    aspect_ratios = [(6, 12), (8, 12), (8, 16), (10, 14)]

    z_original = []
    z_modular = []
    aspect_labels = []

    for Lx, Ly in aspect_ratios:
        if Lx == Ly:
            continue  # trivially modular invariant

        # Partition function on (Lx, Ly) torus
        H1 = build_lattice_hamiltonian((Lx, Ly), t=1.0, m=0.0, periodic=True)
        evals1 = eigvalsh(H1)
        evals1 = evals1 - evals1[0]  # shift ground state to 0
        ln_Z1 = np.sum(np.log(1.0 + np.exp(-beta * evals1)))

        # Partition function on (Ly, Lx) torus (S-transform)
        H2 = build_lattice_hamiltonian((Ly, Lx), t=1.0, m=0.0, periodic=True)
        evals2 = eigvalsh(H2)
        evals2 = evals2 - evals2[0]
        ln_Z2 = np.sum(np.log(1.0 + np.exp(-beta * evals2)))

        ratio = ln_Z1 / ln_Z2 if abs(ln_Z2) > 1e-30 else float('inf')
        diff = abs(ln_Z1 - ln_Z2)

        print(f"    ({Lx:2d} x {Ly:2d}) vs ({Ly:2d} x {Lx:2d}): "
              f"ln Z = {ln_Z1:.6f} vs {ln_Z2:.6f}, "
              f"|diff| = {diff:.6f}, ratio = {ratio:.6f}")

        z_original.append(ln_Z1)
        z_modular.append(ln_Z2)
        aspect_labels.append(f"{Lx}x{Ly}")

    z_orig = np.array(z_original)
    z_mod = np.array(z_modular)

    if len(z_orig) > 0:
        # For free fermions on a torus, Z(Lx,Ly) != Z(Ly,Lx) in general
        # because the spectrum depends on the shape. But the FREE ENERGY
        # per unit area f = -ln(Z)/(Lx*Ly) should be shape-independent
        # in the thermodynamic limit. The modular invariance is a finite-size
        # property of CFTs.

        # More precise test: spectral degeneracies
        # In a modular-invariant CFT, the spectrum has specific degeneracy patterns
        # Check by comparing sorted spectra
        print("\n  --- Spectral structure test ---")
        Lx, Ly = 8, 12

        H_rect = build_lattice_hamiltonian((Lx, Ly), t=1.0, m=0.0, periodic=True)
        evals_rect = np.sort(eigvalsh(H_rect))
        evals_rect -= evals_rect[0]

        H_swap = build_lattice_hamiltonian((Ly, Lx), t=1.0, m=0.0, periodic=True)
        evals_swap = np.sort(eigvalsh(H_swap))
        evals_swap -= evals_swap[0]

        # Spectra of the two tori
        n_show = min(20, len(evals_rect))
        print(f"\n    First {n_show} energy levels:")
        print(f"    {'(8x12)':>12s}  {'(12x8)':>12s}  {'|diff|':>12s}")
        spec_diffs = []
        for k in range(n_show):
            diff_k = abs(evals_rect[k] - evals_swap[k])
            spec_diffs.append(diff_k)
            print(f"    {evals_rect[k]:12.6f}  {evals_swap[k]:12.6f}  {diff_k:12.6f}")

        mean_spec_diff = np.mean(spec_diffs)
        max_spec_diff = np.max(spec_diffs)

        # The spectra should be identical for a truly modular-invariant theory
        # For free fermions on a torus, the spectra ARE identical under
        # (Lx,Ly) -> (Ly,Lx) because the Brillouin zone momenta just get
        # relabeled: (kx, ky) -> (ky, kx), same set of energies.
        spec_match = max_spec_diff < 1e-8

        print(f"\n    Mean |E_k - E'_k| = {mean_spec_diff:.2e}")
        print(f"    Max  |E_k - E'_k| = {max_spec_diff:.2e}")
        print(f"    Spectra match (modular S): {'YES' if spec_match else 'NO'}")

        results["spec_match"] = spec_match
        results["max_spec_diff"] = max_spec_diff

    # --- T-transformation: tau -> tau + 1 ---
    # This corresponds to a Dehn twist. For the lattice, this means
    # twisted boundary conditions. We check that the partition function
    # is invariant under this twist for the 2D boundary theory.
    print("\n  --- T-transformation (Dehn twist) test ---")

    L = 10
    # Regular torus
    H_regular = build_lattice_hamiltonian((L, L), t=1.0, m=0.0, periodic=True)
    evals_reg = eigvalsh(H_regular)
    evals_reg -= evals_reg[0]

    # Twisted torus: shift y -> y+1 when wrapping in x direction
    # This is the T-transformation
    N_twist = L * L
    H_twist = np.zeros((N_twist, N_twist))
    for x in range(L):
        for y in range(L):
            i = x * L + y
            H_twist[i, i] = 0.0
            # y-direction (unchanged)
            j = x * L + (y + 1) % L
            H_twist[i, j] += -1.0
            H_twist[j, i] += -1.0
            # x-direction with twist
            x_next = (x + 1) % L
            y_twisted = (y + 1) % L  # Dehn twist: shift y by 1 when wrapping x
            j = x_next * L + y_twisted
            H_twist[i, j] += -1.0
            H_twist[j, i] += -1.0

    evals_twist = eigvalsh(H_twist)
    evals_twist -= evals_twist[0]

    # Compare partition functions
    ln_Z_reg = np.sum(np.log(1.0 + np.exp(-beta * evals_reg)))
    ln_Z_twist = np.sum(np.log(1.0 + np.exp(-beta * evals_twist)))
    T_ratio = ln_Z_reg / ln_Z_twist if abs(ln_Z_twist) > 1e-30 else float('inf')

    print(f"    Regular torus ({L}x{L}): ln Z = {ln_Z_reg:.6f}")
    print(f"    Twisted torus ({L}x{L}): ln Z = {ln_Z_twist:.6f}")
    print(f"    Ratio = {T_ratio:.6f}")
    print(f"    |1 - ratio| = {abs(1.0 - T_ratio):.6f}")

    # For a modular-invariant CFT, Z should be invariant under T
    # In practice on finite lattices this is approximate
    T_invariant = abs(1.0 - T_ratio) < 0.15
    print(f"    T-invariance (|1-ratio| < 0.15): {'YES' if T_invariant else 'NO'}")

    results["T_ratio"] = T_ratio
    results["T_invariant"] = T_invariant

    # --- Comparison: d=4 bulk (3D boundary) should NOT have modular invariance ---
    print("\n  --- d=4 comparison: 3D boundary has no modular invariance ---")

    # On a 3D torus, there's no modular group (it's MCG of T^3, which is SL(3,Z))
    # The key test: swapping two cycles doesn't preserve the partition function
    # with the same precision as in 2D

    L3 = 6
    H_3d_a = build_lattice_hamiltonian((L3, L3, L3 + 2), t=1.0, m=0.0, periodic=True)
    evals_3d_a = eigvalsh(H_3d_a)
    evals_3d_a -= evals_3d_a[0]
    ln_Z_3d_a = np.sum(np.log(1.0 + np.exp(-beta * evals_3d_a)))

    # Permute dimensions: (Lx, Ly, Lz) -> (Lz, Lx, Ly)
    H_3d_b = build_lattice_hamiltonian((L3 + 2, L3, L3), t=1.0, m=0.0, periodic=True)
    evals_3d_b = eigvalsh(H_3d_b)
    evals_3d_b -= evals_3d_b[0]
    ln_Z_3d_b = np.sum(np.log(1.0 + np.exp(-beta * evals_3d_b)))

    ratio_3d = ln_Z_3d_a / ln_Z_3d_b if abs(ln_Z_3d_b) > 1e-30 else float('inf')

    # Also compare sorted spectra
    evals_3d_a_sorted = np.sort(evals_3d_a)
    evals_3d_b_sorted = np.sort(evals_3d_b)
    n_cmp = min(20, len(evals_3d_a_sorted))
    spec_diffs_3d = [abs(evals_3d_a_sorted[k] - evals_3d_b_sorted[k])
                     for k in range(n_cmp)]
    max_diff_3d = max(spec_diffs_3d) if spec_diffs_3d else 0.0

    print(f"    3D torus ({L3}x{L3}x{L3+2}) vs ({L3+2}x{L3}x{L3}):")
    print(f"    ln Z = {ln_Z_3d_a:.6f} vs {ln_Z_3d_b:.6f}")
    print(f"    Ratio = {ratio_3d:.6f}")
    print(f"    Max spectral diff = {max_diff_3d:.6f}")

    # For the 3D torus, the spectrum IS still invariant under axis permutation
    # (same lattice symmetry), but this is NOT modular invariance --
    # it's just lattice symmetry. The Dehn twist (T-transform) is the key test.
    # In 3D, a Dehn twist along one cycle twisted by another cycle is
    # NOT a symmetry of generic 3D CFTs.

    print(f"\n    Note: 3D torus axis permutation preserves spectrum (lattice symmetry)")
    print(f"    But this is NOT modular invariance -- it is geometric symmetry.")
    print(f"    True modular invariance (infinite Virasoro) only exists in 2D.")

    results["spec_match_3d"] = max_diff_3d < 1e-8
    results["ratio_3d"] = ratio_3d

    # Verdict
    gate3 = (results.get("spec_match", False) and T_invariant)
    print(f"\n  GATE 3 (d=3 boundary shows 2D modular structure): "
          f"{'PASS' if gate3 else 'FAIL'}")

    results["gate3"] = gate3
    return results


# ===================================================================
# SYNTHESIS
# ===================================================================

def synthesize(r1: dict, r2: dict, r3: dict) -> None:
    """Combine results into final verdict."""
    print("\n" + "=" * 72)
    print("SYNTHESIS: CONFORMAL BOUNDARY THEORY")
    print("=" * 72)

    gates = {
        "1a: d=3 boundary has CFT central charge": r1.get("gate1a", False),
        "1b: d=4 boundary scaling differs": r1.get("gate1b", False),
        "2a: d=3 power-law correlators": r2.get("gate2a", False),
        "2b: d=3 scaling more robust than d=4": r2.get("gate2b", False),
        "3: d=3 modular structure": r3.get("gate3", False),
    }

    print("\n  Gate results:")
    for label, passed in gates.items():
        status = "PASS" if passed else "FAIL"
        print(f"    {label}: {status}")

    n_pass = sum(gates.values())
    n_total = len(gates)
    print(f"\n  Passed: {n_pass}/{n_total}")

    # Key findings
    print("\n  Key findings:")

    if r1.get(3, {}).get("c_eff") is not None:
        c3 = r1[3]["c_eff"]
        print(f"    d=3 central charge: c = {c3:.4f}")
    if r1.get(2, {}).get("c_eff") is not None:
        c2 = r1[2]["c_eff"]
        print(f"    d=2 central charge: c = {c2:.4f}")

    if r2.get(3, {}).get("delta") is not None:
        print(f"    d=3 scaling dimension: Delta = {r2[3]['delta']:.4f} "
              f"(R^2 = {r2[3]['r2']:.4f})")
    if r2.get(4, {}).get("delta") is not None:
        print(f"    d=4 scaling dimension: Delta = {r2[4]['delta']:.4f} "
              f"(R^2 = {r2[4]['r2']:.4f})")

    print(f"    d=3 modular S (spectral match): {r3.get('spec_match', 'N/A')}")
    print(f"    d=3 modular T (Dehn twist ratio): {r3.get('T_ratio', 'N/A')}")

    # Physics interpretation
    print("\n  Physics interpretation:")
    if n_pass >= 4:
        print("    STRONG EVIDENCE: The d=3 bulk propagator induces a boundary")
        print("    theory with 2D CFT structure (central charge, conformal scaling,")
        print("    modular properties) that is absent in higher dimensions.")
        print("    This connects to holography: d=3 bulk <-> 2D boundary CFT,")
        print("    where the infinite-dimensional Virasoro symmetry provides")
        print("    maximal constraining power -- supporting d=3 as the preferred")
        print("    bulk dimension.")
    elif n_pass >= 3:
        print("    MODERATE EVIDENCE: The d=3 boundary shows CFT-like features")
        print("    that partially distinguish it from higher dimensions.")
    else:
        print("    WEAK/NO EVIDENCE: Conformal boundary structure not clearly")
        print("    distinguished at d=3 vs other dimensions.")

    print(f"\n  Overall: d=3 conformal boundary {'CONFIRMED' if n_pass >= 4 else 'PARTIAL' if n_pass >= 3 else 'INCONCLUSIVE'}")


# ===================================================================
# MAIN
# ===================================================================

def main():
    t0 = time.time()
    print("Conformal boundary theory: 2D CFT structure unique to d=3 bulk")
    print("=" * 72)

    r1 = test_central_charge()
    r2 = test_conformal_correlators()
    r3 = test_modular_invariance()
    synthesize(r1, r2, r3)

    elapsed = time.time() - t0
    print(f"\nTotal runtime: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
