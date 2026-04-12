#!/usr/bin/env python3
"""
Product Law Without Bilinear Ansatz
====================================

Goal:
  Demonstrate F ~ M1*M2 emerges from Poisson linearity WITHOUT any
  bilinear term V ~ M1*M2 in the Hamiltonian.

Why this script exists:
  The previous exact_two_particle_product_law.py baked M1*M2 into the
  interaction: V(x1,x2) = -G * s1 * s2 / |x1-x2|. Exact diagonalization
  then confirmed what was assumed. This script removes that circularity.

Method:
  1. TWO SEPARATE Poisson solves, one per mass:
       (L + mu^2) phi_A = G * rho_A     where rho_A = M_A * |psi_A|^2
       (L + mu^2) phi_B = G * rho_B     where rho_B = M_B * |psi_B|^2
     The mass M_i enters ONLY as a source amplitude. No M_A*M_B product.

  2. Cross-field coupling (no self-interaction):
       H_A includes phi_B only  (particle A feels B's field)
       H_B includes phi_A only  (particle B feels A's field)

  3. Force measurement from the OTHER particle's field:
       F_on_A = -M_A * integral |psi_A|^2 * grad(phi_B)
     The M_A factor comes from rho_A = M_A * |psi_A|^2 (test-mass response).
     The M_B dependence comes from phi_B ~ M_B (Poisson linearity).
     Together: F ~ M_A * M_B, but this is MEASURED, not imposed.

  4. Controls:
     a) FROZEN-SOURCE: Poisson fields from initial densities, held fixed.
        Product law should hold (pure field-linearity test).
     b) HAND-CRAFTED 1/r: Replace Poisson solve with analytic 1/r field
        centered at the partner's position. Confirms the force measurement
        pipeline is correct independent of the Poisson solver.

  5. STATIC vs DYNAMIC comparison:
     STATIC  = frozen fields, t=0 force only (purest linearity test)
     DYNAMIC = self-consistent field updates each step (tests robustness)

PStack experiment: frontier-product-law-no-ansatz
"""

from __future__ import annotations

import itertools
import time

import numpy as np
from scipy.sparse import csc_matrix, csr_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import splu


# --- lattice and physics parameters ---
SIDE = 14
BARE_MASS = 0.30
MU2 = 0.001
REG = 1e-6
DT = 0.08
N_STEPS = 6
G_COUPLING = 50.0
SIGMA = 0.80
SEPARATION = 5

# Mass values to sweep independently
MASS_VALUES = [0.10, 0.20, 0.40, 0.80]

# Acceptance thresholds
ALPHA_TOL = 0.05
BETA_TOL = 0.05
R2_MIN = 0.99
SYMMETRY_TOL = 0.02
BILINEAR_TOL = 0.05  # |gamma - 1| for the M1*M2 product test


