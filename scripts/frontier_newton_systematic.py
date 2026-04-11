#!/usr/bin/env python3
"""
Systematic Newton exponent study on open-boundary Wilson lattices.

Goal:
  Determine whether the near-`-2` distance-law exponent for the Wilson
  mutual-channel observable is robust across lattice sizes and coupling
  strengths on one fixed open-boundary surface.

Protocol:
  - Open 3D Wilson lattice (no periodic images)
  - Wilson Hamiltonian: complex hopping with WILSON_R=1.0
  - Poisson with the same `-4*pi*G*rho` convention used by the audited
    open-Wilson runners
  - Mutual acceleration = a(SHARED) - a(SELF_ONLY)
  - Power-law fit: log|a_mutual| vs log(d)
  - Report: side x G -> exponent +/- stderr

Conventions (matching frontier_wilson_two_body_open.py):
  H = diag(MASS + phi + 0.5*WILSON_R*degree)
      + (-0.5j + 0.5*WILSON_R) * adj_upper
      + (+0.5j + 0.5*WILSON_R) * adj_lower
  Poisson: (lap - mu2*I - REG*I) phi = -4*pi*G*rho

Important note:
  This runner does not by itself settle the normalization debate from the
  broader frontier narrative. It is only a same-convention systematic sweep of
  the open-Wilson lane. Use it to test robustness *within that lane*, not to
  claim that `4*pi` was or was not the source of earlier discrepancies across
  different runners.
"""

from __future__ import annotations

import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply, spsolve


# ── Physics constants (matching baseline that gave -2.02) ──
MASS = 0.30
WILSON_R = 1.0
DT = 0.08
REG = 1e-3
N_STEPS = 20
SIGMA = 1.0
MU2 = 0.001

# ── Sweep grid ──
SIDES = [15, 20, 25]
G_VALUES = [2.0, 5.0, 10.0]
DISTANCES = [3, 5, 7, 9, 11, 13]


