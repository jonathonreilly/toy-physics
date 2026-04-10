#!/usr/bin/env python3
"""
frontier_chiral_2plus1d_dispersion.py

KEY TEST: Does the 2+1D chiral walk give E² = θ² + k_y² + k_z² (Klein-Gordon)?

Architecture: Each site (y,z) has 4 chiral components: ψ_{+y}, ψ_{-y}, ψ_{+z}, ψ_{-z}.
Per layer: Coin (4x4 unitary at each site) then Shift (each chirality moves 1 step).

Tests three coins:
  1. Factorized: C_y(θ) ⊗ C_z(θ)  — expected to NOT give KG (sum of 1D dispersions)
  2. Grover-4: (1/2)J_4 - I_4      — isotropic mixing
  3. DFT-4: 4x4 DFT matrix         — another isotropic option

HYPOTHESIS: At least one coin gives E² = m² + k_y² + k_z² (isotropic Klein-Gordon).
FALSIFICATION: All coins give anisotropic or non-Klein-Gordon dispersion.
"""

import numpy as np
from numpy import linalg as la
import warnings
warnings.filterwarnings('ignore')

# ── Parameters ──────────────────────────────────────────────────────────
N_Y = 11       # grid size in y
N_Z = 11       # grid size in z
THETA = 0.3    # coin angle
N_INTERNAL = 4 # chiralities: +y, -y, +z, -z
N_TOTAL = N_INTERNAL * N_Y * N_Z

print("=" * 72)
print("FRONTIER: 2+1D Chiral Walk Dispersion")
print("=" * 72)
print(f"Grid: {N_Y} x {N_Z}, θ = {THETA}, dim = {N_TOTAL}")
print()


def index(c, y, z):
    """Flat index for chirality c, site (y, z)."""
    return c * (N_Y * N_Z) + y * N_Z + z


def build_shift_matrix():
    """Build the shift operator: each chirality shifts 1 step in its direction.
    c=0: +y (y -> y+1), c=1: -y (y -> y-1), c=2: +z (z -> z+1), c=3: -z (z -> z-1)
    Periodic boundaries.
    """
    S = np.zeros((N_TOTAL, N_TOTAL), dtype=complex)
    for y in range(N_Y):
        for z in range(N_Z):
            # +y: moves to y+1
            S[index(0, (y + 1) % N_Y, z), index(0, y, z)] = 1.0
            # -y: moves to y-1
            S[index(1, (y - 1) % N_Y, z), index(1, y, z)] = 1.0
            # +z: moves to z+1
            S[index(2, y, (z + 1) % N_Z), index(2, y, z)] = 1.0
            # -z: moves to z-1
            S[index(3, y, (z - 1) % N_Z), index(3, y, z)] = 1.0
    return S


def build_coin_matrix(coin_4x4):
    """Apply a 4x4 coin at every site."""
    C = np.zeros((N_TOTAL, N_TOTAL), dtype=complex)
    for y in range(N_Y):
        for z in range(N_Z):
            for ci in range(N_INTERNAL):
                for cj in range(N_INTERNAL):
                    C[index(ci, y, z), index(cj, y, z)] = coin_4x4[ci, cj]
    return C


def build_evolution(coin_4x4):
    """U = S . C (coin then shift)."""
    S = build_shift_matrix()
    C = build_coin_matrix(coin_4x4)
    return S @ C


