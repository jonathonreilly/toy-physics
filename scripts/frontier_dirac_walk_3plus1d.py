#!/usr/bin/env python3
"""
4-Component Dirac Walk in 3+1D
================================
HYPOTHESIS: A 4-component Dirac walk (standard architecture from literature,
  arXiv:1603.06442) produces isotropic 3D Klein-Gordon dispersion (R^2>0.99)
  and passes the 10-property closure card with theta-modulation gravity.

MOTIVATION: The 6-component chiral walk is a structural no-go for 3D KG
  (R^2=0.156 regardless of coin). The 4-component Dirac walk uses a tensor-
  product-like structure that couples all spatial dimensions through gamma
  matrices, which is known to reproduce the Dirac equation.

ARCHITECTURE:
  State: 4 components per site (Dirac spinor), n^3 sites
  Coin: C(m) = cos(m)*I4 + i*sin(m)*gamma0   (mass coin)
  Shift: 3 conditional shifts using gamma0*gamma_j for j=1,2,3
  Evolution per step: U = S3 * S2 * S1 * C(m)
  Gravity: m(r) = m0 * (1 - f(r)), f = strength/(r + 0.1)

FALSIFICATION: If R^2 < 0.99 on a 4-component walk, the architecture
  doesn't reproduce KG either. If closure card < 8/10, gravity coupling
  breaks physics.

SUCCESS CRITERIA:
  KG R^2 > 0.99  (6-component: 0.156)
  Closure card >= 8/10
  Unitarity error < 1e-10
"""

import numpy as np
from scipy import stats
import time


# ============================================================================
# Gamma matrices (Dirac representation)
# ============================================================================

# gamma0 = diag(I2, -I2)
gamma0 = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, -1, 0],
    [0, 0, 0, -1]
], dtype=complex)

# gamma1 = [[0, sigma_x], [-sigma_x, 0]]
gamma1 = np.array([
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, -1, 0, 0],
    [-1, 0, 0, 0]
], dtype=complex)

# gamma2 = [[0, sigma_y], [-sigma_y, 0]]
gamma2 = np.array([
    [0, 0, 0, -1j],
    [0, 0, 1j, 0],
    [0, 1j, 0, 0],
    [-1j, 0, 0, 0]
], dtype=complex)

# gamma3 = [[0, sigma_z], [-sigma_z, 0]]
gamma3 = np.array([
    [0, 0, 1, 0],
    [0, 0, 0, -1],
    [-1, 0, 0, 0],
    [0, 1, 0, 0]
], dtype=complex)

# Verify anticommutation: {gamma_mu, gamma_nu} = 2 * eta_mu_nu
gammas = [gamma0, gamma1, gamma2, gamma3]
def verify_clifford():
    for i in range(4):
        for j in range(4):
            ac = gammas[i] @ gammas[j] + gammas[j] @ gammas[i]
            if i == j:
                expected = 2 * (1 if i == 0 else -1) * np.eye(4)
            else:
                expected = np.zeros((4, 4))
            err = np.max(np.abs(ac - expected))
            if err > 1e-10:
                print(f"  WARNING: Clifford algebra violation at ({i},{j}): err={err:.2e}")
                return False
    return True


# ============================================================================
# Dirac Walk: Coin and Shift
# ============================================================================

def dirac_coin(mass):
    """Mass coin: C(m) = cos(m)*I4 + i*sin(m)*gamma0."""
    return np.cos(mass) * np.eye(4, dtype=complex) + 1j * np.sin(mass) * gamma0


def dirac_coin_step(psi_4d, mass_field, n):
    """Apply spatially-varying Dirac mass coin.
    psi_4d: shape (4, n, n, n), complex
    mass_field: shape (n, n, n), real
    """
    cm = np.cos(mass_field)  # (n,n,n)
    sm = np.sin(mass_field)  # (n,n,n)
    out = np.zeros_like(psi_4d)
    # C = cos(m)*I + i*sin(m)*gamma0
    # gamma0 = diag(1, 1, -1, -1)
    # So: out[0] = cos(m)*psi[0] + i*sin(m)*psi[0] = (cos(m) + i*sin(m))*psi[0] = exp(im)*psi[0]
    #     out[1] = exp(im)*psi[1]
    #     out[2] = cos(m)*psi[2] - i*sin(m)*psi[2] = exp(-im)*psi[2]
    #     out[3] = exp(-im)*psi[3]
    out[0] = (cm + 1j*sm) * psi_4d[0]
    out[1] = (cm + 1j*sm) * psi_4d[1]
    out[2] = (cm - 1j*sm) * psi_4d[2]
    out[3] = (cm - 1j*sm) * psi_4d[3]
    return out


