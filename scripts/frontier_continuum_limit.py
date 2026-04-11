#!/usr/bin/env python3
"""
Continuum limit of the Wilson two-body inverse-square law.

Goal:
  Test whether the distance-law exponent converges to exactly -2.0
  as the lattice becomes finer (larger side at fixed physical problem).

Method:
  For each lattice side L in [12, 15, 18, 20, 22, 25]:
    1. Place two masses at separations that are fixed FRACTIONS of L
       (d/L = 0.2, 0.3, 0.4, 0.5, 0.6) so that we probe the same
       relative geometry at every resolution.
    2. Fit |a_mutual| ~ d^alpha using the clean attractive points.
    3. Record alpha(L), amplitude at d/L=0.3, and R^2.

  Then extrapolate:
    alpha(L) = alpha_inf + c / L^p

  If alpha_inf = -2.000 +/- small error, we have a Nature-level
  statement: the continuum limit reproduces Newton's inverse-square law.

Parameters: G=5, mu2=0.001, MASS=0.3, WILSON_R=1.0, DT=0.08, N_STEPS=15
"""

from __future__ import annotations

import time
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply, spsolve
from scipy.optimize import curve_fit


# ── Physics parameters ──────────────────────────────────────────────────
MASS = 0.30
WILSON_R = 1.0
DT = 0.08
REG = 1e-3
N_STEPS = 15
SIGMA = 1.0
G_VAL = 5.0
MU2_VAL = 0.001


# ── Lattice infrastructure (from frontier_wilson_two_body_open.py) ──────
class OpenWilsonLattice:
    def __init__(self, side: int):
        self.side = side
        self.n = side ** 3
        self.pos = np.zeros((self.n, 3))
        self.adj: dict[int, list[int]] = {}
        for x in range(side):
            for y in range(side):
                for z in range(side):
                    i = self.site_index(x, y, z)
                    self.pos[i] = [x, y, z]
                    self.adj[i] = []
                    for dx, dy, dz in (
                        (1, 0, 0), (-1, 0, 0),
                        (0, 1, 0), (0, -1, 0),
                        (0, 0, 1), (0, 0, -1),
                    ):
                        nx_, ny_, nz_ = x + dx, y + dy, z + dz
                        if 0 <= nx_ < side and 0 <= ny_ < side and 0 <= nz_ < side:
                            self.adj[i].append(self.site_index(nx_, ny_, nz_))
        self.lap = self._build_laplacian()

    def site_index(self, x: int, y: int, z: int):
        return x * self.side ** 2 + y * self.side + z

    def _build_laplacian(self):
        rows, cols, vals = [], [], []
        for i in range(self.n):
            rows.append(i)
            cols.append(i)
            vals.append(-len(self.adj[i]))
            for j in self.adj[i]:
                rows.append(i)
                cols.append(j)
                vals.append(1.0)
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def gaussian_wavepacket(self, center, sigma=SIGMA):
        psi = np.zeros(self.n, dtype=complex)
        cx, cy, cz = center
        r2 = ((self.pos[:, 0] - cx) ** 2
              + (self.pos[:, 1] - cy) ** 2
              + (self.pos[:, 2] - cz) ** 2)
        psi = np.exp(-r2 / (2 * sigma ** 2)).astype(complex)
        psi /= np.linalg.norm(psi)
        return psi

    def solve_poisson(self, rho):
        A = self.lap - MU2_VAL * sparse.eye(self.n) - REG * sparse.eye(self.n)
        rhs = -4.0 * np.pi * G_VAL * rho
        return spsolve(A.tocsc(), rhs).real

    def build_wilson_hamiltonian(self, phi):
        rows, cols, vals = [], [], []
        for i in range(self.n):
            for j in self.adj[i]:
                if j <= i:
                    continue
                rows.append(i)
                cols.append(j)
                vals.append(-0.5j + 0.5 * WILSON_R)
                rows.append(j)
                cols.append(i)
                vals.append(+0.5j + 0.5 * WILSON_R)
            diag = MASS + phi[i] + 0.5 * WILSON_R * len(self.adj[i])
            rows.append(i)
            cols.append(i)
            vals.append(diag)
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def center_of_mass_x(self, psi):
        rho = np.abs(psi) ** 2
        return float(np.sum(rho * self.pos[:, 0]) / max(np.sum(rho), 1e-30))

    def evolve_step(self, psi, H):
        return expm_multiply(-1j * DT * H, psi)

    def run_mode(self, mode, center_a, center_b):
        psi_a = self.gaussian_wavepacket(center_a)
        psi_b = self.gaussian_wavepacket(center_b)

        seps = np.zeros(N_STEPS + 1)
        seps[0] = self.center_of_mass_x(psi_b) - self.center_of_mass_x(psi_a)

        phi_frozen = None
        if mode == "FROZEN":
            rho_total = np.abs(psi_a) ** 2 + np.abs(psi_b) ** 2
            phi_frozen = self.solve_poisson(rho_total)

        for t in range(N_STEPS):
            if mode == "FREE":
                phi_a = np.zeros(self.n)
                phi_b = np.zeros(self.n)
            elif mode == "SHARED":
                rho_total = np.abs(psi_a) ** 2 + np.abs(psi_b) ** 2
                phi_shared = self.solve_poisson(rho_total)
                phi_a = phi_shared
                phi_b = phi_shared
            elif mode == "SELF_ONLY":
                phi_a = self.solve_poisson(np.abs(psi_a) ** 2)
                phi_b = self.solve_poisson(np.abs(psi_b) ** 2)
            else:
                phi_a = phi_frozen
                phi_b = phi_frozen

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
    a[1:-1] = (sep[2:] - 2 * sep[1:-1] + sep[:-2]) / DT ** 2
    a[0] = a[1]
    a[-1] = a[-2]
    return a


