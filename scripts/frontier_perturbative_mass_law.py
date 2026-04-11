#!/usr/bin/env python3
"""
Perturbative extraction of Newton's mass law on a Wilson 3D lattice.

Motivation:
  The Hartree mean-field two-orbital approach cannot cleanly separate the
  mutual mass channel from self-field contamination. The self-potential phi
  enters the Hamiltonian diagonal alongside the inertial mass, so varying
  mass changes both inertia AND the self-potential well depth.

  At first order in G (weak coupling), the mutual acceleration is analytically
  separable from the self-field:

    a_mutual(A<-B) = -<psi_A| nabla V_partner |psi_A>

  where V_partner = G * K * |psi_B|^2, and K = (L + mu^2 I)^{-1} is the
  Green's function of the screened Poisson operator.

  The mass dependence enters through |psi_B|^2 which scales with M_B (the
  source amplitude). At first order the partner's contribution is SEPARATE
  from the self-contribution, so a_mutual should scale as M_B cleanly.

Protocol:
  1. Build Wilson 3D open-BC lattice, side=20, mu2=0.001
  2. Compute Green's function K = -(L - mu2*I - REG*I)^{-1}
  3. For two Gaussians at separation d:
     a. V_partner = G * K * |psi_B|^2  (partner's contribution to phi)
     b. Compute gradient of V_partner along x at psi_A's location
     c. a_mutual(A<-B) = -<psi_A| dV/dx |psi_A>  (force expectation value)
  4. Vary partner amplitude (M_B) and separation d
  5. Check: does a_mutual proportional to M_B? proportional to 1/d^2?
  6. Compare perturbative prediction against full Hartree simulation

This is a THEORETICAL first-order calculation, not a dynamical simulation.
"""

from __future__ import annotations

import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

# ── Physics parameters (matching confirmed Newton exponent results) ──
MASS = 0.30
WILSON_R = 1.0
G_VAL = 5.0
MU2 = 0.001
REG = 1e-3
SIGMA = 1.0
SIDE = 20
N = SIDE ** 3

# ── Sweep parameters ──
MASS_WEIGHTS = [0.25, 0.5, 1.0, 2.0, 3.0, 4.0]
SEPARATIONS = [3, 4, 5, 6, 7, 8, 9, 10, 12]
G_SWEEP = [1.0, 2.0, 5.0, 10.0]


def build_lattice():
    """Build open-BC 3D cubic lattice structures."""
    xs = np.arange(SIDE)
    gx, gy, gz = np.meshgrid(xs, xs, xs, indexing="ij")
    pos = np.column_stack([gx.ravel(), gy.ravel(), gz.ravel()])

    idx = np.arange(N).reshape(SIDE, SIDE, SIDE)

    # Forward edges in each direction
    fwd_rows_list, fwd_cols_list = [], []
    # +x
    fwd_rows_list.append(idx[:-1, :, :].ravel())
    fwd_cols_list.append(idx[1:, :, :].ravel())
    # +y
    fwd_rows_list.append(idx[:, :-1, :].ravel())
    fwd_cols_list.append(idx[:, 1:, :].ravel())
    # +z
    fwd_rows_list.append(idx[:, :, :-1].ravel())
    fwd_cols_list.append(idx[:, :, 1:].ravel())

    fwd_rows = np.concatenate(fwd_rows_list)
    fwd_cols = np.concatenate(fwd_cols_list)

    # Adjacency (symmetric)
    adj_rows = np.concatenate([fwd_rows, fwd_cols])
    adj_cols = np.concatenate([fwd_cols, fwd_rows])
    ones = np.ones(len(adj_rows))
    adj = sparse.csr_matrix((ones, (adj_rows, adj_cols)), shape=(N, N))

    degree = np.array(adj.sum(axis=1)).ravel()
    lap = adj - sparse.diags(degree, format="csr")

    # Poisson operator: (L - mu2*I - REG*I)
    poisson_op = (lap - (MU2 + REG) * sparse.eye(N)).tocsc()

    return pos, lap, poisson_op, degree


