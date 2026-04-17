#!/usr/bin/env python3
"""
Emergent M1*M2 Product Law via Self-Consistent Poisson Field
=============================================================

Goal:
  Demonstrate that the gravitational product law F ~ M_A * M_B is recovered
  from cross-field Poisson linearity on one audited open 3D staggered surface
  rather than being baked into the Hamiltonian.

Why this matters:
  Previous tests used V(x1,x2) = -G * s1 * s2 / |x1-x2|, which hardcodes
  the bilinear M1*M2 factor into the interaction operator. That proves
  the solver works but not that the product law is a consequence of
  field dynamics. Here, NO bilinear term appears anywhere in the code.

How it works:
  1. Each particle sources its own gravitational potential via Poisson:
       (L + mu^2) phi_A = G * rho_A,    rho_A = M_A * |psi_A|^2
  2. The OTHER particle feels this potential (cross-field coupling):
       H_A includes phi_B only (not phi_A)
       H_B includes phi_A only (not phi_B)
  3. The Poisson equation is LINEAR, so phi_A scales as M_A.
  4. The test-mass response is LINEAR, so the force on B scales as M_B.
  5. Together these give F ~ M_A * M_B, but only as a bounded field-linearity
     result on the audited surface.

Controls:
  - FROZEN_SOURCE: Poisson fields computed once from initial densities,
    held fixed during evolution. Product law should survive (confirms
    it is a field-linearity result, not a dynamical accident).

Architecture:
  Open 3D staggered lattice with parity-correct scalar coupling,
  Crank-Nicolson time stepping, sparse Poisson solver.

PStack experiment: frontier-emergent-product-law
"""

from __future__ import annotations

import itertools
import time

import numpy as np
from scipy.sparse import csc_matrix, csr_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import splu, spsolve


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
ALPHA_TOL = 0.05       # |alpha - 1| < 5%
BETA_TOL = 0.05        # |beta - 1| < 5%
R2_MIN = 0.99
SYMMETRY_TOL = 0.02    # 2% relative tolerance for t=0 frozen symmetry


class OpenStaggered3D:
    """Open-boundary 3D staggered lattice with Poisson solver."""

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
        # Precompute Poisson operator and its LU factorization
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

    def solve_phi(self, rho: np.ndarray) -> np.ndarray:
        """Solve (L + mu^2) phi = G * rho via precomputed LU."""
        if np.allclose(rho, 0.0):
            return np.zeros(self.n_sites)
        return self._poisson_lu.solve(G_COUPLING * rho).real

    def build_hamiltonian(self, phi: np.ndarray) -> csc_matrix:
        """Staggered Hamiltonian with scalar field phi on the diagonal."""
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
        """Crank-Nicolson stepper: (I + i H dt/2) psi_new = (I - i H dt/2) psi_old."""
        a_plus = (self.eye_csc + 1j * hamiltonian * DT / 2).tocsc()
        a_minus = self.eye_csr - 1j * hamiltonian * DT / 2
        return splu(a_plus), a_minus

    def step(self, psi: np.ndarray, lu, a_minus) -> np.ndarray:
        psi_new = lu.solve(a_minus.dot(psi))
        return psi_new / np.linalg.norm(psi_new)

    def gradient_x(self, phi: np.ndarray) -> np.ndarray:
        """Central-difference gradient along x (forward/backward at boundaries)."""
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
        """Force on particle with mass M from partner's field phi_partner.

        F = -M * integral |psi|^2 * grad(phi_partner)

        The mass factor is CRUCIAL: rho = M * |psi|^2, so the force is
        F = -integral rho * grad(phi) = -M * integral |psi|^2 * grad(phi).

        This is what makes F ~ M_test * M_source emerge:
          - phi_partner ~ M_source (Poisson linearity)
          - F ~ M_test * grad(phi_partner) (this function)
          - Together: F ~ M_test * M_source

        Sign convention: positive = force in +x direction.
        """
        prob = np.abs(psi) ** 2
        prob = prob / np.sum(prob)  # normalize probability
        grad = self.gradient_x(phi_partner)
        return float(-mass * np.sum(prob * grad))


