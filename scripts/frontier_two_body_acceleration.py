#!/usr/bin/env python3
"""
Frontier Two-Body Mutual Acceleration Test
===========================================
Hartree two-orbital approach on a 3D staggered lattice (n=9, N=729).

Observable: early-time mutual acceleration  a_mutual = a_SHARED - a_SELF_ONLY
  - Negative a_mutual at t=1..5 → mutual gravitational attraction
  - Should scale with G, decrease with distance, increase with partner mass

Four evolution modes: SHARED, SELF_ONLY, FREE, FROZEN
Sweeps over: G, mu², separation, mass ratio
"""

import numpy as np
from scipy.sparse import lil_matrix, csc_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from time import perf_counter

# ── lattice parameters ──────────────────────────────────────────────
N_SIDE = 9
N = N_SIDE ** 3
MASS = 0.30
DT = 0.08
N_STEPS = 20

# ── coordinate arrays ───────────────────────────────────────────────
coords = np.zeros((N, 3), dtype=int)
for x in range(N_SIDE):
    for y in range(N_SIDE):
        for z in range(N_SIDE):
            i = x * N_SIDE**2 + y * N_SIDE + z
            coords[i] = (x, y, z)

x_coord = coords[:, 0].astype(float)
y_coord = coords[:, 1].astype(float)
z_coord = coords[:, 2].astype(float)
parity = np.array([(-1) ** (coords[i, 0] + coords[i, 1] + coords[i, 2]) for i in range(N)], dtype=float)


def index_of(x, y, z):
    return (x % N_SIDE) * N_SIDE**2 + (y % N_SIDE) * N_SIDE + (z % N_SIDE)


# ── adjacency list (periodic 3D cubic) ──────────────────────────────
adj = [[] for _ in range(N)]
for x in range(N_SIDE):
    for y in range(N_SIDE):
        for z in range(N_SIDE):
            i = index_of(x, y, z)
            for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                j = index_of(x+dx, y+dy, z+dz)
                if j not in adj[i]:
                    adj[i].append(j)


# ── build graph Laplacian (periodic 3D) ─────────────────────────────
def build_laplacian():
    L = lil_matrix((N, N), dtype=float)
    for i in range(N):
        for j in adj[i]:
            if j > i:
                L[i, j] -= 1
                L[j, i] -= 1
                L[i, i] += 1
                L[j, j] += 1
    return csc_matrix(L)

LAP = build_laplacian()


# ── build 3D staggered Hamiltonian ──────────────────────────────────
def build_H_3d(phi):
    """Build staggered Hamiltonian with potential phi on 3D periodic lattice."""
    H = lil_matrix((N, N), dtype=complex)
    for x in range(N_SIDE):
        for y in range(N_SIDE):
            for z in range(N_SIDE):
                i = index_of(x, y, z)
                eps = (-1) ** (x + y + z)
                H[i, i] = (MASS + phi[i]) * eps

                # x-hop: eta_1 = 1
                j = index_of(x+1, y, z)
                H[i, j] += -0.5j
                H[j, i] +=  0.5j

                # y-hop: eta_2 = (-1)^x
                j = index_of(x, y+1, z)
                eta2 = (-1) ** x
                H[i, j] += eta2 * (-0.5j)
                H[j, i] += eta2 * ( 0.5j)

                # z-hop: eta_3 = (-1)^(x+y)
                j = index_of(x, y, z+1)
                eta3 = (-1) ** (x + y)
                H[i, j] += eta3 * (-0.5j)
                H[j, i] += eta3 * ( 0.5j)

    return csc_matrix(H)


# ── Crank-Nicolson step ─────────────────────────────────────────────
def cn_step(H, psi, dt):
    """One Crank-Nicolson half-step: (I + i dt/2 H)^{-1} (I - i dt/2 H) psi."""
    I = speye(N, format='csc')
    A = I + 0.5j * dt * H
    B = I - 0.5j * dt * H
    rhs = B @ psi
    return spsolve(A, rhs)


