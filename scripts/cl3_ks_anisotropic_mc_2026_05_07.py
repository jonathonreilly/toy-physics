"""
Anisotropic Wilson 4D lattice Monte Carlo to compute the KS Hamiltonian
ground-state plaquette expectation on the 2x2 spatial torus.

KS Hamiltonian -> 4D anisotropic Wilson action:
  S = -(beta_sigma/N_c) Sum_{p_spatial} Re Tr U_p
      -(beta_tau/N_c)   Sum_{p_temporal} Re Tr U_p

where:
  beta_sigma = 1/(g^2 xi)        [spatial coupling]
  beta_tau   = xi/g^2            [temporal coupling]
  xi = a_sigma / a_tau           [anisotropy]

KS Hamilton limit: xi -> infinity (a_tau -> 0).
Isotropic Wilson: xi = 1, beta_sigma = beta_tau = 1/g^2 = 6 at g^2=1
                 But in conventional Wilson, beta = 6/g^2 (factor 2 N_c).
                 Standard: beta_iso = 2 N_c / g^2 = 6 for SU(3).

Note convention: action S = -(beta/N_c) Sum_p Re Tr U_p translates to
beta_iso = 2 N_c / g^2 only after absorbing factors of 2.

We compute <Re Tr U_p / N_c> for spatial plaquettes only, on the
2x2x2xLt geometry, sweeping xi from 1 (isotropic) to large (KS limit).

This provides a path-integral benchmark for the KS Hamiltonian
expectation value <P>_KS that bypasses variational ED basis truncation.
"""

from __future__ import annotations

import time
import numpy as np
from numpy.random import default_rng
from scipy.linalg import expm


def gell_mann_T():
    L = []
    L.append(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex))
    L.append(np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex))
    L.append(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex))
    L.append(np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex))
    L.append(np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex))
    L.append(np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex))
    L.append(np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex))
    L.append(np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex)
              / np.sqrt(3))
    return [0.5 * Lam for Lam in L]


_TS_CACHE = None


def _get_Ts():
    global _TS_CACHE
    if _TS_CACHE is None:
        _TS_CACHE = gell_mann_T()
    return _TS_CACHE


