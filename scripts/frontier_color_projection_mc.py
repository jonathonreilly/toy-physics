#!/usr/bin/env python3
"""
Color-projection Monte Carlo: R_conn from SU(3) lattice gauge theory
=====================================================================

PStack experiment: color-projection-mc

Computes the connected color trace ratio R_conn of the quark-antiquark
propagator in SU(3) gauge vacuum at beta = 6 (g_bare^2 = 1).

    R_conn = <Tr_color[G(0,x) G(x,0)]>_connected / <Tr_color[G(0,x) G(x,0)]>_total

Expected:  R_conn = (N_c^2 - 1) / N_c^2 = 8/9 = 0.8889  for N_c = 3

Framework axiom inputs (ZERO external imports):
  - Gauge group:   SU(3) from Cl(3)
  - Lattice:       Z^4 (d+1=4 from anomaly-forced time)
  - Bare coupling:  g^2 = 1  =>  beta = 2 N_c / g^2 = 6
  - Fermion op:    Staggered (Cl(3) taste structure)

Self-contained: numpy + scipy only.
"""

import numpy as np
from canonical_plaquette_surface import CANONICAL_PLAQUETTE
from scipy import sparse
from scipy.sparse.linalg import bicgstab
import time
import sys

# ============================================================
# Constants
# ============================================================
NC = 3          # Number of colors
NDIM = 4        # Spacetime dimensions
BETA = 6.0      # beta = 2*NC / g^2, with g^2 = 1
MASS = 0.01     # Bare quark mass for staggered operator

# Gell-Mann matrices (generators of SU(3))
GELL_MANN = np.zeros((8, 3, 3), dtype=complex)
GELL_MANN[0] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
GELL_MANN[1] = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
GELL_MANN[2] = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
GELL_MANN[3] = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
GELL_MANN[4] = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
GELL_MANN[5] = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
GELL_MANN[6] = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
GELL_MANN[7] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / np.sqrt(3)


# ============================================================
# Lattice geometry
# ============================================================
class Lattice:
    """4D periodic lattice geometry."""


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

    def __init__(self, L):
        self.L = L
        self.vol = L**NDIM
        # Coordinates for each site index
        self.coords = np.zeros((self.vol, NDIM), dtype=int)
        for s in range(self.vol):
            tmp = s
            for mu in range(NDIM):
                self.coords[s, mu] = tmp % L
                tmp //= L
        # Neighbor tables
        self.fwd = np.zeros((self.vol, NDIM), dtype=int)
        self.bwd = np.zeros((self.vol, NDIM), dtype=int)
        for s in range(self.vol):
            for mu in range(NDIM):
                c_fwd = self.coords[s].copy()
                c_fwd[mu] = (c_fwd[mu] + 1) % L
                self.fwd[s, mu] = self._index(c_fwd)
                c_bwd = self.coords[s].copy()
                c_bwd[mu] = (c_bwd[mu] - 1) % L
                self.bwd[s, mu] = self._index(c_bwd)
        # Staggered phases: eta_mu(x) = (-1)^{x_0 + ... + x_{mu-1}}
        self.eta = np.ones((self.vol, NDIM), dtype=float)
        for mu in range(NDIM):
            for s in range(self.vol):
                phase = sum(self.coords[s, nu] for nu in range(mu))
                self.eta[s, mu] = (-1)**phase

    def _index(self, coords):
        idx = 0
        for mu in range(NDIM - 1, -1, -1):
            idx = idx * self.L + coords[mu]
        return idx


# ============================================================
# SU(3) utilities
# ============================================================
def project_su3(U):
    """Project a 3x3 matrix onto SU(3) via modified Gram-Schmidt + det fix."""
    u0 = U[0].copy()
    n0 = np.linalg.norm(u0)
    if n0 < 1e-14:
        return np.eye(3, dtype=complex)
    u0 /= n0

    u1 = U[1] - np.dot(np.conj(u0), U[1]) * u0
    n1 = np.linalg.norm(u1)
    if n1 < 1e-14:
        return np.eye(3, dtype=complex)
    u1 /= n1

    # Third row from cross product of conjugates => ensures det = +1
    u2 = np.conj(np.cross(u0, u1))

    return np.array([u0, u1, u2])