class OpenStaggered3D:
    """Open-boundary 3D staggered lattice with separate Poisson solves."""

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
        self._poisson_op = (
            self.laplacian + (MU2 + REG) * speye(self.n_sites, format="csr")
        ).tocsc()
        self._poisson_lu = splu(self._poisson_op)

    def index(self, x: int, y: int, z: int) -> int:
        return x * self.side * self.side + y * self.side + z

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

    def gaussian(self, center: tuple[float, float, float], sigma: float = SIGMA) -> np.ndarray:
        rel = self.pos - np.asarray(center, dtype=float)
        psi = np.exp(-0.5 * np.sum(rel * rel, axis=1) / sigma ** 2).astype(complex)
        return psi / np.linalg.norm(psi)

    def solve_phi_single(self, mass: float, psi: np.ndarray) -> np.ndarray:
        """Solve Poisson for ONE particle: (L + mu^2) phi = G * M * |psi|^2.

        The mass enters ONLY as a source amplitude multiplier.
        No other particle's mass appears anywhere in this solve.
        """
        rho = mass * np.abs(psi) ** 2
        if np.allclose(rho, 0.0):
            return np.zeros(self.n_sites)
        return self._poisson_lu.solve(G_COUPLING * rho).real

    def handcrafted_1_over_r(self, center: tuple[float, float, float],
                              mass: float) -> np.ndarray:
        """Analytic 1/r field centered at `center`, amplitude ~ G * mass.

        phi(r) = -G * mass / (|r - center| + softening)

        This bypasses the Poisson solver entirely, providing an independent
        check that the force-measurement pipeline correctly recovers F ~ M1*M2.
        """
        rel = self.pos - np.asarray(center, dtype=float)
        dist = np.sqrt(np.sum(rel * rel, axis=1)) + 0.5  # softening
        return -G_COUPLING * mass / dist

    def build_hamiltonian(self, phi: np.ndarray) -> csc_matrix:
        """Staggered Hamiltonian with external scalar field phi."""
        h = lil_matrix((self.n_sites, self.n_sites), dtype=complex)
        eps = np.where(self.parity == 0, 1.0, -1.0)
        h.setdiag((BARE_MASS + phi) * eps)

        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    if x + 1 < self.side:
                        j = self.index(x + 1, y, z)
                        h[i, j] += -0.5j
                        h[j, i] += 0.5j
                    eta_y = (-1) ** x
                    if y + 1 < self.side:
                        j = self.index(x, y + 1, z)
                        h[i, j] += eta_y * (-0.5j)
                        h[j, i] += eta_y * (0.5j)
                    eta_z = (-1) ** (x + y)
                    if z + 1 < self.side:
                        j = self.index(x, y, z + 1)
                        h[i, j] += eta_z * (-0.5j)
                        h[j, i] += eta_z * (0.5j)

        return h.tocsc()

    def make_stepper(self, hamiltonian: csc_matrix):
        """Crank-Nicolson: (I + i H dt/2) psi_new = (I - i H dt/2) psi_old."""
        a_plus = (self.eye_csc + 1j * hamiltonian * DT / 2).tocsc()
        a_minus = self.eye_csr - 1j * hamiltonian * DT / 2
        return splu(a_plus), a_minus

    def step(self, psi: np.ndarray, lu, a_minus) -> np.ndarray:
        psi_new = lu.solve(a_minus.dot(psi))
        return psi_new / np.linalg.norm(psi_new)

    def gradient_x(self, phi: np.ndarray) -> np.ndarray:
        """Central-difference gradient along x."""
        grad = np.zeros(self.n_sites, dtype=float)
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    if x == 0:
                        grad[i] = phi[self.index(x + 1, y, z)] - phi[i]
                    elif x == self.side - 1:
                        grad[i] = phi[i] - phi[self.index(x - 1, y, z)]
                    else:
                        grad[i] = 0.5 * (
                            phi[self.index(x + 1, y, z)] - phi[self.index(x - 1, y, z)]
                        )
        return grad

    def force_x_on(self, psi: np.ndarray, phi_partner: np.ndarray,
                   mass: float) -> float:
        """Force on particle (mass M) from partner's field phi_partner.

        F = -M * integral |psi|^2 * grad(phi_partner)

        M enters as the test-mass response factor.
        phi_partner ~ M_partner from Poisson linearity.
        Together: F ~ M * M_partner, but MEASURED not imposed.
        """
        prob = np.abs(psi) ** 2
        prob = prob / np.sum(prob)
        grad = self.gradient_x(phi_partner)
        return float(-mass * np.sum(prob * grad))


