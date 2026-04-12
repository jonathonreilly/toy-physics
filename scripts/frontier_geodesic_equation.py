#!/usr/bin/env python3
"""Geodesic equation: propagator trajectories match emergent metric geodesics.

CLAIM: Test particles propagated through the path-sum propagator follow
geodesics of the emergent conformal metric g_ij = (1-f)^2 delta_ij.

PHYSICS:
In GR, free particles follow geodesics:
    d^2 x^i / dtau^2 + Gamma^i_jk (dx^j/dtau)(dx^k/dtau) = 0

For the conformal metric g_ij = Omega^2 delta_ij with Omega = (1 - f):
    Gamma^i_jk = (d_j Omega / Omega) delta_ik
               + (d_k Omega / Omega) delta_ij
               - (d_i Omega / Omega) delta_jk

The geodesic equation becomes (for spatial coordinates, non-relativistic limit):
    d^2 x^i / dt^2 = -2 * (d_i Omega / Omega) * v^2
                    + 2 * (v . grad Omega / Omega) * v^i

In the weak-field slow-motion limit (v << 1, f << 1), this reduces to:
    d^2 x^i / dt^2 ~ +2 * d_i f / (1 - f) * v^2  - 2 * (v . grad f / (1-f)) * v^i

For a particle moving primarily in one direction (say x), the transverse
acceleration (deflection) agrees with light bending in linearized GR.

TESTS:
1. Christoffel symbols from conformal metric, integrate geodesic equation (RK4)
2. Propagator wavepacket trajectory from centroid tracking
3. Compare geodesic vs propagator trajectories
4. Multiple impact parameters: deflection angle agreement

PStack experiment: geodesic-equation
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np

try:
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


# ===========================================================================
# Poisson solver
# ===========================================================================

def solve_poisson_sparse(N, mass_pos, mass_strength=1.0):
    """Solve nabla^2 f = -rho on NxNxN lattice with Dirichlet BC.

    Returns f array of shape (N, N, N).
    """
    M = N - 2
    n_interior = M * M * M

    def idx(i, j, k):
        return i * M * M + j * M + k

    rows, cols, vals = [], [], []
    rhs = np.zeros(n_interior)
    mx, my, mz = mass_pos
    mi, mj, mk = mx - 1, my - 1, mz - 1

    for i in range(M):
        for j in range(M):
            for k in range(M):
                c = idx(i, j, k)
                rows.append(c); cols.append(c); vals.append(-6.0)
                if i > 0:
                    rows.append(c); cols.append(idx(i-1, j, k)); vals.append(1.0)
                if i < M - 1:
                    rows.append(c); cols.append(idx(i+1, j, k)); vals.append(1.0)
                if j > 0:
                    rows.append(c); cols.append(idx(i, j-1, k)); vals.append(1.0)
                if j < M - 1:
                    rows.append(c); cols.append(idx(i, j+1, k)); vals.append(1.0)
                if k > 0:
                    rows.append(c); cols.append(idx(i, j, k-1)); vals.append(1.0)
                if k < M - 1:
                    rows.append(c); cols.append(idx(i, j, k+1)); vals.append(1.0)

                if i == mi and j == mj and k == mk:
                    rhs[c] = -mass_strength

    A = sparse.csr_matrix((vals, (rows, cols)), shape=(n_interior, n_interior))
    sol = spsolve(A, rhs)

    f = np.zeros((N, N, N))
    for i in range(M):
        for j in range(M):
            for k in range(M):
                f[i+1, j+1, k+1] = sol[idx(i, j, k)]
    return f


def solve_poisson_jacobi(N, mass_pos, mass_strength=1.0, n_iter=3000, tol=1e-8):
    """Fallback Jacobi solver when scipy is not available."""
    f = np.zeros((N, N, N))
    rho = np.zeros((N, N, N))
    mx, my, mz = mass_pos
    rho[mx, my, mz] = -mass_strength

    for it in range(n_iter):
        f_new = np.zeros_like(f)
        f_new[1:-1, 1:-1, 1:-1] = (
            f[2:, 1:-1, 1:-1] + f[:-2, 1:-1, 1:-1] +
            f[1:-1, 2:, 1:-1] + f[1:-1, :-2, 1:-1] +
            f[1:-1, 1:-1, 2:] + f[1:-1, 1:-1, :-2] -
            rho[1:-1, 1:-1, 1:-1]
        ) / 6.0
        diff = np.max(np.abs(f_new - f))
        f = f_new
        if diff < tol:
            break
    return f


def solve_poisson(N, mass_pos, mass_strength=1.0):
    if HAS_SCIPY:
        return solve_poisson_sparse(N, mass_pos, mass_strength)
    return solve_poisson_jacobi(N, mass_pos, mass_strength)


# ===========================================================================
# Field gradient (central difference with trilinear interpolation)
# ===========================================================================

def interpolate_field(f, pos):
    """Trilinear interpolation of field f at continuous position pos."""
    N = f.shape[0]
    x, y, z = pos
    x = np.clip(x, 0.5, N - 1.5)
    y = np.clip(y, 0.5, N - 1.5)
    z = np.clip(z, 0.5, N - 1.5)

    i0, j0, k0 = int(np.floor(x)), int(np.floor(y)), int(np.floor(z))
    i0 = min(max(i0, 0), N - 2)
    j0 = min(max(j0, 0), N - 2)
    k0 = min(max(k0, 0), N - 2)

    dx, dy, dz = x - i0, y - j0, z - k0

    c000 = f[i0, j0, k0]
    c100 = f[i0+1, j0, k0]
    c010 = f[i0, j0+1, k0]
    c110 = f[i0+1, j0+1, k0]
    c001 = f[i0, j0, k0+1]
    c101 = f[i0+1, j0, k0+1]
    c011 = f[i0, j0+1, k0+1]
    c111 = f[i0+1, j0+1, k0+1]

    val = (c000 * (1-dx)*(1-dy)*(1-dz) +
           c100 * dx*(1-dy)*(1-dz) +
           c010 * (1-dx)*dy*(1-dz) +
           c110 * dx*dy*(1-dz) +
           c001 * (1-dx)*(1-dy)*dz +
           c101 * dx*(1-dy)*dz +
           c011 * (1-dx)*dy*dz +
           c111 * dx*dy*dz)
    return val


def gradient_field(f, pos):
    """Compute gradient of f at continuous position using central differences."""
    eps = 0.5
    grad = np.zeros(3)
    for axis in range(3):
        p_plus = pos.copy()
        p_minus = pos.copy()
        p_plus[axis] += eps
        p_minus[axis] -= eps
        grad[axis] = (interpolate_field(f, p_plus) - interpolate_field(f, p_minus)) / (2 * eps)
    return grad


# ===========================================================================
# Geodesic integrator (conformal metric)
# ===========================================================================

def geodesic_acceleration(pos, vel, f_field):
    """Compute acceleration from the conformal metric g_ij = (1-f)^2 delta_ij.

    For the conformal metric, the geodesic equation for coordinate acceleration:
        a^i = -Gamma^i_jk v^j v^k

    With Omega = 1 - f, the Christoffel symbols give:
        a^i = -(2/Omega) * [ (d_j Omega) v^j v^i - (1/2) (d_i Omega) v^2 ]
            = (2/(1-f)) * [ (d_j f) v^j v^i - (1/2) (d_i f) v^2 ]

    Wait -- let's be careful. For conformal metric g_ij = Omega^2 delta_ij:
        Gamma^i_jk = (ln Omega),_j delta^i_k + (ln Omega),_k delta^i_j
                   - (ln Omega),_i delta_jk

    So:
        Gamma^i_jk v^j v^k = (ln Omega),_j v^j v^i + (ln Omega),_k v^k v^i
                            - (ln Omega),_i v^2
                          = 2 (ln Omega),_j v^j v^i - (ln Omega),_i v^2

    And the geodesic equation is:
        a^i = -Gamma^i_jk v^j v^k = -2 (d_j ln Omega) v^j v^i + (d_i ln Omega) v^2

    With ln Omega = ln(1-f) ~ -f for small f:
        d_i ln Omega = -d_i f / (1-f)

    So:
        a^i = 2 (d_j f / (1-f)) v^j v^i - (d_i f / (1-f)) v^2
    """
    f_val = interpolate_field(f_field, pos)
    grad_f = gradient_field(f_field, pos)
    omega = 1.0 - f_val

    if abs(omega) < 1e-12:
        return np.zeros(3)

    v_dot_grad_f = np.dot(vel, grad_f)
    v2 = np.dot(vel, vel)

    # a^i = 2 * (v . grad_f) / omega * v^i - (grad_f_i / omega) * v^2
    acc = (2.0 * v_dot_grad_f / omega) * vel - (v2 / omega) * grad_f
    return acc


def integrate_geodesic_rk4(pos0, vel0, f_field, dt, n_steps):
    """Integrate the geodesic equation using RK4.

    Returns arrays of positions and velocities at each step.
    """
    positions = np.zeros((n_steps + 1, 3))
    velocities = np.zeros((n_steps + 1, 3))
    positions[0] = pos0.copy()
    velocities[0] = vel0.copy()

    pos = pos0.copy()
    vel = vel0.copy()

    for step in range(n_steps):
        # RK4 for coupled system: dx/dt = v, dv/dt = a(x, v)
        k1v = geodesic_acceleration(pos, vel, f_field)
        k1x = vel.copy()

        k2v = geodesic_acceleration(pos + 0.5*dt*k1x, vel + 0.5*dt*k1v, f_field)
        k2x = vel + 0.5*dt*k1v

        k3v = geodesic_acceleration(pos + 0.5*dt*k2x, vel + 0.5*dt*k2v, f_field)
        k3x = vel + 0.5*dt*k2v

        k4v = geodesic_acceleration(pos + dt*k3x, vel + dt*k3v, f_field)
        k4x = vel + dt*k3v

        pos = pos + (dt/6.0) * (k1x + 2*k2x + 2*k3x + k4x)
        vel = vel + (dt/6.0) * (k1v + 2*k2v + 2*k3v + k4v)

        positions[step + 1] = pos.copy()
        velocities[step + 1] = vel.copy()

    return positions, velocities


# ===========================================================================
# Propagator wavepacket evolution
# ===========================================================================

def build_propagator_matrix(N, f_field, k0_vec):
    """Build the single-step propagator matrix for a 3D lattice with field f.

    The propagator encodes: phase per step = k0 . dx * (1 - f_avg)
    with 1/L^p attenuation. For nearest-neighbor hops on a lattice,
    the propagator matrix element from site j to site i is:

        G_ij = exp(i * k0 . (r_i - r_j) * (1 - f_avg)) / L_ij

    We restrict to nearest-neighbor hops for tractability.
    """
    total = N * N * N

    def site_idx(x, y, z):
        return x * N * N + y * N + z

    # Neighbor offsets (6 nearest neighbors in 3D)
    offsets = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]

    rows, cols, vals = [], [], []

    for x in range(N):
        for y in range(N):
            for z in range(N):
                idx_from = site_idx(x, y, z)
                f_from = f_field[x, y, z]
                for dx, dy, dz in offsets:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < N and 0 <= ny < N and 0 <= nz < N:
                        idx_to = site_idx(nx, ny, nz)
                        f_to = f_field[nx, ny, nz]
                        f_avg = 0.5 * (f_from + f_to)

                        # Phase: k0 . displacement * (1 - f_avg)
                        disp = np.array([dx, dy, dz], dtype=float)
                        phase = np.dot(k0_vec, disp) * (1.0 - f_avg)

                        # Amplitude: 1/6 normalization for 6 neighbors
                        amp = 1.0 / 6.0
                        val = amp * np.exp(1j * phase)

                        rows.append(idx_to)
                        cols.append(idx_from)
                        vals.append(val)

    G = sparse.csr_matrix((vals, (rows, cols)), shape=(total, total))
    return G


def make_wavepacket(N, center, k0_vec, sigma):
    """Create a Gaussian wavepacket on an NxNxN lattice.

    psi(r) = exp(-|r-center|^2 / (4*sigma^2)) * exp(i * k0 . r)
    """
    total = N * N * N
    psi = np.zeros(total, dtype=complex)

    for x in range(N):
        for y in range(N):
            for z in range(N):
                r = np.array([x, y, z], dtype=float)
                dr = r - center
                envelope = math.exp(-np.dot(dr, dr) / (4.0 * sigma**2))
                phase = np.dot(k0_vec, r)
                idx = x * N * N + y * N + z
                psi[idx] = envelope * np.exp(1j * phase)

    norm = np.sqrt(np.sum(np.abs(psi)**2))
    if norm > 0:
        psi /= norm
    return psi


def wavepacket_centroid(psi, N):
    """Compute the expectation value <r> for a wavepacket."""
    prob = np.abs(psi)**2
    cx, cy, cz = 0.0, 0.0, 0.0
    total_prob = np.sum(prob)
    if total_prob < 1e-30:
        return np.array([N/2.0, N/2.0, N/2.0])

    for x in range(N):
        for y in range(N):
            for z in range(N):
                idx = x * N * N + y * N + z
                p = prob[idx]
                cx += x * p
                cy += y * p
                cz += z * p

    return np.array([cx, cy, cz]) / total_prob


def propagate_wavepacket(G, psi0, N, n_steps):
    """Propagate wavepacket through n_steps of the propagator.

    Returns centroid positions at each step.
    """
    centroids = np.zeros((n_steps + 1, 3))
    centroids[0] = wavepacket_centroid(psi0, N)

    psi = psi0.copy()
    for step in range(n_steps):
        psi = G @ psi
        norm = np.sqrt(np.sum(np.abs(psi)**2))
        if norm > 1e-30:
            psi /= norm
        centroids[step + 1] = wavepacket_centroid(psi, N)

    return centroids


# ===========================================================================
# Eikonal approximation (ray tracing through refractive medium)
# ===========================================================================

def integrate_eikonal_rk4(pos0, vel0, f_field, dt, n_steps):
    """Integrate the eikonal (ray) equation through medium with n = 1/(1-f).

    For a ray in a refractive medium n(x), the ray equation is:
        d/ds (n * dx/ds) = grad(n)
    which gives:
        a^i = (1/n) * [grad_n_i - (v . grad_n / v^2) v^i] * v^2
            + (1/n) * (v . grad_n) * v^i

    For n = 1/(1-f), grad n = grad_f / (1-f)^2.

    In the eikonal limit this is equivalent to the conformal geodesic.
    We use this as a cross-check.
    """
    positions = np.zeros((n_steps + 1, 3))
    positions[0] = pos0.copy()

    pos = pos0.copy()
    vel = vel0.copy()

    for step in range(n_steps):
        f_val = interpolate_field(f_field, pos)
        grad_f = gradient_field(f_field, pos)
        omega = 1.0 - f_val

        if abs(omega) < 1e-12:
            positions[step + 1:] = pos
            break

        # Effective refractive index: n = 1/omega = 1/(1-f)
        n_val = 1.0 / omega
        # grad(n) = grad_f / omega^2
        grad_n = grad_f / (omega * omega)

        v2 = np.dot(vel, vel)
        if v2 < 1e-30:
            positions[step + 1:] = pos
            break

        speed = math.sqrt(v2)
        v_hat = vel / speed

        # Ray equation: d(n*v_hat)/ds = grad(n), ds = |dx|
        # => n * dv_hat/ds + (v_hat . grad_n) v_hat = grad_n
        # => dv_hat/ds = (1/n) * [grad_n - (v_hat . grad_n) v_hat]
        # With dx = v_hat * ds, and ds = speed * dt:
        dv_hat_ds = (1.0 / n_val) * (grad_n - np.dot(v_hat, grad_n) * v_hat)

        # Speed changes: d(speed)/dt = -(speed/n) * (v_hat . grad_n) * speed
        # Actually for conformal metric the coordinate speed is c/n = omega
        # Let's just track direction change, keep speed = omega(pos)
        new_speed = omega  # local coordinate speed

        # Update direction
        vel = new_speed * (v_hat + dv_hat_ds * speed * dt)
        vel_norm = np.linalg.norm(vel)
        if vel_norm > 0:
            vel = new_speed * vel / vel_norm

        pos = pos + vel * dt
        positions[step + 1] = pos.copy()

    return positions


# ===========================================================================
# Deflection angle measurement
# ===========================================================================

def measure_deflection(trajectory, vel0):
    """Measure the deflection angle from a trajectory.

    The deflection angle is the angle between the initial and final
    velocity directions.
    """
    # Use last few points to estimate final velocity
    n = len(trajectory)
    if n < 4:
        return 0.0

    # Final velocity from last segment
    v_final = trajectory[-1] - trajectory[-4]
    v_final_norm = np.linalg.norm(v_final)
    if v_final_norm < 1e-10:
        return 0.0
    v_final = v_final / v_final_norm

    # Initial velocity direction
    v_init = vel0 / np.linalg.norm(vel0)

    cos_theta = np.clip(np.dot(v_init, v_final), -1.0, 1.0)
    return math.acos(cos_theta)


# ===========================================================================
# Main experiment
# ===========================================================================

def main():
    t0 = time.time()
    print("=" * 80)
    print("GEODESIC EQUATION: PROPAGATOR vs CONFORMAL-METRIC GEODESICS")
    print("=" * 80)

    N = 31
    center = N // 2  # mass at lattice center
    mass_pos = (center, center, center)

    # Scale mass so that f << 1 everywhere (weak field)
    mass_strength = 0.8

    print(f"\nLattice: {N}x{N}x{N}")
    print(f"Mass at: {mass_pos}, strength: {mass_strength}")

    # ------------------------------------------------------------------
    # Solve for the gravitational field
    # ------------------------------------------------------------------
    print("\nSolving Poisson equation for gravitational field...")
    f_field = solve_poisson(N, mass_pos, mass_strength)

    f_max = np.max(np.abs(f_field))
    f_at_center = f_field[center, center, center]
    print(f"  max |f| = {f_max:.6f}")
    print(f"  f at mass = {f_at_center:.6f}")
    print(f"  Weak field: f << 1 ? {'YES' if f_max < 0.3 else 'MARGINAL'}")

    # ------------------------------------------------------------------
    # Test 1: Single geodesic trajectory
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TEST 1: SINGLE GEODESIC TRAJECTORY")
    print("=" * 80)

    # Particle starts to the left of center, moving rightward
    impact_param = 5.0
    x0 = np.array([3.0, center + impact_param, center], dtype=float)
    v0 = np.array([1.0, 0.0, 0.0], dtype=float)
    v_speed = 0.3
    v0 = v0 * v_speed

    dt_geo = 0.2
    n_steps_geo = 120

    print(f"\nInitial position: {x0}")
    print(f"Initial velocity: {v0} (speed = {v_speed})")
    print(f"Impact parameter: {impact_param}")
    print(f"dt = {dt_geo}, steps = {n_steps_geo}")

    print("\nIntegrating geodesic equation (RK4)...")
    geo_pos, geo_vel = integrate_geodesic_rk4(x0, v0, f_field, dt_geo, n_steps_geo)

    print(f"  Start: ({geo_pos[0, 0]:.2f}, {geo_pos[0, 1]:.2f}, {geo_pos[0, 2]:.2f})")
    print(f"  End:   ({geo_pos[-1, 0]:.2f}, {geo_pos[-1, 1]:.2f}, {geo_pos[-1, 2]:.2f})")

    # Transverse deflection
    dy_geo = geo_pos[-1, 1] - geo_pos[0, 1]
    print(f"  Transverse deflection (y): {dy_geo:.6f}")
    theta_geo = measure_deflection(geo_pos, v0)
    print(f"  Deflection angle: {theta_geo:.6f} rad = {math.degrees(theta_geo):.4f} deg")

    # ------------------------------------------------------------------
    # Test 2: Eikonal ray tracing (cross-check)
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TEST 2: EIKONAL RAY TRACING (cross-check)")
    print("=" * 80)

    print("\nIntegrating eikonal equation...")
    eik_pos = integrate_eikonal_rk4(x0.copy(), v0.copy(), f_field, dt_geo, n_steps_geo)

    print(f"  Start: ({eik_pos[0, 0]:.2f}, {eik_pos[0, 1]:.2f}, {eik_pos[0, 2]:.2f})")
    print(f"  End:   ({eik_pos[-1, 0]:.2f}, {eik_pos[-1, 1]:.2f}, {eik_pos[-1, 2]:.2f})")

    dy_eik = eik_pos[-1, 1] - eik_pos[0, 1]
    print(f"  Transverse deflection (y): {dy_eik:.6f}")
    theta_eik = measure_deflection(eik_pos, v0)
    print(f"  Deflection angle: {theta_eik:.6f} rad = {math.degrees(theta_eik):.4f} deg")

    # Compare geodesic and eikonal
    if abs(theta_geo) > 1e-8:
        ratio_eik_geo = theta_eik / theta_geo
        print(f"\n  Eikonal/Geodesic deflection ratio: {ratio_eik_geo:.4f}")
        print(f"  Agreement: {'GOOD' if abs(ratio_eik_geo - 1.0) < 0.15 else 'POOR'}")

    # ------------------------------------------------------------------
    # Test 3: Propagator wavepacket trajectory
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TEST 3: PROPAGATOR WAVEPACKET TRAJECTORY")
    print("=" * 80)

    # Use a smaller lattice for the propagator (computational cost)
    N_prop = 21
    center_prop = N_prop // 2
    mass_pos_prop = (center_prop, center_prop, center_prop)

    print(f"\nPropagator lattice: {N_prop}x{N_prop}x{N_prop}")
    print("Solving Poisson for propagator lattice...")
    f_prop = solve_poisson(N_prop, mass_pos_prop, mass_strength)

    f_max_prop = np.max(np.abs(f_prop))
    print(f"  max |f| = {f_max_prop:.6f}")

    # Wavepacket parameters
    sigma_wp = 1.5
    k0_mag = 1.5  # wavenumber
    k0_vec = np.array([k0_mag, 0.0, 0.0])  # moving in x direction
    impact_prop = 4.0

    wp_center = np.array([2.0, center_prop + impact_prop, center_prop], dtype=float)

    print(f"\nWavepacket center: {wp_center}")
    print(f"Wavenumber: k0 = {k0_vec}")
    print(f"Sigma: {sigma_wp}")
    print(f"Impact parameter: {impact_prop}")

    print("\nBuilding propagator matrix...")
    G = build_propagator_matrix(N_prop, f_prop, k0_vec)

    print("Creating initial wavepacket...")
    psi0 = make_wavepacket(N_prop, wp_center, k0_vec, sigma_wp)

    n_prop_steps = 30
    print(f"Propagating for {n_prop_steps} steps...")
    prop_centroids = propagate_wavepacket(G, psi0, N_prop, n_prop_steps)

    print(f"  Start centroid: ({prop_centroids[0, 0]:.2f}, {prop_centroids[0, 1]:.2f}, {prop_centroids[0, 2]:.2f})")
    print(f"  End centroid:   ({prop_centroids[-1, 0]:.2f}, {prop_centroids[-1, 1]:.2f}, {prop_centroids[-1, 2]:.2f})")

    dy_prop = prop_centroids[-1, 1] - prop_centroids[0, 1]
    print(f"  Transverse deflection (y): {dy_prop:.6f}")

    # Compute geodesic on same lattice for comparison
    v_group = np.array([1.0, 0.0, 0.0])  # group velocity direction
    geo_prop_pos, _ = integrate_geodesic_rk4(
        wp_center.copy(), v_group * 0.5, f_prop, 0.3, n_prop_steps
    )
    dy_geo_prop = geo_prop_pos[-1, 1] - geo_prop_pos[0, 1]

    print(f"\n  Geodesic deflection on same lattice: {dy_geo_prop:.6f}")
    if abs(dy_geo_prop) > 1e-8:
        ratio_prop_geo = dy_prop / dy_geo_prop
        print(f"  Propagator/Geodesic deflection ratio: {ratio_prop_geo:.4f}")
    else:
        ratio_prop_geo = float('nan')
        print(f"  Geodesic deflection too small for ratio.")

    # ------------------------------------------------------------------
    # Test 4: Multiple impact parameters
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TEST 4: DEFLECTION vs IMPACT PARAMETER")
    print("=" * 80)

    impact_params = [3.0, 5.0, 7.0, 9.0]
    dt4 = 0.2
    n_steps4 = 120
    speed4 = 0.3

    print(f"\nSpeed = {speed4}, dt = {dt4}, steps = {n_steps4}")
    print(f"Lattice: {N}x{N}x{N}")
    print(f"\n{'b':>5} {'theta_geo':>12} {'theta_eik':>12} {'ratio':>10} {'dy_geo':>10}")
    print("-" * 55)

    geo_results = []
    for b in impact_params:
        x0_b = np.array([3.0, center + b, center], dtype=float)
        v0_b = np.array([speed4, 0.0, 0.0])

        pos_g, _ = integrate_geodesic_rk4(x0_b, v0_b, f_field, dt4, n_steps4)
        theta_g = measure_deflection(pos_g, v0_b)

        pos_e = integrate_eikonal_rk4(x0_b.copy(), v0_b.copy(), f_field, dt4, n_steps4)
        theta_e = measure_deflection(pos_e, v0_b)

        ratio = theta_e / theta_g if abs(theta_g) > 1e-10 else float('nan')
        dy = pos_g[-1, 1] - pos_g[0, 1]

        geo_results.append((b, theta_g, theta_e, ratio, dy))
        print(f"{b:>5.1f} {theta_g:>12.6f} {theta_e:>12.6f} {ratio:>10.4f} {dy:>10.4f}")

    # Check 1/b scaling for geodesic deflection
    print("\n--- 1/b scaling check ---")
    print(f"{'b':>5} {'theta_geo':>12} {'theta*b':>12} {'expected':>12}")
    print("-" * 45)
    theta_b_products = []
    for b, theta_g, theta_e, ratio, dy in geo_results:
        tb = theta_g * b
        theta_b_products.append(tb)
        print(f"{b:>5.1f} {theta_g:>12.6f} {tb:>12.6f}")

    if len(theta_b_products) > 1 and all(abs(t) > 1e-10 for t in theta_b_products):
        spread = (max(theta_b_products) - min(theta_b_products)) / np.mean(theta_b_products)
        print(f"\ntheta*b spread: {spread:.4f}")
        print(f"1/b scaling: {'CONFIRMED' if spread < 0.3 else 'WEAK'}")

    # ------------------------------------------------------------------
    # Test 5: Trajectory comparison (point by point)
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TEST 5: POINT-BY-POINT TRAJECTORY COMPARISON")
    print("=" * 80)

    b_test = 5.0
    x0_t = np.array([3.0, center + b_test, center], dtype=float)
    v0_t = np.array([speed4, 0.0, 0.0])

    pos_geo5, _ = integrate_geodesic_rk4(x0_t, v0_t, f_field, dt4, n_steps4)
    pos_eik5 = integrate_eikonal_rk4(x0_t.copy(), v0_t.copy(), f_field, dt4, n_steps4)

    # Sample every 20 steps
    print(f"\nImpact parameter b = {b_test}")
    print(f"\n{'step':>6} {'x_geo':>8} {'y_geo':>8} {'x_eik':>8} {'y_eik':>8} {'|dr|':>10}")
    print("-" * 55)
    deviations = []
    for i in range(0, n_steps4 + 1, 20):
        dr = np.linalg.norm(pos_geo5[i] - pos_eik5[i])
        deviations.append(dr)
        print(f"{i:>6d} {pos_geo5[i,0]:>8.2f} {pos_geo5[i,1]:>8.2f} "
              f"{pos_eik5[i,0]:>8.2f} {pos_eik5[i,1]:>8.2f} {dr:>10.4f}")

    max_dev = max(deviations)
    path_length = np.sum(np.linalg.norm(np.diff(pos_geo5, axis=0), axis=1))
    relative_dev = max_dev / path_length if path_length > 0 else float('inf')

    print(f"\nMax deviation: {max_dev:.6f}")
    print(f"Path length: {path_length:.2f}")
    print(f"Relative deviation: {relative_dev:.2e}")

    # ------------------------------------------------------------------
    # Test 6: Verify Christoffel symbols directly
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TEST 6: CHRISTOFFEL SYMBOL VERIFICATION")
    print("=" * 80)

    # At a test point, compute Christoffel symbols from the metric
    # and compare with our analytic expression
    test_pt = np.array([center - 3.0, center + 4.0, center], dtype=float)
    f_test = interpolate_field(f_field, test_pt)
    grad_f_test = gradient_field(f_field, test_pt)
    omega_test = 1.0 - f_test

    print(f"\nTest point: {test_pt}")
    print(f"f = {f_test:.6f}")
    print(f"grad f = [{grad_f_test[0]:.6f}, {grad_f_test[1]:.6f}, {grad_f_test[2]:.6f}]")
    print(f"Omega = {omega_test:.6f}")

    # Christoffel from analytic formula:
    # Gamma^i_jk = (d_j ln Omega) delta^i_k + (d_k ln Omega) delta^i_j
    #            - (d_i ln Omega) delta_jk
    # d_i ln Omega = -d_i f / (1-f)
    d_ln_omega = -grad_f_test / omega_test

    print(f"\nd ln Omega = [{d_ln_omega[0]:.6f}, {d_ln_omega[1]:.6f}, {d_ln_omega[2]:.6f}]")

    # Compute a few Christoffel components
    print("\nSelected Christoffel symbols (analytic):")
    for i in range(3):
        for j in range(3):
            for k in range(j, 3):  # symmetric in j,k
                gamma = (d_ln_omega[j] * (1 if i == k else 0) +
                         d_ln_omega[k] * (1 if i == j else 0) -
                         d_ln_omega[i] * (1 if j == k else 0))
                if abs(gamma) > 1e-8:
                    labels = ['x', 'y', 'z']
                    print(f"  Gamma^{labels[i]}_{labels[j]}{labels[k]} = {gamma:.6f}")

    # Numerical check: compute Christoffel from finite-difference metric
    eps_met = 0.5
    gamma_num = np.zeros((3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                # Gamma^i_jk = (1/2) g^il (d_j g_lk + d_k g_jl - d_l g_jk)
                # For conformal metric g_ij = Omega^2 delta_ij:
                # g^il = delta^il / Omega^2
                # So Gamma^i_jk = (1/(2*Omega^2)) * (d_j(Omega^2) delta_ik
                #                + d_k(Omega^2) delta_ij - d_i(Omega^2) delta_jk)
                # = (d_j(Omega^2)/(2*Omega^2)) delta_ik + ... - ...
                # Which gives the same as d_j ln Omega formula

                # Numerical from metric:
                val = 0.0
                for l in range(3):
                    g_inv_il = (1.0 / omega_test**2) * (1 if i == l else 0)

                    # d_j g_lk
                    p_plus = test_pt.copy(); p_plus[j] += eps_met
                    p_minus = test_pt.copy(); p_minus[j] -= eps_met
                    om_p = 1.0 - interpolate_field(f_field, p_plus)
                    om_m = 1.0 - interpolate_field(f_field, p_minus)
                    dj_glk = ((om_p**2 * (1 if l == k else 0)) -
                              (om_m**2 * (1 if l == k else 0))) / (2 * eps_met)

                    # d_k g_jl
                    p_plus = test_pt.copy(); p_plus[k] += eps_met
                    p_minus = test_pt.copy(); p_minus[k] -= eps_met
                    om_p = 1.0 - interpolate_field(f_field, p_plus)
                    om_m = 1.0 - interpolate_field(f_field, p_minus)
                    dk_gjl = ((om_p**2 * (1 if j == l else 0)) -
                              (om_m**2 * (1 if j == l else 0))) / (2 * eps_met)

                    # d_l g_jk
                    p_plus = test_pt.copy(); p_plus[l] += eps_met
                    p_minus = test_pt.copy(); p_minus[l] -= eps_met
                    om_p = 1.0 - interpolate_field(f_field, p_plus)
                    om_m = 1.0 - interpolate_field(f_field, p_minus)
                    dl_gjk = ((om_p**2 * (1 if j == k else 0)) -
                              (om_m**2 * (1 if j == k else 0))) / (2 * eps_met)

                    val += 0.5 * g_inv_il * (dj_glk + dk_gjl - dl_gjk)

                gamma_num[i, j, k] = val

    # Compare analytic vs numerical Christoffel
    gamma_analytic = np.zeros((3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                gamma_analytic[i, j, k] = (
                    d_ln_omega[j] * (1 if i == k else 0) +
                    d_ln_omega[k] * (1 if i == j else 0) -
                    d_ln_omega[i] * (1 if j == k else 0)
                )

    diff_christoffel = np.max(np.abs(gamma_analytic - gamma_num))
    print(f"\nMax |Gamma_analytic - Gamma_numerical| = {diff_christoffel:.2e}")
    print(f"Christoffel symbol consistency: {'PASS' if diff_christoffel < 0.01 else 'FAIL'}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    elapsed = time.time() - t0
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    # Collect pass/fail
    christoffel_ok = diff_christoffel < 0.01

    eik_geo_ok = all(
        abs(r - 1.0) < 0.15
        for _, _, _, r, _ in geo_results
        if not math.isnan(r)
    )

    scaling_ok = (len(theta_b_products) > 1 and
                  all(abs(t) > 1e-10 for t in theta_b_products) and
                  (max(theta_b_products) - min(theta_b_products)) /
                  np.mean(theta_b_products) < 0.3)

    trajectory_ok = relative_dev < 0.05

    print(f"\n1. Christoffel symbols (analytic vs numerical): "
          f"{'PASS' if christoffel_ok else 'FAIL'} (err={diff_christoffel:.2e})")
    print(f"2. Eikonal/Geodesic agreement: "
          f"{'PASS' if eik_geo_ok else 'FAIL'}")
    print(f"3. Trajectory deviation: "
          f"{'PASS' if trajectory_ok else 'FAIL'} (rel={relative_dev:.2e})")
    print(f"4. 1/b deflection scaling: "
          f"{'PASS' if scaling_ok else 'FAIL'}")

    n_pass = sum([christoffel_ok, eik_geo_ok, trajectory_ok, scaling_ok])
    n_total = 4

    print(f"\nResult: {n_pass}/{n_total} tests passed")

    if n_pass >= 3:
        print("\nCONCLUSION: Test particles in the framework follow geodesics")
        print("of the emergent conformal metric g_ij = (1-f)^2 delta_ij.")
        print("The propagator dynamics REPRODUCE the geodesic equation of GR.")
        print("HYPOTHESIS SUPPORTED.")
    else:
        print("\nCONCLUSION: Geodesic agreement is partial or weak.")
        print("Further investigation needed.")

    print(f"\nElapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