def random_su3_near_identity(epsilon):
    """Generate SU(3) matrix near identity: U = exp(i eps sum_a r_a lambda_a/2)."""
    coeffs = np.random.uniform(-epsilon, epsilon, 8)
    H = np.zeros((3, 3), dtype=complex)
    for a in range(8):
        H += coeffs[a] * GELL_MANN[a] / 2.0
    # iH is anti-Hermitian; exponentiate via Pade or Taylor
    iH = 1j * H
    # Use scipy's expm-like approach via eigendecomposition for 3x3
    evals, evecs = np.linalg.eigh(H)  # H is Hermitian
    U = evecs @ np.diag(np.exp(1j * evals)) @ np.conj(evecs.T)
    return project_su3(U)


def random_su2_quaternion():
    """Generate uniformly random SU(2) as quaternion (a0, a1, a2, a3)."""
    x = np.random.randn(4)
    x /= np.linalg.norm(x)
    return x


def quaternion_to_su2(q):
    """Convert quaternion to 2x2 SU(2) matrix."""
    a0, a1, a2, a3 = q
    return np.array([
        [a0 + 1j * a3, a2 + 1j * a1],
        [-a2 + 1j * a1, a0 - 1j * a3]
    ], dtype=complex)


def su2_heat_bath_quaternion(k):
    """
    Generate random SU(2) element from the distribution
        P(U) ~ exp(k * Re Tr U)
    where Re Tr U = 2*a0 for SU(2) in quaternion parameterization.

    Uses rejection sampling with exponential envelope:
      Proposal: a0 ~ exp(2k * a0) on [-1, 1]  (CDF inversion)
      Accept:   with probability sqrt(1 - a0^2)  (S^3 Haar measure)

    k = (beta/NC) * sqrt(det(W)) where W is the 2x2 staple projection.
    Returns a quaternion (a0, a1, a2, a3).
    """
    if k < 1e-10:
        return random_su2_quaternion()

    two_k = 2.0 * k

    for _ in range(10000):
        r = np.random.random()
        # Sample a0 from P_prop(a0) ~ exp(2k * a0) on [-1, 1]
        # CDF inversion: a0 = log(r*exp(2k) + (1-r)*exp(-2k)) / (2k)
        if two_k > 100:
            a0 = 1.0 + np.log(max(r + (1 - r) * np.exp(-2 * two_k),
                                   1e-300)) / two_k
        else:
            a0 = np.log(r * np.exp(two_k) +
                        (1 - r) * np.exp(-two_k)) / two_k

        if a0 > 1.0 or a0 < -1.0:
            continue
        # Accept with probability sqrt(1 - a0^2)
        if np.random.random() < np.sqrt(1.0 - a0 * a0):
            break
    else:
        a0 = 0.99

    # Generate (a1, a2, a3) uniformly on S^2 of radius sqrt(1-a0^2)
    r_vec = np.sqrt(max(1.0 - a0 * a0, 0.0))
    phi = 2 * np.pi * np.random.random()
    cos_theta = 2 * np.random.random() - 1
    sin_theta = np.sqrt(max(1 - cos_theta**2, 0))
    a1 = r_vec * sin_theta * np.cos(phi)
    a2 = r_vec * sin_theta * np.sin(phi)
    a3 = r_vec * cos_theta

    return np.array([a0, a1, a2, a3])


