#!/usr/bin/env python3
"""
Coupled Dirac-Like Coin for 3+1D Chiral Quantum Walk
=====================================================
HYPOTHESIS: A coupled 6x6 unitary coin that mixes all chirality pairs
  can produce isotropic 3D Klein-Gordon dispersion (R^2 > 0.99)
  while preserving the existing 10/10 closure card.

OBSERVABLE: E^2 vs k^2 fit R^2 from Bloch analysis at n=9.

FALSIFICATION: If NO 6x6 on-site unitary achieves R^2 > 0.90,
  the 6-component architecture is structurally incapable.

Five candidate coins tested:
  1. Block-Circulant (S3-symmetric, two-parameter family)
  2. Cayley-Coupled (matrix exponential with cross-coupling)
  3. DFT-6 (democratic Fourier mixing)
  4. Grover-6 (Householder reflection)
  5. Dirac-Embedded (4-in-6 via isometry)

Success criteria:
  KG R^2 > 0.99 (current factorized: 0.156)
  AB visibility > 0.5 (current factorized: 0.0)
  Closure card: maintain 10/10
"""

import numpy as np
from scipy import stats
from scipy.linalg import expm
import time

# ============================================================================
# SECTION 1: Coin Factories
# ============================================================================

def C2(t):
    """Standard 2x2 symmetric Lorentzian coin."""
    return np.array([[np.cos(t), 1j*np.sin(t)],
                     [1j*np.sin(t), np.cos(t)]])


def coin_factorized(theta):
    """BASELINE: block-diagonal 3 x (2x2) coin. R^2 = 0.156."""
    C6 = np.zeros((6, 6), dtype=complex)
    c = C2(theta)
    for i in range(3):
        C6[2*i:2*i+2, 2*i:2*i+2] = c
    return C6


def coin_block_circulant(theta_plus, theta_minus):
    """Candidate 1: S3-symmetric block-circulant.
    Diagonal blocks = A, off-diagonal = B.
    A+2B = C(theta_plus), A-B = C(theta_minus) => both 2x2 unitary => 6x6 unitary.
    Reduces to factorized when theta_plus == theta_minus.
    """
    cp = C2(theta_plus)
    cm = C2(theta_minus)
    A = (1.0/3.0)*cp + (2.0/3.0)*cm
    B = (1.0/3.0)*cp - (1.0/3.0)*cm
    C6 = np.zeros((6, 6), dtype=complex)
    for i in range(3):
        for j in range(3):
            block = A if i == j else B
            C6[2*i:2*i+2, 2*j:2*j+2] = block
    return C6


def coin_cayley(theta, epsilon):
    """Candidate 2: Matrix exponential with cross-coupling.
    H = H_factorized(theta) + epsilon * H_cross
    C = expm(i * H)
    """
    H = np.zeros((6, 6), dtype=complex)
    # Factorized part: each pair gets theta * [[0,i],[i,0]] (Hermitian generator)
    for pair_start in [0, 2, 4]:
        H[pair_start, pair_start+1] = 1j * theta
        H[pair_start+1, pair_start] = -1j * theta
    # Cross-coupling: + chiralities (0<->2, 0<->4, 2<->4)
    for (a, b) in [(0, 2), (0, 4), (2, 4)]:
        H[a, b] += 1j * epsilon
        H[b, a] += -1j * epsilon
    # - chiralities (1<->3, 1<->5, 3<->5)
    for (a, b) in [(1, 3), (1, 5), (3, 5)]:
        H[a, b] += 1j * epsilon
        H[b, a] += -1j * epsilon
    return expm(1j * H)


def coin_dft6(theta):
    """Candidate 3: DFT-6 with diagonal mass rotation."""
    omega = np.exp(2j * np.pi / 6)
    F6 = np.array([[omega**(j*k) for k in range(6)] for j in range(6)]) / np.sqrt(6)
    D = np.diag([np.exp(1j*theta), np.exp(-1j*theta),
                 np.exp(1j*theta), np.exp(-1j*theta),
                 np.exp(1j*theta), np.exp(-1j*theta)])
    return F6 @ D


def coin_grover6(theta):
    """Candidate 4: Grover-like Householder reflection.
    C = -I + 2|w><w| where |w> depends on theta.
    """
    w = np.array([np.cos(theta), 1j*np.sin(theta),
                  np.cos(theta), 1j*np.sin(theta),
                  np.cos(theta), 1j*np.sin(theta)]) / np.sqrt(3)
    return -np.eye(6) + 2 * np.outer(w, w.conj())