def power_law_fit_2d(s1_vals, s2_vals, f_vals):
    """Fit log|F| = alpha * log(M_A) + beta * log(M_B) + const."""
    log_s1 = np.log(np.array(s1_vals))
    log_s2 = np.log(np.array(s2_vals))
    log_f = np.log(np.abs(np.array(f_vals)))

    X = np.column_stack([log_s1, log_s2, np.ones_like(log_s1)])
    coeffs, _, _, _ = np.linalg.lstsq(X, log_f, rcond=None)

    alpha, beta, const = coeffs
    pred = X @ coeffs
    ss_res = float(np.sum((log_f - pred) ** 2))
    ss_tot = float(np.sum((log_f - np.mean(log_f)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0

    return alpha, beta, const, r2


def product_fit(products, f_vals):
    """Fit log|F| = gamma * log(M1*M2) + const."""
    log_p = np.log(np.array(products))
    log_f = np.log(np.abs(np.array(f_vals)))

    slope, intercept = np.polyfit(log_p, log_f, 1)
    pred = slope * log_p + intercept
    ss_res = float(np.sum((log_f - pred) ** 2))
    ss_tot = float(np.sum((log_f - np.mean(log_f)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0

    return slope, r2


def run_pair_poisson(lat: OpenStaggered3D, m_a: float, m_b: float,
                     center_a, center_b, frozen: bool = False) -> dict:
    """Run one (M_A, M_B) pair with separate Poisson solves per particle.

    NO bilinear term anywhere:
      - phi_A is solved from rho_A = M_A * |psi_A|^2 alone
      - phi_B is solved from rho_B = M_B * |psi_B|^2 alone
      - A evolves under phi_B, B evolves under phi_A (cross-field)
    """
    psi_a = lat.gaussian(center_a)
    psi_b = lat.gaussian(center_b)

    # Initial Poisson fields (separate solves, one per mass)
    phi_a_frozen = lat.solve_phi_single(m_a, psi_a)
    phi_b_frozen = lat.solve_phi_single(m_b, psi_b)

    force_a_hist = []
    force_b_hist = []

    for step_idx in range(N_STEPS):
        if frozen:
            phi_a = phi_a_frozen
            phi_b = phi_b_frozen
        else:
            phi_a = lat.solve_phi_single(m_a, psi_a)
            phi_b = lat.solve_phi_single(m_b, psi_b)

        # Force on A from B's field (test-mass M_A, source field phi_B ~ M_B)
        f_a = lat.force_x_on(psi_a, phi_b, m_a)
        # Force on B from A's field (test-mass M_B, source field phi_A ~ M_A)
        f_b = -lat.force_x_on(psi_b, phi_a, m_b)

        force_a_hist.append(f_a)
        force_b_hist.append(f_b)

        # Evolve: A under phi_B, B under phi_A (cross-field, no bilinear)
        h_a = lat.build_hamiltonian(phi_b)
        h_b = lat.build_hamiltonian(phi_a)

        lu_a, am_a = lat.make_stepper(h_a)
        lu_b, am_b = lat.make_stepper(h_b)

        psi_a = lat.step(psi_a, lu_a, am_a)
        psi_b = lat.step(psi_b, lu_b, am_b)

    early = slice(0, min(4, N_STEPS))
    f_a_mean = float(np.mean(force_a_hist[early]))
    f_b_mean = float(np.mean(force_b_hist[early]))

    return {
        "m_a": m_a,
        "m_b": m_b,
        "f_a": f_a_mean,
        "f_b": f_b_mean,
        "f_a_t0": force_a_hist[0],
        "f_b_t0": force_b_hist[0],
        "f_sym": 0.5 * (f_a_mean + f_b_mean),
        "f_sym_t0": 0.5 * (force_a_hist[0] + force_b_hist[0]),
        "frozen": frozen,
    }


def run_pair_handcrafted(lat: OpenStaggered3D, m_a: float, m_b: float,
                         center_a, center_b) -> dict:
    """Control: hand-crafted 1/r fields instead of Poisson solve.

    phi_B = -G * M_B / |r - r_B|  (analytic, no Poisson)
    phi_A = -G * M_A / |r - r_A|  (analytic, no Poisson)

    This is a frozen-source, analytic-field control. If the force
    pipeline is correct, we should still get F ~ M_A * M_B.
    """
    psi_a = lat.gaussian(center_a)
    psi_b = lat.gaussian(center_b)

    # Hand-crafted 1/r fields (no Poisson solver involved)
    phi_a_analytic = lat.handcrafted_1_over_r(center_a, m_a)
    phi_b_analytic = lat.handcrafted_1_over_r(center_b, m_b)

    # t=0 force only (frozen analytic fields)
    f_a = lat.force_x_on(psi_a, phi_b_analytic, m_a)
    f_b = -lat.force_x_on(psi_b, phi_a_analytic, m_b)

    return {
        "m_a": m_a,
        "m_b": m_b,
        "f_a": f_a,
        "f_b": f_b,
        "f_sym": 0.5 * (f_a + f_b),
    }


def main():
    t0 = time.time()

    print("=" * 96)
    print("PRODUCT LAW WITHOUT BILINEAR ANSATZ")
    print("=" * 96)
    print()
    print("CRITICAL DESIGN: No M_A*M_B product appears in any Hamiltonian or potential.")
    print("Each particle gets its OWN Poisson solve with its OWN mass as source.")
    print("The other particle feels that field. M_A*M_B must EMERGE from:")
    print("  phi_i ~ M_i  (Poisson linearity of separate solve)")
    print("  F_j  ~ M_j  (test-mass response)")
    print("  =>  F ~ M_i * M_j  (emergent, not imposed)")
    print()
    print(f"SIDE={SIDE}, BARE_MASS={BARE_MASS}, G={G_COUPLING}, MU2={MU2}")
    print(f"DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}, SEPARATION={SEPARATION}")
    print(f"MASS_VALUES={MASS_VALUES}")
    print(f"Lattice sites: {SIDE}^3 = {SIDE**3}")
    print()

    lat = OpenStaggered3D(SIDE)
    center = 0.5 * (SIDE - 1)
    center_a = (center - SEPARATION / 2.0, center, center)
    center_b = (center + SEPARATION / 2.0, center, center)

    pairs = list(itertools.product(MASS_VALUES, MASS_VALUES))

    # ==================================================================
    # Phase 1: STATIC (frozen fields, t=0 force) -- purest linearity test
    # ==================================================================
    print("=" * 96)
    print("PHASE 1: STATIC (FROZEN FIELDS, t=0 FORCE ONLY)")
    print("=" * 96)
    print("Poisson fields computed once from initial Gaussians, forces measured at t=0.")
    print("This is the purest test of Poisson linearity: no dynamics, no feedback.")
    print()
    print(f"{'M_A':>6s} {'M_B':>6s} {'M_A*M_B':>9s} {'F_A':>12s} {'F_B':>12s} {'F_sym':>12s}")
    print("-" * 68)

    static_rows = []
    for m_a, m_b in pairs:
        row = run_pair_poisson(lat, m_a, m_b, center_a, center_b, frozen=True)
        static_rows.append(row)
        print(f"{m_a:6.2f} {m_b:6.2f} {m_a*m_b:9.4f} "
              f"{row['f_a_t0']:+12.6e} {row['f_b_t0']:+12.6e} {row['f_sym_t0']:+12.6e}")

    print()

    # ==================================================================
    # Phase 2: DYNAMIC (self-consistent field updates)
    # ==================================================================
    print("=" * 96)
    print("PHASE 2: DYNAMIC (SELF-CONSISTENT POISSON UPDATES)")
    print("=" * 96)
    print("Poisson fields recomputed each step from evolved densities.")
    print("Tests whether product law survives self-consistent dynamics.")
    print()
    print(f"{'M_A':>6s} {'M_B':>6s} {'M_A*M_B':>9s} {'F_A':>12s} {'F_B':>12s} {'F_sym':>12s}")
    print("-" * 68)

    dynamic_rows = []
    for m_a, m_b in pairs:
        row = run_pair_poisson(lat, m_a, m_b, center_a, center_b, frozen=False)
        dynamic_rows.append(row)
        print(f"{m_a:6.2f} {m_b:6.2f} {m_a*m_b:9.4f} "
              f"{row['f_a']:+12.6e} {row['f_b']:+12.6e} {row['f_sym']:+12.6e}")

    print()

    # ==================================================================
    # Phase 3: HAND-CRAFTED 1/r CONTROL
    # ==================================================================
    print("=" * 96)
    print("PHASE 3: HAND-CRAFTED 1/r FIELD CONTROL")
    print("=" * 96)
    print("Analytic phi = -G*M / (|r - r_center| + softening), no Poisson solver.")
    print("Tests force pipeline independently of Poisson discretization.")
    print()
    print(f"{'M_A':>6s} {'M_B':>6s} {'M_A*M_B':>9s} {'F_A':>12s} {'F_B':>12s} {'F_sym':>12s}")
    print("-" * 68)

    handcrafted_rows = []
    for m_a, m_b in pairs:
        row = run_pair_handcrafted(lat, m_a, m_b, center_a, center_b)
        handcrafted_rows.append(row)
        print(f"{m_a:6.2f} {m_b:6.2f} {m_a*m_b:9.4f} "
              f"{row['f_a']:+12.6e} {row['f_b']:+12.6e} {row['f_sym']:+12.6e}")

    print()

    # ==================================================================
    # Phase 4: Product law fits for all three modes
    # ==================================================================
    all_fits = {}

    for label, rows, f_key in [
        ("STATIC (t=0 frozen)", static_rows, "f_sym_t0"),
        ("DYNAMIC (self-consistent)", dynamic_rows, "f_sym"),
        ("HAND-CRAFTED 1/r", handcrafted_rows, "f_sym"),
    ]:
        print("=" * 96)
        print(f"PRODUCT LAW FITS: {label}")
        print("=" * 96)

        m_a_all = [r["m_a"] for r in rows]
        m_b_all = [r["m_b"] for r in rows]
        f_all = [r[f_key] for r in rows]
        prod_all = [r["m_a"] * r["m_b"] for r in rows]

        valid = [i for i in range(len(f_all)) if abs(f_all[i]) > 1e-20]
        if len(valid) < 4:
            print("  ERROR: Too few valid data points.")
            continue

        m_a_v = [m_a_all[i] for i in valid]
        m_b_v = [m_b_all[i] for i in valid]
        f_v = [f_all[i] for i in valid]
        prod_v = [prod_all[i] for i in valid]

        # Separate exponents
        alpha, beta, const, r2 = power_law_fit_2d(m_a_v, m_b_v, f_v)
        print(f"  Separate fit: |F| ~ M_A^{alpha:.4f} * M_B^{beta:.4f}")
        print(f"    alpha (M_A exponent) = {alpha:.4f}  (expect 1.0)")
        print(f"    beta  (M_B exponent) = {beta:.4f}  (expect 1.0)")
        print(f"    R^2 = {r2:.6f}")

        # Bilinear product fit
        gamma, r2_prod = product_fit(prod_v, f_v)
        print(f"  Product fit: |F| ~ (M_A*M_B)^{gamma:.4f}  (R^2={r2_prod:.6f})")
        print(f"    gamma = {gamma:.4f}  (expect 1.0)")
        print()

        all_fits[label] = {
            "alpha": alpha, "beta": beta, "r2": r2,
            "gamma": gamma, "r2_prod": r2_prod,
        }

        # Fixed-M_B slices
        print(f"  --- Fixed-M_B slices ---")
        print(f"  {'M_B_fixed':>10s} {'exp(M_A)':>10s} {'R^2':>8s}")
        for m_b_fixed in MASS_VALUES:
            sub = [r for r in rows if r["m_b"] == m_b_fixed and abs(r[f_key]) > 1e-20]
            if len(sub) < 3:
                continue
            log_ma = np.log([r["m_a"] for r in sub])
            log_f = np.log(np.abs([r[f_key] for r in sub]))
            slope, intercept = np.polyfit(log_ma, log_f, 1)
            pred = slope * log_ma + intercept
            ss_res = float(np.sum((log_f - pred) ** 2))
            ss_tot = float(np.sum((log_f - np.mean(log_f)) ** 2))
            r2_s = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
            print(f"  {m_b_fixed:10.2f} {slope:10.4f} {r2_s:8.6f}")

        print(f"  --- Fixed-M_A slices ---")
        print(f"  {'M_A_fixed':>10s} {'exp(M_B)':>10s} {'R^2':>8s}")
        for m_a_fixed in MASS_VALUES:
            sub = [r for r in rows if r["m_a"] == m_a_fixed and abs(r[f_key]) > 1e-20]
            if len(sub) < 3:
                continue
            log_mb = np.log([r["m_b"] for r in sub])
            log_f = np.log(np.abs([r[f_key] for r in sub]))
            slope, intercept = np.polyfit(log_mb, log_f, 1)
            pred = slope * log_mb + intercept
            ss_res = float(np.sum((log_f - pred) ** 2))
            ss_tot = float(np.sum((log_f - np.mean(log_f)) ** 2))
            r2_s = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
            print(f"  {m_a_fixed:10.2f} {slope:10.4f} {r2_s:8.6f}")

        print()

    # ==================================================================
    # Phase 5: STATIC vs DYNAMIC comparison
    # ==================================================================
    print("=" * 96)
    print("STATIC vs DYNAMIC COMPARISON")
    print("=" * 96)
    print(f"{'M_A':>6s} {'M_B':>6s} {'F_static':>12s} {'F_dynamic':>12s} {'rel_diff':>10s}")
    print("-" * 56)
    stat_dyn_diffs = []
    for i, (m_a, m_b) in enumerate(pairs):
        f_stat = static_rows[i]["f_sym_t0"]
        f_dyn = dynamic_rows[i]["f_sym"]
        denom = max(abs(f_stat), abs(f_dyn), 1e-30)
        rel = abs(f_stat - f_dyn) / denom
        stat_dyn_diffs.append(rel)
        print(f"{m_a:6.2f} {m_b:6.2f} {f_stat:+12.6e} {f_dyn:+12.6e} {rel:10.2%}")

    print(f"\n  Max static/dynamic difference:  {max(stat_dyn_diffs):.4%}")
    print(f"  Mean static/dynamic difference: {float(np.mean(stat_dyn_diffs)):.4%}")
    print()

    # ==================================================================
    # Phase 6: Symmetry check (t=0, frozen -- acceptance gate)
    # ==================================================================
    print("=" * 96)
    print("SYMMETRY CHECK (t=0, FROZEN -- acceptance gate)")
    print("=" * 96)
    print("F_A(M_A=a, M_B=b) vs F_B(M_A=b, M_B=a) at t=0 with frozen fields.")
    print()

    sym_violations = []
    print(f"{'M_A':>6s} {'M_B':>6s} {'F_A(a,b)':>12s} {'F_B(b,a)':>12s} {'rel_diff':>10s}")
    print("-" * 56)
    for m_a in MASS_VALUES:
        for m_b in MASS_VALUES:
            if m_a >= m_b:
                continue
            r_ab = next(r for r in static_rows if r["m_a"] == m_a and r["m_b"] == m_b)
            r_ba = next(r for r in static_rows if r["m_a"] == m_b and r["m_b"] == m_a)
            f_ab = r_ab["f_a_t0"]
            f_ba = r_ba["f_b_t0"]
            denom = max(abs(f_ab), abs(f_ba), 1e-30)
            rel = abs(f_ab - f_ba) / denom
            sym_violations.append(rel)
            print(f"{m_a:6.2f} {m_b:6.2f} {f_ab:+12.6e} {f_ba:+12.6e} {rel:10.2%}")

    max_sym = max(sym_violations) if sym_violations else 0.0
    mean_sym = float(np.mean(sym_violations)) if sym_violations else 0.0
    print(f"\n  Max symmetry violation:  {max_sym:.4%}")
    print(f"  Mean symmetry violation: {mean_sym:.4%}")
    print()

    # ==================================================================
    # VERDICT
    # ==================================================================
    print("=" * 96)
    print("VERDICT")
    print("=" * 96)

    checks = []

    # Static fit (purest test)
    if "STATIC (t=0 frozen)" in all_fits:
        fit_s = all_fits["STATIC (t=0 frozen)"]
        alpha_s_ok = abs(fit_s["alpha"] - 1.0) < ALPHA_TOL
        beta_s_ok = abs(fit_s["beta"] - 1.0) < BETA_TOL
        r2_s_ok = fit_s["r2"] > R2_MIN
        gamma_s_ok = abs(fit_s["gamma"] - 1.0) < BILINEAR_TOL
        checks.extend([alpha_s_ok, beta_s_ok, r2_s_ok, gamma_s_ok])

        print(f"  STATIC (frozen, t=0):")
        print(f"    alpha = {fit_s['alpha']:.4f}  "
              f"{'PASS' if alpha_s_ok else 'FAIL'} (|1-alpha| < {ALPHA_TOL})")
        print(f"    beta  = {fit_s['beta']:.4f}  "
              f"{'PASS' if beta_s_ok else 'FAIL'} (|1-beta| < {BETA_TOL})")
        print(f"    R^2   = {fit_s['r2']:.6f}  "
              f"{'PASS' if r2_s_ok else 'FAIL'} (>{R2_MIN})")
        print(f"    gamma (bilinear) = {fit_s['gamma']:.4f}  "
              f"{'PASS' if gamma_s_ok else 'FAIL'} (|1-gamma| < {BILINEAR_TOL})")

    # Dynamic fit
    if "DYNAMIC (self-consistent)" in all_fits:
        fit_d = all_fits["DYNAMIC (self-consistent)"]
        alpha_d_ok = abs(fit_d["alpha"] - 1.0) < ALPHA_TOL
        beta_d_ok = abs(fit_d["beta"] - 1.0) < BETA_TOL
        r2_d_ok = fit_d["r2"] > R2_MIN
        gamma_d_ok = abs(fit_d["gamma"] - 1.0) < BILINEAR_TOL
        checks.extend([alpha_d_ok, beta_d_ok, r2_d_ok, gamma_d_ok])

        print(f"  DYNAMIC (self-consistent):")
        print(f"    alpha = {fit_d['alpha']:.4f}  "
              f"{'PASS' if alpha_d_ok else 'FAIL'} (|1-alpha| < {ALPHA_TOL})")
        print(f"    beta  = {fit_d['beta']:.4f}  "
              f"{'PASS' if beta_d_ok else 'FAIL'} (|1-beta| < {BETA_TOL})")
        print(f"    R^2   = {fit_d['r2']:.6f}  "
              f"{'PASS' if r2_d_ok else 'FAIL'} (>{R2_MIN})")
        print(f"    gamma (bilinear) = {fit_d['gamma']:.4f}  "
              f"{'PASS' if gamma_d_ok else 'FAIL'} (|1-gamma| < {BILINEAR_TOL})")

    # Hand-crafted control
    if "HAND-CRAFTED 1/r" in all_fits:
        fit_h = all_fits["HAND-CRAFTED 1/r"]
        alpha_h_ok = abs(fit_h["alpha"] - 1.0) < ALPHA_TOL
        beta_h_ok = abs(fit_h["beta"] - 1.0) < BETA_TOL
        gamma_h_ok = abs(fit_h["gamma"] - 1.0) < BILINEAR_TOL

        print(f"  HAND-CRAFTED 1/r CONTROL:")
        print(f"    alpha = {fit_h['alpha']:.4f}  "
              f"{'PASS' if alpha_h_ok else 'FAIL'}")
        print(f"    beta  = {fit_h['beta']:.4f}  "
              f"{'PASS' if beta_h_ok else 'FAIL'}")
        print(f"    gamma = {fit_h['gamma']:.4f}  "
              f"{'PASS' if gamma_h_ok else 'FAIL'}")
        # Hand-crafted is informational, not gated
        # (it validates the force pipeline, not the physics)

    # Symmetry gate
    sym_ok = max_sym < SYMMETRY_TOL
    checks.append(sym_ok)
    print(f"  SYMMETRY (t=0 frozen, gate):")
    print(f"    max violation = {max_sym:.4%}  "
          f"{'PASS' if sym_ok else 'FAIL'} (<{SYMMETRY_TOL:.0%})")

    print()
    all_pass = all(checks)
    if all_pass:
        print("  ALL GATES PASSED.")
        print()
        print("  The M1*M2 product law EMERGES from separate Poisson solves.")
        print("  No bilinear term V ~ M_A*M_B was used in any Hamiltonian.")
        print("  The mechanism is:")
        print("    phi_A = Poisson(M_A * |psi_A|^2)  =>  phi_A ~ M_A")
        print("    F_on_B = -M_B * <grad phi_A>      =>  F ~ M_A * M_B")
        print("  Both STATIC and DYNAMIC modes confirm this.")
        print("  The hand-crafted 1/r control validates the force pipeline.")
    else:
        print("  SOME GATES FAILED.")
        print("  Investigate lattice size, sigma, dt, or coupling strength.")

    print(f"\nElapsed: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
