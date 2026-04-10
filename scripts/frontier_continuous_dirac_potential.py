#!/usr/bin/env python3
"""
Continuous-Time Dirac Walk with Scalar Potential Gravity
=========================================================
Eliminates the split-step parity artifact by using Hamiltonian evolution:
  U(dt) = exp(-i * H * dt)
where H = H_Dirac + V(x) is the full Dirac Hamiltonian plus scalar potential.

H_Dirac = m*gamma0 + sum_j (-i*gamma0*gamma_j * nabla_j)
V(x)    = g * strength / (|x - x_mass| + eps)

On the lattice, nabla_j is the centered finite difference:
  (nabla_j psi)(x) = (psi(x+e_j) - psi(x-e_j)) / 2

The full Hamiltonian is a sparse 4n^3 x 4n^3 matrix. We evolve via
expm(-i*H*dt) applied to the state vector. For small n this is exact;
for large n we use Krylov subspace methods (scipy expm_multiply).

KEY PREDICTIONS:
  1. No odd/even N parity → N-stability should improve dramatically
  2. Scalar potential → equivalence principle maintained
  3. Continuous dispersion → less lattice chromaticity
  4. dt controls the Courant number (stability vs resolution)

HYPOTHESIS: Continuous-time + scalar potential gives >80% TOWARD across
  N range, achromatic gravity, and mass-independent force.
"""

import numpy as np
from scipy import stats
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import expm_multiply
import time

# ============================================================================
# Gamma matrices
# ============================================================================
gamma0 = np.diag([1,1,-1,-1]).astype(complex)
gamma1 = np.array([[0,0,0,1],[0,0,1,0],[0,-1,0,0],[-1,0,0,0]], dtype=complex)
gamma2 = np.array([[0,0,0,-1j],[0,0,1j,0],[0,1j,0,0],[-1j,0,0,0]], dtype=complex)
gamma3 = np.array([[0,0,1,0],[0,0,0,-1],[-1,0,0,0],[0,1,0,0]], dtype=complex)

g0g = [gamma0 @ gamma1, gamma0 @ gamma2, gamma0 @ gamma3]


# ============================================================================
# Build Hamiltonian
# ============================================================================

def idx(ix, iy, iz, comp, n):
    """Flatten (ix, iy, iz, comp) -> linear index in 4n^3 vector."""
    return ((ix * n + iy) * n + iz) * 4 + comp


def min_img_scalar(n, mp, ix, iy, iz):
    """Minimum-image distance from site (ix,iy,iz) to mass position mp."""
    dx = min(abs(ix - mp[0]), n - abs(ix - mp[0]))
    dy = min(abs(iy - mp[1]), n - abs(iy - mp[1]))
    dz = min(abs(iz - mp[2]), n - abs(iz - mp[2]))
    return np.sqrt(dx**2 + dy**2 + dz**2)


def build_hamiltonian(n, mass0, g=0.0, strength=0.0, mass_positions=None):
    """Build the full Dirac Hamiltonian as a sparse matrix.

    H = mass0 * gamma0 (on-site)
      + sum_j (-i * g0g_j) * (centered difference in direction j)
      + V(x) * I_4 (scalar potential)

    Centered difference: (psi(x+e_j) - psi(x-e_j)) / 2
    """
    dim = 4 * n**3
    H = lil_matrix((dim, dim), dtype=complex)

    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                site = (ix, iy, iz)

                # On-site: mass term + potential
                V = 0.0
                if mass_positions and g > 0 and strength > 0:
                    for mp in mass_positions:
                        r = min_img_scalar(n, mp, ix, iy, iz)
                        V += g * strength / (r + 0.1)

                for a in range(4):
                    for b in range(4):
                        val = mass0 * gamma0[a, b]
                        if a == b:
                            val += V  # scalar potential on diagonal
                        if abs(val) > 1e-15:
                            H[idx(ix,iy,iz,a,n), idx(ix,iy,iz,b,n)] += val

                # Derivative terms: -i * g0g_j * centered_diff_j
                neighbors = [
                    (0, ((ix+1)%n, iy, iz), ((ix-1)%n, iy, iz)),  # x-direction
                    (1, (ix, (iy+1)%n, iz), (ix, (iy-1)%n, iz)),  # y-direction
                    (2, (ix, iy, (iz+1)%n), (ix, iy, (iz-1)%n)),  # z-direction
                ]

                for j, fwd, bwd in neighbors:
                    G = g0g[j]  # gamma0 * gamma_j
                    for a in range(4):
                        for b in range(4):
                            if abs(G[a, b]) < 1e-15:
                                continue
                            # -i * G[a,b] * (psi_b(fwd) - psi_b(bwd)) / 2
                            coeff = -1j * G[a, b] / 2.0
                            H[idx(ix,iy,iz,a,n), idx(fwd[0],fwd[1],fwd[2],b,n)] += coeff
                            H[idx(ix,iy,iz,a,n), idx(bwd[0],bwd[1],bwd[2],b,n)] -= coeff

    return csr_matrix(H)