def dirac_shift_x(psi_4d, n):
    """Conditional shift in x-direction using gamma0*gamma1.
    T_x|psi> : if gamma0*gamma1 eigenvalue = +1, shift +x; if -1, shift -x.

    gamma0*gamma1 = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]] = sigma_x tensor I2
    Eigenvalues: +1 for (psi0+psi3)/sqrt2, (psi1+psi2)/sqrt2
                 -1 for (psi0-psi3)/sqrt2, (psi1-psi2)/sqrt2

    Equivalently: S_x = exp(i*k_x * gamma0*gamma1) in Bloch space.
    In position space: rotate to eigenbasis, shift, rotate back.
    """
    g0g1 = gamma0 @ gamma1
    # Diagonalize g0g1
    evals, evecs = np.linalg.eigh(g0g1)
    # evals should be ±1
    # P_plus projects onto +1 eigenspace, P_minus onto -1
    P_plus = np.zeros((4, 4), dtype=complex)
    P_minus = np.zeros((4, 4), dtype=complex)
    for i in range(4):
        v = evecs[:, i:i+1]
        if evals[i] > 0:
            P_plus += v @ v.conj().T
        else:
            P_minus += v @ v.conj().T

    out = np.zeros_like(psi_4d)
    # Apply P_plus, shift +x (axis 0, roll -1), then P_minus, shift -x (roll +1)
    for c in range(4):
        # Component in +1 eigenspace
        psi_plus = np.zeros((n, n, n), dtype=complex)
        psi_minus = np.zeros((n, n, n), dtype=complex)
        for d in range(4):
            psi_plus += P_plus[c, d] * psi_4d[d]
            psi_minus += P_minus[c, d] * psi_4d[d]
        # Shift
        out[c] += np.roll(psi_plus, -1, axis=0)  # +x
        out[c] += np.roll(psi_minus, +1, axis=0)  # -x
    return out


def dirac_shift_y(psi_4d, n):
    """Conditional shift in y-direction using gamma0*gamma2."""
    g0g2 = gamma0 @ gamma2
    evals, evecs = np.linalg.eigh(g0g2)
    P_plus = np.zeros((4, 4), dtype=complex)
    P_minus = np.zeros((4, 4), dtype=complex)
    for i in range(4):
        v = evecs[:, i:i+1]
        if evals[i] > 0:
            P_plus += v @ v.conj().T
        else:
            P_minus += v @ v.conj().T
    out = np.zeros_like(psi_4d)
    for c in range(4):
        psi_plus = np.zeros((n, n, n), dtype=complex)
        psi_minus = np.zeros((n, n, n), dtype=complex)
        for d in range(4):
            psi_plus += P_plus[c, d] * psi_4d[d]
            psi_minus += P_minus[c, d] * psi_4d[d]
        out[c] += np.roll(psi_plus, -1, axis=1)
        out[c] += np.roll(psi_minus, +1, axis=1)
    return out


def dirac_shift_z(psi_4d, n):
    """Conditional shift in z-direction using gamma0*gamma3."""
    g0g3 = gamma0 @ gamma3
    evals, evecs = np.linalg.eigh(g0g3)
    P_plus = np.zeros((4, 4), dtype=complex)
    P_minus = np.zeros((4, 4), dtype=complex)
    for i in range(4):
        v = evecs[:, i:i+1]
        if evals[i] > 0:
            P_plus += v @ v.conj().T
        else:
            P_minus += v @ v.conj().T
    out = np.zeros_like(psi_4d)
    for c in range(4):
        psi_plus = np.zeros((n, n, n), dtype=complex)
        psi_minus = np.zeros((n, n, n), dtype=complex)
        for d in range(4):
            psi_plus += P_plus[c, d] * psi_4d[d]
            psi_minus += P_minus[c, d] * psi_4d[d]
        out[c] += np.roll(psi_plus, -1, axis=2)
        out[c] += np.roll(psi_minus, +1, axis=2)
    return out