def coin_dirac_embed(theta):
    """Candidate 5: Embed 4x4 Dirac coin in 6D.
    Standard Dirac coin: C4 = cos(theta)*I4 + i*sin(theta)*gamma0
    gamma0 = diag(I2, -I2) in Dirac representation.
    Embed via 6x4 isometry V.
    """
    I4 = np.eye(4)
    gamma0 = np.diag([1, 1, -1, -1]).astype(complex)
    C4 = np.cos(theta) * I4 + 1j * np.sin(theta) * gamma0

    # Build 6x4 isometry: map Dirac spinor to chiral-walk basis
    # Use Pauli sigma eigenstates for spatial direction assignment
    # This is heuristic; orthogonalize via QR
    V = np.zeros((6, 4), dtype=complex)
    # +y ~ left-handed, sigma_y = +1
    V[0, :] = [1, 1j, 0, 0]
    # -y ~ left-handed, sigma_y = -1
    V[1, :] = [1, -1j, 0, 0]
    # +z ~ right-handed, sigma_z = +1
    V[2, :] = [0, 0, 1, 0]
    # -z ~ right-handed, sigma_z = -1
    V[3, :] = [0, 0, 0, 1]
    # +w ~ mixed
    V[4, :] = [1, 0, 1, 0]
    # -w ~ mixed
    V[5, :] = [0, 1, 0, 1]
    # Normalize rows
    for i in range(6):
        V[i] /= np.linalg.norm(V[i])
    # QR to get orthonormal embedding
    Q, R = np.linalg.qr(V.T)  # Q is 4x4, but we need 6x4
    # Actually: V is 6x4, we want V s.t. V^H V = I4
    # Use SVD: V = U S Vt, then take first 4 columns of U
    U, S, Vt = np.linalg.svd(V, full_matrices=True)
    V_orth = U[:, :4]  # 6x4 isometry

    # Project: C6 = V C4 V^H + phase*(I6 - V V^H) for the null space
    P = V_orth @ V_orth.conj().T  # 6x6 projector onto 4D subspace
    C6 = V_orth @ C4 @ V_orth.conj().T + np.exp(1j * theta) * (np.eye(6) - P)
    return C6


def check_unitarity(C6, name=""):
    """Verify C6 is unitary."""
    err = np.max(np.abs(C6 @ C6.conj().T - np.eye(6)))
    if err > 1e-8:
        print(f"  WARNING: {name} unitarity error = {err:.2e}")
    return err < 1e-8


# ============================================================================
# SECTION 2: Bloch Analysis Engine
# ============================================================================

def bloch_kg_analysis(C6, n=9, verbose=False):
    """Compute Klein-Gordon R^2 for a given 6x6 coin via Bloch decomposition.

    For each momentum (ky, kz, kw):
      U_k = S_k . C6
      S_k = diag[e^{iky}, e^{-iky}, e^{ikz}, e^{-ikz}, e^{ikw}, e^{-ikw}]
      Eigendecompose -> 6 phases -> E^2 vs k^2

    Returns: r2_kg, m_fit, c2_fit, isotropy_info
    """
    ks_raw = 2 * np.pi * np.arange(n) / n

    all_E2 = []
    all_k2 = []
    # For isotropy: track per-axis slopes
    axis_data = {'y': ([], []), 'z': ([], []), 'w': ([], [])}

    for my in range(n):
        ky = ks_raw[my]
        ky_c = ky if ky <= np.pi else ky - 2*np.pi
        for mz in range(n):
            kz = ks_raw[mz]
            kz_c = kz if kz <= np.pi else kz - 2*np.pi
            for mw in range(n):
                kw = ks_raw[mw]
                kw_c = kw if kw <= np.pi else kw - 2*np.pi

                S = np.diag([
                    np.exp(1j*ky), np.exp(-1j*ky),
                    np.exp(1j*kz), np.exp(-1j*kz),
                    np.exp(1j*kw), np.exp(-1j*kw)
                ])
                Uk = S @ C6
                eigs_k = np.linalg.eigvals(Uk)
                phases = np.angle(eigs_k)

                k2 = ky_c**2 + kz_c**2 + kw_c**2
                for ph in phases:
                    all_E2.append(ph**2)
                    all_k2.append(k2)

                # Per-axis data (on-axis momenta only)
                if mz == 0 and mw == 0 and my > 0:
                    for ph in phases:
                        axis_data['y'][0].append(ky_c**2)
                        axis_data['y'][1].append(ph**2)
                if my == 0 and mw == 0 and mz > 0:
                    for ph in phases:
                        axis_data['z'][0].append(kz_c**2)
                        axis_data['z'][1].append(ph**2)
                if my == 0 and mz == 0 and mw > 0:
                    for ph in phases:
                        axis_data['w'][0].append(kw_c**2)
                        axis_data['w'][1].append(ph**2)

    all_E2 = np.array(all_E2)
    all_k2 = np.array(all_k2)

    # KG fit on small-k points
    mask = all_k2 < 1.0
    E2_small = all_E2[mask]
    k2_small = all_k2[mask]

    if len(E2_small) > 10:
        slope, intercept, r_value, _, _ = stats.linregress(k2_small, E2_small)
        r2_kg = r_value**2
        m_fit = np.sqrt(abs(intercept))
        c2_fit = slope
    else:
        r2_kg, m_fit, c2_fit = 0.0, 0.0, 0.0

    # Isotropy: fit slope per axis
    axis_slopes = {}
    for ax_name, (k2_ax, e2_ax) in axis_data.items():
        k2_ax = np.array(k2_ax)
        e2_ax = np.array(e2_ax)
        m_ax = k2_ax < 1.0
        if np.sum(m_ax) > 3:
            sl, _, _, _, _ = stats.linregress(k2_ax[m_ax], e2_ax[m_ax])
            axis_slopes[ax_name] = sl
        else:
            axis_slopes[ax_name] = None

    if verbose and r2_kg > 0:
        print(f"    KG R^2={r2_kg:.6f}, m={m_fit:.4f}, c^2={c2_fit:.4f}")
        for ax, sl in axis_slopes.items():
            if sl is not None:
                print(f"    {ax}-axis slope: {sl:.4f}")

    return r2_kg, m_fit, c2_fit, axis_slopes


# ============================================================================
# SECTION 3: Parameter Sweep
# ============================================================================