# ============================================================================
# Evolution
# ============================================================================

def make_initial_state(n):
    """Balanced source at center."""
    dim = 4 * n**3
    psi = np.zeros(dim, dtype=complex)
    c = n // 2
    amp = 0.5
    for comp in range(4):
        psi[idx(c, c, c, comp, n)] = amp
    return psi


def evolve_continuous(n, dt, n_steps, mass0, g=0.0, strength=0.0, mpos=None):
    """Evolve via exp(-i*H*dt) for n_steps."""
    H = build_hamiltonian(n, mass0, g, strength, mpos)
    psi = make_initial_state(n)
    # Use expm_multiply for efficiency: exp(-i*H*dt)*psi
    for _ in range(n_steps):
        psi = expm_multiply(-1j * H * dt, psi)
    return psi


def prob_from_flat(psi, n):
    """Extract probability density from flat state vector."""
    psi_4d = psi.reshape(n, n, n, 4)
    return np.sum(np.abs(psi_4d)**2, axis=3)


# ============================================================================
# Tests
# ============================================================================

def test_gravity_and_n_stability():
    print("=" * 70)
    print("TEST 1: Gravity Direction + N-Stability (continuous time)")
    print("=" * 70)

    n = 11  # smaller for speed with full Hamiltonian
    m0 = 0.3; g = 5.0; S = 5e-4; c = n//2
    dt = 0.5  # time step

    print(f"  n={n}, mass={m0}, g={g}, S={S}, dt={dt}")
    print(f"  Building Hamiltonian ({4*n**3} dim)...")

    t0 = time.time()
    H_flat = build_hamiltonian(n, m0)
    H_grav = build_hamiltonian(n, m0, g, S, [(c,c,c+2)])
    t_build = time.time() - t0
    print(f"  Built in {t_build:.1f}s")

    # Check Hermiticity
    diff = H_flat - H_flat.conj().T
    herm_err = np.max(np.abs(diff.toarray())) if hasattr(diff, 'toarray') else 0
    print(f"  Hermiticity error: {herm_err:.2e}")

    psi0 = make_initial_state(n)
    n_tw = 0; n_tot = 0
    forces = []

    print(f"\n  N-step sweep (dt={dt}):")
    for n_steps in range(1, 16):
        T = n_steps * dt
        psi_flat = expm_multiply(-1j * H_flat * T, psi0)
        psi_grav = expm_multiply(-1j * H_grav * T, psi0)

        rho_flat = prob_from_flat(psi_flat, n)
        rho_grav = prob_from_flat(psi_grav, n)
        d = rho_grav - rho_flat

        tw = sum(d[c, c, c+dz] for dz in range(1, 3))
        aw = sum(d[c, c, c-dz] for dz in range(1, 3))
        is_tw = tw > aw
        if is_tw: n_tw += 1
        n_tot += 1
        force = tw - aw
        forces.append(force)
        print(f"    T={T:5.1f} (steps={n_steps:2d}): tw={tw:+.4e}, aw={aw:+.4e} "
              f"{'TOWARD' if is_tw else 'AWAY'} |F|={abs(force):.4e}")

    frac = n_tw / n_tot
    print(f"\n  TOWARD fraction: {n_tw}/{n_tot} = {frac:.2f}")

    # Check monotonic force growth
    abs_f = [abs(f) for f in forces]
    growing = sum(1 for i in range(len(abs_f)-1) if abs_f[i+1] > abs_f[i] * 0.5)
    print(f"  Force growing: {growing}/{len(abs_f)-1}")
    print(f"  {'PASS' if frac > 0.8 else 'PARTIAL' if frac > 0.5 else 'FAIL'}")

    return frac, forces