# ── Gaussian wavepacket ─────────────────────────────────────────────
def gaussian_packet(cx, cy, cz, sigma, mass_weight=1.0):
    """
    Gaussian wavepacket centered at (cx,cy,cz).
    mass_weight controls the "mass" (integral of |psi|^2).
    A packet with mass_weight=2 has twice the density → twice the gravitational source.
    """
    psi = np.zeros(N, dtype=complex)
    for i in range(N):
        dx = coords[i, 0] - cx
        dy = coords[i, 1] - cy
        dz = coords[i, 2] - cz
        # Minimum image for periodic
        dx = dx - N_SIDE * round(dx / N_SIDE)
        dy = dy - N_SIDE * round(dy / N_SIDE)
        dz = dz - N_SIDE * round(dz / N_SIDE)
        r2 = dx**2 + dy**2 + dz**2
        psi[i] = np.exp(-r2 / (2 * sigma**2))
    # Normalize to unit norm first, then scale by sqrt(mass_weight)
    # so that |psi|^2 integrates to mass_weight
    norm = np.sqrt(np.sum(np.abs(psi)**2))
    if norm > 0:
        psi *= np.sqrt(mass_weight) / norm
    return psi


# ── centroid ─────────────────────────────────────────────────────────
def centroid_x(psi):
    """Centroid in x using circular mean to handle periodicity."""
    prob = np.abs(psi)**2
    prob /= prob.sum()
    theta = 2 * np.pi * x_coord / N_SIDE
    cx_cos = np.sum(prob * np.cos(theta))
    cx_sin = np.sum(prob * np.sin(theta))
    angle = np.arctan2(cx_sin, cx_cos)
    if angle < 0:
        angle += 2 * np.pi
    return angle * N_SIDE / (2 * np.pi)


# ── solve Poisson with regularization ───────────────────────────────
def solve_poisson(rho, G_val, mu2, reg=1e-3):
    """Solve (L + mu2*I + reg*I) phi = G * rho."""
    M = LAP + (mu2 + reg) * speye(N, format='csc')
    return spsolve(M, G_val * rho)


# ── run one configuration ───────────────────────────────────────────
def run_mode(mode, psi_A0, psi_B0, G_val, mu2, n_steps=N_STEPS):
    """
    Evolve two orbitals and return separation timeseries.
    mode: 'shared', 'self_only', 'free', 'frozen'
    """
    psi_A = psi_A0.copy()
    psi_B = psi_B0.copy()
    seps = np.zeros(n_steps + 1)
    cx_A_arr = np.zeros(n_steps + 1)
    cx_B_arr = np.zeros(n_steps + 1)

    cx_A_arr[0] = centroid_x(psi_A)
    cx_B_arr[0] = centroid_x(psi_B)
    seps[0] = cx_B_arr[0] - cx_A_arr[0]

    if mode == 'frozen':
        rho_total = np.abs(psi_A)**2 + np.abs(psi_B)**2
        phi_frozen = solve_poisson(rho_total, G_val, mu2)
        H_frozen = build_H_3d(phi_frozen)

    if mode == 'free':
        H_free = build_H_3d(np.zeros(N))

    for step in range(n_steps):
        if mode == 'shared':
            rho_total = np.abs(psi_A)**2 + np.abs(psi_B)**2
            phi = solve_poisson(rho_total, G_val, mu2)
            H = build_H_3d(phi)
            psi_A = cn_step(H, psi_A, DT)
            psi_B = cn_step(H, psi_B, DT)

        elif mode == 'self_only':
            rho_A = np.abs(psi_A)**2
            rho_B = np.abs(psi_B)**2
            phi_A = solve_poisson(rho_A, G_val, mu2)
            phi_B = solve_poisson(rho_B, G_val, mu2)
            H_A = build_H_3d(phi_A)
            H_B = build_H_3d(phi_B)
            psi_A = cn_step(H_A, psi_A, DT)
            psi_B = cn_step(H_B, psi_B, DT)

        elif mode == 'free':
            psi_A = cn_step(H_free, psi_A, DT)
            psi_B = cn_step(H_free, psi_B, DT)

        elif mode == 'frozen':
            psi_A = cn_step(H_frozen, psi_A, DT)
            psi_B = cn_step(H_frozen, psi_B, DT)

        cx_A_arr[step + 1] = centroid_x(psi_A)
        cx_B_arr[step + 1] = centroid_x(psi_B)
        seps[step + 1] = cx_B_arr[step + 1] - cx_A_arr[step + 1]

    return seps, cx_A_arr, cx_B_arr


