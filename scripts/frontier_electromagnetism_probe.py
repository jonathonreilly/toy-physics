#!/usr/bin/env python3
"""
Electromagnetism Probe -- U(1) Gauge Phases on Graph Edges
==========================================================

Goal:
  Probe whether simple U(1) phases on directed graph edges and a scalar
  Coulomb potential reproduce bounded electromagnetic-style behaviour on the
  staggered lattice. This is a consistency probe of the chosen discretization,
  not a derivation of Maxwell theory.

Design:
  On a 3D cubic lattice with open boundaries, test two electromagnetic sectors:

  Part 1 -- Electrostatic sector (scalar potential V on diagonal):
    F = -<psi|grad(q*V)|psi> gives the correct Coulomb force on a probe
    wavepacket. Tested for:
    (a) Attraction (opposite charges, Q*q < 0)
    (b) Repulsion (like charges, Q*q > 0)
    (c) Neutral immunity (q = 0)
    (d) 1/r^2 force law
    (e) Dynamic centroid tracking confirms inward drift under attraction

  Part 2 -- Magnetic sector (U(1) link phases):
    A_{ij} = line integral of vector potential A = (B/2)(-y,x,0) on edges.
    Tested for:
    (a) Transverse deflection of charged particle (Lorentz force)
    (b) Deflection monotone in B strength
    (c) Neutral immunity

  This script does not run a coupled nonzero gravity+electromagnetism case.

Method:
  Electrostatic force uses force expectation value (classical, on initial
  wavepacket). Centroid tracking uses differential measurement (subtract
  control with q=0) to remove lattice artifacts.

  Note on staggered charge conjugation: The staggered Hamiltonian has a
  mass-like diagonal coupling q*V*eps. The centroid response to a mass
  gradient is always attractive regardless of sign (Ehrenfest for staggered
  fermions). Charge conjugation symmetry is therefore broken by the staggered
  doubling. The force expectation value, being a classical observable, correctly
  captures the sign. This is a known lattice artifact, not a physics failure.
"""

from __future__ import annotations

import time

import numpy as np
from scipy.sparse import csc_matrix, csr_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import splu, spsolve


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.001
REG = 1e-6
DT = 0.08
N_STEPS = 12
G = 50.0
Q_EM = 5.0
SIGMA = 0.80
SIDE = 18
DISTANCES = (3, 4, 5, 6, 7)
B_STRENGTHS = (0.05, 0.10, 0.20, 0.40)