def test_equivalence():
    print("\n" + "=" * 70)
    print("TEST 2: Equivalence Principle (mass independence)")
    print("=" * 70)

    n = 11; g = 5.0; S = 5e-4; c = n//2; dt = 0.5; n_steps = 8
    T = n_steps * dt

    forces = []
    masses = [0.1, 0.2, 0.3, 0.5, 0.8]
    for m0 in masses:
        H_flat = build_hamiltonian(n, m0)
        H_grav = build_hamiltonian(n, m0, g, S, [(c,c,c+2)])
        psi0 = make_initial_state(n)
        psi_f = expm_multiply(-1j * H_flat * T, psi0)
        psi_g = expm_multiply(-1j * H_grav * T, psi0)
        rho_f = prob_from_flat(psi_f, n)
        rho_g = prob_from_flat(psi_g, n)
        d = rho_g - rho_f
        f = sum(d[c,c,c+dz] for dz in range(1,3))
        forces.append(f)
        tag = "TOWARD" if f > 0 else "AWAY"
        print(f"  m0={m0:.2f}: force={f:+.4e} {tag}")

    fa = np.array(forces); ma = np.array(masses)
    valid = np.abs(fa) > 1e-30
    if np.sum(valid) >= 3:
        _, _, rv, _, _ = stats.linregress(ma[valid], fa[valid])
        r2 = rv**2
    else:
        r2 = 0.0

    print(f"\n  R^2(force vs mass) = {r2:.4f}")
    print(f"  {'PASS' if r2 < 0.1 else 'PARTIAL' if r2 < 0.5 else 'FAIL'}")
    return r2


def test_achromatic():
    print("\n" + "=" * 70)
    print("TEST 3: Achromatic Gravity (k-independence)")
    print("=" * 70)

    n = 11; m0 = 0.3; g = 5.0; S = 5e-4; c = n//2; dt = 0.5; n_steps = 8
    T = n_steps * dt

    H_flat = build_hamiltonian(n, m0)
    H_grav = build_hamiltonian(n, m0, g, S, [(c,c,c+2)])

    forces = []
    for k_idx in range(n//2 + 1):
        k = 2 * np.pi * k_idx / n
        # Plane wave in z-direction
        dim = 4 * n**3
        psi0 = np.zeros(dim, dtype=complex)
        amp = 0.5 / np.sqrt(n)
        for iz in range(n):
            phase = np.exp(1j * k * iz)
            for comp in range(4):
                psi0[idx(c, c, iz, comp, n)] = amp * phase

        psi_f = expm_multiply(-1j * H_flat * T, psi0)
        psi_g = expm_multiply(-1j * H_grav * T, psi0)
        rho_f = prob_from_flat(psi_f, n)
        rho_g = prob_from_flat(psi_g, n)
        d = rho_g - rho_f
        f = sum(d[c,c,c+dz] for dz in range(1,3))
        forces.append(f)
        tag = "TOWARD" if f > 0 else "AWAY"
        print(f"  k={k:.4f} (idx={k_idx}): force={f:+.4e} {tag}")

    fa = np.array(forces)
    all_toward = all(f > 0 for f in fa)
    all_away = all(f < 0 for f in fa)
    same_sign = all_toward or all_away
    mean_abs = np.mean(np.abs(fa))
    cv = np.std(fa) / mean_abs if mean_abs > 0 else float('inf')

    print(f"\n  Same sign: {same_sign}")
    print(f"  CV = {cv:.4f}")
    if same_sign and cv < 0.3:
        print("  -> ACHROMATIC PASS")
    elif same_sign:
        print(f"  -> PARTIALLY achromatic (same sign, CV={cv:.2f})")
    else:
        print("  -> CHROMATIC FAIL")
    return same_sign, cv


def test_fpm():
    print("\n" + "=" * 70)
    print("TEST 4: F proportional to M")
    print("=" * 70)

    n = 11; m0 = 0.3; g = 5.0; c = n//2; dt = 0.5; n_steps = 8
    T = n_steps * dt

    H_flat = build_hamiltonian(n, m0)
    psi0 = make_initial_state(n)
    psi_flat = expm_multiply(-1j * H_flat * T, psi0)
    rho_flat = prob_from_flat(psi_flat, n)

    strengths = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3]
    forces = []
    for S in strengths:
        H_g = build_hamiltonian(n, m0, g, S, [(c,c,c+2)])
        psi_g = expm_multiply(-1j * H_g * T, psi0)
        rho_g = prob_from_flat(psi_g, n)
        d = rho_g - rho_flat
        f = sum(d[c,c,c+dz] for dz in range(1,3))
        forces.append(f)
        print(f"  S={S:.0e}: force={f:+.4e}")

    fa = np.array(forces); sa = np.array(strengths)
    co = np.polyfit(sa, fa, 1); pred = np.polyval(co, sa)
    ss_r = np.sum((fa-pred)**2); ss_t = np.sum((fa-np.mean(fa))**2)
    r2 = 1 - ss_r/ss_t if ss_t > 0 else 0
    print(f"\n  F~M R^2 = {r2:.6f} {'PASS' if r2>0.9 else 'FAIL'}")
    return r2


