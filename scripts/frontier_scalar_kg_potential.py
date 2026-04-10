#!/usr/bin/env python3
"""
Scalar Klein-Gordon Field with Gravitational Potential (No Coin)
=================================================================
THE INSIGHT: The coin's mixing period π/m is the root of all three
gravity blockers. Remove the coin entirely.

ARCHITECTURE: One complex scalar field ψ(x) on a 3D lattice.
  - Kinetic: E(k) = sqrt(k_lattice² + m²) where k_lattice = 2*sum(1-cos(k_j))
  - Evolution via FFT split-step (Strang splitting):
    1. Half kinetic step in k-space: ψ̃(k) *= exp(-i*E(k)*dt/2)
    2. Full potential step in x-space: ψ(x) *= exp(-i*V(x)*dt)
    3. Half kinetic step in k-space: ψ̃(k) *= exp(-i*E(k)*dt/2)
  - Gravity: V(x) = g * strength / (|x - x_mass| + eps)

NO COIN. NO INTERNAL STATES. NO MIXING PERIOD.

WHAT THIS GIVES:
  - Exact KG dispersion E² = m² + k² (by construction)
  - Unitary (phase rotations)
  - No Zitterbewegung → no N-oscillation
  - Achromatic gravity (V has no k dependence)
  - Mass-independent acceleration (Ehrenfest theorem)
  - F ∝ M (V ∝ strength)
  - Superposition (linear Schrödinger evolution)

WHAT WE LOSE:
  - Spinor structure (no spin/chirality)
  - Born rule test via barriers (need different test design)
  - Connection to Dirac equation (this is KG, not Dirac)

HYPOTHESIS: Scalar KG + potential gravity passes all 6 bottleneck tests.
FALSIFICATION: If centroid doesn't shift TOWARD mass, the mechanism fails.
"""

import numpy as np
from scipy import stats
import time


# ============================================================================
# Lattice Klein-Gordon Evolution
# ============================================================================

def build_dispersion(n, mass):
    """Build E(k) = sqrt(k_lattice^2 + m^2) on n^3 grid.
    k_lattice^2 = sum_j 2*(1 - cos(2*pi*m_j/n))  (lattice Laplacian eigenvalue)
    """
    freqs = np.fft.fftfreq(n) * 2 * np.pi  # k values
    kx = freqs[:, None, None]
    ky = freqs[None, :, None]
    kz = freqs[None, None, :]
    # Lattice Laplacian eigenvalue: -2*(cos(k)-1) = 2*(1-cos(k)) per direction
    k2_lat = 2*(1 - np.cos(kx)) + 2*(1 - np.cos(ky)) + 2*(1 - np.cos(kz))
    E = np.sqrt(k2_lat + mass**2)
    return E


def build_potential(n, g, strength, mass_positions):
    """V(x) = g * sum_masses strength / (r + eps)."""
    V = np.zeros((n, n, n))
    c_arr = np.arange(n)
    for mp in mass_positions:
        dx = np.abs(c_arr[:, None, None] - mp[0])
        dx = np.minimum(dx, n - dx)
        dy = np.abs(c_arr[None, :, None] - mp[1])
        dy = np.minimum(dy, n - dy)
        dz = np.abs(c_arr[None, None, :] - mp[2])
        dz = np.minimum(dz, n - dz)
        r = np.sqrt(dx**2 + dy**2 + dz**2)
        V += g * strength / (r + 0.1)
    return V