def sweep_block_circulant(n=9):
    """Sweep block-circulant coin parameters."""
    print("\n--- Candidate 1: Block-Circulant ---")
    print("  Phase 1: Fix theta_minus=0.3, sweep theta_plus")

    best_r2, best_tp, best_tm = 0.0, 0.3, 0.3
    theta_minus = 0.3
    results_1d = []

    for tp in np.linspace(0.1, 1.5, 20):
        C6 = coin_block_circulant(tp, theta_minus)
        if not check_unitarity(C6):
            continue
        r2, m, c2, _ = bloch_kg_analysis(C6, n)
        results_1d.append((tp, r2, m, c2))
        if r2 > best_r2:
            best_r2, best_tp, best_tm = r2, tp, theta_minus

    # Print top 5
    results_1d.sort(key=lambda x: -x[1])
    print(f"  Top 5 (theta_minus={theta_minus:.2f}):")
    for tp, r2, m, c2 in results_1d[:5]:
        print(f"    theta_plus={tp:.4f}: R^2={r2:.6f}, m={m:.4f}, c^2={c2:.4f}")

    # Phase 2: 2D grid around the best region
    print(f"\n  Phase 2: 2D grid near best theta_plus={best_tp:.3f}")
    tp_range = np.linspace(max(0.05, best_tp - 0.3), min(np.pi, best_tp + 0.3), 12)
    tm_range = np.linspace(0.05, 1.2, 12)

    results_2d = []
    for tp in tp_range:
        for tm in tm_range:
            C6 = coin_block_circulant(tp, tm)
            if not check_unitarity(C6):
                continue
            r2, m, c2, _ = bloch_kg_analysis(C6, n)
            results_2d.append((tp, tm, r2, m, c2))
            if r2 > best_r2:
                best_r2, best_tp, best_tm = r2, tp, tm

    results_2d.sort(key=lambda x: -x[2])
    print(f"  Top 5 (2D grid):")
    for tp, tm, r2, m, c2 in results_2d[:5]:
        print(f"    theta_plus={tp:.4f}, theta_minus={tm:.4f}: R^2={r2:.6f}, m={m:.4f}")

    print(f"  BEST: R^2={best_r2:.6f} at theta_plus={best_tp:.4f}, theta_minus={best_tm:.4f}")
    return best_r2, best_tp, best_tm


def sweep_cayley(n=9):
    """Sweep Cayley-coupled coin parameter."""
    print("\n--- Candidate 2: Cayley-Coupled ---")
    theta = 0.3
    best_r2, best_eps = 0.0, 0.0
    results = []

    for eps in np.linspace(0.0, 1.5, 25):
        C6 = coin_cayley(theta, eps)
        if not check_unitarity(C6):
            continue
        r2, m, c2, _ = bloch_kg_analysis(C6, n)
        results.append((eps, r2, m, c2))
        if r2 > best_r2:
            best_r2, best_eps = r2, eps

    results.sort(key=lambda x: -x[1])
    print(f"  Top 5 (theta={theta}):")
    for eps, r2, m, c2 in results[:5]:
        print(f"    epsilon={eps:.4f}: R^2={r2:.6f}, m={m:.4f}, c^2={c2:.4f}")

    print(f"  BEST: R^2={best_r2:.6f} at epsilon={best_eps:.4f}")
    return best_r2, best_eps


def sweep_dft6(n=9):
    """Sweep DFT-6 coin."""
    print("\n--- Candidate 3: DFT-6 ---")
    best_r2, best_th = 0.0, 0.0
    results = []

    for th in np.linspace(0.05, 1.5, 20):
        C6 = coin_dft6(th)
        if not check_unitarity(C6):
            continue
        r2, m, c2, _ = bloch_kg_analysis(C6, n)
        results.append((th, r2, m, c2))
        if r2 > best_r2:
            best_r2, best_th = r2, th

    results.sort(key=lambda x: -x[1])
    print(f"  Top 5:")
    for th, r2, m, c2 in results[:5]:
        print(f"    theta={th:.4f}: R^2={r2:.6f}, m={m:.4f}, c^2={c2:.4f}")

    print(f"  BEST: R^2={best_r2:.6f} at theta={best_th:.4f}")
    return best_r2, best_th


def sweep_grover6(n=9):
    """Sweep Grover-6 coin."""
    print("\n--- Candidate 4: Grover-6 ---")
    best_r2, best_th = 0.0, 0.0
    results = []

    for th in np.linspace(0.05, 1.5, 20):
        C6 = coin_grover6(th)
        if not check_unitarity(C6):
            continue
        r2, m, c2, _ = bloch_kg_analysis(C6, n)
        results.append((th, r2, m, c2))
        if r2 > best_r2:
            best_r2, best_th = r2, th

    results.sort(key=lambda x: -x[1])
    print(f"  Top 5:")
    for th, r2, m, c2 in results[:5]:
        print(f"    theta={th:.4f}: R^2={r2:.6f}, m={m:.4f}, c^2={c2:.4f}")

    print(f"  BEST: R^2={best_r2:.6f} at theta={best_th:.4f}")
    return best_r2, best_th