def dirac_step(psi_4d, mass_field, n):
    """One full Dirac walk step: U = S_z * S_y * S_x * C(m)."""
    psi = dirac_coin_step(psi_4d, mass_field, n)
    psi = dirac_shift_x(psi, n)
    psi = dirac_shift_y(psi, n)
    psi = dirac_shift_z(psi, n)
    return psi


# ============================================================================
# Bloch Analysis
# ============================================================================

def bloch_kg_analysis(mass0, n=9):
    """Compute KG R^2 via Bloch decomposition of the 4-component Dirac walk."""
    print(f"\n  Bloch analysis (n={n}, mass={mass0:.4f})...")
    t0 = time.time()

    # Build the 4x4 Bloch matrix U_k for each momentum
    C4 = dirac_coin(mass0)

    # Precompute projectors for each shift direction
    def get_projectors(gamma_product):
        evals, evecs = np.linalg.eigh(gamma_product)
        P_plus = np.zeros((4, 4), dtype=complex)
        P_minus = np.zeros((4, 4), dtype=complex)
        for i in range(4):
            v = evecs[:, i:i+1]
            if evals[i] > 0:
                P_plus += v @ v.conj().T
            else:
                P_minus += v @ v.conj().T
        return P_plus, P_minus

    Px_p, Px_m = get_projectors(gamma0 @ gamma1)
    Py_p, Py_m = get_projectors(gamma0 @ gamma2)
    Pz_p, Pz_m = get_projectors(gamma0 @ gamma3)

    ks_raw = 2 * np.pi * np.arange(n) / n

    all_E2 = []
    all_k2 = []
    axis_data = {'x': ([], []), 'y': ([], []), 'z': ([], [])}

    for mx in range(n):
        kx = ks_raw[mx]
        kx_c = kx if kx <= np.pi else kx - 2*np.pi
        for my in range(n):
            ky = ks_raw[my]
            ky_c = ky if ky <= np.pi else ky - 2*np.pi
            for mz in range(n):
                kz = ks_raw[mz]
                kz_c = kz if kz <= np.pi else kz - 2*np.pi

                # Shift matrices in Bloch space
                # S_x(kx) = exp(+ikx)*P_plus + exp(-ikx)*P_minus
                Sx = np.exp(1j*kx) * Px_p + np.exp(-1j*kx) * Px_m
                Sy = np.exp(1j*ky) * Py_p + np.exp(-1j*ky) * Py_m
                Sz = np.exp(1j*kz) * Pz_p + np.exp(-1j*kz) * Pz_m

                # Full step: U = Sz * Sy * Sx * C
                Uk = Sz @ Sy @ Sx @ C4

                eigs_k = np.linalg.eigvals(Uk)
                phases = np.angle(eigs_k)

                k2 = kx_c**2 + ky_c**2 + kz_c**2

                for ph in phases:
                    all_E2.append(ph**2)
                    all_k2.append(k2)

                # Per-axis
                if my == 0 and mz == 0 and mx > 0:
                    for ph in phases:
                        axis_data['x'][0].append(kx_c**2)
                        axis_data['x'][1].append(ph**2)
                if mx == 0 and mz == 0 and my > 0:
                    for ph in phases:
                        axis_data['y'][0].append(ky_c**2)
                        axis_data['y'][1].append(ph**2)
                if mx == 0 and my == 0 and mz > 0:
                    for ph in phases:
                        axis_data['z'][0].append(kz_c**2)
                        axis_data['z'][1].append(ph**2)

    all_E2 = np.array(all_E2)
    all_k2 = np.array(all_k2)

    # KG fit: E^2 = m^2 + c^2 * k^2 on small-k
    mask = all_k2 < 1.0
    E2_s = all_E2[mask]
    k2_s = all_k2[mask]

    if len(E2_s) > 10:
        slope, intercept, r_value, _, _ = stats.linregress(k2_s, E2_s)
        r2_kg = r_value**2
        m_fit = np.sqrt(abs(intercept))
        c2_fit = slope
    else:
        r2_kg, m_fit, c2_fit = 0.0, 0.0, 0.0

    # Isotropy
    axis_slopes = {}
    for ax, (k2a, e2a) in axis_data.items():
        k2a, e2a = np.array(k2a), np.array(e2a)
        m_ax = k2a < 1.0
        if np.sum(m_ax) > 3:
            sl, _, _, _, _ = stats.linregress(k2a[m_ax], e2a[m_ax])
            axis_slopes[ax] = sl

    dt = time.time() - t0
    print(f"    R^2 = {r2_kg:.6f}, m_fit = {m_fit:.4f}, c^2 = {c2_fit:.4f}")
    for ax, sl in axis_slopes.items():
        print(f"    {ax}-axis slope: {sl:.4f}")
    slopes = [v for v in axis_slopes.values()]
    if len(slopes) >= 2 and min(slopes) > 0:
        print(f"    Isotropy ratio: {max(slopes)/min(slopes):.4f}")
    print(f"    Time: {dt:.1f}s")

    return r2_kg, m_fit, c2_fit, axis_slopes