def evolve_kg(n, mass, dt, n_steps, g=0.0, strength=0.0, mpos=None, psi0=None):
    """Evolve scalar KG field via Strang split-step.

    Half kinetic → full potential → half kinetic (per step).
    """
    E = build_dispersion(n, mass)
    V = build_potential(n, g, strength, mpos) if mpos and abs(g) > 0 else np.zeros((n, n, n))

    # Phase operators
    half_kin = np.exp(-1j * E * dt / 2)  # (n,n,n) in k-space
    full_pot = np.exp(-1j * V * dt)       # (n,n,n) in x-space

    if psi0 is None:
        # Gaussian wavepacket at center
        psi = np.zeros((n, n, n), dtype=complex)
        c = n // 2
        sigma = max(2.0, n / 8)
        x = np.arange(n)
        gx = np.exp(-(x - c)**2 / (2 * sigma**2))
        psi = gx[:, None, None] * gx[None, :, None] * gx[None, None, :]
        psi = psi.astype(complex)
        psi /= np.sqrt(np.sum(np.abs(psi)**2))
    else:
        psi = psi0.copy()

    for _ in range(n_steps):
        # Half kinetic (k-space)
        psi_k = np.fft.fftn(psi)
        psi_k *= half_kin
        psi = np.fft.ifftn(psi_k)
        # Full potential (x-space)
        psi *= full_pot
        # Half kinetic (k-space)
        psi_k = np.fft.fftn(psi)
        psi_k *= half_kin
        psi = np.fft.ifftn(psi_k)

    return psi


def prob(psi):
    return np.abs(psi)**2


def centroid_z(rho, n):
    """Compute center of mass in z-direction."""
    c = n // 2
    z = np.arange(n) - c
    p_z = np.sum(rho, axis=(0, 1))  # marginal in z
    total = np.sum(p_z)
    return np.sum(z * p_z) / total if total > 0 else 0.0


# ============================================================================
# TEST 1: Gravity Direction + N-Stability
# ============================================================================

def test_gravity_n_stability():
    print("=" * 70)
    print("TEST 1: Gravity Direction + N-Stability")
    print("=" * 70)

    n = 21; mass = 0.3; g = 5.0; S = 5e-4; c = n//2; dt = 0.3

    print(f"  n={n}, mass={mass}, g={g}, S={S}, dt={dt}")
    n_tw = 0; n_tot = 0
    forces = []

    for n_steps in range(1, 21):
        T = n_steps * dt
        psi_flat = evolve_kg(n, mass, dt, n_steps, 0.0, 0.0)
        psi_grav = evolve_kg(n, mass, dt, n_steps, g, S, [(c, c, c+3)])

        rho_f = prob(psi_flat); rho_g = prob(psi_grav)
        # Centroid shift in z
        cz_f = centroid_z(rho_f, n)
        cz_g = centroid_z(rho_g, n)
        delta_cz = cz_g - cz_f  # positive = toward mass at c+3

        is_tw = delta_cz > 0
        if is_tw: n_tw += 1
        n_tot += 1
        forces.append(delta_cz)
        print(f"    T={T:5.2f} (steps={n_steps:2d}): delta_cz={delta_cz:+.6e} "
              f"{'TOWARD' if is_tw else 'AWAY'}")

    frac = n_tw / n_tot
    print(f"\n  TOWARD fraction: {n_tw}/{n_tot} = {frac:.2f}")

    # Check monotonic growth
    abs_f = [abs(f) for f in forces]
    monotonic = all(abs_f[i] <= abs_f[i+1]*1.05 for i in range(len(abs_f)-1))
    print(f"  Monotonic growth: {monotonic}")
    print(f"  {'PASS' if frac > 0.8 else 'PARTIAL' if frac > 0.5 else 'FAIL'}")

    return frac, forces


# ============================================================================
# TEST 2: Achromatic Gravity
# ============================================================================

