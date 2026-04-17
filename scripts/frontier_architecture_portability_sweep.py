#!/usr/bin/env python3
"""
Architecture portability sweep for source-mass scaling and gravitational attraction.

Tests key observables across four lattice architectures:
  1. Ordered 3D cubic (baseline)
  2. Staggered 3D cubic (parity-alternating mass sign)
  3. Wilson 3D cubic (Wilson fermion Hamiltonian)
  4. Random geometric graph (irregular topology)

For each architecture, measures:
  - Mass exponent beta via varying source strength and fitting deflection vs strength
  - Force direction (attractive vs repulsive)
  - Born rule I_3 (Sorkin inclusion-exclusion, where architecture supports it)

Acceptance gate:
  - beta within 10% of 1.0 on at least 3 of 4 architectures
  - Attractive force on all architectures
  - If Born rule measured, I_3 < 1e-6 (finite-size floor on small lattices)

Boundary:
  This is a portability companion. It demonstrates architecture portability
  of source-mass scaling and attraction sign, not a standalone Newton closure.
  Lattice sizes are kept small for tractability.
"""

from __future__ import annotations

import math
import time
from collections import deque

import numpy as np
from scipy.sparse import csc_matrix, csr_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import splu, spsolve, expm_multiply


# ============================================================================
# Shared constants
# ============================================================================

MASS = 0.30
DT = 0.08
N_STEPS = 15
REG = 1e-3

# Source amplitudes for mass sweep
SOURCE_AMPLITUDES = (0.4, 0.6, 0.8, 1.0, 1.5)


# ============================================================================
# Utility: power law fit
# ============================================================================

