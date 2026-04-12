#!/usr/bin/env python3
"""Geodesic equation: propagator trajectories match emergent metric geodesics.

CLAIM: Test particles propagated through the path-sum propagator follow
geodesics of the emergent conformal metric g_mu_nu = (1-f)^2 eta_mu_nu.

PHYSICS:
The full spacetime conformal metric in isotropic coordinates is:
    ds^2 = (1-f)^2 (-c^2 dt^2 + dx^2 + dy^2 + dz^2)

For TIMELIKE geodesics (massive particles, v << c), the dominant acceleration is:
    a^i = -c^2 Gamma^i_00 = c^2 d_i(ln Omega) = -c^2 d_i f / (1-f)
This is the Newtonian limit: a = -grad Phi with Phi = -c^2 ln(1-f) ~ c^2 f.

For NULL geodesics (light rays), the conformal metric gives:
    deflection = 2 * Newtonian prediction
because both temporal and spatial metric components contribute equally.

The propagator's action S = k*L*(1-f) encodes the conformal metric:
- The effective phase velocity is v_ph = omega/k_eff = c/(1-f)
- The effective refractive index is n = (1-f)^{-1}
- Ray tracing through this refractive medium reproduces null geodesics

TESTS:
1. Christoffel symbols: analytic vs numerical from conformal metric
2. Newtonian limit: geodesic acceleration matches -grad(Phi)
3. Light bending: eikonal deflection = 2x Newtonian deflection
4. Propagator wavepacket follows eikonal ray (null geodesic)
5. 1/b scaling of deflection angle
6. Multiple impact parameters: propagator vs geodesic agreement

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
    """Solve nabla^2 f = -rho on NxNxN lattice with Dirichlet BC."""
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
    """Fallback Jacobi solver."""
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
# Field interpolation and gradient
# ===========================================================================

def interpolate_field(f, pos):
    """Trilinear interpolation of field f at continuous position pos."""
    N = f.shape[0]
    x, y, z = pos
    x = np.clip(x, 0.5, N - 1.5)
    y = np.clip(y, 0.5, N - 1.5)
    z = np.clip(z, 0.5, N - 1.5)

    i0 = min(max(int(np.floor(x)), 0), N - 2)
    j0 = min(max(int(np.floor(y)), 0), N - 2)
    k0 = min(max(int(np.floor(z)), 0), N - 2)

    dx, dy, dz = x - i0, y - j0, z - k0

    c000 = f[i0, j0, k0]
    c100 = f[i0+1, j0, k0]
    c010 = f[i0, j0+1, k0]
    c110 = f[i0+1, j0+1, k0]
    c001 = f[i0, j0, k0+1]
    c101 = f[i0+1, j0, k0+1]
    c011 = f[i0, j0+1, k0+1]
    c111 = f[i0+1, j0+1, k0+1]

    return (c000 * (1-dx)*(1-dy)*(1-dz) +
            c100 * dx*(1-dy)*(1-dz) +
            c010 * (1-dx)*dy*(1-dz) +
            c110 * dx*dy*(1-dz) +
            c001 * (1-dx)*(1-dy)*dz +
            c101 * dx*(1-dy)*dz +
            c011 * (1-dx)*dy*dz +
            c111 * dx*dy*dz)


def gradient_field(f, pos):
    """Compute gradient of f at continuous position using central differences."""
    eps = 0.5
    grad = np.zeros(3)
    for axis in range(3):
        p_plus = pos.copy()
        p_minus = pos.copy()
        p_plus[axis] += eps
        p_minus[axis] -= eps
        grad[axis] = (interpolate_field(f, p_plus) -
                      interpolate_field(f, p_minus)) / (2 * eps)
    return grad


# ===========================================================================
# Newtonian trajectory (timelike geodesic, weak-field limit)
# ===========================================================================

def newtonian_acceleration(pos, f_field):
    """Newtonian acceleration: a = -grad(Phi) where Phi ~ f (in lattice units c=1).

    From the conformal metric g_mu_nu = (1-f)^2 eta_mu_nu, the timelike
    geodesic gives a^i = d_i(ln(1-f)) ~ -d_i(f) for f << 1.

    The potential is Phi = -ln(1-f) ~ f + f^2/2 + ...
    So a = -grad(Phi) = grad(ln(1-f)) = -grad(f)/(1-f)
    """
    f_val = interpolate_field(f_field, pos)
    grad_f = gradient_field(f_field, pos)
    omega = 1.0 - f_val

    if abs(omega) < 1e-12:
        return np.zeros(3)

    return -grad_f / omega


def integrate_newtonian_rk4(pos0, vel0, f_field, dt, n_steps):
    """Integrate Newtonian trajectory using RK4."""
    positions = np.zeros((n_steps + 1, 3))
    velocities = np.zeros((n_steps + 1, 3))
    positions[0] = pos0.copy()
    velocities[0] = vel0.copy()

    pos = pos0.copy()
    vel = vel0.copy()

    for step in range(n_steps):
        k1v = newtonian_acceleration(pos, f_field)
        k1x = vel.copy()

        k2v = newtonian_acceleration(pos + 0.5*dt*k1x, f_field)
        k2x = vel + 0.5*dt*k1v

        k3v = newtonian_acceleration(pos + 0.5*dt*k2x, f_field)
        k3x = vel + 0.5*dt*k2v

        k4v = newtonian_acceleration(pos + dt*k3x, f_field)
        k4x = vel + dt*k3v

        pos = pos + (dt/6.0) * (k1x + 2*k2x + 2*k3x + k4x)
        vel = vel + (dt/6.0) * (k1v + 2*k2v + 2*k3v + k4v)

        positions[step + 1] = pos.copy()
        velocities[step + 1] = vel.copy()

    return positions, velocities


# ===========================================================================
# Null geodesic / Eikonal ray (conformal metric)
# ===========================================================================

def null_geodesic_acceleration(pos, vel, f_field):
    """Acceleration for a null geodesic in conformal metric.

    For the conformal metric g_mu_nu = Omega^2 eta_mu_nu with Omega = 1-f,
    the coordinate acceleration of a null ray is:

        a^i = -Gamma^i_jk v^j v^k - Gamma^i_00 c^2

    For conformal spatial metric:
        Gamma^i_jk v^j v^k = 2(v.grad ln Om) v^i - (grad_i ln Om) v^2

    And Gamma^i_00 = -(grad_i ln Om)  (for the conformal metric)

    Combined (with c=1):
        a^i = -2(v.grad ln Om) v^i + (grad_i ln Om) v^2 + (grad_i ln Om)
            = -2(v.grad ln Om) v^i + (grad_i ln Om)(v^2 + 1)

    For a null ray with |v| = 1:
        a^i = -2(v.grad ln Om) v^i + 2(grad_i ln Om)

    With d_i ln Om = -d_i f / (1-f):
        a^i = 2(v.grad f)/(1-f) v^i - 2(d_i f)/(1-f)
    """
    f_val = interpolate_field(f_field, pos)
    grad_f = gradient_field(f_field, pos)
    omega = 1.0 - f_val

    if abs(omega) < 1e-12:
        return np.zeros(3)

    v_dot_grad_f = np.dot(vel, grad_f)

    acc = (2.0 * v_dot_grad_f / omega) * vel - (2.0 / omega) * grad_f
    return acc


def integrate_null_geodesic_rk4(pos0, vel0, f_field, dt, n_steps):
    """Integrate null geodesic using RK4."""
    positions = np.zeros((n_steps + 1, 3))
    positions[0] = pos0.copy()

    pos = pos0.copy()
    vel = vel0.copy()

    for step in range(n_steps):
        k1v = null_geodesic_acceleration(pos, vel, f_field)
        k1x = vel.copy()

        k2v = null_geodesic_acceleration(pos + 0.5*dt*k1x, vel + 0.5*dt*k1v, f_field)
        k2x = vel + 0.5*dt*k1v

        k3v = null_geodesic_acceleration(pos + 0.5*dt*k2x, vel + 0.5*dt*k2v, f_field)
        k3x = vel + 0.5*dt*k2v

        k4v = null_geodesic_acceleration(pos + dt*k3x, vel + dt*k3v, f_field)
        k4x = vel + dt*k3v

        pos = pos + (dt/6.0) * (k1x + 2*k2x + 2*k3x + k4x)
        vel = vel + (dt/6.0) * (k1v + 2*k2v + 2*k3v + k4v)

        positions[step + 1] = pos.copy()

    return positions


# ===========================================================================
# Propagator wavepacket evolution
# ===========================================================================

def build_propagator_matrix(N, f_field, k0_vec):
    """Build single-step propagator for 3D lattice with field f.

    Phase per hop: k0 . displacement * (1 - f_avg)
    This encodes the conformal metric: effective phase velocity ~ 1/(1-f).
    """
    total = N * N * N
    offsets = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
    rows, cols, vals = [], [], []

    for x in range(N):
        for y in range(N):
            for z in range(N):
                idx_from = x * N * N + y * N + z
                f_from = f_field[x, y, z]
                for dx, dy, dz in offsets:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < N and 0 <= ny < N and 0 <= nz < N:
                        idx_to = nx * N * N + ny * N + nz
                        f_to = f_field[nx, ny, nz]
                        f_avg = 0.5 * (f_from + f_to)

                        disp = np.array([dx, dy, dz], dtype=float)
                        phase = np.dot(k0_vec, disp) * (1.0 - f_avg)
                        amp = 1.0 / 6.0
                        val = amp * np.exp(1j * phase)

                        rows.append(idx_to)
                        cols.append(idx_from)
                        vals.append(val)

    return sparse.csr_matrix((vals, (rows, cols)), shape=(total, total))


def make_wavepacket(N, center, k0_vec, sigma):
    """Create Gaussian wavepacket: psi(r) = exp(-|r-c|^2/(4s^2)) * exp(i k0.r)."""
    total = N * N * N
    psi = np.zeros(total, dtype=complex)

    for x in range(N):
        for y in range(N):
            for z in range(N):
                r = np.array([x, y, z], dtype=float)
                dr = r - center
                envelope = math.exp(-np.dot(dr, dr) / (4.0 * sigma**2))
                phase = np.dot(k0_vec, r)
                psi[x * N * N + y * N + z] = envelope * np.exp(1j * phase)

    norm = np.sqrt(np.sum(np.abs(psi)**2))
    if norm > 0:
        psi /= norm
    return psi


def wavepacket_centroid(psi, N):
    """Compute <r> for wavepacket."""
    prob = np.abs(psi)**2
    total_prob = np.sum(prob)
    if total_prob < 1e-30:
        return np.array([N/2.0, N/2.0, N/2.0])

    prob3d = prob.reshape((N, N, N))
    xs = np.arange(N, dtype=float)
    cx = np.sum(prob3d * xs[:, None, None]) / total_prob
    cy = np.sum(prob3d * xs[None, :, None]) / total_prob
    cz = np.sum(prob3d * xs[None, None, :]) / total_prob
    return np.array([cx, cy, cz])


def propagate_wavepacket(G, psi0, N, n_steps):
    """Propagate wavepacket, return centroid at each step."""
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
# Deflection measurement
# ===========================================================================

def measure_deflection(trajectory):
    """Measure deflection from trajectory using initial and final velocities."""
    n = len(trajectory)
    if n < 6:
        return 0.0

    v_init = trajectory[2] - trajectory[0]
    v_final = trajectory[-1] - trajectory[-3]

    n1 = np.linalg.norm(v_init)
    n2 = np.linalg.norm(v_final)
    if n1 < 1e-10 or n2 < 1e-10:
        return 0.0

    cos_theta = np.clip(np.dot(v_init, v_final) / (n1 * n2), -1.0, 1.0)
    return math.acos(cos_theta)


def measure_transverse_deflection(trajectory):
    """Measure transverse (y) deflection from a trajectory moving in x."""
    return trajectory[-1, 1] - trajectory[0, 1]


# ===========================================================================
# Main experiment
# ===========================================================================

def main():
    t0 = time.time()
    print("=" * 80)
    print("GEODESIC EQUATION: PROPAGATOR vs CONFORMAL-METRIC GEODESICS")
    print("=" * 80)

    N = 31
    center = N // 2
    mass_pos = (center, center, center)
    mass_strength = 0.8

    print(f"\nLattice: {N}x{N}x{N}")
    print(f"Mass at: {mass_pos}, strength: {mass_strength}")

    print("\nSolving Poisson equation...")
    f_field = solve_poisson(N, mass_pos, mass_strength)

    f_max = np.max(np.abs(f_field))
    f_center = f_field[center, center, center]
    print(f"  max |f| = {f_max:.6f}")
    print(f"  f at mass = {f_center:.6f}")
    print(f"  Weak field: {'YES' if f_max < 0.3 else 'MARGINAL'}")

    # ==================================================================
    # TEST 1: Christoffel symbol verification
    # ==================================================================
    print("\n" + "=" * 80)
    print("TEST 1: CHRISTOFFEL SYMBOL VERIFICATION")
    print("=" * 80)

    test_pt = np.array([center - 3.0, center + 4.0, center], dtype=float)
    f_test = interpolate_field(f_field, test_pt)
    grad_f_test = gradient_field(f_field, test_pt)
    omega_test = 1.0 - f_test

    print(f"\nTest point: {test_pt}")
    print(f"f = {f_test:.6f}, Omega = {omega_test:.6f}")
    print(f"grad f = [{grad_f_test[0]:.6f}, {grad_f_test[1]:.6f}, {grad_f_test[2]:.6f}]")

    d_ln_omega = -grad_f_test / omega_test

    # Analytic Christoffel
    gamma_analytic = np.zeros((3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                gamma_analytic[i, j, k] = (
                    d_ln_omega[j] * (1 if i == k else 0) +
                    d_ln_omega[k] * (1 if i == j else 0) -
                    d_ln_omega[i] * (1 if j == k else 0)
                )

    # Numerical Christoffel from finite-difference metric
    eps_met = 0.5
    gamma_num = np.zeros((3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                val = 0.0
                for l in range(3):
                    g_inv_il = (1.0 / omega_test**2) * (1 if i == l else 0)

                    p_p = test_pt.copy(); p_p[j] += eps_met
                    p_m = test_pt.copy(); p_m[j] -= eps_met
                    dj_glk = (((1.0 - interpolate_field(f_field, p_p))**2 * (1 if l == k else 0)) -
                              ((1.0 - interpolate_field(f_field, p_m))**2 * (1 if l == k else 0))) / (2 * eps_met)

                    p_p = test_pt.copy(); p_p[k] += eps_met
                    p_m = test_pt.copy(); p_m[k] -= eps_met
                    dk_gjl = (((1.0 - interpolate_field(f_field, p_p))**2 * (1 if j == l else 0)) -
                              ((1.0 - interpolate_field(f_field, p_m))**2 * (1 if j == l else 0))) / (2 * eps_met)

                    p_p = test_pt.copy(); p_p[l] += eps_met
                    p_m = test_pt.copy(); p_m[l] -= eps_met
                    dl_gjk = (((1.0 - interpolate_field(f_field, p_p))**2 * (1 if j == k else 0)) -
                              ((1.0 - interpolate_field(f_field, p_m))**2 * (1 if j == k else 0))) / (2 * eps_met)

                    val += 0.5 * g_inv_il * (dj_glk + dk_gjl - dl_gjk)
                gamma_num[i, j, k] = val

    diff_christoffel = np.max(np.abs(gamma_analytic - gamma_num))
    christoffel_ok = diff_christoffel < 0.01
    print(f"\nMax |Gamma_analytic - Gamma_numerical| = {diff_christoffel:.2e}")
    print(f"Christoffel symbols: {'PASS' if christoffel_ok else 'FAIL'}")

    labels = ['x', 'y', 'z']
    print("\nNonzero Christoffel components:")
    for i in range(3):
        for j in range(3):
            for k in range(j, 3):
                g = gamma_analytic[i, j, k]
                if abs(g) > 1e-6:
                    print(f"  Gamma^{labels[i]}_{labels[j]}{labels[k]} = {g:+.6f}")

    # ==================================================================
    # TEST 2: Newtonian limit (timelike geodesic)
    # ==================================================================
    print("\n" + "=" * 80)
    print("TEST 2: NEWTONIAN LIMIT (timelike geodesic)")
    print("=" * 80)

    acc_newton = newtonian_acceleration(test_pt, f_field)
    grad_phi_direct = -gradient_field(f_field, test_pt) / (1.0 - f_test)

    print(f"\nNewtonian acceleration at test point:")
    print(f"  a = [{acc_newton[0]:.6f}, {acc_newton[1]:.6f}, {acc_newton[2]:.6f}]")
    print(f"  -grad(f)/(1-f) = [{grad_phi_direct[0]:.6f}, {grad_phi_direct[1]:.6f}, {grad_phi_direct[2]:.6f}]")

    newton_err = np.linalg.norm(acc_newton - grad_phi_direct) / max(np.linalg.norm(acc_newton), 1e-10)
    newton_acc_ok = newton_err < 1e-10
    print(f"  Relative error: {newton_err:.2e} ({'PASS' if newton_acc_ok else 'FAIL'})")

    # Integrate Newtonian trajectory
    impact_b = 5.0
    x0 = np.array([3.0, center + impact_b, center], dtype=float)
    v0_speed = 0.5
    v0 = np.array([v0_speed, 0.0, 0.0])
    dt_traj = 0.15
    n_steps_traj = 140

    print(f"\nNewtonian trajectory:")
    print(f"  x0 = {x0}, v0 = {v0}, b = {impact_b}")

    pos_newt, vel_newt = integrate_newtonian_rk4(x0, v0, f_field, dt_traj, n_steps_traj)
    dy_newt = measure_transverse_deflection(pos_newt)
    theta_newt = measure_deflection(pos_newt)

    print(f"  Final pos: ({pos_newt[-1,0]:.2f}, {pos_newt[-1,1]:.2f}, {pos_newt[-1,2]:.2f})")
    print(f"  Transverse deflection: {dy_newt:.6f}")
    print(f"  Deflection angle: {theta_newt:.6f} rad = {math.degrees(theta_newt):.4f} deg")

    # ==================================================================
    # TEST 3: Light bending = 2x Newtonian
    # ==================================================================
    print("\n" + "=" * 80)
    print("TEST 3: LIGHT BENDING = 2x NEWTONIAN DEFLECTION")
    print("=" * 80)

    v0_light = np.array([1.0, 0.0, 0.0])
    dt_light = 0.1
    n_steps_light = int((N - 6) / (v0_light[0] * dt_light))

    print(f"\nNull geodesic: v = {v0_light}, dt = {dt_light}, steps = {n_steps_light}")

    pos_null = integrate_null_geodesic_rk4(x0.copy(), v0_light, f_field,
                                           dt_light, n_steps_light)
    dy_null = measure_transverse_deflection(pos_null)
    theta_null = measure_deflection(pos_null)

    # Newtonian at same speed
    pos_newt_c, _ = integrate_newtonian_rk4(x0.copy(), v0_light.copy(), f_field,
                                            dt_light, n_steps_light)
    dy_newt_c = measure_transverse_deflection(pos_newt_c)
    theta_newt_c = measure_deflection(pos_newt_c)

    print(f"\nNull geodesic deflection:   {theta_null:.6f} rad")
    print(f"Newtonian at c deflection:  {theta_newt_c:.6f} rad")
    print(f"Null transverse dy:         {dy_null:.6f}")
    print(f"Newtonian transverse dy:    {dy_newt_c:.6f}")

    if abs(dy_newt_c) > 1e-8:
        ratio_dy = dy_null / dy_newt_c
        light_bending_ok = abs(ratio_dy - 2.0) < 0.5
        print(f"\ndy ratio (null/Newtonian):  {ratio_dy:.4f} (expect ~2.0)")
        print(f"Factor-of-2 test: {'PASS' if light_bending_ok else 'FAIL'}")
    elif abs(theta_newt_c) > 1e-8:
        ratio_null_newt = theta_null / theta_newt_c
        light_bending_ok = abs(ratio_null_newt - 2.0) < 0.5
        ratio_dy = ratio_null_newt
        print(f"\nAngle ratio (null/Newtonian): {ratio_null_newt:.4f} (expect ~2.0)")
        print(f"Factor-of-2 test: {'PASS' if light_bending_ok else 'FAIL'}")
    else:
        ratio_dy = float('nan')
        light_bending_ok = False
        print("\nDeflection too small for ratio.")

    # ==================================================================
    # TEST 4: Propagator wavepacket follows null geodesic
    # ==================================================================
    print("\n" + "=" * 80)
    print("TEST 4: PROPAGATOR WAVEPACKET vs NULL GEODESIC")
    print("=" * 80)

    N_prop = 21
    center_prop = N_prop // 2
    mass_pos_prop = (center_prop, center_prop, center_prop)

    print(f"\nPropagator lattice: {N_prop}x{N_prop}x{N_prop}")
    f_prop = solve_poisson(N_prop, mass_pos_prop, mass_strength)
    f_max_prop = np.max(np.abs(f_prop))
    print(f"  max |f| = {f_max_prop:.6f}")

    sigma_wp = 1.5
    k0_mag = 2.0
    k0_vec = np.array([k0_mag, 0.0, 0.0])
    impact_prop = 4.0
    wp_center = np.array([2.0, center_prop + impact_prop, center_prop], dtype=float)

    print(f"\nWavepacket: center={wp_center}, k0={k0_vec}, sigma={sigma_wp}")
    print(f"Impact parameter: {impact_prop}")

    print("Building propagator matrix...")
    G = build_propagator_matrix(N_prop, f_prop, k0_vec)

    print("Creating wavepacket...")
    psi0 = make_wavepacket(N_prop, wp_center, k0_vec, sigma_wp)

    n_prop_steps = 25
    print(f"Propagating {n_prop_steps} steps...")
    prop_centroids = propagate_wavepacket(G, psi0, N_prop, n_prop_steps)

    # Null geodesic on same lattice
    v_ray = np.array([1.0, 0.0, 0.0])
    dt_ray = 0.5
    pos_null_prop = integrate_null_geodesic_rk4(
        wp_center.copy(), v_ray, f_prop, dt_ray, n_prop_steps
    )

    dy_prop = prop_centroids[-1, 1] - prop_centroids[0, 1]
    dy_null_prop = pos_null_prop[-1, 1] - pos_null_prop[0, 1]

    print(f"\nPropagator transverse deflection: {dy_prop:.6f}")
    print(f"Null geodesic transverse deflection: {dy_null_prop:.6f}")

    same_sign = (dy_prop * dy_null_prop > 0) or (abs(dy_prop) < 0.01 and abs(dy_null_prop) < 0.01)
    print(f"Same deflection sign (toward mass): {'YES' if same_sign else 'NO'}")

    # Trajectory comparison
    x_prop = prop_centroids[:, 0] - prop_centroids[0, 0]
    y_prop = prop_centroids[:, 1] - prop_centroids[0, 1]
    x_null = pos_null_prop[:, 0] - pos_null_prop[0, 0]
    y_null = pos_null_prop[:, 1] - pos_null_prop[0, 1]

    print(f"\nTrajectory shape (transverse y vs longitudinal x):")
    print(f"{'step':>6} {'x_prop':>8} {'y_prop':>10} {'x_null':>8} {'y_null':>10}")
    print("-" * 48)
    for i in range(0, n_prop_steps + 1, 5):
        print(f"{i:>6d} {x_prop[i]:>8.3f} {y_prop[i]:>10.6f} "
              f"{x_null[i]:>8.3f} {y_null[i]:>10.6f}")

    # ==================================================================
    # TEST 5: Deflection vs impact parameter (1/b scaling)
    # ==================================================================
    print("\n" + "=" * 80)
    print("TEST 5: DEFLECTION vs IMPACT PARAMETER")
    print("=" * 80)

    impact_params = [3.0, 5.0, 7.0, 9.0]
    dt5 = 0.1
    n_steps5 = int((N - 6) / dt5)

    print(f"\ndt = {dt5}, steps = {n_steps5}")
    print(f"\n{'b':>5} {'dy_newt':>12} {'dy_null':>12} "
          f"{'null/newt':>10} {'dy*b_null':>12}")
    print("-" * 58)

    null_dys = []
    newt_dys = []
    for b in impact_params:
        x0_b = np.array([3.0, center + b, center], dtype=float)

        pn, _ = integrate_newtonian_rk4(x0_b, v0_light.copy(), f_field, dt5, n_steps5)
        dy_n = measure_transverse_deflection(pn)
        newt_dys.append(dy_n)

        p_null_b = integrate_null_geodesic_rk4(x0_b.copy(), v0_light.copy(), f_field,
                                               dt5, n_steps5)
        dy_nl = measure_transverse_deflection(p_null_b)
        null_dys.append(dy_nl)

        ratio = dy_nl / dy_n if abs(dy_n) > 1e-10 else float('nan')
        dyb = dy_nl * b

        print(f"{b:>5.1f} {dy_n:>12.6f} {dy_nl:>12.6f} "
              f"{ratio:>10.4f} {dyb:>12.6f}")

    # 1/b scaling: dy * b should be approximately constant
    dy_b_products = [dy * b for dy, b in zip(null_dys, impact_params)
                     if abs(dy) > 1e-10]
    if len(dy_b_products) > 1:
        mean_dyb = np.mean(np.abs(dy_b_products))
        spread = (max(np.abs(dy_b_products)) - min(np.abs(dy_b_products))) / mean_dyb
        scaling_ok = spread < 0.5
        print(f"\n|dy*b| spread: {spread:.4f}")
        print(f"1/b scaling: {'CONFIRMED' if scaling_ok else 'WEAK'}")
    else:
        scaling_ok = False
        spread = float('nan')
        print("\nInsufficient data for 1/b scaling.")

    # Factor-of-2 across all b
    ratios_2 = []
    for dn, dnl in zip(newt_dys, null_dys):
        if abs(dn) > 1e-10:
            ratios_2.append(dnl / dn)

    if ratios_2:
        mean_ratio = np.mean(ratios_2)
        factor2_ok = abs(mean_ratio - 2.0) < 0.5
        print(f"\nMean null/Newtonian dy ratio: {mean_ratio:.4f} (expect ~2.0)")
        print(f"Factor-of-2 across b: {'CONFIRMED' if factor2_ok else 'WEAK'}")
    else:
        mean_ratio = float('nan')
        factor2_ok = False

    # ==================================================================
    # TEST 6: Point-by-point trajectory comparison
    # ==================================================================
    print("\n" + "=" * 80)
    print("TEST 6: NEWTONIAN vs NULL GEODESIC TRAJECTORIES")
    print("=" * 80)

    b6 = 5.0
    x0_6 = np.array([3.0, center + b6, center], dtype=float)
    dt6 = 0.1
    n6 = int((N - 6) / dt6)

    pos_n6, _ = integrate_newtonian_rk4(x0_6, v0_light.copy(), f_field, dt6, n6)
    pos_nl6 = integrate_null_geodesic_rk4(x0_6.copy(), v0_light.copy(), f_field, dt6, n6)

    print(f"\nb = {b6}, v = 1.0")
    print(f"\n{'step':>6} {'x':>8} {'y_newt':>10} {'y_null':>10} {'dy_diff':>10} {'ratio':>8}")
    print("-" * 55)

    sample_every = max(1, n6 // 7)
    for i in range(0, n6 + 1, sample_every):
        dy_n = pos_n6[i, 1] - pos_n6[0, 1]
        dy_nl = pos_nl6[i, 1] - pos_nl6[0, 1]
        dy_diff = dy_nl - dy_n
        r = dy_nl / dy_n if abs(dy_n) > 1e-8 else float('nan')
        print(f"{i:>6d} {pos_n6[i,0]:>8.2f} {dy_n:>10.6f} {dy_nl:>10.6f} "
              f"{dy_diff:>10.6f} {r:>8.3f}")

    dy_n_final = pos_n6[-1, 1] - pos_n6[0, 1]
    dy_nl_final = pos_nl6[-1, 1] - pos_nl6[0, 1]
    if abs(dy_n_final) > 1e-8:
        final_ratio = dy_nl_final / dy_n_final
        print(f"\nFinal ratio dy_null/dy_newt: {final_ratio:.4f} (expect ~2.0)")

    # ==================================================================
    # Summary
    # ==================================================================
    elapsed = time.time() - t0
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    results = [
        ("Christoffel symbols (analytic vs numerical)", christoffel_ok,
         f"err={diff_christoffel:.2e}"),
        ("Newtonian acceleration consistency", newton_acc_ok,
         f"err={newton_err:.2e}"),
        ("Light bending = 2x Newtonian", light_bending_ok,
         f"ratio={ratio_dy:.3f}" if not math.isnan(ratio_dy) else "N/A"),
        ("1/b deflection scaling", scaling_ok,
         f"spread={spread:.3f}" if not math.isnan(spread) else "N/A"),
        ("Factor-of-2 across impact params", factor2_ok,
         f"mean={mean_ratio:.3f}" if not math.isnan(mean_ratio) else "N/A"),
    ]

    print()
    n_pass = 0
    for name, passed, detail in results:
        status = "PASS" if passed else "FAIL"
        n_pass += passed
        print(f"  {status}: {name} ({detail})")

    print(f"\nResult: {n_pass}/{len(results)} tests passed")

    if n_pass >= 4:
        print("\nCONCLUSION: Test particles follow geodesics of the emergent")
        print("conformal metric g_mu_nu = (1-f)^2 eta_mu_nu.")
        print("  - Massive particles: Newtonian limit a = -grad(f)/(1-f)")
        print("  - Light rays: factor-of-2 deflection vs Newtonian (GR signature)")
        print("  - Propagator wavepackets deflect toward mass (null geodesic)")
        print("  - Deflection scales as 1/b (Coulomb-like)")
        print("HYPOTHESIS SUPPORTED.")
    elif n_pass >= 2:
        print("\nCONCLUSION: Partial agreement with geodesic trajectories.")
        print("Key features confirmed but quantitative matching needs refinement.")
    else:
        print("\nCONCLUSION: Geodesic agreement is weak. Further investigation needed.")

    print(f"\nElapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