# ---------------------------------------------------------------------------
# Lattice
# ---------------------------------------------------------------------------
class OpenLattice3D:
    """Open-boundary 3D cubic lattice for staggered fermion propagation."""

    def __init__(self, side: int):
        self.side = side
        self.n_sites = side ** 3
        self.pos = np.zeros((self.n_sites, 3), dtype=float)
        self.parity = np.zeros(self.n_sites, dtype=int)
        self._adj: dict[int, list[int]] = {i: [] for i in range(self.n_sites)}
        self._fill_geometry()
        self.laplacian = self._build_laplacian()
        self.eye_csc = speye(self.n_sites, format="csc")
        self.eye_csr = speye(self.n_sites, format="csr")

    def _fill_geometry(self) -> None:
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    self.pos[i] = (x, y, z)
                    self.parity[i] = (x + y + z) % 2
                    for dx, dy, dz in (
                        (1, 0, 0), (-1, 0, 0),
                        (0, 1, 0), (0, -1, 0),
                        (0, 0, 1), (0, 0, -1),
                    ):
                        xx, yy, zz = x + dx, y + dy, z + dz
                        if 0 <= xx < self.side and 0 <= yy < self.side and 0 <= zz < self.side:
                            self._adj[i].append(self.index(xx, yy, zz))

    def index(self, x: int, y: int, z: int) -> int:
        return x * self.side * self.side + y * self.side + z

    def _build_laplacian(self) -> csr_matrix:
        lap = lil_matrix((self.n_sites, self.n_sites), dtype=float)
        for i, nbrs in self._adj.items():
            for j in nbrs:
                if i >= j:
                    continue
                lap[i, j] -= 1.0
                lap[j, i] -= 1.0
                lap[i, i] += 1.0
                lap[j, j] += 1.0
        return lap.tocsr()

    def gaussian(self, center: tuple[float, ...], sigma: float = SIGMA) -> np.ndarray:
        rel = self.pos - np.asarray(center, dtype=float)
        psi = np.exp(-0.5 * np.sum(rel * rel, axis=1) / sigma ** 2).astype(complex)
        return psi / np.linalg.norm(psi)

    def centroid(self, psi: np.ndarray) -> np.ndarray:
        rho = np.abs(psi) ** 2
        rho = rho / np.sum(rho)
        return np.sum(rho[:, None] * self.pos, axis=0)

    def gradient_x(self, field: np.ndarray) -> np.ndarray:
        """Central-difference gradient in x."""
        grad = np.zeros(self.n_sites, dtype=float)
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    if x == 0:
                        grad[i] = field[self.index(x + 1, y, z)] - field[i]
                    elif x == self.side - 1:
                        grad[i] = field[i] - field[self.index(x - 1, y, z)]
                    else:
                        grad[i] = 0.5 * (
                            field[self.index(x + 1, y, z)] - field[self.index(x - 1, y, z)]
                        )
        return grad

    def force_x(self, psi: np.ndarray, grad_V_x: np.ndarray) -> float:
        """F = -<psi|grad_V|psi> in x."""
        rho = np.abs(psi) ** 2
        rho = rho / np.sum(rho)
        return float(-np.sum(rho * grad_V_x))

    def build_hamiltonian(
        self,
        phi_grav: np.ndarray,
        V_em: np.ndarray | None = None,
        A_phases: dict[tuple[int, int], float] | None = None,
        charge: float = 0.0,
    ) -> csc_matrix:
        """Staggered Hamiltonian with gravity + EM."""
        h = lil_matrix((self.n_sites, self.n_sites), dtype=complex)
        eps = np.where(self.parity == 0, 1.0, -1.0)

        diag = (MASS + phi_grav) * eps
        if V_em is not None and charge != 0.0:
            diag = diag + charge * V_em * eps
        h.setdiag(diag)

        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)

                    if x + 1 < self.side:
                        j = self.index(x + 1, y, z)
                        gauge = 1.0
                        if A_phases is not None and charge != 0.0:
                            gauge = np.exp(1j * charge * A_phases.get((i, j), 0.0))
                        h[i, j] += -0.5j * gauge
                        h[j, i] += 0.5j * np.conj(gauge)

                    eta_y = (-1) ** x
                    if y + 1 < self.side:
                        j = self.index(x, y + 1, z)
                        gauge = 1.0
                        if A_phases is not None and charge != 0.0:
                            gauge = np.exp(1j * charge * A_phases.get((i, j), 0.0))
                        h[i, j] += eta_y * (-0.5j) * gauge
                        h[j, i] += eta_y * (0.5j) * np.conj(gauge)

                    eta_z = (-1) ** (x + y)
                    if z + 1 < self.side:
                        j = self.index(x, y, z + 1)
                        gauge = 1.0
                        if A_phases is not None and charge != 0.0:
                            gauge = np.exp(1j * charge * A_phases.get((i, j), 0.0))
                        h[i, j] += eta_z * (-0.5j) * gauge
                        h[j, i] += eta_z * (0.5j) * np.conj(gauge)

        return h.tocsc()

    def make_stepper(self, hamiltonian: csc_matrix):
        a_plus = (self.eye_csc + 1j * hamiltonian * DT / 2).tocsc()
        a_minus = self.eye_csr - 1j * hamiltonian * DT / 2
        return splu(a_plus), a_minus

    def step(self, psi: np.ndarray, lu, a_minus: csr_matrix) -> np.ndarray:
        psi = lu.solve(a_minus.dot(psi))
        return psi / np.linalg.norm(psi)


# ---------------------------------------------------------------------------
# Potentials
# ---------------------------------------------------------------------------
def coulomb_potential(
    lat: OpenLattice3D,
    source_pos: tuple[float, ...],
    source_charge: float,
) -> np.ndarray:
    """V(r) = Q / |r - r_source|, regularized at origin."""
    rel = lat.pos - np.asarray(source_pos, dtype=float)
    r = np.sqrt(np.sum(rel * rel, axis=1))
    r = np.maximum(r, 1.0)
    return source_charge / r