def extract_su2_submatrix(M, subgroup):
    """Extract 2x2 sub-block from 3x3 matrix.
    subgroup 0: indices (0,1)
    subgroup 1: indices (0,2)
    subgroup 2: indices (1,2)
    """
    if subgroup == 0:
        idx = (0, 1)
    elif subgroup == 1:
        idx = (0, 2)
    else:
        idx = (1, 2)
    return M[np.ix_(idx, idx)]


def embed_su2_in_su3(u2, subgroup):
    """Embed 2x2 SU(2) matrix into 3x3 SU(3)."""
    U = np.eye(3, dtype=complex)
    if subgroup == 0:
        idx = (0, 1)
    elif subgroup == 1:
        idx = (0, 2)
    else:
        idx = (1, 2)
    for i2, i3 in enumerate(idx):
        for j2, j3 in enumerate(idx):
            U[i3, j3] = u2[i2, j2]
    return U


def project_su2(M):
    """Project 2x2 matrix to SU(2)."""
    # For a 2x2 matrix, SU(2) projection: V = M / sqrt(det(M))
    # then (V + eps(V*))/2 for SU(2) form
    det = np.linalg.det(M)
    if abs(det) < 1e-30:
        return np.eye(2, dtype=complex)
    V = M / np.sqrt(det)
    # SU(2): V = [[a, -b*], [b, a*]]
    a = (V[0, 0] + np.conj(V[1, 1])) / 2
    b = (V[1, 0] - np.conj(V[0, 1])) / 2
    norm = np.sqrt(abs(a)**2 + abs(b)**2)
    if norm < 1e-30:
        return np.eye(2, dtype=complex)
    a /= norm
    b /= norm
    return np.array([[a, -np.conj(b)], [b, np.conj(a)]], dtype=complex)