def extract_dispersion(U, coin_name):
    """Eigendecompose U, extract (E, k_y, k_z) for each mode."""
    eigenvalues, eigenvectors = la.eig(U)

    # Verify unitarity
    mags = np.abs(eigenvalues)
    print(f"  Unitarity check: |λ| in [{mags.min():.6f}, {mags.max():.6f}]")

    # Eigenphases
    E_all = np.angle(eigenvalues)  # in [-π, π]

    # Allowed momenta
    ky_vals = 2 * np.pi * np.arange(N_Y) / N_Y  # [0, 2π/N, ..., 2π(N-1)/N]
    kz_vals = 2 * np.pi * np.arange(N_Z) / N_Z

    results = []
    for idx in range(N_TOTAL):
        E = E_all[idx]
        vec = eigenvectors[:, idx]

        # For each chirality, compute spatial Fourier transform to find dominant (ky, kz)
        # Sum over chiralities to get total momentum content
        power_yz = np.zeros((N_Y, N_Z))
        for c in range(N_INTERNAL):
            psi_yz = np.zeros((N_Y, N_Z), dtype=complex)
            for y in range(N_Y):
                for z in range(N_Z):
                    psi_yz[y, z] = vec[index(c, y, z)]
            ft = np.fft.fft2(psi_yz)
            power_yz += np.abs(ft) ** 2

        # Find dominant momentum
        iy, iz = np.unravel_index(np.argmax(power_yz), power_yz.shape)
        ky_dom = ky_vals[iy]
        kz_dom = kz_vals[iz]

        # Wrap to [-π, π]
        if ky_dom > np.pi:
            ky_dom -= 2 * np.pi
        if kz_dom > np.pi:
            kz_dom -= 2 * np.pi

        # Sharpness: fraction of power in dominant mode
        sharpness = power_yz[iy, iz] / power_yz.sum()

        results.append((E, ky_dom, kz_dom, sharpness))

    return results


def analyze_dispersion(results, coin_name):
    """Fit E² vs k² and check for Klein-Gordon."""
    print(f"\n{'─' * 60}")
    print(f"  COIN: {coin_name}")
    print(f"{'─' * 60}")

    # Filter for sharp momentum modes (well-defined k)
    sharp = [(E, ky, kz, s) for E, ky, kz, s in results if s > 0.3]
    print(f"  Total modes: {len(results)}, sharp (s>0.3): {len(sharp)}")

    if len(sharp) < 10:
        print("  WARNING: Too few sharp modes for reliable fit")
        # Lower threshold
        sharp = [(E, ky, kz, s) for E, ky, kz, s in results if s > 0.1]
        print(f"  Relaxed (s>0.1): {len(sharp)}")

    if len(sharp) < 5:
        print("  SKIP: insufficient sharp modes")
        return None

    E_arr = np.array([r[0] for r in sharp])
    ky_arr = np.array([r[1] for r in sharp])
    kz_arr = np.array([r[2] for r in sharp])

    E2 = E_arr ** 2
    k2 = ky_arr ** 2 + kz_arr ** 2

    # ── Test 1: E² = m² + k² (isotropic Klein-Gordon) ──
    # Linear regression: E² = a + b * k²
    if k2.max() - k2.min() > 1e-10:
        A = np.column_stack([np.ones(len(k2)), k2])
        coeffs, residuals, _, _ = la.lstsq(A, E2, rcond=None)
        m2_fit = coeffs[0]
        slope = coeffs[1]
        E2_pred = A @ coeffs
        ss_res = np.sum((E2 - E2_pred) ** 2)
        ss_tot = np.sum((E2 - E2.mean()) ** 2)
        R2_iso = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        print(f"\n  [Isotropic fit] E² = {m2_fit:.4f} + {slope:.4f} * k²")
        print(f"    R² = {R2_iso:.6f}")
        print(f"    m² = {m2_fit:.4f}, expected θ² = {THETA**2:.4f}")
        print(f"    slope = {slope:.4f}, expected 1.0 for Klein-Gordon")
    else:
        R2_iso = 0
        print("  Insufficient k² spread for isotropic fit")

    # ── Test 2: E² = m² + a*k_y² + b*k_z² (anisotropic) ──
    ky2 = ky_arr ** 2
    kz2 = kz_arr ** 2
    A2 = np.column_stack([np.ones(len(ky2)), ky2, kz2])
    coeffs2, _, _, _ = la.lstsq(A2, E2, rcond=None)
    E2_pred2 = A2 @ coeffs2
    ss_res2 = np.sum((E2 - E2_pred2) ** 2)
    ss_tot2 = np.sum((E2 - E2.mean()) ** 2)
    R2_aniso = 1 - ss_res2 / ss_tot2 if ss_tot2 > 0 else 0

    print(f"\n  [Anisotropic fit] E² = {coeffs2[0]:.4f} + {coeffs2[1]:.4f}*k_y² + {coeffs2[2]:.4f}*k_z²")
    print(f"    R² = {R2_aniso:.6f}")
    print(f"    Isotropy ratio a_y/a_z = {coeffs2[1]/coeffs2[2]:.4f}" if abs(coeffs2[2]) > 1e-10 else "")

    # ── Test 3: cos(E) = cos(θ)*cos(ky)*cos(kz) analytic (factorized) ──
    cos_E_pred = np.cos(THETA) * np.cos(ky_arr) * np.cos(THETA) * np.cos(kz_arr)
    # Actually for factorized: E = E_y + E_z where cos(E_y) = cos(θ)cos(k_y)
    # So cos(E_y) = cos(θ)cos(ky), E_y = arccos(cos(θ)cos(ky))
    # E = E_y + E_z
    E_y_pred = np.arccos(np.clip(np.cos(THETA) * np.cos(ky_arr), -1, 1))
    E_z_pred = np.arccos(np.clip(np.cos(THETA) * np.cos(kz_arr), -1, 1))
    E_sum_pred = E_y_pred + E_z_pred

    residual_sum = np.mean((np.abs(E_arr) - E_sum_pred) ** 2)
    print(f"\n  [Factorized test] <(|E| - E_y - E_z)²> = {residual_sum:.6f}")

    # ── Test 4: Direct cos(E) relation ──
    # Try cos(E) = f(ky, kz) for various forms
    cos_E = np.cos(E_arr)

    # Test cos(E) = cos(θ²) * cos(ky) * cos(kz)  (possible KG form)
    cos_pred_kg = np.cos(THETA) * np.cos(ky_arr) * np.cos(kz_arr)
    res_kg = np.mean((cos_E - cos_pred_kg) ** 2)
    print(f"  [cos test] <(cos E - cosθ·cos ky·cos kz)²> = {res_kg:.6f}")

    # ── Test 5: Check a few specific modes ──
    print(f"\n  Sample modes (E, ky, kz, sharpness):")
    sorted_modes = sorted(sharp, key=lambda r: r[1] ** 2 + r[2] ** 2)
    for i in range(min(15, len(sorted_modes))):
        E, ky, kz, s = sorted_modes[i]
        print(f"    E={E:+.4f}  ky={ky:+.4f}  kz={kz:+.4f}  k²={ky**2+kz**2:.4f}  E²={E**2:.4f}  s={s:.3f}")

    return {
        'R2_iso': R2_iso,
        'R2_aniso': R2_aniso,
        'coin': coin_name,
    }