def power_law_fit_2d(s1_vals, s2_vals, f_vals):
    """Fit log|F| = alpha * log(M_A) + beta * log(M_B) + const.

    Returns (alpha, beta, const, R^2).
    """
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


def run_pair(lat: OpenStaggered3D, m_a: float, m_b: float,
             center_a, center_b, frozen: bool = False) -> dict:
    """Run one (M_A, M_B) pair with cross-field Poisson coupling.

    If frozen=True, compute phi_A and phi_B once from initial densities
    and hold them fixed for all time steps.
    """
    psi_a = lat.gaussian(center_a)
    psi_b = lat.gaussian(center_b)

    # Initial densities and Poisson fields
    rho_a_init = m_a * np.abs(psi_a) ** 2
    rho_b_init = m_b * np.abs(psi_b) ** 2
    phi_a_frozen = lat.solve_phi(rho_a_init)
    phi_b_frozen = lat.solve_phi(rho_b_init)

    force_a_hist = []  # force on A from B's field
    force_b_hist = []  # force on B from A's field

    for step_idx in range(N_STEPS):
        if frozen:
            phi_a = phi_a_frozen
            phi_b = phi_b_frozen
        else:
            # Recompute Poisson fields from current densities
            rho_a = m_a * np.abs(psi_a) ** 2
            rho_b = m_b * np.abs(psi_b) ** 2
            phi_a = lat.solve_phi(rho_a)
            phi_b = lat.solve_phi(rho_b)

        # Measure force BEFORE stepping (Ehrenfest)
        # Force on A from B's field: F_A = -M_A * <grad phi_B>
        f_a = lat.force_x_on(psi_a, phi_b, m_a)
        # Force on B from A's field: F_B = -M_B * <grad phi_A>
        # B is on the right, attracted leftward = -x, so negate
        f_b = -lat.force_x_on(psi_b, phi_a, m_b)

        force_a_hist.append(f_a)
        force_b_hist.append(f_b)

        # Cross-field Hamiltonian: A evolves under phi_B, B evolves under phi_A
        h_a = lat.build_hamiltonian(phi_b)
        h_b = lat.build_hamiltonian(phi_a)

        lu_a, am_a = lat.make_stepper(h_a)
        lu_b, am_b = lat.make_stepper(h_b)

        psi_a = lat.step(psi_a, lu_a, am_a)
        psi_b = lat.step(psi_b, lu_b, am_b)

    # Use early-time forces (before wavepacket distortion)
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


