"""
Wilson 4D lattice Monte Carlo benchmark on a SMALL spatial torus
to compare with the 2x2 spatial torus spin-network ED.

This computes <Re Tr U_p / N_c> for SU(3) lattice gauge theory at
beta = 6/g^2 = 6 (canonical g^2 = 1), but on a very small lattice
(2x2x2x4 or 2x2x2x8 etc.).

Method: standard Cabibbo-Marinari pseudo-heatbath for SU(3).
Measurements: spatial plaquettes only (to compare with the KS Hamilton
limit of just spatial plaquettes).

Reference: large-volume MC at beta=6 gives <P> ~ 0.5934.
Small-volume MC may differ due to finite-size effects.

This script provides an independent benchmark for the spin-network ED
result on the 2x2 spatial torus to determine whether <P> ~ 0.045 is a
genuine finite-size answer or an artifact of basis truncation.
"""

from __future__ import annotations

import time
import numpy as np
from numpy.random import default_rng


def gell_mann_T():
    """SU(3) generators T_a = lambda_a/2."""
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


# -------------------------------------------------------------------
# SU(2) heatbath (for SU(3) Cabibbo-Marinari sub-block updates)
# -------------------------------------------------------------------

def su2_heatbath_kernel(rng, beta_eff, N_tries=10):
    """
    Generate SU(2) matrix from heatbath distribution exp(beta_eff/2 Tr X)
    via Creutz / Kennedy-Pendleton method.
    """
    # We need x0 distributed as p(x0) ~ sqrt(1-x0^2) exp(beta_eff x0)
    # Then x1, x2, x3 uniformly on sphere of radius sqrt(1-x0^2).
    # KP algorithm: rejection sampling via x0 = 1 + (1/beta_eff) ln(...)
    if beta_eff < 1e-6:
        # Random SU(2)
        x = rng.standard_normal(4)
        x /= np.linalg.norm(x)
        return x

    for _ in range(N_tries):
        # KP rejection
        r = rng.uniform(0.0, 1.0, size=4)
        delta = (-1.0 / beta_eff) * (
            np.log(max(r[0], 1e-30))
            + np.cos(2 * np.pi * r[1]) ** 2 * np.log(max(r[2], 1e-30))
        )
        if r[3] ** 2 > 1.0 - 0.5 * delta:
            continue
        x0 = 1.0 - delta
        if abs(x0) > 1.0:
            continue
        # x1, x2, x3 uniform on sphere of radius sqrt(1 - x0^2)
        s = np.sqrt(max(0.0, 1.0 - x0 ** 2))
        # Spherical
        phi = rng.uniform(0, 2 * np.pi)
        cos_th = rng.uniform(-1, 1)
        sin_th = np.sqrt(max(0.0, 1.0 - cos_th ** 2))
        x1 = s * sin_th * np.cos(phi)
        x2 = s * sin_th * np.sin(phi)
        x3 = s * cos_th
        return np.array([x0, x1, x2, x3])
    # Fallback random
    x = rng.standard_normal(4)
    x /= np.linalg.norm(x)
    return x


def x_to_su2(x):
    """SU(2) matrix from quaternion x = (x0, x1, x2, x3)."""
    return np.array([
        [x[0] + 1j * x[3], x[2] + 1j * x[1]],
        [-x[2] + 1j * x[1], x[0] - 1j * x[3]],
    ])


# -------------------------------------------------------------------
# SU(3) Cabibbo-Marinari heatbath
# -------------------------------------------------------------------