def check_1d_baseline():
    """Verify 1+1D chiral walk gives E² = θ² + k² as baseline."""
    print("\n" + "=" * 72)
    print("BASELINE: 1+1D Chiral Walk")
    print("=" * 72)

    N = 21
    cos_t = np.cos(THETA)
    sin_t = np.sin(THETA)
    coin_2x2 = np.array([[cos_t, -sin_t], [sin_t, cos_t]])

    # Build 1D evolution: U = S . C
    dim = 2 * N
    S = np.zeros((dim, dim), dtype=complex)
    C_full = np.zeros((dim, dim), dtype=complex)

    for x in range(N):
        # Shift: +chirality goes right, -chirality goes left
        S[0 * N + (x + 1) % N, 0 * N + x] = 1.0
        S[1 * N + (x - 1) % N, 1 * N + x] = 1.0
        # Coin
        for ci in range(2):
            for cj in range(2):
                C_full[ci * N + x, cj * N + x] = coin_2x2[ci, cj]

    U = S @ C_full
    eigenvalues = la.eigvals(U)
    E_all = np.angle(eigenvalues)

    # Extract momenta
    eigvals, eigvecs = la.eig(U)
    k_vals = 2 * np.pi * np.arange(N) / N

    modes = []
    for idx in range(dim):
        E = np.angle(eigvals[idx])
        vec = eigvecs[:, idx]
        power = np.zeros(N)
        for c in range(2):
            psi = np.array([vec[c * N + x] for x in range(N)])
            ft = np.fft.fft(psi)
            power += np.abs(ft) ** 2
        ix = np.argmax(power)
        k = k_vals[ix]
        if k > np.pi:
            k -= 2 * np.pi
        sharpness = power[ix] / power.sum()
        modes.append((E, k, sharpness))

    sharp = [(E, k, s) for E, k, s in modes if s > 0.3]
    E_arr = np.array([r[0] for r in sharp])
    k_arr = np.array([r[1] for r in sharp])
    E2 = E_arr ** 2
    k2 = k_arr ** 2

    A = np.column_stack([np.ones(len(k2)), k2])
    coeffs, _, _, _ = la.lstsq(A, E2, rcond=None)
    E2_pred = A @ coeffs
    ss_res = np.sum((E2 - E2_pred) ** 2)
    ss_tot = np.sum((E2 - E2.mean()) ** 2)
    R2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    print(f"  1D fit: E² = {coeffs[0]:.4f} + {coeffs[1]:.4f} * k²")
    print(f"  R² = {R2:.6f}")
    print(f"  m² = {coeffs[0]:.4f}, θ² = {THETA**2:.4f}")
    print(f"  slope = {coeffs[1]:.4f} (expect 1.0)")
    print(f"  1D Klein-Gordon: {'PASS' if R2 > 0.99 and abs(coeffs[1] - 1.0) < 0.1 else 'FAIL'}")