def mutual_acceleration(lat, d):
    """Run SHARED and SELF_ONLY, return mean mutual acceleration."""
    center = lat.side // 2
    x_a = center - d // 2
    x_b = center + (d - d // 2)
    center_a = (x_a, center, center)
    center_b = (x_b, center, center)

    sep_sh = lat.run_mode("SHARED", center_a, center_b)
    sep_so = lat.run_mode("SELF_ONLY", center_a, center_b)

    a_mut = acceleration(sep_sh) - acceleration(sep_so)
    early = slice(2, min(11, N_STEPS + 1))
    mean = float(np.mean(a_mut[early]))
    std = float(np.std(a_mut[early]))
    snr = abs(mean) / (std + 1e-12)
    return mean, std, snr


def power_law_fit(xs, ys):
    lx = np.log(np.asarray(xs, dtype=float))
    ly = np.log(np.asarray(ys, dtype=float))
    slope, intercept = np.polyfit(lx, ly, 1)
    fit_y = slope * lx + intercept
    ss_res = float(np.sum((ly - fit_y) ** 2))
    ss_tot = float(np.sum((ly - np.mean(ly)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return slope, np.exp(intercept), r2


def continuum_extrapolation(L_vals, alpha_vals, alpha_errs=None):
    """Fit alpha(L) = alpha_inf + c / L^p."""
    L = np.array(L_vals, dtype=float)
    alpha = np.array(alpha_vals, dtype=float)

    # Try fitting with free p
    def model_free(x, a_inf, c, p):
        return a_inf + c / x ** p

    # Try fitting with fixed p=1 (simplest finite-size correction)
    def model_p1(x, a_inf, c):
        return a_inf + c / x

    def model_p2(x, a_inf, c):
        return a_inf + c / x ** 2

    results = {}

    for name, model, p0, bounds in [
        ("p=1", model_p1, [-2.0, 1.0], ([-3.0, -100], [-1.0, 100])),
        ("p=2", model_p2, [-2.0, 10.0], ([-3.0, -1000], [-1.0, 1000])),
        ("p=free", model_free, [-2.0, 1.0, 1.0], ([-3.0, -1000, 0.1], [-1.0, 1000, 5.0])),
    ]:
        try:
            popt, pcov = curve_fit(model, L, alpha, p0=p0, bounds=bounds, maxfev=10000)
            perr = np.sqrt(np.diag(pcov))
            pred = model(L, *popt)
            ss_res = np.sum((alpha - pred) ** 2)
            ss_tot = np.sum((alpha - np.mean(alpha)) ** 2)
            r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
            results[name] = {
                "popt": popt,
                "perr": perr,
                "r2": r2,
                "alpha_inf": popt[0],
                "alpha_inf_err": perr[0],
            }
        except Exception as e:
            results[name] = {"error": str(e)}

    return results


def main():
    print("=" * 90)
    print("CONTINUUM LIMIT: WILSON TWO-BODY INVERSE-SQUARE LAW")
    print("=" * 90)
    print(f"G={G_VAL}, mu2={MU2_VAL}, MASS={MASS}, WILSON_R={WILSON_R}")
    print(f"DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print()
    print("Question: does alpha(L) -> -2.0 as L -> infinity?")
    print()

    # ── Test grid ────────────────────────────────────────────────────────
    lattice_sides = [12, 15, 18, 20, 22, 25]
    d_over_L_targets = [0.20, 0.30, 0.40, 0.50, 0.60]

    all_results = {}  # side -> list of (d, a_mean, a_std, snr)
    alphas = {}       # side -> (alpha, amplitude_at_ref, r2)

    total_t0 = time.time()

    for side in lattice_sides:
        print("-" * 90)
        print(f"L = {side}  (N = {side**3} sites)")
        print("-" * 90)

        t0 = time.time()
        lat = OpenWilsonLattice(side)
        t_build = time.time() - t0
        print(f"  Lattice built in {t_build:.1f}s")

        side_data = []
        for frac in d_over_L_targets:
            d = max(3, round(frac * side))
            if d >= side - 2:
                continue
            # Skip duplicate d values
            if any(dd == d for dd, _, _, _ in side_data):
                continue

            t1 = time.time()
            mean, std, snr = mutual_acceleration(lat, d)
            dt = time.time() - t1

            signal = "ATTRACT" if mean < -1e-6 else ("REPEL" if mean > 1e-6 else "NULL")
            quality = "CLEAN" if snr > 2.0 else ("MARGINAL" if snr > 1.0 else "NOISY")

            side_data.append((d, mean, std, snr))
            actual_frac = d / side
            print(f"  d={d:2d} (d/L={actual_frac:.2f}): "
                  f"a_mut={mean:+.6f} +/- {std:.6f} SNR={snr:.2f} "
                  f"[{signal}] [{quality}] ({dt:.1f}s)")

        all_results[side] = side_data

        # Fit power law for this side
        clean = [(d, abs(m)) for d, m, s, snr in side_data
                 if m < -1e-6 and snr > 2.0]
        if len(clean) >= 3:
            ds = [d for d, _ in clean]
            amps = [a for _, a in clean]
            alpha, amp0, r2 = power_law_fit(ds, amps)
            alphas[side] = (alpha, amp0, r2)
            print(f"  FIT: |a_mut| ~ d^{alpha:.4f}  (R^2={r2:.6f})")
        elif len(clean) == 2:
            ds = [d for d, _ in clean]
            amps = [a for _, a in clean]
            alpha, amp0, r2 = power_law_fit(ds, amps)
            alphas[side] = (alpha, amp0, r2)
            print(f"  FIT (2pt): |a_mut| ~ d^{alpha:.4f}  (R^2=N/A, 2 points)")
        else:
            print(f"  FIT: insufficient clean attractive points ({len(clean)})")

        elapsed = time.time() - t0
        print(f"  Side {side} total: {elapsed:.1f}s")
        print()

    total_elapsed = time.time() - total_t0

    # ── Summary table ────────────────────────────────────────────────────
    print("=" * 90)
    print("EXPONENT vs LATTICE SIZE")
    print("=" * 90)
    print(f"{'L':>4} | {'alpha':>10} | {'R^2':>10} | {'amplitude':>12} | {'delta(alpha+2)':>14}")
    print("-" * 60)

    L_fit = []
    alpha_fit = []
    for side in lattice_sides:
        if side in alphas:
            alpha, amp0, r2 = alphas[side]
            delta = alpha + 2.0
            L_fit.append(side)
            alpha_fit.append(alpha)
            print(f"{side:>4} | {alpha:>+10.4f} | {r2:>10.6f} | {amp0:>12.6f} | {delta:>+14.4f}")
        else:
            print(f"{side:>4} | {'N/A':>10} | {'N/A':>10} | {'N/A':>12} | {'N/A':>14}")

    # ── Amplitude convergence at fixed physical fraction ─────────────────
    print()
    print("=" * 90)
    print("AMPLITUDE at d/L ~ 0.3 (fixed physical separation fraction)")
    print("=" * 90)
    print(f"{'L':>4} | {'d':>4} | {'d/L':>6} | {'|a_mut|':>12}")
    print("-" * 35)
    for side in lattice_sides:
        if side not in all_results:
            continue
        target_d = round(0.3 * side)
        for d, m, s, snr in all_results[side]:
            if d == target_d and m < -1e-6:
                print(f"{side:>4} | {d:>4} | {d/side:>6.3f} | {abs(m):>12.6f}")

    # ── Continuum extrapolation ──────────────────────────────────────────
    print()
    print("=" * 90)
    print("CONTINUUM EXTRAPOLATION: alpha(L) = alpha_inf + c / L^p")
    print("=" * 90)

    if len(L_fit) >= 3:
        ext = continuum_extrapolation(L_fit, alpha_fit)
        for name in ["p=1", "p=2", "p=free"]:
            if name not in ext or "error" in ext[name]:
                err = ext.get(name, {}).get("error", "unknown")
                print(f"  {name}: fit failed ({err})")
                continue
            r = ext[name]
            popt = r["popt"]
            perr = r["perr"]
            a_inf = r["alpha_inf"]
            a_inf_err = r["alpha_inf_err"]
            delta = a_inf + 2.0

            if name == "p=free":
                print(f"  {name}: alpha_inf = {a_inf:.4f} +/- {a_inf_err:.4f}"
                      f"  c = {popt[1]:.3f} +/- {perr[1]:.3f}"
                      f"  p = {popt[2]:.3f} +/- {perr[2]:.3f}"
                      f"  R^2 = {r['r2']:.6f}")
            else:
                print(f"  {name}: alpha_inf = {a_inf:.4f} +/- {a_inf_err:.4f}"
                      f"  c = {popt[1]:.3f} +/- {perr[1]:.3f}"
                      f"  R^2 = {r['r2']:.6f}")
            print(f"         delta(alpha_inf + 2) = {delta:+.4f} +/- {a_inf_err:.4f}")

            # Hypothesis test: is alpha_inf consistent with -2.0?
            n_sigma = abs(delta) / a_inf_err if a_inf_err > 1e-10 else float("inf")
            if n_sigma < 1.0:
                verdict = "CONSISTENT with -2.0 at 1-sigma"
            elif n_sigma < 2.0:
                verdict = "CONSISTENT with -2.0 at 2-sigma"
            elif n_sigma < 3.0:
                verdict = "MARGINAL (2-3 sigma from -2.0)"
            else:
                verdict = f"INCONSISTENT ({n_sigma:.1f} sigma from -2.0)"
            print(f"         {verdict}")
            print()
    else:
        print("  Insufficient data for continuum extrapolation")
        print(f"  (need >= 3 lattice sizes with clean fits, have {len(L_fit)})")

    # ── R^2 trend ────────────────────────────────────────────────────────
    print("=" * 90)
    print("FIT QUALITY (R^2) vs LATTICE SIZE")
    print("=" * 90)
    print(f"{'L':>4} | {'R^2':>10} | {'quality':>20}")
    print("-" * 40)
    for side in lattice_sides:
        if side in alphas:
            _, _, r2 = alphas[side]
            if r2 > 0.999:
                quality = "EXCELLENT"
            elif r2 > 0.99:
                quality = "GOOD"
            elif r2 > 0.95:
                quality = "ACCEPTABLE"
            else:
                quality = "POOR"
            print(f"{side:>4} | {r2:>10.6f} | {quality:>20}")

    # ── Final verdict ────────────────────────────────────────────────────
    print()
    print("=" * 90)
    print("VERDICT")
    print("=" * 90)
    if len(L_fit) >= 3:
        # Use the best extrapolation model
        best = None
        for name in ["p=free", "p=1", "p=2"]:
            if name in ext and "error" not in ext[name]:
                if best is None or ext[name]["r2"] > ext[best]["r2"]:
                    best = name
        if best is not None:
            r = ext[best]
            a_inf = r["alpha_inf"]
            a_inf_err = r["alpha_inf_err"]
            delta = a_inf + 2.0
            n_sigma = abs(delta) / a_inf_err if a_inf_err > 1e-10 else float("inf")
            print(f"Best extrapolation model: {best}")
            print(f"  alpha_infinity = {a_inf:.4f} +/- {a_inf_err:.4f}")
            print(f"  deviation from -2.0: {delta:+.4f} ({n_sigma:.1f} sigma)")
            if n_sigma < 2.0:
                print()
                print("  *** CONTINUUM LIMIT IS CONSISTENT WITH NEWTON'S")
                print("      INVERSE-SQUARE LAW (alpha = -2.0) ***")
            elif n_sigma < 3.0:
                print()
                print("  Marginal consistency with -2.0 (2-3 sigma)")
            else:
                print()
                print(f"  Continuum limit deviates from -2.0 by {n_sigma:.1f} sigma")
                print(f"  alpha_infinity = {a_inf:.4f} is the intrinsic exponent")
        else:
            print("All extrapolation models failed")
    else:
        print("Insufficient data for continuum extrapolation")

    print()
    print(f"Total runtime: {total_elapsed:.0f}s")


if __name__ == "__main__":
    main()