def sweep_dirac_embed(n=9):
    """Sweep Dirac-embedded coin."""
    print("\n--- Candidate 5: Dirac-Embedded ---")
    best_r2, best_th = 0.0, 0.0
    results = []

    for th in np.linspace(0.05, 1.5, 20):
        C6 = coin_dirac_embed(th)
        if not check_unitarity(C6):
            continue
        r2, m, c2, _ = bloch_kg_analysis(C6, n)
        results.append((th, r2, m, c2))
        if r2 > best_r2:
            best_r2, best_th = r2, th

    results.sort(key=lambda x: -x[1])
    print(f"  Top 5:")
    for th, r2, m, c2 in results[:5]:
        print(f"    theta={th:.4f}: R^2={r2:.6f}, m={m:.4f}, c^2={c2:.4f}")

    print(f"  BEST: R^2={best_r2:.6f} at theta={best_th:.4f}")
    return best_r2, best_th


# ============================================================================
# SECTION 4: Deep Analysis of Best Coin
# ============================================================================

def deep_analysis(C6, name, n=9):
    """Full band structure and isotropy analysis."""
    print(f"\n{'='*70}")
    print(f"DEEP ANALYSIS: {name}")
    print(f"{'='*70}")

    # Unitarity
    err = np.max(np.abs(C6 @ C6.conj().T - np.eye(6)))
    print(f"  Unitarity error: {err:.2e}")

    # Full KG fit
    r2, m, c2, axis_slopes = bloch_kg_analysis(C6, n, verbose=True)
    print(f"\n  Klein-Gordon: R^2={r2:.6f}, mass={m:.4f}, c^2={c2:.4f}")

    # Isotropy ratio
    slopes = [v for v in axis_slopes.values() if v is not None]
    if len(slopes) >= 2:
        iso_ratio = max(slopes) / min(slopes) if min(slopes) > 0 else float('inf')
        print(f"  Isotropy ratio (max/min slope): {iso_ratio:.4f}")
    else:
        iso_ratio = float('inf')

    # Band structure along principal axes
    print(f"\n  Band structure along k_y axis (kz=kw=0):")
    ks_raw = 2 * np.pi * np.arange(n) / n
    for my in range(n):
        ky = ks_raw[my]
        ky_c = ky if ky <= np.pi else ky - 2*np.pi
        S = np.diag([np.exp(1j*ky), np.exp(-1j*ky), 1, 1, 1, 1])
        Uk = S @ C6
        phases = sorted(np.angle(np.linalg.eigvals(Uk)))
        phase_str = ', '.join(f'{p:.4f}' for p in phases)
        print(f"    ky={ky_c:+.4f}: E = [{phase_str}]")

    # Diagonal (1,1,1) direction
    print(f"\n  Band structure along (1,1,1) diagonal:")
    for mi in range(n):
        k = ks_raw[mi]
        k_c = k if k <= np.pi else k - 2*np.pi
        S = np.diag([np.exp(1j*k), np.exp(-1j*k),
                     np.exp(1j*k), np.exp(-1j*k),
                     np.exp(1j*k), np.exp(-1j*k)])
        Uk = S @ C6
        phases = sorted(np.angle(np.linalg.eigvals(Uk)))
        phase_str = ', '.join(f'{p:.4f}' for p in phases)
        print(f"    k={k_c:+.4f}: E = [{phase_str}]")

    return r2, m, c2, iso_ratio


# ============================================================================
# SECTION 5: Closure Card with Coupled Coin
# ============================================================================

def shift_3d(psi_6d, n):
    """Shift each chirality 1 step in its direction (periodic)."""
    result = np.zeros_like(psi_6d)
    result[0] = np.roll(psi_6d[0], -1, axis=0)
    result[1] = np.roll(psi_6d[1], +1, axis=0)
    result[2] = np.roll(psi_6d[2], -1, axis=1)
    result[3] = np.roll(psi_6d[3], +1, axis=1)
    result[4] = np.roll(psi_6d[4], -1, axis=2)
    result[5] = np.roll(psi_6d[5], +1, axis=2)
    return result


def apply_coupled_coin_and_shift(psi_6d, n, coin_func, field_args):
    """Apply spatially-varying coupled coin then shift.
    coin_func: callable(field_args) -> per-site coin application
    field_args: dict with precomputed field arrays
    """
    # Apply coin: 6x6 matrix-vector at each site, but coin varies spatially
    # For block-circulant: A, B blocks vary with theta_plus/theta_minus fields
    new_psi = np.zeros_like(psi_6d)
    a_diag = field_args['a_diag']  # (n,n,n) arrays
    a_off = field_args['a_off']
    b_diag = field_args['b_diag']
    b_off = field_args['b_off']

    for i in range(3):
        for j in range(3):
            if i == j:
                d, o = a_diag, a_off
            else:
                d, o = b_diag, b_off
            new_psi[2*i]   += d * psi_6d[2*j]   + o * psi_6d[2*j+1]
            new_psi[2*i+1] += o * psi_6d[2*j]   + d * psi_6d[2*j+1]

    return shift_3d(new_psi, n)


def precompute_block_circulant_fields(theta_plus_field, theta_minus_field):
    """Precompute A, B block components for spatially-varying block-circulant coin."""
    ct_p = np.cos(theta_plus_field)
    st_p = 1j * np.sin(theta_plus_field)
    ct_m = np.cos(theta_minus_field)
    st_m = 1j * np.sin(theta_minus_field)
    return {
        'a_diag': (1.0/3.0)*ct_p + (2.0/3.0)*ct_m,
        'a_off':  (1.0/3.0)*st_p + (2.0/3.0)*st_m,
        'b_diag': (1.0/3.0)*ct_p - (1.0/3.0)*ct_m,
        'b_off':  (1.0/3.0)*st_p - (1.0/3.0)*st_m,
    }