class OpenWilsonLattice:
    """Open-boundary 3D cubic lattice with Wilson fermion Hamiltonian.

    Fully vectorized construction -- no Python loops over sites.
    """

    def __init__(self, side: int):
        self.side = side
        self.n = side ** 3

        # Position array: shape (n, 3)
        xs = np.arange(side)
        gx, gy, gz = np.meshgrid(xs, xs, xs, indexing="ij")
        self.pos = np.column_stack([gx.ravel(), gy.ravel(), gz.ravel()])

        # Build adjacency (sparse) and Laplacian vectorized
        self._build_sparse_structures()

    def _build_sparse_structures(self):
        s = self.side
        n = self.n
        idx = np.arange(n).reshape(s, s, s)

        row_list, col_list = [], []
        # +x neighbors
        row_list.append(idx[:-1, :, :].ravel())
        col_list.append(idx[1:, :, :].ravel())
        # +y neighbors
        row_list.append(idx[:, :-1, :].ravel())
        col_list.append(idx[:, 1:, :].ravel())
        # +z neighbors
        row_list.append(idx[:, :, :-1].ravel())
        col_list.append(idx[:, :, 1:].ravel())

        # Forward edges (i < j for each direction)
        fwd_rows = np.concatenate(row_list)
        fwd_cols = np.concatenate(col_list)

        # Full adjacency = forward + backward
        adj_rows = np.concatenate([fwd_rows, fwd_cols])
        adj_cols = np.concatenate([fwd_cols, fwd_rows])
        n_edges = len(adj_rows)

        # Adjacency matrix (unweighted)
        ones = np.ones(n_edges)
        adj = sparse.csr_matrix((ones, (adj_rows, adj_cols)), shape=(n, n))

        # Degree vector
        self.degree = np.array(adj.sum(axis=1)).ravel()

        # Laplacian = adj - diag(degree)
        self.lap = adj - sparse.diags(self.degree, format="csr")

        # Store forward edges for Hamiltonian
        self.fwd_rows = fwd_rows
        self.fwd_cols = fwd_cols

        # Precompute Poisson LHS (constant since mu2 is fixed)
        self._poisson_A = (
            self.lap - (MU2 + REG) * sparse.eye(n)
        ).tocsc()

        # Precompute static part of Hamiltonian (hopping + Wilson off-diag)
        n_fwd = len(fwd_rows)
        # Forward: (-0.5j + 0.5*WILSON_R), Backward: (+0.5j + 0.5*WILSON_R)
        hop_fwd = np.full(n_fwd, -0.5j + 0.5 * WILSON_R)
        hop_bwd = np.full(n_fwd, +0.5j + 0.5 * WILSON_R)

        h_rows = np.concatenate([fwd_rows, fwd_cols])
        h_cols = np.concatenate([fwd_cols, fwd_rows])
        h_vals = np.concatenate([hop_fwd, hop_bwd])

        self._H_offdiag = sparse.csr_matrix(
            (h_vals, (h_rows, h_cols)), shape=(n, n)
        )
        # Static diagonal contribution: MASS + 0.5*WILSON_R*degree
        self._H_diag_static = MASS + 0.5 * WILSON_R * self.degree

    def gaussian_wavepacket(self, center, sigma=SIGMA):
        c = np.asarray(center, dtype=float)
        r2 = np.sum((self.pos - c) ** 2, axis=1)
        psi = np.exp(-r2 / (2 * sigma ** 2)).astype(complex)
        psi /= np.linalg.norm(psi)
        return psi

    def solve_poisson(self, rho, G):
        rhs = -4.0 * np.pi * G * rho
        return spsolve(self._poisson_A, rhs).real

    def build_wilson_hamiltonian(self, phi):
        diag_vals = self._H_diag_static + phi
        return self._H_offdiag + sparse.diags(diag_vals, format="csr")

    def center_of_mass_x(self, psi):
        rho = np.abs(psi) ** 2
        return float(np.dot(rho, self.pos[:, 0]) / max(np.sum(rho), 1e-30))

    def evolve_step(self, psi, H):
        return expm_multiply(-1j * DT * H, psi)


def acceleration(sep):
    a = np.zeros(len(sep))
    a[1:-1] = (sep[2:] - 2 * sep[1:-1] + sep[:-2]) / DT ** 2
    a[0] = a[1]
    a[-1] = a[-2]
    return a