# ── Build coins ─────────────────────────────────────────────────────────

# Coin 1: Factorized C_y(θ) ⊗ C_z(θ)
cos_t = np.cos(THETA)
sin_t = np.sin(THETA)
C_y = np.array([[cos_t, -sin_t], [sin_t, cos_t]])
C_z = np.array([[cos_t, -sin_t], [sin_t, cos_t]])
coin_factorized = np.kron(C_y, C_z)

# Coin 2: Grover-4 = (1/2)J_4 - I_4
J4 = np.ones((4, 4))
coin_grover = 0.5 * J4 - np.eye(4)

# Coin 3: DFT-4
coin_dft = np.fft.fft(np.eye(4)) / 2  # normalized

# Coin 4: Rotation that couples all 4 — parametric
# Use a rotation in SO(4) parameterized by θ
# Specifically: exp(θ * A) where A is antisymmetric mixing all pairs
A_mix = np.array([
    [0, -1, -1, 0],
    [1, 0, 0, -1],
    [1, 0, 0, -1],
    [0, 1, 1, 0]
], dtype=float) * THETA / np.sqrt(2)
A_mix = (A_mix - A_mix.T) / 2  # ensure antisymmetric
coin_so4 = la.expm(A_mix) if hasattr(la, 'expm') else None

# Use scipy for matrix exponential
try:
    from scipy.linalg import expm
    coin_so4 = expm(A_mix)
except ImportError:
    # Manual: for small θ, use Padé approximant
    coin_so4 = np.eye(4) + A_mix + A_mix @ A_mix / 2 + A_mix @ A_mix @ A_mix / 6


# ── Run baseline ────────────────────────────────────────────────────────
check_1d_baseline()

# ── Run 2+1D tests ─────────────────────────────────────────────────────
coins = {
    "Factorized C_y⊗C_z": coin_factorized,
    "Grover-4 (½J-I)": coin_grover,
    "DFT-4 (normalized)": coin_dft,
    "SO(4) rotation": coin_so4,
}

print("\n" + "=" * 72)
print("SHIFT OPERATOR")
print("=" * 72)
S = build_shift_matrix()
print(f"  Shape: {S.shape}")
print(f"  Unitarity: |det(S)| = {abs(la.det(S)):.6f}")

all_results = {}
for name, coin in coins.items():
    # Verify coin unitarity
    uu = coin @ coin.conj().T
    is_unitary = np.allclose(uu, np.eye(4), atol=1e-10)
    print(f"\n  Coin '{name}': unitary = {is_unitary}")
    if not is_unitary:
        print(f"    UU† max deviation: {np.max(np.abs(uu - np.eye(4))):.2e}")

    print(f"  Building evolution operator...")
    U = build_evolution(coin)

    print(f"  Eigendecomposing {U.shape[0]}x{U.shape[0]} matrix...")
    results = extract_dispersion(U, name)
    summary = analyze_dispersion(results, name)
    if summary:
        all_results[name] = summary