def min_image_dist(n, mass_pos):
    """Minimum-image distance on periodic grid."""
    c = np.arange(n)
    dy = np.abs(c[:, None, None] - mass_pos[0])
    dy = np.minimum(dy, n - dy)
    dz = np.abs(c[None, :, None] - mass_pos[1])
    dz = np.minimum(dz, n - dz)
    dw = np.abs(c[None, None, :] - mass_pos[2])
    dw = np.minimum(dw, n - dw)
    return np.sqrt(dy**2 + dz**2 + dw**2)


def evolve_coupled(n, n_layers, strength, theta_plus_0, theta_minus_0,
                   mass_positions=None):
    """Evolve with coupled block-circulant coin."""
    psi = np.zeros((6, n, n, n), dtype=np.complex128)
    c_idx = n // 2
    amp = 1.0 / np.sqrt(6.0)
    for k in range(6):
        psi[k, c_idx, c_idx, c_idx] = amp

    # Build theta fields
    theta_plus_field = np.full((n, n, n), theta_plus_0)
    theta_minus_field = np.full((n, n, n), theta_minus_0)

    if mass_positions:
        total_f = np.zeros((n, n, n))
        for mp in mass_positions:
            r = min_image_dist(n, mp)
            total_f += strength / (r + 0.1)
        # Modulate both parameters by same field (gravity coupling)
        theta_plus_field = theta_plus_0 * (1.0 - total_f)
        theta_minus_field = theta_minus_0 * (1.0 - total_f)

    fields = precompute_block_circulant_fields(theta_plus_field, theta_minus_field)

    for _ in range(n_layers):
        psi = apply_coupled_coin_and_shift(psi, n, None, fields)

    return psi


def probability_density(psi):
    return np.sum(np.abs(psi)**2, axis=0)