# ============================================================================
# Band Structure
# ============================================================================

def band_structure(mass0, n=9):
    """Print band structure along principal axes and diagonal."""
    print(f"\n  Band structure along k_x axis (ky=kz=0):")
    C4 = dirac_coin(mass0)

    def get_projectors(gp):
        evals, evecs = np.linalg.eigh(gp)
        Pp = sum(np.outer(evecs[:,i], evecs[:,i].conj()) for i in range(4) if evals[i] > 0)
        Pm = sum(np.outer(evecs[:,i], evecs[:,i].conj()) for i in range(4) if evals[i] < 0)
        return Pp, Pm

    Px_p, Px_m = get_projectors(gamma0 @ gamma1)
    Py_p, Py_m = get_projectors(gamma0 @ gamma2)
    Pz_p, Pz_m = get_projectors(gamma0 @ gamma3)

    ks_raw = 2 * np.pi * np.arange(n) / n

    for mx in range(n):
        kx = ks_raw[mx]
        kx_c = kx if kx <= np.pi else kx - 2*np.pi
        Sx = np.exp(1j*kx)*Px_p + np.exp(-1j*kx)*Px_m
        Sy = Py_p + Py_m  # ky=0 -> exp(0)=1
        Sz = Pz_p + Pz_m
        Uk = Sz @ Sy @ Sx @ C4
        phases = sorted(np.angle(np.linalg.eigvals(Uk)))
        print(f"    kx={kx_c:+.4f}: E = [{', '.join(f'{p:.4f}' for p in phases)}]")

    print(f"\n  Band structure along (1,1,1) diagonal:")
    for mi in range(n):
        k = ks_raw[mi]
        k_c = k if k <= np.pi else k - 2*np.pi
        Sx = np.exp(1j*k)*Px_p + np.exp(-1j*k)*Px_m
        Sy = np.exp(1j*k)*Py_p + np.exp(-1j*k)*Py_m
        Sz = np.exp(1j*k)*Pz_p + np.exp(-1j*k)*Pz_m
        Uk = Sz @ Sy @ Sx @ C4
        phases = sorted(np.angle(np.linalg.eigvals(Uk)))
        print(f"    k={k_c:+.4f}: E = [{', '.join(f'{p:.4f}' for p in phases)}]")


# ============================================================================
# Unitarity Check (full matrix)
# ============================================================================