# ── Deeper analysis: try cos(E) = cos(m) * cos(ky) * cos(kz) ──
print("\n" + "=" * 72)
print("DEEPER ANALYSIS: Exact dispersion relations")
print("=" * 72)

for name, coin in coins.items():
    print(f"\n{'─' * 60}")
    print(f"  {name}")
    print(f"{'─' * 60}")

    # Bloch analysis: for each (ky, kz), diagonalize the 4x4 Bloch Hamiltonian
    # U(ky,kz) = S(ky,kz) . C where S(ky,kz) is diagonal with phase shifts
    # S(ky,kz) = diag(e^{iky}, e^{-iky}, e^{ikz}, e^{-ikz})

    ky_fine = np.linspace(-np.pi, np.pi, 101)
    kz_fine = np.linspace(-np.pi, np.pi, 101)

    # Scan along ky with kz=0
    E_vs_ky = []
    for ky in ky_fine:
        S_bloch = np.diag([np.exp(1j * ky), np.exp(-1j * ky),
                           np.exp(0j), np.exp(0j)])  # kz=0
        U_bloch = S_bloch @ coin
        eigs = la.eigvals(U_bloch)
        phases = np.sort(np.angle(eigs))
        E_vs_ky.append(phases)
    E_vs_ky = np.array(E_vs_ky)

    # Scan along kz with ky=0
    E_vs_kz = []
    for kz in kz_fine:
        S_bloch = np.diag([np.exp(0j), np.exp(0j),
                           np.exp(1j * kz), np.exp(-1j * kz)])
        U_bloch = S_bloch @ coin
        eigs = la.eigvals(U_bloch)
        phases = np.sort(np.angle(eigs))
        E_vs_kz.append(phases)
    E_vs_kz = np.array(E_vs_kz)

    # Scan diagonal ky=kz
    E_vs_kd = []
    for k in ky_fine:
        S_bloch = np.diag([np.exp(1j * k), np.exp(-1j * k),
                           np.exp(1j * k), np.exp(-1j * k)])
        U_bloch = S_bloch @ coin
        eigs = la.eigvals(U_bloch)
        phases = np.sort(np.angle(eigs))
        E_vs_kd.append(phases)
    E_vs_kd = np.array(E_vs_kd)

    print(f"  Band structure at k=0:")
    S0 = np.eye(4, dtype=complex)
    U0 = S0 @ coin
    eigs0 = la.eigvals(U0)
    E0 = np.sort(np.angle(eigs0))
    for i, e in enumerate(E0):
        print(f"    Band {i}: E(0,0) = {e:+.6f}")

    # Check: does |E| at k=0 give mass gap?
    mass_gap = np.min(np.abs(E0[E0 != 0])) if np.any(E0 != 0) else 0
    print(f"  Mass gap (min |E| at k=0): {mass_gap:.6f}")

    # Check Klein-Gordon: E² ≈ m² + k² near k=0
    # For each band, fit E²(ky, kz=0) near ky=0
    mid = len(ky_fine) // 2
    window = 15  # points near k=0
    for band in range(4):
        E_band = E_vs_ky[mid - window:mid + window + 1, band]
        ky_near = ky_fine[mid - window:mid + window + 1]

        E2_band = E_band ** 2
        k2_near = ky_near ** 2

        A = np.column_stack([np.ones(len(k2_near)), k2_near])
        coeffs, _, _, _ = la.lstsq(A, E2_band, rcond=None)
        E2_pred = A @ coeffs
        ss_res = np.sum((E2_band - E2_pred) ** 2)
        ss_tot = np.sum((E2_band - E2_band.mean()) ** 2)
        R2 = 1 - ss_res / ss_tot if ss_tot > 1e-15 else 0

        # Also check along kz (should give same slope for isotropy)
        E_band_kz = E_vs_kz[mid - window:mid + window + 1, band]
        E2_band_kz = E_band_kz ** 2
        kz_near = kz_fine[mid - window:mid + window + 1]
        k2_near_z = kz_near ** 2
        Az = np.column_stack([np.ones(len(k2_near_z)), k2_near_z])
        coeffs_z, _, _, _ = la.lstsq(Az, E2_band_kz, rcond=None)

        # Diagonal
        E_band_d = E_vs_kd[mid - window:mid + window + 1, band]
        E2_band_d = E_band_d ** 2
        kd_near = ky_fine[mid - window:mid + window + 1]
        k2_near_d = 2 * kd_near ** 2  # k² = ky² + kz² = 2k²
        Ad = np.column_stack([np.ones(len(k2_near_d)), k2_near_d])
        coeffs_d, _, _, _ = la.lstsq(Ad, E2_band_d, rcond=None)

        iso_check = abs(coeffs[1] - coeffs_z[1]) / max(abs(coeffs[1]), 1e-10) if abs(coeffs[1]) > 1e-10 else float('inf')

        print(f"\n    Band {band}: E(0)={E0[band]:+.4f}")
        print(f"      Along ky: E² = {coeffs[0]:.4f} + {coeffs[1]:.4f}*ky²  (R²={R2:.4f})")
        print(f"      Along kz: E² = {coeffs_z[0]:.4f} + {coeffs_z[1]:.4f}*kz²")
        print(f"      Diagonal: E² = {coeffs_d[0]:.4f} + {coeffs_d[1]:.4f}*(ky²+kz²)")
        print(f"      Isotropy: |slope_y - slope_z|/slope_y = {iso_check:.4f}")

        is_kg = (R2 > 0.99 and abs(coeffs[1] - 1.0) < 0.15
                 and iso_check < 0.05 and abs(coeffs_d[1] - 1.0) < 0.15)
        if is_kg:
            print(f"      *** KLEIN-GORDON: E² = {coeffs[0]:.4f} + k² ***")
        elif R2 > 0.99 and iso_check < 0.05:
            print(f"      Quadratic & isotropic but slope={coeffs[1]:.4f} (not 1)")