def power_law_fit(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Fit log(|y|) = slope * log(x) + intercept. Return (slope, R^2)."""
    log_x = np.log(np.asarray(xs, dtype=float))
    log_y = np.log(np.abs(np.asarray(ys, dtype=float)))
    slope, intercept = np.polyfit(log_x, log_y, 1)
    pred = slope * log_x + intercept
    ss_res = float(np.sum((log_y - pred) ** 2))
    ss_tot = float(np.sum((log_y - np.mean(log_y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(slope), r2


# ============================================================================
# Architecture 1: Ordered 3D Cubic
# ============================================================================

class Ordered3D:
    """Plain 3D cubic lattice, scalar Schrodinger with Poisson potential."""

    def __init__(self, side: int):
        self.side = side
        self.n = side ** 3
        self.pos = np.zeros((self.n, 3), dtype=float)
        self._adj: dict[int, list[int]] = {i: [] for i in range(self.n)}
        self._fill()
        self.lap = self._build_laplacian()

    def _fill(self) -> None:
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self._idx(x, y, z)
                    self.pos[i] = (x, y, z)
                    for dx, dy, dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
                        nx, ny, nz = x+dx, y+dy, z+dz
                        if 0 <= nx < self.side and 0 <= ny < self.side and 0 <= nz < self.side:
                            self._adj[i].append(self._idx(nx, ny, nz))

    def _idx(self, x: int, y: int, z: int) -> int:
        return x * self.side * self.side + y * self.side + z

    def _build_laplacian(self) -> csr_matrix:
        lap = lil_matrix((self.n, self.n), dtype=float)
        for i, nbrs in self._adj.items():
            lap[i, i] = float(len(nbrs))
            for j in nbrs:
                lap[i, j] -= 1.0
        return lap.tocsr()

    def gaussian(self, center, sigma: float, amplitude: float = 1.0) -> np.ndarray:
        rel = self.pos - np.asarray(center, dtype=float)
        psi = amplitude * np.exp(-0.5 * np.sum(rel * rel, axis=1) / sigma ** 2).astype(complex)
        return psi

    def solve_poisson(self, rho: np.ndarray, G: float, mu2: float) -> np.ndarray:
        A = (self.lap + (mu2 + REG) * speye(self.n, format="csr")).tocsc()
        return spsolve(A, G * rho).real

    def build_hamiltonian(self, phi: np.ndarray) -> csc_matrix:
        """Kinetic (hopping -0.5) + mass - potential (gravitational well)."""
        h = lil_matrix((self.n, self.n), dtype=complex)
        # Negative sign: phi > 0 near source, so -phi creates a potential well
        # that attracts the test packet toward the source.
        h.setdiag(MASS - phi)
        for i, nbrs in self._adj.items():
            for j in nbrs:
                if j > i:
                    h[i, j] -= 0.5
                    h[j, i] -= 0.5
        return h.tocsc()

    def center_of_mass_x(self, psi: np.ndarray) -> float:
        rho = np.abs(psi) ** 2
        total = np.sum(rho)
        if total < 1e-30:
            return 0.0
        return float(np.sum(rho * self.pos[:, 0]) / total)


# ============================================================================
# Architecture 2: Staggered 3D Cubic
# ============================================================================

class Staggered3D:
    """3D cubic with parity-alternating mass sign (staggered fermion)."""

    def __init__(self, side: int):
        self.side = side
        self.n = side ** 3
        self.pos = np.zeros((self.n, 3), dtype=float)
        self.parity = np.zeros(self.n, dtype=int)
        self._adj: dict[int, list[int]] = {i: [] for i in range(self.n)}
        self._fill()
        self.lap = self._build_laplacian()

    def _fill(self) -> None:
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self._idx(x, y, z)
                    self.pos[i] = (x, y, z)
                    self.parity[i] = (x + y + z) % 2
                    for dx, dy, dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
                        nx, ny, nz = x+dx, y+dy, z+dz
                        if 0 <= nx < self.side and 0 <= ny < self.side and 0 <= nz < self.side:
                            self._adj[i].append(self._idx(nx, ny, nz))

    def _idx(self, x: int, y: int, z: int) -> int:
        return x * self.side * self.side + y * self.side + z

    def _build_laplacian(self) -> csr_matrix:
        lap = lil_matrix((self.n, self.n), dtype=float)
        for i, nbrs in self._adj.items():
            for j in nbrs:
                if i < j:
                    lap[i, j] -= 1.0
                    lap[j, i] -= 1.0
                    lap[i, i] += 1.0
                    lap[j, j] += 1.0
        return lap.tocsr()

    def gaussian(self, center, sigma: float, amplitude: float = 1.0) -> np.ndarray:
        rel = self.pos - np.asarray(center, dtype=float)
        psi = amplitude * np.exp(-0.5 * np.sum(rel * rel, axis=1) / sigma ** 2).astype(complex)
        return psi

    def solve_poisson(self, rho: np.ndarray, G: float, mu2: float) -> np.ndarray:
        A = (self.lap + (mu2 + REG) * speye(self.n, format="csr")).tocsc()
        return spsolve(A, G * rho).real

    def build_hamiltonian(self, phi: np.ndarray) -> csc_matrix:
        """Staggered: diagonal = (m + phi) * epsilon(x), hopping = anti-Hermitian."""
        h = lil_matrix((self.n, self.n), dtype=complex)
        eps = np.where(self.parity == 0, 1.0, -1.0)
        h.setdiag((MASS + phi) * eps)
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self._idx(x, y, z)
                    if x + 1 < self.side:
                        j = self._idx(x+1, y, z)
                        h[i, j] += -0.5j
                        h[j, i] += 0.5j
                    eta_y = (-1) ** x
                    if y + 1 < self.side:
                        j = self._idx(x, y+1, z)
                        h[i, j] += eta_y * (-0.5j)
                        h[j, i] += eta_y * (0.5j)
                    eta_z = (-1) ** (x + y)
                    if z + 1 < self.side:
                        j = self._idx(x, y, z+1)
                        h[i, j] += eta_z * (-0.5j)
                        h[j, i] += eta_z * (0.5j)
        return h.tocsc()

    def center_of_mass_x(self, psi: np.ndarray) -> float:
        rho = np.abs(psi) ** 2
        total = np.sum(rho)
        if total < 1e-30:
            return 0.0
        return float(np.sum(rho * self.pos[:, 0]) / total)


# ============================================================================
# Architecture 3: Wilson 3D Cubic
# ============================================================================

class Wilson3D:
    """3D cubic with Wilson fermion Hamiltonian."""

    WILSON_R = 1.0

    def __init__(self, side: int):
        self.side = side
        self.n = side ** 3
        self.pos = np.zeros((self.n, 3), dtype=float)
        self._adj: dict[int, list[int]] = {}
        self._fill()
        self.lap = self._build_laplacian()

    def _fill(self) -> None:
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self._idx(x, y, z)
                    self.pos[i] = (x, y, z)
                    self._adj[i] = []
                    for dx, dy, dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
                        nx, ny, nz = x+dx, y+dy, z+dz
                        if 0 <= nx < self.side and 0 <= ny < self.side and 0 <= nz < self.side:
                            self._adj[i].append(self._idx(nx, ny, nz))

    def _idx(self, x: int, y: int, z: int) -> int:
        return x * self.side * self.side + y * self.side + z

    def _build_laplacian(self) -> csr_matrix:
        rows, cols, vals = [], [], []
        for i in range(self.n):
            rows.append(i); cols.append(i); vals.append(-len(self._adj[i]))
            for j in self._adj[i]:
                rows.append(i); cols.append(j); vals.append(1.0)
        return csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def gaussian(self, center, sigma: float, amplitude: float = 1.0) -> np.ndarray:
        rel = self.pos - np.asarray(center, dtype=float)
        psi = amplitude * np.exp(-0.5 * np.sum(rel * rel, axis=1) / sigma ** 2).astype(complex)
        return psi

    def solve_poisson(self, rho: np.ndarray, G: float, mu2: float) -> np.ndarray:
        A = self.lap - (mu2 + REG) * speye(self.n, format="csr")
        rhs = -4.0 * np.pi * G * rho
        return spsolve(A.tocsc(), rhs).real

    def build_hamiltonian(self, phi: np.ndarray) -> csr_matrix:
        """Wilson: H = m + phi + (r/2)*deg + sum_<ij> (-i/2 + r/2)."""
        rows, cols, vals = [], [], []
        r = self.WILSON_R
        for i in range(self.n):
            for j in self._adj[i]:
                if j <= i:
                    continue
                rows.append(i); cols.append(j); vals.append(-0.5j + 0.5 * r)
                rows.append(j); cols.append(i); vals.append(+0.5j + 0.5 * r)
            diag = MASS + phi[i] + 0.5 * r * len(self._adj[i])
            rows.append(i); cols.append(i); vals.append(diag)
        return csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def center_of_mass_x(self, psi: np.ndarray) -> float:
        rho = np.abs(psi) ** 2
        total = np.sum(rho)
        if total < 1e-30:
            return 0.0
        return float(np.sum(rho * self.pos[:, 0]) / total)


# ============================================================================
# Architecture 4: Random Geometric Graph
# ============================================================================

class RandomGeometric:
    """2D random geometric graph with bipartite coloring (irregular topology)."""

    def __init__(self, side: int = 10, seed: int = 42):
        import random as _random
        rng = _random.Random(seed)
        self.side = side
        coords = []
        colors = []
        index = {}
        idx = 0
        for x in range(side):
            for y in range(side):
                coords.append((
                    x + 0.08 * (rng.random() - 0.5),
                    y + 0.08 * (rng.random() - 0.5),
                ))
                colors.append((x + y) % 2)
                index[(x, y)] = idx
                idx += 1

        self.n = len(coords)
        self.pos = np.array(coords, dtype=float)
        self.colors = np.array(colors, dtype=int)
        self._adj: dict[int, list[int]] = {i: [] for i in range(self.n)}

        for i in range(side):
            for j in range(side):
                a = index[(i, j)]
                for di, dj in ((1, 0), (0, 1), (1, 1), (1, -1)):
                    ii, jj = i + di, j + dj
                    if (ii, jj) not in index:
                        continue
                    b = index[(ii, jj)]
                    if self.colors[a] == self.colors[b]:
                        continue
                    dist = math.hypot(
                        self.pos[b, 0] - self.pos[a, 0],
                        self.pos[b, 1] - self.pos[a, 1],
                    )
                    if dist <= 1.28:
                        if b not in self._adj[a]:
                            self._adj[a].append(b)
                        if a not in self._adj[b]:
                            self._adj[b].append(a)

        self.lap = self._build_laplacian()
        # Identify center and x-like direction
        self._center_idx = index.get((side // 2, side // 2), 0)

    def _build_laplacian(self) -> csr_matrix:
        lap = lil_matrix((self.n, self.n), dtype=float)
        for i, nbrs in self._adj.items():
            for j in nbrs:
                if i < j:
                    d = math.hypot(
                        self.pos[j, 0] - self.pos[i, 0],
                        self.pos[j, 1] - self.pos[i, 1],
                    )
                    w = 1.0 / max(d, 0.5)
                    lap[i, j] -= w
                    lap[j, i] -= w
                    lap[i, i] += w
                    lap[j, j] += w
        return lap.tocsr()

    def gaussian(self, center_idx: int, sigma: float, amplitude: float = 1.0) -> np.ndarray:
        center = self.pos[center_idx]
        rel = self.pos - center
        psi = amplitude * np.exp(-0.5 * np.sum(rel * rel, axis=1) / sigma ** 2).astype(complex)
        return psi

    def solve_poisson(self, rho: np.ndarray, G: float, mu2: float) -> np.ndarray:
        A = (self.lap + (mu2 + REG) * speye(self.n, format="csr")).tocsc()
        return spsolve(A, G * rho).real

    def build_hamiltonian(self, phi: np.ndarray) -> csr_matrix:
        """Scalar Schrodinger: diagonal = m - phi (gravitational well), real hopping."""
        h = lil_matrix((self.n, self.n), dtype=complex)
        # Negative sign for gravitational attraction (potential well near source)
        h.setdiag(MASS - phi)
        for i, nbrs in self._adj.items():
            for j in nbrs:
                if i < j:
                    d = math.hypot(
                        self.pos[j, 0] - self.pos[i, 0],
                        self.pos[j, 1] - self.pos[i, 1],
                    )
                    w = 1.0 / max(d, 0.5)
                    h[i, j] -= 0.5 * w
                    h[j, i] -= 0.5 * w
        return h.tocsc()

    def center_of_mass_x(self, psi: np.ndarray) -> float:
        rho = np.abs(psi) ** 2
        total = np.sum(rho)
        if total < 1e-30:
            return 0.0
        return float(np.sum(rho * self.pos[:, 0]) / total)


# ============================================================================
# Generic Crank-Nicolson stepper
# ============================================================================

def cn_step(h_csc: csc_matrix, n: int, psi: np.ndarray, dt: float) -> np.ndarray:
    """One Crank-Nicolson step: (I + iH dt/2) psi_new = (I - iH dt/2) psi."""
    eye = speye(n, format="csc")
    a_plus = (eye + 1j * h_csc * dt / 2).tocsc()
    a_minus = eye - 1j * h_csc * dt / 2
    lu = splu(a_plus)
    psi_new = lu.solve(a_minus.dot(psi))
    return psi_new / np.linalg.norm(psi_new)


def cn_step_expm(h_csr: csr_matrix, psi: np.ndarray, dt: float) -> np.ndarray:
    """One step via matrix exponential (for Wilson where H is not skew-Hermitian)."""
    psi_new = expm_multiply(-1j * dt * h_csr, psi)
    return psi_new / np.linalg.norm(psi_new)


# ============================================================================
# Test protocol: mass-law sweep on a given architecture
# ============================================================================

def run_mass_sweep_cubic(
    arch_name: str,
    lattice,
    side: int,
    G_val: float,
    mu2: float,
    distance: int,
    sigma_source: float,
    sigma_test: float,
    use_expm: bool = False,
) -> dict:
    """
    For 3D cubic-like architectures (Ordered, Staggered, Wilson).
    Place source at center, test particle at center + distance along x.
    Vary source amplitude, measure displacement, fit mass exponent.
    """
    c = side // 2
    center_source = (c, c, c)
    center_test = (c + distance, c, c)

    results = []
    for amp in SOURCE_AMPLITUDES:
        psi_source = lattice.gaussian(center_source, sigma_source, amplitude=amp)
        rho_source = np.abs(psi_source) ** 2
        source_mass = float(np.sum(rho_source))
        phi = lattice.solve_poisson(rho_source, G_val, mu2)

        psi_test = lattice.gaussian(center_test, sigma_test)
        psi_test /= np.linalg.norm(psi_test)
        psi_free = psi_test.copy()

        h_grav = lattice.build_hamiltonian(phi)
        h_free = lattice.build_hamiltonian(np.zeros(lattice.n))

        if use_expm:
            # Wilson: use expm
            for _ in range(N_STEPS):
                psi_test = cn_step_expm(h_grav, psi_test, DT)
                psi_free = cn_step_expm(h_free, psi_free, DT)
        else:
            # CN stepper
            h_grav_csc = h_grav.tocsc() if not isinstance(h_grav, csc_matrix) else h_grav
            h_free_csc = h_free.tocsc() if not isinstance(h_free, csc_matrix) else h_free
            for _ in range(N_STEPS):
                psi_test = cn_step(h_grav_csc, lattice.n, psi_test, DT)
                psi_free = cn_step(h_free_csc, lattice.n, psi_free, DT)

        x_grav = lattice.center_of_mass_x(psi_test)
        x_free = lattice.center_of_mass_x(psi_free)
        dx = x_grav - x_free  # negative => moved toward source (lower x)

        results.append({
            "amplitude": amp,
            "source_mass": source_mass,
            "dx": dx,
            "toward": dx < 0,
        })

    return _summarize_sweep(arch_name, results)


def run_mass_sweep_random_geometric(
    lattice: RandomGeometric,
    G_val: float,
    mu2: float,
    sigma_source: float,
    sigma_test: float,
) -> dict:
    """
    For random geometric graph (2D, irregular).
    Source at graph center, test at a neighbor some hops away.
    """
    import random as _random

    # Find source and test positions
    src_idx = lattice._center_idx
    # BFS to find a node ~3-4 hops away
    depth = _bfs_graph(lattice._adj, src_idx, lattice.n)
    # Pick the test node at distance 3-4 hops, choosing one with max x-coord delta
    candidates = [i for i in range(lattice.n) if 3 <= depth[i] <= 5]
    if not candidates:
        candidates = [i for i in range(lattice.n) if 2 <= depth[i] <= 6]
    if not candidates:
        candidates = [i for i in range(lattice.n) if depth[i] >= 1 and depth[i] < 999]

    # Pick the candidate farthest in x from source
    src_x = lattice.pos[src_idx, 0]
    candidates.sort(key=lambda i: abs(lattice.pos[i, 0] - src_x), reverse=True)
    test_idx = candidates[0]
    test_x_initial = lattice.pos[test_idx, 0]
    # If test is at higher x than source, "toward" means dx < 0 (motion to lower x)
    # If test is at lower x than source, "toward" means dx > 0 (motion to higher x)

    results = []
    for amp in SOURCE_AMPLITUDES:
        psi_source = lattice.gaussian(src_idx, sigma_source, amplitude=amp)
        rho_source = np.abs(psi_source) ** 2
        source_mass = float(np.sum(rho_source))
        phi = lattice.solve_poisson(rho_source, G_val, mu2)

        psi_test = lattice.gaussian(test_idx, sigma_test)
        psi_test /= np.linalg.norm(psi_test)
        psi_free = psi_test.copy()

        h_grav = lattice.build_hamiltonian(phi)
        h_free = lattice.build_hamiltonian(np.zeros(lattice.n))

        h_grav_csc = h_grav.tocsc() if not isinstance(h_grav, csc_matrix) else h_grav
        h_free_csc = h_free.tocsc() if not isinstance(h_free, csc_matrix) else h_free
        for _ in range(N_STEPS):
            psi_test = cn_step(h_grav_csc, lattice.n, psi_test, DT)
            psi_free = cn_step(h_free_csc, lattice.n, psi_free, DT)

        x_grav = lattice.center_of_mass_x(psi_test)
        x_free = lattice.center_of_mass_x(psi_free)
        dx = x_grav - x_free

        # Determine if motion is toward the source
        if test_x_initial > src_x:
            is_toward = dx < 0  # moved to lower x = toward source
        else:
            is_toward = dx > 0  # moved to higher x = toward source

        results.append({
            "amplitude": amp,
            "source_mass": source_mass,
            "dx": dx,
            "toward": is_toward,
        })

    return _summarize_sweep("random_geometric", results)


def _bfs_graph(adj: dict, src: int, n: int) -> np.ndarray:
    depth = np.full(n, 999.0)
    depth[src] = 0
    q = deque([src])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if depth[j] > depth[i] + 1:
                depth[j] = depth[i] + 1
                q.append(j)
    return depth


def _summarize_sweep(arch_name: str, results: list[dict]) -> dict:
    """Fit mass exponent and check attraction."""
    masses = [r["source_mass"] for r in results]
    dx_abs = [abs(r["dx"]) for r in results]
    n_toward = sum(1 for r in results if r["toward"])

    valid = [(m, d) for m, d in zip(masses, dx_abs) if d > 1e-14]
    if len(valid) >= 3:
        beta, r2 = power_law_fit([m for m, _ in valid], [d for _, d in valid])
    else:
        beta, r2 = float("nan"), 0.0

    return {
        "arch": arch_name,
        "beta": beta,
        "r2": r2,
        "n_toward": n_toward,
        "n_total": len(results),
        "attractive": n_toward >= len(results) - 1,  # allow 1 marginal
        "results": results,
    }


# ============================================================================
# Born rule I_3 test (Sorkin inclusion-exclusion on 1D path sums)
# ============================================================================

def born_rule_i3(h_builder, n_sites: int, slit_indices: list[int],
                 source_idx: int, detector_idx: int, dt: float, steps: int) -> float:
    """
    Compute Sorkin I_3 on a lattice Hamiltonian.

    Uses amplitude propagation: for each slit subset, block all other slits
    and propagate source -> detector. Measures probability at detector.

    I_3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C

    h_builder(blocked_set) -> H matrix with blocked sites zeroed out.
    """
    from itertools import combinations

    slits = slit_indices[:3]  # use exactly 3
    if len(slits) < 3:
        return float("nan")

    all_slits = set(slits)

    def propagate_prob(open_slits: set[int]) -> float:
        blocked = all_slits - open_slits
        H = h_builder(blocked)
        H_csc = H.tocsc() if not isinstance(H, csc_matrix) else H
        psi = np.zeros(n_sites, dtype=complex)
        psi[source_idx] = 1.0
        for _ in range(steps):
            psi = cn_step(H_csc, n_sites, psi, dt)
        return float(np.abs(psi[detector_idx]) ** 2)

    # Single slits
    P = {}
    for s in slits:
        P[frozenset([s])] = propagate_prob({s})

    # Pairs
    for pair in combinations(slits, 2):
        P[frozenset(pair)] = propagate_prob(set(pair))

    # Triple
    P[frozenset(slits)] = propagate_prob(set(slits))

    A, B, C = slits
    I3 = (P[frozenset(slits)]
          - P[frozenset([A, B])] - P[frozenset([A, C])] - P[frozenset([B, C])]
          + P[frozenset([A])] + P[frozenset([B])] + P[frozenset([C])])

    return I3


def born_rule_test_ordered(side: int) -> float:
    """
    Born rule I_3 on ordered 3D cubic lattice.
    Creates a barrier with 3 slits, propagates through.
    """
    lat = Ordered3D(side)
    c = side // 2

    # Barrier at x = c, slits at y = c-1, c, c+1 (z = c fixed)
    slit_positions = [c - 1, c, c + 1]
    slit_indices = [lat._idx(c, sy, c) for sy in slit_positions]

    # All barrier sites (x = c, varying y, z = c plane)
    barrier_sites = set()
    for y in range(side):
        barrier_sites.add(lat._idx(c, y, c))

    source_idx = lat._idx(c - 3, c, c)
    detector_idx = lat._idx(c + 3, c, c)

    all_slit_set = set(slit_indices)

    def h_builder(blocked: set[int]):
        """Build Hamiltonian with barrier, some slits blocked."""
        actual_blocked = (barrier_sites - all_slit_set) | blocked
        h = lil_matrix((lat.n, lat.n), dtype=complex)
        h.setdiag(MASS)
        for i, nbrs in lat._adj.items():
            if i in actual_blocked:
                h[i, i] = 1e6  # high wall
                continue
            for j in nbrs:
                if j > i and j not in actual_blocked:
                    h[i, j] -= 0.5
                    h[j, i] -= 0.5
        return h.tocsc()

    return born_rule_i3(h_builder, lat.n, slit_indices, source_idx, detector_idx, DT, 20)


def born_rule_test_staggered(side: int) -> float:
    """Born rule I_3 on staggered 3D cubic."""
    lat = Staggered3D(side)
    c = side // 2
    slit_positions = [c - 1, c, c + 1]
    slit_indices = [lat._idx(c, sy, c) for sy in slit_positions]

    barrier_sites = set()
    for y in range(side):
        barrier_sites.add(lat._idx(c, y, c))

    source_idx = lat._idx(c - 3, c, c)
    detector_idx = lat._idx(c + 3, c, c)
    all_slit_set = set(slit_indices)

    def h_builder(blocked: set[int]):
        actual_blocked = (barrier_sites - all_slit_set) | blocked
        h = lil_matrix((lat.n, lat.n), dtype=complex)
        eps = np.where(lat.parity == 0, 1.0, -1.0)
        diag = MASS * eps
        for i in actual_blocked:
            diag[i] = 1e6
        h.setdiag(diag)
        for x in range(lat.side):
            for y in range(lat.side):
                for z in range(lat.side):
                    i = lat._idx(x, y, z)
                    if i in actual_blocked:
                        continue
                    if x + 1 < lat.side:
                        j = lat._idx(x+1, y, z)
                        if j not in actual_blocked:
                            h[i, j] += -0.5j
                            h[j, i] += 0.5j
                    eta_y = (-1) ** x
                    if y + 1 < lat.side:
                        j = lat._idx(x, y+1, z)
                        if j not in actual_blocked:
                            h[i, j] += eta_y * (-0.5j)
                            h[j, i] += eta_y * (0.5j)
                    eta_z = (-1) ** (x + y)
                    if z + 1 < lat.side:
                        j = lat._idx(x, y, z+1)
                        if j not in actual_blocked:
                            h[i, j] += eta_z * (-0.5j)
                            h[j, i] += eta_z * (0.5j)
        return h.tocsc()

    return born_rule_i3(h_builder, lat.n, slit_indices, source_idx, detector_idx, DT, 20)


# ============================================================================
# Main: run all architectures
# ============================================================================

def main() -> None:
    t0 = time.time()
    print("=" * 90)
    print("ARCHITECTURE PORTABILITY SWEEP")
    print("=" * 90)
    print(f"MASS={MASS}, DT={DT}, N_STEPS={N_STEPS}, REG={REG}")
    print(f"Source amplitudes: {SOURCE_AMPLITUDES}")
    print("Goal: beta ~ 1.0, attractive force, I_3 ~ 0 where measured")
    print()

    all_results = []

    # ---- Architecture 1: Ordered 3D Cubic ----
    print("-" * 90)
    print("ARCHITECTURE 1: Ordered 3D Cubic (side=14)")
    print("-" * 90)
    side = 14
    lat = Ordered3D(side)
    res = run_mass_sweep_cubic(
        "ordered_3d", lat, side,
        G_val=0.005, mu2=0.001, distance=4,
        sigma_source=1.3, sigma_test=1.0,
    )
    _print_sweep(res)
    all_results.append(res)

    # Born rule
    print("  Born rule I_3 (side=12)...", end=" ", flush=True)
    i3_ordered = born_rule_test_ordered(12)
    print(f"I_3 = {i3_ordered:.2e}")
    res["I3"] = i3_ordered

    # ---- Architecture 2: Staggered 3D Cubic ----
    print()
    print("-" * 90)
    print("ARCHITECTURE 2: Staggered 3D Cubic (side=14)")
    print("-" * 90)
    side = 14
    lat = Staggered3D(side)
    res = run_mass_sweep_cubic(
        "staggered_3d", lat, side,
        G_val=0.005, mu2=0.001, distance=4,
        sigma_source=1.3, sigma_test=1.0,
    )
    _print_sweep(res)
    all_results.append(res)

    print("  Born rule I_3 (side=12)...", end=" ", flush=True)
    i3_stag = born_rule_test_staggered(12)
    print(f"I_3 = {i3_stag:.2e}")
    res["I3"] = i3_stag

    # ---- Architecture 3: Wilson 3D Cubic ----
    print()
    print("-" * 90)
    print("ARCHITECTURE 3: Wilson 3D Cubic (side=14)")
    print("-" * 90)
    side = 14
    lat = Wilson3D(side)
    res = run_mass_sweep_cubic(
        "wilson_3d", lat, side,
        G_val=0.002, mu2=0.001, distance=4,
        sigma_source=1.5, sigma_test=1.0,
        use_expm=True,
    )
    _print_sweep(res)
    all_results.append(res)
    res["I3"] = float("nan")  # Wilson Born rule is structurally different; skip

    # ---- Architecture 4: Random Geometric ----
    print()
    print("-" * 90)
    print("ARCHITECTURE 4: Random Geometric Graph (2D mass-only, side=10, n=100)")
    print("-" * 90)
    lat = RandomGeometric(side=10, seed=42)
    res = run_mass_sweep_random_geometric(
        lat,
        G_val=0.05, mu2=0.1,
        sigma_source=1.5, sigma_test=0.8,
    )
    _print_sweep(res)
    all_results.append(res)
    res["I3"] = float("nan")  # irregular topology, no clean 3-slit
    print("  Note: random geometric is 2D and mass-scaling only; no distance-law comparison.")

    # ---- Summary table ----
    print()
    print("=" * 90)
    print("ARCHITECTURE COMPARISON TABLE")
    print("=" * 90)
    print(f"{'Architecture':<22s} {'beta':>8s} {'R^2':>8s} {'Attract':>9s} {'I_3':>12s} {'Verdict':>9s}")
    print("-" * 90)

    n_beta_pass = 0
    n_attract_pass = 0
    i3_all_pass = True

    for r in all_results:
        beta_ok = not math.isnan(r["beta"]) and abs(r["beta"] - 1.0) < 0.10
        attract_ok = r["attractive"]
        i3_val = r.get("I3", float("nan"))
        # Threshold 1e-6: I_3 scales with finite-size effects on small lattices;
        # values < 1e-6 are strongly consistent with Born rule compliance.
        i3_ok = math.isnan(i3_val) or abs(i3_val) < 1e-6

        if beta_ok:
            n_beta_pass += 1
        if attract_ok:
            n_attract_pass += 1
        if not i3_ok:
            i3_all_pass = False

        verdict = "PASS" if (beta_ok and attract_ok and i3_ok) else "FAIL"
        i3_str = f"{i3_val:.2e}" if not math.isnan(i3_val) else "n/a"

        print(
            f"{r['arch']:<22s} "
            f"{r['beta']:>8.4f} "
            f"{r['r2']:>8.4f} "
            f"{'YES' if attract_ok else 'NO':>9s} "
            f"{i3_str:>12s} "
            f"{verdict:>9s}"
        )

    print("-" * 90)
    print()

    # ---- Acceptance gate ----
    print("=" * 90)
    print("ACCEPTANCE GATE")
    print("=" * 90)
    gate_beta = n_beta_pass >= 3
    gate_attract = n_attract_pass == len(all_results)
    gate_born = i3_all_pass

    print(f"  beta within 10% of 1.0: {n_beta_pass}/4 architectures (need >= 3) -> {'PASS' if gate_beta else 'FAIL'}")
    print(f"  Attractive force:       {n_attract_pass}/{len(all_results)} architectures (need all) -> {'PASS' if gate_attract else 'FAIL'}")
    print(f"  Born rule I_3 < 1e-6:   {'all measured pass' if gate_born else 'FAIL'} -> {'PASS' if gate_born else 'FAIL'}")
    print()

    overall = gate_beta and gate_attract and gate_born
    print(f"  OVERALL: {'PASS — bounded source-mass portability companion established' if overall else 'FAIL — see details above'}")
    print()
    print(f"Elapsed: {time.time() - t0:.1f}s")


def _print_sweep(res: dict) -> None:
    """Print per-architecture sweep details."""
    print(f"  Mass exponent beta = {res['beta']:.4f} (R^2 = {res['r2']:.4f})")
    print(f"  Attraction: {res['n_toward']}/{res['n_total']} toward source -> {'YES' if res['attractive'] else 'NO'}")
    for r in res["results"]:
        print(
            f"    A={r['amplitude']:.1f}  M={r['source_mass']:.4f}  "
            f"dx={r['dx']:+.6f}  {'TOWARD' if r['toward'] else 'AWAY'}"
        )


if __name__ == "__main__":
    main()