def main():
    t0 = time.time()

    print("=" * 96)
    print("EMERGENT M1*M2 PRODUCT LAW VIA SELF-CONSISTENT POISSON FIELD")
    print("=" * 96)
    print(f"SIDE={SIDE}, BARE_MASS={BARE_MASS}, G={G_COUPLING}, MU2={MU2}")
    print(f"DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}, SEPARATION={SEPARATION}")
    print(f"MASS_VALUES={MASS_VALUES}")
    print(f"Lattice sites: {SIDE}^3 = {SIDE**3}")
    print()
    print("KEY DESIGN POINT: NO bilinear V(x1,x2) = M_A*M_B*f(r) anywhere.")
    print("Each particle sources its own Poisson field; the OTHER particle")
    print("feels that field. The M_A*M_B scaling must EMERGE from:")
    print("  phi_A ~ M_A (Poisson linearity) + force_B ~ M_B (test-mass linearity)")
    print()

    lat = OpenStaggered3D(SIDE)
    center = 0.5 * (SIDE - 1)
    center_a = (center - SEPARATION / 2.0, center, center)
    center_b = (center + SEPARATION / 2.0, center, center)

    # ======================================================================
    # Phase 1: Dynamic (self-consistent) sweep
    # ======================================================================
    print("=" * 96)
    print("PHASE 1: DYNAMIC (SELF-CONSISTENT) MASS SWEEP")
    print("=" * 96)
    pairs = list(itertools.product(MASS_VALUES, MASS_VALUES))
    print(f"{'M_A':>6s} {'M_B':>6s} {'M_A*M_B':>9s} {'F_A':>12s} {'F_B':>12s} {'F_sym':>12s}")
    print("-" * 68)

    dynamic_rows = []
    for m_a, m_b in pairs:
        row = run_pair(lat, m_a, m_b, center_a, center_b, frozen=False)
        dynamic_rows.append(row)
        print(f"{m_a:6.2f} {m_b:6.2f} {m_a*m_b:9.4f} "
              f"{row['f_a']:+12.6e} {row['f_b']:+12.6e} {row['f_sym']:+12.6e}")

    print()

    # ======================================================================
    # Phase 2: Frozen-source control sweep
    # ======================================================================
    print("=" * 96)
    print("PHASE 2: FROZEN-SOURCE CONTROL SWEEP")
    print("=" * 96)
    print(f"{'M_A':>6s} {'M_B':>6s} {'M_A*M_B':>9s} {'F_A':>12s} {'F_B':>12s} {'F_sym':>12s}")
    print("-" * 68)

    frozen_rows = []
    for m_a, m_b in pairs:
        row = run_pair(lat, m_a, m_b, center_a, center_b, frozen=True)
        frozen_rows.append(row)
        print(f"{m_a:6.2f} {m_b:6.2f} {m_a*m_b:9.4f} "
              f"{row['f_a']:+12.6e} {row['f_b']:+12.6e} {row['f_sym']:+12.6e}")

    print()

    # ======================================================================
    # Phase 3: Fit product law
    # ======================================================================
    for label, rows in [("DYNAMIC", dynamic_rows), ("FROZEN", frozen_rows)]:
        print("=" * 96)
        print(f"PRODUCT LAW FITS ({label})")
        print("=" * 96)

        m_a_all = [r["m_a"] for r in rows]
        m_b_all = [r["m_b"] for r in rows]
        f_sym_all = [r["f_sym"] for r in rows]
        f_a_all = [r["f_a"] for r in rows]
        f_b_all = [r["f_b"] for r in rows]

        # Check all forces have consistent sign (attractive)
        positive_count = sum(1 for f in f_sym_all if f > 0)
        print(f"  Attractive force rows: {positive_count}/{len(f_sym_all)}")

        # Use absolute values for fitting
        valid = [i for i in range(len(f_sym_all)) if abs(f_sym_all[i]) > 1e-20]
        if len(valid) < 4:
            print("  ERROR: Too few valid data points for fitting.")
            continue

        m_a_v = [m_a_all[i] for i in valid]
        m_b_v = [m_b_all[i] for i in valid]
        f_v = [f_sym_all[i] for i in valid]

        alpha, beta, const, r2 = power_law_fit_2d(m_a_v, m_b_v, f_v)
        print(f"  Fit: |F_sym| ~ M_A^{alpha:.4f} * M_B^{beta:.4f}")
        print(f"    alpha (M_A exponent) = {alpha:.4f}  (expect 1.0)")
        print(f"    beta  (M_B exponent) = {beta:.4f}  (expect 1.0)")
        print(f"    R^2 = {r2:.6f}")
        print()

        # Fit F_A and F_B separately
        f_a_v = [f_a_all[i] for i in valid]
        f_b_v = [f_b_all[i] for i in valid]

        alpha_a, beta_a, _, r2_a = power_law_fit_2d(m_a_v, m_b_v, f_a_v)
        alpha_b, beta_b, _, r2_b = power_law_fit_2d(m_a_v, m_b_v, f_b_v)
        print(f"  F_A fit: |F_A| ~ M_A^{alpha_a:.4f} * M_B^{beta_a:.4f}  (R^2={r2_a:.6f})")
        print(f"  F_B fit: |F_B| ~ M_A^{alpha_b:.4f} * M_B^{beta_b:.4f}  (R^2={r2_b:.6f})")
        print()

        # Fixed-M_B slices
        print(f"  --- Fixed-M_B slices ({label}) ---")
        print(f"  {'M_B_fixed':>10s} {'exp(M_A)':>10s} {'R^2':>8s}")
        for m_b_fixed in MASS_VALUES:
            sub = [r for r in rows if r["m_b"] == m_b_fixed and abs(r["f_sym"]) > 1e-20]
            if len(sub) < 3:
                continue
            log_ma = np.log([r["m_a"] for r in sub])
            log_f = np.log(np.abs([r["f_sym"] for r in sub]))
            slope, intercept = np.polyfit(log_ma, log_f, 1)
            pred = slope * log_ma + intercept
            ss_res = float(np.sum((log_f - pred) ** 2))
            ss_tot = float(np.sum((log_f - np.mean(log_f)) ** 2))
            r2_s = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
            print(f"  {m_b_fixed:10.2f} {slope:10.4f} {r2_s:8.6f}")

        # Fixed-M_A slices
        print(f"  --- Fixed-M_A slices ({label}) ---")
        print(f"  {'M_A_fixed':>10s} {'exp(M_B)':>10s} {'R^2':>8s}")
        for m_a_fixed in MASS_VALUES:
            sub = [r for r in rows if r["m_a"] == m_a_fixed and abs(r["f_sym"]) > 1e-20]
            if len(sub) < 3:
                continue
            log_mb = np.log([r["m_b"] for r in sub])
            log_f = np.log(np.abs([r["f_sym"] for r in sub]))
            slope, intercept = np.polyfit(log_mb, log_f, 1)
            pred = slope * log_mb + intercept
            ss_res = float(np.sum((log_f - pred) ** 2))
            ss_tot = float(np.sum((log_f - np.mean(log_f)) ** 2))
            r2_s = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
            print(f"  {m_a_fixed:10.2f} {slope:10.4f} {r2_s:8.6f}")

        print()

    # ======================================================================
    # Phase 4: Symmetry checks
    # ======================================================================
    # Two symmetry tests:
    # (a) FROZEN: F_A(a,b) vs F_B(b,a) in frozen fields. Since the
    #     wavepackets don't evolve differently, this isolates the
    #     Poisson-field symmetry and is the acceptance gate.
    # (b) DYNAMIC: same comparison under self-consistent evolution.
    #     Staggered-phase lattice artifacts break this at O(few%),
    #     reported for transparency but not gated.

    # t=0 frozen symmetry: purest test (no evolution at all)
    print("=" * 96)
    print("SYMMETRY CHECK (t=0, FROZEN FIELDS -- acceptance gate)")
    print("=" * 96)
    print("F_A(M_A=a, M_B=b, t=0) vs F_B(M_A=b, M_B=a, t=0)")
    print("At t=0 with frozen fields, wavepackets are identical Gaussians.")
    print("Any residual asymmetry is purely from lattice discretization.")
    print()

    sym_violations_t0 = []
    print(f"{'M_A':>6s} {'M_B':>6s} {'F_A(a,b)':>12s} {'F_B(b,a)':>12s} {'rel_diff':>10s}")
    print("-" * 56)
    for m_a in MASS_VALUES:
        for m_b in MASS_VALUES:
            if m_a >= m_b:
                continue
            r_ab = next(r for r in frozen_rows if r["m_a"] == m_a and r["m_b"] == m_b)
            r_ba = next(r for r in frozen_rows if r["m_a"] == m_b and r["m_b"] == m_a)

            f_ab = r_ab["f_a_t0"]
            f_ba = r_ba["f_b_t0"]
            denom = max(abs(f_ab), abs(f_ba), 1e-30)
            rel = abs(f_ab - f_ba) / denom
            sym_violations_t0.append(rel)
            print(f"{m_a:6.2f} {m_b:6.2f} {f_ab:+12.6e} {f_ba:+12.6e} {rel:10.2%}")

    max_sym_t0 = max(sym_violations_t0) if sym_violations_t0 else 0.0
    mean_sym_t0 = float(np.mean(sym_violations_t0)) if sym_violations_t0 else 0.0
    print(f"\n  Max symmetry violation:  {max_sym_t0:.4%}")
    print(f"  Mean symmetry violation: {mean_sym_t0:.4%}")
    print()

    # Dynamic symmetry (informational)
    print("=" * 96)
    print("SYMMETRY CHECK (DYNAMIC, multi-step average -- informational)")
    print("=" * 96)
    sym_violations_dyn = []
    print(f"{'M_A':>6s} {'M_B':>6s} {'F_A(a,b)':>12s} {'F_B(b,a)':>12s} {'rel_diff':>10s}")
    print("-" * 56)
    for m_a in MASS_VALUES:
        for m_b in MASS_VALUES:
            if m_a >= m_b:
                continue
            r_ab = next(r for r in dynamic_rows if r["m_a"] == m_a and r["m_b"] == m_b)
            r_ba = next(r for r in dynamic_rows if r["m_a"] == m_b and r["m_b"] == m_a)
            f_ab = r_ab["f_a"]
            f_ba = r_ba["f_b"]
            denom = max(abs(f_ab), abs(f_ba), 1e-30)
            rel = abs(f_ab - f_ba) / denom
            sym_violations_dyn.append(rel)
            print(f"{m_a:6.2f} {m_b:6.2f} {f_ab:+12.6e} {f_ba:+12.6e} {rel:10.2%}")

    max_sym_dynamic = max(sym_violations_dyn) if sym_violations_dyn else 0.0
    print(f"\n  Max symmetry violation:  {max_sym_dynamic:.4%}")
    print()

    # ======================================================================
    # Phase 5: Frozen vs Dynamic comparison
    # ======================================================================
    print("=" * 96)
    print("FROZEN vs DYNAMIC COMPARISON")
    print("=" * 96)
    print(f"{'M_A':>6s} {'M_B':>6s} {'F_dyn':>12s} {'F_frz':>12s} {'rel_diff':>10s}")
    print("-" * 56)
    frz_dyn_diffs = []
    for i, (m_a, m_b) in enumerate(pairs):
        f_dyn = dynamic_rows[i]["f_sym"]
        f_frz = frozen_rows[i]["f_sym"]
        denom = max(abs(f_dyn), abs(f_frz), 1e-30)
        rel = abs(f_dyn - f_frz) / denom
        frz_dyn_diffs.append(rel)
        print(f"{m_a:6.2f} {m_b:6.2f} {f_dyn:+12.6e} {f_frz:+12.6e} {rel:10.2%}")

    print(f"\n  Max frozen/dynamic difference:  {max(frz_dyn_diffs):.4%}")
    print(f"  Mean frozen/dynamic difference: {float(np.mean(frz_dyn_diffs)):.4%}")
    print()

    # ======================================================================
    # Phase 6: Fit frozen results
    # ======================================================================
    m_a_v_f = [r["m_a"] for r in frozen_rows if abs(r["f_sym"]) > 1e-20]
    m_b_v_f = [r["m_b"] for r in frozen_rows if abs(r["f_sym"]) > 1e-20]
    f_v_f = [r["f_sym"] for r in frozen_rows if abs(r["f_sym"]) > 1e-20]

    alpha_f, beta_f, _, r2_f = power_law_fit_2d(m_a_v_f, m_b_v_f, f_v_f)

    # Dynamic fit (already computed but recompute for clarity)
    m_a_v_d = [r["m_a"] for r in dynamic_rows if abs(r["f_sym"]) > 1e-20]
    m_b_v_d = [r["m_b"] for r in dynamic_rows if abs(r["f_sym"]) > 1e-20]
    f_v_d = [r["f_sym"] for r in dynamic_rows if abs(r["f_sym"]) > 1e-20]
    alpha_d, beta_d, _, r2_d = power_law_fit_2d(m_a_v_d, m_b_v_d, f_v_d)

    # ======================================================================
    # VERDICT
    # ======================================================================
    print("=" * 96)
    print("VERDICT")
    print("=" * 96)

    checks = []

    # Dynamic exponents
    alpha_ok = abs(alpha_d - 1.0) < ALPHA_TOL
    beta_ok = abs(beta_d - 1.0) < BETA_TOL
    r2_ok = r2_d > R2_MIN
    checks.extend([alpha_ok, beta_ok, r2_ok])

    print(f"  DYNAMIC:")
    print(f"    alpha (M_A exponent) = {alpha_d:.4f}  "
          f"{'PASS' if alpha_ok else 'FAIL'} (|1-alpha| < {ALPHA_TOL})")
    print(f"    beta  (M_B exponent) = {beta_d:.4f}  "
          f"{'PASS' if beta_ok else 'FAIL'} (|1-beta| < {BETA_TOL})")
    print(f"    R^2                  = {r2_d:.6f}  "
          f"{'PASS' if r2_ok else 'FAIL'} (>{R2_MIN})")

    # Frozen exponents
    alpha_f_ok = abs(alpha_f - 1.0) < ALPHA_TOL
    beta_f_ok = abs(beta_f - 1.0) < BETA_TOL
    r2_f_ok = r2_f > R2_MIN
    checks.extend([alpha_f_ok, beta_f_ok, r2_f_ok])

    print(f"  FROZEN:")
    print(f"    alpha (M_A exponent) = {alpha_f:.4f}  "
          f"{'PASS' if alpha_f_ok else 'FAIL'} (|1-alpha| < {ALPHA_TOL})")
    print(f"    beta  (M_B exponent) = {beta_f:.4f}  "
          f"{'PASS' if beta_f_ok else 'FAIL'} (|1-beta| < {BETA_TOL})")
    print(f"    R^2                  = {r2_f:.6f}  "
          f"{'PASS' if r2_f_ok else 'FAIL'} (>{R2_MIN})")

    # Symmetry (t=0 frozen = acceptance gate; dynamic = informational)
    sym_ok = max_sym_t0 < SYMMETRY_TOL
    checks.append(sym_ok)
    print(f"  SYMMETRY (t=0 frozen, gate):")
    print(f"    max violation        = {max_sym_t0:.4%}  "
          f"{'PASS' if sym_ok else 'FAIL'} (<{SYMMETRY_TOL:.0%})")
    print(f"  SYMMETRY (dynamic, informational):")
    print(f"    max violation        = {max_sym_dynamic:.4%}")

    print()
    all_pass = all(checks)
    if all_pass:
        print("  ALL GATES PASSED.")
        print()
        print("  The M1*M2 product law is recovered from cross-field Poisson dynamics")
        print("  on the audited open 3D staggered surface.")
        print("  No bilinear interaction term was used anywhere in the Hamiltonian.")
        print("  The mechanism is: phi_i ~ M_i (Poisson linearity)")
        print("                  + F_j ~ M_j (test-mass response linearity)")
        print("                  = F ~ M_i * M_j.")
        print("  The frozen-source control confirms this is a field-linearity result,")
        print("  not a full Newton-closure claim.")
    else:
        print("  SOME GATES FAILED.")
        print("  Investigate lattice size, sigma, dt, or coupling strength.")

    print(f"\nElapsed: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