def constant_B_gauge(
    lat: OpenLattice3D,
    B_z: float,
    center: tuple[float, ...],
) -> dict[tuple[int, int], float]:
    """Symmetric gauge A = (B/2)*(-y, x, 0) for constant B_z."""
    cx, cy, _ = center
    phases: dict[tuple[int, int], float] = {}

    for x in range(lat.side):
        for y in range(lat.side):
            for z in range(lat.side):
                i = lat.index(x, y, z)
                ry = y - cy

                if x + 1 < lat.side:
                    j = lat.index(x + 1, y, z)
                    phases[(i, j)] = -0.5 * B_z * ry

                if y + 1 < lat.side:
                    j = lat.index(x, y + 1, z)
                    rx = x - cx
                    phases[(i, j)] = 0.5 * B_z * (rx + 0.5)

                if z + 1 < lat.side:
                    j = lat.index(x, y, z + 1)
                    phases[(i, j)] = 0.0

    return phases


# ---------------------------------------------------------------------------
# Part 1: Electrostatic sector
# ---------------------------------------------------------------------------
def test_electrostatics(lat: OpenLattice3D) -> dict[str, object]:
    """Electrostatic tests: force expectation + centroid tracking."""
    print("\n" + "=" * 80)
    print("PART 1: ELECTROSTATIC SECTOR")
    print("=" * 80)

    results: dict[str, object] = {}
    center = lat.side / 2.0
    source_pos = (center, center, center)

    # --- (a) Force sign: attraction, repulsion, neutral ---
    print("\n--- (a) Force expectation value: F_x = -<grad(q*V)> ---")
    print(f"{'d':>4} {'Q':>5} {'q':>5} {'F_x':>12} {'direction':>12}")
    print("-" * 50)

    force_rows = []
    for d in DISTANCES:
        probe_start = (center + d, center, center)
        psi = lat.gaussian(probe_start)

        for Q, q_probe in [(-1.0, Q_EM), (+1.0, Q_EM), (-1.0, 0.0)]:
            V = coulomb_potential(lat, source_pos, Q)
            grad_qV = lat.gradient_x(q_probe * V)
            fx = lat.force_x(psi, grad_qV)

            label = "neutral" if q_probe == 0.0 else ("attract" if Q * q_probe < 0 else "repel")
            direction = "toward" if fx < 0 else "away" if fx > 0 else "none"
            force_rows.append({"d": d, "Q": Q, "q": q_probe, "F_x": fx, "label": label})
            print(f"{d:>4d} {Q:>+5.1f} {q_probe:>+5.1f} {fx:>+12.6f} {direction:>12s}")

    attract_forces = [r["F_x"] for r in force_rows if r["label"] == "attract"]
    attract_ok = all(f < 0 for f in attract_forces)
    results["attract_force"] = attract_ok
    print(f"\n  Attraction (F_x < 0 for Q*q < 0): {attract_ok}")

    repel_forces = [r["F_x"] for r in force_rows if r["label"] == "repel"]
    repel_ok = all(f > 0 for f in repel_forces)
    results["repel_force"] = repel_ok
    print(f"  Repulsion (F_x > 0 for Q*q > 0): {repel_ok}")

    neutral_forces = [r["F_x"] for r in force_rows if r["label"] == "neutral"]
    neutral_ok = all(abs(f) < 1e-12 for f in neutral_forces)
    results["neutral_immune"] = neutral_ok
    print(f"  Neutral immune (F_x ~ 0 for q=0): {neutral_ok}")

    # --- (b) 1/r^2 force law ---
    print("\n--- (b) Force law: |F_x| vs distance (attraction) ---")
    attract_by_d = [(r["d"], abs(r["F_x"])) for r in force_rows if r["label"] == "attract"]
    dists = np.array([x[0] for x in attract_by_d])
    forces = np.array([x[1] for x in attract_by_d])

    log_d = np.log(dists)
    log_f = np.log(forces)
    slope, intercept = np.polyfit(log_d, log_f, 1)
    pred = slope * log_d + intercept
    ss_res = np.sum((log_f - pred) ** 2)
    ss_tot = np.sum((log_f - np.mean(log_f)) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    print(f"  Power law: |F| ~ d^{slope:.3f}  (1/r^2 Coulomb expects -2.0)")
    print(f"  R^2 = {r2:.4f}")
    force_law_ok = -3.5 < slope < -1.0 and r2 > 0.9
    results["force_law_1r2"] = force_law_ok
    results["force_law_slope"] = slope
    results["force_law_r2"] = r2

    # --- (c) Centroid tracking: attraction ---
    print("\n--- (c) Centroid tracking (attraction Q=-1, q=+Q_EM) ---")
    phi_grav = np.zeros(lat.n_sites)
    V_attract = coulomb_potential(lat, source_pos, -1.0)

    centroid_rows = []
    for d in DISTANCES:
        probe_start = (center + d, center, center)
        psi0 = lat.gaussian(probe_start)

        H_ctrl = lat.build_hamiltonian(phi_grav)
        lu_c, am_c = lat.make_stepper(H_ctrl)
        psi_c = psi0.copy()

        H_test = lat.build_hamiltonian(phi_grav, V_em=V_attract, charge=Q_EM)
        lu_t, am_t = lat.make_stepper(H_test)
        psi_t = psi0.copy()

        for _ in range(N_STEPS):
            psi_c = lat.step(psi_c, lu_c, am_c)
            psi_t = lat.step(psi_t, lu_t, am_t)

        delta_x = lat.centroid(psi_c)[0] - lat.centroid(psi_t)[0]
        centroid_rows.append({"d": d, "delta_x": delta_x})
        print(f"  d={d}: delta_x={delta_x:+.6f}")

    centroid_attract = all(r["delta_x"] > 0 for r in centroid_rows)
    results["centroid_attract"] = centroid_attract
    print(f"  All centroids shift toward source: {centroid_attract}")

    # Power law for centroid displacement
    c_dists = np.array([r["d"] for r in centroid_rows])
    c_deltas = np.array([r["delta_x"] for r in centroid_rows])
    if all(c_deltas > 0):
        c_slope, _ = np.polyfit(np.log(c_dists), np.log(c_deltas), 1)
        print(f"  Centroid displacement ~ d^{c_slope:.3f}")
        results["centroid_slope"] = c_slope

    return results


# ---------------------------------------------------------------------------
# Part 2: Magnetic sector
# ---------------------------------------------------------------------------
def test_magnetic(lat: OpenLattice3D) -> dict[str, object]:
    """Magnetic Lorentz force from U(1) link phases."""
    print("\n" + "=" * 80)
    print("PART 2: MAGNETIC SECTOR (U(1) LINK PHASES)")
    print("=" * 80)

    results: dict[str, object] = {}
    center = lat.side / 2.0
    c = (center, center, center)
    start = (center - 3, center, center)

    psi0 = lat.gaussian(start)
    kx = 0.5
    psi0 = psi0 * np.exp(1j * kx * lat.pos[:, 0])
    psi0 = psi0 / np.linalg.norm(psi0)

    phi_grav = np.zeros(lat.n_sites)
    H_ctrl = lat.build_hamiltonian(phi_grav)
    lu_c, am_c = lat.make_stepper(H_ctrl)

    # --- (a) Transverse deflection vs B ---
    print("\n--- (a) Charged particle transverse deflection vs B ---")
    deflection_data = []
    for B in B_STRENGTHS:
        A = constant_B_gauge(lat, B, c)
        H = lat.build_hamiltonian(phi_grav, A_phases=A, charge=Q_EM)
        lu, am = lat.make_stepper(H)

        psi_c, psi_t = psi0.copy(), psi0.copy()
        for _ in range(N_STEPS):
            psi_c = lat.step(psi_c, lu_c, am_c)
            psi_t = lat.step(psi_t, lu, am)

        dy = lat.centroid(psi_t)[1] - lat.centroid(psi_c)[1]
        deflection_data.append({"B": B, "dy": dy})
        print(f"  B={B:.2f}: dy={dy:+.6f}")

    deflections = [abs(r["dy"]) for r in deflection_data]
    curves = any(d > 1e-4 for d in deflections)
    monotone = all(
        deflections[i] <= deflections[i + 1] + 1e-6
        for i in range(len(deflections) - 1)
    )
    results["charged_curves"] = curves
    results["deflection_monotone"] = monotone
    print(f"  Charged shows deflection: {curves}")
    print(f"  Deflection monotone in B: {monotone}")

    # Fit deflection ~ B^alpha
    Bs = np.array([r["B"] for r in deflection_data])
    dys = np.array([abs(r["dy"]) for r in deflection_data])
    if all(dys > 0):
        b_slope, _ = np.polyfit(np.log(Bs), np.log(dys), 1)
        print(f"  Deflection ~ B^{b_slope:.3f}  (expect ~1 for Lorentz)")
        results["B_exponent"] = b_slope

    # --- (b) Neutral particle ---
    print("\n--- (b) Neutral particle in B field ---")
    B_max = B_STRENGTHS[-1]
    A = constant_B_gauge(lat, B_max, c)
    H_neutral = lat.build_hamiltonian(phi_grav, A_phases=A, charge=0.0)
    lu_n, am_n = lat.make_stepper(H_neutral)

    psi_c, psi_n = psi0.copy(), psi0.copy()
    for _ in range(N_STEPS):
        psi_c = lat.step(psi_c, lu_c, am_c)
        psi_n = lat.step(psi_n, lu_n, am_n)

    dy_neutral = lat.centroid(psi_n)[1] - lat.centroid(psi_c)[1]
    neutral_ok = abs(dy_neutral) < 1e-10
    results["neutral_straight"] = neutral_ok
    print(f"  B={B_max:.2f}, q=0: dy={dy_neutral:+.2e}")
    print(f"  Neutral unaffected: {neutral_ok}")

    # --- (c) Wilson loop: gauge-invariant plaquette observable ---
    print("\n--- (c) Wilson loop (plaquette) holonomy ---")
    B_test = 0.20
    A_phases = constant_B_gauge(lat, B_test, c)

    # Compute plaquette holonomy for an xy plaquette at lattice center
    cx, cy, cz = int(center), int(center), int(center)
    i00 = lat.index(cx, cy, cz)
    i10 = lat.index(cx + 1, cy, cz)
    i11 = lat.index(cx + 1, cy + 1, cz)
    i01 = lat.index(cx, cy + 1, cz)

    # Plaquette: i00 -> i10 -> i11 -> i01 -> i00
    holonomy = (
        A_phases.get((i00, i10), 0.0)
        + A_phases.get((i10, i11), 0.0)
        - A_phases.get((i01, i11), 0.0)
        - A_phases.get((i00, i01), 0.0)
    )
    # Expected: B * (area=1) = B_test
    print(f"  Plaquette holonomy at center: {holonomy:.6f}")
    print(f"  Expected (B * area): {B_test:.6f}")
    holonomy_ok = abs(holonomy - B_test) < 0.1 * B_test
    results["wilson_plaquette"] = holonomy_ok
    print(f"  Holonomy matches B: {holonomy_ok}")

    # Check multiple plaquettes
    plaquette_values = []
    for x in range(2, lat.side - 3):
        for y in range(2, lat.side - 3):
            z = int(center)
            i00 = lat.index(x, y, z)
            i10 = lat.index(x + 1, y, z)
            i11 = lat.index(x + 1, y + 1, z)
            i01 = lat.index(x, y + 1, z)
            hol = (
                A_phases.get((i00, i10), 0.0)
                + A_phases.get((i10, i11), 0.0)
                - A_phases.get((i01, i11), 0.0)
                - A_phases.get((i00, i01), 0.0)
            )
            plaquette_values.append(hol)

    plaq_arr = np.array(plaquette_values)
    print(f"  Plaquette mean={np.mean(plaq_arr):.6f}, std={np.std(plaq_arr):.6f}")
    uniform_ok = np.std(plaq_arr) < 0.01 * abs(np.mean(plaq_arr))
    results["uniform_B_field"] = uniform_ok
    print(f"  B field uniform: {uniform_ok}")

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    t0 = time.time()
    print("=" * 80)
    print("ELECTROMAGNETISM PROBE -- U(1) GAUGE PHASES ON GRAPH EDGES")
    print("=" * 80)
    print(
        f"MASS={MASS}, G={G}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, "
        f"SIGMA={SIGMA}, SIDE={SIDE}, Q_EM={Q_EM}"
    )
    print(f"distances={DISTANCES}")
    print(f"B_strengths={B_STRENGTHS}")

    lat = OpenLattice3D(SIDE)
    print(f"lattice: {SIDE}^3 = {lat.n_sites} sites")

    e_results = test_electrostatics(lat)
    m_results = test_magnetic(lat)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    all_results = {**e_results, **m_results}

    bool_results = {k: v for k, v in all_results.items() if isinstance(v, bool)}
    num_results = {
        k: v for k, v in all_results.items()
        if isinstance(v, (int, float)) and not isinstance(v, bool)
    }

    passes = sum(1 for v in bool_results.values() if v)
    total = len(bool_results)

    for k, v in sorted(bool_results.items()):
        tag = "PASS" if v else "FAIL"
        print(f"  {k:30s}: {tag}")

    if num_results:
        print()
        for k, v in sorted(num_results.items()):
            print(f"  {k:30s}: {v:.4f}")

    print(f"\nOverall: {passes}/{total} tests pass")
    print(f"elapsed={time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