def test_achromatic():
    print("\n" + "=" * 70)
    print("TEST 2: Achromatic Gravity (k-independence)")
    print("=" * 70)

    n = 21; mass = 0.3; g = 5.0; S = 5e-4; c = n//2; dt = 0.3; n_steps = 10

    forces = []
    for k_idx in range(n//2 + 1):
        k = 2 * np.pi * k_idx / n
        # Plane wave in z-direction with Gaussian envelope
        psi0 = np.zeros((n, n, n), dtype=complex)
        sigma = max(2.0, n / 8)
        x = np.arange(n)
        gx = np.exp(-(x - c)**2 / (2 * sigma**2))
        envelope = gx[:, None, None] * gx[None, :, None] * gx[None, None, :]
        for iz in range(n):
            psi0[:, :, iz] = envelope[:, :, iz] * np.exp(1j * k * iz)
        psi0 /= np.sqrt(np.sum(np.abs(psi0)**2))

        psi_f = evolve_kg(n, mass, dt, n_steps, 0.0, 0.0, psi0=psi0)
        psi_g = evolve_kg(n, mass, dt, n_steps, g, S, [(c,c,c+3)], psi0=psi0)

        cz_f = centroid_z(prob(psi_f), n)
        cz_g = centroid_z(prob(psi_g), n)
        delta = cz_g - cz_f
        forces.append(delta)
        tag = "TOWARD" if delta > 0 else "AWAY"
        print(f"  k={k:.4f} (idx={k_idx}): delta_cz={delta:+.6e} {tag}")

    fa = np.array(forces)
    all_tw = all(f > 0 for f in fa)
    all_aw = all(f < 0 for f in fa)
    same_sign = all_tw or all_aw
    mean_abs = np.mean(np.abs(fa))
    cv = np.std(fa) / mean_abs if mean_abs > 0 else float('inf')

    print(f"\n  Same sign: {same_sign} ({'all TOWARD' if all_tw else 'all AWAY' if all_aw else 'MIXED'})")
    print(f"  CV = {cv:.4f}")
    if same_sign and cv < 0.3:
        print("  -> ACHROMATIC PASS")
    elif same_sign:
        print(f"  -> PARTIALLY achromatic (same sign, CV={cv:.2f})")
    else:
        print("  -> CHROMATIC FAIL")

    return same_sign, cv


# ============================================================================
# TEST 3: Equivalence Principle
# ============================================================================

def test_equivalence():
    print("\n" + "=" * 70)
    print("TEST 3: Equivalence Principle (mass independence)")
    print("=" * 70)

    n = 21; g = 5.0; S = 5e-4; c = n//2; dt = 0.3; n_steps = 10

    forces = []
    masses = [0.1, 0.2, 0.3, 0.5, 0.8, 1.0]
    for mass in masses:
        psi_f = evolve_kg(n, mass, dt, n_steps, 0.0, 0.0)
        psi_g = evolve_kg(n, mass, dt, n_steps, g, S, [(c,c,c+3)])
        delta = centroid_z(prob(psi_g), n) - centroid_z(prob(psi_f), n)
        forces.append(delta)
        tag = "TOWARD" if delta > 0 else "AWAY"
        print(f"  mass={mass:.2f}: delta_cz={delta:+.6e} {tag}")

    fa = np.array(forces); ma = np.array(masses)
    valid = np.abs(fa) > 1e-30
    if np.sum(valid) >= 3:
        _, _, rv, _, _ = stats.linregress(ma[valid], fa[valid])
        r2 = rv**2
    else:
        r2 = 0.0

    print(f"\n  R^2(force vs mass) = {r2:.4f}")
    if r2 < 0.1:
        print("  -> EQUIVALENCE HOLDS")
    elif r2 < 0.5:
        print("  -> PARTIAL mass dependence")
    else:
        print("  -> EQUIVALENCE VIOLATED")

    return r2


# ============================================================================
# TEST 4: F proportional to M
# ============================================================================

def test_fpm():
    print("\n" + "=" * 70)
    print("TEST 4: F proportional to M")
    print("=" * 70)

    n = 21; mass = 0.3; g = 5.0; c = n//2; dt = 0.3; n_steps = 10

    strengths = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3]
    forces = []
    cz_flat = centroid_z(prob(evolve_kg(n, mass, dt, n_steps)), n)
    for S in strengths:
        psi_g = evolve_kg(n, mass, dt, n_steps, g, S, [(c,c,c+3)])
        delta = centroid_z(prob(psi_g), n) - cz_flat
        forces.append(delta)
        print(f"  S={S:.0e}: delta_cz={delta:+.6e}")

    fa = np.array(forces); sa = np.array(strengths)
    co = np.polyfit(sa, fa, 1); pred = np.polyval(co, sa)
    ss_r = np.sum((fa-pred)**2); ss_t = np.sum((fa-np.mean(fa))**2)
    r2 = 1 - ss_r/ss_t if ss_t > 0 else 0
    print(f"\n  F~M R^2 = {r2:.6f} {'PASS' if r2>0.9 else 'FAIL'}")
    return r2