def gaussian_wavepacket(pos, center, sigma=SIGMA, amplitude=1.0):
    """Normalized Gaussian wavepacket with controllable amplitude (mass weight)."""
    c = np.asarray(center, dtype=float)
    r2 = np.sum((pos - c) ** 2, axis=1)
    psi = np.exp(-r2 / (2 * sigma ** 2)).astype(complex)
    psi /= np.linalg.norm(psi)
    # Scale density by amplitude: |psi|^2 integrates to amplitude
    psi *= np.sqrt(amplitude)
    return psi


def solve_partner_potential(poisson_op, rho_partner, G):
    """Compute V_partner = phi from partner's density alone.

    Poisson equation: (L - mu2*I) phi = -4*pi*G * rho
    So phi = -(L - mu2*I)^{-1} * 4*pi*G * rho = K * 4*pi*G * rho
    where K = -(L - mu2*I - REG*I)^{-1} (with regularization).
    """
    rhs = -4.0 * np.pi * G * rho_partner
    return spsolve(poisson_op, rhs).real


def compute_gradient_x(pos, phi):
    """Compute dV/dx using finite differences on the lattice.

    For each site, estimate dV/dx from neighbors in the x-direction.
    Central difference where possible, one-sided at boundaries.
    """
    grad = np.zeros(N)
    idx = np.arange(N).reshape(SIDE, SIDE, SIDE)

    # Central difference for interior
    for x in range(1, SIDE - 1):
        for y in range(SIDE):
            for z in range(SIDE):
                i = idx[x, y, z]
                ip = idx[x + 1, y, z]
                im = idx[x - 1, y, z]
                grad[i] = (phi[ip] - phi[im]) / 2.0

    # Forward difference at x=0
    for y in range(SIDE):
        for z in range(SIDE):
            i = idx[0, y, z]
            ip = idx[1, y, z]
            grad[i] = phi[ip] - phi[i]

    # Backward difference at x=SIDE-1
    for y in range(SIDE):
        for z in range(SIDE):
            i = idx[SIDE - 1, y, z]
            im = idx[SIDE - 2, y, z]
            grad[i] = phi[i] - phi[im]

    return grad


def compute_gradient_x_vectorized(phi):
    """Vectorized dV/dx using central differences on the 3D grid."""
    phi_3d = phi.reshape(SIDE, SIDE, SIDE)
    grad_3d = np.zeros_like(phi_3d)

    # Central difference for interior
    grad_3d[1:-1, :, :] = (phi_3d[2:, :, :] - phi_3d[:-2, :, :]) / 2.0
    # Forward difference at x=0
    grad_3d[0, :, :] = phi_3d[1, :, :] - phi_3d[0, :, :]
    # Backward difference at x=SIDE-1
    grad_3d[-1, :, :] = phi_3d[-1, :, :] - phi_3d[-2, :, :]

    return grad_3d.ravel()


def perturbative_acceleration(pos, poisson_op, psi_a, psi_b, G):
    """First-order perturbative mutual acceleration of A due to B.

    a_mutual(A<-B) = -<psi_A| dV_partner/dx |psi_A>

    where V_partner is the potential sourced by |psi_B|^2 alone.
    """
    rho_b = np.abs(psi_b) ** 2
    V_partner = solve_partner_potential(poisson_op, rho_b, G)
    dV_dx = compute_gradient_x_vectorized(V_partner)

    # Expectation value: <psi_A| dV/dx |psi_A>
    rho_a = np.abs(psi_a) ** 2
    force_expectation = np.sum(rho_a * dV_dx)

    # Mutual acceleration = -dV/dx (force = -grad V, acceleration = force/m_inertial)
    # At first order, the inertial mass is just MASS (no self-field correction)
    a_mutual = -force_expectation

    return a_mutual, V_partner