def su3_pseudo_heatbath(staple, beta, rng):
    """
    Cabibbo-Marinari SU(3) pseudo-heatbath update for link with given staple.

    staple: 3x3 complex matrix sum of staples around the link.
    beta = 2 N_c / g^2 = 6/g^2 for SU(3).

    Updates each of 3 SU(2) sub-blocks (1-2, 1-3, 2-3) sequentially.
    Returns updated SU(3) link matrix.
    """
    U = np.eye(3, dtype=complex)
    # Sub-block indices
    sub_blocks = [(0, 1), (0, 2), (1, 2)]
    for (i, j) in sub_blocks:
        # Effective SU(2) staple from R_ij = U @ staple
        R = U @ staple
        # Extract 2x2 sub-block in (i,j) sector
        a = R[i, i] + np.conj(R[j, j])
        b = R[i, j] - np.conj(R[j, i])
        # k = sqrt(|a|^2 + |b|^2)
        k = np.sqrt(np.abs(a) ** 2 + np.abs(b) ** 2)
        if k < 1e-12:
            continue
        beta_eff = (2.0 / 3.0) * beta * k  # SU(3) -> SU(2): scale beta
        x = su2_heatbath_kernel(rng, beta_eff)
        # Now form V in the SU(2) sub-block.
        # The "SU(2) parent" of the SU(3) update follows Pendleton/Kennedy
        # construction. Here we use the standard:
        # V_su2 corresponds to (a, b) above, and we update as
        # x_full = x * (a/k, -b/k)^{-1} = x in the rotated frame.
        # Actually: we need to update U[i,j sub-block] = V where V is
        # such that V @ (a, b stuff) is heatbath-distributed.
        # Cabibbo-Marinari: U <- W @ U, where W is identity except in
        # (i, j) sub-block, where W_2x2 = x * a_norm^{-1}, with
        # a_norm = (a -conj(b); b conj(a)) / k.
        # We construct V_su2 such that the 2x2 block in (i,j) of W is V.
        a_re = a.real / k
        a_im = a.imag / k
        b_re = b.real / k
        b_im = b.imag / k
        # The "current" SU(2) element from the staple is
        # M = ((a -conj(b); b conj(a))) / k = (a_re + i a_im, -b_re + i b_im;
        #                                       b_re + i b_im, a_re - i a_im)
        M = np.array([[a_re + 1j * a_im, -b_re + 1j * b_im],
                      [b_re + 1j * b_im, a_re - 1j * a_im]])
        # New SU(2) = x * M^{-1}
        x_su2 = x_to_su2(x)
        V_su2 = x_su2 @ np.conj(M.T)  # M is unitary; inverse = conjugate transpose
        # Build W (3x3) with V_su2 in (i,j) sub-block
        W = np.eye(3, dtype=complex)
        W[i, i] = V_su2[0, 0]
        W[i, j] = V_su2[0, 1]
        W[j, i] = V_su2[1, 0]
        W[j, j] = V_su2[1, 1]
        # Update
        U = W @ U
        # Re-unitarize occasionally (numerical drift)
        if (i, j) == (1, 2):
            # Project back to SU(3): QR + det fix
            Q, R = np.linalg.qr(U)
            phases = np.diagonal(R) / np.abs(np.diagonal(R))
            Q = Q * np.conj(phases)[np.newaxis, :]
            detQ = np.linalg.det(Q)
            Q[:, -1] *= np.conj(detQ)
            U = Q
    return U


# Simpler approach: use standard Metropolis instead of Cabibbo-Marinari
# Avoids CM complexity for this benchmark.

_TS_CACHE = None

def _get_Ts():
    global _TS_CACHE
    if _TS_CACHE is None:
        _TS_CACHE = gell_mann_T()
    return _TS_CACHE


def metropolis_su3_step(U_old, staple, beta, rng, eps=0.3):
    """
    Single-link Metropolis-Hastings update.
    Trial: U_new = R U_old where R = exp(i sum_a alpha_a T_a) with small alpha.
    Action: S = -(beta/N_c) Re Tr(U_link @ staple)
    Acceptance: min(1, exp(-(S_new - S_old)))
              = min(1, exp(+(beta/N_c)(Re Tr(U_new staple) - Re Tr(U_old staple))))
    """
    from scipy.linalg import expm
    Ts = _get_Ts()
    alpha = rng.standard_normal(8) * eps
    A = sum(a * T for a, T in zip(alpha, Ts))
    R = expm(1j * A)
    U_new = R @ U_old
    # delta_S = -(beta/N_c) [Re Tr(U_new staple) - Re Tr(U_old staple)]
    re_old = np.trace(U_old @ staple).real
    re_new = np.trace(U_new @ staple).real
    dS = -(beta / 3.0) * (re_new - re_old)
    # Acceptance prob = exp(-dS)
    if dS <= 0 or rng.uniform(0, 1) < np.exp(-dS):
        return U_new, True
    return U_old, False


# -------------------------------------------------------------------
# 4D Wilson lattice MC
# -------------------------------------------------------------------