# ============================================================================
# TEST 5: Distance Law
# ============================================================================

def test_distance():
    print("\n" + "=" * 70)
    print("TEST 5: Distance Law")
    print("=" * 70)

    n = 25; mass = 0.3; g = 5.0; S = 5e-4; c = n//2; dt = 0.3; n_steps = 10

    max_off = n // 4
    offs = list(range(2, max_off + 1))
    cz_flat = centroid_z(prob(evolve_kg(n, mass, dt, n_steps)), n)
    forces = []
    for dz in offs:
        psi_g = evolve_kg(n, mass, dt, n_steps, g, S, [(c,c,c+dz)])
        delta = centroid_z(prob(psi_g), n) - cz_flat
        forces.append(delta)
        tag = "TOWARD" if delta > 0 else "AWAY"
        print(f"  offset={dz}: delta_cz={delta:+.6e} {tag}")

    n_tw = sum(1 for f in forces if f > 0)
    print(f"\n  TOWARD: {n_tw}/{len(forces)}")

    fa = np.array(forces); oa = np.array(offs, dtype=float)
    tw = fa > 0
    if np.sum(tw) >= 3:
        lr = np.log(oa[tw]); lf = np.log(fa[tw])
        cf = np.polyfit(lr, lf, 1)
        pf = np.polyval(cf, lr)
        sr = np.sum((lf-pf)**2); st = np.sum((lf-np.mean(lf))**2)
        r2 = 1-sr/st if st > 0 else 0; alpha = cf[0]
        print(f"  Power law: alpha={alpha:.3f}, R^2={r2:.4f}")
    else:
        alpha, r2 = 0.0, 0.0

    return n_tw, len(forces), alpha


# ============================================================================
# TEST 6: Superposition
# ============================================================================

def test_superposition():
    print("\n" + "=" * 70)
    print("TEST 6: Two-Body Superposition")
    print("=" * 70)

    n = 21; mass = 0.3; g = 5.0; S = 5e-4; c = n//2; dt = 0.3; n_steps = 10

    rho_0 = prob(evolve_kg(n, mass, dt, n_steps))
    rho_A = prob(evolve_kg(n, mass, dt, n_steps, g, S, [(c,c,c+3)]))
    rho_B = prob(evolve_kg(n, mass, dt, n_steps, g, S, [(c,c,c-3)]))
    rho_AB = prob(evolve_kg(n, mass, dt, n_steps, g, S, [(c,c,c+3),(c,c,c-3)]))

    dA = rho_A - rho_0; dB = rho_B - rho_0; dAB = rho_AB - rho_0
    err = np.sum(np.abs(dAB - dA - dB)) / np.sum(np.abs(dAB)) if np.sum(np.abs(dAB)) > 0 else 0
    print(f"  |dAB - dA - dB| / |dAB| = {err*100:.4f}%")
    print(f"  {'PASS' if err<0.01 else 'MARGINAL' if err<0.05 else 'FAIL'}")
    return err


# ============================================================================
# TEST 7: Norm + Unitarity
# ============================================================================

def test_norm():
    print("\n" + "=" * 70)
    print("TEST 7: Norm Preservation")
    print("=" * 70)

    n = 15; mass = 0.3; g = 5.0; S = 5e-4; c = n//2; dt = 0.3

    psi = evolve_kg(n, mass, dt, 0)  # initial state
    norm0 = np.sum(np.abs(psi)**2)

    norms = []
    for n_steps in range(1, 21):
        psi_t = evolve_kg(n, mass, dt, n_steps, g, S, [(c,c,c+3)])
        norms.append(np.sum(np.abs(psi_t)**2))

    max_dev = max(abs(nm - norm0) for nm in norms)
    print(f"  Initial norm: {norm0:.10f}")
    print(f"  Max |norm(t) - norm(0)| over 20 steps: {max_dev:.2e}")
    print(f"  {'PASS' if max_dev < 1e-10 else 'FAIL'}")
    return max_dev


# ============================================================================
# KG Dispersion Verification
# ============================================================================