def run_hartree_acceleration(pos, poisson_op, degree, psi_a0, psi_b0, G, dt=0.08, n_steps=15):
    """Full Hartree evolution for comparison. Returns early-time mutual acceleration."""
    from scipy.sparse.linalg import expm_multiply

    fwd_rows_list, fwd_cols_list = [], []
    idx_3d = np.arange(N).reshape(SIDE, SIDE, SIDE)
    fwd_rows_list.append(idx_3d[:-1, :, :].ravel())
    fwd_cols_list.append(idx_3d[1:, :, :].ravel())
    fwd_rows_list.append(idx_3d[:, :-1, :].ravel())
    fwd_cols_list.append(idx_3d[:, 1:, :].ravel())
    fwd_rows_list.append(idx_3d[:, :, :-1].ravel())
    fwd_cols_list.append(idx_3d[:, :, 1:].ravel())
    fwd_rows = np.concatenate(fwd_rows_list)
    fwd_cols = np.concatenate(fwd_cols_list)

    # Off-diagonal Hamiltonian
    n_fwd = len(fwd_rows)
    hop_fwd = np.full(n_fwd, -0.5j + 0.5 * WILSON_R)
    hop_bwd = np.full(n_fwd, +0.5j + 0.5 * WILSON_R)
    h_rows = np.concatenate([fwd_rows, fwd_cols])
    h_cols = np.concatenate([fwd_cols, fwd_rows])
    h_vals = np.concatenate([hop_fwd, hop_bwd])
    H_offdiag = sparse.csr_matrix((h_vals, (h_rows, h_cols)), shape=(N, N))
    H_diag_static = MASS + 0.5 * WILSON_R * degree

    def build_H(phi):
        return H_offdiag + sparse.diags(H_diag_static + phi, format="csr")

    def com_x(psi):
        rho = np.abs(psi) ** 2
        return float(np.dot(rho, pos[:, 0]) / max(np.sum(rho), 1e-30))

    # SHARED evolution
    seps = {}
    for mode in ("SHARED", "SELF_ONLY"):
        psi_a = psi_a0.copy()
        psi_b = psi_b0.copy()
        sep_t = np.zeros(n_steps + 1)
        sep_t[0] = com_x(psi_b) - com_x(psi_a)

        for t in range(n_steps):
            rho_a = np.abs(psi_a) ** 2
            rho_b = np.abs(psi_b) ** 2
            if mode == "SHARED":
                phi = solve_partner_potential(poisson_op, rho_a + rho_b, G)
                phi_a = phi_b = phi
            else:
                phi_a = solve_partner_potential(poisson_op, rho_a, G)
                phi_b = solve_partner_potential(poisson_op, rho_b, G)

            H_a = build_H(phi_a)
            H_b = build_H(phi_b)
            psi_a = expm_multiply(-1j * dt * H_a, psi_a)
            psi_b = expm_multiply(-1j * dt * H_b, psi_b)
            psi_a /= np.linalg.norm(psi_a)
            psi_b /= np.linalg.norm(psi_b)
            sep_t[t + 1] = com_x(psi_b) - com_x(psi_a)

        seps[mode] = sep_t

    # Acceleration from finite differences
    def accel(sep):
        a = np.zeros(len(sep))
        a[1:-1] = (sep[2:] - 2 * sep[1:-1] + sep[:-2]) / dt ** 2
        a[0] = a[1]
        a[-1] = a[-2]
        return a

    a_shared = accel(seps["SHARED"])
    a_self = accel(seps["SELF_ONLY"])
    a_mutual = a_shared - a_self
    early = slice(2, min(11, n_steps + 1))
    return float(np.mean(a_mutual[early]))