def run_closure_card(theta_plus, theta_minus, n=15, n_layers=14):
    """Run 10-property closure card with coupled coin."""
    print(f"\n{'='*70}")
    print(f"CLOSURE CARD: Block-Circulant (theta+={theta_plus:.4f}, theta-={theta_minus:.4f})")
    print(f"  n={n}, N={n_layers}")
    print(f"{'='*70}")

    c = n // 2
    STRENGTH = 5e-4
    score = 0

    # 1. Born |I3|/P
    print("\n  [1] Born |I3|/P...")
    barrier_layer = 6
    slit_positions = [c - 2, c, c + 2]

    def evolve_with_barrier(slits):
        psi = np.zeros((6, n, n, n), dtype=np.complex128)
        amp = 1.0 / np.sqrt(6.0)
        for k in range(6):
            psi[k, c, c, c] = amp
        fields_flat = precompute_block_circulant_fields(
            np.full((n,n,n), theta_plus), np.full((n,n,n), theta_minus))
        for step in range(n_layers):
            psi = apply_coupled_coin_and_shift(psi, n, None, fields_flat)
            if step == barrier_layer - 1:
                mask = np.zeros((n, n, n), dtype=bool)
                for sy in slits:
                    mask[sy, :, :] = True
                for k in range(6):
                    psi[k] = psi[k] * mask
        return probability_density(psi)

    rho_full = evolve_with_barrier(slit_positions)
    rho_singles = [evolve_with_barrier([s]) for s in slit_positions]
    I3 = rho_full - sum(rho_singles)
    P_total = np.sum(rho_full)
    born = np.sum(np.abs(I3)) / P_total if P_total > 0 else 0.0
    p1 = born > 0.01
    print(f"      |I3|/P = {born:.6f}  {'PASS' if p1 else 'FAIL'}")
    if p1: score += 1

    # 2. d_TV
    print("  [2] d_TV...")
    rho_up = evolve_with_barrier([c - 2])
    rho_dn = evolve_with_barrier([c + 2])
    p_up = rho_up / np.sum(rho_up) if np.sum(rho_up) > 0 else rho_up
    p_dn = rho_dn / np.sum(rho_dn) if np.sum(rho_dn) > 0 else rho_dn
    dtv = 0.5 * np.sum(np.abs(p_up - p_dn))
    p2 = dtv > 0.01
    print(f"      d_TV = {dtv:.6f}  {'PASS' if p2 else 'FAIL'}")
    if p2: score += 1

    # 3. f=0 control
    print("  [3] f=0 control...")
    psi0 = evolve_coupled(n, n_layers, 0.0, theta_plus, theta_minus)
    rho0 = probability_density(psi0)
    plus_z = np.sum(rho0[c, c, c+1:c+4])
    minus_z = np.sum(rho0[c, c, c-3:c])
    bias = abs(plus_z - minus_z) / (plus_z + minus_z) if (plus_z + minus_z) > 0 else 0
    p3 = bias < 0.01
    print(f"      bias = {bias:.8f}  {'PASS' if p3 else 'FAIL'}")
    if p3: score += 1

    # 4. F proportional to M
    print("  [4] F~M...")
    rho0 = probability_density(evolve_coupled(n, n_layers, 0.0, theta_plus, theta_minus))
    strengths = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3]
    forces = []
    for s in strengths:
        psi1 = evolve_coupled(n, n_layers, s, theta_plus, theta_minus, [(c, c, c+3)])
        rho1 = probability_density(psi1)
        delta = rho1 - rho0
        force = sum(delta[c, c, c+dz] for dz in range(1, 4))
        forces.append(force)
    forces_arr = np.array(forces)
    strengths_arr = np.array(strengths)
    coeffs = np.polyfit(strengths_arr, forces_arr, 1)
    predicted = np.polyval(coeffs, strengths_arr)
    ss_res = np.sum((forces_arr - predicted)**2)
    ss_tot = np.sum((forces_arr - np.mean(forces_arr))**2)
    r2_fm = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    p4 = r2_fm > 0.9
    print(f"      R^2 = {r2_fm:.6f}  {'PASS' if p4 else 'FAIL'}")
    if p4: score += 1

    # 5. Gravity sign
    print("  [5] Gravity sign...")
    rho0 = probability_density(evolve_coupled(n, n_layers, 0.0, theta_plus, theta_minus))
    psi1 = evolve_coupled(n, n_layers, STRENGTH, theta_plus, theta_minus, [(c, c, c+3)])
    rho1 = probability_density(psi1)
    delta = rho1 - rho0
    toward = sum(delta[c, c, c+dz] for dz in range(1, 4))
    away = sum(delta[c, c, c-dz] for dz in range(1, 4))
    is_toward = toward > away
    p5 = is_toward
    print(f"      toward={toward:.4e}, away={away:.4e} -> {'TOWARD' if is_toward else 'AWAY'}  {'PASS' if p5 else 'FAIL'}")
    if p5: score += 1

    # 6. Decoherence
    print("  [6] Decoherence...")
    # Born with noise should decrease
    def born_noisy(noise_str):
        rng = np.random.RandomState(42)
        psi = np.zeros((6, n, n, n), dtype=np.complex128)
        amp = 1.0 / np.sqrt(6.0)
        for k in range(6):
            psi[k, c, c, c] = amp
        fields_flat = precompute_block_circulant_fields(
            np.full((n,n,n), theta_plus), np.full((n,n,n), theta_minus))
        for step in range(n_layers):
            if noise_str > 0:
                phase = rng.uniform(-noise_str, noise_str, (n,n,n))
                pf = np.exp(1j * phase)
                for k in range(6):
                    psi[k] = psi[k] * pf
            psi = apply_coupled_coin_and_shift(psi, n, None, fields_flat)
            if step == barrier_layer - 1:
                mask = np.zeros((n,n,n), dtype=bool)
                for sy in slit_positions:
                    mask[sy,:,:] = True
                for k in range(6):
                    psi[k] = psi[k] * mask
        rho = probability_density(psi)
        rho_s = [evolve_with_barrier([s]) for s in slit_positions]
        I3 = rho - sum(rho_s)
        P = np.sum(rho)
        return np.sum(np.abs(I3)) / P if P > 0 else 0.0

    bc = born  # clean born from test 1
    bn = born_noisy(0.5)
    p6 = bn < bc
    print(f"      clean={bc:.6f}, noisy={bn:.6f}  {'PASS' if p6 else 'FAIL'}")
    if p6: score += 1

    # 7. MI
    print("  [7] Mutual information...")
    psi_g = evolve_coupled(n, n_layers, STRENGTH, theta_plus, theta_minus, [(c,c,c)])
    rho_g = probability_density(psi_g)
    rho_n = rho_g / np.sum(rho_g)
    p_y = np.sum(rho_n, axis=(1,2))
    p_z = np.sum(rho_n, axis=(0,2))
    p_yz = np.sum(rho_n, axis=2)
    mi = 0.0
    for iy in range(n):
        for iz in range(n):
            if p_yz[iy,iz] > 1e-30 and p_y[iy] > 1e-30 and p_z[iz] > 1e-30:
                mi += p_yz[iy,iz] * np.log(p_yz[iy,iz] / (p_y[iy] * p_z[iz]))
    p7 = mi > 0.0
    print(f"      MI = {mi:.6e}  {'PASS' if p7 else 'FAIL'}")
    if p7: score += 1

    # 8. Purity stable
    print("  [8] Purity stable...")
    purities = {}
    for L in [10, 12, 14]:
        psi = evolve_coupled(n, L, STRENGTH, theta_plus, theta_minus, [(c,c,c)])
        rho = probability_density(psi)
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
    for L in [10, 12, 14]:
        rho0 = probability_density(evolve_coupled(n, L, 0.0, theta_plus, theta_minus))
        psi1 = evolve_coupled(n, L, STRENGTH, theta_plus, theta_minus, [(c,c,c+3)])
        rho1 = probability_density(psi1)
        delta = rho1 - rho0
        gforces[L] = sum(delta[c, c, c+dz] for dz in range(1, 4))
    vals_g = [gforces[L] for L in [10, 12, 14]]
    mono = all(vals_g[i] <= vals_g[i+1] for i in range(len(vals_g)-1))
    p9 = mono
    for ll, gf in gforces.items():
        print(f"      L={ll}: force={gf:.4e}")
    print(f"      Monotonic: {mono}  {'PASS' if p9 else 'FAIL'}")
    if p9: score += 1

    # 10. Distance law
    print("  [10] Distance law...")
    max_offset = min(5, n // 4)
    offsets = list(range(2, max_offset + 1))
    forces_dl = []
    rho0 = probability_density(evolve_coupled(n, n_layers, 0.0, theta_plus, theta_minus))
    for dz in offsets:
        psi1 = evolve_coupled(n, n_layers, STRENGTH, theta_plus, theta_minus, [(c,c,c+dz)])
        rho1 = probability_density(psi1)
        delta = rho1 - rho0
        force = sum(delta[c, c, c+dd] for dd in range(1, dz+1))
        forces_dl.append(force)
    forces_dl_arr = np.array(forces_dl)
    offsets_arr = np.array(offsets, dtype=float)
    abs_f = np.abs(forces_dl_arr)
    valid = abs_f > 1e-30
    if np.sum(valid) >= 3:
        log_r = np.log(offsets_arr[valid])
        log_f = np.log(abs_f[valid])
        coeffs_dl = np.polyfit(log_r, log_f, 1)
        predicted_dl = np.polyval(coeffs_dl, log_r)
        ss_res_dl = np.sum((log_f - predicted_dl)**2)
        ss_tot_dl = np.sum((log_f - np.mean(log_f))**2)
        r2_dl = 1 - ss_res_dl / ss_tot_dl if ss_tot_dl > 0 else 0
        exp_dl = coeffs_dl[0]
    else:
        r2_dl, exp_dl = 0.0, 0.0
    p10 = r2_dl > 0.7
    print(f"      exponent={exp_dl:.3f}, R^2={r2_dl:.4f}  {'PASS' if p10 else 'FAIL'}")
    if p10: score += 1

    print(f"\n  CLOSURE CARD SCORE: {score}/10")
    labels = ["Born", "d_TV", "f=0", "F~M", "TOWARD", "Decoh", "MI", "Purity", "GravGrow", "DistLaw"]
    results = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
    for lab, res in zip(labels, results):
        print(f"    {lab:10s} {'PASS' if res else 'FAIL'}")
    return score, results


# ============================================================================
# SECTION 6: Aharonov-Bohm Test
# ============================================================================

def ab_test_coupled(C6_func, params, n=9):
    """Aharonov-Bohm test: sweep flux A, measure modulation visibility."""
    print(f"\n{'='*70}")
    print("AHARONOV-BOHM TEST")
    print(f"{'='*70}")

    n_layers = 12
    c_idx = n // 2

    def evolve_ab(A_flux):
        psi = np.zeros(n*n*n*6, dtype=complex)
        amp = 1.0 / np.sqrt(6.0)
        for comp in range(6):
            idx = ((c_idx * n + c_idx) * n + c_idx) * 6 + comp
            psi[idx] = amp

        # Build uniform coupled coin
        C6 = C6_func(*params)
        # Apply AB phase to shift: multiply component by exp(i*A) per direction
        for step in range(n_layers):
            # Coin step (uniform, coupled)
            psi_4d = psi.reshape(n, n, n, 6)
            psi_coined = np.einsum('ij,yzwj->yzwi', C6, psi_4d).reshape(-1)

            # Shift with AB phase
            psi_4d = psi_coined.reshape(n, n, n, 6).copy()
            out = np.zeros_like(psi_4d)
            # +y with phase exp(+iA)
            out[:,:,:,0] = np.roll(psi_4d[:,:,:,0], +1, axis=0) * np.exp(1j*A_flux)
            out[:,:,:,1] = np.roll(psi_4d[:,:,:,1], -1, axis=0) * np.exp(-1j*A_flux)
            out[:,:,:,2] = np.roll(psi_4d[:,:,:,2], +1, axis=1)
            out[:,:,:,3] = np.roll(psi_4d[:,:,:,3], -1, axis=1)
            out[:,:,:,4] = np.roll(psi_4d[:,:,:,4], +1, axis=2)
            out[:,:,:,5] = np.roll(psi_4d[:,:,:,5], -1, axis=2)
            psi = out.reshape(-1)

        rho = np.abs(psi.reshape(n,n,n,6))**2
        rho_site = np.sum(rho, axis=3)
        # Measure probability at a detection point
        det_y = c_idx + 3
        if det_y < n:
            P_det = np.sum(rho_site[det_y, :, :])
        else:
            P_det = 0.0
        return P_det

    A_values = np.linspace(0, 2*np.pi, 13)
    P_values = []
    for A in A_values:
        P = evolve_ab(A)
        P_values.append(P)
        print(f"  A={A:.2f}: P={P:.6f}")

    P_values = np.array(P_values)
    if np.max(P_values) > 0:
        V_ab = (np.max(P_values) - np.min(P_values)) / (np.max(P_values) + np.min(P_values))
    else:
        V_ab = 0.0

    print(f"\n  AB visibility V = {V_ab:.4f}")
    ab_pass = V_ab > 0.5
    print(f"  {'PASS' if ab_pass else 'FAIL'} (need V > 0.5)")
    return V_ab, ab_pass


# ============================================================================
# SECTION 7: MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()

    print("=" * 70)
    print("COUPLED DIRAC-LIKE COIN FOR 3+1D CHIRAL WALK")
    print("=" * 70)
    print("HYPOTHESIS: Coupled 6x6 coin can produce isotropic 3D KG (R^2>0.99)")
    print("FALSIFICATION: If no coin achieves R^2>0.90, 6-component is structural no-go")
    print("CURRENT BASELINE: Factorized coin R^2=0.156, AB V=0.0")
    print()

    # Baseline check
    print("--- BASELINE: Factorized coin ---")
    C_base = coin_factorized(0.3)
    r2_base, m_base, c2_base, _ = bloch_kg_analysis(C_base, 9, verbose=True)
    print(f"  Baseline R^2 = {r2_base:.6f}\n")

    # Run all sweeps
    n_bloch = 9

    r2_bc, tp_bc, tm_bc = sweep_block_circulant(n_bloch)
    r2_cy, eps_cy = sweep_cayley(n_bloch)
    r2_dft, th_dft = sweep_dft6(n_bloch)
    r2_gr, th_gr = sweep_grover6(n_bloch)
    r2_de, th_de = sweep_dirac_embed(n_bloch)

    # Summary table
    print(f"\n{'='*70}")
    print("SWEEP SUMMARY")
    print(f"{'='*70}")
    candidates = [
        ("Factorized (baseline)", r2_base, "theta=0.3"),
        ("Block-Circulant", r2_bc, f"theta+={tp_bc:.4f}, theta-={tm_bc:.4f}"),
        ("Cayley-Coupled", r2_cy, f"theta=0.3, eps={eps_cy:.4f}"),
        ("DFT-6", r2_dft, f"theta={th_dft:.4f}"),
        ("Grover-6", r2_gr, f"theta={th_gr:.4f}"),
        ("Dirac-Embedded", r2_de, f"theta={th_de:.4f}"),
    ]
    candidates.sort(key=lambda x: -x[1])
    print(f"  {'Coin':<25s} {'R^2':>10s}  {'Params'}")
    print(f"  {'-'*25} {'-'*10}  {'-'*30}")
    for name, r2, params in candidates:
        marker = " ***" if r2 > 0.90 else ""
        print(f"  {name:<25s} {r2:10.6f}  {params}{marker}")

    # Find best
    best_name, best_r2 = candidates[0][0], candidates[0][1]

    # Deep analysis of winner
    if best_r2 > r2_base + 0.01:
        # Build the best coin for deep analysis
        if "Block-Circulant" in best_name:
            C_best = coin_block_circulant(tp_bc, tm_bc)
            deep_analysis(C_best, f"Block-Circulant (theta+={tp_bc:.4f}, theta-={tm_bc:.4f})", n_bloch)
        elif "Cayley" in best_name:
            C_best = coin_cayley(0.3, eps_cy)
            deep_analysis(C_best, f"Cayley-Coupled (eps={eps_cy:.4f})", n_bloch)
        elif "DFT" in best_name:
            C_best = coin_dft6(th_dft)
            deep_analysis(C_best, f"DFT-6 (theta={th_dft:.4f})", n_bloch)
        elif "Grover" in best_name:
            C_best = coin_grover6(th_gr)
            deep_analysis(C_best, f"Grover-6 (theta={th_gr:.4f})", n_bloch)
        elif "Dirac" in best_name:
            C_best = coin_dirac_embed(th_de)
            deep_analysis(C_best, f"Dirac-Embedded (theta={th_de:.4f})", n_bloch)

    # Run closure card if best is block-circulant and R^2 is promising
    closure_score = None
    if best_r2 > 0.5 and "Block-Circulant" in best_name:
        closure_score, closure_results = run_closure_card(tp_bc, tm_bc, n=15, n_layers=12)

    # AB test on the best coin
    ab_v = None
    if best_r2 > 0.5:
        if "Block-Circulant" in best_name:
            ab_v, ab_pass = ab_test_coupled(coin_block_circulant, (tp_bc, tm_bc), n=9)
        elif "Cayley" in best_name:
            ab_v, ab_pass = ab_test_coupled(coin_cayley, (0.3, eps_cy), n=9)

    # Even if best didn't beat threshold, run closure + AB on block-circulant if it's close
    if closure_score is None and r2_bc > r2_base + 0.01:
        print("\n  (Running closure card on best block-circulant even though R^2 < 0.5)")
        closure_score, closure_results = run_closure_card(tp_bc, tm_bc, n=15, n_layers=12)
    if ab_v is None and r2_bc > r2_base + 0.01:
        ab_v, ab_pass = ab_test_coupled(coin_block_circulant, (tp_bc, tm_bc), n=9)

    # ========================================================================
    # VERDICT
    # ========================================================================
    elapsed = time.time() - t_start

    print(f"\n{'='*70}")
    print("FINAL VERDICT")
    print(f"{'='*70}")
    print(f"  Baseline factorized R^2:    {r2_base:.6f}")
    print(f"  Best coupled R^2:           {best_r2:.6f} ({best_name})")
    print(f"  KG R^2 > 0.99 target:       {'PASS' if best_r2 > 0.99 else 'FAIL'}")
    print(f"  KG R^2 > 0.90 threshold:    {'PASS' if best_r2 > 0.90 else 'FAIL (structural no-go)'}")
    if ab_v is not None:
        print(f"  AB visibility:              {ab_v:.4f} ({'PASS' if ab_v > 0.5 else 'FAIL'})")
    if closure_score is not None:
        print(f"  Closure card:               {closure_score}/10")

    if best_r2 > 0.99:
        print("\n  RESULT: Coupled coin achieves isotropic 3D Klein-Gordon. Not falsified.")
    elif best_r2 > 0.90:
        print("\n  RESULT: Coupled coin shows significant improvement but not fully isotropic.")
        print("  The 6-component architecture can support cross-pair coupling.")
    elif best_r2 > r2_base + 0.05:
        print("\n  RESULT: Coupled coin shows marginal improvement over factorized.")
        print("  Cross-coupling helps but is insufficient for isotropic KG.")
    else:
        print("\n  RESULT: No tested 6x6 on-site coin improves significantly on factorized.")
        print("  The 6-component + single-site architecture may be structurally limited.")
        print("  Next steps: try 8-component basis, multi-step coin, or non-local coin.")

    print(f"\n  Total time: {elapsed:.1f}s")