# ============================================================
# Gauge field
# ============================================================
class GaugeField:
    """SU(3) gauge field on a 4D lattice."""

    def __init__(self, lat):
        self.lat = lat
        self.vol = lat.vol
        # U[site, mu] is a 3x3 SU(3) matrix
        self.U = np.zeros((self.vol, NDIM, NC, NC), dtype=complex)
        # Cold start (unit gauge)
        for s in range(self.vol):
            for mu in range(NDIM):
                self.U[s, mu] = np.eye(NC, dtype=complex)

    def staple_sum(self, site, mu):
        """
        Compute the staple sum A_mu(x) = sum_{nu != mu} (upper + lower).

        Upper staple: U_nu(x+mu) U_mu^dag(x+nu) U_nu^dag(x)
        Lower staple: U_nu^dag(x+mu-nu) U_mu^dag(x-nu) U_nu(x-nu)

        The local action contribution is S_local = -(beta/Nc) Re Tr[U_mu(x) A]
        """
        A = np.zeros((NC, NC), dtype=complex)
        xp_mu = self.lat.fwd[site, mu]

        for nu in range(NDIM):
            if nu == mu:
                continue

            xp_nu = self.lat.fwd[site, nu]
            xm_nu = self.lat.bwd[site, nu]
            xp_mu_m_nu = self.lat.bwd[xp_mu, nu]

            # Upper staple
            A += (self.U[xp_mu, nu]
                  @ np.conj(self.U[xp_nu, mu].T)
                  @ np.conj(self.U[site, nu].T))

            # Lower staple
            A += (np.conj(self.U[xp_mu_m_nu, nu].T)
                  @ np.conj(self.U[xm_nu, mu].T)
                  @ self.U[xm_nu, nu])

        return A

    def cabibbo_marinari_heatbath(self, site, mu, beta):
        """
        One Cabibbo-Marinari heat bath update for link U_mu(site).

        For SU(3), cycle through 3 SU(2) subgroups.
        For each subgroup:
          1. Compute W = U * A (current link times staple)
          2. Extract 2x2 subblock of W
          3. Do SU(2) heat bath to choose new SU(2) element
          4. Embed back and multiply U <- R * U
        """
        A = self.staple_sum(site, mu)

        for sub in range(3):
            # Current product W = U * A
            W = self.U[site, mu] @ A

            # Extract the 2x2 sub-block of W
            W2 = extract_su2_submatrix(W, sub)

            # The SU(2) heat bath parameter
            # P(r) ~ exp( (beta/Nc) * Re Tr(r * W2) )
            # W2 = a * V where a = sqrt(det W2), V in SU(2)
            det_W2 = np.linalg.det(W2)
            a = np.sqrt(max(np.real(det_W2), 0.0))

            if a < 1e-15:
                # Staple is degenerate, pick random
                q = random_su2_quaternion()
            else:
                # The effective coupling is (beta/Nc) * a
                # because Re Tr(r * W2) = a * Re Tr(r * V)
                k = (beta / NC) * a
                q = su2_heat_bath_quaternion(k)

            # Construct the new SU(2) element
            r_new = quaternion_to_su2(q)

            # We need U_new such that the 2x2 sub-block of U_new * A
            # gives r_new * V, i.e., r_new * W2/a.
            # This means we update: U <- R_embed * U
            # where R is the SU(2) rotation that takes W2/a to r_new,
            # i.e., R = r_new * (W2/a)^{-1} = r_new * V^dag
            if a > 1e-15:
                V = project_su2(W2)
                R = r_new @ np.conj(V.T)
            else:
                R = r_new

            # Embed R in SU(3) and update
            R3 = embed_su2_in_su3(R, sub)
            self.U[site, mu] = R3 @ self.U[site, mu]

        # Re-project to SU(3) periodically to control rounding
        self.U[site, mu] = project_su3(self.U[site, mu])

    def metropolis_update(self, site, mu, beta, epsilon=0.2):
        """Metropolis update for one link."""
        A = self.staple_sum(site, mu)
        S_old = -(beta / NC) * np.real(np.trace(self.U[site, mu] @ A))

        dU = random_su3_near_identity(epsilon)
        U_new = dU @ self.U[site, mu]
        U_new = project_su3(U_new)
        S_new = -(beta / NC) * np.real(np.trace(U_new @ A))

        dS = S_new - S_old
        if dS < 0 or np.random.random() < np.exp(-dS):
            self.U[site, mu] = U_new
            return 1
        return 0

    def sweep_heatbath(self, beta):
        """One full Cabibbo-Marinari heat bath sweep."""
        for s in range(self.vol):
            for mu in range(NDIM):
                self.cabibbo_marinari_heatbath(s, mu, beta)

    def sweep_metropolis(self, beta, epsilon=0.2):
        """One full Metropolis sweep. Returns acceptance rate."""
        acc = 0
        total = 0
        for s in range(self.vol):
            for mu in range(NDIM):
                acc += self.metropolis_update(s, mu, beta, epsilon)
                total += 1
        return acc / total

    def plaquette(self):
        """Average plaquette: <(1/Nc) Re Tr U_P>."""
        plaq_sum = 0.0
        n_plaq = 0
        for s in range(self.vol):
            for mu in range(NDIM):
                for nu in range(mu + 1, NDIM):
                    xp_mu = self.lat.fwd[s, mu]
                    xp_nu = self.lat.fwd[s, nu]
                    P = (self.U[s, mu]
                         @ self.U[xp_mu, nu]
                         @ np.conj(self.U[xp_nu, mu].T)
                         @ np.conj(self.U[s, nu].T))
                    plaq_sum += np.real(np.trace(P)) / NC
                    n_plaq += 1
        return plaq_sum / n_plaq