class WilsonLattice4D:
    """4D periodic SU(3) Wilson lattice with link-by-link MC."""

    def __init__(self, Lx, Ly, Lz, Lt, beta, seed=42):
        self.Lx, self.Ly, self.Lz, self.Lt = Lx, Ly, Lz, Lt
        self.beta = beta
        self.rng = default_rng(seed)
        # U[mu, t, z, y, x] = link from site (t,z,y,x) in direction mu
        # mu = 0 (x), 1 (y), 2 (z), 3 (t)
        self.U = np.zeros((4, Lt, Lz, Ly, Lx, 3, 3), dtype=complex)
        # Initialize cold (identity)
        for mu in range(4):
            self.U[mu] = np.eye(3)[None, None, None, None] * np.ones(
                (Lt, Lz, Ly, Lx, 1, 1), dtype=complex
            )

    def site_idx(self, t, z, y, x):
        return (t % self.Lt, z % self.Lz, y % self.Ly, x % self.Lx)

    def get_link(self, mu, t, z, y, x):
        idx = self.site_idx(t, z, y, x)
        return self.U[mu, idx[0], idx[1], idx[2], idx[3]]

    def shift(self, t, z, y, x, mu, sgn=+1):
        delta = [0, 0, 0, 0]
        delta[3 - mu] = sgn  # mu=0 -> shift x, mu=1 -> y, mu=2 -> z, mu=3 -> t
        # Indices: (t, z, y, x), mu=0 is x
        return (t + (delta[0] if False else 0),  # placeholder
                z, y, x)  # We handle below

    def staple_sum(self, mu, t, z, y, x):
        """
        Sum of 6 staples around link U_mu(site). Each plaquette through the link
        is Tr[U_mu(site) @ staple_contribution]. Staple = sum over plaquettes.

        Forward plaquette in (mu, nu) plane at site:
            U_mu(s) U_nu(s+mu) U_mu(s+nu)^dag U_nu(s)^dag
            staple_fwd = U_nu(s+mu) U_mu(s+nu)^dag U_nu(s)^dag

        Backward plaquette in (mu, nu) plane at site s-nu:
            U_mu(s-nu) U_nu(s-nu+mu) U_mu(s)^dag U_nu(s-nu)^dag
        We need U_mu(s) (not U_mu(s)^dag). Use Re Tr U_p = Re Tr U_p^dag,
        so Re Tr [...U_mu(s)^dag... ] = Re Tr [U_mu(s) ... ].
        Backward plaquette daggered:
            (U_mu(s-nu) U_nu(s-nu+mu) U_mu(s)^dag U_nu(s-nu)^dag)^dag
            = U_nu(s-nu) U_mu(s) U_nu(s-nu+mu)^dag U_mu(s-nu)^dag
        Extract U_mu(s):
            staple_bwd = U_nu(s-nu+mu)^dag U_mu(s-nu)^dag U_nu(s-nu)

        Total staple = sum_{nu != mu} (staple_fwd + staple_bwd).
        """
        Lx, Ly, Lz, Lt = self.Lx, self.Ly, self.Lz, self.Lt
        coord = [t, z, y, x]
        ax_idx = [3, 2, 1, 0]  # mu=0 -> coord[3] = x, etc.

        S = np.zeros((3, 3), dtype=complex)
        for nu in range(4):
            if nu == mu:
                continue
            # site + mu
            cm = list(coord)
            cm[ax_idx[mu]] = (cm[ax_idx[mu]] + 1) % [Lx, Ly, Lz, Lt][mu]
            # site + nu
            cn = list(coord)
            cn[ax_idx[nu]] = (cn[ax_idx[nu]] + 1) % [Lx, Ly, Lz, Lt][nu]
            U_nu_pm = self.U[nu, cm[0], cm[1], cm[2], cm[3]]      # U_nu(s+mu)
            U_mu_pn = self.U[mu, cn[0], cn[1], cn[2], cn[3]]      # U_mu(s+nu)
            U_nu_s = self.U[nu, coord[0], coord[1], coord[2], coord[3]]  # U_nu(s)
            S += U_nu_pm @ np.conj(U_mu_pn.T) @ np.conj(U_nu_s.T)

            # site - nu
            cn_m = list(coord)
            cn_m[ax_idx[nu]] = (cn_m[ax_idx[nu]] - 1) % [Lx, Ly, Lz, Lt][nu]
            # site - nu + mu
            cn_m_pm = list(cn_m)
            cn_m_pm[ax_idx[mu]] = (cn_m_pm[ax_idx[mu]] + 1) % [Lx, Ly, Lz, Lt][mu]
            U_nu_pmn = self.U[nu, cn_m_pm[0], cn_m_pm[1], cn_m_pm[2], cn_m_pm[3]]  # U_nu(s-nu+mu)
            U_mu_mn = self.U[mu, cn_m[0], cn_m[1], cn_m[2], cn_m[3]]               # U_mu(s-nu)
            U_nu_mn = self.U[nu, cn_m[0], cn_m[1], cn_m[2], cn_m[3]]               # U_nu(s-nu)
            S += np.conj(U_nu_pmn.T) @ np.conj(U_mu_mn.T) @ U_nu_mn
        return S

    def metropolis_sweep(self, eps=0.3):
        """One full sweep of all links via Metropolis."""
        accepted = 0
        total = 0
        for mu in range(4):
            for t in range(self.Lt):
                for z in range(self.Lz):
                    for y in range(self.Ly):
                        for x in range(self.Lx):
                            U_old = self.U[mu, t, z, y, x]
                            staple = self.staple_sum(mu, t, z, y, x)
                            U_new, acc = metropolis_su3_step(
                                U_old, staple, self.beta, self.rng, eps
                            )
                            self.U[mu, t, z, y, x] = U_new
                            if acc:
                                accepted += 1
                            total += 1
        return accepted / total

    def measure_plaquette(self):
        """<Re Tr U_p / N_c> averaged over all plaquettes."""
        total = 0.0
        n_plaq = 0
        Lx, Ly, Lz, Lt = self.Lx, self.Ly, self.Lz, self.Lt
        ax_idx = [3, 2, 1, 0]
        for t in range(Lt):
            for z in range(Lz):
                for y in range(Ly):
                    for x in range(Lx):
                        coord = [t, z, y, x]
                        for mu in range(4):
                            for nu in range(mu + 1, 4):
                                cm = list(coord)
                                cm[ax_idx[mu]] = (cm[ax_idx[mu]] + 1) \
                                    % [Lx, Ly, Lz, Lt][mu]
                                cn = list(coord)
                                cn[ax_idx[nu]] = (cn[ax_idx[nu]] + 1) \
                                    % [Lx, Ly, Lz, Lt][nu]
                                U1 = self.U[mu, coord[0], coord[1], coord[2], coord[3]]
                                U2 = self.U[nu, cm[0], cm[1], cm[2], cm[3]]
                                U3 = self.U[mu, cn[0], cn[1], cn[2], cn[3]]
                                U4 = self.U[nu, coord[0], coord[1], coord[2], coord[3]]
                                P = U1 @ U2 @ np.conj(U3.T) @ np.conj(U4.T)
                                total += np.trace(P).real / 3.0
                                n_plaq += 1
        return total / n_plaq

    def measure_spatial_plaquette(self):
        """<Re Tr U_p / N_c> averaged over SPATIAL (x-y, x-z, y-z) plaquettes only."""
        total = 0.0
        n_plaq = 0
        Lx, Ly, Lz, Lt = self.Lx, self.Ly, self.Lz, self.Lt
        ax_idx = [3, 2, 1, 0]
        for t in range(Lt):
            for z in range(Lz):
                for y in range(Ly):
                    for x in range(Lx):
                        coord = [t, z, y, x]
                        # Spatial plaquettes only: (x,y), (x,z), (y,z)
                        for (mu, nu) in [(0, 1), (0, 2), (1, 2)]:
                            cm = list(coord)
                            cm[ax_idx[mu]] = (cm[ax_idx[mu]] + 1) \
                                % [Lx, Ly, Lz, Lt][mu]
                            cn = list(coord)
                            cn[ax_idx[nu]] = (cn[ax_idx[nu]] + 1) \
                                % [Lx, Ly, Lz, Lt][nu]
                            U1 = self.U[mu, coord[0], coord[1], coord[2], coord[3]]
                            U2 = self.U[nu, cm[0], cm[1], cm[2], cm[3]]
                            U3 = self.U[mu, cn[0], cn[1], cn[2], cn[3]]
                            U4 = self.U[nu, coord[0], coord[1], coord[2], coord[3]]
                            P = U1 @ U2 @ np.conj(U3.T) @ np.conj(U4.T)
                            total += np.trace(P).real / 3.0
                            n_plaq += 1
        return total / n_plaq


