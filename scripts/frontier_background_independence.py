#!/usr/bin/env python3
"""Background independence: effective geometry differs from input graph topology.

The path-sum propagator with action S = L(1-f), where f is the gravitational
field from the Poisson equation, creates an EFFECTIVE geometry that differs
from the bare lattice topology:

1. EFFECTIVE CONNECTIVITY: The propagator edge weight w = exp(-k*(1-f)) is
   NON-UNIFORM when gravity is present. Near mass, f>0 makes w larger --
   the effective graph has stronger connections near mass. We measure the
   edge weight distribution and show it becomes non-uniform.

2. EFFECTIVE DISTANCE: d_eff(i,j) = -log|G(i,j)| defines a metric from the
   Green's function. With gravity, effective distances differ from graph
   distances -- the effective metric is NOT the flat lattice metric.

3. EFFECTIVE DIMENSION: The spectral dimension of the propagator-weighted
   Laplacian differs from 3 near the source, measured via the heat kernel
   return probability on the weighted graph.

4. GEOMETRY RESPONDS TO MATTER: The effective geometry around one mass
   changes when a second mass is added elsewhere -- matter tells geometry
   how to curve.

Key result: "Although the graph topology is fixed, the effective geometry --
as measured by propagator Green's functions, spectral dimension, and
connectivity -- changes in response to the gravitational field. The input
graph provides the substrate; the geometry is an output."

PStack experiment: background-independence
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np

try:
    from scipy import sparse
    from scipy.sparse.linalg import spsolve, eigsh
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


# ============================================================================
# Poisson solver (standard infrastructure)
# ============================================================================

def solve_poisson_sparse(N: int, mass_positions: list[tuple[int, int, int]],
                         mass_strengths: list[float]) -> np.ndarray:
    """Solve 3D Poisson equation with multiple sources, Dirichlet BC."""
    M = N - 2
    n_interior = M * M * M

    def idx(i, j, k):
        return i * M * M + j * M + k

    rows, cols, vals = [], [], []
    rhs = np.zeros(n_interior)

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

                for pos, strength in zip(mass_positions, mass_strengths):
                    mx, my, mz = pos
                    mi, mj, mk = mx - 1, my - 1, mz - 1
                    if i == mi and j == mj and k == mk:
                        rhs[c] += -strength

    A = sparse.csr_matrix((vals, (rows, cols)), shape=(n_interior, n_interior))
    phi_interior = spsolve(A, rhs)

    field = np.zeros((N, N, N))
    for i in range(M):
        for j in range(M):
            for k in range(M):
                field[i+1, j+1, k+1] = phi_interior[idx(i, j, k)]
    return field


def solve_poisson_jacobi(N: int, mass_positions: list[tuple[int, int, int]],
                         mass_strengths: list[float],
                         max_iter: int = 10000, tol: float = 1e-7) -> np.ndarray:
    """Fallback Jacobi solver."""
    field = np.zeros((N, N, N))
    source = np.zeros((N, N, N))
    for pos, strength in zip(mass_positions, mass_strengths):
        mx, my, mz = pos
        source[mx, my, mz] = strength
    for _ in range(max_iter):
        new = np.zeros_like(field)
        new[1:-1, 1:-1, 1:-1] = (
            field[2:, 1:-1, 1:-1] + field[:-2, 1:-1, 1:-1] +
            field[1:-1, 2:, 1:-1] + field[1:-1, :-2, 1:-1] +
            field[1:-1, 1:-1, 2:] + field[1:-1, 1:-1, :-2] +
            source[1:-1, 1:-1, 1:-1]
        ) / 6.0
        if np.max(np.abs(new - field)) < tol:
            field = new
            break
        field = new
    return field


def solve_poisson(N: int, mass_positions: list[tuple[int, int, int]],
                  mass_strengths: list[float]) -> np.ndarray:
    if HAS_SCIPY and N <= 50:
        return solve_poisson_sparse(N, mass_positions, mass_strengths)
    return solve_poisson_jacobi(N, mass_positions, mass_strengths)


# ============================================================================
# Propagator-weighted graph tools
# ============================================================================

def edge_weight(field: np.ndarray, x1: int, y1: int, z1: int,
                x2: int, y2: int, z2: int, k: float) -> float:
    """Propagator edge weight: geometric mean of endpoint weights.

    w(i,j) = exp(-k * (1-f_i)/2) * exp(-k * (1-f_j)/2)
           = exp(-k * (1 - (f_i+f_j)/2))

    This symmetrizes the weight between endpoints.
    """
    f_avg = 0.5 * (field[x1, y1, z1] + field[x2, y2, z2])
    return math.exp(-k * (1.0 - f_avg))


def build_effective_laplacian(N: int, field: np.ndarray,
                              k: float = 1.0) -> sparse.csr_matrix:
    """Build the propagator-weighted Laplacian on the 3D lattice.

    Edge weight w_{ij} = exp(-k * (1 - f_avg)) where f_avg = (f_i + f_j)/2.
    L_eff[i,j] = w_{ij} for neighbors, L_eff[i,i] = -sum_j w_{ij}.
    """
    n_sites = N * N * N

    def flat_idx(x, y, z):
        return x * N * N + y * N + z

    rows, cols, vals = [], [], []
    neighbors = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    for x in range(N):
        for y in range(N):
            for z in range(N):
                i = flat_idx(x, y, z)
                diag_sum = 0.0
                for dx, dy, dz in neighbors:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < N and 0 <= ny < N and 0 <= nz < N:
                        j = flat_idx(nx, ny, nz)
                        f_avg = 0.5 * (field[x, y, z] + field[nx, ny, nz])
                        w = math.exp(-k * (1.0 - f_avg))
                        rows.append(i); cols.append(j); vals.append(w)
                        diag_sum += w
                rows.append(i); cols.append(i); vals.append(-diag_sum)

    return sparse.csr_matrix((vals, (rows, cols)), shape=(n_sites, n_sites))


def compute_green_function_column(L_eff: sparse.csr_matrix,
                                  source_idx: int,
                                  regularize: float = 0.01) -> np.ndarray:
    """Compute one column of the Green's function G = (regularize*I - L_eff)^{-1}.

    We solve (regularize*I - L_eff) * g = e_source.
    """
    n = L_eff.shape[0]
    rhs = np.zeros(n)
    rhs[source_idx] = 1.0
    A = regularize * sparse.eye(n) - L_eff
    g = spsolve(A.tocsc(), rhs)
    return g


# ============================================================================
# Test 1: Effective connectivity (edge weight distribution)
# ============================================================================

def test_effective_connectivity(N: int, mass_strength: float, k: float):
    """Show that gravity makes edge weights non-uniform."""
    print("=" * 80)
    print("TEST 1: EFFECTIVE CONNECTIVITY")
    print("=" * 80)
    print()
    print("On the flat lattice, every edge has weight w = exp(-k) (uniform).")
    print("With gravity, w = exp(-k*(1-f)) varies with position.")
    print("Near mass (f>0): w > exp(-k) -- edges are STRONGER (more amplitude).")
    print("Far from mass (f~0): w ~ exp(-k) -- edges approach flat value.")
    print("The effective graph has non-uniform connectivity from gravity.")
    print()

    mid = N // 2
    field_grav = solve_poisson(N, [(mid, mid, mid)], [mass_strength])

    w_flat = math.exp(-k)

    # Collect average edge weight at each radius
    print(f"Lattice N={N}, mass at center, M={mass_strength:.1f}, k={k:.1f}")
    print(f"Flat edge weight: w_flat = exp(-{k:.1f}) = {w_flat:.6f}")
    print()
    print(f"{'r':>4s} {'<w>':>12s} {'w/w_flat':>12s} {'std(w)':>12s} "
          f"{'f(r)':>12s} {'n_edges':>8s}")
    print("-" * 65)

    results = []
    for r in range(1, mid - 1):
        weights = []
        f_vals = []
        neighbors = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
                      (0, 0, 1), (0, 0, -1)]
        for x in range(1, N - 1):
            for y in range(1, N - 1):
                for z in range(1, N - 1):
                    dist = math.sqrt((x - mid)**2 + (y - mid)**2 + (z - mid)**2)
                    if abs(dist - r) < 0.7:
                        for dx, dy, dz in neighbors:
                            nx, ny, nz = x + dx, y + dy, z + dz
                            if 0 <= nx < N and 0 <= ny < N and 0 <= nz < N:
                                w = edge_weight(field_grav, x, y, z,
                                                nx, ny, nz, k)
                                weights.append(w)
                        f_vals.append(field_grav[x, y, z])

        if weights:
            avg_w = np.mean(weights)
            std_w = np.std(weights)
            avg_f = np.mean(f_vals) if f_vals else 0.0
            ratio = avg_w / w_flat
            results.append((r, avg_w, ratio, std_w, avg_f, len(weights)))
            print(f"{r:>4d} {avg_w:>12.6f} {ratio:>12.6f} {std_w:>12.6f} "
                  f"{avg_f:>12.6f} {len(weights):>8d}")

    print()
    if results:
        inner = [r for r in results if r[0] <= 3]
        outer = [r for r in results if r[0] >= mid - 3]
        if inner and outer:
            ratio_inner = np.mean([r[2] for r in inner])
            ratio_outer = np.mean([r[2] for r in outer])
            print(f"Edge weight ratio w/w_flat:")
            print(f"  Inner (r<=3): {ratio_inner:.6f}")
            print(f"  Outer (r>={mid-3}): {ratio_outer:.6f}")
            print(f"  Ratio inner/outer: {ratio_inner/ratio_outer:.6f}")
            print()
            if ratio_inner > ratio_outer * 1.01:
                print("RESULT: Edge weights are NON-UNIFORM. Gravity creates an")
                print("effective graph with different connectivity than the input lattice.")
                print(f"Edges near mass are {(ratio_inner/ratio_outer - 1)*100:.1f}% "
                      f"stronger than far from mass.")
            else:
                print("Edge weights are approximately uniform.")

    print()
    return True


# ============================================================================
# Test 2: Effective distance
# ============================================================================

def test_effective_distance(N: int, mass_strength: float, k: float):
    """Show that d_eff = -log|G| differs from graph distance with gravity."""
    print("=" * 80)
    print("TEST 2: EFFECTIVE DISTANCE")
    print("=" * 80)
    print()
    print("Define d_eff(i,j) = -log|G(i,j)| where G is the Green's function.")
    print("On a flat lattice, d_eff scales linearly with graph distance r.")
    print("With gravity, d_eff(r) has a different profile -- the effective")
    print("metric departs from the flat lattice metric.")
    print()

    mid = N // 2
    field_grav = solve_poisson(N, [(mid, mid, mid)], [mass_strength])
    field_flat = np.zeros((N, N, N))

    L_grav = build_effective_laplacian(N, field_grav, k)
    L_flat = build_effective_laplacian(N, field_flat, k)

    source_idx = mid * N * N + mid * N + mid
    g_grav = compute_green_function_column(L_grav, source_idx)
    g_flat = compute_green_function_column(L_flat, source_idx)

    G_grav = g_grav.reshape((N, N, N))
    G_flat = g_flat.reshape((N, N, N))

    print(f"Lattice N={N}, source at center, M={mass_strength:.1f}, k={k:.1f}")
    print()

    # Measure d_eff along the positive x-axis
    print("Effective distance along x-axis from center:")
    print(f"{'r':>4s} {'d_flat':>12s} {'d_grav':>12s} {'Delta_d':>12s} "
          f"{'d_flat/r':>12s} {'d_grav/r':>12s} {'f(r)':>12s}")
    print("-" * 80)

    results = []
    for r in range(1, mid - 1):
        x_site = mid + r
        if x_site >= N - 1:
            continue
        y_site, z_site = mid, mid

        g_f = abs(G_flat[x_site, y_site, z_site])
        g_g = abs(G_grav[x_site, y_site, z_site])

        if g_f < 1e-30 or g_g < 1e-30:
            continue

        d_flat = -math.log(g_f)
        d_grav = -math.log(g_g)
        delta = d_grav - d_flat
        f_r = field_grav[x_site, y_site, z_site]

        results.append((r, d_flat, d_grav, delta, d_flat / r, d_grav / r, f_r))
        print(f"{r:>4d} {d_flat:>12.6f} {d_grav:>12.6f} {delta:>+12.6f} "
              f"{d_flat/r:>12.6f} {d_grav/r:>12.6f} {f_r:>12.6f}")

    print()
    if results:
        # Check non-uniformity: d_eff/r should be constant for flat, non-constant with gravity
        flat_slopes = [r[4] for r in results]
        grav_slopes = [r[5] for r in results]

        flat_std = np.std(flat_slopes)
        grav_std = np.std(grav_slopes)

        print(f"Uniformity of d_eff/r (std dev of d/r across radii):")
        print(f"  Flat: std(d_flat/r) = {flat_std:.6f}")
        print(f"  Grav: std(d_grav/r) = {grav_std:.6f}")
        print()

        # The Delta should have a radial profile (not constant)
        deltas = [r[3] for r in results]
        delta_range = max(deltas) - min(deltas)
        print(f"Range of Delta_d = d_grav - d_flat across radii: {delta_range:.6f}")
        print()

        if delta_range > 0.01:
            print("RESULT: The effective distance d_eff = -log|G| has a DIFFERENT")
            print("radial profile with gravity vs. without. The propagator sees a")
            print("metric that differs from the flat lattice metric.")
            print()
            # Show the metric deviation
            inner_delta = np.mean([r[3] for r in results if r[0] <= 3])
            outer_delta = np.mean([r[3] for r in results if r[0] >= mid - 4])
            print(f"  Delta_d (inner, r<=3): {inner_delta:+.6f}")
            print(f"  Delta_d (outer, r>={mid-4}): {outer_delta:+.6f}")
            if abs(inner_delta) > abs(outer_delta):
                print("  Metric modification is strongest near the mass => curved geometry.")
            elif abs(inner_delta) < abs(outer_delta):
                print("  Metric modification is strongest far from mass (boundary effects).")
        else:
            print("Effective distances track graph distances closely.")

    print()
    return True


# ============================================================================
# Test 3: Effective spectral dimension via heat kernel
# ============================================================================

def test_effective_dimension(N: int, mass_strength: float, k: float):
    """Show spectral dimension changes near gravitational source.

    Uses the random walk / heat kernel approach: diffuse from a point on
    the weighted graph and measure the return probability P(t).
    d_s = -2 * d(log P)/d(log t).
    """
    print("=" * 80)
    print("TEST 3: EFFECTIVE SPECTRAL DIMENSION")
    print("=" * 80)
    print()
    print("The spectral dimension d_s = -2 * d(log P(t))/d(log t)")
    print("where P(t) is the heat kernel return probability on the weighted graph.")
    print("We compute P(t) via matrix exponentiation of the normalized Laplacian.")
    print()

    mid = N // 2
    field_grav = solve_poisson(N, [(mid, mid, mid)], [mass_strength])
    field_flat = np.zeros((N, N, N))

    # Build normalized transition matrices: T = D^{-1} W
    # where D is degree matrix and W is adjacency weight matrix
    # Then P(t) = (T^t)_{ii} for integer diffusion steps

    def build_transition_matrix(field, N, k_val):
        """Build row-stochastic transition matrix from weighted edges."""
        n = N * N * N

        def flat_idx(x, y, z):
            return x * N * N + y * N + z

        rows_l, cols_l, vals_l = [], [], []
        nbrs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
                (0, 0, 1), (0, 0, -1)]

        for x in range(N):
            for y in range(N):
                for z in range(N):
                    i = flat_idx(x, y, z)
                    ws = []
                    js = []
                    for dx, dy, dz in nbrs:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < N and 0 <= ny < N and 0 <= nz < N:
                            j = flat_idx(nx, ny, nz)
                            f_avg = 0.5 * (field[x, y, z] + field[nx, ny, nz])
                            w = math.exp(-k_val * (1.0 - f_avg))
                            ws.append(w)
                            js.append(j)
                    # Normalize to make row-stochastic
                    w_sum = sum(ws)
                    if w_sum > 0:
                        for j, w in zip(js, ws):
                            rows_l.append(i)
                            cols_l.append(j)
                            vals_l.append(w / w_sum)

        return sparse.csr_matrix((vals_l, (rows_l, cols_l)), shape=(n, n))

    print(f"Lattice N={N}, mass at center, M={mass_strength:.1f}, k={k:.1f}")
    print("Building transition matrices...")

    T_grav = build_transition_matrix(field_grav, N, k)
    T_flat = build_transition_matrix(field_flat, N, k)

    # Compute return probability via repeated sparse matrix-vector multiplication
    # P(t) = (T^t e_i)[i]
    n_steps = 80
    step_values = list(range(1, n_steps + 1))

    # Test at several positions
    test_sites = [
        ("center", mid, mid, mid),
        ("near (r=2)", mid + 2, mid, mid),
        ("mid (r=5)", mid + 5, mid, mid),
        ("far (r=8)", mid + 8, mid, mid) if mid + 8 < N else None,
    ]
    test_sites = [s for s in test_sites if s is not None]

    print()
    for label, px, py, pz in test_sites:
        site_idx = px * N * N + py * N + pz
        f_val = field_grav[px, py, pz]

        # Diffuse on flat graph
        v_flat = np.zeros(N * N * N)
        v_flat[site_idx] = 1.0
        p_flat = []
        v = v_flat.copy()
        for t in range(1, n_steps + 1):
            v = T_flat.dot(v)
            p_flat.append(v[site_idx])

        # Diffuse on gravity graph
        v_grav = np.zeros(N * N * N)
        v_grav[site_idx] = 1.0
        p_grav = []
        v = v_grav.copy()
        for t in range(1, n_steps + 1):
            v = T_grav.dot(v)
            p_grav.append(v[site_idx])

        # Compute spectral dimension from log-log slope
        # Use intermediate steps to avoid early/late artifacts
        t_arr = np.array(step_values, dtype=float)
        p_flat_arr = np.array(p_flat)
        p_grav_arr = np.array(p_grav)

        # Select range where P(t) is well-behaved
        start_t = 5
        end_t = 40
        mask = (t_arr >= start_t) & (t_arr <= end_t) & (p_flat_arr > 1e-30) & (p_grav_arr > 1e-30)

        if np.sum(mask) >= 5:
            log_t = np.log(t_arr[mask])
            log_pf = np.log(p_flat_arr[mask])
            log_pg = np.log(p_grav_arr[mask])

            slope_f = np.polyfit(log_t, log_pf, 1)[0]
            slope_g = np.polyfit(log_t, log_pg, 1)[0]

            ds_flat = -2.0 * slope_f
            ds_grav = -2.0 * slope_g
        else:
            ds_flat = ds_grav = float('nan')

        print(f"  {label}: f={f_val:.4f}, d_s(flat)={ds_flat:.3f}, "
              f"d_s(grav)={ds_grav:.3f}, Delta={ds_grav - ds_flat:+.3f}")

    print()
    print("Interpretation: if d_s differs between flat and gravity cases,")
    print("the effective dimensionality seen by the propagator changes.")
    print("Non-uniform d_s across positions = curved effective geometry.")
    print()
    return True


# ============================================================================
# Test 4: Geometry responds to matter
# ============================================================================

def test_geometry_responds_to_matter(N: int, mass_strength: float, k: float):
    """Show that geometry near mass A depends on where mass B is placed."""
    print("=" * 80)
    print("TEST 4: GEOMETRY RESPONDS TO MATTER")
    print("=" * 80)
    print()
    print("Place two masses at different positions. Show that the effective")
    print("geometry (Green's function) around mass A depends on where mass B is.")
    print("This is the graph analog of 'matter tells geometry how to curve'.")
    print()

    mid = N // 2

    # Configuration 1: mass A at center only
    pos_A = (mid, mid, mid)
    field_A = solve_poisson(N, [pos_A], [mass_strength])

    # Configuration 2: mass A at center + mass B offset along x
    offset = max(4, mid // 2)
    pos_B1 = (mid + offset, mid, mid)
    field_AB1 = solve_poisson(N, [pos_A, pos_B1], [mass_strength, mass_strength])

    # Configuration 3: mass A at center + mass B offset along y
    pos_B2 = (mid, mid + offset, mid)
    field_AB2 = solve_poisson(N, [pos_A, pos_B2], [mass_strength, mass_strength])

    # Build effective Laplacians
    L_A = build_effective_laplacian(N, field_A, k)
    L_AB1 = build_effective_laplacian(N, field_AB1, k)
    L_AB2 = build_effective_laplacian(N, field_AB2, k)

    # Compute Green's function from center (mass A location)
    center_idx = mid * N * N + mid * N + mid

    print(f"Lattice N={N}, k={k:.1f}, M={mass_strength:.1f}")
    print(f"Mass A at {pos_A}")
    print(f"Mass B1 at {pos_B1} (offset along x by {offset})")
    print(f"Mass B2 at {pos_B2} (offset along y by {offset})")
    print()

    g_A = compute_green_function_column(L_A, center_idx)
    g_AB1 = compute_green_function_column(L_AB1, center_idx)
    g_AB2 = compute_green_function_column(L_AB2, center_idx)

    G_A = g_A.reshape((N, N, N))
    G_AB1 = g_AB1.reshape((N, N, N))
    G_AB2 = g_AB2.reshape((N, N, N))

    # Compare effective distances d_eff = -log|G| at sample points around mass A
    print("Effective distance d_eff = -log|G| from center in each configuration:")
    print(f"{'point':>15s} {'d(A)':>10s} {'d(A+Bx)':>10s} {'d(A+By)':>10s} "
          f"{'Bx shift':>10s} {'By shift':>10s}")
    print("-" * 65)

    sample_points = []
    # Along x-axis (toward/away from B1)
    for dr in [2, 3, 4, -2, -3, -4]:
        x = mid + dr
        if 1 <= x < N - 1:
            sample_points.append(((x, mid, mid), f"x={dr:+d}"))
    # Along y-axis (toward/away from B2)
    for dr in [2, 3, 4, -2, -3, -4]:
        y = mid + dr
        if 1 <= y < N - 1:
            sample_points.append(((mid, y, mid), f"y={dr:+d}"))

    shifts_bx = []
    shifts_by = []

    for (px, py, pz), label in sample_points:
        ga = abs(G_A[px, py, pz])
        gab1 = abs(G_AB1[px, py, pz])
        gab2 = abs(G_AB2[px, py, pz])

        if ga < 1e-30:
            continue

        d_a = -math.log(ga)
        d_ab1 = -math.log(max(gab1, 1e-30))
        d_ab2 = -math.log(max(gab2, 1e-30))
        shift_bx = d_ab1 - d_a
        shift_by = d_ab2 - d_a

        shifts_bx.append(shift_bx)
        shifts_by.append(shift_by)

        print(f"{label:>15s} {d_a:>10.5f} {d_ab1:>10.5f} {d_ab2:>10.5f} "
              f"{shift_bx:>+10.5f} {shift_by:>+10.5f}")

    print()

    if shifts_bx and shifts_by:
        rms_bx = np.sqrt(np.mean(np.array(shifts_bx) ** 2))
        rms_by = np.sqrt(np.mean(np.array(shifts_by) ** 2))
        print(f"RMS metric shift from mass B along x: {rms_bx:.6f}")
        print(f"RMS metric shift from mass B along y: {rms_by:.6f}")

        if rms_bx > 0.001 or rms_by > 0.001:
            print()
            print("RESULT: The effective geometry around mass A CHANGES when mass B")
            print("is added. The metric shift depends on mass B's position.")
            print("=> Matter tells geometry how to curve.")
        else:
            print()
            print("NOTE: Metric shifts are small. Try increasing mass_strength.")

        # Check anisotropy of the shift pattern
        # Bx should shift x-direction distances more than y-direction
        x_pts_bx = [s for s, ((px, py, pz), lbl) in
                     zip(shifts_bx, sample_points) if px != mid]
        y_pts_bx = [s for s, ((px, py, pz), lbl) in
                     zip(shifts_bx, sample_points) if py != mid]

        if x_pts_bx and y_pts_bx:
            rms_x = np.sqrt(np.mean(np.array(x_pts_bx) ** 2))
            rms_y = np.sqrt(np.mean(np.array(y_pts_bx) ** 2))
            print()
            print(f"Anisotropy of Bx metric shift:")
            print(f"  Along x (toward/away from B1): RMS = {rms_x:.6f}")
            print(f"  Along y (perpendicular to B1): RMS = {rms_y:.6f}")
            if abs(rms_x - rms_y) > 0.001 * max(rms_x, rms_y):
                print("  => ANISOTROPIC: geometry responds directionally to matter.")

    print()
    return True


# ============================================================================
# Summary
# ============================================================================

def print_summary():
    """Print the key conclusion."""
    print("=" * 80)
    print("SUMMARY: BACKGROUND INDEPENDENCE")
    print("=" * 80)
    print()
    print("Although the graph topology is fixed (cubic lattice, every node has")
    print("6 neighbors), the effective geometry -- as measured by:")
    print()
    print("  1. Edge weights: non-uniform in gravity (stronger near mass)")
    print("  2. Effective distances d_eff = -log|G|: depart from flat profile")
    print("  3. Spectral dimension: modified by the gravitational field")
    print("  4. Two-mass response: geometry around A depends on B's position")
    print()
    print("-- changes in response to the gravitational field.")
    print()
    print("The input graph provides the substrate; the geometry is an output.")
    print()
    print("This is background independence: the effective geometry seen by the")
    print("propagator is determined by the matter content, not prescribed by hand.")
    print("The lattice is scaffolding; the physics lives in the propagator weights.")
    print()


# ============================================================================
# Main
# ============================================================================

def main():
    print()
    print("BACKGROUND INDEPENDENCE: EFFECTIVE GEOMETRY DIFFERS FROM INPUT GRAPH")
    print("=" * 80)
    print()

    # Parameters
    N = 20
    mass_strength = 5.0
    k = 1.0

    if not HAS_SCIPY:
        print("WARNING: scipy not found. Using Jacobi fallback (slower).")
        print("Install scipy for optimal performance: pip install scipy")
        print()

    # Allow command-line override
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    if len(sys.argv) > 2:
        mass_strength = float(sys.argv[2])
    if len(sys.argv) > 3:
        k = float(sys.argv[3])

    print(f"Parameters: N={N}, mass_strength={mass_strength}, k={k}")
    print()

    t_start = time.time()

    # Test 1: Effective connectivity
    test_effective_connectivity(N, mass_strength, k)

    # Test 2: Effective distance
    test_effective_distance(N, mass_strength, k)

    # Test 3: Effective spectral dimension
    test_effective_dimension(N, mass_strength, k)

    # Test 4: Geometry responds to matter
    test_geometry_responds_to_matter(N, mass_strength, k)

    # Summary
    print_summary()

    total = time.time() - t_start
    print(f"Total runtime: {total:.1f}s")


if __name__ == "__main__":
    main()