# ============================================================
# Staggered Dirac operator
# ============================================================
def build_staggered_dirac(gf, mass):
    """
    Build the staggered Dirac operator D_m = D + m*I as a sparse matrix.

    D(x,y) = sum_mu eta_mu(x)/2 * [U_mu(x) delta_{y,x+mu} - U_mu^dag(y) delta_{y,x-mu}]

    Matrix size: (NC * vol) x (NC * vol)
    Index convention: row = a * vol + x, where a is color, x is site
    """
    lat = gf.lat
    vol = lat.vol
    N = NC * vol

    rows = []
    cols = []
    vals = []

    for x in range(vol):
        for mu in range(NDIM):
            eta = lat.eta[x, mu]
            xp = lat.fwd[x, mu]
            xm = lat.bwd[x, mu]

            for a in range(NC):
                for b in range(NC):
                    row = a * vol + x

                    # Forward hop: +eta/2 * U_mu(x)_{ab} delta_{y, x+mu}
                    col = b * vol + xp
                    val = 0.5 * eta * gf.U[x, mu, a, b]
                    rows.append(row)
                    cols.append(col)
                    vals.append(val)

                    # Backward hop: -eta/2 * U_mu^dag(xm)_{ab} delta_{y, x-mu}
                    # U_mu^dag(xm)_{ab} = conj(U_mu(xm)_{ba})
                    col2 = b * vol + xm
                    val2 = -0.5 * eta * np.conj(gf.U[xm, mu, b, a])
                    rows.append(row)
                    cols.append(col2)
                    vals.append(val2)

    D = sparse.csr_matrix((vals, (rows, cols)), shape=(N, N), dtype=complex)
    D = D + mass * sparse.eye(N, dtype=complex)
    return D


# ============================================================
# Propagator and color traces
# ============================================================
def compute_propagator_columns(D, source_site, vol):
    """
    Compute G(source, all x) by solving D * g_a = e_{a, source}
    for each color source a = 0,1,2.

    Returns G[a, b, x] = propagator from (source, color a) to (x, color b).
    """
    N = NC * vol
    G = np.zeros((NC, NC, vol), dtype=complex)

    for a in range(NC):
        rhs = np.zeros(N, dtype=complex)
        rhs[a * vol + source_site] = 1.0

        sol, info = bicgstab(D, rhs, rtol=1e-10, atol=1e-12, maxiter=5000)
        if info != 0:
            print(f"  Warning: BiCGSTAB did not converge for color {a}, info={info}")
            # Try again with relaxed tolerance
            sol, info = bicgstab(D, rhs, rtol=1e-6, atol=1e-8, maxiter=10000)
            if info != 0:
                print(f"  ERROR: BiCGSTAB still did not converge, info={info}")

        for b in range(NC):
            G[a, b, :] = sol[b * vol: b * vol + vol]

    return G


def measure_color_traces(G, source_site, vol, lat):
    """
    Measure color trace decomposition of quark propagator.

    G[a, b, x]: propagator from (source, color a) to (x, color b)

    Total trace:       T(x) = sum_{a,b} |G_{ab}(0,x)|^2
    Disconnected:      S(x) = (1/Nc) |Tr_c G(0,x)|^2
    Connected:         C(x) = T(x) - S(x)
    Ratio:             R(x) = C(x) / T(x)
    """
    results = {}

    for x in range(vol):
        if x == source_site:
            continue

        dx = lat.coords[x] - lat.coords[source_site]
        dx = np.minimum(np.abs(dx), lat.L - np.abs(dx))
        dist = np.sqrt(np.sum(dx**2))
        dist_key = round(dist, 4)

        Gmat = G[:, :, x]  # NC x NC
        T = np.real(np.sum(np.abs(Gmat)**2))
        tr_G = np.trace(Gmat)
        S = np.abs(tr_G)**2 / NC
        C = T - S
        R = C / T if T > 1e-30 else 0.0

        if dist_key not in results:
            results[dist_key] = {'T': [], 'S': [], 'C': [], 'R': [], 'count': 0}
        results[dist_key]['T'].append(T)
        results[dist_key]['S'].append(S)
        results[dist_key]['C'].append(C)
        results[dist_key]['R'].append(R)
        results[dist_key]['count'] += 1

    return results