def test_kg_dispersion():
    print("\n" + "=" * 70)
    print("TEST 0: KG Dispersion Verification")
    print("=" * 70)

    n = 15; mass = 0.3
    E = build_dispersion(n, mass)
    freqs = np.fft.fftfreq(n) * 2 * np.pi

    # Check: E(0,0,0) should be m
    print(f"  E(0,0,0) = {E[0,0,0]:.6f} (expected {mass:.6f})")

    # Check: E(k,0,0) = sqrt(2*(1-cos(k)) + m^2) for small k ≈ sqrt(k^2 + m^2)
    print("  E(kx,0,0) vs sqrt(kx^2 + m^2):")
    for i in range(min(5, n//2)):
        kx = freqs[i]
        E_exact = E[i, 0, 0]
        E_kg = np.sqrt(kx**2 + mass**2)
        k_lat = 2*(1 - np.cos(kx))
        E_lat = np.sqrt(k_lat + mass**2)
        print(f"    kx={kx:+.4f}: E_lattice={E_exact:.6f}, E_KG(continuum)={E_kg:.6f}, "
              f"E_KG(lattice)={E_lat:.6f}")

    # R^2 test: E^2 vs k^2 for small k
    all_E2, all_k2 = [], []
    for ix in range(n):
        kx = freqs[ix]; kxc = kx
        for iy in range(n):
            ky = freqs[iy]; kyc = ky
            for iz in range(n):
                kz = freqs[iz]; kzc = kz
                k2 = kxc**2 + kyc**2 + kzc**2
                all_E2.append(E[ix,iy,iz]**2)
                all_k2.append(k2)
    all_E2 = np.array(all_E2); all_k2 = np.array(all_k2)
    mask = all_k2 < 1.0
    sl, ic, rv, _, _ = stats.linregress(all_k2[mask], all_E2[mask])
    r2 = rv**2
    print(f"\n  KG fit (E^2 vs k^2, small k): R^2={r2:.6f}, m_fit={np.sqrt(abs(ic)):.4f}, c^2={sl:.4f}")
    print(f"  {'PASS' if r2>0.99 else 'FAIL'}")
    return r2


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()
    print("=" * 70)
    print("SCALAR KLEIN-GORDON + POTENTIAL GRAVITY (NO COIN)")
    print("=" * 70)
    print("Architecture: 1 complex scalar per site, FFT split-step evolution")
    print("No internal states. No coin. No mixing period. No Zitterbewegung.")
    print()

    r2_kg = test_kg_dispersion()
    frac, forces = test_gravity_n_stability()
    same_sign, cv = test_achromatic()
    r2_eq = test_equivalence()
    r2_fm = test_fpm()
    n_tw, n_tot, alpha = test_distance()
    sup = test_superposition()
    norm_dev = test_norm()

    elapsed = time.time() - t_start
    print(f"\n{'='*70}")
    print("FINAL SCORECARD")
    print(f"{'='*70}")
    tests = [
        ("KG dispersion", f"R^2={r2_kg:.6f}", r2_kg > 0.99),
        ("N-stability", f"{frac:.0%} TOWARD", frac > 0.8),
        ("Achromatic", f"CV={cv:.4f}, same_sign={same_sign}", same_sign and cv < 0.3),
        ("Equivalence", f"R^2={r2_eq:.4f}", r2_eq < 0.1),
        ("F~M", f"R^2={r2_fm:.6f}", r2_fm > 0.9),
        ("Distance", f"{n_tw}/{n_tot} TOWARD, alpha={alpha:.2f}", n_tw > n_tot // 2),
        ("Superposition", f"{sup*100:.4f}%", sup < 0.01),
        ("Unitarity", f"dev={norm_dev:.2e}", norm_dev < 1e-10),
    ]
    passes = 0
    for name, result, passed in tests:
        status = "PASS" if passed else "FAIL"
        if passed: passes += 1
        print(f"  {name:<20s} {result:<35s} {status}")

    print(f"\n  SCORE: {passes}/{len(tests)}")
    print(f"  Total time: {elapsed:.1f}s")