def run_wilson_4d_mc(Lx, Ly, Lz, Lt, beta, n_therm=100, n_meas=200, seed=42,
                       eps=0.1):
    """Run Wilson 4D MC and return mean <P>."""
    print(f"\n--- Wilson 4D MC: {Lx}x{Ly}x{Lz}x{Lt}, beta={beta:.2f}, eps={eps} ---")
    lat = WilsonLattice4D(Lx, Ly, Lz, Lt, beta, seed)
    print(f"  Thermalizing {n_therm} sweeps...")
    t0 = time.time()
    for s in range(n_therm):
        ar = lat.metropolis_sweep(eps=eps)
        if (s + 1) % 100 == 0:
            P = lat.measure_plaquette()
            print(f"    sweep {s+1}: <P>={P:.4f}, accept={ar:.2f}")
    print(f"  Measuring {n_meas} sweeps...")
    measurements_all = []
    measurements_sp = []
    for s in range(n_meas):
        lat.metropolis_sweep(eps=eps)
        P_all = lat.measure_plaquette()
        P_sp = lat.measure_spatial_plaquette()
        measurements_all.append(P_all)
        measurements_sp.append(P_sp)
    P_all_mean = np.mean(measurements_all)
    P_all_std = np.std(measurements_all, ddof=1) / np.sqrt(len(measurements_all))
    P_sp_mean = np.mean(measurements_sp)
    P_sp_std = np.std(measurements_sp, ddof=1) / np.sqrt(len(measurements_sp))
    dt = time.time() - t0
    print(f"  Total time: {dt:.1f}s")
    print(f"  <P>_all     = {P_all_mean:.4f} +/- {P_all_std:.4f}")
    print(f"  <P>_spatial = {P_sp_mean:.4f} +/- {P_sp_std:.4f}")
    return {
        'Lx': Lx, 'Ly': Ly, 'Lz': Lz, 'Lt': Lt,
        'beta': beta,
        'P_all_mean': P_all_mean, 'P_all_std': P_all_std,
        'P_sp_mean': P_sp_mean, 'P_sp_std': P_sp_std,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("Wilson 4D MC benchmark on small spatial torus")
    print("=" * 70)
    print()
    print("Goal: independent benchmark for the 2x2 spatial torus KS Hamiltonian")
    print("via 4D Euclidean lattice MC at large N_t (Hamilton limit).")
    print()

    # Beta = 6/g^2 for SU(3); g^2=1 means beta=6 (canonical Wilson value)
    # Use eps=0.1 for proper thermalization at beta=6
    print("[1] 2x2x2x8 lattice at beta=6 (g^2=1)")
    r1 = run_wilson_4d_mc(2, 2, 2, 8, 6.0, n_therm=1000, n_meas=2000, seed=42, eps=0.1)

    print("\n[2] 2x2x2x16 lattice at beta=6 (Hamilton limit closer)")
    r2 = run_wilson_4d_mc(2, 2, 2, 16, 6.0, n_therm=1000, n_meas=1000, seed=42, eps=0.1)

    print("\n[3] 2x2x2x32 lattice at beta=6 (close to Hamilton limit)")
    r3 = run_wilson_4d_mc(2, 2, 2, 32, 6.0, n_therm=1000, n_meas=500, seed=42, eps=0.1)

    print("\n[4] 4x4x4x4 at beta=6 (intermediate volume reference)")
    r4 = run_wilson_4d_mc(4, 4, 4, 4, 6.0, n_therm=1000, n_meas=500, seed=42, eps=0.1)

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    for r in [r1, r2, r3, r4]:
        print(f"  {r['Lx']}x{r['Ly']}x{r['Lz']}x{r['Lt']}, beta={r['beta']:.1f}: "
              f"<P>_all = {r['P_all_mean']:.4f}+/-{r['P_all_std']:.4f}, "
              f"<P>_spatial = {r['P_sp_mean']:.4f}+/-{r['P_sp_std']:.4f}")
    print()
    print("Reference: large-volume Wilson MC at beta=6 gives <P> ~ 0.5934.")
    print("If small-volume <P> matches large-volume, the 2x2 spatial torus")
    print("can support <P> ~ 0.55-0.60 and the spin-network ED truncation")
    print("error is the framework gap.")