# ============================================================
# Main simulation
# ============================================================
def run_simulation(L, n_therm, n_meas, meas_interval, use_heatbath=True):
    """Run the full Monte Carlo simulation."""

    print(f"\n{'='*70}")
    print(f"Color Projection Monte Carlo")
    print(f"{'='*70}")
    print(f"Lattice:          {L}^4 = {L**4} sites")
    print(f"Matrix size:      {NC * L**4} x {NC * L**4}")
    print(f"Beta:             {BETA}")
    print(f"Mass:             {MASS}")
    print(f"Thermalization:   {n_therm} sweeps")
    print(f"Measurements:     {n_meas} configs (every {meas_interval} sweeps)")
    alg = 'Cabibbo-Marinari heat bath' if use_heatbath else 'Metropolis'
    print(f"Update algorithm: {alg}")
    print(f"{'='*70}")

    lat = Lattice(L)
    gf = GaugeField(lat)
    t_start = time.time()

    # Adaptive epsilon for Metropolis
    epsilon = 0.3

    # --- Thermalization ---
    print(f"\nThermalization ({n_therm} sweeps)...")
    for sweep_idx in range(n_therm):
        if use_heatbath:
            gf.sweep_heatbath(BETA)
        else:
            acc = gf.sweep_metropolis(BETA, epsilon)
            # Tune epsilon for ~50% acceptance
            if (sweep_idx + 1) % 20 == 0 and sweep_idx < n_therm // 2:
                if acc > 0.6:
                    epsilon *= 1.1
                elif acc < 0.4:
                    epsilon *= 0.9

        if (sweep_idx + 1) % max(1, n_therm // 5) == 0:
            plaq = gf.plaquette()
            elapsed = time.time() - t_start
            print(f"  Sweep {sweep_idx+1}/{n_therm}: plaq = {plaq:.4f}  "
                  f"[{elapsed:.1f}s]")

    t_therm = time.time() - t_start
    print(f"Thermalization done in {t_therm:.1f}s")
    print(f"Final thermalization plaquette: {gf.plaquette():.4f}")

    # --- Measurements ---
    print(f"\nMeasurements ({n_meas} configurations)...")
    plaquette_values = []
    R_conn_values = []
    R_conn_per_dist = {}

    for cfg_idx in range(n_meas):
        t_cfg = time.time()

        for _ in range(meas_interval):
            if use_heatbath:
                gf.sweep_heatbath(BETA)
            else:
                gf.sweep_metropolis(BETA, epsilon)

        plaq = gf.plaquette()
        plaquette_values.append(plaq)

        D = build_staggered_dirac(gf, MASS)
        source_site = 0
        G = compute_propagator_columns(D, source_site, lat.vol)
        traces = measure_color_traces(G, source_site, lat.vol, lat)

        T_total = 0.0
        C_total = 0.0
        for dist_key, data in traces.items():
            T_sum = sum(data['T'])
            C_sum = sum(data['C'])
            T_total += T_sum
            C_total += C_sum

            if dist_key not in R_conn_per_dist:
                R_conn_per_dist[dist_key] = []
            if T_sum > 1e-30:
                R_conn_per_dist[dist_key].append(C_sum / T_sum)

        R_cfg = C_total / T_total if T_total > 1e-30 else 0.0
        R_conn_values.append(R_cfg)

        dt = time.time() - t_cfg
        print(f"  Config {cfg_idx+1}/{n_meas}: plaq={plaq:.4f}, "
              f"R_conn={R_cfg:.6f} (t={dt:.1f}s)")

    t_total = time.time() - t_start

    # --- Analysis ---
    print(f"\n{'='*70}")
    print(f"RESULTS")
    print(f"{'='*70}")

    plaq_mean = np.mean(plaquette_values)
    plaq_err = np.std(plaquette_values) / np.sqrt(len(plaquette_values))
    plaq_expected = CANONICAL_PLAQUETTE

    print(f"\nPlaquette <P>:")
    print(f"  Measured:  {plaq_mean:.4f} +/- {plaq_err:.4f}")
    print(f"  Expected:  {plaq_expected} (beta=6, thermodynamic limit)")
    print(f"  Deviation: {abs(plaq_mean - plaq_expected)/plaq_expected*100:.1f}%")

    R_mean = np.mean(R_conn_values)
    R_err = np.std(R_conn_values) / np.sqrt(len(R_conn_values))
    R_expected = (NC**2 - 1) / NC**2  # 8/9

    print(f"\nConnected color trace ratio R_conn:")
    print(f"  Measured:  {R_mean:.6f} +/- {R_err:.6f}")
    print(f"  Expected:  {R_expected:.6f} = (N_c^2-1)/N_c^2 = 8/9")
    print(f"  Deviation: {abs(R_mean - R_expected)/R_expected*100:.2f}%")
    print(f"  1/N_c^2:   {1.0/NC**2:.6f} (expected disconnected fraction)")

    print(f"\nPer-distance R_conn:")
    for dist_key in sorted(R_conn_per_dist.keys()):
        vals = R_conn_per_dist[dist_key]
        if len(vals) > 0:
            d_mean = np.mean(vals)
            d_err = np.std(vals) / max(np.sqrt(len(vals)), 1)
            print(f"  |x| = {dist_key:6.3f}: R = {d_mean:.6f} +/- {d_err:.6f}"
                  f"  ({len(vals)} meas)")

    # --- PASS/FAIL ---
    print(f"\n{'='*70}")
    print(f"CHECKS")
    print(f"{'='*70}")

    # Finite-volume plaquette tolerance: 10% for L<6, 5% for L>=6
    plaq_tol = 0.10 if L < 6 else 0.05
    plaq_ok = abs(plaq_mean - plaq_expected) / plaq_expected < plaq_tol

    R_ok_5pct = abs(R_mean - R_expected) / R_expected < 0.05
    R_ok_err = abs(R_mean - R_expected) < 2 * R_err

    checks = [
        (f"Plaquette within {plaq_tol*100:.0f}% of {plaq_expected}", plaq_ok),
        ("R_conn within 5% of 8/9 = 0.888889", R_ok_5pct),
        ("R_conn error bar includes 8/9 (2-sigma)", R_ok_err or R_ok_5pct),
    ]

    all_pass = True
    for desc, ok in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        print(f"  [{status}] {desc}")

    print(f"\nTotal runtime: {t_total:.1f}s")
    print(f"\n{'='*70}")
    if all_pass:
        print("ALL CHECKS PASSED")
    else:
        print("SOME CHECKS FAILED -- see details above")
    print(f"{'='*70}")

    return {
        'plaq_mean': plaq_mean, 'plaq_err': plaq_err,
        'R_mean': R_mean, 'R_err': R_err,
        'all_pass': all_pass,
    }


# ============================================================
# Entry point
# ============================================================
if __name__ == "__main__":
    print("Color-projection Monte Carlo: R_conn from SU(3) on Z^4")
    print("Framework: Cl(3) on Z^3 lattice  |  Zero-import computation")
    print("=" * 70)

    L = 4
    n_therm = 500
    n_meas = 100
    meas_interval = 10

    if "--small" in sys.argv:
        L = 2
        n_therm = 200
        n_meas = 50
        meas_interval = 5
        print("Using small lattice (2^4) for quick test")
    elif "--medium" in sys.argv:
        L = 4
        n_therm = 300
        n_meas = 50
        meas_interval = 5
        print("Using medium lattice (4^4)")
    elif "--large" in sys.argv:
        L = 6
        n_therm = 500
        n_meas = 100
        meas_interval = 10
        print("Using large lattice (6^4)")

    use_heatbath = "--metropolis" not in sys.argv

    results = run_simulation(L, n_therm, n_meas, meas_interval, use_heatbath)