def test_norm():
    print("\n" + "=" * 70)
    print("TEST 5: Norm Preservation (unitarity)")
    print("=" * 70)

    n = 9; m0 = 0.3; g = 5.0; S = 5e-4; c = n//2; dt = 0.5
    H = build_hamiltonian(n, m0, g, S, [(c,c,c+2)])
    psi = make_initial_state(n)

    norms = []
    for step in range(20):
        T = (step + 1) * dt
        psi_t = expm_multiply(-1j * H * T, make_initial_state(n))
        norm = np.sum(np.abs(psi_t)**2)
        norms.append(norm)

    max_dev = max(abs(nm - 1.0) for nm in norms)
    print(f"  Max |norm - 1| over 20 steps: {max_dev:.2e}")
    print(f"  {'PASS' if max_dev < 1e-8 else 'FAIL'}")
    return max_dev


def test_distance():
    print("\n" + "=" * 70)
    print("TEST 6: Distance Law")
    print("=" * 70)

    n = 13; m0 = 0.3; g = 5.0; S = 5e-4; c = n//2; dt = 0.5; n_steps = 8
    T = n_steps * dt

    H_flat = build_hamiltonian(n, m0)
    psi0 = make_initial_state(n)
    psi_flat = expm_multiply(-1j * H_flat * T, psi0)
    rho_flat = prob_from_flat(psi_flat, n)

    max_off = n // 4
    offs = list(range(2, max_off + 1))
    forces = []
    for dz in offs:
        H_g = build_hamiltonian(n, m0, g, S, [(c,c,c+dz)])
        psi_g = expm_multiply(-1j * H_g * T, psi0)
        rho_g = prob_from_flat(psi_g, n)
        d = rho_g - rho_flat
        f = sum(d[c,c,c+dd] for dd in range(1, dz+1))
        forces.append(f)
        tag = "TOWARD" if f > 0 else "AWAY"
        print(f"  offset={dz}: force={f:+.4e} {tag}")

    n_tw = sum(1 for f in forces if f > 0)
    print(f"\n  TOWARD: {n_tw}/{len(forces)}")
    return n_tw, len(forces)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()
    print("=" * 70)
    print("CONTINUOUS-TIME DIRAC WALK + SCALAR POTENTIAL GRAVITY")
    print("=" * 70)
    print("Eliminates split-step parity artifact via Hamiltonian evolution.")
    print("H = m*gamma0 + sum_j (-i*g0g_j*nabla_j) + V(x)*I_4")
    print("Evolution: exp(-i*H*T) via scipy expm_multiply.")
    print()

    frac, forces = test_gravity_and_n_stability()
    r2_eq = test_equivalence()
    same_sign, cv = test_achromatic()
    r2_fm = test_fpm()
    norm_dev = test_norm()
    n_tw, n_tot = test_distance()

    elapsed = time.time() - t_start
    print(f"\n{'='*70}")
    print("SUMMARY — CONTINUOUS-TIME DIRAC + SCALAR POTENTIAL")
    print(f"{'='*70}")
    print(f"  N-stability:   {frac:.0%} TOWARD {'PASS' if frac>0.8 else 'PARTIAL' if frac>0.5 else 'FAIL'}")
    print(f"  Equivalence:   R^2={r2_eq:.4f} {'PASS' if r2_eq<0.1 else 'PARTIAL' if r2_eq<0.5 else 'FAIL'}")
    print(f"  Achromatic:    same_sign={same_sign}, CV={cv:.4f} {'PASS' if same_sign and cv<0.3 else 'PARTIAL' if same_sign else 'FAIL'}")
    print(f"  F~M:           R^2={r2_fm:.6f} {'PASS' if r2_fm>0.9 else 'FAIL'}")
    print(f"  Unitarity:     max_dev={norm_dev:.2e} {'PASS' if norm_dev<1e-8 else 'FAIL'}")
    print(f"  Distance:      {n_tw}/{n_tot} TOWARD")
    print(f"  Total time: {elapsed:.1f}s")

    passes = sum([
        frac > 0.8,
        r2_eq < 0.1,
        same_sign and cv < 0.3,
        r2_fm > 0.9,
        norm_dev < 1e-8,
        n_tw > n_tot // 2
    ])
    print(f"\n  SCORE: {passes}/6 bottleneck tests")