# ── FINAL VERDICT ───────────────────────────────────────────────────────
print("\n" + "=" * 72)
print("VERDICT")
print("=" * 72)

# Re-run Bloch analysis for summary
found_kg = False
for name, coin in coins.items():
    ky_fine = np.linspace(-np.pi, np.pi, 101)
    mid = len(ky_fine) // 2
    window = 15

    for kz_val in [0.0]:
        E_bands_ky = []
        for ky in ky_fine:
            S_bloch = np.diag([np.exp(1j * ky), np.exp(-1j * ky),
                               np.exp(1j * kz_val), np.exp(-1j * kz_val)])
            U_bloch = S_bloch @ coin
            eigs = la.eigvals(U_bloch)
            E_bands_ky.append(np.sort(np.angle(eigs)))
        E_bands_ky = np.array(E_bands_ky)

        E_bands_kz = []
        for kz in ky_fine:
            S_bloch = np.diag([np.exp(0j), np.exp(0j),
                               np.exp(1j * kz), np.exp(-1j * kz)])
            U_bloch = S_bloch @ coin
            eigs = la.eigvals(U_bloch)
            E_bands_kz.append(np.sort(np.angle(eigs)))
        E_bands_kz = np.array(E_bands_kz)

        E_bands_kd = []
        for k in ky_fine:
            S_bloch = np.diag([np.exp(1j * k), np.exp(-1j * k),
                               np.exp(1j * k), np.exp(-1j * k)])
            U_bloch = S_bloch @ coin
            eigs = la.eigvals(U_bloch)
            E_bands_kd.append(np.sort(np.angle(eigs)))
        E_bands_kd = np.array(E_bands_kd)

        for band in range(4):
            E_ky = E_bands_ky[mid - window:mid + window + 1, band]
            E_kz = E_bands_kz[mid - window:mid + window + 1, band]
            E_kd = E_bands_kd[mid - window:mid + window + 1, band]
            k_near = ky_fine[mid - window:mid + window + 1]

            # Fit ky direction
            A = np.column_stack([np.ones(len(k_near)), k_near ** 2])
            cy, _, _, _ = la.lstsq(A, E_ky ** 2, rcond=None)
            cz, _, _, _ = la.lstsq(A, E_kz ** 2, rcond=None)

            Ad = np.column_stack([np.ones(len(k_near)), 2 * k_near ** 2])
            cd, _, _, _ = la.lstsq(Ad, E_kd ** 2, rcond=None)

            slope_y = cy[1]
            slope_z = cz[1]
            slope_d = cd[1]
            m2 = cy[0]
            iso = abs(slope_y - slope_z) / max(abs(slope_y), 1e-10) if abs(slope_y) > 1e-10 else float('inf')

            if (abs(slope_y - 1.0) < 0.15 and abs(slope_z - 1.0) < 0.15
                    and abs(slope_d - 1.0) < 0.15 and iso < 0.05):
                print(f"  FOUND Klein-Gordon in '{name}', band {band}:")
                print(f"    E² = {m2:.4f} + k²  (slope_y={slope_y:.4f}, slope_z={slope_z:.4f}, slope_diag={slope_d:.4f})")
                print(f"    mass = {np.sqrt(abs(m2)):.4f}")
                found_kg = True

