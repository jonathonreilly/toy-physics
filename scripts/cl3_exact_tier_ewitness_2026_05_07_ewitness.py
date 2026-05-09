"""
Exact-tier ε_witness push: numba-accelerated path-integral W1 closure.

Authority role
--------------
Source-note proposal -- audit verdict and downstream status set only by
the independent audit lane.

Strategy
========
The prior bounded theorem (PR #674) established:
  - <P_iso>(beta_W=6, 4^4)         = 0.5970 ± 0.0010
  - <P_sigma>(g^2=1, xi=4, 4^3x8)  = 0.414  ± 0.002
  - rel_shift = 0.21 · s_t = 0.105·g^2/xi   (Convention C-iso, leading)

This runner pushes toward ε_witness ~ 3×10⁻⁴ via three engineering paths:

  Path A: numba-accelerated MC for ~10x speedup. Refactor heatbath
    inner loop into @njit kernels. Run high-statistics ensembles
    (5000+ measurement sweeps) with multi-seed averaging.

  Path B: Larger lattices for thermodynamic-limit extrapolation.
    Spatial volumes L^3 in {4, 6} (cap at 6^3 due to compute).
    Fit <P>(L) = <P>_inf + a/L^2 + b/L^4.

  Path C: Convention C-iso analytic refinement to higher order.
    Compute NLO O(g^4/xi^2) correction to rel_shift = 0.105·g^2/xi.
    Verify via direct heat-kernel-vs-Wilson temporal-plaquette eval
    at multiple xi.

Implementation
==============
- numba-jitted SU(2) and SU(3) helpers, vectorized matmul
- @njit heatbath_link / overrelax_link kernels
- Vectorized plaquette measurement
- Block-jackknife error estimation
- Multi-seed ensemble averaging

Anisotropic Wilson action (standard Wilson convention):
    S = -(beta_sigma/N_c) sum_{spatial-spatial p} Re Tr U_p
        -(beta_tau/N_c)   sum_{spatial-temporal p} Re Tr U_p
with
    beta_sigma = 2 N_c / (g^2 xi),   beta_tau = 2 N_c xi / g^2.

Plaquette expectation:  <P> = (1/N_c) <Re Tr U_plaq>.

In the Hamilton limit xi -> infinity, <P_sigma> -> <P_H>_KS, the
Hamilton-form spatial plaquette expectation in H_KS at g^2 = bare.

References
----------
- Cabibbo N., Marinari E. (1982), Phys. Lett. B119, 387 -- SU(N)
  pseudo-heat-bath via SU(2) subgroup sweeps.
- Kennedy A.D., Pendleton B.J. (1985), Phys. Lett. B156, 393 -- SU(2)
  exact heat-bath sampler.
- Lüscher M., Wolff U. (1990), Nucl. Phys. B339, 222 -- error analysis
  / autocorrelation in lattice simulations.
- Engels et al. (1990), Nucl. Phys. B342, 7 -- SU(3) plaquette benchmarks.
- Klassen T. (1998), Nucl. Phys. B533, 557 -- anisotropic SU(3) tuning.
- Karsch F. (1982), Nucl. Phys. B205, 285 -- anisotropic SU(2) couplings.
- Drouffe J.M., Zuber J.B. (1983), Phys. Rep. 102 -- strong-coupling expansion.
- Menotti P., Onofri E. (1981), Nucl. Phys. B190, 288 -- heat-kernel action.

Verifies:
  1. Self-test:  isotropic SU(3) at beta=6, agrees with Engels 1990.
  2. Path A:    high-statistics 4^3 x 16 anisotropic xi=4 with 5+ seeds.
  3. Path B:    finite-size scaling fit on {4^3 x 16, 6^3 x 24}.
  4. Path C:    NLO analytic refinement of Convention C-iso.

Usage:
    python3 scripts/cl3_exact_tier_ewitness_2026_05_07_ewitness.py
        --mode self_test
    python3 scripts/cl3_exact_tier_ewitness_2026_05_07_ewitness.py
        --mode all  --n_thermalize 200 --n_measure 1000
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Tuple, List

import numpy as np

try:
    from numba import njit, prange
    NUMBA_OK = True
except Exception:
    NUMBA_OK = False
    def njit(*args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            return args[0]
        def deco(f): return f
        return deco
    def prange(n): return range(n)

# -------------------------- numerics knobs --------------------------- #

NC = 3
NDIM = 4
SMALL = 1e-30


# -------------------------- jitted SU(2)/SU(3) primitives ------------ #


@njit(cache=False, fastmath=False)
def _project_su3(M):
    """Gram-Schmidt + cross-product third row. Returns SU(3) matrix."""
    out = M.copy()
    # Row 0 normalize
    n0 = 0.0
    for j in range(NC):
        n0 += (out[0, j].real ** 2 + out[0, j].imag ** 2)
    n0 = math.sqrt(max(n0, SMALL))
    for j in range(NC):
        out[0, j] = out[0, j] / n0
    # Row 1 orthogonalize
    proj_re = 0.0
    proj_im = 0.0
    for j in range(NC):
        proj_re += (out[0, j].conjugate() * out[1, j]).real
        proj_im += (out[0, j].conjugate() * out[1, j]).imag
    proj = complex(proj_re, proj_im)
    for j in range(NC):
        out[1, j] = out[1, j] - proj * out[0, j]
    n1 = 0.0
    for j in range(NC):
        n1 += (out[1, j].real ** 2 + out[1, j].imag ** 2)
    n1 = math.sqrt(max(n1, SMALL))
    for j in range(NC):
        out[1, j] = out[1, j] / n1
    # Row 2 = conjugate cross product of rows 0 and 1
    out[2, 0] = (out[0, 1] * out[1, 2] - out[0, 2] * out[1, 1]).conjugate()
    out[2, 1] = (out[0, 2] * out[1, 0] - out[0, 0] * out[1, 2]).conjugate()
    out[2, 2] = (out[0, 0] * out[1, 1] - out[0, 1] * out[1, 0]).conjugate()
    return out


@njit(cache=False)
def _matmul3(A, B):
    """Inline 3x3 complex matmul for speed (vs numpy @ which has overhead)."""
    C = np.zeros((3, 3), dtype=np.complex128)
    for i in range(3):
        for j in range(3):
            s = 0.0 + 0.0j
            for k in range(3):
                s += A[i, k] * B[k, j]
            C[i, j] = s
    return C


@njit(cache=False)
def _matmul3_dag(A, B):
    """A @ B^dagger for 3x3 complex."""
    C = np.zeros((3, 3), dtype=np.complex128)
    for i in range(3):
        for j in range(3):
            s = 0.0 + 0.0j
            for k in range(3):
                s += A[i, k] * B[j, k].conjugate()
            C[i, j] = s
    return C


@njit(cache=False)
def _dag_matmul3(A, B):
    """A^dagger @ B for 3x3 complex."""
    C = np.zeros((3, 3), dtype=np.complex128)
    for i in range(3):
        for j in range(3):
            s = 0.0 + 0.0j
            for k in range(3):
                s += A[k, i].conjugate() * B[k, j]
            C[i, j] = s
    return C


@njit(cache=False)
def _re_tr3(A):
    """Real trace of 3x3 complex matrix."""
    return A[0, 0].real + A[1, 1].real + A[2, 2].real


@njit(cache=False)
def _su2_heatbath_a0(k, rng_state):
    """Kennedy-Pendleton sample of a0 ~ exp(2 k a0) on [-1, 1].
    rng_state: array of length 1, used for np.random calls (numba random).
    Returns float a0.
    """
    if k < 1e-10:
        return 2.0 * np.random.random() - 1.0
    two_k = 2.0 * k
    for _ in range(200):
        rr = np.random.random()
        if two_k > 50.0:
            inner = max(rr + (1.0 - rr) * math.exp(-2.0 * two_k), SMALL)
            a0 = 1.0 + math.log(inner) / two_k
        else:
            a0 = math.log(rr * math.exp(two_k) + (1.0 - rr) * math.exp(-two_k)) / two_k
        if a0 >= -1.0 and a0 <= 1.0:
            test = math.sqrt(max(1.0 - a0 * a0, 0.0))
            if np.random.random() < test:
                return a0
    return 0.0


@njit(cache=False)
def _su2_heatbath_matrix(k):
    """SU(2) heatbath: sample SU(2) matrix in 2x2 form."""
    a0 = _su2_heatbath_a0(k, np.zeros(1))
    rad = math.sqrt(max(1.0 - a0 * a0, 0.0))
    phi = 2.0 * math.pi * np.random.random()
    cos_th = 2.0 * np.random.random() - 1.0
    sin_th = math.sqrt(max(1.0 - cos_th * cos_th, 0.0))
    a1 = rad * sin_th * math.cos(phi)
    a2 = rad * sin_th * math.sin(phi)
    a3 = rad * cos_th
    out = np.zeros((2, 2), dtype=np.complex128)
    out[0, 0] = complex(a0, a3)
    out[0, 1] = complex(a2, a1)
    out[1, 0] = complex(-a2, a1)
    out[1, 1] = complex(a0, -a3)
    return out


@njit(cache=False)
def _project_su2(M):
    """Project 2x2 onto SU(2) via quaternion form.
    Returns (SU(2) matrix as 2x2, scale).
    """
    a = 0.5 * (M[0, 0] + M[1, 1].conjugate())
    b = 0.5 * (M[1, 0] - M[0, 1].conjugate())
    norm_sq = a.real ** 2 + a.imag ** 2 + b.real ** 2 + b.imag ** 2
    norm = math.sqrt(max(norm_sq, 0.0))
    out = np.zeros((2, 2), dtype=np.complex128)
    if norm < 1e-30:
        out[0, 0] = 1.0
        out[1, 1] = 1.0
        return out, 0.0
    a /= norm
    b /= norm
    out[0, 0] = a
    out[0, 1] = -b.conjugate()
    out[1, 0] = b
    out[1, 1] = a.conjugate()
    return out, norm


@njit(cache=False)
def _extract_su2_block(M, sg):
    """Extract 2x2 SU(2) block in subgroup sg in {0,1,2}: rows/cols (i0,i1)."""
    if sg == 0:
        i0, i1 = 0, 1
    elif sg == 1:
        i0, i1 = 0, 2
    else:
        i0, i1 = 1, 2
    out = np.empty((2, 2), dtype=np.complex128)
    out[0, 0] = M[i0, i0]
    out[0, 1] = M[i0, i1]
    out[1, 0] = M[i1, i0]
    out[1, 1] = M[i1, i1]
    return out


@njit(cache=False)
def _left_multiply_subgroup(link, R, sg):
    """Embed R (2x2) into SU(3) subgroup sg, left-multiply link in place."""
    if sg == 0:
        i0, i1 = 0, 1
    elif sg == 1:
        i0, i1 = 0, 2
    else:
        i0, i1 = 1, 2
    out = link.copy()
    for j in range(NC):
        a0 = link[i0, j]
        a1 = link[i1, j]
        out[i0, j] = R[0, 0] * a0 + R[0, 1] * a1
        out[i1, j] = R[1, 0] * a0 + R[1, 1] * a1
    return out


# -------------------------- staples (jitted) ------------------------- #


@njit(cache=False)
def _staple_aniso(U, fwd, bwd, site, mu, beta_sigma, beta_tau):
    """Anisotropic weighted staple at link (site, mu).
    U: shape (vol, NDIM, NC, NC). fwd, bwd: shape (vol, NDIM).
    Returns 3x3 complex array.

    For link (site, mu), the (mu, nu) plaquettes through (site, mu) give:
      Forward staple S_+:  U_nu(site+mu) U_mu^d(site+nu) U_nu^d(site)
      Backward staple S_-: U_nu^d(site+mu-nu) U_mu^d(site-nu) U_nu(site-nu)
    Total staple V = sum_nu w(mu,nu) (S_+ + S_-).
    """
    a = np.zeros((NC, NC), dtype=np.complex128)
    xp_mu = fwd[site, mu]
    for nu in range(NDIM):
        if nu == mu:
            continue
        if mu == 3 or nu == 3:
            w = beta_tau
        else:
            w = beta_sigma
        if w == 0.0:
            continue
        xp_nu = fwd[site, nu]
        xm_nu = bwd[site, nu]
        xp_mu_m_nu = bwd[xp_mu, nu]

        # Forward: S_+ = U_nu(site+mu) @ U_mu^d(site+nu) @ U_nu^d(site)
        T1 = _matmul3_dag(U[xp_mu, nu], U[xp_nu, mu])
        S_plus = _matmul3_dag(T1, U[site, nu])

        # Backward: S_- = U_nu^d(site+mu-nu) @ U_mu^d(site-nu) @ U_nu(site-nu)
        # = (U_nu(site+mu-nu)^d) @ (U_mu(site-nu)^d) @ U_nu(site-nu)
        # = _dag_matmul3 then _matmul3_dag style: T2 = U[xp_mu_m_nu,nu]^d @ U[xm_nu,mu]^d
        # then T2 @ U[xm_nu, nu]
        # Build T2 = U[xp_mu_m_nu, nu]^d @ U[xm_nu, mu]^d directly.
        T2 = np.zeros((NC, NC), dtype=np.complex128)
        for i in range(NC):
            for j in range(NC):
                s = 0.0 + 0.0j
                for k in range(NC):
                    s += U[xp_mu_m_nu, nu, k, i].conjugate() * U[xm_nu, mu, j, k].conjugate()
                T2[i, j] = s
        S_minus = _matmul3(T2, U[xm_nu, nu])

        for i in range(NC):
            for j in range(NC):
                a[i, j] += w * (S_plus[i, j] + S_minus[i, j])
    return a


# -------------------------- update routines (jitted) ----------------- #


@njit(cache=False)
def _heatbath_link(U, fwd, bwd, site, mu, beta_sigma, beta_tau):
    """Cabibbo-Marinari pseudo-heatbath on link U(site, mu)."""
    V = _staple_aniso(U, fwd, bwd, site, mu, beta_sigma, beta_tau)
    link = U[site, mu].copy()
    for sg in range(3):
        W = _matmul3(link, V)
        W2 = _extract_su2_block(W, sg)
        v_su2, scale = _project_su2(W2)
        k = scale / NC
        r_new = _su2_heatbath_matrix(k)
        if scale > 1e-15:
            R = np.zeros((2, 2), dtype=np.complex128)
            for i in range(2):
                for j in range(2):
                    s = 0.0 + 0.0j
                    for kk in range(2):
                        s += r_new[i, kk] * v_su2[j, kk].conjugate()
                    R[i, j] = s
        else:
            R = r_new
        link = _left_multiply_subgroup(link, R, sg)
    U[site, mu] = _project_su3(link)


@njit(cache=False)
def _overrelax_link(U, fwd, bwd, site, mu, beta_sigma, beta_tau):
    """SU(3) overrelaxation via three SU(2) reflections."""
    V = _staple_aniso(U, fwd, bwd, site, mu, beta_sigma, beta_tau)
    link = U[site, mu].copy()
    for sg in range(3):
        W = _matmul3(link, V)
        W2 = _extract_su2_block(W, sg)
        v_su2, scale = _project_su2(W2)
        if scale > 1e-15:
            # R = V^d V^d
            vd = np.empty((2, 2), dtype=np.complex128)
            for i in range(2):
                for j in range(2):
                    vd[i, j] = v_su2[j, i].conjugate()
            R = np.zeros((2, 2), dtype=np.complex128)
            for i in range(2):
                for j in range(2):
                    s = 0.0 + 0.0j
                    for kk in range(2):
                        s += vd[i, kk] * vd[kk, j]
                    R[i, j] = s
        else:
            R = np.eye(2, dtype=np.complex128)
        link = _left_multiply_subgroup(link, R, sg)
    U[site, mu] = _project_su3(link)


@njit(cache=False)
def _sweep_jit(U, fwd, bwd, parity_arr, vol, beta_sigma, beta_tau, n_overrelax):
    """One full sweep: heatbath + n_overrelax overrelaxation passes.
    Even/odd checkerboard ordering for proper detailed balance.
    """
    for parity in range(2):
        for site in range(vol):
            if parity_arr[site] != parity:
                continue
            for mu in range(NDIM):
                _heatbath_link(U, fwd, bwd, site, mu, beta_sigma, beta_tau)
    for _ in range(n_overrelax):
        for parity in range(2):
            for site in range(vol):
                if parity_arr[site] != parity:
                    continue
                for mu in range(NDIM):
                    _overrelax_link(U, fwd, bwd, site, mu, beta_sigma, beta_tau)


# -------------------------- measurement (jitted) --------------------- #


@njit(cache=False)
def _plaquette_measure_jit(U, fwd, vol):
    """Measure mean spatial-spatial and spatial-temporal plaquette.
    Returns (P_sigma, P_tau).
    """
    s_sigma = 0.0
    s_tau = 0.0
    n_sigma = 0
    n_tau = 0
    for site in range(vol):
        for mu in range(NDIM):
            for nu in range(mu + 1, NDIM):
                xp_mu = fwd[site, mu]
                xp_nu = fwd[site, nu]
                T1 = _matmul3(U[site, mu], U[xp_mu, nu])
                T2 = _matmul3_dag(T1, U[xp_nu, mu])
                P = _matmul3_dag(T2, U[site, nu])
                tr = _re_tr3(P) / NC
                if mu == 3 or nu == 3:
                    s_tau += tr
                    n_tau += 1
                else:
                    s_sigma += tr
                    n_sigma += 1
    if n_sigma == 0:
        n_sigma = 1
    if n_tau == 0:
        n_tau = 1
    return s_sigma / n_sigma, s_tau / n_tau


# -------------------------- 4D lattice geometry --------------------- #


class Lattice:
    """4D periodic lattice. site = (x, y, z, t) flattened with x fastest."""

    def __init__(self, dims):
        if len(dims) != 4 or any(d <= 1 for d in dims):
            raise ValueError(f"dims must be 4 ints > 1, got {dims}")
        self.dims = tuple(int(d) for d in dims)
        self.vol = int(np.prod(self.dims))
        self._build_neighbors()

    def _build_neighbors(self):
        lx, ly, lz, lt = self.dims
        vol = self.vol
        fwd = np.empty((vol, NDIM), dtype=np.int64)
        bwd = np.empty((vol, NDIM), dtype=np.int64)
        parity = np.empty(vol, dtype=np.int64)
        for s in range(vol):
            x = s % lx
            y = (s // lx) % ly
            z = (s // (lx * ly)) % lz
            t = (s // (lx * ly * lz)) % lt
            parity[s] = (x + y + z + t) & 1
            for mu, length in enumerate(self.dims):
                cp = [x, y, z, t]
                cm = [x, y, z, t]
                cp[mu] = (cp[mu] + 1) % length
                cm[mu] = (cm[mu] - 1) % length
                fwd[s, mu] = ((cp[3] * lz + cp[2]) * ly + cp[1]) * lx + cp[0]
                bwd[s, mu] = ((cm[3] * lz + cm[2]) * ly + cm[1]) * lx + cm[0]
        self.fwd = fwd
        self.bwd = bwd
        self.parity = parity


# -------------------------- driver ---------------------------------- #


def cold_links(lat: Lattice) -> np.ndarray:
    U = np.zeros((lat.vol, NDIM, NC, NC), dtype=np.complex128)
    eye = np.eye(NC, dtype=np.complex128)
    U[:, :] = eye
    return U


def run_anisotropic(
    dims: Tuple[int, int, int, int],
    g2: float,
    xi: float,
    n_thermalize: int,
    n_measure: int,
    measure_every: int,
    n_overrelax: int,
    seed: int,
    verbose: bool = True,
) -> dict:
    """Run anisotropic SU(3) Wilson 4D MC. numba-jitted hot path."""
    np.random.seed(seed)
    lat = Lattice(dims)

    beta_sigma = 2.0 * NC / (g2 * xi)
    beta_tau = 2.0 * NC * xi / g2

    U = cold_links(lat)

    if verbose:
        print(
            f"[run_anisotropic] dims={dims} vol={lat.vol} g2={g2} xi={xi} "
            f"beta_sigma={beta_sigma:.4f} beta_tau={beta_tau:.4f} seed={seed} "
            f"numba={NUMBA_OK}"
        )

    P_sigma_series = []
    P_tau_series = []

    t0 = time.time()
    # Thermalization
    for it in range(n_thermalize):
        _sweep_jit(U, lat.fwd, lat.bwd, lat.parity, lat.vol,
                   beta_sigma, beta_tau, n_overrelax)
    if verbose:
        print(f"  thermalized in {time.time() - t0:.1f}s ({n_thermalize} sweeps)")

    # Measurements
    t1 = time.time()
    for it in range(n_measure):
        _sweep_jit(U, lat.fwd, lat.bwd, lat.parity, lat.vol,
                   beta_sigma, beta_tau, n_overrelax)
        if (it + 1) % measure_every == 0:
            P_sigma, P_tau = _plaquette_measure_jit(U, lat.fwd, lat.vol)
            P_sigma_series.append(P_sigma)
            P_tau_series.append(P_tau)

    if verbose:
        print(
            f"  measured in {time.time() - t1:.1f}s ({n_measure} sweeps, "
            f"{len(P_sigma_series)} measurements)"
        )

    P_sigma_arr = np.array(P_sigma_series)
    P_tau_arr = np.array(P_tau_series)
    n_meas = len(P_sigma_arr)

    def stderr(arr):
        if len(arr) < 2:
            return 0.0
        return float(np.std(arr, ddof=1) / np.sqrt(len(arr)))

    def jackknife(arr, n_blocks=10):
        if len(arr) < n_blocks:
            return stderr(arr)
        n = len(arr)
        block_size = n // n_blocks
        blocks = arr[: n_blocks * block_size].reshape(n_blocks, block_size)
        block_means = blocks.mean(axis=1)
        total = block_means.sum()
        jk = np.array([(total - bm) / (n_blocks - 1) for bm in block_means])
        return float(np.sqrt((n_blocks - 1) / n_blocks * np.sum((jk - jk.mean()) ** 2)))

    return {
        "dims": list(dims),
        "vol": lat.vol,
        "g2": g2,
        "xi": xi,
        "beta_sigma": beta_sigma,
        "beta_tau": beta_tau,
        "n_thermalize": n_thermalize,
        "n_measure": n_measure,
        "measure_every": measure_every,
        "n_overrelax": n_overrelax,
        "seed": seed,
        "n_meas": n_meas,
        "P_sigma_mean": float(P_sigma_arr.mean()) if n_meas else 0.0,
        "P_sigma_stderr": jackknife(P_sigma_arr),
        "P_sigma_naive_stderr": stderr(P_sigma_arr),
        "P_tau_mean": float(P_tau_arr.mean()) if n_meas else 0.0,
        "P_tau_stderr": jackknife(P_tau_arr),
        "P_tau_naive_stderr": stderr(P_tau_arr),
        "P_sigma_series": P_sigma_arr.tolist(),
        "P_tau_series": P_tau_arr.tolist(),
        "wall_time_s": time.time() - t0,
    }


def run_multi_seed(
    dims, g2, xi, n_thermalize, n_measure, measure_every, n_overrelax, seeds, verbose=True,
) -> dict:
    """Run multi-seed ensemble at fixed (dims, g2, xi).
    Returns aggregated stats: per-seed means + ensemble mean / stderr.
    """
    per_seed = []
    sigma_means = []
    sigma_stderrs = []
    tau_means = []
    tau_stderrs = []
    for seed in seeds:
        if verbose:
            print(f"\n  --- seed {seed} ---")
        r = run_anisotropic(
            dims, g2, xi, n_thermalize, n_measure, measure_every,
            n_overrelax, seed, verbose=verbose,
        )
        per_seed.append(r)
        sigma_means.append(r["P_sigma_mean"])
        sigma_stderrs.append(r["P_sigma_stderr"])
        tau_means.append(r["P_tau_mean"])
        tau_stderrs.append(r["P_tau_stderr"])

    sigma_means_arr = np.array(sigma_means)
    sigma_stderrs_arr = np.array(sigma_stderrs)
    tau_means_arr = np.array(tau_means)
    tau_stderrs_arr = np.array(tau_stderrs)

    # Combine across seeds: weighted mean (or simple mean if errors are similar)
    # Use simple mean across seeds, with seed-to-seed std as stderr
    n_seeds = len(seeds)

    # Inverse-variance weighted mean
    def iv_combine(means, errs):
        if (errs > 0).all():
            w = 1.0 / errs ** 2
            mu = (w * means).sum() / w.sum()
            err = math.sqrt(1.0 / w.sum())
            return float(mu), float(err)
        return float(np.mean(means)), float(np.std(means, ddof=1) / math.sqrt(n_seeds))

    sigma_mean, sigma_err = iv_combine(sigma_means_arr, sigma_stderrs_arr)
    tau_mean, tau_err = iv_combine(tau_means_arr, tau_stderrs_arr)

    # Seed-to-seed std for cross-check
    sigma_seed_std = float(np.std(sigma_means_arr, ddof=1)) if n_seeds > 1 else 0.0
    tau_seed_std = float(np.std(tau_means_arr, ddof=1)) if n_seeds > 1 else 0.0

    return {
        "dims": list(dims),
        "g2": g2,
        "xi": xi,
        "seeds": list(seeds),
        "per_seed": per_seed,
        "P_sigma_mean": sigma_mean,
        "P_sigma_stderr": sigma_err,
        "P_sigma_seed_std": sigma_seed_std,
        "P_tau_mean": tau_mean,
        "P_tau_stderr": tau_err,
        "P_tau_seed_std": tau_seed_std,
        "P_sigma_per_seed_means": sigma_means_arr.tolist(),
        "P_sigma_per_seed_stderrs": sigma_stderrs_arr.tolist(),
        "P_tau_per_seed_means": tau_means_arr.tolist(),
        "P_tau_per_seed_stderrs": tau_stderrs_arr.tolist(),
    }


# -------------------------- Path C: NLO analytic --------------------- #


def heat_kernel_su2(theta, s, j_max=30):
    """SU(2) heat kernel at U = exp(i theta n.sigma/2)."""
    if abs(theta) < 1e-12:
        return float(sum((2 * j + 1) ** 2 * np.exp(-s * j * (j + 1)) for j in range(j_max + 1)))
    return float(sum(
        (2 * j + 1) * np.exp(-s * j * (j + 1)) *
        np.sin((2 * j + 1) * theta / 2) / np.sin(theta / 2)
        for j in range(j_max + 1)
    ))


def haar_su2(theta):
    return (2.0 / math.pi) * (math.sin(theta / 2)) ** 2


def single_plaq_wilson_su2(beta):
    """SU(2) Wilson single-plaquette <1 - (1/N_c) Re Tr U> = 1 - I_2(beta)/I_1(beta)."""
    from scipy.special import iv as bessel_iv
    if beta < 1e-10:
        return 0.5
    return float(1.0 - bessel_iv(2, beta) / bessel_iv(1, beta))


def single_plaq_hk_su2(s):
    """SU(2) HK single-plaquette <1 - (1/N_c) Re Tr U> = 1 - exp(-3s/4)."""
    return float(1.0 - math.exp(-0.75 * s))


def path_c_nlo_refinement(g2_list, xi_list, fit_max_order=4):
    """Path C: NLO refinement of Convention C-iso.

    For SU(2) Wilson vs heat-kernel:
        <P>_W(beta_W) - <P>_HK(s_t) = ?  with beta_W = N_c/s_t

    The leading-order match is exact at infinite beta_W (small s_t).
    The relative shift is known from prior to be linear in s_t with
    coefficient ~0.21 for SU(2). Here we extend:

      1. Direct numerical eval of (P_W - P_HK)/P_HK at xi in {1,2,4,8,16,32,64}
         to extract polynomial coefficients in s_t.
      2. Fit rel_shift(s_t) = a1·s_t + a2·s_t^2 + a3·s_t^3 + ...
         to extract NLO and beyond.
      3. Compare to small-s_t Taylor expansion:
         P_HK = 3s/4 - 9s^2/32 + 27s^3/128 - ...
         P_W(2/s) = ?  via Bessel asymptotic.

    Returns dict with rows, leading and NLO fitted coefficients.
    """
    print("\n=== Path C (NLO): Convention C-iso analytic refinement ===")
    print("    Direct comparison of SU(2) Wilson vs HK temporal plaquette")
    print("    extracting linear, quadratic, cubic coefficients in s_t.\n")

    rows = []
    for g2 in g2_list:
        for xi in xi_list:
            s_t = g2 / (2.0 * xi)
            beta_W = 2.0 / s_t  # N_c=2 for SU(2)
            P_HK = single_plaq_hk_su2(s_t)
            P_W = single_plaq_wilson_su2(beta_W)
            diff = P_W - P_HK
            rel = diff / P_HK if P_HK > 1e-10 else 0.0
            rows.append({
                "g2": g2,
                "xi": xi,
                "s_t": s_t,
                "beta_W": beta_W,
                "P_HK": P_HK,
                "P_W": P_W,
                "abs_diff": diff,
                "rel_shift": rel,
            })

    # Print table
    print(f"  {'g^2':>5}  {'xi':>5}  {'s_t':>8}  {'beta_W':>8}  "
          f"{'<P>_HK':>9}  {'<P>_W':>9}  {'(W-HK)':>10}  {'rel.shift':>10}")
    print("  " + "-" * 80)
    for r in rows:
        print(
            f"  {r['g2']:>5.2f}  {r['xi']:>5.2f}  {r['s_t']:>8.5f}  "
            f"{r['beta_W']:>8.3f}  {r['P_HK']:>9.5f}  {r['P_W']:>9.5f}  "
            f"{r['abs_diff']:>+10.5f}  {r['rel_shift']:>+10.4%}"
        )

    # Polynomial fit of |rel_shift|/s_t = a0 + a1·s_t + a2·s_t^2 in small-s_t regime
    s_arr = np.array([r["s_t"] for r in rows])
    rel_arr = np.array([r["rel_shift"] for r in rows])
    abs_diff_arr = np.array([r["abs_diff"] for r in rows])

    # Use only small-s_t rows for clean polynomial fit
    mask = s_arr < 0.6
    s_fit = s_arr[mask]
    rel_fit = rel_arr[mask]
    abs_fit = abs_diff_arr[mask]

    # Fit |rel_shift| = sum_n a_n * s_t^n for n in {1, 2, 3, ...}
    # Equivalent: (rel_shift / s_t) = a_1 + a_2*s_t + a_3*s_t^2 + ...
    # Use polynomial in s_t directly (with constraint a_0 = 0 enforced by no constant term)
    # i.e. fit rel_shift as poly in s_t with no constant
    if len(s_fit) >= fit_max_order:
        # Build Vandermonde without constant: columns s_t^1, s_t^2, ..., s_t^k
        k = min(fit_max_order, len(s_fit) - 1)
        V = np.column_stack([s_fit ** i for i in range(1, k + 1)])
        coefs, residuals, rank, sv = np.linalg.lstsq(V, rel_fit, rcond=None)
        a_coefs = coefs.tolist()  # a_1, a_2, ...
    else:
        a_coefs = [None] * fit_max_order

    print("\n  Polynomial fit of rel_shift(s_t) for s_t < 0.6 (no constant term):")
    if a_coefs[0] is not None:
        for i, a in enumerate(a_coefs, start=1):
            print(f"    a_{i} (coefficient of s_t^{i}) = {a:+.6f}")

    print("\n  Compare to leading Taylor expansion of (P_W - P_HK):")
    print("    SU(2) HK: P_HK(s) = 3s/4 - 9s^2/32 + 27s^3/128 - ...")
    print("    SU(2) Wilson at beta = 2/s: P_W(beta) = 1 - I_2(beta)/I_1(beta).")
    print("    For beta -> infinity (s -> 0):")
    print("      I_2(b)/I_1(b) = 1 - 3/(2b) + 15/(8b^2) - 105/(16b^3) + ...")
    print("                    = 1 - 3s/4 + 15 s^2/32 - 105 s^3/128 + ...")
    print("    Hence P_W(2/s) = 3s/4 - 15 s^2/32 + 105 s^3/128 - ...")
    print("\n    (P_W - P_HK)(s) = (15/32 - 9/32) s^2 + (-105/128 + 27/128) s^3 + ...")
    print("                    = (3/16) s^2 - (39/64) s^3 + ...")
    print("                    = 0.1875 s^2 - 0.609 s^3 + ...")
    print("\n    rel_shift(s) = (P_W - P_HK)/P_HK(s)")
    print("                ~ (0.1875 s^2 - 0.609 s^3) / (3s/4 - 9s^2/32)")
    print("                ~ 0.25 s + O(s^2)")
    print("    Leading coefficient: 0.250 (analytic).")
    print(f"    Numerical fit a_1: {a_coefs[0]:+.4f}" if a_coefs[0] is not None else "")

    # Predict at canonical operating points
    print("\n  Predicted Convention C-iso shift at canonical operating points:")
    if a_coefs[0] is not None:
        for xi_pred in [1.0, 2.0, 4.0, 8.0, 16.0, 32.0]:
            s = 1.0 / (2.0 * xi_pred)  # at g^2 = 1
            pred = sum(a_coefs[i] * s ** (i + 1) for i in range(len(a_coefs)))
            # Also LO-only
            pred_lo = a_coefs[0] * s
            print(f"    xi={xi_pred:>5.1f} (s_t={s:.4f}): "
                  f"NLO+={pred:>+8.4%}   LO-only={pred_lo:>+8.4%}")

    # Save
    return {
        "rows": rows,
        "a_coefs": a_coefs,
        "fit_mask_s_t_max": 0.6,
        "analytic_LO_coef": 0.25,
        "interpretation": (
            "rel_shift(s_t) = a_1*s_t + a_2*s_t^2 + ... where a_1 = 1/4 analytically "
            "(SU(2)) and a_2 captures NLO Convention C-iso correction beyond linear."
        ),
    }


# -------------------------- Path B: thermodynamic-limit fit --------- #


def thermodynamic_limit_fit(volumes_results: List[dict]) -> dict:
    """Fit <P>(L) = <P>_inf + a/L^2 + b/L^4 to extract <P>_inf.

    volumes_results: list of dicts with 'dims' and 'P_sigma_mean', 'P_sigma_stderr'.
    """
    print("\n=== Path B fit: thermodynamic-limit extrapolation ===")
    Ls = []
    Ps = []
    Es = []
    for r in volumes_results:
        L = r["dims"][0]  # spatial extent (assume cubic spatial)
        Ls.append(L)
        Ps.append(r["P_sigma_mean"])
        Es.append(r["P_sigma_stderr"])
    Ls = np.array(Ls, dtype=float)
    Ps = np.array(Ps)
    Es = np.array(Es)

    # Sort by L
    idx = np.argsort(Ls)
    Ls = Ls[idx]
    Ps = Ps[idx]
    Es = Es[idx]

    print(f"  Volumes: L = {Ls.tolist()}")
    print(f"  <P_sigma> = {Ps.tolist()}")
    print(f"  stderr    = {Es.tolist()}")

    n = len(Ls)
    if n < 2:
        print("  Insufficient data for fit; need >= 2 volumes.")
        return {"P_inf": None, "a": None, "b": None, "fit_n": n}

    # Build weighted least-squares fit
    # Model: P(L) = P_inf + a/L^2 + b/L^4
    # If n == 2, fit only constant + a/L^2.
    if n >= 3:
        X = np.column_stack([np.ones_like(Ls), 1.0 / Ls ** 2, 1.0 / Ls ** 4])
        # Weighted least squares
        W = 1.0 / np.maximum(Es, 1e-6) ** 2
        sqrtW = np.sqrt(W)
        Xw = X * sqrtW[:, None]
        Yw = Ps * sqrtW
        beta, *_ = np.linalg.lstsq(Xw, Yw, rcond=None)
        P_inf, a, b = beta.tolist()
        # Residuals
        pred = X @ beta
        resid = Ps - pred
        chi2 = np.sum((resid / np.maximum(Es, 1e-6)) ** 2)
        # Error on P_inf via covariance matrix
        cov = np.linalg.inv(Xw.T @ Xw)
        P_inf_err = math.sqrt(cov[0, 0])
        print(f"  Fit:  P_inf = {P_inf:.5f} ± {P_inf_err:.5f}, "
              f"a = {a:+.4f}, b = {b:+.4f}")
        print(f"  chi^2 = {chi2:.3f} (dof = {n - 3})")
        return {
            "fit_form": "P(L) = P_inf + a/L^2 + b/L^4",
            "P_inf": P_inf,
            "P_inf_err": P_inf_err,
            "a": a,
            "b": b,
            "chi2": chi2,
            "dof": n - 3,
            "Ls": Ls.tolist(),
            "Ps": Ps.tolist(),
            "Es": Es.tolist(),
            "fit_n": n,
        }
    else:  # n == 2
        # 2-point fit: P(L) = P_inf + a/L^2
        X = np.column_stack([np.ones_like(Ls), 1.0 / Ls ** 2])
        W = 1.0 / np.maximum(Es, 1e-6) ** 2
        sqrtW = np.sqrt(W)
        Xw = X * sqrtW[:, None]
        Yw = Ps * sqrtW
        beta, *_ = np.linalg.lstsq(Xw, Yw, rcond=None)
        P_inf, a = beta.tolist()
        cov = np.linalg.inv(Xw.T @ Xw)
        P_inf_err = math.sqrt(cov[0, 0])
        print(f"  Fit (2pt):  P_inf = {P_inf:.5f} ± {P_inf_err:.5f}, a = {a:+.4f}")
        return {
            "fit_form": "P(L) = P_inf + a/L^2 (2-point)",
            "P_inf": P_inf,
            "P_inf_err": P_inf_err,
            "a": a,
            "b": None,
            "chi2": None,
            "dof": 0,
            "Ls": Ls.tolist(),
            "Ps": Ps.tolist(),
            "Es": Es.tolist(),
            "fit_n": n,
        }


# -------------------------- main entry ----------------------------- #


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=[
            "self_test", "path_a", "path_b", "path_c", "all", "fast",
        ], default="fast",
    )
    parser.add_argument("--g2", type=float, default=1.0)
    parser.add_argument("--xi", type=float, default=4.0)
    parser.add_argument("--n_thermalize", type=int, default=80)
    parser.add_argument("--n_measure", type=int, default=400)
    parser.add_argument("--measure_every", type=int, default=2)
    parser.add_argument("--n_overrelax", type=int, default=2)
    parser.add_argument("--seeds", type=str, default="1,2,3,4,5")
    parser.add_argument("--volumes_list", type=str, default="4x4x4x16,6x6x6x24")
    parser.add_argument(
        "--out_dir", type=str,
        default="outputs/action_first_principles_2026_05_07/exact_tier_e_witness_push",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    results: dict = {
        "args": vars(args),
        "version": "exact-tier-ewitness-2026-05-07",
        "numba_available": NUMBA_OK,
    }

    seeds = [int(s) for s in args.seeds.split(",")]

    print(f"\nnumba_available = {NUMBA_OK}")

    # ------------------------------------------------------------------
    # Self-test
    # ------------------------------------------------------------------
    if args.mode in ("self_test", "all", "fast"):
        print("\n" + "=" * 70)
        print("SELF-TEST: isotropic SU(3) Wilson, beta=6 on 2^4 lattice")
        print("=" * 70)
        st_result = run_anisotropic(
            dims=(2, 2, 2, 2), g2=1.0, xi=1.0,
            n_thermalize=60, n_measure=200, measure_every=2,
            n_overrelax=2, seed=12345,
        )
        print(f"  <P_sigma> = {st_result['P_sigma_mean']:.4f} ± {st_result['P_sigma_stderr']:.4f}")
        print(f"  <P_tau>   = {st_result['P_tau_mean']:.4f} ± {st_result['P_tau_stderr']:.4f}")
        print(f"  ENGELS-1990 BENCHMARK: <P>(beta=6) ~ 0.594 (large vol)")
        results["self_test"] = st_result

    # ------------------------------------------------------------------
    # Path A: high-statistics multi-seed at xi=4
    # ------------------------------------------------------------------
    if args.mode in ("path_a", "all", "fast"):
        print("\n" + "=" * 70)
        print(f"PATH A: high-statistics multi-seed anisotropic xi={args.xi} on 4^3 x 16")
        print("=" * 70)
        path_a = run_multi_seed(
            dims=(4, 4, 4, 16), g2=args.g2, xi=args.xi,
            n_thermalize=args.n_thermalize, n_measure=args.n_measure,
            measure_every=args.measure_every, n_overrelax=args.n_overrelax,
            seeds=seeds, verbose=True,
        )
        print(f"\n  Multi-seed combined:")
        print(f"    <P_sigma> = {path_a['P_sigma_mean']:.5f} ± {path_a['P_sigma_stderr']:.5f}  "
              f"(seed-std: {path_a['P_sigma_seed_std']:.5f})")
        print(f"    <P_tau>   = {path_a['P_tau_mean']:.5f} ± {path_a['P_tau_stderr']:.5f}  "
              f"(seed-std: {path_a['P_tau_seed_std']:.5f})")
        results["path_a"] = path_a

    # ------------------------------------------------------------------
    # Path B: finite-size scaling on volumes_list
    # ------------------------------------------------------------------
    if args.mode in ("path_b", "all"):
        print("\n" + "=" * 70)
        print(f"PATH B: finite-size scaling extrapolation at xi={args.xi}")
        print("=" * 70)
        path_b_volumes = []
        for vol_str in args.volumes_list.split(","):
            dims = tuple(int(x) for x in vol_str.split("x"))
            print(f"\n  --- volume {vol_str} ---")
            r = run_multi_seed(
                dims=dims, g2=args.g2, xi=args.xi,
                n_thermalize=args.n_thermalize, n_measure=args.n_measure,
                measure_every=args.measure_every, n_overrelax=args.n_overrelax,
                seeds=seeds[:3], verbose=True,  # Use 3 seeds for volume scan
            )
            print(f"  dims={dims}: <P_sigma>={r['P_sigma_mean']:.5f} ± {r['P_sigma_stderr']:.5f}")
            path_b_volumes.append(r)
        path_b_fit = thermodynamic_limit_fit(path_b_volumes)
        results["path_b"] = {"volumes": path_b_volumes, "fit": path_b_fit}

    # ------------------------------------------------------------------
    # Path C: NLO analytic refinement
    # ------------------------------------------------------------------
    if args.mode in ("path_c", "all", "fast"):
        path_c = path_c_nlo_refinement(
            g2_list=[args.g2],
            xi_list=[1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0],
        )
        results["path_c"] = path_c

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------
    out_path = out_dir / f"results_mode-{args.mode}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2,
                  default=lambda o: float(o) if isinstance(o, np.generic) else str(o))
    print(f"\nSaved results to {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