def power_law_fit(xs, ys):
    """Fit log|y| = alpha * log(x) + const. Return alpha, stderr, R^2."""
    lx = np.log(np.asarray(xs, dtype=float))
    ly = np.log(np.asarray(ys, dtype=float))
    n = len(lx)
    slope, intercept = np.polyfit(lx, ly, 1)
    fit = slope * lx + intercept
    ss_res = float(np.sum((ly - fit) ** 2))
    ss_tot = float(np.sum((ly - np.mean(ly)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    if n > 2 and ss_tot > 0:
        mse = ss_res / (n - 2)
        sx2 = float(np.sum((lx - np.mean(lx)) ** 2))
        se = np.sqrt(mse / sx2) if sx2 > 0 else float("inf")
    else:
        se = float("inf")
    return float(slope), float(se), float(r2)


def main():
    t_start = time.time()

    print("=" * 96)
    print("PERTURBATIVE MASS LAW: First-Order Extraction of Newton's F ~ M_B / d^2")
    print("Wilson 3D open-BC lattice")
    print("=" * 96)
    print(f"MASS={MASS}, WILSON_R={WILSON_R}, G={G_VAL}, mu2={MU2}, SIDE={SIDE}")
    print(f"SIGMA={SIGMA}, REG={REG}")
    print(f"Mass weights (M_B): {MASS_WEIGHTS}")
    print(f"Separations: {SEPARATIONS}")
    print()
    print("KEY INSIGHT: At first order in G, the mutual acceleration")
    print("  a(A<-B) = -<psi_A| d/dx [G * K * |psi_B|^2] |psi_A>")
    print("is LINEAR in |psi_B|^2 (hence linear in M_B), with NO self-field mixing.")
    print()

    # Build lattice
    print(f"Building {SIDE}^3 = {N} site lattice...", end=" ", flush=True)
    t0 = time.time()
    pos, lap, poisson_op, degree = build_lattice()
    print(f"done ({time.time() - t0:.1f}s)")
    print()

    center = SIDE // 2

    # ================================================================
    # PHASE 1: Mass dependence at fixed separation
    # ================================================================
    d_fixed = 6
    print("=" * 96)
    print(f"PHASE 1: Mass dependence (fixed d={d_fixed}, G={G_VAL})")
    print("=" * 96)
    print(f"  Varying M_B (partner amplitude^2), measuring a_mutual(A<-B)")
    print()

    x_a = center - d_fixed // 2
    x_b = center + (d_fixed - d_fixed // 2)
    center_a = (x_a, center, center)
    center_b = (x_b, center, center)

    # Fixed wavepacket A (unit amplitude)
    psi_a = gaussian_wavepacket(pos, center_a, amplitude=1.0)

    mass_results = []
    for m_b in MASS_WEIGHTS:
        t0 = time.time()
        psi_b = gaussian_wavepacket(pos, center_b, amplitude=m_b)
        a_pert, V_partner = perturbative_acceleration(pos, poisson_op, psi_a, psi_b, G_VAL)
        elapsed = time.time() - t0

        # V_partner at A's center
        idx_a = int(x_a * SIDE ** 2 + center * SIDE + center)
        V_at_A = V_partner[idx_a]

        mass_results.append({
            "m_b": m_b,
            "a_pert": a_pert,
            "V_at_A": V_at_A,
        })

        print(
            f"  M_B={m_b:5.2f}: a_pert={a_pert:+.8e}  "
            f"V_partner(A)={V_at_A:+.6e}  ({elapsed:.2f}s)"
        )

    print()

    # Fit mass exponent: a_pert vs M_B
    ms = [r["m_b"] for r in mass_results]
    a_vals = [abs(r["a_pert"]) for r in mass_results]
    if all(a > 0 for a in a_vals):
        mass_exp, mass_se, mass_r2 = power_law_fit(ms, a_vals)
        print(f"  MASS EXPONENT: |a_pert| ~ M_B^{mass_exp:.4f}")
        print(f"    Standard error: {mass_se:.4f}")
        print(f"    R^2: {mass_r2:.6f}")
        print(f"    Expected (Newton): 1.000")
        print(f"    Deviation: {abs(mass_exp - 1.0):.4f}")
    else:
        mass_exp = float("nan")
        mass_r2 = float("nan")
        print("  WARNING: some accelerations are zero or negative, cannot fit")
    print()

    # Check linearity directly: ratio a_pert / M_B should be constant
    print("  LINEARITY CHECK (a_pert / M_B should be constant):")
    ratios = []
    for r in mass_results:
        ratio = r["a_pert"] / r["m_b"]
        ratios.append(ratio)
        print(f"    M_B={r['m_b']:5.2f}: a/M_B = {ratio:+.8e}")
    if ratios:
        mean_ratio = np.mean(ratios)
        std_ratio = np.std(ratios)
        cv = abs(std_ratio / mean_ratio) if abs(mean_ratio) > 1e-30 else float("inf")
        print(f"    Mean: {mean_ratio:+.8e}, Std: {std_ratio:.2e}, CV: {cv:.6f}")
        print(f"    Perfect linearity would give CV = 0")
    print()

    # ================================================================
    # PHASE 2: Distance dependence at fixed mass
    # ================================================================
    print("=" * 96)
    print(f"PHASE 2: Distance dependence (fixed M_B=1.0, G={G_VAL})")
    print("=" * 96)

    dist_results = []
    for d in SEPARATIONS:
        x_a_d = center - d // 2
        x_b_d = center + (d - d // 2)

        if x_a_d < 1 or x_b_d >= SIDE - 1:
            print(f"  d={d:2d}: SKIP (out of bounds)")
            continue

        center_a_d = (x_a_d, center, center)
        center_b_d = (x_b_d, center, center)

        psi_a_d = gaussian_wavepacket(pos, center_a_d, amplitude=1.0)
        psi_b_d = gaussian_wavepacket(pos, center_b_d, amplitude=1.0)

        t0 = time.time()
        a_pert, _ = perturbative_acceleration(pos, poisson_op, psi_a_d, psi_b_d, G_VAL)
        elapsed = time.time() - t0

        dist_results.append({"d": d, "a_pert": a_pert})
        signal = "ATTRACT" if a_pert < 0 else "REPEL"
        print(f"  d={d:2d}: a_pert={a_pert:+.8e}  [{signal}]  ({elapsed:.2f}s)")

    print()

    # Fit distance exponent
    attract_results = [r for r in dist_results if r["a_pert"] < 0]
    if len(attract_results) >= 3:
        ds = [r["d"] for r in attract_results]
        amps = [abs(r["a_pert"]) for r in attract_results]
        dist_exp, dist_se, dist_r2 = power_law_fit(ds, amps)
        print(f"  DISTANCE EXPONENT: |a_pert| ~ d^{dist_exp:.4f}")
        print(f"    Standard error: {dist_se:.4f}")
        print(f"    R^2: {dist_r2:.6f}")
        print(f"    Expected (Newton 3D): -2.000")
        print(f"    Deviation: {abs(dist_exp - (-2.0)):.4f}")
    else:
        dist_exp = float("nan")
        dist_r2 = float("nan")
        print(f"  Insufficient attractive points for distance fit ({len(attract_results)})")
    print()

    # ================================================================
    # PHASE 3: G-coupling linearity
    # ================================================================
    print("=" * 96)
    print(f"PHASE 3: Coupling linearity (d={d_fixed}, M_B=1.0)")
    print("=" * 96)
    print("  At first order, a_pert should be LINEAR in G")
    print()

    psi_a_g = gaussian_wavepacket(pos, center_a, amplitude=1.0)
    psi_b_g = gaussian_wavepacket(pos, center_b, amplitude=1.0)

    g_results = []
    for G in G_SWEEP:
        t0 = time.time()
        a_pert, _ = perturbative_acceleration(pos, poisson_op, psi_a_g, psi_b_g, G)
        elapsed = time.time() - t0
        g_results.append({"G": G, "a_pert": a_pert})
        print(f"  G={G:5.1f}: a_pert={a_pert:+.8e}  ({elapsed:.2f}s)")

    print()

    g_vals = [r["G"] for r in g_results]
    a_g_vals = [abs(r["a_pert"]) for r in g_results]
    if all(a > 0 for a in a_g_vals):
        g_exp, g_se, g_r2 = power_law_fit(g_vals, a_g_vals)
        print(f"  G EXPONENT: |a_pert| ~ G^{g_exp:.4f}")
        print(f"    R^2: {g_r2:.6f}")
        print(f"    Expected (first order): 1.000")
        print(f"    Deviation: {abs(g_exp - 1.0):.4f}")
    else:
        g_exp = float("nan")
        g_r2 = float("nan")
    print()

    # ================================================================
    # PHASE 4: Cross-check M_B x d (full 2D grid)
    # ================================================================
    print("=" * 96)
    print("PHASE 4: Full M_B x d grid (checking F ~ M_B / d^2)")
    print("=" * 96)
    print()

    grid_ms = [0.5, 1.0, 2.0, 4.0]
    grid_ds = [4, 6, 8, 10]

    grid_results = []
    for m_b in grid_ms:
        for d in grid_ds:
            x_a_g = center - d // 2
            x_b_g = center + (d - d // 2)
            if x_a_g < 1 or x_b_g >= SIDE - 1:
                continue

            psi_a_grid = gaussian_wavepacket(pos, (x_a_g, center, center), amplitude=1.0)
            psi_b_grid = gaussian_wavepacket(pos, (x_b_g, center, center), amplitude=m_b)

            a_pert, _ = perturbative_acceleration(pos, poisson_op, psi_a_grid, psi_b_grid, G_VAL)
            grid_results.append({"m_b": m_b, "d": d, "a_pert": a_pert})

    # Print grid
    print(f"  {'M_B':>6s}", end="")
    for d in grid_ds:
        print(f"  {'d='+str(d):>14s}", end="")
    print()
    print("  " + "-" * (6 + 16 * len(grid_ds)))

    for m_b in grid_ms:
        print(f"  {m_b:6.2f}", end="")
        for d in grid_ds:
            matching = [r for r in grid_results if r["m_b"] == m_b and r["d"] == d]
            if matching:
                print(f"  {matching[0]['a_pert']:+14.6e}", end="")
            else:
                print(f"  {'---':>14s}", end="")
        print()
    print()

    # Check: a * d^2 / M_B should be constant (= G * geometric factor)
    print("  NEWTON PRODUCT CHECK: a_pert * d^2 / M_B should be constant")
    products = []
    for r in grid_results:
        if r["a_pert"] != 0:
            product = r["a_pert"] * r["d"] ** 2 / r["m_b"]
            products.append(product)
            print(
                f"    M_B={r['m_b']:4.1f}, d={r['d']:2d}: "
                f"a*d^2/M_B = {product:+.6e}"
            )

    if products:
        mean_p = np.mean(products)
        std_p = np.std(products)
        cv_p = abs(std_p / mean_p) if abs(mean_p) > 1e-30 else float("inf")
        print(f"    Mean: {mean_p:+.6e}, Std: {std_p:.2e}, CV: {cv_p:.6f}")
    print()

    # ================================================================
    # PHASE 5: Compare with full Hartree at a few points
    # ================================================================
    print("=" * 96)
    print("PHASE 5: Perturbative vs Hartree comparison")
    print("=" * 96)
    print("  Running full Hartree evolution at selected (M_B, d) points...")
    print()

    comparison_points = [(1.0, 4), (1.0, 6), (1.0, 8), (2.0, 6)]
    for m_b, d in comparison_points:
        x_a_c = center - d // 2
        x_b_c = center + (d - d // 2)
        if x_a_c < 1 or x_b_c >= SIDE - 1:
            print(f"  M_B={m_b}, d={d}: SKIP (out of bounds)")
            continue

        center_a_c = (x_a_c, center, center)
        center_b_c = (x_b_c, center, center)

        # Perturbative
        psi_a_c = gaussian_wavepacket(pos, center_a_c, amplitude=1.0)
        psi_b_c = gaussian_wavepacket(pos, center_b_c, amplitude=m_b)
        a_pert_c, _ = perturbative_acceleration(pos, poisson_op, psi_a_c, psi_b_c, G_VAL)

        # Hartree (uses unit-norm wavefunctions; mass enters through source weight)
        # For the Hartree comparison, we use amplitude=1.0 for both since the
        # Hartree code uses |psi|^2 directly. Mass weighting is different.
        psi_a_h = gaussian_wavepacket(pos, center_a_c, amplitude=1.0)
        psi_b_h = gaussian_wavepacket(pos, center_b_c, amplitude=1.0)
        t0 = time.time()
        a_hartree = run_hartree_acceleration(
            pos, poisson_op, degree, psi_a_h, psi_b_h, G_VAL
        )
        elapsed = time.time() - t0

        ratio = a_pert_c / a_hartree if abs(a_hartree) > 1e-30 else float("inf")
        print(
            f"  M_B={m_b:4.1f}, d={d:2d}: "
            f"a_pert={a_pert_c:+.6e}  a_hartree={a_hartree:+.6e}  "
            f"ratio={ratio:.4f}  ({elapsed:.1f}s)"
        )
    print()

    # ================================================================
    # FINAL SUMMARY
    # ================================================================
    total_time = time.time() - t_start
    print("=" * 96)
    print("FINAL SUMMARY: Perturbative Mass Law Results")
    print("=" * 96)
    print()

    if np.isfinite(mass_exp):
        mass_pass = abs(mass_exp - 1.0) < 0.05 and mass_r2 > 0.999
        print(f"  MASS EXPONENT:     {mass_exp:+.4f} (expect +1.000)")
        print(f"    R^2 = {mass_r2:.6f}")
        print(f"    {'PASS' if mass_pass else 'FAIL'}: a_mutual ~ M_B^{mass_exp:.4f}")
    else:
        mass_pass = False
        print(f"  MASS EXPONENT:     COULD NOT FIT")

    if np.isfinite(dist_exp):
        dist_pass = abs(dist_exp - (-2.0)) < 0.3 and dist_r2 > 0.99
        print(f"  DISTANCE EXPONENT: {dist_exp:+.4f} (expect -2.000)")
        print(f"    R^2 = {dist_r2:.6f}")
        print(f"    {'PASS' if dist_pass else 'FAIL'}: a_mutual ~ d^{dist_exp:.4f}")
    else:
        dist_pass = False
        print(f"  DISTANCE EXPONENT: COULD NOT FIT")

    if np.isfinite(g_exp):
        g_pass = abs(g_exp - 1.0) < 0.05 and g_r2 > 0.999
        print(f"  G EXPONENT:        {g_exp:+.4f} (expect +1.000)")
        print(f"    R^2 = {g_r2:.6f}")
        print(f"    {'PASS' if g_pass else 'FAIL'}: a_mutual ~ G^{g_exp:.4f}")
    else:
        g_pass = False

    print()
    if mass_pass:
        print("  >>> MASS LAW CONFIRMED: F ~ M_B at first order in G <<<")
        print("  The perturbative calculation cleanly separates mutual from self-field.")
        print("  The Hartree self-field contamination is a HIGHER-ORDER effect.")
    else:
        print("  >>> MASS LAW: needs investigation <<<")

    if mass_pass and dist_pass:
        print()
        print("  >>> FULL NEWTON: F ~ G * M_B / d^2 CONFIRMED at first order <<<")

    if products:
        print()
        print(f"  Newton product a*d^2/M_B coefficient of variation: {cv_p:.6f}")
        if cv_p < 0.01:
            print("  Product law F ~ M_B / d^2 holds to < 1% across the grid")

    print(f"\n  Total runtime: {total_time:.0f}s")


if __name__ == "__main__":
    main()