class AnisotropicWilsonLattice:
    """
    Anisotropic 4D Wilson lattice.

    Action: S = -(beta_sigma/N_c) Sum_{spatial p} Re Tr U_p
                -(beta_tau/N_c)   Sum_{temporal p} Re Tr U_p

    Spatial directions: x, y, z (mu = 0, 1, 2)
    Temporal direction: t (mu = 3)

    A 'spatial' plaquette has both directions in {0,1,2}.
    A 'temporal' plaquette has one direction = 3.
    """

    def __init__(self, Lx, Ly, Lz, Lt, beta_sigma, beta_tau, seed=42):
        self.Lx, self.Ly, self.Lz, self.Lt = Lx, Ly, Lz, Lt
        self.beta_sigma = beta_sigma
        self.beta_tau = beta_tau
        self.rng = default_rng(seed)
        # U[mu, t, z, y, x]
        self.U = np.zeros((4, Lt, Lz, Ly, Lx, 3, 3), dtype=complex)
        for mu in range(4):
            self.U[mu] = np.eye(3)[None, None, None, None] * np.ones(
                (Lt, Lz, Ly, Lx, 1, 1), dtype=complex
            )
        self._L = [Lx, Ly, Lz, Lt]
        self._ax_idx = [3, 2, 1, 0]  # mu=0->x->coord[3]

    def staple_sum(self, mu, t, z, y, x):
        """
        Sum of 6 staples around link U_mu(site), separately weighted by
        beta_sigma/N_c or beta_tau/N_c depending on plaquette orientation.

        We return TWO staples: spatial-coupled S_sigma and temporal-coupled S_tau.
        """
        coord = [t, z, y, x]
        ax_idx = self._ax_idx
        L_list = self._L

        S_sigma = np.zeros((3, 3), dtype=complex)
        S_tau = np.zeros((3, 3), dtype=complex)

        for nu in range(4):
            if nu == mu:
                continue
            cm = list(coord)
            cm[ax_idx[mu]] = (cm[ax_idx[mu]] + 1) % L_list[mu]
            cn = list(coord)
            cn[ax_idx[nu]] = (cn[ax_idx[nu]] + 1) % L_list[nu]
            U_nu_pm = self.U[nu, cm[0], cm[1], cm[2], cm[3]]
            U_mu_pn = self.U[mu, cn[0], cn[1], cn[2], cn[3]]
            U_nu_s = self.U[nu, coord[0], coord[1], coord[2], coord[3]]
            fwd = U_nu_pm @ np.conj(U_mu_pn.T) @ np.conj(U_nu_s.T)

            cn_m = list(coord)
            cn_m[ax_idx[nu]] = (cn_m[ax_idx[nu]] - 1) % L_list[nu]
            cn_m_pm = list(cn_m)
            cn_m_pm[ax_idx[mu]] = (cn_m_pm[ax_idx[mu]] + 1) % L_list[mu]
            U_nu_pmn = self.U[nu, cn_m_pm[0], cn_m_pm[1], cn_m_pm[2], cn_m_pm[3]]
            U_mu_mn = self.U[mu, cn_m[0], cn_m[1], cn_m[2], cn_m[3]]
            U_nu_mn = self.U[nu, cn_m[0], cn_m[1], cn_m[2], cn_m[3]]
            bwd = np.conj(U_nu_pmn.T) @ np.conj(U_mu_mn.T) @ U_nu_mn

            # Plaquette in (mu, nu) plane: spatial if both mu, nu < 3, else temporal
            if mu < 3 and nu < 3:
                S_sigma += fwd + bwd
            else:
                S_tau += fwd + bwd
        return S_sigma, S_tau

    def metropolis_step(self, mu, t, z, y, x, eps=0.1):
        Ts = _get_Ts()
        S_sigma, S_tau = self.staple_sum(mu, t, z, y, x)
        # Build effective staple: beta_sigma * S_sigma + beta_tau * S_tau
        # The action change is dS = -(beta_sigma/N_c) Re[(U_new - U_old) S_sigma]
        #                            -(beta_tau/N_c) Re[(U_new - U_old) S_tau]
        # = -(1/N_c) Re[(U_new - U_old) (beta_sigma S_sigma + beta_tau S_tau)]
        # So we use: effective staple = beta_sigma * S_sigma + beta_tau * S_tau
        # and acceptance via -dS using factor 1/N_c (same convention as scalar Wilson).
        S_eff = self.beta_sigma * S_sigma + self.beta_tau * S_tau

        U_old = self.U[mu, t, z, y, x]
        alpha = self.rng.standard_normal(8) * eps
        A = sum(a * T for a, T in zip(alpha, Ts))
        R = expm(1j * A)
        U_new = R @ U_old

        re_old = np.trace(U_old @ S_eff).real
        re_new = np.trace(U_new @ S_eff).real
        dS = -(1.0 / 3.0) * (re_new - re_old)
        if dS <= 0 or self.rng.uniform(0, 1) < np.exp(-dS):
            self.U[mu, t, z, y, x] = U_new
            return True
        return False

    def sweep(self, eps=0.1):
        accepted = 0
        total = 0
        for mu in range(4):
            for t in range(self.Lt):
                for z in range(self.Lz):
                    for y in range(self.Ly):
                        for x in range(self.Lx):
                            if self.metropolis_step(mu, t, z, y, x, eps):
                                accepted += 1
                            total += 1
        return accepted / total

    def measure_spatial_plaquette(self):
        """<Re Tr U_p / N_c> averaged over SPATIAL (x-y, x-z, y-z) plaquettes only."""
        total = 0.0
        n_plaq = 0
        coord_axes = self._ax_idx
        for t in range(self.Lt):
            for z in range(self.Lz):
                for y in range(self.Ly):
                    for x in range(self.Lx):
                        coord = [t, z, y, x]
                        for (mu, nu) in [(0, 1), (0, 2), (1, 2)]:
                            cm = list(coord)
                            cm[coord_axes[mu]] = (cm[coord_axes[mu]] + 1) % self._L[mu]
                            cn = list(coord)
                            cn[coord_axes[nu]] = (cn[coord_axes[nu]] + 1) % self._L[nu]
                            U1 = self.U[mu, coord[0], coord[1], coord[2], coord[3]]
                            U2 = self.U[nu, cm[0], cm[1], cm[2], cm[3]]
                            U3 = self.U[mu, cn[0], cn[1], cn[2], cn[3]]
                            U4 = self.U[nu, coord[0], coord[1], coord[2], coord[3]]
                            P = U1 @ U2 @ np.conj(U3.T) @ np.conj(U4.T)
                            total += np.trace(P).real / 3.0
                            n_plaq += 1
        return total / n_plaq

    def measure_temporal_plaquette(self):
        """<Re Tr U_p / N_c> averaged over TEMPORAL (mu-3 with mu<3) plaquettes."""
        total = 0.0
        n_plaq = 0
        coord_axes = self._ax_idx
        for t in range(self.Lt):
            for z in range(self.Lz):
                for y in range(self.Ly):
                    for x in range(self.Lx):
                        coord = [t, z, y, x]
                        for (mu, nu) in [(0, 3), (1, 3), (2, 3)]:
                            cm = list(coord)
                            cm[coord_axes[mu]] = (cm[coord_axes[mu]] + 1) % self._L[mu]
                            cn = list(coord)
                            cn[coord_axes[nu]] = (cn[coord_axes[nu]] + 1) % self._L[nu]
                            U1 = self.U[mu, coord[0], coord[1], coord[2], coord[3]]
                            U2 = self.U[nu, cm[0], cm[1], cm[2], cm[3]]
                            U3 = self.U[mu, cn[0], cn[1], cn[2], cn[3]]
                            U4 = self.U[nu, coord[0], coord[1], coord[2], coord[3]]
                            P = U1 @ U2 @ np.conj(U3.T) @ np.conj(U4.T)
                            total += np.trace(P).real / 3.0
                            n_plaq += 1
        return total / n_plaq