# ── acceleration from separation timeseries ─────────────────────────
def compute_acceleration(seps):
    """Central-difference second derivative: a[t] = (s[t+1] - 2s[t] + s[t-1]) / dt^2."""
    n = len(seps)
    acc = np.zeros(n)
    for t in range(1, n - 1):
        acc[t] = (seps[t+1] - 2*seps[t] + seps[t-1]) / DT**2
    return acc


def compute_velocity(seps):
    """Central-difference first derivative."""
    n = len(seps)
    vel = np.zeros(n)
    for t in range(1, n - 1):
        vel[t] = (seps[t+1] - seps[t-1]) / (2 * DT)
    return vel


def smoothed_acceleration(seps, deg=3):
    """
    Fit a polynomial to sep(t) and return its second derivative at each t.
    This filters out the lattice oscillations and extracts the secular trend.
    """
    n = len(seps)
    t_arr = np.arange(n) * DT
    # Fit polynomial of given degree
    coeffs = np.polyfit(t_arr, seps, deg)
    # Second derivative of polynomial
    p = np.polyder(np.poly1d(coeffs), 2)
    return p(t_arr)


# ── main sweeps ──────────────────────────────────────────────────────
def main():
    print("=" * 80)
    print("FRONTIER TWO-BODY MUTUAL ACCELERATION TEST")
    print("3D staggered lattice, n=9, N=729, Hartree two-orbital")
    print("=" * 80)

    sigma = 1.0
    center_y, center_z = 4, 4

    # ── Sweep 1: G coupling strength ────────────────────────────────
    print("\n" + "=" * 80)
    print("SWEEP 1: G coupling strength  (sep=4, mu2=0.01)")
    print("=" * 80)

    G_values = [5, 10, 20, 50, 100]
    mu2_default = 0.01
    cx_A_default, cx_B_default = 2, 6

    psi_A0 = gaussian_packet(cx_A_default, center_y, center_z, sigma)
    psi_B0 = gaussian_packet(cx_B_default, center_y, center_z, sigma)
    sep0 = centroid_x(psi_B0) - centroid_x(psi_A0)
    print(f"Initial separation: {sep0:.4f}")

    for G_val in G_values:
        t0 = perf_counter()
        seps_shared, _, _ = run_mode('shared', psi_A0, psi_B0, G_val, mu2_default)
        seps_self,   _, _ = run_mode('self_only', psi_A0, psi_B0, G_val, mu2_default)
        seps_free,   _, _ = run_mode('free', psi_A0, psi_B0, G_val, mu2_default)
        seps_frozen, _, _ = run_mode('frozen', psi_A0, psi_B0, G_val, mu2_default)
        elapsed = perf_counter() - t0

        acc_shared = compute_acceleration(seps_shared)
        acc_self   = compute_acceleration(seps_self)
        acc_free   = compute_acceleration(seps_free)
        acc_frozen = compute_acceleration(seps_frozen)
        acc_mutual = acc_shared - acc_self

        # Smoothed (polynomial fit) acceleration
        sa_shared = smoothed_acceleration(seps_shared, deg=4)
        sa_self   = smoothed_acceleration(seps_self, deg=4)
        sa_free   = smoothed_acceleration(seps_free, deg=4)
        sa_mutual = sa_shared - sa_self

        print(f"\n  G = {G_val:>3d}  ({elapsed:.1f}s)")
        print(f"  Raw accelerations:")
        print(f"  {'t':>3s}  {'a_shared':>12s}  {'a_self':>12s}  {'a_mutual':>12s}  {'a_free':>12s}  {'a_frozen':>12s}")
        for t in range(1, 8):
            print(f"  {t:>3d}  {acc_shared[t]:>12.6f}  {acc_self[t]:>12.6f}  {acc_mutual[t]:>12.6f}  "
                  f"{acc_free[t]:>12.6f}  {acc_frozen[t]:>12.6f}")

        mean_mutual_early = np.mean(acc_mutual[1:6])
        print(f"  Mean raw a_mutual[1:5] = {mean_mutual_early:.8f}  ({'ATTRACTIVE' if mean_mutual_early < 0 else 'NOT attractive'})")

        print(f"  Smoothed (poly-fit) accelerations:")
        print(f"  {'t':>3s}  {'sa_shared':>12s}  {'sa_self':>12s}  {'sa_mutual':>12s}  {'sa_free':>12s}")
        for t in range(0, 8):
            print(f"  {t:>3d}  {sa_shared[t]:>12.6f}  {sa_self[t]:>12.6f}  {sa_mutual[t]:>12.6f}  "
                  f"{sa_free[t]:>12.6f}")
        sa_mean = np.mean(sa_mutual[:6])
        print(f"  Mean smoothed a_mutual[0:5] = {sa_mean:.8f}  ({'ATTRACTIVE' if sa_mean < 0 else 'NOT attractive'})")

        # Also report total separation change
        dsep = seps_shared[-1] - seps_shared[0]
        dsep_self = seps_self[-1] - seps_self[0]
        dsep_free = seps_free[-1] - seps_free[0]
        print(f"  Total delta_sep: shared={dsep:.6f}  self={dsep_self:.6f}  free={dsep_free:.6f}  diff={dsep-dsep_self:.6f}")

    # ── Sweep 2: mu² screening mass ─────────────────────────────────
    print("\n" + "=" * 80)
    print("SWEEP 2: mu² screening  (G=50, sep=4)")
    print("=" * 80)

    mu2_values = [0.0, 0.01, 0.05, 0.22, 1.0]
    G_fixed = 50

    for mu2 in mu2_values:
        t0 = perf_counter()
        seps_shared, _, _ = run_mode('shared', psi_A0, psi_B0, G_fixed, mu2)
        seps_self,   _, _ = run_mode('self_only', psi_A0, psi_B0, G_fixed, mu2)
        elapsed = perf_counter() - t0

        acc_shared = compute_acceleration(seps_shared)
        acc_self   = compute_acceleration(seps_self)
        acc_mutual = acc_shared - acc_self
        sa_shared = smoothed_acceleration(seps_shared, deg=4)
        sa_self   = smoothed_acceleration(seps_self, deg=4)
        sa_mutual = sa_shared - sa_self

        mean_mutual = np.mean(acc_mutual[1:6])
        sa_mean = np.mean(sa_mutual[:6])
        dsep = seps_shared[-1] - seps_shared[0]
        dsep_self = seps_self[-1] - seps_self[0]
        print(f"  mu2 = {mu2:.2f}:  raw a_mutual={mean_mutual:.8f}  smooth a_mutual={sa_mean:.8f}  "
              f"delta_sep={dsep:.6f}/{dsep_self:.6f}  ({elapsed:.1f}s)")

    # ── Sweep 3: separation distance ─────────────────────────────────
    print("\n" + "=" * 80)
    print("SWEEP 3: separation distance  (G=50, mu2=0.01)")
    print("=" * 80)

    separations = [3, 4, 5, 6]
    for d in separations:
        cx_A = (N_SIDE - d) // 2
        cx_B = cx_A + d
        psi_A = gaussian_packet(cx_A, center_y, center_z, sigma)
        psi_B = gaussian_packet(cx_B, center_y, center_z, sigma)
        sep0 = centroid_x(psi_B) - centroid_x(psi_A)

        t0 = perf_counter()
        seps_shared, _, _ = run_mode('shared', psi_A, psi_B, G_fixed, mu2_default)
        seps_self,   _, _ = run_mode('self_only', psi_A, psi_B, G_fixed, mu2_default)
        elapsed = perf_counter() - t0

        acc_shared = compute_acceleration(seps_shared)
        acc_self   = compute_acceleration(seps_self)
        acc_mutual = acc_shared - acc_self
        sa_shared = smoothed_acceleration(seps_shared, deg=4)
        sa_self   = smoothed_acceleration(seps_self, deg=4)
        sa_mutual = sa_shared - sa_self

        mean_mutual = np.mean(acc_mutual[1:6])
        sa_mean = np.mean(sa_mutual[:6])
        dsep = seps_shared[-1] - seps_shared[0]
        dsep_self = seps_self[-1] - seps_self[0]
        print(f"  d = {d} (actual sep = {sep0:.3f}):  raw={mean_mutual:.8f}  smooth={sa_mean:.8f}  "
              f"dsep={dsep:.6f}/{dsep_self:.6f}  ({elapsed:.1f}s)")

    # ── Sweep 4: mass ratio ──────────────────────────────────────────
    print("\n" + "=" * 80)
    print("SWEEP 4: mass ratio  (G=50, mu2=0.01, sep=4)")
    print("=" * 80)

    mass_weights_B = [1.0, 1.5, 2.0, 3.0]
    for mw in mass_weights_B:
        psi_A = gaussian_packet(cx_A_default, center_y, center_z, sigma, mass_weight=1.0)
        psi_B = gaussian_packet(cx_B_default, center_y, center_z, sigma, mass_weight=mw)

        t0 = perf_counter()
        seps_shared, cxA_s, cxB_s = run_mode('shared', psi_A, psi_B, G_fixed, mu2_default)
        seps_self,   cxA_o, cxB_o = run_mode('self_only', psi_A, psi_B, G_fixed, mu2_default)
        elapsed = perf_counter() - t0

        acc_shared = compute_acceleration(seps_shared)
        acc_self   = compute_acceleration(seps_self)
        acc_mutual = acc_shared - acc_self

        # Also compute individual centroid accelerations
        acc_A_shared = compute_acceleration(cxA_s)
        acc_A_self   = compute_acceleration(cxA_o)
        acc_B_shared = compute_acceleration(cxB_s)
        acc_B_self   = compute_acceleration(cxB_o)
        acc_A_mutual = acc_A_shared - acc_A_self
        acc_B_mutual = acc_B_shared - acc_B_self

        sa_shared_sep = smoothed_acceleration(seps_shared, deg=4)
        sa_self_sep   = smoothed_acceleration(seps_self, deg=4)
        sa_mutual_sep = sa_shared_sep - sa_self_sep

        mean_mutual = np.mean(acc_mutual[1:6])
        sa_mean = np.mean(sa_mutual_sep[:6])
        mean_A_mutual = np.mean(acc_A_mutual[1:6])
        mean_B_mutual = np.mean(acc_B_mutual[1:6])

        mass_A = np.sum(np.abs(psi_A)**2)
        mass_B = np.sum(np.abs(psi_B)**2)
        dsep = seps_shared[-1] - seps_shared[0]
        dsep_self = seps_self[-1] - seps_self[0]
        print(f"  mass_B = {mw:.1f} (|psi_A|^2={mass_A:.3f}, |psi_B|^2={mass_B:.3f}):")
        print(f"    raw a_mutual={mean_mutual:.8f}  smooth={sa_mean:.8f}  dsep={dsep:.6f}/{dsep_self:.6f}")
        print(f"    A accel: {mean_A_mutual:.8f}   B accel: {mean_B_mutual:.8f}  ({elapsed:.1f}s)")

    # ── Summary ──────────────────────────────────────────────────────
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("Look for:")
    print("  1. a_mutual < 0 at early times → mutual attraction")
    print("  2. |a_mutual| grows with G → gravitational scaling")
    print("  3. |a_mutual| decreases with separation → distance law")
    print("  4. Heavier B → larger acceleration of A → mass coupling")
    print("  5. a_free ≈ 0 → no spurious drift")
    print("  6. Higher mu2 → weaker mutual attraction (screening)")


if __name__ == '__main__':
    main()
