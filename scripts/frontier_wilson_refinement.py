#!/usr/bin/env python3
"""
Wilson two-body lattice refinement test.

Question: does the distance-law exponent (-3.4 at side=9) converge
toward Newton (-2.0) as the lattice spacing a -> 0?

Protocol:
  1. Fixed-side sweep: sides [9,11,13,15] with d=4 lattice units
     (coarse check: does the exponent change with box size?)

  2. Distance sweep at side=13: d = [3,4,5,6,7]
     (extract exponent at one lattice spacing)

  3. TRUE lattice refinement at fixed physical size L=9:
       a=1.0 -> side= 9,  d_lat=4
       a=0.7 -> side=13,  d_lat=6  (4/0.7 ~ 5.7, round to 6)
       a=0.5 -> side=18,  d_lat=8

     Hopping and Wilson mass rescaled by 1/a so the physical
     Hamiltonian stays fixed while resolution increases.

  4. Multi-distance refinement: at each a, sweep physical D in [3,4,5,6]
     and extract the exponent. Does it soften toward -2.0?
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply, spsolve


# Physical parameters (fixed)
MASS = 0.30
WILSON_R = 1.0
DT = 0.08
REG = 1e-3
N_STEPS = 15
SIGMA = 1.0
G_VAL = 5.0
MU2_VAL = 0.22


class RefinedWilsonLattice:
    """Open-boundary 3D Wilson lattice with adjustable spacing a."""

    def __init__(self, side: int, a: float = 1.0):
        self.side = side
        self.a = a
        self.n = side**3
        self.pos = np.zeros((self.n, 3))
        self.adj: dict[int, list[int]] = {}

        for x in range(side):
            for y in range(side):
                for z in range(side):
                    i = self.site_index(x, y, z)
                    self.pos[i] = [x * a, y * a, z * a]
                    self.adj[i] = []
                    for dx, dy, dz in (
                        (1, 0, 0), (-1, 0, 0),
                        (0, 1, 0), (0, -1, 0),
                        (0, 0, 1), (0, 0, -1),
                    ):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < side and 0 <= ny < side and 0 <= nz < side:
                            self.adj[i].append(self.site_index(nx, ny, nz))

        self.lap = self._build_laplacian()

    def site_index(self, x: int, y: int, z: int) -> int:
        return x * self.side**2 + y * self.side + z

    def gaussian_wavepacket(self, center_phys, sigma=SIGMA):
        """Gaussian centered at physical coordinates."""
        psi = np.zeros(self.n, dtype=complex)
        cx, cy, cz = center_phys
        for i in range(self.n):
            px, py, pz = self.pos[i]
            r2 = (px - cx)**2 + (py - cy)**2 + (pz - cz)**2
            psi[i] = np.exp(-r2 / (2 * sigma**2))
        psi /= np.linalg.norm(psi)
        return psi

    def _build_laplacian(self):
        """Discrete Laplacian scaled by 1/a^2 for correct continuum limit."""
        rows, cols, vals = [], [], []
        inv_a2 = 1.0 / (self.a**2)
        for i in range(self.n):
            rows.append(i)
            cols.append(i)
            vals.append(-len(self.adj[i]) * inv_a2)
            for j in self.adj[i]:
                rows.append(i)
                cols.append(j)
                vals.append(inv_a2)
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def solve_poisson(self, rho, G, mu2):
        """Solve (lap - mu2 - reg) phi = -4pi G rho."""
        A = self.lap - mu2 * sparse.eye(self.n) - REG * sparse.eye(self.n)
        rhs = -4.0 * np.pi * G * rho
        return spsolve(A.tocsc(), rhs).real

    def build_wilson_hamiltonian(self, phi):
        """Wilson Hamiltonian with hopping scaled by 1/(2a)."""
        rows, cols, vals = [], [], []
        w_hop = 1.0 / (2.0 * self.a)
        w_wilson = WILSON_R / (2.0 * self.a)

        for i in range(self.n):
            for j in self.adj[i]:
                if j <= i:
                    continue
                rows.append(i)
                cols.append(j)
                vals.append(-0.5j * w_hop + w_wilson)
                rows.append(j)
                cols.append(i)
                vals.append(+0.5j * w_hop + w_wilson)

            diag = MASS + phi[i] + w_wilson * len(self.adj[i])
            rows.append(i)
            cols.append(i)
            vals.append(diag)

        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def center_of_mass_x(self, psi):
        """Physical x-coordinate of center of mass."""
        rho = np.abs(psi)**2
        return float(np.sum(rho * self.pos[:, 0]) / max(np.sum(rho), 1e-30))

    def evolve_step(self, psi, H):
        return expm_multiply(-1j * DT * H, psi)

    def run_mode(self, mode, center_a_phys, center_b_phys):
        """Run SHARED or SELF_ONLY at fixed G, mu2."""
        psi_a = self.gaussian_wavepacket(center_a_phys)
        psi_b = self.gaussian_wavepacket(center_b_phys)

        seps = np.zeros(N_STEPS + 1)
        seps[0] = self.center_of_mass_x(psi_b) - self.center_of_mass_x(psi_a)

        for t in range(N_STEPS):
            if mode == "FREE":
                phi_a = np.zeros(self.n)
                phi_b = np.zeros(self.n)
            elif mode == "SHARED":
                rho_total = np.abs(psi_a)**2 + np.abs(psi_b)**2
                phi_shared = self.solve_poisson(rho_total, G_VAL, MU2_VAL)
                phi_a = phi_shared
                phi_b = phi_shared
            elif mode == "SELF_ONLY":
                phi_a = self.solve_poisson(np.abs(psi_a)**2, G_VAL, MU2_VAL)
                phi_b = self.solve_poisson(np.abs(psi_b)**2, G_VAL, MU2_VAL)
            else:
                raise ValueError(f"Unknown mode: {mode}")

            H_a = self.build_wilson_hamiltonian(phi_a)
            H_b = self.build_wilson_hamiltonian(phi_b)
            psi_a = self.evolve_step(psi_a, H_a)
            psi_b = self.evolve_step(psi_b, H_b)
            psi_a /= np.linalg.norm(psi_a)
            psi_b /= np.linalg.norm(psi_b)
            seps[t + 1] = self.center_of_mass_x(psi_b) - self.center_of_mass_x(psi_a)

        return seps


def acceleration(sep):
    a = np.zeros(len(sep))
    a[1:-1] = (sep[2:] - 2 * sep[1:-1] + sep[:-2]) / DT**2
    a[0] = a[1]
    a[-1] = a[-2]
    return a


def mutual_accel(lat, center_a_phys, center_b_phys):
    """Return early-time mutual acceleration (SHARED - SELF_ONLY)."""
    sep_sh = lat.run_mode("SHARED", center_a_phys, center_b_phys)
    sep_so = lat.run_mode("SELF_ONLY", center_a_phys, center_b_phys)
    a_mut = acceleration(sep_sh) - acceleration(sep_so)
    early = slice(2, min(6, N_STEPS + 1))
    mean = float(np.mean(a_mut[early]))
    std = float(np.std(a_mut[early]))
    snr = abs(mean) / (std + 1e-12)
    return mean, std, snr


def power_law_fit(xs, ys):
    lx = np.log(np.asarray(xs, dtype=float))
    ly = np.log(np.asarray(ys, dtype=float))
    slope, intercept = np.polyfit(lx, ly, 1)
    fit = slope * lx + intercept
    ss_res = float(np.sum((ly - fit)**2))
    ss_tot = float(np.sum((ly - np.mean(ly))**2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return slope, intercept, r2


def label(mean, snr):
    signal = "ATTRACT" if mean < -1e-6 else ("REPEL" if mean > 1e-6 else "NULL")
    quality = "CLEAN" if snr > 2.0 else ("MARGINAL" if snr > 1.0 else "NOISY")
    return signal, quality


def section_1_fixed_side_sweep():
    """Side sweep at fixed lattice separation d=4."""
    print("=" * 88)
    print("SECTION 1: Fixed-side sweep (a=1, d=4 lattice units)")
    print("=" * 88)

    results = []
    for side in (9, 11, 13, 15):
        t0 = time.time()
        lat = RefinedWilsonLattice(side, a=1.0)
        c = side // 2
        ca = (c - 2.0, float(c), float(c))
        cb = (c + 2.0, float(c), float(c))
        mean, std, snr = mutual_accel(lat, ca, cb)
        elapsed = time.time() - t0
        sig, qual = label(mean, snr)
        results.append((side, 4, abs(mean), snr, sig, qual))
        print(
            f"  side={side:2d}: a_mut={mean:+.6f} +/- {std:.6f} "
            f"SNR={snr:.2f} [{sig}] [{qual}] ({elapsed:.1f}s)"
        )

    return results


def section_2_distance_sweep():
    """Distance sweep at side=13, a=1."""
    print()
    print("=" * 88)
    print("SECTION 2: Distance sweep (side=13, a=1)")
    print("=" * 88)

    results = []
    lat = RefinedWilsonLattice(13, a=1.0)
    c = 13 // 2

    for d in (3, 4, 5, 6, 7):
        t0 = time.time()
        half = d / 2.0
        ca = (c - half, float(c), float(c))
        cb = (c + half, float(c), float(c))
        mean, std, snr = mutual_accel(lat, ca, cb)
        elapsed = time.time() - t0
        sig, qual = label(mean, snr)
        results.append((13, d, abs(mean), snr, sig, qual))
        print(
            f"  d={d}: a_mut={mean:+.6f} +/- {std:.6f} "
            f"SNR={snr:.2f} [{sig}] [{qual}] ({elapsed:.1f}s)"
        )

    fit_pts = [(d, amp) for _, d, amp, snr, sig, qual in results
               if sig == "ATTRACT" and qual in ("CLEAN", "MARGINAL")]
    if len(fit_pts) >= 2:
        slope, _, r2 = power_law_fit(
            [d for d, _ in fit_pts], [amp for _, amp in fit_pts]
        )
        print(f"\n  Exponent at side=13: |a_mut| ~ d^{slope:.3f}  (R^2={r2:.4f})")
    else:
        print("\n  Insufficient clean attract points for fit.")

    return results


def section_3_true_refinement():
    """
    True lattice refinement: fixed physical box L=9, physical separation D=4.
    Decrease a to increase resolution.
    """
    print()
    print("=" * 88)
    print("SECTION 3: True lattice refinement (L_phys=9, D_phys=4)")
    print("=" * 88)
    print("  a=1.0 -> side=9,  d_lat=4")
    print("  a=0.7 -> side=13, d_lat=6  (4/0.7=5.7)")
    print("  a=0.5 -> side=18, d_lat=8")
    print()

    configs = [
        (9,  1.0, 4),
        (13, 0.7, 6),
        (18, 0.5, 8),
    ]

    results = []
    for side, a, d_lat in configs:
        t0 = time.time()
        lat = RefinedWilsonLattice(side, a=a)

        phys_center = (side * a) / 2.0
        D_phys = d_lat * a
        half_D = D_phys / 2.0
        ca = (phys_center - half_D, phys_center, phys_center)
        cb = (phys_center + half_D, phys_center, phys_center)

        mean, std, snr = mutual_accel(lat, ca, cb)
        elapsed = time.time() - t0
        sig, qual = label(mean, snr)

        results.append({
            "side": side, "a": a, "d_lat": d_lat,
            "D_phys": D_phys,
            "a_mut": mean, "std": std, "snr": snr,
            "sig": sig, "qual": qual,
        })
        print(
            f"  a={a:.1f} side={side:2d} d_lat={d_lat}: "
            f"D_phys={D_phys:.2f} a_mut={mean:+.6f} +/- {std:.6f} "
            f"SNR={snr:.2f} [{sig}] [{qual}] ({elapsed:.1f}s)"
        )

    return results


def section_4_multi_distance_refinement():
    """
    At each lattice spacing, sweep physical separations and extract exponent.
    Does the exponent soften toward -2.0 as a -> 0?
    """
    print()
    print("=" * 88)
    print("SECTION 4: Multi-distance refinement (exponent vs lattice spacing)")
    print("=" * 88)

    refinement_configs = [
        (9,  1.0),
        (13, 0.7),
    ]
    # side=18 (a=0.5) would be 5832 nodes; include if side=13 is fast enough
    include_18 = True

    all_exponents = []

    for side, a in refinement_configs:
        print(f"\n  --- a={a:.1f}, side={side} ---")
        lat = RefinedWilsonLattice(side, a=a)
        phys_center = (side * a) / 2.0

        phys_dists = [3.0, 4.0, 5.0, 6.0]
        row_data = []

        for D_phys in phys_dists:
            d_lat = round(D_phys / a)
            if d_lat < 2 or d_lat >= side - 2:
                print(f"    D={D_phys:.1f} -> d_lat={d_lat} out of range, skip")
                continue

            t0 = time.time()
            half_D = D_phys / 2.0
            ca = (phys_center - half_D, phys_center, phys_center)
            cb = (phys_center + half_D, phys_center, phys_center)
            mean, std, snr = mutual_accel(lat, ca, cb)
            elapsed = time.time() - t0
            sig, qual = label(mean, snr)
            row_data.append((D_phys, abs(mean), snr, sig, qual))
            print(
                f"    D={D_phys:.1f} (d_lat={d_lat}): "
                f"a_mut={mean:+.6f} SNR={snr:.2f} [{sig}] [{qual}] ({elapsed:.1f}s)"
            )

        fit_pts = [(D, amp) for D, amp, snr, sig, qual in row_data
                   if sig == "ATTRACT" and snr > 1.0]
        if len(fit_pts) >= 2:
            slope, _, r2 = power_law_fit(
                [D for D, _ in fit_pts], [amp for _, amp in fit_pts]
            )
            all_exponents.append((a, side, slope, r2, len(fit_pts)))
            print(f"    Exponent: |a_mut| ~ D^{slope:.3f}  (R^2={r2:.4f}, {len(fit_pts)} pts)")
        else:
            all_exponents.append((a, side, float("nan"), 0.0, len(fit_pts)))
            print(f"    Insufficient points for fit ({len(fit_pts)} usable)")

    if include_18:
        side, a = 18, 0.5
        print(f"\n  --- a={a:.1f}, side={side} (may be slow: {side**3} nodes) ---")
        lat = RefinedWilsonLattice(side, a=a)
        phys_center = (side * a) / 2.0

        phys_dists = [3.0, 4.0, 5.0, 6.0]
        row_data = []

        for D_phys in phys_dists:
            d_lat = round(D_phys / a)
            if d_lat < 2 or d_lat >= side - 2:
                print(f"    D={D_phys:.1f} -> d_lat={d_lat} out of range, skip")
                continue

            t0 = time.time()
            half_D = D_phys / 2.0
            ca = (phys_center - half_D, phys_center, phys_center)
            cb = (phys_center + half_D, phys_center, phys_center)
            mean, std, snr = mutual_accel(lat, ca, cb)
            elapsed = time.time() - t0
            sig, qual = label(mean, snr)
            row_data.append((D_phys, abs(mean), snr, sig, qual))
            print(
                f"    D={D_phys:.1f} (d_lat={d_lat}): "
                f"a_mut={mean:+.6f} SNR={snr:.2f} [{sig}] [{qual}] ({elapsed:.1f}s)"
            )

        fit_pts = [(D, amp) for D, amp, snr, sig, qual in row_data
                   if sig == "ATTRACT" and snr > 1.0]
        if len(fit_pts) >= 2:
            slope, _, r2 = power_law_fit(
                [D for D, _ in fit_pts], [amp for _, amp in fit_pts]
            )
            all_exponents.append((a, side, slope, r2, len(fit_pts)))
            print(f"    Exponent: |a_mut| ~ D^{slope:.3f}  (R^2={r2:.4f}, {len(fit_pts)} pts)")
        else:
            all_exponents.append((a, side, float("nan"), 0.0, len(fit_pts)))
            print(f"    Insufficient points for fit ({len(fit_pts)} usable)")

    return all_exponents


def main():
    print("=" * 88)
    print("WILSON TWO-BODY LATTICE REFINEMENT TEST")
    print("=" * 88)
    print(f"MASS={MASS}, WILSON_R={WILSON_R}, DT={DT}, REG={REG}, N_STEPS={N_STEPS}")
    print(f"G={G_VAL}, mu2={MU2_VAL}, sigma={SIGMA}")
    print("Question: does exponent (-3.4) soften toward Newton (-2.0) as a->0?")
    print()

    t_total = time.time()

    section_1_fixed_side_sweep()
    dist_results = section_2_distance_sweep()
    section_3_true_refinement()
    exponents = section_4_multi_distance_refinement()

    print()
    print("=" * 88)
    print("SUMMARY: Exponent vs lattice spacing")
    print("=" * 88)
    print(f"{'a':>6s} {'side':>6s} {'exponent':>10s} {'R2':>8s} {'pts':>4s}")
    print("-" * 40)
    for a, side, slope, r2, npts in exponents:
        if math.isnan(slope):
            print(f"{a:6.2f} {side:6d} {'N/A':>10s} {'N/A':>8s} {npts:4d}")
        else:
            print(f"{a:6.2f} {side:6d} {slope:10.3f} {r2:8.4f} {npts:4d}")

    newton_exp = -2.0
    valid = [(a, slope) for a, _, slope, r2, npts in exponents
             if not math.isnan(slope) and npts >= 2]
    if len(valid) >= 2:
        a_vals = [a for a, _ in valid]
        s_vals = [s for _, s in valid]
        print(f"\nExponent trend: a={a_vals} -> exp={[f'{s:.2f}' for s in s_vals]}")
        if s_vals[-1] > s_vals[0]:
            print("Direction: exponent INCREASING (softening toward Newton)")
        else:
            print("Direction: exponent DECREASING (steepening away from Newton)")
        print(f"Newton target: {newton_exp:.1f}")
        gap = abs(s_vals[-1] - newton_exp)
        print(f"Gap from Newton at finest a: {gap:.2f}")

    elapsed_total = time.time() - t_total
    print(f"\nTotal runtime: {elapsed_total:.1f}s")


if __name__ == "__main__":
    main()