if not found_kg:
    print("  No coin produced exact E² = m² + k² Klein-Gordon.")
    print()
    print("  Checking for APPROXIMATE Klein-Gordon (slope in [0.5, 2.0], isotropic)...")
    for name, coin in coins.items():
        ky_fine = np.linspace(-np.pi, np.pi, 101)
        mid = len(ky_fine) // 2
        window = 15

        E_bands_ky = []
        for ky in ky_fine:
            S_bloch = np.diag([np.exp(1j * ky), np.exp(-1j * ky),
                               np.exp(0j), np.exp(0j)])
            U_bloch = S_bloch @ coin
            eigs = la.eigvals(U_bloch)
            E_bands_ky.append(np.sort(np.angle(eigs)))
        E_bands_ky = np.array(E_bands_ky)

        E_bands_kz = []
        for kz in ky_fine:
            S_bloch = np.diag([np.exp(0j), np.exp(0j),
                               np.exp(1j * kz), np.exp(-1j * kz)])
            U_bloch = S_bloch @ coin
            eigs = la.eigvals(U_bloch)
            E_bands_kz.append(np.sort(np.angle(eigs)))
        E_bands_kz = np.array(E_bands_kz)

        for band in range(4):
            E_ky = E_bands_ky[mid - window:mid + window + 1, band]
            E_kz = E_bands_kz[mid - window:mid + window + 1, band]
            k_near = ky_fine[mid - window:mid + window + 1]

            A = np.column_stack([np.ones(len(k_near)), k_near ** 2])
            cy, _, _, _ = la.lstsq(A, E_ky ** 2, rcond=None)
            cz, _, _, _ = la.lstsq(A, E_kz ** 2, rcond=None)

            slope_y = cy[1]
            slope_z = cz[1]
            m2 = cy[0]
            iso = abs(slope_y - slope_z) / max(abs(slope_y), 1e-10) if abs(slope_y) > 1e-10 else float('inf')

            if (0.5 < abs(slope_y) < 2.0 and iso < 0.1
                    and abs(m2) > 0.01):
                print(f"  Approximate KG: '{name}', band {band}")
                print(f"    E² ≈ {m2:.4f} + {slope_y:.4f}*k_y² + {slope_z:.4f}*k_z²")
                print(f"    Isotropy ratio: {iso:.4f}")

print()
print("HYPOTHESIS: 'At least one 2+1D coin gives E² = m² + k_y² + k_z²'")
if found_kg:
    print("RESULT: CONFIRMED")
else:
    print("RESULT: NOT CONFIRMED with tested coins")
    print("  The 2+1D chiral walk does NOT trivially extend 1D Klein-Gordon.")
    print("  Possible paths: different coin families, multi-step protocols,")
    print("  or accept that the lattice dispersion is cos(E) = f(cos ky, cos kz).")