def unitarity_check(mass0, n=5):
    """Build full (4n^3 x 4n^3) evolution matrix and verify unitarity."""
    print(f"\n  Unitarity check (n={n}, {4*n**3} dim)...")
    dim = 4 * n**3
    mass_field = np.full((n, n, n), mass0)

    U = np.zeros((dim, dim), dtype=complex)
    for col in range(dim):
        psi = np.zeros((4, n, n, n), dtype=complex)
        c_idx = col // (n*n*n)
        spatial = col % (n*n*n)
        ix = spatial // (n*n)
        iy = (spatial // n) % n
        iz = spatial % n
        psi[c_idx, ix, iy, iz] = 1.0
        psi = dirac_step(psi, mass_field, n)
        U[:, col] = psi.reshape(-1)

    UUd = U @ U.conj().T
    err = np.max(np.abs(UUd - np.eye(dim)))
    print(f"    max|UU^dag - I| = {err:.2e}")
    print(f"    {'PASS' if err < 1e-10 else 'FAIL'}")
    return err < 1e-10


# ============================================================================
# Closure Card
# ============================================================================

def min_image_dist(n, mass_pos):
    c = np.arange(n)
    dx = np.abs(c[:, None, None] - mass_pos[0])
    dx = np.minimum(dx, n - dx)
    dy = np.abs(c[None, :, None] - mass_pos[1])
    dy = np.minimum(dy, n - dy)
    dz = np.abs(c[None, None, :] - mass_pos[2])
    dz = np.minimum(dz, n - dz)
    return np.sqrt(dx**2 + dy**2 + dz**2)


def evolve_dirac(n, n_layers, mass0, strength=0.0, mass_positions=None):
    """Evolve Dirac walk with optional gravity."""
    psi = np.zeros((4, n, n, n), dtype=np.complex128)
    c_idx = n // 2
    amp = 1.0 / 2.0  # 4 components
    for k in range(4):
        psi[k, c_idx, c_idx, c_idx] = amp

    mass_field = np.full((n, n, n), mass0)
    if mass_positions and strength > 0:
        total_f = np.zeros((n, n, n))
        for mp in mass_positions:
            r = min_image_dist(n, mp)
            total_f += strength / (r + 0.1)
        mass_field = mass0 * (1.0 - total_f)

    for _ in range(n_layers):
        psi = dirac_step(psi, mass_field, n)
    return psi


def prob_density(psi):
    return np.sum(np.abs(psi)**2, axis=0)


def run_closure_card(mass0, n=15, n_layers=12):
    """10-property closure card for the Dirac walk."""
    print(f"\n{'='*70}")
    print(f"CLOSURE CARD: 4-Component Dirac Walk (mass={mass0:.4f})")
    print(f"  n={n}, N={n_layers}")
    print(f"{'='*70}")

    c = n // 2
    STRENGTH = 5e-4
    score = 0
    barrier_layer = 6
    slit_positions = [c - 2, c, c + 2]

    def evolve_with_barrier(slits, noise=0.0):
        psi = np.zeros((4, n, n, n), dtype=np.complex128)
        amp = 0.5
        for k in range(4):
            psi[k, c, c, c] = amp
        mf = np.full((n, n, n), mass0)
        rng = np.random.RandomState(42) if noise > 0 else None
        for step in range(n_layers):
            if noise > 0:
                phase = rng.uniform(-noise, noise, (n,n,n))
                pf = np.exp(1j * phase)
                for k in range(4):
                    psi[k] = psi[k] * pf
            psi = dirac_step(psi, mf, n)
            if step == barrier_layer - 1:
                mask = np.zeros((n,n,n), dtype=bool)
                for sy in slits:
                    mask[sy,:,:] = True
                for k in range(4):
                    psi[k] = psi[k] * mask
        return prob_density(psi)

    # 1. Born
    print("\n  [1] Born |I3|/P...")
    rho_full = evolve_with_barrier(slit_positions)
    rho_singles = [evolve_with_barrier([s]) for s in slit_positions]
    P_total = np.sum(rho_full)
    born = np.sum(np.abs(rho_full - sum(rho_singles))) / P_total if P_total > 0 else 0
    p1 = born > 0.01
    print(f"      |I3|/P = {born:.6f}  {'PASS' if p1 else 'FAIL'}")
    if p1: score += 1

    # 2. d_TV
    print("  [2] d_TV...")
    rho_up = evolve_with_barrier([c-2])
    rho_dn = evolve_with_barrier([c+2])
    p_up = rho_up / np.sum(rho_up) if np.sum(rho_up) > 0 else rho_up
    p_dn = rho_dn / np.sum(rho_dn) if np.sum(rho_dn) > 0 else rho_dn
    dtv = 0.5 * np.sum(np.abs(p_up - p_dn))
    p2 = dtv > 0.01
    print(f"      d_TV = {dtv:.6f}  {'PASS' if p2 else 'FAIL'}")
    if p2: score += 1

    # 3. f=0 control
    print("  [3] f=0 control...")
    psi0 = evolve_dirac(n, n_layers, mass0, 0.0)
    rho0 = prob_density(psi0)
    plus_z = np.sum(rho0[c, c, c+1:c+4])
    minus_z = np.sum(rho0[c, c, c-3:c])
    bias = abs(plus_z - minus_z) / (plus_z + minus_z) if (plus_z + minus_z) > 0 else 0
    p3 = bias < 0.01
    print(f"      bias = {bias:.8f}  {'PASS' if p3 else 'FAIL'}")
    if p3: score += 1

    # 4. F proportional to M
    print("  [4] F~M...")
    rho0 = prob_density(evolve_dirac(n, n_layers, mass0, 0.0))
    strengths = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3]
    forces = []
    for s in strengths:
        rho1 = prob_density(evolve_dirac(n, n_layers, mass0, s, [(c,c,c+3)]))
        delta = rho1 - rho0
        force = sum(delta[c, c, c+dz] for dz in range(1, 4))
        forces.append(force)
    forces_arr = np.array(forces)
    strengths_arr = np.array(strengths)
    coeffs = np.polyfit(strengths_arr, forces_arr, 1)
    predicted = np.polyval(coeffs, strengths_arr)
    ss_res = np.sum((forces_arr - predicted)**2)
    ss_tot = np.sum((forces_arr - np.mean(forces_arr))**2)
    r2_fm = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    p4 = r2_fm > 0.9
    print(f"      R^2 = {r2_fm:.6f}, forces = [{', '.join(f'{f:.4e}' for f in forces)}]")
    print(f"      {'PASS' if p4 else 'FAIL'}")
    if p4: score += 1

    # 5. Gravity sign
    print("  [5] Gravity sign...")
    rho0 = prob_density(evolve_dirac(n, n_layers, mass0, 0.0))
    rho1 = prob_density(evolve_dirac(n, n_layers, mass0, STRENGTH, [(c,c,c+3)]))
    delta = rho1 - rho0
    toward = sum(delta[c, c, c+dz] for dz in range(1, 4))
    away = sum(delta[c, c, c-dz] for dz in range(1, 4))
    is_toward = toward > away
    p5 = is_toward
    print(f"      toward={toward:.4e}, away={away:.4e} -> {'TOWARD' if is_toward else 'AWAY'}  {'PASS' if p5 else 'FAIL'}")
    if p5: score += 1

    # 6. Decoherence
    print("  [6] Decoherence...")
    bn = 0.0
    rho_noisy = evolve_with_barrier(slit_positions, noise=0.5)
    P_noisy = np.sum(rho_noisy)
    rho_singles_n = [evolve_with_barrier([s]) for s in slit_positions]  # reuse clean singles
    bn = np.sum(np.abs(rho_noisy - sum(rho_singles_n))) / P_noisy if P_noisy > 0 else 0
    p6 = bn < born
    print(f"      clean={born:.6f}, noisy={bn:.6f}  {'PASS' if p6 else 'FAIL'}")
    if p6: score += 1

    # 7. MI
    print("  [7] MI...")
    psi_g = evolve_dirac(n, n_layers, mass0, STRENGTH, [(c,c,c)])
    rho_g = prob_density(psi_g)
    rho_n = rho_g / np.sum(rho_g)
    p_x = np.sum(rho_n, axis=(1,2))
    p_y = np.sum(rho_n, axis=(0,2))
    p_xy = np.sum(rho_n, axis=2)
    mi = 0.0
    for ix in range(n):
        for iy in range(n):
            if p_xy[ix,iy] > 1e-30 and p_x[ix] > 1e-30 and p_y[iy] > 1e-30:
                mi += p_xy[ix,iy] * np.log(p_xy[ix,iy] / (p_x[ix] * p_y[iy]))
    p7 = mi > 0.0
    print(f"      MI = {mi:.6e}  {'PASS' if p7 else 'FAIL'}")
    if p7: score += 1

    # 8. Purity stable
    print("  [8] Purity stable...")
    purities = {}
    for L in [8, 10, 12]:
        psi = evolve_dirac(n, L, mass0, STRENGTH, [(c,c,c)])
        rho = prob_density(psi)
        purities[L] = np.sum(rho**2) / np.sum(rho)**2
    vals = list(purities.values())
    cv = np.std(vals) / np.mean(vals) if np.mean(vals) > 0 else 0
    p8 = cv < 0.5
    for ll, pu in purities.items():
        print(f"      L={ll}: purity={pu:.6e}")
    print(f"      CV={cv:.4f}  {'PASS' if p8 else 'FAIL'}")
    if p8: score += 1

    # 9. Gravity grows
    print("  [9] Gravity grows...")
    gforces = {}
    for L in [8, 10, 12]:
        rho0 = prob_density(evolve_dirac(n, L, mass0, 0.0))
        rho1 = prob_density(evolve_dirac(n, L, mass0, STRENGTH, [(c,c,c+3)]))
        delta = rho1 - rho0
        gforces[L] = sum(delta[c, c, c+dz] for dz in range(1, 4))
    vals_g = [gforces[L] for L in [8, 10, 12]]
    mono = all(vals_g[i] <= vals_g[i+1] for i in range(len(vals_g)-1))
    p9 = mono
    for ll, gf in gforces.items():
        print(f"      L={ll}: force={gf:.4e}")
    print(f"      Monotonic: {mono}  {'PASS' if p9 else 'FAIL'}")
    if p9: score += 1

    # 10. Distance law
    print("  [10] Distance law...")
    max_off = min(5, n // 4)
    offsets = list(range(2, max_off + 1))
    forces_dl = []
    rho0 = prob_density(evolve_dirac(n, n_layers, mass0, 0.0))
    for dz in offsets:
        rho1 = prob_density(evolve_dirac(n, n_layers, mass0, STRENGTH, [(c,c,c+dz)]))
        delta = rho1 - rho0
        force = sum(delta[c, c, c+dd] for dd in range(1, dz+1))
        forces_dl.append(force)
    forces_dl_arr = np.array(forces_dl)
    offsets_arr = np.array(offsets, dtype=float)
    abs_f = np.abs(forces_dl_arr)
    valid = abs_f > 1e-30
    if np.sum(valid) >= 3:
        lr = np.log(offsets_arr[valid])
        lf = np.log(abs_f[valid])
        c_dl = np.polyfit(lr, lf, 1)
        pred_dl = np.polyval(c_dl, lr)
        ss_r = np.sum((lf - pred_dl)**2)
        ss_t = np.sum((lf - np.mean(lf))**2)
        r2_dl = 1 - ss_r / ss_t if ss_t > 0 else 0
        exp_dl = c_dl[0]
    else:
        r2_dl, exp_dl = 0.0, 0.0
    p10 = r2_dl > 0.7
    for i, dz in enumerate(offsets):
        d = "TOWARD" if forces_dl[i] > 0 else "AWAY"
        print(f"      offset={dz}: force={forces_dl[i]:.4e} {d}")
    print(f"      exponent={exp_dl:.3f}, R^2={r2_dl:.4f}  {'PASS' if p10 else 'FAIL'}")
    if p10: score += 1

    print(f"\n  CLOSURE CARD SCORE: {score}/10")
    labels = ["Born", "d_TV", "f=0", "F~M", "TOWARD", "Decoh", "MI", "Purity", "GravGrow", "DistLaw"]
    results = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
    for lab, res in zip(labels, results):
        print(f"    {lab:10s} {'PASS' if res else 'FAIL'}")
    return score, results


# ============================================================================
# AB Test
# ============================================================================

def ab_test(mass0, n=9, n_layers=12):
    """Aharonov-Bohm: add phase to x-shifts, measure modulation."""
    print(f"\n{'='*70}")
    print("AHARONOV-BOHM TEST")
    print(f"{'='*70}")

    c_idx = n // 2

    Px_p, Px_m = np.linalg.eigh(gamma0 @ gamma1)
    evals, evecs = np.linalg.eigh(gamma0 @ gamma1)
    Pp = sum(np.outer(evecs[:,i], evecs[:,i].conj()) for i in range(4) if evals[i] > 0)
    Pm = sum(np.outer(evecs[:,i], evecs[:,i].conj()) for i in range(4) if evals[i] < 0)

    def evolve_ab(A_flux):
        psi = np.zeros((4, n, n, n), dtype=complex)
        for k in range(4):
            psi[k, c_idx, c_idx, c_idx] = 0.5
        mf = np.full((n,n,n), mass0)

        for _ in range(n_layers):
            psi = dirac_coin_step(psi, mf, n)
            # x-shift with AB phase
            out = np.zeros_like(psi)
            for c in range(4):
                pp = sum(Pp[c,d] * psi[d] for d in range(4))
                pm = sum(Pm[c,d] * psi[d] for d in range(4))
                out[c] += np.roll(pp, -1, axis=0) * np.exp(1j*A_flux)
                out[c] += np.roll(pm, +1, axis=0) * np.exp(-1j*A_flux)
            psi = out
            psi = dirac_shift_y(psi, n)
            psi = dirac_shift_z(psi, n)

        rho = prob_density(psi)
        det_x = c_idx + 3
        return np.sum(rho[det_x, :, :]) if det_x < n else 0.0

    A_values = np.linspace(0, 2*np.pi, 13)
    P_values = []
    for A in A_values:
        P = evolve_ab(A)
        P_values.append(P)
        print(f"  A={A:.2f}: P={P:.6f}")

    P_arr = np.array(P_values)
    V_ab = (np.max(P_arr) - np.min(P_arr)) / (np.max(P_arr) + np.min(P_arr)) if np.max(P_arr) > 0 else 0
    print(f"\n  AB visibility V = {V_ab:.4f}")
    print(f"  {'PASS' if V_ab > 0.5 else 'FAIL'} (need V > 0.5)")
    return V_ab


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()

    print("=" * 70)
    print("4-COMPONENT DIRAC WALK IN 3+1D")
    print("=" * 70)
    print("HYPOTHESIS: 4-component Dirac walk produces isotropic 3D KG (R^2>0.99)")
    print("BASELINE: 6-component chiral walk R^2=0.156 (structural no-go)")
    print()

    # Verify Clifford algebra
    print("--- Clifford algebra check ---")
    cliff_ok = verify_clifford()
    print(f"  {gammas[0]=}\n  Clifford: {'PASS' if cliff_ok else 'FAIL'}")

    # Sweep mass parameter
    print("\n--- Mass parameter sweep (Bloch KG) ---")
    best_r2, best_mass = 0.0, 0.3
    for mass in [0.1, 0.2, 0.3, 0.4, 0.5]:
        r2, m_fit, c2, _ = bloch_kg_analysis(mass, n=9)
        if r2 > best_r2:
            best_r2, best_mass = r2, mass

    print(f"\n  Best KG R^2 = {best_r2:.6f} at mass = {best_mass:.2f}")

    # Unitarity check
    uni_ok = unitarity_check(best_mass, n=5)

    # Band structure
    band_structure(best_mass, n=9)

    # Closure card
    closure_score, closure_results = run_closure_card(best_mass, n=13, n_layers=10)

    # AB test
    ab_v = ab_test(best_mass, n=9, n_layers=10)

    # ========================================================================
    # VERDICT
    # ========================================================================
    elapsed = time.time() - t_start

    print(f"\n{'='*70}")
    print("FINAL VERDICT")
    print(f"{'='*70}")
    print(f"  Architecture: 4-component Dirac walk (gamma-matrix coin + conditional shift)")
    print(f"  KG R^2:        {best_r2:.6f} ({'PASS' if best_r2 > 0.99 else 'FAIL'}, need >0.99)")
    print(f"  Unitarity:     {'PASS' if uni_ok else 'FAIL'}")
    print(f"  Closure card:  {closure_score}/10")
    print(f"  AB visibility: {ab_v:.4f} ({'PASS' if ab_v > 0.5 else 'FAIL'})")

    if best_r2 > 0.99 and closure_score >= 8:
        print("\n  RESULT: 4-component Dirac walk achieves isotropic 3D KG AND gravity closure.")
        print("  This architecture supersedes the 6-component chiral walk for 3+1D.")
    elif best_r2 > 0.99:
        print("\n  RESULT: 3D KG achieved but closure card incomplete. Gravity coupling needs work.")
    elif best_r2 > 0.5:
        print(f"\n  RESULT: Partial improvement (R^2={best_r2:.4f}) but not fully isotropic.")
    else:
        print(f"\n  RESULT: 4-component Dirac walk also struggles with isotropic 3D KG (R^2={best_r2:.4f}).")
        print("  The split-step factorization may introduce order-dependent anisotropy.")
        print("  Next: try single-step U = exp(-i*H*dt) with full Dirac Hamiltonian.")

    print(f"\n  Total time: {elapsed:.1f}s")