def run_config(lat: OpenWilsonLattice, G_val: float, d: int):
    """Run SHARED and SELF_ONLY modes, return mutual acceleration stats."""
    side = lat.side
    center = side // 2
    x_a = center - d // 2
    x_b = center + (d - d // 2)

    if x_a < 1 or x_b >= side - 1:
        return None

    center_a = (x_a, center, center)
    center_b = (x_b, center, center)

    psi_a0 = lat.gaussian_wavepacket(center_a)
    psi_b0 = lat.gaussian_wavepacket(center_b)

    seps = {}
    for mode in ("SHARED", "SELF_ONLY"):
        psi_a = psi_a0.copy()
        psi_b = psi_b0.copy()
        sep_t = np.zeros(N_STEPS + 1)
        sep_t[0] = lat.center_of_mass_x(psi_b) - lat.center_of_mass_x(psi_a)

        for t in range(N_STEPS):
            rho_a = np.abs(psi_a) ** 2
            rho_b = np.abs(psi_b) ** 2
            if mode == "SHARED":
                phi = lat.solve_poisson(rho_a + rho_b, G_val)
                phi_a = phi_b = phi
            else:
                phi_a = lat.solve_poisson(rho_a, G_val)
                phi_b = lat.solve_poisson(rho_b, G_val)

            H_a = lat.build_wilson_hamiltonian(phi_a)
            H_b = lat.build_wilson_hamiltonian(phi_b)
            psi_a = lat.evolve_step(psi_a, H_a)
            psi_b = lat.evolve_step(psi_b, H_b)
            psi_a /= np.linalg.norm(psi_a)
            psi_b /= np.linalg.norm(psi_b)
            sep_t[t + 1] = lat.center_of_mass_x(psi_b) - lat.center_of_mass_x(psi_a)

        seps[mode] = sep_t

    a_mut = acceleration(seps["SHARED"]) - acceleration(seps["SELF_ONLY"])
    early = slice(2, min(11, N_STEPS + 1))
    mean_val = float(np.mean(a_mut[early]))
    std_val = float(np.std(a_mut[early]))
    snr = abs(mean_val) / (std_val + 1e-12)

    return {
        "d": d,
        "a_mutual_mean": mean_val,
        "a_mutual_std": std_val,
        "snr": snr,
    }


def power_law_fit(ds, amps):
    """Fit log|amp| = alpha * log(d) + const.  Return alpha, stderr, R^2."""
    lx = np.log(np.asarray(ds, dtype=float))
    ly = np.log(np.asarray(amps, dtype=float))
    n = len(lx)
    slope, intercept = np.polyfit(lx, ly, 1)
    fit = slope * lx + intercept
    ss_res = float(np.sum((ly - fit) ** 2))
    ss_tot = float(np.sum((ly - np.mean(ly)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    if n > 2 and ss_tot > 0:
        mse = ss_res / (n - 2)
        sx2 = float(np.sum((lx - np.mean(lx)) ** 2))
        se = np.sqrt(mse / sx2) if sx2 > 0 else float("inf")
    else:
        se = float("inf")
    return float(slope), float(se), float(r2)


def main():
    print("=" * 96)
    print("SYSTEMATIC NEWTON EXPONENT STUDY")
    print("=" * 96)
    print(f"MASS={MASS}, WILSON_R={WILSON_R}, DT={DT}, mu2={MU2}, SIGMA={SIGMA}")
    print(f"Lattice sides: {SIDES}")
    print(f"G values:      {G_VALUES}")
    print(f"Separations:   {DISTANCES}")
    print(f"Open BC, complex Wilson hopping, Poisson with 4*pi*G")
    print()

    # Pre-build lattices
    lattices = {}
    for side in SIDES:
        t0 = time.time()
        print(f"Building L={side} lattice ({side**3} sites)...", end=" ", flush=True)
        lattices[side] = OpenWilsonLattice(side)
        print(f"{time.time()-t0:.1f}s")
    print()

    results = {}
    all_rows = []

    for side in SIDES:
        lat = lattices[side]
        for G in G_VALUES:
            label = f"L={side:2d}, G={G:5.1f}"
            print(f"--- {label} ---")
            rows = []
            t_config = time.time()

            for d in DISTANCES:
                if d >= side - 2:
                    print(f"  d={d:2d}: SKIP (too close to boundary)")
                    continue
                t0 = time.time()
                result = run_config(lat, G, d)
                elapsed = time.time() - t0
                if result is None:
                    print(f"  d={d:2d}: SKIP (placement out of bounds)")
                    continue

                signal = "ATTRACT" if result["a_mutual_mean"] < -1e-6 else (
                    "REPEL" if result["a_mutual_mean"] > 1e-6 else "NULL")
                quality = "CLEAN" if result["snr"] > 2.0 else (
                    "MARGINAL" if result["snr"] > 1.0 else "NOISY")
                rows.append(result)
                all_rows.append({"side": side, "G": G, **result})
                print(
                    f"  d={d:2d}: a_mut={result['a_mutual_mean']:+.6f} "
                    f"SNR={result['snr']:.2f} [{signal:7s}] [{quality:8s}] "
                    f"({elapsed:.1f}s)"
                )

            # Fit on clean attractive rows
            clean_attract = [
                r for r in rows
                if r["a_mutual_mean"] < -1e-6 and r["snr"] > 2.0
            ]
            n_attract = sum(1 for r in rows if r["a_mutual_mean"] < -1e-6)
            n_total = len(rows)

            if len(clean_attract) >= 3:
                ds = [r["d"] for r in clean_attract]
                amps = [abs(r["a_mutual_mean"]) for r in clean_attract]
                alpha, se, r2 = power_law_fit(ds, amps)
                results[(side, G)] = (alpha, se, r2, len(clean_attract), n_total)
                print(
                    f"  FIT: alpha={alpha:+.3f} +/- {se:.3f}  "
                    f"R^2={r2:.4f}  (N_clean={len(clean_attract)}/{n_total})"
                )
            elif len(clean_attract) == 2:
                ds = [r["d"] for r in clean_attract]
                amps = [abs(r["a_mutual_mean"]) for r in clean_attract]
                alpha, se, r2 = power_law_fit(ds, amps)
                results[(side, G)] = (alpha, se, r2, 2, n_total)
                print(
                    f"  FIT (2-pt): alpha={alpha:+.3f}  "
                    f"(R^2=N/A, N_clean=2/{n_total})"
                )
            else:
                results[(side, G)] = (float("nan"), float("nan"), float("nan"),
                                      len(clean_attract), n_total)
                print(f"  FIT: insufficient clean attractive points ({len(clean_attract)}/{n_total})")

            elapsed_total = time.time() - t_config
            print(f"  ({elapsed_total:.1f}s total)")
            print()

    # ── Summary table ──
    print("=" * 96)
    print("SUMMARY TABLE: Newton exponent alpha (|a_mut| ~ d^alpha)")
    print("=" * 96)
    print(f"{'':8s}", end="")
    for G in G_VALUES:
        print(f"{'G='+str(G):>22s}", end="")
    print()
    print("-" * (8 + 22 * len(G_VALUES)))

    for side in SIDES:
        print(f"L={side:2d}    ", end="")
        for G in G_VALUES:
            key = (side, G)
            if key in results:
                alpha, se, r2, nc, nt = results[key]
                if np.isfinite(alpha):
                    if np.isfinite(se) and se < 10:
                        print(f"  {alpha:+.2f} +/- {se:.2f} (n={nc})", end="")
                    else:
                        print(f"  {alpha:+.2f}       (n={nc})", end="")
                else:
                    print(f"  {'---':>20s}", end="")
            else:
                print(f"  {'N/A':>20s}", end="")
        print()

    print("-" * (8 + 22 * len(G_VALUES)))
    print()

    # ── Global fit across all clean attractive rows ──
    global_clean = [
        r for r in all_rows
        if r["a_mutual_mean"] < -1e-6 and r["snr"] > 2.0
    ]
    if len(global_clean) >= 3:
        ds = [r["d"] for r in global_clean]
        amps = [abs(r["a_mutual_mean"]) for r in global_clean]
        alpha, se, r2 = power_law_fit(ds, amps)
        print(f"GLOBAL FIT (all configs pooled): alpha={alpha:+.3f} +/- {se:.3f}  "
              f"R^2={r2:.4f}  N={len(global_clean)}")
    else:
        print(f"GLOBAL FIT: insufficient clean attractive points ({len(global_clean)})")

    print()
    print("KEY QUESTION: Is alpha ~ -2.0 robust across lattice sizes and couplings?")
    alphas = [results[k][0] for k in results if np.isfinite(results[k][0])]
    if alphas:
        mean_a = np.mean(alphas)
        std_a = np.std(alphas)
        print(f"  Mean alpha = {mean_a:+.3f} +/- {std_a:.3f}  (N={len(alphas)} configs)")
        if abs(mean_a + 2.0) < 2 * max(std_a, 0.01):
            print("  CONSISTENT with -2.0 (inverse-square law)")
        else:
            print(f"  DEVIATES from -2.0 by {abs(mean_a + 2.0)/max(std_a, 0.01):.1f} sigma")


if __name__ == "__main__":
    main()