def run_anisotropic(Lx, Ly, Lz, Lt, beta_sigma, beta_tau,
                     n_therm=1000, n_meas=1000, seed=42, eps=0.1,
                     verbose=True):
    if verbose:
        print(f"\n--- Anisotropic Wilson MC: {Lx}x{Ly}x{Lz}x{Lt}, "
              f"beta_sigma={beta_sigma:.2f}, beta_tau={beta_tau:.2f} ---")
    lat = AnisotropicWilsonLattice(Lx, Ly, Lz, Lt, beta_sigma, beta_tau, seed)
    if verbose:
        print(f"  Thermalizing {n_therm} sweeps...")
    t0 = time.time()
    for s in range(n_therm):
        ar = lat.sweep(eps=eps)
        if verbose and (s + 1) % 200 == 0:
            P_sp = lat.measure_spatial_plaquette()
            P_tau = lat.measure_temporal_plaquette()
            print(f"    sweep {s+1}: P_sp={P_sp:.4f}, P_tau={P_tau:.4f}, "
                  f"accept={ar:.2f}")
    if verbose:
        print(f"  Measuring {n_meas} sweeps...")
    P_sp_all = []
    P_tau_all = []
    for s in range(n_meas):
        lat.sweep(eps=eps)
        P_sp_all.append(lat.measure_spatial_plaquette())
        P_tau_all.append(lat.measure_temporal_plaquette())
    P_sp_mean = np.mean(P_sp_all)
    P_sp_err = np.std(P_sp_all, ddof=1) / np.sqrt(len(P_sp_all))
    P_tau_mean = np.mean(P_tau_all)
    P_tau_err = np.std(P_tau_all, ddof=1) / np.sqrt(len(P_tau_all))
    dt = time.time() - t0
    if verbose:
        print(f"  Total time: {dt:.1f}s")
        print(f"  P_sp  = {P_sp_mean:.4f} +/- {P_sp_err:.4f}")
        print(f"  P_tau = {P_tau_mean:.4f} +/- {P_tau_err:.4f}")
    return {
        'Lx': Lx, 'Ly': Ly, 'Lz': Lz, 'Lt': Lt,
        'beta_sigma': beta_sigma, 'beta_tau': beta_tau,
        'P_sp': P_sp_mean, 'P_sp_err': P_sp_err,
        'P_tau': P_tau_mean, 'P_tau_err': P_tau_err,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("Anisotropic Wilson MC for KS Hamiltonian limit")
    print("=" * 70)
    print()
    print("KS Hamilton limit: xi -> infinity")
    print("Trotter dictionary (Kogut-Susskind):")
    print("  beta_sigma = 1/(g^2 xi),  beta_tau = xi/g^2")
    print()

    g_squared = 1.0
    Lx, Ly, Lz = 2, 2, 2

    # Isotropic xi=1: beta_sigma = beta_tau = 1/g^2 = 1
    # (Note: this differs from standard Wilson convention of beta=2*N_c/g^2=6.)
    # We use the action S = -(beta/N_c) Re Tr U_p; if beta_iso for standard
    # Wilson is 6, our convention should also use beta_sigma = 6 at xi=1, g^2=1.

    # Standard Wilson convention with our action form:
    # S = -(beta_W/N_c) Re Tr U_p; beta_W = 2*N_c/g^2 = 6 at g^2=1.
    # So canonical beta_sigma_iso = 6, beta_tau_iso = 6.
    # Trotter relation: beta_sigma = beta_W / xi, beta_tau = beta_W * xi
    # at xi=1, both = beta_W. At xi=infty, spatial -> 0, temporal -> infty.

    # Isotropic xi=1 (standard Wilson)
    print("[1] xi=1 (isotropic): beta_sigma=beta_tau=6, Lt=16")
    r1 = run_anisotropic(Lx, Ly, Lz, 16, 6.0, 6.0,
                          n_therm=500, n_meas=500, seed=42, eps=0.1)

    # xi=2: spatial coupling halved, temporal doubled
    print("\n[2] xi=2: beta_sigma=3, beta_tau=12, Lt=32")
    r2 = run_anisotropic(Lx, Ly, Lz, 32, 3.0, 12.0,
                          n_therm=500, n_meas=500, seed=42, eps=0.1)

    # xi=4
    print("\n[3] xi=4: beta_sigma=1.5, beta_tau=24, Lt=64")
    r3 = run_anisotropic(Lx, Ly, Lz, 64, 1.5, 24.0,
                          n_therm=500, n_meas=500, seed=42, eps=0.1)

    # xi=8
    print("\n[4] xi=8: beta_sigma=0.75, beta_tau=48, Lt=64")
    r4 = run_anisotropic(Lx, Ly, Lz, 64, 0.75, 48.0,
                          n_therm=500, n_meas=500, seed=42, eps=0.1)

    print("\n=== Summary: 2x2x2 spatial torus, g^2=1 ===")
    print(f"{'xi':>6}  {'beta_sigma':>10}  {'beta_tau':>9}  {'Lt':>4}  "
          f"{'P_sp':>10}  {'P_tau':>10}")
    for r, xi in [(r1, 1), (r2, 2), (r3, 4), (r4, 8)]:
        print(f"{xi:>6}  {r['beta_sigma']:>10.2f}  {r['beta_tau']:>9.2f}  "
              f"{r['Lt']:>4}  {r['P_sp']:>10.4f}  {r['P_tau']:>10.4f}")
    print()
    print("Interpretation:")
    print("  As xi -> infinity (Hamilton limit), P_sp converges to <P>_KS")
    print("  on the 2x2x2 spatial torus. This is the path-integral analog")
    print("  of the variational ED problem.")
    print()
    print("Reference: KS literature P_sp ~ 0.55-0.60")
    print("           Wilson 4D MC isotropic beta=6: P_sp ~ 0.5934 (large vol)")
